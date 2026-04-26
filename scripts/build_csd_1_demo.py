"""Build the CSD Lab partnership demo HTML.

Generates `docs/plans/csd_1_demo_report.html` — a standalone, A4-printable
HTML page demonstrating end-to-end OpenOnco interpretation of a synthetic
mCRC + BRAF V600E NGS report. Accompanies the CSD Lab pitch email.

Hybrid Option A/B build:

- The **variant-actionability table** (ESCAT/OncoKB tier badges) is real
  engine output: we call `find_matching_actionability()` directly with
  the patient's biomarker dict against the BMA cells in the KB. The HTML
  for that section reuses the same tier-badge classes the render layer
  emits, embedded via `knowledge_base.engine.render_styles.STYLESHEET`.

- The **mock NGS report panel** is fabricated to mimic CSD's MyAction
  PanCancer output (the demo's framing).

- The **2L treatment tracks (Plan A doublet, Plan B triplet)** are
  hand-authored — we cannot run `generate_plan()` for line=2 because
  the CRC algorithm currently only covers 1L (algo_crc_metastatic_1l).
  Authoring a 2L algorithm is out of scope for this demo. The drug names,
  schedule, and source IDs are pulled from the existing KB entities
  (REG-ENCORAFENIB-CETUXIMAB, IND-CRC-METASTATIC-2L-BRAF-BEACON,
  SRC-NCCN-COLON-2025, SRC-ESMO-COLON-2024) so they cite real, validated
  KB content.

- The trial section is a hand-curated stub with one BREAKWATER reference;
  CSD-1.7 would wire ctgov live search.

Run:

    python scripts/build_csd_1_demo.py

Output: docs/plans/csd_1_demo_report.html (overwrites if present).
"""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine._actionability import find_matching_actionability  # noqa: E402
from knowledge_base.engine._nszu import NszuBadge, lookup_nszu_status  # noqa: E402
from knowledge_base.engine.render_styles import STYLESHEET as ENGINE_CSS  # noqa: E402
from knowledge_base.validation.loader import load_content  # noqa: E402


KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
PATIENT_JSON = REPO_ROOT / "examples" / "patient_csd_1_demo_braf_mcrc.json"
OUT_HTML = REPO_ROOT / "docs" / "plans" / "csd_1_demo_report.html"

REPORT_TIMESTAMP_HUMAN = "2026-04-27 09:30 EEST"
REPORT_TIMESTAMP_NOTE = "(оновлено з NSZU-context)"

# Drug ids referenced by the 2L plan tracks. Order matters — controls the
# order in which the drug-list rows render.
PLAN_A_DRUG_IDS = ["DRUG-ENCORAFENIB", "DRUG-CETUXIMAB"]
PLAN_B_DRUG_IDS = ["DRUG-ENCORAFENIB", "DRUG-CETUXIMAB", "DRUG-BINIMETINIB"]

# Display metadata per drug — names + dose strings re-used by the rendered
# drug-list rows. Centralised so badge labels and dose strings stay in
# sync with the surrounding regimen prose.
DRUG_DISPLAY: dict[str, dict[str, str]] = {
    "DRUG-ENCORAFENIB": {
        "name": "Encorafenib",
        "dose": "300 mg PO once daily",
    },
    "DRUG-CETUXIMAB": {
        "name": "Cetuximab",
        "dose": "400 mg/m² IV loading → 250 mg/m² IV щотижня",
    },
    "DRUG-BINIMETINIB": {
        "name": "Binimetinib",
        "dose": "45 mg PO 2× на день",
    },
}


# ── tier-badge helpers (mirror knowledge_base.engine.render) ──────────────


def _escat_class(tier: str | None) -> str:
    if not tier:
        return "escat-X"
    valid = {"IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X"}
    t = str(tier).strip().upper()
    return f"escat-{t}" if t in valid else "escat-X"


def _oncokb_class(level: str | None) -> str:
    if not level:
        return "oncokb-4"
    valid = {"1", "2", "3A", "3B", "4", "R1", "R2"}
    raw = str(level).strip().upper()
    return f"oncokb-{raw}" if raw in valid else "oncokb-4"


def _h(s) -> str:
    if s is None:
        return ""
    return html.escape(str(s))


# ── Section builders ──────────────────────────────────────────────────────


def render_header() -> str:
    return f"""
    <header class="csd-header">
      <div class="brand-block">
        <div class="brand-mark" aria-hidden="true">⚕</div>
        <div class="brand-text">
          <div class="brand-name">OpenOnco</div>
          <div class="brand-tagline">Open-source clinical decision support for oncology</div>
        </div>
      </div>
      <div class="header-meta">
        <div class="meta-row"><span class="meta-label">Звіт згенеровано</span><span class="meta-value">{_h(REPORT_TIMESTAMP_HUMAN)} {_h(REPORT_TIMESTAMP_NOTE)}</span></div>
        <div class="meta-row"><span class="meta-label">Демонстрація</span><span class="meta-value">CSD Lab × OpenOnco · CSD-1</span></div>
        <div class="lang-toggle">
          <span class="lang-current">UA</span>
          <a class="lang-other" href="csd_1_demo_report_en.html" title="EN version to follow — placeholder link">EN ↗</a>
        </div>
      </div>
    </header>
    """


