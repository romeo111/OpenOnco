"""Decision provenance — append-only event log + graph for Plan formation.

See specs/MDT_ORCHESTRATOR_SPEC.md §6. Database-ready shape; persistence
itself is deferred (events live in-memory + JSON-serializable). Future
storage may be SQLite event_log table, JSONL file, or object storage —
schema is the same.

This module **does not** make clinical decisions. It records what the
engine and clinicians did and when, so the audit trail can be
reconstructed later (CHARTER §10.2, §15.1 Criterion 4).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Optional


EventType = Literal[
    "confirmed",
    "modified",
    "rejected",
    "added_question",
    "approved",
    "requested_data",
    "flagged_risk",
    # Phase 2 of OncoKB integration — surface-only external KB consultation.
    # See oncokb_integration_safe_rollout_v3.md §7. Backward-compatible
    # extension; older events without these values still load.
    "external_kb_consulted",
    "resistance_conflict_detected",
]

TargetType = Literal[
    "diagnosis",
    "staging",
    "regimen",
    "contraindication",
    "red_flag",
    "source",
    "plan_section",
    "oncokb_query",
]


@dataclass
class ProvenanceEvent:
    event_id: str
    timestamp: str
    actor_role: str  # canonical role_id, or "engine" / "system"
    actor_id: Optional[str]  # specific reviewer; None for engine / anonymous
    event_type: EventType
    target_type: TargetType
    target_id: str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DecisionProvenanceGraph:
    """Lightweight graph + event log binding events to plan structure.

    `nodes` = canonical entities involved in this Plan (diagnosis,
    regimen, contraindications, …). `edges` = relationships
    (e.g. regimen → contraindication, kind=triggers). `events` = the
    append-only log of changes/decisions over time.
    """

    nodes: list[dict] = field(default_factory=list)
    edges: list[dict] = field(default_factory=list)
    events: list[ProvenanceEvent] = field(default_factory=list)
    plan_version: int = 1

    def add_node(self, node_id: str, node_type: str, label: str) -> None:
        self.nodes.append({"id": node_id, "type": node_type, "label": label})

    def add_edge(self, frm: str, to: str, kind: str) -> None:
        self.edges.append({"from": frm, "to": to, "kind": kind})

    def add_event(self, event: ProvenanceEvent) -> None:
        self.events.append(event)

    def to_dict(self) -> dict:
        return {
            "nodes": list(self.nodes),
            "edges": list(self.edges),
            "events": [e.to_dict() for e in self.events],
            "plan_version": self.plan_version,
        }


# ── Helpers for callers that just want to mint events quickly ──────────────


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_event(
    event_id: str,
    actor_role: str,
    event_type: EventType,
    target_type: TargetType,
    target_id: str,
    summary: str,
    actor_id: Optional[str] = None,
    evidence_refs: Optional[list[str]] = None,
    timestamp: Optional[str] = None,
) -> ProvenanceEvent:
    return ProvenanceEvent(
        event_id=event_id,
        timestamp=timestamp or now_iso(),
        actor_role=actor_role,
        actor_id=actor_id,
        event_type=event_type,
        target_type=target_type,
        target_id=target_id,
        summary=summary,
        evidence_refs=list(evidence_refs or []),
    )


__all__ = [
    "DecisionProvenanceGraph",
    "EventType",
    "ProvenanceEvent",
    "TargetType",
    "make_event",
    "now_iso",
]
