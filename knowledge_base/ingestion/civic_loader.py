"""CIViC loader — TSV → YAML.

CIViC publishes nightly bulk TSV dumps at
https://civicdb.org/downloads/nightly/nightly-ClinicalEvidenceSummaries.tsv

CC0 licence — we can host fully (SOURCE_INGESTION_SPEC §2.5).

Output: knowledge_base/hosted/civic/<date>/evidence.yaml
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml


def parse_civic_tsv(path: Path) -> list[dict]:
    entries: list[dict] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            entries.append({
                "id": row.get("evidence_id") or row.get("id"),
                "gene": row.get("gene"),
                "variant": row.get("variant"),
                "disease": row.get("disease"),
                "doid": row.get("doid"),
                "drugs": [d.strip() for d in (row.get("drugs") or "").split(",") if d.strip()],
                "evidence_level": row.get("evidence_level"),
                "evidence_type": row.get("evidence_type"),
                "clinical_significance": row.get("clinical_significance"),
                "evidence_direction": row.get("evidence_direction"),
                "pmid": row.get("pubmed_id"),
                "rating": row.get("rating"),
            })
    return entries


def load_civic(tsv_path: Path, out_root: Path, snapshot_date: str | None = None) -> Path:
    snapshot_date = snapshot_date or date.today().isoformat()
    entries = parse_civic_tsv(tsv_path)

    out_dir = out_root / snapshot_date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "evidence.yaml"
    payload = {
        "source_id": "SRC-CIVIC",
        "snapshot_date": snapshot_date,
        "source_url": "https://civicdb.org/downloads/nightly/",
        "license": "CC0-1.0",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "evidence_items": entries,
    }
    out_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Load a CIViC nightly TSV into YAML.")
    parser.add_argument("tsv", type=Path)
    parser.add_argument(
        "--out-root",
        type=Path,
        default=Path("knowledge_base/hosted/civic"),
    )
    parser.add_argument("--date", help="YYYY-MM-DD snapshot date (default: today)")
    args = parser.parse_args()

    if not args.tsv.is_file():
        print(f"ERROR: TSV not found: {args.tsv}", file=sys.stderr)
        return 2

    out = load_civic(args.tsv, args.out_root, snapshot_date=args.date)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
