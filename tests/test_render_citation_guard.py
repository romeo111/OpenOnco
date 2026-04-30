"""PR5 — citation-presence guard at the render layer.

Layer 3 of three independent citation-verification layers (see
`knowledge_base/engine/_citation_guard.py` module docstring for the full
context).

Coverage:

1. Cited entity → no badge.
2. Uncited entity (empty sources) in WARN mode → badge present, content
   still renders.
3. Broken entity (sources contain only unresolved SRC-* IDs) in WARN
   mode → badge present.
4. Same uncited entity in STRICT mode → original content gone, replaced
   by `stripped-block` placeholder.
5. Real-KB drift count: render a representative plan against the real KB
   and assert the guard fires somewhere (>0 badges) — proves the guard
   is wired and surfaces real drift, without pinning an exact number.

These tests intentionally pass `valid_source_ids` directly into the
unit-level resolver to bypass the on-disk lru_cache for determinism.
The end-to-end render tests use a synthetic Plan / SimpleNamespace
fixture, so they exercise the actual `_render_variant_actionability` +
track-block render paths without spinning up the full engine.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._citation_guard import (
    needs_guard,
    render_citation_warn_badge,
    render_stripped_block,
    resolve_citation_status,
)
from knowledge_base.engine.render import (
    _render_variant_actionability,
    _track_citation_dd,
)


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


# ── Synthetic-data fixtures ─────────────────────────────────────────────────


@pytest.fixture
def valid_src_ids():
    """A tiny set of valid SRC-* IDs used by the synthetic tests so we
    don't depend on the real KB's source roster."""
    return {"SRC-FOO-2026", "SRC-BAR-2025"}


def _hit(**kw):
    """Build a SimpleNamespace stand-in for a VariantActionabilityHit.

    `_render_variant_actionability` reads via attribute access; namespace
    is sufficient — same shape the upstream `test_actionability_render`
    suite uses.
    """
    defaults = dict(
        bma_id="BMA-TEST",
        biomarker_id="BIO-TEST",
        variant_qualifier=None,
        escat_tier="IA",
        evidence_sources=[],
        evidence_summary="test summary",
        recommended_combinations=[],
        primary_sources=[],
    )
    defaults.update(kw)
    return SimpleNamespace(**defaults)


def _plan_ns(hits):
    """Build a SimpleNamespace stand-in for `Plan` carrying the hits
    list — enough for `_render_variant_actionability` to iterate."""
    return SimpleNamespace(variant_actionability=hits)


# ── Resolver unit tests ─────────────────────────────────────────────────────


def test_resolver_empty_entity_is_uncited(valid_src_ids):
    r = resolve_citation_status({}, valid_source_ids=valid_src_ids)
    assert r["status"] == "uncited"
    assert r["cited_count"] == 0
    assert r["resolved_count"] == 0


def test_resolver_resolved_source_is_cited(valid_src_ids):
    r = resolve_citation_status(
        {"primary_sources": ["SRC-FOO-2026"]},
        valid_source_ids=valid_src_ids,
    )
    assert r["status"] == "cited"
    assert r["cited_count"] == 1
    assert r["resolved_count"] == 1
    assert r["unresolved_ids"] == []


def test_resolver_unresolved_source_is_broken(valid_src_ids):
    r = resolve_citation_status(
        {"primary_sources": ["SRC-MISSING"]},
        valid_source_ids=valid_src_ids,
    )
    assert r["status"] == "broken"
    assert r["cited_count"] == 1
    assert r["resolved_count"] == 0
    assert r["unresolved_ids"] == ["SRC-MISSING"]


def test_resolver_indication_citation_dict_shape(valid_src_ids):
    """Indication YAML uses `sources: list[Citation]` where each entry
    is a dict with `source_id`. Resolver must handle that shape."""
    r = resolve_citation_status(
        {"sources": [{"source_id": "SRC-FOO-2026", "weight": "primary"}]},
        valid_source_ids=valid_src_ids,
    )
    assert r["status"] == "cited"


def test_resolver_regimen_string_list_shape(valid_src_ids):
    """Regimen YAML uses `sources: list[str]` (raw SRC-* IDs)."""
    r = resolve_citation_status(
        {"sources": ["SRC-FOO-2026", "SRC-BAR-2025"]},
        valid_source_ids=valid_src_ids,
    )
    assert r["status"] == "cited"
    assert r["cited_count"] == 2
    assert r["resolved_count"] == 2


def test_resolver_bma_evidence_sources_shape(valid_src_ids):
    """BMA YAML carries `evidence_sources: list[{source: SRC-*, ...}]`."""
    r = resolve_citation_status(
        {
            "evidence_sources": [
                {"source": "SRC-FOO-2026", "level": "A"},
                {"source": "SRC-MISSING", "level": "B"},
            ]
        },
        valid_source_ids=valid_src_ids,
    )
    # At least one resolves → cited, even though one is broken
    assert r["status"] == "cited"
    assert r["cited_count"] == 2
    assert r["resolved_count"] == 1
    assert r["unresolved_ids"] == ["SRC-MISSING"]


def test_resolver_partial_resolution_is_cited(valid_src_ids):
    """≥1 resolves → status=cited (the badge only fires when NO source
    resolves). This is intentional — a single good citation is enough
    for citation-presence."""
    r = resolve_citation_status(
        {"primary_sources": ["SRC-FOO-2026", "SRC-MISSING-A", "SRC-MISSING-B"]},
        valid_source_ids=valid_src_ids,
    )
    assert r["status"] == "cited"
    assert r["resolved_count"] == 1
    assert r["unresolved_ids"] == ["SRC-MISSING-A", "SRC-MISSING-B"]


def test_needs_guard_branches():
    assert needs_guard("uncited") is True
    assert needs_guard("broken") is True
    assert needs_guard("cited") is False


# ── Track-block helper tests ────────────────────────────────────────────────


def test_cited_entity_no_badge(valid_src_ids):
    """Test 1 — synthetic indication + regimen with valid sources → no
    badge in the rendered <dd> cells."""
    ind_status = resolve_citation_status(
        {"sources": [{"source_id": "SRC-FOO-2026"}]},
        valid_source_ids=valid_src_ids,
    )
    reg_status = resolve_citation_status(
        {"sources": ["SRC-BAR-2025"]},
        valid_source_ids=valid_src_ids,
    )
    ind_dd, reg_dd = _track_citation_dd(
        indication_id="IND-TEST",
        regimen_label="Test Regimen",
        ind_status=ind_status,
        reg_status=reg_status,
        target_lang="uk",
        strict=False,
    )
    assert "no-citation-badge" not in ind_dd
    assert "no-citation-badge" not in reg_dd
    assert "stripped-block" not in ind_dd
    assert "stripped-block" not in reg_dd
    assert "IND-TEST" in ind_dd
    assert "Test Regimen" in reg_dd


def test_uncited_entity_warn_mode_emits_badge(valid_src_ids):
    """Test 2 — entity with empty sources, default warn mode → badge
    present AND original block content still rendered."""
    ind_status = resolve_citation_status({}, valid_source_ids=valid_src_ids)
    reg_status = resolve_citation_status({}, valid_source_ids=valid_src_ids)
    ind_dd, reg_dd = _track_citation_dd(
        indication_id="IND-UNCITED",
        regimen_label="Unsourced Regimen",
        ind_status=ind_status,
        reg_status=reg_status,
        target_lang="uk",
        strict=False,
    )
    assert "no-citation-badge" in ind_dd
    assert "no-citation-badge" in reg_dd
    # WARN: original content still rendered
    assert "IND-UNCITED" in ind_dd
    assert "Unsourced Regimen" in reg_dd
    # Strip placeholder NOT present
    assert "stripped-block" not in ind_dd
    assert "stripped-block" not in reg_dd


def test_broken_entity_warn_mode_emits_badge(valid_src_ids):
    """Test 3 — entity with `sources: [SRC-MISSING]` (none resolve) →
    badge present in WARN mode."""
    ind_status = resolve_citation_status(
        {"sources": [{"source_id": "SRC-MISSING-CITATION"}]},
        valid_source_ids=valid_src_ids,
    )
    reg_status = resolve_citation_status(
        {"sources": ["SRC-ALSO-MISSING"]},
        valid_source_ids=valid_src_ids,
    )
    assert ind_status["status"] == "broken"
    assert reg_status["status"] == "broken"
    ind_dd, reg_dd = _track_citation_dd(
        indication_id="IND-BROKEN",
        regimen_label="Broken Regimen",
        ind_status=ind_status,
        reg_status=reg_status,
        target_lang="uk",
        strict=False,
    )
    assert "no-citation-badge" in ind_dd
    assert "no-citation-badge" in reg_dd
    # WARN: original content still rendered
    assert "IND-BROKEN" in ind_dd
    assert "Broken Regimen" in reg_dd


def test_uncited_entity_strict_mode_strips(valid_src_ids):
    """Test 4 — same as #2 but strict=True. Original content must be
    GONE; `stripped-block` placeholder takes its place."""
    ind_status = resolve_citation_status({}, valid_source_ids=valid_src_ids)
    reg_status = resolve_citation_status({}, valid_source_ids=valid_src_ids)
    ind_dd, reg_dd = _track_citation_dd(
        indication_id="IND-WILL-BE-STRIPPED",
        regimen_label="Will Be Stripped Regimen",
        ind_status=ind_status,
        reg_status=reg_status,
        target_lang="uk",
        strict=True,
    )
    assert "stripped-block" in ind_dd
    assert "stripped-block" in reg_dd
    # In strict mode the original content is REPLACED — not coexisting
    assert "IND-WILL-BE-STRIPPED" not in ind_dd
    assert "Will Be Stripped Regimen" not in reg_dd
    # And no warn-mode badge in strict mode (it's redacted, not flagged)
    assert "no-citation-badge" not in ind_dd
    assert "no-citation-badge" not in reg_dd


# ── Variant actionability table guard tests ─────────────────────────────────


def test_variant_actionability_warn_badges_uncited_hit():
    """An ESCAT row whose primary_sources + evidence_sources are both
    empty triggers the warn-mode badge in the biomarker cell."""
    plan = _plan_ns([
        _hit(
            biomarker_id="BIO-FOO",
            primary_sources=[],
            evidence_sources=[],
        )
    ])
    html = _render_variant_actionability(plan)
    assert "no-citation-badge" in html
    assert "stripped-row" not in html
    # Row content (biomarker label) still rendered
    assert "BIO-FOO" in html


def test_variant_actionability_strict_strips_uncited_hit():
    plan = _plan_ns([
        _hit(
            biomarker_id="BIO-FOO",
            primary_sources=[],
            evidence_sources=[],
        )
    ])
    html = _render_variant_actionability(plan, strict_citation_guard=True)
    assert "stripped-block" in html
    # Biomarker label NOT in HTML (row was redacted)
    assert "BIO-FOO" not in html


def test_variant_actionability_cited_hit_no_badge():
    """SRC-CIVIC is a real Source entity — no badge expected. (The cache
    is module-level; this exercises the on-disk path on purpose.)"""
    plan = _plan_ns([
        _hit(
            biomarker_id="BIO-CIVIC-OK",
            evidence_sources=[{"source": "SRC-CIVIC", "level": "A"}],
            primary_sources=["SRC-CIVIC"],
        )
    ])
    html = _render_variant_actionability(plan)
    # No badge for the cited row
    assert "no-citation-badge" not in html
    assert "BIO-CIVIC-OK" in html


# ── End-to-end render integration ───────────────────────────────────────────


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def _count_inline_badges(html: str) -> int:
    """Count `no-citation-badge` occurrences excluding the CSS class
    definition (which appears in every rendered <style>). Subtracting
    `.no-citation-badge` (with leading dot) is a clean way to discount
    the CSS-block hits from inline-aside hits.
    """
    return html.count("no-citation-badge") - html.count(".no-citation-badge")


def test_real_kb_drift_count_diagnostic():
    """Test 5a — render a representative plan against the real KB and
    print the structural drift count. This is a diagnostic test, NOT a
    regression assertion: the structural drift on the current KB is 0
    (real KB is well-cited at the structural level — see the
    monkeypatched test below for the regression check).

    Using `patient_zero_indolent.json` because the existing render-suite
    smoke test already builds this profile reliably."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    badge_count = _count_inline_badges(html)
    print(f"\n[citation-guard] real-KB structural drift for "
          f"patient_zero_indolent: {badge_count} inline badges")
    # Document shell well-formed
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


