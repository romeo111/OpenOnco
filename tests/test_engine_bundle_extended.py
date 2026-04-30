"""Extended tests for the CSD-5B core + per-disease bundle split.

Complements `test_engine_bundle_optimization.py` with finer-grained
checks on:

  Section A — Per-disease bundle integrity (cross-disease leakage,
              positive presence of indications & algorithms, per-bundle
              size ceiling, per-disease index coverage).
  Section B — Lazy-load API contract (entity dict shape, unknown-disease
              graceful path, core+disease entity merge).
  Section C — Backward-compatibility (monolithic still produced and
              loadable through the standard validation loader).
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml

from scripts.build_site import bundle_engine
from knowledge_base.engine.lazy_loader import (
    apply_disease_module,
    lazy_load_disease,
    load_bundle_index,
    merge_disease_module,
)
from knowledge_base.validation.loader import (
    clear_load_cache,
    load_content,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_CONTENT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


@pytest.fixture(scope="module")
def bundle_out(tmp_path_factory) -> dict:
    """Build the core + per-disease bundles once per module."""
    out = tmp_path_factory.mktemp("docs_bundle_ext")
    info = bundle_engine(out)
    info["_dir"] = out
    return info


def _names(zp: Path) -> set[str]:
    with zipfile.ZipFile(zp) as zf:
        return set(zf.namelist())


def _unpack(zp: Path, target: Path) -> None:
    with zipfile.ZipFile(zp) as zf:
        zf.extractall(target)


# ──────────────────────────────────────────────────────────────────────────
# Section A — Per-disease bundle integrity
# ──────────────────────────────────────────────────────────────────────────


def test_per_disease_bundle_contains_only_relevant_entities(
    bundle_out: dict,
) -> None:
    """The DIS-DLBCL-NOS bundle must not contain IND-CRC-* entities (or
    any other unrelated disease's indications)."""
    bundle = Path(bundle_out["_dir"]) / "disease" / "openonco-dis-dlbcl-nos.zip"
    assert bundle.is_file(), "DLBCL bundle expected"
    leaked: list[str] = []
    with zipfile.ZipFile(bundle) as zf:
        for name in zf.namelist():
            base = name.rsplit("/", 1)[-1].lower()
            # Heuristic: any *_crc_* file in indications/algorithms/redflags
            # would be a cross-disease leak.
            if (
                base.startswith(("ind_crc_", "algo_crc_", "rf_crc_"))
                or base.startswith(("ind_nsclc_", "algo_nsclc_", "rf_nsclc_"))
                or base.startswith(("ind_breast_", "algo_breast_", "rf_breast_"))
            ):
                leaked.append(name)
    assert not leaked, f"unrelated disease entities in DLBCL bundle: {leaked[:5]}"


def test_per_disease_bundle_contains_disease_indications(
    bundle_out: dict,
) -> None:
    """The DIS-DLBCL-NOS bundle must carry ≥1 IND-DLBCL-* indication."""
    bundle = Path(bundle_out["_dir"]) / "disease" / "openonco-dis-dlbcl-nos.zip"
    inds: list[str] = []
    with zipfile.ZipFile(bundle) as zf:
        for name in zf.namelist():
            if "/indications/" in name and name.endswith(".yaml"):
                text = zf.read(name).decode("utf-8")
                # Confirm it's a DLBCL indication by ID prefix
                for line in text.splitlines():
                    line = line.strip()
                    if line.startswith("id:") and "IND-DLBCL" in line.upper():
                        inds.append(name)
                        break
    assert len(inds) >= 1, (
        "DLBCL bundle must contain ≥1 IND-DLBCL-* entity, got "
        f"{len(inds)}"
    )


def test_per_disease_bundle_contains_disease_algorithms(
    bundle_out: dict,
) -> None:
    """The DIS-DLBCL-NOS bundle must carry ≥1 ALGO-DLBCL-* algorithm."""
    bundle = Path(bundle_out["_dir"]) / "disease" / "openonco-dis-dlbcl-nos.zip"
    algos: list[str] = []
    with zipfile.ZipFile(bundle) as zf:
        for name in zf.namelist():
            if "/algorithms/" in name and name.endswith(".yaml"):
                text = zf.read(name).decode("utf-8")
                for line in text.splitlines():
                    line = line.strip()
                    if line.startswith("id:") and "ALGO-DLBCL" in line.upper():
                        algos.append(name)
                        break
    assert len(algos) >= 1, (
        "DLBCL bundle must contain ≥1 ALGO-DLBCL-* entity, got "
        f"{len(algos)}"
    )


def test_per_disease_bundle_size_under_300kb(bundle_out: dict) -> None:
    """Hard ceiling: every per-disease bundle is ≤300 KB compressed.

    Surfaces the actual size in the failure message so a regression
    report is actionable without needing a re-run.
    """
    disease_dir = Path(bundle_out["_dir"]) / "disease"
    over = []
    for zp in sorted(disease_dir.glob("openonco-*.zip")):
        size = zp.stat().st_size
        if size > 300_000:
            over.append((zp.name, size))
    assert not over, (
        f"per-disease bundles exceed 300 KB ceiling: "
        f"{[(n, f'{s/1024:.1f} KB') for n, s in over]}"
    )


def test_per_disease_bundle_index_lists_all_diseases(
    bundle_out: dict,
) -> None:
    """Every DIS-* present in `knowledge_base/hosted/content/diseases/`
    that has at least one disease-scoped artifact (indication / algorithm /
    redflag / BMA cell) must show up in the bundle index. Catches the
    failure mode where a freshly added disease's content fails to
    attribute and is silently dropped from the per-disease layer."""
    index = load_bundle_index(
        Path(bundle_out["_dir"]) / "openonco-engine-index.json"
    )
    indexed = set((index.get("diseases") or {}).keys())

    # Load all DIS-* IDs that appear with disease-scoped artifacts in the
    # KB. We use the bundle build to determine "has artifacts" — the
    # index itself is the ground truth for that question, but we want a
    # cross-check: re-derive expected diseases from the disease YAMLs
    # plus a heuristic on the indication/algorithm filenames.
    diseases_dir = KB_CONTENT / "diseases"
    expected_with_content: set[str] = set()
    for p in diseases_dir.glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        did = data.get("id")
        if not did or not did.startswith("DIS-"):
            continue
        # Heuristic: look for a matching slug in indications/ or algorithms/
        slug = did.lower().replace("dis-", "").replace("-", "_")
        # First fragment is usually the meaningful one
        slug_head = slug.split("_")[0]
        ind_hits = list(
            (KB_CONTENT / "indications").glob(f"ind_{slug_head}*.yaml")
        )
        algo_hits = list(
            (KB_CONTENT / "algorithms").glob(f"algo_{slug_head}*.yaml")
        )
        if ind_hits or algo_hits:
            expected_with_content.add(did)

    # Index must cover every DIS-* with content. Allow extras in the index
    # (the build's attribution is the source of truth and may pick up
    # diseases our heuristic missed).
    missing = expected_with_content - indexed
    assert not missing, (
        f"index missing per-disease bundles for diseases that have "
        f"indications/algorithms in the KB: {sorted(missing)}"
    )


# ──────────────────────────────────────────────────────────────────────────
# Section B — Lazy load
# ──────────────────────────────────────────────────────────────────────────


def test_lazy_load_disease_returns_entity_dict(
    bundle_out: dict, tmp_path: Path
) -> None:
    """Contract: `lazy_load_disease(...)` returns a dict with at minimum
    `disease_id`, `extracted` (list), and `summary` (dict with `by_type`)."""
    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack(out_dir / "openonco-engine-core.zip", target)

    clear_load_cache()
    result = lazy_load_disease(
        "DIS-DLBCL-NOS", bundle_dir=out_dir, kb_root=target
    )
    assert isinstance(result, dict)
    assert result.get("disease_id") == "DIS-DLBCL-NOS"
    assert isinstance(result.get("extracted"), list)
    assert result["extracted"], "no files extracted for DLBCL"
    summary = result.get("summary")
    assert isinstance(summary, dict)
    assert isinstance(summary.get("by_type"), dict)
    assert "indications" in summary["by_type"], (
        "merged summary should report at least one indications entry "
        f"after DLBCL merge — got {summary['by_type']}"
    )


def test_lazy_load_disease_unknown_returns_none_or_empty(
    bundle_out: dict, tmp_path: Path
) -> None:
    """Asking for a disease that has no per-disease bundle (its content
    is fully in core) must NOT raise — it should gracefully return a
    summary with an empty `extracted` list and a `note` field."""
    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack(out_dir / "openonco-engine-core.zip", target)

    clear_load_cache()
    result = lazy_load_disease(
        "DIS-DOES-NOT-EXIST",
        bundle_dir=out_dir,
        kb_root=target,
    )
    # Graceful path: no extracted files; note explains why
    assert isinstance(result, dict)
    assert result.get("extracted") == []
    assert "note" in result, (
        "unknown disease should surface a 'note' field explaining the "
        "graceful no-op path"
    )


def test_lazy_load_disease_merges_with_core(
    bundle_out: dict, tmp_path: Path
) -> None:
    """After core unpack + DLBCL lazy-load, the merged loader output must
    contain BOTH core entities (drugs / sources) AND DLBCL-specific
    entities (the DLBCL indication YAML)."""
    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack(out_dir / "openonco-engine-core.zip", target)

    clear_load_cache()
    result = lazy_load_disease(
        "DIS-DLBCL-NOS", bundle_dir=out_dir, kb_root=target
    )
    by_type = result["summary"]["by_type"]
    # Core-only entity types must still be present after the merge
    assert by_type.get("drugs", 0) > 0, "drugs (core) missing post-merge"
    assert by_type.get("sources", 0) > 0, "sources (core) missing post-merge"
    # Disease-specific type appears too
    assert by_type.get("indications", 0) > 0, (
        "indications (DLBCL) missing post-merge"
    )
    # And the DLBCL file is on disk where the loader will find it
    content_root = target / "knowledge_base" / "hosted" / "content"
    dlbcl_files = list(
        (content_root / "indications").glob("ind_dlbcl_*.yaml")
    )
    assert dlbcl_files, "no DLBCL indication YAMLs found post-merge"


# Section C (back-compat for monolithic bundle) was removed 2026-04-30:
# the legacy `openonco-engine.zip` was retired in CSD-9C (2026-04-27,
# scripts/build_site.py:272-278 deletes any stale monolithic on build).
# Tests that asserted its presence have been deleted; the lazy-load
# core + per-disease bundles are tested in Sections A and B above and
# in test_engine_bundle_optimization.py.
