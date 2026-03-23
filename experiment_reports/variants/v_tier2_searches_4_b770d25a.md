<!-- VARIANT METADATA
variant_id: v_tier2_searches_4_b770d25a
base_hash: 3e0d530775
mutation: tier2_searches: 3 -> 4
generated_at: 2026-03-23T17:41:27.660377
-->

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
| Tier 2 — Approved Targeted/Immuno | 4 | HIGH |
| Tier 3 — Clinical Trials | 3 | MEDIUM |
| Tier 4 — Experimental/Cutting-Edge | 2 | MEDIUM |
| Tier 5 — Combination Strategies | 2 | MEDIUM |
| Tier 6 — Supportive/Adjunctive | 2 | LOW — execute last |

## Complexity Classifier

Compute a complexity score per case before searching. Higher complexity = more searches.
`run_experiment.py` parses this section automatically — do NOT rename headers or table columns.

### Complexity Factors (additive)

| Factor | Condition | Points |
|--------|-----------|--------|
| Rare histology | cancer_type contains: adenoid cystic, mucoepidermoid, acinic cell, salivary gland, sinonasal, nasopharyngeal, paraganglioma, sarcoma, lymphoma, melanoma, chordoma, esthesioneuroblastoma, SNUC, NUT, plasmacytoma, Kaposi, ameloblastic, Ewing | +3 |
| Multiple molecular markers | len(molecular_markers) >= 3 | +2 |
| Actionable fusion or rare mutation | any marker contains: fusion, rearrangement, amplification, NTRK, ALK, ROS1, RET, BRAF V600E, MYB-NFIB, ETV6, EWSR1 | +2 |
| Poor performance status | performance_status contains: ECOG 2, ECOG 3, ECOG 4 | +3 |
| Metastatic or unresectable | stage contains: M1, IVB, IVC, unresectable | +2 |
| Prior treatment complication | risk_factors contains: prior radiation, prior surgery, second primary, recurrent | +1 |

### Budget Tiers

| Complexity Score | Total Searches | Label |
|-----------------|----------------|-------|
| 0–2 | 10 | simple |
| 3–5 | 15 | standard |
| 6–8 | 18 | complex |
| 9+ | 20 | highly_complex |

### Tier Distribution for Complex Cases

When total budget > 15, add extra searches to tiers 3 and 4 first (trials + experimental).
Tiers 1 and 2 always get at least 3 searches. Tier 6 stays at 2 unless budget allows more.

---

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

### Tier 3 — Clinical Trials, Emerging & De-escalation
```
{cancer_type} clinical trial phase 3 results 2025 2026
{cancer_type} breakthrough therapy designation
{cancer_type} antibody drug conjugate OR bispecific antibody trial
{cancer_type} de-escalation OR de-intensification OR reduced-dose trial
{cancer_type} network meta-analysis OR systematic review comparative effectiveness
```
De-escalation note: For HPV-positive oropharyngeal, nasopharyngeal, and any cancer
where de-intensification trials are active, ALWAYS run the de-escalation query
(e.g., RTOG 1016, De-ESCALaTE HPV, NRG-HN002, PATHOS, E3311).

### Tier 4 — Experimental & Cutting-Edge
```
{cancer_type} mRNA vaccine OR neoantigen therapy trial
{cancer_type} novel experimental therapy 2025 2026
{cancer_type} failed trial negative result inferior outcome site:pubmed.ncbi.nlm.nih.gov OR site:nejm.org OR site:thelancet.com
```
Negative-result note: Always search for trials that failed or showed inferiority.
Knowing what does NOT work is as clinically important as knowing what does.
Example: RTOG 1016 showed cetuximab inferior to cisplatin for HPV+ OPSCC —
this is practice-defining negative evidence that must be captured.

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
3. **Network meta-analyses and Cochrane systematic reviews** — highest-level comparative evidence; often more useful than a single RCT for treatment comparisons
4. **FDA/EMA approval announcements** — for approved therapies
5. **ClinicalTrials.gov entries** — for active trials (prefer direct clinicaltrials.gov URLs)
6. **Phase 2 trial results** with survival endpoints
7. **Negative/failed trial publications** — look for these explicitly; document what was tried and did not work
8. **Conference abstracts** (ASCO, ESMO, AACR) from 2024-2026 — label as preliminary
9. **Institutional treatment protocols** — major cancer centers

Fetch at least 8 sources per case. Aim for 12-15.

Source recency note: For rapidly evolving cancers (NSCLC, melanoma, HNSCC immunotherapy),
prioritize sources from 2021-2026. For foundational evidence (surgical techniques,
radiation fractionation, basic chemotherapy regimens), older landmark trials (2000-2020)
remain valid and should NOT be excluded by date filters.

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

## Treatment Intent Classification

**MANDATORY**: Every treatment entry MUST include an `intent` field. This is the most
clinically critical piece of metadata — it determines where a treatment fits in the
patient's journey and prevents curative/palliative conflation.

