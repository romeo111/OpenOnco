# Latest changes PWA + KB architecture review - 2026-05-07

**Scope:** review of the latest committed changes on `HEAD` through `adc073474`, focused on the GI-2 gastric/esophageal KB wave, generated site refresh, and the implications for a future PWA wrapper around `try.html`.

**Reviewed commits:**

- `adc073474` - `feat(kb): GI-2 A2 extended personalisation BMA - FGFR2b + EBV gastric (#409)`
- `bce7a093e` - `feat(kb): GI-2 A1-redux esophageal 1L metastatic gaps (2/3 indications + 1 regimen) (#408)`
- `e726ff4e3` - `chore(site): daily refresh - 30329+ refs across 349 sources`
- `927440237` - `feat(kb): GI-2 W0-4 add DESTINY-Gastric04 source stub (#404)`
- `1017fe5c7` - `docs(plans): GI-2 wave plan + post-W0 corrections (#402)`
- `093590876` - `fix(kb): GI-2 B1 reconcile gastric 1L PD-L1 CPS threshold + add CheckMate-649 canonical nivo dose (#401)`
- `3cac0fe81` - `feat(kb): GI-2 W0-2 esophageal trial source backfill (5 sources) (#398)`
- `b6f49b260` - `fix(kb): GI-2 W0-3 propagate SRC-CHECKMATE-649-JANJIGIAN-2022 citations (#397)`

## Executive assessment

The latest changes are directionally sound: they extend high-value GI coverage using the existing declarative KB model rather than adding special-case code to the engine or to `try.html`. The best architectural signal is that new clinical logic continues to land as YAML entities under `knowledge_base/hosted/content/`, while the browser layer remains a delivery/runtime shell.

The changes are safe for PWA evolution only under the current source-of-truth model: Git-tracked YAML + validation + generated immutable bundles. They would not be safe if the future PWA were allowed to mutate the canonical KB directly from the browser.

## What changed

The last two feature commits add a compact but meaningful GI-2 slice:

- Gastric biomarker/actionability expansion:
  - `bma_ebv_positive_gastric.yaml`
  - `bma_fgfr2b_membrane_gastric.yaml`
  - `bio_fgfr2b_ihc.yaml`
  - `ind_gastric_metastatic_1l_fgfr2b_bemarituzumab.yaml`
- Esophageal metastatic 1L expansion:
  - `ind_esoph_metastatic_1l_her2_trastuzumab_chemo.yaml`
  - `ind_esoph_metastatic_1l_scc_ipi_nivo.yaml`
  - `reg_ipi_nivo_esoph_scc.yaml`
- Earlier GI-2 commits also touched gastric PD-L1 CPS handling, FOLFOX+nivolumab, and trial source stubs/backfill.
- The daily refresh regenerated a large docs surface: 1308 files changed, mostly case HTML and search/wiki artifacts, with roughly balanced insertions/deletions.

## Validation findings

A full KB load with the bundled Python runtime produced:

| Check | Result |
|---|---:|
| Loaded entities | 2793 |
| Schema errors | 91 |
| Referential errors | 179 |
| Contract errors | 0 |
| Contract warnings | 217 |
| Overall loader state | `ok=False` |

Important nuance: filtering the validator output to the newly changed GI-2 KB files found no schema errors, no referential errors, no contract errors, and no contract warnings for those files. The latest GI-2 files are not the source of the current global validation debt.

V1 compatibility follow-up in this branch reduced the global validation debt without adding new clinical KB content:

| Check | Before V1 compatibility | After V1 compatibility |
|---|---:|---:|
| Schema errors | 91 | 65 |
| Referential errors | 179 | 154 |
| Contract errors | 0 | 0 |
| Contract warnings | 217 | 238 |
| Regimen schema errors | 26 | 0 |
| Regimen referential errors | 22 | 6 |

The warning increase is intentional: legacy free-text `mandatory_supportive_care` entries are now reported as authoring warnings instead of blocking as unresolved SupportiveCare IDs. True `SUP-*` typos still fail referential integrity.

V1 drug-entity follow-up in the next commit resolved the remaining regimen
component blockers:

| Check | After compatibility | After missing-drug slice |
|---|---:|---:|
| Referential errors | 154 | 148 |
| Regimen referential errors | 6 | 0 |
| Contract errors | 0 | 0 |

The five added Drug entities are intentionally thin: `DRUG-CABAZITAXEL`,
`DRUG-MESNA`, `DRUG-NAL-IRI`, `DRUG-MITOMYCIN-C`, and `DRUG-PAZOPANIB`.
They make existing regimens materializable, while detailed availability and
full monograph metadata remain future curation work.

Final V1 cleanup follow-up completed the structural validation pass:

| Check | Original baseline | After V1 cleanup |
|---|---:|---:|
| Schema errors | 91 | 0 |
| Referential errors | 179 | 0 |
| Contract errors | 0 | 0 |
| Loader `ok` | false | true |

This was achieved through compatibility shims for legacy Indication/Source/BMA
authoring shapes and thin structural catalog entries for missing Tests,
Biomarkers, RedFlags, and five referenced Regimens. The remaining warnings are
authoring-quality warnings, not loader blockers.

The existing debt is still a release-management problem. A PWA or service worker will make stale/invalid KB states more persistent on client devices, so the deploy gate should distinguish:

- block deploy on schema/ref errors in release-scoped content,
- allow clearly labelled draft clinical warnings only when they are intentional,
- stamp every bundle and service-worker cache with a content hash, as the current `openonco-engine-index.json` and `sw.js` already do.

