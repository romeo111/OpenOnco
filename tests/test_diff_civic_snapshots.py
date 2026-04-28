"""Unit tests for scripts/diff_civic_snapshots.py.

Covers added/removed/changed detection, level/direction sensitivity,
intersection with the actionability_lookup biomarker set, and the
markdown rendering surface.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.diff_civic_snapshots import (  # noqa: E402
    diff_snapshots,
    intersect_with_actionability,
    load_actionability_lookup_pairs,
    load_snapshot,
    main as diff_main,
    render_markdown,
)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _item(
    ev_id,
    *,
    gene="BRAF",
    variant="V600E",
    level="A",
    direction="Supports",
    significance="Sensitivity/Response",
    therapies=None,
    disease="Hairy Cell Leukemia",
):
    return {
        "id": str(ev_id),
        "gene": gene,
        "variant": variant,
        "molecular_profile": f"{gene} {variant}",
        "evidence_level": level,
        "evidence_direction": direction,
        "significance": significance,
        "therapies": list(therapies or []),
        "disease": disease,
    }


def _write_snapshot(path: Path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_id": "SRC-CIVIC",
        "snapshot_date": "2026-04-25",
        "evidence_items": items,
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture
def snapshots(tmp_path):
    old_items = [
        _item(1, gene="BRAF", variant="V600E", level="A"),
        _item(2, gene="JAK2", variant="V617F", level="B"),
        _item(3, gene="EGFR", variant="L858R", level="A", therapies=["Erlotinib"]),
        _item(4, gene="KRAS", variant="G12C", level="B", direction="Supports"),
    ]
    new_items = [
        # 1 unchanged
        _item(1, gene="BRAF", variant="V600E", level="A"),
        # 2 changed: level B → A (level promotion)
        _item(2, gene="JAK2", variant="V617F", level="A"),
        # 3 removed
        # 4 changed: direction Supports → Does Not Support (resistance flip)
        _item(4, gene="KRAS", variant="G12C", level="B", direction="Does Not Support"),
        # 5 added — touches actionability_lookup
        _item(5, gene="BRAF", variant="V600E", level="C"),
        # 6 added — does NOT touch actionability_lookup
        _item(6, gene="FOO", variant="X1Y", level="D"),
    ]
    old_path = tmp_path / "old.yaml"
    new_path = tmp_path / "new.yaml"
    _write_snapshot(old_path, old_items)
    _write_snapshot(new_path, new_items)
    return old_path, new_path


@pytest.fixture
def biomarkers_dir(tmp_path):
    """Two BIO-* files declaring actionability_lookup pairs."""
    bdir = tmp_path / "biomarkers"
    bdir.mkdir()
    (bdir / "bio_braf_v600e.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "BIO-BRAF-V600E",
                "actionability_lookup": {"gene": "BRAF", "variant": "V600E"},
            }
        ),
        encoding="utf-8",
    )
    (bdir / "bio_egfr_l858r.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "BIO-EGFR-L858R",
                "actionability_lookup": {"gene": "EGFR", "variant": "L858R"},
            }
        ),
        encoding="utf-8",
    )
    # Skip-this: no actionability_lookup at all.
    (bdir / "bio_unrelated.yaml").write_text(
        yaml.safe_dump({"id": "BIO-OTHER"}), encoding="utf-8"
    )
    return bdir


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------


def test_load_snapshot_indexes_by_id(snapshots):
    old_path, _ = snapshots
    idx = load_snapshot(old_path)
    assert set(idx.keys()) == {"1", "2", "3", "4"}
    assert idx["1"]["gene"] == "BRAF"


def test_diff_added_detection(snapshots):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    added_ids = {item["id"] for item in diff["added"]}
    assert added_ids == {"5", "6"}


def test_diff_removed_detection(snapshots):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    removed_ids = {item["id"] for item in diff["removed"]}
    assert removed_ids == {"3"}


def test_diff_level_change_detection(snapshots):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    changed_ids = {entry["id"] for entry in diff["changed"]}
    # EID 2 (level change) and EID 4 (direction change) are both reported.
    assert "2" in changed_ids
    # EID 2's old/new differ on evidence_level.
    entry = next(e for e in diff["changed"] if e["id"] == "2")
    assert entry["old"]["evidence_level"] == "B"
    assert entry["new"]["evidence_level"] == "A"


def test_diff_direction_change_detection(snapshots):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    changed_ids = {entry["id"] for entry in diff["changed"]}
    assert "4" in changed_ids
    entry = next(e for e in diff["changed"] if e["id"] == "4")
    assert entry["old"]["evidence_direction"] == "Supports"
    assert entry["new"]["evidence_direction"] == "Does Not Support"


def test_diff_therapies_change_detection(tmp_path):
    """An item whose therapies list changes is flagged as changed."""
    old = tmp_path / "o.yaml"
    new = tmp_path / "n.yaml"
    _write_snapshot(old, [_item(10, therapies=["Vemurafenib"])])
    _write_snapshot(new, [_item(10, therapies=["Vemurafenib", "Dabrafenib"])])
    diff = diff_snapshots(load_snapshot(old), load_snapshot(new))
    assert len(diff["changed"]) == 1
    assert diff["changed"][0]["id"] == "10"


def test_diff_no_change_when_only_unwatched_field_differs(tmp_path):
    """A diff in `rating` (not in WATCHED_FIELDS) is NOT a change."""
    old = tmp_path / "o.yaml"
    new = tmp_path / "n.yaml"
    base = _item(20)
    base["rating"] = "3"
    _write_snapshot(old, [base])
    base2 = dict(base)
    base2["rating"] = "5"
    _write_snapshot(new, [base2])
    diff = diff_snapshots(load_snapshot(old), load_snapshot(new))
    assert diff["added"] == []
    assert diff["removed"] == []
    assert diff["changed"] == []


def test_load_actionability_lookup_pairs(biomarkers_dir):
    pairs = load_actionability_lookup_pairs(biomarkers_dir)
    assert pairs == {("BRAF", "V600E"), ("EGFR", "L858R")}


def test_load_actionability_lookup_pairs_missing_dir(tmp_path):
    """Missing dir returns empty set, not an error."""
    pairs = load_actionability_lookup_pairs(tmp_path / "does-not-exist")
    assert pairs == set()


def test_intersection_with_actionability(snapshots, biomarkers_dir):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    pairs = load_actionability_lookup_pairs(biomarkers_dir)
    inter = intersect_with_actionability(diff, pairs)

    # Added: EID 5 is BRAF V600E (in lookup); EID 6 is FOO X1Y (not in lookup).
    added_ids = {i["id"] for i in inter["added"]}
    assert added_ids == {"5"}

    # Removed: EID 3 is EGFR L858R — IS in lookup.
    removed_ids = {i["id"] for i in inter["removed"]}
    assert removed_ids == {"3"}

    # Changed: EID 2 is JAK2 V617F (NOT in lookup); EID 4 is KRAS G12C (NOT in lookup).
    # So intersect of changed = empty.
    assert inter["changed"] == []


def test_render_markdown_summary_counts(snapshots, biomarkers_dir):
    old_path, new_path = snapshots
    diff = diff_snapshots(load_snapshot(old_path), load_snapshot(new_path))
    pairs = load_actionability_lookup_pairs(biomarkers_dir)
    inter = intersect_with_actionability(diff, pairs)
    md = render_markdown(old_path, new_path, diff, inter)
    assert "Added: **2**" in md
    assert "Removed: **1**" in md
    assert "Changed" in md and "**2**" in md
    # Special-attention header present.
    assert "actionability_lookup" in md


def test_render_markdown_no_diff_short_circuits(tmp_path):
    """Identical snapshots emit a `_No differences detected._` block."""
    p = tmp_path / "s.yaml"
    _write_snapshot(p, [_item(1)])
    snap = load_snapshot(p)
    diff = diff_snapshots(snap, snap)
    inter = intersect_with_actionability(diff, set())
    md = render_markdown(p, p, diff, inter)
    assert "No differences detected" in md
    assert "Added: **0**" in md


def test_render_markdown_flags_resistance(tmp_path, biomarkers_dir):
    """Items with `Does Not Support` direction get a ⚠️ marker."""
    old = tmp_path / "o.yaml"
    new = tmp_path / "n.yaml"
    _write_snapshot(old, [])
    _write_snapshot(
        new,
        [_item(99, gene="BRAF", variant="V600E", direction="Does Not Support")],
    )
    diff = diff_snapshots(load_snapshot(old), load_snapshot(new))
    pairs = load_actionability_lookup_pairs(biomarkers_dir)
    inter = intersect_with_actionability(diff, pairs)
    md = render_markdown(old, new, diff, inter)
    assert "⚠️" in md


def test_main_writes_output_file(tmp_path, snapshots, biomarkers_dir):
    old_path, new_path = snapshots
    out = tmp_path / "diff.md"
    rc = diff_main(
        [
            str(old_path),
            str(new_path),
            "--out",
            str(out),
            "--biomarkers-dir",
            str(biomarkers_dir),
        ]
    )
    assert rc == 0
    assert out.is_file()
    body = out.read_text(encoding="utf-8")
    assert "CIViC snapshot diff" in body


def test_main_returns_zero_on_missing_old(tmp_path, snapshots):
    """Informational tool — missing input is logged but exit is still 0."""
    _, new_path = snapshots
    rc = diff_main([str(tmp_path / "nope.yaml"), str(new_path)])
    assert rc == 0
