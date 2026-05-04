# Skill-Oriented Architecture Specification

**Проєкт:** OpenOnco
**Документ:** Skill-Oriented Architecture — MDT roles as clinically-verified skills
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з Clinical Co-Leads. Не запускає refactor —
лише формалізує модель.
**Попередні документи:** CHARTER.md (особливо §1, §6, §8.3, §15),
MDT_ORCHESTRATOR_SPEC.md, DIAGNOSTIC_MDT_SPEC.md,
WORKUP_METHODOLOGY_SPEC.md.

---

## Мета документа

Зафіксувати mental model, який вже **implicit** у нашій архітектурі і
зробити його **explicit** як direction для подальшого розвитку.

**Теза:** профільний лікар у MDT (гематолог, патолог, радіолог тощо) —
це по суті **clinically-verified skill**, який:

1. Приймає **input** = patient profile + поточні плани/висновки
2. Має **deterministic behavior** = набір правил коли його залучати +
   що він зазвичай запитує з KB + які питання адресує іншим скілам
3. Verified = пройшов CHARTER §6.1 two-reviewer merge клінічними
   co-leads (тому він "clinically-verified")
4. **Output** = два типи запитів:
   - до **shared knowledge base** (Test catalog, Source citations,
     Indication / Workup attributes)
   - до **інших skills** (відкриті питання `OpenQuestion.owner_role`)

Цей документ описує модель, її обмеження, і запропонований шлях
рефакторингу `mdt_orchestrator.py` під per-skill modules.

---

## 1. Принципи

### 1.1. Skill ≠ autonomous agent

Skill — це **declarative codification** of clinical patterns
(коли залучати → що запитати → що передати далі). Це **не**
autonomous reasoning agent. Skills:

- НЕ містять LLM (CHARTER §8.3)
- НЕ роблять inter-agent message-passing у real time (немає event loop,
  немає queue, немає async)
- НЕ "думають" — тільки **матчать input проти заздалегідь верифікованих
  rules**

Якщо хтось з контрибуторів запропонує "давайте додамо LLM-based
hematologist skill що чате з pathologist skill" — це автоматично
порушує:
- CHARTER §8.3 (LLM не клінічний decision-maker)
- CHARTER §15.2 C5 (sources must be established) — autonomous LLM
  output не є established source
- FDA non-device CDS Criterion 4 — HCP не може незалежно review
  basis опкої LLM reasoning chain

**Hard rule:** skill modules — pure Python rule code + KB content
references. Жодного LLM call inside `skills/`.

### 1.2. Skill ≠ replacement of real specialist

Skill emits "потрібен патолог + ось питання що його чекають". Реальний
**патолог відповідає** на питання — його judgment не replicated.

Скіл — це **scaffolding for the doctor's question**, не **the doctor's
answer**.

Це core thesis MDT Orchestrator (`MDT_ORCHESTRATOR_SPEC §1.2`):
- system визначає team composition + open questions + provenance
- system НЕ дає клінічних відповідей
- skill-orient framing цього не змінює — воно посилює explicit-ність

### 1.3. Skill = unit of clinical responsibility

Ключова перевага per-skill modules — **independent клінічний review**.

Коли Reviewer A (онкогематолог) має підписати клінічний контент, зараз
вона/він читає 1000-рядковий `mdt_orchestrator.py` де R1-R9 + D1-D6 +
escalation rules + дедуп +data quality + provenance — все змішане.

Якщо переходимо до per-skill modules:
- Reviewer A читає тільки `skills/hematologist.py` (≤200 рядків)
- Що скіл триггерить, що питає, що пере-передає далі — все локально
- Підпис is meaningful, бо обсяг scoping clear

CHARTER §6.1 process стає operationally практичним замість evident-only.

---

## 2. Skill protocol

### 2.1. Pydantic / dataclass shape (proposed)

