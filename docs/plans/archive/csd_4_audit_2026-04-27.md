# CSD-4 Solid-Tumor 2L+ Gap Audit (2026-04-27)

Per-cancer audit of existing 1L coverage, missing 2L+ indications, and
required drug-stub additions to enable Wave 1 (5 parallel cancer-family
agents — CRC, NSCLC, BREAST, MELANOMA, OVARIAN).

Drug-existence column legend: ✓ exists in `knowledge_base/hosted/content/drugs/`
as of audit timestamp; ✗ missing (stubbed in this commit unless noted);
*S* = stub authored in this commit.

---

## DIS-CRC — Colorectal carcinoma

### Existing
- 1L indications (3): IND-CRC-METASTATIC-1L-MSI-H-PEMBRO,
  IND-CRC-METASTATIC-1L-RAS-WT-LEFT, IND-CRC-METASTATIC-1L-FOLFOX-BEV
- Adjuvant indications (1): IND-CRC-ADJUVANT-STAGE3-FOLFOX
- 2L+ indications (4): IND-CRC-METASTATIC-2L-BRAF-BEACON,
  IND-CRC-METASTATIC-2L-FOLFIRI-BEV, IND-CRC-METASTATIC-3L-REGORAFENIB,
  IND-CRC-METASTATIC-3L-TAS102-BEV
- Maintenance indications: 0 (5-FU/cape ± bev maintenance not modeled)
- 1L algorithm: ALGO-CRC-METASTATIC-1L exists
- 2L+ algorithm: **missing** ← target for CSD-4-crc

### Needed (from NCCN Colon v4.2025 / ESMO mCRC 2024)
2L+ indications to author in Wave 1 (target ~6-8):
- IND-CRC-METASTATIC-2L-MSI-H-NIVO-IPI — needs DRUG-NIVOLUMAB ✓ + DRUG-IPILIMUMAB ✓ (CheckMate-8HW post-pembro path)
- IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB-TRASTUZUMAB (MOUNTAINEER) — needs DRUG-TUCATINIB ✓ + DRUG-TRASTUZUMAB ✓
- IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD (DESTINY-CRC02) — needs DRUG-TRASTUZUMAB-DERUXTECAN ✓
- IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-PANITUMUMAB (CodeBreaK 300) — needs DRUG-SOTORASIB ✓ + DRUG-PANITUMUMAB ✗ (panitumumab missing — see below)
- IND-CRC-METASTATIC-2L-KRAS-G12C-ADAGRASIB-CETUXIMAB (KRYSTAL-10) — needs DRUG-ADAGRASIB ✓ + DRUG-CETUXIMAB ✓
- IND-CRC-METASTATIC-3L-FRUQUINTINIB (FRESCO-2) — needs DRUG-FRUQUINTINIB *S*
- IND-CRC-METASTATIC-3L-NTRK-LAROTRECTINIB / -ENTRECTINIB (tumor-agnostic) — needs DRUG-LAROTRECTINIB ✓ + DRUG-ENTRECTINIB ✓
- IND-CRC-METASTATIC-3L-RET-SELPERCATINIB (rare RET-fusion mCRC) — needs DRUG-SELPERCATINIB ✓
- IND-CRC-MAINTENANCE-CAPE-BEV (post-FOLFOX/CAPOX-bev induction) — needs DRUG-CAPECITABINE ✓ + DRUG-BEVACIZUMAB ✓

### Drugs missing in KB (post-stubs)
- DRUG-FRUQUINTINIB — *stubbed in this commit*
- DRUG-PANITUMUMAB — **NOT stubbed** (out of CSD-4 scope; flag for Wave 1 author or follow-up)

### Biomarkers
- BIO-MSI-H, BIO-MMR, BIO-RAS-WT, BIO-BRAF-V600E, BIO-HER2-AMP, BIO-KRAS-G12C all present (verified in CSD-1/CSD-2). No new biomarkers required.

### Notes
- Sidedness (right vs left primary) is captured as condition string in algorithm; no new RF needed.
- Panitumumab gap is real — appears nowhere in CRC indications today; should be addressed in Wave 1 or in a follow-up drug-stub PR.

