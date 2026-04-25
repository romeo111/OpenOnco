"""HTML render layer — Plan / DiagnosticPlan / Revision → single-file
A4-printable HTML document.

Design language adapted from the project's reference patient deliverables
(infograph/*план лікування.html — gitignored, not the source of patient
data; only the visual idiom is borrowed): green medical palette, DM Serif
Display headings, Source Sans 3 body, badges + alerts + cards.
Layout adapted for A4 print + browser preview (no scroll-snap, single
flow column). UI patterns avoid automation bias per CHARTER §15.2 C6
(both tracks shown side-by-side, alternative is not buried, every
recommendation cites sources).

Three render entry points (one per document type):

- render_plan_html(plan_result, mdt=None) — treatment Plan with tracks
- render_diagnostic_brief_html(diag_result, mdt=None) — Workup Brief
- render_revision_note_html(prev, new, transition) — Revision Note

Each returns a complete single-file HTML string (CSS embedded). Caller
decides where to write it.

Per CHARTER §15.2 C7 — diagnostic banner mandatory in DiagnosticBrief,
treatment-Plan-not-applicable disclaimer surfaced above the fold.
"""

from __future__ import annotations

import html
from datetime import datetime, timezone
from typing import Optional, Union

from .diagnostic import _DIAGNOSTIC_BANNER, DiagnosticPlanResult
from .mdt_orchestrator import MDTOrchestrationResult
from .plan import PlanResult


# ── Embedded CSS (adapted from infograph reference, A4-tuned) ─────────────


