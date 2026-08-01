"""Prior-therapy discriminator: deriving scalar findings from prior_lines.

`findings.prior_lines` is a list and the RedFlag clause evaluator resolves
flat scalars only, so before this derivation no `finding:` clause could
express "the prior line was osimertinib". These tests pin the derivation
contract, and in particular the absence-vs-recorded-false boundary.
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine.prior_therapy import (
    build_drug_index,
    derive_prior_therapy_findings,
)
from knowledge_base.engine.redflag_eval import evaluate_redflag_trigger
from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _entities(*drugs: dict) -> dict:
    return {d["id"]: {"type": "drugs", "data": d} for d in drugs}


OSIMERTINIB = {
    "id": "DRUG-OSIMERTINIB",
    "names": {"preferred": "Osimertinib", "brand_names": ["Tagrisso"]},
    "drug_class": "3rd-generation EGFR TKI (T790M-active)",
}
ERLOTINIB = {
    "id": "DRUG-ERLOTINIB",
    "names": {"preferred": "Erlotinib", "brand_names": ["Tarceva"]},
    "drug_class": "1st-generation EGFR TKI (reversible)",
}
SORAFENIB = {
    "id": "DRUG-SORAFENIB",
    "names": {"preferred": "Sorafenib", "brand_names": ["Nexavar"]},
    "drug_class": "Multi-targeted oral tyrosine kinase inhibitor (VEGFR1-3, PDGFR)",
}
PEMBROLIZUMAB = {
    "id": "DRUG-PEMBROLIZUMAB",
    "names": {"preferred": "Pembrolizumab", "brand_names": ["Keytruda"]},
    "drug_class": "Anti-PD-1 monoclonal antibody",
}

INDEX = build_drug_index(_entities(OSIMERTINIB, ERLOTINIB, SORAFENIB, PEMBROLIZUMAB))


# ── Absence vs recorded-false ────────────────────────────────────────────
# The distinction the whole discriminator rests on: a patient with no
# recorded prior therapy must stay unknown, never become a recorded false.


def test_prior_lines_absent_derives_nothing():
    assert derive_prior_therapy_findings({"stage_iv": True}, INDEX) == {}


def test_prior_lines_none_derives_nothing():
    assert derive_prior_therapy_findings({"prior_lines": None}, INDEX) == {}


def test_prior_lines_empty_list_derives_nothing():
    assert derive_prior_therapy_findings({"prior_lines": []}, INDEX) == {}


def test_prior_lines_as_integer_count_derives_nothing():
    """`patient_melanoma_nivo_relatlimab.json` records prior_lines as a
    count (`1`), which names no drug. Deriving `prior_osimertinib: false`
    from it would assert something the profile does not say."""
    assert derive_prior_therapy_findings({"prior_lines": 1}, INDEX) == {}


def test_recorded_prior_therapy_is_marked_distinctly_from_absence():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "erlotinib"}]}, INDEX
    )
    assert derived["prior_therapy_recorded"] is True
    assert derived["prior_osimertinib"] is False  # recorded-false, not unknown


# ── The discriminator ────────────────────────────────────────────────────


def test_osimertinib_naive_prior_egfr_tki():
    derived = derive_prior_therapy_findings(
        {
            "prior_lines": [
                {
                    "line": 1,
                    "regimen": "erlotinib",
                    "best_response": "PR",
                    "outcome": "PD with acquired T790M",
                }
            ]
        },
        INDEX,
    )
    assert derived["prior_egfri_received"] is True
    assert derived["prior_osimertinib"] is False
    assert derived["prior_egfri_progression"] is True
    assert derived["best_response_to_egfri"] == "PR"


def test_post_osimertinib_is_distinguishable():
    derived = derive_prior_therapy_findings(
        {
            "prior_lines": [
                {"line": 1, "regimen": "osimertinib 80 mg PO daily", "outcome": "PD at 14 mo"}
            ]
        },
        INDEX,
    )
    assert derived["prior_osimertinib"] is True
    assert derived["prior_egfri_received"] is True


def test_brand_name_resolves_to_the_same_drug():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "Tagrisso"}]}, INDEX
    )
    assert derived["prior_osimertinib"] is True


def test_multiple_prior_lines_are_all_considered():
    derived = derive_prior_therapy_findings(
        {
            "prior_lines": [
                {"line": 1, "regimen": "pembrolizumab", "outcome": "PD at 6 mo"},
                {"line": 2, "regimen": "erlotinib", "outcome": "PD at 11 mo"},
            ]
        },
        INDEX,
    )
    assert derived["prior_drug_ids"] == ["DRUG-ERLOTINIB", "DRUG-PEMBROLIZUMAB"]
    assert derived["prior_egfri_received"] is True
    assert derived["prior_osimertinib"] is False


def test_progression_taken_from_best_response_field():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "erlotinib", "best_response": "PD"}]},
        INDEX,
    )
    assert derived["prior_egfri_progression"] is True


def test_non_egfr_prior_line_does_not_set_egfri_flags():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "pembrolizumab", "outcome": "PD at 6 mo"}]},
        INDEX,
    )
    assert derived["prior_egfri_received"] is False
    assert derived["prior_egfri_progression"] is False
    assert "best_response_to_egfri" not in derived


# ── Free-text robustness ─────────────────────────────────────────────────
# 18 of the 36 prior_lines-carrying profiles author plain strings, not dicts.


def test_list_of_strings_shape_is_supported():
    derived = derive_prior_therapy_findings(
        {"prior_lines": ["erlotinib 150 mg PO daily → PD at 18 mo"]}, INDEX
    )
    assert derived["prior_egfri_received"] is True
    assert derived["prior_egfri_progression"] is True


def test_unknown_drug_name_is_surfaced_and_fails_safe():
    derived = derive_prior_therapy_findings({"prior_lines": ["CHOEP x6"]}, INDEX)
    assert derived["prior_therapy_unmatched_lines"] == ["CHOEP x6"]
    assert derived["prior_egfri_received"] is False
    assert derived["prior_osimertinib"] is False


def test_drug_name_is_not_matched_inside_a_longer_word():
    derived = derive_prior_therapy_findings({"prior_lines": ["superosimertinibase"]}, INDEX)
    assert derived["prior_osimertinib"] is False


def test_vegfr_inhibitor_is_not_read_as_egfr_directed():
    """`VEGFR` contains the substring `EGFR`. Ten catalogue drug_class
    strings match "EGFR" naively but are multi-kinase VEGFR inhibitors."""
    assert "DRUG-SORAFENIB" not in INDEX.egfr_directed
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "sorafenib", "outcome": "PD at 5 mo"}]},
        INDEX,
    )
    assert derived["prior_egfri_received"] is False


def test_pd_l1_is_not_read_as_progressive_disease():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [{"line": 1, "regimen": "erlotinib", "outcome": "PD-L1 TPS 10%"}]},
        INDEX,
    )
    assert derived["prior_egfri_progression"] is False


def test_malformed_entries_are_skipped_not_fatal():
    derived = derive_prior_therapy_findings(
        {"prior_lines": [None, 42, {}, {"line": 1, "regimen": "erlotinib"}]}, INDEX
    )
    assert derived["prior_egfri_received"] is True


# ── Catalogue-driven index ───────────────────────────────────────────────


def test_real_catalogue_classifies_egfr_directed_drugs():
    entities = load_content(KB_ROOT).entities_by_id
    index = build_drug_index(entities)
    assert "DRUG-OSIMERTINIB" in index.egfr_directed
    assert "DRUG-ERLOTINIB" in index.egfr_directed
    assert "DRUG-CETUXIMAB" in index.egfr_directed
    # VEGFR multi-kinase inhibitors must not leak in via substring match.
    assert "DRUG-LENVATINIB" not in index.egfr_directed
    assert "DRUG-REGORAFENIB" not in index.egfr_directed


# ── End to end: the previously inert universal RedFlag ───────────────────


def test_universal_prior_egfri_redflag_fires_on_the_t790m_showcase():
    """RF-PRIOR-EGFRI-PROGRESSION triggers on scalars that no example
    profile authors, so it could never fire. The derivation revives it."""
    entities = load_content(KB_ROOT).entities_by_id
    index = build_drug_index(entities)
    rf = next(
        info["data"]
        for info in entities.values()
        if info["type"] == "redflags"
        and info["data"].get("id") == "RF-PRIOR-EGFRI-PROGRESSION"
    )
    profile = json.loads(
        (EXAMPLES / "patient_showcase_nsclc_egfr_t790m_2l.json").read_text(encoding="utf-8")
    )
    findings = dict(profile["findings"])

    assert evaluate_redflag_trigger(rf["trigger"], findings) is False

    findings.update(derive_prior_therapy_findings(findings, index))
    assert evaluate_redflag_trigger(rf["trigger"], findings) is True


def test_authored_findings_win_over_derived_values():
    """Derived keys are merged with setdefault, so a profile that states a
    prior-therapy scalar explicitly keeps its authored value."""
    from knowledge_base.engine.plan import _flatten_findings

    entities = _entities(OSIMERTINIB, ERLOTINIB)
    patient = {
        "findings": {
            "prior_lines": [{"line": 1, "regimen": "osimertinib"}],
            "prior_osimertinib": False,
        }
    }
    findings = _flatten_findings(patient, entities)
    assert findings["prior_osimertinib"] is False


def test_flatten_without_entities_derives_nothing():
    """Back-compat: callers that pass no entities get the old behaviour."""
    from knowledge_base.engine.plan import _flatten_findings

    patient = {"findings": {"prior_lines": [{"line": 1, "regimen": "osimertinib"}]}}
    assert "prior_osimertinib" not in _flatten_findings(patient)
