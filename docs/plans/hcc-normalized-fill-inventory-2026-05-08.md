# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-HCC

- Disease file: `knowledge_base/hosted/content/diseases/hcc.yaml`
- Name: Hepatocellular carcinoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 0/6/6/5/6; BMA/families = 6/6; inflation = 1.0
- Backlog: tier `major_solid`, score `30`, gaps SOC/IND/REG/Drug/RF = 2/4/2/3/1; flags `signoff_cold, indication_signoff_cold, low_tier_dominant`
- Recommended next chunk: Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- BMA review blockers: pending_signoff=6, review_required=6
- BMA metadata consistency: ready=6, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0
- BMA family groups: BIO-BRAF-V600E x1, BIO-HNF1A x1, BIO-KRAS-G12C x1, BIO-MET x1, BIO-PIK3CA-MUTATION x1, BIO-TP53-MUTATION x1
- BMA review queue: low_tier_tail[low] x5
- Regimen wiring consistency: linked=6, missing_records=0, missing_sources=0, wired=6

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|
| BMA-BRAF-V600E-HCC | BIO-BRAF-V600E | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_hcc.yaml |
| BMA-HNF1A-HCC | BIO-HNF1A | IIB | pending_clinical_signoff | True | 2026-05-04 | knowledge_base/hosted/content/biomarker_actionability/bma_hnf1a_hcc.yaml |
| BMA-KRAS-G12C-HCC | BIO-KRAS-G12C | IV | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_hcc.yaml |
| BMA-MET-AMP-HCC | BIO-MET | IIIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_hcc.yaml |
| BMA-PIK3CA-HOTSPOT-HCC | BIO-PIK3CA-MUTATION | IV | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_pik3ca_hotspot_hcc.yaml |
| BMA-TP53-MUT-HCC | BIO-TP53-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_tp53_mut_hcc.yaml |

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|
| BIO-BRAF-V600E | 1 | IIIB | BMA-BRAF-V600E-HCC |
| BIO-HNF1A | 1 | IIB | BMA-HNF1A-HCC |
| BIO-KRAS-G12C | 1 | IV | BMA-KRAS-G12C-HCC |
| BIO-MET | 1 | IIIA | BMA-MET-AMP-HCC |
| BIO-PIK3CA-MUTATION | 1 | IV | BMA-PIK3CA-HOTSPOT-HCC |
| BIO-TP53-MUTATION | 1 | IIIB | BMA-TP53-MUT-HCC |

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|
| low_tier_tail | low | 5 | BIO-BRAF-V600E, BIO-KRAS-G12C, BIO-MET, BIO-PIK3CA-MUTATION, BIO-TP53-MUTATION | Low-tier exploratory/prognostic rows; review after core SOC and intermediate families. |

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 6 | BMA-BRAF-V600E-HCC, BMA-HNF1A-HCC, BMA-KRAS-G12C-HCC, BMA-MET-AMP-HCC, BMA-PIK3CA-HOTSPOT-HCC, BMA-TP53-MUT-HCC |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 0 | - |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Regimen Wiring Consistency

