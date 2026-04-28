# J-draft re-attribution — Phase 5+ (CIViC pivot follow-up)

**Date:** 2026-04-27
**Author:** automation (`scripts/reattribute_j_drafts.py`)
**Predecessors:**
- `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` (CIViC-pivot ToS audit)
- `docs/reviews/bma-j-drafts-civic-diff-2026-04-27.md` (Phase 3-O J-draft / CIViC diff)

## 0. Why

Phase 1.5 of the CIViC pivot migrated legacy `oncokb_level: <N>` claims
into structured `evidence_sources: [{source: SRC-ONCOKB, ...}]` entries.
Phase 3-N then attached CIViC therapeutic-option evidence wherever a
biomarker's `actionability_lookup` returned hits.

The Phase 3-O audit (`docs/reviews/bma-j-drafts-civic-diff-2026-04-27.md`)
identified **18 of the 23 J-agent BMA drafts** (`drafted_by:
claude_extraction`) where CIViC has **no actionable evidence** because
the underlying biomarker is IHC / methylation / a composite signature /
a multi-allele panel — i.e. categorically out of CIViC's variant-level
scope (NO-LOOKUP, n=16) — or because CIViC happens to have no
therapeutic option for the specific (gene, variant) (NO-EVIDENCE, n=2:
EZH2 Y641N FL, NPM1 W288fs AML).

These 18 BMAs still carried only the legacy `SRC-ONCOKB` `evidence_sources`
entry, which the render layer skips (per OncoKB ToS §2.5 / §4.2 — the
Phase 1 pivot rationale). End-effect: the BMA renders as **uncited**
to clinicians even though `primary_sources` already names guideline-tier
sources (NCCN/ESMO/ASCO and pivotal trials).

## 1. What this run did

`scripts/reattribute_j_drafts.py` (idempotent, with `--dry-run`):

1. For each J-draft whose `evidence_sources` consisted only of
   `SRC-ONCOKB`, **dropped** the legacy entry (per ToS — citation-shaped
   data we cannot legally surface).
2. **Promoted** each non-OncoKB `primary_sources` entry into a fresh
   `evidence_sources` row with `level: "pending-extraction"`. We
   deliberately do NOT invent the source's level token; the per-source
   level call (NCCN Category, ESMO grade, etc.) needs human extraction
   from the actual guideline section. The promoted entry's `note`
   explains this.
3. Where the post-promotion BMA carried fewer than two entries (i.e. its
   only non-OncoKB primary source is itself a stub), set
   `blocked_on_source_ingestion: [<stub-source-id>]` so the clinical
   co-lead can prioritise ingestion.
4. Set `actionability_review_required: true` (already true on most).

## 2. Per-BMA outcome

All 18 NO-LOOKUP / NO-EVIDENCE J-drafts processed. Numbers count
`evidence_sources` entries on disk after the run.

| BMA | biomarker | disease | `evidence_sources` before | `evidence_sources` after | blocked? |
|---|---|---|---:|---:|---|
| BMA-CALR-ET | BIO-CALR | DIS-ET | 1 | 3 | — |
| BMA-CALR-PMF | BIO-CALR | DIS-PMF | 1 | 6 | — |
| BMA-CD30-ALCL | BIO-CD30-IHC | DIS-ALCL | 1 | 2 | — |
| BMA-CD30-CHL | BIO-CD30-IHC | DIS-CHL | 1 | 2 | — |
| BMA-CXCR4-WHIM-WM | BIO-CXCR4-WHIM | DIS-WM | 1 | 2 | — |
| BMA-ESR1-MUT-BREAST | BIO-ESR1 | DIS-BREAST | 1 | 2 | — |
| BMA-EZH2-Y641-FL | BIO-EZH2-Y641 | DIS-FL | 1 | 2 | — |
| BMA-HER2-AMP-CRC | BIO-HER2-SOLID | DIS-CRC | 1 | 2 | — |
| BMA-HER2-AMP-ESOPHAGEAL | BIO-HER2-SOLID | DIS-ESOPHAGEAL | 1 | 2 | — |
| BMA-HER2-AMP-GASTRIC | BIO-HER2-SOLID | DIS-GASTRIC | 1 | 2 | — |
| BMA-HRD-STATUS-BREAST | BIO-HRD-STATUS | DIS-BREAST | 1 | 3 | — |
| BMA-HRD-STATUS-OVARIAN | BIO-HRD-STATUS | DIS-OVARIAN | 1 | 2 | — |
| BMA-HRD-STATUS-PDAC | BIO-HRD-STATUS | DIS-PDAC | 1 | 2 | — |
| BMA-HRD-STATUS-PROSTATE | BIO-HRD-STATUS | DIS-PROSTATE | 1 | 3 | — |
| **BMA-IDH1-R132-CHOLANGIO** | BIO-IDH-MUTATION | DIS-CHOLANGIOCARCINOMA | 1 | **1** | **yes — SRC-NCCN-HEPATOBILIARY** |
| BMA-IGHV-UNMUTATED-CLL | BIO-IGHV-MUTATIONAL-STATUS | DIS-CLL | 1 | 3 | — |
| BMA-MGMT-METHYLATION-GBM | BIO-MGMT-METHYLATION | DIS-GBM | 1 | 2 | — |
| BMA-NPM1-AML | BIO-NPM1 | DIS-AML | 1 | 5 | — |

