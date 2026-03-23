# Re-evaluation Task: TN-016

## Context
- **Case ID**: TN-016
- **Cancer type**: Cervical Lymph Node Squamous Cell Carcinoma — Unknown Primary, HPV-Positive
- **Stage**: T0N1M0 (AJCC 8th Edition: Stage I for HPV-positive oropharyngeal primary)
- **Molecular profile**: HPV-positive (p16+), PD-L1 CPS >= 20, Presumed occult oropharyngeal primary (tonsil or tongue base)
- **Report file**: experiment_reports\TN-016_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-016 report are the lack of data on Pembrolizumab Monotherapy for Recurrent/Metastatic disease, which is a crucial treatment option that has shown significant efficacy in various studies, and the absence of information on Cetuximab + RT for Cisplatin-Ineligible Patients, which could provide valuable insights into alternative treatment options for patients who are not eligible for chemotherapy. Filling these gaps with high-quality data will improve the score by providing a more comprehensive understanding of treatment outcomes and options for patients with head and neck cancer.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-016_report.json`.

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
    "cancer_type": "Cervical Lymph Node Squamous Cell Carcinoma — Unknown Primary, HPV-Positive",
    "stage": "T0N1M0 (AJCC 8th Edition: Stage I for HPV-positive oropharyngeal primary)",
    "molecular_profile": [
      "HPV-positive (p16+)",
      "PD-L1 CPS >= 20",
      "Presumed occult oropharyngeal primary (tonsil or tongue base)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Neck Dissection + Ipsilateral RT (60-66 Gy) with Concurrent Cisplatin",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 2A recommendation for unknown primary HPV+ with N1 disease; supported by ASCO guideline (JCO 2020) and ASTRO clinical practice guideline (2024). Standard of care based on multiple retrospective series and guideline consensus."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "HPV-positive unknown primary T0N1 has excellent prognosis: 3-year OS ~94.8%, 5-year OS ~85-90%. Multimodality approach (surgery + adjuvant CRT) provides highest cure rates. Neck dissection provides pathologic staging to guide adjuvant therapy intensity."
        },
        "accessibility": {
          "score": 9,
          "rationale": "All components (neck dissection, IMRT, cisplatin) are FDA-approved, widely available at academic and community cancer centers. Cisplatin is generic and inexpensive. IMRT is standard radiation modality."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Cisplatin-based CRT causes ototoxicity (33%), nephrotoxicity, mucositis, dysphagia, nausea. Ipsilateral RT significantly reduces toxicity vs bilateral fields. Neck dissection risks include cranial nerve XI injury, shoulder dysfunction, lymphedema."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "HPV-positive status confirms favorable biology and expected excellent response to cisplatin-based chemoradiation. CPS>=20 not directly relevant for curative-intent CRT but confirms immunogenic tumor biology."
        }
      },
      "mechanism_of_action": "Neck dissection removes gross nodal disease and provides pathologic staging. Adjuvant radiation with concurrent cisplatin eliminates microscopic residual disease. Cisplatin is a DNA-crosslinking agent that potentiates radiation-induced DNA damage through inhibition of DNA repair. Ipsilateral RT targets the involved neck and putative oropharyngeal mucosal sites while sparing contralateral structures.",
      "key_evidence": {
        "study_name": "ASCO Guideline: Diagnosis and Management of SCC Unknown Primary Head and Neck",
        "journal": "Journal of Clinical Oncology",
        "year": 2020,
        "sample_size": 4350,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
      
... (truncated — read full file from experiment_reports\TN-016_report.json)
```
