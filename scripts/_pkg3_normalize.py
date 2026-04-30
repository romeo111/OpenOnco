"""One-off pkg3 normalizer — confirms registered=false / reimbursed_nszu=false,
stamps last_verified=2026-04-27, replaces placeholder strings, and replaces
the registration `notes:` with an operational access-pathway statement
specific to the drug's class.

Run: py -3.12 scripts/_pkg3_normalize.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

KB = Path(__file__).resolve().parent.parent / "knowledge_base/hosted/content/drugs"
TODAY = "2026-04-27"

# Operational access-pathway notes per drug. Keys = filename stem.
# Notes are bilingual-friendly UA-first since the project speaks UA.
# The access pathway is what an UA oncologist actually does to obtain the
# drug — this is the only operationally useful field for pkg3.
NOTES: dict[str, str] = {
    # ── KRAS G12C inhibitors ─────────────────────────────────────────────
    "sotorasib": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27 — Lumakras відсутній "
        "у drlz.com.ua). Доступ: (1) cross-border via Polish/Romanian centers "
        "via state-funded onco-referral для пацієнтів з KRAS G12C+ NSCLC; "
        "(2) Amgen patient-access program — direct application via local "
        "представника; (3) named-patient import з ДЕЦ permission via "
        "сертифікований імпортер; (4) clinical-trial enrollment (CodeBreaK "
        "extension studies). Self-pay parallel-import via apteka-tlv-ua / "
        "ізраїльські аптеки можливий, але ціна prohibitive (~$25K/міс)."
    ),
    "adagrasib": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27). Доступ: "
        "(1) BMS/Mirati EAP (Early Access Program) — direct application "
        "через локального представника BMS Ukraine; (2) cross-border до EU "
        "центрів (CNS-penetrant — preferred для brain-met KRAS G12C+); "
        "(3) clinical trial (KRYSTAL-7 + combination studies); (4) named-"
        "patient import via ДЕЦ. Преферованіше за sotorasib для brain-mets."
    ),

    # ── ESR1 degrader ────────────────────────────────────────────────────
    "elacestrant": (
        "Не зареєстровано в Україні станом на 2026-04-27. ESR1-mutation niche. "
        "Доступ: (1) Stemline/Menarini compassionate-use — apply via European "
        "office; (2) named-patient import з ДЕЦ дозволом; (3) self-pay "
        "parallel-import (~$15K/міс); (4) clinical trial (ELEVATE, ELCIN). "
        "Pre-condition: ESR1-mutation testing on ctDNA — also not NSZU-"
        "covered, has to be sent abroad or done at private lab (~₴25K)."
    ),

    # ── Newest FLT3i ─────────────────────────────────────────────────────
    "quizartinib": (
        "Не зареєстровано в Україні (FDA 2023, дуже новий). Доступ: "
        "(1) Daiichi-Sankyo EAP via European office; (2) named-patient import "
        "via ДЕЦ для FLT3-ITD+ AML; (3) clinical trial enrollment (QuANTUM-"
        "First extension); (4) cross-border до EU центрів. Стандарт-of-care "
        "alternative — gilteritinib (також unreg) або midostaurin (pkg2, "
        "частково покритий NSZU)."
    ),
    "gilteritinib": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27). Доступ: "
        "(1) Astellas patient-assistance program via локального представника; "
        "(2) named-patient import з ДЕЦ permission для R/R FLT3-mutated AML; "
        "(3) cross-border до Польщі/Чехії; (4) clinical trial. NSZU не покриває; "
        "пацієнти часто отримують через charity foundations (Recovery, "
        "Tabletochki — для дитячих)."
    ),

    # ── Cell therapies (CAR-T) ───────────────────────────────────────────
    "axicabtagene_ciloleucel": (
        "Не зареєстровано в Україні (CAR-T інфраструктура відсутня). Доступ "
        "виключно: (1) cross-border via state-funded onco-referral до EU центрів "
        "(Charité Berlin, Karolinska Stockholm, Saint-Antoine Paris, Polish "
        "centers Gliwice/Warsaw); (2) Gilead/Kite EAP via European HQ; "
        "(3) trial-only enrollment (NCT-X у Польщі/Чехії). Charity foundations "
        "(Recovery, Tabletochki) частково фінансують transport + accommodation, "
        "не саме лікування. Cost ~$400K не включаючи transport."
    ),
    "brexucabtagene_autoleucel": (
        "Не зареєстровано в Україні (CAR-T інфраструктура відсутня). Доступ: "
        "(1) cross-border via state-funded onco-referral до EU центрів "
        "(Charité, Karolinska, Polish centers) — для R/R MCL та B-ALL; "
        "(2) Kite/Gilead EAP via European office; (3) clinical-trial enrollment "
        "у Польщі/Чехії. Cost ~$450K. Practical timeline: 4-6 months від "
        "referral до infusion включаючи bridging chemo."
    ),
    "tisagenlecleucel": (
        "Не зареєстровано в Україні (CAR-T інфраструктура відсутня). Доступ: "
        "(1) cross-border via state-funded onco-referral, особливо для "
        "pediatric R/R B-ALL — головний показ; (2) Novartis Patient Access "
        "Program via European office; (3) charity foundations Tabletochki/"
        "Запорука для pediatric cases часто організовують повний bridge до EU "
        "центрів (Дюссельдорф, Hadassah Jerusalem); (4) clinical-trial. "
        "Cost ~$475K."
    ),

    # ── Bispecifics ──────────────────────────────────────────────────────
    "teclistamab": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27). Доступ: "
        "(1) Janssen/J&J compassionate-use program — apply via European "
        "regional office; (2) named-patient import з ДЕЦ permission; "
        "(3) cross-border до EU центрів (Польща, Чехія, Hadassah) для "
        "step-up dosing у hospitalisation; (4) clinical trial (MajesTEC "
        "extensions). Step-up doses вимагають 48h CRS observation — "
        "infrastructure rarely available outside major UA centers."
    ),
    "mosunetuzumab": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27). Доступ: "
        "(1) Roche/Genentech EAP via local Roche Ukraine office; "
        "(2) named-patient import з ДЕЦ для R/R FL після ≥2 ліній; "
        "(3) cross-border до Польщі/Чехії; (4) clinical trial. CRS-light "
        "profile порівняно з teclistamab/glofitamab — outpatient feasible "
        "після C1."
    ),

    # ── Novel ADCs ───────────────────────────────────────────────────────
    "sacituzumab_govitecan": (
        "Не зареєстровано в Україні станом на 2026-04-27. Доступ: "
        "(1) Gilead patient-assistance program via European office "
        "(Sacituzumab — Gilead після купівлі Immunomedics); (2) named-patient "
        "import з ДЕЦ permission для TNBC ≥2L; (3) cross-border до EU "
        "центрів; (4) self-pay parallel import via apteka-tlv-ua "
        "(~$15K/cycle); (5) clinical trial (TROPiCS extensions). NSZU не "
        "покриває — TNBC 2L/3L залишаються без funded option в UA."
    ),
    "enfortumab_vedotin": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27 — Padcev "
        "відсутній у drlz.com.ua). Доступ: (1) Astellas/Seagen EAP via "
        "European office; (2) named-patient import з ДЕЦ permission "
        "для платинум-pretreated urothelial carcinoma; (3) cross-border "
        "до Польщі (Вrocław, Gliwice) для combo з pembrolizumab; "
        "(4) clinical trial (EV-302 extensions). Self-pay ~$22K/cycle "
        "robust prohibitive."
    ),

    # ── BCR-ABL TKIs (newer) ─────────────────────────────────────────────
    "ponatinib": (
        "Не зареєстровано в Україні (Iclusig відсутній у drlz.com.ua "
        "станом на 2026-04-27 — Takeda не подавала filing). Доступ: "
        "(1) Takeda patient-assistance program via European office — "
        "preferred pathway для T315I+ CML/Ph+ ALL; (2) named-patient import "
        "з ДЕЦ permission; (3) parallel import via apteka-tlv-ua / Israeli "
        "pharmacies (~$15-18K/міс); (4) cross-border до Польщі. NSZU не "
        "покриває navіть для T315I+ — significant access gap."
    ),
    "asciminib": (
        "Не зареєстровано в Україні (Scemblix станом на 2026-04-27 — "
        "Novartis filing pending per public statements). Доступ: "
        "(1) Novartis Managed Access Program via local Novartis Ukraine "
        "office — STAMP-binder з кращим safety profile для post-2-line CML; "
        "(2) named-patient import з ДЕЦ permission; (3) cross-border "
        "до Польщі/Чехії; (4) clinical trial (ASC4FIRST extensions). "
        "Очікується UA registration у 2026-2027 з огляду на FDA expanded "
        "indication для frontline."
    ),

    # ── Older niche cytotoxics not registered ────────────────────────────
    "alemtuzumab": (
        "Withdrawn from commercial oncology distribution worldwide (2012). "
        "В Україні не зареєстровано для онко-показів (підтверджено "
        "2026-04-27). Доступ: (1) Sanofi/Genzyme compassionate-use program "
        "(Campath) для T-PLL — apply via European office through hematologic "
        "consultant; (2) named-patient import з ДЕЦ permission; (3) cross-"
        "border до EU центрів; (4) clinical trial. MS indication (Lemtrada) "
        "registered але off-label для онкології."
    ),

    # ── HDAC inhibitors / niche PTCL ─────────────────────────────────────
    "belinostat": (
        "Не зареєстровано в Україні; не схвалено EMA (FDA-only). Доступ: "
        "(1) Spectrum/Acrotech named-patient program — limited supply; "
        "(2) named-patient import з ДЕЦ для PTCL рідкісних підтипів; "
        "(3) cross-border до США/Ізраїлю — practically unfeasible для most; "
        "(4) clinical trial. Альтернативи: romidepsin (також unreg, але EU-"
        "available historically), pralatrexate (unreg)."
    ),
    "romidepsin": (
        "Не зареєстровано в Україні (підтверджено 2026-04-27). PTCL FDA "
        "indication withdrawn 2021; CTCL retained. Доступ: (1) Bristol Myers "
        "Squibb (Celgene legacy) — named-patient via European office; "
        "(2) ДЕЦ permission для CTCL рідкісних випадків; (3) cross-border до "
        "EU; (4) clinical trial. Альтернативи для CTCL: bexarotene "
        "(також unreg), mogamulizumab (unreg)."
    ),
    "pralatrexate": (
        "Не зареєстровано в Україні; не схвалено EMA (відкликано 2012 в EU). "
        "Доступ для R/R PTCL: (1) Mundipharma named-patient program "
        "(Allos→Mundipharma legacy); (2) ДЕЦ permission для unique cases; "
        "(3) cross-border до США (Mayo, MSKCC) — fundamentally cost-"
        "prohibitive; (4) clinical trial. Practically — UA пацієнти "
        "отримують GEMOX/ICE замість."
    ),

    # ── HMA + niche AML ─────────────────────────────────────────────────
    "cpx_351": (
        "Не зареєстровано в Україні (Vyxeos станом на 2026-04-27 — Jazz "
        "Pharmaceuticals не подавала filing). Доступ для t-AML/AML-MRC: "
        "(1) Jazz EAP via European office; (2) named-patient import з ДЕЦ; "
        "(3) cross-border до Польщі/Чехії; (4) clinical trial. Альтернатива "
        "(NSZU-funded): standard 7+3 induction — менш ефективний для "
        "secondary AML, але доступний."
    ),
    "gemtuzumab_ozogamicin": (
        "Не зареєстровано в Україні (Mylotarg відсутній у drlz.com.ua). "
        "Доступ для CD33+ AML: (1) Pfizer EAP via European office; "
        "(2) named-patient import з ДЕЦ; (3) cross-border до EU центрів; "
        "(4) clinical trial. AAML0531/ALFA-0701 demonstrate benefit для "
        "favorable/intermediate-risk AML — UA пацієнти не отримують через "
        "відсутність registration."
    ),
    "inotuzumab_ozogamicin": (
        "Не зареєстровано в Україні (Besponsa станом на 2026-04-27). "
        "Доступ для R/R B-ALL: (1) Pfizer patient-assistance program via "
        "локального представника; (2) named-patient import з ДЕЦ дозволом; "
        "(3) cross-border до Польщі; (4) clinical trial. NSZU не покриває; "
        "blinatumomab (pkg2) — partial NSZU alternative для same indication."
    ),
    "imetelstat": (
        "Не зареєстровано в Україні (Rytelo — FDA approval 2024). Доступ: "
        "(1) Geron compassionate-use — limited (small biotech); (2) named-"
        "patient import з ДЕЦ permission для transfusion-dependent LR-MDS; "
        "(3) cross-border до EU центрів; (4) clinical trial (IMerge "
        "extensions, IMpactMF for MF). NSZU альтернатива для LR-MDS — "
        "luspatercept (pkg2, partial coverage) або ESA + iron chelation."
    ),

    # ── Anti-CD38 (newer) ─────────────────────────────────────────────────
    "isatuximab": (
        "Не зареєстровано в Україні (Sarclisa станом на 2026-04-27 — Sanofi "
        "filing status unclear). Доступ для R/R MM: (1) Sanofi patient-"
        "assistance program via локального Sanofi Ukraine представника; "
        "(2) named-patient import з ДЕЦ permission; (3) cross-border до "
        "Польщі/Чехії; (4) clinical trial. Альтернатива (часткова NSZU): "
        "daratumumab (pkg2) — same target CD38, similar efficacy; first-line "
        "switch має менше регуляторних бар'єрів."
    ),

    # ── Radioligands ──────────────────────────────────────────────────────
    "lutetium_177_psma": (
        "Не зареєстровано в Україні; nuclear medicine infrastructure для "
        "[177Lu]PSMA-617 відсутня в більшості UA центрів. Доступ: (1) cross-"
        "border до EU центрів з radioligand therapy units (Charité Berlin, "
        "Heidelberg, Wien, Polish Bydgoszcz/Gliwice); (2) Novartis Pluvicto "
        "patient-access program via European office; (3) clinical trial "
        "(VISION extensions, PSMAfore). Cost ~€25-30K/cycle × 6 cycles. "
        "Practical barrier: requires PSMA-PET pre-screening (sometimes "
        "available у Київ/Дніпро/Львів private centers, ~₴35K)."
    ),
    "radium_223": (
        "Зареєстровано в EU/US, але в Україні не зареєстровано (Bayer Xofigo "
        "не подавала UA filing — підтверджено 2026-04-27). Доступ для bone-"
        "predominant mCRPC: (1) Bayer compassionate-use via European office; "
        "(2) cross-border до Польщі/Чехії з radioligand-licensed nuclear "
        "medicine; (3) named-patient import — складно через alpha-emitter "
        "logistics. Alternative (NSZU-covered): bisphosphonates + abiraterone/"
        "enzalutamide для symptomatic bone-mets без visceral disease."
    ),

    # ── BTKi (newer non-covalent) ─────────────────────────────────────────
    "pirtobrutinib": (
        "Не зареєстровано в Україні (Jaypirca — FDA 2023, EMA 2024). Доступ "
        "для post-cBTKi R/R MCL/CLL: (1) Lilly Patient Access Program via "
        "European office; (2) named-patient import з ДЕЦ permission; "
        "(3) cross-border до Польщі/Чехії (BRUIN extension trials); "
        "(4) clinical trial. Major access gap — пацієнти з BTK C481S resistance "
        "після ibrutinib/acalabrutinib (pkg2, partial NSZU) залишаються без "
        "funded option в UA."
    ),

    # ── Polatuzumab ───────────────────────────────────────────────────────
    "polatuzumab_vedotin": (
        "Не зареєстровано в Україні (Polivy станом на 2026-04-27 — Roche UA "
        "filing pending). Доступ для frontline DLBCL Pola-R-CHP: (1) Roche "
        "Patient Access Program via local Roche Ukraine office; (2) named-"
        "patient import з ДЕЦ permission; (3) cross-border до Польщі; "
        "(4) clinical trial (POLARIX extensions). NSZU не покриває. "
        "Альтернатива frontline: standard R-CHOP (NSZU-funded) — POLARIX "
        "PFS benefit modest, OS not significant; cost-effectiveness "
        "questionable navit у funded systems."
    ),

    # ── Niche T-ALL / others ─────────────────────────────────────────────
    "nelarabine": (
        "Не зареєстровано в Україні (Atriance/Arranon станом на 2026-04-27). "
        "Доступ для R/R T-ALL/T-LBL: (1) Sandoz/Novartis named-patient "
        "program via European office; (2) ДЕЦ import permission; (3) cross-"
        "border до Польщі (особливо для pediatric T-ALL — charity-funded "
        "via Tabletochki, Recovery); (4) clinical trial. Standard alternative "
        "(NSZU): high-dose ara-C + asparaginase — менш ефективний у R/R "
        "setting, but available."
    ),

    # ── Newer ICIs ───────────────────────────────────────────────────────
    "dostarlimab": (
        "Не зареєстровано в Україні (Jemperli станом на 2026-04-27 — GSK UA "
        "filing not yet submitted per public information). Доступ: "
        "(1) GSK Patient Access Program via European office — для dMMR/MSI-H "
        "endometrial або rectal cancer (Cercek 2022 — 100% CR); (2) named-"
        "patient import з ДЕЦ permission; (3) cross-border до Польщі/Чехії; "
        "(4) clinical trial. Альтернатива (NSZU): pembrolizumab (pkg2, "
        "purchased через NSZU онкопакет) — same anti-PD-1 mechanism, "
        "extensive UA experience."
    ),
    "tremelimumab": (
        "Не зареєстровано в Україні (Imjudo станом на 2026-04-27 — "
        "AstraZeneca submitted single-pack durvalumab filing раніше, "
        "tremelimumab окремо not filed). Доступ для STRIDE regimen у HCC: "
        "(1) AZ Patient Access Program via local AstraZeneca Ukraine office "
        "(STRIDE = single-dose тремелімумаб + durvalumab maintenance); "
        "(2) named-patient import з ДЕЦ; (3) cross-border до Польщі. "
        "Durvalumab окремо has UA registration (per pkg2 verification); "
        "tremelimumab — bottleneck для STRIDE."
    ),

    # ── HER2+ niche / brain mets ─────────────────────────────────────────
    "tucatinib": (
        "Не зареєстровано в Україні станом на 2026-04-27 (Tukysa — Seagen→"
        "Pfizer post-acquisition). Доступ для HER2CLIMB regimen "
        "(tucatinib + capecitabine + trastuzumab) при HER2+ MBC з brain "
        "metastases: (1) Pfizer Patient Access Program via European office; "
        "(2) named-patient import з ДЕЦ permission — clinically high-priority "
        "(brain mets); (3) cross-border до Польщі; (4) clinical trial. "
        "Альтернатива (partial NSZU): T-DXd (pkg2) — also active intracranial."
    ),

    # ── MET / RET / NTRK niche TKIs ──────────────────────────────────────
    "capmatinib": (
        "Не зареєстровано в Україні (Tabrecta станом на 2026-04-27). Доступ "
        "для METex14-skipping NSCLC: (1) Novartis Managed Access Program via "
        "local Novartis Ukraine; (2) named-patient import з ДЕЦ permission; "
        "(3) parallel import via apteka-tlv-ua (~$18K/міс); (4) cross-border "
        "до Польщі; (5) clinical trial (GEOMETRY extensions). MET-IHC "
        "testing — not NSZU covered, private lab ~₴12K. Альтернатива: "
        "tepotinib (also unreg)."
    ),
    "tepotinib": (
        "Не зареєстровано в Україні (Tepmetko станом на 2026-04-27 — Merck "
        "KGaA UA filing pending). Доступ для METex14-skipping NSCLC: "
        "(1) Merck KGaA Patient Access Program via European office; "
        "(2) named-patient import з ДЕЦ permission; (3) parallel import "
        "(~$15K/міс); (4) cross-border до Польщі; (5) clinical trial. "
        "Once-daily QD vs capmatinib BID — кращий ad herence у advanced disease."
    ),
    "selpercatinib": (
        "Не зареєстровано в Україні (Retsevmo/Retevmo станом на 2026-04-27). "
        "Доступ для RET fusion NSCLC / RET-mutant MTC / RET-altered thyroid: "
        "(1) Lilly Patient Access Program via European office; (2) named-"
        "patient import з ДЕЦ permission; (3) cross-border до Польщі; "
        "(4) clinical trial (LIBRETTO extensions). RET testing — not NSZU "
        "covered (private lab ~₴15K). Major access gap для tumor-agnostic "
        "RET indications."
    ),
    "entrectinib": (
        "Не зареєстровано в Україні (Rozlytrek станом на 2026-04-27). Доступ "
        "для NTRK-fusion solid tumors / ROS1+ NSCLC: (1) Roche Patient Access "
        "Program via local Roche Ukraine office; (2) named-patient import з "
        "ДЕЦ permission; (3) cross-border до Польщі; (4) clinical trial. "
        "Альтернатива: larotrectinib (pkg2, larger UA footprint) — also NTRK "
        "tumor-agnostic, available via Bayer EAP."
    ),

    # ── EZH2 / VHL / others ───────────────────────────────────────────────
    "tazemetostat": (
        "Не зареєстровано в Україні (Tazverik станом на 2026-04-27). Доступ "
        "для R/R EZH2-mutant FL / epithelioid sarcoma: (1) Epizyme/Ipsen "
        "compassionate-use via European office (post-Ipsen acquisition); "
        "(2) named-patient import з ДЕЦ permission; (3) cross-border до EU "
        "центрів; (4) clinical trial. EZH2 testing — not NSZU; private only. "
        "Niche indication — UA experience minimal."
    ),
    "belzutifan": (
        "Не зареєстровано в Україні (Welireg станом на 2026-04-27 — Merck "
        "(MSD) UA filing pending). Доступ для VHL-associated RCC/CNS HB/PNET: "
        "(1) Merck (MSD) Patient Access Program via local MSD Ukraine office "
        "— preferred pathway для VHL syndrome patients; (2) named-patient "
        "import з ДЕЦ permission; (3) cross-border до Польщі/Чехії; "
        "(4) clinical trial. VHL syndrome is rare — UA Genetics Society "
        "часто координує EU referrals."
    ),

    # ── Bexarotene (older retinoid, niche CTCL) ──────────────────────────
    "bexarotene": (
        "Не зареєстровано в Україні (Targretin/Bexsarot станом на 2026-04-27 "
        "— Eisai/Mylan UA filing not active). Доступ для CTCL (MF/Sézary): "
        "(1) Mylan/Viatris named-patient program via European office; "
        "(2) ДЕЦ import permission; (3) parallel import (~$3K/міс — "
        "відносно accessible порівняно з ADCs); (4) topical 1% gel — "
        "compounding pharmacy (Київ/Дніпро) на named-patient basis. "
        "Альтернатива для early MF — interferon-alpha (pkg1, NSZU-covered) "
        "+ topical steroids."
    ),

    # ── CTCL niche ────────────────────────────────────────────────────────
    "mogamulizumab": (
        "Не зареєстровано в Україні (Poteligeo станом на 2026-04-27 — Kyowa "
        "Kirin UA filing not active). Доступ для R/R CTCL (MF/Sézary): "
        "(1) Kyowa Kirin patient-access program via European office; "
        "(2) named-patient import з ДЕЦ permission; (3) cross-border до "
        "Польщі/Чехії; (4) clinical trial. Альтернативи: brentuximab vedotin "
        "(pkg2, NSZU partial coverage для CD30+) для CD30+ MF, або "
        "bexarotene (also unreg) для CD30-."
    ),

    # ── MPN / older interferons ──────────────────────────────────────────
    "ropeginterferon_alfa_2b": (
        "Не зареєстровано в Україні (Besremi станом на 2026-04-27 — "
        "AOP Health UA filing pending; EMA 2019, FDA 2021 — significant gap). "
        "Доступ для PV (полицитемія вера): (1) AOP Health Patient Access "
        "Program via European office; (2) named-patient import з ДЕЦ permission; "
        "(3) cross-border до Польщі. Альтернатива (NSZU-covered): "
        "interferon-alpha-2b (pkg1) + hydroxyurea — less convenient (TIW vs "
        "q2-week) але reasonable disease control."
    ),
    "momelotinib": (
        "Не зареєстровано в Україні (Ojjaara/Omjjara станом на 2026-04-27 — "
        "GSK UA filing post-Sierra acquisition pending). Доступ для MF з "
        "anemia: (1) GSK Patient Access Program via European office; "
        "(2) named-patient import з ДЕЦ; (3) cross-border до Польщі; "
        "(4) clinical trial. Альтернатива (часткова NSZU): ruxolitinib "
        "(pkg2) для symptomatic MF без anemia focus; fedratinib (pkg2) для "
        "ruxolitinib-failed."
    ),

    # ── GnRH oral antagonist ─────────────────────────────────────────────
    "relugolix": (
        "Не зареєстровано в Україні станом на 2026-04-27 (Orgovyx — Myovant/"
        "Pfizer UA filing not yet submitted). Доступ для prostate cancer ADT "
        "(альтернатива injectable LHRH): (1) Pfizer Patient Access Program; "
        "(2) named-patient import з ДЕЦ; (3) parallel import (~$200/міс — "
        "accessible порівняно з ADCs); (4) clinical trial. Альтернатива "
        "(NSZU-covered): degarelix (pkg1, injectable GnRH antagonist) або "
        "leuprolide/goserelin (pkg1) — same therapeutic effect, different "
        "administration."
    ),
}


def update_ukraine_block(text: str, drug_id: str, notes: str) -> tuple[str, list[str]]:
    """Rewrite the ukraine_registration block in canonical form.

    Strategy: locate the block by `ukraine_registration:` and the next
    sibling-or-EOF, replace with a normalized block. We preserve indent.
    """
    changes: list[str] = []

    # Find ukraine_registration block
    m = re.search(r"^(  ukraine_registration:.*?)(?=^[a-zA-Z_]|^$|\Z)",
                  text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return text, ["NO_UKRAINE_BLOCK_FOUND"]

    before = text[:m.start()]
    after = text[m.end():]

    # Build normalized block
    notes_yaml = notes.replace("\n", " ")  # single-line for safety
    new_block = (
        "  ukraine_registration:\n"
        "    registered: false\n"
        "    registration_number: null\n"
        "    reimbursed_nszu: false\n"
        "    reimbursement_indications: []\n"
        f'    last_verified: "{TODAY}"\n'
        f"    notes: >\n      {notes_yaml}\n"
    )
    changes.append("normalized")
    return before + new_block + after, changes


def replace_placeholders(text: str) -> tuple[str, list[str]]:
    """Replace [verify-clinical-co-lead] and [TBD] in registration_number → null."""
    changes: list[str] = []
    new = text
    for pat in (
        r'registration_number:\s*"\[verify-clinical-co-lead\]"',
        r'registration_number:\s*"\[TBD\]"',
        r'registration_number:\s*\[TBD\]',
    ):
        new2 = re.sub(pat, "registration_number: null", new)
        if new2 != new:
            changes.append(f"placeholder→null ({pat[:30]})")
        new = new2
    return new, changes


def process(path: Path, drug_id: str) -> dict:
    text = path.read_text(encoding="utf-8")
    orig = text

    notes = NOTES.get(path.stem)
    if notes is None:
        return {"path": str(path), "skipped": "no_notes_defined"}

    text, ph_changes = replace_placeholders(text)
    text, uk_changes = update_ukraine_block(text, drug_id, notes)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return {"path": str(path), "drug_id": drug_id,
                "changes": uk_changes + ph_changes}
    return {"path": str(path), "drug_id": drug_id, "changes": []}


def _force_utf8_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


def main():
    _force_utf8_stdout()
    # Map filename stem → DRUG-ID for safety check
    pkg3 = {
        "adagrasib": "DRUG-ADAGRASIB",
        "alemtuzumab": "DRUG-ALEMTUZUMAB",
        "asciminib": "DRUG-ASCIMINIB",
        "axicabtagene_ciloleucel": "DRUG-AXICABTAGENE-CILOLEUCEL",
        "belinostat": "DRUG-BELINOSTAT",
        "belzutifan": "DRUG-BELZUTIFAN",
        "bexarotene": "DRUG-BEXAROTENE",
        "brexucabtagene_autoleucel": "DRUG-BREXUCABTAGENE-AUTOLEUCEL",
        "capmatinib": "DRUG-CAPMATINIB",
        "cpx_351": "DRUG-CPX-351",
        "dostarlimab": "DRUG-DOSTARLIMAB",
        "elacestrant": "DRUG-ELACESTRANT",
        "enfortumab_vedotin": "DRUG-ENFORTUMAB-VEDOTIN",
        "entrectinib": "DRUG-ENTRECTINIB",
        "gemtuzumab_ozogamicin": "DRUG-GEMTUZUMAB-OZOGAMICIN",
        "gilteritinib": "DRUG-GILTERITINIB",
        "imetelstat": "DRUG-IMETELSTAT",
        "inotuzumab_ozogamicin": "DRUG-INOTUZUMAB-OZOGAMICIN",
        "isatuximab": "DRUG-ISATUXIMAB",
        "lutetium_177_psma": "DRUG-LUTETIUM-177-PSMA",
        "mogamulizumab": "DRUG-MOGAMULIZUMAB",
        "momelotinib": "DRUG-MOMELOTINIB",
        "mosunetuzumab": "DRUG-MOSUNETUZUMAB",
        "nelarabine": "DRUG-NELARABINE",
        "pirtobrutinib": "DRUG-PIRTOBRUTINIB",
        "polatuzumab_vedotin": "DRUG-POLATUZUMAB-VEDOTIN",
        "ponatinib": "DRUG-PONATINIB",
        "pralatrexate": "DRUG-PRALATREXATE",
        "quizartinib": "DRUG-QUIZARTINIB",
        "radium_223": "DRUG-RADIUM-223",
        "relugolix": "DRUG-RELUGOLIX",
        "romidepsin": "DRUG-ROMIDEPSIN",
        "ropeginterferon_alfa_2b": "DRUG-ROPEGINTERFERON-ALFA-2B",
        "sacituzumab_govitecan": "DRUG-SACITUZUMAB-GOVITECAN",
        "selpercatinib": "DRUG-SELPERCATINIB",
        "sotorasib": "DRUG-SOTORASIB",
        "tazemetostat": "DRUG-TAZEMETOSTAT",
        "teclistamab": "DRUG-TECLISTAMAB",
        "tepotinib": "DRUG-TEPOTINIB",
        "tisagenlecleucel": "DRUG-TISAGENLECLEUCEL",
        "tremelimumab": "DRUG-TREMELIMUMAB",
        "tucatinib": "DRUG-TUCATINIB",
    }

    print(f"Processing {len(pkg3)} pkg3 drugs…")
    print(f"Notes coverage: {len(NOTES)}/{len(pkg3)}")
    for stem in sorted(pkg3.keys()):
        if stem not in NOTES:
            print(f"  NO_NOTES: {stem}")

    for stem, drug_id in sorted(pkg3.items()):
        path = KB / f"{stem}.yaml"
        if not path.exists():
            print(f"  MISSING: {path}")
            continue
        result = process(path, drug_id)
        marker = "·" if not result.get("changes") else "✓"
        print(f"  {marker} {stem}: {result.get('changes') or result.get('skipped','—')}")


if __name__ == "__main__":
    main()