```python
# knowledge_base/skills/base.py

from typing import Protocol, runtime_checkable

@runtime_checkable
class Skill(Protocol):
    """A clinically-verified MDT skill — declarative, deterministic.

    Skill instances are NOT shared mutable state. Each engine call
    instantiates skills fresh from per-module entries, applies them
    in deterministic order, returns role recommendations + queries.
    """

    role_id: str           # canonical role catalog entry
    role_name: str         # UA display name
    domain: str            # "hematology" / "solid_tumor" / "neuro_oncology" / ...

    def applies_to(self, ctx: SkillContext) -> bool:
        """When this skill should fire for the given patient + plan
        context. Pure function of inputs. Deterministic."""

    def priority(self, ctx: SkillContext) -> Literal["required", "recommended", "optional"]:
        """Initial priority if applies_to() returned True. Can be
        escalated by other rules (e.g., RedFlag-driven escalation
        per MDT_ORCHESTRATOR_SPEC §3-Esc)."""

    def reason(self, ctx: SkillContext) -> str:
        """UA-language clinical justification for the role
        recommendation. Cite-able by clinicians."""

    def kb_queries(self, ctx: SkillContext) -> list[KBQuery]:
        """What this skill 'knows to look up' from the shared knowledge
        base — Test IDs, Source IDs, IHC panel components, etc.
        Surfaces in MDT brief як "this role would consult these KB items"."""

    def inter_skill_queries(self, ctx: SkillContext) -> list[OpenQuestion]:
        """OpenQuestions this skill raises for OTHER skills.
        Already exists в `mdt_orchestrator._apply_open_question_rules` —
        skill-paradigm just reorganizes by owner."""

    def linked_findings(self, ctx: SkillContext) -> list[str]:
        """Profile fields / biomarker IDs / RedFlag IDs that triggered
        this skill. Surfaces у MDTRequiredRole.linked_findings."""
```

`SkillContext` — read-only struct з patient, current plan/diagnostic
brief, loaded entities, fired RedFlags. Skill methods НЕ mutate
context (deterministic).

`KBQuery` — pointer у KB:
```python
@dataclass
class KBQuery:
    target_type: Literal["test", "source", "biomarker", "indication", "regimen", ...]
    target_id: str
    relevance: str  # UA-language: "for staging", "for prognostic risk", etc.
```

### 2.2. Engine integration

Existing `mdt_orchestrator.orchestrate_mdt()` стає dispatcher:

```python
def orchestrate_mdt(patient, plan_or_diagnostic, kb_root):
    ctx = build_skill_context(patient, plan_or_diagnostic, kb_root)
    skills = load_all_skills()  # imports skills/*.py modules

    roles, kb_query_log, inter_skill_qs = [], [], []
    for skill in skills:
        if not skill.applies_to(ctx):
            continue
        roles.append(MDTRequiredRole(
            role_id=skill.role_id,
            role_name=skill.role_name,
            reason=skill.reason(ctx),
            priority=skill.priority(ctx),
            linked_findings=skill.linked_findings(ctx),
        ))
        kb_query_log.extend(skill.kb_queries(ctx))
        inter_skill_qs.extend(skill.inter_skill_queries(ctx))

    # then existing dedup + escalation + provenance logic
    # (RedFlag-driven escalation залишається у orchestrator — крос-скіл concern)
    ...
```

Behavior — ідентичний сьогоднішньому output, але організація per-domain.

---

## 3. Запропонований skills/ layout

Layout проектується під **~60-skill horizon** (повний oncology MDT) —
з достатнім structure щоб не перетворитись на flat-folder pile, але без
over-engineering (≤2 рівнів вкладеності).

