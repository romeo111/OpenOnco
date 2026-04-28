# Contributor Quickstart

You want to help OpenOnco. You have an AI tool (Codex / Claude Code / Cursor / ChatGPT). You have ~2–4 hours. Here's the shortest path from "want to help" to "PR merged."

> Prerequisite reading: [`HELP_WANTED.md`](HELP_WANTED.md) — pilot framing and safety boundaries. **You will not write medical advice or treatment recommendations.** You drive your AI tool through structured evidence drafting; maintainers review.

## Fastest path — paste-and-go (recommended)

If your AI tool has filesystem + shell access (Claude Code, Codex CLI, Cursor):

1. Read [`PROMPT_PASTE_AND_GO.md`](PROMPT_PASTE_AND_GO.md) — the canonical 8-line prompt
2. Paste it into your AI agent
3. The agent runs `scripts/tasktorrent/bootstrap_contributor.sh` → finds next chunk → orchestrates `auto_claim.sh` → does work → runs `auto_pr.sh`

Manual phase-by-phase steps below if you want to understand each step or your tool is web-only (ChatGPT).

## 1. Setup (5 min)

```bash
# Fork https://github.com/romeo111/OpenOnco on GitHub, then:
git clone https://github.com/<your-username>/OpenOnco.git
cd OpenOnco
pip install -e .
pip install pyyaml pydantic
```

Confirm Python 3.12 (the schema layer needs PEP 585 syntax):

```bash
python --version    # 3.12.x or higher; on Windows: py -V:3.12
```

## 2. Pick an active chunk (5 min)

1. Open the active-chunk issue list:
   <https://github.com/romeo111/OpenOnco/issues?q=is%3Aissue+is%3Aopen+label%3Achunk-task+label%3Astatus-active>
2. Read the chunk-task issue. It links to the full chunk spec at
   `https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/<chunk-id>.md`.
3. Note the chunk's **`claim_method`** — declared in the spec. Two values:
   - `formal-issue`: comment on issue → maintainer assigns. Step 3 below.
   - `trusted-agent-wip-branch-first`: skip issue claim, push WIP branch immediately. Step 3 below describes this.
4. For `formal-issue` chunks: comment on the issue: `I'd like to take this chunk.` Wait up to 24 hours for the maintainer to assign you. **24h SLA** — if not assigned, the chunk auto-releases.

If no chunks are `status-active`, all slots are taken or queued. Subscribe to the repo or check back.

## 3. Branch + WIP-push (1 min)

For both claim methods:

```bash
git checkout -b tasktorrent/<chunk-id>      # e.g. tasktorrent/escat-tier-audit
git commit --allow-empty -m "wip: starting <chunk-id>"
git push -u origin tasktorrent/<chunk-id>
```

**The empty WIP-push is mandatory for `trusted-agent-wip-branch-first` chunks** — it broadcasts your claim immediately, before you do significant local work. Other trusted agents see the branch on origin and don't duplicate.

For `formal-issue` chunks: WIP-push is recommended even though the issue assignee is the primary lock. Two layers of visibility = better coordination.

The branch name matters — CI looks for the `tasktorrent/` prefix.

**Stale-claim auto-release:** if you don't push commits to your branch for 14 days, a bot will release your claim (drop assignee, re-open the slot). If you need more time, comment on the issue with an ETA before the bot fires.

## 4. Read the agent prompt (10 min)

For each chunk, there is a copy-paste prompt at
`docs/contributing/AGENT_PROMPT_<chunk-id>.md`. Open it. The prompt is the canonical instructions for your AI tool.

