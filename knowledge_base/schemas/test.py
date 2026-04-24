"""Test entity — KNOWLEDGE_SCHEMA_SPECIFICATION §10."""

from typing import Optional

from pydantic import Field

from .base import Base, NamePair, TestPriority


class TestAvailabilityUkraine(Base):
    state_funded: bool = False
    typical_cost_uah: Optional[float] = None
    typical_availability: Optional[str] = None  # "major centers only" | "widely" | ...
    notes: Optional[str] = None


class Test(Base):
    id: str
    names: NamePair
    loinc_codes: list[str] = Field(default_factory=list)
    category: Optional[str] = None  # lab | imaging | histology | genomic | clinical_assessment
    purpose: Optional[str] = None

    specimen: Optional[str] = None
    turnaround_time: Optional[str] = None
    priority_class: TestPriority = TestPriority.STANDARD

    availability_ukraine: Optional[TestAvailabilityUkraine] = None

    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
