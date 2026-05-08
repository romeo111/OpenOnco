# Disease Fill Inventory

This is a low-token inventory for planning source-grounded disease fill work.
It does not author clinical claims or change YAML content.

## DIS-HNSCC

- Disease file: `knowledge_base/hosted/content/diseases/hnscc.yaml`
- Name: Head and neck squamous cell carcinoma
- Current normalized coverage: SOC/IND/REG/Drug/RF = 0/5/5/5/5; BMA/families = 0/0; inflation = -
- Backlog: tier `major_solid`, score `40`, gaps SOC/IND/REG/Drug/RF = 2/5/3/3/2; flags `none`
- Recommended next chunk: Add 2 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- BMA review blockers: pending_signoff=0, review_required=0
- BMA metadata consistency: ready=0, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0
- Regimen wiring consistency: linked=5, missing_records=0, missing_sources=0, wired=5

### BMA Files

| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |
|---|---|---|---|---|---|---|

### BMA Families

| Biomarker | Records | Highest ESCAT | Record IDs |
|---|---:|---|---|

### BMA Review Queue

| Queue | Priority | Records | Biomarkers | Reason |
|---|---|---:|---|---|

### BMA Metadata Consistency

| Check | Count | IDs |
|---|---:|---|
| Metadata-ready rows | 0 | - |
| Missing `primary_sources` | 0 | - |
| Missing `evidence_sources` | 0 | - |
| Missing `contraindicated_monotherapy` | 0 | - |
| Guideline evidence order mismatch | 0 | - |

### Regimen Wiring Consistency

| Check | Count | IDs |
|---|---:|---|
| Linked regimens from indications | 5 | REG-EXTREME-HNSCC, REG-NIVOLUMAB-MONO, REG-PEMBRO-CHEMO-HNSCC-1L, REG-PEMBRO-MONO-HNSCC-1L, REG-PEMBROLIZUMAB-MONO |
| Missing regimen records | 0 | - |
| Existing linked regimens missing `sources` | 0 | - |
| Fully wired linked regimens | 5 | REG-EXTREME-HNSCC, REG-NIVOLUMAB-MONO, REG-PEMBRO-CHEMO-HNSCC-1L, REG-PEMBRO-MONO-HNSCC-1L, REG-PEMBROLIZUMAB-MONO |

### Indications

| ID | Regimen | Line | NCCN | Signoffs | Path |
|---|---|---|---|---|---|
| IND-HNSCC-RM-1L-EXTREME | REG-EXTREME-HNSCC | - | 1 | - | knowledge_base/hosted/content/indications/ind_hnscc_rm_1l_extreme.yaml |
| IND-HNSCC-RM-1L-PEMBRO-CHEMO | REG-PEMBRO-CHEMO-HNSCC-1L | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_hnscc_rm_1l_pembro_chemo.yaml |
| IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH | REG-PEMBRO-MONO-HNSCC-1L | - | 1 | 2 | knowledge_base/hosted/content/indications/ind_hnscc_rm_1l_pembro_mono_cps_high.yaml |
| IND-HNSCC-RM-2L-NIVOLUMAB | REG-NIVOLUMAB-MONO | - | 1 | 0 | knowledge_base/hosted/content/indications/ind_hnscc_rm_2l_nivolumab.yaml |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | REG-PEMBROLIZUMAB-MONO | - | 1 | 0 | knowledge_base/hosted/content/indications/ind_hnscc_rm_2l_pembrolizumab.yaml |

### Linked Regimens

