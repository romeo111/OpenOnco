# Reference Case Specification

**Project:** OpenOnco
**Document:** Reference Case Specification — "Patient Zero"
**Version:** v0.1 (draft)
**Status:** Draft for discussion; final entry of patient data
is deferred until formal consent is obtained
**Prerequisite documents:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md

---

## Purpose of this document

This document formalizes the **reference clinical case**, which serves as:

1. **Acceptance criterion** for the first working version of the system — "when
   the system generates something equivalent, we know it works"
2. **Calibration benchmark** — concrete material against which Clinical Content
   Standards, Knowledge Schema, and Data Standards are validated
3. **Working contract** between Clinical Co-Leads and developers — exactly
   what we are building
4. **Demonstration case** for pitches and public materials (after
   de-identification and obtaining consent)

The reference case is HCV-associated marginal zone lymphoma (HCV-MZL).
Chosen because:
- An expert-verified document of equivalent quality already exists
- The archetype (etiologically_driven) covers all elements of the Knowledge
  Schema well
- Clinically significant but rare — demonstrates the value of automation
- The HCV component provides a natural interdisciplinary link (hematology +
  hepatology + infectious disease)

---

## Critical caveat on status

**As of v0.1 of this document:**

- Real patient-level data is **not included** in this document
- All examples are presented as **structural placeholders**
- Inclusion of real data requires:
  1. Formal **written patient consent** to use their case as a public reference
  2. Full **de-identification** per Data Standards §14
  3. **Re-identification review** by an independent clinician
  4. Approval from all Clinical Co-Leads

Until these conditions are met, the document functions as a **template**
describing the structure and requirements. After they are met, real data is
entered through the governance process into the designated sections.

---

## 1. Reference document (existing artifact)

### 1.1. What we have

The project has one **expert-verified document** at its disposal —
a pair of treatment plans (standard + aggressive options) for a patient
with HCV-MZL. The document was verified by a hematologist as "one of the
best-structured documents I have seen".

This is the **target output**. The question for the system: can it generate
a functionally equivalent document from structured patient input?

### 1.2. Key characteristics of the target output

Without reproducing patient-specific details, the document structure contains:

**Slide 1 — Title**: diagnosis, plan version, basic patient summary
**Slide 2 — Disclaimer**: medical disclaimer + primary goal of the plan
**Slide 3 — Diagnosis summary**: 4 cards — histology, markers,
clinical context, imaging
**Slide 4 — Etiological driver**: why HCV status is critically important
**Slide 5 — Safety layer**: HBV screening, HCC screening, interactions
**Slide 6 — Pre-treatment investigations**: table with priority (critical/
standard/desired/calculation)
**Slide 7 — Timeline**: treatment chronology with milestones
**Slide 8 — Regimen details**: drugs, doses, days, particularities
**Slide 9 — Expected outcomes**: honest comparison with numbers, HR, CI
**Slide 10 — Alternative monotherapy option**: when it fits / does not fit
**Slide 11 — Shared components**: what the standard and
aggressive plans have in common
**Slide 12 — Decision algorithm**: step 1 → step 2 for choosing between options
**Slide 13 — What NOT to do**: prohibited actions + evidence
**Slide 14 — Patient assessment**: parameters/status/implications table
**Slide 15 — Supportive care**: PJP, antiviral, allopurinol, calcium/D,
vaccinations, lifestyle
**Slide 16 — Monitoring schedule**: phases with frequencies
**Slide 17 — Red flags**: categories + symptom list
**Slide 18 — Next steps**: immediate + subsequent actions
**Slide 19 — Closing**: "the final plan is determined by the MDT"

### 1.3. Acceptance criteria (structural)

System v1.0 is considered to pass the reference case test if the generated
output contains:

**Mandatory (critical):**
- [ ] Two plan options (standard + aggressive)
- [ ] Explicit disclaimer with CCS §11 formulation
- [ ] Diagnosis summary with histology + stage + key markers + context
- [ ] Etiological driver section (for etiologically_driven archetype)
- [ ] Pre-treatment investigations with priority class
- [ ] Regimen details (drug, dose, schedule, particularities) for
      both plans
