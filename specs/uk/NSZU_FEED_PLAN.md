# NSZU Feed — План фічі (Live-feed змін формуляру НСЗУ)

**Статус:** v0.1 draft, pre-discovery.
**Власник:** TBD.
**Дата:** 2026-04-26.

## Мета і не-цілі

**Мета:** клініцист отримує сигнал про зміни reimbursement, що зачіпають його активні плани, без ручного моніторингу.

**Явні не-цілі:**
- Не вирішуємо за лікаря — лише signaling.
- **Не фільтруємо план за reimbursement** (CHARTER §8.3 + memory-правило `efficacy > registration`: NSZU-статус — metadata layer, не gate. Engine все одно показує найкращий по доказах варіант).
- Не trackуємо реальну наявність у конкретній лікарні (це ProZorro-рівень, окрема пайплайн, не у скоупі).

## P0 — Discovery (треба ДО першого рядка коду)

Найризикованіший етап. Без чесних відповідей будуємо в порожнечу.

| Питання | Як відповісти |
|-|-|
| Де НСЗУ публікує актуальний формуляр? (PDF / HTML / open-data CSV) | 2 години manual exploration `nszu.gov.ua` + open-data порталу |
| Як часто оновлюється? Регулярно чи спорадично? | Те ж + перевірити `Last-Modified` headers за 3 місяці |
| Granularity: тільки INN, чи з brand-names + дозуваннями? | Inspect конкретного PDF онко-пакета ПМГ |
| Reimbursement відрізняється по регіонах? | 1 запит у НСЗУ-press або клін-чат |
| Що болить більше: «у формулярі» vs «реально на складі лікарні»? | Питання №3 в інтерв'ю (нижче) |

**Output P0:** `specs/NSZU_FEED_DISCOVERY.md` — підтверджена cadence + format + ризики. Якщо формату немає (тільки скан-PDFs без структури) — переоцінити доцільність.

## Дані: джерела

**Primary:** Програма медичних гарантій, онко-пакет НСЗУ.
**Secondary:** МОЗ-наказ зі списком "Доступні ліки" (онко-частина), якщо релевантно.
**Out of scope:** ProZorro tender-data (наявність на установі).

Snapshot-storage:
```
knowledge_base/hosted/content/reimbursement/snapshots/
  nszu_2026-04-26.yaml
  nszu_2026-05-03.yaml
  ...
```

Один файл на дату, immutable, валідується schema-loader-ом.

## Schema additions

**`ReimbursementStatus`** (per drug):
```yaml
drug_id: drugbank-DB06317
nszu_program: pmg_oncology_2026
status: reimbursed | restricted | not_listed
restrictions:
  - line_of_therapy: ["1L"]
  - indication_codes: ["C90.0"]
effective_from: 2026-04-26
source_url: https://nszu.gov.ua/...
source_snapshot: nszu_2026-04-26.yaml
```

**`ReimbursementChange`** (diff-derived, не пишеться руками):
```yaml
change_id: rc-2026-05-03-darat-loss
drug_id: drugbank-DB06317
from_status: reimbursed
to_status: not_listed
detected_at: 2026-05-03
affected_regimen_ids: [REG-DARA-VRD, REG-DARA-RD]
```

## Mapping: НСЗУ-рядок → KB Drug

**Найкрихкіша частина.** НСЗУ публікує українські INN + brand-names; engine оперує `Drug.id` (RxNorm/DrugBank-based).

Підхід:
1. **Manual seed:** 50 онко-препаратів з активних KB-Regimens → `knowledge_base/hosted/content/reimbursement/mapping_nszu.yaml`. Two-reviewer merge (CHARTER §6.1) бо плив на recommendations.
2. **Test gate:** кожен `Drug.id`, який використовується у активному `Regimen`, мусить мати або mapping, або явний `reimbursement_status: not_tracked`. Інакше CI fail.
3. **Unmapped queue:** нові НСЗУ-рядки без mapping → `unmapped_log.yaml` → ручний розгляд Clinical Co-Lead (додати / відхилити).

## Pipeline

```
[ weekly cron job ]
       ↓
1. fetch NSZU sources (HTML + PDF + open-data CSV)
       ↓
2. parse → snapshot YAML (валідується loader-ом)
       ↓
3. diff(today, previous_snapshot) → list[ReimbursementChange]
       ↓
4. для кожної change:
     - знайти Regimens що використовують affected Drug
     - emit ProvenanceEvent (event_type=reimbursement_change) на patient_id
       (через існуючий event_store/append_event)
       ↓
5. публікація:
     - knowledge_base/hosted/content/reimbursement/changelog.yaml (truth)
     - docs/changelog-nszu.html (public, build_site)
```

**Re-use що вже існує:** `ProvenanceEvent` + `event_store` (commit `98ec53f`). Reimbursement-change це новий `event_type` literal, інакше та сама механіка.

## Engine integration

Под час побудови плану engine читає поточний `ReimbursementStatus` для кожного `Regimen` і **додає його як metadata-badge** — не виключає не-reimbursed варіант:

- 🟢 **НСЗУ** — у формулярі, дата snapshot
- 🟡 **обмежено** — є restriction (line / indication / dose)
- 🔴 **не у формулярі** — patient-pay або заявка
- ⚪ **not_tracked** — препарат не в нашому mapping (чесний indicator)

