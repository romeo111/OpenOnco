# Clinical Content Standards

**Проєкт:** OpenOnco
**Документ:** Clinical Content Standards
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads
**Попередній документ:** CHARTER.md

---

## Мета документа

Цей документ визначає, **як клінічний контент пишеться, цитується,
оцінюється і ревʼюється** у knowledge base проєкту.

Без цього документа:
- Три клініцисти-співзасновники не мають спільної мови для рев'ю
- Не існує об'єктивних критеріїв «good content» vs «bad content»
- Неможливо зробити відтворювану оцінку evidence
- Нові контрибутори не знають, як пропонувати зміни

Цей документ — **редакційний стандарт** проєкту. Аналоги: NCCN Guidelines
Methodology, Cochrane Handbook, ESMO Living Guidelines Methodology.

---

## 1. Принципи

### 1.1. Evidence-based by default

Кожна клінічна твердження в knowledge base має бути прослідковане до
первинного джерела. Немає «загальновідомого» контенту без цитати.

### 1.2. Transparency over elegance

Якщо джерела суперечать одне одному — **показуємо суперечність**, не
вибираємо «переможця» за власним смаком. Клініцист, що використовує
систему, має право знати про розбіжність.

### 1.3. Дата важливіша за авторитет

Стаття 2020 року з NEJM може бути застаріла у 2026. Recent evidence з
меншого джерела може бути валідніша за стару з топового. Ієрархія
джерел не заміщує temporal currency.

### 1.4. Explicit over implicit

Те, що не сказано явно, не існує. «Препарат X звичайно використовують
у дозі Y» без цитати — не враховується.

### 1.5. Uncertainty is content, not a gap

«Evidence недостатнє для рекомендації» — це повноцінний висновок, не
провал. Система має вміти сказати «не знаємо», а не припускати.

### 1.6. Local context matters

Міжнародні настанови (NCCN, ESMO) — основа, але не єдина правда.
Українська доступність препаратів, протоколи МОЗ, формуляр НСЗУ —
обов'язковий шар для клінічно корисних рекомендацій.

---

## 2. Ієрархія джерел

Ієрархія визначає, який вага призначається різним типам джерел при
розбіжностях.

### 2.1. Tier 1 — Consensus guidelines

Найвищий пріоритет. Використовуються як основа рекомендацій.

**Міжнародні:**
- NCCN Guidelines (актуальна версія; зазначати версію: v.X.YYYY)
- ESMO Clinical Practice Guidelines
- ASCO Clinical Practice Guidelines
- EHA Guidelines (онкогематологія)
- BSH Guidelines (Велика Британія, онкогематологія)
- EASL Guidelines (при HCV-related pathologies)
- CAP Guidelines (Pathology)

**Класифікаційні:**
- WHO Classification of Tumours 5th ed. (IARC Blue Books)
- AJCC Cancer Staging Manual 8th ed. (готується 9-те)
- ICD-O-3.2
- Lugano Classification (для лімфом)

**Регуляторні:**
- FDA drug labels (openFDA.gov)
- EMA EPARs
- Накази МОЗ України — уніфіковані клінічні протоколи з онкології
- Державний формуляр України
- Перелік реімбурсованих препаратів НСЗУ

### 2.2. Tier 2 — High-quality primary evidence

Використовуються коли guidelines застаріли або не покривають ситуацію.

- Peer-reviewed RCT (Phase 3) у журналах з IF ≥10:
  NEJM, Lancet, JAMA, Nature Medicine, Cell, JCO, Annals of Oncology,
  Blood, Lancet Oncology, Journal of Hematology & Oncology
- Cochrane Systematic Reviews
- Large meta-analyses (peer-reviewed, з методологією PRISMA)
- Registration trials для FDA/EMA approvals

### 2.3. Tier 3 — Primary evidence, нижча сила

- Phase 2 RCT
- Phase 3 з обмеженнями (малий N, non-US/EU cohort, surrogate endpoints)
- Network meta-analyses
- Real-world evidence studies (Flatiron, SEER-based, реєстрові дані)
- Post-marketing surveillance studies

### 2.4. Tier 4 — Supporting evidence

Можна цитувати, але не як основу для сильних рекомендацій.

- Phase 1-2 single-arm studies
- Retrospective cohort studies
- Conference abstracts (ASCO, ESMO, ASH) — маркуємо як preliminary
- Expert opinion papers у peer-reviewed журналах

### 2.5. Tier 5 — Molecular knowledge bases

