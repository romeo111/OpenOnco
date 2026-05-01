"""Test entity — KNOWLEDGE_SCHEMA_SPECIFICATION §10."""

from typing import Literal, Optional

from pydantic import Field

from .base import Base, NamePair, TestPriority


class TestAvailabilityUkraine(Base):
    state_funded: bool = False
    typical_cost_uah: Optional[float] = None
    typical_availability: Optional[str] = None  # "major centers only" | "widely" | ...
    notes: Optional[str] = None


class LabAvailabilityUA(Base):
    """Where a clinician can actually order this test in Ukraine.

    Orthogonal to `availability_ukraine` (which describes state-funding /
    cost / scarcity). This block names a specific provider + their product
    code so the patient plan can render a concrete "where to get it" link
    instead of the abstract clinical-test name.
    """

    lab: str  # e.g. "CSD Lab", "Synevo", "Diala"
    product_code: Optional[str] = None  # provider's catalog code (e.g. CSD "M081", "B001")
    product_name: Optional[str] = None
    url: Optional[str] = None
    confirmation: Literal[
        "product_code_verified",  # specific code matched on provider's public catalog
        "category_verified",      # provider category exists, exact code not public
        "unconfirmed",            # asserted but not yet checked
    ] = "category_verified"
    coverage_notes: Optional[str] = None  # e.g. "RNA fusions only — DNA mutations need separate test"
    last_verified: Optional[str] = None   # ISO date of public-catalog check


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
    lab_availability_ua: list[LabAvailabilityUA] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
