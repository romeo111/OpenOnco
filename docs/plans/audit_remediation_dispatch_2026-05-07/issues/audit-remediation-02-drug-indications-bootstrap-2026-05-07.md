# [Stream 2] Drug Indications Bootstrap

## Mission

Create the first-class `drug_indications` content queue for label,
off-label, and reimbursement status.

## Baseline

`docs/audits/clinical_gap_audit.md` reports:

- 654 inferred drug-disease-indication pairs.
- 0 explicit label/off-label statuses.
- 0 explicit reimbursement statuses.

The schema and loader are now present. Content still needs to be generated
and reviewed.

## First Step

Generate the candidate report:

```powershell
python scripts/backfill_drug_indications.py --report
```

Expected output:

`docs/audits/drug_indication_backfill_candidates.json`

## Work Plan

1. Inspect candidate IDs for duplicates and awkward context collapse.
2. Write draft YAML rows with:

```powershell
python scripts/backfill_drug_indications.py --write-yaml
```

3. Keep all generated rows as `draft: true`.
4. Prioritize reviewed status chunks for NSCLC, breast, CRC, ovarian, and
   DLBCL.
5. For each reviewed row, verify:
   - FDA label status
   - EMA label status
   - Ukraine registration/label state
   - NCCN/ESMO guideline support
   - NSZU or payer reimbursement status when relevant

## File Allowlist

- `knowledge_base/hosted/content/drug_indications/*.yaml`
- `knowledge_base/hosted/content/sources/*.yaml`
- `docs/audits/drug_indication_backfill_candidates.json`

## Quality Gate

- Every non-unknown status has source refs.
- Label status and reimbursement status are not conflated.
- Jurisdiction and payer are explicit.
- Off-label status distinguishes guideline-supported, compendia-supported,
  investigational, and not-labeled.

## Acceptance

Bootstrap is complete when every candidate pair has a draft
`drug_indications` row and the high-priority disease set has review chunks
ready for label/access verification.
