"""DailyMed REST API client.

Per specs/SOURCE_INGESTION_SPEC §16.3 — referenced-mode live API for
FDA drug labels. Endpoint: https://dailymed.nlm.nih.gov/dailymed/services/v2/

Rate limit: NLM doesn't enforce strict limits; be polite (~1 req/sec).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Literal, Optional

from .base import BaseSourceClient, CacheBackend, RateLimit, SourceResponse

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


@dataclass
class DailyMedQuery:
    """Either a label search by drug name (mode='search') or a label
    fetch by SPL set_id (mode='get')."""

    mode: Literal["search", "get"] = "search"
    name: Optional[str] = None
    set_id: Optional[str] = None
    page_size: int = 10


class DailyMedClient(BaseSourceClient[DailyMedQuery, dict]):
    """SourceClient for DailyMed."""

    source_id = "SRC-DAILYMED"
    rate_limit = RateLimit(tokens_per_second=1.0, burst=2)
    cache_ttl_seconds = 7 * 24 * 3600  # 7 days
    api_version = "v2"

    def __init__(self, cache: Optional[CacheBackend] = None) -> None:
        super().__init__(cache=cache)

    def _fetch_raw(self, query: DailyMedQuery) -> tuple[dict, Optional[str]]:
        if query.mode == "get":
            if not query.set_id:
                raise ValueError("DailyMedQuery.mode='get' requires set_id")
            return get_label(query.set_id), self.api_version
        return search_labels(query.name or "", page_size=query.page_size), self.api_version

    def health(self) -> dict:
        try:
            search_labels("aspirin", page_size=1)
            return {"ok": True, "latency_ms": None, "last_error": None}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "latency_ms": None, "last_error": str(e)}
