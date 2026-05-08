# Normalized Coverage Fill Backlog

This backlog ranks disease fill work from normalized clinical coverage, not raw YAML counts.
NSCLC is frozen for expansion by policy here; it should receive quality/signoff work only.

## Summary

- Active fill candidates: 55
- Ready-for-review diseases (>80%): 21
- Freeze-expansion diseases: 1
- Quality-only candidates: 1

## Highest Priority Fill Chunks

| Rank | Disease | Tier | Readiness | Score | SOC gap | IND gap | REG gap | Drug gap | RF gap | Current SOC/IND/REG/Drug/RF | Recommended chunk | Quality flags |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | DIS-ENDOMETRIAL | major_solid | 44.0% | 51 | 5 | 5 | 4 | 3 | 0 | 1/5/4/5/7 | Add 5 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, low_tier_dominant |
| 2 | DIS-GBM | major_solid | 35.2% | 46 | 1 | 6 | 7 | 7 | 2 | 1/4/1/1/5 | Create or backfill 3 linked regimen records referenced by existing indications. | signoff_cold, indication_signoff_cold, low_tier_dominant, missing_regimen_records |
| 3 | DIS-HNSCC | major_solid | 49.3% | 40 | 2 | 5 | 3 | 3 | 2 | 0/5/5/5/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | - |
| 4 | DIS-RCC | major_solid | 61.5% | 35 | 5 | 2 | 1 | 1 | 1 | 1/8/7/7/6 | Add 5 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| 5 | DIS-HCC | major_solid | 57.7% | 30 | 2 | 4 | 2 | 3 | 1 | 0/6/6/5/6 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| 6 | DIS-T-PLL | heme | 40.5% | 29 | 2 | 3 | 2 | 2 | 0 | 0/2/2/2/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 7 | DIS-HSTCL | heme | 45.2% | 27 | 2 | 3 | 2 | 0 | 0 | 0/2/2/7/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 8 | DIS-PDAC | major_solid | 62.0% | 27 | 0 | 6 | 4 | 1 | 0 | 2/4/4/7/9 | Add 6 indication records to close line-of-therapy sequencing. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| 9 | DIS-GRANULOSA-CELL | rare_or_thin | 0.0% | 26 | 1 | 2 | 2 | 2 | 5 | 0/0/0/0/0 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold |
| 10 | DIS-JMML | rare_or_thin | 0.0% | 26 | 1 | 2 | 2 | 2 | 5 | 0/0/0/0/0 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold |
| 11 | DIS-MENINGIOMA | rare_or_thin | 0.0% | 26 | 1 | 2 | 2 | 2 | 5 | 0/0/0/0/0 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold |
| 12 | DIS-MTC | high_value_solid_thin | 46.8% | 25 | 2 | 3 | 2 | 2 | 0 | 1/2/2/2/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold |
| 13 | DIS-THYROID-ANAPLASTIC | high_value_solid_thin | 46.8% | 25 | 2 | 3 | 2 | 2 | 0 | 1/2/2/2/6 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 14 | DIS-T-ALL | heme | 45.2% | 23 | 2 | 3 | 2 | 0 | 0 | 0/2/2/9/8 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 15 | DIS-EATL | heme | 51.4% | 22 | 1 | 3 | 2 | 0 | 0 | 0/2/2/7/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 16 | DIS-PMBCL | heme | 57.1% | 22 | 2 | 2 | 1 | 0 | 0 | 0/3/3/8/7 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 17 | DIS-THYROID-PAPILLARY | high_value_solid_thin | 43.2% | 21 | 0 | 4 | 3 | 3 | 0 | 2/1/1/1/5 | Add 4 indication records to close line-of-therapy sequencing. | signoff_cold, indication_signoff_cold |
| 18 | DIS-UROTHELIAL | major_solid | 70.4% | 21 | 0 | 4 | 2 | 3 | 2 | 3/6/6/5/5 | Add 4 indication records to close line-of-therapy sequencing. | signoff_cold, indication_signoff_cold |
| 19 | DIS-BCC | rare_or_thin | 22.7% | 21 | 0 | 2 | 2 | 2 | 5 | 2/0/0/0/0 | Add 2 indication records to close line-of-therapy sequencing. | signoff_cold |
| 20 | DIS-EPITHELIOID-SARCOMA | rare_or_thin | 22.7% | 21 | 0 | 2 | 2 | 2 | 5 | 1/0/0/0/0 | Add 2 indication records to close line-of-therapy sequencing. | signoff_cold |
| 21 | DIS-LAM | rare_or_thin | 22.7% | 21 | 0 | 2 | 2 | 2 | 5 | 1/0/0/0/0 | Add 2 indication records to close line-of-therapy sequencing. | signoff_cold |
| 22 | DIS-TGCT | rare_or_thin | 22.7% | 21 | 0 | 2 | 2 | 2 | 5 | 1/0/0/0/0 | Add 2 indication records to close line-of-therapy sequencing. | signoff_cold |
| 23 | DIS-MDS-HR | heme | 52.4% | 20 | 2 | 2 | 1 | 2 | 0 | 0/3/3/2/9 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold, variant_inflation_3.67x, low_tier_dominant |
| 24 | DIS-HGBL-DH | heme | 57.1% | 18 | 2 | 2 | 1 | 0 | 0 | 0/3/3/8/7 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 25 | DIS-HCL | heme | 59.5% | 17 | 1 | 2 | 2 | 2 | 0 | 1/3/2/2/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 26 | DIS-NK-T-NASAL | heme | 64.9% | 17 | 1 | 2 | 1 | 0 | 0 | 0/3/3/8/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 27 | DIS-PTCL-NOS | heme | 69.0% | 17 | 2 | 1 | 0 | 0 | 0 | 0/4/4/8/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 28 | DIS-NODAL-MZL | heme | 61.9% | 16 | 2 | 1 | 1 | 1 | 0 | 0/4/3/3/5 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 29 | DIS-GASTRIC | major_solid | 77.5% | 16 | 0 | 4 | 2 | 0 | 0 | 3/6/6/12/8 | Add 4 indication records to close line-of-therapy sequencing. | signoff_cold, low_tier_dominant |
| 30 | DIS-NLPBL | heme | 59.5% | 15 | 1 | 2 | 2 | 0 | 0 | 0/3/2/5/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 31 | DIS-IMT | rare_or_thin | 50.0% | 15 | 1 | 1 | 1 | 1 | 0 | 0/1/1/1/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 32 | DIS-HCV-MZL | heme | 62.2% | 14 | 1 | 2 | 1 | 1 | 0 | 0/3/3/3/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 33 | DIS-SPLENIC-MZL | heme | 62.2% | 14 | 1 | 2 | 1 | 1 | 0 | 0/3/3/3/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 34 | DIS-MPNST | rare_or_thin | 54.5% | 14 | 1 | 1 | 1 | 0 | 0 | 0/1/1/2/6 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |
| 35 | DIS-ATLL | heme | 64.9% | 13 | 1 | 2 | 1 | 0 | 0 | 0/3/3/9/6 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 36 | DIS-MDS-LR | heme | 69.0% | 13 | 2 | 1 | 0 | 0 | 0 | 0/4/4/4/8 | Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold, variant_inflation_3.00x, low_tier_dominant |
| 37 | DIS-PCNSL | heme | 64.9% | 13 | 1 | 2 | 1 | 0 | 0 | 0/3/3/6/6 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 38 | DIS-PTLD | heme | 64.9% | 13 | 1 | 2 | 1 | 0 | 0 | 0/3/3/5/5 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 39 | DIS-CERVICAL | high_value_solid_thin | 64.9% | 13 | 1 | 2 | 1 | 0 | 0 | 0/3/3/6/6 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | signoff_cold, indication_signoff_cold |
| 40 | DIS-APL | heme | 78.4% | 12 | 1 | 1 | 0 | 0 | 0 | 0/4/4/4/9 | Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis. | indication_signoff_cold |

