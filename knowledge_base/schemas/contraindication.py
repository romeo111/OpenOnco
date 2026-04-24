"""Contraindication entity — KNOWLEDGE_SCHEMA_SPECIFICATION §8."""

from typing import Optional

from pydantic import Field

from .base import Base, ContraindicationSeverity


class ContraindicationTrigger(Base):
    """Semi-structured trigger per KNOWLEDGE_SCHEMA §8.2."""

    type: str  # drug_drug_interaction | patient_condition | lab_value | pregnancy | age | ...
    conditions: list[dict] = Field(default_factory=list)  # free-form for now
    logic: Optional[str] = "AND"  # AND | OR


class Contraindication(Base):
    id: str
    severity: ContraindicationSeverity
    trigger: ContraindicationTrigger

    description: Optional[str] = None
    description_ua: Optional[str] = None

    alternative_actions: list[str] = Field(default_factory=list)
    affects_indications: list[str] = Field(default_factory=list)  # Indication IDs
    affects_drugs: list[str] = Field(default_factory=list)
    affects_regimens: list[str] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
