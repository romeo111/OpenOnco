# Re-evaluation Task: TN-019

## Context
- **Case ID**: TN-019
- **Cancer type**: RAI-Refractory Follicular Thyroid Carcinoma
- **Stage**: T3N0M1 (Stage IVB) with bone metastases
- **Molecular profile**: NRAS Q61R activating mutation, TERT promoter mutation (poor prognosis marker), Radioactive iodine refractory
- **Report file**: experiment_reports\TN-019_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-019 cancer research report are the lack of data on Lenvatinib (First-line TKI) and Conventional External Beam Radiation Therapy (EBRT) for bone metastases, which will be addressed by filling these intent missing sections to provide more comprehensive information on treatment options. By adding this data, the score can improve as it will allow researchers to better understand the efficacy of Lenvatinib in first-line treatment and the effectiveness of EBRT in managing bone metastases, providing valuable insights for future cancer research.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-019_report.json`.

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
    "cancer_type": "RAI-Refractory Follicular Thyroid Carcinoma",
    "stage": "T3N0M1 (Stage IVB) with bone metastases",
    "molecular_profile": [
      "NRAS Q61R activating mutation",
      "TERT promoter mutation (poor prognosis marker)",
      "Radioactive iodine refractory"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Lenvatinib (First-line TKI)",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 SELECT trial (N=392) published in NEJM; definitive RCT establishing lenvatinib as first-line standard for RAI-refractory DTC"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Median PFS 18.3 vs 3.6 months (HR 0.21, p<0.001); ORR 64.8% vs 1.5%; median OS 43.2 months in treatment arm; among responders OS 52.2 months"
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA approved (2015) for RAI-refractory DTC; globally available; NCCN Category 1 recommendation"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant toxicity requiring dose reductions in ~67% of patients; common AEs include hypertension (68%), diarrhea (59%), fatigue (59%), decreased appetite (50%), weight loss (46%), proteinuria; manageable with dose modifications"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirement; effective across all molecular subtypes of RAI-refractory DTC including NRAS-mutated and TERT-mutated tumors"
        }
      },
      "mechanism_of_action": "Multi-kinase inhibitor targeting VEGFR1-3, FGFR1-4, PDGFRalpha, RET, and KIT. Inhibits tumor angiogenesis and directly suppresses tumor cell proliferation through blockade of multiple oncogenic signaling pathways.",
      "key_evidence": {
        "study_name": "SELECT (Study of (E7080) LEnvatinib in Differentiated Cancer of the Thyroid)",
        "journal": "New England Journal of Medicine",
        "year": 2015,
        "sample_size": 392,
        "os_months": {
          "treatment": 43.2,
          "control": 34.0,
          "hazard_ratio": 0.73,
          "p_value": 0.1
        },
        "pfs_months": {
          "treatment": 18.3,
          "control": 3.6
        },
        "orr_percent": {
          "treatment": 64.8,
          "control": 1.5
        }
      },
      "biomarker_requirements": [
        "None — approved for all RAI-refractory DTC regardless of mutation status"
      ],
      "notable_side_effects": [
        "Hypertension (68%)",
        "Diarrhea (59%)",
        "Fatigue/asthenia (59%)",
        "Decreased appetite (50%)",
        "Weight loss (46%)",
        "Proteinuria (31%)",
        "Palmar-plantar erythrodysesthesia (32%)",
        "Nausea (41%)",
        "Arterial thromboembolic events (5.4%)"
      ],
 
... (truncated — read full file from experiment_reports\TN-019_report.json)
```
