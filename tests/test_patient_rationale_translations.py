from copy import deepcopy
from types import SimpleNamespace

from knowledge_base.engine._patient_rationale import (
    RATIONALE_TRANSLATION_STATUS, build_track_rationale, build_track_rationale_html,
)


def test_english_rationale_preserves_findings_thresholds_and_input():
    result = SimpleNamespace(
        plan=SimpleNamespace(variant_actionability=[{'biomarker_id': 'BIO-BRAF', 'variant_qualifier': 'V600E', 'escat_tier': 'IA'}]),
        trace=[{'fired_red_flags': ['RF-TEST']}],
        kb_resolved={'red_flags': {'RF-TEST': {'definition': 'Value <0.5 mg/L. Second sentence.', 'definition_ua': 'Показник <0.5 mg/L.'}}},
    )
    before = deepcopy(result.__dict__)
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True), target_lang='en')
    assert 'BRAF V600E' in bullets[0]
    assert '<0.5 mg/L' in bullets[1]
    assert 'Second sentence' not in bullets[1]
    assert result.__dict__ == before
    rendered = build_track_rationale_html(result, SimpleNamespace(is_default=True), target_lang='en')
    assert '&lt;0.5 mg/L' in rendered
    assert RATIONALE_TRANSLATION_STATUS['en'] == 'draft_pending_review'


def test_missing_english_definition_explicitly_retains_original():
    result = SimpleNamespace(plan=None, trace=[{'fired_red_flags': ['RF-TEST']}], kb_resolved={'red_flags': {'RF-TEST': {'definition_ua': 'Не чекати.'}}})
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True), target_lang='en')
    assert 'original Ukrainian text; translation unavailable' in bullets[0]
    assert 'Не чекати' in bullets[0]


def test_no_fired_flags_is_not_a_claim_of_absent_clinical_risk():
    result = SimpleNamespace(plan=None, trace=[], kb_resolved={})
    track = SimpleNamespace(is_default=True)
    assert 'does not rule out risks' in build_track_rationale(result, track, target_lang='en')[0]
    assert 'не виключає ризиків' in build_track_rationale(result, track)[0]
