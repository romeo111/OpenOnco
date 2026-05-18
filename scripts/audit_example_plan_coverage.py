"""Audit coverage of (disease + line + plan) signatures across the KB
and the public example corpus.

Produces:
  docs/example-plan-coverage-report.json
  docs/example-plan-coverage-report.md

Signature = (disease_id, line_of_therapy, recommended_regimen)
            — proxy for "treatment plan". Procedure / radiation_course
              targets are not used in the current KB.

Routeable signatures come from:
  - knowledge_base/hosted/content/algorithms/*.yaml   (output_indications)
  - knowledge_base/hosted/content/indications/*.yaml  (applicable_to)

Public covered signatures come from:
  - examples/*.json + scripts/site_cases.py (CASES, minus
    GALLERY_EXCLUDED_CASE_IDS) + docs/examples.json if present.

Each public example is executed through `generate_plan()` and the
default-indication track is recorded.

Outputs explicitly list:
  - all_routeable
  - covered_signatures
  - missing_signatures
  - duplicate_signatures (same sig covered by 2+ public examples)
  - no_plan_examples       (example produced empty tracks)
  - mismatched_examples    (default_indication does not match its target)
  - ref_error_examples     (load warnings contain "ref error")
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONTENT_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
ALGO_DIR = CONTENT_ROOT / "algorithms"
IND_DIR = CONTENT_ROOT / "indications"
EXAMPLES_DIR = REPO_ROOT / "examples"
DOCS_DIR = REPO_ROOT / "docs"

from knowledge_base.engine import generate_plan  # noqa: E402
from scripts.site_cases import (  # noqa: E402
    CASES,
    GALLERY_EXCLUDED_CASE_IDS,
    BROKEN_CASE_IDS,
)


def _load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _all_indications() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(IND_DIR.glob("*.yaml")):
        d = _load_yaml(p)
        if isinstance(d, dict) and d.get("id"):
            out[d["id"]] = d
    return out


def _all_algorithms() -> list[dict]:
    out: list[dict] = []
    for p in sorted(ALGO_DIR.glob("*.yaml")):
        d = _load_yaml(p)
        if isinstance(d, dict) and d.get("id"):
            out.append(d)
    return out


def _ind_signature(ind: dict) -> tuple[str, int, str] | None:
    """(disease, line, regimen) signature from an indication YAML."""
    appl = ind.get("applicable_to") or {}
    if not isinstance(appl, dict):
        return None
    disease = appl.get("disease_id") or appl.get("disease")
    line = appl.get("line_of_therapy")
    regimen = (
        ind.get("recommended_regimen")
        or ind.get("recommended_procedure")
        or ind.get("recommended_radiation_course")
    )
    if not disease or line is None or not regimen:
        return None
    try:
        line_i = int(line)
    except (ValueError, TypeError):
        return None
    return (disease, line_i, regimen)


def collect_routeable() -> dict[str, Any]:
    """Routeable signatures: any indication that an algorithm can output
    AND that has a `recommended_*` target.

    `algo_routeable` = signatures reachable via some algorithm.
    `ind_only` = indications with valid applicable_to + recommended_* but
                  no algorithm route (handy upper bound).
    """
    indications = _all_indications()
    algos = _all_algorithms()

    algo_indication_ids: set[str] = set()
    for a in algos:
        outs = a.get("output_indications") or []
        if isinstance(outs, list):
            for x in outs:
                if isinstance(x, str):
                    algo_indication_ids.add(x)
        d = a.get("default_indication")
        if isinstance(d, str):
            algo_indication_ids.add(d)
        alt = a.get("alternative_indication")
        if isinstance(alt, str):
            algo_indication_ids.add(alt)

    algo_routeable: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    ind_only: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    for ind_id, ind in indications.items():
        sig = _ind_signature(ind)
        if sig is None:
            continue
        if ind_id in algo_indication_ids:
            algo_routeable[sig].append(ind_id)
        else:
            ind_only[sig].append(ind_id)

    return {
        "algo_routeable": algo_routeable,
        "ind_only": ind_only,
        "indications": indications,
        "algorithms": algos,
    }


def _example_files_for_case(c) -> Path:
    return EXAMPLES_DIR / c.file


def run_example(case) -> dict:
    """Load example JSON, run generate_plan, return summary dict."""
    p = _example_files_for_case(case)
    if not p.exists():
        return {"case_id": case.case_id, "file": case.file, "exists": False}
    try:
        patient = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "case_id": case.case_id, "file": case.file, "exists": True,
            "error": f"json: {e}",
        }
    try:
        result = generate_plan(patient, kb_root=CONTENT_ROOT)
    except Exception as e:
        return {
            "case_id": case.case_id, "file": case.file, "exists": True,
            "error": f"engine: {e}",
        }
    tracks = []
    if result.plan and getattr(result.plan, "tracks", None):
        for t in result.plan.tracks:
            tracks.append({
                "track_id": t.track_id,
                "indication_id": t.indication_id,
                "is_default": t.is_default,
            })
    return {
        "case_id": case.case_id,
        "file": case.file,
        "exists": True,
        "patient_id": patient.get("patient_id"),
        "disease_id": result.disease_id,
        "line_of_therapy": int(patient.get("line_of_therapy", 1)),
        "algorithm_id": result.algorithm_id,
        "default_indication_id": result.default_indication_id,
        "alternative_indication_id": result.alternative_indication_id,
        "tracks": tracks,
        "warnings": list(result.warnings or []),
        "target_indication_id": patient.get("_target_indication_id"),
    }


def build_coverage_report() -> dict[str, Any]:
    routeable = collect_routeable()
    indications = routeable["indications"]
    algo_sigs = routeable["algo_routeable"]
    ind_only_sigs = routeable["ind_only"]

    # Run all public (non-excluded) CASES.
    case_runs: list[dict] = []
    for c in CASES:
        if c.case_id in GALLERY_EXCLUDED_CASE_IDS:
            continue
        case_runs.append(run_example(c))

    # Compute covered signatures and diagnostics.
    covered: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    no_plan_examples: list[dict] = []
    ref_error_examples: list[dict] = []
    mismatched_examples: list[dict] = []
    missing_file: list[dict] = []
    runtime_errors: list[dict] = []

    for r in case_runs:
        if not r.get("exists"):
            missing_file.append(r)
            continue
        if "error" in r:
            runtime_errors.append(r)
            continue
        if any("ref error" in w for w in r.get("warnings", [])):
            ref_error_examples.append(r)
        if not r.get("tracks"):
            no_plan_examples.append(r)
            continue
        default_ind = r.get("default_indication_id")
        if not default_ind or default_ind not in indications:
            no_plan_examples.append(r)
            continue
        ind = indications[default_ind]
        sig = _ind_signature(ind)
        if sig is None:
            continue
        if r.get("target_indication_id") and r["target_indication_id"] != default_ind:
            mismatched_examples.append({**r, "matched_signature": sig})
        # Sanity: signature disease/line should match runtime
        if sig[0] != r["disease_id"] or sig[1] != r["line_of_therapy"]:
            mismatched_examples.append({**r, "matched_signature": sig,
                                         "reason": "disease/line mismatch"})
        covered[sig].append(r["case_id"])

    covered_set = set(covered.keys())
    algo_set = set(algo_sigs.keys())
    ind_only_set = set(ind_only_sigs.keys())
    all_routeable_set = algo_set | ind_only_set

    missing = sorted(algo_set - covered_set)
    missing_ext = sorted(all_routeable_set - covered_set)
    duplicates = {
        f"{s[0]}|line={s[1]}|{s[2]}": cases
        for s, cases in covered.items() if len(cases) > 1
    }

    # Map signatures back to indication ids (so the generator has its
    # input: missing sig → indication candidate).
    sig_to_indications: dict[tuple[str, int, str], list[str]] = defaultdict(list)
    for ind_id, ind in indications.items():
        sig = _ind_signature(ind)
        if sig:
            sig_to_indications[sig].append(ind_id)

    def _sig_record(sig: tuple[str, int, str]) -> dict:
        return {
            "disease_id": sig[0],
            "line_of_therapy": sig[1],
            "regimen_id": sig[2],
            "indication_ids": sorted(sig_to_indications.get(sig, [])),
        }

    report = {
        "summary": {
            "indications_total": len(indications),
            "routeable_via_algorithm": len(algo_set),
            "routeable_via_indication_only": len(ind_only_set),
            "routeable_total_upper_bound": len(all_routeable_set),
            "public_examples_evaluated": len(case_runs),
            "public_covered_signatures": len(covered_set),
            "public_covered_via_algorithm": len(covered_set & algo_set),
            "missing_via_algorithm": len(missing),
            "missing_extended": len(missing_ext),
            "duplicate_signatures": len(duplicates),
            "no_plan_examples": len(no_plan_examples),
            "ref_error_examples": len(ref_error_examples),
            "mismatched_examples": len(mismatched_examples),
            "runtime_errors": len(runtime_errors),
            "missing_file": len(missing_file),
        },
        "all_routeable_signatures": [_sig_record(s) for s in sorted(all_routeable_set)],
        "algo_routeable_signatures": [_sig_record(s) for s in sorted(algo_set)],
        "covered_signatures": [
            {**_sig_record(s), "case_ids": sorted(c)}
            for s, c in sorted(covered.items())
        ],
        "missing_via_algorithm": [_sig_record(s) for s in missing],
        "missing_extended": [_sig_record(s) for s in missing_ext],
        "duplicate_signatures": duplicates,
        "no_plan_examples": no_plan_examples,
        "ref_error_examples": ref_error_examples,
        "mismatched_examples": mismatched_examples,
        "runtime_errors": runtime_errors,
        "missing_file": missing_file,
        "known_broken_case_ids": sorted(BROKEN_CASE_IDS),
    }
    return report


def render_md(report: dict) -> str:
    s = report["summary"]
    lines: list[str] = []
    lines.append("# Example plan coverage report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for k, v in s.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    # Top diseases by signature
    by_disease: dict[str, dict[str, int]] = defaultdict(lambda: {"routeable": 0, "covered": 0})
    for rec in report["all_routeable_signatures"]:
        by_disease[rec["disease_id"]]["routeable"] += 1
    covered_sigs = {(c["disease_id"], c["line_of_therapy"], c["regimen_id"])
                    for c in report["covered_signatures"]}
    routeable_sigs = {(c["disease_id"], c["line_of_therapy"], c["regimen_id"])
                      for c in report["all_routeable_signatures"]}
    for sig in covered_sigs & routeable_sigs:
        by_disease[sig[0]]["covered"] += 1

    lines.append("## Top diseases by routeable signatures")
    lines.append("")
    lines.append("| disease | routeable | covered |")
    lines.append("|---|---:|---:|")
    for d, counts in sorted(by_disease.items(), key=lambda x: -x[1]["routeable"])[:40]:
        lines.append(f"| {d} | {counts['routeable']} | {counts['covered']} |")
    lines.append("")

    lines.append("## Missing via algorithm — first 80")
    lines.append("")
    for rec in report["missing_via_algorithm"][:80]:
        lines.append(
            f"- {rec['disease_id']} · line={rec['line_of_therapy']} · "
            f"{rec['regimen_id']} (indication: {', '.join(rec['indication_ids']) or '∅'})"
        )
    lines.append("")
    if report["no_plan_examples"]:
        lines.append("## No-plan examples")
        lines.append("")
        for r in report["no_plan_examples"]:
            warns = "; ".join(r.get("warnings") or [])[:200]
            lines.append(f"- {r['case_id']} ({r['file']}) — {warns or '(no warnings recorded)'}")
        lines.append("")
    if report["ref_error_examples"]:
        lines.append("## Ref-error examples")
        lines.append("")
        for r in report["ref_error_examples"]:
            warns = "; ".join(w for w in r.get("warnings", []) if "ref error" in w)
            lines.append(f"- {r['case_id']} — {warns[:200]}")
        lines.append("")
    if report["mismatched_examples"]:
        lines.append("## Mismatched examples")
        lines.append("")
        for r in report["mismatched_examples"]:
            lines.append(
                f"- {r['case_id']} target={r.get('target_indication_id')} "
                f"default={r.get('default_indication_id')}"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    report = build_coverage_report()
    (DOCS_DIR / "example-plan-coverage-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    (DOCS_DIR / "example-plan-coverage-report.md").write_text(
        render_md(report), encoding="utf-8"
    )
    s = report["summary"]
    print(f"Routeable via algorithm: {s['routeable_via_algorithm']}")
    print(f"Routeable upper bound:   {s['routeable_total_upper_bound']}")
    print(f"Public examples run:     {s['public_examples_evaluated']}")
    print(f"Public covered:          {s['public_covered_signatures']}")
    print(f"Missing via algorithm:   {s['missing_via_algorithm']}")
    print(f"Missing extended:        {s['missing_extended']}")
    print(f"No-plan examples:        {s['no_plan_examples']}")
    print(f"Ref-error examples:      {s['ref_error_examples']}")
    print(f"Mismatched examples:     {s['mismatched_examples']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
