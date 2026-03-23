# Re-evaluation Task: TN-018

## Context
- **Case ID**: TN-018
- **Cancer type**: Medullary thyroid carcinoma (MTC) — sporadic
- **Stage**: Stage III (T3N1aM0)
- **Molecular profile**: RET M918T somatic mutation, Sporadic (non-hereditary, rule out MEN2 pending germline testing)
- **Report file**: experiment_reports\TN-018_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: The lack of data on Selpercatinib Neoadjuvant Therapy and Total Thyroidectomy + Central/Lateral Neck Dissect are critical gaps that need to be addressed, as they relate to key treatment options for thyroid cancer patients, which will improve the score by providing more comprehensive information on treatment efficacy. Additionally, including sample sizes for External Beam Radiation Therapy (EBRT) — Adjuvant/ will provide a crucial metric for evaluating the effectiveness of this treatment approach, further enhancing the report's credibility and usefulness.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  11/25  |  44.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (44.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-018_report.json`.

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
    "cancer_type": "Medullary thyroid carcinoma (MTC) — sporadic",
    "stage": "Stage III (T3N1aM0)",
    "molecular_profile": [
      "RET M918T somatic mutation",
      "Sporadic (non-hereditary, rule out MEN2 pending germline testing)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Selpercatinib (Retevmo) — Selective RET Inhibitor",
      "category": "Approved Targeted Therapy",
      "composite_rating": 9.4,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 RCT LIBRETTO-531 (NEJM 2023, n=291) demonstrated clear superiority over cabozantinib/vandetanib. Phase 1/2 LIBRETTO-001 (n=531) provided long-term durability data at 42+ months follow-up. FDA traditional approval September 2024"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "LIBRETTO-531: median PFS not reached vs 16.8 months for MKIs (HR 0.28, p<0.001). ORR 69.4% vs 38.8%. LIBRETTO-001: 82.5% ORR in treatment-naive MTC, median PFS not reached at 42.4 months. 18-month OS rate 95.5% vs 92.8%. Dramatic improvement over prior standard MKIs"
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA traditional approval September 2024 for adults and pediatric patients >=2 years with advanced/metastatic RET-mutant MTC. Widely available at oncology centers. Covered by major insurance plans"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Favorable safety vs MKIs. Grade >=3 AEs: 52.8% vs 76.3% control. Dose reduction 38.9% vs 77.3%. Discontinuation 4.7% vs 26.8%. Main toxicities: hypertension (21% grade >=3), diarrhea, dry mouth, ALT/AST elevation. Better tolerated than cabozantinib/vandetanib"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Patient has RET M918T somatic mutation — the most common RET mutation in MTC (62.7% of LIBRETTO-531 patients). Selpercatinib directly targets the RET kinase. Perfect biomarker match"
        }
      },
      "mechanism_of_action": "Highly selective, ATP-competitive small-molecule inhibitor of RET receptor tyrosine kinase. Potently inhibits wild-type RET and multiple mutant forms including M918T, V804L/M gatekeeper mutations, and CCDC6-RET fusions. Blocks constitutive RET signaling driving tumor proliferation and survival through MAPK, PI3K/AKT, and JAK/STAT pathways.",
      "key_evidence": {
        "study_name": "LIBRETTO-531 Phase III RCT",
        "journal": "New England Journal of Medicine",
        "year": 2023,
        "sample_size": 291,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.37,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 0,
          "control": 16.8
        },
        "orr_percent": {
          "treatment": 69.4,
          "control": 38.8
        }
      },
      "biom
... (truncated — read full file from experiment_reports\TN-018_report.json)
```
