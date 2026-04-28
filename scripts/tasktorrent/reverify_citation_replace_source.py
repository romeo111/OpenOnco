"""Computational re-verify for `replace_source` rows in citation-verify
v2-style reports.

A `replace_source` action says "the cited claim is supportable, but the
current source is wrong; here is the right SRC-*". The high-stakes failure
mode (observed in PR #23 first submission) is **lexical-match** against
existing SRC-* IDs landing on a semantically-unrelated trial. Example:
"Resolved trial 'MAGNITUDE' to SRC-CHECKMATE-649" — different drug, disease,
mechanism.

This script enforces the title-verification rule: for every `replace_source`
row whose `verified_rationale` contains "Resolved trial '<X>'", the trial
name <X> MUST appear (case-insensitive, stripped of separators) in the
target Source's `title` or `notes` field. If not, the row is rejected.

Usage:
    python -m scripts.tasktorrent.reverify_citation_replace_source <chunk-id>

Examples:
    python -m scripts.tasktorrent.reverify_citation_replace_source citation-semantic-verify-v2

Exit 0 on full pass, 1 on any mismatch.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"
SOURCES_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"

# Match "Resolved trial 'XXX'" or "Resolved trial \"XXX\"" anywhere in rationale.
_TRIAL_RE = re.compile(r"""Resolved trial ['"]([^'"]+)['"]""")


def _load_yaml(p: Path) -> Any:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _normalize(s: str) -> str:
    """Lowercase + strip non-alphanumeric for substring match.

    Example: 'KEYNOTE-522' -> 'keynote522'; 'IMpower-133' -> 'impower133'.
    """
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _build_source_index() -> dict[str, str]:
    """SRC-* id → normalized 'title + notes + attribution.text' blob."""
    idx: dict[str, str] = {}
    if not SOURCES_ROOT.exists():
        return idx
    for p in SOURCES_ROOT.rglob("*.yaml"):
        try:
            doc = _load_yaml(p)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(doc, dict):
            continue
        sid = doc.get("id")
        if not isinstance(sid, str):
            continue
        blob_parts = [
            doc.get("title") or "",
            doc.get("notes") or "",
        ]
        attr = doc.get("attribution")
        if isinstance(attr, dict):
            blob_parts.append(str(attr.get("text") or ""))
        idx[sid] = _normalize(" ".join(blob_parts))
    return idx


def _find_report(chunk_dir: Path) -> Path | None:
    """v1-shape: citation-report.yaml. v2-shape: citation-report-v2.yaml.
    Take whichever exists (prefer v2 if both)."""
    for name in ("citation-report-v2.yaml", "citation-report.yaml"):
        p = chunk_dir / name
        if p.exists():
            return p
    return None


def _iter_rows(report: dict) -> list[dict]:
    """Both v1 (`findings`) and v2 (`rows`) shapes supported."""
    if isinstance(report.get("rows"), list):
        return [r for r in report["rows"] if isinstance(r, dict)]
    if isinstance(report.get("findings"), list):
        return [r for r in report["findings"] if isinstance(r, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("chunk_id")
    args = parser.parse_args()

    chunk_dir = CONTRIB_ROOT / args.chunk_id
    if not chunk_dir.exists():
        print(f"chunk dir missing: {chunk_dir}", file=sys.stderr)
        return 1

    report_path = _find_report(chunk_dir)
    if report_path is None:
        print(f"no report file in {chunk_dir}", file=sys.stderr)
        return 1

    print(f"Loading report: {report_path.relative_to(REPO_ROOT)}")
    report = _load_yaml(report_path)
    if not isinstance(report, dict):
        print("report top-level not a mapping", file=sys.stderr)
        return 1

    print("Building Source title/notes index...")
    src_idx = _build_source_index()
    print(f"  {len(src_idx)} sources indexed")

    rows = _iter_rows(report)
    repl_rows = [
        r for r in rows
        if r.get("suggested_action") == "replace_source"
    ]
    print(f"\nReplace-source rows: {len(repl_rows)}")

    mismatches: list[tuple[str, str, str, str]] = []
    no_trial_pattern = 0
    src_not_found = 0
    for r in repl_rows:
        fid = r.get("finding_id", "?")
        rat = r.get("verified_rationale") or ""
        target_src = (
            r.get("suggested_replacement_source_id")
            or r.get("suggested_replacement_source")
            or ""
        )
        m = _TRIAL_RE.search(rat)
        if not m:
            no_trial_pattern += 1
            continue
        trial = m.group(1)
        norm_trial = _normalize(trial)
        if not norm_trial:
            continue
        target_blob = src_idx.get(target_src)
        if target_blob is None:
            src_not_found += 1
            mismatches.append((fid, trial, target_src, "TARGET SRC-* not in hosted sources"))
            continue
        if norm_trial not in target_blob:
            mismatches.append(
                (fid, trial, target_src, "trial name not in target title/notes")
            )

    print(f"\nReport summary:")
    print(f"  rows without 'Resolved trial' pattern (no check applies): {no_trial_pattern}")
    print(f"  rows with target SRC-* not on master: {src_not_found}")
    print(f"  rows with trial-vs-title mismatch: {len(mismatches)}")
    if mismatches:
        print("\nMismatch detail (up to 30):")
        for fid, trial, src, reason in mismatches[:30]:
            print(f"  {fid}: trial='{trial}' target={src} ({reason})")
        if len(mismatches) > 30:
            print(f"  ... +{len(mismatches) - 30} more")
        return 1
    print("\nAll replace_source rows pass title-verification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