_CSS = """
:root {
    --green-900: #0a2e1a; --green-800: #0d3f24; --green-700: #14532d;
    --green-600: #166534; --green-500: #16a34a; --green-400: #22c55e;
    --green-300: #4ade80; --green-200: #86efac; --green-100: #dcfce7;
    --green-50: #f0fdf4; --teal: #0d9488; --teal-dark: #115e59;
    --red-alert: #dc2626; --red-bg: #fef2f2;
    --amber-alert: #d97706; --amber-bg: #fffbeb;
    --blue-bg: #eff6ff; --blue-700: #1d4ed8;
    --purple-bg: #faf5ff; --purple-700: #7e22ce;
    --gray-50: #f9fafb; --gray-100: #f3f4f6; --gray-200: #e5e7eb;
    --gray-500: #6b7280; --gray-700: #374151; --gray-900: #111827;
    --font-display: 'DM Serif Display', Georgia, serif;
    --font-body: 'Source Sans 3', 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', Menlo, monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-font-smoothing: antialiased; }
body {
    font-family: var(--font-body); color: var(--gray-900);
    background: var(--gray-50); line-height: 1.55;
}
.page {
    max-width: 920px; margin: 0 auto; padding: 32px 48px;
    background: white; min-height: 100vh;
    box-shadow: 0 0 24px rgba(0,0,0,.04);
}
@media print {
    body { background: white; }
    .page { box-shadow: none; padding: 16mm; max-width: 100%; }
    @page { size: A4; margin: 12mm; }
    .no-print { display: none; }
    section { page-break-inside: avoid; }
}

/* Header */
.doc-header {
    border-bottom: 2px solid var(--green-700);
    padding-bottom: 18px; margin-bottom: 24px;
}
.doc-label {
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    letter-spacing: 2px; text-transform: uppercase;
    color: var(--green-700); margin-bottom: 8px;
}
.doc-title {
    font-family: var(--font-display); font-size: 32px; line-height: 1.15;
    color: var(--green-900); margin-bottom: 6px;
}
.doc-sub {
    font-size: 14px; color: var(--gray-500);
    font-family: var(--font-mono);
}

/* Patient strip */
.patient-strip {
    background: var(--green-50); border-left: 4px solid var(--green-600);
    padding: 14px 18px; margin-bottom: 22px; border-radius: 4px;
}
.patient-strip .label {
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 1px;
    text-transform: uppercase; color: var(--green-700); margin-bottom: 4px;
}
.patient-strip .value { font-size: 15px; color: var(--gray-900); }

/* Banner — diagnostic phase */
.banner {
    border-radius: 8px; padding: 16px 20px; margin-bottom: 22px;
    border-left: 4px solid; font-size: 14px; line-height: 1.55;
}
.banner--diagnostic {
    background: var(--amber-bg); border-color: var(--amber-alert);
    color: #92400e;
}
.banner--diagnostic strong { display: block; font-size: 15px; margin-bottom: 4px; }
.banner--info {
    background: var(--green-50); border-color: var(--green-500);
    color: var(--green-800);
}
.banner--alert {
    background: var(--red-bg); border-color: var(--red-alert);
    color: #991b1b;
}

/* Sections */
section { margin-bottom: 28px; }
h2 {
    font-family: var(--font-display); font-size: 22px; line-height: 1.2;
    color: var(--green-800); margin-bottom: 12px;
}
.section-sub {
    font-size: 13px; color: var(--gray-500); margin-bottom: 14px;
    font-family: var(--font-mono);
}
h3 {
    font-size: 14px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; margin: 18px 0 10px; color: var(--gray-700);
}

/* Tracks (treatment plan) */
.tracks { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.track {
    border: 1px solid var(--gray-200); border-radius: 10px; padding: 18px;
    background: white;
}
.track--default { border-left: 4px solid var(--green-600); }
.track--alternative { border-left: 4px solid var(--gray-500); }
.track--surveillance { border-left: 4px solid var(--teal); }
.track--palliative { border-left: 4px solid var(--purple-700); }
.track-head {
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 8px;
}
.track-name { font-family: var(--font-display); font-size: 18px; }
.track-default-badge {
    background: var(--green-100); color: var(--green-700);
    font-size: 10px; padding: 2px 8px; border-radius: 4px;
    font-family: var(--font-mono); text-transform: uppercase;
}
.track dl { font-size: 13px; }
.track dt { font-weight: 700; color: var(--gray-700); margin-top: 8px; }
.track dd { color: var(--gray-700); margin-left: 0; }
.track ul { font-size: 13px; padding-left: 18px; }

/* Tables — workup steps, etc. */
.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.tbl th {
    background: var(--green-700); color: white; padding: 8px 10px;
    text-align: left; font-size: 11px; letter-spacing: 0.5px;
    text-transform: uppercase; font-weight: 600;
}
.tbl td {
    padding: 8px 10px; border-bottom: 1px solid var(--gray-100);
    vertical-align: top; color: var(--gray-700);
}
.tbl tr:last-child td { border-bottom: none; }
.tbl tbody tr:nth-child(even) td { background: var(--gray-50); }

/* Badges */
.badge {
    display: inline-block; padding: 2px 7px; border-radius: 4px;
    font-size: 10px; font-weight: 600; font-family: var(--font-mono);
    text-transform: uppercase; letter-spacing: 0.3px;
}
.badge--required { background: var(--red-bg); color: #b91c1c; }
.badge--recommended { background: var(--blue-bg); color: var(--blue-700); }
.badge--optional { background: var(--gray-100); color: var(--gray-700); }
.badge--blocking { background: var(--red-bg); color: #b91c1c; }
.badge--default { background: var(--green-100); color: var(--green-700); }
.badge--lab { background: var(--blue-bg); color: var(--blue-700); }
.badge--imaging { background: var(--purple-bg); color: var(--purple-700); }
.badge--histology { background: var(--amber-bg); color: #92400e; }
.badge--consult { background: var(--gray-100); color: var(--gray-700); }
.badge--other { background: var(--gray-100); color: var(--gray-700); }

/* Lists */
.role-list { list-style: none; padding: 0; }
.role-list li {
    padding: 10px 0; border-bottom: 1px dashed var(--gray-200);
}
.role-list li:last-child { border-bottom: none; }
.role-list .role-name { font-weight: 600; color: var(--gray-900); }
.role-list .role-reason {
    font-size: 13px; color: var(--gray-700); margin-top: 4px;
}
.role-list .role-questions {
    font-size: 12px; color: var(--gray-500); margin-top: 4px;
    font-family: var(--font-mono);
}

.q-list { list-style: none; padding: 0; }
.q-list li {
    padding: 12px 14px; margin-bottom: 8px;
    border-radius: 6px; background: var(--gray-50);
    border-left: 3px solid var(--gray-200);
}
.q-list li.blocking {
    border-left-color: var(--red-alert); background: var(--red-bg);
}
.q-list .q-id {
    font-family: var(--font-mono); font-size: 11px;
    color: var(--gray-500); margin-bottom: 4px;
}
.q-list .q-text { font-size: 14px; color: var(--gray-900); margin-bottom: 4px; }
.q-list .q-rationale { font-size: 12px; color: var(--gray-700); font-style: italic; }
.q-list .q-owner {
    font-family: var(--font-mono); font-size: 11px;
    color: var(--green-700); margin-top: 4px;
}

/* MDT block */
.mdt {
    background: var(--green-50); border-radius: 10px; padding: 18px;
    margin-top: 14px;
}

/* Steps timeline (workup) */
.steps { padding-left: 0; list-style: none; }
.steps li {
    padding: 10px 0 10px 36px; position: relative;
    border-bottom: 1px solid var(--gray-100);
}
.steps li:last-child { border-bottom: none; }
.steps .step-num {
    position: absolute; left: 0; top: 12px; width: 24px; height: 24px;
    background: var(--green-600); color: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; font-family: var(--font-mono);
}
.steps .step-name { font-weight: 600; color: var(--gray-900); }
.steps .step-rationale { font-size: 12px; color: var(--gray-500); margin-top: 4px; }

/* Sources */
.sources { font-family: var(--font-mono); font-size: 11px; color: var(--gray-500); }
.sources li { padding: 4px 0; }

/* Etiological driver — featured card for etiologically_driven archetype */
.etiology-card {
    background: linear-gradient(135deg, var(--green-50) 0%, white 100%);
    border-left: 4px solid var(--teal); border-radius: 8px;
    padding: 18px 20px; margin-bottom: 22px;
}
.etiology-card .label {
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 1px;
    text-transform: uppercase; color: var(--teal-dark); margin-bottom: 6px;
}
.etiology-card .archetype {
    font-family: var(--font-display); font-size: 18px; color: var(--green-900);
    margin-bottom: 8px;
}
.etiology-card ul { padding-left: 20px; font-size: 14px; color: var(--gray-700); }
.etiology-card ul li { padding: 3px 0; }

/* PRO/CONTRA — two-column grid for red flags */
.pro-contra { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pc-col { border: 1px solid var(--gray-200); border-radius: 8px; padding: 14px; }
.pc-col--pro { border-left: 4px solid var(--amber-alert); background: var(--amber-bg); }
.pc-col--contra { border-left: 4px solid var(--red-alert); background: var(--red-bg); }
.pc-col h3 { color: var(--gray-900); margin-top: 0; }
.pc-col ul { padding-left: 20px; font-size: 13px; color: var(--gray-700); }
.pc-col li { padding: 4px 0; }
.pc-col .rf-id {
    font-family: var(--font-mono); font-size: 10px; color: var(--gray-500);
    display: block; margin-top: 2px;
}

/* Do-not — strongly framed prohibitive list */
.do-not {
    background: var(--red-bg); border-left: 4px solid var(--red-alert);
    border-radius: 6px; padding: 14px 18px; margin-bottom: 12px;
}
.do-not .track-name {
    font-family: var(--font-display); font-size: 15px; color: var(--gray-900);
    margin-bottom: 8px;
}
.do-not ul { padding-left: 20px; font-size: 13px; color: #7f1d1d; }
.do-not li { padding: 3px 0; }

/* Timeline — horizontal phase strip */
.timeline {
    display: flex; gap: 4px; margin-top: 8px;
    overflow-x: auto; padding-bottom: 8px;
}
.tl-phase {
    flex: 1; min-width: 120px;
    background: var(--green-100); border-radius: 6px;
    padding: 10px 12px; border-top: 3px solid var(--green-600);
}
.tl-phase--baseline { border-top-color: var(--teal); background: #ccfbf1; }
.tl-phase--induction { border-top-color: var(--green-600); background: var(--green-100); }
.tl-phase--response { border-top-color: var(--amber-alert); background: var(--amber-bg); }
.tl-phase--maintenance { border-top-color: var(--blue-700); background: var(--blue-bg); }
.tl-phase--followup { border-top-color: var(--gray-500); background: var(--gray-100); }
.tl-phase .name {
    font-weight: 700; font-size: 12px; color: var(--gray-900);
    margin-bottom: 4px;
}
.tl-phase .window {
    font-family: var(--font-mono); font-size: 10px; color: var(--gray-700);
}

/* Footer */
.doc-footer {
    margin-top: 40px; padding-top: 20px;
    border-top: 1px solid var(--gray-200);
    font-size: 11px; color: var(--gray-500); line-height: 1.6;
}
.fda-disclosure {
    background: var(--gray-50); padding: 14px; border-radius: 6px;
    margin-bottom: 14px; font-size: 12px; color: var(--gray-700);
}
.fda-disclosure strong { color: var(--gray-900); }
.version-chain {
    font-family: var(--font-mono); font-size: 11px;
    background: var(--gray-100); padding: 8px 12px; border-radius: 4px;
    margin-bottom: 10px;
}
.medical-disclaimer {
    font-style: italic; color: var(--gray-700); font-size: 11px;
    border-left: 2px solid var(--gray-200); padding-left: 12px;
}
"""


