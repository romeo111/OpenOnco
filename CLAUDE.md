# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and similar AI
agents (Codex, etc.) when working in this repository. **Read this file
in full at the start of every session.**

## Project: OpenOnco

Free public resource for oncology clinical decision support. User uploads a
patient profile → receives two alternative treatment plans (standard +
aggressive) with full source citations. Plans refresh as new data arrives
(new labs, doctor decisions, updated guidelines).

**Status:** v0.1 draft. KB expansion waves GI-2, GI-3, PUL, HEME-1 complete
(2026-05-09). CIViC-primary actionability pivot phases 2-5 still pending.
Rule engine + render in progress.

## Source of truth hierarchy

When instructions conflict, obey this order:

1. `specs/CHARTER.md` — project governance + scope
2. Other `specs/*.md` — clinical, data, schema, source, reference case
3. This `CLAUDE.md`
4. `README.md`
5. Anything under `legacy/` — **not authoritative**; historical reference only

`legacy/` contains the pre-OpenOnco autoresearch pipeline. Retired (not
deleted) because the LLM-ranks-treatments pattern conflicts with CHARTER
§8.3. Don't use it as a pattern for new work.

## Repo layout (top level)

```
cancer-autoresearch/
├── specs/                            # active specifications (UA)
├── knowledge_base/
│   ├── clients/                      # SourceClient implementations
│   │   ├── ctgov_client.py           # ClinicalTrials.gov v2
│   │   ├── pubmed_client.py
│   │   ├── dailymed_client.py
│   │   ├── openfda_client.py
│   │   └── translate_client.py
│   ├── engine/                       # rule engine + render + MDT
│   │                                 # actionability_{types,client,extract,conflict}.py
│   ├── schemas/                      # Pydantic entity schemas
│   ├── validation/                   # YAML loader + validators
│   ├── ingestion/                    # МОЗ extractor, civic_loader.py, ...
│   └── hosted/
│       ├── content/                  # KB YAML data (diseases, regimens, RFs, …)
│       └── civic/<date>/             # CIViC nightly snapshot (CC0)
├── docs/                             # built site (openonco.info) + reviews/
├── scripts/                          # build_site.py, fill scripts, coverage tools
├── tests/                            # pytest suite
├── legacy/                           # retired autoresearch pipeline (not authoritative)
├── README.md
└── CLAUDE.md
```

Two Ukrainian HTML files at the repo root (`*план лікування.html`) are
real first-patient deliverables. **Gitignored** per CHARTER §9.3 — do
not stage, do not move without explicit user instruction.

## Critical invariants

- **Language:** specs and READMEs are English-canonical. Ukrainian originals
  are preserved in `uk/` subfolders (e.g. `specs/uk/`, `knowledge_base/uk/`).
  New spec content should be written in English. Technical terms and license
  names stay English inline.
- **LLMs are not the clinical decision-maker** (CHARTER §8.3). Clinical
  recommendations come from a declarative rule engine reading a versioned
  knowledge base. LLMs do only: boilerplate code, doc drafts, extraction
  from clinical documents (with human verification), translation with
  clinical review. Not: choosing regimens, generating dosing, interpreting
  biomarkers for treatment selection.
- **Two-reviewer merge for clinical content** (CHARTER §6.1). Any change
  under `knowledge_base/hosted/content/` that affects clinical recommendations
  needs two of three Clinical Co-Leads to approve.
- **No destructive action on patient data.** Two HTML files at repo root
  + any future patient artifacts must not leak into git history or public
  artifacts. CHARTER §9.3 requires informed consent + de-identification +
  ethics approval before any patient data goes public.
- **Source hosting default = `referenced`, not `hosted`** (SOURCE_INGESTION_SPEC §1.4).
  Hosting requires explicit H1–H5 justification.
- **Free public resource → non-commercial** (CHARTER §2). Many source
  licenses depend on this.
- **Actionability data source = CIViC (CC0).** OncoKB rejected per ToS
  conflict with CHARTER §2 — see
  `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`. Engine modules
  use `actionability_*` naming. Any `SRC-ONCOKB` citations in YAML are
  legacy migration metadata; render layer must not surface them.

## Multi-agent coordination protocol

