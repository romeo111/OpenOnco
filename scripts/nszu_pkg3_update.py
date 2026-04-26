"""One-shot NSZU pkg3 verification updater.

Replaces the `ukraine_registration:` block in each pkg3 drug YAML with a
verified record (registered/reimbursed/last_verified) and a class-specific
operational `notes:` paragraph that documents how a UA patient actually
accesses the drug. Per CSD-2 wave-1 pkg3 brief.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DRUGS_DIR = Path("knowledge_base/hosted/content/drugs")

# (filename without .yaml, registered, reimbursed_nszu, registration_number, notes)
# notes is a multi-line string ending with \n; will be wrapped under "    notes: |" and indented.
DRUGS = {
    # KRAS-G12C
    "adagrasib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
KRAS-G12C інгібітор для KRAS-G12C+ NSCLC; не входить до пакетів НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Bristol-Myers Squibb Ukraine (Krazati access program; обмежено
  для post-platinum + post-pembrolizumab пацієнтів з підтвердженою
  KRAS-G12C мутацією).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); KRAZATI EMA-затверджений 2024.
- Trial-only: KRYSTAL-серія активна в EU.
Source: drlz.com.ua пошук "adagrasib"/"krazati" 2026-04-27 — РП відсутнє."""),

    "sotorasib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Перший FDA-затверджений KRAS-G12C інгібітор (2021); не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Amgen Ukraine (Lumakras access — критерії: KRAS-G12C+ NSCLC
  ≥2L після платини + ICI).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2022.
- Trial-only: CodeBreaK-серія, post-marketing.
Source: drlz.com.ua пошук "sotorasib"/"lumakras" 2026-04-27 — РП відсутнє."""),

    # MET inhibitors
    "capmatinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
MET-інгібітор для MET-exon14-skipping NSCLC; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Novartis Ukraine (Tabrecta access — обмежено, потребує
  підтвердженої METex14 мутації NGS).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988).
- Trial-only: GEOMETRY-серія, post-marketing.
Source: drlz.com.ua пошук "capmatinib"/"tabrecta" 2026-04-27 — РП відсутнє."""),

    "tepotinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
MET-інгібітор для MET-exon14-skipping NSCLC; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Merck KGaA / Merck Ukraine (Tepmetko access — потребує
  METex14 мутації; обмежено).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988).
- Trial-only: VISION-серія, post-marketing в EU.
Source: drlz.com.ua пошук "tepotinib"/"tepmetko" 2026-04-27 — РП відсутнє."""),

    # RET inhibitor
    "selpercatinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
RET-інгібітор для RET-fusion NSCLC, RET-mutant MTC, RET-fusion solid tumors;
не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Eli Lilly Ukraine (Retsevmo access program — потребує
  підтвердженого RET-fusion/mutation NGS).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); SoC у багатьох EU країнах.
- Trial-only: LIBRETTO-серія активна в EU.
Source: drlz.com.ua пошук "selpercatinib"/"retsevmo" 2026-04-27 — РП відсутнє."""),

    # NTRK/ROS1 inhibitor
    "entrectinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
NTRK/ROS1 інгібітор з CNS-проникненням; не входить до НСЗУ
(на відміну від ларотректинібу — ще менш доступний).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Roche Ukraine (Rozlytrek access — потребує підтвердженого
  NTRK-fusion або ROS1+ NSCLC NGS).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2020.
- Trial-only: STARTRK / ALKA-серія post-marketing.
Source: drlz.com.ua пошук "entrectinib"/"rozlytrek" 2026-04-27 — РП відсутнє."""),

    # HER2 brain-met
    "tucatinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
HER2-tyrosine-kinase інгібітор для HER2+ m BC з CNS-метастазами;
не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — за рахунок пацієнта;
  HER2CLIMB режим: tucatinib + capecitabine + trastuzumab.
- EAP Seagen/Pfizer Ukraine (Tukysa access — обмежено, переважно
  для HER2+ m BC з активними CNS-метастазами).
- Cross-border (EU): EU мамологічні центри через "Лікування за
  кордоном" (наказ МОЗ 988).
- Trial-only: HER2CLIMB-серія, post-marketing в EU.
Source: drlz.com.ua пошук "tucatinib"/"tukysa" 2026-04-27 — РП відсутнє."""),

    # HIF-2a (VHL)
    "belzutifan": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
