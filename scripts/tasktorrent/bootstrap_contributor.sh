#!/usr/bin/env bash
#
# bootstrap_contributor — one-prompt onboarding entry point.
#
# Usage:
#   bootstrap_contributor.sh [--repo OWNER/REPO]
#                             [--clone-dir PATH]   # default: ./openonco
#                             [--no-clone]         # skip clone (already cloned)
#                             [--dry-run]
#
# Pipeline:
#   1. Sanity-check deps (git, gh, python ≥3.10)
#   2. Verify gh authentication
#   3. Clone OpenOnco (unless --no-clone)
#   4. Run next_chunk.py to find the next claimable chunk
#   5. Print the contributor's marching orders + next-step commands
#
# Does NOT itself claim a chunk — that's `auto_claim.sh`. This is just
# the discovery + handoff stage so the contributor's agent can decide
# whether the chunk fits its skills + token budget.
#
# Exit codes:
#   0 — discovered next chunk and printed orders
#   1 — dependency check failed
#   2 — auth failed
#   3 — clone failed
#   4 — no chunks available (shelf empty)
#   5 — next_chunk parse error

set -euo pipefail

REPO="romeo111/OpenOnco"
CLONE_DIR="./openonco"
NO_CLONE=0
DRY_RUN=0

usage() {
  sed -n '3,/^$/p' "$0" | sed -n '/^# /s/^# //p'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)      REPO="$2"; shift 2 ;;
    --clone-dir) CLONE_DIR="$2"; shift 2 ;;
    --no-clone)  NO_CLONE=1; shift ;;
    --dry-run)   DRY_RUN=1; shift ;;
    -h|--help)   usage 0 ;;
    *)           echo "ERROR: unknown arg $1" >&2; usage 1 >&2 ;;
  esac
done

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then echo "+ $*"
  else "$@"
  fi
}

echo "TaskTorrent contributor bootstrap"
echo "================================="
echo "→ repo:      $REPO"
echo "→ clone dir: $CLONE_DIR"
[[ "$NO_CLONE" -eq 1 ]] && echo "→ skipping clone (--no-clone)"
[[ "$DRY_RUN" -eq 1 ]] && echo "→ DRY-RUN"
echo

# --- 1. Dependency check ---

echo "Step 1/5: Checking dependencies..."
for cmd in git gh; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "  ERROR: $cmd not on PATH" >&2
    echo "    git: https://git-scm.com/" >&2
    echo "    gh:  https://cli.github.com/" >&2
    exit 1
  fi
done

# Find a Python 3.10+ interpreter from common candidates.
# PY_CMD is an array so multi-token launchers like `py -3` work.
PY_CMD=()
PYTHON_VERSION_RE='Python 3\.(1[0-9]|[2-9][0-9])'
declare -a CANDIDATES=(
  "python3"
  "python"
  "py -3.12"
  "py -3.11"
  "py -3.10"
  "py -3"
)
for candidate in "${CANDIDATES[@]}"; do
  # shellcheck disable=SC2086
  ver=$($candidate --version 2>&1 || true)
  if printf '%s' "$ver" | grep -qE "$PYTHON_VERSION_RE"; then
    # shellcheck disable=SC2206
    PY_CMD=($candidate); break
  fi
