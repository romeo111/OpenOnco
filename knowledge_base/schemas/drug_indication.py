"""DrugIndication entity.

First-class drug-use metadata for one drug in one disease/indication context.

This separates "the regimen uses this drug" from "the drug is labeled,
off-label guideline-supported, reimbursed, or still unknown in a specific
jurisdiction." The engine must not use this entity for track selection; it is
render, audit, payer, and governance metadata.
"""

from typing import Literal, Optional

from pydantic import Field, field_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base


LabelStatus = Literal[
    "labeled",
    "off_label_guideline_supported",
    "off_label_compendia_supported",
    "off_label_investigational",
    "not_labeled",
    "unknown_pending_review",
]

ReimbursementStatus = Literal[
    "reimbursed",
    "partially_reimbursed",
    "not_reimbursed",
    "not_applicable",
    "unknown_pending_review",
]


class RegulatoryLabelRecord(Base):
    """One jurisdiction's label/off-label status for a drug-use pair."""

    jurisdiction: str  # FDA | EMA | Ukraine | NCCN | ESMO | other
    status: LabelStatus = "unknown_pending_review"
    label_indication_text: Optional[str] = None
    approval_reference: Optional[str] = None
    source_refs: list[str] = Field(default_factory=list)
    current_as_of: Optional[str] = None
    notes: Optional[str] = None


class ReimbursementRecord(Base):
    """One payer/access status for a drug-use pair."""

    jurisdiction: str = "Ukraine"
    payer: Optional[str] = "NSZU"
    status: ReimbursementStatus = "unknown_pending_review"
    reimbursement_indication_text: Optional[str] = None
    source_refs: list[str] = Field(default_factory=list)
    current_as_of: Optional[str] = None
    notes: Optional[str] = None


class DrugIndication(Base):
    id: str

    drug_id: str
    disease_id: str
    indication_id: Optional[str] = None
    regimen_id: Optional[str] = None
    line_of_therapy: Optional[int] = None
    clinical_context: Optional[str] = None

    # Summary status for quick filters. Detailed jurisdiction-specific rows
    # live below and are the source of truth once reviewed.
    label_status: LabelStatus = "unknown_pending_review"
    reimbursement_status: ReimbursementStatus = "unknown_pending_review"

    regulatory_statuses: list[RegulatoryLabelRecord] = Field(default_factory=list)
    reimbursement_statuses: list[ReimbursementRecord] = Field(default_factory=list)

    nccn_category: Optional[str] = None
    esmo_level: Optional[str] = None
    evidence_source_refs: list[str] = Field(default_factory=list)

    # Backfill provenance. Generated rows should remain draft until a reviewer
    # confirms the label/reimbursement status.
    inferred_from: dict = Field(default_factory=dict)
    draft: bool = True

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)
