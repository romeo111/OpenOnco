# REDFLAG_AUTHORING_GUIDE — як додати RedFlag

**Status:** v0.1 (P0). **Owner:** Clinical Co-Leads (per CHARTER §6.1).
**Pre-requisites read:** `KNOWLEDGE_SCHEMA_SPECIFICATION.md` §9 (RedFlag),
`CLINICAL_CONTENT_STANDARDS.md` §2/§4/§6, `CHARTER.md` §6 / §8.3.

Цей документ — operational guide для контент-авторів та CI gates. Він
описує **що таке RedFlag, яким мінімальним вимогам має відповідати
кожна нова RedFlag, і як вона вмикається в Algorithm.decision_tree**.

---

## 1. Що таке RedFlag (і чим він не є)

**RedFlag** — це машинно-обчислюваний клінічний finding, який, якщо
тригерується у профілі пацієнта, **зміщує вибір Indication** у вже
існуючому Algorithm. RedFlag **не призначає лікування сам по собі**.
RedFlag — це **вхід** до decision_tree, не вихід (CHARTER §8.3).

### RedFlag IS

- Бінарний `True / False` predicate, обчислюваний з `findings` пацієнта
  (lab thresholds, biomarker presence, imaging dimension, composite score).
- Прив'язаний до ≥1 хвороби (`relevant_diseases`) або позначений
  як універсальний (`relevant_diseases: ["*"]`) — якщо застосовний на
  багатьох диseases (HBV-reactivation, TLS-risk, прозн.).
- Має `clinical_direction` — **семантика того, як він зміщує Algorithm**:
  `intensify | de-escalate | hold | investigate`.
- Цитований ≥2 Tier-1/2 джерелами (CLINICAL_CONTENT_STANDARDS §6.1).
  Tier-1: NCCN, ESMO, ASCO, FDA labels, регуляторні документи. Tier-2:
  опубліковані Phase-3 RCT, Cochrane, мета-аналізи.

### RedFlag IS NOT

- ❌ Регімен / доза / графік. Це належить Regimen / Indication.
- ❌ "Цей пацієнт high-risk → дай aggressive treatment" — це
  призначає LLM лікування. Замість цього: RedFlag тригериться по
  cytogenetics → Algorithm обирає альтернативну Indication.
- ❌ Free-text condition без машинного предиката. Кожен trigger має
  посилатися на `findings.<key>` зі threshold/value/comparator.
- ❌ Hard-coded дублікат для кожної хвороби. Якщо flag застосовний
  скрізь (HBV, TLS), позначай `relevant_diseases: ["*"]` і клади в
  `redflags/universal/`.

---

## 2. 5-type matrix (мінімум для кожної хвороби)

Кожна хвороба у KB повинна мати **≥5 RedFlag-ів**, по одному з кожної
категорії (де клінічно доречно):

| # | Тип | Що ловить | Default `clinical_direction` |
|---|-----|----------|------------------------------|
| 1 | **organ-dysfunction** | CrCl <30, Child-Pugh B/C, LVEF <50%, bilirubin >3×ULN, pulmonary diffusion <60% | `de-escalate` або `hold` |
| 2 | **infection-screening** | HBsAg+, anti-HCV+, HIV+, TB-latent (для anti-CD20, BTKi, autoSCT) | `hold` (поки нелікований) або `investigate` |
| 3 | **high-risk-biology** | TP53 / del(17p), MYC-rearrangement, double-/triple-hit, blastoid morph., Ph-like, Ki67 >30% | `intensify` |
| 4 | **transformation-progression** | rapid-progression на therapy, нова bulky mass, нова EN-локалізація | `intensify` |
| 5 | **frailty / age** | ECOG ≥3 OR (вік ≥75 + ≥2 коморбідності + albumin <3.5) | `de-escalate` |

Якщо для хвороби якась з категорій клінічно нерелевантна (e.g.,
infection-screening для PCNSL до анти-CD20 не потрібен) — постав
`<rf>.notes:` з обґрунтуванням замість заглушки.

---

## 3. Шаблон YAML