# ── Helpers ───────────────────────────────────────────────────────────────


def _h(s) -> str:
    """Escape for HTML output."""
    if s is None:
        return ""
    return html.escape(str(s))


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _doc_shell(title: str, body: str) -> str:
    """Wrap rendered body in a complete HTML document with embedded CSS."""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="uk">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{_h(title)}</title>\n"
        '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display'
        '&family=Source+Sans+3:wght@300;400;500;600;700'
        '&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
        f"<style>{_CSS}</style>\n"
        "</head>\n<body>\n"
        f'<div class="page">{body}</div>\n'
        "</body>\n</html>\n"
    )


def _render_mdt_section(mdt: Optional[MDTOrchestrationResult]) -> str:
    if mdt is None:
        return ""
    parts: list[str] = []

    def _role_block(label: str, badge_cls: str, roles) -> str:
        if not roles:
            return ""
        items = []
        for r in roles:
            qs = (
                f'<div class="role-questions">Owns: {_h(", ".join(r.linked_questions))}</div>'
                if r.linked_questions else ""
            )
            items.append(
                f"<li>"
                f'<span class="role-name">{_h(r.role_name)}</span> '
                f'<span class="badge {badge_cls}">{_h(r.priority)}</span>'
                f'<div class="role-reason">{_h(r.reason)}</div>'
                f"{qs}"
                f"</li>"
            )
        return (
            f"<h3>{_h(label)} ({len(roles)})</h3>"
            f'<ul class="role-list">{"".join(items)}</ul>'
        )

    parts.append(_role_block("Required roles", "badge--required", mdt.required_roles))
    parts.append(_role_block("Recommended roles", "badge--recommended", mdt.recommended_roles))
    parts.append(_role_block("Optional roles", "badge--optional", mdt.optional_roles))

    qs = mdt.open_questions
    if qs:
        blocking = sum(1 for q in qs if q.blocking)
        items = []
        for q in qs:
            cls = " blocking" if q.blocking else ""
            tag = '<span class="badge badge--blocking">BLOCKING</span> ' if q.blocking else ""
            items.append(
                f'<li class="{cls.strip()}">'
                f'<div class="q-id">{tag}{_h(q.id)}</div>'
                f'<div class="q-text">{_h(q.question)}</div>'
                f'<div class="q-rationale">{_h(q.rationale)}</div>'
                f'<div class="q-owner">→ {_h(q.owner_role)}</div>'
                f"</li>"
            )
        parts.append(
            f"<h3>Open questions ({len(qs)}, {blocking} blocking)</h3>"
            f'<ul class="q-list">{"".join(items)}</ul>'
        )

    dq = mdt.data_quality_summary or {}
    crit = dq.get("missing_critical_fields") or []
    rec = dq.get("missing_recommended_fields") or []
    unevaluated = dq.get("unevaluated_red_flags") or []
    if crit or rec or unevaluated:
        parts.append("<h3>Data quality</h3><ul>")
        if crit:
            parts.append(f"<li>Missing critical: {_h(', '.join(crit))}</li>")
        if rec:
            parts.append(f"<li>Missing recommended: {_h(', '.join(rec))}</li>")
        if unevaluated:
            parts.append(f"<li>Unevaluated RedFlags: {_h(', '.join(unevaluated))}</li>")
        parts.append("</ul>")

    return f'<section><h2>MDT brief</h2><div class="mdt">{"".join(parts)}</div></section>'


