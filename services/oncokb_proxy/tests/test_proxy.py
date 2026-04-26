"""Smoke + unit tests for the OncoKB proxy. Live calls are mocked.

Run from project root:
    cd services/oncokb_proxy
    pip install -r requirements.txt -r tests/requirements.txt
    pytest tests/
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure scaffold mode for tests; live mode is integration-only.
os.environ.setdefault("ONCOKB_LIVE", "0")
os.environ.setdefault(
    "ONCOKB_PROXY_CORS_ORIGINS",
    "https://openonco.info,https://openonco.org,http://localhost:8000",
)
# Disable rate-limiter in tests — we exercise the limit explicitly in a
# dedicated test, but other tests must not trip it.
os.environ.setdefault("ONCOKB_RATE_LIMIT_DISABLED", "1")
os.environ.setdefault("GIT_SHA", "test-sha-deadbeef")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from app import app  # noqa: E402


client = TestClient(app)


def test_healthz_reports_scaffold_mode():
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["live_mode"] is False
    assert body["token_configured"] is False  # no token set in test env
    assert "https://openonco.org" in body["allowed_origins"]


def test_lookup_scaffold_returns_empty_options_and_url():
    r = client.post(
        "/lookup",
        json={"gene": "BRAF", "variant": "V600E", "tumor_type": "MEL"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["gene"] == "BRAF"
    assert body["variant"] == "V600E"
    assert body["oncokb_url"] == "https://www.oncokb.org/gene/BRAF/V600E"
    assert body["therapeutic_options"] == []
    assert body["cached"] is False


def test_lookup_caches_repeat_call():
    payload = {"gene": "EGFR", "variant": "L858R"}
    first = client.post("/lookup", json=payload).json()
    second = client.post("/lookup", json=payload).json()
    assert first["cached"] is False
    assert second["cached"] is True


def test_lookup_validates_input():
    r = client.post("/lookup", json={"gene": "", "variant": "V600E"})
    assert r.status_code == 422  # pydantic min_length violation


def test_cors_preflight_allows_openonco_origin():
    r = client.options(
        "/lookup",
        headers={
            "Origin": "https://openonco.org",
            "Access-Control-Request-Method": "POST",
        },
    )
    # FastAPI/Starlette auto-handles preflight; expect 200 with allow-origin
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == "https://openonco.org"


def test_cors_preflight_allows_localhost_regex():
    r = client.options(
        "/lookup",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_lookup_normalizes_gene_to_uppercase():
    r = client.post("/lookup", json={"gene": "kras", "variant": "G12D"}).json()
    assert r["gene"] == "KRAS"
    assert r["oncokb_url"] == "https://www.oncokb.org/gene/KRAS/G12D"


# ── Live-mode integration tests ──────────────────────────────────────────
# Live OncoKB call mocked via monkeypatch on httpx — no real API quota
# burn, no token required. Unblocked for CI after legal-team approval
# of OncoKB Academic Terms compatibility (2026-04-26; see src_oncokb.yaml
# legal_review.status: reviewed).


import app as oncokb_proxy_app  # noqa: E402


class _FakeAsyncClient:
    """Async-context-manager replacement for httpx.AsyncClient that
    captures request args + returns a pre-canned OncoKB-shaped response."""

    captured: dict = {}

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return False

    async def get(self, url, params=None, headers=None):
        _FakeAsyncClient.captured = {"url": url, "params": params, "headers": headers}

        class _Resp:
            status_code = 200

            def json(self):
                return {
                    "treatments": [
                        {
                            "level": "LEVEL_1",
                            "drugs": [{"drugName": "Vemurafenib"}, {"drugName": "Cobimetinib"}],
                            "description": "Standard-of-care BRAF V600E doublet in melanoma",
                            "pmids": ["28891423", "29320654"],
                        },
                        {
                            "level": "LEVEL_2",
                            "drugs": [{"drugName": "Dabrafenib"}, {"drugName": "Trametinib"}],
                            "description": "Alternative BRAF V600E doublet",
                            "pmids": ["29320654"],
                        },
                    ]
                }

            @property
            def text(self):
                return ""

        return _Resp()


def _force_live_mode(monkeypatch):
    """Flip module-globals to live-mode so /lookup takes the OncoKB path."""
    monkeypatch.setattr(oncokb_proxy_app, "LIVE_MODE", True)
    monkeypatch.setattr(oncokb_proxy_app, "ONCOKB_API_TOKEN", "test-token-secret")
    # Reset cache between live tests so we don't leak scaffold-mode entries
    oncokb_proxy_app._cache._d.clear()


def test_live_mode_calls_oncokb_with_bearer_token(monkeypatch):
    _force_live_mode(monkeypatch)
    monkeypatch.setattr(oncokb_proxy_app.httpx, "AsyncClient", _FakeAsyncClient)

    r = client.post(
        "/lookup",
        json={"gene": "BRAF", "variant": "V600E", "tumor_type": "MEL"},
    )
    assert r.status_code == 200, r.text

    captured = _FakeAsyncClient.captured
    assert captured["headers"]["Authorization"] == "Bearer test-token-secret"
    assert captured["headers"]["Accept"] == "application/json"
    assert captured["params"]["hugoSymbol"] == "BRAF"
    assert captured["params"]["alteration"] == "V600E"
    assert captured["params"]["tumorType"] == "MEL"
    assert captured["url"].endswith("/annotate/mutations/byProteinChange")


def test_live_mode_trims_oncokb_response_into_therapeutic_options(monkeypatch):
    _force_live_mode(monkeypatch)
    monkeypatch.setattr(oncokb_proxy_app.httpx, "AsyncClient", _FakeAsyncClient)

    body = client.post("/lookup", json={"gene": "BRAF", "variant": "V600E"}).json()

    assert body["gene"] == "BRAF"
    assert body["variant"] == "V600E"
    assert body["cached"] is False
    options = body["therapeutic_options"]
    assert len(options) == 2

    level1 = options[0]
    assert level1["level"] == "1"  # "LEVEL_1" prefix stripped
    assert level1["drugs"] == ["Vemurafenib", "Cobimetinib"]
    assert "BRAF V600E" in (level1["description"] or "")
    assert level1["pmids"] == ["28891423", "29320654"]

    level2 = options[1]
    assert level2["level"] == "2"
    assert level2["drugs"] == ["Dabrafenib", "Trametinib"]


def test_live_mode_caches_repeat_call(monkeypatch):
    _force_live_mode(monkeypatch)
    monkeypatch.setattr(oncokb_proxy_app.httpx, "AsyncClient", _FakeAsyncClient)

    payload = {"gene": "EGFR", "variant": "L858R", "tumor_type": "NSCLC"}
    first = client.post("/lookup", json=payload).json()
    second = client.post("/lookup", json=payload).json()
    assert first["cached"] is False
    assert second["cached"] is True
    assert second["therapeutic_options"] == first["therapeutic_options"]


def test_live_mode_without_token_returns_500(monkeypatch):
    monkeypatch.setattr(oncokb_proxy_app, "LIVE_MODE", True)
    monkeypatch.setattr(oncokb_proxy_app, "ONCOKB_API_TOKEN", None)
    oncokb_proxy_app._cache._d.clear()

    r = client.post("/lookup", json={"gene": "TP53", "variant": "R175H"})
    assert r.status_code == 500
    assert "ONCOKB_API_TOKEN is unset" in r.json()["detail"]


def test_healthz_reports_live_mode(monkeypatch):
    _force_live_mode(monkeypatch)
    body = client.get("/healthz").json()
    assert body["live_mode"] is True
    assert body["token_configured"] is True


# ── Phase 1a hardening tests ─────────────────────────────────────────────


def test_healthz_reports_git_sha_and_kill_switch():
    body = client.get("/healthz").json()
    assert body["git_sha"] == "test-sha-deadbeef"
    assert body["integration_enabled"] is True
    assert body["rate_limit"] == "disabled"


def test_cors_default_includes_openonco_info():
    r = client.options(
        "/lookup",
        headers={
            "Origin": "https://openonco.info",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == "https://openonco.info"


def test_request_id_is_echoed_when_provided():
    r = client.post(
        "/lookup",
        json={"gene": "BRAF", "variant": "V600E"},
        headers={"X-Request-Id": "client-supplied-abc123"},
    )
    assert r.status_code == 200
    assert r.headers.get("x-request-id") == "client-supplied-abc123"


def test_request_id_is_generated_when_absent():
    r = client.post("/lookup", json={"gene": "EGFR", "variant": "T790M"})
    assert r.status_code == 200
    rid = r.headers.get("x-request-id")
    assert rid is not None
    assert rid.startswith("req-")
    assert len(rid) == 16  # "req-" + 12 hex chars


def test_kill_switch_returns_503_on_lookup(monkeypatch):
    monkeypatch.setattr(oncokb_proxy_app, "INTEGRATION_ENABLED", False)
    r = client.post("/lookup", json={"gene": "BRAF", "variant": "V600E"})
    assert r.status_code == 503
    assert "disabled" in r.json()["detail"].lower()
    # Healthz remains accessible so operators can diagnose
    h = client.get("/healthz")
    assert h.status_code == 200


def test_scrub_strips_bearer_token():
    from app import scrub
    assert scrub("Bearer abc123def") == "[REDACTED]"
    assert scrub("Authorization: Bearer xyz789") == "Authorization: [REDACTED]"
    assert scrub("api_key=secret123") == "[REDACTED]"
    assert scrub("token: my-token-here") == "[REDACTED]"
    # Idempotent
    assert scrub(scrub("Bearer abc123")) == "[REDACTED]"
    # Doesn't touch unrelated text
    assert scrub("BRAF V600E") == "BRAF V600E"
    assert scrub("") == ""


def test_scrub_is_applied_to_upstream_error_body(monkeypatch):
    """If OncoKB ever echoes our Authorization header in an error body,
    we must strip it before propagating to the client."""

    class _ErrAsyncClient(_FakeAsyncClient):
        async def get(self, url, params=None, headers=None):
            class _Resp:
                status_code = 500

                def json(self):
                    return {}

                @property
                def text(self):
                    return "Upstream error: Bearer test-token-secret was used"

            return _Resp()

    _force_live_mode(monkeypatch)
    monkeypatch.setattr(oncokb_proxy_app.httpx, "AsyncClient", _ErrAsyncClient)

    r = client.post("/lookup", json={"gene": "BRAF", "variant": "V600E"})
    assert r.status_code == 502
    detail = r.json()["detail"]
    assert "test-token-secret" not in detail
    assert "[REDACTED]" in detail


def test_rate_limit_enforced_when_enabled(monkeypatch):
    """Re-enable the limiter, set a tiny budget, verify 429 after exceeding."""
    # Rebuild the limiter with a tight budget. We need a fresh app to apply
    # the limit cleanly because slowapi binds limits at decorator time.
    from importlib import reload
    monkeypatch.setenv("ONCOKB_RATE_LIMIT_DISABLED", "0")
    monkeypatch.setenv("ONCOKB_RATE_LIMIT", "2/minute")

    import app as fresh_app
    reload(fresh_app)
    fresh_client = TestClient(fresh_app.app)

    payload = {"gene": "BRAF", "variant": "V600E"}
    r1 = fresh_client.post("/lookup", json=payload)
    r2 = fresh_client.post("/lookup", json=payload)
    r3 = fresh_client.post("/lookup", json=payload)
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 429

    # Restore default-disabled state for subsequent tests
    monkeypatch.setenv("ONCOKB_RATE_LIMIT_DISABLED", "1")
    reload(fresh_app)
