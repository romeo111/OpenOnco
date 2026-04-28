"""Unit tests for SnapshotCIViCClient.

Uses a hand-crafted ~10-item fixture under
``tests/fixtures/civic_subset_for_testing.yaml`` so these tests don't depend
on the production snapshot moving under their feet. End-to-end sanity vs the
real snapshot lives in the commit-message report and the Phase-2 smoke test.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from knowledge_base.engine.actionability_types import (
    ActionabilityQuery,
    ActionabilityResult,
)
from knowledge_base.engine.snapshot_civic_client import (
    CIVIC_RESISTANCE_DIRECTIONS,
    CIVIC_SURFACED_LEVELS,
    SnapshotCIViCClient,
)


FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "civic_subset_for_testing.yaml"
)


@pytest.fixture(scope="module")
def client() -> SnapshotCIViCClient:
    return SnapshotCIViCClient(FIXTURE_PATH)


def _q(gene: str, variant: str, biomarker_id: str = "BIO-TEST") -> ActionabilityQuery:
    return ActionabilityQuery(
        gene=gene,
        variant=variant,
        oncotree_code=None,
        source_biomarker_id=biomarker_id,
    )


# ── Surfacing-policy constants (test #5) ─────────────────────────────────


def test_surfaced_levels_constant_is_correct():
    assert CIVIC_SURFACED_LEVELS == frozenset({"A", "B", "C", "D"})
    assert "E" not in CIVIC_SURFACED_LEVELS


def test_resistance_directions_constant_is_correct():
    assert CIVIC_RESISTANCE_DIRECTIONS == frozenset({"Does Not Support"})


# ── Test #1: BRAF V600E returns evidence ─────────────────────────────────


def test_braf_v600e_returns_evidence(client: SnapshotCIViCClient):
    result = client.lookup(_q("BRAF", "V600E"))
    assert isinstance(result, ActionabilityResult)
    assert not result.is_negative
    drugs = {d for opt in result.therapeutic_options for d in opt.drugs}
    assert "Vemurafenib" in drugs
    assert "Dabrafenib" in drugs
    assert "Trametinib" in drugs


# ── Test #2: unknown gene → empty (negative) result, NOT error ───────────


def test_unknown_gene_returns_empty_result(client: SnapshotCIViCClient):
    result = client.lookup(_q("ZZZ_FAKE_GENE", "V600E"))
    assert isinstance(result, ActionabilityResult)
    assert result.is_negative
    assert result.therapeutic_options == ()


# ── Test #3: known gene + unknown variant → empty result ─────────────────


def test_known_gene_unknown_variant_returns_empty_result(
    client: SnapshotCIViCClient,
):
    result = client.lookup(_q("BRAF", "V601Q"))
    assert isinstance(result, ActionabilityResult)
    assert result.is_negative


# ── Test #4: fusion-aware (ABL1, T315I) hits BCR::ABL1 ───────────────────


def test_fusion_aware_abl1_t315i_matches_bcr_abl1(client: SnapshotCIViCClient):
    """Confirms Agent L's matcher is wired into lookup."""
    result = client.lookup(_q("ABL1", "T315I"))
    assert isinstance(result, ActionabilityResult)
    assert not result.is_negative
    drugs = {d for opt in result.therapeutic_options for d in opt.drugs}
    assert "Ponatinib" in drugs


def test_fusion_aware_alk_g1202r_matches_eml4_alk(client: SnapshotCIViCClient):
    result = client.lookup(_q("ALK", "G1202R"))
    assert isinstance(result, ActionabilityResult)
    assert not result.is_negative
    drugs = {d for opt in result.therapeutic_options for d in opt.drugs}
    assert "Lorlatinib" in drugs


# ── Test #5: level E is INCLUDED in the result (filtering = render's job) ─


def test_level_e_is_returned_by_client(client: SnapshotCIViCClient):
    """Caller (render layer) is responsible for surfacing filter; the client
    returns everything that matches so resistance flagging at any level
    works."""
    result = client.lookup(_q("BRAF", "V600K"))
    assert isinstance(result, ActionabilityResult)
    levels = {opt.level for opt in result.therapeutic_options}
    assert "E" in levels


# ── Test #6: "Does Not Support" preserved in description ─────────────────


def test_does_not_support_preserved_in_description(client: SnapshotCIViCClient):
    result = client.lookup(_q("KRAS", "G12C"))
    assert not result.is_negative
    descriptions = [opt.description or "" for opt in result.therapeutic_options]
    assert any("Does Not Support" in d for d in descriptions), (
        f"Expected 'Does Not Support' in one of {descriptions}"
    )


