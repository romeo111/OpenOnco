#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
auto_loop.py — Automatic Iteration Runner for Cancer AutoResearch

Replaces the manual while-loop described in program.md with a fully automated
Python process. Generates strategy variants, runs experiments (serially or in
parallel), keeps the best variant if it improves the score, and loops until
a target score or max iterations is reached.

Usage:
    python auto_loop.py
    python auto_loop.py --target-score 92 --max-iters 20
    python auto_loop.py --cases benchmark_cases_hn3.json --parallel 3 --variants 3
    python auto_loop.py --enrich-pubmed --focus search_budget
    python auto_loop.py --dry-run       # just generate variants, no experiment

The loop writes to:
    strategy.md               (overwritten when a variant is kept)
    results.tsv               (appended by run_experiment.py subprocess)
    auto_loop.log             (NDJSON, one record per iteration)
    mutation_history.json     (managed by strategy_optimizer)
    experiment_reports/variants/  (generated strategy variant files)
    experiment_reports/runs/      (per-variant isolated report directories)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


# ── Constants ─────────────────────────────────────────────────────────────────

KEEP_THRESHOLD = 2.5         # min improvement to accept a variant (1.0 was within noise floor)
VARIANTS_DIR   = os.path.join("experiment_reports", "variants")
RUNS_DIR       = os.path.join("experiment_reports", "runs")
LOG_FILE       = "auto_loop.log"
RESULTS_FILE   = "results.tsv"


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_best_score() -> float:
    """Read highest 'keep' score from results.tsv."""
    if not os.path.exists(RESULTS_FILE):
        return 0.0
    best = 0.0
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("timestamp"):
                continue
            parts = line.split("\t")
            if len(parts) >= 4 and parts[3] == "keep":
                try:
                    best = max(best, float(parts[2]))
                except ValueError:
                    pass
    return best


def load_strategy(path: str = "strategy.md") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def atomic_write_strategy(content: str, path: str = "strategy.md") -> None:
    """Write strategy atomically via .tmp rename (safe against interruption)."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)


def append_log(record: dict) -> None:
    """Append one NDJSON record to auto_loop.log."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def read_last_run_scores(run_dir: str) -> dict:
    """Read last_run_scores.json from a run directory."""
    path = os.path.join(run_dir, "last_run_scores.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_header(iteration: int, best_score: float, target: float) -> None:
    bar = "=" * 65
    print(f"\n{bar}")
    print(f"  AUTO LOOP — Iteration {iteration}")
    print(f"  Best score: {best_score:.1f}/100   Target: {target}/100")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{bar}")


# ── Single Variant Runner ─────────────────────────────────────────────────────

def run_single_variant(
    variant_id: str,
    variant_path: str,
    run_dir: str,
    cases_file: str,
    best_score: float,
    timeout_per_case: int,
    enrich_pubmed: bool,
    verbose: bool = True,
) -> dict:
    """
    Run run_experiment.py for one strategy variant in an isolated directory.
    Returns result dict with mean_score, decision, per-case data.
    """
    os.makedirs(run_dir, exist_ok=True)

    cmd = [
        sys.executable, "run_experiment.py",
        "--cases",       cases_file,
        "--strategy",    variant_path,
        "--reports-dir", run_dir,
        "--best-score",  str(best_score),
        "--timeout",     str(timeout_per_case),
    ]
    if enrich_pubmed:
        cmd.append("--enrich-pubmed")

    start = time.monotonic()
    if verbose:
        print(f"  [variant {variant_id[:20]}] running...")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=not verbose,
            text=True,
            timeout=timeout_per_case * 200,  # generous outer limit
        )
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        exit_code = 3

    duration = time.monotonic() - start

    # Read scores from the run directory
    run_data = read_last_run_scores(run_dir)
    mean_score = run_data.get("mean_score", 0.0)
    decision = run_data.get("decision", "pending")
    per_case = run_data.get("cases", [])

    return {
        "variant_id":    variant_id,
        "variant_path":  variant_path,
        "run_dir":       run_dir,
        "mean_score":    mean_score,
        "decision":      decision,
        "exit_code":     exit_code,
        "duration_s":    round(duration, 1),
        "per_case":      per_case,
    }


# ── Parallel Execution ────────────────────────────────────────────────────────

