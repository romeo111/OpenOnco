from __future__ import annotations

from pathlib import Path

from knowledge_base.engine import generate_plan
from knowledge_base.validation.loader import clear_load_cache, load_content

KB_ROOT = Path(__file__).parent.parent / "knowledge_base" / "hosted" / "content"


def _patient(findings: dict) -> dict:
    return {
        "patient_id": "ESOPH-1L-TEST",
        "disease": {"id": "DIS-ESOPHAGEAL"},
        "disease_state": "metastatic",
        "line_of_therapy": 1,
        "findings": {
            "metastatic_or_unresectable": True,
            **findings,
        },
        "demographics": {"ecog": 1},
        "biomarkers": {},
    }


def test_esophageal_1l_outputs_include_a1_indications() -> None:
    clear_load_cache()
    result = load_content(KB_ROOT)
    algo = result.entities_by_id["ALGO-ESOPH-METASTATIC-1L"]["data"]

    assert "IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO" in algo["output_indications"]
    assert (
        "IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO"
        in algo["output_indications"]
    )


def test_escc_cps_positive_chemo_sparing_routes_to_ipi_nivo() -> None:
    plan = generate_plan(
        _patient(
            {
                "histology_escc": True,
                "ESCC CPS >=1": True,
                "chemo_sparing_preference": True,
            }
        ),
        kb_root=KB_ROOT,
    )

    assert plan.algorithm_id == "ALGO-ESOPH-METASTATIC-1L"
    assert plan.default_indication_id == "IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO"


def test_escc_cps_positive_without_chemo_sparing_keeps_nivo_chemo() -> None:
    plan = generate_plan(
        _patient(
            {
                "histology_escc": True,
                "ESCC CPS >=1": True,
                "rapid_response_priority": True,
            }
        ),
        kb_root=KB_ROOT,
    )

    assert plan.default_indication_id == "IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC"


def test_her2_positive_eac_routes_to_trastuzumab_chemo() -> None:
    plan = generate_plan(
        _patient(
            {
                "histology_adenocarcinoma": True,
                "her2_positive": True,
                "PD-L1 CPS >= 10": True,
            }
        ),
        kb_root=KB_ROOT,
    )

    assert (
        plan.default_indication_id
        == "IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO"
    )


def test_her2_negative_eac_keeps_pembro_chemo() -> None:
    plan = generate_plan(
        _patient(
            {
                "histology_adenocarcinoma": True,
                "PD-L1 CPS >= 10": True,
            }
        ),
        kb_root=KB_ROOT,
    )

    assert plan.default_indication_id == "IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO"
