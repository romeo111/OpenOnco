# Session Summary: MM 1L §17 IndicationPhase (2026-05-09)

## Overview

Wired `IND-MM-1L-DVRD` as a 4-phase phased indication per the ratified §17
IndicationPhase schema (PR #427). PERSEUS protocol fully modeled:
D-VRd × 4 induction → ASCT → D-VRd × 2 consolidation → dara-len maintenance.

---

## PR merged this session

| PR | Title | Files changed |
|----|-------|--------------|
| [#535](https://github.com/romeo111/OpenOnco/pull/535) | HEME-1 MM-1L §17 phases — D-VRd+ASCT+dara-len maintenance (PERSEUS) | proc_asct.yaml (NEW), reg_dara_len_maintenance.yaml (NEW), ind_mm_1l_dvrd.yaml (EDIT), CLAUDE.md |

---

## Clinical decisions wired

### IND-MM-1L-DVRD phases (PERSEUS, PMID 38084760)

| Phase | Entity | Detail |
|-------|--------|--------|
| induction | REG-DARA-VRD × 4 cycles | D+V+R+d, 28-day cycles; stem cell harvest after cycle 4 |
| surgery | SUR-ASCT-AUTOLOGOUS (6 wk) | HDM/mel-200 + PBSC reinfusion; ~3-4 wk inpatient |
| adjuvant | REG-DARA-VRD × 2 cycles | Consolidation per PERSEUS post-ASCT |
| maintenance | REG-DARA-LEN-MAINTENANCE | Dara SC q4w (→q8w after cycle 6) + len 10mg d1-21 until progression |

### Scope gate added
`fit_for_transplant: true` in `applicable_to.demographic_constraints` —
explicitly restricts IND-MM-1L-DVRD to transplant-eligible NDMM.

### Transplant-ineligible gap documented (not yet modeled)
D-Rd (MAIA, Facon NEJM 2019) and D-VRd×6 (GRIFFIN-style) for non-transplant-eligible
NDMM: flagged in notes, pending HEME backlog wave.

---

## New entities

- **SUR-ASCT-AUTOLOGOUS** (`proc_asct.yaml`): stem_cell_transplant / consolidation intent;
  applicable to DIS-MM; EBMT TRM 1-3%; 10 common complication entries; Ukraine BMT center note
- **REG-DARA-LEN-MAINTENANCE** (`reg_dara_len_maintenance.yaml`): dara 1800mg SC q4w
  (→q8w after cycle 6) + len 10mg d1-21 q28d until progression (PERSEUS schedule);
  5 dose_adjustments; 6 between_visit_watchpoints; ukraine_availability note (dara not
  НСЗУ-reimbursed → REG-LENALIDOMIDE-MAINTENANCE is standard-access fallback)

---

## ind_mm_1l_dvrd.yaml changes

- `recommended_regimen:` → null (phases present; `_has_authored_treatment_phases()` satisfies
  loader contract — no routing error)
- `demographic_constraints.fit_for_transplant: true` added
- `phases:` block added (4 entries, XOR FK per phase, schema-valid)
- `notes` updated: transplant-ineligible gap + phases wiring provenance
- `last_reviewed` updated to 2026-05-09

---

## Test results

Full suite (skipping pre-existing hero failure): **2164 passed, 34 pre-existing failures, 9 skipped**

All 34 remaining failures are pre-existing on master and unrelated to this wave.

### Fixups applied in continuation session (2026-05-09)

Three bugs were caught by the full suite and corrected before final push:

| Commit | Bug | Fix |
|--------|-----|-----|
| `89c393c` | `SUP-ANTIINFECTIVE-PROPHYLAXIS-MM` invented FK in `mandatory_supportive_care` | Removed; only `SUP-MM-VTE-PROPHYLAXIS` + `SUP-MM-BONE-PROTECTION` remain |
| `d6dea10` | `proc_asct.yaml` `intent: consolidation` — not in `Surgery.intent` enum (`curative\|palliative\|diagnostic\|salvage`) | Changed to `intent: curative` (curative-intent taxonomy for transplant-eligible NDMM) |
| `d6dea10` | `ind_mm_1l_dvrd.yaml` `recommended_regimen:` nulled — engine reads this field for track routing; `phases` support in engine is pending | Restored `recommended_regimen: REG-DARA-VRD`; `phases:` block is additive metadata for future renderer |

Pre-existing failure (out of scope):
- `test_landing_is_public_with_hero_and_ctas` — Codex site-redesign removed `class="hero"`;
  requires site team fix or test update.

---

## Forward plan

| Area | Status | Notes |
|------|--------|-------|
| MM 1L D-VRd phases | ✅ complete | PERSEUS 4-phase fully wired; PR #535 |
| Transplant-ineligible NDMM | 🔲 next | D-Rd (MAIA) + D-VRd×6 as separate IND-MM-1L-DARA-RD entity |
| Site test fix | 🔴 blocked | hero class missing; Codex session issue |
| FL-2L ORR/CR data | ⏳ pending | Full-text Lancet Oncol/JCO needed |
| NATALEE eligibility RF | 🔲 future | Node-negative + high-risk feature RF not authored |
| BREAST early low-risk HR+ | 🔲 future | IND-BREAST-HR-POS-EARLY-ADJUVANT-AI not modeled |
