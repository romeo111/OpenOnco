"""Static-site builder for the OpenOnco GitHub Pages landing.

Two goals (per user direction):

  1. Explain the project + show numerical metrics already achieved
     (KB scope, per-disease coverage, sources, etc.) — public landing.
  2. Let any visitor manually input a virtual patient profile and get
     a generated Plan back, in-browser, no backend.

The interactive engine demo (`try.html`) runs the real Python engine
in the browser via Pyodide:

    Pyodide loads → micropip installs pydantic + pyyaml → we unpack a
    zip of knowledge_base/ into the Pyodide filesystem → user submits
    patient JSON → generate_plan(...) runs → rendered HTML lands in
    an iframe.

Layout produced:

  docs/
    .nojekyll                      # disable Jekyll
    style.css                      # shared landing/gallery styles
    index.html                     # public landing (hero + stats + comparison)
    gallery.html                   # 7 pre-generated sample cases
    try.html                       # interactive Pyodide demo
    cases/<case-id>.html           # one rendered Plan / Diagnostic Brief
    openonco-engine.zip            # zipped engine + KB content for Pyodide
    examples.json                  # dropdown payload for try.html

No real patient data ever flows here — only synthetic seed cases under
examples/, guarded by CHARTER §9.3.

Usage:

    python -m scripts.build_site [--output docs/] [--clean]
"""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
    orchestrate_mdt,
    render_diagnostic_brief_html,
    render_plan_html,
)
from knowledge_base.stats import collect_stats, format_html_widget


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"

GH_REPO = "romeo111/cancer-autoresearch"
GH_NEW_ISSUE = f"https://github.com/{GH_REPO}/issues/new"

# Custom apex domain on GitHub Pages. The build writes a CNAME file every
# run so wiping docs/ via --clean never breaks the binding.
CUSTOM_DOMAIN = "openonco.info"


@dataclass
class CaseEntry:
    case_id: str
    file: str
    label_ua: str
    summary_ua: str
    badge: str
    badge_class: str


