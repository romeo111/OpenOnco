# Re-evaluation Task: HN2-003

## Context
- **Case ID**: HN2-003
- **Cancer type**: Esthesioneuroblastoma (Olfactory Neuroblastoma)
- **Stage**: Kadish C (intracranial extension), Hyams Grade III
- **Molecular profile**: Synaptophysin-positive, Chromogranin A-positive, SSTR2-positive (expected >82% prevalence), Neuroendocrine differentiation, Potential FGFR3 amplification (28% prevalence), Potential IDH2 R172 mutation (35% in basal-like subtype)
- **Report file**: experiment_reports\HN2-003_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-003 are the lack of data on Neoadjuvant Cisplatin/Etoposide + Surgery + Adjuvant chemotherapy and Elective Neck Irradiation / Neck Dissection for N0 neck status, which will improve the score by providing more comprehensive information on treatment outcomes for patients with specific cancer types. Filling these gaps will enable researchers to better understand the effectiveness of these treatments and provide more accurate recommendations for patient care, ultimately leading to improved patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-003_report.json`.

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
    "cancer_type": "Esthesioneuroblastoma (Olfactory Neuroblastoma)",
    "stage": "Kadish C (intracranial extension), Hyams Grade III",
    "molecular_profile": [
      "Synaptophysin-positive",
      "Chromogranin A-positive",
      "SSTR2-positive (expected >82% prevalence)",
      "Neuroendocrine differentiation",
      "Potential FGFR3 amplification (28% prevalence)",
      "Potential IDH2 R172 mutation (35% in basal-like subtype)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Craniofacial Resection + Adjuvant Intensity-Modulated Radiation Therapy (IMRT)",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Decades of institutional series and meta-analyses consistently demonstrate superior outcomes with surgery plus adjuvant RT. Largest series (931 patients) showed HR 0.22 for combined modality. 5-year OS 84.4% for surgery+RT in 64-patient series. Not phase 3 RCT due to rarity, but highest available evidence for ENB."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 70.8-84.4% for Kadish C with combined modality therapy. 5-year local control 85.9% with adjuvant RT vs 72.7% without. Hyams III 5-year OS approximately 73.7%. Represents best achievable survival for this stage/grade."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at all major academic medical centers with skull base surgery programs. IMRT widely available. Established standard of care approach requiring no special drug access."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Craniofacial resection carries risks of CSF leak (1-6%), meningitis (1.8-4.5%), and anosmia. IMRT late toxicities infrequent (11.5%) including dysosmia, hearing loss, rare temporal lobe necrosis. Endoscopic approach reduces morbidity significantly."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of molecular profile. Standard approach for all ENB patients with Kadish C disease."
        }
      },
      "mechanism_of_action": "Complete surgical resection of tumor via craniofacial approach (open or endoscopic endonasal) removes gross disease including intracranial extension. Adjuvant IMRT (60-70 Gy) delivers conformal radiation to the tumor bed and margins to eliminate microscopic residual disease while sparing critical structures (optic nerves, brainstem, temporal lobes).",
      "key_evidence": {
        "study_name": "Long-Term Survival Outcomes and Treatment Experience of 64 Patients With Esthesioneuroblastoma",
        "journal": "Frontiers in Oncology",
        "year": 2021,
        "sample_size": 64,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
 
... (truncated — read full file from experiment_reports\HN2-003_report.json)
```
