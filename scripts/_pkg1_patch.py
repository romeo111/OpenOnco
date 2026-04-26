"""Targeted ukraine_registration block rewriter for pkg1 drugs that the
prior indications-insertion script broke (it confused block boundaries
where the original had a multi-line `>` `typical_dosing:` /
`formulations:` block immediately after `ukraine_registration:`).

This script:
  1. Reads each pkg1 YAML.
  2. Locates the `  ukraine_registration:` line by 2-space indent.
  3. Finds the block end (next line with indent <= 2 that starts with
     a key character, ignoring blank lines).
  4. Replaces the entire block with a freshly-constructed one using:
       - registered: <preserved or default true>
       - registration_number: <preserved or null>
       - reimbursed_nszu: <preserved or default true>
       - reimbursement_indications: <new list, replacing existing>
       - last_verified: "2026-04-27"
       - notes: <preserved or override>

For stems already not in the indications dict, leaves indications as-is
(uses existing list if any). This is idempotent and structure-safe.

Run: py -3.12 scripts/_pkg1_patch.py
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DRUGS_DIR = REPO / "knowledge_base" / "hosted" / "content" / "drugs"

# Indications by stem — comprehensive pkg1 set.
INDICATIONS: dict[str, list[str]] = {
    # Cytotoxics
    "fluorouracil": [
        "Колоректальний рак (ад'ювантна + метастатична терапія, FOLFOX/FOLFIRI/FOLFIRINOX)",
        "Рак шлунка / стравохідно-шлункового з'єднання (FLOT)",
        "Рак підшлункової залози (FOLFIRINOX)",
        "Плоскоклітинний рак голови та шиї",
    ],
    "bendamustine": [
        "Хронічний лімфоцитарний лейкоз (1L у фіт-пацієнтів без TP53 — BR)",
        "Індолентні B-клітинні лімфоми (FL, MZL, MCL — BR / R-Bendamustine)",
    ],
    "carboplatin": [
        "Рак яєчників (1L з паклітакселом)",
        "Недрібноклітинний рак легень (1L платина-дублети)",
        "Рак сечового міхура / уротеліальний (cisplatin-ineligible)",
        "Лімфоми (R-ICE, R-DHAP — рятівні схеми)",
    ],
    "cisplatin": [
        "Гермінативно-клітинні пухлини (BEP)",
        "Недрібноклітинний рак легень (1L платина-дублети)",
        "Плоскоклітинний рак голови та шиї (CRT)",
        "Рак сечового міхура / уротеліальний (MVAC, gemcitabine-cisplatin)",
        "Рак шийки матки / стравоходу (CRT)",
    ],
    "cyclophosphamide": [
        "Лімфоми (R-CHOP, BEACOPP, R-CVP)",
        "Рак молочної залози (AC/EC/TAC ад'ювантна)",
        "Гострий лімфобластний лейкоз (Hyper-CVAD)",
        "Множинна мієлома (VCD, KCd)",
        "Кондиціонування перед ало-/авто-ТКМ (Cy-TBI, FluCy)",
    ],
    "docetaxel": [
        "Рак молочної залози (TC, TAC ад'ювантна, метастатична)",
        "Кастраційно-резистентний рак передміхурової залози (доцетаксел стандарт)",
        "Метастатичний гормон-чутливий рак передміхурової залози (CHAARTED)",
        "Недрібноклітинний рак легень (2L)",
        "Рак шлунка (FLOT)",
    ],
    "etoposide": [
        "Дрібноклітинний рак легень (EP, EC ± atezolizumab/durvalumab)",
        "Гермінативно-клітинні пухлини (BEP)",
        "Лімфоми (R-EPOCH, R-ICE, BEACOPP)",
        "Гострий мієлоїдний лейкоз (FLAG-Ida — окремі схеми)",
    ],
    "gemcitabine": [
        "Рак підшлункової залози (gemcitabine-monotherapy, gem-nab-paclitaxel)",
        "Недрібноклітинний рак легень (gem-cisplatin, gem-carboplatin)",
        "Рак сечового міхура / уротеліальний (gem-cisplatin, gem-carboplatin)",
        "Рак яєчників (рецидив)",
        "Рак молочної залози (метастатична)",
        "Лімфоми (GDP, R-GemOx — рятівні схеми)",
    ],
    "ifosfamide": [
        "Саркоми м'яких тканин (AIM, MAID)",
        "Гермінативно-клітинні пухлини (VeIP, TIP — рятівні)",
        "Лімфоми (ICE, R-ICE — рятівні)",
        "Рак шийки матки (paclitaxel-ifosfamide-cisplatin)",
    ],
    "irinotecan": [
        "Колоректальний рак (FOLFIRI, FOLFIRINOX)",
        "Рак шлунка / стравохідно-шлункового з'єднання",
        "Дрібноклітинний рак легень (IP — окремі схеми)",
    ],
    "l_asparaginase": [
        "Гострий лімфобластний лейкоз (педіатричні + AYA схеми)",
        "Лімфобластна лімфома",
    ],
    "methotrexate": [
        "Гострий лімфобластний лейкоз (HD-MTX системно + ІТ профілактика ЦНС)",
        "Первинна лімфома ЦНС (R-MPV / HD-MTX-based)",
        "Лімфоми (R-CODOX-M/IVAC; ІТ профілактика для high-risk DLBCL)",
        "Рак молочної залози (CMF — історично)",
        "Гестаційна трофобластна хвороба",
    ],
    "nab_paclitaxel": [
        "Метастатичний рак молочної залози (моно)",
        "Метастатичний рак підшлункової залози (gem-nab-paclitaxel)",
    ],
    "oxaliplatin": [
        "Колоректальний рак (FOLFOX, CAPOX, FOLFIRINOX — ад'ювантна + метастатична)",
        "Рак шлунка / стравохідно-шлункового з'єднання (FLOT)",
        "Рак підшлункової залози (FOLFIRINOX)",
        "Лімфоми (R-GemOx — окремі рятівні схеми)",
    ],
    "paclitaxel": [
        "Рак яєчників (1L paclitaxel-carboplatin)",
        "Рак молочної залози (паклітаксел еженедельний — ад'ювантна, метастатична)",
        "Недрібноклітинний рак легень",
        "Рак стравоходу / шлунка",
    ],
    "thiotepa": [
        "Кондиціонування перед ало-/авто-ТКМ (TBC, BuCyTT, CFT-MAC)",
        "Первинна лімфома ЦНС (high-dose з ритуксимабом перед ТКМ)",
        "Рак молочної залози / яєчників (high-dose режими — історично)",
    ],
    "zidovudine": [
        "Адультна Т-клітинна лейкемія/лімфома (ATLL — у комбінації з інтерфероном α)",
    ],
    # Hormonals
    "abiraterone": [
        "Метастатичний кастраційно-резистентний рак передміхурової залози (mCRPC)",
        "Метастатичний гормон-чутливий рак передміхурової залози високого ризику (mHSPC, LATITUDE/STAMPEDE)",
    ],
    "anastrozole": [
        "Гормон-чутливий рак молочної залози (ад'ювантна терапія, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
    ],
    "enzalutamide": [
        "Метастатичний кастраційно-резистентний рак передміхурової залози (mCRPC)",
        "Метастатичний гормон-чутливий рак передміхурової залози (mHSPC)",
        "Неметастатичний кастраційно-резистентний рак передміхурової залози (nmCRPC)",
    ],
    "exemestane": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози (після нестероїдного АІ)",
    ],
    "fulvestrant": [
        "Метастатичний HR+/HER2- рак молочної залози (моно- або у комбінації з CDK4/6i / alpelisib)",
    ],
    "letrozole": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
    ],
    "tamoxifen": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, пременопауза/постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
        "Профілактика рецидиву DCIS",
    ],
    "leuprolide": [
        "Рак передміхурової залози (АДТ)",
        "Гормон-чутливий рак молочної залози (пременопауза, у комбінації з АІ)",
    ],
    "goserelin": [
        "Рак передміхурової залози (АДТ, моно- або у комбінації)",
        "Гормон-чутливий рак молочної залози (пременопауза, овариальна супресія)",
    ],
    # Cytotoxics with detailed indications already in earlier dict
    "bleomycin": [
        "Лімфома Ходжкіна (ABVD)",
        "Гермінативно-клітинні пухлини (BEP)",
    ],
    "capecitabine": [
        "Колоректальний рак (ад'ювантна, метастатична)",
        "Рак шлунка / стравохідно-шлункового з'єднання",
        "Рак молочної залози (метастатична, у комбінації)",
    ],
    "capecitabine_breast": [
        "Метастатичний рак молочної залози (моно- або у комбінації, у т.ч. HER2CLIMB / трастузумаб)",
        "Залишкова інвазія TNBC після неоад'ювантної терапії (CREATE-X)",
    ],
    "cladribine": [
        "Волосистоклітинний лейкоз (1L)",
        "Лангергансово-клітинний гістіоцитоз",
    ],
    "cytarabine": [
        "Гострий мієлоїдний лейкоз (індукція 7+3, консолідація HiDAC)",
        "Гострий лімфобластний лейкоз (інтратекальна профілактика ЦНС)",
        "Лімфоми (R-DHAP, R-ESHAP — рятівні схеми)",
    ],
    "dacarbazine": [
        "Лімфома Ходжкіна (ABVD)",
        "Метастатична меланома (моно- або у комбінації)",
        "Саркоми м'яких тканин",
    ],
    "daunorubicin": [
        "Гострий мієлоїдний лейкоз (7+3 індукція)",
        "Гострий промієлоцитарний лейкоз (AIDA, з ATRA/ATO)",
        "Гострий лімфобластний лейкоз (індукція)",
    ],
    "doxorubicin": [
        "Лімфома Ходжкіна (ABVD)",
        "Дифузна великоклітинна B-клітинна лімфома (R-CHOP)",
        "Рак молочної залози (AC/EC ад'ювантна)",
        "Саркоми м'яких тканин",
    ],
    "fludarabine": [
        "Хронічний лімфоцитарний лейкоз (FCR — у відібраних випадках без TP53/del17p)",
        "Кондиціонування перед CAR-T / ало-ТКМ (флударабін + циклофосфамід / мелфалан)",
        "Низькоступеневі лімфоми (рятівні схеми)",
    ],
    "hydroxyurea": [
        "Хронічна мієлоїдна лейкемія (циторедукція до старту ТКІ)",
        "Справжня поліцитемія / есенціальна тромбоцитемія високого ризику",
        "Гострі лейкози (циторедукція при гіперлейкоцитозі)",
    ],
    "idarubicin": [
        "Гострий мієлоїдний лейкоз (7+3 індукція)",
        "Гострий промієлоцитарний лейкоз (AIDA)",
    ],
    "leucovorin": [
        "Колоректальний рак (FOLFOX, FOLFIRI — модулятор 5-ФУ)",
        "Рятувальна терапія після високих доз метотрексату",
    ],
    "mercaptopurine": [
        "Гострий лімфобластний лейкоз (підтримка)",
    ],
    "pemetrexed": [
        "Неплоскоклітинний недрібноклітинний рак легень (1L + підтримка)",
        "Злоякісна плевральна мезотеліома",
    ],
    "pertuzumab": [
        "HER2+ рак молочної залози (неоад'ювантна, ад'ювантна, метастатична — у комбінації з трастузумабом)",
    ],
    "prednisone": [
        "Лімфоми (R-CHOP, BEACOPP, CVP)",
        "Гострі лейкози (індукція ALL)",
        "Множинна мієлома (VMP, VRd, Rd — у комбінації)",
    ],
    "temozolomide": [
        "Гліобластома (Stupp — конкомітантно з променевою терапією та ад'ювантно)",
        "Анапластична астроцитома / олігодендрогліома",
    ],
    "vinblastine": [
        "Лімфома Ходжкіна (ABVD)",
        "Гермінативно-клітинні пухлини",
    ],
    "vincristine": [
        "Лімфоми (R-CHOP, BEACOPP, EPOCH)",
        "Гострий лімфобластний лейкоз (індукція + підтримка)",
        "Множинна мієлома (VAD — історично)",
    ],
    # CML / TKI
    "imatinib": [
        "Хронічна мієлоїдна лейкемія (1L хронічна фаза, прискорена/бластна фаза)",
        "Ph+ гострий лімфобластний лейкоз (у комбінації з хіміотерапією)",
        "Гастроінтестинальна стромальна пухлина (GIST — KIT/PDGFRA-чутливі)",
    ],
    "dasatinib": [
        "Хронічна мієлоїдна лейкемія (1L хронічна фаза, прискорена/бластна фаза)",
        "Ph+ гострий лімфобластний лейкоз (у комбінації з хіміотерапією)",
    ],
    "nilotinib": [
        "Хронічна мієлоїдна лейкемія (1L хронічна фаза, 2L після іматинібу)",
    ],
    # Bone-targeted
    "denosumab": [
        "Профілактика скелетних подій при метастазах у кістки (Xgeva)",
        "Гігантоклітинна пухлина кістки (нерезектабельна / рецидивна)",
    ],
    "zoledronate": [
        "Профілактика скелетних подій при метастазах у кістки (солідні пухлини)",
        "Множинна мієлома (профілактика остеолітичних подій)",
        "Гіперкальциємія злоякісного ґенезу",
    ],
    # ATRA / ATO
    "atra": [
        "Гострий промієлоцитарний лейкоз (APL — індукція + консолідація з ATO ± хіміотерапією)",
    ],
    "arsenic_trioxide": [
        "Гострий промієлоцитарний лейкоз (APL — індукція + консолідація з ATRA)",
    ],
    # Biologics
    "rituximab": [
        "Дифузна великоклітинна B-клітинна лімфома (R-CHOP)",
        "Фолікулярна лімфома (R-CHOP / R-Bendamustine; підтримка R)",
        "Лімфома маргінальної зони (НСЗУ перелік)",
        "Хронічний лімфоцитарний лейкоз (R-FC у відібраних)",
        "Мантійноклітинна лімфома",
    ],
    "trastuzumab": [
        "HER2+ рак молочної залози (неоад'ювантна, ад'ювантна, метастатична — TCHP, AC-TH тощо)",
        "HER2+ рак шлунка / стравохідно-шлункового з'єднання (метастатична)",
    ],
    "bevacizumab": [
        "Метастатичний колоректальний рак (FOLFOX/FOLFIRI + bev)",
        "Гліобластома (рецидив)",
        "Метастатичний рак яєчників (у комбінації)",
        "Недрібноклітинний рак легень (неплоскоклітинний — у комбінації)",
    ],
    "cetuximab": [
        "Метастатичний колоректальний рак (RAS-WT, лівобічний — у комбінації з FOLFOX/FOLFIRI)",
        "Плоскоклітинний рак голови та шиї (з RT або платинівмісною ХТ)",
    ],
    # Supportive
    "acyclovir": [
        "Профілактика реактивації HSV/VZV при імуносупресивній терапії (інгібітори протеасоми, флударабін, ало-ТКМ)",
        "Лікування активних HSV/VZV інфекцій",
    ],
    "allopurinol": [
        "Профілактика синдрому лізису пухлини",
        "Гіперурикемія",
    ],
    "dexamethasone": [
        "Антиеметична профілактика при високоемоегенній хіміотерапії",
        "Множинна мієлома (VRd, VCD, Rd, KRd — компонент)",
        "Лімфоми (R-CHOP, BEACOPP, R-DHAP)",
        "Симптоматичне лікування пухлинного набряку (ЦНС, спинальної компресії)",
    ],
    "epoetin_alfa": [
        "Анемія у пацієнтів з хіміотерапіями (у відповідних показаннях)",
        "Анемія при мієлодиспластичних синдромах низького ризику",
    ],
    "filgrastim": [
        "Профілактика та лікування фебрильної нейтропенії (Г-КСФ підтримка)",
        "Мобілізація гемопоетичних стовбурових клітин для авто-/ало-ТКМ",
    ],
    "ondansetron": [
        "Антиеметична профілактика при хіміотерапії (5-HT3 антагоніст)",
    ],
    "trimethoprim_sulfamethoxazole": [
        "Профілактика Pneumocystis jirovecii (PJP) у пацієнтів з імуносупресією (флударабін, ритуксимаб, тривала кортикостероїдна терапія)",
    ],
    "entecavir": [
        "Профілактика реактивації HBV у HBsAg+ / anti-HBc+ пацієнтів на анти-CD20 терапії (ритуксимаб, обінутузумаб)",
    ],
    "glecaprevir_pibrentasvir": [
        "Лікування HCV-інфекції до/під час імуносупресивної терапії (особливо HCV-MZL — досягнення SVR як перша лінія)",
    ],
    "sofosbuvir_velpatasvir": [
        "Лікування HCV-інфекції до/під час імуносупресивної терапії (HCV-MZL — пангенотиповий режим)",
    ],
    "interferon_alpha": [
        "Хронічні мієлопроліферативні новоутвори (PV / ET — циторедукція високого ризику, у відібраних випадках)",
        "Хронічний мієлоїдний лейкоз (історично, до ери ТКІ)",
        "Адультна Т-клітинна лейкемія/лімфома (ATLL — у комбінації з зидовудином)",
    ],
}

# Drugs that should be reimbursed_nszu=false (registered=true).
NOT_REIMBURSED: dict[str, dict] = {
    "anagrelide": {
        "registered": True, "reimbursed_nszu": False,
        "notes": "Зареєстрований; НЕ в основному переліку НСЗУ — гідроксисечовина залишається 1L cytoreductive option для PV/ET. Перевірено 2026-04-27 (drlz.com.ua, nszu.gov.ua/likuvannya-zlovkisnykh-novoutvoren).",
    },
    "apalutamide": {
        "registered": True, "reimbursed_nszu": False,
        "notes": "Зареєстрований; станом на 2026-04 не покривається НСЗУ. Out-of-pocket або через благодійні програми. Перевірено 2026-04-27 (drlz.com.ua).",
    },
    "aspirin": {
        "registered": True, "reimbursed_nszu": False, "registration_number": "OTC",
        "notes": "OTC — не входить у реімбурсаційну програму, але загальнодоступний. Перевірено 2026-04-27.",
    },
    "degarelix": {
        "registered": True, "reimbursed_nszu": False,
        "notes": "Зареєстрований; НЕ покривається НСЗУ — лейпролід / госерелін є стандартом онкопакету для АДТ. Перевірено 2026-04-27 (drlz.com.ua).",
    },
    "trifluridine_tipiracil": {
        "registered": True, "reimbursed_nszu": False,
        "notes": "Зареєстрований в Україні; НЕ покривається НСЗУ. Out-of-pocket або через благодійні програми / клінічні дослідження. Перевірено 2026-04-27 (drlz.com.ua).",
    },
    "procarbazine": {
        "registered": False, "reimbursed_nszu": False,
        "notes": "Не зареєстрований в Україні (Держреєстр ЛЗ — не знайдено станом на 2026-04-27). Доступ через named-patient import для PCNSL (R-MPV) та escalated BEACOPP. Перевірено 2026-04-27.",
    },
}

# Drugs whose notes need clinical-context override even though reimbursed.
NOTES_OVERRIDE: dict[str, str] = {
    "abiraterone": (
        "Доступний як генерик; покривається НСЗУ для mCRPC та "
        "mHSPC високого ризику. Перевірено 2026-04-27 (drlz.com.ua, "
        "nszu.gov.ua/likuvannya-zlovkisnykh-novoutvoren)."
    ),
    "rituximab": (
        "Біосиміляри (Truxima, Ruxience, Riabni) широко доступні в "
        "Україні — взаємозамінні з MabThera за керівництвом НСЗУ. "
        "Перевірено 2026-04-27."
    ),
    "filgrastim": (
        "Біосиміляри філграстиму (Tevagrastim, Zarzio, Nivestim тощо) "
        "включені в онкопакет НСЗУ як підтримуюча терапія. "
        "Перевірено 2026-04-27."
    ),
    "trastuzumab": (
        "Біосиміляри (Herzuma, Ontruzant, Kanjinti) широко доступні; "
        "взаємозамінні. Покриття НСЗУ для HER2+ РМЗ та HER2+ раку "
        "шлунка. Перевірено 2026-04-27."
    ),
    "bevacizumab": (
        "Оригінальний біологічний препарат у значній мірі OOP; "
        "біосиміляри (Mvasi, Zirabev) дедалі доступніші; покриття НСЗУ "
        "для відібраних показань (mCRC, гліобластома). Перевірено 2026-04-27."
    ),
    "cetuximab": (
        "Покриття НСЗУ для RAS-WT лівобічного mCRC; для H&N — частково. "
        "Перевірено 2026-04-27."
    ),
    "nab_paclitaxel": (
        "Селективне покриття НСЗУ; для більшості показань — "
        "out-of-pocket. Звичайний паклітаксел є NSZU-default. "
        "Перевірено 2026-04-27."
    ),
    "interferon_alpha": (
        "Доступний як Roferon-A / Intron A; покривається НСЗУ як "
        "онкоімунотерапія в окремих показаннях (передусім МПН). "
        "Перевірено 2026-04-27."
    ),
    "atra": (
        "Стандарт індукції/консолідації APL разом з ATO. Покривається "
        "НСЗУ як життєво необхідний препарат. Перевірено 2026-04-27."
    ),
    "arsenic_trioxide": (
        "Стандарт APL у комбінації з ATRA. Покривається НСЗУ для APL. "
        "Перевірено 2026-04-27."
    ),
    "imatinib": (
        "Доступний як оригінал (Glivec) та генерики; покривається НСЗУ "
        "для CML та Ph+ ALL з 2017. Перевірено 2026-04-27."
    ),
}


def find_block_range(lines: list[str], header: str = "ukraine_registration", base_indent: int = 2) -> tuple[int, int, int] | None:
    """Find (start, end_exclusive, content_indent) for a YAML block under
    header at base_indent spaces. Returns None if not found."""
    pat = re.compile(r"^" + " " * base_indent + re.escape(header) + r"\s*:\s*$")
    for i, line in enumerate(lines):
        if pat.match(line):
            # find end: next non-blank line whose indent <= base_indent
            j = i + 1
            end = len(lines)
            inner_indent = base_indent + 2
            for k in range(i + 1, len(lines)):
                line2 = lines[k]
                if not line2.strip():
                    continue
                line_indent = len(line2) - len(line2.lstrip(" "))
                if line_indent <= base_indent:
                    end = k
                    break
            return (i, end, inner_indent)
    return None


def extract_field(block: str, field: str) -> str | None:
    """Extract a single-line scalar value of `field:` from a text block."""
    m = re.search(r"^\s*" + re.escape(field) + r"\s*:\s*(.*?)\s*$", block, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    # ignore multi-line `>` or `|` markers
    if val in (">", "|", ">-", "|-"):
        return None
    return val


def build_block(stem: str, original_block: str, content_indent: int) -> list[str]:
    """Construct fresh ukraine_registration block lines.

    Honours overrides in NOT_REIMBURSED; defaults to registered=true,
    reimbursed_nszu=true for the rest of pkg1.
    """
    pad = " " * content_indent
    pad2 = " " * (content_indent + 2)

    # Determine registered/reimbursed/registration_number defaults
    if stem in NOT_REIMBURSED:
        cfg = NOT_REIMBURSED[stem]
        registered = cfg["registered"]
        reimbursed = cfg["reimbursed_nszu"]
        reg_num_default = cfg.get("registration_number", None)
        notes_default = cfg["notes"]
    else:
        registered = True
        reimbursed = True
        reg_num_default = None
        notes_default = None

    # Preserve existing registration_number if non-placeholder, non-null
    existing_reg_num = extract_field(original_block, "registration_number")
    if existing_reg_num and existing_reg_num != "null":
        # strip surrounding quotes
        rn = existing_reg_num
        # ignore placeholders
        if "verify-clinical-co-lead" in rn or "TBD" in rn:
            rn = None
        else:
            rn = rn  # keep as-is (already has quotes)
    else:
        rn = None
    if rn is None and reg_num_default is not None:
        rn = f'"{reg_num_default}"'

    # Indications
    indications = INDICATIONS.get(stem)
    if not reimbursed:
        indications = []  # empty if not reimbursed

    # Existing notes
    existing_notes = NOTES_OVERRIDE.get(stem) or notes_default
    if existing_notes is None:
        # Try to preserve single-line notes from original
        m = re.search(r'^\s*notes\s*:\s*"([^"]*)"', original_block, re.MULTILINE)
        if m:
            existing_notes = m.group(1)

    out = [" " * (content_indent - 2) + "ukraine_registration:"]
    out.append(f"{pad}registered: {'true' if registered else 'false'}")
    if rn is not None:
        out.append(f"{pad}registration_number: {rn}")
    else:
        out.append(f"{pad}registration_number: null")
    out.append(f"{pad}reimbursed_nszu: {'true' if reimbursed else 'false'}")
    if indications:
        out.append(f"{pad}reimbursement_indications:")
        for ind in indications:
            # escape any double-quote in indication
            safe = ind.replace('"', '\\"')
            out.append(f'{pad2}- "{safe}"')
    else:
        out.append(f"{pad}reimbursement_indications: []")
    out.append(f'{pad}last_verified: "2026-04-27"')
    if existing_notes:
        safe = existing_notes.replace('"', '\\"')
        out.append(f'{pad}notes: "{safe}"')
    return out


def patch_file(stem: str) -> bool:
    p = DRUGS_DIR / f"{stem}.yaml"
    if not p.exists():
        print(f"[skip-missing] {stem}")
        return False
    text = p.read_text(encoding="utf-8")
    lines = text.split("\n")
    rng = find_block_range(lines, "ukraine_registration", base_indent=2)
    if rng is None:
        rng = find_block_range(lines, "ukraine_registration", base_indent=4)
    if rng is None:
        print(f"[no-block] {stem}")
        return False
    bs, be, content_indent = rng
    original_block = "\n".join(lines[bs:be])
    new_block_lines = build_block(stem, original_block, content_indent)
    new_lines = lines[:bs] + new_block_lines + lines[be:]
    new_text = "\n".join(new_lines)
    if new_text != text:
        p.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


PKG1_STEMS = [
    "fluorouracil", "abiraterone", "acyclovir", "allopurinol", "anagrelide",
    "anastrozole", "apalutamide", "aspirin", "arsenic_trioxide", "atra",
    "bendamustine", "bevacizumab", "bleomycin", "capecitabine",
    "capecitabine_breast", "carboplatin", "cetuximab", "cisplatin",
    "cladribine", "cyclophosphamide", "cytarabine", "dacarbazine",
    "dasatinib", "daunorubicin", "degarelix", "denosumab", "dexamethasone",
    "docetaxel", "doxorubicin", "entecavir", "enzalutamide", "epoetin_alfa",
    "etoposide", "exemestane", "filgrastim", "fludarabine", "fulvestrant",
    "gemcitabine", "glecaprevir_pibrentasvir", "goserelin", "hydroxyurea",
    "idarubicin", "ifosfamide", "imatinib", "interferon_alpha", "irinotecan",
    "leucovorin", "leuprolide", "letrozole", "l_asparaginase",
    "mercaptopurine", "methotrexate", "nab_paclitaxel", "nilotinib",
    "ondansetron", "oxaliplatin", "paclitaxel", "pemetrexed", "pertuzumab",
    "prednisone", "procarbazine", "rituximab", "sofosbuvir_velpatasvir",
    "tamoxifen", "temozolomide", "thiotepa", "trimethoprim_sulfamethoxazole",
    "trastuzumab", "trifluridine_tipiracil", "vinblastine", "vincristine",
    "zidovudine", "zoledronate",
]


def main() -> None:
    updated = 0
    for stem in PKG1_STEMS:
        if patch_file(stem):
            updated += 1
            print(f"[patched] {stem}")
        else:
            print(f"[unchanged] {stem}")
    print(f"\nPatched: {updated}/{len(PKG1_STEMS)}")


if __name__ == "__main__":
    main()
