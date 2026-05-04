# Data Standards Specification

**Project:** OpenOnco
**Document:** Data Standards — Patient Model and Interoperability
**Version:** v0.1 (draft)
**Status:** Draft for discussion with the team
**Preceding documents:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md, KNOWLEDGE_SCHEMA_SPECIFICATION.md

---

## Purpose of this document

This document defines **how patient data are modelled at system input**
and how the system interoperates with external sources (EHR,
lab systems, imaging).

Knowledge Schema (Document 2) is the knowledge side.
Data Standards (Document 3) is the patient side.
The Rule Engine connects them.

Without this document:
- There is no clear patient-input structure — UI developers do not know
  which fields to model
- There is no path to integration with EHR/eHealth
- Testing the engine on realistic datasets is impossible
- Developers model the patient ad-hoc

---

## 1. Principles

### 1.1. Standards-first

We **do not invent** a patient schema from scratch. We take **FHIR R4** and
profile it for oncology via **mCODE** (minimal Common Oncology Data
Elements, HL7 FHIR IG).

**Rationale:**
- mCODE is the ASCO standard for oncology data
- FHIR is the de facto standard for medical interoperability
- Future integrations with EHR (including Ukrainian eHealth) will be
  significantly simpler with a FHIR-compatible model
- We do not spend effort on problems already solved by the community

### 1.2. Subset, not superset

For the MVP we take the **minimum subset** of mCODE sufficient for the
first nosology. We expand later. We do not try to cover all of mCODE on day one.

### 1.3. Explicit unknowns

The difference between "field not filled in" and "explicitly unknown" is
critical for clinical safety. We use FHIR `dataAbsentReason`.

### 1.4. Local adaptation layer

Some fields require Ukrainian adaptation — drug codes from the State Formulary,
the official Ukrainian ICD-10 translation, NHSU institutional codes.

### 1.5. No PHI in public repos

Real patient data — never in public git. Test cases —
synthetic or retired/de-identified via the governance process.

---

## 2. Patient data architecture

