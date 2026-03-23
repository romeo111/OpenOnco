# Cancer Research Output Template

Use this template for the Markdown report output.

---

```markdown
# Cancer Research Report: [Cancer Type]
### Maximum Life Extension Treatment Analysis
**Generated**: [Date]
**Cancer Type**: [Full medical name]
**Stage**: [If specified, otherwise "All stages covered"]
**Molecular Profile**: [If specified, otherwise "General — biomarker-specific options noted"]

---

> ⚠️ **MEDICAL DISCLAIMER**: This document is generated for research and educational
> purposes only. It is NOT medical advice. All treatment decisions must be made in
> consultation with a qualified oncology team who can evaluate the patient's individual
> circumstances. Never start, stop, or change treatment based solely on this document.

---

## 1. Executive Summary

[2-3 paragraph overview: what this cancer is, current prognosis landscape, and the
top 3 most promising approaches identified by this research with their ratings]

**Top 3 Approaches by Evidence-Weighted Rating:**

| Rank | Approach | Rating | Evidence Level | Key Benefit |
|------|----------|--------|----------------|-------------|
| 1 | [Name] | [X.X/10] | [Phase/Level] | [Brief survival stat] |
| 2 | [Name] | [X.X/10] | [Phase/Level] | [Brief survival stat] |
| 3 | [Name] | [X.X/10] | [Phase/Level] | [Brief survival stat] |

---

## 2. Standard of Care Overview

### Current First-Line Treatment
[Description of NCCN/ESMO-recommended first-line therapy]

### Expected Outcomes with Standard Treatment
- **Median Overall Survival (OS)**: [X months/years]
- **Median Progression-Free Survival (PFS)**: [X months]
- **Overall Response Rate (ORR)**: [X%]
- **5-Year Survival Rate**: [X%]

### Key Guidelines Referenced
- [Guideline 1 — organization, version, date]
- [Guideline 2]

---

## 3. Ranked Treatment Approaches

### 3.1 [Treatment Name] — Rating: [X.X/10]

**Category**: [Standard of Care / Approved Targeted / Immunotherapy / Clinical Trial / Experimental]
**Evidence Level**: [Phase 3 RCT / Phase 2 / Phase 1 / Preclinical]
**Availability**: [FDA Approved / EMA Approved / Clinical Trial / Research Only]

**Mechanism of Action**:
[1-2 sentences on how this therapy works]

**Key Evidence**:
- Study: [Trial name/ID], [Journal], [Year]
- Population: [N patients, key demographics]
- Results: OS [X months vs Y months control], HR [X.XX], p=[X.XXX]
- PFS: [X months vs Y months], ORR: [X% vs Y%]

**Rating Breakdown**:
| Factor | Score | Rationale |
|--------|-------|-----------|
| Evidence Level | [X/10] | [Why] |
| Survival Benefit | [X/10] | [Why] |
| Accessibility | [X/10] | [Why] |
| Safety Profile | [X/10] | [Why] |
| Biomarker Match | [X/10] | [Why] |

**Biomarker Requirements**: [Required markers, if any]
**Notable Side Effects**: [Key toxicities]
**Source**: [URL or citation]

---

[Repeat Section 3.X for each treatment approach, ordered by rating descending]

---

## 4. Clinical Trial Opportunities

### Active Phase 3 Trials

| Trial ID | Title | Phase | Status | Key Sites | Biomarker Req |
|-----------|-------|-------|--------|-----------|---------------|
| [NCT#] | [Name] | [Phase] | [Recruiting/Active] | [Countries] | [Markers] |

### Promising Phase 2 Trials

| Trial ID | Title | Phase | Early Results | Key Sites |
|-----------|-------|-------|---------------|-----------|
| [NCT#] | [Name] | [Phase] | [Brief data] | [Countries] |

**How to Find Trials**: Search [clinicaltrials.gov](https://clinicaltrials.gov) with
the cancer type and any molecular markers. Ask your oncologist about eligibility.

---

## 5. Emerging Research Pipeline

[Describe 3-5 experimental approaches not yet in late-stage trials but showing
promise. Include: mechanism, early data, timeline to potential availability,
and the research groups or companies behind them.]

### 5.1 [Approach Name]
- **Stage**: [Preclinical / Phase 1 / Early Phase 2]
- **Mechanism**: [How it works]
- **Early Data**: [Key results]
- **Timeline**: [Estimated years to potential approval]
- **Led By**: [Institution/Company]

---

## 6. Combination Strategy Matrix

[Which treatments can be combined for potential synergistic benefit]

| Base Therapy | Combination Partner | Evidence | Rationale |
|--------------|-------------------|----------|-----------|
| [Therapy A] | [Therapy B] | [Phase/Study] | [Why they may synergize] |

---

## 7. Supportive & Adjunctive Care

[Evidence-based approaches that may complement primary treatment]

### 7.1 [Approach — e.g., Exercise Programs]
- **Evidence**: [Study/meta-analysis]
- **Benefit**: [Survival improvement or QoL data]
- **Recommendation Level**: [Strong/Moderate/Emerging]

---

## 8. Methodology & Sources

### Research Methodology
This report was compiled by systematically searching:
- National Comprehensive Cancer Network (NCCN) guidelines
- European Society for Medical Oncology (ESMO) guidelines
- PubMed / peer-reviewed oncology journals
- ClinicalTrials.gov for active trials
- FDA/EMA drug approval databases
- Recent oncology conference presentations (ASCO, ESMO, AACR)

### Sources
[Numbered list of all sources cited in the report]

---

## 9. Appendix: Rating Methodology

Each treatment was scored on a 1-10 composite scale:
- **Evidence Level (30%)**: Phase 3 RCT=10, Phase 2=7, Phase 1=4, Preclinical=2
- **Survival Benefit (30%)**: Magnitude of OS/PFS improvement vs. standard of care
- **Accessibility (15%)**: FDA approved=10, Phase 3 trial=7, Phase 2=5, Phase 1=3
- **Safety Profile (15%)**: Well-tolerated=10, Manageable=7, Significant toxicity=4
- **Biomarker Match (10%)**: Universal=10, Common marker=7, Rare marker=4

**Composite** = (Evidence × 0.30) + (Survival × 0.30) + (Access × 0.15) + (Safety × 0.15) + (Biomarker × 0.10)
```