```yaml
# knowledge_base/hosted/content/redflags/rf_<disease>_<category>_<short>.yaml
id: RF-<DISEASE>-<CATEGORY>-<SHORT>          # uppercase, kebab; e.g., RF-PMBCL-BULKY-MEDIASTINAL
definition: "<one-line EN, machine-extractable trigger spelled out>"
definition_ua: "<one-line UA — translation, not invention>"

# trigger MUST be machine-evaluable. Refer to canonical findings names
# (see DATA_STANDARDS.md §4.2 для list of standardized finding keys).
trigger:
  type: lab_value | imaging_finding | biomarker | composite_score | symptom_composite
  any_of:                                     # OR clauses
    - finding: "<key>"
      threshold: <number>
      comparator: ">=" | ">" | "<=" | "<" | "==" | "!="
    - finding: "<key>"
      value: <bool|string>
  # all_of:  AND clauses (use one or both of any_of/all_of)
  # none_of: must-not-fire clauses

clinical_direction: intensify | de-escalate | hold | investigate

severity: critical | major | minor          # default: major. Used for
                                            # conflict-resolution tie-break
                                            # (engine prefers higher severity
                                            # when directions clash).
priority: 100                                # lower wins in tie-break;
                                            # default 100. Bump to <50 only
                                            # for true override flags.

relevant_diseases:
  - DIS-<CODE>                              # ≥1 disease ID (or ["*"] universal)
shifts_algorithm:
  - ALGO-<CODE>                             # Algorithm IDs whose decision_tree
                                            # references this RedFlag

# Optional: pin which decision_tree step.id this RedFlag drives, для
# coverage-tooling. Engine still walks tree as authored.
branch_targets:
  ALGO-<CODE>: "step-1"

sources:                                    # ≥2 Tier-1/2 sources required
  - SRC-NCCN-BCELL-2025
  - SRC-ESMO-DLBCL-2024

last_reviewed: "YYYY-MM-DD"                # ISO date of last clinical review
draft: false                                # set true only пока триває
                                           # authoring; CI блокує merge non-draft
                                           # без ≥1 source.
notes: >
  Free-text clinical context: чому flag важливий, де він на межі,
  які practical access-constraints в Україні (НСЗУ-reimbursement,
  drug availability), reference до конкретних trial-ів.
```

---

## 4. Wiring у Algorithm.decision_tree

RedFlag активується тоді, коли Algorithm.decision_tree-step посилається
на нього в `evaluate:` блоці:

```yaml
# knowledge_base/hosted/content/algorithms/algo_<disease>_<line>.yaml
id: ALGO-PMBCL-1L
applicable_to_disease: DIS-PMBCL
default_indication: IND-PMBCL-1L-RCHOP-RT

decision_tree:
  - step: 1
    evaluate:
      any_of:
        - red_flag: RF-PMBCL-BULKY-MEDIASTINAL   # single-flag branch
    if_true:
      result: IND-PMBCL-1L-DA-EPOCH-R            # different indication
    if_false:
      next_step: 2

  - step: 2
    evaluate:
      red_flags_all_of:                          # multi-flag combo (P2)
        - RF-PMBCL-RT-INELIGIBLE
        - RF-PMBCL-PARTIAL-RESPONSE-PET
    if_true:
      result: IND-PMBCL-1L-DA-EPOCH-R-NORT
    if_false:
      result: IND-PMBCL-1L-RCHOP-RT
```

**Правила wiring-а:**

1. Кожна `shifts_algorithm: [ALGO-X]` посилання має мати **зворотне**
   посилання — Algorithm `ALGO-X.decision_tree` мусить містити цю
   RedFlag в якомусь step. Інакше CI прапорить orphan RedFlag.
2. Якщо `clinical_direction: investigate` — `shifts_algorithm` має
   бути порожнім (investigate-flags не зміщують вибір; вони тільки
   surface-aть annotations у Plan / MDT brief).
3. Multi-flag combos (`red_flags_all_of: [...]`, `red_flags_any_of: [...]`)
   — підтримуються engine-ом з P2. Використовуй для ситуацій типу
   "DLBCL з HIGH-IPI **та** double-hit → DA-EPOCH-R + IT prophylaxis".

---

## 5. Conflict-resolution (як engine розрулює, коли тригериться кілька)

