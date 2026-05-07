# Schema-refactor lessons (for future reference)

**Stamp:** 2026-05-07-2300
**Source:** §17 schema refactor (Surgery + RadiationCourse + Indication.phases) — see `docs/plans/schema_17_refactor_2026-05-07.md` for the executed work
**Audience:** future refactor sessions (orchestrator + agents) — read before planning the next schema-level change

---

## 1. What §17 refactored

Schema-level extension in v0.1 KB — modelling support for three solid-tumor patterns that were previously unmodellable:

1. **Sequential phases within one line of therapy** (periop FLOT: neoadj → surgery → adj)
2. **Surgery as a treatment modality** (Whipple, esophagectomy, etc.)
3. **Radiation as concurrent / sequential treatment** (CROSS 41.4 Gy, SBRT, definitive CRT)

Status before refactor: `KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 was open PROPOSAL since 2026-04-26; 5 GI diseases shipped at `proposal_status: partial` with `awaiting_proposal: §17`. Phase C of GI-2 wave (5 chunks) was blocked.

## 2. Architectural decisions worth preserving

### 2.1 Backward-compat first

| Choice | Rationale |
|---|---|
| `Indication.phases` is **opt-in** (Optional / nullable) | Existing indications without phases continue loading unchanged. No regression risk. |
| **No auto-migration script** | Existing phasing-implied indications (CROSS, FLOT) stay as free-text `notes:` until they're re-authored in their own focused chunks (Phase C). Auto-migration on clinical content = high blast-radius. |
| Schema additions, not replacements | New entity types (Surgery, RadiationCourse) added; existing models untouched. |

**For the next refactor:** if a schema change can be made additive + opt-in, do that. Migration of hosted KB content should always be a separate dedicated chunk, never bundled with the schema change.

### 2.2 Folder + filename conventions

| Decision | Pattern |
|---|---|
| Folder names | snake_case plural — `procedures/`, `radiation_courses/`, `regimens/`, `indications/`, `biomarkers/` |
| Filename prefix | three-letter abbreviation + underscore — `proc_*.yaml`, `rc_*.yaml`, `reg_*.yaml`, `ind_*.yaml`, `bma_*.yaml`, `bio_*.yaml`, `rf_*.yaml`, `src_*.yaml`, `algo_*.yaml`, `dis_*.yaml`, `drug_*.yaml` |

**For the next refactor:** new content types must follow this convention. Don't introduce singular-noun folders or non-prefixed filenames — they break grep / glob patterns and `upsert_contributions.py` PREFIX_TO_DIR routing.

### 2.3 Enum / type design

| Choice | Rationale |
|---|---|
| Domain-specific intent enums | `SurgeryIntent` (curative / palliative / diagnostic / salvage) + `RadiationIntent` (neoadjuvant / definitive / adjuvant / palliative) — separate enums, vocabularies don't match in clinical practice |
| **No top-level `Indication.intent` field** | Intent implicit from `applicable_to.stage_requirements` + phase composition. Adding a redundant `intent:` risks drift between the field and the implied intent. |
| Phase enum extended beyond original sketch | Sketch had only `neoadjuvant / surgery / adjuvant` and `chemotherapy / surgery / radiation / chemoradiation`. Real clinical reality needed `induction / maintenance / definitive` (sequential systemic, unresectable CRT) + `targeted_therapy / immunotherapy` phase types. |

**For the next refactor:** when designing enums, audit existing clinical content first to surface vocabulary that the original sketch missed. Original §17.1 was sufficient for FLOT/CROSS but missed unresectable CRT and modern targeted/IO sequencing.

### 2.4 Foreign-key XOR pattern

`IndicationPhase` requires exactly one of `regimen_id` / `surgery_id` / `radiation_id` non-null. Implemented via Pydantic v2 `@model_validator(mode='after')` returning `self` after raising on multi-FK or zero-FK cases.

**For the next refactor:** XOR rules for foreign keys are a recurring pattern. Use `model_validator(mode='after')` not `field_validator`, because the rule spans multiple fields. Document the rule in a docstring on the model class.

### 2.5 Engine + render hooks deferred

§17.4 originally listed 7 steps including engine pass-through (step 4) + render phased-timeline (step 5). We deferred those to a separate "Phase C readiness" workstream. Schema landed without them.

**For the next refactor:** schema can land without engine/render integration. Engine reads new fields lazily; render shows them when ready. This reduces single-PR blast radius. Don't bundle UI work with schema work unless absolutely tightly coupled.

## 3. Process patterns that worked

### 3.1 Planning doc with explicit decisions BEFORE dispatch

`docs/plans/schema_17_refactor_2026-05-07.md` was authored as a comprehensive design doc with:
- §1 What §17 currently says (verbatim summary of existing PROPOSAL)
- §2 Design decisions with explicit choice + rationale per item
- §3 Workstream split (single chunk, with justification)
- §4 Files in scope (explicit list, ±2 tolerance)
- §5 Acceptance criteria
- §6 Rejection criteria
- §7 Branch + chunk-id
- §8 Self-push policy

**For the next refactor:** invest 30 min in a planning doc before dispatching agents. Catches design defects early. Acceptance + rejection criteria pairs guard against scope creep.

### 3.2 Single coherent chunk for tightly-coupled changes

Schema + validator + tests + 5 disease re-stamps + spec text → one PR. Not split into "schema then validator then tests".

**Reason:** schema without validator updates fails loader. Validator without tests is unverified. Spec without code is non-actionable. They're tightly coupled — split causes broken intermediate states.

**For the next refactor:** if changes can't compile / pass tests independently, they must land together. Split only when each PR is independently green.

### 3.3 Branch prefix `feat/...` for infrastructure

Chunk-task content uses `chunk/...` prefix. Infrastructure refactor uses `feat/...`. Distinct prefix signals different review expectations + different self-push gates.

### 3.4 Authority basis written explicitly

The §17 chunk's issue body cited `CLAUDE.md` + memory `project_charter_dev_mode_exemptions.md` to justify dev-mode autonomous execution (CHARTER §6.1 two-reviewer signoff exempt during v0.1). Without this, agent might over-pause for "clinical signoff" that isn't needed in v0.1.

**For the next refactor:** if doing autonomous work that the agent might confuse with content-requiring-signoff, state the authority basis clearly in the issue body.

## 4. Gotchas (from GI-2 wave + earlier sessions — apply to all refactors)

### 4.1 Schema-discovery FIRST

**Mandatory step in every chunk-task:** read `schemas/*.py` + 2-3 existing entity templates BEFORE writing anything. Don't trust speculative field names from planning docs.

GI-2 wave produced 5 spec defects in plans (HER2-low/positive confusion, OMEC-1 year, schema fields `kind` / `clinical_trial_registration`, Kim PMID, paper description) — all caught by agents during schema-discovery + canonical-citation verification.

**For the next refactor:** explicitly bake schema-discovery as Step 1 of agent prompts.

### 4.2 DO NOT invent fields

If a needed field doesn't exist in the canonical Pydantic schema:
- Check if existing convention covers it (search existing files via grep)
- Use `extra='allow'` Pydantic config to add stratum/region-specific outcomes via flexible dict (B1 lesson — `ExpectedOutcomes.extra='allow'` for HR stratification)
- Free-text in `notes:` / `description:` if no structural fit
- DO NOT invent new top-level fields — that fragments the schema

### 4.3 Pre-existing baseline drift

Schema_errors_count and ref_errors_count in master drift over time. Agents must capture baseline pre-edit and verify post-edit is `<=` baseline, not `== 0`.

Baseline as of 2026-05-07 evening (post-GI-2 Phase A+D): 91 schema errors / 354 ref errors (some validators) / 216 ref errors (others, with different strict-mode flags). Different validators report different counts.

**For the next refactor:** the canonical baseline number depends on which validator command + flags are used. Capture both pre-edit AND post-edit with the SAME command.

### 4.4 Hyphenation inconsistency in source IDs

KB has mixed conventions — `SRC-CHECKMATE-577-KELLY-2021` (hyphenated) vs `SRC-CHECKMATE648-DOKI-2022` / `SRC-KEYNOTE190-SUN-2021` (non-hyphenated). Issue #400 tracks renormalisation backlog.

**For the next refactor:** when introducing new ID patterns, use hyphenated form. Verify against KB before declaring a "new" ID — collisions waste agent restart cycles (W0-2 lost ~20 min to a CHECKMATE-648 collision).

### 4.5 Pre-commit hooks not configured in repo

Multiple agents reported `.pre-commit-config.yaml` does not exist; `pre-commit run --all-files` is a no-op in this repo.

**For the next refactor:** quality gate reduces to `validate_kb` + `pytest`. Don't rely on pre-commit hook coverage. If you want pre-commit, that's a separate infrastructure chunk.

### 4.6 Pytest baseline failures

`test_seed_loads_without_errors` and a regimen-schema-error pattern in `regimens/reg_bep_gct.yaml`, `reg_cabazitaxel_mcrpc.yaml`, etc. fail on baseline `origin/master`. They're pre-existing, not introduced by Phase A or §17.

**For the next refactor:** verify pytest fail count is **identical pre/post**, not zero. Baseline failures are NOT regressions.

### 4.7 Worktree isolation is non-negotiable

Per CLAUDE.md incident #241: agents NEVER `cd` to user's main tree. Always work in `.claude/worktrees/agent-*/`. Pre-flight `pwd` check is mandatory.

### 4.8 Self-push when all gates green

Per CLAUDE.md commit `3a60901b`: agent self-pushes feature branches when all quality gates pass. No need for orchestrator approval. Force-push, `--no-verify`, master direct still banned.

## 5. Anti-patterns to avoid

### 5.1 Bundling unrelated changes in one chunk

Don't bundle schema refactor with unrelated content additions. The §17 chunk did NOT add any sample Surgery / RadiationCourse content (those land in Phase C). Keeping infrastructure separate from clinical content reduces review burden.

### 5.2 Auto-migration of hosted KB

Don't write migration scripts that touch `knowledge_base/hosted/content/*.yaml` to populate new schema fields. Make new fields opt-in. Re-author existing content in dedicated chunks with full clinical review.

### 5.3 Renaming canonical fields

Avoid renaming. The KB has 2-3K entities; rename touches every citation. If naming is inconsistent (hyphenation), defer to a renormalisation chunk that does NOTHING ELSE.

### 5.4 Silent scope creep

When agent discovers an issue beyond chunk scope (e.g. English-string predicates that never fire, found by D1 agent in PR #423): flag in PR body, don't fix in same chunk. Out-of-scope fixes inflate review burden + risk regression.

## 6. Authority levels (for the next refactor — who does what)

| Action | Authority required |
|---|---|
| Schema additive (new model, new optional field) | Dev-mode autonomous (CHARTER §6.1 exempt v0.1) |
| Schema breaking (rename / remove / type change) | Major version bump per spec §18; CHANGELOG-SCHEMA.md entry |
| New entity type (e.g. Surgery) | Dev-mode autonomous if additive |
| Validator referential-integrity new rule | Dev-mode autonomous |
| Migration of hosted KB content | Separate chunk; clinical signoff per CHARTER §6.1 (dev-mode-exempt v0.1 BUT prefer to co-locate with content-author chunks anyway) |
| Engine routing change | Dev-mode autonomous |
| Render UI change | Dev-mode autonomous |
| New folder under `knowledge_base/hosted/content/` | Mention in spec §2 / `KNOWLEDGE_SCHEMA_SPECIFICATION.md` if new entity type |
| spec ratification | Dev-mode autonomous v0.1; v1.0+ requires §6 governance |

## 7. Index of related docs

- `docs/plans/schema_17_refactor_2026-05-07.md` — §17 executed work
- `docs/plans/gi2_long_tail_followups_2026-05-07.md` — long-tail backlog
- `docs/plans/gi2_wave_gastric_esophageal_2026-05-04-1730.md` — GI-2 wave plan + post-mortem
- `docs/plans/q_axis_dispatch_template_2026-05-01.md` — chunk-task template patterns
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` — canonical schema spec
- `CLAUDE.md` — repo conventions + multi-agent coordination protocol

---

## 8. Execution-level findings from §17 agent (added post-merge `9882381c`)

These are concrete things the §17 agent did/discovered during execution that supplement the planning-stage decisions in §2-§3.

### 8.1 IndicationPhase placement: sibling-in-same-file

Planning doc §2.2 left this as agent's call ("nested or in same file"). Agent chose **sibling-in-same-file** in `indication.py`, matching the existing `RegimenPhase` pattern. **Cite this precedent in future**: nested model classes go in the same file as their parent, when the relationship is one-to-many composition.

### 8.2 Loader pattern: `ENTITY_BY_DIR` + `REF_FIELDS`

Loader uses two declarative tables:
- `ENTITY_BY_DIR` maps folder name → Pydantic model (added `procedures: Surgery`, `radiation_courses: RadiationCourse`)
- `REF_FIELDS` declares foreign-key paths for ref-integrity (added `concurrent_chemo_regimen → regimens`)
- Per-entity special cases handle paths that don't fit the simple `field_name → entity_type` shape (`phases[*].{regimen,surgery,radiation}_id`, `procedures.applicable_diseases[]`)

**For future refactors:** before adding new entity types, read these two tables. They define the loader's contract surface. Most additive changes need updates to BOTH (new dir mapping + any fk paths).

### 8.3 Folders need not exist for loader to be ready

Agent verified that `procedures/` and `radiation_courses/` folders don't yet exist (no Surgery / RadiationCourse content authored — that's Phase C). Loader's existing dir-walk tolerates non-existent folders gracefully. New entity types can be schema-ready without populated content.

### 8.4 Free-string `Optional[str]` for vocabulary-pending fields

Agent kept `Surgery.type` as `Optional[str]` per §17.1 sketch rather than promoting to enum. Rationale: curator vocabulary will stabilize after Phase C uses Surgery in real content. Premature enum promotion is a recurring schema-design trap.

**For future refactors:** when a field's value-set isn't yet stable from clinical content, ship it as `Optional[str]` first. Promote to enum only after multiple chunks of real content reveal the canonical vocabulary.

### 8.5 Pydantic v2 `@model_validator(mode='after')` for XOR rules

XOR rule on `IndicationPhase.{regimen_id,surgery_id,radiation_id}` implemented via `@model_validator(mode='after')` returning `self` after raising `ValueError` on multi-FK or zero-FK cases. **Standard idiom for cross-field validation in Pydantic v2.**

### 8.6 Test count rule of thumb

Agent wrote 28 tests for §17 (12 phases + 8 surgery + 8 radiation). Roughly: 8-12 tests per new model covers accept-paths (valid construction + serialization) + reject-paths (each validator failure mode). Use as estimating heuristic for future refactors.

### 8.7 Golden fixtures via `model_validate`, not `load_content`

Test fixtures (`phased_indication.yaml`, `surgery_whipple.yaml`, `radiation_cross.yaml`) loaded via direct `model_validate()` calls in tests, NOT through the full `load_content` loader pipeline. This decouples model-level testing from loader-level testing — fixture data doesn't have to satisfy ref-integrity.

**For future refactors:** model tests via `model_validate`; loader tests via real KB load. Separate test layers.

### 8.8 Migration scripts NOT needed when fields are opt-in

Agent did NOT write a migration script. Confirmed: existing 2799 entities continue loading unchanged because `phases:` is `Optional[list[IndicationPhase]] = None`. **Re-validates planning doc §2.5 — opt-in fields remove the entire migration burden.**

### 8.9 Pre-existing pytest failure verification via git-stash round-trip

Agent verified `test_seed_loads_without_errors` failure pre-exists by stashing changes, running test on baseline, confirming same failure, then restoring changes. Standard technique.

**For future refactors:** when "all tests pass except N" is the result, EVERY pre-existing failure must be verified via stash round-trip. Don't accept "they were probably failing before" without proof.

### 8.10 Spec text edit pattern: §X.4 step-by-step done/deferred

§17.4 originally listed 7 resolution steps. Agent marked steps 1, 2, 3, 6, 7 done in this PR; steps 4 (engine pass-through) + 5 (render phased-timeline) explicitly deferred to Phase C readiness work — visible in the spec text post-merge.

**For future refactors:** when ratifying a multi-step proposal, edit the resolution-path section to mark each step's status (done/deferred). Future readers see at a glance what landed vs what's pending.

### 8.11 `feat/...` branch prefix worked cleanly with self-push

`feat/schema-17-refactor-2026-05-07-2200` was an infrastructure branch — no chunk-task label needed. Self-pushed successfully per CLAUDE.md `3a60901b` after green gates. **Confirms `feat/` prefix is the right signal for refactor / schema / engine / render work.** `chunk/` is reserved for clinical-content workstreams.

---

## 9. Phase C consumer-level findings (added 2026-05-08, post Phase C wave 1+2 merge)

After §17 schema landed, six chunks (C1-C5 + C5-backfill) consumed the new schema. Patterns + gotchas surfaced from real clinical content authoring against `Indication.phases` / Surgery / RadiationCourse:

### 9.1 YAML empty-list-with-comments pitfall

`biomarker_requirements_excluded:` (or any list-typed field) followed only by comments — without explicit `: []` — parses as `None`, which Pydantic rejects for list field. **Symptom:** loader fails on indication YAML with valid-looking syntax.

**Fix pattern:**
```yaml
# BAD (parses as None):
biomarker_requirements_excluded:
  # No exclusions in v0.1; HER2-positive routes to dedicated track

# GOOD (parses as []):
biomarker_requirements_excluded: []
# No exclusions in v0.1; HER2-positive routes to dedicated track
```

Caught by C1 agent during validator checks. Worth pre-flagging for any chunk that authors new indications.

### 9.2 §17 concurrent chemo+RT: RadiationCourse owns the ref

XOR rule on `IndicationPhase` (exactly one of regimen_id / surgery_id / radiation_id) means concurrent chemoradiation can't put BOTH `radiation_id` AND `regimen_id` on a single phase. Decision: **`RadiationCourse.concurrent_chemo_regimen` field owns the reference**.

Pattern (used by C2 CROSS + C3 definitive CRT):
```yaml
# Indication phase:
phases:
  - phase: neoadjuvant
    type: chemoradiation
    radiation_id: RC-CROSS-NEOADJ
    duration_weeks: 5

# RadiationCourse:
id: RC-CROSS-NEOADJ
total_dose_gy: 41.4
fractions: 23
concurrent_chemo_regimen: REG-CARBOPLATIN-PACLITAXEL-WEEKLY  # ← here
```

Mirrors `tests/fixtures/radiation_cross.yaml` golden fixture. **Don't try to put concurrent regimen on the phase itself** — XOR validator rejects.

### 9.3 Backward-compat on edits via preserved `recommended_regimen`

When converting a free-text-RT indication to §17 phases (C2 CROSS), preserve the existing `recommended_regimen` field. Renderers / engine layers may still read it. Adding `phases:` is opt-in additive; removing existing fields breaks back-compat. Old field becomes redundant but harmless.

**Render layer migration** to phase-aware iteration is a separate workstream (§17.4 step 5 deferred). Until then: keep both.

### 9.4 `recommended_regimen: null` is valid (Optional[str] semantics)

C5 oligomet shipped with `recommended_regimen: null` because REG-FLOT didn't exist yet. C5-backfill predicted "ref_errors should drop by 2" when wired up. **Empirically: 0 drop.**

`Indication.recommended_regimen` is `Optional[str]` per schema. `null` is already valid (no ref-integrity error). Wiring to a real regimen ID upgrades from `valid-null` to `valid-resolved` but doesn't reduce error count.

**Implication for future agents:** don't predict ref-error drops from null→FK swaps. Predict drops only from invalid-FK (referencing non-existent ID) → valid-FK (now-existing ID).

### 9.5 Disease filename convention: no `dis_` prefix

Multiple agents discovered: gastric disease file is `gastric.yaml`, not `dis_gastric.yaml`. Esoph is `esophageal.yaml`, not `dis_esophageal.yaml`. **Verify via `ls knowledge_base/hosted/content/diseases/` before writing pathspecs.** Don't assume `dis_` prefix.

`procedures/proc_*.yaml`, `radiation_courses/rc_*.yaml`, `regimens/reg_*.yaml`, `indications/ind_*.yaml`, `redflags/rf_*.yaml`, `biomarkers/bio_*.yaml`, `bma/bma_*.yaml`, `sources/src_*.yaml`, `algorithms/algo_*.yaml`, `drugs/drug_*.yaml` — these DO use prefixes. Diseases don't.

### 9.6 Disease.procedure_options: use metadata namespace

C1 discovered `Disease` schema has no canonical `procedure_options` top-level field in v0.1. Used `metadata.procedure_options` via Pydantic `extra='allow'`. C4 (esoph) mirrored exactly.

**Pattern for future Disease extensions:** when a disease-level concept doesn't have schema support, use `metadata.<concept_name>` (extra='allow' admits this). Promote to top-level only when concept is universally adopted across multiple diseases AND clinical co-leads request.

### 9.7 Filename in chunk spec ≠ actual filename

Multiple agents found: chunk-spec filenames are descriptive, not literal. Examples:
- Spec said `ind_esoph_neoadj_cross.yaml`; actual is `ind_esoph_resectable_cross_neoadjuvant.yaml`
- Spec said `dis_esophageal.yaml`; actual is `esophageal.yaml`

**Pattern:** when chunk spec lists a target filename, agent verifies via `ls` first and adapts to actual filename. Spec author should ideally list real filenames, but not always feasible when spec was written before content audit.

### 9.8 First-consumer chunk sets gold-standard pattern for siblings

C1 was first §17 consumer (FLOT periop). C2 → C5 + C5-backfill all explicitly cited "C1 precedent" or "mirrors C1's pattern" in their commits. **Designate one chunk as gold-standard pattern when launching a multi-chunk wave on new schema.** Subsequent chunks save dispatch time by referencing the precedent file directly.

### 9.9 Sequential-vs-parallel timing for FK-dependent chunks

C5 (oligomet) needed REG-FLOT. C1 (FLOT periop) created REG-FLOT. Dispatched both in parallel — C5 shipped with `recommended_regimen: null` honestly + flagged backfill needed. C5-backfill chunk (#438) wired the FK after C1 merged.

**Pattern:** when chunk B depends on entity created by chunk A, and both are urgent:
- Sequential: C1 first, then C5 — slower but no deferred state
- Parallel + backfill chunk: ship null + small follow-up — faster end-to-end + honest reporting

For Phase C, parallel + backfill won — one extra trivial chunk (#438) but ~15-30 min saved end-to-end. Worth it.

### 9.10 Algorithm-wiring is consistently out of clinical-content chunk scope

Every Phase C chunk flagged "algorithm doesn't route to new indication yet" as out-of-scope follow-up. Aggregated into D2 algorithm-extension chunk. **Confirmed pattern:** new clinical content lands first; engine routing extends in dedicated D-prefix chunk.

This decoupling means clinical content can be reviewed for accuracy independently of routing logic — separate review surfaces per file type.
