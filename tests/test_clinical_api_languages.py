"""Native API prose must not change clinical extraction or engine contracts."""
import json

import pytest

from serverless import clinical_question as cq
from serverless.clinical_locale_messages import localize_response


@pytest.mark.parametrize('locale,language', [('es','Spanish'),('pt','European Portuguese'),('de','German'),('fr','French')])
def test_presenter_language_and_immutable_clinical_values(monkeypatch, locale, language):
    captured = {}
    monkeypatch.setattr(cq, 'call_openai_json', lambda **kwargs: captured.update(kwargs) or {})
    engine = cq.EngineSummary(mode='treatment', ok=False, payload={}, warnings=[], error=None)
    patient = {'disease': {'id': 'DIS-NSCLC'}, 'biomarkers': {'EGFR': 'negative'}}
    cq.compose_answer(case_text='Synthetic example', extraction={}, patient=patient, engine=engine, locale=locale)
    assert f'Write all user-facing prose in {language}.' in captured['system']
    assert 'doses, numeric values and source identifiers exactly' in captured['system']
    body = json.loads(captured['user'])
    assert body['patient_profile'] == patient
    assert body['required_safety_note'] == cq.DISCLAIMER_TRANSLATIONS[locale]


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_empty_request_uses_native_clarification_without_provider(monkeypatch, locale):
    monkeypatch.setattr(cq, 'call_openai_json', lambda **kwargs: pytest.fail('No provider call expected'))
    answer = cq.answer_clinical_question('', locale=locale)
    assert answer['clarifying_questions'][0] != 'Надішліть клінічну ситуацію текстом.'
    assert answer['safety_note'] == cq.DISCLAIMER_TRANSLATIONS[locale]
    assert answer['status'] == 'needs_clarification'


@pytest.mark.parametrize('case', ['Lungenkrebs, Stadium IV', 'Cancro da mama', 'Cáncer de pulmón', 'Leucémie aiguë'])
def test_native_oncology_cases_pass_preflight(case):
    assert cq._preflight_case_text(case, locale='fr') is None


def test_clarification_preserves_suspect_tokens_and_engine_payload():
    original = {'direct_answer': '', 'clarifying_questions': ['Clarify or correct biomarker(s): TYPO-EGFR. They were not found in the OpenOnco KB vocabulary.'], 'engine_summary': {'mode': 'treatment', 'payload': {'dose': '10 mg', 'id': 'REG-TEST'}}}
    localized = localize_response(original, 'fr')
    assert 'TYPO-EGFR' in localized['clarifying_questions'][0]
    assert localized['engine_summary'] == original['engine_summary']
    assert localized['clarifying_questions'] != original['clarifying_questions']
