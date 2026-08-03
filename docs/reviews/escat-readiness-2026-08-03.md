# ESCAT readiness audit

Generated: `2026-08-03`. This is a deterministic data-quality queue, not an automated clinical assessment or tier reassignment.

| Measure | Value |
|---|---:|
| BMA records scanned | 475 |
| Clinically ready under release gate | 0 |
| Latest CIViC snapshot | 2026-04-25 |
| Snapshot age (days) | 100 |
| Strong-tier records missing evidence sources | 48 |
| BMAs absent from historical manifest | 40 |

## Issue counts

- critical: 250
- major: 392
- minor: 386

## Reviewer queue

### Critical

- `missing_evidence_sources` — `BMA-CD30-ALCL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-CD30-CHL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-CXCR4-WHIM-WM`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-EPCAM-GERMLINE-CRC`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-HER2-AMP-ESOPHAGEAL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-HRD-STATUS-OVARIAN`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-HRD-STATUS-PDAC`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-IGHV-UNMUTATED-CLL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-GERMLINE-OVARIAN`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-GERMLINE-PROSTATE`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-GERMLINE-UROTHELIAL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-SOMATIC-OVARIAN`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-SOMATIC-PROSTATE`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MLH1-SOMATIC-UROTHELIAL`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-GERMLINE-GASTRIC`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-GERMLINE-OVARIAN`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-GERMLINE-PROSTATE`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-SOMATIC-GASTRIC`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-SOMATIC-OVARIAN`: BMA has no per-source evidence records.
- `missing_evidence_sources` — `BMA-MSH2-SOMATIC-PROSTATE`: BMA has no per-source evidence records.
- … 230 additional critical findings are in the JSON artifact.

### Major

- `biomarker_taxonomy_mismatch` — `BMA-BRAF-V600K-MELANOMA`: BIO lookup tokens ['V600E'] do not overlap BMA qualifier tokens ['V600K'].
- `biomarker_taxonomy_mismatch` — `BMA-FLT3-F691L-AML`: BIO lookup tokens ['D835Y'] do not overlap BMA qualifier tokens ['F691L'].
- `civic_snapshot_stale` — `CIVIC-SNAPSHOT`: Latest snapshot 2026-04-25 is 100 days old (limit 45).
- `civic_variant_mismatch` — `BMA-ALK-G1202R-NSCLC`: Qualifier tokens ['G1202R'] do not overlap 33 CIViC EID variant(s): EID236 (C1156Y), EID237 (L1196M), EID763 (L1152R), EID764 (G1269A), EID765 (G1269A); +28 more.
- `civic_variant_mismatch` — `BMA-ALK-L1196M-NSCLC`: Qualifier tokens ['L1196M'] do not overlap 33 CIViC EID variant(s): EID236 (C1156Y), EID763 (L1152R), EID764 (G1269A), EID765 (G1269A), EID841 (C1156Y); +28 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-E255K-CML`: Qualifier tokens ['E255K', 'E255V'] do not overlap 284 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4396 (M351T); +279 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-F317L-BALL`: Qualifier tokens ['F317L'] do not overlap 294 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4350 (E255K); +289 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-F317L-CML`: Qualifier tokens ['F317L'] do not overlap 294 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4350 (E255K); +289 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-T315I-BALL`: Qualifier tokens ['T315I'] do not overlap 287 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4350 (E255K); +282 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-T315I-CML`: Qualifier tokens ['T315I'] do not overlap 287 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4350 (E255K); +282 more.
- `civic_variant_mismatch` — `BMA-BCR-ABL1-V299L-CML`: Qualifier tokens ['V299L'] do not overlap 304 CIViC EID variant(s): EID3819 (F359V), EID4302 (M244V), EID4316 (G250E), EID4335 (Y253H), EID4350 (E255K); +299 more.
- `civic_variant_mismatch` — `BMA-BRAF-V600K-MELANOMA`: Qualifier tokens ['V600K'] do not overlap 95 CIViC EID variant(s): EID1409 (V600E), EID3017 (V600E), EID9851 (V600E), EID12161 (V600E), EID12162 (V600E); +90 more.
- `civic_variant_mismatch` — `BMA-EZH2-Y641-FL`: Qualifier tokens ['Y641N'] do not overlap 4 CIViC EID variant(s): EID11111 (A682G, A692V, Y646C, Y646F, Y646H, Y646N, Y646S), EID12876 (A682G), EID11109 (A682G, A692V, Y646C, Y646F, Y646H, Y646N, Y646S), EID12875 (A682G).
- `civic_variant_mismatch` — `BMA-FLT3-F691L-AML`: Qualifier tokens ['F691L'] do not overlap 2 CIViC EID variant(s): EID8108 (D835Y), EID11095 (D835Y).
- `civic_variant_mismatch` — `BMA-PDGFRA-EXON12-GIST`: Qualifier tokens ['V561D'] do not overlap 13 CIViC EID variant(s): EID2 (D842V), EID15 (D842V), EID16 (D842V), EID738 (D842V), EID2478 (D842V); +8 more.
- `civic_variant_mismatch` — `BMA-PDGFRA-EXON14-GIST`: Qualifier tokens ['N659K', 'N659Y'] do not overlap 14 CIViC EID variant(s): EID2 (D842V), EID15 (D842V), EID16 (D842V), EID738 (D842V), EID2478 (D842V); +9 more.
- `civic_variant_mismatch` — `BMA-ROS1-G2032R-NSCLC`: Qualifier tokens ['G2032R'] do not overlap 7 CIViC EID variant(s): EID1252 (L2026M), EID1256 (L2155S), EID1257 (L2026M), EID1259 (G2101A), EID1253 (L2026M); +2 more.
- `legacy_broad_tier_iv` — `BMA-BCL2-REARRANGEMENT-MCL`: Legacy broad tier IV must be resolved to IVA or IVB during clinical review.
- `legacy_broad_tier_iv` — `BMA-BRAF-V600E-DLBCL-NOS`: Legacy broad tier IV must be resolved to IVA or IVB during clinical review.
- `legacy_broad_tier_iv` — `BMA-BRCA2-SOMATIC-MELANOMA`: Legacy broad tier IV must be resolved to IVA or IVB during clinical review.
- … 372 additional major findings are in the JSON artifact.

