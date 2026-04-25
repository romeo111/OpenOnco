"""End-to-end engine test for Classical Hodgkin Lymphoma + NLPBL."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


# ── Classical Hodgkin ─────────────────────────────────────────────────────


def test_chl_resolves():
    plan = generate_plan(_patient("patient_chl_advanced.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-CHL"
    assert plan.algorithm_id == "ALGO-CHL-1L"


def test_chl_advanced_routes_to_a_avd():
    plan = generate_plan(_patient("patient_chl_advanced.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-CHL-1L-A-AVD"


def test_chl_early_routes_to_abvd():
    plan = generate_plan(_patient("patient_chl_early.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-CHL-1L-ABVD"


def test_a_avd_replaces_bleomycin_with_brentuximab():
    plan = generate_plan(_patient("patient_chl_advanced.json"), kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    drug_ids = {c["drug_id"] for c in aggressive.regimen_data["components"]}
    # A+AVD: bleomycin REMOVED, brentuximab ADDED
    assert "DRUG-BRENTUXIMAB-VEDOTIN" in drug_ids
    assert "DRUG-BLEOMYCIN" not in drug_ids
    # Backbone preserved
    assert {"DRUG-DOXORUBICIN", "DRUG-VINBLASTINE", "DRUG-DACARBAZINE"} <= drug_ids


def test_abvd_includes_bleomycin():
    plan = generate_plan(_patient("patient_chl_early.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    # ABVD: classical 4-drug combo
    assert {"DRUG-DOXORUBICIN", "DRUG-BLEOMYCIN", "DRUG-VINBLASTINE",
            "DRUG-DACARBAZINE"} <= drug_ids


# ── NLPBL ─────────────────────────────────────────────────────────────────


def test_nlpbl_resolves():
    plan = generate_plan(_patient("patient_nlpbl_early.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-NLPBL"
    assert plan.algorithm_id == "ALGO-NLPBL-1L"


def test_nlpbl_early_routes_to_observation_or_rt():
    plan = generate_plan(_patient("patient_nlpbl_early.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-NLPBL-1L-OBSERVATION-OR-RT"


def test_nlpbl_observation_track_has_no_regimen():
    """Surveillance / RT-alone track has no drug regimen."""
    plan = generate_plan(_patient("patient_nlpbl_early.json"), kb_root=KB_ROOT)
    surv = next(t for t in plan.plan.tracks if t.track_id == "surveillance")
    assert surv.regimen_data is None


def test_nlpbl_ia_rt_contraindicated_routes_to_rituximab_mono():
    """Early-stage NLPBL where RT contraindicated (young, breast/thyroid
    field overlap) — engine should select rituximab monotherapy alternative
    instead of ISRT default. CD20+ biology preserved (NLPBL = B-cell post
    WHO 5th-ed reclassification, NOT Hodgkin)."""
    plan = generate_plan(_patient("patient_nlpbl_ia_rituximab.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-NLPBL"
    assert plan.default_indication_id == "IND-NLPBL-1L-RITUXIMAB-MONO"


def test_nlpbl_rituximab_mono_uses_rituximab():
    """Rituximab-mono regimen must contain DRUG-RITUXIMAB only (single
    agent). NLPBL must NEVER route through ABVD pathway."""
    plan = generate_plan(_patient("patient_nlpbl_ia_rituximab.json"), kb_root=KB_ROOT)
    track = next(t for t in plan.plan.tracks if t.regimen_data is not None)
    drug_ids = {c["drug_id"] for c in track.regimen_data["components"]}
    assert drug_ids == {"DRUG-RITUXIMAB"}, f"NLPBL R-mono should be single-agent; got {drug_ids}"
    # Verify ABVD components NEVER appear in any NLPBL track
    for t in plan.plan.tracks:
        if t.regimen_data:
            ds = {c["drug_id"] for c in t.regimen_data["components"]}
            assert "DRUG-BLEOMYCIN" not in ds, "NLPBL must not route through ABVD"
            assert "DRUG-VINBLASTINE" not in ds, "NLPBL must not route through ABVD"
            assert "DRUG-DACARBAZINE" not in ds, "NLPBL must not route through ABVD"
