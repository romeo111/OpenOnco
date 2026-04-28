"""SnapshotCIViCClient — read CIViC nightly YAML snapshot, fusion-aware lookup.

Phase 2 of the CIViC pivot. Replaces the live HTTP client (deleted) and the
NotImplementedError placeholder in ``actionability_client.SnapshotActionabilityClient``.

Why a separate class instead of replacing ``SnapshotActionabilityClient``:
``tests/test_actionability_invariants.py::test_snapshot_client_lookup_not_implemented``
locks the placeholder behaviour as a baseline contract (the safe-rollout
firewall test treats the *placeholder* as a Phase-1 deliverable). Per the
implementation brief's allowlist this test must not be modified, so the
canonical Phase-2 reader lives here and callers select it explicitly. The
placeholder remains as documentation of "Phase 2 lives at this name" for any
codepath that imported it before the pivot. A follow-up cleanup pass (Phase
4) can collapse the two once the invariant test is updated to assert the new
behaviour.

Source contract:
- Reads the nightly snapshot under ``knowledge_base/hosted/civic/<date>/evidence.yaml``.
- CIViC license is CC0 — fully redistributable. Surfaceable per CHARTER §2.
- OncoKB is forbidden under our ToS audit; this client never consults OncoKB
  even if a query carries OncoKB-flavoured context.

Lookup is sub-millisecond after init thanks to a per-gene index built once.
The matcher is fusion-aware (delegates to
``knowledge_base.engine.civic_variant_matcher.matches_civic_entry``) so a
query like ``(ABL1, T315I)`` correctly hits a CIViC entry with
``gene="BCR::ABL1", variant="Fusion AND ABL1 T315I"``.

Surfacing rules — see module-level constants below.

Per safe-rollout v3 §0 invariant 3 (fail-open): per-query failure modes
return ``ActionabilityError`` instead of raising. Init-time failure
(missing/unreadable file) does raise — that is a caller bug, not a
runtime fault.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import yaml

from .actionability_types import (
    ActionabilityError,
    ActionabilityQuery,
    ActionabilityResult,
    ActionabilityTherapeuticOption,
)
from .civic_variant_matcher import matches_civic_entry, split_fusion_components

__all__ = [
    "SnapshotCIViCClient",
    "CIVIC_SURFACED_LEVELS",
    "CIVIC_RESISTANCE_DIRECTIONS",
]

_LOG = logging.getLogger(__name__)


# ── Surfacing policy (caller filters; client returns everything) ─────────

# Levels A/B/C/D surface in the rendered HCP layer. Level E is preclinical /
# inferential — too low confidence to surface. The client returns level-E
# evidence regardless; render layer is responsible for applying this filter
# (separation of concerns: client = data, render = policy).
CIVIC_SURFACED_LEVELS: frozenset[str] = frozenset({"A", "B", "C", "D"})

# CIViC encodes resistance via direction="Does Not Support" on a Predictive
# evidence_type with significance="Sensitivity/Response", or via
# direction="Supports" with significance="Resistance". The first axis maps
# functionally to OncoKB R1/R2 — preserve verbatim in the option description
# so the render layer can flag it. The second axis is captured by the
# significance field (also surfaced in description).
CIVIC_RESISTANCE_DIRECTIONS: frozenset[str] = frozenset({"Does Not Support"})


# Required keys on a CIViC evidence_item — items missing any of these are
# skipped at init with a warning. Matches the schema produced by
# scripts/refresh_civic_snapshot.py.
_REQUIRED_FIELDS: tuple[str, ...] = ("gene", "variant", "evidence_level")


# ── Client ───────────────────────────────────────────────────────────────


class SnapshotCIViCClient:
    """Reads a CIViC nightly snapshot YAML once, serves ActionabilityResult.

    CIViC is CC0 — surfaceable per CHARTER §2. OncoKB is forbidden; if a
    query somehow references OncoKB context, this client ignores it and
    answers from CIViC only.

    Usage:
        client = SnapshotCIViCClient("knowledge_base/hosted/civic/2026-04-25/evidence.yaml")
        result = client.lookup(ActionabilityQuery(gene="BRAF", variant="V600E", ...))

    Construction is O(n_evidence) (single linear pass to build the per-gene
    index). Lookup is O(n_entries_for_query.gene), typically <20.
    """

    def __init__(self, snapshot_path: Path | str) -> None:
        self._path = Path(snapshot_path)
        if not self._path.exists():
            raise FileNotFoundError(
                f"CIViC snapshot not found at {self._path}. "
                f"Run scripts/refresh_civic_snapshot.py to fetch one."
            )
        with self._path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(
                f"CIViC snapshot at {self._path} did not parse as a mapping; "
                f"got {type(data).__name__}"
            )

        self._snapshot_date: Optional[str] = data.get("snapshot_date")
        evidence_items = data.get("evidence_items") or []
        if not isinstance(evidence_items, list):
            raise ValueError(
                f"CIViC snapshot at {self._path}: 'evidence_items' is not a list"
            )

        # Build the per-gene index. For fusion entries (e.g. "BCR::ABL1") we
        # index under every component HGNC symbol (BCR, ABL1) AND under the
        # raw fusion symbol — so both ``query_gene="ABL1"`` and a hypothetical
        # ``query_gene="BCR::ABL1"`` can hit it.
        self._gene_index: dict[str, list[dict[str, Any]]] = {}
        skipped = 0
        kept = 0
        for raw in evidence_items:
            if not isinstance(raw, dict):
                skipped += 1
                continue
            if not all(raw.get(k) for k in _REQUIRED_FIELDS):
                _LOG.warning(
                    "CIViC snapshot: skipping malformed evidence item id=%r "
                    "(missing one of %s)",
                    raw.get("id"),
                    _REQUIRED_FIELDS,
                )
                skipped += 1
                continue
            kept += 1
            civic_gene = str(raw["gene"])
            keys = {civic_gene.upper()}
            for component in split_fusion_components(civic_gene):
                keys.add(component.upper())
            for key in keys:
                self._gene_index.setdefault(key, []).append(raw)

        self._kept_count = kept
        self._skipped_count = skipped
        _LOG.info(
            "Loaded CIViC snapshot from %s — %d items indexed across %d gene keys "
            "(skipped %d malformed)",
            self._path,
            kept,
            len(self._gene_index),
            skipped,
        )

    # ── Public API ──────────────────────────────────────────────────────

    def lookup(
        self, query: ActionabilityQuery
    ) -> ActionabilityResult | ActionabilityError:
        """Return matching CIViC evidence as ActionabilityResult.

        Returns an empty (negative) ActionabilityResult — never an error —
        for unknown gene or known-gene-no-matching-variant. ActionabilityError
        is reserved for true failure modes (none of those exist in this
        snapshot-based client; method retained for Protocol compatibility).
        """

        try:
            return self._lookup_impl(query)
        except Exception as exc:  # pragma: no cover - defensive fail-open
            _LOG.exception(
                "CIViC lookup raised for query %s — returning ActionabilityError",
                query,
            )
            return ActionabilityError(
                query=query,
                error_kind="parse_error",
                detail=f"CIViC snapshot lookup failed: {exc}",
            )

    def batch_lookup(
        self, queries: list[ActionabilityQuery]
    ) -> list[ActionabilityResult | ActionabilityError]:
        return [self.lookup(q) for q in queries]

    # ── Internals ───────────────────────────────────────────────────────

    def _lookup_impl(self, query: ActionabilityQuery) -> ActionabilityResult:
        gene_key = (query.gene or "").strip().upper()
        candidates = self._gene_index.get(gene_key, [])

        matched: list[dict[str, Any]] = []
        for entry in candidates:
            if matches_civic_entry(
                query_gene=query.gene,
                query_variant=query.variant,
                civic_gene=str(entry.get("gene", "")),
                civic_variant=str(entry.get("variant", "")),
            ):
                matched.append(entry)

        therapeutic_options = tuple(
            opt
            for opt in (_evidence_to_option(e) for e in matched)
            if opt is not None
        )

        source_url = _pick_source_url(query.gene, matched)

        return ActionabilityResult(
            query=query,
            source_url=source_url,
            therapeutic_options=therapeutic_options,
            cached=True,
            data_version=self._snapshot_date,
        )


# ── Helpers (module-level, easy to unit-test) ────────────────────────────


def _evidence_to_option(
    entry: dict[str, Any],
) -> ActionabilityTherapeuticOption | None:
    """Convert a single CIViC evidence_item dict into a therapeutic option.

    Returns None if the entry has no therapies (filtered — a diagnostic /
    prognostic evidence item with no drug attached is not a 'therapeutic'
    option in the ActionabilityResult sense).
    """

    therapies_raw = entry.get("therapies") or []
    if not therapies_raw:
        return None
    drugs = tuple(str(t) for t in therapies_raw if t)
    if not drugs:
        return None

    description = _build_description(entry)

    pmids: tuple[str, ...] = ()
    citation_source_type = entry.get("citation_source_type")
    citation_id = entry.get("citation_id")
    if citation_source_type == "PubMed" and citation_id:
        pmids = (str(citation_id),)

    return ActionabilityTherapeuticOption(
        level=str(entry.get("evidence_level", "?")),
        drugs=drugs,
        description=description,
        pmids=pmids,
        # CIViC does not track FDA approval status; the Drug entity in our
        # KB owns that field. Leave default (False / None).
        fda_approved=False,
        fda_approval_year=None,
    )


def _build_description(entry: dict[str, Any]) -> str:
    """Compose a human-readable description from CIViC axes.

    Format: "<evidence_type> — <evidence_direction> — <significance>". Empty
    components are omitted. Includes therapy_interaction_type when set
    (e.g. "Combination") because that materially changes how the option
    should be read by the render layer.
    """

    parts: list[str] = []
    for key in ("evidence_type", "evidence_direction", "significance"):
        val = entry.get(key)
        if val:
            parts.append(str(val).strip())
    base = " — ".join(parts) if parts else ""

    interaction = entry.get("therapy_interaction_type")
    if interaction:
        base = f"{base} ({interaction})" if base else f"({interaction})"

    return base


def _pick_source_url(query_gene: str, matched: list[dict[str, Any]]) -> str:
    """Pick the most useful source URL.

    Strategy: if any matched entry has a civic_url, use the highest-rated
    entry's URL (rating descending — CIViC ratings 1–5). Else fall back to
    the gene-level CIViC link.
    """

    if matched:
        # Sort by rating descending; ties broken by evidence_level (A best).
        def _rank_key(e: dict[str, Any]) -> tuple[int, int]:
            try:
                rating = -int(str(e.get("rating") or 0))
            except (TypeError, ValueError):
                rating = 0
            level = str(e.get("evidence_level") or "Z")
            level_rank = ord(level[0]) if level else ord("Z")
            return (rating, level_rank)

        best = sorted(matched, key=_rank_key)[0]
        url = best.get("civic_url")
        if url:
            return str(url)

    gene = (query_gene or "").strip()
    if gene:
        return f"https://civicdb.org/links/genes/{gene}"
    return "https://civicdb.org/"
