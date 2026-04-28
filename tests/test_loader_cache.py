"""Tests for the load_content() module-level cache.

Skill candidate #5 — KB loader caching. The cache is keyed on the resolved
KB path, so callers don't pay the YAML+Pydantic walk twice for the same
content. A 99×2 batch build (parallel + sequential) was eating ~400 redundant
load_content() calls before this; tests cement the contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from knowledge_base.validation.loader import (
    LoadResult,
    _LOAD_CACHE,
    clear_load_cache,
    load_content,
)


@pytest.fixture
def kb_root() -> Path:
    return Path("knowledge_base/hosted/content")


@pytest.fixture(autouse=True)
def _isolate_cache():
    """Each test starts with an empty cache and leaves it empty."""
    clear_load_cache()
    yield
    clear_load_cache()


def test_first_call_populates_cache(kb_root: Path):
    assert _LOAD_CACHE == {}
    result = load_content(kb_root)
    assert isinstance(result, LoadResult)
    assert len(_LOAD_CACHE) == 1


def test_second_call_returns_same_instance(kb_root: Path):
    """Cache hit must return the *same* LoadResult — not a copy. Callers
    rely on object identity (e.g., `result1 is result2`)."""
    r1 = load_content(kb_root)
    r2 = load_content(kb_root)
    assert r1 is r2


def test_relative_and_absolute_paths_share_cache(kb_root: Path):
    """The resolved-path key normalises so that a relative call and an
    absolute call to the same directory hit one entry."""
    r_rel = load_content(kb_root)
    r_abs = load_content(kb_root.resolve())
    assert r_rel is r_abs
    assert len(_LOAD_CACHE) == 1


def test_distinct_roots_get_distinct_entries(tmp_path: Path, kb_root: Path):
    """Two different KB roots must not share a cache entry."""
    # Synthesize a minimal alternative KB with one disease YAML.
    alt_root = tmp_path / "alt_kb"
    (alt_root / "diseases").mkdir(parents=True)
    (alt_root / "diseases" / "fake.yaml").write_text(
        "id: DIS-FAKE\nname: Fake Disease\nicd_o_3_morphology: '9999/9'\n",
        encoding="utf-8",
    )
    real = load_content(kb_root)
    fake = load_content(alt_root)
    assert real is not fake
    assert len(_LOAD_CACHE) == 2


def test_clear_cache_drops_all_entries(kb_root: Path):
    load_content(kb_root)
    assert len(_LOAD_CACHE) == 1
    clear_load_cache()
    assert _LOAD_CACHE == {}
    # And the next call rebuilds.
    r = load_content(kb_root)
    assert isinstance(r, LoadResult)
    assert len(_LOAD_CACHE) == 1
