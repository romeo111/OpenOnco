# `expected_outcomes` traceability — per-disease appendix (2026-05-01)

Per-indication detail tables for every disease **except** the worst-3 (which are inlined in the main report `expected_outcomes_traceability_2026-05-01.md`).

Rows are limited to populated outcome fields. `absent` rows are summarized in the rollup line at the head of each section, not listed individually.

## `DIS-AITL` — Angioimmunoblastic T-Cell Lymphoma / Nodal TFH-cell lymphoma

Indications: 5; populated: 20; cited: 1; probably-cited: 0; uncited: 19; absent: 5; outcomes-cited % (loose): 5.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-AITL-1L-CHOEP | complete_response | uncited | — | ~45-55% |
| IND-AITL-1L-CHOEP | overall_response_rate | uncited | — | ~70-75% |
| IND-AITL-1L-CHOEP | overall_survival_5y | uncited | — | ~30-40% (worse than B-cell aggressive lymphomas; AITL has dismal prognosis without consolidation) |
| IND-AITL-1L-CHOEP | progression_free_survival | uncited | — | Median PFS ~2-3 years; ~25-35% 5y PFS |
| IND-AITL-1L-CHP-BV | complete_response | uncited | — | ~60-70% |
| IND-AITL-1L-CHP-BV | overall_response_rate | uncited | — | ~80-85% |
| IND-AITL-1L-CHP-BV | overall_survival_5y | uncited | — | ~50-60% (substantial improvement over CHOP-only era for CD30+ AITL) |
| IND-AITL-1L-CHP-BV | progression_free_survival | cited | trial-number resolved: ECHELON-2 | ECHELON-2 AITL subset signal favorable; full subset PFS ~57% 3y in CD30+ T-cell (driven by ALCL) |
| IND-AITL-2L-AZACITIDINE | complete_response | uncited | — | ~30-40% |
| IND-AITL-2L-AZACITIDINE | overall_response_rate | uncited | — | ~50-75% (RUYUAN-2 / Lemonnier 2018-2023; small AITL series) |
| IND-AITL-2L-AZACITIDINE | overall_survival_5y | uncited | — | Mature OS pending; ~50-60% 18-mo OS in responders |
| IND-AITL-2L-AZACITIDINE | progression_free_survival | uncited | — | Median PFS ~6-15 mo (early data, AITL-specific cohorts) |
| IND-AITL-2L-BELINOSTAT | complete_response | uncited | — | ~11% |
| IND-AITL-2L-BELINOSTAT | overall_response_rate | uncited | — | ~26% overall (BELIEF); higher in AITL subset (~46%) |
| IND-AITL-2L-BELINOSTAT | overall_survival_5y | uncited | — | ~25-30% (heavily pretreated cohort baseline poor) |
| IND-AITL-2L-BELINOSTAT | progression_free_survival | uncited | — | Median PFS ~1.6 mo overall; mDOR for responders ~13.6 mo |
| IND-AITL-2L-ROMIDEPSIN | complete_response | uncited | — | ~15% |
| IND-AITL-2L-ROMIDEPSIN | overall_response_rate | uncited | — | ~25-38% (NCI 1312); AITL subset higher (~33%) |
| IND-AITL-2L-ROMIDEPSIN | overall_survival_5y | uncited | — | ~25-30% (heavily pretreated baseline) |
| IND-AITL-2L-ROMIDEPSIN | progression_free_survival | uncited | — | Median PFS ~4 mo; mDOR ~17 mo for responders |

## `DIS-ALCL` — Anaplastic Large Cell Lymphoma (systemic)

Indications: 5; populated: 20; cited: 1; probably-cited: 1; uncited: 18; absent: 5; outcomes-cited % (loose): 10.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ALCL-2L-BENDAMUSTINE | complete_response | uncited | — | ~28% |
| IND-ALCL-2L-BENDAMUSTINE | overall_response_rate | uncited | — | ~50% (BENTLY mixed cohort) |
| IND-ALCL-2L-BENDAMUSTINE | overall_survival_5y | uncited | — | ~25-35% (heavily pretreated baseline poor) |
| IND-ALCL-2L-BENDAMUSTINE | progression_free_survival | uncited | — | Median PFS ~3-4 mo; mDOR ~6 mo for responders |
| IND-ALCL-2L-BRENTUXIMAB-MONO | complete_response | uncited | — | ~57% |
| IND-ALCL-2L-BRENTUXIMAB-MONO | overall_response_rate | uncited | — | ~86% (SGN-35-005) |
| IND-ALCL-2L-BRENTUXIMAB-MONO | overall_survival_5y | uncited | — | ~60% (SGN-35-005 5-year follow-up) |
| IND-ALCL-2L-BRENTUXIMAB-MONO | progression_free_survival | uncited | — | Median PFS ~13.3 mo; mDOR 12.6 mo |
| IND-ALCL-2L-CRIZOTINIB-ALKPOS | complete_response | uncited | — | ~75-80% |
| IND-ALCL-2L-CRIZOTINIB-ALKPOS | overall_response_rate | uncited | — | ~88-90% (NCI-9015) |
| IND-ALCL-2L-CRIZOTINIB-ALKPOS | overall_survival_5y | uncited | — | ~60-70% with continuous therapy + SCT consolidation |
| IND-ALCL-2L-CRIZOTINIB-ALKPOS | progression_free_survival | uncited | — | Median PFS ~24 mo+ (small adult cohorts; longer in pediatric) |
| IND-ALCL-MAINTENANCE-BV-POST-ASCT | complete_response | uncited | — | Sustains pre-existing CR |
| IND-ALCL-MAINTENANCE-BV-POST-ASCT | overall_response_rate | uncited | — | Maintenance setting — CR/PR already achieved at ASCT |
| IND-ALCL-MAINTENANCE-BV-POST-ASCT | overall_survival_5y | uncited | — | Trend toward OS benefit in highest-risk subgroups; ALCL ALK- subset most likely to benefit |
| IND-ALCL-MAINTENANCE-BV-POST-ASCT | progression_free_survival | probably-cited | trial-number unresolved: AETHERA | Extrapolated from AETHERA: 5-yr PFS benefit ~18 percentage points (59% vs 41%) in high-risk cHL post-ASCT; ALCL data ... |
| IND-TCELL-1L-CHP-BV | complete_response | uncited | — | ~70% |
| IND-TCELL-1L-CHP-BV | overall_response_rate | uncited | — | ~85% |
| IND-TCELL-1L-CHP-BV | overall_survival_5y | uncited | — | ~70-85% (varies sharply by ALK status + IPI) |
| IND-TCELL-1L-CHP-BV | progression_free_survival | cited | trial-number resolved: ECHELON-2 | 3-year PFS ~57% (CHP-Bv) vs ~44% (CHOP) in ECHELON-2 — substantial benefit in ALCL ALK- |

## `DIS-ANAL-SCC` — Squamous cell carcinoma of the anal canal

Indications: 3; populated: 10; cited: 0; probably-cited: 0; uncited: 10; absent: 11; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ANAL-SCC-LA-1L-NIGRO-CRT | colostomy_free_survival_3y | uncited | — | ~70% colostomy-free at 3 years |
| IND-ANAL-SCC-LA-1L-NIGRO-CRT | complete_response_rate | uncited | — | ~90% complete response at 26 weeks (ACT II) |
| IND-ANAL-SCC-LA-1L-NIGRO-CRT | overall_survival_5y | uncited | — | ~80-85% 5-year OS for stage II-III with CRT |
| IND-ANAL-SCC-LA-1L-NIGRO-CRT | progression_free_survival | uncited | — | 74% 3-year PFS (ACT II, MMC arm) |
| IND-ANAL-SCC-LA-1L-NIGRO-CRT | salvage_apr_rate | uncited | — | ~10-25% require salvage APR for residual/recurrent disease |
| IND-ANAL-SCC-METASTATIC-1L-CARBO-PACLI | orr | uncited | — | ~20-35% (retrospective series) |
| IND-ANAL-SCC-METASTATIC-1L-CARBO-PACLI | pfs_months | uncited | — | ~5-7 (backbone doublet without ICI) |
| IND-ANAL-SCC-METASTATIC-1L-RETIFANLIMAB-CARBO-PACLI | overall_response_rate | uncited | — | ~57% ORR (retifanlimab+carbo+pacli, POD1UM-303) |
| IND-ANAL-SCC-METASTATIC-1L-RETIFANLIMAB-CARBO-PACLI | overall_survival | uncited | — | Data maturing; 12-month OS ~65% (preliminary) |
| IND-ANAL-SCC-METASTATIC-1L-RETIFANLIMAB-CARBO-PACLI | progression_free_survival | uncited | — | ~9-10 months mPFS vs ~6-7 months with chemotherapy alone (POD1UM-303) |

## `DIS-APL` — Acute Promyelocytic Leukemia (PML-RARA)

Indications: 4; populated: 16; cited: 0; probably-cited: 0; uncited: 16; absent: 4; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-APL-1L-ATRA-ATO | complete_response | uncited | — | ~99% post-induction |
| IND-APL-1L-ATRA-ATO | overall_response_rate | uncited | — | ~99% complete remission (APL0406: ATRA+ATO arm) |
| IND-APL-1L-ATRA-ATO | overall_survival_5y | uncited | — | ~95-99% in low/intermediate-risk treated with ATRA + ATO |
| IND-APL-1L-ATRA-ATO | progression_free_survival | uncited | — | 2-y EFS 97% (APL0406) |
| IND-APL-1L-ATRA-ATO-IDA | complete_response | uncited | — | ~85-90% post-induction |
| IND-APL-1L-ATRA-ATO-IDA | overall_response_rate | uncited | — | ~90-95% complete remission (high-risk APL with intensified regimens) |
| IND-APL-1L-ATRA-ATO-IDA | overall_survival_5y | uncited | — | ~85% high-risk treated with ATRA + ATO + idarubicin |
| IND-APL-1L-ATRA-ATO-IDA | progression_free_survival | uncited | — | 5-y EFS ~80-85% high-risk |
| IND-APL-RELAPSED-GEMTUZUMAB | complete_response | uncited | — | Rapid deep molecular CR in majority |
| IND-APL-RELAPSED-GEMTUZUMAB | overall_response_rate | uncited | — | CR ~91% in MyloFrance series (gemtuzumab + ATO) |
| IND-APL-RELAPSED-GEMTUZUMAB | overall_survival_5y | uncited | — | 5-y OS ~50-70% with autoSCT consolidation; lower without |
| IND-APL-RELAPSED-GEMTUZUMAB | progression_free_survival | uncited | — | Median EFS variable; autoSCT consolidation extends durable remission |
| IND-APL-SALVAGE-ATRA-ATO | complete_response | uncited | — | Molecular CR in 80-90% by end of induction (typically 4-8 weeks) |
| IND-APL-SALVAGE-ATRA-ATO | overall_response_rate | uncited | — | CR ~85-95% (Lengfelder et al., Leukemia 2017 registry) |
| IND-APL-SALVAGE-ATRA-ATO | overall_survival_5y | uncited | — | 5-y OS ~70-80% with autoSCT consolidation; ~50-60% without consolidation; <30% if molecular non-CR |
| IND-APL-SALVAGE-ATRA-ATO | progression_free_survival | uncited | — | 5-y EFS 60-80% with autoSCT consolidation in molecularly-CR responders |

## `DIS-ATLL` — Adult T-Cell Leukemia/Lymphoma

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ATLL-1L-AGGRESSIVE | complete_response | uncited | — | ~40% |
| IND-ATLL-1L-AGGRESSIVE | overall_response_rate | uncited | — | ~60-80% (з mogamulizumab + chemo) |
| IND-ATLL-1L-AGGRESSIVE | overall_survival_5y | uncited | — | ~10% chemo-only; ~30-35% з allo-SCT у CR1 |
| IND-ATLL-1L-AGGRESSIVE | progression_free_survival | uncited | — | Median PFS ~9-12 months chemo-only; ~24 months з allo-SCT |
| IND-ATLL-1L-INDOLENT-AZT-IFN | complete_response | uncited | — | ~30-40% |
| IND-ATLL-1L-INDOLENT-AZT-IFN | overall_response_rate | uncited | — | ~60-70% (indolent forms) |
| IND-ATLL-1L-INDOLENT-AZT-IFN | overall_survival_5y | uncited | — | ~80% smoldering; ~60% chronic |
| IND-ATLL-1L-INDOLENT-AZT-IFN | progression_free_survival | uncited | — | Median PFS ~3-5 years (smoldering); ~2 years (chronic) |
| IND-ATLL-2L-MOGAMULIZUMAB | complete_response | uncited | — | ~30% |
| IND-ATLL-2L-MOGAMULIZUMAB | overall_response_rate | uncited | — | ~50% (Ishida 2012 phase 2; r/r ATLL) |
| IND-ATLL-2L-MOGAMULIZUMAB | overall_survival_5y | uncited | — | <10% chemo-only; ~25-30% if successful bridge to alloSCT in CR |
| IND-ATLL-2L-MOGAMULIZUMAB | progression_free_survival | uncited | — | Median PFS ~5 months without alloSCT consolidation |

## `DIS-B-ALL` — B-Lymphoblastic Leukemia / Lymphoma

Indications: 6; populated: 24; cited: 0; probably-cited: 1; uncited: 23; absent: 6; outcomes-cited % (loose): 4.2%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-B-ALL-1L-PH-NEG | complete_response | uncited | — | ~85% |
| IND-B-ALL-1L-PH-NEG | overall_response_rate | uncited | — | ~90% |
| IND-B-ALL-1L-PH-NEG | overall_survival_5y | uncited | — | ~40-50% adults; ~85% AYA з pediatric-inspired |
| IND-B-ALL-1L-PH-NEG | progression_free_survival | uncited | — | Median PFS ~36 months (з MRD-driven escalation) |
| IND-B-ALL-1L-PH-POS | complete_response | uncited | — | ~95% (post-induction) |
| IND-B-ALL-1L-PH-POS | overall_response_rate | uncited | — | ~95% |
| IND-B-ALL-1L-PH-POS | overall_survival_5y | uncited | — | ~50-60% (highly age-dependent) |
| IND-B-ALL-1L-PH-POS | progression_free_survival | uncited | — | Median PFS ~30 months (з allo-SCT consolidation у CR1) |
| IND-B-ALL-2L-INOTUZUMAB | complete_response | uncited | — | MRD-negativity in CR/CRi 78.4% |
| IND-B-ALL-2L-INOTUZUMAB | overall_response_rate | uncited | — | CR/CRi 80.7% vs 29.4% chemo (INO-VATE) |
| IND-B-ALL-2L-INOTUZUMAB | overall_survival_5y | uncited | — | Median OS 7.7 vs 6.7 mo chemo (HR 0.77); responders bridged to alloHCT have substantially longer survival |
| IND-B-ALL-2L-INOTUZUMAB | progression_free_survival | uncited | — | Median PFS 5.0 vs 1.8 mo chemo (HR 0.45) |
| IND-B-ALL-3L-TISAGENLECLEUCEL | complete_response | uncited | — | CR/CRi 60%; MRD-negativity in CR/CRi 100% |
| IND-B-ALL-3L-TISAGENLECLEUCEL | overall_response_rate | probably-cited | trial-family: ELIANA | ORR 81% (ELIANA) |
| IND-B-ALL-3L-TISAGENLECLEUCEL | overall_survival_5y | uncited | — | 12-month OS 76%; 5-y OS ~40-50% in long-term follow-up subsets |
| IND-B-ALL-3L-TISAGENLECLEUCEL | progression_free_survival | uncited | — | 12-month EFS 50% |
| IND-B-ALL-BLINATUMOMAB-MRD-OR-RR | complete_response | uncited | — | MRD-negativity in CR/CRh ~80% |
| IND-B-ALL-BLINATUMOMAB-MRD-OR-RR | overall_response_rate | uncited | — | MRD+ (BLAST): complete MRD response 78%; R/R Ph- (TOWER): CR/CRh 44% vs 25% chemo |
| IND-B-ALL-BLINATUMOMAB-MRD-OR-RR | overall_survival_5y | uncited | — | TOWER median OS 7.7 vs 4.0 mo chemo (HR 0.71); BLAST 5-y RFS 36% (vs historic ~10% MRD+ continuing chemo) |
| IND-B-ALL-BLINATUMOMAB-MRD-OR-RR | progression_free_survival | uncited | — | TOWER median EFS 7.3 vs 4.6 mo chemo |
| IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE | complete_response | uncited | — | Already in CR at start; maintenance preserves CR + eradicates residual disease |
| IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE | overall_response_rate | uncited | — | Maintenance setting — measured by EFS/OS, not response rate |
| IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE | overall_survival_5y | uncited | — | 3-y OS 73% (CALGB 10403); historical adult-style regimens 30-40% in AYA — pediatric-style maintenance is the dominant... |
| IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE | progression_free_survival | uncited | — | 3-y EFS 59% (CALGB 10403, AYA cohort with full pediatric-inspired regimen) |

## `DIS-BREAST` — Breast cancer (invasive)

Indications: 26; populated: 47; cited: 23; probably-cited: 2; uncited: 22; absent: 112; outcomes-cited % (loose): 53.2%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-BREAST-BRCA-MET-TALAZOPARIB | median_progression_free_survival_months | uncited | — | 9 |
| IND-BREAST-BRCA-POS-MET-PARPI | median_progression_free_survival_months | cited | trial-number resolved: OlympiAD | 7 |
| IND-BREAST-HER2-LOW-2L-DATO-DXD | median_progression_free_survival_months | uncited | — | 7 |
| IND-BREAST-HER2-POS-3L-TUCATINIB | median_overall_survival_months | uncited | — | 22 |
| IND-BREAST-HER2-POS-3L-TUCATINIB | median_progression_free_survival_months | uncited | — | 8 |
| IND-BREAST-HER2-POS-EARLY-NEOADJUVANT | five_year_invasive_disease_free_survival_with_pcr | uncited | — | >90% |
| IND-BREAST-HER2-POS-EARLY-NEOADJUVANT | pathologic_complete_response_rate | uncited | — | 60-65% |
| IND-BREAST-HER2-POS-MAINT-TRAST | complete_response | uncited | — | ~5% |
| IND-BREAST-HER2-POS-MAINT-TRAST | overall_response_rate | cited | trial-number resolved: CLEOPATRA | ~80% during induction phase (CLEOPATRA) |
| IND-BREAST-HER2-POS-MAINT-TRAST | overall_survival_5y | cited | trial-number resolved: CLEOPATRA | 8-yr OS landmark ~37% (CLEOPATRA Swain 2020 ESMO update; mOS 57.1 mo) |
| IND-BREAST-HER2-POS-MAINT-TRAST | progression_free_survival | cited | trial-number resolved: CLEOPATRA | Median PFS 18.7 mo (CLEOPATRA Swain 2015 NEJM final) |
| IND-BREAST-HER2-POS-MET-1L-THP | median_overall_survival_months | cited | trial-number resolved: CLEOPATRA | 57 |
| IND-BREAST-HER2-POS-MET-2L-TDXD | median_progression_free_survival_months | cited | trial-number resolved: DESTINY-Breast03 | 28 |
| IND-BREAST-HR-POS-1L-INAVOLISIB | median_progression_free_survival_months | probably-cited | trial-number unresolved: INAVO120 | 15 |
| IND-BREAST-HR-POS-2L-AKT-CAPIVASERTIB | median_progression_free_survival_months | cited | trial-number resolved: CAPItello-291 | 7 |
| IND-BREAST-HR-POS-2L-DATO-DXD | median_progression_free_survival_months | uncited | — | 7 |
| IND-BREAST-HR-POS-2L-ESR1-ELACESTRANT | median_progression_free_survival_months | probably-cited | trial-family: EMERALD | 4 |
| IND-BREAST-HR-POS-2L-FUL-EVEROLIMUS | median_progression_free_survival_months | uncited | — | 10 |
| IND-BREAST-HR-POS-2L-PIK3CA-ALPELISIB | median_progression_free_survival_months | uncited | — | 11 |
| IND-BREAST-HR-POS-2L-T-DXD-HER2-LOW | median_overall_survival_months | cited | trial-number resolved: DESTINY-Breast04 | 24 |
| IND-BREAST-HR-POS-2L-T-DXD-HER2-LOW | median_progression_free_survival_months | cited | trial-number resolved: DESTINY-Breast04 | 10 |
| IND-BREAST-HR-POS-3L-POST-CDK46I-POST-AKT | complete_response | uncited | — | rare |
| IND-BREAST-HR-POS-3L-POST-CDK46I-POST-AKT | overall_response_rate | uncited | — | ~12% everolimus + exemestane post-AI/CDK4/6i (BOLERO-2 indirect; 3L+ data limited) |
| IND-BREAST-HR-POS-3L-POST-CDK46I-POST-AKT | overall_survival_5y | uncited | — | Limited; salvage setting; mOS ~12-18 mo |
| IND-BREAST-HR-POS-3L-POST-CDK46I-POST-AKT | progression_free_survival | uncited | — | Median PFS 4-6 mo (cross-trial; BOLERO-2 mPFS 7.8 mo in 2L; less in 3L+) |
| IND-BREAST-HR-POS-MAINT-CDK46I | complete_response | uncited | — | ~5% |
| IND-BREAST-HR-POS-MAINT-CDK46I | overall_response_rate | cited | trial-number resolved: MONALEESA-2 | ~55% during initial response phase (PALOMA-2 / MONALEESA-2) |
| IND-BREAST-HR-POS-MAINT-CDK46I | overall_survival_5y | cited | trial-number resolved: MONALEESA-2 | OS benefit confirmed for ribociclib (MONALEESA-2 OS HR 0.76) + abemaciclib; palbociclib OS benefit not statistically ... |
| IND-BREAST-HR-POS-MAINT-CDK46I | progression_free_survival | cited | trial-number resolved: MONALEESA-2 | Median PFS 27.6 mo palbo+letro (PALOMA-2 Finn 2016/Rugo 2019), 25.3 mo ribo+letro (MONALEESA-2) |
| IND-BREAST-HR-POS-MET-1L-CDKI | median_overall_survival_months | cited | trial-number resolved: MONALEESA-2 | 63 |
| IND-BREAST-HR-POS-MET-1L-CDKI | median_progression_free_survival_months | cited | trial-number resolved: MONALEESA-2 | 25 |
| IND-BREAST-TNBC-2L-BRCA-OLAPARIB | median_progression_free_survival_months | cited | trial-number resolved: OlympiAD | 7 |
| IND-BREAST-TNBC-2L-BRCA-TALAZOPARIB | median_progression_free_survival_months | uncited | — | 9 |
| IND-BREAST-TNBC-2L-DATO-DXD | median_progression_free_survival_months | cited | trial-number resolved: ASCENT | 6 |
| IND-BREAST-TNBC-2L-SACITUZUMAB | median_overall_survival_months | cited | trial-number resolved: ASCENT | 12 |
| IND-BREAST-TNBC-2L-SACITUZUMAB | median_progression_free_survival_months | cited | trial-number resolved: ASCENT | 6 |
| IND-BREAST-TNBC-2L-T-DXD-HER2-LOW | median_overall_survival_months | cited | trial-number resolved: DESTINY-Breast04 | 18 |
| IND-BREAST-TNBC-2L-T-DXD-HER2-LOW | median_progression_free_survival_months | cited | trial-number resolved: DESTINY-Breast04 | 8 |
| IND-BREAST-TNBC-3L-POST-SACI-POST-T-DXD | complete_response | uncited | — | rare |
| IND-BREAST-TNBC-3L-POST-SACI-POST-T-DXD | overall_response_rate | uncited | — | ~10-20% sequential single-agent chemo (capecitabine, eribulin, vinorelbine, gemcitabine) |
| IND-BREAST-TNBC-3L-POST-SACI-POST-T-DXD | overall_survival_5y | uncited | — | Salvage setting; mOS 6-12 mo from 3L initiation |
| IND-BREAST-TNBC-3L-POST-SACI-POST-T-DXD | progression_free_survival | uncited | — | Median PFS 2-4 mo per single-agent (cross-trial) |
| IND-BREAST-TNBC-EARLY-NEOADJUVANT | pathologic_complete_response_rate | cited | trial-number resolved: KEYNOTE-522 | 65% |
| IND-BREAST-TNBC-EARLY-NEOADJUVANT | three_year_event_free_survival | cited | trial-number resolved: KEYNOTE-522 | 85% |
| IND-BREAST-TNBC-METASTATIC-1L-PEMBRO-CHEMO | overall_response_rate | cited | trial-number resolved: KEYNOTE-355 | ~53.2% vs 39.8% (CPS ≥10 subgroup; KEYNOTE-355) |
| IND-BREAST-TNBC-METASTATIC-1L-PEMBRO-CHEMO | overall_survival | uncited | — | ~23.0 vs 16.1 months (HR 0.73 for CPS ≥10; Cortes NEJM 2022) |
| IND-BREAST-TNBC-METASTATIC-1L-PEMBRO-CHEMO | progression_free_survival | uncited | — | ~9.7 vs 5.6 months (HR 0.65 for CPS ≥10) |

