# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-RCC

- Disease file: `knowledge_base/hosted/content/diseases/rcc.yaml`
- Name: Renal cell carcinoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 1/8/7/7/6; BMA/families = 5/5; inflation = 1.0
- Backlog: tier `major_solid`, score `35`, gaps SOC/IND/REG/Drug/RF = 5/2/1/1/1; flags `signoff_cold, indication_signoff_cold, low_tier_dominant`
- Recommended next chunk: Add 5 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- BMA review blockers: pending_signoff=5, review_required=5
- BMA metadata consistency: ready=5, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0
- BMA family groups: BIO-BAP1 x1, BIO-MET x1, BIO-PIK3CA-MUTATION x1, BIO-TP53-MUTATION x1, BIO-TSC1 x1
- BMA review queue: low_tier_tail[low] x2
- Regimen wiring consistency: linked=7, missing_records=0, missing_sources=0, wired=7

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|
| BMA-BAP1-MUT-RCC-PROGNOSTIC | BIO-BAP1 | III | pending_clinical_signoff | True | - | knowledge_base/hosted/content/biomarker_actionability/bma_bap1_mut_rcc_prognostic.yaml |
| BMA-MET-AMP-RCC-PAPILLARY | BIO-MET | IIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_rcc_papillary.yaml |
| BMA-PIK3CA-HOTSPOT-RCC | BIO-PIK3CA-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_pik3ca_hotspot_rcc.yaml |
| BMA-TP53-MUT-RCC | BIO-TP53-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_tp53_mut_rcc.yaml |
| BMA-TSC1-TSC-RENAL-AML | BIO-TSC1 | IB | pending_clinical_signoff | True | 2026-05-04 | knowledge_base/hosted/content/biomarker_actionability/bma_tsc1_tsc_renal_aml.yaml |

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|
| BIO-BAP1 | 1 | III | BMA-BAP1-MUT-RCC-PROGNOSTIC |
| BIO-MET | 1 | IIA | BMA-MET-AMP-RCC-PAPILLARY |
| BIO-PIK3CA-MUTATION | 1 | IIIB | BMA-PIK3CA-HOTSPOT-RCC |
| BIO-TP53-MUTATION | 1 | IIIB | BMA-TP53-MUT-RCC |
| BIO-TSC1 | 1 | IB | BMA-TSC1-TSC-RENAL-AML |

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|
| low_tier_tail | low | 2 | BIO-PIK3CA-MUTATION, BIO-TP53-MUTATION | Low-tier exploratory/prognostic rows; review after core SOC and intermediate families. |

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 5 | BMA-BAP1-MUT-RCC-PROGNOSTIC, BMA-MET-AMP-RCC-PAPILLARY, BMA-PIK3CA-HOTSPOT-RCC, BMA-TP53-MUT-RCC, BMA-TSC1-TSC-RENAL-AML |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 0 | - |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Regimen Wiring Consistency