def test_real_kb_drift_with_forced_unresolvable_sources(monkeypatch):
    """Test 5b — the regression check the brief asks for. Forces the
    source-id loader to return an empty set so EVERY cited SRC-* in the
    rendered plan looks broken; then asserts the guard fires under real
    render conditions.

    This proves the guard is wired into the actual render pipeline (not
    just the unit-tested helpers) and would catch real drift if the KB
    started shedding sources.
    """
    from knowledge_base.engine import _citation_guard
    # Force every SRC-* lookup to fail by emptying the source set
    monkeypatch.setattr(
        _citation_guard, "_load_source_ids", lambda: frozenset()
    )
    _citation_guard.clear_source_id_cache()

    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    badge_count = _count_inline_badges(html)
    # Both tracks (standard + aggressive) carry an indication AND a
    # regimen with sources; with all sources unresolvable, every one
    # should trigger a badge. ≥1 is the floor; in practice 4 fire.
    assert badge_count >= 1, (
        f"Expected ≥1 inline badge under forced-broken-sources stress, "
        f"got {badge_count}. Guard not wired into render pipeline?"
    )

    # And confirm the actual badge HTML is present (not just the class)
    assert "❓ без цитати" in html


def test_real_kb_strict_mode_strips_under_forced_drift(monkeypatch):
    """Strict mode under forced drift — `stripped-block` placeholder
    must appear. Proves strict-mode wiring."""
    from knowledge_base.engine import _citation_guard
    monkeypatch.setattr(
        _citation_guard, "_load_source_ids", lambda: frozenset()
    )
    _citation_guard.clear_source_id_cache()

    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, strict_citation_guard=True)
    assert "stripped-block" in html
    # Doc shell still well-formed
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


def test_real_kb_strict_mode_clean_run_does_not_strip():
    """Strict mode against the un-stressed real KB — no entity should
    be stripped because the KB is structurally well-cited (drift=0). The
    placeholder text must not appear in the rendered output."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, strict_citation_guard=True)
    # The actual placeholder text — not the CSS class — should not appear.
    assert "блок видалено" not in html
    # Doc shell still well-formed
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


# ── Localisation sanity ─────────────────────────────────────────────────────


def test_warn_badge_label_is_ukrainian_by_default():
    badge = render_citation_warn_badge("uk")
    assert "без цитати" in badge
    assert "no-citation-badge" in badge


def test_warn_badge_label_english():
    badge = render_citation_warn_badge("en")
    assert "no citation" in badge


def test_stripped_block_label_ua_default():
    block = render_stripped_block("uk")
    assert "блок видалено" in block
    assert "stripped-block" in block
