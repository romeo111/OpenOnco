# Re-evaluation Task: HN3-027

## Context
- **Case ID**: HN3-027
- **Cancer type**: Scalp Angiosarcoma (Radiation-Induced, Locally Advanced)
- **Stage**: Locally advanced, 15cm, radiation-induced
- **Molecular profile**: MYC amplification, VEGFR amplification, Radiation-induced secondary angiosarcoma
- **Report file**: experiment_reports\HN3-027_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can, however, help with something else.

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

Read the full report JSON at `experiment_reports\HN3-027_report.json`.

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
    "cancer_type": "Scalp Angiosarcoma (Radiation-Induced, Locally Advanced)",
    "stage": "Locally advanced, 15cm, radiation-induced",
    "molecular_profile": [
      "MYC amplification",
      "VEGFR amplification",
      "Radiation-induced secondary angiosarcoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Weekly Paclitaxel Monotherapy",
      "category": "Standard of Care",
      "composite_rating": 7.3,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "ANGIOTAX phase 2 trial and multiple retrospective series; ORR 19-89% depending on study; most active single-agent chemotherapy for angiosarcoma; widely accepted first-line option"
        },
        "survival_benefit": {
          "score": 6,
          "rationale": "Disease control rate 74% in ANGIOTAX; median PFS approximately 4-6 months; scalp/face angiosarcoma may have better response to paclitaxel than other sites"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Generic paclitaxel widely available; weekly dosing schedule well-established; standard first-line chemotherapy for angiosarcoma"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Weekly low-dose schedule provides favorable safety profile especially in elderly; manageable neuropathy, myelosuppression, alopecia"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Anti-angiogenic properties of taxanes particularly relevant for vascular tumors; activity independent of MYC or VEGFR amplification status"
        }
      },
      "mechanism_of_action": "Paclitaxel binds to beta-tubulin subunits of microtubules, stabilizing them and preventing depolymerization required for cell division. At metronomic doses, paclitaxel also has potent anti-angiogenic effects by inhibiting endothelial cell proliferation and migration, particularly relevant for angiosarcoma's vascular biology.",
      "key_evidence": {
        "study_name": "ANGIOTAX Phase 2 Trial",
        "journal": "Journal of Clinical Oncology",
        "year": 2008,
        "sample_size": 30,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 4.0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 19,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Peripheral neuropathy",
        "Myelosuppression",
        "Fatigue",
        "Alopecia",
        "Hypersensitivity reactions"
      ],
      "availability": "FDA Approved (generic)",
      "source_urls": [
        "https://pubmed.ncbi.nlm.nih.gov/10570428/",
        "https://www.annalsofoncology.org/article/S0923-7534(19)34396-0/fulltext"
      ]
    },
    {
      "rank":
... (truncated — read full file from experiment_reports\HN3-027_report.json)
```
