"""Tests for the MDT Orchestrator (specs/MDT_ORCHESTRATOR_SPEC.md).

Verifies the four contractual properties:

1. Indolent HCV-MZL → hematologist required, infectious/hepatology recommended.
2. Bulky HCV-MZL → radiologist escalated, pathologist still in scope.
3. Missing HBV/staging data → blocking OpenQuestion(s) created.
4. orchestrate_mdt() does NOT mutate default_indication_id (no clinical
   override). This is the structural guarantee that the orchestrator
   never replaces the rule-engine recommendation.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from knowledge_base.engine import generate_plan, orchestrate_mdt

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def _role_ids(roles) -> set[str]:
    return {r.role_id for r in roles}


def test_indolent_hcv_mzl_requires_hematologist_recommends_infectious():
    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)

    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    assert mdt.disease_id == "DIS-HCV-MZL"
    assert mdt.plan_id and mdt.plan_id.startswith("PLAN-PZ-001-INDOLENT")

    required = _role_ids(mdt.required_roles)
    recommended = _role_ids(mdt.recommended_roles)

    assert "hematologist" in required, (
        "lymphoma diagnosis must trigger hematologist as required"
    )
    assert "infectious_disease_hepatology" in recommended, (
        "HCV-positive patient must trigger infectious-disease/hepatology"
    )
    # Pathologist always in scope for lymphoma diagnosis confirmation
    assert "pathologist" in recommended


def test_bulky_hcv_mzl_escalates_radiologist_and_keeps_pathologist():
    patient = _patient("patient_zero_bulky.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)

    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    required = _role_ids(mdt.required_roles)
    recommended = _role_ids(mdt.recommended_roles)

    # Bulky → radiologist becomes required (mass >= 7 cm)
    assert "radiologist" in required, (
        "bulky disease must escalate radiologist to required"
    )
    # Pathology review for transformation risk still in scope
    assert "pathologist" in recommended
    # Aggressive regimen → clinical pharmacist recommended
    assert "clinical_pharmacist" in recommended
    # Hematologist is always required for lymphoma
    assert "hematologist" in required


def test_missing_hbv_serology_creates_blocking_open_question():
    """Indolent patient profile in examples/ does not include HBV serology;
    this must surface as a blocking question owned by infectious disease."""

    patient = _patient("patient_zero_indolent.json")
    # Belt-and-suspenders: confirm fixture really lacks HBV fields
    findings = {
        **(patient.get("findings") or {}),
        **(patient.get("biomarkers") or {}),
        **(patient.get("demographics") or {}),
    }
    assert "hbsag" not in findings
    assert "anti_hbc_total" not in findings

    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    blocking_ids = {q.id for q in mdt.open_questions if q.blocking}
    assert "OQ-HBV-SEROLOGY" in blocking_ids, (
        "missing HBV serology must produce a blocking OpenQuestion"
    )

    hbv_q = next(q for q in mdt.open_questions if q.id == "OQ-HBV-SEROLOGY")
    assert hbv_q.owner_role == "infectious_disease_hepatology"
    assert hbv_q.blocking is True


def test_orchestration_does_not_change_default_indication():
    """Hard non-interference guarantee: orchestrate_mdt is read-only with
    respect to clinical recommendations. default_indication_id must be
    identical before and after."""

    patient = _patient("patient_zero_bulky.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)

    before = plan_result.default_indication_id
    before_alt = plan_result.alternative_indication_id
    before_track_ids = [t.indication_id for t in plan_result.plan.tracks]

    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    assert plan_result.default_indication_id == before
    assert plan_result.alternative_indication_id == before_alt
    assert [t.indication_id for t in plan_result.plan.tracks] == before_track_ids
    # And the MDT result must point at the same plan
    assert mdt.plan_id == plan_result.plan.id


def test_provenance_records_initial_engine_events():
    """Smoke test: the bootstrap provenance has at least one engine
    'confirmed' event for the plan and one 'requested_data' event per
    role. Provenance is the audit hook MDT spec §6 requires."""

    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    assert mdt.provenance is not None
    events = mdt.provenance.events
    assert any(e.event_type == "confirmed" and e.target_type == "plan_section" for e in events)

    role_event_targets = {
        e.target_id for e in events if e.event_type == "requested_data"
    }
    total_roles = (
        len(mdt.required_roles) + len(mdt.recommended_roles) + len(mdt.optional_roles)
    )
    assert len(role_event_targets) == total_roles
