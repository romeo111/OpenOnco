# CSD-4 Cancer Family Scope Plan (2026-04-27)

This document drives the 5 parallel Wave 1 cancer-family agents
(CRC, NSCLC, BREAST, MELANOMA, OVARIAN) for solid-tumor 2L+ expansion.
Each section enumerates the indication YAMLs, regimen YAMLs, and
algorithm YAMLs the corresponding agent should author. Drug-stub
prerequisites are tracked in `csd_4_audit_2026-04-27.md` — all CSD-4
drug stubs already landed in this commit.

---

## CSD-4-crc → DIS-CRC (Colorectal)

**Indications to author (~8):**
- IND-CRC-METASTATIC-2L-MSI-H-NIVO-IPI (CheckMate-8HW post-pembro)
- IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB-TRASTUZUMAB (MOUNTAINEER)
- IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD (DESTINY-CRC02)
- IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-PANITUMUMAB (CodeBreaK 300) — gated on DRUG-PANITUMUMAB stub
- IND-CRC-METASTATIC-2L-KRAS-G12C-ADAGRASIB-CETUXIMAB (KRYSTAL-10)
- IND-CRC-METASTATIC-3L-FRUQUINTINIB (FRESCO-2)
- IND-CRC-METASTATIC-3L-NTRK-LAROTRECTINIB (tumor-agnostic)
- IND-CRC-MAINTENANCE-CAPE-BEV (post-induction maintenance)

**Algorithm:** ALGO-CRC-METASTATIC-2L
- Branches: HER2-amp → MOUNTAINEER/T-DXd; BRAF V600E → BEACON (existing IND);
  KRAS G12C → adagrasib+cetux/sotorasib+panit; MSI-H post-pembro → nivo+ipi;
  NTRK/RET fusion → tumor-agnostic TKI; default RAS-mut → FOLFIRI±bev (existing IND);
  3L+ → fruquintinib / regorafenib / TAS-102 (existing INDs).

**Regimens to author (~6):**
- REG-NIVO-IPI-CRC-MSIH (note: distinct from melanoma nivo+ipi dosing — q3w ipi 1 mg/kg + nivo 240 mg q3w x4 then nivo 480 mg q4w)
- REG-TUCATINIB-TRASTUZUMAB-CRC (HER2CRC dosing — different from breast HER2CLIMB; no capecitabine)
- REG-T-DXD-CRC (5.4 mg/kg q3w; same dose as breast)
- REG-SOTORASIB-PANITUMUMAB
- REG-ADAGRASIB-CETUXIMAB
- REG-FRUQUINTINIB-MONO (5 mg PO daily 3w/1w)
- REG-CAPE-BEV-MAINTENANCE

**Prerequisites (drugs):** all in KB except DRUG-PANITUMUMAB — Wave 1
agent should stub-author panitumumab as part of its commit, OR drop the
sotorasib-panitumumab indication and rely on adagrasib-cetuximab for KRAS G12C.

---

## CSD-4-nsclc → DIS-NSCLC

**Indications to author (~12):**
- IND-NSCLC-EGFR-1L-AMIVANTAMAB-LAZERTINIB (MARIPOSA — alt to osimertinib)
- IND-NSCLC-EGFR-2L-AMIVANTAMAB-CHEMO (MARIPOSA-2 post-osimertinib)
- IND-NSCLC-EGFR-EXON20-AMIVANTAMAB (CHRYSALIS)
- IND-NSCLC-EGFR-MET-AMP-2L-TEPOTINIB-OSIMERTINIB (post-osi resistance)
- IND-NSCLC-ROS1-1L-REPOTRECTINIB (TRIDENT-1 TKI-naive)
- IND-NSCLC-ROS1-2L-REPOTRECTINIB (TRIDENT-1 post-crizotinib)
- IND-NSCLC-RET-1L-SELPERCATINIB (LIBRETTO-431)
- IND-NSCLC-MET-EX14-CAPMATINIB (GEOMETRY mono-1)
- IND-NSCLC-HER2-MUT-2L-T-DXD (DESTINY-Lung01/02)
- IND-NSCLC-KRAS-G12C-2L-ADAGRASIB (KRYSTAL-1) — alt to existing sotorasib IND
- IND-NSCLC-PDL1-HIGH-1L-CEMIPLIMAB (EMPOWER-Lung 1) — alt to pembro
- IND-NSCLC-EARLY-OSIMERTINIB-ADJUVANT (ADAURA — EGFR+ resected stage IB-IIIA)
- IND-NSCLC-EARLY-ATEZO-ADJUVANT (IMpower010 — PD-L1+ resected II-IIIA)
- IND-NSCLC-EARLY-PEMBRO-NEOADJUVANT (KEYNOTE-671 — perioperative)

