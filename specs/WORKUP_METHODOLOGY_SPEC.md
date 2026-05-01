# Workup Methodology Specification

**Project:** OpenOnco
**Document:** Workup Research Methodology — how we build a basic workup for any oncology domain
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads
**Preceding documents:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DIAGNOSTIC_MDT_SPEC.md, SOURCE_INGESTION_SPEC.md

---

## Purpose of this document

OpenOnco is scaling from HCV-MZL → hematological oncology broadly → solid
tumors → other conditions. Each expansion requires a **detailed basic workup**
for the relevant suspicion: which tests are needed for diagnosis +
staging + pre-treatment baseline.

Without a formalized methodology, workup quality becomes chaotic: different
conditions covered at different depths, reviewers have no way to tell whether
`WORKUP-X` was written following NCCN or "from memory," and there are no
inclusion/exclusion criteria.

This document is the **process** for converting a condition into a DiagnosticWorkup +
a subset of Test entities in the KB — analogous to `SOURCE_INGESTION_SPEC`
for data sources, but for clinical workup content.

**First application:** comprehensive hematology workup catalog (HCV-MZL,
acute leukemia, multiple myeloma, MPN/MDS, undifferentiated lymphadenopathy,
cytopenias, monoclonal gammopathy).

---

## 1. Principles

### 1.1. Workup = "what to do," not "how to treat"

`DiagnosticWorkup` describes **diagnostic actions** (tests, biopsy,
imaging, IHC, molecular), not therapeutic recommendations.
The latter belongs to `Indication` / `Regimen` after confirmed histology.
This is a clear boundary: workup methodology does NOT extend beyond the scope
of FDA non-device CDS Criterion 3 (not a "specific treatment directive").

### 1.2. Conservative first — extend per evidence

`DiagnosticWorkup.required_tests` should contain **tests indicated in 95%
of relevant cases**, not "all possible tests if anything is unclear."
Edge cases and disease-specific extensions belong in additional fields
(`required_ihc_panel.if_b_cell`, etc.) or in separate workup variants.

Otherwise a "comprehensive" workup becomes an inflated checklist that
nobody can realistically order.

### 1.3. Universal-to-specific decomposition

```
WORKUP-CYTOPENIA-EVALUATION (broad triage)
    │
    ├─→ findings: lymphadenopathy → WORKUP-SUSPECTED-LYMPHOMA
    ├─→ findings: blasts on smear → WORKUP-SUSPECTED-ACUTE-LEUKEMIA
    ├─→ findings: monoclonal protein → WORKUP-SUSPECTED-MULTIPLE-MYELOMA
    └─→ findings: unexplained → WORKUP-MDS-EVALUATION
```

Decomposition via `applicable_to.lineage_hints` +
`applicable_to.presentation_keywords`. The engine matcher allows
**a broader workup to transition into a specific one** as findings are
refined (revisions workflow per DIAGNOSTIC_MDT_SPEC §7.1).

### 1.4. Cite-able provenance per Test attribute

Each Test must reference an authority through the `sources:` field
(the existing Source entities mechanism). Not a vague "everyone knows that."
This strengthens Criterion 4 transparency — a clinician can trace why
test X is listed in this workup.

---

## 2. Source hierarchy for workup research

### 2.1. Tier 1 — mandatory consultation for every workup

| Authority | Purpose | Frontmatter in Source entity |
|---|---|---|
| **NCCN Guidelines** | US standard of care; the most detailed initial workup sections in "WORKUP" and "DIAGNOSIS" sub-tables | `evidence_tier: 1`, `hosting_mode: referenced` (NCCN copyright) |
| **ESMO Clinical Practice Guidelines** | EU equivalent; often more concise, but explicit on initial assessment | `evidence_tier: 1` |
| **WHO Classification of Tumours (5th ed.)** | Canonical classification + diagnostic criteria per disease | `evidence_tier: 1`, `hosting_mode: referenced` |
| **EHA Guidelines (for hematology)** | European Hematology Association — detail on molecular workup, nuances per subtype | `evidence_tier: 1` |
| **BSH Guidelines (for hematology, UK)** | British Society for Haematology — practical approaches, well organized | `evidence_tier: 1` |
| **ASH (American Society of Hematology) Pocket Guides + Education Program** | Contemporary consensus, especially for emerging entities | `evidence_tier: 1-2` |

### 2.2. Tier 2 — additional context

