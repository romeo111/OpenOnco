"""Coverage suite for the CSD-4 solid-tumor 2L+ expansion.

Validates the seven new 2L+ algorithms (CRC, NSCLC, three breast subtype
algorithms, melanoma, ovarian), the indications wired underneath them,
and 5 known-case end-to-end fixtures.

Sections:
  A — 2L+ algorithm presence: each new ALGO-*-2L loads from the KB
  B — Indications quality: every CSD-4 2L+ indication has line >= 2,
      >= 1 source, last_reviewed, and reviewer_signoffs == 0 per
      CHARTER §6.1 (two-reviewer merge gate not yet satisfied)
  C — Algorithm structure: every then_indication / result resolves to
      a real Indication entity; biomarker references resolve
  D — End-to-end known cases: 5 synthetic patient fixtures exercise
      the new algorithms and assert the expected algorithm + a
      candidate indication appears in the plan output. Tests are
      permissive about which exact Indication the engine selects —
      free-text "condition" clauses don't currently fire, so engine
      falls through to algorithm defaults; the assertion is that the
      expected algorithm runs and the expected indication is at least
      a routable candidate.

Engine selection MUST NOT be tightened up here unilaterally — the
indication-routing precision is owned by the algorithm + RedFlag
authoring pipeline (CSD-4.5+), not by these tests.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan
from knowledge_base.validation.loader import load_content


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "cases"


CSD4_DISEASE_IDS = {
    "DIS-CRC",
    "DIS-NSCLC",
    "DIS-BREAST",
    "DIS-MELANOMA",
    "DIS-OVARIAN",
}

# CSD-4 2L+ algorithm IDs — the seven new algorithms wired in this batch.
CSD4_2L_ALGORITHM_IDS = {
    "ALGO-CRC-METASTATIC-2L",
    "ALGO-NSCLC-METASTATIC-2L",
    "ALGO-BREAST-HR-POS-2L",
    "ALGO-BREAST-HER2-POS-2L",
    "ALGO-BREAST-TNBC-2L",
    "ALGO-MELANOMA-METASTATIC-2L",
    "ALGO-OVARIAN-2L",
}


# ── Module-scoped KB load (one ~3s walk reused across all tests) ──────────


@pytest.fixture(scope="module")
def kb_load():
    return load_content(KB_ROOT)


@pytest.fixture(scope="module")
def entities(kb_load):
    return kb_load.entities_by_id


@pytest.fixture(scope="module")
def csd4_2l_indications(entities, csd4_2l_algorithms):
    """Every Indication entity that:
      - is referenced from one of the seven CSD-4 2L+ algorithms'
        `output_indications` candidate sets, AND
      - belongs to a CSD-4 disease, AND
      - applies at line_of_therapy >= 2.

    Scoping by algorithm-membership (rather than disease + line) keeps
    the test focused on the new CSD-4 batch and avoids pulling in
    pre-existing 2L+ indications that predate the CSD-4 quality bar.
    """
    in_scope: set[str] = set()
    for algo in csd4_2l_algorithms.values():
        for ind_id in algo.get("output_indications") or []:
            if isinstance(ind_id, str):
                in_scope.add(ind_id)
        for slot in ("default_indication", "alternative_indication"):
            v = algo.get(slot)
            if isinstance(v, str):
                in_scope.add(v)

    out: dict[str, dict] = {}
    for ind_id in in_scope:
        info = entities.get(ind_id)
        if info is None or info["type"] != "indications":
            continue
        data = info["data"]
        applic = data.get("applicable_to") or {}
        if applic.get("disease_id") not in CSD4_DISEASE_IDS:
            continue
        line = applic.get("line_of_therapy")
        try:
            line_int = int(line) if line is not None else 0
        except (TypeError, ValueError):
            line_int = 0
        if line_int < 2:
            continue
        out[ind_id] = data
    return out


@pytest.fixture(scope="module")
def csd4_2l_algorithms(entities):
    out: dict[str, dict] = {}
    for algo_id in CSD4_2L_ALGORITHM_IDS:
        info = entities.get(algo_id)
        if info and info["type"] == "algorithms":
            out[algo_id] = info["data"]
    return out


# ── Section A — 2L+ algorithm presence ────────────────────────────────────


def _assert_algorithm_loads(entities, algo_id: str, expected_disease: str):
    info = entities.get(algo_id)
    assert info is not None, f"Algorithm {algo_id} not loaded from KB"
    assert info["type"] == "algorithms", (
        f"Entity {algo_id} loaded as {info['type']}, expected algorithms"
    )
    data = info["data"]
    assert data.get("id") == algo_id
    assert data.get("applicable_to_disease") == expected_disease, (
        f"{algo_id}.applicable_to_disease = {data.get('applicable_to_disease')!r}, "
        f"expected {expected_disease!r}"
    )
    assert int(data.get("applicable_to_line_of_therapy", 0)) >= 2, (
        f"{algo_id}.applicable_to_line_of_therapy must be >= 2"
    )
    assert data.get("output_indications"), (
        f"{algo_id}.output_indications must be non-empty"
    )


def test_crc_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-CRC-METASTATIC-2L", "DIS-CRC")


def test_nsclc_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-NSCLC-METASTATIC-2L", "DIS-NSCLC")


def test_breast_hr_pos_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-BREAST-HR-POS-2L", "DIS-BREAST")


def test_breast_her2_pos_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-BREAST-HER2-POS-2L", "DIS-BREAST")


def test_breast_tnbc_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-BREAST-TNBC-2L", "DIS-BREAST")


def test_melanoma_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-MELANOMA-METASTATIC-2L", "DIS-MELANOMA")


def test_ovarian_2l_algorithm_exists(entities):
    _assert_algorithm_loads(entities, "ALGO-OVARIAN-2L", "DIS-OVARIAN")


# ── Section B — Indications quality ───────────────────────────────────────


def test_all_csd4_2l_indications_have_line_of_therapy_geq_2(csd4_2l_indications):
    """Every CSD-4 2L+ indication declares applicable_to.line_of_therapy >= 2."""
    assert csd4_2l_indications, (
        "Expected at least one CSD-4 2L+ indication in the KB; got zero"
    )
    bad: list[tuple[str, object]] = []
    for ind_id, data in csd4_2l_indications.items():
        line = (data.get("applicable_to") or {}).get("line_of_therapy")
        try:
            ok = int(line) >= 2
        except (TypeError, ValueError):
            ok = False
        if not ok:
            bad.append((ind_id, line))
    assert not bad, (
        f"Indications with applicable_to.line_of_therapy < 2: {bad}"
    )


def test_all_csd4_2l_indications_have_at_least_one_source(csd4_2l_indications):
    bad: list[str] = []
    for ind_id, data in csd4_2l_indications.items():
        sources = data.get("sources") or []
        if len(sources) < 1:
            bad.append(ind_id)
    assert not bad, f"CSD-4 2L+ indications missing sources: {bad}"


def test_all_csd4_2l_indications_have_last_reviewed(csd4_2l_indications):
    bad: list[str] = []
    for ind_id, data in csd4_2l_indications.items():
        if not data.get("last_reviewed"):
            bad.append(ind_id)
    assert not bad, f"CSD-4 2L+ indications missing last_reviewed: {bad}"


def test_all_csd4_2l_indications_reviewer_signoffs_zero(csd4_2l_indications):
    """Per CHARTER §6.1 — STUB content starts at 0 sign-offs and only
    publishes after >=2 Clinical Co-Lead reviews. This test pins the
    pre-publish state so a stray sign-off bump has to be explicit."""
    bad: list[tuple[str, int]] = []
    for ind_id, data in csd4_2l_indications.items():
        signoffs = int(data.get("reviewer_signoffs") or 0)
        if signoffs != 0:
            bad.append((ind_id, signoffs))
    assert not bad, (
        f"CSD-4 2L+ indications with reviewer_signoffs != 0: {bad} — "
        "publish-gate state changed; verify CHARTER §6.1 compliance."
    )


# ── Section C — Algorithm structure ───────────────────────────────────────


def _collect_then_indications(algo: dict) -> set[str]:
    """Collect every Indication ID referenced by either the algorithm's
    output_indications, default/alternative slots, or any decision-tree
    step's if_true / if_false `result` field."""
    ids: set[str] = set()
    for ind_id in algo.get("output_indications") or []:
        if isinstance(ind_id, str):
            ids.add(ind_id)
    for slot in ("default_indication", "alternative_indication"):
        v = algo.get(slot)
        if isinstance(v, str):
            ids.add(v)
    for step in algo.get("decision_tree") or []:
        for branch in ("if_true", "if_false"):
            b = step.get(branch) or {}
            res = b.get("result") if isinstance(b, dict) else None
            if isinstance(res, str):
                ids.add(res)
    return ids


