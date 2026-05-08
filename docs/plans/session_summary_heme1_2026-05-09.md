# HEME-1 session summary

**Stamp:** 2026-05-09
**Master HEAD at close:** `79f7ca520` (post HEME-1 D1 merge)
**Session span:** 2026-05-09 (continuation of 2026-05-09 PUL-close session)
**PRs merged this session:** #513 (PUL-D), #514 (HEME-1 A2), #515 (HEME-1 W0), #516 (HEME-1 A3), #517 (HEME-1 A1), #518 (HEME-1 D1)

---

## 1. PUL wave closed (this session)

All pulmonary chunks landed. Summary:

| PR | Chunk | Content |
|---|---|---|
| #505 | PUL-A6 | NSCLC adjuvant atezo (IMpower010) — IND-NSCLC-ADJUVANT-ATEZO-PDL1POS + REG-ATEZO-ADJUVANT-NSCLC |
| #506 | PUL-A8 | NSCLC 1L nivo+ipi+chemo (CheckMate-9LA) — IND-NSCLC-DRIVER-NEG-MET-1L-NIVO-IPI-CHEMO + REG-NIVO-IPI-CHEMO-NSCLC-1L |
| #507 | PUL-A7 | Mesothelioma 2L nivo (CONFIRM) — IND-MESOTHELIOMA-2L-NIVO + REG-NIVO-MONO-MESOTHELIOMA-2L |
| #513 | PUL-D | 3 NEW algos (NSCLC-resectable-periop, mesothelioma-2l, NSCLC-adjuvant) + 3 EDITS (SCLC-1l, SCLC-2l, NSCLC-metastatic-1l) |

PUL-D notes:
- `algo_sclc_1l`: added ADRIATIC durvalumab consolidation gate (step 2)
- `algo_sclc_2l`: inserted DLL3 tarlatamab gate (step 3); renumbered steps 3→4, 4→5, 5→6
- `algo_nsclc_metastatic_1l`: added CheckMate-9LA MDT gate (step 10)

---

## 2. HEME-1 wave (this session)

### 2.1 Entity tally

| Category | NEW | Notes |
|---|---|---|
| Sources | 3 | POLARIX (Tilly NEJM 2022), PERSEUS (Sonneveld NEJM 2024), AMPLIFY (Brown NEJM 2025) |
| Regimens | 2 | REG-ISA-KD-MM-3L, REG-AVO-CLL-1L |
| Indications NEW | 2 | IND-MM-3L-ISA-KD, IND-CLL-1L-AVO |
| Indications EDIT | 2 | ind_dlbcl_1l_pola_r_chp (POLARIX backfill), ind_mm_1l_dvrd (PERSEUS + GRIFFIN backfill) |
| Algorithms NEW | 1 | ALGO-MM-3L |
| Algorithms EDIT | 1 | ALGO-CLL-1L (AVO branch + zanubrutinib preserved) |

### 2.2 PRs

| PR | Chunk | Content |
|---|---|---|
| #515 | HEME-1 W0 | 3 NEW sources: SRC-POLARIX-TILLY-2022, SRC-PERSEUS-SONNEVELD-2024, SRC-AMPLIFY-BROWN-2025 |
| #514 | HEME-1 A2 | IND-MM-3L-ISA-KD + REG-ISA-KD-MM-3L (IKEMA PFS HR 0.531) |
| #517 | HEME-1 A1 | IND-CLL-1L-AVO + REG-AVO-CLL-1L (AMPLIFY 3-arm, PFS HR 0.42) |
| #516 | HEME-1 A3 | Backfill primary sources into pola-R-CHP + DVRd indications |
| #518 | HEME-1 D1 | ALGO-MM-3L (NEW) + ALGO-CLL-1L EDIT (AVO step 4) |

### 2.3 PMID defect findings (W0)

All 3 PMIDs in the W0 brief were wrong (~100% defect rate, consistent with session history §10.1):

| Trial | Brief PMID | Correct PMID | Correction |
|---|---|---|---|
| POLARIX | 36197394 (nursing study) | 34904799 | First author Tilly H (not André) → source ID changed |
| PERSEUS | 38364583 (GLP1R diabetes) | 38084760 | Sonneveld confirmed |
| AMPLIFY | 38949978 (ACTN4 nephrotic) | 39976417 | First author Brown JR (not Neal); year 2025; 3-arm design |

---

## 3. Forward plan

### 3.1 HEME-1 continuation (next wave)

Wave 2 candidates for next session:

- **HEME-1 B1** DLBCL algo (`algo_dlbcl_1l.yaml`) — already has pola-R-CHP source backfilled; add routing for POLARIX pola-R-CHP vs R-CHOP
- **HEME-1 B2** MM 1L DVRd algo — DVRd sources backfilled (PERSEUS + GRIFFIN); extend `algo_mm_1l.yaml` for DVRd branch
- **HEME-1 A4** CLL 2L — venetoclax+rituximab (MURANO, SRC-MURANO-SEYMOUR-2018 exists?); verify
- **HEME-1 A5** DLBCL 2L+ CAR-T (axi-cel ZUMA-7 / liso-cel TRANSFORM) — high-impact gap; UA access near-zero but schema coverage needed
- **HEME-1 A6** MM 1L transplant-eligible (DVRd induction + ASCT + dara-len maint, PERSEUS) — expand `ind_mm_1l_dvrd.yaml` with §17 phases

### 3.2 Future domain waves

Per `docs/plans/session_tally_and_forward_plan_2026-05-09.md` §2.3:
- **Breast** — monarchE abemaciclib, NATALEE ribociclib, KEYNOTE-522 TNBC, DB-04
- **GU** — EV-302 enfortumab+pembro, PROpel/MAGNITUDE PARPi prostate
- **Gyn** — KN-826 cervical, RUBY + NRG-GY018 endometrial

### 3.3 Backlog (low priority)

- Source-ID renormalisation #400 (hyphenation cleanup, large blast radius)
- ALGO-CRC state-agnostic collision (engine refactor)
- §18 PROPOSAL: patient-trajectory entity (longitudinal)
- Phase 1.5 BMA two-Clinical-Co-Lead signoff queue

---

## 4. Resumption checklist

1. Verify master HEAD (should be ≥ `79f7ca520`)
2. Read this doc + `docs/plans/session_tally_and_forward_plan_2026-05-09.md`
3. Check `docs/plans/refactor_lessons_2026-05-07.md` for patterns
4. Decide: continue HEME-1 wave 2 (B1 DLBCL algo + B2 MM algo) or pivot to breast/GU/gyn
5. W0 pattern: always verify PMIDs via PubMed fetch before writing source stubs

---

## 5. Reference docs

- `docs/plans/session_tally_and_forward_plan_2026-05-09.md` — PUL + prior session tally
- `docs/plans/gi3_wave_closure_summary_2026-05-08.md` — GI-3 17-PR ledger
- `docs/plans/refactor_lessons_2026-05-07.md` — 11+ sections, 36+ patterns
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` — canonical schema (§17 ratified)
- `CLAUDE.md` — repo conventions
