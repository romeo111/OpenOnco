# Re-evaluation Task: HN3-037

## Context
- **Case ID**: HN3-037
- **Cancer type**: HPV-Positive Oropharyngeal Squamous Cell Carcinoma in HIV/AIDS Patient
- **Stage**: T2N1M0 (AJCC 8th Edition Stage I, p16+)
- **Molecular profile**: HPV-positive (p16+), PD-L1 CPS >=20, HIV/AIDS on ART, CD4 350 cells/uL, Undetectable viral load
- **Report file**: experiment_reports\HN3-037_report.json
- **Current score**: 68/100
- **Gap analysis (local GPU)**: The lack of data on concurrent cisplatin + IMRT (70 Gy) with INSTI-bas and concurrent carboplatin/5-FU + IMRT (cisplatin-inel) regimens is a critical gap, as these combinations are commonly used in cancer treatment and their efficacy needs to be evaluated. Filling these gaps will improve the score by providing more comprehensive information on the effectiveness of these treatments, which is essential for making informed treatment decisions and improving patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-037_report.json`.

Your task: Fix ONLY the `rating_breakdown` fields in the `treatments` array.

For each treatment, verify:
1. `evidence_level.score` matches the actual study phase:
   - Phase 3 RCT (N>=500, top journal) = 9-10
   - Phase 3 RCT (N<500) = 7-8
   - Phase 2 = 5-7
   - Phase 1 = 2-4
   - Case series / retrospective = 1-3
2. `survival_benefit.score` matches actual OS delta:
   - >12 months delta = 9-10
   - 6-12 months = 7-8
   - 3-6 months = 5-6
   - 1-3 months = 3-4
   - <1 month or no control = 1-2
3. `composite_rating` = weighted average (evidence 30%, survival 30%, access 15%, safety 15%, biomarker 10%)
4. Treatments must be re-sorted descending by composite_rating after changes

Do NOT change any other field. Return the complete corrected `treatments` array only.

## Output format

Return a valid JSON object containing ONLY the corrected section (e.g., `{"treatments": [...]}` or `{"sources": [...]}`).

Do NOT return the full report — only the corrected array. The runner will merge it back.

After returning the JSON, add one line:
`SCORE_IMPACT: <estimated new score>/100`

## Report JSON (for reference)

```json
{
  "report_metadata": {
    "generated_date": "2026-03-23",
    "cancer_type": "HPV-Positive Oropharyngeal Squamous Cell Carcinoma in HIV/AIDS Patient",
    "stage": "T2N1M0 (AJCC 8th Edition Stage I, p16+)",
    "molecular_profile": [
      "HPV-positive (p16+)",
      "PD-L1 CPS >=20",
      "HIV/AIDS on ART",
      "CD4 350 cells/uL",
      "Undetectable viral load"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Concurrent cisplatin + IMRT (70 Gy) with INSTI-based ART optimization",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "RTOG 1016 and ASTRO 2024 guidelines confirm cisplatin + RT as standard of care for HPV+ OPC. 70 Gy with concurrent cisplatin remains gold standard. T2N1 is borderline for concurrent systemic therapy (single node <=3cm may be RT alone)."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 84.6% with cisplatin + RT in RTOG 1016 for HPV+ OPC. HIV-positive patients have worse outcomes (greater hazards for recurrence and death), making intensified therapy important. Standard CRT remains superior to de-intensification."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Cisplatin and IMRT universally available. Standard regimen at all oncology centers. ART optimization with INSTI-based regimen minimizes drug interactions."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Must switch from TDF to TAF or abacavir to avoid compounding cisplatin nephrotoxicity. Overlapping toxicities: cisplatin nephrotoxicity + TDF renal effects, NRTI neuropathy + cisplatin neuropathy. CD4 will drop ~200 cells during CRT. Enhanced mucositis monitoring needed."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "HPV+ tumors are highly radiosensitive. PD-L1 CPS>=20 indicates robust immune microenvironment. CD4 350 is adequate for treatment tolerance. Undetectable VL indicates good ART adherence."
        }
      },
      "mechanism_of_action": "Cisplatin forms DNA crosslinks that impair repair of radiation-induced double-strand breaks, providing radiosensitization. IMRT delivers 70 Gy to gross disease with conformal dose distribution. ART must be optimized to INSTI-based backbone (dolutegravir/bictegravir + TAF/emtricitabine) to minimize drug interactions and overlapping nephrotoxicity with cisplatin.",
      "key_evidence": {
        "study_name": "NRG Oncology RTOG 1016 / ASTRO HPV+ OPC Guideline 2024",
        "journal": "Lancet / Practical Radiation Oncology",
        "year": 2024,
        "sample_size": 849,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 1.45,
          "p_value": 0.0163
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
 
... (truncated — read full file from experiment_reports\HN3-037_report.json)
```
