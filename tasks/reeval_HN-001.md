# Re-evaluation Task: HN-001

## Context
- **Case ID**: HN-001
- **Cancer type**: HPV-positive oropharyngeal squamous cell carcinoma
- **Stage**: Stage III (T2N1M0)
- **Molecular profile**: HPV p16+, PD-L1 CPS >=20
- **Report file**: experiment_reports\HN-001_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in HN-001's research report include the lack of data on Proton Beam Therapy with Concurrent Cisplatin and Adjuvant Nivolumab Post-Surgery (NIVOPOSTOP), which are crucial for understanding the efficacy of these treatments in head and neck cancer. Filling these gaps will improve the score by providing more comprehensive insights into the effectiveness of innovative therapies, such as proton beam therapy and immunotherapy combinations, which have shown promise in treating head and neck cancer.

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

Read the full report JSON at `experiment_reports\HN-001_report.json`.

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
    "cancer_type": "HPV-positive oropharyngeal squamous cell carcinoma",
    "stage": "Stage III (T2N1M0)",
    "molecular_profile": [
      "HPV p16+",
      "PD-L1 CPS >=20"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Cisplatin + Intensity-Modulated Radiation Therapy (70 Gy)",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Multiple Phase 3 RCTs (RTOG 0129, De-ESCALaTE HPV, NRG-HN005) with thousands of patients confirming cisplatin+RT as gold standard for HPV+ oropharyngeal cancer"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "NRG-HN005 showed 2-year PFS 98.1% and 2-year OS 99%. RTOG 0129 showed 3-year OS 82.4% for HPV+ patients with HR 0.42 vs HPV-negative. 5-year OS rates reach 85-93%"
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA approved, universally available at all oncology centers worldwide. Standard of care per NCCN/ESMO guidelines"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant acute toxicity: grade 3+ mucositis in 40-60%, nephrotoxicity, ototoxicity, dysphagia, weight loss. Long-term effects include xerostomia and dysphagia affecting QoL for decades in young patients"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker required — universal applicability regardless of molecular profile. HPV+ status confers better prognosis but treatment is the same"
        }
      },
      "mechanism_of_action": "Cisplatin forms DNA crosslinks causing cell death and radiosensitization. IMRT delivers conformal radiation to tumor while sparing surrounding tissue. Combined modality attacks tumor through complementary DNA damage mechanisms.",
      "key_evidence": {
        "study_name": "NRG-HN005",
        "journal": "ASTRO Annual Meeting / Lancet Oncology",
        "year": 2024,
        "sample_size": 382,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
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
      "biomarker_requirements": [],
      "notable_side_effects": [
        "grade 3+ mucositis (40-60%)",
        "nephrotoxicity",
        "ototoxicity (hearing loss)",
        "severe dysphagia",
        "xerostomia",
        "weight loss",
        "nausea/vomiting"
      ],
      "availability": "FDA Approved — universally available",
      "source_urls": [
        "https://ascopost.com/issues/april-25-2025/study-finds-standard-chemoradiation-therapy-superior-to-deintensification-approaches-for-hpv-related-oropharyngeal-cancer/",
        "https://www.practi
... (truncated — read full file from experiment_reports\HN-001_report.json)
```
