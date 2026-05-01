"""Plain-UA vocabulary for patient-mode plan rendering.

Each clinical / molecular / regulatory / lab / adverse-event / screening
term maps to a 1-3 sentence Ukrainian explanation written for a
layperson at roughly an 8th-grade reading level. The renderer attaches
these explanations next to the corresponding clinician-facing label so
the patient-mode bundle can be read without a medical dictionary.

Source convention for the plain-UA wording:

  * НСЗУ patient-info brochures (НСЗУ programs of medical guarantees,
    pacient-facing leaflets) — coverage / reimbursement language.
  * МОЗ patient brochures and MOZ-published clinical pathway summaries
    — adverse-event and screening wording.
  * ESMO patient guides (Ukrainian translations published with ESMO
    permission for non-commercial use, CC-BY-NC-ND) — drug-class and
    treatment-rationale wording.
  * Cancer.gov NCI-PDQ patient versions (US National Cancer Institute,
    public domain) — variant-type and biomarker wording, adapted to UA.

This is a render-time, render-only layer. The engine MUST NOT consult
this table as a treatment-selection signal (CHARTER §8.3 invariant —
same contract as `_actionability.py` and `_nszu.py`). NEVER write these
strings back into KB content; they are deliberately maintained
separately so that the canonical KB stays clinician-facing while the
patient layer can be edited / re-translated independently.

Usage:

    from knowledge_base.engine._patient_vocabulary import explain
    explain("V600E")
    # → "конкретна заміна валіну на глутамат у позиції 600 BRAF — …"

The `explain()` helper does case-insensitive lookup across all
categories; callers that need a category-scoped lookup can index the
appropriate dict directly.
"""

from __future__ import annotations

from typing import Optional


# ── Drug-class / mechanism-of-action vocabulary ──────────────────────
#
# Targeted at the renderer's "What this drug does" hover/inline blurb.
# Keep wording short (1-2 sentences) and avoid English jargon where a
# Ukrainian word exists; fall back to inline English for canonical
# molecular labels (BRAF, HER2, PD-1, etc.).

