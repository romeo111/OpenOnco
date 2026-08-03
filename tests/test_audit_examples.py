from __future__ import annotations

from scripts.audit_examples import audit_examples
from scripts.site_cases import CASES, QUARANTINED_CASE_IDS


def test_example_registry_has_structured_publication_metadata():
    assert QUARANTINED_CASE_IDS
    assert all(case.visibility in {"public", "internal"} for case in CASES)
    assert all(case.quality_tier for case in CASES)
    assert all(case.scenario_type for case in CASES)
    assert all(
        case.visibility == "internal" for case in CASES if case.case_id in QUARANTINED_CASE_IDS
    )


def test_public_example_audit_passes_and_all_bma_profiles_are_registered():
    report = audit_examples()
    assert report["summary"]["failed"] == 0
    assert report["summary"]["unregistered_bma_profiles"] == 0
    assert report["summary"]["by_quality_tier"]["molecular"] >= 100
