# Re-evaluation Task: HN2-017

## Context
- **Case ID**: HN2-017
- **Cancer type**: Retromolar trigone squamous cell carcinoma (oral cavity/oropharynx junction)
- **Stage**: Stage IVA (T4aN1M0) — pterygoid plate invasion, trismus (MIO 30mm)
- **Molecular profile**: PD-L1 CPS 15, TP53 mutated, CDKN2A mutated, HPV-negative (smoking/alcohol-associated)
- **Report file**: experiment_reports\HN2-017_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in HN2-017 include the lack of data on Composite Resection with Mandibulectomy + Neck Dis and Pembrolizumab + Platinum + 5-FU (EXTREME-like regimen), which are crucial for understanding treatment outcomes in head and neck cancer patients. Filling these gaps will improve the score by providing more comprehensive information on the efficacy and safety of these treatments, allowing for more accurate comparisons with other studies and potentially leading to improved patient care.

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

Read the full report JSON at `experiment_reports\HN2-017_report.json`.

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
    "cancer_type": "Retromolar trigone squamous cell carcinoma (oral cavity/oropharynx junction)",
    "stage": "Stage IVA (T4aN1M0) — pterygoid plate invasion, trismus (MIO 30mm)",
    "molecular_profile": [
      "PD-L1 CPS 15",
      "TP53 mutated",
      "CDKN2A mutated",
      "HPV-negative (smoking/alcohol-associated)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Composite Resection with Mandibulectomy + Neck Dissection + Adjuvant Cisplatin-Based Chemoradiation",
      "category": "Standard of Care",
      "composite_rating": 8.3,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "NCCN Category 1 recommendation for resectable T4a oral cavity SCC. Based on EORTC 22931 and RTOG 9501 Phase 3 RCTs demonstrating superiority of adjuvant CRT over RT alone in high-risk resected HNSCC. Standard of care for over two decades with Level 1 evidence"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "For T4aN1 retromolar trigone SCC, 5-year OS approximately 38-55% with combined modality therapy per systematic review (mean 38.9% across studies; 55.3% in selected surgical series). EORTC 22931 showed 3-year DFS 59% with adjuvant CRT vs 41% with RT alone (p=0.009). Substantial benefit but RMT location carries worse prognosis than other oral cavity subsites"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all head and neck cancer centers. Cisplatin 100mg/m2 q3w x3 or 40mg/m2 weekly x6-7 with 60-66 Gy RT are standard regimens. Well-established surgical and radiation oncology protocols"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Major surgery requiring composite mandibulectomy with potential infratemporal fossa dissection. Oro-cutaneous fistula rate 10.6%, wound infection 8.1%, osteoradionecrosis 11.6% in irradiated patients. Cisplatin causes nephrotoxicity, ototoxicity, nausea. Combined morbidity is significant in this 45yo heavy smoker/drinker"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirements — universally applicable. TP53/CDKN2A mutations are the most common in HPV-negative HNSCC and do not exclude standard therapy. These mutations are associated with smoking-related carcinogenesis"
        }
      },
      "mechanism_of_action": "Composite resection removes the primary tumor with en-bloc mandibulectomy, pterygoid plate resection, and ipsilateral neck dissection for regional nodes. Adjuvant cisplatin radiosensitizes residual microscopic disease while 60-66 Gy radiation eradicates subclinical deposits. Cisplatin crosslinks DNA, preventing replication in rapidly dividing tumor cells.",
      "key_evidence": {
        "study_name": "EORTC 22931 Phase 3 RCT",
        "journal": "New England Journal of Medicine",
        "year": 2
... (truncated — read full file from experiment_reports\HN2-017_report.json)
```