CASES: list[CaseEntry] = [
    CaseEntry(
        case_id="hcv-mzl-reference",
        file="patient_zero_reference_case.json",
        label_ua="HCV-MZL · Reference Case (Patient Zero)",
        summary_ua="Чоловік 49, ECOG 1, 5.3 см ураження кореня язика, HCV генотип 1b, indolent presentation. Acceptance test для P0.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="hcv-mzl-indolent",
        file="patient_zero_indolent.json",
        label_ua="HCV-MZL · Indolent (стандартний варіант)",
        summary_ua="HCV-MZL із non-bulky disease — engine обирає antiviral-first (DAA SOF/VEL) як default.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="hcv-mzl-bulky",
        file="patient_zero_bulky.json",
        label_ua="HCV-MZL · Bulky (агресивний варіант)",
        summary_ua="HCV-MZL із bulky disease (>7 см) — RF-BULKY-DISEASE спрацьовує, engine обирає BR + concurrent DAA.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="mm-standard-risk",
        file="patient_mm_standard_risk.json",
        label_ua="Multiple Myeloma · Standard-Risk",
        summary_ua="Newly-diagnosed MM, t(11;14) + hyperdiploid, R-ISS II — engine обирає триплет VRd як default.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="mm-high-risk",
        file="patient_mm_high_risk.json",
        label_ua="Multiple Myeloma · High-Risk",
        summary_ua="Newly-diagnosed MM, t(4;14) + gain 1q21, R2-ISS III — RF-MM-HIGH-RISK-CYTOGENETICS, engine обирає квадруплет D-VRd.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="diagnostic-lymphoma-suspect",
        file="patient_diagnostic_lymphoma_suspect.json",
        label_ua="Suspect Lymphoma · Pre-Biopsy (Diagnostic Brief)",
        summary_ua="Pre-biopsy режим — engine генерує Workup Brief, не Treatment Plan (CHARTER §15.2 C7 — без histology немає лікування).",
        badge="Diagnostic Brief",
        badge_class="bdg-diag",
    ),
    CaseEntry(
        case_id="diagnostic-lymphoma-confirmed",
        file="patient_diagnostic_lymphoma_confirmed.json",
        label_ua="Lymphoma Confirmed · Post-Biopsy (Treatment Plan)",
        summary_ua="Той самий пацієнт після підтвердження гістології — diagnostic→treatment promotion через revise_plan.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    # ── Tier 1 lymphomas (DLBCL, FL, CLL, MCL — added in marathon block) ──
    CaseEntry(
        case_id="dlbcl-low-ipi",
        file="patient_dlbcl_low_ipi.json",
        label_ua="DLBCL NOS · Low-IPI (R-CHOP standard)",
        summary_ua="Чоловік 54, ECOG 1, IPI 1, GCB cell-of-origin — engine обирає R-CHOP × 6 циклів як default. Найпоширеніша агресивна лімфома (~30% NHL).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="dlbcl-high-ipi",
        file="patient_dlbcl_high_ipi.json",
        label_ua="DLBCL NOS · High-IPI (Pola-R-CHP)",
        summary_ua="Жінка 67, IPI 4, multiple extranodal — RF-DLBCL-HIGH-IPI fired. Engine ескалує до Pola-R-CHP (POLARIX trial); Ukraine-funding caveat.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="fl-low-burden",
        file="patient_fl_low_burden.json",
        label_ua="Follicular · Low Burden (Watch-and-Wait)",
        summary_ua="FL grade 1-2, asymptomatic, no GELF criteria — engine обирає surveillance трек (3 plans usable side-by-side, default = W&W).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="fl-high-burden",
        file="patient_fl_high_burden.json",
        label_ua="Follicular · High Burden (BR)",
        summary_ua="FL з 8 cm масою + B-symptoms + LDH↑ — RF-FL-HIGH-TUMOR-BURDEN-GELF fired. Engine обирає BR (бендамустин + ритуксимаб); reuse REG-BR-STANDARD з HCV-MZL.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="fl-transformation",
        file="patient_fl_transformation.json",
        label_ua="Follicular · Transformation Suspect (R-CHOP)",
        summary_ua="FL з rapid progression + LDH doubling — RF-FL-TRANSFORMATION-SUSPECT fired. Engine обирає R-CHOP (трактує як DLBCL pathway).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="cll-low-risk",
        file="patient_cll_low_risk.json",
        label_ua="CLL/SLL · Low-Risk (BTKi continuous)",
        summary_ua="ХЛЛ зі стандартним ризиком (no TP53/del 17p/IGHV-unmut) — engine обирає acalabrutinib continuous; modern era замість FCR/BR.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="cll-high-risk",
        file="patient_cll_high_risk.json",
        label_ua="CLL/SLL · High-Risk (VenO time-limited)",
        summary_ua="ХЛЛ з TP53 mutation + IGHV-unmut + complex karyotype — RF-CLL-HIGH-RISK fired. Engine ескалує до venetoclax+obinutuzumab (CLL14).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="mcl-fit-younger",
        file="patient_mcl_fit_younger.json",
        label_ua="Mantle Cell · Fit Younger (Intensive + autoSCT)",
        summary_ua="MCL вік 58, ECOG 0, TP53-wt — engine обирає intensive R-CHOP/R-DHAP × 6 + autoSCT + R-maintenance × 3 years (Nordic protocol).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="mcl-unfit-tp53",
        file="patient_mcl_unfit_or_tp53.json",
        label_ua="Mantle Cell · Unfit / TP53-mutant (BTKi+R)",
        summary_ua="MCL вік 71, ECOG 2, TP53 mutation — RF-MCL-BLASTOID-OR-TP53 fired. Engine обирає acalabrutinib + rituximab (BTKi-based).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    # ── More Tier 1 (MZL splenic + nodal, Burkitt, HCL, WM, HGBL-DH) ────
    CaseEntry(
        case_id="smzl-hcv-positive",
        file="patient_smzl_hcv_positive.json",
        label_ua="Splenic MZL · HCV-positive (DAA antiviral)",
        summary_ua="Селезінкова MZL із HCV-позитивним статусом — engine обирає DAA antiviral (sofosbuvir/velpatasvir 12 тижнів) як 1L; reuse REG-DAA-SOF-VEL з HCV-MZL extranodal.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="smzl-hcv-negative",
        file="patient_smzl_hcv_negative.json",
        label_ua="Splenic MZL · HCV-negative (Rituximab mono)",
        summary_ua="Селезінкова MZL HCV-negative — engine обирає rituximab monotherapy (4 weekly + 2-year maintenance).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="nmzl-low-burden",
        file="patient_nmzl_low_burden.json",
        label_ua="Nodal MZL · Low Burden (W&W)",
        summary_ua="Нодальна MZL без GELF-критеріїв — engine обирає surveillance трек (повторює FL-парадигму).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="burkitt-low-risk",
        file="patient_burkitt_low_risk.json",
        label_ua="Burkitt · Low/Intermediate Risk (DA-EPOCH-R)",
        summary_ua="Burkitt без CNS+, LDH в нормі — engine обирає DA-EPOCH-R (CALGB 10002, ~90% CR including HIV+).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="burkitt-high-risk",
        file="patient_burkitt_high_risk.json",
        label_ua="Burkitt · High Risk (CODOX-M / IVAC)",
        summary_ua="Burkitt з CNS involvement + LDH >3× ULN + bulky abdomen — RF-BURKITT-HIGH-RISK fired. Engine обирає Magrath protocol з HD-MTX + IT MTX/cytarabine.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="hcl-typical",
        file="patient_hcl_typical.json",
        label_ua="Hairy Cell Leukemia (Cladribine 7-day)",
        summary_ua="Волосатоклітинний лейкоз з cytopenia + splenomegaly — engine обирає 1 курс cladribine 7 днів. ~85% durable CR.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="wm-myd88-positive",
        file="patient_wm_myd88_positive.json",
        label_ua="Waldenström · MYD88-positive (Zanubrutinib)",
        summary_ua="WM з MYD88 L265P + iwWM treatment indication — engine обирає zanubrutinib (ASPEN — superior до ibrutinib).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="hgbl-double-hit",
        file="patient_hgbl_double_hit.json",
        label_ua="HGBL · Double-Hit (DA-EPOCH-R)",
        summary_ua="High-Grade B-Cell Lymphoma з MYC + BCL2 break-apart — engine обирає DA-EPOCH-R (substantial OS improvement vs R-CHOP); reuse регіму з Burkitt.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
]


# ── Engine bundling for Pyodide ───────────────────────────────────────────


# What we ship to the browser. Engine code + schemas + validation + content.
# Excludes: code_systems/civic/ctcae (huge, not referenced at runtime),
# clients/, ingestion/ (need network), __pycache__, *.pyc.
_BUNDLE_INCLUDE_DIRS = [
    "engine",
    "schemas",
    "validation",
    "hosted/content",
]
_BUNDLE_INCLUDE_FILES = ["__init__.py"]


def bundle_engine(output_dir: Path) -> dict:
    """Zip the runtime parts of knowledge_base/ → docs/openonco-engine.zip
    so Pyodide can `pyodide.unpackArchive` it into its filesystem."""
    src = REPO_ROOT / "knowledge_base"
    out_zip = output_dir / "openonco-engine.zip"

    files_added = 0
    bytes_uncompressed = 0
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in _BUNDLE_INCLUDE_FILES:
            p = src / fname
            if p.is_file():
                zf.write(p, f"knowledge_base/{fname}")
                files_added += 1
                bytes_uncompressed += p.stat().st_size
        for sub in _BUNDLE_INCLUDE_DIRS:
            sub_root = src / sub
            if not sub_root.is_dir():
                continue
            for path in sub_root.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                    continue
                arcname = "knowledge_base/" + str(path.relative_to(src)).replace("\\", "/")
                zf.write(path, arcname)
                files_added += 1
                bytes_uncompressed += path.stat().st_size

    return {
        "zip": str(out_zip.relative_to(output_dir)),
        "files": files_added,
        "uncompressed_bytes": bytes_uncompressed,
        "compressed_bytes": out_zip.stat().st_size,
    }


def bundle_examples(output_dir: Path) -> dict:
    """Write docs/examples.json — array of {label, json} entries used as
    the 'Load example' dropdown on try.html."""
    payload = []
    for c in CASES:
        p = EXAMPLES / c.file
        if not p.exists():
            continue
        payload.append({
            "case_id": c.case_id,
            "label": c.label_ua,
            "file": c.file,
            "json": json.loads(p.read_text(encoding="utf-8")),
        })
    out = output_dir / "examples.json"
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {"path": "examples.json", "count": len(payload)}


# ── Landing page (index.html) ─────────────────────────────────────────────


def _render_top_bar(active: str = "") -> str:
    def cls(name: str) -> str:
        return ' class="active"' if active == name else ""
    return f"""<header class="top-bar">
  <div class="brand-line">
    <a href="index.html" class="brand-mini">OpenOnco</a>
  </div>
  <nav class="top-actions">
    <a href="index.html"{cls("home")}>Головна</a>
    <a href="try.html"{cls("try")}>Спробувати</a>
    <a href="gallery.html"{cls("gallery")}>Приклади</a>
    <a href="https://github.com/{GH_REPO}" target="_blank" rel="noopener">GitHub</a>
  </nav>
</header>"""


def render_landing(stats) -> str:
    diseases_full = sum(1 for d in stats.diseases if d.coverage_status in {"stub_full_chain", "reviewed"})
    diseases_partial = sum(1 for d in stats.diseases if d.coverage_status == "partial")

    # Pull headline numbers
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_regimens = by_type.get("regimens", 0)
    n_drugs = by_type.get("drugs", 0)
    n_tests = by_type.get("tests", 0)
    n_sources = by_type.get("sources", 0)
    n_workups = by_type.get("workups", 0)
    n_redflags = by_type.get("redflags", 0)
    n_skills = stats.skills_planned_roles  # 13 — full registry of virtual specialists

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco — Open-source CDS for oncology</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="home")}

<main>
  <section class="hero">
    <div class="hero-content">
      <h1>Структуроване рішення для tumor-board.<br>Без чорних скриньок.</h1>
      <p class="hero-sub">
        Лікар завантажує профіль пацієнта → отримує два альтернативні плани лікування
        (стандартний + агресивний) із повними цитуваннями. Плани оновлюються при появі
        нових даних. Усе на rule engine + curated knowledge base, без LLM-судження.
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="try.html">Спробувати з віртуальним пацієнтом →</a>
        <a class="btn btn-secondary" href="gallery.html">Дивитись приклади</a>
      </div>
      <div class="hero-meta">
        Жодних реальних пацієнтських даних на цьому деплої · CHARTER §9.3 · FDA non-device CDS positioning per CHARTER §15
      </div>
    </div>
  </section>

  <section class="numbers">
    <h2>Що вже зроблено</h2>
    <div class="num-grid num-grid--rich">

      <div class="num-card">
        <div class="num-big">{n_diseases}</div>
        <div class="num-lbl">Хвороби в KB</div>
        <div class="num-detail">{diseases_full} з повним ланцюгом disease→indication→regimen→algorithm · {diseases_partial} частково</div>
        <p class="num-text">
          Кожна хвороба має свій <strong>archetype</strong> (etiologically_driven як
          HCV-MZL, risk_stratified як MM, biomarker_driven, stage_driven), що визначає
          логіку алгоритму вибору лікування.
        </p>
      </div>

      <div class="num-card num-card--accent">
        <div class="num-big">{n_skills}</div>
        <div class="num-lbl">Лікарі-скіли (віртуальні спеціалісти)</div>
        <div class="num-detail">кожен скіл має свою версію, sources, last_reviewed</div>
        <p class="num-text">
          Гематолог, патолог, інфекціоніст-гепатолог, радіолог, молекулярний генетик,
          клінічний фармацевт, радіотерапевт, паліативна допомога та інші — кожен
          активується на конкретні тригери у профілі пацієнта і додає свої open-questions
          + supportive care recommendations до плану.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_workups}</div>
        <div class="num-lbl">Workups (триаж)</div>
        <div class="num-detail">pre-biopsy діагностичний шлях</div>
        <p class="num-text">
          Коли в пацієнта ще немає підтвердженої гістології (CHARTER §15.2 C7 забороняє
          treatment Plan без неї), engine вмикає <strong>diagnostic mode</strong>: видає
          Workup Brief зі списком тестів, biopsy approach, IHC panel, та переліком ролей
          що мають бути в triage MDT. Як тільки histology підтверджено — diagnostic plan
          promote-иться в treatment plan через <code>revise_plan(...)</code>.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_redflags}</div>
        <div class="num-lbl">Red flags</div>
        <div class="num-detail">тригери ескалації або розслідування</div>
        <p class="num-text">
          Червоні прапорці — структуровані клінічні умови, що автоматично змінюють план:
          <em>RF-BULKY-DISEASE</em> (нодальна маса &gt;7 см) перемикає HCV-MZL з antiviral-first
          на BR + DAA, <em>RF-MM-HIGH-RISK-CYTOGENETICS</em> (t(4;14), del(17p), gain 1q)
          ескалує MM з триплету VRd до квадруплету D-VRd. Кожен RedFlag прив'язаний до
          domain-role, який «виловлює» його у MDT brief.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_regimens}</div>
        <div class="num-lbl">Режими лікування</div>
        <p class="num-text">
          Кожен регімен — список drugs з дозами, шкалою циклів, dose adjustments
          (для renal impairment, FIB-4, frailty), premedications, mandatory supportive
          care та monitoring schedule.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_drugs}</div>
        <div class="num-lbl">Препарати</div>
        <p class="num-text">
          ATC/RxNorm-кодовані. Кожен з регуляторним статусом FDA/EMA/MOЗ + НСЗУ
          reimbursement (наприклад, daratumumab наразі НЕ реімбурсується НСЗУ —
          це блокер для D-VRd, явно фіксований у плані).
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_tests}</div>
        <div class="num-lbl">Тести / процедури</div>
        <p class="num-text">
          LOINC-кодовані лабораторні + imaging + histology + IHC + genomic тести.
          Кожен має <code>priority_class</code> (critical / standard / desired /
          calculation_based) — рендеряться у Plan як «pre-treatment investigations»
          таблиця.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{n_sources}</div>
        <div class="num-lbl">Джерела</div>
        <div class="num-detail">NCCN · ESMO · EHA · BSH · EASL · МОЗ · WHO</div>
        <p class="num-text">
          Кожна Indication / Regimen / RedFlag цитує конкретні джерела з
          <em>position</em> (supports / contradicts / context) та paraphrased quote.
          FDA Criterion 4 — лікар може незалежно перевірити підставу кожної рекомендації.
        </p>
      </div>

      <div class="num-card">
        <div class="num-big">{stats.specs_count}</div>
        <div class="num-lbl">Специфікації</div>
        <p class="num-text">
          CHARTER (governance + FDA позиціювання), CLINICAL_CONTENT_STANDARDS,
          KNOWLEDGE_SCHEMA, DATA_STANDARDS, SOURCE_INGESTION, REFERENCE_CASE,
          MDT_ORCHESTRATOR, DIAGNOSTIC_MDT, WORKUP_METHODOLOGY, SKILL_ARCHITECTURE.
        </p>
      </div>

    </div>
    <div class="num-foot">
      Зріз станом на <code>{stats.generated_at_utc}</code>.
      Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
      — увесь клінічний контент позначено як <strong>STUB</strong> до dual-sign-off
      Clinical Co-Lead. Це інструмент підтримки рішень, не медичний пристрій.
    </div>
  </section>

  <section class="problem">
    <h2>Проблема</h2>
    <p class="problem-text">
      Щоб призначити лікування, лікар або клінічний фармаколог витрачає 2–4 години
      ручної роботи: відкриває NCCN PDF, звіряє ESMO guideline, перечитує МОЗ протокол,
      перевіряє НСЗУ-формуляр на доступність препарату, шукає dose adjustments
      для нирок чи печінки, додає supportive care, не забуває про вакцинації та
      профілактику опортуністичних інфекцій. І так — для кожного пацієнта,
      кожного разу заново. Будь-яка пропущена контраіндикація може коштувати
      життя. OpenOnco автоматизує цю чорнову роботу: лікар отримує готовий
      проект плану з усіма джерелами, а далі лише верифікує і коригує під
      конкретного пацієнта.
    </p>
  </section>

  <section class="how">
    <h2>Як це працює</h2>
    <p class="how-lead">
      Логіка така ж, як у класичної мультидисциплінарної команди (MDT): кілька
      спеціалістів навколо пацієнта, обговорення випадку, узгоджений план,
      повернення до випадку при появі нових даних. Ми просто оформлюємо це як
      structured engine — кожен «віртуальний лікар» — це модуль із версією,
      правилами і списком джерел.
    </p>
    <figure class="how-fig">
      <img src="MDT.png" alt="Мультидисциплінарна команда — як спеціалісти спільно ухвалюють план лікування пацієнта" loading="lazy">
      <figcaption>Кожна роль (Хірург-онколог, Хіміотерапевт, Радіолог, Патолог, Молекулярний генетик, Радіотерапевт, Психолог/паліатив тощо) у нашій системі — це <strong>скіл</strong> із власною версією. Активується автоматично при умовах профілю пацієнта і додає до плану свої open-questions, contraindications, supportive care.</figcaption>
    </figure>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    Жодних реальних пацієнтських даних · CHARTER §9.3.
    Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


