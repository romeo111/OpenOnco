"""End-to-end tests for the rule engine on the HCV-MZL reference case."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_indolent_hcv_mzl_picks_antiviral_default():
    """Low-burden HCV-MZL patient: antiviral-only should be the default,
    BR should be the alternative."""

    result = generate_plan(_patient("patient_zero_indolent.json"), kb_root=KB_ROOT)

    assert result.disease_id == "DIS-HCV-MZL"
    assert result.algorithm_id == "ALGO-HCV-MZL-1L"
    assert result.default_indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"
    assert result.alternative_indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"
    assert result.warnings == []


def test_bulky_hcv_mzl_picks_br_default():
    """Bulky HCV-MZL patient: BR should become the default via
    RF-BULKY-DISEASE firing; antiviral remains the alternative."""

    result = generate_plan(_patient("patient_zero_bulky.json"), kb_root=KB_ROOT)

    assert result.disease_id == "DIS-HCV-MZL"
    assert result.default_indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"
    assert result.alternative_indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"
    # RF-BULKY-DISEASE fired at step 1
    step_1 = next((t for t in result.trace if t.get("step") == 1), None)
    assert step_1 is not None
    assert step_1["outcome"] is True


def test_plan_result_has_full_indication_records():
    """PlanResult should carry fully-materialised Indication data for rendering."""

    result = generate_plan(_patient("patient_zero_indolent.json"), kb_root=KB_ROOT)
    assert result.default_indication is not None
    assert result.default_indication.get("id") == "IND-HCV-MZL-1L-ANTIVIRAL"
    assert result.default_indication.get("recommended_regimen") == "REG-DAA-SOF-VEL"
