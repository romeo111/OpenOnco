#!/usr/bin/env python3
"""
evaluate.py — Quality Scoring Harness for Cancer Research Reports

The "val_bpb" of the autoresearch loop. Takes a generated JSON report
and produces a single 0-100 quality score across 7 dimensions.

Reuses cancer_research_scorer.py's validate_report() for structural checks.

Usage:
    python evaluate.py report.json
    python evaluate.py report.json --verbose
    python evaluate.py report.json --json-output scores.json
"""

import json
import sys
import argparse
import re
from datetime import datetime

# Import structural validation from existing scorer
from cancer_research_scorer import validate_report, compute_composite, RATING_FACTORS


# ── Dimension Definitions ────────────────────────────────────────────────────
# Each dimension has a max score and an evaluation function.
# Total max = 100.

DIMENSIONS = {
    "structural_integrity": {"max": 15, "description": "JSON validates, all sections present, minimum counts"},
    "evidence_depth": {"max": 25, "description": "OS/PFS/ORR/HR/sample-size data density across treatments"},
    "tier_coverage": {"max": 10, "description": "All 6 research tiers represented in treatments"},
    "rating_calibration": {"max": 15, "description": "Score spread, range, rationale completeness"},
    "source_quality": {"max": 15, "description": "URL count, validity, type diversity"},
    "clinical_relevance": {"max": 10, "description": "Biomarker specificity, side effects, trial status details"},
    "combo_supportive_coverage": {"max": 10, "description": "Combination strategies + supportive care depth"},
}


def score_structural_integrity(data: dict) -> tuple:
    """Score: 15 pts max. JSON validity, sections present, min treatment count."""
    score = 0
    details = []

    # Reuse existing validator (0-3 pts for clean validation)
    warnings = validate_report(data)
    if not warnings:
        score += 3
        details.append("+3: Clean validation (no warnings)")
    elif len(warnings) <= 2:
        score += 2
        details.append(f"+2: Minor validation issues ({len(warnings)} warnings)")
    elif len(warnings) <= 5:
        score += 1
        details.append(f"+1: Some validation issues ({len(warnings)} warnings)")
    else:
        details.append(f"+0: Many validation issues ({len(warnings)} warnings)")

    # report_metadata present and complete (0-2 pts)
    meta = data.get("report_metadata", {})
    meta_fields = ["cancer_type", "generated_date", "stage", "molecular_profile"]
    meta_present = sum(1 for f in meta_fields if meta.get(f))
    if meta_present >= 4:
        score += 2
        details.append("+2: All metadata fields present")
    elif meta_present >= 2:
        score += 1
        details.append(f"+1: {meta_present}/4 metadata fields present")
    else:
        details.append(f"+0: Only {meta_present}/4 metadata fields")

    # Treatment count (0-4 pts)
    treatments = data.get("treatments", [])
    n_treatments = len(treatments)
    if n_treatments >= 10:
        score += 4
        details.append(f"+4: {n_treatments} treatments (≥10)")
    elif n_treatments >= 7:
        score += 3
        details.append(f"+3: {n_treatments} treatments (7-9)")
    elif n_treatments >= 4:
        score += 2
        details.append(f"+2: {n_treatments} treatments (4-6)")
    elif n_treatments >= 1:
        score += 1
        details.append(f"+1: {n_treatments} treatments (1-3)")
    else:
        details.append("+0: No treatments found")

    # Section presence (0-3 pts): clinical_trials, combination_strategies, supportive_care
    sections = ["clinical_trials", "combination_strategies", "supportive_care"]
    sections_present = sum(1 for s in sections if data.get(s) and len(data[s]) > 0)
    score += sections_present
    details.append(f"+{sections_present}: {sections_present}/3 optional sections present")

    # Sources section (0-3 pts)
    sources = data.get("sources", [])
    if len(sources) >= 10:
        score += 3
        details.append(f"+3: {len(sources)} sources (≥10)")
    elif len(sources) >= 5:
        score += 2
        details.append(f"+2: {len(sources)} sources (5-9)")
    elif len(sources) >= 1:
        score += 1
        details.append(f"+1: {len(sources)} sources (1-4)")
    else:
        details.append("+0: No sources")

    return min(score, 15), details


