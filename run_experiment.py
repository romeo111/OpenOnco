#!/usr/bin/env python3
"""
run_experiment.py — Experiment Orchestrator for AutoResearch Loop

For each case in benchmark_cases.json:
1. Invoke research skill with current strategy.md
2. Enforce time limit per case
3. Capture JSON output
4. Score with evaluate.py
5. Compute mean score, append to results.tsv
6. Return keep/discard decision

Usage:
    python run_experiment.py
    python run_experiment.py --cases benchmark_cases.json --timeout 600
    python run_experiment.py --best-score 55.0
    python run_experiment.py --single-case HN-003
    python run_experiment.py --strategy experiment_reports/variants/v_tier1_searches_4_abc.md
    python run_experiment.py --reports-dir experiment_reports/runs/run_abc123
    python run_experiment.py --enrich-pubmed
"""

import json
import re
import sys
import os
import argparse
import subprocess
import signal
import time
from datetime import datetime
from pathlib import Path

# Import the evaluator and tumor board
from evaluate import evaluate_report
from virtual_tumor_board import run_heuristic_board

RESULTS_FILE = "results.tsv"
REPORTS_DIR = "experiment_reports"
KEEP_THRESHOLD = 1.0  # must improve by this much to keep


def load_cases(cases_file: str) -> list:
    """Load benchmark cases from JSON file."""
    with open(cases_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("cases", [])


def load_strategy(strategy_file: str = "strategy.md") -> str:
    """Load strategy file content."""
    with open(strategy_file, "r", encoding="utf-8") as f:
        return f.read()


# ── Complexity Classifier ────────────────────────────────────────────────────

_COMPLEXITY_DEFAULTS = {
    "simple": 10, "standard": 15, "complex": 18, "highly_complex": 20
}

_RARE_HISTOLOGY_TERMS = [
    "adenoid cystic", "mucoepidermoid", "acinic cell", "salivary gland",
    "sinonasal", "nasopharyngeal", "paraganglioma", "sarcoma", "lymphoma",
    "melanoma", "chordoma", "esthesioneuroblastoma", "snuc", "nut",
    "plasmacytoma", "kaposi", "ameloblastic", "ewing",
]

_ACTIONABLE_FUSION_TERMS = [
    "fusion", "rearrangement", "amplification", "ntrk", "alk", "ros1",
    "ret", "braf v600e", "myb-nfib", "etv6", "ewsr1",
]


def classify_case_complexity(case: dict, strategy: str) -> dict:
    """
    Parse the ## Complexity Classifier section from strategy and score the case.
    Falls back to default budget (15 searches) if parsing fails.

    Returns:
        {
          "complexity_score": int,
          "label": str,
          "total_searches": int,
          "tier_budgets": dict,   # {tier: search_count}
        }
    """
    score = 0
    ctx = case.get("patient_context", {})
    cancer_type_lower = case.get("cancer_type", "").lower()
    markers = [m.lower() for m in case.get("molecular_markers", [])]
    ps = (ctx.get("performance_status", "") or "").lower()
    stage_lower = (case.get("stage", "") or "").lower()
    risk_lower = " ".join(ctx.get("risk_factors", [])).lower()

    # Rare histology
    if any(term in cancer_type_lower for term in _RARE_HISTOLOGY_TERMS):
        score += 3

    # Multiple markers
    if len(markers) >= 3:
        score += 2

    # Actionable fusions
    all_markers_str = " ".join(markers)
    if any(term in all_markers_str for term in _ACTIONABLE_FUSION_TERMS):
        score += 2

    # Poor performance
    if any(f"ecog {n}" in ps for n in ["2", "3", "4"]):
        score += 3

    # Metastatic/unresectable
    if any(t in stage_lower for t in ["m1", "ivb", "ivc", "unresectable"]):
        score += 2

    # Prior treatment complication
    if any(t in risk_lower for t in ["prior radiation", "prior surgery",
                                      "second primary", "recurrent"]):
        score += 1

    # Map score to label + budget
    if score <= 2:
        label, total = "simple", 10
    elif score <= 5:
        label, total = "standard", 15
    elif score <= 8:
        label, total = "complex", 18
    else:
        label, total = "highly_complex", 20

    # Try to parse override from strategy Complexity Classifier section
    try:
        section_match = re.search(
            r"## Complexity Classifier.*?### Budget Tiers.*?\n((?:\|.*\n)+)",
            strategy, re.DOTALL
        )
        if section_match:
            table = section_match.group(1)
            for row in table.splitlines():
                cells = [c.strip() for c in row.strip("|").split("|")]
                if len(cells) >= 3 and cells[2].strip().isdigit():
                    range_str = cells[0].strip()
                    budget_val = int(cells[2].strip())
                    # Parse range like "0–2" or "3–5" or "9+"
                    if "+" in range_str:
                        low = int(re.search(r"\d+", range_str).group())
                        if score >= low:
                            total = budget_val
                    else:
                        nums = re.findall(r"\d+", range_str)
                        if len(nums) == 2:
                            low, high = int(nums[0]), int(nums[1])
                            if low <= score <= high:
                                total = budget_val
    except Exception:
        pass  # always fall back gracefully

    # Distribute budget across tiers (scale proportionally from base 15)
    base_tiers = {1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2}
    if total != 15:
        extra = total - 15
        tier_budgets = dict(base_tiers)
        if extra > 0:
            for t in (4, 3, 2):  # Experimental gets first bump
                tier_budgets[t] += 1
                extra -= 1
                if extra <= 0:
                    break
        elif extra < 0:
            for t in (6, 5, 4):  # Cut from lower tiers first
                if tier_budgets[t] > 1:
                    tier_budgets[t] -= 1
                    extra += 1
                if extra >= 0:
                    break
    else:
        tier_budgets = dict(base_tiers)

    return {
        "complexity_score": score,
        "label":            label,
        "total_searches":   total,
        "tier_budgets":     {f"tier{k}": v for k, v in tier_budgets.items()},
    }


def build_research_prompt(case: dict, strategy: str, reports_dir: str = REPORTS_DIR) -> str:
    """Build the research prompt for a single case, including adaptive search budget."""
    ctx = case.get("patient_context", {})
    markers = ", ".join(case.get("molecular_markers", []))
    risk_factors = ", ".join(ctx.get("risk_factors", []))
    comorbidities = ", ".join(ctx.get("comorbidities", [])) or "none"

    complexity = classify_case_complexity(case, strategy)
    tier_lines = "  ".join(
        f"Tier {k[-1]}: {v} searches"
        for k, v in complexity["tier_budgets"].items()
    )

    prompt = f"""Research the following cancer case and produce a comprehensive JSON report.

## Patient Case
- **Cancer type**: {case['cancer_type']}
- **Stage**: {case['stage']}
- **Molecular markers**: {markers}
- **Patient**: {ctx.get('age', 'unknown')} year old {ctx.get('sex', 'unknown')}
- **Performance status**: {ctx.get('performance_status', 'unknown')}
- **Risk factors**: {risk_factors}
- **Comorbidities**: {comorbidities}

## Computed Search Budget for This Case
- Complexity: **{complexity['label']}** (score: {complexity['complexity_score']})
- Total searches allocated: **{complexity['total_searches']}**
- Tier distribution: {tier_lines}

## Research Strategy
Follow the research strategy below for search queries, source prioritization,
rating calibration, and output targets:

{strategy}

## Output Requirements
Generate a JSON report matching the schema in output_template.md.
The JSON must include: report_metadata, treatments (8-15), clinical_trials,
combination_strategies, supportive_care, and sources.

Save the JSON report to: {reports_dir}/{case['id']}_report.json
"""
    return prompt


def run_single_case(
    case: dict,
    strategy: str,
    timeout: int,
    reports_dir: str = REPORTS_DIR,
    enrich_pubmed: bool = False,
) -> dict:
    """Run research for a single case and return evaluation result.

    This function prepares the prompt and invokes the research skill.
    In practice, the research is executed by Claude Code via the skill.
    For automated runs, this writes the prompt to a file for the agent to pick up.
    """
    case_id = case["id"]
    report_path = os.path.join(reports_dir, f"{case_id}_report.json")
    prompt_path = os.path.join(reports_dir, f"{case_id}_prompt.md")

    # Build and save the prompt
    prompt = build_research_prompt(case, strategy, reports_dir=reports_dir)
    os.makedirs(reports_dir, exist_ok=True)
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    # Check if a report already exists (from a previous or concurrent run)
    if os.path.exists(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)

            # Optional PubMed enrichment before scoring
            if enrich_pubmed:
                try:
                    from pubmed_client import enrich_report_with_pubmed
                    n_enriched = enrich_report_with_pubmed(report_path, verbose=False)
                    if n_enriched > 0:
                        with open(report_path, "r", encoding="utf-8") as f:
                            report_data = json.load(f)
                except Exception:
                    pass  # enrichment is always optional

            # Optional ClinicalTrials.gov enrichment
            if enrich_pubmed:  # reuse same flag — both are live-data enrichments
                try:
                    from clinicaltrials_client import enrich_report_with_trials
                    n_ct = enrich_report_with_trials(report_path, verbose=False)
                    if n_ct > 0:
                        with open(report_path, "r", encoding="utf-8") as f:
                            report_data = json.load(f)
                except Exception:
                    pass  # always optional

            result = evaluate_report(report_data)
            board = run_heuristic_board(report_data)
            return {
                "case_id": case_id,
                "cancer_type": case["cancer_type"],
                "quality_score": result["quality_score"],
                "dimensions": result["dimensions"],
                "board_score": board["board_score"],
                "board_spread": board["spread"],
                "board_most_critical": board["most_critical"],
                "report_path": report_path,
                "status": "evaluated",
            }
        except (json.JSONDecodeError, KeyError) as e:
            return {
                "case_id": case_id,
                "cancer_type": case["cancer_type"],
                "quality_score": 0,
                "dimensions": {},
                "report_path": report_path,
                "status": f"error: {e}",
            }

    # If no report exists yet, return a pending status
    return {
        "case_id": case_id,
        "cancer_type": case["cancer_type"],
        "quality_score": 0,
        "dimensions": {},
        "report_path": report_path,
        "prompt_path": prompt_path,
        "status": "prompt_ready",
    }


def compute_mean_score(results: list) -> float:
    """Compute mean quality score across all evaluated cases."""
    scores = [r["quality_score"] for r in results if r["status"] == "evaluated"]
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 1)


