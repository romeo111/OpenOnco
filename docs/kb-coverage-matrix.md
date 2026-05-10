# KB Coverage Matrix

_Generated_: 2026-05-10 06:02 UTC

Auto-generated from `knowledge_base/hosted/content/` by `scripts/kb_coverage_matrix.py`. **Do not edit by hand** — re-run the script. The strategy doc that explains how to read this is [`kb-coverage-strategy.md`](kb-coverage-strategy.md).

## Top-level KPIs

| Entity | Count |
|---|---:|
| Diseases | 78 |
| Biomarker_actionability (BMA) | 440 |
| Indications | 432 |
| Red flags | 475 |
| Drugs | 256 |
| Regimens | 368 |
| Sources | 388 |
| Biomarkers | 181 |
| Algorithms | 147 |
| Questionnaires | 78 |
| **Total entities** | **2765** |

## Quality scores

| Axis | Numerator | Denominator | Score |
|---|---:|---:|---:|
| BMA with ESCAT tier | 440 | 440 | 100% |
| BMA with CIViC evidence_sources | 345 | 440 | 78% |
| BMA UA-signed-off | 0 | 440 | 0% |
| BMA UA pending review | 439 | 440 | 100% |
| Indications with expected_outcomes | 430 | 432 | 100% |
| Indications with NCCN category | 432 | 432 | 100% |
| RF with sources | 473 | 475 | 100% |
| RF with last_reviewed | 443 | 475 | 93% |
| Sources with license declared | 347 | 388 | 89% |
| Sources current_as_of <365d | 189 | 388 | 49% |
| Drugs UA-registered | 155 | 256 | 61% |
| Drugs NSZU-reimbursed | 132 | 256 | 52% |

## ESCAT tier distribution (across 399 BMAs)

| Tier | Count | % |
|---|---:|---:|
| IA | 146 | 33% |
| IB | 49 | 11% |
| IIA | 60 | 14% |
| IIB | 26 | 6% |
| IIIA | 56 | 13% |
| IIIB | 68 | 15% |
| IV | 33 | 8% |
| V | 0 | 0% |
| X | 2 | 0% |
| (unset) | 0 | 0% |

## Per-disease coverage matrix

Sorted by (BMA + IND + RF) descending. Diseases with 0 across all axes are listed under "Coverage gaps" below.

