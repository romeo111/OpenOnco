from __future__ import annotations

from knowledge_base.engine.civic_disease_matcher import civic_entry_matches_disease


def _disease(disease_id: str, english: str, synonyms=None, oncotree=""):
    return {
        "id": disease_id,
        "names": {
            "preferred": english,
            "english": english,
            "synonyms": list(synonyms or []),
        },
        "oncotree_code": oncotree,
    }


def test_crc_civic_colorectal_cancer_matches_dis_crc():
    entry = {"disease": "Colorectal Cancer"}
    disease = _disease(
        "DIS-CRC",
        "Colorectal carcinoma",
        synonyms=["Colon cancer + Rectal cancer", "Bowel cancer"],
        oncotree="COADREAD",
    )

    assert civic_entry_matches_disease(entry, disease) is True


def test_braf_melanoma_evidence_does_not_match_crc_cell():
    entry = {"disease": "Melanoma"}
    disease = _disease("DIS-CRC", "Colorectal carcinoma")

    assert civic_entry_matches_disease(entry, disease) is False


def test_nsclc_alias_matches_civic_lung_non_small_cell_carcinoma():
    entry = {"disease": "Lung Non-small Cell Carcinoma"}
    disease = _disease("DIS-NSCLC", "Non-small cell lung cancer", oncotree="NSCLC")

    assert civic_entry_matches_disease(entry, disease) is True


def test_missing_disease_metadata_preserves_fail_open_behavior():
    assert civic_entry_matches_disease({"disease": "Melanoma"}, None) is True


def test_missing_civic_disease_rejects_when_local_disease_is_known():
    disease = _disease("DIS-CRC", "Colorectal carcinoma")

    assert civic_entry_matches_disease({"disease": ""}, disease) is False