def score_evidence_depth(data: dict) -> tuple:
    """Score: 25 pts max. Density of OS/PFS/ORR/HR/sample-size data."""
    score = 0
    details = []
    treatments = data.get("treatments", [])

    if not treatments:
        return 0, ["No treatments to evaluate"]

    total_evidence_points = 0
    treatments_with_evidence = 0

    for t in treatments:
        ev = t.get("key_evidence", {})
        t_points = 0

        # OS data (0-3 pts per treatment — magnitude-weighted)
        os_data = ev.get("os_months", {})
        if isinstance(os_data, dict):
            os_trt = os_data.get("treatment") or 0
            os_ctl = os_data.get("control") or 0
            if os_trt and os_ctl:
                delta = float(os_trt) - float(os_ctl)
                if delta >= 6.0:
                    t_points += 3  # meaningful survival gain: both arms + large delta
                elif delta >= 1.0:
                    t_points += 2  # both arms present, modest delta
                else:
                    t_points += 1  # both arms but negligible/negative delta
            elif os_trt:
                t_points += 1  # single-arm OS only

        # PFS data (0-1 pt)
        pfs_data = ev.get("pfs_months", {})
        if isinstance(pfs_data, dict) and pfs_data.get("treatment"):
            t_points += 1

        # ORR data (0-1 pt)
        orr_data = ev.get("orr_percent", {})
        if isinstance(orr_data, dict) and orr_data.get("treatment"):
            t_points += 1

        # HR / p-value (0-1 pt)
        if isinstance(os_data, dict):
            if os_data.get("hazard_ratio") and os_data.get("p_value"):
                t_points += 1

        # Sample size (0-1 pt)
        if ev.get("sample_size") and ev["sample_size"] > 0:
            t_points += 1

        # Study name / journal (0-1 pt)
        if ev.get("study_name") and ev.get("journal"):
            t_points += 1

        if t_points > 0:
            treatments_with_evidence += 1
        total_evidence_points += t_points

    # Normalize: max 9 points per treatment (OS now 0-3), scale to 25
    max_possible = len(treatments) * 9
    if max_possible > 0:
        ratio = total_evidence_points / max_possible
        score = round(ratio * 20)  # Up to 20 pts for data density

    # Bonus: breadth (up to 5 pts)
    if treatments_with_evidence == len(treatments) and len(treatments) >= 5:
        score += 5
        details.append(f"+5: All {treatments_with_evidence} treatments have evidence data")
    elif treatments_with_evidence >= len(treatments) * 0.75:
        score += 3
        details.append(f"+3: {treatments_with_evidence}/{len(treatments)} treatments have evidence")
    elif treatments_with_evidence >= len(treatments) * 0.5:
        score += 2
        details.append(f"+2: {treatments_with_evidence}/{len(treatments)} treatments have evidence")
    elif treatments_with_evidence > 0:
        score += 1
        details.append(f"+1: Only {treatments_with_evidence}/{len(treatments)} have evidence")

    details.insert(0, f"Evidence density: {total_evidence_points}/{max_possible} data points across {len(treatments)} treatments")

    return min(score, 25), details


