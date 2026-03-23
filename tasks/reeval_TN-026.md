# Re-evaluation Task: TN-026

## Context
- **Case ID**: TN-026
- **Cancer type**: Neck Synovial Sarcoma (High-Grade, Deep, >5cm, SS18-SSX Fusion Positive)
- **Stage**: Localized high-risk (>5cm, deep, high-grade) — 45-year-old male
- **Molecular profile**: SS18-SSX fusion positive (pathognomonic translocation t(X;18)(p11.2;q11.2)), High-grade histology, NY-ESO-1 expression likely (~80% of synovial sarcomas), MAGE-A4 expression likely (~82-88% of synovial sarcomas), PRAME expression likely (~70-86% of synovial sarcomas)
- **Report file**: experiment_reports\TN-026_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The lack of data on High-Dose Ifosfamide Monotherapy (14 g/m²) and Trabectedin (Yondelis) treatment regimens is a significant gap, as these therapies are crucial for patients with advanced cancer who have not responded to standard treatments, and including this data will provide more comprehensive insights into their efficacy. Filling in the gaps on Pazopanib (Votrient), Afamitresgene Autoleucel (Tecelra/Afami-cel) — MAG, Letetresgene Autoleucel (Lete-cel) — NY-ESO-1-dire, and Regorafenib (Stivarga) treatment regimens will also improve the score by providing more detailed information on targeted therapies for specific cancer types.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-026_report.json`.

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
    "cancer_type": "Neck Synovial Sarcoma (High-Grade, Deep, >5cm, SS18-SSX Fusion Positive)",
    "stage": "Localized high-risk (>5cm, deep, high-grade) — 45-year-old male",
    "molecular_profile": [
      "SS18-SSX fusion positive (pathognomonic translocation t(X;18)(p11.2;q11.2))",
      "High-grade histology",
      "NY-ESO-1 expression likely (~80% of synovial sarcomas)",
      "MAGE-A4 expression likely (~82-88% of synovial sarcomas)",
      "PRAME expression likely (~70-86% of synovial sarcomas)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Surgical Excision with Negative Margins + Adjuvant Radiation Therapy (60-66 Gy)",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Supported by NCCN/ESMO guidelines, large retrospective series, and decades of consistent data establishing surgery plus RT as cornerstone treatment. Head/neck synovial sarcoma series (243 cases) show 60.3% alive NED. 5-year survival 76% with combined modality."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "For localized high-grade synovial sarcoma >5cm, complete R0 resection with adjuvant RT achieves 5-year OS of 60-76%. RT significantly reduces local recurrence. Without RT, local recurrence rates exceed 30-40% in high-grade tumors. In neck anatomy, achieving clear margins is challenging but critical."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard of care available at all major cancer centers worldwide. Surgery and radiation therapy are universally accessible treatments with established infrastructure."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Neck surgery carries risks to critical structures (carotid, jugular, cranial nerves, brachial plexus). Radiation to neck may cause dysphagia, xerostomia, fibrosis, hypothyroidism, and late-onset vascular complications. Functional morbidity can be significant depending on extent of resection."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of biomarker status. SS18-SSX fusion confirms synovial sarcoma diagnosis supporting treatment selection."
        }
      },
      "mechanism_of_action": "Wide excision removes the primary tumor with a cuff of normal tissue to achieve microscopically negative margins (R0 resection). Adjuvant external beam radiation therapy (60-66 Gy in 30-33 fractions) eliminates microscopic residual disease, reducing local recurrence. In neck synovial sarcoma, anatomic constraints may limit surgical margins, making RT particularly critical for local control.",
      "key_evidence": {
        "study_name": "Oncologic Outcomes in Patients with Localized Primary Head and Neck Synovial Sarcoma (MDPI 2024) and 
... (truncated — read full file from experiment_reports\TN-026_report.json)
```
