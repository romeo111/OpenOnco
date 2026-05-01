# Reference Case Specification

**Проєкт:** OpenOnco
**Документ:** Reference Case Specification — "Patient Zero"
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення; фінальне введення пацієнтських даних
відкладається до отримання формальної згоди
**Попередні документи:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md

---

## Мета документа

Цей документ формалізує **референсний клінічний випадок**, який служить:

1. **Acceptance criterion** для першої робочої версії системи — "коли
   система згенерує щось еквівалентне, ми знаємо, що вона працює"
2. **Calibration benchmark** — конкретний матеріал, на якому валідуються
   Clinical Content Standards, Knowledge Schema, Data Standards
3. **Working contract** між Clinical Co-Leads і розробниками — що саме
   ми будуємо
4. **Demonstration case** для pitch і публічних матеріалів (після
   деідентифікації і отримання згоди)

Референсний випадок — HCV-asociated marginal zone lymphoma (HCV-MZL).
Обраний тому, що:
- Існує вже expert-verified документ еквівалентного рівня
- Archetype (etiologically_driven) добре покриває всі елементи Knowledge
  Schema
- Клінічно значимий, але рідкий — демонструє цінність автоматизації
- HCV-компонент дає природний міжнауковий зв'язок (гематологія +
  гепатологія + інфекціоністика)

---

## Критичне застереження про статус

**На момент v0.1 цього документа:**

- Реальні patient-level дані **не включені** в цей документ
- Всі приклади представлені як **structural placeholders**
- Включення реальних даних вимагає:
  1. Формальної **письмової згоди пацієнта** на використання його
     випадку як публічного референсного
  2. Повної **деідентифікації** per Data Standards §14
  3. **Re-identification review** незалежним клініцистом
  4. Approval від всіх Clinical Co-Leads

До виконання цих умов документ функціонує як **template**, що
описує структуру і вимоги. Після виконання — реальні дані вносяться
через governance процес у визначені секції.

---

## 1. Reference document (existing artifact)

### 1.1. Що ми маємо

Проект має у своєму розпорядженні один **expert-verified документ** —
пара планів лікування (стандартний + агресивний варіанти) для пацієнта
з HCV-MZL. Документ верифікований гематологом як "один з найкращих по
структурі, що я бачив".

Це **target output**. Питання для системи: чи може вона згенерувати
функціонально еквівалентний документ з структурованого patient input?

### 1.2. Ключові характеристики target output

Без відтворення пацієнтських специфіки, структура документа містить:

**Слайд 1 — Title**: диагноз, версія плану, базова пацієнтська довідка
**Слайд 2 — Disclaimer**: медичний disclaimer + пріоритетна мета плану
**Слайд 3 — Diagnosis summary**: 4 cards — гістологія, маркери,
клінічний контекст, imaging
**Слайд 4 — Etiological driver**: чому HCV-status принципово важливий
**Слайд 5 — Safety layer**: HBV screening, HCC screening, interactions
**Слайд 6 — Pre-treatment investigations**: таблиця з priority (critical/
standard/desired/calculation)
**Слайд 7 — Timeline**: хронологія лікування з milestones
**Слайд 8 — Regimen details**: препарати, дози, дні, particularities
**Слайд 9 — Expected outcomes**: честне порівняння з числами, HR, CI
**Слайд 10 — Alternative monotherapy option**: коли підходить/не підходить
**Слайд 11 — Shared components**: що спільного між стандартним і
агресивним планами
**Слайд 12 — Decision algorithm**: крок 1 → крок 2 для вибору між варіантами
**Слайд 13 — What NOT to do**: заборонені дії + evidence
**Слайд 14 — Patient assessment**: параметри/статус/implications таблиця
**Слайд 15 — Supportive care**: PJP, antiviral, allopurinol, calcium/D,
vaccinations, lifestyle
**Слайд 16 — Monitoring schedule**: phases з частотами
**Слайд 17 — Red flags**: категорії + список симптомів
**Слайд 18 — Next steps**: першочергові + наступні дії
**Слайд 19 — Closing**: "остаточний план визначає МДК"

### 1.3. Acceptance criteria (структурні)

Система v1.0 вважається passing reference case test, якщо згенерований
output містить:

**Обов'язково (critical):**
- [ ] Два варіанти плану (стандартний + агресивний)
- [ ] Явний disclaimer з CCS §11 formulating
- [ ] Diagnosis summary з histology + stage + key markers + context
- [ ] Etiological driver section (for etiologically_driven archetype)
- [ ] Pre-treatment investigations з priority class
- [ ] Regimen details (drug, dose, schedule, particularities) для
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

**Бажано (should have):**
- [ ] Timeline visualization
- [ ] Side-by-side comparison of plans
- [ ] Shared components section
- [ ] Alternative monotherapy option (if applicable)
- [ ] Ukrainian localization (primary output language)

**Acceptable gap для v1.0:**
- [ ] Advanced visualizations (timelines, charts) — можуть бути простіші
- [ ] Perfectly polished prose — може потребувати human editing
- [ ] Comprehensive patient education layer — Phase 2

