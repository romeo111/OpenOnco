"""Per-RedFlag golden fixtures + structural integrity tests.

See tests/fixtures/redflags/README.md for fixture format.

This module covers two layers:

1. Trigger fixtures (data-driven). Every subdir of tests/fixtures/redflags/
   matches one RedFlag ID. Each fixture YAML inside specifies a findings
   dict and an expected_fires boolean. The test asserts the engine's
   evaluate_redflag_trigger matches.

2. Structural tests (config-driven). Every shifts_algorithm:[ALGO-X]
   declaration on a RedFlag must be reciprocated by ALGO-X.decision_tree
   actually referencing that RF (no orphans). Conversely, every
   {red_flag: RF-X} clause inside an Algorithm.decision_tree must
   resolve to a known RedFlag. And every clinical_direction=investigate
   RedFlag must have an empty shifts_algorithm (per
   REDFLAG_AUTHORING_GUIDE §4 rule 2).
"""

from __future__ import annotations

import functools
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine.redflag_eval import (
    evaluate_redflag_trigger,
    is_redflag_applicable,
    resolve_redflag_conflict,
)

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "redflags"


# NOTE: Caches below shave ~14 minutes off the full pytest suite.
# `test_redflag_fixture` is parametrized over ~864 fixture YAMLs and was
# rebuilding the entire RedFlag map (rglob + yaml.safe_load over ~500
# files) on EVERY invocation. With lru_cache, the walk happens once per
# pytest session. KB YAMLs are immutable during a test session, so the
# cache is safe.

@functools.lru_cache(maxsize=4096)
def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@functools.lru_cache(maxsize=1)
def _load_redflags() -> dict[str, dict]:
    """All RedFlag YAMLs, keyed by id."""
    rfs: dict[str, dict] = {}
    for p in sorted((KB_ROOT / "redflags").rglob("*.yaml")):
        data = _load_yaml(p)
        rid = data.get("id")
        if rid:
            rfs[rid] = data
    return rfs


@functools.lru_cache(maxsize=1)
def _load_algorithms() -> dict[str, dict]:
    algs: dict[str, dict] = {}
    for p in sorted((KB_ROOT / "algorithms").glob("*.yaml")):
        data = _load_yaml(p)
        aid = data.get("id")
        if aid:
            algs[aid] = data
    return algs


def _collect_red_flag_refs_in_evaluate(evaluate: dict) -> list[str]:
    """Extract every RedFlag ID referenced inside an Algorithm step's
    `evaluate:` block, including the P2 shorthand combo lists."""
    if not isinstance(evaluate, dict):
        return []
    out: list[str] = []
    for key in ("all_of", "any_of", "none_of"):
        for clause in evaluate.get(key) or []:
            if isinstance(clause, dict):
                if "red_flag" in clause:
                    out.append(clause["red_flag"])
                # nested groups
                for nested_key in ("all_of", "any_of", "none_of"):
                    if nested_key in clause:
                        out.extend(_collect_red_flag_refs_in_evaluate(clause))
    for key in ("red_flags_all_of", "red_flags_any_of"):
        for rid in evaluate.get(key) or []:
            out.append(rid)
    return out


# ── Fixture-based trigger tests ──────────────────────────────────────────


def _discover_fixtures() -> list[tuple[str, Path]]:
    """Yield (rf_id, fixture_path) for every fixture YAML under FIXTURE_ROOT."""
    out: list[tuple[str, Path]] = []
    if not FIXTURE_ROOT.is_dir():
        return out
    for rf_dir in sorted(FIXTURE_ROOT.iterdir()):
        if not rf_dir.is_dir():
            continue
        for f in sorted(rf_dir.glob("*.yaml")):
            out.append((rf_dir.name, f))
    return out


@pytest.mark.parametrize("rf_id,fixture_path", _discover_fixtures())
def test_redflag_fixture(rf_id: str, fixture_path: Path) -> None:
    """Each fixture asserts: when given these findings, this RedFlag
    fires (or does not) per its trigger predicate."""
    fixture = _load_yaml(fixture_path)
    assert fixture.get("red_flag") == rf_id, (
        f"{fixture_path}: red_flag field {fixture.get('red_flag')!r} "
        f"doesn't match parent dir {rf_id!r}"
    )

    rfs = _load_redflags()
    assert rf_id in rfs, f"Fixture references unknown RedFlag {rf_id}"

    expected = fixture.get("expected_fires")
    assert expected is not None, f"{fixture_path}: missing expected_fires"

    findings = fixture.get("findings") or {}
    actual = evaluate_redflag_trigger(rfs[rf_id].get("trigger") or {}, findings)
    assert actual == expected, (
        f"{fixture_path}: expected fires={expected}, got {actual}; "
        f"findings={findings}"
    )


# ── Structural tests (run once, not per-fixture) ─────────────────────────


