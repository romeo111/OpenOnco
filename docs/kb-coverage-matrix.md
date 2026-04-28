# KB Coverage Matrix

_Generated_: 2026-04-28 20:56 UTC

Auto-generated from `knowledge_base/hosted/content/` by `scripts/kb_coverage_matrix.py`. **Do not edit by hand** — re-run the script. The strategy doc that explains how to read this is [`kb-coverage-strategy.md`](kb-coverage-strategy.md).

## Top-level KPIs

| Entity | Count |
|---|---:|
| Diseases | 65 |
| Biomarker_actionability (BMA) | 399 |
| Indications | 302 |
| Red flags | 426 |
| Drugs | 216 |
| Regimens | 244 |
| Sources | 269 |
| Biomarkers | 111 |
| Algorithms | 110 |
| Questionnaires | 65 |
| **Total entities** | **2142** |

## Quality scores

| Axis | Numerator | Denominator | Score |
|---|---:|---:|---:|
| BMA with ESCAT tier | 399 | 399 | 100% |
| BMA with CIViC evidence_sources | 295 | 399 | 74% |
| BMA UA-signed-off | 0 | 399 | 0% |
| BMA UA pending review | 398 | 399 | 100% |
| Indications with expected_outcomes | 302 | 302 | 100% |
| Indications with NCCN category | 302 | 302 | 100% |
| RF with sources | 426 | 426 | 100% |
| RF with last_reviewed | 394 | 426 | 92% |
| Sources with license declared | 240 | 269 | 89% |
| Sources current_as_of <365d | 27 | 269 | 10% |
| Drugs UA-registered | 151 | 216 | 70% |
| Drugs NSZU-reimbursed | 132 | 216 | 61% |

## ESCAT tier distribution (across 399 BMAs)

| Tier | Count | % |
|---|---:|---:|
| IA | 135 | 34% |
| IB | 47 | 12% |
| IIA | 52 | 13% |
| IIB | 18 | 5% |
| IIIA | 53 | 13% |
| IIIB | 61 | 15% |
| IV | 31 | 8% |
| V | 0 | 0% |
| X | 2 | 1% |
| (unset) | 0 | 0% |

## Per-disease coverage matrix

Sorted by (BMA + IND + RF) descending. Diseases with 0 across all axes are listed under "Coverage gaps" below.

