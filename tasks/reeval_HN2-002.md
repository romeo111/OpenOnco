# Re-evaluation Task: HN2-002

## Context
- **Case ID**: HN2-002
- **Cancer type**: Ethmoid Sinus Intestinal-Type Adenocarcinoma (ITAC)
- **Stage**: T3N0M0 (Stage III, cribriform plate involvement)
- **Molecular profile**: CDX2+, CK20+, Intestinal immunophenotype, EGFR wild-type (no activating mutation), Occupational etiology: hardwood dust exposure (furniture maker), Microsatellite stable
- **Report file**: experiment_reports\HN2-002_report.json
- **Current score**: 82/100
- **Gap analysis (local GPU)**: The lack of data on Topical 5-Fluorouracil (Post-Surgical Adjuvant) and Endoscopic Debulking + Topical 5-FU (Without Forma) procedures significantly hampers the report's comprehensiveness, as these treatments are crucial for assessing the efficacy of adjuvant therapies in head and neck cancer. Filling these gaps with high-quality data will enable a more accurate evaluation of treatment outcomes, thereby improving the overall score from 82/100 to a higher rating.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  10/25  |  40.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (40.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-002_report.json`.

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
    "cancer_type": "Ethmoid Sinus Intestinal-Type Adenocarcinoma (ITAC)",
    "stage": "T3N0M0 (Stage III, cribriform plate involvement)",
    "molecular_profile": [
      "CDX2+",
      "CK20+",
      "Intestinal immunophenotype",
      "EGFR wild-type (no activating mutation)",
      "Occupational etiology: hardwood dust exposure (furniture maker)",
      "Microsatellite stable"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Endoscopic Endonasal Resection + Adjuvant IMRT (60-66 Gy)",
      "category": "Standard of Care",
      "composite_rating": 8.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Large retrospective cohort of 200 patients (Frontiers in Oncology 2025) with long-term follow-up. No Phase 3 RCTs exist for this rare tumor but strong institutional series consistently demonstrate outcomes. EEA has become standard-of-reference for most sinonasal malignancies"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 71.4%, 5-year DSS 85.1% in 200-patient series. EEA correlated with improved DSS vs external surgery for T3-T4 tumors. For T3N0M0 with clear margins, outcomes approach 70-80% 5-year survival"
        },
        "accessibility": {
          "score": 8,
          "rationale": "Available at major academic medical centers with experienced skull base surgical teams. Requires multidisciplinary team (ENT, neurosurgery, radiation oncology). Not available at all community hospitals"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "EEA has fewer complications than open craniofacial resection: shorter hospitalization (4 vs 7 days), improved cosmetic outcome, no facial incisions. Main risks include CSF leak (5-10%), epistaxis, orbital complications"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirements. Universal applicability for all ITAC subtypes regardless of molecular profile. Surgery is the cornerstone for all resectable disease"
        }
      },
      "mechanism_of_action": "Endoscopic endonasal approach provides minimally invasive transnasal access for complete tumor resection with transnasal craniectomy for cribriform plate involvement. Adjuvant IMRT delivers conformal radiation (60-66 Gy in 30-33 fractions) to the tumor bed and at-risk margins while sparing critical structures (optic nerves, brain). Combined modality targets residual microscopic disease and reduces local recurrence from 50% (surgery alone) to approximately 15-20%.",
      "key_evidence": {
        "study_name": "Long-term outcomes of endoscopic resection and tailored adjuvant radiotherapy for sinonasal ITAC (200-patient cohort)",
        "journal": "Frontiers in Oncology",
        "year": 2025,
        "sample_size": 200,
        "os_months": {
          "treatment": 0,
          "control": 0,
... (truncated — read full file from experiment_reports\HN2-002_report.json)
```
