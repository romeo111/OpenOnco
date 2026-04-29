"""One-off worker for chunk-task #37 — add-tasktorrent-version-observability.

Walks the manifest list, computes the first-commit date+sha for each
source contribution directory, reads the existing _contribution_meta.yaml,
adds `tasktorrent_version: YYYY-MM-DD-shortsha`, and writes the result
to contributions/add-tasktorrent-version-observability-2026-04-29-0030/<chunk-id>/_contribution_meta.yaml.

Idempotent — running twice yields the same output.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"
OUT_CHUNK_ID = "add-tasktorrent-version-observability-2026-04-29-0030"
OUT_DIR = CONTRIB_ROOT / OUT_CHUNK_ID

MANIFEST = [
    "bma-drafting-gap-diseases",
    "citation-semantic-verify-v2",
    "citation-verify-914-audit",
    "civic-bma-reconstruct-all",
    "drug-class-normalization",
    "escat-tier-audit",
    "indication-line-of-therapy-audit",
    "rec-wording-audit-claim-bearing",
    "redflag-indication-coverage-fill",
    "source-stub-ingest-batch",
    "trial-source-ingest-pubmed",
    "ua-translation-review-batch",
]


def first_commit_for_dir(rel_dir: str) -> tuple[str, str] | None:
    """Returns (date_iso, short_sha) of the FIRST commit touching this dir."""
    cmd = [
        "git", "log", "--reverse", "--format=%h %ai", "--",
        f"contributions/{rel_dir}/",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT,
                         encoding="utf-8", errors="replace", check=False)
    if res.returncode != 0 or not res.stdout.strip():
        return None
    first = res.stdout.strip().splitlines()[0].split()
    if len(first) < 2:
        return None
    short_sha, date = first[0], first[1]
    return date, short_sha


def render_version_stamp(date_iso: str, short_sha: str) -> str:
    return f"{date_iso}-{short_sha}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_lines: list[str] = []
    written = 0

    for chunk_id in MANIFEST:
        src_meta = CONTRIB_ROOT / chunk_id / "_contribution_meta.yaml"
        if not src_meta.is_file():
            print(f"  SKIP {chunk_id} — no source _contribution_meta.yaml found", file=sys.stderr)
            continue

        commit_info = first_commit_for_dir(chunk_id)
        if commit_info is None:
            print(f"  SKIP {chunk_id} — git log returned nothing", file=sys.stderr)
            continue
        date_iso, short_sha = commit_info
        # Use just date portion (YYYY-MM-DD) + sha
        date_part = date_iso.split()[0] if " " in date_iso else date_iso[:10]
        version = render_version_stamp(date_part, short_sha)

        # Read source meta, parse, add field, write to nested output path
        text = src_meta.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            print(f"  SKIP {chunk_id} — YAML parse error: {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            print(f"  SKIP {chunk_id} — meta is not a dict", file=sys.stderr)
            continue

        # The schema typically wraps under `_contribution:` block; if so, add
        # the field there. Otherwise add at top level.
        if "_contribution" in data and isinstance(data["_contribution"], dict):
            data["_contribution"]["tasktorrent_version"] = version
        else:
            data["tasktorrent_version"] = version

        out_dir = OUT_DIR / chunk_id
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "_contribution_meta.yaml"
        out_path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        rel = out_path.relative_to(REPO_ROOT).as_posix()
        manifest_lines.append(f"contributions/{chunk_id}/_contribution_meta.yaml")
        written += 1
        print(f"  WROTE {rel}  (version={version})")

    # Write our own task_manifest.txt
    (OUT_DIR / "task_manifest.txt").write_text(
        "\n".join(manifest_lines) + "\n", encoding="utf-8"
    )

    # Write our own _contribution_meta.yaml (self-describing, with our own version stamp)
    self_version = "2026-04-29-tbd"  # will be updated to actual sha after first commit
    self_meta = {
        "_contribution": {
            "chunk_id": OUT_CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": "2026-04-29",
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "ai_model_version": "1m-context",
            "ai_session_notes": (
                "Schema-evolution chunk. Read 12 source `_contribution_meta.yaml` "
                "files in the manifest, compute first-commit date+short-sha per "
                "source contribution directory, write nested output meta with "
                "`tasktorrent_version: <YYYY-MM-DD-shortsha>` added. No other "
                "fields modified. No KB content touched. See "
                "scripts/tasktorrent/_chunk37_backfill.py for the worker."
            ),
            "tasktorrent_version": self_version,
        }
    }
    (OUT_DIR / "_contribution_meta.yaml").write_text(
        yaml.safe_dump(self_meta, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print(f"\n{written}/{len(MANIFEST)} manifest entries backfilled.")
    print(f"Output: {OUT_DIR.relative_to(REPO_ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