| Disease | Archetype | Subtypes | BMA | ESCAT% | CIViC% | UA✓ | IND | Outcomes% | NCCN% | RF | RF cats | Regimens | Sources | Quest |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| Non-small cell lung cancer (NSCLC) | biomarker_driven | 10 | 36 | 100% | 94% | 0% | 28 | 100% | 100% | 22 | 5 | 20 | 20 | ✓ |
| Breast cancer (invasive) (BREAST) | biomarker_driven | — | 36 | 100% | 86% | 0% | 20 | 100% | 100% | 11 | 5 | 13 | 11 | ✓ |
| Ovarian carcinoma (high-grade serous predominant) (OVARIAN) | biomarker_driven | — | 39 | 100% | 67% | 0% | 15 | 100% | 100% | 11 | 5 | 11 | 10 | ✓ |
| Colorectal carcinoma (CRC) (CRC) | stage_driven | — | 27 | 100% | 59% | 0% | 18 | 100% | 100% | 8 | 5 | 12 | 2 | ✓ |
| Acute Myeloid Leukemia (non-APL) (AML) | risk_stratified | — | 24 | 100% | 96% | 0% | 11 | 100% | 100% | 12 | 5 | 6 | 6 | ✓ |
| Prostate adenocarcinoma (PROSTATE) | line_of_therapy_sequential | — | 20 | 100% | 45% | 0% | 5 | 100% | 100% | 9 | 6 | 5 | 3 | ✓ |
| Diffuse Large B-Cell Lymphoma, NOS (DLBCL-NOS) | risk_stratified | — | 13 | 100% | 85% | 0% | 9 | 100% | 100% | 11 | 6 | 4 | 2 | ✓ |
| Multiple Myeloma (MM) | risk_stratified | — | 10 | 100% | 80% | 0% | 7 | 100% | 100% | 12 | 6 | 5 | 3 | ✓ |
| Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma (CLL) | risk_stratified | — | 10 | 100% | 70% | 0% | 6 | 100% | 100% | 12 | 7 | 5 | 3 | ✓ |
| Cutaneous melanoma (MELANOMA) | biomarker_driven | 4 | 11 | 100% | 100% | 0% | 9 | 100% | 100% | 8 | 5 | 6 | 6 | ✓ |
| Gastric / GEJ adenocarcinoma (GASTRIC) | stage_driven | — | 15 | 100% | 40% | 0% | 5 | 100% | 100% | 6 | 5 | 5 | 2 | ✓ |
| Mantle Cell Lymphoma (MCL) | risk_stratified | — | 11 | 100% | 55% | 0% | 6 | 100% | 100% | 8 | 5 | 6 | 3 | ✓ |
| Endometrial carcinoma (ENDOMETRIAL) | biomarker_driven | 4 | 15 | 100% | 40% | 0% | 4 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ |
| Pancreatic ductal adenocarcinoma (PDAC) (PDAC) | stage_driven | — | 16 | 100% | 94% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| Myelodysplastic Syndromes — Higher-Risk (IPSS-R high / very high; includes MDS-EB) (MDS-HR) | risk_stratified | — | 11 | 100% | 100% | 0% | 3 | 100% | 100% | 9 | 6 | 3 | 3 | ✓ |
| Urothelial carcinoma (bladder + upper tract) (UROTHELIAL) | line_of_therapy_sequential | — | 15 | 100% | 47% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| B-Lymphoblastic Leukemia / Lymphoma (B-ALL) | biomarker_driven | — | 6 | 100% | 100% | 0% | 6 | 100% | 100% | 7 | 5 | 5 | 4 | ✓ |
| Chronic Myeloid Leukemia (BCR-ABL1) (CML) | etiologically_driven | — | 5 | 100% | 100% | 0% | 5 | 100% | 100% | 9 | 6 | 5 | 3 | ✓ |
| Follicular Lymphoma (FL) | risk_stratified | — | 4 | 100% | 25% | 0% | 7 | 100% | 100% | 8 | 6 | 6 | 2 | ✓ |
| Myelodysplastic Syndromes — Lower-Risk (IPSS-R very low / low / intermediate) (MDS-LR) | risk_stratified | — | 6 | 100% | 100% | 0% | 4 | 100% | 100% | 8 | 6 | 4 | 3 | ✓ |
| Gastrointestinal stromal tumor (GIST) (GIST) | biomarker_driven | — | 9 | 100% | 33% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 4 | ✓ |
| Glioblastoma (IDH-WT, WHO grade 4) (GBM) | stage_driven | — | 9 | 100% | 89% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ |
| Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma (AITL) | risk_stratified | — | 2 | 100% | 100% | 0% | 5 | 100% | 100% | 7 | 5 | 5 | 2 | ✓ |
| Hepatocellular carcinoma (HCC) (HCC) | stage_driven | — | 5 | 100% | 100% | 0% | 3 | 100% | 100% | 6 | 5 | 3 | 2 | ✓ |
| Primary Myelofibrosis (DIPSS-Plus stratified) (PMF) | risk_stratified | — | 2 | 100% | 50% | 0% | 5 | 100% | 100% | 7 | 6 | 4 | 4 | ✓ |
| Acute Promyelocytic Leukemia (PML-RARA) (APL) | molecularly_defined_emergency | — | 0 | — | — | — | 4 | 100% | 100% | 9 | 6 | 4 | 3 | ✓ |
| Classical Hodgkin Lymphoma (CHL) | stage_driven | — | 1 | 100% | 0% | 0% | 7 | 100% | 100% | 5 | 5 | 5 | 2 | ✓ |
| Polycythemia Vera (PV) | risk_stratified | — | 1 | 100% | 100% | 0% | 6 | 100% | 100% | 6 | 5 | 4 | 3 | ✓ |
| Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma (WM) | biomarker_driven | — | 2 | 100% | 50% | 0% | 5 | 100% | 100% | 6 | 5 | 5 | 2 | ✓ |
| Anaplastic Large Cell Lymphoma (systemic) (ALCL) | biomarker_driven | — | 2 | 100% | 50% | 0% | 5 | 100% | 100% | 5 | 5 | 5 | 2 | ✓ |
| Burkitt Lymphoma (BURKITT) | biomarker_driven | — | 1 | 100% | 100% | 0% | 5 | 100% | 100% | 6 | 5 | 5 | 2 | ✓ |
| Esophageal carcinoma (squamous + adeno) (ESOPHAGEAL) | stage_driven | — | 3 | 100% | 67% | 0% | 4 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ |
| High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit) (HGBL-DH) | biomarker_driven | — | 2 | 100% | 50% | 0% | 3 | 100% | 100% | 7 | 5 | 3 | 2 | ✓ |
| Renal cell carcinoma (RCC) | biomarker_driven | — | 3 | 100% | 67% | 0% | 4 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| T-Lymphoblastic Leukemia / Lymphoma (T-ALL) | risk_stratified | — | 2 | 100% | 100% | 0% | 2 | 100% | 100% | 8 | 5 | 2 | 4 | ✓ |
| Essential Thrombocythemia (ET) | risk_stratified | — | 2 | 100% | 50% | 0% | 3 | 100% | 100% | 6 | 5 | 2 | 3 | ✓ |
| Cervical carcinoma (squamous predominant + adeno) (CERVICAL) | etiologically_driven | — | 2 | 100% | 100% | 0% | 2 | 100% | 100% | 6 | 5 | 1 | 2 | ✓ |
| Cholangiocarcinoma (bile duct cancer) (CHOLANGIOCARCINOMA) | stage_driven | — | 4 | 100% | 100% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 4 | ✓ |
| Mycosis Fungoides / Sézary Syndrome (MF-SEZARY) | stage_driven | — | 0 | — | — | — | 5 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ |
| Nodal Marginal Zone Lymphoma (NODAL-MZL) | risk_stratified | — | 1 | 100% | 100% | 0% | 4 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| Primary Diffuse Large B-Cell Lymphoma of the CNS (PCNSL) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 6 | 5 | 3 | 3 | ✓ |
| Primary Mediastinal (Thymic) Large B-Cell Lymphoma (PMBCL) | risk_stratified | — | 0 | — | — | — | 3 | 100% | 100% | 7 | 5 | 3 | 2 | ✓ |
| Small cell lung cancer (SCLC) | stage_driven | — | 1 | 100% | 100% | 0% | 2 | 100% | 100% | 7 | 5 | 2 | 2 | ✓ |
| Adult T-Cell Leukemia/Lymphoma (ATLL) | etiologically_driven | — | 0 | — | — | — | 3 | 100% | 100% | 6 | 5 | 3 | 3 | ✓ |
| Hairy Cell Leukemia (HCL) | biomarker_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| HCV-associated Marginal Zone Lymphoma (HCV-MZL) | etiologically_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 4 | ✓ |
| Medullary thyroid carcinoma (MTC) (MTC) | biomarker_driven | — | 2 | 100% | 100% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL) (NLPBL) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| Peripheral T-Cell Lymphoma, Not Otherwise Specified (PTCL-NOS) | risk_stratified | — | 0 | — | — | — | 4 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ |
| Post-Transplant Lymphoproliferative Disorder (PTLD) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| Salivary gland carcinoma (SALIVARY) | biomarker_driven | — | 2 | 100% | 0% | 0% | 1 | 100% | 100% | 6 | 5 | 1 | 4 | ✓ |
| Splenic Marginal Zone Lymphoma (SPLENIC-MZL) | etiologically_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| Advanced systemic mastocytosis (AdvSM) (MASTOCYTOSIS) | biomarker_driven | — | 1 | 100% | 100% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 4 | ✓ |
| Extranodal NK/T-Cell Lymphoma, Nasal Type (NK-T-NASAL) | etiologically_driven | — | 0 | — | — | — | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ |
| Anaplastic thyroid carcinoma (ATC) (THYROID-ANAPLASTIC) | biomarker_driven | — | 1 | 100% | 100% | 0% | 1 | 100% | 100% | 6 | 5 | 1 | 2 | ✓ |
| Papillary thyroid carcinoma (PTC) (THYROID-PAPILLARY) | stage_driven | — | 2 | 100% | 50% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ |
| Enteropathy-Associated T-Cell Lymphoma (EATL) | etiologically_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| Low-grade glioma (LGG, WHO grade 2 — IDH-mutant) (GLIOMA-LOW-GRADE) | biomarker_driven | — | 0 | — | — | — | 1 | 100% | 100% | 6 | 5 | 0 | 4 | ✓ |
| Head and neck squamous cell carcinoma (HNSCC) (HNSCC) | etiologically_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 4 | ✓ |
| Hepatosplenic T-Cell Lymphoma (HSTCL) | biomarker_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| Infantile fibrosarcoma (IFS) (IFS) | biomarker_driven | — | 1 | 100% | 0% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ |
| Malignant peripheral nerve sheath tumor (MPNST) (MPNST) | biomarker_driven | — | 0 | — | — | — | 1 | 100% | 100% | 6 | 5 | 1 | 2 | ✓ |
| T-Cell Prolymphocytic Leukemia (T-PLL) | biomarker_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ |
| Chondrosarcoma (CHONDROSARCOMA) | stage_driven | — | 0 | — | — | — | 1 | 100% | 100% | 5 | 5 | 1 | 4 | ✓ |
| Inflammatory myofibroblastic tumor (IMT) (IMT) | biomarker_driven | — | 0 | — | — | — | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ |

