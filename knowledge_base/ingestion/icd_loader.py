"""ICD-O-3.2 code loader.

WHO publishes ICD-O-3 as CSV. Expected columns:
    code, term, behavior, synonyms

Input is split into morphology (9xxx codes) and topography (Cxx codes).

Output: knowledge_base/hosted/code_systems/icd_o_3/<version>/codes.yaml
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml


def parse_icd_o_3_csv(path: Path) -> dict:
    morphology: list[dict] = []
    topography: list[dict] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (row.get("code") or "").strip()
            if not code:
                continue
            entry = {
                "code": code,
                "term": (row.get("term") or "").strip(),
                "synonyms": [
                    s.strip() for s in (row.get("synonyms") or "").split("|") if s.strip()
                ],
            }
            if code.startswith("C"):
                topography.append(entry)
            else:
                behavior = (row.get("behavior") or "").strip()
                if behavior:
                    entry["behavior"] = behavior
                morphology.append(entry)
    return {"morphology": morphology, "topography": topography}


def load_icd_o_3(csv_path: Path, out_dir: Path, version: str = "v2020") -> Path:
    data = parse_icd_o_3_csv(csv_path)
    out_dir = out_dir / version
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "codes.yaml"
    payload = {
        "source_id": "SRC-ICD-O-3",
        "version": version,
        "source_url": "https://www.who.int/standards/classifications/other-classifications/international-classification-of-diseases-for-oncology",
        **data,
    }
    out_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Load ICD-O-3 CSV into YAML.")
    parser.add_argument("csv", type=Path)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("knowledge_base/hosted/code_systems/icd_o_3"),
    )
    parser.add_argument("--version", default="v2020")
    args = parser.parse_args()

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 2

    out = load_icd_o_3(args.csv, args.out_dir, version=args.version)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
