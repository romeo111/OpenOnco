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