# ── Gallery page ──────────────────────────────────────────────────────────


def render_gallery(stats_widget_html: str) -> str:
    cards = []
    for c in CASES:
        cards.append(
            f"""<a class="case-card" href="cases/{c.case_id}.html">
  <div class="case-badge {c.badge_class}">{c.badge}</div>
  <h3>{c.label_ua}</h3>
  <p>{c.summary_ua}</p>
  <div class="case-foot">{c.file}</div>
</a>"""
        )
    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Sample cases</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="gallery")}

<main class="gallery">
  <h1>Готові приклади</h1>
  <p class="lead">
    Сім синтетичних пацієнтських профілів прогнані через рушій. Кожен клік
    відкриває повний Plan або Diagnostic Brief, як його побачить лікар у
    tumor-board. Якщо щось виглядає клінічно неправильно або дезорієнтує —
    <a href="{GH_NEW_ISSUE}?title=%5Bfeedback%5D+&labels=tester-feedback"
       target="_blank" rel="noopener">відкрий issue на GitHub</a>
    з посиланням на конкретний кейс.
  </p>

  <section class="case-grid">
    {cards_html}
  </section>

  <section class="kb-stats">
    {stats_widget_html}
  </section>

  <footer class="page-foot">
    OpenOnco — open-source · MIT-style usage
    · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    · Жодних реальних пацієнтських даних · CHARTER §9.3
  </footer>
