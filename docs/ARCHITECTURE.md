# Cancer AutoResearch — Open-Source Distributed Platform Architecture

## 1. Vision

Cancer AutoResearch began as a single-machine loop: generate a research report, score it, mutate
the strategy, repeat. The vision for open-sourcing it is to turn that loop into a **distributed
scientific mesh** where thousands of contributors — GPU donors, API subscribers, and curious
readers — collectively drive the quality of cancer treatment research toward the theoretical maximum.

When fully open-sourced, this platform will:

- Maintain a continuously-improving, publicly-auditable database of evidence-ranked treatment plans
  covering every major cancer type, updated automatically as new trials and approvals emerge
- Run the Karpathy autoresearch loop across a global fleet of heterogeneous compute nodes,
  converging on the best possible research strategy through empirical score-driven optimization
- Expose a public query API so patients, caregivers, and clinicians can ask plain-English questions
  and receive answers grounded in the highest-scoring research reports available
- Operate with no single point of control — strategy changes require multi-node consensus,
  database writes are append-only, and every score is reproducible from the public evaluation harness

The guiding principle is **empirical self-improvement**: the system gets better not by hand-tuning
prompts, but by running experiments, measuring outcomes, and promoting changes that measurably
improve quality scores — exactly the way training loss guides a neural network.

---

## 2. The Karpathy Autoresearch Loop — Distributed Form

### The Analogy

Andrej Karpathy's autoML loop optimizes a training script (`train.py`) by treating validation
bits-per-byte (`val_bpb`) as the objective. The loop proposes edits to `train.py`, runs training,
measures `val_bpb`, keeps improvements, discards regressions. The "weights" are the model
parameters; the "training log" is the history of edits that improved `val_bpb`.

This project mirrors that structure exactly:

| Karpathy's Loop           | Cancer AutoResearch                          |
|---------------------------|----------------------------------------------|
| `train.py`                | `strategy.md` — the agent-editable "program" |
| Model weights             | The research reports (outputs of the program) |
| `val_bpb` (lower = better) | `quality_score` (0–100, higher = better)    |
| Training run              | `run_experiment.py` on benchmark cases       |
| Optimizer proposes edits  | `strategy_optimizer.py` mutates 13 "knobs"  |
| Edit accepted if val_bpb drops | Variant kept if score improves by ≥2.5 |
| Training log              | `auto_loop.log` + strategy version history   |

### Why This Works

`strategy.md` is not just a config file — it is the **entire research algorithm**. It encodes:
- How many web searches to perform per tier
- Which sources to prioritize
- How to calibrate treatment ratings (evidence levels, survival benefit anchors)
- What mandatory fields every treatment entry must include
- How to rank curative vs. palliative treatments

Mutating `strategy.md` is therefore equivalent to mutating an optimizer's hyperparameters or
architecture. The quality score (`quality_score` from `evaluate.py`) is the objective function.
The loop converges toward the strategy configuration that maximizes mean quality score across
the fixed benchmark cases — which are the held-out "validation set."

### The Distributed Extension

On a single machine, the loop is serial: generate variant → run → score → keep/discard. The
distributed form parallelizes this across N worker nodes:

```
Iteration t:
  Orchestrator broadcasts strategy_v(t) to all workers
  Each worker pulls a job: {cancer_type, benchmark_case, strategy_hash}
  Workers run research + score in parallel
  Workers submit results: {score, report_json, quality_dimensions}
  Orchestrator aggregates:
    If strategy_variant_X improves mean_score by ≥2.5 across ≥3 independent workers:
      Promote variant_X to strategy_v(t+1)
      Log promotion in strategy version history
    Else:
      Discard variant_X, try next mutation
```

This is stochastic gradient descent in strategy-space, parallelized. Each worker is an
independent sample from the score distribution. Requiring ≥3 independent confirmations
before promotion provides noise resistance equivalent to multiple validation runs.

### The "Loss Function" is Mean Quality Score

The objective: **maximize mean `quality_score` across all benchmark cases**.

