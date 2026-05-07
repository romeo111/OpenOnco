# GI-3 wave: pancreaticobiliary + CRC expansion

**Stamp:** 2026-05-08-1500
**Status:** PROPOSED — not dispatched
**Source:** GI-2 wave plan §11.5.1 future workstream + post-Phase-A audit
**Predecessors:** GI-2 wave Phase A+C+D closed (`71fb7638` master HEAD); §17 schema ratified

---

## 1. Why GI-3 now

GI-2 wave covered gastric + esophageal. GI-3 covers the rest of GI: PDAC (pancreatic), cholangiocarcinoma, CRC. Coverage audit reveals all three diseases ALREADY have meaningful scaffold content, BUT critical 2024-2026 trial readouts + biomarker actionability + multimodal periop (analogous to FLOT) are missing.

§17 schema is now ratified — phased indications work. PDAC mFOLFIRINOX adjuvant, CRC TNT (total neoadjuvant therapy), cholangio gem-cis-durvalumab (TOPAZ-1) all need phasing or have it implicit in notes today.

## 2. Existing KB coverage (audit, 2026-05-08)

### 2.1 Pancreatic (DIS-PDAC)

Existing indications:
- `ind_pdac_metastatic_1l_folfirinox.yaml`
- `ind_pdac_metastatic_1l_gem_nab_pac.yaml`
- `ind_pdac_metastatic_2l_nal_iri.yaml`
- `ind_pdac_maintenance_olaparib_brca.yaml`

Existing algorithms: `algo_pdac_metastatic_1l`, `algo_pdac_metastatic_2l`

Coverage gaps:
- Resectable PDAC: **mFOLFIRINOX adjuvant** (PRODIGE-24 / CCTG PA.6) — NOT modelled
- Borderline-resectable PDAC: **neoadjuvant FOLFIRINOX or gem+nab+RT** (NORPACT-1, ESPAC-5F, SWOG S1505) — NOT modelled
- Periop phasing: §17 phases not yet used despite this being PDAC's primary use case
- BRCA-mutation 1L: **NALIRIFOX / mFOLFIRINOX preference** for BRCA — exists as monotherapy maintenance only; 1L preference rule missing
- KRAS G12C 2L: sotorasib (CodeBreaK 100/300) — present in CRC, not yet PDAC despite NCT05726399
- HER2-amplified PDAC: trastuzumab+pertuzumab from MyPathway — out of scope for v0.1?
- Targeted: NTRK fusions, MSI-H, BRAF V600E pan-tumor extrapolations — not surfaced as PDAC-specific BMA

### 2.2 Cholangiocarcinoma (DIS-CHOLANGIOCARCINOMA)

Existing indications:
- `ind_cholangio_advanced_gem_cis.yaml` — 1L
- `ind_cholangio_2l_fgfr2_fusion_*` (3 — pemigatinib, infigratinib, futibatinib)

Existing algorithms: `algo_cholangio_1l`, `algo_cholangio_2l`

Coverage gaps:
- **TOPAZ-1 (durvalumab + gem+cis 1L)** — gold standard 1L per 2022; NOT in current 1L indication
- **KEYNOTE-966 (pembrolizumab + gem+cis 1L)** — alternative IO 1L per 2023; NOT in KB
- **IDH1-mutant 2L: ivosidenib (ClarIDHy)** — NOT in KB
- **HER2+ cholangio: zanidatamab / trastuzumab** (HERIZON-BTC-01) — NOT in KB
- **NTRK fusion** pan-tumor extrapolation — not surfaced
- **MSI-H pan-tumor pembro** — not surfaced for cholangio

### 2.3 Colorectal (DIS-CRC)

Existing indications: ~16 (1L MSI-H pembro, 1L FOLFOX+bev, 1L FOLFOXIRI+bev, 1L RAS-WT left, 2L FOLFIRI+bev, 2L BRAF BEACON, 2L EGFR rechallenge, 2L HER2 T-DXd, 2L HER2 tucatinib, 2L KRAS G12C sotorasib+cetuximab, 2L MSI-H pembro — comprehensive)

