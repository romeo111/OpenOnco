#!/usr/bin/env python3
"""Audit UA-translation coverage across the KB.

For every YAML under ``knowledge_base/hosted/content/``, count the EN
text fields that have a UA companion, what state the UA companion is in,
and how recently the EN source was modified (file-level mtime via git
log, used to defer recently-churning entities from translation waves).

Output
------
1. CSV at ``docs/reviews/ua-coverage-<DATE>.csv`` — one row per
   (file, en_field, ua_field).
2. Terminal summary by entity type with counts:
   missing | drafted_pending | drafted_v2plus | human_reviewed | total

Run
---
    python scripts/audit_ua_coverage.py
    python scripts/audit_ua_coverage.py --out docs/reviews/ua-coverage-2026-05-12.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
KB = REPO / "knowledge_base" / "hosted" / "content"

# (entity_dir, [(en_field, ua_field), ...]) — fields the auditor checks.
# Mirrors scripts/draft_ua_fields.py ENTITY_PLAN, extended with
# ``description`` and ``epidemiology.context`` where present.
ENTITY_PLAN: dict[str, list[tuple[str, str]]] = {
    "biomarkers": [("notes", "notes_ua"), ("description", "description_ua")],
    "biomarker_actionability": [
        ("evidence_summary", "evidence_summary_ua"),
        ("notes", "notes_ua"),
    ],
    "diseases": [("notes", "notes_ua")],
    "regimens": [("notes", "notes_ua")],
    "redflags": [("notes", "notes_ua"), ("description", "description_ua")],
    "indications": [("rationale", "rationale_ua")],
    "drugs": [("notes", "notes_ua")],
    "algorithms": [("notes", "notes_ua")],
    "procedures": [("notes", "notes_ua")],
    "radiation_courses": [("notes", "notes_ua")],
}

DATE = dt.date.today().isoformat()


def git_mtime_days(path: Path) -> int:
    """Days since last commit touching ``path``. Returns -1 on failure."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if not out:
            return -1
        last_commit = dt.datetime.fromtimestamp(int(out), tz=dt.timezone.utc)
        delta = dt.datetime.now(dt.timezone.utc) - last_commit
        return delta.days
    except Exception:
        return -1


def classify(ua_value, status, drafted_by, draft_revision) -> str:
    """Bucket a UA companion field into a coverage state."""
    if ua_value is None or (isinstance(ua_value, str) and not ua_value.strip()):
        return "missing"
    if status in ("human_reviewed", "clinically_signed_off"):
        return "human_reviewed"
    if isinstance(draft_revision, int) and draft_revision >= 2:
        return "drafted_v2plus"
    if drafted_by == "claude_extraction" or status == "pending_clinical_signoff":
        return "drafted_pending"
    return "drafted_pending"


def audit_file(path: Path, plan: list[tuple[str, str]]) -> list[dict]:
    """Return one row per (en_field, ua_field) tracked in this entity type."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [
            {
                "file": str(path.relative_to(REPO)).replace("\\", "/"),
                "entity_type": path.parent.name,
                "en_field": "_PARSE_ERROR_",
                "ua_field": "_PARSE_ERROR_",
                "state": "parse_error",
                "ua_status": "",
                "ua_drafted_by": "",
                "draft_revision": "",
                "en_chars": 0,
                "ua_chars": 0,
                "mtime_days": git_mtime_days(path),
                "note": str(exc)[:120],
            }
        ]
    if not isinstance(data, dict):
        return []
    rows = []
    status = data.get("ukrainian_review_status", "")
    drafted_by = data.get("ukrainian_drafted_by", "")
    revision = data.get("draft_revision", 1) if status else None
    mtime = git_mtime_days(path)
    for en_field, ua_field in plan:
        en_val = data.get(en_field)
        ua_val = data.get(ua_field)
        en_present = bool(en_val) and bool(str(en_val).strip())
        if not en_present:
            continue  # nothing to translate; skip row entirely
        rows.append(
            {
                "file": str(path.relative_to(REPO)).replace("\\", "/"),
                "entity_type": path.parent.name,
                "en_field": en_field,
                "ua_field": ua_field,
                "state": classify(ua_val, status, drafted_by, revision),
                "ua_status": status,
                "ua_drafted_by": drafted_by,
                "draft_revision": revision if revision else "",
                "en_chars": len(str(en_val)),
                "ua_chars": len(str(ua_val)) if ua_val else 0,
                "mtime_days": mtime,
                "note": "",
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=REPO / "docs" / "reviews" / f"ua-coverage-{DATE}.csv",
    )
    ap.add_argument(
        "--defer-recent-days",
        type=int,
        default=14,
        help="Files modified within this many days are flagged 'defer'.",
    )
    args = ap.parse_args()

    rows: list[dict] = []
    for entity_dir, plan in ENTITY_PLAN.items():
        d = KB / entity_dir
        if not d.exists():
            continue
        for path in sorted(d.glob("*.yaml")):
            rows.extend(audit_file(path, plan))

    # Tag deferred (recently-churning EN source).
    for r in rows:
        if 0 <= r["mtime_days"] < args.defer_recent_days:
            r["defer"] = "yes"
        else:
            r["defer"] = ""

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "file",
        "entity_type",
        "en_field",
        "ua_field",
        "state",
        "ua_status",
        "ua_drafted_by",
        "draft_revision",
        "en_chars",
        "ua_chars",
        "mtime_days",
        "defer",
        "note",
    ]
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Summary table.
    states = ["missing", "drafted_pending", "drafted_v2plus", "human_reviewed", "parse_error"]
    by_type: dict[str, dict[str, int]] = {}
    deferred_by_type: dict[str, int] = {}
    for r in rows:
        et = r["entity_type"]
        by_type.setdefault(et, {s: 0 for s in states})
        by_type[et][r["state"]] = by_type[et].get(r["state"], 0) + 1
        if r["defer"] == "yes":
            deferred_by_type[et] = deferred_by_type.get(et, 0) + 1

    print(f"\nUA coverage audit — {DATE}")
    print(f"CSV: {args.out.relative_to(REPO)}")
    print(f"Defer threshold: <{args.defer_recent_days} days since last commit\n")
    header = f"{'entity_type':<28}" + "".join(f"{s:>18}" for s in states) + f"{'defer':>10}{'TOTAL':>10}"
    print(header)
    print("-" * len(header))
    totals = {s: 0 for s in states}
    total_def = 0
    for et in sorted(by_type):
        counts = by_type[et]
        defc = deferred_by_type.get(et, 0)
        total = sum(counts.values())
        line = f"{et:<28}" + "".join(f"{counts[s]:>18}" for s in states) + f"{defc:>10}{total:>10}"
        print(line)
        for s in states:
            totals[s] += counts[s]
        total_def += defc
    grand_total = sum(totals.values())
    line = f"{'TOTAL':<28}" + "".join(f"{totals[s]:>18}" for s in states) + f"{total_def:>10}{grand_total:>10}"
    print("-" * len(header))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
