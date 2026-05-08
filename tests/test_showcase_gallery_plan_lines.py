import json
from pathlib import Path

from knowledge_base.engine.plan import generate_plan


SHOWCASE_DIR = Path("examples")


def _indication_line(track):
    applicable_to = (track.indication_data or {}).get("applicable_to") or {}
    value = applicable_to.get("line_of_therapy")
    return int(value) if value is not None else None


def test_showcase_current_tracks_match_patient_line():
    for path in sorted(SHOWCASE_DIR.glob("patient_showcase_*.json")):
        patient = json.loads(path.read_text(encoding="utf-8"))
        result = generate_plan(patient, actionability_enabled=True)
        assert result.plan is not None, path
        assert result.plan.tracks, path
        patient_line = int(patient.get("line_of_therapy", 1))
        for track in result.plan.tracks:
            line = _indication_line(track)
            assert line in (None, patient_line), (
                path,
                track.indication_id,
                line,
                patient_line,
            )
        assert result.plan.tracks[0].is_default, path


def test_showcase_targeted_defaults_are_not_generic_fallbacks():
    expected = {
        "patient_showcase_nsclc_alk_fusion_1l.json": "IND-NSCLC-ALK-MET-1L",
        "patient_showcase_crc_braf_v600e_2l.json": "IND-CRC-METASTATIC-2L-BRAF-BEACON",
        "patient_showcase_breast_pik3ca_h1047r_2l.json": "IND-BREAST-HR-POS-2L-AKT-CAPIVASERTIB",
        "patient_showcase_nsclc_egfr_t790m_2l.json": "IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ",
        "patient_showcase_cholangio_idh1_r132_2l.json": "IND-CHOLANGIO-2L-IDH1-IVOSIDENIB",
        "patient_showcase_gastric_her2_amp_1l.json": "IND-GASTRIC-METASTATIC-1L-HER2-TOGA",
        "patient_showcase_prostate_brca2_germline_mcrpc.json": "IND-PROSTATE-MCRPC-2L-PARPI",
    }
    for filename, indication_id in expected.items():
        patient = json.loads((SHOWCASE_DIR / filename).read_text(encoding="utf-8"))
        result = generate_plan(patient, actionability_enabled=True)
        assert result.plan is not None
        assert result.plan.tracks[0].indication_id == indication_id
