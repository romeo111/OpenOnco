"""Indication schema — Phase 2 OutcomeValue migration tests.

Pivotal Trial Outcomes Ingestion Plan
(`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`)
Phase 2 introduces ``OutcomeValue`` (citation-bearing wrapper) and a
``mode='before'`` field validator on ``ExpectedOutcomes`` that coerces
plain-string outcome values (the legacy YAML shape carried by all 312
indications today) into ``OutcomeValue(value=str, source='SRC-LEGACY-UNCITED')``
so the loader stays green without forcing a same-PR rewrite of every
indication YAML.

These tests pin the contract: legacy strings, dict-shaped values, and
mixed shapes inside one ``ExpectedOutcomes`` block all load without
error. They also pin the two new fields the plan calls out
(``overall_survival_median``, ``disease_free_survival_hr``).

The full-KB integrity check ("all 312 indications still load and the
audit's bucket counts haven't drifted") is exercised by the existing
``tests/test_loader.py`` and the manual ``audit_expected_outcomes.py``
re-run; the tests here are pure schema-level.
"""

from __future__ import annotations

import pytest

from knowledge_base.schemas.indication import (
    LEGACY_UNCITED_SOURCE_ID,
    ExpectedOutcomes,
    OutcomeValue,
)


# ── Legacy-string coercion ───────────────────────────────────────────────────


def test_plain_string_coerces_to_outcome_value_with_legacy_source():
    eo = ExpectedOutcomes.model_validate(
        {"overall_response_rate": "75% (PATHFINDER advanced SM)"}
    )
    orr = eo.overall_response_rate
    assert isinstance(orr, OutcomeValue)
    assert orr.value == "75% (PATHFINDER advanced SM)"
    assert orr.source == LEGACY_UNCITED_SOURCE_ID
    assert orr.confidence_interval is None
    assert orr.median_followup_months is None


def test_legacy_source_id_constant_is_canonical():
    """The placeholder SRC id is a public symbol — render layer + audit
    + loader all reference it. Pin the literal so a typo on either side
    surfaces here, not as a silent reference-resolution failure."""
    assert LEGACY_UNCITED_SOURCE_ID == "SRC-LEGACY-UNCITED"


# ── Dict-shape (Phase 2 native) values ───────────────────────────────────────


def test_dict_shape_outcome_value_loads_full_record():
    eo = ExpectedOutcomes.model_validate(
        {
            "progression_free_survival": {
                "value": "5.5 months",
                "source": "SRC-KEYNOTE-006",
                "confidence_interval": "95% CI 4.7-6.5",
                "median_followup_months": 33.7,
            }
        }
    )
    pfs = eo.progression_free_survival
    assert isinstance(pfs, OutcomeValue)
    assert pfs.value == "5.5 months"
    assert pfs.source == "SRC-KEYNOTE-006"
    assert pfs.confidence_interval == "95% CI 4.7-6.5"
    assert pfs.median_followup_months == pytest.approx(33.7)


def test_dict_shape_minimum_fields_only():
    """Only ``value`` + ``source`` are required on OutcomeValue; the
    optional CI / follow-up fields default to None."""
    eo = ExpectedOutcomes.model_validate(
        {
            "complete_response": {
                "value": "33-40%",
                "source": "SRC-EXTREME-VERMORKEN-2008",
            }
        }
    )
    cr = eo.complete_response
    assert isinstance(cr, OutcomeValue)
    assert cr.value == "33-40%"
    assert cr.source == "SRC-EXTREME-VERMORKEN-2008"
    assert cr.confidence_interval is None
    assert cr.median_followup_months is None


# ── Mixed shapes inside one ExpectedOutcomes block ───────────────────────────


