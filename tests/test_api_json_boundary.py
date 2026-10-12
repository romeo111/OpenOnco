"""HTTP parser failures must not reach clinical processing or paid providers."""
import importlib.util
import io
from pathlib import Path
import sys

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
    from serverless.request_json import decode_request_json, MAX_JSON_NESTING
    original = {'text': '[{' * 6000 + '\\"' + ']}' * 6000}
    assert decode_request_json(json.dumps(original)) == original
    assert decode_request_json('[' * MAX_JSON_NESTING + '0' + ']' * MAX_JSON_NESTING)
    with pytest.raises(ValueError, match='nesting'):
        decode_request_json('[' * (MAX_JSON_NESTING + 1) + '0' + ']' * (MAX_JSON_NESTING + 1))