`evaluate.py` scores reports on 7 dimensions (max 100 total):
- Structural Integrity (15): JSON validity, sections present, treatment count
- Evidence Depth (25): OS/PFS/ORR/HR data density — the highest-weighted dimension
- Tier Coverage (10): All 6 research tiers represented
- Rating Calibration (15): Score spread, evidence-phase consistency, rationale completeness
- Source Quality (15): URL count, validity, type diversity
- Clinical Relevance (10): Biomarker specificity, side effects, trial IDs, intent fields
- Combo/Supportive Coverage (10): Combination strategies and supportive care depth

A strategy variant that lifts mean quality_score by 2.5 points represents a measurable,
generalizable improvement in research quality — not noise.

---

## 3. Three Participation Tiers

### Tier 1: GPU Donors

**Profile**: Have a CUDA-capable GPU (RTX 3070+, 8+ GB VRAM), willing to contribute compute.

**What they run**: `worker.py --mode local`, which uses `ollama` to run a capable local LLM
(llama3.1:70b quantized, or best available for their VRAM). The local LLM generates research
reports from the case prompt + current strategy.md.

**What they contribute**: Research reports for assigned benchmark cases, quality scores, and
occasionally strategy mutation proposals (every 5 jobs, using phi3:mini or similar to propose
a targeted edit to the weakest-scoring strategy section).

**What they receive**: Compute credits accumulate with each scored job submitted. Credits unlock
read access to premium reports (those generated by Claude API workers, which tend to score higher).
The exchange rate: 1 validated benchmark job = 10 read credits. A premium report costs 5 credits.

**Hardware requirements**:
- VRAM: 8 GB minimum (llama3.2:3b), 24 GB recommended (llama3.1:70b Q4)
- RAM: 16 GB minimum
- Storage: 20 GB for models + database cache
- OS: Linux/macOS/Windows with CUDA or Metal support

**Software setup**:
```bash
pip install cancer-autoresearch-worker
ollama pull llama3.1:70b   # or llama3.2:3b for smaller GPUs
worker.py --server https://autoresearch.example.org --mode local
```

### Tier 2: API Subscribers

**Profile**: Have an Anthropic API key, willing to spend API credits for research generation.

**What they run**: `worker.py --mode claude`, which calls `claude-opus-4-6` via the Anthropic API
to generate full research reports. Claude's reports consistently score 15–25 points higher than
local LLM reports because Claude can: (a) synthesize complex multi-source evidence, (b) correctly
populate all mandatory JSON fields, and (c) apply nuanced treatment ranking rules.

**What they contribute**: High-quality research reports that raise the floor of the database.
Their jobs are preferentially assigned to complex cases (rare histologies, multiple molecular
markers, poor performance status) where local LLM quality degrades most.

**What they receive**: Full database access — all reports, all scores, all strategy history.
The ability to run private research queries against the full 41-cancer-type database. Priority
job assignment for cancer types not yet covered.

**Cost estimate**: Approximately $0.15–0.40 per research report using claude-opus-4-6 at current
pricing. A full 10-case benchmark run costs ~$2–4. This is competitive with journal access fees
for equivalent clinical literature.

