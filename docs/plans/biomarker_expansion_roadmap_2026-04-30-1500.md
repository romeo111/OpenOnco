# Biomarker expansion roadmap (Tier 1 + Tier 2 + Tier 3, excl. LymphGen) — 2026-04-30-1500

**Status:** active planning track. Sequel to `docs/plans/curated_examples_expansion_2026-04-29-0313.md`.
**Driver:** clinical-specialist gap audit of `knowledge_base/hosted/content/biomarkers/` (111 entries as of `ca21b9f7`).
**Excluded scope:** LymphGen DLBCL subtype classifier — moved to `docs/plans/lymphgen_dlbcl_proposal_2026-04-30-1500.md` (deferred until composite-classifier engine layer + FDA-approved subtype-targeted therapy).
**Related docs:** `docs/plans/kb_data_quality_plan_2026-04-29.md` (Q1/Q5 quality gates), `docs/plans/curated_examples_expansion_2026-04-29-0313.md` (prior chunk-fleet pattern).

## Why this exists

A clinical oncology specialist auditing OpenOnco today would flag ~12 immediate-impact biomarker gaps + ~12 stratification gaps. Each gap maps to either an FDA-approved drug we cannot route to (Tier 1) or a research-grade stratification we don't yet model (Tier 2). The 60 curated cases shipped on `f69e5d24` exposed an additional 10 KB-drift signals — engine-side and content-side fixes that the new biomarkers will partially overlap with.

This roadmap turns "add more biomarkers" into concrete chunks with allowlists, validation gates, and explicit stop conditions, mirroring the curated-cases pattern that landed cleanly.

## Workstream summary

| ID | Workstream | Cadence | KB-edits? | Owner agent count |
|---|---|---|---|---|
| W1 | Tier-1 biomarkers (12) — 4 disease-area chunks + integration | this week | yes | 5 |
| W2 | Curated-case regression fixture + `#Curated` coverage column | parallel with W1 | no | 1 |
| W3 | Tier-2 biomarkers (~12, no LymphGen) — deferred to v0.2 | next month | yes | TBD |
| W4 | Tier-3 biomarkers — deferred to post-v1.0 | rare-disease roadmap-gated | yes | TBD |
| W5 | KB drift fixes from curated chunks (10 signals) — engine + KB authoring | parallel | yes (engine + KB) | 3-4 |
| W6 | LymphGen DLBCL classifier | deferred | requires engine layer | see separate plan |

## W1 — Tier-1 biomarkers (12 across 4 chunks)

**Goal:** add 12 immediate-impact biomarkers + their indication/regimen/algorithm wiring. Closes the gap between FDA-approved targeted therapies and the engine's ability to route patients to them.

### Chunks (parallel, branch off `origin/master`)

#### B1 — Myeloid (AML + MDS) — 4 biomarkers

- **KMT2A (MLL) rearrangement** → IND-AML-2L-KMT2A-REVUMENIB (AUGMENT-101, FDA Nov 2024)
- **IDH2 R140Q** + **IDH2 R172K** → IND-AML-2L-IDH2-ENASIDENIB (IDHENTIFY)
- **TP53 adverse-AML** → ELN-2022 risk classification, informational + future Ven-Aza preference
- **del(5q) MDS-LR** → IND-MDS-LR-DEL5Q-LENALIDOMIDE (MDS-005)

KB delta: ~5 bio + ~4 RF + ~2 reg + ~2 drug + ~2 ind. Algorithm edits: `algo_aml_2l.yaml` (+2 steps), `algo_mds_lr_1l.yaml` (+1 step).

#### B2 — Solid GI (gastric + CRC + cholangio) — 3 biomarkers

- **CLDN18.2** → IND-GASTRIC-METASTATIC-1L-CLDN18-2-ZOLBETUXIMAB (SPOTLIGHT/GLOW, FDA Oct 2024)
- **HER2-amp CRC** (distinct from existing HER2-solid IHC for breast/gastric) → IND-CRC-METASTATIC-2L-HER2-AMP-MOUNTAINEER (FDA Jan 2023)
- **FGFR2 fusion** → IND-CHOLANGIO-2L-FGFR2-FUSION-PEMIGATINIB (FIGHT-202, FDA Apr 2020)

