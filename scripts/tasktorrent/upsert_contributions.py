"""Upsert reviewed sidecar contributions into hosted/content/.

Run by maintainers ONLY, after PR review, with --confirm. Strips the
`_contribution` wrapper from each sidecar and writes the payload to the
appropriate hosted-content directory.

This script does NOT bypass clinical review. It is the mechanical step
that follows maintainer + Clinical Co-Lead signoff. Default mode is
--dry-run; --confirm is required to actually write files.

Per CHARTER §6.1, claim-bearing upserts (BMA, Indication, Drug with
clinical claims, RedFlag) require two of three Clinical Co-Lead
signoffs recorded in `_contribution.notes_for_reviewer` or in the PR
review comments. This script does not enforce that gate — it trusts
the maintainer who runs it. Provenance is captured in the
`upsert-log-<timestamp>.md` written next to the chunk dir.

Usage:
    python -m scripts.tasktorrent.upsert_contributions <chunk-id>          # dry-run
    python -m scripts.tasktorrent.upsert_contributions <chunk-id> --confirm
    python -m scripts.tasktorrent.upsert_contributions <chunk-id> --diff   # show diff vs hosted

Exit 0 on success, 1 on any error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"
HOSTED_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

# Map sidecar filename prefix → hosted-content subdir.
PREFIX_TO_DIR = {
    "bma_": "biomarker_actionability",
    "bio_": "biomarkers",
    "drug_": "drugs",
    "ind_": "indications",
    "src_": "sources",          # in-place source upsert (recency refresh,
                                # license update, etc) — keep filename
    "source_stub_": "sources",  # source stubs land in sources/, but the
                                # filename will be normalized to src_*.yaml
}


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _dump_yaml(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            payload,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


def _hosted_path_for(sidecar_path: Path, payload: dict) -> Path | None:
    """Determine the hosted-content path for a given sidecar."""
    name = sidecar_path.name
    for prefix, subdir in PREFIX_TO_DIR.items():
        if not name.startswith(prefix):
            continue
        if prefix == "source_stub_":
            entity_id = payload.get("id", "")
            slug = entity_id.lower().replace("src-", "src_").replace("-", "_")
            return HOSTED_ROOT / subdir / f"{slug}.yaml"
        # bma_ / bio_ / drug_ / ind_: keep filename, just relocate
        return HOSTED_ROOT / subdir / name
    return None


def _strip_wrapper(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k != "_contribution"}


def _sidecar_files(chunk_dir: Path) -> list[Path]:
    return sorted(
        p for p in chunk_dir.iterdir()
        if p.is_file()
        and p.suffix == ".yaml"
        and p.name not in {"_contribution_meta.yaml"}
    )


def _diff_existing(payload: dict, hosted_path: Path) -> str:
    if not hosted_path.exists():
        return "(new file, no diff)"
    try:
        existing_text = hosted_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return f"(could not read existing: {exc})"
    new_text = yaml.safe_dump(
        payload, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    diff = difflib.unified_diff(
        existing_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=str(hosted_path.relative_to(REPO_ROOT)),
        tofile=f"(upsert from sidecar)",
        n=3,
    )
    return "".join(diff) or "(no textual diff)"


def _upsert_chunk(chunk_id: str, confirm: bool, show_diff: bool) -> int:
    chunk_dir = CONTRIB_ROOT / chunk_id
    if not chunk_dir.exists():
        print(f"contributions/{chunk_id}/ does not exist", file=sys.stderr)
        return 1

    sidecars = _sidecar_files(chunk_dir)
    if not sidecars:
        print(f"contributions/{chunk_id}/ has no payloads", file=sys.stderr)
        return 1

    print(f"Found {len(sidecars)} sidecar(s) in contributions/{chunk_id}/")
    log_lines: list[str] = []
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    log_lines.append(f"# Upsert log: {chunk_id} ({timestamp})\n")
    log_lines.append(f"Mode: {'CONFIRM (writes applied)' if confirm else 'DRY-RUN (no writes)'}\n\n")

    for sc in sidecars:
        rel = sc.relative_to(REPO_ROOT)
        try:
            doc = _load_yaml(sc)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL [{rel}] YAML parse: {exc}")
            log_lines.append(f"- {rel}: YAML parse error: {exc}\n")
            continue
        if not isinstance(doc, dict):
            print(f"  FAIL [{rel}] top-level not a mapping")
            log_lines.append(f"- {rel}: top-level not a mapping\n")
            continue
        payload = _strip_wrapper(doc)
        hosted_path = _hosted_path_for(sc, payload)
        if hosted_path is None:
            print(f"  SKIP [{rel}] unknown prefix; not auto-routed")
            log_lines.append(f"- {rel}: SKIP unknown prefix\n")
            continue

        if show_diff:
            print(f"\n--- diff for {rel} -> {hosted_path.relative_to(REPO_ROOT)} ---")
            print(_diff_existing(payload, hosted_path))

        action = "UPDATE" if hosted_path.exists() else "CREATE"
        if confirm:
            _dump_yaml(payload, hosted_path)
            print(f"  {action} [{rel}] -> {hosted_path.relative_to(REPO_ROOT)}")
            log_lines.append(f"- {rel}: {action} -> {hosted_path.relative_to(REPO_ROOT)}\n")
        else:
            print(f"  {action} (dry-run) [{rel}] -> {hosted_path.relative_to(REPO_ROOT)}")
            log_lines.append(f"- {rel}: {action} (dry-run)\n")

    log_path = chunk_dir / f"upsert-log-{timestamp}.md"
    log_path.write_text("".join(log_lines), encoding="utf-8")
    print(f"\nLog written to {log_path.relative_to(REPO_ROOT)}")
    if not confirm:
        print("Re-run with --confirm to apply changes.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("chunk_id", help="chunk-id directory under contributions/")
    parser.add_argument("--confirm", action="store_true", help="actually write files")
    parser.add_argument("--diff", action="store_true", help="show unified diff per file")
    args = parser.parse_args()
    return _upsert_chunk(args.chunk_id, args.confirm, args.diff)


if __name__ == "__main__":
    sys.exit(main())
