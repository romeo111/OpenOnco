"""ATC / DDD loader — manual curation only.

WHO Collaborating Centre restricts bulk redistribution (commercial use
triggers license per SOURCE_INGESTION_SPEC §2.6). Per §13.5 we maintain
a **small manual YAML** with just the ~15–20 ATC codes for drugs in our
Regimens, re-curated annually.

This loader is thin: it reads a maintained YAML file as-is and only
validates its shape. To add a new ATC code, edit the YAML directly and
re-run the validator.

Format (`knowledge_base/hosted/code_systems/atc/2025/codes.yaml`):
    source_id: SRC-ATC
    attribution: "ATC/DDD: WHO Collaborating Centre..."
    codes:
      - atc: L01FA01
        name: Rituximab
        ddd: null
      ...
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = {"atc", "name"}


def validate_atc_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["Root is not a mapping"]
    if "codes" not in data or not isinstance(data["codes"], list):
        errors.append("Missing list 'codes'")
        return errors
    for i, entry in enumerate(data["codes"]):
        if not isinstance(entry, dict):
            errors.append(f"codes[{i}]: not a mapping")
            continue
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            errors.append(f"codes[{i}]: missing fields {missing}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate manually-curated ATC YAML.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: not found: {args.path}", file=sys.stderr)
        return 2

    errs = validate_atc_file(args.path)
    if errs:
        for e in errs:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"OK — {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
