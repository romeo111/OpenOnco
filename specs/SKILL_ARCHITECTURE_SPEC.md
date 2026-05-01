# Skill-Oriented Architecture Specification

**Project:** OpenOnco
**Document:** Skill-Oriented Architecture — MDT roles as clinically-verified skills
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads. Does not trigger a
refactor — only formalizes the model.
**Preceding documents:** CHARTER.md (especially §1, §6, §8.3, §15),
MDT_ORCHESTRATOR_SPEC.md, DIAGNOSTIC_MDT_SPEC.md,
WORKUP_METHODOLOGY_SPEC.md.

---

## Purpose of this document

To capture the mental model that is already **implicit** in our architecture
and make it **explicit** as a direction for future development.

**Thesis:** a specialist physician in an MDT (hematologist, pathologist,
radiologist, etc.) is essentially a **clinically-verified skill** that:

1. Accepts **input** = patient profile + current plans/conclusions
2. Has **deterministic behavior** = a set of rules for when to engage it +
   what it typically queries from the KB + which questions it addresses to
   other skills
3. Is verified = has passed CHARTER §6.1 two-reviewer merge by clinical
   co-leads (hence "clinically-verified")
4. Produces **output** = two types of queries:
   - to the **shared knowledge base** (Test catalog, Source citations,
     Indication / Workup attributes)
   - to **other skills** (open questions `OpenQuestion.owner_role`)

This document describes the model, its constraints, and the proposed path for
refactoring `mdt_orchestrator.py` into per-skill modules.

---

## 1. Principles

### 1.1. Skill ≠ autonomous agent

A skill is a **declarative codification** of clinical patterns
(when to engage → what to query → what to pass forward). It is **not**
an autonomous reasoning agent. Skills:

- Do NOT contain LLMs (CHARTER §8.3)
- Do NOT perform inter-agent message-passing in real time (no event loop,
  no queue, no async)
- Do NOT "think" — they only **match input against pre-verified rules**

If any contributor proposes "let's add an LLM-based hematologist skill
that chats with the pathologist skill" — this automatically violates:
- CHARTER §8.3 (LLM is not the clinical decision-maker)
- CHARTER §15.2 C5 (sources must be established) — autonomous LLM output
  is not an established source
- FDA non-device CDS Criterion 4 — an HCP cannot independently review the
  basis of any LLM reasoning chain

**Hard rule:** skill modules — pure Python rule code + KB content
references. No LLM calls inside `skills/`.

### 1.2. Skill ≠ replacement of a real specialist

A skill emits "a pathologist is needed + here are the questions awaiting
them." The real **pathologist answers** those questions — their judgment
is not replicated.

A skill is **scaffolding for the doctor's question**, not **the doctor's
answer**.

This is the core thesis of the MDT Orchestrator (`MDT_ORCHESTRATOR_SPEC §1.2`):
- The system determines team composition + open questions + provenance
- The system does NOT provide clinical answers
- The skill-oriented framing does not change this — it reinforces explicitness

### 1.3. Skill = unit of clinical responsibility

The key advantage of per-skill modules is **independent clinical review**.

When Reviewer A (a hemato-oncologist) must sign off on clinical content,
they currently read a 1,000-line `mdt_orchestrator.py` where R1-R9 + D1-D6 +
escalation rules + deduplication + data quality + provenance are all mixed
together.

When we move to per-skill modules:
- Reviewer A reads only `skills/hematologist.py` (≤200 lines)
- What the skill triggers, what it queries, what it passes forward — all local
- The sign-off is meaningful because the scope is clearly bounded

The CHARTER §6.1 process becomes operationally practical rather than
merely formal.

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
        """Ukrainian-language clinical justification for the role
        recommendation. Cite-able by clinicians."""

    def kb_queries(self, ctx: SkillContext) -> list[KBQuery]:
        """What this skill 'knows to look up' from the shared knowledge
        base — Test IDs, Source IDs, IHC panel components, etc.
        Surfaces in MDT brief as "this role would consult these KB items"."""

    def inter_skill_queries(self, ctx: SkillContext) -> list[OpenQuestion]:
        """OpenQuestions this skill raises for OTHER skills.
        Already exists in `mdt_orchestrator._apply_open_question_rules` —
        skill-paradigm just reorganizes by owner."""

    def linked_findings(self, ctx: SkillContext) -> list[str]:
        """Profile fields / biomarker IDs / RedFlag IDs that triggered
        this skill. Surfaces in MDTRequiredRole.linked_findings."""
```

`SkillContext` — a read-only struct containing the patient, the current
plan/diagnostic brief, loaded entities, and fired RedFlags. Skill methods
do NOT mutate context (deterministic).

`KBQuery` — a pointer into the KB:
```python
@dataclass
class KBQuery:
    target_type: Literal["test", "source", "biomarker", "indication", "regimen", ...]
    target_id: str
    relevance: str  # Ukrainian-language: "for staging", "for prognostic risk", etc.
