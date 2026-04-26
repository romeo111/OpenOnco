"""BiomarkerActionability entity — maps (gene-variant, tumor_type) pairs to
clinical actionability tiers per ESMO ESCAT and OncoKB standards.

Each instance answers "what does this specific variant mean for treatment in
this specific cancer?" Composes existing BIO-* (gene/variant taxonomy) and
DIS-* (disease taxonomy) entities into a per-tumor clinical interpretation.

Not in KNOWLEDGE_SCHEMA_SPECIFICATION yet (added 2026-04-26 for the CSD Lab
partnership pitch). When the spec is updated, register this entity there.
"""

from typing import Literal, Optional

from pydantic import Field

from .base import Base


# ── ESCAT (ESMO Scale for Clinical Actionability of molecular Targets) ────────
# Mateo et al. 2018, Ann Oncol 29(9):1895-1902. Tiers I–V plus X (no evidence).
EscatTier = Literal["IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X"]

# OncoKB Therapeutic Levels of Evidence v2 (Chakravarty et al. 2017,
# JCO Precis Oncol). 1, 2 = standard care. 3A/3B = clinical evidence.
# 4 = biological evidence. R1/R2 = resistance.
OncoKbLevel = Literal["1", "2", "3A", "3B", "4", "R1", "R2"]


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


class BiomarkerActionability(Base):
    """Tumor-specific clinical actionability of a biomarker variant.

    ID convention: ``BMA-{biomarker}-{variant?}-{disease}``
    e.g. ``BMA-BRAF-V600E-CRC``, ``BMA-EGFR-T790M-NSCLC``.

    The ``biomarker_id`` may already encode the variant (e.g. BIO-BRAF-V600E);
    in that case ``variant_qualifier`` may repeat or refine it (sub-variant /
    co-occurrence). Use null ``variant_qualifier`` when the cell is gene-level
    (any pathogenic alteration treated identically).

    Sources are FK strings to Source entities (SRC-*); not Citation objects,
    because actionability assignment is a single attestation per source rather
    than quote-level provenance. Use ``notes`` for nuance.
    """

    id: str  # BMA-{biomarker}-{variant?}-{disease}
    biomarker_id: str  # FK → BIO-*
    variant_qualifier: Optional[str] = None  # e.g. "V600E", "T790M"; null = gene-level
    disease_id: str  # FK → DIS-*

    escat_tier: EscatTier
    oncokb_level: OncoKbLevel

    evidence_summary: str  # 1–3 sentences clinical interpretation
    regulatory_approval: RegulatoryApproval = Field(default_factory=RegulatoryApproval)

    recommended_combinations: list[str] = Field(default_factory=list)
    contraindicated_monotherapy: list[str] = Field(default_factory=list)

    primary_sources: list[str]  # FK → SRC-*, ≥1 required (enforced by loader)
    last_verified: str  # ISO date (YYYY-MM-DD)
    oncokb_snapshot_version: Optional[str] = None  # e.g. "v3.20-2026-04"
    notes: Optional[str] = None
