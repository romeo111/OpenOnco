# Source Ingestion & Licensing Specification

**Project:** OpenOnco
**Document:** Source Ingestion & Licensing — Hosting Matrix
**Version:** v0.1 (draft, Part A — licensing and hosting matrix)
**Status:** Draft for discussion with Clinical Co-Leads and legal counsel
**Prerequisite documents:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md, KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md
**Planned subsequent parts:**
- Part B — Per-source ingestion playbook (how exactly to pull each source)
- Part C — Conflict & precedence rules (what the engine does when sources disagree)
- Part D — Freshness TTL & re-ingestion cadence

---

## Purpose of this document

CHARTER §2 declares OpenOnco as a **free public information resource**.
KNOWLEDGE_SCHEMA_SPECIFICATION §5 (Source entity) envisages aggregation
from many sources — from NCCN and ESMO to OncoKB and the Ministry of Health.

These two requirements automatically conflict: **not all sources can be hosted**.
NCCN Guidelines are protected by copyright, SNOMED CT requires a license,
OncoKB has different terms for academic and commercial use, and so on.

Without a clear licensing and hosting matrix we either:
- (a) risk a cease & desist from NCCN / Elsevier / SNOMED International
- (b) build a scheme that **cannot** contain what a physician actually needs
  (the recommendation text, not just a reference)
- (c) pay for licenses we did not plan for

This document fixes the **hosting mode for each source** and the resulting
requirements for the `Source` entity.

**Core principle (§1.4):** `referenced` by default — we **do not mirror**
external databases. `hosted` only when there is an explicit justification
(no API, performance-critical matching, audit snapshot, our own content).
This keeps the knowledge base compact, legally safe by default, and guarantees
that the user always sees fresh data from the source.

---

## 1. Hosting modes (three modes)

Each source in the OpenOnco knowledge base has one of three modes:

### 1.1. `hosted` (full hosting)

We download, normalise, and store the full content. Content is displayed
in the UI without redirecting to an external source. We maintain versioning,
`last_verified`, and re-ingestion on a schedule.

**Permitted for:** ClinicalTrials.gov, OpenFDA / DailyMed, CIViC, PubMed
abstracts (with caveat — see §2.4), Ministry of Health / NHSU protocols,
LOINC, ICD-10-CM, FDA drug labels, EMA EPARs (with attribution).

**UI/output requirements:**
- Source attribution (logo or text "via [source]")
- Link to the original with every use
- If the license requires — ShareAlike: our output inherits the same license
- For CC-BY: author credit must be preserved

### 1.2. `referenced` (reference + metadata only)

We store **metadata** for the source (title, version, authors, date, URL,
DOI/PMID) and a **brief human paraphrase** (not a quotation) written by our
clinicians in their own words. We do NOT store the original recommendation
text, tables, or images from the source.

**Permitted for:** NCCN Guidelines, WHO Classification of Tumours, AJCC
Cancer Staging Manual, ESMO Pocket Guidelines (mostly), ASCO Guidelines,
Cochrane full-text reviews, OMIM, MedDRA (if without a license).

**UI/output requirements:**
- `Indication.rationale` may contain **our** paraphrase with attribution:
  _"Per NCCN B-Cell Lymphomas Guideline v.2.2025 (paraphrased): for
  HCV-associated MZL, antiviral therapy is preferred first-line"_
- Never copy-paste from the source
- Always a clickable link to the source
- Fair use for **very short** quotations (< 1 sentence, with quotation marks
  and attribution) is acceptable in individual cases, but not by default

### 1.3. `mixed` (structure yes, prose no)

For sources that openly publish structured data (mutation-drug mappings,
trial records, taxonomies) but protect narrative text with copyright.

**Permitted for:** EMA EPARs (tables OK, PDF body — attribution),
FDA Structured Product Labels (sections yes, full narrative with attribution),
ESMO (structured therapy tables by agreement).
(OncoKB was once cited as a `mixed` example — but its ToS blocks the
OpenOnco use case, see §2.5 and §16.4.)

**Requirements:**
- Structured fields (gene, variant, drug, evidence level) are hosted
- Prose summary / discussion — our paraphrase with a link
- Mode and license are fixed at the **source level**, not per-fact

### 1.4. ⭐ Principle: `referenced` by default

**If a source can be referenced — we reference it. We do not mirror
external databases.** This is a founding principle for OpenOnco.

Reasons:
- **Cost & maintenance:** mirroring CT.gov (500K+ records), PubMed
  (38M abstracts), DailyMed — is infrastructure we don't need to maintain,
  and a mirror always lags behind the source
- **Freshness:** a live API call sees today's update, a snapshot does not
- **Legal safety:** `referenced` automatically eliminates most copyright
  concerns — safe by default
- **User trust:** the user sees the original source with full context,
  not our extract with a possible interpretation

`hosted` requires **explicit justification** by at least one criterion:

| # | Criterion | Typical examples |
|---|---|---|
| **H1** | No API / public endpoint | Ministry of Health protocols, NHSU formulary, State Drug Registry, PDF-only guidelines |
| **H2** | Performance-critical for rule matching | Code systems (ICD, LOINC, RxNorm, ATC) — the rule engine calls them on every request |
| **H3** | Immutable audit snapshot required | Version/date stamp of the source the physician saw when making the decision (metadata snapshot only, not full content) |
| **H4** | Project's own content | Our Indications, Regimens, Contraindications, Algorithms, RedFlags |
| **H5** | Small, stable, and critical to logic | CTCAE v5.0 (toxicity grading), HGNC gene symbols, ICD-O-3 |

If none of H1-H5 applies — `referenced`. Crucially: the rule engine
contacts external APIs (CT.gov, PubMed, DailyMed, openFDA) via our
existing clients (`clinicaltrials_client.py`, `pubmed_client.py`) during
evaluation — it does not read from a local mirror.

**Where we do cache without hosting:** the Source entity always contains
a metadata snapshot (title, version, URL, DOI, last_verified date) — this
is not content hosting, it is a citation. `referenced` ≠ "we store nothing";
it means "we store the citation, not the content".

---

## 2. Licensing and hosting matrix

The matrix is split into 7 tiers by functional role in the knowledge base.
Priority for OpenOnco: **Tier 3 (Ukraine-local)** is more important than
Tier 1 for actually generating plans — without it, we cannot determine what
is available to the patient.

### 2.1. Tier 1 — Core primary clinical sources