| Intent Value | Definition | Use When |
|---|---|---|
| `curative` | Definitive therapy for localized disease | Stage I-III, resectable |
| `adjuvant` | Post-operative treatment to prevent recurrence | After surgery |
| `neoadjuvant` | Pre-operative treatment to shrink tumor | Before planned surgery |
| `palliative` | Treatment for Stage IV M1 or unresectable recurrent disease | Not curable |
| `salvage` | Second/third-line therapy after prior treatment failure | Recurrent/refractory |
| `maintenance` | Ongoing treatment to delay progression after response | Post-induction |
| `preventive` | Risk reduction or surveillance | Post-curative completion |

### RANKING RULE — Critical
**Never rank a palliative treatment above a curative treatment for a patient with
potentially curable disease (Stage I-III, resectable Stage IVA/IVB).**

For curative-intent patients: sort by intent group first:
1. curative / adjuvant / neoadjuvant treatments (ranked among themselves)
2. maintenance treatments
3. palliative / salvage treatments (listed separately, lower ranking)

For palliative-intent patients (Stage IV M1, unresectable): palliative treatments
rank first; curative approaches are listed only as historical context.

Example of WRONG ranking: Patient with Stage III HPV+ OPSCC, rank #2 = KEYNOTE-048
(R/M pembrolizumab+chemo — this is palliative-intent, should not be rank #2).
Example of CORRECT ranking: rank #2 = reduced-dose RT de-escalation trial (curative-intent).

## Performance Status Treatment Gating

Before including a treatment, verify ECOG PS compatibility. Flag incompatible
treatments clearly rather than excluding them — the clinical team needs to know
the option exists but requires PS improvement or is contraindicated.

| ECOG PS | Contraindicated Approaches | Alternative |
|---------|---------------------------|-------------|
| 0–1 | None — full spectrum appropriate | — |
| 2 | High-dose cisplatin (100 mg/m²), aggressive multiagent chemo | Carboplatin, cetuximab, or reduced-dose regimens |
| 3 | Cisplatin-based CRT, combination immunotherapy + chemo | Single-agent immunotherapy, best supportive care |
| 4 | All cytotoxic chemotherapy | Best supportive care only |

Label treatments that require ECOG 0-1 with `"ps_requirement": "ECOG 0-1 required"`.
Label treatments suitable for ECOG 2 with `"ps_requirement": "ECOG 0-2 acceptable"`.

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
6. **Treatment intent** — every treatment must have an `intent` field (curative/adjuvant/neoadjuvant/palliative/salvage/maintenance)
7. **QoL and functional outcomes** — for head & neck, lung, GI, and GU cancers, document:
   - Dysphagia severity and PEG tube risk (H&N)
   - Xerostomia (permanent vs. temporary, H&N)
   - Ototoxicity / hearing loss (cisplatin-containing regimens)
   - Peripheral neuropathy (taxane/platinum regimens)
   - Relevant QoL instruments: MDADI, FACT-H&N, EORTC QLQ-H&N43, EORTC QLQ-C30
8. **Long-term vs. acute toxicity** — distinguish in `notable_side_effects`:
   - Acute (during/immediately post-treatment): grade 3+ mucositis, neutropenia, emesis
   - Late/permanent: xerostomia, osteoradionecrosis, hearing loss, neuropathy, hypothyroidism
9. **Negative evidence** — when a treatment was tested and found inferior or harmful,
   document this explicitly. A failed trial result is as important as a positive one.

## Data Density Targets

Per treatment entry, aim to populate:
- `key_evidence.study_name` and `key_evidence.journal` — always
- `key_evidence.sample_size` — always (even if approximate)
- `key_evidence.os_months.treatment` and `.control` — when available; BOTH arms required for magnitude scoring
- `key_evidence.pfs_months.treatment` and `.control` — when available
- `key_evidence.orr_percent.treatment` — when available
- `key_evidence.os_months.hazard_ratio` and `.p_value` — for Phase 3 data
- `biomarker_requirements` — always (use empty list if universal)
- `notable_side_effects` — always list top 3-5 side effects, distinguish acute vs. late
- `source_urls` — minimum 1 URL per treatment
- `intent` — MANDATORY: curative / adjuvant / neoadjuvant / palliative / salvage / maintenance
- `ps_requirement` — when treatment requires specific ECOG PS (e.g., "ECOG 0-1 required")
- `qol_impact` — for H&N, lung, GI cancers: describe functional impact on swallowing, speech, hearing, breathing

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

For head & neck cancers specifically, also include:
- **Prophylactic swallowing exercises** (pre- and during-RT): RCT evidence showing reduced long-term dysphagia and PEG tube dependence (DIGEST trial, Carroll et al.)
- **Intensity-Modulated Proton Therapy (IMPT)** when available: reduces xerostomia and dysphagia vs. IMRT (MD Anderson data)
- **Amifostine** for xerostomia prevention during RT: controversial but FDA-approved; cite evidence and current guideline status
- **Hyperbaric oxygen** for osteoradionecrosis prevention/treatment: Level 2 evidence; relevant for mandibular radiation fields

Each must have: approach, evidence (study citation), benefit (quantified if possible), recommendation_level, and for H&N cases: qol_instrument (the validated scale used to measure benefit, e.g., MDADI, FACT-H&N).