```

### 2.2. Engine integration

The existing `mdt_orchestrator.orchestrate_mdt()` becomes a dispatcher:

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
    # (RedFlag-driven escalation stays in orchestrator — cross-skill concern)
    ...
```

Behavior is identical to today's output, but the organization is per-domain.

---

## 3. Proposed skills/ layout

The layout is designed for a **~60-skill horizon** (a complete oncology MDT) —
with enough structure to avoid a flat-folder pile, but without over-engineering
(≤2 levels of nesting).

```
knowledge_base/skills/
  __init__.py            # registry + load_all_skills()
  base.py                # Skill protocol, SkillContext, KBQuery dataclasses
  _helpers.py            # SimpleSkill base for trivial role+lineage rules
  registry.py            # auto-discovery of skills/<domain>/<role>.py

  shared/                # domain-agnostic; reused across diseases
    __init__.py
    pathologist.py       # generic pathologist (deferred to subspecialty if present)
    radiologist.py       # generic; subspecialties in sub-modules if needed
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
    radiologist_msk.py               # musculoskeletal — critical for sarcoma
    nuclear_medicine.py              # PET interpretation, theranostics

  supportive/            # ~7 skills
    __init__.py
    palliative_care.py
    pain_specialist.py
    nutritionist.py
    physical_therapist.py
    psychologist.py
    psychiatrist.py                  # separate from psychologist (medication management)
    social_worker_case_manager.py
    spiritual_care.py
```

**Layout principles:**
- 8 top-level domain folders + `shared/` — aligned with the clinical mental map
- `shared/` — domain-agnostic (the rendering pipeline does not import domain modules)
- Auto-discovery: `registry.py` globs `skills/**/*.py`, collects Skill-protocol-conforming exports
- One file per (domain, role) — clinical review scope = one file
- Subspecialty separation only when rules differ substantially
  (e.g., radiologist_neuro vs radiologist_msk — different KB queries)
- **Maximum nesting: 2 levels** (`skills/<domain>/<role>.py`). Deeper nesting
  is a sign of over-engineering.

### 3.1. Sizing horizon

| Horizon | Active skills | What we add | When |
|---|---|---|---|
| **Today (HCV-MZL focus)** | ~7 active | (from 13 in `_ROLE_CATALOG`; rest are catalog-only) | done |
| **MVP refactor** | **12-15** | Extract existing rules + 2-3 new: hematopath, transplant_hematologist, nurse_navigator | next 1-3 commits |
| **Full hematology** | **~18-20** | + coag specialist, transfusion medicine, pain, separate psychiatrist | 6 months |
| **+ Solid tumors (CHARTER §3 future)** | **~35-40** | 10 organ-specific oncology skills + pharmacogenomics + germline counselor | 12-18 months |
| **Comprehensive** | **~50-60** | + subspecialty radiology + radiation modalities + supportive expansions + ops/coordination | 24+ months |

**Sanity check:** the layout (§3) can sustain a 60-skill horizon without
re-architecting. The current 1,000-line monolith **cannot**. Refactoring
to skills/ is **not optional** for scope expansion past hematology.

### 3.2. SimpleSkill helper for trivial cases

Observation: **~80% of skills will be single-rule** — "when disease lineage
∈ {X, Y, Z} → recommend role R with reason 'standard MDT participant for ...'".
A full `Skill` protocol implementation is overkill for these.

Helper in `skills/_helpers.py`:

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
    reason_template: str = "Standard MDT participant for {lineage}."
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

80% of skills are then declared in one step:

```python
# skills/hematology/transplant_hematologist.py
SKILL = SimpleRoleSkill(
    role_id="transplant_hematologist",
    role_name="Transplant Hematologist",
    domain="hematology",
    lineage_match=["aml", "all", "mds_high_risk", "mm_transplant_eligible"],
    priority_value="recommended",
    reason_template="alloHSCT/autoHSCT candidacy assessment for {lineage}.",
    sources=["SRC-NCCN-AML-2025"],
)
```

The 20% of more complex skills (hematologist with 4-rule trigger logic +
RedFlag-driven escalation) use the full Skill protocol implementation,
~80-150 lines.

### 3.3. Skill versioning

Each skill module has:
- `__version__` (semver)
- `__last_reviewed__` (ISO date)
- `__reviewers__` (list of reviewer IDs after sign-off)

At load time — the engine emits a warning if `last_reviewed > 6 months`
per CLINICAL_CONTENT_STANDARDS §9.1.

### 3.4. Skill testing convention

`tests/skills/test_<role>.py` per skill:
- `test_applies_to_lymphoma_suspicion` (positive case)
- `test_does_not_apply_to_solid_tumor` (negative case)
- `test_kb_queries_includes_expected_tests`
- `test_inter_skill_queries_owner_routing`

Per skill: 4-8 focused tests. 200-line test file maximum. Easy to maintain.

---

## 4. Hard rules (CHARTER alignment)

### 4.1. CHARTER §8.3 — LLM is not the clinical decision-maker