```
┌─────────────────────────────────────────────────────────┐
│             PATIENT BUNDLE (FHIR Bundle)                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Patient ─── core demographics                           │
│    │                                                      │
│    ├──< Condition (primary cancer diagnosis)             │
│    │     └── mCODE: CancerDiseaseStatus                  │
│    │                                                      │
│    ├──< Condition (comorbidities)                        │
│    │                                                      │
│    ├──< Observation (staging)                            │
│    │     └── mCODE: TNMClinicalStage / PathologicalStage │
│    │                                                      │
│    ├──< Observation (biomarkers)                         │
│    │     └── mCODE: TumorMarkerTest,                     │
│    │          GenomicRegionStudied,                      │
│    │          GenomicVariant                             │
│    │                                                      │
│    ├──< Observation (lab values)                         │
│    │                                                      │
│    ├──< MedicationStatement (current medications)        │
│    │                                                      │
│    ├──< Procedure (prior treatments)                     │
│    │     └── mCODE: CancerRelatedSurgicalProcedure,      │
│    │          CancerRelatedRadiationProcedure            │
│    │                                                      │
│    ├──< MedicationRequest (prior chemo/targeted/immuno)  │
│    │     └── mCODE: CancerRelatedMedicationRequest       │
│    │                                                      │
│    ├──< AllergyIntolerance                               │
│    │                                                      │
│    └──< Observation (performance status)                 │
│          └── mCODE: ECOGPerformanceStatus                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Core Patient profile

### 3.1. Minimum Patient resource

```json
{
  "resourceType": "Patient",
  "id": "patient-case-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-patient"]
  },
  "identifier": [
    {
      "system": "https://oncoopen.ua/patient-id",
      "value": "case-001"
    }
  ],
  "gender": "male",
  "birthDate": "1975",
  "_birthDate": {
    "extension": [
      {
        "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
        "valueCode": "masked",
        "comment": "Year of birth only; exact date redacted for privacy"
      }
    ]
  }
}
```

### 3.2. Required fields

- `resourceType`: "Patient"
- `id`: unique identifier within the project
- `gender`: "male" | "female" | "other" | "unknown"
- `birthDate` OR `_birthDate.extension` (if masked)

### 3.3. Privacy defaults

- We do not store name, address, or contact details
- `birthDate` — year only (for MVP)
- `identifier` — project-local ID, not a passport/medical card number

---

## 4. Primary Cancer Diagnosis

We use mCODE **PrimaryCancerCondition**.

### 4.1. Example

```json
{
  "resourceType": "Condition",
  "id": "primary-cancer-case-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-primary-cancer-condition"]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "clinicalStatus": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
      "code": "active"
    }]
  },
  "verificationStatus": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
      "code": "confirmed"
    }]
  },
  "code": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/icd-o-3",
        "code": "9699/3",
        "display": "Marginal zone B-cell lymphoma, NOS"
      },
      {
        "system": "http://hl7.org/fhir/sid/icd-10",
        "code": "C85.1",
        "display": "B-cell lymphoma, unspecified"
      },
      {
        "system": "http://snomed.info/sct",
        "code": "118605005"
      }
    ],
    "text": "HCV-associated marginal zone lymphoma"
  },
  "bodySite": [{
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "21974007",
      "display": "Base of tongue"
    }],
    "text": "Root of tongue with involvement of tonsil"
  }],
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-histology-morphology-behavior",
      "valueCodeableConcept": {
        "coding": [{
          "system": "http://snomed.info/sct",
          "code": "4797003",
          "display": "Malignant lymphoma, marginal zone"
        }]
      }
    }
  ],
  "recordedDate": "2026-04-07",
  "note": [{
    "text": "Histologically confirmed via biopsy. Ki-67 ~60%. HCV-RNA positive."
  }]
}
```

### 4.2. Required fields

- `code` with at least one standard coding (prefer ICD-O-3 + ICD-10)
- `bodySite` if applicable
- `verificationStatus`: "confirmed" for biopsy-confirmed diagnoses
- `subject`: reference to Patient

### 4.3. Mapping to Knowledge Schema

The engine maps the FHIR `code.coding[icd-o-3]` → KS `Disease.codes.icd_o_3`
to find the relevant Disease entity in the knowledge base.

---

## 5. Staging

### 5.1. TNM or disease-specific

For solid tumors — TNM via mCODE, with the staging type explicit (МОЗ
наказ №473/2026 requires cTNM / pTNM / ypTNM to be stated):

| Type | When | mCODE profile | Simplified field value |
|---|---|---|---|
| **cTNM** | Pre-treatment clinical staging (imaging + biopsy, no surgery) | `TNMClinicalStageGroup` | `"cTNM"` |
| **pTNM** | Post-surgical pathological staging | `TNMPathologicalStageGroup` | `"pTNM"` |
| **ypTNM** | Post-neoadjuvant therapy pathological staging | `TNMPathologicalStageGroup` + `method` extension | `"ypTNM"` |

For lymphomas — Lugano / Ann Arbor via a separate Observation
(`tnm_staging_type: null`).

### 5.2. Example (Lugano for lymphoma)

```json
{
  "resourceType": "Observation",
  "id": "staging-case-001",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "exam"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "21908-9",
      "display": "Stage group clinical Cancer"
    }],
    "text": "Lugano Stage"
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "effectiveDateTime": "2026-04-07",
  "valueCodeableConcept": {
    "text": "Stage IV-E"
  },
  "component": [
    {
      "code": {"text": "B-symptoms"},
      "valueBoolean": false
    },
    {
      "code": {"text": "Bulky disease (>7 cm)"},
      "valueBoolean": false
    },
    {
      "code": {"text": "Extranodal involvement"},
      "valueBoolean": true
    }
  ]
}
```

### 5.3. Example (solid tumor — cTNM vs pTNM)

```json
{
  "resourceType": "Observation",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-tnm-pathological-stage-group"]
  },
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "21902-2",
      "display": "Stage group pathological Cancer"
    }]
  },
  "subject": {"reference": "Patient/patient-001"},
  "effectiveDateTime": "2026-04-07",
  "valueCodeableConcept": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "1229947003",
      "display": "pIIIA"
    }]
  },
  "component": [
    {"code": {"coding": [{"system": "http://loinc.org", "code": "21899-0", "display": "Primary tumor.pathology Cancer"}]},
     "valueCodeableConcept": {"text": "pT2"}},
    {"code": {"coding": [{"system": "http://loinc.org", "code": "21900-6", "display": "Regional lymph nodes.pathology"}]},
     "valueCodeableConcept": {"text": "pN2"}},
    {"code": {"coding": [{"system": "http://loinc.org", "code": "21901-4", "display": "Distant metastases.pathology"}]},
     "valueCodeableConcept": {"text": "pM0"}}
  ]
}