- [ ] Decision algorithm (step 1 → step 2)
- [ ] Red flags: both PRO aggressive + CONTRA aggressive
- [ ] Hard contraindications highlighted
- [ ] Supportive care (per regimen)
- [ ] Monitoring schedule with phases
- [ ] Expected outcomes with source-referenced numbers
- [ ] "What NOT to do" section
- [ ] Knowledge base version stamp + generation timestamp
- [ ] All recommendations sourced (per CCS §5.2)

**Desired (should have):**
- [ ] Timeline visualization
- [ ] Side-by-side comparison of plans
- [ ] Shared components section
- [ ] Alternative monotherapy option (if applicable)
- [ ] Ukrainian localization (primary output language)

**Acceptable gap for v1.0:**
- [ ] Advanced visualizations (timelines, charts) — simpler versions are acceptable
- [ ] Perfectly polished prose — may require human editing
- [ ] Comprehensive patient education layer — Phase 2

---

## 2. Patient profile template

To be filled with real de-identified data after the governance-approved process.

### 2.1. Demographics (template)

```json
{
  "patient_id": "REFERENCE-CASE-0001",
  "gender": "[redacted until consent]",
  "birth_year_cohort": "[redacted until consent, 5-year range]",
  "age_at_diagnosis_range": "[e.g., '45-55']",
  "performance_status_ecog": "[0 | 1 | 2 | 3 | 4]",
  "height_cm": null,
  "weight_kg": null,
  "bsa_m2": null
}
```

### 2.2. Diagnosis (template)

```json
{
  "primary_diagnosis": {
    "disease_entity": "HCV-associated marginal zone lymphoma",
    "icd_o_3": "9699/3",
    "icd_10": "C85.1",
    "who_classification_5th_ed": "Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue",
    "date_of_histological_confirmation": "[redacted]",
    "biopsy_site": "[clinically significant location, e.g., 'root of tongue']",
    "diagnostic_method": "histological biopsy with IHC"
  },
  "staging": {
    "staging_system": "Lugano",
    "stage": "[e.g., IV-E]",
    "b_symptoms": "[boolean]",
    "bulky_disease_over_7cm": false,
    "extranodal_involvement": true
  }
}
```

### 2.3. Molecular/IHC profile (template)

Based on the reference document structure:

```json
{
  "ihc_markers": {
    "CD20": "positive",
    "MNDA": "positive",
    "BCL2": "positive",
    "FoxP1": "positive",
    "c_MYC": "approximately_30_percent",
    "Ki67_percent": "[numeric value, e.g., 60]",
    "double_expressor_status": "no"
  },
  "molecular_tests": {
    "NGS_panel": "[if performed; otherwise null]",
    "FISH_tests": "[if performed; otherwise null]"
  }
}
```

### 2.4. Infectious status (template)

```json
{
  "HCV": {
    "status": "chronic_infection_confirmed",
    "RNA_quantitative": "[positive; value in IU/mL]",
    "genotype": "[if known, otherwise 'not_performed']",
    "duration_known": "[years]",
    "prior_DAA_treatment": "no"
  },
  "HBV": {
    "HBsAg": "[negative | positive]",
    "anti_HBc": "[negative | positive]",
    "anti_HBs": "[negative | positive]"
  },
  "HIV": "[negative | positive | not_tested]"
}
```

### 2.5. Laboratory values (template)

Baseline prior to treatment:

```json
{
  "cbc": {
    "hemoglobin_g_dl": null,
    "platelets_k_ul": null,
    "anc_k_ul": null,
    "alc_k_ul": null
  },
  "liver_panel": {
    "AST_U_L": null,
    "ALT_U_L": null,
    "alkaline_phosphatase_U_L": null,
    "GGT_U_L": null,
    "total_bilirubin_mg_dL": null,
    "albumin_g_dL": null,
    "INR": null
  },
  "renal": {
    "creatinine_mg_dL": null,
    "eGFR": null
  },
  "other": {
    "LDH_U_L": null,
    "B2_microglobulin": null
  },
  "calculations": {
    "FIB_4": null,
    "CrCl_CockcroftGault": null
  }
}
```

