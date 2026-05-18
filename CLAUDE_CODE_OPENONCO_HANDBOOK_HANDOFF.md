# OpenOnco Handbook Handoff

## Current State

OpenOnco Handbook now has a working MVP for authored educational handbook content. It is explicitly not an ESMO copy, derivative, or CME replacement. The current implementation supports structured handbook chapters, practice questions, KB reference validation, static HTML generation, and search/index metadata.

Implemented content coverage:

- DLBCL first-line reasoning
- Metastatic colorectal cancer first-line biomarker reasoning
- Metastatic NSCLC first-line driver-first reasoning
- Multiple myeloma first-line reasoning

Current seed volume:

- 4 `handbook_chapters`
- 12 `handbook_questions`

## Files Added Or Updated

Core schema and loader:

- `knowledge_base/schemas/handbook.py`
- `knowledge_base/schemas/__init__.py`
- `knowledge_base/validation/loader.py`

Static generation:

- `scripts/build_handbook.py`
- `scripts/build_site.py`

Specs and documentation:

- `specs/HANDBOOK_MODE_SPEC.md`
- `specs/README.md`
- `CLAUDE_CODE_OPENONCO_HANDBOOK_HANDOFF.md`

Seed content:

- `knowledge_base/hosted/content/handbook_chapters/*.yaml`
- `knowledge_base/hosted/content/handbook_questions/*.yaml`

Generated docs:

- `docs/handbook.html`
- `docs/handbook/*.html`
- `docs/handbook_index.json`

Tests:

- `tests/test_handbook_mode.py`

## Verification Already Run

Use these commands as the baseline regression suite for this feature:

```powershell
C:\Python312\python.exe -m knowledge_base.validation.loader knowledge_base/hosted/content
C:\Python312\python.exe scripts\build_handbook.py
C:\Python312\python.exe -m pytest tests\test_handbook_mode.py tests\test_loader.py
C:\Python312\python.exe -m py_compile scripts\build_handbook.py scripts\build_site.py knowledge_base\schemas\handbook.py tests\test_handbook_mode.py
```

Last known result:

- Loader succeeds and reports 4 handbook chapters and 12 handbook questions.
- Targeted pytest succeeds with 5 passing tests.
- Python compile checks succeed.
- Existing global KB contract warnings remain, but they are unrelated to the Handbook MVP.

## Important Product Rules

1. Do not copy ESMO handbook text, figures, tables, or CME questions.
2. Keep all handbook content OpenOnco-authored and source-linked.
3. Keep clinical claims tied to existing KB entities and sources where possible.
4. Treat handbook content as educational support, not medical advice or official guideline material.
5. Require clinical review before promoting `review_status` beyond `draft`.

## Next Agent Plan

### Phase 1: Site Integration

Goal: make the handbook discoverable in the existing static site.

Tasks:

- Inspect the current generated site layout and navigation patterns.
- Add a stable link from the main docs index/site navigation to `docs/handbook.html`.
- If the site has a common template, integrate there instead of hardcoding duplicate nav.
- Re-run `scripts/build_site.py` and confirm it also regenerates handbook assets.
- Add or update tests if the project already tests generated navigation.

Acceptance criteria:

- A user can reach the Handbook index from the main generated docs/site entry point.
- Existing site generation still succeeds.
- Handbook pages remain generated under `docs/handbook/`.

### Phase 2: Search And Filtering

Goal: make the Handbook usable once it has more than a few chapters.

Tasks:

- Extend `docs/handbook_index.json` only if needed, preserving backward-compatible fields.
- Add client-side filtering by disease, topic tags, and review status.
- Add text search over title, learning objectives, at-a-glance bullets, and source IDs.
- Keep the implementation static and dependency-free unless the existing site already has a frontend stack.

Acceptance criteria:

- Search works without a backend.
- Filtering does not require rebuilding the page after load.
- Search index includes all 4 current chapters and remains deterministic.

### Phase 3: Quiz Session Mode

Goal: turn question YAML into a usable self-check workflow.

Tasks:

- Add a static quiz/session page or per-chapter quiz mode.
- Support single-best-answer and multi-select questions.
- Show answer explanations after submission.
- Track local score in browser state only; do not add auth or persistence yet.
- Keep question rendering driven by `handbook_questions` YAML, not duplicated HTML.

Acceptance criteria:

- A learner can answer all questions in a chapter and see score/explanations.
- Multi-select correctness is evaluated exactly, not partially by accident.
- Question source IDs remain visible.

### Phase 4: Reviewer Workflow

Goal: make clinical governance explicit before content expands.

Tasks:

- Formalize status transitions for `draft`, `proposed`, `reviewed`, `needs_refresh`, and `retired`.
- Add validation warnings for stale `last_reviewed` values where status is `reviewed`.
- Decide whether Handbook review uses existing `reviewers` entities or needs a dedicated field.
- Add a test fixture proving invalid review metadata is caught.

Acceptance criteria:

- Draft content is allowed but visibly marked.
- Reviewed content requires enough metadata to audit ownership and review date.
- Stale content can be detected automatically.

### Phase 5: Content Expansion

Goal: expand coverage without weakening quality.

Recommended next chapters:

- Breast cancer HR+/HER2- metastatic first-line
- Breast cancer HER2+ metastatic first-line
- Prostate mCRPC biomarker and sequencing reasoning
- Ovarian cancer HRD/BRCA first-line maintenance reasoning
- Melanoma BRAF/IO first-line reasoning

For every new chapter:

- Link to disease, algorithm, indication, regimen, biomarker, redflag, test, and source entities.
- Include 2-4 sections.
- Include 2-3 case links where examples exist.
- Include 3-5 practice questions.
- Run loader validation before committing.

## Known Risks

- The generated HTML is intentionally simple and inline-styled. That is acceptable for MVP, but future UI work may need to align it with the rest of the docs site.
- The current search index is minimal. Extend it carefully so consumers do not break.
- Existing KB contract warnings can obscure new warnings. When adding content, inspect warnings around the files touched, not only the final pass/fail status.
- Some linked KB entities have placeholder-style labels. The Handbook renderer can expose that roughness, so future content work may require improving upstream entity titles.

## Suggested Next Commit After This One

Use a small follow-up commit focused only on site navigation and handbook discoverability:

```text
Expose OpenOnco Handbook in generated site navigation
```

Do not combine UI navigation, quiz mode, reviewer workflow, and new disease content in one commit.
