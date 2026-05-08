from __future__ import annotations

from knowledge_base.engine.civic_evidence_lanes import (
    EvidenceLane,
    classify_civic_evidence_item,
    classify_civic_evidence_source_ref,
    summarize_lanes,
    standard_care_confirming_source_ids,
)


def _item(**overrides):
    base = {
        "id": "123",
        "evidence_level": "A",
        "evidence_type": "Predictive",
        "evidence_direction": "Supports",
        "significance": "Sensitivity/Response",
        "therapies": ["Vemurafenib"],
        "citation_id": "21639808",
    }
    base.update(overrides)
    return base


def test_civic_only_high_predictive_evidence_is_molecular_option():
    decision = classify_civic_evidence_item(_item())

    assert decision.lane == EvidenceLane.MOLECULAR_EVIDENCE_OPTION
    assert "not standard care" in decision.reason
    assert "SRC-CIVIC-EID-123" in decision.source_ids


def test_standard_care_requires_explicit_non_civic_confirmation():
    decision = classify_civic_evidence_item(
        _item(),
        standard_care_confirmed=True,
        standard_care_source_ids=("SRC-FDA-LABEL-BRAF",),
    )

    assert decision.lane == EvidenceLane.STANDARD_CARE
    assert "SRC-FDA-LABEL-BRAF" in decision.source_ids


def test_does_not_support_is_resistance_lane():
    decision = classify_civic_evidence_item(
        _item(evidence_direction="Does Not Support")
    )

    assert decision.lane == EvidenceLane.RESISTANCE_OR_AVOIDANCE_SIGNAL


def test_resistance_significance_is_resistance_lane():
    decision = classify_civic_evidence_item(_item(significance="Resistance"))

    assert decision.lane == EvidenceLane.RESISTANCE_OR_AVOIDANCE_SIGNAL


def test_lower_tier_predictive_evidence_routes_to_trial_research():
    decision = classify_civic_evidence_item(_item(evidence_level="D"))

    assert decision.lane == EvidenceLane.TRIAL_RESEARCH_OPTION


def test_non_predictive_evidence_does_not_create_treatment_option():
    decision = classify_civic_evidence_item(
        _item(evidence_type="Diagnostic", significance="Positive")
    )

    assert decision.lane == EvidenceLane.INSUFFICIENT_EVIDENCE


def test_no_therapy_attached_is_insufficient_even_if_predictive():
    decision = classify_civic_evidence_item(_item(therapies=[]))

    assert decision.lane == EvidenceLane.INSUFFICIENT_EVIDENCE


def test_bucketed_evidence_source_ref_classification_for_reports():
    decision = classify_civic_evidence_source_ref(
        {
            "source": "SRC-CIVIC",
            "level": "B",
            "evidence_ids": ["5"],
            "direction": "Does Not Support",
            "significance": "Sensitivity/Response",
            "note": "therapies: Cetuximab",
        }
    )

    assert decision.lane == EvidenceLane.RESISTANCE_OR_AVOIDANCE_SIGNAL
    assert decision.source_ids == ("SRC-CIVIC-EID-5",)


def test_bucketed_evidence_source_ref_prefers_persisted_lane():
    decision = classify_civic_evidence_source_ref(
        {
            "source": "SRC-CIVIC",
            "level": "B",
            "evidence_lane": "standard_care",
            "evidence_ids": ["5"],
            "direction": "Supports",
            "significance": "Sensitivity/Response",
        }
    )

    assert decision.lane == EvidenceLane.STANDARD_CARE
    assert decision.source_ids == ("SRC-CIVIC-EID-5",)


def test_summarize_lanes_is_stable_and_unique():
    decisions = [
        classify_civic_evidence_item(_item(evidence_level="D")),
        classify_civic_evidence_item(_item()),
        classify_civic_evidence_item(_item(evidence_level="D")),
    ]

    assert summarize_lanes(decisions) == (
        "molecular_evidence_option",
        "trial_research_option",
    )


def test_standard_care_confirmation_helper_accepts_guideline_and_regulatory_sources():
    source_ids = standard_care_confirming_source_ids(
        evidence_sources=[
            {"source": "SRC-CIVIC"},
            {"source": "SRC-FDA-LABEL-BRAF"},
            {"source": "SRC-ONCOKB"},
        ],
        primary_sources=["SRC-NCCN-CRC-2026", "SRC-CIVIC"],
    )

    assert source_ids == ("SRC-FDA-LABEL-BRAF", "SRC-NCCN-CRC-2026")


def test_standard_care_confirmation_helper_rejects_civic_and_literature_only():
    source_ids = standard_care_confirming_source_ids(
        evidence_sources=[{"source": "SRC-CIVIC"}],
        primary_sources=["SRC-PMID-12345", "SRC-ONCOKB"],
    )

    assert source_ids == ()
