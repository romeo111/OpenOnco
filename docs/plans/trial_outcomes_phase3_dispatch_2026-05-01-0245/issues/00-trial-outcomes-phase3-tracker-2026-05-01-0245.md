# [Tracker] Trial-outcomes Phase 3 dispatch 2026-05-01-0245

## Mission

Master tracker for Phase-3 of the pivotal-trial-outcomes ingestion plan
(`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`). Replace
`SRC-LEGACY-UNCITED` placeholders introduced by Phase-2 schema migration
with real pivotal-trial citations across **278 indications**
split into **61 chunks**, ≤10 indications/chunk per the plan.

Phase 2 schema reference: [PR #177](https://github.com/romeo111/OpenOnco/pull/177).
Phase 1 audit baseline: [`docs/audits/expected_outcomes_traceability_2026-05-01.md`](../../../audits/expected_outcomes_traceability_2026-05-01.md).

## Sub-issues checklist

Check off each as it lands on master. Diseases ordered by audit `uncited` rank (highest first).

**Phase 4 (render layer, independent — can ship in parallel with Wave A):**

- [ ] [Phase-4] outcome-render-phase4-2026-05-01

**Phase 3 chunks (per-disease):**

- [ ] [DIS-NSCLC] outcome-citations-phase3-nsclc-part1of3-2026-05-01
- [ ] [DIS-NSCLC] outcome-citations-phase3-nsclc-part2of3-2026-05-01
- [ ] [DIS-NSCLC] outcome-citations-phase3-nsclc-part3of3-2026-05-01
- [ ] [DIS-CRC] outcome-citations-phase3-crc-part1of2-2026-05-01
- [ ] [DIS-CRC] outcome-citations-phase3-crc-part2of2-2026-05-01
- [ ] [DIS-OVARIAN] outcome-citations-phase3-ovarian-part1of2-2026-05-01
- [ ] [DIS-OVARIAN] outcome-citations-phase3-ovarian-part2of2-2026-05-01
- [ ] [DIS-AML] outcome-citations-phase3-aml-part1of2-2026-05-01
- [ ] [DIS-AML] outcome-citations-phase3-aml-part2of2-2026-05-01
- [ ] [DIS-MELANOMA] outcome-citations-phase3-melanoma-2026-05-01
- [ ] [DIS-DLBCL-NOS] outcome-citations-phase3-dlbcl-nos-2026-05-01
- [ ] [DIS-CHL] outcome-citations-phase3-chl-2026-05-01
- [ ] [DIS-FL] outcome-citations-phase3-fl-2026-05-01
- [ ] [DIS-MM] outcome-citations-phase3-mm-2026-05-01
- [ ] [DIS-B-ALL] outcome-citations-phase3-b-all-2026-05-01
- [ ] [DIS-BREAST] outcome-citations-phase3-breast-2026-05-01
- [ ] [DIS-CLL] outcome-citations-phase3-cll-2026-05-01
- [ ] [DIS-GASTRIC] outcome-citations-phase3-gastric-2026-05-01
- [ ] [DIS-MCL] outcome-citations-phase3-mcl-2026-05-01
- [ ] [DIS-PV] outcome-citations-phase3-pv-2026-05-01
- [ ] [DIS-AITL] outcome-citations-phase3-aitl-2026-05-01
- [ ] [DIS-ALCL] outcome-citations-phase3-alcl-2026-05-01
- [ ] [DIS-BURKITT] outcome-citations-phase3-burkitt-2026-05-01
- [ ] [DIS-CML] outcome-citations-phase3-cml-2026-05-01
- [ ] [DIS-MF-SEZARY] outcome-citations-phase3-mf-sezary-2026-05-01
- [ ] [DIS-PMF] outcome-citations-phase3-pmf-2026-05-01
- [ ] [DIS-PROSTATE] outcome-citations-phase3-prostate-2026-05-01
- [ ] [DIS-WM] outcome-citations-phase3-wm-2026-05-01
- [ ] [DIS-APL] outcome-citations-phase3-apl-2026-05-01
- [ ] [DIS-ESOPHAGEAL] outcome-citations-phase3-esophageal-2026-05-01
- [ ] [DIS-MDS-LR] outcome-citations-phase3-mds-lr-2026-05-01
- [ ] [DIS-NODAL-MZL] outcome-citations-phase3-nodal-mzl-2026-05-01
- [ ] [DIS-PTCL-NOS] outcome-citations-phase3-ptcl-nos-2026-05-01
- [ ] [DIS-ATLL] outcome-citations-phase3-atll-2026-05-01
- [ ] [DIS-ENDOMETRIAL] outcome-citations-phase3-endometrial-2026-05-01
- [ ] [DIS-ET] outcome-citations-phase3-et-2026-05-01
- [ ] [DIS-HCC] outcome-citations-phase3-hcc-2026-05-01
- [ ] [DIS-HCL] outcome-citations-phase3-hcl-2026-05-01
- [ ] [DIS-HCV-MZL] outcome-citations-phase3-hcv-mzl-2026-05-01
- [ ] [DIS-HGBL-DH] outcome-citations-phase3-hgbl-dh-2026-05-01
- [ ] [DIS-HNSCC] outcome-citations-phase3-hnscc-2026-05-01
- [ ] [DIS-MDS-HR] outcome-citations-phase3-mds-hr-2026-05-01
- [ ] [DIS-NK-T-NASAL] outcome-citations-phase3-nk-t-nasal-2026-05-01
- [ ] [DIS-NLPBL] outcome-citations-phase3-nlpbl-2026-05-01
- [ ] [DIS-PCNSL] outcome-citations-phase3-pcnsl-2026-05-01
- [ ] [DIS-PDAC] outcome-citations-phase3-pdac-2026-05-01
- [ ] [DIS-PMBCL] outcome-citations-phase3-pmbcl-2026-05-01
- [ ] [DIS-PTLD] outcome-citations-phase3-ptld-2026-05-01
- [ ] [DIS-SPLENIC-MZL] outcome-citations-phase3-splenic-mzl-2026-05-01
- [ ] [DIS-CERVICAL] outcome-citations-phase3-cervical-2026-05-01
- [ ] [DIS-EATL] outcome-citations-phase3-eatl-2026-05-01
- [ ] [DIS-GIST] outcome-citations-phase3-gist-2026-05-01
- [ ] [DIS-HSTCL] outcome-citations-phase3-hstcl-2026-05-01
- [ ] [DIS-MASTOCYTOSIS] outcome-citations-phase3-mastocytosis-2026-05-01
- [ ] [DIS-MTC] outcome-citations-phase3-mtc-2026-05-01
- [ ] [DIS-RCC] outcome-citations-phase3-rcc-2026-05-01
- [ ] [DIS-T-ALL] outcome-citations-phase3-t-all-2026-05-01
- [ ] [DIS-T-PLL] outcome-citations-phase3-t-pll-2026-05-01
- [ ] [DIS-CHOLANGIOCARCINOMA] outcome-citations-phase3-cholangiocarcinoma-2026-05-01
- [ ] [DIS-GBM] outcome-citations-phase3-gbm-2026-05-01
- [ ] [DIS-GLIOMA-LOW-GRADE] outcome-citations-phase3-glioma-low-grade-2026-05-01

## Sequencing

- **Wave A (parallel):** Top-5 worst-offender diseases (CRC, NSCLC, AML, Ovarian, DLBCL-NOS) — ~20 chunks.
- **Wave B (parallel, after Wave A merges):** ranks 6-15 (Melanoma, FL, PV, B-ALL, MM, Breast, etc.) — ~30 chunks.
- **Wave C (parallel, after Wave B):** remaining diseases — fewer indications/disease, lower priority.
- **Phase 4 render** dispatched separately once Phase-3 hits ~70% completion (tracked at the plan level, not as a chunk here).

## Quality gates (uniform per chunk)

1. KB validator clean.
2. Audit re-run shows the chunk's indications moved from `uncited` → `cited`.
3. Per-chunk allowlist strictly enforced.
4. Sources cited (no invented IDs, no fabricated PMIDs).
5. Self-push authorized per CLAUDE.md commit `3a60901b`.

## Acceptance for the wave

- All non-deferred sub-issues closed.
- KB validator clean throughout.
- Audit `cited+probably-cited` rises from 15.7% baseline toward ≥90% v1.0 target.
- No `SRC-LEGACY-UNCITED` placeholders remain (or remaining set is documented + intentionally deferred).
- Phase 4 render chunk dispatched once Phase 3 hits 70%.
