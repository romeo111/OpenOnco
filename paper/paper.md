---
title: "OpenOnco: an open-source, source-cited, rules-first clinical decision support engine for oncology tumor boards"
tags:
  - oncology
  - clinical decision support
  - knowledge base
  - rule engine
  - Python
  - FHIR
  - mCODE
authors:
  - name: "REPLACE WITH MAINTAINER NAME"        # maintainer: fill in
    orcid: "0000-0000-0000-0000"                # maintainer: add ORCID
    affiliation: 1
affiliations:
  - name: "Independent / REPLACE WITH AFFILIATION"
    index: 1
date: 18 June 2026
bibliography: paper.bib
---

<!--
DRAFT for maintainer review. Before submitting to JOSS (https://joss.theoj.org),
assess fit: JOSS targets research software; OpenOnco may also fit a medical-
informatics venue (JAMIA, JMIR, JMIR Medical Informatics). Fill in author
name/affiliation/ORCID, finalize references in paper.bib, and ensure the
software meets the venue's substance/test/documentation bar. Keep the honest
early-stage framing — do NOT overstate clinical validation.
-->

# Summary

`OpenOnco` is a free, open-source clinical decision support (CDS) system for
oncology multidisciplinary tumor boards. Given a structured patient profile
(a FHIR/mCODE-shaped JSON object describing disease, biomarkers, findings, and
demographics), a **deterministic rule engine** evaluates a versioned, fully
source-cited knowledge base and returns a plan containing at least two
alternative treatment tracks — a standard track and a more aggressive track —
side by side, each with its regimen, supportive care, contraindications,
monitoring schedule, a step-by-step decision trace, and a literature citation on
every recommendation. When histology is not yet confirmed, the engine returns a
diagnostic workup brief rather than a treatment plan. The engine runs offline
(command line, in-browser via Pyodide [@pyodide], Python import, or a Model
Context Protocol server), so patient data never leaves the user's device.

A defining design constraint is that **no large language model selects the
regimen or dose**: all clinical recommendations are produced by declarative
rules authored and reviewed by clinicians, so the system cannot hallucinate a
drug or a dose, and identical inputs against a given knowledge-base version
yield identical, auditable output.

# Statement of need

Selecting a regimen for a single oncology patient is hours of manual desk work:
cross-referencing multiple guidelines, checking biomarker actionability, verifying
renal/hepatic dose adjustments, layering supportive care, and confirming
contraindications. This burden is heaviest where specialist tumor boards are
scarce — rural settings and low- and middle-income countries — and a single
missed contraindication can be fatal.

General-purpose large language models are increasingly used for such questions,
but they can fabricate plausible-but-wrong drugs or doses, an unacceptable
failure mode in oncology. `OpenOnco` addresses this by keeping the clinical
decision in a deterministic rule engine over a curated, peer-reviewed knowledge
base, and by requiring a source citation for every claim (enforced by a
three-layer citation guard at load time, in continuous integration, and at
render time). Biomarker actionability is drawn from the openly licensed CIViC
knowledgebase [@civic]. Patient intake follows the HL7 FHIR [@fhir] and mCODE
[@mcode] data models, and the system deliberately avoids license-gated
terminologies in favor of open standards. An accompanying Model Context Protocol
server lets general assistants *call* the deterministic engine and relay its
cited output, rather than answering from memory.

`OpenOnco` is intended for healthcare professionals and is positioned as
informational, non-device clinical decision support; it is early-stage, most
knowledge-base content is marked provisional pending two-reviewer clinical
sign-off, and it has not undergone formal clinical validation. Every
recommendation must be verified by a qualified oncologist. The project is
released under the MIT license (code) and CC BY 4.0 (content) to enable
reuse and adaptation, including for resource-limited settings.

# Acknowledgements

We thank the open clinical-data communities whose resources OpenOnco builds on,
including CIViC and the HL7 FHIR/mCODE communities.

# References
