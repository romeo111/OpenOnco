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
    """A patient whose profile lacks HBV serology must surface a blocking
    OpenQuestion owned by infectious disease.

    NOTE: built inline because patient_zero_indolent.json was updated
    in commit a774bbe to include hbsag/anti_hbc_total = negative — the
    older fixture-based version of this test relied on those fields
    being absent and would fail trivially against the current data."""

    patient = _patient("patient_zero_indolent.json")
    # Strip HBV fields so the OQ generator detects the absence and
    # raises the blocking question.
    findings = dict(patient.get("findings") or {})
    findings.pop("hbsag", None)
    findings.pop("anti_hbc_total", None)
    patient = {**patient, "findings": findings}

    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    blocking_ids = {q.id for q in mdt.open_questions if q.blocking}
    assert "OQ-HBV-SEROLOGY" in blocking_ids, (
        f"missing HBV serology must produce a blocking OpenQuestion; "
        f"got blocking IDs: {blocking_ids}"
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


def test_persisted_reviewer_events_are_rehydrated_into_graph(tmp_path, monkeypatch):
    """orchestrate_mdt() must call merge_events_into_graph so historical
    reviewer events (`confirmed`/`modified`/`approved` from past sessions)
    survive a fresh orchestration. Otherwise re-rendering a Plan in a new
    session would silently drop the audit trail."""

    from knowledge_base.engine import event_store
    from knowledge_base.engine.provenance import ProvenanceEvent

    # Point event_store at a temp dir so the test never touches real
    # patient_plans/.
    monkeypatch.setattr(event_store, "DEFAULT_ROOT", tmp_path)

    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)

    historical_event = ProvenanceEvent(
        event_id="evt-rehydration-test-001",
        actor_role="medical_oncologist",
        actor_id="dr-test",
        event_type="approved",
        target_type="plan_section",
        target_id=plan_result.plan.id,
        timestamp="2025-01-01T00:00:00Z",
        summary="Pre-existing approval persisted from a prior session.",
    )
    event_store.append_event(plan_result.patient_id, historical_event, root=tmp_path)

    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    assert any(
        e.event_id == "evt-rehydration-test-001" for e in mdt.provenance.events
    ), "merge_events_into_graph not wired into orchestrate_mdt"


# ── Drift fixes (post-audit) ──────────────────────────────────────────────


