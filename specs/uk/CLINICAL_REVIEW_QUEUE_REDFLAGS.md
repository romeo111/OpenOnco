# Черга клінічного review — RedFlags

**Кому:** клінічному рецензенту OpenOnco (онколог-гематолог).
**Контекст:** після технічного раунду роботи над red-flag-розгалуженнями
(2026-04-25) лишились пункти, які **тільки клініцист може закрити** — бо
CHARTER §8.3 забороняє LLM генерувати клінічні рекомендації без
людського підтвердження.

**Що вже зроблено** (для розуміння контексту):
- Schema RedFlag розширена (`severity`, `priority`, `branch_targets`, `draft`).
- Engine підтримує multi-flag combos + детермінований conflict-resolver.
- 21 active + 3 universal RFs мають golden-fixture pos+neg тести (48 фікстур, 56 pytest-passing).
- 75 scaffolds згенеровано для 15 хвороб з нульовим покриттям (всі marked `draft: true`).
- CI-валідатор блокує merge non-draft RF без джерел / з invalid `clinical_direction` / з orphan `relevant_diseases`.
- Author guide: `specs/REDFLAG_AUTHORING_GUIDE.md` — читай перед редагуванням.

**Estimate сумарно**: ~110-160 годин роботи в 4-х черзіх (A → B → C → D).
A і B — найвищий ROI (compliance + найменше зусиль).

---

## TL;DR — порядок виконання

1. **A.** 18 RFs мають тільки 1 джерело — додай ≥1 додаткове Tier-1/2.
   *~9 годин content lookup*. Open targets per CLINICAL_CONTENT_STANDARDS §6.1.
2. **B.** 1 RF (RF-HBV-COINFECTION) лишився orphan — clinical decision:
   додати 3-тю Indication у ALGO-HCV-MZL-1L АБО reclassify як investigate
   + deprecate (бо є universal-аналог). *~2-4 години*.
3. **C.** 75 scaffold-stub-ів (15 хвороб × 5 категорій) — заповнити real
   trigger predicate, ≥2 sources, decision_tree wiring у відповідному
   Algorithm. *~1-2 години на RF — ~100-150 годин total*.
4. **D.** Sanity-review 48 golden fixtures: чи покриває pos/neg
   реалістичні clinical scenarios.
   *~5-10 хвилин на fixture — ~5-8 годин total*.
5. **E.** *(опційно)* Перегляд 6 `investigate`-only RFs — чи якісь з них
   мають насправді shift-ити. *~3-5 годин*.

Кожна задача — окремий PR з two-reviewer sign-off (CHARTER §6.1).
Робота **A**, **B** і **D** можна робити паралельно; **C** — disease-by-disease.

---

## A. Citation backfill — 18 single-cited RFs

CLINICAL_CONTENT_STANDARDS §6.1 вимагає **≥2 незалежних Tier-1/2 джерел**
для clinical content. Зараз кожен з 18 RFs нижче має лише 1 — задача
додати ≥1 ще.

**Action per item:**
1. Відкрий YAML.
2. Знайди 2-ге Tier-1/2 джерело (ESMO guideline, ASCO, peer-reviewed
   Phase-3 RCT, FDA label) яке підтверджує той самий clinical concept.
3. Якщо Source entity ще немає в `knowledge_base/hosted/content/sources/` —
   спочатку додай його за SOURCE_INGESTION_SPEC §8.
4. Додай ID у `sources:` block.
5. Onov `last_reviewed: "<сьогоднішня дата>"`.
6. PR + 2-reviewer merge.

**Acceptance:** `python -m knowledge_base.validation.loader` дає 0
contract warnings про "<2 sources" для цього RF.

