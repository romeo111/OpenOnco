# Re-evaluation Task: TN-017

## Context
- **Case ID**: TN-017
- **Cancer type**: Cervical Node Squamous Cell Carcinoma — Unknown Primary, HPV-Negative (T0N2bM0)
- **Stage**: T0N2bM0 (AJCC 8th Edition Stage III — HPV-negative unknown primary)
- **Molecular profile**: HPV-negative (p16-negative), PD-L1 CPS 5, TP53 mutant, 25 pack-year smoking history
- **Report file**: experiment_reports\TN-017_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-017 cancer research report include the lack of data on Pembrolizumab plus Cisplatin/5-FU (KEYNOTE-048 Regimen) and Neoadjuvant Pembrolizumab Followed by Surgery, which will improve the score by providing more comprehensive insights into effective treatment combinations for patients with specific types of cancer. Filling these gaps will enable researchers to better understand the efficacy and safety of these regimens, ultimately leading to improved patient outcomes and a higher overall score.

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

Read the full report JSON at `experiment_reports\TN-017_report.json`.

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
    "cancer_type": "Cervical Node Squamous Cell Carcinoma — Unknown Primary, HPV-Negative (T0N2bM0)",
    "stage": "T0N2bM0 (AJCC 8th Edition Stage III — HPV-negative unknown primary)",
    "molecular_profile": [
      "HPV-negative (p16-negative)",
      "PD-L1 CPS 5",
      "TP53 mutant",
      "25 pack-year smoking history"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Neck Dissection Followed by Adjuvant Cisplatin-Based Chemoradiation with Comprehensive Mucosal Irradiation",
      "category": "Standard of Care",
      "composite_rating": 7.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "ASCO 2020 guideline and NCCN-recommended approach for HPV-negative SCCUP with N2b disease; supported by multiple retrospective cohort studies and institutional series with consistent outcomes data"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS of 67.7-71% for HPV-negative CUP with neck dissection plus adjuvant chemoradiation; 5-year DSS of 82-86%; significantly superior to radiation alone (HR 4.45 for adjuvant RT alone vs CRT)"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard of care approach available at all major cancer centers; cisplatin and radiation widely available; neck dissection is standard surgical oncology procedure"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Comprehensive mucosal irradiation (bilateral neck, pharynx, larynx) carries significant toxicity: grade 3/4 mucositis 33%, dermatitis 41%, dysphagia 15%; high-dose cisplatin associated with nephrotoxicity and ototoxicity; only 68% complete all chemotherapy cycles; PEG tube often required"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Standard approach for HPV-negative CUP regardless of specific biomarkers; comprehensive mucosal fields specifically indicated for HPV-negative unknown primary where primary site cannot be identified; TP53 mutation may reduce cisplatin sensitivity but CRT remains standard"
        }
      },
      "mechanism_of_action": "Multimodal approach: surgical resection removes gross nodal disease providing pathologic staging and local control; cisplatin acts as a radiosensitizer via DNA cross-linking and inhibition of DNA repair; comprehensive mucosal irradiation (70 Gy to neck, 54-60 Gy elective to bilateral pharyngeal and laryngeal mucosa) targets potential occult primary and residual microscopic disease across all possible mucosal primary sites",
      "key_evidence": {
        "study_name": "Multicenter Retrospective Analysis of HNCUP Outcomes (Muller von der Grun et al.)",
        "journal": "BMC Cancer",
        "year": 2021,
        "sample_size": 59,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 4.45,
   
... (truncated — read full file from experiment_reports\TN-017_report.json)
```
