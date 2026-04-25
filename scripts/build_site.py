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
        summary_ua="High-Grade B-Cell Lymphoma з MYC + BCL2 break-apart — engine обирає DA-EPOCH-R (substantial OS improvement vs R-CHOP); reuse схеми з Burkitt.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    # ── T-cell block + Hodgkin (final marathon block) ──────────────────────
    CaseEntry(
        case_id="alcl-alk-negative",
        file="patient_alcl_alk_negative.json",
        label_ua="ALCL · ALK-negative (CHP-Bv)",
        summary_ua="Системна анапластична великоклітинна лімфома, ALK-negative — universally CD30+. Engine обирає CHP-Bv (ECHELON-2: brentuximab замість vincristine).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="ptcl-cd30-negative",
        file="patient_ptcl_cd30_negative.json",
        label_ua="PTCL NOS · CD30-negative (CHOEP)",
        summary_ua="Периферична T-клітинна лімфома, CD30-negative — engine обирає CHOEP (CHOP + etoposide). CD30+ варіант ескалював би до CHP-Bv.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="aitl-cd30-positive",
        file="patient_aitl_cd30_positive.json",
        label_ua="AITL · CD30-positive (CHP-Bv)",
        summary_ua="Ангіоімунобластна T-клітинна лімфома, CD30+ — RF-TCELL-CD30-POSITIVE fired. Engine обирає CHP-Bv.",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="chl-advanced",
        file="patient_chl_advanced.json",
        label_ua="Classical Hodgkin · Advanced (A+AVD)",
        summary_ua="Стадія IV cHL — RF-CHL-ADVANCED-STAGE fired. Engine обирає A+AVD (ECHELON-1: brentuximab замість bleomycin, superior OS).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="chl-early",
        file="patient_chl_early.json",
        label_ua="Classical Hodgkin · Early Stage (ABVD)",
        summary_ua="Стадія IIA cHL, без advanced criteria — engine обирає ABVD × 2-4 + ISRT (response-adapted).",
        badge="Treatment Plan",
        badge_class="bdg-plan",
    ),
    CaseEntry(
        case_id="nlpbl-early",
        file="patient_nlpbl_early.json",
        label_ua="NLPBL · Early Stage (Observation / RT)",
        summary_ua="Нодулярна лімфоцит-домінантна B-клітинна лімфома (перекласифіковано WHO 5th-ed з NLPHL у B-cell) — early stage. Engine обирає observation / ISRT alone.",
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
    <a href="capabilities.html"{cls("capabilities")}>Можливості</a>
    <a href="limitations.html"{cls("limitations")}>Обмеження</a>
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
    refs_thousands = stats.corpus_references_total // 1000
    refs_compact = (
        f"{refs_thousands:,}K+" if refs_thousands >= 1
        else f"{stats.corpus_references_total:,}+"
    )

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
      <div class="hero-corpus">
        <div class="hcorpus-num">{refs_compact}</div>
        <div class="hcorpus-text">
          <strong>{stats.corpus_references_total:,}+ клінічних публікацій</strong>
          реферуються під {n_sources} обраними guidelines
          (NCCN · ESMO · BSH · EHA · EASL · WHO · МОЗ).
          <strong>{stats.corpus_pages_total:,}</strong> сторінок керівництв сумарно.
          Жоден лікар фізично не може опрацювати такий обсяг для кожного пацієнта —
          engine реферує його за вас.
        </div>
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
          Кожен схема — список drugs з дозами, шкалою циклів, dose adjustments
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

      <div class="num-card num-card--accent">
        <div class="num-big">{n_sources}</div>
        <div class="num-lbl">Джерела (top-level guidelines + RCTs)</div>
        <div class="num-detail">NCCN · ESMO · EHA · BSH · EASL · МОЗ · WHO · CTCAE · FDA</div>
        <p class="num-text">
          Під цими {n_sources} джерелами — <strong>{stats.corpus_references_total:,}+ primary
          clinical publications</strong> (RCTs, мета-аналізи, когортні дослідження)
          і <strong>{stats.corpus_pages_total:,} сторінок керівництв</strong>. Сама лише
          NCCN B-Cell Lymphomas guideline — ~500 сторінок з ~700 references.
          Кожна Indication / Regimen / RedFlag цитує конкретні джерела з
          <em>position</em> (supports / contradicts / context), paraphrased
          quote, page/section. FDA Criterion 4 — лікар незалежно перевіряє
          підставу кожної рекомендації.
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
.hero-corpus {
  margin-top: 32px; padding: 18px 22px;
  background: white; border-radius: 12px;
  border: 1px solid var(--green-100);
  box-shadow: 0 4px 14px rgba(10, 46, 26, 0.05);
  display: flex; gap: 22px; align-items: center;
  max-width: 720px;
}
.hcorpus-num {
  font-family: var(--font-display); font-size: 56px;
  color: var(--green-700); line-height: 1;
  flex-shrink: 0;
}
.hcorpus-text {
  font-size: 14.5px; color: var(--gray-700);
  line-height: 1.55;
}
.hcorpus-text strong { color: var(--green-900); }
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

/* Info pages (capabilities / limitations) */
.info-page { padding: 32px 0 48px; }
.info-page h1 {
  font-family: var(--font-display); font-size: 36px;
  color: var(--green-900); margin-bottom: 10px;
}
.info-page .lead {
  font-size: 16px; color: var(--gray-700); max-width: 820px;
  margin-bottom: 28px; line-height: 1.6;
}
.info-section { margin-top: 36px; }
.info-section h2 {
  font-family: var(--font-display); font-size: 24px;
  color: var(--green-900); margin-bottom: 14px;
}
.info-section p { font-size: 14.5px; color: var(--gray-700); margin-bottom: 12px; }
.info-section .info-text {
  max-width: 820px; line-height: 1.6;
}
.flow-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 10px; margin: 18px 0;
}
.flow-step {
  background: white; border: 1px solid var(--gray-200);
  border-radius: 10px; padding: 14px 14px;
  border-top: 3px solid var(--green-600);
}
.flow-step .flow-num {
  font-family: var(--font-mono); font-size: 11px;
  color: var(--green-700); margin-bottom: 6px;
  letter-spacing: 1px; text-transform: uppercase;
}
.flow-step .flow-title {
  font-weight: 700; font-size: 14px;
  color: var(--gray-900); margin-bottom: 6px;
  font-family: var(--font-display);
}
.flow-step .flow-desc {
  font-size: 12.5px; color: var(--gray-700); line-height: 1.45;
}
.flow-step code {
  font-family: var(--font-mono); font-size: 11px;
  background: var(--gray-100); padding: 1px 5px; border-radius: 3px;
}
.gap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}
.gap-card {
  background: white; border: 1px solid var(--gray-200);
  border-radius: 10px; padding: 16px 18px;
  border-left: 3px solid var(--amber);
}
.gap-card .gap-tag {
  font-family: var(--font-mono); font-size: 11px;
  color: var(--amber); letter-spacing: 0.5px; text-transform: uppercase;
  margin-bottom: 6px;
}
.gap-card h3 {
  font-family: var(--font-display); font-size: 17px;
  color: var(--green-900); margin-bottom: 8px;
}
.gap-card p { font-size: 13px; color: var(--gray-700); line-height: 1.5; }
.gap-card.gap-hard { border-left-color: var(--red); }
.gap-card.gap-hard .gap-tag { color: var(--red); }
.q-list {
  background: var(--green-50); border: 1px solid var(--green-100);
  border-radius: 8px; padding: 14px 18px; margin: 12px 0;
}
.q-list h4 {
  font-family: var(--font-display); font-size: 15px;
  color: var(--green-900); margin-bottom: 8px;
}
.q-list ul { padding-left: 18px; font-size: 13px; color: var(--gray-700); }
.q-list li { margin-bottom: 4px; line-height: 1.5; }
.q-list code {
  font-family: var(--font-mono); font-size: 11px;
  background: white; padding: 1px 5px; border-radius: 3px;
  color: var(--green-800);
}
.callout {
  background: var(--amber-bg); border-left: 3px solid var(--amber);
  padding: 12px 16px; border-radius: 4px; margin: 16px 0;
  font-size: 13.5px; color: var(--gray-900); line-height: 1.55;
}
.callout.callout-good {
  background: var(--green-50); border-left-color: var(--green-600);
}
.callout.callout-hard {
  background: var(--red-bg); border-left-color: var(--red);
}
.kv-table {
  width: 100%; border-collapse: collapse; font-size: 13px;
  margin-top: 10px;
}
.kv-table th, .kv-table td {
  text-align: left; padding: 8px 10px;
  border-bottom: 1px solid var(--gray-100);
}
.kv-table th {
  background: var(--gray-50); font-weight: 600;
  color: var(--gray-700); font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.04em;
}
.kv-table code {
  font-family: var(--font-mono); font-size: 11px;
  background: var(--gray-100); padding: 1px 5px; border-radius: 3px;
}

