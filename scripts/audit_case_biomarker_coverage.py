"""Audit public example cases for required biomarker coverage.

The audit uses the production planner plus MDT orchestration and reports the
coverage object surfaced in each tumor-board brief. It is intended for local
QA and optional CI gates, not for changing plan selection.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine import generate_plan, orchestrate_mdt
from scripts.site_cases import CASES, GALLERY_EXCLUDED_CASE_IDS, CaseEntry


@dataclass(frozen=True)
class BiomarkerGap:
    biomarker_id: str
    owner_role: str
    default_track: bool
    tracks: tuple[str, ...]


@dataclass(frozen=True)
class CaseAuditRow:
    case_id: str
    file: str
    disease_id: str | None
    coverage_percent: int
    required_known: int
    required_total: int
    required_missing: int
    missing_default_track: int
    gaps: tuple[BiomarkerGap, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "file": self.file,
            "disease_id": self.disease_id,
            "coverage_percent": self.coverage_percent,
            "required_known": self.required_known,
            "required_total": self.required_total,
            "required_missing": self.required_missing,
            "missing_default_track": self.missing_default_track,
            "gaps": [
                {
                    "biomarker_id": gap.biomarker_id,
                    "owner_role": gap.owner_role,
                    "default_track": gap.default_track,
                    "tracks": list(gap.tracks),
                }
                for gap in self.gaps
            ],
            "warnings": list(self.warnings),
        }


def _is_treatment_case(case: CaseEntry) -> bool:
    return case.badge_class != "bdg-diag" and "Diagnostic Brief" not in case.badge


def _selected_cases(
    *,
    include_diagnostic: bool,
    include_excluded: bool,
    limit: int | None,
) -> list[CaseEntry]:
    out: list[CaseEntry] = []
    for case in CASES:
        if not include_diagnostic and not _is_treatment_case(case):
            continue
        if not include_excluded and case.case_id in GALLERY_EXCLUDED_CASE_IDS:
            continue
        out.append(case)
        if limit is not None and len(out) >= limit:
            break
    return out


def audit_case(case: CaseEntry) -> CaseAuditRow:
    patient_path = EXAMPLES / case.file
    with patient_path.open("r", encoding="utf-8") as fh:
        patient = json.load(fh)

    plan = generate_plan(patient, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(patient, plan, kb_root=KB_ROOT)
    coverage = mdt.data_quality_summary.get("biomarker_coverage") or {}
    missing = coverage.get("missing") or []
    gaps = tuple(
        BiomarkerGap(
            biomarker_id=str(item.get("biomarker_id") or ""),
            owner_role=str(item.get("owner_role") or ""),
            default_track=bool(item.get("default_track")),
            tracks=tuple(str(track) for track in (item.get("tracks") or [])),
        )
        for item in missing
    )
    warnings = tuple(plan.warnings) + tuple(mdt.warnings)

    return CaseAuditRow(
        case_id=case.case_id,
        file=case.file,
        disease_id=plan.disease_id,
        coverage_percent=int(coverage.get("coverage_percent", 100)),
        required_known=int(coverage.get("required_known", 0)),
        required_total=int(coverage.get("required_total", 0)),
        required_missing=int(coverage.get("required_missing", 0)),
        missing_default_track=sum(1 for gap in gaps if gap.default_track),
        gaps=gaps,
        warnings=warnings,
    )


def _sort_rows(rows: list[CaseAuditRow]) -> list[CaseAuditRow]:
    return sorted(
        rows,
        key=lambda row: (
            row.coverage_percent,
            -row.missing_default_track,
            -row.required_missing,
            row.case_id,
        ),
    )


def _print_table(rows: list[CaseAuditRow], *, max_rows: int) -> None:
    if not rows:
        return
    print("Worst biomarker coverage cases:")
    print("case_id\tcoverage\tknown/total\tdefault_gaps\tmissing_biomarkers")
    for row in _sort_rows(rows)[:max_rows]:
        missing_ids = ",".join(gap.biomarker_id for gap in row.gaps) or "-"
        print(
            f"{row.case_id}\t{row.coverage_percent}%\t"
            f"{row.required_known}/{row.required_total}\t"
            f"{row.missing_default_track}\t{missing_ids}"
        )


def _print_summary(rows: list[CaseAuditRow], *, max_rows: int) -> None:
    audited = len(rows)
    avg = round(sum(row.coverage_percent for row in rows) / audited) if audited else 100
    missing_cases = sum(1 for row in rows if row.required_missing)
    default_gap_cases = sum(1 for row in rows if row.missing_default_track)

    print(f"Audited {audited} cases.")
    print(f"Average required biomarker coverage: {avg}%")
    print(f"Cases with missing required biomarkers: {missing_cases}")
    print(f"Cases with default-track biomarker gaps: {default_gap_cases}")
    _print_table([row for row in rows if row.required_missing], max_rows=max_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit example treatment plans for required biomarker coverage."
    )
    parser.add_argument("--limit", type=int, help="Audit only the first N selected cases.")
    parser.add_argument(
        "--include-diagnostic",
        action="store_true",
        help="Include diagnostic-brief cases.",
    )
    parser.add_argument(
        "--include-excluded",
        action="store_true",
        help="Include examples hidden from the public gallery.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of text.",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        default=None,
        metavar="PERCENT",
        help="Exit non-zero if any audited case is below this coverage percent.",
    )
    parser.add_argument(
        "--fail-on-default-missing",
        action="store_true",
        help="Exit non-zero if any default-track required biomarker is missing.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=25,
        help="Maximum rows to print in text mode.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cases = _selected_cases(
        include_diagnostic=args.include_diagnostic,
        include_excluded=args.include_excluded,
        limit=args.limit,
    )
    rows = [audit_case(case) for case in cases]

    if args.json:
        print(json.dumps([row.to_dict() for row in _sort_rows(rows)], indent=2))
    else:
        _print_summary(rows, max_rows=args.max_rows)

    failed_threshold = (
        args.fail_under is not None
        and any(row.coverage_percent < args.fail_under for row in rows)
    )
    failed_default_gap = (
        args.fail_on_default_missing
        and any(row.missing_default_track for row in rows)
    )
    return 1 if failed_threshold or failed_default_gap else 0


if __name__ == "__main__":
    raise SystemExit(main())
