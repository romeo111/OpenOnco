"""CTCAE v5.0 loader.

CTCAE is published by NCI as an Excel workbook (.xlsx). Extract the
"CTCAE Terms" sheet and feed it as CSV (or convert in-place with
openpyxl) — this loader parses CSV for simplicity.

Expected CSV columns:
    MedDRA_SOC, CTCAE_Term, Grade_1, Grade_2, Grade_3, Grade_4, Grade_5

Output: knowledge_base/hosted/ctcae/v5.0/grading.yaml
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable

import yaml


def parse_ctcae_csv(rows: Iterable[dict]) -> list[dict]:
    adverse_events: list[dict] = []
    for row in rows:
        term = (row.get("CTCAE_Term") or "").strip()
        if not term:
            continue
        code_slug = term.lower().replace(" ", "_").replace("/", "_")
        adverse_events.append({
            "code": f"CTCAE.{code_slug}",
            "term": term,
            "soc_category": (row.get("MedDRA_SOC") or "").strip() or None,
            "grades": {
                "1": (row.get("Grade_1") or "").strip(),
                "2": (row.get("Grade_2") or "").strip(),
                "3": (row.get("Grade_3") or "").strip(),
                "4": (row.get("Grade_4") or "").strip(),
                "5": (row.get("Grade_5") or "").strip(),
            },
        })
    return adverse_events


def load_ctcae(csv_path: Path, out_dir: Path) -> Path:
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        aes = parse_ctcae_csv(reader)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "grading.yaml"
    payload = {
        "version": "v5.0",
        "source_url": "https://ctep.cancer.gov/protocolDevelopment/electronic_applications/ctc.htm",
        "fetched_at": None,
        "adverse_events": aes,
    }
    out_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Load CTCAE v5.0 CSV into YAML.")
    parser.add_argument("csv", type=Path, help="CTCAE v5.0 CSV (converted from NCI Excel)")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("knowledge_base/hosted/ctcae/v5.0"),
    )
    args = parser.parse_args()

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 2

    out = load_ctcae(args.csv, args.out_dir)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
