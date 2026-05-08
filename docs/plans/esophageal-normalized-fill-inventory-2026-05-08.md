# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-ESOPHAGEAL

- Disease file: `knowledge_base/hosted/content/diseases/esophageal.yaml`
- Name: Esophageal carcinoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 1/6/4/4/6; BMA/families = 3/3; inflation = 1.0
- Backlog: tier `high_value_solid_thin`, score `0`, gaps SOC/IND/REG/Drug/RF = 0/0/0/0/0; flags `signoff_cold, low_tier_dominant, missing_regimen_records`
- Recommended next chunk: Create or backfill 2 linked regimen records referenced by existing indications.
- BMA review blockers: pending_signoff=3, review_required=3
- BMA metadata consistency: ready=2, missing_primary=0, missing_evidence=1, missing_contra=0, guideline_order_mismatch=0
- BMA family groups: BIO-HER2-SOLID x1, BIO-PIK3CA-MUTATION x1, BIO-TP53-MUTATION x1
- BMA review queue: low_tier_tail[low] x2
- Regimen wiring consistency: linked=6, missing_records=2, missing_sources=0, wired=4

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|
| BMA-HER2-AMP-ESOPHAGEAL | BIO-HER2-SOLID | IA | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_esophageal.yaml |
| BMA-PIK3CA-HOTSPOT-ESOPHAGEAL | BIO-PIK3CA-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_pik3ca_hotspot_esophageal.yaml |
| BMA-TP53-MUT-ESOPHAGEAL | BIO-TP53-MUTATION | IIIB | pending_clinical_signoff | True | 2026-04-27 | knowledge_base/hosted/content/biomarker_actionability/bma_tp53_mut_esophageal.yaml |

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|
| BIO-HER2-SOLID | 1 | IA | BMA-HER2-AMP-ESOPHAGEAL |
| BIO-PIK3CA-MUTATION | 1 | IIIB | BMA-PIK3CA-HOTSPOT-ESOPHAGEAL |
| BIO-TP53-MUTATION | 1 | IIIB | BMA-TP53-MUT-ESOPHAGEAL |

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|
| low_tier_tail | low | 2 | BIO-PIK3CA-MUTATION, BIO-TP53-MUTATION | Low-tier exploratory/prognostic rows; review after core SOC and intermediate families. |

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 2 | BMA-PIK3CA-HOTSPOT-ESOPHAGEAL, BMA-TP53-MUT-ESOPHAGEAL |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 1 | BMA-HER2-AMP-ESOPHAGEAL |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Regimen Wiring Consistency

| Check | Count | IDs |
|---|---:|---|
| Linked regimens from indications | 6 | REG-CARBOPLATIN-PACLITAXEL-WEEKLY, REG-NIVO-ADJUVANT-ESOPH, REG-NIVO-CHEMO-ESCC, REG-NIVO-MONO-ESOPH-2L, REG-PEMBRO-CISPLATIN-5FU-ESOPH, REG-PEMBRO-MONO-ESOPH-2L |
| Missing regimen records | 2 | REG-NIVO-CHEMO-ESCC, REG-PEMBRO-CISPLATIN-5FU-ESOPH |
| Existing linked regimens missing `sources` | 0 | - |
| Fully wired linked regimens | 4 | REG-CARBOPLATIN-PACLITAXEL-WEEKLY, REG-NIVO-ADJUVANT-ESOPH, REG-NIVO-MONO-ESOPH-2L, REG-PEMBRO-MONO-ESOPH-2L |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS | REG-NIVO-ADJUVANT-ESOPH | - | 1 | - | knowledge_base/hosted/content/indications/ind_esoph_adjuvant_nivolumab_post_cross.yaml |
| IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC | REG-NIVO-CHEMO-ESCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_esoph_metastatic_1l_nivo_chemo_scc.yaml |
| IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO | REG-PEMBRO-CISPLATIN-5FU-ESOPH | - | 1 | - | knowledge_base/hosted/content/indications/ind_esoph_metastatic_1l_pembro_chemo.yaml |
| IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS | REG-NIVO-MONO-ESOPH-2L | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_esoph_metastatic_2l_nivo_squamous.yaml |
| IND-ESOPH-METASTATIC-2L-PEMBRO-CPS10 | REG-PEMBRO-MONO-ESOPH-2L | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_esoph_metastatic_2l_pembro_cps10.yaml |
| IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT | REG-CARBOPLATIN-PACLITAXEL-WEEKLY | - | 1 | - | knowledge_base/hosted/content/indications/ind_esoph_resectable_cross_neoadjuvant.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-CARBOPLATIN-PACLITAXEL-WEEKLY | Weekly carboplatin + paclitaxel (CROSS-style chemo backbone) | SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024 | - | - | knowledge_base/hosted/content/regimens/carboplatin_paclitaxel_weekly.yaml |
| REG-NIVO-ADJUVANT-ESOPH | Nivolumab adjuvant — post-CROSS without pCR (CheckMate-577) | SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024 | - | - | knowledge_base/hosted/content/regimens/nivolumab_adjuvant_esophageal.yaml |
| REG-NIVO-MONO-ESOPH-2L | Nivolumab monotherapy — 2L esophageal squamous (ATTRACTION-3) | SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024 | - | - | knowledge_base/hosted/content/regimens/reg_nivo_mono_esoph_2l.yaml |
| REG-PEMBRO-MONO-ESOPH-2L | Pembrolizumab monotherapy — 2L esophageal PD-L1 CPS ≥10 (KEYNOTE-181) | SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_mono_esoph_2l.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-ESOPH-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_esoph_frailty_age.yaml |
| RF-ESOPH-HIGH-RISK-BIOLOGY | - | critical | - | knowledge_base/hosted/content/redflags/rf_esoph_high_risk_biology.yaml |
| RF-ESOPH-INFECTION-SCREENING | - | critical | - | knowledge_base/hosted/content/redflags/rf_esoph_infection_screening.yaml |
| RF-ESOPH-SEVERE-DYSPHAGIA-ASPIRATION | - | critical | - | knowledge_base/hosted/content/redflags/rf_esoph_severe_dysphagia_aspiration.yaml |
| RF-ESOPH-TRANSFORMATION-PROGRESSION | - | major | - | knowledge_base/hosted/content/redflags/rf_esoph_transformation_progression.yaml |
| RF-ESOPHAGEAL-POST-CROSS-NON-PCR | - | critical | - | knowledge_base/hosted/content/redflags/rf_esophageal_post_cross_non_pcr.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-CHECKMATE648-DOKI-2022 | rct_publication | 2022 | current | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_checkmate648_doki_2022.yaml |
| SRC-CIVIC | molecular_kb | nightly snapshot | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_civic.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-ESMO-ESOPHAGEAL-2024 | guideline | 2024 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_esmo_esophageal_2024.yaml |
| SRC-KEYNOTE590-SUN-2021 | rct_publication | 2021 | current | - | 2026-05-04 | knowledge_base/hosted/content/sources/src_keynote590_sun_2021.yaml |
| SRC-NCCN-ESOPHAGEAL-2025 | guideline | v.3.2025 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_esophageal_2025.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ESOPHAGEAL --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-ESOPHAGEAL --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ESOPHAGEAL --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
