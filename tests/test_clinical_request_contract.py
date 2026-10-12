import json

import pytest
from serverless import clinical_question as cq


@pytest.mark.parametrize('field', ['case_text', 'locale'])
@pytest.mark.parametrize('value', [[], {}, ['PRIVATE-MARKER'], {'patient': 'PRIVATE-MARKER'}, 0, 1.5, False, True])
def test_wrong_field_types_stop_before_quota_and_processing(monkeypatch, field, value):
    def forbidden(*args, **kwargs):
        pytest.fail('Malformed request reached quota or clinical processing')
    for name in ('_quota_principal', '_quota_usage', '_record_quota_usage', 'answer_clinical_question'):
        monkeypatch.setattr(cq, name, forbidden)
    body = {'case_text': 'VIRTUAL ONLY', 'locale': 'en', field: value}
    status, _, response = cq.handle_json_request(body)
    assert status == 400
    assert response == {'status': 'error', 'message': f'{field} must be a string or null.'}
    assert 'PRIVATE-MARKER' not in json.dumps(response)


@pytest.mark.parametrize('locale', ['PRIVATE-MARKER', 'xx', 'uk_UA', 'en\nPRIVATE-MARKER'])
def test_unknown_language_is_not_guessed_or_charged(monkeypatch, locale):
    monkeypatch.setattr(cq, '_quota_principal', lambda *args: pytest.fail('Invalid locale reached quota'))
    status, _, response = cq.handle_json_request({'case_text': 'VIRTUAL ONLY', 'locale': locale})
    assert status == 400 and response == {'status': 'error', 'message': 'Unsupported locale.'}


@pytest.mark.parametrize('locale', list(cq.ANSWER_LANGUAGES) + ['fr-CA', 'PT-PT'])
def test_supported_languages_preserve_text_and_existing_quota(monkeypatch, locale):
    cq._USAGE_COUNTS.clear()
    seen = []
    def answer(text, *, locale):
        seen.append((text, locale))
        return {'status': 'test'}
    monkeypatch.setattr(cq, 'answer_clinical_question', answer)
    text = '  VIRTUAL ONLY\n  '
    status, _, response = cq.handle_json_request({'case_text': text, 'locale': locale})
    assert status == 200 and response['questions_used'] == 1
    assert seen == [(text, locale)]


@pytest.mark.parametrize('body', [{}, {'case_text': None, 'locale': None}, {'case_text': '', 'locale': ''}])
def test_optional_null_and_empty_fields_keep_legacy_defaults(monkeypatch, body):
    cq._USAGE_COUNTS.clear()
    def answer(text, *, locale):
        assert text == '' and locale == 'uk'
        return {'status': 'test'}
    monkeypatch.setattr(cq, 'answer_clinical_question', answer)
    assert cq.handle_json_request(body)[0] == 200


@pytest.mark.parametrize('locale,expected', [('en-PRIVATE-MARKER', 'en'), ('PRIVATE-MARKER', 'unknown'), ({'PRIVATE-MARKER': 1}, 'unknown')])
def test_audit_locale_never_contains_arbitrary_input(monkeypatch, tmp_path, locale, expected):
    log = tmp_path / 'audit.jsonl'
    monkeypatch.setenv('OPENONCO_ASK_AUDIT_LOG', str(log))
    cq._write_ask_audit_log(body={'case_text': 'VIRTUAL ONLY', 'locale': locale}, request_meta=None,
                            http_status=400, response={'status': 'error'})
    row = json.loads(log.read_text(encoding='utf-8'))
    assert row['locale'] == expected
    assert 'PRIVATE-MARKER' not in log.read_text(encoding='utf-8')