## `DIS-BURKITT` — Burkitt Lymphoma

Indications: 5; populated: 20; cited: 0; probably-cited: 0; uncited: 20; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-BURKITT-1L-CODOXM-IVAC | complete_response | uncited | — | ~80-85% |
| IND-BURKITT-1L-CODOXM-IVAC | overall_response_rate | uncited | — | ~92% |
| IND-BURKITT-1L-CODOXM-IVAC | overall_survival_5y | uncited | — | ~75-85% |
| IND-BURKITT-1L-CODOXM-IVAC | progression_free_survival | uncited | — | Median PFS ~5 years for fit younger high-risk |
| IND-BURKITT-1L-DAEPOCHR | complete_response | uncited | — | ~85-90% |
| IND-BURKITT-1L-DAEPOCHR | overall_response_rate | uncited | — | ~95% |
| IND-BURKITT-1L-DAEPOCHR | overall_survival_5y | uncited | — | ~85-90% |
| IND-BURKITT-1L-DAEPOCHR | progression_free_survival | uncited | — | 4-year PFS ~85% (CALGB 10002 — adult Burkitt including HIV+) |
| IND-BURKITT-1L-HYPERCVAD-R | complete_response | uncited | — | ~80-90% |
| IND-BURKITT-1L-HYPERCVAD-R | overall_response_rate | uncited | — | ~90-95% |
| IND-BURKITT-1L-HYPERCVAD-R | overall_survival_5y | uncited | — | ~70-80% in fit younger high-risk; substantially worse age >60 |
| IND-BURKITT-1L-HYPERCVAD-R | progression_free_survival | uncited | — | 3y PFS ~70-80% in fit younger high-risk per Thomas 2010 |
| IND-BURKITT-2L-RDHAP-ASCT | complete_response | uncited | — | ~30-40% to R-DHAP alone; CR2 candidates proceed to ASCT |
| IND-BURKITT-2L-RDHAP-ASCT | overall_response_rate | uncited | — | ~50-60% (extrapolated from r/r aggressive B-NHL salvage; CORAL-style) |
| IND-BURKITT-2L-RDHAP-ASCT | overall_survival_5y | uncited | — | ~30-40% (heavily pretreated baseline poor) |
| IND-BURKITT-2L-RDHAP-ASCT | progression_free_survival | uncited | — | 3y PFS ~30-40% in fit younger r/r Burkitt with R-DHAP → ASCT in CR2 |
| IND-BURKITT-2L-RICE-ASCT | complete_response | uncited | — | ~30-40% to R-ICE alone; CR2 candidates proceed to ASCT |
| IND-BURKITT-2L-RICE-ASCT | overall_response_rate | uncited | — | ~50-60% (extrapolated from r/r aggressive B-NHL salvage; Burkitt-specific data limited) |
| IND-BURKITT-2L-RICE-ASCT | overall_survival_5y | uncited | — | ~30-40% (heavily pretreated baseline poor; primary-refractory worse) |
| IND-BURKITT-2L-RICE-ASCT | progression_free_survival | uncited | — | 3y PFS ~30-40% in fit younger r/r Burkitt with R-ICE → ASCT in CR2 |

## `DIS-CERVICAL` — Cervical carcinoma (squamous predominant + adeno)

Indications: 3; populated: 12; cited: 3; probably-cited: 0; uncited: 9; absent: 3; outcomes-cited % (loose): 25.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CERVICAL-2L-TISOTUMAB-VEDOTIN | complete_response | uncited | — | ~7% (innovaTV 204) |
| IND-CERVICAL-2L-TISOTUMAB-VEDOTIN | overall_response_rate | uncited | — | ~24% (innovaTV 204, Coleman 2021); 17.8% vs 5.2% chemo (innovaTV 301, Vergote 2024) |
| IND-CERVICAL-2L-TISOTUMAB-VEDOTIN | overall_survival_5y | uncited | — | Median OS 12.1 mo (innovaTV 204); 11.5 vs 9.5 mo (innovaTV 301, HR 0.70, p=0.0038) |
| IND-CERVICAL-2L-TISOTUMAB-VEDOTIN | progression_free_survival | uncited | — | Median PFS 4.2 mo (innovaTV 204); 4.2 vs 2.9 mo (innovaTV 301, HR 0.67) |
| IND-CERVICAL-LOCALLY-ADVANCED-CRT | complete_response | uncited | — | ~60-70% local control |
| IND-CERVICAL-LOCALLY-ADVANCED-CRT | overall_response_rate | uncited | — | ~80% complete clinical response post-CRT |
| IND-CERVICAL-LOCALLY-ADVANCED-CRT | overall_survival_5y | uncited | — | 5-yr OS ~55-65% locally advanced (depends on FIGO stage + nodal status) |
| IND-CERVICAL-LOCALLY-ADVANCED-CRT | progression_free_survival | uncited | — | 5-yr DFS ~65-70% IB3-IIB; ~40-50% IIIB |
| IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV | complete_response | uncited | — | ~23% |
| IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV | overall_response_rate | cited | trial-number resolved: KEYNOTE-826 | ~68% (KEYNOTE-826 PD-L1 CPS ≥1, pembro+chemo arm) |
| IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV | overall_survival_5y | cited | trial-number resolved: KEYNOTE-826 | Median OS 28.6 mo vs 16.5 mo (HR 0.64 in CPS ≥1, KEYNOTE-826 final analysis) |
| IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV | progression_free_survival | cited | trial-number resolved: KEYNOTE-826 | Median PFS 10.4 mo (pembro+chemo vs 8.2 mo placebo+chemo, HR 0.62 in CPS ≥1, KEYNOTE-826) |

## `DIS-CHL` — Classical Hodgkin Lymphoma

Indications: 7; populated: 28; cited: 2; probably-cited: 5; uncited: 21; absent: 7; outcomes-cited % (loose): 25.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CHL-1L-A-AVD | complete_response | uncited | — | ~85% |
| IND-CHL-1L-A-AVD | overall_response_rate | uncited | — | ~96% |
| IND-CHL-1L-A-AVD | overall_survival_5y | cited | trial-number resolved: ECHELON-1 | ~93% (ECHELON-1 OS HR 0.59 vs ABVD) |
| IND-CHL-1L-A-AVD | progression_free_survival | cited | trial-number resolved: ECHELON-1 | 6y PFS ~83% (ECHELON-1 advanced cHL) |
| IND-CHL-1L-ABVD | complete_response | uncited | — | ~80-85% |
| IND-CHL-1L-ABVD | overall_response_rate | uncited | — | ~95% |
| IND-CHL-1L-ABVD | overall_survival_5y | uncited | — | ~85-90% advanced, ~95% early-stage |
| IND-CHL-1L-ABVD | progression_free_survival | uncited | — | 5y PFS ~80% advanced, ~90% early-stage |
| IND-CHL-1L-N-AVD | complete_response | uncited | — | ~85% |
| IND-CHL-1L-N-AVD | overall_response_rate | uncited | — | ~94% (SWOG S1826) |
| IND-CHL-1L-N-AVD | overall_survival_5y | uncited | — | Mature OS data still maturing; 2-year OS ~99% (S1826) |
| IND-CHL-1L-N-AVD | progression_free_survival | uncited | — | 2y PFS 92% (SWOG S1826) — superior to A+AVD 83% (HR 0.48) |
| IND-CHL-2L-BRENTUXIMAB-MAINTENANCE | complete_response | uncited | — | Already in CR/PR post-ASCT |
| IND-CHL-2L-BRENTUXIMAB-MAINTENANCE | overall_response_rate | uncited | — | Maintenance setting (post-ASCT remission) — measured by PFS/OS, not response rate |
| IND-CHL-2L-BRENTUXIMAB-MAINTENANCE | overall_survival_5y | probably-cited | trial-number unresolved: AETHERA | ~80% (5-year OS not significantly different in primary AETHERA analysis) |
| IND-CHL-2L-BRENTUXIMAB-MAINTENANCE | progression_free_survival | probably-cited | trial-number unresolved: AETHERA | 5y PFS 59% (BV maintenance) vs 41% placebo (AETHERA, HR 0.52) |
| IND-CHL-2L-PEMBROLIZUMAB | complete_response | uncited | — | ~24.5% |
| IND-CHL-2L-PEMBROLIZUMAB | overall_response_rate | probably-cited | trial-number unresolved: KEYNOTE-204 | ~66% (KEYNOTE-204) |
| IND-CHL-2L-PEMBROLIZUMAB | overall_survival_5y | probably-cited | trial-number unresolved: KEYNOTE-087 | ~75-80% (KEYNOTE-087 long-term follow-up) |
| IND-CHL-2L-PEMBROLIZUMAB | progression_free_survival | probably-cited | trial-number unresolved: KEYNOTE-204 | Median PFS ~13.2 mo (KEYNOTE-204; superior to BV 8.3 mo, HR 0.65) |
| IND-CHL-CHILD-PUGH-C-MOD | complete_response | uncited | — | ~55% |
| IND-CHL-CHILD-PUGH-C-MOD | overall_response_rate | uncited | — | ~70% (extrapolated; modified regimen in severe hepatic impairment lacks RCT data) |
| IND-CHL-CHILD-PUGH-C-MOD | overall_survival_5y | uncited | — | 5-yr OS ~65% (modified regimen extrapolation; competing risks dominate) |
| IND-CHL-CHILD-PUGH-C-MOD | progression_free_survival | uncited | — | 5-yr PFS ~60% (lower than non-hepatic due to hold of bleomycin / DTIC + competing hepatic mortality) |
| IND-CHL-PREGNANCY-MOD-ABVD | complete_response | uncited | — | ~70% |
| IND-CHL-PREGNANCY-MOD-ABVD | overall_response_rate | uncited | — | ~85% (extrapolated from non-pregnant ABVD) |
| IND-CHL-PREGNANCY-MOD-ABVD | overall_survival_5y | uncited | — | 5-yr OS ~85% (extrapolated; pregnancy registry data limited) |
| IND-CHL-PREGNANCY-MOD-ABVD | progression_free_survival | uncited | — | 5-yr PFS ~75% (extrapolated) |

## `DIS-CHOLANGIOCARCINOMA` — Cholangiocarcinoma (bile duct cancer)

Indications: 4; populated: 11; cited: 0; probably-cited: 0; uncited: 11; absent: 9; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CHOLANGIO-2L-FGFR2-FUSION-PEMIGATINIB | complete_response | uncited | — | ~3% |
| IND-CHOLANGIO-2L-FGFR2-FUSION-PEMIGATINIB | overall_response_rate | uncited | — | ~35.5% (FIGHT-202 cohort A FGFR2 fusion / rearrangement) |
| IND-CHOLANGIO-2L-FGFR2-FUSION-PEMIGATINIB | overall_survival_5y | uncited | — | Median OS 21.1 mo (FIGHT-202); long-term f/u pending |
| IND-CHOLANGIO-2L-FGFR2-FUSION-PEMIGATINIB | progression_free_survival | uncited | — | Median PFS 6.9 mo (FIGHT-202) |
| IND-CHOLANGIO-2L-FUTIBATINIB | complete_response | uncited | — | ~1% |
| IND-CHOLANGIO-2L-FUTIBATINIB | overall_response_rate | uncited | — | ~41.7% (FOENIX-CCA2; 43/103 confirmed responders) |
| IND-CHOLANGIO-2L-FUTIBATINIB | overall_survival_5y | uncited | — | Median OS 21.7 mo (FOENIX-CCA2; long-term f/u) |
| IND-CHOLANGIO-2L-FUTIBATINIB | progression_free_survival | uncited | — | Median PFS 9.0 mo (FOENIX-CCA2) |
| IND-CHOLANGIO-2L-INFIGRATINIB | overall_response_rate | uncited | — | ~23.1% (CBGJ398X2204 cohort; 25/108 confirmed responders) |
| IND-CHOLANGIO-2L-INFIGRATINIB | overall_survival_5y | uncited | — | Median OS 12.2 mo (CBGJ398X2204) |
| IND-CHOLANGIO-2L-INFIGRATINIB | progression_free_survival | uncited | — | Median PFS 7.3 mo (CBGJ398X2204) |

