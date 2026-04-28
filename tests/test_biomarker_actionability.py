"""Comprehensive test suite for the BiomarkerActionability ESCAT/OncoKB system.

Covers:
  - Section A: Schema validation (every BMA YAML cell parses cleanly)
  - Section B: FK resolution (biomarker_id, disease_id, primary_sources)
  - Section C: Variant matching helper unit tests
  - Section D: 5 known-case end-to-end fixtures (BRAF/EGFR/BRCA1/KRAS/ALK)
  - Section E: Render output asserts ESCAT/OncoKB tier badges in HTML

CSD-1 partnership context: confirms that an NGS report → tumor-board brief
flow surfaces ESMO-grade and OncoKB-grade clinical context next to the
chosen track. The engine MUST NOT use these tier values for selection
(CHARTER §8.3) — they are render-time metadata only.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._actionability import (
    _biomarker_keys_match,
    _extract_variant,
    _normalize_gene_stem,
    _variant_matches,
    find_matching_actionability,
)
from knowledge_base.schemas.biomarker_actionability import BiomarkerActionability
from knowledge_base.validation.loader import load_content


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
BMA_DIR = KB_ROOT / "biomarker_actionability"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "cases"


# Module-level cached load (KB load is ~1-2s; reuse across tests)
@pytest.fixture(scope="module")
def kb_load():
    """Load the KB once for the whole module."""
    return load_content(KB_ROOT)


@pytest.fixture(scope="module")
def entities(kb_load):
    return kb_load.entities_by_id


@pytest.fixture(scope="module")
def bma_records():
    """Yield (path, raw_dict) for every BMA YAML file."""
    out = []
    for path in sorted(BMA_DIR.rglob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        out.append((path, raw))
    return out


# ── Valid enum sets per the schema ───────────────────────────────────────
VALID_ESCAT = {"IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X"}
VALID_ONCOKB = {"1", "2", "3A", "3B", "4", "R1", "R2"}


# ─────────────────────────────────────────────────────────────────────────
# Section A — Schema validation
# ─────────────────────────────────────────────────────────────────────────


def test_all_bma_cells_load_clean(bma_records):
    """Every BMA YAML cell parses into a BiomarkerActionability without raising."""
    assert bma_records, "Expected at least one BMA cell on disk"
    failures: list[tuple[str, str]] = []
    for path, raw in bma_records:
        try:
            BiomarkerActionability.model_validate(raw)
        except Exception as exc:  # noqa: BLE001
            failures.append((path.name, str(exc)[:200]))
    assert not failures, f"BMA schema validation failures: {failures}"


def test_all_bma_cells_have_valid_escat_tier(bma_records):
    """Every cell's escat_tier is in the canonical ESMO ESCAT set."""
    bad = [
        (path.name, raw.get("escat_tier"))
        for path, raw in bma_records
        if raw.get("escat_tier") not in VALID_ESCAT
    ]
    assert not bad, f"Cells with invalid escat_tier: {bad}"


@pytest.mark.skip(
    reason="phase-1.5: BMA YAML still carries legacy `oncokb_level`; "
    "schema dropped that field in Phase 1 (CIViC pivot). Phase 1.5 "
    "migrates the field into `evidence_sources` entries; this test "
    "is restored as a check on `evidence_sources` content then."
)
def test_all_bma_cells_have_valid_oncokb_level(bma_records):
    """Every cell's oncokb_level is in the canonical OncoKB v2 levels set."""
    bad = [
        (path.name, raw.get("oncokb_level"))
        for path, raw in bma_records
        if str(raw.get("oncokb_level")) not in VALID_ONCOKB
    ]
    assert not bad, f"Cells with invalid oncokb_level: {bad}"


def test_all_bma_cells_have_at_least_one_source(bma_records):
    """primary_sources must be a non-empty list (loader-enforced; tested here too)."""
    bad = [
        path.name
        for path, raw in bma_records
        if not (raw.get("primary_sources") or [])
    ]
    assert not bad, f"Cells with empty primary_sources: {bad}"


