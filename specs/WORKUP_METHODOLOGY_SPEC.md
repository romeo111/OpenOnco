# Workup Methodology Specification

**Проєкт:** OpenOnco
**Документ:** Workup Research Methodology — як ми будуємо basic workup для будь-якої онкологічної області
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads
**Попередні документи:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DIAGNOSTIC_MDT_SPEC.md, SOURCE_INGESTION_SPEC.md

---

## Мета документа

OpenOnco масштабується від HCV-MZL → онкогематологія загалом → solid
tumours → інші nозології. Кожне розширення вимагає **детального basic
workup** для відповідної підозри: які тести потрібні для diagnosis +
staging + pre-treatment baseline.

Без формалізованої методології workup-катастрофа: різні нозології
покриті різною глибиною, рев'юер не знає чи `WORKUP-X` написаний по
NCCN чи "з голови", критеріїв inclusion/exclusion немає.

Цей документ — **процес** як перетворити нозологію → DiagnosticWorkup +
підмножину Test entities у KB. Аналогічно `SOURCE_INGESTION_SPEC` для
data sources, тільки для clinical workup content.

**Перший застосунок:** comprehensive hematology workup catalog (HCV-MZL,
acute leukemia, multiple myeloma, MPN/MDS, недиференційована
лімфаденопатія, цитопенії, моноклональна гаммопатія).

---

## 1. Принципи

### 1.1. Workup = "що зробити", не "як лікувати"

`DiagnosticWorkup` описує **діагностичні дії** (тести, біопсія,
imaging, IHC, молекулярні), а **не** therapeutic recommendations.
Останнє — `Indication` / `Regimen` після підтвердженої гістології.
Це чіткий boundary: workup methodology НЕ виходить за scope FDA
non-device CDS Criterion 3 (не "specific treatment directive").

### 1.2. Conservative first — extend per evidence

`DiagnosticWorkup.required_tests` має містити **тести-кандидати у 95%
відповідних випадків**, не "all possible tests if anything is unclear".
Edge cases і disease-specific розширення — через додаткові поля
(`required_ihc_panel.if_b_cell` etc.) або окремі workup variants.

Інакше "comprehensive" workup стає inflated checklist що ніхто не
встигає виконати реально.

### 1.3. Universal-to-specific decomposition

```
WORKUP-CYTOPENIA-EVALUATION (broad triage)
    │
    ├─→ findings: lymphadenopathy → WORKUP-SUSPECTED-LYMPHOMA
    ├─→ findings: blasts on smear → WORKUP-SUSPECTED-ACUTE-LEUKEMIA
    ├─→ findings: monoclonal protein → WORKUP-SUSPECTED-MULTIPLE-MYELOMA
    └─→ findings: unexplained → WORKUP-MDS-EVALUATION
```

Декомпозиція через `applicable_to.lineage_hints` +
`applicable_to.presentation_keywords`. Engine matcher дозволяє
**broader workup перейти у specific** коли findings уточнюються
(revisions workflow per DIAGNOSTIC_MDT_SPEC §7.1).

### 1.4. Cite-able provenance per Test attribute

Кожен Test має посилатись на authority через `sources:` поле
(існуючий механізм Source entities). Не вільне "everyone knows that".
Це posilвue Criterion 4 transparency — лікар може tracé why X test is
listed in this workup.

---

## 2. Source hierarchy для workup research

### 2.1. Tier 1 — обов'язково консультуємо для кожного workup

| Авторитет | Призначення | Frontmatter в Source entity |
|---|---|---|
| **NCCN Guidelines** | US standard of care; найдетальніша initial workup секція в "WORKUP" і "DIAGNOSIS" sub-tables | `evidence_tier: 1`, `hosting_mode: referenced` (NCCN copyright) |
| **ESMO Clinical Practice Guidelines** | EU equivalent; часто стисліше, але explicit на initial assessment | `evidence_tier: 1` |
| **WHO Classification of Tumours (5th ed.)** | Канонічна класифікація + diagnostic criteria per disease | `evidence_tier: 1`, `hosting_mode: referenced` |
| **EHA Guidelines (для гематології)** | European Hematology Association — деталі на molecular workup, нюанси per subtype | `evidence_tier: 1` |
| **BSH Guidelines (для гематології, UK)** | British Society for Haematology — практичні підходи, добре organized | `evidence_tier: 1` |
| **ASH (American Society of Hematology) Pocket Guides + Education Program** | Сучасні консенсуси, особливо emerging entities | `evidence_tier: 1-2` |

### 2.2. Tier 2 — додатковий контекст