DRUG_CLASS_PLAIN_UA: dict[str, str] = {
    # Targeted small molecules — kinase inhibitors & co.
    "BRAFi": "препарат, який блокує мутацію BRAF — ключову рушійну мутацію пухлини",
    "MEKi": "препарат, який блокує сигнал нижче за BRAF — у комбінації працює краще",
    "BRAF+MEK": "комбінація BRAFi + MEKi — стандартна для BRAF V600 меланоми та деяких NSCLC",
    "PARPi": "препарат, який блокує DNA-repair фермент — пухлина гине, бо не може лагодити свою ДНК",
    "TKI": "tyrosine kinase inhibitor — таблетка, що блокує конкретний пухлинний фермент",
    "EGFRi": "блокує EGFR-сигнал — ключовий для деяких раків легені та CRC",
    "ALKi": "блокує ALK-fusion білок — для ~3-5% раків легені",
    "ROS1i": "блокує ROS1-fusion — для ~1-2% раків легені",
    "FGFRi": "блокує FGFR-сигнал — для cholangiocarcinoma та urothelial",
    "METi": "блокує MET — Ex14-skipping мутація легені",
    "RETi": "блокує RET-fusion — для NSCLC і MTC",
    "NTRKi": "блокує NTRK-fusion — pan-tumor препарат, працює незалежно від типу пухлини",
    "KIT/PDGFRAi": "блокує KIT/PDGFRA — основний препарат для GIST",
    "BTKi": "блокує B-cell receptor signaling — основа для CLL та MCL",
    "BCL-2i": "знімає захист від apoptosis у пухлинних клітинах — клітини самі гинуть",
    "CDK4/6i": "зупиняє поділ клітин — у комбінації з anti-hormonal для breast HR+",
    "mTORi": "блокує mTOR-сигнал — для RCC та breast",
    "VEGFi": "блокує ріст судин у пухлині — пухлина не отримує крові й перестає рости",
    "PI3Ki": "блокує PI3K-сигнал — для деяких breast HR+ та лімфом",
    "AKTi": "блокує AKT-сигнал нижче за PI3K",
    "JAKi": "блокує JAK-кінази — для MPN (myelofibrosis, polycythemia vera)",
    "FLT3i": "блокує FLT3 — для деяких AML",
    "IDHi": "блокує мутантний IDH1/IDH2 — для AML і cholangiocarcinoma",
    "BCRi": "блокує BCR-ABL — основа для CML (imatinib, dasatinib, nilotinib)",
    "HDACi": "блокує histone deacetylase — для T-cell лімфом",
    "EZH2i": "блокує EZH2 — для FL та епітеліоїдної саркоми",
    "SMOi": "блокує Hedgehog-сигнал — для basal-cell карциноми",
    "PSMAi": "цільовий препарат для PSMA-позитивної простати (lutetium-PSMA)",
    "Erbb-pan-i": "блокує родину HER1/HER2/HER3/HER4",
    "KRASi": "блокує мутантний KRAS — нова таргетна група (G12C і незабаром G12D)",

    # Monoclonal antibodies & immune checkpoint inhibitors
    "anti-CD20 mAb": "білок-мітка, що знаходить B-клітини і сигналізує імунній системі знищити їх (включно з лімфомою)",
    "anti-CD19 mAb": "білок-мітка для B-клітин — альтернатива до CD20 при лімфомах",
    "anti-CD22 mAb": "білок-мітка для B-клітин — для ALL та deяких NHL",
    "anti-CD30 mAb": "білок-мітка для лімфоми Ходжкіна та ALCL",
    "anti-CD38 mAb": "білок-мітка для мієломних клітин (daratumumab, isatuximab)",
    "anti-CD52 mAb": "білок-мітка для лімфоцитів — потужна імуносупресія",
    "anti-CD79b mAb": "білок-мітка для B-клітинних лімфом (як ADC: polatuzumab)",
    "anti-CCR4 mAb": "білок-мітка для T-клітинних лімфом (mogamulizumab)",
    "anti-HER2 mAb": "білок-мітка, що знаходить пухлинні клітини з HER2-amplification і нейтралізує їх",
    "anti-EGFR mAb": "блокує EGFR на поверхні клітини — для CRC та плоскоклітинного раку голови/шиї",
    "anti-VEGF mAb": "блокує ріст судин (bevacizumab) — додається до хіміотерапії у багатьох пухлин",
    "anti-PD-1": "імунотерапія — знімає блок з ваших Т-клітин, щоб вони могли атакувати пухлину",
    "anti-PD-L1": "схожий до anti-PD-1, але блокує сигнал з боку самої пухлини",
    "anti-CTLA-4": "імунотерапія, що активує початкову імунну відповідь",
    "anti-LAG3": "новіший checkpoint — у комбінації з anti-PD-1 для меланоми",
    "anti-TIGIT": "експериментальний checkpoint у клінічних випробуваннях",
    "ICI": "imune checkpoint inhibitor — узагальнений термін для anti-PD-1/PD-L1/CTLA-4",
    "anti-RANKL": "блокує кісткову резорбцію (denosumab) — для метастазів у кістки",
    "anti-IL6": "блокує запалення — для CRS після CAR-T",

    # Cell / immune therapies and bispecifics
    "CAR-T": "ваші Т-клітини генетично модифіковані лабораторно, щоб знищувати пухлину",
    "TCR-T": "ваші Т-клітини отримують новий рецептор для розпізнавання конкретного антигена",
    "TIL": "tumor-infiltrating lymphocytes — лімфоцити витягують з пухлини, розмножують і повертають",
    "bispecific antibody": "білок з двома руками — одна тримає Т-клітину, друга — пухлинну",
    "BiTE": "bispecific T-cell engager — підкатегорія bispecifics (blinatumomab)",
    "ADC": "antibody-drug conjugate — антитіло, що несе хіміо-молекулу прямо до пухлини",
    "radioligand": "радіоактивна молекула, що йде до пухлини за рецепторним сигналом (lutetium-PSMA, lutetium-DOTATATE)",
    "oncolytic virus": "вірус, що інфікує переважно пухлинні клітини й руйнує їх (T-VEC)",
    "vaccine therapy": "вакцина, що тренує ваш імунітет розпізнавати пухлинні білки",
    "allo-HSCT": "пересадка стовбурових клітин від донора — потужна, але токсична опція",
    "auto-HSCT": "пересадка ваших власних стовбурових клітин після високодозової хіміотерапії",

    # Classical chemotherapy classes
    "alkylating agent": "класична хіміотерапія, яка пошкоджує ДНК пухлини",
    "anthracycline": "класична хіміотерапія (doxorubicin, daunorubicin); ефективна, але токсична для серця",
    "platinum agent": "класична хіміотерапія (cisplatin, carboplatin, oxaliplatin)",
    "antimetabolite": "блокує синтез ДНК пухлини (5-FU, methotrexate, gemcitabine)",
    "topoisomerase inhibitor": "блокує розплутування ДНК (irinotecan, etoposide)",
    "vinca alkaloid": "блокує мікротрубочки клітин (vincristine, vinblastine)",
    "taxane": "блокує мікротрубочки інакше (paclitaxel, docetaxel)",
    "fluoropyrimidine": "клас 5-FU/capecitabine — основа лікування CRC, gastric, breast",
    "nitrosourea": "alkylating підклас, що проникає у мозок (lomustine, carmustine)",
    "epothilone": "близькі до taxanes, обходять деякі механізми резистентності",
    "purine analog": "fludarabine, cladribine — для CLL та HCL",
    "proteasome inhibitor": "блокує клітинне 'сміттєзбирання' — основа для multiple myeloma (bortezomib, carfilzomib)",

    # Hormonal therapies
    "anti-androgen": "блокує тестостерон-сигнал у простаті (enzalutamide, abiraterone, apalutamide)",
    "GnRH analog": "вимикає тестостерон/естроген на гіпоталамічному рівні",
    "GnRH antagonist": "швидко вимикає тестостерон/естроген — без початкового 'спалаху'",
    "aromatase inhibitor": "блокує синтез естрогену в адипозній тканині (anastrozole, letrozole)",
    "SERM/SERD": "selective estrogen receptor modulator/degrader (tamoxifen, fulvestrant, elacestrant)",
    "AR-degrader": "новий клас — повністю руйнує androgen-receptor білок",
    "progestin": "прогестини як hormonal-маневр у деяких ендометріальних та breast HR+",

    # Other targeted / immunomodulatory drugs and supportive care
    "HMA": "hypomethylating agent — 'reset' епігенетики у мієлоїдних пухлинах",
    "IMiD": "immunomodulator — для multiple myeloma та MDS-LR (lenalidomide, pomalidomide)",
    "bisphosphonate": "захищає кістки від руйнування метастазами (zoledronate, pamidronate)",
    "G-CSF": "стимулятор гранулоцитопоезу — підтримка крові під час хіміотерапії",
    "ESA": "стимулятор еритропоезу — лікування анемії, спричиненої хіміотерапією",
    "antiemetic": "проти нудоти і блювання (ondansetron, aprepitant, palonosetron)",
    "steroid": "кортикостероїд (dexamethasone, prednisone) — як частина схеми та для побічних реакцій",
    "PPI": "інгібітор протонової помпи — захист шлунка під час лікування",
    "anti-fungal prophylaxis": "профілактика грибкових інфекцій під час глибокої нейтропенії",
    "antiviral prophylaxis": "профілактика реактивації HBV/HSV/VZV (entecavir, acyclovir, valacyclovir)",
    "PCP prophylaxis": "профілактика Pneumocystis-пневмонії — TMP/SMX під час інтенсивної імуносупресії",
    "growth factor": "загальний термін для G-CSF / GM-CSF / EPO / TPO-mimetics",
    "TPO-mimetic": "стимулює продукцію тромбоцитів (eltrombopag, romiplostim)",
    "iron chelator": "виводить надлишок заліза після численних трансфузій (deferasirox)",
}


# ── Variant-type vocabulary ──────────────────────────────────────────
#
# Renderer attaches this next to a biomarker label in the actionability
# panel. Keep wording short and concrete; the patient should be able to
# tell whether their lab result matches the recommendation.