---

## 2. Patient profile template

Заповнюється реальними деідентифікованими даними після governance-
approved процесу.

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

Базуючись на reference document structure:

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

Baseline перед лікуванням:

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

Для описаного patient profile, engine має виконати наступну логіку:

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

Як ми перевіряємо, що system output еквівалентний reference document.

### 4.1. Structural validation (automated)

Script перевіряє, що engine output містить:

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

Script перевіряє конкретні елементи:

```python
def validate_content(output, reference):
    assert output.disease == reference.disease
    assert set(output.pre_treatment_tests) >= set(reference.critical_tests)
    assert output.regimens_considered == reference.regimens_considered
    assert output.contraindications_identified >= reference.critical_contraindications
    # ...
```

### 4.3. Expert validation (human)

Clinical Co-Lead проходить side-by-side comparison:

**Checklist:**
- [ ] Основна рекомендація збігається (обидва варіанти)
- [ ] Дози коректні
- [ ] Timeline коректний
- [ ] Red flags правильно категоризовані
- [ ] Джерела цитовані вірно
- [ ] Нічого критичного не пропущено
- [ ] Нічого суттєво зайвого не додано
- [ ] Українська термінологія коректна
- [ ] Формулювання neutral (per CCS §3.3)
- [ ] Output clinically usable у tumor board

**Scoring:**
- Pass: система клінічно використовна, може замінити manual preparation
- Needs revision: gaps identified, не блокери, але треба виправити
- Fail: серйозні клінічні помилки, система не готова

### 4.4. Iteration protocol

Якщо validation виявляє gaps:

1. **Classify gap:** knowledge base issue | engine logic issue | rendering issue
2. **Fix через standard governance** (CCS §6 для KB changes)
3. **Re-run engine** для cases
4. **Re-validate** з same reviewer (не новим, щоб забезпечити consistency)
5. **Повторити** до pass або до documented acceptable limitations

Limit of iterations — немає, але якщо після 5 iterations не досягли
pass, це сигнал для архітектурного обговорення.

---

## 5. Testing with variations

Один пацієнтський case — недостатньо для повної валідації. Створюємо
**варіації** на базі reference case для тестування edge cases.

### 5.1. Test variant generation

Від основного case робимо hypothetical variations:

**Variant A: Red flag AGAINST aggressive**
Оригінальні дані + hypothetical LVEF 40%
Expected output: STANDARD plan, aggressive NOT offered due to cardiac risk

**Variant B: Red flag FOR aggressive**
Оригінальні дані + hypothetical B-symptoms present
Expected output: AGGRESSIVE plan should be shown as default option

**Variant C: Cirrhosis present**
Оригінальні дані + hypothetical FIB-4 = 4.2
Expected output: Bendamustine dose reduction to 70 mg/m² flagged

**Variant D: HBV co-infection**
Оригінальні дані + hypothetical HBsAg positive
Expected output: Mandatory entecavir prophylaxis added

**Variant E: Missing critical data**
Оригінальні дані, але Ki-67 = unknown, LVEF = unknown
Expected output: System requests these tests before full recommendation

**Variant F: Age >75**
Оригінальні дані + age = 78
Expected output: Dose reduction considered, functional assessment flagged

**Variant G: Concurrent amiodarone**
Оригінальні дані + hypothetical current medication = amiodarone
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

Кожен variant — окремий structured patient JSON + expected
structured output. Stored in `test_cases/reference_variants/`.

### 5.3. Coverage goals

Для v1.0 system acceptance:
- All 7 variants above pass
- Plus original reference case passes
- Plus 3 completely different synthetic cases (не HCV-MZL) fail
  gracefully з "not yet supported" повідомленням

---

## 6. Known limitations and acceptable gaps

Для чесності з команди і потенційними користувачами.

### 6.1. Що reference case НЕ тестує

- Multi-line therapy decisions (relapsed/refractory)
- Pediatric пацієнти
- Other archetypes (biomarker_driven, stage_driven, etc.)
- Solid tumors
- Radiation therapy planning
- Surgical oncology decisions
- Psychosocial assessment
- Palliative-only scenarios

### 6.2. Архітектурні обмеження на v1.0

- Engine — rule-based, не ML
- No learning from patient outcomes (clinicians review, не data pipeline
  feeds back)
- Knowledge base manual curation bottleneck
- Document rendering — template-based, limited creativity vs human-written
  document
- Ukrainian NLP для free-text input — не MVP

### 6.3. Що вважається acceptable gap

Для v1.0 acceptable:
- Слайд layout може візуально відрізнятися від reference
- Prose формулювання може потребувати human editing перед публічним
  використанням
- Precise numeric statistics можуть варіюватися ±10% якщо множинні
  sources дають різні числа
- Level of detail в supportive care може бути спрощеним

Не acceptable навіть для v1.0:
- Wrong regimen recommendation
- Wrong dose
- Missed hard contraindication
- Missed emergency indication (like amiodarone + sofosbuvir)
- Fabricated citations
- Recommendations без sources

