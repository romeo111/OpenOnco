# KB Coverage Strategy v0.2 — Proposals

**Status:** draft, 2026-04-30. Inputs to a future v0.2 revision of
[`docs/kb-coverage-strategy.md`](../kb-coverage-strategy.md). Not authoritative
on its own — adoption requires Co-Lead signoff per the strategy doc's own
governance section.

## Why this exists

The current v0.1 strategy doc + matrix answer "where are we?" and "where are
we going?" but leave four gaps that make the plan harder to execute than it
should be:

1. **Misleading 100% headlines.** ESCAT-tier and `expected_outcomes` both show
   100% in the matrix, but the 100% is presence-of-field, not verified
   correctness. The B2 audit subset projects ~25% mistier rate at full scale.
2. **Capacity is parenthetical.** "BMA UA-signed-off: 0% → 100% (bottleneck:
   Co-Lead queue)" hides the single biggest precondition for v1.0 in a side
   note. Throughput numbers should be first-class targets.
3. **No prioritization function.** The "pick a cell that has high
   gap-magnitude / UA-population priority / scriptable methodology" checklist
   doesn't disambiguate when those criteria conflict — and they often do
   (rare lymphomas have high gap but low scriptability and unmeasured UA
   weight).
4. **Living-data automation has no owners.** NCCN, FDA, trial readouts all
   marked ❌ with no chunks pointing at them. The "Sources <365d ≥60%" target
   is unreachable through manual labor alone.

These proposals are scoped to the strategy doc only. The matrix is
auto-generated and re-runs against KB state — no proposal here changes how
the matrix is built (those would be Queue-C chunks, listed separately
below).

## Proposal 1 — Split presence-of-field rows from verified rows

**Current** (per-entity-type quality targets table):

| BMA with valid ESCAT tier | 100% | 100% **and ≥85% verified** (B2 audit shows nominal 100% has ~10% overclaim risk) |
| Indications with `expected_outcomes` | 100% | 100% **and ≥90% citation-traceable** to a specific RCT |

**Proposed:**

| BMA with ESCAT tier set (presence-of-field) | 100% | 100% (already met; necessary but not sufficient) |
| BMA with ESCAT tier audited + verified | ~3% (12/399 in B2 subset) | ≥85% verified across all 399 (B2 subset projects ~25% mistier rate at full scale) |
| Indications with `expected_outcomes` (presence) | 100% | 100% (already met) |
| Indications with `expected_outcomes` citation-traceable to a specific RCT | not yet measured | ≥90% |

**Why:** the current single-row format conflates "the field exists" with
"the field is correct." A reader skimming the matrix sees 100% twice and
walks away thinking ESCAT is solved. The B2 subset projects ~120 overclaim +
~175 underclaim across 399 BMAs; that should be the headline, not the
parenthetical.

**How to apply:** strict text replacement in the per-entity-type quality
targets table; no script changes needed.

## Proposal 2 — New "Capacity assumptions" subsection

**Insert** after the per-entity-type quality targets table, before the
Living-data targets table:

```
### Capacity assumptions

The targets above are unreachable without throughput to match. Treat these
as first-class targets, not parentheticals.

| Resource | Current throughput | v1.0 requirement | Gap |
|---|---|---|---|
| Co-Lead BMA signoff | 0/week (queue cold) | ≥10 BMA/week sustained, or ≥40/month batched | unblocking this is the single biggest precondition for v1.0 |
| Co-Lead RF/IND review | ad-hoc | ≥1 batched review day/month | minor compared to BMA queue |
| Refresh automation chunks | 1 (CIViC monthly) | ≥3 (CIViC + NCCN + FDA) | 2 chunks need owners — see Queue C |
| ESCAT verification budget | 12 BMAs audited (B2 subset) | full 399 audited | ~830k tokens, 1 chunk (already in Queue B "Examples next") |

Surface the Co-Lead-queue blocker in every quarterly governance review until
throughput is non-zero. A roadmap that depends on a stalled bottleneck is
not a roadmap.
```

**Why:** with 399 BMAs pending and 0/week landing, "100% UA-signoff" is
aspirational rather than falsifiable. Putting capacity in the targets table
makes the bottleneck visible to governance reviews.

