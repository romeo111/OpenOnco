"""Tests for ProvenanceEvent persistence (knowledge_base/engine/event_store.py).

Verifies:
1. append_event() creates the file + writes one JSON line per event
2. read_events() round-trips appended events in arrival order
3. malformed lines are skipped, valid lines still readable
4. validation rejects unknown event_type / target_type
5. skip_if_exists prevents duplicate event_ids
6. merge_events_into_graph() loads persisted events into a fresh graph
   without dupes
7. patient_id required
8. append_events() bulk variant

All tests use tmp_path so nothing writes to the real patient_plans/ tree.
"""

from __future__ import annotations

import json

import pytest

from knowledge_base.engine.event_store import (
    EVENTS_FILENAME,
    append_event,
    append_events,
    events_path,
    merge_events_into_graph,
    read_events,
)
from knowledge_base.engine.provenance import (
    DecisionProvenanceGraph,
    make_event,
)


def _ev(eid: str, etype: str = "confirmed", target: str = "REG-VRD") -> object:
    return make_event(
        event_id=eid,
        actor_role="medical_oncologist",
        event_type=etype,  # type: ignore[arg-type]
        target_type="regimen",
        target_id=target,
        summary=f"event {eid}",
        actor_id="dr.example",
        evidence_refs=["NCCN-MM-2024"],
    )


# ── Append + read round-trip ───────────────────────────────────────────────


def test_append_event_creates_file(tmp_path):
    pid = "patient-abc"
    path = append_event(pid, _ev("ev-1"), root=tmp_path)
    assert path == tmp_path / pid / EVENTS_FILENAME
    assert path.is_file()


def test_round_trip_single_event(tmp_path):
    pid = "patient-abc"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    events = read_events(pid, root=tmp_path)
    assert len(events) == 1
    e = events[0]
    assert e.event_id == "ev-1"
    assert e.actor_role == "medical_oncologist"
    assert e.actor_id == "dr.example"
    assert e.evidence_refs == ["NCCN-MM-2024"]


def test_arrival_order_preserved(tmp_path):
    pid = "patient-order"
    for i in range(5):
        append_event(pid, _ev(f"ev-{i}"), root=tmp_path)
    ids = [e.event_id for e in read_events(pid, root=tmp_path)]
    assert ids == ["ev-0", "ev-1", "ev-2", "ev-3", "ev-4"]


def test_read_events_empty_when_no_file(tmp_path):
    assert read_events("nobody", root=tmp_path) == []


# ── Malformed line tolerance ──────────────────────────────────────────────


def test_malformed_lines_skipped(tmp_path):
    pid = "patient-junk"
    append_event(pid, _ev("ev-good-1"), root=tmp_path)
    log = tmp_path / pid / EVENTS_FILENAME
    with open(log, "a", encoding="utf-8") as f:
        f.write("this is not json\n")
        f.write('{"missing": "required fields"}\n')
        f.write("\n")  # blank
    append_event(pid, _ev("ev-good-2"), root=tmp_path)
    events = read_events(pid, root=tmp_path)
    assert [e.event_id for e in events] == ["ev-good-1", "ev-good-2"]


# ── Validation ────────────────────────────────────────────────────────────


def test_rejects_unknown_event_type(tmp_path):
    bad = make_event(
        event_id="ev-bad",
        actor_role="medical_oncologist",
        event_type="exploded",  # type: ignore[arg-type]
        target_type="regimen",
        target_id="REG-X",
        summary="nope",
    )
    with pytest.raises(ValueError, match="event_type"):
        append_event("patient-x", bad, root=tmp_path)


def test_rejects_unknown_target_type(tmp_path):
    bad = make_event(
        event_id="ev-bad",
        actor_role="medical_oncologist",
        event_type="confirmed",
        target_type="banana",  # type: ignore[arg-type]
        target_id="X",
        summary="nope",
    )
    with pytest.raises(ValueError, match="target_type"):
        append_event("patient-x", bad, root=tmp_path)


def test_requires_patient_id(tmp_path):
    with pytest.raises(ValueError, match="patient_id"):
        append_event("", _ev("ev-1"), root=tmp_path)


# ── Idempotency ───────────────────────────────────────────────────────────


def test_skip_if_exists_avoids_duplicate(tmp_path):
    pid = "patient-dup"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    append_event(pid, _ev("ev-1"), root=tmp_path, skip_if_exists=True)
    append_event(pid, _ev("ev-1"), root=tmp_path, skip_if_exists=True)
    events = read_events(pid, root=tmp_path)
    assert len(events) == 1


def test_skip_if_exists_default_false_allows_duplicates(tmp_path):
    pid = "patient-noskip"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    append_event(pid, _ev("ev-1"), root=tmp_path)  # no flag → both written
    assert len(read_events(pid, root=tmp_path)) == 2


# ── Graph merge ───────────────────────────────────────────────────────────


def test_merge_into_empty_graph_adds_all(tmp_path):
    pid = "patient-merge"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    append_event(pid, _ev("ev-2", etype="approved"), root=tmp_path)

    graph = DecisionProvenanceGraph()
    merge_events_into_graph(graph, pid, root=tmp_path)

    assert [e.event_id for e in graph.events] == ["ev-1", "ev-2"]


def test_merge_dedupes_by_event_id(tmp_path):
    pid = "patient-merge-dedup"
    # Pre-seed in-memory graph with one of the events
    graph = DecisionProvenanceGraph()
    graph.add_event(_ev("ev-1"))

    # Persist the same event id + a new one
    append_event(pid, _ev("ev-1"), root=tmp_path)
    append_event(pid, _ev("ev-2", etype="modified"), root=tmp_path)

    merge_events_into_graph(graph, pid, root=tmp_path)
    ids = [e.event_id for e in graph.events]
    assert ids == ["ev-1", "ev-2"]
    assert len(ids) == 2


def test_merge_when_log_missing_is_noop(tmp_path):
    graph = DecisionProvenanceGraph()
    graph.add_event(_ev("ev-1"))
    merge_events_into_graph(graph, "no-such-patient", root=tmp_path)
    assert [e.event_id for e in graph.events] == ["ev-1"]


# ── Bulk + helper ─────────────────────────────────────────────────────────


def test_append_events_bulk(tmp_path):
    pid = "patient-bulk"
    append_events(pid, [_ev("ev-1"), _ev("ev-2"), _ev("ev-3")], root=tmp_path)
    assert [e.event_id for e in read_events(pid, root=tmp_path)] == [
        "ev-1", "ev-2", "ev-3"
    ]


def test_events_path_returns_none_when_missing(tmp_path):
    assert events_path("nobody", root=tmp_path) is None


def test_events_path_returns_path_when_present(tmp_path):
    pid = "patient-here"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    p = events_path(pid, root=tmp_path)
    assert p is not None and p.is_file()


# ── Storage format sanity ─────────────────────────────────────────────────


def test_jsonl_one_event_per_line(tmp_path):
    pid = "patient-jsonl"
    append_event(pid, _ev("ev-1"), root=tmp_path)
    append_event(pid, _ev("ev-2"), root=tmp_path)
    raw = (tmp_path / pid / EVENTS_FILENAME).read_text(encoding="utf-8")
    lines = [ln for ln in raw.split("\n") if ln.strip()]
    assert len(lines) == 2
    for ln in lines:
        json.loads(ln)  # each line must be parseable JSON
