"""Citation-presence guard — Layer 3 of three independent
citation-verification layers (PR5).

Layer 1 (PR #32 on master, b98e316): PR-time check on `contributions/`
sidecars.
Layer 2 (PR4 on `feat/citation-verifier-src-resolution`): load-time
referential-integrity check (catches 38 unresolved SRC-* refs).
Layer 3 (this module): render-time check at the HTML output for
patient/clinician — emits a visible "❓ без цитати" / "❓ no citation"
badge for any clinical entity (Regimen, Indication, BMA) that fails to
resolve at least one cited source.

Two modes:

- **WARN** (default): badge added inline at the top of the rendered
  block; block content still renders. For current-state KB drift
  visibility.
- **STRICT**: rendered block content is replaced with a placeholder
  ``<div class="stripped-block">[block redacted: missing citation]</div>``.
  For production safety once KB drift is closed out.

Source-collection logic supports the four shapes from PR4's recon:

1. Top-level ``sources: list[str]`` (Regimen)
2. Top-level ``sources: list[Citation-dict]`` with ``source_id`` key
   (Indication)
3. Top-level ``primary_sources: list[str]`` (BMA)
4. Top-level ``evidence_sources: list[dict-with-source-key]`` (BMA)

Nested ``source_refs`` inside ``dose_adjustments`` etc. are out of scope
for this MVP — see brief.

Per OncoKB ToS (CHARTER §2 banned list), `SRC-ONCOKB` is a real Source
entity in the KB even though the render layer filters it from
user-visible output. Citation-presence treats it as resolvable so a BMA
whose only source is ``SRC-ONCOKB`` is not double-penalised.
"""

from __future__ import annotations

import functools
import html
from pathlib import Path
from typing import Iterable, Optional

import yaml


# ── Source-ID lookup (lazy-loaded from disk) ────────────────────────────────