## `DIS-CHONDROSARCOMA` — Chondrosarcoma

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-CLL` — Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma

Indications: 7; populated: 28; cited: 0; probably-cited: 8; uncited: 20; absent: 7; outcomes-cited % (loose): 28.6%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CLL-1L-BTKI | complete_response | uncited | — | ~30% |
| IND-CLL-1L-BTKI | overall_response_rate | uncited | — | ~94% (≥PR by iwCLL) |
| IND-CLL-1L-BTKI | overall_survival_5y | uncited | — | ~85-90% |
| IND-CLL-1L-BTKI | progression_free_survival | probably-cited | trial-family: ELEVATE | 5-year PFS ~78% (ELEVATE-TN) |
| IND-CLL-1L-VENO | complete_response | probably-cited | trial-family: CLL14 | ~50% (with MRD-negative depth ~75% at end of treatment, CLL14) |
| IND-CLL-1L-VENO | overall_response_rate | uncited | — | ~85% |
| IND-CLL-1L-VENO | overall_survival_5y | uncited | — | ~85-90% |
| IND-CLL-1L-VENO | progression_free_survival | probably-cited | trial-family: CLL14 | 6-year PFS ~53% (CLL14 follow-up); fixed-duration |
| IND-CLL-1L-ZANUBRUTINIB | complete_response | uncited | — | ~30% |
| IND-CLL-1L-ZANUBRUTINIB | overall_response_rate | uncited | — | ~95% (≥PR by iwCLL, SEQUOIA / ALPINE r/r) |
| IND-CLL-1L-ZANUBRUTINIB | overall_survival_5y | uncited | — | ~85-90% |
| IND-CLL-1L-ZANUBRUTINIB | progression_free_survival | uncited | — | 5-year PFS ~75-80% (SEQUOIA 1L) |
| IND-CLL-2L-VENR-MURANO | complete_response | uncited | — | ~27% (CR/CRi) |
| IND-CLL-2L-VENR-MURANO | overall_response_rate | probably-cited | trial-family: MURANO | ~92% (≥PR by iwCLL, MURANO) |
| IND-CLL-2L-VENR-MURANO | overall_survival_5y | uncited | — | 5-year OS ~82% vs ~62% BR (HR 0.41) |
| IND-CLL-2L-VENR-MURANO | progression_free_survival | probably-cited | trial-family: MURANO | 4-year PFS 57.3% vs 4.6% BR (MURANO; HR 0.19) |
| IND-CLL-3L-LISOCEL | complete_response | uncited | — | ~18% (CR + CRi with undetectable MRD ~64% of CR responders) |
| IND-CLL-3L-LISOCEL | overall_response_rate | probably-cited | trial-number unresolved: TRANSCEND | ~47% (TRANSCEND CLL-004 primary cohort, n≈87 evaluable, double-exposed cBTKi + BCL-2i progression) |
| IND-CLL-3L-LISOCEL | overall_survival_5y | uncited | — | Median OS ~30+ months at primary analysis; long-term follow-up ongoing |
| IND-CLL-3L-LISOCEL | progression_free_survival | uncited | — | Median PFS ~12 months overall; deeper / longer in CR + uMRD subset (median PFS not reached at primary analysis) |
| IND-CLL-3L-PIRTOBRUTINIB | complete_response | uncited | — | ~3-7% |
| IND-CLL-3L-PIRTOBRUTINIB | overall_response_rate | probably-cited | trial-number unresolved: BRUIN | ~73% (BRUIN; ~71% in BTK-C481-mutated subset) |
| IND-CLL-3L-PIRTOBRUTINIB | overall_survival_5y | uncited | — | Mature OS data still maturing; 18-month OS ~80% |
| IND-CLL-3L-PIRTOBRUTINIB | progression_free_survival | probably-cited | trial-number unresolved: BRUIN | Median PFS ~19.6 mo (BRUIN, mostly post-cBTKi+BCL2i) |
| IND-CLL-ELDERLY-O-CHL | complete_response | uncited | — | ~21% |
| IND-CLL-ELDERLY-O-CHL | overall_response_rate | uncited | — | ~78% (CLL11 Goede 2014 NEJM) |
| IND-CLL-ELDERLY-O-CHL | overall_survival_5y | uncited | — | 5-yr OS ~74% (CLL11) |
| IND-CLL-ELDERLY-O-CHL | progression_free_survival | uncited | — | Median PFS 26.7 mo (CLL11 obinutuzumab + chlorambucil; 6-yr update Goede 2018) |

## `DIS-CML` — Chronic Myeloid Leukemia (BCR-ABL1)

Indications: 5; populated: 20; cited: 0; probably-cited: 1; uncited: 19; absent: 5; outcomes-cited % (loose): 5.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-CML-1L-2GEN-TKI | complete_response | uncited | — | MMR (BCR-ABL1 IS ≤0.1%) achieved in ~70-80% by 12 months on 2nd-gen TKI (vs 50-60% imatinib) |
| IND-CML-1L-2GEN-TKI | overall_response_rate | uncited | — | ~95-98% complete hematologic response by 3 months |
| IND-CML-1L-2GEN-TKI | overall_survival_5y | uncited | — | Approaches age-matched general population for patients in DMR |
| IND-CML-1L-2GEN-TKI | progression_free_survival | uncited | — | 10-y PFS ~85-90% (DASISION, ENESTnd long-term follow-up) |
| IND-CML-1L-IMATINIB | complete_response | uncited | — | Major molecular response (BCR-ABL1 IS ≤0.1%) achieved in ~50-60% by 12 months on imatinib (vs ~70-80% on 2nd-gen TKI) |
| IND-CML-1L-IMATINIB | overall_response_rate | uncited | — | ~95-98% complete hematologic response by 3 months |
| IND-CML-1L-IMATINIB | overall_survival_5y | uncited | — | ~83% at 10 years (IRIS); approaches age-matched general population for patients in DMR |
| IND-CML-1L-IMATINIB | progression_free_survival | uncited | — | 10-y PFS ~80-85% (IRIS) |
| IND-CML-2L-PONATINIB-T315I | complete_response | uncited | — | ~34% MMR (CML-CP); ~18% durable CMR |
| IND-CML-2L-PONATINIB-T315I | overall_response_rate | uncited | — | ~56% MCyR (CML-CP); ~70% MCyR in T315I-positive subset (PACE) |
| IND-CML-2L-PONATINIB-T315I | overall_survival_5y | uncited | — | 5-y OS ~73% in CML-CP per PACE long-term follow-up |
| IND-CML-2L-PONATINIB-T315I | progression_free_survival | uncited | — | Median PFS ~26 months (CML-CP at full dose); response-adjusted dosing per OPTIC extends with reduced vascular events |
| IND-CML-3L-ASCIMINIB | complete_response | uncited | — | MR4 (BCR-ABL1 IS ≤0.01%) ~10.8% at 24 weeks; ~17.4% at 96 weeks |
| IND-CML-3L-ASCIMINIB | overall_response_rate | probably-cited | trial-family: ASCEMBL | ~25.5% MMR at 24 weeks (ASCEMBL 3L+; vs 13.2% bosutinib) |
| IND-CML-3L-ASCIMINIB | overall_survival_5y | uncited | — | Mature OS data still maturing; 96-week OS ~90%+ |
| IND-CML-3L-ASCIMINIB | progression_free_survival | uncited | — | Median PFS not reached at 96 weeks; ~85% PFS at 96 weeks |
| IND-CML-ADVANCED-ALLOHCT | complete_response | uncited | — | Durable molecular CR ~50-70% at 5 years for CML-CP at HCT; ~20-40% for advanced phase / blast crisis |
| IND-CML-ADVANCED-ALLOHCT | overall_response_rate | uncited | — | ~80-90% achieve hematologic + cytogenetic remission post-HCT (variable by pre-HCT disease control) |
| IND-CML-ADVANCED-ALLOHCT | overall_survival_5y | uncited | — | 5-y OS 60-70% CML-CP; ~30% blast crisis (markedly worse without disease control pre-HCT) |
| IND-CML-ADVANCED-ALLOHCT | progression_free_survival | uncited | — | 5-y PFS 60-70% in CML-CP at HCT with optimal disease control; ~20-30% in blast crisis |

## `DIS-DLBCL-NOS` — Diffuse Large B-Cell Lymphoma, NOS

Indications: 12; populated: 48; cited: 2; probably-cited: 4; uncited: 42; absent: 12; outcomes-cited % (loose): 12.5%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-DLBCL-1L-POLA-R-CHP | complete_response | uncited | — | ~70% |
| IND-DLBCL-1L-POLA-R-CHP | overall_response_rate | probably-cited | trial-number unresolved: POLARIX | ~88% (≥PR after 6 cycles, POLARIX) |
| IND-DLBCL-1L-POLA-R-CHP | overall_survival_5y | uncited | — | Mature OS data still maturing; trends comparable or favoring Pola-R-CHP |
| IND-DLBCL-1L-POLA-R-CHP | progression_free_survival | uncited | — | 2-year PFS ~76.7% (vs 70.2% R-CHOP, HR 0.73) |
| IND-DLBCL-1L-RCHOP | complete_response | uncited | — | ~65-70% |
| IND-DLBCL-1L-RCHOP | overall_response_rate | uncited | — | ~85% (≥PR after 6 cycles) |
| IND-DLBCL-1L-RCHOP | overall_survival_5y | uncited | — | ~60% overall (low-IPI ~80%, high-IPI ~55%) |
| IND-DLBCL-1L-RCHOP | progression_free_survival | uncited | — | Median PFS ~5 years for low-IPI; ~2 years for high-IPI |
| IND-DLBCL-1L-RCHOP-ISRT-EARLY | complete_response | uncited | — | ~85-90% |
| IND-DLBCL-1L-RCHOP-ISRT-EARLY | overall_response_rate | uncited | — | ~95% (≥PR by end of treatment) |
| IND-DLBCL-1L-RCHOP-ISRT-EARLY | overall_survival_5y | uncited | — | ~89-91% in non-bulky stage I-II |
| IND-DLBCL-1L-RCHOP-ISRT-EARLY | progression_free_survival | uncited | — | 5-year PFS ~85-90% (LYSA / SWOG S1001) |
| IND-DLBCL-2L-LISOCEL | complete_response | uncited | — | ~74% (vs ~43% with standard salvage + autoSCT) |
| IND-DLBCL-2L-LISOCEL | overall_response_rate | uncited | — | ~86% (TRANSFORM phase 3 RCT vs salvage chemo + autoSCT) |
| IND-DLBCL-2L-LISOCEL | overall_survival_5y | uncited | — | OS trend favourable but crossover-confounded; long-term follow-up ongoing |
| IND-DLBCL-2L-LISOCEL | progression_free_survival | uncited | — | Median EFS 10.1 months vs 2.3 months for salvage chemo + autoSCT (HR ~0.36) |
| IND-DLBCL-2L-POLA-R-BENDAMUSTINE | complete_response | uncited | — | ~40% (vs 18% BR alone) |
| IND-DLBCL-2L-POLA-R-BENDAMUSTINE | overall_response_rate | uncited | — | ~63% (GO29365) |
| IND-DLBCL-2L-POLA-R-BENDAMUSTINE | overall_survival_5y | uncited | — | mOS ~12.4 mo (vs 4.7 mo BR; 2-year OS ~28%) |
| IND-DLBCL-2L-POLA-R-BENDAMUSTINE | progression_free_survival | uncited | — | Median PFS ~9.5 mo (vs 3.7 mo BR) |
| IND-DLBCL-3L-AXICEL-CART | complete_response | uncited | — | ~58% |
| IND-DLBCL-3L-AXICEL-CART | overall_response_rate | cited | trial-number resolved: ZUMA-1 | ~83% (ZUMA-1) |
| IND-DLBCL-3L-AXICEL-CART | overall_survival_5y | cited | trial-number resolved: ZUMA-1 | ~43% (ZUMA-1 5-year follow-up) |
| IND-DLBCL-3L-AXICEL-CART | progression_free_survival | uncited | — | Median PFS ~6 months for all responders; ~40% sustained remission at 5 years (durable) |
| IND-DLBCL-3L-EPCORITAMAB | complete_response | uncited | — | ~39% |
| IND-DLBCL-3L-EPCORITAMAB | overall_response_rate | uncited | — | ~63% (EPCORE NHL-1; n=157, ≥3L r/r LBCL with ~39% prior CAR-T) |
| IND-DLBCL-3L-EPCORITAMAB | overall_survival_5y | uncited | — | OS not reached at primary analysis; 12-month OS ~50% in pooled bispecific cohorts |
| IND-DLBCL-3L-EPCORITAMAB | progression_free_survival | uncited | — | Median PFS ~4.4 months overall; substantially longer in CR responders (median DOR ~12 months) |
| IND-DLBCL-3L-GLOFITAMAB | complete_response | uncited | — | ~39% |
| IND-DLBCL-3L-GLOFITAMAB | overall_response_rate | uncited | — | ~52% (NP30179; n=155, ≥3L r/r DLBCL with ~33% prior CAR-T) |
| IND-DLBCL-3L-GLOFITAMAB | overall_survival_5y | uncited | — | 12-month OS ~50%; long-term follow-up ongoing |
| IND-DLBCL-3L-GLOFITAMAB | progression_free_survival | uncited | — | Median CR DOR not reached at primary analysis; 12-month PFS among CR responders ~71% |
| IND-DLBCL-3L-LISO-CEL-CART | complete_response | uncited | — | ~53% |
| IND-DLBCL-3L-LISO-CEL-CART | overall_response_rate | probably-cited | trial-number unresolved: TRANSCEND | ~73% (TRANSCEND NHL-001 Abramson 2020 Lancet) |
| IND-DLBCL-3L-LISO-CEL-CART | overall_survival_5y | probably-cited | trial-number unresolved: TRANSCEND | Median OS 27.3 mo (TRANSCEND); CR responders mOS not reached |
| IND-DLBCL-3L-LISO-CEL-CART | progression_free_survival | probably-cited | trial-number unresolved: TRANSCEND | Median PFS 6.8 mo overall; 22.8 mo in CR responders (TRANSCEND) |
| IND-DLBCL-3L-LONCASTUXIMAB | complete_response | uncited | — | ~24% |
| IND-DLBCL-3L-LONCASTUXIMAB | overall_response_rate | uncited | — | ~48% (LOTIS-2 Caimi 2021 Lancet Oncol) |
| IND-DLBCL-3L-LONCASTUXIMAB | overall_survival_5y | uncited | — | Median OS 9.5 mo (LOTIS-2) |
| IND-DLBCL-3L-LONCASTUXIMAB | progression_free_survival | uncited | — | Median PFS 4.9 mo (LOTIS-2) |
| IND-DLBCL-RENAL-FAILURE-MOD-RCHOP | complete_response | uncited | — | ~60% |
| IND-DLBCL-RENAL-FAILURE-MOD-RCHOP | overall_response_rate | uncited | — | ~80% (extrapolated from R-CHOP non-CKD cohorts; Ostgard 2014 retrospective CKD subgroup) |
| IND-DLBCL-RENAL-FAILURE-MOD-RCHOP | overall_survival_5y | uncited | — | 5-yr OS ~50% (modified regimen extrapolation; competing risks dominate) |
| IND-DLBCL-RENAL-FAILURE-MOD-RCHOP | progression_free_survival | uncited | — | Median PFS ~3-4 yr (lower than non-CKD due to dose reduction + competing CKD mortality) |
| IND-EMERG-INFUSION-REACTION-IRR | complete_response | uncited | — | N/A (acute management) |
| IND-EMERG-INFUSION-REACTION-IRR | overall_response_rate | uncited | — | ~95% successfully resume infusion at slower rate after grade 1-2 IRR management |
| IND-EMERG-INFUSION-REACTION-IRR | overall_survival_5y | uncited | — | Anaphylaxis (grade 4 IRR) mortality without epinephrine ~10-15%; with proper management <1% |
| IND-EMERG-INFUSION-REACTION-IRR | progression_free_survival | uncited | — | N/A |

## `DIS-EATL` — Enteropathy-Associated T-Cell Lymphoma

Indications: 2; populated: 8; cited: 0; probably-cited: 0; uncited: 8; absent: 2; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-EATL-1L-CHOEP-AUTOSCT | complete_response | uncited | — | ~40-50% |
| IND-EATL-1L-CHOEP-AUTOSCT | overall_response_rate | uncited | — | ~60-70% |
| IND-EATL-1L-CHOEP-AUTOSCT | overall_survival_5y | uncited | — | ~50-60% (з autoSCT); ~20% chemo-only |
| IND-EATL-1L-CHOEP-AUTOSCT | progression_free_survival | uncited | — | Median PFS ~24 months (з autoSCT) |
| IND-EATL-2L-ICE | complete_response | uncited | — | ~25-30% |
| IND-EATL-2L-ICE | overall_response_rate | uncited | — | ~50% (small series; EATL very chemo-refractory) |
| IND-EATL-2L-ICE | overall_survival_5y | uncited | — | <20% without alloSCT; ~25-30% if bridge to alloSCT in CR2 |
| IND-EATL-2L-ICE | progression_free_survival | uncited | — | Median PFS ~6-9 months without consolidative SCT |

## `DIS-ENDOMETRIAL` — Endometrial carcinoma

Indications: 5; populated: 14; cited: 1; probably-cited: 3; uncited: 10; absent: 13; outcomes-cited % (loose): 28.6%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR | complete_response | uncited | — | ~15% |
| IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR | overall_response_rate | uncited | — | ~45% (GARNET dMMR cohort, single-arm) |
| IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR | overall_survival_5y | uncited | — | 2-year OS ~63% (GARNET dMMR) |
| IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR | progression_free_survival | uncited | — | Median DoR not reached (>16 mo); median PFS not reached for responders |
| IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR | complete_response | uncited | — | ~5% pMMR |
| IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR | overall_response_rate | probably-cited | trial-number unresolved: KEYNOTE-775 | ~30% pMMR (KEYNOTE-775) |
| IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR | overall_survival_5y | probably-cited | trial-number unresolved: KEYNOTE-775 | mOS 17.4 vs 12.0 mo chemo pMMR (HR 0.68, KEYNOTE-775) |
| IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR | progression_free_survival | probably-cited | trial-number unresolved: KEYNOTE-775 | Median PFS 6.6 vs 3.8 mo chemo pMMR (HR 0.60, KEYNOTE-775) |
| IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO | pfs_hr_dmmr | cited | trial-number resolved: RUBY | 0.3 |
| IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO | pfs_hr_pmmr | uncited | — | 0.64 |
| IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION | complete_response | uncited | — | n/a |
| IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION | overall_response_rate | uncited | — | n/a (post-surgical surveillance — no systemic / radiation therapy) |
| IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION | overall_survival_5y | uncited | — | >95% (excellent prognosis driven by hypermutator phenotype + early stage) |
| IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION | progression_free_survival | uncited | — | Stage I POLE-EDM 5-year PFS ~95-100% per PORTEC-3 / TransPORTEC pooled analysis |

## `DIS-ESOPHAGEAL` — Esophageal carcinoma (squamous + adeno)

Indications: 6; populated: 20; cited: 6; probably-cited: 5; uncited: 9; absent: 12; outcomes-cited % (loose): 55.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS | overall_survival_5y | uncited | — | OS endpoint maturing — DFS doubling practice-changing |
| IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS | progression_free_survival | probably-cited | trial-number unresolved: CheckMate-577 | Median DFS 22 vs 11 mo placebo (CheckMate-577) |
| IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC | overall_response_rate | cited | trial-number resolved: CheckMate-648 | 47.0% vs 27.3% (CPS≥1 nivo+chemo vs chemo; CheckMate-648) |
| IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC | overall_survival_median | cited | trial-number resolved: CheckMate-648 | mOS 15.4 vs 9.1 mo (CPS≥1, HR 0.54, p<0.0001) |
| IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC | progression_free_survival | cited | trial-number resolved: CheckMate-648 | mPFS 6.9 vs 4.4 mo (CPS≥1, HR 0.65) |
| IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO | overall_response_rate | cited | trial-number resolved: KEYNOTE-590 | ~51% (ESCC CPS≥10 pembro+chemo vs 26% chemo; KEYNOTE-590) |
| IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO | overall_survival_median | cited | trial-number resolved: KEYNOTE-590 | mOS 13.9 vs 8.8 mo (ESCC CPS≥10, HR 0.57, p<0.0001) |
| IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO | progression_free_survival | cited | trial-number resolved: KEYNOTE-590 | mPFS 7.5 vs 5.5 mo (ESCC CPS≥10, HR 0.51) |
| IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS | complete_response | uncited | — | ~1% |
| IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS | overall_response_rate | probably-cited | trial-family: ATTRACTION | ~19% (ATTRACTION-3) |
| IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS | overall_survival_5y | probably-cited | trial-family: ATTRACTION | mOS 10.9 vs 8.4 mo taxane (HR 0.77, ATTRACTION-3); 12-mo OS 47% vs 34% |
| IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS | progression_free_survival | uncited | — | Median PFS 1.7 mo (vs 3.4 mo taxane; ICI delayed-effect kinetics) |
| IND-ESOPH-METASTATIC-2L-PEMBRO-CPS10 | complete_response | uncited | — | ~5% |
| IND-ESOPH-METASTATIC-2L-PEMBRO-CPS10 | overall_response_rate | probably-cited | trial-number unresolved: KEYNOTE-181 | ~22% (KEYNOTE-181 CPS ≥10 subgroup) |
| IND-ESOPH-METASTATIC-2L-PEMBRO-CPS10 | overall_survival_5y | probably-cited | trial-number unresolved: KEYNOTE-181 | mOS 9.3 vs 6.7 mo chemo (HR 0.69, KEYNOTE-181 CPS ≥10) |
| IND-ESOPH-METASTATIC-2L-PEMBRO-CPS10 | progression_free_survival | uncited | — | Median PFS 2.6 mo CPS ≥10 (vs 3.0 mo chemo; ICI kinetics) |
| IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT | complete_response | uncited | — | pCR rates above |
| IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT | overall_response_rate | uncited | — | pCR rate ~29% squamous, ~23% adeno (CROSS) |
| IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT | overall_survival_5y | uncited | — | 5-yr OS ~47% (CROSS) |
| IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT | progression_free_survival | uncited | — | median DFS ~24 mo (CROSS combined) |

## `DIS-ET` — Essential Thrombocythemia

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ET-1L-ASA | complete_response | uncited | — | Thrombosis-risk reduction; symptom improvement |
| IND-ET-1L-ASA | overall_response_rate | uncited | — | Plt control to <400-450K achievable in >80% on HU |
| IND-ET-1L-ASA | overall_survival_5y | uncited | — | Median OS ~18-20 years; 5-y OS ~90% with proper management |
| IND-ET-1L-ASA | progression_free_survival | uncited | — | Thrombosis-related events ~50-60% reduction on HU + ASA in high-risk |
| IND-ET-1L-HU | complete_response | uncited | — | Cytoreduction + thrombosis-risk reduction |
| IND-ET-1L-HU | overall_response_rate | uncited | — | Plt <400-450K achievable in >85% on HU |
| IND-ET-1L-HU | overall_survival_5y | uncited | — | Median OS ~18-20 years; 5-y OS ~88% |
| IND-ET-1L-HU | progression_free_survival | uncited | — | Thrombosis events reduced ~50% vs ASA alone in high-risk (PT-1 control arm) |
| IND-ET-2L-ANAGRELIDE | complete_response | uncited | — | Cytoreduction goal — measured by platelet response and thrombosis prevention |
| IND-ET-2L-ANAGRELIDE | overall_response_rate | uncited | — | ~70-75% achieve plt <600 × 10⁹/L; ~50% achieve <450 × 10⁹/L |
| IND-ET-2L-ANAGRELIDE | overall_survival_5y | uncited | — | Median OS ~15-20 years for ET overall; not directly altered by 2L choice |
| IND-ET-2L-ANAGRELIDE | progression_free_survival | uncited | — | Long-term cytoreductive maintenance; thrombosis-free survival inferior to HU per PT-1 in arterial events |

## `DIS-FL` — Follicular Lymphoma

Indications: 7; populated: 27; cited: 0; probably-cited: 2; uncited: 25; absent: 8; outcomes-cited % (loose): 7.4%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-FL-1L-BR | complete_response | uncited | — | ~40% |
| IND-FL-1L-BR | overall_response_rate | uncited | — | ~93% |
| IND-FL-1L-BR | overall_survival_5y | uncited | — | ~88% |
| IND-FL-1L-BR | progression_free_survival | uncited | — | Median PFS ~6-7 years (StiL trial — superior to R-CHOP for FL) |
| IND-FL-1L-RCHOP-AGGRESSIVE | complete_response | uncited | — | ~70% |
| IND-FL-1L-RCHOP-AGGRESSIVE | overall_response_rate | uncited | — | ~85-90% |
| IND-FL-1L-RCHOP-AGGRESSIVE | overall_survival_5y | uncited | — | ~85% |
| IND-FL-1L-RCHOP-AGGRESSIVE | progression_free_survival | uncited | — | Median PFS comparable to BR for FL grade 1-2; preferred for FL grade 3A and transformation |
| IND-FL-1L-WATCH | overall_response_rate | uncited | — | N/A — observational |
| IND-FL-1L-WATCH | overall_survival_5y | uncited | — | Equivalent to immediate-treatment arm in multiple RCTs (Ardeshna 2014, RESORT) |
| IND-FL-1L-WATCH | progression_free_survival | uncited | — | Median time-to-treatment 2-5 years; many patients never need treatment |
| IND-FL-3L-AXICEL-CART | complete_response | uncited | — | ~79% |
| IND-FL-3L-AXICEL-CART | overall_response_rate | probably-cited | trial-number unresolved: ZUMA-5 | ~94% (ZUMA-5) |
| IND-FL-3L-AXICEL-CART | overall_survival_5y | probably-cited | trial-number unresolved: ZUMA-5 | ~73% (4-year OS ZUMA-5) |
| IND-FL-3L-AXICEL-CART | progression_free_survival | uncited | — | Median PFS not reached at 4y; ~57% of complete responders remain in remission at 4y |
| IND-FL-3L-MOSUNETUZUMAB | complete_response | uncited | — | ~60% |
| IND-FL-3L-MOSUNETUZUMAB | overall_response_rate | uncited | — | ~80% (GO29781) |
| IND-FL-3L-MOSUNETUZUMAB | overall_survival_5y | uncited | — | Mature OS data still maturing; estimated 24-mo OS ~87% |
| IND-FL-3L-MOSUNETUZUMAB | progression_free_survival | uncited | — | Median PFS ~17.9 mo; median DOR ~22.8 mo |
| IND-FL-3L-TAZEMETOSTAT | complete_response | uncited | — | ~13% (EZH2-mut) / ~4% (EZH2-WT) |
| IND-FL-3L-TAZEMETOSTAT | overall_response_rate | uncited | — | ~69% (EZH2-mut) / ~35% (EZH2-WT) per E7438-G000-101 |
| IND-FL-3L-TAZEMETOSTAT | overall_survival_5y | uncited | — | Not reached for either subset at primary analysis; estimated 24-mo OS ~88% (mut) |
| IND-FL-3L-TAZEMETOSTAT | progression_free_survival | uncited | — | Median PFS ~13.8 mo (EZH2-mut) / ~11.1 mo (EZH2-WT) |
| IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | complete_response | uncited | — | N/A (maintenance phase) |
| IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | overall_response_rate | uncited | — | Maintenance — measured by deepening + duration; ~30% achieve CR conversion during maintenance |
| IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | overall_survival_5y | uncited | — | OS impact unclear; PRIMA 9-yr update no OS difference |
| IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | progression_free_survival | uncited | — | Median PFS ~10 years vs ~4 years observation (PRIMA Salles 2011 + 2019 update) |

## `DIS-GASTRIC` — Gastric / GEJ adenocarcinoma

Indications: 6; populated: 25; cited: 4; probably-cited: 8; uncited: 13; absent: 7; outcomes-cited % (loose): 48.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GASTRIC-METASTATIC-1L-CLDN18-2-ZOLBETUXIMAB | overall_response_rate | probably-cited | trial-number unresolved: GLOW | ~60-65% (SPOTLIGHT/GLOW combined zolbetuximab + chemo arms; consistent with chemo backbone alone but durable) |
| IND-GASTRIC-METASTATIC-1L-CLDN18-2-ZOLBETUXIMAB | overall_survival_5y | probably-cited | trial-number unresolved: GLOW | Median OS 18.2 mo (SPOTLIGHT) / 14.4 mo (GLOW); HR ~0.75 vs chemo alone |
| IND-GASTRIC-METASTATIC-1L-CLDN18-2-ZOLBETUXIMAB | progression_free_survival | probably-cited | trial-number unresolved: GLOW | Median PFS 10.6 mo (SPOTLIGHT mFOLFOX6) / 8.2 mo (GLOW CAPOX) |
| IND-GASTRIC-METASTATIC-1L-HER2-TOGA | complete_response | uncited | — | ~5% |
| IND-GASTRIC-METASTATIC-1L-HER2-TOGA | overall_response_rate | uncited | — | ~47% (TOGA HER2 IHC3+ subgroup) |
| IND-GASTRIC-METASTATIC-1L-HER2-TOGA | overall_survival_5y | uncited | — | mOS 13.8 vs 11.1 chemo-only TOGA; 17.9 in HER2 IHC3+ subgroup |
| IND-GASTRIC-METASTATIC-1L-HER2-TOGA | progression_free_survival | uncited | — | Median ~7 mo |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | complete_response | uncited | — | ~10% |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | overall_response_rate | cited | trial-number resolved: CheckMate-649 | ~60% (CheckMate-649 CPS ≥5); preserved benefit at CPS 1-4 |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | overall_survival_5y | cited | trial-number resolved: CheckMate-649 | mOS 14.4 mo (vs 11.1 chemo alone, CheckMate-649 CPS ≥5) |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | overall_survival_hr_cps_1_to_4 | cited | SRC-id hit: SRC-CHECKMATE-649-JANJIGIAN-2022 | OS HR 0.78 (CPS 1-4; preserved benefit, smaller magnitude than CPS ≥5) SRC-CHECKMATE-649-JANJIGIAN-2022 |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | overall_survival_hr_cps_5plus | cited | SRC-id hit: SRC-CHECKMATE-649-JANJIGIAN-2022 | OS HR 0.71 (CPS ≥5; CheckMate-649) SRC-CHECKMATE-649-JANJIGIAN-2022 |
| IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI | progression_free_survival | uncited | — | Median ~7.7 mo (CPS ≥5) |
| IND-GASTRIC-METASTATIC-2L-HER2-TDXD | complete_response | uncited | — | ~9% |
| IND-GASTRIC-METASTATIC-2L-HER2-TDXD | overall_response_rate | probably-cited | trial-number unresolved: DESTINY-Gastric01 | ~51% (DESTINY-Gastric01) |
| IND-GASTRIC-METASTATIC-2L-HER2-TDXD | overall_survival_5y | probably-cited | trial-number unresolved: DESTINY-Gastric01 | mOS 12.5 vs 8.4 mo (HR 0.59, DESTINY-Gastric01) |
| IND-GASTRIC-METASTATIC-2L-HER2-TDXD | progression_free_survival | uncited | — | Median PFS 5.6 mo (vs 3.5 mo investigator's choice; HR 0.47) |
| IND-GASTRIC-METASTATIC-2L-RAMUCIRUMAB-PACLITAXEL | complete_response | uncited | — | ~1% |
| IND-GASTRIC-METASTATIC-2L-RAMUCIRUMAB-PACLITAXEL | overall_response_rate | probably-cited | trial-family: RAINBOW | ~28% (RAINBOW) |
| IND-GASTRIC-METASTATIC-2L-RAMUCIRUMAB-PACLITAXEL | overall_survival_5y | probably-cited | trial-family: RAINBOW | mOS 9.6 vs 7.4 mo (HR 0.81, RAINBOW) |
| IND-GASTRIC-METASTATIC-2L-RAMUCIRUMAB-PACLITAXEL | progression_free_survival | probably-cited | trial-family: RAINBOW | Median PFS 4.4 vs 2.9 mo paclitaxel alone (HR 0.64, RAINBOW) |
| IND-GASTRIC-METASTATIC-3L-TAS102 | complete_response | uncited | — | <1% |
| IND-GASTRIC-METASTATIC-3L-TAS102 | overall_response_rate | uncited | — | ~4% (TAGS — modest cytoreduction) |
| IND-GASTRIC-METASTATIC-3L-TAS102 | overall_survival_5y | uncited | — | mOS 5.7 vs 3.6 mo placebo (HR 0.69, TAGS) |
| IND-GASTRIC-METASTATIC-3L-TAS102 | progression_free_survival | uncited | — | Median PFS 2.0 vs 1.8 mo placebo (HR 0.57, TAGS) |

## `DIS-GBM` — Glioblastoma (IDH-WT, WHO grade 4)

Indications: 4; populated: 8; cited: 0; probably-cited: 0; uncited: 8; absent: 15; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GBM-NEWLY-DIAGNOSED-ELDERLY-HYPORT | overall_survival_median | uncited | — | mOS 9.3 mo (hypoRT + TMZ) vs 7.6 mo (hypoRT alone; CCTG CE.6, n=562, ≥65 yrs) |
| IND-GBM-NEWLY-DIAGNOSED-ELDERLY-TMZ | overall_survival_median | uncited | — | mOS ~7-9 mo in elderly GBM with TMZ alone (Nordic; MGMT-methylated: ~10 mo) |
| IND-GBM-NEWLY-DIAGNOSED-STUPP | overall_response_rate | uncited | — | Adjuvant — measured by PFS/OS |
| IND-GBM-NEWLY-DIAGNOSED-STUPP | overall_survival_5y | uncited | — | mOS 14.6 mo (2-yr OS 27%); MGMT-methylated 21.7 mo |
| IND-GBM-NEWLY-DIAGNOSED-STUPP | progression_free_survival | uncited | — | Median PFS ~7 mo; 6-mo PFS ~54% |
| IND-GBM-RECURRENT-BEVACIZUMAB | overall_response_rate | uncited | — | ~28-38% (radiographic response; predominantly pseudo-response on MRI) |
| IND-GBM-RECURRENT-BEVACIZUMAB | overall_survival_median | uncited | — | mOS ~9-10 mo from recurrence (no OS benefit in randomized data) |
| IND-GBM-RECURRENT-BEVACIZUMAB | progression_free_survival | uncited | — | mPFS ~4-6 mo (AVAglio + RTOG 0825 recurrent data; phase 2 studies) |

## `DIS-GI-NET` — Gastroenteropancreatic neuroendocrine tumor — GI origin (carcinoid), well-differentiated G1/G2

Indications: 1; populated: 4; cited: 0; probably-cited: 0; uncited: 4; absent: 1; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GI-NET-ADVANCED-1L-LANREOTIDE | complete_response | uncited | — | <1% |
| IND-GI-NET-ADVANCED-1L-LANREOTIDE | overall_response_rate | uncited | — | ~3% (partial response; stable disease is the primary endpoint — 65% in CLARINET lanreotide arm) |
| IND-GI-NET-ADVANCED-1L-LANREOTIDE | overall_survival_5y | uncited | — | No OS benefit demonstrated in CLARINET (low event rate, cross-over); OS secondary endpoint |
| IND-GI-NET-ADVANCED-1L-LANREOTIDE | progression_free_survival | uncited | — | mPFS not reached (lanreotide arm) vs 18.0 mo placebo (HR 0.47, CLARINET) |

## `DIS-GIST` — Gastrointestinal stromal tumor (GIST)

Indications: 3; populated: 10; cited: 0; probably-cited: 1; uncited: 9; absent: 5; outcomes-cited % (loose): 10.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GIST-1L-AVAPRITINIB-PDGFRA-D842V | overall_response_rate | uncited | — | ~88% (NAVIGATOR PDGFRA D842V cohort) |
| IND-GIST-1L-AVAPRITINIB-PDGFRA-D842V | overall_survival_5y | uncited | — | Not yet mature; ~70% at 36 months in NAVIGATOR D842V cohort |
| IND-GIST-1L-AVAPRITINIB-PDGFRA-D842V | progression_free_survival | uncited | — | Median ~34 months (NAVIGATOR PDGFRA D842V) |
| IND-GIST-1L-IMATINIB | overall_response_rate | uncited | — | ~50-67% (KIT exon 11) |
| IND-GIST-1L-IMATINIB | overall_survival_5y | uncited | — | ~50% advanced disease; ~80-90% adjuvant high-risk |
| IND-GIST-1L-IMATINIB | progression_free_survival | uncited | — | ~24 months (KIT exon 11); ~12 months (KIT exon 9 at 800 mg) |
| IND-GIST-4L-RIPRETINIB | complete_response | uncited | — | ~0% CR; majority partial responses + stable disease |
| IND-GIST-4L-RIPRETINIB | overall_response_rate | uncited | — | ~9.4% ORR (INVICTUS, n=129; ripretinib 150 mg vs placebo 4L+ GIST) |
| IND-GIST-4L-RIPRETINIB | overall_survival_5y | probably-cited | trial-number unresolved: INTRIGUE | Median OS 15.1 vs 6.6 months (HR 0.36) — INVICTUS secondary endpoint with crossover allowed. INTRIGUE phase III (ripr... |
| IND-GIST-4L-RIPRETINIB | progression_free_survival | uncited | — | Median PFS 6.3 vs 1.0 months (HR 0.15, p<0.0001) — INVICTUS primary endpoint |

## `DIS-GLIOMA-LOW-GRADE` — Low-grade glioma (LGG, WHO grade 2 — IDH-mutant)

Indications: 1; populated: 3; cited: 3; probably-cited: 0; uncited: 0; absent: 2; outcomes-cited % (loose): 100.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GLIOMA-LOW-GRADE-1L-RT-PCV | overall_response_rate | cited | SRC-id hit: SRC-EANO-GBM-2024 | Median PFS 10.4 yr (RT+PCV) vs 4.0 yr (RT alone), RTOG 9802 high-risk LGG |
| IND-GLIOMA-LOW-GRADE-1L-RT-PCV | overall_survival_5y | cited | SRC-id hit: SRC-EANO-GBM-2024 | Median OS 13.3 yr (RT+PCV) vs 7.8 yr (RT alone) per RTOG 9802 (Buckner 2016 NEJM); 10-yr OS 60% vs 40% |
| IND-GLIOMA-LOW-GRADE-1L-RT-PCV | progression_free_survival | cited | SRC-id hit: SRC-EANO-GBM-2024 | Median PFS 10.4 yr per RTOG 9802 long-term |

## `DIS-HCC` — Hepatocellular carcinoma (HCC)

Indications: 6; populated: 24; cited: 3; probably-cited: 0; uncited: 21; absent: 6; outcomes-cited % (loose): 12.5%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HCC-SYSTEMIC-1L-ATEZO-BEV | complete_response | uncited | — | ~7% |
| IND-HCC-SYSTEMIC-1L-ATEZO-BEV | overall_response_rate | uncited | — | ~30% (RECIST mRECIST higher) |
| IND-HCC-SYSTEMIC-1L-ATEZO-BEV | overall_survival_5y | cited | trial-number resolved: IMbrave150 | mOS 19.2 mo IMbrave150 vs 13.4 sorafenib |
| IND-HCC-SYSTEMIC-1L-ATEZO-BEV | progression_free_survival | cited | trial-number resolved: IMbrave150 | Median ~6.8 mo (IMbrave150) |
| IND-HCC-SYSTEMIC-1L-DURVA-TREME | complete_response | uncited | — | ~3% |
| IND-HCC-SYSTEMIC-1L-DURVA-TREME | overall_response_rate | uncited | — | ~20% |
| IND-HCC-SYSTEMIC-1L-DURVA-TREME | overall_survival_5y | cited | trial-number resolved: HIMALAYA | mOS 16.4 vs 13.8 sorafenib (HIMALAYA) |
| IND-HCC-SYSTEMIC-1L-DURVA-TREME | progression_free_survival | uncited | — | Median ~4 mo |
| IND-HCC-SYSTEMIC-1L-SORAFENIB | complete_response | uncited | — | <1% |
| IND-HCC-SYSTEMIC-1L-SORAFENIB | overall_response_rate | uncited | — | ~3% (RECIST); 10-15% (mRECIST) |
| IND-HCC-SYSTEMIC-1L-SORAFENIB | overall_survival_5y | uncited | — | mOS ~10-11 mo (SHARP), worse for CP-B |
| IND-HCC-SYSTEMIC-1L-SORAFENIB | progression_free_survival | uncited | — | Median ~4 mo |
| IND-HCC-SYSTEMIC-2L-CABOZANTINIB | complete_response | uncited | — | <1% |
| IND-HCC-SYSTEMIC-2L-CABOZANTINIB | overall_response_rate | uncited | — | ~4% ORR (RECIST 1.1, CELESTIAL) — disease stabilization is the primary goal |
| IND-HCC-SYSTEMIC-2L-CABOZANTINIB | overall_survival_5y | uncited | — | Median OS 10.2 mo vs 8.0 mo (HR 0.76, 95% CI 0.63–0.92, p=0.005, CELESTIAL) |
| IND-HCC-SYSTEMIC-2L-CABOZANTINIB | progression_free_survival | uncited | — | Median PFS 5.2 mo vs 1.9 mo (HR 0.44, p<0.001, CELESTIAL) |
| IND-HCC-SYSTEMIC-2L-RAMUCIRUMAB | complete_response | uncited | — | ~1% |
| IND-HCC-SYSTEMIC-2L-RAMUCIRUMAB | overall_response_rate | uncited | — | ~5% ORR (RECIST 1.1, REACH-2) |
| IND-HCC-SYSTEMIC-2L-RAMUCIRUMAB | overall_survival_5y | uncited | — | Median OS 8.5 mo vs 7.3 mo (HR 0.71, 95% CI 0.53–0.95, p=0.0199, REACH-2) |
| IND-HCC-SYSTEMIC-2L-RAMUCIRUMAB | progression_free_survival | uncited | — | Median PFS 2.8 mo vs 1.6 mo (HR 0.45, REACH-2) |
| IND-HCC-SYSTEMIC-2L-REGORAFENIB | complete_response | uncited | — | ~1% |
| IND-HCC-SYSTEMIC-2L-REGORAFENIB | overall_response_rate | uncited | — | ~11% ORR (RECIST 1.1); DCR 65% vs placebo 36% (RESORCE) |
| IND-HCC-SYSTEMIC-2L-REGORAFENIB | overall_survival_5y | uncited | — | Median OS 10.6 mo vs 7.8 mo (HR 0.63, 95% CI 0.50–0.79, p<0.0001, RESORCE); sequential sorafenib→regorafenib OS ~26 m... |
| IND-HCC-SYSTEMIC-2L-REGORAFENIB | progression_free_survival | uncited | — | Median PFS 3.1 mo vs 1.5 mo (HR 0.46, p<0.0001, RESORCE) |

## `DIS-HCL` — Hairy Cell Leukemia

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HCL-1L-CLADRIBINE | complete_response | uncited | — | ~85% |
| IND-HCL-1L-CLADRIBINE | overall_response_rate | uncited | — | ~95% |
| IND-HCL-1L-CLADRIBINE | overall_survival_5y | uncited | — | ~90% |
| IND-HCL-1L-CLADRIBINE | progression_free_survival | uncited | — | Median PFS >10 years |
| IND-HCL-1L-PENTOSTATIN | complete_response | uncited | — | ~80% |
| IND-HCL-1L-PENTOSTATIN | overall_response_rate | uncited | — | ~95% |
| IND-HCL-1L-PENTOSTATIN | overall_survival_5y | uncited | — | ~85-90% |
| IND-HCL-1L-PENTOSTATIN | progression_free_survival | uncited | — | Median PFS ~10 years |
| IND-HCL-2L-VEMURAFENIB | complete_response | uncited | — | ~87% CR; ~65% MRD-negative |
| IND-HCL-2L-VEMURAFENIB | overall_response_rate | uncited | — | ~96% (Tiacci 2021 NEJM vemurafenib + rituximab in r/r HCL) |
| IND-HCL-2L-VEMURAFENIB | overall_survival_5y | uncited | — | ~95% |
| IND-HCL-2L-VEMURAFENIB | progression_free_survival | uncited | — | Median PFS not reached at 4-year follow-up |

## `DIS-HCV-MZL` — HCV-associated Marginal Zone Lymphoma

Indications: 3; populated: 14; cited: 0; probably-cited: 0; uncited: 14; absent: 1; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HCV-MZL-1L-ANTIVIRAL | complete_response | uncited | — | ~50% at 12 months post-SVR |
| IND-HCV-MZL-1L-ANTIVIRAL | hcv_cure_rate_svr12 | uncited | — | >95% (non-cirrhotic, treatment-naive) |
| IND-HCV-MZL-1L-ANTIVIRAL | overall_response_rate | uncited | — | ~75% (lymphoma regression after SVR12) |
| IND-HCV-MZL-1L-ANTIVIRAL | overall_survival_5y | uncited | — | >85% in non-cirrhotic responders |
| IND-HCV-MZL-1L-ANTIVIRAL | progression_free_survival | uncited | — | Median not reached in DAA-responsive cases; prolonged |
| IND-HCV-MZL-1L-BR-AGGRESSIVE | complete_response | uncited | — | ~70% |
| IND-HCV-MZL-1L-BR-AGGRESSIVE | hcv_cure_rate_svr12 | uncited | — | >95% (with concurrent DAA) |
| IND-HCV-MZL-1L-BR-AGGRESSIVE | overall_response_rate | uncited | — | ~90% |
| IND-HCV-MZL-1L-BR-AGGRESSIVE | overall_survival_5y | uncited | — | >80% |
| IND-HCV-MZL-1L-BR-AGGRESSIVE | progression_free_survival | uncited | — | Median >5 years in responders |
| IND-HCV-MZL-POST-DAA-SURVEILLANCE | complete_response | uncited | — | ~45-55% lymphoma CR from DAA alone |
| IND-HCV-MZL-POST-DAA-SURVEILLANCE | overall_response_rate | uncited | — | ~70% hematologic response from DAA alone (Arcaini 2014; modern DAA era confirmation Carrier 2015) |
| IND-HCV-MZL-POST-DAA-SURVEILLANCE | overall_survival_5y | uncited | — | Excellent (~90%+) for responders; non-responders route to immunochemotherapy |
| IND-HCV-MZL-POST-DAA-SURVEILLANCE | progression_free_survival | uncited | — | Median time-to-event ~6-12 months for visible response; durable in most responders |

## `DIS-HGBL-DH` — High-Grade B-Cell Lymphoma with MYC and BCL2 and/or BCL6 rearrangements (double-hit / triple-hit)

Indications: 3; populated: 12; cited: 2; probably-cited: 0; uncited: 10; absent: 3; outcomes-cited % (loose): 16.7%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HGBL-DH-1L-DAEPOCHR | complete_response | uncited | — | ~60-70% |
| IND-HGBL-DH-1L-DAEPOCHR | overall_response_rate | uncited | — | ~85% |
| IND-HGBL-DH-1L-DAEPOCHR | overall_survival_5y | uncited | — | ~50-65% (substantially better than R-CHOP ~30%) |
| IND-HGBL-DH-1L-DAEPOCHR | progression_free_survival | uncited | — | Median PFS ~3-5 years |
| IND-HGBL-DH-1L-RCHOP | complete_response | uncited | — | ~50% |
| IND-HGBL-DH-1L-RCHOP | overall_response_rate | uncited | — | ~70% |
| IND-HGBL-DH-1L-RCHOP | overall_survival_5y | uncited | — | ~30% |
| IND-HGBL-DH-1L-RCHOP | progression_free_survival | uncited | — | Median PFS ~1-2 years |
| IND-HGBL-DH-2L-CART-AXICEL | complete_response | uncited | — | ~58% |
| IND-HGBL-DH-2L-CART-AXICEL | overall_response_rate | cited | trial-number resolved: ZUMA-1 | ~83% (ZUMA-1 axi-cel in r/r aggressive B-NHL including HGBL-DH subgroup) |
| IND-HGBL-DH-2L-CART-AXICEL | overall_survival_5y | cited | trial-number resolved: ZUMA-1 | ~25-40% durable (5-yr ZUMA-1 update) |
| IND-HGBL-DH-2L-CART-AXICEL | progression_free_survival | uncited | — | Median PFS ~5.9 mo; durable response ~40% at 24 mo |

## `DIS-HNSCC` — Head and neck squamous cell carcinoma (HNSCC)

Indications: 5; populated: 21; cited: 18; probably-cited: 0; uncited: 3; absent: 15; outcomes-cited % (loose): 85.7%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HNSCC-RM-1L-EXTREME | overall_response_rate | uncited | — | ~36% (vs 20% platin+5-FU; EXTREME) |
| IND-HNSCC-RM-1L-EXTREME | overall_survival_5y | uncited | — | Median OS 10.1 vs 7.4 mo (HR 0.80, p=0.04); long-term survival rare in R/M SCCHN historically (5-yr OS <5%) |
| IND-HNSCC-RM-1L-EXTREME | progression_free_survival | uncited | — | Median PFS 5.6 vs 3.3 mo (HR 0.54) |
| IND-HNSCC-RM-1L-PEMBRO-CHEMO | overall_response_rate | cited | trial-number resolved: KEYNOTE-048 | ~36% (KEYNOTE-048 chemo-IO arm) |
| IND-HNSCC-RM-1L-PEMBRO-CHEMO | overall_survival_5y | cited | trial-number resolved: KEYNOTE-048 | Median OS 13.6 mo (vs 10.4 mo EXTREME); 24-mo OS ~29% |
| IND-HNSCC-RM-1L-PEMBRO-CHEMO | progression_free_survival | cited | trial-number resolved: KEYNOTE-048 | Median ~5 months |
| IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH | overall_response_rate | cited | trial-number resolved: KEYNOTE-048 | ~23% (KEYNOTE-048 mono CPS ≥20) |
| IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH | overall_survival_5y | cited | trial-number resolved: KEYNOTE-048 | Median OS 14.9 mo (vs 10.7 mo EXTREME); 24-mo OS ~35% |
| IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH | progression_free_survival | cited | trial-number resolved: KEYNOTE-048 | Median ~3.4 mo (selection bias toward responders has long tail) |
| IND-HNSCC-RM-2L-NIVOLUMAB | median_os_comparator_months | cited | trial-number resolved: CheckMate-141 | 5.1 |
| IND-HNSCC-RM-2L-NIVOLUMAB | median_os_nivolumab_months | cited | trial-number resolved: CheckMate-141 | 7.5 |
| IND-HNSCC-RM-2L-NIVOLUMAB | one_year_os | cited | trial-number resolved: CheckMate-141 | 36% (vs 16.6% comparator) |
| IND-HNSCC-RM-2L-NIVOLUMAB | os_hr | cited | trial-number resolved: CheckMate-141 | 0.7 |
| IND-HNSCC-RM-2L-NIVOLUMAB | overall_response_rate | cited | trial-number resolved: CheckMate-141 | 13.3% (vs 5.8% comparator) |
| IND-HNSCC-RM-2L-NIVOLUMAB | pdl1_pos_os_hr | cited | trial-number resolved: CheckMate-141 | 0.55 |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | cps_ge1_os_hr | cited | trial-number resolved: KEYNOTE-040 | 0.74 |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | cps_ge20_os_hr | cited | trial-number resolved: KEYNOTE-040 | 0.53 |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | median_os_comparator_months | cited | trial-number resolved: KEYNOTE-040 | 6.9 |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | median_os_pembro_months | cited | trial-number resolved: KEYNOTE-040 | 8.4 |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | orr_pembro | cited | trial-number resolved: KEYNOTE-040 | 14.6% |
| IND-HNSCC-RM-2L-PEMBROLIZUMAB | os_hr | cited | trial-number resolved: KEYNOTE-040 | 0.8 |

## `DIS-HSTCL` — Hepatosplenic T-Cell Lymphoma

Indications: 2; populated: 8; cited: 0; probably-cited: 0; uncited: 8; absent: 2; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-HSTCL-1L-CHOEP-UNFIT | complete_response | uncited | — | ~15-20% |
| IND-HSTCL-1L-CHOEP-UNFIT | overall_response_rate | uncited | — | ~30-40% (anthracycline-based regimens largely ineffective in HSTCL) |
| IND-HSTCL-1L-CHOEP-UNFIT | overall_survival_5y | uncited | — | <10% — anthracycline-based regimens consistently inferior to platinum/AraC-based |
| IND-HSTCL-1L-CHOEP-UNFIT | progression_free_survival | uncited | — | Median PFS ~6-9 months |
| IND-HSTCL-1L-ICE-ALLOSCT | complete_response | uncited | — | ~30-40% |
| IND-HSTCL-1L-ICE-ALLOSCT | overall_response_rate | uncited | — | ~50-60% |
| IND-HSTCL-1L-ICE-ALLOSCT | overall_survival_5y | uncited | — | ~10% chemo-only; ~30-40% з allo-SCT у CR1 |
| IND-HSTCL-1L-ICE-ALLOSCT | progression_free_survival | uncited | — | Median ~12 months chemo-only; ~36 months з allo-SCT |

## `DIS-IFS` — Infantile fibrosarcoma (IFS)

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-IMT` — Inflammatory myofibroblastic tumor (IMT)

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-MASTOCYTOSIS` — Advanced systemic mastocytosis (AdvSM)

Indications: 2; populated: 6; cited: 0; probably-cited: 0; uncited: 6; absent: 4; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ADVSM-1L-AVAPRITINIB | overall_response_rate | uncited | — | ~75% (PATHFINDER advanced SM) |
| IND-ADVSM-1L-AVAPRITINIB | overall_survival_5y | uncited | — | ASM ~70% at 24 mo (vs historical ~50%); SM-AHN and MCL with concomitant AHN-directed therapy |
| IND-ADVSM-1L-AVAPRITINIB | progression_free_survival | uncited | — | Median not reached (PATHFINDER 24-mo follow-up) |
| IND-ADVSM-1L-MIDOSTAURIN | overall_response_rate | uncited | — | ~28% (Valent/Cheson criteria); ~60% (IWG-MRT-ECNM-modified); D-RIVE |
| IND-ADVSM-1L-MIDOSTAURIN | overall_survival_5y | uncited | — | ASM ~26 mo median OS; SM-AHN ~21 mo; MCL ~9 mo (D-RIVE long-term) |
| IND-ADVSM-1L-MIDOSTAURIN | progression_free_survival | uncited | — | Not formally reported in advanced-SM trial |

## `DIS-MCL` — Mantle Cell Lymphoma

Indications: 7; populated: 28; cited: 3; probably-cited: 2; uncited: 23; absent: 7; outcomes-cited % (loose): 17.9%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MCL-1L-BTKI-R | complete_response | uncited | — | ~50% |
| IND-MCL-1L-BTKI-R | overall_response_rate | uncited | — | ~85-90% |
| IND-MCL-1L-BTKI-R | overall_survival_5y | uncited | — | ~70% |
| IND-MCL-1L-BTKI-R | progression_free_survival | uncited | — | Median PFS ~3-5 years (longer in TP53-wt subset) |
| IND-MCL-1L-INTENSIVE | complete_response | uncited | — | ~60-70% post-induction; ~85% post-autoSCT |
| IND-MCL-1L-INTENSIVE | overall_response_rate | uncited | — | ~95% |
| IND-MCL-1L-INTENSIVE | overall_survival_5y | uncited | — | ~70-80% fit-younger cohort |
| IND-MCL-1L-INTENSIVE | progression_free_survival | uncited | — | Median PFS ~7-8 years |
| IND-MCL-2L-ACALABRUTINIB | complete_response | uncited | — | ~40% |
| IND-MCL-2L-ACALABRUTINIB | overall_response_rate | uncited | — | ~81% (ACE-LY-004) |
| IND-MCL-2L-ACALABRUTINIB | overall_survival_5y | uncited | — | ~50-60% |
| IND-MCL-2L-ACALABRUTINIB | progression_free_survival | uncited | — | Median PFS ~22 mo; mDOR ~26 mo (ACE-LY-004 long-term) |
| IND-MCL-3L-BREXUCEL-CART | complete_response | uncited | — | ~68% |
| IND-MCL-3L-BREXUCEL-CART | overall_response_rate | cited | trial-number resolved: ZUMA-2 | ~91% (ZUMA-2) |
| IND-MCL-3L-BREXUCEL-CART | overall_survival_5y | cited | trial-number resolved: ZUMA-2 | ~40-50% (3-yr OS ~60% per ZUMA-2; mature 5-yr maturing) |
| IND-MCL-3L-BREXUCEL-CART | progression_free_survival | cited | trial-number resolved: ZUMA-2 | Median PFS ~25 mo (ZUMA-2 3-yr update); ~37% PFS at 3y |
| IND-MCL-3L-LISOCEL | complete_response | uncited | — | ~72% |
| IND-MCL-3L-LISOCEL | overall_response_rate | probably-cited | trial-number unresolved: TRANSCEND | ~83% (TRANSCEND NHL-001 MCL cohort, n≈88 evaluable) |
| IND-MCL-3L-LISOCEL | overall_survival_5y | uncited | — | 12-month OS ~74%; long-term follow-up ongoing |
| IND-MCL-3L-LISOCEL | progression_free_survival | uncited | — | Median PFS ~15-16 months; durable responses ~50% at 12 months |
| IND-MCL-3L-PIRTOBRUTINIB | complete_response | uncited | — | ~13% |
| IND-MCL-3L-PIRTOBRUTINIB | overall_response_rate | probably-cited | trial-number unresolved: BRUIN | ~50% (BRUIN MCL cohort) |
| IND-MCL-3L-PIRTOBRUTINIB | overall_survival_5y | uncited | — | Mature OS data still maturing; 18-mo OS ~67% |
| IND-MCL-3L-PIRTOBRUTINIB | progression_free_survival | uncited | — | Median PFS ~7.4 mo; mDOR ~17.6 mo |
| IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | complete_response | uncited | — | N/A (maintenance phase) |
| IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | overall_response_rate | uncited | — | Maintenance — measured by PFS + OS extension |
| IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | overall_survival_5y | uncited | — | Post-autoSCT (LyMa): 4-yr OS 89% maintenance vs 80% observation |
| IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE | progression_free_survival | uncited | — | Post-autoSCT (LyMa): 4-yr PFS 83% maintenance vs 64% observation |

## `DIS-MDS-HR` — Myelodysplastic Syndromes — Higher-Risk (IPSS-R high / very high; includes MDS-EB)

Indications: 3; populated: 12; cited: 1; probably-cited: 0; uncited: 11; absent: 3; outcomes-cited % (loose): 8.3%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MDS-HR-1L-AZA | complete_response | uncited | — | CR ~17% (AZA-001) |
| IND-MDS-HR-1L-AZA | overall_response_rate | uncited | — | ~50% complete + partial response (azacitidine; AZA-001 trial) |
| IND-MDS-HR-1L-AZA | overall_survival_5y | uncited | — | ~10-15% (HR-MDS without alloHCT); ~40-50% with alloHCT bridging |
| IND-MDS-HR-1L-AZA | progression_free_survival | uncited | — | Median ~21 months (AZA-001 vs ~15 mo conventional care) |
| IND-MDS-HR-1L-VEN-AZA | complete_response | uncited | — | Higher CR rates than aza alone in series; durability + OS benefit not yet phase-3 confirmed |
| IND-MDS-HR-1L-VEN-AZA | overall_response_rate | cited | trial-number resolved: VIALE-A | ~50-70% composite CR + CRi (extrapolated from VIALE-A AML; small phase-2 HR-MDS series; no phase-3 yet) |
| IND-MDS-HR-1L-VEN-AZA | overall_survival_5y | uncited | — | Insufficient data for HR-MDS-specific 5-y; alloHCT bridging is the path to long-term survival |
| IND-MDS-HR-1L-VEN-AZA | progression_free_survival | uncited | — | Median PFS ~12-15 months in early studies |
| IND-MDS-HR-ALLOHCT | complete_response | uncited | — | Durable molecular CR ~40-60% at 5 years for MDS-HR with optimal pre-HCT control |
| IND-MDS-HR-ALLOHCT | overall_response_rate | uncited | — | ~70-90% achieve disease control post-HCT (variable by pre-HCT blast burden) |
| IND-MDS-HR-ALLOHCT | overall_survival_5y | uncited | — | 5-y OS 40-50% MDS-HR overall; substantially better than non-transplant (~10-15% 5-y OS) |
| IND-MDS-HR-ALLOHCT | progression_free_survival | uncited | — | 5-y PFS 35-50% for MDS-HR overall; 50-60% for IPSS-R high; 25-35% for very high; ~20-30% for TP53-mutated |

## `DIS-MDS-LR` — Myelodysplastic Syndromes — Lower-Risk (IPSS-R very low / low / intermediate)

Indications: 4; populated: 16; cited: 1; probably-cited: 0; uncited: 15; absent: 4; outcomes-cited % (loose): 6.2%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MDS-LR-1L-ESA | complete_response | uncited | — | Transfusion independence ~30-40% |
| IND-MDS-LR-1L-ESA | overall_response_rate | uncited | — | ~50-60% Hb response in selected MDS-LR (endogenous EPO ≤500 mU/mL + RBC TD ≤2U/month) |
| IND-MDS-LR-1L-ESA | overall_survival_5y | uncited | — | Per IPSS-R: VL ~80%; L ~50-60%; Int ~30-40% |
| IND-MDS-LR-1L-ESA | progression_free_survival | uncited | — | Cytopenia management; does not alter MDS natural history |
| IND-MDS-LR-1L-LUSPATERCEPT | complete_response | uncited | — | Transfusion independence ~50-60% |
| IND-MDS-LR-1L-LUSPATERCEPT | overall_response_rate | cited | trial-number resolved: COMMANDS | ~58% RBC transfusion independence ≥12 wk in COMMANDS (vs 31% ESA); ~38% TI ≥8 wk in MEDALIST 2L |
| IND-MDS-LR-1L-LUSPATERCEPT | overall_survival_5y | uncited | — | Per IPSS-R baseline |
| IND-MDS-LR-1L-LUSPATERCEPT | progression_free_survival | uncited | — | Cytopenia management; does not alter natural history |
| IND-MDS-LR-2L-IMETELSTAT | complete_response | uncited | — | Sustained 24-week TI ~28% (vs 3.3% placebo) |
| IND-MDS-LR-2L-IMETELSTAT | overall_response_rate | uncited | — | 8-week RBC TI ~39.8% (IMerge; vs 15.0% placebo, p<0.001) |
| IND-MDS-LR-2L-IMETELSTAT | overall_survival_5y | uncited | — | Per IPSS-R / IPSS-M baseline; OS not significantly altered (cytopenia management indication) |
| IND-MDS-LR-2L-IMETELSTAT | progression_free_survival | uncited | — | Cytopenia management; does not alter natural history; median TI duration ~52 weeks for responders |
| IND-MDS-LR-LENALIDOMIDE-DEL5Q | complete_response | uncited | — | ~20-25% achieve cytogenetic CR (loss of del(5q) clone) |
| IND-MDS-LR-LENALIDOMIDE-DEL5Q | overall_response_rate | uncited | — | ~56% RBC TI at 26 weeks (MDS-004; vs 5.9% placebo) |
| IND-MDS-LR-LENALIDOMIDE-DEL5Q | overall_survival_5y | uncited | — | Per IPSS-R baseline; lenalidomide does not alter natural history but improves QoL via TI |
| IND-MDS-LR-LENALIDOMIDE-DEL5Q | progression_free_survival | uncited | — | Median TI duration >2 years per MDS-004 |

## `DIS-MELANOMA` — Cutaneous melanoma

Indications: 11; populated: 37; cited: 9; probably-cited: 0; uncited: 28; absent: 20; outcomes-cited % (loose): 24.3%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MELANOMA-2L-KIT-IMATINIB | complete_response | uncited | — | low single-digit % |
| IND-MELANOMA-2L-KIT-IMATINIB | overall_response_rate | uncited | — | 23% (Carvajal 2011, KIT-mutant cohort) |
| IND-MELANOMA-2L-KIT-IMATINIB | overall_survival_5y | uncited | — | Limited mature data; durable responders reported |
| IND-MELANOMA-2L-KIT-IMATINIB | progression_free_survival | uncited | — | Median PFS ~3.5 mo overall; durable responses (>1 year) in subset with exon 11/13 hotspot mutations |
| IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO | complete_response | uncited | — | ~22% |
| IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO | overall_response_rate | cited | trial-number resolved: CheckMate-067 | ~58% (CheckMate-067 in 1L; lower in 2L post-targeted) |
| IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO | overall_survival_5y | cited | trial-number resolved: CheckMate-067 | 5-y OS 52% (CheckMate-067 1L) |
| IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO | progression_free_survival | cited | trial-number resolved: CheckMate-067 | Median PFS 11.5 mo (CheckMate-067 1L); shorter in 2L post-BRAFi cohorts |
| IND-MELANOMA-2L-POST-IO-BRAFI-MEKI | complete_response | uncited | — | ~8% |
| IND-MELANOMA-2L-POST-IO-BRAFI-MEKI | overall_response_rate | uncited | — | ~64% (COLUMBUS, encorafenib+binimetinib) |
| IND-MELANOMA-2L-POST-IO-BRAFI-MEKI | overall_survival_5y | uncited | — | 5-y OS 35% (encorafenib+binimetinib arm; mOS 33.6 mo) |
| IND-MELANOMA-2L-POST-IO-BRAFI-MEKI | progression_free_survival | uncited | — | Median PFS 14.9 mo (vs 7.3 mo vemurafenib) |
| IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB | complete_response | uncited | — | ~16% |
| IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB | overall_response_rate | uncited | — | ~43% (RELATIVITY-047 1L) |
| IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB | overall_survival_5y | uncited | — | 4-y OS ~48% (RELATIVITY-047) |
| IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB | progression_free_survival | uncited | — | Median PFS 10.1 mo (vs 4.6 mo nivo mono; HR 0.75) |
| IND-MELANOMA-3L-LIFILEUCEL | complete_response | uncited | — | ~9% |
| IND-MELANOMA-3L-LIFILEUCEL | overall_response_rate | uncited | — | 31.4% (C-144-01 pooled, n=153) |
| IND-MELANOMA-3L-LIFILEUCEL | overall_survival_5y | uncited | — | mOS 13.9 mo overall; durable plateau ~25-30% among responders |
| IND-MELANOMA-3L-LIFILEUCEL | progression_free_survival | uncited | — | Median PFS 4.1 mo overall; mDoR not reached at 27.6 mo follow-up among responders |
| IND-MELANOMA-3L-POST-LIFILEUCEL | complete_response | uncited | — | rare |
| IND-MELANOMA-3L-POST-LIFILEUCEL | overall_response_rate | uncited | — | <15% with empirical chemo (dacarbazine, temozolomide, paclitaxel) |
| IND-MELANOMA-3L-POST-LIFILEUCEL | overall_survival_5y | uncited | — | Salvage; mOS 4-8 mo from 4L initiation |
| IND-MELANOMA-3L-POST-LIFILEUCEL | progression_free_survival | uncited | — | Median PFS 1.5-3 mo |
| IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III | overall_response_rate | uncited | — | N/A — adjuvant disease-free setting (microscopic / no measurable disease) |
| IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III | overall_survival_5y | cited | trial-number resolved: KEYNOTE-054 | 5-yr OS data still maturing per KEYNOTE-054 long-term follow-up; OS benefit not yet formally demonstrated, but RFS ma... |
| IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III | progression_free_survival | uncited | — | 12-mo RFS 75.4% vs 61.0% placebo (HR 0.57); 5-yr RFS 55.4% vs 38.3% (HR 0.61) |
| IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME | median_progression_free_survival_months | uncited | — | 12 |
| IND-MELANOMA-METASTATIC-1L-NIVO-IPI | five_year_overall_survival | cited | trial-number resolved: CheckMate-067 | 52% |
| IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO | complete_response | uncited | — | ~13-14% |
| IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO | overall_response_rate | cited | trial-number resolved: KEYNOTE-006 | ~33-42% (KEYNOTE-006 pembro Q2W / Q3W arms) |
| IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO | overall_survival_5y | uncited | — | 5-yr OS ~38-39% pembro vs ~31% ipi; 7-yr OS ~37% vs ~25% |
| IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO | progression_free_survival | uncited | — | Median PFS ~8.4 mo (Q2W) / 5.5 mo (Q3W); 6-mo PFS 47% (vs 26% ipi) |
| IND-MELANOMA-NIVO-MAINT | complete_response | uncited | — | ~22% landmark |
| IND-MELANOMA-NIVO-MAINT | overall_response_rate | cited | trial-number resolved: CheckMate-067 | ~58% during induction phase (CheckMate-067) |
| IND-MELANOMA-NIVO-MAINT | overall_survival_5y | cited | trial-number resolved: CheckMate-067 | 5-yr OS 52% nivo+ipi vs 44% nivo mono vs 26% ipi mono (CheckMate-067) |
| IND-MELANOMA-NIVO-MAINT | progression_free_survival | cited | trial-number resolved: CheckMate-067 | Median PFS 11.5 mo for nivo+ipi (CheckMate-067; Larkin 2019 NEJM 5-yr update) |

## `DIS-MESOTHELIOMA` — Malignant pleural mesothelioma (MPM)

Indications: 2; populated: 7; cited: 2; probably-cited: 0; uncited: 5; absent: 4; outcomes-cited % (loose): 28.6%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MESOTHELIOMA-1L-NIVO-IPI | complete_response | uncited | — | ~5% |
| IND-MESOTHELIOMA-1L-NIVO-IPI | overall_response_rate | cited | trial-number resolved: CheckMate-743 | ~40% ORR (CheckMate-743; modified RECIST) |
| IND-MESOTHELIOMA-1L-NIVO-IPI | overall_survival_5y | cited | trial-number resolved: CheckMate-743 | "Median OS 18.1 mo vs 14.1 mo chemo (HR 0.74, 95% CI 0.60–0.91, p=0.005, CheckMate-743); 2-year OS 41% vs 27%; Non-ep... |
| IND-MESOTHELIOMA-1L-NIVO-IPI | progression_free_survival | uncited | — | Median PFS 6.8 mo vs 7.2 mo chemo (not superior); durable responses in responders |
| IND-MESOTHELIOMA-1L-PEMETREXED-PLATINUM | overall_response_rate | uncited | — | ~41% (EMPHACIS, pemetrexed+cisplatin vs 17% cisplatin alone) |
| IND-MESOTHELIOMA-1L-PEMETREXED-PLATINUM | overall_survival | uncited | — | ~12.1 months (EMPHACIS); 13.3 months in fully vitamin-supplemented patients |
| IND-MESOTHELIOMA-1L-PEMETREXED-PLATINUM | progression_free_survival | uncited | — | ~5.7 months |

## `DIS-MF-SEZARY` — Mycosis Fungoides / Sézary Syndrome

Indications: 5; populated: 20; cited: 0; probably-cited: 0; uncited: 20; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MF-ADVANCED-1L-BV | complete_response | uncited | — | ~16% (ALCANZA) |
| IND-MF-ADVANCED-1L-BV | overall_response_rate | uncited | — | ~67% ORR4 (ALCANZA — sustained ≥4 months); single-agent |
| IND-MF-ADVANCED-1L-BV | overall_survival_5y | uncited | — | ~75-80% mature data |
| IND-MF-ADVANCED-1L-BV | progression_free_survival | uncited | — | Median PFS ~16.7 months (ALCANZA) |
| IND-MF-ADVANCED-1L-MOGA | complete_response | uncited | — | ~5% globally; higher in blood compartment ~30-40% |
| IND-MF-ADVANCED-1L-MOGA | overall_response_rate | uncited | — | ~28% (MAVORIC, r/r setting; 1L higher in real-world) |
| IND-MF-ADVANCED-1L-MOGA | overall_survival_5y | uncited | — | Improvements vs vorinostat era; mature data accumulating |
| IND-MF-ADVANCED-1L-MOGA | progression_free_survival | uncited | — | Median PFS ~7.7 months (MAVORIC); higher in B2 / Sézary |
| IND-MF-ADVANCED-2L-BEXAROTENE | complete_response | uncited | — | ~10% |
| IND-MF-ADVANCED-2L-BEXAROTENE | overall_response_rate | uncited | — | ~45-55% (Duvic 2001 r/r CTCL all stages) |
| IND-MF-ADVANCED-2L-BEXAROTENE | overall_survival_5y | uncited | — | Highly variable — chronic disease; many continue indefinitely on maintenance |
| IND-MF-ADVANCED-2L-BEXAROTENE | progression_free_survival | uncited | — | Median PFS ~9-12 months in responders |
| IND-MF-EARLY-1L-SKIN-DIRECTED | complete_response | uncited | — | ~50-70% (varies by modality + extent) |
| IND-MF-EARLY-1L-SKIN-DIRECTED | overall_response_rate | uncited | — | ~80-90% (skin-directed for IA-IIA) |
| IND-MF-EARLY-1L-SKIN-DIRECTED | overall_survival_5y | uncited | — | >90% IA; ~85% IIA |
| IND-MF-EARLY-1L-SKIN-DIRECTED | progression_free_survival | uncited | — | Median PFS years; many never progress past skin-directed era |
| IND-MF-MAINTENANCE-RETINOID | complete_response | uncited | — | Sustains; rare deepening |
| IND-MF-MAINTENANCE-RETINOID | overall_response_rate | uncited | — | Maintenance setting — extends pre-existing CR/PR |
| IND-MF-MAINTENANCE-RETINOID | overall_survival_5y | uncited | — | Highly variable — chronic disease; many continue indefinitely on maintenance |
| IND-MF-MAINTENANCE-RETINOID | progression_free_survival | uncited | — | Extends median PFS by ~6-12 months over surveillance in responders |

## `DIS-MM` — Multiple Myeloma

Indications: 13; populated: 52; cited: 3; probably-cited: 12; uncited: 37; absent: 19; outcomes-cited % (loose): 28.8%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MM-1L-DVRD | complete_response | probably-cited | trial-number unresolved: PERSEUS | ~50-65% post-induction; ~70-80% post-ASCT consolidation (PERSEUS) |
| IND-MM-1L-DVRD | overall_response_rate | probably-cited | trial-number unresolved: PERSEUS | ~98-100% (≥PR after 4 cycles per PERSEUS) |
| IND-MM-1L-DVRD | overall_survival_5y | uncited | — | >80% (mature OS data still maturing) |
| IND-MM-1L-DVRD | progression_free_survival | probably-cited | trial-number unresolved: PERSEUS | Estimated 4-year PFS ~84% transplant-eligible (PERSEUS); HR ~0.42 vs VRd |
| IND-MM-1L-VRD | complete_response | uncited | — | ~30-40% post-induction; ~50-60% post-ASCT consolidation |
| IND-MM-1L-VRD | overall_response_rate | uncited | — | ~95-98% (≥PR after 4 cycles) |
| IND-MM-1L-VRD | overall_survival_5y | uncited | — | ~70-75% transplant-eligible |
| IND-MM-1L-VRD | progression_free_survival | uncited | — | Median ~50-60 months (transplant-eligible with ASCT + maintenance); ~43 months transplant-ineligible (SWOG S0777) |
| IND-MM-2L-DKD | complete_response | uncited | — | ~29% sCR / CR |
| IND-MM-2L-DKD | overall_response_rate | uncited | — | ~84% (CANDOR) |
| IND-MM-2L-DKD | overall_survival_5y | uncited | — | Mature OS data still maturing; OS HR 0.78 favoring DKd at 3-year follow-up |
| IND-MM-2L-DKD | progression_free_survival | uncited | — | Median PFS ~28.6 mo (vs 15.2 mo Kd; HR 0.59) |
| IND-MM-4L-CILTACEL-CART | complete_response | uncited | — | ~83% sCR / CR |
| IND-MM-4L-CILTACEL-CART | overall_response_rate | probably-cited | trial-number unresolved: CARTITUDE-1 | ~98% (CARTITUDE-1 Berdeja 2021 Lancet; Martin 2023 update) |
| IND-MM-4L-CILTACEL-CART | overall_survival_5y | probably-cited | trial-number unresolved: CARTITUDE-1 | ~74% 30-mo OS landmark (CARTITUDE-1) |
| IND-MM-4L-CILTACEL-CART | progression_free_survival | probably-cited | trial-number unresolved: CARTITUDE-1 | Median PFS ~35 mo (CARTITUDE-1 Martin 2023 JCO 3-yr update) |
| IND-MM-4L-TECLISTAMAB | complete_response | uncited | — | ~39% sCR / CR |
| IND-MM-4L-TECLISTAMAB | overall_response_rate | uncited | — | ~63% (MajesTEC-1) |
| IND-MM-4L-TECLISTAMAB | overall_survival_5y | uncited | — | Median OS ~22 mo (mature follow-up) |
| IND-MM-4L-TECLISTAMAB | progression_free_survival | uncited | — | Median PFS ~11 mo |
| IND-MM-ELDERLY-FRAIL-VRD-LIGHT | complete_response | uncited | — | ~25% |
| IND-MM-ELDERLY-FRAIL-VRD-LIGHT | overall_response_rate | uncited | — | ~80% (VRD-lite O'Donnell 2018 BJH; Gay 2017 Lancet Oncol) |
| IND-MM-ELDERLY-FRAIL-VRD-LIGHT | overall_survival_5y | uncited | — | 5-yr OS ~65% (extrapolated; VRD-lite cohorts have better tolerability than full-dose VRD in elderly) |
| IND-MM-ELDERLY-FRAIL-VRD-LIGHT | progression_free_survival | uncited | — | Median PFS ~35 mo (VRD-lite O'Donnell) |
| IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE | complete_response | uncited | — | MRD-negativity conversion in ~25-35% during first 24 months |
| IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE | overall_response_rate | uncited | — | Maintenance — measured by depth deepening (~30% achieve ≥CR with maintenance vs without) |
| IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE | overall_survival_5y | uncited | — | Median OS 113 mo (vs 84 mo placebo, HR 0.72) |
| IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE | progression_free_survival | uncited | — | Median PFS 46 mo (vs 27 mo placebo, CALGB 100104) |
| IND-MM-RR-2L-CILTACEL | complete_response | uncited | — | ~73% sCR / CR (cilta-cel arm) |
| IND-MM-RR-2L-CILTACEL | overall_response_rate | probably-cited | trial-number unresolved: CARTITUDE-4 | ~85% (CARTITUDE-4; San-Miguel 2023 NEJM) |
| IND-MM-RR-2L-CILTACEL | overall_survival_median | probably-cited | trial-number unresolved: CARTITUDE-4 | Not Reached at 16-mo median follow-up (CARTITUDE-4); OS HR favours cilta-cel |
| IND-MM-RR-2L-CILTACEL | progression_free_survival | probably-cited | trial-number unresolved: CARTITUDE-4 | Median PFS Not Reached vs 11.8 mo SOC (HR 0.26; CARTITUDE-4) |
| IND-MM-RR-3L-CILTACEL | complete_response | uncited | — | ~83% sCR / CR |
| IND-MM-RR-3L-CILTACEL | overall_response_rate | cited | trial-number resolved: CARTITUDE-1 | ~98% (CARTITUDE-1; Berdeja 2021 Lancet, Martin 2023 JCO 3-yr update) |
| IND-MM-RR-3L-CILTACEL | overall_survival_median | cited | trial-number resolved: CARTITUDE-1 | 30-mo OS landmark ~74% (CARTITUDE-1) |
| IND-MM-RR-3L-CILTACEL | progression_free_survival | cited | trial-number resolved: CARTITUDE-1 | Median PFS ~35 mo (CARTITUDE-1 Martin 2023 JCO 3-yr update) |
| IND-MM-RR-3L-ELRANATAMAB | complete_response | uncited | — | ~35% sCR / CR |
| IND-MM-RR-3L-ELRANATAMAB | overall_response_rate | uncited | — | ~61% (MagnetisMM-3 BCMA-naive cohort A; Lesokhin 2023 Nat Med) |
| IND-MM-RR-3L-ELRANATAMAB | overall_survival_median | uncited | — | Median OS ~24+ mo (immature follow-up) |
| IND-MM-RR-3L-ELRANATAMAB | progression_free_survival | uncited | — | Median PFS ~17.2 mo (longer-term update; not yet mature) |
| IND-MM-RR-3L-IDECEL | complete_response | uncited | — | ~33% sCR / CR |
| IND-MM-RR-3L-IDECEL | overall_response_rate | probably-cited | trial-family: KarMMa | ~73% (KarMMa pivotal; Munshi 2021 NEJM) |
| IND-MM-RR-3L-IDECEL | overall_survival_median | probably-cited | trial-family: KarMMa | Median OS ~24.8 mo (KarMMa) |
| IND-MM-RR-3L-IDECEL | progression_free_survival | probably-cited | trial-number unresolved: KarMMa-3 | Median PFS ~12.1 mo (KarMMa); ~13.3 mo (KarMMa-3 update) |
| IND-MM-RR-3L-TALQUETAMAB | complete_response | uncited | — | ~33% sCR / CR |
| IND-MM-RR-3L-TALQUETAMAB | overall_response_rate | uncited | — | ~73% (MonumenTAL-1 QW 0.4 mg/kg + Q2W 0.8 mg/kg pooled; Chari 2022 NEJM) |
| IND-MM-RR-3L-TALQUETAMAB | overall_survival_median | uncited | — | Median OS ~22 mo (immature; differs by schedule) |
| IND-MM-RR-3L-TALQUETAMAB | progression_free_survival | uncited | — | Median PFS ~7.5 mo (QW); ~11.9 mo (Q2W cohort) |
| IND-MM-RR-3L-TECLISTAMAB | complete_response | uncited | — | ~39% sCR / CR |
| IND-MM-RR-3L-TECLISTAMAB | overall_response_rate | uncited | — | ~63% (MajesTEC-1; Moreau 2022 NEJM) |
| IND-MM-RR-3L-TECLISTAMAB | overall_survival_median | uncited | — | Median OS ~22 mo (mature follow-up) |
| IND-MM-RR-3L-TECLISTAMAB | progression_free_survival | uncited | — | Median PFS ~11.3 mo |

## `DIS-MPNST` — Malignant peripheral nerve sheath tumor (MPNST)

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-MTC` — Medullary thyroid carcinoma (MTC)

