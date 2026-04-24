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


class Biomarker(Base):
    id: str
    names: NamePair
    biomarker_type: Optional[str] = None
    # protein_expression_ihc | protein_serology | gene_mutation | gene_fusion |
    # copy_number | msi_status | tmb | methylation | ...

    measurement: Optional[BiomarkerMeasurement] = None
    mutation_details: Optional[MutationDetails] = None
    specimen_requirements: list[str] = Field(default_factory=list)

    related_biomarkers: list[str] = Field(default_factory=list)
    knowledge_base_refs: dict[str, str] = Field(default_factory=dict)  # oncokb | civic | clinvar URL
    sources: list[str] = Field(default_factory=list)

    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
