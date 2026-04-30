"""PR4 — citation-verifier slice 1: SRC-* referential integrity tests.

These tests cover the loader's new pass that walks SRC-* citations
(structural FKs and inline narrative mentions) and reports unresolved
IDs with categorized hints.

The loader gates this behaviour on ``strict_source_refs``:
  - default (False) → contract_warnings (does not break ``result.ok``)
  - strict (True)   → ref_errors (breaks ``result.ok``)

The tests cover both paths plus three categories of unresolved IDs:
  - ``typo``  — Levenshtein ≤ 2 to a known SRC-* ID; "did you mean…?"
  - ``banned`` — matches CHARTER §2 ban list; "banned per CHARTER §2"
  - ``gap``    — neither; "file a source_stub_<id>.yaml"
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

import pytest

from knowledge_base.validation.loader import (
    BANNED_SOURCE_IDS,
    _categorize_unresolved_src,
    _levenshtein,
    clear_load_cache,
    load_content,
)

LIVE_KB = Path(__file__).parent.parent / "knowledge_base" / "hosted" / "content"
_UNRESOLVED_RE = re.compile(r"Unresolved citation ref '(SRC-[A-Z0-9_-]+)'")


# ---------------------------------------------------------------------------
# Fixture builders for synthetic mini-KBs.
# ---------------------------------------------------------------------------


def _write_source(root: Path, src_id: str, *, name: str | None = None) -> Path:
    """Write a minimal Source YAML stub that satisfies the Pydantic
    schema (only ``id`` / ``source_type`` / ``title`` are required).
    """
    sources_dir = root / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    p = sources_dir / f"{src_id.lower()}.yaml"
    p.write_text(
        textwrap.dedent(
            f"""\
            id: {src_id}
            source_type: guideline
            title: {name or src_id}
            """
        ),
        encoding="utf-8",
    )
    return p


def _write_regimen(
    root: Path,
    reg_id: str,
    *,
    sources: list[str],
    drug_ids: list[str] | None = None,
) -> Path:
    """Write a regimen citing the given SRC-* IDs in its top-level
    ``sources`` list."""
    reg_dir = root / "regimens"
    reg_dir.mkdir(parents=True, exist_ok=True)
    p = reg_dir / f"{reg_id.lower()}.yaml"
    components = drug_ids or ["DRUG-RITUXIMAB"]
    yaml_src = ["id: " + reg_id, "name: Test regimen", "components:"]
    for d in components:
        yaml_src.append(f"  - drug_id: {d}")
    yaml_src.append("sources:")
    for s in sources:
        yaml_src.append(f"  - {s}")
    p.write_text("\n".join(yaml_src) + "\n", encoding="utf-8")
    return p


def _write_drug(root: Path, drug_id: str) -> Path:
    drug_dir = root / "drugs"
    drug_dir.mkdir(parents=True, exist_ok=True)
    p = drug_dir / f"{drug_id.lower()}.yaml"
    p.write_text(
        textwrap.dedent(
            f"""\
            id: {drug_id}
            names:
              preferred: {drug_id}
            sources: []
            """
        ),
        encoding="utf-8",
    )
    return p


def _unresolved_entries(entries: list[tuple[Path, str]]) -> list[tuple[Path, str]]:
    """Filter (path, msg) entries down to SRC-resolution-only ones."""
    return [(p, m) for (p, m) in entries if "Unresolved citation ref" in m]


# ---------------------------------------------------------------------------
# Helper-function unit tests (pure, no I/O — fast smoke).
# ---------------------------------------------------------------------------


def test_levenshtein_basic_distances():
    assert _levenshtein("abc", "abc") == 0
    assert _levenshtein("abc", "abd") == 1
    assert _levenshtein("kitten", "sitting") == 3
    # Bounded by cap
    assert _levenshtein("abc", "xyzwxyz", cap=3) == 3


def test_categorize_banned_id_returns_banned():
    cat, hint = _categorize_unresolved_src("SRC-ONCOKB", set())
    assert cat == "banned"
    assert "CHARTER" in hint


def test_categorize_typo_id_returns_typo_with_suggestion():
    known = {"SRC-NCCN-BCELL-2025"}
    cat, hint = _categorize_unresolved_src("SRC-NCCN-BCELL-2024", known)
    assert cat == "typo"
    assert "SRC-NCCN-BCELL-2025" in hint


def test_categorize_authentic_gap_returns_gap_with_stub_hint():
    known = {"SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"}
    cat, hint = _categorize_unresolved_src("SRC-COMPLETELY-NOVEL-2026", known)
    assert cat == "gap"
    assert "source_stub" in hint


def test_banned_set_includes_oncokb_snomed_meddra():
    assert "SRC-ONCOKB" in BANNED_SOURCE_IDS
    assert "SRC-SNOMED" in BANNED_SOURCE_IDS
    assert "SRC-MEDDRA" in BANNED_SOURCE_IDS


# ---------------------------------------------------------------------------
# Live KB drift count — proves the check is active.
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not LIVE_KB.exists(),
    reason="live knowledge_base/hosted/content not present",
)
def test_live_kb_strict_surfaces_unresolved_src_refs():
    """Run strict mode against the real KB. Assert at least 1 unresolved
    SRC-* citation surfaces — proves the check is wired up.

    Don't pin exact count (changes as Source stubs are filed); just that
    the check is active and produces the canonical message.
    """
    clear_load_cache()
    result = load_content(LIVE_KB, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    # At time of writing PR4: 38 unresolved entries (35 unique IDs:
    # 2 typo / 0 banned / 33 authentic gaps). Lower bound: > 0.
    assert len(src_errs) > 0, (
        "strict-mode load against live KB found 0 unresolved SRC-* refs — "
        "check is unwired or KB has been fully filled"
    )
    # Drift inventory for posterity / future regression: capture unique IDs.
    unique = {
        m.group(1) for (_, msg) in src_errs if (m := _UNRESOLVED_RE.search(msg))
    }
    print(
        f"\n[drift] live KB strict-mode unresolved SRC-* unique IDs: "
        f"{len(unique)} (entries={len(src_errs)})"
    )


@pytest.mark.skipif(
    not LIVE_KB.exists(),
    reason="live knowledge_base/hosted/content not present",
)
def test_live_kb_default_mode_is_warn_only():
    """Default load (warn-only) must keep result.ok=True even when the
    live KB has unresolved SRC-* citations. Existing test_loader tests
    rely on this back-compat.
    """
    clear_load_cache()
    result = load_content(LIVE_KB)  # default strict_source_refs=False
    src_warns = _unresolved_entries(result.contract_warnings)
    src_errs = _unresolved_entries(result.ref_errors)
    assert src_errs == [], (
        "default mode leaked SRC-resolution into ref_errors — "
        "back-compat broken"
    )
    assert len(src_warns) > 0, "default mode should warn on unresolved SRC-* refs"
    # Result.ok should still be True (modulo other unrelated contract
    # errors that may exist on master). Specifically: SRC-resolution must
    # NOT have populated ref_errors or contract_errors.


# ---------------------------------------------------------------------------
# Synthetic clean KB — passes both strict and default modes.
# ---------------------------------------------------------------------------


def test_synthetic_clean_kb_passes_strict(tmp_path: Path):
    clear_load_cache()
    _write_source(tmp_path, "SRC-X")
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_regimen(tmp_path, "REG-X", sources=["SRC-X"])

    result = load_content(tmp_path, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    src_warns = _unresolved_entries(result.contract_warnings)
    assert src_errs == [], f"unexpected ref_errors: {src_errs}"
    assert src_warns == [], f"unexpected warnings: {src_warns}"


# ---------------------------------------------------------------------------
# Synthetic broken KB — fails cleanly.
# ---------------------------------------------------------------------------


def test_synthetic_broken_kb_strict_fails_with_one_error(tmp_path: Path):
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    # No SRC-MISSING source defined.
    _write_regimen(tmp_path, "REG-Y", sources=["SRC-MISSING"])

    result = load_content(tmp_path, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    assert len(src_errs) == 1, f"expected 1 ref_error, got: {src_errs}"
    path, msg = src_errs[0]
    assert "SRC-MISSING" in msg
    assert "Unresolved citation ref" in msg
    assert "sources[" in msg  # field label
    # Authentic gap, no typo candidates
    assert "source_stub" in msg


def test_synthetic_broken_kb_default_warns_only(tmp_path: Path):
    """Default mode keeps result.ok=True; unresolved SRC-* lands in
    contract_warnings instead."""
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_regimen(tmp_path, "REG-Z", sources=["SRC-MISSING"])

    result = load_content(tmp_path)  # default warn-only
    src_errs = _unresolved_entries(result.ref_errors)
    src_warns = _unresolved_entries(result.contract_warnings)
    assert src_errs == [], "default mode must not populate ref_errors"
    assert len(src_warns) == 1
    assert "SRC-MISSING" in src_warns[0][1]


# ---------------------------------------------------------------------------
# Banned-source detection.
# ---------------------------------------------------------------------------


def test_synthetic_kb_banned_source_id_gets_banned_hint(tmp_path: Path):
    """Unresolved banned-legacy ID (SRC-SNOMED) gets a 'banned' hint per
    CHARTER §2 instead of a typo suggestion or stub-file hint.

    SRC-SNOMED is used here because it never appears as a Source entity
    (license-incompatible). SRC-ONCOKB and SRC-MEDDRA are also in the
    banned set; the categorization helper covers all three (see
    test_categorize_banned_id_returns_banned).
    """
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_regimen(tmp_path, "REG-BANNED", sources=["SRC-SNOMED"])

    result = load_content(tmp_path, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    assert len(src_errs) == 1
    msg = src_errs[0][1]
    assert "SRC-SNOMED" in msg
    assert "banned" in msg.lower()
    assert "CHARTER" in msg


# ---------------------------------------------------------------------------
# Typo suggestion.
# ---------------------------------------------------------------------------


def test_synthetic_kb_typo_gets_did_you_mean(tmp_path: Path):
    """Brief test #5: two sources, regimen cites a typo'd version of one
    of them. Loader suggests the closest match.
    """
    clear_load_cache()
    _write_source(tmp_path, "SRC-NCCN-BCELL-2025")
    _write_source(tmp_path, "SRC-NCCN-DLBCL-2024")
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    # Typo: 2024 vs 2025 — Levenshtein distance 1 from SRC-NCCN-BCELL-2025
    _write_regimen(tmp_path, "REG-TYPO", sources=["SRC-NCCN-BCELL-2024"])

    result = load_content(tmp_path, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    assert len(src_errs) == 1
    msg = src_errs[0][1]
    assert "SRC-NCCN-BCELL-2024" in msg
    assert "did you mean" in msg.lower()
    assert "SRC-NCCN-BCELL-2025" in msg


# ---------------------------------------------------------------------------
# Narrative-field scan — notes / evidence_summary mentions.
# ---------------------------------------------------------------------------


def test_synthetic_kb_notes_field_unresolved_src_is_caught(tmp_path: Path):
    """SRC-XYZ mentioned inside ``notes:`` markdown is caught even though
    it isn't a structural FK. This is what the citation-verifier
    workstream needs — narrative drift is a render hazard."""
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_source(tmp_path, "SRC-X")
    reg_dir = tmp_path / "regimens"
    reg_dir.mkdir(parents=True, exist_ok=True)
    (reg_dir / "reg_narrative.yaml").write_text(
        textwrap.dedent(
            """\
            id: REG-NARRATIVE
            name: Test regimen
            components:
              - drug_id: DRUG-RITUXIMAB
            sources:
              - SRC-X
            notes: |
              Per SRC-INVENTED-2099, response rate was 80% in pivotal trial.
            """
        ),
        encoding="utf-8",
    )

    result = load_content(tmp_path, strict_source_refs=True)
    src_errs = _unresolved_entries(result.ref_errors)
    # One unresolved: SRC-INVENTED-2099 in notes.
    assert any("SRC-INVENTED-2099" in m for (_, m) in src_errs), (
        f"narrative SRC-* mention not caught: {src_errs}"
    )


# ---------------------------------------------------------------------------
# Cache key invalidates on strict-flag toggle.
# ---------------------------------------------------------------------------


def test_cache_key_includes_strict_flag(tmp_path: Path):
    """Toggling strict_source_refs between calls must produce distinct
    LoadResult instances (different ref_errors/contract_warnings)."""
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_regimen(tmp_path, "REG-CACHE", sources=["SRC-MISSING"])

    warn = load_content(tmp_path, strict_source_refs=False)
    strict = load_content(tmp_path, strict_source_refs=True)

    assert warn is not strict, "cache mistakenly merges strict + warn entries"
    assert _unresolved_entries(warn.ref_errors) == []
    assert _unresolved_entries(strict.ref_errors) != []


# ---------------------------------------------------------------------------
# Audit script smoke test.
# ---------------------------------------------------------------------------


def test_audit_script_runs_end_to_end_on_synthetic(tmp_path: Path):
    """``scripts.audit_unresolved_sources`` runs against a tmp_path mini-KB,
    emits structured markdown, and exits 1 when unresolved refs exist."""
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_regimen(tmp_path, "REG-AUDIT", sources=["SRC-MISSING"])

    import subprocess
    import sys as _sys

    proc = subprocess.run(
        [
            _sys.executable,
            "-X",
            "utf8",
            "-m",
            "scripts.audit_unresolved_sources",
            "--root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    # Exit code should be 1 (unresolved refs present)
    assert proc.returncode == 1, (
        f"unexpected exit code {proc.returncode}; stderr={proc.stderr!r}"
    )
    # Output should be markdown with the table sections
    assert "# Unresolved SRC-* citation audit" in proc.stdout
    assert "Authentic gaps" in proc.stdout
    assert "SRC-MISSING" in proc.stdout


def test_audit_script_clean_kb_exits_zero(tmp_path: Path):
    clear_load_cache()
    _write_drug(tmp_path, "DRUG-RITUXIMAB")
    _write_source(tmp_path, "SRC-CLEAN")
    _write_regimen(tmp_path, "REG-OK", sources=["SRC-CLEAN"])

    import subprocess
    import sys as _sys

    proc = subprocess.run(
        [
            _sys.executable,
            "-X",
            "utf8",
            "-m",
            "scripts.audit_unresolved_sources",
            "--root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, (
        f"clean KB should exit 0; got {proc.returncode}; "
        f"stdout={proc.stdout!r}; stderr={proc.stderr!r}"
    )
