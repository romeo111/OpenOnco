# Re-evaluation Task: HN3-036

## Context
- **Case ID**: HN3-036
- **Cancer type**: Incidental HPV-Positive Tonsillar Squamous Cell Carcinoma
- **Stage**: T1N0M0 (AJCC 8th Edition Stage I, p16+)
- **Molecular profile**: HPV-positive (p16+), PD-L1 CPS 15, Positive margins on tonsillectomy specimen
- **Report file**: experiment_reports\HN3-036_report.json
- **Current score**: 69/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-036 cancer research report are the lack of data on PET/CT staging followed by risk-adapted management, which is a crucial step in determining the optimal treatment plan for patients with oropharyngeal cancer, and the absence of information on proton beam radiation therapy, which has shown promise as a de-escalated adjuvant treatment option. Addressing these gaps will improve the score by providing more comprehensive data on treatment outcomes and options, ultimately enhancing the accuracy and reliability of the report's findings.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-036_report.json`.

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
    "cancer_type": "Incidental HPV-Positive Tonsillar Squamous Cell Carcinoma",
    "stage": "T1N0M0 (AJCC 8th Edition Stage I, p16+)",
    "molecular_profile": [
      "HPV-positive (p16+)",
      "PD-L1 CPS 15",
      "Positive margins on tonsillectomy specimen"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Re-excision (TORS lateral oropharyngectomy) to negative margins + observation",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "ECOG-ACRIN 3311 Arm A validated observation after complete resection with negative margins in pT1-2N0-1 HPV+ OPC; 2-year PFS >95% in low-risk group. Multiple retrospective series support TORS for T1 tonsil SCC."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "HPV+ T1N0 with negative margins has >95% 3-year OS. Avoids radiation toxicity entirely in a disease with excellent prognosis. Re-excision converts a positive-margin case to a low-risk category."
        },
        "accessibility": {
          "score": 8,
          "rationale": "TORS is widely available at academic centers; lateral oropharyngectomy is well-established. Not all community hospitals have robotic surgery capability."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Single surgical procedure; 7% oropharyngeal hemorrhage rate for unilateral TORS. Avoids all radiation-related morbidity (xerostomia, dysphagia, fibrosis)."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "HPV-positive status confers excellent prognosis after complete surgical excision. p16+ T1N0 with negative margins is the most favorable head and neck cancer scenario."
        }
      },
      "mechanism_of_action": "Surgical re-excision of the tonsillar fossa using transoral robotic surgery to achieve negative margins, converting the patient to ECOG 3311 low-risk category (pT1N0, margins ≥3mm) eligible for observation alone without adjuvant therapy.",
      "key_evidence": {
        "study_name": "ECOG-ACRIN 3311 (Low-risk arm A)",
        "journal": "Journal of Clinical Oncology",
        "year": 2022,
        "sample_size": 40,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 36,
          "control": 0
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "HPV-positive (p16+)"
      ],
      "notable_side_effects": [
        "Post-tonsillectomy hemorrhage (7%)",
        "Transient dysphagia",
        "Oropharyngeal pain",
        "Velopharyngeal insufficiency (rare)"
      ],
      "availability": "FDA Approved (TORS for T1-T2 oropharyngeal tumors)",
   
... (truncated — read full file from experiment_reports\HN3-036_report.json)
```
