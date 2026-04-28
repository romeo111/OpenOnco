# OpenOnco contributor — paste-and-go prompt

Copy-paste this into Claude Code, Codex, Cursor, or ChatGPT. The agent will discover the next claimable chunk, do the work, and open a PR.

> **Read this before pasting.** OpenOnco is a free public oncology decision-support project. By contributing you agree:
> - No medical advice or treatment recommendations in your output
> - No patient-specific data
> - Banned sources: SRC-ONCOKB, SRC-SNOMED, SRC-MEDDRA (CHARTER §2)
> - Two-reviewer signoff for clinical content
> - You verify your output against cited sources

---

## The 8-line prompt

```
You are an OpenOnco TaskTorrent contributor agent. Your goal is to do one chunk of structured KB work and submit it as a PR.

1. Read https://github.com/romeo111/OpenOnco/blob/master/docs/contributing/CONTRIBUTOR_QUICKSTART.md (full workflow).
2. Run scripts/tasktorrent/bootstrap_contributor.sh — it tells you the next available chunk.
3. Read the chunk spec at the printed URL. Confirm you can complete it within the Drop estimate. If not, exit.
4. Run scripts/tasktorrent/auto_claim.sh <chunk-id> --issue <#> --method <method>.
5. Do the work on branch tasktorrent/<chunk-id>, only under contributions/<chunk-id>/. Every sidecar's _contribution_meta.yaml must declare ai_tool + ai_model.
6. Run python -m scripts.tasktorrent.validate_contributions <chunk-id> until it passes.
7. Run scripts/tasktorrent/auto_pr.sh <chunk-id> --issue <#> to open the PR.
8. STOP after PR is opened. Do not push to master, do not create chunks, do not delete branches.
```

## How it works under the hood

| Step | What runs | Side effects |
|---|---|---|
| 2 | `next_chunk.py` queries GitHub for `chunk-task,status-active,assignee=none` and returns oldest | read-only |
| 4 | `auto_claim.sh` either comments on the issue or pushes a WIP branch to origin (depends on `claim_method`) | one comment OR one branch push |
| 5 | Your agent's actual work | files in `contributions/<chunk-id>/` only |
| 6 | `validate_contributions.py` — schema, manifest, banned-sources, ID-collision checks | read-only |
| 7 | `auto_pr.sh` — pre-flight (branch, scope, validator) then `gh pr create` | one PR |

## Hard invariants the agent must respect

- **Allowlist:** every file you touch must be under `contributions/<chunk-id>/`. Anything outside is a `scope` rejection.
- **Banned sources** (CHARTER §2): SRC-ONCOKB, SRC-SNOMED, SRC-MEDDRA. Hard rejection on any reference.
- **No `git add -A`:** stage explicit pathspecs only. Other in-flight work might be on the same branch.
- **No `--no-verify`** on commits. Pre-commit hooks are gates, not noise.
- **No medical advice, no patient-specific output.** The KB describes evidence; it does not prescribe. CHARTER §8.3.
- **Two-reviewer signoff** for clinical content (CHARTER §6.1). The maintainer routes; you don't self-approve.

## What if you get stuck

Add `_contribution.notes_for_reviewer` to your sidecar explaining the blocker. Maintainer will reroute or close.

If the validator rejects in a way you don't understand, **don't bypass it**. Read the error, fix the cause, re-run. The validator is the contract.

## Quick reference

```bash
# Discovery
$ python -m scripts.tasktorrent.next_chunk --json-only
{
  "chunk_id": "trial-source-ingest-pubmed",
  "issue_number": 26,
  "claim_method": "formal-issue",
  ...
}

# Claim
$ scripts/tasktorrent/auto_claim.sh trial-source-ingest-pubmed --issue 26 --method formal-issue

# Validate (run this often during work)
$ python -m scripts.tasktorrent.validate_contributions trial-source-ingest-pubmed

# Open PR
$ scripts/tasktorrent/auto_pr.sh trial-source-ingest-pubmed --issue 26
```

## Cadence + expectations

- Drop estimate ≈ 100k tokens of structured AI work. Most chunks are 1-3 Drops.
- 24-hour SLA on `formal-issue` claims (claim-sla-bot enforces).
- 14-day stale-claim release: if your branch goes silent for 14 days, the bot releases the assignee back to the shelf.
- One contributor per chunk; one chunk per PR.

## License + attribution

OpenOnco is non-commercial public-good. Your contributions land under the project's license (see CHARTER §2). Cited sources keep their own licenses; you classify them in source stubs.

## Questions

Open an issue with the `question` label on https://github.com/romeo111/OpenOnco. Don't DM the maintainer privately — keep the audit trail public.
