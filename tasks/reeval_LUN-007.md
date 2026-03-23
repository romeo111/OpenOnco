# Re-evaluation Task: LUN-007

## Context
- **Case ID**: LUN-007
- **Cancer type**: Non-Small Cell Lung Cancer (NSCLC) with MET Exon 14 Skipping Mutation
- **Stage**: Stage II
- **Molecular profile**: MET exon 14 skipping mutation, MET amplification
- **Report file**: experiment_reports\LUN-007_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The lack of data on Tepotinib, Capmatinib, and Vebreltinib for their respective first-line MET-targeted therapies will hinder the understanding of these treatments' efficacy and safety profiles, ultimately impacting the overall assessment of LUN-007's research. Filling in the gaps for Pembrolizumab + Platinum-Based Chemotherapy with a sample size will provide crucial insight into the immunotherapy combination's effectiveness and potential side effects, allowing for a more comprehensive evaluation of LUN-007's findings.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\LUN-007_report.json`.

Your task: Fill missing evidence fields in `treatments[].key_evidence`.

For each treatment where these are null or missing, search and fill:
- `key_evidence.study_name` — full trial name
- `key_evidence.year` — publication year
- `key_evidence.sample_size` — numeric patient count
- `key_evidence.os_months.treatment` — median OS in treatment arm (months)
- `key_evidence.os_months.control` — median OS in control arm (months)
- `key_evidence.os_months.hazard_ratio` — HR from primary analysis
- `key_evidence.os_months.p_value` — p-value from OS analysis
- `key_evidence.pfs_months.treatment` — median PFS treatment arm
- `key_evidence.pfs_months.control` — median PFS control arm

Rules:
- Only fill with data you can verify from published trials
- Set to null (not omit) if genuinely unavailable after searching
- Do NOT fabricate or estimate numbers

Return the corrected `treatments` array only.

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
    "cancer_type": "Non-Small Cell Lung Cancer (NSCLC) with MET Exon 14 Skipping Mutation",
    "stage": "Stage II",
    "molecular_profile": [
      "MET exon 14 skipping mutation",
      "MET amplification"
    ],
    "patient_info": {
      "case_id": "LUN-007",
      "age": 45,
      "sex": "Male",
      "ecog_status": 0,
      "risk_factors": [
        "hypertension"
      ],
      "comorbidities": [
        "hyperlipidemia"
      ]
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Surgical Resection (Lobectomy) + Adjuvant Cisplatin-Based Chemotherapy",
      "category": "Standard of Care",
      "composite_rating": 8.7,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Multiple phase 3 RCTs and meta-analyses (LACE meta-analysis) establish surgical resection with adjuvant platinum-based chemotherapy as standard of care for stage II NSCLC with 5.4% absolute 5-year OS improvement"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Stage II 5-year survival 46-60% with surgery + adjuvant chemo; curative intent approach with absolute survival benefit of 5.4% at 5 years from adjuvant chemotherapy; potentially curative for this 45-year-old ECOG 0 patient"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available standard of care; lobectomy and cisplatin-based doublet widely accessible at all cancer centers"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgical morbidity manageable in ECOG 0 patient; cisplatin-based chemotherapy has well-characterized toxicity profile including nephrotoxicity, nausea, and myelosuppression; hypertension and hyperlipidemia are manageable comorbidities"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Surgery is biomarker-agnostic for resectable NSCLC; standard approach for stage II regardless of driver mutation; however adjuvant chemo benefit may be lower in MET-driven tumors due to relative chemoresistance"
        }
      },
      "mechanism_of_action": "Surgical lobectomy removes the primary tumor with curative intent. Adjuvant cisplatin-based doublet chemotherapy (typically cisplatin/pemetrexed for adenocarcinoma) eliminates micrometastatic disease to reduce recurrence risk.",
      "key_evidence": {
        "study_name": "LACE Meta-Analysis (Lung Adjuvant Cisplatin Evaluation)",
        "journal": "Journal of Clinical Oncology",
        "year": 2008,
        "sample_size": 4584,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.89,
          "p_value": 0.005
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [
... (truncated — read full file from experiment_reports\LUN-007_report.json)
```