**Setup**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
pip install cancer-autoresearch-worker anthropic
worker.py --server https://autoresearch.example.org --mode claude
```

### Tier 3: Readers / Consumers

**Profile**: Patients, caregivers, clinicians, researchers — anyone who needs treatment information.

**What they access**: The public query API (`database_api.py`) to:
- Search reports by cancer type, stage, molecular markers
- Ask plain-English questions about treatment options
- Get ranked treatment recommendations from the best available report
- Compare two cancer types side-by-side
- View database statistics and coverage

**Public tier limits**: 50 queries per day per IP, reports capped at quality_score ≥ 60,
full JSON only accessible with a free account. Raw report downloads require Tier 1/2 access.

**Access model**: No payment required for basic access. Create a free account to increase limits
and receive notifications when a cancer type's best score improves.

---

## 4. System Architecture

### Components

#### Orchestrator Server (`server.py`)

The central coordination node. Runs on a single server (or replicated behind a load balancer).
Responsibilities:
- Maintains the canonical `strategy.md` — the current best version
- Manages the job queue: which (cancer_type, case_id, strategy_hash) triples need to be run
- Authenticates workers and tracks their modes (local vs. claude)
- Aggregates submitted scores and reports
- Evaluates strategy promotion criteria
- Maintains strategy version history (append-only, never delete)
- Serves the public query API
- Provides leaderboard rankings

Implemented with: Python stdlib `http.server` + `sqlite3`. No external dependencies.
Persistence: single SQLite file (`orchestrator.db`).

#### Worker Clients (`worker.py`)

Stateless compute nodes that connect to the orchestrator. Each worker:
1. Registers its mode (local/claude) and hardware info
2. Fetches the canonical strategy
3. Pulls a job from the queue
4. Runs research (local LLM or Claude API)
5. Scores the result locally with `evaluate.py`
6. Submits result to orchestrator
7. Loops; proposes mutations every 5 jobs

Workers are designed to be ephemeral — they can crash, reconnect, or be killed at any time.
Jobs not completed within a timeout window are re-queued automatically.

#### Shared Database

Two layers:
- **SQLite (`orchestrator.db`)**: job queue, worker registry, score aggregation, strategy history
- **Research DB (`research_db/`)**: the actual report files, organized by cancer category/type

Reports are written by workers after job completion. The SQLite layer tracks which reports exist,
their quality scores, and which strategy version generated them.

#### Query API

Served by the orchestrator at `/database/search` and `/database/ask`.
Also available as a standalone CLI (`database_api.py`) that reads directly from `research_db/`
without needing the server running — useful for local use.

---

## 5. The Distributed Karpathy Loop Protocol

### Step-by-Step Protocol

```
1. INITIALIZATION
   Orchestrator loads canonical strategy.md (hash: H_canonical)
   Orchestrator populates job queue with all (case_id, strategy_hash) pairs
   Workers register, receive H_canonical

2. JOB ASSIGNMENT
   Worker requests job: GET /jobs/next
   Orchestrator selects next pending job, considering:
     - Worker mode (local → simpler cases, claude → complex cases)
     - Jobs not assigned to this worker in the last 5 iterations
     - Round-robin across pending cases
   Worker receives: {job_id, case_data, strategy_content, strategy_hash}

3. RESEARCH EXECUTION
   Worker builds prompt from case_data + strategy_content
   Worker runs research (ollama generate or anthropic.messages.create)
   Worker parses response into structured JSON report
   Worker scores report locally with evaluate.py

4. RESULT SUBMISSION
   Worker submits: POST /jobs/{job_id}/result
     {score, quality_dimensions, report_json, duration_s, worker_id}
   Orchestrator stores result in SQLite
   Orchestrator writes report JSON to research_db/{category}/{subtype}/reports/

5. STRATEGY MUTATION PROPOSAL
   Every 5 jobs, worker proposes a mutation:
     POST /mutations/propose
     {variant_content, mutation_desc, base_hash}
   Orchestrator assigns mutation_id, status=proposed

6. MUTATION VALIDATION
   Other workers validate proposed mutations (when idle):
     GET /mutations/next-to-validate
     Worker runs the variant on a fresh benchmark case
     POST /mutations/{id}/validate {score, quality_dimensions}

7. PROMOTION DECISION
   After each validation, orchestrator checks:
     Does this mutation have ≥3 validations?
     Is mean_score_with_mutation ≥ current_canonical_score + 2.5?
   If YES:
     Promote: INSERT INTO strategy_variants (hash, content, promoted_at, mean_score)
     Update canonical: current_canonical_hash = mutation.hash
     Broadcast new strategy to all active workers
     Mark all pending jobs with old hash as stale (re-queue with new hash)
   If NO (after ≥5 validations and score not improving):
     Mark mutation as rejected

8. STRATEGY VERSION HISTORY
   Every promoted strategy gets a version entry:
     {version, hash, parent_hash, mutation_desc, mean_score, promoted_at, worker_count}
   This is the "training log" — shows the evolution of strategy.md over time
   Old versions are never deleted; the full lineage is preserved