Read it once yourself before pasting. Things that look wrong to you (file paths that don't exist, manifest items that look misnamed) **probably are wrong** — comment on the chunk issue and ask before running. Don't have your AI tool guess.

## 5. Run with your AI tool (1–3 hours)

### If you use Codex CLI / Claude Code / Cursor

These tools can read files in the repo. Just:

1. Open the repo in the tool.
2. Paste the agent prompt as the first message.
3. Let it work. It reads, generates, writes sidecars.
4. Watch token usage — chunks are sized at ~1M tokens of structured AI work; budget accordingly.

### If you use ChatGPT (web, no file access)

You'll need to feed it context manually:

1. Paste the agent prompt.
2. Paste the contents of `contributions/<chunk-id>/task_manifest.txt`.
3. For the first 1–2 entities in the manifest: paste the existing entity YAML from `knowledge_base/hosted/content/<subdir>/<file>.yaml`.
4. Ask it to produce the sidecar for that entity.
5. Save the output as `contributions/<chunk-id>/<filename>.yaml`.
6. Repeat for next entity. Yes, this is tedious — Codex / Claude Code is much faster.

### Reference output

A working PoC sidecar lives at:

```
contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml
```

This is the exact shape your AI tool should produce. Match the `_contribution` wrapper, the field order, the way `evidence_sources` are bucketed.

## 6. Self-validate (2 min)

Before you commit anything, run the validator locally:

```bash
python -m scripts.tasktorrent.validate_contributions <chunk-id>
```

Expected last line: `All contributions pass validation.`

If you see `FAIL`, the script names the file and the rule that failed. Fix and re-run. **Do not submit a PR with FAIL output.** CI will reject it; maintainer time wasted on both sides.

Common failures:

| Failure | Fix |
|---|---|
| `_contribution.ai_tool missing` | Add `ai_tool: codex` (or your tool) to every sidecar wrapper. |
| `_contribution.ai_model missing` | Add `ai_model: gpt-5-mini` (or your model). |
| `target_entity_id 'X' not in task_manifest.txt` | Either remove the out-of-scope sidecar or check why your AI tool processed it. |
| `references unknown SRC-* 'SRC-FOO'` | Either find the existing `SRC-*` ID or file a `source_stub_<id>.yaml` in the chunk dir. |
| `Pydantic validation failed: ...` | Field name or type wrong. Compare against the schema file in `knowledge_base/schemas/`. |

## 7. Commit and push (3 min)

```bash
# Stage ONLY the chunk dir — never use git add -A or git add .
git add contributions/<chunk-id>/

# Commit
git commit -m "tasktorrent(<chunk-id>): N sidecars"

# Push
git push origin tasktorrent/<chunk-id>
```

If pre-commit hooks complain (formatting / lint), fix what they flag and re-stage. Never use `--no-verify`.

## 8. Open the PR (2 min)

```bash
gh pr create --title "tasktorrent(<chunk-id>): <N> sidecars" --base master
```

Or via web UI. The PR template auto-loads — fill in the AI Model section and tick the safety + machine-checkable validation boxes you actually verified.

Link the chunk-task issue (`Closes #<issue-number>`).

## 9. Wait for review (1–7 working days)

CI runs `validate_contributions.py` automatically. Possible outcomes:

- **CI passes + maintainer accepts:** PR merges. Your sidecars sit in `contributions/<chunk-id>/`. Maintainer later runs the upsert script after Clinical Co-Lead signoff (where applicable). You're done.
- **CI passes + maintainer requests changes:** read the review, fix, force-push to your branch. CI re-runs.
- **CI fails:** fix the issues listed and force-push.
- **PR rejected:** maintainer posts a standardized rejection comment (see `REJECTION_TEMPLATES.md`). Either fix and re-submit, or drop the chunk.

## 10. Drop a chunk if you can't finish

You're a volunteer. If you started a chunk and can't complete it within 14 days, comment on the chunk issue saying so, and the maintainer reopens the slot. Don't disappear silently — that blocks a slot.

---

## When your AI tool gets stuck

Common stuck-states and how to unstick:

- **Tool keeps producing fields not in the schema.** Force it to read `knowledge_base/schemas/<entity>.py` first. Cite the schema file in your prompt. If your tool can't read files, paste the relevant schema class as context.
- **Tool invents `SRC-*` IDs that don't exist.** Tell it explicitly: "Do not invent `SRC-*` IDs. If a citation has no corresponding Source entity, file a `source_stub_<id>.yaml` in the chunk dir."
- **Tool generates the same row 3 times with slightly different IDs.** Add to prompt: "Each entity in the manifest gets exactly one sidecar file. Check for duplicates before writing."
- **Tool writes to `knowledge_base/hosted/content/`.** Stop it. That's hosted clinical content, not contributor scope. Contributor output goes ONLY to `contributions/<chunk-id>/`.
- **Tool's output looks plausible but you can't verify a citation.** Mark `support_status: unclear` (for citation chunks) or `actionability_review_required: true` (for BMA chunks). Don't claim certainty you don't have. Maintainers expect contributors to be conservative.

## What you do NOT do

- **You do not write medical advice.** No "best treatment", no "patients should", no recommendation phrasing. Use neutral evidence wording.
- **You do not edit `knowledge_base/hosted/content/`.** All output goes to `contributions/<chunk-id>/`.
- **You do not bundle multiple chunks in one PR.** One chunk = one PR.
- **You do not skip pre-commit hooks.** No `--no-verify`.
- **You do not use `git add -A` / `git add .`.** Stage explicit paths only.
- **You do not cite `SRC-ONCOKB`, `SRC-SNOMED`, or `SRC-MEDDRA`.** These are banned for the pilot.

## Where to ask questions

- Comment on the chunk-task issue.
- Open a separate issue with label `question`.
- Discussions: <https://github.com/romeo111/OpenOnco/discussions>

Don't ask your AI tool to "ask me clarifying questions" — its questions usually aren't useful. Ask the maintainer directly.

---

Happy contributing. You're helping people get better cancer treatment plans without a billable hour going to it. Don't over-promise on what your AI tool can do; do under-promise and over-deliver one chunk at a time.
