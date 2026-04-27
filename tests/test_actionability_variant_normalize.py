"""Variant normalization corpus — Phase 3a of OncoKB safe-rollout v3.

Per safe-rollout v3 §4: variant normalization MUST be conservative.
A skip is recoverable (clinician consults OncoKB manually); a wrong
canonicalization is not (clinician receives wrong evidence silently).

These tests pin the contract. If you change the canonical OUTPUT_FORMAT
(e.g. after Phase 0 A6 verification reveals OncoKB prefers "p.V600E"),
update the expected outputs here together with engine/oncokb_extract.py.
"""

from __future__ import annotations

import pytest

from knowledge_base.engine.oncokb_extract import (
    extract_oncokb_queries,
    normalize_variant,
)
from knowledge_base.engine.oncokb_types import NormalizedVariant


# ── Canonical short HGVS-p (the most common form) ────────────────────────


@pytest.mark.parametrize(
    "raw,gene,expected_query",
    [
        ("V600E", "BRAF", "V600E"),
        ("L858R", "EGFR", "L858R"),
        ("T790M", "EGFR", "T790M"),
        ("G12C", "KRAS", "G12C"),
        ("G12D", "KRAS", "G12D"),
        ("G12V", "KRAS", "G12V"),
        ("Q61H", "NRAS", "Q61H"),
        ("R175H", "TP53", "R175H"),
        ("L265P", "MYD88", "L265P"),
        ("F1174L", "ALK", "F1174L"),
        ("D816V", "KIT", "D816V"),
        ("E545K", "PIK3CA", "E545K"),
    ],
)
def test_short_hgvs_p_passes_through(raw: str, gene: str, expected_query: str):
    nv = normalize_variant(raw, gene)
    assert nv is not None
    assert nv.gene == gene.upper()
    assert nv.oncokb_query_string == expected_query
    assert nv.raw == raw


# ── HGVS-p with "p." prefix — strip prefix, keep short form ──────────────


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("p.V600E", "V600E"),
        ("p.L858R", "L858R"),
        ("p.G12C", "G12C"),
    ],
)
def test_short_hgvs_p_with_prefix_strips_prefix(raw: str, expected: str):
    nv = normalize_variant(raw, "BRAF")
    assert nv is not None
    assert nv.oncokb_query_string == expected


# ── 3-letter HGVS-p → short form ──────────────────────────────────────────


@pytest.mark.parametrize(
    "raw,gene,expected",
    [
        ("p.Val600Glu", "BRAF", "V600E"),
        ("Val600Glu", "BRAF", "V600E"),
        ("p.Leu858Arg", "EGFR", "L858R"),
        ("p.Thr790Met", "EGFR", "T790M"),
        ("p.Gly12Cys", "KRAS", "G12C"),
        ("p.Arg175His", "TP53", "R175H"),
        ("p.Trp288Ter", "NPM1", "W288*"),
    ],
)
def test_three_letter_hgvs_p_normalizes_to_short(raw: str, gene: str, expected: str):
    nv = normalize_variant(raw, gene)
    assert nv is not None
    assert nv.oncokb_query_string == expected


# ── Exon-level descriptors (whitelist) ──────────────────────────────────


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Exon 19 deletion", "Exon 19 deletion"),
        ("exon 19 deletion", "Exon 19 deletion"),
        ("EX19DEL", "Exon 19 deletion"),
        ("Exon 19 del", "Exon 19 deletion"),
        ("Exon 20 insertion", "Exon 20 insertion"),
        ("EX20INS", "Exon 20 insertion"),
    ],
)
def test_exon_descriptors_canonicalize(raw: str, expected: str):
    nv = normalize_variant(raw, "EGFR")
    assert nv is not None
    assert nv.oncokb_query_string == expected


# ── Structured exon deletions (E746_A750del style) ──────────────────────


def test_structured_exon_deletion_passes_through():
    nv = normalize_variant("E746_A750del", "EGFR")
    assert nv is not None
    assert nv.oncokb_query_string == "E746_A750del"


def test_structured_exon_deletion_with_del_prefix():
    nv = normalize_variant("del E746_A750", "EGFR")
    assert nv is not None
    assert nv.oncokb_query_string == "E746_A750del"


# ── Frameshift ──────────────────────────────────────────────────────────


def test_frameshift_passes_through():
    nv = normalize_variant("W288fs", "NPM1")
    assert nv is not None
    assert nv.oncokb_query_string == "W288fs"


def test_frameshift_with_termination_count():
    nv = normalize_variant("W288fs*12", "NPM1")
    assert nv is not None
    assert nv.oncokb_query_string == "W288fs*12"


# ── Skips (must return None) ────────────────────────────────────────────


@pytest.mark.parametrize(
    "raw,gene,reason",
    [
        # Boolean / generic flags — no specific variant
        ("true", "TP53", "boolean flag"),
        ("positive", "MSI", "boolean flag"),
        ("negative", "PD-L1", "boolean flag"),
        # HGVS-c — never guess transcript mapping
        ("c.1799T>A", "BRAF", "HGVS-c without transcript"),
        ("c.5266dupC", "BRCA1", "HGVS-c"),
        # Fusions — out of MVP scope
        ("EML4-ALK", "ALK", "fusion"),
        ("BCR-ABL1", "ABL1", "fusion"),
        # ITDs — out of MVP scope
        ("FLT3-ITD", "FLT3", "ITD"),
        ("internal tandem duplication", "FLT3", "ITD spelled out"),
        # Garbage / unrecognised
        ("???", "BRAF", "garbage"),
        ("amplification", "HER2", "copy-number descriptor — separate endpoint"),
        ("", "BRAF", "empty"),
    ],
)
def test_unsafe_variants_return_none(raw: str, gene: str, reason: str):
    assert normalize_variant(raw, gene) is None, f"should skip ({reason})"