Окрема категорія для mutation-treatment associations.

- OncoKB — з рівнями доказовості 1, 2, 3A, 3B, 4, R1, R2
- CIViC (community-curated)
- JAX Clinical Knowledgebase
- My Cancer Genome

Ці бази є **агрегаторами первинних доказів**. При використанні їх
рекомендацій, зберігаємо посилання на базу + посилання на первинне
дослідження, на яке вона посилається.

### 2.6. НЕ приймаються як джерела

- Non-peer-reviewed preprints (medRxiv, bioRxiv) — окрім як indicative
  signal, що треба слідкувати; не як основа рекомендації
- Промоційні матеріали фармкомпаній
- Медичні блоги, podcasts, news articles
- Статті з predatory journals (перевірка через Beall's List, DOAJ)
- ChatGPT/LLM-generated content без human verification
- Wikipedia

---

## 3. Структура клінічної рекомендації

Кожна рекомендація в knowledge base має **обов'язкову структуру**.

### 3.1. Обов'язкові поля

```yaml
recommendation_id: REC-HCV-MZL-001
disease_entity: HCV-associated marginal zone lymphoma
clinical_scenario: >
  First-line therapy for HCV-positive MZL without red flags for
  transformation
recommendation: >
  DAA (sofosbuvir/velpatasvir) + BR (bendamustine/rituximab) as
  concurrent therapy, followed by R-maintenance for 2 years
evidence_level: Strong (see section 4)
strength_of_recommendation: Preferred (see section 4)
sources:
  - type: guideline
    id: NCCN-B-cell-Lymphomas-v2.2026
    page_or_section: MZL-3
    date_accessed: YYYY-MM-DD
  - type: guideline
    id: ESMO-MZL-2020
    url: https://www.annalsofoncology.org/...
  - type: primary_rct
    id: BArT-trial
    citation: Arcaini L et al., Blood 2014;124:2753-2760
    pmid: XXXXXXXX
  - type: primary_rct
    id: BRIGHT-study
    citation: Flinn IW et al., J Clin Oncol 2019
    pmid: XXXXXXXX
applicable_population:
  - HCV RNA-positive
  - MZL confirmed histologically
  - No red flags for high-grade transformation
contraindications_link: [CONTRA-AMIODARONE-SOFOSBUVIR, CONTRA-HBV-NO-PROPHYLAXIS]
last_reviewed: YYYY-MM-DD
last_reviewer_ids: [reviewer-id-1, reviewer-id-2]
notes: >
  Historical alternative (R-CHOP) is addressed in REC-HCV-MZL-002
  for patients with red flags for transformation
```

### 3.2. Заборонені формулювання

**Не вживаємо без контексту:**
- «найкращий», «оптимальний», «ідеальний» — subjective, не evidence
- «більшість пацієнтів» — без конкретного % і джерела
- «доведено ефективним» — треба сказати як саме (OS, PFS, ORR)
- «загалом добре переноситься» — треба конкретні toxicity rates
- «сучасний стандарт» — без посилання на конкретну настанову + дату

**Замінюємо на:**
- «preferred per NCCN v.X.YYYY, category 1»
- «30% of patients achieve CR per BArT trial (Arcaini 2014)»
- «median OS extension of 3.2 months (HR 0.78, 95% CI 0.65-0.94) per trial X»
- «grade 3-4 neutropenia in 18% per registration trial»

### 3.3. Language neutrality

Рекомендації пишуться **фактично**, без промоційного тону. Порівняйте:

**Погано:** «Пембролізумаб — революційний breakthrough у лікуванні НМРЛ»
**Добре:** «Пембролізумаб + хіміотерапія покращив OS у порівнянні з
хіміотерапією (HR 0.56, 95% CI 0.45-0.70) за KEYNOTE-189 (Gandhi 2018)»

---

## 4. Оцінка сили доказів

Ми **не створюємо власну шкалу**, а використовуємо встановлені.

### 4.1. Evidence Level (сила доказу)

Використовуємо адаптовану **GRADE** (Grading of Recommendations
Assessment, Development and Evaluation) — міжнародний стандарт,
використовується Cochrane, WHO, NICE.

| Рівень | Значення | Типові джерела |
|---|---|---|
| **High** | Подальші дослідження малоймовірно змінять оцінку ефекту | Multiple RCTs з consistent results + meta-analysis |
| **Moderate** | Подальші дослідження можуть суттєво вплинути | Single RCT або RCTs з обмеженнями |
| **Low** | Подальші дослідження ймовірно змінять оцінку | Observational studies, small RCTs |
| **Very low** | Оцінка дуже невизначена | Case series, expert opinion |

### 4.2. Strength of Recommendation (сила рекомендації)

Окремо від evidence level. Рекомендація може мати Moderate evidence,
але Strong strength (якщо великий клінічний ефект і немає альтернатив).

| Рівень | Значення |
|---|---|
| **Preferred / Strong** | Benefit clearly outweighs harm; usually recommend |
| **Alternative / Conditional** | Balance of benefit and harm is closer; individualize |
| **Not recommended** | Evidence against use, OR harm ≥ benefit |
| **Insufficient evidence** | Cannot determine benefit-harm balance |

### 4.3. NCCN Categories як cross-reference

Для сумісності з клінічною практикою в США, також вказуємо NCCN
category, якщо рекомендація взята з NCCN:

- **Category 1:** High-level evidence + uniform NCCN consensus
- **Category 2A:** Lower-level evidence + uniform NCCN consensus
- **Category 2B:** Lower-level evidence + non-uniform NCCN consensus
- **Category 3:** Major NCCN disagreement

### 4.4. Molecular/Biomarker evidence — OncoKB levels

Для рекомендацій, основаних на молекулярних маркерах:

- **Level 1:** FDA-approved biomarker для конкретної пухлини
- **Level 2:** Standard of care biomarker в guidelines для конкретної пухлини
- **Level 3A:** Clinical evidence in same indication (early phase)
- **Level 3B:** Clinical evidence in different indication
- **Level 4:** Preclinical evidence
- **Level R1:** Standard care resistance
- **Level R2:** Investigational resistance

### 4.5. Що НЕ робимо

- Не створюємо кастомні 1-10 rating scales
- Не агрегуємо evidence у composite score
- Не робимо ranking рекомендацій через single number
- Не автоматизуємо evidence evaluation через LLM

Ranking за single composite score — це шлях, яким пішов IBM Watson, і
який приховує реальну структуру доказів. Ми презентуємо рекомендації
з повним breakdown, лікар обирає сам.

---

## 5. Цитування джерел

### 5.1. Мінімальна інформація для цитати

Кожне джерело в knowledge base зберігається з:

```yaml
source_id: "NCCN-B-Cell-Lymphomas-v2.2026"  # unique identifier
type: guideline | phase3_rct | meta_analysis | regulatory | molecular_kb | other
title: "NCCN Guidelines for B-Cell Lymphomas"
version_or_edition: "v.2.2026"  # для guidelines
authors: ["Zelenetz AD", "..."]  # для RCT/меш-аналізів
journal: "Blood"  # для статей
year: 2026
pmid: "XXXXXXXX"  # якщо є
doi: "10.XXXX/..."  # якщо є
url: "https://..."
date_accessed: "2026-04-15"  # коли актуально переглянуто для внесення
access_notes: "Subscription required via institutional access"  # якщо закрите
```

### 5.2. Traceability requirement

Кожне клінічне твердження в knowledge base має бути «одним кліком»
від цитати. На практиці це означає:

- UI відображення рекомендації завжди показує список джерел
- Клік на джерело → opens source record з повною метаінформацією
- Клік на PMID → opens PubMed entry (external)
- Клік на DOI → opens publisher page (external)

### 5.3. Коли guideline і RCT розходяться

Наприклад, NCCN рекомендує X, але recent RCT (після останнього
guideline update) показує, що Y краще.

**Підхід:**
1. Фіксуємо обидва
2. Відображаємо обидва з датами: "NCCN v.1.2025 рекомендує X (дата:
   Jan 2025); RCT [name] published Mar 2025 показав Y superior"
