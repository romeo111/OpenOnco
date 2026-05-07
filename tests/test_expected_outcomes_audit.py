from scripts.audit_expected_outcomes import (
    LEGACY_UNCITED_SOURCE_ID,
    build_remediation_backlog,
    classify_indication,
)


def test_audit_treats_outcome_value_source_as_cited_when_on_indication_sources():
    stats = classify_indication(
        {
            "id": "IND-TEST",
            "applicable_to": {"disease_id": "DIS-TEST"},
            "sources": [{"source_id": "SRC-TRIAL-1"}],
            "expected_outcomes": {
                "progression_free_survival": {
                    "value": "Median 12 months",
                    "source": "SRC-TRIAL-1",
                }
            },
        },
        {"SRC-TRIAL-1": "trial 1"},
    )

    row = next(c for c in stats.classifications if c.field_name == "progression_free_survival")
    assert row.bucket == "cited"
    assert row.matched_via == "OutcomeValue.source: SRC-TRIAL-1"


def test_audit_keeps_legacy_placeholder_in_uncited_backlog():
    stats = classify_indication(
        {
            "id": "IND-TEST",
            "applicable_to": {"disease_id": "DIS-TEST"},
            "sources": [{"source_id": "SRC-TRIAL-1"}],
            "expected_outcomes": {
                "overall_response_rate": {
                    "value": "75%",
                    "source": LEGACY_UNCITED_SOURCE_ID,
                }
            },
        },
        {
            "SRC-TRIAL-1": "trial 1",
            LEGACY_UNCITED_SOURCE_ID: "legacy uncited placeholder",
        },
    )

    backlog = build_remediation_backlog([stats])
    assert backlog[0]["bucket"] == "uncited"
    assert "SRC-LEGACY-UNCITED" in backlog[0]["remediation_hint"]
