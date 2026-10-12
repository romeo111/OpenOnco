import math
from pathlib import Path

import pytest

from knowledge_base.engine import generate_diagnostic_brief, generate_plan, is_diagnostic_profile
from knowledge_base.engine.profile_input import validate_json_object, validate_patient_profile
from serverless.clinical_question import _safe_json_object, handle_json_request


@pytest.mark.parametrize('profile', [None, [], [1], 1, False, 'profile'])
def test_rejects_non_object_before_kb_io(profile, tmp_path):
    for generate in (generate_plan, generate_diagnostic_brief):
        with pytest.raises(ValueError, match='object'):
            generate(profile, kb_root=tmp_path / 'nonexistent-kb')


@pytest.mark.parametrize('number', [math.nan, math.inf, -math.inf])
def test_nested_nonfinite_stops_routing_and_generation(number, tmp_path):
    profile = {'disease': {'suspicion': {}}, 'findings': {'nested': [0, {'value': number}]}}
    for generate in (generate_plan, generate_diagnostic_brief):
        with pytest.raises(ValueError, match='non-finite'):
            generate(profile, kb_root=tmp_path / 'nonexistent-kb')
    with pytest.raises(ValueError, match='non-finite'):
        is_diagnostic_profile(profile)


@pytest.mark.parametrize('section', ['disease', 'demographics', 'findings', 'biomarkers', 'clinician_confirmations'])
def test_nonobject_sections_rejected(section):
    for wrong in ([], 0, False, 'unknown'):
        with pytest.raises(ValueError, match=section):
            validate_patient_profile({section: wrong})


def test_preserves_unknown_zero_false_and_shared_structure():
    shared = {'value': 0.836, 'negative': False}
    profile = {'findings': shared, 'metadata': [shared, None], 'demographics': None, 'patient_id': 'VIRTUAL-BOUNDARY-001'}
    before = repr(profile)
    validate_patient_profile(profile)
    assert repr(profile) == before
    cyclic = {}; cyclic['self'] = cyclic
    with pytest.raises(ValueError, match='cyclic'):
        validate_json_object(cyclic)


@pytest.mark.parametrize('text', ['{"findings":{"value":NaN}}', '{"findings":{"value":Infinity}}', '{"findings":{"value":-Infinity}}', '{"findings":{"value":1e9999}}'])
def test_model_json_cannot_bypass_finite_boundary(text):
    with pytest.raises(ValueError, match='non-finite'):
        _safe_json_object(text)


def test_bad_request_rejected_before_quota_or_model(monkeypatch):
    import serverless.clinical_question as endpoint
    def forbidden(*args, **kwargs):
        raise AssertionError('Invalid payload reached quota/provider work')
    monkeypatch.setattr(endpoint, '_quota_principal', forbidden)
    status, _, response = handle_json_request({'case_text': 'VIRTUAL ONLY', 'extra': math.inf})
    assert status == 400 and response['status'] == 'error'