def run_parallel_variants(
    variants: list,          # list of StrategyVariant objects
    cases_file: str,
    best_score: float,
    timeout_per_case: int,
    max_workers: int,
    enrich_pubmed: bool,
    iteration: int,
) -> list:
    """
    Submit all variants to a ThreadPoolExecutor.
    Returns results sorted by mean_score descending.
    """
    futures = {}
    os.makedirs(RUNS_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for v in variants:
            run_dir = os.path.join(RUNS_DIR, f"iter{iteration}_{v.variant_id}")
            future = executor.submit(
                run_single_variant,
                v.variant_id,
                v._file_path,      # set by write_variants_to_disk()
                run_dir,
                cases_file,
                best_score,
                timeout_per_case,
                enrich_pubmed,
                verbose=(max_workers == 1),
            )
            futures[future] = v

        results = []
        for future in as_completed(futures):
            result = future.result()
            v = futures[future]
            result["mutation"] = v.mutation
            results.append(result)
            print(f"  [{result['variant_id'][:24]}]  score={result['mean_score']:.1f}  "
                  f"decision={result['decision']}  ({result['duration_s']}s)")

    return sorted(results, key=lambda r: r["mean_score"], reverse=True)


# ── Main Loop ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Automated autoresearch loop — runs indefinitely until target or max-iters"
    )
    parser.add_argument("--target-score", type=float, default=80.0,
                        help="Stop when mean_score >= this (default: 80.0)")
    parser.add_argument("--max-iters",    type=int,   default=50,
                        help="Hard stop after N iterations (default: 50)")
    parser.add_argument("--cases",        default="benchmark_cases.json",
                        help="Benchmark cases file (default: benchmark_cases.json)")
    parser.add_argument("--timeout",      type=int,   default=600,
                        help="Per-case timeout seconds (default: 600)")
    parser.add_argument("--parallel",     type=int,   default=1,
                        help="Max parallel variant experiments (default: 1)")
    parser.add_argument("--variants",     type=int,   default=3,
                        help="Variants to generate per iteration (default: 3)")
    parser.add_argument("--strategy",     default="strategy.md",
                        help="Baseline strategy file (default: strategy.md)")
    parser.add_argument("--focus",        default=None,
                        choices=["search_budget", "source_priority", "treatment_targets",
                                 "rating_calibration", "query_templates"],
                        help="Restrict mutations to this knob category")
    parser.add_argument("--auto-focus",   action="store_true",
                        help="Auto-detect weakest dimension and focus mutations there")
    parser.add_argument("--enrich-pubmed", action="store_true",
                        help="Enrich reports with live PubMed data before scoring")
    parser.add_argument("--seed",         type=int,   default=None,
                        help="RNG seed for reproducible variant generation")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Generate variants only — do not run experiments")
    parser.add_argument("--no-revert",    action="store_true",
                        help="Never revert strategy.md (always keep last variant)")
    parser.add_argument("--local-llm",    action="store_true",
                        help="Use local Ollama LLM (phi3:mini) to add one semantic "
                             "strategy variant per iteration (requires ollama)")
    args = parser.parse_args()

    # Import optimizer here so module-level errors surface clearly
    from strategy_optimizer import (
        generate_variants, variant_to_file, load_mutation_history,
        record_mutation_outcome, suggest_focus_category,
        StrategyVariant,
    )

    os.makedirs(VARIANTS_DIR, exist_ok=True)
    os.makedirs(RUNS_DIR, exist_ok=True)

    # ── Local LLM setup ──
    local_llm_ready = False
    if args.local_llm:
        try:
            from local_llm import check_ollama, is_model_available, generate_semantic_variant, MUTATE_MODEL
            if check_ollama() and is_model_available(MUTATE_MODEL):
                local_llm_ready = True
                print(f"[local-llm] phi3:mini ready via ollama")
            else:
                print(f"[local-llm] ollama/phi3:mini not available — semantic variants disabled")
                print(f"  Run: ollama pull phi3:mini")
        except ImportError:
            print("[local-llm] local_llm.py not found — semantic variants disabled")

    print(f"\n{'='*65}")
    print(f"  CANCER AUTORESEARCH — AUTO LOOP")
    print(f"  Target: {args.target_score}/100   Max iterations: {args.max_iters}")
    print(f"  Cases: {args.cases}   Variants/iter: {args.variants}")
    print(f"  Parallel workers: {args.parallel}   PubMed: {args.enrich_pubmed}")
    print(f"{'='*65}\n")

    # ── Initial state ──
    best_score    = get_best_score()
    baseline      = load_strategy(args.strategy)
    iteration     = 0
    kept_variants = 0

    print(f"Starting best score: {best_score:.1f}/100")

    while iteration < args.max_iters:
        print_header(iteration, best_score, args.target_score)

        if best_score >= args.target_score:
            print(f"Target score {args.target_score} reached! Stopping.")
            break

        # ── Determine focus category ──
        focus = args.focus
        if args.auto_focus and not focus:
            focus = suggest_focus_category()
            print(f"Auto-focus: {focus}")

        # ── Generate variants ──
        history = load_mutation_history()
        variants = generate_variants(
            baseline,
            n=args.variants,
            seed=args.seed,
            focus_category=focus,
            history=history,
        )

        if not variants:
            print("No new variants available (all candidates exhausted). Stopping.")
            break

        # ── Optional: add one semantic variant via local LLM ──
        if local_llm_ready:
            last_run_path = os.path.join(RUNS_DIR, f"iter{iteration - 1}_*/last_run_scores.json") \
                            if iteration > 0 else "experiment_reports/last_run_scores.json"
            # Use global last_run_scores.json as fallback
            last_run_fallback = os.path.join(RUNS_DIR, "last_run_scores.json")
            lrp = last_run_fallback if os.path.exists(last_run_fallback) \
                  else "experiment_reports/last_run_scores.json"
            print(f"  [local-llm] generating semantic variant from {lrp}...")
            try:
                sem_result = generate_semantic_variant(baseline, lrp)
                if sem_result:
                    sem_content, sem_mutation = sem_result
                    import hashlib
                    base_hash = hashlib.sha1(baseline.encode()).hexdigest()[:10]
                    sem_id    = f"v_semantic_{sem_mutation['knob']}_{base_hash[:8]}"
                    meta_comment = (
                        f"<!-- VARIANT METADATA\n"
                        f"variant_id: {sem_id}\n"
                        f"base_hash: {base_hash}\n"
                        f"mutation: {sem_mutation['knob']} (semantic LLM edit)\n"
                        f"model: {sem_mutation.get('model', 'phi3:mini')}\n"
                        f"-->\n\n"
                    )
                    sem_variant = StrategyVariant(
                        variant_id=sem_id,
                        base_strategy_hash=base_hash,
                        mutation=sem_mutation,
                        content=meta_comment + sem_content,
                        generated_at=datetime.now().isoformat(),
                    )
                    variants.append(sem_variant)
                    print(f"  [local-llm] added semantic variant: {sem_id[:40]}")
            except Exception as e:
                print(f"  [local-llm] semantic variant failed: {e}")

        print(f"\nGenerated {len(variants)} variant(s):")
        # Write to disk and attach path
        for v in variants:
            v._file_path = variant_to_file(v, VARIANTS_DIR)
            mut = v.mutation
            print(f"  {v.variant_id[:32]}  [{mut['knob']}: {mut['from']} -> {mut['to']}]")

        if args.dry_run:
            print(f"\nDry run — variants written to {VARIANTS_DIR}/. Stopping.")
            break

        # ── Run experiments ──
        print(f"\nRunning experiments (parallel={args.parallel})...")
        results = run_parallel_variants(
            variants,
            cases_file=args.cases,
            best_score=best_score,
            timeout_per_case=args.timeout,
            max_workers=args.parallel,
            enrich_pubmed=args.enrich_pubmed,
            iteration=iteration,
        )

        # ── Evaluate results ──
        winner = results[0] if results else None
        discarded = results[1:] if len(results) > 1 else []

        decision   = "discard"
        note       = ""
        new_best   = best_score

        if winner and winner["mean_score"] >= best_score + KEEP_THRESHOLD:
            decision = "keep"
            new_best = winner["mean_score"]
            note     = (f"Variant {winner['variant_id'][:20]} improved by "
                        f"{winner['mean_score'] - best_score:.1f} pts "
                        f"(knob: {winner['mutation']['knob']})")
            # Apply winner to strategy.md
            with open(winner["variant_path"], "r", encoding="utf-8") as f:
                winning_content = f.read()
            # Strip metadata comment block before saving as canonical strategy
            clean = winning_content
            if clean.startswith("<!--"):
                end_comment = clean.find("-->")
                if end_comment != -1:
                    clean = clean[end_comment + 3:].lstrip("\n")
            atomic_write_strategy(clean, args.strategy)
            baseline  = clean
            best_score = new_best
            kept_variants += 1
            print(f"\n  KEPT: {note}")
        else:
            top_score = winner["mean_score"] if winner else 0.0
            note = (f"Best variant scored {top_score:.1f}, "
                    f"threshold {best_score + KEEP_THRESHOLD:.1f}")
            print(f"\n  DISCARD: {note}")

        # ── Record outcomes in mutation history ──
        for r in results:
            # Find the matching StrategyVariant object
            v_match = next((v for v in variants if v.variant_id == r["variant_id"]), None)
            if v_match:
                record_mutation_outcome(v_match, r["mean_score"], r["decision"])

        # ── Log iteration ──
        log_record = {
            "timestamp":       datetime.now().isoformat(),
            "iteration":       iteration,
            "variants_tested": len(results),
            "best_variant_id": winner["variant_id"] if winner else None,
            "mean_score":      winner["mean_score"] if winner else 0.0,
            "prev_best":       best_score if decision == "discard" else (best_score - (winner["mean_score"] - best_score)),
            "decision":        decision,
            "mutation_desc":   (f"{winner['mutation']['knob']}: "
                                f"{winner['mutation']['from']} -> {winner['mutation']['to']}"
                                if winner else "none"),
            "note":            note,
            "discarded_ids":   [r["variant_id"] for r in discarded],
        }
        append_log(log_record)

        iteration += 1

    # ── Final summary ──
    print(f"\n{'='*65}")
    print(f"  LOOP COMPLETE")
    print(f"  Iterations run:   {iteration}")
    print(f"  Variants kept:    {kept_variants}")
    print(f"  Final best score: {best_score:.1f}/100")
    print(f"  Target score:     {args.target_score}/100")
    print(f"  Log:              {LOG_FILE}")
    print(f"{'='*65}\n")

    # Exit 0 if target reached, 1 otherwise
    sys.exit(0 if best_score >= args.target_score else 1)


if __name__ == "__main__":
    main()
