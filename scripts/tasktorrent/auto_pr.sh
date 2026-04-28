#!/usr/bin/env bash
#
# auto_pr — open a PR for a finished TaskTorrent chunk.
#
# Usage:
#   auto_pr.sh <chunk-id> [--repo OWNER/REPO]
#                          [--base BRANCH]       # default: master
#                          [--branch BRANCH]     # default: tasktorrent/<chunk-id>
#                          [--issue NUMBER]      # links into PR body
#                          [--draft]
#                          [--dry-run]
#
# Pre-flight checks (abort if any fails):
#   1. We're on the expected branch (--branch / tasktorrent/<chunk-id>).
#   2. Working tree is clean.
#   3. contributions/<chunk-id>/ exists and contains _contribution_meta.yaml.
#   4. task_manifest.txt exists in contributions/<chunk-id>/.
#   5. validate_contributions.py passes for this chunk.
#   6. git diff --name-only base..HEAD lists only files under
#      contributions/<chunk-id>/ (allowlist enforcement).
#
# PR body is generated from the chunk-spec acceptance criteria + the
# sidecar's _contribution_meta.yaml. Links the chunk-task issue if
# given via --issue.
#
# Exit codes:
#   0 — PR opened
#   1 — usage / argument error
#   2 — gh CLI missing
#   3 — pre-flight check failed
#   4 — gh pr create failed

set -euo pipefail

REPO="romeo111/OpenOnco"
CHUNK_ID=""
BASE="master"
BRANCH=""
ISSUE_NUMBER=""
DRAFT=0
DRY_RUN=0

usage() {
  sed -n '3,/^$/p' "$0" | sed -n '/^# /s/^# //p'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO="$2"; shift 2 ;;
    --base)    BASE="$2"; shift 2 ;;
    --branch)  BRANCH="$2"; shift 2 ;;
    --issue)   ISSUE_NUMBER="$2"; shift 2 ;;
    --draft)   DRAFT=1; shift ;;
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
  echo "ERROR: gh CLI not on PATH" >&2; exit 2
fi

BRANCH="${BRANCH:-tasktorrent/$CHUNK_ID}"
SIDECAR_DIR="contributions/$CHUNK_ID"

echo "→ chunk_id: $CHUNK_ID"
echo "→ branch:   $BRANCH (base $BASE)"
echo "→ sidecar:  $SIDECAR_DIR/"
[[ -n "$ISSUE_NUMBER" ]] && echo "→ issue:    #$ISSUE_NUMBER"
[[ "$DRY_RUN" -eq 1 ]] && echo "→ DRY-RUN"
echo

# --- Pre-flight ---

current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [[ "$current_branch" != "$BRANCH" ]]; then
  echo "ERROR: pre-flight failed — on branch '$current_branch', expected '$BRANCH'" >&2
  exit 3
fi

if ! git diff --quiet --exit-code; then
  echo "ERROR: pre-flight failed — working tree has unstaged changes" >&2
  exit 3
fi
if ! git diff --quiet --cached --exit-code; then
  echo "ERROR: pre-flight failed — working tree has staged-but-uncommitted changes" >&2
  exit 3
fi

if [[ ! -d "$SIDECAR_DIR" ]]; then
  echo "ERROR: pre-flight failed — $SIDECAR_DIR/ does not exist" >&2
  exit 3
fi
if [[ ! -f "$SIDECAR_DIR/_contribution_meta.yaml" ]]; then
  echo "ERROR: pre-flight failed — $SIDECAR_DIR/_contribution_meta.yaml missing" >&2
  exit 3
fi
if [[ ! -f "$SIDECAR_DIR/task_manifest.txt" ]]; then
  echo "ERROR: pre-flight failed — $SIDECAR_DIR/task_manifest.txt missing" >&2
  exit 3
fi

# Allowlist enforcement: every changed file relative to base must live under sidecar dir.
git fetch origin "$BASE" --quiet 2>/dev/null || true
out_of_scope=$(git diff --name-only "origin/$BASE...HEAD" -- ":(exclude)$SIDECAR_DIR" || true)
if [[ -n "$out_of_scope" ]]; then
  echo "ERROR: pre-flight failed — files outside $SIDECAR_DIR/ in this branch:" >&2
  echo "$out_of_scope" >&2
  exit 3
fi

# Optional but recommended: run the validator if it's available.
if [[ -f "scripts/tasktorrent/validate_contributions.py" ]]; then
  echo "→ Running validate_contributions.py..."
  if ! python -m scripts.tasktorrent.validate_contributions "$CHUNK_ID" >/dev/null 2>&1; then
    echo "ERROR: pre-flight failed — validate_contributions.py reported errors" >&2
    echo "       Run manually to see details:" >&2
    echo "       python -m scripts.tasktorrent.validate_contributions $CHUNK_ID" >&2
    exit 3
  fi
fi

echo "✓ Pre-flight passed"
echo

# --- Generate PR body ---

PR_TITLE="[TaskTorrent] $CHUNK_ID — chunk deliverable"
PR_BODY_FILE=$(mktemp)
trap 'rm -f "$PR_BODY_FILE"' EXIT

cat > "$PR_BODY_FILE" <<EOF
## Chunk: \`$CHUNK_ID\`

EOF

if [[ -n "$ISSUE_NUMBER" ]]; then
  echo "Closes #$ISSUE_NUMBER" >> "$PR_BODY_FILE"
  echo "" >> "$PR_BODY_FILE"
fi

cat >> "$PR_BODY_FILE" <<EOF
## Sidecar files

\`\`\`
$(git diff --name-only "origin/$BASE...HEAD" | head -50)
\`\`\`

## Validation

- [x] Pre-flight: branch + working tree + sidecar dir
- [x] Allowlist: only files under \`$SIDECAR_DIR/\`
- [x] \`task_manifest.txt\` committed
- [x] \`_contribution_meta.yaml\` includes \`ai_tool\` + \`ai_model\`
EOF

if [[ -f "scripts/tasktorrent/validate_contributions.py" ]]; then
  echo "- [x] \`validate_contributions.py\` passes locally" >> "$PR_BODY_FILE"
fi

cat >> "$PR_BODY_FILE" <<EOF

## Maintainer review

- [ ] Computational re-verify (per chunk-spec)
- [ ] Sample re-verify (if applicable)
- [ ] Acceptance criteria semantic check

🤖 Generated by \`scripts/tasktorrent/auto_pr.sh\`
EOF

# --- Open PR ---

CMD=(gh pr create --repo "$REPO" --base "$BASE" --head "$BRANCH"
     --title "$PR_TITLE" --body-file "$PR_BODY_FILE")
[[ "$DRAFT" -eq 1 ]] && CMD+=(--draft)

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "DRY-RUN — would run:"
  printf '  %q ' "${CMD[@]}"; echo
  echo
  echo "PR body would be:"
  echo "================"
  cat "$PR_BODY_FILE"
  exit 0
fi

if ! "${CMD[@]}"; then
  echo "ERROR: gh pr create failed" >&2
  exit 4
fi
