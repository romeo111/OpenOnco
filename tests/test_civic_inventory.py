from __future__ import annotations

from pathlib import Path

from knowledge_base.ingestion.civic_inventory import (
    build_civic_inventory_from_path,
    render_inventory_markdown,
)


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "civic_subset_for_testing.yaml"
REAL_SNAPSHOT_PATH = (
    Path(__file__).resolve().parents[1]
    / "knowledge_base"
    / "hosted"
    / "civic"
    / "2026-04-25"
    / "evidence.yaml"
)


def test_fixture_inventory_counts_are_deterministic():
    inventory = build_civic_inventory_from_path(FIXTURE_PATH, top_n=3)

    assert inventory.snapshot_date == "2026-04-25-fixture"
    assert inventory.evidence_items == 10
    assert inventory.accepted_evidence_items == 10
    assert inventory.unique_molecular_profiles == 9
    assert inventory.unique_gene_variant_pairs == 9
    assert inventory.unique_genes == 7
    assert inventory.therapy_bearing_evidence_items == 9
    assert inventory.resistance_evidence_items == 1
    assert inventory.evidence_level_distribution == {
        "A": 4,
        "B": 3,
        "C": 2,
        "E": 1,
    }
    assert inventory.evidence_type_distribution["Predictive"] == 9
    assert inventory.evidence_type_distribution["Diagnostic"] == 1
    assert inventory.top_genes_by_evidence[0] == ("BRAF", 3)


def test_inventory_markdown_contains_review_tables():
    inventory = build_civic_inventory_from_path(FIXTURE_PATH, top_n=2)
    markdown = render_inventory_markdown(
        inventory,
        snapshot_label="tests/fixtures/civic_subset_for_testing.yaml",
    )

    assert "# CIViC snapshot inventory - 2026-04-25-fixture" in markdown
    assert "Evidence Level Distribution" in markdown
    assert "| BRAF | 3 |" in markdown
    assert "Top Disease/Therapy Pairs" in markdown


def test_real_snapshot_inventory_matches_current_hosted_snapshot():
    inventory = build_civic_inventory_from_path(REAL_SNAPSHOT_PATH, top_n=5)

    assert inventory.snapshot_date == "2026-04-25"
    assert inventory.evidence_items == 4842
    assert inventory.accepted_evidence_items == 4842
    assert inventory.unique_molecular_profiles == 1933
    assert inventory.unique_gene_variant_pairs == 1933
    assert inventory.unique_genes == 551
    assert inventory.therapy_bearing_evidence_items == 2841
    assert inventory.resistance_evidence_items == 1333
    assert inventory.evidence_level_distribution == {
        "A": 225,
        "B": 1619,
        "C": 1668,
        "D": 1298,
        "E": 32,
    }