KB delta: ~3 bio + ~3 RF + ~3 reg + ~3 drug + ~3 ind. Algorithm edits: `algo_gastric_metastatic_1l.yaml`, `algo_crc_metastatic_2l.yaml`, possibly new `algo_cholangio_2l.yaml`.

#### B3 — Breast / NSCLC / Prostate — 3 biomarkers

- **HER2-low** (IHC 1+/2+ FISH−) → IND-BREAST-HER2-LOW-MET-2L-TDXD (DESTINY-Breast04, FDA Aug 2022)
- **MET amplification** (distinct from MET ex14) → IND-NSCLC-2L-MET-AMP-CAPMATINIB (GEOMETRY mono-1, off-label common)
- **AR-V7 splice variant** → biomarker + RF only (informational; no Tx-modifying indication in current KB scope; PROPHECY trial predictive)

KB delta: ~3 bio + ~3 RF + ~1 reg + ~2 ind. Algorithm edits: breast HER2-2L, NSCLC-2L step extension.

#### B4 — Pan-tumor — 4 biomarkers (TROP2 + POLE + POLD1 + IDH1 expansion)

- **TROP2 expression** → biomarker + RF only (sacituzumab eligibility implicit in existing regimens for TNBC + urothelial)
- **POLE hypermutator** → IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION (TransPORTEC; observation only, no chemo/RT)
- **POLD1 hypermutator** → same path as POLE
- **IDH1 R132C** + **IDH1 R132G** → variant-level expansion of existing IDH1 R132H; reuse REG-IVOSIDENIB

KB delta: ~5 bio + ~1 RF + ~1 ind.

### W1 sequencing

- **Phase 1:** B1 + B2 + B3 + B4 in parallel (worktree-isolation per chunk, branch off `origin/master`).
- **Phase 2:** Single integration agent merges 4 chunk-branches via `--no-ff`, runs full validator + pytest + engine smoke on representative existing cases per disease area, commits + pushes.

### W1 validation gates (each chunk)

1. KB validator: `PYTHONIOENCODING=utf-8 C:/Python312/python.exe -m knowledge_base.validation.loader knowledge_base/hosted/content` → "OK — all entities valid". Entity counts ≥ baseline.
2. Pre-merge baseline: `pytest tests/ -x -q --ignore=tests/test_curated_chunk_e2e.py` → record pass count. Post-edit: same command → pass count ≥ baseline.
3. Engine smoke on 2-5 existing curated cases per disease in chunk's scope (e.g., B1 runs against `examples/patient_aml_*.json`, `patient_mds_*.json`) — exit 0, default indication still resolves (may differ if new biomarker fires for that patient — document if so).
4. NO existing YAML modified outside the chunk's algorithm-extension scope. Verify: `git diff --name-only origin/master | grep -v "^knowledge_base/hosted/content/"` should be empty.
5. KB drift surfaces honestly in commit body — do not silently fix routing if engine routes to unexpected indication; document instead.

### W1 stop conditions

- Validator regression
- pytest regression
- Algorithm-file restructure required (vs additive step) — escalate to user
- Existing YAML modification beyond additive sections
- Trial Source ID missing from KB and required by indication — drop case + document, do not invent IDs
- Two chunks editing same algorithm file (B1 KMT2A vs B1 IDH2 both touch `algo_aml_2l.yaml` — chunk B1 owner serializes internally; B2/B3/B4 disjoint by design)

### W1 self-push

Authorized per CLAUDE.md `3a60901b`. Chunk branches: `chunk/biomarker-tier1-{myeloid|gi|breast-thoracic-prostate|pantumor}-2026-04-30-<HHMM>`. Integration: `feat/biomarker-tier1-integration-2026-04-30-<HHMM>`.

## W2 — Curated-case regression fixture + `#Curated` matrix column

**Goal:** convert 60 curated `examples/patient_*.json` shipped via PR #150 into a parametrized pytest module + add `#Curated` column to `scripts/disease_coverage_matrix.py` output.

**Status:** prompt drafted, ready to spawn. Self-contained brief available in this session's recent message.

**Integration with W1:** W2 should land BEFORE W1 chunks merge — provides the regression baseline that W1 chunk-agents need to compare against. If W1 changes engine routing for any of the 60 cases (because a Tier-1 biomarker fires for a curated patient), the test will fail and force documentation.