Indications: 2; populated: 6; cited: 3; probably-cited: 0; uncited: 3; absent: 4; outcomes-cited % (loose): 50.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-MTC-ADVANCED-1L-CABOZANTINIB-RET-WT | overall_response_rate | uncited | — | ~28% (EXAM) |
| IND-MTC-ADVANCED-1L-CABOZANTINIB-RET-WT | overall_survival_5y | uncited | — | OS benefit limited to RET M918T subgroup (HR 0.60); overall ITT not significant |
| IND-MTC-ADVANCED-1L-CABOZANTINIB-RET-WT | progression_free_survival | uncited | — | Median 11.2 mo vs 4.0 mo placebo (EXAM) |
| IND-MTC-ADVANCED-1L-SELPERCATINIB | overall_response_rate | cited | trial-number resolved: LIBRETTO-531 | ~73% (LIBRETTO-001 RET-mutant MTC); ~69% (LIBRETTO-531 1L) |
| IND-MTC-ADVANCED-1L-SELPERCATINIB | overall_survival_5y | cited | trial-number resolved: LIBRETTO-531 | Not yet mature; PFS at 24 mo ~73% |
| IND-MTC-ADVANCED-1L-SELPERCATINIB | progression_free_survival | cited | trial-number resolved: LIBRETTO-531 | Median not reached at 24 mo follow-up (LIBRETTO-531) |

