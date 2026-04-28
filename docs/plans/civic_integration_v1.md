# CIViC integration plan v1 — 2026-04-27

Replaces `docs/plans/oncokb_integration_safe_rollout_v3.md` after the
OncoKB ToS audit (`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`).

## Why CIViC

- **License:** CC0-1.0 — explicitly redistributable, no patient-services
  carve-out, no AI-training prohibition. Compatible with CHARTER §2 (free
  public resource) without a license waiver.
- **Scale:** ~4,842 accepted evidence items / 1,933 distinct (gene, variant)
  pairs / 551 distinct gene symbols in the 2026-04-25 snapshot.
- **Refresh cadence:** CIViC publishes nightly; we pull a monthly snapshot
  via CI (`.github/workflows/civic-monthly-refresh.yml`).
- **Coverage of OpenOnco's variant-keyed actionability:** **27 of 29**
  BIO-* with `actionability_lookup` are variant-level confirmable in CIViC
  (per the audit). The 2 gaps (EZH2 Y641N, RHOA G17V) are tractable via
  direct guideline citation.
- **Fusion-aware encoding:** CIViC encodes fusions as `BCR::ABL1`,
  `EML4::ALK`, etc., with resistance mutations on a fusion background
  encoded inside the variant string (e.g. `Fusion AND ABL1 T315I`).
  Our matcher handles this natively.
- **Resistance preserved:** CIViC's `direction == "Does Not Support"` and
  `significance == "Resistance"` are surfaced verbatim — no flattening
  required.

## What's landed (as of 2026-04-27)

### Phase 0: coverage audit
- Output: `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`
- Drove the OncoKB → CIViC pivot decision.
- Cherry-pick of the audit commit onto `feat/civic-primary` is pending
  (Phase 5).

### Phase 1: engine rename + schema generalization
- Commit `5384348 feat(engine): rename oncokb_* → actionability_* + drop services/oncokb_proxy (CIViC pivot)`
- Module files: `actionability_{types,client,extract,conflict}.py` under
  `knowledge_base/engine/`.
- BMA schema: `evidence_sources: list[EvidenceSourceRef]` replaces the
  legacy `oncokb_level + oncokb_snapshot_version` pair.
- `services/oncokb_proxy/` removed — no proxy needed for CIViC (snapshot
  is hosted as CC0).

### Phase 1.5: YAML migration
- Commit `c72e45b feat(kb): migrate oncokb_lookup → actionability_lookup, oncokb_level → evidence_sources`
- 29 BIO-* files: `oncokb_lookup` → `actionability_lookup`.
- 399 BMA files: legacy `oncokb_level` entries migrated into the
  `evidence_sources` block as `SRC-ONCOKB` metadata (kept for audit
  trail; render layer must not surface them).
- `actionability_review_required: true` set on all migrated BMAs pending
  CIViC reconstruction or two-reviewer signoff.
- Migration script: `scripts/migrate_oncokb_yaml_fields.py` (idempotent).

### Phase 2: CIViC integration
- Commit `1d16841 feat(engine): civic_variant_matcher` — fusion-aware
  (gene, variant) matcher (BCR::ABL1+T315I, EML4-ALK+resistance, etc.).
- Commit `de19dee feat(engine): SnapshotCIViCClient` — CIViC YAML reader,
  levels A–D surfaced (E filtered as "inferential" per audit §6.1),
  resistance preserved via `direction == "Does Not Support"` + significance.
- Commit `0b53a5c feat(ci): monthly CIViC snapshot refresh + diff CI` —
  `.github/workflows/civic-monthly-refresh.yml`,
  `scripts/refresh_civic.py`, `scripts/diff_civic_snapshots.py`.

### Phase 3: BMA evidence reconstruction + J-draft audit
- Commit `e31ebd1 feat(kb): Phase 3-N — BMA evidence reconstruction via CIViC`
  — 37 BMAs with CIViC entries; 27 carry resistance evidence.
- Commit `94cd7be docs(reviews): Phase 3-O — J-drafts vs CIViC side-by-side diff`
  — 5 of 23 J-drafts CIViC-confirmable; 18 need NCCN/ESMO re-attribution.

## What's pending