**How to apply:** placeholder numbers (≥10 BMA/week, ≥40/month) need
Co-Lead calibration before adoption. The structure is the proposal; the
numbers come from the people who'd do the signoff.

## Proposal 3 — Queue A / Queue D triage rule

**Current** (newly-added paragraph at the end of per-entity-type table in
the version with Queue D additions):

> Queue-D work should be prioritized before more broad expansion when a
> disease or entity family already has unverified claims.

**Proposed** — replace with:

```
### Queue A / Queue D triage rule

Both queues run in parallel. Use these guard rails instead of a blanket
"verify before expand" rule (which would freeze the KB, since every BMA
family has unverified claims):

- Queue D **blocks** Queue A only on the same `disease × axis` cell
  currently under active verification (don't add new BMAs to a disease
  whose existing BMAs are mid-audit).
- Queue D **takes priority** for diseases that already have ≥3 BMAs but
  unresolved evidence-quality gaps (104 BMAs missing CIViC, ~120 projected
  ESCAT overclaims).
- Queue A **proceeds freely** for the 14 zero-BMA diseases — no
  verification work is gated on records that don't exist yet.
- A plan with fewer traceable, fresh, licensed, reviewed records beats a
  larger plan with unclear evidence state — but this is a per-cell
  prioritization, not a global gate.
```

