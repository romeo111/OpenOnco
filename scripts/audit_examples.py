"""Verify that public synthetic examples are safe to publish.

This is an engineering quality gate, not clinical sign-off.  It proves that a
registered public profile resolves through the current engine and that its
declared scenario type matches the generated output.  Clinical claims remain
visible with the normal treating-physician verification notice.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
)
from scripts.site_cases import CASES, CaseEntry


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
DEFAULT_EXAMPLES_DIR = REPO_ROOT / "examples"

SELECTION_WARNING_MARKERS = (
    "fell back to",
    "using first current-line candidate",
)


def _audit_case(case: CaseEntry, *, examples_dir: Path, kb_root: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "case_id": case.case_id,
        "file": case.file,
        "visibility": case.visibility,
        "quality_tier": case.quality_tier,
        "scenario_type": case.scenario_type,
        "status": "pass",
        "issues": [],
        "selection_warnings": [],
    }
    profile_path = examples_dir / case.file
    if not profile_path.exists():
        record["status"] = "fail"
        record["issues"].append("registered profile file is missing")
        return record

    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        record["status"] = "fail"
        record["issues"].append(f"profile is not valid JSON: {type(exc).__name__}")
        return record

    try:
        diagnostic = is_diagnostic_profile(profile)
        if diagnostic:
            result = generate_diagnostic_brief(profile, kb_root=kb_root)
            if result.diagnostic_plan is None:
                record["issues"].append("no diagnostic brief generated")
            if case.scenario_type != "diagnostic":
                record["issues"].append("diagnostic profile has non-diagnostic scenario_type")
        else:
            result = generate_plan(profile, kb_root=kb_root)
            plan = result.plan
            if plan is None or not plan.tracks:
                record["issues"].append("no treatment or prevention plan generated")
            if case.scenario_type == "diagnostic":
                record["issues"].append("treatment profile has diagnostic scenario_type")

        for warning in getattr(result, "warnings", []) or []:
            text = str(warning)
            if any(marker in text for marker in SELECTION_WARNING_MARKERS):
                record["selection_warnings"].append(text)
        # A molecular example deliberately demonstrates a biomarker evidence
        # lane against a compact synthetic profile.  Keep selection fallback
        # visible in its audit record, but do not reject an otherwise working
        # BMA scenario as if it were a fully specified patient treatment case.
        if record["selection_warnings"] and case.scenario_type != "molecular":
            record["issues"].append("ambiguous algorithm or indication selection")
    except Exception as exc:  # pragma: no cover - defensive gate reporting
        record["issues"].append(f"engine exception: {type(exc).__name__}: {exc}")

    if record["issues"]:
        record["status"] = "fail"
    return record


def audit_examples(
    *,
    include_internal: bool = False,
    examples_dir: Path = DEFAULT_EXAMPLES_DIR,
    kb_root: Path = DEFAULT_KB_ROOT,
) -> dict[str, Any]:
    """Return a serialisable audit of registered example quality."""
    selected = [case for case in CASES if include_internal or case.visibility == "public"]
    records = [_audit_case(case, examples_dir=examples_dir, kb_root=kb_root) for case in selected]
    registered_files = {case.file for case in CASES}
    on_disk = {path.name for path in examples_dir.glob("*.json")}
    unregistered_bma = sorted(
        filename for filename in on_disk - registered_files if filename.startswith("bma_")
    )
    failures = [record for record in records if record["status"] == "fail"]
    return {
        "scope": "all_registered" if include_internal else "public",
        "summary": {
            "checked": len(records),
            "passed": len(records) - len(failures),
            "failed": len(failures),
            "by_quality_tier": dict(Counter(record["quality_tier"] for record in records)),
            "unregistered_bma_profiles": len(unregistered_bma),
        },
        "failures": failures,
        "unregistered_bma_profiles": unregistered_bma,
        "records": records,
    }


def _markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Example quality audit",
        "",
        f"Scope: `{report['scope']}`",
        "",
        f"- Checked: {summary['checked']}",
        f"- Passed: {summary['passed']}",
        f"- Failed: {summary['failed']}",
        f"- Unregistered BMA profiles: {summary['unregistered_bma_profiles']}",
        "",
    ]
    if report["failures"]:
        lines.extend(["## Failures", ""])
        for record in report["failures"]:
            issues = "; ".join(record["issues"])
            lines.append(f"- `{record['case_id']}` — {issues}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-internal", action="store_true")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    args = parser.parse_args(argv)

    report = audit_examples(include_internal=args.include_internal)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(_markdown(report), encoding="utf-8")

    summary = report["summary"]
    print(
        f"Example audit ({report['scope']}): {summary['passed']}/{summary['checked']} passed; "
        f"{summary['unregistered_bma_profiles']} unregistered BMA profiles"
    )
    for record in report["failures"]:
        print(f"FAIL {record['case_id']}: {'; '.join(record['issues'])}")
    return 1 if summary["failed"] or summary["unregistered_bma_profiles"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