/* Page footer */
.page-foot {
  margin-top: 36px; padding-top: 18px;
  border-top: 1px solid var(--gray-200);
  font-size: 12px; color: var(--gray-500);
}
.page-foot a { color: var(--green-700); }
"""


# ── Capabilities page ─────────────────────────────────────────────────────


def render_capabilities(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_regimens = by_type.get("regimens", 0)
    n_tests = by_type.get("tests", 0)
    n_redflags = by_type.get("redflags", 0)
    n_workups = by_type.get("workups", 0)
    n_sources = by_type.get("sources", 0)
    n_drugs = by_type.get("drugs", 0)
    n_skills = stats.skills_planned_roles

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Можливості</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="capabilities")}

<main>
  <section class="info-page">
    <h1>Можливості</h1>
    <p class="lead">
      OpenOnco приймає JSON-профіль пацієнта і повертає структурований план
      лікування або діагностичний brief, з повним trace кожного рішення і
      цитуваннями всіх джерел. Жодного «чорного ящика»: усе рішення складається
      з декларативних правил, які можна прочитати у KB і відстежити в trace.
      Нижче — детально, як ми працюємо з даними, джерелами і запитами.
    </p>

    <div class="info-section">
      <h2>1. Як обробляється запит</h2>
      <p class="info-text">
        Лікар дає engine'у JSON-профіль пацієнта (FHIR/mCODE-сумісний у
        майбутньому, спрощений dict у MVP). Engine виконує 6 послідовних
        стадій і повертає Plan з ≥2 альтернативними tracks (CHARTER §2 —
        обидва треки в одному документі, alternative не сховано).
      </p>
      <div class="flow-strip">
        <div class="flow-step">
          <div class="flow-num">Stage 1</div>
          <div class="flow-title">Disease + Algorithm resolve</div>
          <div class="flow-desc">
            <code>disease.icd_o_3_morphology</code> або <code>disease.id</code>
            → знайти Disease entity. Disease + <code>line_of_therapy</code>
            → знайти відповідний Algorithm.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 2</div>
          <div class="flow-title">Findings flattening</div>
          <div class="flow-desc">
            Об'єднує <code>demographics</code> + <code>biomarkers</code>
            + <code>findings</code> в один flat dict для evaluation.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 3</div>
          <div class="flow-title">RedFlag evaluation</div>
          <div class="flow-desc">
            Кожен з {n_redflags} RedFlag-ів перевіряється проти findings.
            Boolean rule engine: <code>any_of</code>/<code>all_of</code>/<code>none_of</code>
            clauses з threshold-ами.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 4</div>
          <div class="flow-title">Algorithm walk</div>
          <div class="flow-desc">
            Decision tree крок за кроком. Кожен step → outcome → branch
            (<code>result</code> або <code>next_step</code>). Trace зберігає
            всі fired_red_flags на кожному кроці.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 5</div>
          <div class="flow-title">Tracks materialization</div>
          <div class="flow-desc">
            ВСІ Indication з <code>algorithm.output_indications</code> стають
            окремими tracks (standard / aggressive / surveillance). Selected
            = default, перший. Решта — alternative.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 6</div>
          <div class="flow-title">Per-track resolution</div>
          <div class="flow-desc">
            Indication → Regimen → MonitoringSchedule + SupportiveCare +
            Contraindications. Все resolve'иться з KB readonly.
          </div>
        </div>
      </div>
      <p class="info-text">
        Час обробки одного пацієнта — 50-200&nbsp;ms (KB load домінує). У
        Pyodide перший запуск 8-15&nbsp;сек (завантаження runtime), наступні
        — як локальний CLI. <strong>Серверу немає</strong> — engine крутиться
        локально (CLI) або у браузері користувача (Pyodide). Patient JSON
        ніколи не залишає машину.
      </p>
    </div>

    <div class="info-section">
      <h2>2. Як ми працюємо з даними пацієнта</h2>
      <p class="info-text">
        Engine читає лише структуровані поля з patient profile. Кожне поле
        має чітку семантику: або тригерить RedFlag, або filter'ує доступні
        Indications, або configurує Regimen materialization. Невпізнані поля
        ігноруються — ніяких «прихованих ефектів».
      </p>
      <table class="kv-table">
        <thead><tr><th>Категорія</th><th>Що читаємо</th><th>Як використовуємо</th></tr></thead>
        <tbody>
          <tr>
            <td>Disease (вхідна точка)</td>
            <td><code>disease.id</code> · <code>icd_o_3_morphology</code> · <code>line_of_therapy</code></td>
            <td>визначає який Algorithm запускати</td>
          </tr>
          <tr>
            <td>Diagnostic mode trigger</td>
            <td><code>disease.suspicion.lineage_hint</code> · <code>tissue_locations</code> · <code>presentation</code></td>
            <td>вмикає DiagnosticPlan замість Plan (workup brief)</td>
          </tr>
          <tr>
            <td>Demographics</td>
            <td><code>age</code> · <code>sex</code> · <code>ecog</code> · <code>fit_for_transplant</code> · <code>decompensated_cirrhosis</code> · <code>pregnancy_status</code></td>
            <td>filter в <code>Indication.applicable_to.demographic_constraints</code></td>
          </tr>
          <tr>
            <td>Biomarkers</td>
            <td>будь-які <code>BIO-X</code> з KB як ключі: <code>BIO-CLL-HIGH-RISK-GENETICS</code>, <code>BIO-MM-CYTOGENETICS-HR</code>, <code>BIO-HCV-RNA</code>, ...</td>
            <td>тригерять RedFlags, filter'ять Indications</td>
          </tr>
          <tr>
            <td>Findings</td>
            <td>{n_redflags}+ структурованих полів — <code>dominant_nodal_mass_cm</code>, <code>ldh_ratio_to_uln</code>, <code>creatinine_clearance_ml_min</code>, <code>blastoid_morphology</code>, <code>tp53_mutation</code>, <code>del_17p</code>, ...</td>
            <td>thresholds у RedFlag triggers</td>
          </tr>
          <tr>
            <td>Prior tests completed</td>
            <td><code>prior_tests_completed: [TEST-IDs]</code></td>
            <td>виключає вже зроблені тести з generated workup_steps</td>
          </tr>
          <tr>
            <td>Clinical record (free-form)</td>
            <td>будь-який <code>clinical_record</code> envelope</td>
            <td>не читається engine'ом — використовується тільки render layer для context</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="info-section">
      <h2>3. Як ми працюємо з джерелами — і чому це наша ключова перевага</h2>
      <div class="hero-corpus" style="max-width:none; margin-bottom:18px;">
        <div class="hcorpus-num">{stats.corpus_references_total:,}+</div>
        <div class="hcorpus-text">
          <strong>{stats.corpus_references_total:,}+ primary clinical publications</strong>
          (RCTs, мета-аналізи, когортні дослідження) реферуються під
          <strong>{n_sources} обраними top-level guidelines</strong>.
          Сумарно — <strong>{stats.corpus_pages_total:,} сторінок керівництв</strong>.
          Жоден лікар фізично не може опрацювати такий обсяг для кожного пацієнта;
          engine реферує його за вас і повертає Plan з phrased citations + page links.
        </div>
      </div>
      <p class="info-text">
        Кожне джерело — це окрема <code>Source</code> entity з власним ID
        (наприклад <code>SRC-NCCN-BCELL-2025</code>), title, version, license,
        access mode (referenced vs hosted per SOURCE_INGESTION_SPEC §1.4).
        Зараз у KB <strong>{n_sources}</strong> джерел:
      </p>
      <table class="kv-table">
        <thead><tr><th>Source ID</th><th>Тип</th><th>Сторінок</th><th>Primary refs</th><th>Роль у корпусі</th></tr></thead>
        <tbody>
          <tr><td><code>SRC-NCCN-BCELL-2025</code></td><td>NCCN B-Cell Lymphomas v.2.2025</td><td class="num">500</td><td class="num">700</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MM-2025</code></td><td>NCCN Multiple Myeloma 2025</td><td class="num">400</td><td class="num">600</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-AML-2025</code></td><td>NCCN AML 2025</td><td class="num">350</td><td class="num">500</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MPN-2025</code></td><td>NCCN MPN 2025</td><td class="num">300</td><td class="num">400</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-EASL-HCV-2023</code></td><td>EASL HCV Guidelines 2023</td><td class="num">80</td><td class="num">250</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-WHO-LNSC-2023</code></td><td>WHO Lymph Node, Spleen, Thymus Cytopathology</td><td class="num">150</td><td class="num">200</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-CTCAE-V5</code></td><td>NCI CTCAE v5.0 (toxicity terminology)</td><td class="num">150</td><td class="num">30</td><td>terminology</td></tr>
          <tr><td><code>SRC-ESMO-MZL-2024</code></td><td>ESMO Marginal Zone Lymphomas 2024</td><td class="num">30</td><td class="num">150</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-BSH-MZL-2024</code></td><td>BSH MZL Guideline 2024</td><td class="num">50</td><td class="num">120</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-EHA-WORKUP-2024</code></td><td>EHA Practical Workup Guidelines 2024</td><td class="num">40</td><td class="num">100</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-MOZ-UA-LYMPH-2024</code></td><td>МОЗ Україна — Лімфоми (placeholder)</td><td class="num">60</td><td class="num">50</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-ARCAINI-2014</code></td><td>IELSG-19 RCT — MALT lymphoma</td><td class="num">10</td><td class="num">50</td><td>rct_publication</td></tr>
          <tr><td><code>SRC-FDA-CDS-2026</code></td><td>FDA CDS Software Guidance 2026</td><td class="num">30</td><td class="num">20</td><td>regulatory</td></tr>
          <tr><td colspan="2"><strong>Сумарно</strong></td><td class="num"><strong>{stats.corpus_pages_total:,}</strong></td><td class="num"><strong>{stats.corpus_references_total:,}+</strong></td><td>—</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        <strong>Кожна клінічна claim у KB має citation</strong>. Indication,
        Regimen, RedFlag, Algorithm — всі мають поле <code>sources: list</code>
        де для кожного джерела вказано:
      </p>
      <div class="q-list">
        <h4>Структура citation</h4>
        <ul>
          <li><code>source_id</code> — посилання на Source entity</li>
          <li><code>position</code> — <em>supports</em> / <em>contradicts</em> / <em>context</em></li>
          <li><code>relevant_quote_paraphrase</code> — паніфразоване твердження з guideline (не дослівне copy-paste для license safety)</li>
          <li><code>page_or_section</code> — точна локалізація в документі</li>
        </ul>
      </div>
      <p class="info-text">
        Render layer показує <strong>повний список cited sources</strong>
        під кожною Indication у Plan. Це і є FDA Criterion 4 (CHARTER §15.2):
        лікар може незалежно перевірити підставу кожної рекомендації, не
        довіряючись engine на віру.
      </p>
      <div class="callout callout-good">
        <strong>Source hosting за замовчуванням — referenced.</strong>
        Ми не дублюємо бази (NCCN, ESMO, etc.) — посилаємось. Hosting
        потребує explicit H1-H5 justification (CHARTER §15.2 referenced
        vs hosted vs mixed). Виключення: PDF документи (FDA CDS, CTCAE)
        збережено локально для archive stability.
      </div>
    </div>

    <div class="info-section">
      <h2>4. Як ми обробляємо запити</h2>
      <p class="info-text">
        Три способи запустити engine, жоден не серверний:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">CLI</div>
          <div class="num-lbl">Локально на машині лікаря</div>
          <p class="num-text">
            <code>python -m knowledge_base.engine.cli --patient profile.json --render plan.html</code>.
            Працює offline, не потребує мережі. Profile залишається на диску.
          </p>
        </div>
        <div class="num-card num-card--accent">
          <div class="num-big">Pyodide</div>
          <div class="num-lbl">У браузері (try.html)</div>
          <p class="num-text">
            Pyodide v0.26.4 завантажує Python WebAssembly runtime, micropip
            ставить pydantic+pyyaml, розпаковує engine bundle (~302KB) у
            in-memory FS. Engine крутиться у браузері. Patient JSON не
            покидає машину.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">Library</div>
          <div class="num-lbl">Python import</div>
          <p class="num-text">
            <code>from knowledge_base.engine import generate_plan, revise_plan</code>
            — інтеграція з EHR, CSV pipelines, batch testing. Stateless, deterministic.
          </p>
        </div>
      </div>
      <div class="callout callout-good">
        <strong>Privacy by design.</strong> Patient JSON ніколи не залишає
        машину користувача. Немає логів, немає БД, немає accidental
        leakage. Reproducibility: <code>Plan.knowledge_base_state.algorithm_version</code>
        фіксує версію KB → same input + same KB = same output.
      </div>
    </div>

    <div class="info-section">
      <h2>5. Що повертаємо назад</h2>
      <p class="info-text">
        Engine повертає <strong>Plan</strong> (treatment mode) або
        <strong>DiagnosticPlan</strong> (workup brief). Кожен Plan містить:
      </p>
      <table class="kv-table">
        <thead><tr><th>Поле</th><th>Що містить</th></tr></thead>
        <tbody>
          <tr><td><code>tracks[]</code></td><td>≥2 alternative tracks (default first), кожен з indication + regimen + monitoring + supportive_care + contraindications</td></tr>
          <tr><td><code>fda_compliance</code></td><td>FDA Criterion 4 fields: intended_use, hcp_user_specification, patient_population_match, algorithm_summary, data_sources_summary, data_limitations, automation_bias_warning</td></tr>
          <tr><td><code>trace</code></td><td>покрокова історія walk_algorithm: step / outcome / branch / fired_red_flags для кожного кроку</td></tr>
          <tr><td><code>knowledge_base_state</code></td><td>snapshot версії KB на момент генерації (audit per CHARTER §10.2)</td></tr>
          <tr><td><code>kb_resolved</code></td><td>всі referenced entities (Disease, Tests, RedFlags, Algorithm) для render layer</td></tr>
          <tr><td><code>warnings</code></td><td>schema/ref errors, time_critical disqualifications, missing data hints</td></tr>
          <tr><td><code>supersedes</code> / <code>superseded_by</code></td><td>версійний chain між plans для тієї ж пацієнта</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        Опціонально вмикається <strong>MDT brief</strong> — orchestrate_mdt() читає Plan +
        патієнтський профіль і додає required/recommended/optional ролі (з {n_skills}
        віртуальних спеціалістів), open questions, provenance graph. Renders як inline
        section у Plan HTML.
      </p>
    </div>

    <div class="info-section">
      <h2>6. Як план оновлюється при появі нових даних</h2>
      <p class="info-text">
        <code>revise_plan(updated_patient, previous_plan, revision_trigger)</code>
        приймає оновлений профіль і генерує нову версію плану з
        <code>supersedes</code>/<code>superseded_by</code> chain. Три легальні
        переходи + одна заборона:
      </p>
      <table class="kv-table">
        <thead><tr><th>Із</th><th>Зі змінами</th><th>Перехід</th><th>Результат</th></tr></thead>
        <tbody>
          <tr><td>DiagnosticPlan vN</td><td>тільки suspicion (без histology)</td><td>diagnostic → diagnostic</td><td>DiagnosticPlan v(N+1)</td></tr>
          <tr><td>DiagnosticPlan vN</td><td>підтверджена histology</td><td>diagnostic → treatment <strong>(promotion)</strong></td><td>Plan v1 (перший treatment)</td></tr>
          <tr><td>Plan vN</td><td>будь-яке оновлення з histology</td><td>treatment → treatment</td><td>Plan v(N+1)</td></tr>
          <tr><td>Plan vN</td><td>видалено histology</td><td colspan="2"><span style="color:var(--red);font-weight:600;">ILLEGAL — ValueError, CHARTER §15.2 C7</span></td></tr>
        </tbody>
      </table>
      <p class="info-text">
        Попередній plan <strong>не мутується</strong> — повертається deep copy
        з <code>superseded_by</code> заповненим. Caller (CLI / EHR) сам вирішує
        що робити з обома версіями. Per CHARTER §10.2 — стара версія
        зберігається indefinitely.
      </p>
      <div class="callout callout-good">
        <strong>Що тригерить новий plan:</strong> зміна будь-якого з ~30 структурованих
        полів — нові biomarkers (del(17p) виявлено), нова стадія (ECOG 1→3),
        нові findings (bulky disease на restaging), нові infectious flags (HBV
        reactivation), pregnancy detected. Зміна <code>clinical_record</code>
        free-text НЕ тригерить regeneration (engine не читає free text).
      </div>
    </div>

    <div class="info-section">
      <h2>7. Що ще робимо</h2>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">{n_workups}</div>
          <div class="num-lbl">Diagnostic workups</div>
          <p class="num-text">
            Pre-biopsy режим: коли histology ще немає, engine видає
            <strong>Workup Brief</strong> зі списком тестів, biopsy approach,
            IHC panel і ролей triage MDT. Per CHARTER §15.2 C7 — без
            histology treatment Plan не генерується.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">MDT</div>
          <div class="num-lbl">Multidisciplinary brief</div>
          <p class="num-text">
            Orchestrator читає Plan + profile і призначає required/recommended/
            optional ролі ({n_skills} catalog), формулює open questions
            (Q1-Q6 + DQ1-DQ4), будує decision provenance graph.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">stats</div>
          <div class="num-lbl">KB dashboard</div>
          <p class="num-text">
            <code>python -m knowledge_base.stats</code> — actual entity counts
            + per-disease coverage matrix + reviewer signoff ratio. Доступне
            як CLI / JSON / embeddable HTML widget для landing page.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">render</div>
          <div class="num-lbl">A4 print-friendly HTML</div>
          <p class="num-text">
            Single-file HTML з embedded CSS, без external assets крім Google Fonts.
            Adapt'ується під A4 print через <code>@page</code> + <code>@media print</code>.
            Tracks side-by-side, alternative не сховано (anti automation-bias per CHARTER §15.2 C6).
          </p>
        </div>
      </div>
    </div>
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


# ── Limitations page ──────────────────────────────────────────────────────


def render_limitations(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_redflags = by_type.get("redflags", 0)
    diseases_full = sum(1 for d in stats.diseases if d.coverage_status in {"stub_full_chain", "reviewed"})

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Обмеження</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="limitations")}

<main>
  <section class="info-page">
    <h1>Обмеження</h1>
    <p class="lead">
      OpenOnco свідомо не намагається замінити лікаря або повноцінну
      MDT-команду. Цей розділ — повний і чесний список того, що engine
      <strong>не робить</strong>, де він <strong>відмовляється</strong>
      генерувати план без додаткових даних, і де клінічне рішення
      залишається за лікарем. Знати обмеження так само важливо, як
      знати можливості.
    </p>

    <div class="callout callout-hard">
      <strong>STUB-статус усього клінічного контенту.</strong>
      Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
      (CHARTER §6.1 вимагає двох Clinical Co-Lead approvals для будь-якої
      Indication, перш ніж її можна вважати «published»). Зараз весь контент
      — STUB. Це інструмент демонстрації архітектури, не клінічна довідка
      для реальних пацієнтів. Стан станом на <code>{stats.generated_at_utc}</code>.
    </div>

    <div class="info-section">
      <h2>1. Виявлення відсутніх даних — Open Questions механізм</h2>
      <p class="info-text">
        Engine <strong>не приймає рішення без потрібних даних</strong>. Замість
        того, щоб мовчки brati default, він явно фіксує які поля бракує і
        якого тесту/висновку потребує. Цей механізм називається
        <strong>Open Questions</strong> і він — цілеспрямована частина
        MDT-orchestrator (Q1-Q6 + DQ1-DQ4 rules per MDT_ORCHESTRATOR_SPEC §3).
      </p>
      <div class="q-list">
        <h4>Treatment-mode Open Questions (Q1-Q6) — приклади з реального коду</h4>
        <ul>
          <li><strong>Q1 — Histology not confirmed:</strong> якщо <code>disease.id</code> резолвиться але немає <code>biopsy_date</code> чи <code>histology_report</code> — engine emits warning «Treatment Plan generated against ICD-O-3 code only; recommend confirming primary histology before initiating therapy».</li>
          <li><strong>Q2 — Stage missing:</strong> якщо Algorithm.decision_tree посилається на staging але profile немає <code>stage</code> — fall-through на default з flag «Lugano/Ann Arbor stage required for confident risk-stratification».</li>
          <li><strong>Q3 — RedFlag clause references findings absent:</strong> якщо <code>RF-MM-HIGH-RISK-CYTOGENETICS</code> перевіряє <code>tp53_mutation</code> + <code>del_17p</code> + <code>t_4_14</code> + <code>gain_1q</code>, а в profile є тільки <code>del_17p</code> — engine не дає false negative; emits «Cytogenetic panel incomplete; high-risk status assessed with partial data».</li>
          <li><strong>Q4 — Biomarker required by Indication missing:</strong> якщо <code>IND-CLL-1L-VENO</code> вимагає <code>BIO-CLL-HIGH-RISK-GENETICS</code> для default-track selection — engine emits «IGHV mutation status + FISH del(17p) required to confirm 1L recommendation».</li>
          <li><strong>Q5 — Performance status missing:</strong> якщо <code>ecog</code> відсутній — fall на conservative default (тільки standard track), emits «ECOG performance status required for transplant-eligibility assessment».</li>
          <li><strong>Q6 — Drug availability flag:</strong> якщо selected Regimen містить препарат позначений як <code>nszu_reimbursement: false</code> (наприклад daratumumab у MM) — emits «D-VRd: daratumumab not currently NSZU-reimbursed in Ukraine; verify funding pathway before initiation».</li>
        </ul>
      </div>
      <div class="q-list">
        <h4>Diagnostic-mode Open Questions (DQ1-DQ4) — для pre-biopsy режиму</h4>
        <ul>
          <li><strong>DQ1 — Tissue location missing:</strong> якщо <code>suspicion.tissue_locations</code> empty — workup match не може ranжувати, emits «Тип ткани локалізації потрібно вказати для матчингу workup».</li>
          <li><strong>DQ2 — Lineage hint absent:</strong> без <code>lineage_hint</code> engine використовує тільки tissue + presentation для matching, lower confidence.</li>
          <li><strong>DQ3 — Presentation free-text empty:</strong> presentation_keywords scoring × 0; only lineage + tissue brati участь.</li>
          <li><strong>DQ4 — Working hypotheses not provided:</strong> engine не має preferred direction, переважає найбільш generic workup (наприклад <code>WORKUP-LYMPHADENOPATHY-NONSPECIFIC</code> замість <code>WORKUP-SUSPECTED-LYMPHOMA</code>).</li>
        </ul>
      </div>
      <div class="callout">
        <strong>Чому не «беремо default тихо»:</strong> CHARTER §15.2 C6 (anti
        automation-bias) — engine не може робити вигляд що знає коли не знає.
        Кожна missing-data ситуація має бути візуально помітна лікарю.
        Open Questions рендеряться у Plan як окрема section, не сховано.
      </div>
    </div>

    <div class="info-section">
      <h2>2. П'ять gap-ів персоналізації</h2>
      <p class="info-text">
        «Персоналізація» в OpenOnco — це rule-based <strong>вибір з фіксованих
        варіантів</strong>, а не AI-генерація. Цe навмисна архітектурна позиція
        (CHARTER §8.3 — заборонені prompt patterns). Конкретні gap-и:
      </p>
      <div class="gap-grid">
        <div class="gap-card">
          <div class="gap-tag">Gap 1</div>
          <h3>Без per-patient dose calculation</h3>
          <p>
            Regimen зберігає <strong>стандартну дозу</strong> (<code>bortezomib 1.3 mg/m²</code>),
            не множиться на BSA пацієнта і не зменшується під CrCl 30 мл/хв
            автоматично. Лікар сам перераховує. Це принципово, щоб уникнути
            класифікації як FDA medical device.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 2</div>
          <h3>Без response-adapted cycle adjustment</h3>
          <p>
            Regimen фіксує <code>total_cycles: 6 + 2 maintenance</code>.
            Engine не адаптується автоматично на основі response (PR vs CR
            після PET2). Re-staging plan генерується через окремий
            <code>revise_plan</code> з новим profile — лікар явно тригерить.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 3</div>
          <h3>Genomic matching обмежений curated biomarkers</h3>
          <p>
            Якщо у пацієнта виявили PD-L1 78%, engine не запропонує pembrolizumab —
            бо немає Indication з відповідним biomarker_requirement у KB.
            Це обмеження coverage (треба додати entity), не engine-логіки.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 4</div>
          <h3>SupportiveCare однакова для всіх на одному режимі</h3>
          <p>
            PJP prophylaxis attached до D-VRd для всіх — навіть для пацієнта
            з алергією на bactrim. Engine не знає альтернатив (dapsone замість
            bactrim). Лікар сам substitute'ить.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 5</div>
          <h3>Без cumulative-toxicity tracking між lines</h3>
          <p>
            2L plan для пацієнта що отримав bortezomib у 1L з grade 2
            нейропатією — engine не знає про попередній exposure якщо
            нічого нового не вказано. Profile не carrier'ить
            <code>prior_treatment_history</code> як structured field зараз.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>3. Жорсткі CHARTER-обмеження (will not change)</h2>
      <p class="info-text">
        Це не technical debt — це принципові архітектурні рішення
        що визначають позицію проекту як non-device CDS і
        gатекіпять FDA / клінічну безпеку.
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §8.3</div>
          <h3>LLM не приймає клінічні рішення</h3>
          <p>
            LLM-и допомагають лише з: boilerplate code, doc drafts,
            extraction з clinical documents (з human verification),
            translation з clinical review. <strong>Не</strong>: вибір
            режиму, генерація доз, інтерпретація biomarker для
            therapy selection.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C7</div>
          <h3>Без histology — без treatment Plan</h3>
          <p>
            Treatment Plan генерується тільки якщо <code>disease.id</code>
            або <code>icd_o_3_morphology</code> підтверджені. Інакше
            engine відмовляється і вмикає DiagnosticPlan mode (workup brief).
            <code>revise_plan</code> з treatment назад в diagnostic —
            <strong>заборонено</strong>, raises ValueError.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C5</div>
          <h3>Без time-critical recommendations</h3>
          <p>
            Engine не призначений для emergency oncology (oncologic
            emergencies, time-sensitive infusion reactions). Це б тригернуло
            device classification. Якщо Indication позначена
            <code>time_critical: true</code> — engine додає disqualification
            warning у FDA compliance.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §6.1</div>
          <h3>Two-reviewer merge для clinical content</h3>
          <p>
            Будь-яка зміна під <code>knowledge_base/hosted/content/</code>
            що affects clinical recommendations потребує два з трьох Clinical
            Co-Lead approvals. Без цього Indication залишається STUB.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C6</div>
          <h3>Anti automation-bias mandatory</h3>
          <p>
            Engine ніколи не показує тільки одну рекомендацію — завжди ≥2
            tracks side-by-side. Alternative не buried, не «click to expand»,
            не fine-print. Лікар бачить що це вибір, не директива.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §9.3</div>
          <h3>Patient data ніколи не у repo / public artifact</h3>
          <p>
            <code>patient_plans/</code> gitignored. Будь-які patient HTML —
            gitignored pattern. Site (<code>docs/</code>) показує тільки
            synthetic examples. Збір telemetry заборонений без explicit consent.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>4. Coverage limits (поточний стан KB)</h2>
      <p class="info-text">
        OpenOnco — work in progress. Зараз covered лише <strong>{n_diseases}
        захворювань</strong> (з ~100-150 у WHO-HAEM5 для лімфоїдних +
        ~50 солідних пухлин). Конкретно:
      </p>
      <table class="kv-table">
        <thead><tr><th>Категорія</th><th>Стан</th><th>Що це означає</th></tr></thead>
        <tbody>
          <tr><td>Хвороби з повним ланцюгом</td><td>{diseases_full} / {n_diseases}</td><td>Решта — частково модельовані; engine може видати warning «no Algorithm found for disease=X»</td></tr>
          <tr><td>Indications</td><td>{n_indications}</td><td>Тільки 1L (first-line). 2L+ режими ще не модельовані.</td></tr>
          <tr><td>RedFlags</td><td>{n_redflags}</td><td>Cover критичні clinical scenarios для існуючих хвороб; для нових диsease треба додавати</td></tr>
          <tr><td>Solid tumors</td><td>0</td><td>Engine generic-ready, але KB поки тільки гематологія</td></tr>
          <tr><td>Pediatric oncology</td><td>0</td><td>Out of scope for MVP — окремий track спеціалізації</td></tr>
          <tr><td>Радіотерапія планів</td><td>не модельовано</td><td>RT як Indication відсутня; має з'явитись як окрема сутність</td></tr>
          <tr><td>Хірургія планів</td><td>не модельовано</td><td>Surgical oncology indications відсутні</td></tr>
          <tr><td>Маркетингових даних доступу до режимів (НСЗУ formulary live)</td><td>статичний flag</td><td>Поки що hard-coded на режимах; не auto-refresh з НСЗУ — це окремий backlog item</td></tr>
        </tbody>
      </table>
      <div class="callout">
        <strong>Що НЕ означає STUB:</strong> structured data + algorithm logic
        + sources вже є. Що STUB означає: <strong>не пройшло dual sign-off
        Clinical Co-Lead</strong>. Тобто фактично ми маємо «proposed plan»
        який треба перевірити, не «approved plan».
      </div>
    </div>

    <div class="info-section">
      <h2>5. Що engine ніколи не робить</h2>
      <p class="info-text">
        Прозорий список заборонених patterns — щоб усі знали межі:
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не сховує alternative track</h3>
          <p>Обидві рекомендації завжди показані. UI не has «expand to see alternative» pattern.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не генерує нову Indication LLM-ом</h3>
          <p>Усе вибирається з уже-curated KB. Якщо немає підходящої Indication — engine emits warning, не «creative invention».</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не модифікує дози «під пацієнта»</h3>
          <p>Дози зі стандартного NCCN/ESMO. Adjustments тільки через explicit dose_modification_rules у Regimen YAML, ніяких ad hoc calculations.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не оцінює «що краще» між tracks</h3>
          <p>Algorithm обирає default, але не вирішує що default «кращий». Лікар має повну autonomy обрати alternative — це задокументовано у automation_bias_warning.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не інтерпретує imaging</h3>
          <p>«Bulky disease» приходить як structured field <code>dominant_nodal_mass_cm</code>, не з аналізу зображень. Image analysis = device classification.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не робить cohort matching</h3>
          <p>«У базі з N пацієнтів M% обрали X» — це окремий future feature, потребує persisted patient registry + privacy review. Поки що недоступне.</p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>6. Як з цим жити</h2>
      <p class="info-text">
        Цей engine задумано як <strong>підготовку до tumor-board</strong>,
        не заміну. Лікар вводить profile, отримує structured draft з усіма
        sources і open questions, а далі:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">1</div>
          <div class="num-lbl">Перевіряє sources</div>
          <p class="num-text">
            Кожна claim у плані має citation. Лікар може прочитати оригінальний
            NCCN/ESMO/МОЗ розділ і підтвердити що engine не misquote'ить.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">2</div>
          <div class="num-lbl">Заповнює Open Questions</div>
          <p class="num-text">
            Якщо engine emit'ить «cytogenetic panel incomplete» — лікар замовляє
            тест, додає у profile, запускає <code>revise_plan</code>. Plan
            оновлюється, OpenQuestion закривається.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">3</div>
          <div class="num-lbl">Адаптує під пацієнта</div>
          <p class="num-text">
            Дози пере-перевіряє, supportive care substitute'ить за алергіями,
            Ukraine-availability перевіряє вручну. Engine — draft, лікар — final.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">4</div>
          <div class="num-lbl">Tumor board discusses</div>
          <p class="num-text">
            MDT brief показує які ролі activated і які питання відкриті. Це
            structured agenda для board meeting. Decisions з board fixед'аться
            як provenance events.
          </p>
        </div>
      </div>
    </div>
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
    (output_dir / "capabilities.html").write_text(render_capabilities(stats), encoding="utf-8")
    (output_dir / "limitations.html").write_text(render_limitations(stats), encoding="utf-8")
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
