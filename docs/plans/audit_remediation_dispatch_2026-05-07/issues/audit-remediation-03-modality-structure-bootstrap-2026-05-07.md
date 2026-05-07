# [Stream 3] Modality Structure Bootstrap

## Mission

Convert surgery/radiation prose mentions into a reviewed queue for
structured modality records.

## Baseline

`docs/audits/clinical_gap_audit.md` reports:

- 344 indications mention surgery or radiation in text.
- 0 structured surgery entities.
- 0 structured radiation entities.

The schema and loader are now present. Content migration has not started.

## First Step

Generate the modality triage report:

```powershell
python scripts/audit_modality_structure.py
```

Expected output:

`docs/audits/modality_structure_audit.json`

## Work Plan

1. Split candidate mentions into surgery, radiation, and combined CRT
   queues.
2. Remove false positives where prose mentions are historical context only.
3. Start Wave A with CRC, breast, NSCLC, ovarian, cervical, and anal.
4. For each record, author the modality entity only from source-backed
   clinical content.
5. Keep records `draft: true` until specialist review.

## File Allowlist

- `knowledge_base/hosted/content/surgery/*.yaml`
- `knowledge_base/hosted/content/radiation/*.yaml`
- `knowledge_base/hosted/content/sources/*.yaml`
- `docs/audits/modality_structure_audit.json`

## Quality Gate

- Every modality record has `disease_id`, intent, source refs, and either
  indication links or explicit disease-level scope.
- Radiation dose/fractionation is populated only when source-backed.
- Surgery procedure names are specific enough for review but not
  over-prescriptive.
- Engine selection behavior does not change.

## Acceptance

Bootstrap is complete when the triage report exists and Wave A has
review-ready modality authoring chunks.
