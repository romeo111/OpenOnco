# `expected_outcomes` traceability audit (2026-05-01)

Phase 1 deliverable for [`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`](../plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md). Read-only baseline of how well each indication's `expected_outcomes` block traces back to its `Indication.sources`. Re-run via `py -3.12 scripts/audit_expected_outcomes.py`.

## Methodology

For every YAML at `knowledge_base/hosted/content/indications/*.yaml`, every populated field of `expected_outcomes` (schema fields plus any extra `extra='allow'` siblings) is bucketed:

- **`cited`** — value contains a `SRC-*` id from `Indication.sources`, or a recognized trial abbreviation (e.g. `KEYNOTE-006`, `CheckMate-577`) whose number resolves by substring to one of the indication's source ids or titles.
- **`probably-cited`** — value contains a trial-family keyword or trial number that did not resolve to `Indication.sources`. A SRC id from outside the indication's source list also lands here.
- **`uncited`** — value present and non-empty but no citation pointer. This is the Phase-3 remediation backlog.
- **`absent`** — field is null or missing.

Sibling keys inside `expected_outcomes` that are conceptually metadata (`notes`, `note`, `comment`, `comments`, `rationale`, `follow_up`, `caveats`) are **not** counted as outcome fields, but their text **is** appended to the citation-lookup haystack of every sibling outcome value in the same block. This handles the common pattern `{median_overall_survival_months: 46, notes: "KEYNOTE-426"}` where the trial name lives in `notes` and the numeric value cannot self-cite.

Trial-name regexes are an explicit allowlist hard-coded in `scripts/audit_expected_outcomes.py`. They cover the common modern oncology trials (KEYNOTE, CheckMate, DESTINY-Breast, IMpower / IMbrave, etc.) but are deliberately incomplete — uncovered trials will land as `uncited` rather than `probably-cited`. False negatives here under-state the citation rate; tighten the allowlist as new trial families enter the KB.

## Headline numbers

- **Indications audited:** 390
- **Outcome-field slots (populated + absent):** 2124
- **Populated outcome-field slots:** 1351

| Bucket | Count | % of populated | % of all slots |
|---|---:|---:|---:|
| `cited` | 163 | 12.1% | 7.7% |
| `probably-cited` | 76 | 5.6% | 3.6% |
| `uncited` | 1112 | 82.3% | 52.4% |
| `absent` | 773 | n/a | 36.4% |

**Combined `cited + probably-cited`:** 239 / 1351 = 17.7% of populated outcome values carry a citation pointer (loose definition). Strict-cited only: 163 / 1351 = 12.1%.

Plan v1.0 target is ≥90% citation-traceable on the strict definition. Today's `cited`-only rate is the gap to close.

## Top 10 worst-offender diseases (by absolute `uncited` count)

Sorted by raw `uncited` count: the diseases with the largest Phase-3 remediation backlog measured in cells, not percentage.

| # | Disease | Indications | populated | uncited | probably-cited | cited | outcomes-cited % (loose) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `DIS-NSCLC` — Non-small cell lung cancer | 40 | 120 | 83 | 4 | 33 | 30.8% |
| 2 | `DIS-CRC` — Colorectal carcinoma (CRC) | 22 | 85 | 72 | 6 | 7 | 15.3% |
| 3 | `DIS-AML` — Acute Myeloid Leukemia (non-APL) | 15 | 60 | 55 | 1 | 4 | 8.3% |
| 4 | `DIS-OVARIAN` — Ovarian carcinoma (high-grade serous predominant) | 15 | 48 | 42 | 2 | 4 | 12.5% |
| 5 | `DIS-DLBCL-NOS` — Diffuse Large B-Cell Lymphoma, NOS | 12 | 48 | 42 | 4 | 2 | 12.5% |
| 6 | `DIS-MM` — Multiple Myeloma | 13 | 52 | 37 | 12 | 3 | 28.8% |
| 7 | `DIS-MELANOMA` — Cutaneous melanoma | 11 | 37 | 28 | 0 | 9 | 24.3% |
| 8 | `DIS-FL` — Follicular Lymphoma | 7 | 27 | 25 | 2 | 0 | 7.4% |
| 9 | `DIS-PROSTATE` — Prostate adenocarcinoma | 8 | 35 | 24 | 1 | 10 | 31.4% |
| 10 | `DIS-PV` — Polycythemia Vera | 6 | 24 | 24 | 0 | 0 | 0.0% |

## Top 10 best-cited diseases (by outcomes-cited %)

Sorted by `(cited + probably-cited) / populated`. Tie-broken by absolute `cited` count, then disease id. Diseases with zero populated outcome fields are excluded.

| # | Disease | Indications | populated | cited | probably-cited | uncited | outcomes-cited % (loose) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `DIS-T-PLL` — T-Cell Prolymphocytic Leukemia | 2 | 8 | 8 | 0 | 0 | 100.0% |
| 2 | `DIS-HNSCC` — Head and neck squamous cell carcinoma (HNSCC) | 5 | 21 | 18 | 0 | 3 | 85.7% |
| 3 | `DIS-ESOPHAGEAL` — Esophageal carcinoma (squamous + adeno) | 6 | 20 | 6 | 5 | 9 | 55.0% |
| 4 | `DIS-BREAST` — Breast cancer (invasive) | 26 | 47 | 23 | 2 | 22 | 53.2% |
| 5 | `DIS-MTC` — Medullary thyroid carcinoma (MTC) | 2 | 6 | 3 | 0 | 3 | 50.0% |
| 6 | `DIS-GASTRIC` — Gastric / GEJ adenocarcinoma | 6 | 25 | 4 | 8 | 13 | 48.0% |
| 7 | `DIS-RCC` — Renal cell carcinoma | 8 | 18 | 2 | 5 | 11 | 38.9% |
| 8 | `DIS-PROSTATE` — Prostate adenocarcinoma | 8 | 35 | 10 | 1 | 24 | 31.4% |
| 9 | `DIS-NSCLC` — Non-small cell lung cancer | 40 | 120 | 33 | 4 | 83 | 30.8% |
| 10 | `DIS-MM` — Multiple Myeloma | 13 | 52 | 3 | 12 | 37 | 28.8% |

## Per-disease rollup (all diseases, alphabetical)

