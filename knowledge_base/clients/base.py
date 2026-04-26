"""BaseSourceClient + CacheBackend + TokenBucket — shared infrastructure for
referenced-source live API clients.

Per specs/SOURCE_INGESTION_SPEC.md §12.2 and §12.3. Concrete clients
(CT.gov, PubMed, DailyMed, openFDA) inherit from `BaseSourceClient[Q, R]`,
where Q is a per-source dataclass query type and R is the raw response
payload type. Each concrete client overrides `_fetch_raw(query)` only —
caching, rate-limiting, error capture, and SourceResponse construction
all live here.

Test substitution happens at the **CacheBackend** seam: production injects
`DiskCacheBackend(root=knowledge_base/cache)`, tests inject
`InMemoryCacheBackend()`. The seam is real — two adapters justify it.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generic, Optional, Protocol, TypeVar


# ── Public data classes ──────────────────────────────────────────────────────


@dataclass
class RateLimit:
    """How often a concrete client may hit its upstream. Enforced by a
    `TokenBucket` constructed from this in `BaseSourceClient.__init__`."""

    tokens_per_second: float
    burst: int = 1


@dataclass
class SourceResponse:
    """Wrapper around a raw upstream payload + provenance fields a caller
    needs to attach a Source citation."""

    data: Any
    source_id: str
    fetched_at: str  # ISO-8601
    cache_hit: bool = False
    api_version: Optional[str] = None


# ── Cache backend port ───────────────────────────────────────────────────────


class CacheBackend(Protocol):
    """Where SourceResponses live between calls. Real seam: prod uses
    `DiskCacheBackend`, tests use `InMemoryCacheBackend`."""

    def get(self, key: str) -> Optional[SourceResponse]: ...

    def put(self, key: str, value: SourceResponse, ttl_seconds: int) -> None: ...

    def invalidate(self, key: str) -> None: ...


@dataclass
class _CacheEntry:
    value: SourceResponse
    expires_at: float


class InMemoryCacheBackend:
    """Ephemeral, per-process. Default for tests and the CLI when no
    cache root is configured."""

    def __init__(self) -> None:
        self._mem: dict[str, _CacheEntry] = {}

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

    def invalidate(self, key: str) -> None:
        self._mem.pop(key, None)


class DiskCacheBackend:
    """Write-through cache: in-memory first, JSON files under
    `<root>/<source_id>/<key>.json` for cross-run persistence. Used in CI
    and local dev to avoid hammering upstream APIs."""

    def __init__(self, root: Path) -> None:
        self._mem = InMemoryCacheBackend()
        self._root = Path(root)

    def _path_for(self, key: str) -> Path:
        # The first 6 chars of the hash become a sharding directory so that
        # a long-running cache doesn't end up with 100k files in one dir.
        return self._root / key[:6] / f"{key}.json"

    def get(self, key: str) -> Optional[SourceResponse]:
        hit = self._mem.get(key)
        if hit is not None:
            return hit
        p = self._path_for(key)
        if not p.is_file():
            return None
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if payload.get("expires_at", 0) < time.time():
            return None
        resp = SourceResponse(
            data=payload["data"],
            source_id=payload["source_id"],
            fetched_at=payload["fetched_at"],
            cache_hit=True,
            api_version=payload.get("api_version"),
        )
        # Promote into memory for the rest of the process.
        self._mem.put(key, resp, max(1, int(payload["expires_at"] - time.time())))
        return resp

    def put(self, key: str, value: SourceResponse, ttl_seconds: int) -> None:
        self._mem.put(key, value, ttl_seconds)
        p = self._path_for(key)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "data": value.data,
            "source_id": value.source_id,
            "fetched_at": value.fetched_at,
            "api_version": value.api_version,
            "expires_at": time.time() + ttl_seconds,
        }
        p.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")

    def invalidate(self, key: str) -> None:
        self._mem.invalidate(key)
        p = self._path_for(key)
        if p.is_file():
            p.unlink()


# ── Token bucket rate limiter ────────────────────────────────────────────────


class TokenBucket:
    """Thread-safe token bucket. `acquire()` blocks until a token is
    available, sleeping the deficit if needed.

    Concrete clients construct one of these from their declared `RateLimit`;
    `BaseSourceClient.fetch` calls `acquire()` before every upstream call,
    even on cache miss. Cache hits do not consume a token.
    """

    def __init__(self, tokens_per_second: float, burst: int = 1) -> None:
        self._rate = float(tokens_per_second)
        self._burst = max(1, int(burst))
        self._tokens = float(self._burst)
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            self._tokens = min(self._burst, self._tokens + (now - self._last) * self._rate)
            self._last = now
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return
            sleep_for = (1.0 - self._tokens) / self._rate
        # Release the lock before sleeping so other threads can replenish.
        time.sleep(sleep_for)
        with self._lock:
            self._tokens = 0.0
            self._last = time.monotonic()


# ── Base source client ───────────────────────────────────────────────────────


Q = TypeVar("Q")  # per-source query dataclass
R = TypeVar("R")  # raw payload type returned by upstream


class BaseSourceClient(ABC, Generic[Q, R]):
    """Deep module: HTTP+cache+rate-limit live here. Concrete clients
    declare three class attributes and override `_fetch_raw` only.

    Required class attributes on the subclass:
        source_id: str          — e.g. "SRC-PUBMED"
        rate_limit: RateLimit   — tokens/sec + burst for the upstream
        cache_ttl_seconds: int  — how long a SourceResponse stays fresh

    Optional:
        api_version: str        — stamped into SourceResponse.api_version
    """

    source_id: str
    rate_limit: RateLimit
    cache_ttl_seconds: int
    api_version: Optional[str] = None

    def __init__(self, cache: Optional[CacheBackend] = None) -> None:
        self._cache: CacheBackend = cache or InMemoryCacheBackend()
        self._limiter = TokenBucket(self.rate_limit.tokens_per_second, self.rate_limit.burst)
        self._last_error: Optional[str] = None

    # ── Public interface (callers cross this seam) ────────────────────────

    def fetch(self, query: Q) -> SourceResponse:
        key = self._cache_key(query)
        cached = self._cache.get(key)
        if cached is not None:
            cached.cache_hit = True
            return cached

        self._limiter.acquire()
        try:
            data, api_version = self._fetch_raw(query)
        except Exception as exc:  # noqa: BLE001 — propagate but record
            self._last_error = str(exc)
            raise

        resp = SourceResponse(
            data=data,
            source_id=self.source_id,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            cache_hit=False,
            api_version=api_version or self.api_version,
        )
        self._cache.put(key, resp, self.cache_ttl_seconds)
        return resp

    def health(self) -> dict:
        """Default healthcheck — concrete clients override with a cheap
        upstream call when one exists."""
        return {"ok": self._last_error is None, "latency_ms": None, "last_error": self._last_error}

    def quota(self) -> dict:
        return {"remaining": None, "reset_at": None}

    # ── Subclass hook ────────────────────────────────────────────────────

    @abstractmethod
    def _fetch_raw(self, query: Q) -> tuple[R, Optional[str]]:
        """Make the upstream call. Return (raw_payload, api_version_str)."""
        raise NotImplementedError

    # ── Internals ────────────────────────────────────────────────────────

    def _cache_key(self, query: Q) -> str:
        if is_dataclass(query):
            canonical = json.dumps(asdict(query), sort_keys=True, default=str)
        elif isinstance(query, dict):
            canonical = json.dumps(query, sort_keys=True, default=str)
        else:
            canonical = repr(query)
        raw = f"{self.source_id}|{canonical}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


__all__ = [
    "BaseSourceClient",
    "CacheBackend",
    "DiskCacheBackend",
    "InMemoryCacheBackend",
    "RateLimit",
    "SourceResponse",
    "TokenBucket",
]
