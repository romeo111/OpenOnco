# §17 schema refactor: Solid-tumor extensions

**Stamp:** 2026-05-07-2200
**Source:** `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 (PROPOSAL since 2026-04-26)
**Blocking:** GI-2 wave Phase C (5 chunks — FLOT periop / CROSS phasing / definitive CRT / MIE / oligomet)
**Authority:** dev-mode autonomous per CLAUDE.md + memory `project_charter_dev_mode_exemptions.md` (CHARTER §6.1 two-reviewer signoff dev-mode-exempt during v0.1)

---

## 1. What §17 currently says

PROPOSAL identifies three solid-tumor patterns the schema cannot model today:

1. **Sequential phases in one line of therapy** (periop FLOT, CROSS) — `Indication.followed_by` means next-line, not next-phase-of-this-line
2. **Surgery as a treatment modality** (Whipple, esophagectomy, gastrectomy, hepatectomy) — no Surgery entity
3. **Radiation therapy** (CROSS 41.4 Gy / 23 fx, SCRT, SBRT, definitive CRT) — no RadiationCourse entity

Proposed entities (§17.1 sketch):
- `Surgery` model: id, names, type, intent enum, target_organ, applicable_diseases, operative_mortality_pct, common_complications, sources
- `RadiationCourse` model: id, names, total_dose_gy, fractions, fraction_size_gy, target_volume, schedule, concurrent_chemo_regimen (optional), intent enum, sources
- `Indication.phases: list[IndicationPhase]` — ordered list per indication, each entry has phase (neoadjuvant/surgery/adjuvant), type (chemotherapy/surgery/radiation/chemoradiation), regimen_id OR surgery_id OR radiation_id, cycles

Resolution path §17.4 (7 steps):
1. Clinical co-leads ratify
2. Pydantic schemas added
3. Loader referential integrity
4. Engine pass-through `phases` → PlanTrack.indication_data
5. Render phased-timeline section
6. Tests / golden fixtures
7. Re-stamp 5 GI diseases proposal_status partial → full

5 GI diseases currently at `metadata.proposal_status: partial` + `awaiting_proposal: "KNOWLEDGE_SCHEMA_SPECIFICATION.md §17 Solid-tumor extensions"`: gastric, esophageal, PDAC, HCC, CRC.

## 2. Design decisions

### 2.1 Folder layout for new content types

| Decision | Rationale |
|---|---|
| `knowledge_base/hosted/content/procedures/` for Surgery | Generic name in case future RT-guided / interventional procedures join. Plural matches existing `regimens/`, `indications/`, `biomarkers/`. |
| `knowledge_base/hosted/content/radiation_courses/` for RadiationCourse | Match existing folder naming convention (snake_case plural). |
| Filenames: `proc_<name>.yaml` and `rc_<trial-or-protocol>.yaml` | Match existing prefix conventions (`reg_`, `ind_`, `bma_`, `bio_`, `rf_`, `src_`, `algo_`, `dis_`, `drug_`). `proc_` for procedure (covers Surgery + future), `rc_` for radiation course. |

### 2.2 Pydantic schema layout

| File | Contents |
|---|---|
| `knowledge_base/schemas/surgery.py` | `Surgery` model + `SurgeryIntent` enum (curative / palliative / diagnostic / salvage) |
| `knowledge_base/schemas/radiation_course.py` | `RadiationCourse` model + `RadiationIntent` enum (neoadjuvant / definitive / adjuvant / palliative) |
| `knowledge_base/schemas/indication.py` (EDIT) | Add `phases: list[IndicationPhase] \| None`; `IndicationPhase` model nested or in same file |
| `knowledge_base/schemas/__init__.py` (EDIT) | Re-export new types |

`IndicationPhase` fields (per §17.1 sketch):
- `phase: IndicationPhaseStage` — enum: `neoadjuvant`, `surgery`, `adjuvant`, `induction`, `maintenance`, `definitive` (extension over §17.1 — definitive for unresectable CRT, induction/maintenance for sequential systemic)
- `type: IndicationPhaseType` — enum: `chemotherapy`, `surgery`, `radiation`, `chemoradiation`, `targeted_therapy`, `immunotherapy` (extension — clinical reality has more types than §17.1 lists)
- `regimen_id: str \| None` — foreign key to Regimen (one of regimen_id / surgery_id / radiation_id required)
- `surgery_id: str \| None` — foreign key to Surgery
- `radiation_id: str \| None` — foreign key to RadiationCourse
- `cycles: int \| None` — only for chemo/targeted/immune phases
- `duration_weeks: int \| None` — alternative to cycles for RT or surgical recovery
- Validator: exactly ONE of `regimen_id` / `surgery_id` / `radiation_id` must be non-null per phase

### 2.3 IntentOfTreatment enum (§17.1 didn't have a unified enum)

NOT introducing top-level `Indication.intent` field. Reasoning: the indication's intent is implicit from its `applicable_to.stage_requirements` and the phase composition. Adding redundant `intent:` on Indication risks drift. If future need arises (e.g., for engine routing or render), add then.

§17.1 sketch had `intent:` on Surgery (curative/palliative/diagnostic/salvage) and on RadiationCourse (neoadjuvant/definitive/adjuvant/palliative). Keep those as-is, scope-local. Different enums OK — surgical vs radiation intent vocabulary differs in practice.

### 2.4 Validation rules (loader)

New ref-integrity checks:
1. Every `phases[*].surgery_id` → Surgery entity exists (existing-pattern follows `bio_id`, `regimen_id`, etc.)
2. Every `phases[*].radiation_id` → RadiationCourse entity exists
3. Every `phases[*].regimen_id` → Regimen entity exists (existing rule, applies inside phases too)
4. Per-phase: exactly ONE of `regimen_id` / `surgery_id` / `radiation_id` non-null (Pydantic-level model_validator)
5. Phase ordering: `phase` value should make clinical sense in list order (e.g., neoadjuvant before surgery before adjuvant). Soft check (warning, not error) for v0.1.
6. Surgery referential: `Surgery.applicable_diseases` IDs → Disease entities exist
7. RadiationCourse: `concurrent_chemo_regimen` (optional) → Regimen entity exists if present

### 2.5 Migration approach

**No auto-migration.** Existing indications that imply phasing in `notes:` text (CROSS, FLOT, mFOLFIRINOX adjuvant) stay unchanged. They can be re-authored in Phase C chunks (C1 FLOT periop, C2 CROSS phasing, etc.) where phases are populated explicitly with full clinical review.

Adding `phases:` is opt-in. Indications without `phases:` continue to work as they do today.

### 2.6 Disease re-stamp policy

After schema lands, the `awaiting_proposal: "...§17..."` is no longer accurate (schema EXISTS). But the indications haven't been re-authored yet to populate phases.

Decision: **re-stamp `proposal_status: partial → full`** + **remove `awaiting_proposal` field** for 5 GI diseases. Reasoning:
- §17 was about schema absence, not indication population
- `partial` was a flag of "the schema can't model this disease's complexity yet" — now schema CAN, even if no indications have used it
- Phase C chunks populate phases. Diseases stay `full` regardless.
- Add a new disease-level field if re-stamp feels premature: `metadata.phasing_populated: false` until Phase C lands. Decided: not worth the bookkeeping; just re-stamp to `full`.

### 2.7 Engine + render: out of scope

§17.4 steps 4 (engine pass-through) and 5 (render phased-timeline) are deferred to Phase C readiness work. They're 1-line engine change + bigger UI work. Schema refactor lands without them; first periop indication (C1 FLOT) won't render with phased timeline yet, but the YAML structure will be queryable from `PlanTrack.indication_data.phases` if engine is touched. Deferred to keep this chunk scoped.

## 3. Workstream split

Single chunk: **SR-1 §17 schema ratification + implementation**.

- Spec text edits (§17 PROPOSAL → ratified)
- 2 new Pydantic schema files + edits to indication.py + __init__.py
- Validator updates (new entity types, new ref-integrity rules)
- Test fixtures + tests
- Re-stamp 5 GI disease YAMLs

Rationale: schemas without validator updates fail loader; validator without tests is unverified; spec without code is non-actionable. All tightly coupled. Single PR.

Estimated agent-hours: 2-3 hours (more than typical chunk-task because it's infrastructure work, not single-file content).

## 4. Files in scope

```
specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md                  [EDIT — §17 PROPOSAL → ratified]