</main>
</body>
</html>
"""


# ── Try page (Pyodide interactive) ────────────────────────────────────────


_PYODIDE_VERSION = "0.26.4"


def render_try() -> str:
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Спробувати</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="try")}

<main class="try-page">
  <h1>Спробувати з віртуальним пацієнтом</h1>
  <p class="lead">
    Введи (або підвантаж із прикладу) JSON-профіль синтетичного пацієнта і отримай повний
    Plan. <strong>Жодних реальних пацієнтських даних</strong> — це лише runner для перевірки
    функціоналу. Рушій (Python) запускається у твоєму браузері через Pyodide.
  </p>

  <div class="try-grid">
    <section class="try-input">
      <label>
        Завантажити приклад
        <select id="exampleSelect">
          <option value="">— оберіть —</option>
        </select>
      </label>

      <label>
        Patient profile (JSON)
        <textarea id="patientJson" rows="22" spellcheck="false" placeholder='{{"patient_id": "...", "disease": {{"icd_o_3_morphology": "9699/3"}}, ...}}'></textarea>
      </label>

      <div class="try-actions">
        <button id="runBtn" class="btn btn-primary">Згенерувати план</button>
        <button id="formatBtn" class="btn btn-secondary">Format JSON</button>
      </div>

      <div id="status" class="status"></div>
      <div id="error" class="error" hidden></div>
    </section>

    <section class="try-output">
      <div id="placeholder" class="placeholder">
        <div class="placeholder-icon">▶</div>
        <p>Результат з'явиться тут.<br>Перший запуск завантажує Pyodide (~10–15 МБ) та сам рушій. Очікуй ~10–30 секунд при першому запуску, потім &lt;1 с.</p>
      </div>
      <iframe id="resultFrame" hidden></iframe>
    </section>
  </div>

  <footer class="page-foot">
    Якщо щось не працює — <a href="{GH_NEW_ISSUE}?title=%5Btry-page%5D+&labels=tester-feedback" target="_blank" rel="noopener">відкрий issue</a>.
    Pyodide v{_PYODIDE_VERSION} · engine bundle <code>openonco-engine.zip</code>.
  </footer>
</main>

<script type="module">
import {{ loadPyodide }} from "https://cdn.jsdelivr.net/pyodide/v{_PYODIDE_VERSION}/full/pyodide.mjs";

const status = document.getElementById('status');
const errorBox = document.getElementById('error');
const runBtn = document.getElementById('runBtn');
const formatBtn = document.getElementById('formatBtn');
const exampleSelect = document.getElementById('exampleSelect');
const textarea = document.getElementById('patientJson');
const placeholder = document.getElementById('placeholder');
const resultFrame = document.getElementById('resultFrame');

let pyodide = null;
let enginReady = false;

function setStatus(msg, kind = 'info') {{
  status.textContent = msg;
  status.dataset.kind = kind;
}}
function setError(msg) {{
  if (msg) {{
    errorBox.hidden = false;
    errorBox.textContent = msg;
  }} else {{
    errorBox.hidden = true;
    errorBox.textContent = '';
  }}
}}

// Load examples list
async function loadExamples() {{
  const resp = await fetch('examples.json');
  const examples = await resp.json();
  exampleSelect.innerHTML = '<option value="">— оберіть —</option>';
  examples.forEach((ex, i) => {{
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = ex.label;
    exampleSelect.appendChild(opt);
  }});
  exampleSelect.addEventListener('change', () => {{
    const i = exampleSelect.value;
    if (i === '') return;
    textarea.value = JSON.stringify(examples[i].json, null, 2);
    setError(null);
  }});
  // Default to first example
  if (examples.length > 0) {{
    exampleSelect.value = '0';
    textarea.value = JSON.stringify(examples[0].json, null, 2);
  }}
}}

async function ensureEngine() {{
  if (enginReady) return pyodide;
  setStatus('Завантажую Pyodide…');
  pyodide = await loadPyodide({{indexURL: "https://cdn.jsdelivr.net/pyodide/v{_PYODIDE_VERSION}/full/"}});
  setStatus('Встановлюю pydantic + pyyaml…');
  await pyodide.loadPackage(['micropip']);
  await pyodide.runPythonAsync(`
import micropip
await micropip.install(['pydantic', 'pyyaml'])
`);
  setStatus('Завантажую двигун OpenOnco…');
  const resp = await fetch('openonco-engine.zip');
  const buf = await resp.arrayBuffer();
  pyodide.unpackArchive(buf, 'zip');
  // Quick smoke test
  await pyodide.runPythonAsync(`
from pathlib import Path
from knowledge_base.validation.loader import load_content
_r = load_content(Path('knowledge_base/hosted/content'))
assert _r.ok, f'KB validation failed: {{_r.schema_errors[:3]}}'
`);
  enginReady = true;
  setStatus('Двигун готовий ✓', 'ok');
  return pyodide;
}}

async function runEngine() {{
  setError(null);
  // 1. Validate JSON
  let patient;
  try {{
    patient = JSON.parse(textarea.value);
  }} catch (e) {{
    setError('Невалідний JSON: ' + e.message);
    return;
  }}
  // 2. Ensure Pyodide loaded
  try {{
    await ensureEngine();
  }} catch (e) {{
    setError('Pyodide не завантажився: ' + (e.message || e));
    setStatus('');
    return;
  }}
  // 3. Run engine
  setStatus('Запускаю двигун…');
  try {{
    pyodide.globals.set('_patient_json', JSON.stringify(patient));
    const html = await pyodide.runPythonAsync(`
import json
from pathlib import Path
from knowledge_base.engine import (
    generate_plan, generate_diagnostic_brief, is_diagnostic_profile,
    orchestrate_mdt, render_plan_html, render_diagnostic_brief_html,
)

patient = json.loads(_patient_json)
KB = Path('knowledge_base/hosted/content')
if is_diagnostic_profile(patient):
    result = generate_diagnostic_brief(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_diagnostic_brief_html(result, mdt=mdt)
else:
    result = generate_plan(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_plan_html(result, mdt=mdt)
html
`);
    placeholder.hidden = true;
    resultFrame.hidden = false;
    resultFrame.srcdoc = html;
    setStatus('Готово ✓', 'ok');
  }} catch (e) {{
    setError('Двигун повернув помилку:\\n' + (e.message || e));
    setStatus('');
  }}
}}

formatBtn.addEventListener('click', () => {{
  setError(null);
  try {{
    const obj = JSON.parse(textarea.value);
    textarea.value = JSON.stringify(obj, null, 2);
  }} catch (e) {{
    setError('Невалідний JSON: ' + e.message);
  }}
}});

runBtn.addEventListener('click', runEngine);

loadExamples().catch(e => setError('examples.json не завантажився: ' + e));
</script>
</body>
</html>
"""


