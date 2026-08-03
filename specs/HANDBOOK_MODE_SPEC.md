# Handbook Mode Specification

## 1. Purpose

Handbook Mode is an OpenOnco-authored educational layer for oncology learning,
exam-style preparation, and source-grounded clinical reasoning practice.

It is not:

- official ESMO material;
- a CME-credit provider;
- patient-specific medical advice;
- a treatment-selection pathway separate from the OpenOnco rule engine.

## 2. Legal Boundary

Handbook chapters must be original OpenOnco content. Authors must not copy,
translate, paraphrase, or structurally clone ESMO handbooks, official CME
questions, tables, figures, screenshots, or paywalled/member-only material.

Permitted source use:

- cite Source IDs from the OpenOnco KB;
- summarize guideline positions in OpenOnco's own words;
- link to original source records;
- use synthetic cases authored in the repository.

## 3. Audience

The initial audience is `hcp_learner`: clinicians, trainees, contributors, and
maintainers using synthetic scenarios to learn oncology reasoning.

Handbook Mode must not be positioned as direct-to-patient guidance. A simplified
learner summary is permitted only when it is clearly educational and not framed
as patient instructions.

## 4. Content Entities

Two first-class KB entities define Handbook Mode:

- `handbook_chapters/`: educational chapters linked to diseases, algorithms,
  indications, regimens, biomarkers, red flags, tests, workups, and sources.
- `handbook_questions/`: practice questions linked to exactly one chapter and
  grounded in source IDs.

Every chapter must include:

- `learning_objectives`;
- `at_a_glance`;
- `source_ids`;
- `review_status`;
- linked KB entities where applicable.

Every objective question must include:

- a stem;
- options;
- a correct answer;
- an explanation;
- `source_ids`.

## 5. Review Lifecycle

Allowed `review_status` values:

- `draft`: authored or generated, not clinically reviewed;
- `proposed`: ready for clinical review;
- `reviewed`: clinically reviewed and signed off;
- `needs_refresh`: a source or linked entity changed after review;
- `retired`: no longer suitable for learning use.

Questions follow the same lifecycle as chapters. A question explanation can be
clinically unsafe even when the chapter prose is correct, so question review is
not optional.

### 5.1 Reviewer field decision

Handbook entities reuse the existing `ReviewerProfile` (REV-*) entities and
`ReviewerSignoff` value object that already gate clinical content elsewhere
(RedFlag, Indication, etc.). No dedicated `handbook_reviewers` field — the
governance regime is the same as CHARTER §6.1 and there is no value in
forking the reviewer roster per content type.

`HandbookChapter.reviewer_signoffs` and `HandbookQuestion.reviewer_signoffs`
are typed as `list[ReviewerSignoff]`. Each signoff carries `reviewer_id`
(must resolve to a REV-* entity), `timestamp` (ISO 8601), and optional
`rationale` / `entity_version`.

### 5.2 Status → metadata requirements (schema-enforced)

| `review_status` | `last_reviewed` | `reviewer_signoffs` | Notes |
| --- | --- | --- | --- |
| `draft` | not required | not required | default for new content. |
| `proposed` | required (ISO date) | ≥1 | content has been read by a clinical reviewer, awaiting second signoff. |
| `reviewed` | required (ISO date) | ≥2, from distinct reviewer IDs | mirrors CHARTER §6.1 two-reviewer publish gate. |
| `needs_refresh` | required (ISO date) | may carry prior signoffs | content was previously reviewed and went stale. |
| `retired` | optional | optional | terminal state; renderer should not surface in active index. |

The Pydantic model rejects any entity that declares one of `proposed`,
`reviewed`, or `needs_refresh` without the required metadata. This is **not**
a change to the CHARTER §6.1 dev-mode exemption that allows draft and
proposed content to exist without two-reviewer signoffs during the v0.1
phase — the schema only fires when the author *claims* a higher review
state.

### 5.3 Staleness (loader-emitted warning)

`review_status: reviewed` content carries a freshness budget of **365 days**
from the date in `last_reviewed`. The loader emits a `contract_warning`
(non-blocking) when a `reviewed` entity is older than that, recommending a
transition to `needs_refresh`. The renderer surfaces the same condition as a
red `stale (>365d)` badge next to the status badge on the chapter page.

The threshold is enforced in code at
`knowledge_base/validation/loader.py:HANDBOOK_REVIEW_STALE_DAYS`.

### 5.4 Loader cross-checks

Beyond the schema's intrinsic invariants, `load_content` also verifies that
each `reviewer_signoffs[*].reviewer_id` resolves to a `reviewers/REV-*`
entity. Unresolved reviewer IDs surface as `ref_errors`, not warnings,
because a sign-off pointing at a non-existent reviewer is a data-integrity
problem that the publish gate cannot interpret.

## 6. Rendering Contract

The static renderer must show:

- title, audience, language, and review status (status-aware badge plus a
  red `stale` indicator when §5.3 is triggered);
- learning objectives and at-a-glance bullets;
- section-level source IDs;
- linked entity chips;
- synthetic case links;
- practice questions as an interactive quiz (Phase 3): radios for `type_a`
  and `mcq`, checkboxes for `type_k`, free text + reveal for `short_answer`;
  per-question result panels expose source IDs and reasoning tags; the
  chapter-level score is held in `sessionStorage` only;
- a review panel with `last_reviewed`, resolved reviewer names from each
  `ReviewerSignoff`, and a link back to §5 of this spec. Placeholder
  reviewer names (e.g. `[Solid-Tumor Co-Lead — to be filled]`) must be
  surfaced via the reviewer's `specialty` field plus a "placeholder" tag,
  never as a bracketed string masquerading as a real signature;
- a disclaimer that the content is OpenOnco-authored educational material.

The renderer must be deterministic. LLMs may assist draft authoring, but the
site build path renders checked-in YAML only.

## 7. Initial MVP

The first MVP chapter is `HB-DLBCL-1L`, covering first-line DLBCL reasoning:

- diagnostic minimum;
- R-CHOP standard track;
- Pola-R-CHP intensified track;
- IPI and biology red flags;
- viral screening, CNS-risk, cardiac safety, and other common traps;
- synthetic case links;
- practice questions.