```

### Convergence Properties

- Each promotion requires multi-node consensus (≥3 workers), providing noise resistance
- The 2.5-point threshold prevents chasing noise (evaluate.py noise floor is ~1-2 points)
- Strategy versions are a DAG, not a linear chain — parallel experiments can propose
  mutations from the same base, and the first to achieve ≥3 validations wins
- The "training log" (strategy version history) enables analysis of which mutation types
  (search_budget, source_priority, rating_calibration, etc.) contributed most to score gains

---

## 6. Economics and Incentives

### Why Contributors Contribute

**GPU Donors**: The primary motivation is access to a high-quality medical research database
that would otherwise require either expensive API access or extensive manual literature review.
A GPU donor running 50 jobs/day earns 500 compute credits — enough for 100 premium report reads.
The database improves as more contributors participate, creating a positive feedback loop.

**API Subscribers**: Premium-quality reports generated by claude-opus-4-6 are worth having in the
database. An API subscriber who runs 20 complex cases creates significant value: those reports
become the benchmark against which local LLM reports are compared, and they populate the database
for cancer types that have no coverage yet. In exchange, subscribers get unrestricted database
access and the ability to commission research on specific cancer types.

**Readers**: Access to a continuously-updated, quality-scored treatment database with no paywall
for basic queries. Unlike static clinical guidelines, this database reflects the latest trial
data and is explicitly ranked by evidence quality.

### Credit System

```
Earning credits:
  1 validated benchmark job submitted           = 10 credits
  1 complex case completed (quality_score ≥ 75) = 20 credits
  1 strategy mutation validated by 3+ workers   = 50 credits
  1 strategy mutation promoted to canonical     = 200 credits

Spending credits:
  Read 1 premium report (quality_score ≥ 85)    = 5 credits
  Download full report JSON                      = 10 credits
  Run 1 custom query via /database/ask           = 2 credits
  Request research for new cancer type           = 100 credits
```

### Public Tier

Free forever:
- Browse database statistics and coverage
- View report summaries (treatment names, top-3 treatments, overall score)
- Limited /database/ask queries (10/day)
- Download reports with quality_score ≥ 60 for cancer types with ≥ 10 reports

---

## 7. Data Flow Diagram

```
                      ┌─────────────────────────────────────────────┐
                      │              ORCHESTRATOR SERVER             │
                      │                  (server.py)                 │
                      │                                              │
                      │  ┌──────────┐  ┌───────────┐  ┌─────────┐  │
                      │  │ Job Queue│  │ Strategy  │  │ Scores  │  │
                      │  │ (SQLite) │  │ History   │  │  DB     │  │
                      │  └──────────┘  │ (SQLite)  │  │(SQLite) │  │
                      │                └───────────┘  └─────────┘  │
                      └──────────┬──────────────────────────────────┘
                                 │  HTTP (stdlib http.server)
              ┌──────────────────┼──────────────────────┐
              │                  │                       │
    ┌─────────▼───────┐  ┌───────▼────────┐  ┌──────────▼──────────┐
    │  GPU DONOR      │  │  API SUBSCRIBER │  │  READER / CONSUMER  │
    │  worker.py      │  │  worker.py      │  │  database_api.py    │
    │  --mode local   │  │  --mode claude  │  │  or /database/ask   │
    │                 │  │                 │  │                     │
    │ ollama          │  │ anthropic API   │  │ GET /database/search│
    │ llama3.1:70b    │  │ claude-opus-4-6 │  │ GET /database/ask   │
    │                 │  │                 │  └─────────────────────┘
    │ PULL JOB        │  │ PULL JOB        │
    │ ↓               │  │ ↓               │
    │ RUN RESEARCH    │  │ RUN RESEARCH    │
    │ ↓               │  │ ↓               │
    │ SCORE (local)   │  │ SCORE (local)   │
    │ ↓               │  │ ↓               │
    │ SUBMIT RESULT   │  │ SUBMIT RESULT   │
    └────────┬────────┘  └────────┬────────┘
             │                    │
             └──────────┬─────────┘
                        │ POST /jobs/{id}/result
                        ▼
              ┌──────────────────┐
              │   research_db/   │
              │   (filesystem)   │
              │                  │
              │ carcinomas/      │
              │   head_and_neck/ │
              │     reports/     │
              │       *.json     │
              │   lung/          │
              │     reports/     │
              │ sarcomas/...     │
              │ leukemias/...    │
              └──────────────────┘

