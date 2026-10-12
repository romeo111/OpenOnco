"""Synthetic review-provenance contracts; no production approvals are written."""
from copy import deepcopy
from datetime import date

import pytest
import yaml

from knowledge_base.engine.render import _render_signoff_badge_patient
from knowledge_base.engine._actionability import find_matching_actionability
from knowledge_base.schemas._review_readiness import eligible_signoffs
from knowledge_base.schemas.biomarker_actionability import (
    BiomarkerActionability,
    actionability_release_readiness,
)
from knowledge_base.schemas.reviewer_profile import ReviewerProfile
from scripts import clinical_signoff
from scripts.audit_escat_readiness import audit_escat_readiness
from scripts.clinical_curated_copy import messages_for
from tests.review_provenance_fixtures import authorized_profiles


def _candidate():
    return {
        "id": "BMA-TEST-CRC", "biomarker_id": "BIO-TEST", "disease_id": "DIS-CRC",
        "actionability_scope": "therapeutic_predictive", "escat_applicability": "applicable",
        "escat_tier": "IC", "last_verified": "2026-08-03",
        "escat_evidence_dossier": {
            "assessment_status": "clinically_reviewed", "tier_rationale": "Synthetic test rationale.",
            "evidence_records": [{"source": "SRC-TEST", "therapy_context": "test only",
                                  "tumour_context": "test only", "study_design": "other"}],
        },
        "evidence_summary": "Synthetic fixture, not clinical evidence.",
        "primary_sources": ["SRC-TEST"],
        "reviewer_signoffs": [
            {"reviewer_id": reviewer, "timestamp": "2026-08-03T12:00:00Z",
             "entity_version": "2026-08-03", "scope_match": True}
            for reviewer in ("REV-TEST-A", "REV-TEST-B")
        ],
    }


def _profiles():
    return authorized_profiles("REV-TEST-A", "REV-TEST-B")


def _readiness(data, profiles):
    normalized = BiomarkerActionability.model_validate(data).model_dump(mode="json")
    return actionability_release_readiness(normalized, reviewer_profiles=profiles)


def test_current_authorized_distinct_reviews_positive_control():
    data, profiles = _candidate(), _profiles()
    original = deepcopy((data, profiles))
    assert _readiness(data, profiles).ready
    assert (data, profiles) == original


@pytest.mark.parametrize("failure", ["missing_scope", "null_scope", "blank_revision", "placeholder"])
def test_normalized_reproduced_readiness_gaps_are_rejected(failure):
    data, profiles = _candidate(), _profiles()
    for signoff in data["reviewer_signoffs"]:
        if failure == "missing_scope":
            signoff.pop("scope_match")
        elif failure == "null_scope":
            signoff["scope_match"] = None
        elif failure == "blank_revision":
            signoff.pop("entity_version")
        elif failure == "placeholder":
            old_id = signoff["reviewer_id"]
            new_id = old_id + "-PLACEHOLDER"
            profiles[new_id] = profiles.pop(old_id)
            profiles[new_id]["id"] = new_id
            signoff["reviewer_id"] = new_id
    if failure == "blank_revision":
        data["last_verified"] = ""
    result = _readiness(data, profiles)
    assert not result.ready
    assert result.reasons


@pytest.mark.parametrize("status", ["pending", "revoked"])
def test_named_registered_profile_without_current_authority_is_rejected(status):
    profiles = _profiles()
    profiles["REV-TEST-B"]["authorization"]["status"] = status
    data = _candidate()
    data["reviewer_signoffs"] = data["reviewer_signoffs"][1:]
    assert not _readiness(data, profiles).ready


def test_unknown_reviewer_registry_cannot_establish_clinical_readiness():
    assert not _readiness(_candidate(), {}).ready


def test_two_accounts_of_one_person_are_one_review():
    profiles = _profiles()
    profiles["REV-TEST-B"]["authorization"]["identity_key"] = profiles["REV-TEST-A"]["authorization"]["identity_key"]
    data = _candidate()
    rows = eligible_signoffs(data, profiles, revision_field="last_verified", entity_type="BiomarkerActionability")
    assert len(rows) == 1
    assert _readiness(data, profiles).ready


@pytest.mark.parametrize("field,value", [
    ("verified_on", "not-a-date"), ("verified_on", "2099-01-01"),
    ("decision_reference", ""), ("identity_key", ""),
])
def test_incomplete_or_future_authorization_cannot_confer_readiness(field, value):
    profiles = _profiles()
    profiles["REV-TEST-B"]["authorization"][field] = value
    data = _candidate()
    data["reviewer_signoffs"] = data["reviewer_signoffs"][1:]
    assert not _readiness(data, profiles).ready


@pytest.mark.parametrize("timestamp", [
    "not-a-time", "2026-08-03T12:00:00", "2099-01-01T00:00:00Z",
    "2026-08-02T23:59:59Z",
])
def test_invalid_future_or_pre_authorization_review_is_rejected(timestamp):
    data = _candidate()
    data["reviewer_signoffs"][1]["timestamp"] = timestamp
    data["reviewer_signoffs"] = data["reviewer_signoffs"][1:]
    assert not _readiness(data, _profiles()).ready