@functools.lru_cache(maxsize=1)
def _load_source_ids() -> frozenset[str]:
    """Return the set of SRC-* IDs defined as Source entities in the
    canonical KB at ``knowledge_base/hosted/content/sources/``.

    Cached. On filesystem failure (missing directory, unreadable YAML),
    returns an empty frozenset — callers must accept that and degrade
    gracefully to "all SRC-* references look broken". This is preferable
    to crashing the render pipeline mid-document.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent
    src_dir = repo_root / "knowledge_base" / "hosted" / "content" / "sources"
    if not src_dir.is_dir():
        return frozenset()
    ids: set[str] = set()
    for p in sorted(src_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            ids.add(data["id"])
    return frozenset(ids)


def clear_source_id_cache() -> None:
    """Clear the lru_cache for ``_load_source_ids``. Tests use this so
    filesystem-backed scenarios stay deterministic across runs.

    Tolerates monkeypatched replacements (which drop the `cache_clear`
    attribute) — the call is best-effort, not a hard contract."""
    fn = globals().get("_load_source_ids")
    if fn is not None and hasattr(fn, "cache_clear"):
        fn.cache_clear()


# ── Source-ID extraction (handles the 4 KB shapes) ──────────────────────────


def _collect_source_ids(entity_data: dict) -> list[str]:
    """Walk an entity-shaped dict and harvest every SRC-* string in the
    fields the brief calls out as in-scope for the MVP guard.

    The same SRC-* ID may appear in more than one field — we keep
    duplicates, because ``cited_count`` is intended to reflect *citation
    intent* density, not distinct-source diversity. The render badge
    only asks "is at least one resolvable?", which doesn't care.
    """
    if not isinstance(entity_data, dict):
        return []
    out: list[str] = []

    # Pattern 1+2: top-level `sources` — either list[str] or list[Citation]
    raw_sources = entity_data.get("sources")
    if isinstance(raw_sources, list):
        for s in raw_sources:
            if isinstance(s, str) and s:
                out.append(s)
            elif isinstance(s, dict):
                # Citation shape (Indication): {source_id: SRC-*, weight?, ...}
                sid = s.get("source_id") or s.get("id")
                if isinstance(sid, str) and sid:
                    out.append(sid)

    # Pattern 3: top-level `primary_sources: list[str]` (BMA)
    raw_primary = entity_data.get("primary_sources")
    if isinstance(raw_primary, list):
        for s in raw_primary:
            if isinstance(s, str) and s:
                out.append(s)

    # Pattern 4: top-level `evidence_sources: list[dict-with-source-key]` (BMA)
    raw_evidence = entity_data.get("evidence_sources")
    if isinstance(raw_evidence, list):
        for es in raw_evidence:
            if isinstance(es, dict):
                sid = es.get("source") or es.get("source_id")
                if isinstance(sid, str) and sid:
                    out.append(sid)

    return out


# ── Citation-status resolver ────────────────────────────────────────────────


def resolve_citation_status(
    entity_data: Optional[dict],
    valid_source_ids: Optional[Iterable[str]] = None,
) -> dict:
    """Compute citation-presence status for one entity.

    Args:
        entity_data: Entity dict loaded from YAML (regimen / indication /
            BMA — or a hit-style flat dict carrying primary_sources /
            evidence_sources). May be None (treated as fully uncited).
        valid_source_ids: Iterable of valid SRC-* IDs to check against.
            None → fall back to the on-disk Source entity set
            (``_load_source_ids()``). Tests pass an explicit set.

    Returns:
        ``{
          "status": "cited" | "uncited" | "broken",
          "cited_count": int,           # SRC-* IDs declared
          "resolved_count": int,        # SRC-* IDs that resolve
          "unresolved_ids": list[str],  # SRC-* IDs that don't resolve
        }``

    Statuses:
        - ``cited``: at least 1 declared SRC-* resolves to a real Source
        - ``uncited``: 0 SRC-* IDs declared (truly unsourced)
        - ``broken``: ≥1 SRC-* declared, but NONE resolve (typos / missing)
    """
    cited = _collect_source_ids(entity_data or {})
    cited_count = len(cited)

    if valid_source_ids is None:
        valid: set[str] | frozenset[str] = _load_source_ids()
    else:
        valid = set(valid_source_ids)

    resolved: list[str] = [s for s in cited if s in valid]
    unresolved: list[str] = [s for s in cited if s not in valid]

    if cited_count == 0:
        status = "uncited"
    elif len(resolved) == 0:
        status = "broken"
    else:
        status = "cited"

    return {
        "status": status,
        "cited_count": cited_count,
        "resolved_count": len(resolved),
        "unresolved_ids": unresolved,
    }


# ── HTML emission helpers ───────────────────────────────────────────────────


_BADGE_LABEL = {
    "uk": "❓ без цитати",
    "en": "❓ no citation",
}

_STRIPPED_LABEL = {
    "uk": "[блок видалено: відсутня цитата]",
    "en": "[block redacted: missing citation]",
}


def _badge_label(target_lang: str) -> str:
    return _BADGE_LABEL.get(
        "en" if (target_lang or "uk").lower().startswith("en") else "uk",
        _BADGE_LABEL["uk"],
    )


def _stripped_label(target_lang: str) -> str:
    return _STRIPPED_LABEL.get(
        "en" if (target_lang or "uk").lower().startswith("en") else "uk",
        _STRIPPED_LABEL["uk"],
    )


def render_citation_warn_badge(target_lang: str = "uk") -> str:
    """Emit the inline warn-mode badge HTML. Caller decides where to
    insert it (top of block, beside <dt>, etc.)."""
    return (
        '<aside class="no-citation-badge" role="note">'
        f'{html.escape(_badge_label(target_lang))}'
        '</aside>'
    )


def render_stripped_block(target_lang: str = "uk") -> str:
    """Emit the strict-mode placeholder that replaces a block's content
    when the entity has no resolvable citation."""
    return (
        '<div class="stripped-block">'
        f'{html.escape(_stripped_label(target_lang))}'
        '</div>'
    )


def needs_guard(status: str) -> bool:
    """``True`` when the entity should be flagged (badge or strip) —
    i.e. status is ``uncited`` or ``broken``. ``cited`` passes through."""
    return status in ("uncited", "broken")


__all__ = [
    "_load_source_ids",
    "clear_source_id_cache",
    "resolve_citation_status",
    "render_citation_warn_badge",
    "render_stripped_block",
    "needs_guard",
]
