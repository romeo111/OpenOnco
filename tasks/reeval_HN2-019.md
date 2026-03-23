# Re-evaluation Task: HN2-019

## Context
- **Case ID**: HN2-019
- **Cancer type**: Osteosarcoma of the mandible (gnathic osteosarcoma)
- **Stage**: Stage IIB (high-grade, localized)
- **Molecular profile**: TP53 mutated, No MDM2 amplification, Radiation-induced secondary malignancy (post-retinoblastoma treatment), High-grade conventional osteosarcoma
- **Report file**: experiment_reports\HN2-019_report.json
- **Current score**: 81/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-019 are the lack of data on Neoadjuvant + Adjuvant MAP Chemotherapy (Methotrexate) and Postoperative Radiation Therapy (60-66 Gy, Proton), which will improve the score by providing more comprehensive information on treatment regimens for patients with head and neck cancer. Filling these gaps will enable a more accurate assessment of the effectiveness of these treatments, allowing researchers to better understand patient outcomes and inform future clinical trials.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |   9/25  |  36.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (36.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-019_report.json`.

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
    "cancer_type": "Osteosarcoma of the mandible (gnathic osteosarcoma)",
    "stage": "Stage IIB (high-grade, localized)",
    "molecular_profile": [
      "TP53 mutated",
      "No MDM2 amplification",
      "Radiation-induced secondary malignancy (post-retinoblastoma treatment)",
      "High-grade conventional osteosarcoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Segmental Mandibulectomy with Free Fibula Flap Reconstruction",
      "category": "Standard of Care — Surgery",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "R0 resection is the single most important prognostic factor for gnathic osteosarcoma per consensus recommendations (Dietz et al., Cancer 2026). Negative margins (>=3mm on permanent histology) are the cornerstone of curative treatment. Decades of institutional series consistently demonstrate that complete surgical resection is the only treatment associated with long-term cure."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year disease-specific survival 66.8% with R0 resection per multi-institutional data. Jaw osteosarcoma has better prognosis than extremity OS when completely resected (lower metastatic rate ~2% at presentation vs 10-15% for extremity). Patients achieving negative margins have 80% OS vs 31% without, per gnathic OS consensus data."
        },
        "accessibility": {
          "score": 8,
          "rationale": "Available at major head-and-neck surgical oncology centers. Requires expertise in microvascular free flap reconstruction. Free fibula flap is the gold standard for mandibular reconstruction with 92% flap survival rate. Should be performed at tertiary sarcoma center."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Major surgery with significant morbidity. Risks include flap failure (8%), donor site morbidity, altered speech, mastication difficulty, facial nerve compromise, and prolonged recovery. However, well-tolerated in 45-year-old with adequate performance status. Long-term functional rehabilitation achievable."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Surgery is universally applicable regardless of molecular profile. TP53 status and radiation-induced etiology do not affect surgical candidacy. The key determinant is anatomic resectability, which is favorable for mandibular lesions."
        }
      },
      "mechanism_of_action": "Complete en-bloc surgical resection of the tumor-bearing mandibular segment with adequate margins (>=3mm), followed by immediate reconstruction with vascularized free fibula flap to restore mandibular continuity, facial contour, and eventual dental rehabilitation with osseointegrated implants.",
      "key_evidence": {
        "study_name": "Consensus Recommendations in Managemen
... (truncated — read full file from experiment_reports\HN2-019_report.json)
```
