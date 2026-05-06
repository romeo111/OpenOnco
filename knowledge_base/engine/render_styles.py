"""CSS for the engine HTML render layer.

Extracted from render.py to keep the renderer focused on document
structure (and to let stylesheet edits happen without scrolling through
1900+ lines of Python). The stylesheet is large because every Plan /
DiagnosticBrief / Revision page is a single self-contained HTML file
(per render.py module docstring) — no external CSS link.
"""

STYLESHEET = """
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
    --font-display: 'Playfair Display', Georgia, serif;
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

/* Per-test "Where to order" cell — pre-treatment investigations */
.lab-avail-cell { font-size: 12px; line-height: 1.5; }
.lab-chip {
    display: inline-block; padding: 1px 6px; border-radius: 3px;
    background: var(--blue-bg); color: var(--blue-700);
    font-family: var(--font-mono); font-size: 11px;
    text-decoration: none; white-space: nowrap;
}
a.lab-chip:hover { text-decoration: underline; }

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
.q-list--featured {
    margin: 8px 0 18px;
}
.q-list--featured li {
    background: #fff;
    border: 1px solid var(--green-200);
    border-left: 4px solid var(--green-600);
    box-shadow: 0 4px 14px rgba(6, 78, 59, 0.06);
}
.q-list--featured li.blocking {
    border-color: var(--red-alert);
    border-left-color: var(--red-alert);
}
.q-list--featured .q-text {
    font-size: 15px;
    font-weight: 600;
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

/* Branch-explanation — actually-fired RFs from the engine trace, with
   the conflict-resolution winner highlighted. Distinct from PRO/CONTRA
   above (which lists possible triggers in the abstract). */
.branch-explanation { margin: 18px 0; }
.branch-explanation .branch-step {
    background: var(--green-bg, #ecfdf5); border-left: 4px solid var(--green-700, #047857);
    padding: 10px 14px; border-radius: 6px; margin-bottom: 10px;
}
.branch-explanation .branch-step-head {
    font-size: 13px; color: var(--gray-700); margin-bottom: 6px; font-weight: 600;
}
.branch-explanation .branch-step ul {
    margin: 0; padding-left: 20px; font-size: 13px; color: var(--gray-700);
}
.branch-explanation .branch-step li { padding: 3px 0; line-height: 1.5; }
.branch-explanation .rf-winner-tag {
    font-family: var(--font-mono); font-size: 9.5px; letter-spacing: 0.5px;
    background: var(--green-700, #047857); color: white;
    padding: 1px 6px; border-radius: 3px; margin-left: 4px; vertical-align: 1px;
}
.branch-explanation .src-chip {
    font-family: var(--font-mono); font-size: 9.5px;
    background: var(--gray-100); color: var(--gray-700);
    padding: 1px 6px; border-radius: 3px; margin-left: 4px;
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

/* Skill catalog block */
.skill-catalog {
    margin-top: 18px;
    border-top: 1px dashed var(--green-200);
    padding-top: 10px;
}
.skill-catalog summary {
    cursor: pointer;
    color: var(--gray-700);
    font-size: 13px;
    font-weight: 600;
}
.skill-catalog table { width: 100%; border-collapse: collapse; font-size: 12px; }
.skill-catalog th {
    text-align: left; padding: 6px 8px; background: var(--gray-100);
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.5px;
    text-transform: uppercase; color: var(--gray-700);
}
.skill-catalog td {
    padding: 6px 8px; border-bottom: 1px solid var(--gray-100);
    vertical-align: top;
}
.skill-catalog tr.activated td:first-child::before {
    content: "✓ "; color: var(--green-600); font-weight: 700;
}
.skill-catalog tr.dormant { color: var(--gray-500); }
.skill-catalog tr.dormant td:first-child::before {
    content: "○ "; color: var(--gray-500);
}
.skill-catalog .ver {
    font-family: var(--font-mono); color: var(--gray-700);
}

/* Access Matrix (ua-ingestion plan §4) */
.access-matrix { margin-top: 32px; padding: 20px; background: var(--green-50);
    border: 1px solid var(--green-200); border-radius: 6px;
}
.access-matrix details { width: 100%; }
.access-matrix summary {
    cursor: pointer; list-style: none; display: flex; flex-direction: column;
    gap: 4px; padding: 4px 0;
}
.access-matrix summary::-webkit-details-marker { display: none; }
.access-matrix summary::before {
    content: "▶ "; color: var(--green-700); font-size: 12px; margin-right: 4px;
}
.access-matrix details[open] summary::before { content: "▼ "; }
.access-matrix summary h2 {
    display: inline; font-family: var(--font-display); font-size: 22px;
    color: var(--green-900); margin: 0;
}
.access-matrix .section-sub { font-size: 12px; color: var(--gray-700); }
.access-matrix-table {
    width: 100%; border-collapse: collapse; margin-top: 14px;
    font-size: 12.5px; background: white;
}
.access-matrix-table th {
    text-align: left; padding: 8px 10px; background: var(--green-100);
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.5px;
    text-transform: uppercase; color: var(--green-700);
    border-bottom: 1px solid var(--green-200);
}
.access-matrix-table td {
    padding: 10px; border-bottom: 1px solid var(--gray-100);
    vertical-align: top;
}
.access-matrix-table tr:last-child td { border-bottom: none; }
.access-matrix-table .track-cell { width: 32%; }
.access-matrix-table .regimen-name {
    font-size: 11.5px; color: var(--gray-700); margin-top: 3px;
}
.access-matrix-table .regimen-id {
    font-family: var(--font-mono); font-size: 10px; color: var(--gray-500);
}
.access-matrix-table .cost-cell { width: 22%; font-variant-numeric: tabular-nums; }
.access-matrix-table .cost-row { line-height: 1.5; }
.access-matrix-table .cost-label {
    font-family: var(--font-mono); font-size: 10px; color: var(--gray-500);
    margin-right: 4px;
}
.access-matrix-table .cost-trial {
    color: var(--green-700); font-style: italic;
}
.access-matrix-table .cost-unknown {
    color: var(--amber-alert); font-style: italic;
}
.access-matrix-table .pathway-cell { width: 22%; font-size: 11.5px; }
.access-matrix-table .pathway-cell .alt-paths {
    font-size: 10px; color: var(--gray-500);
}
.access-matrix-table .badge--ok { background: var(--green-100); color: var(--green-700); }
.access-matrix-table .badge--no { background: var(--red-bg); color: var(--red-alert); }
.access-matrix-table .badge--unknown { background: var(--gray-100); color: var(--gray-500); }
.access-matrix-table .badge {
    display: inline-block; padding: 2px 8px; border-radius: 3px;
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.3px;
    white-space: nowrap;
}
.access-matrix-table tr.track-trial { background: var(--purple-bg); }
.access-matrix-table .notes {
    font-size: 11px; color: var(--gray-700); margin-top: 4px; font-style: italic;
}
.access-matrix-table .notes-stale {
    font-size: 11px; color: var(--amber-alert); margin-top: 4px; font-weight: 600;
}
.access-matrix-table .more-notes {
    cursor: help; color: var(--gray-500); font-size: 10px; margin-left: 4px;
    border-bottom: 1px dotted var(--gray-500);
}
.access-matrix .matrix-disclaimer {
    margin-top: 10px; font-size: 11px; color: var(--gray-500); font-style: italic;
}
.access-matrix .matrix-plan-notes {
    margin: 10px 0 4px 0; padding: 8px 12px; background: var(--amber-bg);
    border-left: 3px solid var(--amber-alert); list-style: none; font-size: 12px;
    color: var(--gray-900);
}
@media print {
    .access-matrix { background: white; border: 1px solid var(--gray-200); }
    .access-matrix details { width: 100%; }
    .access-matrix summary::before { content: ""; }
    .access-matrix details:not([open]) > *:not(summary) { display: block; }
}

/* Variant actionability — ESCAT tier badges */
.variant-actionability { margin: 22px 0; }
.variant-actionability h2 { color: var(--green-800); }
.variant-actionability .section-sub {
    font-size: 12px; color: var(--gray-500); margin-bottom: 10px;
    font-family: var(--font-mono);
}
.actionability-table {
    width: 100%; border-collapse: collapse; font-size: 12.5px;
    background: white; border: 1px solid var(--gray-200); border-radius: 6px;
    overflow: hidden;
}
.actionability-table th {
    text-align: left; padding: 8px 10px; background: var(--green-700); color: white;
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.5px;
    text-transform: uppercase; font-weight: 600;
}
.actionability-table td {
    padding: 8px 10px; border-bottom: 1px solid var(--gray-100);
    vertical-align: top; color: var(--gray-700);
}
.actionability-table tr:last-child td { border-bottom: none; }
.actionability-table tbody tr:nth-child(even) td { background: var(--gray-50); }
.actionability-table .gene { font-family: var(--font-mono); font-weight: 600; color: var(--gray-900); }
.actionability-table .variant { font-family: var(--font-mono); color: var(--gray-700); }
.actionability-table .summary { font-size: 12px; color: var(--gray-700); }
.actionability-table .combos { font-size: 12px; color: var(--gray-700); }
.actionability-table .src-list {
    font-family: var(--font-mono); font-size: 10.5px; color: var(--gray-500);
}
.actionability-table .src-list li { padding: 1px 0; list-style: none; }
.actionability-table .empty-row td {
    text-align: center; color: var(--gray-500); font-style: italic;
    padding: 14px 10px;
}

/* Tier badges — ESCAT (IA/IB green; IIA/IIB yellow; IIIA/IIIB orange;
   IV light gray; X gray). Per-source level details render via
   .evidence-sources <ul> in the same row. */
.tier-badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-family: var(--font-mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.4px; white-space: nowrap;
}
.escat-IA, .escat-IB { background: #16a34a; color: white; }
.escat-IIA, .escat-IIB { background: #facc15; color: #713f12; }
.escat-IIIA, .escat-IIIB { background: #f97316; color: white; }
.escat-IV { background: var(--gray-100); color: var(--gray-700); }
.escat-X { background: var(--gray-200); color: var(--gray-700); }

/* Per-source evidence list inside each actionability row */
.evidence-sources {
    list-style: none; padding-left: 0; margin: 0;
    font-family: var(--font-mono); font-size: 11px;
}
.evidence-sources li { padding: 1px 0; color: var(--gray-700); }

/* Biomarker audit sub-sections (covered / uncovered split) */
.biomarker-subsection { margin-bottom: 10px; }
.biomarker-subsection-header {
    font-size: 12px; font-weight: 600; padding: 5px 0 4px 0;
    font-family: var(--font-mono); letter-spacing: 0.3px;
}
.biomarker-subsection.covered .biomarker-subsection-header { color: var(--green-700); }
.biomarker-subsection.uncovered .biomarker-subsection-header { color: #b45309; }
.uncovered-table th { background: #78716c; }
.biomarker-status-negative {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    background: var(--gray-100); color: var(--gray-600);
    font-family: var(--font-mono); font-size: 11px;
}
.biomarker-status-unmatched {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    background: #fef3c7; color: #92400e;
    font-family: var(--font-mono); font-size: 11px; font-weight: 600;
}
.evidence-sources .evidence-meta { color: var(--gray-500); font-size: 10px; }
.evidence-sources a { color: var(--green-700); text-decoration: none; }
.evidence-sources a:hover { text-decoration: underline; }

/* Resistance evidence flag — ⚠ badge for direction="Does Not Support"
   or significance contains "Resistance" (CIViC anti-evidence). */
.evidence-resistance {
    display: inline-block; padding: 0 6px; margin-left: 4px;
    border-radius: 3px;
    background: #fee2e2; color: #991b1b;
    font-size: 10px; font-weight: 700; letter-spacing: 0.3px;
}

/* Fallback rendering — when leveled evidence is unavailable,
   primary_sources are promoted as citation cards without a level.
   Visually muted relative to leveled evidence. */
.evidence-sources--fallback li.evidence-fallback {
    color: var(--gray-600); font-style: italic;
}
.evidence-fallback-note {
    margin-top: 4px;
    font-size: 10px; color: var(--gray-500);
    font-family: var(--font-sans); font-style: italic;
}

/* NSZU availability badges — per-drug coverage flag rendered alongside
   each component in the track's drug list. Render-time metadata only
   (engine never reads these — CHARTER §8.3 invariant). */
.nszu-badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 0.85em; font-weight: 600; white-space: nowrap;
    margin-left: 6px; vertical-align: middle;
}
.nszu-covered { background: #d4edda; color: #155724; }
.nszu-partial { background: #fff3cd; color: #856404; }
.nszu-oop { background: #ffe5cc; color: #804000; }
.nszu-not-registered { background: #f8d7da; color: #721c24; }

/* ── Sign-off badges (CHARTER §6.1) ──────────────────────────────
   Surfaces Clinical Co-Lead approval state on each track in the
   treatment Plan render. Emitted by render._render_signoff_badge.
   Mirrored in docs/style.css for the static-site renderer. */
.track-signoff { margin: 4px 0 8px 0; }
.signoff-badge {
    display: inline-block; padding: 4px 10px; border-radius: 4px;
    font-size: 0.85em; font-weight: 600; line-height: 1.3;
    border: 1px solid transparent;
}
.signoff-pending {
    background: #fef2f2; color: #991b1b; border-color: #fecaca;
}
.signoff-partial {
    background: #fffbeb; color: #92400e; border-color: #fde68a;
}
.signoff-complete {
    background: #ecfdf5; color: #065f46; border-color: #a7f3d0;
}

.drug-list { list-style: none; padding-left: 0; margin: 4px 0; }
.drug-list .drug-row { padding: 3px 0; line-height: 1.5; }
.drug-list .drug-name { font-weight: 600; }
.drug-list .drug-id { font-family: var(--font-mono); font-size: 11px; color: var(--gray-500); }
.drug-list .drug-dose { color: var(--gray-700); font-size: 12px; margin-left: 4px; }

/* Treatment phases — multi-phase regimen rendering (PR2 of phases-refactor).
   Each phase is a discrete block with its own heading + drug list. Legacy
   auto-wrapped single-phase regimens (name="main") render the wrapper but
   suppress the heading, keeping the visual close to pre-PR2 for unmigrated
   YAMLs. Multi-phase regimens (lymphodepletion → main_infusion for axi-cel,
   etc.) render as visually separated blocks per
   docs/reviews/regimen-phases-refactor-plan-2026-04-28.md §4.4. */
.phase-block {
    border: 1px solid var(--gray-200); border-radius: 6px;
    padding: 10px 14px; margin-bottom: 8px; background: var(--gray-50);
}
.phase-block:last-child { margin-bottom: 4px; }
.phase-block[data-phase="main"]:only-of-type {
    /* Auto-wrapped legacy regimen — single block, no border noise. */
    border: none; padding: 0; background: transparent;
}
.phase-block .phase-heading {
    font-family: var(--font-mono); font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px;
    color: var(--green-700); margin: 0 0 6px 0; font-weight: 700;
}
.phase-block .drug-list { margin: 0; }

/* Bridging options block — CAR-T / TIL manufacturing-window slot. Lists
   acceptable bridging regimen IDs; rendered after all phase blocks. */
.bridging-options {
    margin-top: 10px; padding: 10px 14px; background: var(--blue-bg);
    border-left: 3px solid var(--blue-700); border-radius: 4px;
}
.bridging-options .bridging-options-label {
    font-size: 12px; color: var(--blue-700);
    font-weight: 600; margin-bottom: 4px;
}
.bridging-options-list {
    list-style: none; padding-left: 0; margin: 0;
    font-family: var(--font-mono); font-size: 11px; color: var(--gray-700);
}
.bridging-options-list li.bridging-option { padding: 2px 0; }

/* PR5 — citation-presence guard
   `.no-citation-badge` is the WARN-mode flag rendered inline at the top of
   any Regimen / Indication / BMA cell whose declared sources fail to
   resolve to a real Source entity. It uses a soft amber palette so it
   reads as a warning without overpowering surrounding clinical content.
   `.stripped-block` is the STRICT-mode placeholder that replaces the
   block body when the same condition fires.

   Source: docs/reviews/cross-repo-task_torrent-sync-plan-2026-04-28.md
   §6 verifier algorithms — item #1 "Cite-or-strip at render". */
.no-citation-badge {
  display: inline-block;
  background: #fff8e1;
  color: #6d4c00;
  border: 1px solid #ffd54f;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
  margin: 4px 0;
}
.stripped-block {
  background: #fafafa;
  border: 1px dashed #bbb;
  color: #888;
  padding: 8px;
  font-style: italic;
  text-align: center;
}
"""