knowledge_base/schemas/surgery.py                        [NEW]
knowledge_base/schemas/radiation_course.py               [NEW]
knowledge_base/schemas/indication.py                     [EDIT — add phases field]
knowledge_base/schemas/__init__.py                       [EDIT — re-export]

knowledge_base/validation/loader.py                      [EDIT — add Surgery + RadiationCourse loading + ref-integrity]
                                                         (or whichever module owns entity-loading; agent discovers)

knowledge_base/hosted/content/diseases/dis_gastric.yaml  [EDIT — proposal_status partial → full]
knowledge_base/hosted/content/diseases/dis_esophageal.yaml [EDIT — same]
knowledge_base/hosted/content/diseases/dis_pdac.yaml     [EDIT — same]
knowledge_base/hosted/content/diseases/dis_hcc.yaml      [EDIT — same]
knowledge_base/hosted/content/diseases/dis_crc.yaml      [EDIT — same]

tests/test_phases.py                                     [NEW — phase-validation accept/reject]
tests/test_surgery.py                                    [NEW — Surgery model accept/reject]
tests/test_radiation_course.py                           [NEW — RadiationCourse model accept/reject]
tests/fixtures/phased_indication.yaml                    [NEW — golden fixture]
tests/fixtures/surgery_whipple.yaml                      [NEW — golden fixture]
tests/fixtures/radiation_cross.yaml                      [NEW — golden fixture]
```

## 5. Acceptance criteria

- ✅ §17 spec text shows `Status: ratified 2026-05-07`, removes "PROPOSAL" prefix in heading, removes `(sketch — to be ratified)` qualifiers
- ✅ Pydantic schemas pass mypy/strict if applicable; field validators reject malformed phases (multiple foreign keys, invalid phase enum, etc.)
- ✅ Loader successfully discovers `procedures/` and `radiation_courses/` folders if present (empty folder OK; folders may not even exist yet — first Surgery / RadiationCourse files land in Phase C chunks)
- ✅ Validator: existing `validate_kb` (or whatever the canonical CLI is) on master must NOT regress. Pre-existing schema_errors_count = 91 (or current baseline) → unchanged
- ✅ All new tests pass; existing test suite passes
- ✅ 5 GI disease YAMLs flipped to `proposal_status: full`; `awaiting_proposal` field removed
- ✅ `git diff --stat origin/master..HEAD` matches §4 file list within ±2 files (allowing for minor agent discoveries)

## 6. Rejection criteria

- ANY existing indication breaks (regression — phases is opt-in, existing data must continue loading)
- ANY hosted KB content edit beyond the 5 disease re-stamps (e.g., agent gets tempted to author a sample Surgery file — STOP, that's Phase C scope)
- Engine/render layer touched (out of scope per §2.7)
- Schema fields invented beyond §17.1 sketch + §2.2 explicit extensions (induction/maintenance/definitive phase enum, targeted_therapy/immunotherapy phase type)
- 5 GI diseases left with `awaiting_proposal` field after re-stamp

## 7. Branch + chunk-id

- chunk-id: `schema-17-refactor-2026-05-07-2200`
- Branch: `feat/schema-17-refactor-2026-05-07-2200`
- (Note: `feat/` prefix, not `chunk/` — this is infrastructure not chunk-task content)
- Branch off: `origin/master`

## 8. Self-push policy

Per CLAUDE.md commit `3a60901b`: self-push authorized when all gates green:
- `validate_kb` ok=True, schema/ref errors NOT increased vs baseline
- Full pytest suite green (or pre-existing baseline failures verified unchanged)
- pre-commit hooks pass (if configured — they're not as of 2026-05-07; verified by W0 chunks)
- Branch is `feat/...`, not master
- No force-push, no `--no-verify`, no `git add -A/.`