| Authority | Purpose |
|---|---|
| **Cochrane Systematic Reviews** | Where a review of a specific test/protocol exists |
| **Ukrainian Ministry of Health clinical protocols** | Local practice + reimbursement context (for NSZU) |
| **Major textbooks (Williams Hematology, Wintrobe's, Hoffman)** | Background reading; not a primary source |
| **Peer-reviewed RCTs in JCO / Blood / Lancet Oncol / NEJM** | Specific evidence for confirmation tests or novel diagnostic markers |

### 2.3. Tier 3 — permitted only explicitly

| Authority | When permitted |
|---|---|
| **Expert opinion / case series** | Only when nothing higher exists, **and** flagged in Test.notes as "expert opinion only — pending higher-tier evidence" |
| **Single-institution practice** | Only as an example, not a foundation |

### 2.4. What is **not** a Tier source

- UpToDate (proprietary, paid, not open)
- Wikipedia (not authoritative)
- LLM-generated content without human verification
- Pharma marketing materials

---

## 3. Test entity attribute completeness checklist

Check the following for each new or updated Test:

### 3.1. Required fields (no Test merges without these)

- [ ] `id` — format `TEST-<SHORT-SLUG>`
- [ ] `names.preferred` (English) + `names.ukrainian`
- [ ] `category` ∈ {`lab`, `imaging`, `histology`, `genomic`, `clinical_assessment`}
- [ ] `purpose` — one sentence explaining **why** we perform this test
- [ ] `priority_class` ∈ {`critical`, `standard`, `desired`, `calculation_based`}
- [ ] `sources` — minimum 1 Tier 1 reference

### 3.2. Recommended

- [ ] `loinc_codes` — if a LOINC code exists; null is acceptable for specific panels (cytogenetics, FISH)
- [ ] `specimen` — which biological matrix
- [ ] `turnaround_time` — typical lab turnaround (1-3 hours / same day / 1-3 days / 7-14 days, etc.)
- [ ] `availability_ukraine` — test in the Ukrainian context (state_funded, typical_cost_uah, regional availability)

### 3.3. Optional (per test type)

- `synonyms` — alternate names
- `notes` — caveats, when not applicable, common pitfalls

### 3.4. Anti-patterns (rejection criteria in clinical review)

❌ Test without `purpose` (no **why**)
❌ Test with `priority_class: critical` without cite-able rationale in Tier 1
❌ Test with only a proprietary marker name (e.g., commercial assay name without generic description)
❌ Test with `turnaround_time: null` when it is well known (laziness, not genuine unknown)

---

## 4. DiagnosticWorkup entity completeness checklist

### 4.1. Required fields

- [ ] `id` — format `WORKUP-<PRESENTATION-OR-SUSPICION>`
- [ ] `applicable_to.lineage_hints` — minimum 1 controlled-vocabulary hint
- [ ] `applicable_to.tissue_locations` OR `applicable_to.presentation_keywords` — minimum one category
- [ ] `required_tests` — minimum 3 (otherwise this is not a "workup," it's a "single test")
- [ ] `mandatory_questions_to_resolve` — minimum 2 (otherwise the workup is trivial)
- [ ] `triggers_mdt_roles.required` — minimum 1
- [ ] `expected_timeline_days` — realistic estimate
- [ ] `sources` — minimum 2 Tier 1 references
- [ ] `last_reviewed` + (after publishing) `reviewers` ≥ 2

### 4.2. Recommended

- `biopsy_approach` — preferred + alternatives + rationale, for any suspicion where biopsy is part of the standard
- `required_ihc_panel` — baseline + conditional (if_b_cell / if_t_cell / if_aggressive / if_solid) — for suspicions where histology is always part of the workup
- `expected_workup_cost_uah_estimate` — for Ukrainian financial planning
- `triggers_mdt_roles.recommended` + `optional`

### 4.3. Workup composition

More complex presentations can **raise multiple workups simultaneously**:
- A patient with cytopenias + lymphadenopathy → match BOTH
  `WORKUP-CYTOPENIA-EVALUATION` AND `WORKUP-SUSPECTED-LYMPHOMA`
- The engine should add tests from both (deduplicated)
- MVP: the matcher returns the top-1 match. Future: composition matcher
  (roadmap item)

---

## 5. Process: extending OpenOnco to a new oncology domain

Each expansion (e.g., "add solid tumor — breast cancer") should follow these steps:

### Step 1: Survey authoritative guidelines (Tier 1)

- NCCN Guideline for the condition (Initial Workup section)
- ESMO Clinical Practice Guideline
- WHO Classification subtype detail
- Specialty society (for breast — NABCO, ABS, EBCC; for GI — DDW, etc.)

Artifact: `references/<domain>/guidelines_survey.md` listing consulted documents + URLs + version dates.

### Step 2: Identify baseline tests + diagnostic studies

For each condition from Step 1, identify:
- **Initial assessment** (history, exam, basic labs)
- **Confirmatory** (biopsy, imaging for diagnosis)
- **Staging** (extent of disease)
- **Pre-treatment baseline** (organ function, fertility, vaccination)
- **Risk stratification** (prognostic markers)

All are separate Test entities. Reuse existing ones where possible (CBC, LFT — universal).

### Step 3: Build / extend the KB

Per Test:
- Create YAML per §3 checklist
- Links to Tier 1 sources

Per Workup:
- Create YAML per §4 checklist
- `triggers_mdt_roles` — what team composition is required

### Step 4: Patient profile fields

If a new condition requires specific profile fields (e.g., breast exam,
mammographic findings) — add them to DATA_STANDARDS under the relevant
section + adjust the engine matcher per `presentation_keywords`.

### Step 5: Engine integration

If needed — add new D-rules to `mdt_orchestrator._apply_diagnostic_role_rules`
for domain-specific role recommendations (e.g., breast surgical oncologist
for any breast suspicion).

### Step 6: Clinical review

CHARTER §6.1 standard process: **2 of 3 Clinical Co-Leads** must sign off
on content. Reviewer A — domain expert (e.g., breast oncologist for a breast
workup). Reviewer B — methodological reviewer.

After sign-off — `Test.reviewer_signoffs: 2` AND `Workup.reviewer_signoffs: 2`.
Until then — everything is STUB and explicitly labelled.

### Step 7: Update WORKUP_METHODOLOGY_SPEC.md changelog

Add a row in §7 for the domain extension, referencing the guidelines survey
and responsible reviewers.

---

## 6. Anti-patterns and bias detection

### 6.1. Anti-pattern: "kitchen sink" workup

The tendency to add every mentioned test → 30+ required tests.
In practice a clinician cannot order all of them, and the cost is prohibitive.

**Mitigation:** use `priority_class`:
- `critical` — without this the plan cannot proceed (≤ 5-7 per workup)
- `standard` — 95% of cases (≤ 10-15)
- `desired` — additional for specific findings (state conditions in Test.notes)
- `calculation_based` — derived from others (FIB-4, HCT, etc.)

### 6.2. Anti-pattern: Western-only practice

NCCN/ESMO assume access to PET, NGS panels, and monoclonal antibodies.
In the Ukrainian context these may be unavailable.

**Mitigation:** `availability_ukraine.state_funded: false` flag + alternative test
references. Ukrainian Ministry of Health protocols are Tier 1 for the Ukrainian baseline.

### 6.3. Anti-pattern: outdated workup

Diagnostics evolves. Old cytogenetic panels → NGS. Old imaging → PET-MR.

**Mitigation:** `last_reviewed` date + quarterly audit (CLINICAL_CONTENT_STANDARDS §9.1).
A Test with `last_reviewed` > 2 years → quality gate flag.

### 6.4. Anti-pattern: AI-generated workup without sources

The temptation to use an LLM to rapidly generate a "comprehensive workup"
for a new condition.

**Mitigation:** CHARTER §8.3 hard rule — an LLM is not the clinical
decision-maker. Workup content is **always** human-authored with cite-able
sources. LLMs are permitted for extraction from PDFs (per CHARTER §8.1)
with human verification — not for inventing new recommendations.

---

## 7. Domain extensions log

| Date | Domain | Workups added | Tests added | Reviewer A | Reviewer B | Spec update |
|---|---|---|---|---|---|---|
| 2026-04-25 | Hematology — initial broad coverage | WORKUP-SUSPECTED-LYMPHOMA (expanded), -ACUTE-LEUKEMIA, -MULTIPLE-MYELOMA, -MPN-MDS, -CYTOPENIA-EVALUATION, -LYMPHADENOPATHY-NONSPECIFIC, -MONOCLONAL-GAMMOPATHY | ~30 hematology Tests | TBD | TBD | This document v0.1 |

(Add future entries upon each extension.)

---

## 8. Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-04-25 | Initial MVP. Principles (§1), Source hierarchy (§2), Test/Workup completeness (§3-§4), Domain extension process (§5), Anti-patterns (§6), Domain extensions log (§7). |