## `DIS-NK-T-NASAL` — Extranodal NK/T-Cell Lymphoma, Nasal Type

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-NK-T-NASAL-1L-P-GEMOX | complete_response | uncited | — | ~50% |
| IND-NK-T-NASAL-1L-P-GEMOX | overall_response_rate | uncited | — | ~80% (Wang 2013, comparable to SMILE) |
| IND-NK-T-NASAL-1L-P-GEMOX | overall_survival_5y | uncited | — | ~70% localized; ~40% disseminated |
| IND-NK-T-NASAL-1L-P-GEMOX | progression_free_survival | uncited | — | 5-year PFS ~70% (localized stage I/II); ~30-40% (disseminated) |
| IND-NK-T-NASAL-1L-SMILE | complete_response | uncited | — | ~50-70% (localized); ~30-40% (disseminated) |
| IND-NK-T-NASAL-1L-SMILE | overall_response_rate | uncited | — | ~80% (localized); ~60% (disseminated) |
| IND-NK-T-NASAL-1L-SMILE | overall_survival_5y | uncited | — | ~70% localized; ~40% disseminated |
| IND-NK-T-NASAL-1L-SMILE | progression_free_survival | uncited | — | 5-year PFS ~70% (localized stage I/II); ~30% (disseminated) |
| IND-NK-T-NASAL-2L-AVELUMAB | complete_response | uncited | — | ~24% |
| IND-NK-T-NASAL-2L-AVELUMAB | overall_response_rate | uncited | — | ~38% (Kim 2020 phase 2 r/r NK/T-NL) |
| IND-NK-T-NASAL-2L-AVELUMAB | overall_survival_5y | uncited | — | <10% chemo-only; ~25-30% if successful bridge to alloSCT |
| IND-NK-T-NASAL-2L-AVELUMAB | progression_free_survival | uncited | — | Median PFS ~3-4 months without consolidation; sustained only with alloSCT in CR |

