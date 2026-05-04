# Q-axis (W12a/W12b) agent-dispatch prompt template

Date authored: 2026-05-01
Author: orchestrator session `musing-murdock-c08478` (post-batch-5a retrospective)

## Context

Batch 5a of W12a/W12b dispatched 12 agents with prompts that conflicted with the
canonical chunk-spec encoded in each issue body. 11/12 agents self-corrected by
following the issue body and consulting advisor; 2 stalled mid-task and needed
manual recovery; some hit branch-name drift (`chunk/...` vs `tasktorrent/...`).

The template below is what the orchestrator-level prompt SHOULD look like for
W12a/W12b agents — aligned with the issue body so the agent doesn't have to
reconcile two sources of truth.

## Authoritative differences vs W7-W11 dispatch pattern

| Dimension | W7-W11 (Tier-2 KB authoring) | W12a/W12b (Q-axis quality) |
|---|---|---|
| Output mode | Direct edits to `knowledge_base/hosted/content/...` | Sidecar files under `contributions/<chunk-id>/` only |
| Branch prefix | `chunk/...` | `tasktorrent/...` |
| Quality gate | `validate_kb` + `pytest tests/test_curated_chunk_e2e.py` (82 passed) | `scripts.tasktorrent.validate_contributions <chunk-id>` only |
| Manifest size | Variable, read from issue | Variable (4-5 IDs typical), read from issue |
| Hosted KB rejection | n/a (you ARE editing hosted) | Editing hosted = REJECT per issue's "Rejection Criteria" |

## Template (parameterize {ISSUE_NUM} and {CHUNK_TYPE} per agent)

```
Execute GitHub issue #{ISSUE_NUM}.

You are one of N parallel Q-axis agents. Repo: OpenOnco. READ CLAUDE.md in your worktree before any write.

CRITICAL — WORKTREE ISOLATION:
- Work ONLY in your assigned isolated worktree.
- NEVER `cd C:\Users\805\cancer-autoresearch` or `cd /c/Users/805/cancer-autoresearch` — that is the user's main tree (incident #241).
- All git ops happen in your worktree path.

Pre-flight (mandatory before any write):
1. `pwd` — confirm path is under `.claude/worktrees/agent-*/`, NOT the main tree
2. `git rev-parse --abbrev-ref HEAD` and `git status --short` — record + confirm clean

CANONICAL CHUNK SPEC: the issue body is authoritative. If anything in this
prompt conflicts with the issue body, follow the issue body.

Steps:
1. `gh issue view {ISSUE_NUM} --json title,body -q '.body'` — extract ALL manifest IDs (do NOT assume count; some chunks have 4, some 5).
2. Sidecar contract (issue's Quality Gate):
   - Output ONLY under `contributions/<chunk-id>/`
   - Branch prefix: `tasktorrent/<chunk-id>`
   - Hosted KB edits = REJECT per issue's Rejection Criteria
3. For each manifest ID, follow the per-chunk-type guidance below.
4. Required sidecar files (mirrors wave-1 reference pattern):
   - `_contribution_meta.yaml`
   - `task_manifest.txt`
   - `audit-report.yaml` (BMA chunks) OR `source_recency_audit.yaml` (source chunks)
   - `refresh_summary.yaml` (source chunks only)
   - `unreachable.yaml` (source chunks, when applicable)
   - per-entity upsert YAMLs for matched/verifiable items
5. Quality gate: `C:/Python312/python.exe -m scripts.tasktorrent.validate_contributions <chunk-id>` → must PASS.
6. Diff scope: `git diff --name-only origin/master..HEAD` — all paths must be under `contributions/<chunk-id>/`. No hosted KB files.
7. Commit with explicit pathspecs (NEVER `git add -A`/`.` — banned per CLAUDE.md). Push origin. Comment on issue with branch+SHA+per-entity result.

Self-push authorized (CLAUDE.md commit `3a60901b`) on feature branch with green gates.

For W12a (BMA-CIViC backfill):
- Reference pattern: closed issue #43 (`bma-civic-backfill-2026-04-29-001/-009`).
- For each BMA: lookup CIViC snapshot at `knowledge_base/hosted/civic/<latest>/`, match by gene + variant + disease (use disease synonym expansion if needed).
- Variant-aware filter: exclude evidence items whose variant inverts the BMA's clinical message (e.g. for PDGFRA-EXON12 BMA, exclude exon-18 D842/I843 imatinib-resistant items).
- Match → write upsert sidecar with `evidence_sources.civic_*` block (level/direction/statement/citation_id), preserve `actionability_review_required: true` for maintainer adjudication.
- No match → audit-only row in `audit-report.yaml` with structured reason (`gene_not_in_civic` / `gene_in_civic_no_disease_overlap` / `gene_disease_match_but_alteration_mismatch` / etc).

For W12b (source-recency-refresh):
- Reference pattern: closed issues #92-#121 (`source-recency-refresh-2026-04-29-*`).
- For each Source: httpx GET `url` (30s timeout, 3 retries, follow redirects, **`User-Agent: Mozilla/5.0 (compatible; OpenOnco-recency-bot)` header to reduce bot-walls**).
- 200 → upsert with `last_verified: 2026-05-01`, bump `current_as_of` if older than 2026-04-01.
- 301/302 to different URL → upsert with new `url` + `url_redirected_from`.
- 404/410 → unreachable.yaml entry with `url_status: dead`, `url_replacement_needed: true`.
- 403 (publisher bot-wall) → unreachable.yaml entry with `url_status: blocked_by_bot_protection`. **Do NOT bump `current_as_of`** unless content is independently verified (PMID/DOI lookup). Suggest DOI canonical URL replacement in audit notes.
- No URL field on stub → unreachable.yaml entry, suggest PMID/DOI in notes.

Stop conditions per CLAUDE.md (abort + report):
- Edits would touch files outside `contributions/<chunk-id>/`
- HEAD on different branch than expected
- Working tree mutated unexpectedly
- Validator regresses (new errors)

Report back: branch + SHA + push URL + comment URL + per-entity outcome table.
```

## Known issues fixed in this template

1. **Branch name drift**: prompt now matches issue's `tasktorrent/...` convention (was `chunk/...`).
2. **Hosted KB rejection**: prompt explicitly states sidecar-only (was "edit hosted YAML").
3. **Wrong gate**: prompt now uses `validate_contributions` (was `validate_kb` + pytest).
4. **Manifest count**: prompt no longer hardcodes "4 IDs" — agents read from issue.
5. **Pytest baseline drift**: prompt no longer cites "82 passed" (full suite has 6 pre-existing failures unrelated).
6. **Synchronous gate execution**: agents in batch 5a stalled when they spawned background pytest — prompt now implies synchronous execution. (Two agents `#186`/`#204` returned mid-stream "Now let me wait for pytest" / "Background tasks just started. Let me wait for the notification." and never resumed.)
7. **403 bot-wall handling**: prompt prescribes `User-Agent` header AND advises NOT to bump `current_as_of` for blocked items unless independently verified.

## Open template gaps (not yet addressed)

- **Wave-1 sidecar redundancy detection**: agents should grep for existing
  `contributions/bma-civic-backfill-2026-04-29-*/<bma-id>.yaml` and skip
  redundant work or explicitly supersede with rationale. Current template
  doesn't surface this.
- **Per-source DOI canonical fallback**: when 403 hits a publisher URL, the
  template should suggest the agent attempts `https://doi.org/<doi>` resolution
  before classifying as `blocked_by_bot_protection`. Several batch-5a agents
  flagged this manually but didn't try the fallback.
