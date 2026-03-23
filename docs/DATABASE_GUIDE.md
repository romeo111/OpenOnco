# Cancer AutoResearch — Database Guide

## Overview

The database stores structured cancer research reports for every cancer type,
organized by the WHO/NCI tumor classification taxonomy. All reports use a
single JSON schema (see `SCHEMA_REFERENCE.md`). The autoresearch loop generates,
scores, and iteratively improves reports — this guide explains how the database
is organized and how to work with it.

---

## Database Location

```
cancer_autoresearch/
├── research_db/               ← master database root
│   ├── INDEX.json             ← master index of all cancer types and status
│   ├── carcinomas/            ← epithelial origin (most common cancers)
│   ├── sarcomas/              ← connective tissue origin
│   ├── leukemias/             ← blood/bone marrow origin
│   ├── lymphomas/             ← lymphatic system origin
│   ├── myelomas/              ← plasma cell origin
│   └── cns_tumors/            ← brain and spinal cord
└── experiment_reports/        ← legacy location (head & neck, lung reports)
```

Each cancer subtype folder follows the same layout:

```
research_db/{category}/{subtype}/
├── benchmark_cases.json       ← fixed test set (generated once, never changed)
├── results.tsv                ← scoring history for this subtype's loop
├── mutation_history.json      ← strategy variant outcomes
└── reports/
    ├── {CASE_ID}_report.json  ← one report per benchmark case
    └── last_run_scores.json   ← scores from most recent experiment run
```

---

## Cancer Type Taxonomy

### Carcinomas — `research_db/carcinomas/`
Cancers originating in **epithelial cells** (skin, organ linings, glands).
The most common cancer type overall (~85% of all cancers).

| Subtype | Folder | Key Cancers |
|---|---|---|
| Head & Neck | `head_and_neck/` | HNSCC, NPC, thyroid, salivary gland |
| Lung | `lung/` | NSCLC (adenocarcinoma, squamous, LCLC), SCLC |
| Breast | `breast/` | HR+/HER2-, TNBC, HER2+, inflammatory, lobular |
| Colorectal | `colorectal/` | Colon, rectal, anal, appendiceal adenocarcinoma |
| Pancreatic | `pancreatic/` | PDAC (resectable/LA/metastatic), pNET |
| Gastric | `gastric/` | Gastric adenocarcinoma, GEJ, gastric MALT |
| Hepatocellular | `hepatocellular/` | HCC, intrahepatic cholangiocarcinoma |
| Thyroid | `thyroid/` | PTC, FTC, MTC, anaplastic |
| Cervical | `cervical/` | HPV+ squamous cell, adenocarcinoma |
| Ovarian | `ovarian/` | High-grade serous, clear cell, endometrioid, BRCA-related |
| Bladder | `bladder/` | Urothelial carcinoma (NMIBC, MIBC, metastatic) |
| Kidney/Renal | `kidney_renal/` | Clear cell RCC, papillary RCC, chromophobe |
| Prostate | `prostate/` | Localized, castration-sensitive, CRPC, neuroendocrine |
| Skin/Melanoma | `skin_melanoma/` | Cutaneous melanoma, Merkel cell, basal cell, SCC |

### Sarcomas — `research_db/sarcomas/`
Cancers originating in **connective tissue** — bones, cartilage, muscle, fat, blood vessels.
Rare (~1% of adult cancers, ~15% of pediatric cancers).

| Subtype | Folder | Key Cancers |
|---|---|---|
| Osteosarcoma | `osteosarcoma/` | High-grade central OS, parosteal, periosteal |
| Chondrosarcoma | `chondrosarcoma/` | Conventional, dedifferentiated, mesenchymal |
| Ewing Sarcoma | `ewing_sarcoma/` | EWSR1-FLI1+, localized, metastatic |
| Rhabdomyosarcoma | `rhabdomyosarcoma/` | Embryonal, alveolar (PAX-FOXO1), pleomorphic |
| Leiomyosarcoma | `leiomyosarcoma/` | Uterine, retroperitoneal, vascular origin |
| Liposarcoma | `liposarcoma/` | Well-differentiated, dedifferentiated, myxoid, pleomorphic |
| GIST | `gastrointestinal_stromal/` | KIT+, PDGFRA D842V, SDH-deficient, NF1-related |

### Leukemias — `research_db/leukemias/`
Blood cancers originating in **bone marrow**, disrupting normal white blood cell production.

