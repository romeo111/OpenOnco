# Source Ingestion & Licensing Specification

**Проєкт:** OpenOnco
**Документ:** Source Ingestion & Licensing — Hosting Matrix
**Версія:** v0.1 (draft, частина А — ліцензійно-хостингова матриця)
**Статус:** Draft для обговорення з Clinical Co-Leads та юридичним консультантом
**Попередні документи:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md, KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md
**Наступні частини (заплановані):**
- Part B — Per-source ingestion playbook (як саме тягнути кожне джерело)
- Part C — Conflict & precedence rules (що робить engine коли джерела розходяться)
- Part D — Freshness TTL & re-ingestion cadence

---

## Мета документа

CHARTER §2 декларує OpenOnco як **безкоштовний публічний інформаційний ресурс**.
KNOWLEDGE_SCHEMA_SPECIFICATION §5 (Source entity) передбачає агрегацію
з багатьох джерел — від NCCN і ESMO до OncoKB і МОЗ.

Ці дві вимоги конфліктують автоматично: **не всі джерела можна хостити**.
NCCN Guidelines захищені авторським правом, SNOMED CT вимагає ліцензії,
OncoKB має різні умови для академічного і комерційного використання,
і так далі.

Без чіткої ліцензійно-хостингової матриці ми або:
- (а) ризикуємо cease & desist від NCCN / Elsevier / SNOMED International
- (б) будуємо схему, яка **не може** містити те, що реально потрібно
  лікарю (текст рекомендації, а не тільки посилання)
- (в) платимо за ліцензії, які не планували

Цей документ фіксує **режим хостингу для кожного джерела** і випливаючі
з цього вимоги до `Source` entity.

**Основний принцип (§1.4):** `referenced` за замовчуванням — ми
**не дзеркалимо** зовнішні бази. `hosted` тільки тоді, коли є явне
обґрунтування (немає API, performance-critical matching, audit snapshot,
наш власний контент). Це робить knowledge base компактною, legally
safe за замовчуванням, і гарантує що користувач бачить завжди-свіжі
дані з джерела.

---

## 1. Режими хостингу (три режими)

Кожне джерело у базі знань OpenOnco має один з трьох режимів:

### 1.1. `hosted` (повний хостинг)

Ми завантажуємо, нормалізуємо і зберігаємо повний контент. Контент
відображається у UI без редиректу на зовнішнє джерело. Ми підтримуємо
versioning, `last_verified`, re-ingestion по кадансу.

**Допустимо для:** ClinicalTrials.gov, OpenFDA / DailyMed, CIViC, PubMed
abstracts (з застереженням — див. §2.4), МОЗ/НСЗУ протоколи, LOINC,
ICD-10-CM, FDA drug labels, EMA EPARs (з атрибуцією).

**Вимоги до UI/output:**
- Атрибуція джерела (логотип або текстове "via [source]")
- Лінк на оригінал при кожному використанні
- Якщо ліцензія вимагає — ShareAlike: наш output успадковує ту саму ліцензію
- Для CC-BY: обов'язкове збереження авторства

### 1.2. `referenced` (тільки посилання + метадані)

Ми зберігаємо **метадані** джерела (title, version, authors, date, URL,
DOI/PMID) і **короткий людський парафраз** (не цитату) який написали
наші клініцисти власними словами. Ми НЕ зберігаємо оригінальний текст
рекомендацій, таблиць, зображень з джерела.

**Допустимо для:** NCCN Guidelines, WHO Classification of Tumours, AJCC
Cancer Staging Manual, ESMO Pocket Guidelines (переважно), ASCO
Guidelines, Cochrane full-text reviews, OMIM, MedDRA (якщо без ліцензії).

**Вимоги до UI/output:**
- `Indication.rationale` може містити **наш** парафраз з атрибуцією:
  _"Per NCCN B-Cell Lymphomas Guideline v.2.2025 (paraphrased): for
  HCV-associated MZL, antiviral therapy is preferred first-line"_
- Ніколи не copy-paste з джерела
- Завжди клікабельний лінк на джерело
- Fair use для **дуже коротких** цитат (< 1 речення, з лапками і
  атрибуцією) допустимий в окремих випадках, але не за замовчуванням

### 1.3. `mixed` (структура так, проза ні)

Для джерел, які відкрито публікують структуровані дані (mutation-drug
mappings, trial records, taxonomies) але захищають наративний текст
авторським правом.

**Допустимо для:** OncoKB (academic tier), EMA EPARs (таблиці OK, PDF
body — атрибуція), FDA Structured Product Labels (sections yes, full
narrative з атрибуцією), ESMO (structured therapy tables за погодженням).

**Вимоги:**
- Структуровані поля (gene, variant, drug, evidence level) хостимо
- Проза summary / discussion — наш парафраз з посиланням
- Режим і ліцензія фіксуються на **рівні джерела**, а не per-fact

### 1.4. ⭐ Принцип: `referenced` за замовчуванням

**Якщо джерело можна референсити — референсимо. Ми не дзеркалимо
зовнішні бази.** Це founding principle для OpenOnco.

Причини:
- **Cost & maintenance:** мирорити CT.gov (500K+ записів), PubMed
  (38M abstracts), DailyMed — це інфраструктура, яку нам не треба
  утримувати, і mirror завжди застаріває відносно джерела
- **Freshness:** live API call бачить сьогоднішнє оновлення, snapshot — ні
- **Legal safety:** `referenced` автоматично знімає більшість copyright
  проблем — за замовчуванням безпечно
- **User trust:** користувач бачить оригінальне джерело з повним
  контекстом, не наш витяг з можливою інтерпретацією

`hosted` потребує **явного обґрунтування** хоча б за одним критерієм:

| # | Критерій | Типові приклади |
|---|---|---|
| **H1** | Немає API / публічного endpoint | МОЗ протоколи, НСЗУ формуляр, Держреєстр ЛЗ, PDF-only guidelines |
| **H2** | Performance-critical для rule matching | Code systems (ICD, LOINC, RxNorm, ATC) — rule engine викликає на кожному запиті |
| **H3** | Immutable audit snapshot потрібен | Version/date stamp джерела, яке лікар бачив при прийнятті рішення (тільки metadata snapshot, не full content) |
| **H4** | Власний контент проєкту | Наші Indications, Regimens, Contraindications, Algorithms, RedFlags |
| **H5** | Малий, стабільний і критичний для логіки | CTCAE v5.0 (toxicity grading), HGNC gene symbols, ICD-O-3 |

Якщо жодного H1-H5 — `referenced`. Crucially: rule engine звертається
до зовнішнього API (CT.gov, PubMed, DailyMed, openFDA) через наші
існуючі клієнти (`clinicaltrials_client.py`, `pubmed_client.py`) під час
evaluation, не читає з локального mirror.

**Де ми все ж кешуємо без хостингу:** Source entity завжди містить
metadata snapshot (title, version, URL, DOI, last_verified date) — це
не хостинг контенту, це цитата. `referenced` ≠ "нічого не зберігаємо";
це "зберігаємо citation, не content".

---

## 2. Ліцензійно-хостингова матриця

Матриця розбита на 7 tier-ів за функціональною роллю у базі. Пріоритет
для OpenOnco: **Tier 3 (Ukraine-local)** важливіша за Tier 1 для
фактичного видавання планів — без неї не можна визначити що пацієнту
доступно.

### 2.1. Tier 1 — Core primary clinical sources