3. Не приховуємо суперечність, не вибираємо за read
4. Clinical Co-Lead комітет обговорює, як формулювати рекомендацію з
   урахуванням двох перспектив

### 5.4. Управління застарілими джерелами

Guidelines оновлюються (NCCN — кілька разів на рік). Системі потрібна
дисципліна:

- Source record має field `currency_status`: current | superseded | historical
- Superseded source залишається в БД з вказівкою на replacement
- Рекомендація, що посилається на superseded source, автоматично
  позначається flag `needs_review` під час quarterly audit

---

## 6. Процес internal review

### 6.1. Перед поданням на review

Contributor перевіряє:

- [ ] Всі поля рекомендації заповнені
- [ ] Мінімум 2 незалежні джерела Tier 1 або 2
- [ ] Контрадикції перелічені і зв'язані
- [ ] Evidence level оцінено з GRADE обґрунтуванням
- [ ] Strength of recommendation обрано з обґрунтуванням
- [ ] Formatting і language neutrality перевірено
- [ ] Немає заборонених формулювань з розділу 3.2
- [ ] Поле `applicable_population` чітко задане
- [ ] Дата last_reviewed — поточна

### 6.2. Clinical review checklist

Кожен з двох незалежних reviewers проходить:

**Коректність джерел:**
- [ ] Цитати існують і доступні
- [ ] Опис даних з джерела відповідає реальному змісту джерела
- [ ] Найсвіжіші релевантні настанови процитовані
- [ ] Конфлікти з іншими джерелами задокументовані