def test_changed_current_scope_invalidates_old_affirmative_scope_flag():
    profiles = _profiles()
    profiles["REV-TEST-B"]["sign_off_scope"]["diseases_explicit"] = ["DIS-DLBCL-NOS"]
    data = _candidate()
    data["reviewer_signoffs"] = data["reviewer_signoffs"][1:]
    assert not _readiness(data, profiles).ready


@pytest.mark.parametrize("revision", ["invalid-date", "2099-01-01"])
def test_invalid_or_future_content_revision_cannot_be_ready(revision):
    data = _candidate()
    data["last_verified"] = revision
    for signoff in data["reviewer_signoffs"]:
        signoff["entity_version"] = revision
    assert not _readiness(data, _profiles()).ready


def test_two_unknown_ids_cannot_display_patient_approval():
    data = _candidate()
    data["last_reviewed"] = data["last_verified"]
    badge = _render_signoff_badge_patient(data, target_lang="en", reviewer_profiles={})
    assert "signoff-complete" not in badge
    assert "Reviewed by doctors" not in badge


def test_cli_scope_uses_canonical_type_and_explicit_disease_field():
    profile = ReviewerProfile.model_validate(_profiles()["REV-TEST-A"])
    assert clinical_signoff._scope_match(profile, {"disease_id": "DIS-CRC"}, "biomarker_actionability")[0]
    assert not clinical_signoff._scope_match(profile, {"disease_id": "DIS-DLBCL-NOS"}, "biomarker_actionability")[0]


def test_cli_scope_recognizes_declared_all_categories(monkeypatch):
    data = _profiles()["REV-TEST-A"]
    data["sign_off_scope"] = {"entity_types": ["BiomarkerActionability"], "disease_categories": ["all"]}
    profile = ReviewerProfile.model_validate(data)
    monkeypatch.setattr(clinical_signoff, "_load_disease", lambda disease_id: {"id": disease_id})
    assert clinical_signoff._scope_match(profile, {"disease_id": "DIS-CRC"}, "biomarker_actionability")[0]


def test_engine_registry_changes_review_flag_without_dropping_findings():
    data = _candidate()
    entities = {data["id"]: {"type": "biomarker_actionability", "data": data}}
    before = find_matching_actionability({"BIO-TEST": True}, "DIS-CRC", entities)
    entities.update({rid: {"type": "reviewers", "data": profile} for rid, profile in _profiles().items()})
    after = find_matching_actionability({"BIO-TEST": True}, "DIS-CRC", entities)
    assert not before[0]["clinical_use_ready"]
    assert after[0]["clinical_use_ready"]
    for key in before[0].keys() - {"clinical_use_ready", "clinical_use_reasons"}:
        assert before[0][key] == after[0][key]


def test_nested_indication_review_uses_current_authorized_context():
    data = _candidate()
    data.update(last_reviewed=data["last_verified"], applicable_to={"disease_id": "DIS-CRC"})
    data.pop("disease_id")
    badge = _render_signoff_badge_patient(data, target_lang="en", reviewer_profiles=_profiles())
    assert 'data-review-count="2"' in badge
    assert "Current clinical-content review recorded" in badge
    assert "approved" not in badge.lower()


def test_multi_disease_record_requires_scope_for_every_disease():
    data = _candidate()
    data.update(last_reviewed=data["last_verified"], relevant_diseases=["DIS-CRC", "DIS-DLBCL-NOS"])
    profiles = _profiles()
    for profile in profiles.values():
        profile["sign_off_scope"]["entity_types"] = ["RedFlag"]
    assert not eligible_signoffs(data, profiles, revision_field="last_reviewed", entity_type="RedFlag")


@pytest.mark.parametrize("locale", ["es", "pt", "de", "fr"])
def test_patient_review_statuses_have_explicit_native_draft_copy(locale):
    catalog = messages_for(locale)
    for source in (
        "Clinical content review pending",
        "Clinical content review pending (1 of 2 eligible reviews recorded)",
        "Current clinical-content review recorded",
        "This status describes reviews of the knowledge-base content, not approval of a plan for you.",
    ):
        assert catalog[source] and catalog[source] != source
    assert catalog["Перегляд клінічного змісту очікується"] == catalog["Clinical content review pending"]


def test_audit_uses_supplied_kb_registry_and_fails_closed_on_revocation(tmp_path):
    bma_dir, reviewers_dir = tmp_path / "biomarker_actionability", tmp_path / "reviewers"
    bma_dir.mkdir()
    reviewers_dir.mkdir()
    (bma_dir / "test.yaml").write_text(yaml.safe_dump(_candidate()), encoding="utf-8")
    profiles = _profiles()
    for rid, profile in profiles.items():
        (reviewers_dir / f"{rid}.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    arguments = dict(bma_dir=bma_dir, biomarker_dir=tmp_path / "biomarkers",
                     civic_root=tmp_path / "civic", manifest=None, as_of=date(2026, 10, 11))
    assert audit_escat_readiness(**arguments)["release_ready_count"] == 1
    for rid, profile in profiles.items():
        profile["authorization"]["status"] = "revoked"
        (reviewers_dir / f"{rid}.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    report = audit_escat_readiness(**arguments)
    assert report["release_ready_count"] == 0
    assert any("human-governance authorization" in issue["detail"] for issue in report["issues"])
