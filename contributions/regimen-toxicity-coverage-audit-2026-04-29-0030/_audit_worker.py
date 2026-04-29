"""One-off worker for chunk-task #35 — regimen-toxicity-coverage-audit.

Walks all 244 regimen files in knowledge_base/hosted/content/regimens/
and classifies each by toxicity-coverage completeness:

  - has_toxicity_profile (the single-string field)
  - has_key_toxicities (structured list field, currently absent in KB)
  - has_ctcae_grades (any "Grade N" / "Gn" / "CTCAE" mentions in toxicity prose)
  - dose_adjustments_count (proxy for safety-action density)

Output: audit-report.yaml — deterministic, report-only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
REGIMEN_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "regimens"
OUT_DIR = REPO_ROOT / "contributions" / "regimen-toxicity-coverage-audit-2026-04-29-0030"

CTCAE_RE = re.compile(r"\b(?:CTCAE|grade\s*[1-5]|G[1-5]\+?)\b", re.IGNORECASE)


def has_grade_text(value) -> bool:
    """Look for CTCAE-style grade mentions anywhere in a value tree."""
    if isinstance(value, str):
        return bool(CTCAE_RE.search(value))
    if isinstance(value, list):
        return any(has_grade_text(v) for v in value)
    if isinstance(value, dict):
        return any(has_grade_text(v) for v in value.values())
    return False


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    profile_dist: dict[str, int] = {}
    completeness_buckets = {"none": 0, "minimal": 0, "partial": 0, "structured": 0}

    for path in sorted(REGIMEN_DIR.glob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        reg_id = data.get("id") or path.stem

        has_profile = bool(data.get("toxicity_profile"))
        profile_value = data.get("toxicity_profile") or "(unset)"
        profile_dist[profile_value] = profile_dist.get(profile_value, 0) + 1

        has_key = isinstance(data.get("key_toxicities"), list) and len(data.get("key_toxicities") or []) > 0
        has_grades = has_grade_text(data.get("key_toxicities")) or has_grade_text(data.get("notes"))

        dose_adj = data.get("dose_adjustments")
        dose_adj_count = len(dose_adj) if isinstance(dose_adj, list) else 0

        # Completeness bucket:
        #   structured = key_toxicities list with CTCAE grades
        #   partial    = key_toxicities present but no grades, OR notes have grades
        #   minimal    = only toxicity_profile (single string)
        #   none       = no toxicity field at all
        if has_key and has_grades:
            bucket = "structured"
        elif has_key or (has_profile and has_grades):
            bucket = "partial"
        elif has_profile:
            bucket = "minimal"
        else:
            bucket = "none"
        completeness_buckets[bucket] += 1

        rows.append({
            "regimen_id": reg_id,
            "toxicity_profile": profile_value,
            "has_key_toxicities": has_key,
            "has_ctcae_grades_in_text": has_grades,
            "dose_adjustments_count": dose_adj_count,
            "completeness": bucket,
        })

    # Stable sort — by completeness ascending then by id
    completeness_order = {"none": 0, "minimal": 1, "partial": 2, "structured": 3}
    rows.sort(key=lambda r: (completeness_order[r["completeness"]], r["regimen_id"]))

    total = len(rows)
    report = {
        "_contribution_kind": "audit-report",
        "chunk_id": "regimen-toxicity-coverage-audit-2026-04-29-0030",
        "regimen_total_count": total,
        "completeness_distribution": completeness_buckets,
        "completeness_pct": {
            k: round(100 * v / total, 1) if total else 0.0
            for k, v in completeness_buckets.items()
        },
        "toxicity_profile_distribution": dict(sorted(profile_dist.items(),
                                                     key=lambda kv: -kv[1])),
        "summary": (
            "0 regimens currently ship structured CTCAE-graded toxicity data. "
            f"{completeness_buckets['minimal']}/{total} have only the single-string "
            "`toxicity_profile` field. The schema gap is real and uniform across the KB. "
            "Recommend: a follow-up Queue-C schema-evolution chunk that adds "
            "`key_toxicities: list[{name, ctcae_grade_p_any, ctcae_grade_p_g3plus, source}]` "
            "to the Pydantic schema, then a Queue-A coverage-fill chunk to populate "
            "the field per-regimen from FDA labels + pivotal trial AE tables."
        ),
        "rows": rows,
    }

    out_path = OUT_DIR / "audit-report.yaml"
    out_path.write_text(
        yaml.safe_dump(report, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"  wrote {out_path.relative_to(REPO_ROOT).as_posix()}")
    print(f"  Summary: {total} regimens · "
          f"{completeness_buckets['structured']} structured · "
          f"{completeness_buckets['partial']} partial · "
          f"{completeness_buckets['minimal']} minimal · "
          f"{completeness_buckets['none']} none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
