"""Fill LOW-priority RedFlag scaffolds (10 RFs across NMZL + NLPBL).

NMZL (nodal MZL) shares much of its biology with FL — algorithm already
references RF-FL-* flags. NMZL-specific RFs are mostly investigate-only.

NLPBL (nodular lymphocyte-predominant B-cell lymphoma) is indolent;
algorithm has 2 arms (observation-or-RT vs rituximab-mono). RFs are
mostly investigate-only or de-escalate.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"

SPECS: list[dict] = [
    # ─── NMZL (5) — nodal MZL ──────────────────────────────────────────
    {
        "file": "rf_nmzl_organ_dysfunction.yaml",
        "id": "RF-NMZL-ORGAN-DYSFUNCTION",
        "disease": "DIS-NODAL-MZL",
        "definition": "Renal dysfunction (CrCl <40 mL/min) — bendamustine clearance reduced; dose adjustment or alternative regimen (R-CHOP or rituximab monotherapy) considered.",
        "definition_ua": "Ниркова дисфункція (CrCl <40 мл/хв) — кліренс bendamustine знижений; коригування дози або альтернативний режим (R-CHOP або rituximab моно).",
        "trigger_yaml": """trigger:
  type: lab_value
  any_of:
    - finding: "creatinine_clearance_ml_min"
      threshold: 40
      comparator: "<"
