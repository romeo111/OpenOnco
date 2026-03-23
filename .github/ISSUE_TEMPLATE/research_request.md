---
name: Research Request
about: Request AI-generated research for a specific cancer type or patient scenario
title: "[RESEARCH REQUEST] "
labels: research-request, help-wanted
assignees: ''
---

## What cancer do you need researched?

**Cancer type:** <!-- Be specific: e.g. "Glioblastoma, IDH-wildtype, MGMT-methylated" not just "brain cancer" -->
**Stage:** <!-- e.g. WHO Grade 4 / Stage IIIB / Metastatic -->
**Key molecular markers:** <!-- e.g. EGFR L858R, PD-L1 TPS 60%, BRCA2 germline, etc. -->

## Patient context (optional — helps calibrate the research)

- **Age / sex:**
- **Performance status:** <!-- ECOG 0 / 1 / 2 / 3 -->
- **Prior treatments:** <!-- None / post-surgery / relapsed after... -->
- **Comorbidities:**

## What clinical question does this research need to answer?

<!-- Examples:
- What is the best first-line treatment for this specific molecular profile?
- Are there active clinical trials for this patient profile?
- What are the options after first-line treatment failure?
- Is de-escalated therapy appropriate for this stage/subtype?
-->

## Why this matters

<!-- Who needs this? Is this a common scenario, an underserved patient population,
     a rare cancer with few resources, etc.? -->

## Anything else

<!-- Links to relevant guidelines, trials you know about, specific drugs to evaluate, etc. -->

---

**What happens next:**
1. A maintainer will create a benchmark case from your request
2. A contributor with compute access will run the research
3. The scored report will be added to `research_db/` and linked here
4. You can query the results: `python database_api.py ask "..."`

*Average turnaround depends on contributor availability. Star the repo to follow along.*