## `DIS-NLPBL` — Nodular Lymphocyte-Predominant B-cell Lymphoma (formerly NLPHL)

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-NLPBL-1L-OBSERVATION-OR-RT | complete_response | uncited | — | ISRT ~90% |
| IND-NLPBL-1L-OBSERVATION-OR-RT | overall_response_rate | uncited | — | ISRT ~95% |
| IND-NLPBL-1L-OBSERVATION-OR-RT | overall_survival_5y | uncited | — | >95% early-stage |
| IND-NLPBL-1L-OBSERVATION-OR-RT | progression_free_survival | uncited | — | 10y PFS ~85% with ISRT alone for early stage |
| IND-NLPBL-1L-RITUXIMAB-MONO | complete_response | uncited | — | ~50-70% |
| IND-NLPBL-1L-RITUXIMAB-MONO | overall_response_rate | uncited | — | ~75-85% (single-agent rituximab in NLPBL) |
| IND-NLPBL-1L-RITUXIMAB-MONO | overall_survival_5y | uncited | — | >90% (NLPBL indolent biology preserved) |
| IND-NLPBL-1L-RITUXIMAB-MONO | progression_free_survival | uncited | — | Median PFS ~3-5 years; relapse-prone but salvageable |
| IND-NLPBL-2L-RCHOP-TRANSFORMATION | complete_response | uncited | — | ~65-70% |
| IND-NLPBL-2L-RCHOP-TRANSFORMATION | overall_response_rate | uncited | — | ~85% (R-CHOP for transformed/aggressive B-NHL) |
| IND-NLPBL-2L-RCHOP-TRANSFORMATION | overall_survival_5y | uncited | — | ~70-80% |
| IND-NLPBL-2L-RCHOP-TRANSFORMATION | progression_free_survival | uncited | — | 5-year PFS ~50-60% for transformed NLPBL post-R-CHOP |

## `DIS-NODAL-MZL` — Nodal Marginal Zone Lymphoma

Indications: 4; populated: 15; cited: 0; probably-cited: 0; uncited: 15; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-NMZL-1L-BR | complete_response | uncited | — | ~50% |
| IND-NMZL-1L-BR | overall_response_rate | uncited | — | ~90% |
| IND-NMZL-1L-BR | overall_survival_5y | uncited | — | ~85% |
| IND-NMZL-1L-BR | progression_free_survival | uncited | — | Median PFS ~5-7 years |
| IND-NMZL-1L-HCV-POSITIVE | hcv_cure_rate_svr12 | uncited | — | >95% (non-cirrhotic, treatment-naive) |
| IND-NMZL-1L-HCV-POSITIVE | overall_response_rate | uncited | — | ~40-60% lymphoma regression after SVR12 (smaller series than HCV-MZL extranodal/SMZL) |
| IND-NMZL-1L-HCV-POSITIVE | overall_survival_5y | uncited | — | >80% in non-cirrhotic responders |
| IND-NMZL-1L-HCV-POSITIVE | progression_free_survival | uncited | — | Variable; durable in DAA-responders, otherwise revert to BR |
| IND-NMZL-1L-WATCH | overall_response_rate | uncited | — | N/A — observational |
| IND-NMZL-1L-WATCH | overall_survival_5y | uncited | — | Equivalent to immediate-treatment for low-burden |
| IND-NMZL-1L-WATCH | progression_free_survival | uncited | — | Median time-to-treatment 2-5 years for low-burden cases |
| IND-NMZL-2L-BR | complete_response | uncited | — | ~50-60% |
| IND-NMZL-2L-BR | overall_response_rate | uncited | — | ~85-90% |
| IND-NMZL-2L-BR | overall_survival_5y | uncited | — | ~75-85% |
| IND-NMZL-2L-BR | progression_free_survival | uncited | — | Median PFS ~3-4 years |

## `DIS-OVARIAN` — Ovarian carcinoma (high-grade serous predominant)

