"""Wave 7 batch worker — drug-ua-nszu-access-audit chunks #122-#141 (20 chunks × ~5 drugs each).

For each drug in each chunk's manifest:
  - Read drug yaml `regulatory_status.ukraine_registration` block
  - Classify completeness:
    * full: registered + reimbursed_nszu set + reimbursement_indications + last_verified
    * partial: some fields set, others missing
    * minimal: registered field only
    * absent: no ukraine_registration block at all
  - Check `last_verified` staleness (>180d → flag)
  - Generate per-drug audit row
  - Per chunk: produce audit-report.yaml report-only

This is an audit chunk — output is a per-drug status report for
maintainer triage. No KB modifications. No web fetch (chunk-spec says
"record uncertainty explicitly" — flagging gaps without resolving is
valid output).
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DRUG_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "drugs"
CONTRIB_ROOT = REPO_ROOT / "contributions"
TODAY = dt.date(2026, 4, 30)
STALE_DAYS = 180

MANIFESTS_FILE = "/tmp/drug_nszu_manifests.json"


def _drug_yaml_path(drug_id: str) -> Path | None:
    candidate = drug_id.replace("DRUG-", "").lower().replace("-", "_")
    direct = DRUG_DIR / f"{candidate}.yaml"
    if direct.is_file():
        return direct
    for p in DRUG_DIR.glob("*.yaml"):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") == drug_id:
            return p
    return None


def _date_from(value) -> dt.date | None:
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def audit_drug(drug_id: str) -> dict:
    path = _drug_yaml_path(drug_id)
    if path is None:
        return {"drug_id": drug_id, "verdict": "not_found_in_master"}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"drug_id": drug_id, "verdict": "yaml_parse_fail", "error": str(e)[:100]}
    if not isinstance(data, dict):
        return {"drug_id": drug_id, "verdict": "yaml_not_a_mapping"}

    rs = data.get("regulatory_status") or {}
    ua = rs.get("ukraine_registration") if isinstance(rs, dict) else None

    if not isinstance(ua, dict):
        return {
            "drug_id": drug_id,
            "verdict": "ukraine_registration_block_absent",
            "completeness": "absent",
            "fields_missing": ["registered", "reimbursed_nszu", "last_verified", "reimbursement_indications"],
        }

    has_registered = "registered" in ua
    has_reimbursed = "reimbursed_nszu" in ua
    has_lv = "last_verified" in ua
    lv_date = _date_from(ua.get("last_verified")) if has_lv else None
    has_indications = isinstance(ua.get("reimbursement_indications"), list) and ua.get("reimbursement_indications")
    has_notes = bool(ua.get("notes"))

    fields_set = sum([has_registered, has_reimbursed, has_lv, bool(has_indications), has_notes])

    if fields_set >= 4:
        completeness = "full"
    elif fields_set >= 2:
        completeness = "partial"
    elif fields_set == 1:
        completeness = "minimal"
    else:
        completeness = "absent"

    stale = False
    stale_days_count = None
    if lv_date:
        stale_days_count = (TODAY - lv_date).days
        stale = stale_days_count > STALE_DAYS

    fields_missing = []
    if not has_registered: fields_missing.append("registered")
    if not has_reimbursed: fields_missing.append("reimbursed_nszu")
    if not has_lv: fields_missing.append("last_verified")
    if not has_indications: fields_missing.append("reimbursement_indications")

    return {
        "drug_id": drug_id,
        "verdict": "audited",
        "completeness": completeness,
        "registered": ua.get("registered"),
        "reimbursed_nszu": ua.get("reimbursed_nszu"),
        "last_verified": ua.get("last_verified"),
        "stale_days": stale_days_count,
        "is_stale": stale,
        "indication_count": len(ua.get("reimbursement_indications") or []),
        "fields_missing": fields_missing or None,
    }


def process_chunk(chunk_id: str, drug_ids: list[str], issue_number: int) -> dict:
    out_dir = CONTRIB_ROOT / chunk_id
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [audit_drug(did) for did in drug_ids]

    counts = {"full": 0, "partial": 0, "minimal": 0, "absent": 0,
              "not_found_in_master": 0, "yaml_parse_fail": 0,
              "ukraine_registration_block_absent": 0, "stale": 0}
    for r in rows:
        if r["verdict"] == "audited":
            counts[r["completeness"]] += 1
            if r.get("is_stale"):
                counts["stale"] += 1
        elif r["verdict"] in counts:
            counts[r["verdict"]] += 1

    (out_dir / "audit-report.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-30",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Audit-only: per-drug UA-registration completeness check. "
                    "No web fetch to NSZU registry — flagging gaps in existing "
                    "yaml fields. Per chunk-spec: 'record uncertainty explicitly'."
                ),
            },
            "summary": {
                "drug_count": len(drug_ids),
                "completeness_distribution": {
                    "full": counts["full"], "partial": counts["partial"],
                    "minimal": counts["minimal"], "absent": counts["absent"],
                },
                "stale_count": counts["stale"],
                "stale_threshold_days": STALE_DAYS,
                "issues": {
                    "not_found_in_master": counts["not_found_in_master"],
                    "yaml_parse_fail": counts["yaml_parse_fail"],
                },
            },
            "rows": rows,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    (out_dir / "task_manifest.txt").write_text(
        "\n".join(drug_ids) + "\n", encoding="utf-8"
    )

    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-30",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave 7 batch — closes #{issue_number}. UA-NSZU access audit "
                    "for drug manifest. Output is report-only (audit-report.yaml). "
                    "No KB modifications; no web fetch. Worker shared across all "
                    "20 drug-ua-nszu-access-audit chunks."
                ),
                "tasktorrent_version": "2026-04-30-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-drug audit row classifies completeness (full/partial/"
                    "minimal/absent), flags stale `last_verified` (>180d), and "
                    "lists missing fields. NSZU registry web fetch deferred."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    return {
        "chunk_id": chunk_id, "issue_number": issue_number,
        "drug_count": len(drug_ids),
        **counts,
    }


def main() -> int:
    with open(MANIFESTS_FILE, encoding="utf-8") as f:
        manifests = json.load(f)
    summaries = []
    for issue_num_str in sorted(manifests.keys(), key=int):
        n = int(issue_num_str)
        chunk_id, drugs = manifests[issue_num_str]
        s = process_chunk(chunk_id, drugs, n)
        summaries.append(s)
        print(f"  #{n} {chunk_id}: full={s['full']} partial={s['partial']} "
              f"minimal={s['minimal']} absent={s['absent']} stale={s['stale']}",
              file=sys.stderr)
    total = {
        "chunks": len(summaries),
        "full": sum(s["full"] for s in summaries),
        "partial": sum(s["partial"] for s in summaries),
        "minimal": sum(s["minimal"] for s in summaries),
        "absent": sum(s["absent"] for s in summaries),
        "stale": sum(s["stale"] for s in summaries),
    }
    print(f"\nBatch done: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