---

## JSON Output Template

Also generate a companion JSON file with this structure:

```json
{
  "report_metadata": {
    "generated_date": "YYYY-MM-DD",
    "cancer_type": "",
    "stage": "",
    "molecular_profile": []
  },
  "treatments": [
    {
      "rank": 1,
      "name": "",
      "category": "",
      "composite_rating": 0.0,
      "rating_breakdown": {
        "evidence_level": { "score": 0, "rationale": "" },
        "survival_benefit": { "score": 0, "rationale": "" },
        "accessibility": { "score": 0, "rationale": "" },
        "safety_profile": { "score": 0, "rationale": "" },
        "biomarker_match": { "score": 0, "rationale": "" }
      },
      "mechanism_of_action": "",
      "key_evidence": {
        "study_name": "",
        "journal": "",
        "year": 0,
        "sample_size": 0,
        "os_months": { "treatment": 0, "control": 0, "hazard_ratio": 0, "p_value": 0 },
        "pfs_months": { "treatment": 0, "control": 0 },
        "orr_percent": { "treatment": 0, "control": 0 }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [],
      "availability": "",
      "source_urls": []
    }
  ],
  "clinical_trials": [
    {
      "trial_id": "",
      "title": "",
      "phase": "",
      "status": "",
      "sites": [],
      "biomarker_requirements": [],
      "early_results": ""
    }
  ],
  "combination_strategies": [
    {
      "base_therapy": "",
      "combination_partner": "",
      "evidence_level": "",
      "rationale": ""
    }
  ],
  "supportive_care": [
    {
      "approach": "",
      "evidence": "",
      "benefit": "",
      "recommendation_level": ""
    }
  ],
  "sources": [
    {
      "index": 1,
      "title": "",
      "url": "",
      "type": ""
    }
  ]
}
```