def test_mixed_string_and_dict_shapes_in_one_block():
    """Indications mid-migration may carry some Phase-2 dicts alongside
    legacy strings. Both must load."""
    eo = ExpectedOutcomes.model_validate(
        {
            # Legacy string — coerces to SRC-LEGACY-UNCITED.
            "overall_response_rate": "~75%",
            # Phase-2 native dict — kept as-authored.
            "progression_free_survival": {
                "value": "Median not reached (24-mo follow-up)",
                "source": "SRC-PATHFINDER-DEANGELO-2023",
            },
            # None — stays absent.
            "overall_survival_5y": None,
        }
    )
    assert isinstance(eo.overall_response_rate, OutcomeValue)
    assert eo.overall_response_rate.source == LEGACY_UNCITED_SOURCE_ID

    assert isinstance(eo.progression_free_survival, OutcomeValue)
    assert eo.progression_free_survival.source == "SRC-PATHFINDER-DEANGELO-2023"
    assert eo.progression_free_survival.value.startswith("Median not reached")

    assert eo.overall_survival_5y is None


# ── Phase-2 newly-added fields ───────────────────────────────────────────────


def test_overall_survival_median_field_is_present():
    """`overall_survival_median` is one of the two new fields the plan
    calls out — schema must accept it both as legacy string and dict."""
    legacy = ExpectedOutcomes.model_validate(
        {"overall_survival_median": "26.4 months"}
    )
    assert isinstance(legacy.overall_survival_median, OutcomeValue)
    assert legacy.overall_survival_median.value == "26.4 months"
    assert legacy.overall_survival_median.source == LEGACY_UNCITED_SOURCE_ID

    native = ExpectedOutcomes.model_validate(
        {
            "overall_survival_median": {
                "value": "26.4 months",
                "source": "SRC-CHECKMATE-577-KELLY-2021",
            }
        }
    )
    assert native.overall_survival_median.source == "SRC-CHECKMATE-577-KELLY-2021"


def test_disease_free_survival_hr_field_is_present():
    """`disease_free_survival_hr` is the adjuvant-trial readout the plan
    adds — used by KEYNOTE-054, APHINITY, etc."""
    eo = ExpectedOutcomes.model_validate(
        {
            "disease_free_survival_hr": {
                "value": "HR 0.81 (p=0.045)",
                "source": "SRC-APHINITY-VONMINCKWITZ-2017",
                "confidence_interval": "95% CI 0.66-1.00",
            }
        }
    )
    dfs = eo.disease_free_survival_hr
    assert isinstance(dfs, OutcomeValue)
    assert dfs.value == "HR 0.81 (p=0.045)"
    assert dfs.source == "SRC-APHINITY-VONMINCKWITZ-2017"
    assert dfs.confidence_interval == "95% CI 0.66-1.00"


# ── Disease-specific extras (extra='allow') stay untouched ───────────────────


def test_disease_specific_extras_pass_through_without_coercion():
    """`Base.extra='allow'` admits disease-specific outcome fields
    (``hcv_cure_rate_svr12`` is the only schema-declared example, but
    indications in the wild carry e.g. ``median_overall_survival_months``,
    ``time_to_treatment_failure_months``, ``svr_at_12_weeks``…). The
    Phase-2 validator deliberately does NOT coerce these — they keep
    whatever shape the YAML author wrote until a future migration
    formalizes each one. Phase 2 scope is bounded to schema-declared
    fields only."""
    eo = ExpectedOutcomes.model_validate(
        {
            "median_overall_survival_months": 46,
            "time_to_treatment_failure_months": "12.4",
            "notes": "KEYNOTE-426 5-yr update (Rini, ASCO 2024)",
        }
    )
    # Extras are accessible via model_extra; not coerced to OutcomeValue.
    assert eo.model_extra is not None
    assert eo.model_extra["median_overall_survival_months"] == 46
    assert eo.model_extra["time_to_treatment_failure_months"] == "12.4"
    assert "KEYNOTE-426" in eo.model_extra["notes"]


# ── All-fields-absent empty block stays valid ────────────────────────────────


def test_empty_expected_outcomes_block_is_valid():
    """An indication can legitimately publish an empty
    ``expected_outcomes`` block (e.g. supportive-care indications where
    no RCT readout applies). All seven schema fields default to None."""
    eo = ExpectedOutcomes.model_validate({})
    assert eo.overall_response_rate is None
    assert eo.complete_response is None
    assert eo.progression_free_survival is None
    assert eo.overall_survival_5y is None
    assert eo.overall_survival_median is None
    assert eo.disease_free_survival_hr is None
    assert eo.hcv_cure_rate_svr12 is None