def _render_fda_disclosure(text: str) -> str:
    return (
        f'<div class="fda-disclosure">'
        f"<strong>Per FDA non-device CDS positioning (CHARTER §15):</strong> "
        f"{_h(text)}"
        f"</div>"
    )


def _render_version_chain(plan_id, version, supersedes, superseded_by, generated_at) -> str:
    parts = [f"plan_id: {_h(plan_id)} | version: {_h(version)} | generated: {_h(generated_at)}"]
    if supersedes:
        parts.append(f"supersedes: {_h(supersedes)}")
    if superseded_by:
        parts.append(f"superseded_by: {_h(superseded_by)}")
    return f'<div class="version-chain">{" | ".join(parts)}</div>'


_MEDICAL_DISCLAIMER = (
    "Цей документ — інформаційний ресурс для підтримки обговорення в "
    "тумор-борді (per CHARTER §11). Не система, що приймає клінічні рішення. "
    "Усі рекомендації потребують перевірки лікуючим лікарем."
)


# ── Section helpers (treatment Plan) ──────────────────────────────────────


def _render_etiological_driver(disease: Optional[dict]) -> str:
    """Etiologically-driven archetype gets a featured card explaining WHY
    a particular driver (HCV, H. pylori, EBV, etc.) shapes treatment.
    Returns empty string for non-etiologically_driven diseases."""
    if not disease:
        return ""
    archetype = disease.get("archetype")
    if archetype != "etiologically_driven":
        return ""
    factors = disease.get("etiological_factors") or []
    name = (disease.get("names") or {}).get("ukrainian") or (
        disease.get("names") or {}).get("preferred") or disease.get("id", "")
    factor_items = "".join(f"<li>{_h(f)}</li>" for f in factors) or "<li>—</li>"
    return (
        '<section>'
        '<h2>Етіологічний драйвер</h2>'
        '<div class="etiology-card">'
        '<div class="label">Etiological driver · etiologically_driven archetype</div>'
        f'<div class="archetype">{_h(name)}</div>'
        f'<ul>{factor_items}</ul>'
        '</div>'
        '</section>'
    )


_PRIORITY_LABEL_UA = {
    "critical": "Критично",
    "standard": "Стандарт",
    "desired": "Бажано",
    "calculation_based": "Розрахунок",
}
_PRIORITY_BADGE_CLS = {
    "critical": "badge--required",
    "standard": "badge--recommended",
    "desired": "badge--optional",
    "calculation_based": "badge--optional",
}
_PRIORITY_RANK = {"critical": 0, "standard": 1, "desired": 2, "calculation_based": 3}


def _render_pretreatment_investigations(plan, kb_resolved: dict) -> str:
    """Pre-treatment investigations table: union of required + desired tests
    across all tracks, sorted by priority_class. Each row shows test name,
    priority badge, category, and which tracks need it.
    Per REFERENCE_CASE_SPECIFICATION §3.5."""
    tests_lookup = (kb_resolved or {}).get("tests") or {}
    if not tests_lookup:
        return ""

    # Collect: test_id → {required_by: set[track_id], desired_by: set[track_id]}
    test_use: dict[str, dict] = {}
    for t in plan.tracks:
        ind = t.indication_data or {}
        for tid in ind.get("required_tests") or []:
            test_use.setdefault(tid, {"required_by": set(), "desired_by": set()})
            test_use[tid]["required_by"].add(t.track_id)
        for tid in ind.get("desired_tests") or []:
            test_use.setdefault(tid, {"required_by": set(), "desired_by": set()})
            test_use[tid]["desired_by"].add(t.track_id)
    if not test_use:
        return ""

    rows = []
    for tid, use in sorted(
        test_use.items(),
        key=lambda kv: (
            _PRIORITY_RANK.get((tests_lookup.get(kv[0]) or {}).get("priority_class", "standard"), 1),
            kv[0],
        ),
    ):
        test = tests_lookup.get(tid) or {}
        names = test.get("names") or {}
        name = names.get("ukrainian") or names.get("preferred") or tid
        priority = test.get("priority_class") or "standard"
        category = test.get("category") or "—"
        # If required by every track → "all"; else list which tracks
        all_track_ids = {t.track_id for t in plan.tracks}
        if use["required_by"] == all_track_ids:
            scope = "усі треки"
        elif use["required_by"]:
            scope = ", ".join(sorted(use["required_by"]))
        else:
            scope = "бажано (" + ", ".join(sorted(use["desired_by"])) + ")"
        priority_badge = (
            f'<span class="badge {_PRIORITY_BADGE_CLS.get(priority, "badge--optional")}">'
            f'{_h(_PRIORITY_LABEL_UA.get(priority, priority))}</span>'
        )
        rows.append(
            f'<tr><td>{_h(tid)}</td><td>{_h(name)}</td>'
            f'<td>{priority_badge}</td>'
            f'<td>{_h(category)}</td><td>{_h(scope)}</td></tr>'
        )

    return (
        '<section>'
        '<h2>Pre-treatment investigations</h2>'
        '<div class="section-sub">Дослідження перед стартом терапії · '
        'критичні / стандарт / бажано · поєднані по треках</div>'
        '<table class="tbl">'
        '<thead><tr><th>ID</th><th>Назва</th><th>Пріоритет</th>'
        '<th>Категорія</th><th>Потрібно для</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '</section>'
    )


