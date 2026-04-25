"""Clinician event CLI — record reviewer actions into the provenance log.

Wraps `event_store` so reviewers (or scripts integrating with their
workflow) can append events from the command line without writing
Python.

Usage:
    # Append an event
    python -m knowledge_base.engine.event_cli add PATIENT_ID \\
        --event-type confirmed \\
        --target-type regimen \\
        --target-id REG-VRD \\
        --summary "Confirmed VRd at MDT 2026-04-25" \\
        [--actor-role medical_oncologist] \\
        [--actor-id dr.example] \\
        [--evidence NCCN-MM-2024 ESMO-MM-2023] \\
        [--event-id ev-confirmed-vrd-1]   # auto-generated UUID4 if omitted

    # List events for a patient
    python -m knowledge_base.engine.event_cli list PATIENT_ID
    python -m knowledge_base.engine.event_cli list PATIENT_ID --json

The events.jsonl file lives at `patient_plans/<patient_id>/events.jsonl`
(gitignored per CHARTER §9.3). Override the root with --root.

This CLI does not validate that target_id corresponds to a real KB
entity — by design. Reviewers may need to record events about
provisional or local IDs that exist outside the canonical KB.
event_store enforces enum membership for event_type and target_type
(those are part of the audit contract).
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import uuid
from pathlib import Path

from .event_store import (
    DEFAULT_ROOT,
    append_event,
    read_events,
)
from .provenance import (
    EventType,
    TargetType,
    make_event,
)


if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


_VALID_EVENT_TYPES = sorted(EventType.__args__)  # type: ignore[attr-defined]
_VALID_TARGET_TYPES = sorted(TargetType.__args__)  # type: ignore[attr-defined]


def _cmd_add(args: argparse.Namespace) -> int:
    event_id = args.event_id or f"ev-{uuid.uuid4().hex[:12]}"
    try:
        event = make_event(
            event_id=event_id,
            actor_role=args.actor_role,
            event_type=args.event_type,
            target_type=args.target_type,
            target_id=args.target_id,
            summary=args.summary,
            actor_id=args.actor_id,
            evidence_refs=args.evidence,
        )
    except (TypeError, ValueError) as e:
        print(f"ERROR constructing event: {e}", file=sys.stderr)
        return 2

    try:
        path = append_event(
            args.patient_id,
            event,
            root=args.root,
            skip_if_exists=args.skip_if_exists,
        )
    except ValueError as e:
        print(f"ERROR appending event: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "event_id": event_id,
            "path": str(path),
            "event": event.to_dict(),
        }, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"Appended {event_id} → {path}")
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    events = read_events(args.patient_id, root=args.root)
    if args.json:
        print(json.dumps(
            [e.to_dict() for e in events],
            ensure_ascii=False,
            indent=2,
            default=str,
        ))
        return 0

    if not events:
        print(f"(no events for patient {args.patient_id} under {args.root})")
        return 0

    print(f"=== Events for {args.patient_id} ({len(events)}) ===")
    for e in events:
        actor = e.actor_role + (f"/{e.actor_id}" if e.actor_id else "")
        print(f"  [{e.timestamp}] {e.event_type:>16}  {e.target_type}:{e.target_id}")
        print(f"      actor:    {actor}")
        print(f"      summary:  {e.summary}")
        if e.evidence_refs:
            print(f"      evidence: {', '.join(e.evidence_refs)}")
        print(f"      event_id: {e.event_id}")
        print()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m knowledge_base.engine.event_cli",
        description="Record clinician/reviewer events into the provenance log.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"Storage root (default: {DEFAULT_ROOT}/)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ── add ──
    p_add = sub.add_parser("add", help="Append a new event for a patient")
    p_add.add_argument("patient_id", help="Patient identifier (path key)")
    p_add.add_argument(
        "--event-type",
        required=True,
        choices=_VALID_EVENT_TYPES,
        help="What the actor did",
    )
    p_add.add_argument(
        "--target-type",
        required=True,
        choices=_VALID_TARGET_TYPES,
        help="What the action targeted",
    )
    p_add.add_argument("--target-id", required=True, help="Target entity id (e.g. REG-VRD)")
    p_add.add_argument("--summary", required=True, help="Human-readable note")
    p_add.add_argument(
        "--actor-role",
        default="medical_oncologist",
        help="Canonical role id (default: medical_oncologist)",
    )
    p_add.add_argument(
        "--actor-id",
        default=None,
        help="Specific reviewer id (e.g. dr.example); omit for anonymous",
    )
    p_add.add_argument(
        "--evidence",
        nargs="*",
        default=[],
        metavar="SOURCE_ID",
        help="Source ids supporting this action (e.g. NCCN-MM-2024)",
    )
    p_add.add_argument(
        "--event-id",
        default=None,
        help="Custom event id; auto-generated UUID4 if omitted",
    )
    p_add.add_argument(
        "--skip-if-exists",
        action="store_true",
        help="No-op if an event with this --event-id is already in the log",
    )
    p_add.add_argument("--json", action="store_true", help="Print machine-readable result")
    p_add.set_defaults(func=_cmd_add)

    # ── list ──
    p_list = sub.add_parser("list", help="List events for a patient")
    p_list.add_argument("patient_id", help="Patient identifier")
    p_list.add_argument("--json", action="store_true", help="Emit JSON array of events")
    p_list.set_defaults(func=_cmd_list)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
