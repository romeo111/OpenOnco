# Charter та Governance

**Проєкт:** OpenOnco
**Версія:** v0.1 (draft)
**Дата:** [дата публікації]
**Статус:** Draft для публічного обговорення

---

## 1. Мета проєкту

Дати онкологу можливість **за хвилини отримати структуроване бачення
випадку** у вигляді двох альтернативних планів лікування (менш і більш
інтенсивний) на основі даних пацієнта, з повним цитуванням джерел і
чесним описом trade-offs.

Проєкт — **інформаційний ресурс для підтримки обговорення в тумор-борді**,
а **не система, що приймає клінічні рішення**. Всі рекомендації
потребують перевірки лікуючим лікарем і мультидисциплінарного
обговорення перед застосуванням.

---

## 2. Що проєкт робить і чого не робить

**Робить:**
- Приймає структуровані дані пацієнта (нозологія, стадія, гістологія,
  біомаркери, коморбідності, попереднє лікування)
- Застосовує затверджену базу знань (NCCN, ESMO, WHO Classification,
  українські протоколи МОЗ)
- Генерує **один документ (Plan)** з кількома альтернативними планами
  (tracks: standard / aggressive / опційно інші) поданими паралельно для
  обговорення на тумор-борді. Версіонується при отриманні нових даних.
- Цитує джерела для кожної рекомендації
- Явно відмічає невідомі параметри і red flags

**Не робить:**
- Не призначає препарати автоматично
- Не інтегрується з EHR для виконання дій
- Не замінює клінічне рішення лікаря
- Не претендує на рекомендації для рідкісних/ексальних випадків
- Не працює з педіатричними пацієнтами (scope — дорослі)
- Не є медичним виробом у регуляторному сенсі (per §15)
- **Не призначений для пацієнтів / опікунів напряму** — тільки HCP
  (онколог/гематолог у клінічному контексті). Direct-to-patient
  розгортання вимагало б re-classification як medical device — поза
  scope CHARTER (per §15).
- **Не призначений для time-critical/urgent рішень** — outpatient
  планування. Гострі стани (TLS active management, neutropenic fever,
  spinal cord compression) — поза scope (per §15).

---

## 3. Scope (на MVP-стадії)

**Включено:**
- Первинне лікування (first-line) для підтверджених нозологій
- Доросла онкогематологія (стартова область)

**Не включено на MVP:**
- Relapsed/refractory сценарії
- Педіатрія
- Solid tumors (планується після стабілізації онкогематології)
- Автоматичне виконання дій в EHR

**Перші нозології для покриття:**
- [Нозологія 1] — reference case з документом для верифікації
- [Нозологія 2] — TBD після Phase 1

---

## 4. Команда і ролі

### 4.1. Постійні ролі

**Project Initiator / Coordinator:** [імʼя]
Координує роботу команди, веде комунікацію, відповідає за публічну
репрезентацію. Не має права approve-ити клінічний контент.

**Clinical Co-Leads:** [імʼя 1], [імʼя 2], [імʼя 3]
Троє практикуючих онкологів (мінімум один — онкогематолог відповідного
домену). Кожний approve-ить клінічний контент у своєму домені. Одночасна
згода двох з трьох необхідна для merge клінічних змін.

**Technical Implementation:**
- Coding Agent A: [назва/версія, наприклад, Claude Code]
- Coding Agent B: [назва/версія]
- LLM models for auxiliary tasks: [перелік моделей]

Детальні правила роботи з AI-інструментами — розділ 8.

### 4.2. Що означає «три лікарі»

На MVP-стадії клінічний governance тримається на трьох людях. Це
свідоме обмеження, з якого випливає:

- Мінімум двоє з трьох мають approve-ити кожну клінічну зміну
- Розбіжність → тижнева пауза на reconciliation, за потреби — залучення
  зовнішнього клініциста для consultation
- У разі недоступності одного — клінічний merge призупиняється, поки
  не буде відновлено мінімум двох активних рев'юерів
- Escalation для складних розбіжностей: консультація з профільним
  професійним товариством (ESMO, EHA, ASCO) або expert у установі-партнері

### 4.3. Що ми шукаємо далі

