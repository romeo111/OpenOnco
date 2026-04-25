"""End-to-end tests for HCL + Waldenström + HGBL-DH (3 smaller B-cell entities)."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


# ── HCL ───────────────────────────────────────────────────────────────────


def test_hcl_resolves():
    plan = generate_plan(_patient("patient_hcl_typical.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-HCL"
    assert plan.algorithm_id == "ALGO-HCL-1L"


def test_hcl_routes_to_cladribine():
    plan = generate_plan(_patient("patient_hcl_typical.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-HCL-1L-CLADRIBINE"


def test_hcl_regimen_uses_cladribine():
    plan = generate_plan(_patient("patient_hcl_typical.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    assert standard.regimen_data["id"] == "REG-CLADRIBINE-SINGLE"
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    assert "DRUG-CLADRIBINE" in drug_ids


# ── WM ────────────────────────────────────────────────────────────────────


def test_wm_resolves():
    plan = generate_plan(_patient("patient_wm_myd88_positive.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-WM"
    assert plan.algorithm_id == "ALGO-WM-1L"


def test_wm_myd88_positive_routes_to_btki():
    plan = generate_plan(_patient("patient_wm_myd88_positive.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-WM-1L-BTKI"


def test_wm_btki_uses_zanubrutinib():
    plan = generate_plan(_patient("patient_wm_myd88_positive.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    assert "DRUG-ZANUBRUTINIB" in drug_ids


# ── HGBL-DH ───────────────────────────────────────────────────────────────


def test_hgbl_dh_resolves():
    plan = generate_plan(_patient("patient_hgbl_double_hit.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-HGBL-DH"
    assert plan.algorithm_id == "ALGO-HGBL-DH-1L"


def test_hgbl_dh_routes_to_da_epoch_r():
    plan = generate_plan(_patient("patient_hgbl_double_hit.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-HGBL-DH-1L-DAEPOCHR"


def test_hgbl_dh_reuses_da_epoch_r_regimen_from_burkitt():
    """Cross-disease regimen reuse — DA-EPOCH-R serves Burkitt + HGBL-DH."""
    plan = generate_plan(_patient("patient_hgbl_double_hit.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    assert standard.regimen_data["id"] == "REG-DA-EPOCH-R"
