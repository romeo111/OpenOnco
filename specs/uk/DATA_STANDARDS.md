# Data Standards Specification

**Проєкт:** OpenOnco
**Документ:** Data Standards — Patient Model and Interoperability
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з командою
**Попередні документи:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md, KNOWLEDGE_SCHEMA_SPECIFICATION.md

---

## Мета документа

Цей документ визначає, **як моделюються пацієнтські дані на вході в
систему** і як система інтероперує з зовнішніми джерелами (EHR,
lab systems, imaging).

Knowledge Schema (Document 2) — це сторона знань.
Data Standards (Document 3) — це сторона пацієнта.
Rule Engine з'єднує їх.

Без цього документа:
- Немає чіткої структури patient input — UI-розробники не знають,
  які поля моделювати
- Немає шляху до інтеграції з EHR/eHealth
- Неможливо тестувати engine на realistic datasets
- Розробники моделюють пацієнта ad-hoc

---

## 1. Принципи

### 1.1. Standards-first

Ми **не винаходимо** схему пацієнта з нуля. Беремо **FHIR R4** і
профілюємо його для онкології через **mCODE** (minimal Common
Oncology Data Elements, HL7 FHIR IG).

**Мотивація:**
- mCODE — стандарт ASCO для онкологічних даних
- FHIR — фактичний стандарт медичної інтероперабельності
- Майбутні інтеграції з EHR (включно з українським eHealth) значно
  простіші з FHIR-сумісною моделлю
- Не тратимо зусилля на проблеми, які вже розв'язані community

### 1.2. Subset, not superset

Для MVP беремо **мінімальне підмножина** mCODE, достатню для першої
нозології. Розширяємо пізніше. Не намагаємось покрити всю mCODE з
першого дня.

### 1.3. Explicit unknowns

Різниця між "поле не заповнене" і "явно невідомо" — критична для
clinical safety. Використовуємо FHIR dataAbsentReason.

### 1.4. Local adaptation layer

Деякі поля потребують української адаптації — коди препаратів за
Державним формуляром, ICD-10 офіційний український переклад,
інституційні коди НСЗУ.

### 1.5. No PHI in public repos

Реальні пацієнтські дані — ніколи в public git. Test cases —
synthetic або retired/deidentified з governance процесу.

---

## 2. Архітектура даних пацієнта

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

### 3.1. Мінімальний Patient resource

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
- `id`: унікальний ідентифікатор в проекті
- `gender`: "male" | "female" | "other" | "unknown"
- `birthDate` OR `_birthDate.extension` (якщо замасковано)

### 3.3. Privacy defaults

- Не зберігаємо name, address, contact details
- birthDate — тільки рік (для MVP)
- identifier — project-local ID, не passport/medical card

---

## 4. Primary Cancer Diagnosis

Використовуємо mCODE **PrimaryCancerCondition**.

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
- `verificationStatus`: "confirmed" для біопсично-підтверджених
- `subject`: reference до Patient

### 4.3. Mapping до Knowledge Schema

Engine маппить FHIR `code.coding[icd-o-3]` → KS `Disease.codes.icd_o_3`
для знаходження релевантної Disease entity в knowledge base.

---

## 5. Staging

### 5.1. TNM або disease-specific

Для solid tumors — TNM через mCODE TNMClinicalStageGroup.
Для лімфом — Lugano / Ann Arbor через окремий Observation.

### 5.2. Example (Lugano для лімфоми)

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

### 5.3. Notes

- "unknown" на staging — це valid value, треба використовувати
  dataAbsentReason
- Combination staging systems — окремі Observation (наприклад,
  ISS + R-ISS для MM)

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
- Karnofsky: 0-100 (step 10) — окремий profile mCODE KarnofskyPerformanceStatus
- Невідомо → dataAbsentReason

---

## 8. Lab values

Standard FHIR Observations з LOINC кодами. Критично для engine —
лабораторні значення, що впливають на dose modification або
contraindications.

### 8.1. Мінімальний набір для MVP (онкогематологія)

