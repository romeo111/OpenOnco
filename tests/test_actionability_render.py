"""Actionability render tests — phase-4 (ESCAT-primary + CIViC-detailed).

Renamed from test_oncokb_render.py during the CIViC pivot. Phase 1 removed
the OncoKB-shaped tier-badge banner. Phase 4 (2026-04-27) reinstates these
tests in source-agnostic form against `_format_evidence_sources` +
`_render_variant_actionability` in `knowledge_base.engine.render`.

Pinned contracts (defense-in-depth):
  - SRC-ONCOKB entries are NEVER surfaced in HCP HTML (OncoKB ToS).
  - When evidence_sources is empty after SRC-ONCOKB skip, primary_sources
    (sans OncoKB) are promoted as a fallback (Phase 3-O finding).
  - SRC-CIVIC entries link to civicdb.org.
  - direction="Does Not Support" or significance="Resistance" surface
    a ⚠ Resistance flag.
  - Multiple SRC-CIVIC entries at the same level collapse cleanly.
  - Patient-mode never surfaces evidence_sources content (firewall —
    enforced by `tests/test_patient_render.py`; cross-checked here).
"""

from __future__ import annotations

from types import SimpleNamespace

from knowledge_base.engine.render import (
    _format_evidence_sources,
    _render_variant_actionability,
    _is_resistance_entry,
    _is_skipped_source,
)


# ── Helpers ──────────────────────────────────────────────────────────────


def _hit(**kw):
    """Build a minimal VariantActionabilityHit-like object for the renderer.

    `_render_variant_actionability` reads via attribute access on the items
    in `plan.variant_actionability`, so SimpleNamespace is sufficient."""
    defaults = dict(
        bma_id="BMA-TEST",
        biomarker_id="BIO-TEST",
        variant_qualifier=None,
        escat_tier="IA",
        evidence_sources=[],
        evidence_summary="",
        recommended_combinations=[],
        primary_sources=[],
    )
    defaults.update(kw)
    return SimpleNamespace(**defaults)


def _plan(hits):
    return SimpleNamespace(variant_actionability=hits)


# ── _is_skipped_source / _is_resistance_entry primitives ─────────────────


def test_is_skipped_source_catches_oncokb_variants():
    assert _is_skipped_source("SRC-ONCOKB") is True
    assert _is_skipped_source("src-oncokb") is True
    assert _is_skipped_source("SRC-ONCOKB-V4") is True
    assert _is_skipped_source("SRC-CIVIC") is False
    assert _is_skipped_source("SRC-NCCN-NSCLC-2026") is False
    assert _is_skipped_source("") is False
    assert _is_skipped_source(None) is False


def test_is_resistance_entry_handles_does_not_support():
    assert _is_resistance_entry("Does Not Support", "Sensitivity/Response") is True
    assert _is_resistance_entry("does_not_support", "") is True
    assert _is_resistance_entry("Supports", "Resistance") is True
    assert _is_resistance_entry("Supports", "Reduced Sensitivity") is False
    assert _is_resistance_entry("Supports", "Sensitivity/Response") is False
    assert _is_resistance_entry(None, None) is False


# ── _format_evidence_sources direct unit tests ───────────────────────────


def test_format_skips_src_oncokb_entirely():
    """A BMA with [SRC-ONCOKB, SRC-CIVIC] → only CIViC entry visible."""
    es = [
        {"source": "SRC-ONCOKB", "level": "1"},
        {
            "source": "SRC-CIVIC",
            "level": "B",
            "direction": "Supports",
            "significance": "Sensitivity/Response",
            "evidence_ids": ["12345"],
        },
    ]
    out = _format_evidence_sources(es)
    assert "ONCOKB" not in out.upper()
    assert "SRC-CIVIC" in out
    assert "Level B" in out
    assert "civicdb.org/links/evidence_items/12345" in out


def test_format_civic_link_strips_eid_prefix():
    es = [{"source": "SRC-CIVIC", "level": "A", "evidence_ids": ["EID9999"]}]
    out = _format_evidence_sources(es)
    assert "civicdb.org/links/evidence_items/9999" in out


def test_format_civic_link_falls_back_to_homepage_if_no_numeric_id():
    es = [{"source": "SRC-CIVIC", "level": "A", "evidence_ids": []}]
    out = _format_evidence_sources(es)
    assert "civicdb.org/" in out