| ID | Name | Sources | Signoffs | Verified | Path |
|---|---|---|---|---|---|
| REG-EXTREME-HNSCC | EXTREME (cetuximab + cisplatin/carboplatin + 5-FU; HNSCC R/M, 1L) | SRC-EXTREME-VERMORKEN-2008, SRC-NCCN-HNSCC-2025, SRC-ESMO-HNSCC-2020 | - | - | knowledge_base/hosted/content/regimens/reg_extreme_hnscc.yaml |
| REG-NIVOLUMAB-MONO | - | SRC-CHECKMATE141-FERRIS-2016 | - | - | knowledge_base/hosted/content/regimens/reg_nivolumab_mono.yaml |
| REG-PEMBRO-CHEMO-HNSCC-1L | Pembrolizumab + 5-FU + platinum (HNSCC R/M, 1L; PD-L1 CPS ≥1) | SRC-NCCN-HNSCC-2025 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_chemo_hnscc_1l.yaml |
| REG-PEMBRO-MONO-HNSCC-1L | Pembrolizumab monotherapy (HNSCC R/M, 1L; PD-L1 CPS ≥20) | SRC-NCCN-HNSCC-2025 | - | - | knowledge_base/hosted/content/regimens/reg_pembro_mono_hnscc_1l.yaml |
| REG-PEMBROLIZUMAB-MONO | - | SRC-KEYNOTE040-COHEN-2019, SRC-KEYNOTE045-BELLMUNT-2017, SRC-KEYNOTE564-CHOUEIRI-2021, SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024 | - | - | knowledge_base/hosted/content/regimens/reg_pembrolizumab_mono.yaml |

### Redflags

| ID | Title | Severity | Verified | Path |
|---|---|---|---|---|
| RF-HNSCC-FRAILTY-AGE | - | major | - | knowledge_base/hosted/content/redflags/rf_hnscc_frailty_age.yaml |
| RF-HNSCC-HIGH-RISK-BIOLOGY | - | major | - | knowledge_base/hosted/content/redflags/rf_hnscc_high_risk_biology.yaml |
| RF-HNSCC-INFECTION-SCREENING | - | critical | - | knowledge_base/hosted/content/redflags/rf_hnscc_infection_screening.yaml |
| RF-HNSCC-ORGAN-DYSFUNCTION | - | major | - | knowledge_base/hosted/content/redflags/rf_hnscc_organ_dysfunction.yaml |
| RF-HNSCC-TRANSFORMATION-PROGRESSION | - | critical | - | knowledge_base/hosted/content/redflags/rf_hnscc_transformation_progression.yaml |

### Sources

| ID | Type | Version | Currency | Superseded By | Verified | Path |
|---|---|---|---|---|---|---|
| SRC-CHECKMATE141-FERRIS-2016 | - | - | - | - | - | knowledge_base/hosted/content/sources/src_checkmate141_ferris_2016.yaml |
| SRC-CTCAE-V5 | terminology | v5.0 (2017-11-27) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_ctcae_v5.yaml |
| SRC-ESMO-HNSCC-2020 | guideline | 2020 | current | - | 2026-04-28 | knowledge_base/hosted/content/sources/src_esmo_hnscc_2020.yaml |
| SRC-ESMO-RCC-2024 | guideline | 2024 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_esmo_rcc_2024.yaml |
| SRC-EXTREME-VERMORKEN-2008 | rct_publication | 2008 | current | - | 2026-05-01 | knowledge_base/hosted/content/sources/src_extreme_vermorken_2008.yaml |
| SRC-KEYNOTE040-COHEN-2019 | - | - | - | - | - | knowledge_base/hosted/content/sources/src_keynote040_cohen_2019.yaml |
| SRC-KEYNOTE045-BELLMUNT-2017 | - | - | - | - | - | knowledge_base/hosted/content/sources/src_keynote045_bellmunt_2017.yaml |
| SRC-KEYNOTE564-CHOUEIRI-2021 | rct_publication | 2021 | current | - | 2026-05-03 | knowledge_base/hosted/content/sources/src_keynote564_choueiri_2021.yaml |
| SRC-NCCN-HNSCC-2025 | guideline | 2025.v3 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_hnscc_2025.yaml |
| SRC-NCCN-KIDNEY-2025 | guideline | 2025.v3 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_kidney_2025.yaml |
| SRC-NCCN-NSCLC-2025 | guideline | 2025.v8 | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_nccn_nsclc_2025.yaml |
| SRC-ONCOKB | knowledge_base | continuous (last verified 2026-04-25) | current | - | 2026-04-27 | knowledge_base/hosted/content/sources/src_oncokb.yaml |

### Next Low-Token Commands

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HNSCC --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-HNSCC --compact-json
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
```

Suggested cheaper-model command:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HNSCC --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.
```