# ── Per-case page (back-link banner, no auth gate) ────────────────────────


def _wrap_case_html(rendered_html: str, case: CaseEntry) -> str:
    """Insert a thin sticky bar with back-link + per-case feedback into the
    rendered Plan/Brief HTML. No auth gate — landing is fully public."""
    bar_style = (
        '<style>'
        '.case-bar{position:sticky;top:0;z-index:99;background:#0a2e1a;'
        'color:#dcfce7;padding:10px 24px;display:flex;justify-content:space-between;'
        'align-items:center;font-family:Source Sans 3,sans-serif;font-size:13px;}'
        '.case-bar a{color:#86efac;text-decoration:none;margin-left:14px;}'
        '.case-bar a:hover{text-decoration:underline;}'
        '@media print{.case-bar{display:none;}}'
        '</style>\n'
    )

    bar_html = (
        '<div class="case-bar no-print">'
        f'<div>OpenOnco · <strong>{case.label_ua}</strong></div>'
        '<div>'
        '<a href="../gallery.html">← Назад до галереї</a>'
        f'<a href="{GH_NEW_ISSUE}?title=%5Bfeedback%5D+'
        f'{case.case_id}&labels=tester-feedback" target="_blank" rel="noopener">'
        'Feedback на цей кейс</a>'
        '</div>'
        '</div>\n'
    )

    out = rendered_html.replace("</head>", bar_style + "</head>", 1)
    out = out.replace('<div class="page">', bar_html + '<div class="page">', 1)
    return out


