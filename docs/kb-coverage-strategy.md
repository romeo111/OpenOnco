# KB Coverage Strategy

**Status:** v0.2 draft, 2026-04-30. Lives alongside the auto-generated [`kb-coverage-matrix.md`](kb-coverage-matrix.md) which is the live snapshot of where we are. This doc explains _how to read it, where v1.0 ends, and how chunks should reference it._

## What this is for

OpenOnco's KB grew opportunistically — gap → chunk → fill → next gap. That works while the maintainer can hold the entire shape of the KB in their head. We're past that point: 2,142 entities across 10 types, 65 diseases × 5 quality axes = 325 cells of state, plus three orthogonal audit dimensions.

This strategy doc + the matrix together answer four questions that the chunk shelf alone cannot:

1. **Where are we now?** (`kb-coverage-matrix.md` — auto-generated)
2. **Where are we going?** (target state, this doc)
3. **What's the next highest-leverage chunk?** (gap × priority weight, this doc)
4. **Are we converging?** (matrix-over-time diff, future cron)

Without it, "база майже готова" is unfalsifiable. With it, "DLBCL row is at 8/12 cells; 4 to go" is an honest statement of progress.

## How chunks reference this

Every new chunk-spec (per `tasktorrent` v0.4 schema) should reference the matrix in its **Mission** section. Pattern:

> _This chunk advances **`kb-coverage-matrix.md > Per-disease matrix > glioma-low-grade > BMA`** from 0 to ≥3 by adding actionability records for IDH1/IDH2/MGMT/1p19q/BRAF V600E in low-grade glioma._

The chunk-spec linter does not enforce this (yet) — it's a writing discipline. Without it, chunks tend to drift toward "what's quick" rather than "what closes a known gap."

### Data-quality rule for all future chunks

Coverage movement is not sufficient. Every new plan or chunk that touches KB
data must also state its **quality gate**: provenance, recency, license/terms,
clinical-strength verification, UA applicability, or signoff readiness.

Use `docs/plans/kb_data_quality_plan_2026-04-29.md` as the quality contract for
chunk authoring. In practice, this means each chunk-spec should declare:

1. The baseline quality gap it addresses.
2. The manifest IDs it owns.
3. The quality field expected to move.
4. The evidence standard for accepting sidecars.
5. The validator or audit command that proves the work did not regress.

Unresolved findings are acceptable when they are explicit. Silent gaps are not.

## Three classes of work, three distinct queues

The matrix surfaces three orthogonal axes; each generates its own queue. They should not compete for the same shelf slot.

### Queue A — Coverage-fill

**Driver:** the matrix's gap sections (zero-BMA, thin-BMA, no-RF, etc.)

**Metric:** entity count ↑ for a specific disease × axis cell.

