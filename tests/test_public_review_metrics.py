"""Public claims use current authority and complete denominators, not counters."""
from copy import deepcopy

import pytest
import yaml

from knowledge_base.review_metrics import current_review_count, historical_review_counts
from knowledge_base import stats
from tests.review_provenance_fixtures import authorized_profiles


def context():
    profiles = authorized_profiles("REV-A", "REV-B")
    entity = {
        "id": "IND-TEST", "last_reviewed": "2026-08-03",
        "applicable_to": {"disease_id": "DIS-CRC"},
        "recommended_regimen": "REG-TEST",
        "reviewer_signoffs": [
            {"reviewer_id": rid, "entity_version": "2026-08-03",
             "scope_match": True, "timestamp": "2026-08-04T00:00:00+00:00"}
            for rid in profiles
        ],
    }
    return entity, profiles, {"DIS-CRC": {"id": "DIS-CRC", "lineage": "carcinoma"}}


@pytest.mark.parametrize("failure", ["legacy", "alias", "stale", "pending", "revoked", "scope", "unknown_disease"])
def test_public_reviews_fail_closed(failure):
    entity, profiles, diseases = context()
    original = deepcopy((entity, profiles, diseases))
    assert current_review_count(entity, "indications", profiles, diseases) == 2
    assert (entity, profiles, diseases) == original
    if failure == "legacy":
        entity["reviewer_signoffs"] = 99
    elif failure == "alias":
        profiles["REV-B"]["authorization"]["identity_key"] = profiles["REV-A"]["authorization"]["identity_key"]
    elif failure == "stale":
        entity["last_reviewed"] = "2026-08-05"
    elif failure in {"pending", "revoked"}:
        profiles["REV-B"]["authorization"]["status"] = failure
    elif failure == "scope":
        profiles["REV-B"]["sign_off_scope"]["diseases_explicit"] = ["DIS-OTHER"]
    else:
        diseases.clear()
    assert current_review_count(entity, "indications", profiles, diseases) < 2


def test_stats_denominator_includes_absent_reviews_and_bma(tmp_path, monkeypatch):
    entity, profiles, diseases = context()
    contents = {"diseases": list(diseases.values()), "reviewers": list(profiles.values()),
                "indications": [entity, {"id": "IND-OTHER", "applicable_to": {"disease_id": "DIS-CRC"}}],
                "regimens": [{"id": "REG-TEST", "reviewer_signoffs": 77}],
                "algorithms": [{"id": "ALG-TEST", "applicable_to_disease": "DIS-CRC"}],
                "biomarker_actionability": [{"id": "BMA-TEST", "disease_id": "DIS-CRC"}]}
    for directory, records in contents.items():
        target = tmp_path / directory
        target.mkdir()
        for row in records:
            (target / (row["id"] + ".yaml")).write_text(yaml.safe_dump(row), encoding="utf-8")
    monkeypatch.setattr(stats, "_KB_CONTENT", tmp_path)
    monkeypatch.setattr(stats, "_role_catalog", lambda: {})
    snapshot = stats.collect_stats()
    assert snapshot.reviewer_signoffs_total == 5
    assert snapshot.reviewer_signoffs_reviewed == 1
    assert snapshot.historical_structured_reviews == 2
    assert snapshot.legacy_review_counter_total == 77
    disease = snapshot.diseases[0]
    assert disease.reviewer_signoffs_max == 2
    # One reviewed indication cannot confer reviewed status on other records.
    assert disease.coverage_status == "stub_full_chain"


def test_historical_counts_are_explicitly_separate():
    assert historical_review_counts({"reviewer_signoffs": 2}) == (0, 2)
    assert historical_review_counts({"reviewer_signoffs": [{}, "bad"]}) == (1, 0)
    assert historical_review_counts({"reviewer_signoffs": True}) == (0, 0)
    assert historical_review_counts({"reviewer_signoffs": -9}) == (0, 0)


def test_disease_reviewed_requires_every_record():
    coverage = stats.DiseaseCoverage("DIS-TEST", "Synthetic", 1, 1, True, 0, 0, 2, 3, 3)
    assert coverage.coverage_status == "reviewed"
    coverage.clinical_records_reviewed = 2
    assert coverage.coverage_status == "stub_full_chain"


def test_coverage_positive_control_includes_linked_and_disease_context_records():
    entity, _, diseases = context()
    algorithm = {"id": "ALG-TEST", "applicable_to_disease": "DIS-CRC"}
    regimen = {"id": "REG-TEST"}
    biomarker = {"id": "BMA-TEST", "disease_id": "DIS-CRC"}
    redflag = {"id": "RF-TEST", "relevant_diseases": ["DIS-CRC"]}
    records = {row["id"]: row for row in [entity, algorithm, regimen, biomarker, redflag]}
    counts = {entity_id: 2 for entity_id in records}
    coverage = stats._build_coverage(list(diseases.values()), [entity], [algorithm], [], counts, records)[0]
    assert coverage.clinical_records_total == 5
    assert coverage.coverage_status == "reviewed"
    counts["BMA-TEST"] = 0
    coverage = stats._build_coverage(list(diseases.values()), [entity], [algorithm], [], counts, records)[0]
    assert coverage.coverage_status == "stub_full_chain"


def test_malformed_statistics_input_cannot_silently_disappear(tmp_path):
    path = tmp_path / "invalid.yaml"
    path.write_text("- invalid entity", encoding="utf-8")
    with pytest.raises(ValueError, match="Expected a mapping"):
        stats._load_yaml(path)


def test_current_review_explanation_has_four_native_drafts():
    from scripts.clinical_curated_copy import messages_for
    source = "Only current independent content reviews by authorized reviewers are counted; this is not approval of a patient's treatment."
    ukrainian = 'Рахуються лише актуальні незалежні перегляди змісту від уповноважених рецензентів; це не схвалення лікування пацієнта.'
    for locale in ('es', 'pt', 'de', 'fr'):
        catalog = messages_for(locale)
        assert catalog[source] and catalog[source] != source
        assert catalog[ukrainian] == catalog[source]


def test_solo_capabilities_do_not_impose_a_reviewer_quota():
    from scripts.build_site import render_capabilities, render_specs
    snapshot = stats.Stats("Synthetic verification", [], 0, 0, 0, 0, 0, 10, 0, [])
    for locale, expected in [('en', 'External clinical review is optional'),
                             ('uk', 'Зовнішній клінічний перегляд є додатковим')]:
        page = render_capabilities(snapshot, target_lang=locale)
        assert expected in page
        assert '0/10' not in page
        assert '≥85% verified' not in page
        assert 'dual-reviewer sign-off' not in page
        specification_page = render_specs(snapshot, target_lang=locale)
        assert 'two-reviewer merge' not in specification_page
        assert '2 of 3 Clinical Co-Lead' not in specification_page
        assert '2 з 3 Clinical Co-Lead' not in specification_page


def test_solo_policy_has_four_native_drafts():
    from scripts.clinical_curated_copy import messages_for
    english = 'Solo project. One maintainer delivers updates with automated checks and source traceability. External clinical review is optional and is recorded separately.'
    ukrainian = 'Солопроєкт. Один власник доставляє оновлення з автоматичними перевірками та простежуваними джерелами. Зовнішній клінічний перегляд є додатковим і записується окремо.'
    for locale in ('es', 'pt', 'de', 'fr'):
        catalog = messages_for(locale)
        assert catalog[english] != english
        assert catalog[ukrainian] == catalog[english]