| Авторитет | Призначення |
|---|---|
| **Cochrane Systematic Reviews** | Якщо існує review про конкретний test/protocol |
| **МОЗ України клінічні протоколи** | Локальна practice + reimbursement context (для НСЗУ) |
| **Major textbooks (Williams Hematology, Wintrobe's, Hoffman)** | Background reading; не primary source |
| **Peer-reviewed РКД у JCO / Blood / Lancet Onc / NEJM** | Specific evidence для confirmation tests чи novel diagnostic markers |

### 2.3. Tier 3 — допускається тільки явно

| Авторитет | Коли допускається |
|---|---|
| **Expert opinion / case series** | Тільки якщо вище нічого нема, **і** позначити в Test.notes "expert opinion only — pending higher-tier evidence" |
| **Single-institution practice** | Тільки як приклад, не основа |

### 2.4. Що **не** є Tier джерелом

- UpToDate (proprietary, paid, не open)
- Wikipedia (не authoritative)
- LLM-generated content без human verification
- Pharma marketing materials

---

## 3. Test entity attribute completeness checklist

Для кожного нового / оновленого Test перевірити:

### 3.1. Обов'язкові поля (no Test merges without these)

- [ ] `id` — формат `TEST-<SHORT-SLUG>`
- [ ] `names.preferred` (English) + `names.ukrainian`
- [ ] `category` ∈ {`lab`, `imaging`, `histology`, `genomic`, `clinical_assessment`}
- [ ] `purpose` — одна речення українською: **навіщо** робимо
- [ ] `priority_class` ∈ {`critical`, `standard`, `desired`, `calculation_based`}
- [ ] `sources` — мінімум 1 Tier 1 reference

### 3.2. Бажано (рекомендовано)

- [ ] `loinc_codes` — якщо існує LOINC; null допустимо для специфічних panels (cytogenetics, FISH)
- [ ] `specimen` — який biological matrix
- [ ] `turnaround_time` — typical lab turnaround (1-3 hours / same day / 1-3 days / 7-14 days etc.)
- [ ] `availability_ukraine` — дослід у Ukraine context (state_funded, typical_cost_uah, regional availability)

### 3.3. Опційно (per test type)

- `synonyms` — alternate names
- `notes` — caveats, when not applicable, common pitfalls

### 3.4. Anti-patterns (rejection criteria у клінічному ревю)

❌ Test без `purpose` (нема **why**)
❌ Test з `priority_class: critical` без cite-able rationale у Tier 1
❌ Test з proprietary marker name тільки (e.g., commercial assay name without generic description)
❌ Test з turnaround_time `null` коли він добре відомий (ленощі, не unknown)

---

## 4. DiagnosticWorkup entity completeness checklist

### 4.1. Обов'язкові поля

- [ ] `id` — формат `WORKUP-<PRESENTATION-OR-SUSPICION>`
- [ ] `applicable_to.lineage_hints` — мінімум 1 controlled-vocabulary hint
- [ ] `applicable_to.tissue_locations` АБО `applicable_to.presentation_keywords` — мінімум одна категорія
- [ ] `required_tests` — мінімум 3 (інакше це не "workup", це "single test")
- [ ] `mandatory_questions_to_resolve` — мінімум 2 (інакше workup тривіальний)
- [ ] `triggers_mdt_roles.required` — мінімум 1
- [ ] `expected_timeline_days` — realistic estimate
- [ ] `sources` — мінімум 2 Tier 1 references
- [ ] `last_reviewed` + (after publishing) `reviewers` ≥ 2

### 4.2. Бажано

- `biopsy_approach` — preferred + alternatives + rationale, для будь-якого suspicion де біопсія part of standard
- `required_ihc_panel` — baseline + conditional (if_b_cell / if_t_cell / if_aggressive / if_solid) — для suspicions де histology завжди part of workup
- `expected_workup_cost_uah_estimate` — для Ukraine financial planning
- `triggers_mdt_roles.recommended` + `optional`

### 4.3. Композиція workups

Складніші presentations можуть **підняти кілька workups одночасно**:
- Patient має cytopenias + lymphadenopathy → match BOTH
  `WORKUP-CYTOPENIA-EVALUATION` AND `WORKUP-SUSPECTED-LYMPHOMA`
- Engine має додавати тести з обох (deduplicated)
- MVP: matcher повертає top-1 match. Future: composition matcher
  (item у roadmap)

---

## 5. Process: extending OpenOnco до нової onкологічної області

Кожне розширення (e.g., "додати solid tumour breast cancer") пройти ці кроки:

### Step 1: Survey authoritative guidelines (Tier 1)

- NCCN Guideline для нозології (Initial Workup секція)
- ESMO Clinical Practice Guideline
- WHO Classification subtype detail
- Specialty society (для breast — NABCO, ABS, EBCC; для GI — DDW etc.)

Артефакт: `references/<domain>/guidelines_survey.md` зі списком consulted documents + URLs + version dates.

### Step 2: Identify базові tests + diagnostic studies

Для кожної нозології з Step 1 виокремити:
- **Initial assessment** (history, exam, basic labs)
- **Confirmatory** (biopsy, imaging для diagnosis)
- **Staging** (extent of disease)
- **Pre-treatment baseline** (organ function, fertility, vaccination)
- **Risk stratification** (prognostic markers)

Усі — окремі Test entities. Reuse існуючих де можливо (CBC, LFT — universal).

### Step 3: Build / extend KB

Per Test:
- Створити YAML за §3 checklist
- Links to Tier 1 sources

Per Workup:
- Створити YAML за §4 checklist
- `triggers_mdt_roles` — який team склад потрібен

### Step 4: Patient profile fields

Якщо нова нозологія потребує специфічних profile fields (e.g., breast
exam, mammographic findings) — додати у DATA_STANDARDS під відповідну
секцію + adjust engine matcher per `presentation_keywords`.

### Step 5: Engine integration

Якщо потрібно — нові D-rules у `mdt_orchestrator._apply_diagnostic_role_rules`
для domain-specific role recommendations (e.g., breast surgical
oncologist для будь-якої breast suspicion).

### Step 6: Clinical review

CHARTER §6.1 standard process: **2 з 3 Clinical Co-Leads** мусять
підписати content. Reviewer A — domain expert (e.g., breast oncologist
для breast workup). Reviewer B — методологічний reviewer.

Після підпису — `Test.reviewer_signoffs: 2` AND `Workup.reviewer_signoffs: 2`.
До цього — все STUB і явно labelled.

### Step 7: Update WORKUP_METHODOLOGY_SPEC.md changelog

Додати рядок у §7 про domain extension з посиланням на guidelines
survey та responsible reviewers.

---

## 6. Anti-patterns та bias detection

### 6.1. Anti-pattern: "kitchen sink" workup

Тенденція додавати кожен mentioned тест → 30+ обов'язкових тестів.
Реально лікар не зможе це призначити, ще й коштує цілий бюджет.

**Mitigation:** використовувати `priority_class`:
- `critical` — без цього план не може просуватись (≤ 5-7 на workup)
- `standard` — 95% випадків (≤ 10-15)
- `desired` — додатково при специфічних findings (умови вказати у Test.notes)
- `calculation_based` — derived з інших (FIB-4, HCT etc.)

### 6.2. Anti-pattern: Western-only practice

NCCN/ESMO припускають доступ до PET, NGS panels, monoclonal antibodies.
В Ukraine context це може бути недоступно.

**Mitigation:** `availability_ukraine.state_funded: false` flag + alternative test
references. МОЗ протоколи — Tier 1 для Ukraine baseline.

### 6.3. Anti-pattern: outdated workup

Diagnostics evolves. Old cytogenetic panels → NGS. Old imaging → PET-MR.

**Mitigation:** `last_reviewed` дата + quarterly audit (CLINICAL_CONTENT_STANDARDS §9.1).
Test з last_reviewed > 2 years → quality gate flag.

### 6.4. Anti-pattern: AI-generated workup без джерел

Спокуса використати LLM щоб згенерувати "comprehensive workup" для
нової нозології швидко.

**Mitigation:** CHARTER §8.3 hard rule — LLM не клінічний
decision-maker. Workup content **завжди** human-authored з cite-able
sources. LLM допустимий для extraction з PDF (per CHARTER §8.1) при
human verification, не для inventing нових recommendations.

---

## 7. Domain extensions log

| Дата | Domain | Workups added | Tests added | Reviewer A | Reviewer B | Spec update |
|---|---|---|---|---|---|---|
| 2026-04-25 | Hematology — initial broad coverage | WORKUP-SUSPECTED-LYMPHOMA (expanded), -ACUTE-LEUKEMIA, -MULTIPLE-MYELOMA, -MPN-MDS, -CYTOPENIA-EVALUATION, -LYMPHADENOPATHY-NONSPECIFIC, -MONOCLONAL-GAMMOPATHY | ~30 hematology Tests | TBD | TBD | This document v0.1 |

(Future entries додавати при extension.)

---

## 8. Зміни у цьому документі

| Версія | Дата | Зміни |
|---|---|---|
| v0.1 | 2026-04-25 | Початковий MVP. Принципи (§1), Source hierarchy (§2), Test/Workup completeness (§3-§4), Domain extension process (§5), Anti-patterns (§6), Domain extensions log (§7). |