**Why:** the original rule, taken literally, blocks all expansion forever
because every BMA family has unverified claims (UA-signoff = 0% across the
board). The three guard rails preserve the spirit ("verify before expand
where verification is in progress") while keeping the 14 zero-BMA diseases
unblocked.

**How to apply:** strict text replacement.

## Proposal 4 — Living-data automation chunks

**Add to Queue C "Examples next":**

```
- Living-data refresh automation (top-2 sources first). NCCN guideline
  poller (per-disease, ~6-monthly) and FDA approvals weekly poller. Each
  is a Queue-C effort that produces a Queue-A pipeline. Without these,
  the "Sources `current_as_of <365d` ≥60%" target is unreachable through
  manual labor (243 of 269 sources are currently >1y stale; manual
  re-verification doesn't scale at this volume + cadence). Trial
  pivotal-readout monitoring and UA-registration sync are the next two
  after these land.
```

**Why:** the Living-data targets table has 4 ❌ rows and only 1 ✅. Naming
chunks-with-owners is how those Xs become checkmarks; without that, the
target is decorative.

**How to apply:** add as bullet to existing Queue-C "Examples next" list.
Actual chunk-spec authoring is downstream work, not part of this proposal.

## Proposal 5 — Promote citation density + recency from deferred to v0.2

**Current** ("What we don't yet measure"): six items, all "deferred to v0.2"
without distinction.

**Proposed:** split into two subsections:

```
### v0.2 — must add before v1.0 sign-off

1. Citation density per claim. Without this, "BMA with sources" remains
   presence-of-field — one source counts the same as five. Distribution
   histogram per entity type.
2. Recency of cited evidence. % of citations from <2020 / 2020-2024 /
   2024+. Source-level `current_as_of` is necessary but not sufficient —
   the underlying citations themselves age.

### v0.3+ — deferred but tracked

3. Coverage of trial readouts per regimen
4. Toxicity-profile completeness per regimen
5. UA epidemiology weighting
6. Per-disease patient-scenario coverage
```

**Why:** without citation density, two BMAs with one source each look the
same as two BMAs with five sources each in the matrix. That's a hidden
quality gap that affects every disease row. Recency matters because oncology
evidence from 2018 is often superseded — source-level `current_as_of`
doesn't catch that. The other four are real but can wait; these two block
v1.0 credibility.

**How to apply:** restructure the section. Implementation requires a
matrix-script change (Queue C) — count + bucket citations per BMA/IND, emit
new columns in the matrix.

## Proposal 6 — Strict tiered priority for chunk selection

**Current** ("For maintainers picking the next chunk"):

> 3. Pick a cell that:
>    - Has high gap-magnitude (zero or low %)
>    - Has UA-population priority (rare lymphomas if epidemiology-weighted; otherwise volume)
>    - Has scriptable methodology (don't open chunks where the work would be one expert reading 5 papers)

**Proposed** — replace step 3 with:

```
3. Apply the Queue A / Queue D triage rule above to filter candidates.
4. Rank surviving candidates by this strict lexicographic order — only
   break ties at the next tier:
   - Tier 1 — gap magnitude. Zero-coverage cells before thin-coverage
     before quality-gap cells. Within each, larger absolute gap wins.
   - Tier 2 — UA epidemiology weight. Until measured (v0.3 deferred
     metric), use volume proxy: NSCLC / breast / CRC / prostate beat
     rare lymphomas. Override only with explicit clinical-co-lead
     direction.
   - Tier 3 — scriptability. Cells where work is N records of mechanical
     extraction beat cells requiring expert read-through of 5 papers.
   - Tier 4 — cost. Lowest expert-hours estimate wins.
5. Open chunk-spec referencing both the specific cell and the priority
   tier it satisfied.
```

**Why:** the current checklist is three independent criteria that often
conflict (rare lymphomas have high gap-magnitude, low scriptability, and
unmeasured UA weight — pick which wins?). Lexicographic ordering breaks
ties deterministically; "asserted UA-priority for rare lymphomas" gets
demoted unless a clinical co-lead says otherwise.

**How to apply:** text replacement. The Tier-2 UA-weight rule contradicts
the existing Queue-A "Examples next" line that asserts rare-lymphoma
priority — that line should also be reconciled (see Proposal 7).

## Proposal 7 — Reconcile Queue-A "Examples next" with Tier 2 priority

**Current** (Queue A "Examples next"):

> 14 zero-BMA diseases need ≥3 BMAs each (~42 new BMA records). Priority
> on UA-frequent rare lymphomas (PTCL-NOS, NK/T-Nasal, MF-Sezary).

**Proposed:**

```
- 14 zero-BMA diseases need ≥3 BMAs each (~42 new BMA records). Apply
  the Tier-2 volume proxy until UA epidemiology is measured: HNSCC,
  low-grade glioma, MPNST, chondrosarcoma — all higher-volume than the
  rare lymphomas. PTCL-NOS / NK-T-Nasal / MF-Sezary are also zero-BMA
  but should wait for explicit clinical-co-lead UA-frequency
  confirmation.
```

**Why:** the rare-lymphoma priority assertion in v0.1 is exactly the kind
of unverified prioritization the v0.3 UA-epidemiology metric is meant to
fix. Without that data, defaulting to volume proxy is honest; asserting
UA-frequency for three specific rare lymphomas is not.

**How to apply:** text replacement.

## Adoption sequence

If all seven proposals are accepted as-is, applying them is one
documentation PR (~150 lines added, ~25 removed). Recommended sequence:

1. Get Co-Lead calibration on Proposal 2 capacity numbers (≥10 BMA/week
   etc.). Without that, the table is structurally right but numerically
   placeholder.
2. Apply Proposals 1, 3, 4, 5, 6, 7 — these are mechanical doc edits with
   no external dependencies.
3. Apply Proposal 2 with the calibrated numbers.
4. Bump strategy doc version to v0.2 in the status line.

The Queue-C work that Proposal 5 implies (matrix script change for
citation density + recency columns) is a separate effort — that's a code
change, not a doc change.

## Open questions

- **Capacity numbers (Proposal 2).** ≥10 BMA/week is a guess. Real
  throughput depends on Co-Lead time per BMA × number of Co-Leads ×
  hours/week. Need calibration.
- **Tier-2 volume proxy specifics (Proposal 6).** "NSCLC / breast / CRC /
  prostate beat rare lymphomas" is rough. Better: rank by national cancer
  registry volume once available. Until then, the proxy is good enough
  for ordering 14 zero-BMA diseases.
- **Whether Proposal 5's two new metrics need Pydantic schema changes.**
  Citation density is computable from existing `evidence_sources` blocks
  and citation arrays; recency requires that citations have publication
  dates, which not all do. Schema gap may surface during implementation.
