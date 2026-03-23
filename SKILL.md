---
name: cancer-research
description: >
  Deep cancer research skill for finding maximum life-extension treatment strategies.
  Use this skill whenever a user asks about cancer treatment options, cancer research,
  oncology treatment plans, survival optimization, clinical trials for cancer,
  immunotherapy options, or any query about extending life for a cancer patient.
  Triggers on: cancer type + treatment, "best treatment for [cancer]", "how to extend
  life with [cancer]", clinical trial search, oncology research, cancer prognosis
  optimization, "treatment plan for [cancer]", stage-specific cancer strategies,
  combination therapy research, emerging cancer treatments, experimental therapies.
  Also triggers when a user provides a cancer diagnosis and wants to understand all
  available options ranked by evidence quality and survival benefit.
---

# Cancer Research — Maximum Life Extension Treatment Planner

## Purpose

This skill performs deep, systematic research into cancer treatment options for a given
cancer type. It produces a comprehensive, evidence-ranked treatment plan that maximizes
patient life extension, drawing from established protocols, clinical trials, emerging
therapies, and cutting-edge research.

**IMPORTANT MEDICAL DISCLAIMER**: This skill generates research-grade information
summaries. All output must include a prominent disclaimer that this is NOT medical
advice and patients must consult their oncology team before making any treatment
decisions. This tool is for research and educational purposes only.

## Workflow

### Step 1: Parse the Input

Extract from the user's query:
- **Cancer type** (required) — e.g., "pancreatic adenocarcinoma", "NSCLC", "triple-negative breast cancer"
- **Stage** (if provided) — I through IV, or specific substaging
- **Molecular markers** (if provided) — e.g., EGFR+, HER2+, BRCA1/2, MSI-H, PD-L1 expression, KRAS G12C
- **Patient context** (if provided) — age range, prior treatments, comorbidities
- **Country/region** (if provided) — affects clinical trial availability and drug approvals

If the user provides only a cancer type, proceed with a general overview across all stages. Ask clarifying questions ONLY if the cancer type itself is ambiguous.

### Step 2: Research Strategy

Perform web searches across multiple evidence tiers. Use **10–20 searches** to build a comprehensive picture. Search categories:

#### Tier 1 — Standard of Care (SoC)
Search for NCCN guidelines, ESMO guidelines, and current first-line protocols.
Example queries:
- `[cancer type] NCCN guidelines 2025 2026`
- `[cancer type] standard of care first line treatment`
- `[cancer type] stage [N] treatment protocol`

#### Tier 2 — Approved Targeted & Immunotherapies
Search for FDA/EMA-approved targeted therapies and immunotherapies.
- `[cancer type] approved targeted therapy 2025 2026`
- `[cancer type] immunotherapy checkpoint inhibitor results`
- `[cancer type] [known molecular marker] targeted therapy`

#### Tier 3 — Clinical Trials & Emerging Therapies
Search for active Phase II/III trials and breakthrough designations.
- `[cancer type] clinical trial phase 3 results 2025 2026`
- `[cancer type] breakthrough therapy designation`
- `[cancer type] CAR-T cell therapy trial`
- `[cancer type] bispecific antibody trial`
- `[cancer type] antibody drug conjugate results`

#### Tier 4 — Experimental & Cutting-Edge Research
Search for novel approaches including mRNA vaccines, personalized neoantigen therapies,
epigenetic therapies, and other frontier science.
- `[cancer type] mRNA vaccine trial`
- `[cancer type] neoantigen personalized therapy`
- `[cancer type] tumor treating fields`
- `[cancer type] CRISPR gene therapy cancer`
- `[cancer type] radioligand therapy`
- `[cancer type] oncolytic virus therapy`

#### Tier 5 — Combination Strategies & Survival Data
Search for synergistic combinations and real-world survival outcomes.
- `[cancer type] combination therapy overall survival`
- `[cancer type] median survival improvement 2025 2026`
- `[cancer type] long term survivors research`

#### Tier 6 — Supportive & Adjunctive Approaches
Search for evidence-based supportive care that may extend survival.
- `[cancer type] exercise survival benefit study`
- `[cancer type] nutrition intervention trial`
- `[cancer type] fasting mimicking diet cancer research`
- `[cancer type] metformin repurposed cancer`
- `[cancer type] palliative care early integration survival`

### Step 3: Fetch and Analyze Key Sources

Use `web_fetch` on the most promising search results to get detailed data:
- Survival statistics (OS, PFS, ORR)
- Study phase and sample sizes
- Side effect profiles
- Biomarker requirements
- Where trials are recruiting

### Step 4: Build the Treatment Plan

Organize findings into a structured treatment plan. Use the **rating system** below
to score each approach.

### Step 5: Generate Output Document

Create a comprehensive Markdown document saved to `/mnt/user-data/outputs/`. Use the
output template in `references/output_template.md`.

The filename format: `cancer_research_[cancer_type]_[date].md`

Also generate a JSON data file for programmatic use:
`cancer_research_[cancer_type]_[date].json`

---

## Rating System

Each treatment approach gets a composite score from 1–10 based on:

| Factor | Weight | Description |
|---|---|---|
| Evidence Level | 30% | Phase 3 RCT = 10, Phase 2 = 7, Phase 1 = 4, Preclinical = 2, Case reports = 1 |
| Survival Benefit | 30% | Magnitude of OS/PFS improvement vs. SoC |
| Accessibility | 15% | FDA/EMA approved = 10, Phase 3 trial = 7, Phase 2 = 5, Phase 1 = 3, Preclinical = 1 |
| Safety Profile | 15% | Well-tolerated = 10, Manageable = 7, Significant toxicity = 4, Severe = 2 |
| Biomarker Match | 10% | Universal = 10, Common marker = 7, Rare marker = 4, Unknown = 5 |

**Composite Score** = (Evidence × 0.30) + (Survival × 0.30) + (Access × 0.15) + (Safety × 0.15) + (Biomarker × 0.10)

Round to one decimal place. Sort all approaches by composite score descending.

---

## Output Structure

Read `references/output_template.md` for the full template. The key sections are:

1. **Executive Summary** — Cancer type, key findings, top 3 recommended approaches
2. **Standard of Care Overview** — Current guidelines, expected outcomes
3. **Ranked Treatment Approaches** — Each approach with rating, evidence, and sources
4. **Clinical Trial Opportunities** — Active trials with enrollment info
5. **Emerging Research Pipeline** — Pre-approval promising approaches
6. **Combination Strategy Matrix** — Which treatments combine synergistically
7. **Supportive Care Evidence** — Adjunctive approaches with survival data
8. **Methodology & Sources** — How research was conducted, source list
9. **Disclaimer** — Medical disclaimer

---

## Important Guidelines

- Always present survival data in context (median OS, confidence intervals, comparison arms)
- Never overstate preclinical results — clearly label evidence tier
- Include negative results when relevant (failed trials inform the landscape)
- Note geographic availability of treatments and trials
- Flag biomarker requirements prominently — many targeted therapies only work for specific molecular subtypes
- When survival data conflicts between studies, present the range and note study quality
- Always note whether a treatment is curative-intent vs. life-extending
- Include quality-of-life considerations alongside survival data
- Present both optimistic and realistic scenarios

## File Management

After generating the report:
1. Save the Markdown report to `/mnt/user-data/outputs/`
2. Save the JSON data file to `/mnt/user-data/outputs/`
3. Present both files to the user
4. Offer to dive deeper into any specific treatment approach or find specific clinical trials