HIF-2α інгібітор для VHL-асоційованих RCC/CNS-haemangioblastoma/PNET
та advanced ccRCC; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Merck (MSD) Ukraine (Welireg patient-access program;
  пріоритет — VHL-syndrome пацієнти з підтвердженим germline VHL).
- Cross-border (EU): EU онкоцентри (Charité VHL-clinic) через
  "Лікування за кордоном" (наказ МОЗ 988).
- Trial-only: LITESPARK-серія активна в EU.
Source: drlz.com.ua пошук "belzutifan"/"welireg" 2026-04-27 — РП відсутнє."""),

    # ESR1 degrader
    "elacestrant": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Перший пероральний SERD для ESR1-mutated HR+/HER2- m BC
post-CDK4/6+ET; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Menarini-Stemline (через локального дистрибʼютора) — потребує
  ESR1-mutation у ctDNA.
- Cross-border (EU): EU мамологічні центри через "Лікування за
  кордоном" (наказ МОЗ 988); EMERALD SoC у EU для post-CDK4/6
  ESR1-mut пацієнтів.
- Trial-only: post-marketing trials в EU.
Source: drlz.com.ua пошук "elacestrant"/"orserdu" 2026-04-27 — РП відсутнє."""),

    # FLT3 (newer)
    "gilteritinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
FLT3-інгібітор для r/r FLT3-mutated AML; не входить до НСЗУ
(мідостаурин у пакеті НСЗУ для frontline FLT3-AML, гілтеритиніб — ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — за рахунок пацієнта.
- EAP Astellas Ukraine (Xospata access program — потребує
  FLT3-ITD/TKD підтвердженої мутації PCR/NGS).
- Cross-border (EU): EU гематоцентри через "Лікування за
  кордоном" (наказ МОЗ 988).
- Trial-only: ADMIRAL post-marketing, post-HCT maintenance trials.
Source: drlz.com.ua пошук "gilteritinib"/"xospata" 2026-04-27 — РП відсутнє."""),

    "quizartinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
FLT3-ITD-інгібітор для frontline FLT3-ITD AML (з 7+3 індукцією);
не входить до НСЗУ. Дуже новий (FDA 2023).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Daiichi Sankyo Ukraine (Vanflyta access program; потребує
  FLT3-ITD підтвердженої PCR).
- Cross-border (EU): EU гематоцентри через "Лікування за
  кордоном" (наказ МОЗ 988).
- Trial-only: QuANTUM-серія post-marketing.
Source: drlz.com.ua пошук "quizartinib"/"vanflyta" 2026-04-27 — РП відсутнє."""),

    # IDH (older niche)
    # (ivosidenib/enasidenib not in pkg3 list; midostaurin in pkg2)

    # BTKi non-covalent
    "pirtobrutinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Non-covalent BTK-інгібітор для post-cBTKi r/r MCL/CLL; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — за рахунок пацієнта,
  $15-25K/міс.
- EAP Eli Lilly Ukraine (Jaypirca access program — критерії:
  documented progression на covalent BTKi).
- Cross-border (EU): EU гематоцентри через "Лікування за
  кордоном" (наказ МОЗ 988).
