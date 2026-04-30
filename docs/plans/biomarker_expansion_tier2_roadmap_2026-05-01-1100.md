# Tier-2 expansion roadmap (W7–W13) — 2026-05-01-1100

**Status:** active planning track. Sequel to `docs/plans/biomarker_expansion_roadmap_2026-04-30-1500.md` (Tier-1 W1–W6, landed via PR #166 commit `b5810f4b` and W5b/W5c via PR #171).
**Driver:** Tier-1 closed the immediate-impact biomarker gaps. Tier-2 covers the second wave — emerging-targeted-therapy biomarkers, bispecific/CAR-T expansion, drug-class line additions, and the long tail of Q-axis quality work (CIViC backfill wave-2, source recency wave-2). Drug UA-NSZU axis is **complete** (220/220) and SKIPPED here.
**Excluded scope:** LymphGen DLBCL classifier (`docs/plans/lymphgen_dlbcl_proposal_2026-04-30-1500.md` still deferred — trigger conditions unchanged); Tier-3 niche entities (W13 — enumerated but post-v1.0); engine refactors (none required).
**Related docs:** `docs/plans/kb_data_quality_plan_2026-04-29.md` (Q1–Q5 quality gates each chunk must satisfy), `docs/plans/curated_examples_expansion_2026-04-29-0313.md` (chunk-fleet pattern reference), `docs/kb-coverage-matrix.md` (matrix the chunks move).

## Why this exists

Tier-1 (12 biomarkers) routed FDA-approved targeted therapies that the engine could not previously reach. Tier-2 (28 biomarkers + 21 drugs + ~50 regimens + ~50 indications + ~25 RFs) is **second-wave coverage**: drugs approved in 2023–2025 that the v0.1 KB does not yet wire (heme bispecifics, CAR-T expansion across diseases, breast/NSCLC ADC second-wave, gyn ADC, gastric/CRC/cholangio targeted-therapy expansion). It also closes two Q-axes that did not finish in the first 100-chunk batch:

- **Q1 BMA-CIViC:** 295/399 BMAs have an `evidence_sources[SRC-CIVIC]` block or `no_civic_match_reason`. **104 outstanding** — wave-2 targets these.
- **Q2 source recency:** 269/271 sources are stale by `current_as_of` (older than 2026-04-01) or are missing the field entirely. The orchestrator's "131 stale" prioritization is honored: this roadmap selects the 131 oldest (missing-field first, then ascending date) for wave-2.
- **Q3 drug UA-NSZU access:** **complete (220/220)** — no Tier-2 chunks needed.

Tier-2 turns these gaps into concrete chunks with allowlists, validation gates, and explicit stop conditions, mirroring the Tier-1 pattern that landed cleanly.

## Workstream summary

| ID | Workstream | Cadence | KB-edits? | Chunks |
|---|---|---|---|---|
| W7 | Tier-2 biomarkers (28 entities) | this month | yes | 7 |
| W8 | Tier-2 drugs (21 not-yet-in-KB entities) | this month | yes | 5 |
| W9 | Tier-2 regimens (~50 across W8 drugs × line × disease) | this month | yes | 8 |
| W10 | Tier-2 indications (~50, wiring W7 + W8 + W9) | this month | yes | 7 |
| W11 | Tier-2 RFs (~25, gating W10 indications) | this month | yes | 4 |
| W12a | BMA-CIViC backfill wave-2 (104 BMAs / 5 per chunk) | parallel | yes (sidecar) | 21 |
| W12b | Source recency refresh wave-2 (131 sources / 5 per chunk) | parallel | yes (sidecar) | 27 |
| W13 | Tier-3 niche entities (deferred, stubs only) | post-v1.0 | yes | 3 |
| — | Dispatch tracker | — | no | 1 |

**Total dispatchable issues:** ~83 (7 W7 + 5 W8 + 8 W9 + 7 W10 + 4 W11 + 21 W12a + 27 W12b + 3 W13 + 1 tracker = 83).

## W7 — Tier-2 biomarkers (28 entities, 7 chunks)

**Goal:** add 28 second-wave biomarkers grouped by therapeutic area. These are research-grade or recently-FDA-approved markers that the v0.1 KB can route to once Tier-2 drugs + indications land in W8/W10. Each chunk authors `bio_*.yaml` files with provenance + UA fields per Q1/Q3 quality gates.

### W7a — Heme expression markers (6 bio)

Chunk key: `tier2-bio-heme-2026-05-01`.

- `bio_cd79b_mutation` (LymphGen MCD-relevant, distinct from existing `bio_cd79b_ihc`)
- `bio_notch2_mutation` (LymphGen BN2-relevant)
- `bio_cd22_expression` (quantitative — for inotuzumab eligibility)
- `bio_cd33_expression` (quantitative — for gemtuzumab/CD33 ADC eligibility)
- `bio_bcma_expression` (for teclistamab/elranatamab/CAR-T eligibility)
- `bio_cd38_expression` (quantitative — for daratumumab/isatuximab line stratification)

KB delta: 6 bio. No regimen/indication wiring in this chunk (W10 wires).

### W7b — Hereditary panel split (5 bio)

Chunk key: `tier2-bio-hereditary-2026-05-01`.

- `bio_brca_somatic` (distinct from existing `bio_brca_germline`/`bio_brca1_brca2_germline` — affects PARPi tier per disease)
- `bio_palb2_germline`
- `bio_atm_chek2_cdk12_germline` (composite hereditary panel; or 3 separate entries — verify schema preference at chunk time)
- `bio_cdh1_germline` (lobular breast / hereditary diffuse gastric)
- `bio_lynch_panel_split` (MLH1 / MSH2 / MSH6 / PMS2 — author either as one composite biomarker entity with 4 alleles or 4 separate entries; chunk picks the cleaner option after reading existing Lynch coverage in `bio_msi_*` and `bio_dmmr_*`)

KB delta: 5 bio entities (or up to 8 if Lynch authored allele-by-allele).

### W7c — Prostate (3 bio)

Chunk key: `tier2-bio-prostate-2026-05-01`.

- `bio_ar_amplification` (distinct from existing AR-V7 splice variant; mCRPC ARSI-resistance complement)
- `bio_tmprss2_erg_fusion` (prostate prognostic, not Tx-modifying)
- `bio_dmmr_prostate` (small-population pembro eligibility — verify if existing `bio_dmmr_solid` already covers prostate; if so, this is an indication-wiring chunk only)

KB delta: 3 bio (or 2 + indication delta).

### W7d — Emerging targeted (6 bio)

Chunk key: `tier2-bio-emerging-targeted-2026-05-01`.

- `bio_nrg1_fusion` (zenocutuzumab pan-tumor, FDA Dec 2024)
- `bio_braf_class_ii_iii` (non-V600, distinct drug strategy)
- `bio_her2_ultralow` (DESTINY-Breast06; distinct from existing `bio_her2_low`)
- `bio_esr1_y537s_d538g` (extension to existing `bio_esr1`; hot-spot allele granularity for elacestrant)
- `bio_akt1_e17k` (extension to existing `bio_akt1`; capivasertib eligibility hot-spot)
- `bio_cdkn2a_loss` (extension to existing `bio_cdkn2a`; co-deletion vs LOH variants)

KB delta: 6 bio (or extensions to existing — chunk decides based on schema flexibility).

### W7e — Melanoma + rare (4 bio)

Chunk key: `tier2-bio-melanoma-rare-2026-05-01`.

- `bio_nf1_mutation` (melanoma sub-classification)
- `bio_bap1_mutation` (uveal melanoma + mesothelioma)
- `bio_ctdna_mrd` (generic ctDNA-MRD; lineage-agnostic)
- `bio_hrd_assay_distinction` (Myriad MyChoice CDx vs F1CDx — extend existing `bio_hrd_status` or new entity)

KB delta: 4 bio.

### W7f — PD-L1 IHC clones (4 bio)

Chunk key: `tier2-bio-pdl1-clones-2026-05-01`.

Currently `bio_pdl1_cps`, `bio_pdl1_tps`, `bio_pdl1_expression` exist. Add clone-specific entries because clinical literature ties specific drugs to specific clones (KEYNOTE used 22C3, IMpower used SP142, IMmotion used SP142, CheckMate used 28-8).

- `bio_pdl1_22c3_clone` (Dako 22C3 — pembrolizumab indications)
- `bio_pdl1_sp142_clone` (Ventana SP142 — atezolizumab TNBC, urothelial)
- `bio_pdl1_sp263_clone` (Ventana SP263 — durvalumab)
- `bio_pdl1_28_8_clone` (Dako 28-8 — nivolumab)

KB delta: 4 bio. Wiring lives in W10.

### W7 sequencing

All seven chunks parallel. Worktree-isolated. Branch off `origin/master`. Integration agent **not** required: W10 indication chunks reference these IDs and will surface any naming-clash via validator failure.

### W7 validation gates (each chunk)

1. KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK — all entities valid". Entity counts ≥ baseline.
2. pytest fixture: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed" (no regression).
3. Per-chunk allowlist strictly enforced: `git diff --name-only origin/master | grep -v "^knowledge_base/hosted/content/biomarkers/"` should be empty.
4. Each new biomarker has `actionability_lookup` if a single-variant target gene/variant; otherwise `oncokb_skip_reason`. Mutually exclusive — model_validator enforces.
5. Each new biomarker has UA fields (`names.ukrainian`, `ukrainian_review_status: pending_clinical_signoff`, `ukrainian_drafted_by: claude_extraction`).
6. Trial Source IDs cited in commit body if any new ones referenced; flag missing trial Sources as "to be authored" — do not invent.

## W8 — Tier-2 drugs (21 not-yet-in-KB entities, 5 chunks)

**Existence-check pre-flight (verified 2026-05-01):** of the 35 drugs in the original Tier-2 brief, 13 already exist in `knowledge_base/hosted/content/drugs/`:

> avapritinib, blinatumomab, capivasertib, fruquintinib, inotuzumab_ozogamicin, mirvetuximab_soravtansine, mosunetuzumab, niraparib, quizartinib, repotrectinib, talazoparib, teclistamab, tisagenlecleucel.

Tier-2 W8 therefore covers the **21 remaining**.

### W8a — Heme bispecifics + CAR-T (6 drugs)

Chunk key: `tier2-drug-heme-bispecific-cart-2026-05-01`.

- `drug_elranatamab` (BCMA bispecific — MagnetisMM-3, FDA Aug 2023)
- `drug_talquetamab` (GPRC5D bispecific — MonumenTAL-1, FDA Aug 2023)
- `drug_idecabtagene_vicleucel` (ide-cel BCMA CAR-T — KarMMa, FDA Mar 2021)
- `drug_ciltacabtagene_autoleucel` (cilta-cel BCMA CAR-T — CARTITUDE-1, FDA Feb 2022)
- `drug_epcoritamab` (CD3xCD20 bispecific — EPCORE NHL-1, FDA May 2023)
- `drug_glofitamab` (CD3xCD20 bispecific — NP30179, FDA Jun 2023)

### W8b — Heme CAR-T continued (1 drug)

Chunk key: `tier2-drug-heme-liso-cel-2026-05-01`.

- `drug_lisocabtagene_maraleucel` (liso-cel CD19 CAR-T — TRANSCEND, FDA Feb 2021; CLL TRANSCEND-CLL Mar 2024)

(Authored as separate small chunk because it's CD19-target across DLBCL+CLL+MCL; W11 RFs differ per disease.)

### W8c — Breast + NSCLC emerging (5 drugs)

Chunk key: `tier2-drug-breast-nsclc-emerging-2026-05-01`.

- `drug_inavolisib` (PIK3CA-mut HR+ breast — INAVO120, FDA Oct 2024)
- `drug_datopotamab_deruxtecan` (TROP2 ADC — TROPION-Breast01 / TROPION-Lung01)
- `drug_zenocutuzumab` (NRG1-fusion bispecific — eNRGy, FDA Dec 2024)
- `drug_patritumab_deruxtecan` (HER3 ADC — HERTHENA-Lung01)
- `drug_ensartinib` (ALK TKI — eXalt3, FDA Dec 2024)

### W8d — GI + GYN emerging (5 drugs)

Chunk key: `tier2-drug-gi-gyn-emerging-2026-05-01`.

- `drug_futibatinib` (FGFR2 TKI for cholangio — FOENIX-CCA2, FDA Sep 2022)
- `drug_infigratinib` (FGFR2 TKI for cholangio — CBGJ398X2204, FDA May 2021; commercial status volatile — verify still marketed at chunk time)
- `drug_magrolimab` (CD47 mAb — verify FDA approval status at chunk time; AML/MDS development was discontinued 2024 — chunk may drop and document)
- `drug_tisotumab_vedotin` (TF ADC — innovaTV 204, FDA Sep 2021 cervical)
- `drug_olutasidenib` (IDH1 R132 inhibitor — Study 2102-HEM-101, FDA Dec 2022 R/R AML)

### W8e — Misc niche (4 drugs)

Chunk key: `tier2-drug-misc-niche-2026-05-01`.

- `drug_lurbinectedin` (RNAPII inhibitor — ATLANTIS, FDA Jun 2020 SCLC R/R)
- `drug_ripretinib` (KIT/PDGFRA TKI — INVICTUS, FDA May 2020 GIST 4L+)
- `drug_retifanlimab` (PD-1 mAb — POD1UM-202 anal SCC, FDA Mar 2023)
- `drug_erdafitinib` (FGFR TKI — BLC2001/THOR, FDA Apr 2019; THOR Jan 2024 reaffirmation urothelial 2L)

### W8 validation gates

Same as W7 (validator + pytest + allowlist + UA fields). Plus drug-specific:

- Each drug has `mechanism_of_action` UA-language field, `class`, `route`, `monitoring`, `nszu_status` (Q3 axis — defer to "unresolved" if not yet in NSZU registry rather than guessing).
- Each drug cites at least one regulatory source (FDA label or EMA SmPC) and one pivotal-trial source.

## W9 — Tier-2 regimens (~50, 8 chunks)

**Goal:** every drug from W8 becomes 2–3 regimen YAMLs (per disease × line of therapy combination). Estimate 4–6 regimens per chunk.

### W9 chunks

| Chunk key | Drug class | Estimated regimens |
|---|---|---|
| `tier2-reg-mm-bispecific-2026-05-01` | teclistamab/elranatamab/talquetamab @ MM-RR (3L+, 4L+) | 6 |
| `tier2-reg-mm-cart-2026-05-01` | ide-cel/cilta-cel @ MM-RR (3L+, 4L+) | 5 |
| `tier2-reg-dlbcl-bispecific-cart-2026-05-01` | epcoritamab/glofitamab/liso-cel @ DLBCL (2L, 3L) | 6 |
| `tier2-reg-breast-emerging-2026-05-01` | capivasertib/inavolisib/dato-DXd @ breast HR+ post-CDK4/6i; HER2+ post-T-DXd | 6 |
| `tier2-reg-nsclc-emerging-2026-05-01` | dato-DXd-Lung/patritumab-DXd/repotrectinib/ensartinib | 6 |
| `tier2-reg-gi-emerging-2026-05-01` | futibatinib/infigratinib (FGFR2 cholangio); fruquintinib (CRC-3L); erdafitinib (urothelial-2L) | 5 |
| `tier2-reg-gyn-emerging-2026-05-01` | tisotumab-vedotin (cervical-2L); mirvetuximab (FRα ovarian-2L); retifanlimab (anal-1L) | 5 |
| `tier2-reg-niche-2026-05-01` | lurbinectedin (SCLC-RR); ripretinib (GIST-4L); olutasidenib (AML-RR-IDH1); blinatumomab/inotuzumab (B-ALL adult) | 6 |

KB delta per chunk: 4–6 `regimen_*.yaml` files. Each cites a pivotal-trial source.

### W9 validation gates

Same five quality gates plus:

- Each regimen references existing drug IDs (W8 chunks must merge first or be on integration branch; orchestrator sequences W9 to start *after* W8 merges).
- Each regimen has dosing (UA-language `description`), supportive-care notes (anti-emesis, GCSF), and CTCAE-toxicity profile.

## W10 — Tier-2 indications (~50, 7 chunks)

**Goal:** wire W7 biomarkers + W8 drugs + W9 regimens into the engine via `indication_*.yaml` files. Each indication = `(disease, line_of_therapy, biomarker_constraint, regimen_id)`.

### W10 chunks

| Chunk key | Disease area | Estimated indications |
|---|---|---|
| `tier2-ind-mm-2026-05-01` | MM 3L+/4L+ bispecifics + CAR-T | 6 |
| `tier2-ind-dlbcl-mcl-cll-2026-05-01` | DLBCL 2L/3L+ bispecifics + CAR-T; MCL/CLL CAR-T | 8 |
| `tier2-ind-breast-2026-05-01` | breast HR+ post-CDK4/6i (capivasertib/inavolisib); HER2+ post-T-DXd; TNBC/HR+ dato-DXd | 8 |
| `tier2-ind-nsclc-2026-05-01` | NSCLC NRG1/HER3/TROP2/ALK-2L/ROS1/NTRK | 8 |
| `tier2-ind-gi-2026-05-01` | cholangio FGFR2 (futibatinib/infigratinib); urothelial FGFR (erdafitinib); CRC-3L (fruquintinib) | 6 |
| `tier2-ind-gyn-2026-05-01` | cervical 2L (tisotumab); ovarian 2L FRα (mirvetuximab); anal 1L (retifanlimab) | 5 |
| `tier2-ind-aml-bal-misc-2026-05-01` | AML-RR-IDH1 (olutasidenib); B-ALL adult (blino/InO); SCLC-RR (lurbinectedin); GIST-4L (ripretinib) | 8 |

### W10 validation gates

Same plus:

- Each indication's `biomarker_constraints` reference existing biomarker IDs.
- Each indication's `regimen_ids` reference existing regimen IDs.
- Each indication ships with at least 2 source citations (Q4 citation density).
- Algorithm-file edits limited to additive steps; document if existing-step modification needed.

## W11 — Tier-2 RFs (~25, 4 chunks)

**Goal:** for each new biomarker that gates an indication, author the corresponding RF. Group by therapeutic area.

### W11 chunks

| Chunk key | Therapeutic area | Estimated RFs |
|---|---|---|
| `tier2-rf-heme-2026-05-01` | BCMA-pos / CD22-pos / CD33-pos / CD38-quant / CD79B-mut / NOTCH2-mut RFs | 7 |
| `tier2-rf-breast-nsclc-2026-05-01` | HER2-ultralow, ESR1-Y537S/D538G, AKT1-E17K, NRG1, HER3-high, PIK3CA-coalt | 7 |
| `tier2-rf-hereditary-prostate-2026-05-01` | BRCA-somatic, PALB2, ATM/CHEK2/CDK12, CDH1, AR-amp, TMPRSS2-ERG | 6 |
| `tier2-rf-misc-2026-05-01` | NF1, BAP1, ctDNA-MRD, HRD-assay-distinction, PD-L1 clone-specific eligibility | 5 |

### W11 validation gates

Same as W7 plus:

- Each RF references existing biomarker IDs (or W7 IDs landed earlier in the wave).
- RF `evaluation` block uses structured `findings` keys, not free-text `condition:` strings (drift signal #4 from W5 already documented this; do not reintroduce).

## W12 — Q-axis second waves

### W12a — BMA-CIViC backfill wave-2 (104 BMAs / 5 per chunk = 21 chunks)

**Goal:** advance Q1 BMA evidence integrity from 295/399 (74%) to 399/399 (100%). Each chunk owns a manifest of 5 BMAs and either adds an `evidence_sources[SRC-CIVIC]` entry (with CIViC evidence ID + PMID) or records a structured `no_civic_match_reason`.

**Chunking pattern:** identical to closed `bma-civic-backfill-2026-04-29-007` (issue #49). Sidecar-only output under `contributions/<chunk-id>/`. Hosted YAML never edited directly in chunk.

**Manifest distribution:** 104 BMAs distributed across 21 chunks via deterministic round-robin (5 per chunk, last chunk gets 4). Manifests are listed in each issue body.

**Chunk keys:** `bma-civic-backfill-wave2-001` … `bma-civic-backfill-wave2-021`.

### W12b — Source recency refresh wave-2 (131 sources / 5 per chunk = 27 chunks)

**Goal:** advance Q2 source recency. The brief specifies "131 sources stale by `last_verified` older than 2026-04-01"; this roadmap reproduced that count via a different proxy (most sources had identical `last_verified` post the Q2 wave-1 batch; ordering was done by `current_as_of` ascending, missing-field first). Chunk picks 5 sources, verifies the URL, bumps `current_as_of` to the chunk's run date, and adds a sidecar `source_recency_audit.yaml`.

**Chunk keys:** `source-recency-refresh-wave2-001` … `source-recency-refresh-wave2-027`.

### W12 validation gates

- `py -3.12 -m scripts.tasktorrent.validate_contributions <chunk-id>` passes.
- `git diff --name-only master..HEAD` shows no paths outside `contributions/<chunk-id>/`.
- No disallowed source IDs (`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`) appear.

## W13 — Tier-3 niche (deferred, 3 stub issues)

Specialist-noted gaps that don't have immediate FDA-approved-drug routing or require multi-entity stratification. Authored here as stubs with deferral rationale.

| Chunk key | Scope | Trigger to revisit |
|---|---|---|
| `tier3-bio-sarcoma-fusions-deferred` | EWSR1, SS18, DDIT3, MDM2 amp; sarcoma fusions | rare-disease coverage initiative or specialist request |
| `tier3-bio-pediatric-cns-deferred` | H3K27M, BRAF-fusion KIAA1549, DICER1 thyroid | pediatric oncology track activation |
| `tier3-bio-hereditary-panel-deferred` | Lynch genes individually, TP53 germline, APC, MUTYH (if not absorbed by W7b Lynch decision) | hereditary cancer counseling integration |

Each W13 issue is a short stub: trigger condition + contact-on-revisit + estimated scope.

## Cross-cutting concerns

### Tier-2 chunk validation gates (uniform per chunk)

1. KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK — all entities valid".
2. pytest fixture: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed" (no regression).
3. Per-chunk allowlist strictly enforced.
4. Sources cited (no invented IDs); flag missing trial Sources in commit body — do not invent.
5. Self-push authorized per CLAUDE.md commit `3a60901b`.

### Quality gates (per `kb_data_quality_plan_2026-04-29.md` Q1–Q5)

- **Q1 BMA evidence integrity:** W7 biomarkers ship with `actionability_lookup` (single-variant) XOR `oncokb_skip_reason` (composite/IHC/CN). W12a closes the BMA-CIViC backfill axis.
- **Q2 Source metadata:** W8/W9/W10 cite existing `SRC-*` IDs only. W12b closes the recency axis.
- **Q3 UA applicability:** every new biomarker/drug carries `names.ukrainian`, `ukrainian_review_status: pending_clinical_signoff`, `ukrainian_drafted_by: claude_extraction`. NSZU status declared explicitly (or `unresolved`).
- **Q4 Citation density:** each indication ≥ 2 source citations.
- **Q5 Regression prevention:** existing 62-case curated fixture is the gate. Tier-2 must not regress it without documented routing-change rationale.

### Multi-session reality

Master moves daily. Tier-2 chunks branch off `origin/master` at the moment they start, not from a frozen baseline. Where W9/W10 depend on W8 drug IDs, the orchestrator sequences (W7+W8+W12 parallel; W9 after W8 merges; W10 after W7+W8+W9; W11 last).

### Self-push authorization

Per CLAUDE.md commit `3a60901b`: chunks self-push when all gates pass. Branch names follow `chunk/<chunk-key>-<NNN>` per memory `feedback_chunk_naming`.

### Stop conditions (any chunk)

- HEAD on a different branch than expected.
- Working tree unexpectedly modified outside the chunk allowlist.
- KB validator regresses (was clean, now isn't).
- pytest 62-case fixture regresses without routing-rationale documentation.
- Trial / source ID missing from KB and required by indication — drop case, document, do not invent IDs.
- Two chunks editing the same file (coordination bug — surfaces as worktree merge conflict).
- Existing YAML modification beyond additive sections (escalate to user).

## Sequencing summary

```
Wave A (parallel, ~Day 1-2):
  W7a heme bio
  W7b hereditary bio
  W7c prostate bio
  W7d emerging targeted bio
  W7e melanoma+rare bio
  W7f PD-L1 clones bio
  W8a heme bispecific+CAR-T drugs
  W8b liso-cel drug
  W8c breast+NSCLC emerging drugs
  W8d GI+GYN emerging drugs
  W8e niche drugs
  W12a × 21 BMA-CIViC backfill (sidecar — fully parallel)
  W12b × 27 source-recency (sidecar — fully parallel)

Wave B (after W8 merges, ~Day 2-3):
  W9 × 8 regimens

Wave C (after W7+W9 merges, ~Day 3-4):
  W10 × 7 indications

Wave D (after W7 merges, ~Day 3-4):
  W11 × 4 RFs

W13: deferred stubs (open as parking issues only).
```

## Acceptance criteria for this roadmap

- All 28 Tier-2 biomarkers shipped end-to-end (biomarker + RF + indication + regimen + drug wiring) per W7+W8+W9+W10+W11.
- 104 outstanding BMAs closed via W12a (CIViC link or `no_civic_match_reason`).
- 131 oldest sources refreshed via W12b.
- W13 stubs filed, deferral rationale + revisit triggers documented.
- KB validator stays clean throughout.
- pytest 62-case fixture never regresses without documented justification.
- All chunks self-pushed per CLAUDE.md `3a60901b`.

## Appendix A — counts at roadmap-author time (2026-05-01)

- biomarkers: 125
- biomarker_actionability: 399 (104 outstanding for CIViC)
- sources: 271 (131 selected for wave-2 refresh)
- drugs: 220 (220 with NSZU axis complete; 13 of 35 Tier-2 drugs already in KB)
- pytest fixture: `tests/test_curated_chunk_e2e.py` = 62 passed

## Appendix B — drugs already in KB (W8 scope reduction)

Confirmed present at `origin/master` HEAD `5df14cc8`: avapritinib, blinatumomab, capivasertib, fruquintinib, inotuzumab_ozogamicin, mirvetuximab_soravtansine, mosunetuzumab, niraparib, quizartinib, repotrectinib, talazoparib, teclistamab, tisagenlecleucel.

These are referenced by W9 regimens and W10 indications but are NOT re-authored in W8. The original Tier-2 brief listed 35 drugs; W8 scope reduced to **21**.

## Appendix C — recency-stat reconciliation note

Orchestrator brief specified "131 sources with `last_verified` older than 2026-04-01". Actual filesystem state at `5df14cc8` shows 270/271 sources with `last_verified` in 2026-04 (post wave-1 batch refresh). Roadmap therefore selected 131 oldest sources by `current_as_of` (missing-field first, then ascending date) as the wave-2 priority queue. Manifests reflect that selection. Final report flags this discrepancy.
