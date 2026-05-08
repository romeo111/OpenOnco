# GI-2 long-tail follow-ups + cross-cutting backlog

**Stamp:** 2026-05-07-2100
**Source:** GI-2 wave Phase A+D closure (master HEAD `7caae642`)
**Status:** BACKLOG — not yet scheduled. Park here for future scheduling once §17 schema refactor lands.

---

## 1. Why this doc exists

GI-2 wave Phase A+D closed cleanly across 14 PRs (#396, #397, #398, #401, #402, #404, #408, #409, #414, #416, #417, #418, #421, #423). During dispatch, agents flagged specific follow-up items that weren't in scope for their chunks. This doc captures them durably so they don't drop on the floor.

The user's next priority is **§17 schema refactor** (Surgery + RadiationCourse + Indication.phases + IntentOfTreatment), which unblocks Phase C (multimodal). All items below are deferred until after that lands.

## 2. Source ingestion follow-ups (small chunks)

### 2.1 KEYNOTE-061 EBV+ subset analysis source
- Flagged in: `bma_ebv_positive_gastric.notes:` (post-W0-5 cleanup)
- Why: BMA cites Kim NatMed 2018 as primary; KN-061 EBV+ subset is supplementary, not yet ingested
- Effort: 1 source-stub chunk, ~10 min agent time
- PMID: search PubMed via WebFetch ("KEYNOTE-061 EBV gastric subset")
- Risk: low — pure additive

### 2.2 Pazopanib primary RCTs
- VEG105192 (Sternberg 2010 JCO — pazopanib RCC)
- PALETTE (van der Graaf 2012 Lancet — pazopanib STS)
- COMPARZ (Motzer 2013 NEJM — pazopanib vs sunitinib non-inferiority)
- Flagged in: `drug_pazopanib.yaml notes:` (post drug-stubs PR #421)
- Currently `drug_pazopanib` cites NCCN-Kidney-2025 + ESMO-RCC-2024 fallback only
- Effort: 1 source-stub chunk, 3 sources, ~15 min
- Risk: low

### 2.3 SRC-FORTITUDE-101 tier upgrade
- Currently `evidence_tier: 2`, `paper_pending: true` (ESMO 2025 LBA10 abstract only)
- Upgrade to tier 1 (`rct_publication`) when full PubMed publication lands
- Trigger: monitor PubMed for FORTITUDE-101 / Rha first-author / NCT05052801
- Effort: 1 source-edit chunk, ~5 min when triggered
- Risk: trivial

### 2.4 DESTINY-Gastric02 watch
- HER2-low Western gastric T-DXd phase 3 trial
- Outstanding readout (not yet published as of 2026-05-07)
- When published: enables HER2-low gastric/esoph T-DXd indication that was deliberately dropped from GI-2 wave
- Trigger: monitor PubMed for DESTINY-Gastric02 / NCT04379596
- Effort: when triggered, full source-stub + new BMA + new indication ≈ 1 chunk

## 3. Naming / hygiene cleanups

### 3.1 Source-ID hyphenation normalisation (issue #400 OPEN)
- KB has 2 conventions: hyphenated (`SRC-CHECKMATE-577-KELLY-2021`) and non-hyphenated (`SRC-CHECKMATE648-DOKI-2022`, `SRC-KEYNOTE590-SUN-2021`, `SRC-KEYNOTE189-GANDHI-2018`, `SRC-CHECKMATE238-WEBER-2017`, etc.)
- W0-2 lost an agent-restart cycle to a collision caused by this inconsistency
- Effort: 1 chunk — audit all `src_*.yaml`, decide canonical (likely hyphenated), rename source files + IDs + propagate citations across `indications/`, `regimens/`, `redflags/`, `algorithms/`, `biomarkers/`, `bma/`
- Estimated touch: 30-50 file edits depending on coverage
- Risk: medium — wide blast radius; needs careful diff review

### 3.2 OMEC-1 year mismatch (subset of #400)
- `SRC-OMEC-1-KROESE-2018` references PMID 36947929 which is actually 2023 paper
- Bundled into renormalisation chunk (3.1) or solo
- Effort: trivial when bundled

### 3.3 English-string predicate cleanup in algo_esoph_metastatic_1l
- Steps 1-4 use English-string `condition:` clauses that functionally never fire
- `default_indication` fallback handles routing instead
- Latent bug — works today by accident
- Flagged by D1 agent (PR #423)
- Effort: 1 chunk to convert to real finding-keyed lookups
- Risk: low if engine smoke confirms no behavior change

## 4. Clinical signoff queue (CHARTER §6.1, §6.2)

Per Phase 1.5 CIViC-pivot schema, all tier-1 BMAs ship with `actionability_review_required: true` until 2/3 Clinical Co-Leads sign off.

Outstanding signoff queue from GI-2 wave:
- `BMA-FGFR2B-MEMBRANE-GASTRIC` (ESCAT IIA) — added in A2 (PR #409)
- `BMA-EBV-POSITIVE-GASTRIC` (ESCAT IIIA) — added in A2 (PR #409); citations upgraded in W0-5 (PR #414)
- `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO` — added in A1 (PR #408); ipi+nivo confidence pattern
- `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO` — extrapolation from gastric ToGA; confidence moderate
- `IND-ESOPH-METASTATIC-2L-HER2-POSITIVE-T-DXD` — extrapolation from gastric DG-04; confidence moderate
- `IND-GASTRIC-METASTATIC-1L-FGFR2B-BEMARITUZUMAB` — bemarituzumab evidence interim (FORTITUDE-101)
- `DRUG-BEMARITUZUMAB`, `DRUG-PAZOPANIB` — drug stubs marked `pending_clinical_signoff` (PR #421)

Operational note: per memory `project_charter_dev_mode_exemptions.md`, §6.1 two-reviewer signoff is dev-mode-exempt during v0.1 phase. So these flags are documentation-only until v1.0 release gate.

## 5. Future workstream candidates (not GI-2 scope)

### 5.1 GI-3 wave: pancreaticobiliary + CRC expansion
- DIS-PDAC: existing scaffold; needs FOLFIRINOX vs gemcitabine+nab-paclitaxel 1L; second-line options; targeted (BRCA, KRAS G12C with sotorasib/adagrasib post-CodeBreaK)
- DIS-CHOLANGIOCARCINOMA: FGFR2 fusions (pemigatinib, futibatinib), IDH1 (ivosidenib), HER2+ (trastuzumab+pertuzumab post-MyPathway / DESTINY-PanTumor02)
- DIS-CRC: KRAS G12C 2L (sotorasib+pembro per CodeBreaK 300), HER2-amplified MOUNTAINEER-02 / DESTINY-CRC01, recent BRAF V600E updates
- Estimated effort: 8-12 chunks, similar pattern to GI-2

### 5.2 Other domain expansions (per memory roadmap)
Maintained in separate roadmap doc — not enumerated here.

### 5.3 Phase C of GI-2 wave (BLOCKED on §17)
- C1 FLOT periop gastric (FLOT4)
- C2 CROSS RT phasing
- C3 definitive CRT esoph SCC unresectable
- C4 MIE / RAMIE selection
- C5 OMEC oligometastatic
- 5 chunks, all §17-blocked. Will be dispatched after §17 ratification + schema bump + migration land.

## 6. Index of related docs

- `docs/plans/gi2_wave_gastric_esophageal_2026-05-04-1730.md` (GI-2 plan, §13 final outcome)
- `docs/plans/q_axis_dispatch_template_2026-05-01.md` (chunk-task template patterns)
- `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md` (Tier-2 roadmap pre-GI-2)
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 (schema PROPOSAL pending ratification)
- Issues: #394 (§17 tracker), #400 (renormalisation backlog)
