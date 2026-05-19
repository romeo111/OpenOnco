# Wave L KB Coverage Report — 2026-05-19

**Branch:** `wave-l-prep-2026-05-19` (PR #611)
**Baseline:** master tip `d60004b723` (post-PR #610 merge)
**Status:** in-flight; Wave M agents running in parallel.

## Headline metrics

| Metric | Baseline | Wave L | Δ |
|---|---|---|---|
| Total entities | ~3,770 | 3,868 | +98 |
| RedFlags (all categories) | 100 | 121 | +21 |
| Prevention indications | 188 | 246 | +58 |
| Ref errors | 0 | 0 | — |
| Contract errors | 0 | 0 | — |
| Pre-existing biomarker schema errors | 15 | 15 | — |

## RedFlag breakdown by `risk_category`

| Category | Baseline | Wave L | Δ | Notes |
|---|---|---|---|---|
| genetic | 28 | 45 | +17 | ATM/PALB2/CHEK2/BARD1/BRIP1/RAD51C-D carriers (6); NF1/CDH1/CMMRD (3); cascade pilots Lynch/BRCA/LFS/VHL/FAP (5) |
| occupational | 17 | 21 | +4 | IARC 2A: glyphosate, shiftwork, PCB, frying-emissions |
| iatrogenic | 20 | 22 | +2 | MTX-LPD, I-131 secondary cancer |
| chronic_condition | 14 | 16 | +2 | T2DM multi-organ, NAFLD/MASLD HCC |
| lifestyle | 11 | 16 | +5 | smokeless tobacco, SSBs, salty/pickled diet, red meat HIGH, hot maté |
| infectious | 13 | 13 | — | (Wave J completed coverage; Wave L did not add) |
| reproductive | 3 | 7 | +4 | DES in-utero, endometriosis-ovarian, high-parity-cervical, PCOS-endometrial |

## Indication intent breakdown

| Intent | Wave L count |
|---|---|
| treatment | 436 |
| prevention | 246 |
| surveillance | 40 |
| screening | 0 (gap; all prevention/screening currently filed under `prevention` or `surveillance`) |

## Wave L commit log (chronological)

1. `2ef6ffc69d` — reproductive prevention expansion (4 RFs + 8 indications)
2. `c0eea22cf8` — chronic-condition prevention expansion (T2DM + NAFLD/MASLD)
3. `fe0c901d4c` — lifestyle prevention expansion (smokeless + SSB + salt)
4. `252eca9dcb` — moderate-penetrance hereditary carriers (ATM, PALB2, CHEK2)
5. `10023385dd` — Wave K cherry-pick: 15 demo patients (examples batch 8)
6. `0adbb3e957` — Wave K cherry-pick: prevention KB audit suite (`tests/test_prevention_kb_audit.py`, 42 sub-tests)
7. `fa9f2bd7a1` — Wave K cherry-pick: 5 cascade-testing pilots
8. `59255bdc20` — Wave K cherry-pick: 12 chemoprevention/PrEP/vaccination drug entities
9. `dce7c02e26` — Wave K cherry-pick: 6 IARC Group 2A probable-carcinogen pilots
10. `7e2882a456` — fix: DIS-PANCREATIC → DIS-PDAC references
11. `aa0b6b472a` — pediatric/inherited high-penetrance (NF1, CDH1/HDGC, CMMRD) — fills Wave K pediatric agent silent failure
12. `b5e7d42c8e` — HR-pathway moderate-penetrance carriers (BARD1, BRIP1, RAD51C/D)
13. `7e338e1690` — iatrogenic prevention expansion (MTX-LPD, I-131)
14. `b062ea8641` — fix: PCOS routing duplicate + DES content-overlap documentation (advisor-flagged)

## Known issues + v0.4 follow-up queue

### 🟡 Content duplication (no routing bug; v0.4 consolidation)
- **DES in-utero exposure**: covered by both `rf_iatrogenic_des_exposure_prevention` (pre-existing) and `rf_reproductive_des_in_utero_exposure_prevention` (Wave L). Finding-key sets disjoint so single-patient JSONs don't double-fire, but content duplication should be consolidated (likely keeping iatrogenic since DES is a medication-induced exposure).

### 🟡 Pediatric coverage incomplete
- Wave K pediatric agent (Beckwith-Wiedemann, Costello, Rhabdoid) silently failed; 3 of 6 pediatric pilots (NF1, CDH1, CMMRD) authored by Wave L instead.
- Wave M pediatric agent re-launched for Beckwith-Wiedemann + Costello + Rhabdoid; status running.

### 🟡 Family-history-suspicion variants missing
- Wave L added 7 confirmed-carrier RFs (ATM/PALB2/CHEK2/BARD1/BRIP1/RAD51C-D/NF1) but only 5 of 7 have suspicion variants per pre-existing convention.
- Wave M suspicion-variant agent running; status running.

### 🟡 Pre-existing baseline test failures (not Wave L regressions)
- `tests/test_workup_catalog.py` reports 1 failure on master baseline — pre-existing.
- Full-suite `pytest tests/` reports 3500 errors + 8 failures — pre-existing (mainly from non-prevention test fixtures); confirmed by stash + run-on-stashed-baseline.
- Prevention test suite (73 tests): all green.

### 🟢 Schema gaps to address in v0.4
- `BiomarkerClinicalContext` enum doesn't include `screening`, `precursor_lesion`, `dysplasia_grading`, `hereditary_surveillance`, `diagnostic_workup` — 15 pre-existing biomarker schema errors result. Enum needs extension.
- `intent: screening` is defined in enum but unused in current YAML; should retro-label screening-style content (HPV primary, FIT, LDCT lung) from `intent: prevention` → `intent: screening` for clearer Indication routing.
- `environmental` risk category not in `PreventionRiskCategory` enum despite multiple `rf_environmental_*` filenames; current workaround is `risk_category: occupational` for environmental-exposure RFs.

## Outstanding gaps for Wave M / Wave N

- Beckwith-Wiedemann + Costello + Rhabdoid (Wave M in flight)
- Family-history-suspicion variants for 7 carriers (Wave M in flight)
- 18 example patient JSONs for Wave L RFs (Wave M in flight)
- Pediatric-anchor disease entities (DIS-HEPATOBLASTOMA, DIS-MEDULLOBLASTOMA, DIS-NEUROBLASTOMA, DIS-RHABDOMYOSARCOMA, DIS-ATRT, DIS-MRT)
- Additional moderate-penetrance: NBN, RAD50, MRE11A, TP53 family-history-suspicion variant
- Cronkhite-Canada, Juvenile Polyposis (SMAD4/BMPR1A), Familial Pancreatic Cancer
- More iatrogenic: ASCT secondary MDS/AML, BCG bladder leukemia, CAR-T late effects (emerging)
- More infectious: HCV→HCC standalone (separate from HCV→NHL), HBV reactivation risk pre-chemotherapy
- More chronic: severe obesity BMI≥40, Crohn's-specific (split from IBD), Sjögren's-specific MALT
- Engine: render-layer improvements for PreventionPlan output (current cardiac/breast/etc surveillance schedules cluttered)
- Tests: add e2e test covering each Wave L RF
- Spec: §20 v0.3 ratification (current ratified state is §20 v0.2-A from 2026-05-18)

## Audit-trail compliance

All Wave L entities:
- `draft: true`
- `reviewer_signoffs: 0`
- `ukrainian_review_status: pending_clinical_signoff`
- `notes: STUB pending two-Co-Lead signoff per CHARTER §6.1 dev-mode`
- Sources from existing entities only (no banned-list violations)
- Pre-commit hooks passed on every commit
- No `--no-verify`, no force-push, no master direct-commit

## Test coverage

- `tests/test_prevention_engine.py` (21 tests) — all pass
- `tests/test_prevention_render.py` (8 tests) — all pass
- `tests/test_prevention_kb_audit.py` (10 functions × parametrize = 42 sub-tests) — all pass

Total prevention coverage: 73 passing tests.