Проєкт явно шукає розширення Clinical Co-Leads до 5-7 людей через:
- Академічне партнерство з медичною установою
- Залучення onkologist-residents і fellows як associate contributors
- International advisory (українські клініцисти в ЄС/США)

---

## 5. Джерела знань

### 5.1. Дозволені первинні джерела

**Міжнародні настанови:**
- NCCN Guidelines (через офіційний доступ)
- ESMO Clinical Practice Guidelines (відкритий доступ)
- WHO Classification of Tumours 5th ed. (для класифікації)
- BSH, EHA guidelines (для гематології)
- EASL (для HCV-related lymphomas)

**Українські:**
- Уніфіковані клінічні протоколи МОЗ України
- Перелік реімбурсованих препаратів НСЗУ
- Державний формуляр

**Доказова база:**
- Peer-reviewed RCT (PubMed-indexed)
- Cochrane systematic reviews
- FDA labels, EMA EPARs

**Молекулярні показання:**
- OncoKB (academic tier)
- CIViC

### 5.2. Відкриті бази для валідації і тестування

- cBioPortal (MSK-IMPACT, MSK-CHORD, GENIE)
- TCGA / GDC Portal
- AACR Project GENIE
- MMRF CoMMpass (мієлома)
- ICGC/ARGO
- ClinicalTrials.gov (через API)
- GDC (для геномних даних)
- COSMIC (academic tier)
- SEER (для епідеміологічного контексту)
- MIMIC-IV (для NLP-компонентів, де релевантно)
- DepMap (для drug response validation)

### 5.3. Стандарти даних

- **FHIR R4/R5** для обміну даними пацієнта
- **mCODE** (minimal Common Oncology Data Elements) — профіль для онкології
- **ICD-10** і **ICD-O-3.2** для діагнозів і гістології
- **SNOMED CT** для клінічної термінології
- **LOINC** для лабораторних показників
- **RxNorm** для препаратів
- **HL7 CQL** для декларативних клінічних правил

### 5.4. Що не використовується

- Secondary sources без traceability до первинних
- Промоційні матеріали фармкомпаній
- Single-center retrospective studies без peer review
- Джерела, що вимагають payment для цитування без legitimate доступу

---

## 6. Процес внесення клінічних змін

### 6.1. Стандартний workflow

> **⚠ Тимчасовий dev-режим (з 2026-04-26):** проект у фазі v0.1
> (specs-first / KB-bootstrap). Clinical Co-Leads ще не призначені,
> тому two-reviewer signoff на рівні PR **тимчасово вважається "OK"**
> для merge при умовах: (а) контент має ≥1 цитоване primary-джерело,
> (б) всі Indication / Regimen / RedFlag залишаються позначені як
> `STUB` (`reviewer_signoffs: 0`), (в) жоден Plan, побудований з цього
> KB, не публікується пацієнтам поза synthetic / demo-режимом.
> Цей відступ діє до призначення Clinical Co-Leads або до першого
> production-deploy для реальних HCP-користувачів — що настане раніше.
> Tracker: roadmap → "Operations → Reviewer signoff workflow".

1. **Proposal:** Contributor створює PR з клінічною зміною.
   Обов'язкові поля: опис, обґрунтування, джерела (мінімум 1 primary),
   evidence level, вплив на існуючі рекомендації.

2. **Triage:** Один з Clinical Co-Leads (rotating) протягом 7 днів
   призначає двох рев'юерів.

3. **Medical review:** Two independent clinicians протягом 14 днів.
   Standardized checklist: коректність цитувань, узгодженість з
   актуальними настановами, контрадикції, evidence level, повнота.

4. **Reconciliation:** Якщо рев'юери згодні — merge. Якщо розходяться —
   обговорення, за потреби — третій клініцист або публічне розкриття
   обох позицій з поміткою "контроверсія" (аналогічно NCCN category 2B).

5. **Technical review:** Перевірка format, schema validity, test coverage.

6. **Automated tests:** На test patient cohort (synthetic + deidentified
   real cases).

7. **Merge + changelog:** Публічний запис з авторами, рев'юерами,
   джерелами, версією.

8. **Post-merge flag:** Перші 30 днів — status "recent", priority на
   bug reports.

### 6.2. Emergency pathway

