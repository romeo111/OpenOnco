# MDT Orchestrator та Decision Provenance Specification

**Проєкт:** OpenOnco
**Документ:** MDT Orchestrator + Decision Provenance
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads
**Попередні документи:** CHARTER.md (особливо §1, §2, §6, §8.3, §15),
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md,
REFERENCE_CASE_SPECIFICATION.md, SOURCE_INGESTION_SPEC.md

---

## Мета документа

Закриває явну прогалину, зафіксовану у `KNOWLEDGE_SCHEMA_SPECIFICATION.md`
§1306 ("Не моделюються: clinical trial matching, genetic syndromes,
**multidisciplinary coordination**").

OpenOnco **не приймає клінічних рішень** (CHARTER §1, §8.3) і не
виставляє себе як "розумніше за лікаря" — навпаки, він готує
**структурований пакет для онкоконсиліуму (MDT — multidisciplinary
team / тумор-борд)**, який допомагає зрозуміти:

1. **Хто має бути за столом** (роль-рекомендація / role recommendation)
2. **Які питання залишаються відкритими** (OpenQuestion)
3. **Які дані відсутні або сумнівні** (data quality summary)
4. **Хто і коли що зробив** (decision provenance / audit trail)

MDT Orchestrator — це окремий шар поверх rule-engine, що **не змінює**
вибір regimen або жодну іншу клінічну рекомендацію. Усі терапевтичні
рекомендації лишаються прерогативою curated knowledge base + rule
engine (CHARTER §8.3).

---

## 1. Принципи

### 1.1. Що Orchestrator робить

- Аналізує `patient` profile + `PlanResult` з rule engine
- За набором детермінованих правил визначає, **яких ролей бракує**
  для повного MDT
- За правилами та аналізом profile fields визначає, **що відсутнє у
  даних** і блокує впевнене ведення (формує `OpenQuestion`)
- Створює initial `ProvenanceEvent` записи: "engine згенерував план",
  "engine ідентифікував required role X", "engine підняв питання Y"
- Пакує результат у `MDTOrchestrationResult` — структурований brief
  для тумор-борду

### 1.2. Що Orchestrator не робить

- **Не змінює** `default_indication_id` чи будь-який інший вихід
  rule engine
- **Не пропонує** нових клінічних рекомендацій (зміна regimen, dose,
  додавання препарату — суворо `Indication` / `Regimen` / curated
  KB)
- **Не використовує LLM** для клінічного reasoning (CHARTER §8.3) —
  всі правила декларативні і зрозумілі рев'юеру
- **Не імітує** експертну оцінку лікаря — лише **запитує** її
- **Не приймає рішень за пацієнта** і не виходить за scope HCP
  (CHARTER §15.2 C1)

### 1.3. Сумісність з FDA non-device CDS positioning (CHARTER §15)

MDT Orchestrator **посилює** FDA Criterion 4 ("HCP can independently
review the basis"):

- Робить explicit "що ми НЕ знаємо" (Open Questions, data quality)
- Робить explicit "хто має дати другу думку" (required roles)
- Робить explicit "що сказала система і коли" (provenance log)

Це знижує automation bias (FDA Guidance §IV(4)) — лікар бачить, що
система **визнає межі своєї компетенції** і просить експертного
ревю там, де треба.

---

## 2. Сутності даних

Усі сутності — **JSON-serializable Python dataclasses**. Persistence
у MVP — in-memory + опціональний JSON-серіалізатор; БД shape (event
log, append-only) описана у §6 нижче, але реалізація відкладена до
наступної ітерації.

### 2.1. `MDTRequiredRole`

Одна роль, яку треба запросити на тумор-борд (або principle of
referral) для повного ведення цього пацієнта.

| Поле | Тип | Опис |
|---|---|---|
| `role_id` | `str` | Канонічний ID ролі: `hematologist`, `pathologist`, `radiologist`, `infectious_disease_hepatology`, `clinical_pharmacist`, `radiation_oncologist`, `surgical_oncologist`, `palliative_care`, `social_worker_case_manager`, … |
| `role_name` | `str` | Українською: "Гематолог / онкогематолог", "Патолог / гематопатолог" тощо |
| `reason` | `str` | Коротке клінічне обґрунтування **українською** для рев'юера |
| `trigger_type` | `enum` | `missing_data` \| `diagnosis_complexity` \| `treatment_domain` \| `safety_risk` \| `molecular_data` \| `local_availability` \| `palliative_need` |
| `priority` | `enum` | `required` \| `recommended` \| `optional` |
| `linked_findings` | `list[str]` | Ідентифікатори findings/biomarkers/RedFlags, що тригернули правило |
| `linked_questions` | `list[str]` | ID OpenQuestion, на які ця роль має дати відповідь |

### 2.2. `OpenQuestion`

Питання, на яке система не може відповісти автоматично і яке має
бути закрите перед фінальним прийняттям плану.

| Поле | Тип | Опис |
|---|---|---|
| `id` | `str` | `OQ-<short-slug>` |
| `question` | `str` | Питання українською мовою |
| `owner_role` | `str` | `role_id` ролі, що зазвичай дає відповідь (`hematologist`, `radiologist`, тощо) |
| `blocking` | `bool` | Чи блокує це питання прийняття плану |
| `rationale` | `str` | Чому це питання важливе |
| `linked_findings` | `list[str]` | Які поля profile відсутні/неоднозначні |

### 2.3. `MDTOrchestrationResult`

Top-level контейнер, що повертає `orchestrate_mdt(...)`.

| Поле | Тип | Опис |
|---|---|---|
| `patient_id` | `Optional[str]` | З `patient.patient_id`; `null` якщо anonymous |
| `plan_id` | `Optional[str]` | З `PlanResult.plan.id`, якщо план згенеровано |
| `disease_id` | `Optional[str]` | З `PlanResult.disease_id` |
| `required_roles` | `list[MDTRequiredRole]` | priority `required` |
| `recommended_roles` | `list[MDTRequiredRole]` | priority `recommended` |
| `optional_roles` | `list[MDTRequiredRole]` | priority `optional` |
| `open_questions` | `list[OpenQuestion]` | Усі питання, у тому числі blocking |
| `data_quality_summary` | `dict` | Лічильники: missing fields, ambiguous, unknown red-flag inputs |
| `warnings` | `list[str]` | Технічні warning'и (entity не знайдено, тощо) |
| `provenance` | `DecisionProvenanceGraph` | Initial events |

### 2.4. `ProvenanceEvent` (event-log shape — append-only)

| Поле | Тип | Опис |
|---|---|---|
| `event_id` | `str` | Globally unique, e.g. `EV-<plan_id>-001` |
| `timestamp` | `str` | ISO-8601 UTC |
| `actor_role` | `str` | `engine` \| `hematologist` \| … (canonical role_id або системний) |
| `actor_id` | `Optional[str]` | Конкретний рев'юер (e.g. `dr-coleadX`); `null` для engine або anonymous |
| `event_type` | `enum` | `confirmed` \| `modified` \| `rejected` \| `added_question` \| `approved` \| `requested_data` \| `flagged_risk` |
| `target_type` | `enum` | `diagnosis` \| `staging` \| `regimen` \| `contraindication` \| `red_flag` \| `source` \| `plan_section` |
| `target_id` | `str` | Канонічний id (e.g. `IND-HCV-MZL-1L-ANTIVIRAL`, `RF-BULKY-DISEASE`) |
| `summary` | `str` | Коротко українською |
| `evidence_refs` | `list[str]` | Source IDs / citation IDs, що підкріплюють |

### 2.5. `DecisionProvenanceGraph`

| Поле | Тип | Опис |
|---|---|---|
| `nodes` | `list[dict]` | Канонічні вузли: `{id, type, label}` (наприклад diagnosis-вузол, regimen-вузол) |
| `edges` | `list[dict]` | Зв'язки між вузлами: `{from, to, kind}` (наприклад `regimen → contraindication` `kind=triggers`) |
| `events` | `list[ProvenanceEvent]` | Послідовний лог |
| `plan_version` | `int` | Версія Plan, до якої прив'язаний цей граф |

---

## 3. Правила role recommendation (для HCV-MZL reference case)

Усі правила — детерміновані; якщо умова виконується, додається
відповідна роль. Правила розширюються per-disease у міру зростання KB.

| # | Тригер | Роль | Priority | trigger_type |
|---|---|---|---|---|
| R1 | `Disease.lineage` містить `lymphoma` АБО `Disease.archetype == "etiologically_driven"` для лімфом | `hematologist` | `required` | `diagnosis_complexity` |
| R2 | HCV-біомаркер позитивний (BIO-HCV-RNA == positive) АБО HBV-серологія позитивна | `infectious_disease_hepatology` | `recommended` | `molecular_data` |
| R3 | Ознаки об'ємного захворювання (`dominant_nodal_mass_cm >= 7`) АБО будь-які imaging fields у profile | `radiologist` | `recommended` | `diagnosis_complexity` |
| R4 | Лімфомний diagnosis (CD20-IHC, biopsy-related fields) АБО ризик трансформації під ревю | `pathologist` | `recommended` | `diagnosis_complexity` |
| R5 | Дефолтний/альтернативний track має `plan_track == "aggressive"` (chemoimmunotherapy) | `clinical_pharmacist` | `recommended` | `treatment_domain` |
| R6 | Disease — extranodal MALT (e.g. gastric, salivary, ocular adnexa) — RT може бути локально-ефективною | `radiation_oncologist` | `optional` | `treatment_domain` |
| R7 | Лікувальний план потребує препаратів з `reimbursed_nszu == false` | `social_worker_case_manager` | `recommended` | `local_availability` |
| R8 | ECOG ≥ 3 АБО декомпенсована коморбідність → паліативна оцінка | `palliative_care` | `recommended` | `palliative_need` |

**Ескалація priority:** якщо у патієнта є RedFlag `clinical_direction == "intensify"` АБО `"hold"` для конкретної ролі-домену — priority цієї ролі підвищується.

**Дедублікація:** одна `role_id` зустрічається у result не більше одного разу. Якщо різні правила дають різні priority — береться **найвищий** (`required` > `recommended` > `optional`).

---

## 4. Правила Open Questions (для HCV-MZL reference case)

Поява `OpenQuestion` означає: rule engine не міг впевнено відповісти,
бо вхідні дані відсутні або суперечливі.

| # | Тригер | Питання | owner_role | blocking |
|---|---|---|---|---|
| Q1 | Disease — HCV-MZL АБО HCV+ І `hbsag` / `anti_hbc_total` відсутні | "Чи проведена серологія HBV (HBsAg, anti-HBc total)? HBV reactivation risk перед anti-CD20 therapy." | `infectious_disease_hepatology` | `true` |
| Q2 | HCV+ І `child_pugh_class` / `decompensated_cirrhosis` / `fib4_index` відсутні | "Який стадій фіброзу/цирозу печінки? Це впливає на вибір DAA та dosing бендамустину." | `infectious_disease_hepatology` | `true` |
| Q3 | Лімфома І відсутня confirmation `cd20_ihc_status` / `biopsy_confirmed` | "Чи підтверджено CD20+ статус гістологією? Без CD20+ rituximab/obinutuzumab не показані." | `pathologist` | `true` |
| Q4 | Лімфома І відсутні staging fields (Lugano stage, PET-CT date) | "Чи виконано повне стадіювання (Lugano + PET/CT)?" | `radiologist` | `false` |
| Q5 | Aggressive track обраний, відсутній `ldh_ratio_to_uln` | "Який актуальний LDH? Це маркер пухлинного навантаження і трансформації." | `hematologist` | `false` |
| Q6 | Будь-який regimen має drug з `reimbursed_nszu == false` | "Чи доступний препарат X для пацієнта (out-of-pocket vs program)? Чи потрібен social work consult?" | `social_worker_case_manager` | `false` |

**Розширюваність:** правила додаються per-disease. У MVP реалізовано
підмножину для HCV-MZL.

---

## 5. Data quality summary

Метаінформація для тумор-борду:

```python
{
    "missing_critical_fields": [...],      # поля, відсутність яких блокує впевнене ведення
    "missing_recommended_fields": [...],   # поля, бажані але не блокуючі
    "ambiguous_findings": [...],           # значення, інтерпретація яких потребує уточнення
    "unevaluated_red_flags": [...],        # RedFlag IDs, які не вдалось evaluate через відсутні findings
    "fields_present_count": int,
    "fields_expected_count": int,
}
```

Це **не нова клінічна рекомендація**; це чесний звіт про повноту даних,
який допомагає рев'юеру зрозуміти, наскільки впевнено система могла
працювати з тим, що мала.

---

## 6. Decision Provenance — append-only event log

### 6.1. Призначення

Кожна зміна в Plan / MDT context — це **подія**. Подія immutable,
події утворюють лог, лог реконструює історію формування плану.
Підтримує:

- Audit trail для regulatory inquiry (CHARTER §10.2, §15.1 Criterion 4)
- Reproducibility: будь-який Plan можна відновити до стану на
  визначений timestamp
- Attribution: видно, **хто** саме (роль + опційно лікар) додав
  питання, схвалив рекомендацію, відхилив pathway
- Базу для майбутньої persistence (БД-ready shape)

### 6.2. Ініціальні події (генеруються автоматично)

При першому виклику `orchestrate_mdt(...)`:

1. `confirmed` / `plan_section` — "engine згенерував Plan версії N"
2. Для кожної required/recommended ролі — `requested_data` / `plan_section`
   з summary "потрібен ревю з боку ролі X"
3. Для кожного OpenQuestion — `added_question` / `plan_section`
4. Якщо RedFlag спрацював → `flagged_risk` / `red_flag` для кожного

### 6.3. Подальші події (наступні ітерації, не у MVP)

Після MVP: додається API додавання events від клініцистів —
- `confirmed` / `diagnosis` від pathologist
- `modified` / `regimen` від hematologist (з прив'язкою до нового
  Plan version)
- `approved` / `plan_section` від tumor board (фінальний підпис)

### 6.4. Persistence (наступний крок, не у MVP)

Подієвий лог за дизайном append-only — природно лягає на:
- SQLite / Postgres event_log table з `event_id PRIMARY KEY`,
  `(target_type, target_id, timestamp)` index
- Або JSONL файл `patient_plans/<patient_id>/events.jsonl`
- Або immutable object storage (S3/MinIO) для compliance use cases

У MVP реалізація — in-memory + JSON-серіалізація на запит. БД-міграція
описана у roadmap.

---

## 7. Інтеграція з існуючим engine

### 7.1. API

Новий публічний модуль `knowledge_base/engine/mdt_orchestrator.py`:

```python
def orchestrate_mdt(
    patient: dict,
    plan_result: PlanResult,
    kb_root: Path | str = "knowledge_base/hosted/content",
) -> MDTOrchestrationResult:
    ...
```

`generate_plan(...)` **не змінюється** — MDT context опційний шар.

### 7.2. CLI

Прапорець `--mdt` у `knowledge_base/engine/cli.py`. Без `--mdt`
поведінка CLI ідентична поточній. З `--mdt` після Plan summary
друкується:

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
  - [BLOCKING] OQ-HBV-SEROLOGY: Чи проведена серологія HBV? (owner: infectious_disease_hepatology)
  ...
Data quality:
  Missing critical fields: 2
  Unevaluated red flags: 0
```

### 7.3. Інваріанти у тестах

`test_mdt_orchestrator.py` явно перевіряє: після `orchestrate_mdt(...)`
значення `plan_result.default_indication_id` **незмінне**. Це механічна
гарантія non-interference.

---

## 8. Розширення в майбутньому (не у MVP)

- Per-disease правила role/question (не лише HCV-MZL)
- Інтеграція з `Indication.required_tests` / `desired_tests` →
  автоматична генерація OpenQuestion для відсутніх тестів
- Persistence event log
- API для додавання `ProvenanceEvent` від клініцистів (REST endpoint
  або CLI команда `record-event`)
- Render layer: візуалізація `DecisionProvenanceGraph` як interactive
  графа у UI плану
- Підтримка annotations на Plan (`Plan.annotations[]`) — координація
  з `PlanAnnotation` модель з `knowledge_base/schemas/plan.py`

---

## 9. Зміни у цьому документі

| Версія | Дата | Зміни |
|---|---|---|
| v0.1 | 2026-04-25 | Початковий MVP-spec; покриває HCV-MZL reference case + загальні правила |
