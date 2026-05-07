# [Stream 1] Outcome Citations Wave A

## Mission

Move the largest expected-outcome citation gaps from uncited to strict-cited.
This implements Stream 1 of
`docs/plans/audit_remediation_deep_plan_2026-05-07.md`.

## Baseline

`docs/audits/expected_outcomes_traceability_2026-05-01.md` reports:

- 1070 populated outcome cells.
- 100 strict-cited.
- 68 probably-cited.
- 902 uncited.

Wave A owns the five worst-offender diseases:

- `DIS-CRC`: 55 uncited
- `DIS-NSCLC`: 52 uncited
- `DIS-AML`: 51 uncited
- `DIS-OVARIAN`: 42 uncited
- `DIS-DLBCL-NOS`: 30 uncited

## First Step

Regenerate the backlog:

```powershell
python scripts/audit_expected_outcomes.py
```

Expected output:

`docs/audits/expected_outcomes_traceability_2026-05-01_backlog.json`

## Work Plan

1. Split the backlog by disease and indication.
2. For each disease, create part files of <=10 indications.
3. For each indication, identify the source that reports the exact
   endpoint value.
4. Reuse or create a `SRC-*` record with PMID/DOI/journal/year when
   available.
5. Convert scalar values to `OutcomeValue` dicts.
6. Rerun the audit and confirm the changed cells are `cited`.

## File Allowlist

- `knowledge_base/hosted/content/indications/*.yaml`
- `knowledge_base/hosted/content/sources/*.yaml`
- `docs/audits/expected_outcomes_traceability_2026-05-01*.md`
- `docs/audits/expected_outcomes_traceability_2026-05-01_backlog.json`

## Quality Gate

- No invented values.
- No invented source IDs.
- `SRC-LEGACY-UNCITED` only remains for explicitly deferred cells.
- Every changed populated outcome has `source` or `source_refs`.
- Audit rerun improves strict-cited count.

## Acceptance

Wave A is complete when the five named diseases have no unreviewed uncited
outcome cells except documented deferrals.
