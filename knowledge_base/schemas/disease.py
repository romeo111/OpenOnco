"""Disease entity — KNOWLEDGE_SCHEMA_SPECIFICATION §2."""

from typing import Optional

from pydantic import Field

from .base import Base, NamePair


class DiseaseCodes(Base):
    icd_o_3_morphology: Optional[str] = None
    icd_o_3_topography: list[str] = Field(default_factory=list)
    icd_10: Optional[str] = None
    snomed_ct: Optional[str] = None  # only populated if country license acquired
    who_classification: Optional[str] = None


class Disease(Base):
    id: str
    names: NamePair
    codes: DiseaseCodes

    archetype: Optional[str] = None  # etiologically_driven | biomarker_driven | ...
    lineage: Optional[str] = None  # b_cell_lymphoma | carcinoma | sarcoma | ...

    etiological_factors: list[str] = Field(default_factory=list)
    related_diseases: list[str] = Field(default_factory=list)

    epidemiology: Optional[dict] = None  # free-form notes from curator
    sources: list[str] = Field(default_factory=list)

    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