| # | RedFlag | YAML | Поточне джерело | Що додати (підказка) |
|---|---------|------|-----------------|----------------------|
| 1 | RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION | rf_aggressive_histology_transformation.yaml | NCCN B-cell 2025 | ESMO MZL guideline 2024 (transformation criteria) |
| 2 | RF-AITL-AUTOIMMUNE-CYTOPENIA | rf_aitl_autoimmune_cytopenia.yaml | NCCN B-cell 2025 | ESMO PTCL guideline; де AIHA/ITP описані як AITL feature |
| 3 | RF-AITL-EBV-DRIVEN-B-CELL | rf_aitl_ebv_driven_b_cell.yaml | NCCN B-cell 2025 | ESMO PTCL; WHO 5th-edition lymphoid classification |
| 4 | RF-AITL-HYPOGAMMA | rf_aitl_hypogamma.yaml | NCCN B-cell 2025 | ESMO PTCL; recurrent infection + IVIG indication |
| 5 | RF-BURKITT-HIGH-RISK | rf_burkitt_high_risk.yaml | NCCN B-cell 2025 | ESMO Burkitt 2024; CALGB-style risk stratification |
| 6 | RF-CHL-ADVANCED-STAGE | rf_chl_advanced_stage.yaml | NCCN B-cell 2025 | ESMO Hodgkin 2024 (Lugano staging III/IV → ABVD/escBEACOPP) |
| 7 | RF-CLL-HIGH-RISK | rf_cll_high_risk.yaml | NCCN B-cell 2025 | iwCLL 2018 guidelines (TP53/del17p definition) + ESMO CLL |
| 8 | RF-DLBCL-CNS-RISK | rf_dlbcl_cns_risk.yaml | NCCN B-cell 2025 | CNS-IPI primary publication (Schmitz et al. JCO 2016); ESMO DLBCL |
| 9 | RF-DLBCL-HIGH-IPI | rf_dlbcl_high_ipi.yaml | NCCN B-cell 2025 | POLARIX trial (Tilly et al. NEJM 2022); ESMO DLBCL |
| 10 | RF-FL-HIGH-TUMOR-BURDEN-GELF | rf_fl_high_tumor_burden_gelf.yaml | NCCN B-cell 2025 | GELF criteria primary (Brice et al. JCO 1997); ESMO FL |
| 11 | RF-FL-TRANSFORMATION-SUSPECT | rf_fl_transformation_suspect.yaml | NCCN B-cell 2025 | ESMO FL; histologic transformation review |
| 12 | RF-MCL-BLASTOID-OR-TP53 | rf_mcl_blastoid_or_tp53.yaml | NCCN B-cell 2025 | TRIANGLE trial; ESMO MCL 2024 |
| 13 | RF-MF-LARGE-CELL-TRANSFORMATION | rf_mf_large_cell_transformation.yaml | NCCN B-cell 2025 | ESMO MF/SS; large-cell transformation criteria |
| 14 | RF-MF-SEZARY-LEUKEMIC | rf_mf_sezary_leukemic.yaml | NCCN B-cell 2025 | ISCL/EORTC staging (Olsen et al. Blood 2007) |
| 15 | RF-MM-HIGH-RISK-CYTOGENETICS | rf_mm_high_risk_cytogenetics.yaml | NCCN MM 2025 | mSMART 3.0; IMWG R-ISS; ESMO MM |
| 16 | RF-MM-RENAL-DYSFUNCTION | rf_mm_renal_dysfunction.yaml | NCCN MM 2025 | IMWG renal failure consensus; ESMO MM |
| 17 | RF-TCELL-CD30-POSITIVE | rf_tcell_cd30_positive.yaml | NCCN B-cell 2025 | ECHELON-2 trial (Horwitz et al. Lancet 2019); ESMO PTCL |
| 18 | RF-WM-HYPERVISCOSITY | rf_wm_hyperviscosity.yaml | NCCN B-cell 2025 | IWWM consensus; ESMO WM |

**Total: ~9 годин** (≈30 хв на RF: знайти джерело, перевірити, додати).

---

## B. Wiring orphan RFs

**Status (станом на 2026-04-25):** з 3 початкових orphans **2 вже wired-овані**
(см. `docs/plans/archive/rf_wiring_audit_2026-04-25.md`). Лишився **1 відкритий**
clinical-decision item:

| RF | Algorithm | Status |
|----|-----------|--------|
| RF-DECOMP-CIRRHOSIS | ALGO-HCV-MZL-1L | ✅ wired у step 1 |
| RF-TCELL-CD30-POSITIVE | ALGO-ALCL-1L | ✅ wired у step 1 |
| RF-HBV-COINFECTION | ALGO-HCV-MZL-1L | ⏳ **clinical decision needed** |

