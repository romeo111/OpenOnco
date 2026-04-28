"""Lazy-load a per-disease KB module on top of an already-loaded core.

CSD-5B introduces a two-tier bundle model for the Pyodide demo:

    1. Core bundle  (openonco-engine-core.zip)  — Python code + schemas +
       validation + shared content (drugs, sources, biomarkers, tests,
       supportive_care, monitoring, workups, questionnaires,
       contraindications, mdt_skills, diseases, plus universal redflags
       and any indications/algorithms/regimens/RFs/BMA cells that don't
       pin to a single disease). Loaded immediately on /try.html ready.

    2. Per-disease bundle (disease/openonco-{slug}.zip) — disease-scoped
       indications, algorithms, regimens, redflags, biomarker_actionability
       cells. Fetched on demand once the patient's `disease_id` is known.

This module is the merge point. After Pyodide unpacks the per-disease
zip on top of the existing `knowledge_base/hosted/content/` tree
(via `pyodide.unpackArchive`), Python code calls `apply_disease_module()`
to invalidate the load cache so the next `generate_plan()` re-validates
with the freshly-arrived YAMLs included.

Server-side / test usage is symmetric: `load_disease_module()` extracts
a per-disease zip (path or bytes) into a target KB root on disk and then
calls `apply_disease_module()` to clear the load cache. Tests use this
to verify the split bundles round-trip cleanly.

The functions here are intentionally synchronous. In Pyodide the JS
side is responsible for the network fetch (via `fetch()`), and only
the bytes are handed to Python — so async-vs-sync is not the engine's
problem.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from knowledge_base.validation.loader import (
    clear_load_cache,
    load_content,
)


# Default location matches scripts/build_site.py: bundle index lives
# next to the core zip at docs/openonco-engine-index.json.
DEFAULT_INDEX_NAME = "openonco-engine-index.json"


def disease_bundle_basename(disease_id: str) -> str:
    """`DIS-DLBCL-NOS` → `openonco-dis-dlbcl-nos.zip`. Mirrors
    `scripts.build_site._disease_bundle_basename` so callers can compute
    the URL without a network round-trip to the index."""
    slug = disease_id.lower().replace("_", "-")
    return f"openonco-{slug}.zip"


def load_bundle_index(index_path: Path | str) -> dict:
    """Read the bundle index JSON written by `scripts.build_site.bundle_engine`.

    Returns the parsed dict — `{core, core_version, monolithic, diseases,
    disease_versions}` — so callers can resolve a disease_id to the URL
    of its per-disease bundle.
    """
    p = Path(index_path)
    return json.loads(p.read_text(encoding="utf-8"))


def url_for_disease(index: dict, disease_id: str) -> str | None:
    """Look up the per-disease bundle URL in a loaded index. Returns
    None when the disease has no per-disease module (its content is
    entirely in core)."""
    return (index.get("diseases") or {}).get(disease_id.upper())


def load_disease_module(
    bundle: bytes | Path | str,
    *,
    kb_root: Path | str,
) -> list[Path]:
    """Extract a per-disease zip into an existing KB root on disk.

    `bundle` may be raw bytes (the network response in Pyodide) or a
    filesystem path to a previously-downloaded zip. `kb_root` is the
    directory that contains `knowledge_base/` — typically the parent
    of the unpacked core bundle. In the Pyodide filesystem and in
    tests this is the working directory where `pyodide.unpackArchive`
    placed the core.

    Returns the list of YAML file paths newly extracted, so callers
    can verify the merge produced the entities they expected.

    This function does NOT clear the loader cache by itself — call
    `apply_disease_module()` afterwards (or use the all-in-one
    `merge_disease_module()`) so the cache invalidation is explicit.
    """
    if isinstance(bundle, (bytes, bytearray, memoryview)):
        zf = zipfile.ZipFile(io.BytesIO(bytes(bundle)))
    else:
        zf = zipfile.ZipFile(Path(bundle))

    extracted: list[Path] = []
    root = Path(kb_root)
    try:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))
            if target.suffix == ".yaml":
                extracted.append(target)
    finally:
        zf.close()
    return extracted


def apply_disease_module(content_root: Path | str) -> dict:
    """Drop the load cache and re-run `load_content()` against the
    given hosted/content/ root. Returns the resulting LoadResult as a
    dict-of-dicts summary suitable for printing back to the JS layer
    (counts by entity type + ok flag).

    Call this after every per-disease module extraction so the next
    `generate_plan()` sees the new entities.
    """
    clear_load_cache()
    result = load_content(Path(content_root))
    by_type: dict[str, int] = {}
    for info in result.entities_by_id.values():
        by_type[info["type"]] = by_type.get(info["type"], 0) + 1
    return {
        "ok": result.ok,
        "total_entities": len(result.entities_by_id),
        "by_type": by_type,
        "schema_errors": len(result.schema_errors),
        "ref_errors": len(result.ref_errors),
        "contract_errors": len(result.contract_errors),
    }


def merge_disease_module(
    bundle: bytes | Path | str,
    *,
    kb_root: Path | str,
    content_subpath: str = "knowledge_base/hosted/content",
) -> dict:
    """Convenience: extract a per-disease bundle AND invalidate the load
    cache in one call. Returns a `{extracted: [...paths], summary: {...}}`
    dict where `summary` is `apply_disease_module()`'s output.

    `kb_root` is the root the zip was authored against — typically the
    same directory you pass to `pyodide.unpackArchive` for the core. The
    per-disease zip's archive paths are `knowledge_base/hosted/content/...`,
    so we pass `<kb_root>/<content_subpath>` to the validator afterwards.
    """
    extracted = load_disease_module(bundle, kb_root=kb_root)
    summary = apply_disease_module(Path(kb_root) / content_subpath)
    return {
        "extracted": [str(p) for p in extracted],
        "summary": summary,
    }


def lazy_load_disease(
    disease_id: str,
    *,
    bundle_dir: Path | str,
    kb_root: Path | str,
    content_subpath: str = "knowledge_base/hosted/content",
) -> dict:
    """Pure-Python entry point used by tests and any non-Pyodide caller.

    Resolves `disease_id` against the bundle index living under
    `bundle_dir`, locates the matching per-disease zip on disk, and
    merges it into `kb_root`. Returns the same shape as
    `merge_disease_module()` (with an extra `disease_id` key for
    tracing).

    In Pyodide the JS side does the fetch + `pyodide.unpackArchive`
    itself, then calls `apply_disease_module()` directly — this helper
    is for environments where reading from local disk is fine.
    """
    bundle_dir = Path(bundle_dir)
    index = load_bundle_index(bundle_dir / DEFAULT_INDEX_NAME)
    rel_url = url_for_disease(index, disease_id)
    if rel_url is None:
        # Nothing to lazy-load — disease's content is entirely in core.
        summary = apply_disease_module(Path(kb_root) / content_subpath)
        return {
            "disease_id": disease_id,
            "extracted": [],
            "summary": summary,
            "note": "no per-disease bundle (content fully in core)",
        }
    bundle_path = bundle_dir / rel_url
    if not bundle_path.is_file():
        raise FileNotFoundError(
            f"Per-disease bundle missing for {disease_id}: expected {bundle_path}"
        )
    out = merge_disease_module(
        bundle_path,
        kb_root=kb_root,
        content_subpath=content_subpath,
    )
    out["disease_id"] = disease_id
    return out