## Coverage gaps

### Diseases with **zero BMA** (14)

| Disease | Archetype | IND | RF |
|---|---|---:|---:|
| Acute Promyelocytic Leukemia (PML-RARA) (DIS-APL) | molecularly_defined_emergency | 4 | 9 |
| Adult T-Cell Leukemia/Lymphoma (DIS-ATLL) | etiologically_driven | 3 | 6 |
| Chondrosarcoma (DIS-CHONDROSARCOMA) | stage_driven | 1 | 5 |
| Enteropathy-Associated T-Cell Lymphoma (DIS-EATL) | etiologically_driven | 2 | 5 |
| Low-grade glioma (LGG, WHO grade 2 — IDH-mutant) (DIS-GLIOMA-LOW-GRADE) | biomarker_driven | 1 | 6 |
| Head and neck squamous cell carcinoma (HNSCC) (DIS-HNSCC) | etiologically_driven | 2 | 5 |
| Hepatosplenic T-Cell Lymphoma (DIS-HSTCL) | biomarker_driven | 2 | 5 |
| Inflammatory myofibroblastic tumor (IMT) (DIS-IMT) | biomarker_driven | 1 | 5 |
| Mycosis Fungoides / Sézary Syndrome (DIS-MF-SEZARY) | stage_driven | 5 | 5 |
| Malignant peripheral nerve sheath tumor (MPNST) (DIS-MPNST) | biomarker_driven | 1 | 6 |
| Extranodal NK/T-Cell Lymphoma, Nasal Type (DIS-NK-T-NASAL) | etiologically_driven | 3 | 5 |
| Primary Mediastinal (Thymic) Large B-Cell Lymphoma (DIS-PMBCL) | risk_stratified | 3 | 7 |
| Peripheral T-Cell Lymphoma, Not Otherwise Specified (DIS-PTCL-NOS) | risk_stratified | 4 | 5 |
| T-Cell Prolymphocytic Leukemia (DIS-T-PLL) | biomarker_driven | 2 | 5 |

