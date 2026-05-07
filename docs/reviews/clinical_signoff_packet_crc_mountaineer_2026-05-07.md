# Clinical Signoff Packet: CRC MOUNTAINEER Seed

## Packet Metadata

| Field | Value |
|---|---|
| Packet ID | `SIGNOFF-CRC-MOUNTAINEER-2026-05-07` |
| Created | 2026-05-07 |
| Workstream | Audit remediation Streams 1 and 2 |
| Reviewer role needed | GI medical oncology; access/reimbursement reviewer for drug rows |
| Entity family | `indications`, `drug_indications` |
| Entity IDs | `IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB`; `DIND-TUCATINIB-CRC-MOUNTAINEER`; `DIND-TRASTUZUMAB-CRC-MOUNTAINEER` |
| Target signoff scope | Outcome source traceability and draft drug-use row correctness |

## Changed Fields

| Entity ID | Field | Change type | Source refs |
|---|---|---|---|
| `IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB` | `expected_outcomes.overall_response_rate` | scalar to `OutcomeValue` | `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |
| `IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB` | `expected_outcomes.progression_free_survival` | scalar to `OutcomeValue` | `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |
| `IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB` | `expected_outcomes.overall_survival_median` | moved from median OS text in `overall_survival_5y` to semantically correct field | `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |
| `IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB` | `sources[]` | added trial sources | `SRC-MOUNTAINEER-STRICKLER-2022`, `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |
| `DIND-TUCATINIB-CRC-MOUNTAINEER` | full row | new draft row | `SRC-NCCN-COLON-2025`, `SRC-ESMO-COLON-2024`, `SRC-MOUNTAINEER-STRICKLER-2022`, `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |
| `DIND-TRASTUZUMAB-CRC-MOUNTAINEER` | full row | new draft row | `SRC-NCCN-COLON-2025`, `SRC-ESMO-COLON-2024`, `SRC-MOUNTAINEER-STRICKLER-2022`, `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` |

## Evidence Trail

| Source ID | Source type | Why it supports review |
|---|---|---|
| `SRC-MOUNTAINEER-STRICKLER-2022` | RCT publication | Local source note reports ORR 38.1%, median PFS 8.2 months, and median OS 24.1 months for tucatinib plus trastuzumab in HER2-positive RAS-WT chemotherapy-refractory mCRC |
| `SRC-MOUNTAINEER-FINAL-STRICKLER-2026` | RCT publication final analysis | Reports updated ORR 39.3%, median PFS 8.1 months, and median OS 23.9 months after extended follow-up |
| `SRC-NCCN-COLON-2025` | guideline | Existing indication/regimen source for recommended option and context |
| `SRC-ESMO-COLON-2024` | guideline | Existing indication/regimen source for HER2 amplification testing and anti-HER2 option context |

## Explicit Deferrals

- `complete_response` remains legacy scalar text because the local
  MOUNTAINEER source note does not explicitly support the complete-response
  percentage.
- Label/off-label and reimbursement fields in both `drug_indications` rows
  remain `unknown_pending_review`.

## Reviewer Checklist

- [ ] MOUNTAINEER source supports the three converted outcome values.
- [ ] `complete_response` should remain deferred or be source-verified.
- [ ] Draft drug-use rows correctly represent regimen components.
- [ ] Regulatory/reimbursement unknown status is appropriate pending
      jurisdiction-specific review.
- [ ] Packet can proceed to second reviewer or needs changes.

## Reviewer Decision

| Decision | Reviewer | Date | Rationale |
|---|---|---|---|
| pending |  |  |  |
