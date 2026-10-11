"""Read-only audit: python -m scripts.profile_engine_bundle --output report.json.

Analyses ZIP composition, including the legacy compatibility core archive.
The preferred tar.gz transport is recorded separately in the bundle index.
Never rebuilds, extracts or changes clinical data.
Packaging attribution is not clinical validation or permission to remove files.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path
import zipfile
from scripts.build_site import _DISEASE_SCOPED_DIRS, _disease_id_for_yaml

BUNDLE = Path(__file__).resolve().parent.parent / "docs/openonco-engine-core.zip"
CORE_BUDGET_BYTES = 4_250_000


def profile_bundle(bundle: Path) -> dict:
    """Account for actual compressed bytes without double-counted estimates."""
    groups = defaultdict(lambda: {"files": 0, "compressed_bytes": 0})
    diseases = defaultdict(lambda: {"files": 0, "compressed_bytes": 0})
    files = []
    attributed_bytes = 0
    with zipfile.ZipFile(bundle) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            parts = info.filename.split("/")
            content = parts[:3] == ["knowledge_base", "hosted", "content"] and len(parts) >= 5
            group = f"content/{parts[3]}" if content else "/".join(parts[:2])
            groups[group]["files"] += 1
            groups[group]["compressed_bytes"] += info.compress_size
            disease = None
            if content and parts[3] in _DISEASE_SCOPED_DIRS and info.filename.endswith(".yaml"):
                disease = _disease_id_for_yaml(archive.read(info).decode("utf-8"), info.filename)
            if disease:
                attributed_bytes += info.compress_size
                diseases[disease]["files"] += 1
                diseases[disease]["compressed_bytes"] += info.compress_size
            files.append({"path": info.filename, "compressed_bytes": info.compress_size,
                          "uncompressed_bytes": info.file_size, "single_disease": disease})
    payload = sum(item["compressed_bytes"] for item in files)
    size = bundle.stat().st_size
    return {
        "bundle": str(bundle.resolve()), "archive_bytes": size,
        "compressed_payload_bytes": payload, "zip_overhead_bytes": size - payload,
        "core_budget_bytes": CORE_BUDGET_BYTES,
        "over_budget_bytes": max(0, size - CORE_BUDGET_BYTES), "files": len(files),
        "single_disease_scoped_payload_bytes": attributed_bytes,
        "other_payload_bytes": payload - attributed_bytes,
        "groups": dict(sorted(groups.items())),
        "single_disease_scoped_groups": dict(sorted(diseases.items())),
        "largest_files": sorted(files, key=lambda item: (-item["compressed_bytes"], item["path"]))[:20],
        "limitations": [
            "Single-disease files may be required transitive dependencies of shared entities.",
            "Other payload includes shared content, disease metadata, code and non-YAML assets.",
            "Byte counts do not prove clinical validity, first-load latency or removability.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=BUNDLE)
    parser.add_argument("--output", type=Path, help="Optional JSON report; otherwise print JSON")
    parser.add_argument("--check-budget", action="store_true")
    args = parser.parse_args(argv)
    if not args.bundle.is_file():
        parser.error(f"Archive does not exist: {args.bundle}. Build separately; this audit never rebuilds.")
    if args.output and args.output.resolve() == args.bundle.resolve():
        parser.error("Report output must not overwrite the archive.")
    report = profile_bundle(args.bundle)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(json.dumps({key: report[key] for key in (
            "archive_bytes", "files", "over_budget_bytes", "single_disease_scoped_payload_bytes"
        )}))
    else:
        print(payload, end="")
    return int(args.check_budget and report["over_budget_bytes"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