Для safety-critical змін (drug recall, new contraindication, FDA alert):
- Один з Clinical Co-Leads + один додатковий клініцист (може бути
  зовнішній expert) можуть approve emergency change
- Повний review — протягом 7 днів post-merge
- Явний label "emergency update" у changelog

### 6.3. Deprecation

Застарілі рекомендації не видаляються миттєво:
- Deprecation period — 6 місяців з явним warning
- Архівний доступ зберігається назавжди
- Changelog пояснює причини зміни

---

## 7. Прозорість

### 7.1. Завжди публічне

- Всі прийняті клінічні зміни з усією метаданими
- Changelog з повною історією
- CoI declarations усіх Clinical Co-Leads
- Governance documents
- Meeting minutes (якщо є формальні meetings)
- Contribution guidelines
- Known clinical issues

### 7.2. Приватне

- Реальні дані пацієнтів для testing (тільки deidentified, в окремому
  access-controlled репо)
- Preliminary drafts до перших reviews

### 7.3. Conflict of Interest

> **⚠ Тимчасовий dev-режим (з 2026-04-26):** Clinical Co-Leads ще не
> призначені, тому CoI-декларації **тимчасово вважаються "OK"** як
> "відсутні / N/A". Як тільки перший Co-Lead узгоджений — декларація
> публікується перед першим voting участю. Цей відступ синхронізований
> з §6.1 dev-режимом.

Всі Clinical Co-Leads щорічно декларують:
- Консалтинг для фармацевтичних компаній
- Speaking fees
- Research grants
- Equity / ownership в medical ventures
- Family ties з industry

Декларації — публічні на сайті. При обговоренні рекомендацій, що
стосуються препаратів з декларованими CoI, відповідний Co-Lead
recuses від voting на цю зміну.

---

## 8. Правила роботи з AI-інструментами

Це новий розділ для OSS governance, зумовлений специфікою проєкту.

### 8.1. Класифікація використання AI

**Дозволено без особливих обмежень:**
- Генерація boilerplate коду
- Допомога з документацією
- Refactoring існуючого коду
- Unit tests generation
- UI/UX components

**Дозволено з підвищеною увагою:**
- Генерація prose-розділів для пацієнтських/лікарських документів на
  основі структурованих даних
- Витяг структурованих даних з clinical documents (patological reports,
  medical records) — з обов'язковою людською верифікацією
- Translation між мовами (EN/UK) — з клінічним рев'ю

**Заборонено:**
- Вибір клінічних рекомендацій (це rule-based з knowledge base)
- Визначення доз препаратів
- Інтерпретація біомаркерів для вибору лікування
- "Заповнення прогалин" у даних пацієнта
- Генерація медичного контенту для knowledge base без цитувань

### 8.2. Audit trail для AI-контрибуцій

- Код, згенерований AI-coding агентом, маркується в commit message
  (наприклад, `[agent:claude-code]`)
- Людина-контрибутор, що merge-ить AI-генерований код, несе ту саму
  відповідальність, що за власноручний код
- LLM-генеровані prose-розділи у документах — маркуються окремим tag
  `<!-- ai-generated, reviewed by: [name] -->`
- Weekly log AI tool usage: які моделі використовувались, для яких задач

### 8.3. Заборонені промпт-патерни

- "Напиши рекомендацію для..."
- "Яка найкраща терапія при..."
- "Згенеруй дозування препарату X..."
- Будь-що, що робить LLM фактичним клінічним decision-maker

Все клінічне reasoning — через декларативні правила у knowledge base,
виконувані rule engine. LLM працює тільки з виходом, не замість нього.

### 8.4. Валідація AI-generated виходу

- Prose-розділи, зроблені LLM: обов'язкова клінічна верифікація перед
  первою публікацією, періодичні audits
- Extraction-результати: random sample audit на точність
- Coding-агенти: standard code review + test coverage

---

## 9. Safety і обробка помилок

### 9.1. Reporting clinical errors

- Public issue tracker з тегом `clinical-error`
- Alternative private channel для sensitive reports: [email]
- SLA: triage — 48 годин, assessment — 7 днів, fix для критичних — ASAP

### 9.2. Hall of Responsibility

- Public credit для reporters (якщо згодні)
- Публічний розбір критичних помилок (post-mortem) з lessons learned
- Список known issues — завжди доступний