# ── Test #7: multiple evidence items collapse into option list ───────────


def test_multiple_evidence_items_collapse_correctly(client: SnapshotCIViCClient):
    """BRAF V600E has two evidence items in the fixture (F1 vemurafenib +
    F2 dabrafenib/trametinib). They should appear as two distinct options,
    each with its own (level, drugs, description) tuple."""
    result = client.lookup(_q("BRAF", "V600E"))
    # F1 + F2 = 2 options; F6 (V600K) excluded.
    assert len(result.therapeutic_options) == 2
    levels = [opt.level for opt in result.therapeutic_options]
    assert levels == ["A", "A"]
    drug_sets = {opt.drugs for opt in result.therapeutic_options}
    assert ("Vemurafenib",) in drug_sets
    assert ("Dabrafenib", "Trametinib") in drug_sets


# ── Test #8: batch_lookup preserves order ────────────────────────────────


def test_batch_lookup_preserves_order(client: SnapshotCIViCClient):
    queries = [
        _q("BRAF", "V600E", "BIO-1"),
        _q("ZZZ_FAKE", "X", "BIO-2"),
        _q("EGFR", "T790M", "BIO-3"),
        _q("ABL1", "T315I", "BIO-4"),
    ]
    results = client.batch_lookup(queries)
    assert len(results) == 4
    biomarker_ids = [r.query.source_biomarker_id for r in results]
    assert biomarker_ids == ["BIO-1", "BIO-2", "BIO-3", "BIO-4"]


# ── Test #9: snapshot version reported in result ─────────────────────────


def test_snapshot_version_reported(client: SnapshotCIViCClient):
    result = client.lookup(_q("BRAF", "V600E"))
    assert result.data_version == "2026-04-25-fixture"
    assert result.cached is True


# ── Test #10: empty-therapies entries don't produce options ──────────────


def test_empty_therapies_entries_filtered(client: SnapshotCIViCClient):
    """JAK2 V617F in the fixture has therapies=[] (diagnostic-only). The
    gene+variant match but no therapeutic option should be produced."""
    result = client.lookup(_q("JAK2", "V617F"))
    assert isinstance(result, ActionabilityResult)
    # Match exists but yields no therapeutic options.
    assert result.therapeutic_options == ()
    assert result.is_negative


# ── Additional: pmids tuple shape ────────────────────────────────────────


def test_pubmed_citation_populates_pmid(client: SnapshotCIViCClient):
    result = client.lookup(_q("EGFR", "T790M"))
    assert result.therapeutic_options
    assert result.therapeutic_options[0].pmids == ("25923549",)


def test_non_pubmed_citation_yields_empty_pmids(client: SnapshotCIViCClient):
    result = client.lookup(_q("IDH1", "R132H"))
    assert result.therapeutic_options
    assert result.therapeutic_options[0].pmids == ()


# ── Additional: source_url construction ──────────────────────────────────


def test_source_url_is_civic_evidence_link_when_match_exists(
    client: SnapshotCIViCClient,
):
    result = client.lookup(_q("BRAF", "V600E"))
    assert result.source_url.startswith("https://civicdb.org/links/evidence_items/")


def test_source_url_falls_back_to_gene_link_when_no_match(
    client: SnapshotCIViCClient,
):
    result = client.lookup(_q("BRAF", "V601Q"))
    # Gene known but variant unknown → gene-level fallback.
    assert result.source_url == "https://civicdb.org/links/genes/BRAF"


# ── Additional: malformed entries skipped at init ────────────────────────


def test_malformed_entry_skipped_at_init():
    """Item F10 in the fixture has gene='' and should be dropped at load
    time without crashing."""
    c = SnapshotCIViCClient(FIXTURE_PATH)
    # 10 items in fixture, 1 malformed → 9 kept.
    assert c._kept_count == 9
    assert c._skipped_count == 1


# ── Additional: missing snapshot file raises at __init__ ─────────────────


def test_missing_snapshot_raises_file_not_found(tmp_path):
    bogus = tmp_path / "does_not_exist.yaml"
    with pytest.raises(FileNotFoundError):
        SnapshotCIViCClient(bogus)


# ── Additional: case-insensitive gene lookup ─────────────────────────────


def test_gene_lookup_is_case_insensitive(client: SnapshotCIViCClient):
    upper = client.lookup(_q("BRAF", "V600E"))
    lower = client.lookup(_q("braf", "V600E"))
    assert len(upper.therapeutic_options) == len(lower.therapeutic_options)
