# Endometrial Clinical Review Plan

This document closes the technical planning phase for `DIS-ENDOMETRIAL`.
It is source-grounded planning only. It does not author new clinical claims.
Under the current workflow rule, only diseases above `80%` target completion should enter disease-level review.

## Status

- Stale source cleanup: complete
- Queue slicing and low-token tooling: complete
- Review-packet tooling: complete
- BMA metadata consistency cleanup: complete
- Clinical review packets prepared: complete
- Workflow lane: `fill_first`
- Disease-level review/signoff: blocked until target completion exceeds `80%`

## Current State

- Disease: `DIS-ENDOMETRIAL`
- BMA rows: `17`
- BMA metadata-ready: `17/17`
- Review readiness: `44.0%`
- Review queues:
  1. `soc_dmmr_family` - `9` rows
  2. `intermediate_family_audit` - `3` rows
  3. `low_tier_tail` - `5` rows

## Queue Order

These packets are review-prep assets only. They should not consume clinician review bandwidth yet.

1. `soc_dmmr_family`
2. `intermediate_family_audit`
3. `low_tier_tail`

## Queue Summary

### 1. SOC DMMR Family

- Review packet: `docs/plans/endometrial-review-packet-soc-dmmr-2026-05-07.md`
- Metadata-ready: `9/9`
- Shared primary sources:
  - `SRC-NCCN-UTERINE-2025`
  - `SRC-ESGO-ENDOMETRIAL-2025`
- Main reviewer question:
  - confirm family-level dMMR framing and handle `BMA-EPCAM-GERMLINE-ENDOMETRIAL` as the only likely source-framing edge case

Low-token command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json
```

### 2. Intermediate Family Audit

- Review packet: `docs/plans/endometrial-review-packet-intermediate-2026-05-07.md`
- Metadata-ready: `3/3`
- Shared primary sources:
  - `SRC-NCCN-UTERINE-2025`
  - `SRC-ESGO-ENDOMETRIAL-2025`
- Main reviewer questions:
  - confirm `CTNNB1` remains guideline-led prognostic/risk-stratification content
  - confirm `PIK3R1` remains pathway-level actionability content
  - confirm `FGFR2` source-role pattern is acceptable with CIViC-only `evidence_sources`

Low-token command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json
```

### 3. Low Tier Tail

- Review packet: `docs/plans/endometrial-review-packet-low-tier-2026-05-07.md`
- Metadata-ready: `5/5`
- Shared primary sources:
  - `SRC-NCCN-UTERINE-2025`
- Main reviewer questions:
  - keep `KRAS G12C` distinct from `BIO-RAS-MUTATION` low-tier rows
  - confirm `PIK3CA` remains exploratory/pathway-level
  - confirm `TP53` remains prognostic rather than therapeutic

Low-token command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json
```

## Definition of Complete

This planning phase is complete when:

- all three queue review packets exist in repo docs
- all queue rows are metadata-ready
- no stale endometrial source ids remain
- runbook and review-packet commands are stable

The next phase is not immediate clinician signoff. It is normalized fill work until `DIS-ENDOMETRIAL` crosses the `80%` review gate, then clinician review/signoff.
