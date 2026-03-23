# AutoResearch Loop — Agent Instructions

You are an autonomous research optimization agent. Your job is to iteratively
improve cancer research report quality by editing `strategy.md` and measuring
the results.

## The Loop

```
while true:
    1. Read current strategy.md
    2. Make ONE targeted edit to strategy.md (your hypothesis)
    3. Run: python run_experiment.py
    4. Read results.tsv for the new mean_score
    5. If mean_score >= best_score + 1.0 → KEEP (strategy.md stays)
       If mean_score < best_score + 1.0  → DISCARD (revert strategy.md)
    6. Log your reasoning
    7. Go to 1
```

## Rules

### What You CAN Edit
- **`strategy.md`** — this is the ONLY file you may modify

### What You CANNOT Edit
- `evaluate.py` — the scoring harness is fixed (like a test suite)
- `generate_cases.py` — the benchmark generator is fixed
- `benchmark_cases.json` — the test cases are fixed
- `run_experiment.py` — the experiment runner is fixed
- `cancer_research_scorer.py` — the structural validator is fixed
- `program.md` — these instructions are fixed (you can't change yourself)

### Edit Strategy
Make ONE change at a time. Good changes to try:

1. **Search query templates** — add synonyms, year ranges, specific journal names
2. **Search budget allocation** — shift searches toward underperforming tiers
3. **Source fetch priorities** — reorder what gets fetched first
4. **Rating calibration anchors** — tighten or loosen score boundaries
5. **Treatment inclusion criteria** — adjust thresholds
6. **Data density targets** — add fields to emphasize
7. **Output emphasis guidance** — change what gets highlighted
8. **Combination/supportive care guidance** — adjust minimum counts

### Keep/Discard Threshold
- **Keep** if: `new_mean_score >= best_mean_score + 1.0`
- **Discard** if: `new_mean_score < best_mean_score + 1.0`
- On discard, revert `strategy.md` to the previous version
- The +1.0 threshold prevents noise from causing false improvements

### How to Analyze Results
After each experiment:
1. Check which dimensions scored lowest (from the per-case evaluations)
2. Read the dimensional details to understand WHY scores are low
3. Target your next strategy.md edit at the weakest dimension
4. Avoid re-trying edits that were previously discarded

### Logging
After each iteration, note:
- What you changed in strategy.md
- The mean_score achieved
- Whether you kept or discarded
- What you plan to try next

### Baseline
The first run with the seed strategy.md establishes the baseline.
This score is your `best_score` — all future runs compare against it.

## Important
- Never stop the loop unless instructed by the user
- Never edit the evaluation criteria — the score must be an honest signal
- If stuck (3+ consecutive discards), try a bigger change or a different dimension
- The goal is to reach quality_score ≥ 80 on average across all benchmark cases
