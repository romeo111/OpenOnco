# Re-evaluation Task: HN2-001

## Context
- **Case ID**: HN2-001
- **Cancer type**: Maxillary sinus squamous cell carcinoma
- **Stage**: T4aN0M0 (Stage IVA) — orbital floor invasion
- **Molecular profile**: PD-L1 CPS 10, TP53 mutation, EGFR overexpression, Occupational wood dust exposure (woodworker)
- **Report file**: experiment_reports\HN2-001_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| rating_calibration                  |  15/15  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-001_report.json`.

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
    "cancer_type": "Maxillary sinus squamous cell carcinoma",
    "stage": "T4aN0M0 (Stage IVA) — orbital floor invasion",
    "molecular_profile": [
      "PD-L1 CPS 10",
      "TP53 mutation",
      "EGFR overexpression",
      "Occupational wood dust exposure (woodworker)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Perioperative Pembrolizumab + Surgery + Adjuvant CRT (KEYNOTE-689 Regimen)",
      "category": "Immunotherapy",
      "composite_rating": 7.7,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Phase 3 RCT (KEYNOTE-689) with 704 patients showed statistically significant EFS benefit (HR 0.73, p=0.0041). FDA approved June 2025 for perioperative use in PD-L1+ LA-HNSCC. First positive perioperative trial in HNSCC in 20+ years. Published in NEJM 2025."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Median EFS 51.8 months vs 30.4 months with SOC alone. 36-month EFS 57.6% vs 46.4%. However, sinonasal subsites were a minority of enrolled patients and benefit may differ. OS data still maturing."
        },
        "accessibility": {
          "score": 8,
          "rationale": "FDA approved (June 2025) for PD-L1-expressing resectable LA-HNSCC. Pembrolizumab widely available. Patient's PD-L1 CPS 10 meets eligibility threshold (CPS >= 1). Requires coordination of neoadjuvant dosing before surgery."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Neoadjuvant pembrolizumab did not affect surgical completion rates. Immune-related adverse events (colitis, hepatitis, pneumonitis, thyroiditis) occur in ~15-20% but mostly grade 1-2. Added to baseline surgical + CRT toxicity."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Patient's PD-L1 CPS 10 meets the CPS >= 1 threshold for approved indication. Benefit increases with higher CPS. TP53 mutation may reduce immunotherapy benefit per some analyses, but PD-L1 positivity is the validated biomarker."
        }
      },
      "mechanism_of_action": "Neoadjuvant pembrolizumab (2 cycles, 200 mg IV q3w) primes antitumor T-cell response before surgery by blocking PD-1/PD-L1 interaction, potentially converting immunologically cold tumors to hot. Adjuvant pembrolizumab (15 cycles) maintains immune surveillance post-surgery to eliminate micrometastatic disease. Combined with standard adjuvant RT +/- cisplatin.",
      "key_evidence": {
        "study_name": "KEYNOTE-689",
        "journal": "New England Journal of Medicine",
        "year": 2025,
        "sample_size": 704,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.73,
          "p_value": 0.0041
        },
        "pfs_months": {
          "treatment": 51.8,
          "control": 30.4
        },
        "orr_percent": {
          "treatment": 0,
          "c
... (truncated — read full file from experiment_reports\HN2-001_report.json)
```
