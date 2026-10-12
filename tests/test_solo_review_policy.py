"""An optional real content review is not a publication quorum or care approval."""
from copy import deepcopy

from knowledge_base.engine.render import _render_signoff_badge_patient
from knowledge_base.engine.mdt_orchestrator import SkillMetadata
from knowledge_base.review_metrics import current_review_count
from knowledge_base.schemas.biomarker_actionability import actionability_release_readiness
from scripts.clinical_curated_copy import content_review_messages
from tests.test_review_readiness_fail_closed import _candidate, _profiles


def test_one_current_authorized_independent_review_is_recorded():
    data = _candidate()
    data['reviewer_signoffs'] = data['reviewer_signoffs'][:1]
    profiles = _profiles()
    assert actionability_release_readiness(data, reviewer_profiles=profiles).ready
    data['last_reviewed'] = data['last_verified']
    data['applicable_to'] = {'disease_id': data.pop('disease_id')}
    assert current_review_count(data, 'indications', profiles, {'DIS-CRC': {'lineage': 'solid_tumor'}}) == 1
    badge = _render_signoff_badge_patient(data, target_lang='en', reviewer_profiles=profiles)
    assert 'data-review-count="1"' in badge
    assert 'Current clinical-content review recorded' in badge
    assert '1 of 2' not in badge and 'approved' not in badge.lower()
    revoked = deepcopy(profiles)
    revoked['REV-TEST-A']['authorization']['status'] = 'revoked'
    assert 'signoff-complete' not in _render_signoff_badge_patient(data, target_lang='en', reviewer_profiles=revoked)


def test_raw_mdt_records_do_not_claim_clinical_validation():
    skill = SkillMetadata('VIRTUAL', 'Virtual', '1', '2026-10-12', verified_by=[{'reviewer_id': 'UNKNOWN'}])
    assert skill.review_status == 'recorded'
    assert skill.review_status != 'reviewed'


def test_review_status_native_copy_is_available_for_all_nine_locales():
    for locale in ('es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi'):
        copy = content_review_messages(locale)
        assert copy['Current clinical-content review recorded'] != 'Current clinical-content review recorded'
        assert copy['Записано актуальний перегляд клінічного змісту'] == copy['Current clinical-content review recorded']