VARIANT_TYPE_PLAIN_UA: dict[str, str] = {
    # BRAF
    "V600E": "конкретна заміна валіну на глутамат у позиції 600 BRAF — найчастіша рушійна мутація",
    "V600K": "схожа на V600E, але lysine замість глутамату — поведінкою близько ідентична",
    "V600": "будь-яка заміна у позиції 600 BRAF — клас V600E/K/D/R разом",
    "BRAF non-V600": "інші BRAF-мутації (наприклад G469A, K601E) — потребують індивідуальної оцінки",

    # EGFR
    "T790M": "часто виникає як стійкість до 1-ї та 2-ї лінії EGFR-інгібіторів",
    "C797S": "стійкість до 3-ї лінії EGFR-інгібіторів (osimertinib)",
    "Ex19del": "видалення в 19-му екзоні EGFR — перша значуща EGFR-рушійна мутація",
    "L858R": "точкова заміна в 21-му екзоні EGFR — друга значуща EGFR-рушійна мутація",
    "Ex20ins": "вставка в exon 20 EGFR — гірше відповідає на стандартні EGFR-інгібітори",
    "G719X": "uncommon EGFR — частково чутливий до afatinib/osimertinib",
    "L861Q": "uncommon EGFR — частково чутливий до afatinib/osimertinib",

    # KRAS / NRAS / HRAS
    "G12C": "найчастіша KRAS мутація у NSCLC; має таргетну терапію (sotorasib/adagrasib)",
    "G12D": "найчастіша KRAS мутація у PDAC; ще немає approved таргетної терапії",
    "G12V": "поширена KRAS мутація у CRC та PDAC",
    "G13D": "KRAS мутація позиції 13 — часто у CRC",
    "Q61X": "KRAS/NRAS мутація позиції 61 — 'агресивніший' клас",

    # MET / ERBB2 / etc.
    "Ex14 skipping": "MET без exon 14 = гіперактивний; чутливий до capmatinib/tepotinib",
    "MET amplification": "багато копій MET — частий механізм резистентності до EGFRi",
    "HER2 amplification": "багато копій HER2 — actionable у breast, gastric, biliary, NSCLC",
    "HER2 mutation": "точкова мутація HER2 (часто Ex20ins) — actionable у NSCLC та інших",

    # Generic alteration types
    "amplification": "багато копій гена → гіперекспресія білка; для HER2, MET, FGFR1 — actionable",
    "fusion": "дві ділянки ДНК злилися; для ALK, ROS1, RET, NTRK, FGFR2/3 — критично actionable",
    "rearrangement": "перебудова хромосоми, що часто створює fusion — суть та сама",
    "translocation": "обмін шматками між хромосомами — часто створює fusion білок",
    "inversion": "ділянка ДНК перевернута — також може створити fusion",
    "deletion": "видалення ділянки ДНК — часто веде до loss-of-function",
    "insertion": "вставка зайвих нуклеотидів у ген — порушує функцію білка",
    "missense": "одна амінокислота замінена іншою — функція може бути збережена або порушена",
    "nonsense": "стоп-кодон з'явився всередині гена — білок обривається посередині",
    "frameshift": "вставка/делеція зміщує 'рамку зчитування' — білок повністю спотворюється",
    "splice site": "мутація на межі екзон/інтрон — порушує правильну збірку білка",
    "loss-of-function": "ген не працює (часто — tumor suppressor як TP53, PTEN, ATM)",
    "gain-of-function": "білок працює сильніше за норму — типово для онкогенів",
    "biallelic loss": "обидві копії гена пошкоджені — пухлина повністю втратила цю функцію",

    # Origin / zygosity
    "germline": "мутація успадкована від батьків; присутня у всіх клітинах тіла; впливає на родичів",
    "somatic": "мутація з'явилася лише в пухлині; не передається дітям",
    "heterozygous": "одна копія гена змінена, інша нормальна",
    "homozygous": "обидві копії гена однакові (часто обидві пошкоджені)",
    "mosaic": "мутація присутня лише в частині клітин організму",

    # Quantitative biomarkers
    "VAF": "процент клітин пухлини з цією мутацією — 50% означає, що половина клітин має її",
    "TMB-high": "пухлина має багато мутацій — частіше відповідає на імунотерапію",
    "TMB-low": "пухлина має мало мутацій — імунотерапія працює гірше",
    "MSI-H": "пухлина не може лагодити неспівпадіння в ДНК → багато мутацій → ICI eligibility",
    "MSI-L": "проміжний стан між MSI-H і MSS — рідко actionable",
    "MSS": "стабільні мікросателіти — імунотерапія зазвичай не працює",
    "dMMR": "deficient mismatch repair — фактично те саме, що MSI-H",
    "pMMR": "proficient mismatch repair — інтактна система виправлення помилок",
    "HRD-positive": "пухлина не може лагодити double-strand breaks → чутлива до PARPi + платинових",
    "HRD-negative": "система репарації працює — PARPi працюватиме гірше",
    "PD-L1 high": "пухлина демонструє багато PD-L1 — частіше відповідає на anti-PD-1",
    "PD-L1 low": "PD-L1 знижений — імунотерапія працює гірше, але не виключена",
    "CPS": "Combined Positive Score — стандарт для PD-L1 у деяких пухлинах (gastric, cervical)",
    "TPS": "Tumor Proportion Score — стандарт для PD-L1 у NSCLC",

    # Lymphoma-specific
    "double-hit lymphoma": "лімфома з двома рушійними транслокаціями (MYC + BCL2) — агресивніша",
    "triple-hit lymphoma": "MYC + BCL2 + BCL6 — найагресивніший підтип",
    "GCB": "germinal center B-cell — підтип DLBCL з кращим прогнозом",
    "ABC": "activated B-cell — підтип DLBCL з гіршим прогнозом",
    "MYD88 L265P": "характерна мутація для Waldenström і деяких DLBCL",
    "del(17p)": "втрата короткого плеча хромосоми 17, що несе TP53 — поганий прогноз у CLL/MM",
    "TP53 mutation": "ушкодження ключового tumor suppressor — асоційоване з гіршим прогнозом",
    "complex karyotype": "≥3 хромосомних аномалії — поганий прогноз у CLL та AML",
    "t(11;14)": "translocation у MCL та частина MM — створює CCND1 overexpression",
    "t(14;18)": "translocation у follicular lymphoma — створює BCL2 overexpression",
    "t(8;14)": "translocation у Burkitt lymphoma — створює MYC overexpression",
    "t(15;17)": "translocation, що визначає APL — PML-RARA fusion",
    "t(9;22)": "Philadelphia chromosome — BCR-ABL fusion (CML, Ph+ ALL)",
    "inv(16)": "inversion at chromosome 16 — favorable AML прогноз",
    "del(5q)": "часта втрата при MDS-low risk",
    "FLT3-ITD": "internal tandem duplication FLT3 — несприятливий AML",
    "FLT3-TKD": "tyrosine kinase domain mutation FLT3 — менш несприятливий, ніж ITD",
    "NPM1 mutation": "часто favorable у AML без FLT3-ITD",
    "JAK2 V617F": "характерна для polycythemia vera і деяких MPN",
    "CALR mutation": "альтернативна до JAK2 у essential thrombocythemia та myelofibrosis",
    "BCR-ABL": "fusion gene при CML — повністю керується TKI терапією",
    "PML-RARA": "fusion у APL — драматично відповідає на ATRA + ATO",

    # Hereditary syndromes (often surfaced via germline panels)
    "BRCA1": "ген репарації ДНК; germline-мутація = підвищений ризик breast/ovarian/prostate/PDAC",
    "BRCA2": "схожий до BRCA1; чутливість до PARPi і платинових препаратів",
    "ATM": "ген репарації; germline = підвищений ризик breast і lymphoma",
    "PALB2": "партнер BRCA2; germline = підвищений ризик breast та PDAC",
    "Lynch syndrome": "germline дефект MMR-генів (MLH1/MSH2/MSH6/PMS2) — CRC, endometrial, інші",
    "Li-Fraumeni": "germline TP53 — широкий спектр пухлин у молодому віці",
    "MEN1": "Multiple Endocrine Neoplasia type 1 — пангeard ендокринних пухлин",
    "MEN2": "Multiple Endocrine Neoplasia type 2 — RET germline, MTC та інші",
    "VHL": "von Hippel-Lindau — RCC, hemangioblastoma, pheochromocytoma",
    "NF1": "neurofibromatosis type 1 — підвищений ризик MPNST та інших пухлин",
    "FAP": "familial adenomatous polyposis — APC germline → ранній CRC",
}


