"""Structured local-modality entities.

Surgery and radiation were previously represented mostly as prose inside
Indication text. These schemas make local therapy reviewable, citable, and
machine-auditable without letting the engine choose modalities autonomously.
"""

from typing import Literal, Optional

from pydantic import Field, field_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base


ModalityIntent = Literal[
    "diagnostic",
    "neoadjuvant",
    "definitive",
    "adjuvant",
    "consolidative",
    "palliative",
    "salvage",
]


class ModalityTiming(Base):
    phase: Optional[str] = None
    relative_to: Optional[str] = None  # diagnosis | systemic_regimen | surgery | radiation
    window: Optional[str] = None
    sequencing_notes: Optional[str] = None


class SurgeryModality(Base):
    id: str
    disease_id: str
    indication_ids: list[str] = Field(default_factory=list)

    intent: ModalityIntent
    procedure: str
    anatomical_site: Optional[str] = None
    timing: Optional[ModalityTiming] = None

    selection_criteria: list[str] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)
    margin_or_extent_goal: Optional[str] = None
    lymph_node_management: Optional[str] = None
    perioperative_considerations: list[str] = Field(default_factory=list)
    required_tests: list[str] = Field(default_factory=list)

    source_refs: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    draft: bool = True
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)


class RadiationDose(Base):
    total_dose: Optional[str] = None
    fractions: Optional[str] = None
    dose_per_fraction: Optional[str] = None
    boost: Optional[str] = None
    notes: Optional[str] = None


class RadiationModality(Base):
    id: str
    disease_id: str
    indication_ids: list[str] = Field(default_factory=list)

    intent: ModalityIntent
    anatomical_site: str
    technique: Optional[str] = None  # EBRT | IMRT | SBRT | brachytherapy | proton | other
    dose: Optional[RadiationDose] = None
    timing: Optional[ModalityTiming] = None

    selection_criteria: list[str] = Field(default_factory=list)
    organs_at_risk: list[str] = Field(default_factory=list)
    concurrent_systemic_therapy: list[str] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)
    required_tests: list[str] = Field(default_factory=list)

    source_refs: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    draft: bool = True
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)