---

## DIS-NSCLC — Non-small cell lung cancer

### Existing
- 1L indications (6): IND-NSCLC-EGFR-MUT-MET-1L,
  IND-NSCLC-ALK-MET-1L, IND-NSCLC-PDL1-HIGH-MET-1L,
  IND-NSCLC-PDL1-LOW-NONSQ-MET-1L, IND-NSCLC-TMB-HIGH-MET-1L-PEMBRO-MONO,
  IND-NSCLC-STAGE-III-PACIFIC (chemoradiation + durvalumab consolidation)
- 2L+ indications (3): IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB,
  IND-NSCLC-ALK-2L-LORLATINIB, IND-NSCLC-KRAS-G12C-MET-2L
- Maintenance indications (1): IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO
- 1L algorithm: ALGO-NSCLC-METASTATIC-1L exists
- 2L+ algorithm: **missing** ← target for CSD-4-nsclc

### Needed (from NCCN NSCLC v4.2025 / ESMO mNSCLC 2024)
Driver-mutant 2L (resistance to 1L TKI) is the dominant subway:
- IND-NSCLC-EGFR-2L-AMIVANTAMAB-CHEMO (MARIPOSA-2 post-osimertinib) — needs DRUG-AMIVANTAMAB *S* + DRUG-LAZERTINIB *S* + DRUG-CARBOPLATIN ✓ + DRUG-PEMETREXED ✓
- IND-NSCLC-EGFR-1L-AMIVANTAMAB-LAZERTINIB (MARIPOSA — 1L alt to osimertinib; biomarker subset) — needs same drugs *S*
- IND-NSCLC-EGFR-MET-AMP-TEPOTINIB-OSIMERTINIB (post-osi resistance) — needs DRUG-TEPOTINIB ✓ + DRUG-OSIMERTINIB ✓
- IND-NSCLC-EGFR-EXON20-AMIVANTAMAB (CHRYSALIS) — needs DRUG-AMIVANTAMAB *S*
- IND-NSCLC-ROS1-1L-REPOTRECTINIB / -2L-POST-CRIZOTINIB (TRIDENT-1) — needs DRUG-REPOTRECTINIB *S*
- IND-NSCLC-RET-SELPERCATINIB / -PRALSETINIB — needs DRUG-SELPERCATINIB ✓ + DRUG-PRALSETINIB *S*
- IND-NSCLC-MET-EX14-CAPMATINIB / -TEPOTINIB — needs DRUG-CAPMATINIB ✓ + DRUG-TEPOTINIB ✓
- IND-NSCLC-HER2-MUT-TDXD (DESTINY-Lung) — needs DRUG-TRASTUZUMAB-DERUXTECAN ✓
- IND-NSCLC-NTRK-LAROTRECTINIB / -ENTRECTINIB — already exist as drugs ✓
- IND-NSCLC-PDL1-HIGH-1L-CEMIPLIMAB (EMPOWER-Lung 1, alt to pembro) — needs DRUG-CEMIPLIMAB *S*
- IND-NSCLC-NONSQ-2L-DOCETAXEL-NINTEDANIB (LUME-Lung 1; alt to ramucirumab) — needs DRUG-NINTEDANIB ✗ (out of CSD-4 scope; flag)
- IND-NSCLC-KRAS-G12C-2L-ADAGRASIB (KRYSTAL-1) — needs DRUG-ADAGRASIB ✓
- IND-NSCLC-EARLY-OSIMERTINIB-ADJUVANT (ADAURA — EGFR+ stage IB-IIIA post-resection) — needs DRUG-OSIMERTINIB ✓
- IND-NSCLC-EARLY-ATEZO-ADJUVANT (IMpower010 — PD-L1+ stage II-IIIA post-resection + chemo) — needs DRUG-ATEZOLIZUMAB ✓

### Drugs missing in KB (post-stubs)
- DRUG-AMIVANTAMAB — *stubbed in this commit*
- DRUG-LAZERTINIB — *stubbed in this commit*
- DRUG-REPOTRECTINIB — *stubbed in this commit*
- DRUG-PRALSETINIB — *stubbed in this commit*
- DRUG-CEMIPLIMAB — *stubbed in this commit*
- DRUG-NINTEDANIB — **NOT stubbed** (LUME-Lung 1 niche; flag for Wave 1 or follow-up)

