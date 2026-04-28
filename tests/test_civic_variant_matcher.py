"""Unit tests for civic_variant_matcher.

Covers the audit-known tricky cases from
``docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`` §2.5 plus
substring-trap negatives and pan-fusion handling.
"""

from __future__ import annotations

import pytest

from knowledge_base.engine.civic_variant_matcher import (
    matches_civic_entry,
    split_fusion_components,
)


# ── split_fusion_components ──────────────────────────────────────────────


class TestSplitFusionComponents:
    def test_double_colon(self):
        assert split_fusion_components("BCR::ABL1") == ["BCR", "ABL1"]

    def test_hyphen_both_hgnc(self):
        assert split_fusion_components("EML4-ALK") == ["EML4", "ALK"]

    def test_etv6_ntrk3(self):
        assert split_fusion_components("ETV6::NTRK3") == ["ETV6", "NTRK3"]

    def test_single_gene(self):
        assert split_fusion_components("BRAF") == ["BRAF"]

    def test_v_alk_civic_idiom(self):
        # CIViC sometimes uses "V::ALK" for variant ALK fusions.
        assert split_fusion_components("V::ALK") == ["V", "ALK"]

    def test_hyphen_not_a_fusion(self):
        # Hyphenated string that isn't gene-gene shouldn't split.
        # E.g. a variant-like string accidentally landing in the gene field.
        assert split_fusion_components("p.V600-mut") == ["p.V600-mut"]

    def test_empty(self):
        assert split_fusion_components("") == []

    def test_whitespace(self):
        assert split_fusion_components("  BCR::ABL1  ") == ["BCR", "ABL1"]


# ── matches_civic_entry ──────────────────────────────────────────────────


