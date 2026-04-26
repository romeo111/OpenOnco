"""Generate sign-off coverage dashboard markdown.

Walks the KB, counts sign-offs per entity / entity-type / disease, then
joins recent activity from `knowledge_base/hosted/audit/signoffs.jsonl`.

Output: `docs/plans/signoff_status_<YYYY-MM-DD>.md`.

Usage:
    py scripts/build_signoff_dashboard.py
    py scripts/build_signoff_dashboard.py --out custom.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
REVIEWERS_DIR = KB_ROOT / "reviewers"
AUDIT_LOG = REPO_ROOT / "knowledge_base" / "hosted" / "audit" / "signoffs.jsonl"

SIGNOFF_ELIGIBLE_DIRS = [
    "indications",
    "algorithms",
    "regimens",
    "redflags",
    "biomarker_actionability",
]
ENTITY_TYPE_LABEL = {
    "indications": "Indication",
    "algorithms": "Algorithm",
    "regimens": "Regimen",
    "redflags": "RedFlag",
    "biomarker_actionability": "BiomarkerActionability",
}


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _load_reviewers() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not REVIEWERS_DIR.is_dir():
        return out
    for p in sorted(REVIEWERS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("id"):
            out[data["id"]] = data
    return out


def _entity_disease_id(data: dict, dir_name: str) -> Optional[str]:
    if dir_name == "indications":
        a = data.get("applicable_to") or {}
        return a.get("disease_id") if isinstance(a, dict) else None
    if dir_name == "algorithms":
        return data.get("applicable_to_disease")
    if dir_name == "redflags":
        rd = data.get("relevant_diseases") or []
        if isinstance(rd, list) and rd and rd[0] != "*":
            return rd[0]
    if dir_name == "biomarker_actionability":
        return data.get("disease_id")
    return None


def _walk_entities() -> list[dict]:
    """Return list of {id, dir, signoffs (list), disease_id}."""
    out: list[dict] = []
    for d in SIGNOFF_ELIGIBLE_DIRS:
        root = KB_ROOT / d
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*.yaml")):
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            if not isinstance(data, dict):
                continue
            signoffs = data.get("reviewer_signoffs_v2") or []
            if not isinstance(signoffs, list):
                signoffs = []
            out.append({
                "id": data.get("id"),
                "dir": d,
                "signoffs": [s for s in signoffs if isinstance(s, dict)],
                "disease_id": _entity_disease_id(data, d),
            })
    return out


def _load_audit() -> list[dict]:
    if not AUDIT_LOG.exists():
        return []
    rows: list[dict] = []
    for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _load_disease_label_map() -> dict[str, str]:
    out: dict[str, str] = {}
    diseases_dir = KB_ROOT / "diseases"
    if not diseases_dir.is_dir():
        return out
    for p in sorted(diseases_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        did = data.get("id")
        if not did:
            continue
        names = data.get("names") or {}
        label = (
            (names.get("ukrainian") or names.get("preferred") or names.get("english") or did)
            if isinstance(names, dict) else did
        )
        out[did] = str(label)
    return out


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def build_dashboard() -> str:
    entities = _walk_entities()
    audit = _load_audit()
    reviewers = _load_reviewers()
    disease_labels = _load_disease_label_map()
    today = _today()

    total = len(entities)
    with_1 = sum(1 for e in entities if len(e["signoffs"]) >= 1)
    with_2 = sum(1 for e in entities if len(e["signoffs"]) >= 2)
    with_0 = total - with_1

    # Per type
    per_type: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "ge1": 0, "ge2": 0, "zero": 0})
    for e in entities:
        bucket = per_type[e["dir"]]
        bucket["total"] += 1
        n = len(e["signoffs"])
        if n >= 1:
            bucket["ge1"] += 1
        if n >= 2:
            bucket["ge2"] += 1
        if n == 0:
            bucket["zero"] += 1

    # Per disease
    per_disease: dict[str, dict[str, int]] = defaultdict(lambda: {"indications": 0, "algorithms": 0, "signoffs_total": 0})
    for e in entities:
        did = e["disease_id"] or "(disease-agnostic)"
        if e["dir"] == "indications":
            per_disease[did]["indications"] += 1
        elif e["dir"] == "algorithms":
            per_disease[did]["algorithms"] += 1
        per_disease[did]["signoffs_total"] += len(e["signoffs"])

    # Per reviewer
    per_reviewer_approve: dict[str, int] = defaultdict(int)
    per_reviewer_withdraw: dict[str, int] = defaultdict(int)
    per_reviewer_recent: dict[str, str] = defaultdict(str)
    for row in audit:
        rid = row.get("reviewer_id")
        if not rid:
            continue
        if row.get("action") == "approve":
            per_reviewer_approve[rid] += 1
        elif row.get("action") == "withdraw":
            per_reviewer_withdraw[rid] += 1
        ts = row.get("timestamp") or ""
        if ts > per_reviewer_recent[rid]:
            per_reviewer_recent[rid] = ts

    # ── Markdown assembly ────────────────────────────────────────────
    md: list[str] = []
    md.append(f"# Clinical Sign-off Status — {today}")
    md.append("")
    md.append("CHARTER §6.1: any clinical-content change needs ≥2 of three Clinical Co-Lead sign-offs.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Total entities requiring sign-off: **{total}**")
    pct_1 = f"{(with_1/total*100):.1f}" if total else "0.0"
    pct_2 = f"{(with_2/total*100):.1f}" if total else "0.0"
    md.append(f"- Entities with ≥1 sign-off: **{with_1}** ({pct_1}%)")
    md.append(f"- Entities with ≥2 sign-offs (CHARTER §6.1 minimum): **{with_2}** ({pct_2}%)")
    md.append(f"- Entities with 0 sign-offs: **{with_0}**")
    md.append("")

    md.append("## Per entity-type")
    md.append("")
    rows = []
    for d in SIGNOFF_ELIGIBLE_DIRS:
        b = per_type[d]
        rows.append([
            ENTITY_TYPE_LABEL.get(d, d),
            b["total"],
            b["ge1"],
            b["ge2"],
            b["zero"],
        ])
    md.append(_md_table(["Type", "Total", "≥1 sign-off", "≥2 sign-offs", "0 sign-offs"], rows))
    md.append("")

    md.append("## Per disease (top 20 by indication count)")
    md.append("")
    sorted_diseases = sorted(
        per_disease.items(),
        key=lambda kv: (-kv[1]["indications"], -kv[1]["algorithms"], kv[0]),
    )[:20]
    rows = []
    for did, b in sorted_diseases:
        label = disease_labels.get(did, did) if did != "(disease-agnostic)" else did
        avg = (b["signoffs_total"] / max(b["indications"] + b["algorithms"], 1))
        rows.append([
            f"{label} (`{did}`)",
            b["indications"],
            b["algorithms"],
            f"{avg:.2f}",
        ])
    md.append(_md_table(["Disease", "Indications", "Algorithms", "Sign-offs (avg)"], rows))
    md.append("")

    md.append("## Per reviewer")
    md.append("")
    rows = []
    for rid, profile in sorted(reviewers.items()):
        rows.append([
            f"{rid}",
            profile.get("display_name", "—"),
            per_reviewer_approve.get(rid, 0),
            per_reviewer_recent.get(rid, "—") or "—",
            per_reviewer_withdraw.get(rid, 0),
        ])
    # Reviewers with audit activity but no profile — surface as orphans.
    for rid in sorted(set(per_reviewer_approve) | set(per_reviewer_withdraw)):
        if rid not in reviewers:
            rows.append([
                f"{rid} (orphan — no profile)",
                "—",
                per_reviewer_approve.get(rid, 0),
                per_reviewer_recent.get(rid, "—"),
                per_reviewer_withdraw.get(rid, 0),
            ])
    md.append(_md_table(["Reviewer", "Display name", "Approvals", "Most-recent", "Withdrawals"], rows))
    md.append("")

    md.append("## Recent activity (last 7 days, max 50 entries)")
    md.append("")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    recent = [r for r in audit if (r.get("timestamp") or "") >= cutoff]
    recent.sort(key=lambda r: r.get("timestamp") or "", reverse=True)
    recent = recent[:50]
    if recent:
        rows = [[
            r.get("timestamp", "")[:19],
            r.get("reviewer_id", ""),
            r.get("action", ""),
            r.get("entity_id", ""),
            (r.get("rationale") or "")[:80],
        ] for r in recent]
        md.append(_md_table(["Timestamp", "Reviewer", "Action", "Entity", "Rationale"], rows))
    else:
        md.append("_No activity in the last 7 days._")
    md.append("")
    md.append(f"---")
    md.append(f"_Generated {today} from `knowledge_base/hosted/audit/signoffs.jsonl`._")
    md.append("")
    return "\n".join(md)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="build_signoff_dashboard")
    parser.add_argument("--out", help="Output path (default docs/plans/signoff_status_<today>.md)")
    args = parser.parse_args(argv)

    md = build_dashboard()
    if args.out:
        out = Path(args.out)
    else:
        out = REPO_ROOT / "docs" / "plans" / f"signoff_status_{_today()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out} ({len(md):,} chars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
