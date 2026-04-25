"""Tests for the curated questionnaire schema + live evaluator.

Verifies:
1. All 3 hand-authored questionnaire YAMLs load + validate against schema
2. evaluate_partial() returns sane values for empty / partial / full profiles
3. fired_redflags + would_select_indication match what generate_plan would do
4. assemble_profile() reconstructs a profile from flat answers + fixed_fields
"""

from __future__ import annotations

from pathlib import Path

import yaml

from knowledge_base.engine import (
    assemble_profile,
    evaluate_partial,
    generate_plan,
    list_questions,
)
from knowledge_base.schemas import Questionnaire


REPO = Path(__file__).resolve().parent.parent
QDIR = REPO / "knowledge_base" / "hosted" / "content" / "questionnaires"
KB = REPO / "knowledge_base" / "hosted" / "content"


def _load_quest(name: str) -> dict:
    return yaml.safe_load((QDIR / name).read_text(encoding="utf-8"))


def test_three_questionnaires_load_and_validate():
    files = sorted(QDIR.glob("*.yaml"))
    assert len(files) >= 3, f"expected ≥3 questionnaires, got {len(files)}"
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        # Pydantic validation — raises on schema violation
        Questionnaire(**data)


def test_list_questions_flattens_groups():
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    flat = list_questions(q)
    assert len(flat) > 5
    assert all("_group" in qq for qq in flat)
    assert all(qq.get("field") for qq in flat)


def test_evaluate_empty_profile_reports_missing_critical():
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    res = evaluate_partial({}, q, kb_root=KB)
    assert res.filled_count == 0
    assert res.completion_pct == 0
    assert len(res.missing_critical) > 0
    assert res.ready_to_generate is False


def test_evaluate_partial_profile_progresses():
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    profile = {
        "demographics": {"age": 49, "ecog": 1, "sex": "male",
                         "fit_for_chemoimmunotherapy": True,
                         "decompensated_cirrhosis": False},
        "biomarkers": {"BIO-HCV-RNA": "positive"},
    }
    res = evaluate_partial(profile, q, kb_root=KB)
    assert res.filled_count > 0
    assert res.completion_pct > 0


def test_evaluate_full_hcv_mzl_indolent_picks_antiviral():
    """Reference-case-like indolent HCV+ profile → engine picks ANTIVIRAL."""
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    profile = {
        "patient_id": "TEST",
        "disease": {"icd_o_3_morphology": "9699/3"},
        "line_of_therapy": 1,
        "demographics": {
            "age": 49, "sex": "male", "ecog": 1,
            "fit_for_chemoimmunotherapy": True,
            "decompensated_cirrhosis": False,
        },
        "biomarkers": {"BIO-HCV-RNA": "positive"},
        "findings": {
            "dominant_nodal_mass_cm": 5.3,
            "mediastinal_ratio": 0.12,
            "symptomatic_b_symptoms_severe": False,
            "biopsy_shows_dlbcl": False,
            "ldh_ratio_to_uln": 1.05,
            "clinical_progression_weeks": 48,
            "HCV RNA positive": True,
            "Indolent presentation (non-bulky, asymptomatic or minimally symptomatic)": True,
            "hbsag": "negative",
            "anti_hbc_total": "negative",
        },
    }
    res = evaluate_partial(profile, q, kb_root=KB)
    assert res.would_select_indication == "IND-HCV-MZL-1L-ANTIVIRAL", res.would_select_indication
    assert res.ready_to_generate is True


def test_evaluate_bulky_hcv_mzl_picks_aggressive():
    """Bulky disease (RF-BULKY-DISEASE fires) → engine picks BR-AGGRESSIVE."""
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    profile = {
        "patient_id": "TEST-BULKY",
        "disease": {"icd_o_3_morphology": "9699/3"},
        "line_of_therapy": 1,
        "demographics": {"age": 60, "sex": "male", "ecog": 1,
                         "fit_for_chemoimmunotherapy": True,
                         "decompensated_cirrhosis": False},
        "biomarkers": {"BIO-HCV-RNA": "positive"},
        "findings": {
            "dominant_nodal_mass_cm": 8.5,  # bulky
            "symptomatic_b_symptoms_severe": False,
            "biopsy_shows_dlbcl": False,
            "ldh_ratio_to_uln": 1.2,
            "HCV RNA positive": True,
            "Indolent presentation (non-bulky, asymptomatic or minimally symptomatic)": False,
            "hbsag": "negative",
            "anti_hbc_total": "negative",
        },
    }
    res = evaluate_partial(profile, q, kb_root=KB)
    assert "RF-BULKY-DISEASE" in res.fired_redflags
    assert res.would_select_indication == "IND-HCV-MZL-1L-BR-AGGRESSIVE"


