# [Stream 6] Supportive-Care Depth Wave A

## Mission

Start closing regimen supportive-care gaps by risk, not alphabetically.

## Baseline

`docs/audits/clinical_gap_audit.md` reports:

- 138/302 regimens have mandatory supportive care.
- 120 regimens are missing mandatory supportive care.
- 40 regimens have monitoring.
- 292 regimens have dose adjustments.

## First Step

Create a risk-ranked queue from the 120 missing regimens:

1. highly emetogenic chemotherapy,
2. platinum/taxane combinations,
3. anthracycline-containing regimens,
4. CAR-T, bispecifics, immune effector therapies,
5. TKIs with cardiac, hepatic, QT, ocular, or pneumonitis risk,
6. immunotherapy combinations,
7. lower-intensity oral maintenance.

## Work Plan

1. Parse missing regimen list from refreshed clinical gap audit.
2. Assign risk tier and toxicity family.
3. Start Wave A with <=20 high-risk regimens.
4. Add or reuse supportive-care entities.
5. Attach `mandatory_supportive_care`, `monitoring_schedule_id`,
   `dose_adjustments`, and patient watchpoints as appropriate.
6. Rerun validator and clinical gap audit.

## File Allowlist

- `knowledge_base/hosted/content/regimens/*.yaml`
- `knowledge_base/hosted/content/supportive_care/*.yaml`
- `knowledge_base/hosted/content/monitoring/*.yaml`
- `knowledge_base/hosted/content/sources/*.yaml`
- `docs/audits/clinical_gap_audit.*`

## Quality Gate

- Supportive-care IDs resolve.
- Monitoring IDs resolve.
- Patient watchpoints include urgency.
- Safety claims have source refs or explicit institution-protocol pending
  review status.
- No regimen loses existing dose adjustment or watchpoint content.

## Acceptance

Wave A is complete when the highest acute-toxicity missing regimens have
mandatory supportive care and monitoring coverage, with clean validator and
updated audit counts.
