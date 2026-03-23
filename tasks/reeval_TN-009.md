# Re-evaluation Task: TN-009

## Context
- **Case ID**: TN-009
- **Cancer type**: Oral tongue squamous cell carcinoma in Fanconi anemia / Li-Fraumeni syndrome (dual genetic predisposition)
- **Stage**: Stage II (T2N0M0)
- **Molecular profile**: Fanconi anemia (FA/BRCA pathway defect — DNA crosslink repair deficiency), Li-Fraumeni syndrome (germline TP53 variant), Bone marrow hypoplasia, Non-smoker, 45-year-old male, EGFR status unknown — recommend testing, Bcl-2 expression unknown — recommend testing, PD-L1 CPS unknown — recommend testing
- **Report file**: experiment_reports\TN-009_report.json
- **Current score**: 81/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  10/25  |  40.0% |
| rating_calibration                  |  12/15  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (40.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-009_report.json`.

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
    "cancer_type": "Oral tongue squamous cell carcinoma in Fanconi anemia / Li-Fraumeni syndrome (dual genetic predisposition)",
    "stage": "Stage II (T2N0M0)",
    "molecular_profile": [
      "Fanconi anemia (FA/BRCA pathway defect — DNA crosslink repair deficiency)",
      "Li-Fraumeni syndrome (germline TP53 variant)",
      "Bone marrow hypoplasia",
      "Non-smoker, 45-year-old male",
      "EGFR status unknown — recommend testing",
      "Bcl-2 expression unknown — recommend testing",
      "PD-L1 CPS unknown — recommend testing"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision (Partial Glossectomy) with Elective Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 8.8,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple large retrospective series and prospective cohort studies confirm partial glossectomy + END as standard of care for T2N0 oral tongue SCC. NCCN guidelines Category 1 recommendation. Specific FA-HNSCC guidelines from FARF and Clinical Cancer Research (2021) identify surgery as primary modality for FA patients given contraindications to chemoradiation."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year disease-specific survival 85% for pN0 T2 oral tongue SCC after surgery. 10-year RFS approximately 73% and OS 43-44%. For FA patients specifically, surgical resection offers the best chance of cure; IFAR cohort showed 5-year survival ~39% overall but most presented at advanced stage (43% Stage IV). Early-stage FA-HNSCC with complete resection has better expected outcomes."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard surgical procedure available at all major head and neck surgery centers worldwide. No specialized equipment beyond standard OR instrumentation required."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Surgery is well-tolerated in FA patients unlike chemo/radiation. Perioperative risks include bleeding (monitor given bone marrow hypoplasia — ensure adequate platelet counts pre-op), wound healing concerns. Speech and swallowing deficits expected but manageable with rehabilitation. No DNA-damaging systemic toxicity."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — no biomarker requirements. Surgery is the only treatment modality that avoids the DNA repair pathway vulnerabilities inherent to FA and the radiation-induced malignancy risk of Li-Fraumeni syndrome."
        }
      },
      "mechanism_of_action": "Complete surgical excision of the primary tumor with adequate margins (target >= 5mm) combined with ipsilateral selective neck dissection (levels I-III) for occult nodal disease staging. Removes the tumor without systemic DNA damage, cr
... (truncated — read full file from experiment_reports\TN-009_report.json)
```