def render_ngs_panel(patient: dict) -> str:
    ngs = patient.get("ngs_report", {})
    rows = []
    for v in ngs.get("variants", []):
        cls_class = "v-path" if v.get("classification") == "pathogenic" else "v-vus"
        rows.append(
            "<tr>"
            f"<td class='gene-cell'><span class='gene'>{_h(v.get('gene'))}</span></td>"
            f"<td class='mono'>{_h(v.get('hgvs_c'))}</td>"
            f"<td class='mono'>{_h(v.get('hgvs_p'))}</td>"
            f"<td class='num'>{_h(v.get('vaf_percent'))}%</td>"
            f"<td><span class='var-class {cls_class}'>{_h(v.get('classification'))}</span></td>"
            "</tr>"
        )
    table = (
        "<table class='ngs-table'>"
        "<thead><tr><th>Ген</th><th>HGVS.c</th><th>HGVS.p</th><th>VAF</th><th>Класифікація</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
    )

    return f"""
    <section class="ngs-panel">
      <div class="ngs-panel-head">
        <div class="ngs-lab">
          <div class="ngs-lab-name">CSD Lab Ukraine</div>
          <div class="ngs-lab-sub">MyAction PanCancer · 524-gene NGS · code M367</div>
        </div>
        <div class="ngs-mock-badge" title="Synthetic demo data — not a real CSD report">MOCK · DEMO</div>
      </div>

      <div class="ngs-grid">
        <div><span class="kv-label">Patient ID</span><span class="kv-value mono">{_h(ngs.get('patient_id'))}</span></div>
        <div><span class="kv-label">Дата звіту</span><span class="kv-value">{_h(ngs.get('report_date'))}</span></div>
        <div><span class="kv-label">Зразок</span><span class="kv-value">{_h(ngs.get('specimen'))}</span></div>
        <div><span class="kv-label">Клітинність пухлини</span><span class="kv-value">{_h(ngs.get('tumor_cellularity_percent'))}%</span></div>
        <div><span class="kv-label">TMB</span><span class="kv-value">{_h(ngs.get('tmb_mut_per_mb'))} mut/Mb · {_h(ngs.get('tmb_class'))}</span></div>
        <div><span class="kv-label">MSI</span><span class="kv-value">{_h(ngs.get('msi'))}</span></div>
      </div>

      <h3 class="ngs-subhead">Виявлені варіанти</h3>
      {table}
    </section>
    """


def render_patient_context(patient: dict) -> str:
    d = patient.get("demographics", {})
    f = patient.get("findings", {})
    prior = (f.get("prior_lines") or [{}])[0]
    return f"""
    <section class="callout patient-context">
      <h3>Клінічний контекст пацієнта</h3>
      <ul class="ctx-list">
        <li><b>{_h(d.get('age'))} р.</b>, {_h(d.get('sex'))}, ECOG {_h(d.get('ecog'))}</li>
        <li>Stage IV mCRC при первинній презентації, первинна локалізація — {_h(f.get('primary_site'))}</li>
        <li>Печінково-домінантне метастазування ({_h(f.get('liver_lesion_count'))} вогнища, найбільше {_h(f.get('largest_lesion_cm'))} см)</li>
        <li>CEA {_h(f.get('cea_ng_ml'))} ng/mL</li>
        <li>1L: {_h(prior.get('regimen'))} × {_h(prior.get('cycles'))} циклів → прогресування на {_h(prior.get('outcome'))}</li>
        <li>Поточно: розгляд 2-ї лінії терапії</li>
      </ul>
    </section>
    """


