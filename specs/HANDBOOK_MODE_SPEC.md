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

## 6. Rendering Contract

The static renderer must show:

- title, audience, language, and review status;
- learning objectives and at-a-glance bullets;
- section-level source IDs;
- linked entity chips;
- synthetic case links;
- practice questions with hidden explanations;
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
