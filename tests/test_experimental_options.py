"""Phase C tracer-bullet tests for the experimental-options enumerator.

Plan: docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §3.3 + §5.4.
Module: knowledge_base/engine/experimental_options.py

Five behaviours validated here:
  1. With a stub search_fn, recruiting trials are returned as ExperimentalTrial.
  2. Closed-enrollment statuses (COMPLETED / TERMINATED) are filtered out.
  3. UA-site presence is surfaced via `sites_ua` when ctgov reports a UA country.
  4. ctgov failures + no-search-fn return an empty bundle, never raise — per
     plan §3.3 ("Не падає"). This protects the engine when offline.
  5. Cache returns the same option for the same query signature.

Architectural invariant (CHARTER §8.3 + feedback_efficacy_over_registration.md):
the enumerator is render-time metadata only. It exposes alternatives; it
never changes which Indication the engine selects. That invariant is
guarded by `tests/test_plan_invariant_ua_availability.py`; this file
just validates the enumerator's contract.
"""

from __future__ import annotations

import pytest

from knowledge_base.engine import (
    clear_experimental_cache,
    enumerate_experimental_options,
)
from knowledge_base.engine.experimental_options import TrialQuery
from knowledge_base.schemas.experimental_option import ExperimentalOption


def _study(
    nct_id: str,
    *,
    status: str = "RECRUITING",
    title: str = "Sample trial",
    countries: list[str] | None = None,
    eligibility: str = "",
    phase: str = "PHASE2",
    sponsor: str = "Acme Onc",
) -> dict:
    """Mimics one entry returned by ctgov_client.search_trials."""
    return {
        "nct_id": nct_id,
        "title": title,
        "status": status,
        "phase": phase,
        "sponsor": sponsor,
        "summary": "Brief summary.",
        "eligibility_criteria": eligibility,
        "countries": countries or [],
    }


@pytest.fixture(autouse=True)
def _reset_cache():
    clear_experimental_cache()
    yield
    clear_experimental_cache()


# ── 1. Happy path ───────────────────────────────────────────────────────


def test_enumerate_returns_recruiting_trials():
    studies = [
        _study("NCT00000001", title="FLAURA2", phase="PHASE3"),
        _study("NCT00000002", title="MARIPOSA", phase="PHASE3"),
    ]
    opt = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="Non-small cell lung cancer",
        biomarker_profile="EGFR mutation",
        line_of_therapy=1,
        search_fn=lambda **_: studies,
    )

    assert isinstance(opt, ExperimentalOption)
    assert opt.id.startswith("EXPER-DIS-NSCLC-EGFR_MUTATION-L1-")
    assert opt.disease_id == "DIS-NSCLC"
    assert opt.molecular_subtype == "EGFR mutation"
    assert opt.line_of_therapy == 1
    assert [t.nct_id for t in opt.trials] == ["NCT00000001", "NCT00000002"]
    assert opt.trials[0].title == "FLAURA2"
    assert opt.trials[0].phase == "PHASE3"
    assert opt.last_synced is not None


# ── 2. Status filter ────────────────────────────────────────────────────


def test_closed_enrollment_studies_are_filtered():
    studies = [
        _study("NCT-OPEN", status="RECRUITING"),
        _study("NCT-DONE", status="COMPLETED"),
        _study("NCT-TERM", status="TERMINATED"),
        _study("NCT-WITH", status="WITHDRAWN"),
        _study("NCT-INV",  status="ENROLLING_BY_INVITATION"),
        _study("NCT-ACT",  status="ACTIVE_NOT_RECRUITING"),
    ]
    opt = enumerate_experimental_options(
        disease_id="DIS-MM",
        disease_term="Multiple myeloma",
        search_fn=lambda **_: studies,
    )
    surfaced = {t.nct_id for t in opt.trials}
    assert surfaced == {"NCT-OPEN", "NCT-INV", "NCT-ACT"}


# ── 3. UA-site enrichment ───────────────────────────────────────────────


def test_ua_country_surfaces_in_sites_ua():
    studies = [
        _study("NCT-UA",   countries=["US", "UA", "DE"]),
        _study("NCT-NOUA", countries=["US", "DE"]),
        _study("NCT-NAME", countries=["Ukraine"]),  # full name, not ISO
    ]
    opt = enumerate_experimental_options(
        disease_id="DIS-CLL",
        disease_term="Chronic lymphocytic leukemia",
        search_fn=lambda **_: studies,
    )
    by_id = {t.nct_id: t for t in opt.trials}
    assert by_id["NCT-UA"].sites_ua == ["UA"]
    assert by_id["NCT-NOUA"].sites_ua == []
    assert by_id["NCT-NAME"].sites_ua == ["UA"]
    # Full country list still preserved on every trial
    assert by_id["NCT-UA"].countries == ["US", "UA", "DE"]


