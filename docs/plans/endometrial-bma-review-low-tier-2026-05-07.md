# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-ENDOMETRIAL

- Disease file: `knowledge_base/hosted/content/diseases/endometrial.yaml`
- Name: Endometrial carcinoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 1/5/4/5/7; BMA/families = 17/8; inflation = 2.12
- Backlog: tier `major_solid`, score `51`, gaps SOC/IND/REG/Drug/RF = 5/5/4/3/0; flags `signoff_cold, low_tier_dominant`
- Recommended next chunk: Add 5 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- BMA review blockers: pending_signoff=5, review_required=5
- BMA metadata consistency: ready=5, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0
- BMA family groups: BIO-KRAS-G12C x1, BIO-PIK3CA-MUTATION x1, BIO-RAS-MUTATION x2, BIO-TP53-MUTATION x1
- BMA review queue: low_tier_tail[low] x5

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|
| BMA-KRAS-G12C-ENDOMETRIAL | BIO-KRAS-G12C | IIIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_endometrial.yaml |
| BMA-KRAS-G12D-ENDOMETRIAL | BIO-RAS-MUTATION | IV | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_endometrial.yaml |
| BMA-KRAS-G12V-ENDOMETRIAL | BIO-RAS-MUTATION | IV | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12v_endometrial.yaml |
| BMA-PIK3CA-HOTSPOT-ENDOMETRIAL | BIO-PIK3CA-MUTATION | IIIA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_pik3ca_hotspot_endometrial.yaml |
| BMA-TP53-MUT-ENDOMETRIAL | BIO-TP53-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_tp53_mut_endometrial.yaml |

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|
| BIO-KRAS-G12C | 1 | IIIA | BMA-KRAS-G12C-ENDOMETRIAL |
| BIO-PIK3CA-MUTATION | 1 | IIIA | BMA-PIK3CA-HOTSPOT-ENDOMETRIAL |
| BIO-RAS-MUTATION | 2 | IV | BMA-KRAS-G12D-ENDOMETRIAL, BMA-KRAS-G12V-ENDOMETRIAL |
| BIO-TP53-MUTATION | 1 | IIIB | BMA-TP53-MUT-ENDOMETRIAL |

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|
| low_tier_tail | low | 5 | BIO-KRAS-G12C, BIO-PIK3CA-MUTATION, BIO-RAS-MUTATION, BIO-TP53-MUTATION | Low-tier exploratory/prognostic rows; review after core SOC and intermediate families. |

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 5 | BMA-KRAS-G12C-ENDOMETRIAL, BMA-KRAS-G12D-ENDOMETRIAL, BMA-KRAS-G12V-ENDOMETRIAL, BMA-PIK3CA-HOTSPOT-ENDOMETRIAL, BMA-TP53-MUT-ENDOMETRIAL |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 0 | - |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR | REG-DOSTARLIMAB-MONO-ENDOM | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_endometrial_2l_dostarlimab_dmmr.yaml |
| IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR | REG-PEMBRO-LENVATINIB-ENDOM | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_endometrial_2l_pembro_lenva_pmmr.yaml |
| IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO | REG-DOSTARLIMAB-CARBO-PACLI-ENDOM | - | 1 | - | knowledge_base/hosted/content/indications/ind_endometrial_advanced_1l_dostarlimab_chemo.yaml |
| IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO | REG-PEMBRO-CARBO-PACLI-ENDOM | - | 1 | - | knowledge_base/hosted/content/indications/ind_endometrial_advanced_1l_pembro_chemo.yaml |
| IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION | - | - | 1 | - | knowledge_base/hosted/content/indications/ind_endometrial_stage_i_pole_observation.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-DOSTARLIMAB-CARBO-PACLI-ENDOM | Dostarlimab + carbo + paclitaxel (endometrial advanced 1L dMMR) | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | - | - | knowledge_base/hosted/content/regimens/reg_dostarlimab_carbo_pacli_endom.yaml |
| REG-DOSTARLIMAB-MONO-ENDOM | Dostarlimab monotherapy (GARNET) — 2L+ dMMR endometrial | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | - | - | knowledge_base/hosted/content/regimens/reg_dostarlimab_mono_endom.yaml |
| REG-PEMBRO-CARBO-PACLI-ENDOM | Pembrolizumab + carbo + paclitaxel (endometrial advanced 1L) | SRC-NCCN-UTERINE-2025 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_carbo_pacli_endom.yaml |
| REG-PEMBRO-LENVATINIB-ENDOM | Pembrolizumab + Lenvatinib (KEYNOTE-775) — 2L pMMR endometrial | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_lenvatinib_endom.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-ENDOMETRIAL-FIT-FOR-LENVATINIB-COMBO | - | minor | - | knowledge_base/hosted/content/redflags/rf_endometrial_fit_for_lenvatinib_combo.yaml |
| RF-ENDOMETRIAL-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_endometrial_frailty_age.yaml |
| RF-ENDOMETRIAL-HIGH-RISK-BIOLOGY | - | major | - | knowledge_base/hosted/content/redflags/rf_endometrial_high_risk_biology.yaml |
| RF-ENDOMETRIAL-INFECTION-SCREENING | - | major | - | knowledge_base/hosted/content/redflags/rf_endometrial_infection_screening.yaml |
| RF-ENDOMETRIAL-ORGAN-DYSFUNCTION | - | major | - | knowledge_base/hosted/content/redflags/rf_endometrial_organ_dysfunction.yaml |
| RF-ENDOMETRIAL-TRANSFORMATION-PROGRESSION | - | critical | - | knowledge_base/hosted/content/redflags/rf_endometrial_transformation_progression.yaml |
| RF-POLE-POLD1-ENDOMETRIAL-LOW-RISK | - | major | - | knowledge_base/hosted/content/redflags/rf_pole_pold1_endometrial_low_risk.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-CIVIC | molecular_kb | nightly snapshot | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_civic.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-ESGO-ENDOMETRIAL-2025 | guideline | 2025 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_esgo_endometrial_2025.yaml |
| SRC-GY018-MAKKER-2022 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_gy018_makker_2022.yaml |
| SRC-NCCN-UTERINE-2025 | guideline | 2025.v2 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_uterine_2025.yaml |
| SRC-RUBY-MIRZA-2023 | - | - | - | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_ruby_mirza_2023.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-ENDOMETRIAL --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --inventory-queue low_tier_tail --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