class TestMatchesCivicEntry:

    # Rule 1 — exact match
    def test_01_exact_match_braf_v600e(self):
        assert matches_civic_entry(
            query_gene="BRAF", query_variant="V600E",
            civic_gene="BRAF", civic_variant="V600E",
        ) is True

    # Rule 2 — audit case: BCR::ABL1 + T315I
    def test_02_bcr_abl1_t315i_audit_case(self):
        assert matches_civic_entry(
            query_gene="ABL1", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is True

    # Rule 2 — EML4-ALK + G1202R
    def test_03_eml4_alk_g1202r(self):
        assert matches_civic_entry(
            query_gene="ALK", query_variant="G1202R",
            civic_gene="EML4-ALK", civic_variant="Fusion AND ALK G1202R",
        ) is True

    # Rule 2 — EML4-ALK + L1196M
    def test_04_eml4_alk_l1196m(self):
        assert matches_civic_entry(
            query_gene="ALK", query_variant="L1196M",
            civic_gene="EML4-ALK", civic_variant="Fusion AND ALK L1196M",
        ) is True

    # Rule 2 — CD74-ROS1 + G2032R
    def test_05_cd74_ros1_g2032r(self):
        assert matches_civic_entry(
            query_gene="ROS1", query_variant="G2032R",
            civic_gene="CD74-ROS1", civic_variant="Fusion AND ROS1 G2032R",
        ) is True

    # Rule 3 — pan-ALK fusion query
    def test_06_pan_alk_fusion(self):
        assert matches_civic_entry(
            query_gene="ALK", query_variant="Fusion",
            civic_gene="EML4-ALK", civic_variant="EML4-ALK Fusion",
        ) is True

    # Negative — gene match, different variant
    def test_07_negative_braf_v600k_vs_v600e(self):
        assert matches_civic_entry(
            query_gene="BRAF", query_variant="V600K",
            civic_gene="BRAF", civic_variant="V600E",
        ) is False

    # Negative — variant match, different gene (not fusion partner)
    def test_08_negative_braf_t315i_vs_bcr_abl1(self):
        assert matches_civic_entry(
            query_gene="BRAF", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    # Negative — substring trap (T315 must NOT match T315I)
    def test_09_negative_substring_trap_t315_vs_t315i(self):
        assert matches_civic_entry(
            query_gene="ABL1", query_variant="T315",
            civic_gene="BCR::ABL1", civic_variant="T315I",
        ) is False

    # Negative — wrong fusion partner (TPM3 not in CD74-ROS1)
    def test_10_negative_wrong_fusion_partner(self):
        assert matches_civic_entry(
            query_gene="TPM3", query_variant="Fusion",
            civic_gene="CD74-ROS1", civic_variant="CD74-ROS1",
        ) is False

    # Edge — empty civic_variant
    def test_11_edge_empty_civic_variant(self):
        assert matches_civic_entry(
            query_gene="ABL1", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="",
        ) is False

    # Edge — query gene not in fusion components
    def test_12_edge_query_gene_not_in_components(self):
        assert matches_civic_entry(
            query_gene="KRAS", query_variant="G12C",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    # ── Audit-driven additions ──────────────────────────────────────────

    # ETV6::NTRK3 — common pediatric / secretory carcinoma fusion.
    def test_13_etv6_ntrk3_g623r_resistance(self):
        # Synthetic NTRK3 resistance mutation on ETV6::NTRK3 background.
        assert matches_civic_entry(
            query_gene="NTRK3", query_variant="G623R",
            civic_gene="ETV6::NTRK3", civic_variant="Fusion AND NTRK3 G623R",
        ) is True

    # Pan-fusion via the "Rearrangement" sentinel.
    def test_14_pan_fusion_rearrangement_sentinel(self):
        assert matches_civic_entry(
            query_gene="ALK", query_variant="Rearrangement",
            civic_gene="EML4::ALK", civic_variant="EML4::ALK",
        ) is True

    # Pan-fusion case-insensitivity ("fusions" plural).
    def test_15_pan_fusions_plural(self):
        assert matches_civic_entry(
            query_gene="ROS1", query_variant="fusions",
            civic_gene="CD74::ROS1", civic_variant="CD74-ROS1 Fusion",
        ) is True

    # Pan-fusion query against a single-gene CIViC entry that says "Fusion".
    def test_16_pan_fusion_single_gene_entry(self):
        # Some CIViC entries have a single gene with variant "Fusion".
        assert matches_civic_entry(
            query_gene="ALK", query_variant="Fusion",
            civic_gene="ALK", civic_variant="Fusion",
        ) is True

    # Pan-fusion query against a single-gene non-fusion variant → False.
    def test_17_pan_fusion_query_against_point_mutation(self):
        assert matches_civic_entry(
            query_gene="BRAF", query_variant="Fusion",
            civic_gene="BRAF", civic_variant="V600E",
        ) is False

    # Substring trap on the gene side: "ABL" ≠ "ABL1".
    def test_18_negative_gene_substring_trap_abl_vs_abl1(self):
        # ABL is not a fusion component of BCR::ABL1.
        assert matches_civic_entry(
            query_gene="ABL", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    # Empty query — defensive.
    def test_19_empty_query_gene(self):
        assert matches_civic_entry(
            query_gene="", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    def test_20_empty_query_variant(self):
        assert matches_civic_entry(
            query_gene="ABL1", query_variant="",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    # Compound resistance variant on fusion: variant is a token list.
    def test_21_compound_variant_multiple_mutations(self):
        # "Fusion AND ABL1 T315I AND ABL1 E255K" — should match either component.
        assert matches_civic_entry(
            query_gene="ABL1", query_variant="E255K",
            civic_gene="BCR::ABL1",
            civic_variant="Fusion AND ABL1 T315I AND ABL1 E255K",
        ) is True

    # Negative: variant-token match but wrong fusion partner gene.
    def test_22_negative_variant_token_match_wrong_partner(self):
        # T315I is a token in the variant, but the query gene ("EGFR") is
        # not a component of BCR::ABL1.
        assert matches_civic_entry(
            query_gene="EGFR", query_variant="T315I",
            civic_gene="BCR::ABL1", civic_variant="Fusion AND ABL1 T315I",
        ) is False

    # Phase 3.5 — Rule 1 case-insensitive on variant.
    def test_23_rule1_case_insensitive_variant_npm1_w288fs(self):
        # NPM1 W288fs (lowercase fs) vs CIViC W288FS (uppercase). Surfaced
        # by Phase 3-O via SnapshotCIViCClient against real 2026-04-25 snapshot.
        assert matches_civic_entry(
            query_gene="NPM1", query_variant="W288fs",
            civic_gene="NPM1", civic_variant="W288FS",
        ) is True

    # Phase 3.5 — Rule 1 case-insensitive on gene (defensive).
    def test_24_rule1_case_insensitive_gene_lowercase_braf(self):
        # HGNC convention is uppercase; defensive against non-canonical input.
        assert matches_civic_entry(
            query_gene="braf", query_variant="V600E",
            civic_gene="BRAF", civic_variant="V600E",
        ) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