### B.1 — RF-HBV-COINFECTION (відкрите питання)

- **Тригер:** `hbsag=positive OR anti_hbc_total=positive`
- **Поточний `clinical_direction:`** `hold`
- **Проблема:** ALGO-HCV-MZL-1L має 2 arm-и (ANTIVIRAL vs BR-AGGRESSIVE);
  жоден з них не семантично "hold для HBV-prophylaxis". Тобто `hold`
  direction не підходить під поточну архітектуру цього algorithm-у.

**Дві опції на вибір клініциста:**

- **Опція 1 — додати 3-тю Indication.** Створити нову Indication
  `IND-HCV-MZL-1L-HBV-PROPHYLAXIS-FIRST` яка вмикає entecavir/TDF
  prophylaxis ПЕРЕД продовженням rituximab-based терапії. Тоді
  decision_tree додає step: HBsAg+ → ця нова Indication; інакше — поточний
  flow.

- **Опція 2 — reclassify як investigate** + видалити `ALGO-HCV-MZL-1L` з
  `shifts_algorithm`. RF лишається surveillance flag (annotation у Plan
  про необхідність HBV-prophylaxis); regimen вибирається без змін;
  premedication додається через `supportive_care` entity.

  *Це підказана опція**, бо вже є **universal RF-UNIVERSAL-HBV-REACTIVATION-RISK**
  з тим самим тригером і `clinical_direction: investigate` — disease-specific
  RF-HBV-COINFECTION тоді стане редундантним і його можна **deprecate-ити**
  (видалити, лишити лише universal).

- **Файл:** `knowledge_base/hosted/content/redflags/rf_hbv_coinfection.yaml`
- **Після рішення:** прибрати `("RF-HBV-COINFECTION", "ALGO-HCV-MZL-1L")` з
  whitelist у `tests/test_redflag_fixtures.py::_KNOWN_ORPHANS`.

**Total B: ~2-4 години** (одне рішення + або wiring, або YAML edit + тесты).

---

## C. Заповнити 75 scaffolds для 15 zero-coverage хвороб

Кожна з цих 15 хвороб тепер має 5 RF-stubs (по одному на категорію
з REDFLAG_AUTHORING_GUIDE §2). Усі marked `draft: true` і CI їх
warn-ить, але не блокує merge.

**Workflow per RF:**
1. Відкрити stub YAML.
2. Замінити placeholder `definition` і `definition_ua` на disease-specific
   clinical statement (1 речення, що саме ловить).
3. Замінити placeholder `trigger.any_of[*].finding` на real machine-evaluable
   predicate з cited guideline. Якщо canonical `finding` key ще не
   існує в DATA_STANDARDS — або обери канонічний, або додай у §4.2.
4. Замінити `SRC-TODO` на ≥2 real Tier-1/2 source IDs. Створи Source
   entity якщо ще немає (SOURCE_INGESTION_SPEC §8).
5. Додати step у `<algorithm_id>.decision_tree`, що посилається на цей RF
   та routes до конкретної (existing або нової) Indication.
6. Заповнити `shifts_algorithm: [<algorithm_id>]`.
7. Поставити `last_reviewed: "<дата>"`, `draft: false`.
8. Додати golden-fixture у `tests/fixtures/redflags/<rf_id>/{positive,negative}.yaml`.
9. PR + 2-reviewer merge.

**Acceptance per RF:**
- `python -m knowledge_base.validation.loader` чисто.
- `pytest tests/test_redflag_fixtures.py` чисто.
- `python scripts/redflag_coverage.py` показує цей RF у відповідній клітинці матриці.

### Список хвороб, кожна = 5 stubs

Категорії в кожній хворобі: **organ-dysfunction**, **infection-screening**,
**high-risk-biology**, **transformation-progression**, **frailty-age**.
Якщо клінічно нерелевантна — заміни stub на `notes:` обґрунтуванням.

