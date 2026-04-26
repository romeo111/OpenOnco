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
from dataclasses import dataclass
from typing import Any, Literal, Optional

from .base import BaseSourceClient, CacheBackend, RateLimit, SourceResponse

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


@dataclass
class OpenFDAQuery:
    """openFDA endpoint dispatch + free-text search expression."""

    endpoint: Literal["label", "recall"] = "label"
    search: str = ""
    limit: int = 10


class OpenFDAClient(BaseSourceClient[OpenFDAQuery, dict]):
    """SourceClient for openFDA."""

    source_id = "SRC-OPENFDA"
    rate_limit = RateLimit(tokens_per_second=4.0, burst=10)  # 240/min without key
    cache_ttl_seconds = 24 * 3600  # 1 day
    api_version = "openFDA"

    def _fetch_raw(self, query: OpenFDAQuery) -> tuple[dict, Optional[str]]:
        if query.endpoint == "label":
            return drug_label_search(query.search, limit=query.limit), self.api_version
        if query.endpoint == "recall":
            return drug_recalls(query.search, limit=query.limit), self.api_version
        raise ValueError(f"Unknown openFDA endpoint: {query.endpoint!r}")

    def health(self) -> dict:
        try:
            drug_label_search("aspirin", limit=1)
            return {"ok": True, "latency_ms": None, "last_error": None}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "latency_ms": None, "last_error": str(e)}

    def quota(self) -> dict:
        if os.environ.get("OPENFDA_API_KEY"):
            return {"remaining": "up to 120000/day with key", "reset_at": None}
        return {"remaining": "240/min without key", "reset_at": None}
