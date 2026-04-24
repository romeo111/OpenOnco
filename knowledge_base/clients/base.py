"""SourceClient protocol + TTLCache for referenced-source live API calls.

Per specs/SOURCE_INGESTION_SPEC.md §12.2 and §12.3. All concrete
clients (CT.gov, PubMed, DailyMed, openFDA, OncoKB, ClinVar, gnomAD)
implement this interface.

Implementations live in sibling modules (ctgov_client.py etc.) and are
not all written yet — see TODO.md §7.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Protocol, runtime_checkable


# ── Data classes ──────────────────────────────────────────────────────────────


@dataclass
class RateLimit:
    tokens_per_second: float
    burst: int = 1


@dataclass
class SourceResponse:
    data: Any
    source_id: str
    fetched_at: str  # ISO-8601
    cache_hit: bool = False
    api_version: Optional[str] = None


# ── Protocol ──────────────────────────────────────────────────────────────────


@runtime_checkable
class SourceClient(Protocol):
    """Interface all live-API source clients conform to."""

    source_id: str
    base_url: str
    rate_limit: RateLimit
    cache_ttl_seconds: int

    def fetch(self, query: dict) -> SourceResponse: ...

    def health(self) -> dict: ...
    # {ok: bool, latency_ms: int, last_error: Optional[str]}

    def quota(self) -> dict: ...
    # {remaining: Optional[int], reset_at: Optional[str]}


# ── TTL cache ─────────────────────────────────────────────────────────────────


@dataclass
class _CacheEntry:
    value: SourceResponse
    expires_at: float


class TTLCache:
    """Very small in-memory + optional on-disk TTL cache. On-disk scope
    is per-source under `knowledge_base/cache/<source>/<hash>.json`."""

    def __init__(self, cache_root: Optional[Path] = None):
        self._mem: dict[str, _CacheEntry] = {}
        self._root = cache_root

    @staticmethod
    def key_for(source_id: str, endpoint: str, params: dict) -> str:
        """Deterministic cache key for a given source+endpoint+params."""
        canonical = json.dumps(params, sort_keys=True, default=str)
        raw = f"{source_id}|{endpoint}|{canonical}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def get(self, key: str) -> Optional[SourceResponse]:
        entry = self._mem.get(key)
        if entry is None:
            return None
        if entry.expires_at < time.time():
            self._mem.pop(key, None)
            return None
        return entry.value

    def put(self, key: str, value: SourceResponse, ttl_seconds: int) -> None:
        self._mem[key] = _CacheEntry(value=value, expires_at=time.time() + ttl_seconds)
        # Disk persistence left for concrete clients to opt into.

    def invalidate(self, key: str) -> None:
        self._mem.pop(key, None)


__all__ = ["RateLimit", "SourceClient", "SourceResponse", "TTLCache"]
