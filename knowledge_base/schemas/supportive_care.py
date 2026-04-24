"""SupportiveCare entity — KNOWLEDGE_SCHEMA_SPECIFICATION §11."""

from typing import Optional

from pydantic import Field

from .base import Base


class StandardIntervention(Base):
    drug_id: Optional[str] = None
    dose: Optional[str] = None
    schedule: Optional[str] = None
    notes: Optional[str] = None


class SupportiveCareTrigger(Base):
    relevant_regimens: list[str] = Field(default_factory=list)
    relevant_diseases: list[str] = Field(default_factory=list)
    lab_thresholds: list[dict] = Field(default_factory=list)
    clinical_condition: Optional[str] = None


class SupportiveCare(Base):
    id: str
    intervention_type: str  # prophylaxis | premedication | monitoring | screening | ...
    name: str
    name_ua: Optional[str] = None

    standard_intervention: Optional[StandardIntervention] = None
    alternatives: list[StandardIntervention] = Field(default_factory=list)

    triggers: Optional[SupportiveCareTrigger] = None
    rationale: Optional[str] = None

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
