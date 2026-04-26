"""Build the CSD-3 patient-mode demo HTML.

Generates ``docs/plans/csd_3_patient_demo.html`` — the patient-facing
companion to the CSD-1 clinician demo. Same synthetic BRAF V600E mCRC
patient (``examples/patient_csd_1_demo_braf_mcrc.json``), rendered through
``render_plan_html(plan_result, mode="patient")`` and wrapped in a small
demo-only chrome:

- Brand header with patient-friendly tagline + a toggle link to the
  clinician version (``csd_1_demo_report.html``).
- A gentle mock CSD Lab "letter" introducing the report.
- A prominent QR-code panel encoding the gzipped patient profile token
  (URL: ``openonco.info/try.html#p=<token>``). The PNG is embedded inline
  as a base64 data URI so the demo HTML stays self-contained.
- The full patient-mode plan rendering (delegated to the engine).
- A footer with attribution + medical disclaimer.

Run::

    PYTHONPATH=. py -3.12 scripts/build_csd_3_patient_demo.py

Output: ``docs/plans/csd_3_patient_demo.html`` (overwrites if present).

This is the demo a CSD molecular oncologist sees alongside the clinician
view — it makes concrete the "two outputs from the same engine" point of
OpenOnco.
"""

from __future__ import annotations

import base64
import json
import sys
from io import BytesIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine.plan import generate_plan  # noqa: E402
from knowledge_base.engine.render import render_plan_html  # noqa: E402
from scripts._token_helpers import encode as encode_patient_token  # noqa: E402


KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
PATIENT_JSON = REPO_ROOT / "examples" / "patient_csd_1_demo_braf_mcrc.json"
OUT_HTML = REPO_ROOT / "docs" / "plans" / "csd_3_patient_demo.html"

REPORT_DATE_HUMAN = "2026-04-27"


# ── Sign-off helpers (CSD-5 clinical sign-off surfacing) ──────────────────
#
# The patient demo does NOT modify the engine render layer (that surfaces
# drugs only). We instead build a small post-engine "Підтвердження
# лікарів" panel that lists each track's indication with a friendly badge.
# Indication YAMLs may carry `reviewer_signoffs` (int) and/or `reviewers`
# (list); we take the larger to avoid over-claiming.


def _signoff_count(indication_data: dict | None) -> int:
    if not indication_data:
        return 0
    declared = indication_data.get("reviewer_signoffs")
    try:
        declared_int = int(declared) if declared is not None else 0
    except (TypeError, ValueError):
        declared_int = 0
    reviewers = indication_data.get("reviewers") or []
    list_count = len(reviewers) if isinstance(reviewers, list) else 0
    return max(declared_int, list_count)


def _patient_signoff_label(n: int) -> tuple[str, str]:
    """Map a sign-off count to (css-modifier, friendly UA label)."""
    if n >= 2:
        return ("complete", "✅ Підтверджено лікарями")
    if n == 1:
        return ("partial", "🟡 Один лікар підтвердив")
    return ("pending", "🔴 Лікарі ще перевіряють цю рекомендацію")


def render_patient_signoff_panel(plan_result) -> str:
    """One row per unique track indication, with a friendly sign-off label.

    Hidden when the plan has no resolvable tracks (rare — the engine
    always returns at least one track for a successfully-matched
    algorithm)."""
    plan = plan_result.plan
    if plan is None or not plan.tracks:
        return ""
    seen: set[str] = set()
    rows: list[str] = []
    track_label_map = {
        "standard": "Стандартний варіант",
        "aggressive": "Альтернативний варіант",
    }
    for t in plan.tracks:
        ind_id = t.indication_id or ""
        if not ind_id or ind_id in seen:
            continue
        seen.add(ind_id)
        n = _signoff_count(t.indication_data or {})
        modifier, label = _patient_signoff_label(n)
        track_label = track_label_map.get(t.track_id, t.track_id or "Варіант лікування")
        rows.append(
            '<li class="signoff-row">'
            f'<span class="signoff-track">{_h_text(track_label)}</span>'
            f'<span class="signoff-pill signoff-pill--{modifier}">{_h_text(label)}</span>'
            "</li>"
        )
    if not rows:
        return ""
    return (
        '<aside class="patient-signoff-panel">'
        "<h2>Хто перевірив цю рекомендацію</h2>"
        '<p class="signoff-intro">'
        "Ми позначаємо кожну рекомендацію статусом перевірки лікарями. "
        "Будь-яка терапія, яка ще не отримала зеленої позначки, потребує "
        "обов'язкового обговорення з вашим онкологом."
        "</p>"
        f'<ul class="signoff-list">{"".join(rows)}</ul>'
        "</aside>"
    )