| Disease | Archetype | Subtypes | BMA | ESCAT% | CIViC% | UA✓ | IND | Outcomes% | NCCN% | RF | RF cats | Regimens | Sources | Quest | #Curated |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|
| Non-small cell lung cancer (NSCLC) | biomarker_driven | 10 | 41 | 100% | 88% | 0% | 45 | 100% | 100% | 27 | 6 | 28 | 21 | ✓ | 14 |
| Breast cancer (invasive) (BREAST) | biomarker_driven | — | 37 | 100% | 86% | 0% | 28 | 100% | 100% | 21 | 6 | 19 | 21 | ✓ | 17 |
| Ovarian carcinoma (high-grade serous predominant) (OVARIAN) | biomarker_driven | — | 39 | 100% | 67% | 0% | 15 | 100% | 100% | 13 | 5 | 11 | 15 | ✓ | 2 |
| Colorectal carcinoma (CRC) (CRC) | stage_driven | — | 29 | 100% | 79% | 0% | 25 | 92% | 100% | 11 | 6 | 15 | 5 | ✓ | 6 |
| Acute Myeloid Leukemia (non-APL) (AML) | risk_stratified | — | 26 | 100% | 92% | 0% | 15 | 100% | 100% | 16 | 5 | 10 | 8 | ✓ | 7 |
| Prostate adenocarcinoma (PROSTATE) | line_of_therapy_sequential | — | 20 | 100% | 60% | 0% | 9 | 100% | 100% | 15 | 6 | 8 | 7 | ✓ | 2 |
| Diffuse Large B-Cell Lymphoma, NOS (DLBCL-NOS) | risk_stratified | — | 13 | 100% | 100% | 0% | 12 | 100% | 100% | 15 | 7 | 8 | 2 | ✓ | 7 |
| Multiple Myeloma (MM) | risk_stratified | — | 10 | 100% | 80% | 0% | 14 | 100% | 100% | 14 | 6 | 11 | 8 | ✓ | — |
| Gastric / GEJ adenocarcinoma (GASTRIC) | stage_driven | — | 18 | 100% | 50% | 0% | 9 | 100% | 100% | 10 | 6 | 8 | 9 | ✓ | 2 |
| Pancreatic ductal adenocarcinoma (PDAC) (PDAC) | stage_driven | — | 18 | 100% | 83% | 0% | 8 | 100% | 100% | 10 | 6 | 5 | 7 | ✓ | 1 |
| Cutaneous melanoma (MELANOMA) | biomarker_driven | 4 | 11 | 100% | 100% | 0% | 11 | 100% | 100% | 12 | 6 | 8 | 11 | ✓ | 5 |
| Endometrial carcinoma (ENDOMETRIAL) | biomarker_driven | 4 | 18 | 100% | 83% | 0% | 5 | 100% | 100% | 8 | 7 | 4 | 4 | ✓ | 2 |
| Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma (CLL) | risk_stratified | — | 10 | 100% | 90% | 0% | 8 | 100% | 100% | 12 | 7 | 6 | 3 | ✓ | 4 |
| Urothelial carcinoma (bladder + upper tract) (UROTHELIAL) | line_of_therapy_sequential | — | 16 | 100% | 69% | 0% | 6 | 100% | 100% | 6 | 6 | 6 | 3 | ✓ | 1 |
| Mantle Cell Lymphoma (MCL) | risk_stratified | — | 11 | 100% | 82% | 0% | 7 | 100% | 100% | 9 | 6 | 6 | 3 | ✓ | 3 |
| Myelodysplastic Syndromes — Higher-Risk (IPSS-R high / very high; includes MDS-EB) (MDS-HR) | risk_stratified | — | 11 | 100% | 100% | 0% | 3 | 100% | 100% | 9 | 6 | 3 | 3 | ✓ | — |
| Esophageal carcinoma (squamous + adeno) (ESOPHAGEAL) | stage_driven | — | 3 | 100% | 67% | 0% | 11 | 100% | 100% | 8 | 6 | 10 | 7 | ✓ | 1 |
| B-Lymphoblastic Leukemia / Lymphoma (B-ALL) | biomarker_driven | — | 7 | 100% | 86% | 0% | 6 | 100% | 100% | 8 | 5 | 5 | 6 | ✓ | — |
| Follicular Lymphoma (FL) | risk_stratified | — | 4 | 100% | 100% | 0% | 9 | 100% | 100% | 8 | 6 | 8 | 2 | ✓ | — |
| Renal cell carcinoma (RCC) | biomarker_driven | — | 4 | 100% | 75% | 0% | 9 | 100% | 100% | 8 | 7 | 7 | 3 | ✓ | 2 |
| Cholangiocarcinoma (bile duct cancer) (CHOLANGIOCARCINOMA) | stage_driven | — | 5 | 100% | 80% | 0% | 8 | 100% | 100% | 7 | 5 | 8 | 5 | ✓ | — |
| Chronic Myeloid Leukemia (BCR-ABL1) (CML) | etiologically_driven | — | 5 | 100% | 100% | 0% | 5 | 100% | 100% | 9 | 6 | 5 | 3 | ✓ | — |
| Glioblastoma (IDH-WT, WHO grade 4) (GBM) | stage_driven | — | 10 | 100% | 90% | 0% | 4 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ | — |
| Hepatocellular carcinoma (HCC) (HCC) | stage_driven | — | 6 | 100% | 83% | 0% | 6 | 100% | 100% | 7 | 6 | 6 | 3 | ✓ | 2 |
| Gastrointestinal stromal tumor (GIST) (GIST) | biomarker_driven | — | 9 | 100% | 89% | 0% | 4 | 100% | 100% | 5 | 5 | 4 | 4 | ✓ | — |
| Myelodysplastic Syndromes — Lower-Risk (IPSS-R very low / low / intermediate) (MDS-LR) | risk_stratified | — | 6 | 100% | 100% | 0% | 4 | 100% | 100% | 8 | 6 | 4 | 3 | ✓ | — |
| Small cell lung cancer (SCLC) | stage_driven | — | 2 | 100% | 50% | 0% | 7 | 100% | 100% | 7 | 5 | 7 | 2 | ✓ | 2 |
| Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma (AITL) | risk_stratified | — | 2 | 100% | 100% | 0% | 5 | 100% | 100% | 7 | 5 | 5 | 2 | ✓ | — |
| Classical Hodgkin Lymphoma (CHL) | stage_driven | — | 1 | 100% | 0% | 0% | 7 | 100% | 100% | 6 | 6 | 5 | 3 | ✓ | — |
| Primary Myelofibrosis (DIPSS-Plus stratified) (PMF) | risk_stratified | — | 2 | 100% | 100% | 0% | 5 | 100% | 100% | 7 | 6 | 4 | 4 | ✓ | — |
| Acute Promyelocytic Leukemia (PML-RARA) (APL) | molecularly_defined_emergency | — | 0 | — | — | — | 4 | 100% | 100% | 9 | 6 | 4 | 3 | ✓ | — |
| Polycythemia Vera (PV) | risk_stratified | — | 1 | 100% | 100% | 0% | 6 | 100% | 100% | 6 | 5 | 4 | 3 | ✓ | — |
| Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma (WM) | biomarker_driven | — | 2 | 100% | 50% | 0% | 5 | 100% | 100% | 6 | 5 | 5 | 2 | ✓ | — |
| Anaplastic Large Cell Lymphoma (systemic) (ALCL) | biomarker_driven | — | 2 | 100% | 50% | 0% | 5 | 100% | 100% | 5 | 5 | 5 | 2 | ✓ | — |
| Burkitt Lymphoma (BURKITT) | biomarker_driven | — | 1 | 100% | 100% | 0% | 5 | 100% | 100% | 6 | 5 | 5 | 2 | ✓ | — |
| Cervical carcinoma (squamous predominant + adeno) (CERVICAL) | etiologically_driven | — | 2 | 100% | 100% | 0% | 3 | 100% | 100% | 7 | 6 | 3 | 3 | ✓ | — |
| High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit) (HGBL-DH) | biomarker_driven | — | 2 | 100% | 50% | 0% | 3 | 100% | 100% | 7 | 5 | 3 | 2 | ✓ | — |
| T-Lymphoblastic Leukemia / Lymphoma (T-ALL) | risk_stratified | — | 2 | 100% | 100% | 0% | 2 | 100% | 100% | 8 | 5 | 2 | 4 | ✓ | — |
| Essential Thrombocythemia (ET) | risk_stratified | — | 2 | 100% | 100% | 0% | 3 | 100% | 100% | 6 | 5 | 2 | 3 | ✓ | — |
| Head and neck squamous cell carcinoma (HNSCC) (HNSCC) | etiologically_driven | — | 0 | — | — | — | 5 | 100% | 100% | 6 | 6 | 5 | 5 | ✓ | 2 |
| Mycosis Fungoides / Sézary Syndrome (MF-SEZARY) | stage_driven | — | 1 | 100% | 0% | 0% | 5 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ | — |
| Primary Mediastinal (Thymic) Large B-Cell Lymphoma (PMBCL) | risk_stratified | — | 0 | — | — | — | 3 | 100% | 100% | 8 | 6 | 3 | 3 | ✓ | — |
| Adult T-Cell Leukemia/Lymphoma (ATLL) | etiologically_driven | — | 1 | 100% | 0% | 0% | 3 | 100% | 100% | 6 | 5 | 3 | 3 | ✓ | — |
| Low-grade glioma (LGG, WHO grade 2 — IDH-mutant) (GLIOMA-LOW-GRADE) | biomarker_driven | — | 3 | 100% | 0% | 0% | 1 | 100% | 100% | 6 | 5 | 1 | 4 | ✓ | — |
| Hairy Cell Leukemia (HCL) | biomarker_driven | — | 2 | 100% | 50% | 0% | 3 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Nodal Marginal Zone Lymphoma (NODAL-MZL) | risk_stratified | — | 1 | 100% | 100% | 0% | 4 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ | — |
| Primary Diffuse Large B-Cell Lymphoma of the CNS (PCNSL) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 6 | 5 | 3 | 3 | ✓ | — |
| HCV-associated Marginal Zone Lymphoma (HCV-MZL) | etiologically_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 4 | ✓ | — |
| Medullary thyroid carcinoma (MTC) (MTC) | biomarker_driven | — | 2 | 100% | 100% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL) (NLPBL) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Peripheral T-Cell Lymphoma, Not Otherwise Specified (PTCL-NOS) | risk_stratified | — | 0 | — | — | — | 4 | 100% | 100% | 5 | 5 | 4 | 2 | ✓ | — |
| Post-Transplant Lymphoproliferative Disorder (PTLD) | stage_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ | — |
| Salivary gland carcinoma (SALIVARY) | biomarker_driven | — | 2 | 100% | 0% | 0% | 1 | 100% | 100% | 6 | 5 | 1 | 3 | ✓ | — |
| Splenic Marginal Zone Lymphoma (SPLENIC-MZL) | etiologically_driven | — | 1 | 100% | 100% | 0% | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ | — |
| Anaplastic thyroid carcinoma (ATC) (THYROID-ANAPLASTIC) | biomarker_driven | — | 1 | 100% | 100% | 0% | 2 | 100% | 100% | 6 | 5 | 2 | 3 | ✓ | — |
| Papillary thyroid carcinoma (PTC) (THYROID-PAPILLARY) | stage_driven | — | 3 | 100% | 33% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ | — |
| Advanced systemic mastocytosis (AdvSM) (MASTOCYTOSIS) | biomarker_driven | — | 1 | 100% | 100% | 0% | 2 | 100% | 100% | 5 | 5 | 2 | 4 | ✓ | — |
| Extranodal NK/T-Cell Lymphoma, Nasal Type (NK-T-NASAL) | etiologically_driven | — | 0 | — | — | — | 3 | 100% | 100% | 5 | 5 | 3 | 2 | ✓ | — |
| Enteropathy-Associated T-Cell Lymphoma (EATL) | etiologically_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Hepatosplenic T-Cell Lymphoma (HSTCL) | biomarker_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Infantile fibrosarcoma (IFS) (IFS) | biomarker_driven | — | 1 | 100% | 100% | 0% | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ | — |
| Malignant peripheral nerve sheath tumor (MPNST) (MPNST) | biomarker_driven | — | 0 | — | — | — | 1 | 100% | 100% | 6 | 5 | 1 | 3 | ✓ | — |
| T-Cell Prolymphocytic Leukemia (T-PLL) | biomarker_driven | — | 0 | — | — | — | 2 | 100% | 100% | 5 | 5 | 2 | 2 | ✓ | — |
| Chondrosarcoma (CHONDROSARCOMA) | stage_driven | — | 0 | — | — | — | 1 | 100% | 100% | 5 | 5 | 1 | 4 | ✓ | — |
| Inflammatory myofibroblastic tumor (IMT) (IMT) | biomarker_driven | — | 0 | — | — | — | 1 | 100% | 100% | 5 | 5 | 1 | 2 | ✓ | — |
| Basal cell carcinoma (BCC) (BCC) | biomarker_driven | — | 2 | 100% | 0% | 0% | 2 | 100% | 100% | 0 | 0 | 2 | 0 | ✓ | — |
| Malignant pleural mesothelioma (MPM) (MESOTHELIOMA) | stage_driven | — | 0 | — | — | — | 3 | 100% | 100% | 1 | 1 | 3 | 1 | ✓ | — |
| Soft tissue sarcoma (STS) (SOFT-TISSUE-SARCOMA) | histology_driven | — | 0 | — | — | — | 4 | 100% | 100% | 0 | 0 | 4 | 0 | ✓ | — |
| Testicular germ cell tumor (GCT) (TESTICULAR-GCT) | stage_driven | — | 0 | — | — | — | 4 | 100% | 100% | 0 | 0 | 3 | 0 | ✓ | — |
| Squamous cell carcinoma of the anal canal (ANAL-SCC) | stage_driven | — | 0 | — | — | — | 3 | 100% | 100% | 0 | 0 | 3 | 0 | ✓ | — |
| Gastroenteropancreatic neuroendocrine tumor — GI origin (carcinoid), well-differentiated G1/G2 (GI-NET) | grade_and_stage_driven | — | 0 | — | — | — | 1 | 100% | 100% | 2 | 2 | 1 | 1 | ✓ | — |
| Lymphangioleiomyomatosis (LAM) (LAM) | biomarker_driven | — | 2 | 100% | 0% | 0% | 1 | 100% | 100% | 0 | 0 | 1 | 0 | ✓ | — |
| Pancreatic neuroendocrine tumor (pNET), well-differentiated G1/G2 (PNET) | grade_and_stage_driven | — | 0 | — | — | — | 1 | 100% | 100% | 2 | 2 | 1 | 1 | ✓ | — |
| Epithelioid sarcoma (EPITHELIOID-SARCOMA) | biomarker_driven | — | 1 | 100% | 0% | 0% | 1 | 100% | 100% | 0 | 0 | 1 | 0 | ✓ | — |
| Adult granulosa cell tumor of the ovary (GRANULOSA-CELL) | biomarker_driven | — | 1 | 100% | 0% | 0% | 1 | 100% | 100% | 0 | 0 | 1 | 0 | ✓ | — |
| Tenosynovial giant cell tumor (TGCT) (TGCT) | biomarker_driven | — | 1 | 100% | 0% | 0% | 1 | 100% | 100% | 0 | 0 | 1 | 0 | ✓ | — |
| Juvenile myelomonocytic leukemia (JMML) (JMML) | biomarker_driven | — | 1 | 100% | 0% | 0% | 0 | — | — | 0 | 0 | 0 | 0 | ✓ | — |
| Meningioma (MENINGIOMA) | biomarker_driven | — | 1 | 100% | 0% | 0% | 0 | — | — | 0 | 0 | 0 | 0 | ✓ | — |