# ── Patient-mode CSS ─────────────────────────────────────────────────
#
# Mirrored verbatim from the "Patient mode" section in docs/style.css so
# the embedded engine HTML (Plan / DiagnosticBrief patient bundles) ships
# the same look as the static site without an external stylesheet link.
#
# Kept in a separate constant rather than appended to STYLESHEET so the
# clinician-mode renderer can opt out and keep its bundle small. Compose
# in render.py as `STYLESHEET + PATIENT_MODE_CSS` when a patient-mode
# document is being emitted.
#
# Whenever this string is updated, mirror the same change in
# docs/style.css (search for the "Patient mode" comment block) so the
# static site and engine HTML do not drift.

PATIENT_MODE_CSS = """
/* ── Patient mode ──────────────────────────────────────────────────
   Patient-facing renderer styles. Distinct typography (larger body
   text, longer line-height) and a calmer palette than the clinician
   bundle. Mirror of the same-named section in docs/style.css. */

.patient-report {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 32px;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 18px;
  line-height: 1.7;
  color: #2c3e50;
}

.patient-report h1 { font-size: 2.2em; margin: 0 0 12px; color: #1a3a5c; }
.patient-report h2 {
  font-size: 1.6em; margin: 32px 0 16px; color: #1a3a5c;
  border-bottom: 2px solid #e8f0fa; padding-bottom: 8px;
}
.patient-report h3 { font-size: 1.2em; margin: 20px 0 8px; color: #1a3a5c; }

.patient-subhead { font-size: 1.1em; color: #5a6e80; margin-bottom: 24px; }

.patient-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 1em;
  font-weight: 600;
  margin: 4px 0;
}
.patient-good { background: #d4edda; color: #155724; }
.patient-warn { background: #fff3cd; color: #856404; }
.patient-info { background: #d1ecf1; color: #0c5460; }
.patient-emergency { background: #f8d7da; color: #721c24; }

.patient-nszu {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: 500;
  margin-top: 4px;
}
.patient-nszu-covered { background: #d4edda; color: #155724; }
.patient-nszu-partial { background: #fff3cd; color: #856404; }
.patient-nszu-oop { background: #ffe5cc; color: #804000; }
.patient-nszu-not-registered { background: #f8d7da; color: #721c24; }

.drug-explanation {
  background: #f8fafc;
  border-left: 4px solid #3b82f6;
  padding: 16px 20px;
  margin: 16px 0;
  border-radius: 4px;
}
.drug-explanation .lay-language {
  font-size: 1em;
  margin: 8px 0;
  color: #2c3e50;
}

/* Per-track wrapper inside `what-now` / `why-this-plan` / `between-visits`
   sections. Renders side-by-side on wide screens, stacks on mobile. Class
   modifier tracks the engine track_id so CSS reuse with the clinician
   bundle stays consistent. */
.tracks-grid {
  display: grid;
  gap: 18px;
  margin: 16px 0 24px;
}
@media (min-width: 720px) {
  .tracks-grid--two { grid-template-columns: 1fr 1fr; }
}
.track-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #94a3b8;
  border-radius: 6px;
  padding: 18px 20px;
}
.track-card--default { border-left-color: #16a34a; }
.track-card--alternative { border-left-color: #6366f1; }
.track-card .track-label {
  font-family: 'JetBrains Mono', Menlo, monospace;
  font-size: 0.85em;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #64748b;
  margin: 0 0 4px;
}
.track-card .track-title {
  font-size: 1.15em;
  font-weight: 700;
  color: #1a3a5c;
  margin: 0 0 8px;
}
.track-card .regimen-schedule {
  font-size: 0.95em;
  color: #475569;
  margin: 4px 0 12px;
}

/* "Why this plan for you" — rationale per track, plain UA bullets. */
.why-this-plan {
  background: #fefce8;
  border-left: 4px solid #eab308;
  padding: 18px 22px;
  border-radius: 4px;
  margin: 24px 0;
}
.why-this-plan h2 {
  border-bottom-color: #fde68a;
}
.why-this-plan .why-track {
  margin: 12px 0;
}
.why-this-plan .why-track + .why-track { margin-top: 18px; }
.why-this-plan ul { margin: 8px 0 0 20px; }
.why-this-plan li { margin: 6px 0; }
.why-this-plan .why-fallback {
  font-style: italic;
  color: #78350f;
}

/* "Between visits" section — patient watchpoints grouped by urgency.
   PATIENT_MODE_SPEC §3.4. The same `er_now` items can also surface in
   the emergency-signals banner; the renderer dedupes on trigger_ua text
   so a patient never sees the same call-to-action twice. */
.between-visits {
  background: #f0f9ff;
  border-left: 4px solid #0ea5e9;
  padding: 18px 22px;
  border-radius: 4px;
  margin: 24px 0;
}
.between-visits h2 {
  border-bottom-color: #bae6fd;
}
.between-visits .bv-track {
  margin: 12px 0 18px;
}
.between-visits .bv-track + .bv-track { margin-top: 22px; }
.between-visits .bv-urgency-group {
  margin: 10px 0 14px;
}
.between-visits .bv-urgency-group h3 {
  font-size: 1em;
  font-weight: 700;
  margin: 6px 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.between-visits .bv-log h3 { color: #0c4a6e; }
.between-visits .bv-call h3 { color: #b45309; }
.between-visits .bv-er h3 { color: #991b1b; }
.between-visits ul { margin: 4px 0 0 20px; }
.between-visits li { margin: 6px 0; }
.between-visits .bv-trigger { font-weight: 600; }
.between-visits .bv-action { color: #475569; }
.between-visits .bv-window {
  font-size: 0.85em;
  color: #64748b;
  font-family: 'JetBrains Mono', Menlo, monospace;
}
.between-visits .bv-fallback {
  font-style: italic;
  color: #475569;
}

/* Cross-link chip — anchors patient ↔ clinician bundles in their headers
   so a doctor reading the patient bundle can jump to canonical version,
   and a patient reading the clinician bundle can jump to plain UA. */
.mode-toggle {
  display: inline-block;
  margin-top: 12px;
  font-size: 0.95em;
  font-family: 'JetBrains Mono', Menlo, monospace;
  background: #f1f5f9;
  color: #1e293b;
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
  border: 1px solid #cbd5e1;
}
.mode-toggle:hover {
  background: #e0f2fe;
  color: #075985;
  border-color: #38bdf8;
}
@media print {
  .mode-toggle { display: none; }
}

.emergency-list {
  background: #fff5f5;
  border-left: 4px solid #dc2626;
  padding: 16px 20px;
  margin: 16px 0;
  list-style: none;
}
.emergency-list li {
  margin: 12px 0;
  font-weight: 500;
}

.ask-doctor {
  background: #f0f9ff;
  border-left: 4px solid #0ea5e9;
  padding: 20px;
  border-radius: 4px;
  margin: 24px 0;
}
.ask-doctor ul { margin: 12px 0 0 20px; }
.ask-doctor li { margin: 8px 0; line-height: 1.5; }

.patient-disclaimer {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 2px solid #e2e8f0;
  font-size: 0.95em;
  color: #5a6e80;
}

@media (max-width: 600px) {
  .patient-report { padding: 16px 20px; font-size: 16px; }
  .patient-report h1 { font-size: 1.8em; }
  .patient-report h2 { font-size: 1.4em; }
}

@media print {
  .patient-report { font-size: 14pt; }
  .patient-disclaimer { page-break-before: avoid; }
}
"""


# Phase 4 (CIViC pivot, 2026-04-27) keeps actionability CSS in this same
# file under `.actionability-table`, `.evidence-sources`,
# `.evidence-resistance`, and `.evidence-fallback*` rules above. The
# previous render_oncokb.ONCOKB_CSS splice was removed in Phase 1
# alongside the legacy OncoKB-shaped renderer.


__all__ = ["STYLESHEET", "PATIENT_MODE_CSS"]
