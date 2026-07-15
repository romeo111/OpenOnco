"""Regression coverage for diseases that previously had only starter examples."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_lgg_coverage_example_generates_rt_pcv_plan():
    plan = generate_plan(_patient("patient_coverage_lgg_rt_pcv_1l.json"), kb_root=KB_ROOT)

    assert plan.disease_id == "DIS-GLIOMA-LOW-GRADE"
    assert plan.algorithm_id == "ALGO-GLIOMA-LGG-1L"
    assert plan.default_indication_id == "IND-GLIOMA-LOW-GRADE-1L-RT-PCV"
    assert plan.plan and plan.plan.tracks


def test_jmml_coverage_example_generates_allohct_plan():
    plan = generate_plan(_patient("patient_coverage_jmml_allohct_1l.json"), kb_root=KB_ROOT)

    assert plan.disease_id == "DIS-JMML"
    assert plan.algorithm_id == "ALGO-JMML-1L"
    assert plan.default_indication_id == "IND-JMML-1L-ALLOHCT"
    assert plan.plan and plan.plan.tracks


def test_meningioma_coverage_example_generates_local_therapy_plan():
    plan = generate_plan(_patient("patient_coverage_meningioma_resection_rt_1l.json"), kb_root=KB_ROOT)

    assert plan.disease_id == "DIS-MENINGIOMA"
    assert plan.algorithm_id == "ALGO-MENINGIOMA-1L"
    assert plan.default_indication_id == "IND-MENINGIOMA-1L-RESECTION-RT"
    assert plan.plan and plan.plan.tracks
