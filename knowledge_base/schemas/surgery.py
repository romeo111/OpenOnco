"""Surgery entity — KNOWLEDGE_SCHEMA_SPECIFICATION §17 (RATIFIED 2026-05-07).

Solid-tumor surgical procedure as a first-class treatment modality.
Whipple, esophagectomy, gastrectomy, hepatectomy / transplant, low-anterior
resection, etc. — referenced from `IndicationPhase.surgery_id` to model
neoadjuvant → surgery → adjuvant sequencing inside a single line of therapy.

See `docs/plans/schema_17_refactor_2026-05-07.md` for the full rationale.
First Surgery YAMLs land in Phase C of the GI-2 wave (FLOT periop, CROSS
phasing, Whipple-aware PDAC indications).
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import Base, NamePair


class SurgeryIntent(str, Enum):
    """Surgical intent vocabulary — distinct from RadiationIntent because
    surgical and radiation oncology classify intent differently in practice
    (planning doc §2.3)."""

    CURATIVE = "curative"
    PALLIATIVE = "palliative"
    DIAGNOSTIC = "diagnostic"
    SALVAGE = "salvage"


class SurgeryComplication(Base):
    """One known complication of a Surgery, with frequency annotation.

    `frequency` is intentionally free-string ("10-20%", "1-3% in high-volume
    centers", "rare") rather than a structured percentage, mirroring the
    §17.1 sketch and matching how clinical literature actually reports
    these figures.
    """

    name: str
    frequency: Optional[str] = None


class Surgery(Base):
    """Surgical procedure entity — §17.1 ratified 2026-05-07.

    Files live at `knowledge_base/hosted/content/procedures/proc_*.yaml`.
    `applicable_diseases` IDs must resolve to Disease entities (loader
    enforces ref-integrity per planning doc §2.4 rule 5).
    """

    id: str
    names: NamePair

    # Free-string per §17.1 sketch (e.g. "pancreaticoduodenectomy",
    # "low_anterior_resection", "right_hemicolectomy"). Keeping un-enum'd
    # in v0.1 — surgical taxonomy is broad and curator vocabulary will
    # stabilize after the first ~10 procedures land.
    type: Optional[str] = None
    intent: SurgeryIntent

    target_organ: Optional[str] = None  # e.g. "pancreas_head", "stomach", "esophagus"
    applicable_diseases: list[str] = Field(default_factory=list)  # Disease IDs

    operative_mortality_pct: Optional[str] = None  # free-string e.g. "1-3% in high-volume centers"
    common_complications: list[SurgeryComplication] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