# ── Static stylesheet ─────────────────────────────────────────────────────


_STYLE_CSS = """
:root {
  --green-900: #0a2e1a;
  --green-800: #0d3f24;
  --green-700: #14532d;
  --green-600: #166534;
  --green-500: #16a34a;
  --green-100: #dcfce7;
  --green-50: #f0fdf4;
  --teal: #0d9488;
  --amber-bg: #fffbeb;
  --amber: #d97706;
  --red-bg: #fef2f2;
  --red: #dc2626;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-500: #6b7280;
  --gray-700: #374151;
  --gray-900: #111827;
  --font-sans: 'Source Sans 3', 'Segoe UI', sans-serif;
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-mono: 'JetBrains Mono', Menlo, monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-sans);
  color: var(--gray-900);
  background: var(--gray-50);
  line-height: 1.55;
}
a { color: var(--green-700); }
main { max-width: 1100px; margin: 0 auto; padding: 0 24px 48px; }

/* Top bar */
.top-bar {
  background: var(--green-900); color: var(--green-100);
  padding: 12px 24px;
  display: flex; justify-content: space-between; align-items: center;
}
.brand-line { display: flex; align-items: center; gap: 12px; }
.brand-mini {
  font-family: var(--font-display); font-size: 18px;
  color: var(--green-100); text-decoration: none;
}
.role-pill {
  background: var(--teal); color: white;
  font-family: var(--font-mono); font-size: 10px;
  padding: 2px 8px; border-radius: 4px; letter-spacing: 0.5px;
  text-transform: uppercase;
}
.top-actions a {
  color: var(--green-100); margin-left: 16px; text-decoration: none;
  font-size: 13px;
}
.top-actions a:hover, .top-actions a.active { color: white; }
.top-actions a.active {
  border-bottom: 2px solid var(--green-100); padding-bottom: 1px;
}

/* Hero */
.hero {
  background:
    radial-gradient(ellipse at top left, var(--green-100) 0%, transparent 55%),
    radial-gradient(ellipse at bottom right, #ccfbf1 0%, transparent 55%),
    var(--gray-50);
  padding: 60px 24px 50px;
  margin: 0 -24px;
}
.hero-content { max-width: 880px; margin: 0 auto; }
.eyebrow {
  font-family: var(--font-mono); font-size: 11px; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--green-700); margin-bottom: 16px;
}
.hero h1 {
  font-family: var(--font-display); font-size: 44px; line-height: 1.12;
  color: var(--green-900); margin-bottom: 20px;
}
.hero-sub {
  font-size: 18px; color: var(--gray-700); max-width: 720px;
  margin-bottom: 28px;
}
.cta-row { display: flex; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-block; padding: 12px 22px; border-radius: 8px;
  font-weight: 600; font-size: 15px; text-decoration: none;
  font-family: var(--font-sans); cursor: pointer; border: none;
}
.btn-primary { background: var(--green-700); color: white; }
.btn-primary:hover { background: var(--green-600); }
.btn-secondary {
  background: white; color: var(--green-700);
  border: 1px solid var(--gray-200);
}
.btn-secondary:hover { border-color: var(--green-600); }
.hero-meta {
  margin-top: 24px; font-size: 12px; color: var(--gray-500);
  font-family: var(--font-mono);
}

/* Numbers */
.numbers { padding: 50px 0 30px; }
.numbers h2, .problem h2, .how h2, .gallery h1, .try-page h1 {
  font-family: var(--font-display); font-size: 30px;
  color: var(--green-900); margin-bottom: 24px;
}
.numbers-lead {
  font-size: 15px; color: var(--gray-700); margin-bottom: 24px;
  max-width: 880px;
}
.num-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 12px;
}
.num-grid--rich {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.num-card {
  background: white; border: 1px solid var(--gray-200); border-radius: 10px;
  padding: 20px 18px; border-top: 3px solid var(--green-600);
  display: flex; flex-direction: column;
}
.num-card--accent { border-top-color: var(--teal); background: linear-gradient(180deg, var(--green-50) 0%, white 40%); }
.num-big {
  font-family: var(--font-display); font-size: 38px; line-height: 1;
  color: var(--green-900);
}
.num-lbl {
  font-size: 14px; color: var(--gray-900); margin-top: 6px;
  font-weight: 700;
}
.num-detail {
  font-family: var(--font-mono); font-size: 11px; color: var(--gray-500);
  margin-top: 4px;
}
.num-text {
  font-size: 13px; color: var(--gray-700); margin-top: 10px;
  line-height: 1.5;
}
.num-text code {
  font-family: var(--font-mono); font-size: 11px;
  background: var(--gray-100); padding: 1px 5px; border-radius: 3px;
}
.num-text em { font-style: normal; font-family: var(--font-mono); font-size: 12px; color: var(--green-700); }
.num-foot {
  font-size: 13px; color: var(--gray-700); margin-top: 18px;
  padding: 14px 16px; background: var(--amber-bg);
  border-left: 3px solid var(--amber); border-radius: 4px;
}
.num-foot code { font-family: var(--font-mono); font-size: 12px; }

/* Problem */
.problem { padding: 30px 0; }
.problem-text {
  font-size: 16px; color: var(--gray-700); max-width: 880px;
  line-height: 1.65;
}

/* How it works */
.how { padding: 30px 0; }
.how-lead {
  font-size: 15px; color: var(--gray-700); max-width: 880px;
  margin-bottom: 22px;
}
.how-fig {
  background: #0a2e1a;  /* dark backdrop matches infograph palette */
  padding: 24px; border-radius: 12px; text-align: center;
  margin: 0;
}
.how-fig img {
  max-width: 100%; height: auto; border-radius: 6px;
  background: white;
}
.how-fig figcaption {
  margin-top: 14px; font-size: 13px; color: var(--green-100);
  text-align: left; line-height: 1.55;
}
.how-fig figcaption strong { color: white; }

/* Gallery */
.gallery { padding: 32px 0; }
.gallery .lead {
  font-size: 15px; color: var(--gray-700); margin-bottom: 28px;
  max-width: 760px;
}
.case-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px; margin-bottom: 36px;
}
.case-card {
  display: block; background: white; border-radius: 10px;
  border: 1px solid var(--gray-200); padding: 18px;
  text-decoration: none; color: var(--gray-900);
  transition: border-color .15s, box-shadow .15s, transform .15s;
}
.case-card:hover {
  border-color: var(--green-600);
  box-shadow: 0 6px 16px rgba(10, 46, 26, .07);
  transform: translateY(-1px);
}
.case-badge {
  display: inline-block; font-family: var(--font-mono);
  font-size: 10px; letter-spacing: 1px; text-transform: uppercase;
  padding: 3px 8px; border-radius: 4px; margin-bottom: 10px;
}
.bdg-plan { background: var(--green-100); color: var(--green-700); }
.bdg-diag { background: var(--amber-bg); color: var(--amber); }
.case-card h3 {
  font-family: var(--font-display); font-size: 18px;
  color: var(--green-900); margin-bottom: 8px; line-height: 1.25;
}
.case-card p { font-size: 13px; color: var(--gray-700); }
.case-foot {
  margin-top: 12px; font-family: var(--font-mono);
  font-size: 11px; color: var(--gray-500);
}

.kb-stats { margin-top: 16px; }

/* Try page */
.try-page { padding: 32px 0; }
.try-page .lead {
  font-size: 15px; color: var(--gray-700); margin-bottom: 24px;
  max-width: 800px;
}
.try-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
  align-items: start;
}
.try-input label {
  display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px;
  font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;
  color: var(--gray-700); font-weight: 600;
}
.try-input select, .try-input textarea {
  font-family: var(--font-mono); font-size: 13px;
  padding: 10px 12px; border: 1px solid var(--gray-200);
  border-radius: 6px; background: white;
}
.try-input textarea {
  width: 100%; resize: vertical; line-height: 1.45;
  min-height: 380px;
}
.try-input select { width: 100%; }
.try-input select:focus, .try-input textarea:focus {
  outline: 2px solid var(--green-600); outline-offset: 0;
  border-color: var(--green-600);
}
.try-actions { display: flex; gap: 8px; margin-top: 8px; }
.status {
  font-family: var(--font-mono); font-size: 12px; color: var(--gray-700);
  padding: 8px 12px; min-height: 32px; margin-top: 12px;
  background: var(--gray-50); border-radius: 4px;
  border-left: 3px solid var(--gray-200);
}
.status[data-kind="ok"] {
  background: var(--green-50); border-left-color: var(--green-500);
  color: var(--green-800);
}
.error {
  font-family: var(--font-mono); font-size: 12px; color: var(--red);
  background: var(--red-bg); padding: 10px 12px; border-radius: 4px;
  margin-top: 10px; white-space: pre-wrap;
  border-left: 3px solid var(--red);
}
.try-output {
  background: white; border: 1px solid var(--gray-200);
  border-radius: 10px; min-height: 600px;
  display: flex; flex-direction: column; overflow: hidden;
}
.placeholder {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 40px; text-align: center; color: var(--gray-500);
}
.placeholder-icon {
  font-size: 48px; color: var(--green-600); margin-bottom: 16px;
  font-family: var(--font-display);
}
#resultFrame {
  flex: 1; width: 100%; height: 800px; border: none;
}

@media (max-width: 800px) {
  .hero h1 { font-size: 32px; }
  .problem-grid, .try-grid { grid-template-columns: 1fr; }
}

/* Page footer */
.page-foot {
  margin-top: 36px; padding-top: 18px;
  border-top: 1px solid var(--gray-200);
  font-size: 12px; color: var(--gray-500);
}
.page-foot a { color: var(--green-700); }
"""