## Architecture impact

The latest changes fit the existing architecture well:

- They preserve the separation between content, schemas, engine, and static delivery.
- They do not introduce runtime network dependency for treatment selection.
- They do not make `try.html` responsible for clinical decision logic.
- They keep generated docs as downstream artifacts, not as the source of truth.

This is the right shape for continuous KB growth. The main technical pressure is not from the new GI content itself, but from the growing generated surface and the large `try.html` orchestration script.

## Coverage and normalization document impact

Two adjacent planning/contribution documents are relevant to the current decision:

- `contributions/drug-class-normalization/normalization_report.yaml` is a negative-finding audit. It reviewed all hosted Drug `drug_class` values and found zero actionable normalization clusters. It should not create work for the GI-2/PWA path; its useful lesson is procedural: run a cheap upstream audit before opening speculative cleanup chunks.
- `docs/kb-coverage-strategy.md` and `docs/kb-coverage-matrix.md` are more consequential. They confirm that coverage growth must be tied to a specific disease x axis cell and must not treat presence-of-field as clinical verification. For GI-2 this means a new BMA or indication is not enough by itself: routing and PWA display should distinguish drafted/available content from verified, signoff-ready content.

This does not change the PWA architecture recommendation. It reinforces it: the PWA can show coverage, verification, freshness, and cache version state, but it must not present generated bundles as a clinically signed-off database unless the matrix quality gates are green for the relevant cells.

Follow-up implemented in this branch: the loader now rejects Algorithms that route to active treatment tracks with `recommended_regimen: null`, unless the Indication uses an explicit non-regimen `plan_track`. Existing no-regimen routed records were reclassified as `surveillance`, `local_therapy`, or `transplant` as appropriate.

Second follow-up implemented: `ALGO-ESOPH-METASTATIC-1L` now exposes the already-authored A1 indications for ESCC chemo-sparing ipi+nivo and HER2-positive EAC/GEJ Siewert I trastuzumab+chemo. Gastric FGFR2b remains intentionally unrouted because its indication still has no regimen.

Third follow-up implemented: the loader and Regimen schema now normalize legacy generated regimen YAML in memory (`agents:` -> `components:`, `DRG-*` -> `DRUG-*`, `total_planned_cycles` -> `total_cycles`, and fallback names from `REG-*` IDs). This keeps old source-controlled content ingestible while still surfacing genuinely missing Drug entities as ref errors.

Fourth follow-up implemented: CI now uses `scripts/audit_validator.py --human` as the release gate. The gate fails on schema, referential-integrity, or loader contract errors; scheduled audit state, metrics, and issue planning now track contract regressions explicitly.

## PWA implications

The project is already close to a PWA-compatible delivery model:

- `docs/sw.js` implements cache-first behavior for engine artifacts and stale-while-revalidate for `try.html` / `style.css`.
- `docs/openonco-engine-index.json` maps 78 diseases to per-disease bundles.
- `docs/openonco-engine-core.zip` is the browser runtime core bundle.
- `try.html` uses Pyodide and lazy disease module loading rather than requiring a backend.

What is still missing for a complete PWA:

- a web app manifest,
- install icons and display metadata,
- a clearer offline/update UX,
- explicit cache version visibility in the UI,
- extraction of the large inline JS in `try.html` into maintainable modules.

The right PWA role is: offline-capable viewer/generator for synthetic or locally entered profiles, plus a possible contributor draft tool. The wrong role is: browser-local canonical KB editor.

## Risks

1. **Authoring-warning debt.** Global schema/ref/contract validation is now clean, but 524 loader warnings remain. These should be worked down before presenting the PWA as a durable clinical KB client.
2. **Generated-doc churn.** The daily refresh touches over a thousand files. This is acceptable for GitHub Pages deployment, but it makes human review harder. Future PRs should keep source KB changes separate from generated refreshes when possible.
3. **`try.html` maintainability.** The page is already doing UI state, Pyodide boot, lazy bundle fetch, localStorage, modal rendering, and service-worker registration. That is tolerable now, but it will become the main PWA bottleneck.
4. **Client cache semantics.** Service-worker cache rotation is hash-stamped, which is good. The UI still needs to make update state obvious so clinicians/contributors know which KB build they are using.
5. **Clinical review boundary.** New BMAs and indications must remain draft/proposed until the signoff process confirms them. PWA installability must not imply clinical readiness.

## Recommended next steps

1. Split generated docs refreshes from clinical KB PRs where practical.
2. Add `manifest.webmanifest`, install icons, and minimal PWA metadata now that structural validation is clean.
3. Refactor `try.html` into external JS modules while keeping the static GitHub Pages deployment model.
4. Add a visible build/version panel in the try page: core bundle hash, disease bundle hash, release date, and offline/cache status.
5. For future contributor editing, create a "draft contribution" flow that exports YAML/patches for PR review instead of writing canonical KB from the PWA.
6. Work down the 524 warnings by priority: convert legacy free-text tests/contraindications/supportive care into authored entities, then review draft RedFlags.

## Decision

Proceed with the PWA direction, but keep the canonical KB pipeline outside the browser. The latest changes reinforce the correct architecture: declarative KB growth plus generated browser bundles. The blocking issue for a more serious PWA release is not the GI-2 change set; it is the remaining warning debt, visible bundle/cache versioning, and the need to modularize the try-page runtime.
