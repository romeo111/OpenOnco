#!/usr/bin/env python3
"""JSON wrapper around `knowledge_base.validation.loader.load_content`.

Emits a structured snapshot of the KB integrity state to stdout (or
`--output FILE`). Used by the scheduled-audit orchestrator
(`scripts/run_scheduled_audit.py`) — `load_content` already collects
schema + ref errors imperatively, but the orchestrator needs JSON it
can diff against the previous archived state.

Schema of the emitted JSON:

    {
      "loaded_entities": int,                  # total IDs in entities_by_id
      "schema_errors_count": int,
      "ref_errors_count": int,
      "errors": [
        {"file": "x.yaml", "type": "schema", "message": "..."},
        {"file": "y.yaml", "type": "ref",    "message": "..."},
        ...
      ],
      "summary_by_file": {                    # convenience for reporting
        "x.yaml": {"schema": 1, "ref": 0},
      }
    }

Exit codes:
  0 — KB loaded cleanly (no errors)
  1 — schema or ref errors present
  2 — catastrophic failure (loader crashed; KB structurally broken)

Usage:
  python scripts/audit_validator.py                          # JSON to stdout
  python scripts/audit_validator.py --output validator.json  # write to file
  python scripts/audit_validator.py --human                  # readable summary
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def collect_validator_state(kb_root: Path = KB_ROOT) -> dict[str, Any]:
    """Run the loader, capture errors, normalize to JSON-friendly dict.

    Returned dict is stable across runs at the same git SHA — same
    inputs produce same outputs (modulo dict-iteration order, which
    we sort to make the output diffable)."""

    # Late import — keeps `python scripts/audit_validator.py --help`
    # responsive without paying the schema-import cost.
    from knowledge_base.validation.loader import load_content

    try:
        result = load_content(kb_root)
    except Exception as exc:  # pylint: disable=broad-except
        # Catastrophic: e.g. Pydantic upgrade incompatibility.
        return {
            "loaded_entities": 0,
            "schema_errors_count": 0,
            "ref_errors_count": 0,
            "catastrophic_error": f"{type(exc).__name__}: {exc}",
            "errors": [],
            "summary_by_file": {},
        }

    errors: list[dict[str, str]] = []
    summary_by_file: dict[str, dict[str, int]] = defaultdict(
        lambda: {"schema": 0, "ref": 0}
    )

    for path, message in result.schema_errors:
        fname = path.name
        errors.append({
            "file": fname,
            "type": "schema",
            "message": str(message),
        })
        summary_by_file[fname]["schema"] += 1

    for path, message in result.ref_errors:
        fname = path.name
        errors.append({
            "file": fname,
            "type": "ref",
            "message": str(message),
        })
        summary_by_file[fname]["ref"] += 1

    # Sort for determinism (file path → type → first-N-chars of msg).
    errors.sort(key=lambda e: (e["file"], e["type"], e["message"][:80]))

    return {
        "loaded_entities": len(result.entities_by_id),
        "schema_errors_count": len(result.schema_errors),
        "ref_errors_count": len(result.ref_errors),
        "errors": errors,
        "summary_by_file": dict(summary_by_file),
    }


def render_human(state: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"KB validator snapshot — {state['loaded_entities']} entities loaded")
    lines.append("")

    if state.get("catastrophic_error"):
        lines.append(f"❌ CATASTROPHIC: {state['catastrophic_error']}")
        return "\n".join(lines) + "\n"

    schema_n = state["schema_errors_count"]
    ref_n = state["ref_errors_count"]
    if schema_n == 0 and ref_n == 0:
        lines.append("✓ Clean — 0 schema errors, 0 ref errors.")
        return "\n".join(lines) + "\n"

    lines.append(f"Schema errors: {schema_n}")
    lines.append(f"Ref errors:    {ref_n}")
    lines.append("")
    lines.append("By file:")
    for fname, counts in sorted(state["summary_by_file"].items()):
        lines.append(
            f"  {fname:50s}  schema={counts['schema']:>2}  ref={counts['ref']:>2}"
        )
    if state["errors"]:
        lines.append("")
        lines.append("First 10 errors:")
        for err in state["errors"][:10]:
            lines.append(f"  [{err['type']}] {err['file']}: {err['message'][:120]}")
        if len(state["errors"]) > 10:
            lines.append(f"  ... and {len(state['errors']) - 10} more")
    return "\n".join(lines) + "\n"


def _force_utf8_stdout() -> None:
    """Make stdout/stderr UTF-8 — Windows console defaults to cp1252 which
    can't encode ✓ ❌ ⚠. Safe no-op on POSIX (already UTF-8)."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


def main() -> int:
    _force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--output", type=Path, default=None,
        help="Write JSON to this file instead of stdout.",
    )
    parser.add_argument(
        "--human", action="store_true",
        help="Emit a readable text summary instead of JSON.",
    )
    parser.add_argument(
        "--kb-root", type=Path, default=KB_ROOT,
        help=f"Path to KB content root (default: {KB_ROOT}).",
    )
    args = parser.parse_args()

    state = collect_validator_state(args.kb_root)

    if args.human:
        out = render_human(state)
    else:
        out = json.dumps(state, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)

    if state.get("catastrophic_error"):
        return 2
    if state["schema_errors_count"] or state["ref_errors_count"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