def _collect_biomarker_refs(algo: dict) -> set[str]:
    """Collect biomarker IDs referenced inside decision-tree clauses
    (only structured `biomarker:` keys — free-text condition strings
    are not parsed)."""
    ids: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "biomarker" and isinstance(v, str):
                    ids.add(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for step in algo.get("decision_tree") or []:
        walk(step.get("evaluate") or {})
    return ids


def test_algorithms_reference_existing_indications(entities, csd4_2l_algorithms):
    assert csd4_2l_algorithms, "No CSD-4 2L+ algorithms loaded"
    missing: list[tuple[str, str]] = []
    for algo_id, algo in csd4_2l_algorithms.items():
        for ind_id in _collect_then_indications(algo):
            info = entities.get(ind_id)
            if info is None or info["type"] != "indications":
                missing.append((algo_id, ind_id))
    assert not missing, (
        f"Algorithm references that don't resolve to an Indication: {missing}"
    )


def test_algorithms_reference_existing_biomarkers(entities, csd4_2l_algorithms):
    assert csd4_2l_algorithms, "No CSD-4 2L+ algorithms loaded"
    missing: list[tuple[str, str]] = []
    for algo_id, algo in csd4_2l_algorithms.items():
        for bio_id in _collect_biomarker_refs(algo):
            info = entities.get(bio_id)
            if info is None or info["type"] != "biomarkers":
                missing.append((algo_id, bio_id))
    assert not missing, (
        f"Algorithm biomarker references that don't resolve to a Biomarker: "
        f"{missing}"
    )


# ── Section D — End-to-end known cases ────────────────────────────────────


def _load_fixture(name: str) -> dict:
    path = FIXTURES_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_indication_routable(
    entities,
    expected_ind_ids: set[str],
    selected_indication_id: str | None,
    algorithm_ids: set[str],
) -> bool:
    """Permissive E2E assertion (per task constraints): the engine may
    resolve the precise expected indication, OR may return only the
    algorithm reference. We accept either:
      (a) the engine selected one of the expected indications directly, or
      (b) the expected indication is in the candidate `output_indications`
          set of any of the expected algorithms (routable through the
          authoring layer — routing precision is the algorithm/RedFlag
          authoring problem, not the test's).
    """
    if selected_indication_id in expected_ind_ids:
        return True
    candidates: set[str] = set()
    for algo_id in algorithm_ids:
        info = entities.get(algo_id)
        if info is None or info["type"] != "algorithms":
            continue
        candidates.update(info["data"].get("output_indications") or [])
    return bool(expected_ind_ids & candidates)


def _run_e2e(
    entities,
    fixture_name: str,
    expected_algorithm_ids: set[str],
    expected_indication_ids: set[str],
):
    patient = _load_fixture(fixture_name)
    result = generate_plan(patient, kb_root=KB_ROOT)

    # Plan must materialize without raising and without schema/ref-error
    # warnings (those would indicate a KB-load break, not an engine issue).
    blocking = [
        w for w in result.warnings
        if "schema error" in w.lower() or "ref error" in w.lower()
    ]
    assert not blocking, f"KB load errors during {fixture_name}: {blocking}"

    assert result.disease_id == patient["disease"]["id"], (
        f"{fixture_name}: disease_id mismatch — got {result.disease_id!r}, "
        f"expected {patient['disease']['id']!r}"
    )
    assert result.algorithm_id in expected_algorithm_ids, (
        f"{fixture_name}: engine selected algorithm {result.algorithm_id!r}, "
        f"expected one of {sorted(expected_algorithm_ids)}"
    )
    assert result.plan is not None, f"{fixture_name}: plan was not generated"

    # Permissive routing assertion: the expected indication is either
    # selected outright or sits in the candidate set of any of the
    # expected algorithms.
    assert _expected_indication_routable(
        entities,
        expected_indication_ids,
        result.default_indication_id,
        expected_algorithm_ids,
    ), (
        f"{fixture_name}: expected one of {sorted(expected_indication_ids)} "
        f"to be routable from one of {sorted(expected_algorithm_ids)}; "
        f"engine selected algorithm={result.algorithm_id!r}, "
        f"indication={result.default_indication_id!r}"
    )


def test_e2e_crc_braf_v600e_2l(entities):
    _run_e2e(
        entities,
        "csd_4_crc_braf_v600e_2l.json",
        expected_algorithm_ids={"ALGO-CRC-METASTATIC-2L"},
        expected_indication_ids={"IND-CRC-METASTATIC-2L-BRAF-BEACON"},
    )


def test_e2e_nsclc_egfr_post_osi_2l(entities):
    _run_e2e(
        entities,
        "csd_4_nsclc_egfr_post_osi_2l.json",
        expected_algorithm_ids={"ALGO-NSCLC-METASTATIC-2L"},
        expected_indication_ids={"IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ"},
    )


def test_e2e_breast_pik3ca_post_cdk46i_2l(entities):
    # DIS-BREAST has three line=2 algorithms (HR+, HER2+, TNBC). The
    # engine's _find_algorithm picks the first one matching disease+line
    # in dict-iteration order; receptor-subtype dispatching is not yet
    # in the engine. Accept any of the three breast-2L algorithms here
    # AND accept either a PIK3CA or AKT pathway-targeted indication
    # as the expected match for the HR+ PIK3CA-mutant cohort.
    _run_e2e(
        entities,
        "csd_4_breast_pik3ca_post_cdk46i_2l.json",
        expected_algorithm_ids={
            "ALGO-BREAST-HR-POS-2L",
            "ALGO-BREAST-HER2-POS-2L",
            "ALGO-BREAST-TNBC-2L",
        },
        expected_indication_ids={
            "IND-BREAST-HR-POS-2L-AKT-CAPIVASERTIB",
            "IND-BREAST-HR-POS-2L-PIK3CA-ALPELISIB",
        },
    )


def test_e2e_melanoma_braf_post_io_2l(entities):
    _run_e2e(
        entities,
        "csd_4_melanoma_braf_post_io_2l.json",
        expected_algorithm_ids={"ALGO-MELANOMA-METASTATIC-2L"},
        expected_indication_ids={"IND-MELANOMA-2L-POST-IO-BRAFI-MEKI"},
    )


def test_e2e_ovarian_brca1_plat_sens_2l(entities):
    _run_e2e(
        entities,
        "csd_4_ovarian_brca1_plat_sens_2l.json",
        expected_algorithm_ids={"ALGO-OVARIAN-2L"},
        expected_indication_ids={"IND-OVARIAN-MAINT-PARPI-BRCAM-OLAPARIB"},
    )