def _render_red_flags_pro_contra(plan, kb_resolved: dict) -> str:
    """RedFlag PRO/CONTRA categorization for the aggressive escalation:

    - PRO-AGGRESSIVE: red flags that, when present, push the engine toward
      the aggressive track. Source: indication.red_flags_triggering_alternative
      on the STANDARD track + algorithm.decision_tree any_of red_flag clauses
      that resolve to the aggressive indication.
    - CONTRA-AGGRESSIVE: hard contraindications attached to the AGGRESSIVE
      track's indication / regimen — reasons NOT to escalate.

    Per REFERENCE_CASE_SPECIFICATION §3.8.
    """
    rf_lookup = (kb_resolved or {}).get("red_flags") or {}
    if not plan.tracks:
        return ""

    # PRO: union of red_flags_triggering_alternative across non-aggressive tracks
    pro_ids: set[str] = set()
    for t in plan.tracks:
        if t.track_id == "aggressive":
            continue
        ind = t.indication_data or {}
        pro_ids.update(ind.get("red_flags_triggering_alternative") or [])
    # Also pick up red flags from algorithm decision tree pointing to aggressive
    algo = (kb_resolved or {}).get("algorithm") or {}
    aggr_ind_ids = {
        t.indication_id for t in plan.tracks if t.track_id == "aggressive"
    }
    for step in algo.get("decision_tree") or []:
        if_true = (step.get("if_true") or {}).get("result")
        if if_true in aggr_ind_ids:
            ev = step.get("evaluate") or {}
            for clause in (ev.get("any_of") or []) + (ev.get("all_of") or []):
                if isinstance(clause, dict) and clause.get("red_flag"):
                    pro_ids.add(clause["red_flag"])

    # CONTRA: hard contraindications on aggressive track
    contra_items: list[dict] = []
    for t in plan.tracks:
        if t.track_id != "aggressive":
            continue
        for c in t.contraindications_data or []:
            contra_items.append(c)

    if not pro_ids and not contra_items:
        return ""

    def _rf_li(rid: str) -> str:
        rf = rf_lookup.get(rid) or {}
        defn = rf.get("definition_ua") or rf.get("definition") or "—"
        return f'<li>{_h(defn)}<span class="rf-id">{_h(rid)}</span></li>'

    def _ci_li(c: dict) -> str:
        cid = c.get("id", "?")
        descr = c.get("description_ua") or c.get("description") or "—"
        return f'<li>{_h(descr)}<span class="rf-id">{_h(cid)}</span></li>'

    pro_html = (
        '<div class="pc-col pc-col--pro">'
        '<h3>PRO-AGGRESSIVE</h3>'
        '<div class="section-sub">Тригери що штовхають до агресивного треку</div>'
        f'<ul>{"".join(_rf_li(r) for r in sorted(pro_ids)) or "<li>—</li>"}</ul>'
        '</div>'
    )
    contra_html = (
        '<div class="pc-col pc-col--contra">'
        '<h3>CONTRA-AGGRESSIVE</h3>'
        '<div class="section-sub">Жорсткі протипоказання до ескалації</div>'
        f'<ul>{"".join(_ci_li(c) for c in contra_items) or "<li>—</li>"}</ul>'
        '</div>'
    )
    return (
        '<section>'
        '<h2>Red flags — PRO / CONTRA aggressive</h2>'
        f'<div class="pro-contra">{pro_html}{contra_html}</div>'
        '</section>'
    )


def _render_what_not_to_do(plan) -> str:
    """Explicitly prohibitive 'do_not_do' list per track.
    Per REFERENCE_CASE_SPECIFICATION §1.3 critical."""
    blocks = []
    for t in plan.tracks:
        ind = t.indication_data or {}
        items = ind.get("do_not_do") or []
        if not items:
            continue
        li = "".join(f"<li>{_h(x)}</li>" for x in items)
        blocks.append(
            '<div class="do-not">'
            f'<div class="track-name">{_h(t.label)} ({_h(t.indication_id)})</div>'
            f'<ul>{li}</ul>'
            '</div>'
        )
    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Що НЕ робити</h2>'
        '<div class="section-sub">Прямі прохібітивні правила, кожне з обґрунтуванням у regimen / supportive care / contraindication</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