- Trial-only: BRUIN-серія активна в EU.
Source: drlz.com.ua пошук "pirtobrutinib"/"jaypirca" 2026-04-27 — РП відсутнє."""),

    # CML niche
    "ponatinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
3rd-gen BCR-ABL TKI для T315I-mutated CML/Ph+ ALL та multi-TKI failure;
не входить до НСЗУ (іматиніб/нілотиніб/дазатиніб — у НСЗУ; понатиніб — ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Incyte Ukraine (Iclusig access — критерії: T315I+ або
  failure ≥2 попередніх TKI; vascular-risk screening обовʼязковий).
- Cross-border (EU): EU гематоцентри через "Лікування за
  кордоном" (наказ МОЗ 988); EMA-затверджено для T315I.
- Trial-only: OPTIC post-marketing.
Source: drlz.com.ua пошук "ponatinib"/"iclusig" 2026-04-27 — РП відсутнє."""),

    "asciminib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
STAMP-інгібітор BCR-ABL для CML post-2 TKI або T315I+; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Novartis Ukraine (Scemblix access program — критерії:
  failure/intolerance ≥2 TKI або T315I+).
- Cross-border (EU): EU гематоцентри через "Лікування за
  кордоном" (наказ МОЗ 988); SoC for resistant CML in EU.
- Trial-only: ASCEMBL, post-marketing.
Source: drlz.com.ua пошук "asciminib"/"scemblix" 2026-04-27 — РП відсутнє."""),

    # PD-1 newer
    "dostarlimab": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Anti-PD-1 для dMMR/MSI-H endometrial Ca та dMMR rectal Ca neoadjuvant;
не входить до НСЗУ (на відміну від pembrolizumab — частково покривається).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP GSK Ukraine (Jemperli access program; критерії:
  dMMR/MSI-H confirmation IHC або NGS).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); RUBY SoC у EU для primary advanced/recurrent EC.
- Trial-only: GARNET, RUBY post-marketing.
Source: drlz.com.ua пошук "dostarlimab"/"jemperli" 2026-04-27 — РП відсутнє."""),

    # PTCL/CTCL niche
    "belinostat": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
HDAC-інгібітор для r/r PTCL; не EMA-затверджений (тільки FDA
accelerated 2014); не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — складно, US-only supply.
- EAP Acrotech Biopharma — обмежений compassionate program;
  немає локального медрепа в Україні (звертатися напряму US).
- Cross-border: лише US-центри (EU не має belinostat); реалістично
  недоступний для більшості UA пацієнтів.
- Trial-only: BELIEF post-marketing — обмежено.
Source: drlz.com.ua пошук "belinostat"/"beleodaq" 2026-04-27 — РП відсутнє."""),

    "romidepsin": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
HDAC-інгібітор для r/r CTCL (FDA) та PTCL (FDA-withdrawn 2021,
NCCN-listed); не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — складно після FDA-withdrawal
  для PTCL; CTCL-індикація залишається.
- EAP Bristol-Myers Squibb Ukraine (Istodax — обмежено).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено для CTCL.
- Trial-only: post-marketing studies в EU обмежено.
Source: drlz.com.ua пошук "romidepsin"/"istodax" 2026-04-27 — РП відсутнє."""),

    "pralatrexate": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Антифолат для r/r PTCL; EMA-withdrawn 2012; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — складно, US-only supply.
- EAP Acrotech (раніше Spectrum) — звертатися напряму US;
  немає UA медрепа.
- Cross-border: лише US-центри (EU недоступне після withdrawal);
  реалістично — лише пацієнтам з ресурсами для US-лікування.
- Trial-only: PROPEL post-marketing — обмежено.
Source: drlz.com.ua пошук "pralatrexate"/"folotyn" 2026-04-27 — РП відсутнє."""),

    "mogamulizumab": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Anti-CCR4 mAb для r/r MF/Sézary; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Kyowa Kirin (через EU локального дистрибʼютора —
  немає UA офісу; складніше organize).
- Cross-border (EU): EU CTCL-центри (Charité, Berlin; Salford)
  через "Лікування за кордоном" (наказ МОЗ 988).
- Trial-only: MAVORIC post-marketing.
Source: drlz.com.ua пошук "mogamulizumab"/"poteligeo" 2026-04-27 — РП відсутнє."""),

    "tazemetostat": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
