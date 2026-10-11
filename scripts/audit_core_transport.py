"""Validate the shipped compressed core without extraction or rebuilding."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
import zipfile

CORE_BUDGET_BYTES = 4_250_000


def audit_core_transport(site: Path) -> dict:
    index = json.loads((site / "openonco-engine-index.json").read_text(encoding="utf-8"))
    if not isinstance(index, dict):
        raise ValueError("Invalid bundle index object")
    expected = {"core": "openonco-engine-core.zip", "core_compressed": "openonco-engine-core.tar.gz"}
    for key, filename in expected.items():
        if index.get(key) != filename:
            raise ValueError(f"Invalid {key} archive path")
        version = index.get(key + "_version")
        if not isinstance(version, str) or not re.fullmatch(r"[a-f0-9]{12}", version):
            raise ValueError(f"Invalid {key} version")
        content = (site / filename).read_bytes()
        if hashlib.sha256(content).hexdigest()[:12] != version:
            raise ValueError(f"Hash mismatch: {filename}")
    compressed = site / expected["core_compressed"]
    size = compressed.stat().st_size
    if size >= CORE_BUDGET_BYTES:
        raise ValueError(f"Preferred core exceeds transfer budget: {size} >= {CORE_BUDGET_BYTES}")
    with zipfile.ZipFile(site / expected["core"]) as legacy, tarfile.open(compressed, "r:gz") as stream:
        members = stream.getmembers()
        names = [member.name for member in members]
        original_names = legacy.namelist()
        if len(set(names)) != len(names) or len(set(original_names)) != len(original_names):
            raise ValueError("Duplicate archive member")
        if set(names) != set(original_names):
            raise ValueError("Archive member sets differ")
        if not names:
            raise ValueError("Empty core archive")
        for member in members:
            path = member.name
            if not member.isfile() or not path.startswith("knowledge_base/") or ".." in path.split("/") or "\\" in path:
                raise ValueError(f"Unsafe archive member: {path}")
            with stream.extractfile(member) as source:
                if source.read() != legacy.read(path):
                    raise ValueError(f"Archive content differs: {path}")
    return {"status": "ok", "files": len(names), "preferred_core_bytes": size,
            "core_budget_bytes": CORE_BUDGET_BYTES, "preferred_core_version": index["core_compressed_version"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path(__file__).resolve().parent.parent / "docs")
    args = parser.parse_args(argv)
    try:
        report = audit_core_transport(args.site_dir)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "failed", "error": str(error)}))
        return 1
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