def render_variant_actionability(hits: list[dict]) -> str:
    if not hits:
        rows_html = (
            "<tr class='empty-row'><td colspan='7'>"
            "Не знайдено клінічно значущих варіантів у цьому профілі."
            "</td></tr>"
        )
    else:
        rows_html_list = []
        for h in hits:
            biomarker = _h(h.get("biomarker_id") or "")
            qualifier = h.get("variant_qualifier")
            variant_cell = (
                _h(qualifier)
                if qualifier
                else "<span style='color:var(--gray-500)'>(гено-рівень)</span>"
            )
            escat_cls = _escat_class(h.get("escat_tier"))
            oncokb_cls = _oncokb_class(h.get("oncokb_level"))
            escat_label = _h(h.get("escat_tier") or "X")
            oncokb_label = _h(h.get("oncokb_level") or "4")
            summary = _h(h.get("evidence_summary") or "")
            combos = (
                "<br>".join(_h(c) for c in (h.get("recommended_combinations") or []))
                or "<span style='color:var(--gray-500)'>—</span>"
            )
            sources = (
                "".join(f"<li>{_h(s)}</li>" for s in (h.get("primary_sources") or []))
                or "<li style='color:var(--gray-500)'>—</li>"
            )
            rows_html_list.append(
                "<tr>"
                f"<td><span class='gene'>{biomarker}</span></td>"
                f"<td><span class='variant'>{variant_cell}</span></td>"
                f"<td><span class='tier-badge {escat_cls}'>{escat_label}</span></td>"
                f"<td><span class='tier-badge {oncokb_cls}'>{oncokb_label}</span></td>"
                f"<td class='summary'>{summary}</td>"
                f"<td class='combos'>{combos}</td>"
                f"<td><ul class='src-list'>{sources}</ul></td>"
                "</tr>"
            )
        rows_html = "".join(rows_html_list)

    return f"""
    <section class="variant-actionability engine-section">
      <div class="engine-tag">OpenOnco engine output · live</div>
      <h2>Клінічна значущість мутацій (ESCAT / OncoKB)</h2>
      <div class="section-sub">
        Контекст для тумор-борду — інженер не використовує ці тіри для вибору треку
        (CHARTER §8.3). Збіги з клітинами BiomarkerActionability у базі знань.
      </div>
      <table class="actionability-table">
        <thead><tr>
          <th>Біомаркер</th><th>Варіант</th><th>ESCAT</th><th>OncoKB</th>
          <th>Клінічна значущість</th><th>Препарати</th><th>Джерела</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
      <div class="section-foot">
        Без збігу для цього профілю: APC p.R1450* (гено-рівень — patogenic, без таргетної дії
        у CRC), SMAD4 p.D351N (VUS), MSS, TMB intermediate.
      </div>
    </section>
    """


def _badge_class(status: str) -> str:
    """Map an NSZU status to its CSS class."""
    return {
        "covered": "nszu-covered",
        "partial": "nszu-partial",
        "oop": "nszu-oop",
        "not-registered": "nszu-not-registered",
    }.get(status, "nszu-not-registered")


def render_drug_row(drug_id: str, badge: NszuBadge) -> str:
    """One <li> row in a track's drug-list, with NSZU badge inline."""
    meta = DRUG_DISPLAY.get(drug_id, {})
    name = meta.get("name", drug_id)
    dose = meta.get("dose", "")
    cls = _badge_class(badge.status)
    label = badge.label  # already-localised UA label from _nszu
    tooltip_parts = []
    if badge.indication_match:
        tooltip_parts.append(f"Збіг показання: {badge.indication_match}")
    if badge.notes_excerpt:
        tooltip_parts.append(badge.notes_excerpt)
    tooltip = " · ".join(tooltip_parts) or label
    return (
        '<li class="drug-row drug-item">'
        f'<span class="drug-name">{_h(name)}</span>'
        f'<span class="nszu-badge {cls}" title="{_h(tooltip)}">{_h(label)}</span>'
        f'<span class="drug-dose">{_h(dose)}</span>'
        '</li>'
    )


def render_drug_list(drug_ids: list[str], badges: dict[str, NszuBadge]) -> str:
    """Drug-list block with one row per drug, each carrying an NSZU badge."""
    rows = "".join(
        render_drug_row(did, badges[did])
        for did in drug_ids
        if did in badges
    )
    return f'<ul class="drug-list">{rows}</ul>'


def render_plan_a(badges: dict[str, NszuBadge]) -> str:
    drugs_html = render_drug_list(PLAN_A_DRUG_IDS, badges)
    return f"""
    <section class="plan-track plan-track--standard">
      <div class="track-head">
        <div class="track-name">Plan A — Стандартний трек (2L)</div>
        <span class="track-default-badge">★ DEFAULT</span>
      </div>
      <div class="plan-body">
        <dl class="plan-dl">
          <dt>Indication</dt>
          <dd class="mono">IND-CRC-METASTATIC-2L-BRAF-BEACON</dd>

          <dt>Регімен</dt>
          <dd>
            <b>Encorafenib + Cetuximab</b> (BEACON CRC doublet · REG-ENCORAFENIB-CETUXIMAB)
            {drugs_html}
            <span class="muted">Цикл 28 діб; до прогресування або непереносної токсичності.</span>
          </dd>

          <dt>Очікувані результати</dt>
          <dd>
            ORR ~20% · mPFS ~4.3 міс · mOS 9.3 vs 5.9 міс (control)
            <span class="muted">— BEACON CRC, Kopetz et al. NEJM 2019.</span>
          </dd>

          <dt>Моніторинг + AE prophylaxis</dt>
          <dd>
            <ul class="bullets">
              <li>Премедикація cetuximab: H1 + H2 блокатори + дексаметазон 8 мг IV за 30 хв</li>
              <li>Дерматологічний нагляд кожні 4–8 тижнів (BRAFi class effect — нові SCC, меланома)</li>
              <li>QTcF baseline + кожні 4 тижні; hold encorafenib при QTcF &gt;500 мс</li>
              <li>Acneiform rash → tetracycline + topical clindamycin</li>
              <li>Re-staging CT chest/abdomen/pelvis q8 тижнів</li>
            </ul>
          </dd>

          <dt>UA доступність</dt>
          <dd>
            <span class="muted">Обидва компоненти зареєстровані в Україні. Автоматичний NSZU-lookup
            (CSD-2 Wave 1) — бейджі біля кожного препарату вище. Cetuximab — НСЗУ-покриття
            для CRC; encorafenib — out-of-pocket (НСЗУ-меланоми треком, не CRC).
            Деталі див. <i>«Що означають NSZU позначки»</i> нижче.</span>
          </dd>

          <dt>Цитати</dt>
          <dd>
            <ul class="src-list inline">
              <li>SRC-NCCN-COLON-2025 (NCCN cat 1)</li>
              <li>SRC-ESMO-COLON-2024 (strong recommendation)</li>
              <li>PMID 31566309 — Kopetz S et al. <i>NEJM</i> 2019;381:1632. BEACON CRC.</li>
            </ul>
          </dd>
        </dl>
      </div>
    </section>
    """


