#!/usr/bin/env python3
"""
cancer_research_scorer.py

Validates cancer research JSON output and recomputes composite ratings.
Ensures all treatments are properly scored and sorted by rating.

Usage:
    python3 cancer_research_scorer.py <input.json> [--output <output.json>]
"""

import json
import sys
import argparse
from datetime import datetime

WEIGHTS = {
    "evidence_level": 0.30,
    "survival_benefit": 0.30,
    "accessibility": 0.15,
    "safety_profile": 0.15,
    "biomarker_match": 0.10,
}

RATING_FACTORS = list(WEIGHTS.keys())


def compute_composite(rating_breakdown: dict) -> float:
    """Compute weighted composite score from rating breakdown."""
    total = 0.0
    for factor, weight in WEIGHTS.items():
        score = rating_breakdown.get(factor, {}).get("score", 0)
        if not isinstance(score, (int, float)):
            score = 0
        score = max(0, min(10, score))  # clamp 0-10
        total += score * weight
    return round(total, 1)


def validate_treatment(treatment: dict, index: int) -> list:
    """Validate a single treatment entry. Returns list of warnings."""
    warnings = []
    required_fields = ["name", "category", "rating_breakdown"]

    for field in required_fields:
        if field not in treatment:
            warnings.append(f"Treatment #{index}: missing required field '{field}'")

    rb = treatment.get("rating_breakdown", {})
    for factor in RATING_FACTORS:
        if factor not in rb:
            warnings.append(f"Treatment #{index} ({treatment.get('name', '?')}): missing rating factor '{factor}'")
        else:
            score = rb[factor].get("score")
            if score is None:
                warnings.append(f"Treatment #{index}: '{factor}' has no score")
            elif not (0 <= score <= 10):
                warnings.append(f"Treatment #{index}: '{factor}' score {score} out of range [0-10]")
            if not rb[factor].get("rationale"):
                warnings.append(f"Treatment #{index}: '{factor}' has no rationale")

    return warnings


def validate_report(data: dict) -> list:
    """Validate the full report structure. Returns list of warnings."""
    warnings = []

    if "report_metadata" not in data:
        warnings.append("Missing 'report_metadata'")
    else:
        meta = data["report_metadata"]
        if not meta.get("cancer_type"):
            warnings.append("report_metadata: missing 'cancer_type'")
        if not meta.get("generated_date"):
            warnings.append("report_metadata: missing 'generated_date'")

    treatments = data.get("treatments", [])
    if not treatments:
        warnings.append("No treatments found in report")

    for i, t in enumerate(treatments):
        warnings.extend(validate_treatment(t, i + 1))

    return warnings


def recompute_and_sort(data: dict) -> dict:
    """Recompute all composite ratings and re-sort treatments by rating."""
    treatments = data.get("treatments", [])

    for t in treatments:
        rb = t.get("rating_breakdown", {})
        t["composite_rating"] = compute_composite(rb)

    # Sort descending by composite rating
    treatments.sort(key=lambda x: x.get("composite_rating", 0), reverse=True)

    # Reassign ranks
    for i, t in enumerate(treatments):
        t["rank"] = i + 1

    data["treatments"] = treatments
    return data


def print_summary(data: dict):
    """Print a human-readable summary of the rated treatments."""
    meta = data.get("report_metadata", {})
    print(f"\n{'='*70}")
    print(f"CANCER RESEARCH REPORT SUMMARY")
    print(f"Cancer Type: {meta.get('cancer_type', 'Unknown')}")
    print(f"Stage: {meta.get('stage', 'Not specified')}")
    print(f"Generated: {meta.get('generated_date', 'Unknown')}")
    print(f"{'='*70}\n")

    treatments = data.get("treatments", [])
    print(f"{'Rank':<6} {'Rating':<8} {'Category':<25} {'Treatment'}")
    print(f"{'-'*6} {'-'*8} {'-'*25} {'-'*40}")

    for t in treatments:
        rank = t.get("rank", "?")
        rating = t.get("composite_rating", 0)
        cat = t.get("category", "Unknown")[:24]
        name = t.get("name", "Unknown")
        print(f"{rank:<6} {rating:<8.1f} {cat:<25} {name}")

    print(f"\nTotal treatments analyzed: {len(treatments)}")

    trials = data.get("clinical_trials", [])
    print(f"Clinical trials identified: {len(trials)}")

    combos = data.get("combination_strategies", [])
    print(f"Combination strategies: {len(combos)}")

    supportive = data.get("supportive_care", [])
    print(f"Supportive care approaches: {len(supportive)}")

    sources = data.get("sources", [])
    print(f"Sources cited: {len(sources)}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Validate and score cancer research JSON")
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument("--output", "-o", help="Output JSON file path (optional, overwrites input if not specified)")
    parser.add_argument("--validate-only", action="store_true", help="Only validate, don't recompute")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    # Validate
    warnings = validate_report(data)
    if warnings:
        print("⚠️  Validation warnings:")
        for w in warnings:
            print(f"   - {w}")
    else:
        print("✅ Report structure validated successfully")

    if not args.validate_only:
        # Recompute ratings and sort
        data = recompute_and_sort(data)
        print("✅ Composite ratings recomputed and treatments re-sorted")

        # Save
        out_path = args.output or args.input
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved to {out_path}")

    # Print summary
    print_summary(data)


if __name__ == "__main__":
    main()
