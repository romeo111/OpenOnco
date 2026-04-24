"""LOINC subset loader.

LOINC is large (~100K codes) and requires a free Regenstrief account to
download. Per SOURCE_INGESTION_SPEC §13.3 we host only a **subset** —
codes actually used by our Tests. The curator maintains a usage list,
and this loader filters the official Loinc.csv down to that list.

Usage list format: `knowledge_base/hosted/content/_loinc_usage.txt`
    11011-4
    718-7
    ...

Output: knowledge_base/hosted/code_systems/loinc/<version>/codes.yaml
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml


def load_loinc_subset(loinc_csv: Path, usage_list: Path, out_dir: Path, version: str) -> Path:
    wanted = {
        line.strip() for line in usage_list.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }

    rows: list[dict] = []
    with loinc_csv.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            code = (r.get("LOINC_NUM") or "").strip()
            if code in wanted:
                rows.append({
                    "code": code,
                    "long_name": r.get("LONG_COMMON_NAME"),
                    "short_name": r.get("SHORTNAME"),
                    "component": r.get("COMPONENT"),
                    "property": r.get("PROPERTY"),
                    "system": r.get("SYSTEM"),
                    "scale_typ": r.get("SCALE_TYP"),
                    "class": r.get("CLASS"),
                })

    out_dir = out_dir / version
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "codes.yaml"
    payload = {
        "source_id": "SRC-LOINC",
        "version": version,
        "attribution": "This material contains content from LOINC® (http://loinc.org)",
        "curated_subset": True,
        "codes": rows,
    }
    out_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Load LOINC subset filtered by usage list.")
    parser.add_argument("loinc_csv", type=Path, help="Path to Loinc.csv from Regenstrief release")
    parser.add_argument(
        "--usage-list",
        type=Path,
        default=Path("knowledge_base/hosted/content/_loinc_usage.txt"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("knowledge_base/hosted/code_systems/loinc"),
    )
    parser.add_argument("--version", required=True, help="LOINC release version, e.g. v2.76")
    args = parser.parse_args()

    if not args.loinc_csv.is_file():
        print(f"ERROR: LOINC CSV not found: {args.loinc_csv}", file=sys.stderr)
        return 2
    if not args.usage_list.is_file():
        print(f"ERROR: usage list not found: {args.usage_list}", file=sys.stderr)
        return 2

    out = load_loinc_subset(args.loinc_csv, args.usage_list, args.out_dir, args.version)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
