"""Shared enums and common types for OpenOnco knowledge-base entities.

Aligned with specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md and
specs/SOURCE_INGESTION_SPEC.md §3.
"""

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ── Enums ─────────────────────────────────────────────────────────────────────


class HostingMode(str, Enum):
    HOSTED = "hosted"
    REFERENCED = "referenced"
    MIXED = "mixed"


class IngestionMethod(str, Enum):
    LIVE_API = "live_api"
    SCHEDULED_BATCH = "scheduled_batch"
    MANUAL = "manual"
    NONE = "none"


class CurrencyStatus(str, Enum):
    CURRENT = "current"
    SUPERSEDED = "superseded"
    HISTORICAL = "historical"


class LegalReviewStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ESCALATED = "escalated"


class EvidenceLevel(str, Enum):
    """GRADE levels (CLINICAL_CONTENT_STANDARDS §4.1)."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"


class StrengthOfRecommendation(str, Enum):
    """GRADE strength."""

    STRONG = "strong"
    CONDITIONAL = "conditional"


class ContraindicationSeverity(str, Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    CAUTION = "caution"


class TestPriority(str, Enum):
    CRITICAL = "critical"
    STANDARD = "standard"
    DESIRED = "desired"
    CALCULATION_BASED = "calculation_based"


class RedFlagDirection(str, Enum):
    INTENSIFY = "intensify"
    DE_ESCALATE = "de-escalate"
    HOLD = "hold"
    INVESTIGATE = "investigate"


class RedFlagSeverity(str, Enum):
    """Severity tier for conflict-resolution when multiple RedFlags fire.

    Resolution order (engine): clinical_direction precedence
    (hold > intensify > de_escalate > investigate) THEN severity
    (critical > major > minor) THEN explicit numeric priority.
    """

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class RedFlagCategory(str, Enum):
    """5-type matrix from REDFLAG_AUTHORING_GUIDE §2 plus an `other` bucket.

    Used by coverage tooling and downstream UI grouping. Authored on the
    RedFlag itself so we don't have to rely on filename/keyword heuristics.
    """

    ORGAN_DYSFUNCTION = "organ-dysfunction"
    INFECTION_SCREENING = "infection-screening"
    HIGH_RISK_BIOLOGY = "high-risk-biology"
    TRANSFORMATION_PROGRESSION = "transformation-progression"
    FRAILTY_AGE = "frailty-age"
    OTHER = "other"


# ── Common embedded models ────────────────────────────────────────────────────


class Base(BaseModel):
    """Common config for all entities — forgiving to YAML schema evolution."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class License(Base):
    name: str = Field(..., description="Canonical license name")
    url: Optional[str] = None
    spdx_id: Optional[str] = None


class Attribution(Base):
    required: bool = False
    text: Optional[str] = None
    logo_url: Optional[str] = None


class LegalReview(Base):
    status: LegalReviewStatus = LegalReviewStatus.PENDING
    reviewer: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None


class IngestionConfig(Base):
    method: IngestionMethod
    client: Optional[str] = None
    endpoint: Optional[str] = None
    rate_limit: Optional[str] = None


class CachePolicy(Base):
    enabled: bool = False
    ttl_hours: Optional[int] = None
    scope: Optional[Literal["query_result", "entity_snapshot", "none"]] = None


class Citation(Base):
    """Reference from any entity back to a Source."""

    source_id: str
    page: Optional[int] = None
    section: Optional[str] = None
    quote_paraphrase: Optional[str] = None
    relevant_quote_paraphrase: Optional[str] = None  # alias used in some YAMLs
    position: Optional[Literal["supports", "contradicts", "context"]] = None


class UkraineRegistration(Base):
    """Reused across Drug and Regimen per KNOWLEDGE_SCHEMA_SPECIFICATION §5.1 / §6.1."""

    registered: bool = False
    registration_number: Optional[str] = None
    reimbursed_nszu: bool = False
    reimbursement_indications: list[str] = Field(default_factory=list)
    typical_cost_per_cycle_uah: Optional[float] = None
    last_verified: Optional[str] = None
    notes: Optional[str] = None


class RegulatoryStatus(Base):
    """FDA / EMA / Ukraine regulatory info bundled on Drug."""

    fda: Optional[dict] = None  # {approved: bool, indications: [...], etc.}
    ema: Optional[dict] = None
    ukraine_registration: Optional[UkraineRegistration] = None


class NamePair(Base):
    """Preferred + Ukrainian + synonyms."""

    preferred: str
    ukrainian: Optional[str] = None
    english: Optional[str] = None
    synonyms: list[str] = Field(default_factory=list)
    brand_names: list[str] = Field(default_factory=list)


__all__ = [
    "Base",
    "HostingMode",
    "IngestionMethod",
    "CurrencyStatus",
    "LegalReviewStatus",
    "EvidenceLevel",
    "StrengthOfRecommendation",
    "ContraindicationSeverity",
    "TestPriority",
    "RedFlagDirection",
    "RedFlagSeverity",
    "RedFlagCategory",
    "License",
    "Attribution",
    "LegalReview",
    "IngestionConfig",
    "CachePolicy",
    "Citation",
    "UkraineRegistration",
    "RegulatoryStatus",
    "NamePair",
]
