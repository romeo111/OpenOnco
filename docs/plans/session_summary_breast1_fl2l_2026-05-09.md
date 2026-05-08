# Session Summary: BREAST-1 wave + FL-2L gap fill (2026-05-09)

## Overview

This session continued from the HEME-1 wave (which completed earlier) and ran two content
waves: BREAST-1 (early HR+ adjuvant CDK4/6i wiring) and FL-2L (GADOLIN + AUGMENT gap fill).
Also included a citation schema hotfix that resolved cascading E2E test failures.

---

## PRs merged this session (post-context)

| PR | Title | Files changed |
|----|-------|--------------|
| [#526](https://github.com/romeo111/OpenOnco/pull/526) | BREAST-1 W0+A1 — KN-522 source + TNBC neoadjuvant backfill | src_keynote522_schmid_2022.yaml (NEW), ind_breast_tnbc_early_neoadjuvant.yaml (EDIT) |
| [#527](https://github.com/romeo111/OpenOnco/pull/527) | BREAST-1 A2 — monarchE source + abemaciclib adjuvant | src_monarche_johnston_2023.yaml (NEW), reg_abemaciclib_adjuvant.yaml (NEW), ind_breast_hr_pos_early_adjuvant_cdk46i.yaml (NEW) |
| [#528](https://github.com/romeo111/OpenOnco/pull/528) | BREAST-1 D1 — route early HR+ to adjuvant CDK4/6i; fix bma_bap1 | algo_breast_1l.yaml (EDIT), bma_bap1_mut_rcc_prognostic.yaml (FIX) |
| [#529](https://github.com/romeo111/OpenOnco/pull/529) | hotfix — Citation.position primary/supporting → supports | ind_cll_2l_venr_murano.yaml, ind_dlbcl_1l_pola_r_chp.yaml, ind_mm_1l_dvrd.yaml |
| [#530](https://github.com/romeo111/OpenOnco/pull/530) | BREAST-1 A3 — NATALEE source + ribociclib adjuvant indication | src_natalee_slamon_2024.yaml (NEW), reg_ribociclib_ai_adjuvant.yaml (NEW), ind_breast_hr_pos_early_adjuvant_ribociclib.yaml (NEW) |
| [#531](https://github.com/romeo111/OpenOnco/pull/531) | BREAST-1 D2 — wire ribociclib into breast 1L algo | algo_breast_1l.yaml (EDIT: IND-BREAST-HR-POS-EARLY-ADJ-RIBOCICLIB + SRC-NATALEE) |
| [#532](https://github.com/romeo111/OpenOnco/pull/532) | FL-2L — GADOLIN + AUGMENT complete wave | src_gadolin_sehn_2016.yaml (NEW), src_augment_leonard_2019.yaml (NEW), reg_obinutuzumab_benda.yaml (NEW), reg_rituximab_lenalidomide_r2.yaml (NEW), ind_fl_2l_obg_benda.yaml (NEW), ind_fl_2l_r2.yaml (NEW), algo_fl_2l.yaml (EDIT: line 3→2, steps 0+01 added) |
| [#533](https://github.com/romeo111/OpenOnco/pull/533) | chore — KB entity count update; correct redflags 510→474 | CLAUDE.md |

---

## BREAST-1 wave summary

### Clinical decisions wired
- **Early HR+/HER2- high-risk adjuvant (step 5 in algo_breast_1l.yaml)**:
  - Default: `IND-BREAST-HR-POS-EARLY-ADJ-CDK46I` (abemaciclib 2yr, monarchE criteria)
  - Alternative: `IND-BREAST-HR-POS-EARLY-ADJ-RIBOCICLIB` (ribociclib 3yr, NATALEE — broader eligibility including node-negative + ≥1 risk factor)
  - Distinction: abemaciclib requires ≥4 nodes OR 1-3 nodes + Ki67≥20%/grade 3; ribociclib broader but requires QTc monitoring

### Key PMID corrections (100% defect rate in briefs confirmed again)
| Brief PMID | Correct PMID | Error |
|-----------|-------------|-------|
| 35320644 (DESTINY-Breast03) | 35139274 | Wrong trial entirely |
| 37379993 (GI endoscopy) | 36493792 | Wrong paper entirely |
| Any NATALEE guess | 38507751 | Year also wrong (2024, not 2023); journal vol 390 not 388 |

### New entities
- Sources: SRC-KEYNOTE-522-SCHMID-2022 (PMID 35139274), SRC-MONARCHE-JOHNSTON-2023 (PMID 36493792), SRC-NATALEE-SLAMON-2024 (PMID 38507751)
- Indications: IND-BREAST-HR-POS-EARLY-ADJ-CDK46I, IND-BREAST-HR-POS-EARLY-ADJ-RIBOCICLIB
- Regimens: REG-ABEMACICLIB-ADJUVANT (150mg BID × 2yr), REG-RIBOCICLIB-AI-ADJUVANT (400mg QD d1-21 × 3yr)

---

## FL-2L wave summary

### Gap filled
`algo_fl_2l.yaml` was mis-labeled as `applicable_to_line_of_therapy: 3` (routing to EZH2/CAR-T/mosunetuzumab 3L+ options) with no true 2L indication. Now wired:
- Step 0: prior_lines ≤1 → step 01 (true 2L routing)
- Step 01: rituximab-refractory → `IND-FL-2L-OBG-BENDA` (standard); rituximab-sensitive → `IND-FL-2L-R2` (aggressive chemo-free)
- Existing steps 1-3 unchanged (EZH2/CAR-T/mosunetuzumab for ≥2 prior lines)

### Key PMID corrections
| Brief guess | Correct PMID | Trial |
|------------|-------------|-------|
| Not specified | 27345636 | GADOLIN (Sehn LH, Lancet Oncol 2016) |
| Not specified | 30897038 | AUGMENT (Leonard JP, JCO 2019) |

### PFS data (abstract-verified; ORR/CR pending full-text)
- GADOLIN: PFS HR 0.55 (rituximab-refractory iNHL)
- AUGMENT: PFS HR 0.46 (r/r FL/MZL)

### New entities
- Sources: SRC-GADOLIN-SEHN-2016, SRC-AUGMENT-LEONARD-2019
- Indications: IND-FL-2L-OBG-BENDA (standard), IND-FL-2L-R2 (aggressive)
- Regimens: REG-OBINUTUZUMAB-BENDA, REG-RITUXIMAB-LENALIDOMIDE-R2

---

## Hotfix (#529): Citation.position schema violations

Three indication files had `position: primary` or `position: supporting` in source citations — both invalid per the Citation schema (only `supports`, `contradicts`, `context` accepted). These caused cascade failures in E2E tests (KB load error → test failure).

Files fixed: `ind_cll_2l_venr_murano.yaml`, `ind_dlbcl_1l_pola_r_chp.yaml`, `ind_mm_1l_dvrd.yaml`.

**Invariant to carry forward**: after adding sources to any indication, always verify `position:` is one of `supports`/`contradicts`/`context`.

---

## bma_bap1 fix (bundled in #528)
Pre-existing test failures in `bma_bap1_mut_rcc_prognostic.yaml`:
- `escat_tier: "III"` → `"IIIB"` (ESCAT valid values: IA/IB/IIA/IIB/IIIA/IIIB/IV/X)
- Added missing `primary_sources` and `last_verified` fields

---

## Remaining pre-existing test failures (not from this session)
1. `test_landing_is_public_with_hero_and_ctas` — site redesign (Codex session) removed `class="hero"` from landing page; test expects it. Requires site team to update test OR revert/update the hero class.
2. Various `test_curated_chunk_e2e` errors — external service/fixture issues unrelated to KB content.

---

## Forward plan

| Area | Status | Notes |
|------|--------|-------|
| BREAST-1 wave | ✅ complete | KN-522, monarchE, NATALEE sources; 2 early adjuvant indications; algo routed |
| FL-2L gap | ✅ filled | GADOLIN + AUGMENT; algo line corrected 3→2 |
| Site test fix | 🔴 blocked | landing page hero class missing; Codex session issue |
| ORR/CR data for FL-2L | ⏳ pending | Lancet Oncol/JCO full-text needed |
| HEME-1 long-tail MM 1L phases | 🔲 next | §17 IndicationPhase schema for D-VRd+ASCT+maintenance |
| NATALEE eligibility RF | 🔲 future | node-negative + high-risk feature RF not yet authored |
| BREAST early low-risk HR+ adjuvant AI | 🔲 future | IND-BREAST-HR-POS-EARLY-ADJUVANT-AI not modeled |