Коли в одному step тригерять кілька RedFlag-ів з різними
`clinical_direction`, engine застосовує наступний deterministic order:

1. **Direction precedence** (highest wins): `hold` > `intensify` > `de-escalate` > `investigate`
2. **Severity** (highest wins): `critical` > `major` > `minor`
3. **Priority** (lowest number wins): default 100, bump-аj <50 для
   справжніх override-ів

Engine викидає переможця в `trace[*].fired_red_flags[0]` і логує
повний список як `trace[*].fired_red_flags[1:]`. **Не покладайся
на implicit ordering** — якщо хочеш конкретний flag завжди вигравав
свій conflict, виставляй `priority: <50`.

---

## 6. Citation requirements (CHARTER §6.1, CLINICAL_CONTENT_STANDARDS §6.1)

- **Мінімум 2 незалежні Tier-1 або Tier-2 джерела** для кожної non-draft
  RedFlag. CI попереджає (warn) якщо <2 і блокує (error) якщо 0.
- **Tier-1**: NCCN (поточна version), ESMO (поточна), ASCO, WHO, FDA labels.
- **Tier-2**: опубліковані Phase-3 RCT, Cochrane reviews, мета-аналізи з peer-reviewed журналів.
- Source IDs мусять існувати в `knowledge_base/hosted/content/sources/`.
  Якщо потрібного джерела немає — спочатку додай Source entity per
  SOURCE_INGESTION_SPEC §8.

---

## 7. Authoring checklist (пройдись по всіх до PR)

- [ ] YAML валідується pydantic-схемою (запусти `python -m knowledge_base.validation.loader`)
- [ ] `id` уникальний у KB
- [ ] `definition` + `definition_ua` обидва заповнені
- [ ] `trigger` 100% машинно-обчислюваний (`finding` + `threshold|value`)
- [ ] `clinical_direction` присвоєний (та consistent з `shifts_algorithm`)
- [ ] `relevant_diseases` posilaa-ся на існуючі `DIS-*` або `["*"]`
- [ ] ≥2 sources (Tier-1/2) з валідними `SRC-*` IDs
- [ ] Algorithm ALGO-X у `shifts_algorithm` дійсно посилається на цей RF в decision_tree
- [ ] Якщо `investigate` → `shifts_algorithm: []`
- [ ] `last_reviewed` встановлений на дату клінічного review
- [ ] `draft: false` (або `true` якщо ще на review)
- [ ] Two-reviewer sign-off у PR (CHARTER §6.1)

---

## 8. Найчастіші помилки

| Симптом | Причина | Фікс |
|---------|---------|------|
| RF тригериться але Plan не міняється | shifts_algorithm порожній / Algorithm не посилається на RF | Додай `red_flag: RF-X` в decision_tree step |
| Кілька RF-ів тригерять, обирається не той | Conflict-resolution: подивись на trace; виставив priority/severity | Підкоригуй `priority: <N>` на тому, що мав вигравати |
| CI помилка "X not found in any loaded entity" | `relevant_diseases` / `sources` / `shifts_algorithm` посилається на неіснуючий ID | Створи відсутню entity або виправ ID |
| Pydantic ValidationError при load | `clinical_direction` не з enum, або `severity` не з enum | Використай тільки `intensify/de-escalate/hold/investigate` та `critical/major/minor` |

---

## 9. Тестова батарея (P3)

Для кожної новонаписаної RedFlag — мінімум 2 golden fixtures у
`knowledge_base/tests/fixtures/redflags/<rf_id>/`:

```
positive.json  # virtual patient who SHOULD trigger this RF
negative.json  # virtual patient who SHOULD NOT
expected.yaml: # expected fired_red_flags + selected_indication for each
  positive:
    fires: true
    selected_indication: IND-...
  negative:
    fires: false
    selected_indication: IND-...   # whatever the algorithm's default branch yields
```

CI runner запустить `walk_algorithm` на кожній фікстурі і fail-ить
тест якщо `fired_red_flags` чи `selected_indication` розходиться з
очікуваним. Це і дає coverage-метрику ("X% RFs мають golden tests")
і regression-захист коли engine чи RF-структура змінюються.
