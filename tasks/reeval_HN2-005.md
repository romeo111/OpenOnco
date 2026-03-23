# Re-evaluation Task: HN2-005

## Context
- **Case ID**: HN2-005
- **Cancer type**: NUT Carcinoma (NUT Midline Carcinoma, Sinonasal)
- **Stage**: T4aN2M0 (Locally Advanced)
- **Molecular profile**: BRD4-NUT fusion positive (pathognomonic), Ki-67 90%, NUTM1 rearrangement confirmed
- **Report file**: experiment_reports\HN2-005_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-005 are the lack of data on Upfront Surgical Resection with Negative Margins and Concurrent Chemoradiation (without surgery), as addressing these areas would provide more comprehensive insights into effective treatment strategies for patients with specific types of cancer. Filling these gaps will improve the score by providing a more nuanced understanding of treatment outcomes, allowing researchers to better identify optimal treatment regimens and ultimately improve patient care.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-005_report.json`.

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
    "cancer_type": "NUT Carcinoma (NUT Midline Carcinoma, Sinonasal)",
    "stage": "T4aN2M0 (Locally Advanced)",
    "molecular_profile": [
      "BRD4-NUT fusion positive (pathognomonic)",
      "Ki-67 90%",
      "NUTM1 rearrangement confirmed"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Upfront Surgical Resection with Negative Margins + Adjuvant Chemoradiation",
      "category": "Standard of Care",
      "composite_rating": 6.8,
      "rating_breakdown": {
        "evidence_level": {
          "score": 6,
          "rationale": "Retrospective series of 40 HN NUT carcinoma patients (Chau et al., Cancer 2016) — no RCTs exist for this ultra-rare cancer. R0 resection achieved 80% 2-year OS vs 7% without surgery (p=0.003)."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "R0 resection yields 80% 2-year OS, median OS 9.7 months overall but significantly longer with complete resection. Surgery for tumors <6 cm: HR=0.13 for OS (p=0.005). Best documented survival strategy."
        },
        "accessibility": {
          "score": 7,
          "rationale": "Available at major head and neck surgical centers. T4a sinonasal tumors require experienced skull-base surgical teams. Feasibility depends on resectability assessment — T4a may be borderline resectable."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Major skull-base surgery carries significant morbidity: cranial nerve deficits, CSF leak, orbital complications, prolonged recovery. Adjuvant cisplatin-based CRT adds hematologic and renal toxicity."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Surgery is biomarker-agnostic. All NUT carcinoma patients with resectable disease benefit. BRD4-NUT fusion does not affect surgical indication."
        }
      },
      "mechanism_of_action": "Complete surgical extirpation removes the primary tumor burden. Adjuvant concurrent chemoradiation (typically cisplatin 100 mg/m2 q3w + 60-70 Gy IMRT) targets microscopic residual disease and regional nodal metastases. The goal is R0 resection with negative margins, which is the strongest predictor of long-term survival in NUT carcinoma of the head and neck.",
      "key_evidence": {
        "study_name": "Intensive Treatment and Survival Outcomes in NUT Midline Carcinoma of the Head and Neck",
        "journal": "Cancer",
        "year": 2016,
        "sample_size": 40,
        "os_months": {
          "treatment": 24,
          "control": 6.6,
          "hazard_ratio": 0.35,
          "p_value": 0.003
        },
        "pfs_months": {
          "treatment": 14,
          "control": 3.5
        },
        "orr_percent": {
          "treatment": 80,
          "control": 7
        }
      },
      "biomarker_requirements": [
        "NUT IHC positive",
        "NUTM1 rearrangement confirmed by FISH or NGS"
      ],
      "no
... (truncated — read full file from experiment_reports\HN2-005_report.json)
```