# ── 4. Eligibility split ────────────────────────────────────────────────


def test_eligibility_text_split_into_inclusion_and_exclusion():
    elig = (
        "Inclusion Criteria:\n- Age >= 18\n- ECOG 0-1\n\n"
        "Exclusion Criteria:\n- Active CNS disease\n- Prior anti-PD1"
    )
    studies = [_study("NCT-E", eligibility=elig)]
    opt = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
        search_fn=lambda **_: studies,
    )
    t = opt.trials[0]
    assert t.inclusion_summary is not None and "ECOG 0-1" in t.inclusion_summary
    assert t.exclusion_summary is not None and "Active CNS" in t.exclusion_summary


# ── 5. Offline / failure-path safety ────────────────────────────────────


def test_no_search_fn_returns_empty_bundle_with_note():
    opt = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
    )
    assert opt.trials == []
    assert opt.notes is not None and "ctgov search not configured" in opt.notes


def test_search_fn_exception_returns_empty_bundle_with_note():
    def _boom(**_):
        raise RuntimeError("network down")

    opt = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
        search_fn=_boom,
    )
    assert opt.trials == []
    assert opt.notes is not None and "ctgov search failed" in opt.notes
    assert "network down" in opt.notes


# ── 6. Cache behaviour ──────────────────────────────────────────────────


def test_cache_returns_same_option_for_same_query():
    call_count = {"n": 0}

    def _counting_fn(**_):
        call_count["n"] += 1
        return [_study("NCT-1")]

    o1 = enumerate_experimental_options(
        disease_id="DIS-X",
        disease_term="x cancer",
        biomarker_profile="BRCA1",
        line_of_therapy=2,
        search_fn=_counting_fn,
    )
    o2 = enumerate_experimental_options(
        disease_id="DIS-X",
        disease_term="x cancer",
        biomarker_profile="BRCA1",
        line_of_therapy=2,
        search_fn=_counting_fn,
    )
    assert call_count["n"] == 1, "cache should suppress the second call"
    assert o1 is o2

    # Different signature → fresh call
    enumerate_experimental_options(
        disease_id="DIS-X",
        disease_term="x cancer",
        biomarker_profile="BRCA2",
        line_of_therapy=2,
        search_fn=_counting_fn,
    )
    assert call_count["n"] == 2


def test_query_signature_is_stable():
    a = TrialQuery(disease_term="NSCLC", biomarker_term="EGFR", line_of_therapy=1)
    b = TrialQuery(disease_term="NSCLC", biomarker_term="EGFR", line_of_therapy=1)
    c = TrialQuery(disease_term="NSCLC", biomarker_term="EGFR", line_of_therapy=2)
    assert a.signature() == b.signature()
    assert a.signature() != c.signature()


# ── 7. generate_plan() integration ──────────────────────────────────────


def test_generate_plan_attaches_experimental_options_when_search_fn_given():
    """When a search_fn is passed, generate_plan attaches an
    ExperimentalOption to PlanResult — and the engine selection
    is identical to a control run without it (CHARTER §8.3 +
    plan §3.2 invariant: append-only, never a selection signal)."""

    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan

    REPO_ROOT = Path(__file__).parent.parent
    KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    EXAMPLES = REPO_ROOT / "examples"

    patient = json.loads(
        (EXAMPLES / "patient_mm_high_risk.json").read_text(encoding="utf-8")
    )

    seen_calls: list[dict] = []

    def _stub_search(**kwargs):
        seen_calls.append(kwargs)
        return [_study("NCT-EXAMPLE", title="Stub trial", countries=["UA", "DE"])]

    control = generate_plan(patient, kb_root=KB_ROOT)
    with_trial = generate_plan(
        patient, kb_root=KB_ROOT, experimental_search_fn=_stub_search
    )

    # Engine selection unchanged — the invariant.
    assert control.default_indication_id == with_trial.default_indication_id
    assert control.alternative_indication_id == with_trial.alternative_indication_id
    assert [t.indication_id for t in (control.plan.tracks if control.plan else [])] == \
           [t.indication_id for t in (with_trial.plan.tracks if with_trial.plan else [])]

    # Experimental option attached on the second run, absent on control.
    assert control.experimental_options is None
    assert with_trial.experimental_options is not None
    opt = with_trial.experimental_options
    assert opt.disease_id == with_trial.disease_id
    assert [t.nct_id for t in opt.trials] == ["NCT-EXAMPLE"]
    assert opt.trials[0].sites_ua == ["UA"]

    # Search function received the disease term + line of therapy.
    assert len(seen_calls) == 1
    assert seen_calls[0]["max_results"] >= 1
    assert seen_calls[0]["condition"]  # non-empty disease term


