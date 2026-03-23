#!/usr/bin/env python3
"""
strategy_optimizer.py — Parameterized Strategy Variant Generator

Mutates "knobs" in strategy.md to produce reproducible strategy variants
for the auto_loop. Each variant changes exactly ONE parameter, enabling
controlled A/B comparisons. Tracks outcomes in mutation_history.json
so proven losers are not retried.

Usage:
    python strategy_optimizer.py generate --n 3
    python strategy_optimizer.py generate --n 5 --focus search_budget
    python strategy_optimizer.py list-knobs
    python strategy_optimizer.py history
    python strategy_optimizer.py suggest
    python strategy_optimizer.py generate --knob tier1_searches --value 4
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# ── Data Structures ───────────────────────────────────────────────────────────

@dataclass
class Knob:
    name:               str
    category:           str
    current_value:      Any
    mutation_candidates: list
    description:        str
    section_pattern:    str          # regex that locates this knob's value in strategy.md
    value_group:        int = 1      # which regex capture group holds the value


@dataclass
class StrategyVariant:
    variant_id:         str
    base_strategy_hash: str
    mutation:           dict         # {"knob": str, "from": Any, "to": Any}
    content:            str          # full modified strategy.md text
    generated_at:       str


class MutationError(Exception):
    pass


# ── Knob Definitions ──────────────────────────────────────────────────────────

# These patterns match the exact Markdown table rows in strategy.md
_KNOB_DEFINITIONS = [
    # Search budget tier rows  ─ match "| Tier N — … | <int> |"
    Knob(
        name="tier1_searches",
        category="search_budget",
        current_value=3,
        mutation_candidates=[2, 3, 4, 5],
        description="Searches for Tier 1 — Standard of Care",
        section_pattern=r"(\|\s*Tier 1[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    Knob(
        name="tier2_searches",
        category="search_budget",
        current_value=3,
        mutation_candidates=[2, 3, 4, 5],
        description="Searches for Tier 2 — Approved Targeted/Immuno",
        section_pattern=r"(\|\s*Tier 2[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    Knob(
        name="tier3_searches",
        category="search_budget",
        current_value=3,
        mutation_candidates=[2, 3, 4, 5],
        description="Searches for Tier 3 — Clinical Trials",
        section_pattern=r"(\|\s*Tier 3[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    Knob(
        name="tier4_searches",
        category="search_budget",
        current_value=2,
        mutation_candidates=[1, 2, 3, 4],
        description="Searches for Tier 4 — Experimental",
        section_pattern=r"(\|\s*Tier 4[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    Knob(
        name="tier5_searches",
        category="search_budget",
        current_value=2,
        mutation_candidates=[1, 2, 3, 4],
        description="Searches for Tier 5 — Combination Strategies",
        section_pattern=r"(\|\s*Tier 5[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    Knob(
        name="tier6_searches",
        category="search_budget",
        current_value=2,
        mutation_candidates=[1, 2, 3],
        description="Searches for Tier 6 — Supportive/Adjunctive",
        section_pattern=r"(\|\s*Tier 6[^\|]*\|\s*)(\d+)(\s*\|)",
        value_group=2,
    ),
    # Source fetch targets  ─ match "Fetch at least N sources per case. Aim for M."
    Knob(
        name="min_fetch_sources",
        category="source_priority",
        current_value=8,
        mutation_candidates=[6, 8, 10, 12],
        description="Minimum sources to fetch per case",
        section_pattern=r"(Fetch at least\s+)(\d+)(\s+sources per case)",
        value_group=2,
    ),
    Knob(
        name="target_fetch_sources",
        category="source_priority",
        current_value=12,
        mutation_candidates=[10, 12, 15, 18],
        description="Target (aim for) number of sources per case",
        section_pattern=r"(Aim for\s+)(\d+)[-–]?(\d+)?(\s*\.)",
        value_group=2,
    ),
    # Treatment count targets  ─ match "Target: N-M treatments per case"
    Knob(
        name="min_treatments",
        category="treatment_targets",
        current_value=8,
        mutation_candidates=[8, 10, 12],
        description="Minimum treatments per report",
        section_pattern=r"(Target:\s+)(\d+)(-\d+\s+treatments per case)",
        value_group=2,
    ),
    # Combination strategy floor
    Knob(
        name="min_combos",
        category="treatment_targets",
        current_value=4,
        mutation_candidates=[3, 4, 5, 6],
        description="Minimum combination strategies per report",
        section_pattern=r"(Generate at least\s+)(\d+)(\s+combination strategies)",
        value_group=2,
    ),
    # Supportive care floor
    Knob(
        name="min_supportive",
        category="treatment_targets",
        current_value=4,
        mutation_candidates=[3, 4, 5, 6],
        description="Minimum supportive care approaches per report",
        section_pattern=r"(Include at least\s+)(\d+)(\s+supportive care approaches)",
        value_group=2,
    ),
    # Rating calibration — evidence level top anchor (patient count for score=10)
    Knob(
        name="evidence_anchor_500",
        category="rating_calibration",
        current_value=500,
        mutation_candidates=[300, 500, 750],
        description="Patient count threshold for Evidence Level = 10",
        section_pattern=r"(\*\*10\*\*: Large Phase 3 RCT.*?>)(\d+)(\s+patients)",
        value_group=2,
    ),
    # Survival benefit anchor — OS improvement for score=10
    Knob(
        name="survival_anchor_months",
        category="rating_calibration",
        current_value=12,
        mutation_candidates=[9, 12, 15],
        description="OS improvement (months) threshold for Survival Benefit = 10",
        section_pattern=r"(\*\*10\*\*: >)(\d+)(\s+months OS improvement)",
        value_group=2,
    ),
]

# Map dimension names (from evaluate.py output) to optimizer knob categories
_DIM_TO_CATEGORY = {
    "evidence_depth":           "search_budget",
    "source_quality":           "source_priority",
    "rating_calibration":       "rating_calibration",
    "tier_coverage":            "search_budget",
    "combo_supportive_coverage":"treatment_targets",
    "clinical_relevance":       "query_templates",
    "structural_integrity":     "treatment_targets",
}


# ── Core Functions ────────────────────────────────────────────────────────────

def _sha1(content: str) -> str:
    return hashlib.sha1(content.encode("utf-8")).hexdigest()[:10]


def _variant_id(knob_name: str, new_value: Any, base_hash: str) -> str:
    raw = f"{knob_name}_{new_value}_{base_hash}"
    short = hashlib.sha1(raw.encode()).hexdigest()[:8]
    return f"v_{knob_name}_{new_value}_{short}"


def parse_knobs(strategy_content: str) -> list:
    """
    Return a fresh copy of knob definitions with current_value updated
    to match what is actually in the strategy_content.
    """
    knobs = []
    for template in _KNOB_DEFINITIONS:
        knob = Knob(**template.__dict__.copy())
        m = re.search(template.section_pattern, strategy_content, re.IGNORECASE)
        if m:
            try:
                knob.current_value = int(m.group(template.value_group))
            except (ValueError, IndexError):
                pass  # keep default
        knobs.append(knob)
    return knobs


def apply_mutation(strategy_content: str, knob: Knob, new_value: Any) -> str:
    """
    Apply a single knob mutation. Returns modified strategy string.
    Raises MutationError if the pattern is not found.
    """
    def replacer(m: re.Match) -> str:
        groups = list(m.groups())
        groups[knob.value_group - 1] = str(new_value)
        return "".join(groups)

    new_content, count = re.subn(
        knob.section_pattern, replacer, strategy_content,
        count=1, flags=re.IGNORECASE
    )
    if count == 0:
        raise MutationError(
            f"Pattern not found for knob '{knob.name}': {knob.section_pattern!r}"
        )
    return new_content


def generate_variants(
    strategy_content: str,
    n: int = 3,
    seed: Optional[int] = None,
    exclude_knobs: Optional[list] = None,
    focus_category: Optional[str] = None,
    history: Optional[dict] = None,
) -> list:
    """
    Generate N StrategyVariant objects, each mutating exactly one knob.

    Args:
        strategy_content: Raw content of strategy.md
        n:                Number of variants to generate
        seed:             RNG seed for reproducibility
        exclude_knobs:    List of knob names to skip
        focus_category:   Only mutate knobs in this category
        history:          mutation_history dict; avoids re-trying known losers

    Returns:
        List of StrategyVariant objects (may be < n if candidates exhausted)
    """
    rng = random.Random(seed)
    knobs = parse_knobs(strategy_content)
    base_hash = _sha1(strategy_content)
    exclude_knobs = set(exclude_knobs or [])

    # Build candidate (knob, new_value) pairs
    # Avoid: same as current, already tried and lost
    tried_losers: set[tuple] = set()
    if history:
        for entry in history.get("mutations", []):
            if entry.get("decision") == "discard":
                tried_losers.add((entry["knob"], entry["value"]))

    candidates = []
    for knob in knobs:
        if knob.name in exclude_knobs:
            continue
        if focus_category and knob.category != focus_category:
            continue
        for val in knob.mutation_candidates:
            if val == knob.current_value:
                continue
            if (knob.name, val) in tried_losers:
                continue
            candidates.append((knob, val))

    rng.shuffle(candidates)

    # Deduplicate by (knob.name) so we don't generate two variants for same knob
    seen_knobs: set[str] = set()
    variants = []
    for knob, new_value in candidates:
        if len(variants) >= n:
            break
        if knob.name in seen_knobs:
            continue
        try:
            new_content = apply_mutation(strategy_content, knob, new_value)
        except MutationError as exc:
            print(f"  [warn] Skipping knob '{knob.name}': {exc}", file=sys.stderr)
            continue

        vid = _variant_id(knob.name, new_value, base_hash)
        # Prepend metadata comment block
        meta_comment = (
            f"<!-- VARIANT METADATA\n"
            f"variant_id: {vid}\n"
            f"base_hash: {base_hash}\n"
            f"mutation: {knob.name}: {knob.current_value} -> {new_value}\n"
            f"generated_at: {datetime.now().isoformat()}\n"
            f"-->\n\n"
        )
        variants.append(StrategyVariant(
            variant_id=vid,
            base_strategy_hash=base_hash,
            mutation={"knob": knob.name, "from": knob.current_value, "to": new_value},
            content=meta_comment + new_content,
            generated_at=datetime.now().isoformat(),
        ))
        seen_knobs.add(knob.name)

    return variants


def variant_to_file(variant: "StrategyVariant", output_dir: str) -> str:
    """Write variant content to output_dir/variant_<id>.md. Returns path."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{variant.variant_id}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(variant.content)
    return path