**Клінічна коректність:**
- [ ] Рекомендація відповідає current standard of care
- [ ] Рівень доказовості оцінений коректно за GRADE
- [ ] Applicable_population — точна, без over/under-inclusion
- [ ] Нічого важливого не пропущено (альтернативи, контрадикції)

**Консистентність:**
- [ ] Не суперечить існуючим рекомендаціям у БД (або явно розходиться
      з documented rationale)
- [ ] Термінологія консистентна з існуючою
- [ ] Формулювання не promotional

**Безпека:**
- [ ] Всі hard contraindications перелічені
- [ ] Warnings (особливо black box warnings FDA) перелічені
- [ ] Взаємодії з поширеними concomitant medications перевірені

### 6.3. Dual review resolution

- Обидва reviewers згодні → merge
- Reviewer A згоден, Reviewer B має питання, які requestor виправив →
  merge після acknowledgment B
- Reviewers принципово розходяться → escalate до third reviewer або
  до full Clinical Editorial Board discussion
- Контроверсія не вирішується → **document both positions** з явною
  поміткою і let clinician-user вирішувати

### 6.4. Emergency content updates

Для критичних оновлень (drug recall, safety alert, нова black box
warning):

- Один Clinical Co-Lead + один зовнішній експерт можуть approve
  emergency change
- Change публікується з label `emergency_update`
- Full dual review протягом 7 днів post-publication
- Retroactive audit через 30 днів

---

## 7. Мовна політика

### 7.1. Внутрішня мова knowledge base — англійська

Knowledge base зберігається англійською для:
- Сумісності з міжнародними термінологіями (SNOMED CT, ICD-O, LOINC)
- Цитувань англомовних джерел без translation noise
- Міжнародного collaborators потенціалу

### 7.2. Output — багатомовний

Система генерує документи українською (primary) та англійською
(for reference). Translation:

- Клінічна термінологія — використовуємо офіційні українські
  відповідники з МКХ-10/11, наказів МОЗ, українських медичних
  словників
- Назви препаратів — за Державним формуляром України
- Назви досліджень — зберігаємо оригінальні англійські (KEYNOTE-522,
  BArT, BRIGHT тощо), не транслітеруємо
- Dosage units — метричні, SI-compliant (мг/м², мг/кг)

### 7.3. Consistency через glossary

Ведеться `GLOSSARY.md` з узгодженими translation pairs для clinical
terms. Це частина проекту, public і editable через standard review.

---

## 8. Conflict of interest (CoI) disclosure

Всі contributors клінічного контенту декларують CoI перед першим
прийнятим PR. Declaration public на сайті проекту.

### 8.1. Типи CoI, що потребують декларації

- Консалтинг для фармкомпаній (з переліком компаній)
- Speaking fees, honoraria
- Research grants (institutional і personal)
- Advisory board membership
- Equity / stock ownership у medical ventures
- Intellectual property / patents
- Family members з industry ties

### 8.2. Recusal rules

Contributor з декларованим CoI **не може бути primary author** для
рекомендацій, що стосуються продуктів компаній, з якими він має
зв'язок. Може бути reviewer якщо:

- CoI явно задекларований у review comments
- Другий reviewer — без CoI з цим же продуктом
- Escalation до Clinical Co-Lead для final approval

### 8.3. Публічна CoI page

На сайті проекту — публічна сторінка:

```
Clinical Content Contributors — CoI Declarations

[Reviewer Name], [Credentials], [Institution]
  Last updated: YYYY-MM-DD
  Industry relationships:
    - [Company X]: Speaking honoraria 2024-2025
    - [Company Y]: Advisory board 2023
  Research grants:
    - [NIH/European grant]: ongoing
  No ownership in medical companies
```