# ── ESCAT tier vocabulary ────────────────────────────────────────────
#
# ESCAT (ESMO Scale for Clinical Actionability of molecular Targets)
# tier explanations. Plain-UA wording for the actionability panel.

ESCAT_PLAIN_UA: dict[str, str] = {
    "IA": "найвищий рівень — препарат FDA/EMA-схвалений саме для вашого варіанту й типу пухлини, з randomized clinical trial доказами",
    "IB": "дуже високий рівень — препарат працює, часто вимагається комбінація",
    "IIA": "помірний рівень — ретроспективні дані показують клінічну користь у вашому типі пухлини",
    "IIB": "обмежений рівень — попередні дані обнадійливі, але треба більше доказів",
    "IIIA": "цільовий препарат існує для іншого типу пухлини — basket-trial показує користь і у вас; обговорити з лікарем",
    "IIIB": "цільовий препарат існує для іншого типу — basket-даних поки немає для вашого; trial-only",
    "IV": "preclinical — поки тільки клітинні/тваринні моделі",
    "X": "поки немає клінічно значущих даних для вашого варіанту",
}


# OncoKB level vocabulary intentionally omitted — OncoKB ToS forbids
# OpenOnco's use case (CHARTER §2 conflict). Actionability vocabulary
# is render-firewalled from patient mode anyway. If patient-facing
# CIViC level translations are added later, they need clinical UA review.


# ── НСЗУ availability vocabulary ─────────────────────────────────────
#
# Patient-facing language for the NSZU coverage badge.

NSZU_PLAIN_UA: dict[str, str] = {
    "covered": "Держбюджет покриває цей препарат для вашого діагнозу — ви не платите",
    "partial": "Препарат покривається NSZU, але не для цього показання — потрібно або змінити лікування, або платити самому",
    "oop": "Ви оплачуватимете цей препарат самостійно (приблизно 2200-30000 UAH/цикл залежно від препарату)",
    "not-registered": "Цей препарат поки що не доступний легально в Україні; потрібен named-patient import, EAP від виробника, або поїздка до EU",
}


# ── Lab / functional-status vocabulary ───────────────────────────────
#
# Renderer attaches this where the plan refers to a lab threshold, ECOG,
# or functional metric. Keep wording action-oriented (what will happen if
# the value is out of range).

LAB_PLAIN_UA: dict[str, str] = {
    "CrCl": "як добре нирки фільтрують — якщо <30 мл/хв, дозу зменшують або препарат не використовують",
    "GFR": "ниркова фільтрація — синонім CrCl у клінічних рекомендаціях",
    "eGFR": "розрахунок ниркової фільтрації за креатиніном — те саме, що CrCl",
    "ECOG": "оцінка вашого загального стану — 0 = повна активність, 4 = повна нерухомість",
    "Karnofsky": "альтернативна шкала загального стану — від 0 (смерть) до 100 (повна активність)",
    "PS": "performance status — узагальнено для ECOG/Karnofsky",
    "Hgb": "гемоглобін — кисень-носна функція; <8 г/дл = можлива анемія, потрібне переливання",
    "WBC": "загальна кількість лейкоцитів — занадто низька = ризик інфекцій",
    "ANC": "absolute neutrophil count — критично для запобігання інфекціям під час хіміотерапії; <0.5 = висока ризик сепсису",
    "ALC": "absolute lymphocyte count — нижчий = вища імуносупресія",
    "platelets": "тромбоцити — згортання крові; <50 000 = ризик кровотечі",
    "PLT": "те саме, що platelets — скорочення з аналізу",
    "bilirubin": "печінкова функція; підвищений = можлива печінкова токсичність препарату",
    "creatinine": "ниркова функція; підвищений = можлива потреба зменшити дозу",
    "ALT": "печінковий фермент — підвищений = можлива гепатотоксичність препарату",
    "AST": "печінковий фермент — підвищений = можлива гепатотоксичність препарату",
    "ALP": "alkaline phosphatase — підвищена при ураженні печінки/кісток метастазами",
    "GGT": "печінковий фермент — підвищений при холестазі та алкогольному ураженні",
    "ALT/AST": "печінкові ферменти — підвищені = можлива гепатотоксичність препарату",
    "LDH": "lactate dehydrogenase — маркер швидкого пухлинного росту",
    "albumin": "білок плазми; знижений = ризик токсичності деяких препаратів (наприклад іфосфаміду)",
    "calcium": "кальцій крові; підвищений = тривога щодо кісткових метастазів і паранеопластичного синдрому",
    "uric acid": "сечова кислота; підвищена після хіміотерапії = ризик tumor lysis syndrome",
    "INR": "показник згортання — підвищений = підвищений ризик кровотечі",
    "PT": "prothrombin time — оцінка зовнішнього шляху коагуляції",
    "aPTT": "activated partial thromboplastin time — оцінка внутрішнього шляху коагуляції",
    "TSH": "функція щитоподібної залози; може змінюватися від імунотерапії",
    "T4": "тироксин — використовується разом з TSH для оцінки щитоподібної",
    "cortisol": "гормон надниркових; контролюється на фоні імунотерапії",
    "glucose": "цукор крові; підвищений на фоні стероїдів і деяких таргетних препаратів",
    "HbA1c": "тримісячний показник глюкози — для моніторингу діабету під час лікування",
    "lipase": "ферменти підшлункової — підвищені після імунотерапії = ризик панкреатиту",
    "amylase": "те саме, що lipase, у контексті панкреатиту",
    "CK": "creatine kinase — підвищений при міозитах від імунотерапії",
    "troponin": "маркер ушкодження серця — критичний на фоні anthracyclines і деяких ICI",
    "BNP": "маркер серцевої недостатності — стежать на фоні кардіотоксичних схем",
    "NT-proBNP": "альтернатива BNP, той самий клінічний сенс",
    "LVEF": "фракція викиду лівого шлуночка — серце; <50% = переглянути anthracycline/trastuzumab",
    "QTc": "інтервал на ЕКГ; подовжений = ризик аритмії на тлі деяких таргетних препаратів",
    "B12": "вітамін B12 — низький рівень = можлива причина анемії або neuropathy",
    "ferritin": "запаси заліза в організмі — низький = залізодефіцитна анемія",
    "iron": "сироваткове залізо — частина оцінки анемії",
    "transferrin": "транспортний білок заліза — допомагає інтерпретувати ferritin",
    "vitamin D": "часто знижений у онкологічних пацієнтів — може впливати на кістки",
    "PSA": "простатоспецифічний антиген — маркер відповіді на лікування простати",
    "CEA": "опухолевий маркер при CRC, breast, gastric — стежать у динаміці",
    "CA 19-9": "маркер при PDAC, biliary, gastric",
    "CA-125": "маркер при ovarian — стежать як показник відповіді/рецидиву",
    "CA 15-3": "маркер при breast — стежать як індикатор рецидиву",
    "AFP": "α-fetoprotein — маркер HCC та germ-cell tumors",
    "β-hCG": "маркер germ-cell tumors і трофобластичних пухлин",
    "chromogranin A": "маркер neuroendocrine tumors",
    "VAF": "процент клітин пухлини з цією мутацією — підвищена відсоткова частка часто означає більш активну пухлину",
    "BMI": "індекс маси тіла; екстремальні значення впливають на дозування і толерантність",
    "BSA": "площа поверхні тіла — для розрахунку дози багатьох хіміопрепаратів",
}


