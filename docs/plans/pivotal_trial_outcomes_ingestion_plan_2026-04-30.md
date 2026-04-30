# Pivotal Trial Outcomes Ingestion — Plan

**Status:** v0.1 draft, 2026-04-30. Sister plan to
[`kb_data_quality_plan_2026-04-29.md`](kb_data_quality_plan_2026-04-29.md);
implements the v0.2 must-add metric "citation density per claim" from
[`../kb-coverage-strategy.md`](../kb-coverage-strategy.md). Owns the
Queue-D work for `expected_outcomes` traceability.

## Why this plan exists

The KB-coverage strategy (v0.2, merged via PR #163) lists this as a
v0.2 credibility-blocking gap:

> **Citation density per claim.** How many independent sources back each
> clinical recommendation. Without this, "BMA with sources" remains
> presence-of-field — one source counts the same as five.

Drug target databases (DrugBank, Open Targets, ChEMBL) cannot fill this
gap — pivotal-trial outcomes (ORR / mPFS / mOS / DFS-HR) are not their
domain. The data lives in pivotal-trial publications (PubMed / FDA
labels / NCCN evidence appendices), and ingesting it is its own
workstream.

This plan scopes that workstream.

## Current state

| Entity | Total | With `expected_outcomes` block (presence-of-field) | Citation-traceable to a specific RCT (v1.0 target ≥90%) |
|---|---:|---:|---:|
| Indications | 306 | 306 (100%) | **not yet measured** |
| Regimens | 249 | 0 (schema-side: outcomes live on Indication, not Regimen) | n/a |

Every Indication carries an `expected_outcomes: ExpectedOutcomes` block,
but the values inside vary: some have full ORR / CR / PFS / OS-5y
populated against a named trial; others have one or two free-text values
without a citation pointer. The matrix doesn't currently measure the
quality dimension.

### What `ExpectedOutcomes` looks like today

From [`knowledge_base/schemas/indication.py`](../../knowledge_base/schemas/indication.py):

```python
class ExpectedOutcomes(Base):
    overall_response_rate: Optional[str] = None
    complete_response: Optional[str] = None
    progression_free_survival: Optional[str] = None
    overall_survival_5y: Optional[str] = None
    hcv_cure_rate_svr12: Optional[str] = None
    # extra='allow' for disease-specific fields
```

All `Optional[str]`. No structured citation pointer alongside each value
— if `progression_free_survival: "5.5 months"` is filled, the trail back
to "Robert NEJM 2015 (KEYNOTE-006), median PFS 5.5 mo" goes through
`Indication.sources` only. That conflation is the audit gap.

## Goal — v1.0 target state

For each Indication, `expected_outcomes` should:

1. **Be populated** with at least the ORR or PFS or OS value the
   reference trial reports (some palliative / supportive indications
   genuinely don't have RCT data — `null` is acceptable when explicit).
2. **Carry a citation pointer** (SRC ID) per filled value, naming which
   trial publication produced the number. A new field — see "Schema
   evolution" below.
3. **Be readable from the matrix** — `kb-coverage-matrix.md` adds a
   `Outcomes-Cited %` column per disease.

## Schema evolution (Queue C)

Today `ExpectedOutcomes` carries plain strings. Proposed shape:

```python
class OutcomeValue(Base):
    value: str           # "5.5 months", "33-40%", "not reached"
    source: str          # SRC-* citation ID
    confidence_interval: Optional[str] = None  # "95% CI 4.7-6.5"
    median_followup_months: Optional[float] = None

class ExpectedOutcomes(Base):
    overall_response_rate: Optional[OutcomeValue] = None
    complete_response: Optional[OutcomeValue] = None
    progression_free_survival: Optional[OutcomeValue] = None
    overall_survival_5y: Optional[OutcomeValue] = None
    overall_survival_median: Optional[OutcomeValue] = None  # (new)
    disease_free_survival_hr: Optional[OutcomeValue] = None  # (new — adjuvant)
    hcv_cure_rate_svr12: Optional[OutcomeValue] = None
```

Backward compat: `field_validator(mode="before")` accepts either a plain
string (legacy) or an `OutcomeValue` dict (new). Plain string coerces to
`OutcomeValue(value=str, source="SRC-LEGACY-UNCITED")` so the audit can
flag pre-migration entries.

## Sourcing — what data we trust

| Tier | Source | Use case |
|---|---|---|
| 1 | Pivotal trial peer-reviewed publication (NEJM / JCO / Lancet via PubMed) | Primary citation for ORR / PFS / OS / CR |
| 1 | NCT trial registry primary results posting | Co-citation for trials with no full-text |
| 2 | FDA approval label (PI document) | Useful when PI quotes summary stats; cite in addition to (not instead of) the trial paper |
| 2 | NCCN evidence appendix | Acceptable for older trials whose papers are paywalled and not indexed |
| 3 | Review articles / meta-analyses | Last resort; cite only when no primary source exists |
| ⛔ | Drug target databases (DrugBank, Open Targets) | Do not use — they do not carry trial outcomes |
| ⛔ | LLM-synthesized values | Forbidden per CHARTER §8.3 — extraction with verification only |

PubMed is the primary access path. The bio-research plugin's PubMed MCP
or the existing [`knowledge_base/clients/pubmed_client.py`](../../knowledge_base/clients/pubmed_client.py)
can serve as the fetcher; either way, the fetched text is
human-extracted by the agent into `OutcomeValue` records, with the
citation field populated to a real `SRC-*` entity.

## Phases

### Phase 1 — audit (1 chunk, ~1 Drop)

Generate `docs/audits/expected_outcomes_traceability_2026-04-30.md`:

- Read all 306 indications.
- For each `expected_outcomes` field set to a non-null string, attempt
  to match the value to a citation in `Indication.sources` (heuristic:
  string contains a recognized trial abbreviation, source's `title`
  field, or a PMID).
- Output: 4 buckets per indication × per outcome field — `cited`,
  `probably-cited` (heuristic match), `uncited` (value present, no
  source link), `absent` (null).
- Bucket counts roll up to a per-disease column for the matrix.
- No KB mutation in this phase.

### Phase 2 — schema migration (1 Queue-C chunk)

- Add `OutcomeValue` class per the proposal above.
- Add field validator for legacy string → `OutcomeValue(value=str, source="SRC-LEGACY-UNCITED")`.
- Add `outcomes_cited_pct` derivation to the coverage-matrix script.
- Run validator + matrix. Expect ~70-80% of current outcomes to show as
  `SRC-LEGACY-UNCITED` — that's the remediation backlog.

### Phase 3 — gap-fill (multiple chunks, prioritized)

Priority order, applied to the audit's `uncited` and `absent` buckets:

1. **8 shelf-task items first** (KEYNOTE-006/-054, EXTREME, CPX-351, GO,
   loncastuximab, zanu 1L CLL, CheckMate-577) — these are blocking new
   curated cases. Already opened as a separate shelf task.
2. **High-volume diseases** with uncited outcomes — NSCLC, breast, CRC,
   prostate, AML, DLBCL. Each ~5-15 indications. Per Tier-2 of the
   maintainer priority rule (volume proxy until UA epidemiology lands).
3. **Other diseases** in alphabetical order until ≥90% threshold met.
4. **`null` outcome fields** — leave null when the indication's reference
   doesn't report that outcome (e.g., adjuvant trials have DFS-HR but
   not ORR). Add a one-line note explaining why.

Per-chunk size: ≤10 indications per chunk to keep review manageable.

### Phase 4 — render (1 chunk)

- Update render layer to surface `OutcomeValue.source` as a clickable
  citation reference next to each shown outcome value.
- Add a "Trial-readout traceability" badge to indication cards in the
  rendered plan when ≥80% of populated outcomes are cited.

## Per-item workflow

For each indication being remediated:

1. Fetch the pivotal-trial PubMed entry via `pubmed_client` or PubMed
   MCP (whichever the harness has wired up).
2. Read the abstract + Results section (full text via NCT primary
   results posting if abstract is sparse).
3. Transcribe (don't synthesize) ORR / CR / mPFS / mOS / DFS-HR exactly
   as the publication states them, with units. If a value is reported
   only with median follow-up X mo, capture both.
4. If the trial has named arms (e.g., 1L pembrolizumab vs ipilimumab in
   KEYNOTE-006), populate the indication's outcomes from the
   corresponding arm only.
5. Create or reuse an `SRC-*` entity for the publication. Citation
   should include PMID, DOI, journal, year, first-author surname.
6. Set `OutcomeValue.source` to the SRC-* ID.
7. Add 1-line `notes` if the value differs from frequently-quoted
   numbers (e.g., updated readout supersedes original).

Forbidden:

- Synthesizing or interpolating outcome values not stated in the
  primary source.
- Picking which arm's outcomes apply (clinical-co-lead decision) when
  the indication's `applicable_to` block doesn't unambiguously map to
  a single arm.
- Filling missing CIs from "typical" ranges.
- Translating outcome strings — keep them in the trial's reporting
  language (English) for traceability; UA goes in `notes_patient` /
  display layer.

## Quality gates

Per `kb_data_quality_plan_2026-04-29.md` and the Quality Gate rule from
strategy doc v0.2:

- Each chunk must declare which of the 306 indications it owns.
- Each chunk must declare its citation evidence standard.
- Each chunk must surface an audit command (re-run the Phase-1 audit
  against the chunk's IDs and confirm the cited count went up).
- Unresolved items (outcomes the publication doesn't report) are
  acceptable when explicit (`null` + note); silent gaps are not.
- CHARTER §6.1 two-reviewer signoff applies (currently dev-mode-exempt
  per memory note); each chunk should still record one reviewer in
  `Indication.reviewer_signoffs` with rationale tied to the citations
  added.

## Acceptance criteria — v1.0

| Metric | Current | v1.0 target |
|---|---:|---:|
| Indications with `expected_outcomes` populated (≥1 field) | 100% | 100% |
| Indications with all populated outcomes citation-traceable | not measured | ≥90% |
| Indications carrying ≥2 distinct sources for outcomes | not measured | ≥60% |
| Schema migration to `OutcomeValue` complete | 0% | 100% |
| Matrix shows `Outcomes-Cited %` column per disease | no | yes |

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Scope creep to "fix all weakly-cited fields project-wide" | Phase 1 audit produces the queue; Phase 3 takes only that queue. Don't touch fields the audit didn't flag. |
| Clinical interpretation drift (LLM picks the "wrong" arm or extrapolates) | Per-item workflow forbids synthesis; add a reviewer signoff per chunk; the audit re-runs to confirm. |
| Cloudflare 403 mid-execution (recurred twice this session) | Each chunk's commits should be local-first, then push. Recovery: manual push of locally-committed work. |
| Parallel session conflict (other sessions land trial sources or indication edits) | Use `--no-ff` chunk merges; rebase before push; keep chunk size ≤10 indications so windows are short. |
| `OutcomeValue` migration leaks legacy strings into Phase-3 work | Migration validator marks legacy entries with `SRC-LEGACY-UNCITED` so they're visible in the audit; Phase 3 cannot complete a chunk while any of its indications still carry that placeholder. |
| Pivotal-trial publication paywalled / not in PubMed | Tier-2 fallback: cite NCT primary results + FDA label co-citation. Document in chunk notes. |

## Sequencing — proposed timeline

- Week 1 (2026-05-01..2026-05-07): Phase 1 audit + Phase 2 schema migration (single PR each).
- Week 2-3: Phase 3 first 4 chunks (the 8 shelf-task items split across 2-3 chunks; first NSCLC + breast chunks).
- Week 4+: continue Phase 3 by disease-volume priority until ≥90% target. Estimated ~25-30 chunks total.
- Phase 4 renders once Phase 3 hits ~70% — surfaces partial progress without waiting for completion.

## Out of scope

- **Toxicity profile completeness per regimen** — separate v0.3 metric in the
  strategy doc; uses CTCAE v5 grading, not RCT outcome reporting.
- **Trial-readout monitoring automation** — the strategy doc's "Trial pivotal-readout monitoring | monthly | ❌ no automation" Living-data target. Different effort: continuous, agent-driven, depends on a poller that this plan does not include. Listed as Queue-C "Examples next" in the strategy doc.
- **Drug target metadata structured fields** (target gene + UniProt ID) —
  separate Queue-C effort if we decide to capture this; not blocking
  outcomes ingestion.
- **Translation of outcome strings to UA** — render-time concern, not
  authoring concern.

## Open questions

1. **Schema migration timing.** Phase 2 (OutcomeValue) is a breaking
   change at the validation layer. Should Phase 1 audit complete first
   to know the size of the legacy backlog before committing to the
   migration approach?
2. **PubMed MCP vs in-house client.** The bio-research plugin's PubMed
   MCP is a candidate but adds an external dependency. The in-house
   `pubmed_client.py` is already integrated. Pick one and document.
3. **Trial-arm disambiguation.** Some indications conceptually map to
   one trial arm; others to a comparison. Worth a Queue-C schema
   addition (`Indication.applies_to_trial_arm: Optional[str]`) before
   Phase 3?
4. **`SRC-LEGACY-UNCITED` placeholder lifetime.** How long do we let
   legacy-marked entries linger before the matrix turns it red?
   Suggestion: 90 days after Phase 2 lands.