**Algorithm:** ALGO-NSCLC-METASTATIC-2L
- Driver-resistance subway: EGFR → MARIPOSA-2 / T-DXd-MET / tepotinib-MET-amp;
  ALK → lorlatinib (existing); ROS1 → repotrectinib; KRAS G12C → sotorasib/adagrasib;
  driver-negative post-IO → docetaxel±ramucirumab (existing) or T-DXd HER2-mut.

Optional: ALGO-NSCLC-EARLY-ADJUVANT (separate algo for adjuvant decision tree:
osimertinib EGFR+ vs atezolizumab PD-L1+ vs no adjuvant chemo-only).

**Regimens to author (~10):**
- REG-AMIVANTAMAB-LAZERTINIB (MARIPOSA)
- REG-AMIVANTAMAB-CARBO-PEMETREXED (MARIPOSA-2)
- REG-AMIVANTAMAB-MONO (CHRYSALIS exon 20)
- REG-TEPOTINIB-OSIMERTINIB (off-label-by-trial; MET-amp post-osi)
- REG-REPOTRECTINIB-MONO (160 mg lead-in then 160 BID)
- REG-CAPMATINIB-MONO
- REG-T-DXD-NSCLC (HER2-mut)
- REG-ADAGRASIB-MONO (KRAS G12C)
- REG-CEMIPLIMAB-MONO (350 mg q3w)
- REG-OSIMERTINIB-ADJUVANT (3y duration ADAURA)
- REG-ATEZOLIZUMAB-ADJUVANT (1y IMpower010)

**Prerequisites:** Verify DRUG-NINTEDANIB if LUME-Lung indication included.
All other drugs in KB (incl. CSD-4 stubs amivantamab, lazertinib, repotrectinib,
pralsetinib, cemiplimab).

---

## CSD-4-breast → DIS-BREAST (3 sub-algorithms)

**ALGO-BREAST-HR-POS-2L (HR+/HER2- metastatic 2L+)**

Indications (~6):
- IND-BREAST-HR-POS-MET-2L-CAPIVASERTIB-FULVESTRANT (CAPItello-291; PIK3CA/AKT1/PTEN+)
- IND-BREAST-HR-POS-MET-2L-ALPELISIB-FULVESTRANT (SOLAR-1; PIK3CA-mut)
- IND-BREAST-HR-POS-MET-2L-ELACESTRANT (EMERALD; ESR1-mut)
- IND-BREAST-HR-POS-MET-2L-EVEROLIMUS-EXEMESTANE (BOLERO-2)
- IND-BREAST-HR-POS-MET-2L-FULVESTRANT-MONO (post-AI; biomarker-untargeted)
- IND-BREAST-HR-POS-MET-3L-TDXD (DESTINY-Breast06; HER2-low/ultralow)

Branching: PIK3CA-mut → alpelisib OR capivasertib (capivasertib if AKT1/PTEN
co-altered or post-alpelisib intolerance); ESR1-mut → elacestrant; HER2-low →
T-DXd; mTOR-naive PI3K-WT → everolimus-exemestane; default → fulvestrant-mono.

**ALGO-BREAST-HER2-POS-2L (HER2+ metastatic 2L+)**

Indications (~3-4):
- IND-BREAST-HER2-POS-MET-3L-TUCATINIB-TRASTUZUMAB-CAPECITABINE (HER2CLIMB; brain mets)
- IND-BREAST-HER2-POS-MET-3L-T-DM1 (EMILIA; alt to T-DXd 2L per access)
- (IND-BREAST-HER2-POS-MET-2L-TDXD already exists)