# ── Adverse-event vocabulary ─────────────────────────────────────────
#
# Renderer attaches this in the side-effects panel + emergency banner.
# Wording is action-oriented: what to do if you notice this.

AE_PLAIN_UA: dict[str, str] = {
    "neutropenia": "знижена кількість нейтрофілів → ризик інфекцій → лихоманка >38°C — терміново звертатись до лікаря",
    "febrile neutropenia": "лихоманка на фоні нейтропенії — ургентний стан, негайно у відділення",
    "thrombocytopenia": "знижена кількість тромбоцитів → ризик кровотечі → синці, кровоточивість ясен/носа = звернутись",
    "anemia": "знижений гемоглобін → втома, задишка → можлива потреба переливання",
    "leukopenia": "знижені лейкоцити загалом — ширше за нейтропенію",
    "lymphopenia": "знижені лімфоцити — підвищений ризик опортуністичних інфекцій",
    "pancytopenia": "знижені всі три лінії крові — потребує негайної оцінки",
    "mucositis": "запалення слизової рота — біль при ковтанні; можна полегшити полосканням",
    "stomatitis": "те саме, що mucositis — виразки і біль у роті",
    "esophagitis": "запалення стравоходу — біль за грудиною при ковтанні",
    "diarrhea": "часті рідкі випорожнення — небезпечно якщо >10 разів на день; зневоднення = звернутись",
    "constipation": "запор — типово при vinca alkaloids та deяких опіоїдах",
    "nausea/vomiting": "нудота і блювання; контролюємо antiemetics; >24 години без полегшення = звернутись",
    "anorexia": "втрата апетиту — поширене побічне явище; стежте за вагою",
    "dysgeusia": "зміна сприйняття смаку — типово при таргетній і платиновій терапії",
    "alopecia": "тимчасова втрата волосся — повертається після завершення лікування",
    "fatigue": "постійна втома, відсутність сили — характерна для всіх онкологічних терапій",
    "asthenia": "виражена слабкість — синонім fatigue",
    "hand-foot syndrome": "почервоніння і біль у долонях/підошвах від деяких препаратів (capecitabine, regorafenib)",
    "PPE": "palmar-plantar erythrodysesthesia — інша назва hand-foot syndrome",
    "rash": "висип на шкірі — частий побічний ефект EGFRi та імунотерапії",
    "pruritus": "сверблячка — часто супроводжує висип на тлі імунотерапії",
    "photosensitivity": "підвищена чутливість до сонця — використовуйте крем SPF 50+",
    "infusion reaction": "реакція на введення препарату — лихоманка, озноб, задишка під час інфузії; повідомляйте медсестрі негайно",
    "anaphylaxis": "тяжка алергічна реакція — задишка, набряк, гіпотензія; невідкладна медична допомога",
    "CRS": "cytokine release syndrome — лихоманка, гіпотензія, гіпоксія після CAR-T або bispecifics; ургентний стан",
    "ICANS": "нейротоксичність, пов'язана з імунною клітинною терапією — сплутаність свідомості, тремор після CAR-T",
    "pneumonitis": "запалення легень — задишка, кашель; рідко але серйозно",
    "interstitial lung disease": "ускладнення деяких таргетних препаратів — задишка, кашель; терміново",
    "hepatotoxicity": "токсичність для печінки — слабість, жовте забарвлення шкіри/очей, темна сеча; терміново",
    "hepatitis": "запалення печінки — частіше від імунотерапії; стежать ALT/AST",
    "cardiotoxicity": "токсичність для серця (від антрациклінів, трастузумабу) — задишка, набряки, прискорене серцебиття",
    "QT prolongation": "подовження QT-інтервалу — ризик аритмії; контроль ЕКГ",
    "hypertension": "підвищений артеріальний тиск — частий ефект VEGFi та TKI",
    "thromboembolism": "тромбози — підвищений ризик при IMiD та деяких хіміотерапіях",
    "neuropathy": "поколювання, оніміння кистей/стіп (taxanes, vinca alkaloids, platinum); часто незворотна",
    "peripheral neuropathy": "те саме, що neuropathy — конкретно про периферичні нерви",
    "ototoxicity": "втрата слуху або шум у вухах — ризик від цисплатину",
    "nephrotoxicity": "ушкодження нирок — особливо від цисплатину чи метотрексату; контроль креатиніну",
    "hemorrhagic cystitis": "кров у сечі від cyclophosphamide/ifosfamide; запобігаємо MESNA та гідратацією",
    "tumor lysis syndrome": "TLS — масовий розпад пухлинних клітин → розлад електролітів; небезпечно у перший тиждень лікування",
    "differentiation syndrome": "ускладнення ATRA/IDHi у AML — задишка, набряки, лихоманка; терміново стероїди",
    "ВІЛ-реактивація": "у пацієнтів з прихованим ВГВ ризик активації під час хіміотерапії — потрібна профілактика entecavir",
    "HBV reactivation": "латентний гепатит B може активуватися під час імуносупресії — entecavir для профілактики",
    "HCV reactivation": "латентна інфекція може активуватися під час імуносупресії",
    "HSV reactivation": "герпес може активуватися під час хіміотерапії — acyclovir для профілактики",
    "VZV reactivation": "вітряна віспа/оперізуючий герпес може активуватися — valacyclovir для профілактики",
    "CMV reactivation": "цитомегаловірус — особливо важливий після алло-ТСК",
    "PJP": "Pneumocystis jirovecii pneumonia — рідкісна, але смертельна без TMP/SMX профілактики",
    "secondary malignancy": "ризик другої пухлини через роки після хіміотерапії — важливо знати",
    "infertility": "тимчасова або постійна втрата фертильності — обговорити кріоконсервацію репродуктивних клітин перед стартом",
    "menopausal symptoms": "припливи, сухість слизових — ефект hormonal-терапії",
    "weight gain": "набирання ваги — частий ефект стероїдів та hormonal-блокаторів",
    "weight loss": "втрата ваги — типова при поширеній пухлині та хіміотерапії",
    "edema": "набряки — частий ефект imatinib, taxanes та deяких таргетних",
    "pleural effusion": "рідина в плеврі — типова при dasatinib",
    "ascites": "рідина в животі — поширений симптом ovarian і peritoneal carcinomatosis",
    "lymphedema": "набряк руки/ноги після лімфаденектомії або променевої — постійна проблема",
    "thyroid dysfunction": "гіпо- або гіпертиреоз від ICI — стежать TSH",
    "hypophysitis": "запалення гіпофіза від ICI — терміново стероїди",
    "adrenal insufficiency": "недостатність надниркових від ICI — глюкокортикоїдна заміна довічно",
    "type 1 diabetes (ICI-induced)": "новий діабет від імунотерапії — рідкісний, але незворотний",
    "colitis": "запалення кишечника від імунотерапії — діарея, біль; терміново стероїди",
    "myocarditis": "запалення серця від імунотерапії — рідкісне, але смертельне; ургентно",
    "myositis": "запалення м'язів від імунотерапії — слабкість, біль; стероїди",
    "uveitis": "запалення ока від імунотерапії — біль, почервоніння, погіршення зору",
    "encephalitis": "запалення мозку від імунотерапії — головний біль, сплутаність; ургентно",
    "Guillain-Barré": "імунно-опосередковане ураження периферичних нервів від ICI — ургентно",
    "myasthenia gravis": "слабкість м'язів очей і ковтання від ICI — терміново",
    "renal toxicity (ICI)": "імунно-опосередкований нефрит — підвищений креатинін; стероїди",
    "skin toxicity (EGFRi)": "акнеформний висип на тлі EGFRi — фактично свідчить про активність препарату",
    "paronychia": "запалення нігтьового валика на тлі EGFRi/MEKi",
    "ocular toxicity (MEKi)": "тимчасові порушення зору на тлі траметинібу/кобіметинібу",
    "GVHD": "graft-versus-host disease — імунна реакція донорських клітин проти ваших тканин після allo-HSCT",
    "VOD/SOS": "veno-occlusive disease / sinusoidal obstruction syndrome — ускладнення HSCT",
    "engraftment syndrome": "ранні дні після HSCT — лихоманка, висип, набряки",
    "secondary infection": "опортуністичні інфекції під час глибокої імуносупресії — постійна пильність",
    "fall risk": "ризик падіння через втому, neuropathy, hypotension — приберіть килими, тримайтесь",
    "bone loss": "втрата кісткової маси на тлі hormonal-блокаторів — denosumab/bisphosphonate для захисту",
    "osteonecrosis of jaw": "рідкісне ускладнення denosumab/bisphosphonate — стоматолог перед початком",
}


