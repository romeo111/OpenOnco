Research the following cancer case and produce a comprehensive JSON report.

## Patient Case
- **Cancer type**: Tonsillar squamous cell carcinoma — HPV-positive
- **Stage**: Stage I (T2N1M0, AJCC 8th HPV+)
- **Molecular markers**: HPV p16+, PD-L1 CPS >=20
- **Patient**: 45 year old male
- **Performance status**: ECOG 0
- **Risk factors**: HPV exposure, non-smoker
- **Comorbidities**: none

## Research Strategy
Follow the research strategy below for search queries, source prioritization,
rating calibration, and output targets:

# Research Strategy — Agent-Editable Configuration
#
# This file is the ONLY file the autoresearch loop agent may edit.
# It parameterizes how cancer research reports are generated.
# The outer loop (program.md) will modify this file to improve quality scores.
#
# Version: seed-1.0 (extracted from SKILL.md)

## Search Budget Allocation

Total searches per case: 15
Distribution across tiers:

| Tier | Searches | Priority |
|------|----------|----------|
| Tier 1 — Standard of Care | 3 | HIGH — always execute first |
| Tier 2 — Approved Targeted/Immuno | 3 | HIGH |
| Tier 3 — Clinical Trials | 3 | MEDIUM |
| Tier 4 — Experimental/Cutting-Edge | 2 | MEDIUM |
| Tier 5 — Combination Strategies | 2 | MEDIUM |
| Tier 6 — Supportive/Adjunctive | 2 | LOW — execute last |

## Search Query Templates

### Tier 1 — Standard of Care
```
{cancer_type} NCCN guidelines 2025 2026
{cancer_type} standard of care first line treatment
{cancer_type} {stage} treatment protocol current
```

### Tier 2 — Approved Targeted & Immunotherapies
```
{cancer_type} approved targeted therapy 2025 2026
{cancer_type} immunotherapy checkpoint inhibitor results
{cancer_type} {molecular_markers} targeted therapy
```

### Tier 3 — Clinical Trials & Emerging
```
{cancer_type} clinical trial phase 3 results 2025 2026
{cancer_type} breakthrough therapy designation
{cancer_type} antibody drug conjugate OR bispecific antibody trial
```

### Tier 4 — Experimental & Cutting-Edge
```
{cancer_type} mRNA vaccine OR neoantigen therapy trial
{cancer_type} novel experimental therapy 2025 2026
```

### Tier 5 — Combination Strategies
```
{cancer_type} combination therapy overall survival improvement
{cancer_type} synergistic combination regimen results
```

### Tier 6 — Supportive & Adjunctive
```
{cancer_type} exercise OR nutrition survival benefit study
{cancer_type} supportive care early integration survival impact
```

## Source Fetch Prioritization

When choosing which search results to fetch with web_fetch, prioritize in this order:

1. **NCCN/ESMO guidelines** — always fetch if found
2. **Phase 3 RCT publications** in major journals (NEJM, Lancet, JCO, Annals of Oncology)
3. **FDA/EMA approval announcements** — for approved therapies
4. **ClinicalTrials.gov entries** — for active trials
5. **Phase 2 trial results** with survival endpoints
6. **Conference abstracts** (ASCO, ESMO, AACR) from 2024-2026
7. **Systematic reviews / meta-analyses** — for supportive care evidence
8. **Institutional treatment protocols** — major cancer centers

Fetch at least 8 sources per case. Aim for 12-15.

## Treatment Inclusion Criteria

Include a treatment if ANY of these apply:
- It is current standard of care for this cancer type/stage
- It has Phase 2+ data showing clinical benefit (ORR ≥20% or OS/PFS improvement)
- It has FDA/EMA approval for this indication
- It has breakthrough therapy designation for this cancer
- It is in an actively recruiting Phase 3 trial
- It targets a specific molecular marker present in the case

Exclude:
- Preclinical-only approaches with no human data (unless uniquely promising)
- Withdrawn or failed therapies
- Approaches without any published data

Target: 8-15 treatments per case, spanning all 6 tiers.

