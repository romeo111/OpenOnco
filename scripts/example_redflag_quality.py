"""Helpers for keeping public examples RedFlag-complete.

Public gallery examples should be synthetic but complete enough that the MDT
data-quality section does not report `unevaluated_red_flags`. When a RedFlag
trigger references an absent finding, we can often add an explicit neutral
finding value ("known absent" / "not detected") without changing the plan.

This module does that conservatively:

* it only fills fields referenced by disease-relevant RedFlags;
* it preserves the fired/not-fired result of every applicable RedFlag;
* it verifies the Plan default and alternative indication do not change.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from knowledge_base.engine import generate_plan, is_diagnostic_profile, orchestrate_mdt
from knowledge_base.engine.mdt_orchestrator import (
    _flatten_findings,
    _trigger_referenced_fields,
)
from knowledge_base.engine.redflag_eval import (
    _resolve_finding,
    evaluate_redflag_trigger,
)
from knowledge_base.validation.loader import load_content


NEUTRAL_CANDIDATES: tuple[Any, ...] = (
    "absent",
    "negative",
    "not_detected",
    "wildtype",
    "none",
    False,
    0,
    -1,
    1,
    9999,
    True,
    "true",
    "false",
)

B_CELL_LYMPHOMA_DISEASES = {
    "DIS-HCV-MZL",
    "DIS-DLBCL-NOS",
    "DIS-FL",
    "DIS-CLL",
    "DIS-MCL",
    "DIS-SPLENIC-MZL",
    "DIS-NODAL-MZL",
    "DIS-BURKITT",
    "DIS-HCL",
    "DIS-WM",
    "DIS-HGBL-DH",
    "DIS-NLPBL",
    "DIS-PMBCL",
    "DIS-PTLD",
}

MDT_FIELD_DEFAULTS: dict[str, Any] = {
    "hbsag": "negative",
    "anti_hbc_total": "negative",
    "lugano_stage": "II",
    "ldh_ratio_to_uln": 1.0,
    "fib4_index": 1.2,
    "pet_ct_date": "2026-04-15",
}


def _applicable_redflags(kb_root: Path, disease_id: str | None) -> list[tuple[str, dict]]:
    entities = load_content(kb_root).entities_by_id
    redflags: list[tuple[str, dict]] = []
    for entity_id, info in entities.items():
        if info.get("type") != "redflags":
            continue
        rf = info.get("data") or {}
        relevant = rf.get("relevant_diseases") or []
        if relevant and disease_id and disease_id not in relevant:
            continue
        redflags.append((entity_id, rf))
    return redflags


def _redflag_outcomes(
    redflags: list[tuple[str, dict]],
    findings: dict[str, Any],
) -> dict[str, bool]:
    return {
        redflag_id: evaluate_redflag_trigger(rf.get("trigger") or {}, findings)
        for redflag_id, rf in redflags
    }


def _missing_redflag_fields(
    redflags: list[tuple[str, dict]],
    findings: dict[str, Any],
) -> list[str]:
    missing: set[str] = set()
    for _redflag_id, rf in redflags:
        for field in _trigger_referenced_fields(rf.get("trigger") or {}):
            if _resolve_finding(findings, field) is None:
                missing.add(field)
    return sorted(missing)


def enrich_profile_for_redflag_completeness(
    profile: dict,
    *,
    kb_root: Path,
) -> tuple[dict, dict[str, Any]]:
    """Return `(profile, added_findings)` with neutral RedFlag fields filled.

    Raises `RuntimeError` if a neutral value cannot be found without changing
    RedFlag outcomes or the selected treatment route.
    """
    enriched = deepcopy(profile)
    if is_diagnostic_profile(enriched):
        return enriched, {}

    before_plan = generate_plan(enriched, kb_root=kb_root)
    if before_plan.plan is None:
        return enriched, {}

    disease_id = before_plan.disease_id
    redflags = _applicable_redflags(kb_root, disease_id)
    findings = _flatten_findings(enriched)
    before_outcomes = _redflag_outcomes(redflags, findings)

    added: dict[str, Any] = {}
    for field in _missing_redflag_fields(redflags, findings):
        if _resolve_finding({**findings, **added}, field) is not None:
            continue

        selected = None
        for candidate in NEUTRAL_CANDIDATES:
            trial_findings = {**findings, **added, field: candidate}
            try:
                after_outcomes = _redflag_outcomes(redflags, trial_findings)
            except Exception:
                continue
            if after_outcomes == before_outcomes:
                selected = candidate
                break

        if selected is None:
            patient_id = enriched.get("patient_id") or "<unknown>"
            raise RuntimeError(
                f"{patient_id}: no neutral RedFlag value found for {field!r}"
            )
        added[field] = selected

    if not added:
        return enriched, {}

    enriched.setdefault("findings", {}).update(added)
    after_plan = generate_plan(enriched, kb_root=kb_root)
    before_route = (
        before_plan.default_indication_id,
        before_plan.alternative_indication_id,
    )
    after_route = (
        after_plan.default_indication_id,
        after_plan.alternative_indication_id,
    )
    if after_route != before_route:
        patient_id = enriched.get("patient_id") or "<unknown>"
        raise RuntimeError(
            f"{patient_id}: neutral RedFlag enrichment changed plan route "
            f"from {before_route} to {after_route}"
        )

    return enriched, added


def _route(plan_result) -> tuple[str | None, str | None]:
    return (
        plan_result.default_indication_id,
        plan_result.alternative_indication_id,
    )


def _default_for_mdt_field(field: str, disease_id: str | None) -> Any:
    if field == "cd20_ihc_status":
        return "positive" if disease_id in B_CELL_LYMPHOMA_DISEASES else "not_applicable"
    return MDT_FIELD_DEFAULTS.get(field, "known")


def _biomarker_value_candidates(missing_entry: dict) -> list[Any]:
    constraint = missing_entry.get("value_constraint")
    if missing_entry.get("default_track"):
        candidates = [constraint, "positive", "known", "negative", "absent"]
    else:
        candidates = ["negative", "absent", "not_detected", constraint, "known", "positive"]

    out: list[Any] = []
    for value in candidates:
        if value in (None, ""):
            continue
        if value not in out:
            out.append(value)
    return out


def enrich_profile_for_gallery_quality(
    profile: dict,
    *,
    kb_root: Path,
) -> tuple[dict, dict[str, Any]]:
    """Fill public-gallery example data-quality gaps without changing route.

    Returns the enriched profile and a summary with `redflag_findings`,
    `mdt_findings`, and `biomarkers` entries.
    """
    enriched, redflag_added = enrich_profile_for_redflag_completeness(
        profile,
        kb_root=kb_root,
    )
    summary: dict[str, Any] = {
        "redflag_findings": redflag_added,
        "mdt_findings": {},
        "biomarkers": {},
    }

    if is_diagnostic_profile(enriched):
        return enriched, summary

    before_plan = generate_plan(enriched, kb_root=kb_root)
    if before_plan.plan is None:
        return enriched, summary
    expected_route = _route(before_plan)

    mdt = orchestrate_mdt(enriched, before_plan, kb_root=kb_root)
    data_quality = mdt.data_quality_summary
    mdt_fields = (
        list(data_quality.get("missing_critical_fields") or [])
        + list(data_quality.get("missing_recommended_fields") or [])
    )
    for field in mdt_fields:
        if _resolve_finding(_flatten_findings(enriched), field) is not None:
            continue
        value = _default_for_mdt_field(field, before_plan.disease_id)
        enriched.setdefault("findings", {})[field] = value
        summary["mdt_findings"][field] = value

    # Fill required biomarker coverage. Candidate values are selected by
    # preserving the plan route; non-default-track biomarkers prefer an
    # explicit negative/absent value so they are known without making an
    # alternative track accidentally become the routed default.
    for _iteration in range(3):
        current_plan = generate_plan(enriched, kb_root=kb_root)
        current_mdt = orchestrate_mdt(enriched, current_plan, kb_root=kb_root)
        missing = (
            current_mdt.data_quality_summary.get("biomarker_coverage", {})
            .get("missing")
            or []
        )
        if not missing:
            break

        changed = False
        for entry in missing:
            biomarker_id = entry["biomarker_id"]
            if _resolve_finding(_flatten_findings(enriched), biomarker_id) is not None:
                continue

            selected = None
            for candidate in _biomarker_value_candidates(entry):
                trial = deepcopy(enriched)
                trial.setdefault("biomarkers", {})[biomarker_id] = candidate
                if _route(generate_plan(trial, kb_root=kb_root)) == expected_route:
                    selected = candidate
                    break

            if selected is None:
                patient_id = enriched.get("patient_id") or "<unknown>"
                raise RuntimeError(
                    f"{patient_id}: no route-preserving value found for "
                    f"required biomarker {biomarker_id}"
                )
            enriched.setdefault("biomarkers", {})[biomarker_id] = selected
            summary["biomarkers"][biomarker_id] = selected
            changed = True

        if not changed:
            break

    after_plan = generate_plan(enriched, kb_root=kb_root)
    if _route(after_plan) != expected_route:
        patient_id = enriched.get("patient_id") or "<unknown>"
        raise RuntimeError(
            f"{patient_id}: gallery-quality enrichment changed plan route "
            f"from {expected_route} to {_route(after_plan)}"
        )

    final_mdt = orchestrate_mdt(enriched, after_plan, kb_root=kb_root)
    final_dq = final_mdt.data_quality_summary
    if final_dq.get("status") != "complete_for_mdt_review":
        patient_id = enriched.get("patient_id") or "<unknown>"
        raise RuntimeError(
            f"{patient_id}: data quality still incomplete after enrichment: "
            f"{final_dq.get('status')}"
        )

    return enriched, summary