Indications: 15; populated: 48; cited: 4; probably-cited: 2; uncited: 42; absent: 27; outcomes-cited % (loose): 12.5%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-OVARIAN-2L-PLAT-RES-MIRVETUXIMAB | overall_response_rate | uncited | — | 42% (MIRASOL vs 16% chemo control) |
| IND-OVARIAN-2L-PLAT-RES-MIRVETUXIMAB | overall_survival_5y | uncited | — | mOS 16.46 vs 12.75 mo (MIRASOL, HR 0.67) — first phase-3 OS win in platinum-resistant ovarian |
| IND-OVARIAN-2L-PLAT-RES-MIRVETUXIMAB | progression_free_survival | uncited | — | mPFS 5.62 vs 3.98 mo (MIRASOL, HR 0.65) |
| IND-OVARIAN-2L-PLAT-RES-PLD-BEV | overall_response_rate | uncited | — | 17.4% (AURELIA PLD+bev arm vs 7.8% PLD alone) |
| IND-OVARIAN-2L-PLAT-RES-PLD-BEV | overall_survival_5y | uncited | — | mOS 16.6 vs 13.3 mo overall AURELIA cohort (HR 0.85, NS) — significant OS benefit in weekly-pacli subgroup specifically |
| IND-OVARIAN-2L-PLAT-RES-PLD-BEV | progression_free_survival | uncited | — | mPFS 5.4 vs 3.5 mo (AURELIA PLD arm, HR 0.57) |
| IND-OVARIAN-2L-PLAT-RES-TOPOTECAN | overall_response_rate | uncited | — | ~7-15% (single-agent in platinum-resistant) |
| IND-OVARIAN-2L-PLAT-RES-TOPOTECAN | overall_survival_5y | uncited | — | mOS ~9-13 mo single-agent in platinum-resistant |
| IND-OVARIAN-2L-PLAT-RES-TOPOTECAN | progression_free_survival | uncited | — | mPFS ~3-4 mo |
| IND-OVARIAN-2L-PLAT-RES-WEEKLY-PAC-BEV | overall_response_rate | uncited | — | 53.3% (AURELIA weekly-pacli+bev arm vs 30.2% pacli alone) |
| IND-OVARIAN-2L-PLAT-RES-WEEKLY-PAC-BEV | overall_survival_5y | uncited | — | mOS 22.4 vs 13.2 mo (AURELIA weekly-pacli subgroup, HR 0.65) — only AURELIA chemo arm with significant OS benefit |
| IND-OVARIAN-2L-PLAT-RES-WEEKLY-PAC-BEV | progression_free_survival | uncited | — | mPFS 10.4 vs 3.9 mo (AURELIA weekly-pacli arm, HR 0.46) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-GEM-BEV | overall_response_rate | uncited | — | 78.5% (OCEANS carbo+gem+bev arm) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-GEM-BEV | overall_survival_5y | uncited | — | mOS 33.3 vs 32.9 mo (OCEANS — OS not significantly improved vs chemo alone) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-GEM-BEV | progression_free_survival | uncited | — | mPFS 12.4 vs 8.4 mo over carbo+gem alone (OCEANS, HR 0.484) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-PLD-BEV | overall_response_rate | uncited | — | ~70-78% (platinum-sensitive re-induction; extrapolated from CALYPSO + GOG-0213) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-PLD-BEV | overall_survival_5y | uncited | — | GOG-0213: mOS 42.2 vs 37.3 mo (HR 0.823, primary endpoint missed by predefined alpha but clinically meaningful) |
| IND-OVARIAN-2L-PLAT-SENS-CARBO-PLD-BEV | progression_free_survival | uncited | — | Median ~13-14 mo with bev-containing platinum-sensitive backbone (GOG-0213) |
| IND-OVARIAN-3L-POST-PARPi-POST-MIRVE | complete_response | uncited | — | rare |
| IND-OVARIAN-3L-POST-PARPi-POST-MIRVE | overall_response_rate | uncited | — | ~10-15% sequential single-agent (pegylated liposomal doxorubicin, weekly paclitaxel, topotecan, gemcitabine, trabecte... |
| IND-OVARIAN-3L-POST-PARPi-POST-MIRVE | overall_survival_5y | uncited | — | Salvage; mOS 12-18 mo from 3L initiation |
| IND-OVARIAN-3L-POST-PARPi-POST-MIRVE | progression_free_survival | uncited | — | Median PFS 3-4 mo per agent |
| IND-OVARIAN-3L-TRABECTEDIN-PLD | overall_response_rate | uncited | — | 27.6% (OVA-301 vs 18.8% PLD alone, p=0.008) |
| IND-OVARIAN-3L-TRABECTEDIN-PLD | overall_survival_5y | uncited | — | Partially-platinum-sensitive subgroup mOS 23.0 vs 17.1 mo (HR 0.59) |
| IND-OVARIAN-3L-TRABECTEDIN-PLD | progression_free_survival | uncited | — | Overall mPFS 7.3 vs 5.8 mo (OVA-301, HR 0.79); partially-platinum-sensitive subgroup 7.4 vs 5.5 mo (HR 0.65) |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG | overall_response_rate | uncited | — | ~70% (induction) |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG | overall_survival_5y | uncited | — | ~30-35% all-comers stage III/IV |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG | progression_free_survival | uncited | — | Median ~10-13 mo without maintenance; +bev maintenance adds 2-4 mo PFS |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP | complete_response | uncited | — | ~50% |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP | overall_response_rate | uncited | — | ~80% (induction) |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP | overall_survival_5y | uncited | — | ~50-60% in HRD+ subset |
| IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP | progression_free_survival | uncited | — | Median ~37 mo with HRD+ + olaparib maintenance (PAOLA-1) |
| IND-OVARIAN-MAINT-BEV | complete_response | uncited | — | N/A (maintenance phase) |
| IND-OVARIAN-MAINT-BEV | overall_response_rate | uncited | — | Maintenance — measured by PFS extension |
| IND-OVARIAN-MAINT-BEV | overall_survival_5y | uncited | — | OS benefit confined to high-risk subgroup (ICON7 mOS 39.7 vs 30.2 mo); no overall OS gain in GOG-218 |
| IND-OVARIAN-MAINT-BEV | progression_free_survival | uncited | — | Median PFS extension ~3.8 mo (GOG-218 Burger 2011 NEJM; mPFS 14.1 vs 10.3 mo); high-risk subgroup gain larger (ICON7 ... |
| IND-OVARIAN-MAINT-PARPI-BRCAM-OLAPARIB | overall_response_rate | uncited | — | Maintenance — measured by PFS not response |
| IND-OVARIAN-MAINT-PARPI-BRCAM-OLAPARIB | overall_survival_5y | cited | trial-number resolved: SOLO2 | mOS 51.7 vs 38.8 mo (SOLO2 long-term update Poveda 2021, HR 0.74) |
| IND-OVARIAN-MAINT-PARPI-BRCAM-OLAPARIB | progression_free_survival | cited | trial-number resolved: SOLO2 | mPFS 19.1 vs 5.5 mo (SOLO2/ENGOT-Ov21, HR 0.30) |
| IND-OVARIAN-MAINT-PARPI-HRD-NIRAPARIB | overall_response_rate | uncited | — | Maintenance — measured by PFS not response |
| IND-OVARIAN-MAINT-PARPI-HRD-NIRAPARIB | overall_survival_5y | uncited | — | OS not significantly improved in NOVA final analysis (Matulonis 2023); benefit cohort-dependent |
| IND-OVARIAN-MAINT-PARPI-HRD-NIRAPARIB | progression_free_survival | uncited | — | Non-gBRCA HRD+ mPFS 12.9 vs 3.8 mo (NOVA, HR 0.38); gBRCA mPFS 21.0 vs 5.5 mo; non-gBRCA all-comers 9.3 vs 3.9 mo |
| IND-OVARIAN-MAINT-PARPI-RUCAPARIB | overall_response_rate | uncited | — | Maintenance — measured by PFS not response |
| IND-OVARIAN-MAINT-PARPI-RUCAPARIB | overall_survival_5y | cited | trial-number resolved: ARIEL3 | ARIEL3 final OS analysis (Coleman 2022) — no significant OS benefit overall, signals in BRCA-mut subset |
| IND-OVARIAN-MAINT-PARPI-RUCAPARIB | progression_free_survival | cited | trial-number resolved: ARIEL3 | BRCA-mut mPFS 16.6 vs 5.4 mo (ARIEL3, HR 0.23); HRD+ 13.6 vs 5.4 mo (HR 0.32); ITT 10.8 vs 5.4 mo (HR 0.36) |
| IND-OVARIAN-MAINTENANCE-OLAPARIB | overall_response_rate | uncited | — | Maintenance — measured by PFS not response |
| IND-OVARIAN-MAINTENANCE-OLAPARIB | overall_survival_5y | probably-cited | trial-family: SOLO | 5-yr OS ~67% SOLO-1 BRCA arm vs 47% placebo |
| IND-OVARIAN-MAINTENANCE-OLAPARIB | progression_free_survival | probably-cited | trial-family: SOLO | mPFS 56 mo SOLO-1 (BRCA-mut); 37 mo PAOLA-1 (HRD+ all) |

## `DIS-PCNSL` — Primary Diffuse Large B-Cell Lymphoma of the CNS

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PCNSL-1L-MATRIX | complete_response | uncited | — | ~50% |
| IND-PCNSL-1L-MATRIX | overall_response_rate | uncited | — | ~87% |
| IND-PCNSL-1L-MATRIX | overall_survival_5y | uncited | — | ~65% |
| IND-PCNSL-1L-MATRIX | progression_free_survival | uncited | — | Median PFS ~36 months (з autoSCT consolidation) |
| IND-PCNSL-1L-R-MPV | complete_response | uncited | — | ~40% |
| IND-PCNSL-1L-R-MPV | overall_response_rate | uncited | — | ~75% |
| IND-PCNSL-1L-R-MPV | overall_survival_5y | uncited | — | ~45% |
| IND-PCNSL-1L-R-MPV | progression_free_survival | uncited | — | Median PFS ~24 months |
| IND-PCNSL-2L-RMPV-SALVAGE | complete_response | uncited | — | ~40-50% |
| IND-PCNSL-2L-RMPV-SALVAGE | overall_response_rate | uncited | — | ~50-70% in chemosensitive late relapse (>12 mo from 1L) |
| IND-PCNSL-2L-RMPV-SALVAGE | overall_survival_5y | uncited | — | ~30-40% |
| IND-PCNSL-2L-RMPV-SALVAGE | progression_free_survival | uncited | — | Median PFS ~12-18 mo; longer with autoSCT consolidation |

## `DIS-PDAC` — Pancreatic ductal adenocarcinoma (PDAC)

Indications: 4; populated: 13; cited: 3; probably-cited: 0; uncited: 10; absent: 7; outcomes-cited % (loose): 23.1%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PDAC-MAINTENANCE-OLAPARIB-BRCA | overall_survival_5y | uncited | — | OS endpoint NS (POLO); ORR maintained 18 vs 9% |
| IND-PDAC-MAINTENANCE-OLAPARIB-BRCA | progression_free_survival | uncited | — | Median 7.4 vs 3.8 mo placebo (POLO) |
| IND-PDAC-METASTATIC-1L-FOLFIRINOX | complete_response | uncited | — | ~5% |
| IND-PDAC-METASTATIC-1L-FOLFIRINOX | overall_response_rate | uncited | — | ~32% |
| IND-PDAC-METASTATIC-1L-FOLFIRINOX | overall_survival_5y | uncited | — | mOS ~11.1 mo metastatic; ~54 mo PRODIGE-24 adjuvant |
| IND-PDAC-METASTATIC-1L-FOLFIRINOX | progression_free_survival | uncited | — | Median ~6.4 mo |
| IND-PDAC-METASTATIC-1L-GEM-NAB-PAC | overall_response_rate | uncited | — | ~23% |
| IND-PDAC-METASTATIC-1L-GEM-NAB-PAC | overall_survival_5y | uncited | — | mOS ~8.5 mo (MPACT) |
| IND-PDAC-METASTATIC-1L-GEM-NAB-PAC | progression_free_survival | uncited | — | Median ~5.5 mo |
| IND-PDAC-METASTATIC-2L-NAL-IRI | complete_response | uncited | — | ~1% |
| IND-PDAC-METASTATIC-2L-NAL-IRI | overall_response_rate | cited | trial-number resolved: NAPOLI-1 | ~16% ORR (nal-IRI+5-FU/LV arm, NAPOLI-1) |
| IND-PDAC-METASTATIC-2L-NAL-IRI | overall_survival_5y | cited | trial-number resolved: NAPOLI-1 | Median OS 6.1 mo vs 4.2 mo 5-FU/LV alone (HR 0.67, 95% CI 0.49–0.92, p=0.012, NAPOLI-1) |
| IND-PDAC-METASTATIC-2L-NAL-IRI | progression_free_survival | cited | trial-number resolved: NAPOLI-1 | Median PFS 3.1 mo (vs 1.5 mo 5-FU/LV alone; HR 0.56, NAPOLI-1) |

## `DIS-PMBCL` — Primary Mediastinal (Thymic) Large B-Cell Lymphoma

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PMBCL-1L-DA-EPOCH-R | complete_response | uncited | — | ~80-85% (PET-CT verified) |
| IND-PMBCL-1L-DA-EPOCH-R | overall_response_rate | uncited | — | ~95% |
| IND-PMBCL-1L-DA-EPOCH-R | overall_survival_5y | uncited | — | ~95% |
| IND-PMBCL-1L-DA-EPOCH-R | progression_free_survival | uncited | — | 5-year PFS ~93% (NCI 2013) |
| IND-PMBCL-1L-RCHOP-RT | complete_response | uncited | — | ~70% |
| IND-PMBCL-1L-RCHOP-RT | overall_response_rate | uncited | — | ~85% |
| IND-PMBCL-1L-RCHOP-RT | overall_survival_5y | uncited | — | ~85% |
| IND-PMBCL-1L-RCHOP-RT | progression_free_survival | uncited | — | 5-year PFS ~75% (з consolidation RT) |
| IND-PMBCL-2L-RICE-AUTOSCT | complete_response | uncited | — | ~30-40% post-salvage chemo + autoSCT |
| IND-PMBCL-2L-RICE-AUTOSCT | overall_response_rate | uncited | — | ~50-60% (chemosensitive disease) |
| IND-PMBCL-2L-RICE-AUTOSCT | overall_survival_5y | uncited | — | ~50-60% for chemosensitive responders |
| IND-PMBCL-2L-RICE-AUTOSCT | progression_free_survival | uncited | — | 2-year PFS ~50% in chemosensitive responders post-autoSCT |

## `DIS-PMF` — Primary Myelofibrosis (DIPSS-Plus stratified)

Indications: 5; populated: 20; cited: 0; probably-cited: 0; uncited: 20; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PMF-1L-OBSERVATION | complete_response | uncited | — | Spontaneous; does not eliminate clone; no MF reversal |
| IND-PMF-1L-OBSERVATION | overall_response_rate | uncited | — | Symptom control + spleen-volume reduction in ~40-50% on JAKi (COMFORT-I/II) |
| IND-PMF-1L-OBSERVATION | overall_survival_5y | uncited | — | DIPSS-Plus low ~10-15 yrs; int-1 ~6-7 yrs; int-2 ~3 yrs; high ~1.5 yrs |
| IND-PMF-1L-OBSERVATION | progression_free_survival | uncited | — | Symptomatic improvement; AML-transformation rate not altered |
| IND-PMF-1L-RUXOLITINIB | complete_response | uncited | — | Symptom + spleen response; clonal burden largely unchanged |
| IND-PMF-1L-RUXOLITINIB | overall_response_rate | uncited | — | ~42% achieve ≥35% spleen volume reduction at 24 weeks (COMFORT-I) |
| IND-PMF-1L-RUXOLITINIB | overall_survival_5y | uncited | — | DIPSS-Plus int-2 ~3 yrs; high ~1.5 yrs without alloHCT; alloHCT in fit eligible improves long-term outcomes |
| IND-PMF-1L-RUXOLITINIB | progression_free_survival | uncited | — | Pooled COMFORT-I/II suggests OS benefit (~30% reduction in death) over best available therapy |
| IND-PMF-2L-FEDRATINIB | complete_response | uncited | — | ≥50% MFSAF symptom score reduction ~27% |
| IND-PMF-2L-FEDRATINIB | overall_response_rate | uncited | — | ≥35% spleen volume reduction at week 24: 31-55% (JAKARTA-2; criteria-dependent) |
| IND-PMF-2L-FEDRATINIB | overall_survival_5y | uncited | — | Salvage setting; OS dependent on baseline DIPSS-Plus + alloHCT pathway |
| IND-PMF-2L-FEDRATINIB | progression_free_survival | uncited | — | Median treatment duration ~7-9 months in JAKARTA-2; FREEDOM-2 confirms efficacy |
| IND-PMF-ALLOHCT-HIGH-RISK | complete_response | uncited | — | Durable molecular CR ~30-50% at 5 years (variable by mutation profile) |
| IND-PMF-ALLOHCT-HIGH-RISK | overall_response_rate | uncited | — | ~70-90% achieve disease control post-HCT (variable by pre-HCT spleen volume + disease control) |
| IND-PMF-ALLOHCT-HIGH-RISK | overall_survival_5y | uncited | — | 5-y OS 30-65% high-risk MF (substantially better than non-transplant: <20% high-risk without HCT) |
| IND-PMF-ALLOHCT-HIGH-RISK | progression_free_survival | uncited | — | 5-y PFS 30-65% by DIPSS-Plus / MIPSS70 risk; substantially worse for TP53-mutated |
| IND-PMF-MOMELOTINIB-ANEMIA | complete_response | uncited | — | Spleen volume response 22% vs 3% danazol; transfusion independence 31% vs 20% |
| IND-PMF-MOMELOTINIB-ANEMIA | overall_response_rate | uncited | — | MFSAF total symptom score response 25% vs 9% danazol (MOMENTUM, p=0.0095) |
| IND-PMF-MOMELOTINIB-ANEMIA | overall_survival_5y | uncited | — | Salvage setting; OS dependent on baseline DIPSS-Plus + alloHCT pathway |
| IND-PMF-MOMELOTINIB-ANEMIA | progression_free_survival | uncited | — | Median treatment duration ongoing in MOMENTUM long-term follow-up |

## `DIS-PNET` — Pancreatic neuroendocrine tumor (pNET), well-differentiated G1/G2

Indications: 1; populated: 4; cited: 0; probably-cited: 0; uncited: 4; absent: 1; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PNET-METASTATIC-1L-EVEROLIMUS | complete_response | uncited | — | ~1% |
| IND-PNET-METASTATIC-1L-EVEROLIMUS | overall_response_rate | uncited | — | ~5% (RECIST CR+PR); disease control rate ~73% |
| IND-PNET-METASTATIC-1L-EVEROLIMUS | overall_survival_5y | uncited | — | No significant OS benefit proven (>70% crossover at progression confounds OS data) |
| IND-PNET-METASTATIC-1L-EVEROLIMUS | progression_free_survival | uncited | — | Median PFS 11.0 mo (HR 0.35 vs placebo, RADIANT-3) |

## `DIS-PROSTATE` — Prostate adenocarcinoma

Indications: 8; populated: 35; cited: 10; probably-cited: 1; uncited: 24; absent: 35; outcomes-cited % (loose): 31.4%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PROSTATE-MCRPC-1L-ARPI | median_overall_survival_months | uncited | — | 35 |
| IND-PROSTATE-MCRPC-1L-ARPI | median_radiographic_pfs_months | uncited | — | 20 |
| IND-PROSTATE-MCRPC-1L-ARPI | overall_response_rate | uncited | — | PSA decline ≥50% in ~78% |
| IND-PROSTATE-MCRPC-1L-PARPI | median_overall_survival_months | uncited | — | 19 |
| IND-PROSTATE-MCRPC-1L-PARPI | median_radiographic_pfs_months | uncited | — | 7.4 |
| IND-PROSTATE-MCRPC-1L-PARPI | overall_response_rate | uncited | — | Confirmed objective response ~33% in BRCA-mutant |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | ipfs_hr_vs_second_arpi | uncited | — | 0.54 |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | median_ipfs_months | uncited | — | 8.0 |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | median_os_months | uncited | — | 13.6 |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | os_hr_vs_second_arpi | uncited | — | 0.64 |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | overall_response_rate | uncited | — | 35.7% (CARD; post-docetaxel + post-ARPI) |
| IND-PROSTATE-MCRPC-2L-CABAZITAXEL | psa_decline_50pct | uncited | — | 35.7% |
| IND-PROSTATE-MCRPC-2L-DOCETAXEL | median_os_months | uncited | — | 18.9 (TAX 327; mCRPC population) |
| IND-PROSTATE-MCRPC-2L-DOCETAXEL | os_hr_vs_mitoxantrone | uncited | — | 0.76 |
| IND-PROSTATE-MCRPC-2L-DOCETAXEL | psa_decline_50pct | uncited | — | 45% (TAX 327) |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | median_os_control_months | cited | trial-number resolved: VISION | 11.3 |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | median_os_lu_psma_months | cited | trial-number resolved: VISION | 15.3 |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | median_rpfs_control_months | cited | trial-number resolved: VISION | 3.4 |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | median_rpfs_lu_psma_months | cited | trial-number resolved: VISION | 8.7 |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | os_hr | cited | trial-number resolved: VISION | 0.62 |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | psa_decline_50pct | cited | trial-number resolved: VISION | ~46% |
| IND-PROSTATE-MCRPC-2L-LU-PSMA | radiographic_pfs_hr | cited | trial-number resolved: VISION | 0.4 |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | alkaline_phosphatase_normalization | uncited | — | 47% vs 3% |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | bone_pain_palliation | uncited | — | Significant — primary benefit beyond survival |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | median_os_placebo_months | uncited | — | 11.3 |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | median_os_radium_months | uncited | — | 14.9 |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | os_hr | uncited | — | 0.7 |
| IND-PROSTATE-MCRPC-2L-RADIUM223 | time_to_sse_hr | uncited | — | 0.66 |
| IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET | median_overall_survival_months | cited | trial-number resolved: LATITUDE | 53 |
| IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET | median_radiographic_pfs_months | cited | trial-number resolved: LATITUDE | 33 |
| IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET | overall_response_rate | cited | trial-number resolved: LATITUDE | PSA decline ≥90% in ~75-80% within 6 months |
| IND-PROSTATE-MHSPC-1L-TRIPLET | hr_overall_survival | uncited | — | 0.68 |
| IND-PROSTATE-MHSPC-1L-TRIPLET | median_overall_survival_months | probably-cited | trial-number unresolved: ARASENS | Not yet reached (ARASENS final analysis pending) |
| IND-PROSTATE-MHSPC-1L-TRIPLET | median_radiographic_pfs_months | uncited | — | 36 |
| IND-PROSTATE-MHSPC-1L-TRIPLET | overall_response_rate | uncited | — | PSA <0.2 ng/mL at 9 months in ~55-65% |

## `DIS-PTCL-NOS` — Peripheral T-Cell Lymphoma, Not Otherwise Specified

Indications: 4; populated: 16; cited: 0; probably-cited: 1; uncited: 15; absent: 4; outcomes-cited % (loose): 6.2%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PTCL-1L-CHOEP-ALLOSCT | complete_response | uncited | — | ~50-55% post-induction |
| IND-PTCL-1L-CHOEP-ALLOSCT | overall_response_rate | uncited | — | ~70-75% post-induction (CHOEP) |
| IND-PTCL-1L-CHOEP-ALLOSCT | overall_survival_5y | uncited | — | ~50-60% with alloSCT consolidation (substantial improvement vs ~30-40% historical CHOEP-only) |
| IND-PTCL-1L-CHOEP-ALLOSCT | progression_free_survival | uncited | — | 5y PFS ~50% with alloSCT consolidation in CR1 (vs ~25-30% CHOEP alone) per EBMT registries |
| IND-PTCL-2L-PRALATREXATE | complete_response | uncited | — | ~11% |
| IND-PTCL-2L-PRALATREXATE | overall_response_rate | probably-cited | trial-number unresolved: PROPEL | ~29% (PROPEL) |
| IND-PTCL-2L-PRALATREXATE | overall_survival_5y | uncited | — | ~25-30% (heavily pretreated baseline poor) |
| IND-PTCL-2L-PRALATREXATE | progression_free_survival | uncited | — | Median PFS ~3.5 mo; mDOR 10.1 mo for responders |
| IND-PTCL-2L-ROMIDEPSIN | complete_response | uncited | — | ~15% |
| IND-PTCL-2L-ROMIDEPSIN | overall_response_rate | uncited | — | ~25-38% (NCI 1312) |
| IND-PTCL-2L-ROMIDEPSIN | overall_survival_5y | uncited | — | ~25-30% (heavily pretreated baseline) |
| IND-PTCL-2L-ROMIDEPSIN | progression_free_survival | uncited | — | Median PFS ~4 mo; mDOR ~17 mo for responders |
| IND-TCELL-1L-CHOEP | complete_response | uncited | — | ~50% |
| IND-TCELL-1L-CHOEP | overall_response_rate | uncited | — | ~75% |
| IND-TCELL-1L-CHOEP | overall_survival_5y | uncited | — | ~30-40% |
| IND-TCELL-1L-CHOEP | progression_free_survival | uncited | — | Median PFS ~2-3 years |

## `DIS-PTLD` — Post-Transplant Lymphoproliferative Disorder

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PTLD-1L-RCHOP | complete_response | uncited | — | ~70% |
| IND-PTLD-1L-RCHOP | overall_response_rate | uncited | — | ~80-90% |
| IND-PTLD-1L-RCHOP | overall_survival_5y | uncited | — | ~50-60% monomorphic |
| IND-PTLD-1L-RCHOP | progression_free_survival | uncited | — | Median PFS ~30 months у monomorphic |
| IND-PTLD-1L-REDUCE-IS | complete_response | uncited | — | ~25% reduce-IS only; +rituximab — ~60-70% |
| IND-PTLD-1L-REDUCE-IS | overall_response_rate | uncited | — | ~50% з reduction-of-IS alone (early polymorphic) |
| IND-PTLD-1L-REDUCE-IS | overall_survival_5y | uncited | — | ~60-70% полиморфна; ~40-50% монoморфна |
| IND-PTLD-1L-REDUCE-IS | progression_free_survival | uncited | — | Variable — depends on PTLD category + IS modulation |
| IND-PTLD-MAINTENANCE-RITUXIMAB | complete_response | uncited | — | ~70% sustained CR at 2 years with PTLD-1 sequential schedule (Trappe 2017) |
| IND-PTLD-MAINTENANCE-RITUXIMAB | overall_response_rate | uncited | — | Maintenance — sustains pre-existing CR/PR achieved with rituximab induction |
| IND-PTLD-MAINTENANCE-RITUXIMAB | overall_survival_5y | uncited | — | ~70-80% in low-risk subset (PTLD-1 stratification) |
| IND-PTLD-MAINTENANCE-RITUXIMAB | progression_free_survival | uncited | — | Median PFS >36 months in low-risk responders |

## `DIS-PV` — Polycythemia Vera

Indications: 6; populated: 24; cited: 0; probably-cited: 0; uncited: 24; absent: 6; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-PV-1L-HU | complete_response | uncited | — | Cytoreduction + thrombosis-risk reduction; clonal burden may decline modestly |
| IND-PV-1L-HU | overall_response_rate | uncited | — | Hct <45% + plt <400K achievable in >80% on HU + phlebotomy |
| IND-PV-1L-HU | overall_survival_5y | uncited | — | Median OS ~14-20 years; 5-y OS ~85% with proper cytoreduction |
| IND-PV-1L-HU | progression_free_survival | uncited | — | Thrombosis-related events reduced ~50-60% on HU vs phlebotomy alone in high-risk |
| IND-PV-1L-PHLEBOTOMY-ASA | complete_response | uncited | — | Spontaneous; symptom + thrombosis-risk reduction |
| IND-PV-1L-PHLEBOTOMY-ASA | overall_response_rate | uncited | — | Hct target <45% achievable in >90% with phlebotomy ± HU |
| IND-PV-1L-PHLEBOTOMY-ASA | overall_survival_5y | uncited | — | Median OS ~14-20 years; 5-y OS ~85-90% with proper Hct + risk control |
| IND-PV-1L-PHLEBOTOMY-ASA | progression_free_survival | uncited | — | PV-related thrombosis reduced from ~5%/y to <2%/y on aspirin + Hct control |
| IND-PV-1L-ROPEGINTERFERON | complete_response | uncited | — | Hct <45% + WBC + plt control sustained ≥1 year ~50-60% |
| IND-PV-1L-ROPEGINTERFERON | overall_response_rate | uncited | — | Complete hematologic response 71% vs 51% HU at 36 months (CONTINUATION-PV) |
| IND-PV-1L-ROPEGINTERFERON | overall_survival_5y | uncited | — | Mature OS data still maturing; non-inferior to HU for thrombosis-free survival at 36 months |
| IND-PV-1L-ROPEGINTERFERON | progression_free_survival | uncited | — | Disease-modifying potential — JAK2-V617F allele burden reduction substantially greater than HU; long-term implication... |
| IND-PV-2L-RUXOLITINIB | complete_response | uncited | — | Hct <45% achieved in ~60%; symptom + spleen response in majority |
| IND-PV-2L-RUXOLITINIB | overall_response_rate | uncited | — | ~21% composite primary response (Hct control + ≥35% spleen volume reduction at week 32) per RESPONSE; vs 1% best-avai... |
| IND-PV-2L-RUXOLITINIB | overall_survival_5y | uncited | — | OS not significantly altered vs HU per RESPONSE-2 long-term follow-up; cytoreductive maintenance |
| IND-PV-2L-RUXOLITINIB | progression_free_survival | uncited | — | Median treatment duration >5 years; thrombosis rate reduced vs BAT in pooled analyses |
| IND-PV-ANAGRELIDE-CONTINUOUS | complete_response | uncited | — | N/A (chronic cytoreduction) |
| IND-PV-ANAGRELIDE-CONTINUOUS | overall_response_rate | uncited | — | ~70-80% platelet response rate (ELN criteria) for anagrelide in HU-failure ET/PV |
| IND-PV-ANAGRELIDE-CONTINUOUS | overall_survival_5y | uncited | — | No OS difference vs HU in PT1; concern for higher arterial thrombosis with anagrelide (PT1) |
| IND-PV-ANAGRELIDE-CONTINUOUS | progression_free_survival | uncited | — | Thrombosis-free survival comparable to HU in PT1 trial (ET cohort); PV-specific data extrapolated from ET evidence |
| IND-PV-PREGNANCY-PEG-IFN | complete_response | uncited | — | N/A (chronic management) |
| IND-PV-PREGNANCY-PEG-IFN | overall_response_rate | uncited | — | HCT control + platelet stability achievable in ~70-80% with peg-IFN throughout pregnancy |
| IND-PV-PREGNANCY-PEG-IFN | overall_survival_5y | uncited | — | N/A |
| IND-PV-PREGNANCY-PEG-IFN | progression_free_survival | uncited | — | Live birth rate ~70-75% with combined IFN + ASA + low-dose phlebotomy (vs ~50% historical) |

## `DIS-RCC` — Renal cell carcinoma

Indications: 8; populated: 18; cited: 2; probably-cited: 5; uncited: 11; absent: 32; outcomes-cited % (loose): 38.9%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-RCC-ADJUVANT-PEMBRO | disease_free_survival | cited | trial-number resolved: KEYNOTE-564 | DFS HR 0.68 (p=0.002) at primary analysis |
| IND-RCC-ADJUVANT-PEMBRO | overall_survival | cited | trial-number resolved: KEYNOTE-564 | OS HR 0.62 (p=0.001) — first adjuvant therapy showing OS benefit in RCC |
| IND-RCC-METASTATIC-1L-LENV-PEMBRO | overall_response_rate | uncited | — | 71% vs 36% (sunitinib) |
| IND-RCC-METASTATIC-1L-LENV-PEMBRO | overall_survival_median | uncited | — | OS HR 0.66 (p=0.005) at interim; mOS 33.6 vs 29.5 mo |
| IND-RCC-METASTATIC-1L-LENV-PEMBRO | progression_free_survival | uncited | — | mPFS 23.9 mo vs 9.2 mo sunitinib (HR 0.39, p<0.001) |
| IND-RCC-METASTATIC-1L-NIVO-CABO | overall_response_rate | probably-cited | trial-family: CheckMate | 55.7% vs 27.1% (sunitinib) |
| IND-RCC-METASTATIC-1L-NIVO-CABO | overall_survival_median | probably-cited | trial-family: CheckMate | mOS 37.7 vs 34.3 mo (HR 0.70, p=0.001) |
| IND-RCC-METASTATIC-1L-NIVO-CABO | progression_free_survival | probably-cited | trial-family: CheckMate | mPFS 16.6 mo vs 8.3 mo sunitinib (HR 0.51, p<0.001) |
| IND-RCC-METASTATIC-1L-NIVO-IPI | median_overall_survival_months | probably-cited | trial-number unresolved: CheckMate-214 | 56 |
| IND-RCC-METASTATIC-1L-PEMBRO-AXI | median_overall_survival_months | probably-cited | trial-number unresolved: KEYNOTE-426 | 46 |
| IND-RCC-METASTATIC-2L-BELZUTIFAN | median_overall_survival_months | uncited | — | 21 |
| IND-RCC-METASTATIC-2L-BELZUTIFAN | median_progression_free_survival_months | uncited | — | 5.6 |
| IND-RCC-METASTATIC-2L-BELZUTIFAN | overall_response_rate | uncited | — | ORR 23%; DCR 78% |
| IND-RCC-METASTATIC-2L-CABOZANTINIB | overall_response_rate | uncited | — | 17% vs 3% (everolimus) |
| IND-RCC-METASTATIC-2L-CABOZANTINIB | overall_survival_median | uncited | — | mOS 21.4 vs 16.5 mo (HR 0.66, p=0.0003) |
| IND-RCC-METASTATIC-2L-CABOZANTINIB | progression_free_survival | uncited | — | mPFS 7.4 mo vs 3.8 mo everolimus (HR 0.58, p<0.001) |
| IND-RCC-VHL-DISEASE-BELZUTIFAN | median_progression_free_survival_months | uncited | — | Not yet reached (24+ mo follow-up) |
| IND-RCC-VHL-DISEASE-BELZUTIFAN | overall_response_rate | uncited | — | ORR 49% (RCC subset, LITESPARK-004); 30% (CNS hemangioblastoma); 91% (pancreatic NETs) |

## `DIS-SALIVARY` — Salivary gland carcinoma

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-SCLC` — Small cell lung cancer

Indications: 5; populated: 13; cited: 0; probably-cited: 1; uncited: 12; absent: 15; outcomes-cited % (loose): 7.7%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-SCLC-EXTENSIVE-1L | median_overall_survival_months | probably-cited | trial-family: CASPIAN | 13 |
| IND-SCLC-LIMITED-1L | median_overall_survival_months | uncited | — | 27 |
| IND-SCLC-PLATINUM-RECHALLENGE | overall_response_rate | uncited | — | ~50-60% for CTFI ≥180d (multiple retrospective series) |
| IND-SCLC-PLATINUM-RECHALLENGE | overall_survival | uncited | — | ~8-12 months from rechallenge |
| IND-SCLC-PLATINUM-RECHALLENGE | progression_free_survival | uncited | — | ~4-6 months |
| IND-SCLC-RR-LURBINECTEDIN | complete_response | uncited | — | ~2-5% CR; majority partial responses |
| IND-SCLC-RR-LURBINECTEDIN | overall_response_rate | uncited | — | ~35.2% ORR overall (Trigo phase II basket trial, n=105); platinum-sensitive (CTFI ≥90 days) ORR 45%; platinum-resista... |
| IND-SCLC-RR-LURBINECTEDIN | overall_survival_5y | uncited | — | Median OS 9.3 mo overall; 11.9 mo platinum-sensitive; 5.0 mo platinum-resistant. ATLANTIS phase III combination (lurb... |
| IND-SCLC-RR-LURBINECTEDIN | progression_free_survival | uncited | — | Median DoR 5.3 mo overall; 6.2 mo platinum-sensitive; 4.7 mo platinum-resistant |
| IND-SCLC-RR-TOPOTECAN | complete_response | uncited | — | ~5% CR in platinum-sensitive; rare in resistant |
| IND-SCLC-RR-TOPOTECAN | overall_response_rate | uncited | — | ~24% in platinum-sensitive; ~4% in platinum-resistant |
| IND-SCLC-RR-TOPOTECAN | overall_survival_5y | uncited | — | Median OS ~7-8 mo in platinum-sensitive; ~5 mo in platinum-resistant (von Pawel 1999 vs CAV, similar OS HR ~0.93, p=NS) |
| IND-SCLC-RR-TOPOTECAN | progression_free_survival | uncited | — | Median PFS ~3.4 mo (phase 3 vs CAV) |

## `DIS-SOFT-TISSUE-SARCOMA` — Soft tissue sarcoma (STS)

Indications: 4; populated: 18; cited: 0; probably-cited: 0; uncited: 18; absent: 16; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-STS-ADVANCED-1L-AI | overall_response_rate | uncited | — | ~26% (EORTC 62012) |
| IND-STS-ADVANCED-1L-AI | overall_survival | uncited | — | ~14.3 months (EORTC 62012) |
| IND-STS-ADVANCED-1L-AI | progression_free_survival | uncited | — | ~7.4 months (EORTC 62012) |
| IND-STS-ADVANCED-1L-DOXORUBICIN | overall_response_rate | uncited | — | ~14% (EORTC 62012) |
| IND-STS-ADVANCED-1L-DOXORUBICIN | overall_survival | uncited | — | ~12.8 months (EORTC 62012) |
| IND-STS-ADVANCED-1L-DOXORUBICIN | progression_free_survival | uncited | — | ~4.6 months (EORTC 62012) |
| IND-STS-ADVANCED-2L-GEMDOC | median_os_months | uncited | — | 17.9 |
| IND-STS-ADVANCED-2L-GEMDOC | orr | uncited | — | ~16-18% (SARC002: 16% GemDoc vs 8% gem mono) |
| IND-STS-ADVANCED-2L-GEMDOC | os_hr | uncited | — | 0.73 |
| IND-STS-ADVANCED-2L-GEMDOC | pfs_gem_mono_months | uncited | — | 3.0 |
| IND-STS-ADVANCED-2L-GEMDOC | pfs_gemdoc_months | uncited | — | 6.2 |
| IND-STS-ADVANCED-2L-PAZOPANIB | disease_control_rate | uncited | — | 67% |
| IND-STS-ADVANCED-2L-PAZOPANIB | median_os_pazopanib_months | uncited | — | 12.5 |
| IND-STS-ADVANCED-2L-PAZOPANIB | median_pfs_pazopanib_months | uncited | — | 4.6 |
| IND-STS-ADVANCED-2L-PAZOPANIB | median_pfs_placebo_months | uncited | — | 1.6 |
| IND-STS-ADVANCED-2L-PAZOPANIB | orr | uncited | — | ~6% |
| IND-STS-ADVANCED-2L-PAZOPANIB | os_hr | uncited | — | 0.86 |
| IND-STS-ADVANCED-2L-PAZOPANIB | pfs_hr | uncited | — | 0.35 |

## `DIS-SPLENIC-MZL` — Splenic Marginal Zone Lymphoma

Indications: 3; populated: 12; cited: 0; probably-cited: 0; uncited: 12; absent: 3; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-SMZL-1L-HCV-POSITIVE | hcv_cure_rate_svr12 | uncited | — | >95% (non-cirrhotic, treatment-naive) |
| IND-SMZL-1L-HCV-POSITIVE | overall_response_rate | uncited | — | ~50-75% lymphoma regression after SVR12 |
| IND-SMZL-1L-HCV-POSITIVE | overall_survival_5y | uncited | — | >85% in non-cirrhotic responders |
| IND-SMZL-1L-HCV-POSITIVE | progression_free_survival | uncited | — | Median not reached in DAA-responsive cases; durable in many |
| IND-SMZL-1L-RITUXIMAB | complete_response | uncited | — | ~50% |
| IND-SMZL-1L-RITUXIMAB | overall_response_rate | uncited | — | ~80-90% |
| IND-SMZL-1L-RITUXIMAB | overall_survival_5y | uncited | — | ~85% |
| IND-SMZL-1L-RITUXIMAB | progression_free_survival | uncited | — | Median PFS 5+ years |
| IND-SMZL-2L-BR | complete_response | uncited | — | ~50-60% |
| IND-SMZL-2L-BR | overall_response_rate | uncited | — | ~85-90% (Rummel 2013 BR for indolent NHL; SMZL subgroup similar) |
| IND-SMZL-2L-BR | overall_survival_5y | uncited | — | ~75-85% |
| IND-SMZL-2L-BR | progression_free_survival | uncited | — | Median PFS ~3-4 years |

## `DIS-T-ALL` — T-Lymphoblastic Leukemia / Lymphoma

Indications: 2; populated: 8; cited: 0; probably-cited: 0; uncited: 8; absent: 2; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-T-ALL-1L-HYPER-CVAD | complete_response | uncited | — | ~85% |
| IND-T-ALL-1L-HYPER-CVAD | overall_response_rate | uncited | — | ~90% |
| IND-T-ALL-1L-HYPER-CVAD | overall_survival_5y | uncited | — | ~50% adults; ~80% AYA з pediatric-inspired |
| IND-T-ALL-1L-HYPER-CVAD | progression_free_survival | uncited | — | Median PFS ~30-40 months |
| IND-T-ALL-2L-NELARABINE | complete_response | uncited | — | ~31% (CR + CRi) |
| IND-T-ALL-2L-NELARABINE | overall_response_rate | uncited | — | ~36-41% (Gökbuget 2017; DeAngelo 2007) |
| IND-T-ALL-2L-NELARABINE | overall_survival_5y | uncited | — | ~10% chemo-only; ~30-40% if successful bridge to alloSCT |
| IND-T-ALL-2L-NELARABINE | progression_free_survival | uncited | — | Median PFS ~3-4 months without consolidation; sustained only with alloSCT |

## `DIS-T-PLL` — T-Cell Prolymphocytic Leukemia

Indications: 2; populated: 8; cited: 0; probably-cited: 0; uncited: 8; absent: 2; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-T-PLL-1L-ALEMTUZUMAB | complete_response | uncited | — | ~70-80% |
| IND-T-PLL-1L-ALEMTUZUMAB | overall_response_rate | uncited | — | ~90% |
| IND-T-PLL-1L-ALEMTUZUMAB | overall_survival_5y | uncited | — | ~10% chemo-only; ~30-40% з allo-SCT у CR1 |
| IND-T-PLL-1L-ALEMTUZUMAB | progression_free_survival | uncited | — | Median PFS ~12 months chemo-only; ~36 months з allo-SCT |
| IND-T-PLL-2L-VENETOCLAX-ALEMTUZUMAB | complete_response | uncited | — | ~30% |
| IND-T-PLL-2L-VENETOCLAX-ALEMTUZUMAB | overall_response_rate | uncited | — | ~50-60% (small case series, Hampel 2020 Blood Adv) |
| IND-T-PLL-2L-VENETOCLAX-ALEMTUZUMAB | overall_survival_5y | uncited | — | ~10% chemo-only; ~25-35% if successful bridge to alloSCT in CR |
| IND-T-PLL-2L-VENETOCLAX-ALEMTUZUMAB | progression_free_survival | uncited | — | Median PFS ~6-9 months without alloSCT consolidation |

## `DIS-TESTICULAR-GCT` — Testicular germ cell tumor (GCT)

Indications: 4; populated: 14; cited: 0; probably-cited: 0; uncited: 14; absent: 15; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-GCT-METASTATIC-1L-BEP | complete_response | uncited | — | ~70-80% complete marker normalization |
| IND-GCT-METASTATIC-1L-BEP | overall_response_rate | uncited | — | ~90-95% ORR for good-risk GCT; ~80-85% for intermediate-risk |
| IND-GCT-METASTATIC-1L-BEP | overall_survival_5y | uncited | — | 5-year OS: ~92-95% good risk; ~80% intermediate risk; ~50-55% poor risk (IGCCC 1997) |
| IND-GCT-METASTATIC-1L-BEP | progression_free_survival | uncited | — | 5-year relapse-free survival: ~92% good risk; ~80% intermediate risk; ~50% poor risk |
| IND-GCT-METASTATIC-1L-EP | complete_response_rate | uncited | — | Equivalent to BEP × 3 for good-risk (Loehrer 1995) |
| IND-GCT-METASTATIC-1L-EP | overall_survival_5y | uncited | — | ~92% good risk; ~80% intermediate risk; ~50% poor risk (same as BEP) |
| IND-GCT-SALVAGE-2L-HDCT-ASCT | ned_2year_overall | uncited | — | 63% (Einhorn 2007) |
| IND-GCT-SALVAGE-2L-HDCT-ASCT | ned_favorable | uncited | — | 78% |
| IND-GCT-SALVAGE-2L-HDCT-ASCT | ned_unfavorable | uncited | — | 53% |
| IND-GCT-SALVAGE-2L-HDCT-ASCT | treatment_related_mortality | uncited | — | <3% |
| IND-GCT-SALVAGE-2L-TIP | complete_response_rate | uncited | — | 63% (Kondagunta 2005) |
| IND-GCT-SALVAGE-2L-TIP | durable_ned_rate | uncited | — | 52% |
| IND-GCT-SALVAGE-2L-TIP | favorable_subgroup_cr | uncited | — | 76% (AFP <1000, no liver/bone/brain mets) |
| IND-GCT-SALVAGE-2L-TIP | unfavorable_subgroup_cr | uncited | — | 45% |

## `DIS-THYROID-ANAPLASTIC` — Anaplastic thyroid carcinoma (ATC)

Indications: 2; populated: 4; cited: 0; probably-cited: 0; uncited: 4; absent: 6; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-ATC-BRAF-V600E-DAB-TRAM | complete_response | uncited | — | ~13-20% CR; some patients converted to surgical resection after response |
| IND-ATC-BRAF-V600E-DAB-TRAM | overall_response_rate | uncited | — | ~69% ORR (initial ROAR ATC cohort n=29, Subbiah JCO 2018); updated 2022 cohort n=36: ORR 56% |
| IND-ATC-BRAF-V600E-DAB-TRAM | overall_survival_5y | uncited | — | Median OS ~14.5 mo (vs historical mOS ~5 mo for unresectable ATC — 3× improvement) |
| IND-ATC-BRAF-V600E-DAB-TRAM | progression_free_survival | uncited | — | Median DoR ~9.0 mo; responses durable in CR subset |

## `DIS-THYROID-PAPILLARY` — Papillary thyroid carcinoma (PTC)

Indications: 1; populated: 0; cited: 0; probably-cited: 0; uncited: 0; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| _(no populated outcome fields)_ | | | | |

## `DIS-UROTHELIAL` — Urothelial carcinoma (bladder + upper tract)

Indications: 6; populated: 14; cited: 4; probably-cited: 0; uncited: 10; absent: 24; outcomes-cited % (loose): 28.6%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-UROTHELIAL-2L-ERDAFITINIB | overall_response_rate | uncited | — | ~35.3% vs 8.5% chemo (THOR cohort 1) |
| IND-UROTHELIAL-2L-ERDAFITINIB | overall_survival_5y | uncited | — | Median OS 12.1 vs 7.8 mo chemo (THOR cohort 1; HR 0.64, p=0.005) |
| IND-UROTHELIAL-2L-ERDAFITINIB | progression_free_survival | uncited | — | Median PFS 5.6 vs 2.7 mo chemo (THOR cohort 1; HR 0.58) |
| IND-UROTHELIAL-2L-EV | overall_response_rate | uncited | — | ~40.6% (EV-301 vs 17.9% chemo) |
| IND-UROTHELIAL-2L-EV | overall_survival | uncited | — | ~12.9 months (EV-301 vs 9.0 months chemo; HR 0.70) |
| IND-UROTHELIAL-2L-EV | progression_free_survival | uncited | — | ~5.6 months (EV-301) |
| IND-UROTHELIAL-2L-PEMBROLIZUMAB | complete_response_rate | cited | trial-number resolved: KEYNOTE-045 | ~7% (with durable responses; ~19% 5-year responders) |
| IND-UROTHELIAL-2L-PEMBROLIZUMAB | overall_response_rate | cited | trial-number resolved: KEYNOTE-045 | ~21.1% (KEYNOTE-045 vs 11.0% chemo) |
| IND-UROTHELIAL-2L-PEMBROLIZUMAB | overall_survival | cited | trial-number resolved: KEYNOTE-045 | ~10.3 months (KEYNOTE-045 vs 7.4 months chemo; HR 0.73) |
| IND-UROTHELIAL-2L-PEMBROLIZUMAB | pdl1_cps10_os | cited | trial-number resolved: KEYNOTE-045 | ~8.0 months (HR 0.57 for CPS ≥10 subgroup) |
| IND-UROTHELIAL-2L-PLATINUM-CHEMO | median_pfs_months | uncited | — | ~5-7 (extrapolated from 1L cisplatin-ineligible data; no dedicated 2L post-EV+pembro RCT) |
| IND-UROTHELIAL-2L-PLATINUM-CHEMO | orr_historical | uncited | — | ~35-40% (gem+carbo in cisplatin-ineligible UC 1L; EORTC/von der Maase data) |
| IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO | median_overall_survival_months | uncited | — | 31 |
| IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB | median_overall_survival_months | uncited | — | 21 |

## `DIS-WM` — Waldenström Macroglobulinemia / Lymphoplasmacytic Lymphoma

Indications: 5; populated: 20; cited: 0; probably-cited: 0; uncited: 20; absent: 5; outcomes-cited % (loose): 0.0%.

| Indication | Field | Bucket | Matched via | Value excerpt |
|---|---|---|---|---|
| IND-WM-1L-BTKI | complete_response | uncited | — | ~30% |
| IND-WM-1L-BTKI | overall_response_rate | uncited | — | ~94% (≥MR) |
| IND-WM-1L-BTKI | overall_survival_5y | uncited | — | ~85% |
| IND-WM-1L-BTKI | progression_free_survival | uncited | — | Median PFS not reached at 5 years (ASPEN) |
| IND-WM-1L-DRC | complete_response | uncited | — | ~10-15% |
| IND-WM-1L-DRC | overall_response_rate | uncited | — | ~85% |
| IND-WM-1L-DRC | overall_survival_5y | uncited | — | ~75% |
| IND-WM-1L-DRC | progression_free_survival | uncited | — | Median PFS ~3-5 years |
| IND-WM-2L-CARFILZOMIB-CXCR4MUT | complete_response | uncited | — | ~15% CR; ~68% VGPR |
| IND-WM-2L-CARFILZOMIB-CXCR4MUT | overall_response_rate | uncited | — | ~87% major response (CaRD Treon 2014) |
| IND-WM-2L-CARFILZOMIB-CXCR4MUT | overall_survival_5y | uncited | — | ~75-80% |
| IND-WM-2L-CARFILZOMIB-CXCR4MUT | progression_free_survival | uncited | — | Median PFS ~46 months (CaRD r/r WM cohort) |
| IND-WM-2L-VRD | complete_response | uncited | — | ~10-15% CR; ~50-60% VGPR |
| IND-WM-2L-VRD | overall_response_rate | uncited | — | ~88% major response (Treon 2009 r/r WM cohort) |
| IND-WM-2L-VRD | overall_survival_5y | uncited | — | ~70-80% |
| IND-WM-2L-VRD | progression_free_survival | uncited | — | Median PFS ~3-4 years post-induction |
| IND-WM-2L-ZANUBRUTINIB | complete_response | uncited | — | ~3-7% CR; ~28% VGPR (numerically superior to ibrutinib 19%) |
| IND-WM-2L-ZANUBRUTINIB | overall_response_rate | uncited | — | ~94% (≥minor response, ASPEN); ~28% VGPR-or-better in MYD88-mut cohort |
| IND-WM-2L-ZANUBRUTINIB | overall_survival_5y | uncited | — | ~85% |
| IND-WM-2L-ZANUBRUTINIB | progression_free_survival | uncited | — | Median PFS not reached at 5y (ASPEN); 4-y PFS ~78% |
