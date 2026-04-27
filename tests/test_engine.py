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
    """Bulky HCV-MZL patient: BR should become the default.

    NOTE: ALGO-HCV-MZL-1L is now a 4-step tree (post-CSD orphan-RF wiring
    2026-04-27):
      step 1 = RF-DECOMP-CIRRHOSIS → ANTIVIRAL (de-escalate)
      step 2 = RF-HCV-MZL-FRAILTY-AGE → ANTIVIRAL (de-escalate)
      step 3 = RF-BULKY-DISEASE / RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION → BR
      step 4 = HCV-RNA+ + indolent → ANTIVIRAL
    Bulky-without-decomp, non-frail patient: step 1 False, step 2 False,
    step 3 True → BR."""

    result = generate_plan(_patient("patient_zero_bulky.json"), kb_root=KB_ROOT)

    assert result.disease_id == "DIS-HCV-MZL"
    assert result.default_indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"
    assert result.alternative_indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"

    step_1 = next((t for t in result.trace if t.get("step") == 1), None)
    step_2 = next((t for t in result.trace if t.get("step") == 2), None)
    step_3 = next((t for t in result.trace if t.get("step") == 3), None)
    assert step_1 is not None and step_1["outcome"] is False, (
        "decomp-cirrhosis step should NOT fire for the bulky-without-decomp patient"
    )
    assert step_2 is not None and step_2["outcome"] is False, (
        "frailty-age step should NOT fire for the age-62 fit patient"
    )
    assert step_3 is not None and step_3["outcome"] is True, (
        "bulky-disease step should fire and route to BR-AGGRESSIVE"
    )


def test_plan_result_has_full_indication_records():
    """PlanResult should carry fully-materialised Indication data for rendering."""

    result = generate_plan(_patient("patient_zero_indolent.json"), kb_root=KB_ROOT)
    assert result.default_indication is not None
    assert result.default_indication.get("id") == "IND-HCV-MZL-1L-ANTIVIRAL"
    assert result.default_indication.get("recommended_regimen") == "REG-DAA-SOF-VEL"


def test_plan_object_has_two_tracks_in_one_document():
    """Per CHARTER §2 the Plan presents both alternatives in one document
    (one Plan, multiple PlanTrack entries). One track is marked is_default."""

    result = generate_plan(_patient("patient_zero_indolent.json"), kb_root=KB_ROOT)
    assert result.plan is not None
    assert len(result.plan.tracks) >= 2
    defaults = [t for t in result.plan.tracks if t.is_default]
    assert len(defaults) == 1, "exactly one track should be marked as engine default"
    assert defaults[0].indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"


def test_plan_carries_fda_compliance_metadata():
    """Per CHARTER §15 every Plan must surface the FDA Criterion-4 elements
    so an HCP can independently review the basis."""

    result = generate_plan(_patient("patient_zero_indolent.json"), kb_root=KB_ROOT)
    fda = result.plan.fda_compliance
    assert fda.intended_use
    assert fda.hcp_user_specification
    assert fda.patient_population_match
    assert fda.algorithm_summary
    assert fda.automation_bias_warning
    assert fda.time_critical is False  # outpatient cancer planning
    assert fda.data_sources_summary, "Plan must cite at least one source"


def test_plan_tracks_materialize_regimen_and_supportive_care():
    """Aggressive (BR) track should bring its full Regimen + supportive care
    references into the Plan output for one-document rendering."""

    result = generate_plan(_patient("patient_zero_bulky.json"), kb_root=KB_ROOT)
    default = next(t for t in result.plan.tracks if t.is_default)
    assert default.indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"
    assert default.regimen_data is not None
    assert default.regimen_data.get("id") == "REG-BR-STANDARD"
    # BR has mandatory supportive care wired (antiemetic + PJP)
    assert len(default.supportive_care_data) >= 2
    # And hard contraindications are surfaced
    assert len(default.contraindications_data) >= 1