# Known orphans — RedFlag declares shifts_algorithm:[ALGO-X] but the
# Algorithm's decision_tree doesn't actually reference the RF. These
# are clinical-content TODOs (the decision_tree needs a step that branches
# on the RF). Resolve by either:
#   (a) editing the Algorithm's decision_tree to add the missing step, OR
#   (b) re-classifying the RF as clinical_direction=investigate and
#       clearing shifts_algorithm.
# Whitelist exists so this test catches NEW regressions while existing
# debt remains visible. Empty this whitelist as items are fixed.
# All known orphans resolved as of 2026-04-25 (clinical sign-off):
#   - RF-DECOMP-CIRRHOSIS → wired into ALGO-HCV-MZL-1L step 1
#   - RF-TCELL-CD30-POSITIVE → wired into ALGO-ALCL-1L step 1
#   - RF-HBV-COINFECTION → reclassified to clinical_direction=investigate
#     (CLINICAL_REVIEW_QUEUE_REDFLAGS §B.1 Option 2); cleared shifts_algorithm
#
# Re-introduced 2026-04-27 by the CIViC pivot + CSD-7/8 + solid-tumor expansion.
# Three cohorts:
#
# (A) Biomarker-actionability annotations (CIViC pivot, Phase 3-N) — surface
#     variant-level evidence into the actionability render layer (ESCAT-primary),
#     not into the algorithm decision tree. shifts_algorithm documents which
#     algorithms the variant *should be considered against*; wiring is
#     render-side via BiomarkerActionability, not engine routing.
# (B) Clinical-data RFs awaiting algorithm wiring (CSD-8 follow-up) —
#     clinician-prioritized but step-design needs co-lead review.
# (C) Solid-tumor PDL1/CRC RAS RFs from CSD-9 expansion — same wiring TODO.
#
# Tracked in docs/reviews/preexisting-failures-2026-04-27.md.
_KNOWN_ORPHANS: set[tuple[str, str]] = {
    # (A) Biomarker-actionability (CIViC pivot — render-layer, not engine-routed)
    ("RF-CLL-POST-BTKI-C481-ACTIONABLE", "ALGO-CLL-2L"),
    ("RF-CLL-TP53-DELETION-ACTIONABLE", "ALGO-CLL-1L"),
    ("RF-CLL-VEN-RESISTANT-ACTIONABLE", "ALGO-CLL-2L"),
    ("RF-FL-EZH2-Y641-ACTIONABLE", "ALGO-FL-2L"),
    ("RF-WM-MYD88-L265P-ACTIONABLE", "ALGO-WM-1L"),
    # (B) Clinical-data RFs awaiting algorithm wiring (CSD-8 follow-up)
    ("RF-AML-CORE-BINDING-FACTOR-FAVORABLE", "ALGO-AML-1L"),
    ("RF-AML-MEASURABLE-RESIDUAL-DISEASE", "ALGO-AML-1L"),
    ("RF-AML-MEASURABLE-RESIDUAL-DISEASE", "ALGO-AML-2L"),
    ("RF-IPSS-M-HIGH", "ALGO-MDS-LR-1L"),
    ("RF-MCL-BLASTOID-VARIANT", "ALGO-MCL-2L"),
    # (C) Solid-tumor PDL1 / CRC RAS (CSD-9 expansion — wiring TODO)
    ("RF-CERVICAL-PDL1-CPS-1-PLUS", "ALGO-CERVICAL-LOCALLY-ADVANCED-1L"),
    ("RF-CRC-RAS-MUTANT", "ALGO-CRC-METASTATIC-1L"),
    ("RF-CRC-RAS-MUTANT", "ALGO-CRC-METASTATIC-2L"),
    ("RF-CRC-RAS-WT", "ALGO-CRC-METASTATIC-1L"),
    ("RF-GASTRIC-PDL1-CPS-1-PLUS", "ALGO-GASTRIC-METASTATIC-1L"),
    ("RF-NSCLC-PDL1-50-PLUS", "ALGO-NSCLC-METASTATIC-1L"),
    # (D) Tier-1 biomarker expansion (PR #166 — AML KMT2A / TP53 wiring TODO)
    ("RF-AML-KMT2A-ACTIONABLE", "ALGO-AML-1L"),
    ("RF-AML-KMT2A-ACTIONABLE", "ALGO-AML-2L"),
    ("RF-AML-TP53-ADVERSE", "ALGO-AML-1L"),
    ("RF-AML-TP53-ADVERSE", "ALGO-AML-2L"),
}


