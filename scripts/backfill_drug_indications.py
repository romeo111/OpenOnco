"""Generate draft DrugIndication rows from existing Indication/Regimen links.

This is a schema-evolution helper for the drug label/off-label tracking gap.
It infers candidate rows only; it does not determine whether a use is labeled,
off-label, reimbursed, or guideline-supported. Generated YAML stays
`draft: true` and `unknown_pending_review` until reviewed against regulatory,
guideline, and reimbursement Sources.

Usage:
    python scripts/backfill_drug_indications.py --report
    python scripts/backfill_drug_indications.py --write-yaml
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
INDICATIONS = CONTENT / "indications"
REGIMENS = CONTENT / "regimens"
OUT_DIR = CONTENT / "drug_indications"
REPORT_OUT = REPO_ROOT / "docs" / "audits" / "drug_indication_backfill_candidates.json"


def _load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def _source_ids(indication: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for item in indication.get("sources") or []:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict) and isinstance(item.get("source_id"), str):
            out.append(item["source_id"])
    return sorted(set(out))


def _slug(entity_id: str) -> str:
    text = re.sub(r"^(DRUG|DIS|IND|REG)-", "", entity_id.upper())
    text = re.sub(r"[^A-Z0-9]+", "-", text).strip("-")
    return text or "UNKNOWN"


def _candidate_id(drug_id: str, indication_id: str) -> str:
    return f"DIND-{_slug(drug_id)}-{_slug(indication_id)}"


def load_regimens() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted(REGIMENS.glob("*.yaml")):
        data = _load_yaml(path)
        if data and isinstance(data.get("id"), str):
            rows[data["id"]] = data
    return rows


def build_candidates() -> list[dict[str, Any]]:
    regimens = load_regimens()
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for path in sorted(INDICATIONS.glob("*.yaml")):
        indication = _load_yaml(path)
        if not indication:
            continue
        ind_id = indication.get("id")
        regimen_id = indication.get("recommended_regimen")
        applicable = indication.get("applicable_to") or {}
        disease_id = applicable.get("disease_id") if isinstance(applicable, dict) else None
        line = applicable.get("line_of_therapy") if isinstance(applicable, dict) else None
        if not (
            isinstance(ind_id, str)
            and isinstance(regimen_id, str)
            and isinstance(disease_id, str)
        ):
            continue

        regimen = regimens.get(regimen_id) or {}
        components = regimen.get("components") or []
        if not isinstance(components, list):
            continue

        sources = _source_ids(indication)
        for comp in components:
            if not isinstance(comp, dict):
                continue
            drug_id = comp.get("drug_id")
            if not isinstance(drug_id, str):
                continue
            key = (drug_id, disease_id, ind_id)
            if key in seen:
                continue
            seen.add(key)
            row = {
                "id": _candidate_id(drug_id, ind_id),
                "drug_id": drug_id,
                "disease_id": disease_id,
                "indication_id": ind_id,
                "regimen_id": regimen_id,
                "line_of_therapy": line,
                "clinical_context": "inferred from Indication.recommended_regimen",
                "label_status": "unknown_pending_review",
                "reimbursement_status": "unknown_pending_review",
                "regulatory_statuses": [
                    {"jurisdiction": "FDA", "status": "unknown_pending_review"},
                    {"jurisdiction": "EMA", "status": "unknown_pending_review"},
                    {"jurisdiction": "Ukraine", "status": "unknown_pending_review"},
                ],
                "reimbursement_statuses": [
                    {
                        "jurisdiction": "Ukraine",
                        "payer": "NSZU",
                        "status": "unknown_pending_review",
                    }
                ],
                "nccn_category": indication.get("nccn_category"),
                "evidence_source_refs": sources,
                "sources": sources,
                "inferred_from": {
                    "indication_id": ind_id,
                    "regimen_id": regimen_id,
                    "component_drug_id": drug_id,
                },
                "draft": True,
                "notes": (
                    "Generated backfill candidate. Verify jurisdiction-specific "
                    "label/off-label and reimbursement status before review."
                ),
            }
            rows.append(row)
    return sorted(rows, key=lambda r: r["id"])


def write_yaml(rows: list[dict[str, Any]]) -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for row in rows:
        path = OUT_DIR / f"{row['id'].lower().replace('-', '_')}.yaml"
        if path.exists():
            continue
        path.write_text(
            yaml.safe_dump(row, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        written += 1
    return written


def write_report(rows: list[dict[str, Any]]) -> None:
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(
        json.dumps(
            {
                "generated_by": "scripts/backfill_drug_indications.py",
                "candidate_count": len(rows),
                "quality_gate": (
                    "All rows are draft unknown_pending_review candidates. "
                    "Do not mark reviewed without source-backed clinical and "
                    "regulatory review."
                ),
                "rows": rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true", help="Write JSON candidate report.")
    parser.add_argument("--write-yaml", action="store_true", help="Write draft YAML rows.")
    args = parser.parse_args(argv)

    rows = build_candidates()
    if args.report or not args.write_yaml:
        write_report(rows)
        print(f"Wrote {REPORT_OUT.relative_to(REPO_ROOT)} ({len(rows)} candidates)")
    if args.write_yaml:
        written = write_yaml(rows)
        print(f"Wrote {written} draft YAML rows under {OUT_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