## Ready For Review

| Disease | Tier | Readiness | Current SOC/IND/REG/Drug/RF | Next step | Quality flags |
|---|---|---:|---|---|---|
| DIS-ALCL | heme | 88.1% | 1/5/5/6/5 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-AML | heme | 100.0% | 4/15/10/13/16 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-B-ALL | heme | 100.0% | 2/6/5/14/8 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-BURKITT | heme | 88.1% | 1/5/5/13/6 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-CHL | heme | 100.0% | 1/7/5/7/5 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-CLL | heme | 88.1% | 1/7/5/7/12 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-CML | heme | 100.0% | 1/5/5/7/9 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, variant_inflation_5.00x |
| DIS-FL | heme | 88.1% | 1/7/6/10/8 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-MCL | heme | 100.0% | 2/7/6/11/9 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-MF-SEZARY | heme | 83.8% | 0/5/4/3/5 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-PMF | heme | 97.6% | 2/5/4/3/7 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-PV | heme | 88.1% | 1/6/4/5/6 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-WM | heme | 100.0% | 2/5/5/6/6 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-CHOLANGIOCARCINOMA | high_value_solid_thin | 91.9% | 3/4/4/5/6 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold |
| DIS-BREAST | major_solid | 100.0% | 6/26/17/24/20 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, variant_inflation_4.62x, low_tier_dominant |
| DIS-CRC | major_solid | 100.0% | 6/22/15/16/9 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, variant_inflation_3.22x, low_tier_dominant |
| DIS-MELANOMA | major_solid | 83.5% | 3/11/8/12/11 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, low_tier_dominant |
| DIS-OVARIAN | major_solid | 89.0% | 4/15/11/11/13 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, variant_inflation_4.88x, low_tier_dominant |
| DIS-PROSTATE | major_solid | 91.5% | 4/8/8/8/15 | Eligible for disease-level review/signoff workflow. | signoff_cold, indication_signoff_cold, variant_inflation_3.33x |
| DIS-GIST | rare_or_thin | 100.0% | 3/3/3/3/5 | Eligible for disease-level review/signoff workflow. | signoff_cold, variant_inflation_3.00x |
| DIS-MASTOCYTOSIS | rare_or_thin | 100.0% | 1/2/2/2/5 | Eligible for disease-level review/signoff workflow. | signoff_cold |