def test_no_orphan_red_flag_decl() -> None:
    """Every RedFlag.shifts_algorithm[i]=ALGO-X must be reciprocated:
    ALGO-X.decision_tree must reference this RedFlag in some step.
    Investigate-only flags (clinical_direction=investigate) are exempt.
    Pre-existing debt is whitelisted in _KNOWN_ORPHANS."""
    rfs = _load_redflags()
    algs = _load_algorithms()
    failures: list[str] = []

    # Build alg -> set(referenced RedFlag IDs)
    alg_refs: dict[str, set[str]] = {}
    for aid, a in algs.items():
        refs: set[str] = set()
        for step in a.get("decision_tree") or []:
            refs.update(_collect_red_flag_refs_in_evaluate(step.get("evaluate") or {}))
        alg_refs[aid] = refs

    for rid, rf in rfs.items():
        if rf.get("clinical_direction") == "investigate":
            continue
        if rf.get("draft"):
            # Scaffolded drafts aren't wired into decision trees yet by
            # design — they get a contract-warning instead.
            continue
        for alg_id in rf.get("shifts_algorithm") or []:
            referenced = alg_refs.get(alg_id, set())
            if rid in referenced:
                continue
            if (rid, alg_id) in _KNOWN_ORPHANS:
                continue
            failures.append(
                f"{rid}: shifts_algorithm references {alg_id} but "
                f"{alg_id}.decision_tree doesn't mention {rid}"
            )

    assert not failures, "New orphan RedFlag declarations:\n" + "\n".join(failures)


def test_no_unknown_red_flag_in_algorithms() -> None:
    """Every {red_flag: RF-X} (or shorthand list entry) inside an Algorithm
    must resolve to a known RedFlag YAML."""
    rfs = _load_redflags()
    algs = _load_algorithms()
    failures: list[str] = []

    for aid, a in algs.items():
        for step in a.get("decision_tree") or []:
            for ref in _collect_red_flag_refs_in_evaluate(step.get("evaluate") or {}):
                if ref not in rfs:
                    failures.append(f"{aid} step {step.get('step')}: unknown RedFlag {ref}")

    assert not failures, "Unknown RedFlag refs:\n" + "\n".join(failures)


def test_investigate_flags_do_not_shift() -> None:
    """clinical_direction=investigate must mean shifts_algorithm is empty
    (per REDFLAG_AUTHORING_GUIDE §4 rule 2). investigate flags only
    surface annotations; they must not appear in any decision_tree."""
    rfs = _load_redflags()
    failures: list[str] = []
    for rid, rf in rfs.items():
        if rf.get("clinical_direction") == "investigate" and rf.get("shifts_algorithm"):
            failures.append(
                f"{rid}: clinical_direction=investigate but shifts_algorithm="
                f"{rf['shifts_algorithm']} — re-classify or clear shifts_algorithm"
            )
    assert not failures, "investigate-flags shifting Algorithms:\n" + "\n".join(failures)


def test_relevant_diseases_resolve() -> None:
    """relevant_diseases entries must be either '*' (universal) or
    point at a known disease YAML."""
    rfs = _load_redflags()
    disease_ids: set[str] = set()
    for p in (KB_ROOT / "diseases").glob("*.yaml"):
        d = _load_yaml(p)
        if d.get("id"):
            disease_ids.add(d["id"])

    failures: list[str] = []
    for rid, rf in rfs.items():
        for d in rf.get("relevant_diseases") or []:
            if d == "*":
                continue
            if d not in disease_ids:
                failures.append(f"{rid}: relevant_diseases entry {d} unresolved")

    assert not failures, "Unresolved relevant_diseases:\n" + "\n".join(failures)


# ── Conflict-resolver unit tests ─────────────────────────────────────────


def test_conflict_hold_beats_intensify() -> None:
    lookup = {
        "RF-A": {"clinical_direction": "intensify", "severity": "critical", "priority": 50},
        "RF-B": {"clinical_direction": "hold", "severity": "minor", "priority": 200},
    }
    winner, _ = resolve_redflag_conflict(["RF-A", "RF-B"], lookup)
    assert winner == "RF-B", "hold direction must outrank intensify regardless of severity/priority"


def test_conflict_severity_tiebreaker() -> None:
    lookup = {
        "RF-A": {"clinical_direction": "intensify", "severity": "minor", "priority": 100},
        "RF-B": {"clinical_direction": "intensify", "severity": "critical", "priority": 100},
    }
    winner, _ = resolve_redflag_conflict(["RF-A", "RF-B"], lookup)
    assert winner == "RF-B", "critical severity must outrank minor when direction is equal"


def test_conflict_priority_tiebreaker() -> None:
    lookup = {
        "RF-A": {"clinical_direction": "intensify", "severity": "major", "priority": 100},
        "RF-B": {"clinical_direction": "intensify", "severity": "major", "priority": 30},
    }
    winner, _ = resolve_redflag_conflict(["RF-A", "RF-B"], lookup)
    assert winner == "RF-B", "lower priority number must win on tie"


def test_universal_redflag_applicability() -> None:
    universal = {"relevant_diseases": ["*"]}
    specific = {"relevant_diseases": ["DIS-DLBCL-NOS"]}
    assert is_redflag_applicable(universal, "DIS-CLL")
    assert is_redflag_applicable(universal, None)
    assert is_redflag_applicable(specific, "DIS-DLBCL-NOS")
    assert not is_redflag_applicable(specific, "DIS-CLL")