## Coverage gaps

### Diseases with **zero BMA** (17)

| Disease | Archetype | IND | RF |
|---|---|---:|---:|
| Squamous cell carcinoma of the anal canal (DIS-ANAL-SCC) | stage_driven | 3 | 0 |
| Acute Promyelocytic Leukemia (PML-RARA) (DIS-APL) | molecularly_defined_emergency | 4 | 9 |
| Chondrosarcoma (DIS-CHONDROSARCOMA) | stage_driven | 1 | 5 |
| Enteropathy-Associated T-Cell Lymphoma (DIS-EATL) | etiologically_driven | 2 | 5 |
| Gastroenteropancreatic neuroendocrine tumor — GI origin (carcinoid), well-differentiated G1/G2 (DIS-GI-NET) | grade_and_stage_driven | 1 | 2 |
| Head and neck squamous cell carcinoma (HNSCC) (DIS-HNSCC) | etiologically_driven | 5 | 6 |
| Hepatosplenic T-Cell Lymphoma (DIS-HSTCL) | biomarker_driven | 2 | 5 |
| Inflammatory myofibroblastic tumor (IMT) (DIS-IMT) | biomarker_driven | 1 | 5 |
| Malignant pleural mesothelioma (MPM) (DIS-MESOTHELIOMA) | stage_driven | 3 | 1 |
| Malignant peripheral nerve sheath tumor (MPNST) (DIS-MPNST) | biomarker_driven | 1 | 6 |
| Extranodal NK/T-Cell Lymphoma, Nasal Type (DIS-NK-T-NASAL) | etiologically_driven | 3 | 5 |
| Primary Mediastinal (Thymic) Large B-Cell Lymphoma (DIS-PMBCL) | risk_stratified | 3 | 8 |
| Pancreatic neuroendocrine tumor (pNET), well-differentiated G1/G2 (DIS-PNET) | grade_and_stage_driven | 1 | 2 |
| Peripheral T-Cell Lymphoma, Not Otherwise Specified (DIS-PTCL-NOS) | risk_stratified | 4 | 5 |
| Soft tissue sarcoma (STS) (DIS-SOFT-TISSUE-SARCOMA) | histology_driven | 4 | 0 |
| T-Cell Prolymphocytic Leukemia (DIS-T-PLL) | biomarker_driven | 2 | 5 |
| Testicular germ cell tumor (GCT) (DIS-TESTICULAR-GCT) | stage_driven | 4 | 0 |

