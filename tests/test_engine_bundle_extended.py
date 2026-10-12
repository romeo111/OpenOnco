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

import json
import zipfile
from pathlib import Path

import pytest
import yaml

from scripts.build_site import bundle_engine
from knowledge_base.engine import generate_plan, generate_diagnostic_brief
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


def test_per_disease_bundle_size_under_500kb(bundle_out: dict) -> None:
    """Hard ceiling: every per-disease bundle is ≤500 KB compressed.

    Surfaces the actual size in the failure message so a regression
    report is actionable without needing a re-run.
    """
    disease_dir = Path(bundle_out["_dir"]) / "disease"
    over = []
    for zp in sorted(disease_dir.glob("openonco-*.zip")):
        size = zp.stat().st_size
        if size > 500_000:
            over.append((zp.name, size))
    assert not over, (
        f"per-disease bundles exceed 500 KB ceiling: "
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
    # cross-check: use authored disease_id values rather than filename
    # prefixes ("pituitary" also matches unrelated Pituitary Blastoma).
    expected_with_content: set[str] = set()
    for p in list((KB_CONTENT / "indications").glob("*.yaml")) + list(
        (KB_CONTENT / "algorithms").glob("*.yaml")
    ):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        did = data.get("disease_id")
        if isinstance(did, str) and did.startswith("DIS-"):
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
    assert result['summary']['ok'], result['summary']
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


@pytest.mark.parametrize("example,disease_slug", [
    ("auto_dlbcl_nos.json", "dis-dlbcl-nos"),
    ("auto_crc.json", "dis-crc"),
    ("auto_breast.json", "dis-breast"),
    ("patient_nsclc_pdl1_low_chemo_io.json", "dis-nsclc"),
])
def test_lazy_loaded_disease_generates_same_plan_as_full_kb(
    bundle_out: dict, tmp_path: Path, example: str, disease_slug: str
) -> None:
    """A valid archive must produce a treatment plan, not just pass loader checks."""
    profile = json.loads(
        (REPO_ROOT / "examples" / example).read_text(encoding="utf-8")
    )
    full = generate_plan(profile, kb_root=KB_CONTENT)
    assert full.plan is not None and full.plan.tracks

    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack(out_dir / "openonco-engine-core.zip", target)
    _unpack(out_dir / "disease" / f"openonco-{disease_slug}.zip", target)
    clear_load_cache()
    partial = generate_plan(
        profile, kb_root=target / "knowledge_base" / "hosted" / "content"
    )

    assert partial.plan is not None and partial.plan.tracks, partial.warnings[:5]
    assert partial.default_indication_id == full.default_indication_id
    assert [track.indication_id for track in partial.plan.tracks] == [
        track.indication_id for track in full.plan.tracks
    ]
    assert partial.kb_resolved.get("reviewers") == full.kb_resolved.get("reviewers")
    assert partial.plan.variant_actionability == full.plan.variant_actionability


@pytest.mark.parametrize('histology', [None, 'squamous'])
def test_lazy_nsclc_bundle_preserves_histology_withholding(bundle_out, tmp_path, histology):
    profile = json.loads((REPO_ROOT / 'examples/patient_nsclc_pdl1_low_chemo_io.json').read_text(encoding='utf-8'))
    profile['findings']['histology'] = histology
    full = generate_plan(profile, kb_root=KB_CONTENT)
    target = tmp_path / 'kb_root'
    target.mkdir()
    out_dir = Path(bundle_out['_dir'])
    _unpack(out_dir / 'openonco-engine-core.zip', target)
    _unpack(out_dir / 'disease/openonco-dis-nsclc.zip', target)
    clear_load_cache()
    partial = generate_plan(profile, kb_root=target / 'knowledge_base/hosted/content')
    for result in (full, partial):
        assert result.plan is not None
        reason = 'profile_selection_withheld' if histology == 'squamous' else 'histology_selection_withheld'
        assert result.plan.knowledge_base_state[reason] is True
        assert result.plan.tracks == result.plan.sequencing_tracks == []
        assert result.default_indication_id is None
        assert result.warnings
    assert partial.plan.variant_actionability == full.plan.variant_actionability


@pytest.mark.parametrize("mutation", ["unlisted", "wrong_type"])
def test_partial_bundle_does_not_ignore_broken_reference(
    bundle_out: dict, tmp_path: Path, mutation: str
) -> None:
    profile = json.loads(
        (REPO_ROOT / "examples" / "auto_dlbcl_nos.json").read_text(encoding="utf-8")
    )
    target = tmp_path / "kb_root"
    target.mkdir()
    out_dir = Path(bundle_out["_dir"])
    _unpack(out_dir / "openonco-engine-core.zip", target)
    _unpack(out_dir / "disease" / "openonco-dis-dlbcl-nos.zip", target)
    content = target / "knowledge_base" / "hosted" / "content"
    manifest_path = content / "_bundle_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    clear_load_cache()
    loaded = load_content(content)
    deferred_id = next(
        eid for _, _, eid, target_type in loaded.missing_refs
        if eid in manifest["deferred_entities"] and target_type is not None
    )
    if mutation == "unlisted":
        manifest["deferred_entities"].pop(deferred_id)
    else:
        manifest["deferred_entities"][deferred_id]["type"] = "wrong_type"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    result = generate_plan(profile, kb_root=content)
    assert result.plan is None
    assert any(deferred_id in warning for warning in result.warnings)


def test_real_core_startup_defers_only_manifest_modules(bundle_out, tmp_path):
    from knowledge_base.validation.bundle import load_packaged_content

    target = tmp_path / 'core_startup'
    target.mkdir()
    _unpack(Path(bundle_out['_dir']) / 'openonco-engine-core.zip', target)
    content = target / 'knowledge_base/hosted/content'
    clear_load_cache()
    raw = load_content(content)
    assert raw.ref_errors, 'Fixture must exercise deferred references, not an already complete KB'
    startup = load_packaged_content(content, core_only=True)
    assert startup.ok, startup.ref_errors[:5]
    assert raw.ref_errors, 'Packaged validation must not mutate the strict loader cache'
    manifest = json.loads((content / '_bundle_manifest.json').read_text(encoding='utf-8'))
    _, _, missing_id, _ = next(item for item in raw.missing_refs if item[2] in manifest['deferred_entities'])
    active_disease = manifest['deferred_entities'][missing_id]['disease_id']
    incomplete = load_packaged_content(content, active_disease=active_disease)
    assert not incomplete.ok
    assert any(missing_id in message for _, message in incomplete.ref_errors)


@pytest.mark.parametrize('mutation', ['unlisted', 'wrong_type', 'malformed'])
def test_real_core_startup_rejects_damaged_manifest(bundle_out, tmp_path, mutation):
    from knowledge_base.validation.bundle import load_packaged_content

    target = tmp_path / 'damaged_core'
    target.mkdir()
    _unpack(Path(bundle_out['_dir']) / 'openonco-engine-core.zip', target)
    content = target / 'knowledge_base/hosted/content'
    clear_load_cache()
    raw = load_content(content)
    path = content / '_bundle_manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    missing_id = next(eid for _, _, eid, target_type in raw.missing_refs if eid in manifest['deferred_entities'] and target_type)
    if mutation == 'unlisted':
        manifest['deferred_entities'].pop(missing_id)
    elif mutation == 'wrong_type':
        manifest['deferred_entities'][missing_id]['type'] = 'sources'
    else:
        manifest['deferred_entities'] = []
    path.write_text(json.dumps(manifest), encoding='utf-8')
    assert not load_packaged_content(content, core_only=True).ok


@pytest.mark.parametrize('example', [
    'patient_diagnostic_lymphoma_suspect.json',
    'patient_diagnostic_lung_mass_smoker_prebiopsy.json',
])
def test_core_only_diagnostic_brief_matches_full_kb(bundle_out, tmp_path, example):
    patient = json.loads((REPO_ROOT / 'examples' / example).read_text(encoding='utf-8'))
    full = generate_diagnostic_brief(patient, kb_root=KB_CONTENT)
    assert full.diagnostic_plan is not None
    target = tmp_path / 'diagnostic_core'
    target.mkdir()
    _unpack(Path(bundle_out['_dir']) / 'openonco-engine-core.zip', target)
    clear_load_cache()
    partial = generate_diagnostic_brief(patient, kb_root=target / 'knowledge_base/hosted/content')
    assert partial.diagnostic_plan is not None, partial.warnings
    assert partial.matched_workup_id == full.matched_workup_id
    assert partial.diagnostic_plan.workup_steps == full.diagnostic_plan.workup_steps
    assert partial.diagnostic_plan.mandatory_questions == full.diagnostic_plan.mandatory_questions


# Section C (back-compat for monolithic bundle) was removed 2026-04-30:
# the legacy `openonco-engine.zip` was retired in CSD-9C (2026-04-27,
# scripts/build_site.py:272-278 deletes any stale monolithic on build).
# Tests that asserted its presence have been deleted; the lazy-load
# core + per-disease bundles are tested in Sections A and B above and
# in test_engine_bundle_optimization.py.