def get_best_score() -> float:
    """Read best_score from results.tsv (last 'keep' entry, or 0)."""
    if not os.path.exists(RESULTS_FILE):
        return 0.0

    best = 0.0
    with open(RESULTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("timestamp"):
                continue
            parts = line.split("\t")
            if len(parts) >= 4 and parts[3] == "keep":
                try:
                    score = float(parts[2])
                    best = max(best, score)
                except ValueError:
                    pass
    return best


def append_result(mean_score: float, decision: str, note: str = ""):
    """Append a result row to results.tsv."""
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w") as f:
            f.write("timestamp\titeration\tmean_score\tdecision\tnote\n")

    # Count existing rows to determine iteration number
    iteration = 0
    with open(RESULTS_FILE, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("timestamp"):
                iteration += 1

    with open(RESULTS_FILE, "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts}\t{iteration}\t{mean_score}\t{decision}\t{note}\n")


def print_experiment_summary(results: list, mean_score: float, best_score: float, decision: str):
    """Print a formatted experiment summary."""
    print(f"\n{'='*70}")
    print(f"  EXPERIMENT RESULTS")
    print(f"{'='*70}")
    print(f"  Cases evaluated: {sum(1 for r in results if r['status'] == 'evaluated')}/{len(results)}")
    print(f"  Cases pending:   {sum(1 for r in results if r['status'] == 'prompt_ready')}")
    print(f"  Mean score:      {mean_score}/100")
    print(f"  Best score:      {best_score}/100")
    print(f"  Threshold:       {best_score + KEEP_THRESHOLD}/100")
    print(f"  Decision:        {decision.upper()}")
    print(f"{'='*70}\n")

    print(f"  {'Case':<10} {'Score':>6}  {'Status':<12} {'Cancer Type'}")
    print(f"  {'-'*10} {'-'*6}  {'-'*12} {'-'*40}")
    for r in results:
        print(f"  {r['case_id']:<10} {r['quality_score']:>6}  {r['status']:<12} {r['cancer_type'][:40]}")
    print()

    # Dimension summary across evaluated cases
    evaluated = [r for r in results if r["status"] == "evaluated"]
    if evaluated:
        dim_names = list(evaluated[0].get("dimensions", {}).keys())
        if dim_names:
            print(f"  Average Dimension Scores:")
            for dim in dim_names:
                scores = [r["dimensions"][dim]["score"] for r in evaluated if dim in r.get("dimensions", {})]
                maxes = [r["dimensions"][dim]["max"] for r in evaluated if dim in r.get("dimensions", {})]
                if scores:
                    avg = sum(scores) / len(scores)
                    mx = maxes[0] if maxes else 0
                    label = dim.replace("_", " ").title()
                    print(f"    {label:<30} {avg:>5.1f}/{mx}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Run autoresearch experiment")
    parser.add_argument("--cases", default="benchmark_cases.json",
                        help="Path to benchmark cases JSON (default: benchmark_cases.json)")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Timeout per case in seconds (default: 600)")
    parser.add_argument("--best-score", type=float, default=None,
                        help="Override best score (default: read from results.tsv)")
    parser.add_argument("--single-case", default=None,
                        help="Run only a single case by ID")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate prompts only, don't evaluate")
    parser.add_argument("--strategy", default="strategy.md",
                        help="Path to strategy file (default: strategy.md)")
    parser.add_argument("--reports-dir", default=REPORTS_DIR,
                        help=f"Directory for reports output (default: {REPORTS_DIR})")
    parser.add_argument("--enrich-pubmed", action="store_true",
                        help="Enrich reports with live PubMed data before scoring")
    parser.add_argument("--show-complexity", action="store_true",
                        help="Print complexity classification for each case")
    args = parser.parse_args()

    reports_dir = args.reports_dir

    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Load cases
    cases = load_cases(args.cases)
    if not cases:
        print("Error: No benchmark cases found.", file=sys.stderr)
        sys.exit(1)

    if args.single_case:
        cases = [c for c in cases if c["id"] == args.single_case]
        if not cases:
            print(f"Error: Case '{args.single_case}' not found.", file=sys.stderr)
            sys.exit(1)

    # Load strategy
    strategy = load_strategy(args.strategy)
    print(f"Loaded {args.strategy} ({len(strategy)} chars)")
    print(f"Reports dir: {reports_dir}")
    print(f"Running {len(cases)} benchmark cases...")

    # Run each case
    results = []
    for i, case in enumerate(cases):
        print(f"\n[{i+1}/{len(cases)}] {case['id']}: {case['cancer_type']}")
        if args.show_complexity:
            cx = classify_case_complexity(case, strategy)
            print(f"  Complexity: {cx['label']} (score {cx['complexity_score']}, "
                  f"{cx['total_searches']} searches)")
        result = run_single_case(
            case, strategy, args.timeout,
            reports_dir=reports_dir,
            enrich_pubmed=args.enrich_pubmed,
        )
        results.append(result)

        if result["status"] == "evaluated":
            print(f"  Score: {result['quality_score']}/100 | Board: {result.get('board_score', '?')}/100 (spread: {result.get('board_spread', '?')})")
        elif result["status"] == "prompt_ready":
            print(f"  Prompt saved: {result.get('prompt_path', 'N/A')}")
            print(f"  Awaiting report: {result['report_path']}")
        else:
            print(f"  Status: {result['status']}")

    if args.dry_run:
        print(f"\nDry run complete. {len(results)} prompts generated in {REPORTS_DIR}/")
        return

    # Compute results
    mean_score = compute_mean_score(results)
    best_score = args.best_score if args.best_score is not None else get_best_score()

    # Keep/discard decision
    evaluated_count = sum(1 for r in results if r["status"] == "evaluated")
    if evaluated_count == 0:
        decision = "pending"
        note = f"No reports evaluated yet. Prompts ready in {REPORTS_DIR}/"
    elif mean_score >= best_score + KEEP_THRESHOLD:
        decision = "keep"
        note = f"Improved by {mean_score - best_score:.1f} pts"
    else:
        decision = "discard"
        note = f"Only {mean_score:.1f} vs threshold {best_score + KEEP_THRESHOLD:.1f}"

    # Log results
    append_result(mean_score, decision, note)

    # Print summary
    print_experiment_summary(results, mean_score, best_score, decision)

    # Write per-case results for analysis
    per_case_path = os.path.join(REPORTS_DIR, "last_run_scores.json")
    with open(per_case_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "mean_score": mean_score,
            "best_score": best_score,
            "decision": decision,
            "cases": results,
        }, f, indent=2, default=str)

    # Exit code: 0 if keep, 1 if discard, 2 if pending
    if decision == "keep":
        sys.exit(0)
    elif decision == "discard":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
