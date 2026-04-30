"""Wave 7 batch worker — bma-ua-signoff-prep chunks #64-#83 (20 chunks × 5 BMAs).

For each BMA: prepare for UA clinical-language signoff. Check
UA-translation completeness and flag fields that block
`ukrainian_review_status: signed_off`.

Per-BMA checks:
  * has `evidence_summary_ua`?
  * has `notes_ua`?
  * `ukrainian_review_status` value (pending_clinical_signoff / signed_off / etc.)
  * `ukrainian_drafted_by` present?
  * Translation completeness — does evidence_summary_ua have UA Cyrillic
    chars at all? (proxy for "translated", not "left as English")
  * Mixed-language detection — significant English fragments inside
    UA fields (basic ratio)

Output: per-chunk audit-report.yaml — report-only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CONTRIB_ROOT = REPO_ROOT / "contributions"
MANIFESTS_FILE = "/tmp/bma_signoff_manifests.json"

# Cyrillic block — Ukrainian / Russian Cyrillic letters (rough)
CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
# Latin word (≥4 chars to filter out abbreviations) — proxy for "English fragment"
LATIN_WORD_RE = re.compile(r"\b[a-zA-Z]{4,}\b")


def _bma_path(bma_id: str) -> Path | None:
    candidate = bma_id.replace("BMA-", "").lower().replace("-", "_")
    direct = BMA_DIR / f"bma_{candidate}.yaml"
    if direct.is_file():
        return direct
    for p in BMA_DIR.glob("*.yaml"):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") == bma_id:
            return p
    return None


def text_metrics(s: str) -> dict:
    if not isinstance(s, str) or not s:
        return {"length": 0, "cyrillic_chars": 0, "latin_words": 0,
                "language_mix_ratio": 0.0, "is_translated": False}
    cyr = len(CYRILLIC_RE.findall(s))
    latin = len(LATIN_WORD_RE.findall(s))
    total_letters = cyr + sum(1 for c in s if c.isalpha())
    mix = (latin / max(1, latin + (cyr / 4))) if cyr or latin else 0.0
    return {
        "length": len(s),
        "cyrillic_chars": cyr,
        "latin_words_count": latin,
        "language_mix_ratio": round(mix, 2),
        "is_translated": cyr > 20,
    }


def audit_bma(bma_id: str) -> dict:
    path = _bma_path(bma_id)
    if path is None:
        return {"bma_id": bma_id, "verdict": "not_found_in_master"}
    try:
        bma = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"bma_id": bma_id, "verdict": "yaml_parse_fail", "error": str(e)[:100]}
    if not isinstance(bma, dict):
        return {"bma_id": bma_id, "verdict": "yaml_not_a_mapping"}

    es_ua = bma.get("evidence_summary_ua") or ""
    notes_ua = bma.get("notes_ua") or ""
    review_status = bma.get("ukrainian_review_status")
    drafted_by = bma.get("ukrainian_drafted_by")
    es_metrics = text_metrics(es_ua)
    notes_metrics = text_metrics(notes_ua)

    blockers: list[str] = []
    if not es_ua: blockers.append("missing_evidence_summary_ua")
    elif not es_metrics["is_translated"]: blockers.append("evidence_summary_ua_not_translated")
    elif es_metrics["language_mix_ratio"] > 0.5: blockers.append("evidence_summary_ua_high_english_mix")

    if not bma.get("evidence_summary"): blockers.append("missing_evidence_summary_en")
    if not review_status: blockers.append("missing_ukrainian_review_status")
    if review_status == "signed_off": blockers.append("already_signed_off")  # nothing to prep

    signoff_ready = (
        review_status == "pending_clinical_signoff"
        and "missing_evidence_summary_ua" not in blockers
        and "evidence_summary_ua_not_translated" not in blockers
        and "evidence_summary_ua_high_english_mix" not in blockers
    )

    return {
        "bma_id": bma_id,
        "verdict": "audited",
        "ukrainian_review_status": review_status,
        "ukrainian_drafted_by": drafted_by,
        "evidence_summary_ua_metrics": es_metrics,
        "notes_ua_metrics": notes_metrics,
        "signoff_ready": signoff_ready,
        "blockers": blockers or None,
    }


def process_chunk(chunk_id: str, bma_ids: list[str], issue_number: int) -> dict:
    out_dir = CONTRIB_ROOT / chunk_id
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [audit_bma(b) for b in bma_ids]
    n_audited = sum(1 for r in rows if r["verdict"] == "audited")
    n_ready = sum(1 for r in rows if r["verdict"] == "audited" and r.get("signoff_ready"))
    n_blocked = sum(1 for r in rows if r["verdict"] == "audited" and not r.get("signoff_ready"))
    n_signed = sum(1 for r in rows if r["verdict"] == "audited"
                   and r.get("ukrainian_review_status") == "signed_off")
    n_missing = sum(1 for r in rows if r["verdict"] != "audited")

    (out_dir / "audit-report.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-30",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Audit-only: per-BMA UA-translation readiness check. "
                    "Flags blockers preventing ukrainian_review_status: signed_off. "
                    "No KB modifications. The actual signoff is human-review later."
                ),
            },
            "summary": {
                "bma_count": len(bma_ids),
                "audited": n_audited,
                "signoff_ready": n_ready,
                "blocked": n_blocked,
                "already_signed_off": n_signed,
                "missing_or_parse_fail": n_missing,
            },
            "rows": rows,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    (out_dir / "task_manifest.txt").write_text("\n".join(bma_ids) + "\n", encoding="utf-8")

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
                    f"Wave 7 batch — closes #{issue_number}. UA-signoff readiness "
                    "audit. Per-BMA check of UA-translation fields + status flags. "
                    "Worker shared across all 20 chunks."
                ),
                "tasktorrent_version": "2026-04-30-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-BMA row gives Cyrillic/Latin metrics + blocker list. "
                    "Maintainer / Co-Lead uses this as the prep-list for actual "
                    "signoff session."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    return {
        "chunk_id": chunk_id, "issue_number": issue_number,
        "bma_count": len(bma_ids), "audited": n_audited,
        "signoff_ready": n_ready, "blocked": n_blocked,
        "already_signed_off": n_signed,
    }


def main() -> int:
    with open(MANIFESTS_FILE, encoding="utf-8") as f:
        manifests = json.load(f)
    summaries = []
    for k in sorted(manifests.keys(), key=int):
        n = int(k)
        chunk_id, bmas = manifests[k]
        s = process_chunk(chunk_id, bmas, n)
        summaries.append(s)
        print(f"  #{n}: ready={s['signoff_ready']} blocked={s['blocked']} "
              f"signed_off={s['already_signed_off']} (of {s['bma_count']})", file=sys.stderr)
    total = {
        "chunks": len(summaries),
        "ready": sum(s["signoff_ready"] for s in summaries),
        "blocked": sum(s["blocked"] for s in summaries),
        "already_signed_off": sum(s["already_signed_off"] for s in summaries),
    }
    print(f"\nBatch done: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