```

The staging type is encoded by `meta.profile` — that IS the cTNM/pTNM
discriminator in FHIR/mCODE; no extra field needed at the FHIR level.

| Staging type | `meta.profile` | LOINC `code` | T/N/M LOINC codes |
|---|---|---|---|
| cTNM | `mcode-tnm-clinical-stage-group` | `21908-9` | `21905-5` / `21906-3` / `21907-1` |
| pTNM | `mcode-tnm-pathological-stage-group` | `21902-2` | `21899-0` / `21900-6` / `21901-4` |
| ypTNM | `mcode-tnm-pathological-stage-group` + `method` ext | `21902-2` | same as pTNM |

The simplified input field `tnm_staging_type` (§11) drives this profile
selection when the engine serialises to FHIR.

### 5.4. Notes

- "unknown" for staging is a valid value; use `dataAbsentReason`
- Combined staging systems — separate Observations (e.g.,
  ISS + R-ISS for multiple myeloma)
- `tnm_staging_type` in the simplified input (§11) maps to the mCODE
  profile selection here; the engine performs the mapping automatically

---

## 6. Biomarkers and molecular profile

### 6.1. mCODE TumorMarkerTest (for protein/serum/IHC markers)

```json
{
  "resourceType": "Observation",
  "id": "biomarker-ki67-case-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-tumor-marker-test"]
  },
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "85319-2",
      "display": "Ki-67 [Presence] in Tissue by Immune stain"
    }],
    "text": "Ki-67 proliferation index"
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "effectiveDateTime": "2026-04-07",
  "valueQuantity": {
    "value": 60,
    "unit": "%",
    "system": "http://unitsofmeasure.org",
    "code": "%"
  },
  "specimen": {"reference": "Specimen/biopsy-case-001"}
}
```

### 6.2. mCODE Variant (for genomic mutations)

```json
{
  "resourceType": "Observation",
  "id": "variant-hypothetical-case",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-genetic-variant"]
  },
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "laboratory"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "69548-6",
      "display": "Genetic variant assessment"
    }]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "component": [
    {
      "code": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "48018-6",
          "display": "Gene studied"
        }]
      },
      "valueCodeableConcept": {
        "coding": [{
          "system": "http://www.genenames.org/geneId",
          "code": "HGNC:3236",
          "display": "EGFR"
        }]
      }
    },
    {
      "code": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "48004-6",
          "display": "DNA change (c.HGVS)"
        }]
      },
      "valueCodeableConcept": {
        "text": "c.2573T>G"
      }
    },
    {
      "code": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "48005-3",
          "display": "Amino acid change (pHGVS)"
        }]
      },
      "valueCodeableConcept": {
        "text": "p.Leu858Arg"
      }
    },
    {
      "code": {"text": "Interpretation"},
      "valueCodeableConcept": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "LA6576-8",
          "display": "Pathogenic"
        }]
      }
    }
  ]
}
```

### 6.3. Virology markers (HCV status)

```json
{
  "resourceType": "Observation",
  "id": "hcv-rna-case-001",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "11011-4",
      "display": "Hepatitis C virus RNA [#/volume] (viral load) in Serum or Plasma by NAA with probe detection"
    }]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "effectiveDateTime": "2026-04-01",
  "valueQuantity": {
    "value": 1500000,
    "unit": "IU/mL",
    "system": "http://unitsofmeasure.org",
    "code": "[IU]/mL"
  }
}
```

---

## 7. Performance Status

### 7.1. mCODE ECOGPerformanceStatus

```json
{
  "resourceType": "Observation",
  "id": "ecog-case-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-ecog-performance-status"]
  },
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "89247-1",
      "display": "ECOG Performance Status score"
    }]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "effectiveDateTime": "2026-04-07",
  "valueInteger": 1
}
```

### 7.2. Valid values

- ECOG: 0, 1, 2, 3, 4, 5
- Karnofsky: 0-100 (step 10) — separate mCODE KarnofskyPerformanceStatus profile
- Unknown → `dataAbsentReason`

---

## 8. Lab values

Standard FHIR Observations with LOINC codes. Critical for the engine —
lab values that affect dose modification or contraindications.

### 8.1. Minimum set for MVP (hemato-oncology)

```
CBC:
  - 6690-2   Leukocytes [#/volume] in Blood by Automated count
  - 789-8    Erythrocytes [#/volume] in Blood by Automated count
  - 718-7    Hemoglobin [Mass/volume] in Blood
  - 777-3    Platelets [#/volume] in Blood by Automated count
  - 751-8    Neutrophils [#/volume] in Blood by Automated count
  - 731-0    Lymphocytes [#/volume] in Blood by Automated count

Liver panel:
  - 1742-6   Alanine aminotransferase [Enzymatic activity/volume] (ALT)
  - 1920-8   Aspartate aminotransferase [Enzymatic activity/volume] (AST)
  - 6768-6   Alkaline phosphatase [Enzymatic activity/volume] (ALP)
  - 2324-2   Gamma glutamyl transferase (GGT)
  - 1975-2   Bilirubin.total [Mass/volume] in Serum or Plasma
  - 1751-7   Albumin [Mass/volume] in Serum or Plasma

Renal:
  - 2160-0   Creatinine [Mass/volume] in Serum or Plasma
  - 3097-3   eGFR (calculated)

Other critical:
  - 14804-9  LDH [Enzymatic activity/volume] in Serum or Plasma
  - 2028-9   β-2 microglobulin [Mass/volume] in Serum or Plasma

Coagulation:
  - 6301-6   INR in Platelet poor plasma by Coagulation assay
```

### 8.2. Example

```json
{
  "resourceType": "Observation",
  "id": "alt-case-001",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "laboratory"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "1742-6",
      "display": "Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma"
    }]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "effectiveDateTime": "2026-04-01",
  "valueQuantity": {
    "value": 45,
    "unit": "U/L",
    "system": "http://unitsofmeasure.org",
    "code": "U/L"
  },
  "referenceRange": [{
    "low": {"value": 5, "unit": "U/L"},
    "high": {"value": 40, "unit": "U/L"},
    "type": {"text": "normal"}
  }]
}
```

---

## 9. Prior treatments

### 9.1. mCODE CancerRelatedMedicationRequest

For prior systemic therapy.

```json
{
  "resourceType": "MedicationRequest",
  "id": "prior-chemo-case-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-cancer-related-medication-request"]
  },
  "status": "completed",
  "intent": "order",
  "medicationCodeableConcept": {
    "coding": [{
      "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
      "code": "121191",
      "display": "rituximab"
    }]
  },
  "subject": {"reference": "Patient/patient-case-001"},
  "authoredOn": "2025-08-15",
  "reasonReference": [{"reference": "Condition/primary-cancer-case-001"}]
}
```

### 9.2. Line of therapy tracking

A separate extension — which line of therapy this is, with associated outcomes.

```json
"extension": [{
  "url": "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-therapy-line-number",
  "valueInteger": 1
}]
```

---

## 10. Performance and dosing calculations

### 10.1. Height, weight, BSA

For dose calculations — required Observations:

- LOINC 8302-2: Body height
- LOINC 29463-7: Body weight
- BSA calculated from height/weight (not stored separately; calculated)

The engine uses the DuBois formula by default:
```
BSA = 0.007184 × height^0.725 × weight^0.425
(height in cm, weight in kg, BSA in m²)
```

### 10.2. Creatinine clearance

Cockcroft-Gault:
```
CrCl = ((140 - age) × weight × (0.85 if female)) / (72 × serum_creatinine)
```

The engine calculates automatically when creatinine + age + weight are available.

### 10.3. FIB-4 (for HCV context)

```
FIB-4 = (age × AST) / (platelet_count × √ALT)
```

Critical for bendamustine dosing. Calculated by the engine.

---

## 11. Structured input for MVP UI

For the first UI, a **simplified subset** of FHIR-compatible format:

```json
{
  "patient": {
    "id": "case-001",
    "gender": "male",
    "birth_year": 1975,
    "height_cm": 178,
    "weight_kg": 82,
    "performance_status_ecog": 1
  },
  "diagnosis": {
    "icd_o_3": "9699/3",
    "disease_entity": "HCV-associated marginal zone lymphoma",
    "staging_system": "Lugano",
    "stage": "IV-E",
    "tnm_staging_type": null,
    "histologic_grade": null,
    "verification_method": "histological_biopsy",
    "biopsy_date": "2026-04-07",
    "body_sites": ["root_of_tongue", "tonsil"]
  },
  "molecular_profile": {
    "ihc_markers": {
      "CD20": "positive",
      "MNDA": "positive",
      "BCL2": "positive",
      "FoxP1": "positive",
      "c_MYC": "approximately_30_percent",
      "Ki67": 60
    },
    "mutations": [],
    "fusions": []
  },
  "infectious_status": {
    "HCV_RNA": {"value": 1500000, "unit": "IU/mL", "date": "2026-04-01"},
    "HBV_serology": {
      "HBsAg": "negative",
      "anti_HBc": "negative",
      "anti_HBs": "negative"
    },
    "HIV": "negative"
  },
  "lab_values": {
    "cbc": {
      "hemoglobin_g_dl": 14.2,
      "platelets_k_ul": 220,
      "anc_k_ul": 4.5,
      "alc_k_ul": 1.8
    },
    "chemistry": {
      "AST_U_L": 38,
      "ALT_U_L": 45,
      "alkaline_phosphatase_U_L": 85,
      "GGT_U_L": 42,
      "total_bilirubin_mg_dL": 0.9,
      "albumin_g_dL": 4.1,
      "creatinine_mg_dL": 0.9,
      "LDH_U_L": 220
    }
  },
  "comorbidities": [
    {"icd10": "I10", "description": "Essential hypertension", "status": "controlled"}
  ],
  "current_medications": [
    {"rxnorm": "197379", "name": "lisinopril", "dose": "10 mg daily"}
  ],
  "allergies": [],
  "prior_treatments": [],
  "symptoms": {
    "b_symptoms": {
      "fever": false,
      "night_sweats": false,
      "weight_loss_10_percent": false
    }
  },
  "clinical_concerns": {
    "rapid_progression": false,
    "bulky_disease_over_7cm": false,
    "known_cardiac_disease": false,
    "lvef_available": false,
    "lvef_value": null
  }
}
```

The engine converts this to a FHIR Bundle internally when required for
integrations. The simplified format is used for the UI.

### 11.1. Optional `diagnosis` fields (МОЗ наказ №473 / 2026-04-07)

These fields are optional (`null` when not applicable) but required by МОЗ
order №473 when present in the pathology report:

| Field | Accepted values | Notes |
|---|---|---|
| `histologic_grade` | `"G1"` / `"G2"` / `"G3"` / `"G4"` / `"GX"` | `null` for hematologic malignancies where grade is encoded in the disease entity or a disease-specific system (Gleason/ISUP, WHO CNS grade, Ki-67-based NET grade) |
| `tnm_staging_type` | `"cTNM"` / `"pTNM"` / `"ypTNM"` / `null` | `null` for lymphomas (Ann Arbor / Lugano) and other non-TNM systems |
| `verification_method` | `"histological_biopsy"` / `"cytological"` / `"liquid_biopsy"` / `"imaging_only"` / `"clinical"` | Maps to FHIR `verificationStatus`; required per nakas 473 §4 |

---

## 12. DataAbsentReason codes

For explicit representation of unknowns:

| Code | When to use |
|---|---|
| `unknown` | The value is genuinely unknown |
| `asked-unknown` | The patient was asked but does not know |
| `temp-unknown` | Test result is pending |
| `not-asked` | Was not asked |
| `asked-declined` | Patient declined to answer |
| `masked` | Known but concealed (for privacy) |
| `not-applicable` | Does not apply to this patient |
| `unsupported` | The format does not support this data type |
| `as-text` | Available only as free text |
| `error` | Measurement error |
| `not-a-number` | Test could not be performed |
| `negative-infinity` / `positive-infinity` | Off-scale |
| `not-performed` | Test was not performed |
| `not-permitted` | Prohibited from returning |

### 12.1. Engine behavior

The engine distinguishes:
- **Missing with reason** (e.g., "not-performed"): the test may be recommended
  as a required pre-treatment step
- **Unknown-unknown** (field simply not filled in): triggers UI validation
  to ask the clinician
- **Explicitly excluded** (not-applicable): the engine does not recommend performing the test

---

## 13. Ukraine-specific extensions

### 13.1. Official ICD-10 code (Ukrainian translation)

We use the official Ukrainian ICD-10 version from the Ministry of Health + ICD-10
International. We store both:

```json
"code": {
  "coding": [
    {"system": "http://hl7.org/fhir/sid/icd-10", "code": "C85.1"},
    {"system": "http://moz.gov.ua/icd-10-uk", "code": "C85.1",
     "display": "B-cell lymphoma, unspecified (Ukrainian official)"}
  ]
}
```

### 13.2. State Formulary of Ukraine

For drugs — an extension with a reference to the State Formulary:

```json
{
  "medicationCodeableConcept": {
    "coding": [
      {"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "121191"},
      {"system": "http://moz.gov.ua/drug-formulary", "code": "[UA formulary code]"}
    ]
  },
  "extension": [{
    "url": "http://oncoopen.ua/StructureDefinition/reimbursement-status",
    "valueCodeableConcept": {
      "coding": [{
        "system": "http://oncoopen.ua/nszu-reimbursement",
        "code": "reimbursed",
        "display": "Reimbursed by NHSU"
      }]
    }
  }]
}
```

### 13.3. Integration with eHealth

Future work (not MVP). Ukrainian eHealth uses FHIR R4, so the patient
model must be import-compatible. Specific mapping details — after MVP
stabilization.

---

## 14. De-identification requirements

### 14.1. For test cases

None of the following should be present in public repos:
- First name, last name, initials
- Full dates (of birth, biopsy, hospitalisation)
- The institution where treatment was administered
- Region, city (except major cities >100k population for demographics)
- Unique identifying combinations (rare cancer + rare occupation + age to the year)
- Medical identifiers (chart number, insurance number)

### 14.2. Safe tokens

For test cases, use:
- Relative dates: "day 0" instead of "2026-04-07"
- Age ranges: "50-55" instead of "52"
- Institutional tokens: "[tertiary-oncology-center]"
- Patient IDs: "case-001", not real identifiers

### 14.3. Re-identification review

Before publishing any test case derived from a real patient:
1. Hypothetical re-identification attempt
2. Review by a clinician who was not involved in the case
3. Sign-off from governance

---

## 15. Validation schema

For every incoming patient document:

### 15.1. Schema validation

Validate against FHIR R4 + mCODE StructureDefinitions via standard tools:

- **HAPI FHIR Validator** (Java)
- **fhir.resources** (Python)
- **Firely .NET SDK**

### 15.2. Semantic validation

Additionally, the engine checks:
- Code system consistency (ICD-O + ICD-10 are aligned)
- Units consistency (SI and US customary are not mixed)
- Temporal logic (biopsy is not in the future; labs are not excessively old)
- Reference resolution (all `Reference` values resolve)

### 15.3. Completeness for the engine

The engine verifies whether patient data are sufficient to operate:
- Disease identified → yes
- Biomarkers relevant to the disease → critical hit list
- Labs relevant to proposed regimens → checked
- Performance status → mandatory
- If anything is missing → the engine generates a list of required tests

---

## 16. Example: complete minimal Patient Bundle

```json
{
  "resourceType": "Bundle",
  "id": "patient-bundle-case-001",
  "type": "collection",
  "entry": [
    {"resource": {"resourceType": "Patient", "id": "patient-case-001", "...": "..."}},
    {"resource": {"resourceType": "Condition", "id": "primary-cancer-case-001", "...": "..."}},
    {"resource": {"resourceType": "Observation", "id": "staging-case-001", "...": "..."}},
    {"resource": {"resourceType": "Observation", "id": "ecog-case-001", "...": "..."}},
    {"resource": {"resourceType": "Observation", "id": "biomarker-ki67-case-001", "...": "..."}},
    {"resource": {"resourceType": "Observation", "id": "hcv-rna-case-001", "...": "..."}},
    {"resource": {"resourceType": "Observation", "id": "alt-case-001", "...": "..."}}
  ]
}
```

---

## 17. Data flow

### 17.1. Happy path

```
1. Clinician inputs patient data via UI (structured form)
2. UI serializes to FHIR Bundle (internally)
3. FHIR Bundle → Patient Context object (engine internal format)
4. Engine queries Knowledge Base:
   - Find Disease entity matching ICD-O-3
   - Find applicable Indications
   - Check Contraindications against medications/labs
   - Evaluate RedFlags against symptoms/labs
   - Apply Algorithm to select default + alternative
5. Engine returns structured Plan (two variants)
6. Rendering layer generates HTML/PDF documents
7. Clinician reviews and uses in tumor board
```

### 17.2. Missing data handling

```
If required data missing:
  → Engine returns PartialPlan with:
     - list of missing required tests
     - indicated preliminary recommendations
     - flags for "cannot generate until X resolved"
  → UI prompts clinician to gather data
  → Once data provided, re-run engine
```

---

## 18. Future interoperability

### 18.1. FHIR import

Future: accepting FHIR Bundles from an external EHR. Standard FHIR R4
POST endpoint:
```
POST /fhir/Patient-Bundle
Content-Type: application/fhir+json
Authorization: Bearer [token]
```

### 18.2. FHIR export

Generated treatment plans can be exported as a FHIR CarePlan
resource for import back into an EHR (if the EHR supports it).

### 18.3. HL7 v2 bridge

For legacy systems without FHIR — a bridge via HL7 v2 OMP^O09 messages
(as the closest analogue). This is separate work, not for MVP.

### 18.4. Ukrainian eHealth

A future phase. Integration via the eHealth Central API. Project registration
as a learning platform / research tool will be required.

---

## 19. Governance of this document

- Major changes (breaking patient schema) — consensus of Tech Lead +
  all Clinical Co-Leads + 14 days of public comment
- Minor additions (new optional fields) — Tech Lead + one Co-Lead
- Field deprecation — 6 months' notice with a migration guide
- Changelog in CHANGELOG-DATA-STANDARDS.md

---

## 20. Current status and limitations

**v0.1:**
- Minimum subset of FHIR/mCODE for the first nosology
- Does not cover all mCODE profiles
- Ukraine-specific extensions — draft only
- eHealth integration — future phase

**Known limitations:**
- Not modelled: genetic counseling, family history, advanced directives
- Imaging — via references only, not detailed DICOM metadata
- Pathology reports — as text, not structured (NLP phase later)
- Translational/research data — out of scope for MVP

**What is needed after v0.1:**
- Implementation of HCV-MZL input in this schema
- Validation that the engine can read a real case
- Calibration against the real UI workflow
- If anything is missing — add it

---

**Pull requests — welcomed. Especially regarding Ukrainian extensions and
real-world FHIR compatibility.**