```
CBC:
  - 6690-2   Leukocytes [#/volume] in Blood by Automated count
  - 789-8    Erythrocytes [#/volume] in Blood by Automated count
  - 718-7    Hemoglobin [Mass/volume] in Blood
  - 777-3    Platelets [#/volume] in Blood by Automated count
  - 751-8    Neutrophils [#/volume] in Blood by Automated count
  - 731-0    Lymphocytes [#/volume] in Blood by Automated count

Liver panel:
  - 1742-6   Alanine aminotransferase [Enzymatic activity/volume] (АЛТ)
  - 1920-8   Aspartate aminotransferase [Enzymatic activity/volume] (АСТ)
  - 6768-6   Alkaline phosphatase [Enzymatic activity/volume] (ЛФ)
  - 2324-2   Gamma glutamyl transferase (ГГТ)
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

Для попередньої системної терапії.

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

Окреме розширення — яка це лінія терапії, з якими outcomes.

```json
"extension": [{
  "url": "http://hl7.org/fhir/us/mcode/StructureDefinition/mcode-therapy-line-number",
  "valueInteger": 1
}]
```

---

## 10. Performance and dosing calculations

### 10.1. Height, weight, BSA

Для dose calculations — необхідні Observations:

- LOINC 8302-2: Body height
- LOINC 29463-7: Body weight
- BSA calculated from height/weight (не зберігається окремо; calculated)

Engine використовує DuBois формулу за замовчуванням:
```
BSA = 0.007184 × height^0.725 × weight^0.425
(height in cm, weight in kg, BSA in m²)
```

### 10.2. Creatinine clearance

Cockcroft-Gault:
```
CrCl = ((140 - age) × weight × (0.85 if female)) / (72 × serum_creatinine)
```

Engine автоматично обчислює якщо є креатинін + вік + вага.

### 10.3. FIB-4 (для HCV context)

```
FIB-4 = (age × AST) / (platelet_count × √ALT)
```

Критичний для bendamustine dosing. Обчислюється engine.

---

## 11. Structured input for MVP UI

Для першого UI, **спрощений субсет** FHIR-compatible формату:

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

Engine конвертує це в FHIR Bundle внутрішньо, якщо потрібно для
інтеграцій. Для UI використовується спрощений формат.

---

## 12. DataAbsentReason codes

Для явного representation невідомого:

| Code | Коли використовувати |
|---|---|
| `unknown` | Значення справді невідоме |
| `asked-unknown` | Пацієнта спитали, він не знає |
| `temp-unknown` | Результат тесту очікується |
| `not-asked` | Не питали |
| `asked-declined` | Пацієнт відмовився відповідати |
| `masked` | Відомо, але приховано (для privacy) |
| `not-applicable` | Не застосовується до цього пацієнта |
| `unsupported` | Формат не підтримує цей тип даних |
| `as-text` | Доступне тільки як free text |
| `error` | Помилка вимірювання |
| `not-a-number` | Тест не вдалося виконати |
| `negative-infinity` / `positive-infinity` | Off-scale |
| `not-performed` | Тест не виконувався |
| `not-permitted` | Заборонено повертати |

### 12.1. Engine behavior

Engine розрізняє:
- **Missing with reason** (e.g., "not-performed"): tests може бути рекомендований
  як необхідний pre-treatment
- **Unknown-unknown** (field просто не заповнено): triggers UI validation
  to ask clinician
- **Explicitly excluded** (not-applicable): engine не рекомендує перевіряти

---

## 13. Ukraine-specific extensions

### 13.1. Код МКХ-10 офіційний (український переклад)

Використовуємо офіційну українську версію МКХ-10 від МОЗ + ICD-10
International. Зберігаємо обидва:

```json
"code": {
  "coding": [
    {"system": "http://hl7.org/fhir/sid/icd-10", "code": "C85.1"},
    {"system": "http://moz.gov.ua/icd-10-uk", "code": "C85.1",
     "display": "Лімфома В-клітинна, неуточнена"}
  ]
}
```

### 13.2. Державний формуляр України

Для препаратів — розширення з reference в Державний формуляр:

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
        "display": "Відшкодовується НСЗУ"
      }]
    }
  }]
}
```