---

## 7. Path to production

Reference case visualizes заповнення gap між current state (nothing)
і production-ready v1.0.

### 7.1. Phase structure

**Phase 0 — Documentation (now):** 4 foundational documents (this one
included) + governance setup.

**Phase 1 — Knowledge Population:** Clinical Co-Leads curate all
entities for HCV-MZL (Disease, Drugs, Regimens, Indications,
Contraindications, Red Flags, Tests, Supportive Care, Monitoring,
Algorithms) per Knowledge Schema. Target: 1-2 months with dedicated
time.

**Phase 2 — Engine Implementation:** Developers build rule execution
engine that reads YAML knowledge base and applies to patient input.
Target: 2-3 months parallel з Phase 1.

**Phase 3 — Document Rendering:** Template-based rendering system
that transforms structured Plan → HTML/PDF. Target: 1-2 months.

**Phase 4 — Reference Case Validation:** Full end-to-end test з
reference case (після consent) + 7 variants. Target: 2 weeks.

**Phase 5 — Iteration:** Fix gaps found in validation. Target: 1-2
months.

**Phase 6 — Second Disease:** Add another etiologically_driven disease
(e.g., Helicobacter-related MALT lymphoma) to validate schema
generalizability. Target: 1 month.

**Total estimate to usable v1.0:** 6-9 months з active team of 5-7
people з ~50% time commitment.

### 7.2. Milestones

- **M1:** Phase 0 complete — all 4 foundational documents approved by
  Clinical Co-Leads
- **M2:** HCV-MZL knowledge base 80% populated
- **M3:** Engine MVP runs on synthetic test case
- **M4:** Engine runs on reference case, generates first document
- **M5:** Reference case passes expert validation
- **M6:** Second disease added and validated
- **M7:** v1.0 release (educational/research positioning, not medical
  device)

---

## 8. What this means for the pitch

Для demonstration перед клініцистами-співзасновниками і потенційними
партнерами:

### 8.1. Що показувати зараз

- CHARTER.md — наша governance логіка
- CLINICAL_CONTENT_STANDARDS.md — наш редакційний підхід
- KNOWLEDGE_SCHEMA_SPECIFICATION.md — технічна структура
- DATA_STANDARDS.md — патієнтський модель, FHIR/mCODE-compliant
- Цей документ — target output на прикладі HCV-MZL
- Сам reference document (HCV-MZL) — як "ось, що ми хочемо генерувати
  автоматично" (за consent)

### 8.2. Чесне commitment

- 6-9 місяців до функціонального v1.0
- Потрібна full-team робота, не вечірній hobby
- Knowledge curation — bottleneck, не coding
- Не обіцяємо "AI, що лікує" — обіцяємо "structured information
  support, яка економить 2-4 години підготовки tumor board"

### 8.3. Чому це не Watson

Коротка перевірка для скептиків:

| Watson problem | Наш підхід |
|---|---|
| Тренували на synthetic cases | Валідуємо на real expert-verified document |
| Рекомендації з "single authority" preferences | Рекомендації з multiple published guidelines |
| "Black box" scoring | Transparent evidence levels з GRADE |
| LLM generates recommendations | LLM only formats; rules generate recommendations |
| No human medical review per rec | Dual medical review mandatory |
| Scaled before validation | Scope свідомо обмежений до validated domains |
| Sold as "decision maker" | Positioned as "information support" |

---

## 9. Governance цього документа

- Template зміни (без пацієнтських даних) — consensus Tech Lead +
  один Clinical Co-Lead
- Incorporation реальних деідентифікованих даних — full dual medical
  review + Project Coordinator approval + documented consent
- Re-identification re-review — через 12 місяців після публікації, і
  при будь-якій суттєвій зміні
- Version bump при кожному change

---

## 10. Поточний статус і обмеження

**v0.1:**
- Structural template готовий
- Реальні patient дані — placeholder, чекають consent
- Test variants (Section 5) — hypothetical, потребують clinical
  validation що вони корректні edge cases
- Validation protocol (Section 4) — не implemented в code

**Що треба:**
- [ ] Отримати формальну письмову згоду reference patient
- [ ] Провести деідентифікацію per Data Standards §14
- [ ] Re-identification review
- [ ] Заповнити Sections 2 з real deidentified data
- [ ] Calibrate test variants з Clinical Co-Leads
- [ ] Implement validation scripts

---

## 11. Summary: чому цей документ важливий

Four documents разом (Charter, Content Standards, Knowledge Schema,
Data Standards) визначили **як** ми будуємо систему. Цей документ
визначає **що саме** ми будуємо — конкретну цільову функціональність,
проти якої все інше валідується.

Без reference case попередні документи залишаються абстрактними. З
reference case команда знає, що саме має бути згенеровано, і може
йти до цієї цілі методично.

Це — наш контракт сам з собою і з майбутніми користувачами.

---

**Questions, pull requests, suggestions — всі вітаються через
governance process (CHARTER §6).**
