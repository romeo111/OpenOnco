"""Biomarker entity — KNOWLEDGE_SCHEMA_SPECIFICATION §4."""

from typing import Literal, Optional

from pydantic import Field, model_validator

from .base import Base, NamePair


# Stable machine-readable tokens for biomarkers we deliberately exclude
# from OncoKB lookups. These strings are greppable and downstream code
# (engine/oncokb_extract.py) keys behavior off them — DO NOT rename
# without coordinating with that module.
OncoKBSkipReason = Literal[
    "ihc_no_variant",
    "score",
    "clinical_composite",
    "serological",
    "viral_load",
    "tumor_marker",
    "imaging",
    "germline_no_somatic",
    "fusion_mvp",
    "itd_mvp",
    "multi_allele_mvp",
    "tumor_agnostic",
]


class BiomarkerMeasurement(Base):
    method: Optional[str] = None  # IHC | PCR | NGS | flow_cytometry | serology
    units: Optional[str] = None
    typical_range: Optional[list[float]] = None


class MutationDetails(Base):
    gene: Optional[str] = None
    gene_hugo_id: Optional[str] = None
    exon: Optional[str] = None
    variant_type: Optional[str] = None  # missense | fusion | amplification | deletion | ...
    functional_impact: Optional[str] = None  # activating | loss_of_function | ...
    hgvs_protein: Optional[str] = None
    hgvs_coding: Optional[str] = None


class OncoKBLookupHint(Base):
    """Explicit hint to enable OncoKB lookups for this biomarker.

    Per oncokb_integration_safe_rollout_v3.md §4: variant normalization is
    conservative — biomarkers without an explicit hint are SKIPPED. This
    is intentional: silent guessing of (gene, variant) from biomarker id
    risks false negatives that clinicians wouldn't notice.

    `gene` must be the HGNC symbol (uppercase). `variant` should be the
    short HGVS-p form (e.g. "V600E", "L858R", "G12C"), a structured
    descriptor recognised by OncoKB (e.g. "Exon 19 deletion",
    "E746_A750del"), or a frameshift token (e.g. "W288fs"). Full HGVS
    validation lives in `engine/oncokb_extract.py:normalize_variant`;
    this schema only type-checks. Anything that fails normalization at
    runtime (HGVS-c, fusion, boolean flag) should not be represented
    here — leave the hint absent and use `oncokb_skip_reason` instead.
    """

    gene: str = Field(..., min_length=1, max_length=32)
    variant: str = Field(..., min_length=1, max_length=128)


class BiomarkerExternalIDs(Base):
    """Stable cross-references to external knowledge bases.

    Per oncokb_integration_safe_rollout_v3.md §4: surfacing OncoKB /
    CIViC / ClinGen records uses these IDs as canonical anchors. All
    fields are optional — a partial mapping (e.g., only `hgnc_symbol`)
    is valid for biomarkers we haven't fully classified yet.
    """

    hgnc_symbol: Optional[str] = None
    hgnc_id: Optional[str] = None
    oncokb_url: Optional[str] = None
    civic_id: Optional[str] = None
    civic_url: Optional[str] = None
    clingen_id: Optional[str] = None
    hgvs_protein: Optional[str] = None
    hgvs_coding: Optional[str] = None


class Biomarker(Base):
    id: str
    names: NamePair
    biomarker_type: Optional[str] = None
    # protein_expression_ihc | protein_serology | gene_mutation | gene_fusion |
    # copy_number | msi_status | tmb | methylation | ...

    measurement: Optional[BiomarkerMeasurement] = None
    mutation_details: Optional[MutationDetails] = None
    specimen_requirements: list[str] = Field(default_factory=list)

    # Phase 2 OncoKB integration — opt-in hint per biomarker.
    # If absent, the OncoKB extractor skips this biomarker entirely.
    oncokb_lookup: Optional[OncoKBLookupHint] = None

    # Mutually exclusive with `oncokb_lookup`: a stable machine-readable
    # token explaining WHY this biomarker is intentionally excluded from
    # OncoKB lookups (per oncokb_integration_safe_rollout_v3.md §4).
    # Zero-or-one classification per biomarker; both unset is fine for
    # biomarkers not yet triaged.
    oncokb_skip_reason: Optional[OncoKBSkipReason] = None

    # Cross-references to external KBs (HGNC, OncoKB, CIViC, ClinGen).
    # Optional and partial — see BiomarkerExternalIDs.
    external_ids: Optional[BiomarkerExternalIDs] = None

    related_biomarkers: list[str] = Field(default_factory=list)
    knowledge_base_refs: dict[str, str] = Field(default_factory=dict)  # oncokb | civic | clinvar URL
    sources: list[str] = Field(default_factory=list)

    last_reviewed: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _oncokb_lookup_xor_skip(self) -> "Biomarker":
        """`oncokb_lookup` and `oncokb_skip_reason` are mutually exclusive.

        Zero-or-one is fine — a biomarker that hasn't been triaged for
        OncoKB integration yet may have neither set. But declaring both
        is contradictory (the lookup would be requested AND deliberately
        skipped) and almost certainly an authoring error.
        """
        if self.oncokb_lookup is not None and self.oncokb_skip_reason is not None:
            raise ValueError(
                "Biomarker may set at most one of `oncokb_lookup` and "
                "`oncokb_skip_reason` — not both."
            )
        return self
