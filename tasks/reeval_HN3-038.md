# Re-evaluation Task: HN3-038

## Context
- **Case ID**: HN3-038
- **Cancer type**: Radiation-Induced Undifferentiated Pleomorphic Sarcoma of the Neck
- **Stage**: 6 cm tumor in previously irradiated field (post-Hodgkin's RT 25 years ago)
- **Molecular profile**: Complex karyotype, Radiation-induced secondary malignancy, No specific actionable mutations, History of mediastinal/neck radiation for Hodgkin lymphoma
- **Report file**: experiment_reports\HN3-038_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: The lack of data on perioperative pembrolizumab + preoperative RT + surgery and reirradiation with IMRT or proton therapy (adjuvant) are critical gaps that need to be addressed as they relate to effective treatment strategies for patients with head and neck cancer, which will improve the score by providing more comprehensive information on treatment outcomes. Filling these data gaps will enable researchers to better understand the efficacy of these treatments and inform clinical practice guidelines, ultimately leading to improved patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-038_report.json`.

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
    "cancer_type": "Radiation-Induced Undifferentiated Pleomorphic Sarcoma of the Neck",
    "stage": "6 cm tumor in previously irradiated field (post-Hodgkin's RT 25 years ago)",
    "molecular_profile": [
      "Complex karyotype",
      "Radiation-induced secondary malignancy",
      "No specific actionable mutations",
      "History of mediastinal/neck radiation for Hodgkin lymphoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide surgical excision with free flap reconstruction",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "Multiple retrospective series demonstrate surgery is the primary treatment for radiation-induced sarcoma (RIS). R0/R1 resection correlates with significantly better DSS and OS vs R2 resection. No RCTs exist due to rarity."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Surgery alone median OS ~42 months for RIS. 5-year OS 47% for radiation-associated UPS. R0 resection is the strongest predictor of favorable outcome. Head/neck location challenges wide margin achievement."
        },
        "accessibility": {
          "score": 7,
          "rationale": "Requires head and neck surgical oncology center with microvascular reconstruction capability. Free flap reconstruction (ALT, pectoralis major, fibula) often needed for large defects in fibrotic irradiated tissue."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Surgery in previously irradiated fibrotic tissue is technically challenging. Wound healing impaired. Higher complication rates: flap failure, wound dehiscence, fistula. Must assess for radiation-induced coronary disease before GA. Carotid artery involvement risk."
        },
        "biomarker_match": {
          "score": 6,
          "rationale": "Complex karyotype UPS does not have targeted therapy options. Surgery is histology-agnostic and remains the best local control approach regardless of molecular profile."
        }
      },
      "mechanism_of_action": "En bloc surgical excision of the sarcoma with wide margins (ideally 2+ cm) in the irradiated field. Requires resection of surrounding fibrotic tissue to achieve negative margins. Free tissue transfer reconstruction (anterolateral thigh, pectoralis major, or other flaps) fills the surgical defect and brings vascularized tissue into the radiation-damaged field.",
      "key_evidence": {
        "study_name": "Survival and Margin Status in Head and Neck RIS and De Novo Sarcomas",
        "journal": "Head & Neck",
        "year": 2017,
        "sample_size": 45,
        "os_months": {
          "treatment": 42,
          "control": 6,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
  
... (truncated — read full file from experiment_reports\HN3-038_report.json)
```