### Biomarkers
- All driver-mutation biomarkers present (BIO-EGFR-MUT, BIO-EGFR-EX20-INS, BIO-ALK-REARRANGED, BIO-ROS1, BIO-KRAS-G12C, BIO-MET-EX14, BIO-RET-FUSION, BIO-NTRK-FUSION, BIO-HER2-MUT, BIO-PDL1-TPS, BIO-MET-AMP). Verify BIO-EGFR-T790M and BIO-MET-AMP-POST-OSI explicitly during Wave 1 author.

---

## DIS-BREAST — Invasive breast cancer

### Existing
- 1L early indications (2): IND-BREAST-HER2-POS-EARLY-NEOADJUVANT,
  IND-BREAST-TNBC-EARLY-NEOADJUVANT
- 1L metastatic indications (2): IND-BREAST-HR-POS-MET-1L-CDKI,
  IND-BREAST-HER2-POS-MET-1L-THP
- 2L+ indications (2): IND-BREAST-HER2-POS-MET-2L-TDXD,
  IND-BREAST-BRCA-POS-MET-PARPI (cross-line BRCA path)
- Maintenance: 0 (CDK4/6i continuation through progression handled within 1L)
- 1L algorithm: ALGO-BREAST-1L exists (single algo currently — needs to split into HR+ / HER2+ / TNBC sub-algos OR remain unified with branching)
- 2L+ algorithm: **missing** ← targets for CSD-4-breast (3 sub-algos)

### Needed (from NCCN Breast v3.2025 / ESMO mBC 2024)

**HR+/HER2- 2L+ (CSD-4-breast → ALGO-BREAST-HR-POS-2L)**
- IND-BREAST-HR-POS-MET-2L-CAPIVASERTIB-FULVESTRANT (CAPItello-291; PIK3CA/AKT1/PTEN-altered) — needs DRUG-CAPIVASERTIB *S* + DRUG-FULVESTRANT ✓
- IND-BREAST-HR-POS-MET-2L-ALPELISIB-FULVESTRANT (SOLAR-1; PIK3CA-mutant) — needs DRUG-ALPELISIB ✓ + DRUG-FULVESTRANT ✓
- IND-BREAST-HR-POS-MET-2L-ELACESTRANT (EMERALD; ESR1-mutant) — needs DRUG-ELACESTRANT ✓
- IND-BREAST-HR-POS-MET-2L-EVEROLIMUS-EXEMESTANE (BOLERO-2) — needs DRUG-EVEROLIMUS ✗ (likely missing — verify) + DRUG-EXEMESTANE ✓
- IND-BREAST-HR-POS-MET-3L-TDXD (DESTINY-Breast06; HER2-low/ultralow) — needs DRUG-TRASTUZUMAB-DERUXTECAN ✓
- IND-BREAST-HR-POS-MET-2L-FULVESTRANT-MONO (post-AI; biomarker-untargeted) — needs DRUG-FULVESTRANT ✓

**HER2+ 2L+ (CSD-4-breast → ALGO-BREAST-HER2-POS-2L)**
- IND-BREAST-HER2-POS-MET-3L-TUCATINIB-TRASTUZUMAB-CAPECITABINE (HER2CLIMB; brain mets) — needs DRUG-TUCATINIB ✓ + DRUG-TRASTUZUMAB ✓ + DRUG-CAPECITABINE ✓
- IND-BREAST-HER2-POS-MET-3L-T-DM1 (EMILIA; alt to T-DXd 2L per access) — needs DRUG-TRASTUZUMAB-EMTANSINE ✓
- IND-BREAST-HER2-POS-MET-4L-MARGETUXIMAB (SOPHIA — niche) — drug missing; out of CSD-4 scope
- IND-BREAST-HER2-POS-MET-LATE-NERATINIB-CAPECITABINE (NALA) — DRUG-NERATINIB ✗ likely missing; out of CSD-4 scope