**Branch:** `feat/curated-cases-regression-fixture-2026-04-30-<HHMM>`. No KB edits.

## W3 — Tier-2 biomarkers (deferred to v0.2)

Specialist-noted gaps that don't have immediate FDA-approved-drug routing or require multi-entity stratification work:

- CD79B mutation (DLBCL ABC-subtype + ibrutinib R-CHOP signal — not LymphGen, just the gene)
- BCL6 fusion / NOTCH2 mutation (BN2-like genetics, but added as standalone biomarkers)
- BRCA somatic vs germline distinction (currently aggregated)
- PALB2, ATM, CDK12 germline/somatic discrimination (PROfound prostate granularity)
- CDH1 (lobular breast / hereditary diffuse gastric)
- AR amplification (mCRPC ARSI-resistance complement to AR-V7)
- TMPRSS2-ERG fusion (prostate prognostic)
- HRD scoring methodology distinction (Myriad vs FoundationOne assay-specific cutoffs)
- PD-L1 IHC clone fragmentation (22C3 / SP142 / SP263 / 28-8 — currently TPS/CPS only)
- NRG1 fusion (zenocutuzumab pan-tumor, FDA Dec 2024)
- BRAF non-V600 (class II/III — different drug strategy from V600)
- MSI/dMMR in prostate (small population, pembro eligibility)

**Deferred trigger:** v0.1 → v0.2 milestone close. Re-prioritize per actual specialist feedback once v0.1 launches publicly.

**Out of scope but worth flagging here:** CD22, CD33, BCMA, CD38 as biomarker entities (immunotherapy targets — currently lives in regimens, not biomarkers). Architectural question: do we mint biomarker entities for ICD/CAR-T targets that are universally expressed in their lineage? Resolution: revisit at v0.2 with CHARTER §8 amendment if needed.

## W4 — Tier-3 biomarkers (deferred to post-v1.0)

Rare-disease scope, hereditary-cancer scope, niche pediatric:

- Sarcoma fusions (EWSR1, SS18, DDIT3, MDM2 amp)
- Pediatric/CNS (H3K27M, BRAF-fusion KIAA1549)
- Hereditary cancer panel (Lynch genes individually, TP53 germline, APC, MUTYH)
- GIST PDGFRA D842V (avapritinib)
- Thyroid-specific (DICER1)
- B-cell lineage IHC completeness (CD3/4/8/25/PAX5/TdT/CD79a/Cyclin-D1 for diagnostic mode)

**Deferred trigger:** rare-disease coverage initiative or specific clinical-co-lead request.

## W5 — KB drift fixes from curated-case chunks

The 60 curated cases on `f69e5d24` documented 10 KB/engine drift signals in their commit bodies + JSON `comment` fields. Each is a real bug or content gap. Already-spawned task chip exists for #1.

| # | Drift | Surface area | Fix scope |
|---|---|---|---|
| 1 | Engine track-filter matches by `biomarker_id` only, ignores `value_constraint` (T790M case in S1) | engine | `knowledge_base/engine/_track_filter.py` |
| 2 | `_find_algorithm` doesn't consult `disease_state` for sequential archetypes (4 prostate cases in S5) | engine | `knowledge_base/engine/plan.py::_find_algorithm` |
| 3 | Algo-dispatch by load-order when 2+ algos share `(disease, line_of_therapy)` (HER2-2L wins for all line=2 breast in S2) | engine | same as #2 — needs disambiguation |
| 4 | Free-text `condition:` strings unevaluable outside RF context (S6 RCC/urothelial/endometrial; S7 PDAC; H3 MCL) | KB authoring + engine | RF authoring for the gaps; engine could optionally allow structured condition clauses |
| 5 | KEYNOTE-006 melanoma 1L pembro mono — indication unwired (S4) | KB authoring | new IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO + algo step |
| 6 | KEYNOTE-054 stage III adjuvant melanoma — no algorithm (S4) | KB authoring | new ALGO-MELANOMA-ADJUVANT-1L + IND |
| 7 | HNSCC EXTREME — indication absent (S8 highest gap) | KB authoring | new IND-HNSCC-RM-1L-EXTREME |
| 8 | CPX-351 + GO not branched in ALGO-AML-1L (H1) | KB authoring | algo step expansion + IND for CPX-351 secondary AML |
| 9 | IND-DLBCL-3L-LONCASTUXIMAB + REG-LONCASTUXIMAB-TESIRINE unwired (H2) | KB authoring | new reg + ind |
| 10 | CLL 1L zanubrutinib indication exists but unwired in ALGO-CLL-1L (H3) | KB authoring | algo step extension |
| (bonus) | Esophageal CheckMate-577 unreachable from 1L `output_indications` (S7) | KB authoring | needs PROPOSAL §17 phasing OR explicit adjuvant algo |