def _render_monitoring_phases(plan) -> str:
    """Monitoring schedule phases as a per-track table.
    Per REFERENCE_CASE_SPECIFICATION §1.3 critical."""
    blocks = []
    seen_monitoring_ids: set[str] = set()
    for t in plan.tracks:
        mon = t.monitoring_data
        if not mon:
            continue
        mid = mon.get("id") or ""
        if mid in seen_monitoring_ids:
            continue  # dedupe — both tracks may share the same monitoring schedule
        seen_monitoring_ids.add(mid)
        phases = mon.get("phases") or []
        if not phases:
            continue
        rows = []
        for ph in phases:
            tests = ", ".join(ph.get("tests") or []) or "—"
            checks = ph.get("checkpoints") or []
            checks_html = (
                "<ul style='padding-left:16px;margin:0;'>"
                + "".join(f"<li>{_h(c)}</li>" for c in checks)
                + "</ul>"
            ) if checks else "—"
            rows.append(
                f'<tr><td><strong>{_h(ph.get("name", "?"))}</strong></td>'
                f'<td>{_h(ph.get("window", "—"))}</td>'
                f'<td style="font-family:var(--font-mono);font-size:11px;">{_h(tests)}</td>'
                f'<td>{checks_html}</td></tr>'
            )
        blocks.append(
            f'<h3>{_h(t.label)} · {_h(mid)}</h3>'
            '<table class="tbl">'
            '<thead><tr><th>Фаза</th><th>Вікно</th>'
            '<th>Тести</th><th>Контрольні точки</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            '</table>'
        )
    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Monitoring schedule</h2>'
        '<div class="section-sub">Графік моніторингу за фазами лікування</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


def _render_timeline(plan) -> str:
    """Horizontal timeline strip composed from Regimen.cycle_length_days +
    total_cycles + MonitoringSchedule.phases. CSS-only, no SVG/JS.
    Per REFERENCE_CASE_SPECIFICATION §1.3 should-have."""
    if not plan.tracks:
        return ""

    blocks = []
    seen: set[tuple] = set()
    for t in plan.tracks:
        reg = t.regimen_data or {}
        mon = t.monitoring_data or {}
        key = (reg.get("id"), mon.get("id"))
        if key in seen or key == (None, None):
            continue
        seen.add(key)

        phases_html: list[str] = []

        # Baseline phase from monitoring (always first if present)
        mon_phases = mon.get("phases") or []
        baseline = next((p for p in mon_phases if p.get("name") == "baseline"), None)
        if baseline:
            phases_html.append(
                '<div class="tl-phase tl-phase--baseline">'
                '<div class="name">Baseline</div>'
                f'<div class="window">{_h(baseline.get("window", "—"))}</div>'
                '</div>'
            )

        # Induction phase from regimen cycle metadata
        cycle_len = reg.get("cycle_length_days")
        total_cycles = reg.get("total_cycles") or "—"
        if cycle_len:
            cycles_str = str(total_cycles).strip()
            window = (
                f"{cycle_len}-day cycles × {cycles_str}"
                if cycles_str and cycles_str != "—"
                else f"{cycle_len}-day cycles"
            )
            phases_html.append(
                '<div class="tl-phase tl-phase--induction">'
                f'<div class="name">Induction · {_h(reg.get("name", "—")[:30])}</div>'
                f'<div class="window">{_h(window)}</div>'
                '</div>'
            )

        # Response assessment phase from monitoring
        ra = next((p for p in mon_phases if "response" in (p.get("name", "").lower())), None)
        if ra:
            phases_html.append(
                '<div class="tl-phase tl-phase--response">'
                '<div class="name">Response assessment</div>'
                f'<div class="window">{_h(ra.get("window", "—"))}</div>'
                '</div>'
            )

        # Maintenance phase if present
        maint = next((p for p in mon_phases if "maint" in (p.get("name", "").lower())), None)
        if maint:
            phases_html.append(
                '<div class="tl-phase tl-phase--maintenance">'
                '<div class="name">Maintenance</div>'
                f'<div class="window">{_h(maint.get("window", "—"))}</div>'
                '</div>'
            )

        # Follow-up phase if present
        fu = next(
            (p for p in mon_phases if "follow" in (p.get("name", "").lower())),
            None,
        )
        if fu:
            phases_html.append(
                '<div class="tl-phase tl-phase--followup">'
                '<div class="name">Follow-up</div>'
                f'<div class="window">{_h(fu.get("window", "—"))}</div>'
                '</div>'
            )

        if phases_html:
            blocks.append(
                f'<h3>{_h(t.label)}</h3>'
                f'<div class="timeline">{"".join(phases_html)}</div>'
            )

    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Timeline</h2>'
        '<div class="section-sub">Хронологія лікування — derived from regimen + monitoring schedule</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


# ── Treatment Plan render ─────────────────────────────────────────────────


