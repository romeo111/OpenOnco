from knowledge_base.schemas import RadiationModality, SurgeryModality


def test_surgery_modality_schema_accepts_structured_local_therapy():
    row = SurgeryModality.model_validate(
        {
            "id": "SURG-CRC-RESECTABLE-PRIMARY",
            "disease_id": "DIS-CRC",
            "indication_ids": ["IND-CRC-ADJUVANT-STAGE3-FOLFOX"],
            "intent": "definitive",
            "procedure": "Oncologic colectomy with regional lymphadenectomy",
            "selection_criteria": ["Resectable non-metastatic colon cancer"],
            "source_refs": ["SRC-NCCN-COLON-2026"],
        }
    )

    assert row.intent == "definitive"
    assert row.draft is True
    assert row.source_refs == ["SRC-NCCN-COLON-2026"]


def test_radiation_modality_schema_accepts_dose_fractionation():
    row = RadiationModality.model_validate(
        {
            "id": "RT-ANAL-SCC-DEFINITIVE-CRT",
            "disease_id": "DIS-ANAL-SCC",
            "indication_ids": ["IND-ANAL-SCC-LA-1L-NIGRO-CRT"],
            "intent": "definitive",
            "anatomical_site": "anus and involved nodes",
            "technique": "IMRT",
            "dose": {
                "total_dose": "50.4-59.4 Gy",
                "fractions": "28-33",
            },
            "concurrent_systemic_therapy": ["REG-MMC-5FU-RT"],
            "source_refs": ["SRC-NCCN-ANAL-2026"],
        }
    )

    assert row.dose is not None
    assert row.dose.fractions == "28-33"
    assert row.concurrent_systemic_therapy == ["REG-MMC-5FU-RT"]