This repo runs multiple parallel Claude/Codex sessions. Branches, working
tree, and HEAD can change between any two commands without warning. Treat
the repo state as adversarially mutable.

### Pre-flight check (mandatory for every agent, every task)

Before any write or destructive operation, run AND verify:

```bash
git rev-parse --abbrev-ref HEAD       # expected branch
git rev-parse HEAD                    # expected commit
git status --short                    # expected clean (or known mods)
```

If any of these mismatch what the brief promised: **STOP, report, do not
proceed.** The orchestrating session corrects state; agents do not.

### Branch ownership

- One workstream = one named feature branch (`feat/*`, `hotfix/*`).
- **Never commit directly to `master`.**
- **Never delete a branch** (`git branch -d/-D`) without explicit user instruction.
- **Never force-push** (`-f`, `--force-with-lease`) without explicit user instruction.
- For long-running pivots, tag a baseline at start: `git tag <name>-baseline`.
- Branch refs may vanish between commands (parallel session deleted them) —
  the commits remain on other branches and via reflog. Don't panic-recreate
  state; report and ask.

### Worktree isolation

- Parallel agents (background batches, multi-agent runs) **MUST** use
  worktree isolation (`isolation: "worktree"`).
- The user's main working tree is for the user + the foreground orchestrator
  only. Other agents must not edit it.
- If an agent realises it's been editing the main worktree by accident,
  **STOP** immediately and report. Do not attempt clever recovery
  (`git stash` + `git reset --hard` + `git checkout -- .` chains have lost
  work in this repo before).
- `worktree-agent-*` branches are recovery points. Do not delete them.

### Commit hygiene

- **`git add -A` and `git add .` are BANNED.** Always pass explicit pathspecs.
  Other agents leave untracked files behind; `-A` swallows them.
- One agent = one logical commit (or a named small set). Composite commits
  spanning multiple agents' work are forbidden — they destroy audit trails.
- Pre-commit hooks run; **never use `--no-verify`**.
- Never amend a commit that's been shared across branches (`--amend` only
  while a commit is solo on its branch and unpushed).
- Stash messages must include `<branch>-<purpose>-<HHMM>` for grep-recovery.

### Stop conditions (abort + report, do not proceed)

- HEAD on a different branch than the brief expected.
- Working tree unexpectedly modified.
- Expected commit absent from current branch (cherry-pick / merge needed —
  orchestrator's call, not agent's).
- Stash pop / cherry-pick / merge conflict.
- Unfamiliar branches/tags appearing (likely from parallel session).
- Edits would land outside the brief's allowlist of file paths.

### File-set partitioning for parallel batches

When orchestrator launches N parallel agents, each agent receives an
**explicit allowlist of file paths**. Agents skip files outside the
allowlist silently (no error). The orchestrator partitions by:

- File-system path (different directories)
- Entity type (`bio_*.yaml` vs `bma_*.yaml` vs `rf_*.yaml`)
- Biomarker/disease/source classification (e.g., IHC bucket vs single-allele bucket)

Two agents writing to the same file is a coordination bug — surfaces as a
worktree merge conflict at integration time.

### Multi-session realities to expect

- Other sessions check out branches under your feet.
- HEAD jumps to unrelated commits.
- Stashes accumulate; some are yours, most aren't. **Never `git stash drop`
  a stash you didn't create.**
- New `worktree-agent-*` branches appear in `git worktree list`.
- 30+ such branches is normal; they are work-in-progress recovery points.

## Technology choices

- **Python 3.11+.** Schema layer requires 3.12 specifically (PEP 585).
  Default `python` on Windows shells often resolves to 3.8 — use
  `C:/Python312/python.exe` or `py -V:3.12` for validator/tests.
- **Dependencies:** `pydantic`, `httpx`, `pyyaml`/`ruamel.yaml`, `pypdf` /
  `pdfplumber`, `pytesseract` + Ukrainian language pack.
- **Storage = YAML files + git history**, validated by Pydantic on load
  (SOURCE_INGESTION_SPEC §12.1). Migrate to PostgreSQL when entity count
  passes ~10K.
- **No Django, no ORMs, no heavy frameworks.**
- **FHIR R4/R5 + mCODE** as patient-input data model.
- **No SNOMED CT, no MedDRA** in MVP — license gates. Use LOINC + ICD-10/O-3
  + RxNorm + CTCAE v5.0 instead.

