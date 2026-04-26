"""Tests at the BaseSourceClient interface — the seam where every concrete
source client (CTGov, PubMed, DailyMed, openFDA) plugs in.

The interface is the test surface (per .claude/skills/improve-codebase-architecture/
DEEPENING.md). We exercise cache hit/miss/expiry, rate-limit acquire,
error capture, and CacheBackend substitution through a minimal in-process
fake — no network.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest

from knowledge_base.clients.base import (
    BaseSourceClient,
    DiskCacheBackend,
    InMemoryCacheBackend,
    RateLimit,
    SourceResponse,
    TokenBucket,
)


# ── Test doubles ─────────────────────────────────────────────────────────────


@dataclass
class _FakeQuery:
    term: str
    n: int = 1


class _FakeClient(BaseSourceClient[_FakeQuery, dict]):
    """Concrete BaseSourceClient that does not hit the network — the
    upstream call is just a counter we can assert against."""

    source_id = "SRC-FAKE"
    rate_limit = RateLimit(tokens_per_second=1000.0, burst=1000)  # effectively unlimited
    cache_ttl_seconds = 60
    api_version = "fake-1"

    def __init__(self, cache=None) -> None:
        super().__init__(cache=cache)
        self.fetch_count = 0
        self.next_error: Optional[Exception] = None

    def _fetch_raw(self, query: _FakeQuery) -> tuple[dict, Optional[str]]:
        if self.next_error is not None:
            raise self.next_error
        self.fetch_count += 1
        return {"echo": query.term, "n": query.n}, self.api_version


# ── BaseSourceClient: cache behaviour ────────────────────────────────────────


def test_first_call_misses_cache_and_invokes_upstream():
    c = _FakeClient()
    resp = c.fetch(_FakeQuery(term="aspirin"))
    assert resp.cache_hit is False
    assert resp.data == {"echo": "aspirin", "n": 1}
    assert resp.source_id == "SRC-FAKE"
    assert resp.api_version == "fake-1"
    assert c.fetch_count == 1


def test_second_identical_call_hits_cache_no_upstream():
    c = _FakeClient()
    c.fetch(_FakeQuery(term="aspirin"))
    second = c.fetch(_FakeQuery(term="aspirin"))
    assert second.cache_hit is True
    assert c.fetch_count == 1, "upstream should not be called again on cache hit"


def test_distinct_queries_distinct_cache_entries():
    c = _FakeClient()
    c.fetch(_FakeQuery(term="aspirin"))
    c.fetch(_FakeQuery(term="ibuprofen"))
    c.fetch(_FakeQuery(term="aspirin", n=2))  # different field => different key
    assert c.fetch_count == 3


def test_expired_entry_refetches():
    c = _FakeClient()
    c.cache_ttl_seconds = 0  # expire immediately
    c.fetch(_FakeQuery(term="aspirin"))
    time.sleep(0.001)
    c.fetch(_FakeQuery(term="aspirin"))
    assert c.fetch_count == 2


def test_upstream_error_is_recorded_and_propagated():
    c = _FakeClient()
    c.next_error = RuntimeError("upstream 503")
    with pytest.raises(RuntimeError, match="upstream 503"):
        c.fetch(_FakeQuery(term="aspirin"))
    assert c._last_error == "upstream 503"
    health = c.health()
    assert health["ok"] is False
    assert health["last_error"] == "upstream 503"


# ── CacheBackend substitution ────────────────────────────────────────────────


def test_in_memory_backend_is_default(tmp_path):
    c = _FakeClient()
    assert isinstance(c._cache, InMemoryCacheBackend)


def test_disk_backend_persists_across_clients(tmp_path: Path):
    backend1 = DiskCacheBackend(root=tmp_path)
    c1 = _FakeClient(cache=backend1)
    c1.fetch(_FakeQuery(term="aspirin"))

    # New process simulation: brand-new backend pointing at the same root,
    # brand-new client. Should hit on disk, not call upstream.
    backend2 = DiskCacheBackend(root=tmp_path)
    c2 = _FakeClient(cache=backend2)
    second = c2.fetch(_FakeQuery(term="aspirin"))
    assert second.cache_hit is True
    assert c2.fetch_count == 0, "second process must hit the disk cache"


def test_in_memory_backend_invalidate():
    backend = InMemoryCacheBackend()
    c = _FakeClient(cache=backend)
    resp = c.fetch(_FakeQuery(term="aspirin"))
    key = c._cache_key(_FakeQuery(term="aspirin"))
    assert backend.get(key) is not None
    backend.invalidate(key)
    assert backend.get(key) is None


# ── TokenBucket ──────────────────────────────────────────────────────────────


def test_token_bucket_burst_does_not_block():
    tb = TokenBucket(tokens_per_second=1.0, burst=5)
    start = time.monotonic()
    for _ in range(5):
        tb.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 0.05, f"burst should not block: {elapsed=}"


def test_token_bucket_blocks_after_burst():
    tb = TokenBucket(tokens_per_second=20.0, burst=2)
    tb.acquire()  # consume burst token 1
    tb.acquire()  # consume burst token 2
    start = time.monotonic()
    tb.acquire()  # must wait ~50 ms for next token
    elapsed = time.monotonic() - start
    assert 0.02 < elapsed < 0.2, f"expected ~50ms wait, got {elapsed=}"


# ── _cache_key determinism ──────────────────────────────────────────────────


def test_cache_key_is_field_order_independent():
    c = _FakeClient()
    k1 = c._cache_key(_FakeQuery(term="x", n=2))
    k2 = c._cache_key(_FakeQuery(n=2, term="x"))
    assert k1 == k2


def test_cache_key_includes_source_id():
    """Two different concrete clients with structurally identical queries
    must not collide in a shared cache."""

    class _OtherFakeClient(_FakeClient):
        source_id = "SRC-OTHER"

    c1 = _FakeClient()
    c2 = _OtherFakeClient()
    assert c1._cache_key(_FakeQuery(term="x")) != c2._cache_key(_FakeQuery(term="x"))