Existing algorithms: `algo_crc_adjuvant`, `algo_crc_metastatic_1l`, `algo_crc_metastatic_2l`

Coverage gaps:
- **Total neoadjuvant therapy (TNT) for rectal cancer** — RAPIDO + PRODIGE-23 — NOT modelled (would require §17 phases + RadiationCourse for SCRT + chemo + watch-and-wait)
- **Watch-and-wait protocol** post complete clinical response — NOT modelled
- **Adjuvant 3 mo vs 6 mo CapOx** for stage III low-risk (IDEA collaboration) — NOT explicit
- **MOUNTAINEER-02** — tucatinib+T-DXd HER2+ CRC (newer than MOUNTAINEER trastu+tucatinib) — verify
- **Liver-limited oligomet CRC**: oligomet routing analogous to GI-2 C5 (was implemented for gastric/esoph; could extend to CRC)
- **Maintenance therapy 1L post induction**: capecitabine + bev (CAIRO3) explicit indication
- **3rd-line+ TAS-102, regorafenib, fruquintinib** (FRESCO-2) — verify FRESCO-2 in KB

## 3. Phasing/§17 use cases in GI-3

Strong candidates for `Indication.phases` (mirrors GI-2 C1 FLOT pattern):

| Indication | Phases |
|---|---|
| `ind_pdac_resectable_periop_mfolfirinox` (NEW) | adjuvant mFOLFIRINOX × 12 (PRODIGE-24) |
| `ind_pdac_borderline_resectable_neoadj_folfirinox` (NEW) | neoadj FOLFIRINOX → restaging → resection → adj |
| `ind_rectal_tnt_short_course_chemo` (NEW) | SCRT 25 Gy / 5 fx → chemo (CapOx ≈ 6 cycles) → resection (RAPIDO) |
| `ind_rectal_tnt_long_course_chemoradiation` (NEW) | LCCRT 50.4 Gy + 5-FU → chemo → resection (PRODIGE-23) |
| `ind_pdac_chemoradiation_lapc` (NEW) | induction chemo × 3-4 → CRT (definitive or downstaging) |

These need both phases AND new RadiationCourse entities (SCRT 25/5, LCCRT 50.4/28, PDAC SBRT).

## 4. Workstream sequencing (5 phases)

Same pattern as GI-2 (W0 → A → B → §17-consumers C → D algorithms).

### Phase W0 (sources)

Source backfill before content. Estimate 12-15 NEW sources:

- **PDAC:** PRODIGE-24-Conroy-2018, ESPAC-4-Neoptolemos-2017, NORPACT-1-Labori-2024, ESPAC-5F-Ghaneh-2023, NAPOLI-3-Wainberg-2024 (NALIRIFOX 1L), POLO-Golan-2019 (already in KB? verify)
- **Cholangio:** TOPAZ-1-Oh-2022, KEYNOTE-966-Kelley-2023, ClarIDHy-Abou-Alfa-2020, HERIZON-BTC-01-Harding-2023, ABC-02-Valle-2010 (already? gem+cis basis)
- **CRC:** RAPIDO-Bahadoer-2021, PRODIGE-23-Conroy-2021, FRESCO-2-Dasari-2023, MOUNTAINEER-02 (verify), CAIRO3-Simkens-2015, IDEA-Grothey-2018

Priority: 8-10 most-cited sources first; lower-priority defer.

### Phase A (1L + 2L metastatic gaps)

- A1 cholangio 1L IO (TOPAZ-1 + KEYNOTE-966)
- A2 cholangio 2L expansion (ClarIDHy IDH1, HERIZON HER2+)
- A3 PDAC 1L NAPOLI-3 NALIRIFOX
- A4 CRC oligomet (extension from GI-2 C5 pattern)
- A5 CRC 3L+ FRESCO-2 fruquintinib

