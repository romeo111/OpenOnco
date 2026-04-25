"""Append-only event log for ProvenanceEvent records.

Per CHARTER §10.2 / §15.1 Criterion 4 the audit trail of who-did-what-when
must be reconstructable. `DecisionProvenanceGraph` (provenance.py) holds
events in memory; this module persists them to disk so they survive past
a single engine invocation and can be merged into freshly-built graphs
when a Plan is re-rendered.

Storage layout (gitignored per CHARTER §9.3):

    patient_plans/<patient_id>/events.jsonl

One ProvenanceEvent per line, JSON-encoded. Append-only — never rewritten,
never deleted. Order in the file = chronological order of arrival.

The schema is database-ready (ProvenanceEvent fields map cleanly to a
SQLite event_log table); JSONL is the MVP storage. Migrating later does
not require schema work, only a loader swap.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .provenance import (
    DecisionProvenanceGraph,
    EventType,
    ProvenanceEvent,
    TargetType,
)


# Default root matches persistence.py — same gitignored tree.
DEFAULT_ROOT = Path("patient_plans")
EVENTS_FILENAME = "events.jsonl"


# Allowed value sets — derived from provenance.py Literal types so the
# guard here stays in sync if those types are extended. We resolve them
# at import time once.
_VALID_EVENT_TYPES = set(EventType.__args__)  # type: ignore[attr-defined]
_VALID_TARGET_TYPES = set(TargetType.__args__)  # type: ignore[attr-defined]


# ── Internal helpers ──────────────────────────────────────────────────────


def _events_path(patient_id: str, root: Path) -> Path:
    return root / patient_id / EVENTS_FILENAME


def _validate_event(event: ProvenanceEvent) -> None:
    if not event.event_id:
        raise ValueError("ProvenanceEvent.event_id is required.")
    if not event.timestamp:
        raise ValueError("ProvenanceEvent.timestamp is required.")
    if event.event_type not in _VALID_EVENT_TYPES:
        raise ValueError(
            f"Unknown event_type {event.event_type!r}; "
            f"allowed: {sorted(_VALID_EVENT_TYPES)}"
        )
    if event.target_type not in _VALID_TARGET_TYPES:
        raise ValueError(
            f"Unknown target_type {event.target_type!r}; "
            f"allowed: {sorted(_VALID_TARGET_TYPES)}"
        )


def _event_from_dict(d: dict) -> ProvenanceEvent:
    """Rehydrate a ProvenanceEvent from a JSONL line. Tolerant of unknown
    keys (forward-compat) but strict on the type-checked fields."""

    return ProvenanceEvent(
        event_id=d["event_id"],
        timestamp=d["timestamp"],
        actor_role=d.get("actor_role", "unknown"),
        actor_id=d.get("actor_id"),
        event_type=d["event_type"],
        target_type=d["target_type"],
        target_id=d["target_id"],
        summary=d.get("summary", ""),
        evidence_refs=list(d.get("evidence_refs") or []),
    )


# ── Public API ────────────────────────────────────────────────────────────


def append_event(
    patient_id: str,
    event: ProvenanceEvent,
    root: Path = DEFAULT_ROOT,
    skip_if_exists: bool = False,
) -> Path:
    """Append a single event to the patient's events.jsonl. Returns the
    file path. Creates parent dirs if missing.

    Args:
        patient_id: required (path key).
        event: a fully-constructed ProvenanceEvent.
        root: storage root (defaults to gitignored `patient_plans/`).
        skip_if_exists: if True, scan existing log first; do nothing if an
            event with the same `event_id` is already present. Off by
            default — caller is normally responsible for unique ids.

    Raises:
        ValueError: missing patient_id, malformed event_type/target_type.
    """

    if not patient_id:
        raise ValueError("patient_id is required for event_store.append_event.")
    _validate_event(event)

    path = _events_path(patient_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)

    if skip_if_exists and path.is_file():
        for existing in read_events(patient_id, root=root):
            if existing.event_id == event.event_id:
                return path

    line = json.dumps(event.to_dict(), ensure_ascii=False, default=str)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return path


def read_events(
    patient_id: str,
    root: Path = DEFAULT_ROOT,
) -> list[ProvenanceEvent]:
    """Return events for a patient in arrival order. Empty list if the
    log file does not exist. Malformed lines are skipped silently — the
    log is meant to be append-tolerant; partial reads beat loud crashes
    when one entry is hand-edited."""

    path = _events_path(patient_id, root)
    if not path.is_file():
        return []
    out: list[ProvenanceEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            out.append(_event_from_dict(d))
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    return out


def merge_events_into_graph(
    graph: DecisionProvenanceGraph,
    patient_id: str,
    root: Path = DEFAULT_ROOT,
) -> DecisionProvenanceGraph:
    """Load persisted events for a patient and append them to an
    in-memory graph, deduping by event_id. Returns the same graph
    instance for chaining.

    Use case: when re-rendering a Plan in a new session, the engine
    rebuilds the graph fresh — but historical reviewer events would be
    lost without this merge. Call after `_bootstrap_provenance()`.
    """

    seen = {e.event_id for e in graph.events}
    for ev in read_events(patient_id, root=root):
        if ev.event_id in seen:
            continue
        graph.add_event(ev)
        seen.add(ev.event_id)
    return graph


def append_events(
    patient_id: str,
    events: Iterable[ProvenanceEvent],
    root: Path = DEFAULT_ROOT,
) -> Path:
    """Bulk-append helper. Same path is returned regardless of count."""

    path = _events_path(patient_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for event in events:
            _validate_event(event)
            line = json.dumps(event.to_dict(), ensure_ascii=False, default=str)
            f.write(line + "\n")
    return path


def events_path(patient_id: str, root: Path = DEFAULT_ROOT) -> Optional[Path]:
    """Return the events.jsonl path if it exists for this patient, else None."""
    path = _events_path(patient_id, root)
    return path if path.is_file() else None


__all__ = [
    "DEFAULT_ROOT",
    "EVENTS_FILENAME",
    "append_event",
    "append_events",
    "events_path",
    "merge_events_into_graph",
    "read_events",
]
