#!/usr/bin/env python3
"""Per-entity-type freshness audit — flags stale `last_reviewed`.

Walks every YAML under `knowledge_base/hosted/content/{biomarkers,
indications,algorithms,drugs,regimens,redflags,sources,...}/` and
classifies each entity into one of:

  - ✓ fresh:        within SLA
  - ⚠ stale:        past SLA (clinical re-review needed)
  - ❌ never:       `last_reviewed` is null / missing (never reviewed)

SLAs (per-entity-type, in months — see CHARTER §6.1 for review cadence):

  Drug, Regimen, Biomarker, RedFlag    : 12 months
  Indication, Algorithm                 : 6 months   (guideline tempo)
  Source                                : 18 months  (publishers slower)
  All other types                       : 12 months  (default)

JSON schema emitted:

    {
      "today": "2026-04-26",
      "by_entity_type": {
        "Drug": {
          "sla_months": 12,
          "total": 50,
          "fresh": 35,
          "stale_past_sla": 5,
          "never_reviewed": 10,
          "stale_ids": ["DRUG-X", ...],
          "never_reviewed_ids": ["DRUG-Y", ...]
        },
        ...
      },
      "total_breaches": int     # stale + never_reviewed across all types
    }

Exit codes:
  0 — all entities fresh
  1 — at least one breach (stale or never)

Usage:
  python scripts/audit_freshness.py
  python scripts/audit_freshness.py --human
  python scripts/audit_freshness.py --output freshness.json
  python scripts/audit_freshness.py --today 2026-06-01   # for testing
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


# Per-entity-type SLA in months. Keep in sync with
# docs/plans/scheduled_kb_audit_2026-04-26.md §2.3.
SLA_MONTHS: dict[str, int] = {
    "biomarkers": 12,
    "drugs": 12,
    "regimens": 12,
    "redflags": 12,
    "indications": 6,
    "algorithms": 6,
    "sources": 18,
}
DEFAULT_SLA_MONTHS = 12

# Friendly entity-type label (matches Pydantic class names where they
# differ from the directory name).
TYPE_LABEL: dict[str, str] = {
    "biomarkers": "Biomarker",
    "drugs": "Drug",
    "regimens": "Regimen",
    "redflags": "RedFlag",
    "indications": "Indication",
    "algorithms": "Algorithm",
    "sources": "Source",
    "tests": "Test",
    "diseases": "Disease",
    "contraindications": "Contraindication",
    "monitoring": "MonitoringSchedule",
    "supportive_care": "SupportiveCare",
    "questionnaires": "Questionnaire",
    "workups": "DiagnosticWorkup",
    "access_pathways": "AccessPathway",
}


def _force_utf8_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


def _months_between(start: date, end: date) -> int:
    """Whole-month delta. Avoids 30/31 ambiguity by counting calendar
    months, not days. Negative if `start > end` (shouldn't happen)."""
    return (end.year - start.year) * 12 + (end.month - start.month)


def _parse_iso_date(raw: Any) -> Optional[date]:
    """Parse `last_reviewed`. Accepts:
    - ISO date string "YYYY-MM-DD"
    - PyYAML auto-parsed datetime.date
    - PyYAML auto-parsed datetime.datetime
    Returns None when null / missing / unparseable."""

    if raw is None:
        return None
    if isinstance(raw, date) and not isinstance(raw, datetime):
        return raw
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, str):
        try:
            return datetime.fromisoformat(raw[:10]).date()
        except ValueError:
            return None
    return None