def score_tier_coverage(data: dict) -> tuple:
    """Score: 10 pts max. Check if all 6 research tiers are represented."""
    treatments = data.get("treatments", [])
    categories_found = set()

    # Map treatment categories to tiers
    tier_map = {
        "standard of care": "tier1",
        "soc": "tier1",
        "first-line": "tier1",
        "first line": "tier1",
        "approved targeted": "tier2",
        "targeted therapy": "tier2",
        "immunotherapy": "tier2",
        "checkpoint inhibitor": "tier2",
        "clinical trial": "tier3",
        "phase 2": "tier3",
        "phase 3": "tier3",
        "experimental": "tier4",
        "preclinical": "tier4",
        "emerging": "tier4",
        "phase 1": "tier4",
        "novel": "tier4",
        "combination": "tier5",
        "combo": "tier5",
        "supportive": "tier6",
        "adjunctive": "tier6",
        "palliative": "tier6",
    }

    for t in treatments:
        cat = (t.get("category", "") or "").lower()
        avail = (t.get("availability", "") or "").lower()
        combined = cat + " " + avail

        for keyword, tier in tier_map.items():
            if keyword in combined:
                categories_found.add(tier)

    # Also check top-level sections for tiers 5 and 6
    if data.get("combination_strategies") and len(data["combination_strategies"]) > 0:
        categories_found.add("tier5")
    if data.get("supportive_care") and len(data["supportive_care"]) > 0:
        categories_found.add("tier6")
    if data.get("clinical_trials") and len(data["clinical_trials"]) > 0:
        categories_found.add("tier3")

    n_tiers = len(categories_found)
    details = []

    if n_tiers >= 6:
        score = 10
        details.append(f"+10: All 6 tiers covered")
    elif n_tiers >= 5:
        score = 8
        details.append(f"+8: {n_tiers}/6 tiers covered")
    elif n_tiers >= 4:
        score = 6
        details.append(f"+6: {n_tiers}/6 tiers covered")
    elif n_tiers >= 3:
        score = 4
        details.append(f"+4: {n_tiers}/6 tiers covered")
    elif n_tiers >= 2:
        score = 2
        details.append(f"+2: {n_tiers}/6 tiers covered")
    else:
        score = 0
        details.append(f"+0: Only {n_tiers}/6 tiers covered")

    missing = {"tier1", "tier2", "tier3", "tier4", "tier5", "tier6"} - categories_found
    tier_names = {
        "tier1": "SoC", "tier2": "Targeted/Immuno", "tier3": "Clinical Trials",
        "tier4": "Experimental", "tier5": "Combinations", "tier6": "Supportive"
    }
    if missing:
        details.append(f"Missing: {', '.join(tier_names.get(t, t) for t in sorted(missing))}")

    return score, details


def score_rating_calibration(data: dict) -> tuple:
    """Score: 15 pts max. Score spread, range, rationale completeness."""
    score = 0
    details = []
    treatments = data.get("treatments", [])

    if not treatments:
        return 0, ["No treatments to evaluate"]

    composites = [t.get("composite_rating", 0) for t in treatments]
    composites = [c for c in composites if c > 0]

    if not composites:
        return 0, ["No composite ratings found"]

    # Rating consistency (0-5 pts): do evidence_level scores match study phases?
    # Rewards accurate calibration, not artificial spread.
    consistency_pts = 0
    consistency_checks = 0
    for t in treatments:
        rb = t.get("rating_breakdown", {})
        ev = t.get("key_evidence", {})
        el_score = rb.get("evidence_level", {}).get("score", 0) if isinstance(rb.get("evidence_level"), dict) else 0
        study = (ev.get("study_name", "") or "").lower()
        n = ev.get("sample_size", 0) or 0

        if not el_score:
            continue
        consistency_checks += 1

        # Phase 3 / large RCT → evidence_level should be 8-10
        if any(k in study for k in ["phase 3", "phase iii", "rct", "randomized"]) or n >= 300:
            if el_score >= 8:
                consistency_pts += 1
        # Phase 2 → evidence_level should be 5-7
        elif any(k in study for k in ["phase 2", "phase ii"]) or (0 < n < 200):
            if 5 <= el_score <= 7:
                consistency_pts += 1
        # Phase 1 / small → evidence_level should be ≤5
        elif any(k in study for k in ["phase 1", "phase i"]) or (0 < n < 50):
            if el_score <= 5:
                consistency_pts += 1
        else:
            consistency_pts += 1  # can't determine phase — no penalty

    if consistency_checks > 0:
        ratio = consistency_pts / consistency_checks
        pts = round(ratio * 5)
        score += pts
        details.append(f"+{pts}: Rating consistency ({consistency_pts}/{consistency_checks} treatments correctly calibrated)")
    else:
        details.append("+0: Could not assess rating consistency (no phase data)")

    # Max score reasonableness (0-3 pts): top score should be realistic
    max_score = max(composites)
    if 6.0 <= max_score <= 9.5:
        score += 3
        details.append(f"+3: Top score realistic ({max_score:.1f})")
    elif 5.0 <= max_score <= 9.8:
        score += 2
        details.append(f"+2: Top score acceptable ({max_score:.1f})")
    else:
        details.append(f"+0: Top score questionable ({max_score:.1f})")

    # Rationale completeness (0-5 pts): all factors have rationale text
    total_factors = 0
    factors_with_rationale = 0
    for t in treatments:
        rb = t.get("rating_breakdown", {})
        for factor in RATING_FACTORS:
            if factor in rb:
                total_factors += 1
                rationale = rb[factor].get("rationale", "")
                if rationale and len(str(rationale)) >= 10:
                    factors_with_rationale += 1

    if total_factors > 0:
        ratio = factors_with_rationale / total_factors
        if ratio >= 0.95:
            score += 5
            details.append(f"+5: {factors_with_rationale}/{total_factors} factors have rationale")
        elif ratio >= 0.80:
            score += 4
            details.append(f"+4: {factors_with_rationale}/{total_factors} have rationale")
        elif ratio >= 0.60:
            score += 3
            details.append(f"+3: {factors_with_rationale}/{total_factors} have rationale")
        elif ratio >= 0.40:
            score += 2
            details.append(f"+2: {factors_with_rationale}/{total_factors} have rationale")
        else:
            score += 1
            details.append(f"+1: Only {factors_with_rationale}/{total_factors} have rationale")

    # Correct sorting (0-2 pts)
    is_sorted = all(composites[i] >= composites[i+1] for i in range(len(composites)-1))
    if is_sorted:
        score += 2
        details.append("+2: Treatments correctly sorted by rating")
    else:
        details.append("+0: Treatments NOT sorted by rating")

    return min(score, 15), details


