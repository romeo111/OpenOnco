# Re-evaluation Task: HN-006

## Context
- **Case ID**: HN-006
- **Cancer type**: Oral cavity squamous cell carcinoma (tongue)
- **Stage**: Stage II (T2N0M0)
- **Molecular profile**: PD-L1 CPS <1, NOTCH1 mutated
- **Report file**: experiment_reports\HN-006_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in HN-006's treatment protocol are the lack of Adjuvant Cisplatin-Based Chemoradiation (High-Risk) and Sentinel Lymph Node Biopsy, which are crucial for accurately staging and treating high-risk patients with head and neck cancer, thereby improving patient outcomes. Addressing these gaps will enhance the score by providing more comprehensive treatment options for high-risk patients, ultimately leading to better survival rates and quality of life.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN-006_report.json`.

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
    "cancer_type": "Oral cavity squamous cell carcinoma (tongue)",
    "stage": "Stage II (T2N0M0)",
    "molecular_profile": [
      "PD-L1 CPS <1",
      "NOTCH1 mutated"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Partial Glossectomy with Elective Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 9.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 RCT evidence from landmark trial (596 patients, T1-T2N0 OCSCC) demonstrating superior 3-year OS with elective neck dissection (80.0% vs 67.5%). NCCN Category 1 recommendation for surgery-first approach in early-stage oral cavity SCC"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "3-year OS 80.0% with upfront END. 5-year OS for low-risk pT1-T2N0 managed by partial glossectomy and neck dissection is excellent. Local control rate of 80-90% for T1-T2 cancers with single-modality surgery. For T2 with DOI >=4mm, END improves OS with HR 0.37"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available surgical procedure at all head and neck cancer centers. Standard of care per NCCN and ESMO guidelines worldwide"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Partial glossectomy is well-tolerated with short-term speech and swallowing deficits that recover to near-baseline by 6-12 months. Neck dissection adds shoulder dysfunction risk. Surgical mortality is low (<1%). Diabetes may slightly increase wound healing risk"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirements. Surgery is the universal primary treatment for resectable oral cavity SCC regardless of PD-L1 or mutational status"
        }
      },
      "mechanism_of_action": "Surgical excision of the primary tongue tumor with adequate margins (>=5mm) combined with ipsilateral or bilateral selective neck dissection (levels I-III/IV) to remove the primary tumor and address occult nodal metastases. For T2 tumors, depth of invasion >=4mm strongly supports elective neck dissection given 45.7% 5-year risk of regional disease.",
      "key_evidence": {
        "study_name": "Elective versus Therapeutic Neck Dissection in Node-Negative Oral Cancer (D'Cruz et al.)",
        "journal": "New England Journal of Medicine",
        "year": 2015,
        "sample_size": 596,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.63,
          "p_value": 0.01
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
        "temporary speech impairment (resolves by 12 mon
... (truncated — read full file from experiment_reports\HN-006_report.json)
```