done
if [[ ${#PY_CMD[@]} -eq 0 ]]; then
  echo "  ERROR: Python 3.10+ not found." >&2
  echo "    Tried: ${CANDIDATES[*]}" >&2
  echo "    Install: https://python.org/ (3.10+)" >&2
  exit 1
fi
echo "  ✓ git, gh, ${PY_CMD[*]} ($("${PY_CMD[@]}" --version 2>&1))"

# --- 2. gh auth ---

echo
echo "Step 2/5: Checking gh authentication..."
if ! gh auth status >/dev/null 2>&1; then
  echo "  Not authenticated. Run: gh auth login" >&2
  exit 2
fi
echo "  ✓ gh authenticated"

# --- 3. Clone (unless --no-clone) ---

REPO_ROOT="$CLONE_DIR"
if [[ "$NO_CLONE" -eq 0 ]]; then
  echo
  echo "Step 3/5: Cloning $REPO..."
  if [[ -d "$CLONE_DIR/.git" ]]; then
    echo "  $CLONE_DIR already exists; skipping clone (use git pull manually if you want updates)"
  else
    if ! run gh repo clone "$REPO" "$CLONE_DIR"; then
      echo "  ERROR: clone failed" >&2
      exit 3
    fi
  fi
else
  echo
  echo "Step 3/5: Skipped clone (--no-clone)"
  REPO_ROOT="."
fi

# --- 4. Find next chunk ---

echo
echo "Step 4/5: Finding next claimable chunk..."
NEXT_JSON_FILE=$(mktemp)
trap 'rm -f "$NEXT_JSON_FILE"' EXIT

# Run from inside the clone so module path resolves
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "+ (${PY_CMD[*]} -m scripts.tasktorrent.next_chunk --repo $REPO --json-only) > $NEXT_JSON_FILE"
  echo '  (dry-run: skipping actual fetch)'
  exit 0
fi

if [[ -d "$REPO_ROOT/scripts/tasktorrent" ]]; then
  ( cd "$REPO_ROOT" && "${PY_CMD[@]}" -m scripts.tasktorrent.next_chunk \
      --repo "$REPO" --json-only ) > "$NEXT_JSON_FILE" || true
else
  # Fallback: invoke from current directory
  "${PY_CMD[@]}" -m scripts.tasktorrent.next_chunk --repo "$REPO" --json-only \
    > "$NEXT_JSON_FILE" || true
fi

STATUS=$("${PY_CMD[@]}" -c "import json,sys; print(json.load(open(sys.argv[1])).get('status','error'))" "$NEXT_JSON_FILE" 2>/dev/null || echo "error")

if [[ "$STATUS" == "no_chunks_available" ]]; then
  echo
  echo "Shelf is empty — no chunks open for new claims right now."
  echo "Watch https://github.com/$REPO/issues?q=is%3Aopen+label%3Achunk-task+label%3Astatus-active for new ones."
  exit 4
fi
if [[ "$STATUS" != "ok" ]]; then
  echo "  ERROR: next_chunk.py returned unexpected status: $STATUS" >&2
  cat "$NEXT_JSON_FILE" >&2
  exit 5
fi

# Extract a few key fields for the orders
read -r CHUNK_ID ISSUE_NUMBER BRANCH METHOD SPEC_URL DROPS < <(
  "${PY_CMD[@]}" -c "
import json,sys
d=json.load(open(sys.argv[1]))
def s(k): return str(d.get(k) or '')
print(s('chunk_id'), s('issue_number'), s('branch'), s('claim_method'), s('spec_url'), s('drop_estimate'))
" "$NEXT_JSON_FILE"
)

# --- 5. Print marching orders ---

echo
echo "Step 5/5: Marching orders"
echo "========================="
echo
echo "Chunk:         $CHUNK_ID"
echo "Issue:         #$ISSUE_NUMBER  (https://github.com/$REPO/issues/$ISSUE_NUMBER)"
echo "Branch:        $BRANCH"
echo "Claim method:  $METHOD"
echo "Spec:          $SPEC_URL"
echo "Drop estimate: $DROPS"
echo
echo "To claim and start work:"
echo
echo "  cd $REPO_ROOT"
echo "  scripts/tasktorrent/auto_claim.sh $CHUNK_ID --issue $ISSUE_NUMBER --method $METHOD"
echo
echo "Then do the work in $BRANCH on contributions/$CHUNK_ID/."
echo "Read the chunk spec carefully:  $SPEC_URL"
echo
echo "When done:"
echo "  scripts/tasktorrent/auto_pr.sh $CHUNK_ID --issue $ISSUE_NUMBER"
echo
echo "Full JSON for your agent (paste into context):"
cat "$NEXT_JSON_FILE"
