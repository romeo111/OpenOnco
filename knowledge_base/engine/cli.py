"""CLI: generate a treatment plan or diagnostic brief for a patient profile.

Usage:
    python -m knowledge_base.engine.cli examples/patient_zero_indolent.json
    python -m knowledge_base.engine.cli patient.json --kb knowledge_base/hosted/content
    python -m knowledge_base.engine.cli patient.json --json-output plan.json --verbose
    python -m knowledge_base.engine.cli patient.json --mdt
    python -m knowledge_base.engine.cli patient.json --diagnostic --mdt
    python -m knowledge_base.engine.cli patient_v2.json --revise prev_plan.json \
        --revision-trigger "biopsy result 2026-05-10 → DLBCL confirmed"

Mode auto-detect:
- patient.disease.id OR .icd_o_3_morphology present → treatment mode (Plan)
- only patient.disease.suspicion present                → diagnostic mode (DiagnosticPlan)
- --diagnostic flag forces diagnostic mode (errors if confirmed diagnosis present)
- --revise PREV.json + --revision-trigger "..."  → generate next-version plan that
  supersedes the previous one. Auto-detects diagnostic→diagnostic /
  diagnostic→treatment / treatment→treatment. Refuses treatment→diagnostic.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

from .diagnostic import (
    _DIAGNOSTIC_BANNER,
    DiagnosticPlanResult,
    generate_diagnostic_brief,
    is_diagnostic_profile,
    is_treatment_profile,
)
from .mdt_orchestrator import orchestrate_mdt
from .persistence import (
    DEFAULT_ROOT as PATIENT_PLANS_ROOT,
    list_versions,
    load_result,
    save_result,
    update_superseded_by_on_disk,
)
from .plan import PlanResult, generate_plan
from .render import (
    render_diagnostic_brief_html,
    render_plan_html,
    render_revision_note_html,
)
from .revisions import revise_plan

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

    agg = mdt.aggregation_summary or {}
    if agg:
        print("  AI-агрегація (step 2 per project infographic):")
        print(f"    KB entities loaded:       {agg.get('kb_entities_loaded')}")
        print(f"    Indications evaluated:    {agg.get('indications_evaluated')}")
        print(f"    Sources cited:            {len(agg.get('kb_sources_cited') or [])}")
        print(f"    Biomarkers referenced:    {len(agg.get('biomarkers_referenced') or [])}")
        print(f"    RedFlags fired / total:   {len(agg.get('red_flags_fired') or [])} / {agg.get('red_flags_total_in_kb')}")
        print(f"    Open questions raised:    {agg.get('open_questions_raised')}")
        clients = agg.get("live_api_clients_available") or []
        if clients:
            print(f"    Live API clients ready:   {', '.join(clients)}")

    if mdt.warnings:
        print("  Warnings:")
        for w in mdt.warnings:
            print(f"    - {w}")


def _print_diagnostic_brief(result) -> None:
    print()
    print("=" * 72)
    print("  " + _DIAGNOSTIC_BANNER)
    print("=" * 72)
    print(f"Patient:        {result.patient_id or '<anonymous>'}")
    if result.suspicion:
        print(f"Suspicion:      lineage={result.suspicion.lineage_hint}, "
              f"tissues={', '.join(result.suspicion.tissue_locations) or '-'}")
        if result.suspicion.working_hypotheses:
            print(f"Hypotheses:     {', '.join(result.suspicion.working_hypotheses)}")
    print(f"Matched workup: {result.matched_workup_id or '<none>'}")
    if result.diagnostic_plan:
        dp = result.diagnostic_plan
        print(f"Plan id:        {dp.id}  (v{dp.version})")
        print(f"Timeline:       ~{dp.expected_timeline_days} днів")
        print()
        print(f"Workup steps ({len(dp.workup_steps)}):")
        for s in dp.workup_steps:
            line = f"  {s.step}. [{s.category}] {s.description or s.test_id or '?'}"
            print(line)
            if s.rationale:
                print(f"      rationale: {s.rationale[:100]}")
            if s.biopsy_approach:
                print(f"      biopsy preferred: {s.biopsy_approach.preferred[:90]}")
            if s.ihc_panel and s.ihc_panel.baseline:
                print(f"      IHC baseline: {', '.join(s.ihc_panel.baseline)}")
        print()
        if dp.mandatory_questions:
            print(f"Mandatory questions ({len(dp.mandatory_questions)}):")
            for q in dp.mandatory_questions:
                print(f"  - {q}")
    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  - {w}")


def _run_list_versions(patient_id: str, root: Path) -> int:
    versions = list_versions(patient_id, root=root)
    if not versions:
        print(f"No saved plans for patient_id={patient_id!r} under {root}/")
        return 0
    print(f"Saved plans for patient_id={patient_id!r}  ({len(versions)} total):")
    print()
    for v in versions:
        chain = ""
        if v["supersedes"]:
            chain += f" ← {v['supersedes']}"
        if v["superseded_by"]:
            chain += f" → {v['superseded_by']}"
        print(f"  [{v['mode']:11s}] v{v['version']}  {v['plan_id']}{chain}")
        print(f"               file: {v['path']}")
    return 0


def _load_previous_result(path_or_id, save_dir: Path = PATIENT_PLANS_ROOT):
    """Reconstruct a PlanResult or DiagnosticPlanResult.

    Accepts either:
    - a Path to a JSON file (CLI --json-output dump or persistence file)
    - a string that is a plan_id (resolved via persistence layer)
    """
    return load_result(path_or_id, root=save_dir)


def _run_revise(
    patient: dict,
    prev_arg,  # str (path or plan_id) — argparse passed Path, but accept string too
    trigger: str,
    kb_root: Path,
    json_output: Path | None,
    mdt: bool,
    save: bool = False,
    save_dir: Path = PATIENT_PLANS_ROOT,
    render_path: Path | None = None,
    actionability_enabled: bool = False,
    actionability_client=None,
) -> int:
    try:
        # `prev_arg` is the value of --revise. If the path doesn't exist as
        # a file, fall back to interpreting it as a plan_id under save_dir.
        if isinstance(prev_arg, Path) and not prev_arg.is_file():
            previous = _load_previous_result(str(prev_arg), save_dir=save_dir)
        else:
            previous = _load_previous_result(prev_arg, save_dir=save_dir)
    except Exception as e:
        print(f"ERROR loading previous plan: {e}", file=sys.stderr)
        return 2

    try:
        revised_prev, new_result = revise_plan(
            patient, previous, trigger, kb_root=kb_root,
            actionability_enabled=actionability_enabled,
            actionability_client=actionability_client,
        )
    except (ValueError, TypeError) as e:
        print(f"ERROR revising plan: {e}", file=sys.stderr)
        return 2

    print("=== Revision summary ===")
    prev_id = (
        previous.diagnostic_plan.id if isinstance(previous, DiagnosticPlanResult)
        and previous.diagnostic_plan
        else (previous.plan.id if isinstance(previous, PlanResult) and previous.plan else "?")
    )
    new_id = (
        new_result.diagnostic_plan.id if isinstance(new_result, DiagnosticPlanResult)
        and new_result.diagnostic_plan
        else (new_result.plan.id if isinstance(new_result, PlanResult) and new_result.plan else "?")
    )
    transition = (
        "diagnostic→treatment" if isinstance(previous, DiagnosticPlanResult)
        and isinstance(new_result, PlanResult)
        else "diagnostic→diagnostic" if isinstance(previous, DiagnosticPlanResult)
        else "treatment→treatment"
    )
    print(f"  Previous: {prev_id}")
    print(f"  New:      {new_id}")
    print(f"  Trigger:  {trigger}")
    print(f"  Transition: {transition}")
    print()

    # Render the new result with existing helpers
    if isinstance(new_result, DiagnosticPlanResult):
        _print_diagnostic_brief(new_result)
    else:
        # Treatment plan — print core summary inline
        if new_result.plan:
            print(f"Plan id:   {new_result.plan.id}  (v{new_result.plan.version})")
            print(f"Supersedes: {new_result.plan.supersedes}")
            print(f"Trigger:    {new_result.plan.revision_trigger}")
            print(f"Tracks ({len(new_result.plan.tracks)}):")
            for t in new_result.plan.tracks:
                _print_track(t)
                print()

    if mdt:
        m = orchestrate_mdt(patient, new_result, kb_root=kb_root)
        _print_mdt_brief(m)

    if json_output:
        payload = {
            "transition": transition,
            "previous_with_superseded_by_set": (
                revised_prev.to_dict()
                if hasattr(revised_prev, "to_dict")
                else None
            ),
            "new_result": (
                new_result.to_dict()
                if hasattr(new_result, "to_dict")
                else None
            ),
        }
        json_output.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        print(f"\nRevision JSON written to {json_output}")

    if save:
        try:
            saved_new = save_result(new_result, root=save_dir)
            print(f"\nNew plan persisted: {saved_new}")
            try:
                updated_prev = update_superseded_by_on_disk(prev_id, new_id, root=save_dir)
                print(f"Previous plan updated in place (superseded_by={new_id}): {updated_prev}")
            except FileNotFoundError:
                print(
                    f"Warning: previous plan {prev_id} not found in {save_dir}/ — "
                    "superseded_by chain is in-memory only on disk side. "
                    "Original was loaded from an explicit file path; persist it via --save first.",
                    file=sys.stderr,
                )
        except (ValueError, OSError) as e:
            print(f"ERROR persisting plan: {e}", file=sys.stderr)
            return 2

    if render_path:
        m_obj = orchestrate_mdt(patient, new_result, kb_root=kb_root) if mdt else None
        html_str = render_revision_note_html(revised_prev, new_result, transition, mdt=m_obj)
        render_path.write_text(html_str, encoding="utf-8")
        print(f"\nRevision note rendered: {render_path}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenOnco rule engine — generate a Plan or DiagnosticPlan.")
    parser.add_argument(
        "patient",
        type=Path,
        nargs="?",
        help="Patient profile JSON (omit when using --list-versions)",
    )
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
    parser.add_argument(
        "--diagnostic",
        action="store_true",
        help="Force diagnostic mode (errors if patient.disease.id present per CHARTER §15.2 C7)",
    )
    parser.add_argument(
        "--revise",
        type=Path,
        help=("Path to a previous plan JSON (output of an earlier --json-output run). "
              "Generates a next-version plan that supersedes it; auto-detects transition."),
    )
    parser.add_argument(
        "--revision-trigger",
        type=str,
        default=None,
        help="Free-text description of what new data triggered this revision (audit hook).",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help=("Persist generated plan under patient_plans/<patient_id>/<plan_id>.json "
              "(gitignored per CHARTER §9.3). With --revise, also updates the previous "
              "file's superseded_by in place."),
    )
    parser.add_argument(
        "--save-dir",
        type=Path,
        default=PATIENT_PLANS_ROOT,
        help=f"Persistence root (default: {PATIENT_PLANS_ROOT}/)",
    )
    parser.add_argument(
        "--list-versions",
        type=str,
        metavar="PATIENT_ID",
        help="List all saved plan versions for a patient_id, then exit.",
    )
    parser.add_argument(
        "--render",
        type=Path,
        metavar="OUT.html",
        help=("Render result to a single-file HTML document (A4 print-friendly). "
              "Works with treatment plan, diagnostic brief, and --revise (revision note)."),
    )
    # Actionability flags. The OncoKB-specific --oncokb-proxy / --oncokb-timeout
    # were removed in Phase 1 of the CIViC pivot (the proxy is gone; see
    # docs/reviews/oncokb-public-civic-coverage-2026-04-27.md). Phase 2 will
    # add `--civic-snapshot PATH` once SnapshotActionabilityClient ships.
    args = parser.parse_args()

    # ── List versions and exit (no patient profile needed) ──────────────
    if args.list_versions:
        return _run_list_versions(args.list_versions, args.save_dir)

    if args.patient is None:
        print("ERROR: patient profile is required (or use --list-versions PATIENT_ID)", file=sys.stderr)
        return 2
    if not args.patient.is_file():
        print(f"ERROR: patient file not found: {args.patient}", file=sys.stderr)
        return 2

    patient = json.loads(args.patient.read_text(encoding="utf-8"))

    # ── Revision mode ────────────────────────────────────────────────────
    if args.revise is not None:
        if not args.revision_trigger:
            print("ERROR: --revise requires --revision-trigger \"...\"", file=sys.stderr)
            return 2
        # TODO(phase-2): wire --civic-snapshot to revise re-query as well.
        # `--revise` accepts either an explicit file path or a plan_id.
        # _run_revise / _load_previous_result handles both; do not pre-check.
        return _run_revise(patient, args.revise, args.revision_trigger, args.kb,
                           json_output=args.json_output, mdt=args.mdt,
                           save=args.save, save_dir=args.save_dir,
                           render_path=args.render,
                           actionability_enabled=False,
                           actionability_client=None)

    # Mode dispatch — see DIAGNOSTIC_MDT_SPEC §6.3
    use_diagnostic = args.diagnostic or (
        is_diagnostic_profile(patient) and not is_treatment_profile(patient)
    )

    if use_diagnostic:
        try:
            diag_result = generate_diagnostic_brief(patient, kb_root=args.kb)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        _print_diagnostic_brief(diag_result)
        mdt = None
        if args.mdt:
            mdt = orchestrate_mdt(patient, diag_result, kb_root=args.kb)
            _print_mdt_brief(mdt)
        if args.json_output:
            payload = diag_result.to_dict()
            if mdt is not None:
                payload["mdt"] = mdt.to_dict()
            args.json_output.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            print(f"\nFull DiagnosticPlan JSON written to {args.json_output}")
        if args.save and diag_result.diagnostic_plan is not None:
            try:
                saved_path = save_result(diag_result, root=args.save_dir)
                print(f"\nDiagnosticPlan persisted: {saved_path}")
            except (ValueError, OSError) as e:
                print(f"ERROR persisting plan: {e}", file=sys.stderr)
                return 2
        if args.render and diag_result.diagnostic_plan is not None:
            html_str = render_diagnostic_brief_html(diag_result, mdt=mdt)
            args.render.write_text(html_str, encoding="utf-8")
            print(f"\nHTML rendered: {args.render}")
        if diag_result.diagnostic_plan is None:
            return 1
        return 0

    # Treatment mode (existing flow). TODO(phase-2): wire --civic-snapshot
    # → SnapshotActionabilityClient when CIViC reader lands.
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

    if args.save and result.plan is not None:
        try:
            saved_path = save_result(result, root=args.save_dir)
            print(f"\nPlan persisted: {saved_path}")
        except (ValueError, OSError) as e:
            print(f"ERROR persisting plan: {e}", file=sys.stderr)
            return 2

    if args.render and result.plan is not None:
        html_str = render_plan_html(result, mdt=mdt)
        args.render.write_text(html_str, encoding="utf-8")
        print(f"\nHTML rendered: {args.render}")

    if not result.default_indication_id:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
