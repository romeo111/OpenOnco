"""Tests for the expanded hematology workup catalog + prior_tests_completed
+ active_surveillance plan_track support.

Verifies:
1. All 8 workups load valid (existing + 6 new)
2. prior_tests_completed excludes those tests from generated workup_steps
3. WORKUP-SUSPECTED-LYMPHOMA expanded — has all critical hematology tests
4. Disease-specific workups match correct lineage_hints
5. active_surveillance plan_track has UA + EN labels available
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_diagnostic_brief
from knowledge_base.engine.diagnostic import _match_workup
from knowledge_base.engine.plan import _TRACK_LABELS_EN, _TRACK_LABELS_UA
from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


# ── Catalog completeness ──────────────────────────────────────────────────


def test_all_workups_load_and_validate():
    result = load_content(KB_ROOT)
    assert result.ok, f"validation errors: {result.schema_errors + result.ref_errors}"

    workup_ids = {
        eid for eid, info in result.entities_by_id.items()
        if info["type"] == "workups"
    }
    expected = {
        "WORKUP-SUSPECTED-LYMPHOMA",
        "WORKUP-SUSPECTED-SOLID-TUMOR",
        "WORKUP-SUSPECTED-ACUTE-LEUKEMIA",
        "WORKUP-SUSPECTED-MULTIPLE-MYELOMA",
        "WORKUP-SUSPECTED-MPN-MDS",
        "WORKUP-CYTOPENIA-EVALUATION",
        "WORKUP-LYMPHADENOPATHY-NONSPECIFIC",
        "WORKUP-MONOCLONAL-GAMMOPATHY-INCIDENTAL",
    }
    missing = expected - workup_ids
    assert not missing, f"missing workups: {missing}"


def test_lymphoma_workup_expanded_to_basic_hematology_battery():
    """WORKUP-SUSPECTED-LYMPHOMA has the comprehensive basic-workup
    test set per WORKUP_METHODOLOGY_SPEC + clinical reality."""
    result = load_content(KB_ROOT)
    wkp = result.entities_by_id["WORKUP-SUSPECTED-LYMPHOMA"]["data"]
    required = set(wkp.get("required_tests") or [])

    # Must include the new basic-hematology essentials
    must_have = {
        "TEST-CBC", "TEST-PERIPHERAL-SMEAR", "TEST-CMP", "TEST-LFT", "TEST-LDH",
        "TEST-COAG-PANEL", "TEST-HBV-SEROLOGY", "TEST-HCV-ANTIBODY",
        "TEST-HIV-SEROLOGY", "TEST-IMMUNOGLOBULINS", "TEST-B2-MICROGLOBULIN",
        "TEST-CECT-CAP", "TEST-LN-EXCISIONAL-BIOPSY", "TEST-FLOW-CYTOMETRY",
        "TEST-CD20-IHC", "TEST-ECHO", "TEST-PREGNANCY",
    }
    missing = must_have - required
    assert not missing, f"WORKUP-SUSPECTED-LYMPHOMA missing essentials: {missing}"


# ── Workup matching by lineage ────────────────────────────────────────────


def test_acute_leukemia_lineage_hint_matches_correct_workup():
    result = load_content(KB_ROOT)
    susp = type("S", (), {})()
    susp.lineage_hint = "aml"
    susp.tissue_locations = ["bone_marrow"]
    susp.presentation = "blasts on smear, pancytopenia"
    matched = _match_workup(susp, result.entities_by_id)
    assert matched is not None
    assert matched["id"] == "WORKUP-SUSPECTED-ACUTE-LEUKEMIA"


def test_multiple_myeloma_lineage_hint_matches_correct_workup():
    result = load_content(KB_ROOT)
    susp = type("S", (), {})()
    susp.lineage_hint = "multiple_myeloma"
    susp.tissue_locations = ["bone_marrow", "bone"]
    susp.presentation = "lytic lesion + hypercalcemia + anemia"
    matched = _match_workup(susp, result.entities_by_id)
    assert matched is not None
    assert matched["id"] == "WORKUP-SUSPECTED-MULTIPLE-MYELOMA"


def test_mpn_lineage_hint_matches_correct_workup():
    result = load_content(KB_ROOT)
    susp = type("S", (), {})()
    susp.lineage_hint = "polycythemia_vera"
    susp.tissue_locations = ["bone_marrow"]
    susp.presentation = "erythrocytosis"
    matched = _match_workup(susp, result.entities_by_id)
    assert matched is not None
    assert matched["id"] == "WORKUP-SUSPECTED-MPN-MDS"


def test_undifferentiated_cytopenia_matches_evaluation_workup():
    result = load_content(KB_ROOT)
    susp = type("S", (), {})()
    susp.lineage_hint = "cytopenia_unexplained"
    susp.tissue_locations = ["peripheral_blood"]
    susp.presentation = "anemia and thrombocytopenia, no clear etiology"
    matched = _match_workup(susp, result.entities_by_id)
    assert matched is not None
    assert matched["id"] == "WORKUP-CYTOPENIA-EVALUATION"


# ── prior_tests_completed exclusion ───────────────────────────────────────


def _suspect_patient_with_prior(prior: list[str]) -> dict:
    return {
        "patient_id": "PZ-PRIOR-TEST",
        "disease": {
            "suspicion": {
                "lineage_hint": "b_cell_lymphoma",
                "tissue_locations": ["lymph_node"],
                "presentation": "lymphadenopathy + B-symptoms",
            }
        },
        "demographics": {"age": 60, "ecog": 1},
        "findings": {},
        "prior_tests_completed": prior,
    }


def test_prior_tests_completed_excluded_from_workup_steps():
    """If the patient already has CBC + LFT + HBV serology done elsewhere,
    those don't appear in the new DiagnosticPlan workup_steps."""
    prior = ["TEST-CBC", "TEST-LFT", "TEST-HBV-SEROLOGY"]
    p = _suspect_patient_with_prior(prior)

    result = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    assert result.diagnostic_plan is not None

    step_test_ids = {s.test_id for s in result.diagnostic_plan.workup_steps if s.test_id}
    for excluded in prior:
        assert excluded not in step_test_ids, (
            f"{excluded} is in prior_tests_completed but still in workup steps"
        )


def test_prior_tests_empty_no_exclusion_no_op():
    """Without prior_tests_completed, the workup is full size."""
    p = _suspect_patient_with_prior([])
    result = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    assert result.diagnostic_plan is not None
    # Full workup → many steps (lab + imaging + histology). Lymphoma workup
    # has 22 required_tests + biopsy combined — at least 15+ visible steps.
    assert len(result.diagnostic_plan.workup_steps) >= 15


# ── active_surveillance plan_track ────────────────────────────────────────


def test_surveillance_track_label_available():
    """Per user request: active_surveillance available as a plan_track
    with both UA and EN labels in the engine's track-label dictionaries."""
    assert "surveillance" in _TRACK_LABELS_UA
    assert "surveillance" in _TRACK_LABELS_EN
    assert "watch-and-wait" in _TRACK_LABELS_UA["surveillance"].lower()
    assert "watch-and-wait" in _TRACK_LABELS_EN["surveillance"].lower()