# ── Screening / surveillance vocabulary ──────────────────────────────
#
# Used in the "before-start" workup and surveillance schedule sections.

SCREENING_PLAIN_UA: dict[str, str] = {
    "HBV serology": "тест на гепатит В перед початком імуносупресії — щоб уникнути реактивації",
    "HCV antibody": "тест на гепатит С — частіше асоційований з MZL та DLBCL",
    "HIV test": "стандартний тест перед серйозною хіміотерапією та імунотерапією",
    "EBV-DNA": "тест на Епштейн-Барр вірус — особливо важливий перед CAR-T та для NK/T-nasal лімфом",
    "CMV serology": "тест на цитомегаловірус — критичний перед allo-HSCT",
    "TB screening": "виключення активного або латентного туберкульозу перед anti-PD-1 або високими дозами стероїдів",
    "QuantiFERON": "лабораторний тест на латентний туберкульоз — альтернатива пробі Манту",
    "syphilis screening": "тест на сифіліс перед початком HSCT та інших серйозних схем",
    "echocardiogram": "ехокардіографія — для оцінки серцевої функції перед anthracycline або trastuzumab",
    "MUGA scan": "альтернатива echo для оцінки LVEF — точніше число, але радіація",
    "ECG": "стандартна ЕКГ — для оцінки QTc і виключення патології перед TKI",
    "PET-CT": "позитронно-емісійна томографія — найбільш чутливий метод для лімфом і деяких солідних пухлин",
    "CT chest/abdomen/pelvis": "стандартний staging-тест більшості пухлин — оцінка поширення",
    "MRI brain": "виключення метастазів у мозок — обов'язковий перед лікуванням ALK+ NSCLC і меланоми",
    "bone scan": "сцинтиграфія кісток — для виявлення кісткових метастазів",
    "bone marrow biopsy": "трепанобіопсія — для оцінки лімфом, мієломи, AML/MDS",
    "lumbar puncture": "люмбальна пункція — оцінка CNS-залучення при ALL, лімфомах",
    "endoscopy": "ендоскопія — для оцінки CRC, gastric, esophageal",
    "colonoscopy": "колоноскопія — для CRC скринінгу та контролю",
    "mammography": "мамографія — стандартний скринінг breast cancer",
    "breast MRI": "MRI грудних залоз — для жінок з BRCA та з high-risk сценаріями",
    "Pap smear": "цитологія шийки матки — скринінг cervical cancer",
    "HPV test": "тест на онкогенні штами HPV — поряд із Pap smear",
    "low-dose CT chest": "LDCT — скринінг легені у курців",
    "PSA screening": "PSA-моніторинг — для контролю прогресії або скринінгу простати",
    "CEA monitoring": "регулярний контроль CEA після CRC-резекції — раннє виявлення рецидиву",
    "MRD monitoring": "minimal residual disease — глибокий молекулярний контроль після ремісії",
    "fertility consult": "консультація з репродуктологом перед початком — кріоконсервація сперми/яйцеклітин",
    "dental clearance": "санація ротової порожнини перед bisphosphonate/denosumab — профілактика ONJ",
    "ophthalmology baseline": "огляд очного дна перед MEKi/IDHi-терапією",
    "PFT": "pulmonary function tests — оцінка легень перед bleomycin або brentuximab vedotin",
    "DLCO": "дифузійна здатність легень — компонент PFT, особливо чутливий до bleomycin-tox",
    "audiometry": "тест слуху перед cisplatin — і повторно протягом курсу",
    "neuropsych baseline": "оцінка когнітивних функцій перед HSCT та CAR-T",
    "fall risk assessment": "оцінка ризику падіння у літніх — особливо актуально перед інтенсивними схемами",
    "geriatric assessment": "комплексна оцінка геронтологом — стандарт перед терапією у >70 років",
    "frailty score": "індекс крихкості — впливає на вибір інтенсивності схеми",
    "DEXA scan": "денситометрія — оцінка кісткової маси перед AI/ADT",
    "vaccination review": "перевірка вакцинації (грип, пневмокок, HBV, COVID) перед імуносупресією",
}