| Source | License | Mode | What can be stored | Commercial use | Hot spots |
|---|---|---|---|---|---|
| **NCCN Guidelines** | © NCCN, free personal use with registration, **no redistribution** | `referenced` | URL, version, date, our paraphrase | ❌ license required | Active enforcement activity. Do not host tables or text. [licensing info](https://www.nccn.org/guidelines/nccn-guidelines) |
| **ESMO Clinical Practice Guidelines** | Typically CC-BY-NC-ND 4.0 (recent years, in _Annals of Oncology_) | `mixed` | Structured therapy recommendations + paraphrase + full citation | NC only — **our "free resource" ≈ non-commercial, but verify** | NC-ND: building a rule engine on top of parsed guidelines may be "derivative" — clarify with legal |
| **ASCO Guidelines** | © ASCO, published in JCO, free to read, redistribution restricted | `referenced` | Metadata + paraphrase | ❌ | [ASCO reprint policy](https://ascopubs.org/action/clickThrough?id=7009&url=%2Fpermissions) |
| **WHO Classification of Tumours (5th ed.)** | © WHO/IARC, proprietary | `referenced` | ICD-O-3 codes (public), classification naming — paraphrase | ❌ for content | IARC actively licenses |
| **AJCC Cancer Staging Manual** | © American Cancer Society / Springer | `referenced` | Stage names (paraphrase) + link | ❌ | Commercial use of stage tables is prohibited |
| **Cochrane Systematic Reviews** | Typically subscription; access in Ukraine via Cochrane Collaboration | `referenced` | Abstract summary (brief paraphrase) + DOI | ❌ | Full text paywalled; abstracts can be stored |

**Practical conclusion for Tier 1:** OpenOnco **does not host content** from Tier 1.
For each Indication the clinical reviewer writes their own `rationale` and
references the source. This is the primary clinical layer that requires manual work.

### 2.2. Tier 2 — Regulatory (FDA, EMA, DailyMed)

| Source | License | Mode | What can be stored | Hot spots |
|---|---|---|---|---|
| **FDA drug labels** (DailyMed / openFDA) | US government work, public domain | `referenced` | Metadata + DailyMed ID; live API call during rule evaluation | [openFDA API](https://open.fda.gov/) |
| **FDA Orange Book / Purple Book** | US gov, public domain | `referenced` | Metadata + link | — |
| **EMA EPARs** (European Public Assessment Reports) | © EMA, reuse with attribution, non-commercial | `referenced` | Metadata + EPAR number + URL | — |
| **Health Canada Drug Product Database** | Crown copyright, open license | `referenced` | Metadata + DIN | — |
| **UK MHRA** | Crown copyright, OGL (Open Government Licence) | `referenced` | Metadata | — |
| **Australian TGA** | Crown copyright, CC-BY 4.0 for most | `referenced` | Metadata | — |

**Practical conclusion for Tier 2:** **Reference via live API**, do not
mirror. openFDA / DailyMed APIs are called during rule evaluation via a
client (need to add `dailymed_client.py` similar to the existing `pubmed_client.py`).

**Exception to consider (escalation to `mixed`):** if rule engine latency
for Drug.contraindication lookup via openFDA becomes a problem — cache only
those structured fields (contraindications, AE lists) actually needed for
matching, per criterion H2 (§1.4). Start with pure `referenced`, switch to
`mixed` based on production latency data.

### 2.3. Tier 3 — Ukraine-local (Tier 1 priority for the project)

| Source | License | Mode | What can be stored | Hot spots |
|---|---|---|---|---|
| **Ministry of Health Unified Clinical Protocols** | Public (government document) | `hosted` | Full protocol text | No API, scraper needed from [moz.gov.ua](https://moz.gov.ua/) |
| **NHSU formulary (reimbursed drugs)** | Public | `hosted` | Full list + conditions | [nszu.gov.ua](https://nszu.gov.ua/) — PDF/Excel format, updates ~monthly |
| **State Drug Formulary** | Public | `hosted` | Full | [dec.gov.ua](https://www.dec.gov.ua/) — annual updates |
| **State Drug Registry (SEC of the Ministry of Health)** | Public | `hosted` | Registration data, INN, manufacturer | [State Drug Registry](https://www.drlz.com.ua/) |

**Practical conclusion for Tier 3:** **We host everything.** This is what
makes OpenOnco genuinely useful for Ukraine (as opposed to "yet another NCCN
copy"). **BUT**: none of these sources has a modern API. All require
PDF/HTML scraping or manual data entry. This is the primary engineering
work of Tier 3.

### 2.4. Tier 4 — Clinical trials + literature

| Source | License | Mode | What can be stored | Hot spots |
|---|---|---|---|---|
| **ClinicalTrials.gov** | US NLM, public domain | `referenced` | Metadata snapshot (NCT ID, title, date accessed) for audit. Live query via `clinicaltrials_client.py` during evaluation | [API v2](https://clinicaltrials.gov/data-api/api). Not mirrored — 500K+ records change daily |
| **EU Clinical Trials Register (EUCTR)** | © EMA, reuse with attribution | `referenced` | Metadata + EudraCT number + link | No friendly API, live query via scraping only on demand |
| **PubMed / MEDLINE metadata** | NLM, mostly public domain | `referenced` | PMID + metadata snapshot. Abstracts fetched live via `pubmed_client.py` | Live E-utilities queries; per-journal copyright concerns don't apply as we don't host |
| **PubMed Central OA Subset** | CC-BY, CC-BY-NC, per-article | `referenced` | PMCID + metadata | Full-text live fetch per query; no mirror |
| **PubMed full text (non-OA)** | Publisher-copyright | `referenced` | PMID + metadata + link | Never host |
| **Cochrane Library** | Subscription + Cochrane terms | `referenced` | Abstract summary (brief paraphrase) + DOI | See Tier 1 |
| **bioRxiv / medRxiv** | CC-BY 4.0 (mostly) | `referenced` | Metadata + DOI; live fetch on demand | Status "preprint, not peer-reviewed" — clinical UI requirement |

**Practical conclusion for Tier 4:** **Everything is referenced.** Clients
`clinicaltrials_client.py` and `pubmed_client.py` already exist in the
repository and are used by the rule engine live, not for batch ingestion.
This greatly simplifies infrastructure: no ETL pipeline, no cron, no SQLite
mirror for 500K trials and 38M abstracts.

**What we store locally:** only `Source` entity metadata snapshots
(NCT-ID, PMID, title, version/date at the time of citation). This is a
citation record for the audit — "this recommendation referenced NCT05123456
as of 2026-04-24" — not a copy of the data.

**Risk:** dependency on the uptime and rate limits of external APIs.
CT.gov / NLM have occasional downtime. For a clinical tool this must be
mitigated: graceful degradation + local cache with TTL (hours-to-day),
not a mirror.

### 2.5. Tier 5 — Molecular / biomarker KBs

| Source | License | Mode | What can be stored | Hot spots |
|---|---|---|---|---|
| **CIViC** ⭐ **PRIMARY actionability source** | CC0-1.0 (no constraints) | `hosted` (H2 + H5) | Full variant-evidence records locally | Small (~5K accepted evidence items, ~1.9K (gene, variant) pairs as of 2026-04-25), performance-critical for biomarker→indication matching, CC0 removes all legal constraints. **This is the primary biomarker-actionability source in v0.1.** |
| **OncoKB** ❌ **REJECTED 2026-04-27** | Academic license; redistribution forbidden; "use for patient services" + AI training prohibited | (not used) | (not used) | Initially planned as the primary actionability source. Audit [`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`](../docs/reviews/oncokb-public-civic-coverage-2026-04-27.md) showed that OncoKB Terms of Use explicitly prohibit the OpenOnco use case. Replaced by CIViC. Engine modules named vendor-neutral (`actionability_*`) so a future pivot to another source remains possible. |
| **JAX Clinical Knowledgebase (CKB)** | Free academic, commercial paid | `referenced` | Metadata | Similar to OncoKB — license terms require a fresh audit before use. Not integrated as of 2026-04. |
| **MyCancerGenome** | Variable per entry | `referenced` | Metadata | Verify per entry |
| **COSMIC** | Academic free registration; commercial paid | `referenced` | Metadata + query link | Sanger actively separating tiers after 2024 |
| **ClinVar** | Public domain (NCBI) | `referenced` | Metadata + variant ID; live API query | — |
| **gnomAD** | Public | `referenced` | Live API query for population frequencies | — |

**Practical conclusion for Tier 5:** **CIViC is the only hosted and only
primary** source in this tier. Justification: H2 (rule engine needs fast
lookup variant → evidence on every patient evaluation) + H5 (small, stable,
CC0 with no constraints).

**CIViC implementation status (2026-04-27):**
- Snapshot hosted at `knowledge_base/hosted/civic/<YYYY-MM-DD>/evidence.yaml`
  (loader: `knowledge_base/ingestion/civic_loader.py`).
- Monthly refresh CI workflow: `.github/workflows/civic-monthly-refresh.yml` —
  fetch + diff + PR.
- Fusion-aware variant matching (CIViC-specific `BCR::ABL1` notation with
  inline kinase-domain mutations like `Fusion AND ABL1 T315I`):
  `knowledge_base/engine/civic_variant_matcher.py`.
- Snapshot client (read-only over hosted YAML, not live API):
  `knowledge_base/engine/snapshot_civic_client.py`.

**OncoKB rejection — details.** The audit identified **three independent
grounds** for rejection:
1. OncoKB Terms of Use prohibit redistribution (academic users
   "may not redistribute or share the Content with any third party").
2. Directly forbidden use case: "**use for patient services**" and
   "**generation of reports in a hospital or other patient care setting**" —
   which is the definition of OpenOnco's scope (CHARTER §2: free public
   resource that produces patient treatment plans).
3. AI training "strictly prohibited", which forecloses future evolution.

`oncokb-datahub` (gene-level subset on GitHub) has no separate LICENSE —
it inherits OncoKB Terms by reference. **We do not mirror it, we do not
vendor it.** If any remaining mentions of OncoKB as a planned source appear
in spec text — that is historical context; no new integration is to begin.

Everything else in Tier 5 — referenced via API.

### 2.6. Tier 6 — Terminologies / code systems

| Source | License | Mode | What can be stored | Hot spots |
|---|---|---|---|---|
| **ICD-10-CM** (US) | Public domain (CDC/CMS) | `hosted` | Full | OK |
| **ICD-10** (WHO) | WHO — free use with restrictions | `hosted` with attribution | Full | Modifications require WHO permission |
| **ICD-O-3.2** | WHO — free academic/clinical | `hosted` with attribution | Full | Commercial OK for authorized users |
| **SNOMED CT** | SNOMED International, per-country license | ⚠️ **LICENSE REQUIRED** | Nothing without a license | Ukraine is not a member country at time of writing. Alternative: LOINC + ICD + own code system |
| **LOINC** | Regenstrief, LOINC License (attribution required, no modifications without permission) | `hosted` with attribution | Full | OK. [LOINC License](https://loinc.org/license/) |
| **RxNorm** | NLM / UMLS, permissive | `hosted` with attribution | Full | UMLS Terminology Services license required, but free |
| **ATC / DDD** (WHO Collaborating Centre) | Free for academic/personal; commercial licensed | `hosted` with attribution | Full | [ATC/DDD policy](https://www.whocc.no/copyright_disclaimer/) — commercial redistribution requires a license |
| **HGNC (HUGO gene symbols)** | Free, CC-BY 4.0 | `hosted` | Full | OK |
| **MedDRA** | MSSO, license required | ⚠️ **LICENSE REQUIRED** | Nothing without a license | For non-profit — fixed annual fee. [MedDRA licensing](https://www.meddra.org/subscription) |
| **HGVS nomenclature** | Free, HGVS Society | `hosted` | Full syntax | OK |
| **UCUM (units of measure)** | Regenstrief, free | `hosted` | Full | OK |

**Practical conclusion for Tier 6:** This is the **primary exception** to
the "referenced by default" principle (§1.4). Code systems are hosted under
criteria **H2** (the rule engine calls code lookups on every patient match —
ICD → Disease, LOINC → Test, RxNorm → Drug — API-call latency per query is
unmanageable) and **H5** (small, stable, critical to logic).

- **SNOMED CT — not used in MVP.** Without a country license we have no
  right. For lab results + clinical concepts we use
  **LOINC + ICD + RxNorm + a lightweight own taxonomy** for clinical
  concepts not covered by these three.
- **MedDRA — not used in MVP.** AEs are described with free text +
  CTCAE v5.0 grading (public domain, NCI).
- **ATC — hosted with caution.** For non-commercial OpenOnco this is OK;
  if the project becomes commercial — obtain a license. Fallback: RxNorm.

### 2.7. Tier 7 — Research datasets (validation, not knowledge)

These sources **are not** part of the knowledge base as authorities for
recommendations. They are used for validation (does the engine give sensible
answers on real cohorts?) and epidemiological context.

| Source | License | Mode | Use |
|---|---|---|---|
| **TCGA (public tier)** | NIH, public | `referenced` (dataset) | Validation cohort |
| **AACR Project GENIE** | CC-BY 4.0 (registered users) | `referenced` | Validation cohort |
| **cBioPortal** | Variable per dataset | `referenced` | Query interface |
| **MMRF CoMMpass** | Controlled access | `referenced` | Validation (myeloma) |
| **SEER** | Public summaries; patient-level — application required | `referenced` | Epidemiological context |
| **DepMap** | Broad, free for research | `referenced` | Drug response validation |
| **MIMIC-IV** | PhysioNet credentialed access | `referenced` | NLP/EHR context |

**Practical conclusion for Tier 7:** These do not affect the `Source` entity
in the knowledge base. They are **testing artifacts**, not recommendation sources.
A separate part of the document (Part E — Validation Datasets) will describe
access and use cases for each.

---

## 3. Required additions to the `Source` entity

KNOWLEDGE_SCHEMA_SPECIFICATION §5 (Source) describes title, version, authors,
journal, DOI, PMID, URL, access_level, currency_status, evidence_tier.
This is insufficient for license-aware aggregation. Add:

```yaml
Source:
  id: "SRC-CTGOV-REGISTRY"           # abstraction for the registry, not per-trial
  source_type: "clinical_trials_registry"
  # ... existing fields from KNOWLEDGE_SCHEMA_SPECIFICATION §5 ...

  # NEW — licensing & hosting fields
  hosting_mode: "referenced"         # hosted | referenced | mixed
  hosting_justification: null        # H1..H5 if hosted, otherwise null
  ingestion:
    method: "live_api"               # live_api | scheduled_batch | manual | none
    client: "clinicaltrials_client.py"   # module making the request
    endpoint: "https://clinicaltrials.gov/api/v2"
    rate_limit: "50 req/min per IP"  # from the source's documentation
  cache_policy:
    enabled: true                    # for referenced — query-level cache
    ttl_hours: 24                    # for CT.gov; for code systems N/A (hosted)
    scope: "query_result"            # query_result | entity_snapshot | none
  license:
    name: "US public domain"
    url: "https://clinicaltrials.gov/about-site/terms-conditions"
    spdx_id: null                    # SPDX if applicable (e.g. "CC-BY-4.0", "CC0-1.0")
  attribution:
    required: false
    text: "Data from ClinicalTrials.gov, National Library of Medicine"
    logo_url: null
  commercial_use_allowed: true
  redistribution_allowed: true
  modifications_allowed: true
  sharealike_required: false
  known_restrictions: []
  legal_review:
    status: "reviewed"               # pending | reviewed | escalated
    reviewer: "[name/org]"
    date: "2026-05-01"
    notes: "Verified public domain; referenced mode avoids redistribution concerns"
```

`hosting_mode` — primary switch. The rule engine and UI must behave
differently for `hosted` and `referenced` sources:
- `hosted` — cite content directly, maintain `last_verified`,
  re-ingest on schedule
- `referenced` — show only metadata + clickable link + our paraphrase
  from `Indication.rationale`. Never display an archived original

---

## 4. Grey areas and edge cases

### 4.1. Fair use for educational quotations

Under US law and certain European laws, a short quotation (1-2 sentences)
with attribution is permissible for educational/critical purposes.
Ukrainian law contains a similar concept of "lawful reproduction"
(Article 21 of the Law of Ukraine "On Copyright and Related Rights").

**OpenOnco policy:** fair use is **not the basis** of our architecture.
We do not rely on fair use for routine operation. If a very short quotation
from NCCN (<20 words) in quotation marks with attribution is needed in a
rationale for a specific clinical point — this is acceptable, but requires
clinical co-lead review. Do not automate.

### 4.2. PubMed abstracts: public or publisher?

NLM technically distributes abstracts as part of MEDLINE. However, NLM
Data Distribution terms warn: "Some abstracts may be copyrighted by
the publisher." For personal research this is fine; for a public API
on top — a grey area.

**OpenOnco policy:** we **do not host** PubMed abstracts. We query them
live via E-utilities (`pubmed_client.py`) during rule evaluation. We store
only the PMID + metadata snapshot (title, date, journal) as a citation record.
This automatically removes the copyright concern (we do not distribute
content) and provides an always-fresh version of the abstract.

### 4.3. "Free public resource" = commercial use?

This is the **key question** for several licenses (ESMO CC-BY-NC-ND, ATC).
("OncoKB" was previously on this list, but after the 2026-04-27 audit it
was rejected unconditionally — see §2.5 / §16.4: OncoKB ToS blocks the
OpenOnco use case regardless of commercial status.) "Non-commercial" typically
means no profit motive. OpenOnco:
- Open source, free access, no paid tiers → non-commercial
- If an enterprise tier, paid API, or hospital deployment licenses appear
  in the future — **it becomes commercial**

**OpenOnco policy:** as long as we are a **100% non-profit-motive public resource**
— we are non-commercial. `CHARTER.md §2` must establish this as a fixed constraint:
changing to a commercial model triggers a license audit of all `referenced` and
`mixed` sources.

### 4.4. Screenshots / rendered content from NCCN

Absolutely not. A screenshot of an NCCN flowchart is copying their compiled
intellectual property, even without text. Never host as image, SVG, or
reimplementation.

### 4.5. ShareAlike: what does our output constitute

If we integrate a CC-BY-SA source, our derivative output inherits SA.
CC0 and CC-BY do not propagate. Most of our sources are public domain,
CC-BY, or proprietary. **SA sources are not currently planned** — if they
appear, they must be separately recorded in `license.sharealike_required`.

---

## 5. What is prohibited

An explicit negative list:

1. **Do not host NCCN Guidelines content** — text, tables, flowcharts,
   screenshots. Only `referenced` mode with our paraphrase.
2. **Do not use SNOMED CT concepts** in MVP without a country license.
   For clinical concepts — LOINC + ICD + own taxonomy.
3. **Do not use MedDRA** for AE coding — only CTCAE v5.0
   (public) plus free-text.
4. **Do not host Cochrane full-text reviews** — only abstracts + DOI.
5. **Do not host ESMO narrative** without per-publication license
   verification (NC-ND has restrictions).
6. **Do not display PubMed full text** for non-OA articles. Only abstract
   and a link to the DOI / publication page.
7. **Do not create derivatives from CC-BY-NC-ND sources** (such as recent
   ESMO years) — a rule engine built on parsed guidelines may qualify
   as a derivative. **Requires legal clarification.**
8. **Do not use OncoKB at all** — not even on the academic tier. The
   2026-04-27 audit established that OncoKB Terms of Use prohibit "use for
   patient services" and "generation of reports in a hospital or other
   patient care setting", which is the definition of OpenOnco's scope
   (CHARTER §2), regardless of commercial status. CIViC (CC0) is used
   instead. See §2.5 and §16.4.

---

## 6. Red flags — require legal review before public launch

Before `CHARTER §2` transitions from "draft" to "published":

1. **ESMO CC-BY-NC-ND derivative question** — does a rule engine that
   parses structured ESMO recommendations constitute a "derivative work"?
   If so — CC-BY-NC-ND prohibits it. If not — may be used with attribution.
2. **PubMed abstracts commercial distribution** — if OpenOnco ever moves
   to a paid tier, verify NLM Data Distribution terms.
3. **ATC codes commercial use** — if commercial, a license from the
   WHO Collaborating Centre is required.
4. ~~**OncoKB academic tier scope**~~ — **resolved 2026-04-27**: OncoKB
   ToS prohibit the OpenOnco use case regardless of academic/commercial
   distinction (clauses on "patient services" and "patient care reports"
   are absolute). CIViC (CC0) is used instead. Audit:
   `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`.
5. **SNOMED CT timing** — monitor whether Ukraine joins SNOMED
   International as a member country. If so — we can begin using it.

---

## 7. Seed list for the reference case (HCV-MZL)

Specific sources to connect for the first working use case
(HCV-associated Marginal Zone Lymphoma per `REFERENCE_CASE_SPECIFICATION.md`):

Split into two blocks: what we host (minimal, critical) and what we
reference (the vast majority).

#### 7.1. Hosted (locally, with justification)

| Source | Justification | What it provides for HCV-MZL | Next step |
|---|---|---|---|
| **CIViC** | H2 + H5 + CC0 | Variant-evidence entries (if any MZL-specific entries exist) | Discover via API, download subset locally |
| **CTCAE v5.0** | H2 + H5 | Toxicity grading for Regimen AE fields | Download PDF, parse → structured JSON |
| **ICD-O-3.2 codes** | H2 | Code 9699/3 (extranodal MZL), 9689/3 (splenic) | Download code table |
| **LOINC** (subset) | H2 | FIB-4, HCV RNA, CD20 IHC codes | API download, cache subset |
| **RxNorm / ATC** (subset) | H2 | L01FA01 (rituximab), L01AA09 (bendamustine) | Manual table, 20-30 drugs for MVP |
| **Ministry of Health Unified Clinical Protocol "Lymphoma"** | H1 (no API) | Ukrainian guideline — baseline recommendations | Scrape [moz.gov.ua](https://moz.gov.ua/), clinical reviewer verify |
| **NHSU formulary** (for MZL-relevant drugs) | H1 | Is bendamustine/rituximab reimbursed in Ukraine? | PDF parser + manual verify |
| **State Drug Registry** (for MZL-relevant drugs) | H1 | Are the drugs registered in Ukraine? | Scraper |
| **Our Indications, Regimens, Contraindications** | H4 | All clinical logic for HCV-MZL (two plans) | Clinical co-leads write in YAML |

**Total hosted:** code systems + Ukraine-local (no API) + our own content.
This is the minimum set where external referencing is impossible or
breaks performance.

#### 7.2. Referenced (live API / link)

| Source | How we access it | What it provides for HCV-MZL |
|---|---|---|
| **ESMO MZL Guideline 2024** | URL + clinical reviewer paraphrase | First-line recommendations, antiviral-first strategy |
| **NCCN B-Cell Lymphomas v.2.2025** | URL + paraphrase | Parallel opinion, categories of preference |
| **EASL HCV Guideline** | URL + paraphrase | Antiviral (DAA) regimens |
| **ClinicalTrials.gov** | live API via `clinicaltrials_client.py` | Active trials (filter: MZL, indolent lymphoma, Ukraine/EU sites) |
| **PubMed** | live E-utilities via `pubmed_client.py` | Key trials (Arcaini 2014, Hermine 2002) — citation metadata only |
| **DailyMed / openFDA** | live API (need `dailymed_client.py`) | Bendamustine, rituximab, obinutuzumab labels — contraindications, AE |
| **EMA EPARs** | URL + metadata snapshot | EU-specific labels, differences from FDA |
| **CIViC** ⭐ | hosted snapshot (CC0), monthly CI refresh | Biomarker-treatment mappings (primary actionability source — see §14) |
| **ClinVar, gnomAD** | live API | Variant interpretation / population frequency |

**Total referenced:** ~80% of sources. No ETL pipeline, no batch ingestion —
everything via clients during rule evaluation.

**Deliberately absent from the seed list:**
- SNOMED CT — license gate
- MedDRA — license gate
- Cochrane full text — paywalled

---

## 8. Process for adding a new source

For future sources (when expanding beyond HCV-MZL):

1. **Identify the license.** URL to the official terms. Canonical
   license name (SPDX ID if available).
2. **Determine the hosting mode** per the rules in §1. When in doubt —
   `referenced`.
3. **Verify the 4 constraints:**
   - Commercial use allowed?
   - Redistribution allowed?
   - Modifications allowed?
   - ShareAlike required?
4. **Add a row to the §2 matrix** in the appropriate tier.
5. **Create a `Source` entity** with all `license`, `attribution`,
   `hosting_mode` fields.
6. **If `hosting_mode: hosted`** — add the ingestion playbook to
   Part B (when written).
7. **If a red flag applies (Tier 1 license, commercial ambiguity,
   member-only access)** — `legal_review.status: pending`, blocked until review.

---

## 9. Disclaimer

**This document is an engineering best-effort analysis, not legal advice.**

Licenses change. NCCN may update its terms. Ukraine may join SNOMED.
ESMO may switch some guidelines to a different CC license. Before the
public launch of OpenOnco:

- (a) Have a legal counsel experienced in IP / medical data
  (Ukraine + international)
- (b) Legal review of all `Tier 1`, `mixed`-mode, and all sources with
  `legal_review.status: pending`
- (c) Establish OpenOnco's terms of use that explicitly describe:
  - non-commercial character
  - disclaimers
  - how users can report license concerns
  - the process for rapid content removal in the event of a claim

**Every 6 months — a full audit of the §2 matrix.** Sources with
`last_reviewed > 6 months` ago automatically enter the audit queue.

---

# Part B — Per-source Ingestion Playbook

## 11. Scope and goals of Part B

Part A established **what** can be done with each source (legally).
Part B establishes **how** we actually do it: where the data lives, which
clients call which APIs, when updates happen, who verifies, and what to
do when something fails.

**Part B readiness criterion:** an engineer should be able to take this
document + the seed source list from §7 and **within a week** connect the
first hosted entity (for example, ICD-O-3.2 codes) without additional
questions to the product team.

---

## 12. Common patterns

### 12.1. knowledge_base/ directory structure on disk

Proposed structure (open for discussion):

```
knowledge_base/
├── hosted/
│   ├── code_systems/
│   │   ├── icd_o_3/
│   │   │   ├── v2020/
│   │   │   │   ├── codes.yaml           # full code table
│   │   │   │   ├── _meta.yaml           # version, fetched_at, source_url, checksum
│   │   │   │   └── _diff_from_prev.yaml # what changed relative to the previous version
│   │   │   └── current → v2020          # symlink to active version
│   │   ├── loinc/v2.76/...
│   │   ├── rxnorm/2026-04/...
│   │   └── atc/2025/...
│   ├── civic/
│   │   └── 2026-04-24/evidence.yaml
│   ├── ctcae/
│   │   └── v5.0/grading.yaml
│   ├── ukraine/
│   │   ├── moz_protocols/
│   │   │   └── lymphoma-2024/
│   │   │       ├── source.pdf           # original for audit
│   │   │       ├── extracted.yaml       # structured extract
│   │   │       └── review.yaml          # clinical reviewer sign-off
│   │   ├── nszu_formulary/2026-04/reimbursed.yaml
│   │   └── drlz_registry/2026-04-24/registered.yaml
│   └── content/                          # H4 — our own content
│       ├── diseases/
│       │   └── hcv_mzl.yaml
│       ├── drugs/
│       │   ├── rituximab.yaml
│       │   └── bendamustine.yaml
│       ├── regimens/
│       │   ├── br_standard.yaml
│       │   └── r_chop_aggressive.yaml
│       ├── indications/
│       │   ├── ind_hcv_mzl_1l_antiviral.yaml
│       │   ├── ind_hcv_mzl_1l_br.yaml
│       │   └── ind_hcv_mzl_1l_rchop.yaml
│       ├── biomarkers/
│       ├── contraindications/
│       ├── redflags/
│       └── algorithms/
│           └── algo_hcv_mzl_1l.yaml
├── referenced/
│   └── sources.yaml                      # registry of all referenced Source entities
└── cache/                                # gitignored! do not commit
    ├── ctgov/
    │   └── <query_hash>.json             # TTL-expiring
    ├── pubmed/
    │   └── <pmid>.json
    ├── dailymed/
    │   └── <setid>.json
    └── ...
```

**Why YAML and not JSON/SQLite:**
- Readability for clinical reviewers (they edit content by hand)
- Git-friendly diffs (review via PR)
- Schema validation via Pydantic/JSONSchema on CI
- Migration to PostgreSQL later (KNOWLEDGE_SCHEMA §16.1 allows it) — when KB exceeds ~10K entries

**Why versioning via directories (v2020/, v2.76/) rather than git tags:**
- A hosted code system may have 2020 and 2024 versions **simultaneously active**
  — for example, a historical indication references an old ICD
- Git tag = snapshot of the entire repo, not per-source versioning
- The `current` symlink allows the rule engine to use the active version without changing the path

**What is gitignored:**
```
# .gitignore additions for knowledge_base
knowledge_base/cache/
knowledge_base/**/_fetch_log.json  # per-fetch run logs
```

### 12.2. Unified client interface

All live-API clients for referenced sources implement one protocol:

```python
# knowledge_base/clients/base.py

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SourceResponse:
    data: Any
    source_id: str          # "SRC-CTGOV-REGISTRY"
    fetched_at: str         # ISO-8601
    cache_hit: bool
    api_version: str        # whatever endpoint returns

@dataclass
class RateLimit:
    tokens_per_second: float
    burst: int

class SourceClient:
    """Base interface for all referenced-source API clients."""
    source_id: str
    base_url: str
    rate_limit: RateLimit
    cache_ttl_seconds: int

    def fetch(self, query: dict) -> SourceResponse: ...
    def health(self) -> dict: ...      # {ok: bool, latency_ms: int, last_error: str|None}
    def quota(self) -> dict: ...        # {remaining: int, reset_at: str}
```

**Implementations for seed:**
- `knowledge_base/clients/ctgov_client.py` — refactor from existing
  `clinicaltrials_client.py` (currently at top-level)
- `knowledge_base/clients/pubmed_client.py` — refactor from existing
- `knowledge_base/clients/dailymed_client.py` — **new**
- `knowledge_base/clients/openfda_client.py` — **new**
- ~~`knowledge_base/clients/oncokb_client.py`~~ — **REJECTED 2026-04-27**
  (OncoKB ToS, see §16.4). Replaced by the CIViC snapshot client
  (`knowledge_base/engine/snapshot_civic_client.py`), which reads the hosted YAML.
- `knowledge_base/clients/clinvar_client.py` — **new**
- `knowledge_base/clients/gnomad_client.py` — **new**

### 12.3. Caching for referenced sources

Query-level cache with TTL. Not a mirror.

```python
# Pseudo-interface

class TTLCache:
    def get(self, key: str) -> Optional[SourceResponse]: ...
    def put(self, key: str, value: SourceResponse, ttl_seconds: int): ...
    def invalidate(self, key: str): ...
```

**TTL per source** (see §22 for the full table):
- CT.gov: 24 hours (trials update daily, but per-trial rarely)
- PubMed: 7 days (abstracts are stable after publication)
- DailyMed/openFDA: 7 days (labels update rarely)
- ClinVar/gnomAD: 30 days (variant interpretations are more stable)
- (CIViC — not TTL-cached: hosted snapshot, updated monthly via CI;
  see §14. OncoKB excluded — see §16.4.)

**Cache key:**
- For GET with parameters: `{source_id}:{endpoint}:{sorted_params_hash}`
- For POST requests (rare): `{source_id}:{endpoint}:{body_hash}`

**Invalidation triggers:**
- TTL expiry (passive)
- Explicit bust via admin CLI (when we know the source has updated)
- Source entity `last_verified` updated — busts all cached responses
  from that source

### 12.4. General failure handling (graceful degradation)

Behaviour levels when an external API is unresponsive:

| Behaviour | Applied when |
|---|---|
| **Hard fail** — rule engine returns an error | Never. We do not block plan generation because of one downed API |
| **Soft degrade** — mark in output that the source is unavailable | Default for all referenced sources |
| **Stale cache** — use expired cache with a warning | CT.gov, PubMed when TTL expired + API down |
| **Skip** — don't cite this source, continue | CIViC snapshot corrupt / lookup returned no hit — generate without biomarker evidence references (n.b. CIViC is hosted, not live, so "downtime" reduces to `current` symlink integrity) |

The rule engine is required to:
1. Set a timeout on every client call (default 10s)
2. Log failure in `_fetch_log.json` (source_id, timestamp, error)
3. Add to the output a `freshness_warnings` list of sources that could not be contacted
4. UI displays a warning icon next to affected citations

### 12.5. Schema validation

Every hosted entity (code table, CIViC record, our Indication) passes:

1. **Pydantic / JSONSchema validation** on load — structure
2. **Referential integrity check** — all ID-referencing fields find
   their target (Indication.drug_id → Drug.id exists)
3. **Clinical sanity check** (for our content) — see CLINICAL_CONTENT_STANDARDS
4. **License compliance check** — Source entity has `hosting_mode`,
   `license`, `legal_review.status != pending`

On CI (GitHub Actions): fail the PR if any check fails.

---

## 13. Hosted: Code systems (ICD-O-3, LOINC, RxNorm, ATC)

### 13.1. Common pattern

All code systems share a common flow:
1. **Download** the official file (CSV / XML / TSV / JSON) from the source
2. **Parse** into canonical YAML
3. **Diff** against the previous version — what was added, removed, changed
4. **Clinical reviewer** confirms that the diff does not break active Indications
5. **Commit** the new version directory
6. **Switch symlink** `current/` to the new version

### 13.2. ICD-O-3.2

- **Source:** WHO ([ICD-O-3.2](https://www.who.int/standards/classifications/other-classifications/international-classification-of-diseases-for-oncology))
- **Format:** downloadable CSV + PDF reference
- **Update cadence:** rare (revisions every few years); monitor WHO news
- **Scope for MVP:** Full code table (~2000 morphology + ~300 topography). Small.
- **Ingestion:** ad-hoc manual download, one-time. Automated re-check once yearly.
- **Structure after parse:**
  ```yaml
  # knowledge_base/hosted/code_systems/icd_o_3/v2020/codes.yaml
  morphology:
    - code: "9699/3"
      term: "Extranodal marginal zone B-cell lymphoma of mucosa-associated lymphoid tissue (MALT lymphoma)"
      behavior: "3"  # malignant
      synonyms: ["MALT lymphoma", "extranodal MZL", ...]
    - code: "9689/3"
      term: "Splenic B-cell marginal zone lymphoma"
      ...
  topography:
    - code: "C16.0"
      term: "Cardia, stomach"
  ```
- **Client owner:** none (no API, one-time download)
- **Clinical review:** one reviewer confirms that new/deprecated codes
  do not orphan existing Indications

### 13.3. LOINC

- **Source:** Regenstrief ([LOINC](https://loinc.org/downloads/))
- **Format:** CSV / Zip download, requires a free LOINC account
- **Update cadence:** 2x per year (June, December)
- **Scope for MVP:** **Subset** — only codes used in our Tests. For HCV-MZL
  this is ~30-50 codes (FIB-4 components, HCV RNA PCR, CD19/CD20 IHC, CBC,
  LDH, B2-microglobulin, β2m, etc.).
- **Full LOINC:** ~100K codes; we do not host the full set. `v2.76/codes.yaml`
  contains only the `curated_subset: true` flag and the list of used codes
- **Ingestion:** CSV download + Python script that filters by the list
  in `knowledge_base/hosted/content/_loinc_usage.txt`
- **Attribution:** LOINC license requires "This material contains
  content from LOINC® (http://loinc.org)" in the UI.
- **Client owner:** optional — LOINC FHIR API exists, but for a subset
  a one-time local download is faster

### 13.4. RxNorm

- **Source:** NLM ([RxNorm download](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html))
- **Format:** ZIP with RRF (Rich Release Format) files
- **Update cadence:** monthly (1st Monday)
- **Scope for MVP:** subset — drugs in our Regimens. For HCV-MZL this is
  ~10-15 drugs (rituximab, bendamustine, cyclophosphamide, vincristine,
  prednisone, doxorubicin, obinutuzumab, sofosbuvir, velpatasvir, etc.)
- **Ingestion:** RRF files — complex format. Parse
  `RXNCONSO.RRF` + `RXNREL.RRF`, extract SAB='RXNORM' concepts
  that match our usage list
- **Requires:** UMLS Terminology Services license (free, academic).
  Apply online, ~1 week approval.
- **Client owner:** new `knowledge_base/ingestion/rxnorm_loader.py`

### 13.5. ATC / DDD

- **Source:** WHO Collaborating Centre ([ATC](https://www.whocc.no/atc_ddd_index/))
- **Format:** manual lookup or commercial subscription for bulk
- **Update cadence:** annual (January)
- **Scope for MVP:** manual table for drugs in our Regimens.
  Very small — ~15-20 codes. **We do not host the full table** — commercial
  redistribution requires a license.
- **Ingestion:** manual curation, one YAML file, reviewed annually
- **Attribution:** "ATC/DDD: WHO Collaborating Centre for Drug Statistics
  Methodology"

### 13.6. CTCAE v5.0

- **Source:** NCI ([CTCAE](https://ctep.cancer.gov/protocolDevelopment/electronic_applications/ctc.htm))
- **Format:** Excel + PDF, public domain
- **Update cadence:** CTCAE v5.0 (2017) stable. CTCAE v6.0 in progress — monitor.
- **Scope:** full (~800 AEs, each with grade 1-5 criteria)
- **Structure:**
  ```yaml
  # knowledge_base/hosted/ctcae/v5.0/grading.yaml
  adverse_events:
    - code: "CTCAE.10005329"
      term: "Anemia"
      moocd_category: "Blood and lymphatic system disorders"
      grades:
        "1": "Hemoglobin (Hgb) <LLN - 10.0 g/dL; <LLN - 100 g/L; <LLN - 6.2 mmol/L"
        "2": "Hgb <10.0 - 8.0 g/dL; <100 - 80 g/L; <6.2 - 4.9 mmol/L"
        "3": "Hgb <8.0 g/dL; <80 g/L; <4.9 mmol/L; transfusion indicated"
        "4": "Life-threatening consequences; urgent intervention indicated"
        "5": "Death"
  ```
- **Ingestion:** one-time download Excel, Python script → YAML.
- **Client owner:** none (static)

---

## 14. Hosted: CIViC (biomarker KB) — PRIMARY actionability source

**Status (2026-04-27):** Promoted to primary actionability source after
the OncoKB Terms of Use audit (see §2.5, §16.4, and
[`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`](../docs/reviews/oncokb-public-civic-coverage-2026-04-27.md)).

- **Source:** Washington University ([CIViC](https://civicdb.org/))
- **API:** GraphQL + REST available. Bulk download TSV (nightly).
- **License:** CC0-1.0 (no attribution required, but we provide it)
- **Update cadence:** daily updates upstream; we re-fetch monthly via CI.
- **Scope for v0.1:** full accepted evidence-item table. ~5K accepted
  evidence items, ~1.9K (gene, variant) pairs, 551 distinct genes
  (snapshot 2026-04-25; see §2 of the audit).
- **Storage path:** `knowledge_base/hosted/civic/<YYYY-MM-DD>/evidence.yaml`.
- **Ingestion flow:**
  1. Monthly CI workflow (`.github/workflows/civic-monthly-refresh.yml`):
     download CIViC TSV → Python loader → YAML.
  2. Diff vs previous snapshot — count new, changed, retracted entries.
  3. PR opened automatically; clinical reviewer sign-off is required
     if > 50 changes or any retracted entries affect an active `BMA-*` cell.
  4. Promote: `current` symlink to the new date after the PR is merged.
- **Implemented modules:**
  - `knowledge_base/ingestion/civic_loader.py` — TSV → YAML.
  - `knowledge_base/engine/civic_variant_matcher.py` — fusion-aware
    (gene, variant) matching (handles CIViC `BCR::ABL1` notation and
    inline mutations like `Fusion AND ABL1 T315I`).
  - `knowledge_base/engine/snapshot_civic_client.py` — read-only client
    over the hosted snapshot.
- **Structure (canonical):**
  ```yaml
  evidence_items:
    - id: 1234
      variant: {gene: "BRAF", variant: "V600E", hgvs_protein: "..."}
      disease: {name: "Melanoma", doid: "1909"}
      drugs: ["Vemurafenib"]
      evidence_level: "A"             # CIViC: A|B|C|D|E
      evidence_type: "Predictive"     # Predictive|Prognostic|Diagnostic|Predisposing|Functional|Oncogenic
      direction: "Supports"           # Supports | Does Not Support | N/A
      clinical_significance: "Sensitivity/Response"
      pmids: [22735384]
  ```
- **CIViC quirks (known and handled):**
  - Fusions are coded as `gene1::gene2` (e.g. `BCR::ABL1`, `EML4::ALK`).
  - Resistance mutations on a fusion background live in the `variant` field,
    not in `gene` (`gene: BCR::ABL1, variant: "Fusion AND ABL1 T315I"`).
    A naive `gene == "ABL1"` lookup misses 100% of CML kinase-domain
    evidence — `civic_variant_matcher` performs fusion-component splitting.
  - Exon descriptors live in CIViC in upper case (`EXON 19 DELETION`);
    our normalizer performs case-insensitive matching.
- **Direction handling:** `direction == "Does Not Support"` (~10% of items)
  is load-bearing — rendered as an **anti-evidence card**, not dropped.
  See KNOWLEDGE_SCHEMA §4.4.2.
- **Client owner:** existing `knowledge_base/ingestion/civic_loader.py`
  (wrapped in monthly CI).

---

## 15. Hosted: Ukraine-local (Ministry of Health, NHSU, State Drug Registry)

This is the **hardest and most important** block — no API, heterogeneous
formats, requires human verification. Without this OpenOnco provides no
value for Ukraine.

### 15.1. Ministry of Health — Unified Clinical Protocols

- **Source:** [moz.gov.ua](https://moz.gov.ua/) + [dec.gov.ua](https://www.dec.gov.ua/)
- **Format:** PDF (accompanying orders), often scanned copies
- **Update cadence:** irregular. Major protocols updated every 2-5 years
- **Discovery:** manual monitoring — subscribe to moz.gov.ua updates,
  track Order numbers for specific nosologies
- **Ingestion flow:**
  1. Identify a new or updated protocol (manual trigger)
  2. Download PDF → `knowledge_base/hosted/ukraine/moz_protocols/<slug>/<date>/source.pdf`
  3. OCR if scanned (tesseract + Ukrainian language pack)
  4. LLM-assisted extraction (permitted per CHARTER §8.1 — "extracting
     structured data from clinical documents") → `extracted.yaml`
  5. **Mandatory** clinical reviewer verification — compare
     extracted.yaml with the PDF, sign off in `review.yaml`
  6. Only after review sign-off — Indications referencing this
     protocol may be merged
- **Structure after extraction:**
  ```yaml
  # knowledge_base/hosted/ukraine/moz_protocols/lymphoma-2024/extracted.yaml
  protocol_id: "MOZ-UA-LYMPH-2024"
  title: "Unified Clinical Protocol: Lymphomas"
  order_number: "Order of the Ministry of Health of Ukraine No. 1234 dated 2024-XX-XX"
  effective_date: "2024-XX-XX"
  superseded_protocol: "MOZ-UA-LYMPH-2019"
  sections:
    - section_id: "first_line"
      title: "First-line treatment"
      recommendations:
        - text: "..."  # literal paraphrase from the PDF
          source_page: 23
          level_of_evidence: "..."
  raw_pdf_path: "source.pdf"
  extracted_by: "claude-code + manual verify"
  extracted_at: "2026-04-25"
  ```
- **Client owner:** new `knowledge_base/ingestion/moz_extractor.py`
  (PDF + OCR + LLM extraction pipeline)

### 15.2. NHSU formulary

- **Source:** [nszu.gov.ua](https://nszu.gov.ua/) — list of reimbursed drugs
- **Format:** PDF / Excel tables
- **Update cadence:** ~monthly (but changes are often marginal)
- **Ingestion flow:**
  1. Monthly fetch of the current list
  2. Parser Excel → YAML
  3. Diff vs previous — which drugs were added/removed from reimbursement
  4. Alerts for clinical reviewers if a drug in an active Regimen
     changed status
- **Structure:**
  ```yaml
  # knowledge_base/hosted/ukraine/nszu_formulary/2026-04/reimbursed.yaml
  effective_date: "2026-04-01"
  source_url: "https://..."
  drugs:
    - mnn: "Rituximab"
      mnn_ua: "Ритуксимаб"
      atc: "L01FA01"
      indications_reimbursed:
        - "Diffuse large B-cell lymphoma"
        - "Follicular lymphoma"
      conditions: "Within the National List..."
      source_row: "No. 142 in the list"
  ```
- **Client owner:** new `knowledge_base/ingestion/nszu_loader.py`

### 15.3. State Drug Registry

- **Source:** [drlz.com.ua](https://www.drlz.com.ua/) (State Expert Center of the Ministry of Health)
- **Purpose:** confirm that a drug is registered in Ukraine and has not
  been de-registered
- **Format:** web search UI, no bulk download
- **Ingestion:** per-drug lookup when creating a Drug entity. Not bulk.
- **Flow:**
  1. Clinical reviewer enters INN + trade name when creating a new Drug entity
  2. Script queries drlz.com.ua, extracts the result
  3. Stores in the Drug entity: `ukraine_registration.registered: true`,
     `registration_number`, `registered_on`, `last_verified`
  4. Quarterly re-verification — script iterates over all Drugs,
     checks current status. If status changed — alert.
- **Client owner:** new `knowledge_base/ingestion/drlz_lookup.py`

---

### 15a. Architectural invariant — UA-availability is annotation, never filter

> **Status:** PROPOSAL (2026-04-26). Aligns with CHARTER §2 (free public
> resource for evidence-based oncology) and the directive recorded in
> auto-memory `feedback_efficacy_over_registration.md`:
> "important — efficacy not registration status".

**Rule.** Whether a drug is registered in Ukraine, reimbursed by NHSU,
or both, MUST NOT influence which `Indication` / `Regimen` / track the
engine selects. UA-availability fields (`Drug.regulatory_status.ukraine_registration`,
`Drug.regulatory_status.reimbursement_nszu`) are **render-time advisory
metadata only**. The engine's selection signal is efficacy + evidence
tier + patient eligibility, full stop.

**Why.** OpenOnco surfaces the best clinical option per current
evidence even when in-country access is constrained. Hiding a
guideline-endorsed therapy because it is not reimbursed would distort
recommendations toward locally-available, often suboptimal alternatives
— defeating the project's purpose. The doctor, not the engine, decides
how to navigate the funding pathway (charitable foundation, employer
insurance, off-label import, international referral).

**Source-precedence corollary.** Ministry of Health Ukraine clinical protocols
(`SRC-MOZ-UA-*`) are a **national floor**, not a substitute for
Tier-1 international guidelines (NCCN, ESMO, ASCO, EAU). Where the Ministry of Health
prescribes a less-aggressive regimen than current Tier-1/2 evidence
endorses, OpenOnco follows the international evidence and cites the Ministry of Health
as confirmatory / national-floor context — never the other way around.

**Mechanisation.**

1. **`Source.precedence_policy` field** (`leading | confirmatory |
   national_floor_only | secondary_evidence_base`). All `SRC-MOZ-UA-*`
   sources MUST be annotated `national_floor_only`. The validator
   blocks a default-`Indication` whose only sources are
   `national_floor_only` when a peer `Indication` for the same scenario
   has at least one Tier-1/2 source.

2. **Validator gate** — `_check_source_precedence_policy` in
   `knowledge_base/validation/loader.py` runs in Pass 3 alongside
   RedFlag contract checks.

3. **Architectural-invariant test** —
   `tests/test_plan_invariant_ua_availability.py` parametrises four
   real patient fixtures, monkeypatches every `Drug` to
   `registered: false, reimbursed_nszu: false`, and asserts the
   engine's clinical-decision signature (default + alternative
   indication, tracks, regimen ids) is identical to the control run.
   This is the gate for all UA-ingestion work below.

**Anti-pattern (forbidden).**

- Engine-side filter that hides "not-reimbursed" recommendations.
- Ranking signal that downgrades a regimen because its drug is
  unregistered.
- Track-switching logic that prefers a less-effective in-country
  alternative when a better evidence-supported option exists.

**Permitted (advisory only).**

- Render-side **Access Matrix** that, for each surfaced track, shows
  the registration / reimbursement / cost-orientation status with
  pathway hints (per Phase B-D of
  `docs/plans/ua_ingestion_and_alternatives_2026-04-26.md`).
- A separate **`ExperimentalOption`** track exposing relevant
  ClinicalTrials.gov / EU CTR studies as additional alternatives —
  appended, never replacing the evidence-driven default.

---

## 16. Referenced: Live API clients

Short playbook per source. Full interface per §12.2.

### 16.1. ClinicalTrials.gov

- **Endpoint:** `https://clinicaltrials.gov/api/v2/studies`
- **Rate limit:** 50 req/min per IP (soft)
- **Client:** `clinicaltrials_client.py` (existing, at top-level). Refactor to the `SourceClient` interface.
- **Typical queries:**
  - Filter by disease + status (recruiting/active) + country (Ukraine, EU)
  - Fetch by NCT ID for citation
- **Cache TTL:** 24 hours
- **Quota handling:** exponential backoff; fall back to stale cache on
  429/503

### 16.2. PubMed / E-utilities

- **Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Rate limit:** 3 req/sec without API key, 10 req/sec with key
- **Client:** `pubmed_client.py` (existing). Refactor to `SourceClient`.
- **Typical queries:**
  - PMID → abstract + metadata
  - Search by disease + keywords for evidence discovery
- **Cache TTL:** 7 days for individual PMIDs (abstracts stable),
  24h for search queries
- **API key:** apply for a free NCBI key — increases rate limit

### 16.3. DailyMed / openFDA

- **DailyMed Endpoint:** `https://dailymed.nlm.nih.gov/dailymed/services/v2/`
- **openFDA Endpoint:** `https://api.fda.gov/drug/label.json`
- **Rate limit:** openFDA — 240 req/min without key, 120K/day with key
- **Client:** **new** `dailymed_client.py` + `openfda_client.py`
- **Typical queries:**
  - SETID → full drug label
  - Drug name → search labels
- **Cache TTL:** 7 days (labels update rarely)

### 16.4. OncoKB — REJECTED (2026-04-27)

- **Status:** **NOT integrated. Will not be integrated.**
- **Grounds:** OncoKB Terms of Use explicitly prohibit "use for patient
  services" and "generation of reports in a hospital or other patient
  care setting", which is the precise definition of OpenOnco's scope
  (CHARTER §2). Additionally: redistribution forbidden + AI training
  "strictly prohibited".
- **Audit:** [`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`](../docs/reviews/oncokb-public-civic-coverage-2026-04-27.md).
- **Instead of OncoKB:** the primary biomarker-actionability source is **CIViC**
  (CC0), see §2.5 and §14. Engine modules are named vendor-neutral
  (`actionability_*`) so that a future pivot to another source remains
  possible without rewriting the schema.
- **Not planned:** neither `oncokb_client.py` nor a mirror of `oncokb-datahub`.
- **Permitted remnants in YAML:** some `bma_*.yaml` and `BIO-*` files
  historically contain `oncokb_url` as a stable external reference to a
  published scientific page. This is a public URL used purely as a
  cross-reference in a citation record, not as a source of clinical
  recommendations — the render layer does not surface OncoKB content
  in the user UI.

### 16.5. ClinVar, gnomAD

- **ClinVar endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
  (same E-utilities as PubMed, db=clinvar)
- **gnomAD endpoint:** `https://gnomad.broadinstitute.org/api` (GraphQL)
- **Rate limit:** gentle, no hard limits
- **Client:** **new** `clinvar_client.py` + `gnomad_client.py`
- **Typical queries:**
  - Variant ID → clinical significance (ClinVar)
  - Variant → population allele frequency (gnomAD)
- **Cache TTL:** 30 days

---

## 17. Tooling inventory

### Existing (usable as-is / with refactor):
- `clinicaltrials_client.py` (top-level) — refactor to `SourceClient`
- `pubmed_client.py` (top-level) — refactor to `SourceClient`

### To build (seed for HCV-MZL):

| Module | Purpose | Priority |
|---|---|---|
| `knowledge_base/clients/base.py` | `SourceClient` interface, `TTLCache` | P0 — blocks all else |
| `knowledge_base/clients/dailymed_client.py` | DailyMed label lookup | P1 |
| `knowledge_base/clients/openfda_client.py` | openFDA drug labels | P1 |
| ~~`knowledge_base/clients/oncokb_client.py`~~ | **REJECTED 2026-04-27** — OncoKB ToS blocks the OpenOnco use case; replaced by CIViC. See §16.4. | — |
| `knowledge_base/clients/clinvar_client.py` | ClinVar via E-utilities | P2 |
| `knowledge_base/clients/gnomad_client.py` | gnomAD GraphQL | P3 |
| `knowledge_base/ingestion/civic_loader.py` | CIViC TSV → YAML | P1 |
| `knowledge_base/ingestion/icd_loader.py` | ICD-O-3.2 CSV → YAML | P1 |
| `knowledge_base/ingestion/loinc_loader.py` | LOINC subset loader | P1 |
| `knowledge_base/ingestion/rxnorm_loader.py` | RxNorm RRF → YAML | P2 |
| `knowledge_base/ingestion/ctcae_loader.py` | CTCAE Excel → YAML | P1 |
| `knowledge_base/ingestion/moz_extractor.py` | PDF → OCR → LLM → YAML | P0 — unique value |
| `knowledge_base/ingestion/nszu_loader.py` | NHSU Excel → YAML | P0 — unique value |
| `knowledge_base/ingestion/drlz_lookup.py` | per-drug State Drug Registry check | P1 |
| `knowledge_base/validation/schema_validator.py` | Pydantic validation on load | P0 |
| `knowledge_base/validation/refint_checker.py` | referential integrity | P1 |

**Stack:**
- Python 3.11+, stdlib where possible
- `pydantic` for schema validation (new dependency, but very appropriate)
- `httpx` for HTTP clients (better than stdlib `urllib` for async/retry)
- `pypdf` / `pdfplumber` for Ministry of Health PDFs
- `pytesseract` + Ukrainian language pack for OCR scans
- No heavy frameworks (no Django, no full ORMs — YAML + Pydantic is
  sufficient for now)

---

## 18. Operational cadence

| Source | Cadence | Trigger | Owner |
|---|---|---|---|
| ICD-O-3.2 | yearly re-check | manual (WHO news) | clinical lead |
| LOINC | 2x yearly (Jun, Dec) | scheduled | eng + clinical lead |
| RxNorm | monthly | scheduled cron | eng |
| ATC | yearly (January) | scheduled | clinical lead (manual curation) |
| CTCAE | yearly re-check (v6.0 pending) | manual (NCI news) | clinical lead |
| CIViC | monthly | scheduled CI (`.github/workflows/civic-monthly-refresh.yml`) | eng, reviewed by clinical lead if >50 changes |
| Ministry of Health protocols | ad-hoc on new Order | manual discovery | clinical lead |
| NHSU formulary | monthly | scheduled cron | eng + pharmacist review |
| State Drug Registry | quarterly per-drug | scheduled | eng alert → clinical lead |
| CT.gov, PubMed, DailyMed, openFDA, ClinVar, gnomAD | live, cache TTL per §12.3 | on-demand at rule eval | rule engine |

CI (GitHub Actions):
- monthly: CIViC fetch + diff PR (`civic-monthly-refresh.yml`,
  implemented 2026-04-27)
- monthly: RxNorm, NHSU
- weekly: health check all referenced APIs
- quarterly: State Drug Registry re-verification loop

Job output — PR with diff + scheduled re-verification, reviewed by clinical
co-lead before approval.

---

## 19. Failure modes and SLA

| Scenario | Detection | Mitigation | Customer impact |
|---|---|---|---|
| CT.gov API down | health probe fail | serve stale cache + warning | plan generated, but freshness warning on trial citations |
| PubMed rate limited (429) | HTTP 429 | backoff, fall back to cache | same as above |
| ~~OncoKB token expired~~ | n/a (OncoKB not used after the 2026-04-27 pivot — see §16.4) | n/a | n/a |
| Ministry of Health PDF format changed | parser exception on ingestion | manual extraction fallback, alert clinical lead | new Ministry of Health protocol not added to KB until fixed |
| CIViC retracted evidence | diff job detects | alert clinical lead before promote; hold until review | no impact on live system until review is completed |
| Code system version change (ICD, LOINC) | new version publication | scheduled re-check, clinical lead signoff | zero impact during review; switch symlink when ready |
| DailyMed returns modified drug label (recall) | daily poll of hashed labels | emergency pathway (CHARTER §6.2) | Indication clarified within 7 days; inline warning in plan immediately |

**SLA targets (MVP):**
- Plan generation success rate: > 99% (with warnings when needed)
- Zero "plan unavailable" due to external API: hard target
- Time from Ministry of Health protocol release to KB ingestion: < 30 days
- Time from FDA safety recall to KB reflection: < 7 days (emergency pathway)

---

## 20. Checklist: connecting a new hosted source

For each new hosted source (per §8 + additionally):

- [ ] License reviewed (Part A §2)
- [ ] Hosting mode selected (Part A §1); if `hosted` — justification H1-H5
- [ ] Directory structure created per §12.1
- [ ] Ingestion script written (`knowledge_base/ingestion/<source>_loader.py`)
- [ ] Schema validator written (Pydantic model)
- [ ] Source entity created with all license/attribution/legal_review fields (Part A §3)
- [ ] First fetch + diff vs null baseline + clinical review completed
- [ ] CI job for scheduled re-fetch configured
- [ ] Operational cadence entry added to §18
- [ ] Failure mode added to §19
- [ ] UI attribution text approved (if the license requires it)

---

## 21. What is out of scope for Part B (in Part C/D)

The following will be covered in subsequent parts of the document, not here:

- **Part C — Conflict & precedence rules:** when NCCN and ESMO
  disagree on the preferred regimen, what does the physician see?
  Which Indication becomes the default? Tier hierarchy for tie-breaking?
- **Part D — Freshness TTL & re-ingestion cadence deep dive:** formal
  SLA per source, alerting thresholds, snapshot coherence between
  sources (e.g., when the rule engine evaluates an Indication, should all
  its sources come from the same coherent time window?)

---

# Part C — Conflict & Precedence Rules

## 22. Scope and goals of Part C

Part A established **which** sources we listen to. Part B — **how** we
read them. Part C answers: when these sources **disagree with each other**,
how is the final Indication / Contraindication / RedFlag constructed,
and what does the physician see?

This is not an engineering question — it is a clinical editorial decision.
Therefore Part C has the status of **"recommendations for clinical reviewers"**,
not an executable rule. The rule engine does not perform automated conflict
resolution — conflicts are resolved by humans during `content/` editing.

---

## 23. Principles

### 23.1. Never automated resolution

The rule engine **does not choose** between conflicting sources. All
Indications, Regimens, Contraindications, RedFlags are written manually
by the clinical reviewer, with an explicit position taken (or the
controversy displayed). This echoes CHARTER §8.3: LLM/engine is not the
clinical decision-maker.

The engine receives an **already-resolved** Indication + optionally a
`known_controversies` block that clearly shows alternative positions.

### 23.2. Two plans by default (CHARTER §2)

The project always produces **two plans** — standard and aggressive. This
is partly a built-in mechanism for handling disagreement: when two respected
sources propose different approaches, we often have "standard = ESMO default +
Ukraine availability" and "aggressive = NCCN alternate + recent RCT".

Divergence between standard and aggressive is **not a conflict** — it is a
design output. A conflict is when sources disagree WITHIN the standard (or
aggressive) plan.

### 23.3. Presence not precedence

If source A recommends X and source B recommends Y, **both are preserved**
(see CLINICAL_CONTENT_STANDARDS §5.3). The choice of default for an Indication
is the clinical reviewer's. But the alternative position is always displayed
in the UI, with source references.

This is implemented via `Indication.known_controversies`:

```yaml
# knowledge_base/hosted/content/indications/ind_hcv_mzl_1l_standard.yaml
id: "IND-HCV-MZL-1L-STANDARD"
disease_id: "DIS-HCV-MZL"
line_of_therapy: 1
recommended_regimen: "REG-DAA-ANTIVIRAL-ONLY"
evidence_level: "Moderate"
strength_of_recommendation: "Strong"

sources:
  - source_id: "SRC-ESMO-MZL-2024"
    position: "supports"
    relevant_quote_paraphrase: "Antiviral-first for HCV-associated MZL..."
  - source_id: "SRC-NCCN-BCELL-2025"
    position: "supports"
    relevant_quote_paraphrase: "DAA-based antiviral therapy preferred for HCV+..."
  - source_id: "SRC-MOZ-UA-LYMPH-2024"
    position: "supports"

known_controversies:
  - topic: "Role of immediate rituximab if viral load clearance slow"
    positions:
      - position: "Monitor for 6 months post-DAA before adding rituximab"
        sources: ["SRC-ESMO-MZL-2024"]
      - position: "Add rituximab concurrent with DAA if bulky disease"
        sources: ["SRC-NCCN-BCELL-2025"]
        evidence_note: "Based on subgroup analysis; no direct comparison"
    our_default: "Monitor for 6 months"
    rationale: "ESMO position + aligned with Ministry of Health 2024 protocol; rituximab reserved for non-response or aggressive phenotype"
```

---

## 24. Tier hierarchy for clinical reviewers

When a reviewer writes a new Indication and sees a conflict between sources,
this list **influences but does not resolve** the decision. The reviewer
documents the decision in `Indication.rationale`.

### 24.1. Weight order (approximate)

| # | Tier | Sources | When it prevails |
|---|---|---|---|
| 1 | **Ukrainian regulatory** | Ministry of Health protocols, NHSU formulary, State Drug Registry | When determining **availability** and **reimbursement** — a blocking constraint. Not clinical content, but **what is actually accessible to the patient in Ukraine** |
| 2 | **International regulatory** | FDA, EMA labels | Approvals, contraindications, black box warnings — factual, not advisory |
| 3 | **Major international guidelines (current)** | NCCN, ESMO, ASCO, WHO | Default clinical recommendations. This is where conflicts arise most often |
| 4 | **Recent high-quality RCT** (< 2 years) | Phase 3, in a major journal, peer-reviewed | May **override a guideline** if the guideline has not yet updated and the RCT is sufficiently definitive |
| 5 | **Systematic reviews / meta-analyses** | Cochrane, NICE, others | Supporting evidence |
| 6 | **Molecular KBs** | CIViC (primary; OncoKB rejected per §16.4) | Biomarker-specific nuances |
| 7 | **Older / country-specific guidelines** | NCCN v.2020, BSH, EHA | Historical context; deprecated as primary |
| 8 | **Observational studies, single-arm trials** | phase 2, registries | Only when higher tiers are silent |
| 9 | **Expert opinion, editorials** | | Only as colour / rationale, never primary |

### 24.2. Special rules

**Rule 1 — Ukraine availability blocks a recommendation.** If a drug is
not registered in Ukraine OR is not reimbursed, the regimen cannot be
the `default_regimen` for Ukraine deployment. Alternative path:
the regimen remains in the Indication as `alternative_regimen` with an explicit
note "available in Ukraine via off-label import".

**Rule 2 — FDA/EMA black box is treated as an absolute contraindication.**
No guideline overrides this. If a guideline recommends a drug and there is an
FDA black box warning relevant to the patient's condition — the black box
triggers a RedFlag and selection of an alternative regimen.

**Rule 3 — Recent RCT can override an older guideline.** If an RCT was
published in 2026 and NCCN was last updated in 2024, and the RCT shows
statistically significant superiority — the reviewer **may** (not must)
update the default. Required:
- The RCT must be Phase 3, peer-reviewed
- Sample size adequate for the disease entity
- Primary endpoint clinically meaningful (OS > PFS > ORR for solid)
- Must pass both reviewers + one external consultation
- Mark in UI that the recommendation is based on a "post-guideline RCT"
- Trigger re-review at the next guideline update

**Rule 4 — Tier 1 (Ukrainian) does not override clinical evidence,
only availability.** A Ministry of Health protocol may be outdated relative
to NCCN/ESMO. If the Ministry of Health recommends X and NCCN 2025 recommends Y,
the clinical reviewer:
- If Y is available and reimbursed in Ukraine → default Y with references
  to both + note "Ministry of Health protocol predates this update"
- If Y is not available → default X (Ministry of Health), alternative Y with expected
  availability note
- Never silently ignore the Ministry of Health — explain the decision in rationale

**Rule 5 — Molecular KBs are lower than guidelines, but higher when
guidelines are silent.** If NCCN recommends a regimen without biomarker
refinement, and CIViC (primary actionability source — see §14) indicates
that biomarker X predicts response to regimen Y — Y becomes a candidate
for an alternative path, not an override of the default.

### 24.3. What is a "conflict" vs a "refinement"

Not all disagreements are conflicts.

| Situation | Type | Action |
|---|---|---|
| ESMO says "R-CHOP 6 cycles", NCCN "R-CHOP 6-8" | **Refinement** | Our Regimen specifies "6 cycles, 8 only if bulky residual" with references to both |
| ESMO says "bendamustine+rituximab", NCCN "R-CHOP" | **Conflict** | `known_controversies`, reviewer selects default |
| NCCN v.2024 vs NCCN v.2025 differ | **Version update** | Older deprecated, newer active; not a conflict |
| ESCAT IIA vs CIViC Level B | **Agreement with different nomenclature** | Normalise evidence levels (`escat_tier` — primary; per-source `level` — supporting), not a conflict |
| Single RCT contradicts meta-analysis | **Requires judgment** | Usually meta-analysis wins unless the RCT is larger/better |

---

## 25. Reviewer workflow: what to do when you see a conflict

1. **Document both positions explicitly.** Do not choose silently. Both
   positions with references to Source entities.
2. **Check the tier hierarchy (§24.1)** — which tier is each source's
   position from? Is there an obvious advantage?
3. **Check recency.** Older NCCN (v.2020) vs newer ESMO (2024) —
   recency matters.
4. **Check sample size and study design.** Phase 3 n=800 vs phase 2 n=45 —
   no question.
5. **Check Ukraine availability.** May resolve the question — unavailable
   automatically means not the default.
6. **If still unclear after §25.1-5:** other Clinical Co-Leads
   discussion, per CHARTER §6.1. External consultation if needed.
7. **Document the decision in `Indication.rationale`** with a reference to
   the reviewed conflict. The reviewer must record why the decision was
   made, not just what it was.
8. **Flag for re-review** in 12 months or at the next guideline update —
   whichever comes first.

---

## 26. UI patterns for displaying conflicts

### 26.1. Inline indicator

For each Indication / Contraindication that has `known_controversies`:
- Small ⚠️ icon "controversy exists" next to the regimen name
- Click → expands: "Our choice: X. Alternative position: Y (source Z).
  Rationale: ..."

### 26.2. Sources breakdown

Always a clickable "Sources" section at the bottom of the plan:
- Each Source with tier, date accessed, URL
- Tier color-coded (Ukrainian regulatory — blue, Guidelines — green,
  RCTs — orange, Molecular — purple)
- Controversy explicitly marked — "2 of 3 sources support X, 1 supports Y"

### 26.3. "Why not Y?" pattern

For each plan, if there is a rejected alternative, a one-click explanation:
"Why not R-CHOP? — A more aggressive regimen; for this patient with HCV-MZL
start with DAA. See ESMO 2024. If non-response at 6 months — re-evaluation."

This supports clinical transparency and simultaneously serves as material for
clinical education.

---

## 27. Versioning and stale positions

Rule: **a position based on an outdated source is automatically flagged**.

If `Indication.sources` references a Source entity with
`currency_status: superseded`, the CI validator:
- Emits a warning on the PR: "Indication X references superseded NCCN v.2024,
  replacement: NCCN v.2025. Re-review required."
- Does not block merge (may have been deliberate "snapshot for audit"), but
  marks it in the `_stale_review` list

Quarterly audit (CLINICAL_CONTENT_STANDARDS §9.1) iterates `_stale_review`
and reviews each Indication.

---

# Part D — Freshness TTL & Re-ingestion Cadence

## 28. Scope of Part D

Part B outlined TTL briefly in §12.3. Part D provides a detailed table
per source, alerting thresholds, the concept of a "coherent snapshot"
(a coherent point-in-time view of all sources at the moment of plan
rendering), and emergency pathways.

---

## 29. Per-source TTL and cadence (full table)

### 29.1. Hosted — re-ingestion cycle

| Source | Re-ingest cadence | Detection mechanism | Alert threshold | Owner |
|---|---|---|---|---|
| ICD-O-3.2 | Yearly | Manual check WHO news | N/A — stable | Clinical lead |
| LOINC | 2x yearly (June, December) | Release schedule | 60 days after expected release — alert | Engineering + Clinical |
| RxNorm | Monthly (1st Monday) | Scheduled cron | Cron fail > 2 consecutive — page on-call | Engineering |
| ATC | Yearly (January) | Manual | 90 days after expected — alert | Clinical lead |
| CTCAE | Yearly re-check | Manual NCI announcements | v6.0 release — immediate review | Clinical lead |
| CIViC | Monthly | Scheduled CI (`civic-monthly-refresh.yml`) | > 50 diff items or retracted items hitting active `BMA-*` cell — clinical lead signoff required before promote | Engineering + Clinical |
| Ministry of Health protocols | Ad-hoc on new Order | Manual discovery (moz.gov.ua subscription) | New relevant protocol → <30 day ingestion target | Clinical lead |
| NHSU formulary | Monthly | Scheduled cron | Drug status change for active Regimen → immediate alert | Engineering + pharmacist |
| State Drug Registry | Quarterly per-drug | Scheduled | Registration status change → immediate alert | Engineering → Clinical lead |

### 29.2. Referenced — cache TTL

| Source | Cache TTL (default) | Cache scope | Bust triggers |
|---|---|---|---|
| ClinicalTrials.gov | 24 hours | Query result | Explicit admin bust; Source.last_verified update |
| PubMed (PMID fetch) | 7 days | Per PMID | Rare — abstracts stable |
| PubMed (search) | 24 hours | Query hash | Query parameter change |
| DailyMed (SETID fetch) | 7 days | Per SETID | Recall event (manual bust) |
| openFDA (label search) | 24 hours | Query hash | |
| ~~OncoKB~~ | n/a — REJECTED 2026-04-27 (see §16.4); biomarker actionability is read from the hosted CIViC snapshot, not via TTL-cache | | |
| ClinVar | 30 days | Per variant ID | |
| gnomAD | 90 days | Per variant | Very stable |

---

## 30. The "coherent snapshot" concept

When a plan is generated on **2026-05-15**, it references:
- CT.gov records from cache dated 2026-05-14
- PubMed abstracts from 2026-05-08
- Our Indication with `last_reviewed: 2026-03-01`
- NCCN (referenced) last fetched 2026-04-20
- Ministry of Health protocol 2024

This is **temporally incoherent** — different "moments" of knowledge.

### 30.1. What we guarantee

**Sort of "coherent":**
- For each Indication / Regimen / Contraindication — all its `sources`
  have `last_verified` within the last 6 months (CLINICAL_CONTENT §9.1)
- If any source has `currency_status: superseded` — a warning is shown

**Not guaranteed:**
- That the cached CT.gov query from 2026-05-14 and PubMed from 2026-05-08
  represent "the same state of the world". This is a practical impossibility.

### 30.2. What we display in the UI

In the footer of every plan:
```
Plan generated: 2026-05-15 14:23 UTC
Knowledge base snapshot:
  - Our clinical content: last updated 2026-04-12
  - CIViC: 2026-05-13
  - LOINC: 2.76 (2025-12)
  - Ministry of Health Lymphoma Protocol: 2024 (latest)
Live-queried at generation:
  - ClinicalTrials.gov (fetched 2026-05-15)
  - PubMed (fetched 2026-05-15)
  - DailyMed (fetched 2026-05-15)
```

The physician sees exactly what the plan was built from.

---

## 31. Emergency pathway

CHARTER §6.2 describes the emergency update process. Part D specifies
triggers and system behaviour.

### 31.1. Emergency triggers

| Event | Source | Auto-detected? | Target timeline |
|---|---|---|---|
| FDA safety alert (black box added / removed) | openFDA feed | Yes — daily poll hash of FDA drug labels | < 24 hours: alert; < 7 days: fully reflected |
| Drug recall | openFDA recalls endpoint | Yes | < 24 hours: alert + emergency Contraindication added |
| Ministry of Health Order on drug de-registration | Manual monitoring | No | < 48 hours from discovery |
| CIViC retraction of evidence hitting an active Indication | CIViC diff | Yes | Immediate alert; pause Indication merge until reviewed |
| Major guideline update announced | Manual | No | 30-day ingestion target |
| Critical RCT published with clinically significant superiority | Manual | No | Reviewers discuss inclusion |

### 31.2. Emergency workflow

1. **Detection** — either automatic (openFDA diff, CIViC diff) or manual
   (clinical lead noticed)
2. **Immediate action** (first 24h):
   - Temporary inline warning added to relevant Indications:
     "A safety signal has been received; recommendation is under review. Date:
     2026-05-15"
   - Clinical co-lead + additional reviewer make the decision
3. **Structured update** (first 7 days):
   - Contraindication entity created or updated
   - Indication.known_controversies possibly added
   - Source with `emergency_update: true` flag
4. **Full review** (within 14 days):
   - Standard two-reviewer workflow for the permanent change
   - Update changelog with "emergency update" label

External communication — for a critical safety change (drug recall) —
push notification to clinics that generated a plan with the affected drug
in the last N months (if we have opt-in plan registration).

---

## 32. Audit snapshot (for compliance)

Every generated plan **stores an immutable snapshot**:
- `plan_id`, `generated_at`
- `knowledge_base_state`:
  - hashes of the active version of each hosted source
  - timestamps of cached referenced responses
  - Indication, Regimen, Algorithm id + their version
- `patient_input_hash` (no PHI, just shape validation)

This enables:
- Retrospective audit: "on what exact knowledge state was this plan
  generated on 2026-05-15"
- Debugging: reproduce the plan exactly as issued
- Regulatory inquiry response

The snapshot is stored separately from the plan (often PHI-free) and has
`retention: indefinite` in accordance with CHARTER §10.2.

---

## 33. SLA summary (operational targets)

| Metric | Target | Measurement |
|---|---|---|
| Plan generation success rate | > 99% | monthly rolling |
| "Plan unavailable" due to API failure | 0 | hard — should never happen (graceful degrade) |
| Stale warning appearance rate | < 20% of plans | daily |
| Ministry of Health protocol → KB ingestion | < 30 days | per-protocol tracking |
| FDA safety → inline warning | < 24 hours | per-event |
| FDA safety → structured Contraindication | < 7 days | per-event |
| CIViC diff → review | < 7 days | per-release |
| Quarterly audit completion | 100% entries with `last_reviewed < 180 days` | quarterly |

---
