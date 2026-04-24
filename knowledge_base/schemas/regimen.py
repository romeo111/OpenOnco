"""Regimen entity — KNOWLEDGE_SCHEMA_SPECIFICATION §6."""

from typing import Optional

from pydantic import Field

from .base import Base, UkraineRegistration


class RegimenComponent(Base):
    drug_id: str
    dose: Optional[str] = None  # "375 mg/m² IV"
    schedule: Optional[str] = None  # "day 1 of every 28-day cycle"
    route: Optional[str] = None  # IV | PO | SC
    duration: Optional[str] = None


class DoseAdjustment(Base):
    condition: str  # e.g. "FIB-4 > 3.25 OR cirrhosis"
    modification: str  # e.g. "Reduce bendamustine to 70 mg/m²"
    rationale: Optional[str] = None
    source_refs: list[str] = Field(default_factory=list)


class RegimenUkraineAvailability(Base):
    all_components_registered: bool = False
    all_components_reimbursed: bool = False
    per_component: dict[str, UkraineRegistration] = Field(default_factory=dict)
    notes: Optional[str] = None


class Regimen(Base):
    id: str
    name: str
    name_ua: Optional[str] = None
    alternate_names: list[str] = Field(default_factory=list)

    components: list[RegimenComponent]
    cycle_length_days: Optional[int] = None
    total_cycles: Optional[str] = None  # "6", "6-8", "until progression"

    toxicity_profile: Optional[str] = None  # none | low | moderate | severe | variable

    premedication: list[str] = Field(default_factory=list)
    mandatory_supportive_care: list[str] = Field(default_factory=list)  # SupportiveCare IDs
    monitoring_schedule_id: Optional[str] = None

    dose_adjustments: list[DoseAdjustment] = Field(default_factory=list)

    ukraine_availability: Optional[RegimenUkraineAvailability] = None

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