def test_all_bma_cells_have_last_verified(bma_records):
    """last_verified is required and should be an ISO date string (YYYY-MM-DD)."""
    bad = []
    for path, raw in bma_records:
        lv = raw.get("last_verified")
        if not isinstance(lv, str) or len(lv) < 10 or lv[4] != "-" or lv[7] != "-":
            bad.append((path.name, lv))
    assert not bad, f"Cells with missing/malformed last_verified: {bad}"


# ─────────────────────────────────────────────────────────────────────────
# Section B — FK resolution
# ─────────────────────────────────────────────────────────────────────────


def test_bma_biomarker_id_resolves(bma_records, entities):
    """Every cell.biomarker_id exists in entities_by_id with type=biomarkers."""
    bad = []
    for path, raw in bma_records:
        bid = raw.get("biomarker_id")
        info = entities.get(bid)
        if info is None:
            bad.append((path.name, f"missing biomarker_id={bid}"))
        elif info.get("type") != "biomarkers":
            bad.append((path.name, f"{bid} resolved to type={info.get('type')}"))
    assert not bad, f"Unresolved/mistyped biomarker_id refs: {bad}"


def test_bma_disease_id_resolves(bma_records, entities):
    """Every cell.disease_id exists in entities_by_id with type=diseases."""
    bad = []
    for path, raw in bma_records:
        did = raw.get("disease_id")
        info = entities.get(did)
        if info is None:
            bad.append((path.name, f"missing disease_id={did}"))
        elif info.get("type") != "diseases":
            bad.append((path.name, f"{did} resolved to type={info.get('type')}"))
    assert not bad, f"Unresolved/mistyped disease_id refs: {bad}"


def test_bma_primary_sources_resolve(bma_records, entities):
    """Every cell.primary_sources[*] resolves to a Source entity."""
    bad = []
    for path, raw in bma_records:
        for sid in raw.get("primary_sources") or []:
            info = entities.get(sid)
            if info is None:
                bad.append((path.name, f"missing source_id={sid}"))
            elif info.get("type") != "sources":
                bad.append((path.name, f"{sid} resolved to type={info.get('type')}"))
    assert not bad, f"Unresolved/mistyped primary_sources refs: {bad}"


# ─────────────────────────────────────────────────────────────────────────
# Section C — Variant matching helper logic
# ─────────────────────────────────────────────────────────────────────────


def _make_cell(biomarker_id: str, variant_qualifier, disease_id: str, bma_id: str = "BMA-TEST") -> dict:
    """Synthesize a minimal entities_by_id entry for a BMA cell."""
    return {
        bma_id: {
            "type": "biomarker_actionability",
            "data": {
                "id": bma_id,
                "biomarker_id": biomarker_id,
                "variant_qualifier": variant_qualifier,
                "disease_id": disease_id,
                "escat_tier": "IA",
                "oncokb_level": "1",
                "evidence_summary": "test",
                "primary_sources": ["SRC-TEST"],
            },
        }
    }


def test_match_exact_variant_qualifier():
    ents = _make_cell("BIO-BRAF-V600E", "V600E", "DIS-CRC")
    hits = find_matching_actionability({"BRAF": "V600E"}, "DIS-CRC", ents)
    assert len(hits) == 1
    assert hits[0]["bma_id"] == "BMA-TEST"


def test_match_substring_variant_qualifier():
    """Patient `p.V600E` (HGVS-prefixed) should still match a `V600E` cell."""
    ents = _make_cell("BIO-BRAF-V600E", "V600E", "DIS-CRC")
    hits = find_matching_actionability({"BRAF": "p.V600E"}, "DIS-CRC", ents)
    assert len(hits) == 1