## 3. Counts

| metric | n |
|---|---:|
| J-drafts in scope | 23 |
| CONFIRMED by Phase 3-N (skipped by this script) | 5 |
| Targeted by this run | 18 |
| Promoted (`evidence_sources` count increased) | 18 |
| Still blocked (<2 `evidence_sources` entries post-promotion) | 1 |

## 4. Stay-blocked list

Only one BMA remains under-cited after re-attribution:

### BMA-IDH1-R132-CHOLANGIO

- **Why blocked:** the only non-OncoKB `primary_sources` entry is
  `SRC-NCCN-HEPATOBILIARY`, which is currently an auto-stub
  (`drafted_by: claude_extraction`, `ingestion.method: none`, title
  contains a `TODO` placeholder for confirmed citation).
- **`blocked_on_source_ingestion`:** `SRC-NCCN-HEPATOBILIARY`
- **Unblock action:** ingest NCCN Hepatobiliary v3.2025 (or whatever
  current version is) and replace the stub. After that, also consider
  ingesting `SRC-CLARIDHY-ABOU-ALFA-2020` (the pivotal IDH1 cholangio
  RCT), which the BMA's `notes` field already calls out as a source-gap.

## 5. Top-3 most-impactful blocked drafts

Only one BMA is hard-blocked (see §4). The brief asked for top-3 most-
impactful blocked drafts — there is one. The remaining 17 are
"soft-blocked" in the sense that their promoted citations carry
`level: pending-extraction` until clinical extraction. A future Phase 6
should walk those level fields.

The single hard-blocked driver is `SRC-NCCN-HEPATOBILIARY` (unblocks 1
BMA: BMA-IDH1-R132-CHOLANGIO).

## 6. What the script does NOT do

- Does not invent per-source level tokens. Each promoted entry's
  `level` is the sentinel string `"pending-extraction"`; clinical
  co-lead must replace it with the actual NCCN Category / ESMO MCBS /
  trial-tier value during the actionability-review pass that
  `actionability_review_required: true` flags.
- Does not touch the 5 J-drafts already enriched by CIViC in Phase 3-N
  (BMA-BRAF-V600E-CHOLANGIO, BMA-BRAF-V600E-THYROID-ANAPLASTIC,
  BMA-JAK2-V617F-ET / -PMF / -PV).
- Does not modify any non-J-draft BMAs (e.g. cells with
  `drafted_by: clinical_signoff` or absent — those carry the standard
  Phase 1.5 SRC-ONCOKB legacy entry but are clinician-authored and
  preserve the entry pending the Phase 6 sweep).
- Does not delete `SRC-ONCOKB` from `primary_sources` — that list is
  the bibliographic record. The render-layer ToS-skip rule applies
  only to `evidence_sources` entries.

## 7. Validation

- `python -m knowledge_base.validation.loader knowledge_base/hosted/content`
  → all entities valid, all references resolve.
- `pytest tests/test_biomarker_actionability.py -q` → 23 passed, 1 skipped
  (the 1 skip is the legacy `oncokb_level` schema check, intentionally
  parked since Phase 1 of the CIViC pivot).

## 8. Idempotency

Re-running the script after the first apply lists **0 targets**: the
filter `evidence_sources == [{source: SRC-ONCOKB}]` no longer matches
once the legacy entry is dropped, and the existing promoted entries
short-circuit a second promotion pass. Verified.

## 9. Sign-off ask (clinical co-lead)

For each of the 18 processed BMAs:

1. Walk `evidence_sources[*].level` and replace the
   `"pending-extraction"` sentinel with the actual source-level token
   read from the NCCN/ESMO/ASCO/trial body of the source.
2. Confirm the BMA's `escat_tier` against the post-promotion citation
   set (the audit doc §2 has the prior tier; check it still holds when
   the OncoKB call is no longer surfaced).
3. For `BMA-IDH1-R132-CHOLANGIO`, prioritise ingesting
   `SRC-NCCN-HEPATOBILIARY` (and ideally `SRC-CLARIDHY-ABOU-ALFA-2020`)
   to clear the `blocked_on_source_ingestion` flag.

## 10. Files touched

- `scripts/reattribute_j_drafts.py` (new; idempotent + `--dry-run`)
- `docs/reviews/j-drafts-reattribution-2026-04-27.md` (this file)
- 18 BMA YAMLs under `knowledge_base/hosted/content/biomarker_actionability/`:
  - `bma_calr_et.yaml`
  - `bma_calr_pmf.yaml`
  - `bma_cd30_alcl.yaml`
  - `bma_cd30_chl.yaml`
  - `bma_cxcr4_whim_wm.yaml`
  - `bma_esr1_mut_breast.yaml`
  - `bma_ezh2_y641_fl.yaml`
  - `bma_her2_amp_crc.yaml`
  - `bma_her2_amp_esophageal.yaml`
  - `bma_her2_amp_gastric.yaml`
  - `bma_hrd_status_breast.yaml`
  - `bma_hrd_status_ovarian.yaml`
  - `bma_hrd_status_pdac.yaml`
  - `bma_hrd_status_prostate.yaml`
  - `bma_idh1_r132_cholangio.yaml`
  - `bma_ighv_unmutated_cll.yaml`
  - `bma_mgmt_methylation_gbm.yaml`
  - `bma_npm1_aml.yaml`
