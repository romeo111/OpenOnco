# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cancer AutoResearch is a Karpathy-style autoresearch loop that produces evidence-ranked cancer treatment reports. The "program" being optimized is **`strategy.md`** (the research instructions), not model weights. Each iteration mutates `strategy.md`, runs benchmark cases, scores outputs on a fixed 0–100 rubric, and keeps the variant only if mean score improves by ≥ `KEEP_THRESHOLD` (currently **2.5** — see `auto_loop.py`).

This is **not** a traditional app. It is a prompt + Python orchestration system. Reports are JSON/Markdown artifacts; the "product" is the database of scored reports plus the continuously-improving `strategy.md`.

## Architecture

Three layers, loosely coupled:

### 1. Single-machine loop (self-contained)
```
strategy.md ──► run_experiment.py ──► *_report.json ──► evaluate.py ──► score
      ▲                                                                   │
      └──── auto_loop.py (keeps variant iff Δ ≥ 2.5) ◄─────────────────── ┘
```
- `auto_loop.py` — automated driver. Generates variants via `strategy_optimizer.py`, runs experiments in parallel, keeps the best if it beats the current best by ≥ 2.5. Writes `auto_loop.log` (NDJSON), `mutation_history.json`, and appends to `results.tsv`.
- `strategy_optimizer.py` — parameterized mutation engine. Exposes "knobs" (e.g., `tier1_searches`, `search_budget`) and tracks proven losers in `mutation_history.json` so they are not retried.
- `run_experiment.py` — runs all (or a single) benchmark case, writes reports to `experiment_reports/runs/<variant>/`, scores each, returns keep/discard signal.
- `program.md` — describes the *manual* version of this loop for reference. The automated path is `auto_loop.py`; `program.md` is not executed directly.

### 2. Distributed platform (optional, for multi-node runs)
```
Workers (local LLM or Claude API) ◄──HTTP──► server.py (orchestrator)
                                               │
                                               ├── assigns jobs (case + strategy_hash)
                                               ├── collects scored submissions
                                               └── promotes strategy variant when
                                                   Δ ≥ 2.5 across ≥ 3 validations
```
- `server.py` — stdlib-only HTTP orchestrator. SQLite-backed. Promotes a variant when ≥ 3 independent workers validate an improvement.
- `worker.py` — pulls jobs, runs research, submits results. Two modes: `--mode local` (Ollama via `local_llm.py`) or `--mode claude` (requires `pip install anthropic` and `ANTHROPIC_API_KEY`). Simple cases (complexity ≤ 4) are routed to local workers; complex cases to Claude workers.
- Constants live at the top of each file — `PROMOTION_MIN_VALIDATIONS`, `PROMOTION_MIN_SCORE_DELTA`, `SIMPLE_CASE_COMPLEXITY_MAX` in `server.py`; retry/backoff settings in `worker.py`.

### 3. Database + query layer
There are **two distinct databases** — do not confuse them:

| Path | Kind | Owner | Purpose |
|---|---|---|---|
| `research_db/` (directory) | JSON files on disk, categorized (`carcinomas/`, `sarcomas/`, `leukemias/`, `lymphomas/`, `myelomas/`, `cns_tumors/`) with `INDEX.json` master | `database_api.py` | Public, file-based; queried in plain English via `database_api.py ask "..."` |
| `research.db` (file) | SQLite | `research_db.py` | Normalized tables (treatments, trials, sources, evaluations, board_reviews, iterations) for analytics/export |

- `database_api.py` — user-facing query tool over the filesystem `research_db/`. Supports `search`, `ask`, `stats`, `get-best`, `compare`. Works without the server running.
- `research_db.py` — ingest/export CLI for the SQLite mirror.

### Supporting components
- `evaluate.py` — **the fixed scorer**. Never modified by the loop. Imports `validate_report` and `compute_composite` from `cancer_research_scorer.py` — keep those signatures compatible.
- `cancer_research_scorer.py` — JSON validator and re-scorer for the report schema defined in `output_template.md`. Schema/validator must stay in sync.
- `SKILL.md` + `output_template.md` — the skill definition and report contract (9 sections, JSON schema). The research worker prompt is built from `SKILL.md` + `strategy.md`.
- `virtual_tumor_board.py` — 5 adversarial virtual oncologists (Evidence, Aggressor, Guardian, Precision, Frontier) for qualitative review. Three modes: heuristic (no LLM), full 4-round debate prompt, quick review prompt.
- `clinicaltrials_client.py`, `pubmed_client.py` — stdlib HTTP clients for ClinicalTrials.gov v2 API and PubMed E-utilities. Used by strategy tiers to enrich reports with real trial IDs and PMIDs.
- `local_llm.py` — Ollama integration (llama3.2:3b, phi3:mini). Used by `worker.py --mode local` and `local_task_generator.py`.
- `local_task_generator.py` — GPU-powered gap analysis. Runs local LLM over existing reports to identify fixable data gaps, then emits targeted Claude API re-eval prompts into `tasks/`.
- `generate_cases.py` — benchmark case generator. Produces `benchmark_cases_*.json`.

