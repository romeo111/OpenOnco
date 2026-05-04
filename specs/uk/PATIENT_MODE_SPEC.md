# Patient-Mode Render Specification

**Проєкт:** OpenOnco
**Документ:** Patient-mode render layer — спрощений звіт для пацієнта
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads
**Попередні документи:** CHARTER.md (особливо §2, §8.3, §9.3, §11, §15),
KNOWLEDGE_SCHEMA_SPECIFICATION.md, CLINICAL_CONTENT_STANDARDS.md,
DATA_STANDARDS.md
**План реалізації:** `docs/plans/patient_simplified_report_2026-05-01-1300.md`

---

## Мета документа

OpenOnco генерує план лікування у двох mode рендерингу:

1. **Clinician mode** (existing) — повний tumor-board brief: треки
   side-by-side, контрainдікації, sources, ESCAT/CIViC tier, FDA
   metadata, CHARTER §6.1 sign-off badges.
2. **Patient mode** (existing з 2026-04-27 — CSD-3) — стислий звіт
   зрозумілою мовою для пацієнта.

Цей spec формалізує **контракт patient-mode рендера**: інваріанти,
джерела даних, правила перекладу, обов'язкові секції, contract тестів,
а також — критично — **симетричний access-model**: лікар може
відкрити пацієнтський звіт; пацієнт може відкрити лікарський.

До цього spec patient-mode інваріанти жили в test assertions у
[`tests/test_patient_render.py`](../tests/test_patient_render.py); цей
документ робить їх явними і додає правила, яких поточна реалізація не
дотримується (per-track presentation, rationale-from-trace, between-visit
watchpoints, no-Latin gate).

---

## 1. Принципи

### 1.1. CHARTER §8.3 invariant: render-only

Patient-mode не впливає на вибір лікування. Конкретно:

- `_patient_vocabulary.py`, `_ask_doctor.py`, `_emergency_rf.py`,
  `_patient_rationale.py` — **render-only** layer. Engine MUST NOT
  consult ці модулі як treatment-selection signal.
- Engine output (`PlanResult`) — **єдиний source of truth** для обох
  bundle. Patient version — це **переклад**, не **фільтр**.
- Якщо patient bundle показує менше деталей, ніж clinician — це
  translation choice (compression for readability), не filter choice.

### 1.2. Симетричний access (clarified 2026-05-01)

**Обидва bundle відкриті для обох audience.**

- **Лікар читає пацієнтський звіт** — verification path. Лікар хоче
  переконатись, що lay-language версія не вводить в оману, не пропускає
  й не пом'якшує суттєве.
- **Пацієнт читає лікарський звіт** — radical-transparency path.
  Пацієнт має право подивитись canonical version; lay-friendly
  оформлення лікарського bundle не потрібне.

Patient bundle — це **translation** clinician bundle, **не filter**.
Будь-яка інформація в clinician version, що впливає на patient
understanding, MUST бути representable у patient version. Цей принцип
називається *information parity rule* (§3.4).

### 1.3. Не медичний пристрій (CHARTER §15, §11)

Patient bundle — інформаційний інструмент. Footer disclaimer обов'язковий
(див. §3.6). Bundle не призначений замінити консультацію онколога.

### 1.4. PHI обмеження (CHARTER §9.3)

Patient bundle рендериться з тих самих synthetic / de-identified profiles,
що й clinician — той самий gitignore guard. Real-patient bundles на
github не потрапляють.

---

## 2. Audience model

### 2.1. Reading level

8-й клас української, ESMO patient-guide tone. Припущення про читача:

- Має нещодавно встановлений діагноз і онколога, який провадить лікування.
- Не має медичної освіти.
- Може переслати документ родичу / другу для другої думки.
- Друкуватиме на A4 або читатиме на телефоні.
- Може показати другому лікарю (тому технічні якорі — `data-*`
  атрибути — мають залишатись для перевірки).

### 2.2. Що patient bundle НЕ робить

- Не пропонує дозування (дози — лікар).
- Не дає обіцянок про результат (no "ви вилікуєтесь").
- Не висловлює judgement про доцільність (не "цей варіант кращий").
- Не виводить технічні entity ID у візибл-тексті (RF-, BMA-, IND-
  залишаються в `data-*` атрибутах для дебагу).

---

## 3. Структура bundle

### 3.1. Обов'язкові секції

Patient bundle MUST містити такі anchor-секції у такому порядку:

| # | Селектор | Що рендериться |
|---|---|---|
| 1 | `<header>` | Заголовок, діагноз (UA name), дата, версія плану, cross-link на лікарську версію |
| 2 | `<section class="what-was-found">` | Знахідки молекулярного / лабораторного аналізу простою мовою |
| 3 | `<section class="what-now">` | **Per-track**: рекомендовані препарати, режим, NSZU coverage, sign-off status |
| 4 | `<section class="why-this-plan">` | **NEW.** Пояснення per-track: чому саме цей варіант рекомендовано вам |
| 5 | `<section class="between-visits">` | **NEW.** На що звернути увагу між візитами; коли дзвонити в клініку, коли — у лікарню |
| 6 | `<section class="emergency-signals">` | Симптоми, що вимагають негайної звертання у лікарню |
| 7 | `<div class="ask-doctor">` | 5-7 питань до лікаря на наступному візиті |
| 8 | `<footer class="patient-disclaimer">` | Disclaimer + посилання на github issues |

Cross-link `<a class="mode-toggle">` — у `<header>` (§3.5).

### 3.2. Per-track presentation

Коли `len(plan.tracks) > 1`:

- `what-now`, `why-this-plan`, `between-visits` рендеряться **один раз
  на трек**.
- Треки маркуються `track-card track-card--default` /
  `track-card track-card--alternative` (CSS reuse з clinician).
- Видимий префікс: "А) Стандартний варіант" / "Б) Альтернативний варіант".
  Український літерний префікс, не Latin.

Коли `len(plan.tracks) == 1`:

- Той самий блок без А/Б префіксу.
- `why-this-plan` все одно рендериться (єдиний трек має своє "чому").

### 3.3. Why-this-plan: rationale from trace

Source: `PlanResult.trace` + `PlanResult.kb_resolved["red_flags"]` +
`PlanResult.kb_resolved["disease"]`. Без LLM. Без додаткового authoring.

Renderer (`_patient_rationale.py`):

- Walk алгоритм-trace для кожного треку.
- Per fired clause produce 2-4 рядки plain-UA пояснення:
  - "Бо у вас знайдено **BRAF V600E**" — biomarker-driven clause.
  - "Стандартний варіант рекомендовано, бо ваш стан стабільний (ECOG 1)"
    — no aggressive RF fired.
  - "Альтернативний варіант **не рекомендовано як стандартний**, бо у вас
    активний гепатит B без профілактики" — aggressive RF fired.
- Cap: ≤4 bullets per track. Longer logic falls back to "Деталі — у
  технічній версії звіту".
- Empty trace fallback: "Цей варіант запропоновано на основі стандартів
  NCCN/ESMO для вашого діагнозу. Деталі — у технічній версії звіту."

### 3.4. Between-visits: source rule

Source: `Regimen.between_visit_watchpoints` (новий field, drafted у
spec extension §4 нижче).

- Якщо field присутній і непорожній — render список згрупований по
  `urgency` tier.
- Якщо порожній або відсутній — fallback string:
  > "Список того, на що звернути увагу між візитами, для цього курсу
  > ще не узгоджено клінічною командою. Запитайте лікаря на наступному
  > візиті, які симптоми треба занотовувати, а які — приводи дзвонити
  > в клініку."

**Renderer NEVER fabricates watchpoints** з drug-class vocabulary або
inferences. Якщо field порожній — fallback. Цей invariant захищає від
hallucinated medical advice.

### 3.5. Cross-link chip

У `<header>` patient bundle:

```html
<a class="mode-toggle" href="<sibling>">Технічна версія для лікаря →</a>
```

У `doc-header` clinician bundle:

```html
<a class="mode-toggle" href="<sibling>">Версія для пацієнта →</a>
```

`href` rewrite rules:

- При `--render-mode both` CLI rewrites `href` на sibling filename
  (`<basename>.html` ↔ `<basename>.patient.html`).
- При single-mode рендері `href="#"` (placeholder) — caller (web app,
  embed) переписує самостійно.

### 3.6. Footer disclaimer (regulatory boilerplate)

Обов'язкова мінімальна копія:

> Цей звіт — інформаційний інструмент, не медичний прилад. Усі рішення
> про лікування приймає ваш онколог. Звіт оновлюється, коли з'являються
> нові аналізи. Не змінюйте призначене лікування на основі лише цього
> звіту.

---