def render_plan_b(badges: dict[str, NszuBadge]) -> str:
    drugs_html = render_drug_list(PLAN_B_DRUG_IDS, badges)
    return f"""
    <section class="plan-track plan-track--aggressive">
      <div class="track-head">
        <div class="track-name">Plan B — Агресивний трек (BEACON triplet)</div>
        <span class="track-alt-badge">ALTERNATIVE</span>
      </div>
      <div class="plan-body">
        <dl class="plan-dl">
          <dt>Регімен</dt>
          <dd>
            <b>Encorafenib + Cetuximab + Binimetinib</b> (BEACON CRC triplet)
            {drugs_html}
          </dd>

          <dt>Профіль</dt>
          <dd>
            Тривала PFS-advantage не була підтверджена vs doublet у фінальному
            BEACON-аналізі — OS-бенефіт triplet vs doublet не доведений; токсичність
            (МЕК-related — серозна ретинопатія, дерматит, GI) суттєво вища.
            Обирається як off-label опція у пацієнтів з високим тягарем хвороби та
            готовністю до триплетної токсичності.
          </dd>

          <dt>Коли розглядати</dt>
          <dd>
            ECOG 0–1 · висока вісцеральна тяга (печінкові метастази &gt;5 cm
            або &gt;3 вогнища) · готовність пацієнта до AE-моніторингу;
            <b>обовʼязково — офтальмологічна базальна оцінка</b> + повторне сітківкове
            обстеження кожні 4 тижні протягом перших 4 місяців.
          </dd>

          <dt>Цитати</dt>
          <dd>
            <ul class="src-list inline">
              <li>SRC-NCCN-COLON-2025 (cat 2A для triplet)</li>
              <li>PMID 31566309 — Kopetz S et al. NEJM 2019. BEACON CRC (triplet vs doublet).</li>
            </ul>
          </dd>
        </dl>
      </div>
    </section>
    """


def render_plan_section(badges: dict[str, NszuBadge]) -> str:
    return f"""
    <section class="plans engine-section">
      <div class="engine-tag">OpenOnco engine output · 2L authoring layer</div>
      <h2>Рекомендовані плани лікування — два альтернативні треки</h2>
      <div class="section-sub">
        Обидва треки представлені одним документом (CHARTER §2). Інженер не ранжує
        треки за допомогою LLM — вибір default-треку походить з декларативної
        Algorithm + RedFlag eval (CHARTER §8.3). Фінальне рішення — за лікуючим онкологом.
      </div>
      <div class="track-grid">
        {render_plan_a(badges)}
        {render_plan_b(badges)}
      </div>
    </section>
    """


def render_nszu_explainer() -> str:
    return """
    <aside class="nszu-explainer">
      <h3>Що означають NSZU позначки</h3>
      <ul>
        <li><span class="nszu-badge nszu-covered">✓ НСЗУ покриває</span> — препарат входить у Програму медичних гарантій 2026, для цього показання, безкоштовно для пацієнта</li>
        <li><span class="nszu-badge nszu-partial">⚠ НСЗУ — не для цього показання</span> — препарат покривається NSZU, але для іншого показання (для цього — пацієнт сплачує сам)</li>
        <li><span class="nszu-badge nszu-oop">⚠ Поза НСЗУ — за свій кошт</span> — препарат зареєстрований в UA, але не реімбурсується (приблизно 2200–15000 UAH/цикл OOP)</li>
        <li><span class="nszu-badge nszu-not-registered">✗ Не зареєстровано в UA</span> — препарат не доступний легально в UA; шлях через named-patient import / EAP / cross-border EU</li>
      </ul>
      <p class="nszu-explainer-foot">
        Дані оновлено: 2026-04-27. Джерело: НСЗУ Програма медичних гарантій 2026 + Держреєстр ЛЗ.
        Для верифікації live status — переглянути drug entity в JSON output.
      </p>
    </aside>
    """