### 2.6. Imaging (template)

```json
{
  "modality": "MRI",
  "date": "[redacted]",
  "findings": {
    "primary_lesion": {
      "location": "[e.g., root of tongue with tonsil involvement]",
      "dimensions_mm": "[e.g., 33x36x53]",
      "approximate_size_cm": "[e.g., 5.3]",
      "bulky_by_criteria": false
    },
    "lymph_nodes": [
      {
        "station": "[e.g., Ia]",
        "size_mm": "[e.g., up to 10]",
        "suspicious": true
      }
    ],
    "bone_destruction": false,
    "CNS_involvement": false
  }
}
```

### 2.7. Comorbidities and medications (template)

```json
{
  "comorbidities": "[list of ICD-10 + brief description]",
  "current_medications": "[list of drugs that might affect treatment]",
  "allergies": "[documented allergies]",
  "prior_cancer_treatments": "[if any]"
}
```

### 2.8. Symptoms and clinical concerns (template)

```json
{
  "symptoms_onset": "[timeline]",
  "b_symptoms": {
    "fever": "[boolean]",
    "night_sweats": "[boolean]",
    "weight_loss_over_10_percent": "[boolean]"
  },
  "functional_status_changes": "[description]",
  "clinical_concerns_flagged": {
    "rapid_progression": "[boolean]",
    "suspected_transformation": "[boolean]",
    "performance_decline": "[boolean]"
  }
}
```

---

## 3. Expected system behavior

For the described patient profile, the engine must execute the following logic:

### 3.1. Disease matching

```
INPUT: ICD-O-3 = "9699/3" + HCV-positive status
ENGINE ACTION:
  → Find Disease entity DIS-HCV-MZL
  → Archetype = "etiologically_driven"
  → Document template: etiologically_driven template
```

### 3.2. Applicable indications

```
INPUT: DIS-HCV-MZL + line_of_therapy = 1 + HCV-RNA positive
ENGINE ACTION:
  → Find all Indications where applicable_to matches
  → Returns: [IND-HCV-MZL-1L-STANDARD, IND-HCV-MZL-1L-AGGRESSIVE]
  → Two-plan architecture triggered per Algorithm ALGO-HCV-MZL-1L-CHOICE
```

### 3.3. Algorithm execution

```
STEP 1 (per ALGO-HCV-MZL-1L-CHOICE):
  → Check contraindications to aggressive regimen
  → If any RF-PRO-STANDARD triggered → default = STANDARD
  → Else → continue

STEP 2:
  → Check indicators for aggressive regimen
  → If any RF-PRO-AGGRESSIVE triggered → default = AGGRESSIVE
  → Else → default = STANDARD

EXPECTED for reference case (example):
  Step 1: [depends on actual patient data]
  Step 2: [depends on actual patient data]
  Default: [expected to be STANDARD if no red flags]
  Alternative: [AGGRESSIVE always shown for comparison]
```

### 3.4. Contraindication check

```
For each proposed regimen:
  → Check patient current_medications against Drug interactions
  → Check patient labs against lab-based contraindications
  → Check patient HBV status — if positive without prophylaxis →
    flag CONTRA-HBV-NO-PROPHYLAXIS
  → Check FIB-4 → if >3.25 → trigger dose adjustment for bendamustine

EXPECTED for reference case:
  → List of hard contraindications: [...]
  → List of dose adjustments: [...]
  → List of mandatory concurrent therapies: [...]
```

### 3.5. Pre-treatment workup generation

```
For selected indications:
  → Pull all required_tests
  → Pull all desired_tests
  → Pull calculation-based tests (FIB-4, CrCl)
  → Sort by priority_class

EXPECTED output:
  Critical: [CBC, LFT comprehensive, HCV-RNA, HBV serology, FIB-4]
  Standard: [BMA, LDH, ECG, anti-HIV]
  Desired: [Echo with LVEF]
  Calculation: [FIB-4, CrCl]
```