| Джерело | Ліцензія | Режим | Що можна зберігати | Commercial use | Гарячі точки |
|---|---|---|---|---|---|
| **NCCN Guidelines** | © NCCN, free personal use with registration, **no redistribution** | `referenced` | URL, version, date, наш парафраз | ❌ потрібна ліцензія | Активна правозастосовна діяльність. Не хостити таблиці й текст. [licensing info](https://www.nccn.org/guidelines/nccn-guidelines) |
| **ESMO Clinical Practice Guidelines** | Зазвичай CC-BY-NC-ND 4.0 (recent years, в _Annals of Oncology_) | `mixed` | Structured therapy recommendations + парафраз + full citation | NC only — **наш "вільний ресурс" ≈ non-commercial, але перевірити** | NC-ND: creating a rule engine може бути "derivative" — уточнити з юристом |
| **ASCO Guidelines** | © ASCO, published in JCO, free to read, redistribution restricted | `referenced` | Metadata + парафраз | ❌ | [ASCO reprint policy](https://ascopubs.org/action/clickThrough?id=7009&url=%2Fpermissions) |
| **WHO Classification of Tumours (5th ed.)** | © WHO/IARC, proprietary | `referenced` | ICD-O-3 codes (public), classification naming — парафраз | ❌ for content | IARC активно ліцензує |
| **AJCC Cancer Staging Manual** | © American Cancer Society / Springer | `referenced` | Stage назви (parafrase) + посилання | ❌ | Комерційне використання stage tables заборонене |
| **Cochrane Systematic Reviews** | Зазвичай subscription, в Україні доступ через Cochrane Collaboration | `referenced` | Abstract summary (короткий парафраз) + DOI | ❌ | Full text paywalled; abstracts можна зберігати |

**Практичний висновок для Tier 1:** OpenOnco **не хостить контент** Tier 1.
Для кожної Indication клінічний рев'юер пише власний `rationale` і
посилається на джерело. Це основний клінічний шар, який вимагає ручної
праці.

### 2.2. Tier 2 — Regulatory (FDA, EMA, DailyMed)

| Джерело | Ліцензія | Режим | Що можна зберігати | Гарячі точки |
|---|---|---|---|---|
| **FDA drug labels** (DailyMed / openFDA) | US government work, public domain | `referenced` | Metadata + DailyMed ID; live API call при rule evaluation | [openFDA API](https://open.fda.gov/) |
| **FDA Orange Book / Purple Book** | US gov, public domain | `referenced` | Metadata + посилання | — |
| **EMA EPARs** (European Public Assessment Reports) | © EMA, reuse з атрибуцією non-commercial | `referenced` | Metadata + EPAR number + URL | — |
| **Health Canada Drug Product Database** | Crown copyright, open license | `referenced` | Metadata + DIN | — |
| **UK MHRA** | Crown copyright, OGL (Open Government Licence) | `referenced` | Metadata | — |
| **Australian TGA** | Crown copyright, CC-BY 4.0 більшість | `referenced` | Metadata | — |

**Практичний висновок для Tier 2:** **Референсимо через live API**, не
мірроримо. openFDA / DailyMed API викликаються при rule evaluation через
клієнт (треба додати `dailymed_client.py` подібно до existing `pubmed_client.py`).

**Виняток до розгляду (ескалація до `mixed`):** якщо rule engine latency
для Drug.contraindication lookup через openFDA стає проблемою — кешуємо
тільки ті structured fields (contraindications, AE lists), що реально
потрібні для matching, per критерієм H2 (§1.4). Починаємо з pure
`referenced`, переходимо до `mixed` за даними produkcyjnego latency.

### 2.3. Tier 3 — Ukraine-local (Tier 1 за пріоритетом для проєкту)

| Джерело | Ліцензія | Режим | Що можна зберігати | Гарячі точки |
|---|---|---|---|---|
| **Уніфіковані клінічні протоколи МОЗ** | Public (державний документ) | `hosted` | Повний текст протоколу | Немає API, потрібен scraper з [moz.gov.ua](https://moz.gov.ua/) |
| **НСЗУ формуляр (реімбурсовані препарати)** | Public | `hosted` | Повний список + умови | [nszu.gov.ua](https://nszu.gov.ua/) — формат PDF/Excel, оновлення ~щомісяця |
| **Державний формуляр лікарських засобів** | Public | `hosted` | Повний | [dec.gov.ua](https://www.dec.gov.ua/) — щорічні оновлення |
| **Реєстр лікарських засобів (ДЕЦ МОЗ)** | Public | `hosted` | Реєстраційні дані, МНН, виробник | [Державний реєстр ЛЗ](https://www.drlz.com.ua/) |

**Практичний висновок для Tier 3:** **Все хостимо.** Це те, що робить
OpenOnco реально корисним для України (на відміну від "ще одна копія NCCN").
**НО**: жодне з цих джерел не має modern API. Всі — PDF/HTML scraping
або ручна data entry. Це основна інженерна робота Tier 3.

### 2.4. Tier 4 — Clinical trials + literature

| Джерело | Ліцензія | Режим | Що можна зберігати | Гарячі точки |
|---|---|---|---|---|
| **ClinicalTrials.gov** | US NLM, public domain | `referenced` | Metadata snapshot (NCT ID, title, date accessed) для audit. Live query через `clinicaltrials_client.py` при evaluation | [API v2](https://clinicaltrials.gov/data-api/api). Не мірроримо — 500K+ records змінюється щодня |
| **EU Clinical Trials Register (EUCTR)** | © EMA, reuse з атрибуцією | `referenced` | Metadata + EudraCT number + link | Немає дружнього API, live query через scraping тільки на потребу |
| **PubMed / MEDLINE metadata** | NLM, здебільшого public domain | `referenced` | PMID + metadata snapshot. Abstracts викликаються live через `pubmed_client.py` | Живі запити E-utilities; per-journal copyright concerns не зачіпають, бо ми не host'имо |
| **PubMed Central OA Subset** | CC-BY, CC-BY-NC, per-article | `referenced` | PMCID + metadata | Full-text live fetch per-query; не mirror |
| **PubMed full text (non-OA)** | Publisher-copyright | `referenced` | PMID + metadata + link | Ніколи не хостимо |
| **Cochrane Library** | Subscription + Cochrane terms | `referenced` | Abstract summary (короткий парафраз) + DOI | Див. Tier 1 |
| **bioRxiv / medRxiv** | CC-BY 4.0 (здебільшого) | `referenced` | Metadata + DOI; live fetch при потребі | Статус "preprint, not peer-reviewed" — клінічна вимога до UI |

**Практичний висновок для Tier 4:** **Все референсимо.** Клієнти
`clinicaltrials_client.py` і `pubmed_client.py` вже існують у репозиторії
і використовуються rule engine live, не для batch ingestion. Це значно
спрощує infrastructure: немає ETL pipeline, немає cron, немає SQLite
mirror для 500K trials і 38M abstracts.

**Що зберігаємо локально:** тільки `Source` entity metadata snapshot
(NCT-ID, PMID, title, version/date на момент цитування). Це citation
record для audit — "ця рекомендація посилалась на NCT05123456 на
2026-04-24" — не копія даних.

**Risk:** залежність від uptime і rate limits зовнішніх API.
CT.gov / NLM мають occasional downtime. Для clinical tool це треба
обходити: graceful degradation + local cache з TTL (годинник-день),
не mirror.

### 2.5. Tier 5 — Molecular / biomarker KBs

| Джерело | Ліцензія | Режим | Що можна зберігати | Гарячі точки |
|---|---|---|---|---|
| **OncoKB** | Academic free + attribution; commercial paid | `referenced` | Metadata + live API call через академічний tier | [OncoKB terms](https://www.oncokb.org/terms). Якщо OpenOnco переходить у commercial deployment — license |
| **CIViC** | CC0 | `hosted` (H2 + H5) | Full variant-evidence records локально | Малий (~10K entries), performance-critical для biomarker→indication matching, CC0 знімає legal constraints |
| **JAX Clinical Knowledgebase (CKB)** | Free academic, commercial paid | `referenced` | Metadata | Подібно до OncoKB |
| **MyCancerGenome** | Variable per entry | `referenced` | Metadata | Перевіряти per entry |
| **COSMIC** | Academic free registration; commercial paid | `referenced` | Metadata + query link | Sanger активно розділяє tiers після 2024 |
| **ClinVar** | Public domain (NCBI) | `referenced` | Metadata + variant ID; live API query | — |
| **gnomAD** | Public | `referenced` | Live API query для population frequencies | — |

**Практичний висновок для Tier 5:** **CIViC — єдиний hosted** в цьому
tier — обґрунтування H2 (rule engine потребує fast lookup variant →
evidence при кожній patient evaluation) + H5 (малий, стабільний, CC0 без
обмежень). Все інше — referenced через API.

### 2.6. Tier 6 — Terminologies / code systems

| Джерело | Ліцензія | Режим | Що можна зберігати | Гарячі точки |
|---|---|---|---|---|
| **ICD-10-CM** (US) | Public domain (CDC/CMS) | `hosted` | Full | OK |
| **ICD-10** (WHO) | WHO — free використання з обмеженнями | `hosted` з атрибуцією | Full | Modifications потребують WHO permission |
| **ICD-O-3.2** | WHO — free academic/clinical | `hosted` з атрибуцією | Full | Comerc OK for authorized users |
| **SNOMED CT** | SNOMED International, per-country license | ⚠️ **LICENSE REQUIRED** | Нічого без ліцензії | Україна не є member country на момент написання. Альтернатива: LOINC + ICD + own code system |
| **LOINC** | Regenstrief, LOINC License (attribution required, no modifications без дозволу) | `hosted` з атрибуцією | Full | OK. [LOINC License](https://loinc.org/license/) |
| **RxNorm** | NLM / UMLS, permissive | `hosted` з атрибуцією | Full | UMLS Terminology Services license потребується, але безкоштовна |
| **ATC / DDD** (WHO Collaborating Centre) | Free for academic/personal; commercial licensed | `hosted` з атрибуцією | Full | [ATC/DDD policy](https://www.whocc.no/copyright_disclaimer/) — commercial redistribution потребує ліцензії |
| **HGNC (HUGO gene symbols)** | Free, CC-BY 4.0 | `hosted` | Full | OK |
| **MedDRA** | MSSO, license required | ⚠️ **LICENSE REQUIRED** | Нічого без ліцензії | Для non-profit — фіксована річна плата. [MedDRA licensing](https://www.meddra.org/subscription) |
| **HGVS nomenclature** | Free, HGVS Society | `hosted` | Full syntax | OK |
| **UCUM (units of measure)** | Regenstrief, free | `hosted` | Full | OK |

**Практичний висновок для Tier 6:** Це **основний виняток** з принципу
"referenced за замовчуванням" (§1.4). Code systems hosted за критеріями
**H2** (rule engine викликає code lookup на кожному patient match —
ICD → Disease, LOINC → Test, RxNorm → Drug — latency API-call per-query
некерована) та **H5** (малі, стабільні, критичні для логіки).

- **SNOMED CT — не використовуємо в MVP.** Без country license не маємо
  права. Для lab results + clinical concepts використовуємо
  **LOINC + ICD + RxNorm + власна lightweight taxonomy** для клінічних
  концептів, що не покриті цими трьома.
- **MedDRA — не використовуємо в MVP.** AE описуємо вільним текстом +
  CTCAE v5.0 grading (public domain, NCI).
- **ATC — hosted з обережністю.** Для non-commercial OpenOnco OK; якщо
  проєкт переходить у commercial — license. Fallback: RxNorm.

### 2.7. Tier 7 — Research datasets (валідація, не knowledge)

Ці джерела **не входять** у knowledge base як авторитет рекомендацій.
Використовуються для валідації (чи engine дає розумні відповіді на
реальних когортах) і epidemiological context.

| Джерело | Ліцензія | Режим | Використання |
|---|---|---|---|
| **TCGA (public tier)** | NIH, public | `referenced` (dataset) | Validation cohort |
| **AACR Project GENIE** | CC-BY 4.0 (registered users) | `referenced` | Validation cohort |
| **cBioPortal** | Variable per dataset | `referenced` | Query interface |
| **MMRF CoMMpass** | Controlled access | `referenced` | Validation (myeloma) |
| **SEER** | Public summaries; patient-level — application | `referenced` | Epi context |
| **DepMap** | Broad, free for research | `referenced` | Drug response validation |
| **MIMIC-IV** | PhysioNet credentialed access | `referenced` | NLP/EHR context |

**Практичний висновок для Tier 7:** Не впливають на `Source` entity в
knowledge base. Це **testing artifacts**, не джерела рекомендацій.
Окрема частина документа (Part E — Validation Datasets) опише доступ і
use case кожного.

---

## 3. Необхідні доповнення до `Source` entity

KNOWLEDGE_SCHEMA_SPECIFICATION §5 (Source) описує title, version, authors,
journal, DOI, PMID, URL, access_level, currency_status, evidence_tier.
Цього недостатньо для ліцензійно-свідомої агрегації. Додати:

```yaml
Source:
  id: "SRC-CTGOV-REGISTRY"           # абстракція для registry, не per-trial
  source_type: "clinical_trials_registry"
  # ... existing fields from KNOWLEDGE_SCHEMA_SPECIFICATION §5 ...

  # NEW — licensing & hosting fields
  hosting_mode: "referenced"         # hosted | referenced | mixed
  hosting_justification: null        # H1..H5 якщо hosted, інакше null
  ingestion:
    method: "live_api"               # live_api | scheduled_batch | manual | none
    client: "clinicaltrials_client.py"   # модуль, який робить запит
    endpoint: "https://clinicaltrials.gov/api/v2"
    rate_limit: "50 req/min per IP"  # з документації джерела
  cache_policy:
    enabled: true                    # для referenced — query-level cache
    ttl_hours: 24                    # для CT.gov; для code systems N/A (hosted)
    scope: "query_result"            # query_result | entity_snapshot | none
  license:
    name: "US public domain"
    url: "https://clinicaltrials.gov/about-site/terms-conditions"
    spdx_id: null                    # SPDX якщо застосовно (e.g. "CC-BY-4.0", "CC0-1.0")
  attribution:
    required: false
    text: "Data from ClinicalTrials.gov, National Library of Medicine"
    logo_url: null
  commercial_use_allowed: true
  redistribution_allowed: true
  modifications_allowed: true
  sharealike_required: false
  known_restrictions: []
  legal_review:
    status: "reviewed"               # pending | reviewed | escalated
    reviewer: "[name/org]"
    date: "2026-05-01"
    notes: "Verified public domain; referenced mode avoids redistribution concerns"
```

`hosting_mode` — primary switch. Rule engine і UI повинні поводитись
по-різному для `hosted` і `referenced` джерел:
- `hosted` — цитуємо контент напряму, зберігаємо `last_verified`,
  re-ingest по кадансу
- `referenced` — показуємо тільки metadata + клікабельний link + наш
  парафраз з `Indication.rationale`. Ніколи не показуємо заархівований
  оригінал

---

## 4. Сірі зони і edge cases

### 4.1. Fair use для освітніх цитат

В законодавстві США і деяких європейських країнах допустима коротка
цитата (1-2 речення) з атрибуцією для освітніх/критичних цілей.
Українське законодавство має подібну концепцію "правомірного відтворення"
(ст. 21 Закону України "Про авторське право і суміжні права").

**Політика OpenOnco:** fair use **не є основою** нашої архітектури. Ми
не покладаємось на fair use для routine operation. Якщо у rationale
потрібна дуже коротка цитата з NCCN (<20 слів) в лапках з атрибуцією
для специфічного клінічного моменту — це допустимо, але requires
clinical co-lead review. Не автоматизувати.

### 4.2. PubMed abstracts: public чи publisher?

NLM технічно дистрибутивує abstracts як частину MEDLINE. Але NLM Data
Distribution terms попереджають: "Some abstracts may be copyrighted by
the publisher." Для особистого research OK; для публічного API
поверх — gray area.

**Політика OpenOnco:** **не хостимо** PubMed abstracts. Запитуємо live
через E-utilities (`pubmed_client.py`) при rule evaluation. Зберігаємо
тільки PMID + metadata snapshot (title, date, journal) як citation record.
Це автоматично знімає copyright concern (ми не дистрибутивуємо контент)
і дає завжди-свіжу версію abstract.

### 4.3. "Free public resource" = commercial use?

Це **ключове питання** для кількох ліцензій (ESMO CC-BY-NC-ND, OncoKB,
ATC). "Non-commercial" зазвичай означає no-profit-motive. OpenOnco:
- Open source, вільний доступ, без платних tier-ів → non-commercial
- Якщо в майбутньому з'явиться enterprise tier, paid API, hospital
  deployment licenses — **стає commercial**

**Політика OpenOnco:** поки ми **100% non-profit-motive public resource**
— ми non-commercial. У `CHARTER.md §2` треба зафіксувати це як
нерухоме обмеження: зміна на commercial model = triggers license audit
всіх `referenced` і `mixed` джерел.

### 4.4. Screenshots / rendered content з NCCN

Абсолютно ні. Скриншот NCCN flowchart — це копіювання їхньої
compiled intellectual property, навіть без тексту. Ніколи не хостимо
ні як image, ні як SVG, ні як reimplementation.

### 4.5. ShareAlike: що робить наш output

Якщо ми інтегруємо CC-BY-SA джерело, наш derivative output успадковує
SA. CC0 і CC-BY — не успадковують. Більшість наших джерел — public
domain, CC-BY, або proprietary. **SA-джерела на сьогодні не плануємо** —
якщо з'являться, треба окремо фіксувати у `license.sharealike_required`.

---

## 5. Що заборонено

Явна негативна список:

1. **Не хостити NCCN Guidelines контент** — текст, таблиці, flowcharts,
   screenshots. Тільки `referenced` режим з нашим парафразом.
2. **Не використовувати SNOMED CT концепти** в MVP без country license.
   Для clinical concepts — LOINC + ICD + власна taxonomy.
3. **Не використовувати MedDRA** для coding AE — тільки CTCAE v5.0
   (public) плюс free-text.
4. **Не хостити Cochrane full text reviews** — тільки abstracts + DOI.
5. **Не хостити ESMO narrative** без per-publication перевірки ліцензії
   (NC-ND має обмеження).
6. **Не показувати PubMed full text** для non-OA статей. Тільки abstract
   і лінк на DOI / публікаційну сторінку.
7. **Не створювати derivatives з CC-BY-NC-ND джерел** (як ESMO
   recent years) — rule engine поверх parsed guidelines може
   кваліфікуватись як derivative. **Потребує юридичного уточнення.**
8. **Не використовувати OncoKB поза academic tier** без license — якщо
   OpenOnco масштабується у клініки комерційно, OncoKB triggers license fee.

---

## 6. Червоні прапори — потребують юридичного ревю до публічного запуску

Перед тим як `CHARTER §2` перейде з "draft" у "published":

1. **ESMO CC-BY-NC-ND derivative question** — чи rule engine, що парсить
   структуровані рекомендації ESMO, є "derivative work"? Якщо так —
   CC-BY-NC-ND забороняє. Якщо ні — можна використовувати з атрибуцією.
2. **PubMed abstracts commercial distribution** — якщо OpenOnco коли-
   небудь переходить у платний tier, перевіряти NLM Data Distribution.
3. **ATC codes commercial use** — якщо commercial, потрібна ліцензія від
   WHO Collaborating Centre.
4. **OncoKB academic tier scope** — clarify whether OpenOnco deployment
   у приватну клініку вважається commercial OncoKB use.
5. **SNOMED CT timing** — моніторити чи Україна приєднається до SNOMED
   International як member country. Якщо так — можемо почати
   використовувати.

---

## 7. Seed list для reference case (HCV-MZL)

Конкретні джерела, які треба підключити для першого працюючого use case
(HCV-associated Marginal Zone Lymphoma per `REFERENCE_CASE_SPECIFICATION.md`):

Розбито на два блоки: що хостимо (мінімальний, критичний), що референсимо
(переважна більшість).

#### 7.1. Hosted (локально, з обґрунтуванням)

| Джерело | Обґрунтування | Що дає для HCV-MZL | Наступний крок |
|---|---|---|---|
| **CIViC** | H2 + H5 + CC0 | Variant-evidence entries (якщо є MZL-specific) | Discovery через API, download subset локально |
| **CTCAE v5.0** | H2 + H5 | Toxicity grading для Regimen AE fields | Download PDF, parse → structured JSON |
| **ICD-O-3.2 codes** | H2 | Code 9699/3 (extranodal MZL), 9689/3 (splenic) | Download code table |
| **LOINC** (subset) | H2 | FIB-4, HCV RNA, CD20 IHC codes | API download, cache subset |
| **RxNorm / ATC** (subset) | H2 | L01FA01 (rituximab), L01AA09 (bendamustine) | Manual table, 20-30 drugs для MVP |
| **МОЗ Уніфікований клінічний протокол "Лімфома"** | H1 (немає API) | Ukrainian guideline — baseline рекомендацій | Scrape [moz.gov.ua](https://moz.gov.ua/), clinical reviewer verify |
| **НСЗУ формуляр** (для MZL-відповідних препаратів) | H1 | Чи реімбурсований bendamustine/rituximab в Україні | PDF parser + manual verify |
| **Державний реєстр ЛЗ** (для MZL-відповідних) | H1 | Чи зареєстровані препарати в Україні | Scraper |
| **Наші Indications, Regimens, Contraindications** | H4 | Вся клінічна логіка для HCV-MZL (два плани) | Clinical co-leads пишуть в YAML |

**Усього hosted:** код-системи + Ukraine-local (немає API) + наш власний
контент. Це мінімальний набір, де external reference неможливий або
ламає performance.

#### 7.2. Referenced (live API / link)

| Джерело | Як звертаємось | Що дає для HCV-MZL |
|---|---|---|
| **ESMO MZL Guideline 2024** | URL + clinical reviewer paraphrase | Рекомендації першої лінії, antiviral-first strategy |
| **NCCN B-Cell Lymphomas v.2.2025** | URL + paraphrase | Parallel opinion, categories of preference |
| **EASL HCV Guideline** | URL + paraphrase | Antiviral (DAA) regimens |
| **ClinicalTrials.gov** | live API via `clinicaltrials_client.py` | Active trials (filter: MZL, indolent lymphoma, Ukraine/EU sites) |
| **PubMed** | live E-utilities via `pubmed_client.py` | Key trials (Arcaini 2014, Hermine 2002) — citation metadata only |
| **DailyMed / openFDA** | live API (потрібен `dailymed_client.py`) | Bendamustine, rituximab, obinutuzumab labels — contraindications, AE |
| **EMA EPARs** | URL + metadata snapshot | EU-specific labels, differences from FDA |
| **OncoKB** | academic API + metadata | Biomarker-treatment mappings якщо є |
| **ClinVar, gnomAD** | live API | Variant interpretation / population frequency |

**Усього referenced:** ~80% джерел. Жодного ETL pipeline, жодного
batch ingestion — все через клієнти під час rule evaluation.

**Відсутні в seed list (deliberately):**
- SNOMED CT — license gate
- MedDRA — license gate
- Cochrane full text — paywalled

---

## 8. Процес додавання нового джерела

Для майбутніх джерел (коли розширюємось за межі HCV-MZL):

1. **Ідентифікувати ліцензію.** URL на офіційні terms. Canonical
   license name (SPDX ID якщо є).
2. **Визначити hosting mode** за правилами §1. В разі сумніву —
   `referenced`.
3. **Провірити 4 обмеження:**
   - Commercial use allowed?
   - Redistribution allowed?
   - Modifications allowed?
   - ShareAlike required?
4. **Додати рядок у матрицю §2** у відповідний tier.
5. **Створити `Source` entity** з усіма `license`, `attribution`,
   `hosting_mode` полями.
6. **Якщо `hosting_mode: hosted`** — додати ingestion playbook у
   Part B (коли буде написана).
7. **Якщо red flag (Tier 1 license, commercial ambiguity, member-only
   access)** — `legal_review.status: pending`, блокується до ревю.

---

## 9. Дисклеймер

**Цей документ — engineering best-effort аналіз, не юридична консультація.**

Ліцензії змінюються. NCCN може оновити terms. Україна може приєднатися
до SNOMED. ESMO може переключити частину гайдлайнів на іншу CC-ліцензію.
Перед публічним запуском OpenOnco:

- (а) Мати юридичного консультанта з досвідом у IP / медичних даних
  (Україна + міжнародне)
- (б) Юридичний ревю всіх `Tier 1`, `mixed`-mode, і всіх джерел з
  `legal_review.status: pending`
- (в) Зафіксувати terms-of-use OpenOnco, які явно описують:
  - non-commercial character
  - disclaimers
  - як користувачі можуть повідомити про проблеми з ліцензіями
  - процес швидкого видалення контенту у разі claim

**Кожні 6 місяців — повний аудит матриці §2.** Джерела з
`last_reviewed > 6 months` ago автоматично потрапляють у audit queue.

---

# Part B — Per-source Ingestion Playbook

## 11. Scope і цілі Part B

Part A зафіксувала **що** можна робити з кожним джерелом (legally).
Part B фіксує **як** ми це реально робимо: де живуть дані, які
клієнти звертаються до яких API, коли оновлюються, хто верифікує, що
робимо при збої.

**Критерій готовності Part B:** інженер має змогу взяти цей документ +
список seed-джерел з §7 і **за тиждень** підключити першу hosted
сутність (наприклад, ICD-O-3.2 коди) без додаткових питань до product.

---

## 12. Загальні патерни

### 12.1. Структура knowledge_base/ на диску

Пропонована структура (відкрита для обговорення):

```
knowledge_base/
├── hosted/
│   ├── code_systems/
│   │   ├── icd_o_3/
│   │   │   ├── v2020/
│   │   │   │   ├── codes.yaml           # повний code table
│   │   │   │   ├── _meta.yaml           # version, fetched_at, source_url, checksum
│   │   │   │   └── _diff_from_prev.yaml # що змінилось відносно попередньої версії
│   │   │   └── current → v2020          # symlink на active version
│   │   ├── loinc/v2.76/...
│   │   ├── rxnorm/2026-04/...
│   │   └── atc/2025/...
│   ├── civic/
│   │   └── 2026-04-24/evidence.yaml
│   ├── ctcae/
│   │   └── v5.0/grading.yaml
│   ├── ukraine/
│   │   ├── moz_protocols/
│   │   │   └── lymphoma-2024/
│   │   │       ├── source.pdf           # original для audit
│   │   │       ├── extracted.yaml       # structured витяг
│   │   │       └── review.yaml          # клінічний рев'юер підписав
│   │   ├── nszu_formulary/2026-04/reimbursed.yaml
│   │   └── drlz_registry/2026-04-24/registered.yaml
│   └── content/                          # H4 — наш власний контент
│       ├── diseases/
│       │   └── hcv_mzl.yaml
│       ├── drugs/
│       │   ├── rituximab.yaml
│       │   └── bendamustine.yaml
│       ├── regimens/
│       │   ├── br_standard.yaml
│       │   └── r_chop_aggressive.yaml
│       ├── indications/
│       │   ├── ind_hcv_mzl_1l_antiviral.yaml
│       │   ├── ind_hcv_mzl_1l_br.yaml
│       │   └── ind_hcv_mzl_1l_rchop.yaml
│       ├── biomarkers/
│       ├── contraindications/
│       ├── redflags/
│       └── algorithms/
│           └── algo_hcv_mzl_1l.yaml
├── referenced/
│   └── sources.yaml                      # registry всіх referenced Source entity
└── cache/                                # gitignored! не комітити
    ├── ctgov/
    │   └── <query_hash>.json             # TTL-expiring
    ├── pubmed/
    │   └── <pmid>.json
    ├── dailymed/
    │   └── <setid>.json
    └── ...
```

**Чому YAML а не JSON/SQLite:**
- Читабельність для клінічних рев'юерів (вони редагують контент руками)
- Git-friendly diffs (рев'ю через PR)
- Schema validation через Pydantic/JSONSchema на CI
- Міграція на PostgreSQL пізніше (KNOWLEDGE_SCHEMA §16.1 допускає) — коли KB перевищить ~10K entries

**Чому версіонування через директорії (v2020/, v2.76/) а не git tags:**
- Hosted code system може мати 2020 і 2024 версії **одночасно активними**
  — наприклад, historical indication посилається на old ICD
- Git tag = snapshot всього repo, не per-source versioning
- Symlink `current` дозволяє rule engine брати active без зміни шляху

**Що gitignored:**
```
# .gitignore additions for knowledge_base
knowledge_base/cache/
knowledge_base/**/_fetch_log.json  # per-fetch run logs
```

### 12.2. Уніфікований клієнт інтерфейс

Всі live-API клієнти для referenced-джерел реалізують один протокол:

```python
# knowledge_base/clients/base.py

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SourceResponse:
    data: Any
    source_id: str          # "SRC-CTGOV-REGISTRY"
    fetched_at: str         # ISO-8601
    cache_hit: bool
    api_version: str        # whatever endpoint returns

@dataclass
class RateLimit:
    tokens_per_second: float
    burst: int

class SourceClient:
    """Base interface for all referenced-source API clients."""
    source_id: str
    base_url: str
    rate_limit: RateLimit
    cache_ttl_seconds: int

    def fetch(self, query: dict) -> SourceResponse: ...
    def health(self) -> dict: ...      # {ok: bool, latency_ms: int, last_error: str|None}
    def quota(self) -> dict: ...        # {remaining: int, reset_at: str}
```

**Реалізації для seed:**
- `knowledge_base/clients/ctgov_client.py` — рефактор з existing
  `clinicaltrials_client.py` (зараз у top-level)
- `knowledge_base/clients/pubmed_client.py` — рефактор з existing
- `knowledge_base/clients/dailymed_client.py` — **новий**
- `knowledge_base/clients/openfda_client.py` — **новий**
- `knowledge_base/clients/oncokb_client.py` — **новий** (academic tier,
  needs token)
- `knowledge_base/clients/clinvar_client.py` — **новий**
- `knowledge_base/clients/gnomad_client.py` — **новий**

### 12.3. Кешування для referenced-джерел

Query-level кеш з TTL. Не mirror.

```python
# Псевдо-інтерфейс

class TTLCache:
    def get(self, key: str) -> Optional[SourceResponse]: ...
    def put(self, key: str, value: SourceResponse, ttl_seconds: int): ...
    def invalidate(self, key: str): ...
```

**TTL per source** (див. §22 для повної таблиці):
- CT.gov: 24 години (trials оновлюються щоденно, но per-trial рідко)
- PubMed: 7 днів (abstracts стабільні після публікації)
- DailyMed/openFDA: 7 днів (labels оновлюються рідко)
- OncoKB: 7 днів
- ClinVar/gnomAD: 30 днів (variant interpretations стабільніші)

**Cache key:**
- Для GET з параметрами: `{source_id}:{endpoint}:{sorted_params_hash}`
- Для POST запитів (rare): `{source_id}:{endpoint}:{body_hash}`

**Invalidation triggers:**
- TTL expiry (passive)
- Explicit bust через admin CLI (коли знаємо що джерело оновилось)
- Source entity `last_verified` оновлюється — виконує bust по всім
  cached responses з цього source

### 12.4. Загальна обробка збоїв (graceful degradation)

Рівні поведінки коли external API не відповідає:

| Поведінка | Для чого застосовується |
|---|---|
| **Hard fail** — rule engine повертає помилку | Ніколи. Ми не блокуємо генерацію плану через один downed API |
| **Soft degrade** — позначити в output що джерело недоступне | Default для всіх referenced-джерел |
| **Stale cache** — використовувати expired кеш з warning | CT.gov, PubMed коли TTL expired + API down |
| **Skip** — не цитувати це джерело, продовжити | OncoKB недоступний — генеруємо без biomarker evidence посилань |

Rule engine зобов'язаний:
1. Встановити timeout на кожен client call (default 10s)
2. Логувати failure в `_fetch_log.json` (source_id, timestamp, error)
3. Додавати до output `freshness_warnings` list з джерелами, які не
   вдалось звертнути
4. UI відображає warning іконку поряд з affected citations

### 12.5. Валідація schema

Кожен hosted entity (code table, CIViC record, наш Indication) проходить:

1. **Pydantic / JSONSchema validation** при завантаженні — structure
2. **Referential integrity check** — всі ID-referencing поля знаходять
   target (Indication.drug_id → Drug.id існує)
3. **Clinical sanity check** (для нашого content) — см. CLINICAL_CONTENT_STANDARDS
4. **License compliance check** — Source entity має `hosting_mode`,
   `license`, `legal_review.status != pending`

На CI (GitHub Actions): fail PR якщо хоч одна перевірка падає.

---

## 13. Hosted: Code systems (ICD-O-3, LOINC, RxNorm, ATC)

### 13.1. Загальний pattern

Всі code systems мають спільний flow:
1. **Download** офіційного файлу (CSV / XML / TSV / JSON) з source
2. **Parse** у канонічний YAML
3. **Diff** проти попередньої версії — що додано, видалено, змінилось
4. **Clinical reviewer** підписує що diff не ламає active Indications
5. **Commit** нової версії директорії
6. **Switch symlink** `current/` на нову версію

### 13.2. ICD-O-3.2

- **Source:** WHO ([ICD-O-3.2](https://www.who.int/standards/classifications/other-classifications/international-classification-of-diseases-for-oncology))
- **Format:** downloadable CSV + PDF reference
- **Update cadence:** rare (revisions раз на декілька років); monitor WHO news
- **Scope for MVP:** Повний code table (~2000 morphology + ~300 topography). Невеликий.
- **Ingestion:** ad-hoc manual download, one-time. Automated re-check once yearly.
- **Structure after parse:**
  ```yaml
  # knowledge_base/hosted/code_systems/icd_o_3/v2020/codes.yaml
  morphology:
    - code: "9699/3"
      term: "Extranodal marginal zone B-cell lymphoma of mucosa-associated lymphoid tissue (MALT lymphoma)"
      behavior: "3"  # malignant
      synonyms: ["MALT lymphoma", "extranodal MZL", ...]
    - code: "9689/3"
      term: "Splenic B-cell marginal zone lymphoma"
      ...
  topography:
    - code: "C16.0"
      term: "Cardia, stomach"
  ```
- **Client owner:** none (no API, one-time download)
- **Clinical review:** один рев'юер підтверджує що нові/deprecated коди
  не осиротять existing Indications

### 13.3. LOINC

- **Source:** Regenstrief ([LOINC](https://loinc.org/downloads/))
- **Format:** CSV / Zip download, requires LOINC free account
- **Update cadence:** 2x на рік (June, December)
- **Scope for MVP:** **Subset** — тільки codes, що використовуються в
  наших Tests. Для HCV-MZL це ~30-50 codes (FIB-4 components, HCV RNA
  PCR, CD19/CD20 IHC, CBC, LDH, B2-microglobulin, β2m, тощо).
- **Full LOINC:** ~100K codes; ми не хостимо повний. `v2.76/codes.yaml`
  має тільки `curated_subset: true` flag і список використовуваних
- **Ingestion:** CSV download + Python script що фільтрує по list
  із `knowledge_base/hosted/content/_loinc_usage.txt`
- **Attribution:** LOINC license вимагає "This material contains
  content from LOINC® (http://loinc.org)" у UI.
- **Client owner:** optional — LOINC FHIR API exists, але для subset
  швидше один раз downloaded локально

### 13.4. RxNorm

- **Source:** NLM ([RxNorm download](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html))
- **Format:** ZIP with RRF (Rich Release Format) files
- **Update cadence:** monthly (1st Monday)
- **Scope for MVP:** subset — drugs in our Regimens. Для HCV-MZL це
  ~10-15 препаратів (rituximab, bendamustine, cyclophosphamide, vincristine,
  prednisone, doxorubicin, obinutuzumab, sofosbuvir, velpatasvir, etc.)
- **Ingestion:** RRF files — складний формат. Парсимо
  `RXNCONSO.RRF` + `RXNREL.RRF`, екстрактимо SAB='RXNORM' concepts
  that match наш usage list
- **Requires:** UMLS Terminology Services license (free, academic).
  Apply online, ~1 week approval.
- **Client owner:** new `knowledge_base/ingestion/rxnorm_loader.py`

### 13.5. ATC / DDD

- **Source:** WHO Collaborating Centre ([ATC](https://www.whocc.no/atc_ddd_index/))
- **Format:** manual lookup або commercial subscription для bulk
- **Update cadence:** annual (January)
- **Scope for MVP:** manual table для drugs in our Regimens.
  Дуже мало — ~15-20 codes. **Не hostim full table** — commercial
  redistribution потребує license.
- **Ingestion:** manual курування, one YAML file, переглядається щороку
- **Attribution:** "ATC/DDD: WHO Collaborating Centre for Drug Statistics
  Methodology"

### 13.6. CTCAE v5.0

- **Source:** NCI ([CTCAE](https://ctep.cancer.gov/protocolDevelopment/electronic_applications/ctc.htm))
- **Format:** Excel + PDF, public domain
- **Update cadence:** CTCAE v5.0 (2017) stable. CTCAE v6.0 in progress — monitor.
- **Scope:** повний (всі ~800 AE, кожен з grade 1-5 criteria)
- **Structure:**
  ```yaml
  # knowledge_base/hosted/ctcae/v5.0/grading.yaml
  adverse_events:
    - code: "CTCAE.10005329"
      term: "Anemia"
      moocd_category: "Blood and lymphatic system disorders"
      grades:
        "1": "Hemoglobin (Hgb) <LLN - 10.0 g/dL; <LLN - 100 g/L; <LLN - 6.2 mmol/L"
        "2": "Hgb <10.0 - 8.0 g/dL; <100 - 80 g/L; <6.2 - 4.9 mmol/L"
        "3": "Hgb <8.0 g/dL; <80 g/L; <4.9 mmol/L; transfusion indicated"
        "4": "Life-threatening consequences; urgent intervention indicated"
        "5": "Death"
  ```
- **Ingestion:** one-time download Excel, Python script → YAML. 
- **Client owner:** none (static)

---

## 14. Hosted: CIViC (biomarker KB)

- **Source:** Washington University ([CIViC](https://civicdb.org/))
- **API:** GraphQL + REST available. Bulk download TSV.
- **License:** CC0 (no attribution required but ми вказуємо)
- **Update cadence:** daily updates; weekly re-fetch is reasonable
- **Scope for MVP:** full variant-evidence-assertion table. Малий (~10K
  evidence items)
- **Ingestion flow:**
  1. Weekly cron: download CIViC bulk TSV (`nightly-ClinicalEvidenceSummaries.tsv`)
  2. Python loader → YAML в `knowledge_base/hosted/civic/<date>/evidence.yaml`
  3. Diff vs previous — count new, changed, retracted entries
  4. Clinical reviewer signoff якщо > 50 changes або будь-які retracted
     entries впливають на active Indication.biomarker_requirements
  5. Promote: `current` symlink на нову дату
- **Structure:**
  ```yaml
  evidence_items:
    - id: 1234
      variant: {gene: "BRAF", variant: "V600E", hgvs_protein: "..."}
      disease: {name: "Melanoma", doid: "1909"}
      drugs: ["Vemurafenib"]
      evidence_level: "A"
      clinical_significance: "Sensitivity/Response"
      pmids: [22735384]
  ```
- **Client owner:** new `knowledge_base/ingestion/civic_loader.py`

---

## 15. Hosted: Ukraine-local (МОЗ, НСЗУ, Держреєстр ЛЗ)

Це **найважчий і найважливіший** блок — немає API, формати неоднорідні,
вимагає людської верифікації. Без цього OpenOnco не дає value для
України.

### 15.1. МОЗ — Уніфіковані клінічні протоколи

- **Source:** [moz.gov.ua](https://moz.gov.ua/) + [dec.gov.ua](https://www.dec.gov.ua/)
- **Format:** PDF (accompanying orders), часто скан-копії
- **Update cadence:** irregular. Major protocols оновлюються раз на
  2-5 років
- **Discovery:** manual monitoring — subscribe to moz.gov.ua updates,
  track Наказ номер для певних нозологій
- **Ingestion flow:**
  1. Identify new or updated protocol (manual trigger)
  2. Download PDF → `knowledge_base/hosted/ukraine/moz_protocols/<slug>/<date>/source.pdf`
  3. OCR якщо скан (tesseract + Ukrainian language pack)
  4. LLM-assisted extraction (allowed per CHARTER §8.1 — "витяг
     структурованих даних з clinical documents") → `extracted.yaml`
  5. **Obligatory** clinical reviewer verification — порівняти
     extracted.yaml з PDF, підписати в `review.yaml`
  6. Only after review signoff — Indications що посилаються на цей
     протокол можуть merge
- **Structure after extraction:**
  ```yaml
  # knowledge_base/hosted/ukraine/moz_protocols/lymphoma-2024/extracted.yaml
  protocol_id: "MOZ-UA-LYMPH-2024"
  title: "Уніфікований клінічний протокол: Лімфоми"
  order_number: "Наказ МОЗ України № 1234 від 2024-XX-XX"
  effective_date: "2024-XX-XX"
  superseded_protocol: "MOZ-UA-LYMPH-2019"
  sections:
    - section_id: "first_line"
      title: "Лікування першої лінії"
      recommendations:
        - text: "..."  # literal парафраз з PDF
          source_page: 23
          level_of_evidence: "..."
  raw_pdf_path: "source.pdf"
  extracted_by: "claude-code + manual verify"
  extracted_at: "2026-04-25"
  ```
- **Client owner:** new `knowledge_base/ingestion/moz_extractor.py`
  (PDF + OCR + LLM extraction pipeline)

### 15.2. НСЗУ формуляр

- **Source:** [nszu.gov.ua](https://nszu.gov.ua/) — перелік реімбурсованих препаратів
- **Format:** PDF / Excel таблиці
- **Update cadence:** ~monthly (але зміни часто маргінальні)
- **Ingestion flow:**
  1. Monthly fetch of current перелік
  2. Parser Excel → YAML
  3. Diff vs previous — які препарати додано/видалено з реімбурсації
  4. Alerts для клінічних рев'юерів якщо препарат у active Regimen
     змінив статус
- **Structure:**
  ```yaml
  # knowledge_base/hosted/ukraine/nszu_formulary/2026-04/reimbursed.yaml
  effective_date: "2026-04-01"
  source_url: "https://..."
  drugs:
    - mnn: "Rituximab"
      mnn_ua: "Ритуксимаб"
      atc: "L01FA01"
      indications_reimbursed:
        - "Дифузна великоклітинна В-клітинна лімфома"
        - "Фолікулярна лімфома"
      conditions: "У рамках Національного переліку..."
      source_row: "№ 142 в переліку"
  ```
- **Client owner:** new `knowledge_base/ingestion/nszu_loader.py`

### 15.3. Державний реєстр лікарських засобів

- **Source:** [drlz.com.ua](https://www.drlz.com.ua/) (State Expert Center of МОЗ)
- **Purpose:** підтвердження що препарат зареєстрований в Україні і
  не знятий з реєстрації
- **Format:** web search UI, no bulk download
- **Ingestion:** per-drug lookup при створенні Drug entity. Не bulk.
- **Flow:**
  1. Клінічний рев'юер при створенні нового Drug entity вводить
     МНН + торгову назву
  2. Скрипт робить query до drlz.com.ua, екстрактить результат
  3. Зберігає в Drug entity: `ukraine_registration.registered: true`,
     `registration_number`, `registered_on`, `last_verified`
  4. Quarterly re-verification — script iterates over all Drugs,
     checks current status. Якщо status змінився — alert.
- **Client owner:** new `knowledge_base/ingestion/drlz_lookup.py`

---

### 15a. Architectural invariant — UA-availability is annotation, never filter

> **Status:** PROPOSAL (2026-04-26). Aligns with CHARTER §2 (free public
> resource for evidence-based oncology) and the directive recorded in
> auto-memory `feedback_efficacy_over_registration.md`:
> «важливо — ефективність а не реєстрованість».

**Rule.** Whether a drug is registered in Ukraine, reimbursed by НСЗУ,
or both, MUST NOT influence which `Indication` / `Regimen` / track the
engine selects. UA-availability fields (`Drug.regulatory_status.ukraine_registration`,
`Drug.regulatory_status.reimbursement_nszu`) are **render-time advisory
metadata only**. The engine's selection signal is efficacy + evidence
tier + patient eligibility, full stop.

**Why.** OpenOnco surfaces the best clinical option per current
evidence even when in-country access is constrained. Hiding a
guideline-endorsed therapy because it is not reimbursed would distort
recommendations toward locally-available, often suboptimal alternatives
— defeating the project's purpose. The doctor, not the engine, decides
how to navigate the funding pathway (charitable foundation, employer
insurance, off-label import, international referral).

**Source-precedence corollary.** МОЗ Ukraine clinical protocols
(`SRC-MOZ-UA-*`) are a **national floor**, not a substitute for
Tier-1 international guidelines (NCCN, ESMO, ASCO, EAU). Where МОЗ
prescribes a less-aggressive regimen than current Tier-1/2 evidence
endorses, OpenOnco follows the international evidence and cites МОЗ
as confirmatory / national-floor context — never the other way around.

**Mechanisation.**

1. **`Source.precedence_policy` field** (`leading | confirmatory |
   national_floor_only | secondary_evidence_base`). All `SRC-MOZ-UA-*`
   sources MUST be annotated `national_floor_only`. The validator
   blocks a default-`Indication` whose only sources are
   `national_floor_only` when a peer `Indication` for the same scenario
   has at least one Tier-1/2 source.

2. **Validator gate** — `_check_source_precedence_policy` in
   `knowledge_base/validation/loader.py` runs in Pass 3 alongside
   RedFlag contract checks.

3. **Architectural-invariant test** —
   `tests/test_plan_invariant_ua_availability.py` parametrises four
   real patient fixtures, monkeypatches every `Drug` to
   `registered: false, reimbursed_nszu: false`, and asserts the
   engine's clinical-decision signature (default + alternative
   indication, tracks, regimen ids) is identical to the control run.
   This is the gate for all UA-ingestion work below.

**Anti-pattern (forbidden).**

- Engine-side filter that hides "not-reimbursed" recommendations.
- Ranking signal that downgrades a regimen because its drug is
  unregistered.
- Track-switching logic that prefers a less-effective in-country
  alternative when a better evidence-supported option exists.

**Permitted (advisory only).**

- Render-side **Access Matrix** that, for each surfaced track, shows
  the registration / reimbursement / cost-orientation status with
  pathway hints (per Phase B-D of
  `docs/plans/ua_ingestion_and_alternatives_2026-04-26.md`).
- A separate **`ExperimentalOption`** track exposing relevant
  ClinicalTrials.gov / EU CTR studies as additional alternatives —
  appended, never replacing the evidence-driven default.

---

## 16. Referenced: Live API clients

Короткий playbook per source. Full interface per §12.2.

### 16.1. ClinicalTrials.gov

- **Endpoint:** `https://clinicaltrials.gov/api/v2/studies`
- **Rate limit:** 50 req/min per IP (soft)
- **Client:** `clinicaltrials_client.py` (existing, у top-level). Refactor під `SourceClient` interface.
- **Typical queries:**
  - Filter by disease + status (recruiting/active) + country (Ukraine, EU)
  - Fetch by NCT ID for citation
- **Cache TTL:** 24 hours
- **Quota handling:** exponential backoff; fall back to stale cache on
  429/503

### 16.2. PubMed / E-utilities

- **Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Rate limit:** 3 req/sec without API key, 10 req/sec з key
- **Client:** `pubmed_client.py` (existing). Refactor під `SourceClient`.
- **Typical queries:**
  - PMID → abstract + metadata
  - Search по disease + keywords для evidence discovery
- **Cache TTL:** 7 days for individual PMIDs (abstracts stable),
  24h for search queries
- **API key:** apply for free NCBI key — збільшує rate limit

### 16.3. DailyMed / openFDA

- **DailyMed Endpoint:** `https://dailymed.nlm.nih.gov/dailymed/services/v2/`
- **openFDA Endpoint:** `https://api.fda.gov/drug/label.json`
- **Rate limit:** openFDA — 240 req/min without key, 120K/day з key
- **Client:** **new** `dailymed_client.py` + `openfda_client.py`
- **Typical queries:**
  - SETID → full drug label
  - Drug name → search labels
- **Cache TTL:** 7 days (labels оновлюються рідко)

### 16.4. OncoKB

- **Endpoint:** `https://www.oncokb.org/api/v1`
- **Rate limit:** academic tier — gentle; token required
- **Client:** **new** `oncokb_client.py`
- **Auth:** API token from free academic registration
- **Typical queries:**
  - Gene + variant → therapeutic implications
- **Cache TTL:** 7 days
- **⚠️ License gate:** якщо OpenOnco переходить у commercial — replace
  з academic subscription, або replace data source

### 16.5. ClinVar, gnomAD

- **ClinVar endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
  (same E-utilities as PubMed, db=clinvar)
- **gnomAD endpoint:** `https://gnomad.broadinstitute.org/api` (GraphQL)
- **Rate limit:** gentle, no hard limits
- **Client:** **new** `clinvar_client.py` + `gnomad_client.py`
- **Typical queries:**
  - Variant ID → clinical significance (ClinVar)
  - Variant → population allele frequency (gnomAD)
- **Cache TTL:** 30 days

---

## 17. Tooling inventory

### Existing (можна використовувати як є / з refactor):
- `clinicaltrials_client.py` (top-level) — рефактор під `SourceClient`
- `pubmed_client.py` (top-level) — рефактор під `SourceClient`

### To build (seed для HCV-MZL):

| Модуль | Призначення | Пріоритет |
|---|---|---|
| `knowledge_base/clients/base.py` | `SourceClient` інтерфейс, `TTLCache` | P0 — blocks all else |
| `knowledge_base/clients/dailymed_client.py` | DailyMed label lookup | P1 |
| `knowledge_base/clients/openfda_client.py` | openFDA drug labels | P1 |
| `knowledge_base/clients/oncokb_client.py` | OncoKB academic API | P2 |
| `knowledge_base/clients/clinvar_client.py` | ClinVar via E-utilities | P2 |
| `knowledge_base/clients/gnomad_client.py` | gnomAD GraphQL | P3 |
| `knowledge_base/ingestion/civic_loader.py` | CIViC TSV → YAML | P1 |
| `knowledge_base/ingestion/icd_loader.py` | ICD-O-3.2 CSV → YAML | P1 |
| `knowledge_base/ingestion/loinc_loader.py` | LOINC subset loader | P1 |
| `knowledge_base/ingestion/rxnorm_loader.py` | RxNorm RRF → YAML | P2 |
| `knowledge_base/ingestion/ctcae_loader.py` | CTCAE Excel → YAML | P1 |
| `knowledge_base/ingestion/moz_extractor.py` | PDF → OCR → LLM → YAML | P0 — unique value |
| `knowledge_base/ingestion/nszu_loader.py` | НСЗУ Excel → YAML | P0 — unique value |
| `knowledge_base/ingestion/drlz_lookup.py` | per-drug Держреєстр check | P1 |
| `knowledge_base/validation/schema_validator.py` | Pydantic validation on load | P0 |
| `knowledge_base/validation/refint_checker.py` | referential integrity | P1 |

**Stack:**
- Python 3.11+, stdlib where possible
- `pydantic` for schema validation (new dependency, але дуже доречно)
- `httpx` for HTTP clients (better than stdlib `urllib` for async/retry)
- `pypdf` / `pdfplumber` для МОЗ PDFs
- `pytesseract` + Ukrainian language pack для OCR scans
- No heavy frameworks (no Django, no full ORMs — YAML + Pydantic поки
  достатньо)

---

## 18. Operational cadence

| Джерело | Cadence | Trigger | Owner |
|---|---|---|---|
| ICD-O-3.2 | yearly re-check | manual (WHO news) | clinical lead |
| LOINC | 2x yearly (Jun, Dec) | scheduled | eng + clinical lead |
| RxNorm | monthly | scheduled cron | eng |
| ATC | yearly (January) | scheduled | clinical lead (manual curation) |
| CTCAE | yearly re-check (v6.0 pending) | manual (NCI news) | clinical lead |
| CIViC | weekly | scheduled cron | eng, reviewed by clinical lead if >50 changes |
| МОЗ protocols | ad-hoc on new Наказ | manual discovery | clinical lead |
| НСЗУ формуляр | monthly | scheduled cron | eng + pharmacist review |
| Держреєстр ЛЗ | quarterly per-drug | scheduled | eng alert → clinical lead |
| CT.gov, PubMed, DailyMed, openFDA, OncoKB, ClinVar, gnomAD | live, cache TTL per §12.3 | on-demand at rule eval | rule engine |

CI (GitHub Actions) — окремий workflow `ingestion-scheduled.yml`:
- daily: CIViC fetch
- monthly: RxNorm, НСЗУ
- weekly: health check all referenced APIs
- quarterly: Держреєстр ЛЗ re-verification loop

Job output — PR with diff + scheduled re-verification, реви клінічний
co-lead затверджує.

---

## 19. Failure modes і SLA

| Сценарій | Detection | Mitigation | Customer impact |
|---|---|---|---|
| CT.gov API down | health probe fail | serve stale cache + warning | plan generated, but freshness warning на trial citations |
| PubMed rate limited (429) | HTTP 429 | backoff, fall back to cache | same as above |
| OncoKB token expired | 401 response | skip OncoKB, continue without biomarker KB | biomarker evidence citations зникають |
| МОЗ PDF format changed | parser exception on ingestion | manual extraction fallback, alert clinical lead | new МОЗ protocol не потрапляє в KB поки не виправлено |
| CIViC retracted evidence | diff job detects | alert clinical lead before promote; hold until review | no impact on live system поки review не проведено |
| Code system version change (ICD, LOINC) | new version publication | scheduled re-check, clinical lead signoff | zero impact during review; switch symlink коли готово |
| DailyMed returns modified drug label (recall) | daily poll of hashed labels | emergency pathway (CHARTER §6.2) | Indication уточнюється у 7 днів; inline warning в плані негайно |

**SLA targets (MVP):**
- Plan generation success rate: > 99% (з warnings коли potrzeby)
- Zero "plan unavailable" через external API: hard target
- Time from МОЗ protocol release to KB ingestion: < 30 days
- Time from FDA safety recall to KB reflection: < 7 days (emergency pathway)

---

## 20. Checklist: підключення нового hosted-джерела

Для кожного нового hosted-джерела (по §8 + додатково):

- [ ] License розібрана (Part A §2)
- [ ] hosting mode обраний (Part A §1); якщо `hosted` — обґрунтування H1-H5
- [ ] Структура директорії створена за §12.1
- [ ] Ingestion script написаний (`knowledge_base/ingestion/<source>_loader.py`)
- [ ] Schema validator написаний (Pydantic model)
- [ ] Source entity створений з усіма license/attribution/legal_review полями (Part A §3)
- [ ] First fetch + diff vs null baseline + clinical review пройдений
- [ ] CI job для scheduled re-fetch налаштований
- [ ] Operational cadence entry додано в §18
- [ ] Failure mode додано в §19
- [ ] UI attribution text затверджено (якщо license вимагає)

---

## 21. Що виходить за scope Part B (в Part C/D)

Нижчезгадане буде покрито у наступних частинах документа, не тут:

- **Part C — Conflict & precedence rules:** коли NCCN і ESMO
  розходяться по preferred regimen, що бачить лікар? Який Indication
  стає default? Tier hierarchy для tie-breaking?
- **Part D — Freshness TTL & re-ingestion cadence deep dive:** formal
  SLA per-source, alerting thresholds, когерентність snapshot між
  джерелами (наприклад, коли rule engine оцінює Indication, всі його
  sources мають бути з одного coherent time window?)

---

# Part C — Conflict & Precedence Rules

## 22. Scope і цілі Part C

Part A сказала **яких** джерел ми слухаємо. Part B — **як** їх читаємо.
Part C відповідає: коли ці джерела **не згодні між собою**, як будується
фінальний Indication / Contraindication / RedFlag, і що бачить лікар?

Це не інженерне питання — це клінічне редакційне рішення. Тому Part C
має статус **"рекомендації для клінічних рев'юерів"**, а не executable
rule. Rule engine не робить automated conflict resolution — конфлікти
вирішуються людьми на етапі редагування `content/`.

---

## 23. Принципи

### 23.1. Ніколи не automated resolution

Rule engine **не вибирає** між конфліктуючими джерелами. Усі Indication,
Regimen, Contraindication, RedFlag — написані вручну клінічним рев'юером,
з явним обранням позиції (або відображенням controversy). Це повторює
CHARTER §8.3: LLM/engine не є клінічним decision-maker.

Engine отримує **вже вирішений** Indication + опційно `known_controversies`
блок, який ясно показує альтернативні позиції.

### 23.2. Дві плани за замовчуванням (CHARTER §2)

Проєкт завжди видає **два плани** — standard і aggressive. Це частково
вбудований механізм роботи з розбіжністю: коли два шанованих джерела
пропонують різні підходи, ми часто маємо "standard = ESMO default +
Ukraine availability" і "aggressive = NCCN alternate + recent RCT".

Розбіжність між standard і aggressive — **не конфлікт**, а design output.
Конфлікт — це коли ВСЕРЕДИНІ standard (або aggressive) різні джерела
кажуть різне.

### 23.3. Presence не precedence

Якщо джерело А рекомендує X, а джерело Б — Y, **обидва зберігаються**
(див. CLINICAL_CONTENT_STANDARDS §5.3). Вибір default для Indication —
клінічний рев'юер. Але альтернативна позиція відображається в UI
завжди, з посиланнями на джерела.

Це реалізується через `Indication.known_controversies`:

```yaml
# knowledge_base/hosted/content/indications/ind_hcv_mzl_1l_standard.yaml
id: "IND-HCV-MZL-1L-STANDARD"
disease_id: "DIS-HCV-MZL"
line_of_therapy: 1
recommended_regimen: "REG-DAA-ANTIVIRAL-ONLY"
evidence_level: "Moderate"
strength_of_recommendation: "Strong"

sources:
  - source_id: "SRC-ESMO-MZL-2024"
    position: "supports"
    relevant_quote_paraphrase: "Antiviral-first for HCV-associated MZL..."
  - source_id: "SRC-NCCN-BCELL-2025"
    position: "supports"
    relevant_quote_paraphrase: "DAA-based antiviral therapy preferred for HCV+..."
  - source_id: "SRC-MOZ-UA-LYMPH-2024"
    position: "supports"

known_controversies:
  - topic: "Role of immediate rituximab if viral load clearance slow"
    positions:
      - position: "Monitor for 6 months post-DAA before adding rituximab"
        sources: ["SRC-ESMO-MZL-2024"]
      - position: "Add rituximab concurrent з DAA if bulky disease"
        sources: ["SRC-NCCN-BCELL-2025"]
        evidence_note: "Based on subgroup analysis; no direct comparison"
    our_default: "Monitor for 6 months"
    rationale: "ESMO position + aligned with МОЗ 2024 protocol; rituximab reserved for non-response or aggressive phenotype"
```

---

## 24. Tier hierarchy для клінічних рев'юерів

Коли рев'юер пише новий Indication і бачить конфлікт між джерелами,
цей список **впливає, але не вирішує**. Рев'юер документує рішення
у `Indication.rationale`.

### 24.1. Порядок ваги (приблизний)

| # | Tier | Джерела | Коли переважає |
|---|---|---|---|
| 1 | **Ukrainian regulatory** | МОЗ протоколи, НСЗУ формуляр, Держреєстр | Коли визначає **availability** і **reimbursement** — blocking constraint. Не клінічний зміст, а **що реально доступне пацієнту в Україні** |
| 2 | **International regulatory** | FDA, EMA labels | Approvals, contraindications, black box warnings — factual, not advisory |
| 3 | **Major international guidelines (current)** | NCCN, ESMO, ASCO, WHO | Default клінічні рекомендації. Тут найчастіше виникає конфлікт |
| 4 | **Recent high-quality RCT** (< 2 years) | Phase 3, в major journal, peer-reviewed | Може **перекривати guideline**, якщо guideline не встиг оновитись і RCT достатньо definitive |
| 5 | **Systematic reviews / meta-analyses** | Cochrane, NICE, інші | Supporting evidence |
| 6 | **Molecular KBs** | OncoKB, CIViC | Biomarker-specific нюанси |
| 7 | **Older / country-specific guidelines** | NCCN v.2020, BSH, EHA | Historical context; deprecated as primary |
| 8 | **Observational studies, single-arm trials** | phase 2, registries | Only when higher tiers silent |
| 9 | **Expert opinion, editorials** | | Only as color / rationale, never primary |

### 24.2. Особливі правила

**Правило 1 — Ukraine availability блокує рекомендацію.** Якщо препарат
не зареєстрований в Україні АБО не реімбурсований, схема не може
бути `default_regimen` для Ukraine deployment. Alternative path:
схема лишається в Indication як `alternative_regimen` з explicit
note "доступний в Україні за off-label import".

**Правило 2 — FDA/EMA black box трактується як абсолютне contraindication.**
Не гайдлайн це не перекриває. Якщо guideline рекомендує препарат, а
FDA black box warning relevant до стану пацієнта — black box trigger
спричиняє RedFlag і вибір alternative regimen.

**Правило 3 — Recent RCT can override older guideline.** Якщо RCT
published 2026, а NCCN останнє оновлення 2024, і RCT statistically
significant superiority — рев'юер **може** (не must) оновити default.
Обов'язково:
- RCT має бути Phase 3, peer-reviewed
- Sample size adequate для disease entity
- Primary endpoint clinically meaningful (OS > PFS > ORR для solid)
- Має pass обидва reviewer + one external consultation
- Позначити в UI що recommendation базується на "post-guideline RCT"
- Triggered re-review при наступному guideline update

**Правило 4 — Tier 1 (Ukrainian) не перекриває clinical evidence,
тільки доступність.** МОЗ протокол може бути outdated відносно NCCN/ESMO.
Якщо МОЗ рекомендує X, а NCCN 2025 — Y, клінічний рев'юер:
- Якщо Y доступний і реімбурсований в Україні → default Y з посиланням
  на обидва + зауваження "МОЗ протокол передує оновленню"
- Якщо Y недоступний → default X (МОЗ), alternative Y з expected
  availability note
- Ніколи не ігнорувати МОЗ тихо — пояснити рішення в rationale

**Правило 5 — Molecular KBs нижчі за guidelines, але вищі коли
guidelines мовчать.** Якщо NCCN рекомендує regimen без біомаркерного
refinement, а OncoKB / CIViC вказують що biomarker X передбачає
response на regimen Y — Y стає candidate для alternative path, не
override default.

### 24.3. Що таке "conflict" vs "refinement"

Не всі розбіжності — конфлікти.

| Ситуація | Тип | Дія |
|---|---|---|
| ESMO каже "R-CHOP 6 cycles", NCCN "R-CHOP 6-8" | **Refinement** | Наш Regimen специфікує "6 cycles, 8 only if bulky residual" з посиланням на обидва |
| ESMO каже "bendamustine+rituximab", NCCN "R-CHOP" | **Conflict** | `known_controversies`, рев'юер вибирає default |
| NCCN v.2024 vs NCCN v.2025 different | **Version update** | Older deprecated, newer active; не conflict |
| OncoKB Level 2A, CIViC Level B | **Agreement з різною номенклатурою** | Normalize evidence levels, не conflict |
| Single RCT contradicts meta-analysis | **Requires judgment** | Usually meta-analysis wins unless RCT is larger/better |

---

## 25. Workflow для рев'юера: що робити коли бачиш конфлікт

1. **Document both positions explicitly.** Не вибирати мовчки. Обидві
   позиції з посиланнями на Source entity.
2. **Check tier hierarchy (§24.1)** — який tier джерела на кожній
   стороні? Чи є obvious перевага?
3. **Check recency.** Старий NCCN (v.2020) vs новий ESMO (2024) —
   recency matters.
4. **Check sample size and study design.** Phase 3 n=800 vs phase 2 n=45 —
   не питання.
5. **Check Ukraine availability.** Може вирішити питання — недоступне
   автоматично не default.
6. **Якщо після §25.1-5 все ще unclear:** other Clinical Co-Leads
   discussion, за CHARTER §6.1. При потребі — external consultation.
7. **Document decision в `Indication.rationale`** з посиланням на
   reviewed conflict. Reviewer має record чому рішення прийнято, не
   тільки що.
8. **Flag for re-review** через 12 місяців або при наступному guideline
   update — що раніше.

---

## 26. UI patterns для відображення конфліктів

### 26.1. Inline indicator

Для кожного Indication / Contraindication, що має `known_controversies`:
- Мала іконка ⚠️ "є контроверсія" поряд з regimen name
- Click → розгортається: "Наш вибір: X. Альтернативна позиція: Y (джерело Z).
  Раціонал: ..."

### 26.2. Sources breakdown

Завжди клікабельна "Джерела" секція внизу плану:
- Each Source з tier, date accessed, URL
- Tier color-coded (Ukrainian regulatory — blue, Guidelines — green,
  RCTs — orange, Molecular — purple)
- Controversy explicitly marked — "2 of 3 sources support X, 1 supports Y"

### 26.3. "Why not Y?" pattern

Для кожного плану, якщо є rejected alternative, одноклікове пояснення:
"Чому не R-CHOP? — Агресивніший схема, для цього пацієнта з HCV-MZL
спочатку DAA. Див. ESMO 2024. Якщо non-response через 6 місяців —
переоцінка."

Це підтримує клінічну прозорість і одночасно служить materiałем для
клінічного навчання.

---

## 27. Версіонування і stale positions

Правило: **позиція на основі застарілого джерела автоматично flagged**.

Якщо `Indication.sources` посилається на Source entity з
`currency_status: superseded`, CI validator:
- Emit warning на PR: "Indication X посилається на superseded NCCN v.2024,
  replacement: NCCN v.2025. Re-review required."
- Не блокує merge (могло бути deliberate "снимок для audit"), але
  позначає в `_stale_review` list

Quarterly audit (CLINICAL_CONTENT_STANDARDS §9.1) iterates `_stale_review`
і переглядає кожен Indication.

---

# Part D — Freshness TTL & Re-ingestion Cadence

## 28. Scope Part D

Part B намітила TTL у §12.3 коротко. Part D — детальна таблиця per
source, alerting thresholds, concept "coherent snapshot" (когерентний
знімок у часі всіх джерел на момент рендерингу плану), emergency
pathways.

---

## 29. Per-source TTL і cadence (повна таблиця)

### 29.1. Hosted — цикл re-ingestion

| Джерело | Re-ingest cadence | Detection механізм | Alert threshold | Owner |
|---|---|---|---|---|
| ICD-O-3.2 | Yearly | Manual check WHO news | N/A — stable | Clinical lead |
| LOINC | 2x yearly (June, December) | Release schedule | 60 днів after expected release — alert | Engineering + Clinical |
| RxNorm | Monthly (1st Monday) | Scheduled cron | Cron fail > 2 consecutive — page on-call | Engineering |
| ATC | Yearly (January) | Manual | 90 днів after expected — alert | Clinical lead |
| CTCAE | Yearly re-check | Manual NCI announcements | v6.0 release — immediate review | Clinical lead |
| CIViC | Weekly | Scheduled cron | > 50 diff items or retracted items hitting active Indication — clinical lead signoff required before promote | Engineering + Clinical |
| МОЗ protocols | Ad-hoc on new Наказ | Manual discovery (moz.gov.ua subscription) | New relevant protocol → <30 day ingestion target | Clinical lead |
| НСЗУ формуляр | Monthly | Scheduled cron | Drug status change для active Regimen → immediate alert | Engineering + pharmacist |
| Держреєстр ЛЗ | Quarterly per-drug | Scheduled | Reg status change → immediate alert | Engineering → Clinical lead |

### 29.2. Referenced — cache TTL

| Джерело | Cache TTL (default) | Cache scope | Bust triggers |
|---|---|---|---|
| ClinicalTrials.gov | 24 hours | Query result | Explicit admin bust; Source.last_verified update |
| PubMed (PMID fetch) | 7 days | Per PMID | Rare — abstracts stable |
| PubMed (search) | 24 hours | Query hash | Query parameter change |
| DailyMed (SETID fetch) | 7 days | Per SETID | Recall event (manual bust) |
| openFDA (label search) | 24 hours | Query hash | |
| OncoKB | 7 days | Gene+variant query | API response change |
| ClinVar | 30 days | Per variant ID | |
| gnomAD | 90 days | Per variant | Very stable |

---

## 30. Концепція "coherent snapshot"

Коли план генерується **2026-05-15**, він посилається на:
- CT.gov записи з cache від 2026-05-14
- PubMed abstracts від 2026-05-08
- Наш Indication зі `last_reviewed: 2026-03-01`
- NCCN (referenced) останнього fetch 2026-04-20
- МОЗ протокол 2024

Це **некогерентно у часі** — різні "моменти" знань.

### 30.1. Що ми гарантуємо

**Sort of "coherent":**
- Для кожного Indication / Regimen / Contraindication — усі його `sources`
  мають `last_verified` у межах останніх 6 місяців (CLINICAL_CONTENT §9.1)
- Якщо хоч одне джерело має `currency_status: superseded` — warning

**Не гарантуємо:**
- Що cached CT.gov запит від 2026-05-14 і PubMed від 2026-05-08 —
  "той самий state of the world". Це practical impossibility.

### 30.2. Що відображаємо в UI

У footer кожного плану:
```
План згенеровано: 2026-05-15 14:23 UTC
Knowledge base snapshot:
  - Наш клінічний контент: останнє оновлення 2026-04-12
  - CIViC: 2026-05-13
  - LOINC: 2.76 (2025-12)
  - МОЗ протокол Лімфоми: 2024 (останнє)
Live-queried при генерації:
  - ClinicalTrials.gov (fetched 2026-05-15)
  - PubMed (fetched 2026-05-15)
  - DailyMed (fetched 2026-05-15)
```

Лікар бачить точно з чого план складено.

---

## 31. Emergency pathway

CHARTER §6.2 описує emergency update process. Part D конкретизує
triggers і поведінку системи.

### 31.1. Emergency triggers

| Подія | Source | Auto-detected? | Target timeline |
|---|---|---|---|
| FDA safety alert (black box added / removed) | openFDA feed | Так — daily poll hash of FDA drug labels | < 24 години: alert; < 7 днів: fully reflected |
| Drug recall | openFDA recalls endpoint | Так | < 24 години: alert + emergency Contraindication added |
| МОЗ Наказ про зняття препарату з реєстрації | Manual monitoring | Ні | < 48 годин від discovery |
| CIViC retraction of evidence hitting active Indication | CIViC diff | Так | Immediate alert; pause Indication merge поки не reviewed |
| Major guideline update announced | Manual | Ні | 30 days до ingestion target |
| Critical RCT published з clinically significant superiority | Manual | Ні | Рев'юери обговорюють включення |

### 31.2. Emergency workflow

1. **Detection** — або automatic (openFDA diff, CIViC diff) або manual
   (клінічний лід помітив)
2. **Immediate action** (перші 24h):
   - Тимчасовий inline warning додається до relevant Indications:
     "Отримано safety сигнал, рекомендація переглядається. Дата:
     2026-05-15"
   - Clinical co-lead + додатковий reviewer приймають рішення
3. **Structured update** (перші 7 днів):
   - Contraindication entity створюється або оновлюється
   - Indication.known_controversies можливо додається
   - Source з `emergency_update: true` flag
4. **Full review** (протягом 14 днів):
   - Standard two-reviewer workflow для permanent change
   - Update changelog з "emergency update" label

Зовнішній communication — для critical safety change (drug recall) —
push notification клінікам, які згенерували план з affected drug у
останні N місяців (якщо ми маємо opt-in реєстрацію планів).

---

## 32. Audit снапшот (для compliance)

Кожний згенерований план **зберігає immutable snapshot**:
- `plan_id`, `generated_at`
- `knowledge_base_state`:
  - hashes active version кожного hosted source
  - timestamps кешованих referenced responses
  - Indication, Regimen, Algorithm id + їх version
- `patient_input_hash` (no PHI, just shape validation)

Це дозволяє:
- Retrospective audit: "на підставі якого саме knowledge state цей план
  був згенерований 2026-05-15"
- Debugging: reproduce plan точно як видано
- Regulatory inquiry response

Snapshot зберігається окремо від плану (часто PII-free) і має
`retention: indefinite` у відповідності до CHARTER §10.2.

---

## 33. SLA summary (operational targets)

| Метрика | Target | Measurement |
|---|---|---|
| План generation success rate | > 99% | через monthly rolling |
| "Plan unavailable" через API fail | 0 | hard — should never happen (graceful degrade) |
| Stale warning appearance rate | < 20% of plans | daily |
| МОЗ protocol → KB ingestion | < 30 днів | per-protocol tracking |
| FDA safety → inline warning | < 24 години | per-event |
| FDA safety → structured Contraindication | < 7 днів | per-event |
| CIViC diff → review | < 7 днів | per-release |
| Quarterly audit completion | 100% entries with `last_reviewed < 180 днів` | quarterly |

---

## 34. Checklist: ship Part A+B+C+D to production

Перед тим як цей spec перейде з draft у "active" статус:

- [ ] Всі Clinical Co-Leads прочитали і підписали
- [ ] Юридичний консультант підписав Part A §2 + §6 red flags
- [ ] `knowledge_base/` структуру створено (порожні директорії з README)
- [ ] Pydantic моделі для всіх hosted entity types написані
- [ ] Seed HCV-MZL reference case повністю ingested за Part B §7.1
- [ ] Rule engine може згенерувати два плани для HCV-MZL test patient
- [ ] CI workflows: schema validation, referential integrity, license
  compliance, scheduled re-ingest
- [ ] UI prototype показує snapshot section (§30.2) і controversy
  indicator (§26.1)
- [ ] Emergency pathway протестовано на dry-run drug recall scenario
- [ ] Audit snapshot (§32) зберігається для кожного generation test
- [ ] Документація перекладена ключовими секціями на EN (для international
  contributors) — або explicit policy що основна робоча мова — UA

---

## 35. Зміни у цьому документі

| Версія | Дата | Зміни |
|---|---|---|
| v0.1 | 2026-04-24 | Part A — licensing/hosting matrix |
| v0.2 | 2026-04-24 | Part A revision — `referenced` як default, hosted criteria H1-H5 |
| v0.3 | 2026-04-24 | Part B — per-source ingestion playbook |
| v0.4 | 2026-04-24 | Part C — conflict & precedence rules |
| v0.5 | 2026-04-24 | Part D — freshness TTL & re-ingestion cadence deep dive |