**Опційний "NSZU-only fallback track":** якщо клініцист хоче явно — окрема кнопка «Show alternative regimen using only reimbursed drugs». Не дефолт. Це постфакт-лінз, не первинний план.

## UI / alert surfaces

| Surface | Що показує | Auth required? |
|-|-|-|
| `/try.html` plan output | Badge на кожному Regimen | Ні |
| `/changelog-nszu.html` (новий) | Публічний feed усіх змін за 12 тижнів, фільтр по препарату/диз | Ні |
| Per-clinician digest | «13 ваших активних планів торкається сьогоднішня зміна» | Так — відкласти до auth (P3 roadmap) |
| Email-дайджест (легкий) | Mailto: subscribe form, weekly send | Ні (manual mail-merge у переходному періоді) |

## Phasing

| Phase | Scope | Done-criterion | Estimate |
|-|-|-|-|
| **P0** Discovery | Manual NSZU exploration + 1 клін-інтерв'ю | `NSZU_FEED_DISCOVERY.md` з confirmed cadence/format | 1-2 дні |
| **P1** Scraper + snapshot | Один онко-пакет, ручний run | YAML snapshot проходить validator | 3-5 днів |
| **P2** Mapping seed | 50 препаратів + test gate | 100% активних Drug покриті mapping/not_tracked | 2 дні |
| **P3** Engine integration (badge) | Read status, render badge | `/try.html` показує статус на кожному Regimen | 2-3 дні |
| **P4** Diff + public changelog | Weekly cron + `/changelog-nszu.html` | Live page оновлюється з cron | 3 дні |
| **P5** Fallback-track button | «Show NSZU-only alternative» | UX cycle з 1 клін-тестером | 2-3 дні |
| **P6** Per-clinician alerts | Email digest / inbox | Відкласти до auth-роботи | — |

**MVP = P0-P4** (~2 тижні). P5/P6 — окремі релізи, фіча корисна без них.

## Ризики

| Ризик | Mitigation |
|-|-|
| НСЗУ format раптом змінився, parser зламався | Contract-test на кожен snapshot. При fail — last-good snapshot stays + UI-banner «дані застарілі станом на DATE» |
| Drug-name false-positive matching (brand collision) | Manual mapping з two-reviewer sign-off, не auto-mapping |
| Лікар довіриться NSZU-signal-у, пропустить ефективніший regimen | UI-копія: «це інформація про формуляр, не клін-рекомендація». Best-evidence варіант — завжди default |
| «Не доступно в моєму регіоні» хоча у формулярі | Чесно: trackуємо тільки формуляр. Посилання «де перевірити наявність по установі» |
| Snapshot history роздуває репо | Diff-only після 8 тижнів, повний snapshot щомісяця |
| PDF-only джерело без структури | Виявити в P0. Якщо так — переоцінити: можливо проєкт стає volunteer-driven manual-update замість автоматичного |
| Конфлікт з memory-rule `efficacy > registration` | Архітектурно вирішено: metadata layer, не filter. Engine не змінює рекомендацій по reimbursement |

## Validation interview (виконати перед P1)

Один дзвінок, **5 питань, 20 хвилин:**

1. «Скільки разів **на місяць** ви переробляєте план через зміну reimbursement?» — калібрує priority
2. «Як зараз дізнаєтесь — пацієнт, лік-чат, НСЗУ-сайт, ніяк?» — калібрує channel
3. «Що болить сильніше: alert по формуляру, чи real-time stock у конкретній лікарні?» — калібрує scope (формуляр vs ProZorro)
4. «Engine бачить що daratumumab більше не у формулярі — ви хочете автоматично побачити fallback regimen, чи лише попередження?» — калібрує autonomy
5. «Довірили б скрейпер з ризиком що часом зламається — vs руками раз на тиждень дивитися?» — калібрує надійність-vs-effort

**Hard kill criterion:** якщо 2+ клініцистів кажуть «менше ніж 1 раз на квартал переробляю» — фіча не варта зусиль, кладемо на полицю до іншого signal-у.

## Open questions

1. **Клін-контакт для P0?** Без однієї людини, з якою провести інтерв'ю до коду — ризикуємо будувати в порожнечу.
2. **«Metadata, не filter»** — погодити explicitly з Clinical Co-Leads, бо архітектурно це коштує менше але теоретично можна було б фільтрувати.
3. **Priority vs roadmap:** P1 (push перед іншими) чи P2 (після patient-registry/auth)?

## Залежності

- `knowledge_base/engine/event_store.py` (commit `98ec53f`) — re-use для reimbursement-change events.
- `knowledge_base/schemas/` — додати `ReimbursementStatus`, `ReimbursementChange`.
- `knowledge_base/validation/loader.py` — нова контент-категорія `reimbursement/`.
- `scripts/build_site.py` — `/changelog-nszu.html` rendering.
- `legacy/source_pdfs/` — потенційно сюди фоллбекуються raw PDFs (вже у gitignore).

## Що цей spec НЕ покриває

- Auth/registry для per-clinician inbox (P3 у roadmap, окремий spec).
- ProZorro stock-level integration (окрема фіча, окремий spec).
- Reimbursement у країнах поза Україною (поки не у скоупі).