def render_plan_html(
    plan_result: PlanResult,
    mdt: Optional[MDTOrchestrationResult] = None,
) -> str:
    plan = plan_result.plan
    if plan is None:
        return _doc_shell("OpenOnco — empty plan", "<p>Empty PlanResult; nothing to render.</p>")

    fda = plan.fda_compliance

    # Header
    body: list[str] = []
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Treatment Plan</div>'
        f'<div class="doc-title">План лікування — {_h(plan_result.disease_id)}</div>'
        f'<div class="doc-sub">{_h(plan.id)} · v{_h(plan.version)} · {_h(plan.generated_at[:10])}</div>'
        '</div>'
    )

    # Patient strip
    body.append(
        '<div class="patient-strip">'
        '<div class="label">Patient</div>'
        f'<div class="value">{_h(plan.patient_id)} · Algorithm: {_h(plan_result.algorithm_id)}</div>'
        '</div>'
    )

    # Etiological driver — only for etiologically_driven archetype
    body.append(_render_etiological_driver(
        (plan_result.kb_resolved or {}).get("disease")
    ))

    # Tracks
    track_html = []
    for t in plan.tracks:
        track_class = f"track track--{(t.track_id or 'standard')}"
        if t.is_default:
            badge = '<span class="track-default-badge">★ DEFAULT</span>'
        else:
            badge = ""
        regimen_str = (t.regimen_data or {}).get("name", "—") if t.regimen_data else "—"
        sup = (
            f'<dt>Supportive care</dt><dd>{_h(", ".join(s.get("id", "?") for s in t.supportive_care_data))}</dd>'
            if t.supportive_care_data else ""
        )
        ci = (
            f'<dt>Hard contraindications</dt><dd>{_h(", ".join(c.get("id", "?") for c in t.contraindications_data))}</dd>'
            if t.contraindications_data else ""
        )
        track_html.append(
            f'<div class="{track_class}">'
            f'<div class="track-head"><div class="track-name">{_h(t.label)}</div>{badge}</div>'
            f'<dl>'
            f'<dt>Indication</dt><dd>{_h(t.indication_id)}</dd>'
            f'<dt>Regimen</dt><dd>{_h(regimen_str)}</dd>'
            f'{sup}'
            f'{ci}'
            f'<dt>Reason</dt><dd>{_h(t.selection_reason)}</dd>'
            f'</dl>'
            f'</div>'
        )
    body.append(
        f'<section><h2>Treatment options ({len(plan.tracks)} tracks)</h2>'
        f'<div class="tracks">{"".join(track_html)}</div></section>'
    )

    # Pre-treatment investigations · RedFlag PRO/CONTRA · What NOT to do ·
    # Monitoring phases · Timeline (REFERENCE_CASE_SPECIFICATION §1.3)
    body.append(_render_pretreatment_investigations(plan, plan_result.kb_resolved))
    body.append(_render_red_flags_pro_contra(plan, plan_result.kb_resolved))
    body.append(_render_what_not_to_do(plan))
    body.append(_render_monitoring_phases(plan))
    body.append(_render_timeline(plan))

    # MDT brief inline
    body.append(_render_mdt_section(mdt))

    # Sources
    if fda.data_sources_summary:
        items = "".join(f"<li>{_h(s)}</li>" for s in fda.data_sources_summary)
        body.append(f"<section><h2>Sources cited</h2><ul class='sources'>{items}</ul></section>")

    # Footer
    body.append('<div class="doc-footer">')
    body.append(_render_version_chain(
        plan.id, plan.version, plan.supersedes, plan.superseded_by, plan.generated_at,
    ))
    body.append(_render_fda_disclosure(fda.intended_use))
    if fda.automation_bias_warning:
        body.append(_render_fda_disclosure(fda.automation_bias_warning))
    body.append(f'<div class="medical-disclaimer">{_h(_MEDICAL_DISCLAIMER)}</div>')
    body.append('</div>')

    return _doc_shell(f"План лікування — {plan_result.disease_id}", "".join(body))


# ── Diagnostic Brief render ───────────────────────────────────────────────


