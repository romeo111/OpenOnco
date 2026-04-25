"""Fill MEDIUM-priority RedFlag scaffolds (30 RFs across 6 diseases).

Per CLINICAL_REVIEW_QUEUE_REDFLAGS §C, MEDIUM-priority diseases:
HCL, EATL, HSTCL, ATLL, T-PLL, SMZL.

Same approach as fill_high_priority_scaffolds.py — extraction with
clinician verification expected at PR-merge time.

Algorithm reality check:
- HCL: 2-arm (CLADRIBINE / PENTOSTATIN) — branchable
- EATL: single-track CHOEP-AUTOSCT — most RFs are investigate
- HSTCL: single-track ICE-ALLOSCT — most RFs are investigate
- ATLL: 2-arm (AGGRESSIVE / INDOLENT-AZT-IFN) — Shimoyama-driven
- T-PLL: single-track ALEMTUZUMAB — most RFs are investigate
- SMZL: 2-arm (RITUXIMAB / HCV-POSITIVE) — HCV-driven
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"

SPECS: list[dict] = [
    # ─── HCL (5) — 2-arm: cladribine vs pentostatin ────────────────────
    {
        "file": "rf_hcl_organ_dysfunction.yaml",
        "id": "RF-HCL-ORGAN-DYSFUNCTION",
        "disease": "DIS-HCL",
        "definition": "Renal dysfunction (CrCl <60 mL/min) — cladribine clearance reduced; dose adjustment or pentostatin alternative considered.",
        "definition_ua": "Ниркова дисфункція (CrCl <60 мл/хв) — кліренс кладрибіну знижений; коригування дози або заміна на пентостатин.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "creatinine_clearance_ml_min"
      threshold: 60
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Both cladribine and pentostatin are renally cleared; CrCl <60 mL/min triggers 25-50% dose reduction. Hematology decision; not a regimen-class shift.",
    },
    {
        "file": "rf_hcl_infection_screening.yaml",
        "id": "RF-HCL-INFECTION-SCREENING",
        "disease": "DIS-HCL",
        "definition": "Active uncontrolled infection at HCL diagnosis — defer purine analog (cladribine/pentostatin) until infection controlled; profound CD4 lymphopenia for 6-12 months post-treatment increases opportunistic infection risk.",
        "definition_ua": "Активна неконтрольована інфекція на діагнозі HCL — відстрочити пуринові аналоги (кладрибін/пентостатин) до контролю інфекції; виражена CD4-лімфопенія 6-12 місяців після терапії підвищує ризик опортуністичних інфекцій.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "active_uncontrolled_infection"
      value: true
    - finding: "neutropenic_fever_active"
      value: true
""",
        "direction": "hold",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Active infection at diagnosis is common in HCL (severe neutropenia from disease itself). Standard practice: control infection first (G-CSF + antibiotics), then start cladribine. Hold-direction surfaces in MDT brief but doesn't shift Indication.",
    },
    {
        "file": "rf_hcl_high_risk_biology.yaml",
        "id": "RF-HCL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-HCL",
        "definition": "BRAF V600E wild-type variant HCL (HCL-v) OR IGHV4-34 expression — purine analogs less effective; consider rituximab combination upfront or vemurafenib (for BRAF mutant) in 2L.",
        "definition_ua": "BRAF V600E дикий тип, варіантна HCL (HCL-v) АБО IGHV4-34 експресія — пуринові аналоги менш ефективні; розглянути додавання rituximab з 1L або vemurafenib (BRAF mut) у 2L.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hcl_variant_v"
      value: true
    - finding: "ighv4_34_positive"
      value: true
    - finding: "braf_v600e"
      value: "negative"
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "HCL-v and IGHV4-34 are predictors of inferior response to single-agent purine analog. Adding rituximab (HCL14 trial: cladribine + rituximab) raises CR rate notably. Indication-level decision, not a 1L Algorithm switch.",
    },
    {
        "file": "rf_hcl_transformation_progression.yaml",
        "id": "RF-HCL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-HCL",
        "definition": "Failure to achieve CR after 2 courses cladribine OR early relapse (<2 years) — switch to alternative purine analog + rituximab, vemurafenib (BRAF V600E+), or moxetumomab pasudotox.",
        "definition_ua": "Без CR після 2 курсів кладрибіну АБО ранній рецидив (<2 років) — заміна на інший пуриновий аналог + rituximab, vemurafenib (BRAF V600E+), або моксетумомаб пасудотокс.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "hcl_no_cr_after_cladribine"
      value: true
    - finding: "hcl_early_relapse_under_2y"
      value: true
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Refractory/early-relapsed HCL has multiple 2L options; selection driven by BRAF status and prior exposure. Sits in 2L Algorithm not 1L.",
    },
    {
        "file": "rf_hcl_frailty_age.yaml",
        "id": "RF-HCL-FRAILTY-AGE",
        "disease": "DIS-HCL",
        "definition": "Age >75 + ECOG ≥2 OR significant comorbidity — pentostatin's weekly schedule allows finer toxicity titration than cladribine 5-7 day continuous infusion; preferred for fragile patients.",
        "definition_ua": "Вік >75 + ECOG ≥2 АБО суттєва коморбідність — щотижневий пентостатин дозволяє тонше титрування токсичності, ніж 5-7-денна безперервна інфузія кладрибіну; кращий для frail.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  all_of:
    - any_of:
        - finding: "age_years"
          threshold: 75
          comparator: ">"
        - finding: "comorbidity_count"
          threshold: 2
          comparator: ">="
    - finding: "ecog_status"
      threshold: 2
      comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": ["ALGO-HCL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Pentostatin's weekly cadence permits adjustment between doses; cladribine's 5-7-day infusion is committed. For elderly frail, pentostatin's tolerability advantage outweighs cladribine's slightly higher CR rate.",
    },

    # ─── EATL (5) — single-track ──────────────────────────────────────
    {
        "file": "rf_eatl_organ_dysfunction.yaml",
        "id": "RF-EATL-ORGAN-DYSFUNCTION",
        "disease": "DIS-EATL",
        "definition": "Bowel perforation, severe malabsorption (albumin <2.5 g/dL), or surgical complication — defer CHOEP induction until nutritional/surgical stabilization; parenteral nutrition + delayed-onset chemo schedule.",
        "definition_ua": "Перфорація кишки, виражена мальабсорбція (альбумін <2.5 г/дл), або хірургічне ускладнення — відстрочити CHOEP до харчової/хірургічної стабілізації; парентеральне харчування + delayed-onset режим.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "bowel_perforation"
      value: true
    - finding: "albumin_g_dl"
      threshold: 2.5
      comparator: "<"
    - finding: "surgical_complication_active"
      value: true
""",
        "direction": "hold",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "EATL frequently presents with perforation/obstruction requiring emergent surgery. Chemo cannot start safely until ECOG recovers and nutrition stabilizes. Multi-disciplinary surgery-onc-nutrition path.",
    },
    {
        "file": "rf_eatl_infection_screening.yaml",
        "id": "RF-EATL-INFECTION-SCREENING",
        "disease": "DIS-EATL",
        "definition": "HBV/HCV/HIV/CMV serology + Strongyloides screen pre-CHOEP (immigrants from endemic areas) — anti-CD20 not used here, but rituximab-naive patients still require HBV prophylaxis if HBsAg+.",
        "definition_ua": "HBV/HCV/HIV/CMV серологія + Strongyloides скринінг перед CHOEP (іммігранти з ендемічних регіонів) — rituximab тут не застосовують, але HBsAg+ пацієнти потребують HBV профілактики.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "strongyloides_endemic_exposure"
      value: true
    - finding: "hiv_serology"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Immunosuppression-driven Strongyloides hyperinfection is rare but lethal; ivermectin prophylaxis for endemic-area patients is standard.",
    },
    {
        "file": "rf_eatl_high_risk_biology.yaml",
        "id": "RF-EATL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-EATL",
        "definition": "Type II EATL (monomorphic epitheliotropic intestinal T-cell lymphoma) per WHO classification — distinct from celiac-associated Type I EATL; often non-celiac, more chemo-refractory.",
        "definition_ua": "Тип II EATL (мономорфна епітеліотропна кишкова T-клітинна лімфома) за WHO — відрізняється від целіакія-асоційованої Type I EATL; часто без целіакії, більш хіміо-рефрактерна.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "eatl_type_ii_meitl"
      value: true
    - finding: "celiac_disease_negative_eatl"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Type II EATL (now MEITL in WHO 2022) has worse outcomes than Type I; intensification options limited (alloSCT considered upfront when feasible).",
    },
    {
        "file": "rf_eatl_transformation_progression.yaml",
        "id": "RF-EATL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-EATL",
        "definition": "Refractory disease at end-of-induction (no CR/PR after 4 cycles CHOEP) OR rapid relapse — alloSCT or experimental therapy (brentuximab if CD30+, romidepsin/HDAC-i salvage).",
        "definition_ua": "Рефрактерне захворювання на кінець індукції (без CR/PR після 4 циклів CHOEP) АБО швидкий рецидив — alloSCT або експериментальна терапія (брентуксимаб якщо CD30+, ромідепсин/HDAC-i salvage).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "eatl_no_response_after_4_cycles"
      value: true
    - finding: "eatl_rapid_relapse"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Refractory EATL has dismal prognosis; clinical trial referral is the recommended next step.",
    },
    {
        "file": "rf_eatl_frailty_age.yaml",
        "id": "RF-EATL-FRAILTY-AGE",
        "disease": "DIS-EATL",
        "definition": "Age >70 OR ECOG ≥3 — CHOEP intensity + autoSCT consolidation poorly tolerated; CHOP-based with reduced doses ± brentuximab (CD30+) considered.",
        "definition_ua": "Вік >70 АБО ECOG ≥3 — інтенсивність CHOEP + autoSCT погано переноситься; CHOP з redukованими дозами ± брентуксимаб (CD30+).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 70
      comparator: ">"
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "EATL is mostly disease of elderly; autoSCT limited by performance status. Reduced-intensity backbone trades cure rates for tolerability.",
    },

    # ─── HSTCL (5) — single-track ICE-AlloSCT ─────────────────────────
    {
        "file": "rf_hstcl_organ_dysfunction.yaml",
        "id": "RF-HSTCL-ORGAN-DYSFUNCTION",
        "disease": "DIS-HSTCL",
        "definition": "Hepatic dysfunction (Child-Pugh B/C, bilirubin >3xULN) at HSTCL diagnosis — disease itself causes hepatosplenomegaly + cytopenias; ifosfamide + carboplatin + etoposide (ICE) induction toxicity exacerbated.",
        "definition_ua": "Печінкова дисфункція (Child-Pugh B/C, білірубін >3xULN) на діагнозі HSTCL — хвороба сама викликає гепатоспленомегалію + цитопенії; токсичність ICE підвищена.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "child_pugh_class"
      value: "B"
    - finding: "child_pugh_class"
      value: "C"
    - finding: "bilirubin_x_uln"
      threshold: 3
      comparator: ">"
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "HSTCL almost always presents with hepatosplenomegaly + cytopenias; baseline LFT abnormalities common. Hepatology + hematology co-management critical; supportive care intensified.",
    },
    {
        "file": "rf_hstcl_infection_screening.yaml",
        "id": "RF-HSTCL-INFECTION-SCREENING",
        "disease": "DIS-HSTCL",
        "definition": "EBV / HBV / HCV / CMV / Strongyloides screen pre-induction; HSTCL is rare in immunocompetent — exclude post-transplant or anti-TNF-driven HSTCL (different etiology, may regress with IS-reduction).",
        "definition_ua": "EBV/HBV/HCV/CMV/Strongyloides скринінг перед індукцією; HSTCL рідкісна в імунокомпетентних — виключити post-transplant або anti-TNF-індуковану (інша етіологія, може регресувати на IS-редукції).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "ebv_pcr_blood_positive"
      value: true
    - finding: "post_transplant_setting"
      value: true
    - finding: "anti_tnf_exposure"
      value: true
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Anti-TNF-induced HSTCL (Crohn's IBD patients) sometimes regresses with TNF-inhibitor withdrawal; PTLD-like HSTCL after solid organ transplant follows different paradigm. Etiology drives initial path.",
    },
    {
        "file": "rf_hstcl_high_risk_biology.yaml",
        "id": "RF-HSTCL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-HSTCL",
        "definition": "γδ T-cell receptor variant (most common) vs αβ variant — both aggressive but γδ classically associated with worse prognosis; SETD2/INO80 mutations confer chemo-resistance.",
        "definition_ua": "γδ варіант TCR (найчастіший) vs αβ — обидва агресивні, але γδ традиційно гірший прогноз; SETD2/INO80 мутації → хіміо-резистентність.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "tcr_gamma_delta_phenotype"
      value: true
    - finding: "setd2_mutation"
      value: true
    - finding: "ino80_mutation"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "HSTCL biology drives early alloSCT decision more than 1L regimen choice (ICE is universal default). Flag MDT-priority for transplant referral.",
    },
    {
        "file": "rf_hstcl_transformation_progression.yaml",
        "id": "RF-HSTCL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-HSTCL",
        "definition": "Refractory or rapid-relapse disease post-ICE — alloSCT urgently if not yet planned; otherwise pralatrexate or romidepsin salvage with transplant intent.",
        "definition_ua": "Рефрактерна або швидко-рецидивна хвороба після ICE — терміново alloSCT якщо ще не заплановано; інакше pralatrexate або romidepsin salvage з трансплант-інтентом.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "hstcl_refractory_post_ice"
      value: true
    - finding: "hstcl_rapid_relapse"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "HSTCL refractory disease has very poor outcomes; alloSCT is the only realistic curative path.",
    },
    {
        "file": "rf_hstcl_frailty_age.yaml",
        "id": "RF-HSTCL-FRAILTY-AGE",
        "disease": "DIS-HSTCL",
        "definition": "Age >65 OR ECOG ≥3 — ICE + alloSCT toxicity prohibitive; reduced-intensity conditioning alloSCT or palliative chemotherapy considered.",
        "definition_ua": "Вік >65 АБО ECOG ≥3 — токсичність ICE + alloSCT непереносна; reduced-intensity conditioning alloSCT або паліативна хіміо.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 65
      comparator: ">"
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "HSTCL outside trial setting in elderly is largely palliative; cure intent restricted to fit transplant candidates.",
    },

    # ─── ATLL (5) — 2-arm: aggressive vs indolent (Shimoyama) ─────────
    {
        "file": "rf_atll_organ_dysfunction.yaml",
        "id": "RF-ATLL-ORGAN-DYSFUNCTION",
        "disease": "DIS-ATLL",
        "definition": "Hypercalcemia (Ca >12 mg/dL) at diagnosis — hallmark of aggressive ATLL; requires bisphosphonate/calcitonin urgently and predicts aggressive subtype regardless of WBC.",
        "definition_ua": "Гіперкальціємія (Ca >12 мг/дл) на діагнозі — маркер агресивної ATLL; потребує бісфосфонат/кальцитонін терміново і передбачає агресивний підтип незалежно від WBC.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "calcium_mg_dl"
      threshold: 12
      comparator: ">"
    - finding: "atll_hypercalcemia"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": ["ALGO-ATLL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Hypercalcemia in ATLL is paraneoplastic (RANKL-driven by HTLV-1+ T cells) — its presence overrides Shimoyama subtyping toward aggressive variant; AZT+IFN-α inadequate. Immediate hypercalcemia management + aggressive chemo (mLSG-15 / EPOCH-like) standard.",
    },
    {
        "file": "rf_atll_infection_screening.yaml",
        "id": "RF-ATLL-INFECTION-SCREENING",
        "disease": "DIS-ATLL",
        "definition": "HTLV-1 confirmation by serology + PCR; Strongyloides screen mandatory (HTLV-1 endemic areas); HBV/HCV/HIV pre-treatment.",
        "definition_ua": "HTLV-1 підтвердження серологією + PCR; Strongyloides скринінг обов'язковий (HTLV-1 ендемічні регіони); HBV/HCV/HIV перед терапією.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "htlv1_serology"
      value: "positive"
    - finding: "strongyloides_endemic_exposure"
      value: true
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "HTLV-1 confirmation is part of diagnosis; Strongyloides hyperinfection mortality post-immunosuppression is high in endemic-area exposure.",
    },
    {
        "file": "rf_atll_high_risk_biology.yaml",
        "id": "RF-ATLL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-ATLL",
        "definition": "Shimoyama acute or lymphoma subtype (LDH >2×ULN, BUN >ULN, albumin <ULN — any one) — aggressive variant; AZT+IFN-α inadequate, requires intensive chemo (mLSG-15) ± alloSCT.",
        "definition_ua": "Shimoyama гостра або лімфомна форма (LDH >2×ULN, BUN >ULN, альбумін <ULN — будь-який один) — агресивний варіант; AZT+IFN-α недостатній, потрібна інтенсивна хіміо (mLSG-15) ± alloSCT.",
        "trigger_yaml": """trigger:
  type: composite_score
  any_of:
    - finding: "shimoyama_aggressive_subtype"
      value: true
    - finding: "ldh_x_uln"
      threshold: 2
      comparator: ">"
    - finding: "bun_above_uln"
      value: true
    - finding: "albumin_below_uln"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": ["ALGO-ATLL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Shimoyama's prognostic system is THE classifier in ATLL: smoldering/chronic-favorable get watch-and-wait or AZT+IFN-α; acute/lymphoma get aggressive chemo. Engine routes appropriately.",
    },
    {
        "file": "rf_atll_transformation_progression.yaml",
        "id": "RF-ATLL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-ATLL",
        "definition": "Smoldering/chronic ATLL transforming to acute (rising lymphocyte count, new B-symptoms, organ infiltration) — switch from watch-and-wait/AZT+IFN to aggressive chemo immediately.",
        "definition_ua": "Тліюча/хронічна ATLL трансформується в гостру (зростання лімфоцитів, нові B-симптоми, інфільтрація органів) — негайний перехід з watch-and-wait/AZT+IFN на агресивну хіміо.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "atll_transformation_to_acute"
      value: true
    - finding: "lymphocyte_count_doubling_3_months"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Indolent ATLL transformation requires immediate algorithm reassessment — typically modeled as a re-evaluation event triggering revise_plan() rather than a 1L decision_tree branch.",
    },
    {
        "file": "rf_atll_frailty_age.yaml",
        "id": "RF-ATLL-FRAILTY-AGE",
        "disease": "DIS-ATLL",
        "definition": "Age >70 + ECOG ≥3 OR severe cytopenia at diagnosis — mLSG-15 intensive chemotherapy excessive toxicity; CHOP-based or AZT+IFN-α (even in aggressive subtype) considered.",
        "definition_ua": "Вік >70 + ECOG ≥3 АБО важкі цитопенії на діагнозі — інтенсивна mLSG-15 надмірно токсична; CHOP або AZT+IFN-α (навіть в агресивному підтипі).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  all_of:
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
    - finding: "age_years"
      threshold: 70
      comparator: ">"
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "ATLL endemic in older Japanese/Caribbean populations; mLSG-15 trials excluded >70. Real-world elderly aggressive ATLL often gets dose-reduced CHOP at best.",
    },

    # ─── T-PLL (5) — single-track alemtuzumab ─────────────────────────
    {
        "file": "rf_t_pll_organ_dysfunction.yaml",
        "id": "RF-T-PLL-ORGAN-DYSFUNCTION",
        "disease": "DIS-T-PLL",
        "definition": "Severe cytopenia (ANC <0.5 OR platelets <50 OR Hgb <8) at diagnosis — disease-driven marrow infiltration; alemtuzumab will worsen lymphopenia; growth-factor support + transfusion threshold management critical.",
        "definition_ua": "Виражені цитопенії (ANC <0.5 АБО тромбоцити <50 АБО Hgb <8) на діагнозі — пухлинна інфільтрація; alemtuzumab погіршить лімфопенію; G-CSF + трансфузійний поріг критично важливі.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "anc_x10_9_l"
      threshold: 0.5
      comparator: "<"
    - finding: "platelets_x10_9_l"
      threshold: 50
      comparator: "<"
    - finding: "hemoglobin_g_dl"
      threshold: 8
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "T-PLL cytopenias are disease-driven; alemtuzumab causes profound CD52+ lymphocyte depletion (months). Supportive care + opportunistic infection prophylaxis essential.",
    },
    {
        "file": "rf_t_pll_infection_screening.yaml",
        "id": "RF-T-PLL-INFECTION-SCREENING",
        "disease": "DIS-T-PLL",
        "definition": "CMV PCR + HBV/HCV/HIV serology + PCP prophylaxis pre-alemtuzumab — alemtuzumab reactivates CMV in ~30%; PCP prophylaxis mandatory for ≥6 months post-treatment.",
        "definition_ua": "CMV PCR + HBV/HCV/HIV серологія + PCP профілактика перед alemtuzumab — alemtuzumab реактивує CMV у ~30%; PCP профілактика обов'язкова ≥6 міс після терапії.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "cmv_pcr_blood_positive"
      value: true
    - finding: "hbsag"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Alemtuzumab CMV reactivation is the dominant infectious complication; weekly CMV PCR monitoring + pre-emptive ganciclovir threshold is standard of care.",
    },
    {
        "file": "rf_t_pll_high_risk_biology.yaml",
        "id": "RF-T-PLL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-T-PLL",
        "definition": "Complex karyotype (≥3 abnormalities), TP53 mutation/deletion, or Ki-67 >40% — aggressive variant; alemtuzumab response shorter; alloSCT consolidation prioritized.",
        "definition_ua": "Складний каріотип (≥3 аномалій), мутація/делеція TP53 або Ki-67 >40% — агресивний варіант; відповідь на alemtuzumab коротша; alloSCT консолідація пріоритетна.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "complex_karyotype"
      value: true
    - finding: "tp53_mutation"
      value: true
    - finding: "ki67_above_40_percent"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Complex karyotype/TP53 in T-PLL predicts alemtuzumab response duration <6 months; alloSCT urgently while in CR1.",
    },
    {
        "file": "rf_t_pll_transformation_progression.yaml",
        "id": "RF-T-PLL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-T-PLL",
        "definition": "Failure to achieve CR after 12 weeks alemtuzumab IV OR rapid relapse — alloSCT urgently; venetoclax + ibrutinib or pentostatin/cladribine salvage as bridge.",
        "definition_ua": "Без CR після 12 тижнів alemtuzumab IV АБО швидкий рецидив — терміново alloSCT; venetoclax + ibrutinib або pentostatin/cladribine salvage як bridge.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "t_pll_no_cr_after_alemtuzumab"
      value: true
    - finding: "t_pll_rapid_relapse"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "T-PLL median OS without alloSCT ~7-12 months even with alemtuzumab CR. Refractory disease essentially requires transplant or palliative intent.",
    },
    {
        "file": "rf_t_pll_frailty_age.yaml",
        "id": "RF-T-PLL-FRAILTY-AGE",
        "disease": "DIS-T-PLL",
        "definition": "Age >75 OR not alloSCT-eligible (ECOG ≥3, severe organ dysfunction) — alemtuzumab still appropriate but with palliative intent; reduced-intensity-conditioning alloSCT considered if borderline.",
        "definition_ua": "Вік >75 АБО не кандидат на alloSCT (ECOG ≥3, важка органна дисфункція) — alemtuzumab все ще доречний, але з паліативним intent; reduced-intensity conditioning alloSCT якщо межовий.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 75
      comparator: ">"
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "T-PLL incurable without alloSCT; alemtuzumab is bridge only. Frailty surfaces palliative-intent realism in MDT brief.",
    },

    # ─── SMZL (5) — 2-arm: rituximab vs HCV-positive antiviral ─────────
    {
        "file": "rf_smzl_organ_dysfunction.yaml",
        "id": "RF-SMZL-ORGAN-DYSFUNCTION",
        "disease": "DIS-SPLENIC-MZL",
        "definition": "Severe portal hypertension (varices, ascites, splenic vein thrombosis) OR Child-Pugh B/C in HCV-associated SMZL — splenectomy contraindicated; rituximab monotherapy preferred.",
        "definition_ua": "Виражена портальна гіпертензія (варікози, асцит, тромбоз селезінкової вени) АБО Child-Pugh B/C у HCV-асоційованій SMZL — спленектомія протипоказана; rituximab монотерапія переважніша.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "portal_hypertension_severe"
      value: true
    - finding: "child_pugh_class"
      value: "B"
    - finding: "child_pugh_class"
      value: "C"
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "Splenectomy was historic SMZL standard; modern practice prefers rituximab esp. in cirrhosis where surgery risk is prohibitive. Decision drives Indication, not 1L Algorithm class.",
    },
    {
        "file": "rf_smzl_infection_screening.yaml",
        "id": "RF-SMZL-INFECTION-SCREENING",
        "disease": "DIS-SPLENIC-MZL",
        "definition": "HCV RNA PCR mandatory at SMZL diagnosis — HCV-driven SMZL responds to direct-acting antivirals (DAA) with regression in 50-75%; rituximab deferred until antiviral response assessed.",
        "definition_ua": "HCV RNA PCR обов'язково при діагнозі SMZL — HCV-індукована SMZL відповідає на DAA з регресією в 50-75%; rituximab відкладається до оцінки антивірусної відповіді.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hcv_rna_positive"
      value: true
    - finding: "anti_hcv"
      value: "positive"
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": ["ALGO-SMZL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "HCV-positive SMZL is etiologically distinct — DAA antiviral therapy alone induces lymphoma response in majority. Rituximab reserved for HCV-negative or DAA non-responders.",
    },
    {
        "file": "rf_smzl_high_risk_biology.yaml",
        "id": "RF-SMZL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-SPLENIC-MZL",
        "definition": "TP53 mutation, NOTCH2 mutation, or 7q deletion — aggressive SMZL variant with shorter PFS; consider rituximab + bendamustine over rituximab monotherapy.",
        "definition_ua": "TP53 мутація, NOTCH2 мутація або 7q делеція — агресивний варіант SMZL з коротшим PFS; розглянути rituximab + bendamustine над rituximab моно.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "tp53_mutation"
      value: true
    - finding: "notch2_mutation"
      value: true
    - finding: "del_7q"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "Adverse molecular markers in SMZL are emerging branch points; combination therapy (BR) over monotherapy is supportive-care-tested but not yet hard standard.",
    },
    {
        "file": "rf_smzl_transformation_progression.yaml",
        "id": "RF-SMZL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-SPLENIC-MZL",
        "definition": "Histologic transformation to DLBCL (rapid progression, new constitutional symptoms, LDH spike) — biopsy-confirmed transformation reclassifies as DLBCL pathway.",
        "definition_ua": "Гістологічна трансформація в DLBCL (швидка прогресія, нові constitutional симптоми, стрибок LDH) — biopsy-підтверджена трансформація реклассифікує як DLBCL шлях.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "biopsy_shows_dlbcl"
      value: true
    - finding: "smzl_transformation_suspected"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "Transformation to DLBCL changes the disease classification entirely — the engine should hand off to DLBCL Algorithm with the DLBCL biopsy result.",
    },
    {
        "file": "rf_smzl_frailty_age.yaml",
        "id": "RF-SMZL-FRAILTY-AGE",
        "disease": "DIS-SPLENIC-MZL",
        "definition": "Age >80 OR ECOG ≥3 with significant comorbidity AND asymptomatic SMZL — watch-and-wait may be more appropriate than active treatment.",
        "definition_ua": "Вік >80 АБО ECOG ≥3 з суттєвою коморбідністю І асимптоматична SMZL — watch-and-wait може бути доречнішим за активну терапію.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  all_of:
    - finding: "smzl_asymptomatic"
      value: true
    - any_of:
        - finding: "age_years"
          threshold: 80
          comparator: ">"
        - all_of:
            - finding: "ecog_status"
              threshold: 3
              comparator: ">="
            - finding: "comorbidity_count"
              threshold: 2
              comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "SMZL is indolent; in asymptomatic elderly, observation is GELF/iwCLL-style standard of care. Active treatment only for cytopenias / symptomatic splenomegaly / B-symptoms.",
    },
]


