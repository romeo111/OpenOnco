# knowledge_base/TODO

Known open issues surfaced during spec review (2026-04-24). Not blocking
the skeleton — blocking a production-ready OpenOnco.

## Non-blocking schema gaps (from cross-spec review)

### 1. Timeline is a derived output, not an entity

**Source:** REFERENCE_CASE_SPECIFICATION §1.2 requires "Timeline
visualization" in plan output. KNOWLEDGE_SCHEMA has no Timeline entity.

**Decision for now:** derive Timeline at plan render time from the
chosen Indication + its Regimen.cycle_length + MonitoringSchedule.phases.

**Revisit if:** multiple plans need to align on a shared timeline, or
audit trail needs to preserve "what timeline was shown on date X."

### 2. "Safety layer" is scattered across Contraindication + SupportiveCare + Test

**Source:** REFERENCE_CASE §1.3 talks about a "Safety layer" (HBV
prophylaxis, HCC surveillance) as a cohesive section. Our schema
splits this across three entities.

**Decision for now:** render-time aggregation by tag / category.

**Revisit if:** clinical reviewers find it hard to curate safety
protocols as fragmented entities.

### 3. No `Indication.ukraine_availability_note` field

**Source:** SOURCE_INGESTION_SPEC §24.1 says Ukraine regulatory
blocks availability. Currently this has to be enforced by rule engine
checking `Regimen.ukraine_availability` at eval time.

**Decision for now:** rule engine enforces. Explicit in code, implicit
in schema.

**Revisit if:** we need to mark some Indications "default assumes UA
availability" at curation time for clarity.

## Spec consistency

### 4. CQL dropped without explicit governance note

**Source:** CHARTER §5.3 mentions HL7 CQL aspirationally;
KNOWLEDGE_SCHEMA §1.1 commits to YAML; SOURCE_INGESTION_SPEC §12.5
commits to Pydantic.

**Action:** update CHARTER to note CQL is out-of-scope for MVP. Small
edit, should be done before Part D published.

### 5. DATA_STANDARDS §8.1 doesn't cross-reference Test.priority_class

**Source:** DATA_STANDARDS uses "critical" as a word; KNOWLEDGE_SCHEMA
§10.2 formalizes it as enum `critical | standard | desired | calculation_based`.

**Action:** add reference in DATA_STANDARDS when next updated. Cosmetic.

## Skeleton implementation gaps

### 6. Rule engine does not exist yet

**Current:** schemas + loader only. No patient → Indication matching
logic. No Algorithm.decision_tree evaluator.

**Blocking:** yes, for "generate a plan" functionality. Not blocking
for "validate the knowledge base" functionality.

**Priority:** next major work after seed YAMLs are all in place.

### 7. Live-API clients are protocol only

**Current:** `clients/base.py` has SourceClient + TTLCache stubs.

**Missing:** CT.gov and PubMed clients still live in repo top level
(pre-archive); need refactor under `clients/`. DailyMed, openFDA,
OncoKB, ClinVar, gnomAD clients not started.

**Priority:** P1 — each is a ~100-line client.

### 8. Ingestion loaders are not started

**Current:** `ingestion/` directory is empty.

**Missing:** loaders for ICD-O-3, LOINC, RxNorm, ATC, CTCAE, CIViC,
МОЗ, НСЗУ, Держреєстр (9 sources — see SOURCE_INGESTION_SPEC §17).

**Priority:** P0 for МОЗ + НСЗУ (unique value), P1 for code systems
and CIViC.

### 9. No CI workflow for schema / referential integrity

**Current:** workflow `.github/workflows/score_reports.yml` was deleted
in 86c7868 (dormant, referenced legacy paths).

**Missing:** new workflow that runs `validation/loader.py` on PR,
checks that every Source referenced exists, that deprecated sources
are flagged, that two-reviewer-approval metadata is present for
Indication changes.

**Priority:** P1, after seed is more complete.

### 10. No rendering layer

**Current:** YAML → Pydantic entities. No plan PDF/HTML generation.

**Missing:** the two-plan rendering pipeline (see CHARTER §2) that
produces `план лікування.html` output. Part of the existing first-
patient artifacts (in repo root, gitignored) is a manual instance of
this; systematize.

**Priority:** P2 — rule engine first, then rendering.

### 11. Reference case end-to-end test

**Current:** skeleton has HCV-MZL Disease + Drugs + Regimens + Indications
+ Algorithm as YAML. Doesn't actually generate a plan yet (no rule engine).

**Missing:** integration test that takes a synthetic HCV-MZL patient
profile (from REFERENCE_CASE §3), runs it through the rule engine, and
produces the expected two Indications.

**Priority:** acceptance criterion for P0 rule engine.