# ── History Tracking ──────────────────────────────────────────────────────────

HISTORY_FILE = "mutation_history.json"


def load_mutation_history(history_file: str = HISTORY_FILE) -> dict:
    """Load mutation history. Returns empty structure if not found."""
    if not os.path.exists(history_file):
        return {"mutations": []}
    with open(history_file, "r", encoding="utf-8") as f:
        return json.load(f)


def record_mutation_outcome(
    variant: "StrategyVariant",
    mean_score: float,
    decision: str,
    history_file: str = HISTORY_FILE,
) -> None:
    """Append mutation outcome to history file."""
    history = load_mutation_history(history_file)
    history["mutations"].append({
        "variant_id":   variant.variant_id,
        "knob":         variant.mutation["knob"],
        "from_value":   variant.mutation["from"],
        "value":        variant.mutation["to"],
        "mean_score":   mean_score,
        "decision":     decision,
        "timestamp":    datetime.now().isoformat(),
    })
    tmp = history_file + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
    os.replace(tmp, history_file)


# ── Smart Suggestions ─────────────────────────────────────────────────────────

def suggest_focus_category(
    history: Optional[dict] = None,
    last_run_path: str = "experiment_reports/last_run_scores.json",
) -> str:
    """
    Heuristic: find the weakest evaluate.py dimension from last run and map
    it to a knob category. Falls back to "search_budget" if no data.
    """
    if not os.path.exists(last_run_path):
        return "search_budget"

    try:
        with open(last_run_path, "r", encoding="utf-8") as f:
            run_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return "search_budget"

    cases = run_data.get("cases", [])
    evaluated = [c for c in cases if c.get("status") == "evaluated" and c.get("dimensions")]
    if not evaluated:
        return "search_budget"

    # Average each dimension across all cases
    dim_averages = {}
    all_dims = list(evaluated[0]["dimensions"].keys())
    for dim in all_dims:
        scores = []
        for case in evaluated:
            d = case["dimensions"].get(dim, {})
            mx = d.get("max", 1)
            sc = d.get("score", 0)
            if mx > 0:
                scores.append(sc / mx)
        if scores:
            dim_averages[dim] = sum(scores) / len(scores)

    # Find worst dimension
    worst_dim = min(dim_averages, key=lambda d: dim_averages[d]) if dim_averages else "evidence_depth"
    category = _DIM_TO_CATEGORY.get(worst_dim, "search_budget")

    return category


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate and manage strategy.md variants for autoresearch loop"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    p_gen = sub.add_parser("generate", help="Generate strategy variants")
    p_gen.add_argument("--n", type=int, default=3, help="Number of variants")
    p_gen.add_argument("--focus", default=None,
                       choices=["search_budget", "source_priority", "treatment_targets",
                                "rating_calibration", "query_templates"],
                       help="Restrict mutations to this category")
    p_gen.add_argument("--knob", default=None, help="Mutate only this specific knob")
    p_gen.add_argument("--value", default=None, type=int, help="Set knob to this value")
    p_gen.add_argument("--seed", type=int, default=None)
    p_gen.add_argument("--output-dir", default="experiment_reports/variants")
    p_gen.add_argument("--strategy", default="strategy.md")
    p_gen.add_argument("--no-history", action="store_true",
                       help="Ignore mutation history when generating")

    # list-knobs
    p_lk = sub.add_parser("list-knobs", help="List all knobs and current values")
    p_lk.add_argument("--strategy", default="strategy.md")

    # history
    p_hist = sub.add_parser("history", help="Show mutation history and win rates")
    p_hist.add_argument("--file", default=HISTORY_FILE)

    # suggest
    p_sug = sub.add_parser("suggest", help="Suggest focus category based on last run")
    p_sug.add_argument("--last-run", default="experiment_reports/last_run_scores.json")

    args = parser.parse_args()

    if args.command == "generate":
        with open(args.strategy, "r", encoding="utf-8") as f:
            content = f.read()

        history = None if args.no_history else load_mutation_history()

        # Single-knob mode
        if args.knob and args.value is not None:
            knobs = parse_knobs(content)
            target = next((k for k in knobs if k.name == args.knob), None)
            if not target:
                print(f"Knob '{args.knob}' not found.", file=sys.stderr)
                sys.exit(1)
            base_hash = _sha1(content)
            vid = _variant_id(target.name, args.value, base_hash)
            meta = (
                f"<!-- VARIANT METADATA\nvariant_id: {vid}\n"
                f"mutation: {target.name}: {target.current_value} -> {args.value}\n-->\n\n"
            )
            new_content = apply_mutation(content, target, args.value)
            v = StrategyVariant(
                variant_id=vid,
                base_strategy_hash=base_hash,
                mutation={"knob": target.name, "from": target.current_value, "to": args.value},
                content=meta + new_content,
                generated_at=datetime.now().isoformat(),
            )
            path = variant_to_file(v, args.output_dir)
            print(f"Written: {path}")
            return

        variants = generate_variants(
            content,
            n=args.n,
            seed=args.seed,
            focus_category=args.focus,
            history=history,
        )
        if not variants:
            print("No new variants generated (all candidates exhausted or tried).")
            return
        for v in variants:
            path = variant_to_file(v, args.output_dir)
            print(f"  {v.variant_id}  [{v.mutation['knob']}: {v.mutation['from']} -> {v.mutation['to']}]  {path}")

    elif args.command == "list-knobs":
        with open(args.strategy, "r", encoding="utf-8") as f:
            content = f.read()
        knobs = parse_knobs(content)
        print(f"\n{'Knob':<30} {'Category':<20} {'Current':>8}  {'Candidates'}")
        print("-" * 80)
        for k in knobs:
            cands = ", ".join(str(c) for c in k.mutation_candidates)
            print(f"{k.name:<30} {k.category:<20} {str(k.current_value):>8}  [{cands}]")

    elif args.command == "history":
        hist = load_mutation_history(args.file)
        mutations = hist.get("mutations", [])
        if not mutations:
            print("No mutation history found.")
            return
        keep = [m for m in mutations if m.get("decision") == "keep"]
        disc = [m for m in mutations if m.get("decision") == "discard"]
        print(f"\nTotal mutations: {len(mutations)}  (keep: {len(keep)}, discard: {len(disc)})\n")
        print(f"{'Knob':<28} {'From':>6} {'To':>6} {'Score':>7}  {'Decision'}")
        print("-" * 60)
        for m in mutations[-20:]:
            print(f"{m['knob']:<28} {str(m.get('from_value','?')):>6} {str(m['value']):>6} "
                  f"{m.get('mean_score', 0):>7.1f}  {m['decision']}")

    elif args.command == "suggest":
        cat = suggest_focus_category(last_run_path=args.last_run)
        print(f"Suggested focus category: {cat}")
        # Explain why
        if os.path.exists(args.last_run):
            with open(args.last_run) as f:
                run = json.load(f)
            cases = [c for c in run.get("cases", []) if c.get("dimensions")]
            if cases:
                all_dims = list(cases[0]["dimensions"].keys())
                avgs = {}
                for d in all_dims:
                    scores = [c["dimensions"][d]["score"] / max(c["dimensions"][d]["max"], 1)
                              for c in cases if d in c.get("dimensions", {})]
                    if scores:
                        avgs[d] = sum(scores) / len(scores)
                print("\nDimension averages (pct of max):")
                for d, avg in sorted(avgs.items(), key=lambda x: x[1]):
                    bar = "#" * int(avg * 20)
                    print(f"  {d:<35} {bar:<20} {avg*100:>5.1f}%")


if __name__ == "__main__":
    main()
