"""End-to-end engine test for Burkitt — risk-stratified DA-EPOCH-R vs CODOX-M/IVAC."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_burkitt_resolves():
    plan = generate_plan(_patient("patient_burkitt_low_risk.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-BURKITT"
    assert plan.algorithm_id == "ALGO-BURKITT-1L"


def test_burkitt_low_risk_routes_to_daepochr():
    plan = generate_plan(_patient("patient_burkitt_low_risk.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-BURKITT-1L-DAEPOCHR"


def test_burkitt_high_risk_routes_to_codoxm_ivac():
    plan = generate_plan(_patient("patient_burkitt_high_risk.json"), kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-BURKITT-1L-CODOXM-IVAC"


def test_da_epoch_r_includes_etoposide():
    plan = generate_plan(_patient("patient_burkitt_low_risk.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    assert "DRUG-ETOPOSIDE" in drug_ids
    # DA-EPOCH-R differs from R-CHOP by adding etoposide + continuous infusion
    assert {"DRUG-RITUXIMAB", "DRUG-ETOPOSIDE", "DRUG-DOXORUBICIN",
            "DRUG-VINCRISTINE", "DRUG-CYCLOPHOSPHAMIDE", "DRUG-PREDNISONE"} <= drug_ids


def test_codoxm_ivac_includes_methotrexate():
    plan = generate_plan(_patient("patient_burkitt_high_risk.json"), kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    drug_ids = {c["drug_id"] for c in aggressive.regimen_data["components"]}
    assert "DRUG-METHOTREXATE" in drug_ids  # HD-MTX for CNS
    assert "DRUG-CYTARABINE" in drug_ids    # IVAC HiDAC


def test_burkitt_high_risk_in_trace():
    plan = generate_plan(_patient("patient_burkitt_high_risk.json"), kb_root=KB_ROOT)
    assert "RF-BURKITT-HIGH-RISK" in json.dumps(plan.trace)