def test_match_case_insensitive():
    """Patient `braf`/`v600e` lowercased still matches uppercase cell."""
    ents = _make_cell("BIO-BRAF-V600E", "V600E", "DIS-CRC")
    hits = find_matching_actionability({"braf": "v600e"}, "DIS-CRC", ents)
    assert len(hits) == 1


def test_match_gene_level_cell_matches_any_variant():
    """Cell with variant_qualifier=None matches any patient variant of the gene."""
    ents = _make_cell("BIO-BRCA1", None, "DIS-OVARIAN")
    hits = find_matching_actionability(
        {"BRCA1": "some weird novel variant"}, "DIS-OVARIAN", ents
    )
    assert len(hits) == 1


def test_no_match_negative_value():
    """Patient with explicit negative value should not pull any cell."""
    ents = _make_cell("BIO-BRAF-V600E", "V600E", "DIS-CRC")
    assert find_matching_actionability({"BRAF": "negative"}, "DIS-CRC", ents) == []
    assert find_matching_actionability({"BRAF": False}, "DIS-CRC", ents) == []
    assert find_matching_actionability({"BRAF": "wildtype"}, "DIS-CRC", ents) == []


def test_no_match_different_disease():
    """A cell tagged for DIS-MELANOMA must not be returned for a DIS-CRC patient."""
    ents = _make_cell("BIO-BRAF-V600E", "V600E", "DIS-MELANOMA")
    assert find_matching_actionability({"BRAF": "V600E"}, "DIS-CRC", ents) == []


# Bonus low-level helper coverage — gives clear diagnostics if a refactor breaks.


def test_normalize_gene_stem():
    assert _normalize_gene_stem("BRAF") == "BRAF"
    assert _normalize_gene_stem("braf") == "BRAF"
    assert _normalize_gene_stem("BIO-BRAF-V600E") == "BRAF"
    assert _normalize_gene_stem("BIO-EGFR-T790M") == "EGFR"


def test_extract_variant_handles_falsy_and_positive():
    assert _extract_variant(False) is None
    assert _extract_variant(None) is None
    assert _extract_variant("negative") is None
    assert _extract_variant("wildtype") is None
    assert _extract_variant("") is None
    assert _extract_variant(True) == ""           # gene-level positive
    assert _extract_variant("positive") == ""     # gene-level positive
    assert _extract_variant("V600E") == "V600E"
    assert _extract_variant({"variant": "T790M"}) == "T790M"


def test_biomarker_keys_match_token_logic():
    assert _biomarker_keys_match("BRAF", "BIO-BRAF-V600E")
    assert _biomarker_keys_match("EGFR", "BIO-EGFR-MUTATION")
    assert _biomarker_keys_match("BIO-BRAF-V600E", "BIO-BRAF-V600E")
    assert not _biomarker_keys_match("KRAS", "BIO-BRAF-V600E")


def test_variant_matches_lenient():
    assert _variant_matches("V600E", "V600E")
    assert _variant_matches("p.V600E", "V600E")
    assert _variant_matches("v600e", "V600E")
    assert _variant_matches(None, None)            # gene-level cell, no patient var
    assert _variant_matches("", "V600E")           # patient gene-level positive
    assert not _variant_matches("V600K", "V600E")


# ─────────────────────────────────────────────────────────────────────────
# Section D — End-to-end known cases (5 fixtures)
# ─────────────────────────────────────────────────────────────────────────


def _load_fixture(name: str) -> dict:
    path = FIXTURES_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def _hit_by_bma_id(plan, bma_id: str):
    for h in plan.variant_actionability:
        if h.bma_id == bma_id:
            return h
    return None


