# Normalized Coverage Fill Backlog

This backlog ranks disease fill work from normalized clinical coverage, not raw YAML counts.
NSCLC is frozen for expansion by policy here; it should receive quality/signoff work only.

## Summary

- Active fill candidates: 0
- Ready-for-review diseases (>80%): 21
- Freeze-expansion diseases: 0
- Quality-only candidates: 0

## Highest Priority Fill Chunks

| Rank | Disease | Tier | Readiness | Score | SOC gap | IND gap | REG gap | Drug gap | RF gap | Current SOC/IND/REG/Drug/RF | Recommended chunk | Quality flags |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|

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

## Quality-Only Blockers

| Disease | Tier | Readiness | Current SOC/IND/REG/Drug/RF | Next step | Quality flags |
|---|---|---:|---|---|---|

## Planning Rules

- Do not normalize every disease toward NSCLC raw BMA volume.
- Diseases above 80% target completion move to `review_ready` and should go through review/signoff before more fill.
- Diseases below 80% stay in `fill_first` and should not consume clinician review bandwidth yet.
- Major solid tumors target broader SOC/actionable family and line-of-therapy coverage.
- Heme and high-value thin solid tumors target moderate breadth.
- Rare/thin diseases target a minimal truthful vertical: core indications, regimens, drugs, red flags, and only real actionable biomarkers.
- Quality flags are not expansion instructions; use them for signoff, attribution, ESCAT audit, and dedupe chunks.
