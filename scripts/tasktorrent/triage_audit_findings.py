"""Generate maintainer-friendly triage markdown queues from audit-report
sidecars (rec-wording-audit-claim-bearing, ua-translation-review-batch,
citation-verify-914-audit).

Audit reports list per-finding context but suggested_correction /
suggested_rewording fields are meta-descriptions ("Replace X with Y such
as Z"), not literal drop-in replacements. Mechanical bulk-apply produces
wrong fixes. This script generates a markdown queue maintainers can walk
through, opening one entity at a time with the finding context displayed
+ a one-click link to the source field.

Usage:
    python -m scripts.tasktorrent.triage_audit_findings <chunk-id> [--severity critical|moderate|minor]
    python -m scripts.tasktorrent.triage_audit_findings rec-wording-audit-claim-bearing
    python -m scripts.tasktorrent.triage_audit_findings ua-translation-review-batch --severity critical

Outputs:
    contributions/<chunk-id>/triage-queue-<severity>.md

Per-finding output includes:
- entity_id + entity_file path (clickable in editors)
- field_path + current value (full, not truncated)
- finding context (matched_pattern, severity, category)
- suggested action / rewording from contributor
- maintainer checkbox: [ ] applied | [ ] dismissed | [ ] needs-discussion

Exits 0 on successful queue generation.
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


def _emit_finding(f: dict, idx: int, total: int) -> str:
    lines: list[str] = []
    lines.append(f"## {idx}/{total}: {f.get('finding_id', '?')} - {(f.get('severity') or '?').upper()}\n")
    lines.append(f"**Entity:** `{f.get('entity_id', '?')}`")
    lines.append(f"**File:** `{f.get('entity_file', '?')}`")
    lines.append(f"**Field:** `{f.get('field_path', '?')}`")
    if f.get("category"):
        lines.append(f"**Category:** {f.get('category')}")
    if f.get("matched_pattern"):
        lines.append(f"**Matched pattern:** `{f.get('matched_pattern')}`")
    if f.get("pattern_class"):
        lines.append(f"**Pattern class:** {f.get('pattern_class')}")
    lines.append("")

    if f.get("entity_file") and f.get("field_path"):
        current = _read_field_value(f["entity_file"], f["field_path"])
        if len(current) > 1500:
            current = current[:1500] + "...[truncated]"
        lines.append("**Current value:**")
        lines.append("```")
        lines.append(current)
        lines.append("```")
        lines.append("")

    if f.get("excerpt"):
        lines.append(f"**Excerpt context:**\n```\n{f.get('excerpt','')[:600]}\n```\n")
    if f.get("en_excerpt"):
        lines.append(f"**EN excerpt:**\n```\n{f.get('en_excerpt','')[:600]}\n```\n")
    if f.get("ua_excerpt"):
        lines.append(f"**UA excerpt:**\n```\n{f.get('ua_excerpt','')[:600]}\n```\n")

    sugg = f.get("suggested_rewording") or f.get("suggested_correction") or ""
    if sugg:
        lines.append("**Contributor suggestion:**")
        lines.append("```")
        lines.append(str(sugg))
        lines.append("```")
        lines.append("")

    if f.get("notes"):
        lines.append(f"**Notes:** {f.get('notes')}\n")
    if f.get("judgment"):
        lines.append(f"**Contributor judgment:** {f.get('judgment')}\n")

    lines.append("**Maintainer action:**")
    lines.append("- [ ] applied (edited the field with appropriate rewording)")
    lines.append("- [ ] dismissed (false positive / not actually a violation)")
    lines.append("- [ ] needs-discussion (escalate)")
    lines.append("")
    lines.append("---\n")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("chunk_id")
    parser.add_argument("--severity", default=None, help="critical | moderate | minor")
    parser.add_argument("--limit", type=int, default=0, help="cap output (0 = all)")
    args = parser.parse_args()

    report_path = CONTRIB_ROOT / args.chunk_id / "audit-report.yaml"
    if not report_path.exists():
        print(f"audit-report not found: {report_path}", file=sys.stderr)
        return 1

    doc = _load_yaml(report_path)
    if not isinstance(doc, dict):
        print("audit-report top-level not a mapping", file=sys.stderr)
        return 1

    findings = [f for f in doc.get("findings", []) if isinstance(f, dict)]
    if args.severity:
        findings = [f for f in findings if f.get("severity") == args.severity]
    if args.limit:
        findings = findings[: args.limit]

    if not findings:
        print(f"No findings match filter (chunk={args.chunk_id} severity={args.severity})")
        return 0

    out_name = (
        f"triage-queue-{args.severity}.md" if args.severity else "triage-queue-all.md"
    )
    out_path = CONTRIB_ROOT / args.chunk_id / out_name

    lines: list[str] = []
    lines.append(f"# Triage Queue: {args.chunk_id}\n")
    if args.severity:
        lines.append(f"**Filter:** severity = `{args.severity}`\n")
    lines.append(f"**Total findings in queue:** {len(findings)}\n")
    lines.append(
        "Walk through each finding. Read the current value (fetched from "
        "entity file), the contributor's suggestion (often a meta-description, "
        "not a literal replacement), and decide: edit the field with appropriate "
        "rewording, dismiss as false positive, or escalate.\n"
    )
    lines.append("---\n")

    for i, f in enumerate(findings, 1):
        lines.append(_emit_finding(f, i, len(findings)))

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Triage queue written: {out_path.relative_to(REPO_ROOT)}")
    print(f"  {len(findings)} findings (filter: severity={args.severity or 'any'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