```
knowledge_base/skills/
  __init__.py            # registry + load_all_skills()
  base.py                # Skill protocol, SkillContext, KBQuery dataclasses
  _helpers.py            # SimpleSkill base for trivial role+lineage rules
  registry.py            # auto-discovery of skills/<domain>/<role>.py

  shared/                # domain-agnostic; reused across diseases
    __init__.py
    pathologist.py       # generic pathologist (deferred to subspecialty якщо є)
    radiologist.py       # generic; subspecialties у sub-modules якщо потрібно
    clinical_pharmacist.py
    nurse_navigator.py
    primary_care.py
    research_coordinator.py
    patient_advocate.py

  hematology/            # ~6-8 skills
    __init__.py
    hematologist.py
    hematopathologist.py             # subspecialty pathology
    transplant_hematologist.py       # alloHSCT / autoHSCT
    coagulation_specialist.py        # bleeding/clotting
    transfusion_medicine.py          # blood bank, plasma exchange
    infectious_disease_hepatology.py # HCV/HBV/HIV-driven heme

  solid_tumor/           # future, ~10-12 skills
    __init__.py
    medical_oncologist.py
    surgical_oncologist.py           # generic
    breast_oncology.py               # combined surgical+medical breast
    gi_oncology.py
    thoracic_oncology.py
    gyn_oncology.py
    uro_oncology.py
    neuro_oncology.py
    head_and_neck_oncology.py
    sarcoma_oncology.py
    dermatologic_oncology.py         # melanoma + non-melanoma

  radiation/             # ~3 skills
    __init__.py
    radiation_oncologist.py          # general
    radiation_brachytherapy.py
    radiation_proton.py

  molecular/             # ~3 skills
    __init__.py
    molecular_geneticist.py
    pharmacogenomics.py              # PGx — drug metabolism polymorphisms
    germline_genetics_counselor.py   # BRCA, Lynch, Li-Fraumeni

  imaging/               # ~4 skills (subspecialty radiology)
    __init__.py
    radiologist_neuro.py
    radiologist_thoracic.py
    radiologist_msk.py               # musculoskeletal — критично для sarcoma
    nuclear_medicine.py              # PET interpretation, theranostics

  supportive/            # ~7 skills
    __init__.py
    palliative_care.py
    pain_specialist.py
    nutritionist.py
    physical_therapist.py
    psychologist.py
    psychiatrist.py                  # окремо від psychologist (medication management)
    social_worker_case_manager.py
    spiritual_care.py
```

**Принципи layout:**
- 8 top-level domain folders + `shared/` — clinical mental-map alignment
- `shared/` — domain-agnostic (rendering pipeline не імпортує доменні)
- Auto-discovery: `registry.py` глибує `skills/**/*.py`, collects Skill-protocol-conforming exports
- One file per (domain, role) — clinical review scope = one file
- Subspecialty separation тільки коли rules відрізняються істотно
  (наприклад radiologist_neuro vs radiologist_msk — різні KB queries)
- **Maximum nesting: 2 levels** (`skills/<domain>/<role>.py`). Глибше —
  ознака over-engineering.

### 3.1. Sizing horizon

| Horizon | Active skills | Що додаємо | When |
|---|---|---|---|
| **Сьогодні (HCV-MZL focus)** | ~7 active | (з 13 у `_ROLE_CATALOG`; решта catalog-only) | done |
| **MVP refactor** | **12-15** | Extract існуючі rules + 2-3 нові: hematopath, transplant_hematologist, nurse_navigator | next 1-3 commits |
| **Повна гематологія** | **~18-20** | + coag specialist, transfusion medicine, pain, окремий psychiatrist | 6 міс |
| **+ Solid tumors (CHARTER §3 future)** | **~35-40** | 10 organ-specific oncology skills + pharmacogenomics + germline counselor | 12-18 міс |
| **Comprehensive** | **~50-60** | + subspecialty radiology + radiation modalities + supportive expansions + ops/coordination | 24+ міс |

**Sanity check:** layout (§3) витримує 60-skill горизонт без re-architecting.
Поточний 1000-рядковий моноліт — **не витримує**. Refactor на skills/ —
**not optional** для scope expansion past hematology.

### 3.2. SimpleSkill helper for trivial cases

Спостереження: **~80% skills будуть однорядкові** — "коли disease lineage
∈ {X, Y, Z} → recommend role R з reason 'standard MDT participant for ...'".
Повний `Skill` protocol implementation — overkill для них.

Helper у `skills/_helpers.py`:

```python
@dataclass
class SimpleRoleSkill:
    """Single-rule skill: applies if disease lineage matches a fixed set.
    Conforms to Skill protocol via `applies_to`/`priority`/`reason` impl."""

    role_id: str
    role_name: str
    domain: str
    lineage_match: list[str]              # set of lineage_hints; OR-match
    presentation_keywords: list[str] = field(default_factory=list)
    priority_value: Priority = "recommended"
    reason_template: str = "Standard MDT participant для {lineage}."
    kb_query_templates: list[KBQuery] = field(default_factory=list)
    applies_in_modes: set[str] = field(default_factory=lambda: {"diagnostic", "treatment"})
    sources: list[str] = field(default_factory=list)

    def applies_to(self, ctx) -> bool: ...     # standard match
    def priority(self, ctx) -> Priority: ...   # returns priority_value
    def reason(self, ctx) -> str: ...          # formatted reason_template
    def kb_queries(self, ctx): ...             # returns kb_query_templates
    def inter_skill_queries(self, ctx): ...    # default: []
    def linked_findings(self, ctx): ...        # disease_id from ctx
```

Тоді 80% skills декларуються в один step:

```python
# skills/hematology/transplant_hematologist.py
SKILL = SimpleRoleSkill(
    role_id="transplant_hematologist",
    role_name="Гематолог-трансплантолог",
    domain="hematology",
    lineage_match=["aml", "all", "mds_high_risk", "mm_transplant_eligible"],
    priority_value="recommended",
    reason_template="alloHSCT/autoHSCT candidacy assessment для {lineage}.",
    sources=["SRC-NCCN-AML-2025"],
)
```

20% складніших skills (hematologist з 4-rule trigger logic + RedFlag-driven
escalation) — повний Skill protocol implementation, ~80-150 рядків.

### 3.3. Skill versioning

Кожен skill module має:
- `__version__` (semver)
- `__last_reviewed__` (ISO date)
- `__reviewers__` (list of reviewer IDs після підпису)

При load — engine варніф warning якщо `last_reviewed > 6 місяців` per
CLINICAL_CONTENT_STANDARDS §9.1.

### 3.4. Skill testing convention

`tests/skills/test_<role>.py` per skill:
- `test_applies_to_lymphoma_suspicion` (positive case)
- `test_does_not_apply_to_solid_tumor` (negative case)
- `test_kb_queries_includes_expected_tests`
- `test_inter_skill_queries_owner_routing`

Per skill: 4-8 focused tests. 200-line test file max. Easy to maintain.

---

## 4. Hard rules (CHARTER alignment)

### 4.1. CHARTER §8.3 — LLM не клінічний decision-maker

Skills **не** import LLM clients. `skills/` directory має CI lint
правило: `import anthropic`, `import openai`, etc. — **fail build**.
LLM використання дозволене тільки у:
- `knowledge_base/ingestion/moz_extractor.py` (PDF extraction with
  human verification per CHARTER §8.1)
- `legacy/` (archived autoresearch — не в активному коді)

### 4.2. CHARTER §15.2 C5 — sources must be established

Кожен skill module має `__sources__: list[str]` — IDs of Source
entities що підтверджують **кожен rule** у скілі. CI gate: skill
without `__sources__` (or with empty list) — fail merge.

### 4.3. CHARTER §15.2 C6 — automation bias mitigation

Skill output **NEVER** включає "system says X is true". Завжди:
- Role recommendation = "this role should review"
- KB query = "this role would consult these references"
- Inter-skill query = "this question awaits answer from role Y"

Render layer (existing) вже відображає це коректно через
MDTOrchestrationResult — skill refactor просто перенумеровує
**де** rules живуть, не **що** вони видають.

### 4.4. CHARTER §15.2 C7 — diagnostic vs treatment mode

Skills повинні оголошувати applicability в кожному mode:
```python
class HematologistSkill:
    applies_in_modes: set[str] = {"diagnostic", "treatment"}
```

`infectious_disease_hepatology` skill triggers у diagnostic mode на
suspicion рівні (HCV/HBV unresolved); у treatment mode — на confirmed
HCV+ regimen. Один skill, two modes — `applies_to(ctx)` бачить
`ctx.mode` і відповідно reasons differ.

---

## 5. Refactor plan (deferred — не виконується у цьому commit)

Цей spec **зараз** — лише формалізація моделі. Refactor — окремий
workstream після clarification з Clinical Co-Leads.

### Phase 1 — Foundation (1 commit)
- `knowledge_base/skills/base.py` — Skill protocol, SkillContext,
  KBQuery dataclasses
