# Clinical Content Standards

**Project:** OpenOnco
**Document:** Clinical Content Standards
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads
**Preceding document:** CHARTER.md

---

## Purpose of this document

This document defines **how clinical content is written, cited,
assessed, and reviewed** in the project knowledge base.

Without this document:
- The three clinician co-founders have no shared language for review
- No objective criteria exist for "good content" vs "bad content"
- Reproducible evidence assessment is impossible
- New contributors do not know how to propose changes

This document is the project's **editorial standard**. Analogues: NCCN Guidelines
Methodology, Cochrane Handbook, ESMO Living Guidelines Methodology.

---

## 1. Principles

### 1.1. Evidence-based by default

Every clinical claim in the knowledge base must be traceable to a
primary source. There is no "common knowledge" content without a citation.

### 1.2. Transparency over elegance

When sources contradict each other — **we surface the contradiction**, we
do not choose a "winner" by our own judgement. The clinician using
the system has the right to know about the discrepancy.

### 1.3. Date matters more than authority

A 2020 article from NEJM may be outdated by 2026. Recent evidence from
a smaller source may be more valid than an older one from a top-tier journal.
Source hierarchy does not replace temporal currency.

### 1.4. Explicit over implicit

What is not stated explicitly does not exist. "Drug X is commonly used
at dose Y" without a citation — is not counted.

### 1.5. Uncertainty is content, not a gap

"Evidence is insufficient to support a recommendation" — this is a complete
conclusion, not a failure. The system must be able to say "we don't know"
rather than make assumptions.

### 1.6. Local context matters

International guidelines (NCCN, ESMO) are the foundation, but not the
only truth. Ukrainian drug availability, Ministry of Health protocols, the
NHSU formulary — these are a mandatory layer for clinically useful
recommendations.

---

## 2. Source hierarchy

The hierarchy defines how much weight is assigned to different source types
when discrepancies arise.

### 2.1. Tier 1 — Consensus guidelines

Highest priority. Used as the basis for recommendations.

**International:**
- NCCN Guidelines (current version; specify version: v.X.YYYY)
- ESMO Clinical Practice Guidelines
- ASCO Clinical Practice Guidelines
- EHA Guidelines (hemato-oncology)
- BSH Guidelines (United Kingdom, hemato-oncology)
- EASL Guidelines (for HCV-related pathologies)
- CAP Guidelines (Pathology)

**Classification:**
- WHO Classification of Tumours 5th ed. (IARC Blue Books)
- AJCC Cancer Staging Manual 8th ed. (9th edition in preparation)
- ICD-O-3.2
- Lugano Classification (for lymphomas)

**Regulatory:**
- FDA drug labels (openFDA.gov)
- EMA EPARs
- Ministry of Health of Ukraine Orders — unified clinical oncology protocols
- State Formulary of Ukraine
- List of NHSU-reimbursed drugs

### 2.2. Tier 2 — High-quality primary evidence

Used when guidelines are outdated or do not cover the situation.

- Peer-reviewed RCT (Phase 3) in journals with IF ≥10:
  NEJM, Lancet, JAMA, Nature Medicine, Cell, JCO, Annals of Oncology,
  Blood, Lancet Oncology, Journal of Hematology & Oncology
- Cochrane Systematic Reviews
- Large meta-analyses (peer-reviewed, using PRISMA methodology)
- Registration trials for FDA/EMA approvals

### 2.3. Tier 3 — Primary evidence, lower strength

- Phase 2 RCT
- Phase 3 with limitations (small N, non-US/EU cohort, surrogate endpoints)
- Network meta-analyses
- Real-world evidence studies (Flatiron, SEER-based, registry data)
- Post-marketing surveillance studies

### 2.4. Tier 4 — Supporting evidence

May be cited, but not as the basis for strong recommendations.

- Phase 1-2 single-arm studies
- Retrospective cohort studies
- Conference abstracts (ASCO, ESMO, ASH) — marked as preliminary
- Expert opinion papers in peer-reviewed journals

### 2.5. Tier 5 — Molecular knowledge bases

