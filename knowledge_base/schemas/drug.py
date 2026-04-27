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

    # Patient-mode lay-language blurb (1-2 sentences, Ukrainian, friendly
    # tone). Read by `engine.render._render_drugs_plain` when present;
    # otherwise the renderer falls back to the drug_class vocabulary entry
    # in `engine._patient_vocabulary.DRUG_CLASS_PLAIN_UA` and finally to a
    # generic placeholder. NEVER consulted as a treatment-selection signal
    # (CHARTER §8.3 invariant — render-time only).
    notes_patient: Optional[str] = None