def render_engineering_metrics() -> str:
    """Collapsible technical-audience footer — same content as CSD-1
    demo, kept consistent so CSD-5B numbers stay in one place per
    refresh."""
    return """
    <details class="engineering-metrics">
      <summary>Інженерні метрики (для технічної аудиторії)</summary>
      <ul>
        <li>Engine bundle: lazy-load split — core 1.4 MB + per-disease module ~38 KB max (CSD-5B)</li>
        <li>Initial /try.html load: ~3-5 сек (Pyodide + core bundle)</li>
        <li>Per-disease module fetch: &lt;100 ms (browser cache after first visit)</li>
        <li>KB snapshot: 1899 entities (50% growth у CSD-1..4)</li>
        <li>Sign-off coverage: див. <a href="signoff_status_2026-04-27.md">dashboard</a></li>
      </ul>
    </details>
    """


def _h_text(s) -> str:
    """Local html-escape (the engine's _h is private; avoid coupling)."""
    import html as _html
    return _html.escape("" if s is None else str(s))


# ── QR generation ─────────────────────────────────────────────────────────


def build_qr_data_uri(url: str) -> str | None:
    """Return ``data:image/png;base64,...`` for the URL, or ``None`` if
    the ``qrcode`` dependency is unavailable.

    Uses ``error_correction=M`` (~15% recovery) — same setting as
    ``scripts/build_qr.py`` — which handles incidental smudging on
    printed lab reports without ballooning the symbol size.
    """
    try:
        import qrcode  # type: ignore
    except ImportError:
        return None
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def truncate_url(url: str, head: int = 56, tail: int = 8) -> str:
    """Display-friendly URL with the long token middle elided."""
    if len(url) <= head + tail + 1:
        return url
    return f"{url[:head]}…{url[-tail:]}"


# ── Inner-body extraction ─────────────────────────────────────────────────


def extract_patient_inner(full_html: str) -> str:
    """Strip the engine's ``<!DOCTYPE>``/``<html>``/``<head>``/``<body>``
    wrappers from a patient-mode render so we can embed the body inside
    the demo chrome.

    The engine's `_patient_doc_shell` wraps content in
    ``<div class="patient-report">…</div>``. We keep the inner of that
    div, because the demo wrapper supplies its own page chrome (header,
    QR panel, footer) but still wants to render with the engine's
    patient-mode CSS (which we re-include in the demo HTML).
    """
    open_marker = '<div class="patient-report">'
    close_marker = "</div>\n</body>"
    start = full_html.find(open_marker)
    if start == -1:
        return full_html
    start += len(open_marker)
    end = full_html.rfind(close_marker)
    if end == -1:
        return full_html[start:]
    return full_html[start:end]


def extract_engine_styles(full_html: str) -> str:
    """Return the contents of the first ``<style>…</style>`` block in the
    engine's HTML (which is `STYLESHEET + PATIENT_MODE_CSS`)."""
    s = full_html.find("<style>")
    e = full_html.find("</style>")
    if s == -1 or e == -1 or e < s:
        return ""
    return full_html[s + len("<style>"):e]


# ── Demo-only CSS (small wrapper chrome — non-overlapping with engine) ───


