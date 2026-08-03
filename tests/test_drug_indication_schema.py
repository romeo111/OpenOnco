import pytest
from pydantic import ValidationError

from knowledge_base.schemas.drug_indication import DrugIndication


def test_assessed_drug_indication_status_requires_provenance():
    with pytest.raises(ValidationError, match="requires at least one source_id"):
        DrugIndication.model_validate(
            {
                "id": "DIND-TEST",
                "drug_id": "DRUG-TEST",
                "indication_id": "IND-TEST",
                "disease_id": "DIS-TEST",
                "statuses": [{"jurisdiction": "FDA", "status": "on_label"}],
            }
        )


def test_not_assessed_drug_indication_is_explicit_review_queue_item():
    item = DrugIndication.model_validate(
        {
            "id": "DIND-TEST",
            "drug_id": "DRUG-TEST",
            "indication_id": "IND-TEST",
            "disease_id": "DIS-TEST",
            "statuses": [{"jurisdiction": "FDA", "status": "not_assessed"}],
        }
    )

    assert item.statuses[0].status.value == "not_assessed"