| # | Хвороба | Algorithm | Файли | Пріоритет |
|---|---------|-----------|-------|-----------|
| 1 | **PMBCL** | ALGO-PMBCL-1L | rf_pmbcl_*.yaml | **HIGH** — DA-EPOCH-R vs R-CHOP залежить від bulky/PET2 |
| 2 | **PCNSL** | ALGO-PCNSL-1L | rf_pcnsl_*.yaml | **HIGH** — CrCl, age, MTX-eligibility — фундамент 1L |
| 3 | **B-ALL** | ALGO-B-ALL-1L | rf_b_all_*.yaml | **HIGH** — Ph+, MRD, age cutoff (pediatric vs adult) |
| 4 | **T-ALL** | ALGO-T-ALL-1L | rf_t_all_*.yaml | **HIGH** — CNS, ETP-ALL, age |
| 5 | **PTLD** | ALGO-PTLD-1L | rf_ptld_*.yaml | HIGH — EBV-status, IS-reduction, transplant-type |
| 6 | **HGBL-DH/-TH** | ALGO-HGBL-DH-1L | rf_hgbl_dh_*.yaml | HIGH — double/triple-hit; CNS prophylaxis |
| 7 | **NK/T-cell nasal** | ALGO-NK-T-NASAL-1L | rf_nk_t_nasal_*.yaml | HIGH — SMILE vs DDGP, asparaginase tolerance, EBV |
| 8 | **HCL** | ALGO-HCL-1L | rf_hcl_*.yaml | MEDIUM — cladribine vs vemurafenib (BRAF+) |
| 9 | **EATL** | ALGO-EATL-1L | rf_eatl_*.yaml | MEDIUM — рідкісна, але без RFs продукт неповний |
| 10 | **HSTCL** | ALGO-HSTCL-1L | rf_hstcl_*.yaml | MEDIUM |
| 11 | **ATLL** | ALGO-ATLL-1L | rf_atll_*.yaml | MEDIUM — IFN+AZT vs aggressive |
| 12 | **T-PLL** | ALGO-T-PLL-1L | rf_t_pll_*.yaml | MEDIUM — alemtuzumab eligibility |
| 13 | **Splenic MZL** | ALGO-SMZL-1L | rf_smzl_*.yaml | MEDIUM — HCV-status, autoimmune cytopenia |
| 14 | **Nodal MZL** | ALGO-NMZL-1L | rf_nmzl_*.yaml | LOW |
| 15 | **NLPBL** | ALGO-NLPBL-1L | rf_nlpbl_*.yaml | LOW — distinct з cHL |

Запропонована послідовність — High → Medium → Low.

**Особливі питання, що вимагають клінічного рішення per disease:**

- **PMBCL frailty-stub:** в PMBCL зазвичай молоді пацієнти. Чи варто
  лишати frailty-RF або замінити на `notes:` що рідко релевантна?
- **PCNSL infection-screening:** PCNSL не використовує anti-CD20 1L, тому
  HBV/HCV screening менш гостро. Чи замінити на CMV/JC reactivation для
  rituximab-based regimens?
- **B-ALL/T-ALL frailty:** педіатричні pathways не використовують age cutoff
  у звичайному сенсі. Поясни в `notes:`.
- **PTLD organ-dysfunction:** transplant patients за замовчуванням мають
  organ-failure базис — RF тут має значення тільки для **зміни тренду**
  (worsening allograft function), не статичний baseline.
- **HCL infection-screening:** purine analogs → опортуністичні інфекції
  (PCP, Listeria) — це screen-перед-лікуванням чи monitoring-під-час?
- **NK/T-nasal frailty:** SMILE дуже інтенсивний — frailty cut-off важливий.

**Total C: ~100-150 годин** (≈1-2 години на RF × 75 RFs).

---

## D. Sanity-check 48 golden fixtures

Я авторив 48 fixtures (24 RFs × pos+neg) автоматично з trigger-структури.
Кожна — мінімум: одне поле, що тригерить (positive) або всі поля false
(negative). Це коректно з точки зору engine-у, але **клінічно це не
завжди реалістичні patient profiles**.

**Action per fixture (~5-10 хв):**
1. Відкрий `tests/fixtures/redflags/<RF-ID>/positive.yaml` та `negative.yaml`.
2. Чи `findings` виглядають як **реальний пацієнт-профіль**, не "штучний"?
3. Якщо ні — додай 2-3 додаткові findings, щоб scenario був правдоподібним
   (e.g., в RF-DLBCL-HIGH-IPI/positive додай LDH, ECOG, age, stage —
   щоб `ipi_score: 3` мав сенс).