PATIENT_DEMO_CSS = """
:root {
  --green-700: #166534;
  --green-600: #16a34a;
  --green-500: #22c55e;
  --green-100: #dcfce7;
  --green-50:  #f0fdf4;
  --gray-900:  #1f2937;
  --gray-700:  #374151;
  --gray-500:  #6b7280;
  --gray-200:  #e5e7eb;
  --gray-100:  #f3f4f6;
  --gray-50:   #f9fafb;
  --blue-700:  #1d4ed8;
  --blue-50:   #eff6ff;
}

body {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  background: #f4f7f6;
  margin: 0;
  color: var(--gray-900);
}

.demo-page {
  max-width: 920px;
  margin: 0 auto;
  padding: 24px;
  background: white;
  box-shadow: 0 4px 16px rgba(0,0,0,.06);
  border-radius: 8px;
}
@media (max-width: 720px) {
  .demo-page { padding: 14px; border-radius: 0; box-shadow: none; }
}

/* Header */
.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  border-bottom: 3px solid var(--green-600);
  padding-bottom: 16px;
  margin-bottom: 22px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}
.brand-mark {
  width: 52px; height: 52px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--green-700) 0%, var(--green-500) 100%);
  color: white;
  font-size: 30px;
  line-height: 52px;
  text-align: center;
  font-family: Georgia, serif;
  font-weight: bold;
}
.brand h1 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 28px;
  font-weight: 700;
  color: #14532d;
  margin: 0;
  line-height: 1.15;
}
.tagline {
  font-size: 14px;
  color: var(--gray-700);
  margin: 2px 0 0;
}
.toggle-link {
  display: inline-block;
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
  background: var(--gray-100);
  color: var(--gray-700);
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
  border: 1px solid var(--gray-200);
  white-space: nowrap;
  align-self: center;
}
.toggle-link:hover {
  background: var(--green-50);
  color: var(--green-700);
  border-color: var(--green-600);
}

/* Lab "letter" intro */
.lab-letter {
  background: var(--blue-50);
  border-left: 4px solid var(--blue-700);
  padding: 16px 20px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 22px;
  font-size: 15.5px;
  line-height: 1.6;
  color: #1e3a8a;
}
.lab-letter p { margin: 0 0 8px; }
.lab-letter p:last-child { margin-bottom: 0; }
.lab-attribution {
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  color: #475569;
  margin-top: 8px !important;
}

/* QR code panel */
.qr-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 22px 18px;
  margin: 0 auto 28px;
  max-width: 440px;
}
.qr-panel img.qr-img {
  width: 200px;
  height: 200px;
  background: white;
  padding: 8px;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
  image-rendering: pixelated;
}
.qr-caption {
  font-size: 14px;
  color: var(--gray-700);
  margin: 14px 0 6px;
  line-height: 1.5;
  max-width: 340px;
}
.qr-url {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--gray-500);
  word-break: break-all;
  margin-top: 4px;
  padding: 4px 10px;
  background: white;
  border-radius: 4px;
  border: 1px dashed var(--gray-200);
}
.qr-fallback {
  background: #fef3c7;
  border: 1px dashed #d97706;
  color: #78350f;
  padding: 16px 20px;
  border-radius: 6px;
  margin: 0 auto 28px;
  max-width: 440px;
  text-align: center;
  font-size: 13px;
}

/* The patient-plan body is rendered by render_plan_html(mode="patient")
   and styled by PATIENT_MODE_CSS. We just give it a bit of separation. */
.patient-plan {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--gray-100);
}
.patient-plan .patient-report {
  /* The engine wrapper supplies its own padding; flatten here so the
     demo-page chrome doesn't double-indent the patient body. */
  padding: 0 !important;
  max-width: 100% !important;
  margin: 0 !important;
}

/* Patient sign-off panel — friendly per-track confirmation status */
.patient-signoff-panel {
  background: var(--green-50);
  border-left: 4px solid var(--green-600);
  border-radius: 0 6px 6px 0;
  padding: 16px 20px;
  margin: 0 0 22px;
}
.patient-signoff-panel h2 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 18px;
  color: #14532d;
  margin: 0 0 6px;
}
.signoff-intro {
  font-size: 14px;
  color: var(--gray-700);
  margin: 0 0 12px;
  line-height: 1.55;
}
.signoff-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.signoff-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 10px 14px;
  border-radius: 6px;
  border: 1px solid var(--gray-200);
  gap: 12px;
  flex-wrap: wrap;
}
.signoff-track {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 14px;
}
.signoff-pill {
  display: inline-block;
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 999px;
  font-weight: 600;
  white-space: nowrap;
}
.signoff-pill--complete {
  background: var(--green-100);
  color: #14532d;
  border: 1px solid var(--green-600);
}
.signoff-pill--partial {
  background: #fef3c7;
  color: #78350f;
  border: 1px solid #d97706;
}
.signoff-pill--pending {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #dc2626;
}

/* Engineering metrics — collapsible technical block above main disclaimer */
.engineering-metrics {
  margin: 22px 0 12px;
  padding: 10px 14px;
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-radius: 6px;
  font-size: 12px;
  text-align: left;
}
.engineering-metrics summary {
  cursor: pointer;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.3px;
  color: var(--gray-700);
  text-transform: uppercase;
  font-weight: 600;
  padding: 2px 0;
}
.engineering-metrics summary:hover { color: var(--green-700); }
.engineering-metrics ul {
  list-style: none; padding: 0; margin: 8px 0 0;
}
.engineering-metrics li {
  padding: 3px 0;
  line-height: 1.5;
  color: var(--gray-700);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  border-top: 1px dashed var(--gray-200);
}
.engineering-metrics li:first-child { border-top: none; }
.engineering-metrics a { color: var(--green-700); text-decoration: none; }
.engineering-metrics a:hover { text-decoration: underline; }

/* Demo footer */
.demo-footer {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid var(--gray-200);
  text-align: center;
  font-size: 12.5px;
  color: var(--gray-500);
}
.demo-footer p { margin: 4px 0; }
.demo-footer a { color: var(--green-700); text-decoration: none; }
.demo-footer a:hover { text-decoration: underline; }

/* Print: A4 */
@media print {
  body { background: white; }
  .demo-page { box-shadow: none; max-width: 100%; padding: 0; border-radius: 0; }
  .toggle-link { display: none; }
  .qr-panel { break-inside: avoid; }
  .lab-letter { break-inside: avoid; }
  .qr-panel img.qr-img { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
@page { size: A4; margin: 16mm 14mm; }
"""