Strategy Evolution Flow:
  worker proposes mutation → POST /mutations/propose
  other workers validate  → POST /mutations/{id}/validate
  ≥3 validations + Δscore ≥ 2.5 → strategy promoted
  new strategy_hash broadcast → workers fetch GET /strategy
  old-hash jobs re-queued with new hash
```

---

## 8. Technology Stack

The guiding principle is **Python stdlib first, minimal dependencies**.

### Core Dependencies (zero external installs)
- `http.server` — HTTP server for orchestrator and query API
- `sqlite3` — all structured data (jobs, scores, strategy history, worker registry)
- `json` — report serialization and API payloads
- `hashlib` — strategy content hashing (SHA-1, SHA-256)
- `threading` — concurrent connection handling in the HTTP server
- `subprocess` — worker spawns evaluate.py as a subprocess for score isolation
- `urllib.request` — HTTP client for worker↔orchestrator communication
- `argparse` — CLI for all tools
- `datetime` — timestamps throughout
- `re` — strategy.md parsing in strategy_optimizer.py
- `dataclasses` — data structures in strategy_optimizer.py

### Optional Dependencies (feature-gated)
- `anthropic` — Tier 2 workers only: `pip install anthropic`
- `ollama` (via subprocess/HTTP) — Tier 1 workers: run `ollama serve` separately

### Infrastructure
- **Server**: Any VPS with Python 3.8+, 2 GB RAM, 100 GB storage for the database
- **Workers**: Any machine meeting the Tier 1 or Tier 2 hardware requirements
- **Database**: SQLite (single file) scales to millions of rows; no migration tooling needed
- **API**: Plain HTTP/1.1, JSON payloads — no WebSockets, no gRPC, no message queues

### Why Not FastAPI / Celery / Redis?

The design intentionally avoids modern async frameworks and task queue infrastructure because:
1. **Deployability**: Any Python 3.8+ install works; no `pip install` required for the server
2. **Auditability**: Every component is readable in a single sitting
3. **Portability**: Runs on a $5/month VPS, a Raspberry Pi, or a university compute cluster
4. **Contributor trust**: Open-source contributors can inspect the full codebase before running anything

---

## 9. Roadmap

### Phase 1: Local (Current State)

- [x] Single-machine autoresearch loop (`auto_loop.py`)
- [x] 7-dimension quality evaluator (`evaluate.py`)
- [x] Strategy variant generator with 13 mutation knobs (`strategy_optimizer.py`)
- [x] Local LLM integration via ollama (`local_llm.py`)
- [x] PubMed and ClinicalTrials.gov enrichment clients
- [x] Virtual tumor board (5 oncologist personas)
- [x] 41-cancer-type database scaffold (`research_db/`)
- [x] 130+ head & neck benchmark cases with reports
- [ ] `server.py` — orchestrator HTTP server
- [ ] `worker.py` — distributed worker client
- [ ] `database_api.py` — query interface

### Phase 2: Distributed (Next 6 Months)

- [ ] Deploy orchestrator to a public server
- [ ] Release worker client as `pip install cancer-autoresearch-worker`
- [ ] Implement compute credit system and worker authentication
- [ ] Add benchmark cases for 10 additional cancer types (lung, breast, colorectal, etc.)
- [ ] Implement strategy version DAG visualization
- [ ] Public leaderboard: top-scoring workers and strategy versions
- [ ] `/database/ask` natural language query endpoint with full test coverage
- [ ] Automated nightly re-runs: re-score existing reports against latest strategy version
- [ ] Report expiry: flag reports older than 180 days for regeneration (new trials may be published)

### Phase 3: Production (12–18 Months)

- [ ] Cover all 41 cancer types in the taxonomy
- [ ] Real-time update pipeline: monitor ClinicalTrials.gov and PubMed for new publications,
      trigger automatic re-research for affected cancer types
- [ ] Biomarker-specific sub-databases: e.g., EGFR-mutant NSCLC as a first-class entity
- [ ] Multi-language support: Spanish, French, Mandarin report summaries
- [ ] Clinician portal: structured access for oncologists with institutional authentication
- [ ] API versioning and SLA: stable endpoints for downstream applications
- [ ] Peer review integration: mechanism for oncologists to flag inaccurate treatments
      (flagged treatments trigger re-research with higher scrutiny)
- [ ] Foundation model fine-tuning: use accumulated high-quality reports as training data
      for a domain-specific cancer research model (open weights)

---

## 10. Privacy and Medical Disclaimer

### Privacy

**No personal health data is collected or stored.** The system works exclusively with:
- Anonymized or synthetic benchmark cases (generated by `generate_cases.py`)
- Published literature (PubMed abstracts, ClinicalTrials.gov public records)
- Model-generated research reports based on that literature

Workers submit only: quality scores, report JSON files derived from public literature, and
system metadata (worker_id, job timing, model used). No patient data leaves the worker machine.

Workers should not use real patient cases as benchmark inputs. The benchmark cases are
synthetic or de-identified representative cases for methodology development purposes.

### Medical Disclaimer

**This platform is a research and educational tool. It does not provide medical advice.**

All treatment recommendations generated by this system:
- Are derived from publicly available literature and may be incomplete or outdated
- Have not been reviewed or approved by medical boards or regulatory bodies
- Must not be used as the sole basis for any treatment decision
- Should be reviewed by qualified oncologists familiar with the individual patient's case

The quality scores produced by `evaluate.py` measure the **completeness and internal consistency**
of research reports, not the **clinical accuracy** of treatment recommendations. A report can
score 90/100 and still contain errors if the underlying LLM hallucinated evidence.

All platform outputs are labeled with a mandatory disclaimer:
> "FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY. This report was generated by an automated AI
> system and has not been reviewed by a licensed medical professional. Do not make treatment
> decisions based on this report without consulting a qualified oncologist."

### Open-Source Licensing

The codebase (excluding the research_db report files) is released under the MIT License.
Research reports in the database are released under CC BY 4.0 with attribution to the platform
and the original source publications cited in each report.

---

---

## 9. GitHub Mode vs. Server Mode

**TL;DR: No server required.** GitHub is sufficient for all coordination in the open-source model.

### GitHub Mode (default — no server needed)

```
Contributor → clone repo → run worker.py → PR report JSON → CI scores it → merged to main
```

| What you need | How it works |
|---|---|
| Coordination | GitHub PRs + Issues |
| Score enforcement | GitHub Actions (`score_reports.yml`) auto-scores every PR |
| Strategy promotion | PR to `strategy.md` requires human review + CI score evidence |
| Database growth | `git merge` — append-only, all history preserved |
| Query interface | `python database_api.py ask "..."` — runs locally on your clone |

This mode handles 99% of use cases:
- Solo researchers running the loop on their machine
- Teams of <20 contributors synchronizing via GitHub
- Public contributors submitting reports for specific cancer types
- Clinicians reviewing and correcting reports via Issues/PRs

### Server Mode (optional — for real-time clusters)

`server.py` is an **optional extension** for coordinating a live fleet of workers with no manual git steps:

```
Worker A ──┐
Worker B ──┼──► server.py ──► strategy promotion ──► sqlite3 DB
Worker C ──┘                   (≥3 confirmations,
                                Δscore ≥ 2.5)
```

Use server mode only when:
- You have ≥5 workers running continuously (GPU farm, cloud cluster)
- You want real-time strategy promotion without human PR review
- You are running the autoresearch loop in fully-autonomous mode

Even in server mode, the canonical `strategy.md` and report database live in git — the server is a **coordination accelerator**, not a data store.

### How to choose

| Situation | Use |
|---|---|
| Running the loop on your laptop | GitHub mode |
| Small team contributing reports | GitHub mode |
| Reporting errors / corrections | GitHub Issues |
| GPU cluster with 10+ workers | Server mode (optional) |
| CI/CD for report quality gates | GitHub Actions (already configured) |

The `.github/workflows/score_reports.yml` in this repository handles GitHub mode automatically:
- Triggers on any PR that touches `*_report.json` files
- Scores all changed reports with `evaluate.py`
- Posts a score table as a PR comment
- Blocks merge if any report is below 80/100

---

*This document describes the architectural intent for the distributed open-source platform.
Implementation status reflects the Phase 1 (local) baseline. All distributed features are
subject to change as the project evolves through community feedback.*
