"""Tracer-bullet tests for MDT protocol generator (Phase 1).

Plan: docs/plans/mdt_protocol_generator_2026-04-26.md
Module: knowledge_base/engine/mdt_protocol.py

Three required behaviours validated here:
  1. Vote → event mapping is correct + deterministic + audit-complete
  2. HTML protocol surfaces dissent visibly + all required sections
  3. Persistence + rehydration into MDT provenance graph round-trips
     (i.e. protocol generation never silently loses council decisions)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledge_base.engine import event_store, generate_plan, orchestrate_mdt
from knowledge_base.engine.mdt_protocol import (
    MDTProtocolInput,
    ProtocolVote,
    build_mdt_protocol,
    protocol_votes_to_events,
    save_mdt_protocol_events,
)

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def _input_factory(plan_id: str, patient_id: str = "MM-HR-001") -> MDTProtocolInput:
    return MDTProtocolInput(
        patient_id=patient_id,
        plan_id=plan_id,
        meeting_id="MDT-2026-04-26-001",
        meeting_date="2026-04-26",
        chair_role="medical_oncologist",
        chair_id="dr-tymoshenko",
        votes=[
            ProtocolVote(
                role_id="hematologist",
                vote="agree",
                actor_id="dr-tkachenko",
            ),
            ProtocolVote(
                role_id="clinical_pharmacist",
                vote="dissent",
                actor_id="dr-bilyk",
                comment="Lenalidomide dose-modify for CrCl 45 mL/min",
            ),
            ProtocolVote(
                role_id="radiologist",
                vote="abstain",
            ),
        ],
        final_decision="approved_with_modifications",
        final_summary=(
            "VRd backbone confirmed; lenalidomide reduced to 15 mg per "
            "clinical pharmacist input; bortezomib SC; q3w cycles."
        ),
        pending_questions=[
            "Verify HBV serology before lenalidomide dose 1",
        ],
    )


# ── 1. Vote → event mapping ──────────────────────────────────────────────


def test_vote_event_mapping_is_correct_and_deterministic():
    """Each vote + final decision produces the expected EventType /
    TargetType. Re-running the generator with the same input produces
    identical event_ids (idempotency for skip_if_exists path)."""

    p = _input_factory(plan_id="PLAN-MM-HR-001-V1")
    events_a = protocol_votes_to_events(p)
    events_b = protocol_votes_to_events(p)

    # 3 votes + 1 final + 1 pending question = 5 events
    assert len(events_a) == 5

    by_role = {(e.actor_role, e.event_type): e for e in events_a}
    assert by_role[("hematologist", "approved")].target_type == "plan_section"
    assert (
        by_role[("clinical_pharmacist", "rejected")].summary
        .startswith("MDT dissent")
    )
    # Abstain → requested_data (audit-completeness refinement, not "no event")
    assert by_role[("radiologist", "requested_data")].summary.startswith(
        "MDT abstain"
    )
    # Final decision (approved_with_modifications) → modified
    final_evs = [e for e in events_a if "final decision" in e.summary]
    assert len(final_evs) == 1
    assert final_evs[0].event_type == "modified"
    assert final_evs[0].actor_role == "medical_oncologist"
    assert final_evs[0].actor_id == "dr-tymoshenko"

    # Determinism: same input → same event_ids (so re-running is idempotent
    # when paired with append_event(skip_if_exists=True))
    assert [e.event_id for e in events_a] == [e.event_id for e in events_b]

    # Each event references the protocol via evidence_refs
    pid = "PROT-MM-HR-001-MDT-2026-04-26-001"
    assert all(pid in e.evidence_refs for e in events_a)


def test_dissent_without_comment_is_rejected_at_validation():
    """Audit safety: a dissent that doesn't say WHY is unactionable, so
    we raise on construction rather than write a useless event."""

    bad = MDTProtocolInput(
        patient_id="MM-HR-001",
        plan_id="PLAN-MM-HR-001-V1",
        meeting_id="MDT-2026-04-26-001",
        meeting_date="2026-04-26",
        chair_role="medical_oncologist",
        chair_id="dr-chair",
        votes=[
            ProtocolVote(
                role_id="hematologist",
                vote="dissent",
                actor_id="dr-x",
                comment=None,  # ← contract violation
            ),
        ],
        final_decision="rejected_needs_rediscussion",
        final_summary="Cannot proceed.",
    )
    with pytest.raises(ValueError, match="dissent"):
        protocol_votes_to_events(bad)


def test_agree_dissent_require_actor_id_for_audit_trail():
    """Without actor_id, 'hematologist agreed' is not auditable."""

    no_actor = MDTProtocolInput(
        patient_id="MM-HR-001",
        plan_id="PLAN-MM-HR-001-V1",
        meeting_id="MDT-2026-04-26-001",
        meeting_date="2026-04-26",
        chair_role="medical_oncologist",
        chair_id="dr-chair",
        votes=[
            ProtocolVote(role_id="hematologist", vote="agree", actor_id=None),
        ],
        final_decision="approved_as_is",
        final_summary="OK.",
    )
    with pytest.raises(ValueError, match="actor_id"):
        protocol_votes_to_events(no_actor)


# ── 2. HTML render ───────────────────────────────────────────────────────


def test_protocol_html_surfaces_dissent_visibly_and_all_sections():
    """Per plan acceptance criterion: 'every dissent must be visible,
    not hidden in footnotes'. Also smoke-tests presence of all required
    sections (final decision, votes table, signatures, footer)."""

    res = build_mdt_protocol(
        _input_factory(plan_id="PLAN-MM-HR-001-V1"),
        plan_summary="VRd backbone (bortezomib + lenalidomide + dexamethasone), 4 cycles induction.",
        sources_summary=["SRC-NCCN-MM-2025", "SRC-ESMO-MM-2023"],
    )
    html = res.html

    # Protocol id in document header
    assert "PROT-MM-HR-001-MDT-2026-04-26-001" in html

    # Final-decision section, with UA label
    assert "Затверджено зі змінами" in html  # final_decision label
    assert "lenalidomide reduced to 15 mg" in html

    # Dissent block — class="dissent" + dissent reason in body, not just table
    assert "class='dissent'" in html
    assert "Lenalidomide dose-modify" in html
    assert html.count("Lenalidomide dose-modify") >= 2  # appears in BOTH votes table AND dissent block

    # Votes table contains all three roles
    for role in ("hematologist", "clinical_pharmacist", "radiologist"):
        assert role in html

    # Signatures section + chair line
    assert "Підписи" in html
    assert "Голова консиліуму" in html
    assert "dr-tymoshenko" in html

    # Pending question surfaced
    assert "HBV serology" in html

    # Sources block embedded
    assert "SRC-NCCN-MM-2025" in html

    # FDA Criterion-4 disclosure (CHARTER §15.1)
    assert "інформаційна" in html.lower()
    assert "CHARTER" in html


# ── 3. Persistence + rehydration round-trip ──────────────────────────────


def test_protocol_events_round_trip_through_event_store(tmp_path, monkeypatch):
    """Save protocol events → re-read them → confirm they are merged
    back into a freshly-orchestrated MDT provenance graph. This is the
    integration with `merge_events_into_graph` already wired into
    `orchestrate_mdt` (commit 52a8917)."""

    # Redirect event_store to tmp_path so we never touch real patient_plans/.
    monkeypatch.setattr(event_store, "DEFAULT_ROOT", tmp_path)

    patient = _patient("patient_mm_high_risk.json")
    plan_result = generate_plan(patient, kb_root=KB_ROOT)
    assert plan_result.plan is not None  # MM should generate a plan

    # 1. Build protocol + persist its events
    protocol_input = _input_factory(
        plan_id=plan_result.plan.id,
        patient_id=plan_result.patient_id,
    )
    res = build_mdt_protocol(protocol_input)
    save_mdt_protocol_events(plan_result.patient_id, res.events)

    # 2. Idempotency: a second save MUST NOT duplicate event lines.
    # `read_events` captures DEFAULT_ROOT at function-def time — monkeypatch
    # of the module attribute doesn't reach it, so pass root= explicitly.
    save_mdt_protocol_events(plan_result.patient_id, res.events)
    persisted = event_store.read_events(plan_result.patient_id, root=tmp_path)
    expected_ids = {e.event_id for e in res.events}
    persisted_ids = [e.event_id for e in persisted]
    assert set(persisted_ids) == expected_ids
    # No duplicates after second save
    assert len(persisted_ids) == len(set(persisted_ids))

    # 3. Re-orchestrate MDT — events MUST rehydrate into the graph via
    # the wiring in mdt_orchestrator._bootstrap_provenance + merge.
    mdt = orchestrate_mdt(patient, plan_result, kb_root=KB_ROOT)
    rehydrated_ids = {e.event_id for e in mdt.provenance.events}
    assert expected_ids.issubset(rehydrated_ids), (
        f"Protocol events lost on re-orchestration. Missing: "
        f"{expected_ids - rehydrated_ids}"
    )

    # 4. Plan selection MUST NOT change just because protocol exists.
    # (CHARTER §8.3 — generator never alters clinical recommendation.)
    assert plan_result.default_indication_id is not None
    plan_result2 = generate_plan(patient, kb_root=KB_ROOT)
    assert plan_result.default_indication_id == plan_result2.default_indication_id
