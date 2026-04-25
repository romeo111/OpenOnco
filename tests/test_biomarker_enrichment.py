"""Cross-disease biomarker enrichment block — verifies the 10 new
standalone marker entities load correctly + key cross-wirings work
end-to-end.

This block extends the TP53 standalone pattern to: BCL2 expression,
BCL2 rearrangement, IGHV mutational status, CD5, CD23, cyclin D1,
t(11;14) IGH/CCND1, EBV, Ki-67, CD79b. Each gets a dedicated entity
with cross-disease notes + related_biomarkers wiring; the most
algorithm-impactful (IGHV → CLL routing, Ki-67 → MCL routing) get
direct trigger findings on the relevant RedFlags.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.engine import generate_plan
from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def _ents() -> dict:
    return load_content(KB_ROOT).entities_by_id


# ── Entity presence + structural contract ────────────────────────────────


_NEW_BIOMARKERS = [
    "BIO-BCL2-EXPRESSION-IHC",
    "BIO-BCL2-REARRANGEMENT",
    "BIO-IGHV-MUTATIONAL-STATUS",
    "BIO-CD5-IHC",
    "BIO-CD23-IHC",
    "BIO-CCND1-IHC",
    "BIO-T11-14-IGH-CCND1",
    "BIO-EBV-STATUS",
    "BIO-KI67-PROLIFERATION-INDEX",
    "BIO-CD79B-IHC",
]


def test_all_new_biomarker_entities_load():
    ents = _ents()
    missing = [bid for bid in _NEW_BIOMARKERS if bid not in ents]
    assert not missing, f"missing biomarker entities: {missing}"


def test_each_new_biomarker_has_required_fields():
    ents = _ents()
    for bid in _NEW_BIOMARKERS:
        d = ents[bid]["data"]
        assert d.get("biomarker_type"), f"{bid}: missing biomarker_type"
        assert (d.get("names") or {}).get("preferred"), f"{bid}: no preferred name"
        assert d.get("sources"), f"{bid}: no sources cited"
        assert d.get("notes"), f"{bid}: no notes block"


# ── Cross-disease wiring through composites ──────────────────────────────


def test_cll_composite_now_lists_ighv_and_tp53():
    ents = _ents()
    related = set(ents["BIO-CLL-HIGH-RISK-GENETICS"]["data"].get(
        "related_biomarkers") or [])
    assert {"BIO-TP53-MUTATION", "BIO-IGHV-MUTATIONAL-STATUS"} <= related


def test_double_hit_composite_lists_myc_and_bcl2_components():
    ents = _ents()
    related = set(ents["BIO-DOUBLE-HIT"]["data"].get(
        "related_biomarkers") or [])
    assert {"BIO-MYC-REARRANGEMENT", "BIO-BCL2-REARRANGEMENT"} <= related


def test_bcl2_ihc_links_to_rearrangement_and_double_hit():
    ents = _ents()
    related = set(ents["BIO-BCL2-EXPRESSION-IHC"]["data"].get(
        "related_biomarkers") or [])
    assert {"BIO-BCL2-REARRANGEMENT", "BIO-DOUBLE-HIT"} <= related


def test_ccnd1_ihc_links_to_t11_14_translocation():
    ents = _ents()
    related = set(ents["BIO-CCND1-IHC"]["data"].get(
        "related_biomarkers") or [])
    assert "BIO-T11-14-IGH-CCND1" in related


# ── RedFlag wiring — IGHV in CLL + Ki67 in MCL ───────────────────────────


def test_cll_redflag_accepts_ighv_unmutated_via_new_entity():
    ents = _ents()
    rf = ents["RF-CLL-HIGH-RISK"]["data"]
    findings = {c.get("finding") for c in rf["trigger"]["any_of"]}
    assert "BIO-IGHV-MUTATIONAL-STATUS" in findings


def test_mcl_redflag_accepts_ki67_via_new_entity():
    ents = _ents()
    rf = ents["RF-MCL-BLASTOID-OR-TP53"]["data"]
    findings = {c.get("finding") for c in rf["trigger"]["any_of"]}
    assert "BIO-KI67-PROLIFERATION-INDEX" in findings


# ── End-to-end: minimal patient profiles using new entities ──────────────


def test_cll_with_only_ighv_unmutated_routes_to_veno():
    """Patient profile with ONLY IGHV-unmutated as the high-risk signal
    should route to VenO via the new direct-trigger wire."""
    patient = {
        "patient_id": "CLL-IGHV-ONLY-001",
        "disease": {"icd_o_3_morphology": "9823/3"},
        "line_of_therapy": 1,
        "biomarkers": {"BIO-IGHV-MUTATIONAL-STATUS": "unmutated"},
        "demographics": {"age": 65, "sex": "male", "ecog": 1},
        "findings": {"iwcll_treatment_indication": True},
    }
    plan = generate_plan(patient, kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-CLL"
    assert plan.default_indication_id == "IND-CLL-1L-VENO"


# ── Cross-disease relevance audit ────────────────────────────────────────


def test_bcl2_ihc_notes_mention_multiple_diseases():
    """BCL2 should be flagged as cross-disease (CLL + MCL + FL + DLBCL +
    HGBL + MM) in its notes — this is the core rationale for standalone
    entity creation."""
    ents = _ents()
    notes = ents["BIO-BCL2-EXPRESSION-IHC"]["data"].get("notes", "").lower()
    # Must mention at least 4 relevant diseases
    diseases_mentioned = sum(1 for d in ("cll", "mcl", "fl", "dlbcl", "hgbl", "mm")
                             if d in notes)
    assert diseases_mentioned >= 4, (
        f"BCL2 notes should mention multiple diseases (got {diseases_mentioned}/6)"
    )


def test_ebv_notes_mention_multiple_diseases():
    ents = _ents()
    notes = ents["BIO-EBV-STATUS"]["data"].get("notes", "").lower()
    # EBV is etiologic across many diseases
    diseases_mentioned = sum(1 for d in ("burkitt", "hodgkin", "ptld", "hiv",
                                         "nk/t", "aitl", "dlbcl")
                             if d in notes)
    assert diseases_mentioned >= 4, (
        f"EBV notes should mention multiple diseases (got {diseases_mentioned}/7)"
    )