def test_format_resistance_flag_for_does_not_support():
    es = [
        {
            "source": "SRC-CIVIC",
            "level": "B",
            "direction": "Does Not Support",
            "significance": "Sensitivity/Response",
        }
    ]
    out = _format_evidence_sources(es)
    assert "evidence-resistance" in out
    assert "⚠" in out


def test_format_resistance_flag_for_significance_resistance():
    es = [
        {
            "source": "SRC-CIVIC",
            "level": "A",
            "direction": "Supports",
            "significance": "Resistance",
        }
    ]
    out = _format_evidence_sources(es)
    assert "evidence-resistance" in out


def test_format_dedupes_multiple_civic_entries_at_same_level():
    """Multiple SRC-CIVIC entries at the same level collapse to one row."""
    es = [
        {"source": "SRC-CIVIC", "level": "B", "evidence_ids": ["100"]},
        {"source": "SRC-CIVIC", "level": "B", "evidence_ids": ["101"]},
        {"source": "SRC-CIVIC", "level": "B", "evidence_ids": ["102"]},
    ]
    out = _format_evidence_sources(es)
    assert out.count("Level B") == 1


def test_format_keeps_distinct_levels_separate():
    es = [
        {"source": "SRC-CIVIC", "level": "A"},
        {"source": "SRC-CIVIC", "level": "B"},
        {"source": "SRC-CIVIC", "level": "D"},
    ]
    out = _format_evidence_sources(es)
    assert "Level A" in out
    assert "Level B" in out
    assert "Level D" in out


def test_format_fallback_when_only_oncokb_in_evidence_sources():
    """A BMA with ONLY SRC-ONCOKB → fallback engages, primary_sources
    rendered (sans OncoKB)."""
    es = [{"source": "SRC-ONCOKB", "level": "1"}]
    primary = ["SRC-NCCN-MPN-2025", "SRC-ONCOKB", "SRC-ESMO-MPN-2015"]
    out = _format_evidence_sources(es, primary_sources=primary)
    # OncoKB still suppressed
    assert "ONCOKB" not in out.upper()
    # Non-OncoKB primary sources promoted
    assert "SRC-NCCN-MPN-2025" in out
    assert "SRC-ESMO-MPN-2015" in out
    # Fallback note present
    assert "Phase-2-of-CIViC-pivot" in out
    assert "evidence-sources--fallback" in out


def test_format_fallback_when_evidence_sources_empty():
    out = _format_evidence_sources([], primary_sources=["SRC-NCCN-NSCLC-2026"])
    assert "SRC-NCCN-NSCLC-2026" in out
    assert "Phase-2-of-CIViC-pivot" in out


def test_format_fallback_dedupes_primary_sources():
    out = _format_evidence_sources(
        [], primary_sources=["SRC-NCCN-MPN-2025", "SRC-NCCN-MPN-2025"]
    )
    assert out.count("SRC-NCCN-MPN-2025") == 1


def test_format_returns_dash_when_nothing_renderable():
    """No evidence sources, no primary sources, no fallback content."""
    out = _format_evidence_sources([], primary_sources=[])
    assert "—" in out


def test_format_returns_dash_when_only_oncokb_and_no_primary_sources():
    """SRC-ONCOKB skipped + no fallback citations → dash."""
    out = _format_evidence_sources(
        [{"source": "SRC-ONCOKB", "level": "1"}], primary_sources=["SRC-ONCOKB"]
    )
    assert "ONCOKB" not in out.upper()
    assert "—" in out


# ── _render_variant_actionability integration tests ─────────────────────


def test_render_actionability_section_skips_oncokb_in_hcp_mode():
    """HCP-mode rendering of a BMA with [SRC-ONCOKB, SRC-CIVIC] → only
    CIViC entry visible in the rendered table."""
    plan = _plan([
        _hit(
            biomarker_id="BIO-BRAF-V600E",
            variant_qualifier="V600E",
            escat_tier="IA",
            evidence_sources=[
                {"source": "SRC-ONCOKB", "level": "1"},
                {
                    "source": "SRC-CIVIC",
                    "level": "A",
                    "direction": "Supports",
                    "significance": "Sensitivity/Response",
                    "evidence_ids": ["1234"],
                },
            ],
            evidence_summary="BRAF V600E is FDA-recognized.",
            primary_sources=["SRC-NCCN-NSCLC-2026"],
        )
    ])
    html = _render_variant_actionability(plan)
    assert "ONCOKB" not in html.upper()
    assert "SRC-CIVIC" in html
    assert "Level A" in html
    assert "civicdb.org" in html
    # ESCAT tier surfaces as the primary header tag
    assert "escat-IA" in html
    assert "tier-badge" in html


