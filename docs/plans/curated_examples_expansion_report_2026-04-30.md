# Curated Examples Expansion — Phase 1 + 2 Report

**Status:** execution complete, 2026-04-30. Companion to the original plan
[`curated_examples_expansion_2026-04-29-0313.md`](curated_examples_expansion_2026-04-29-0313.md).
Integration branch pushed; PR strategy decision pending.

## Original ask

Analyze ready examples + assess whether more can be made from new data.

## Pre-execution analysis

- **169 example JSON** (104 curated + 65 auto-stub).
- **Gallery:** 164 entries.
- **KB:** 65 diseases.
- **Finding:** solid tumors had ~24 diseases with auto-stub only.
  - NSCLC: 28 indications / 0 curated.
  - BREAST: 20 / 0.
  - CRC: 18 / 1.

## Plan + governance change

- Plan: 12 chunks × ~64 new curated cases, two phases, worktree-isolation
  ([`docs/plans/curated_examples_expansion_2026-04-29-0313.md`](curated_examples_expansion_2026-04-29-0313.md), commit `234ddfc5`).
- `CLAUDE.md` (commit `3a60901b`): added self-push permission when gates are
  green.

## Phase 1 — 12 chunk branches pushed

| Chunk | SHA | Cases | Method |
|---|---|---:|---|
| S1 NSCLC | `b5118253` | 12 | manual smoke-test (maintainer) |
| S2 BREAST | `e6fc3a11` | 8 | parallel agent (after respawn) |
| S3 CRC | `2454b028` | 6 | parallel agent |
| S4 MELANOMA | `4c453f8f` | 5 | parallel agent (after respawn) |
| S5 PROSTATE | `fdd334ef` | 1 / 5 | parallel agent (4 dropped: KB schema gap) |
| S6 GU+SKIN+GYN | `a467fda0` | 6 | parallel agent (after respawn) |
| S7 GI | `3bb286b7` | 6 | parallel agent |
| S8 THORACIC-HNSCC | `de0ec0a7` | 4 | parallel agent |
| H1 AML | `57216bca` | 4 | parallel agent |
| H2 DLBCL | `ec96220b` | 3 | recovered (agent committed locally before Cloudflare 403; pushed manually) |
| H3 INDOLENT-B | `075cedc0` | 2 / 4 | parallel agent (2 dropped: KB wiring gaps) |
| D1 DIAGNOSTIC | `9129f0a4` | 3 | parallel agent |

**Total: 60 / 64 cases shipped.** The 4 misses are not agent bugs — they
are real KB-wiring gaps that the chunks surfaced.

## Phase 2 — integration (commit `f69e5d24`)

Manual integration (Cloudflare 403 blocked agent attempts):

- Merge all 12 chunks into integration branch (zero conflicts, all `--no-ff`).
- Append 60 `CaseEntry` rows in `scripts/site_cases.py`.
- Regenerate `docs/cases/` via `build_site.py`.

## Metrics

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| Curated `patient_*.json` | 104 | 164 | +60 |
| `CaseEntry` in `scripts/site_cases.py` | 526 | 586 | +60 |
| HTML pages in `docs/cases/` | 526 | 586 | +60 |
| Chunk branches on `origin` | 0 | 13 (12 + integration) | +13 |
| KB validator | ok | ok | stable |

## KB drift signals (10 real defects surfaced)

Each curated case exercises a concrete path through `mdt_orchestrator` +
render. The chunks surfaced 10 real defects:

1. **Track-filter ignores `value_constraint`** (S1 T790M).
2. **`_find_algorithm` does not consult `disease_state`** (S5: 4 prostate
   cases dropped).
3. **Algo-dispatch by load-order on collision** (S2 HER2-2L).
4. **Free-text condition: unevaluable** (S6 / S7 / H3).
5–10. **Multiple indications / regimens missing in KB:** KEYNOTE-006,
   KEYNOTE-054, EXTREME HNSCC, CPX-351, GO AML, loncastuximab DLBCL,
   CLL zanu 1L, esophageal CheckMate-577.

Defect #1 has a `spawn-task` chip (`fix-track-filter`); the rest are
documented in chunk-commit bodies.

## Cross-cutting findings

- **Multi-session realities.** Other parallel sessions moved `master`
  during execution (PR #143 added 362 `variant_*.json`). The H1 AML agent
  accidentally absorbed PR #143 into its lineage → the integration branch
  contains both curated chunks and PR #143 work. No conflict (disjoint
  families: `patient_*` vs `variant_*`), but the PR description should
  acknowledge this.
- **Pre-flight protocol.** 5 of 11 parallel agents stopped on pre-flight
  (HEAD mismatch); 6 self-branched from `234ddfc5`. Both behaviors are
  defensible per `CLAUDE.md`; respawn with explicit authorization let all
  5 stopped agents complete.
- **Cloudflare 403.** Blocked the API mid-execution twice (H2 DLBCL agent
  + Phase 2 agent). Recovery: manual push of locally-committed work +
  manual Phase 2.

## Ready for next step

- Integration branch: `chunk/curated-examples-integration-2026-04-29-2105`
  pushed.
- PR to master: not opened. Pending decision: single integration PR vs
  disease-group split PRs.

### Open decisions

1. **PR strategy.** Single PR is the lower-cost choice given `--no-ff`
   merges already preserve per-chunk history. Splitting now would undo
   that. Two-reviewer rule (CHARTER §6.1) targets `knowledge_base/hosted/content/`
   clinical content; curated examples in `examples/` are test fixtures, not
   clinical recommendations.
2. **PR #143 entanglement.** Verify `git log master..chunk/curated-examples-integration-2026-04-29-2105 -- knowledge_base/hosted/content/variants/`
   before opening the PR. If PR #143 has merged to master, the diff dedups
   cleanly; if not, this PR claims work that isn't its own.
3. **Follow-up for the 10 KB drift signals.** Should not be bundled into
   the curated-examples PR. Open a separate issue or chunk-batch covering
   defects 1-4 (engine wiring) and 5-10 (KB content gaps) as two distinct
   workstreams.