# ── Combined lookup helper ───────────────────────────────────────────

_ALL_TABLES: tuple[dict[str, str], ...] = (
    DRUG_CLASS_PLAIN_UA,
    VARIANT_TYPE_PLAIN_UA,
    ESCAT_PLAIN_UA,
    NSZU_PLAIN_UA,
    LAB_PLAIN_UA,
    AE_PLAIN_UA,
    SCREENING_PLAIN_UA,
)


def explain(term: str) -> Optional[str]:
    """Return plain-UA explanation for a clinical/molecular term, or None.

    Lookup order:
      1. Exact match across all category tables (preserves case-sensitive
         distinctions like ESCAT "IA" vs ONCOKB "1").
      2. Case-insensitive, whitespace-stripped match — handles minor
         spelling variation in caller-supplied labels.

    Returns None when no entry matches; caller should fall back to the
    raw clinician label rather than dropping the term silently."""
    if not term:
        return None
    for table in _ALL_TABLES:
        if term in table:
            return table[term]
    norm = term.strip().lower()
    if not norm:
        return None
    for table in _ALL_TABLES:
        for k, v in table.items():
            if k.lower() == norm:
                return v
    return None


# ── Patient-mode tier badge labels ───────────────────────────────────
#
# Shorter labels for the on-page badge itself (the long ESCAT_PLAIN_UA
# explanations live in the tooltip / detail block).

ESCAT_TIER_PATIENT_LABEL: dict[str, str] = {
    "IA": "Найвищий рівень доказів — FDA схвалив саме для вас",
    "IB": "Дуже високий — у комбінації",
    "IIA": "Помірний — ретроспективні дані",
    "IIB": "Обмежений — попередні дані обнадійливі",
    "IIIA": "Цільовий препарат існує — обговорити",
    "IIIB": "Цільовий препарат для іншого типу — trial-only",
    "IV": "Поки тільки лабораторні моделі",
    "X": "Поки даних немає",
}


NSZU_PATIENT_LABEL: dict[str, str] = {
    "covered": "Безкоштовно за програмою НСЗУ",
    "partial": "НСЗУ покриває препарат, але не для цього діагнозу",
    "oop": "Платно (з кишені)",
    "not-registered": "Не зареєстровано в Україні",
}


# ── First-use abbreviation expansion (Phase 5) ───────────────────────
#
# Acronyms that the patient should see expanded the first time they
# appear in renderer-controlled prose. Renderer applies via
# `expand_first_use()` once per bundle. Subsequent occurrences stay
# bare. Engine MUST NOT consult this table (CHARTER §8.3).

ABBREVIATION_FIRST_USE_UA: dict[str, str] = {
    "ESCAT": "ESCAT (рівень доказів — як міцно доведено, що препарат працює)",
    "FDA": "FDA (Управління з продовольства й медикаментів США)",
    "MDT": "MDT (мультидисциплінарна команда лікарів)",
    "ECOG": "ECOG (шкала функціонального стану пацієнта)",
    "MSI": "MSI (індекс мікросателітної нестабільності пухлини)",
    "PD-L1": "PD-L1 (білок на пухлинних клітинах, що блокує імунну атаку)",
    "PD-1": "PD-1 (білок-перемикач імунної системи)",
    "HCV": "HCV (вірус гепатиту C)",
    "HBV": "HBV (вірус гепатиту B)",
    "CAR-T": "CAR-T (терапія модифікованими T-клітинами пацієнта)",
}


# ── Allowlist for the no-Latin / no-abbreviation render gate ─────────
#
# PATIENT_MODE_SPEC §5.3 + §5.4. Tokens here may appear in the rendered
# patient body without triggering the test gate.

# Uppercase abbreviations that may stay bare. Includes gene symbols,
# regimen acronyms widely used in patient-facing material, drug brand
# acronyms, lab abbreviations, and the keys of ABBREVIATION_FIRST_USE_UA
# (the gate treats post-expansion bare occurrences as fine).
PATIENT_ALLOWLIST_ACRONYMS: frozenset[str] = frozenset({
    # Gene symbols + biomarkers (subset; full list grows per disease)
    "BRAF", "EGFR", "KRAS", "NRAS", "BRCA", "BRCA1", "BRCA2", "ALK",
    "ROS1", "RET", "MET", "HER2", "PD-1", "PD-L1", "KIT", "FGFR3",
    "JAK2", "BCR-ABL1", "MGMT", "IDH1", "IDH2", "FLT3", "NPM1", "TP53",
    "PIK3CA", "PTEN", "RB1", "MYC", "BCL2", "CDKN2A", "CD20", "CD30",
    "CD38", "CD52", "CD79", "CCR4", "VEGF", "CTLA-4", "LAG3", "TIGIT",
    "MMR", "HRD", "CPS", "AFP", "PSA",
    # Disease abbreviations the patient may search
    "AML", "ALL", "CLL", "DLBCL", "FL", "MM", "MZL", "MCL", "NHL", "WM",
    "HL", "TNBC", "NSCLC", "SCLC", "RCC", "HCC", "MDS", "MPN", "CML",
    "APL", "PMF", "PV", "ET", "AITL", "ALCL", "MGUS", "GIST", "GBM",
    "HNSCC", "PDAC", "CRC", "PTCL", "PTLD", "ATLL", "T-ALL", "HCL",
    "EATL", "HSTCL", "PMBCL", "PCNSL", "MF", "CTCL", "NLPBL", "NLPHL",
    "iNHL", "T-PLL", "FLT3-ITD",
    # Toxicities / outcomes
    "TLS", "CRS", "GVHD", "VOD", "SOS", "DIC", "ICANS", "PFS", "OS",
    "DFS", "EFS", "RFS", "CR", "PR", "SD", "PD", "ORR", "DCR", "MRD",
    "ANC", "LVEF", "INR", "PFT", "DLCO", "ECG", "EKG", "ICU", "MRI",
    "MUGA", "CTCAE", "QT", "QTc", "BMI", "LDH", "CRP", "BMD",
    # Drug names that travel as acronyms (INN/brand)
    "5-FU", "BCG", "ATRA", "ATO", "TKI", "ADC", "FU",
    # Standard regimen acronyms (widely cited in patient guides)
    "ABVD", "BEACOPP", "CHOP", "CHP", "CHOEP", "RCHOP", "RCHP", "RCVP",
    "BR", "RB", "RFC", "FCR", "RDHA", "RICE", "ICE", "EPOCH", "DEPOC",
    "FOLFOX", "FOLFIRI", "FOLFIRINOX", "CAPOX", "XELOX", "FOLFOXIRI",
    "BV", "AVD", "VAD", "DA-EPOCH", "DRC", "BVD", "VRD", "VTD", "DVD",
    "PVAG", "GEMOX", "GEMCIS", "MAGIC", "FLOT", "STRIDE", "DAA",
    # First-use-expanded abbreviations
    "ESCAT", "FDA", "MDT", "ECOG", "MSI", "HCV", "HBV", "HIV", "EBV",
    "CMV", "TB",
    # Allowed Latin biology fragments
    "DNA", "RNA", "mRNA", "MoA", "AE",
    # ESCAT tier labels
    "IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X",
    # Site / tooling
    "OpenOnco", "GitHub", "MIT", "API", "URL",
    # Routes / common short tokens
    "IV", "PO", "SC", "IM", "IT", "CT", "UA", "EN", "PHI", "CD",
    "NSZU",  # already Cyrillic in body but ASCII-only HTML attrs
})


