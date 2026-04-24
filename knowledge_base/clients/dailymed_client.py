"""DailyMed REST API client.

Per specs/SOURCE_INGESTION_SPEC §16.3 — referenced-mode live API for
FDA drug labels. Endpoint: https://dailymed.nlm.nih.gov/dailymed/services/v2/

Rate limit: NLM doesn't enforce strict limits; be polite (~1 req/sec).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from .base import RateLimit, SourceResponse, TTLCache

DAILYMED_BASE = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
USER_AGENT = "OpenOnco/0.1 (https://github.com/romeo111/cancer-autoresearch)"


def _http_get(path: str, params: dict[str, Any]) -> dict:
    qs = urllib.parse.urlencode(params)
    url = f"{DAILYMED_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_labels(name: str, page_size: int = 10) -> dict:
    return _http_get("/spls.json", {"drug_name": name, "pagesize": page_size})


def get_label(set_id: str) -> dict:
    return _http_get(f"/spls/{set_id}.json", {})


class DailyMedClient:
    """SourceClient for DailyMed."""

    source_id = "SRC-DAILYMED"
    base_url = DAILYMED_BASE
    rate_limit = RateLimit(tokens_per_second=1.0, burst=2)
    cache_ttl_seconds = 7 * 24 * 3600  # 7 days

    def __init__(self, cache: TTLCache | None = None):
        self._cache = cache or TTLCache()
        self._last_error: str | None = None

    def fetch(self, query: dict) -> SourceResponse:
        mode = query.get("mode", "search")
        key = TTLCache.key_for(self.source_id, mode, query)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        try:
            if mode == "get":
                data = get_label(query["set_id"])
            else:
                data = search_labels(query.get("name", ""), page_size=query.get("page_size", 10))
        except Exception as e:
            self._last_error = str(e)
            raise

        resp = SourceResponse(
            data=data,
            source_id=self.source_id,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            cache_hit=False,
            api_version="v2",
        )
        self._cache.put(key, resp, self.cache_ttl_seconds)
        return resp

    def health(self) -> dict:
        try:
            _http_get("/spls.json", {"drug_name": "aspirin", "pagesize": 1})
            return {"ok": True, "latency_ms": None, "last_error": None}
        except Exception as e:
            return {"ok": False, "latency_ms": None, "last_error": str(e)}

    def quota(self) -> dict:
        return {"remaining": None, "reset_at": None}
