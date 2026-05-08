# Normalized Actionability Coverage

This report separates raw YAML volume from normalized disease-level clinical coverage.
It is an observability layer only; it does not change clinical recommendations.

## Summary

- Diseases: 78
- Raw BMA records: 435
- Normalized disease x biomarker-family buckets: 211
- BMA records with >=2 signoffs or signed status: 0
- Diseases with variant-family inflation >=2.0x: 16

## Top Diseases By Raw BMA Volume

| Disease | Archetype | BMA | Families | Inflation | SOC families | Approved/guideline families | Low/investigational BMA | Resistance BMA | Drugs | Regimens | IND | RF | BMA signed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DIS-NSCLC | biomarker_driven | 41 | 17 | 2.41x | 8 | 17 | 25 | 5 | 26 | 24 | 40 | 26 | 0.0% |
| DIS-OVARIAN | biomarker_driven | 39 | 8 | 4.88x | 4 | 8 | 21 | 0 | 11 | 11 | 15 | 13 | 0.0% |
| DIS-BREAST | biomarker_driven | 37 | 8 | 4.62x | 6 | 8 | 25 | 0 | 24 | 17 | 26 | 20 | 0.0% |
| DIS-CRC | stage_driven | 29 | 9 | 3.22x | 6 | 9 | 17 | 0 | 16 | 15 | 22 | 9 | 0.0% |
| DIS-AML | risk_stratified | 26 | 10 | 2.60x | 4 | 10 | 22 | 3 | 13 | 10 | 15 | 16 | 0.0% |
| DIS-PROSTATE | line_of_therapy_sequential | 20 | 6 | 3.33x | 4 | 6 | 3 | 0 | 8 | 8 | 8 | 15 | 0.0% |
| DIS-PDAC | stage_driven | 18 | 9 | 2.00x | 2 | 9 | 13 | 0 | 7 | 4 | 4 | 9 | 0.0% |
| DIS-ENDOMETRIAL | biomarker_driven | 17 | 8 | 2.12x | 1 | 8 | 17 | 0 | 5 | 4 | 5 | 7 | 0.0% |
| DIS-GASTRIC | stage_driven | 16 | 9 | 1.78x | 3 | 9 | 7 | 2 | 12 | 6 | 6 | 8 | 0.0% |
| DIS-UROTHELIAL | line_of_therapy_sequential | 16 | 6 | 2.67x | 3 | 6 | 3 | 0 | 5 | 6 | 6 | 5 | 0.0% |
| DIS-DLBCL-NOS | risk_stratified | 13 | 8 | 1.62x | 0 | 8 | 13 | 0 | 14 | 8 | 12 | 15 | 0.0% |
| DIS-MCL | risk_stratified | 11 | 7 | 1.57x | 2 | 7 | 4 | 0 | 11 | 6 | 7 | 9 | 0.0% |
| DIS-MDS-HR | risk_stratified | 11 | 3 | 3.67x | 0 | 3 | 11 | 0 | 2 | 3 | 3 | 9 | 0.0% |
| DIS-MELANOMA | biomarker_driven | 11 | 6 | 1.83x | 3 | 6 | 9 | 0 | 12 | 8 | 11 | 11 | 0.0% |
| DIS-CLL | risk_stratified | 10 | 6 | 1.67x | 1 | 6 | 8 | 2 | 7 | 5 | 7 | 12 | 0.0% |
| DIS-GBM | stage_driven | 10 | 6 | 1.67x | 1 | 6 | 6 | 0 | 1 | 4 | 4 | 5 | 0.0% |
| DIS-MM | risk_stratified | 10 | 6 | 1.67x | 0 | 6 | 5 | 0 | 12 | 10 | 13 | 14 | 0.0% |
| DIS-GIST | biomarker_driven | 9 | 3 | 3.00x | 3 | 3 | 2 | 0 | 3 | 3 | 3 | 5 | 0.0% |
| DIS-B-ALL | biomarker_driven | 7 | 4 | 1.75x | 2 | 3 | 5 | 0 | 14 | 5 | 6 | 8 | 0.0% |
| DIS-HCC | stage_driven | 6 | 6 | 1.00x | 0 | 6 | 5 | 0 | 5 | 6 | 6 | 6 | 0.0% |
| DIS-MDS-LR | risk_stratified | 6 | 2 | 3.00x | 0 | 2 | 6 | 0 | 4 | 4 | 4 | 8 | 0.0% |
| DIS-CML | etiologically_driven | 5 | 1 | 5.00x | 1 | 1 | 1 | 0 | 7 | 5 | 5 | 9 | 0.0% |
| DIS-RCC | biomarker_driven | 5 | 5 | 1.00x | 1 | 4 | 3 | 0 | 7 | 7 | 8 | 6 | 0.0% |
| DIS-CHOLANGIOCARCINOMA | stage_driven | 4 | 3 | 1.33x | 3 | 3 | 1 | 0 | 5 | 4 | 4 | 6 | 0.0% |
| DIS-FL | risk_stratified | 4 | 4 | 1.00x | 1 | 4 | 4 | 2 | 10 | 6 | 7 | 8 | 0.0% |
| DIS-ESOPHAGEAL | stage_driven | 3 | 3 | 1.00x | 1 | 3 | 2 | 0 | 4 | 6 | 6 | 6 | 0.0% |
| DIS-THYROID-PAPILLARY | stage_driven | 3 | 3 | 1.00x | 2 | 3 | 1 | 0 | 1 | 1 | 1 | 5 | 0.0% |
| DIS-AITL | risk_stratified | 2 | 1 | 2.00x | 0 | 1 | 2 | 0 | 9 | 5 | 5 | 7 | 0.0% |
| DIS-ALCL | biomarker_driven | 2 | 2 | 1.00x | 1 | 2 | 1 | 0 | 6 | 5 | 5 | 5 | 0.0% |
| DIS-BCC | biomarker_driven | 2 | 2 | 1.00x | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0% |

