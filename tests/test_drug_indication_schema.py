from knowledge_base.schemas import DrugIndication


def test_drug_indication_defaults_to_draft_unknown_status():
    row = DrugIndication.model_validate(
        {
            "id": "DIND-RITUXIMAB-DLBCL-1L-RCHOP",
            "drug_id": "DRUG-RITUXIMAB",
            "disease_id": "DIS-DLBCL-NOS",
            "indication_id": "IND-DLBCL-1L-RCHOP",
            "regimen_id": "REG-RCHOP-21",
        }
    )

    assert row.draft is True
    assert row.label_status == "unknown_pending_review"
    assert row.reimbursement_status == "unknown_pending_review"
    assert row.regulatory_statuses == []
    assert row.reimbursement_statuses == []


def test_drug_indication_accepts_source_backed_status_rows():
    row = DrugIndication.model_validate(
        {
            "id": "DIND-PEMBROLIZUMAB-NSCLC-PDL1",
            "drug_id": "DRUG-PEMBROLIZUMAB",
            "disease_id": "DIS-NSCLC",
            "label_status": "labeled",
            "reimbursement_status": "partially_reimbursed",
            "regulatory_statuses": [
                {
                    "jurisdiction": "FDA",
                    "status": "labeled",
                    "source_refs": ["SRC-FDA-PEMBROLIZUMAB-LABEL"],
                }
            ],
            "reimbursement_statuses": [
                {
                    "jurisdiction": "Ukraine",
                    "payer": "NSZU",
                    "status": "unknown_pending_review",
                    "source_refs": ["SRC-NSZU-PKG3-2026"],
                }
            ],
            "evidence_source_refs": ["SRC-NCCN-NSCLC-2026"],
        }
    )

    assert row.regulatory_statuses[0].jurisdiction == "FDA"
    assert row.regulatory_statuses[0].source_refs == ["SRC-FDA-PEMBROLIZUMAB-LABEL"]
    assert row.reimbursement_statuses[0].payer == "NSZU"
