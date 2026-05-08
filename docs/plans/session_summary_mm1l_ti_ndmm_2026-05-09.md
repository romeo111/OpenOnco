# Session Summary: MM 1L Transplant-Ineligible Two-Plan Pair (2026-05-09)

## Overview

Authored the transplant-ineligible NDMM first-line indication pair, closing the
gap documented in IND-MM-1L-DVRD notes. PR #537 opened on `feat/mm-1l-ti-ndmm`.

---

## PR opened this session

| PR | Title | Files changed |
|----|-------|--------------|
| [#537](https://github.com/romeo111/OpenOnco/pull/537) | HEME-1 MM-1L TI-NDMM — D-Rd+Rd two-plan pair (MAIA) | ind_mm_1l_dara_rd.yaml (NEW), ind_mm_1l_rd.yaml (NEW), reg_rd_continuous.yaml (NEW), algo_mm_1l.yaml (EDIT), CLAUDE.md (EDIT) |

---

## Clinical decisions wired

### IND-MM-1L-DARA-RD (aggressive, transplant-ineligible)

| Field | Value |
|-------|-------|
| plan_track | aggressive |
| fit_for_transplant | false |
| recommended_regimen | REG-D-RD-MAIA |
| trial | MAIA (Facon NEJM 2019, PMID 30926586) |
| ORR | ~93% vs ~76% Rd |
| PFS HR | 0.56 (95% CI 0.43–0.73) |
| 5-yr OS | 66.3% vs 53.1% (HR 0.66, Facon JCO 2024) |
| HBV gate | mandatory (anti-CD38 class effect) |
| НСЗУ | daratumumab NOT reimbursed — funding gate |

### IND-MM-1L-RD (standard, transplant-ineligible)

| Field | Value |
|-------|-------|
| plan_track | standard |
| fit_for_transplant | false |
| recommended_regimen | REG-RD-CONTINUOUS (NEW) |
| trial | MAIA control arm (Facon NEJM 2019) + FIRST trial (Benboubker NEJM 2014) |
| ORR | ~76% |
| 30-mo PFS | ~38% |
| 5-yr OS | ~53% |
| НСЗУ | fully reimbursed — standard access backbone |

### REG-RD-CONTINUOUS (new regimen)

- Len 25 mg PO d1-21 + dex 40 mg weekly, 28-day cycles until progression
- Renal dose table: CrCl 30-60 → 10 mg; CrCl <30 → 5 mg daily or 10 mg qod
- Frailty adjustment: dex 20 mg if age >75 / frail; consider len 15 mg start
- mandatory_supportive_care: SUP-MM-VTE-PROPHYLAXIS + SUP-MM-BONE-PROTECTION
- Ukraine: fully НСЗУ-reimbursed; standard-access fallback for TI-NDMM

---

## algo_mm_1l.yaml changes

- `output_indications` expanded: added IND-MM-1L-RD + IND-MM-1L-DARA-RD
- `purpose` updated: documents TE/TI cohort split and transplant-gate TODO
- `notes` rewritten: transplant-gate routing via `applicable_to.demographic_constraints.fit_for_transplant`; etiology rails clarified
- `sources`: added SRC-MAIA-FACON-2019
- `last_reviewed`: 2026-05-09

---

## Test results

Short run (-x): **303 passed, 8 skipped, 1 pre-existing failure** (hero class, unrelated to this wave)
Full run: in progress (background task bkerbrnq9)

---

## Forward plan

| Area | Status | Notes |
|------|--------|-------|
| MM 1L TI-NDMM two-plan pair | ✅ PR #537 | D-Rd (MAIA) + Rd continuous; clinical signoff pending |
| MM 1L TE D-VRd phases | ✅ PR #535 merged | PERSEUS 4-phase wired |
| Transplant-gate engine support | 🔲 future | Engine doesn't yet gate on fit_for_transplant in decision_tree |
| FL-2L ORR/CR data | ⏳ pending | Full-text Lancet Oncol/JCO needed |
| NATALEE eligibility RF | 🔲 future | Node-negative + high-risk feature RF not authored |
| BREAST early low-risk HR+ | 🔲 future | IND-BREAST-HR-POS-EARLY-ADJUVANT-AI not modeled |
| Site test fix | 🔴 blocked | hero class missing; Codex session issue |