A separate category for mutation-treatment associations.

- OncoKB — with evidence levels 1, 2, 3A, 3B, 4, R1, R2
- CIViC (community-curated)
- JAX Clinical Knowledgebase
- My Cancer Genome

These databases are **aggregators of primary evidence**. When using their
recommendations, we retain a reference to the database plus a reference to
the primary study they cite.

### 2.6. NOT accepted as sources

- Non-peer-reviewed preprints (medRxiv, bioRxiv) — except as an indicative
  signal to monitor; not as the basis for a recommendation
- Pharmaceutical company promotional materials
- Medical blogs, podcasts, news articles
- Articles from predatory journals (verified via Beall's List, DOAJ)
- ChatGPT/LLM-generated content without human verification
- Wikipedia

---

## 3. Structure of a clinical recommendation

Every recommendation in the knowledge base has a **mandatory structure**.

### 3.1. Required fields

```yaml
recommendation_id: REC-HCV-MZL-001
disease_entity: HCV-associated marginal zone lymphoma
clinical_scenario: >
  First-line therapy for HCV-positive MZL without red flags for
  transformation
recommendation: >
  DAA (sofosbuvir/velpatasvir) + BR (bendamustine/rituximab) as
  concurrent therapy, followed by R-maintenance for 2 years
evidence_level: Strong (see section 4)
strength_of_recommendation: Preferred (see section 4)
sources:
  - type: guideline
    id: NCCN-B-cell-Lymphomas-v2.2026
    page_or_section: MZL-3
    date_accessed: YYYY-MM-DD
  - type: guideline
    id: ESMO-MZL-2020
    url: https://www.annalsofoncology.org/...
  - type: primary_rct
    id: BArT-trial
    citation: Arcaini L et al., Blood 2014;124:2753-2760
    pmid: XXXXXXXX
  - type: primary_rct
    id: BRIGHT-study
    citation: Flinn IW et al., J Clin Oncol 2019
    pmid: XXXXXXXX
applicable_population:
  - HCV RNA-positive
  - MZL confirmed histologically
  - No red flags for high-grade transformation
contraindications_link: [CONTRA-AMIODARONE-SOFOSBUVIR, CONTRA-HBV-NO-PROPHYLAXIS]
last_reviewed: YYYY-MM-DD
last_reviewer_ids: [reviewer-id-1, reviewer-id-2]
notes: >
  Historical alternative (R-CHOP) is addressed in REC-HCV-MZL-002
  for patients with red flags for transformation
```

### 3.2. Prohibited phrasing

**Do not use without context:**
- "best", "optimal", "ideal" — subjective, not evidence
- "most patients" — without a specific % and source
- "proven effective" — must specify how (OS, PFS, ORR)
- "generally well tolerated" — must provide specific toxicity rates
- "current standard" — without a reference to a specific guideline + date

**Replace with:**
- "preferred per NCCN v.X.YYYY, category 1"
- "30% of patients achieve CR per BArT trial (Arcaini 2014)"
- "median OS extension of 3.2 months (HR 0.78, 95% CI 0.65-0.94) per trial X"
- "grade 3-4 neutropenia in 18% per registration trial"

### 3.3. Language neutrality

Recommendations are written **factually**, without a promotional tone. Compare:

**Bad:** "Pembrolizumab — a revolutionary breakthrough in the treatment of NSCLC"
**Good:** "Pembrolizumab + chemotherapy improved OS compared with
chemotherapy (HR 0.56, 95% CI 0.45-0.70) in KEYNOTE-189 (Gandhi 2018)"

---

## 4. Evidence assessment

We **do not create our own scale** — we use established ones.

### 4.1. Evidence Level

We use the adapted **GRADE** (Grading of Recommendations Assessment,
Development and Evaluation) — an international standard used by Cochrane,
WHO, and NICE.

| Level | Meaning | Typical sources |
|---|---|---|
| **High** | Further research is unlikely to change the estimate of effect | Multiple RCTs with consistent results + meta-analysis |
| **Moderate** | Further research may substantially affect the estimate | Single RCT or RCTs with limitations |
| **Low** | Further research is likely to change the estimate | Observational studies, small RCTs |
| **Very low** | The estimate is very uncertain | Case series, expert opinion |

### 4.2. Strength of Recommendation

Separate from evidence level. A recommendation may have Moderate evidence
but Strong strength (if the clinical effect is large and there are no
alternatives).

| Level | Meaning |
|---|---|
| **Preferred / Strong** | Benefit clearly outweighs harm; usually recommend |
| **Alternative / Conditional** | Balance of benefit and harm is closer; individualize |
| **Not recommended** | Evidence against use, OR harm ≥ benefit |
| **Insufficient evidence** | Cannot determine benefit-harm balance |

### 4.3. NCCN Categories as cross-reference

For compatibility with US clinical practice, we also indicate the NCCN
category when a recommendation is drawn from NCCN:

- **Category 1:** High-level evidence + uniform NCCN consensus
- **Category 2A:** Lower-level evidence + uniform NCCN consensus
- **Category 2B:** Lower-level evidence + non-uniform NCCN consensus
- **Category 3:** Major NCCN disagreement

### 4.4. Molecular/Biomarker evidence — OncoKB levels

For recommendations based on molecular markers:

- **Level 1:** FDA-approved biomarker for the specific tumor type
- **Level 2:** Standard of care biomarker in guidelines for the specific tumor type
- **Level 3A:** Clinical evidence in same indication (early phase)
- **Level 3B:** Clinical evidence in different indication
- **Level 4:** Preclinical evidence
- **Level R1:** Standard care resistance
- **Level R2:** Investigational resistance

### 4.5. What we do NOT do

- We do not create custom 1-10 rating scales
- We do not aggregate evidence into a composite score
- We do not rank recommendations by a single number
- We do not automate evidence evaluation via LLM

Ranking by a single composite score is the path IBM Watson took — one that
conceals the real structure of evidence. We present recommendations with
a full breakdown; the clinician decides.

---

## 5. Source citation

### 5.1. Minimum information for a citation

Every source in the knowledge base is stored with:

```yaml
source_id: "NCCN-B-Cell-Lymphomas-v2.2026"  # unique identifier
type: guideline | phase3_rct | meta_analysis | regulatory | molecular_kb | other
title: "NCCN Guidelines for B-Cell Lymphomas"
version_or_edition: "v.2.2026"  # for guidelines
authors: ["Zelenetz AD", "..."]  # for RCT/meta-analyses
journal: "Blood"  # for articles
year: 2026
pmid: "XXXXXXXX"  # if available
doi: "10.XXXX/..."  # if available
url: "https://..."
date_accessed: "2026-04-15"  # when last reviewed for entry
access_notes: "Subscription required via institutional access"  # if behind paywall
```

### 5.2. Traceability requirement

Every clinical claim in the knowledge base must be "one click" away from
its citation. In practice this means:

- The UI display of a recommendation always shows the list of sources
- Click on a source → opens the source record with full metadata
- Click on a PMID → opens PubMed entry (external)
- Click on a DOI → opens publisher page (external)

### 5.3. When a guideline and an RCT diverge

For example, NCCN recommends X, but a recent RCT (published after the last
guideline update) shows that Y is superior.

**Approach:**
1. Record both
2. Display both with dates: "NCCN v.1.2025 recommends X (date: Jan 2025);
   RCT [name] published Mar 2025 showed Y superior"
3. Do not conceal the contradiction; do not choose by default
4. The Clinical Co-Lead committee discusses how to formulate the recommendation
   taking both perspectives into account

### 5.4. Managing outdated sources

Guidelines are updated (NCCN — several times per year). The system requires
discipline:

- Source records have the field `currency_status`: current | superseded | historical
- A superseded source remains in the database with a pointer to its replacement
- A recommendation referencing a superseded source is automatically flagged
  `needs_review` during the quarterly audit

---

## 6. Internal review process

### 6.1. Before submitting for review

The contributor verifies:

- [ ] All recommendation fields are filled in
- [ ] At least 2 independent Tier 1 or 2 sources
- [ ] Contradictions are listed and linked
- [ ] Evidence level assessed with GRADE rationale
- [ ] Strength of recommendation selected with rationale
- [ ] Formatting and language neutrality checked
- [ ] No prohibited phrasing from section 3.2
- [ ] The `applicable_population` field is clearly defined
- [ ] The `last_reviewed` date is current

### 6.2. Clinical review checklist

Each of the two independent reviewers goes through:

**Source accuracy:**
- [ ] Citations exist and are accessible
- [ ] Description of data from the source matches the actual content of the source
- [ ] The most recent relevant guidelines are cited
- [ ] Conflicts with other sources are documented

**Clinical accuracy:**
- [ ] Recommendation aligns with current standard of care
- [ ] Evidence level assessed correctly per GRADE
- [ ] `applicable_population` is precise, without over/under-inclusion
- [ ] Nothing important is omitted (alternatives, contraindications)

**Consistency:**
- [ ] Does not contradict existing recommendations in the database (or explicitly
      diverges with a documented rationale)
- [ ] Terminology is consistent with existing content
- [ ] Phrasing is not promotional

**Safety:**
- [ ] All hard contraindications are listed
- [ ] Warnings (especially FDA black box warnings) are listed
- [ ] Interactions with common concomitant medications are checked

### 6.3. Dual review resolution

- Both reviewers agree → merge
- Reviewer A agrees; Reviewer B has questions that the requestor has corrected
  → merge after acknowledgment from B
- Reviewers fundamentally disagree → escalate to a third reviewer or
  to full Clinical Editorial Board discussion
- Controversy is not resolved → **document both positions** with an explicit
  notation and let the clinician-user decide

### 6.4. Emergency content updates

For critical updates (drug recall, safety alert, new black box warning):

- One Clinical Co-Lead + one external expert may approve an
  emergency change
- The change is published with the label `emergency_update`
- Full dual review within 7 days post-publication
- Retroactive audit within 30 days

---

## 7. Language policy

### 7.1. Internal language of the knowledge base — English

The knowledge base is stored in English for:
- Compatibility with international terminologies (SNOMED CT, ICD-O, LOINC)
- Citation of English-language sources without translation noise
- International collaboration potential

### 7.2. Output — multilingual

The system generates documents in Ukrainian (primary) and English
(for reference). Translation:

- Clinical terminology — we use official Ukrainian equivalents from
  ICD-10/11, Ministry of Health orders, Ukrainian medical dictionaries
- Drug names — per the State Formulary of Ukraine
- Study names — we keep original English names (KEYNOTE-522,
  BArT, BRIGHT, etc.); we do not transliterate
- Dosage units — metric, SI-compliant (mg/m², mg/kg)

### 7.3. Consistency via glossary

A `GLOSSARY.md` is maintained with agreed translation pairs for clinical
terms. This is part of the project, public and editable via the standard
review process.

---

## 8. Conflict of interest (CoI) disclosure

All clinical content contributors declare CoI before their first
accepted PR. Declaration is public on the project website.

### 8.1. Types of CoI requiring declaration

- Consulting for pharmaceutical companies (with a list of companies)
- Speaking fees, honoraria
- Research grants (institutional and personal)
- Advisory board membership
- Equity / stock ownership in medical ventures
- Intellectual property / patents
- Family members with industry ties

### 8.2. Recusal rules

A contributor with a declared CoI **cannot be the primary author** for
recommendations concerning products of companies with which they have
a relationship. They may act as a reviewer if:

- The CoI is explicitly declared in review comments
- The second reviewer has no CoI with the same product
- Escalation to a Clinical Co-Lead for final approval

### 8.3. Public CoI page

The project website includes a public page:

```
Clinical Content Contributors — CoI Declarations

[Reviewer Name], [Credentials], [Institution]
  Last updated: YYYY-MM-DD
  Industry relationships:
    - [Company X]: Speaking honoraria 2024-2025
    - [Company Y]: Advisory board 2023
  Research grants:
    - [NIH/European grant]: ongoing
  No ownership in medical companies
```

---

## 9. Knowledge base hygiene

### 9.1. Periodic review

Once per quarter, each domain reviewer covers their area and checks:

- Whether new major guidelines have appeared (NCCN updates, ESMO updates)
- Whether practice-changing RCTs have appeared (plenary abstracts ASCO/ESMO/ASH)
- Whether any FDA safety alerts / drug withdrawals have occurred
- Whether recommendations with `last_reviewed` > 6 months ago are still valid

The output is a quarterly report, public, describing the changes.

### 9.2. Annual full audit

Once per year — a full audit of all recommendations in the domain, not only
recently changed ones. A random sample (20% of recommendations) is checked
for coherence.

### 9.3. Deprecation

Outdated recommendations are not deleted immediately:

- Flag `deprecated` with `deprecated_reason` and `replacement_id`
- Deprecation period — 6 months with warning
- Archive retained indefinitely for retrospective audits

---

## 10. Example application (mini case)

To illustrate how the Standards work in practice — a brief demonstration
using the HCV-MZL context (a real example will appear in the Reference Case doc).

**Scenario:** adding a new recommendation "DAA + BR for HCV-MZL 1L"

**Contributor Q:**
```yaml
recommendation_id: REC-HCV-MZL-001
disease_entity: HCV-associated marginal zone lymphoma
clinical_scenario: First-line therapy, no red flags for transformation
recommendation: >
  Concurrent DAA (sofosbuvir/velpatasvir) + BR (bendamustine/rituximab)
  × 6 cycles, followed by rituximab maintenance 375 mg/m² q8w × 12 doses
evidence_level: Moderate (GRADE)
strength_of_recommendation: Preferred
sources:
  - {type: guideline, id: "NCCN-B-Cell-Lymphomas-v2.2026", section: "MZL-3"}
  - {type: guideline, id: "ESMO-MZL-2020-guidelines"}
  - {type: guideline, id: "EASL-HCV-2023"}
  - {type: phase2_trial, id: "BArT", citation: "Arcaini L, Blood 2014", pmid: "..."}
  - {type: phase3_rct, id: "BRIGHT", citation: "Flinn IW, JCO 2019", pmid: "..."}
...
```

**Reviewer A (hemato-oncologist):** Verifies clinical accuracy, dose,
regimen — OK. Notes: "Slight correction — bendamustine dose reduction
to 70 mg/m² when FIB-4 > 3.25 must be explicit, not only in notes."

**Reviewer B (hepatologist):** Verifies the HCV-related section. Notes:
"Prohibited combination sofosbuvir + amiodarone — a separate
CONTRA entry and a link from the recommendation are required." Creates the
CONTRA-AMIODARONE-SOFOSBUVIR entry.

**Contributor Q** incorporates corrections → reviewers approve → merge.

Changelog:
```
2026-04-XX  REC-HCV-MZL-001 created
  Contributor: [id-Q]
  Reviewers: [id-A], [id-B]
  Sources: 5 (2 guidelines, 3 trials)
  Evidence level: Moderate
  Related entries: CONTRA-AMIODARONE-SOFOSBUVIR (new),
                   REC-HCV-MZL-002 (alternative aggressive path, existing)
```

---

## 11. Governance of this document

- Changes to the Clinical Content Standards require consensus of all Clinical
  Co-Leads + 14 days of public comment
- Document reviewed annually or as needed
- Changelog maintained in CHANGELOG-CCS.md

---

## 12. Current status and limitations

**v0.1 means:**
- Skeleton for initial discussion with Clinical Co-Leads
- Requires calibration for the Ukrainian clinical context
- Requires alpha-testing on the first real recommendation

**Still unresolved:**
- Exact YAML/JSON format for storing recommendations (Schema doc)
- Tools for automated source validation
- Integration with reference management (Zotero? local bibliography?)
- GLOSSARY translation for the initial nosologies

**First test:** applying the Standards to the HCV-MZL reference case —
can we reproduce a real verified document through a disciplined clinical
process following these standards?

---

**Proposals, criticism, pull requests — welcome via the standard
governance process (CHARTER.md §6).**