| Check | Count | IDs |
|---|---:|---|
| Linked regimens from indications | 6 | REG-ATEZO-BEV, REG-CABOZANTINIB-HCC, REG-DURVA-TREME-STRIDE, REG-RAMUCIRUMAB-HCC, REG-REGORAFENIB-HCC, REG-SORAFENIB-MONO |
| Missing regimen records | 0 | - |
| Existing linked regimens missing `sources` | 0 | - |
| Fully wired linked regimens | 6 | REG-ATEZO-BEV, REG-CABOZANTINIB-HCC, REG-DURVA-TREME-STRIDE, REG-RAMUCIRUMAB-HCC, REG-REGORAFENIB-HCC, REG-SORAFENIB-MONO |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-HCC-SYSTEMIC-1L-ATEZO-BEV | REG-ATEZO-BEV | - | 1 | - | knowledge_base/hosted/content/indications/ind_hcc_systemic_1l_atezo_bev.yaml |
| IND-HCC-SYSTEMIC-1L-DURVA-TREME | REG-DURVA-TREME-STRIDE | - | 1 | - | knowledge_base/hosted/content/indications/ind_hcc_systemic_1l_durva_treme.yaml |
| IND-HCC-SYSTEMIC-1L-SORAFENIB | REG-SORAFENIB-MONO | - | 1 | - | knowledge_base/hosted/content/indications/ind_hcc_systemic_1l_sorafenib.yaml |
| IND-HCC-SYSTEMIC-2L-CABOZANTINIB | REG-CABOZANTINIB-HCC | - | 1 | 0 | knowledge_base/hosted/content/indications/ind_hcc_systemic_2l_cabozantinib.yaml |
| IND-HCC-SYSTEMIC-2L-RAMUCIRUMAB | REG-RAMUCIRUMAB-HCC | - | 1 | 0 | knowledge_base/hosted/content/indications/ind_hcc_systemic_2l_ramucirumab.yaml |
| IND-HCC-SYSTEMIC-2L-REGORAFENIB | REG-REGORAFENIB-HCC | - | 1 | 0 | knowledge_base/hosted/content/indications/ind_hcc_systemic_2l_regorafenib.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-ATEZO-BEV | Atezolizumab + Bevacizumab | SRC-NCCN-HCC-2025, SRC-AASLD-HCC-2023 | - | - | knowledge_base/hosted/content/regimens/atezolizumab_bevacizumab.yaml |
| REG-CABOZANTINIB-HCC | - | SRC-CELESTIAL-ABOU-ALFA-2018, SRC-NCCN-HCC-2025 | - | - | knowledge_base/hosted/content/regimens/reg_cabozantinib_hcc.yaml |
| REG-DURVA-TREME-STRIDE | Durvalumab + Tremelimumab (STRIDE) | SRC-NCCN-HCC-2025 | - | - | knowledge_base/hosted/content/regimens/durvalumab_tremelimumab_stride.yaml |
| REG-RAMUCIRUMAB-HCC | - | SRC-REACH2-ZHU-2019, SRC-NCCN-HCC-2025 | - | - | knowledge_base/hosted/content/regimens/reg_ramucirumab_hcc.yaml |
| REG-REGORAFENIB-HCC | - | SRC-RESORCE-BRUIX-2017, SRC-NCCN-HCC-2025 | - | - | knowledge_base/hosted/content/regimens/reg_regorafenib_hcc.yaml |
| REG-SORAFENIB-MONO | Sorafenib monotherapy | SRC-NCCN-HCC-2025, SRC-AASLD-HCC-2023 | - | - | knowledge_base/hosted/content/regimens/sorafenib_mono.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-HCC-AFP-RAPID-RISE | - | major | - | knowledge_base/hosted/content/redflags/rf_hcc_afp_rapid_rise.yaml |
| RF-HCC-CHILD-PUGH-B-C | - | critical | - | knowledge_base/hosted/content/redflags/rf_hcc_child_pugh_b_c.yaml |
| RF-HCC-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_hcc_frailty_age.yaml |
| RF-HCC-HBV-REACTIVATION-RISK | - | critical | - | knowledge_base/hosted/content/redflags/rf_hcc_hbv_reactivation_risk.yaml |
| RF-HCC-HIGH-RISK-BIOLOGY | - | critical | - | knowledge_base/hosted/content/redflags/rf_hcc_high_risk_biology.yaml |
| RF-HCC-VARICEAL-BLEED | - | critical | - | knowledge_base/hosted/content/redflags/rf_hcc_variceal_bleed.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-AASLD-HCC-2023 | guideline | 2023 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_aasld_hcc_2023.yaml |
| SRC-CELESTIAL-ABOU-ALFA-2018 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_celestial_abou_alfa_2018.yaml |
| SRC-CIVIC | molecular_kb | nightly snapshot | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_civic.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-HIMALAYA-ABOU-ALFA-2022 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_himalaya_abou_alfa_2022.yaml |
| SRC-IMBRAVE150-FINN-2020 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_imbrave150_finn_2020.yaml |
| SRC-NCCN-HCC-2025 | guideline | v.3.2025 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_hcc_2025.yaml |
| SRC-REACH2-ZHU-2019 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_reach2_zhu_2019.yaml |
| SRC-RESORCE-BRUIX-2017 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_resorce_bruix_2017.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HCC --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-HCC --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HCC --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