# ── Build orchestration ───────────────────────────────────────────────────


def build_one_case(case: CaseEntry, output_dir: Path) -> Path:
    patient_path = EXAMPLES / case.file
    patient = json.loads(patient_path.read_text(encoding="utf-8"))

    if is_diagnostic_profile(patient):
        result = generate_diagnostic_brief(patient, kb_root=KB_ROOT)
        mdt = orchestrate_mdt(patient, result, kb_root=KB_ROOT)
        html = render_diagnostic_brief_html(result, mdt=mdt)
    else:
        result = generate_plan(patient, kb_root=KB_ROOT)
        mdt = orchestrate_mdt(patient, result, kb_root=KB_ROOT)
        html = render_plan_html(result, mdt=mdt)

    wrapped = _wrap_case_html(html, case)
    out_path = output_dir / "cases" / f"{case.case_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(wrapped, encoding="utf-8")
    return out_path


def _copy_landing_assets(output_dir: Path) -> list[str]:
    """Copy infographic images used by the landing into docs/. Source-of-truth
    lives in infograph/ (gitignored except these). Listed by name so we don't
    accidentally copy patient HTMLs (CHARTER §9.3)."""
    src_root = REPO_ROOT / "infograph"
    assets = ["MDT.png"]
    copied: list[str] = []
    for name in assets:
        src = src_root / name
        if src.exists():
            shutil.copyfile(src, output_dir / name)
            copied.append(name)
    return copied