def score_source_quality(data: dict) -> tuple:
    """Score: 15 pts max. URL count, validity patterns, type diversity."""
    score = 0
    details = []

    sources = data.get("sources", [])
    n_sources = len(sources)

    # Source count (0-5 pts)
    if n_sources >= 20:
        score += 5
        details.append(f"+5: {n_sources} sources (≥20)")
    elif n_sources >= 15:
        score += 4
        details.append(f"+4: {n_sources} sources (15-19)")
    elif n_sources >= 10:
        score += 3
        details.append(f"+3: {n_sources} sources (10-14)")
    elif n_sources >= 5:
        score += 2
        details.append(f"+2: {n_sources} sources (5-9)")
    elif n_sources >= 1:
        score += 1
        details.append(f"+1: {n_sources} sources (1-4)")
    else:
        details.append("+0: No sources")

    # URL presence (0-4 pts)
    urls = [s.get("url", "") for s in sources if s.get("url")]
    valid_urls = [u for u in urls if u.startswith("http")]
    if urls:
        ratio = len(valid_urls) / len(urls)
        pts = round(ratio * 4)
        score += pts
        details.append(f"+{pts}: {len(valid_urls)}/{len(urls)} valid URLs")
    else:
        details.append("+0: No URLs found in sources")

    # Source type diversity (0-3 pts)
    types_found = set()
    for s in sources:
        stype = (s.get("type", "") or "").lower()
        if stype:
            types_found.add(stype)

    # Also infer types from URLs
    for u in valid_urls:
        u_lower = u.lower()
        if "clinicaltrials.gov" in u_lower:
            types_found.add("clinical_trial")
        elif "pubmed" in u_lower or "ncbi" in u_lower:
            types_found.add("journal")
        elif "fda.gov" in u_lower:
            types_found.add("regulatory")
        elif "nccn" in u_lower or "esmo" in u_lower:
            types_found.add("guideline")
        elif "asco" in u_lower or "aacr" in u_lower:
            types_found.add("conference")

    if len(types_found) >= 4:
        score += 3
        details.append(f"+3: {len(types_found)} source types ({', '.join(sorted(types_found))})")
    elif len(types_found) >= 2:
        score += 2
        details.append(f"+2: {len(types_found)} source types")
    elif len(types_found) >= 1:
        score += 1
        details.append(f"+1: {len(types_found)} source type")
    else:
        details.append("+0: No source type diversity")

    # Treatment-level source URLs (0-3 pts)
    treatments = data.get("treatments", [])
    treatments_with_urls = sum(1 for t in treatments
                               if t.get("source_urls") and len(t["source_urls"]) > 0)
    if treatments and treatments_with_urls == len(treatments):
        score += 3
        details.append(f"+3: All {len(treatments)} treatments have source URLs")
    elif treatments and treatments_with_urls >= len(treatments) * 0.7:
        score += 2
        details.append(f"+2: {treatments_with_urls}/{len(treatments)} treatments have URLs")
    elif treatments_with_urls > 0:
        score += 1
        details.append(f"+1: Only {treatments_with_urls}/{len(treatments)} have URLs")
    else:
        details.append("+0: No treatment-level URLs")

    return min(score, 15), details