def test_plan_html_renders_experimental_track_section():
    """End-to-end: generate_plan with a stub search_fn → render_plan_html
    surfaces the experimental-track section with the trial NCT, UA badge,
    and the engine-selection-unchanged disclosure."""

    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan, render_plan_html

    REPO_ROOT = Path(__file__).parent.parent
    KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    EXAMPLES = REPO_ROOT / "examples"

    patient = json.loads(
        (EXAMPLES / "patient_mm_high_risk.json").read_text(encoding="utf-8")
    )

    def _stub_search(**_):
        return [
            _study(
                "NCT05153486",
                title="FLAURA2",
                countries=["UA", "US"],
                phase="PHASE3",
                sponsor="AstraZeneca",
                eligibility=(
                    "Inclusion Criteria:\n- Age >= 18\n- ECOG 0-1\n\n"
                    "Exclusion Criteria:\n- Active CNS disease"
                ),
            ),
        ]

    res = generate_plan(patient, kb_root=KB_ROOT, experimental_search_fn=_stub_search)
    html = render_plan_html(res)

    assert 'class="experimental-track"' in html
    assert "Експериментальні опції" in html
    assert "NCT05153486" in html
    assert "FLAURA2" in html
    assert "PHASE3" in html
    assert 'class="badge badge--ua"' in html
    assert "ECOG 0-1" in html  # eligibility excerpt surfaces
    # Render-time disclaimer that engine selection is unchanged
    assert "engine selection не змінюється" in html
    # External link to ctgov
    assert "clinicaltrials.gov/study/NCT05153486" in html


def test_plan_html_renders_unset_placeholder_when_no_search_fn():
    """When no search_fn was passed, render still emits the section with a
    'sync needed' placeholder (per plan §3.3 — visible third track even
    when offline)."""

    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan, render_plan_html

    REPO_ROOT = Path(__file__).parent.parent
    KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    EXAMPLES = REPO_ROOT / "examples"

    patient = json.loads(
        (EXAMPLES / "patient_mm_high_risk.json").read_text(encoding="utf-8")
    )
    res = generate_plan(patient, kb_root=KB_ROOT)
    html = render_plan_html(res)

    assert 'experimental-track--unset' in html
    assert "Дані недоступні" in html
    assert "ClinicalTrials.gov" in html


def test_generate_plan_swallows_search_fn_failure_into_warnings():
    """Engine must not raise if ctgov is broken — it logs a warning
    and returns the plan with experimental_options=None."""

    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan

    REPO_ROOT = Path(__file__).parent.parent
    KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    EXAMPLES = REPO_ROOT / "examples"

    patient = json.loads(
        (EXAMPLES / "patient_mm_high_risk.json").read_text(encoding="utf-8")
    )

    # `enumerate_experimental_options` itself catches the inner exception
    # and returns a notes-bearing bundle, so this path is the "outer"
    # safety: we monkey-patch enumerate to raise, simulating a contract
    # break, and assert generate_plan still returns a PlanResult.
    from knowledge_base.engine import plan as plan_module

    orig = plan_module.enumerate_experimental_options

    def _raise(**_):
        raise RuntimeError("simulated enumerator crash")

    plan_module.enumerate_experimental_options = _raise
    try:
        res = generate_plan(
            patient, kb_root=KB_ROOT, experimental_search_fn=lambda **_: []
        )
    finally:
        plan_module.enumerate_experimental_options = orig

    assert res.plan is not None
    assert res.experimental_options is None
    assert any("experimental options skipped" in w for w in res.warnings)


# ── 6. On-disk TTL cache (plan §5.4 task 2) ─────────────────────────────


