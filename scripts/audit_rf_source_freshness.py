#!/usr/bin/env python3
"""Flag RedFlags whose `last_reviewed` is older than the most recent year
embedded in any of their cited sources' `version` field.

Complements `audit_freshness.py` (which only checks SLA age in months).
This one catches a different failure mode: an RF that was reviewed
on-cadence but cites a source for which a newer revision has since
landed in the KB. Example: RF reviewed 2024-12-15 cites
SRC-NCCN-OVARIAN-2025 (NCCN annual revision). The SLA audit says "fresh"
because <12 months elapsed; this audit says "behind source" because
the guideline year is newer than the review year.

Source version parsing is intentionally lenient — `version` in the KB is
free-text (e.g. "2025", "v4.2", "accessed 2026-05-08", "March 2024"). We
extract the *latest 4-digit year* via regex; sources without a parseable
year are skipped silently (those without provenance dates can't drive a
staleness check). Draft RFs (`draft: true`) are skipped too — they're
flagged separately by the validator.

Usage:
  python scripts/audit_rf_source_freshness.py
  python scripts/audit_rf_source_freshness.py --human
  python scripts/audit_rf_source_freshness.py --output rf_source_freshness.json

Exit codes:
  0 — every non-draft RF is at-or-ahead of its cited sources
  1 — at least one RF is behind a cited source
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

YEAR_RE = re.compile(r"\b(20\d{2})\b")


def _latest_year(version_str: str | None) -> int | None:
    """Extract the latest 4-digit year (2000-2099) from a free-text
    version string. Returns None when no year is present."""
    if not version_str:
        return None
    years = [int(m.group(1)) for m in YEAR_RE.finditer(str(version_str))]
    return max(years) if years else None


def _review_year(last_reviewed: str | None) -> int | None:
    """Parse the year out of an ISO-style `last_reviewed`. Tolerates
    'YYYY-MM-DD', 'YYYY-MM', and bare 'YYYY'. None when missing."""
    if not last_reviewed:
        return None
    m = YEAR_RE.search(str(last_reviewed))
    return int(m.group(1)) if m else None


def _load_sources_index(sources_dir: Path) -> dict[str, dict]:
    """Build {SRC-ID: {version, title, ...}} from every source YAML."""
    index: dict[str, dict] = {}
    for path in sorted(sources_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("id"):
            index[data["id"]] = data
    return index


def _audit_rf(rf_data: dict, sources_index: dict[str, dict]) -> dict | None:
    """Return a finding dict if the RF is behind a cited source; else None."""
    rid = rf_data.get("id")
    if not rid:
        return None
    if rf_data.get("draft") is True:
        return None
    review_year = _review_year(rf_data.get("last_reviewed"))
    cited = rf_data.get("sources") or []

    behind: list[dict] = []
    for sid in cited:
        src = sources_index.get(sid)
        if not src:
            continue  # unresolved source ref — validator flags this separately
        src_year = _latest_year(src.get("version"))
        if src_year is None:
            continue
        if review_year is None or src_year > review_year:
            behind.append({
                "source_id": sid,
                "source_year": src_year,
                "source_title": src.get("title") or src.get("citation") or sid,
            })
    if not behind:
        return None
    return {
        "id": rid,
        "last_reviewed": rf_data.get("last_reviewed"),
        "review_year": review_year,
        "behind_sources": behind,
    }


def audit(kb_root: Path = KB_ROOT) -> dict:
    sources_index = _load_sources_index(kb_root / "sources")
    findings: list[dict] = []
    total = 0
    # rglob — `redflags/universal/*.yaml` holds the cross-disease RFs
    # (HBV reactivation, TLS, infusion reaction); a flat glob misses them.
    for path in sorted((kb_root / "redflags").rglob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        total += 1
        f = _audit_rf(data, sources_index)
        if f:
            findings.append(f)
    return {
        "total_redflags_scanned": total,
        "sources_indexed": len(sources_index),
        "behind_count": len(findings),
        "findings": findings,
    }


def _format_human(report: dict) -> str:
    lines = [
        f"Scanned: {report['total_redflags_scanned']} non-draft RFs against "
        f"{report['sources_indexed']} sources",
        f"Behind a cited source: {report['behind_count']}",
        "",
    ]
    for f in report["findings"][:50]:
        rev = f["review_year"] or "<never>"
        srcs = ", ".join(
            f"{b['source_id']} ({b['source_year']})" for b in f["behind_sources"]
        )
        lines.append(f"  {f['id']:55s}  reviewed={rev}  behind: {srcs}")
    if len(report["findings"]) > 50:
        lines.append(f"  ... and {len(report['findings']) - 50} more")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--human", action="store_true", help="human-readable summary")
    parser.add_argument("--output", type=Path, help="write JSON report here")
    parser.add_argument(
        "--kb",
        type=Path,
        default=KB_ROOT,
        help="path to knowledge_base/hosted/content",
    )
    args = parser.parse_args()

    report = audit(args.kb)
    if args.output:
        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    if args.human:
        print(_format_human(report))
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["behind_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