### Phase 3.5: matcher case-fix
- Phase 3-O surfaced a `civic_variant_matcher.py:171` case-sensitivity
  bug (NPM1 `W288fs` vs CIViC `W288FS`). 1-line fix.

### Phase 4: render + spec + docs (in parallel, including this doc)
- **4-P:** render layer pivot — ESCAT primary + CIViC detail; SRC-ONCOKB
  skip per ToS; fallback for empty `evidence_sources`.
- **4-Q:** `specs/KNOWLEDGE_SCHEMA_SPECIFICATION` + `specs/SOURCE_INGESTION_SPEC`
  updates (owned by Q in parallel).
- **4-R:** this doc + supersede notice on legacy plan.

### Phase 5: verification
- Full test suite green (`pytest tests/`).
- Validator clean (`python -m knowledge_base.validation`).
- Render sample-grep `OncoKB` → 0 hits in HCP-mode rendered output.
- Cherry-pick audit `b4aba91` from origin onto `feat/civic-primary`.

## Architectural carry-over from OncoKB plan

Even though OncoKB itself is rejected, design decisions from the original
`oncokb_integration_safe_rollout_v3` plan that carry over and remain valid:

- **Engine firewall** — actionability code is separated from
  track-builder; enforced by import-graph test. The same firewall applies
  to CIViC (`_build_tracks` is pure, no actionability args).
- **Fail-open contract** — lookup errors return `ActionabilityError`,
  never raise. Plan generation must not depend on CIViC availability.
- **Render-side filtering** — surfacing rules belong in the render layer,
  not in the engine. Levels-1/2 filtering, R1/R2 styling, "Show N more"
  collapse all stay render-layer concerns.
- **HCP-only surface** — patient-mode has zero actionability content.
  Snapshot test + regex grep CI step protect this.
- **Resistance flagging** — preserved via CIViC `direction == "Does Not
  Support"`; surfaced as red `🛑` (analogous to OncoKB R1) or amber `⚠`
  (analogous to R2) per CIViC level.

## Architectural deltas vs OncoKB plan

- **No proxy.** CIViC is hosted as a CC0 snapshot under
  `knowledge_base/hosted/civic/<date>/`; no academic-token network call,
  no server-side proxy, no quota-exhaustion threat (T9), no token-leak
  threat (T1, T10).
- **No level mapping.** CIViC's A/B/C/D/E are rendered verbatim. We do
  **not** try to map to OncoKB's 1/2/3A/3B/4 — different curation
  methodology, and the audit §6.1 mapping was explicitly proposed as
  conservative-and-asymmetric. Render layer surfaces CIViC level + ESCAT
  tier separately; clinicians read both.
- **Multi-source by default.** `evidence_sources` is a list; future agents
  can add `SRC-NCCN-*`, `SRC-ESMO-*`, etc. entries with their own
  level/significance shape per source. The schema is no longer
  OncoKB-shaped.
- **Anti-evidence channel.** CIViC has 513 "Does Not Support" items
  (10.6% of evidence). The render layer surfaces these as a negative
  recommendation card rather than dropping them — OncoKB had no
  equivalent and the original plan's data model didn't accommodate this.

## Open questions

1. **CIViC-A → ESCAT promotion gate.** Without an FDA-CDx whitelist,
   every CIViC-A item maps to ESCAT II by default (audit §6.1, Q3).
   Should we author a manual FDA-CDx promotion list (~20 variants) to
   enable ESCAT IA surfacing? One-time effort; revisit per FDA list updates.
2. **JAK2 V617F level disagreement.** Three BMAs claimed OncoKB Level 1;
   oncokb-datahub gene-level was 2; CIViC has 6 V617F items at levels
   B/D. Now that the OncoKB level is removed, the BMAs need a clinical
   co-lead decision on the canonical level for ruxolitinib in PV / ET /
   PMF. (NCCN-recommended but JAK2 V617F is not the FDA companion
   diagnostic.)
3. **EZH2 Y641N gap.** CIViC 2026-04-25 snapshot has 29 EZH2 evidence
   items but none on Y641N specifically. Refresh cycle (Phase 5)
   should re-pull; if still empty, cite tazemetostat label + Morschhauser
   2020 directly in the BMA.