# ── Page assembly ─────────────────────────────────────────────────────────


def render_qr_panel(qr_data_uri: str | None, url: str | None) -> str:
    if qr_data_uri is None or url is None:
        return (
            '<div class="qr-fallback">'
            "QR-код недоступний (бракує бібліотеки <code>qrcode</code> "
            "або <code>Pillow</code>). Цей демо-артефакт усе ще читабельний — "
            "лише QR-панель пропущена."
            "</div>"
        )
    short = truncate_url(url)
    return (
        '<div class="qr-panel">'
        f'<img class="qr-img" src="{qr_data_uri}" alt="QR-код для відкриття звіту на телефоні">'
        '<p class="qr-caption">'
        "Скануйте, щоб відкрити цей звіт на телефоні / поділитися "
        "з родиною / показати другому лікарю."
        "</p>"
        f'<div class="qr-url" title="{url}">{short}</div>'
        "</div>"
    )


def build_page(patient_inner_html: str, engine_styles: str,
               qr_data_uri: str | None, url: str | None,
               signoff_panel_html: str = "",
               engineering_metrics_html: str = "") -> str:
    qr_panel = render_qr_panel(qr_data_uri, url)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenOnco · Ваш персональний план (пацієнтська версія)</title>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
  <style>
    /* Engine STYLESHEET + PATIENT_MODE_CSS, embedded so the patient body
       renders identically to the standalone engine output. */
    {engine_styles}
  </style>
  <style>
    /* Demo-only chrome: header, lab letter, QR panel, footer. */
    {PATIENT_DEMO_CSS}
  </style>
