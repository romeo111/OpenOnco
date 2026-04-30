# KB Data Quality Plan - 2026-04-29

**Status:** active planning track.
**Scope:** hosted KB content, TaskTorrent chunks, clinical-plan rendering, and
public-facing evidence transparency.
**Related docs:** `docs/kb-coverage-strategy.md`,
`docs/kb-coverage-matrix.md`, `docs/plans/civic_integration_v1.md`,
`docs/plans/source_freshness_audit_2026-04-27.md`,
`docs/clinical_signoff_workflow.md`.

## Why this exists

Coverage alone is not enough. A plan can have many records and still be unsafe
or weak if the claims are stale, poorly sourced, over-tiered, not reviewed, or
unclear in the Ukrainian care context. For OpenOnco, data quality means every
claim can be traced, refreshed, reviewed, and explained.

This plan turns "improve quality" into concrete gates that every future
TaskTorrent chunk and roadmap item should follow.

## Quality Definition

Each clinical or operational KB item should satisfy five checks:

| Dimension | Required standard | Failure mode we avoid |
|---|---|---|
| Provenance | Every clinical claim has source IDs and PMID/DOI/URL where available. | Unsourced recommendation text. |
| Recency | `current_as_of`, `last_verified`, or `last_reviewed` is present and inside the SLA for the entity type. | Old guideline claims looking current. |
| License and reuse | Source license/terms are declared or unresolved explicitly. | Using content we cannot redistribute. |
| Clinical strength | ESCAT/CIViC/evidence level is verified against the cited source, not copied forward blindly. | Overclaiming actionability. |
| UA applicability | Ukrainian registration, NSZU/reimbursement, language, and clinician signoff state are explicit. | Technically correct but unusable locally. |

Unresolved is acceptable when documented. Silent gaps are not.

## Planning Rule

Every new plan or chunk that touches KB data must state:

1. The baseline quality gap it addresses.
2. The exact manifest IDs it owns.
3. The quality field expected to move.
4. The evidence standard for accepting a sidecar.
5. The validator or audit command that proves the work did not regress.

Recommended chunk wording:

```markdown
## Mission
This chunk advances `kb-coverage-matrix.md > Quality gaps > <axis>` from
<baseline> toward <target> for the manifest IDs below.

## Quality Gate
- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly.
- `py -3.12 -m scripts.tasktorrent.validate_contributions <chunk-id>` passes.
```

## Priority Workstreams

### Q1. BMA Evidence Integrity

Goal: make biomarker actionability records traceable and conservative.

Open tasks:
- Backfill missing CIViC links where the snapshot supports the claim.
- Record explicit `no_civic_match_reason` where CIViC has no suitable item.
- Full ESCAT tier audit: detect overclaim, underclaim, and unmapped resistance.
- Add anti-evidence handling for CIViC "Does Not Support" items.

Acceptance:
- BMA records either cite CIViC/ESCAT/source evidence or carry a documented
  unresolved reason.
- ESCAT tier changes require reviewer-readable rationale.

### Q2. Source Metadata Integrity

Goal: make every source reusable, current, and auditable.

Open tasks:
- Backfill missing license/terms metadata.
- Refresh stale `current_as_of` values.
- Replace broken publisher URLs with DOI, PubMed, or verified canonical URLs.
- Mark superseded guidelines with `superseded_by` instead of deleting history.

Acceptance:
- 100% of sources have license/terms status declared.
- Source freshness reports distinguish "verified URL" from "current clinical
  content"; a fresh URL does not mean a fresh guideline.

### Q3. UA Access and Signoff

Goal: make recommendations useful in the Ukrainian care setting.

Open tasks:
- Verify drug registration and NSZU/reimbursement fields.
- Prepare BMA and recommendation wording for Ukrainian clinical signoff.
- Track patient-language readiness separately from clinician-language readiness.

Acceptance:
- UA access fields cite public registry, NSZU, DEC, or hosted source records.
- No patient-facing wording is considered production-ready without signoff state.

### Q4. Citation and Wording Remediation

Goal: remove stale, vague, or overconfident recommendation text.

Open tasks:
- Process citation-verify-v2 findings.
- Remediate critical recommendation-wording findings first.
- Add claim-level source anchors where `expected_outcomes` or line-of-therapy
  text is currently detached from a specific trial/guideline source.

Acceptance:
- Claim-bearing text either maps to a source row or is downgraded to a
  maintainer-review note.
- Remediation chunks preserve clinical meaning and show before/after rationale.

### Q5. Regression Prevention

Goal: prevent quality debt from reappearing after cleanup.

Open tasks:
- Extend `scripts.kb_coverage_matrix` with quality dimensions that are currently
  only described in prose: citation density, outcome coverage, source age, and
  signoff readiness.
- Add CI warnings for newly introduced unsourced claim text.
- Make TaskTorrent chunk specs require a `Quality Gate` section.

Acceptance:
- The matrix shows quality movement over time.
- New chunks cannot be accepted when they improve coverage while degrading
  provenance, license, recency, or signoff status.

## Active Chunk Mapping

The 100 TaskTorrent chunks opened on 2026-04-29 are the first quality-focused
batch for this plan:

| Issue range | Chunk family | Quality dimension |
|---|---|---|
| #43-#63 | `bma-civic-backfill-*` | BMA evidence integrity |
| #64-#83 | `bma-ua-signoff-prep-*` | UA signoff readiness |
| #84-#91 | `source-license-backfill-*` | License and reuse |
| #92-#121 | `source-recency-refresh-*` | Source recency |
| #122-#141 | `drug-ua-nszu-access-audit-*` | UA access |
| #142 | `zero-bma-disease-actionability-scout-*` | Coverage planning with explicit uncertainty |

Future chunk batches should keep this pattern: small manifests, explicit quality
axis, and sidecar-only outputs.

## Metrics To Track

Add or keep visible in `docs/kb-coverage-matrix.md`:

| Metric | Target |
|---|---|
| BMA with source-backed evidence block | 100% |
| BMA with CIViC match or no-match reason | 100% |
| BMA ESCAT verified | >=85% for v1.0, then 100% |
| Sources with license/terms status | 100% |
| Sources with current `current_as_of` / `last_verified` | >=60% for v1.0 |
| Drugs with UA registration status | >=90% |
| Drugs with NSZU/reimbursement status or unresolved reason | >=90% |
| Claim-bearing recommendation text with citation anchor | >=90% |
| Patient-facing UA text with signoff state | 100% |

## Non-Goals

- Do not auto-merge clinical content based only on audits.
- Do not treat CIViC as an autonomous treatment-selection engine.
- Do not hide uncertainty by filling guessed values.
- Do not edit hosted KB files directly in contributor chunks.

## Maintainer Checklist

Before opening a new data chunk:

- Check `docs/kb-coverage-matrix.md` for the exact quality gap.
- Prefer quality remediation over adding another broad coverage batch when the
  same disease/entity already has unverified records.
- Keep manifests small enough that one reviewer can verify them.
- Require structured unresolved reasons.
- Re-run the matrix after accepted sidecars are applied.

