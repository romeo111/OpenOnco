#!/usr/bin/env bash
#
# auto_claim — claim a TaskTorrent chunk per its declared claim_method.
#
# Usage:
#   auto_claim.sh <chunk-id> [--repo OWNER/REPO]
#                              [--issue NUMBER]      # required for formal-issue
#                              [--branch BRANCH]     # default: tasktorrent/<chunk-id>
#                              [--method METHOD]     # formal-issue | trusted-agent-wip-branch-first
#                              [--dry-run]
#
# Behavior per claim_method:
#   formal-issue:
#     - gh issue comment <#> -b "I'd like to take this chunk."
#     - Maintainer assigns within 24h SLA (claim-sla-bot enforces).
#
#   trusted-agent-wip-branch-first:
#     - git checkout -b tasktorrent/<chunk-id>
#     - empty commit "WIP <chunk-id>"
#     - git push -u origin tasktorrent/<chunk-id>
#     - Branch on origin = visible lock (other agents won't duplicate).
#
# If --method is omitted, the script reads the issue body via gh and
# extracts claim_method from the `## Claim Method` section. Falls back
# to formal-issue if nothing parseable is found.
#
# Exit codes:
#   0 — claimed successfully
#   1 — usage / argument error
#   2 — gh CLI missing
#   3 — issue lookup or comment failed
#   4 — git operation failed

set -euo pipefail

REPO="romeo111/OpenOnco"
CHUNK_ID=""
ISSUE_NUMBER=""
BRANCH=""
METHOD=""
DRY_RUN=0

usage() {
  sed -n '3,/^$/p' "$0" | sed -n '/^# /s/^# //p'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO="$2"; shift 2 ;;
    --issue)   ISSUE_NUMBER="$2"; shift 2 ;;
    --branch)  BRANCH="$2"; shift 2 ;;
    --method)  METHOD="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage 0 ;;
    --*)       echo "ERROR: unknown flag $1" >&2; usage 1 >&2 ;;
    *)
      if [[ -z "$CHUNK_ID" ]]; then CHUNK_ID="$1"; shift
      else echo "ERROR: unexpected positional $1" >&2; usage 1 >&2
      fi ;;
  esac
done

if [[ -z "$CHUNK_ID" ]]; then
  echo "ERROR: chunk-id is required" >&2; usage 1 >&2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not on PATH (install: https://cli.github.com/)" >&2
  exit 2
fi

BRANCH="${BRANCH:-tasktorrent/$CHUNK_ID}"

# If method not given, try parsing it from the issue body.
if [[ -z "$METHOD" ]]; then
  if [[ -z "$ISSUE_NUMBER" ]]; then
    # Find issue by chunk-id in title heuristic: search "[Chunk] <chunk-id>"
    ISSUE_NUMBER=$(gh issue list --repo "$REPO" --label chunk-task --state open \
      --search "in:title \"$CHUNK_ID\"" --json number --jq '.[0].number' 2>/dev/null || true)
  fi
  if [[ -n "$ISSUE_NUMBER" ]]; then
    BODY=$(gh issue view "$ISSUE_NUMBER" --repo "$REPO" --json body --jq '.body' 2>/dev/null || true)
    METHOD=$(printf '%s\n' "$BODY" | awk '
      /^## Claim Method/ { in_section=1; next }
      in_section && /^## / { in_section=0 }
      in_section && /`(formal-issue|trusted-agent-wip-branch-first)`/ {
        match($0, /`(formal-issue|trusted-agent-wip-branch-first)`/, m)
        gsub("`","",m[0]); print m[0]; exit
      }
    ')
  fi
  METHOD="${METHOD:-formal-issue}"
fi

case "$METHOD" in
  formal-issue|trusted-agent-wip-branch-first) ;;
  *)
    echo "ERROR: invalid --method $METHOD (expected formal-issue or trusted-agent-wip-branch-first)" >&2
    exit 1
    ;;
esac

echo "→ chunk_id:     $CHUNK_ID"
echo "→ repo:         $REPO"
echo "→ method:       $METHOD"
[[ -n "$ISSUE_NUMBER" ]] && echo "→ issue:        #$ISSUE_NUMBER"
echo "→ branch:       $BRANCH"
[[ "$DRY_RUN" -eq 1 ]] && echo "→ DRY-RUN (no side effects)"
echo

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "+ $*"
  else
    "$@"
  fi
}

case "$METHOD" in
  formal-issue)
    if [[ -z "$ISSUE_NUMBER" ]]; then
      echo "ERROR: formal-issue claim requires --issue NUMBER (or chunk-id resolvable from open issues)" >&2
      exit 1
    fi
    echo "Claiming via comment on issue #$ISSUE_NUMBER..."
    if ! run gh issue comment "$ISSUE_NUMBER" --repo "$REPO" \
         --body "I'd like to take this chunk."; then
      echo "ERROR: gh issue comment failed" >&2
      exit 3
    fi
    echo
    echo "Claim posted. Maintainer assigns within 24h (claim-sla-bot enforces)."
    echo "If not assigned within 24h, bot auto-releases and chunk reopens for others."
    ;;

  trusted-agent-wip-branch-first)
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      echo "ERROR: not inside a git working tree" >&2
      exit 4
    fi
    # Create branch (or switch if it already exists locally)
    if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
      run git checkout "$BRANCH" || { echo "ERROR: cannot checkout $BRANCH" >&2; exit 4; }
    else
      run git checkout -b "$BRANCH" || { echo "ERROR: cannot create $BRANCH" >&2; exit 4; }
    fi
    # Empty WIP commit
    run git commit --allow-empty -m "WIP: $CHUNK_ID — visible-lock per L-19 trusted-agent flow" \
      || { echo "ERROR: empty commit failed" >&2; exit 4; }
    run git push -u origin "$BRANCH" \
      || { echo "ERROR: git push failed" >&2; exit 4; }
    echo
    echo "WIP branch on origin = your visible claim. Other agents won't duplicate."
    echo "Stale-claim auto-release: 14 days of no branch activity → bot reopens."
    ;;
esac

echo
echo "Next: do the work, then run scripts/tasktorrent/auto_pr.sh $CHUNK_ID"