</head>
<body>
  <div class="demo-page">
    <header class="demo-header">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">⚕</div>
        <div>
          <h1>OpenOnco</h1>
          <p class="tagline">Ваш персональний онкологічний план — пояснений мовою, зрозумілою всім</p>
        </div>
      </div>
      <a href="csd_1_demo_report.html" class="toggle-link" title="Технічна версія для лікаря">Технічна версія для лікаря →</a>
    </header>

    <aside class="lab-letter">
      <p>Шановний пацієнте,</p>
      <p>Ваш генетичний аналіз готовий. Цей звіт пояснює прості висновки на основі результатів. Не замінює консультацію з лікарем — це додатковий інструмент розуміння.</p>
      <p class="lab-attribution">Лабораторія CSD · MyAction PanCancer 524-gene NGS · код M367 · {REPORT_DATE_HUMAN} · демо-приклад 2-ї лінії (BRAF V600E)</p>
    </aside>

    {qr_panel}

    {signoff_panel_html}

    <article class="patient-plan">
      <div class="patient-report">{patient_inner_html}</div>
    </article>

    {engineering_metrics_html}

    <footer class="demo-footer">
      <p>OpenOnco · <a href="https://openonco.info">openonco.info</a> · MIT-style usage · <a href="https://github.com/romeo111/OpenOnco">github.com/romeo111/OpenOnco</a></p>
      <p>Цей звіт згенеровано Pyodide rule-engine — без надсилання даних на сервер. Ваші відомості зберігаються лише у вашому браузері.</p>
      <p>Цей документ — інформаційний ресурс, не медичний пристрій. Усі рекомендації потребують перевірки лікуючим онкологом (CHARTER §11).</p>
    </footer>
  </div>
</body>
</html>
"""


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> None:
    print("[csd-3-demo] loading patient profile…")
    patient = json.loads(PATIENT_JSON.read_text(encoding="utf-8"))
    print(f"[csd-3-demo] patient: {patient.get('patient_id')} · "
          f"disease={patient.get('disease', {}).get('id')} · "
          f"line={patient.get('line_of_therapy')}")

    # ALGO-CRC-METASTATIC-2L is now authored in the KB, so the engine
    # resolves the 2L pathway natively for this patient (line=2, BRAF
    # V600E). The previous 1L override hack has been removed — the
    # algorithm's step-2 BRAF V600E branch routes to
    # IND-CRC-METASTATIC-2L-BRAF-BEACON (encorafenib + cetuximab).

    print("[csd-3-demo] generating plan via engine…")
    plan_result = generate_plan(patient, KB_ROOT)
    if plan_result.plan is None:
        print("[csd-3-demo] WARNING: generate_plan returned no plan; "
              f"warnings: {plan_result.warnings[:3]}")
    else:
        print(f"[csd-3-demo] plan: {plan_result.plan.id} · "
              f"tracks={len(plan_result.plan.tracks)} · "
              f"algorithm={plan_result.algorithm_id}")

    print("[csd-3-demo] rendering patient-mode HTML…")
    full_patient_html = render_plan_html(plan_result, mode="patient")
    inner = extract_patient_inner(full_patient_html)
    engine_styles = extract_engine_styles(full_patient_html)
    print(f"[csd-3-demo] inner body: {len(inner)} bytes · "
          f"engine styles: {len(engine_styles)} bytes")

    print("[csd-3-demo] generating QR data URI…")
    token = encode_patient_token(patient)
    url = f"https://openonco.info/try.html#p={token}"
    print(f"[csd-3-demo] token len={len(token)} · url len={len(url)}")
    qr_data_uri = build_qr_data_uri(url)
    if qr_data_uri:
        print(f"[csd-3-demo] QR PNG embedded ({len(qr_data_uri)} bytes data URI)")
    else:
        print("[csd-3-demo] WARNING: qrcode unavailable — falling back to placeholder panel")

    signoff_panel_html = render_patient_signoff_panel(plan_result)
    engineering_metrics_html = render_engineering_metrics()
    if plan_result.plan and plan_result.plan.tracks:
        for t in plan_result.plan.tracks:
            n = _signoff_count(t.indication_data or {})
            try:
                print(f"[csd-3-demo] sign-off {t.track_id} {t.indication_id}: {n}")
            except UnicodeEncodeError:
                pass

    page = build_page(
        inner, engine_styles, qr_data_uri, url,
        signoff_panel_html=signoff_panel_html,
        engineering_metrics_html=engineering_metrics_html,
    )

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding="utf-8")
    size_kb = OUT_HTML.stat().st_size / 1024
    print(f"[csd-3-demo] wrote {OUT_HTML} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
