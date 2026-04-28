# TaskTorrent PR #21/#22/#23 execution log (2026-04-28)

Start time: 2026-04-28 15:57:16 +03:00.

Synced baseline: `origin/master @ 5859cf4c` (`Merge pull request #22 from romeo111/chore/post-pilot-verify-and-apply`).

## Scope limits

- Work only in the clean `OpenOnco_master_sync` worktree.
- Do not modify the older dirty `OpenOnco_work` worktree.
- Do not promote new claim-bearing clinical content without CHARTER section 6.1 review/signoff.
- PR #21, #22, and #23 are already merged; this pass executes mechanical validation, re-verification, and maintainer-facing triage follow-ups.

## PR status at start

- PR #21: merged. Remaining chunks landed as sidecars; claim-bearing application remains gated by Co-Lead review.
- PR #22: merged. `civic-bma-reconstruct-all` was applied to hosted BMA content after deterministic re-verify.
- PR #23: merged. `citation-semantic-verify-v2` report landed; follow-up work is triage and source-replacement/action queues.

## Execution results

### Sync

- Synced `romeo111/OpenOnco` to `origin/master @ 5859cf4c`.
- Created a clean worktree at `C:\Users\805\task_torrent\OpenOnco_master_sync`.
- Created execution branch `codex/execute-pr21-23`.
- Left the older `OpenOnco_work` worktree untouched because it had unrelated local modifications.

### Validation

- `git fetch origin --prune`: PASS; branch baseline still matches `origin/master @ 5859cf4c`.
- `python -m scripts.tasktorrent.validate_contributions --all`: PASS for all 8 chunks.
- `python -m knowledge_base.validation.loader knowledge_base/hosted/content`: PASS; loaded 2414 hosted entities and resolved references.
- Loader warnings remain: 36 contract warnings, mostly draft redflags requiring clinical review plus three one-source warnings.
- `python -m scripts.tasktorrent.reverify_bma_civic`: PASS; 399/399 BMA sidecars match the CIViC snapshot.
- `python -m scripts.tasktorrent.reverify_citation_replace_source citation-semantic-verify-v2`: PASS; 121 replace-source rows, 0 missing target sources, 0 trial/title mismatches.

### PR #21 follow-up state

- `bma-drafting-gap-diseases`: 23 sidecars, all `review_existing_hosted_draft`, all `pending_clinical_signoff`; 5 blocker items remain.
- `redflag-indication-coverage-fill`: 33 sidecars, all `review_existing_hosted_draft`, all `pending_clinical_signoff`; 10 blocker items remain.
- `source-stub-ingest-batch`: 40 source sidecars, all `review_existing_stub`; 12 are `pending_clinical_signoff`, 28 have no explicit review status.
- Six source-stub contribution sidecars still contain `TODO: confirm citation`: `SRC-ASCO-BTC-2023`, `SRC-ATA-ATC-2021`, `SRC-ATA-THYROID-2015`, `SRC-EANO-LGG-2024`, `SRC-ESMO-BTC-2023`, and `SRC-ESMO-HNSCC-2020`.
- Hosted sources still contain multiple `TODO: confirm citation` titles. These are source-quality blockers, not mechanical-validation failures.

### PR #22 follow-up state

- CIViC BMA reverify remains clean after sync: 399 sidecars rechecked against the 2026-04-25 CIViC snapshot.
- No BMA content changes were needed in this pass.

### PR #23 follow-up state

- Regenerated maintainer triage queues without row limits by status:
  - `contributions/citation-semantic-verify-v2/triage-queue-status-supported.md`: 121 supported rows, all replace-source candidates.
  - `contributions/citation-semantic-verify-v2/triage-queue-status-unsupported.md`: 247 unsupported rows, all maintainer-review candidates.
- Generated full maintainer triage queues by action:
  - `contributions/citation-semantic-verify-v2/triage-queue-action-replace_source.md`: 121 rows.
  - `contributions/citation-semantic-verify-v2/triage-queue-action-maintainer_review.md`: 345 rows.
  - `contributions/citation-semantic-verify-v2/triage-queue-action-revise_claim.md`: 124 rows.
  - `contributions/citation-semantic-verify-v2/triage-queue-action-source_stub_needed.md`: 324 rows.
- Re-ran trial extraction:
  - `source_stub_needed` rows: 324.
  - Unique extracted trials: 47.
  - Rows without extractable trial: 153.
  - Existing report path: `contributions/citation-semantic-verify-v2/trials-needing-source-ingest.md`.

## Remaining guarded work

- Merge-ready technical state: validation, KB loading, CIViC reverify, and citation replace-source reverify are green.
- Governance state: remaining blockers are not schema/test failures; they are clinical/source-review queues that must remain explicit for reviewer action.
- Do not bulk-apply the 121 replace-source candidates without maintainer acceptance; one example (`VISION`) can resolve to the wrong oncology trial name across domains.
- Do not promote #21 claim-bearing BMA/redflag/indication drafts until PR-level review or clinical signoff resolves the explicit blocker reports.
- Source-stub TODOs should be resolved by checking primary source pages/metadata and licensing notes before editing hosted source titles or citation identifiers.