**TNBC 2L+ (CSD-4-breast → ALGO-BREAST-TNBC-2L)**
- IND-BREAST-TNBC-MET-2L-SACITUZUMAB-GOVITECAN (ASCENT) — needs DRUG-SACITUZUMAB-GOVITECAN ✓
- IND-BREAST-TNBC-MET-2L-TDXD (DESTINY-Breast04 HER2-low) — needs DRUG-TRASTUZUMAB-DERUXTECAN ✓
- IND-BREAST-TNBC-MET-2L-OLAPARIB / TALAZOPARIB (OlympiAD / EMBRACA; gBRCA+) — needs DRUG-OLAPARIB ✓ / DRUG-TALAZOPARIB ✓
- IND-BREAST-TNBC-EARLY-PEMBRO-CHEMO-NEOADJUVANT-ADJUVANT (KEYNOTE-522) — already partially in IND-BREAST-TNBC-EARLY-NEOADJUVANT — verify pembro arm
- IND-BREAST-TNBC-EARLY-OLAPARIB-ADJUVANT (OlympiA; gBRCA+ residual disease) — needs DRUG-OLAPARIB ✓

### Drugs missing in KB (post-stubs)
- DRUG-CAPIVASERTIB — *stubbed in this commit*
- DRUG-EVEROLIMUS — **NOT stubbed** (verify; widely used — possible existing miss)
- DRUG-NERATINIB — **NOT stubbed** (HER2+ niche; out of CSD-4 scope)
- DRUG-MARGETUXIMAB — **NOT stubbed** (HER2+ niche; out of CSD-4 scope)

### Biomarkers
- BIO-ER, BIO-PR, BIO-HER2, BIO-HER2-LOW, BIO-PIK3CA-MUT, BIO-AKT1-MUT, BIO-PTEN-LOSS, BIO-ESR1-MUT, BIO-BRCA1, BIO-BRCA2, BIO-PALB2 — verify HER2-LOW and HER2-ULTRALOW definitions exist for DESTINY-Breast06.

---

## DIS-MELANOMA — Cutaneous melanoma

### Existing
- 1L metastatic indications (2): IND-MELANOMA-METASTATIC-1L-NIVO-IPI,
  IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME
- 2L+ indications: 0
- Adjuvant indications: 0 (KEYNOTE-054 / CheckMate-238 / COMBI-AD not modeled)
- 1L algorithm: ALGO-MELANOMA-METASTATIC-1L exists
- 2L+ algorithm: **missing** ← target for CSD-4-melanoma

### Needed (from NCCN Melanoma v3.2025 / ESMO Melanoma 2024)
- IND-MELANOMA-METASTATIC-1L-NIVO-RELATLIMAB (RELATIVITY-047) — needs DRUG-RELATLIMAB *S* + DRUG-NIVOLUMAB ✓
- IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO — needs DRUG-PEMBROLIZUMAB ✓
- IND-MELANOMA-BRAF-METASTATIC-1L-ENCORAFENIB-BINIMETINIB (COLUMBUS) — needs DRUG-ENCORAFENIB ✓ + DRUG-BINIMETINIB *S*
- IND-MELANOMA-BRAF-METASTATIC-1L-VEMURAFENIB-COBIMETINIB (coBRIM) — needs DRUG-VEMURAFENIB *S* + DRUG-COBIMETINIB *S*
- IND-MELANOMA-METASTATIC-2L-LIFILEUCEL (TIL therapy post-PD-1 ± BRAFi+MEKi) — needs DRUG-LIFILEUCEL *S*
- IND-MELANOMA-METASTATIC-2L-IPI-MONO (post-PD-1 progression — historical fallback) — needs DRUG-IPILIMUMAB ✓
- IND-MELANOMA-BRAF-METASTATIC-2L-IO-RECHALLENGE (post-BRAFi+MEKi → ICI doublet)
- IND-MELANOMA-ADJUVANT-PEMBRO (KEYNOTE-054; resected stage III) — needs DRUG-PEMBROLIZUMAB ✓
- IND-MELANOMA-ADJUVANT-NIVOLUMAB (CheckMate-238; resected III/IV) — needs DRUG-NIVOLUMAB ✓
- IND-MELANOMA-BRAF-ADJUVANT-DABRA-TRAME (COMBI-AD; resected III BRAF+) — needs DRUG-DABRAFENIB ✓ + DRUG-TRAMETINIB ✓
- IND-MELANOMA-NEOADJUVANT-PEMBRO (SWOG S1801; stage III) — needs DRUG-PEMBROLIZUMAB ✓
- IND-MELANOMA-METASTATIC-LATE-T-VEC (talimogene laherparepvec; injectable for in-transit) — DRUG-TALIMOGENE-LAHERPAREPVEC ✗ niche; out of CSD-4 scope

