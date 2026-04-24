"""Drug entity — KNOWLEDGE_SCHEMA_SPECIFICATION §5."""

from typing import Optional

from pydantic import Field

from .base import Base, NamePair, RegulatoryStatus


class Drug(Base):
    id: str
    names: NamePair
    atc_code: Optional[str] = None
    rxnorm_id: Optional[str] = None
    drug_class: Optional[str] = None  # e.g. "anti-CD20 monoclonal antibody"
    mechanism: Optional[str] = None

    regulatory_status: Optional[RegulatoryStatus] = None

    typical_dosing: Optional[str] = None
    formulations: list[str] = Field(default_factory=list)

    absolute_contraindications: list[str] = Field(default_factory=list)
    black_box_warnings: list[str] = Field(default_factory=list)
    major_interactions: list[str] = Field(default_factory=list)
    common_adverse_events: list[str] = Field(default_factory=list)
    serious_adverse_events: list[str] = Field(default_factory=list)

    pharmacology: Optional[dict] = None  # half-life, clearance, etc.

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
