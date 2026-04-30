#!/usr/bin/env python3
"""Standalone audit: lists every unresolved SRC-* citation in the live KB,
grouped by category (typo / banned / authentic gap).

Loads the KB in strict-source-refs mode, pulls the resulting ref_errors
that match the canonical "Unresolved citation ref" format, and prints a
markdown table grouped by category. Suitable for posting in a GitHub
Discussion or planning thread.

Usage:
    py -V:3.12 -m scripts.audit_unresolved_sources
    py -V:3.12 -m scripts.audit_unresolved_sources --root knowledge_base/hosted/content
    py -V:3.12 -m scripts.audit_unresolved_sources --json

Exit codes:
  0 — zero unresolved SRC-* citations
  1 — at least one unresolved citation
  2 — KB root missing / not a directory
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from knowledge_base.validation.loader import (
    _categorize_unresolved_src,
    clear_load_cache,
    load_content,
)

_UNRESOLVED_RE = re.compile(
    r"Unresolved citation ref '(?P<sid>SRC-[A-Z0-9_-]+)' at field '(?P<field>[^']*)'"
)


def _audit(root: Path) -> dict:
    """Walk the KB and return a categorized inventory of unresolved SRC-* IDs.

    Returns a dict shaped::

        {
          "kb_root": str,
          "total_entries": int,         # one per (path, sid) in ref_errors
          "unique_sids": int,
          "by_category": {
            "banned": [{"sid", "hint", "occurrences": [{"path", "field"}]}],
            "typo":   [...],
            "gap":    [...]
          }
        }
    """
    clear_load_cache()
    result = load_content(root, strict_source_refs=True)
    known_src_ids = {
        eid for eid, info in result.entities_by_id.items() if info["type"] == "sources"
    }

    by_sid: dict[str, list[dict]] = defaultdict(list)
    for path, msg in result.ref_errors:
        m = _UNRESOLVED_RE.search(msg)
        if not m:
            continue
        sid = m.group("sid")
        field_label = m.group("field")
        by_sid[sid].append({"path": str(path), "field": field_label})

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for sid, occs in by_sid.items():
        cat, hint = _categorize_unresolved_src(sid, known_src_ids)
        by_cat[cat].append({"sid": sid, "hint": hint, "occurrences": occs})

    for cat in by_cat:
        by_cat[cat].sort(key=lambda e: e["sid"])

    return {
        "kb_root": str(root),
        "total_entries": sum(len(occs) for occs in by_sid.values()),
        "unique_sids": len(by_sid),
        "by_category": dict(by_cat),
    }


def _format_markdown(report: dict) -> str:
    out: list[str] = []
    out.append("# Unresolved SRC-* citation audit")
    out.append("")
    out.append(f"- KB root: `{report['kb_root']}`")
    out.append(f"- Total unresolved entries: **{report['total_entries']}**")
    out.append(f"- Unique SRC-* IDs: **{report['unique_sids']}**")
    out.append("")
    cats = report["by_category"]
    counts = ", ".join(
        f"{cat}={len(cats.get(cat, []))}" for cat in ("banned", "typo", "gap")
    )
    out.append(f"- By category: {counts}")
    out.append("")

    for cat_name, header in (
        ("banned", "Banned per CHARTER §2"),
        ("typo", "Likely typos (Levenshtein ≤ 2)"),
        ("gap", "Authentic gaps (no close match)"),
    ):
        entries = cats.get(cat_name, [])
        out.append(f"## {header} — {len(entries)}")
        out.append("")
        if not entries:
            out.append("_None._")
            out.append("")
            continue
        out.append("| SRC-* ID | Hint | Occurrences |")
        out.append("|---|---|---|")
        for e in entries:
            n = len(e["occurrences"])
            out.append(f"| `{e['sid']}` | {e['hint']} | {n} |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List unresolved SRC-* citations grouped by category.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("knowledge_base/hosted/content"),
        help="Path to hosted/content/ (default: %(default)s).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of markdown.",
    )
    args = parser.parse_args()

    if not args.root.is_dir():
        print(f"ERROR: not a directory: {args.root}", file=sys.stderr)
        return 2

    report = _audit(args.root)
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print(_format_markdown(report))

    return 0 if report["total_entries"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