def test_flagged_risk_events_target_red_flag_ids():
    """flagged_risk events must reference RedFlag IDs (RF-*), not
    Indication IDs. Regression test for the bootstrap_provenance bug
    surfaced in self-audit."""

    patient = _patient("patient_zero_bulky.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    flagged = [e for e in mdt.provenance.events if e.event_type == "flagged_risk"]
    assert flagged, "bulky patient must produce at least one flagged_risk event"
    for e in flagged:
        assert e.target_type == "red_flag"
        assert e.target_id.startswith("RF-"), (
            f"flagged_risk target_id must be a RedFlag id, got {e.target_id!r}"
        )

    # Specifically: RF-BULKY-DISEASE fires for the bulky patient
    targets = {e.target_id for e in flagged}
    assert "RF-BULKY-DISEASE" in targets


def test_priority_escalation_via_red_flag():
    """Bulky patient: radiologist starts as `recommended` from R3 (imaging
    fields present), then escalates to `required` via §3-Esc because
    RF-BULKY-DISEASE fires with clinical_direction=intensify."""

    patient = _patient("patient_zero_bulky.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    required_ids = {r.role_id for r in mdt.required_roles}
    assert "radiologist" in required_ids

    radiologist = next(r for r in mdt.required_roles if r.role_id == "radiologist")
    assert "RF-BULKY-DISEASE" in (radiologist.reason or "")
    assert "intensify" in (radiologist.reason or "").lower()
    assert "RF-BULKY-DISEASE" in radiologist.linked_findings


def test_non_reimbursed_drug_creates_drug_availability_question():
    """Q6: any track with a regimen component flagged as not reimbursed
    by НСЗУ must produce OQ-DRUG-AVAILABILITY for social_worker_case_manager
    and add the role at `recommended`. Tested by injecting a synthetic
    non-reimbursed component into the default track's regimen_data."""

    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)

    default_track = next(t for t in plan_result.plan.tracks if t.is_default)
    base_regimen = dict(default_track.regimen_data or {})
    base_regimen["ukraine_availability"] = {
        "per_component": {
            "DRUG-TEST-NONREIMB": {"reimbursed_nszu": False},
        },
    }
    default_track.regimen_data = base_regimen

    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    qids = {q.id for q in mdt.open_questions}
    assert "OQ-DRUG-AVAILABILITY" in qids

    drug_q = next(q for q in mdt.open_questions if q.id == "OQ-DRUG-AVAILABILITY")
    assert drug_q.owner_role == "social_worker_case_manager"
    assert drug_q.blocking is False
    assert "DRUG-TEST-NONREIMB" in drug_q.linked_findings


def test_data_quality_lists_unevaluated_red_flags():
    """A patient profile that lacks the laboratory fields multiple RedFlag
    triggers depend on (HBV serology, Child-Pugh class, FIB-4) must surface
    those incompletely-evaluable RFs in `data_quality_summary.unevaluated_red_flags`.

    NOTE: patient_zero_indolent.json now includes hbsag/anti_hbc_total/etc
    (commit a774bbe), so we strip those fields inline here to exercise the
    contract. RF-HBV-COINFECTION was reclassified from `hold` to
    `investigate` (2026-04-25) and may or may not appear in the unevaluated
    list depending on how the orchestrator filters; we assert that AT LEAST
    one HBV/cirrhosis-related RF is flagged."""

    patient = _patient("patient_zero_indolent.json")
    findings = dict(patient.get("findings") or {})
    for k in ("hbsag", "anti_hbc_total", "child_pugh_class", "decompensated_cirrhosis", "fib4_index"):
        findings.pop(k, None)
    patient = {**patient, "findings": findings}

    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    unevaluated = mdt.data_quality_summary.get("unevaluated_red_flags") or []
    assert unevaluated, (
        "stripped patient lacks hbsag/anti_hbc_total/child_pugh_class — "
        "at least one RedFlag must be incompletely evaluable"
    )
    # Either the disease-specific HBV RF (kept for HCV-MZL annotation) or
    # the universal HBV RF or the decomp-cirrhosis RF must surface.
    expected_any = {
        "RF-HBV-COINFECTION",
        "RF-UNIVERSAL-HBV-REACTIVATION-RISK",
        "RF-DECOMP-CIRRHOSIS",
    }
    assert expected_any & set(unevaluated), (
        f"expected one of {expected_any} in unevaluated_red_flags; "
        f"got {unevaluated}"
    )


# ── Infographic-alignment fixes ───────────────────────────────────────────


def test_aggregation_summary_populated():
    """Per spec §2.3, every MDT brief carries an explicit aggregation_summary
    (the infographic step 2: 'AI-агрегація'). Smoke-check core counters."""

    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    agg = mdt.aggregation_summary
    assert agg, "aggregation_summary must be populated, not empty dict"
    assert agg["kb_entities_loaded"] >= 16
    assert agg["indications_evaluated"] == len(plan_result.plan.tracks)
    assert agg["red_flags_total_in_kb"] >= 1
    # BIO-HCV-RNA referenced by IND-HCV-MZL-1L-ANTIVIRAL biomarker_requirements_required
    assert "BIO-HCV-RNA" in agg["biomarkers_referenced"]
    assert "SRC-CTGOV-REGISTRY" in agg["live_api_clients_available"]
    assert "SRC-PUBMED" in agg["live_api_clients_available"]


def test_molecular_geneticist_triggers_on_genomic_biomarker():
    """R9: when an Indication.applicable_to.biomarker_requirements_required
    references a Biomarker with biomarker_type in _ACTIONABLE_GENOMIC_TYPES,
    molecular_geneticist gets recommended.

    Tested by injecting a synthetic gene-mutation biomarker requirement
    into the default track's indication_data, plus a transient Biomarker
    entity via a load_content monkey-patch — does not modify any KB on disk."""

    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    default = next(t for t in plan_result.plan.tracks if t.is_default)
    base_ind = dict(default.indication_data or {})
    applicable = dict(base_ind.get("applicable_to") or {})
    applicable["biomarker_requirements_required"] = list(
        applicable.get("biomarker_requirements_required") or []
    ) + [{"biomarker_id": "BIO-TEST-BRAF-V600E", "required": True}]
    base_ind["applicable_to"] = applicable
    default.indication_data = base_ind

    from knowledge_base.engine import mdt_orchestrator as _mod

    real_load = _mod.load_content

    def fake_load(root):
        result = real_load(root)
        result.entities_by_id["BIO-TEST-BRAF-V600E"] = {
            "type": "biomarkers",
            "data": {
                "id": "BIO-TEST-BRAF-V600E",
                "biomarker_type": "gene_mutation",
                "names": {"preferred": "BRAF V600E (test)"},
            },
            "path": None,
        }
        return result

    _mod.load_content = fake_load
    try:
        mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)
    finally:
        _mod.load_content = real_load

    role_ids = (
        {r.role_id for r in mdt.required_roles}
        | {r.role_id for r in mdt.recommended_roles}
        | {r.role_id for r in mdt.optional_roles}
    )
    assert "molecular_geneticist" in role_ids
    mg = next(
        r for r in mdt.recommended_roles + mdt.required_roles + mdt.optional_roles
        if r.role_id == "molecular_geneticist"
    )
    assert "BIO-TEST-BRAF-V600E" in mg.linked_findings


