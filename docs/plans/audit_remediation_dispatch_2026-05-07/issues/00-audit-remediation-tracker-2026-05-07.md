# [Tracker] Audit Remediation Dispatch 2026-05-07

## Mission

Track the six audit-remediation workstreams started from
`docs/plans/audit_remediation_deep_plan_2026-05-07.md`.

This tracker owns the transition from broad audit findings to executable
chunks. It does not itself change clinical KB content.

## Sub-issues Checklist

- [ ] audit-remediation-01-outcome-citations-wave-a-2026-05-07
- [ ] audit-remediation-02-drug-indications-bootstrap-2026-05-07
- [ ] audit-remediation-03-modality-structure-bootstrap-2026-05-07
- [ ] audit-remediation-04-clinical-signoff-packets-2026-05-07
- [ ] audit-remediation-05-solid-2l-coverage-queue-2026-05-07
- [ ] audit-remediation-06-supportive-care-depth-wave-a-2026-05-07

## Bootstrap Commands

Run once Python is available:

```powershell
python scripts/audit_expected_outcomes.py
python scripts/backfill_drug_indications.py --report
python scripts/audit_modality_structure.py
python scripts/audit_clinical_gaps.py
python scripts/kb_coverage_matrix.py
python -m knowledge_base.validation.loader knowledge_base/hosted/content
pytest tests/test_expected_outcomes_audit.py tests/test_drug_indication_schema.py tests/test_modality_schema.py tests/test_loader.py
```

## Sequencing

1. Generate the three missing machine-readable queues.
2. Start outcome citations Wave A and drug-indication draft backfill in
   parallel.
3. Start modality and supportive-care Wave A after queues are refreshed.
4. Create clinical signoff packets only after each content chunk has a
   stable source-backed diff.
5. Start solid 2L+ authoring after modality triage separates systemic
   pathways from local-therapy pathways.

## Global Quality Gates

1. KB validator clean.
2. No generated draft row is treated as reviewed.
3. No invented source IDs, trial data, label status, or reimbursement state.
4. Each content chunk names the exact entity IDs it owns.
5. Each content chunk names the audit metric it moves.