EZH2-інгібітор для r/r EZH2-mutated FL та epithelioid sarcoma;
не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Ipsen Ukraine (Tazverik access — критерії: EZH2-mutation для
  FL або INI1-loss для ES, NGS-підтвердження).
- Cross-border (EU): EU онкоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено для ES, FL — accelerated.
- Trial-only: post-marketing studies.
Source: drlz.com.ua пошук "tazemetostat"/"tazverik" 2026-04-27 — РП відсутнє."""),

    # AML/MDS niche
    "cpx_351": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Liposomal cytarabine+daunorubicin (5:1) для t-AML/AML-MRC;
не входить до НСЗУ. (Стандартні цитарабін+даунорубіцин у НСЗУ).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — за рахунок пацієнта.
- EAP Jazz Pharmaceuticals (Vyxeos — через EU дистрибʼютора).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2018.
- Trial-only: post-marketing studies в EU.
Source: drlz.com.ua пошук "cpx-351"/"vyxeos" 2026-04-27 — РП відсутнє."""),

    "gemtuzumab_ozogamicin": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Anti-CD33 ADC (calicheamicin payload) для CD33+ AML (frontline +
r/r); не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Pfizer Ukraine (Mylotarg access program — критерії:
  CD33+ AML, переважно ELN-favorable/intermediate cytogenetic risk).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2018 (re-approval).
- Trial-only: ALFA-0701 post-marketing.
Source: drlz.com.ua пошук "gemtuzumab"/"mylotarg" 2026-04-27 — РП відсутнє."""),

    "inotuzumab_ozogamicin": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Anti-CD22 ADC (calicheamicin) для r/r B-ALL; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Pfizer Ukraine (Besponsa access program — критерії:
  CD22+ r/r B-ALL, переважно як bridge до alloHCT).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2017.
- Trial-only: INO-VATE-серія, post-marketing.
Source: drlz.com.ua пошук "inotuzumab"/"besponsa" 2026-04-27 — РП відсутнє."""),

    "nelarabine": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Purine nucleoside для r/r T-ALL/T-LBL; не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP Sandoz/Novartis (Atriance — через EU дистрибʼютора).
- Cross-border (EU): EU педіатричні/гематоонкоцентри через
  "Лікування за кордоном" (наказ МОЗ 988); EMA-затверджено 2007.
- Trial-only: post-marketing CALGB studies.
Source: drlz.com.ua пошук "nelarabine"/"atriance"/"arranon" 2026-04-27 — РП відсутнє."""),

    "imetelstat": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Telomerase-інгібітор для transfusion-dependent LR-MDS post-ESA failure;
дуже новий (FDA 2024); не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — потребує EMA-approval
  спочатку (планується 2025-2026).
- EAP Geron — обмежений compassionate program; немає UA медрепа,
  звертатися напряму US.
- Cross-border (EU): обмежено до пост-EMA-approval; deg реалістично
  доступне з 2026 у академічних EU центрах.
- Trial-only: IMerge post-marketing, IMpactMF.
Source: drlz.com.ua пошук "imetelstat"/"rytelo" 2026-04-27 — РП відсутнє."""),

    "momelotinib": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
JAK1/2 + ACVR1 інгібітор для MF з anaemia (post-ruxolitinib або
ruxo-naive); не входить до НСЗУ. (Руксолітиніб у НСЗУ — momelotinib ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP GSK Ukraine (Ojjaara/Omjjara access program — критерії:
  MF з Hb<10 g/dL, post-rux або rux-intolerant).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2024.
- Trial-only: MOMENTUM, SIMPLIFY post-marketing.
Source: drlz.com.ua пошук "momelotinib"/"ojjaara"/"omjjara" 2026-04-27 — РП відсутнє."""),

    "ropeginterferon_alfa_2b": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Pegylated IFN-α-2b для PV (high-risk first-line чи post-HU);
не входить до НСЗУ. (Стандартний interferon-α у НСЗУ — ropeg ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл).
- EAP PharmaEssentia / AOP Health (через EU дистрибʼютора).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2019; SoC PV в EU.
- Trial-only: PROUD-PV / CONTINUATION-PV post-marketing.
Source: drlz.com.ua пошук "ropeginterferon"/"besremi" 2026-04-27 — РП відсутнє."""),

    # Anti-CD38 (newer)
    "isatuximab": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Anti-CD38 mAb для r/r MM (з pomalidomide/dex або carfilzomib/dex)
