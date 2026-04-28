# TaskTorrent contributor + maintainer scripts

## Contributor flow (one-prompt onboarding)

| Script | What it does |
|---|---|
| `bootstrap_contributor.sh` | One-shot setup: deps check, gh auth, clone, find next chunk, print marching orders |
| `next_chunk.py` | Discover the next claimable chunk; emit JSON for agent context |
| `auto_claim.sh <chunk-id>` | Claim per declared method (`formal-issue` comment OR push WIP branch) |
| `auto_pr.sh <chunk-id>` | Pre-flight then `gh pr create` for the finished sidecar |
| `validate_contributions.py` | Schema + manifest + banned-source + ID-collision checks (run often during work) |

Paste-and-go prompt for AI tools: [`docs/contributing/PROMPT_PASTE_AND_GO.md`](../../docs/contributing/PROMPT_PASTE_AND_GO.md).

Full workflow: [`docs/contributing/CONTRIBUTOR_QUICKSTART.md`](../../docs/contributing/CONTRIBUTOR_QUICKSTART.md).

## Maintainer flow

| Script | What it does |
|---|---|
| `validate_contributions.py` | Same as above; also gates CI on PR |
| `upsert_contributions.py` | Apply merged sidecars to hosted KB (`--confirm` required) |
| `check_manifest_overlap.py` | Pre-flight when opening a new chunk against active chunks |
| `check_claim_sla.py` | Hourly bot — auto-release issues unassigned >24h |
| `auto_release_stale_claims.py` | Daily bot — release assignees inactive >14d |
| `reverify_*.py` | Per-chunk-type computational re-verification (BMA via CIViC, citation title-substring, etc.) |
| `triage_*.py` | Generate maintainer-walkable markdown queues from audit chunks |
| `extract_trials_needing_source.py` | Helper for trial-source-ingest chunks |

## Quick reference for contributors

```bash
# Find next chunk + print orders
scripts/tasktorrent/bootstrap_contributor.sh

# Or just discover (JSON)
python -m scripts.tasktorrent.next_chunk --json-only

# Claim it (formal-issue OR trusted-agent — script auto-detects from issue body)
scripts/tasktorrent/auto_claim.sh <chunk-id> --issue <#>

# Validate as you work
python -m scripts.tasktorrent.validate_contributions <chunk-id>

# Open the PR
scripts/tasktorrent/auto_pr.sh <chunk-id> --issue <#>
```

## Hard invariants the scripts enforce

- **Allowlist**: `auto_pr.sh` rejects PRs whose diff includes files outside `contributions/<chunk-id>/`.
- **Sidecar minimum**: `_contribution_meta.yaml` + `task_manifest.txt` required.
- **Validator gate**: `auto_pr.sh` blocks PR open if `validate_contributions.py` fails.
- **Claim methods**: only `formal-issue` and `trusted-agent-wip-branch-first` accepted.

## Script flags

All four contributor scripts accept `--dry-run` to print what they would do without side effects.

`bootstrap_contributor.sh` accepts `--no-clone` if you've already cloned the repo.

## Why bash scripts (not Python)

The contributor scripts wrap `gh` and `git` — both shell-native. Python wrappers would add an interpreter dependency between contributor and the work. Discovery + parsing (which has real complexity) is in `next_chunk.py`. Everything else is glue.

## Tests

```bash
C:/Python312/python.exe -m pytest tests/test_tasktorrent_next_chunk.py
C:/Python312/python.exe -m pytest tests/test_tasktorrent_scripts_smoke.py
```

22 tests for the parser + 12 smoke tests for the bash scripts.