| Disease | Indications | populated | absent | cited | probably-cited | uncited | outcomes-cited % (loose) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `DIS-AITL` — Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma | 5 | 20 | 5 | 1 | 0 | 19 | 5.0% |
| `DIS-ALCL` — Anaplastic Large Cell Lymphoma (systemic) | 5 | 20 | 5 | 1 | 1 | 18 | 10.0% |
| `DIS-AML` — Acute Myeloid Leukemia (non-APL) | 15 | 60 | 15 | 4 | 1 | 55 | 8.3% |
| `DIS-ANAL-SCC` — Squamous cell carcinoma of the anal canal | 3 | 10 | 11 | 0 | 0 | 10 | 0.0% |
| `DIS-APL` — Acute Promyelocytic Leukemia (PML-RARA) | 4 | 16 | 4 | 0 | 0 | 16 | 0.0% |
| `DIS-ATLL` — Adult T-Cell Leukemia/Lymphoma | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-B-ALL` — B-Lymphoblastic Leukemia / Lymphoma | 6 | 24 | 6 | 0 | 1 | 23 | 4.2% |
| `DIS-BREAST` — Breast cancer (invasive) | 26 | 47 | 112 | 23 | 2 | 22 | 53.2% |
| `DIS-BURKITT` — Burkitt Lymphoma | 5 | 20 | 5 | 0 | 0 | 20 | 0.0% |
| `DIS-CERVICAL` — Cervical carcinoma (squamous predominant + adeno) | 3 | 12 | 3 | 3 | 0 | 9 | 25.0% |
| `DIS-CHL` — Classical Hodgkin Lymphoma | 7 | 28 | 7 | 2 | 5 | 21 | 25.0% |
| `DIS-CHOLANGIOCARCINOMA` — Cholangiocarcinoma (bile duct cancer) | 4 | 11 | 9 | 0 | 0 | 11 | 0.0% |
| `DIS-CHONDROSARCOMA` — Chondrosarcoma | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-CLL` — Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma | 7 | 28 | 7 | 0 | 8 | 20 | 28.6% |
| `DIS-CML` — Chronic Myeloid Leukemia (BCR-ABL1) | 5 | 20 | 5 | 0 | 1 | 19 | 5.0% |
| `DIS-CRC` — Colorectal carcinoma (CRC) | 22 | 85 | 27 | 7 | 6 | 72 | 15.3% |
| `DIS-DLBCL-NOS` — Diffuse Large B-Cell Lymphoma, NOS | 12 | 48 | 12 | 2 | 4 | 42 | 12.5% |
| `DIS-EATL` — Enteropathy-Associated T-Cell Lymphoma | 2 | 8 | 2 | 0 | 0 | 8 | 0.0% |
| `DIS-ENDOMETRIAL` — Endometrial carcinoma | 5 | 14 | 13 | 1 | 3 | 10 | 28.6% |
| `DIS-ESOPHAGEAL` — Esophageal carcinoma (squamous + adeno) | 6 | 20 | 12 | 6 | 5 | 9 | 55.0% |
| `DIS-ET` — Essential Thrombocythemia | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-FL` — Follicular Lymphoma | 7 | 27 | 8 | 0 | 2 | 25 | 7.4% |
| `DIS-GASTRIC` — Gastric / GEJ adenocarcinoma | 6 | 25 | 7 | 4 | 8 | 13 | 48.0% |
| `DIS-GBM` — Glioblastoma (IDH-WT, WHO grade 4) | 4 | 8 | 15 | 0 | 0 | 8 | 0.0% |
| `DIS-GI-NET` — Gastroenteropancreatic neuroendocrine tumor — GI origin (carcinoid), well-differentiated G1/G2 | 1 | 4 | 1 | 0 | 0 | 4 | 0.0% |
| `DIS-GIST` — Gastrointestinal stromal tumor (GIST) | 3 | 10 | 5 | 0 | 1 | 9 | 10.0% |
| `DIS-GLIOMA-LOW-GRADE` — Low-grade glioma (LGG, WHO grade 2 — IDH-mutant) | 1 | 3 | 2 | 0 | 0 | 3 | 0.0% |
| `DIS-HCC` — Hepatocellular carcinoma (HCC) | 6 | 24 | 6 | 3 | 0 | 21 | 12.5% |
| `DIS-HCL` — Hairy Cell Leukemia | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-HCV-MZL` — HCV-associated Marginal Zone Lymphoma | 3 | 14 | 1 | 0 | 0 | 14 | 0.0% |
| `DIS-HGBL-DH` — High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit) | 3 | 12 | 3 | 2 | 0 | 10 | 16.7% |
| `DIS-HNSCC` — Head and neck squamous cell carcinoma (HNSCC) | 5 | 21 | 15 | 18 | 0 | 3 | 85.7% |
| `DIS-HSTCL` — Hepatosplenic T-Cell Lymphoma | 2 | 8 | 2 | 0 | 0 | 8 | 0.0% |
| `DIS-IFS` — Infantile fibrosarcoma (IFS) | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-IMT` — Inflammatory myofibroblastic tumor (IMT) | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-MASTOCYTOSIS` — Advanced systemic mastocytosis (AdvSM) | 2 | 6 | 4 | 0 | 0 | 6 | 0.0% |
| `DIS-MCL` — Mantle Cell Lymphoma | 7 | 28 | 7 | 3 | 2 | 23 | 17.9% |
| `DIS-MDS-HR` — Myelodysplastic Syndromes — Higher-Risk (IPSS-R high / very high; includes MDS-EB) | 3 | 12 | 3 | 1 | 0 | 11 | 8.3% |
| `DIS-MDS-LR` — Myelodysplastic Syndromes — Lower-Risk (IPSS-R very low / low / intermediate) | 4 | 16 | 4 | 1 | 0 | 15 | 6.2% |
| `DIS-MELANOMA` — Cutaneous melanoma | 11 | 37 | 20 | 9 | 0 | 28 | 24.3% |
| `DIS-MESOTHELIOMA` — Malignant pleural mesothelioma (MPM) | 2 | 7 | 4 | 2 | 0 | 5 | 28.6% |
| `DIS-MF-SEZARY` — Mycosis Fungoides / Sézary Syndrome | 5 | 20 | 5 | 0 | 0 | 20 | 0.0% |
| `DIS-MM` — Multiple Myeloma | 13 | 52 | 19 | 3 | 12 | 37 | 28.8% |
| `DIS-MPNST` — Malignant peripheral nerve sheath tumor (MPNST) | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-MTC` — Medullary thyroid carcinoma (MTC) | 2 | 6 | 4 | 3 | 0 | 3 | 50.0% |
| `DIS-NK-T-NASAL` — Extranodal NK/T-Cell Lymphoma, Nasal Type | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-NLPBL` — Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL) | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-NODAL-MZL` — Nodal Marginal Zone Lymphoma | 4 | 15 | 5 | 0 | 0 | 15 | 0.0% |
| `DIS-NSCLC` — Non-small cell lung cancer | 40 | 120 | 114 | 33 | 4 | 83 | 30.8% |
| `DIS-OVARIAN` — Ovarian carcinoma (high-grade serous predominant) | 15 | 48 | 27 | 4 | 2 | 42 | 12.5% |
| `DIS-PCNSL` — Primary Diffuse Large B-Cell Lymphoma of the CNS | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-PDAC` — Pancreatic ductal adenocarcinoma (PDAC) | 4 | 13 | 7 | 3 | 0 | 10 | 23.1% |
| `DIS-PMBCL` — Primary Mediastinal (Thymic) Large B-Cell Lymphoma | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-PMF` — Primary Myelofibrosis (DIPSS-Plus stratified) | 5 | 20 | 5 | 0 | 0 | 20 | 0.0% |
| `DIS-PNET` — Pancreatic neuroendocrine tumor (pNET), well-differentiated G1/G2 | 1 | 4 | 1 | 0 | 0 | 4 | 0.0% |
| `DIS-PROSTATE` — Prostate adenocarcinoma | 8 | 35 | 35 | 10 | 1 | 24 | 31.4% |
| `DIS-PTCL-NOS` — Peripheral T-Cell Lymphoma, Not Otherwise Specified | 4 | 16 | 4 | 0 | 1 | 15 | 6.2% |
| `DIS-PTLD` — Post-Transplant Lymphoproliferative Disorder | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-PV` — Polycythemia Vera | 6 | 24 | 6 | 0 | 0 | 24 | 0.0% |
| `DIS-RCC` — Renal cell carcinoma | 8 | 18 | 32 | 2 | 5 | 11 | 38.9% |
| `DIS-SALIVARY` — Salivary gland carcinoma | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-SCLC` — Small cell lung cancer | 5 | 13 | 15 | 0 | 1 | 12 | 7.7% |
| `DIS-SOFT-TISSUE-SARCOMA` — Soft tissue sarcoma (STS) | 4 | 18 | 16 | 0 | 0 | 18 | 0.0% |
| `DIS-SPLENIC-MZL` — Splenic Marginal Zone Lymphoma | 3 | 12 | 3 | 0 | 0 | 12 | 0.0% |
| `DIS-T-ALL` — T-Lymphoblastic Leukemia / Lymphoma | 2 | 8 | 2 | 0 | 0 | 8 | 0.0% |
| `DIS-T-PLL` — T-Cell Prolymphocytic Leukemia | 2 | 8 | 2 | 8 | 0 | 0 | 100.0% |
| `DIS-TESTICULAR-GCT` — Testicular germ cell tumor (GCT) | 4 | 14 | 15 | 0 | 0 | 14 | 0.0% |
| `DIS-THYROID-ANAPLASTIC` — Anaplastic thyroid carcinoma (ATC) | 2 | 4 | 6 | 0 | 0 | 4 | 0.0% |
| `DIS-THYROID-PAPILLARY` — Papillary thyroid carcinoma (PTC) | 1 | 0 | 5 | 0 | 0 | 0 | 0.0% |
| `DIS-UROTHELIAL` — Urothelial carcinoma (bladder + upper tract) | 6 | 14 | 24 | 4 | 0 | 10 | 28.6% |
| `DIS-WM` — Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma | 5 | 20 | 5 | 0 | 0 | 20 | 0.0% |

## Worst 3 diseases — full per-indication detail

Per the plan brief, the worst three diseases (by `uncited` count) are inlined here. The remaining diseases' per-indication detail lives in the appendix [`expected_outcomes_traceability_2026-05-01_by_disease.md`](expected_outcomes_traceability_2026-05-01_by_disease.md).

### `DIS-NSCLC` — Non-small cell lung cancer

Indications: 40; populated: 120; cited: 33; probably-cited: 4; uncited: 83; absent: 114.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-NSCLC-2L-BRAF-V600E-DAB-TRAM | overall_response_rate | uncited | — | ~63% pretreated cohort B; ~64% 1L cohort C (BRF113928) |
| IND-NSCLC-2L-BRAF-V600E-DAB-TRAM | overall_survival_5y | uncited | — | Median OS 18.2 mo (cohort B) |
| IND-NSCLC-2L-BRAF-V600E-DAB-TRAM | progression_free_survival | uncited | — | Median PFS 9.7 mo (cohort B) |
| IND-NSCLC-2L-DATO-DXD | overall_response_rate | uncited | — | ~26% nonsquamous Dato-DXd vs ~13% docetaxel |
| IND-NSCLC-2L-DATO-DXD | overall_survival | uncited | — | ITT OS not statistically significant; nonsquamous numerical trend favors Dato-DXd; FDA approval restricted to EGFR-mu... |
| IND-NSCLC-2L-DATO-DXD | progression_free_survival | uncited | — | mPFS 5.6 vs 3.7 mo nonsquamous (HR 0.84, 95% CI 0.74-0.95) — TROPION-Lung01 phase III |
| IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB | overall_response_rate | uncited | — | ~23% (REVEL doc-ram vs 14% docetaxel) |
| IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB | overall_survival_5y | uncited | — | Median OS 10.5 vs 9.1 mo (HR 0.86); 1-year OS ~46% |
| IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB | progression_free_survival | uncited | — | Median PFS ~4.5 mo (REVEL doc-ram vs 3.0 mo doc; HR 0.76) |
| IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB | overall_response_rate | uncited | — | ~40% (CHRYSALIS post-platinum cohort) |
| IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB | overall_survival_5y | uncited | — | Median OS 22.8 mo (CHRYSALIS) |
| IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB | progression_free_survival | uncited | — | Median PFS 8.3 mo (CHRYSALIS) |
| IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ | overall_response_rate | uncited | — | ~36-42% (MARIPOSA-2 ami+laz±chemo arms vs chemo alone) |
| IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ | overall_survival_5y | uncited | — | OS interim — trend toward benefit; mature OS data evolving |
| IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ | progression_free_survival | uncited | — | Median PFS 8.3 mo (ami+chemo) and similar 8.3 mo (ami+laz+chemo) vs 4.2 mo chemo alone (HR ~0.44-0.48) |
| IND-NSCLC-2L-HER2-MUT-T-DXD | overall_response_rate | cited | trial-number resolved: DESTINY-Lung01 | ~49% (DESTINY-Lung02 5.4 mg/kg dose); ~55% (DESTINY-Lung01 6.4 mg/kg) |
| IND-NSCLC-2L-HER2-MUT-T-DXD | overall_survival_5y | cited | trial-number resolved: DESTINY-Lung01 | Median OS 19.5 mo (DESTINY-Lung02 5.4 mg/kg); 17.8 mo (DESTINY-Lung01) |
| IND-NSCLC-2L-HER2-MUT-T-DXD | progression_free_survival | cited | trial-number resolved: DESTINY-Lung02 | Median PFS 9.9 mo (DESTINY-Lung02 5.4 mg/kg) |
| IND-NSCLC-2L-KRAS-G12C-ADAGRASIB | overall_response_rate | cited | trial-number resolved: KRYSTAL-1 | ~43% (KRYSTAL-1) |
| IND-NSCLC-2L-KRAS-G12C-ADAGRASIB | overall_survival_5y | cited | trial-number resolved: KRYSTAL-1 | Median OS 12.6 mo (KRYSTAL-1); intracranial ORR ~33% |
| IND-NSCLC-2L-KRAS-G12C-ADAGRASIB | progression_free_survival | cited | trial-number resolved: KRYSTAL-1 | Median PFS 6.5 mo (KRYSTAL-1) |
| IND-NSCLC-2L-KRAS-G12C-SOTORASIB | overall_response_rate | probably-cited | trial-family: CodeBreaK | ~28% (CodeBreaK 200 vs 13% docetaxel) |
| IND-NSCLC-2L-KRAS-G12C-SOTORASIB | overall_survival_5y | uncited | — | Median OS not significant vs docetaxel (HR 1.01) — crossover-confounded |
| IND-NSCLC-2L-KRAS-G12C-SOTORASIB | progression_free_survival | probably-cited | trial-family: CodeBreaK | Median PFS 5.6 mo (CodeBreaK 200 vs 4.5 mo docetaxel; HR 0.66) |
| IND-NSCLC-2L-MET-AMP-CAPMATINIB | overall_response_rate | uncited | — | ~40% (GEOMETRY mono-1 high-amp GCN ≥10 cohort) |
| IND-NSCLC-2L-MET-AMP-CAPMATINIB | overall_survival_5y | uncited | — | Mature OS evolving |
| IND-NSCLC-2L-MET-AMP-CAPMATINIB | progression_free_survival | uncited | — | Median PFS ~5.5 mo (high-amp cohort) |
| IND-NSCLC-2L-MET-EX14-CAPMATINIB | overall_response_rate | uncited | — | ~41% pretreated; ~68% TKI-naïve (GEOMETRY mono-1) |
| IND-NSCLC-2L-MET-EX14-CAPMATINIB | overall_survival_5y | uncited | — | Mature OS evolving |
| IND-NSCLC-2L-MET-EX14-CAPMATINIB | progression_free_survival | uncited | — | Median PFS 5.4 mo pretreated; 12.4 mo TKI-naïve |
| IND-NSCLC-2L-MET-EX14-TEPOTINIB | overall_response_rate | cited | trial-number resolved: VISION | ~46% combined cohort (1L 43%, pretreated 48% — VISION) |
| IND-NSCLC-2L-MET-EX14-TEPOTINIB | overall_survival_5y | uncited | — | Mature OS evolving |
| IND-NSCLC-2L-MET-EX14-TEPOTINIB | progression_free_survival | uncited | — | Median DOR 11.1 mo |
| IND-NSCLC-2L-NTRK-LAROTRECTINIB | overall_response_rate | uncited | — | ~75% pooled (NAVIGATE / SCOUT / phase-1; tumor-agnostic incl. NSCLC subset) |
| IND-NSCLC-2L-NTRK-LAROTRECTINIB | overall_survival_5y | uncited | — | Mature OS evolving; tumor-agnostic data |
| IND-NSCLC-2L-NTRK-LAROTRECTINIB | progression_free_survival | uncited | — | Median DOR not reached at 9.4 mo follow-up in pooled analysis; subsequent updates show durable responses |
| IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL | overall_response_rate | uncited | — | ~23% (REVEL doc-ram vs 14% docetaxel) |
| IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL | overall_survival_5y | uncited | — | Median OS 10.5 vs 9.1 mo (HR 0.86); 1-year OS ~46% |
| IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL | progression_free_survival | uncited | — | Median PFS ~4.5 mo (REVEL doc-ram vs 3.0 mo doc; HR 0.76) |
| IND-NSCLC-2L-RET-FUSION-SELPERCATINIB | overall_response_rate | cited | trial-number resolved: LIBRETTO-001 | ~64% pretreated; ~85% TKI-naïve (LIBRETTO-001) |
| IND-NSCLC-2L-RET-FUSION-SELPERCATINIB | overall_survival_5y | cited | trial-number resolved: LIBRETTO-431 | Mature OS evolving; LIBRETTO-431 phase-3 vs platinum±pembrolizumab confirmed PFS HR 0.46 |
| IND-NSCLC-2L-RET-FUSION-SELPERCATINIB | progression_free_survival | uncited | — | Median PFS 16.5 mo pretreated; intracranial ORR 91% (measurable brain mets) |
| IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB | overall_response_rate | uncited | — | ~67% post-crizotinib (lower than 1L; depends on resistance profile) |
| IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB | overall_survival_5y | uncited | — | Mature OS data evolving |
| IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB | progression_free_survival | uncited | — | Median PFS ~8-13 mo post-crizotinib (lower than 19 mo TKI-naïve) |
| IND-NSCLC-2L-ROS1-REPOTRECTINIB | overall_response_rate | uncited | — | ~79% TKI-naïve; ~38% post-1 ROS1-TKI (TRIDENT-1) |
| IND-NSCLC-2L-ROS1-REPOTRECTINIB | overall_survival_5y | uncited | — | Mature OS evolving; intracranial ORR 89% TKI-naïve |
| IND-NSCLC-2L-ROS1-REPOTRECTINIB | progression_free_survival | uncited | — | TKI-naïve mDOR 34.1 mo; post-TKI mPFS ~9 mo |
| IND-NSCLC-3L-DRIVER-BEYOND-2L | complete_response | uncited | — | ~1% |
| IND-NSCLC-3L-DRIVER-BEYOND-2L | overall_response_rate | uncited | — | ~23% docetaxel + ramucirumab (REVEL Garon 2014 Lancet) |
| IND-NSCLC-3L-DRIVER-BEYOND-2L | overall_survival_5y | uncited | — | Median OS 10.5 vs 9.1 mo (REVEL HR 0.86); benefit modest in 3L+ |
| IND-NSCLC-3L-DRIVER-BEYOND-2L | progression_free_survival | uncited | — | Median PFS 4.5 vs 3.0 mo (REVEL HR 0.76) |
| IND-NSCLC-3L-OSI-FAILURE-AMI | complete_response | uncited | — | ~3% |
| IND-NSCLC-3L-OSI-FAILURE-AMI | overall_response_rate | uncited | — | ~63% amivantamab + lazertinib + chemo (MARIPOSA-2 Passaro 2024 Ann Oncol) |
| IND-NSCLC-3L-OSI-FAILURE-AMI | overall_survival_5y | uncited | — | OS data immature; HR 0.77 trending favorable |
| IND-NSCLC-3L-OSI-FAILURE-AMI | progression_free_survival | uncited | — | Median PFS 8.3 mo amivantamab + chemo vs 4.2 mo chemo alone (MARIPOSA-2) |
| IND-NSCLC-ALK-1L-ENSARTINIB | intracranial_orr | uncited | — | ~64% ensartinib in patients with baseline brain metastases |
| IND-NSCLC-ALK-1L-ENSARTINIB | overall_response_rate | uncited | — | ~74% ensartinib (BICR) |
| IND-NSCLC-ALK-1L-ENSARTINIB | overall_survival | uncited | — | Mature OS evolving; eXalt3 phase III primary endpoint PFS |
| IND-NSCLC-ALK-1L-ENSARTINIB | progression_free_survival | uncited | — | mPFS 25.8 mo (eXalt3 ensartinib) vs 12.7 mo (crizotinib); HR 0.51 (95% CI 0.35-0.72) |
| IND-NSCLC-ALK-2L-LORLATINIB | overall_response_rate | uncited | — | ~40-50% post-2nd-gen TKI (lower than 1L; depends on resistance mutation profile) |
| IND-NSCLC-ALK-2L-LORLATINIB | overall_survival_5y | uncited | — | Mature OS data evolving; 2-year OS ~60-70% |
| IND-NSCLC-ALK-2L-LORLATINIB | progression_free_survival | uncited | — | Median PFS ~7-11 mo post-alectinib failure; longer if specific resistance mutations |
| IND-NSCLC-ALK-MAINT-ALECTINIB | complete_response | uncited | — | ~5% |
| IND-NSCLC-ALK-MAINT-ALECTINIB | overall_response_rate | cited | trial-number resolved: ALEX | ~83% during initial response phase (ALEX) |
| IND-NSCLC-ALK-MAINT-ALECTINIB | overall_survival_5y | cited | trial-number resolved: ALEX | 5-yr OS ~62.5% (ALEX 5-yr update Mok 2024 Annals Oncol) |
| IND-NSCLC-ALK-MAINT-ALECTINIB | progression_free_survival | cited | trial-number resolved: ALEX | Median PFS 34.8 mo (ALEX Mok 2020 update) |
| IND-NSCLC-ALK-MET-1L | median_overall_survival_months | cited | trial-number resolved: ALEX | >5 years (ALEX) |
| IND-NSCLC-ALK-MET-1L | median_progression_free_survival_months | uncited | — | 35 |
| IND-NSCLC-BRAF-V600E-1L-DAB-TRAM | median_pfs_months | uncited | — | ~10.9 |
| IND-NSCLC-BRAF-V600E-1L-DAB-TRAM | orr_treatment_naive | uncited | — | 64.4% (36 treatment-naive; BRF113928 cohort C) |
| IND-NSCLC-EGFR-MAINT-OSIMERTINIB | complete_response | uncited | — | ~3% (deep CR rare) |
| IND-NSCLC-EGFR-MAINT-OSIMERTINIB | overall_response_rate | cited | trial-number resolved: FLAURA | ~80% during initial response phase (FLAURA) |
| IND-NSCLC-EGFR-MAINT-OSIMERTINIB | overall_survival_5y | cited | trial-number resolved: FLAURA | Median OS ~38.6 mo vs ~31.8 mo with 1st-gen TKI (FLAURA OS update) |
| IND-NSCLC-EGFR-MAINT-OSIMERTINIB | progression_free_survival | cited | trial-number resolved: FLAURA | Median PFS ~18.9 mo (FLAURA Soria 2018, Ramalingam 2020 update) |
| IND-NSCLC-EGFR-MUT-MET-1L | median_overall_survival_months | cited | trial-number resolved: FLAURA | 39 |
| IND-NSCLC-EGFR-MUT-MET-1L | median_progression_free_survival_months | cited | trial-number resolved: FLAURA | 19 |
| IND-NSCLC-EGFR-POST-OSI-PATRITUMAB-DXD | duration_of_response | uncited | — | mDOR 5.6 mo |
| IND-NSCLC-EGFR-POST-OSI-PATRITUMAB-DXD | intracranial_orr | uncited | — | ~33% non-irradiated brain metastases |
| IND-NSCLC-EGFR-POST-OSI-PATRITUMAB-DXD | overall_response_rate | uncited | — | ~30% blinded independent central review (HERTHENA-Lung01 phase II, n=225) |
| IND-NSCLC-EGFR-POST-OSI-PATRITUMAB-DXD | progression_free_survival | uncited | — | mPFS 5.5 mo (95% CI 5.1-5.9) |
| IND-NSCLC-ELDERLY-CARBO-PEM-MOD | complete_response | uncited | — | ~3% |
| IND-NSCLC-ELDERLY-CARBO-PEM-MOD | overall_response_rate | uncited | — | ~30% carbo + pem (extrapolated from JCOG 0803 elderly NSCLC; Quoix 2011 Lancet) |
| IND-NSCLC-ELDERLY-CARBO-PEM-MOD | overall_survival_5y | cited | trial-number resolved: KEYNOTE-189 | Median OS ~10-14 mo (elderly cohorts; addition of pembro per KEYNOTE-189 may extend further) |
| IND-NSCLC-ELDERLY-CARBO-PEM-MOD | progression_free_survival | uncited | — | Median PFS ~5-6 mo (elderly cohorts; lower than fit cohorts) |
| IND-NSCLC-KRAS-G12C-MET-2L | median_progression_free_survival_months | probably-cited | trial-family: CodeBreaK | 6.5 |
| IND-NSCLC-MET-EX14-1L-CAPMATINIB | duration_of_response | uncited | — | 12.6 months median DOR (treatment-naive) |
| IND-NSCLC-MET-EX14-1L-CAPMATINIB | orr_treatment_naive | uncited | — | 67.9% (27/40 treatment-naive cohort; GEOMETRY mono-1) |
| IND-NSCLC-MET-EX14-1L-CAPMATINIB | pfs_months | uncited | — | ~12.4 (treatment-naive cohort) |
| IND-NSCLC-NRG1-ZENOCUTUZUMAB | duration_of_response | uncited | — | mDOR 7.4 mo NSCLC subset |
| IND-NSCLC-NRG1-ZENOCUTUZUMAB | overall_response_rate | uncited | — | ~33% NSCLC subset (eNRGy phase II registration cohort, n=93 NSCLC) |
| IND-NSCLC-NRG1-ZENOCUTUZUMAB | pan_tumor_orr | uncited | — | ~37% all-tumor pooled; activity also documented in pancreatic NRG1-fusion+ adenocarcinoma |
| IND-NSCLC-NRG1-ZENOCUTUZUMAB | progression_free_survival | uncited | — | mPFS ~6.8 mo NSCLC subset |
| IND-NSCLC-NTRK-FUSION-1L-LAROTRECTINIB | duration_of_response | uncited | — | 12 months+ median DOR in most series |
| IND-NSCLC-NTRK-FUSION-1L-LAROTRECTINIB | orr_across_histologies | uncited | — | ~75% (Drilon 2018 NEJM; n=55 tumor-agnostic) |
| IND-NSCLC-PDL1-22C3-PEMBRO-CLONE-SPECIFIC | five_year_overall_survival | cited | trial-number resolved: KEYNOTE-024 | 32% pembro mono vs 16% chemo (KEYNOTE-024 5-year update) |
| IND-NSCLC-PDL1-22C3-PEMBRO-CLONE-SPECIFIC | median_overall_survival | cited | trial-number resolved: KEYNOTE-024 | 26.3 mo pembro vs 13.4 mo chemo (KEYNOTE-024) |
| IND-NSCLC-PDL1-22C3-PEMBRO-CLONE-SPECIFIC | overall_response_rate | uncited | — | ~45% pembro mono |
| IND-NSCLC-PDL1-22C3-PEMBRO-CLONE-SPECIFIC | progression_free_survival | cited | trial-number resolved: KEYNOTE-024 | mPFS 7.7 mo pembro vs 5.5 mo chemo (KEYNOTE-024) |
| IND-NSCLC-PDL1-HIGH-MET-1L | five_year_overall_survival | cited | trial-number resolved: KEYNOTE-024 | 32% pembro mono vs 16% chemo |
| IND-NSCLC-PDL1-LOW-NONSQ-MET-1L | median_overall_survival_months | cited | trial-number resolved: KEYNOTE-189 | 22 |
| IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO | overall_response_rate | uncited | — | Sustained from induction; maintenance deepens responses in ~10-15% |
| IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO | overall_survival_5y | cited | trial-number resolved: KEYNOTE-189 | 5-year OS ~19-22% (KEYNOTE-189 5-year update; vs ~11% chemo alone) |
| IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO | progression_free_survival | cited | trial-number resolved: KEYNOTE-189 | Median PFS ~8.8 mo (KEYNOTE-189 non-squamous from start) |
| IND-NSCLC-RET-FUSION-1L-SELPERCATINIB | libretto431_pfs_hr | cited | trial-number resolved: LIBRETTO-001 | 0.46 |
| IND-NSCLC-RET-FUSION-1L-SELPERCATINIB | median_pfs_months | cited | trial-number resolved: LIBRETTO-001 | ~22 (LIBRETTO-001 treatment-naive cohort) |
| IND-NSCLC-RET-FUSION-1L-SELPERCATINIB | orr_12m_dor | cited | trial-number resolved: LIBRETTO-001 | ~70% |
| IND-NSCLC-RET-FUSION-1L-SELPERCATINIB | orr_treatment_naive | cited | trial-number resolved: LIBRETTO-001 | 84.1% (LIBRETTO-001; treatment-naive) |
| IND-NSCLC-ROS1-1L-REPOTRECTINIB | duration_of_response | uncited | — | mDOR 34.1 mo TKI-naïve |
| IND-NSCLC-ROS1-1L-REPOTRECTINIB | intracranial_orr | uncited | — | ~89% TKI-naïve with measurable brain metastases |
| IND-NSCLC-ROS1-1L-REPOTRECTINIB | overall_response_rate | uncited | — | ~79% TKI-naïve (TRIDENT-1 phase I/II registration) |
| IND-NSCLC-ROS1-1L-REPOTRECTINIB | progression_free_survival | uncited | — | mPFS not reached at 24-mo follow-up TKI-naïve cohort |
| IND-NSCLC-STAGE-III-PACIFIC | five_year_overall_survival | probably-cited | trial-family: PACIFIC | 43% durva vs 33% placebo |
| IND-NSCLC-TMB-HIGH-MET-1L-PEMBRO-MONO | median_overall_survival_months | cited | trial-number resolved: KEYNOTE-042 | Not reached at 11.7 mo median follow-up (KEYNOTE-158 NSCLC subset, n=37) |
| IND-NSCLC-TMB-HIGH-MET-1L-PEMBRO-MONO | median_progression_free_survival_months | cited | trial-number resolved: KEYNOTE-042 | 4.1 |
| IND-NSCLC-TMB-HIGH-MET-1L-PEMBRO-MONO | overall_response_rate | cited | trial-number resolved: KEYNOTE-042 | ORR 29% in TMB-high subgroup (vs 6% in TMB-low) per KEYNOTE-158 pan-tumor |
| IND-PAN-NTRK-2L-REPOTRECTINIB | duration_of_response | uncited | — | TRK-naïve mDOR not reached at 24-mo follow-up; post-TKI mDOR ~10 mo |
| IND-PAN-NTRK-2L-REPOTRECTINIB | intracranial_orr | uncited | — | ~50% NTRK-fusion+ tumors with measurable CNS disease |
| IND-PAN-NTRK-2L-REPOTRECTINIB | overall_response_rate | uncited | — | ~58% TRK-naïve; ~50% post-prior TKI (TRIDENT-1 NTRK arm tumor-agnostic, n=88) |
| IND-PAN-NTRK-2L-REPOTRECTINIB | progression_free_survival | uncited | — | TRK-naïve mPFS not reached; post-TKI mPFS ~7 mo |

### `DIS-CRC` — Colorectal carcinoma (CRC)

Indications: 22; populated: 85; cited: 7; probably-cited: 6; uncited: 72; absent: 27.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CRC-3L-FRUQUINTINIB | overall_response_rate | uncited | — | ~1.5% (FRESCO-2; biologic effect dominated by disease stabilization, DCR ~55.5%) |
| IND-CRC-3L-FRUQUINTINIB | overall_survival_5y | uncited | — | Median OS 7.4 mo vs 4.8 mo placebo (FRESCO-2; HR 0.66) |
| IND-CRC-3L-FRUQUINTINIB | progression_free_survival | uncited | — | Median PFS 3.7 mo vs 1.8 mo placebo (FRESCO-2; HR 0.32) |
| IND-CRC-ADJUVANT-STAGE2-HIGHRISK-FOLFOX | complete_response | uncited | — | n/a (post-resection) |
| IND-CRC-ADJUVANT-STAGE2-HIGHRISK-FOLFOX | overall_response_rate | uncited | — | Adjuvant — no response endpoint |
| IND-CRC-ADJUVANT-STAGE2-HIGHRISK-FOLFOX | overall_survival_5y | uncited | — | 5-yr OS ~80-85%; absolute benefit ~3-5% for high-risk stage II |
| IND-CRC-ADJUVANT-STAGE2-HIGHRISK-FOLFOX | progression_free_survival | uncited | — | 5-yr DFS ~75-80% high-risk stage II with adjuvant (vs ~70% without) |
| IND-CRC-ADJUVANT-STAGE3-CAPOX | complete_response | uncited | — | n/a (post-resection) |
| IND-CRC-ADJUVANT-STAGE3-CAPOX | overall_response_rate | uncited | — | Adjuvant — DFS endpoint |
| IND-CRC-ADJUVANT-STAGE3-CAPOX | overall_survival_5y | uncited | — | 5-yr OS ~75-85% stage III; low-risk T1-3 N1 ~85% |
| IND-CRC-ADJUVANT-STAGE3-CAPOX | progression_free_survival | uncited | — | 5-yr DFS: ~73% stage III (all) with oxaliplatin-based adjuvant |
| IND-CRC-ADJUVANT-STAGE3-FOLFOX | complete_response | uncited | — | n/a (post-resection) |
| IND-CRC-ADJUVANT-STAGE3-FOLFOX | overall_response_rate | uncited | — | Adjuvant — assessed by DFS not response |
| IND-CRC-ADJUVANT-STAGE3-FOLFOX | overall_survival_5y | uncited | — | 5-yr OS ~75-85% (depends on sub-stage + tumor biology) |
| IND-CRC-ADJUVANT-STAGE3-FOLFOX | progression_free_survival | uncited | — | 5-yr DFS ~70-75% stage III low-risk; ~55-65% high-risk |
| IND-CRC-METASTATIC-1L-FOLFOX-BEV | complete_response | uncited | — | ~5-8% |
| IND-CRC-METASTATIC-1L-FOLFOX-BEV | overall_response_rate | uncited | — | ~50% |
| IND-CRC-METASTATIC-1L-FOLFOX-BEV | overall_survival_5y | uncited | — | mOS ~24-28 mo (RAS-mutant subgroup) |
| IND-CRC-METASTATIC-1L-FOLFOX-BEV | progression_free_survival | uncited | — | Median ~10-11 mo |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | complete_response | uncited | — | ~5% |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | overall_response_rate | uncited | — | 65-70% (TRIBE; vs ~53% FOLFIRI+bev) |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | overall_survival_5y | uncited | — | ~30% at 5 years (TRIBE long-term) |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | overall_survival_median | uncited | — | mOS 29.8 mo (TRIBE; HR 0.80 vs FOLFIRI+bev) |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | progression_free_survival | uncited | — | mPFS 12.1 mo (TRIBE; HR 0.75 vs FOLFIRI+bev) |
| IND-CRC-METASTATIC-1L-FOLFOXIRI-BEV | r0_resection_rate | uncited | — | 15% vs 12% (TRIBE; higher conversion in liver-limited disease) |
| IND-CRC-METASTATIC-1L-MSI-H-PEMBRO | complete_response | uncited | — | ~13% |
| IND-CRC-METASTATIC-1L-MSI-H-PEMBRO | overall_response_rate | cited | trial-number resolved: KEYNOTE-177 | ~44% (KEYNOTE-177 ORR pembrolizumab arm) |
| IND-CRC-METASTATIC-1L-MSI-H-PEMBRO | overall_survival_5y | uncited | — | Confounded by 60% crossover; ORR + duration favor pembrolizumab definitively |
| IND-CRC-METASTATIC-1L-MSI-H-PEMBRO | progression_free_survival | cited | trial-number resolved: KEYNOTE-177 | Median 16.5 mo vs 8.2 mo on FOLFOX+bev (KEYNOTE-177) |
| IND-CRC-METASTATIC-1L-RAS-WT-LEFT | complete_response | uncited | — | ~10-15% |
| IND-CRC-METASTATIC-1L-RAS-WT-LEFT | overall_response_rate | uncited | — | ~70% (FIRE-3, CALGB-80405 left-sided subgroup) |
| IND-CRC-METASTATIC-1L-RAS-WT-LEFT | overall_survival_5y | uncited | — | mOS ~30+ mo for left-sided RAS-WT (vs ~24 right-sided) |
| IND-CRC-METASTATIC-1L-RAS-WT-LEFT | progression_free_survival | uncited | — | Median ~10-11 mo |
| IND-CRC-METASTATIC-2L-BRAF-BEACON | complete_response | uncited | — | ~3% |
| IND-CRC-METASTATIC-2L-BRAF-BEACON | overall_response_rate | probably-cited | trial-number unresolved: BEACON | ~20% (BEACON CRC doublet) |
| IND-CRC-METASTATIC-2L-BRAF-BEACON | overall_survival_5y | probably-cited | trial-number unresolved: BEACON | mOS 9.3 vs 5.9 mo control (BEACON) |
| IND-CRC-METASTATIC-2L-BRAF-BEACON | progression_free_survival | uncited | — | Median ~4.3 mo |
| IND-CRC-METASTATIC-2L-EGFRI-RECHALLENGE | complete_response | uncited | — | ~0% |
| IND-CRC-METASTATIC-2L-EGFRI-RECHALLENGE | overall_response_rate | uncited | — | ~30% (CHRONOS panitumumab rechallenge in ctDNA RAS-WT subgroup) |
| IND-CRC-METASTATIC-2L-EGFRI-RECHALLENGE | overall_survival_5y | uncited | — | OS data immature; signal favors rechallenge in ctDNA RAS-WT selected patients |
| IND-CRC-METASTATIC-2L-EGFRI-RECHALLENGE | progression_free_survival | uncited | — | Median PFS 4.0 mo (CHRONOS); CITRIC: numerically improved but not statistically significant |
| IND-CRC-METASTATIC-2L-FOLFIRI-BEV | overall_response_rate | uncited | — | ~20-30% (FOLFIRI ± targeted) |
| IND-CRC-METASTATIC-2L-FOLFIRI-BEV | overall_survival_5y | uncited | — | Median OS 11.2 mo (FOLFIRI+bev) vs 9.8 mo (FOLFIRI alone, HR 0.81) |
| IND-CRC-METASTATIC-2L-FOLFIRI-BEV | progression_free_survival | uncited | — | Median PFS ~5.7 mo (FOLFIRI+bev, TML/ML18147 trial) |
| IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD | complete_response | uncited | — | ~0% |
| IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD | overall_response_rate | cited | trial-number resolved: DESTINY-CRC01 | ~45% (DESTINY-CRC01 cohort A, HER2 IHC 3+ or IHC 2+/ISH+) |
| IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD | overall_survival_5y | cited | trial-number resolved: DESTINY-CRC01 | Median OS 15.5 mo (DESTINY-CRC01 cohort A) |
| IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD | progression_free_survival | cited | trial-number resolved: DESTINY-CRC01 | Median PFS 6.9 mo (DESTINY-CRC01 cohort A) |
| IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB | complete_response | uncited | — | ~3% |
| IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB | overall_response_rate | probably-cited | trial-number unresolved: MOUNTAINEER | ~38% (MOUNTAINEER tucatinib + trastuzumab cohort, RAS-WT HER2+ chemo-refractory mCRC) |
| IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB | overall_survival_5y | probably-cited | trial-number unresolved: MOUNTAINEER | Median OS 24.1 mo (MOUNTAINEER); long-term f/u pending |
| IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB | progression_free_survival | probably-cited | trial-number unresolved: MOUNTAINEER | Median PFS 8.2 mo (MOUNTAINEER) |
| IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-CETUXIMAB | complete_response | uncited | — | ~0% |
| IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-CETUXIMAB | overall_response_rate | probably-cited | trial-family: CodeBreaK | ~26% (CodeBreaK 300, sotorasib 960 mg + cetuximab arm) |
| IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-CETUXIMAB | overall_survival_5y | uncited | — | OS data immature; trend favors combination; 1-year OS estimate ~50% |
| IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-CETUXIMAB | progression_free_survival | uncited | — | Median PFS 5.6 mo (vs 2.2 mo investigator-choice chemo, HR 0.49) |
| IND-CRC-METASTATIC-2L-MSI-H-PEMBRO | complete_response | uncited | — | ~6% |
| IND-CRC-METASTATIC-2L-MSI-H-PEMBRO | overall_response_rate | cited | trial-number resolved: KEYNOTE-164 | ~33% (KEYNOTE-164 cohort A, 2L+ MSI-H mCRC) |
| IND-CRC-METASTATIC-2L-MSI-H-PEMBRO | overall_survival_5y | cited | trial-number resolved: KEYNOTE-164 | Median OS 31.4 mo cohort A; 5-yr OS estimate ~30% (KEYNOTE-164 pooled) |
| IND-CRC-METASTATIC-2L-MSI-H-PEMBRO | progression_free_survival | uncited | — | Median PFS 4.1 mo cohort A; 24-mo PFS rate ~33% (sustained plateau) |
| IND-CRC-METASTATIC-3L-RECHALLENGE-EGFRI | complete_response | uncited | — | rare |
| IND-CRC-METASTATIC-3L-RECHALLENGE-EGFRI | overall_response_rate | uncited | — | ~30% for ctDNA-selected rechallenge (CHRONOS Sartore-Bianchi 2022 Nat Med) |
| IND-CRC-METASTATIC-3L-RECHALLENGE-EGFRI | overall_survival_5y | uncited | — | Median OS ~17 mo (CRICKET, ctDNA-positive subset has substantially worse OS) |
| IND-CRC-METASTATIC-3L-RECHALLENGE-EGFRI | progression_free_survival | uncited | — | Median PFS ~3.6 mo (CHRONOS); CRICKET 4.0 mo |
| IND-CRC-METASTATIC-3L-REGORAFENIB | overall_response_rate | uncited | — | ~1% (CORRECT; biologic effect more on disease stabilization) |
| IND-CRC-METASTATIC-3L-REGORAFENIB | overall_survival_5y | uncited | — | Median OS 6.4 mo (vs 5.0 mo placebo, HR 0.77); 1-year OS ~24% |
| IND-CRC-METASTATIC-3L-REGORAFENIB | progression_free_survival | uncited | — | Median PFS 1.9 mo (CORRECT; HR 0.49) |
| IND-CRC-METASTATIC-3L-TAS102-BEV | overall_response_rate | uncited | — | ~6.3% (SUNLIGHT TAS-102+bev vs 1.0% TAS-102 alone) |
| IND-CRC-METASTATIC-3L-TAS102-BEV | overall_survival_5y | uncited | — | Median OS 10.8 mo (vs 7.5 mo, HR 0.61); 1-year OS ~43% |
| IND-CRC-METASTATIC-3L-TAS102-BEV | progression_free_survival | uncited | — | Median PFS 5.6 mo (vs 2.4 mo TAS-102 alone, HR 0.44) |
| IND-CRC-METASTATIC-3L-TRIFLURIDINE-TIPIRACIL-MONO | overall_response_rate | uncited | — | ~1.6% (RECOURSE TAS-102 monotherapy; mainly disease stabilization) |
| IND-CRC-METASTATIC-3L-TRIFLURIDINE-TIPIRACIL-MONO | overall_survival_5y | uncited | — | Median OS 7.1 mo (vs 5.3 mo placebo, HR 0.68); 1-year OS ~27% |
| IND-CRC-METASTATIC-3L-TRIFLURIDINE-TIPIRACIL-MONO | progression_free_survival | uncited | — | Median PFS 2.0 mo (RECOURSE; HR 0.48) |
| IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV | complete_response | uncited | — | N/A (maintenance phase) |
| IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV | overall_response_rate | uncited | — | Maintenance — measured by PFS/duration of disease control |
| IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV | overall_survival_5y | uncited | — | OS benefit modest (~1-2 mo); main rationale is QoL via oxaliplatin neuropathy avoidance |
| IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV | progression_free_survival | uncited | — | Median PFS extension ~3-4 mo vs full-stop after induction (CAIRO3, AIO 0207, PRODIGE 9 meta-analysis) |
| IND-CRC-PERFORMANCE-STATUS-3 | complete_response | uncited | — | rare |
| IND-CRC-PERFORMANCE-STATUS-3 | overall_response_rate | uncited | — | ~10-15% capecitabine monotherapy palliative (extrapolated from elderly/frail cohorts) |
| IND-CRC-PERFORMANCE-STATUS-3 | overall_survival_5y | uncited | — | Median OS 4-8 mo from initiation; competing comorbidity dominates |
| IND-CRC-PERFORMANCE-STATUS-3 | progression_free_survival | uncited | — | Median PFS 3-4 mo |
| IND-CRC-RENAL-FAILURE-MOD-FOLFOX | complete_response | uncited | — | rare |
| IND-CRC-RENAL-FAILURE-MOD-FOLFOX | overall_response_rate | uncited | — | ~30% modified 5FU/LV ± bevacizumab (extrapolated from non-renal cohorts) |
| IND-CRC-RENAL-FAILURE-MOD-FOLFOX | overall_survival_5y | uncited | — | Median OS 12-18 mo (modified regimen extrapolation) |
| IND-CRC-RENAL-FAILURE-MOD-FOLFOX | progression_free_survival | uncited | — | Median PFS 6-8 mo (5FU/LV + bev; modified) |

### `DIS-AML` — Acute Myeloid Leukemia (non-APL)

Indications: 15; populated: 60; cited: 4; probably-cited: 1; uncited: 55; absent: 15.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-AML-1L-7-3 | complete_response | uncited | — | ~70% in ELN favorable; ~60% intermediate; ~30-40% adverse |
| IND-AML-1L-7-3 | overall_response_rate | uncited | — | ~60-80% complete remission post-induction (favorable to intermediate-risk young fit) |
| IND-AML-1L-7-3 | overall_survival_5y | uncited | — | ~60-70% favorable-risk young fit; ~30-40% intermediate; <20% adverse without alloHCT |
| IND-AML-1L-7-3 | progression_free_survival | uncited | — | Median ~18 months for intermediate-risk; >5 years if alloHCT in CR1 for adverse-risk fit patients |
| IND-AML-1L-7-3-GO-CBF | complete_response | uncited | — | ~70-80% in CBF/favorable subset |
| IND-AML-1L-7-3-GO-CBF | overall_response_rate | uncited | — | ~80-90% CR/CRi in CBF/favorable; ~70% in intermediate (vs ~70-80%/60% with 7+3 alone) |
| IND-AML-1L-7-3-GO-CBF | overall_survival_5y | uncited | — | 2-yr OS 53.2% vs 41.9% (ALFA-0701, HR 0.69); 5-yr OS reduced mortality by ~20% in favorable + intermediate per Hills ... |
| IND-AML-1L-7-3-GO-CBF | progression_free_survival | uncited | — | 2-yr EFS 40.8% vs 17.1% (ALFA-0701 overall); CBF subset particularly favorable |
| IND-AML-1L-CPX351-SECONDARY | complete_response | uncited | — | ~38% CR (vs 26% 7+3) |
| IND-AML-1L-CPX351-SECONDARY | overall_response_rate | uncited | — | ~47.7% CR/CRi (vs 33.3% with 7+3) per Lancet et al. 2018 |
| IND-AML-1L-CPX351-SECONDARY | overall_survival_5y | uncited | — | 5-y OS 18% vs 8%; median OS 9.56 vs 5.95 mo (HR 0.69) |
| IND-AML-1L-CPX351-SECONDARY | progression_free_survival | uncited | — | Median EFS 2.5 vs 1.3 mo; PFS benefit dominant in alloHCT-bridge subset |
| IND-AML-1L-QUIZARTINIB-FLT3ITD | complete_response | uncited | — | ~54.9% CR (quizartinib arm) vs 55.4% (placebo) |
| IND-AML-1L-QUIZARTINIB-FLT3ITD | overall_response_rate | uncited | — | ~71.6% CR/CRi (similar between arms; quizartinib effect is on durability + post-CR depth) |
| IND-AML-1L-QUIZARTINIB-FLT3ITD | overall_survival_5y | uncited | — | Median OS 31.9 vs 15.1 mo (HR 0.78); 4-y OS ~39% vs ~30% |
| IND-AML-1L-QUIZARTINIB-FLT3ITD | progression_free_survival | uncited | — | EFS HR 0.916 (similar); benefit emerges in maintenance phase |
| IND-AML-1L-VEN-AZA | complete_response | cited | trial-number resolved: VIALE-A | ~37% CR (VIALE-A) |
| IND-AML-1L-VEN-AZA | overall_response_rate | cited | trial-number resolved: VIALE-A | ~60-70% composite CR + CRi (VIALE-A: 66.4% vs 28.3% with aza alone) |
| IND-AML-1L-VEN-AZA | overall_survival_5y | uncited | — | <10% (cumulative; ~25-30% achieve durable remission lasting 1-3 years) |
| IND-AML-1L-VEN-AZA | progression_free_survival | cited | trial-number resolved: VIALE-A | Median ~14.7 months OS (VIALE-A; vs 9.6 mo aza alone) |
| IND-AML-2L-GILTERITINIB-FLT3 | complete_response | uncited | — | ~21% CR/CRh |
| IND-AML-2L-GILTERITINIB-FLT3 | overall_response_rate | uncited | — | ~21% CR/CRh, ~54% composite CR (ADMIRAL) |
| IND-AML-2L-GILTERITINIB-FLT3 | overall_survival_5y | uncited | — | Median OS 9.3 mo overall (ADMIRAL); ~25-30% 2-y OS for those bridged to alloHCT |
| IND-AML-2L-GILTERITINIB-FLT3 | progression_free_survival | uncited | — | Median EFS 2.8 mo (ADMIRAL); responders bridged to alloHCT have substantially longer PFS |
| IND-AML-2L-IDH2-ENASIDENIB | complete_response | uncited | — | ~19% CR; ~7% CRi/CRp |
| IND-AML-2L-IDH2-ENASIDENIB | overall_response_rate | uncited | — | ~38% ORR (AG221-AML-001 phase 1/2) |
| IND-AML-2L-IDH2-ENASIDENIB | overall_survival_5y | uncited | — | Median OS 9.3 mo (AG221-AML-001); ~25-30% 2-y OS for those bridged to alloHCT. IDHENTIFY phase-3 did not show OS bene... |
| IND-AML-2L-IDH2-ENASIDENIB | progression_free_survival | uncited | — | Median DOR ~5.6 mo overall; longer in patients bridged to alloHCT |
| IND-AML-2L-KMT2A-REVUMENIB | complete_response | uncited | — | ~23% CR/CRh |
| IND-AML-2L-KMT2A-REVUMENIB | overall_response_rate | probably-cited | trial-number unresolved: AUGMENT | ~63% ORR; ~23% CR/CRh in KMT2A-r AML cohort (AUGMENT-101) |
| IND-AML-2L-KMT2A-REVUMENIB | overall_survival_5y | uncited | — | Insufficient mature data (FDA approval Nov 2024); responders bridged to alloHCT trending favorable |
| IND-AML-2L-KMT2A-REVUMENIB | progression_free_survival | uncited | — | Median DOR ~6 mo overall; longer in patients bridged to alloHCT |
| IND-AML-CR1-ORAL-AZA-MAINTENANCE | complete_response | cited | trial-number resolved: QUAZAR | MRD-negativity conversion in subset (QUAZAR exploratory analysis) |
| IND-AML-CR1-ORAL-AZA-MAINTENANCE | overall_response_rate | uncited | — | Maintenance setting — measured by RFS/OS, not response |
| IND-AML-CR1-ORAL-AZA-MAINTENANCE | overall_survival_5y | uncited | — | Median OS 24.7 mo vs 14.8 mo placebo (HR 0.69, p<0.001) |
| IND-AML-CR1-ORAL-AZA-MAINTENANCE | progression_free_survival | uncited | — | Median RFS 10.2 mo vs 4.8 mo placebo (HR 0.65, p<0.001) |
| IND-AML-PEDIATRIC-AAML1031 | complete_response | uncited | — | ~75-80% |
| IND-AML-PEDIATRIC-AAML1031 | overall_response_rate | uncited | — | ~85% (CR after 2 cycles induction; AAML1031 Aplenc 2020 JCO) |
| IND-AML-PEDIATRIC-AAML1031 | overall_survival_5y | uncited | — | 5-yr OS ~65-70% overall; substantially better than adult AML due to better tolerance + biology |
| IND-AML-PEDIATRIC-AAML1031 | progression_free_survival | uncited | — | 5-yr EFS ~50-55% overall; high-risk ~30%, low-risk ~70% |
| IND-AML-RR-IDH1-OLUTASIDENIB | complete_response | uncited | — | ~35% CR + CRh; CR alone ~32% |
| IND-AML-RR-IDH1-OLUTASIDENIB | overall_response_rate | uncited | — | ~48% ORR (Study 2102-HEM-101 R/R AML cohort, n=153) |
| IND-AML-RR-IDH1-OLUTASIDENIB | overall_survival_5y | uncited | — | Median OS ~11.6 months overall; longer in CR + CRh responders bridged to alloHCT. 56-day mortality 8%. |
| IND-AML-RR-IDH1-OLUTASIDENIB | progression_free_survival | uncited | — | Median DoR among CR + CRh responders ~25.9 months; median time to first CR + CRh ~1.9 months |
| IND-EMERG-CINV-HIGH-EMETOGENIC | complete_response | uncited | — | N/A (prevention indication) |
| IND-EMERG-CINV-HIGH-EMETOGENIC | overall_response_rate | uncited | — | ~80-90% complete CINV control (no vomiting + no rescue) with 4-drug regimen (NK1 + 5HT3 + dex + olanzapine) |
| IND-EMERG-CINV-HIGH-EMETOGENIC | overall_survival_5y | uncited | — | Inadequate CINV control causes ~10-15% chemo dose reduction / delay / discontinuation — indirectly affects DFS / OS |
| IND-EMERG-CINV-HIGH-EMETOGENIC | progression_free_survival | uncited | — | N/A |
| IND-EMERG-FEBRILE-NEUTROPENIA-EMPIRICAL | complete_response | uncited | — | N/A (treatment of acute condition) |
| IND-EMERG-FEBRILE-NEUTROPENIA-EMPIRICAL | overall_response_rate | uncited | — | ~70-85% defervesce within 72h with empirical regimen |
| IND-EMERG-FEBRILE-NEUTROPENIA-EMPIRICAL | overall_survival_5y | uncited | — | FN mortality without antibiotics ~50%; with proper empirical management <10%; antibiotic delay >60 min increases mort... |
| IND-EMERG-FEBRILE-NEUTROPENIA-EMPIRICAL | progression_free_survival | uncited | — | N/A |
| IND-EMERG-NEUTROPENIC-FEVER-PROPHYLAXIS | complete_response | uncited | — | N/A (prevention) |
| IND-EMERG-NEUTROPENIC-FEVER-PROPHYLAXIS | overall_response_rate | uncited | — | G-CSF primary prophylaxis reduces FN incidence by ~50% (NNT ~10-12) in high-FN-risk regimens |
| IND-EMERG-NEUTROPENIC-FEVER-PROPHYLAXIS | overall_survival_5y | uncited | — | G-CSF + antibacterial prophylaxis reduces all-cause mortality during cytotoxic phase by ~3-7% absolute; preserves dos... |
| IND-EMERG-NEUTROPENIC-FEVER-PROPHYLAXIS | progression_free_survival | uncited | — | N/A |
| IND-EMERG-TLS-PROPHYLAXIS-RASBURICASE | complete_response | uncited | — | N/A (prevention, not response) |
| IND-EMERG-TLS-PROPHYLAXIS-RASBURICASE | overall_response_rate | uncited | — | ~90% achieve normalization of uric acid within 24h with rasburicase |
| IND-EMERG-TLS-PROPHYLAXIS-RASBURICASE | overall_survival_5y | uncited | — | TLS-related mortality reduced from ~17% (allopurinol-only era, high-risk) to <2% with rasburicase + IV hydration (Cor... |
| IND-EMERG-TLS-PROPHYLAXIS-RASBURICASE | progression_free_survival | uncited | — | N/A (prevention indication) |

## Plan implications — Phase 3 prioritization

The plan (`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md` Phase 3) sequences Phase-3 chunks as:

1. **8 shelf-task items first** — KEYNOTE-006/-054, EXTREME, CPX-351, GO, loncastuximab, zanu 1L CLL, CheckMate-577.
2. **High-volume diseases** with uncited outcomes — NSCLC, breast, CRC, prostate, AML, DLBCL.
3. **Other diseases** alphabetical until ≥90% threshold met.

### Audit findings vs plan order

Below: how this audit's measured `uncited` counts re-shuffle that order. Diseases with **higher** uncited counts than the plan implies should move up; diseases already in good shape (high cited %, low uncited count) should drop down.

| Plan-listed high-volume disease | DIS id (best guess) | populated | uncited | cited | outcomes-cited % | suggested action |
|---|---|---:|---:|---:|---:|---|
| NSCLC | `DIS-NSCLC` | 120 | 83 | 33 | 30.8% | prioritize as planned |
| Breast | `DIS-BREAST` | 47 | 22 | 23 | 53.2% | prioritize as planned |
| CRC | `DIS-CRC` | 85 | 72 | 7 | 15.3% | prioritize as planned |
| Prostate | `DIS-PROSTATE` | 35 | 24 | 10 | 31.4% | prioritize as planned |
| AML | `DIS-AML` | 60 | 55 | 4 | 8.3% | prioritize as planned |
| DLBCL | `DIS-DLBCL-NOS` | 48 | 42 | 2 | 12.5% | prioritize as planned |

### Diseases worse than plan assumes (top-10 worst, not in plan list)

These diseases have larger `uncited` backlogs than the plan's named high-volume list and should be promoted into Phase-3 chunk planning earlier than alphabetical order.

| Disease | populated | uncited | cited | outcomes-cited % |
|---|---:|---:|---:|---:|
| `DIS-OVARIAN` — Ovarian carcinoma (high-grade serous predominant) | 48 | 42 | 4 | 12.5% |
| `DIS-MM` — Multiple Myeloma | 52 | 37 | 3 | 28.8% |
| `DIS-MELANOMA` — Cutaneous melanoma | 37 | 28 | 9 | 24.3% |
| `DIS-FL` — Follicular Lymphoma | 27 | 25 | 0 | 7.4% |
| `DIS-PV` — Polycythemia Vera | 24 | 24 | 0 | 0.0% |

### Diseases better than plan assumes (skip / defer)

Diseases with ≥4 populated outcome values and ≥80% loose-cited rate. Phase 3 can deprioritize these — the marginal cost of remediating the residual uncited cells is high relative to other backlog.

| Disease | populated | cited | probably-cited | uncited | outcomes-cited % |
|---|---:|---:|---:|---:|---:|
| `DIS-T-PLL` — T-Cell Prolymphocytic Leukemia | 8 | 8 | 0 | 0 | 100.0% |
| `DIS-HNSCC` — Head and neck squamous cell carcinoma (HNSCC) | 21 | 18 | 0 | 3 | 85.7% |

---

_Generated by `scripts/audit_expected_outcomes.py` on 2026-05-01. Indications audited: 390. Underlying KB tree: `knowledge_base/hosted/content/`._