def score_clinical_relevance(data: dict) -> tuple:
    """Score: 10 pts max. Biomarker specificity, side effects, trial details."""
    score = 0
    details = []
    treatments = data.get("treatments", [])

    if not treatments:
        return 0, ["No treatments to evaluate"]

    # Biomarker requirements specified (0-3 pts)
    treatments_with_markers = sum(
        1 for t in treatments
        if t.get("biomarker_requirements") and len(t["biomarker_requirements"]) > 0
    )
    if treatments_with_markers >= len(treatments) * 0.5:
        score += 3
        details.append(f"+3: {treatments_with_markers}/{len(treatments)} have biomarker reqs")
    elif treatments_with_markers >= len(treatments) * 0.25:
        score += 2
        details.append(f"+2: {treatments_with_markers}/{len(treatments)} have biomarker reqs")
    elif treatments_with_markers > 0:
        score += 1
        details.append(f"+1: {treatments_with_markers}/{len(treatments)} have biomarker reqs")
    else:
        details.append("+0: No biomarker requirements specified")

    # Side effects documented (0-3 pts)
    treatments_with_sides = sum(
        1 for t in treatments
        if t.get("notable_side_effects") and len(t["notable_side_effects"]) > 0
    )
    if treatments_with_sides >= len(treatments) * 0.7:
        score += 3
        details.append(f"+3: {treatments_with_sides}/{len(treatments)} have side effects listed")
    elif treatments_with_sides >= len(treatments) * 0.4:
        score += 2
        details.append(f"+2: {treatments_with_sides}/{len(treatments)} have side effects")
    elif treatments_with_sides > 0:
        score += 1
        details.append(f"+1: {treatments_with_sides}/{len(treatments)} have side effects")
    else:
        details.append("+0: No side effects documented")

    # Clinical trial details (0-2 pts)
    trials = data.get("clinical_trials", [])
    if trials:
        trials_with_ids = sum(1 for tr in trials if tr.get("trial_id"))
        if trials_with_ids >= 3:
            score += 2
            details.append(f"+2: {trials_with_ids} trials with IDs")
        elif trials_with_ids >= 1:
            score += 1
            details.append(f"+1: {trials_with_ids} trials with IDs")
        else:
            details.append("+0: Trials lack IDs")
    else:
        details.append("+0: No clinical trials section")

    # Availability/status specificity (0-1 pt — reduced to make room for intent)
    treatments_with_avail = sum(
        1 for t in treatments
        if t.get("availability") and len(str(t["availability"])) > 3
    )
    if treatments_with_avail >= len(treatments) * 0.8:
        score += 1
        details.append(f"+1: {treatments_with_avail}/{len(treatments)} have availability info")
    else:
        details.append(f"+0: Availability info sparse ({treatments_with_avail}/{len(treatments)})")

    # Treatment intent field present (0-2 pts)
    _valid_intents = {"curative", "adjuvant", "neoadjuvant", "palliative",
                      "salvage", "maintenance", "preventive"}
    treatments_with_intent = sum(
        1 for t in treatments
        if str(t.get("intent", "")).lower() in _valid_intents
    )
    if treatments_with_intent >= len(treatments) * 0.8:
        score += 2
        details.append(f"+2: {treatments_with_intent}/{len(treatments)} treatments have intent field")
    elif treatments_with_intent >= len(treatments) * 0.4:
        score += 1
        details.append(f"+1: {treatments_with_intent}/{len(treatments)} have intent field")
    else:
        details.append(f"+0: Intent field missing ({treatments_with_intent}/{len(treatments)})")

    return min(score, 10), details