def test_render_actionability_section_fallback_when_only_oncokb_in_evidence():
    """HCP-mode rendering of a BMA with only [SRC-ONCOKB] → fallback
    engages, primary_sources (sans OncoKB) rendered."""
    plan = _plan([
        _hit(
            biomarker_id="BIO-CALR",
            variant_qualifier=None,
            escat_tier="IB",
            evidence_sources=[{"source": "SRC-ONCOKB", "level": "1"}],
            evidence_summary="CALR exon 9 indels in MPN.",
            primary_sources=["SRC-NCCN-MPN-2025", "SRC-ONCOKB", "SRC-ESMO-MPN-2015"],
        )
    ])
    html = _render_variant_actionability(plan)
    # OncoKB never surfaces
    assert "ONCOKB" not in html.upper()
    # Fallback citation cards rendered
    assert "SRC-NCCN-MPN-2025" in html
    assert "SRC-ESMO-MPN-2015" in html
    # Fallback note present
    assert "Phase-2-of-CIViC-pivot" in html
    # ESCAT tier still primary
    assert "escat-IB" in html


def test_render_actionability_section_resistance_marker_renders():
    plan = _plan([
        _hit(
            biomarker_id="BIO-EGFR-T790M",
            variant_qualifier="T790M",
            escat_tier="IA",
            evidence_sources=[
                {
                    "source": "SRC-CIVIC",
                    "level": "B",
                    "direction": "Does Not Support",
                    "significance": "Sensitivity/Response",
                    "evidence_ids": ["555"],
                }
            ],
            primary_sources=["SRC-NCCN-NSCLC-2026"],
        )
    ])
    html = _render_variant_actionability(plan)
    assert "evidence-resistance" in html
    assert "⚠" in html


def test_render_actionability_section_collapses_duplicate_civic_levels():
    plan = _plan([
        _hit(
            biomarker_id="BIO-BRAF-V600E",
            variant_qualifier="V600E",
            escat_tier="IA",
            evidence_sources=[
                {"source": "SRC-CIVIC", "level": "A", "evidence_ids": ["1"]},
                {"source": "SRC-CIVIC", "level": "A", "evidence_ids": ["2"]},
                {"source": "SRC-CIVIC", "level": "A", "evidence_ids": ["3"]},
            ],
            primary_sources=["SRC-NCCN"],
        )
    ])
    html = _render_variant_actionability(plan)
    # One Level A line, not three
    assert html.count("Level A") == 1


def test_render_actionability_section_filters_oncokb_from_primary_sources_column():
    """The right-hand 'Sources' column also filters SRC-ONCOKB."""
    plan = _plan([
        _hit(
            biomarker_id="BIO-BRAF-V600E",
            variant_qualifier="V600E",
            escat_tier="IA",
            evidence_sources=[{"source": "SRC-CIVIC", "level": "A"}],
            primary_sources=["SRC-NCCN-NSCLC-2026", "SRC-ONCOKB"],
        )
    ])
    html = _render_variant_actionability(plan)
    assert "ONCOKB" not in html.upper()
    assert "SRC-NCCN-NSCLC-2026" in html


def test_render_actionability_section_empty_state():
    """No hits → empty placeholder row, no OncoKB anywhere."""
    plan = _plan([])
    html = _render_variant_actionability(plan)
    assert "ONCOKB" not in html.upper()
    assert "actionability-table" in html


def test_render_actionability_section_escat_tier_is_prominent():
    """ESCAT tier renders as the primary `tier-badge` header — vendor-
    neutral, source-of-truth label."""
    plan = _plan([
        _hit(
            biomarker_id="BIO-BRAF-V600E",
            escat_tier="IIA",
            evidence_sources=[{"source": "SRC-CIVIC", "level": "B"}],
            primary_sources=["SRC-NCCN"],
        )
    ])
    html = _render_variant_actionability(plan)
    assert 'tier-badge escat-IIA' in html
    assert ">IIA<" in html