# Lowercase Latin words that may stay bare. Loanwords, biology stems,
# URL fragments, and unavoidable KB regimen-name vocabulary (CHARTER
# §6.1 prevents unilateral KB rewrites — the gate accepts these
# contextually rather than blocking the whole feature on translation).
PATIENT_ALLOWLIST_LATIN_WORDS: frozenset[str] = frozenset({
    # Biology / pharmacology stems
    "anti", "post", "pre", "non", "neo", "auto", "allo", "alpha", "beta",
    "gamma", "delta", "kappa", "lambda", "wild", "type",
    # KB regimen-name vocabulary
    "cycle", "cycles", "week", "weeks", "month", "months", "year",
    "years", "day", "days", "course", "courses", "phase", "phases",
    "cohort", "regimen", "regimens", "monotherapy", "continuous",
    "until", "progression", "toxicity", "unacceptable", "induction",
    "consolidation", "maintenance", "lymphodepletion", "bridging",
    "salvage", "adjuvant", "neoadjuvant", "first", "second", "third",
    "high", "low", "risk", "trial", "stage", "line", "grade",
    # URL / tooling
    "github", "issues", "info", "html", "https", "www", "openonco",
    "claude", "code", "src", "noopener", "noreferrer",
    # Tooling sentinel that may surface in <!-- comments --> stripped
    # by _visible_text — defensive
    "abbrev", "expanded",
})


# Trial-name prefixes — any acronym starting with these passes the
# uppercase gate without an explicit listing.
PATIENT_ALLOWLIST_TRIAL_PREFIXES: tuple[str, ...] = (
    "KEYNOTE", "CHECKMATE", "JAVELIN", "MURANO", "VENICE", "CASTOR",
    "POLLUX", "ALEX", "ALCANZA", "MAVORIC", "ECHELON", "ECHO", "ELOQUENT",
    "FLAURA", "AURA", "OAK", "POPLAR", "IMPOWER", "PACIFIC", "STRIDE",
    "EMERALD", "VIALE", "RATIFY", "APL0406", "IRIS", "RESPONSE", "COMFORT",
    "COMMANDS", "BEACON", "TOGA", "MPACT", "POLO", "SUNLIGHT", "BCFI",
    "STAMPEDE", "ATLAS", "OLYMPIA", "MIRROR", "PROFOUND", "EMBARK",
    "GALACTIC", "ARASENS", "CHAARTED", "LATITUDE", "TITAN", "TROPICAL",
    "DESTINY", "EMBRACA", "PALOMA", "MONALEESA", "MONARCH", "RUBY",
    "ATTRACTION", "TROPiCS", "POSEIDON", "GEMINI", "MARS",
)


def is_allowlisted_acronym(token: str) -> bool:
    """True if `token` is on the patient-mode acronym allowlist —
    either explicitly listed or matches a clinical-trial prefix."""
    if not token:
        return False
    if token in PATIENT_ALLOWLIST_ACRONYMS:
        return True
    upper_prefix = token.split("-", 1)[0].upper()
    if upper_prefix in PATIENT_ALLOWLIST_TRIAL_PREFIXES:
        return True
    return False


def is_allowlisted_latin_word(token: str) -> bool:
    """True if `token` (lowercase Latin word ≥4 chars) is on the
    allowlist of accepted loanwords, biology stems, or KB regimen
    vocabulary."""
    return bool(token) and token.lower() in PATIENT_ALLOWLIST_LATIN_WORDS


def expand_first_use(html: str) -> str:
    """Inject first-use expansions for `ABBREVIATION_FIRST_USE_UA` keys
    into a rendered patient HTML.

    Rule: the **first** unbracketed occurrence of each key in body
    prose is replaced with the expansion; subsequent occurrences stay
    bare. Idempotent — a sentinel HTML comment marks expanded bundles
    so re-renders (mode toggle, language switch) don't double-expand."""
    import re as _re

    sentinel = "<!-- abbrev-expanded -->"
    if sentinel in html:
        return html

    out = html
    for key, expansion in ABBREVIATION_FIRST_USE_UA.items():
        # `\b` plus a negative-lookbehind/ahead that excludes Latin
        # letters, Cyrillic letters, dashes, and digits — so `PD-1`
        # doesn't match inside `BCR-PD-1` and `MSI` doesn't match
        # inside `MSIH`.
        pattern = _re.compile(
            r"(?<![A-Za-zА-Яа-яЇїІіЄєҐґ\-])"
            + _re.escape(key)
            + r"(?![A-Za-zА-Яа-яЇїІіЄєҐґ0-9])"
        )
        m = pattern.search(out)
        if not m:
            continue
        # Replace only the first occurrence.
        out = out[:m.start()] + expansion + out[m.end():]
    return out + sentinel


def total_term_count() -> int:
    """Return total number of unique vocabulary entries across all categories.

    Used by tests to enforce the ≥200-entry coverage gate set in the
    patient-mode renderer spec."""
    return sum(len(t) for t in _ALL_TABLES)


__all__ = [
    "DRUG_CLASS_PLAIN_UA",
    "VARIANT_TYPE_PLAIN_UA",
    "ESCAT_PLAIN_UA",
    "NSZU_PLAIN_UA",
    "LAB_PLAIN_UA",
    "AE_PLAIN_UA",
    "SCREENING_PLAIN_UA",
    "ESCAT_TIER_PATIENT_LABEL",
    "NSZU_PATIENT_LABEL",
    "ABBREVIATION_FIRST_USE_UA",
    "PATIENT_ALLOWLIST_ACRONYMS",
    "PATIENT_ALLOWLIST_LATIN_WORDS",
    "PATIENT_ALLOWLIST_TRIAL_PREFIXES",
    "expand_first_use",
    "is_allowlisted_acronym",
    "is_allowlisted_latin_word",
    "explain",
    "total_term_count",
]
