# OpenOnco development roadmap

Owner: ongoing engineering work in the OpenOnco development chat. Updated: 2026-10-11.

## Mission and operating priorities

Keep OpenOnco free and useful for source-cited oncology discussion. Prioritize reliable tools, evidence, clinical review, privacy and accessibility before visual polish. Helping people reach appropriate care is the intended impact; improved survival has not been demonstrated for this service.

Deliver small, verified changes through the repository's normal commit, push and deployment process. Preserve other contributors' work. Record completed work, remaining risks and the next concrete task here. Review CI and production before choosing the next improvement.

## Current evidence

- Browser plan generation works on the built-in synthetic AML example. The latest observed first engine initialization in a test tab took 12.1 seconds with existing browser caches; this is not a fresh-device cold-load benchmark.
- Compiled safe YAML parsing reduced a local load-and-validation measurement from 39.3 to 2.4 seconds with identical entities and validation results. A portable safe parser remains available.
- Source-linked clinical translations remain drafts. Technical verification does not provide clinical or linguistic sign-off.
- The engine refuses clinical output from invalid knowledge bases. Browser core initialization and cached/network disease-module loading now also reject validation failures, with failure-injection tests in CI. Offline workflows still need end-to-end production verification.
- Marketing must distinguish coverage, technical verification and clinician-reviewed readiness.

## Ordered backlog and acceptance criteria

| Priority | Work | Evidence required before completion |
| --- | --- | --- |
| P0 | Stop browser generation on failed core validation or disease-module download/validation; validate cache hits too | Failure-injection tests for cached and network paths, successful retry, successful synthetic plan on production |
| P0 | Localize the complete patient report: English renderer first, then ES/PT/DE/FR draft catalogs | Inventory Python-authored text and dynamic YAML labels separately; preserve doses, source titles, IDs, negation and selection; inspect generated reports; clinical translation review remains explicit |
| P0 | Exercise complete browser workflows in CI | Synthetic example → validated plan → source links → HTML/PDF export; invalid KB and offline failures explicitly blocked |
| P1 | Measure startup on an empty-cache device, ordinary mobile network and repeat visit | Reproducible timings and payload sizes; separate network, Python initialization, validation and generation |
| P1 | Improve dependency-complete bundle efficiency | Every supported disease module validates with core alone; no clinical inputs removed; compare generated plan contracts |
| P1 | Verify offline use and draft recovery | Previously loaded synthetic profile still produces a validated plan; unavailable modules show an actionable error; server tools do not claim local-only processing |
| P1 | Audit medical translation safety and source freshness | Original text remains accessible; dose, polarity, units and IDs preserved; uncertain content queued for clinical review |
| P1 | Make review readiness visible at decision points | Draft/STUB/missing-data states are explicit; clinician-confirmation gates remain explicit; reviewer packet and feedback export work |
| P2 | Improve accessibility and task completion | Keyboard, mobile forms, readable errors, language switching and report controls verified on representative workflows |
| P2 | Publish evidence-based discovery and educational content | Search metadata and links verified; claims tied to demonstrated capabilities; clear intended audience and review status |
| P2 | Prepare partner and clinician outreach materials | Reviewable drafts, relevant audience, measurable pilot questions; sending requires separate authorization |

## Marketing approach

Start with organic discovery: accurate search metadata, useful source-linked educational material, practical synthetic demos and clear contributions/review instructions. Explain what the tool does, what is still a draft, and how a clinician can evaluate it. Avoid guarantees, unsupported survival claims, fabricated testimonials, implied organizational endorsement and fear-based messaging.

Use technical and usability measures first: successful synthetic plan generation, explicit rejection of invalid data, accessibility, load time, correct export, resolved feedback and clinician review completion. Any patient-outcome claim requires appropriate independent evidence.

Do not add paid dependencies to core access, purchase advertising, contact people or create financial commitments without authorization. Keep public examples synthetic; do not expose patient information in GitHub or analytics.

## Continuation log

