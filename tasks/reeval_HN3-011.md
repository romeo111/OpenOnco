# Re-evaluation Task: HN3-011

## Context
- **Case ID**: HN3-011
- **Cancer type**: Very Early Glottic Squamous Cell Carcinoma (T1a) — Single Vocal Cord
- **Stage**: T1aN0M0 (Stage I)
- **Molecular profile**: SCC histology, Single vocal cord involvement, No anterior commissure involvement
- **Report file**: experiment_reports\HN3-011_report.json
- **Current score**: 66/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-011 cancer research report include the lack of data on Intensity-Modulated Proton Therapy (IMPT) — Single Fraction and Stereotactic Body Radiation Therapy (SBRT) — 3 Fractions, which are essential for comprehensive treatment planning and patient outcomes. Filling these gaps will improve the score by providing more detailed information on innovative radiation therapies that can enhance treatment efficacy and reduce side effects for patients with head and neck cancer.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  10/25  |  40.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-011_report.json`.

Your task: Fix ONLY the `rating_breakdown` fields in the `treatments` array.

For each treatment, verify:
1. `evidence_level.score` matches the actual study phase:
   - Phase 3 RCT (N>=500, top journal) = 9-10
   - Phase 3 RCT (N<500) = 7-8
   - Phase 2 = 5-7
   - Phase 1 = 2-4
   - Case series / retrospective = 1-3
2. `survival_benefit.score` matches actual OS delta:
   - >12 months delta = 9-10
   - 6-12 months = 7-8
   - 3-6 months = 5-6
   - 1-3 months = 3-4
   - <1 month or no control = 1-2
3. `composite_rating` = weighted average (evidence 30%, survival 30%, access 15%, safety 15%, biomarker 10%)
4. Treatments must be re-sorted descending by composite_rating after changes

Do NOT change any other field. Return the complete corrected `treatments` array only.

## Output format

Return a valid JSON object containing ONLY the corrected section (e.g., `{"treatments": [...]}` or `{"sources": [...]}`).

Do NOT return the full report — only the corrected array. The runner will merge it back.

After returning the JSON, add one line:
`SCORE_IMPACT: <estimated new score>/100`

## Report JSON (for reference)

```json
{
  "report_metadata": {
    "case_id": "HN3-011",
    "generated_date": "2026-03-23",
    "cancer_type": "Very Early Glottic Squamous Cell Carcinoma (T1a) — Single Vocal Cord",
    "stage": "T1aN0M0 (Stage I)",
    "molecular_profile": [
      "SCC histology",
      "Single vocal cord involvement",
      "No anterior commissure involvement"
    ],
    "patient_context": "45-year-old male, voice professional (teacher), requiring optimal voice preservation"
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Transoral Laser Microsurgery (TLM) — CO2 Laser Cordectomy Type I/II (ELS Classification)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple large retrospective series and meta-analyses (404-patient reviews, systematic reviews) demonstrate 92-97% local control and 98-99% disease-specific survival for T1a glottic SCC"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year disease-specific survival 98-99%, 5-year overall survival 87.8%, larynx preservation 97.3%; cure rate effectively >95% with salvage options intact"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Widely available at major ENT centers worldwide, single outpatient procedure, minimal recovery time; cost-effective vs. 6-7 weeks of RT"
        },
        "safety_profile": {
          "score": 9,
          "rationale": "Complication rate ~1%, day-surgery procedure, no general radiation exposure, repeatable if needed; Type I/II cordectomy preserves vocal ligament"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability for T1a glottic SCC without anterior commissure involvement; ideal for superficial mid-cord lesions"
        }
      },
      "mechanism_of_action": "CO2 laser precisely excises the tumor with controlled depth. ELS Type I (subepithelial) removes epithelium only; Type II (subligamental) removes epithelium and Reinke's space. Preserves deeper vocal fold structures critical for voice production.",
      "key_evidence": {
        "study_name": "Transoral laser microsurgery for T1a glottic cancer: review of 404 cases",
        "journal": "European Archives of Oto-Rhino-Laryngology",
        "year": 2014,
        "sample_size": 404,
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
      "five_year_outcomes": {
        "local_control": "86.8-92.3%",
        "disease_specific_survival": "98-99%",
        "overall_survival": "87.8%",
        "larynx_preservation": "97.3%"
      },
      "biomarker_requirements": [
        "Confirmed SCC on biopsy"
      ],

... (truncated — read full file from experiment_reports\HN3-011_report.json)
```