### Phase B (reconciliation)

- B1 IDEA 3-mo vs 6-mo CapOx adjuvant — make stratified explicit

### Phase C (§17 multimodal)

- C1 PDAC adjuvant mFOLFIRINOX (phases × 1: adjuvant 12 cycles)
- C2 PDAC borderline-resectable (phases × 3-4: neoadj → restage → surgery → adj)
- C3 Rectal TNT short-course (RAPIDO; phases + RT 25/5)
- C4 Rectal TNT long-course (PRODIGE-23; phases + RT 50.4/28)
- C5 PDAC LAPC chemoradiation (phases + RT)

### Phase D (algorithms)

- D1 algo extensions for new indications (similar to GI-2 D1+D2 pattern)
- D2 watch-and-wait routing post-TNT-cCR (rectal)

## 5. §17 readiness

Existing PDAC + cholangio + CRC diseases all currently `proposal_status: full` (as of §17 ratification PR #427). They can host phased indications immediately.

**Surgery entities to author** (Phase C):
- `proc_pancreaticoduodenectomy` (Whipple — fixture already exists in tests/fixtures/surgery_whipple.yaml; promote to production)
- `proc_distal_pancreatectomy`
- `proc_total_pancreatectomy`
- `proc_low_anterior_resection` (rectal LAR)
- `proc_apr_abdominoperineal_resection` (rectal APR)
- `proc_hepatectomy_partial` (CRC liver mets)

**RadiationCourse entities to author** (Phase C):
- `rc_scrt_25_5_rectal` (RAPIDO short-course)
- `rc_lccrt_504_rectal` (PRODIGE-23 long-course CRT)
- `rc_lapc_chemoradiation` (PDAC LAPC, ~50.4 Gy)
- `rc_pdac_sbrt` (PDAC stereotactic)

## 6. Estimate

| | Without §17 (W0+A+B only) | With §17 (full GI-3 wave) |
|---|---|---|
| Chunks | 8-10 | 14-18 |
| Agent-hours | 16-30 | 35-60 |
| PRs | 8-10 | 14-18 |
| Calendar-days | 3-6 | 5-12 |

§17 is already ratified, so full wave is unblocked.

## 7. Risk register (delta from GI-2)

| # | Risk | Mitigation |
|---|---|---|
| R1 | Rectal TNT modelling — watch-and-wait protocol has no current schema support | Defer watch-and-wait to a §18 proposal if needed; ship TNT phases first |
| R2 | PDAC borderline-resectable definitions vary (NCCN vs IAP vs ESMO) | Cite multiple definitions; let routing depend on stage_requirements text describing resectability bucket |
| R3 | NTRK / MSI-H / BRAF V600E pan-tumor — extrapolation across diseases | Reuse breast / NSCLC patterns as templates; mark `extrapolated: true` per established convention |
| R4 | KRAS G12C sotorasib in PDAC vs CRC — same drug, disease-specific evidence | Author PDAC-specific BMA + indication; share DRUG-SOTORASIB but separate Indication |

## 8. Pre-dispatch decisions needed

1. Start GI-3 immediately or pause for user review of plan?
2. Do W0 + A first (no §17 dependencies) and dispatch C in a separate sub-wave when §17-consumer pattern is confirmed at scale?
3. Rectal cancer — currently DIS-CRC. Should rectal split off into DIS-RECTAL? (Per NCCN they're separate guidelines; clinical management diverges substantially.)

## 9. Reference docs

- `docs/plans/gi2_wave_gastric_esophageal_2026-05-04-1730.md` — GI-2 plan (template)
- `docs/plans/gi2_long_tail_followups_2026-05-07.md` — GI-2 long-tail backlog
- `docs/plans/refactor_lessons_2026-05-07.md` — refactor + Phase C consumer lessons (apply all to GI-3)
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 — Surgery + RadiationCourse + IndicationPhase (ratified)
