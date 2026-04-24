"""CLI: generate a treatment plan for a patient profile JSON.

Usage:
    python -m knowledge_base.engine.cli examples/patient_zero.json
    python -m knowledge_base.engine.cli patient.json --kb knowledge_base/hosted/content
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .plan import generate_plan


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenOnco rule engine — generate two-plan output.")
    parser.add_argument("patient", type=Path, help="Patient profile JSON")
    parser.add_argument(
        "--kb",
        type=Path,
        default=Path("knowledge_base/hosted/content"),
        help="Path to hosted/content/ root",
    )
    parser.add_argument("--json-output", type=Path, help="Write full PlanResult JSON here")
    parser.add_argument("--verbose", action="store_true", help="Print trace + warnings")
    args = parser.parse_args()

    if not args.patient.is_file():
        print(f"ERROR: patient file not found: {args.patient}", file=sys.stderr)
        return 2

    patient = json.loads(args.patient.read_text(encoding="utf-8"))
    result = generate_plan(patient, kb_root=args.kb)

    print(f"Patient: {result.patient_id or '<anonymous>'}")
    print(f"Disease: {result.disease_id}")
    print(f"Algorithm: {result.algorithm_id}")
    print()
    def _track(ind: dict | None) -> str:
        if not ind:
            return ""
        t = ind.get("plan_track")
        return f" [{t}]" if t else ""

    print(f"  Recommended (default):    {result.default_indication_id}{_track(result.default_indication)}")
    print(f"  Alternative:              {result.alternative_indication_id}{_track(result.alternative_indication)}")

    if args.verbose:
        print("\nTrace:")
        for entry in result.trace:
            print(f"  {entry}")
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    if args.json_output:
        args.json_output.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nFull result written to {args.json_output}")

    if not result.default_indication_id:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
