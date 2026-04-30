# Curated examples expansion — chunk plan 2026-04-29-0313

**Driver:** per-disease coverage matrix (`scripts/disease_coverage_matrix.py`) shows
~95% of KB-indications have no curated `examples/patient_*.json` companion.
Solid tumors are the most stark gap — NSCLC has 28 indications and 0
curated cases; BREAST has 20 / 0; CRC has 18 / 1 (BRAF demo only).

**Goal:** add ~64 new curated `patient_*.json` cases across 12 disjoint
chunks runnable in parallel, append to gallery, rebuild `docs/cases/`.
No KB edits — every required Disease/Indication/Regimen/RedFlag/biomarker
already exists and validates.

**Out of scope:** clinical co-lead signoff (CHARTER §6.1, dev-mode exempt
per `project_charter_dev_mode_exemptions`); KB schema changes; new
indications; PROPOSAL §17 (sequential phases) — chunks must work within
current schema, using `extra="allow"` escape hatches only where solid-tumor
KB already does (e.g., `Disease.receptor_subtypes`, `Disease.disease_states`).

## Two-phase orchestration

Single contention point is `scripts/site_cases.py` (gallery registry).
Two parallel agents writing to it = merge conflict. Therefore:

- **Phase 1 (parallel):** 12 agents in worktree isolation, each producing
  ONLY `examples/patient_<disease>_<variant>.json` files. No edits to
  `site_cases.py`. No edits to `docs/`. No edits to KB.
- **Phase 2 (single agent, sequential):** integration pass collects all
  Phase-1 JSONs, appends `CaseEntry` rows to `scripts/site_cases.py`,
  runs `python -m scripts.build_site` to regenerate `docs/cases/<id>.html`
  and `docs/examples.json`, commits the bundle.

Phase 2 cannot start until all Phase-1 chunks have landed (or the orchestrator
declares partial-merge with explicit list of completed chunks).

## Branch + worktree convention

- Branch name: `chunk/curated-examples-<chunk-key>-2026-04-29-0313`
  (e.g., `chunk/curated-examples-nsclc-2026-04-29-0313`).
- Each chunk runs in its own worktree (per CLAUDE.md "Worktree isolation").
- Tag baseline at start: `git tag chunk-curated-examples-2026-04-29-0313-baseline`.
- File allowlist per chunk = strict pathspec list given below. Edits outside
  → STOP + report.
- No `--no-verify`, no `git add -A`, no force-push, no branch deletion.
- NOT pushed without explicit user instruction.

## Per-chunk validation gates

Every Phase-1 chunk must pass before reporting done:

1. KB validator clean: `C:/Python312/python.exe -m knowledge_base.validation.cli` →
   `ok=True`, 0 errors / 0 contract / 0 warnings.
2. Engine smoke: for each new JSON, run
   `C:/Python312/python.exe -m knowledge_base.engine.cli --patient examples/<file>.json`
   → exit 0, output non-empty, default track resolves, no `KeyError` /
   missing-ref errors.
3. Render smoke: `--render /tmp/<file>.html` works, output > 8 KB, contains
   FDA-disclosure footer + medical disclaimer.
4. Test-suite stays green for the chunk's domain test file (e.g.,
   `tests/test_solid_engine.py` if it exists; otherwise the broad
   `tests/test_reference_case_e2e.py` regression-suite as a sanity check).

Phase-2 integration agent additionally runs:

5. `python -m scripts.build_site` succeeds; `docs/cases/<id>.html` produced
   for every new case; `docs/examples.json` parses; gallery filter chips
   render the new entries.

---

## Phase 1 chunks (12 parallel, ~64 new cases)

For each chunk: `chunk-key` · target indications/algorithm paths · expected
JSON files · file allowlist.

### S1 · NSCLC biomarker variants (12 cases)

`chunk-key: nsclc-biomarker-variants`

Cover the molecular subtypes encoded in DIS-NSCLC. One curated case per
biomarker-driven branch:

- `patient_nsclc_egfr_l858r_1l_osimertinib.json` — EGFR L858R metastatic, 1L FLAURA-style
- `patient_nsclc_egfr_ex19del_1l_osimertinib.json` — EGFR Exon-19 deletion 1L
- `patient_nsclc_egfr_t790m_post_1g_tki.json` — T790M after 1st-gen TKI, 2L osimertinib
- `patient_nsclc_alk_1l_alectinib.json` — ALK rearranged, 1L alectinib (ALEX)
- `patient_nsclc_alk_2l_lorlatinib.json` — ALK post-alectinib, 2L lorlatinib
- `patient_nsclc_ros1_1l_entrectinib.json` — ROS1 fusion, 1L
- `patient_nsclc_kras_g12c_2l_sotorasib.json` — KRAS G12C, 2L (CodeBreaK 200)
- `patient_nsclc_braf_v600e_1l_dab_tram.json` — BRAF V600E, 1L
- `patient_nsclc_metex14_1l_capmatinib.json` — METex14 skipping, 1L
- `patient_nsclc_pdl1_high_pembro_mono.json` — PD-L1 ≥50%, 1L pembrolizumab mono (KEYNOTE-024)
- `patient_nsclc_pdl1_low_chemo_io.json` — PD-L1 1–49%, 1L pembro+chemo (KEYNOTE-189)
- `patient_nsclc_squamous_chemo_io.json` — squamous, 1L pembro+carbo+nab-pacli (KEYNOTE-407)

Allowlist:
```
examples/patient_nsclc_egfr_l858r_1l_osimertinib.json
examples/patient_nsclc_egfr_ex19del_1l_osimertinib.json
examples/patient_nsclc_egfr_t790m_post_1g_tki.json
examples/patient_nsclc_alk_1l_alectinib.json
examples/patient_nsclc_alk_2l_lorlatinib.json
examples/patient_nsclc_ros1_1l_entrectinib.json
examples/patient_nsclc_kras_g12c_2l_sotorasib.json
examples/patient_nsclc_braf_v600e_1l_dab_tram.json
examples/patient_nsclc_metex14_1l_capmatinib.json
examples/patient_nsclc_pdl1_high_pembro_mono.json
examples/patient_nsclc_pdl1_low_chemo_io.json
examples/patient_nsclc_squamous_chemo_io.json
```

### S2 · BREAST receptor-subtype + stage variants (8 cases)

`chunk-key: breast-subtypes`

DIS-BREAST is a single Disease with three `receptor_subtypes` × two
`stage_strata` — Algorithm decision_tree resolves subtype via biomarker
findings. One case per major branch:

- `patient_breast_hr_pos_her2_neg_met_1l_cdk46i.json` — HR+/HER2- met 1L AI+palbo (PALOMA-2)
- `patient_breast_hr_pos_post_cdk46i_pik3ca_alpelisib.json` — HR+/HER2- post-CDK4/6i, PIK3CA mut, alpelisib (SOLAR-1)
- `patient_breast_her2_pos_early_neoadj_kn522_path.json` — HER2+ early neoadj TCHP → KATHERINE T-DM1 if non-pCR
- `patient_breast_her2_pos_met_1l_thp.json` — HER2+ met 1L docetaxel+THP (CLEOPATRA)
- `patient_breast_her2_pos_met_2l_tdxd.json` — HER2+ met 2L T-DXd (DESTINY-Breast03)
- `patient_breast_tnbc_neoadj_kn522_pembro_chemo.json` — TNBC neoadj pembro+chemo (KEYNOTE-522)
- `patient_breast_brca_germline_met_olaparib.json` — BRCA1/2 germline met PARPi (OlympiAD)
- `patient_breast_tnbc_met_sacituzumab_2l.json` — TNBC met 2L sacituzumab govitecan (ASCENT)

Allowlist: 8 `examples/patient_breast_*.json` files above.

### S3 · CRC line-of-therapy + biomarker (6 cases)

`chunk-key: crc-lines`

CRC has 18 indications. Existing curated case (`patient_csd_1_demo_braf_mcrc.json`)
covers BEACON BRAF V600E. Add complementary paths:

- `patient_crc_stage_iii_adjuvant_folfox.json` — stage III adjuvant FOLFOX
- `patient_crc_metastatic_ras_wt_left_folfox_cetux.json` — mCRC RAS-WT left-sided 1L FOLFOX+cetux
- `patient_crc_metastatic_ras_mut_folfox_bev.json` — mCRC RAS-mutated 1L FOLFOX+bev
- `patient_crc_metastatic_msi_h_pembro_mono.json` — mCRC MSI-H 1L pembro mono (KEYNOTE-177)
- `patient_crc_metastatic_2l_folfiri_bev.json` — 2L FOLFIRI+bev after FOLFOX
- `patient_crc_metastatic_3l_regorafenib.json` — 3L+ regorafenib

Allowlist: 6 `examples/patient_crc_*.json` files above.

### S4 · MELANOMA BRAF / NRAS / IO (5 cases)

`chunk-key: melanoma-braf-io`

- `patient_melanoma_braf_v600_dab_tram.json` — BRAF V600 1L dabrafenib+trametinib (COMBI-d/v)
- `patient_melanoma_braf_v600_nivo_ipi.json` — BRAF V600 1L IO doublet nivo+ipi (CheckMate-067)
- `patient_melanoma_braf_wt_pembro_mono.json` — BRAF-WT 1L pembrolizumab mono (KEYNOTE-006)
- `patient_melanoma_nivo_relatlimab.json` — 1L nivolumab + relatlimab (RELATIVITY-047)
- `patient_melanoma_adjuvant_pembro_stage_iii.json` — stage III resected adjuvant pembro (KEYNOTE-054)

Allowlist: 5 `examples/patient_melanoma_*.json` files above.

### S5 · PROSTATE disease-state cascade (5 cases)

`chunk-key: prostate-states`

DIS-PROSTATE is `line_of_therapy_sequential` with mHSPC/mCRPC/nmCRPC states:

- `patient_prostate_mhspc_adt_arpi_doublet.json` — mHSPC ADT+enzalutamide (ARCHES) or apalutamide (TITAN)
- `patient_prostate_mhspc_triplet_peace1.json` — mHSPC ADT+abi+docetaxel triplet (PEACE-1)
- `patient_prostate_nmcrpc_apalutamide.json` — nmCRPC apalutamide (SPARTAN)
- `patient_prostate_mcrpc_brca_olaparib_profound.json` — mCRPC BRCA-mut PARPi (PROfound)
- `patient_prostate_mcrpc_psma_pet_lupsma_vision.json` — mCRPC PSMA-PET+ post-novel-hormonal+taxane Lu-177-PSMA-617 (VISION)

Allowlist: 5 `examples/patient_prostate_*.json` files above.

### S6 · GU + skin + gyn tail (6 cases)

`chunk-key: gu-skin-gyn-tail`

- `patient_rcc_imdc_int_nivo_ipi.json` — RCC IMDC int/poor 1L nivo+ipi (CheckMate-214)
- `patient_rcc_imdc_fav_axi_pembro.json` — RCC IMDC favorable 1L axi+pembro (KEYNOTE-426)
- `patient_urothelial_muc_ev_pembro.json` — mUC 1L EV+pembro (EV-302)
- `patient_endometrial_dmmr_pembro_kn775.json` — advanced endometrial dMMR pembro+chemo (NRG-GY018)
- `patient_endometrial_p53_abn_dosta_kn775.json` — advanced endometrial p53-abnormal carbo+pacli+dostarlimab (RUBY)
- `patient_ovarian_hrd_neg_carbo_pacli_no_parpi.json` — ovarian HRD-negative standard induction, no PARPi maintenance (contrast with existing `patient_ovarian_advanced_hrd.json`)

Allowlist: 6 `examples/patient_(rcc|urothelial|endometrial|ovarian)_*.json` files above.

### S7 · GI remaining (HCC / gastric / esophageal / PDAC) (6 cases)

`chunk-key: gi-remaining`

- `patient_hcc_atezo_bev_imbrave150.json` — HCC Child-Pugh-A 1L atezo+bev (IMbrave150)
- `patient_hcc_durva_treme_stride.json` — HCC 1L durva+treme (HIMALAYA STRIDE)
- `patient_gastric_her2_pos_toga.json` — gastric metastatic HER2+ 1L trastuzumab+chemo (TOGA)
- `patient_gastric_pdl1_cps_high_chemo_nivo.json` — gastric metastatic CPS≥5 1L chemo+nivo (CheckMate-649)
- `patient_esophageal_adeno_neoadj_cross_then_nivo.json` — esophageal adeno neoadj CROSS → adjuvant nivo (CheckMate-577)
- `patient_pdac_metastatic_folfirinox_fit.json` — PDAC metastatic fit FOLFIRINOX (PRODIGE-4)

