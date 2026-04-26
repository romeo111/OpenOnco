"""Biomarker entity — KNOWLEDGE_SCHEMA_SPECIFICATION §4."""

from typing import Optional

from pydantic import Field

from .base import Base, NamePair


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
    short HGVS-p form (e.g. "V600E", "L858R", "G12C") or a structured
    descriptor recognised by OncoKB (e.g. "Exon 19 deletion"). Anything
    that fails normalization (HGVS-c, fusion, boolean flag) MUST NOT be
    represented here — leave the hint absent and add a `notes` line.
    """

    gene: str = Field(..., min_length=1, max_length=32)
    variant: str = Field(..., min_length=1, max_length=128)


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

    related_biomarkers: list[str] = Field(default_factory=list)
    knowledge_base_refs: dict[str, str] = Field(default_factory=dict)  # oncokb | civic | clinvar URL
    sources: list[str] = Field(default_factory=list)

    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
