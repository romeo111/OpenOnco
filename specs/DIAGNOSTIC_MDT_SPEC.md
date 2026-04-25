# Diagnostic-Phase MDT Specification

**Проєкт:** OpenOnco
**Документ:** Diagnostic-Phase MDT — pre-biopsy / pre-histology workup
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads
**Попередні документи:** CHARTER.md (особливо §1, §2, §15), MDT_ORCHESTRATOR_SPEC.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md

---

## Мета документа

Закриває реальний клінічний use case: **первинна онкологічна
консультація / тумор-борд ДО підтвердженої гістології**. Пацієнт
прийшов з підозрою (об'ємне утворення, цитопенії, B-симптоми),
біопсії ще нема — але MDT вже має зібратись щоб:

1. Визначити правильний підхід до біопсії (де брати, як, який IHC панель)
2. Запланувати staging studies (PET/CT, костномозкова трепанобіопсія)
3. Визначити склад команди для конкретного suspicion pattern
4. Зафіксувати відкриті питання, які треба закрити **до** будь-яких
   обговорень терапії

OpenOnco до цього commit-у вимагав підтверджений `disease_id` для
будь-якого Plan generation — тобто покривав фазу **після** гістології.
Цей spec додає **другий operational mode**, що покриває фазу **до**.

---

## 1. Принципи

### 1.1. Два operational modes (взаємовиключні)

| Mode | Тригер | Output | Patient profile shape |
|---|---|---|---|
| **`treatment_planning`** (existing) | `patient.disease.id` АБО `patient.disease.icd_o_3_morphology` присутній | `Plan` з ≥2 `tracks` (treatment alternatives) + MDT brief | confirmed diagnosis |
| **`diagnostic`** (new) | `patient.disease.suspicion` присутній І `patient.disease.id` ВІДСУТНІЙ | `DiagnosticPlan` (workup steps, mandatory questions, MDT brief) — **жодних treatment tracks** | suspicion only |

Mode визначається **automatically** з patient profile — клієнт явно
не вказує. CLI прапорець `--diagnostic` опційний, для UI/UX зручності
(force diagnostic mode навіть якщо diagnosis заявлений але рев'юер
хоче перепідтвердити workup).

### 1.2. Hard rule: жодних treatment Plan без histology

**Реалізується механічно у коді, не суб'єктивне judgment:**

- `generate_plan(patient)` повертає **error / empty PlanResult** якщо
  `patient.disease.id` AND `patient.disease.icd_o_3_morphology`
  обидва відсутні
- `generate_diagnostic_brief(patient)` повертає **error** якщо
  `patient.disease.id` присутній (рев'юер має використовувати treatment
  mode для confirmed diagnosis)
- Якщо рев'юер хоче "симуляцію" treatment Plan для suspected diagnosis
  — це окрема дія `simulate_plan_for_hypothesis()` що **не** генерує
  справжній Plan і явно маркує output як hypothesis-driven (поза MVP)

### 1.3. Чому це посилює FDA non-device CDS positioning

Diagnostic-phase MDT — **навіть більш чисто** non-device CDS, ніж
treatment planning:

- Workup recommendations — це "list of preventive/diagnostic options"
  (FDA Guidance §IV(3) Example V.A.10) — exactly the carve-out pattern
- Тут зовсім нема **treatment** directives → жодного ризику
  "specific treatment output" disqualifier
- Open questions і mandatory questions explicit → HCP independent
  review базується на чесних gaps

→ доповнення **CHARTER §15.2 C7**: "no treatment recommendations
without confirmed histology" — це нова hard constraint, що
формалізується тут.

---

## 2. Patient profile shape (diagnostic mode)

```json
{
  "patient_id": "PZ-DIAG-001",
  "disease": {
    "suspicion": {
      "lineage_hint": "b_cell_lymphoma",
      "tissue_locations": ["lymph_node", "spleen"],
      "icd_o_3_topography": ["C77.2", "C42.2"],
      "presentation": "Splenomegaly + mediastinal lymphadenopathy + cytopenias",
      "working_hypotheses": ["DIS-SPLENIC-MZL", "DIS-DLBCL", "DIS-FOLLICULAR-LYMPHOMA"]
    }
  },
  "demographics": {
    "age": 58,
    "sex": "male",
    "ecog": 1
  },
  "findings": {
    "splenic_mass_cm": 12.0,
    "ldh_ratio_to_uln": 1.4,
    "anc": 1200,
    "platelets": 95000
  },
  "history": {
    "hcv_known_positive": false,
    "prior_malignancy": null
  }
}
```

`suspicion.lineage_hint` — controlled vocabulary, виражений канонічним
тегом (див. §3.2 матрицю). Інші поля опційні; що більше profile
заповнений, то точніше DiagnosticWorkup можна підібрати і то менше
OpenQuestion підніметься.

`working_hypotheses` — list of `Disease` IDs, які клініцист розглядає.
Якщо вказані — orchestrator може провести **диференціальну** оцінку
(показати, які тести потрібні щоб розрізнити hypothesis A від
hypothesis B). У MVP — тільки інформативно, не drive рекомендацій.

---

## 3. Сутності даних

### 3.1. `DiagnosticWorkup` (KB content entity)

Curated content, живе під `knowledge_base/hosted/content/workups/`.
Аналогічно `Indication` для treatment-mode, але **без** regimen/dose.

```yaml
id: WORKUP-SUSPECTED-LYMPHOMA
applicable_to:
  lineage_hints:
    - b_cell_lymphoma
    - t_cell_lymphoma
    - hodgkin_lymphoma
    - lymphoma  # generic fallback
  tissue_locations:
    - lymph_node
    - spleen
    - stomach
    - thyroid
    - salivary_gland
  presentation_keywords:  # optional substrings to widen match
    - lymphadenopathy
    - splenomegaly
    - cytopenia
    - B-symptom

required_tests:
  - TEST-CBC
  - TEST-LFT
  - TEST-LDH
  - TEST-HBV-SEROLOGY
  - TEST-PET-CT

biopsy_approach:
  preferred: "Excisional biopsy of largest accessible lymph node"
  alternatives:
    - "Core needle biopsy if excisional не feasible"
    - "Ultrasound-guided biopsy для глибоких локалізацій"
  rationale: >
    Архітектура лімфовузла критична для класифікації лімфоми
    (follicular vs diffuse, nodular vs interfollicular). FNA
    недостатня — пропускає architectural pattern.

required_ihc_panel:
  baseline: ["CD20", "CD3", "CD5", "CD10", "CD23", "BCL2", "BCL6", "Ki67"]
  if_b_cell: ["MUM1", "CyclinD1", "EBER-ISH"]
  if_aggressive: ["MYC", "BCL6 break-apart FISH"]

mandatory_questions_to_resolve:
  - "Чи це лімфома, реактивна гіперплазія, чи інша малігнізація?"
  - "Якщо лімфома — підтип за WHO Classification?"
  - "Чи є ознаки трансформації / aggressive component?"
  - "Чи потрібен молекулярний тест (translocation, FISH)?"

expected_timeline_days: 14
expected_workup_cost_uah_estimate: 8000  # рамкова оцінка для українського контексту

triggers_mdt_roles:
  required: [hematologist, pathologist, radiologist]
  recommended: [infectious_disease_hepatology]  # if HBV/HCV not yet ruled out

sources:
  - SRC-NCCN-BCELL-2025
  - SRC-ESMO-MZL-2024

last_reviewed: "2026-04-25"
notes: >
  STUB — for HCV-MZL reference case workup. Expand per-disease as
  KB grows.
```

### 3.2. `DiagnosticPlan` (per-patient artifact, gitignored)

Аналогічно treatment `Plan` (per CHARTER §9.3 — patient-specific,
не у public KB).

```yaml
id: DPLAN-PZ-DIAG-001-V1
patient_id: PZ-DIAG-001
mode: diagnostic
version: 1
generated_at: "2026-04-25T..."

supersedes: null
superseded_by: null
revision_trigger: null

patient_snapshot: { ...full input... }
suspicion_snapshot:
  lineage_hint: b_cell_lymphoma
  tissue_locations: [lymph_node, spleen]
  presentation: "..."
  working_hypotheses: [DIS-SPLENIC-MZL, DIS-DLBCL]

matched_workup_id: WORKUP-SUSPECTED-LYMPHOMA
workup_steps:
  - step: 1
    category: lab
    test_id: TEST-CBC
    rationale: "Baseline cytopenias, marrow involvement assessment"
  - step: 2
    category: lab
    test_id: TEST-HBV-SEROLOGY
    rationale: "HBV reactivation risk before any anti-CD20"
  - step: 3
    category: imaging
    test_id: TEST-PET-CT
    rationale: "Staging + identify highest-yield biopsy site"
  - step: 4
    category: histology
    biopsy_approach: { ...inline from workup... }
    ihc_panel: { ...inline from workup... }

mandatory_questions:  # from workup, surfaced explicitly
  - "Чи це лімфома, реактивна гіперплазія, чи інша малігнізація?"
  - ...

expected_timeline_days: 14

mdt_brief: { ...MDTOrchestrationResult — same shape as treatment mode... }

trace: []  # diagnostic mode has no algorithm decision tree
warnings: []
```

`DiagnosticPlan` instances **не** йдуть у public KB. Зберігаються
поза репо, аналогічно treatment Plan.

### 3.3. Зв'язок з MDT Orchestrator

`orchestrate_mdt()` приймає **або** `PlanResult` **або**
`DiagnosticPlanResult`. Внутрішньо detect mode → застосовує
відповідний rule set:

- Treatment mode: existing R1-R9 (роль базується на disease + tracks
  + biomarkers + regimen)
- Diagnostic mode: D1-D6 (роль базується на tissue_location +
  lineage_hint + workup steps)

Output type — той самий `MDTOrchestrationResult` — але з diagnostic
context-specific reasons у `MDTRequiredRole.reason`.

---

## 4. Diagnostic-mode MDT rules (D1-D6)

| # | Тригер | Роль | Priority | trigger_type |
|---|---|---|---|---|
| D1 | `suspicion.lineage_hint` містить `lymphoma` | `hematologist` | `required` | `diagnosis_complexity` |
| D2 | Будь-який suspicion → потрібна біопсія | `pathologist` | `required` | `diagnosis_complexity` |
| D3 | `suspicion.tissue_locations` non-empty АБО imaging fields у findings | `radiologist` | `required` | `diagnosis_complexity` |
| D4 | `suspicion.lineage_hint` ∈ {`solid_tumor_*`, generic carcinoma з surgical-relevant локалізацією} | `surgical_oncologist` | `recommended` | `treatment_domain` |
| D5 | `suspicion.lineage_hint` містить `lymphoma` І history містить HCV/HBV (або не виключено) | `infectious_disease_hepatology` | `recommended` | `molecular_data` |
| D6 | ECOG ≥ 3 АБО `suspicion.presentation` містить B-симптоми + decompensation | `palliative_care` | `recommended` (early goals-of-care) | `palliative_need` |

**Ключова відмінність від treatment-mode:**
- `clinical_pharmacist` НЕ recommended (ще нема regimen)
- `radiation_oncologist` НЕ recommended (treatment-domain decision відкладений)
- `social_worker_case_manager` НЕ recommended за non-reimbursed drug
  (no drugs yet); але recommended якщо `suspicion.expected_workup_cost_uah_estimate`
  значний AND patient має фінансові обмеження (поза MVP)

---

## 5. Diagnostic-mode OpenQuestions (DQ1-DQ4)

| # | Тригер | Питання | owner_role | blocking |
|---|---|---|---|---|
| DQ1 | `suspicion.lineage_hint` містить `lymphoma` І `cd20_ihc_status` відсутній | "Який результат CD20 IHC після біопсії? Базис для choice anti-CD20." | `pathologist` | true |
| DQ2 | Lymphoma suspicion І HBV serology відсутня | "Серологія HBV до anti-CD20 — обов'язкова вже зараз." | `infectious_disease_hepatology` | true |
| DQ3 | Lymphoma suspicion І imaging staging відсутня | "Чи виконано PET/CT для staging?" | `radiologist` | true |
| DQ4 | Multiple working_hypotheses у suspicion (≥2) | "Який план диференціальної діагностики? Які молекулярні тести потрібні щоб обрати між {hypothesis A vs B}?" | `pathologist` | false |

OpenQuestions з treatment-mode (Q1-Q6) **не застосовуються** у
diagnostic — там немає Plan з regimen, до якого можна прив'язати
питання.

---

## 6. Engine API

### 6.1. Diagnostic mode entry point

```python
# knowledge_base/engine/diagnostic.py

def generate_diagnostic_brief(
    patient: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
    plan_version: int = 1,
    supersedes: str | None = None,
    revision_trigger: str | None = None,
) -> DiagnosticPlanResult:
    """Build a DiagnosticPlan for a patient WITHOUT confirmed histology.

    Hard rules:
    - patient.disease.id present AND .icd_o_3_morphology present →
      raise ValueError ("use generate_plan() for confirmed diagnosis")
    - patient.disease.suspicion absent → return empty result with warning
    """
    ...
```

### 6.2. MDT Orchestrator dispatch

```python
def orchestrate_mdt(
    patient: dict,
    plan_or_diagnostic: PlanResult | DiagnosticPlanResult,
    kb_root: Path | str = "...",
) -> MDTOrchestrationResult:
    """Detects mode by isinstance and applies the correct rule set."""
```

### 6.3. CLI dispatch

```bash
python -m knowledge_base.engine.cli patient.json              # auto-detect
python -m knowledge_base.engine.cli patient.json --diagnostic  # force
python -m knowledge_base.engine.cli patient.json --mdt         # MDT brief on top
```

Auto-detection rule: patient.disease has `id` чи `icd_o_3_morphology`
→ treatment mode. Інакше якщо є `suspicion` → diagnostic mode.
Інакше → error "patient profile has neither confirmed diagnosis nor
suspicion".

### 6.4. CLI banner — DIAGNOSTIC PHASE

Diagnostic-mode output **обов'язково починається** з:

```
=========================================================
  DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE
  Histology required before any therapy discussion.
=========================================================
```

Це механічний guard проти automation bias (CHARTER §15.2 C6).

---

## 7. Що залишається ОДНАКОВИМ для двох modes

- `MDTOrchestrationResult` shape (той самий dataclass)
- `ProvenanceEvent` shape (те саме provenance.py)
- FDA Criterion 4 fields у output (intended_use, hcp_user_specification, …)
- Source citations
- Audit trail / version chain (supersedes/superseded_by — реалізація у §7.1)
- Termination criterion: коли histology підтверджено →
  diagnostic-mode `DiagnosticPlan` стає `superseded_by` treatment-mode
  `Plan` (формальна transition; supersedes-link перетинає mode boundary)

### 7.1. Revisions — закриття step 5 з інфографіки

`knowledge_base/engine/revisions.py` містить
`revise_plan(updated_patient, previous, revision_trigger, kb_root)`,
що повертає **`(previous_with_superseded_by_set, new_result)`** — обидві
сторони supersedes-chain. Попередній результат **не мутується** —
повертається deep copy з заповненим `superseded_by`.

**Три легальні переходи** (auto-detect зі shapes):

| Previous | Updated patient | Transition | New |
|---|---|---|---|
| `DiagnosticPlan` vN | suspicion-only | `diagnostic → diagnostic` | `DiagnosticPlan` v(N+1) |
| `DiagnosticPlan` vN | confirmed `disease.id` | `diagnostic → treatment` | `Plan` v1 (перший treatment) |
| `Plan` vN | confirmed `disease.id` | `treatment → treatment` | `Plan` v(N+1) |

**Заборонений перехід:**

| `Plan` vN | suspicion-only (no `.id`) | `treatment → diagnostic` | **`ValueError`** — CHARTER §15.2 C7 |

Сенс: якщо вже є treatment Plan, відкат до diagnostic не дозволений
автоматично — це знаменує клінічну невизначеність, що потребує
окремого decision (наприклад нова первинна підозра — створи
**окремий** новий `DiagnosticPlan` без revision-link).

**Provenance:** новий plan отримує `modified` ProvenanceEvent у
`trace`: `summary = "Plan revised from PREV_ID (trigger: ...). This
is version N of patient X."` Audit trail завжди показує **звідки**
прийшла нова версія.

**CLI:** `--revise PREV.json --revision-trigger "biopsy 2026-05-10 →
DLBCL confirmed"`. PREV.json — це попередній output `--json-output`
від попереднього run.

**Persistence:** як і раніше, plan instances не у public KB —
лежать у `patient_plans/<patient_id>/v<N>.{yaml,json}` (gitignored
per CHARTER §9.3). Revisions тільки **готують** новий артефакт;
зберігати — задача caller.

---

## 8. Розширення (не у MVP)

- `simulate_plan_for_hypothesis(patient, hypothesis_disease_id)` —
  показати що було б у treatment plan ЯКЩО diagnosis підтвердиться
  як hypothesis Y. Strict marking "HYPOTHETICAL — not for clinical
  decision".
- DiagnosticPlan → treatment Plan transition automation: коли
  pathology report додано і `disease.id` resolved, автоматично
  generate_plan() з previous DiagnosticPlan як `supersedes`.
- Цінова оцінка workup-кошику (НСЗУ vs out-of-pocket) для
  патієнтського financial planning.
- Відстеження timeline: "минуло 7 з очікуваних 14 днів workup,
  все ще нема histology" → escalation to MDT.

---

## 9. Зміни у цьому документі

| Версія | Дата | Зміни |
|---|---|---|
| v0.1 | 2026-04-25 | Початковий MVP-spec; diagnostic mode з 1 seed workup (lymphoma); D1-D6 + DQ1-DQ4 правила; hard rule "no treatment without histology". |
