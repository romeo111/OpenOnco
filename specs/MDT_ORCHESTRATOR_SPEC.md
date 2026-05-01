# MDT Orchestrator and Decision Provenance Specification

**Project:** OpenOnco
**Document:** MDT Orchestrator + Decision Provenance
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads
**Prerequisite documents:** CHARTER.md (especially §1, §2, §6, §8.3, §15),
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md,
REFERENCE_CASE_SPECIFICATION.md, SOURCE_INGESTION_SPEC.md

---

## Purpose of this document

Addresses the explicit gap noted in `KNOWLEDGE_SCHEMA_SPECIFICATION.md`
§1306 ("Not modelled: clinical trial matching, genetic syndromes,
**multidisciplinary coordination**").

OpenOnco **does not make clinical decisions** (CHARTER §1, §8.3) and
does not position itself as "smarter than the physician" — instead, it
prepares a **structured package for the tumor board (MDT — multidisciplinary
team)** that helps understand:

1. **Who should be at the table** (role recommendation)
2. **What questions remain open** (OpenQuestion)
3. **What data is missing or uncertain** (data quality summary)
4. **Who did what and when** (decision provenance / audit trail)

The MDT Orchestrator is a separate layer on top of the rule engine that
**does not change** the regimen selection or any other clinical recommendation.
All therapeutic recommendations remain the prerogative of the curated
knowledge base + rule engine (CHARTER §8.3).

---

## 1. Principles

### 1.1. What the Orchestrator does

- Analyses the `patient` profile + `PlanResult` from the rule engine
- Using a set of deterministic rules, identifies **which roles are missing**
  for a complete MDT
- Using rules and profile field analysis, identifies **what is absent from
  the data** and prevents confident management (generates `OpenQuestion`)
- Creates initial `ProvenanceEvent` records: "engine generated plan",
  "engine identified required role X", "engine raised question Y"
- Packages the result into an `MDTOrchestrationResult` — a structured brief
  for the tumor board

### 1.2. What the Orchestrator does not do

- **Does not change** `default_indication_id` or any other rule engine output
- **Does not propose** new clinical recommendations (changing regimen, dose,
  adding a drug — strictly `Indication` / `Regimen` / curated KB)
- **Does not use LLMs** for clinical reasoning (CHARTER §8.3) —
  all rules are declarative and transparent to the reviewer
- **Does not simulate** expert physician judgment — it only **requests** it
- **Does not make decisions on behalf of the patient** and does not exceed
  HCP scope (CHARTER §15.2 C1)

### 1.3. What the infographic AI layer of OpenOnco deliberately does NOT do

The infographic `infograph/mdt_with_ai_layer_light_theme.html` shows
six AI-layer blocks (databases/guidelines, literature, genomics, clinical
trials, image analysis, similar cases). OpenOnco as non-device CDS implements
**not all** of them:

| Infographic block | OpenOnco | Why |
|---|---|---|
| AI analysis of databases/guidelines | ✅ rule engine + KB | core scope |
| Literature search | ✅ live `pubmed_client.py` | structured metadata, not full-text |
| Genomic interpretation | ✅ CIViC hosted, OncoKB client (roadmap) | via established evidence-graded KBs |
| Clinical trials | ✅ live `clinicaltrials_client.py` | metadata + recruiting status |
| **Image analysis (CT/MRI/PET pixel-level)** | ❌ **intentionally out of scope** | FDA Criterion 1 (image processing) → device classification (CHARTER §15.2 C3) |
| **Similar cases (cohort matching)** | ❌ not in MVP | requires persisted patient-plan registry + privacy/de-identification layer; a large separate roadmap item |

This section **limits** the orchestrator's scope: neither MVP nor future
iterations should ingest raw image/signal/NGS reads without explicit
re-classification per CHARTER §15.3.

### 1.4. Compatibility with FDA non-device CDS positioning (CHARTER §15)

The MDT Orchestrator **strengthens** FDA Criterion 4 ("HCP can independently
review the basis"):

- Makes explicit "what we do NOT know" (Open Questions, data quality)
- Makes explicit "who should provide a second opinion" (required roles)
- Makes explicit "what the system said and when" (provenance log)

This reduces automation bias (FDA Guidance §IV(4)) — the physician sees that
the system **acknowledges the limits of its competence** and requests expert
review where appropriate.

---

## 2. Data entities

All entities are **JSON-serializable Python dataclasses**. Persistence
in MVP — in-memory + optional JSON serializer; DB shape (event log,
append-only) is described in §6 below, but implementation is deferred
to a future iteration.

### 2.1. `MDTRequiredRole`

One role to invite to the tumor board (or as a principle of referral)
for complete management of this patient.

| Field | Type | Description |
|---|---|---|
| `role_id` | `str` | Canonical role ID: `hematologist`, `pathologist`, `radiologist`, `infectious_disease_hepatology`, `clinical_pharmacist`, `radiation_oncologist`, `surgical_oncologist`, `palliative_care`, `social_worker_case_manager`, … |
| `role_name` | `str` | In Ukrainian: "Гематолог / онкогематолог", "Патолог / гематопатолог", etc. |
| `reason` | `str` | Brief clinical rationale **in Ukrainian** for the reviewer |
| `trigger_type` | `enum` | `missing_data` \| `diagnosis_complexity` \| `treatment_domain` \| `safety_risk` \| `molecular_data` \| `local_availability` \| `palliative_need` |
| `priority` | `enum` | `required` \| `recommended` \| `optional` |
| `linked_findings` | `list[str]` | Identifiers of findings/biomarkers/RedFlags that triggered the rule |
| `linked_questions` | `list[str]` | IDs of OpenQuestions that this role should answer |

### 2.2. `OpenQuestion`

A question the system cannot answer automatically and that must be
resolved before the plan is finalized.

| Field | Type | Description |
|---|---|---|
| `id` | `str` | `OQ-<short-slug>` |
| `question` | `str` | Question in Ukrainian |
| `owner_role` | `str` | `role_id` of the role that typically provides the answer (`hematologist`, `radiologist`, etc.) |
| `blocking` | `bool` | Whether this question blocks plan adoption |
| `rationale` | `str` | Why this question is important |
| `linked_findings` | `list[str]` | Which profile fields are absent/ambiguous |

### 2.3. `MDTOrchestrationResult`

Top-level container returned by `orchestrate_mdt(...)`.

| Field | Type | Description |
|---|---|---|
| `patient_id` | `Optional[str]` | From `patient.patient_id`; `null` if anonymous |
| `plan_id` | `Optional[str]` | From `PlanResult.plan.id`, if a plan was generated |
| `disease_id` | `Optional[str]` | From `PlanResult.disease_id` |
| `required_roles` | `list[MDTRequiredRole]` | priority `required` |
| `recommended_roles` | `list[MDTRequiredRole]` | priority `recommended` |
| `optional_roles` | `list[MDTRequiredRole]` | priority `optional` |
| `open_questions` | `list[OpenQuestion]` | All questions, including blocking ones |
| `data_quality_summary` | `dict` | Counts: missing fields, ambiguous, unknown red-flag inputs |
| `aggregation_summary` | `dict` | Explicit "AI-aggregation" artifact (infographic step 2): `kb_entities_loaded`, `kb_sources_cited`, `indications_evaluated`, `biomarkers_referenced`, `red_flags_total_in_kb`, `red_flags_fired`, `open_questions_raised`, `live_api_clients_available`, `live_api_clients_invoked` |
| `warnings` | `list[str]` | Technical warnings (entity not found, etc.) |
| `provenance` | `DecisionProvenanceGraph` | Initial events |

### 2.4. `ProvenanceEvent` (event-log shape — append-only)

| Field | Type | Description |
|---|---|---|
| `event_id` | `str` | Globally unique, e.g. `EV-<plan_id>-001` |
| `timestamp` | `str` | ISO-8601 UTC |
| `actor_role` | `str` | `engine` \| `hematologist` \| … (canonical role_id or system) |
| `actor_id` | `Optional[str]` | Specific reviewer (e.g. `dr-coleadX`); `null` for engine or anonymous |
| `event_type` | `enum` | `confirmed` \| `modified` \| `rejected` \| `added_question` \| `approved` \| `requested_data` \| `flagged_risk` |
| `target_type` | `enum` | `diagnosis` \| `staging` \| `regimen` \| `contraindication` \| `red_flag` \| `source` \| `plan_section` |
| `target_id` | `str` | Canonical id (e.g. `IND-HCV-MZL-1L-ANTIVIRAL`, `RF-BULKY-DISEASE`) |
| `summary` | `str` | Brief summary in Ukrainian |
| `evidence_refs` | `list[str]` | Source IDs / citation IDs supporting this event |

### 2.5. `DecisionProvenanceGraph`

| Field | Type | Description |
|---|---|---|
| `nodes` | `list[dict]` | Canonical nodes: `{id, type, label}` (e.g. diagnosis node, regimen node) |
| `edges` | `list[dict]` | Links between nodes: `{from, to, kind}` (e.g. `regimen → contraindication` `kind=triggers`) |
| `events` | `list[ProvenanceEvent]` | Sequential log |
| `plan_version` | `int` | Version of the Plan this graph is tied to |

---

## 3. Role recommendation rules (for the HCV-MZL reference case)

All rules are deterministic; if the condition is met, the corresponding
role is added. Rules are expanded per-disease as the KB grows.

| # | Trigger | Role | Priority | trigger_type |
|---|---|---|---|---|
| R1 | `Disease.lineage` contains `lymphoma` OR `Disease.codes.icd_o_3_morphology` falls in the mature B/T-cell lymphoma range (9590–9729 / 9760–9769) | `hematologist` | `required` | `diagnosis_complexity` |
| R2 | HCV biomarker positive (BIO-HCV-RNA == positive) OR HBV serology positive | `infectious_disease_hepatology` | `recommended` | `molecular_data` |
| R3 | Any imaging fields present in the profile (`dominant_nodal_mass_cm`, `mediastinal_ratio`, `pet_ct_date`, `ct_findings`, `lugano_stage`) | `radiologist` | `recommended` (escalates per §3-Esc) | `diagnosis_complexity` |
| R4 | Lymphoma diagnosis (CD20-IHC, biopsy-related fields) OR transformation risk under review | `pathologist` | `recommended` | `diagnosis_complexity` |
| R5 | Default/alternative track has `plan_track == "aggressive"` (chemoimmunotherapy) | `clinical_pharmacist` | `recommended` | `treatment_domain` |
| R6 | Disease — extranodal MALT (ICD-O-3 morphology starts with `9699`) — RT may be locally effective | `radiation_oncologist` | `optional` | `treatment_domain` |
| R7 | Treatment plan requires drugs with `reimbursed_nszu == false` | `social_worker_case_manager` | `recommended` | `local_availability` |
| R8 | ECOG ≥ 3 OR decompensated comorbidity → palliative assessment | `palliative_care` | `recommended` | `palliative_need` |
| R9 | Indication.applicable_to.biomarker_requirements_required references a Biomarker with `biomarker_type` in `_ACTIONABLE_GENOMIC_TYPES` (gene_mutation, fusion, amplification, deletion, copy_number, msi_status, tmb, methylation) | `molecular_geneticist` | `recommended` | `molecular_data` |

### §3-Esc. Priority escalation via RedFlag

If `PlanResult.plan.trace.fired_red_flags` contains a RedFlag with
`clinical_direction in {"intensify", "hold"}`, its domain role is
escalated to `required`. Domain map (MVP):

| RedFlag | Domain role |
|---|---|
| `RF-BULKY-DISEASE` (intensify) | `radiologist` |
| `RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION` (intensify) | `pathologist` |
| `RF-HBV-COINFECTION` (hold) | `infectious_disease_hepatology` |
| `RF-DECOMP-CIRRHOSIS` (de-escalate) | _not escalated_ — direction outside the escalation set |

Extended in `_REDFLAG_DOMAIN_ROLE` as new RedFlags are added.

**Deduplication:** a single `role_id` appears in the result at most once.
If different rules assign different priorities — the **highest** is used
(`required` > `recommended` > `optional`). This applies to escalation in
§3-Esc as well.

**trigger_type coverage:** MVP rules use 5 of the 7 values:
`diagnosis_complexity`, `molecular_data`, `treatment_domain`,
`local_availability`, `palliative_need`. Values `missing_data` and
`safety_risk` are reserved for future rules (extension points).

---

## 4. Open Question rules (for the HCV-MZL reference case)

An `OpenQuestion` appearing means: the rule engine could not answer
confidently because the input data is absent or contradictory.

| # | Trigger | Question | owner_role | blocking |
|---|---|---|---|---|
| Q1 | Disease — HCV-MZL OR HCV+ AND `hbsag` / `anti_hbc_total` absent | "Has HBV serology been performed (HBsAg, anti-HBc total)? HBV reactivation risk before anti-CD20 therapy." | `infectious_disease_hepatology` | `true` |
| Q2 | HCV+ AND `child_pugh_class` / `decompensated_cirrhosis` / `fib4_index` absent | "What is the fibrosis/cirrhosis stage? This affects DAA selection and bendamustine dosing." | `infectious_disease_hepatology` | `true` |
| Q3 | Lymphoma AND `cd20_ihc_status` / `biopsy_confirmed` confirmation absent | "Has CD20+ status been confirmed by histology? Without CD20+, rituximab/obinutuzumab are not indicated." | `pathologist` | `true` |
| Q4 | Lymphoma AND staging fields absent (Lugano stage, PET-CT date) | "Has complete staging been performed (Lugano + PET/CT)?" | `radiologist` | `false` |
| Q5 | Aggressive track selected, `ldh_ratio_to_uln` absent | "What is the current LDH? This is a marker of tumor burden and transformation." | `hematologist` | `false` |
| Q6 | Any regimen has a drug with `reimbursed_nszu == false` | "Is drug X available to the patient (out-of-pocket vs program)? Is a social work consult needed?" | `social_worker_case_manager` | `false` |

**Extensibility:** rules are added per-disease. In MVP, the subset for
HCV-MZL is implemented.

---

## 5. Data quality summary

Meta-information for the tumor board:

```python
{
    "missing_critical_fields": [...],      # fields whose absence prevents confident management
    "missing_recommended_fields": [...],   # fields desired but not blocking
    "ambiguous_findings": [...],           # MVP: always []; extended in future iterations
    "unevaluated_red_flags": [...],        # RedFlag IDs that could not be evaluated due to absent findings
    "fields_present_count": int,
    "fields_expected_count": int,
}
```

**Mechanics of `unevaluated_red_flags`:** the orchestrator iterates over
all RedFlag entities in the KB (filtering by `relevant_diseases` if
specified), recursively extracts all referenced field-keys from
`trigger.any_of/all_of/none_of` (`finding`, `condition`, `lab`, `symptom`).
If any key is absent from patient findings — the RedFlag is considered
incompletely-evaluatable and enters the list. This allows the reviewer
to see "we don't know whether this risk has materialized", rather than
silently treating it as irrelevant.

This is **not a new clinical recommendation**; it is an honest report on
data completeness that helps the reviewer understand how confidently the
system was able to operate with what it had.

---

## 6. Decision Provenance — append-only event log

### 6.1. Purpose

Every change in the Plan / MDT context is an **event**. Events are
immutable, events form a log, the log reconstructs the history of how
the plan was created. Supports:

- Audit trail for regulatory inquiry (CHARTER §10.2, §15.1 Criterion 4)
- Reproducibility: any Plan can be restored to its state at a given timestamp
- Attribution: visible **who** exactly (role + optionally physician) added
  a question, approved a recommendation, rejected a pathway
- Foundation for future persistence (DB-ready shape)

### 6.2. Initial events (generated automatically)

On the first call to `orchestrate_mdt(...)`:

1. `confirmed` / `plan_section` — "engine generated Plan version N"
2. For each required/recommended role — `requested_data` / `plan_section`
   with summary "review required from role X"
3. For each OpenQuestion — `added_question` / `plan_section`
4. If a RedFlag fired → `flagged_risk` / `red_flag` for each

### 6.3. Subsequent events (future iterations, not in MVP)

After MVP: an API for adding events from clinicians is added —
- `confirmed` / `diagnosis` from the pathologist
- `modified` / `regimen` from the hematologist (tied to a new Plan version)
- `approved` / `plan_section` from the tumor board (final sign-off)

### 6.4. Persistence (next step, not in MVP)

The event log is append-only by design — naturally fits:
- SQLite / Postgres event_log table with `event_id PRIMARY KEY`,
  `(target_type, target_id, timestamp)` index
- Or a JSONL file `patient_plans/<patient_id>/events.jsonl`
- Or immutable object storage (S3/MinIO) for compliance use cases

In MVP: in-memory + JSON serialization on demand. DB migration
described in the roadmap.

---

## 7. Integration with the existing engine

### 7.1. API

New public module `knowledge_base/engine/mdt_orchestrator.py`:

```python
def orchestrate_mdt(
    patient: dict,
    plan_result: PlanResult,
    kb_root: Path | str = "knowledge_base/hosted/content",
) -> MDTOrchestrationResult:
    ...
```

`generate_plan(...)` **is not changed** — the MDT context is an optional layer.

### 7.2. CLI

Flag `--mdt` in `knowledge_base/engine/cli.py`. Without `--mdt`
the CLI behaviour is identical to the current one. With `--mdt`, after
the Plan summary, the following is printed:

```
=== MDT Brief ===
Required roles:
  - hematologist: ...
Recommended roles:
  - infectious_disease_hepatology: ...
  - pathologist: ...
Optional roles:
  - radiation_oncologist: ...
Open questions (3, 2 blocking):
  - [BLOCKING] OQ-HBV-SEROLOGY: Has HBV serology been performed? (owner: infectious_disease_hepatology)
  ...
Data quality:
  Missing critical fields: 2
  Unevaluated red flags: 0
```

### 7.3. Invariants in tests

`test_mdt_orchestrator.py` explicitly verifies: after `orchestrate_mdt(...)`,
the value `plan_result.default_indication_id` is **unchanged**. This is a
mechanical guarantee of non-interference.

---

## 8. Future extensions (not in MVP)

- Per-disease role/question rules (not only HCV-MZL)
- Integration with `Indication.required_tests` / `desired_tests` →
  automatic OpenQuestion generation for missing tests
- Persistence event log
- API for adding `ProvenanceEvent` from clinicians (REST endpoint
  or CLI command `record-event`)
- Render layer: visualisation of `DecisionProvenanceGraph` as an interactive
  graph in the plan UI
- Support for annotations on Plan (`Plan.annotations[]`) — coordination
  with the `PlanAnnotation` model from `knowledge_base/schemas/plan.py`

---

## 9. Changes in this document

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-04-25 | Initial MVP spec; covers HCV-MZL reference case + general rules |
