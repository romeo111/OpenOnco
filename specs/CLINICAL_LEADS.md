# Clinical Co-Leads

Per [CHARTER §6.1](CHARTER.md), every change to clinical content
(`knowledge_base/hosted/content/{indications,regimens,redflags,
contraindications,supportive_care}/`) needs **two of three Clinical
Co-Lead approvals** before merge. STUB content stays STUB until that
threshold is reached.

This file is the public registry of active Co-Leads.

## Active Co-Leads

| Name | Sub-specialty area | Public profile | Joined |
|------|--------------------|----------------|--------|
| _seat open_ | _hematology / oncology / clinical pharmacology_ | _link to ORCID, hospital page, or PubMed_ | _YYYY-MM-DD_ |
| _seat open_ | _seat open_ | _seat open_ | _seat open_ |
| _seat open_ | _seat open_ | _seat open_ | _seat open_ |

## Becoming a Co-Lead

The role exists to keep the KB clinically defensible. Sub-specialty
depth in oncology / hematology / clinical pharmacology, plus
willingness to review structured YAML and source citations on a
recurring (not full-time) cadence.

### How to apply

1. Open a PR adding your row to the **Active Co-Leads** table above
   with: name, sub-specialty area, a public profile link (ORCID,
   hospital page, PubMed authorship, GitHub), and the date.
2. Or open a [Co-Lead application
   issue](https://github.com/romeo111/OpenOnco/issues/new?labels=co-lead-application&title=Co-Lead+application:+%5Byour+area%5D)
   with the same fields if you'd rather not edit a file.

Either path routes through public review — by design, no private
channel. The maintainer + existing Co-Leads (if any) review for
sub-specialty fit and conflict-of-interest disclosure
(CHARTER §7.1, §7.3 — currently dev-mode-exempt during v0.1; will be
binding once a Co-Lead seats are filled).

### Conflict of interest

Disclose any active financial or advisory relationships with
pharma / device manufacturers in your application. Disclosures land
in this file alongside the Co-Lead row.

### Removal / rotation

Self-rotation by PR (remove your row). Two-Co-Lead consensus PR for
removal-for-cause. No silent removal.

## What Co-Leads do

- Review clinical-content PRs (Indications, Regimens, RedFlags,
  Contraindications, SupportiveCare) for clinical accuracy + citation
  quality.
- Sign off via the audit log
  ([`knowledge_base/hosted/audit/signoffs.jsonl`](../knowledge_base/hosted/audit/signoffs.jsonl))
  — the signoff is auditable and tracked per entity.
- Flag KB drift between guidelines (NCCN / ESMO / EHA / ASH / BSH)
  and the YAML — CIViC nightly + monthly diffs help, but humans catch
  semantics CI can't.
- Help triage the [clinical-feedback issue
  queue](https://github.com/romeo111/OpenOnco/issues?q=label%3Aclinical-feedback).

## What Co-Leads do NOT do

- Make clinical decisions for individual patients (CHARTER §11 — this
  is decision-support, not a medical device).
- Endorse a single regimen as «the right one» — the engine always
  surfaces ≥2 alternatives (CHARTER §15.2 C6).
- Reply to private DMs — public audit trail by design.
