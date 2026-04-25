"""End-to-end tests for T-cell lymphoma block (PTCL NOS, ALCL, AITL, MF/Sézary).

Shared CD30-driven algorithm pattern: CD30+ → CHP-Bv (ECHELON-2);
CD30- → CHOEP. ALCL is universally CD30+ — algorithm prefers CHP-Bv.
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_alcl_resolves():
    plan = generate_plan(_patient("patient_alcl_alk_negative.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-ALCL"
    assert plan.algorithm_id == "ALGO-ALCL-1L"


def test_alcl_routes_to_chp_bv():
    plan = generate_plan(_patient("patient_alcl_alk_negative.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-TCELL-1L-CHP-BV"


def test_chp_bv_replaces_vincristine_with_brentuximab():
    plan = generate_plan(_patient("patient_alcl_alk_negative.json"), kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    drug_ids = {c["drug_id"] for c in aggressive.regimen_data["components"]}
    assert "DRUG-BRENTUXIMAB-VEDOTIN" in drug_ids
    assert "DRUG-VINCRISTINE" not in drug_ids
    # Backbone shared with CHOP/CHP
    assert {"DRUG-CYCLOPHOSPHAMIDE", "DRUG-DOXORUBICIN", "DRUG-PREDNISONE"} <= drug_ids


def test_ptcl_cd30_negative_routes_to_choep():
    plan = generate_plan(_patient("patient_ptcl_cd30_negative.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-PTCL-NOS"
    assert plan.default_indication_id == "IND-TCELL-1L-CHOEP"


def test_aitl_cd30_positive_routes_to_chp_bv():
    plan = generate_plan(_patient("patient_aitl_cd30_positive.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-AITL"
    # CD30+ AITL → AITL-specific CHP-Bv aggressive track
    # (post-Tier 3: AITL has its own indication with EBER/IgG/DAT workup overlay,
    # not the shared T-cell one)
    assert plan.default_indication_id == "IND-AITL-1L-CHP-BV"


def test_aitl_cd30_negative_routes_to_aitl_choep():
    """CD30-neg AITL → AITL-specific CHOEP (not generic T-cell CHOEP).
    Layered EBV/AIHA/hypogamma workup distinguishes from PTCL CHOEP."""
    plan = generate_plan(_patient("patient_aitl_cd30_negative.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-AITL"
    assert plan.default_indication_id == "IND-AITL-1L-CHOEP"


def test_aitl_indications_layer_eber_dat_iggworkup():
    """AITL indications must carry EBER-ISH + DAT + immunoglobulins in
    required_tests — paraneoplastic surveillance specific to AITL biology."""
    plan = generate_plan(_patient("patient_aitl_cd30_positive.json"), kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    required = set(aggressive.indication_data["required_tests"])
    assert "TEST-EBER-ISH" in required, "AITL workup must include EBER-ISH"
    assert "TEST-DAT-COOMBS" in required, "AITL workup must include DAT/Coombs"
    assert "TEST-IMMUNOGLOBULINS" in required, "AITL workup must include IgG quantitation"


def test_choep_includes_etoposide():
    plan = generate_plan(_patient("patient_ptcl_cd30_negative.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    # CHOEP = CHOP + Etoposide
    assert "DRUG-ETOPOSIDE" in drug_ids
    assert {"DRUG-CYCLOPHOSPHAMIDE", "DRUG-DOXORUBICIN",
            "DRUG-VINCRISTINE", "DRUG-PREDNISONE"} <= drug_ids
