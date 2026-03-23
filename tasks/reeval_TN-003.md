# Re-evaluation Task: TN-003

## Context
- **Case ID**: TN-003
- **Cancer type**: Oral tongue squamous cell carcinoma (OTSCC) with perineural invasion
- **Stage**: T2N0M0 (AJCC 8th Edition), DOI >5mm, PNI+
- **Molecular profile**: PD-L1 CPS 5-10, EGFR overexpressed, NOTCH1 mutated, Betel nut (areca nut) exposure history
- **Report file**: experiment_reports\TN-003_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-003_report.json`.

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
    "cancer_type": "Oral tongue squamous cell carcinoma (OTSCC) with perineural invasion",
    "stage": "T2N0M0 (AJCC 8th Edition), DOI >5mm, PNI+",
    "molecular_profile": [
      "PD-L1 CPS 5-10",
      "EGFR overexpressed",
      "NOTCH1 mutated",
      "Betel nut (areca nut) exposure history"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Surgery (Glossectomy + Elective Neck Dissection) + Adjuvant Radiation Therapy (60-66 Gy IMRT)",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "NCCN Category 1 recommendation. Multiple Phase 3 RCTs and large multi-institutional studies (n=557, PMC10575471) confirm adjuvant RT mitigates PNI impact. AJCC 8th edition staging mandates DOI >5mm as upstaging factor warranting elective neck dissection."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS ~75-83% for T2N0 oral tongue SCC with adequate surgery + adjuvant RT. 2-year DFS improves from 58.0% (no RT) to 81.9% (with RT) in PNI+ early-stage OCSCC. 2-year LRC 88.2% with RT vs 68.9% without. HR for DFS = 0.437 (p=0.034) favoring RT in PNI+ patients."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard of care available at all major cancer centers worldwide. Surgical expertise and IMRT widely accessible. No biomarker requirements or drug costs beyond standard radiation oncology services."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgery carries risks of speech/swallowing impairment. Adjuvant RT causes mucositis, xerostomia, dysphagia, dental complications. Chronic periodontitis requires dental management pre-RT to prevent osteoradionecrosis. Manageable but impactful quality-of-life effects."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — no biomarker requirements. PNI+ status is itself the indication for adjuvant RT per NCCN. DOI >5mm confirms need for elective neck dissection."
        }
      },
      "mechanism_of_action": "Partial glossectomy with adequate margins (>5mm) removes primary tumor. Elective neck dissection (levels I-III/IV) addresses occult nodal metastasis risk (18.8% for DOI >=5mm). Adjuvant IMRT (60-66 Gy in 30-33 fractions) targets the tumor bed and draining lymphatics to eradicate microscopic residual disease, with PNI-positive tumors requiring radiation to cover perineural pathways.",
      "key_evidence": {
        "study_name": "Multi-institutional analysis of adjuvant RT in PNI+ early-stage OCSCC",
        "journal": "Oral Oncology",
        "year": 2023,
        "sample_size": 557,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.437,
          "p_value": 0.034
        },
        "pfs_mo
... (truncated — read full file from experiment_reports\TN-003_report.json)
```