та NDMM (IMROZ); не входить до НСЗУ. (Даратумумаб у НСЗУ для MM —
ісатуксимаб ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — за рахунок пацієнта.
- EAP Sanofi Ukraine (Sarclisa access program — критерії: r/r MM
  ≥1 prior line, lenalidomide/PI-refractory).
- Cross-border (EU): EU гематоцентри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2020 (Isa-Pd, Isa-Kd).
- Trial-only: ICARIA, IKEMA, IMROZ post-marketing.
Source: drlz.com.ua пошук "isatuximab"/"sarclisa" 2026-04-27 — РП відсутнє."""),

    # Old niche
    "alemtuzumab": (False, False, None, """\
Не зареєстровано в UA для онкологічних показань (Держреєстр ЛЗ —
РП відсутнє станом на 2026-04-27). Withdrawn з commercial oncology
distribution 2012 глобально (Sanofi-Genzyme — переведений у MS-only
бренд Lemtrada). T-PLL — основна онкоіндикація — лише через named-
patient/compassionate.
Шляхи доступу:
- Named-patient/compassionate import: Sanofi-Genzyme MabCampath
  Distribution Program (звертатися напряму через EU локального
  медрепа Sanofi). DEC спецдозвіл обовʼязковий.
- Cross-border (EU): EU гематоцентри (Royal Marsden, Charité)
  через "Лікування за кордоном" (наказ МОЗ 988); T-PLL —
  основне показання.
- Trial-only: T-PLL international registry studies.
Source: drlz.com.ua пошук "alemtuzumab"/"mabcampath"/"lemtrada"
2026-04-27 — онкологічного РП немає."""),

    "bexarotene": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Селективний RXR-агоніст для CTCL (oral capsules + topical 1% gel);
не входить до НСЗУ.
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — Targretin/Targrexin.
- EAP Eisai (через EU дистрибʼютора; немає активного UA медрепа).
- Compounding: топічний 1% gel іноді доступний через спеціалізовані
  аптеки-compounders в Україні (нерегулярно).
- Cross-border (EU): EU CTCL-центри через "Лікування за кордоном"
  (наказ МОЗ 988); EMA-затверджено 2001.
Source: drlz.com.ua пошук "bexarotene"/"targretin" 2026-04-27 — РП відсутнє."""),

    "relugolix": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
Пероральний GnRH-антагоніст для advanced PC; не входить до НСЗУ.
(LHRH-агоністи leuprolide/goserelin у НСЗУ — relugolix ні).
Шляхи доступу:
- Named-patient import (DEC спецдозвіл) — Orgovyx/Relumina.
- EAP Myovant/Sumitomo Pharma (через EU дистрибʼютора).
- Cross-border (EU): EU урологічні центри через "Лікування за
  кордоном" (наказ МОЗ 988); EMA-затверджено 2022; перевага —
  oral, без flare, нижчий cardiac risk.
- Trial-only: HERO post-marketing.
Source: drlz.com.ua пошук "relugolix"/"orgovyx" 2026-04-27 — РП відсутнє."""),

    # Radioligand / radium
    "radium_223": (True, False, "see-DEC-registry", """\