## Rating Calibration Rubric

When assigning scores to the 5 rating factors, follow these anchors:

### Evidence Level (weight: 30%)
- **10**: Large Phase 3 RCT, published in top journal, >500 patients
- **8-9**: Phase 3 RCT, moderate sample size, clear statistical significance
- **7**: Phase 2 with strong results, or Phase 3 with small sample
- **5-6**: Phase 2 with moderate results
- **4**: Phase 1 with promising signals, or Phase 2 with mixed results
- **2-3**: Phase 1 only, or case series
- **1**: Case reports, retrospective data only

### Survival Benefit (weight: 30%)
- **10**: >12 months OS improvement over SoC, or curative potential
- **8-9**: 6-12 months OS improvement, or >50% reduction in death risk
- **6-7**: 3-6 months OS improvement, or significant PFS gain
- **4-5**: 1-3 months OS improvement, or moderate PFS improvement
- **2-3**: Marginal survival benefit, mainly response rate improvement
- **1**: No demonstrated survival benefit, preclinical extrapolation only

### Accessibility (weight: 15%)
- **10**: FDA + EMA approved, widely available
- **8-9**: FDA approved, available at most oncology centers
- **7**: Available through Phase 3 trial at multiple sites
- **5-6**: Phase 2 trial, limited sites
- **3-4**: Phase 1 trial, very limited access
- **1-2**: Research only, not accessible to patients

### Safety Profile (weight: 15%)
- **10**: Minimal side effects, well-tolerated by most patients
- **7-8**: Manageable side effects with standard supportive care
- **5-6**: Significant but manageable toxicity, may require dose modifications
- **3-4**: Serious toxicity risk, requires close monitoring
- **1-2**: Life-threatening toxicity potential, narrow therapeutic window

### Biomarker Match (weight: 10%)
- **10**: No biomarker required (universal applicability)
- **7-8**: Requires common biomarker (present in >30% of cases)
- **5**: Biomarker status unknown or not yet determined
- **3-4**: Requires rare biomarker (present in <10% of cases)
- **1-2**: Requires ultra-rare biomarker or specific combination

## Output Emphasis Guidance

When generating reports, emphasize:

1. **Quantitative survival data** over qualitative descriptions — always include OS, PFS, ORR numbers with confidence intervals where available
2. **Comparison to standard of care** — every treatment should reference what it's compared against
3. **Actionable trial information** — include NCT numbers, recruiting status, and key eligibility criteria
4. **Biomarker requirements** — prominently flag which treatments require specific markers
5. **Source URLs** — every treatment must have at least one source URL

## Data Density Targets

Per treatment entry, aim to populate:
- `key_evidence.study_name` and `key_evidence.journal` — always
- `key_evidence.sample_size` — always (even if approximate)
- `key_evidence.os_months.treatment` and `.control` — when available
- `key_evidence.pfs_months.treatment` and `.control` — when available
- `key_evidence.orr_percent.treatment` — when available
- `key_evidence.os_months.hazard_ratio` and `.p_value` — for Phase 3 data
- `biomarker_requirements` — always (use empty list if universal)
- `notable_side_effects` — always list top 3-5 side effects
- `source_urls` — minimum 1 URL per treatment

## Combination Strategy Guidance

Generate at least 4 combination strategies per report:
- One SoC + immunotherapy combination
- One targeted therapy + immunotherapy combination
- One novel combination from clinical trials
- One evidence-based supportive add-on

Each combo must have: base_therapy, combination_partner, evidence_level, and a rationale of ≥20 words.

## Supportive Care Guidance

Include at least 4 supportive care approaches:
- Exercise/physical activity programs
- Nutritional interventions
- Early palliative care integration
- At least one repurposed drug or novel supportive approach

Each must have: approach, evidence (study citation), benefit (quantified if possible), and recommendation_level.


## Output Requirements
Generate a JSON report matching the schema in output_template.md.
The JSON must include: report_metadata, treatments (8-15), clinical_trials,
combination_strategies, supportive_care, and sources.

Save the JSON report to: experiment_reports/HN3-003_report.json
