"""Generate verified, end-to-end-routeable patient examples for each
missing (disease + line + plan) signature reported by
scripts/audit_example_plan_coverage.py.

Strategy:
  1. Re-run audit (in-memory) to enumerate missing signatures.
  2. For each missing sig:
       - take the indication YAML; if multiple, pick one with the
         richest `applicable_to`.
       - synthesize a minimal patient profile from
         `applicable_to.biomarker_requirements_required`,
         `applicable_to.demographic_constraints`, and baseline values.
       - run `generate_plan()`.
       - accept iff: `plan.tracks` non-empty,
                     `default_indication_id == target indication`,
                     no `ref error` warnings.
       - on rejection: record skip reason; do not retry / force.
  3. Write accepted patients to `examples/patient_verified_<slug>.json`.
  4. Append a CaseEntry block (between markers) to
     `scripts/site_cases.py` so the build picks them up.
  5. Re-emit the coverage report.

Output:
  examples/patient_verified_<disease>_<line>_<regimen>.json
  scripts/site_cases.py  (auto-block updated in-place)
  docs/example-plan-coverage-report.json|.md  (re-emitted)
  docs/verified-examples-skips.md             (per-skip rationale)

CLI:
  py -3.12 scripts/generate_verified_treatment_examples.py
      --limit 30                     # only accept N this run
      --dry-run                      # generate + verify but don't write
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONTENT_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
IND_DIR = CONTENT_ROOT / "indications"
DISEASE_DIR = CONTENT_ROOT / "diseases"
ALGO_DIR = CONTENT_ROOT / "algorithms"
EXAMPLES_DIR = REPO_ROOT / "examples"
DOCS_DIR = REPO_ROOT / "docs"
SITE_CASES = REPO_ROOT / "scripts" / "site_cases.py"

from knowledge_base.engine import generate_plan  # noqa: E402
from scripts.audit_example_plan_coverage import (  # noqa: E402
    _load_yaml,
    _all_indications,
    _all_algorithms,
    _ind_signature,
    collect_routeable,
    build_coverage_report,
    render_md,
)
from scripts.site_cases import CASES, BROKEN_CASE_IDS, GALLERY_EXCLUDED_CASE_IDS  # noqa: E402


_AUTO_BLOCK_BEGIN = "    # ── VERIFIED TREATMENT EXAMPLES (regen via scripts/generate_verified_treatment_examples.py) ──"
_AUTO_BLOCK_END = "    # ── /VERIFIED TREATMENT EXAMPLES ──"


# ── Slug helpers ────────────────────────────────────────────────────────────


def _slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"^(dis|ind|reg|proc|rad)-", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


# ── Category lookup (mirrors generate_auto_examples.py) ────────────────────


def _category_for(disease_id: str) -> str:
    lymphoblastic = {"DIS-B-ALL", "DIS-T-ALL", "DIS-T-LBL", "DIS-B-LBL"}
    hodgkin = {"DIS-CHL", "DIS-NLPBL"}
    myeloma = {"DIS-MM", "DIS-WM"}
    t_cell = {
        "DIS-PTCL-NOS", "DIS-ALCL", "DIS-AITL", "DIS-MF-SEZARY",
        "DIS-EATL", "DIS-HSTCL", "DIS-NK-T-NASAL", "DIS-ATLL",
        "DIS-T-PLL",
    }
    indolent = {
        "DIS-FL", "DIS-CLL", "DIS-SPLENIC-MZL", "DIS-NODAL-MZL",
        "DIS-HCV-MZL", "DIS-HCL", "DIS-MALT",
    }
    aggressive_bcell = {
        "DIS-DLBCL-NOS", "DIS-BURKITT", "DIS-PMBCL", "DIS-MCL", "DIS-NLPBL",
    }
    myeloid = {
        "DIS-AML", "DIS-APL", "DIS-MDS", "DIS-CML", "DIS-PV", "DIS-ET",
        "DIS-MF", "DIS-MASTOCYTOSIS", "DIS-CMML", "DIS-JMML",
    }
    if disease_id in lymphoblastic:
        return "lymphoblastic"
    if disease_id in hodgkin:
        return "hodgkin"
    if disease_id in myeloma:
        return "myeloma"
    if disease_id in t_cell:
        return "t_cell"
    if disease_id in indolent:
        return "b_indolent"
    if disease_id in aggressive_bcell:
        return "b_aggressive"
    if disease_id in myeloid:
        return "myeloid"
    return "solid"


def _disease_name(disease_id: str) -> str:
    """Return the English display name for a disease."""
    short = disease_id.replace("DIS-", "").lower().replace("-", "_")
    p = DISEASE_DIR / f"dis_{short}.yaml"
    if not p.exists():
        for pp in DISEASE_DIR.glob("*.yaml"):
            d = _load_yaml(pp)
            if d.get("id") == disease_id:
                p = pp
                break
        else:
            return disease_id
    d = _load_yaml(p)
    names = d.get("names") or {}
    return (
        names.get("english")
        or names.get("preferred")
        or names.get("ua")
        or disease_id
    )


# ── Patient synthesis ──────────────────────────────────────────────────────


_PRESENCE_VALUES = {
    "positive", "pos", "present", "detected", "amplified", "high",
    "expressed", "mutated", "mut",
}

_NEGATIVE_VALUES = {
    "negative", "neg", "absent", "wildtype", "wild-type", "wt", "low",
}


def _normalize_required_value(constraint: Any) -> Any:
    """Map a value_constraint to a patient-side value the engine accepts."""
    if constraint is None or constraint == "":
        return "positive"
    if not isinstance(constraint, str):
        return constraint
    lc = constraint.strip().lower()
    # Very common simple buckets
    if lc in _PRESENCE_VALUES or lc.startswith("positive"):
        return "positive"
    if lc in _NEGATIVE_VALUES or lc.startswith("negative"):
        return "negative"
    if "amplif" in lc:
        return "amplified"
    if "fusion" in lc or "rearrang" in lc:
        return "fusion"
    if "msi-h" in lc or "msi high" in lc or "dmmr" in lc:
        return "MSI-H"
    if "her2-low" in lc or "her2 low" in lc:
        return "low"
    if "pathogenic" in lc:
        return "pathogenic"
    if "hrd-positive" in lc or "hrd positive" in lc:
        return "positive"
    if "cps" in lc:
        return "10"  # arbitrary high CPS
    if "ki67" in lc and "≤" in lc:
        return "10"
    if "any value valid" in lc or "etiology gate" in lc:
        return "positive"
    # Default: pass the constraint verbatim — many constraints are
    # short identifiers like "D816V positive" that the engine matches
    # case-insensitively as a substring.
    return constraint


def _demographic_defaults(constraints: dict | None) -> dict:
    base = {"age": 60, "sex": "male", "ecog": 1}
    if not constraints or not isinstance(constraints, dict):
        return base
    if "age_min" in constraints:
        try:
            base["age"] = max(int(constraints["age_min"]) + 5, base["age"])
        except Exception:
            pass
    if "age_max" in constraints:
        try:
            base["age"] = min(int(constraints["age_max"]) - 5, base["age"])
        except Exception:
            pass
    if "ecog_max" in constraints:
        try:
            base["ecog"] = min(int(constraints["ecog_max"]), base["ecog"])
        except Exception:
            pass
    return base


def _findings_defaults(constraints: dict | None) -> dict:
    base = {
        "creatinine_clearance_ml_min": 90,
        "bilirubin_uln_x": 1.0,
        "absolute_neutrophil_count_k_ul": 2.5,
        "platelets_k_ul": 200,
        "hbsag": "negative",
        "anti_hbc_total": "negative",
        "hcv_status": "negative",
        "hiv_status": "negative",
    }
    if constraints and isinstance(constraints, dict):
        for key, target in (
            ("platelet_min", "platelets_k_ul"),
            ("anc_min", "absolute_neutrophil_count_k_ul"),
        ):
            if key in constraints:
                try:
                    raw = int(constraints[key])
                    # Heuristic: some kb fields store /µL (e.g. 50000),
                    # patient findings are in K/µL; bring them in line.
                    val = raw / 1000 if raw > 5000 else raw
                    base[target] = max(val, base[target])
                except Exception:
                    pass
    return base


RF_DIR = CONTENT_ROOT / "redflags"


def _redflag_trigger(rf_id: str) -> dict | None:
    """Load a RedFlag YAML and return its `trigger` block."""
    candidate = RF_DIR / f"{rf_id.lower().replace('-', '_')}.yaml"
    if candidate.exists():
        d = _load_yaml(candidate)
        return d.get("trigger") if isinstance(d, dict) else None
    for p in RF_DIR.glob("*.yaml"):
        d = _load_yaml(p)
        if isinstance(d, dict) and d.get("id") == rf_id:
            return d.get("trigger")
    return None


def _resolve_threshold_finding(name: str, threshold: Any, comparator: str) -> Any:
    """Choose a value that satisfies `findings[name] {comparator} threshold`."""
    try:
        thr = float(threshold)
    except Exception:
        return threshold
    if comparator in (">=", "≥", "gte"):
        return thr
    if comparator in (">", "gt"):
        return thr + 1
    if comparator in ("<=", "≤", "lte"):
        return thr
    if comparator in ("<", "lt"):
        return thr - 1
    return thr


def _collect_clause_facts(clause: Any, _seen_rf: set | None = None) -> dict:
    """Walk a decision-tree clause and harvest concrete patient-side facts
    (findings, biomarker values, red-flag triggers, conditions) we can
    inject into a patient profile so the clause evaluates to True.

    For `red_flag` references the RF's own `trigger` block is resolved
    recursively, so the patient gets findings that fire the RF.
    """
    if _seen_rf is None:
        _seen_rf = set()
    out = {"findings": {}, "biomarkers": {}, "red_flags": [], "conditions": []}

    def merge(o: dict) -> None:
        out["findings"].update(o["findings"])
        out["biomarkers"].update(o["biomarkers"])
        for rf in o["red_flags"]:
            if rf not in out["red_flags"]:
                out["red_flags"].append(rf)
        out["conditions"].extend(o["conditions"])

    def _has_facts(o: dict) -> bool:
        return bool(o["findings"] or o["biomarkers"])

    if isinstance(clause, dict):
        if "all_of" in clause:
            for c in clause["all_of"] or []:
                merge(_collect_clause_facts(c, _seen_rf))
        if "any_of" in clause:
            # Prefer the first sub-clause that yields a concrete patient
            # fact (finding/biomarker). Fall back to any RF, expanding
            # the RF's own trigger so the patient drives the RF to fire.
            satisfied = False
            for c in clause["any_of"] or []:
                facts = _collect_clause_facts(c, _seen_rf)
                if _has_facts(facts) and not satisfied:
                    merge(facts)
                    satisfied = True
                else:
                    out["conditions"].extend(facts["conditions"])
                    # remember the RF ref even if not the first pick
                    for rf in facts["red_flags"]:
                        if rf not in out["red_flags"]:
                            out["red_flags"].append(rf)
            if not satisfied and out["red_flags"]:
                # Take the first RF and import its trigger findings.
                rf_id = out["red_flags"][0]
                if rf_id not in _seen_rf:
                    _seen_rf.add(rf_id)
                    trig = _redflag_trigger(rf_id)
                    if trig:
                        merge(_collect_clause_facts(trig, _seen_rf))
        if "none_of" in clause:
            for c in clause["none_of"] or []:
                facts = _collect_clause_facts(c, _seen_rf)
                out["conditions"].extend(facts["conditions"])
        if "red_flag" in clause:
            rf = clause["red_flag"]
            if isinstance(rf, str):
                if rf not in out["red_flags"]:
                    out["red_flags"].append(rf)
                if rf not in _seen_rf:
                    _seen_rf.add(rf)
                    trig = _redflag_trigger(rf)
                    if trig:
                        merge(_collect_clause_facts(trig, _seen_rf))
        if "red_flags_any_of" in clause and isinstance(clause["red_flags_any_of"], list):
            for rf in clause["red_flags_any_of"]:
                if isinstance(rf, str):
                    if rf not in out["red_flags"]:
                        out["red_flags"].append(rf)
                    if rf not in _seen_rf:
                        _seen_rf.add(rf)
                        trig = _redflag_trigger(rf)
                        if trig:
                            merge(_collect_clause_facts(trig, _seen_rf))
                    break  # any_of → satisfy one
        if "red_flags_all_of" in clause and isinstance(clause["red_flags_all_of"], list):
            for rf in clause["red_flags_all_of"]:
                if isinstance(rf, str):
                    if rf not in out["red_flags"]:
                        out["red_flags"].append(rf)
                    if rf not in _seen_rf:
                        _seen_rf.add(rf)
                        trig = _redflag_trigger(rf)
                        if trig:
                            merge(_collect_clause_facts(trig, _seen_rf))
        if "finding" in clause:
            f = clause["finding"]
            if isinstance(f, str):
                if "threshold" in clause:
                    v = _resolve_threshold_finding(f, clause["threshold"],
                                                   clause.get("comparator", ">="))
                else:
                    v = clause.get("value", True)
                out["findings"][f] = v
        if "biomarker" in clause or "biomarker_id" in clause:
            bid = clause.get("biomarker") or clause.get("biomarker_id")
            if isinstance(bid, str):
                out["biomarkers"][bid] = _normalize_required_value(clause.get("value"))
        if "condition" in clause:
            c = clause.get("condition")
            if isinstance(c, str):
                out["conditions"].append(c)
    return out


def _algo_path_facts(algorithm: dict, target_ind_id: str) -> dict | None:
    """Walk algorithm decision_tree, find a step whose result equals
    target_ind_id, and return facts that drive evaluation to that step.

    Strategy: simple. For each step `s`:
      - if s.if_true.result == target → return facts that make
        s.evaluate True (best-effort).
      - if s.if_false.result == target → don't inject anything from this
        step (False is the absence of positive signals).

    Returns None if target is unreachable from the decision tree (no step
    references it via `result`).
    """
    if not isinstance(algorithm, dict):
        return None
    if algorithm.get("default_indication") == target_ind_id:
        return {"findings": {}, "biomarkers": {}, "red_flags": [], "conditions": []}

    for step in algorithm.get("decision_tree") or []:
        if not isinstance(step, dict):
            continue
        for branch_key in ("if_true", "if_false"):
            branch = step.get(branch_key) or {}
            if not isinstance(branch, dict):
                continue
            if branch.get("result") == target_ind_id:
                if branch_key == "if_true":
                    return _collect_clause_facts(step.get("evaluate") or {})
                return {"findings": {}, "biomarkers": {}, "red_flags": [],
                        "conditions": ["target on if_false branch — absence of positive signals"]}
    return None


def _find_algorithm_for(disease_id: str, line: int) -> dict | None:
    for p in ALGO_DIR.glob("*.yaml"):
        d = _load_yaml(p)
        if (
            d.get("applicable_to_disease") == disease_id
            and d.get("applicable_to_line_of_therapy") == line
            and d.get("applicable_to_disease_state") is None
        ):
            return d
    # Fallback: any state
    for p in ALGO_DIR.glob("*.yaml"):
        d = _load_yaml(p)
        if (
            d.get("applicable_to_disease") == disease_id
            and d.get("applicable_to_line_of_therapy") == line
        ):
            return d
    return None


def _build_patient(disease_id: str, line: int, ind: dict, target_ind_id: str) -> dict:
    appl = ind.get("applicable_to") or {}
    demographics = _demographic_defaults(appl.get("demographic_constraints"))
    findings = _findings_defaults(appl.get("demographic_constraints"))

    biomarkers: dict[str, Any] = {}
    for r in appl.get("biomarker_requirements_required") or []:
        if not isinstance(r, dict):
            continue
        bid = r.get("biomarker_id")
        if not bid:
            continue
        biomarkers[bid] = _normalize_required_value(r.get("value_constraint"))

    # Algorithm-aware step facts to route the patient to the target.
    algo = _find_algorithm_for(disease_id, line)
    if algo is not None:
        facts = _algo_path_facts(algo, target_ind_id)
        if facts:
            findings.update(facts["findings"])
            biomarkers.update(facts["biomarkers"])

    short = disease_id.replace("DIS-", "")
    patient = {
        "patient_id": f"VERIFIED-{short}-L{line}-{_slug(target_ind_id)[:30].upper()}",
        "_target_indication_id": target_ind_id,
        "_verified_example": True,
        "disease": {"id": disease_id},
        "line_of_therapy": line,
        "biomarkers": biomarkers,
        "demographics": demographics,
        "findings": findings,
    }
    # Mirror common stage flag for solid tumours so the algorithm
    # doesn't strand on a free-text stage clause it can't read. Adding
    # this is harmless: the engine's clause evaluator only looks at
    # findings/biomarkers keys it knows.
    stage = (appl.get("stage_requirements") or [])
    if stage:
        patient["findings"]["stage_requirements_present"] = True
    return patient


# ── Verification ────────────────────────────────────────────────────────────


def _run(patient: dict, target_ind_id: str) -> tuple[bool, dict]:
    result = generate_plan(patient, kb_root=CONTENT_ROOT)
    tracks = []
    if result.plan and result.plan.tracks:
        for t in result.plan.tracks:
            tracks.append({
                "track_id": t.track_id,
                "indication_id": t.indication_id,
                "is_default": t.is_default,
            })
    info = {
        "patient_id": patient.get("patient_id"),
        "disease_id": result.disease_id,
        "algorithm_id": result.algorithm_id,
        "default_indication_id": result.default_indication_id,
        "alternative_indication_id": result.alternative_indication_id,
        "tracks": tracks,
        "warnings": list(result.warnings or []),
    }
    if not tracks:
        info["reject_reason"] = "no_tracks"
        return False, info
    if result.default_indication_id != target_ind_id:
        info["reject_reason"] = (
            f"default_indication_mismatch: got {result.default_indication_id}, "
            f"expected {target_ind_id}"
        )
        return False, info
    for w in info["warnings"]:
        if "ref error" in w:
            info["reject_reason"] = f"ref_error: {w}"
            return False, info
    return True, info


# ── site_cases.py block writer ──────────────────────────────────────────────


def _render_case_entry(case_id: str, file_name: str, *, disease_id: str,
                        line: int, regimen_id: str, target_ind_id: str,
                        category: str, disease_name: str) -> str:
    disease_short = disease_id.replace("DIS-", "")
    reg_short = regimen_id.replace("REG-", "")
    label_en = f"{disease_short} · L{line} · {reg_short}"
    label_ua = f"{disease_short} · {line}L · {reg_short}"
    summary_en = (
        f"Verified end-to-end example for {disease_name[:80]} — "
        f"line {line}, regimen {reg_short}. Auto-synthesised from "
        f"{target_ind_id}; engine routes to it as the default plan."
    )
    summary_ua = (
        f"Перевірений end-to-end приклад для {disease_name[:80]} — "
        f"лінія {line}, режим {reg_short}. Автоматично згенеровано "
        f"з {target_ind_id}; engine обирає його як план за замовчуванням."
    )
    return f"""    CaseEntry(
        case_id="{case_id}",
        file="{file_name}",
        label_ua="{label_ua}",
        summary_ua="{summary_ua}",
        badge="Treatment Plan", badge_class="bdg-plan", category="{category}",
        label_en="{label_en}",
        summary_en="{summary_en}",
    ),"""


def _patch_site_cases(entries: list[str]) -> None:
    text = SITE_CASES.read_text(encoding="utf-8")
    auto_block = _AUTO_BLOCK_BEGIN + "\n" + "\n".join(entries) + "\n" + _AUTO_BLOCK_END
    if _AUTO_BLOCK_BEGIN in text and _AUTO_BLOCK_END in text:
        start = text.index(_AUTO_BLOCK_BEGIN)
        end = text.index(_AUTO_BLOCK_END) + len(_AUTO_BLOCK_END)
        new = text[:start] + auto_block + text[end:]
    else:
        marker = "\n]\n"
        last_close = text.rfind(marker)
        if last_close < 0:
            print("ERROR: could not locate CASES closing bracket", file=sys.stderr)
            return
        new = text[:last_close] + "\n" + auto_block + "\n" + text[last_close:]
    SITE_CASES.write_text(new, encoding="utf-8")


# ── Main ────────────────────────────────────────────────────────────────────


def _pick_indication_for_signature(sig, indications: dict[str, dict]) -> str | None:
    """Pick a target indication for a (disease, line, regimen) signature.
    Prefer the one whose applicable_to has the richest biomarker info.
    """
    candidates: list[tuple[int, str]] = []
    for ind_id, ind in indications.items():
        s = _ind_signature(ind)
        if s != sig:
            continue
        appl = ind.get("applicable_to") or {}
        reqs = appl.get("biomarker_requirements_required") or []
        score = len(reqs)
        candidates.append((score, ind_id))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Max accepted examples per run; default unlimited.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate + verify but do not write JSON files.")
    parser.add_argument("--skip-patch", action="store_true",
                        help="Do not patch scripts/site_cases.py")
    parser.add_argument("--include-extended", action="store_true",
                        help="Also try indication-only signatures (no algorithm route).")
    args = parser.parse_args(argv)

    report = build_coverage_report()
    routeable = collect_routeable()
    indications: dict[str, dict] = routeable["indications"]
    # Use the missing list straight from the audit.
    pool = report["missing_via_algorithm"][:]
    if args.include_extended:
        seen = {(r["disease_id"], r["line_of_therapy"], r["regimen_id"]) for r in pool}
        for r in report["missing_extended"]:
            sig = (r["disease_id"], r["line_of_therapy"], r["regimen_id"])
            if sig not in seen:
                pool.append(r)

    print(f"Pool of missing signatures to try: {len(pool)}")

    accepted: list[dict] = []
    skipped: list[dict] = []
    written_files: list[str] = []

    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    seen_case_ids: set[str] = {c.case_id for c in CASES}

    for rec in pool:
        if args.limit is not None and len(accepted) >= args.limit:
            break
        sig = (rec["disease_id"], rec["line_of_therapy"], rec["regimen_id"])
        target_ind = _pick_indication_for_signature(sig, indications)
        if target_ind is None:
            skipped.append({**rec, "reject_reason": "no indication for signature"})
            continue
        ind = indications[target_ind]
        patient = _build_patient(sig[0], sig[1], ind, target_ind)
        ok, info = _run(patient, target_ind)
        if not ok:
            skipped.append({**rec, "target_indication_id": target_ind, **info})
            continue

        # File name and case id
        d_slug = _slug(sig[0])
        r_slug = _slug(sig[2])
        file_name = f"patient_verified_{d_slug}_l{sig[1]}_{r_slug}.json"
        case_id = f"verified-{d_slug.replace('_','-')}-l{sig[1]}-{r_slug.replace('_','-')}"
        # Truncate to keep ids/path lengths reasonable
        case_id = case_id[:120]
        if case_id in seen_case_ids:
            skipped.append({**rec, "target_indication_id": target_ind,
                            "reject_reason": f"case_id collision: {case_id}"})
            continue
        seen_case_ids.add(case_id)

        if not args.dry_run:
            (EXAMPLES_DIR / file_name).write_text(
                json.dumps(patient, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        accepted.append({
            "case_id": case_id,
            "file": file_name,
            "disease_id": sig[0],
            "line_of_therapy": sig[1],
            "regimen_id": sig[2],
            "target_indication_id": target_ind,
            **info,
        })
        written_files.append(file_name)

    # Build CaseEntry block for accepted ones
    if accepted and not args.dry_run and not args.skip_patch:
        entries = []
        for a in accepted:
            entries.append(_render_case_entry(
                case_id=a["case_id"],
                file_name=a["file"],
                disease_id=a["disease_id"],
                line=a["line_of_therapy"],
                regimen_id=a["regimen_id"],
                target_ind_id=a["target_indication_id"],
                category=_category_for(a["disease_id"]),
                disease_name=_disease_name(a["disease_id"]),
            ))
        # Preserve existing verified block (we re-render the union).
        existing = _existing_verified_entries()
        kept = [e for e in existing if e["case_id"] not in {a["case_id"] for a in accepted}]
        # Render kept first, then new ones, sorted by case_id for stability.
        all_block = kept + [{"case_id": a["case_id"], "rendered": e}
                            for a, e in zip(accepted, entries)]
        all_block.sort(key=lambda r: r["case_id"])
        rendered_list = [r["rendered"] for r in all_block]
        _patch_site_cases(rendered_list)

    skips_path = DOCS_DIR / "verified-examples-skips.md"
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Verified examples — skipped signatures", ""]
    for s in skipped:
        lines.append(
            f"- {s['disease_id']} · L{s['line_of_therapy']} · "
            f"{s['regimen_id']} → {s.get('reject_reason', 'unknown')}"
        )
    skips_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Accepted: {len(accepted)}    Skipped: {len(skipped)}")
    if accepted[:3]:
        for a in accepted[:3]:
            print(f"  + {a['file']}  ({a['target_indication_id']})")
    return 0


def _existing_verified_entries() -> list[dict]:
    """Read existing verified-block CaseEntries from site_cases.py so we
    keep them when re-rendering the block. Returns list of
    {case_id, rendered}."""
    text = SITE_CASES.read_text(encoding="utf-8")
    if _AUTO_BLOCK_BEGIN not in text or _AUTO_BLOCK_END not in text:
        return []
    start = text.index(_AUTO_BLOCK_BEGIN) + len(_AUTO_BLOCK_BEGIN)
    end = text.index(_AUTO_BLOCK_END)
    block = text[start:end]
    out: list[dict] = []
    # Split per CaseEntry — assume each starts with "    CaseEntry(" on its own line.
    chunks = re.split(r"(?=^    CaseEntry\()", block, flags=re.MULTILINE)
    for chunk in chunks:
        m = re.search(r'case_id="([^"]+)"', chunk)
        if not m:
            continue
        out.append({"case_id": m.group(1), "rendered": chunk.rstrip()})
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
