# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: OpenOnco

Free public resource for oncology clinical decision support. User uploads a
patient profile → receives two alternative treatment plans (standard +
aggressive) with full source citations. Plans refresh as new data arrives
(new labs, doctor decisions, updated guidelines).

**Status:** v0.1 draft. The project is in a specifications-first phase —
specs exist; implementation of the knowledge base + rule engine is just
starting.

## Source of truth hierarchy

When instructions conflict, obey this order:

1. `specs/CHARTER.md` — project governance + scope + what the project can/can't do
2. Other `specs/*.md` — clinical, data, schema, source, reference case
3. This `CLAUDE.md`
4. `README.md`
5. Anything under `legacy/` — **not authoritative**; preserved as historical reference

`legacy/` contains the pre-OpenOnco autoresearch pipeline (Karpathy-style
`strategy.md` optimization loop). It generated the first real-patient
treatment plans, which clinicians reviewed favorably. It is retired, not
deleted, because the LLM-ranks-treatments approach conflicts with
CHARTER §8.3 (forbidden prompt patterns). Don't use it as a pattern for
new work.

## Repo layout (top level)

```
cancer-autoresearch/
├── specs/                            # active specifications (UA)
├── knowledge_base/                   # rule-engine KB
│   ├── clients/                      # SourceClient implementations
│   │   ├── ctgov_client.py           # ClinicalTrials.gov v2
│   │   ├── pubmed_client.py          # NCBI E-utilities
│   │   ├── dailymed_client.py
│   │   ├── openfda_client.py
│   │   └── translate_client.py
│   ├── engine/                       # rule engine + render + MDT
│   ├── schemas/                      # Pydantic entity schemas
│   ├── validation/                   # YAML loader + validators
│   ├── ingestion/                    # МОЗ extractor etc.
│   └── hosted/content/               # KB YAML data (diseases, regimens, RFs, …)
├── docs/                             # built site (openonco.info)
├── scripts/                          # build_site.py, fill scripts, coverage tools
├── tests/                            # pytest suite
├── legacy/                           # retired autoresearch pipeline
├── README.md
└── CLAUDE.md
```

Two Ukrainian HTML files at the repo root (`*план лікування.html`) are
real first-patient deliverables. They are **gitignored** per
`specs/CHARTER.md` §9.3 — do not stage them, do not move them without
explicit instruction from the user.

## Critical invariants

- **Language:** specs are in Ukrainian and will stay Ukrainian. Do not
  translate to English unilaterally. Technical terms and license names
  may stay English inline.
- **LLMs may not be the clinical decision-maker** (CHARTER §8.3).
  Clinical recommendations come from a declarative rule engine reading a
  versioned knowledge base. LLMs do only: boilerplate code, doc drafts,
  extraction from clinical documents (with human verification), translation
  with clinical review. Not: choosing regimens, generating dosing,
  interpreting biomarkers for treatment selection.
- **Two-reviewer merge for clinical content** (CHARTER §6.1). Any change
  under `knowledge_base/hosted/content/` that affects clinical
  recommendations needs two of three Clinical Co-Leads to approve.
- **No destructive action on patient data.** The two HTML files at repo
  root and any future patient-specific artifacts must not leak into git
  history or public artifacts. CHARTER §9.3 requires informed consent +
  de-identification + ethics approval before any patient data can be
  public.
- **Source hosting default is `referenced`, not `hosted`** (SOURCE_INGESTION_SPEC §1.4).
  Hosting requires explicit H1–H5 justification. Do not propose mirroring
  external databases.
- **Free public resource → non-commercial** (CHARTER §2). Many source
  licenses (ESMO CC-BY-NC-ND, OncoKB academic, ATC) depend on this.
  Proposing a paid tier triggers a license audit across all `referenced`
  and `mixed` sources.

## Technology choices

- **Python 3.11+.** The legacy code was stdlib-only; OpenOnco adds real
  dependencies where they pay off.
- **Dependencies in scope (planned):** `pydantic` (schema validation +
  referential integrity), `httpx` (HTTP clients with retry/async),
  `pyyaml` (YAML loading), `pypdf` / `pdfplumber` (МОЗ PDF extraction),
  `pytesseract` + Ukrainian language pack (OCR for scanned protocols).
- **Storage format for the KB:** YAML files + git history, validated by
  Pydantic on load. See SOURCE_INGESTION_SPEC §12.1 for the directory
  layout. Migrate to PostgreSQL when entity count passes ~10K
  (KNOWLEDGE_SCHEMA_SPECIFICATION §16.1 allows).
- **No Django, no ORMs, no heavy frameworks.** Python stdlib + the
  dependencies above.
- **FHIR R4/R5 + mCODE** as the patient-input data model (DATA_STANDARDS).
- **No SNOMED CT, no MedDRA** in MVP — license gates. Use LOINC + ICD-10/O-3
  + RxNorm + CTCAE v5.0 instead.

## Workflow expectations

- When asked to design or add to the knowledge base, check the relevant
  entity definition in `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` first.
  If something is vague there, surface the gap and ask — do not invent
  fields unilaterally.
- When adding a new source to the KB, follow `specs/SOURCE_INGESTION_SPEC.md`
  §8 (the add-a-source checklist) and §20 (the hosted-source checklist).
  License classification is a gate, not a formality.
- When writing clinical content (an Indication, a Regimen), every factual
  claim needs a Source entity citation. See CLINICAL_CONTENT_STANDARDS
  for citation format and evidence-level taxonomy.
- Prefer editing existing spec files to creating new ones. If you must
  add a new spec document, register it in CHARTER's document list.

## What Claude Code should (not) do on its own

- **Do** edit specs to fix inconsistencies after surfacing them — if the
  user approves.
- **Do** implement Pydantic schemas, ingestion loaders, validators, client
  refactors autonomously.
- **Do not** commit patient-specific data, ever.
- **Do not** push to `origin` without explicit user instruction.
- **Do not** rename the project, change licenses, or alter CHARTER scope
  statements without explicit user instruction.
- **Do not** revive or build on `legacy/` code as a pattern for new work —
  it is retired.
- **Do not** propose features that assume a paid/commercial tier.

## Current state (as of 2026-04-24)

- All six specs drafted at v0.1. Specs rename: OpenOncoBrief → OncoPlan →
  OpenOnco (final).
- `legacy/` archive committed (be9738b). `specs/` consolidated, stale
  top-level docs moved to `legacy/docs/OLD_*.md` (86c7868).
- Knowledge base implementation (Part B of SOURCE_INGESTION_SPEC):
  **in progress.**
- API clients refactored under `knowledge_base/clients/` per
  SOURCE_INGESTION_SPEC §12.2: `ctgov_client.py` (renamed from
  `clinicaltrials_client.py`), `pubmed_client.py`, `dailymed_client.py`,
  `openfda_client.py`, `translate_client.py`.
- RedFlag quality phases 1-7 done (2026-04-25/26): 106 RFs across all 28
  diseases, ≥2 sources each, golden fixtures auto-generated, 220 RF-tests
  green; clinical sign-off received. See `specs/REDFLAG_AUTHORING_GUIDE.md`.

## Medical disclaimer

This is a research/support tool, not a medical device. All recommendations
must be verified by a qualified oncologist. See CHARTER §11.