| Subtype | Folder | Key Cancers |
|---|---|---|
| AML | `aml/` | AML with NPM1, FLT3-ITD, IDH1/2, t(8;21), APL |
| ALL | `all/` | B-ALL (Ph+, Ph-like), T-ALL, BCR-ABL1-positive |
| CML | `cml/` | Chronic phase, accelerated, blast crisis; BCR-ABL1+ |
| CLL | `cll/` | TP53/del17p, IGHV unmutated, del11q, BTK-inhibitor refractory |
| Hairy Cell | `hairy_cell/` | Classic HCL (BRAF V600E), variant HCL |

### Lymphomas — `research_db/lymphomas/`
Cancers of the **lymphatic system** — lymph nodes, spleen, bone marrow.

| Subtype | Folder | Key Cancers |
|---|---|---|
| Hodgkin | `hodgkin/` | Classical HL (NLPHL, mixed cellularity), PD-L1+ |
| DLBCL | `dlbcl/` | GCB vs ABC subtypes, double-hit, MYC/BCL2/BCL6 |
| Follicular | `follicular/` | Grade 1-3, POD24 risk, transformation |
| Mantle Cell | `mantle_cell/` | Classical, blastoid, leukemic, TP53 mutated |
| Peripheral T-cell | `peripheral_t_cell/` | PTCL-NOS, AITL, ALK+ ALCL, NKTCL |
| Marginal Zone | `marginal_zone/` | Splenic MZL, nodal MZL, MALT lymphoma |

### Myelomas — `research_db/myelomas/`
Cancers of **plasma cells** (antibody-producing B cells in bone marrow).

| Subtype | Folder | Key Cancers |
|---|---|---|
| Multiple Myeloma | `multiple_myeloma/` | NDMM transplant-eligible/ineligible, R/R MM, high-risk |
| Waldenström | `waldenstrom/` | WM/LPL, MYD88 L265P+, CXCR4 mutated |

### CNS Tumors — `research_db/cns_tumors/`
Primary cancers of the **brain and spinal cord**.
Classified by 2021 WHO CNS5 molecular taxonomy.

| Subtype | Folder | Key Cancers |
|---|---|---|
| Glioblastoma | `glioblastoma/` | IDH-wildtype GBM, MGMT-methylated vs unmethylated, EGFRvIII |
| Astrocytoma | `astrocytoma_idh_mutant/` | IDH-mutant grade 2/3/4, ATRX loss, CDKN2A del |
| Meningioma | `meningioma/` | Grade 1/2/3, NF2-mutated, TRAF7, AKT1 |
| Medulloblastoma | `medulloblastoma/` | WNT-activated, SHH-activated, group 3/4 |
| Ependymoma | `ependymoma/` | Spinal (H3 K27M), posterior fossa group A/B, supratentorial ZFTA |
| Spinal Cord | `spinal_cord/` | Spinal ependymoma, astrocytoma, drop metastases |

---

## Master Index (`research_db/INDEX.json`)

The index tracks status for every subtype. Fields:

```json
{
  "status": "pending | active | complete",
  "cases":  <number of benchmark cases>,
  "reports": <number of generated reports>,
  "benchmark_file": "<relative path to benchmark_cases.json or null>"
}
```

Update `INDEX.json` after adding benchmark cases or completing a research run.
Never let the index drift — it is the single source of truth for database state.

---

## Existing Data (Legacy Location)

Current reports live in `experiment_reports/` at the root. They belong in:
- `research_db/carcinomas/head_and_neck/reports/` — all HN, HN2, HN3 reports
- `research_db/carcinomas/lung/reports/` — all LUN reports
- `research_db/carcinomas/head_and_neck/` — benchmark_cases_hn*.json files

Migration is not required to run the loop — the legacy location still works.
Migrate when building query/aggregation tooling across cancer types.

---

## Querying the Database

```bash
# Count total reports
ls research_db/*/*/reports/*.json | wc -l

# List all active cancer types
python -c "
import json
idx = json.load(open('research_db/INDEX.json'))
for cat, data in idx['categories'].items():
    for sub, info in data['subtypes'].items():
        if info['status'] != 'pending':
            print(f'{cat}/{sub}: {info[\"reports\"]} reports')
"

# Score all reports for a cancer type
python run_experiment.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --reports-dir research_db/carcinomas/breast/reports
```