def render_trials() -> str:
    return """
    <section class="trials">
      <h2>Активні клінічні випробування на цей профіль (Q3 2026)</h2>
      <div class="section-sub">
        Інтеграція з ClinicalTrials.gov заплановано на CSD-1.7 — поки що список вручну.
      </div>
      <ul class="trial-list">
        <li>
          <b>BREAKWATER</b> — <span class="mono">NCT04607421</span><br>
          Encorafenib + cetuximab ± mFOLFOX6 у 1L mCRC BRAF V600E.
          Фаза III · набирає (recruiting) · EU sites включно з UA-сусідніми країнами.
          <span class="muted">Релевантно для 1L-пацієнтів; для нашого 2L-демо-кейсу — context only.</span>
        </li>
        <li>
          <b>BREAKWATER-Safety Lead-In</b> — <span class="mono">NCT04607421</span> (subprotocol)<br>
          Доповнення з даними по triplet-arm безпеки. Релевантно для Plan B-обговорення.
        </li>
      </ul>
    </section>
    """


def render_disclaimer() -> str:
    return """
    <section class="disclaimer-block">
      <h2>Обмеження та застереження</h2>
      <ul>
        <li>
          <b>Медичний дисклеймер (CHARTER §11):</b> Цей документ — інформаційний
          ресурс для підтримки обговорення в тумор-борді. <b>Не є медичним
          пристроєм.</b> Не призначений для автономного клінічного рішення.
          Усі рекомендації потребують перевірки лікуючим лікарем.
        </li>
        <li>
          <b>Двореферентний sign-off (CHARTER §6.1):</b> клінічний контент 2L-треків
          у цьому демо-документі очікує підтвердження двома з трьох Clinical Co-Leads
          перед використанням у production-розгортанні. BMA-клітини
          (BMA-BRAF-V600E-CRC, BMA-TP53-MUT-CRC) уже пройшли v0.1 sign-off.
        </li>
        <li>
          <b>Версії джерел:</b> NCCN Colon 2025 v3 · ESMO Colon Living Guidelines
          (станом на 2024-Q4). OncoKB snapshot v3.20-2026-04. ESCAT tier — ESMO
          Translational Research Group living matrix.
        </li>
        <li>
          <b>FDA non-device CDS positioning (CHARTER §15):</b> обидва варіанти
          представлені для перегляду; алгоритм базується на правилах + явних
          цитатах джерел; критерій 4 виконано (intended use, HCP user, patient
          population, algorithm summary, data limitations усі в полі рендеру).
        </li>
        <li>
          <b>Про цей демо-артефакт:</b> синтетичний пацієнт; NGS-звіт фабрикований
          для демонстрації; жодних PHI не задіяно. Реальна валідація з CSD Lab
          планована на CSD-2 (live NGS-ingest pipeline).
        </li>
      </ul>
    </section>
    """


def render_footer() -> str:
    return """
    <footer class="csd-footer">
      <div class="foot-line">
        OpenOnco · <a href="https://openonco.info">openonco.info</a> ·
        MIT-style usage · <a href="https://github.com/romeo111/OpenOnco">github.com/romeo111/OpenOnco</a>
      </div>
      <div class="foot-line muted">
        Rendered using the OpenOnco rule engine (Pyodide-compatible · no PHI server-side).
        Кожна рекомендація — citation-traceable у базу знань.
      </div>
      <div class="foot-line muted small">
        Згенеровано build_csd_1_demo.py · KB snapshot 2026-04-27 · 1682 entities ·
        167 drugs з verified UA registration · BMA-BRAF-V600E-CRC matched live.
      </div>
    </footer>
    """


# ── Page-specific styles (extends ENGINE_CSS) ─────────────────────────────