def collect_freshness_state(
    kb_root: Path = KB_ROOT,
    today: Optional[date] = None,
) -> dict[str, Any]:
    """Walk KB, classify each entity by freshness vs SLA. Deterministic
    given (kb_root, today)."""

    if today is None:
        today = date.today()

    by_type: dict[str, dict[str, Any]] = {}

    if not kb_root.is_dir():
        return {
            "today": today.isoformat(),
            "by_entity_type": {},
            "total_breaches": 0,
            "error": f"kb_root not a directory: {kb_root}",
        }

    for type_dir in sorted(kb_root.iterdir()):
        if not type_dir.is_dir():
            continue
        type_key = type_dir.name
        sla_months = SLA_MONTHS.get(type_key, DEFAULT_SLA_MONTHS)
        label = TYPE_LABEL.get(type_key, type_key.rstrip("s").capitalize())

        fresh: list[str] = []
        stale: list[str] = []
        never: list[str] = []

        for path in sorted(type_dir.rglob("*.yaml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError:
                # Validator catches schema/parse errors — skip here.
                continue
            if not isinstance(data, dict):
                continue
            entity_id = data.get("id") or path.stem.upper()
            reviewed = _parse_iso_date(data.get("last_reviewed"))
            if reviewed is None:
                never.append(entity_id)
                continue
            age = _months_between(reviewed, today)
            if age <= sla_months:
                fresh.append(entity_id)
            else:
                stale.append(entity_id)

        # Sort for determinism
        fresh.sort()
        stale.sort()
        never.sort()

        total = len(fresh) + len(stale) + len(never)
        if total == 0:
            continue  # empty directory — skip silently

        by_type[label] = {
            "sla_months": sla_months,
            "total": total,
            "fresh": len(fresh),
            "stale_past_sla": len(stale),
            "never_reviewed": len(never),
            "stale_ids": stale,
            "never_reviewed_ids": never,
        }

    total_breaches = sum(
        v["stale_past_sla"] + v["never_reviewed"] for v in by_type.values()
    )
    return {
        "today": today.isoformat(),
        "by_entity_type": by_type,
        "total_breaches": total_breaches,
    }


def render_human(state: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"KB freshness snapshot — as of {state['today']}")
    lines.append("")
    if state.get("error"):
        lines.append(f"❌ {state['error']}")
        return "\n".join(lines) + "\n"
    if not state["by_entity_type"]:
        lines.append("(no entities found)")
        return "\n".join(lines) + "\n"

    lines.append(
        f"{'Type':22s} {'SLA':>5s} {'Total':>7s} {'Fresh':>7s} "
        f"{'Stale':>7s} {'Never':>7s}"
    )
    lines.append("-" * 70)
    for label, data in sorted(state["by_entity_type"].items()):
        lines.append(
            f"{label:22s} {data['sla_months']:>3d}mo {data['total']:>7d} "
            f"{data['fresh']:>7d} {data['stale_past_sla']:>7d} "
            f"{data['never_reviewed']:>7d}"
        )
    lines.append("")
    lines.append(f"Total breaches: {state['total_breaches']}")

    # Top 10 stale + never per type — actionable preview
    showed_any = False
    for label, data in sorted(state["by_entity_type"].items()):
        breaches = data["stale_ids"] + data["never_reviewed_ids"]
        if not breaches:
            continue
        if not showed_any:
            lines.append("")
            lines.append("First 10 breaches per type:")
            showed_any = True
        sample = breaches[:10]
        more = len(breaches) - len(sample)
        suffix = f" (+{more} more)" if more > 0 else ""
        lines.append(f"  {label}: {', '.join(sample)}{suffix}")
    return "\n".join(lines) + "\n"


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
    parser.add_argument(
        "--today", type=str, default=None,
        help="Override 'today' (ISO date); useful for tests / replay.",
    )
    args = parser.parse_args()

    today_override: Optional[date] = None
    if args.today:
        try:
            today_override = datetime.fromisoformat(args.today).date()
        except ValueError:
            print(f"Invalid --today: {args.today}", file=sys.stderr)
            return 2

    state = collect_freshness_state(args.kb_root, today_override)

    if args.human:
        out = render_human(state)
    else:
        out = json.dumps(state, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)

    if state.get("error"):
        return 2
    return 1 if state["total_breaches"] else 0


if __name__ == "__main__":
    sys.exit(main())
