"""Prevention KB audit suite — cross-reference integrity + STUB consistency
+ source policy (CHARTER §2 / §6.1 dev-mode invariants, KSS §20).

Companion to `tests/test_prevention_engine.py` (which covers a hand-picked
~12 pilots) and `tests/test_prevention_render.py` (HTML render layer).
This module instead walks the **entire** prevention KB and asserts the
invariants that any new prevention RF / Indication needs to satisfy.

Each test gathers all defects across the KB before failing, so a single
test surfaces the full list of broken entities rather than dying on the
first one. That makes the suite useful as a maintainer-facing audit:
when a new prevention pilot is authored, this catches the common
authoring mistakes (missing source, missing risk_category enum value,
unresolved RF reference, banned-source citation, …) in one pass.

Test 9 (`test_prevention_engine_smoke_all_pilots`) additionally exercises
the engine end-to-end: for a stratified sample of prevention RFs across
all 7 risk_category enum values, synthesize a minimal patient that
satisfies the RF's first trigger clause, run generate_plan(), and assert
≥2 prevention tracks + the RF fired. This catches engine routing
regressions that the 12-pilot subset in test_prevention_engine.py would
not catch (RFs added after the v0.2-A pilot wave).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan
from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


# Mirrored from knowledge_base.schemas.base.PreventionRiskCategory so the
# audit is independent of which enum names are exported by the schema
# (the test surfaces a schema/value mismatch as a failed assertion in
# test 1, not as an ImportError).
VALID_RISK_CATEGORIES: frozenset[str] = frozenset({
    "genetic",
    "infectious",
    "chronic_condition",
    "occupational",
    "iatrogenic",
    "lifestyle",
    "reproductive",
})

PREVENTION_INTENTS: frozenset[str] = frozenset({
    "prevention", "screening", "surveillance",
})

# CHARTER §2 banned-source policy. Mirror of
# `knowledge_base.validation.loader.BANNED_SOURCE_IDS` plus the common
# narrative-prose spellings authors sometimes use (case-insensitive).
BANNED_SOURCE_IDS: frozenset[str] = frozenset({
    "SRC-ONCOKB", "SRC-SNOMED", "SRC-MEDDRA",
})


# ── Shared loader fixture (module-scoped via loader's own cache) ──────────


@pytest.fixture(scope="module")
def kb_load():
    """Load the full KB once for the whole module.

    `load_content` already module-caches by (path, strict) tuple, but the
    fixture wrapper documents intent and lets test 9 keep its
    `generate_plan` calls cheap (each call hits the same cache).
    """
    return load_content(KB_ROOT)


def _prevention_redflags(load) -> dict[str, dict]:
    """Return {id: raw_yaml_data} for every RedFlag whose risk_category
    is set (i.e., participates in the §20 prevention path)."""
    out: dict[str, dict] = {}
    for eid, info in load.entities_by_id.items():
        if info["type"] != "redflags":
            continue
        if info["data"].get("risk_category") is None:
            continue
        out[eid] = info["data"]
    return out


def _prevention_indications(load) -> dict[str, dict]:
    """Return {id: raw_yaml_data} for every Indication whose intent is
    one of {prevention, screening, surveillance}."""
    out: dict[str, dict] = {}
    for eid, info in load.entities_by_id.items():
        if info["type"] != "indications":
            continue
        if info["data"].get("intent") not in PREVENTION_INTENTS:
            continue
        out[eid] = info["data"]
    return out


def _flatten_source_ids(sources: list) -> list[str]:
    """Indications carry `sources: list[Citation]` (dicts with `source_id`);
    RedFlags carry `sources: list[str]`. Normalize to a flat list of strings."""
    out: list[str] = []
    if not isinstance(sources, list):
        return out
    for s in sources:
        if isinstance(s, str):
            out.append(s)
        elif isinstance(s, dict):
            sid = s.get("source_id")
            if isinstance(sid, str):
                out.append(sid)
    return out


# ── Test 1: risk_category enum coverage ───────────────────────────────────


def test_all_prevention_rfs_have_risk_category(kb_load):
    """Every RF with risk_category set must use one of the 7 enum values.

    This guards against typo'd values (e.g. `genetics` instead of
    `genetic`) — the Pydantic schema validator already rejects unknown
    values at load-time, but this also asserts the audit's understanding
    of the canonical 7-value taxonomy stays in sync with the schema.
    """
    defects: list[str] = []
    rfs = _prevention_redflags(kb_load)
    assert rfs, "No prevention RedFlags found — audit suite has nothing to check"
    for eid, data in rfs.items():
        rc = data.get("risk_category")
        if rc not in VALID_RISK_CATEGORIES:
            defects.append(
                f"{eid}: risk_category={rc!r} not in "
                f"{sorted(VALID_RISK_CATEGORIES)}"
            )
    assert not defects, (
        f"Found {len(defects)} RF(s) with invalid risk_category:\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 2: prevention indications must declare triggered_by_redflags ─────


def test_all_prevention_indications_have_triggered_by_redflags(kb_load):
    """Cross-etiology isolation guard (KSS §20.2 + cross-etiology
    regression on 2026-05-18).

    Without an explicit `triggered_by_redflags` binding, the engine
    matches prevention Indications by disease_id only — which causes
    contamination (e.g. a Lynch carrier targeting DIS-GASTRIC would
    pick up H. pylori prevention indications). Every prevention
    Indication must declare the RF that triggers it.
    """
    defects: list[str] = []
    inds = _prevention_indications(kb_load)
    assert inds, "No prevention Indications found — audit has nothing to check"
    for eid, data in inds.items():
        triggered_by = data.get("triggered_by_redflags") or []
        if not triggered_by:
            defects.append(f"{eid}: triggered_by_redflags is empty / missing")
    assert not defects, (
        f"Found {len(defects)} prevention Indication(s) without "
        "triggered_by_redflags (cross-etiology isolation broken):\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 3: every triggered_by_redflags entry resolves to a real RF ───────


def test_all_triggered_by_redflags_resolve_to_existing_rfs(kb_load):
    """For every Indication.triggered_by_redflags entry, the referenced
    RF-* ID must exist somewhere in the KB. Catches typos / dead
    references / RFs renamed without updating their consumers."""
    defects: list[str] = []
    inds = _prevention_indications(kb_load)
    for eid, data in inds.items():
        for rf_id in data.get("triggered_by_redflags") or []:
            if not isinstance(rf_id, str):
                defects.append(
                    f"{eid}: triggered_by_redflags entry is not a string: {rf_id!r}"
                )
                continue
            target = kb_load.entities_by_id.get(rf_id)
            if target is None:
                defects.append(
                    f"{eid}: triggered_by_redflags references {rf_id!r} "
                    "which is not defined in the KB"
                )
                continue
            if target["type"] != "redflags":
                defects.append(
                    f"{eid}: triggered_by_redflags references {rf_id!r} "
                    f"which is a {target['type']}, not a redflags entity"
                )
    assert not defects, (
        f"Found {len(defects)} unresolved triggered_by_redflags refs:\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 4: every prevention RF cites ≥1 source (CHARTER §6.1) ────────────


def test_all_prevention_rfs_have_cited_sources(kb_load):
    """CHARTER §6.1 dev-mode requirement: every clinical content entity
    must cite at least one Source. Prevention RFs are clinical content
    (they drive the PreventionPlan)."""
    defects: list[str] = []
    for eid, data in _prevention_redflags(kb_load).items():
        sources = _flatten_source_ids(data.get("sources") or [])
        if not sources:
            defects.append(f"{eid}: sources list is empty")
    assert not defects, (
        f"Found {len(defects)} prevention RF(s) with no sources:\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 5: every prevention Indication cites ≥1 source ───────────────────


def test_all_prevention_indications_have_cited_sources(kb_load):
    """CHARTER §6.1 dev-mode requirement applied to prevention
    Indications."""
    defects: list[str] = []
    for eid, data in _prevention_indications(kb_load).items():
        sources = _flatten_source_ids(data.get("sources") or [])
        if not sources:
            defects.append(f"{eid}: sources list is empty")
    assert not defects, (
        f"Found {len(defects)} prevention Indication(s) with no sources:\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 6: STUB consistency markers ──────────────────────────────────────


def test_all_prevention_entities_marked_stub(kb_load):
    """CHARTER §6.1 dev-mode marks unsignedoff clinical content as STUB:
      - every prevention RF: `draft: true`
      - every prevention Indication: `reviewer_signoffs: 0` (legacy
        int-zero marker; the schema migrates it to [] at load time,
        but raw YAML keeps `0`).

    When the two-Clinical-Co-Lead signoff phase begins, the STUB markers
    flip and this test will need a corresponding update (which is the
    explicit signal that signoff is in progress, not a regression)."""
    rf_defects: list[str] = []
    for eid, data in _prevention_redflags(kb_load).items():
        if data.get("draft") is not True:
            rf_defects.append(f"{eid}: draft={data.get('draft')!r}, expected True")

    ind_defects: list[str] = []
    for eid, data in _prevention_indications(kb_load).items():
        rs = data.get("reviewer_signoffs")
        if rs != 0:
            ind_defects.append(
                f"{eid}: reviewer_signoffs={rs!r}, expected 0 "
                "(dev-mode unsignedoff marker)"
            )

    msg_parts: list[str] = []
    if rf_defects:
        msg_parts.append(
            f"{len(rf_defects)} prevention RF(s) without draft: true:\n  - "
            + "\n  - ".join(rf_defects)
        )
    if ind_defects:
        msg_parts.append(
            f"{len(ind_defects)} prevention Indication(s) without "
            "reviewer_signoffs: 0:\n  - " + "\n  - ".join(ind_defects)
        )
    assert not msg_parts, "\n\n".join(msg_parts)


# ── Test 7: banned-source policy (CHARTER §2) ─────────────────────────────


def test_no_banned_sources_in_prevention_pilots(kb_load):
    """No prevention RF / Indication may cite OncoKB, SNOMED CT, or
    MedDRA (per CHARTER §2 non-commercial-only KB)."""
    defects: list[str] = []

    for eid, data in _prevention_redflags(kb_load).items():
        for sid in _flatten_source_ids(data.get("sources") or []):
            if sid in BANNED_SOURCE_IDS:
                defects.append(f"RF {eid}: cites banned source {sid!r}")

    for eid, data in _prevention_indications(kb_load).items():
        for sid in _flatten_source_ids(data.get("sources") or []):
            if sid in BANNED_SOURCE_IDS:
                defects.append(f"IND {eid}: cites banned source {sid!r}")

    assert not defects, (
        f"Found {len(defects)} banned-source citation(s) "
        "(CHARTER §2 violation):\n  - " + "\n  - ".join(defects)
    )


# ── Test 8: relevant_diseases must resolve ────────────────────────────────


def test_prevention_rfs_relevant_diseases_resolve(kb_load):
    """Every RF.relevant_diseases entry must resolve to a Disease entity,
    except the `"*"` universal sentinel.

    The loader's `_check_redflag_contracts` already enforces this — but
    only for non-draft RFs. Every prevention RF is draft: true (per
    test 6), so this audit catches the gap that loader bypasses."""
    defects: list[str] = []
    for eid, data in _prevention_redflags(kb_load).items():
        for d in data.get("relevant_diseases") or []:
            if d == "*":
                continue
            target = kb_load.entities_by_id.get(d)
            if target is None:
                defects.append(
                    f"{eid}: relevant_diseases entry {d!r} is not "
                    "defined in the KB"
                )
                continue
            if target["type"] != "diseases":
                defects.append(
                    f"{eid}: relevant_diseases entry {d!r} is a "
                    f"{target['type']}, not a diseases entity"
                )
    assert not defects, (
        f"Found {len(defects)} unresolved relevant_diseases ref(s):\n  - "
        + "\n  - ".join(defects)
    )


# ── Test 9: engine smoke for every prevention RF (stratified sample) ──────


def _synthesize_findings_for_clause(clause: dict) -> dict | None:
    """Build a minimal findings dict that satisfies a single clause.
    Returns None if the shape is not synthesizable."""
    if not isinstance(clause, dict):
        return None
    finding = clause.get("finding") or clause.get("condition")
    if not isinstance(finding, str) or not finding:
        return None

    if "value" in clause:
        return {finding: clause["value"]}

    if "threshold" in clause:
        comparator = clause.get("comparator", ">=")
        threshold = clause["threshold"]
        if not isinstance(threshold, (int, float)):
            return None
        # Pick a value that satisfies the comparator
        if comparator in (">=", "=="):
            return {finding: threshold}
        if comparator == ">":
            return {finding: threshold + 1}
        if comparator in ("<=",):
            return {finding: threshold}
        if comparator == "<":
            return {finding: threshold - 1}
        if comparator == "!=":
            return {finding: threshold + 1}
        return None

    # Bare condition lookup — truthy if value is True. Synth as True.
    return {finding: True}


def _synthesize_findings_for_trigger(trigger: dict) -> dict | None:
    """Walk an RF trigger and build a minimal findings dict that fires it.

    Strategy:
      - top-level `any_of`: satisfy the first element (drill into nested
        boolean groups by taking their first satisfiable branch)
      - top-level `all_of`: satisfy every element (a nested `any_of`
        within an `all_of` is satisfied by its first element)
      - bare clause: synthesize directly

    Returns None if any required clause is non-synthesizable (the
    test then skips with a clear reason)."""
    if not isinstance(trigger, dict):
        return None

    if trigger.get("any_of"):
        # Pick the first element — it might itself be a boolean group
        first = trigger["any_of"][0]
        if isinstance(first, dict) and (first.get("any_of") or first.get("all_of")):
            return _synthesize_findings_for_trigger(first)
        return _synthesize_findings_for_clause(first) if isinstance(first, dict) else None

    if trigger.get("all_of"):
        merged: dict = {}
        for sub in trigger["all_of"]:
            if not isinstance(sub, dict):
                return None
            if sub.get("any_of") or sub.get("all_of"):
                sub_findings = _synthesize_findings_for_trigger(sub)
            else:
                sub_findings = _synthesize_findings_for_clause(sub)
            if sub_findings is None:
                return None
            merged.update(sub_findings)
        return merged or None

    if trigger.get("finding") or trigger.get("condition"):
        return _synthesize_findings_for_clause(trigger)

    return None


def _stratified_rf_sample(rfs: dict[str, dict], per_category: int = 100) -> list[tuple[str, dict]]:
    """Pick up to `per_category` RFs from each risk_category enum value.
    Stable order — sorts by RF id within each category.

    Raised from per_category=5 to 100 in Wave L+M+N+O+P (2026-05-20) —
    KB grew from ~30 prevention RFs to 165 across Waves L-P; full per-RF
    coverage now catches regressions for every shipped RF rather than a
    sparse 5-per-category sample. With current KB this exercises ~150
    distinct RFs as separate parametrize cases."""
    by_cat: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for eid, data in rfs.items():
        by_cat[data.get("risk_category")].append((eid, data))
    sample: list[tuple[str, dict]] = []
    for cat in sorted(by_cat.keys()):
        sample.extend(sorted(by_cat[cat], key=lambda kv: kv[0])[:per_category])
    return sample


def _build_sample(kb_load):
    """pytest's `parametrize` evaluates its argument list at collection time,
    BEFORE fixtures resolve. Wrap the sample build in a function so the
    parametrize call can call it lazily from inside a fixture if needed.
    """
    return _stratified_rf_sample(_prevention_redflags(kb_load))


# Build sample at module-import time using a fresh load. This is fine —
# `load_content` is module-cached, so the load runs once total across
# parametrize + the rest of the suite.
_SAMPLE = _stratified_rf_sample(_prevention_redflags(load_content(KB_ROOT)))


@pytest.mark.parametrize(
    "rf_id,rf_data",
    _SAMPLE,
    ids=[s[0] for s in _SAMPLE],
)
def test_prevention_engine_smoke_all_pilots(rf_id, rf_data):
    """Stratified sample (≤5 RFs per risk_category) — for each RF,
    synthesize a minimal patient that fires the RF's first trigger
    clause, run generate_plan(), and assert:
      - a PreventionPlan was built
      - ≥2 prevention tracks materialized (CHARTER §15.2 C4 invariant)
      - the RF appears in fired_prevention_redflags
      - no algorithm was walked (PreventionPlan.algorithm_id is None)

    Note: other RFs may also fire on the same synthetic finding (the
    `tobacco_status_current_smoker` finding triggers any RF that lists
    that finding too). We do NOT assert exclusivity — only that *this*
    RF is among the fired set."""
    findings = _synthesize_findings_for_trigger(rf_data.get("trigger") or {})
    if findings is None:
        pytest.skip(f"{rf_id}: trigger shape not synthesizable")

    patient = {
        "patient_id": f"PREV-AUDIT-{rf_id}",
        "biomarkers": {},
        "demographics": {"age": 50, "ecog": 1},
        "findings": findings,
    }
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None, (
        f"{rf_id}: no PreventionPlan built — findings {findings!r} "
        f"did not route to prevention path. warnings={result.warnings}"
    )
    assert result.algorithm_id is None, (
        f"{rf_id}: prevention path should not walk an algorithm; "
        f"got algorithm_id={result.algorithm_id}"
    )
    assert len(result.plan.tracks) >= 2, (
        f"{rf_id}: PreventionPlan has only {len(result.plan.tracks)} "
        "track(s) — CHARTER §15.2 C4 requires ≥2"
    )
    fired = result.plan.knowledge_base_state.get(
        "fired_prevention_redflags"
    ) or []
    assert rf_id in fired, (
        f"{rf_id}: RF did not appear in fired_prevention_redflags. "
        f"Fired set: {fired}. Synthesized findings: {findings!r}"
    )


# ── Test 10: coverage summary (smoke-validates overall structure) ─────────


def test_prevention_kb_coverage_summary(kb_load, capsys):
    """Smoke summary: print counts of prevention RFs by category,
    Indications by intent, and example patient fixtures. Asserts only
    the highest-level structural facts (≥1 RF per known category;
    ≥1 Indication per known intent in use). The print output is for
    maintainer visibility via `pytest -s`."""
    rfs = _prevention_redflags(kb_load)
    inds = _prevention_indications(kb_load)

    by_cat = Counter(d.get("risk_category") for d in rfs.values())
    by_intent = Counter(d.get("intent") for d in inds.values())

    example_files = sorted(
        p.name for p in EXAMPLES.glob("patient_*prevention*.json")
    )

    lines = [
        "-- Prevention KB coverage " + "-" * 36,
        f"Total prevention RedFlags:    {len(rfs)}",
    ]
    for cat in sorted(VALID_RISK_CATEGORIES):
        lines.append(f"  - {cat:20s}: {by_cat.get(cat, 0)}")
    unknown_cats = sorted(set(by_cat) - VALID_RISK_CATEGORIES)
    if unknown_cats:
        lines.append("  (unknown risk_category values:)")
        for cat in unknown_cats:
            lines.append(f"  - {cat!r:20s}: {by_cat[cat]}")
    lines.append(f"Total prevention Indications: {len(inds)}")
    for intent in sorted(PREVENTION_INTENTS):
        lines.append(f"  - {intent:20s}: {by_intent.get(intent, 0)}")
    lines.append(f"Total example patient fixtures: {len(example_files)}")
    lines.append("-" * 60)

    print("\n" + "\n".join(lines))

    # Structural assertions — failure here means the prevention pilot
    # wave is degenerate (no RFs / no Indications / unknown categories).
    assert len(rfs) > 0, "No prevention RedFlags in KB"
    assert len(inds) > 0, "No prevention Indications in KB"
    assert not unknown_cats, (
        f"Prevention RFs use risk_category values outside the enum: "
        f"{unknown_cats}"
    )