| Check | Count | IDs |
|---|---:|---|
| Linked regimens from indications | 7 | REG-BELZUTIFAN-MONO, REG-CABOZANTINIB-RCC, REG-LENV-PEMBRO-RCC, REG-NIVO-CABO-RCC, REG-NIVO-IPI-RCC, REG-PEMBRO-AXI-RCC, REG-PEMBROLIZUMAB-MONO |
| Missing regimen records | 0 | - |
| Existing linked regimens missing `sources` | 0 | - |
| Fully wired linked regimens | 7 | REG-BELZUTIFAN-MONO, REG-CABOZANTINIB-RCC, REG-LENV-PEMBRO-RCC, REG-NIVO-CABO-RCC, REG-NIVO-IPI-RCC, REG-PEMBRO-AXI-RCC, REG-PEMBROLIZUMAB-MONO |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-RCC-ADJUVANT-PEMBRO | REG-PEMBROLIZUMAB-MONO | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_adjuvant_pembro.yaml |
| IND-RCC-METASTATIC-1L-LENV-PEMBRO | REG-LENV-PEMBRO-RCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_1l_lenv_pembro.yaml |
| IND-RCC-METASTATIC-1L-NIVO-CABO | REG-NIVO-CABO-RCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_1l_nivo_cabo.yaml |
| IND-RCC-METASTATIC-1L-NIVO-IPI | REG-NIVO-IPI-RCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_1l_nivo_ipi.yaml |
| IND-RCC-METASTATIC-1L-PEMBRO-AXI | REG-PEMBRO-AXI-RCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_1l_pembro_axi.yaml |
| IND-RCC-METASTATIC-2L-BELZUTIFAN | REG-BELZUTIFAN-MONO | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_2l_belzutifan.yaml |
| IND-RCC-METASTATIC-2L-CABOZANTINIB | REG-CABOZANTINIB-RCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_metastatic_2l_cabozantinib.yaml |
| IND-RCC-VHL-DISEASE-BELZUTIFAN | REG-BELZUTIFAN-MONO | - | 1 | - | knowledge_base/hosted/content/indications/ind_rcc_vhl_disease_belzutifan.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-BELZUTIFAN-MONO | Belzutifan monotherapy (VHL-disease tumors / mRCC 2L+) | SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_belzutifan_mono.yaml |
| REG-CABOZANTINIB-RCC | Cabozantinib monotherapy (RCC, 2L) | SRC-METEOR-CHOUEIRI-2016, SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_cabozantinib_rcc.yaml |
| REG-LENV-PEMBRO-RCC | Lenvatinib + pembrolizumab (RCC, 1L) | SRC-CLEAR-MOTZER-2021, SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_lenv_pembro_rcc.yaml |
| REG-NIVO-CABO-RCC | Nivolumab + cabozantinib (RCC, 1L) | SRC-CHECKMATE9ER-CHOUEIRI-2021, SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_nivo_cabo_rcc.yaml |
| REG-NIVO-IPI-RCC | Nivolumab + ipilimumab (RCC, 1L IMDC intermediate/poor) | SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_nivo_ipi_rcc.yaml |
| REG-PEMBRO-AXI-RCC | Pembrolizumab + axitinib (RCC, 1L all-risk) | SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_axi_rcc.yaml |
| REG-PEMBROLIZUMAB-MONO | - | SRC-KEYNOTE040-COHEN-2019, SRC-KEYNOTE045-BELLMUNT-2017, SRC-KEYNOTE564-CHOUEIRI-2021, SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_pembrolizumab_mono.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-RCC-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_rcc_frailty_age.yaml |
| RF-RCC-HIGH-RISK-BIOLOGY | - | major | - | knowledge_base/hosted/content/redflags/rf_rcc_high_risk_biology.yaml |
| RF-RCC-IMDC-INTERMEDIATE-POOR-RISK | - | major | - | knowledge_base/hosted/content/redflags/rf_rcc_imdc_intermediate_poor_risk.yaml |
| RF-RCC-INFECTION-SCREENING | - | major | - | knowledge_base/hosted/content/redflags/rf_rcc_infection_screening.yaml |
| RF-RCC-ORGAN-DYSFUNCTION | - | major | - | knowledge_base/hosted/content/redflags/rf_rcc_organ_dysfunction.yaml |
| RF-RCC-TRANSFORMATION-PROGRESSION | - | critical | - | knowledge_base/hosted/content/redflags/rf_rcc_transformation_progression.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-CHECKMATE9ER-CHOUEIRI-2021 | rct_publication | 2021 | current | - | 2026-05-03 | knowledge_base/hosted/content/sources/src_checkmate9er_choueiri_2021.yaml |
| SRC-CIVIC | molecular_kb | nightly snapshot | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_civic.yaml |
| SRC-CLEAR-MOTZER-2021 | rct_publication | 2021 | current | - | 2026-05-03 | knowledge_base/hosted/content/sources/src_clear_motzer_2021.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-ESMO-RCC-2024 | guideline | 2024 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_esmo_rcc_2024.yaml |
| SRC-KEYNOTE040-COHEN-2019 | - | - | - | - | - | knowledge_base/hosted/content/sources/src_keynote040_cohen_2019.yaml |
| SRC-KEYNOTE045-BELLMUNT-2017 | - | - | - | - | - | knowledge_base/hosted/content/sources/src_keynote045_bellmunt_2017.yaml |
| SRC-KEYNOTE564-CHOUEIRI-2021 | rct_publication | 2021 | current | - | 2026-05-03 | knowledge_base/hosted/content/sources/src_keynote564_choueiri_2021.yaml |
| SRC-METEOR-CHOUEIRI-2016 | rct_publication | 2016 | current | - | 2026-05-03 | knowledge_base/hosted/content/sources/src_meteor_choueiri_2016.yaml |
| SRC-NCCN-KIDNEY-2025 | guideline | 2025.v3 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_kidney_2025.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-RCC --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-RCC --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-RCC --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
