"""Generate maintainer-friendly triage markdown queues from
citation-verify-v2 (or v1) report.

For citation-verify chunks the report is `citation-report-v2.yaml`
(with `rows`) or `citation-report.yaml` (with `findings`). Each row
carries verified_status (supported/unsupported/unclear/access_blocked/
broken_link), suggested_action, and a verified_rationale.

This script groups rows by `verified_status` and `suggested_action` and
emits a walkable markdown queue per filter so maintainer can act
row-by-row.

Usage:
    python -m scripts.tasktorrent.triage_citation_verify <chunk-id> --status unsupported
    python -m scripts.tasktorrent.triage_citation_verify citation-semantic-verify-v2 --status supported
    python -m scripts.tasktorrent.triage_citation_verify citation-semantic-verify-v2 --action source_stub_needed
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"


def _load_yaml(p: Path) -> Any:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_field_value(entity_file: str, field_path: str) -> str:
    p = REPO_ROOT / entity_file
    if not p.exists():
        return f"<entity file not found: {entity_file}>"
    try:
        doc = _load_yaml(p)
    except Exception as exc:  # noqa: BLE001
        return f"<YAML parse error: {exc}>"
    if not isinstance(doc, dict):
        return "<top-level not a mapping>"
    cur: Any = doc
    for part in field_path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return f"<cannot resolve {field_path} on non-mapping>"
        if cur is None:
            return f"<{field_path} is null or missing>"
    return str(cur).strip()


def _emit_row(r: dict, idx: int, total: int) -> str:
    out: list[str] = []
    fid = r.get("finding_id", "?")
    vs = r.get("verified_status", "?")
    sa = r.get("suggested_action", "?")
    out.append(f"## {idx}/{total}: {fid} - {vs} -> {sa}\n")
    if r.get("entity_id"):
        out.append(f"**Entity:** `{r.get('entity_id')}`")
    if r.get("entity_file"):
        out.append(f"**File:** `{r.get('entity_file')}`")
    if r.get("claim_locator"):
        out.append(f"**Claim locator:** `{r.get('claim_locator')}`")
    if r.get("source_id"):
        out.append(f"**v1 source_id:** `{r.get('source_id')}`")
    if r.get("source_section"):
        out.append(f"**Source section:** {r.get('source_section')}")
    out.append("")

    # Show current entity field value if entity_file + claim_locator look like a field path
    if r.get("entity_file") and r.get("claim_locator"):
        loc = r["claim_locator"]
        # claim_locator may be either field name (e.g. "evidence_summary") or path
        # ("docs/reviews/...:line"). Only fetch if it looks like a plain field path.
        if ":" not in loc and "/" not in loc:
            cur = _read_field_value(r["entity_file"], loc)
            if len(cur) > 1500:
                cur = cur[:1500] + "...[truncated]"
            out.append("**Current value:**")
            out.append("```")
            out.append(cur)
            out.append("```")
            out.append("")

    if r.get("claim_excerpt"):
        out.append(f"**Claim excerpt:**\n```\n{r.get('claim_excerpt','')[:600]}\n```\n")
    if r.get("finding_text"):
        out.append(f"**Audit finding text:**\n```\n{r.get('finding_text','')[:600]}\n```\n")

    rat = r.get("verified_rationale") or r.get("rationale") or ""
    if rat:
        rat_str = str(rat)
        if len(rat_str) > 800:
            rat_str = rat_str[:800] + "...[truncated]"
        out.append("**Verification rationale:**")
        out.append("```")
        out.append(rat_str)
        out.append("```")
        out.append("")

    if r.get("suggested_replacement_source_id"):
        out.append(f"**Suggested replacement SRC-***: `{r.get('suggested_replacement_source_id')}`")
        out.append("")

    if r.get("notes"):
        out.append(f"**Notes:** {r.get('notes')}\n")

    if vs == "unsupported":
        actions = [
            "- [ ] revise claim (edit the entity field to match what source actually says)",
            "- [ ] replace_source (find correct cited Source)",
            "- [ ] dismiss (audit was wrong; claim is fine as-is)",
            "- [ ] escalate to Co-Lead",
        ]
    elif vs == "supported":
        actions = [
            "- [ ] keep (no edit needed)",
            "- [ ] apply suggested replace_source (if action=replace_source)",
            "- [ ] re-verify locally (if rationale looks shaky)",
        ]
    elif vs == "access_blocked":
        actions = [
            "- [ ] dismiss (paywalled banned source; current claim acceptable)",
            "- [ ] file source_stub for alternative source",
            "- [ ] escalate",
        ]
    else:  # unclear / broken_link / other
        actions = [
            "- [ ] keep (genuinely unresolvable; no edit)",
            "- [ ] file source_stub_needed (attempt to find authoritative source)",
            "- [ ] revise_claim (narrow the claim wording)",
            "- [ ] escalate",
        ]
    out.append("**Maintainer action:**")
    out.extend(actions)
    out.append("")
    out.append("---\n")
    return "\n".join(out)


def _find_report(chunk_dir: Path) -> Path | None:
    for name in ("citation-report-v2.yaml", "citation-report.yaml"):
        p = chunk_dir / name
        if p.exists():
            return p
    return None


def _iter_rows(report: dict) -> list[dict]:
    if isinstance(report.get("rows"), list):
        return [r for r in report["rows"] if isinstance(r, dict)]
    if isinstance(report.get("findings"), list):
        return [r for r in report["findings"] if isinstance(r, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("chunk_id")
    parser.add_argument("--status", default=None, help="filter by verified_status")
    parser.add_argument("--action", default=None, help="filter by suggested_action")
    parser.add_argument("--limit", type=int, default=0, help="cap output (0 = all)")
    args = parser.parse_args()

    chunk_dir = CONTRIB_ROOT / args.chunk_id
    if not chunk_dir.exists():
        print(f"chunk dir missing: {chunk_dir}", file=sys.stderr)
        return 1

    report_path = _find_report(chunk_dir)
    if report_path is None:
        print(f"no report file in {chunk_dir}", file=sys.stderr)
        return 1

    report = _load_yaml(report_path)
    if not isinstance(report, dict):
        print("report top-level not a mapping", file=sys.stderr)
        return 1

    rows = _iter_rows(report)
    if args.status:
        rows = [r for r in rows if r.get("verified_status") == args.status]
    if args.action:
        rows = [r for r in rows if r.get("suggested_action") == args.action]
    if args.limit:
        rows = rows[: args.limit]

    if not rows:
        print(f"No rows match filter (status={args.status}, action={args.action})")
        return 0

    suffix_parts = []
    if args.status:
        suffix_parts.append(f"status-{args.status}")
    if args.action:
        suffix_parts.append(f"action-{args.action}")
    if not suffix_parts:
        suffix_parts.append("all")
    out_path = chunk_dir / f"triage-queue-{'_'.join(suffix_parts)}.md"

    out: list[str] = []
    out.append(f"# Triage Queue: {args.chunk_id}\n")
    if args.status or args.action:
        out.append(f"**Filter:** status=`{args.status}`, action=`{args.action}`\n")
    out.append(f"**Total rows:** {len(rows)}\n")
    out.append("---\n")
    for i, r in enumerate(rows, 1):
        out.append(_emit_row(r, i, len(rows)))

    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Triage queue written: {out_path.relative_to(REPO_ROOT)}")
    print(f"  {len(rows)} rows (filter: status={args.status}, action={args.action})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
