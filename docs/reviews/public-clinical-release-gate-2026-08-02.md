# Clinical sign-off integrity — 2026-08-02

## Outcome

Clinical sign-off metadata is validated, auditable, and rendered as a review
signal. It is not a blanket availability switch for the public
clinical-question endpoint. That endpoint continues to provide an OpenOnco
tumor-board draft with its clinician-verification disclaimer; it is not an
autonomous clinical decision tool.

## Gate criteria

For a record to carry a clinically approved label or support a public
guideline-grade release, it needs two distinct, in-scope, qualified reviewer
sign-offs. A `scope_match: false` entry, placeholder reviewer, or pending
credentials does not qualify. An explicit `pending_clinical_signoff`
lifecycle status remains visible in the record and review dashboard.

Legacy `reviewer_signoffs_v2` is rejected by the KB validator and ignored by
the renderer. This prevents legacy, unvalidated metadata from being rendered
or treated as clinical approval.

## Contract migration

`scripts/clinical_signoff.py`, the sign-off dashboard, and renderer now share
the canonical structured field. The CLI records `timestamp`, `entity_version`,
and `scope_match`; its audit log remains append-only. The two legacy DLBCL
algorithm records were migrated without making their placeholder reviewer a
qualified approval.

## Verification

```powershell
py -3.12 scripts/audit_validator.py
py -3.12 -m pytest tests/test_source_ref_integrity.py tests/test_audit_validator_contracts.py tests/test_clinical_signoff_e2e.py tests/test_clinical_question_endpoint.py -q
git diff --check
```

Result at this revision: KB validation has 0 schema, reference, and contract
errors; targeted tests pass. The remaining unresolved-source queue is tracked
separately in `source-reference-audit-2026-08-02.md` and does not change the
endpoint's tumor-board-draft status.