- 2026-10-11: Shared public layouts delivered across six languages. Dependency-complete treatment bundles fixed a production generation failure. Startup optimization delivered in `bad3d78a39` and merge `36fbf942ec`; production synthetic plan verified. Regular continuation scheduled every six hours, with notifications for meaningful changes or required action.
- 2026-10-11: P0 browser loading guards implemented with repeatable failure injection in CI: validate cached and downloaded modules before marking them loaded, reject invalid core initialization, reset initialization after failure, and stop generation when a required module fails. Verification and delivery recorded in the development chat.
- 2026-10-11: Treatment reports now link cited source labels to recorded original URLs, with safe URL filtering and plain-text fallback. Renderer/source integration: 58 tests passed. Six browser clients wait for report loading before export; failure and timeout allow retry. Node regression tests verify displayed-language HTML export and print invocation. Actual downloaded PDF content and empty-cache startup remain to be verified.
- Next: verify the complete deployed synthetic workflow and actual exports, then measure fresh-device startup.

- 2026-10-11: Production verification of 51868619c0: Pages deployed successfully. French synthetic AML report generated with core baac4fb46f23 in 13.653 s (10.383 s engine initialization, 3.269 s Python; existing browser caches). Downloaded HTML verified for displayed French locale, PLAN-VIRTUAL-AML-001-V1, REG-VEN-AZA-AML, primary VIALE-A URL and review wording. PDF button interaction timed out in the embedded browser; actual saved PDF content remains unverified. Do not treat print-invocation tests as PDF-content verification.

- 2026-10-11: Unified report language reloads: translation overlay delegates to the guarded builder, including switching between native translation and the same English source. Export remains unavailable until the reload finishes; duplicate iframe reloads removed. Regression test covers the same-source path across six clients.

- 2026-10-11: Production EN → FR reloads and HTML exports verified after 744c9d744c; exported languages, synthetic plan/regimen IDs and publication URLs match the displayed report. Patient renderer is Ukrainian-only despite language selection: full English patient rendering and subsequent reviewed ES/PT/DE/FR catalogs are now P0. Interim integrity fix preserves actual report language in filenames and makes the Ukrainian fallback explicit; this does not complete patient localization.

- 2026-10-11: Patient reports now include original publication links in a readable, expandable bibliography. Titles remain verbatim and internal source IDs remain auditable in attributes. Source rendering leaves the clinical plan unchanged. A render-only Ukrainian label fixes a raw English HCV monitoring qualifier while preserving the original in an attribute. Patient/render/source tests: 96 passed, one skipped.
- Patient translation inventory: python scripts/audit_patient_localization.py --output .tmp/patient-localization-inventory.json identifies 513 Python-authored literals/templates (504 unique); dynamic disease/drug names, red-flag definitions and watchpoints from YAML are outside this count. This is an inventory, not evidence of translated or clinically reviewed coverage. English patient rendering remains unfinished.

- 2026-10-11: Production patient bibliography verified after 05ba808246: synthetic AML patient view shows readable publication titles and original URLs, including ELN 2022 and VIALE-A. First post-deploy tab showed old baac4fb46f23 index badge while rendering the new bibliography; next reliability work must keep bundle-index metadata and loaded package version consistent through service-worker updates. A stale Python source-expression test failed on 4b33babf07; e84878be5f replaces it with executed export behavior, and all 38 localization tests pass locally. Latest full CI remains to be checked.

- 2026-10-11: Bundle-index loading now shares one request, validates manifest metadata and uses a fresh network response with offline fallback. Core and disease ZIP hashes are checked before unpacking; cache keys preserve versions. Offline preparation verifies both existing and downloaded ZIPs before counting them as ready. Node regressions cover mixed-version rejection, cache repair, HTTP/offline fallback, quota errors and every published ZIP hash. Full site-build verification is still running in the development environment; production rollout remains to be verified.

- 2026-10-11: Version-integrity release 929230ddc2 with merge 98ce9ab98c deployed successfully. Production French synthetic AML generation succeeded with core 82ebb20f7101 and module b4b014f3bd27 after hash verification; cached-startup timing 13.394 s (9.430 s initialization, 3.964 s Python). Initial core badge is now blank until the index arrives. Offline preparation reached its verified-cache ready state; actual browser generation with the network disconnected remains unverified. Local full-site fixture process and latest CI are still running and must be inspected in the next continuation.
