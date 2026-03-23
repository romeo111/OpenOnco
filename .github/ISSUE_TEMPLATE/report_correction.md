---
name: Report Correction
about: Flag a clinical inaccuracy, outdated data, or scoring error in an existing report
title: "[CORRECTION] "
labels: correction, clinical-review
assignees: ''
---

## Report

**File:** `research_db/.../reports/CASE_ID_report.json`
**Case ID:** <!-- e.g. HN-001 -->

## What is wrong

<!-- Describe the specific error — wrong OS data, wrong biomarker requirement, missing treatment, etc. -->

## Correct information

<!-- What should it say? Include citation if possible -->

**Source:**
- Study / trial name:
- Journal:
- Year:
- PMID or URL:

## Severity

- [ ] Critical — treatment recommendation is wrong or dangerous
- [ ] Significant — key data point is wrong (OS, HR, p-value)
- [ ] Minor — typo, formatting, or non-clinical detail
- [ ] Outdated — newer data supersedes this (specify new trial/approval)

## Suggested fix

<!-- Optional: paste the corrected JSON fragment -->
```json

```
