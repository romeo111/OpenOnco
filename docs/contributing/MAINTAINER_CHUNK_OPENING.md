# Maintainer Checklist: Opening a Chunk-Task Issue

Before opening a `[Chunk]` issue with `status-active` label (which makes the chunk claimable by contributors), walk this checklist. Skipping steps risks parallel-work duplication, manifest collisions, or contributor confusion.

## 1. Is the chunk-spec ready?

Open `chunks/openonco/<chunk-id>.md` in `task_torrent` repo. Confirm:

- [ ] Status is `queued` (not `completed`/`active`)
- [ ] Economic Profile filled with `break_even_test: PASS` or `MARGINAL` — **never open `FAIL` chunks**
- [ ] `claim_method` declared (`formal-issue` or `trusted-agent-wip-branch-first`)
- [ ] Manifest is concrete (real entity IDs / file ranges, not placeholder)
- [ ] Re-verification spec is real (sample %, expert role, trust threshold)

If anything is missing, fix the chunk-spec first.

## 2. Cross-chunk manifest overlap check

If the chunk's manifest overlaps with another currently-active chunk's manifest, two contributors may collide on the same entity. Run:

```bash
# Save the new chunk's manifest to a temp file
cat > /tmp/new_manifest.txt <<EOF
<paste the manifest IDs, one per line>
EOF

# Run overlap check against existing active chunks
python -m scripts.tasktorrent.check_manifest_overlap <new-chunk-id> /tmp/new_manifest.txt
```

Expected output:

```
No overlap. Safe to open the new chunk-task issue.
```

If overlap detected:

```
OVERLAP with contributions/<other-chunk-id>/ (N entities):
  - <BMA-ID-1>
  - <BMA-ID-2>
  ...
Overlap detected. Resolve before opening the new chunk-task issue.
```

**Resolution options:**

- Wait for the conflicting chunk to close, then re-check.
- Re-scope the new chunk's manifest to avoid the overlap.
- If both must run in parallel, coordinate so they touch DIFFERENT fields of the same entity (e.g. one chunk modifies `evidence_sources`, another modifies `notes`) — and document that in both chunk-specs.

## 3. Open the issue

```bash
gh issue create --label "chunk-task,status-active,<topic-labels>" \
  --title "[Chunk] <chunk-id> — <one-line scope>" \
  --body-file path/to/issue-body.md
```

Issue body template at `.github/ISSUE_TEMPLATE/tasktorrent-chunk-task.md` — fill out every section. The chunk's full spec is at `task_torrent/chunks/openonco/<chunk-id>.md`; link to it from the issue.

## 4. After opening

- For `formal-issue` chunks: wait for first claim comment. Assign within 24h or the bot auto-releases.
- For `trusted-agent-wip-branch-first` chunks: notify the pre-authorized agent via DM/secondary channel. They'll push a WIP branch immediately when starting.
- Add to active-chunks dashboard / shelf listing if you maintain one.

## 5. Active-cap check

Active-cap is currently 10 (per `task_torrent/docs/openonco-pilot-workflow.md`). Before opening, check current active count:

```bash
gh issue list --label "chunk-task,status-active" --state open | wc -l
```

If at cap, hold the open until a slot frees.

## When chunks close

When a chunk's PR merges (sidecars in `contributions/`):

1. Close the chunk-task issue with a comment linking to the merged PR
2. Update chunk-spec status to `completed` (back in task_torrent)
3. Active-cap decrements; new chunk can be promoted

When chunk's content gets applied to hosted/content (Co-Lead signoff happens):

4. Run `application_status: applied` tracking (see PR #15 / improvement plan §9)

## Notes for the bot maintainer

The two bots in `.github/workflows/tasktorrent-claim-bots.yml`:

- **claim-sla-bot** (hourly): auto-releases formal-issue claims unassigned > 24h
- **stale-claim-bot** (daily): auto-releases assignees with no branch activity > 14 days

Both have `workflow_dispatch` for manual trigger with `dry_run: true` to test without side effects.
