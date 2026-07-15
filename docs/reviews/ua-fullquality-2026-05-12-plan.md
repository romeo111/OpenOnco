# UA full-quality translation — parallel-agent plan (2026-05-12)

## Goal

Drive every EN↔UA companion-field pair across the OpenOnco knowledge base
to **publication-quality clinical Ukrainian**, marked
`draft_revision: 2`. Clinical signoff (`reviewed: true`) is a **separate**
two-Co-Lead gate per CHARTER §6.1 and is **not** flipped by this work.

## Source-of-truth files

| File | Role |
|---|---|
| `knowledge_base/translation/ua_terminology.yaml` | Glossary — read-only for agents. New term proposals → `glossary_proposals.jsonl` per-agent. |
| `knowledge_base/validation/ua_quality.py` | Quality gate. Agents run before commit. EN_BLEED + NUMERIC_DRIFT + LINK_PARITY are blocking. |
| `scripts/audit_ua_coverage.py` | Coverage matrix. Re-run after each merge. |
| `docs/reviews/ua-coverage-2026-05-12.csv` | Phase-0 baseline. |

## Baseline (2026-05-12, defer threshold = 2 days)

| entity_type | missing | drafted_pending v1 | total | recently-modified (defer) |
|---|---:|---:|---:|---:|
| algorithms | 150 | 0 | 150 | 59 |
| biomarker_actionability | 449 | 446 | 895 | 27 |
| biomarkers | 4 | 166 | 170 | 0 |
| diseases | 4 | 74 | 78 | 0 |
| drugs | 256 | 0 | 256 | 6 |
| indications | 80 | 306 | 386 | 54 |
| procedures | 9 | 0 | 9 | 1 |
| radiation_courses | 6 | 0 | 6 | 1 |
| redflags | 38 | 448 | 486 | 183 |
| regimens | 73 | 271 | 344 | 6 |
| **TOTAL** | **1069** | **1711** | **2780** | **337** |

Validator baseline: 2424 files have UA content; 2781 errors (EN_BLEED 2359,
NUMERIC_DRIFT 226, MISSING_MARKER 196), 1007 GLOSSARY_MISS warnings.

## Partition (14 agents, audit-balanced ~150-300 fields each)

Each agent works in its own worktree on branch
`feat/ua-fullquality-<agent-id>-2026-05-12-HHMM`. File-set allowlists are
disjoint — two agents writing the same file is a coordination bug.

| Agent | Allowlist (relative to repo root) | EN-fields in scope |
|---|---|---:|
| ua-01 | `knowledge_base/hosted/content/diseases/*.yaml` | 78 |
| ua-02 | `knowledge_base/hosted/content/biomarkers/*.yaml` | ~170 |
| ua-03 | `knowledge_base/hosted/content/biomarker_actionability/bma_[1a-g]*.yaml` | ~264 |
| ua-04 | `knowledge_base/hosted/content/biomarker_actionability/bma_[h-n]*.yaml` | ~348 |
| ua-05 | `knowledge_base/hosted/content/biomarker_actionability/bma_[o-z]*.yaml` | ~284 |
| ua-06 | `knowledge_base/hosted/content/indications/{ind,indication}_[a-f]*.yaml` | ~177 |
| ua-07 | `knowledge_base/hosted/content/indications/{ind,indication}_[g-o]*.yaml` | ~143 |
| ua-08 | `knowledge_base/hosted/content/indications/{ind,indication}_[p-z]*.yaml` | ~122 |
| ua-09 | `knowledge_base/hosted/content/redflags/rf_[a-h]*.yaml` | ~454 |
| ua-10 | `knowledge_base/hosted/content/redflags/{rf_[i-z]*.yaml,rf_universal*.yaml}` | ~524 |
| ua-11 | `knowledge_base/hosted/content/regimens/[a-m]*.yaml` | ~185 |
| ua-12 | `knowledge_base/hosted/content/regimens/[n-z]*.yaml` | ~185 |
| ua-13 | `knowledge_base/hosted/content/algorithms/*.yaml` | 152 |
| ua-14 | `knowledge_base/hosted/content/{drugs,procedures,radiation_courses}/*.yaml` | 271 |

## Per-agent operating rules (NORMATIVE)

1. **Pre-flight**: `git rev-parse --abbrev-ref HEAD` must return your
   feature branch, `git status --short` must be clean. STOP and report
   on mismatch.
2. **Allowlist is hard**: files outside your allowlist → skip silently.
   Two agents touching the same file is a coordination bug.
