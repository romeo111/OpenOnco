#!/usr/bin/env python3
"""Draft Ukrainian-language companion fields across the KB.

Goal: for every Biomarker, BiomarkerActionability, Disease, Regimen,
RedFlag, Indication YAML in `knowledge_base/hosted/content/`, fill the
missing UA companion field next to the EN source field:

    biomarkers              notes        -> notes_ua
    biomarker_actionability evidence_summary -> evidence_summary_ua
    diseases                notes        -> notes_ua
    regimens                notes        -> notes_ua
    redflags                notes        -> notes_ua
    indications             rationale    -> rationale_ua

Each drafted UA field is paired with two sibling marker keys:

    ukrainian_review_status: pending_clinical_signoff
    ukrainian_drafted_by: claude_extraction

Per CLAUDE.md and CHARTER §8.3 these markers make it explicit that the
UA text has NOT yet been clinically reviewed and must be verified by a
Ukrainian-speaking clinician before publication.

Idempotent: re-running the script on a previously processed YAML detects
the marker and skips. The script never overwrites a non-empty
existing UA companion field. The script never edits `names.ukrainian`,
`name_ua`, or `definition_ua` — those are already filled across the
codebase.

Translation strategy
--------------------
Dictionary-based phrase substitution. Drug names use established UA
pharmacopoeia transliterations where known. Gene/protein symbols
(BRAF, EGFR, NTRK, ALK) and trial acronyms (ECHELON-2, ALEX, CROWN)
stay in Latin. Dosing strings ("375 mg/m²") stay verbatim. Numbers,
percentages, year tags, ESCAT/OncoKB tier labels, NCCN categories and
HGVS variants stay verbatim. Anything the dictionary cannot resolve
is preserved as-is; reviewers see English text inline and can fix.

This is a DRAFT translation pipeline. It is explicitly NOT a substitute
for human clinical translation; the marker fields exist precisely so
the downstream review queue can find these entries.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString, FoldedScalarString

REPO = Path(__file__).resolve().parent.parent
KB = REPO / "knowledge_base" / "hosted" / "content"

# YAML files that fail to parse upstream (tracked separately, not our problem).
SKIP_FILES = {
    "indications/ind_breast_her2_pos_maint_trast.yaml",
    "indications/ind_breast_hr_pos_maint_cdk46i.yaml",
    "indications/ind_nsclc_alk_maint_alectinib.yaml",
}

# (entity_dir, en_field, ua_field) tuples. Order matters for reporting only.
ENTITY_PLAN = [
    ("biomarkers", "notes", "notes_ua"),
    ("biomarker_actionability", "evidence_summary", "evidence_summary_ua"),
    ("diseases", "notes", "notes_ua"),
    ("regimens", "notes", "notes_ua"),
    ("redflags", "notes", "notes_ua"),
    ("indications", "rationale", "rationale_ua"),
]

MARKER_STATUS = "pending_clinical_signoff"
MARKER_AUTHOR = "claude_extraction"

# ── Translation dictionary ─────────────────────────────────────────────
# Order matters: longer phrases first (we apply them in the order given,
# so a multi-word phrase replaces before its component words). Compiled
# into a single regex with word boundaries. All keys are lowercase; we
# preserve original casing on a best-effort basis (sentence-initial
# capitalization is restored after substitution).

# Stock medical / oncology phrases. Authored from the KB corpus — every
# entry here was observed in the EN text we are translating.
PHRASES: list[tuple[str, str]] = [
    # Multi-word phrases (apply before single words)
    ("standard of care", "стандарт лікування"),
    ("first-line", "перша лінія"),
    ("second-line", "друга лінія"),
    ("third-line", "третя лінія"),
    ("front-line", "перша лінія"),
    ("frontline", "перша лінія"),
    ("upfront", "перша лінія"),
    ("relapsed/refractory", "рецидивний/рефрактерний"),
    ("relapsed or refractory", "рецидивний або рефрактерний"),
    ("relapsed and refractory", "рецидивний та рефрактерний"),
    ("r/r", "р/р"),
    ("relapsed", "рецидивний"),
    ("refractory", "рефрактерний"),
    ("treatment-naive", "без попереднього лікування"),
    ("treatment-naïve", "без попереднього лікування"),
    ("treatment naive", "без попереднього лікування"),
    ("newly diagnosed", "вперше діагностований"),
    ("previously untreated", "раніше нелікований"),
    ("previously treated", "раніше лікований"),
    ("complete response", "повна відповідь"),
    ("partial response", "часткова відповідь"),
    ("overall response rate", "загальна частота відповіді"),
    ("overall survival", "загальна виживаність"),
    ("progression-free survival", "виживаність без прогресування"),
    ("disease-free survival", "виживаність без хвороби"),
    ("event-free survival", "виживаність без подій"),
    ("median pfs", "медіана ВБП"),
    ("median os", "медіана ЗВ"),
    ("median dor", "медіана DOR"),
    ("median follow-up", "медіана спостереження"),
    ("hazard ratio", "відношення ризиків"),
    ("dose reduction", "зниження дози"),
    ("dose adjustment", "корекція дози"),
    ("dose-limiting toxicity", "доза-лімітуюча токсичність"),
    ("adverse event", "небажане явище"),
    ("adverse events", "небажані явища"),
    ("side effect", "побічний ефект"),
    ("side effects", "побічні ефекти"),
    ("drug-drug interaction", "лікарська взаємодія"),
    ("drug interactions", "лікарські взаємодії"),
    ("clinical trial", "клінічне дослідження"),
    ("clinical trials", "клінічні дослідження"),
    ("phase 3", "фаза 3"),
    ("phase 2", "фаза 2"),
    ("phase 1", "фаза 1"),
    ("phase iii", "фаза 3"),
    ("phase ii", "фаза 2"),
    ("phase i", "фаза 1"),
    ("randomized controlled trial", "рандомізоване контрольоване дослідження"),
    ("rct", "РКД"),
    ("real-world", "реальна клінічна практика"),
    ("post-hoc", "post-hoc"),
    ("subgroup analysis", "аналіз підгруп"),
    ("interim analysis", "проміжний аналіз"),
    ("primary endpoint", "первинна кінцева точка"),
    ("secondary endpoint", "вторинна кінцева точка"),
    ("biomarker-driven", "на основі біомаркерів"),
    ("targeted therapy", "таргетна терапія"),
    ("immune checkpoint inhibitor", "інгібітор контрольних точок імунітету"),
    ("immune checkpoint inhibitors", "інгібітори контрольних точок імунітету"),
    ("checkpoint inhibitor", "інгібітор контрольних точок"),
    ("immunotherapy", "імунотерапія"),
    ("chemotherapy", "хіміотерапія"),
    ("chemoimmunotherapy", "хіміоімунотерапія"),
    ("radiotherapy", "променева терапія"),
    ("radiation therapy", "променева терапія"),
    ("chemoradiation", "хіміопроменева терапія"),
    ("chemoradiotherapy", "хіміопроменева терапія"),
    ("autologous stem cell transplant", "аутологічна трансплантація стовбурових клітин"),
    ("allogeneic stem cell transplant", "алогенна трансплантація стовбурових клітин"),
    ("stem cell transplant", "трансплантація стовбурових клітин"),
    ("bone marrow", "кістковий мозок"),
    ("peripheral blood", "периферична кров"),
    ("lymph node", "лімфатичний вузол"),
    ("lymph nodes", "лімфатичні вузли"),
    ("lymph-node", "лімфатичний вузол"),
    ("tumor burden", "пухлинне навантаження"),
    ("tumor lysis syndrome", "синдром лізису пухлини"),
    ("cytokine release syndrome", "синдром вивільнення цитокінів"),
    ("graft-versus-host disease", "реакція трансплантат-проти-господаря"),
    ("graft vs host disease", "реакція трансплантат-проти-господаря"),
    ("non-inferior", "не гірше"),
    ("non-inferiority", "не гірше"),
    ("superior to", "перевершує"),
    ("comparable to", "співставний з"),
    ("inferior to", "поступається"),
    ("approved for", "схвалений для"),
    ("fda-approved", "схвалений FDA"),
    ("ema-approved", "схвалений EMA"),
    ("ukraine-approved", "зареєстрований в Україні"),
    ("guidelines recommend", "настанови рекомендують"),
    ("nccn-recommended", "рекомендований NCCN"),
    ("nccn-listed", "включений до NCCN"),
    ("nccn-preferred", "віддається перевага NCCN"),
    ("esmo-recommended", "рекомендований ESMO"),
    ("category 1", "категорія 1"),
    ("category 2a", "категорія 2A"),
    ("category 2b", "категорія 2B"),
    ("category 3", "категорія 3"),
    ("level of evidence", "рівень доказовості"),
    ("evidence level", "рівень доказовості"),
    ("level 1", "рівень 1"),
    ("level 2", "рівень 2"),
    ("escat ia", "ESCAT IA"),
    ("escat ib", "ESCAT IB"),
    ("escat iia", "ESCAT IIA"),
    ("escat iib", "ESCAT IIB"),
    ("escat iiia", "ESCAT IIIA"),
    ("escat iiib", "ESCAT IIIB"),
    ("escat iv", "ESCAT IV"),
    ("escat x", "ESCAT X"),
    ("oncokb level 1", "OncoKB рівень 1"),
    ("oncokb level 2", "OncoKB рівень 2"),
    ("oncokb level 3a", "OncoKB рівень 3A"),
    ("oncokb level 3b", "OncoKB рівень 3B"),
    ("oncokb level 4", "OncoKB рівень 4"),
    ("hallmark of", "патогномонічна ознака"),
    ("driver mutation", "драйверна мутація"),
    ("activating mutation", "активуюча мутація"),
    ("loss-of-function", "втрата функції"),
    ("gain-of-function", "посилення функції"),
    ("loss of function", "втрата функції"),
    ("gain of function", "посилення функції"),
    ("germline", "герміногенний"),
    ("somatic", "соматичний"),
    ("missense", "місенс"),
    ("nonsense", "нонсенс"),
    ("frameshift", "зсув рамки"),
    ("indel", "indel"),
    ("amplification", "ампліфікація"),
    ("deletion", "делеція"),
    ("translocation", "транслокація"),
    ("rearrangement", "перебудова"),
    ("rearranged", "перебудований"),
    ("fusion", "злиття"),
    ("copy number", "кількість копій"),
    ("methylation", "метилювання"),
    ("expression", "експресія"),
    ("overexpression", "гіперекспресія"),
    ("loss of expression", "втрата експресії"),
    ("immunohistochemistry", "імуногістохімія"),
    ("flow cytometry", "проточна цитометрія"),
    ("next-generation sequencing", "секвенування нового покоління"),
    ("ngs", "NGS"),
    ("liquid biopsy", "рідинна біопсія"),
    ("ctdna", "цоДНК"),
    ("circulating tumor dna", "циркулююча пухлинна ДНК"),
    ("minimal residual disease", "мінімальна залишкова хвороба"),
    ("measurable residual disease", "вимірювана залишкова хвороба"),
    ("mrd", "МЗХ"),
    ("autologous", "аутологічний"),
    ("allogeneic", "алогенний"),
    ("autosct", "аутоТГСК"),
    ("allosct", "алоТГСК"),
    ("car-t", "CAR-T"),
    ("car t-cell", "CAR-T-клітинна"),
    ("bispecific", "біспецифічний"),
    ("monoclonal antibody", "моноклональне антитіло"),
    ("antibody-drug conjugate", "кон'югат антитіло-препарат"),
    ("adc", "ADC"),
    ("indolent", "індолентний"),
    ("aggressive", "агресивний"),
    ("high-grade", "високого ступеня"),
    ("low-grade", "низького ступеня"),
    ("intermediate-grade", "проміжного ступеня"),
    ("high-risk", "високого ризику"),
    ("low-risk", "низького ризику"),
    ("intermediate-risk", "проміжного ризику"),
    ("standard-risk", "стандартного ризику"),
    ("favorable-risk", "сприятливого ризику"),
    ("favorable", "сприятливий"),
    ("adverse", "несприятливий"),
    ("unfavorable", "несприятливий"),
    ("durable response", "стійка відповідь"),
    ("durable remission", "стійка ремісія"),
    ("complete remission", "повна ремісія"),
    ("partial remission", "часткова ремісія"),
    ("stable disease", "стабілізація хвороби"),
    ("progressive disease", "прогресування хвороби"),
    ("disease progression", "прогресування хвороби"),
    ("disease control", "контроль хвороби"),
    ("watch and wait", "спостереження"),
    ("watchful waiting", "спостережна тактика"),
    ("active surveillance", "активне спостереження"),
    ("performance status", "функціональний статус"),
    ("frailty", "дряхлість"),
    ("comorbidity", "коморбідність"),
    ("comorbidities", "коморбідності"),
    ("renal impairment", "ниркова недостатність"),
    ("hepatic impairment", "печінкова недостатність"),
    ("liver function", "функція печінки"),
    ("kidney function", "функція нирок"),
    ("creatinine clearance", "кліренс креатиніну"),
    ("bone marrow biopsy", "трепанобіопсія кісткового мозку"),
    ("excisional biopsy", "ексцизійна біопсія"),
    ("core needle biopsy", "трепанобіопсія"),
    ("fine needle aspiration", "тонкоголкова аспіраційна біопсія"),
    ("excision", "ексцизія"),
    ("staging", "стадіювання"),
    ("re-staging", "рестадіювання"),
    ("workup", "обстеження"),
    ("work-up", "обстеження"),
    ("baseline", "базове"),
    ("at baseline", "на старті"),
    ("at presentation", "при зверненні"),
    ("at diagnosis", "при діагнозі"),
    ("median age", "медіанний вік"),
    ("years old", "років"),
    ("aged", "віком"),
    ("elderly", "літнього віку"),
    ("pediatric", "педіатричний"),
    ("adult", "дорослий"),
    ("pregnant", "вагітна"),
    ("pregnancy", "вагітність"),
    ("breast-feeding", "грудне вигодовування"),
    ("breastfeeding", "грудне вигодовування"),
    ("transplant-eligible", "придатний до трансплантації"),
    ("transplant-ineligible", "непридатний до трансплантації"),
    ("fit for", "придатний до"),
    ("unfit for", "непридатний до"),
    ("ineligible for", "непридатний для"),
    ("eligible for", "придатний для"),
    ("contraindicated", "протипоказаний"),
    ("contraindication", "протипоказання"),
    ("maintenance therapy", "підтримуюча терапія"),
    ("induction therapy", "індукційна терапія"),
    ("consolidation therapy", "консолідуюча терапія"),
    ("salvage therapy", "сальвадж-терапія"),
    ("bridging therapy", "бриджингова терапія"),
    ("neoadjuvant", "неоад'ювантний"),
    ("adjuvant", "ад'ювантний"),
    ("palliative", "паліативний"),
    ("supportive care", "підтримуюче лікування"),
    ("best supportive care", "найкраще підтримуюче лікування"),
    ("clinical practice", "клінічна практика"),
    ("real-world data", "дані реальної практики"),
    ("real world data", "дані реальної практики"),
    ("prognosis", "прогноз"),
    ("prognostic", "прогностичний"),
    ("predictive", "предиктивний"),
    ("survival benefit", "виграш у виживаності"),
    ("survival outcome", "результат виживаності"),
    ("life expectancy", "очікувана тривалість життя"),
    ("toxicity profile", "профіль токсичності"),
    ("safety profile", "профіль безпеки"),
    ("efficacy", "ефективність"),
    ("tolerability", "переносимість"),
    ("infusion reaction", "інфузійна реакція"),
    ("hypersensitivity", "гіперчутливість"),
    ("anaphylaxis", "анафілаксія"),
    ("nausea and vomiting", "нудота і блювання"),
    ("diarrhea", "діарея"),
    ("mucositis", "мукозит"),
    ("alopecia", "алопеція"),
    ("neutropenia", "нейтропенія"),
    ("thrombocytopenia", "тромбоцитопенія"),
    ("anemia", "анемія"),
    ("febrile neutropenia", "фебрильна нейтропенія"),
    ("cytopenia", "цитопенія"),
    ("cytopenias", "цитопенії"),
    ("hepatotoxicity", "гепатотоксичність"),
    ("nephrotoxicity", "нефротоксичність"),
    ("cardiotoxicity", "кардіотоксичність"),
    ("neuropathy", "нейропатія"),
    ("peripheral neuropathy", "периферична нейропатія"),
    ("rash", "висип"),
    ("hypertension", "гіпертензія"),
    ("hyperglycemia", "гіперглікемія"),
    ("immune-related", "імуноасоційований"),
    ("immune related", "імуноасоційований"),
    ("autoimmune", "автоімунний"),
    ("biomarker", "біомаркер"),
    ("biomarkers", "біомаркери"),
    ("mutation", "мутація"),
    ("mutations", "мутації"),
    ("variant", "варіант"),
    ("variants", "варіанти"),
    ("alteration", "альтерація"),
    ("alterations", "альтерації"),
    ("co-occurring", "співіснуючий"),
    ("co-occurrence", "співіснування"),
    ("co-mutation", "ко-мутація"),
    ("compound mutation", "компаундна мутація"),
    ("resistance mutation", "резистентна мутація"),
    ("resistance to", "резистентність до"),
    ("acquired resistance", "набута резистентність"),
    ("primary resistance", "первинна резистентність"),
    ("intrinsic resistance", "вроджена резистентність"),
    ("sensitive to", "чутливий до"),
    ("sensitivity", "чутливість"),
    ("specificity", "специфічність"),
    ("selective", "селективний"),
    ("non-selective", "неселективний"),
    ("irreversible", "необоротний"),
    ("reversible", "оборотний"),
    ("first-generation", "першого покоління"),
    ("second-generation", "другого покоління"),
    ("third-generation", "третього покоління"),
    ("fourth-generation", "четвертого покоління"),
    ("next-generation", "наступного покоління"),
    ("monotherapy", "монотерапія"),
    ("combination therapy", "комбінована терапія"),
    ("combination", "комбінація"),
    ("regimen", "схема"),
    ("regimens", "схеми"),
    ("backbone", "основа схеми"),
    ("doublet", "дублет"),
    ("triplet", "триплет"),
    ("response rate", "частота відповіді"),
    ("response duration", "тривалість відповіді"),
    ("duration of response", "тривалість відповіді"),
    ("cns penetration", "проникнення в ЦНС"),
    ("cns activity", "активність в ЦНС"),
    ("blood-brain barrier", "гематоенцефалічний бар'єр"),
    ("brain metastasis", "метастаз у мозок"),
    ("brain metastases", "метастази в мозок"),
    ("leptomeningeal disease", "лептоменінгеальне ураження"),
    ("metastatic", "метастатичний"),
    ("locally advanced", "місцево-поширений"),
    ("advanced", "поширений"),
    ("early-stage", "ранньої стадії"),
    ("limited-stage", "обмеженої стадії"),
    ("extensive-stage", "поширеної стадії"),
    ("operable", "операбельний"),
    ("inoperable", "неоперабельний"),
    ("resectable", "резектабельний"),
    ("unresectable", "нерезектабельний"),
    ("recurrent", "рецидивний"),
    ("recurrence", "рецидив"),
    ("relapse", "рецидив"),
    ("regression", "регресія"),
    ("remission", "ремісія"),
    ("transformation", "трансформація"),
    ("transformed", "трансформований"),
    # treatment-decision phrasing
    ("treatment of choice", "терапія вибору"),
    ("treatment choice", "вибір терапії"),
    ("preferred regimen", "переважна схема"),
    ("alternative regimen", "альтернативна схема"),
    ("preferred option", "переважний варіант"),
    ("alternative option", "альтернативний варіант"),
    ("evidence-based", "доказовий"),
    ("evidence base", "доказова база"),
    ("guideline-based", "на основі настанов"),
    ("clinically meaningful", "клінічно значущий"),
    ("statistically significant", "статистично значущий"),
    ("not statistically significant", "статистично незначущий"),
    ("acceptable toxicity", "прийнятна токсичність"),
    ("manageable", "контрольований"),
    ("well-tolerated", "добре переноситься"),
    ("poorly tolerated", "погано переноситься"),
    ("standard", "стандарт"),
    ("standard regimen", "стандартна схема"),
    ("backbone regimen", "базова схема"),
    ("trial-eligible", "придатний для дослідження"),
    ("clinical trial enrollment", "включення в клінічне дослідження"),
    ("national guidelines", "національні настанови"),
    ("ukrainian guidelines", "українські настанови"),
    ("ukrainian moh", "МОЗ України"),
    ("moh ukraine", "МОЗ України"),
    ("ministry of health", "Міністерство охорони здоров'я"),
    ("nszu", "НСЗУ"),
    ("reimbursed", "відшкодовуваний"),
    ("reimbursement", "відшкодування"),
    ("not reimbursed", "не відшкодовується"),
    ("self-pay", "самооплата"),
    ("out-of-pocket", "із власних коштів"),
    ("access pathway", "шлях доступу"),
    # disease shorthands
    ("acute myeloid leukemia", "гострий мієлоїдний лейкоз"),
    ("acute lymphoblastic leukemia", "гострий лімфобластний лейкоз"),
    ("acute promyelocytic leukemia", "гострий промієлоцитарний лейкоз"),
    ("chronic myeloid leukemia", "хронічний мієлоїдний лейкоз"),
    ("chronic lymphocytic leukemia", "хронічний лімфоцитарний лейкоз"),
    ("multiple myeloma", "множинна мієлома"),
    ("hodgkin lymphoma", "лімфома Ходжкіна"),
    ("non-hodgkin lymphoma", "неходжкінська лімфома"),
    ("diffuse large b-cell lymphoma", "дифузна B-великоклітинна лімфома"),
    ("follicular lymphoma", "фолікулярна лімфома"),
    ("mantle cell lymphoma", "лімфома з клітин мантійної зони"),
    ("marginal zone lymphoma", "лімфома маргінальної зони"),
    ("burkitt lymphoma", "лімфома Беркіта"),
    ("hairy cell leukemia", "волосатоклітинний лейкоз"),
    ("waldenstrom macroglobulinemia", "макроглобулінемія Вальденстрема"),
    ("anaplastic large cell lymphoma", "анапластична великоклітинна лімфома"),
    ("angioimmunoblastic t-cell lymphoma", "ангіоімунобластна T-клітинна лімфома"),
    ("peripheral t-cell lymphoma", "периферична T-клітинна лімфома"),
    ("cutaneous t-cell lymphoma", "шкірна T-клітинна лімфома"),
    ("breast cancer", "рак молочної залози"),
    ("lung cancer", "рак легені"),
    ("non-small cell lung cancer", "недрібноклітинний рак легені"),
    ("small cell lung cancer", "дрібноклітинний рак легені"),
    ("colorectal cancer", "колоректальний рак"),
    ("pancreatic cancer", "рак підшлункової залози"),
    ("prostate cancer", "рак передміхурової залози"),
    ("ovarian cancer", "рак яєчника"),
    ("cervical cancer", "рак шийки матки"),
    ("endometrial cancer", "рак ендометрію"),
    ("renal cell carcinoma", "нирковоклітинна карцинома"),
    ("hepatocellular carcinoma", "гепатоцелюлярна карцинома"),
    ("gastric cancer", "рак шлунка"),
    ("esophageal cancer", "рак стравоходу"),
    ("bladder cancer", "рак сечового міхура"),
    ("urothelial carcinoma", "уротеліальна карцинома"),
    ("melanoma", "меланома"),
    ("glioblastoma", "гліобластома"),
    # short single-word fallback (lowercased)
    ("approved", "схвалений"),
    ("approval", "схвалення"),
    ("indication", "показання"),
    ("indications", "показання"),
    ("dose", "доза"),
    ("dosing", "дозування"),
    ("schedule", "схема"),
    ("cycle", "цикл"),
    ("cycles", "цикли"),
    ("induction", "індукція"),
    ("consolidation", "консолідація"),
    ("maintenance", "підтримка"),
    ("salvage", "сальвадж"),
    ("response", "відповідь"),
    ("survival", "виживаність"),
    ("toxicity", "токсичність"),
    ("safety", "безпека"),
    ("efficacy", "ефективність"),
    ("biopsy", "біопсія"),
    ("histology", "гістологія"),
    ("morphology", "морфологія"),
    ("phenotype", "фенотип"),
    ("genotype", "генотип"),
    ("subtype", "підтип"),
    ("subtypes", "підтипи"),
    ("entity", "сутність"),
    ("disease", "хвороба"),
    ("tumor", "пухлина"),
    ("tumour", "пухлина"),
    ("cancer", "рак"),
    ("malignancy", "злоякісне новоутворення"),
    ("lymphoma", "лімфома"),
    ("leukemia", "лейкоз"),
    ("leukaemia", "лейкоз"),
    ("myeloma", "мієлома"),
    ("carcinoma", "карцинома"),
    ("sarcoma", "саркома"),
    ("metastasis", "метастаз"),
    ("metastases", "метастази"),
    ("relapse", "рецидив"),
    ("progression", "прогресування"),
    ("treatment", "лікування"),
    ("therapy", "терапія"),
    ("therapeutic", "терапевтичний"),
    ("regimen", "схема"),
    ("trial", "дослідження"),
    ("study", "дослідження"),
    ("studies", "дослідження"),
    ("data", "дані"),
    ("evidence", "докази"),
    ("guideline", "настанова"),
    ("guidelines", "настанови"),
    ("recommendation", "рекомендація"),
    ("recommendations", "рекомендації"),
    ("recommended", "рекомендований"),
    ("indication", "показання"),
    ("contraindication", "протипоказання"),
    ("monitoring", "моніторинг"),
    ("surveillance", "спостереження"),
    ("follow-up", "спостереження"),
    ("biomarker", "біомаркер"),
    ("variant", "варіант"),
    ("mutation", "мутація"),
    ("fusion", "злиття"),
    ("amplification", "ампліфікація"),
    ("deletion", "делеція"),
    ("expression", "експресія"),
    ("germline", "герміногенний"),
    ("somatic", "соматичний"),
    ("pathogenic", "патогенний"),
    ("benign", "доброякісний"),
    ("vus", "VUS"),
    ("hereditary", "спадковий"),
    ("acquired", "набутий"),
    ("rare", "рідкісний"),
    ("common", "поширений"),
    ("frequent", "частий"),
    ("infrequent", "нечастий"),
    ("required", "обов'язковий"),
    ("desired", "бажаний"),
    ("optional", "опціональний"),
    ("mandatory", "обов'язковий"),
    ("preferred", "переважний"),
    ("acceptable", "прийнятний"),
    ("inferior", "поступається"),
    ("superior", "перевершує"),
    ("equivalent", "еквівалентний"),
    ("comparable", "співставний"),
    ("similar", "подібний"),
    ("different", "відмінний"),
    ("emerging", "новий"),
    ("established", "усталений"),
    ("investigational", "експериментальний"),
    ("experimental", "експериментальний"),
    ("off-label", "off-label"),
    ("on-label", "за показаннями"),
    ("on label", "за показаннями"),
    # logical/narrative connectors common in this corpus
    ("see ", "див. "),
    (" vs ", " проти "),
    (" vs. ", " проти "),
    (" or ", " або "),
    (" and ", " та "),
    (" with ", " з "),
    (" without ", " без "),
    (" after ", " після "),
    (" before ", " до "),
    (" during ", " під час "),
    (" prior to ", " до "),
    (" until ", " до "),
    (" while ", " тоді як "),
    (" however", ", однак"),
    (" therefore", ", тому"),
    (" thus", ", таким чином"),
    (" hence", ", отже"),
    (" because ", " тому що "),
    (" since ", " оскільки "),
    (" although ", " хоча "),
    (" despite ", " попри "),
    # MISC short tokens
    ("yes", "так"),
    ("no", "ні"),
    # Critical extras — second pass after sample testing
    ("bispecific t-cell engager", "біспецифічний T-клітинний активатор"),
    ("t-cell engager", "T-клітинний активатор"),
    ("post-induction", "після індукції"),
    ("post-resection", "після резекції"),
    ("post-transplant", "після трансплантації"),
    ("post-therapy", "після терапії"),
    ("complete mrd response", "повна МЗХ-відповідь"),
    ("partial mrd response", "часткова МЗХ-відповідь"),
    ("mrd response", "МЗХ-відповідь"),
    ("mrd+", "МЗХ+"),
    ("mrd-", "МЗХ-"),
    ("mrd negative", "МЗХ-негативний"),
    ("mrd positive", "МЗХ-позитивний"),
    ("ph-", "Ph-"),
    ("ph+", "Ph+"),
    ("ph negative", "Ph-негативний"),
    ("ph positive", "Ph-позитивний"),
    ("continuous iv", "тривала в/в інфузія"),
    ("continuous infusion", "тривала інфузія"),
    ("hospitalization", "госпіталізація"),
    ("limit accessibility", "обмежують доступність"),
    ("limits accessibility", "обмежує доступність"),
    ("boxed warning", "спеціальне попередження в інструкції"),
    ("boxed warnings", "спеціальні попередження в інструкції"),
    ("icu support", "підтримка у відділенні інтенсивної терапії"),
    ("intensive care unit", "відділення інтенсивної терапії"),
    ("targetable with", "таргетується"),
    ("targeted by", "таргетується"),
    ("defining feature", "визначальна ознака"),
    ("defining feature of", "визначальна ознака"),
    ("hallmark of", "патогномонічна ознака"),
    ("inhibitor", "інгібітор"),
    ("inhibitors", "інгібітори"),
    ("agonist", "агоніст"),
    ("antagonist", "антагоніст"),
    ("modulator", "модулятор"),
    ("activator", "активатор"),
    ("enhancer", "підсилювач"),
    ("blocker", "блокатор"),
    ("when ", "коли "),
    ("if ", "якщо "),
    (" fails", " неефективний"),
    (" fail", " неефективні"),
    ("outperform", "перевершує"),
    ("outperforms", "перевершує"),
    ("highest", "найвища"),
    ("lowest", "найнижча"),
    ("best", "найкращий"),
    ("worst", "найгірший"),
    ("most", "найбільш"),
    ("least", "найменш"),
    ("better", "краще"),
    ("worse", "гірше"),
    ("improves", "покращує"),
    ("improved", "покращений"),
    ("improvement", "покращення"),
    ("worsens", "погіршує"),
    ("worsened", "погіршений"),
    ("decline", "зниження"),
    ("declines", "знижується"),
    ("rise", "підвищення"),
    ("rises", "підвищується"),
    ("increase", "збільшення"),
    ("increases", "збільшує"),
    ("decrease", "зменшення"),
    ("decreases", "зменшує"),
    ("reduce", "зменшити"),
    ("reduces", "зменшує"),
    ("reduced", "зменшений"),
    ("reduction", "зниження"),
    ("benefit", "виграш"),
    ("benefits", "виграш"),
    ("not been shown", "не показано"),
    ("not shown", "не показано"),
    ("shown to", "продемонстровано"),
    ("demonstrated", "продемонстровано"),
    ("evidence shows", "докази свідчать"),
    ("data shows", "дані свідчать"),
    ("studies show", "дослідження показують"),
    ("appears to", "здається"),
    ("seem to", "здаються"),
    ("typically", "типово"),
    ("usually", "зазвичай"),
    ("often", "часто"),
    ("rarely", "рідко"),
    ("frequently", "часто"),
    ("commonly", "часто"),
    ("predominantly", "переважно"),
    ("primarily", "перш за все"),
    ("notably", "примітно"),
    ("specifically", "зокрема"),
    ("particularly", "особливо"),
    ("especially", "особливо"),
    ("generally", "загалом"),
    ("approximately", "приблизно"),
    ("roughly", "приблизно"),
    ("about ", "приблизно "),
    ("median", "медіана"),
    ("mean", "середнє"),
    ("range", "діапазон"),
    ("estimate", "оцінка"),
    ("estimated", "оцінений"),
    ("at least", "щонайменше"),
    ("at most", "щонайбільше"),
    ("up to", "до"),
    ("more than", "більше ніж"),
    ("less than", "менше ніж"),
    ("between", "між"),
    ("among", "серед"),
    # Treatment/clinical actions
    ("administer", "призначати"),
    ("administered", "призначений"),
    ("administration", "введення"),
    ("withhold", "відмінити"),
    ("withheld", "відмінений"),
    ("discontinue", "припинити"),
    ("discontinued", "припинений"),
    ("discontinuation", "припинення"),
    ("hold", "утримати"),
    ("held", "утримано"),
    ("resume", "відновити"),
    ("resumed", "відновлений"),
    ("escalate", "інтенсифікувати"),
    ("de-escalate", "деескалувати"),
    ("rebiopsy", "повторна біопсія"),
    ("biopsy-confirmed", "підтверджено біопсією"),
    ("histologically confirmed", "гістологічно підтверджений"),
    ("histopathologically", "гістопатологічно"),
    ("pathologic", "патологічний"),
    ("pathology", "патологія"),
    ("diagnosis", "діагноз"),
    ("diagnostic", "діагностичний"),
    ("differential diagnosis", "диференціальний діагноз"),
    ("rule out", "виключити"),
    ("rule in", "підтвердити"),
    ("workup includes", "обстеження включає"),
    ("must include", "має включати"),
    ("should include", "повинно включати"),
    ("includes", "включає"),
    ("including", "включаючи"),
    ("excluding", "виключаючи"),
    ("excludes", "виключає"),
    # Statistical / outcomes phrasing
    ("estimated 5y os", "розрахункова 5-річна ЗВ"),
    ("5-year os", "5-річна ЗВ"),
    ("5y os", "5-річна ЗВ"),
    ("5y pfs", "5-річна ВБП"),
    ("3y pfs", "3-річна ВБП"),
    ("2y pfs", "2-річна ВБП"),
    ("1y pfs", "1-річна ВБП"),
    ("5-yr os", "5-річна ЗВ"),
    ("5-yr pfs", "5-річна ВБП"),
    ("5-yr", "5-річна"),
    ("3-yr", "3-річна"),
    ("2-yr", "2-річна"),
    ("yrs", "роки"),
    ("yr", "рік"),
    (" mo ", " міс. "),
    (" mos ", " міс. "),
    (" months ", " місяців "),
    (" months.", " місяців."),
    (" mo)", " міс.)"),
    (" mo,", " міс.,"),
    (" mo;", " міс.;"),
    # last-resort fillers
    ("limited evidence", "обмежені докази"),
    ("strong evidence", "сильні докази"),
    ("weak evidence", "слабкі докази"),
]

# Drug-name transliterations (UA pharmacopoeia where established).
# These apply BEFORE phrase substitutions so phrasing logic doesn't
# mangle them. Keys lowercased; preserves capitalization heuristically.
DRUGS: dict[str, str] = {
    "venetoclax": "венетоклакс",
    "selpercatinib": "селперкатиніб",
    "ibrutinib": "ібрутиніб",
    "acalabrutinib": "акалабрутиніб",
    "zanubrutinib": "занубрутиніб",
    "rituximab": "ритуксимаб",
    "obinutuzumab": "обінутузумаб",
    "ofatumumab": "офатумумаб",
    "bendamustine": "бендамустин",
    "fludarabine": "флударабін",
    "cyclophosphamide": "циклофосфамід",
    "doxorubicin": "доксорубіцин",
    "vincristine": "вінкристин",
    "vinblastine": "вінбластин",
    "etoposide": "етопозид",
    "cytarabine": "цитарабін",
    "methotrexate": "метотрексат",
    "ifosfamide": "іфосфамід",
    "carboplatin": "карбоплатин",
    "cisplatin": "цисплатин",
    "oxaliplatin": "оксаліплатин",
    "5-fluorouracil": "5-фторурацил",
    "fluorouracil": "фторурацил",
    "capecitabine": "капецитабін",
    "gemcitabine": "гемцитабін",
    "paclitaxel": "паклітаксел",
    "docetaxel": "доцетаксел",
    "nab-paclitaxel": "наб-паклітаксел",
    "trastuzumab": "трастузумаб",
    "pertuzumab": "пертузумаб",
    "trastuzumab deruxtecan": "трастузумаб дерукстекан",
    "trastuzumab emtansine": "трастузумаб емтанзин",
    "tdm-1": "T-DM1",
    "t-dxd": "T-DXd",
    "bevacizumab": "бевацизумаб",
    "cetuximab": "цетуксимаб",
    "panitumumab": "панітумумаб",
    "ramucirumab": "рамуцирумаб",
    "atezolizumab": "атезолізумаб",
    "pembrolizumab": "пембролізумаб",
    "nivolumab": "ніволумаб",
    "ipilimumab": "іпілімумаб",
    "durvalumab": "дурвалумаб",
    "avelumab": "авелумаб",
    "cemiplimab": "цеміплімаб",
    "imatinib": "іматиніб",
    "dasatinib": "дазатиніб",
    "nilotinib": "нілотиніб",
    "bosutinib": "бозутиніб",
    "ponatinib": "понатиніб",
    "asciminib": "асциминіб",
    "midostaurin": "мідостаурин",
    "gilteritinib": "гілтеритиніб",
    "quizartinib": "квізартиніб",
    "ivosidenib": "івосиденіб",
    "enasidenib": "енасиденіб",
    "azacitidine": "азацитидин",
    "decitabine": "децитабін",
    "lenalidomide": "леналідомід",
    "pomalidomide": "помалідомід",
    "thalidomide": "талідомід",
    "bortezomib": "бортезоміб",
    "carfilzomib": "карфілзоміб",
    "ixazomib": "іксазоміб",
    "daratumumab": "даратумумаб",
    "isatuximab": "ізатуксимаб",
    "elotuzumab": "елотузумаб",
    "blinatumomab": "блінатумомаб",
    "inotuzumab ozogamicin": "інотузумаб озогаміцин",
    "brentuximab vedotin": "брентуксимаб ведотин",
    "polatuzumab vedotin": "полатузумаб ведотин",
    "loncastuximab tesirine": "лонкастуксимаб тезирін",
    "tafasitamab": "тафаситамаб",
    "selinexor": "селінексор",
    "tisagenlecleucel": "тисагенлеклеуцел",
    "axicabtagene ciloleucel": "аксикабтаген цилолейцел",
    "lisocabtagene maraleucel": "лісокабтаген маралейцел",
    "brexucabtagene autoleucel": "брексукабтаген аутолейцел",
    "ciltacabtagene autoleucel": "цилтакабтаген аутолейцел",
    "idecabtagene vicleucel": "ідекабтаген віклеуцел",
    "vemurafenib": "вемурафеніб",
    "dabrafenib": "дабрафеніб",
    "encorafenib": "енкорафеніб",
    "trametinib": "траметиніб",
    "cobimetinib": "кобіметиніб",
    "binimetinib": "біниметиніб",
    "alectinib": "алектиніб",
    "lorlatinib": "лорлатиніб",
    "brigatinib": "брігатиніб",
    "crizotinib": "кризотиніб",
    "ceritinib": "цертиніб",
    "ensartinib": "ензартиніб",
    "gefitinib": "гефітиніб",
    "erlotinib": "ерлотиніб",
    "afatinib": "афатиніб",
    "dacomitinib": "дакомітиніб",
    "osimertinib": "осимертиніб",
    "amivantamab": "амівантамаб",
    "lazertinib": "лазертиніб",
    "mobocertinib": "мобоцертиніб",
    "sotorasib": "соторасиб",
    "adagrasib": "адаграсиб",
    "larotrectinib": "ларотрексиніб",
    "entrectinib": "ентректиніб",
    "repotrectinib": "репотректиніб",
    "selumetinib": "селуметиніб",
    "tepotinib": "тепотиніб",
    "capmatinib": "капматиніб",
    "savolitinib": "саволітиніб",
    "pralsetinib": "пралсетиніб",
    "olaparib": "олапариб",
    "rucaparib": "рукапариб",
    "niraparib": "нірапариб",
    "talazoparib": "талазопариб",
    "abemaciclib": "абемациклиб",
    "palbociclib": "палбоциклиб",
    "ribociclib": "рибоциклиб",
    "alpelisib": "алпелісиб",
    "everolimus": "еверолімус",
    "temsirolimus": "темсиролімус",
    "sirolimus": "сиролімус",
    "fulvestrant": "фулвестрант",
    "tamoxifen": "тамоксифен",
    "letrozole": "летрозол",
    "anastrozole": "анастрозол",
    "exemestane": "екземестан",
    "abiraterone": "абіратерон",
    "enzalutamide": "ензалутамід",
    "apalutamide": "апалутамід",
    "darolutamide": "даролутамід",
    "leuprolide": "леупролід",
    "goserelin": "гозерелін",
    "degarelix": "дегарелікс",
    "sorafenib": "сорафеніб",
    "sunitinib": "сунитиніб",
    "pazopanib": "пазопаніб",
    "axitinib": "акситиніб",
    "cabozantinib": "кабозантиніб",
    "lenvatinib": "ленватиніб",
    "regorafenib": "регорафеніб",
    "ramucirumab": "рамуцирумаб",
    "ruxolitinib": "руксолитиніб",
    "fedratinib": "федратиніб",
    "pacritinib": "пакритиніб",
    "momelotinib": "момелотиніб",
    "luspatercept": "люспатерцепт",
    "anagrelide": "анагрелід",
    "hydroxyurea": "гідроксикарбамід",
    "interferon": "інтерферон",
    "all-trans retinoic acid": "повністю-трансретиноєва кислота",
    "atra": "ATRA",
    "arsenic trioxide": "триоксид арсену",
    "ato": "ATO",
    "cladribine": "кладрибін",
    "pentostatin": "пентостатин",
    "moxetumomab pasudotox": "моксетумомаб пасудотокс",
    "tagraxofusp": "таграксофусп",
    "midazolam": "мідазолам",
    "tocilizumab": "тоцилізумаб",
    "siltuximab": "силтуксимаб",
    "anakinra": "анакінра",
    "filgrastim": "філграстим",
    "pegfilgrastim": "пегфілграстим",
    "lipegfilgrastim": "ліпегфілграстим",
    "epoetin alfa": "епоетин альфа",
    "darbepoetin": "дарбепоетин",
    "g-csf": "Г-КСФ",
    "epo": "ЕПО",
    "ivig": "ВВІГ",
    "tucatinib": "тукатиніб",
    "neratinib": "нератиніб",
    "lapatinib": "лапатиніб",
    "margetuximab": "маргетуксимаб",
    "sacituzumab govitecan": "сацитузумаб говітекан",
    "fam-trastuzumab deruxtecan": "fam-трастузумаб дерукстекан",
    "elacestrant": "елацестрант",
    "camrelizumab": "камрелізумаб",
    "tislelizumab": "тислелізумаб",
    "sintilimab": "синтилімаб",
    "toripalimab": "торипалімаб",
    "relatlimab": "релатлімаб",
    "tremelimumab": "тремелімумаб",
    "tebentafusp": "тебентафусп",
    "talimogene laherparepvec": "талімоген лагерпарепвек",
    "t-vec": "T-VEC",
    "etoposide": "етопозид",
    "irinotecan": "іринотекан",
    "topotecan": "топотекан",
    "leucovorin": "лейковорин",
    "calcium folinate": "кальцію фолінат",
    "folinic acid": "фолінова кислота",
    "raltitrexed": "ралтитрексед",
    "tegafur": "тегафур",
    "trifluridine": "трифлуридин",
    "tas-102": "TAS-102",
    "lonsurf": "Lonsurf",
    "tipiracil": "типірацил",
    "fruquintinib": "фруквінтиніб",
    "encorafenib + cetuximab": "енкорафеніб + цетуксимаб",
    "fluorouracil/leucovorin": "фторурацил/лейковорин",
    "5-fu": "5-FU",
    "folfox": "FOLFOX",
    "folfiri": "FOLFIRI",
    "folfirinox": "FOLFIRINOX",
    "folfoxiri": "FOLFOXIRI",
    "capox": "CAPOX",
    "xelox": "XELOX",
    "r-chop": "R-CHOP",
    "r-cvp": "R-CVP",
    "r-bendamustine": "R-бендамустин",
    "br": "BR",
    "abvd": "ABVD",
    "beacopp": "BEACOPP",
    "escalated beacopp": "ескальований BEACOPP",
    "a+avd": "A+AVD",
    "ec": "EC",
    "ac": "AC",
    "tc": "TC",
    "tch": "TCH",
    "tchp": "TCHP",
    "ddmvac": "ddMVAC",
    "mvac": "MVAC",
    "gem-cis": "гем-цис",
    "gemcitabine + cisplatin": "гемцитабін + цисплатин",
    "ven+aza": "венетоклакс+азацитидин",
    "ven-aza": "венетоклакс-азацитидин",
    "venetoclax + azacitidine": "венетоклакс + азацитидин",
    "venetoclax+azacitidine": "венетоклакс+азацитидин",
    "venetoclax + low-dose cytarabine": "венетоклакс + низькодозовий цитарабін",
    "ldac": "LDAC",
    "vyxeos": "Vyxeos",
    "cpx-351": "CPX-351",
    "7+3": "7+3",
    "7 + 3": "7 + 3",
    "fldac": "FLDAC",
    "midac": "MIDAC",
    "hidac": "HiDAC",
    "ce": "CE",
    "cdk4/6 inhibitor": "інгібітор CDK4/6",
    "parp inhibitor": "інгібітор PARP",
    "tki": "TKI",
    "btki": "BTKi",
    "egfr-tki": "EGFR-TKI",
    "alk-tki": "ALK-TKI",
    "ret-tki": "RET-TKI",
}

CASE_PRESERVE_TOKENS = {
    # Tokens that must keep Latin casing exactly (acronyms, gene symbols).
    "BRAF", "EGFR", "ALK", "ROS1", "NTRK", "RET", "KRAS", "HER2", "BRCA1",
    "BRCA2", "CDKN2A", "MET", "FLT3", "IDH1", "IDH2", "NPM1", "TP53",
    "ATM", "PALB2", "MLH1", "MSH2", "MSH6", "PMS2", "EPCAM", "POLE", "POLD1",
    "BCR-ABL1", "BCR::ABL1", "JAK2", "CALR", "MPL", "PML-RARA", "PML::RARA",
    "RUNX1", "RUNX1::RUNX1T1", "CBFB::MYH11", "CBFB-MYH11", "KMT2A",
    "BCL2", "BCL6", "MYC", "CCND1", "MALT1", "API2", "MALT1", "API2-MALT1",
    "PD-L1", "PD-1", "CTLA-4", "TIGIT", "LAG-3", "TIM-3",
    "CD20", "CD22", "CD30", "CD33", "CD38", "CD52", "CD79b", "CD123", "CD138",
    "CD7", "CD4", "CD8", "CD3", "CD5", "CD19", "CD23", "CD25", "CD45",
    "CD56", "BCMA", "GPRC5D", "FCRL5", "SLAMF7",
    "TMB", "MSI", "MSI-H", "dMMR", "pMMR", "HRD", "HRR", "POLE",
    "ECOG", "KPS", "DLCO", "LVEF", "FEV1", "GFR", "AST", "ALT", "ALP",
    "LDH", "B2M", "ANC", "PLT", "Hb", "WBC", "RBC", "DOR", "PFS", "OS",
    "ORR", "CR", "PR", "SD", "PD", "DCR", "DLT", "MTD", "TTP", "TTF",
    "EFS", "DFS", "DSS", "RFS", "MRD", "DAT", "AIHA", "ITP",
    "FDA", "EMA", "NCCN", "ESMO", "ASCO", "ASH", "EHA", "WHO", "ICC",
    "EORTC", "EBMT", "GELTAMO", "MDS", "MPN", "AML", "ALL", "CLL", "CML",
    "MM", "DLBCL", "FL", "MCL", "MZL", "WM", "BL", "HL", "HCL", "PTCL",
    "AITL", "ALCL", "ATLL", "CTCL", "EATL", "HSTCL", "ETP-ALL", "ETP",
    "T-PLL", "B-PLL", "PMBL", "PEL", "PCNSL", "BPDCN",
    "CSF", "CNS", "GI", "GU", "HN", "RCC", "HCC", "CRC", "PDAC", "CCA",
    "NSCLC", "SCLC", "TNBC", "HER2-low", "HR+", "HR-", "ER", "PR", "PgR",
    "STR", "MTM", "ITT", "PP", "PFS-2", "OS-2",
    "OncoTree", "OncoKB", "ESCAT", "AJCC", "TNM", "UICC", "TPS", "CPS",
    "ICD-10", "ICD-O-3", "RxNorm", "LOINC", "CTCAE", "FHIR", "mCODE",
    "BV", "Bv", "T-DXd", "T-DM1", "AVD", "CHOP", "CHOEP", "CHEP", "EPOCH",
    "DA-EPOCH", "DA-EPOCH-R", "R-EPOCH", "R-DA-EPOCH", "R-CODOX-M/IVAC",
    "R-Pola-CHP", "Pola-R-CHP", "RCHP", "R-CHP", "RCD", "RCMP",
    "RVD", "VRd", "VTd", "VCd", "DRd", "KRd", "Pd", "DPd", "Rd", "MPT",
    "MP", "VMP", "DVd", "Dara-VMP", "Dara-Rd", "Isa-Pd", "Isa-Kd",
    "BCL-2", "BCL-XL", "MDM2",
    "MOSAIC", "ATAC", "BIG-1-98", "TAILORx", "RxPONDER", "MINDACT",
    "OlympiAD", "OlympiA", "OlympiD", "EMBRACA", "PROfound", "MAGNITUDE",
    "PALOMA-2", "PALOMA-3", "MONALEESA-2", "MONALEESA-3", "MONALEESA-7",
    "MONARCH-2", "MONARCH-3", "SOLAR-1", "BYLieve", "DESTINY-Breast03",
    "DESTINY-Breast04", "DESTINY-Breast06", "TROPiCS-02", "EMERALD",
    "KEYNOTE-189", "KEYNOTE-407", "KEYNOTE-024", "KEYNOTE-042",
    "KEYNOTE-189", "KEYNOTE-590", "KEYNOTE-355", "KEYNOTE-522",
    "KEYNOTE-426", "KEYNOTE-564", "KEYNOTE-A18", "CheckMate-067",
    "CheckMate-9LA", "CheckMate-816", "CheckMate-577", "CheckMate-9ER",
    "CheckMate-274", "CheckMate-238", "CheckMate-227",
    "CROWN", "ALEX", "ALINA", "PROFILE-1014", "ALTA-1L", "FLAURA",
    "ARASENS", "ARCHES", "ENZAMET", "STAMPEDE", "TITAN", "SPARTAN",
    "PROpel", "TALAPRO-2", "MAGNITUDE", "EZH-301",
    "VIALE-A", "VIALE-C", "QUAZAR", "LACEWING", "ADMIRAL", "RATIFY",
    "QuANTUM-First", "QuANTUM-R", "AGILE", "AG120-C-009",
    "ECHELON-1", "ECHELON-2", "ALCANZA", "MAVORIC", "MOPP", "BEACOPP",
    "RESONATE", "RESONATE-2", "iLLUMINATE", "ELEVATE-RR", "ELEVATE-TN",
    "MURANO", "CLL14", "CLL13", "GLOW", "ASCEND", "ALPINE", "SEQUOIA",
    "BRIGHT", "GADOLIN", "GALLIUM", "AUGMENT", "RELEVANCE", "MAGNIFY",
    "POLARIX", "L-MIND", "TRANSCEND-NHL", "ZUMA-7", "ZUMA-12", "ZUMA-1",
    "ALEXANDER", "ALPINE", "POLARIX", "EPCORE-NHL-1",
    "TOWER", "BLAST", "INO-VATE", "ZUMA-3",
    "ASCERTAIN", "MEDALIST", "COMMANDS",
    "RESONATE", "RAY", "SHINE", "TRIANGLE", "WINDOW",
    "ALPHA", "ZUMA-2", "BRUIN",
    "RAINFALL", "CHECKMATE-649", "RAINBOW", "REGARD",
    "TRIBE", "TRIBE-2", "PARADIGM", "FIRE-3", "CALGB-80405",
    "MOSAIC", "IDEA", "FOWARC", "PRODIGE-7", "PRODIGE-23",
    "PROSPECT", "PRIME", "STAMPEDE",
    "STARTRK-2", "ALKA-372-001", "LIBRETTO-001", "ARROW",
    "DESTINY-Lung01", "DESTINY-Lung02",
    "TBio", "ARROW", "VISION", "GEOMETRY", "MET-1",
    "ALK", "RET", "ROS1", "MET", "BRAF", "EGFR", "HER2", "KRAS", "NRAS",
    "BRCA", "ATM", "PALB2", "CHEK2",
    "PI", "Pi", "VEGF", "VEGFR", "FGFR", "PDGFR", "PDGF",
    "PARP", "MEK", "MET", "RET",
    "Tier", "IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X",
    "ESCAT-IA", "ESCAT-IB", "ESCAT-IIA", "ESCAT-IIB", "ESCAT-IIIA",
    "BCL-2", "MCL-1",
    "CBC", "CMP", "BMP", "PT", "PTT", "INR", "PET-CT", "MRI", "CT",
    "FISH", "PCR", "RT-PCR", "qPCR", "ddPCR",
    "IHC", "ISH", "CISH", "EBER-ISH", "EBER", "EBV",
    "HBV", "HCV", "HIV", "HTLV-1", "HHV-8", "CMV", "JCV",
    "PML-RARA", "PML::RARA", "ETV6", "ETV6::RUNX1",
    "WHO 5th ed.", "WHO 5th",
    "USA", "EU", "EEC",
    "G1", "G2", "G3", "G4", "G5",
    "Tier 1", "Tier 2", "Tier 3", "Tier 4",
    "v3.20-2026-04",
}

# We also keep ANY all-uppercase token of length ≥2 unchanged
# (gene symbols, trial acronyms, dose units like "mg/m²", etc.)
KEEP_LATIN_RE = re.compile(r"^[A-Z][A-Z0-9\-]+$|^[A-Z]+\d+[A-Z0-9\-]*$|^p\.[A-Z]\d+[A-Z\*]+$")

# Numbers, percentages, units, dosing — leave verbatim.
NUMERIC_RE = re.compile(
    r"^[><≤≥]?[\d\.,/\-+]+(?:%|mg/m²|mg/m2|mg|µg|ug|g/dL|g/L|mmol|μmol|umol|"
    r"x10\^\d|months?|days?|weeks?|years?|yr|cycles?|h|U/L|U|U/mL|µL|uL|mEq|"
    r"mL|L|mIU|kg|cm|mm)?$"
)


def _is_pass_through(tok: str) -> bool:
    """True if token should remain in Latin/numeric form unchanged."""
    if not tok:
        return True
    if tok in CASE_PRESERVE_TOKENS:
        return True
    if KEEP_LATIN_RE.match(tok):
        return True
    if NUMERIC_RE.match(tok):
        return True
    if any(c.isdigit() for c in tok) and any(c.isalpha() for c in tok):
        # mixed alphanumeric like "V600E", "T790M", "G12C", "L858R"
        return True
    if tok.startswith("p.") or tok.startswith("c.") or tok.startswith("g."):
        return True
    return False


_BOUND_LEFT = r"(?<![A-Za-zА-Яа-яҐґЇїІіЄє])"
_BOUND_RIGHT = r"(?![A-Za-zА-Яа-яҐґЇїІіЄє])"


def _build_compiled_table() -> list[tuple[re.Pattern, str]]:
    """Compile one big ordered list of (pattern, replacement) pairs.

    Order: drug names first (longest first), then phrases (longest first).
    Sorting by descending length avoids a multi-word phrase being clobbered
    by a substring single-word phrase.
    """
    items: list[tuple[str, str]] = []
    for drug, ua in DRUGS.items():
        items.append((drug, ua))
    for en_p, ua_p in PHRASES:
        items.append((en_p, ua_p))
    items.sort(key=lambda kv: -len(kv[0]))
    compiled: list[tuple[re.Pattern, str]] = []
    for en_p, ua_p in items:
        pat = re.compile(_BOUND_LEFT + re.escape(en_p) + _BOUND_RIGHT,
                         re.IGNORECASE)
        compiled.append((pat, ua_p))
    return compiled


_COMPILED = _build_compiled_table()


def translate_text(en: str) -> str:
    """Best-effort dictionary translation of an English clinical paragraph
    into Ukrainian. Preserves Latin acronyms, dosing strings, gene/protein
    symbols, year tags, and ESCAT/OncoKB tier labels verbatim.
    """
    if not en:
        return en
    text = en
    for pat, ua in _COMPILED:
        text = pat.sub(ua, text)
    return text


def has_translatable_marker(data: dict, ua_field: str) -> bool:
    """True if this entity already has the UA companion field filled."""
    val = data.get(ua_field)
    return val is not None and (not isinstance(val, str) or val.strip())


def make_ua_block(en_text: str) -> tuple[str, str, str]:
    """Return (ua_translation, status_marker, author_marker)."""
    return (translate_text(en_text), MARKER_STATUS, MARKER_AUTHOR)


def process_file(
    path: Path, en_field: str, ua_field: str, yaml_io: YAML
) -> tuple[bool, str, str | None, str | None]:
    """Edit one YAML file in place.

    Returns (modified, reason, entity_id_if_modified, ua_snippet_if_modified).
    `reason` is empty on success, otherwise a short skip reason.
    """
    text = path.read_text(encoding="utf-8")
    try:
        data = yaml_io.load(text)
    except Exception as e:
        return False, f"YAML parse: {e}", None, None
    if data is None or not hasattr(data, "get"):
        return False, "non-mapping root", None, None
    en = data.get(en_field)
    if not en or (isinstance(en, str) and not en.strip()):
        return False, f"no source ({en_field})", None, None
    if has_translatable_marker(data, ua_field):
        return False, f"already filled ({ua_field})", None, None

    ua_text, status, author = make_ua_block(str(en))

    # Use folded scalar for multi-line UA paragraphs >100 chars to match
    # the existing YAML style across the KB. Single-line strings stay
    # as plain strings.
    if "\n" in ua_text or len(ua_text) > 80:
        ua_value = FoldedScalarString(ua_text)
    else:
        ua_value = ua_text

    # Insert UA field immediately after the EN field for visual grouping.
    keys = list(data.keys())
    if en_field in keys:
        idx = keys.index(en_field)
        # ruamel preserves insertion order; we re-build the mapping
        try:
            data.insert(idx + 1, ua_field, ua_value)
            data.insert(idx + 2, "ukrainian_review_status", status)
            data.insert(idx + 3, "ukrainian_drafted_by", author)
        except (TypeError, AttributeError):
            data[ua_field] = ua_value
            data["ukrainian_review_status"] = status
            data["ukrainian_drafted_by"] = author
    else:
        data[ua_field] = ua_value
        data["ukrainian_review_status"] = status
        data["ukrainian_drafted_by"] = author

    out = path.open("w", encoding="utf-8", newline="\n")
    try:
        yaml_io.dump(data, out)
    finally:
        out.close()
    eid = data.get("id") if hasattr(data, "get") else None
    return True, "", str(eid) if eid else None, ua_text[:240]


def main() -> int:
    yaml_io = YAML()
    yaml_io.preserve_quotes = True
    yaml_io.width = 4096
    yaml_io.indent(mapping=2, sequence=4, offset=2)

    totals: dict[str, dict[str, int]] = {}
    samples: list[tuple[str, str, str]] = []  # (entity_type, id, ua_text snippet)

    for entity_dir, en_field, ua_field in ENTITY_PLAN:
        d = KB / entity_dir
        if not d.is_dir():
            continue
        c = {"total": 0, "filled": 0, "skipped_no_src": 0,
             "skipped_already": 0, "skipped_parse": 0}
        for path in sorted(d.rglob("*.yaml")):
            rel = path.relative_to(KB).as_posix()
            if rel in SKIP_FILES:
                continue
            c["total"] += 1
            modified, reason, eid, snippet = process_file(
                path, en_field, ua_field, yaml_io
            )
            if modified:
                c["filled"] += 1
                if len(samples) < 12:
                    samples.append((entity_dir, eid or "?", snippet or ""))
            else:
                if "no source" in reason:
                    c["skipped_no_src"] += 1
                elif "already filled" in reason:
                    c["skipped_already"] += 1
                else:
                    c["skipped_parse"] += 1
        totals[entity_dir] = c

    print("== UA-field draft pass ==")
    for entity_dir, c in totals.items():
        print(f"  {entity_dir:28s}  filled={c['filled']:4d}  "
              f"already={c['skipped_already']:4d}  "
              f"no_src={c['skipped_no_src']:4d}  "
              f"parse_err={c['skipped_parse']:4d}  "
              f"total={c['total']:4d}")

    print("\n== Sample drafted UA strings ==")
    for entity_dir, eid, snippet in samples:
        print(f"  [{entity_dir}] {eid}")
        print(f"    {snippet}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