### Diseases with **thin BMA coverage (1-2 entries)** (33)

| Disease | BMA |
|---|---:|
| Adult T-Cell Leukemia/Lymphoma (DIS-ATLL) | 1 |
| Burkitt Lymphoma (DIS-BURKITT) | 1 |
| Epithelioid sarcoma (DIS-EPITHELIOID-SARCOMA) | 1 |
| Adult granulosa cell tumor of the ovary (DIS-GRANULOSA-CELL) | 1 |
| HCV-associated Marginal Zone Lymphoma (DIS-HCV-MZL) | 1 |
| Classical Hodgkin Lymphoma (DIS-CHL) | 1 |
| Infantile fibrosarcoma (IFS) (DIS-IFS) | 1 |
| Juvenile myelomonocytic leukemia (JMML) (DIS-JMML) | 1 |
| Advanced systemic mastocytosis (AdvSM) (DIS-MASTOCYTOSIS) | 1 |
| Meningioma (DIS-MENINGIOMA) | 1 |
| Mycosis Fungoides / Sézary Syndrome (DIS-MF-SEZARY) | 1 |
| Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL) (DIS-NLPBL) | 1 |
| Nodal Marginal Zone Lymphoma (DIS-NODAL-MZL) | 1 |
| Primary Diffuse Large B-Cell Lymphoma of the CNS (DIS-PCNSL) | 1 |
| Post-Transplant Lymphoproliferative Disorder (DIS-PTLD) | 1 |
| Polycythemia Vera (DIS-PV) | 1 |
| Splenic Marginal Zone Lymphoma (DIS-SPLENIC-MZL) | 1 |
| Tenosynovial giant cell tumor (TGCT) (DIS-TGCT) | 1 |
| Anaplastic thyroid carcinoma (ATC) (DIS-THYROID-ANAPLASTIC) | 1 |
| Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma (DIS-AITL) | 2 |
| Anaplastic Large Cell Lymphoma (systemic) (DIS-ALCL) | 2 |
| Basal cell carcinoma (BCC) (DIS-BCC) | 2 |
| Cervical carcinoma (squamous predominant + adeno) (DIS-CERVICAL) | 2 |
| Essential Thrombocythemia (DIS-ET) | 2 |
| Hairy Cell Leukemia (DIS-HCL) | 2 |
| High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit) (DIS-HGBL-DH) | 2 |
| Lymphangioleiomyomatosis (LAM) (DIS-LAM) | 2 |
| Medullary thyroid carcinoma (MTC) (DIS-MTC) | 2 |
| Primary Myelofibrosis (DIPSS-Plus stratified) (DIS-PMF) | 2 |
| Salivary gland carcinoma (DIS-SALIVARY) | 2 |
| Small cell lung cancer (DIS-SCLC) | 2 |
| T-Lymphoblastic Leukemia / Lymphoma (DIS-T-ALL) | 2 |
| Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma (DIS-WM) | 2 |