""",
        "direction": "investigate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "Bendamustine renally cleared; dose reduce 25-50% if CrCl 30-50 mL/min, avoid <30 mL/min.",
    },
    {
        "file": "rf_nmzl_infection_screening.yaml",
        "id": "RF-NMZL-INFECTION-SCREENING",
        "disease": "DIS-NODAL-MZL",
        "definition": "HBV/HCV/HIV serology mandatory pre-rituximab; no NMZL-specific infectious driver established (unlike HCV-MZL or H. pylori gastric MALT).",
        "definition_ua": "HBV/HCV/HIV серологія обов'язково перед rituximab; на відміну від HCV-MZL або H. pylori шлункова MALT, NMZL не має встановленого інфекційного драйвера.",
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
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "Cross-disease HBV reactivation risk handled by RF-UNIVERSAL-HBV-REACTIVATION-RISK; this disease-specific entry kept for NMZL MDT-brief annotation.",
    },
    {
        "file": "rf_nmzl_high_risk_biology.yaml",
        "id": "RF-NMZL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-NODAL-MZL",
        "definition": "TP53 mutation, NOTCH2 mutation (shared with SMZL), or aggressive histologic features — shorter PFS; favor R-CHOP or BR over rituximab monotherapy.",
        "definition_ua": "TP53 мутація, NOTCH2 мутація (спільна з SMZL), або агресивні гістологічні риси — коротший PFS; R-CHOP або BR над rituximab моно.",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "tp53_mutation"
      value: true
    - finding: "notch2_mutation"
      value: true
""",
        "direction": "intensify",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "NMZL molecular landscape overlaps SMZL; adverse markers warrant combination chemoimmuno. Indication-level decision.",
    },
    {
        "file": "rf_nmzl_transformation_progression.yaml",
        "id": "RF-NMZL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-NODAL-MZL",
        "definition": "Histologic transformation to DLBCL (already wired through RF-FL-TRANSFORMATION-SUSPECT in ALGO-NMZL-1L) — biopsy-confirmed transformation reclassifies as DLBCL pathway.",
        "definition_ua": "Гістологічна трансформація в DLBCL (вже wired через RF-FL-TRANSFORMATION-SUSPECT у ALGO-NMZL-1L) — biopsy-підтверджена трансформація реклассифікує як DLBCL шлях.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "biopsy_shows_dlbcl"
      value: true
    - finding: "nmzl_transformation_suspected"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-MZL-2024"],
        "notes": "ALGO-NMZL-1L already imports RF-FL-TRANSFORMATION-SUSPECT; this NMZL-specific entry duplicates that semantically. Kept distinct for MDT-brief disease-context labeling.",
    },
    {
        "file": "rf_nmzl_frailty_age.yaml",
        "id": "RF-NMZL-FRAILTY-AGE",
        "disease": "DIS-NODAL-MZL",
        "definition": "Age >80 OR ECOG ≥3 with comorbidity AND asymptomatic NMZL (no GELF criteria) — observation appropriate; rituximab monotherapy if treatment indicated.",
        "definition_ua": "Вік >80 АБО ECOG ≥3 з коморбідностями І асимптоматична NMZL (без GELF) — спостереження доречне; rituximab моно якщо потрібне лікування.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  all_of:
    - finding: "nmzl_asymptomatic"
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
        "notes": "NMZL is indolent like FL; watch-and-wait standard for asymptomatic. Active treatment reserved for symptomatic burden.",
    },

    # ─── NLPBL (5) — nodular LP B-cell lymphoma ───────────────────────
    {
        "file": "rf_nlpbl_organ_dysfunction.yaml",
        "id": "RF-NLPBL-ORGAN-DYSFUNCTION",
        "disease": "DIS-NLPBL",
        "definition": "Pulmonary or cardiac dysfunction in field-of-RT region — radiation contraindicated; rituximab monotherapy or systemic chemo alternative.",
        "definition_ua": "Легенева або кардіальна дисфункція в зоні RT — променева протипоказана; rituximab моно або системна хіміо альтернатива.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "pulmonary_dysfunction_rt_field"
      value: true
    - finding: "cardiac_dysfunction_rt_field"
      value: true
    - finding: "lvef_percent"
      threshold: 50
      comparator: "<"
""",
        "direction": "de-escalate",
        "severity": "major",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-HODGKIN-2024"],
        "notes": "NLPBL is highly responsive to RT; field-of-RT organ dysfunction is the main contraindication. Rituximab monotherapy + observation acceptable alternative.",
    },
    {
        "file": "rf_nlpbl_infection_screening.yaml",
        "id": "RF-NLPBL-INFECTION-SCREENING",
        "disease": "DIS-NLPBL",
        "definition": "HBV/HCV/HIV serology pre-rituximab. NLPBL not associated with EBV (unlike classical Hodgkin); serology routine, not diagnostic.",
        "definition_ua": "HBV/HCV/HIV серологія перед rituximab. NLPBL не асоційована з EBV (на відміну від класичної Ходжкіна); серологія рутинна, не діагностична.",
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
        "severity": "minor",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-HODGKIN-2024"],
        "notes": "Standard pre-anti-CD20 screening; HBV reactivation handled by universal RF.",
    },
    {
        "file": "rf_nlpbl_high_risk_biology.yaml",
        "id": "RF-NLPBL-HIGH-RISK-BIOLOGY",
        "disease": "DIS-NLPBL",
        "definition": "Variant histology (T-cell rich, diffuse, or with histologic transformation to DLBCL/THRLBCL) — distinct from classical NLPBL nodular pattern; standard NLPBL approach inadequate, treat as aggressive B-cell lymphoma (R-CHOP-based).",
        "definition_ua": "Варіантна гістологія (T-cell rich, дифузна, або трансформація в DLBCL/THRLBCL) — відрізняється від класичної nodular NLPBL; стандартний NLPBL підхід недостатній, лікувати як агресивну B-клітинну лімфому (R-CHOP).",
        "trigger_yaml": """trigger:
  type: biomarker
  any_of:
    - finding: "nlpbl_variant_histology"
      value: true
    - finding: "thrlbcl_pattern"
      value: true
    - finding: "biopsy_shows_dlbcl"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-HODGKIN-2024"],
        "notes": "Variant pattern NLPBL behaves like aggressive B-cell lymphoma; reclassification to DLBCL pathway expected.",
    },
    {
        "file": "rf_nlpbl_transformation_progression.yaml",
        "id": "RF-NLPBL-TRANSFORMATION-PROGRESSION",
        "disease": "DIS-NLPBL",
        "definition": "Multiple relapses or histologic transformation to DLBCL/THRLBCL on rebiopsy — switch to aggressive B-cell pathway (R-CHOP-based ± autoSCT consideration).",
        "definition_ua": "Множинні рецидиви або гістологічна трансформація в DLBCL/THRLBCL на повторній біопсії — перехід на агресивний B-cell шлях (R-CHOP ± autoSCT).",
        "trigger_yaml": """trigger:
  type: composite_clinical
  any_of:
    - finding: "nlpbl_multiple_relapses"
      value: true
    - finding: "biopsy_shows_dlbcl"
      value: true
""",
        "direction": "intensify",
        "severity": "critical",
        "shifts": [],
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-HODGKIN-2024"],
        "notes": "Transformation rate ~7-15% over 10 years; outcomes after transformation depend on aggressive-lymphoma-pathway response.",
    },
    {
        "file": "rf_nlpbl_frailty_age.yaml",
        "id": "RF-NLPBL-FRAILTY-AGE",
        "disease": "DIS-NLPBL",
        "definition": "Age >75 + ECOG ≥3 with asymptomatic stage I-II disease — observation alone is appropriate (NLPBL indolent natural history); RT spared.",
        "definition_ua": "Вік >75 + ECOG ≥3 з асимптоматичною стадією I-II — спостереження достатнє (NLPBL індолентний перебіг); RT не потрібна.",
        "trigger_yaml": """trigger:
  type: composite_clinical
  all_of:
    - finding: "nlpbl_stage_i_or_ii"
      value: true
    - finding: "nlpbl_asymptomatic"
      value: true
    - any_of:
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
        "sources": ["SRC-NCCN-BCELL-2025", "SRC-ESMO-HODGKIN-2024"],
        "notes": "NLPBL has near-normal life expectancy in indolent forms; treatment de-escalation prioritized in elderly.",
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
    print(f"\nDone. Filled {written} LOW-priority scaffolds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