- `knowledge_base/skills/registry.py` — auto-discovery + load_all_skills
- Tests for Skill protocol contract

### Phase 2 — Migrate existing rules to skill modules (1-2 commits)
- Extract R1 (hematologist), R2 (infectious_disease_hepatology),
  R3 (radiologist), R4 (pathologist), R5 (clinical_pharmacist),
  R6 (radiation_oncologist), R7 (social_worker_case_manager),
  R8 (palliative_care), R9 (molecular_geneticist) → per-skill modules
- Same for D1-D6 (diagnostic-mode rules)
- `mdt_orchestrator._apply_role_rules` стає простий dispatcher що
  iterates skills + collects results
- Existing tests should pass без modification (behavioral identity)

### Phase 3 — Per-skill independent tests (1 commit)
- `tests/skills/test_hematologist.py` etc.
- Demonstrates per-skill review scoping

### Phase 4 — CI lint + documentation (1 commit)
- CI rule: `skills/` cannot import LLM SDKs
- CI rule: each skill must have non-empty `__sources__`
- README sections: "How to add a new skill"

### Phase 5 — Skill versioning + audit (future)
- skill `__last_reviewed__` enforcement
- audit dashboard: skills overdue for re-review

**Acceptance criterion для cumulative refactor:** `pytest -q` проходить
після всіх 4 phases без regression. Behavioral output of `orchestrate_mdt`
identical to pre-refactor stdout/JSON for всіх існуючих тест-кейсів.

---

## 6. Що ця формалізація **не** змінює

- Existing KB content (Indications, Regimens, Tests, Workups, Sources) —
  той самий
- Engine for clinical decisions (Algorithm.decision_tree) — лишається
  declarative
- Plan / DiagnosticPlan / Revisions / Persistence — той самий
- FDA non-device positioning — тільки посилюється через explicit
  per-skill source citations
- LLM scope — той самий: extraction with human verification only
- Render layer (commit 192c818) — той самий output, але per-skill
  source provenance стає explicit у future render iterations

---

## 7. Що формалізація **робить можливим**

1. **Per-domain extension легше** — додати онколога-уролога = додати
   `skills/solid_tumor/medical_oncologist_uro.py` + клінічний review
   тільки цього файлу
2. **Independent клінічний review** — Reviewer A відкриває один файл,
   не 1000-рядковий orchestrator
3. **Skill-rule audit** — з аудитного запиту "чому цей патієнт отримав
   recommendation для радіолога?" → log instantly показує
   `skills/shared/radiologist.py:applies_to:line 42`
4. **Multi-version skill A/B testing** — eventually можна тримати
   `radiologist_v2.py` поряд з `radiologist.py`, дозволяти clinical
   leads порівнювати behavior на synthetic case-suite перед switching
5. **Reusable skill registry** — інші OpenOnco-like проекти можуть
   зрелити власні skills використовуючи той самий Skill protocol

---

## 8. Clinical Co-Lead questions

Перед refactor execution потрібен sign-off на:

1. **Skill domain partitioning** — пропоновано `hematology/`, `solid_tumor/`,
   `shared/`, `molecular/`. Узгоджується з вашою специальностнею
   ментальною мапою?
2. **Per-skill version aging policy** — `last_reviewed > 6 months` →
   warning, чи escalate до error на CI?
3. **Skill source citation depth** — перелік Source IDs на module level,
   чи per-rule (тоді richer audit)?
4. **Naming convention** — skill class names (`HematologistSkill`) vs
   functional names (`hematologist_skill`) vs neither (single
   module-level instance)?

Без цих рішень refactor буде під ризиком rework коли co-leads побачать
готову реалізацію.

---

## 9. Зміни у цьому документі

| Версія | Дата | Зміни |
|---|---|---|
| v0.1 | 2026-04-25 | Початковий MVP. Принципи (§1), Skill protocol (§2), Layout (§3), CHARTER alignment (§4), Refactor plan (§5), What this doesn't change / does enable (§6, §7), Co-Lead questions (§8). Refactor execution **deferred** — чекає на §8 sign-off. |
