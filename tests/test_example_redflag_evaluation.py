"""Quality gate for unevaluated RedFlags in shipped example plans.

The MDT data-quality layer reports `unevaluated_red_flags` when a relevant
RedFlag trigger references a finding absent from the patient example. Public
gallery examples are synthetic but should be complete enough to produce plans
without unresolved RedFlag-evaluation gaps.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
    orchestrate_mdt,
)
from scripts.site_cases import CASES, GALLERY_EXCLUDED_CASE_IDS


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"

def _public_treatment_example_quality() -> list[tuple[str, str, str, dict]]:
    """Return one row per gallery treatment example that generates a Plan.

    Row shape: (case_id, example_file, disease_id, data_quality_summary).
    Diagnostic briefs are outside this treatment-plan gate. Cases explicitly
    excluded from the public gallery are also out of scope for this URL-level
    quality contract.
    """
    rows: list[tuple[str, str, str, dict]] = []
    for case in CASES:
        if case.case_id in GALLERY_EXCLUDED_CASE_IDS:
            continue
        patient = json.loads((EXAMPLES / case.file).read_text(encoding="utf-8"))
        if is_diagnostic_profile(patient):
            continue

        plan_result = generate_plan(patient, kb_root=KB_ROOT)
        assert plan_result.plan is not None, (
            f"public gallery case {case.case_id} must generate a treatment plan"
        )

        mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)
        rows.append(
            (case.case_id, case.file, plan_result.disease_id or "", mdt.data_quality_summary)
        )
    return rows


def _failure_details(
    rows: list[tuple[str, str, str, dict]],
    *,
    limit: int = 20,
) -> str:
    by_case = sorted(
        (
            (
                len(data_quality.get("unevaluated_red_flags") or []),
                data_quality.get("status"),
                case_id,
                file_name,
                disease_id,
            )
            for case_id, file_name, disease_id, data_quality in rows
            if data_quality.get("status") != "complete_for_mdt_review"
            or data_quality.get("unevaluated_red_flags")
        ),
        reverse=True,
    )
    by_rf: Counter[str] = Counter()
    for *_prefix, data_quality in rows:
        by_rf.update(data_quality.get("unevaluated_red_flags") or [])

    case_lines = "\n".join(
        f"  {count:>2}  {status}  {case_id} ({disease_id}, {file_name})"
        for count, status, case_id, file_name, disease_id in by_case[:limit]
    )
    rf_lines = "\n".join(
        f"  {count:>2}  {rf_id}" for rf_id, count in by_rf.most_common(limit)
    )
    return f"\nTop affected cases:\n{case_lines}\nTop unevaluated RedFlags:\n{rf_lines}"


def test_public_gallery_treatment_examples_are_complete_for_mdt_review() -> None:
    rows = _public_treatment_example_quality()

    failing = [
        row
        for row in rows
        if row[3].get("status") != "complete_for_mdt_review"
        or row[3].get("unevaluated_red_flags")
    ]
    if failing:
        pytest.fail(
            "Public gallery treatment examples must be complete for MDT review "
            "and render no unevaluated RedFlags."
            + _failure_details(rows)
        )


def test_public_gallery_diagnostic_examples_generate_briefs() -> None:
    failures: list[str] = []
    for case in CASES:
        if case.case_id in GALLERY_EXCLUDED_CASE_IDS:
            continue
        patient = json.loads((EXAMPLES / case.file).read_text(encoding="utf-8"))
        if not is_diagnostic_profile(patient):
            continue
        try:
            brief = generate_diagnostic_brief(patient, kb_root=KB_ROOT)
        except Exception as exc:  # pragma: no cover - failure message path
            failures.append(f"{case.case_id}: {type(exc).__name__}: {exc}")
            continue
        if brief is None:
            failures.append(f"{case.case_id}: diagnostic brief is None")

    assert not failures, "Public diagnostic gallery examples failed:\n" + "\n".join(failures)