**Examples already done:**
- `bma-drafting-gap-diseases` (+23 BMA drafts staged, awaiting Co-Lead signoff)
- `redflag-indication-coverage-fill` (+33 RF entries staged)
- `source-stub-ingest-batch` (+40 source stubs staged)
- `trial-source-ingest-pubmed` (+25 SRC, merged 2026-04-28 via PR #29)

**Examples next:**
- 14 zero-BMA diseases need ≥3 BMAs each (~42 new BMA records). Apply the
  Tier-2 volume proxy until UA epidemiology is measured: HNSCC, low-grade
  glioma, MPNST, chondrosarcoma — all higher-volume than the rare lymphomas.
  PTCL-NOS / NK-T-Nasal / MF-Sezary are also zero-BMA but should wait for
  explicit clinical-co-lead UA-frequency confirmation.
- 25 thin-BMA diseases need 2-3 more each (~60 BMA records).
- HNSCC (zero BMA, etiologically_driven) — needs HPV-positive vs HPV-negative
  actionability split + EGFR amplification. Highest-priority candidate by
  volume.

**Risk profile:** low. Chunks here are scriptable + verifiable.

### Queue B — Audit + remediate

**Driver:** the matrix's quality columns (ESCAT%, CIViC%, UA✓ signoff %) and prior audit reports (citation-verify-v2 793 actionable rows; rec-wording 870; ua-translation 1858).

**Metric:** error count ↓, or quality % ↑, in the matrix's quality columns.

**Pattern:** comes in pairs. Audit chunk (cheap, ~1 Drop) generates a triage queue. Remediation chunk (expensive, depends on triage volume) acts on the queue.

**Examples already done (audit half):**
- citation-verify v1 + v2 — 793 actionable rows surfaced, no remediation chunk run yet
- rec-wording-audit-claim-bearing — 870 findings (229 critical), no remediation
- ua-translation-review-batch — 1858 findings (200 critical), no remediation
- escat-tier-audit (B2 subset) — 16 overclaim / 22 underclaim / 12 correct on 50/399 sample. Full audit not yet run; subset alone projects ~120 overclaim + ~175 underclaim across 399.

**Examples next:**
- ESCAT-tier-audit full chunk (~830k tokens) — confirms B2 projection on remaining 349 BMAs.
- citation-verify-v2 remediation chunk — process the 793-row triage queue.
- rec-wording remediation — start with 229 critical only.

**Risk profile:** medium. Triage steps are mechanical; remediation requires expert read-through. Co-Lead queue depth matters.

### Queue C — Schema-evolution

**Driver:** decision to add a new field, relationship, or enrichment block across an existing entity type.

**Metric:** % of entity_type populated with new field Y ↑.

**Examples already done:**
- `civic-bma-reconstruct-all` (399 BMAs gained `evidence_sources` block; oncokb_lookup → actionability_lookup migration)
- The new `volume_impact` block on volume-mutating chunks (Proposal #18)

**Examples next:**
- Add `cost_estimate` / `cost_actual` fields to chunk-spec + `_contribution_meta.yaml` (per owner decision 2026-04-28).
- Add `line_of_therapy_evidence_source` to all 302 indications (currently `evidence_level` is set but not tied to a specific RCT citation).
- Add `tasktorrent_version` to all sidecars (per L-21).
- Add ESMO ESCAT references explicitly when reconstruction work surfaces them.
- **Living-data refresh automation (top-2 sources first).** NCCN guideline poller (per-disease, ~6-monthly) and FDA approvals weekly poller. Each is a Queue-C effort that produces a Queue-A pipeline. Without these, the "Sources `current_as_of <365d` ≥60%" target is unreachable through manual labor (243 of 269 sources are currently >1y stale; manual re-verification doesn't scale at this volume + cadence). Trial pivotal-readout monitoring and UA-registration sync are the next two after these land.

**Risk profile:** front-loaded. Get the schema right (Pydantic, validators), then mass-fill is mechanical.

### Queue D — Data-quality gates

**Driver:** the dedicated data-quality plan and the matrix's quality-gap
sections: source license, source recency, CIViC/no-match status, ESCAT
verification, citation anchors, UA access, and signoff readiness.

**Metric:** quality risk down, not just entity count up. A successful Queue-D
chunk may add zero new hosted entities and still be high value if it converts
unknowns into verified values or explicit unresolved reasons.

**Examples already opened (2026-04-29):**
- `bma-civic-backfill-*` chunks (#43-#63): backfill CIViC evidence or record
  no-match reasons.
- `bma-ua-signoff-prep-*` chunks (#64-#83): prepare BMA records for Ukrainian
  clinical signoff.
- `source-license-backfill-*` chunks (#84-#91): close license/terms gaps.
- `source-recency-refresh-*` chunks (#92-#121): refresh source dates and
  supersession status.
- `drug-ua-nszu-access-audit-*` chunks (#122-#141): verify Ukrainian
  registration and NSZU/reimbursement state.

**Examples next:**
- Require a `Quality Gate` section in every TaskTorrent chunk spec.
- Add citation-density and claim-anchor columns to `kb-coverage-matrix.md`.
- Promote "unresolved reason present" to a first-class success state for
  CIViC, source license, and UA access audits.

**Risk profile:** medium. Most work is mechanical, but acceptance depends on
reviewer-readable evidence and conservative handling of uncertainty.

## v1.0 target state — what "done" looks like

Concrete, falsifiable numbers per axis. Below is a draft proposal; numbers may need clinical-co-lead calibration before adoption.

### Per-disease coverage targets

For each of 65 diseases:

| Axis | v1.0 target | Current bar |
|---|---|---|
| BMA | ≥3 records covering top biomarker classes | 14 diseases at 0; 25 at 1-2 |
| Indications | ≥1 first-line + ≥1 advanced/relapsed line | All 65 ≥1 ✓ |
| Red-flags | 5-type matrix coverage (organ-dysfunction / infection / pregnancy / age / prior-therapy) | All 65 ≥1; 5-type completeness varies |
| Questionnaire | 1 disease-specific questionnaire | All 65 ✓ |
| Source-citation density | ≥2 distinct sources cited from BMA + IND combined | varies; not yet measured per cell |

### Per-entity-type quality targets

| Entity | Current | v1.0 target |
|---|---|---|
| BMA UA-signed-off | 0% | 100% (precondition: Co-Lead capacity — see Capacity assumptions below) |
| BMA with CIViC evidence | 74% | 95%+ (recover the 104 legacy BMAs) |
| BMA with ESCAT tier set (presence-of-field) | 100% | 100% (already met; necessary but not sufficient) |
| BMA with ESCAT tier audited + verified | ~3% (12/399 in B2 subset) | ≥85% verified across all 399 (B2 subset projects ~25% mistier rate at full scale, so the headline 100% is misleading until audited) |
| Indications with `expected_outcomes` (presence) | 100% | 100% (already met) |
| Indications with `expected_outcomes` citation-traceable to a specific RCT | not yet measured | ≥90% |
| Sources `current_as_of <365d` | 10% | ≥60% (243 of 269 sources currently >1y stale-by-date) |
| Sources with license declared | 89% | 100% (29 sources need license backfill) |
| Drugs UA-registered | 70% | 75%+ (15 percentage points to gain via НСЗУ + DEC.gov.ua sync) |
| RF with `last_reviewed` | 100% | 100% (current hosted files have no missing `last_reviewed` values) |

### Capacity assumptions

The targets above are unreachable without throughput to match. Treat these as
first-class targets, not parentheticals. Without explicit numbers here,
"BMA UA-signed-off 100%" is aspirational rather than falsifiable.

| Resource | Current throughput | v1.0 requirement | Gap |
|---|---|---|---|
| Co-Lead BMA signoff | 0/week (queue cold) | ≥10 BMA/week sustained, or ≥40/month batched | unblocking this is the single biggest precondition for v1.0 |
| Co-Lead RF/IND review | ad-hoc | ≥1 batched review day/month | minor compared to BMA queue |
| Refresh automation chunks | 1 (CIViC monthly) | ≥3 (CIViC + NCCN + FDA) | 2 chunks need owners — see Queue C |
| ESCAT verification budget | 12 BMAs audited (B2 subset) | full 399 audited | ~830k tokens, 1 chunk (already in Queue B "Examples next") |

The capacity numbers above are placeholders pending Co-Lead calibration; the
structure is the proposal. Surface the Co-Lead-queue blocker in every
quarterly governance review until throughput is non-zero. A roadmap that
depends on a stalled bottleneck is not a roadmap.

### Queue A / Queue D triage rule

Both queues run in parallel. Use these guard rails instead of a blanket
"verify before expand" rule (which would freeze the KB, since every BMA
family has unverified claims):

- Queue D **blocks** Queue A only on the same `disease × axis` cell currently
  under active verification (don't add new BMAs to a disease whose existing
  BMAs are mid-audit).
- Queue D **takes priority** for diseases that already have ≥3 BMAs but
  unresolved evidence-quality gaps (104 BMAs missing CIViC, ~120 projected
  ESCAT overclaims).
- Queue A **proceeds freely** for the 14 zero-BMA diseases — no verification
  work is gated on records that don't exist yet.
- A plan with fewer traceable, fresh, licensed, reviewed records beats a
  larger plan with unclear evidence state — but this is a per-cell
  prioritization, not a global gate.

### Living-data targets (continuous)

| Source | Refresh cadence | Status |
|---|---|---|
| CIViC nightly snapshot | monthly via CI | ✅ landed (commit `0b53a5c`) |
| NCCN guideline updates | per-disease, ~6-monthly | ❌ no automation |
| FDA approvals | weekly | ❌ no automation |
| Trial pivotal-readout monitoring | monthly | ❌ no automation |
| UA-registration registry sync | quarterly | ❌ manual |
| CTCAE v5 reference | annual | ✅ static |

## What we don't yet measure (and should)

The current matrix covers presence-of-field. The gaps below are split by
whether they block v1.0 credibility or can wait. Acknowledging the gap
honestly is more useful than measuring fake completeness — but credibility-
blocking gaps need explicit owners, not deferral.

### v0.2 — must add before v1.0 sign-off

1. **Citation density per claim.** How many independent sources back each
   clinical recommendation. Without this, "BMA with sources" remains
   presence-of-field — one source counts the same as five, even though
   evidence-quality differs sharply. Distribution histogram per entity type.
   Already flagged as a Queue-D "Examples next" item; promote to active.
2. **Recency of cited evidence.** % of citations from <2020 / 2020-2024 /
   2024+. Source-level `current_as_of` is necessary but not sufficient —
   the underlying citations themselves age. Critical for oncology where
   2018 evidence is often superseded.

### v0.3+ — deferred but tracked

3. **Coverage of trial readouts per regimen** — out of 244 regimens, how
   many have an attached `expected_outcomes` block (median OS, ORR, CR
   rate). Probably <50%; trial-outcome ingestion is a future Queue-C chunk.
4. **Toxicity-profile completeness per regimen** — CTCAE v5 grading per
   regimen.
5. **UA epidemiology weighting** — which 14 zero-BMA diseases are most
   common in Ukrainian patient population? (Requires one-off pull from
   МОЗ/НСЗУ statistics.) Without this, "fill all 14" is a 6-month chunk
   batch; with it, "fill the 4 most common first" is 2 weeks. Listed in
   v0.3 not because it's unimportant but because it's a one-off pull, not
   a continuous metric.
6. **Per-disease patient-scenario coverage** — out of N reference cases
   (anonymized), what % can the engine fully process given current KB
   state? End-to-end completeness signal; depends on having reference
   cases curated first.

## How to use this doc + matrix

### For maintainers picking the next chunk

1. Open `kb-coverage-matrix.md`.
2. Look at `Coverage gaps` and `Quality gaps` sections.
3. Apply the **Queue A / Queue D triage rule** above to filter candidates.
4. Rank surviving candidates by this strict lexicographic order — only break
   ties at the next tier:
   - **Tier 1 — gap magnitude.** Zero-coverage cells before thin-coverage
     before quality-gap cells. Within each, larger absolute gap wins.
   - **Tier 2 — UA epidemiology weight.** Until measured (v0.3 deferred
     metric), use volume proxy: NSCLC / breast / CRC / prostate beat rare
     lymphomas. Override only with explicit clinical-co-lead direction.
   - **Tier 3 — scriptability.** Cells where work is N records of mechanical
     extraction beat cells requiring expert read-through of 5 papers.
   - **Tier 4 — cost.** Lowest expert-hours estimate wins.
5. Open chunk-spec referencing both the specific cell and the priority tier
   it satisfied. Without that, the chunk-spec linter has no way to tell
   "what's quick" apart from "what closes the highest-leverage gap."

### For contributors (Codex, Claude, others)

1. Read the chunk-spec
2. Check the chunk-spec's Mission references the matrix cell
3. After execution, the maintainer re-runs `scripts/kb_coverage_matrix.py` and the matrix moves

### For governance (CHARTER, Co-Lead)

1. Quarterly review of matrix-over-time diff
2. v1.0 targets above are negotiable — bring proposed adjustments to Co-Lead signoff PR

## Re-running the matrix

```bash
C:/Python312/python.exe -m scripts.kb_coverage_matrix
git diff docs/kb-coverage-matrix.md     # see what moved
```

Output is read-only against `knowledge_base/hosted/content/`. The script does not mutate KB data.

**Cadence (proposed):**
- After every PR that touches `knowledge_base/hosted/content/` (post-merge maintainer step; could be a CI job)
- Weekly cron, posting the diff to a `kb-state` GitHub Discussion or similar

## Document hygiene

- `kb-coverage-matrix.md` is **machine-generated**. Do not edit. Re-run the script.
- This doc (`kb-coverage-strategy.md`) is **human-edited**. Update v1.0 targets when Co-Lead reviews them; update queue examples as chunks land/fail.
- When the matrix changes meaning (new column added, definition changed), this doc must be updated in the same PR.