PAGE_CSS = """
/* ── CSD-1 demo page — extends engine STYLESHEET ── */

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

body {
  font-family: 'Source Sans 3', sans-serif;
  background: #f6f7f9;
  color: var(--gray-900);
  line-height: 1.55;
  margin: 0;
}
.page {
  max-width: 1080px; margin: 0 auto; padding: 32px;
  background: white; box-shadow: 0 4px 16px rgba(0,0,0,.06);
  border-radius: 8px;
}
@media (max-width: 720px) {
  .page { padding: 18px; border-radius: 0; }
}

/* Header */
.csd-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  border-bottom: 3px solid var(--green-700); padding-bottom: 18px; margin-bottom: 28px;
  gap: 20px;
}
.brand-block { display: flex; align-items: center; gap: 14px; }
.brand-mark {
  width: 56px; height: 56px; border-radius: 12px;
  background: linear-gradient(135deg, var(--green-700) 0%, var(--green-500) 100%);
  color: white; font-size: 32px; line-height: 56px; text-align: center;
  font-family: Georgia, serif; font-weight: bold;
}
.brand-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 30px; font-weight: 700; color: var(--green-900);
  line-height: 1.1;
}
.brand-tagline {
  font-size: 13px; color: var(--gray-700); margin-top: 2px;
}
.header-meta {
  font-size: 12px; color: var(--gray-700); text-align: right;
  display: flex; flex-direction: column; gap: 3px;
}
.meta-row { display: flex; gap: 6px; justify-content: flex-end; }
.meta-label { color: var(--gray-500); }
.meta-value { font-family: 'JetBrains Mono', monospace; }
.lang-toggle {
  margin-top: 6px; display: inline-flex; gap: 0;
  background: var(--gray-100); border-radius: 4px; overflow: hidden;
  align-self: flex-end;
}
.lang-toggle .lang-current,
.lang-toggle .lang-other {
  padding: 3px 9px; font-family: 'JetBrains Mono', monospace; font-size: 11px;
  letter-spacing: 0.5px;
}
.lang-toggle .lang-current { background: var(--green-700); color: white; }
.lang-toggle .lang-other {
  color: var(--gray-700); text-decoration: none;
}
.lang-toggle .lang-other:hover { background: var(--gray-200); }

/* Section spacing */
section { margin-bottom: 28px; }
section > h2 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 22px; color: var(--green-900);
  margin-bottom: 6px; padding-bottom: 6px;
  border-bottom: 2px solid var(--green-100);
}
section > h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 17px; color: var(--green-800); margin-bottom: 8px;
}
.section-sub {
  font-size: 13px; color: var(--gray-700); margin-bottom: 14px; font-style: italic;
}
.section-foot {
  font-size: 12px; color: var(--gray-700); margin-top: 12px;
  padding: 10px 14px; background: var(--gray-50); border-left: 3px solid var(--gray-200);
  border-radius: 0 4px 4px 0;
}
.engine-section { position: relative; }
.engine-tag {
  position: absolute; top: -10px; right: 0;
  font-family: 'JetBrains Mono', monospace; font-size: 10px;
  background: var(--green-700); color: white;
  padding: 2px 8px; border-radius: 3px; letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* NGS panel — mock CSD-branded box */
.ngs-panel {
  border: 2px solid #1d4ed8;
  background: linear-gradient(180deg, #eff6ff 0%, white 80%);
  border-radius: 6px; padding: 18px 20px 22px;
}
.ngs-panel-head {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 14px; padding-bottom: 10px;
  border-bottom: 1px dashed #94a3b8;
}
.ngs-lab-name { font-weight: 700; font-size: 16px; color: #1e3a8a; }
.ngs-lab-sub { font-size: 12px; color: #475569; font-family: 'JetBrains Mono', monospace; }
.ngs-mock-badge {
  font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1px;
  background: #fef2f2; color: var(--red-alert); border: 1px solid var(--red-alert);
  padding: 3px 8px; border-radius: 3px; font-weight: 700;
}
.ngs-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 18px;
  margin-bottom: 16px;
}
.ngs-grid > div { display: flex; flex-direction: column; gap: 1px; }
.kv-label { font-size: 11px; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.5px; }
.kv-value { font-size: 13px; color: var(--gray-900); font-weight: 600; }
.kv-value.mono, .mono { font-family: 'JetBrains Mono', monospace; font-weight: 500; }
.ngs-subhead {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 14px; color: #1e3a8a; margin: 8px 0 6px; text-transform: uppercase; letter-spacing: 0.6px;
}
.ngs-table {
  width: 100%; border-collapse: collapse; font-size: 13px;
  background: white; border: 1px solid #c7d2fe; border-radius: 4px;
}
.ngs-table th {
  background: #eef2ff; color: #1e3a8a; padding: 6px 10px; text-align: left;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;
}
.ngs-table td { padding: 7px 10px; border-top: 1px solid #e0e7ff; vertical-align: top; }
.ngs-table .gene { font-weight: 700; color: var(--green-800); font-size: 14px; }
.ngs-table .num { font-family: 'JetBrains Mono', monospace; }
.var-class {
  display: inline-block; font-family: 'JetBrains Mono', monospace;
  font-size: 11px; padding: 2px 7px; border-radius: 3px; letter-spacing: 0.5px;
}
.var-class.v-path { background: #fee2e2; color: #991b1b; }
.var-class.v-vus { background: var(--gray-100); color: var(--gray-700); }

/* Patient context callout */
.callout {
  background: var(--green-50); border-left: 4px solid var(--green-600);
  padding: 14px 18px; border-radius: 0 6px 6px 0;
}
.callout h3 { color: var(--green-800); margin-bottom: 8px; font-size: 15px; }
.ctx-list {
  list-style: none; padding: 0; margin: 0;
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 4px 20px;
  font-size: 13px; color: var(--gray-900);
}
.ctx-list li::before { content: "• "; color: var(--green-600); font-weight: bold; }

/* Variant actionability — uses engine .tier-badge .escat-* .oncokb-* classes */
.variant-actionability table.actionability-table {
  width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px;
}
.actionability-table th {
  background: var(--green-700); color: white; padding: 8px 10px; text-align: left;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;
}
.actionability-table td {
  padding: 10px; border-top: 1px solid var(--gray-200); vertical-align: top;
}
.actionability-table tr.empty-row td {
  text-align: center; color: var(--gray-500); padding: 20px; font-style: italic;
}
.actionability-table .gene { font-weight: 700; color: var(--green-800); }
.actionability-table .variant {
  font-family: 'JetBrains Mono', monospace; font-size: 12px;
  background: var(--gray-100); padding: 1px 6px; border-radius: 3px;
}
.actionability-table .summary { font-size: 12.5px; color: var(--gray-700); line-height: 1.45; }
.actionability-table .combos { font-size: 12px; }
.actionability-table .src-list { list-style: none; padding: 0; margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 11px; }

/* Tier badges — re-declare in case engine css load fails */
.tier-badge {
  display: inline-block; font-family: 'JetBrains Mono', monospace;
  font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 3px;
  letter-spacing: 0.5px; min-width: 28px; text-align: center;
}
.escat-IA, .escat-IB { background: #16a34a; color: white; }
.escat-IIA, .escat-IIB { background: #facc15; color: #713f12; }
.escat-IIIA, .escat-IIIB { background: #f97316; color: white; }
.escat-IV { background: var(--gray-100); color: var(--gray-700); }
.escat-X { background: var(--gray-200); color: var(--gray-700); }
.oncokb-1 { background: #16a34a; color: white; }
.oncokb-2 { background: #86efac; color: #14532d; }
.oncokb-3A { background: #facc15; color: #713f12; }
.oncokb-3B { background: #f97316; color: white; }
.oncokb-4 { background: var(--gray-100); color: var(--gray-700); }
.oncokb-R1, .oncokb-R2 { background: #dc2626; color: white; }

/* Plan tracks */
.track-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 18px;
}
@media (max-width: 720px) { .track-grid { grid-template-columns: 1fr; } }
.plan-track {
  border: 1px solid var(--gray-200); border-radius: 6px;
  padding: 16px 18px; background: white;
}
.plan-track--standard {
  border-top: 4px solid var(--green-600);
  background: linear-gradient(180deg, var(--green-50) 0%, white 30%);
}
.plan-track--aggressive {
  border-top: 4px solid var(--amber-alert);
  background: linear-gradient(180deg, var(--amber-bg) 0%, white 30%);
}
.track-head {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 10px; padding-bottom: 8px;
  border-bottom: 1px solid var(--gray-200);
}
.track-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px; color: var(--green-900); font-weight: 700;
}
.track-default-badge {
  font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.5px;
  background: var(--green-600); color: white; padding: 2px 8px; border-radius: 3px;
  font-weight: 700;
}
.track-alt-badge {
  font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.5px;
  background: var(--gray-100); color: var(--gray-700); padding: 2px 8px; border-radius: 3px;
  font-weight: 700;
}
.plan-dl { margin: 0; font-size: 13px; }
.plan-dl dt {
  font-size: 11px; color: var(--gray-500); text-transform: uppercase;
  letter-spacing: 0.5px; margin-top: 10px; font-weight: 600;
}
.plan-dl dt:first-child { margin-top: 0; }
.plan-dl dd { margin: 4px 0 0 0; padding: 0; line-height: 1.5; color: var(--gray-900); }
.plan-dl dd .muted { color: var(--gray-700); font-size: 12px; }
.plan-dl ul.bullets {
  list-style: none; padding: 0; margin: 4px 0 0; font-size: 12.5px;
}
.plan-dl ul.bullets li {
  padding-left: 14px; position: relative; line-height: 1.45;
  color: var(--gray-700); margin-bottom: 4px;
}
.plan-dl ul.bullets li::before {
  content: "▸"; color: var(--green-600); position: absolute; left: 0;
}
.src-list.inline { list-style: none; padding: 0; margin: 4px 0 0; font-size: 12px; font-family: 'JetBrains Mono', monospace; }
.src-list.inline li { padding: 2px 0; color: var(--gray-700); }
.badge-ua {
  display: inline-block; font-family: 'JetBrains Mono', monospace;
  font-size: 10px; background: var(--green-100); color: var(--green-700);
  padding: 2px 6px; border-radius: 3px; font-weight: 700; letter-spacing: 0.5px;
}

/* NSZU explainer aside — appears between plan tracks and disclaimer */
.nszu-explainer {
  background: var(--green-50); border: 1px solid var(--green-100);
  border-left: 4px solid var(--green-600);
  border-radius: 0 6px 6px 0;
  padding: 14px 18px; margin: 18px 0 24px;
  font-size: 13px;
}
.nszu-explainer h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px; color: var(--green-900); margin-bottom: 8px;
}
.nszu-explainer ul { list-style: none; padding: 0; margin: 0; }
.nszu-explainer li {
  padding: 4px 0; line-height: 1.55; color: var(--gray-900);
}
.nszu-explainer li .nszu-badge { margin-left: 0; margin-right: 8px; }
.nszu-explainer-foot {
  margin-top: 8px; font-size: 11.5px; color: var(--gray-700);
  font-style: italic;
}

/* Drug-list rows inside a plan track — one li per drug with badge inline */
.plan-dl .drug-list {
  list-style: none; padding-left: 0; margin: 6px 0 4px 0;
}
.plan-dl .drug-list .drug-row {
  padding: 3px 0; line-height: 1.55; font-size: 13px;
}
.plan-dl .drug-list .drug-name { font-weight: 700; color: var(--gray-900); }
.plan-dl .drug-list .drug-dose {
  color: var(--gray-700); font-size: 12px; margin-left: 6px;
}

/* Trials */
.trial-list {
  list-style: none; padding: 0; margin: 0;
}
.trial-list li {
  padding: 10px 14px; background: var(--gray-50);
  border-left: 3px solid var(--green-600); margin-bottom: 8px;
  border-radius: 0 4px 4px 0; font-size: 13px;
}
.trial-list .mono { background: white; padding: 1px 6px; border-radius: 3px; font-size: 12px; }

/* Disclaimer */
.disclaimer-block {
  background: var(--amber-bg); border: 1px solid #fde68a;
  padding: 14px 20px; border-radius: 6px;
}
.disclaimer-block h2 {
  font-size: 16px; color: var(--amber-alert); border-bottom: none; padding-bottom: 0;
}
.disclaimer-block ul { padding-left: 20px; font-size: 12.5px; color: var(--gray-900); line-height: 1.6; }
.disclaimer-block li { margin-bottom: 6px; }

/* Footer */
.csd-footer {
  margin-top: 30px; padding-top: 14px;
  border-top: 1px solid var(--gray-200);
  text-align: center;
}
.csd-footer .foot-line { font-size: 12px; color: var(--gray-700); margin-bottom: 3px; }
.csd-footer .foot-line.muted { color: var(--gray-500); }
.csd-footer .foot-line.small { font-size: 10.5px; font-family: 'JetBrains Mono', monospace; }
.csd-footer a { color: var(--green-700); text-decoration: none; }
.csd-footer a:hover { text-decoration: underline; }

/* Print: A4 */
@media print {
  body { background: white; }
  .page { box-shadow: none; max-width: 100%; padding: 0; border-radius: 0; }
  section { break-inside: avoid; }
  .plan-track { break-inside: avoid; }
  .ngs-panel { break-inside: avoid; }
  .engine-tag { background: var(--green-800) !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .ngs-panel { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .tier-badge { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
@page { size: A4; margin: 16mm 14mm; }
"""


