"""Actionability lookup client — Protocol + sync implementations.

Source-agnostic. Phase 1 of the CIViC pivot: original OncoKB-only HTTP
client (HttpxOncoKBClient + services/oncokb_proxy) was deleted because
the OncoKB ToS forbids redistribution + use in patient-services contexts
(see docs/reviews/oncokb-public-civic-coverage-2026-04-27.md). Phase 2
will add a `SnapshotActionabilityClient` reading from a local CIViC YAML
snapshot.

Engine is sync (`generate_plan()` is a plain function), so this client
is sync too.

Per safe-rollout v3 §0 invariant 3 (fail-open): every method swallows
errors and returns ActionabilityError instead of raising. Engine never
crashes because of an actionability lookup failure.

Per safe-rollout v3 §6 + §10: this module is the architectural firewall.
It MUST NOT be imported by:
  - knowledge_base/engine/algorithm_eval.py
  - knowledge_base/engine/redflag_eval.py
  - knowledge_base/engine/_actionability.py
  - any code path inside `generate_plan` BEFORE `tracks` is finalized

The import-graph invariant test in tests/test_actionability_invariants.py
locks this contract.
"""

from __future__ import annotations

from typing import Protocol

from .actionability_types import (
    ActionabilityError,
    ActionabilityQuery,
    ActionabilityResult,
    ActionabilityTherapeuticOption,
)


class ActionabilityClient(Protocol):
    """Sync client interface. Implementations must satisfy fail-open
    contract: per-query errors return ActionabilityError, never raise."""

    def lookup(self, query: ActionabilityQuery) -> ActionabilityResult | ActionabilityError: ...

    def batch_lookup(
        self, queries: list[ActionabilityQuery]
    ) -> list[ActionabilityResult | ActionabilityError]: ...


# ── Null client (default — when engine is invoked without an actionability source) ──


class NullActionabilityClient:
    """Returns disabled-error for every query. Used as default when
    actionability integration is off or no client is wired."""

    def lookup(self, query: ActionabilityQuery) -> ActionabilityError:
        return ActionabilityError(
            query=query,
            error_kind="disabled",
            detail="Actionability lookup integration disabled",
        )

    def batch_lookup(self, queries: list[ActionabilityQuery]) -> list[ActionabilityError]:
        return [self.lookup(q) for q in queries]


# ── Stub client (tests — fixture-driven, no I/O) ─────────────────────────


class StubActionabilityClient:
    """Test client with a pre-baked response map keyed by (gene, variant).
    Anything not in the map returns an empty (negative) result.

    Usage:
        stub = StubActionabilityClient({
            ("BRAF", "V600E"): [
                {"level": "1", "drugs": ["vemurafenib"], "description": "...", "pmids": []},
            ],
            ("EGFR", "T790M"): [
                {"level": "R1", "drugs": ["gefitinib"], "description": "resistance", "pmids": ["123"]},
            ],
        })
    """

    def __init__(
        self,
        responses: dict[tuple[str, str], list[dict]],
        data_version: str | None = "stub-v1.0",
    ) -> None:
        self._responses = {(k[0].upper(), k[1]): v for k, v in responses.items()}
        self._data_version = data_version

    def lookup(self, query: ActionabilityQuery) -> ActionabilityResult:
        key = (query.gene.upper(), query.variant)
        raw_options = self._responses.get(key, [])
        options = tuple(
            ActionabilityTherapeuticOption(
                level=str(o.get("level", "?")),
                drugs=tuple(o.get("drugs", [])),
                description=o.get("description"),
                pmids=tuple(str(p) for p in o.get("pmids", [])),
                fda_approved=bool(o.get("fda_approved", False)),
                fda_approval_year=o.get("fda_approval_year"),
            )
            for o in raw_options
        )
        return ActionabilityResult(
            query=query,
            source_url=f"https://stub.local/gene/{query.gene}/{query.variant}",
            therapeutic_options=options,
            cached=False,
            data_version=self._data_version,
        )

    def batch_lookup(self, queries: list[ActionabilityQuery]) -> list[ActionabilityResult]:
        return [self.lookup(q) for q in queries]


# ── Snapshot client ──────────────────────────────────────────────────────
#
# The canonical CIViC snapshot reader lives in
# ``knowledge_base/engine/snapshot_civic_client.py`` (class
# ``SnapshotCIViCClient``). Import it directly:
#
#     from knowledge_base.engine.snapshot_civic_client import SnapshotCIViCClient
#     client = SnapshotCIViCClient("knowledge_base/hosted/civic/2026-04-25/evidence.yaml")
#
# This module intentionally has NO httpx dependency — CIViC distribution
# is the local snapshot under ``knowledge_base/hosted/civic/``, not a
# live API.


__all__ = [
    "ActionabilityClient",
    "NullActionabilityClient",
    "StubActionabilityClient",
]