def score_combo_supportive_coverage(data: dict) -> tuple:
    """Score: 10 pts max. Combination strategies + supportive care depth."""
    score = 0
    details = []

    # Combination strategies (0-5 pts)
    combos = data.get("combination_strategies", [])
    if len(combos) >= 5:
        score += 4
        details.append(f"+4: {len(combos)} combination strategies (≥5)")
    elif len(combos) >= 3:
        score += 3
        details.append(f"+3: {len(combos)} combination strategies (3-4)")
    elif len(combos) >= 1:
        score += 2
        details.append(f"+2: {len(combos)} combination strategy")
    else:
        details.append("+0: No combination strategies")

    # Combo detail quality
    if combos:
        combos_with_evidence = sum(
            1 for c in combos
            if c.get("evidence_level") and c.get("rationale") and len(str(c["rationale"])) > 10
        )
        if combos_with_evidence == len(combos):
            score += 1
            details.append("+1: All combos have evidence + rationale")

    # Supportive care (0-5 pts)
    supportive = data.get("supportive_care", [])
    if len(supportive) >= 5:
        score += 4
        details.append(f"+4: {len(supportive)} supportive care approaches (≥5)")
    elif len(supportive) >= 3:
        score += 3
        details.append(f"+3: {len(supportive)} supportive care approaches (3-4)")
    elif len(supportive) >= 1:
        score += 2
        details.append(f"+2: {len(supportive)} supportive care approach")
    else:
        details.append("+0: No supportive care")

    # Supportive detail quality
    if supportive:
        supp_with_evidence = sum(
            1 for s in supportive
            if s.get("evidence") and s.get("benefit") and len(str(s["evidence"])) > 10
        )
        if supp_with_evidence == len(supportive):
            score += 1
            details.append("+1: All supportive care has evidence + benefit")

    return min(score, 10), details


# ── Dimension Registry ───────────────────────────────────────────────────────

SCORERS = {
    "structural_integrity": score_structural_integrity,
    "evidence_depth": score_evidence_depth,
    "tier_coverage": score_tier_coverage,
    "rating_calibration": score_rating_calibration,
    "source_quality": score_source_quality,
    "clinical_relevance": score_clinical_relevance,
    "combo_supportive_coverage": score_combo_supportive_coverage,
}


def evaluate_report(data: dict, verbose: bool = False) -> dict:
    """Run all dimension scorers. Returns scoring result dict."""
    results = {}
    total_score = 0

    for dim_name, scorer_fn in SCORERS.items():
        dim_score, dim_details = scorer_fn(data)
        dim_max = DIMENSIONS[dim_name]["max"]
        results[dim_name] = {
            "score": dim_score,
            "max": dim_max,
            "pct": round(dim_score / dim_max * 100, 1) if dim_max > 0 else 0,
            "details": dim_details,
        }
        total_score += dim_score

    return {
        "quality_score": total_score,
        "max_possible": 100,
        "dimensions": results,
        "evaluated_at": datetime.now().isoformat(),
    }


def print_evaluation(result: dict, verbose: bool = False):
    """Print human-readable evaluation output."""
    qs = result["quality_score"]
    print(f"\n{'='*60}")
    print(f"  QUALITY SCORE: {qs}/100")
    print(f"{'='*60}")

    # Grade
    if qs >= 85:
        grade = "A — Excellent"
    elif qs >= 70:
        grade = "B — Good"
    elif qs >= 55:
        grade = "C — Adequate"
    elif qs >= 40:
        grade = "D — Below Average"
    else:
        grade = "F — Poor"
    print(f"  Grade: {grade}\n")

    dims = result["dimensions"]
    print(f"  {'Dimension':<30} {'Score':>6}  {'Max':>4}  {'%':>5}")
    print(f"  {'-'*30} {'-'*6}  {'-'*4}  {'-'*5}")

    for dim_name, dim_data in dims.items():
        label = dim_name.replace("_", " ").title()
        print(f"  {label:<30} {dim_data['score']:>6}  {dim_data['max']:>4}  {dim_data['pct']:>4.0f}%")

    print()

    if verbose:
        for dim_name, dim_data in dims.items():
            label = dim_name.replace("_", " ").title()
            print(f"  --- {label} ---")
            for detail in dim_data["details"]:
                print(f"    {detail}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Evaluate cancer research report quality (0-100)")
    parser.add_argument("input", help="Input JSON report file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed scoring breakdown")
    parser.add_argument("--json-output", "-j",
                        help="Save scoring result as JSON to this path")
    parser.add_argument("--score-only", action="store_true",
                        help="Print only the numeric score (for scripting)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = evaluate_report(data, verbose=args.verbose)

    if args.score_only:
        print(result["quality_score"])
    else:
        print_evaluation(result, verbose=args.verbose)

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        if not args.score_only:
            print(f"  Scoring saved to: {args.json_output}\n")

    return result["quality_score"]


if __name__ == "__main__":
    sys.exit(0 if main() >= 0 else 1)