### Diseases with **zero red-flags** (10)

- Squamous cell carcinoma of the anal canal (DIS-ANAL-SCC)
- Basal cell carcinoma (BCC) (DIS-BCC)
- Epithelioid sarcoma (DIS-EPITHELIOID-SARCOMA)
- Adult granulosa cell tumor of the ovary (DIS-GRANULOSA-CELL)
- Juvenile myelomonocytic leukemia (JMML) (DIS-JMML)
- Lymphangioleiomyomatosis (LAM) (DIS-LAM)
- Meningioma (DIS-MENINGIOMA)
- Soft tissue sarcoma (STS) (DIS-SOFT-TISSUE-SARCOMA)
- Testicular germ cell tumor (GCT) (DIS-TESTICULAR-GCT)
- Tenosynovial giant cell tumor (TGCT) (DIS-TGCT)

### Diseases with **zero indications** (2)

- Juvenile myelomonocytic leukemia (JMML) (DIS-JMML)
- Meningioma (DIS-MENINGIOMA)

### Diseases with **no questionnaire** (0)


## Quality gaps

- **0** BMAs without ESCAT tier
- **95** BMAs without CIViC evidence_sources
- **2** indications without `expected_outcomes` block
- **2** redflags without `sources` block

---

## How to act on this matrix

Each new TaskTorrent chunk should reference a specific cell or gap and state how it advances coverage. Example chunk-spec preamble: _"This chunk advances `Per-disease matrix > breast_cancer > IND-Outcomes%` from 60% to 95% by adding expected_outcomes to 12 missing indications."_

Re-run this script after each KB-mutating PR is applied. Schedule weekly via cron once the strategy doc lands.