Skills do **not** import LLM clients. The `skills/` directory has a CI lint
rule: `import anthropic`, `import openai`, etc. — **fail build**.
LLM usage is permitted only in:
- `knowledge_base/ingestion/moz_extractor.py` (PDF extraction with
  human verification per CHARTER §8.1)
- `legacy/` (archived autoresearch — not in active code)

### 4.2. CHARTER §15.2 C5 — sources must be established

Each skill module has `__sources__: list[str]` — IDs of Source entities
that support **each rule** in the skill. CI gate: a skill without
`__sources__` (or with an empty list) — fails merge.

### 4.3. CHARTER §15.2 C6 — automation bias mitigation

Skill output **NEVER** includes "system says X is true." Always:
- Role recommendation = "this role should review"
- KB query = "this role would consult these references"
- Inter-skill query = "this question awaits answer from role Y"

The render layer (existing) already represents this correctly through
MDTOrchestrationResult — the skill refactor simply reorganizes
**where** rules live, not **what** they produce.

### 4.4. CHARTER §15.2 C7 — diagnostic vs treatment mode

Skills must declare applicability in each mode:
```python
class HematologistSkill:
    applies_in_modes: set[str] = {"diagnostic", "treatment"}
```

The `infectious_disease_hepatology` skill triggers in diagnostic mode at the
suspicion level (HCV/HBV unresolved); in treatment mode — on a confirmed
HCV+ regimen. One skill, two modes — `applies_to(ctx)` reads `ctx.mode`
and the reasons differ accordingly.

---

## 5. Refactor plan (deferred — not executed in this commit)

This spec **at present** is only a formalization of the model. The refactor
is a separate workstream pending clarification from Clinical Co-Leads.

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
- `mdt_orchestrator._apply_role_rules` becomes a simple dispatcher that
  iterates skills + collects results
- Existing tests should pass without modification (behavioral identity)

### Phase 3 — Per-skill independent tests (1 commit)
- `tests/skills/test_hematologist.py` etc.
- Demonstrates per-skill review scoping

### Phase 4 — CI lint + documentation (1 commit)
- CI rule: `skills/` cannot import LLM SDKs
- CI rule: each skill must have non-empty `__sources__`
- README sections: "How to add a new skill"

### Phase 5 — Skill versioning + audit (future)
- Enforcement of skill `__last_reviewed__`
- Audit dashboard: skills overdue for re-review

**Acceptance criterion for the cumulative refactor:** `pytest -q` passes
after all 4 phases without regression. Behavioral output of `orchestrate_mdt`
is identical to pre-refactor stdout/JSON for all existing test cases.

---

## 6. What this formalization does **not** change

- Existing KB content (Indications, Regimens, Tests, Workups, Sources) —
  unchanged
- Engine for clinical decisions (Algorithm.decision_tree) — remains
  declarative
- Plan / DiagnosticPlan / Revisions / Persistence — unchanged
- FDA non-device positioning — only strengthened through explicit
  per-skill source citations
- LLM scope — unchanged: extraction with human verification only
- Render layer (commit 192c818) — same output, but per-skill source
  provenance becomes explicit in future render iterations

---

## 7. What this formalization **makes possible**

1. **Per-domain extension is easier** — adding a uro-oncologist means adding
   `skills/solid_tumor/medical_oncologist_uro.py` + clinical review of only
   that file
2. **Independent clinical review** — Reviewer A opens one file, not a
   1,000-line orchestrator
3. **Skill-rule audit** — given an audit query "why did this patient receive
   a recommendation for a radiologist?" → the log instantly shows
   `skills/shared/radiologist.py:applies_to:line 42`
4. **Multi-version skill A/B testing** — eventually, `radiologist_v2.py` can
   be kept alongside `radiologist.py`, allowing clinical leads to compare
   behavior on a synthetic case suite before switching
5. **Reusable skill registry** — other OpenOnco-like projects can register
   their own skills using the same Skill protocol

---

## 8. Clinical Co-Lead questions

The following require sign-off before the refactor is executed:

1. **Skill domain partitioning** — proposed: `hematology/`, `solid_tumor/`,
   `shared/`, `molecular/`. Does this align with your specialty mental map?
2. **Per-skill version aging policy** — `last_reviewed > 6 months` →
   warning, or escalate to a CI error?
3. **Skill source citation depth** — list of Source IDs at the module level,
   or per-rule (richer audit)?
4. **Naming convention** — skill class names (`HematologistSkill`) vs
   functional names (`hematologist_skill`) vs neither (single
   module-level instance)?

Without these decisions the refactor risks rework once co-leads see the
finished implementation.

---

## 9. Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-04-25 | Initial MVP. Principles (§1), Skill protocol (§2), Layout (§3), CHARTER alignment (§4), Refactor plan (§5), What this doesn't change / does enable (§6, §7), Co-Lead questions (§8). Refactor execution **deferred** — awaiting §8 sign-off. |
