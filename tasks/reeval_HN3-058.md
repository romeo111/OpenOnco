# Re-evaluation Task: HN3-058

## Context
- **Case ID**: HN3-058
- **Cancer type**: Parotid MALT Lymphoma (Extranodal Marginal Zone Lymphoma of Mucosa-Associated Lymphoid Tissue)
- **Stage**: Stage IE (Ann Arbor)
- **Molecular profile**: t(11;18)(q21;q21) positive (API2-MALT1 fusion), CD20 positive, Associated with Sjogren syndrome, Antibiotic-resistant phenotype (t(11;18)+), Radiation-sensitive
- **Report file**: experiment_reports\HN3-058_report.json
- **Current score**: 71/100
- **Gap analysis (local GPU)**: The lack of data on Involved-Field Radiation Therapy (24-30 Gy) and Zanubrutinib (BTK Inhibitor) treatment regimens are critical gaps, as they represent key areas of investigation for novel radiation therapy approaches and BTK inhibitor therapies that have shown promise in treating certain types of cancer. Filling these data gaps will improve the score by providing a more comprehensive understanding of the efficacy and safety profiles of these treatments, allowing researchers to better inform treatment decisions and potentially develop new therapeutic strategies.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-058_report.json`.

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
    "cancer_type": "Parotid MALT Lymphoma (Extranodal Marginal Zone Lymphoma of Mucosa-Associated Lymphoid Tissue)",
    "stage": "Stage IE (Ann Arbor)",
    "molecular_profile": [
      "t(11;18)(q21;q21) positive (API2-MALT1 fusion)",
      "CD20 positive",
      "Associated with Sjogren syndrome",
      "Antibiotic-resistant phenotype (t(11;18)+)",
      "Radiation-sensitive"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Involved-Field Radiation Therapy (24-30 Gy)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple retrospective series with long-term follow-up; NCCN Category 2A for Stage IE MALT lymphoma; 5-year LC rate 100% in most series; standard of care for localized EMZL"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year OS 96.6%, PFS 82.2%, local control 100% in largest series; long-term possible cure for Stage IE disease; t(11;18)+ tumors are radiation-sensitive despite antibiotic resistance"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard radiation therapy available at all cancer centers; well-established dose protocols (24-30 Gy in 12-15 fractions); outpatient treatment"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Low-dose radiation (24-30 Gy) with limited field; main toxicity is xerostomia from parotid irradiation (already affected by Sjogren's); may worsen existing dry mouth; skin reaction"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "t(11;18)+ MALT lymphomas are radiation-sensitive despite being antibiotic-resistant; complete remission achieved in all t(11;18)+ cases after RT in published series; ideal for this molecular profile"
        }
      },
      "mechanism_of_action": "Low-dose involved-field radiation therapy (24-30 Gy) targets the parotid gland containing MALT lymphoma. Radiation induces DNA damage in lymphoma cells, leading to apoptosis. MALT lymphoma is highly radiosensitive, with near-100% local control rates at modest doses. The entire parotid gland including the deep lobe should be included in the CTV.",
      "key_evidence": {
        "study_name": "Long-term outcome in localized EMZL treated with radiotherapy",
        "journal": "Cancer (Wiley)",
        "year": 2010,
        "sample_size": 103,
        "os_months": {
          "treatment": 60,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 49,
          "control": 0
        },
        "orr_percent": {
          "treatment": 100,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "CD20+ (confirms B-cell MALT lymphoma)"
      ],
      "notable_side_effects": [
        "Xer
... (truncated — read full file from experiment_reports\HN3-058_report.json)
```
