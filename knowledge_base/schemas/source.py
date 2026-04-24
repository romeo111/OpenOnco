"""Source entity — merges KNOWLEDGE_SCHEMA_SPECIFICATION §14.1 and
SOURCE_INGESTION_SPEC §3 (licensing & hosting fields)."""

from typing import Optional

from pydantic import Field

from .base import (
    Attribution,
    Base,
    CachePolicy,
    CurrencyStatus,
    HostingMode,
    IngestionConfig,
    LegalReview,
    License,
)


class Source(Base):
    id: str
    source_type: str  # guideline | clinical_trial | rct_publication | molecular_kb | etc.
    title: str
    version: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    journal: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    access_level: Optional[str] = None  # open_access | subscription_required | registered_free

    currency_status: CurrencyStatus = CurrencyStatus.CURRENT
    superseded_by: Optional[str] = None
    current_as_of: Optional[str] = None

    evidence_tier: Optional[int] = None  # 1..6 per CLINICAL_CONTENT_STANDARDS

    # Licensing & hosting (SOURCE_INGESTION_SPEC §3)
    hosting_mode: HostingMode = HostingMode.REFERENCED
    hosting_justification: Optional[str] = None  # H1..H5 per SOURCE_INGESTION_SPEC §1.4
    ingestion: Optional[IngestionConfig] = None
    cache_policy: Optional[CachePolicy] = None
    license: Optional[License] = None
    attribution: Optional[Attribution] = None
    commercial_use_allowed: Optional[bool] = None
    redistribution_allowed: Optional[bool] = None
    modifications_allowed: Optional[bool] = None
    sharealike_required: bool = False
    known_restrictions: list[str] = Field(default_factory=list)
    legal_review: Optional[LegalReview] = None

    relates_to_diseases: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
    last_verified: Optional[str] = None
    verifier: Optional[str] = None