## Variant Inflation Flags

| Disease | BMA | Families | Inflation | Interpretation |
|---|---:|---:|---:|---|
| DIS-CML | 5 | 1 | 5.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-OVARIAN | 39 | 8 | 4.88x | Raw BMA count likely overstates independent driver coverage. |
| DIS-BREAST | 37 | 8 | 4.62x | Raw BMA count likely overstates independent driver coverage. |
| DIS-MDS-HR | 11 | 3 | 3.67x | Raw BMA count likely overstates independent driver coverage. |
| DIS-PROSTATE | 20 | 6 | 3.33x | Raw BMA count likely overstates independent driver coverage. |
| DIS-CRC | 29 | 9 | 3.22x | Raw BMA count likely overstates independent driver coverage. |
| DIS-GIST | 9 | 3 | 3.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-MDS-LR | 6 | 2 | 3.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-UROTHELIAL | 16 | 6 | 2.67x | Raw BMA count likely overstates independent driver coverage. |
| DIS-AML | 26 | 10 | 2.60x | Raw BMA count likely overstates independent driver coverage. |
| DIS-NSCLC | 41 | 17 | 2.41x | Raw BMA count likely overstates independent driver coverage. |
| DIS-ENDOMETRIAL | 17 | 8 | 2.12x | Raw BMA count likely overstates independent driver coverage. |
| DIS-AITL | 2 | 1 | 2.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-MTC | 2 | 1 | 2.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-PDAC | 18 | 9 | 2.00x | Raw BMA count likely overstates independent driver coverage. |
| DIS-SALIVARY | 2 | 1 | 2.00x | Raw BMA count likely overstates independent driver coverage. |

## Notes

- `Families` collapses BMA rows by `biomarker_id`, so EGFR/ALK/ROS1 partner and resistance variants do not each count as independent disease-level coverage.
- `SOC families` counts ESCAT IA/IB families that are not classified as resistance rows.
- `Approved/guideline families` means the BMA carries regulatory approval text or NCCN/ESMO/ESGO primary sources; it is still not a substitute for clinical signoff.
- `Low/investigational BMA` is heuristic: ESCAT III/IV/X or text/evidence-lane signals such as trial, candidate, emerging, off-label, or not approved.
- `Resistance BMA` is heuristic: resistance-specific variant IDs/qualifiers or resistance-only evidence lanes, avoiding mixed CIViC bundles that also support sensitivity.
