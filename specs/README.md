# specs/

Active specifications for OpenOnco. **Specifications are the source of
truth** — when this README, `CLAUDE.md`, `README.md`, or any code
disagrees with `specs/`, the spec wins.

Documents are written in **Ukrainian** with English technical terms
inline (entity names, license names, code conventions). The language
choice is intentional, not accidental — see [`CHARTER §1`](CHARTER.md)
for the language policy.

## Read this first

- **[`CHARTER.md`](CHARTER.md)** — governance, scope, FDA non-device
  CDS positioning, dual clinical-lead review process, what the project
  explicitly does **not** do. **Read before any other spec.**

## Clinical content

- **[`CLINICAL_CONTENT_STANDARDS.md`](CLINICAL_CONTENT_STANDARDS.md)** —
  citation format, evidence levels, draft / proposed / reviewed
  lifecycle, two-reviewer signoff rules.
- **[`REDFLAG_AUTHORING_GUIDE.md`](REDFLAG_AUTHORING_GUIDE.md)** —
  RedFlag schema (≥2 Source citations required), severity, action
  triggers.
- **[`WORKUP_METHODOLOGY_SPEC.md`](WORKUP_METHODOLOGY_SPEC.md)** —
  pre-biopsy diagnostic-path methodology.

## Schema and data

- **[`KNOWLEDGE_SCHEMA_SPECIFICATION.md`](KNOWLEDGE_SCHEMA_SPECIFICATION.md)** —
  entity model: Disease, Drug, Indication, Regimen, BiomarkerActionability,
  RedFlag, Source, Reviewer, etc.
- **[`DATA_STANDARDS.md`](DATA_STANDARDS.md)** — FHIR R4/R5, mCODE,
  LOINC, ICD-10, ICD-O-3, RxNorm, ATC, CTCAE v5.0; explicit no-go list
  (no SNOMED CT, no MedDRA in MVP — license gates).
- **[`SOURCE_INGESTION_SPEC.md`](SOURCE_INGESTION_SPEC.md)** — license
  classification, `referenced` vs `hosted` vs `mixed`, H1–H5 hosting
  justification, monthly snapshot CI cadence.
- **[`REFERENCE_CASE_SPECIFICATION.md`](REFERENCE_CASE_SPECIFICATION.md)** —
  end-to-end reference case for testing the engine.

## Engine and orchestration

- **[`MDT_ORCHESTRATOR_SPEC.md`](MDT_ORCHESTRATOR_SPEC.md)** —
  multidisciplinary tumor-board orchestration, role activation,
  Open Questions.
- **[`DIAGNOSTIC_MDT_SPEC.md`](DIAGNOSTIC_MDT_SPEC.md)** — pre-biopsy
  mode (no histology → diagnostic Brief, never a treatment Plan).
- **[`SKILL_ARCHITECTURE_SPEC.md`](SKILL_ARCHITECTURE_SPEC.md)** —
  versioned skill registry, per-skill `last_reviewed`,
  `clinical_lead`, `verified_by`.

## Operations and integrations

- **[`NSZU_FEED_PLAN.md`](NSZU_FEED_PLAN.md)** — NSZU formulary
  ingestion + reimbursement signal.
- Clinical-review queues: [`CLINICAL_REVIEW_QUEUE_MYELOID.md`](CLINICAL_REVIEW_QUEUE_MYELOID.md),
  [`CLINICAL_REVIEW_QUEUE_REDFLAGS.md`](CLINICAL_REVIEW_QUEUE_REDFLAGS.md)
  — work-in-flight items awaiting Clinical Co-Lead signoff.

## External reference

- `Guidance-Clinical-Decision-Software_5.pdf` — FDA Clinical Decision
  Support guidance; CHARTER §15 cross-references its Criteria 1-4.
