"""openFDA REST API client.

Per specs/SOURCE_INGESTION_SPEC §16.3 — referenced-mode live API for
FDA drug labels, recalls, and adverse events.
Endpoint: https://api.fda.gov

Rate limit: 240 req/min without key, 120K/day with free API key.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from .base import RateLimit, SourceResponse, TTLCache

OPENFDA_BASE = "https://api.fda.gov"
USER_AGENT = "OpenOnco/0.1 (https://github.com/romeo111/cancer-autoresearch)"


def _http_get(path: str, params: dict[str, Any]) -> dict:
    api_key = os.environ.get("OPENFDA_API_KEY")
    if api_key:
        params = {**params, "api_key": api_key}
    qs = urllib.parse.urlencode(params)
    url = f"{OPENFDA_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def drug_label_search(query: str, limit: int = 10) -> dict:
    return _http_get("/drug/label.json", {"search": query, "limit": limit})


def drug_recalls(query: str, limit: int = 10) -> dict:
    return _http_get("/drug/enforcement.json", {"search": query, "limit": limit})


class OpenFDAClient:
    """SourceClient for openFDA."""

    source_id = "SRC-OPENFDA"
    base_url = OPENFDA_BASE
    rate_limit = RateLimit(tokens_per_second=4.0, burst=10)  # 240/min without key
    cache_ttl_seconds = 24 * 3600  # 1 day

    def __init__(self, cache: TTLCache | None = None):
        self._cache = cache or TTLCache()
        self._last_error: str | None = None

    def fetch(self, query: dict) -> SourceResponse:
        endpoint = query.get("endpoint", "label")
        key = TTLCache.key_for(self.source_id, endpoint, query)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        try:
            if endpoint == "label":
                data = drug_label_search(query["search"], limit=query.get("limit", 10))
            elif endpoint == "recall":
                data = drug_recalls(query["search"], limit=query.get("limit", 10))
            else:
                raise ValueError(f"Unknown openFDA endpoint: {endpoint}")
        except Exception as e:
            self._last_error = str(e)
            raise

        resp = SourceResponse(
            data=data,
            source_id=self.source_id,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            cache_hit=False,
            api_version="openFDA",
        )
        self._cache.put(key, resp, self.cache_ttl_seconds)
        return resp

    def health(self) -> dict:
        try:
            drug_label_search("aspirin", limit=1)
            return {"ok": True, "latency_ms": None, "last_error": None}
        except Exception as e:
            return {"ok": False, "latency_ms": None, "last_error": str(e)}

    def quota(self) -> dict:
        if os.environ.get("OPENFDA_API_KEY"):
            return {"remaining": "up to 120000/day with key", "reset_at": None}
        return {"remaining": "240/min without key", "reset_at": None}
