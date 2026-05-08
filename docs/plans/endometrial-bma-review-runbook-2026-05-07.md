# Endometrial BMA Review Runbook

This runbook breaks `DIS-ENDOMETRIAL` BMA review into queue-sized batches.
It is source-grounded planning only. Do not use it to author new clinical claims.
These packets are pre-review assets. Under the current workflow rule, `DIS-ENDOMETRIAL`
stays in fill lane until disease-level completion exceeds `80%`.

## Queue Order

1. `soc_dmmr_family`
2. `intermediate_family_audit`
3. `low_tier_tail`

## Commands

### 1. SOC DMMR Family

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json
```

Scope:
- `BIO-DMMR-IHC`
- 9 BMA records
- Goal: family-level review packet prep and metadata consistency audit

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan for those 9 `BIO-DMMR-IHC` records. Do not author new clinical claims. Do not edit files.
```

### 2. Intermediate Family Audit

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json
```

Scope:
- `BIO-CTNNB1`
- `BIO-FGFR2`
- `BIO-PIK3R1`
- Goal: clean review packets for single-record IIA/IIB families

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan for those 3 BMA records. Do not author new clinical claims. Do not edit files.
```

### 3. Low Tier Tail

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json
```

Scope:
- `BIO-KRAS-G12C`
- `BIO-RAS-MUTATION`
- `BIO-PIK3CA-MUTATION`
- `BIO-TP53-MUTATION`
- Goal: low-tier metadata cleanup and explicit separation from core SOC review work

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan for those 5 low-tier BMA records. Do not author new clinical claims. Do not edit files.
```

## Validation

```powershell
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --compact-json
```
