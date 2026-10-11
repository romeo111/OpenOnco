# OpenOnco — current promotion fact sheet

Updated 2026-10-12. Verify changing counts and functionality against the [live capabilities page](https://openonco.info/capabilities.html) before an external post. This sheet replaces the June 2026 counts and broad privacy claims in older files under `promo/`.

## Safe short description

OpenOnco is a free, open-source, early-stage solo project for oncology decision support. One maintainer delivers updates with automated checks and source traceability. Its deterministic rule engine drafts source-linked options for discussion with a qualified clinician. External clinical review is optional and recorded separately; there is no two-reviewer quota for development or publication. Technical checks are not clinical validation or approval of individual treatment.

## Verified scope and maturity

- The [capabilities page](https://openonco.info/capabilities.html) reported 103 diseases, 831 indications, 404 regimens and 542 sources on 2026-10-11. These are **coverage counts**, not evidence of clinical approval or improved patient outcomes.
- The current source audit on 2026-10-12 found **0/2,570** clinical records with two eligible current reviews. The denominator includes indications, algorithms, regimens, red flags and biomarker-actionability records, even when no review field is present. Five raw structured historical review rows and legacy numeric counters do not establish current authorization, scope, revision or reviewer independence. This does not deny historical clinician feedback. Recheck the source audit before reusing the number; content reviews are not approval of an individual treatment plan.
- The [Plan Builder](https://openonco.info/try.html) can run on synthetic profiles in the browser. A generated draft is for clinician verification; its main and alternative options are not prescriptions or a ranking of clinical superiority. Some profiles yield one option, incomplete output or a diagnostic brief.
- The public site includes source-linked Wiki pages and draft ES/PT/DE/FR translations. Those editions are labeled `pending_language_review`; structural translation checks do not amount to independent clinical review.
- OpenOnco has no completed formal clinical validation study documented in this repository. Do not call it clinically validated, peer-reviewed as a clinical intervention, FDA-cleared, CE-marked, or production-ready.

## Data flow and limits

- The browser Plan Builder and server-backed Tumor Board have **different** data flows. Do not claim that all patient data stays on-device or that every OpenOnco path is offline. Explain the specific interface being discussed and use synthetic examples for demonstrations.
- An LLM must not choose regimens or doses under [CHARTER §8.3](../specs/CHARTER.md); the clinical rule engine remains deterministic. This does not eliminate errors in draft knowledge-base content, citations, translations or input data.
- The project aims at informational support for healthcare professionals. Its patient-facing report is for discussion with a clinician, not self-diagnosis or self-treatment. No real patient case should appear in a public launch without the project's consent, de-identification and ethics requirements.
- FHIR/mCODE alignment is a roadmap and gap-analysis topic. Do not claim conformance, an implemented EHR adapter, OHDSI affiliation or endorsement without corresponding evidence.

## Required language in any outward-facing asset

> OpenOnco is an early-stage informational decision-support project, not a medical device. Clinical content and translations may still be awaiting review. A qualified treating oncologist must verify every recommendation. Do not use it for self-treatment or urgent decisions.

Identify yourself as the project maintainer or contributor where appropriate. Describe example cases as synthetic. Link to the [repository](https://github.com/romeo111/OpenOnco), [site](https://openonco.info/) and the specific live feature you have verified. Do not imply that a directory listing, search submission, academic draft or community mention is an endorsement.

## Publication gate

Before posting an older `promo/` draft, replace stale figures and privacy claims, verify every link and feature against the deployed site, keep the safety paragraph above, and have a domain-appropriate reviewer check clinical assertions. External posts and partner messages require the maintainer's own account and judgment; a prepared draft is not a sent message or accepted submission.
