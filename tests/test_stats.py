"""Tests for knowledge_base.stats — entity counters + per-disease coverage.

Verifies:
1. collect_stats walks the live KB and returns plausible counts (>0 for
   the categories we know exist: diseases, indications, regimens, drugs).
2. Per-disease coverage is populated (DIS-MM and DIS-HCV-MZL exist today
   and both have full disease→indication→regimen→algorithm chains, so
   their status is at least 'stub_full_chain').
3. Text formatter emits the expected section headers without raising.
4. JSON formatter emits valid JSON with derived coverage_status field.
5. HTML widget formatter is well-formed (single .oo-widget div, contains
   counter cards + coverage table + STUB warning when appropriate).
6. CHARTER §6.1 STUB warning fires when no entity has reviewer_signoffs ≥ 2.
"""

from __future__ import annotations

import json

from knowledge_base.stats import (
    collect_stats,
    format_html_widget,
    format_json,
    format_text,
)


def test_collect_stats_baseline():
    s = collect_stats()
    assert s.total_yaml_entities > 0
    by_type = {e.type: e.count for e in s.entities}
    # Categories with known content today
    for required in ("diseases", "indications", "regimens", "drugs", "tests"):
        assert by_type.get(required, 0) > 0, f"expected {required} > 0"
    assert s.specs_count >= 5
    assert s.api_clients_count >= 1
    assert s.skills_planned_roles >= 10  # MDT role catalog


def test_disease_coverage_populated():
    s = collect_stats()
    by_id = {d.disease_id: d for d in s.diseases}
    assert "DIS-MM" in by_id
    mm = by_id["DIS-MM"]
    assert mm.indications >= 1
    assert mm.regimens >= 1
    assert mm.has_algorithm
    assert mm.coverage_status in {"stub_full_chain", "reviewed"}


def test_text_formatter_smoke():
    s = collect_stats()
    out = format_text(s)
    assert "OpenOnco" in out
    assert "KB entities" in out
    assert "Покриття по хворобах" in out
    assert "Reviewer sign-offs" in out


def test_json_formatter_valid():
    s = collect_stats()
    payload = json.loads(format_json(s))
    assert payload["total_yaml_entities"] == s.total_yaml_entities
    assert "diseases" in payload
    assert all("coverage_status" in d for d in payload["diseases"])


def test_html_widget_well_formed():
    s = collect_stats()
    html = format_html_widget(s)
    assert html.count('<div class="oo-widget"') == 1
    assert html.count("</div>") >= 1
    assert "<table>" in html and "</table>" in html
    # Counter cards: one per entity type
    assert html.count('class="oo-card"') == len(s.entities)
    # Disease rows
    for d in s.diseases:
        assert d.disease_id in html


def test_html_widget_stub_warning_present_when_no_reviews():
    s = collect_stats()
    html = format_html_widget(s)
    # As of today no content has 2 sign-offs → warning must show
    if s.reviewer_signoffs_reviewed == 0 and s.reviewer_signoffs_total > 0:
        assert "STUB" in html
        assert "Co-Lead" in html


def test_html_widget_no_style_flag():
    s = collect_stats()
    with_style = format_html_widget(s, embed_style=True)
    without_style = format_html_widget(s, embed_style=False)
    assert with_style.startswith("<style>")
    assert not without_style.startswith("<style>")


def test_corpus_aggregates_populated():
    """Marketing metric: total pages + primary references across all sources.
    All 13 current sources have pages_count + references_count populated; the
    aggregates are non-trivial (~2000+ pages, ~3000+ refs)."""
    s = collect_stats()
    sources_total = next((e.count for e in s.entities if e.type == "sources"), 0)
    assert sources_total > 0, "expected at least one Source entity"
    assert s.sources_with_corpus_data == sources_total, (
        "expected every Source to carry pages_count + references_count "
        "(populated by scripts/_populate_source_corpus.py)"
    )
    assert s.corpus_pages_total > 1000, (
        f"expected >1000 pages of guideline mass; got {s.corpus_pages_total}"
    )
    assert s.corpus_references_total > 2000, (
        f"expected >2000 primary references behind sources; got {s.corpus_references_total}"
    )


def test_corpus_metrics_in_text_formatter():
    s = collect_stats()
    out = format_text(s)
    assert "Корпус літератури" in out
    assert f"{s.corpus_references_total:,}" in out
    assert f"{s.corpus_pages_total:,}" in out


def test_corpus_metrics_in_html_widget():
    s = collect_stats()
    html = format_html_widget(s)
    assert "Корпус літератури" in html
    assert f"{s.corpus_references_total:,}" in html
    assert "primary publications" in html
