"""Public source-client contract: literal retrieval, provenance and safe failures."""

import io
import json
import traceback
import urllib.error
from dataclasses import replace
from datetime import datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from knowledge_base.clients.openfda_client import (
    OpenFDAClient,
    OpenFDAError,
    OpenFDAEventQuery,
    OpenFDAQuery,
)


def payload(skip=0, limit=10):
    return {
        "meta": {
            "last_updated": "2026-07-30",
            "terms": "https://open.fda.gov/terms/",
            "results": {"skip": skip, "limit": limit, "total": 42},
        },
        "results": [
            {
                "safetyreportid": "synthetic-report",
                "patient": {
                    "drug": [{"medicinalproduct": "TAGRISSO"}, {"medicinalproduct": "OTHER DRUG"}],
                    "reaction": [
                        {"reactionmeddrapt": "Synthetic reaction A"},
                        {"reactionmeddrapt": "Synthetic reaction B"},
                    ],
                },
            }
        ],
    }


def stub_http(monkeypatch, data):
    calls = []

    def get(request, timeout):
        calls.append((request, timeout))
        return io.BytesIO(json.dumps(data).encode())

    monkeypatch.setattr("urllib.request.urlopen", get)
    return calls


def test_named_search_and_provenance_preserve_raw_multidrug_reports(monkeypatch):
    upstream = payload()
    calls = stub_http(monkeypatch, upstream)
    query = OpenFDAEventQuery(
        active_substance="  osimertinib  ",
        brand_names=["Tagrisso", "TAGRISSO"],
        received_from="2020-01-01",
        received_to="2026-06-30",
    )
    response = OpenFDAClient().fetch(query)
    assert response.data == upstream  # No reaction/drug attribution or field loss.
    assert response.source_id == "SRC-OPENFDA"
    assert response.api_version == "openFDA"
    assert datetime.fromisoformat(response.fetched_at).tzinfo is not None
    assert not response.cache_hit
    request, timeout = calls[0]
    assert urlsplit(request.full_url).path == "/drug/event.json"
    assert timeout == 20
    params = parse_qs(urlsplit(request.full_url).query)
    assert params["search"] == [
        '(patient.drug.openfda.generic_name:"osimertinib" OR '
        'patient.drug.activesubstance.activesubstancename:"osimertinib" OR '
        'patient.drug.medicinalproduct:"osimertinib" OR '
        'patient.drug.medicinalproduct:"Tagrisso" OR '
        'patient.drug.openfda.brand_name:"Tagrisso") AND receivedate:[20200101 TO 20260630]'
    ]
    assert params["sort"] == ["receivedate:desc"]
    assert params["limit"] == ["10"] and params["skip"] == ["0"]
    assert query.brand_names == ("Tagrisso", "TAGRISSO")


def test_brand_annotations_removed_without_changing_input_and_names_escaped():
    brands = ["Truxima (biosimilar)", 'X" OR _exists_:patient\\drug']
    query = OpenFDAEventQuery(brand_names=brands)
    assert 'medicinalproduct:"Truxima"' in query.search
    assert "biosimilar" not in query.search
    assert 'medicinalproduct:"X\\" OR _exists_:patient\\\\drug"' in query.search
    assert parse_qs(urlsplit(query.request_url).query)["search"] == [query.search]
    brands.append("later mutation")
    assert len(query.brand_names) == 2
    assert query.brand_names[0] == "Truxima (biosimilar)"


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"active_substance": "   "},
        {"active_substance": None},
        {"brand_names": "Tagrisso"},
        {"brand_names": (None,)},
        {"brand_names": (" ",)},
        {"brand_names": ("(biosimilar)",)},
        {"limit": 0},
        {"limit": 1001},
        {"limit": True},
        {"limit": 1.5},
        {"skip": -1},
        {"skip": 25001},
        {"skip": False},
        {"received_from": "2020-01-01"},
        {"received_to": "2026-06-30"},
        {"received_from": "20200101", "received_to": "20260630"},
        {"received_from": "2026-02-30", "received_to": "2026-06-30"},
        {"received_from": "2026-07-01", "received_to": "2026-06-30"},
    ],
)
def test_invalid_queries_rejected_before_http(kwargs):
    if kwargs and "active_substance" not in kwargs and "brand_names" not in kwargs:
        kwargs = {"active_substance": "osimertinib", **kwargs}
    with pytest.raises(ValueError):
        OpenFDAEventQuery(**kwargs)


def test_cache_distinguishes_names_dates_limits_pages_and_legacy_endpoint(monkeypatch):
    calls = []

    def get(request, timeout):
        calls.append(request.full_url)
        params = parse_qs(urlsplit(request.full_url).query)
        return io.BytesIO(
            json.dumps(payload(int(params.get("skip", [0])[0]), int(params["limit"][0]))).encode()
        )

    monkeypatch.setattr("urllib.request.urlopen", get)
    client = OpenFDAClient()
    query = OpenFDAEventQuery(active_substance="osimertinib")
    first = client.fetch(query)
    second = client.fetch(query)
    assert second.cache_hit and second.fetched_at == first.fetched_at
    variants = [
        replace(query, active_substance="imatinib"),
        replace(query, brand_names=("Tagrisso",)),
        replace(query, limit=1),
        replace(query, skip=10),
        replace(query, received_from="2020-01-01", received_to="2026-06-30"),
        OpenFDAQuery(search="osimertinib"),
    ]
    for variant in variants:
        assert not client.fetch(variant).cache_hit
    assert len(calls) == 1 + len(variants)