### 3.6. Supportive care generation

```
For selected regimen:
  → Pull all mandatory_supportive_care
  → Filter by patient contraindications
  → Add vaccination schedule
  → Add monitoring phases

EXPECTED output:
  - PJP prophylaxis (cotrimoxazole)
  - Antiviral prophylaxis (acyclovir)
  - HBV prophylaxis (entecavir IF HBV+)
  - Allopurinol (cycle 1, for TLS)
  - Calcium + Vitamin D
  - Vaccinations (non-live)
  - Lifestyle: alcohol abstention, paracetamol limit 2g/day
```

### 3.7. Expected outcomes

```
For selected indications:
  → Pull expected_outcomes with source_refs
  → Show both STANDARD and AGGRESSIVE for comparison

EXPECTED output (per reference document):
  STANDARD (DAA + BR):
    SVR12 (HCV): ~98%
    ORR lymphoma: 85-90%
    5-year OS: ~85%
    Toxic mortality: 1-2%

  AGGRESSIVE (DAA + R-CHOP):
    SVR12 (HCV): ~98%
    ORR lymphoma: ~88%
    5-year OS: ~83-87%
    Toxic mortality: 2-4%

  Weighted comparison:
    Net OS advantage of AGGRESSIVE: ~2-3 percentage points (within CI)
    Conclusion: STANDARD is preferred default; AGGRESSIVE only with red flags
```

### 3.8. Red flag assessment

```
For the patient profile:
  → Evaluate all relevant RedFlag triggers
  → Categorize as: PRO-AGGRESSIVE | CONTRA-AGGRESSIVE | UNKNOWN
  → Report unknown ones as "needs assessment"

EXPECTED output structure:
  PRO-AGGRESSIVE (triggered): [...]
  PRO-AGGRESSIVE (unknown, needs check): [...]
  CONTRA-AGGRESSIVE (triggered): [...]
  CONTRA-AGGRESSIVE (unknown, needs check): [...]
```

---

## 4. Validation protocol

How we verify that the system output is equivalent to the reference document.

### 4.1. Structural validation (automated)

Script verifies that the engine output contains:

```python
# Pseudocode
def validate_structure(output):
    assert has_two_plans(output)
    assert all_required_sections_present(output, REQUIRED_SECTIONS)
    assert all_recommendations_sourced(output)
    assert disclaimer_text_matches(output, CANONICAL_DISCLAIMER)
    assert knowledge_version_stamped(output)
    assert algorithm_decision_documented(output)
```

### 4.2. Content validation (semi-automated)

Script verifies specific elements:

```python
def validate_content(output, reference):
    assert output.disease == reference.disease
    assert set(output.pre_treatment_tests) >= set(reference.critical_tests)
    assert output.regimens_considered == reference.regimens_considered
    assert output.contraindications_identified >= reference.critical_contraindications
    # ...
```

### 4.3. Expert validation (human)

A Clinical Co-Lead performs a side-by-side comparison:

**Checklist:**
- [ ] The primary recommendation matches (both options)
- [ ] Doses are correct
- [ ] Timeline is correct
- [ ] Red flags are correctly categorized
- [ ] Sources are cited correctly
- [ ] Nothing critical is omitted
- [ ] Nothing substantially extraneous is added
- [ ] Ukrainian terminology is correct
- [ ] Wording is neutral (per CCS §3.3)
- [ ] Output is clinically usable in a tumor board

**Scoring:**
- Pass: the system is clinically usable and can replace manual preparation
- Needs revision: gaps identified, not blockers, but need to be fixed
- Fail: serious clinical errors, system is not ready

### 4.4. Iteration protocol

If validation identifies gaps:

1. **Classify gap:** knowledge base issue | engine logic issue | rendering issue
2. **Fix through standard governance** (CCS §6 for KB changes)
3. **Re-run engine** on cases
4. **Re-validate** with the same reviewer (not a new one, to ensure consistency)
5. **Repeat** until pass or until limitations are documented as acceptable