4. Додай `notes:` field з коментом-описом сценарію.

Acceptance: subjectively — clinician бачить fixture і думає "так,
бачив такого пацієнта у клініці".

**24 RFs з fixtures:**

```
RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION   RF-DLBCL-CNS-RISK              RF-MM-HIGH-RISK-CYTOGENETICS
RF-AITL-AUTOIMMUNE-CYTOPENIA             RF-DLBCL-HIGH-IPI              RF-MM-RENAL-DYSFUNCTION
RF-AITL-EBV-DRIVEN-B-CELL                RF-FL-HIGH-TUMOR-BURDEN-GELF   RF-TCELL-CD30-POSITIVE
RF-AITL-HYPOGAMMA                        RF-FL-TRANSFORMATION-SUSPECT   RF-WM-HYPERVISCOSITY
RF-BULKY-DISEASE                         RF-HBV-COINFECTION             RF-UNIVERSAL-HBV-REACTIVATION-RISK
RF-BURKITT-HIGH-RISK                     RF-MCL-BLASTOID-OR-TP53        RF-UNIVERSAL-INFUSION-REACTION-FIRST-CYCLE
RF-CHL-ADVANCED-STAGE                    RF-MF-LARGE-CELL-TRANSFORMATION  RF-UNIVERSAL-TLS-RISK
RF-CLL-HIGH-RISK                         RF-MF-SEZARY-LEUKEMIC          RF-DECOMP-CIRRHOSIS
```

**Total D: ~5-8 годин**.

---

## E. (Опційно) Перегляд 6 `investigate`-only RFs

Зараз 6 RFs мають `clinical_direction: investigate` (тобто surveillance-only,
не shift). Decision спецою:

| RF | Чи має шифтити? |
|----|------------------|
| RF-DLBCL-CNS-RISK | Так, ймовірно — IT-prophylaxis branch (R-CHOP+IT-MTX) |
| RF-MM-RENAL-DYSFUNCTION | Так, ймовірно — bortezomib-based замість lenalidomide-based |
| RF-WM-HYPERVISCOSITY | Так — plasmapheresis + швидкий BTKi/anti-CD20 |
| RF-AITL-AUTOIMMUNE-CYTOPENIA | Можливо — IVIG ± steroids перед induction |
| RF-AITL-EBV-DRIVEN-B-CELL | Можливо — додати rituximab arm |
| RF-AITL-HYPOGAMMA | Investigate — IVIG як supportive care, не shift |
| RF-UNIVERSAL-INFUSION-REACTION-FIRST-CYCLE | Investigate (premedication, не shift) |

Якщо для якогось пунктів вирішено "так, шифтити" → переробити на
`intensify`/`de-escalate`/`hold` + wire в decision_tree.

**Total E: ~3-5 годин**.

---

## Сумарний effort

| Черга | Опис | Estimate |
|-------|------|----------|
| A | Citation backfill (18 RFs) | ~9 год |
| B | Resolve 1 remaining orphan (RF-HBV-COINFECTION) | ~2-4 год |
| C | Заповнити 75 scaffolds | ~100-150 год |
| D | Sanity-check 48 fixtures | ~5-8 год |
| E | Re-classify 6 investigate-flags | ~3-5 год |
| **Total** | | **~120-175 год** |

Реалістично — **3-6 тижнів part-time work** з two-reviewer merge на кожен PR.

---

## Як запускати локально

```bash
# Validate KB після кожного редагування
python -m knowledge_base.validation.loader knowledge_base/hosted/content

# RF-specific tests
python -m pytest tests/test_redflag_fixtures.py -v

# Coverage report — підтвердити що покриття зростає
python scripts/redflag_coverage.py
```

---

## Контакти / питання

- Schema-питання: `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §9
- Authoring guide: `specs/REDFLAG_AUTHORING_GUIDE.md`
- Source ingestion: `specs/SOURCE_INGESTION_SPEC.md` §8
- Citation standards: `specs/CLINICAL_CONTENT_STANDARDS.md` §6.1
- Engine code: `knowledge_base/engine/redflag_eval.py`,
  `knowledge_base/engine/algorithm_eval.py`