### Fine-tuning pipeline (optional, RTX 5050 target)
- `prepare_finetune_data.py` — builds ChatML training pairs from scored reports into `finetune_data/train_chatml.jsonl` and `val_chatml.jsonl`.
- `finetune.py` — QLoRA fine-tune via Unsloth (targets llama3.2:3b / phi3:mini for 8 GB VRAM; 7B+ won't fit). Can export to GGUF for Ollama.
- `eval_finetuned.py` — runs the fixed scorer against the fine-tuned model's outputs.
- Requires `pip install "unsloth[colab-new]" trl peft accelerate bitsandbytes`.

## Dependencies

- **Default**: Python stdlib only.
- **`worker.py --mode claude`**: `pip install anthropic`, needs `ANTHROPIC_API_KEY`.
- **`worker.py --mode local`, `local_task_generator.py`, `local_llm.py`**: Ollama running on `http://localhost:11434` with `llama3.2:3b` and/or `phi3:mini` pulled.
- **Fine-tuning pipeline**: Unsloth + trl + peft + accelerate + bitsandbytes (see above).

(The old CLAUDE.md claimed "no external dependencies" — that is only true for the core loop, not worker/claude mode or fine-tuning.)

## Common commands

### Run the loop (automated)
```bash
python auto_loop.py                                              # defaults
python auto_loop.py --target-score 92 --max-iters 20
python auto_loop.py --cases benchmark_cases_hn3.json --parallel 3 --variants 3
python auto_loop.py --enrich-pubmed --focus search_budget       # target a specific knob
python auto_loop.py --dry-run                                    # generate variants only
```

### Run experiments directly
```bash
python run_experiment.py                       # all benchmark cases
python run_experiment.py --single-case HN-003  # one case
python run_experiment.py --dry-run             # generate prompts only
```

### Score a report
```bash
python evaluate.py report.json --verbose
python evaluate.py report.json --score-only
python cancer_research_scorer.py input.json --validate-only
```

### Distributed mode
```bash
python server.py --port 8080 --host 0.0.0.0 --db-path orchestrator.db
python worker.py --server http://<host>:8080 --mode local
python worker.py --server http://<host>:8080 --mode claude --max-jobs 10
```

### Query the database
```bash
python database_api.py ask "best treatment for MGMT-methylated GBM in elderly patient"
python database_api.py search --category cns_tumors --min-score 85
python database_api.py stats
python database_api.py get-best "triple negative breast cancer"
python research_db.py query dashboard             # SQLite-backed analytics
python research_db.py export treatments --format csv
```

### Generate benchmark cases
```bash
python generate_cases.py --site "throat and neck" --age 45 --sex male --count 10
```

### Virtual tumor board
```bash
python virtual_tumor_board.py report.json --heuristic
python virtual_tumor_board.py report.json --generate-prompt       # 4-round debate prompt
python virtual_tumor_board.py report.json --case benchmark_cases.json --case-id HN-001
```

### Fine-tune (RTX 5050)
```bash
python prepare_finetune_data.py                   # builds finetune_data/*.jsonl
python finetune.py --dry-run                      # verify data + model init
python finetune.py                                # actual QLoRA run
python finetune.py --export-gguf --model-path models/cancer_llama3_v1
python eval_finetuned.py --model-path models/cancer_llama3_v1
```

## Quality score rubric (fixed — in `evaluate.py`)

| Dimension | Max | Measures |
|---|---|---|
| Structural Integrity | 15 | JSON validates, all sections present, min counts |
| Evidence Depth | 25 | OS/PFS/ORR/HR/sample-size data density |
| Tier Coverage | 10 | All 6 research tiers represented |
| Rating Calibration | 15 | Score spread, range, rationale completeness |
| Source Quality | 15 | URL count, validity, type diversity |
| Clinical Relevance | 10 | Biomarker specificity, side effects, trial status |
| Combo/Supportive | 10 | Combination strategies + supportive care depth |

## Rating composite (in `cancer_research_scorer.py`)

Weighted composite 1–10: Evidence 30% · Survival 30% · Accessibility 15% · Safety 15% · Biomarker 10%. Clamped to [0, 10], rounded to 1 decimal. The scorer re-sorts treatments descending by composite and reassigns ranks.

## Critical invariants

- **`strategy.md` is the only file the loop may rewrite.** All other infrastructure is fixed.
- **`evaluate.py` and the 7-dimension rubric are a fixed contract** — changing them invalidates historical scores in `results.tsv`. Don't.
- **`results.tsv` is append-only.** Never delete or edit prior rows; comparability depends on it.
- **Schema ↔ scorer sync**: `output_template.md` defines the JSON schema; `cancer_research_scorer.py` validates against it; `evaluate.py` imports from the scorer. If you change the schema you must update both.
- **`KEEP_THRESHOLD = 2.5`** in `auto_loop.py`. Raising it makes the loop more conservative; lowering it admits noise.
- Reports must include the medical disclaimer — research/educational use only, not clinical advice.

## File layout pointers (for quick orientation)

- `experiment_reports/` — per-case reports from the main run; `runs/<variant>/` — per-variant isolated outputs from `auto_loop.py`; `variants/` — generated strategy variant files.
- `research_db/` (directory) vs. `research.db` (SQLite file) — see the Database section above; they are separate systems.
- `tasks/` — re-eval prompts emitted by `local_task_generator.py`.
- `finetune_data/` — ChatML JSONL for the fine-tune pipeline.
- `docs/` — `ARCHITECTURE.md`, `DATABASE_GUIDE.md`, `SCHEMA_REFERENCE.md`, `ADDING_CANCER_TYPES.md` for deeper dives.
- `benchmark_cases*.json` — multiple fixed test sets (HN, HN2, HN3, lung, tongue_neck). Do not modify between loop iterations for a given run.
