"""BiomarkerActionability entity — maps (gene-variant, tumor_type) pairs to
clinical actionability tiers, anchored on ESMO ESCAT.

Each instance answers "what does this specific variant mean for treatment in
this specific cancer?" Composes existing BIO-* (gene/variant taxonomy) and
DIS-* (disease taxonomy) entities into a per-tumor clinical interpretation.

Phase 1 of the CIViC pivot (2026-04-27): the OncoKB-specific fields
`oncokb_level` and `oncokb_snapshot_version` were dropped — see
docs/reviews/oncokb-public-civic-coverage-2026-04-27.md for the ToS
audit that triggered the pivot. Per-source level information now lives
in the `evidence_sources` list, where each entry references a Source
entity (SRC-*) and carries the source-native level token.

ESCAT remains the primary actionability tier (`escat_tier`) because it
is open-license and source-neutral. CIViC, OncoKB, NCCN page-section
references, ESMO sections, etc. all become entries inside
`evidence_sources`.

Not in KNOWLEDGE_SCHEMA_SPECIFICATION yet (added 2026-04-26 for the CSD Lab
partnership pitch). When the spec is updated, register this entity there.
"""

from typing import Literal, Optional

from pydantic import Field, field_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base


# ── ESCAT (ESMO Scale for Clinical Actionability of molecular Targets) ────────
# Mateo et al. 2018, Ann Oncol 29(9):1895-1902. Tiers I–V plus X (no evidence).
EscatTier = Literal["IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X"]
EvidenceLaneToken = Literal[
    "standard_care",
    "molecular_evidence_option",
    "resistance_or_avoidance_signal",
    "trial_research_option",
    "insufficient_evidence",
]


class RegulatoryApproval(Base):
    """Per-jurisdiction approval strings for regimens tied to this actionability cell.

    Free-form short strings (e.g. "encorafenib + cetuximab — mCRC 2L+ (FDA approved 2020)").
    Not a structured FK to Drug/Regimen because the same actionability cell often
    spans multiple regimens authorized at different times in different jurisdictions;
    structured links live on the Regimen.regulatory_status entity itself.
    """

    fda: list[str] = Field(default_factory=list)
    ema: list[str] = Field(default_factory=list)
    ukraine: list[str] = Field(default_factory=list)


class EvidenceSourceRef(Base):
    """Per-source actionability evidence reference.

    One BMA cell typically has 1–N entries here, one per source that
    independently attests the actionability claim. Source-native
    vocabulary is preserved verbatim (e.g. CIViC level "A" is stored as
    "A", not coerced to OncoKB "1"). The render layer iterates these
    entries and presents each with a link to the source where available.

    Fields:
        source: SRC-* ID, FK → Source entity (e.g. "SRC-CIVIC",
            "SRC-NCCN-NSCLC-V3-2026", "SRC-ESMO-CRC-2023").
        level: source-native level token. Examples: CIViC "A"/"B"/"C"/"D"/"E",
            NCCN "Category 1"/"Category 2A", OncoKB "1"/"2"/"3A" (legacy
            data only — not authored going forward).
        evidence_ids: source-internal evidence identifiers (e.g. CIViC
            evidence_id like "EID12345", NCCN page-section locator,
            PubMed-only references). Free-form list of strings.
        direction: CIViC-style "supports" | "does_not_support" | None. Other
            sources may leave this null. Generalizable: any source that
            distinguishes confirming vs. refuting evidence can use these
            tokens.
        significance: CIViC-style fine-grained label
            ("sensitivity"/"resistance"/"reduced_sensitivity"/etc.). Other
            sources may leave it null.
        evidence_lane: OpenOnco display lane for separating guideline-backed
            care, molecular options, resistance signals, and research-only
            evidence without collapsing all CIViC rows into standard care.
        note: free-form short clinical note (e.g. "FDA-CDx for osimertinib").
    """

    source: str  # FK → Source entity (SRC-*)
    level: str
    evidence_ids: list[str] = Field(default_factory=list)
    direction: Optional[str] = None  # "supports" | "does_not_support" | None
    significance: Optional[str] = None  # CIViC-specific significance label
    evidence_lane: Optional[EvidenceLaneToken] = None
    note: Optional[str] = None


class BiomarkerActionability(Base):
    """Tumor-specific clinical actionability of a biomarker variant.

    ID convention: ``BMA-{biomarker}-{variant?}-{disease}``
    e.g. ``BMA-BRAF-V600E-CRC``, ``BMA-EGFR-T790M-NSCLC``.

    The ``biomarker_id`` may already encode the variant (e.g. BIO-BRAF-V600E);
    in that case ``variant_qualifier`` may repeat or refine it (sub-variant /
    co-occurrence). Use null ``variant_qualifier`` when the cell is gene-level
    (any pathogenic alteration treated identically).

    Sources: each cell carries a primary `evidence_sources` list (per-source
    leveled attestations) plus a `primary_sources` list (FK strings to Source
    entities used for general citation). Both are required to be non-empty
    in active production data; the loader enforces ≥1 entry on
    `primary_sources`. Phase 1.5 migration populates `evidence_sources` from
    legacy `oncokb_level` claims plus existing `primary_sources`.

    `escat_tier` is the **primary** actionability tier — source-neutral,
    open-license, and stable. Per-source levels live in
    `evidence_sources[*].level`.
    """

    id: str  # BMA-{biomarker}-{variant?}-{disease}
    biomarker_id: str  # FK → BIO-*
    variant_qualifier: Optional[str] = None  # e.g. "V600E", "T790M"; null = gene-level
    disease_id: str  # FK → DIS-*

    # Primary actionability tier — source-neutral, open-license.
    escat_tier: EscatTier

    # Per-source attestations (CIViC level + direction + significance,
    # NCCN page-section, OncoKB legacy, etc.). Populated by Phase 1.5
    # migration from legacy `oncokb_level` claims; default empty for
    # back-compat with un-migrated YAML loads (loader will surface a
    # warning when this list is empty in Phase 2).
    evidence_sources: list[EvidenceSourceRef] = Field(default_factory=list)

    # Phase 1.5 sets this where a BMA's `escat_tier` / drug claims could
    # not be migrated mechanically and need a clinical co-lead to
    # re-verify (e.g. JAK2 V617F where the legacy `oncokb_level: "1"`
    # claim diverges from CIViC + oncokb-datahub gene-level evidence).
    actionability_review_required: bool = False

    evidence_summary: str  # 1–3 sentences clinical interpretation
    regulatory_approval: RegulatoryApproval = Field(default_factory=RegulatoryApproval)

    recommended_combinations: list[str] = Field(default_factory=list)
    contraindicated_monotherapy: list[str] = Field(default_factory=list)

    primary_sources: list[str]  # FK → SRC-*, ≥1 required (enforced by loader)
    last_verified: str  # ISO date (YYYY-MM-DD)
    # CHARTER §6.1: ≥2 sign-offs to publish. Structured form — legacy
    # `reviewer_signoffs: 0` (int) coerced to [] by the validator below.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)