### Drugs missing in KB (post-stubs)
- DRUG-BINIMETINIB — *stubbed in this commit*
- DRUG-COBIMETINIB — *stubbed in this commit*
- DRUG-VEMURAFENIB — *stubbed in this commit*
- DRUG-RELATLIMAB — *stubbed in this commit*
- DRUG-LIFILEUCEL — *stubbed in this commit*
- DRUG-TALIMOGENE-LAHERPAREPVEC — **NOT stubbed** (niche; out of scope)

### Biomarkers
- BIO-BRAF-V600E, BIO-BRAF-V600K, BIO-NRAS-MUT, BIO-KIT-MUT, BIO-LDH (prognostic; not actionable target). Verify BIO-LAG3 not needed (no biomarker selection for relatlimab — unselected use).

---

## DIS-OVARIAN — Ovarian carcinoma

### Existing
- 1L advanced indications (2): IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG,
  IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP
- Maintenance indications (1): IND-OVARIAN-MAINTENANCE-OLAPARIB
- 2L+ indications: 0 (platinum-sensitive vs platinum-resistant relapse not modeled)
- 1L algorithm: ALGO-OVARIAN-ADVANCED-1L exists
- 2L+ algorithm: **missing** ← target for CSD-4-ovarian (likely needs split: platinum-sensitive vs platinum-resistant)

### Needed (from NCCN Ovarian v2.2025 / ESMO Ovarian 2024)

**Platinum-sensitive recurrence (≥6 mo platinum-free interval) — ALGO-OVARIAN-PLAT-SENSITIVE-2L**
- IND-OVARIAN-PLAT-SENSITIVE-2L-CARBO-DOUBLET-BEV (carbo + gem/PLD/pacli + bev maintenance, OCEANS / GOG-0213) — needs DRUG-CARBOPLATIN ✓ + DRUG-GEMCITABINE ✓ + DRUG-PEGYLATED-LIPOSOMAL-DOXORUBICIN *S* + DRUG-BEVACIZUMAB ✓
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-NIRAPARIB (NOVA all-comers post-PR/CR) — needs DRUG-NIRAPARIB ✓
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-OLAPARIB-BRCA (SOLO-2) — needs DRUG-OLAPARIB ✓
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-RUCAPARIB (ARIEL3) — needs DRUG-RUCAPARIB *S*

**Platinum-resistant recurrence (<6 mo) — ALGO-OVARIAN-PLAT-RESISTANT-2L**
- IND-OVARIAN-PLAT-RESISTANT-2L-PLD-MONO (or weekly pacli, topotecan, gem) — needs DRUG-PEGYLATED-LIPOSOMAL-DOXORUBICIN *S* + DRUG-PACLITAXEL ✓ + DRUG-TOPOTECAN *S* + DRUG-GEMCITABINE ✓
- IND-OVARIAN-PLAT-RESISTANT-2L-PLD-MONO-BEV (AURELIA) — adds DRUG-BEVACIZUMAB ✓
- IND-OVARIAN-PLAT-RESISTANT-2L-MIRVETUXIMAB-FRA-HIGH (MIRASOL) — needs DRUG-MIRVETUXIMAB-SORAVTANSINE *S*
- IND-OVARIAN-PLAT-RESISTANT-LATE-NIRAPARIB-MONO-LATE-LINE (post-multiple lines, BRCA-mut) — needs DRUG-NIRAPARIB ✓
- IND-OVARIAN-PLAT-RESISTANT-MSI-H-PEMBRO (rare) — needs DRUG-PEMBROLIZUMAB ✓