## Workflow expectations

- Check `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` before adding to the KB.
  Vague spec → surface gap, ask. Don't invent fields.
- New source → follow `specs/SOURCE_INGESTION_SPEC.md` §8 + §20. License
  classification is a gate, not a formality.
- Clinical content → every factual claim needs a Source citation per
  CLINICAL_CONTENT_STANDARDS.
- Prefer editing existing spec files. New spec docs need registration in
  CHARTER's document list.

## What Claude Code should (not) do on its own

**Do:**
- Edit specs to fix inconsistencies, after surfacing them and getting user approval.
- Implement Pydantic schemas, ingestion loaders, validators, client refactors autonomously.
- Run pre-flight checks before every write.
- Stop and report when stop conditions hit.
- Push completed feature-branch work to `origin` once all gates pass —
  working tree clean, KB validator + pytest + pre-commit hooks green,
  no merge / cherry-pick / stash conflicts, branch is not `master`/`main`,
  push is not a force-push and does not require `--no-verify`. No further
  confirmation needed in this case (authorized 2026-04-29). If any gate
  fails or the push would touch `master` directly, force-push, or skip
  hooks → still ask first.

**Do not:**
- Commit patient-specific data, ever.
- Push directly to `master`/`main` without explicit user instruction.
- Delete branches without explicit user instruction.
- Force-push without explicit user instruction.
- Use `git add -A` / `git add .` / `--no-verify`.
- Rename the project, change licenses, alter CHARTER scope.
- Revive `legacy/` code as a pattern.
- Propose paid/commercial-tier features.
- Drop or modify a stash you didn't create.
- Use destructive shortcuts (`git reset --hard`, `git checkout -- .` over
  files you don't fully understand) to "make a problem go away" — diagnose
  the root cause, ask the user when uncertain.

## Current state (as of 2026-05-09)

- All six specs drafted at v0.1. Specs naming locked: OpenOnco.
- KB scale: **78 diseases, 438 biomarker_actionability, 173 biomarkers, 383
  sources, 251 drugs, 426 indications, 474 redflags, 361 regimens, 140
  algorithms, 8 procedures, 5 radiation courses.** (updated 2026-05-09)
- API clients live under `knowledge_base/clients/`.
- RedFlag quality phases 1-7 done (2026-04-25/26): clinical sign-off received.
- 9-agent parallel run (2026-04-27 morning): ~73 biomarkers tagged with
  `oncokb_skip_reason`, 23 BMA drafts pending clinical signoff, 53 Source
  stubs, 1,251 UA-language fields drafted, several review reports.
- **OncoKB → CIViC pivot** (2026-04-27 afternoon): Phases 0 + 1 + 1.5
  landed on `feat/civic-primary`:
  - Phase 0: coverage audit (`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`)
  - Phase 1 (commit `5384348`): engine module renames `oncokb_*` →
    `actionability_*`, `services/oncokb_proxy/` dropped, schema generalized
    with `evidence_sources` block.
  - Phase 1.5 (commit `c72e45b`): YAML migration — 29 BIO files
    `oncokb_lookup` → `actionability_lookup`, 399 BMA files
    `oncokb_level` + `oncokb_snapshot_version` → `evidence_sources` block
    + `actionability_review_required: true`.
  - Phases 2 (CIViC reader, fusion-aware matcher, monthly refresh CI) +
    3 (BMA evidence reconstruction) + 4 (render + spec + docs) + 5 (verification) pending.

## Audit artifacts

Canonical record of recent multi-agent runs lives in `docs/reviews/`:

- `oncokb-public-civic-coverage-2026-04-27.md` — license + coverage audit
  that drove the CIViC pivot.
- `citation-verification-2026-04-27.md` — 914 findings across 464 entities.
- `redflag-indication-coverage-2026-04-27.md` — 65-disease gap matrix.
- `bma-coverage-2026-04-27.md` — 23 BMA drafts + 14 source-ingest TODOs.

Read these before drafting clinical content in their domain — they list
known gaps, evidence disagreements, and entities awaiting two-reviewer
signoff.

## Medical disclaimer

Research/support tool, not a medical device. All recommendations must be
verified by a qualified oncologist. See CHARTER §11.
