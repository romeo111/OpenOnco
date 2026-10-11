# OpenOnco development roadmap

Owner: ongoing engineering work in the OpenOnco development chat. Updated: 2026-10-11.

## Mission and operating priorities

Keep OpenOnco free and useful for source-cited oncology discussion. Prioritize reliable tools, evidence, clinical review, privacy and accessibility before visual polish. Helping people reach appropriate care is the intended impact; improved survival has not been demonstrated for this service.

Deliver small, verified changes through the repository's normal commit, push and deployment process. Preserve other contributors' work. Record completed work, remaining risks and the next concrete task here. Review CI and production before choosing the next improvement.

## Current evidence

- Browser plan generation works on the built-in synthetic AML example. The latest observed first engine initialization in a test tab took 12.1 seconds with existing browser caches; this is not a fresh-device cold-load benchmark.
- Compiled safe YAML parsing reduced a local load-and-validation measurement from 39.3 to 2.4 seconds with identical entities and validation results. A portable safe parser remains available.
- Source-linked clinical translations remain drafts. Technical verification does not provide clinical or linguistic sign-off.
- The engine refuses clinical output from invalid knowledge bases. Browser loading and cached disease-module validation need equally strict behavior.
- Marketing must distinguish coverage, technical verification and clinician-reviewed readiness.

## Ordered backlog and acceptance criteria

| Priority | Work | Evidence required before completion |
| --- | --- | --- |
| P0 | Stop browser generation on failed core validation or disease-module download/validation; validate cache hits too | Failure-injection tests for cached and network paths, successful retry, successful synthetic plan on production |
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
- Next: add a complete browser workflow test covering source links and export, then measure fresh-device startup. Recheck production and CI before extending functionality.
