"""MDT Protocol generator — formal council-protocol document.

Tracer-bullet for Phase 1 of `docs/plans/mdt_protocol_generator_2026-04-26.md`.

Inputs: PlanResult + MDTOrchestrationResult + per-role votes + final
decision.

Outputs:
  - MDTProtocolResult.html (print-ready single-file HTML)
  - MDTProtocolResult.events (list[ProvenanceEvent]) — written to
    patient_plans/<patient_id>/events.jsonl via event_store.append_events

Per CHARTER §8.3 the generator does NOT compute clinical recommendations.
It aggregates votes already made by humans and formats them as a formal
document. Plan selection is unchanged by protocol generation.

Refinements from plan review (2026-04-26):
  - dissent requires `comment`
  - actor_id required for agree / dissent / final decision (audit trail)
  - abstain DOES write a `requested_data` event (audit completeness;
    "X invited, did not attend" is itself audit-relevant)
  - final_decision enum maps deterministically to one EventType
  - protocol_id deterministic from (patient, meeting); event_ids
    deterministic from (protocol_id, role, vote-index)
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Literal, Optional

from .provenance import ProvenanceEvent, make_event, now_iso


# ── Public types ──────────────────────────────────────────────────────────


VoteKind = Literal["agree", "dissent", "abstain"]

FinalDecision = Literal[
    "approved_as_is",
    "approved_with_modifications",
    "deferred_pending_data",
    "rejected_needs_rediscussion",
]


@dataclass
class ProtocolVote:
    role_id: str
    vote: VoteKind
    actor_id: Optional[str] = None  # required for agree/dissent
    comment: Optional[str] = None   # required for dissent
    target_track_id: Optional[str] = None  # default: plan_id


@dataclass
class MDTProtocolInput:
    patient_id: str
    plan_id: str
    meeting_id: str
    meeting_date: str  # ISO YYYY-MM-DD or full ISO timestamp
    chair_role: str
    chair_id: Optional[str]
    votes: list[ProtocolVote]
    final_decision: FinalDecision
    final_summary: str
    pending_questions: list[str] = field(default_factory=list)
    supersedes_protocol_id: Optional[str] = None  # for repeat MDT meetings


@dataclass
class MDTProtocolResult:
    protocol_id: str
    html: str
    events: list[ProvenanceEvent]
    json_payload: dict  # serializable record of inputs + outputs


# ── Validation ────────────────────────────────────────────────────────────


def _validate(p: MDTProtocolInput) -> None:
    if not p.patient_id:
        raise ValueError("patient_id is required")
    if not p.plan_id:
        raise ValueError("plan_id is required")
    if not p.meeting_id:
        raise ValueError("meeting_id is required")
    if p.final_decision in (
        "approved_as_is",
        "approved_with_modifications",
        "rejected_needs_rediscussion",
    ) and not p.chair_id:
        raise ValueError(
            f"chair_id is required for final_decision={p.final_decision!r} "
            "(audit-trail attribution)"
        )
    seen_role_actor: set[tuple[str, Optional[str]]] = set()
    for v in p.votes:
        if v.vote == "dissent" and not (v.comment and v.comment.strip()):
            raise ValueError(
                f"dissent vote from {v.role_id!r} requires a non-empty comment"
            )
        if v.vote in ("agree", "dissent") and not v.actor_id:
            raise ValueError(
                f"{v.vote!r} vote from {v.role_id!r} requires actor_id "
                "(audit-trail attribution)"
            )
        key = (v.role_id, v.actor_id)
        if key in seen_role_actor:
            raise ValueError(
                f"duplicate vote from {v.role_id!r} actor={v.actor_id!r}"
            )
        seen_role_actor.add(key)


# ── Vote → event mapping ──────────────────────────────────────────────────


_VOTE_EVENT_TYPE: dict[VoteKind, str] = {
    "agree": "approved",
    "dissent": "rejected",
    "abstain": "requested_data",
}

_FINAL_EVENT_TYPE: dict[FinalDecision, str] = {
    "approved_as_is": "approved",
    "approved_with_modifications": "modified",
    "deferred_pending_data": "added_question",
    "rejected_needs_rediscussion": "rejected",
}


def _protocol_id(p: MDTProtocolInput) -> str:
    """Deterministic id: PROT-<patient>-<meeting>. Stable across re-runs."""
    return f"PROT-{p.patient_id.upper()}-{p.meeting_id.upper()}"


def _event_id(protocol_id: str, suffix: str) -> str:
    """Stable per-vote event_id within a protocol — re-running the
    generator with same inputs produces same ids (idempotent appends
    when paired with `skip_if_exists=True`)."""
    seed = f"{protocol_id}|{suffix}"
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
    return f"ev-{h}"


def protocol_votes_to_events(p: MDTProtocolInput) -> list[ProvenanceEvent]:
    _validate(p)
    pid = _protocol_id(p)
    target_id_default = p.plan_id
    events: list[ProvenanceEvent] = []
    ts = p.meeting_date if "T" in p.meeting_date else f"{p.meeting_date}T00:00:00+00:00"

    for idx, v in enumerate(p.votes):
        target_id = v.target_track_id or target_id_default
        ev_type = _VOTE_EVENT_TYPE[v.vote]
        if v.vote == "agree":
            summary = (
                f"MDT vote: {v.role_id} agreed with plan as presented "
                f"(meeting {p.meeting_id})."
            )
        elif v.vote == "dissent":
            summary = (
                f"MDT dissent: {v.role_id} disagreed; reason: {v.comment} "
                f"(meeting {p.meeting_id})."
            )
        else:  # abstain
            who = v.actor_id or "unspecified"
            summary = (
                f"MDT abstain: {v.role_id} (actor {who}) did not vote "
                f"(meeting {p.meeting_id})."
            )
        events.append(
            make_event(
                event_id=_event_id(pid, f"vote-{idx}-{v.role_id}"),
                actor_role=v.role_id,
                actor_id=v.actor_id,
                event_type=ev_type,  # type: ignore[arg-type]
                target_type="plan_section",
                target_id=target_id,
                summary=summary,
                evidence_refs=[pid],
                timestamp=ts,
            )
        )

    # Final-decision event — chair-attributed
    fin_event_type = _FINAL_EVENT_TYPE[p.final_decision]
    fin_summary = f"MDT final decision: {p.final_decision}. {p.final_summary}".strip()
    events.append(
        make_event(
            event_id=_event_id(pid, "final-decision"),
            actor_role=p.chair_role,
            actor_id=p.chair_id,
            event_type=fin_event_type,  # type: ignore[arg-type]
            target_type="plan_section",
            target_id=p.plan_id,
            summary=fin_summary,
            evidence_refs=[pid],
            timestamp=ts,
        )
    )

    # Pending-question events (one per question) — surface them in the
    # provenance graph so a re-render of the plan picks them up.
    for qi, q in enumerate(p.pending_questions or []):
        events.append(
            make_event(
                event_id=_event_id(pid, f"pending-{qi}"),
                actor_role=p.chair_role,
                actor_id=p.chair_id,
                event_type="added_question",
                target_type="plan_section",
                target_id=p.plan_id,
                summary=f"MDT pending question: {q}",
                evidence_refs=[pid],
                timestamp=ts,
            )
        )

    return events


# ── HTML render (print-ready, single file) ────────────────────────────────


def _esc(s: object) -> str:
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


_FINAL_LABELS_UA: dict[FinalDecision, str] = {
    "approved_as_is": "Затверджено без змін",
    "approved_with_modifications": "Затверджено зі змінами",
    "deferred_pending_data": "Відкладено до отримання даних",
    "rejected_needs_rediscussion": "Відхилено, потребує повторного обговорення",
}

_VOTE_LABELS_UA: dict[VoteKind, str] = {
    "agree": "погодився",
    "dissent": "не погодився",
    "abstain": "утримався / відсутній",
}


def render_mdt_protocol_html(
    p: MDTProtocolInput,
    *,
    plan_summary: Optional[str] = None,
    sources_summary: Optional[Iterable[str]] = None,
) -> str:
    """Print-ready single-file HTML protocol. UA-first wording."""

    pid = _protocol_id(p)
    final_label = _FINAL_LABELS_UA[p.final_decision]

    # Votes table
    vote_rows: list[str] = []
    for v in p.votes:
        vote_rows.append(
            f"<tr class='vote-{v.vote}'>"
            f"<td>{_esc(v.role_id)}</td>"
            f"<td>{_VOTE_LABELS_UA[v.vote]}</td>"
            f"<td>{_esc(v.actor_id) or '—'}</td>"
            f"<td>{_esc(v.comment) or ''}</td>"
            f"</tr>"
        )

    # Dissents — visible block, NOT footnote
    dissents = [v for v in p.votes if v.vote == "dissent"]
    dissent_block = ""
    if dissents:
        dissent_items = "".join(
            f"<li><strong>{_esc(d.role_id)}</strong> ({_esc(d.actor_id)}): "
            f"{_esc(d.comment)}</li>"
            for d in dissents
        )
        dissent_block = (
            f"<section class='dissent'><h2>Окремі думки (dissent)</h2>"
            f"<ul>{dissent_items}</ul></section>"
        )

    pending_block = ""
    if p.pending_questions:
        items = "".join(f"<li>{_esc(q)}</li>" for q in p.pending_questions)
        pending_block = (
            f"<section><h2>Відкриті питання / pending data</h2>"
            f"<ul>{items}</ul></section>"
        )

    src_block = ""
    if sources_summary:
        src_items = "".join(f"<li>{_esc(s)}</li>" for s in sources_summary)
        src_block = (
            f"<section><h2>Джерела та підстава рішення</h2>"
            f"<ul class='sources'>{src_items}</ul></section>"
        )

    plan_block = ""
    if plan_summary:
        plan_block = (
            f"<section><h2>Стислий зміст плану</h2>"
            f"<div class='plan-summary'>{_esc(plan_summary)}</div></section>"
        )

    supersedes_note = ""
    if p.supersedes_protocol_id:
        supersedes_note = (
            f"<p class='supersedes'>Замінює протокол: "
            f"<code>{_esc(p.supersedes_protocol_id)}</code></p>"
        )

    style = """
      body { font-family: 'Source Sans 3', Arial, sans-serif; color: #1a1a1a;
             max-width: 780px; margin: 24px auto; padding: 0 24px; line-height: 1.5; }
      h1 { font-size: 22px; margin: 0 0 4px; }
      h2 { font-size: 16px; margin-top: 24px; border-bottom: 1px solid #ccc;
           padding-bottom: 4px; }
      .doc-meta { font-size: 12px; color: #555; margin-bottom: 16px; }
      table.votes { width: 100%; border-collapse: collapse; font-size: 13px; }
      table.votes th, table.votes td { border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }
      table.votes th { background: #f5f5f5; text-align: left; }
      tr.vote-agree { background: #f0faf3; }
      tr.vote-dissent { background: #fdf3f0; }
      tr.vote-abstain { background: #f7f7f7; color: #666; }
      .final-decision { background: #fff8e1; border: 1px solid #e1c46a;
                        padding: 12px 16px; border-radius: 4px; margin: 16px 0; }
      .final-decision .label { font-weight: 600; font-size: 14px; }
      .final-decision .summary { margin-top: 6px; font-size: 13px; color: #333; }
      .dissent { background: #fff5f3; border-left: 3px solid #c0392b;
                 padding: 8px 14px; margin: 12px 0; }
      .signatures { margin-top: 32px; }
      .sig-row { display: flex; justify-content: space-between; margin: 12px 0;
                 border-bottom: 1px dashed #999; padding-bottom: 14px; }
      .sources { font-size: 12px; color: #444; }
      .footer { font-size: 11px; color: #777; margin-top: 32px;
                border-top: 1px solid #ccc; padding-top: 8px; }
      .supersedes { font-size: 12px; color: #555; margin: 4px 0; }
      @media print { body { margin: 12mm; } }
    """

    sig_rows = "".join(
        f"<div class='sig-row'><span>{_esc(v.role_id)} "
        f"({_esc(v.actor_id) or '—'})</span><span>____________________</span></div>"
        for v in p.votes
        if v.vote != "abstain"
    )
    sig_rows += (
        f"<div class='sig-row'><strong>Голова консиліуму: "
        f"{_esc(p.chair_role)} ({_esc(p.chair_id) or '—'})</strong>"
        f"<span>____________________</span></div>"
    )

    body = f"""
    <h1>Протокол онкоконсиліуму</h1>
    <div class='doc-meta'>
      <code>{_esc(pid)}</code> · Пацієнт <code>{_esc(p.patient_id)}</code> ·
      План <code>{_esc(p.plan_id)}</code> · Засідання {_esc(p.meeting_id)}
      від {_esc(p.meeting_date)}
    </div>
    {supersedes_note}

    <section class='final-decision'>
      <div class='label'>Рішення консиліуму: {_esc(final_label)}</div>
      <div class='summary'>{_esc(p.final_summary) or '—'}</div>
    </section>

    {plan_block}

    <section>
      <h2>Голосування</h2>
      <table class='votes'>
        <thead>
          <tr><th>Роль</th><th>Голос</th><th>Лікар</th><th>Коментар</th></tr>
        </thead>
        <tbody>{''.join(vote_rows) or '<tr><td colspan=4>—</td></tr>'}</tbody>
      </table>
    </section>

    {dissent_block}
    {pending_block}
    {src_block}

    <section class='signatures'>
      <h2>Підписи</h2>
      {sig_rows}
    </section>

    <div class='footer'>
      Згенеровано OpenOnco · {_esc(now_iso())}<br>
      Інформаційна підтримка для лікаря; кінцева відповідальність за рішення
      залишається за лікарем / консиліумом (CHARTER §15.1 Criterion 4).
    </div>
    """

    return (
        "<!DOCTYPE html>\n<html lang='uk'><head><meta charset='UTF-8'>"
        f"<title>Протокол онкоконсиліуму — {_esc(pid)}</title>"
        f"<style>{style}</style></head><body>{body}</body></html>"
    )


# ── Top-level orchestration ───────────────────────────────────────────────


def build_mdt_protocol(
    protocol_input: MDTProtocolInput,
    *,
    plan_summary: Optional[str] = None,
    sources_summary: Optional[Iterable[str]] = None,
) -> MDTProtocolResult:
    """Generate the protocol HTML + derived events. Pure — no side effects.

    Persistence is deferred to `save_mdt_protocol_events` so the caller
    can choose whether to actually write to disk (CLI / clinic-mode) or
    just hand the artifact to the user (public-demo mode).
    """
    _validate(protocol_input)
    pid = _protocol_id(protocol_input)
    events = protocol_votes_to_events(protocol_input)
    html = render_mdt_protocol_html(
        protocol_input,
        plan_summary=plan_summary,
        sources_summary=sources_summary,
    )
    json_payload = {
        "protocol_id": pid,
        "input": {
            "patient_id": protocol_input.patient_id,
            "plan_id": protocol_input.plan_id,
            "meeting_id": protocol_input.meeting_id,
            "meeting_date": protocol_input.meeting_date,
            "chair_role": protocol_input.chair_role,
            "chair_id": protocol_input.chair_id,
            "final_decision": protocol_input.final_decision,
            "final_summary": protocol_input.final_summary,
            "supersedes_protocol_id": protocol_input.supersedes_protocol_id,
            "votes": [
                {
                    "role_id": v.role_id,
                    "vote": v.vote,
                    "actor_id": v.actor_id,
                    "comment": v.comment,
                    "target_track_id": v.target_track_id,
                }
                for v in protocol_input.votes
            ],
            "pending_questions": list(protocol_input.pending_questions),
        },
        "events": [e.to_dict() for e in events],
        "generated_at": now_iso(),
    }
    return MDTProtocolResult(
        protocol_id=pid, html=html, events=events, json_payload=json_payload,
    )


def save_mdt_protocol_events(
    patient_id: str,
    events: list[ProvenanceEvent],
    *,
    root=None,
):
    """Persist the protocol events to events.jsonl. Idempotent via
    skip_if_exists — re-running the generator on the same inputs does
    NOT create duplicate log entries.

    Lazy-import event_store so this module is importable without it
    (e.g. for HTML-only / browser-side render scenarios)."""

    from . import event_store

    actual_root = root if root is not None else event_store.DEFAULT_ROOT
    for ev in events:
        event_store.append_event(
            patient_id, ev, root=actual_root, skip_if_exists=True
        )
    return actual_root


__all__ = [
    "FinalDecision",
    "MDTProtocolInput",
    "MDTProtocolResult",
    "ProtocolVote",
    "VoteKind",
    "build_mdt_protocol",
    "protocol_votes_to_events",
    "render_mdt_protocol_html",
    "save_mdt_protocol_events",
]
