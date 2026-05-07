# [Stream 5] Solid Tumor 2L+ Coverage Queue

## Mission

Create an authoring queue for solid diseases missing advanced-line
algorithm or indication coverage.

## Baseline

`docs/audits/clinical_gap_audit.md` reports:

- 21/42 solid diseases have a 2L+ algorithm.
- 18/42 solid diseases have a 2L+ indication.

Missing 2L+ algorithm rows:

`DIS-ANAL-SCC`, `DIS-BCC`, `DIS-CERVICAL`, `DIS-CHONDROSARCOMA`,
`DIS-EPITHELIOID-SARCOMA`, `DIS-GI-NET`, `DIS-GIST`,
`DIS-GLIOMA-LOW-GRADE`, `DIS-GRANULOSA-CELL`, `DIS-IFS`, `DIS-IMT`,
`DIS-LAM`, `DIS-MENINGIOMA`, `DIS-MESOTHELIOMA`, `DIS-MPNST`,
`DIS-MTC`, `DIS-PNET`, `DIS-SALIVARY`, `DIS-TGCT`,
`DIS-THYROID-ANAPLASTIC`, `DIS-THYROID-PAPILLARY`.

## First Step

Classify each missing disease into one of four advanced-line patterns:

- systemic 2L+ standard exists,
- targeted option exists after molecular selection,
- local therapy or surgery/radiation dominates recurrence management,
- no standard systemic path; trial referral or best supportive care should
  be explicit.

## Work Plan

1. Build disease queue with the four pattern labels.
2. Start high-value Wave A: cervical, GIST, MTC, PNET, salivary.
3. Author one disease per chunk.
4. Add indication first, then algorithm link.
5. Add expected outcomes and source refs before declaring coverage moved.

## File Allowlist

- `knowledge_base/hosted/content/indications/*.yaml`
- `knowledge_base/hosted/content/algorithms/*.yaml`
- `knowledge_base/hosted/content/regimens/*.yaml`
- `knowledge_base/hosted/content/sources/*.yaml`
- `docs/audits/clinical_gap_audit.*`
- `docs/kb-coverage-matrix.md`

## Quality Gate

- Every new advanced-line indication has source refs and expected outcomes.
- Algorithm default and alternatives resolve to indication IDs.
- If no 2L+ standard exists, the KB has an explicit sourced deferral state.
- Validation and coverage matrix rerun cleanly.

## Acceptance

The queue starter is complete when all missing diseases are classified and
Wave A disease specs are ready.
