"""Tier 2 biomarker enrichment — 8 more cross-disease standalone entities
on top of TP53 (Tier 0) and the Tier 1 block (BCL2/IGHV/CD5/etc).

Coverage: targeted-therapy markers (EZH2, ALK, PD-L1, CD52),
disease-defining markers (RHOA G17V for AITL, BCL6 rearrangement for
HGBL triple-hit completeness, CXCR4 for WM, NOTCH1 for CLL adverse).
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def _ents() -> dict:
    return load_content(KB_ROOT).entities_by_id


_TIER2_BIOMARKERS = [
    "BIO-EZH2-Y641",
    "BIO-ALK-REARRANGEMENT",
    "BIO-CXCR4-WHIM",
    "BIO-RHOA-G17V",
    "BIO-BCL6-REARRANGEMENT",
    "BIO-CD52-IHC",
    "BIO-PDL1-EXPRESSION",
    "BIO-NOTCH1-MUTATION",
]


def test_all_tier2_biomarkers_load():
    ents = _ents()
    missing = [bid for bid in _TIER2_BIOMARKERS if bid not in ents]
    assert not missing, f"missing Tier 2 biomarker entities: {missing}"


def test_each_tier2_biomarker_has_required_fields():
    ents = _ents()
    for bid in _TIER2_BIOMARKERS:
        d = ents[bid]["data"]
        assert d.get("biomarker_type"), f"{bid}: missing biomarker_type"
        assert (d.get("names") or {}).get("preferred"), f"{bid}: no preferred name"
        assert d.get("sources"), f"{bid}: no sources cited"
        assert d.get("notes"), f"{bid}: no notes block"


def test_double_hit_now_lists_bcl6_via_related():
    """Triple-hit completeness — BIO-DOUBLE-HIT now references all 3
    component rearrangements: MYC, BCL2, BCL6."""
    ents = _ents()
    related = set(ents["BIO-DOUBLE-HIT"]["data"].get(
        "related_biomarkers") or [])
    assert {"BIO-MYC-REARRANGEMENT", "BIO-BCL2-REARRANGEMENT",
            "BIO-BCL6-REARRANGEMENT"} <= related


def test_cll_composite_lists_notch1():
    ents = _ents()
    related = set(ents["BIO-CLL-HIGH-RISK-GENETICS"]["data"].get(
        "related_biomarkers") or [])
    assert "BIO-NOTCH1-MUTATION" in related


def test_myd88_links_to_cxcr4_for_wm_modifier():
    ents = _ents()
    related = set(ents["BIO-MYD88-L265P"]["data"].get(
        "related_biomarkers") or [])
    assert "BIO-CXCR4-WHIM" in related


def test_alk_notes_explain_alcl_stratification():
    """ALK status defines major prognostic split within ALCL — notes
    should explain ALK+ vs ALK- difference."""
    ents = _ents()
    notes = ents["BIO-ALK-REARRANGEMENT"]["data"].get("notes", "").lower()
    assert "alk+" in notes and "alk-" in notes
    assert "alcl" in notes


def test_ezh2_notes_mention_tazemetostat():
    """EZH2 standalone entity must mention tazemetostat targeted therapy."""
    ents = _ents()
    notes = ents["BIO-EZH2-Y641"]["data"].get("notes", "").lower()
    assert "tazemetostat" in notes


def test_pdl1_notes_mention_chl_and_pmbcl():
    ents = _ents()
    notes = ents["BIO-PDL1-EXPRESSION"]["data"].get("notes", "").lower()
    assert "chl" in notes or "hodgkin" in notes
    assert "pmbcl" in notes or "mediastinal" in notes


def test_bcl6_links_to_other_rearrangement_components():
    """BCL6 must cite MYC + BCL2 + DOUBLE-HIT in related_biomarkers
    (it's the third component)."""
    ents = _ents()
    related = set(ents["BIO-BCL6-REARRANGEMENT"]["data"].get(
        "related_biomarkers") or [])
    assert {"BIO-MYC-REARRANGEMENT", "BIO-BCL2-REARRANGEMENT",
            "BIO-DOUBLE-HIT"} <= related