### Minor

- `missing_evidence_lane` — `BMA-1P19Q-CODELETION-LGG`: 2 evidence entries lack evidence_lane (SRC-EANO-GLIOMA-2022, SRC-NCCN-CNS-2025).
- `missing_evidence_lane` — `BMA-ALK-EML4-V1-NSCLC`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-ALK-EML4-V3-NSCLC`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-ALK-FUSION-ALCL`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-ALK-FUSION-NSCLC`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-ALK-G1202R-NSCLC`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-ALK-L1196M-NSCLC`: 11 evidence entries lack evidence_lane (SRC-CIVIC ×11).
- `missing_evidence_lane` — `BMA-APC-CRC`: 2 evidence entries lack evidence_lane (SRC-ESMO-CRC-2024, SRC-NCCN-COLON-2025).
- `missing_evidence_lane` — `BMA-ATM-GERMLINE-BREAST`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-ATM-GERMLINE-PDAC`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-ATM-GERMLINE-PROSTATE`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-ATM-LOSS-CLL`: 4 evidence entries lack evidence_lane (SRC-CIVIC ×4).
- `missing_evidence_lane` — `BMA-ATM-LOSS-MCL`: 1 evidence entries lack evidence_lane (SRC-CIVIC).
- `missing_evidence_lane` — `BMA-ATM-SOMATIC-BREAST`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-ATM-SOMATIC-PDAC`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-ATM-SOMATIC-PROSTATE`: 6 evidence entries lack evidence_lane (SRC-CIVIC ×6).
- `missing_evidence_lane` — `BMA-BAP1-MUT-RCC-PROGNOSTIC`: 1 evidence entries lack evidence_lane (SRC-NCCN-KIDNEY-2025).
- `missing_evidence_lane` — `BMA-BARD1-GERMLINE-BREAST`: 1 evidence entries lack evidence_lane (SRC-CIVIC).
- `missing_evidence_lane` — `BMA-BARD1-GERMLINE-OVARIAN`: 1 evidence entries lack evidence_lane (SRC-CIVIC).
- `missing_evidence_lane` — `BMA-BARD1-SOMATIC-BREAST`: 1 evidence entries lack evidence_lane (SRC-CIVIC).
- … 366 additional minor findings are in the JSON artifact.

## Required handling

1. Clinical co-leads classify scope and ESCAT applicability; they do not accept an inferred tier.
2. Reconcile taxonomy/evidence-ID warnings against primary sources and the relevant tumour context.
3. Record a clinician-authored dossier, then collect two independent sign-offs pinned to `last_verified`.
4. Re-run this audit before release; treatment-track selection remains independent of ESCAT.