## 4. Information parity rule

**Принцип:** anything material у clinician bundle MUST surface у patient
bundle. Compression OK; silent omission — NO.

| Clinician surface | Patient surface |
|---|---|
| Track count + track labels | А/Б prefix у per-track sections (§3.2) |
| Regimen schedule (cycle × cycles) | Plain-UA опис у `what-now` ("4 цикли по 21 день, кожен — крапельниця") |
| Fired RedFlags | Кожен fired RF surface ≥1: emergency banner / rationale / between-visits |
| CHARTER §6.1 sign-off badge per track | Patient sign-off panel (CSD-3 demo вже має) |
| NSZU coverage per drug | NSZU patient label badge (вже існує) |
| ESCAT / CIViC tier | `ESCAT_TIER_PATIENT_LABEL` (вже існує) |
| Source citations (PMIDs, DOIs) | Зведений рядок "Засновано на N клінічних рекомендаціях" — pointer to clinician version for detail |
| FDA disclosure footer | Adapted у patient disclaimer (§3.6) |

### 4.1. Verification anchors (`data-*` attributes)

Кожен patient-visible block emits `data-source-id="REG-…|RF-…|BMA-…"`
attribute. Невидимі по замовчуванню; doctor verifies via View Source або
piping HTML through grep:

```html
<div class="drug-explanation" data-source-id="REG-FOLFOX">
  <h3>Оксаліплатин</h3>
  ...
</div>
```

Це інструмент перевірки, не UI element. CSS не покладається на ці
атрибути.

---

## 5. Vocabulary contract

### 5.1. Lookup tables

Усі — у [`knowledge_base/engine/_patient_vocabulary.py`](../knowledge_base/engine/_patient_vocabulary.py):

- `DRUG_CLASS_PLAIN_UA` — drug-class blurb.
- `VARIANT_TYPE_PLAIN_UA` — V600E, T790M, MSI-H, тощо.
- `ESCAT_PLAIN_UA` + `ESCAT_TIER_PATIENT_LABEL` — рівень доказів.
- `NSZU_PLAIN_UA` + `NSZU_PATIENT_LABEL` — coverage labels.
- `LAB_PLAIN_UA` — ANC, LVEF, eGFR.
- `AE_PLAIN_UA` — побічні ефекти.
- `SCREENING_PLAIN_UA` — pre-treatment workup.

**Floor:** ≥200 unique entries (currently 372). Test gate:
`test_vocabulary_has_min_200_terms`.

### 5.2. First-use abbreviation expansion

Окрема таблиця `ABBREVIATION_FIRST_USE_UA` (новий field, Phase 5):

```python
{
    "ESCAT": "рівень доказів ESCAT (як міцно доведено, що препарат працює)",
    "FDA": "Управління з продовольства й медикаментів США (FDA)",
    "НСЗУ": "Національна служба здоров'я України (НСЗУ)",
    ...
}
```

Renderer expands first occurrence per bundle; subsequent occurrences —
bare abbreviation.

### 5.3. Allowlist для terms, що залишаються

Дозволено залишати без перекладу у visible тексті:

- **Gene symbols:** BRAF, EGFR, KRAS, NRAS, BRCA1, BRCA2, ALK, ROS1, RET,
  MET, HER2, PD-1, PD-L1, KIT, FGFR3, JAK2, BCR-ABL1, MGMT, IDH1, IDH2,
  FLT3, NPM1, TP53, PIK3CA, PTEN, RB1, MYC, BCL2, CDKN2A.
- **Variant labels:** V600E, V600K, T790M, L858R, G12C, G12D, Q61R,
  F1174L, H1047R, R132H, M918T, exon-14, fusion (translated as "злиття").
- **Tier labels:** ESCAT IA / IB / IIA / IIB / IIIA / IIIB / IV / X
  (з first-use expansion).
- **Drug names:** як у international nonproprietary name (INN) —
  оксаліплатин, бевацизумаб, тощо. Cyrillic transliteration переважна;
  Latin acceptable якщо INN не транслітерований.

Все інше — або український переклад, або first-use expansion.

### 5.4. No-Latin / no-abbreviation gate

Phase 5 deliverable. Test gates:

- `test_patient_html_no_latin_abbreviations_in_visible_text` — regex
  `\b[A-Z]{2,}[a-z]?\b` на visible text; fail unless on allowlist OR
  expansion within 80 chars.