def test_case_1_braf_v600e_mcrc():
    patient = _load_fixture("csd_1_braf_v600e_mcrc.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.disease_id == "DIS-CRC"
    assert result.plan is not None
    assert not [w for w in result.warnings if "actionability" in w.lower()]

    hit = _hit_by_bma_id(result.plan, "BMA-BRAF-V600E-CRC")
    assert hit is not None, (
        f"Expected BMA-BRAF-V600E-CRC; got {[h.bma_id for h in result.plan.variant_actionability]}"
    )
    assert hit.escat_tier == "IB"
    assert hit.primary_sources, "primary_sources should be non-empty"
    assert any("encorafenib" in c.lower() for c in hit.recommended_combinations)


def test_case_2_egfr_t790m_nsclc():
    patient = _load_fixture("csd_1_egfr_t790m_nsclc.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.disease_id == "DIS-NSCLC"
    assert result.plan is not None

    hit = _hit_by_bma_id(result.plan, "BMA-EGFR-T790M-NSCLC")
    assert hit is not None, (
        f"Expected BMA-EGFR-T790M-NSCLC; got {[h.bma_id for h in result.plan.variant_actionability]}"
    )
    assert hit.escat_tier == "IA"
    assert hit.primary_sources
    assert any("osimertinib" in c.lower() for c in hit.recommended_combinations)


def test_case_3_brca1_germline_ovarian():
    patient = _load_fixture("csd_1_brca1_germline_ovarian.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.disease_id == "DIS-OVARIAN"
    assert result.plan is not None

    hit = _hit_by_bma_id(result.plan, "BMA-BRCA1-GERMLINE-OVARIAN")
    assert hit is not None, (
        f"Expected BMA-BRCA1-GERMLINE-OVARIAN; got {[h.bma_id for h in result.plan.variant_actionability]}"
    )
    assert hit.escat_tier == "IA"
    assert hit.primary_sources
    assert any("olaparib" in c.lower() for c in hit.recommended_combinations)


def test_case_4_kras_g12c_nsclc():
    patient = _load_fixture("csd_1_kras_g12c_nsclc.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.disease_id == "DIS-NSCLC"
    assert result.plan is not None

    hit = _hit_by_bma_id(result.plan, "BMA-KRAS-G12C-NSCLC")
    assert hit is not None, (
        f"Expected BMA-KRAS-G12C-NSCLC; got {[h.bma_id for h in result.plan.variant_actionability]}"
    )
    assert hit.escat_tier == "IA"
    assert hit.primary_sources
    assert any(
        "sotorasib" in c.lower() or "adagrasib" in c.lower()
        for c in hit.recommended_combinations
    )


def test_case_5_alk_fusion_nsclc_substitution():
    """NTRK-FUSION-IFS does not exist in the KB; substituted with
    BMA-ALK-FUSION-NSCLC as the closest pan-tumor TKI-targeted IA/Level-1
    actionability cell available. See fixture comment."""
    patient = _load_fixture("csd_1_ntrk_fusion_ifs.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.disease_id == "DIS-NSCLC"
    assert result.plan is not None

    hit = _hit_by_bma_id(result.plan, "BMA-ALK-FUSION-NSCLC")
    assert hit is not None, (
        f"Expected BMA-ALK-FUSION-NSCLC; got {[h.bma_id for h in result.plan.variant_actionability]}"
    )
    assert hit.escat_tier == "IA"
    assert hit.primary_sources
    assert any(
        "alectinib" in c.lower() or "lorlatinib" in c.lower() or "brigatinib" in c.lower()
        for c in hit.recommended_combinations
    )


# ─────────────────────────────────────────────────────────────────────────
# Section E — Render output
# ─────────────────────────────────────────────────────────────────────────


def test_render_html_includes_tier_badges():
    """End-to-end render check: the actionability table emits ESCAT
    tier-badge spans with the expected CSS classes (escat-IB for the
    BRAF V600E mCRC case). The OncoKB-level badge column was removed
    in Phase 1 of the CIViC pivot; per-source levels now render via
    the `evidence-sources` <ul>."""
    patient = _load_fixture("csd_1_braf_v600e_mcrc.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    html = render_plan_html(result)
    assert "tier-badge" in html, "Expected tier-badge CSS class in rendered HTML"
    assert "escat-IB" in html, (
        "Expected escat-IB badge class for BRAF V600E mCRC"
    )