Allowlist: 6 `examples/patient_(hcc|gastric|esophageal|pdac)_*.json` files above.

### S8 · Thoracic + HNSCC misc (4 cases)

`chunk-key: thoracic-hnscc-misc`

- `patient_sclc_ls_chemo_rt.json` — SCLC limited-stage chemo + concurrent RT
- `patient_sclc_es_atezo_chemo_impower133.json` — SCLC extensive-stage atezo+carbo+etoposide (IMpower133)
- `patient_hnscc_cps_high_pembro_mono.json` — HNSCC R/M CPS≥1 1L pembro mono (KEYNOTE-048)
- `patient_hnscc_extreme_cetux_platin_5fu.json` — HNSCC R/M EXTREME (cetux+platin+5FU)

Allowlist: 4 `examples/patient_(sclc|hnscc)_*.json` files above.

### H1 · AML subtype expansion (4 cases)

`chunk-key: aml-subtypes`

DIS-AML has 11 indications; only 3 curated. Add:

- `patient_aml_flt3_itd_midostaurin_7_3.json` — FLT3-ITD+ fit, 7+3 + midostaurin (RATIFY)
- `patient_aml_cbf_inv16_7_3_go.json` — CBF inv(16) / t(8;21) fit, 7+3 + gemtuzumab (ALFA-0701)
- `patient_aml_secondary_cpx351.json` — secondary AML / t-AML, CPX-351 (Vyxeos)
- `patient_aml_rr_gilteritinib.json` — R/R FLT3-mut, gilteritinib (ADMIRAL) — distinct from existing `patient_aml_flt3_relapse.json` if that's quizartinib

Allowlist: 4 `examples/patient_aml_*.json` files above (verify no name clash with existing 3).

### H2 · DLBCL line-of-therapy expansion (3 cases)

`chunk-key: dlbcl-lines`

DLBCL has 9 indications; 4 curated. Add:

- `patient_dlbcl_2l_pola_r_b.json` — 2L pola-R-B transplant-ineligible (POLARIX 2L)
- `patient_dlbcl_3l_axi_cel.json` — 3L+ axi-cel post 2L chemo failure (ZUMA-1)
- `patient_dlbcl_primary_refractory_loncast_post_pola.json` — primary-refractory DLBCL post-pola, loncastuximab (LOTIS-2)

Note: existing `patient_dlbcl_chemorefractory_for_cart.json` covers the
chemorefractory-for-CAR-T pre-decision archetype — these new cases pick up
post-decision pathways.

Allowlist: 3 `examples/patient_dlbcl_*.json` files above (verify no name clash).

### H3 · Indolent B-cell line expansion (4 cases)

`chunk-key: indolent-b-lines`

- `patient_cll_zanu_1l_sequoia.json` — CLL 1L zanubrutinib (SEQUOIA)
- `patient_cll_venr_2l_murano.json` — CLL 2L VenR fixed-duration (MURANO)
- `patient_mcl_pirtobrutinib_3l_post_btki.json` — MCL 3L+ pirtobrutinib post-BTKi (BRUIN)
- `patient_fl_r2_lenalidomide_rituximab_2l.json` — FL 2L R² lenalidomide+rituximab (AUGMENT)

Allowlist: 4 `examples/patient_(cll|mcl|fl)_*.json` files above.

### D1 · Diagnostic pre-biopsy solid (3 cases)

`chunk-key: diagnostic-solid-prebiopsy`

Currently only lymphoma diagnostic cases exist. KB has solid-tumor
diagnostic workups (`workup_suspected_breast`, `_nsclc`, `_prostate`, etc.).
Add minimal pre-biopsy diagnostic profiles:

- `patient_diagnostic_breast_lump_prebiopsy.json` — palpable lump, BI-RADS 4–5, no histology yet
- `patient_diagnostic_lung_mass_smoker_prebiopsy.json` — incidental lung mass on CT, smoker hx
- `patient_diagnostic_prostate_psa_elevated_prebiopsy.json` — elevated PSA, mp-MRI PI-RADS 4

Each must trigger Diagnostic Brief mode (CHARTER §15.2 C7), not Treatment Plan.

Allowlist: 3 `examples/patient_diagnostic_*.json` files above.

---

## Phase 2 — integration

Single agent, sequential. Branch:
`chunk/curated-examples-integration-2026-04-29-0313`.

Tasks:

1. Cherry-pick / merge each Phase-1 chunk branch (or accept they're already
   merged into a shared integration branch by orchestrator).
2. Edit `scripts/site_cases.py`: append one `CaseEntry` per new JSON,
   preserving existing ordering by category, with descriptive UA labels +
   2-sentence UA summary referencing the trial / regimen / decision rule.
3. Run `C:/Python312/python.exe -m scripts.build_site` → expect `docs/cases/<id>.html`
   for every new case-id, `docs/examples.json` updated.
4. Verify gallery: open `docs/gallery.html`, confirm filter chips render
   new entries under correct categories (`solid` for S1–S8, `myeloid` for H1,
   `b_aggressive` for H2, `b_indolent` for H3, `diagnostic` for D1).
5. Single commit: explicit pathspec listing every modified/added file.
6. NOT pushed. Report PR-ready commit SHA + brief diff stats.

Allowlist for Phase-2 agent:
```
scripts/site_cases.py
docs/cases/**          # build_site overwrites these
docs/examples.json     # build_site overwrites this
docs/openonco-engine-*.zip   # build_site regenerates these
```

## Stop conditions (any chunk)

- HEAD on a different branch than expected.
- Working tree unexpectedly modified outside the chunk allowlist.
- Engine smoke fails for any new JSON (do not paper-over with try/except —
  surface the engine error; that's a real KB-mismatch signal).
- KB validator regresses (was clean, now isn't) — your JSON shouldn't be
  able to break the validator unless you accidentally edited a YAML.
- Disease/Indication/Regimen/Biomarker referenced in a JSON doesn't exist
  in KB (you cannot mint new IDs in this chunk; if a target indication is
  missing, drop the case from the chunk and report).
- Two agents writing the same path (coordination bug — surfaces as worktree
  conflict at integration).

## Open questions for orchestrator

1. **Existing-case name-clash check**: H1/H2/H3 chunks need to confirm new
   filenames don't already exist (e.g., `patient_aml_flt3_relapse.json` is
   already curated — H1's `patient_aml_rr_gilteritinib.json` may overlap
   in clinical scenario; chunk-agent must `git status` + `ls examples/`
   first).
2. **CLL fit-vs-unfit existing coverage**: H3's CLL cases may overlap with
   `patient_cll_low_risk.json` / `patient_cll_high_risk.json` /
   `patient_cll_post_btki_progression.json` — chunk-agent reviews and
   either refines names or drops duplicates.
3. **Diagnostic-mode workup IDs**: D1 chunk-agent must verify which
   `WORKUP-*` IDs the engine resolves for solid-tumor pre-biopsy mode
   before authoring profiles (read `knowledge_base/engine/diagnostic.py`
   resolution logic).
4. **Trial-source attribution**: many cases reference major trials
   (PEACE-1, KEYNOTE-024, EV-302). If the KB doesn't have a Source entity
   for that trial, the case still works (engine doesn't require trial-level
   source per case), but the rendered Plan won't cite it. Acceptable for
   v0.1 — clinical sign-off pass will close gaps later.

## Estimate

- ~64 new curated `patient_*.json` files across 12 chunks.
- Solid: 52 cases (S1–S8). Heme: 11 cases (H1–H3). Diagnostic: 3 cases (D1).
- Phase 1 wallclock (12 parallel agents): ~30–60 min per chunk in worktree;
  largest is S1/NSCLC at 12 cases.
- Phase 2: 30–60 min for one agent doing site_cases.py append + build_site
  + gallery verification.
- Integration risk: low (all chunks file-disjoint by design; only Phase-2
  edits the shared `site_cases.py`).