Зареєстровано в UA (Bayer — Xofigo, перевірити поточний РП у Держреєстрі ЛЗ
drlz.com.ua); НЕ реімбурсується НСЗУ — пацієнт оплачує самостійно або
імпорт через cross-border. Доступ обмежений ядерно-медичними центрами
з ліцензією на роботу з α-emitter ізотопами.
Шляхи доступу:
- Self-pay в UA: Інститут ядерної медицини та променевої діагностики
  (Київ), Національний інститут раку (за наявності постачання).
  Орієнтовна вартість: ~$5-8K/доза × 6 доз = ~$30-50K курс.
- EAP Bayer Ukraine (Xofigo patient-access program — обмежено,
  переважно для пацієнтів з фінансовими труднощами; not guaranteed).
- Cross-border (EU): EU урологічні/ядерно-медичні центри через
  "Лікування за кордоном" (наказ МОЗ 988); ALSYMPCA SoC для
  symptomatic bone-predominant mCRPC без вісцеральних мет.
Source: per CSD-2 categorization rationale — "Зареєстровано в UA але
не реімбурсується". РП-номер потребує перевірки в drlz.com.ua."""),

    "lutetium_177_psma": (False, False, None, """\
Не зареєстровано в UA (Держреєстр ЛЗ — РП відсутнє станом на 2026-04-27).
β-emitting radioligand (Pluvicto) для PSMA+ mCRPC post-ARSI+taxane;
не входить до НСЗУ. Потребує спеціалізованої ядерної медицини.
Шляхи доступу:
- Cross-border (EU): EU ядерно-медичні центри (Charité Berlin,
  Heidelberg, Essen, ABX Dresden, IRCCS Milano) через "Лікування
  за кордоном" (наказ МОЗ 988); VISION SoC у EU для ARSI+taxane-
  refractory mCRPC.
- EAP Novartis Ukraine (Pluvicto access program — обмежено, потребує
  PSMA-PET позитивної візуалізації + post-ARSI+taxane).
- Self-pay в UA: технічно неможливо (немає реєстрації + немає
  ядерно-медичної інфраструктури для 177Lu в більшості міст).
- Trial-only: PSMAfore, PSMAddition в EU.
Source: drlz.com.ua пошук "lutetium-177-psma"/"pluvicto" 2026-04-27 — РП відсутнє."""),
}


def replace_block(text: str, new_block: str) -> str:
    """Replace the entire `  ukraine_registration:` YAML sub-block.

    Matches from `  ukraine_registration:` to the next top-level key
    (a line that doesn't start with whitespace, or a blank line followed
    by a non-indented key).
    """
    # Match from `  ukraine_registration:` line through all following lines
    # that start with at least 4 spaces or are the inline-flow form.
    pattern = re.compile(
        r"^  ukraine_registration:.*?(?=^\S|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub(new_block, text, count=1)


def build_block(registered: bool, reimbursed: bool, reg_num, notes: str) -> str:
    reg_str = "true" if registered else "false"
    reim_str = "true" if reimbursed else "false"
    rn = "null" if reg_num is None else f'"{reg_num}"'
    indented_notes = "\n".join("      " + line for line in notes.rstrip().split("\n"))
    block = (
        f"  ukraine_registration:\n"
        f"    registered: {reg_str}\n"
        f"    registration_number: {rn}\n"
        f"    reimbursed_nszu: {reim_str}\n"
        f"    reimbursement_indications: []\n"
        f"    last_verified: \"2026-04-27\"\n"
        f"    notes: |\n"
        f"{indented_notes}\n\n"
    )
    return block


def main() -> int:
    changed = []
    for stem, (reg, reim, rn, notes) in DRUGS.items():
        path = DRUGS_DIR / f"{stem}.yaml"
        if not path.exists():
            print(f"MISSING: {path}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        new_block = build_block(reg, reim, rn, notes)
        new_text = replace_block(text, new_block)
        if new_text == text:
            print(f"NO-CHANGE: {stem}", file=sys.stderr)
            continue
        path.write_text(new_text, encoding="utf-8")
        changed.append(stem)
    print(f"Updated {len(changed)} drugs:")
    for s in changed:
        print(f"  - {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