Branching: brain mets present → tucatinib triplet (CNS-active);
no brain mets → T-DXd 2L (existing) → T-DM1 3L; chemo-rechallenge later lines.

**ALGO-BREAST-TNBC-2L (TNBC metastatic 2L+)**

Indications (~3):
- IND-BREAST-TNBC-MET-2L-SACITUZUMAB-GOVITECAN (ASCENT)
- IND-BREAST-TNBC-MET-2L-TDXD-HER2-LOW (DESTINY-Breast04)
- IND-BREAST-TNBC-MET-2L-OLAPARIB / TALAZOPARIB (OlympiAD/EMBRACA; gBRCA+)
- IND-BREAST-TNBC-EARLY-OLAPARIB-ADJUVANT (OlympiA; gBRCA+ residual disease)

Branching: gBRCA+ → PARPi; HER2-low → T-DXd; default → SG.

**Regimens to author (~10):**
- REG-CAPIVASERTIB-FULVESTRANT
- REG-ALPELISIB-FULVESTRANT
- REG-ELACESTRANT-MONO
- REG-EVEROLIMUS-EXEMESTANE
- REG-FULVESTRANT-MONO
- REG-T-DXD-BREAST (already may exist for IND-BREAST-HER2-POS-MET-2L-TDXD; verify)
- REG-TUCATINIB-TRAS-CAPE (HER2CLIMB)
- REG-T-DM1-MONO
- REG-SACITUZUMAB-GOVITECAN-MONO
- REG-OLAPARIB-MONO-BREAST (likely exists for IND-BREAST-BRCA-POS-MET-PARPI; verify)
- REG-TALAZOPARIB-MONO-BREAST

**Prerequisites:** Verify DRUG-EVEROLIMUS exists; if missing, stub it.
All other drugs in KB (incl. CSD-4 stub capivasertib).

---

## CSD-4-melanoma → DIS-MELANOMA

**Indications to author (~10):**
- IND-MELANOMA-METASTATIC-1L-NIVO-RELATLIMAB (RELATIVITY-047; alt to nivo+ipi)
- IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO (KEYNOTE-006 historical reference)
- IND-MELANOMA-BRAF-METASTATIC-1L-ENCORAFENIB-BINIMETINIB (COLUMBUS — alt to dabra+trame existing)
- IND-MELANOMA-BRAF-METASTATIC-1L-VEMURAFENIB-COBIMETINIB (coBRIM)
- IND-MELANOMA-METASTATIC-2L-LIFILEUCEL (post anti-PD-1 ± BRAFi+MEKi)
- IND-MELANOMA-METASTATIC-2L-IPI-MONO (post-PD-1; historical fallback)
- IND-MELANOMA-BRAF-METASTATIC-2L-IO-RECHALLENGE (post-BRAFi+MEKi → ICI doublet)
- IND-MELANOMA-ADJUVANT-PEMBRO (KEYNOTE-054; resected stage III)
- IND-MELANOMA-ADJUVANT-NIVOLUMAB (CheckMate-238; resected III/IV)
- IND-MELANOMA-BRAF-ADJUVANT-DABRA-TRAME (COMBI-AD; resected III BRAF+)
- IND-MELANOMA-NEOADJUVANT-PEMBRO (SWOG S1801)

**Algorithms:**
- ALGO-MELANOMA-METASTATIC-2L (post-1L-progression — IO vs targeted alternation)
- ALGO-MELANOMA-ADJUVANT (separate decision tree — stage III/IV resected →
  PD-1 mono adjuvant vs BRAFi+MEKi if BRAF V600+)

**Regimens to author (~9):**
- REG-NIVO-RELATLIMAB (Opdualag fixed-dose q4w)
- REG-PEMBRO-MELANOMA-MONO
- REG-ENCORAFENIB-BINIMETINIB
- REG-VEMURAFENIB-COBIMETINIB
- REG-LIFILEUCEL-PROTOCOL (lymphodepletion → TIL infusion → IL-2)
- REG-IPI-MONO-MELANOMA-2L (3 mg/kg q3w x4)
- REG-PEMBRO-ADJUVANT-MELANOMA (200 mg q3w x12 mo)
- REG-NIVO-ADJUVANT-MELANOMA (480 mg q4w x12 mo)
- REG-DABRA-TRAME-ADJUVANT (12 mo)