### Drugs missing in KB (post-stubs)
- DRUG-PEGYLATED-LIPOSOMAL-DOXORUBICIN — *stubbed in this commit*
- DRUG-TOPOTECAN — *stubbed in this commit*
- DRUG-MIRVETUXIMAB-SORAVTANSINE — *stubbed in this commit*
- DRUG-RUCAPARIB — *stubbed in this commit*

### Biomarkers
- BIO-BRCA1, BIO-BRCA2, BIO-HRD-STATUS, BIO-FRA-EXPRESSION (verify FRα IHC biomarker exists for mirvetuximab), BIO-MSI-H, BIO-MMR.
- BIO-FRA / BIO-FOLR1 likely missing — **flag for Wave 1 to add as new biomarker** (FOLR1 IHC ≥75% PS2+ for MIRASOL).

---

## Cross-cancer summary

| Cancer | 1L IND | 2L+ IND | Maint IND | 1L algo | 2L+ algo | New 2L+ targets |
|---|---:|---:|---:|---|---|---:|
| CRC | 3 | 4 | 0 | yes | **missing** | ~8 |
| NSCLC | 6 | 3 | 1 | yes | **missing** | ~12 |
| BREAST | 4 | 2 | 0 | yes | **missing** (3 sub-algos) | ~12 |
| MELANOMA | 2 | 0 | 0 | yes | **missing** | ~10 |
| OVARIAN | 2 | 0 | 1 | yes | **missing** (2 sub-algos) | ~9 |
| **Total** | 17 | 9 | 2 | 5 | **0 / 5+ sub-algos** | **~51** |

## Drug-stub summary (this commit)

16 stubs authored (CSD-4 in-scope):
1. DRUG-BINIMETINIB
2. DRUG-CAPIVASERTIB
3. DRUG-LIFILEUCEL
4. DRUG-MIRVETUXIMAB-SORAVTANSINE
5. DRUG-FRUQUINTINIB
6. DRUG-AMIVANTAMAB
7. DRUG-LAZERTINIB
8. DRUG-RUCAPARIB
9. DRUG-PEGYLATED-LIPOSOMAL-DOXORUBICIN
10. DRUG-TOPOTECAN
11. DRUG-COBIMETINIB
12. DRUG-VEMURAFENIB
13. DRUG-RELATLIMAB
14. DRUG-REPOTRECTINIB
15. DRUG-PRALSETINIB
16. DRUG-CEMIPLIMAB

Skipped (already exist): DRUG-SOTORASIB, DRUG-ADAGRASIB, DRUG-ELACESTRANT,
DRUG-TUCATINIB, DRUG-TRASTUZUMAB-DERUXTECAN, DRUG-RAMUCIRUMAB,
DRUG-TRIFLURIDINE-TIPIRACIL, DRUG-REGORAFENIB, DRUG-SACITUZUMAB-GOVITECAN,
DRUG-OLAPARIB, DRUG-NIRAPARIB.

Out-of-scope gaps surfaced (not stubbed; flag for follow-up authoring or Wave 1 author judgment):
- DRUG-PANITUMUMAB (CRC anti-EGFR)
- DRUG-NINTEDANIB (NSCLC LUME-Lung niche)
- DRUG-EVEROLIMUS (BREAST BOLERO-2 — verify it's truly missing first)
- DRUG-NERATINIB (BREAST HER2 niche)
- DRUG-MARGETUXIMAB (BREAST HER2 niche)
- DRUG-TALIMOGENE-LAHERPAREPVEC (MELANOMA in-transit niche)
- BIO-FOLR1 / BIO-FRA-EXPRESSION (OVARIAN — needed for mirvetuximab gating)

## Validator status

Pre-stubs (worktree baseline): ok=True (1698 entities, 167 drugs).
Post-stubs: ok=True (1714 entities, 183 drugs). 3 pre-existing contract
warnings (CML/DLBCL draft RFs) unchanged. No new errors or warnings.

(Counts on `master` HEAD are slightly higher because this worktree
branches from an earlier snapshot — delta of +16 drugs / +16 entities
applies in both contexts.)
