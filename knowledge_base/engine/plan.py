"""Top-level plan generation.

    patient profile  →  Disease match  →  applicable Algorithm
                                    →   Algorithm walked with RedFlags
                                    →   Plan with multiple tracks (≥2)
                                    →   one rendered document per CHARTER §2

Per CHARTER §2 the output always presents at least two alternative tracks
in **one document**. The data-model guarantee for this comes from
`Algorithm.output_indications` (≥2 candidates) plus `default_indication`
+ `alternative_indication` markers.

FDA non-device CDS positioning (CHARTER §15) requires every Plan to surface
the four Criterion-4 elements (intended use, HCP user, patient population,
algorithm summary, data limitations). Engine populates these from Algorithm
and Indication metadata.

Patient profile shape (dict; MVP — we will move to FHIR/mCODE later):

    {
        "patient_id": "PZ-001",                      # required for Plan persistence
        "disease": {"icd_o_3_morphology": "9699/3"}, # or {"id": "DIS-HCV-MZL"}
        "line_of_therapy": 1,                        # default 1
        "biomarkers": {"BIO-HCV-RNA": "positive"},
        "demographics": {"age": 58, "ecog": 1, ...},
        "findings": {"dominant_nodal_mass_cm": 4.0, ...},
    }
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from knowledge_base.schemas import (
    AccessMatrix,
    AccessMatrixRow,
    ExperimentalOption,
    FDAComplianceMetadata,
    Plan,
    PlanTrack,
)
from knowledge_base.validation.loader import load_content
from .access_matrix import build_access_matrix
from .algorithm_eval import walk_algorithm
from .experimental_options import SearchFn, enumerate_experimental_options


# Track labels — ordered, default labels for the well-known plan_track values.
# Extend as we add new track types (palliative, trial-only, etc.)
_TRACK_LABELS_UA = {
    "standard": "Стандартний план",
    "aggressive": "Агресивний план",
    "surveillance": "Активне спостереження (watch-and-wait)",
    "palliative": "Паліативний план",
    "trial": "План у рамках клінічного дослідження",
}
_TRACK_LABELS_EN = {
    "standard": "Standard plan",
    "aggressive": "Aggressive plan",
    "surveillance": "Active surveillance (watch-and-wait)",
    "palliative": "Palliative plan",
    "trial": "Clinical-trial-only plan",
}


@dataclass
class PlanResult:
    """In-memory engine output. Carries both the new Plan structure and
    backward-compat fields for existing tests.
    """

    # Core
    patient_id: Optional[str]
    disease_id: Optional[str]
    algorithm_id: Optional[str]

    # New primary structure: full Plan with tracks + FDA metadata
    plan: Optional[Plan] = None

    # Back-compat shortcuts (derived from plan.tracks)
    default_indication_id: Optional[str] = None
    alternative_indication_id: Optional[str] = None
    default_indication: Optional[dict] = None
    alternative_indication: Optional[dict] = None

    # Engine internals
    trace: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    # Render-time-only metadata: open clinical trials matching this
    # disease + biomarker + line scenario. NEVER read by the engine as
    # a selection signal (CHARTER §8.3, plan §3.2 invariant). When no
    # search function is wired, this stays None — render shows the
    # "ctgov sync needed" placeholder per plan §3.3.
    experimental_options: Optional[ExperimentalOption] = None

    # Runtime KB resolutions for the render layer — NOT persisted with Plan.
    # Holds: 'disease' (dict), 'tests' (dict[id, dict]), 'red_flags' (dict[id, dict]),
    # 'algorithm' (dict). Populated by generate_plan; render gracefully degrades
    # if absent. Persistence (save_result) ignores this field entirely — the
    # rendered Plan dict is the source of truth on disk.
    kb_resolved: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "disease_id": self.disease_id,
            "algorithm_id": self.algorithm_id,
            "default_indication_id": self.default_indication_id,
            "alternative_indication_id": self.alternative_indication_id,
            "default_indication": self.default_indication,
            "alternative_indication": self.alternative_indication,
            "plan": self.plan.model_dump() if self.plan else None,
            "trace": self.trace,
            "warnings": self.warnings,
            "experimental_options": (
                self.experimental_options.model_dump()
                if self.experimental_options is not None
                else None
            ),
        }


# ── KB lookup helpers ─────────────────────────────────────────────────────────


def _find_disease_id(patient: dict, entities_by_id: dict) -> Optional[str]:
    dinfo = patient.get("disease") or {}
    if "id" in dinfo:
        return dinfo["id"]
    icd = dinfo.get("icd_o_3_morphology")
    if icd:
        for eid, info in entities_by_id.items():
            if info["type"] != "diseases":
                continue
            codes = info["data"].get("codes") or {}
            if codes.get("icd_o_3_morphology") == icd:
                return eid
    return None


def _find_algorithm(disease_id: str, line: int, entities_by_id: dict) -> Optional[dict]:
    for eid, info in entities_by_id.items():
        if info["type"] != "algorithms":
            continue
        d = info["data"]
        if d.get("applicable_to_disease") == disease_id and d.get("applicable_to_line_of_therapy") == line:
            return d
    return None


def _collect_redflags(entities_by_id: dict) -> dict[str, dict]:
    return {eid: info["data"] for eid, info in entities_by_id.items() if info["type"] == "redflags"}


def _resolve(entities: dict, entity_id: Optional[str]) -> Optional[dict]:
    if entity_id and entity_id in entities:
        return entities[entity_id]["data"]
    return None


# ── Track materialization ─────────────────────────────────────────────────────


def _materialize_track(
    track_id: str,
    indication_id: str,
    is_default: bool,
    selection_reason: str,
    entities: dict,
) -> PlanTrack:
    indication = _resolve(entities, indication_id)
    regimen = None
    monitoring = None
    supportive: list[dict] = []
    contras: list[dict] = []

    if indication:
        regimen = _resolve(entities, indication.get("recommended_regimen"))
        if regimen:
            monitoring = _resolve(entities, regimen.get("monitoring_schedule_id"))
            for sup_id in regimen.get("mandatory_supportive_care") or []:
                d = _resolve(entities, sup_id)
                if d:
                    supportive.append(d)
        for ci_id in indication.get("hard_contraindications") or []:
            d = _resolve(entities, ci_id)
            if d:
                contras.append(d)

    return PlanTrack(
        track_id=track_id,
        label=_TRACK_LABELS_UA.get(track_id, track_id),
        label_en=_TRACK_LABELS_EN.get(track_id, track_id),
        indication_id=indication_id,
        is_default=is_default,
        selection_reason=selection_reason,
        indication_data=indication,
        regimen_data=regimen,
        monitoring_data=monitoring,
        supportive_care_data=supportive,
        contraindications_data=contras,
    )


# ── FDA compliance metadata ───────────────────────────────────────────────────


def _build_fda_compliance(
    algorithm: dict,
    tracks: list[PlanTrack],
    entities: dict,
    warnings: list[str],
) -> FDAComplianceMetadata:
    """Populate the four Criterion-4 fields that every rendered Plan must carry.
    See specs/CHARTER.md §15 and the FDA Clinical Decision Support Guidance
    (specs/Guidance-Clinical-Decision-Software_5.pdf, source SRC-FDA-CDS-2026)."""

    # Aggregate sources cited across all tracks
    source_ids: set[str] = set()
    for t in tracks:
        ind = t.indication_data or {}
        for s in ind.get("sources") or []:
            if isinstance(s, dict) and s.get("source_id"):
                source_ids.add(s["source_id"])
            elif isinstance(s, str):
                source_ids.add(s)

    sources_summary: list[str] = []
    for sid in sorted(source_ids):
        srec = _resolve(entities, sid)
        if srec:
            sources_summary.append(f"{sid}: {srec.get('title', '')} ({srec.get('version', '')})")
        else:
            sources_summary.append(f"{sid}: (not in KB)")

    # Time-critical: any track marked time_critical disqualifies the whole plan
    time_critical = any((t.indication_data or {}).get("time_critical") for t in tracks)

    limitations: list[str] = list(warnings)
    if time_critical:
        limitations.append(
            "WARNING: This plan includes time-critical Indications — falls "
            "OUTSIDE FDA non-device CDS carve-out per §520(o)(1)(E) Criterion 4."
        )

    return FDAComplianceMetadata(
        intended_use=(
            "Outpatient oncology treatment planning to support tumor-board "
            "discussion. Not a medical device; not for autonomous clinical "
            "decision-making."
        ),
        hcp_user_specification=(
            "Licensed oncologist or hematologist participating in a "
            "multidisciplinary tumor board. Intended user must be qualified "
            "to independently review the basis of every recommendation."
        ),
        patient_population_match=(
            f"Adults with confirmed {(tracks[0].indication_data or {}).get('applicable_to', {}).get('disease_id', 'disease')} "
            f"diagnosis at line of therapy "
            f"{(tracks[0].indication_data or {}).get('applicable_to', {}).get('line_of_therapy', '?')}."
        ),
        algorithm_summary=algorithm.get("purpose") or (
            "Rule-based decision tree evaluating patient findings against "
            "RedFlag entities, selecting an Indication from a fixed candidate "
            "set authored by clinical reviewers."
        ),
        data_sources_summary=sources_summary,
        data_limitations=limitations,
        automation_bias_warning=(
            "Both treatment options below are presented for review. The "
            "engine's selection of a 'recommended' default does not constitute "
            "a clinical decision. Final treatment selection requires HCP "
            "judgment incorporating information not available to the system."
        ),
        time_critical=time_critical,
    )


# ── Top-level entry point ─────────────────────────────────────────────────────


def generate_plan(
    patient: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
    plan_version: int = 1,
    supersedes: Optional[str] = None,
    revision_trigger: Optional[str] = None,
    experimental_search_fn: Optional[SearchFn] = None,
) -> PlanResult:
    """Run the rule engine on a patient profile and return a PlanResult
    containing a fully-materialized Plan with multiple tracks.

    `experimental_search_fn`: optional ctgov search callable. When
    provided, `generate_plan` calls `enumerate_experimental_options`
    after track materialization and attaches the result as
    `result.experimental_options`. This is render-time metadata only —
    never a selection signal (CHARTER §8.3, plan §3.2 invariant).
    """

    result = PlanResult(
        patient_id=patient.get("patient_id"),
        disease_id=None,
        algorithm_id=None,
    )

    load = load_content(Path(kb_root))
    if not load.ok:
        for path, msg in load.schema_errors:
            result.warnings.append(f"schema error in {path.name}: {msg[:120]}")
        for path, msg in load.ref_errors:
            result.warnings.append(f"ref error in {path.name}: {msg}")

    entities = load.entities_by_id
    disease_id = _find_disease_id(patient, entities)
    if disease_id is None:
        result.warnings.append("Could not resolve disease from patient.disease")
        return result
    result.disease_id = disease_id

    line = int(patient.get("line_of_therapy", 1))
    algo = _find_algorithm(disease_id, line, entities)
    if algo is None:
        result.warnings.append(
            f"No Algorithm found for disease={disease_id}, line_of_therapy={line}"
        )
        return result
    result.algorithm_id = algo["id"]

    # Flatten findings + biomarkers + demographics for clause evaluation
    findings = dict(patient.get("findings") or {})
    for k, v in (patient.get("biomarkers") or {}).items():
        findings.setdefault(k, v)
    for k, v in (patient.get("demographics") or {}).items():
        findings.setdefault(k, v)

    redflag_lookup = _collect_redflags(entities)
    selected, trace = walk_algorithm(algo, findings, redflag_lookup)
    result.trace = trace

    # Build the full track list — every Indication in algorithm.output_indications
    # becomes a track, ordered with the engine-selected default first.
    candidates = list(algo.get("output_indications") or [])
    default_id = selected or algo.get("default_indication")
    if default_id and default_id in candidates:
        candidates.remove(default_id)
        candidates.insert(0, default_id)

    tracks: list[PlanTrack] = []
    for ind_id in candidates:
        ind = _resolve(entities, ind_id)
        track_label = (ind or {}).get("plan_track") or ind_id
        is_default = ind_id == default_id
        reason = (
            f"Engine default per algorithm {algo['id']}: {trace[-1] if trace else 'no trace'}"
            if is_default
            else "Alternative track presented for HCP consideration"
        )
        tracks.append(_materialize_track(track_label, ind_id, is_default, reason, entities))

    fda = _build_fda_compliance(algo, tracks, entities, result.warnings)

    # KB state snapshot (per CHARTER §10.2 — immutable audit)
    kb_state = {
        "loaded_entities": len(entities),
        "indications_used": [t.indication_id for t in tracks],
        "algorithm_version": algo.get("last_reviewed"),
    }

    plan_id = f"PLAN-{(result.patient_id or 'ANONYMOUS').upper()}-V{plan_version}"
    result.plan = Plan(
        id=plan_id,
        patient_id=result.patient_id or "ANONYMOUS",
        version=plan_version,
        generated_at=datetime.now(timezone.utc).isoformat(),
        supersedes=supersedes,
        superseded_by=None,
        revision_trigger=revision_trigger,
        patient_snapshot=patient,
        algorithm_id=algo["id"],
        knowledge_base_state=kb_state,
        tracks=tracks,
        fda_compliance=fda,
        trace=trace,
        warnings=result.warnings,
        annotations=[],
    )

    # Back-compat fields for existing tests
    if tracks:
        result.default_indication_id = tracks[0].indication_id
        result.default_indication = tracks[0].indication_data
        if len(tracks) >= 2:
            result.alternative_indication_id = tracks[1].indication_id
            result.alternative_indication = tracks[1].indication_data

    # Resolve KB references that the render layer needs but that aren't
    # carried on the Plan structure: disease (for archetype + etiological_factors),
    # tests (for priority_class on pre-treatment investigations table),
    # red_flags (for PRO/CONTRA categorization with definitions).
    test_ids: set[str] = set()
    redflag_ids: set[str] = set()
    for t in tracks:
        ind = t.indication_data or {}
        test_ids.update(ind.get("required_tests") or [])
        test_ids.update(ind.get("desired_tests") or [])
        redflag_ids.update(ind.get("red_flags_triggering_alternative") or [])
    # Algorithm-referenced red flags too (decision tree)
    for step in algo.get("decision_tree") or []:
        ev = step.get("evaluate") or {}
        for clause in (ev.get("any_of") or []) + (ev.get("all_of") or []):
            rf = clause.get("red_flag") if isinstance(clause, dict) else None
            if rf:
                redflag_ids.add(rf)

    result.kb_resolved = {
        "disease": _resolve(entities, disease_id),
        "algorithm": algo,
        "tests": {tid: _resolve(entities, tid) for tid in test_ids if _resolve(entities, tid)},
        "red_flags": {rid: _resolve(entities, rid) for rid in redflag_ids if _resolve(entities, rid)},
    }

    # Experimental track (Phase C of UA-ingestion plan). Append-only,
    # never feeds back into selection — engine output above is final.
    if experimental_search_fn is not None:
        disease_data = result.kb_resolved.get("disease") or {}
        disease_term = (
            ((disease_data.get("names") or {}).get("english"))
            or ((disease_data.get("names") or {}).get("preferred"))
            or disease_id
        )
        biomarker_term = _first_truthy_biomarker(patient.get("biomarkers") or {})
        try:
            result.experimental_options = enumerate_experimental_options(
                disease_id=disease_id,
                disease_term=disease_term,
                biomarker_profile=biomarker_term,
                line_of_therapy=line,
                search_fn=experimental_search_fn,
            )
        except Exception as exc:
            result.warnings.append(f"experimental options skipped: {exc}")

    # Access Matrix (Phase D of UA-ingestion plan §3.1 + §4). Render-time
    # aggregation of UA-availability metadata across tracks + experimental
    # trials. NEVER read back by engine selection — the invariant test
    # asserts plan signature is unchanged when all drugs are monkeypatched
    # to registered=False.
    try:
        result.plan.access_matrix = build_access_matrix(
            tracks,
            entities,
            experimental_options=result.experimental_options,
        )
    except Exception as exc:
        result.warnings.append(f"access matrix skipped: {exc}")

    return result


def _first_truthy_biomarker(biomarkers: dict) -> Optional[str]:
    """Pick a representative biomarker term for the ctgov query.

    Patient biomarker dicts vary in shape — values may be bool, str,
    or nested dict. We prefer keys whose value is True or a positive
    string ("positive", "mutated", "amplified"). Returns the human
    label form (e.g. `BIO-EGFR-MUT` → `EGFR mutation`-ish), or None
    when no positive biomarker is present.

    Engine doesn't read this — it only feeds the trial query.
    """

    if not biomarkers:
        return None
    for key, val in biomarkers.items():
        if val is True:
            return _humanize_biomarker_key(key)
        if isinstance(val, str) and val.lower() in {
            "positive", "pos", "mutated", "mut", "amplified", "high"
        }:
            return _humanize_biomarker_key(key)
    return None


def _humanize_biomarker_key(key: str) -> str:
    """`BIO-EGFR-MUTATION` → `EGFR mutation`; falls back to the raw key."""
    raw = key
    if raw.upper().startswith("BIO-"):
        raw = raw[4:]
    return raw.replace("_", " ").replace("-", " ").lower()


__all__ = ["PlanResult", "generate_plan"]