TEMPLATE = """id: {id}
definition: "{definition}"
definition_ua: "{definition_ua}"

{trigger_yaml}

clinical_direction: {direction}
severity: {severity}
priority: 100

relevant_diseases: [{disease}]
shifts_algorithm: {shifts}

sources:
{sources_block}

last_reviewed: "2026-04-25"
draft: false

notes: >
  {notes}
"""


def write_yaml(spec: dict) -> str:
    shifts = "[" + ", ".join(spec["shifts"]) + "]" if spec["shifts"] else "[]"
    sources_block = "\n".join(f"  - {s}" for s in spec["sources"])
    return TEMPLATE.format(
        id=spec["id"],
        definition=spec["definition"].replace('"', '\\"'),
        definition_ua=spec["definition_ua"].replace('"', '\\"'),
        trigger_yaml=spec["trigger_yaml"],
        direction=spec["direction"],
        severity=spec["severity"],
        disease=spec["disease"],
        shifts=shifts,
        sources_block=sources_block,
        notes=spec["notes"],
    )


def main() -> int:
    written = 0
    for spec in SPECS:
        target = RF_DIR / spec["file"]
        target.write_text(write_yaml(spec), encoding="utf-8")
        written += 1
        print(f"wrote {spec['file']}")
    print(f"\nDone. Filled {written} MEDIUM-priority scaffolds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
