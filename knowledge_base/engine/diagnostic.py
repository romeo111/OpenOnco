"""Diagnostic-phase engine: pre-biopsy / pre-histology workup planning.

See specs/DIAGNOSTIC_MDT_SPEC.md for full design.

Hard rules (CHARTER §15.2 C7):
- generate_diagnostic_brief() rejects patient profiles that already have
  a confirmed `disease.id` or `disease.icd_o_3_morphology` — those go
  through generate_plan() instead.
- generate_plan() (in plan.py) was not modified by this commit; the
  diagnostic gate lives here. Mode auto-detection is the CLI's job.
- DiagnosticPlan has `mode='diagnostic'` and contains NO treatment
  tracks. There is no path through this module that produces an
  Indication, Regimen, or treatment recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from knowledge_base.schemas import (
    BiopsyApproach,
    DiagnosticPlan,
    DiagnosticWorkup,
    IHCPanel,
    SuspicionSnapshot,
    WorkupStep,
)
from knowledge_base.validation.loader import load_content


_DIAGNOSTIC_BANNER = (
    "DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE. "
    "Histology required before any therapy discussion (CHARTER §15.2 C7)."
)


@dataclass
class DiagnosticPlanResult:
    """In-memory engine output for diagnostic mode. Parallel to
    PlanResult for treatment mode but with NO tracks / regimens.
    """

    patient_id: Optional[str]
    suspicion: Optional[SuspicionSnapshot]
    diagnostic_plan: Optional[DiagnosticPlan] = None
    matched_workup_id: Optional[str] = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "suspicion": self.suspicion.model_dump() if self.suspicion else None,
            "matched_workup_id": self.matched_workup_id,
            "diagnostic_plan": (
                self.diagnostic_plan.model_dump() if self.diagnostic_plan else None
            ),
            "warnings": list(self.warnings),
            "diagnostic_banner": _DIAGNOSTIC_BANNER,
        }


# ── Mode detection ────────────────────────────────────────────────────────


def is_diagnostic_profile(patient: dict) -> bool:
    """True if patient profile is suitable for diagnostic mode:
    a `disease.suspicion` block is present AND no confirmed diagnosis
    fields (`disease.id` or `disease.icd_o_3_morphology`) are set."""

    disease = (patient or {}).get("disease") or {}
    has_confirmed = bool(disease.get("id") or disease.get("icd_o_3_morphology"))
    has_suspicion = bool(disease.get("suspicion"))
    return has_suspicion and not has_confirmed


def is_treatment_profile(patient: dict) -> bool:
    disease = (patient or {}).get("disease") or {}
    return bool(disease.get("id") or disease.get("icd_o_3_morphology"))


# ── Suspicion → workup matching ───────────────────────────────────────────


def _build_suspicion_snapshot(patient: dict) -> Optional[SuspicionSnapshot]:
    raw = ((patient or {}).get("disease") or {}).get("suspicion") or {}
    if not raw:
        return None
    return SuspicionSnapshot(
        lineage_hint=raw.get("lineage_hint"),
        tissue_locations=list(raw.get("tissue_locations") or []),
        icd_o_3_topography=list(raw.get("icd_o_3_topography") or []),
        presentation=raw.get("presentation"),
        working_hypotheses=list(raw.get("working_hypotheses") or []),
    )


def _match_workup(
    suspicion: SuspicionSnapshot, entities: dict
) -> Optional[dict]:
    """Score each DiagnosticWorkup against the suspicion; return the
    best match's raw data dict (or None if no workup matches at all).

    Score = number of overlapping items across (lineage_hints,
    tissue_locations, presentation_keywords). Ties broken by id sort."""

    suspicion_lineage = (suspicion.lineage_hint or "").lower().strip()
    suspicion_tissues = {t.lower().strip() for t in suspicion.tissue_locations}
    presentation_lower = (suspicion.presentation or "").lower()

    best_score = 0
    best: list[dict] = []
    for eid, info in entities.items():
        if info.get("type") != "workups":
            continue
        wkp = info.get("data") or {}
        applicable = wkp.get("applicable_to") or {}

        lineage_hits = 0
        for h in applicable.get("lineage_hints") or []:
            if h.lower().strip() == suspicion_lineage and suspicion_lineage:
                lineage_hits += 1
                break
        tissue_hits = sum(
            1
            for t in (applicable.get("tissue_locations") or [])
            if t.lower().strip() in suspicion_tissues
        )
        keyword_hits = sum(
            1
            for k in (applicable.get("presentation_keywords") or [])
            if k.lower() in presentation_lower
        )

        score = lineage_hits * 3 + tissue_hits + keyword_hits
        if score == 0:
            continue
        if score > best_score:
            best_score = score
            best = [wkp]
        elif score == best_score:
            best.append(wkp)

    if not best:
        return None
    best.sort(key=lambda w: w.get("id", ""))
    return best[0]


# ── Workup → workup steps materialisation ─────────────────────────────────


def _materialise_workup_steps(
    workup: dict,
    entities: dict,
    prior_tests_completed: Optional[list[str]] = None,
) -> list[WorkupStep]:
    """Build workup steps from a DiagnosticWorkup, **excluding** tests
    the patient has already completed (per profile.prior_tests_completed)."""

    steps: list[WorkupStep] = []
    counter = 0
    prior = {t.upper() for t in (prior_tests_completed or [])}

    def next_step() -> int:
        nonlocal counter
        counter += 1
        return counter

    # Labs / imaging / histology — skip those already completed
    for test_id in workup.get("required_tests") or []:
        if test_id.upper() in prior:
            continue
        info = entities.get(test_id, {})
        test_data = info.get("data") or {}
        category_raw = (test_data.get("category") or "").lower()
        if category_raw in {"lab", "imaging", "histology"}:
            category = category_raw
        elif category_raw == "clinical_assessment":
            category = "consult"
        else:
            category = "other"
        names = test_data.get("names") or {}
        descr = names.get("preferred") or test_id
        steps.append(WorkupStep(
            step=next_step(),
            category=category,
            test_id=test_id,
            description=descr,
            rationale=test_data.get("purpose"),
        ))

    # Then biopsy + IHC as a single histology step
    biopsy_raw = workup.get("biopsy_approach")
    ihc_raw = workup.get("required_ihc_panel")
    if biopsy_raw or ihc_raw:
        biopsy = (
            BiopsyApproach(**biopsy_raw)
            if isinstance(biopsy_raw, dict)
            else None
        )
        ihc = IHCPanel(**ihc_raw) if isinstance(ihc_raw, dict) else None
        steps.append(WorkupStep(
            step=next_step(),
            category="histology",
            test_id=None,
            description="Tissue biopsy + IHC panel + ancillary molecular",
            rationale=(biopsy.rationale if biopsy else None),
            biopsy_approach=biopsy,
            ihc_panel=ihc,
        ))

    return steps


# ── Public entry point ────────────────────────────────────────────────────


def generate_diagnostic_brief(
    patient: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
    plan_version: int = 1,
    supersedes: Optional[str] = None,
    revision_trigger: Optional[str] = None,
) -> DiagnosticPlanResult:
    """Build a DiagnosticPlan for a patient WITHOUT confirmed histology.

    Hard rule (CHARTER §15.2 C7): rejects profiles that already have
    `disease.id` or `disease.icd_o_3_morphology` — caller must use
    generate_plan() for those.
    """

    if is_treatment_profile(patient):
        raise ValueError(
            "Patient profile has confirmed diagnosis (disease.id / "
            "icd_o_3_morphology). Use generate_plan() for treatment mode. "
            "DiagnosticPlan is for pre-histology workup only."
        )

    suspicion = _build_suspicion_snapshot(patient)
    result = DiagnosticPlanResult(
        patient_id=patient.get("patient_id"),
        suspicion=suspicion,
    )

    if suspicion is None:
        result.warnings.append(
            "patient.disease.suspicion absent — cannot build a diagnostic brief; "
            "supply at least lineage_hint or tissue_locations."
        )
        return result

    load = load_content(Path(kb_root))
    entities = load.entities_by_id
    for path, msg in load.schema_errors:
        result.warnings.append(f"schema error in {path.name}: {msg[:120]}")
    for path, msg in load.ref_errors:
        result.warnings.append(f"ref error in {path.name}: {msg}")

    workup = _match_workup(suspicion, entities)
    if workup is None:
        result.warnings.append(
            "No DiagnosticWorkup matched the suspicion. Add a workup or "
            "broaden applicable_to.lineage_hints / tissue_locations."
        )
        return result

    result.matched_workup_id = workup.get("id")
    prior_tests = patient.get("prior_tests_completed") or []
    workup_steps = _materialise_workup_steps(workup, entities, prior_tests)

    plan_id = f"DPLAN-{(result.patient_id or 'ANONYMOUS').upper()}-V{plan_version}"
    result.diagnostic_plan = DiagnosticPlan(
        id=plan_id,
        patient_id=result.patient_id or "ANONYMOUS",
        version=plan_version,
        generated_at=datetime.now(timezone.utc).isoformat(),
        supersedes=supersedes,
        revision_trigger=revision_trigger,
        patient_snapshot=patient,
        suspicion_snapshot=suspicion,
        matched_workup_id=workup.get("id"),
        workup_steps=workup_steps,
        mandatory_questions=list(workup.get("mandatory_questions_to_resolve") or []),
        expected_timeline_days=workup.get("expected_timeline_days"),
        population_scope=(
            f"Adults with suspicion of {suspicion.lineage_hint or 'oncologic disease'} "
            f"({', '.join(suspicion.tissue_locations) or 'unspecified site'}) "
            f"prior to histologic confirmation."
        ),
        trace=[],
        warnings=result.warnings,
    )

    return result


__all__ = [
    "DiagnosticPlanResult",
    "_DIAGNOSTIC_BANNER",
    "generate_diagnostic_brief",
    "is_diagnostic_profile",
    "is_treatment_profile",
]
