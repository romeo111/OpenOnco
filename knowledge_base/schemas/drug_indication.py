"""Regulatory and guideline status of a drug used for one KB indication.

This is deliberately separate from ``Drug.regulatory_status``: a medicine can
be on-label for one disease/line/biomarker context and off-label or
investigational for another.  Records are provenance and display metadata;
the planning engine must never use them to hide an otherwise visible draft.
"""

from enum import Enum
from typing import Optional

from pydantic import Field, model_validator

from .base import Base


class DrugUseStatus(str, Enum):
    ON_LABEL = "on_label"
    OFF_LABEL_GUIDELINE_SUPPORTED = "off_label_guideline_supported"
    INVESTIGATIONAL = "investigational"
    NOT_ASSESSED = "not_assessed"


class JurisdictionUseStatus(Base):
    """One jurisdiction-specific status, always backed by provenance.

    ``not_assessed`` explicitly records a review queue item.  It is not a
    clinical assertion and therefore does not require a source.  Every other
    status requires at least one Source ID, enforced below.
    """

    jurisdiction: str  # e.g. FDA | EMA | Ukraine | guideline
    status: DrugUseStatus
    source_ids: list[str] = Field(default_factory=list)
    source_locator: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _require_provenance_for_assessed_status(self) -> "JurisdictionUseStatus":
        if self.status != DrugUseStatus.NOT_ASSESSED and not self.source_ids:
            raise ValueError(
                "Assessed drug-indication status requires at least one source_id"
            )
        return self


class DrugIndication(Base):
    """One drug ↔ indication assessment with jurisdiction-level status."""

    id: str
    drug_id: str
    indication_id: str
    disease_id: str
    regimen_ids: list[str] = Field(default_factory=list)
    statuses: list[JurisdictionUseStatus] = Field(min_length=1)
    evidence_sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _require_unique_jurisdictions(self) -> "DrugIndication":
        jurisdictions = [item.jurisdiction.casefold() for item in self.statuses]
        if len(jurisdictions) != len(set(jurisdictions)):
            raise ValueError("statuses must contain each jurisdiction at most once")
        return self
