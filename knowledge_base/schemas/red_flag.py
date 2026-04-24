"""RedFlag entity — KNOWLEDGE_SCHEMA_SPECIFICATION §9."""

from typing import Optional

from pydantic import Field

from .base import Base, RedFlagDirection


class RedFlagTrigger(Base):
    type: str  # symptom_composite | lab_value | imaging_finding | biomarker_threshold | ...
    all_of: list[dict] = Field(default_factory=list)
    any_of: list[dict] = Field(default_factory=list)
    none_of: list[dict] = Field(default_factory=list)


class RedFlag(Base):
    id: str
    definition: str
    definition_ua: Optional[str] = None

    trigger: RedFlagTrigger
    clinical_direction: RedFlagDirection

    relevant_diseases: list[str] = Field(default_factory=list)
    shifts_algorithm: list[str] = Field(default_factory=list)  # Algorithm IDs affected

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