- `test_patient_html_no_bare_latin_words` — regex `\b[a-z]{4,}\b`
  визначає Latin word ≥4 chars, fail якщо не на allowlist (дозволяє drug
  brand names що повертає `_patient_drug_label`).

---

## 6. Two-reviewer signoff (CHARTER §6.1) scope

Patient-mode зачіпає clinical content у двох місцях:

| Контент | Two-reviewer required? |
|---|---|
| `Regimen.between_visit_watchpoints` (Phase 4) | YES — це нова clinical assertion |
| `AE_PLAIN_UA` patient-facing AE wording | YES — впливає на patient understanding of side effects |
| Drug-class blurbs у `DRUG_CLASS_PLAIN_UA` | YES — clinically loaded statements ("блокує BRAF — driver пухлини") |
| Renderer code (`_render_patient_mode`, `_patient_rationale`) | NO — render layer, no new clinical content |
| Fallback strings ("Список ... ще не узгоджено") | NO — UI copy |
| Question templates у `_ask_doctor.py` | NO — render layer; question wording is UI copy |

---

## 7. Test contract

`tests/test_patient_render.py` (existing) + extensions per phase.

### 7.1. Inherited (Section A-G з CSD-3)

- Vocabulary floor ≥200 (Section A).
- No entity-IDs у visible body (Section B): BMA-, DIS-, ALGO-, IND-,
  REG-, BIO-, DRUG-, RF-.
- Required structural anchors (Section C).
- Emergency RF filter (Section D).
- Ask-doctor selection (Section E).
- End-to-end synthetic mCRC + BRAF V600E (Section F).
- A11y: font-size ≥16px, line-height ≥1.5 (Section G).

### 7.2. Нові (per phase)

**Phase 2 (tracks + cross-link):**

- `test_patient_html_two_track_plan_shows_both_tracks`.
- `test_patient_html_single_track_plan_no_a_b_prefix`.
- `test_patient_html_has_clinician_cross_link`.
- `test_clinician_html_has_patient_cross_link`.
- `test_information_parity_smoke` — кожен трек у clinician → у patient
  через `data-source-id`; кожен fired RF → emergency / rationale /
  between-visits.

**Phase 3 (rationale):**

- `test_patient_rationale_braf_v600e_mcrc`.
- `test_patient_rationale_aggressive_blocked_by_rf`.
- `test_patient_rationale_no_trace_fallback`.

**Phase 4 (watchpoints — schema only у цій ітерації):**

- `test_patient_html_watchpoints_section_renders_authored`.
- `test_patient_html_watchpoints_section_renders_fallback`.
- `test_watchpoints_emergency_dedupe`.

**Phase 5 (Latin gate):**

- `test_patient_html_no_latin_abbreviations_in_visible_text`.
- `test_patient_html_no_bare_latin_words`.

---

## 8. CLI integration

```
python -m knowledge_base.engine.cli patient.json --render out.html
python -m knowledge_base.engine.cli patient.json --render out.html --render-mode patient
python -m knowledge_base.engine.cli patient.json --render out.html --render-mode both
```

- `--render-mode {clinician,patient,both}`, default `clinician`
  (back-compat).
- `both` writes `<out>.html` (clinician) + `<out>.patient.html` (patient).
- Cross-link `href` resolves до sibling filename коли `both` selected.

---

## 9. Out of scope для v0.1

- **EN patient bundles** — UA-only. Деплой не-українською потребує 2×
  vocabulary work; revisit якщо буде на горизонті.
- **PDF export** — A4 print-friendly CSS вже існує; users print з браузера.
- **Email delivery / patient portal** — поза CHARTER §9.3 поки немає
  approved patient-data hosting.
- **Динамічна генерація QR-code** — зараз QR живе у CSD-3 demo як
  static asset; renderer не emit-ить QR.

---

## 10. Open questions

1. **`Regimen.between_visit_watchpoints` schema** — який спектр urgency
   tiers? Запропоновані: `log_at_next_visit`, `call_clinic_same_day`,
   `er_now`. Acceptable?
2. **Source citations** у patient bundle — рядок-зведення "Засновано на
   N рекомендаціях" чи окремий expandable блок зі списком?
3. **Sign-off panel** — CSD-3 demo показує per-track pill ("🟢 Підписано
   двома лікарями" / "🟡 ще одна перевірка" / "🔴 ще не перевірено").
   Залишаємо як є чи інша візуальна мова?
