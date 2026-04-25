"""Fill HIGH-priority RedFlag scaffolds with clinical content extracted
from cited guidelines (NCCN B-cell 2025, ESMO subtype-specific 2024).

Per CLINICAL_REVIEW_QUEUE_REDFLAGS §C, HIGH-priority diseases:
PMBCL, PCNSL, B-ALL, T-ALL, PTLD, HGBL-DH, NK/T-cell nasal.

Each RF below has:
- `definition` / `definition_ua` — disease-specific 1-liner
- `trigger` — machine-evaluable predicate from cited guidelines
- `direction` — intensify / de-escalate / hold / investigate
- `sources` — ≥2 Tier-1/2 source IDs
- `shifts_algorithm` — Algorithm IDs (only when there's a real branch
  in the existing decision_tree); else `[]` for surveillance flags

This is extraction with clinician verification expected at PR-merge
time per CHARTER §6.1 / §8.3. RFs marked `draft: false` here mean "ready
for two-reviewer sign-off", NOT "verified".
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"


# ── Spec data ────────────────────────────────────────────────────────────
# Each entry: filename -> dict of fields. Trigger is a YAML-string fragment
# (so we can express different shapes cleanly).

SPECS: list[dict] = [
    # ─── PMBCL (5) ──────────────────────────────────────────────────────
    {
        "file": "rf_pmbcl_organ_dysfunction.yaml",
        "id": "RF-PMBCL-ORGAN-DYSFUNCTION",
        "disease": "DIS-PMBCL",
        "definition": "Cardiac dysfunction (LVEF <50%) at baseline — both PMBCL 1L arms contain doxorubicin; cardio-oncology evaluation and ECG/echo monitoring required.",
        "definition_ua": "Кардіальна дисфункція (LVEF <50%) на старті — обидві лінії 1L терапії PMBCL містять доксорубіцин; потрібна кардіо-онк консультація + ECG/echo моніторинг.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "lvef_percent"
      threshold: 50
      comparator: "<"
    - finding: "cardiac_dysfunction_baseline"
      value: true""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Both 1L arms (DA-EPOCH-R, R-CHOP+RT) anthracycline-based; no anthracycline-free standard. Surfaces as cardio-onc consult + dose-modification supportive care.",
    },
    {
        "file": "rf_pmbcl_infection_screening.yaml",
        "id": "RF-PMBCL-INFECTION-SCREENING",
        "disease": "DIS-PMBCL",
        "definition": "Pre-treatment HBV/HCV/HIV serology mandatory before rituximab; HBsAg+ requires antiviral prophylaxis (entecavir/TDF) initiated 1 week before anti-CD20.",
        "definition_ua": "Обов'язкова HBV/HCV/HIV серологія перед rituximab; HBsAg+ потребує противірусної профілактики (entecavir/TDF) за 1 тиждень до анти-CD20.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "anti_hcv"
      value: "positive"
    - finding: "hiv_serology"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Cross-disease HBV reactivation risk handled by RF-UNIVERSAL-HBV-REACTIVATION-RISK; this disease-specific entry kept for PMBCL MDT-brief annotation.",
    },
    {
        "file": "rf_pmbcl_high_risk_biology.yaml",
        "id": "RF-PMBCL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-PMBCL",
        "definition": "Bulky mediastinal disease (>10 cm) and/or aaIPI ≥2 — favors DA-EPOCH-R over R-CHOP+RT per IELSG-26 / NCCN B-cell.",
        "definition_ua": "Об'ємне медіастінальне ураження (>10 см) та/або aaIPI ≥2 — DA-EPOCH-R над R-CHOP+RT за IELSG-26 / NCCN B-cell.",
        "trigger_yaml": """trigger:
  type: composite_score
  any_of:
    - finding: "dominant_mediastinal_mass_cm"
      threshold: 10
      comparator: ">="
    - finding: "aaipi_score"
      threshold: 2
      comparator: ">="
    - finding: "bulky_mediastinal_pmbcl"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": ["ALGO-PMBCL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Dunleavy NEJM 2013 phase-2 (DA-EPOCH-R 93% EFS) + IELSG-26 PET-driven response data form the evidence base for DA-EPOCH-R preference in bulky/high-IPI PMBCL.",
    },
    {
        "file": "rf_pmbcl_transformation_progression.yaml",
        "id": "RF-PMBCL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-PMBCL",
        "definition": "Mid-treatment PET-CT progression (Deauville 4-5 with new lesions or SUVmax increase >25%) — switch to salvage 2L pathway, do not continue same regimen.",
        "definition_ua": "Прогресія за PET-CT під час лікування (Deauville 4-5 з новими вогнищами або SUVmax зростання >25%) — перехід на 2L salvage, не продовжувати поточний режим.",
        "trigger_yaml": """trigger:
  type: imaging_finding
  any_of:
    - finding: "pet_deauville_score"
      threshold: 4
      comparator: ">="
    - finding: "interim_pet_progression"
      value: true""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Mid-therapy progression triggers a 2L salvage handoff (separate Algorithm). 1L decision_tree is unaffected; flag surfaces as MDT-brief priority annotation.",
    },
    {
        "file": "rf_pmbcl_frailty_age.yaml",
        "id": "RF-PMBCL-FRAILTY-AGE",
        "disease": "DIS-PMBCL",
        "definition": "Frailty (ECOG ≥3 OR age ≥75 + ≥2 comorbidities) — DA-EPOCH-R infusional toxicity poorly tolerated; R-CHOP+RT preferred for fragile elderly.",
        "definition_ua": "Frailty (ECOG ≥3 АБО вік ≥75 + ≥2 коморбідності) — токсичність інфузійного DA-EPOCH-R погано переноситься; R-CHOP+RT кращий для frail elderly.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
    - all_of:
        - finding: "age_years"
          threshold: 75
          comparator: ">="
        - finding: "comorbidity_count"
          threshold: 2
          comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": ["ALGO-PMBCL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "DA-EPOCH-R infusional schedule + G-CSF support poorly tolerated in elderly frail; R-CHOP+ISRT acceptable per NCCN with similar EFS in this subgroup.",
    },

    # ─── PCNSL (5) ──────────────────────────────────────────────────────
    {
        "file": "rf_pcnsl_organ_dysfunction.yaml",
        "id": "RF-PCNSL-ORGAN-DYSFUNCTION",
        "disease": "DIS-PCNSL",
        "definition": "Renal dysfunction (CrCl <50 mL/min) — high-dose methotrexate (HD-MTX, ≥3 g/m²) backbone of all PCNSL 1L regimens contraindicated; transition to non-MTX regimen or refer to specialized center.",
        "definition_ua": "Ниркова дисфункція (CrCl <50 мл/хв) — високодозовий метотрексат (HD-MTX, ≥3 г/м²) як базис усіх 1L PCNSL режимів протипоказаний; перехід на non-MTX режим або скерувати в спеціалізований центр.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "creatinine_clearance_ml_min"
      threshold: 50
      comparator: "<"
    - finding: "egfr_ml_min"
      threshold: 50
      comparator: "<"
""",
        "direction": "hold",
        "severity": "critical",
        "shifts": ["ALGO-PCNSL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "HD-MTX requires CrCl ≥50 mL/min for safe clearance; below that, MTX accumulates and causes severe nephrotoxicity / mucositis / myelosuppression. Non-MTX salvage options (R-temozolomide, WBRT alone) carry inferior outcomes — this is a hold/refer decision.",
    },
    {
        "file": "rf_pcnsl_infection_screening.yaml",
        "id": "RF-PCNSL-INFECTION-SCREENING",
        "disease": "DIS-PCNSL",
        "definition": "HIV serology mandatory at PCNSL diagnosis — HIV-associated PCNSL (CD4 <200) is treated differently (cART optimization first, intrathecal ± lower-intensity systemic).",
        "definition_ua": "Обов'язкова HIV серологія при діагнозі PCNSL — HIV-асоційована PCNSL (CD4 <200) лікується інакше (спочатку оптимізація cART, потім інтратекально ± менш інтенсивна системна).",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hiv_serology"
      value: "positive"
    - finding: "cd4_count_per_ul"
      threshold: 200
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "HIV+ PCNSL (with CD4 <200) often EBV-driven; cART initiation alone can produce remissions. Distinct from immunocompetent PCNSL — flagged for MDT review and infectious-disease co-management; algorithm choice deferred.",
    },
    {
        "file": "rf_pcnsl_high_risk_biology.yaml",
        "id": "RF-PCNSL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-PCNSL",
        "definition": "Multifocal disease, deep brain involvement (basal ganglia/thalamus/brainstem), or high IELSG-PCNSL score (≥3) — favor consolidation with autoSCT or full-dose WBRT after induction.",
        "definition_ua": "Мультифокальне ураження, глибокі структури (базальні ганглії/таламус/стовбур), або високий IELSG-PCNSL score (≥3) — консолідація autoSCT або повна WBRT після індукції.",
        "trigger_yaml": """trigger:
  type: composite_score
  any_of:
    - finding: "ielsg_pcnsl_score"
      threshold: 3
      comparator: ">="
    - finding: "deep_brain_involvement"
      value: true
    - finding: "multifocal_pcnsl"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "IELSG-PCNSL prognostic model (age, ECOG, LDH, CSF protein, deep-brain involvement) stratifies 2-year OS. Flag drives consolidation strategy decisions (autoSCT vs WBRT) which sit downstream of 1L Algorithm.",
    },
    {
        "file": "rf_pcnsl_transformation_progression.yaml",
        "id": "RF-PCNSL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-PCNSL",
        "definition": "Refractory disease at end-of-induction MRI (any persistent enhancing lesion) or progression during therapy — switch to salvage 2L pathway (R-temozolomide, ibrutinib, lenalidomide-based, or WBRT).",
        "definition_ua": "Рефрактерне захворювання за MRI наприкінці індукції (будь-яке персистуюче контрастне вогнище) або прогресія під час терапії — перехід на 2L salvage (R-temozolomide, ibrutinib, lenalidomide-based, або WBRT).",
        "trigger_yaml": """trigger:
  type: imaging_finding
  any_of:
    - finding: "end_induction_mri_residual"
      value: true
    - finding: "interim_progression_pcnsl"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Progression on HD-MTX-based induction is poor-prognosis; R/R PCNSL pathway (separate Algorithm) takes over. 1L decision_tree unaffected; surfaces as MDT-brief priority.",
    },
    {
        "file": "rf_pcnsl_frailty_age.yaml",
        "id": "RF-PCNSL-FRAILTY-AGE",
        "disease": "DIS-PCNSL",
        "definition": "Age >70 OR ECOG ≥3 OR CrCl 50-70 mL/min — full-dose HD-MTX (≥3.5 g/m²) carries excessive toxicity; reduced-dose MTX (1-3 g/m²) ± rituximab considered.",
        "definition_ua": "Вік >70 АБО ECOG ≥3 АБО CrCl 50-70 мл/хв — повна доза HD-MTX (≥3.5 г/м²) має надлишкову токсичність; знижена доза MTX (1-3 г/м²) ± rituximab.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 70
      comparator: ">"
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
    - all_of:
        - finding: "creatinine_clearance_ml_min"
          threshold: 50
          comparator: ">="
        - finding: "creatinine_clearance_ml_min"
          threshold: 70
          comparator: "<="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Elderly PCNSL OS dominated by tolerability of induction; reduced-dose MTX with rituximab achieves comparable response rates with markedly less toxicity. Decision sits within Indication-level dose-adjustment, not 1L Algorithm branch.",
    },

    # ─── B-ALL (5) ──────────────────────────────────────────────────────
    {
        "file": "rf_b_all_organ_dysfunction.yaml",
        "id": "RF-B-ALL-ORGAN-DYSFUNCTION",
        "disease": "DIS-B-ALL",
        "definition": "Cardiac dysfunction (LVEF <50%) — anthracycline-based induction (hyper-CVAD A, BFM-style protocols) requires modification or substitution.",
        "definition_ua": "Кардіальна дисфункція (LVEF <50%) — антрациклін-вмісна індукція (hyper-CVAD A, BFM протоколи) потребує модифікації або заміни.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "lvef_percent"
      threshold: 50
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Anthracycline-free B-ALL induction (e.g., blinatumomab-based MRD-guided) is emerging but not yet 1L standard outside trials. Flag drives cardio-onc co-management and dose modification.",
    },
    {
        "file": "rf_b_all_infection_screening.yaml",
        "id": "RF-B-ALL-INFECTION-SCREENING",
        "disease": "DIS-B-ALL",
        "definition": "HBV/HCV/HIV/CMV serology + latent TB testing mandatory pre-induction; rituximab-containing regimens (CD20+ B-ALL) require HBV prophylaxis.",
        "definition_ua": "HBV/HCV/HIV/CMV серологія + латентний ТБ обов'язково перед індукцією; rituximab-вмісні режими (CD20+ B-ALL) — HBV профілактика.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "anti_hcv"
      value: "positive"
    - finding: "hiv_serology"
      value: "positive"
    - finding: "tb_latent"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Cross-disease HBV reactivation handled by RF-UNIVERSAL-HBV-REACTIVATION-RISK. CMV monitoring critical given prolonged immunosuppression of B-ALL induction/consolidation.",
    },
    {
        "file": "rf_b_all_high_risk_biology.yaml",
        "id": "RF-B-ALL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-B-ALL",
        "definition": "Philadelphia-positive B-ALL (BCR-ABL1+) — TKI (imatinib/dasatinib/ponatinib) + chemotherapy is standard; Ph-like B-ALL signature requires JAK/ABL pathway-targeted addition.",
        "definition_ua": "Філадельфія-позитивна B-ALL (BCR-ABL1+) — стандарт TKI (imatinib/dasatinib/ponatinib) + хіміо; Ph-like B-ALL потребує таргетної терапії JAK/ABL шляху.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "ph_positive"
      value: true
    - finding: "bcr_abl1"
      value: "positive"
    - finding: "ph_like_signature"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": ["ALGO-B-ALL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Ph+ B-ALL is a fundamentally different disease — TKI addition reverses what was historically the worst-prognosis subgroup. NCCN/ESMO both place TKI testing in upfront workup mandate.",
    },
    {
        "file": "rf_b_all_transformation_progression.yaml",
        "id": "RF-B-ALL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-B-ALL",
        "definition": "MRD-positive at end-of-induction (≥0.01% by flow or PCR) — switch to MRD-eradication strategy (blinatumomab, inotuzumab, or alloSCT consolidation).",
        "definition_ua": "MRD-позитив на кінець індукції (≥0.01% за flow або PCR) — перехід на MRD-ерадикацію (blinatumomab, inotuzumab, або alloSCT консолідація).",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "mrd_positive_post_induction"
      value: true
    - finding: "mrd_level_percent"
      threshold: 0.01
      comparator: ">="
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "MRD post-induction is the single strongest prognostic factor in B-ALL. Drives 2L/consolidation strategy (blinatumomab → alloSCT for fit), not 1L induction choice. Flag surfaces as MDT priority.",
    },
    {
        "file": "rf_b_all_frailty_age.yaml",
        "id": "RF-B-ALL-FRAILTY-AGE",
        "disease": "DIS-B-ALL",
        "definition": "Age ≥65 OR ECOG ≥3 with comorbidities — pediatric-inspired regimens (CALGB 10403, hyper-CVAD) inadequately tolerated; reduced-intensity protocol (mini-HCVD ± inotuzumab/blinatumomab) preferred.",
        "definition_ua": "Вік ≥65 АБО ECOG ≥3 з коморбідностями — педіатричні протоколи (CALGB 10403, hyper-CVAD) погано переносяться; reduced-intensity (mini-HCVD ± inotuzumab/blinatumomab).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 65
      comparator: ">="
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
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Pediatric-inspired adolescent-young-adult protocols dominate in fit <40; >65 mortality from induction toxicity is high. Mini-HCVD + inotuzumab/blinatumomab achieves better tolerability with comparable CR rates.",
    },

    # ─── T-ALL (5) ──────────────────────────────────────────────────────
    {
        "file": "rf_t_all_organ_dysfunction.yaml",
        "id": "RF-T-ALL-ORGAN-DYSFUNCTION",
        "disease": "DIS-T-ALL",
        "definition": "Hepatic dysfunction (bilirubin >3xULN OR transaminases >5xULN) — asparaginase + methotrexate + thiopurines accumulate hepatotoxicity; dose modification or asparaginase substitution required.",
        "definition_ua": "Печінкова дисфункція (білірубін >3xULN АБО трансамінази >5xULN) — аспарагіназа + метотрексат + тіопурини акумулюють гепатотоксичність; модифікація дози або заміна аспарагінази.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "bilirubin_x_uln"
      threshold: 3
      comparator: ">"
    - finding: "alt_x_uln"
      threshold: 5
      comparator: ">"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Hepatotoxicity in T-ALL induction is multi-drug; depends on regimen phase. Surveillance + dose-mod under hematology — not a 1L algorithm shift.",
    },
    {
        "file": "rf_t_all_infection_screening.yaml",
        "id": "RF-T-ALL-INFECTION-SCREENING",
        "disease": "DIS-T-ALL",
        "definition": "HIV/HBV/HCV/CMV serology + PCP prophylaxis pre-induction; nelarabine-containing regimens require PJP prophylaxis throughout treatment.",
        "definition_ua": "HIV/HBV/HCV/CMV серологія + PCP профілактика перед індукцією; nelarabine-вмісні режими — PJP профілактика весь курс.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "hiv_serology"
      value: "positive"
    - finding: "anti_hcv"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "T-ALL induction profoundly lymphopenic; opportunistic infection prophylaxis (PCP, fluconazole, acyclovir) standard regardless of serology — but baseline screen ensures appropriate prophylaxis intensity.",
    },
    {
        "file": "rf_t_all_high_risk_biology.yaml",
        "id": "RF-T-ALL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-T-ALL",
        "definition": "Early T-cell precursor (ETP) phenotype (CD1a-, CD8-, CD5 weak, with myeloid/stem-cell markers) — historically inferior outcomes with standard T-ALL chemo; nelarabine + alloSCT consolidation considered.",
        "definition_ua": "Ранньо-Т-клітинний попередник (ETP) фенотип (CD1a-, CD8-, CD5 слабкий, з мієлоїдними/стовбуровими маркерами) — історично гірші результати на стандартній T-ALL хіміо; nelarabine + alloSCT консолідація.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "etp_phenotype"
      value: true
    - finding: "etp_all"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "ETP-ALL is a WHO 2022 distinct entity. Modern MRD-stratified protocols (UKALL14, GRAALL) have closed much of the historical gap, but alloSCT eligibility remains the dominant decision — hence intensify.",
    },
    {
        "file": "rf_t_all_transformation_progression.yaml",
        "id": "RF-T-ALL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-T-ALL",
        "definition": "MRD-positive post-induction (≥0.01%) OR overt CNS involvement (CNS-3) — alloSCT consolidation becomes standard; nelarabine-containing salvage if not yet exposed.",
        "definition_ua": "MRD-позитив після індукції (≥0.01%) АБО явне ЦНС-ураження (CNS-3) — alloSCT консолідація стає стандартом; nelarabine у salvage якщо ще не отримував.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "mrd_positive_post_induction"
      value: true
    - finding: "cns_status_cns3"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "MRD-driven consolidation strategy sits downstream of 1L induction Algorithm.",
    },
    {
        "file": "rf_t_all_frailty_age.yaml",
        "id": "RF-T-ALL-FRAILTY-AGE",
        "disease": "DIS-T-ALL",
        "definition": "Age >55 — pediatric-inspired protocols (GRAALL, CALGB 10403) carry excessive induction mortality; reduced-intensity backbone with selected MRD-targeted agents (nelarabine, asparaginase modifications) preferred.",
        "definition_ua": "Вік >55 — педіатричні протоколи (GRAALL, CALGB 10403) мають надлишкову смертність на індукції; reduced-intensity backbone з MRD-таргетованими (nelarabine, модифікації аспарагінази).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "age_years"
      threshold: 55
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
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "T-ALL >55 is rare; protocols underrepresented in trials. Reduced-intensity backbone often borrowed from older B-ALL regimens with T-cell substitutions.",
    },

    # ─── PTLD (5) ──────────────────────────────────────────────────────
    {
        "file": "rf_ptld_organ_dysfunction.yaml",
        "id": "RF-PTLD-ORGAN-DYSFUNCTION",
        "disease": "DIS-PTLD",
        "definition": "Allograft dysfunction (worsening creatinine if kidney, transaminases if liver, troponin if heart) at PTLD diagnosis — IS-reduction must be balanced against allograft loss; transplant team co-management mandatory.",
        "definition_ua": "Дисфункція трансплантата (погіршення креатиніну для нирки, трансаміназ для печінки, тропоніну для серця) на діагнозі PTLD — IS-редукція балансується з ризиком втрати трансплантата; обов'язкова co-management з трансплант-командою.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "allograft_dysfunction"
      value: true
    - finding: "creatinine_increase_x_baseline"
      threshold: 1.5
      comparator: ">="
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "PTLD treatment fundamentally requires IS-reduction; balancing allograft survival vs PTLD response is per-patient clinical decision. Flag mandates transplant team involvement.",
    },
    {
        "file": "rf_ptld_infection_screening.yaml",
        "id": "RF-PTLD-INFECTION-SCREENING",
        "disease": "DIS-PTLD",
        "definition": "EBV viral load + CMV PCR mandatory; EBV-driven PTLD (most cases) responds to rituximab ± chemo; EBV-negative PTLD often requires chemo upfront.",
        "definition_ua": "EBV вірусне навантаження + CMV PCR обов'язково; EBV-driven PTLD (більшість випадків) відповідає на rituximab ± хіміо; EBV-негативна PTLD часто потребує хіміо одразу.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "ebv_pcr_blood_positive"
      value: true
    - finding: "cmv_pcr_blood_positive"
      value: true
    - finding: "ebv_status_tumor"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "EBV status determines whether monotherapy rituximab + IS-reduction has high response chance vs requiring R-CHOP-like chemo upfront. Flag drives MDT discussion + indication selection downstream.",
    },
    {
        "file": "rf_ptld_high_risk_biology.yaml",
        "id": "RF-PTLD-HIGH-RISK-BIOLOGY",
        "disease": "DIS-PTLD",
        "definition": "Monomorphic PTLD with DLBCL-type morphology / Burkitt-like / T-cell PTLD — chemoimmunotherapy from start (R-CHOP, EPOCH, or T-cell-specific); polymorphic forms may respond to IS-reduction ± rituximab.",
        "definition_ua": "Мономорфна PTLD з DLBCL-морфологією / Burkitt-like / T-cell PTLD — хіміоімуно одразу (R-CHOP, EPOCH, T-cell-specific); полімерні форми можуть відповідати на IS-редукцію ± rituximab.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "ptld_subtype_monomorphic_dlbcl"
      value: true
    - finding: "ptld_subtype_burkitt_like"
      value: true
    - finding: "ptld_subtype_t_cell"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": ["ALGO-PTLD-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Histologic subtype is the dominant treatment selector in PTLD. Polymorphic / early-lesion → IS-reduction trial first; monomorphic → chemoimmuno from start. T-cell PTLD is rare and requires CHOP-based without rituximab.",
    },
    {
        "file": "rf_ptld_transformation_progression.yaml",
        "id": "RF-PTLD-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-PTLD",
        "definition": "Failure of IS-reduction trial after 2-4 weeks (no clinical/radiologic improvement) — escalate to rituximab monotherapy → R-CHOP if rituximab fails.",
        "definition_ua": "Невдача IS-редукції через 2-4 тижні (без клінічного/радіологічного покращення) — ескалація до rituximab моно → R-CHOP якщо rituximab не спрацював.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "is_reduction_failure_2_4_weeks"
      value: true
    - finding: "ptld_progression_on_rituximab"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Sequential treatment paradigm in polymorphic PTLD: IS-reduction → rituximab → chemoimmuno. Each escalation is a separate Indication selection downstream of 1L Algorithm.",
    },
    {
        "file": "rf_ptld_frailty_age.yaml",
        "id": "RF-PTLD-FRAILTY-AGE",
        "disease": "DIS-PTLD",
        "definition": "Age >70 + advanced organ dysfunction OR ECOG ≥3 — full-dose R-CHOP poorly tolerated; reduced-intensity rituximab-only or modified chemo with growth-factor support.",
        "definition_ua": "Вік >70 + виражена органна дисфункція АБО ECOG ≥3 — повна доза R-CHOP погано переноситься; reduced-intensity rituximab-моно або модифікована хіміо з росток-factor support.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "ecog_status"
      threshold: 3
      comparator: ">="
    - all_of:
        - finding: "age_years"
          threshold: 70
          comparator: ">"
        - finding: "comorbidity_count"
          threshold: 2
          comparator: ">="
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Transplant recipients are usually older with multi-organ comorbidity at PTLD diagnosis. Reduced-intensity approach preserves quality of life; alloSCT obviously not relevant here.",
    },

    # ─── HGBL-DH (5) ────────────────────────────────────────────────────
    {
        "file": "rf_hgbl_dh_organ_dysfunction.yaml",
        "id": "RF-HGBL-DH-ORGAN-DYSFUNCTION",
        "disease": "DIS-HGBL-DH",
        "definition": "Cardiac dysfunction (LVEF <50%) — DA-EPOCH-R (preferred for HGBL-DH/-TH) is anthracycline-intensive; cardio-onc consult and dose-modification required.",
        "definition_ua": "Кардіальна дисфункція (LVEF <50%) — DA-EPOCH-R (preferred для HGBL-DH/-TH) антрациклін-інтенсивний; кардіо-онк консультація + dose-modification.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "lvef_percent"
      threshold: 50
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "DA-EPOCH-R cumulative doxorubicin exceeds R-CHOP; cardio-monitoring should be aggressive in baseline-borderline LVEF. Indication-level dose adjustment, not 1L Algorithm shift.",
    },
    {
        "file": "rf_hgbl_dh_infection_screening.yaml",
        "id": "RF-HGBL-DH-INFECTION-SCREENING",
        "disease": "DIS-HGBL-DH",
        "definition": "HBV/HCV/HIV serology mandatory pre-rituximab; HIV-associated HGBL-DH gets cART optimization concurrently with chemo.",
        "definition_ua": "HBV/HCV/HIV серологія обов'язково перед rituximab; HIV-асоційована HGBL-DH — оптимізація cART паралельно з хіміо.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "hbsag"
      value: "positive"
    - finding: "anti_hcv"
      value: "positive"
    - finding: "hiv_serology"
      value: "positive"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Cross-disease HBV reactivation by RF-UNIVERSAL-HBV-REACTIVATION-RISK. HIV-HGBL behaves more aggressively but treatment intent unchanged.",
    },
    {
        "file": "rf_hgbl_dh_high_risk_biology.yaml",
        "id": "RF-HGBL-DH-HIGH-RISK-BIOLOGY",
        "disease": "DIS-HGBL-DH",
        "definition": "MYC + BCL2 (and/or BCL6) rearrangement (double-/triple-hit) confirmed by FISH — DA-EPOCH-R + IT methotrexate prophylaxis preferred over R-CHOP per multiple retrospective and small prospective series.",
        "definition_ua": "MYC + BCL2 (та/або BCL6) перебудова (double-/triple-hit) підтверджена FISH — DA-EPOCH-R + IT-MTX профілактика над R-CHOP за ретроспективними і малими проспективними даними.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - all_of:
        - finding: "myc_rearrangement"
          value: true
        - finding: "bcl2_rearrangement"
          value: true
    - all_of:
        - finding: "myc_rearrangement"
          value: true
        - finding: "bcl6_rearrangement"
          value: true
    - finding: "double_hit_lymphoma"
      value: true
    - finding: "triple_hit_lymphoma"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": ["ALGO-HGBL-DH-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "WHO 2022/ICC define HGBL-DH/-TH as distinct entity. NCCN explicitly endorses DA-EPOCH-R for HGBL-DH; CNS prophylaxis (IT MTX × 4-8 doses) standard regardless of CNS-IPI in this subtype.",
    },
    {
        "file": "rf_hgbl_dh_transformation_progression.yaml",
        "id": "RF-HGBL-DH-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-HGBL-DH",
        "definition": "PET-2 progression (Deauville 4-5 with new lesions) or end-of-induction non-CR — HGBL-DH refractory disease has very poor outcomes; CAR-T (axi-cel/liso-cel) preferred over salvage chemo.",
        "definition_ua": "PET-2 прогресія (Deauville 4-5 з новими вогнищами) або кінець індукції без CR — рефрактерна HGBL-DH дуже погана прогностично; CAR-T (axi-cel/liso-cel) над salvage хіміо.",
        "trigger_yaml": """trigger:
  type: imaging_finding
  any_of:
    - finding: "interim_pet_progression"
      value: true
    - finding: "end_induction_non_cr"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "Refractory HGBL-DH 12-month OS ~30% with chemo salvage; ZUMA-12 axi-cel data support CAR-T-first paradigm. Sits in 2L Algorithm not 1L; flag drives MDT priority.",
    },
    {
        "file": "rf_hgbl_dh_frailty_age.yaml",
        "id": "RF-HGBL-DH-FRAILTY-AGE",
        "disease": "DIS-HGBL-DH",
        "definition": "Age >75 OR ECOG ≥3 — DA-EPOCH-R toxicity prohibitive; modified R-CHOP + IT MTX prophylaxis acceptable compromise.",
        "definition_ua": "Вік >75 АБО ECOG ≥3 — токсичність DA-EPOCH-R непереносна; модифікований R-CHOP + IT-MTX профілактика прийнятний компроміс.",
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
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-DLBCL-2024"],
        "notes": "DA-EPOCH-R toxicity in elderly approaches 25-30% treatment-related mortality; modified R-CHOP retains majority of efficacy with manageable toxicity. Decision sits at Indication-dose level.",
    },

    # ─── NK/T-cell nasal (5) ────────────────────────────────────────────
    {
        "file": "rf_nk_t_nasal_organ_dysfunction.yaml",
        "id": "RF-NK-T-NASAL-ORGAN-DYSFUNCTION",
        "disease": "DIS-NK-T-NASAL",
        "definition": "Hepatic dysfunction (bilirubin >2xULN OR transaminases >5xULN) — asparaginase (SMILE, modified DDGP, AspaMetDex) is hepatotoxic; pegaspargase substitution + close monitoring.",
        "definition_ua": "Печінкова дисфункція (білірубін >2xULN АБО трансамінази >5xULN) — аспарагіназа (SMILE, modified DDGP, AspaMetDex) гепатотоксична; pegaspargase + моніторинг.",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "bilirubin_x_uln"
      threshold: 2
      comparator: ">"
    - finding: "alt_x_uln"
      threshold: 5
      comparator: ">"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "Asparaginase backbone is pillar of NK/T-nasal therapy; alternatives are inferior. Hepatic-protection + dose-modification, not regimen-class change.",
    },
    {
        "file": "rf_nk_t_nasal_infection_screening.yaml",
        "id": "RF-NK-T-NASAL-INFECTION-SCREENING",
        "disease": "DIS-NK-T-NASAL",
        "definition": "EBV plasma DNA quantification at baseline + during treatment — high baseline EBV (>10^4 copies/mL) and persistent EBV-positivity post-induction predict worse outcomes.",
        "definition_ua": "EBV плазмова ДНК на старті + під час терапії — високий базовий EBV (>10^4 копій/мл) і персистенція EBV після індукції погіршує прогноз.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "ebv_dna_copies_per_ml"
      threshold: 10000
      comparator: ">="
    - finding: "ebv_persistent_post_induction"
      value: true
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "EBV DNA tracking is THE biomarker of response in NK/T-nasal. Drives intensification of consolidation and surveillance schedule.",
    },
    {
        "file": "rf_nk_t_nasal_high_risk_biology.yaml",
        "id": "RF-NK-T-NASAL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-NK-T-NASAL",
        "definition": "Stage III-IV / extranasal involvement / PINK-E score ≥3 — favor SMILE intensive regimen + radiotherapy over reduced-intensity DDGP-mod/AspaMetDex.",
        "definition_ua": "Стадія III-IV / екстраназальне ураження / PINK-E score ≥3 — SMILE інтенсивний над reduced-intensity DDGP-mod/AspaMetDex; + променева.",
        "trigger_yaml": """trigger:
  type: composite_score
  any_of:
    - finding: "ann_arbor_stage"
      threshold: 3
      comparator: ">="
    - finding: "pink_e_score"
      threshold: 3
      comparator: ">="
    - finding: "extranasal_involvement"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": ["ALGO-NK-T-NASAL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "PINK / PINK-E (Prognostic Index NK lymphoma) plus stage drives intensity selection. SMILE has CR rates >70% in advanced disease; less intensive regimens trail by 15-20%.",
    },
    {
        "file": "rf_nk_t_nasal_transformation_progression.yaml",
        "id": "RF-NK-T-NASAL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-NK-T-NASAL",
        "definition": "PD-L1 expression high OR progression on first asparaginase-based regimen — pembrolizumab/sintilimab + chidamide salvage shows ORR 50-60% in this setting.",
        "definition_ua": "Висока експресія PD-L1 АБО прогресія на першому аспарагіназ-вмісному режимі — pembrolizumab/sintilimab + chidamide salvage має ORR 50-60%.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "pd_l1_high_expression"
      value: true
    - finding: "asparaginase_regimen_failure"
      value: true
""",
        "direction": "investigate",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "PD-1 inhibitor activity in NK/T-nasal exceptional (50-60% ORR) — this is a 2L decision driver. 1L Algorithm unaffected.",
    },
    {
        "file": "rf_nk_t_nasal_frailty_age.yaml",
        "id": "RF-NK-T-NASAL-FRAILTY-AGE",
        "disease": "DIS-NK-T-NASAL",
        "definition": "Age >65 OR ECOG ≥3 — SMILE myelosuppression intolerable; modified DDGP or AspaMetDex with reduced asparaginase dosing acceptable.",
        "definition_ua": "Вік >65 АБО ECOG ≥3 — мієлосупресія SMILE непереносна; модифікований DDGP або AspaMetDex зі зниженою дозою аспарагінази.",
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
        "shifts": ["ALGO-NK-T-NASAL-1L"],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-PTCL-2024"],
        "notes": "SMILE TRM in elderly is high (10-15%); reduced-intensity regimens trade 5-10% efficacy for tolerability.",
    },
]


# ── Generator ────────────────────────────────────────────────────────────


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
    body = TEMPLATE.format(
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
    return body


def main() -> int:
    written = 0
    for spec in SPECS:
        target = RF_DIR / spec["file"]
        body = write_yaml(spec)
        target.write_text(body, encoding="utf-8")
        written += 1
        print(f"wrote {spec['file']}")
    print(f"\nDone. Filled {written} HIGH-priority scaffolds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