def render_diagnostic_brief_html(
    diag_result: DiagnosticPlanResult,
    mdt: Optional[MDTOrchestrationResult] = None,
) -> str:
    dp = diag_result.diagnostic_plan
    if dp is None:
        return _doc_shell("OpenOnco — empty diagnostic brief", "<p>Empty DiagnosticPlanResult.</p>")

    body: list[str] = []

    # Header
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Workup Brief · DIAGNOSTIC PHASE</div>'
        '<div class="doc-title">Brief підготовки до тумор-борду</div>'
        f'<div class="doc-sub">{_h(dp.id)} · v{_h(dp.version)} · {_h(dp.generated_at[:10])}</div>'
        '</div>'
    )

    # MANDATORY diagnostic banner (CHARTER §15.2 C7)
    body.append(
        '<div class="banner banner--diagnostic">'
        '<strong>⚠ DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE</strong>'
        f'{_h(_DIAGNOSTIC_BANNER)}'
        '</div>'
    )

    # Patient + suspicion strip
    susp = diag_result.suspicion or dp.suspicion_snapshot
    susp_html = ""
    if susp:
        tissues = ", ".join(susp.tissue_locations) if susp.tissue_locations else "—"
        hyps = ", ".join(susp.working_hypotheses) if susp.working_hypotheses else "—"
        susp_html = (
            '<div class="patient-strip">'
            '<div class="label">Patient</div>'
            f'<div class="value">{_h(dp.patient_id)} · suspicion lineage: {_h(susp.lineage_hint)}</div>'
            f'<div class="value" style="margin-top:6px;font-size:13px;color:var(--gray-700);">'
            f'Tissues: {_h(tissues)} · Hypotheses: {_h(hyps)}</div>'
        )
        if susp.presentation:
            susp_html += f'<div class="value" style="margin-top:6px;font-size:13px;color:var(--gray-700);">{_h(susp.presentation)}</div>'
        susp_html += "</div>"
    body.append(susp_html)

    # Matched workup
    body.append(
        f'<div class="banner banner--info">'
        f'<strong>Matched workup:</strong> {_h(diag_result.matched_workup_id)} · '
        f'<strong>Очікуваний термін:</strong> ~{_h(dp.expected_timeline_days)} днів'
        '</div>'
    )

    # Workup steps
    steps_html = []
    for s in dp.workup_steps:
        cat_badge = f'<span class="badge badge--{_h(s.category)}">{_h(s.category)}</span> '
        descr = s.description or s.test_id or "?"
        rationale = (
            f'<div class="step-rationale">{_h(s.rationale)}</div>' if s.rationale else ""
        )
        biopsy = ""
        if s.biopsy_approach:
            biopsy = (
                f'<div class="step-rationale" style="margin-top:6px;">'
                f'<strong>Biopsy preferred:</strong> {_h(s.biopsy_approach.preferred)}'
                f'</div>'
            )
        ihc = ""
        if s.ihc_panel and s.ihc_panel.baseline:
            ihc = (
                f'<div class="step-rationale" style="margin-top:4px;">'
                f'<strong>IHC baseline:</strong> {_h(", ".join(s.ihc_panel.baseline))}'
                f'</div>'
            )
        steps_html.append(
            f'<li>'
            f'<span class="step-num">{_h(s.step)}</span>'
            f'<span class="step-name">{cat_badge}{_h(descr)}</span>'
            f'{rationale}'
            f'{biopsy}'
            f'{ihc}'
            f'</li>'
        )
    body.append(
        f'<section><h2>Workup steps ({len(dp.workup_steps)})</h2>'
        f'<ul class="steps">{"".join(steps_html)}</ul></section>'
    )

    # Mandatory questions
    if dp.mandatory_questions:
        items = "".join(f"<li>{_h(q)}</li>" for q in dp.mandatory_questions)
        body.append(
            f'<section><h2>Питання що мають бути закриті ({len(dp.mandatory_questions)})</h2>'
            f'<ul style="padding-left:20px;font-size:14px;line-height:1.7;color:var(--gray-700);">{items}</ul></section>'
        )

    # MDT brief
    body.append(_render_mdt_section(mdt))

    # Footer
    body.append('<div class="doc-footer">')
    body.append(_render_version_chain(
        dp.id, dp.version, dp.supersedes, dp.superseded_by, dp.generated_at,
    ))
    body.append(_render_fda_disclosure(dp.intended_use))
    body.append(_render_fda_disclosure(dp.automation_bias_warning))
    body.append(f'<div class="medical-disclaimer">{_h(_MEDICAL_DISCLAIMER)}</div>')
    body.append('</div>')

    return _doc_shell("OpenOnco · Workup Brief", "".join(body))


# ── Revision Note render ──────────────────────────────────────────────────


def render_revision_note_html(
    previous: Union[PlanResult, DiagnosticPlanResult],
    new_result: Union[PlanResult, DiagnosticPlanResult],
    transition: str,
    mdt: Optional[MDTOrchestrationResult] = None,
) -> str:
    """Renders a revision note: shows transition + prev/new IDs, then
    renders the new result inline (so reviewer sees the latest state)."""

    prev_id = (
        previous.diagnostic_plan.id if isinstance(previous, DiagnosticPlanResult)
        and previous.diagnostic_plan
        else (previous.plan.id if isinstance(previous, PlanResult) and previous.plan else "?")
    )
    new_id = (
        new_result.diagnostic_plan.id if isinstance(new_result, DiagnosticPlanResult)
        and new_result.diagnostic_plan
        else (new_result.plan.id if isinstance(new_result, PlanResult) and new_result.plan else "?")
    )
    new_trigger = ""
    if isinstance(new_result, PlanResult) and new_result.plan:
        new_trigger = new_result.plan.revision_trigger or ""
    elif isinstance(new_result, DiagnosticPlanResult) and new_result.diagnostic_plan:
        new_trigger = new_result.diagnostic_plan.revision_trigger or ""

    body: list[str] = []
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Revision Note</div>'
        '<div class="doc-title">Перегляд плану</div>'
        f'<div class="doc-sub">Transition: {_h(transition)} · {_h(_now_iso())}</div>'
        '</div>'
    )

    body.append(
        '<div class="banner banner--info">'
        f'<strong>Previous:</strong> {_h(prev_id)} → <strong>New:</strong> {_h(new_id)}<br>'
        f'<strong>Trigger:</strong> {_h(new_trigger or "(not specified)")}'
        '</div>'
    )

    # Inline render of the NEW result (delegate)
    if isinstance(new_result, DiagnosticPlanResult):
        # Render and strip the wrapping shell to embed inline
        inner = render_diagnostic_brief_html(new_result, mdt=mdt)
    else:
        inner = render_plan_html(new_result, mdt=mdt)
    # Extract <body> contents — quick string trim
    start = inner.find('<div class="page">')
    end = inner.rfind('</div>\n</body>')
    if start >= 0 and end >= 0:
        body.append(inner[start + len('<div class="page">'):end])
    else:
        body.append(inner)  # fallback

    return _doc_shell("OpenOnco · Revision Note", "".join(body))


# ── Polymorphic dispatch ──────────────────────────────────────────────────


def render(
    result: Union[PlanResult, DiagnosticPlanResult],
    mdt: Optional[MDTOrchestrationResult] = None,
) -> str:
    """Auto-dispatch by result type."""
    if isinstance(result, DiagnosticPlanResult):
        return render_diagnostic_brief_html(result, mdt=mdt)
    return render_plan_html(result, mdt=mdt)


__all__ = [
    "render",
    "render_diagnostic_brief_html",
    "render_plan_html",
    "render_revision_note_html",
]