def build_site(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cases").mkdir(parents=True, exist_ok=True)
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    (output_dir / "style.css").write_text(_STYLE_CSS, encoding="utf-8")
    landing_assets = _copy_landing_assets(output_dir)

    stats = collect_stats()

    (output_dir / "index.html").write_text(render_landing(stats), encoding="utf-8")
    (output_dir / "gallery.html").write_text(
        render_gallery(format_html_widget(stats, embed_style=True)),
        encoding="utf-8",
    )
    (output_dir / "try.html").write_text(render_try(), encoding="utf-8")

    case_paths = [{
        "case_id": c.case_id,
        "path": str(build_one_case(c, output_dir).relative_to(output_dir)),
    } for c in CASES]

    engine_bundle = bundle_engine(output_dir)
    examples_payload = bundle_examples(output_dir)

    return {
        "output_dir": str(output_dir),
        "cases_built": len(case_paths),
        "cases": case_paths,
        "engine_bundle": engine_bundle,
        "examples_payload": examples_payload,
        "landing_assets": landing_assets,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build OpenOnco static site for GitHub Pages.")
    parser.add_argument("--output", default="docs", help="Output directory (default: docs/)")
    parser.add_argument("--clean", action="store_true", help="Wipe output directory before building.")
    args = parser.parse_args(argv)

    output_dir = (REPO_ROOT / args.output) if not Path(args.output).is_absolute() else Path(args.output)
    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    report = build_site(output_dir)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
