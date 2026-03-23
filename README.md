# Cancer AutoResearch

**An open-source, AI-powered database of evidence-ranked cancer treatment plans — continuously improved by an autoresearch loop.**

Every report ranks treatments from standard of care through experimental therapies, scored on evidence level, survival benefit, safety, accessibility, and biomarker match. The loop runs 24/7 on donated compute, improving research quality through empirical score-driven optimization.

---

## What this is

- **A growing database** of structured cancer research reports — one per benchmark case, covering every major cancer type
- **An autoresearch loop** (Karpathy-style) that iteratively improves `strategy.md`, the AI's research instructions, by running experiments and keeping changes that measurably improve scores
- **A public query interface** (`database_api.py`) so anyone can ask plain-English questions and get answers grounded in the highest-scoring reports available

Currently active: **140 research reports** across Head & Neck (130) and Lung (10) cancers, mean score **82.4/100**.

---

## Quick start

```bash
git clone https://github.com/romeo111/cancer-autoresearch.git
cd cancer-autoresearch

# Query the existing database
python database_api.py ask "best treatment for MGMT-methylated GBM in elderly patient"

# Score an existing report
python evaluate.py experiment_reports/HN-001_report.json --verbose

# Run the autoresearch loop (improves strategy.md)
python auto_loop.py --cases benchmark_cases.json --target-score 92 --max-iters 20
```

No external dependencies. Pure Python stdlib — except `worker.py --mode claude` which requires `pip install anthropic`.

---

## How it works

```
benchmark_cases.json  ──►  run_experiment.py  ──►  *_report.json
                                                         │
strategy.md  ──────────────────────────────────────────► │
(agent edits this)                                       │
                                                         ▼
                                                   evaluate.py
                                                   (0–100 score)
                                                         │
                                                         ▼
                                                   auto_loop.py
                                              keeps if Δ ≥ 2.5 pts
```

The loop is based on [Karpathy's autoresearch approach](https://github.com/karpathy/llm.c): the "program" (`strategy.md`) is the thing being optimized, not the model weights. Every iteration is a hypothesis test.

### Rating system

Each treatment is scored across 5 dimensions:

| Dimension | Weight | What it measures |
|---|---|---|
| Evidence Level | 30% | RCT phase, sample size, journal quality |
| Survival Benefit | 30% | OS/PFS delta magnitude vs. control |
| Accessibility | 15% | FDA/EMA approval status |
| Safety Profile | 15% | Toxicity grade and manageability |
| Biomarker Match | 10% | How well the patient's markers fit |

---

## Contribute

**→ [HOW_TO_CONTRIBUTE.md](HOW_TO_CONTRIBUTE.md)** — start here, no engineering background required

**→ [CONTRIBUTING.md](CONTRIBUTING.md)** — technical guide (git workflow, CI, autoresearch loop)

**→ [docs/ADDING_CANCER_TYPES.md](docs/ADDING_CANCER_TYPES.md)** — how to add a new cancer type end-to-end

**→ Open an Issue** to request research on a specific cancer type — a contributor will pick it up

### Three ways to help

| Role | What you do | Requirements |
|---|---|---|
| **GPU Donor** | Run `worker.py --mode local` | Any GPU ≥4 GB VRAM, Ollama |
| **API Subscriber** | Run `worker.py --mode claude` | Anthropic API key |
| **Clinician / Reviewer** | Correct errors, review reports | Medical knowledge |

---

## Database structure

```
research_db/
├── INDEX.json                    ← master status tracker
├── carcinomas/                   ← breast, lung, colorectal, etc.
├── sarcomas/                     ← osteosarcoma, GIST, Ewing, etc.
├── leukemias/                    ← AML, ALL, CML, CLL
├── lymphomas/                    ← DLBCL, Hodgkin, follicular, etc.
├── myelomas/                     ← multiple myeloma, Waldenström
└── cns_tumors/                   ← GBM, astrocytoma, medulloblastoma, etc.

experiment_reports/               ← 140 active reports (HN + lung)
```

Full taxonomy: [docs/DATABASE_GUIDE.md](docs/DATABASE_GUIDE.md)
JSON schema: [docs/SCHEMA_REFERENCE.md](docs/SCHEMA_REFERENCE.md)

---

## Files

| File | Purpose |
|---|---|
| `strategy.md` | Research instructions — the thing the loop optimizes |
| `evaluate.py` | Quality scorer (0–100) — never modified by the loop |
| `auto_loop.py` | Autoresearch loop — proposes, tests, keeps/discards variants |
| `worker.py` | Research worker — Claude API or local LLM mode |
| `run_experiment.py` | Runs research on a benchmark set, collects scores |
| `generate_cases.py` | Generates benchmark cases for a cancer type/demographic |
| `clinicaltrials_client.py` | ClinicalTrials.gov v2 API client |
| `pubmed_client.py` | PubMed/NCBI E-utilities client |
| `local_llm.py` | Ollama integration (llama3.2:3b + phi3:mini) |
| `database_api.py` | Query interface across all reports |
| `server.py` | Optional: real-time multi-worker cluster coordination |

---

## Medical disclaimer

**This project is for research and educational purposes only.**

Reports are generated by automated AI systems, not reviewed by licensed medical professionals, and must not be used as the sole basis for any clinical decision. Always consult a qualified oncologist.

---

## License

Code: MIT License
Research reports: CC BY 4.0
