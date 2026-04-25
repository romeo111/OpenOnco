"""CLI: generate a treatment plan for a patient profile JSON.

Usage:
    python -m knowledge_base.engine.cli examples/patient_zero_indolent.json
    python -m knowledge_base.engine.cli patient.json --kb knowledge_base/hosted/content
    python -m knowledge_base.engine.cli patient.json --json-output plan.json --verbose
    python -m knowledge_base.engine.cli patient.json --mdt
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

from .mdt_orchestrator import orchestrate_mdt
from .plan import generate_plan

# Force UTF-8 stdout so Cyrillic + symbols print correctly on Windows cp1252
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def _print_track(t, indent: str = "  ") -> None:
    flag = " * DEFAULT" if t.is_default else ""
    print(f"{indent}[{t.track_id}]{flag}  {t.label} ({t.label_en})")
    print(f"{indent}  Indication: {t.indication_id}")
    if t.regimen_data:
        print(f"{indent}  Regimen:    {t.regimen_data.get('id')} — {t.regimen_data.get('name', '')}")
    if t.supportive_care_data:
        sc = ", ".join(s.get("id", "?") for s in t.supportive_care_data)
        print(f"{indent}  Supportive: {sc}")
    if t.contraindications_data:
        ci = ", ".join(c.get("id", "?") for c in t.contraindications_data)
        print(f"{indent}  Contraindications: {ci}")
    if t.selection_reason:
        print(f"{indent}  Reason: {t.selection_reason[:100]}")


def _print_role_block(label: str, roles) -> None:
    if not roles:
        return
    print(f"  {label} ({len(roles)}):")
    for r in roles:
        print(f"    - [{r.role_id}] {r.role_name}")
        print(f"        reason:  {r.reason}")
        if r.linked_questions:
            print(f"        owns:    {', '.join(r.linked_questions)}")


def _print_mdt_brief(mdt) -> None:
    print()
    print("=== MDT Brief ===")
    print(f"  Plan:    {mdt.plan_id}")
    print(f"  Disease: {mdt.disease_id}")
    print()
    _print_role_block("Required roles", mdt.required_roles)
    _print_role_block("Recommended roles", mdt.recommended_roles)
    _print_role_block("Optional roles", mdt.optional_roles)

    if mdt.open_questions:
        blocking = sum(1 for q in mdt.open_questions if q.blocking)
        print(f"  Open questions ({len(mdt.open_questions)}, {blocking} blocking):")
        for q in mdt.open_questions:
            tag = "[BLOCKING] " if q.blocking else ""
            print(f"    - {tag}{q.id} (owner: {q.owner_role})")
            print(f"        Q: {q.question}")
            print(f"        why: {q.rationale}")
    else:
        print("  Open questions: none")

    dq = mdt.data_quality_summary or {}
    print("  Data quality:")
    print(f"    Missing critical:    {len(dq.get('missing_critical_fields') or [])}")
    print(f"    Missing recommended: {len(dq.get('missing_recommended_fields') or [])}")
    if dq.get("missing_critical_fields"):
        print(f"      → {', '.join(dq['missing_critical_fields'])}")

    if mdt.warnings:
        print("  Warnings:")
        for w in mdt.warnings:
            print(f"    - {w}")


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenOnco rule engine — generate a Plan with multiple tracks.")
    parser.add_argument("patient", type=Path, help="Patient profile JSON")
    parser.add_argument(
        "--kb",
        type=Path,
        default=Path("knowledge_base/hosted/content"),
        help="Path to hosted/content/ root",
    )
    parser.add_argument("--json-output", type=Path, help="Write full Plan JSON here")
    parser.add_argument("--verbose", action="store_true", help="Print trace + warnings + sources")
    parser.add_argument(
        "--mdt",
        action="store_true",
        help="Print MDT brief: required/recommended roles, open questions, data quality",
    )
    args = parser.parse_args()

    if not args.patient.is_file():
        print(f"ERROR: patient file not found: {args.patient}", file=sys.stderr)
        return 2

    patient = json.loads(args.patient.read_text(encoding="utf-8"))
    result = generate_plan(patient, kb_root=args.kb)

    print(f"Patient:   {result.patient_id or '<anonymous>'}")
    print(f"Disease:   {result.disease_id}")
    print(f"Algorithm: {result.algorithm_id}")

    if result.plan:
        print(f"Plan id:   {result.plan.id}  (v{result.plan.version})")
        print()
        print(f"Tracks ({len(result.plan.tracks)}):")
        for t in result.plan.tracks:
            _print_track(t)
            print()

        fda = result.plan.fda_compliance
        print("FDA Criterion 4 metadata (surfaced in rendered document):")
        print(f"  Intended use:   {fda.intended_use}")
        print(f"  HCP user:       {fda.hcp_user_specification[:100]}...")
        print(f"  Population:     {fda.patient_population_match}")
        print(f"  Algorithm:      {fda.algorithm_summary[:100]}...")
        print(f"  Time-critical:  {fda.time_critical}")
        if fda.data_limitations:
            print(f"  Limitations:    {len(fda.data_limitations)} item(s)")
        if args.verbose:
            print(f"  Sources cited:  {len(fda.data_sources_summary)}")
            for s in fda.data_sources_summary:
                print(f"    - {s}")

    if args.verbose:
        print("\nTrace:")
        for entry in result.trace:
            print(f"  {entry}")
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    mdt = None
    if args.mdt:
        mdt = orchestrate_mdt(patient, result, kb_root=args.kb)
        _print_mdt_brief(mdt)

    if args.json_output:
        payload = result.to_dict()
        if mdt is not None:
            payload["mdt"] = mdt.to_dict()
        args.json_output.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        print(f"\nFull Plan JSON written to {args.json_output}")

    if not result.default_indication_id:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