### 13.3. Інтеграція з eHealth

Майбутня робота (не MVP). eHealth України використовує FHIR R4, тому
patient model має бути import-compatible. Конкретні mapping details
— після стабілізації MVP.

---

## 14. De-identification requirements

### 14.1. Для test cases

Жодна з наступних не повинна бути в public repos:
- Ім'я, прізвище, ініціали
- Повні дати (народження, біопсії, госпіталізації)
- Заклад, де проходило лікування
- Регіон, місто (крім великих міст >100k населення для demographics)
- Унікальні комбінації, що ідентифікують (рідкісний рак + рідкісна
  професія + вік з точністю до року)
- Медичні ідентифікатори (номер картки, страховий номер)

### 14.2. Safe tokens

Для test cases використовуються:
- Relative dates: "day 0" замість "2026-04-07"
- Age ranges: "50-55" замість "52"
- Institutional tokens: "[tertiary-oncology-center]"
- Patient IDs: "case-001", не реальні

### 14.3. Re-identification review

Перед публікацією будь-якого test case з реального пацієнта:
1. Hypothetical re-identification attempt
2. Review клініцистом, що не був причетний до case
3. Sign-off від governance

---

## 15. Validation schema

Для кожного вхідного patient document:

### 15.1. Schema validation

Validate проти FHIR R4 + mCODE StructureDefinitions через standard
tools:

- **HAPI FHIR Validator** (Java)
- **fhir.resources** (Python)
- **Firely .NET SDK**

### 15.2. Semantic validation

Додатково engine перевіряє:
- Code system consistency (ICD-O + ICD-10 узгоджені)
- Units consistency (не змішано SI і US customary)
- Temporal logic (біопсія не в майбутньому, лабораторні не занадто старі)
- Reference resolution (всі `Reference` resolve)

### 15.3. Completeness для engine

Engine перевіряє, чи patient data достатні для роботи:
- Disease identified → так
- Biomarkers relevant до disease → hit list критичних
- Labs relevant до proposed regimens → перевірка
- Performance status → обов'язковий
- Якщо чогось бракує → engine генерує list of required tests

---

## 16. Example: повний minimal Patient Bundle

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

Майбутнє: прийом FHIR Bundles з external EHR. Стандартний FHIR R4
POST endpoint:
```
POST /fhir/Patient-Bundle
Content-Type: application/fhir+json
Authorization: Bearer [token]
```

### 18.2. FHIR export

Згенеровані плани лікування можна експортувати як FHIR CarePlan
resource для import назад в EHR (якщо EHR підтримує).

### 18.3. HL7 v2 bridge

Для legacy систем без FHIR — bridge через HL7 v2 OMP^O09 messages
(як найближчий analog). Це окрема робота не для MVP.

### 18.4. Ukrainian eHealth

Фаза майбутнього. Інтеграція через API eHealth Central. Потрібна
реєстрація проекту як learning platform / research tool.

---

## 19. Governance цього документа

- Major changes (breaking patient schema) — consensus Tech Lead +
  all Clinical Co-Leads + 14 днів public comment
- Minor additions (нові optional fields) — Tech Lead + один Co-Lead
- Field deprecation — 6 місяців notice з migration guide
- Changelog в CHANGELOG-DATA-STANDARDS.md

---

## 20. Поточний статус і обмеження

**v0.1:**
- Мінімальне підмножина FHIR/mCODE для першої нозології
- Не покриває всі mCODE profiles
- Ukraine-specific extensions — draft only
- eHealth integration — фаза майбутнього

**Відомі обмеження:**
- Не моделюємо: genetic counseling, family history, advanced directives
- Imaging — тільки через references, не detailed DICOM metadata
- Pathology reports — як text, не structured (NLP phase later)
- Translational/research data — out of scope для MVP

**Що треба після v0.1:**
- Реалізація HCV-MZL input у цій схемі
- Validation що engine може прочитати реальний case
- Calibration під реальний UI workflow
- Якщо щось не вистачає — додати

---

**Pull requests — welcomed. Особливо щодо Ukrainian extensions і
real-world FHIR compatibility.**