There is no iteration limit, but if pass has not been achieved after 5 iterations,
that is a signal for an architectural discussion.

---

## 5. Testing with variations

A single patient case is insufficient for complete validation. We create
**variations** based on the reference case to test edge cases.

### 5.1. Test variant generation

From the primary case, we derive hypothetical variations:

**Variant A: Red flag AGAINST aggressive**
Original data + hypothetical LVEF 40%
Expected output: STANDARD plan, aggressive NOT offered due to cardiac risk

**Variant B: Red flag FOR aggressive**
Original data + hypothetical B-symptoms present
Expected output: AGGRESSIVE plan should be shown as default option

**Variant C: Cirrhosis present**
Original data + hypothetical FIB-4 = 4.2
Expected output: Bendamustine dose reduction to 70 mg/m² flagged

**Variant D: HBV co-infection**
Original data + hypothetical HBsAg positive
Expected output: Mandatory entecavir prophylaxis added

**Variant E: Missing critical data**
Original data, but Ki-67 = unknown, LVEF = unknown
Expected output: System requests these tests before full recommendation

**Variant F: Age >75**
Original data + age = 78
Expected output: Dose reduction considered, functional assessment flagged

**Variant G: Concurrent amiodarone**
Original data + hypothetical current medication = amiodarone
Expected output: Hard contraindication for sofosbuvir, alternative DAA
proposed

### 5.2. Test matrix

| Variant | Input change | Expected behavior change |
|---|---|---|
| A | Low LVEF | Only STANDARD; aggressive blocked |
| B | B-symptoms | AGGRESSIVE becomes default |
| C | Cirrhosis | Dose adjustment in regimen |
| D | HBV+ | Entecavir added to supportive care |
| E | Missing data | Tests requested before full plan |
| F | Elderly | Dose modifications, functional assessment |
| G | Amiodarone | Alternative DAA proposed |

Each variant is a separate structured patient JSON + expected
structured output. Stored in `test_cases/reference_variants/`.

### 5.3. Coverage goals

For v1.0 system acceptance:
- All 7 variants above pass
- Plus the original reference case passes
- Plus 3 completely different synthetic cases (not HCV-MZL) fail
  gracefully with a "not yet supported" message

---

## 6. Known limitations and acceptable gaps

For honesty with the team and potential users.

### 6.1. What the reference case does NOT test

- Multi-line therapy decisions (relapsed/refractory)
- Pediatric patients
- Other archetypes (biomarker_driven, stage_driven, etc.)
- Solid tumors
- Radiation therapy planning
- Surgical oncology decisions
- Psychosocial assessment
- Palliative-only scenarios

### 6.2. Architectural limitations at v1.0

- Engine — rule-based, not ML
- No learning from patient outcomes (clinicians review; a data pipeline
  does not feed back)
- Knowledge base manual curation bottleneck
- Document rendering — template-based, limited creativity compared to a human-written
  document
- Ukrainian NLP for free-text input — not in MVP

### 6.3. What counts as an acceptable gap

Acceptable for v1.0:
- Slide layout may visually differ from the reference
- Prose wording may require human editing before public use
- Precise numeric statistics may vary by ±10% if multiple
  sources give different numbers
- Level of detail in supportive care may be simplified

Not acceptable even for v1.0:
- Wrong regimen recommendation
- Wrong dose
- Missed hard contraindication
- Missed emergency indication (such as amiodarone + sofosbuvir)
- Fabricated citations
- Recommendations without sources

---

## 7. Path to production

The reference case visualizes the gap between the current state (nothing)
and a production-ready v1.0.

### 7.1. Phase structure

**Phase 0 — Documentation (now):** 4 foundational documents (this one
included) + governance setup.

**Phase 1 — Knowledge Population:** Clinical Co-Leads curate all
entities for HCV-MZL (Disease, Drugs, Regimens, Indications,
Contraindications, Red Flags, Tests, Supportive Care, Monitoring,
Algorithms) per Knowledge Schema. Target: 1-2 months with dedicated
time.