@pytest.mark.parametrize("skip", [0, 25000])
def test_explicit_no_matches_is_cached_without_invented_freshness_or_total(monkeypatch, skip):
    calls = []

    def get(request, timeout):
        calls.append(request)
        body = {"error": {"code": "NOT_FOUND", "message": "No matches found!"}}
        raise urllib.error.HTTPError(
            request.full_url, 404, "Not Found", {}, io.BytesIO(json.dumps(body).encode())
        )

    monkeypatch.setattr("urllib.request.urlopen", get)
    client = OpenFDAClient()
    query = OpenFDAEventQuery(active_substance="nonexistent", limit=1, skip=skip)
    response = client.fetch(query)
    expected_page = {"skip": skip, "limit": 1}
    if skip == 0:
        expected_page["total"] = 0
    assert response.data == {"meta": {"results": expected_page}, "results": []}
    assert "last_updated" not in response.data["meta"]
    assert client.fetch(query).cache_hit
    assert len(calls) == 1


@pytest.mark.parametrize(
    "status,body",
    [
        (400, b"{}"),
        (404, b"not json"),
        (404, b'{"error":{"code":"NOT_FOUND","message":"Unknown endpoint"}}'),
        (429, b'{"error":{"code":"NOT_FOUND","message":"No matches found!"}}'),
        (503, b"{}"),
    ],
)
def test_http_failures_not_empty_cached_or_credential_leaking(monkeypatch, status, body):
    calls = []
    secret = "synthetic-api-secret"
    monkeypatch.setenv("OPENFDA_API_KEY", secret)

    def get(request, timeout):
        calls.append(request)
        raise urllib.error.HTTPError(request.full_url, status, secret, {}, io.BytesIO(body))

    monkeypatch.setattr("urllib.request.urlopen", get)
    client = OpenFDAClient()
    query = OpenFDAEventQuery(active_substance="osimertinib")
    for _ in range(2):
        with pytest.raises(OpenFDAError) as error:
            client.fetch(query)
        assert error.value.http_status == status
        assert secret not in str(error.value)
        assert secret not in "".join(traceback.format_exception(error.value))
        assert secret not in client._last_error
    assert len(calls) == 2
    assert parse_qs(urlsplit(calls[0].full_url).query)["api_key"] == [secret]
    assert secret not in query.request_url
    assert "api_key" not in query.params


@pytest.mark.parametrize(
    "error", [urllib.error.URLError("synthetic secret"), TimeoutError("synthetic secret")]
)
def test_transport_failure_not_treated_as_empty(monkeypatch, error):
    def get(request, timeout):
        raise error

    monkeypatch.setattr("urllib.request.urlopen", get)
    with pytest.raises(OpenFDAError, match="transport error") as raised:
        OpenFDAClient().fetch(OpenFDAEventQuery(active_substance="osimertinib"))
    assert "synthetic secret" not in str(raised.value)


@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        {},
        {"results": []},
        {"meta": {"results": {"total": True, "limit": 1, "skip": 0}}, "results": []},
        {"meta": {"results": {"total": 1, "limit": 1, "skip": 0}}, "results": ["not a report"]},
    ],
)
def test_malformed_success_response_is_error(monkeypatch, data):
    calls = stub_http(monkeypatch, data)
    client = OpenFDAClient()
    for _ in range(2):
        with pytest.raises(OpenFDAError, match="invalid result envelope"):
            client.fetch(OpenFDAEventQuery(active_substance="osimertinib"))
    assert len(calls) == 2


def test_invalid_json_is_sanitized(monkeypatch):
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda *args, **kwargs: io.BytesIO(b"upstream secret")
    )
    with pytest.raises(OpenFDAError, match="not valid JSON"):
        OpenFDAClient().fetch(OpenFDAEventQuery(active_substance="osimertinib"))


@pytest.mark.parametrize(
    "endpoint,path", [("label", "/drug/label.json"), ("recall", "/drug/enforcement.json")]
)
def test_existing_label_and_recall_contracts_unchanged(monkeypatch, endpoint, path):
    upstream = {"results": [{"legacy": True}]}
    calls = stub_http(monkeypatch, upstream)
    response = OpenFDAClient().fetch(
        OpenFDAQuery(endpoint=endpoint, search='brand_name:"X"', limit=3)
    )
    assert response.data == upstream
    assert urlsplit(calls[0][0].full_url).path == path
    assert parse_qs(urlsplit(calls[0][0].full_url).query)["search"] == ['brand_name:"X"']
