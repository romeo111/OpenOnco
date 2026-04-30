# knowledge_base/

🇬🇧 English (below) · 🇺🇦 [Українська](#-українська)

The OpenOnco rule engine and knowledge base. Patient profile in
(FHIR R4 / mCODE compatible) → **two alternative treatment plans**
(standard + aggressive), side by side, every recommendation cited.
LLMs do **not** make clinical decisions — clinical logic runs in a
declarative rule engine reading versioned YAML
([CHARTER §8.3](../specs/CHARTER.md)).

Live at **[openonco.info](https://openonco.info)** (EN default,
UA mirror at [`/ukr/`](https://openonco.info/ukr/)).
Live KB metrics, per-disease coverage matrix, sign-off ratio:
**[openonco.info/capabilities](https://openonco.info/capabilities.html)**.

## Layout

```
knowledge_base/
├── schemas/         # Pydantic entity models (Disease, Drug, Indication, …)
├── engine/          # rule engine, MDT orchestrator, render, persistence
├── validation/      # YAML loader + schema + referential-integrity checker
├── clients/         # live-API clients (CT.gov, PubMed, DailyMed, openFDA, …)
├── ingestion/       # loaders for hosted sources (CIViC, CTCAE, ICD-O-3, МОЗ, НСЗУ, …)
├── hosted/
│   ├── content/     # YAML knowledge base — clinical content
│   ├── code_systems/, civic/, ctcae/   # vendored snapshots
│   └── audit/       # signoffs.jsonl — clinical sign-off log
└── stats.py         # KB stats for the public capabilities page
```

## What's implemented

- **Rule engine** — `generate_plan()` and `generate_diagnostic_brief()`
  produce a versioned `PlanResult` from a patient profile.
- **MDT orchestrator** — role activation, Open Questions, decision-
  provenance graph for audit-grade explanation
  ([`MDT_ORCHESTRATOR_SPEC.md`](../specs/MDT_ORCHESTRATOR_SPEC.md),
  [`DIAGNOSTIC_MDT_SPEC.md`](../specs/DIAGNOSTIC_MDT_SPEC.md)).
- **Two-track plans** — standard + aggressive side-by-side
  ([CHARTER §15.2 C6](../specs/CHARTER.md) anti-automation-bias).
- **CIViC actionability** (CC0) — fusion-aware variant matcher,
  ESCAT-tier rendering, monthly snapshot CI refresh.
- **Three-layer citation guard** — loader-level SRC-* referential
  integrity, background citation-verifier, render-time strip-or-fail.
- **Bilingual render** — Plan / Brief HTML in UA and EN; UI labels
  + KB names + free-text prose all locale-aware.
- **Pre-biopsy mode** ([CHARTER §15.2 C7](../specs/CHARTER.md) hard rule)
  — engine refuses to emit a treatment Plan without histology / disease
  ID; emits a `DiagnosticPlan` with workup brief instead.
- **Live API clients** — ClinicalTrials.gov v2, PubMed, DailyMed, openFDA.
  Per-source rate-limit + TTL-cache.
- **Patient mode** — separate render path with plain-language drug /
  ICD glossing, "ask your doctor" prompts, technical-ID stripping.
- **Per-disease lazy loading** — engine bundle is a core zip + per-
  disease zips; the `/try.html` Pyodide engine fetches on demand.

## Run the validator

```bash
pip install -e .
python -m knowledge_base.validation.loader knowledge_base/hosted/content
```

Lists all entities, validates each against its schema, checks every
referenced ID, and runs contract validators (e.g. every clinical claim
cites a Source).

## Generate a Plan from a profile

```python
from pathlib import Path
from knowledge_base.engine import (
    generate_plan, generate_diagnostic_brief, is_diagnostic_profile,
    orchestrate_mdt, render_plan_html, render_diagnostic_brief_html,
)

KB = Path("knowledge_base/hosted/content")
patient = {...}  # FHIR R4 / mCODE-shaped dict

if is_diagnostic_profile(patient):
    result = generate_diagnostic_brief(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_diagnostic_brief_html(result, mdt=mdt, target_lang="en")
else:
    result = generate_plan(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_plan_html(result, mdt=mdt, target_lang="en")
```

The same engine ships in-browser via Pyodide — see
[openonco.info/try.html](https://openonco.info/try.html).

## Adding a new entity

1. Read [`KNOWLEDGE_SCHEMA_SPECIFICATION.md`](../specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md)
   for the canonical entity definition.
2. Write YAML under the appropriate `hosted/content/<type>/` directory.
3. Run the validator.
4. New source → add a Source YAML with full license / hosting metadata
   per [`SOURCE_INGESTION_SPEC.md`](../specs/SOURCE_INGESTION_SPEC.md).
5. Clinical content (Indication / Regimen / RedFlag /
   Contraindication / SupportiveCare) stays STUB until **two of three
   Clinical Co-Leads** approve via the signoff log
   ([CHARTER §6.1](../specs/CHARTER.md)) — never set
   `reviewed: true` yourself.

## Schema conventions

- IDs: prefix + upper-case, e.g. `DIS-HCV-MZL`, `DRUG-RITUXIMAB`,
  `BMA-EGFR-L858R-OSIMERTINIB`.
- Citations: every clinical claim references a Source via
  `source_id`, never inline URL.
- Names: `names: {ukrainian, english, preferred, synonyms: [...]}`.
  Render picks based on `target_lang`.
- `model_config = ConfigDict(extra="allow")` on every entity so adding
  fields in YAML doesn't break schema; pin specific fields as required
  when stable.

## Contributing via TaskTorrent

Idle capacity in Claude Code, Codex, Cursor, or ChatGPT? Take a
structured chunk of work from the queue and open a PR — full guide at
[`docs/contributing/CONTRIBUTOR_QUICKSTART.md`](../docs/contributing/CONTRIBUTOR_QUICKSTART.md)
or the public landing page
[openonco.info/contribute.html](https://openonco.info/contribute.html).

---

## 🇺🇦 Українська

Рушій правил і база знань OpenOnco. Профіль пацієнта (сумісний з
FHIR R4 / mCODE) → **два альтернативні плани лікування** (стандартний
і інтенсивніший) поряд, з повним цитуванням джерел. LLM **не**
приймають клінічних рішень — клінічна логіка працює в декларативному
рушії правил над версіонованим YAML
([CHARTER §8.3](../specs/CHARTER.md)).

Живий сайт: **[openonco.info](https://openonco.info)** (EN за
замовчуванням, UA-дзеркало на [`/ukr/`](https://openonco.info/ukr/)).
Метрики KB у реальному часі, матриця покриття за хворобами, частка
клінічних sign-off:
**[openonco.info/ukr/capabilities](https://openonco.info/ukr/capabilities.html)**.

### Структура каталогу

```
knowledge_base/
├── schemas/         # Pydantic-моделі сутностей (Disease, Drug, Indication, …)
├── engine/          # рушій правил, MDT-оркестратор, render, персистентність
├── validation/      # YAML-loader + схема + перевірка референтної цілісності
├── clients/         # клієнти живих API (CT.gov, PubMed, DailyMed, openFDA, …)
├── ingestion/       # loader-и хостових джерел (CIViC, CTCAE, ICD-O-3, МОЗ, НСЗУ, …)
├── hosted/
│   ├── content/     # YAML-база знань — клінічний контент
│   ├── code_systems/, civic/, ctcae/   # vendored-снепшоти
│   └── audit/       # signoffs.jsonl — журнал клінічних sign-off
└── stats.py         # KB-статистика для публічної /capabilities-сторінки
```

### Що реалізовано

- **Рушій правил** — `generate_plan()` і `generate_diagnostic_brief()`
  будують версіонований `PlanResult` з профілю пацієнта.
- **MDT-оркестратор** — активація ролей, Open Questions, граф
  decision-provenance для аудитного пояснення
  ([`MDT_ORCHESTRATOR_SPEC.md`](../specs/MDT_ORCHESTRATOR_SPEC.md),
  [`DIAGNOSTIC_MDT_SPEC.md`](../specs/DIAGNOSTIC_MDT_SPEC.md)).
- **Двотрекові плани** — стандартний + інтенсивний поряд
  ([CHARTER §15.2 C6](../specs/CHARTER.md) — захист від
  automation-bias).
- **CIViC actionability** (CC0) — fusion-aware variant matcher,
  ESCAT-tier рендеринг, місячний CI-refresh снепшоту.
- **Триланкова citation-guard** — referential-integrity SRC-* у
  loader, фоновий citation-verifier, strip-or-fail при рендері.
- **Білінгвальний рендер** — Plan / Brief HTML в UA та EN; мітки UI
  + назви KB + free-text-проза локалізуються залежно від `target_lang`.
- **Pre-biopsy режим** ([CHARTER §15.2 C7](../specs/CHARTER.md) —
  жорстке правило) — рушій відмовляється видавати лікувальний Plan
  без гістології / disease ID; видає `DiagnosticPlan` з workup-brief.
- **Живі API-клієнти** — ClinicalTrials.gov v2, PubMed, DailyMed,
  openFDA. Окремий rate-limit + TTL-кеш на джерело.
- **Патієнт-режим** — окремий render path з glossing назв препаратів /
  ICD простою мовою, prompt-и "запитайте лікаря", очищення
  технічних ID.
- **Lazy-loading per-disease** — engine bundle = core-zip + per-disease
  zip-и; `/try.html` Pyodide завантажує по запиту.

### Запустити валідатор

```bash
pip install -e .
python -m knowledge_base.validation.loader knowledge_base/hosted/content
```

Виводить усі сутності, валідує кожну проти схеми, перевіряє всі
референси, виконує contract-валідатори (наприклад: кожне клінічне
твердження цитує Source).

### Згенерувати Plan з профілю

```python
from pathlib import Path
from knowledge_base.engine import (
    generate_plan, generate_diagnostic_brief, is_diagnostic_profile,
    orchestrate_mdt, render_plan_html, render_diagnostic_brief_html,
)

KB = Path("knowledge_base/hosted/content")
patient = {...}  # dict у формі FHIR R4 / mCODE

if is_diagnostic_profile(patient):
    result = generate_diagnostic_brief(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_diagnostic_brief_html(result, mdt=mdt, target_lang="uk")
else:
    result = generate_plan(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_plan_html(result, mdt=mdt, target_lang="uk")
```

Той самий рушій працює в браузері через Pyodide — див.
[openonco.info/try.html](https://openonco.info/try.html).

### Додати нову сутність

1. Прочитай [`KNOWLEDGE_SCHEMA_SPECIFICATION.md`](../specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md)
   для канонічного визначення сутності.
2. Напиши YAML під відповідним каталогом `hosted/content/<type>/`.
3. Запусти валідатор.
4. Нове джерело → додай YAML Source з повними license / hosting
   метаданими за [`SOURCE_INGESTION_SPEC.md`](../specs/SOURCE_INGESTION_SPEC.md).
5. Клінічний контент (Indication / Regimen / RedFlag /
   Contraindication / SupportiveCare) лишається STUB, доки **двоє з
   трьох Clinical Co-Leads** не підтвердять через signoff-журнал
   ([CHARTER §6.1](../specs/CHARTER.md)) — ніколи не виставляй
   `reviewed: true` самостійно.

### Конвенції схеми

- ID: префікс + upper-case, наприклад `DIS-HCV-MZL`, `DRUG-RITUXIMAB`,
  `BMA-EGFR-L858R-OSIMERTINIB`.
- Цитування: кожне клінічне твердження посилається на Source через
  `source_id`, ніколи не inline-URL.
- Назви: `names: {ukrainian, english, preferred, synonyms: [...]}`.
  Render обирає на основі `target_lang`.
- `model_config = ConfigDict(extra="allow")` на кожній сутності, щоб
  додавання полів у YAML не ламало схему; pin-уй конкретні поля як
  required, коли стабільні.

### Внески через TaskTorrent

Маєш вільну ємність у Claude Code, Codex, Cursor чи ChatGPT? Візьми
структуровану задачу з черги і відкрий PR — повний гайд у
[`docs/contributing/CONTRIBUTOR_QUICKSTART.md`](../docs/contributing/CONTRIBUTOR_QUICKSTART.md)
або на публічній сторінці
[openonco.info/ukr/contribute.html](https://openonco.info/ukr/contribute.html).
