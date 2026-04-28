---
name: TaskTorrent Chunk Task
about: Active executable chunk for distributed AI-assisted contribution
title: "[Chunk] "
labels: ["chunk-task", "status-active"]
assignees: ""
---

## Chunk Spec

<!-- Link to chunks/<project>/<chunk-id>.md in romeo111/task_torrent -->

## Chunk ID


## Topic Labels

<!-- e.g. civic-evidence, mechanical+judgment -->

## Drop Estimate


## Required Skill


## Branch Naming Convention

`tasktorrent/<chunk-id>`

## Claim Method

<!-- Pick one (must match chunk-spec):
     - formal-issue → contributor comments to claim, maintainer assigns within 24h SLA
     - trusted-agent-wip-branch-first → pre-authorized agent pushes empty WIP commit immediately
-->

claim_method:

## How to claim

For `formal-issue`:
- Comment: `I'd like to take this chunk.`
- Maintainer assigns within 24h. If not assigned, auto-released by bot.
- One contributor per chunk.

For `trusted-agent-wip-branch-first`:
- Push empty WIP commit to `tasktorrent/<chunk-id>` on origin IMMEDIATELY when starting.
- That branch on origin is the visible lock — other agents see it and don't duplicate.

**Stale-claim auto-release:** if no branch activity for 14 days, bot drops assignee + relabels `status-active`.

## Sidecar Output Path

```
contributions/<chunk-id>/
```

## Task Manifest

<!-- Explicit list of stable entity IDs this chunk owns. Contributor must
     ALSO commit this manifest as contributions/<chunk-id>/task_manifest.txt. -->

```
<entity_id_1>
<entity_id_2>
...
```

## Allowed Sources


## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA` (always banned for OpenOnco pilot per CHARTER §2).

## Input Context

- Chunk spec (full): see link above
- Skill spec: `https://github.com/romeo111/task_torrent/blob/main/skills/<skill>.md`
- Pilot workflow: `https://github.com/romeo111/task_torrent/blob/main/docs/openonco-pilot-workflow.md`
- Contributor quickstart: [`docs/contributing/CONTRIBUTOR_QUICKSTART.md`](../blob/master/docs/contributing/CONTRIBUTOR_QUICKSTART.md)
- Per-chunk agent prompt: `docs/contributing/AGENT_PROMPT_<chunk-id>.md`
- Reference output: `contributions/<chunk-id>/` working PoC (where applicable)
- Schema: `knowledge_base/schemas/<entity>.py`

## AI tool + model metadata (required on every sidecar)

Each sidecar's `_contribution` wrapper must include `ai_tool` and `ai_model`. Captured for audit; does not gate accept/reject. See pilot-workflow doc §"AI tool + model metadata".

## Output Format


## Acceptance Criteria (machine-checkable)

- [ ] Every sidecar has `_contribution.ai_tool` and `_contribution.ai_model` set.
- [ ] PR branch name matches `tasktorrent/<chunk-id>`.
- [ ] `git diff --name-only main..HEAD` lists only files under `contributions/<chunk-id>/`.
- [ ] `task_manifest.txt` is committed and matches the manifest in this issue.
- [ ] Every sidecar's `_contribution.target_entity_id` is in the manifest.
- [ ] Every sidecar passes Pydantic validation (after `_contribution:` strip).
- [ ] `pytest tests/` passes on the contributor branch.
- [ ] Every `_contribution.target_action: upsert` references an entity that exists on `master`.
- [ ] Every `_contribution.target_action: new` does NOT collide with an existing ID on `master`.
- [ ] Every `SRC-*` referenced exists on `master` OR has a `source_stub_*.yaml` in the chunk directory.
- [ ] No banned source (`SRC-ONCOKB`, etc.) appears in contributor-authored output.

Run locally before PR:
```
python -m scripts.tasktorrent.validate_contributions <chunk-id>
```

## Acceptance Criteria (semantic, maintainer-checked)

- [ ] Output stays inside assigned manifest.
- [ ] Required schema is followed (no invented fields).
- [ ] Stable IDs preserved for `target_action: upsert`.
- [ ] Duplicates flagged with `target_action: flag_duplicate` and `duplicate_of: <stable-id>`.
- [ ] `_contribution.notes_for_reviewer` explains any non-obvious choice.

## Rejection Criteria

- Medical advice
- Treatment recommendation wording
- Patient-specific output
- Missing or fake citations
- Banned source used
- Unrelated edits or files outside sidecar path
- Entity IDs outside the manifest
- Pre-commit hooks bypassed (`--no-verify`)
- `git add -A` / `git add .` evidence

## How to claim

Comment on this issue: `I'd like to take this chunk.` Maintainer will assign within 24 hours. One contributor per chunk.
