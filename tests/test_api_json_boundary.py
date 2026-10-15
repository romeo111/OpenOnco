"""HTTP parser failures must not reach clinical processing or paid providers."""
import importlib.util
import io
import sys
from pathlib import Path

import pytest


@pytest.fixture(params=['index.py', 'clinical-question.py'])
def endpoint(request):
    path = Path(__file__).resolve().parents[1] / 'api' / request.param
    spec = importlib.util.spec_from_file_location('tested_http_endpoint', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def post(endpoint, monkeypatch, raw):
    clinical_calls = []
    def process(payload, **kwargs):
        clinical_calls.append(payload)
        return 200, {}, {'status': 'test'}
    monkeypatch.setattr(endpoint, 'handle_json_request', process)
    handler = object.__new__(endpoint.handler)
    body = raw.encode('utf-8')
    handler.headers = {'Content-Length': str(len(body))}
    handler.rfile = io.BytesIO(body)
    handler.client_address = ('127.0.0.1', 0)
    responses = []
    handler._send_json = lambda status, headers, payload: responses.append((status, payload))
    handler.do_POST()
    return responses, clinical_calls


@pytest.mark.parametrize('raw', [
    '{"extra":' + '[' * 6000 + '0' + ']' * 6000 + '}',
    '{"extra":' + '9' * 10000 + '}',
    '{"extra":',
], ids=['excessive-nesting', 'excessive-integer', 'malformed-json'])
def test_parser_failure_returns_400_before_clinical_processing(endpoint, monkeypatch, raw):
    if raw.startswith('{"extra":999') and sys.get_int_max_str_digits() == 0:
        pytest.skip('Python integer conversion limit is disabled')
    previous_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(1000)
        responses, calls = post(endpoint, monkeypatch, raw)
    finally:
        sys.setrecursionlimit(previous_limit)
    assert responses == [(400, {'status': 'error', 'message': 'Invalid JSON body'})]
    assert calls == []


def test_valid_nested_request_reaches_processing_unchanged(endpoint, monkeypatch):
    responses, calls = post(endpoint, monkeypatch, '{"case_text":"","extra":{"values":[0,false,null]}}')
    assert responses == [(200, {'status': 'test'})]
    assert calls == [{'case_text': '', 'extra': {'values': [0, False, None]}}]


def test_nesting_limit_ignores_brackets_and_escaped_quotes_in_strings():
    import json

    from serverless.request_json import MAX_JSON_NESTING, decode_request_json
    original = {'text': '[{' * 6000 + '\\"' + ']}' * 6000}
    assert decode_request_json(json.dumps(original)) == original
    assert decode_request_json('[' * MAX_JSON_NESTING + '0' + ']' * MAX_JSON_NESTING)
    with pytest.raises(ValueError, match='nesting'):
        decode_request_json('[' * (MAX_JSON_NESTING + 1) + '0' + ']' * (MAX_JSON_NESTING + 1))


@pytest.mark.parametrize('raw', [
    '{"case_text":"first","case_text":"second"}',
    '{"patient":{"demographics":{"age":17,"age":60}}}',
    '{"patient":{"concomitant_medications":{"status":"partial","status":"complete","drug_ids":[]}}}',
    '{"patient":{"concomitant_medications":{"status":"complete","drug_ids":["DRUG-BLEOMYCIN"],"drug_ids":[]}}}',
    '{"patient":{"biomarkers":{"BIO-CD30-IHC":"negative","BIO-CD30-IHC":"positive"}}}',
    '{"patient":{"age":60,"age":60}}',
    r'{"patient":{"status":"partial","\u0073tatus":"complete"}}',
], ids=['request-field', 'nested-age', 'medication-status', 'medication-list', 'biomarker', 'identical-value', 'escaped-key'])
def test_duplicate_keys_return_400_before_clinical_processing(endpoint, monkeypatch, raw):
    responses, calls = post(endpoint, monkeypatch, raw)
    assert responses == [(400, {'status': 'error', 'message': 'Invalid JSON body'})]
    assert calls == [], 'Ambiguous input must not reach clinical handling or a provider'


def test_same_key_in_different_objects_and_key_like_text_are_preserved(endpoint, monkeypatch):
    import json
    original = {
        'patient': {'status': 'partial', 'extra': {'status': 'unknown'}},
        'metadata': [{'status': False}, {'status': None}],
        'case_text': 'Synthetic text containing "status": "partial", "status": "complete"',
    }
    responses, calls = post(endpoint, monkeypatch, json.dumps(original))
    assert responses == [(200, {'status': 'test'})]
    assert calls == [original]
