# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-GBM

- Disease file: `knowledge_base/hosted/content/diseases/gbm.yaml`
- Name: Glioblastoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 1/4/1/1/5; BMA/families = 10/6; inflation = 1.67
- Backlog: tier `major_solid`, score `46`, gaps SOC/IND/REG/Drug/RF = 1/6/7/7/2; flags `signoff_cold, indication_signoff_cold, low_tier_dominant, missing_regimen_records`
- Recommended next chunk: Add 1 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- BMA review blockers: pending_signoff=10, review_required=10
- BMA metadata consistency: ready=10, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0
- BMA family groups: BIO-BRAF-V600E x1, BIO-EGFR-MUTATION x1, BIO-IDH-MUTATION x5, BIO-MGMT-METHYLATION x1, BIO-TERT x1, BIO-TP53-MUTATION x1
- BMA review queue: low_tier_tail[low] x3
- Regimen wiring consistency: linked=4, missing_records=3, missing_sources=0, wired=1

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|
| BMA-BRAF-V600E-GBM | BIO-BRAF-V600E | IIIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_gbm.yaml |
| BMA-EGFR-MUTATION-GBM | BIO-EGFR-MUTATION | X | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_egfr_mutation_gbm.yaml |
| BMA-IDH1-R132C-GBM | BIO-IDH-MUTATION | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132c_gbm.yaml |
| BMA-IDH1-R132G-GBM | BIO-IDH-MUTATION | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132g_gbm.yaml |
| BMA-IDH1-R132H-GBM | BIO-IDH-MUTATION | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_gbm.yaml |
| BMA-IDH1-R132L-GBM | BIO-IDH-MUTATION | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132l_gbm.yaml |
| BMA-IDH1-R132S-GBM | BIO-IDH-MUTATION | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132s_gbm.yaml |
| BMA-MGMT-METHYLATION-GBM | BIO-MGMT-METHYLATION | IA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_mgmt_methylation_gbm.yaml |
| BMA-TERT-GLIOMA | BIO-TERT | IIB | pending_clinical_signoff | True | 2026-05-04 | knowledge_base/hosted/content/biomarker_actionability/bma_tert_glioma.yaml |
| BMA-TP53-MUT-GBM | BIO-TP53-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_tp53_mut_gbm.yaml |

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|
| BIO-BRAF-V600E | 1 | IIIA | BMA-BRAF-V600E-GBM |
| BIO-EGFR-MUTATION | 1 | X | BMA-EGFR-MUTATION-GBM |
| BIO-IDH-MUTATION | 5 | IIA | BMA-IDH1-R132C-GBM, BMA-IDH1-R132G-GBM, BMA-IDH1-R132H-GBM, BMA-IDH1-R132L-GBM, BMA-IDH1-R132S-GBM |
| BIO-MGMT-METHYLATION | 1 | IA | BMA-MGMT-METHYLATION-GBM |
| BIO-TERT | 1 | IIB | BMA-TERT-GLIOMA |
| BIO-TP53-MUTATION | 1 | IIIB | BMA-TP53-MUT-GBM |

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|
| low_tier_tail | low | 3 | BIO-BRAF-V600E, BIO-EGFR-MUTATION, BIO-TP53-MUTATION | Low-tier exploratory/prognostic rows; review after core SOC and intermediate families. |

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 10 | BMA-BRAF-V600E-GBM, BMA-EGFR-MUTATION-GBM, BMA-IDH1-R132C-GBM, BMA-IDH1-R132G-GBM, BMA-IDH1-R132H-GBM, BMA-IDH1-R132L-GBM, BMA-IDH1-R132S-GBM, BMA-MGMT-METHYLATION-GBM, BMA-TERT-GLIOMA, BMA-TP53-MUT-GBM |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 0 | - |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Regimen Wiring Consistency

| Check | Count | IDs |
|---|---:|---|
| Linked regimens from indications | 4 | REG-BEVACIZUMAB-GBM, REG-HYPOFRACTIONATED-RT-GBM, REG-STUPP-TMZ, REG-TMZ-MONO |
| Missing regimen records | 3 | REG-BEVACIZUMAB-GBM, REG-HYPOFRACTIONATED-RT-GBM, REG-TMZ-MONO |
| Existing linked regimens missing `sources` | 0 | - |
| Fully wired linked regimens | 1 | REG-STUPP-TMZ |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-GBM-NEWLY-DIAGNOSED-ELDERLY-HYPORT | REG-HYPOFRACTIONATED-RT-GBM | - | 1 | - | knowledge_base/hosted/content/indications/ind_gbm_newly_diagnosed_elderly_hyport.yaml |
| IND-GBM-NEWLY-DIAGNOSED-ELDERLY-TMZ | REG-TMZ-MONO | - | 1 | - | knowledge_base/hosted/content/indications/ind_gbm_newly_diagnosed_elderly_tmz.yaml |
| IND-GBM-NEWLY-DIAGNOSED-STUPP | REG-STUPP-TMZ | - | 1 | - | knowledge_base/hosted/content/indications/ind_gbm_newly_diagnosed_stupp.yaml |
| IND-GBM-RECURRENT-BEVACIZUMAB | REG-BEVACIZUMAB-GBM | - | 2A | - | knowledge_base/hosted/content/indications/ind_gbm_recurrent_bevacizumab.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-STUPP-TMZ | Stupp protocol — Temozolomide concurrent + adjuvant | SRC-NCCN-CNS-2025, SRC-EANO-GBM-2024 | - | - | knowledge_base/hosted/content/regimens/stupp_temozolomide.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-GBM-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_gbm_frailty_age.yaml |
| RF-GBM-HIGH-RISK-BIOLOGY | - | major | - | knowledge_base/hosted/content/redflags/rf_gbm_high_risk_biology.yaml |
| RF-GBM-INFECTION-SCREENING | - | major | - | knowledge_base/hosted/content/redflags/rf_gbm_infection_screening.yaml |
| RF-GBM-INTRACRANIAL-PRESSURE-EMERGENCY | - | critical | - | knowledge_base/hosted/content/redflags/rf_gbm_intracranial_pressure_emergency.yaml |
| RF-GBM-TRANSFORMATION-PROGRESSION | - | critical | - | knowledge_base/hosted/content/redflags/rf_gbm_transformation_progression.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-CCTG-CE6-PERRY-2017 | rct_publication | 2017 | current | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_cctg_ce6_perry_2017.yaml |
| SRC-CIVIC | molecular_kb | nightly snapshot | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_civic.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-EANO-GBM-2024 | guideline | 2024 update | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_eano_gbm_2024.yaml |
| SRC-NCCN-CNS-2025 | guideline | v.3.2025 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_cns_2025.yaml |
| SRC-NORDIC-GBM-MALMSTROM-2012 | rct_publication | 2012 | current | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_nordic_gbm_malmstrom_2012.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-GBM --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-GBM --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-GBM --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