def test_assemble_profile_merges_fixed_with_answers():
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    answers = {
        "patient_id": "ASSEMBLE-1",
        "demographics.age": 55,
        "demographics.ecog": 0,
        "biomarkers.BIO-HCV-RNA": "positive",
        "findings.dominant_nodal_mass_cm": 4.2,
    }
    profile = assemble_profile(q, answers)
    assert profile["disease"]["icd_o_3_morphology"] == "9699/3"
    assert profile["line_of_therapy"] == 1
    assert profile["patient_id"] == "ASSEMBLE-1"
    assert profile["demographics"]["age"] == 55
    assert profile["biomarkers"]["BIO-HCV-RNA"] == "positive"


def test_evaluator_matches_real_engine():
    """The would_select_indication should equal what generate_plan picks."""
    q = _load_quest("quest_hcv_mzl_1l.yaml")
    answers = {
        "patient_id": "MATCH-TEST",
        "demographics.age": 49,
        "demographics.sex": "male",
        "demographics.ecog": 1,
        "demographics.fit_for_chemoimmunotherapy": True,
        "demographics.decompensated_cirrhosis": False,
        "biomarkers.BIO-HCV-RNA": "positive",
        "findings.dominant_nodal_mass_cm": 5.3,
        "findings.HCV RNA positive": True,
        "findings.Indolent presentation (non-bulky, asymptomatic or minimally symptomatic)": True,
        "findings.biopsy_shows_dlbcl": False,
        "findings.symptomatic_b_symptoms_severe": False,
        "findings.hbsag": "negative",
        "findings.anti_hbc_total": "negative",
    }
    profile = assemble_profile(q, answers)
    preview = evaluate_partial(profile, q, kb_root=KB)
    plan = generate_plan(profile, kb_root=KB)
    assert preview.would_select_indication == plan.default_indication_id


def test_mm_questionnaire_high_risk_picks_dvrd():
    q = _load_quest("quest_mm_1l.yaml")
    profile = {
        "patient_id": "MM-HR",
        "disease": {"icd_o_3_morphology": "9732/3"},
        "line_of_therapy": 1,
        "demographics": {"age": 60, "sex": "male", "ecog": 1,
                         "fit_for_transplant": True,
                         "pregnancy_status": "not_pregnant"},
        "biomarkers": {"BIO-MM-CYTOGENETICS-HR": "high_risk"},
        "findings": {
            "del_17p": True, "t_4_14": False, "t_14_16": False,
            "gain_1q": False, "tp53_mutation": True,
            "creatinine_clearance_ml_min": 80,
            "serum_creatinine_mg_dl": 1.0,
            "mm_renal_failure": False,
            "severe_neuropathy_grade": 0,
            "hbsag": "negative",
            "mm_cytogenetics_high_risk": True,
        },
    }
    res = evaluate_partial(profile, q, kb_root=KB)
    assert "RF-MM-HIGH-RISK-CYTOGENETICS" in res.fired_redflags
    assert res.would_select_indication == "IND-MM-1L-DVRD"


def test_cll_questionnaire_high_risk_picks_veno():
    q = _load_quest("quest_cll_1l.yaml")
    profile = {
        "patient_id": "CLL-HR",
        "disease": {"icd_o_3_morphology": "9823/3"},
        "line_of_therapy": 1,
        "demographics": {"age": 70, "sex": "male", "ecog": 1,
                         "fit_for_chemoimmunotherapy": False},
        "biomarkers": {"BIO-CLL-HIGH-RISK-GENETICS": "high_risk"},
        "findings": {
            "tp53_mutation": True, "del_17p": True,
            "ighv_unmutated": True, "complex_karyotype": False,
            "iwcll_indication_present": True,
            "afib_history": False, "bleeding_risk_high": False,
            "hbsag": "negative", "anti_hbc_total": "negative",
        },
    }
    res = evaluate_partial(profile, q, kb_root=KB)
    assert "RF-CLL-HIGH-RISK" in res.fired_redflags
    assert res.would_select_indication == "IND-CLL-1L-VENO"
