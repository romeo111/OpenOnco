# Contributing to Cancer AutoResearch

**No server required.** GitHub is the coordination layer. You clone, run, and submit reports via pull request. The CI bot scores them automatically.

---

## Three ways to contribute

### 1. Run Research (GPU Donors + API Subscribers)

You generate new cancer research reports and submit them to the database.

**Option A — Claude API (highest quality)**
```bash
# Install the Anthropic SDK
pip install anthropic

# Run worker in Claude mode (uses claude-opus-4-6 by default)
python worker.py --mode claude --api-key sk-ant-...
```

**Option B — Local LLM via Ollama (free, no API key)**
```bash
# Install ollama: https://ollama.com
ollama pull llama3.2:3b   # fast pre-scorer
ollama pull phi3:mini      # strategy mutation proposals

# Run worker in local mode
python worker.py --mode local
```

**Option C — Manual research**
Write the report JSON yourself following `docs/SCHEMA_REFERENCE.md`.

---

### 2. Add a New Cancer Type

Open a GitHub Issue using the **New Cancer Type** template, then:

```bash
# 1. Create the folder structure
mkdir -p research_db/carcinomas/gastric/reports

# 2. Write benchmark cases (see docs/ADDING_CANCER_TYPES.md)
#    Copy the template from that guide, fill in 8-10 cases
nano research_db/carcinomas/gastric/benchmark_cases.json

# 3. Generate prompts for each case
python run_experiment.py \
  --cases research_db/carcinomas/gastric/benchmark_cases.json \
  --reports-dir research_db/carcinomas/gastric/reports

# 4. Run research for each prompt (open each _prompt.md and execute the skill)

# 5. Score locally before submitting
python evaluate.py research_db/carcinomas/gastric/reports/GAS-001_report.json --verbose
```

Target: mean score ≥ 80/100 before opening a PR.

---

### 3. Fix a Report Error

Open a GitHub Issue using the **Report Correction** template. Or:

1. Edit the JSON directly
2. Re-run `python cancer_research_scorer.py <file> --validate-only`
3. Open a PR — CI re-scores automatically

---

## Submitting a pull request

### Branch naming

```
reports/BRE-001-triple-negative-breast
reports/GAS-001-through-010-gastric-adenocarcinoma
fix/HN-001-wrong-os-data
new-type/gastric
```

### PR checklist

The PR template fills in automatically. The key requirements:

- [ ] All reports at correct path: `research_db/{category}/{subtype}/reports/{CASE_ID}_report.json`
- [ ] Each report scores ≥ 80/100 (CI bot enforces this)
- [ ] `case_id` in `report_metadata` matches the benchmark case ID
- [ ] All treatments have `intent` field set
- [ ] At least 10 sources with URLs

### CI scoring

When you open a PR, the **Score Research Reports** GitHub Action runs automatically:

1. Detects all `*_report.json` files changed vs. `main`
2. Runs `evaluate.py` on each
3. Posts a score table as a PR comment
4. Blocks merge if any report is below 80/100

You don't need to push a perfect score — improve based on CI feedback and re-push.

---

## Local development

```bash
# Clone
git clone https://github.com/YOUR_ORG/cancer-autoresearch.git
cd cancer-autoresearch

# No pip install needed — all tools use Python stdlib only
# (worker.py in Claude mode requires: pip install anthropic)

# Validate your Python version (3.9+ required)
python --version

# Dry run — verifies everything is importable
python auto_loop.py --dry-run

# Score an existing report
python evaluate.py experiment_reports/HN-001_report.json --verbose
```

---

## Autoresearch loop (advanced)

The loop iteratively improves `strategy.md` — the research instructions the AI follows.

```bash
# Basic loop — 20 iterations, target 92/100, 3 parallel variants
python auto_loop.py \
  --cases research_db/carcinomas/head_and_neck/benchmark_cases.json \
  --target-score 92 \
  --max-iters 20 \
  --parallel 2 \
  --variants 3

# With local LLM semantic mutations (requires ollama + phi3:mini)
python auto_loop.py \
  --cases research_db/carcinomas/head_and_neck/benchmark_cases.json \
  --target-score 92 \
  --local-llm \
  --auto-focus
```

A strategy variant is promoted to `strategy.md` only if it scores **≥ 2.5 points above the current best** — this prevents noise-floor improvements from polluting the main strategy.

If you discover a strategy improvement, open a PR that includes:
- Updated `strategy.md`
- `results.tsv` showing the improvement trajectory
- At least 3 re-generated reports scored under the new strategy

---

## Clinical accuracy

This database is for **research and educational purposes only**. All reports carry a medical disclaimer. Clinical contributions are welcome but must be accurate:

- Cite sources for all treatment data (OS, HR, p-values)
- Use real trial names and NCT IDs
- Do not fabricate or extrapolate survival statistics
- Flag uncertain data with appropriate caveats in `rationale` fields

If you are a clinician or researcher, your reviews of existing reports are invaluable — use the **Report Correction** issue template.

---

## Directory map

```
cancer_autoresearch/
├── research_db/            ← Cancer research database (contribute reports here)
│   ├── INDEX.json          ← Master status tracker
│   ├── carcinomas/
│   ├── sarcomas/
│   ├── leukemias/
│   ├── lymphomas/
│   ├── myelomas/
│   └── cns_tumors/
├── experiment_reports/     ← Legacy location (head & neck, lung)
├── docs/
│   ├── DATABASE_GUIDE.md   ← Database taxonomy and structure
│   ├── ADDING_CANCER_TYPES.md  ← How to add a new cancer type
│   ├── SCHEMA_REFERENCE.md ← Full JSON schema reference
│   └── ARCHITECTURE.md     ← System design and open-source model
├── strategy.md             ← Agent research instructions (auto-improved by loop)
├── evaluate.py             ← Quality scorer (0-100)
├── auto_loop.py            ← Autoresearch loop
├── worker.py               ← Research worker (local or Claude mode)
├── run_experiment.py       ← Experiment orchestrator
├── clinicaltrials_client.py ← ClinicalTrials.gov v2 API client
├── local_llm.py            ← Ollama integration (llama3.2:3b + phi3:mini)
├── database_api.py         ← Query interface across all reports
└── server.py               ← Optional: real-time cluster coordination server
```

---

## Questions?

Open a GitHub Issue with the label `question`. For clinical questions, tag a clinician reviewer if one is available.