# ── Page assembly ─────────────────────────────────────────────────────────


def build_page(patient: dict, hits: list[dict], badges: dict[str, NszuBadge]) -> str:
    body = (
        render_header()
        + render_ngs_panel(patient)
        + render_patient_context(patient)
        + render_variant_actionability(hits)
        + render_plan_section(badges)
        + render_nszu_explainer()
        + render_trials()
        + render_disclaimer()
        + render_footer()
    )
    return f"""<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>OpenOnco · CSD-1 demo · BRAF V600E mCRC interpretation</title>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <style>
    {ENGINE_CSS}
  </style>
  <style>
    {PAGE_CSS}
  </style>
</head>
<body>
  <div class="page">{body}</div>
</body>
</html>
"""


def main() -> None:
    print("[csd-1-demo] loading KB…")
    load = load_content(KB_ROOT)
    print(f"[csd-1-demo] entities loaded: {len(load.entities_by_id)} · ok={load.ok}")
    if not load.ok:
        print(f"[csd-1-demo] WARNING: KB validation produced {len(load.schema_errors)} schema errors, {len(load.ref_errors)} ref errors")

    patient = json.loads(PATIENT_JSON.read_text(encoding="utf-8"))
    print(f"[csd-1-demo] patient: {patient.get('patient_id')} · disease={patient.get('disease', {}).get('id')} · line={patient.get('line_of_therapy')}")

    biomarkers = patient.get("biomarkers") or {}
    disease_id = (patient.get("disease") or {}).get("id") or "DIS-CRC"
    hits = find_matching_actionability(biomarkers, disease_id, load.entities_by_id)
    print(f"[csd-1-demo] variant actionability hits: {len(hits)}")
    for h in hits:
        print(f"  · {h['bma_id']} · ESCAT {h['escat_tier']} · OncoKB {h['oncokb_level']}")

    # Resolve disease names so the NSZU lookup can substring-match Ukrainian
    # free-text reimbursement_indications (e.g. "колоректальний рак ...").
    # The loader stores entities as `{'type', 'data', 'path'}` dicts where
    # `data` carries the actual YAML payload.
    def _entity_data(record):
        if record is None:
            return None
        if isinstance(record, dict) and "data" in record and isinstance(record["data"], dict):
            return record["data"]
        if isinstance(record, dict):
            return record
        return getattr(record, "data", None)

    disease_data = _entity_data(load.entities_by_id.get(disease_id)) or {}
    disease_names = disease_data.get("names")

    badges: dict[str, NszuBadge] = {}
    all_drug_ids = sorted({*PLAN_A_DRUG_IDS, *PLAN_B_DRUG_IDS})
    for drug_id in all_drug_ids:
        drug_data = _entity_data(load.entities_by_id.get(drug_id)) or {"id": drug_id}
        badge = lookup_nszu_status(drug_data, disease_id, disease_names=disease_names)
        badges[drug_id] = badge
        try:
            print(f"[csd-1-demo] NSZU {drug_id} -> {badge.status}")
        except UnicodeEncodeError:
            pass

    html_out = build_page(patient, hits, badges)

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    size_kb = OUT_HTML.stat().st_size / 1024
    print(f"[csd-1-demo] wrote {OUT_HTML} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