---

## 9. Knowledge base hygiene

### 9.1. Періодичний review

Раз на квартал кожен domain reviewer проходить свою область і
перевіряє:

- Чи не з'явилися нові major guidelines (NCCN updates, ESMO updates)
- Чи не з'явилися practice-changing RCTs (plenary abstracts ASCO/ESMO/ASH)
- Чи не було FDA safety alerts / drug withdrawals
- Чи рекомендації з last_reviewed > 6 місяців — валідні

Результат — quarterly report, публічний, з описом змін.

### 9.2. Annual full audit

Раз на рік — full audit всіх рекомендацій у домені, не тільки recently
changed. Випадкова вибірка (20% рекомендацій) перевіряється на
coherence.

### 9.3. Deprecation

Застарілі рекомендації не видаляються миттєво:

- Flag `deprecated` з `deprecated_reason` і `replacement_id`
- Deprecation period — 6 місяців з warning
- Архів зберігається безстроково для retrospective audits

---

## 10. Приклад застосування (mini case)

Щоб показати, як Standards працюють на практиці — коротка демонстрація
з HCV-MZL контекстом (реальний приклад буде в Reference Case doc).

**Сценарій:** додаємо нову рекомендацію "DAA + BR для HCV-MZL 1L"

**Contributor Q:**
```yaml
recommendation_id: REC-HCV-MZL-001
disease_entity: HCV-associated marginal zone lymphoma
clinical_scenario: First-line therapy, no red flags for transformation
recommendation: >
  Concurrent DAA (sofosbuvir/velpatasvir) + BR (bendamustine/rituximab)
  × 6 cycles, followed by rituximab maintenance 375 mg/m² q8w × 12 doses
evidence_level: Moderate (GRADE)
strength_of_recommendation: Preferred
sources:
  - {type: guideline, id: "NCCN-B-Cell-Lymphomas-v2.2026", section: "MZL-3"}
  - {type: guideline, id: "ESMO-MZL-2020-guidelines"}
  - {type: guideline, id: "EASL-HCV-2023"}
  - {type: phase2_trial, id: "BArT", citation: "Arcaini L, Blood 2014", pmid: "..."}
  - {type: phase3_rct, id: "BRIGHT", citation: "Flinn IW, JCO 2019", pmid: "..."}
...
```

**Reviewer A (онкогематолог):** Верифікує клінічну коректність, доза,
схема — OK. Зазначає: "Slight correction — bendamustine dose reduction
to 70 mg/m² при FIB-4 > 3.25 має бути explicit, не тільки в нотатках".

**Reviewer B (гепатолог):** Верифікує HCV-related частину. Зазначає:
"Заборонена комбінація sofosbuvir + amiodarone — потрібна окрема
CONTRA-запис і link з рекомендації". Creates CONTRA-AMIODARONE-SOFOSBUVIR
entry.

**Contributor Q** вносить виправлення → reviewers approve → merge.

Changelog:
```
2026-04-XX  REC-HCV-MZL-001 created
  Contributor: [id-Q]
  Reviewers: [id-A], [id-B]
  Sources: 5 (2 guidelines, 3 trials)
  Evidence level: Moderate
  Related entries: CONTRA-AMIODARONE-SOFOSBUVIR (new),
                   REC-HCV-MZL-002 (alternative aggressive path, existing)
```

---

## 11. Governance цього документа

- Зміни в Clinical Content Standards потребують consensus всіх Clinical
  Co-Leads + 14 днів public comment
- Перегляд документа раз на рік або за потреби
- Changelog ведеться в CHANGELOG-CCS.md

---

## 12. Поточний статус і обмеження

**v0.1 означає:**
- Skeleton для стартового обговорення з Clinical Co-Leads
- Потребує calibration під український клінічний контекст
- Потребує альфа-тестування на першій реальній рекомендації

**Що ще не вирішено:**
- Точний формат YAML/JSON для зберігання рекомендацій (Schema doc)
- Інструменти для автоматичного source validation
- Integration з reference management (Zotero? local bibliography?)
- Переклад GLOSSARY для початкових нозологій

**Перший test:** застосування Standards до HCV-MZL reference case —
чи зможемо ми відтворити реальний верифікований документ через
дисциплінований клінічний процес по цих standards?

---

**Пропозиції, критика, pull requests — вітаються через стандартний
governance process (CHARTER.md §6).**