def test_empty_gene_returns_none():
    assert normalize_variant("V600E", "") is None
    assert normalize_variant("V600E", "   ") is None


def test_unknown_amino_acid_token_returns_none():
    # "Xyz" is not a valid AA code — must skip, not guess
    assert normalize_variant("p.Xyz600Glu", "BRAF") is None


# ── Idempotency / determinism (property-based-style) ────────────────────


@pytest.mark.parametrize(
    "raw,gene",
    [
        ("V600E", "BRAF"),
        ("p.Val600Glu", "BRAF"),
        ("Exon 19 deletion", "EGFR"),
        ("E746_A750del", "EGFR"),
        ("W288fs", "NPM1"),
    ],
)
def test_normalization_is_idempotent(raw: str, gene: str):
    """normalize(raw) → nv1 → normalize(nv1.oncokb_query_string) → nv2
    where nv2.oncokb_query_string == nv1.oncokb_query_string."""
    nv1 = normalize_variant(raw, gene)
    assert nv1 is not None
    nv2 = normalize_variant(nv1.oncokb_query_string, gene)
    assert nv2 is not None
    assert nv2.oncokb_query_string == nv1.oncokb_query_string


# ── Gene casing ──────────────────────────────────────────────────────────


def test_gene_is_uppercased():
    nv = normalize_variant("V600E", "braf")
    assert nv is not None
    assert nv.gene == "BRAF"


# ── extract_oncokb_queries (composer) ────────────────────────────────────


def test_extract_dedupes_same_canonical_form():
    """Two biomarker hints that normalize to the same (gene, variant)
    should produce one OncoKBQuery, not two."""
    hints = [
        ("BIO-BRAF-1", "BRAF", "V600E"),
        ("BIO-BRAF-2", "BRAF", "p.Val600Glu"),  # same after normalization
    ]
    queries = extract_oncokb_queries(hints, oncotree_code="MEL")
    assert len(queries) == 1
    assert queries[0].variant == "V600E"


def test_extract_skips_unsafe_silently():
    hints = [
        ("BIO-BRAF", "BRAF", "V600E"),
        ("BIO-BRCA-bool", "BRCA1", "true"),  # skip
        ("BIO-ALK-fusion", "ALK", "EML4-ALK"),  # skip
        ("BIO-EGFR", "EGFR", "L858R"),
    ]
    queries = extract_oncokb_queries(hints, oncotree_code="NSCLC")
    assert len(queries) == 2
    assert {q.gene for q in queries} == {"BRAF", "EGFR"}


def test_extract_deterministic_order():
    """Sorted by (gene_upper, biomarker_id) for stable provenance."""
    hints = [
        ("BIO-Z", "EGFR", "L858R"),
        ("BIO-A", "BRAF", "V600E"),
        ("BIO-M", "KRAS", "G12C"),
    ]
    queries = extract_oncokb_queries(hints, oncotree_code="NSCLC")
    assert [q.gene for q in queries] == ["BRAF", "EGFR", "KRAS"]


def test_extract_with_no_oncotree_code_emits_pan_tumor_query():
    """oncotree_code=None is valid (Q4 pan-tumor fallback). The query
    still goes; render layer adds warning badge."""
    hints = [("BIO-TP53", "TP53", "R175H")]
    queries = extract_oncokb_queries(hints, oncotree_code=None)
    assert len(queries) == 1
    assert queries[0].oncotree_code is None


def test_extract_preserves_biomarker_id_for_provenance():
    hints = [("BIO-BRAF-V600E-NSCLC", "BRAF", "V600E")]
    queries = extract_oncokb_queries(hints, oncotree_code="LUNG")
    assert queries[0].source_biomarker_id == "BIO-BRAF-V600E-NSCLC"


def test_extract_empty_input_returns_empty_list():
    assert extract_oncokb_queries([]) == []


# ── Negative regression — never accidentally accept HGVS-c ──────────────


@pytest.mark.parametrize(
    "raw",
    [
        "c.1799T>A",
        "c.5266dupC",
        "c.5266_5267insTGAAA",
        "c.1A>G",
    ],
)
def test_hgvs_c_always_skipped(raw: str):
    """Critical: HGVS-c without transcript is unsafe — assert always-None."""
    assert normalize_variant(raw, "BRCA1") is None


# ── NormalizedVariant is hashable + frozen ──────────────────────────────


def test_normalized_variant_is_hashable():
    nv = normalize_variant("V600E", "BRAF")
    assert nv is not None
    # Must be usable as dict key (frozen=True)
    d = {nv: "test"}
    assert d[nv] == "test"


def test_normalized_variant_is_frozen():
    nv = normalize_variant("V600E", "BRAF")
    assert nv is not None
    with pytest.raises((AttributeError, Exception)):
        nv.gene = "OTHER"  # type: ignore[misc]