3. **Glossary**: use `knowledge_base/translation/ua_terminology.yaml` for
   every drug name, locked phrase, and stay-Latin token. Do **not** edit
   the glossary. If you encounter a term not in the glossary:
   - **Confident** → translate with best-judgment UA, append a row to
     `glossary_proposals.jsonl` in your worktree root: `{"term_en": "...",
     "proposed_ua": "...", "context_file": "...", "context_field": "..."}`.
   - **Uncertain** (e.g., very recent drug, novel mechanism) → leave
     the EN term inline and add a sibling YAML line comment
     `# UA-GLOSSARY-MISS: <term>` directly above the field.
4. **Field semantics**:
   - For each `(en_field, ua_field)` pair in your entity's plan
     (mirrors `audit_ua_coverage.ENTITY_PLAN`), produce a UA companion
     of full-clinical-textbook quality.
   - Every numeric, dosing, ID (`SRC-*`, `BMA-*`, `EID*`, `NCT*`),
     HGVS variant, cytogenetic notation, percentage, year, and
     markdown link from EN MUST appear verbatim in UA. The validator
     will fail otherwise.
   - Tone: hospital-discharge-letter / textbook clinical UA, third
     person. No patient-direct address ("ви", "вам") in KB fields —
     patient-mode glossing handles that at render time.
   - Drug first-mention: `<UA name> (<EN INN>)`; subsequent: UA alone.
5. **Marker rules** (every entity you edit):
   - `ukrainian_review_status: pending_clinical_signoff` (KEEP this; do
     not flip to `human_reviewed` or invent a new state).
   - `ukrainian_drafted_by: claude_<your-agent-id>` (e.g.,
     `claude_ua_01`).
   - `draft_revision: 2` (set this — signals upgrade past v1
     `claude_extraction`).
6. **Defer**: skip files where the EN source field shows churn within 2
   days. The audit CSV's `defer` column is the authoritative flag — do
   not translate any row with `defer == "yes"`. Reason: avoids redoing
   work when the EN source still moves.
7. **Validation gate** (must run successfully before commit):
   ```
   C:/Python312/python.exe -m knowledge_base.validation.ua_quality <each-changed-file>
   C:/Python312/python.exe -m knowledge_base.validation.loader knowledge_base/hosted/content
   ```
   Zero errors required. Warnings (`GLOSSARY_MISS`) acceptable but log
   the count in the commit message.
8. **Commit hygiene**:
   - Explicit pathspecs only. Never `git add -A` / `git add .`.
   - One commit per ~25 files, message:
     `ua(<entity-type>): upgrade <N> fields to publication quality (agent ua-XX)`.
   - Pre-commit hook is allowed to run; never `--no-verify`.
9. **Stop conditions** (abort + report, do not improvise):
   - HEAD on wrong branch.
   - File outside allowlist would change.
   - Validator error you cannot resolve.
   - Glossary edit attempted (read-only).
   - Cherry-pick / merge conflict.
10. **End-of-run**: push branch to origin. Do not open PR. Orchestrator
    integrates.

## Integration (orchestrator, post-Phase-1)

For each agent branch in order:
1. Cherry-pick onto integration branch (allowlists were disjoint, so no
   conflicts expected).
2. Re-run audit + validator. Counts must move in the right direction.
3. Spot-check 12 random files (4 from BMA, 4 from RF, 4 from disease) —
   read end-to-end, flag stylistic/clinical drift.
4. If clean → merge integration to master via PR with two-reviewer
   approval (this is a docs/translation change; CHARTER §6.1 dev-mode
   exemption applies because EN source is unmodified).
5. Rebuild site (`scripts/build_site.py`), spot-check 6 random `/ukr/`
   pages.

## Post-Phase-1 phases (not yet briefed; sequence set)

- **Phase 2**: site wiki HTML pages (`docs/about,capabilities,ask`,
  case auto-* mirror to `/ukr/`). 4 agents.
- **Phase 3**: render-layer UA strings in `knowledge_base/engine/render*.py`.
  Single agent (small surface, high blast radius).
- **Phase 4**: spec deltas — sync `specs/uk/` against EN-canonical
  changes. 2 agents.

## Why no `translation_quality_ok` state

Per advisor 2026-05-12: an agent flipping a state it set itself is
self-attestation, not a quality signal. The `draft_revision` integer
(1 = `claude_extraction` dictionary pass; 2 = full-quality clinical
register pass) is honest about what the agent layer can deliver. A
human/UA-native clinician would later flip
`ukrainian_review_status → human_reviewed` separately.