**W5 chunking:** group by surface area:
- W5a (engine bugs #1-#3): one PR, one careful agent (or developer hand-fix). Affects ALL existing curated cases — extensive regression testing required.
- W5b (KB authoring #5-#10 + bonus): 1-2 chunks of disease-area authoring, similar pattern to W1.
- W5c (RF authoring #4): small chunk turning the most-impacted free-text conditions into RFs (RCC IMDC int/poor, urothelial EV-pembro eligibility, endometrial dMMR-vs-other, PDAC bilirubin-fitness).

**Sequencing:** W5a should land before W1 integration if at all possible — Tier-1 biomarkers will compound any drift in `_track_filter` / `_find_algorithm`.

## W6 — LymphGen (out of scope for this roadmap)

See `docs/plans/lymphgen_dlbcl_proposal_2026-04-30-1500.md`. Deferred until (a) FDA-approved LymphGen-subtype-targeted therapy or (b) engine extension supporting composite biomarker classifiers.

## Cross-cutting concerns

### Quality gates (per `kb_data_quality_plan_2026-04-29.md` Q1-Q5)

Every new biomarker added in W1 must satisfy:

- **Q1 BMA evidence integrity:** `actionability_lookup` if a single-variant target gene/variant; `oncokb_skip_reason` if structurally unsuitable (composite, IHC, CN, etc.). Mutually exclusive — model_validator enforces.
- **Q2 Source metadata:** every clinical claim cites an existing `SRC-*` ID. If trial Source missing, flag in commit body, do not invent.
- **Q3 UA applicability:** add `ukrainian_review_status: pending_clinical_signoff` and `ukrainian_drafted_by: claude_extraction` markers. UA names in `names.ukrainian`.
- **Q4 Citation density:** each indication ships with at least 2 source citations.
- **Q5 Regression prevention:** W2 fixture (60 cases) is the gate. W1 must not regress it without documented routing-change rationale.

### Multi-session reality

Master moves daily (PR #143 added 362 variants while curated-cases plan was being drafted — chunks needed to branch from a moving target). All W1/W5 chunks branch off `origin/master` at the moment they start, NOT from a frozen baseline. Integration agent merges live HEAD.

### Self-push authorization

Per CLAUDE.md `3a60901b`: chunks self-push when all gates pass. Branch names follow `chunk/<scope>-<YYYY-MM-DD-HHMM>` per memory `feedback_chunk_naming`.

## Sequencing summary

```
Day 1 (parallel):
  W2 (regression fixture + #Curated column)  →  ships first as baseline
  W5a (engine drift fixes #1-#3)              →  optional but high-value before W1
  
Day 2 (parallel):
  W1.B1 (myeloid)                             ┐
  W1.B2 (solid GI)                            │  4 chunks parallel
  W1.B3 (breast/NSCLC/prostate)               │  worktree-isolation
  W1.B4 (pan-tumor)                           ┘

Day 3:
  W1 integration agent                        →  merges B1-B4, full regression test, push

Week 2+:
  W5b (KB authoring drift fixes #5-#10 + bonus) — gradual chunks
  W5c (RF authoring drift fix #4)
  
Month 2+:
  W3 Tier-2 biomarkers (per v0.2 milestone planning)
  
Post-v1.0:
  W4 Tier-3 + W6 LymphGen (gated by clinical evidence + engine extension)
```

## Acceptance criteria for this roadmap

- All 12 Tier-1 biomarkers shipped end-to-end (biomarker + RF + indication + regimen + drug + algorithm wiring) per W1
- W2 fixture passing, gating future engine changes
- 10 drift signals tracked in W5 work log (some fixed, some explicitly deferred with rationale)
- LymphGen plan exists and is up-to-date for future revisit
- KB validator stays clean throughout
- pytest baseline never regresses without documented justification