### 9.3. Нульовий пацієнт (reference case)

Проєкт публікує один reference clinical case як демонстрацію того, як
система повинна працювати. Вимоги:

- **Пацієнт надав informed consent** на використання його випадку як
  публічної reference
- **Видалена вся ідентифікуюча інформація** (імена, ініціали, точні
  дати, заклад, регіон, будь-яке поєднання даних, що дозволяє
  re-identification)
- **Ethics committee approval** від установи, де проводилось лікування
- Case доступний у публічному репо як "Reference Case #0"
- Якщо consent відкликається — case видаляється з публічного доступу

До виконання всіх цих умов — case залишається внутрішнім, не публічним.

---

## 10. Версіонування

### 10.1. Knowledge base

Semantic versioning по нозологіям:
- **MAJOR** (x.0.0): breaking change у рекомендаціях (зміна preferred regimen)
- **MINOR** (0.x.0): нова опція без видалення старої
- **PATCH** (0.0.x): correction, clarification, нове джерело

### 10.2. Retention

- ВСІ версії knowledge base зберігаються безстроково
- Кожен згенерований документ містить snapshot використаних версій
- Retrospective reconstruction стану knowledge на будь-яку дату — можливий

---

## 11. Disclaimer policy

Стандартний disclaimer на всіх виходах системи:

> Цей документ згенеровано інформаційною системою [Назва] як підтримку
> обговорення клінічного випадку. Він **не є медичною рекомендацією** і
> **не замінює рішення лікуючого лікаря**. Всі рекомендації потребують
> перевірки лікарем з доступом до повної клінічної картини пацієнта і
> обговорення мультидисциплінарною командою.
>
> Версія knowledge base: [X.Y.Z], дата генерації: [дата], джерела: [перелік].
> У разі сумнівів звертайтеся до професіоналів охорони здоров'я.

Текст — standardized, не обговорюється per-випадок.

---

## 12. Governance змін самого Governance

- Зміни у цьому документі — через consensus усіх трьох Clinical Co-Leads
  + Project Coordinator
- 7 днів public comment period перед фінальним рішенням
- Зміна фіксується у CHANGELOG цього документу

---

## 13. Поточний статус і обмеження

**Що ми знаємо на цей момент:**
- Governance виключно для MVP-стадії (1-2 нозології, команда до 10 людей)
- Масштабування потребуватиме формалізації у foundation-style структуру
- Регуляторний статус поки — інформаційний ресурс, не медичний виріб
- Проєкт не пройшов формальне clinical validation study

**Що планується в міру зростання:**
- Розширення Clinical Editorial Board до 7+ людей
- Domain Working Groups для кожної клінічної області
- Формальна юридична структура (non-profit foundation)
- Clinical validation studies з peer-reviewed публікаціями
- Регуляторна стратегія (educational resource → дослідження →
  медичний виріб, якщо релевантно)

**Відомі обмеження:**
- Залежність від трьох клініцистів на старті — single points of failure
- Обмежений обсяг нозологій
- Відсутність real-world deployment validation
- Українська-специфічна регуляторна ситуація не повністю опрацьована

---

## 14. Контакти

- Project Coordinator: [контакт]
- Clinical questions: [контакт]
- Security / privacy concerns: [контакт]
- General discussion: [посилання на форум/chat]

---

## 15. FDA Non-Device CDS Positioning

OpenOnco свідомо спроектований так, щоб **відповідати чотирьом
критеріям §520(o)(1)(E) FD&C Act** (carve-out 21st Century Cures Act
2016, інтерпретація FDA — `specs/Guidance-Clinical-Decision-Software_5.pdf`,
Source `SRC-FDA-CDS-2026`). Software, що відповідає всім чотирьом, **не
є medical device** і не підлягає FDA premarket review.

Цей розділ — engineering best-effort positioning, не юридична
консультація. Перед US-deployment потрібен формальний regulatory ревю.

### 15.1. Чотири критерії і як OpenOnco до них підходить

**Criterion 1 — NOT image / IVD signal / signal-pattern processor.**
- OpenOnco приймає **витяги** (radiology report text, lab results як
  числа з LOINC кодами, biomarker statuses), не raw signals чи images
- Genomic data — як structured variants з validated NGS-pipelines (через
  CIViC / OncoKB references), не raw FASTQ