**Phase 2 — Engine Implementation:** Developers build a rule execution
engine that reads the YAML knowledge base and applies it to patient input.
Target: 2-3 months, parallel with Phase 1.

**Phase 3 — Document Rendering:** Template-based rendering system
that transforms a structured Plan → HTML/PDF. Target: 1-2 months.

**Phase 4 — Reference Case Validation:** Full end-to-end test with the
reference case (after consent) + 7 variants. Target: 2 weeks.

**Phase 5 — Iteration:** Fix gaps found in validation. Target: 1-2
months.

**Phase 6 — Second Disease:** Add another etiologically_driven disease
(e.g., Helicobacter-related MALT lymphoma) to validate schema
generalizability. Target: 1 month.

**Total estimate to usable v1.0:** 6-9 months with an active team of 5-7
people at ~50% time commitment.

### 7.2. Milestones

- **M1:** Phase 0 complete — all 4 foundational documents approved by
  Clinical Co-Leads
- **M2:** HCV-MZL knowledge base 80% populated
- **M3:** Engine MVP runs on a synthetic test case
- **M4:** Engine runs on the reference case, generates the first document
- **M5:** Reference case passes expert validation
- **M6:** Second disease added and validated
- **M7:** v1.0 release (educational/research positioning, not a medical
  device)

---

## 8. What this means for the pitch

For demonstrations to clinician co-founders and potential partners:

### 8.1. What to show now

- CHARTER.md — our governance logic
- CLINICAL_CONTENT_STANDARDS.md — our editorial approach
- KNOWLEDGE_SCHEMA_SPECIFICATION.md — the technical structure
- DATA_STANDARDS.md — the patient model, FHIR/mCODE-compliant
- This document — target output using HCV-MZL as the example
- The reference document itself (HCV-MZL) — as "here is what we want to generate
  automatically" (with consent)

### 8.2. Honest commitment

- 6-9 months to a functional v1.0
- Requires full-team effort, not an evening hobby project
- Knowledge curation is the bottleneck, not coding
- We do not promise "AI that heals" — we promise "structured information
  support that saves 2-4 hours of tumor board preparation"

### 8.3. Why this is not Watson

A brief check for skeptics:

| Watson problem | Our approach |
|---|---|
| Trained on synthetic cases | Validated against a real expert-verified document |
| Recommendations from "single authority" preferences | Recommendations from multiple published guidelines |
| "Black box" scoring | Transparent evidence levels with GRADE |
| LLM generates recommendations | LLM only formats; rules generate recommendations |
| No human medical review per recommendation | Dual medical review mandatory |
| Scaled before validation | Scope deliberately limited to validated domains |
| Sold as "decision maker" | Positioned as "information support" |

---

## 9. Governance of this document

- Template changes (without patient data) — consensus of Tech Lead +
  one Clinical Co-Lead
- Incorporation of real de-identified data — full dual medical
  review + Project Coordinator approval + documented consent
- Re-identification re-review — 12 months after publication, and
  at any material change
- Version bump at each change

---

## 10. Current status and limitations

**v0.1:**
- Structural template is ready
- Real patient data — placeholder, awaiting consent
- Test variants (Section 5) — hypothetical, require clinical
  validation that they are correct edge cases
- Validation protocol (Section 4) — not implemented in code

**What is needed:**
- [ ] Obtain formal written consent from the reference patient
- [ ] Carry out de-identification per Data Standards §14
- [ ] Re-identification review
- [ ] Fill in Section 2 with real de-identified data
- [ ] Calibrate test variants with Clinical Co-Leads
- [ ] Implement validation scripts

---

## 11. Summary: why this document matters

Four documents together (Charter, Content Standards, Knowledge Schema,
Data Standards) defined **how** we build the system. This document
defines **what exactly** we are building — the concrete target functionality
against which everything else is validated.

Without the reference case, the previous documents remain abstract. With
the reference case, the team knows exactly what must be generated and can
work toward that goal methodically.

This is our contract with ourselves and with future users.

---

**Questions, pull requests, suggestions — all are welcome through the
governance process (CHARTER §6).**