def test_disk_cache_writes_and_reads(tmp_path):
    """A first call with a search_fn writes a JSON cache file under
    cache_root; a second call with search_fn=None still returns the
    cached option (proving the read path)."""
    studies = [_study("NCT00099001", title="Cached trial")]
    calls = {"n": 0}

    def stub(**_):
        calls["n"] += 1
        return studies

    o1 = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
        biomarker_profile="EGFR mutation",
        line_of_therapy=1,
        search_fn=stub,
        cache_root=tmp_path,
    )
    assert calls["n"] == 1
    assert any(p.name.startswith("ctgov_") and p.suffix == ".json"
               for p in tmp_path.iterdir())

    # Simulate fresh process: clear in-process cache, call again with
    # search_fn=None; disk hit must return the same trial set.
    clear_experimental_cache()
    o2 = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
        biomarker_profile="EGFR mutation",
        line_of_therapy=1,
        search_fn=None,
        cache_root=tmp_path,
    )
    assert calls["n"] == 1, "search_fn must not be called on cache hit"
    assert [t.nct_id for t in o2.trials] == ["NCT00099001"]


def test_disk_cache_respects_ttl(tmp_path):
    """When the on-disk file is older than `cache_ttl_days`, the cache
    is treated as a miss and the search_fn runs again."""
    import json
    from datetime import datetime, timedelta, timezone

    studies = [_study("NCT00099002", title="Stale-cache trial")]
    calls = {"n": 0}

    def stub(**_):
        calls["n"] += 1
        return studies

    enumerate_experimental_options(
        disease_id="DIS-MM",
        disease_term="Multiple myeloma",
        search_fn=stub,
        cache_root=tmp_path,
    )
    assert calls["n"] == 1

    # Backdate the on-disk cache file by 30 days so a 7-day TTL expires
    cache_files = list(tmp_path.glob("ctgov_*.json"))
    assert cache_files, "expected one cache file"
    payload = json.loads(cache_files[0].read_text(encoding="utf-8"))
    payload["cached_at"] = (
        datetime.now(timezone.utc) - timedelta(days=30)
    ).isoformat()
    cache_files[0].write_text(json.dumps(payload), encoding="utf-8")

    clear_experimental_cache()
    enumerate_experimental_options(
        disease_id="DIS-MM",
        disease_term="Multiple myeloma",
        search_fn=stub,
        cache_root=tmp_path,
        cache_ttl_days=7,
    )
    assert calls["n"] == 2, "stale cache must trigger re-fetch"


def test_generate_plan_uses_cache_only_mode(tmp_path):
    """With `experimental_cache_root` set and `experimental_search_fn=None`
    (Pyodide's reality), `generate_plan` must surface trials baked into the
    on-disk cache. Proves the cache-only plumbing in `plan.py`."""

    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan

    REPO_ROOT = Path(__file__).parent.parent
    KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    EXAMPLES = REPO_ROOT / "examples"

    patient = json.loads(
        (EXAMPLES / "patient_mm_high_risk.json").read_text(encoding="utf-8")
    )

    # First call: live search_fn populates the cache at tmp_path.
    studies = [_study("NCT09001000", title="Cached MM trial", phase="PHASE2")]
    res1 = generate_plan(
        patient,
        kb_root=KB_ROOT,
        experimental_search_fn=lambda **_: studies,
        experimental_cache_root=tmp_path,
    )
    assert res1.experimental_options is not None
    assert [t.nct_id for t in res1.experimental_options.trials] == ["NCT09001000"]

    # Second call: cache-only (no search_fn). Must hit the disk cache and
    # return the same trial without raising or returning the empty bundle.
    clear_experimental_cache()
    res2 = generate_plan(
        patient,
        kb_root=KB_ROOT,
        experimental_cache_root=tmp_path,
    )
    assert res2.experimental_options is not None
    assert [t.nct_id for t in res2.experimental_options.trials] == ["NCT09001000"]


def test_disk_cache_corrupted_file_falls_through(tmp_path):
    """A corrupted JSON file must not raise; the function falls back to
    the search_fn path so the engine never blocks on cache I/O."""
    bad = tmp_path / "ctgov_deadbeef0000.json"
    bad.write_text("{not valid json", encoding="utf-8")

    studies = [_study("NCT00099003", title="Recovery trial")]
    o = enumerate_experimental_options(
        disease_id="DIS-NSCLC",
        disease_term="NSCLC",
        biomarker_profile="ALK fusion",
        search_fn=lambda **_: studies,
        cache_root=tmp_path,
    )
    assert [t.nct_id for t in o.trials] == ["NCT00099003"]