def test_role_catalog_covers_infographic_team_composition():
    """Sanity: every role on the project infographic
    (infograph/mdt_with_ai_layer_light_theme.html) must be representable
    in our orchestrator catalog. Not all need to fire on every plan;
    they just need to exist."""

    from knowledge_base.engine.mdt_orchestrator import _ROLE_CATALOG

    expected_roles = {
        "surgical_oncologist",
        "medical_oncologist",
        "hematologist",
        "radiation_oncologist",
        "pathologist",
        "radiologist",
        "molecular_geneticist",
        "psychologist",
        "palliative_care",
    }
    missing = expected_roles - set(_ROLE_CATALOG.keys())
    assert not missing, f"Catalog missing roles from project infographic: {missing}"


# ── Skill versioning (per user request: each skill carries version, last
# reviewed, sign-off status, so changes are easy to verify) ───────────────


def test_every_role_in_catalog_has_skill_registry_entry():
    """Every role advertised in _ROLE_CATALOG must have versioned metadata
    in _SKILL_REGISTRY — otherwise the rendered Plan can't show 'skill X
    v0.1.0, last reviewed YYYY-MM-DD' for that role."""
    from knowledge_base.engine.mdt_orchestrator import (
        _ROLE_CATALOG,
        _SKILL_REGISTRY,
    )
    missing = set(_ROLE_CATALOG.keys()) - set(_SKILL_REGISTRY.keys())
    assert not missing, f"Roles missing from _SKILL_REGISTRY: {missing}"


def test_skill_registry_has_required_metadata_fields():
    """Each skill record carries the contractual fields that the render
    layer surfaces inline (so a clinician can verify which version of
    which skill produced a given role activation)."""
    from knowledge_base.engine.mdt_orchestrator import _SKILL_REGISTRY
    import re
    semver = re.compile(r"^\d+\.\d+\.\d+$")
    iso_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for sid, s in _SKILL_REGISTRY.items():
        assert s.skill_id == sid, f"{sid}: skill_id mismatch"
        assert s.name, f"{sid}: missing display name"
        assert semver.match(s.version), f"{sid}: version not semver: {s.version}"
        assert iso_date.match(s.last_reviewed), (
            f"{sid}: last_reviewed not ISO date: {s.last_reviewed}"
        )
        # signoffs property derived from verified_by length
        assert s.signoffs == len(s.verified_by)
        # All currently STUBs (no clinician sign-offs yet); review_status
        # flips to "reviewed" once 2+ verified_by entries exist
        assert s.review_status in {"reviewed", "stub"}


def test_activated_role_carries_skill_metadata():
    """When a role activates, the MDTRequiredRole instance must carry the
    skill metadata so the render layer can show version inline."""
    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)

    all_roles = (
        list(mdt.required_roles) + list(mdt.recommended_roles) + list(mdt.optional_roles)
    )
    assert all_roles, "test setup: no roles activated for indolent HCV-MZL"
    for r in all_roles:
        assert r.skill is not None, f"role {r.role_id} missing skill metadata"
        assert r.skill.skill_id == r.role_id
        assert r.skill.version


def test_activated_skills_dedupes_across_buckets():
    """A role appearing in multiple buckets (e.g., promoted from
    recommended → required across rules) should appear once in
    activated_skills."""
    patient = _patient("patient_zero_bulky.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)
    activated = mdt.activated_skills
    skill_ids = [s.skill_id for s in activated]
    assert len(skill_ids) == len(set(skill_ids)), (
        f"activated_skills has duplicates: {skill_ids}"
    )


def test_to_dict_surfaces_skill_catalog_for_render():
    """to_dict() must surface the full registry as 'skill_catalog' so the
    render layer can list all skills (activated + dormant) with versions."""
    patient = _patient("patient_zero_indolent.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)
    d = mdt.to_dict()
    assert "activated_skills" in d
    assert "skill_catalog" in d
    catalog_ids = {s["skill_id"] for s in d["skill_catalog"]}
    activated_ids = {s["skill_id"] for s in d["activated_skills"]}
    # Every activated skill must be in the catalog
    assert activated_ids <= catalog_ids
    # Catalog matches registry size
    from knowledge_base.engine.mdt_orchestrator import _SKILL_REGISTRY
    assert catalog_ids == set(_SKILL_REGISTRY.keys())