### Diseases with **thin BMA coverage (1-2 entries)** (25)

| Disease | BMA |
|---|---:|
| Burkitt Lymphoma (DIS-BURKITT) | 1 |
| Hairy Cell Leukemia (DIS-HCL) | 1 |
| HCV-associated Marginal Zone Lymphoma (DIS-HCV-MZL) | 1 |
| Classical Hodgkin Lymphoma (DIS-CHL) | 1 |
| Infantile fibrosarcoma (IFS) (DIS-IFS) | 1 |
| Advanced systemic mastocytosis (AdvSM) (DIS-MASTOCYTOSIS) | 1 |
| Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL) (DIS-NLPBL) | 1 |
| Nodal Marginal Zone Lymphoma (DIS-NODAL-MZL) | 1 |
| Primary Diffuse Large B-Cell Lymphoma of the CNS (DIS-PCNSL) | 1 |
| Post-Transplant Lymphoproliferative Disorder (DIS-PTLD) | 1 |
| Polycythemia Vera (DIS-PV) | 1 |
| Small cell lung cancer (DIS-SCLC) | 1 |
| Splenic Marginal Zone Lymphoma (DIS-SPLENIC-MZL) | 1 |
| Anaplastic thyroid carcinoma (ATC) (DIS-THYROID-ANAPLASTIC) | 1 |
| Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma (DIS-AITL) | 2 |
| Anaplastic Large Cell Lymphoma (systemic) (DIS-ALCL) | 2 |
| Cervical carcinoma (squamous predominant + adeno) (DIS-CERVICAL) | 2 |
| Essential Thrombocythemia (DIS-ET) | 2 |
| High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit) (DIS-HGBL-DH) | 2 |
| Medullary thyroid carcinoma (MTC) (DIS-MTC) | 2 |
| Primary Myelofibrosis (DIPSS-Plus stratified) (DIS-PMF) | 2 |
| Salivary gland carcinoma (DIS-SALIVARY) | 2 |
| T-Lymphoblastic Leukemia / Lymphoma (DIS-T-ALL) | 2 |
| Papillary thyroid carcinoma (PTC) (DIS-THYROID-PAPILLARY) | 2 |
| Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma (DIS-WM) | 2 |

### Diseases with **zero red-flags** (0)


### Diseases with **zero indications** (0)


### Diseases with **no questionnaire** (0)


## Quality gaps

- **0** BMAs without ESCAT tier
- **104** BMAs without CIViC evidence_sources
- **0** indications without `expected_outcomes` block
- **0** redflags without `sources` block

---

## How to act on this matrix

Each new TaskTorrent chunk should reference a specific cell or gap and state how it advances coverage. Example chunk-spec preamble: _"This chunk advances `Per-disease matrix > breast_cancer > IND-Outcomes%` from 60% to 95% by adding expected_outcomes to 12 missing indications."_

Re-run this script after each KB-mutating PR is applied. Schedule weekly via cron once the strategy doc lands.