**Prerequisites:** All drugs in KB (incl. CSD-4 stubs binimetinib,
cobimetinib, vemurafenib, relatlimab, lifileucel).

---

## CSD-4-ovarian → DIS-OVARIAN (2 sub-algorithms)

**ALGO-OVARIAN-PLAT-SENSITIVE-2L (≥6 mo platinum-free interval)**

Indications (~5):
- IND-OVARIAN-PLAT-SENSITIVE-2L-CARBO-GEM-BEV (OCEANS)
- IND-OVARIAN-PLAT-SENSITIVE-2L-CARBO-PLD-BEV (CALYPSO + GOG-0213)
- IND-OVARIAN-PLAT-SENSITIVE-2L-CARBO-PACLI-BEV (GOG-0213)
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-NIRAPARIB (NOVA all-comers post-PR/CR)
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-OLAPARIB-BRCA (SOLO-2)
- IND-OVARIAN-PLAT-SENSITIVE-MAINTENANCE-RUCAPARIB (ARIEL3)

Branching: BRCA-mut → olaparib maintenance preferred; BRCA-WT/HRD-pos →
niraparib maintenance; full-platinum-doublet choice (gem vs PLD vs pacli)
based on prior tox / patient preference; bev maintenance if not in 1L.

**ALGO-OVARIAN-PLAT-RESISTANT-2L (<6 mo platinum-free interval)**

Indications (~4):
- IND-OVARIAN-PLAT-RESISTANT-2L-PLD-MONO (or weekly pacli, topotecan, gem)
- IND-OVARIAN-PLAT-RESISTANT-2L-PLD-BEV (AURELIA)
- IND-OVARIAN-PLAT-RESISTANT-2L-MIRVETUXIMAB-FRA-HIGH (MIRASOL — FRα IHC ≥75% PS2+)
- IND-OVARIAN-PLAT-RESISTANT-MSI-H-PEMBRO (rare — tumor-agnostic)

Branching: FRα-high → mirvetuximab (treatment-defining for the subset);
MSI-H → pembrolizumab; default → single-agent chemo ± bev.

**Regimens to author (~8):**
- REG-CARBO-GEM-BEV
- REG-CARBO-PLD-BEV
- REG-CARBO-PACLI-BEV-2L (slightly different schedule from 1L)
- REG-NIRAPARIB-MAINTENANCE
- REG-RUCAPARIB-MAINTENANCE
- REG-PLD-MONO (40-50 mg/m² q4w)
- REG-PLD-BEV (PLD + bev 10 mg/kg q2w)
- REG-MIRVETUXIMAB-MONO (6 mg/kg adj-IBW q3w)

**Prerequisites:**
- Verify BIO-FOLR1 / BIO-FRA-EXPRESSION biomarker exists; if not, Wave 1
  agent should add (FOLR1 IHC ≥75% PS2+ for MIRASOL gating).
- All drugs in KB (incl. CSD-4 stubs PLD, topotecan, mirvetuximab, rucaparib).

---

## Wave 1 sequencing notes

- **Independent agents:** all 5 cancers are mutually independent — no
  shared regimens / indications across families. Run all 5 in parallel.
- **Drug-stub follow-ups (out of CSD-4 scope):** panitumumab (CRC),
  nintedanib (NSCLC), everolimus (BREAST — verify first), neratinib
  (BREAST), margetuximab (BREAST), talimogene-laherparepvec (MELANOMA).
  These are flagged but NOT blockers for Wave 1; agents should either
  drop the corresponding indication or stub-author the drug as part of
  their own commit.
- **Biomarker follow-up:** BIO-FOLR1 / BIO-FRA-EXPRESSION (OVARIAN) is the
  one likely-missing biomarker — Wave 1 ovarian agent should add it OR
  surface as gap.
- **Validator gate:** every Wave 1 agent must run the loader CLI before
  commit (`C:/Python312/python.exe -m knowledge_base.validation.loader
  knowledge_base/hosted/content`) and the result must remain `ok=True`
  (1714 entities baseline post-CSD-4 stubs in this worktree; ~1769 on
  master HEAD — delta unchanged).