- **Червона лінія:** ніколи не ingest'ити PET/CT pixels, ECG waveforms,
  raw NGS reads напряму

**Criterion 2 — display/analyze/print medical information.**
- Patient profile (mCODE / FHIR per `DATA_STANDARDS`)
- Цитуємо guidelines (NCCN, ESMO, EASL, МОЗ протоколи), drug labels
  (FDA, EMA), peer-reviewed RCT, government recommendations — все це
  явно "medical information" per FDA Guidance §IV(2)

**Criterion 3 — recommendations to HCP about prevention/diagnosis/treatment.**
- Output: `Plan` з кількома `tracks` (≥2: standard + aggressive) — це
  **list / prioritized list of treatment options**, exactly the
  non-device pattern in FDA Examples V.A.9, V.A.10, V.B.2
- HCP-only за дизайном (§2). **Direct-to-patient deployment = device.**
  Permanent constraint.
- Жодного "specific directive" — `Plan.tracks[].is_default` маркує
  engine's selection, але `automation_bias_warning` явно нагадує що
  обидва треки представлені для HCP review

**Criterion 4 — HCP can independently review the basis.**
- `Plan.fda_compliance` блок (FDA Criterion 4 metadata) обов'язково
  surfaced у кожному рендері: `intended_use`, `hcp_user_specification`,
  `patient_population_match`, `algorithm_summary`, `data_sources_summary`,
  `data_limitations`, `automation_bias_warning`, `time_critical`
- Rule engine — transparent YAML, не opaque ML; `Plan.trace` записує
  кожен decision-tree step
- Кожна Indication має `rationale` + `sources[]` Citations з PMID/DOI/URL
- Версіонування ([§10.2](#10-версіонування)) дає reproducibility

### 15.2. Critical constraints (порушення = втрата non-device status)

| # | Constraint | Що стає device |
|---|---|---|
| C1 | HCP-only, never patient-facing | Direct-to-patient → device |
| C2 | Outpatient/non-time-critical only (`Indication.time_critical: false`) | Acute/emergency modules → device |
| C3 | No raw image / signal / NGS read input | Adding such → device |
| C4 | Always ≥2 tracks, never single binding directive | "System prescribes X" UX → device |
| C5 | Sources must be **established / well-understood** (NCCN/ESMO/RCT/regulatory labels) | Novel biomarker discovery without published evidence → device |
| C6 | Render UI must avoid automation-bias patterns | Pre-selected "accept", buried alternatives, missing rationale → device |
| C7 | No treatment recommendations without confirmed histology — diagnostic-phase MDT may suggest workup steps and team composition, but treatment Plan generation is mechanically blocked when `patient.disease.id` / `icd_o_3_morphology` absent (per `specs/DIAGNOSTIC_MDT_SPEC.md` §1.2) | Bypassing histology gate to produce treatment tracks → device + clinical-safety risk |

### 15.3. Зміна, яка triggers re-classification

Будь-яка з наступних змін має пройти governance review (§6) **перед**
implementation:

- Додавання time-critical Indication (toggle `time_critical: true`)
- Додавання image / signal / raw NGS input pathway
- Pivot до patient-facing version
- Видалення алтернативного track ("система обирає одне")
- Hide chi remove rationale / sources / trace з рендеру
- Додавання novel biomarker prediction без published primary evidence
- Перехід на commercial deployment model (триггерить також license
  audit per `SOURCE_INGESTION_SPEC §4.3`)

### 15.4. Інші юрисдикції

Цей розділ написаний з орієнтацією на **US FDA** як global gold standard.
- **Україна:** МОЗ regulation менш формалізована для CDS; принцип
  "decision-support ≠ decision-making" застосовний.
- **EU:** MDR (Medical Device Regulation) має схожий carve-out для CDS,
  але інтерпретація стрімкіша — separate review needed якщо EU launch.
- **UK:** MHRA загалом узгоджений з FDA по CDS позиції.

OpenOnco's design satisfies the **strictest** common denominator (FDA
Criterion 4 transparency requirements); інші юрисдикції повинні бути
strictly easier to clear.

---

**Цей Charter — living document. Критика, пропозиції, pull requests на
сам документ — вітаються.**