## Freeze Expansion

| Disease | Readiness | Current BMA | Families | SOC families | IND | Drugs | Regimens | RF | Required work |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DIS-NSCLC | 100.0% | 41 | 17 | 8 | 40 | 26 | 24 | 26 | Freeze expansion; run signoff, ESCAT/source audit, and dedupe only. |

## Quality-Only Blockers

| Disease | Tier | Readiness | Current SOC/IND/REG/Drug/RF | Next step | Quality flags |
|---|---|---:|---|---|---|
| DIS-ESOPHAGEAL | high_value_solid_thin | 100.0% | 1/6/4/4/6 | Create or backfill 2 linked regimen records referenced by existing indications. | signoff_cold, low_tier_dominant, missing_regimen_records |

## Planning Rules

- Do not normalize every disease toward NSCLC raw BMA volume.
- Diseases above 80% target completion move to `review_ready` and should go through review/signoff before more fill.
- Diseases below 80% stay in `fill_first` and should not consume clinician review bandwidth yet.
- Major solid tumors target broader SOC/actionable family and line-of-therapy coverage.
- Heme and high-value thin solid tumors target moderate breadth.
- Rare/thin diseases target a minimal truthful vertical: core indications, regimens, drugs, red flags, and only real actionable biomarkers.
- Quality flags are not expansion instructions; use them for signoff, attribution, ESCAT audit, and dedupe chunks.
