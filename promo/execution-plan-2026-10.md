# OpenOnco visibility: execution plan

Start: 2026-10-10. Planning horizon: 2026-11-09. Dates below are targets, not scheduled jobs or commitments by external organizations.

## Goal and measurement

Earn discoverability and qualified feedback from oncology clinicians and developers. Thirty-day targets: 3 documented clinician reviews of synthetic cases, 2 reproducible developer setup reports, and 1 appropriate directory submission. Targets are not promised outcomes. Search impressions, indexed URLs, referring domains, GitHub referrals, stars and demo visits are secondary indicators; never equate traffic or coverage with clinical validation.

Baseline checked 2026-10-10: the live homepage reports 103 diseases, 831 indications, 404 regimens and 542 sources. These are coverage counts, not reviewed-content counts. README and June promotion assets quote older counts. GitHub already exposes an MIT license, citation metadata and discovery topics; repeating those tasks adds no value. Existing pages already have MedicalWebPage, canonical and language-alternate metadata, sitemap and robots. The wiki's disease results previously pointed to coverage-table anchors rather than separate pages. Plans already render as A4-printable HTML; browser Save as PDF is the first export path to assess before building another exporter.

Unknown baseline: Search Console access, actual indexed-page counts, search impressions, referral analytics, clinical-review recruitment conversion and domain-specific adoption. Record as unknown until measured; do not invent zeroes. Do not add trackers to patient inputs.

## Sequence and acceptance criteria

| Target | Owner | Action | Definition of done / dependency |
|---|---|---|---|
| Oct 10 | Coding agent | Disease landing pages in EN/UA; MedicalCondition linked to MedicalWebPage; source provenance and clinical-review caveat; README freshness/privacy fix | Focused tests pass; isolated commit pushed; Pages deployment verified or explicitly reported pending |
| Oct 11–13 | Maintainer with agent support | Establish search baseline | Domain verified in Google Search Console and Bing Webmaster Tools using owner accounts; submit existing sitemap; record 10 sample URL inspection results and first dated metrics export |
| Oct 11–14 | Coding agent | Audit 831 indication and 404 regimen pages before adding them | Record missing-page counts and clinical-render requirements; implement small representative batch before corpus-wide rollout; sources, review status and licensing retained |
| Oct 13–17 | Agent + maintainer | Developer launch assets | Capture local synthetic-case demo and MCP setup; verify documentation links use actual default branch `master`; one independent clean-install reproduction before launch |
| Oct 15–20 | Maintainer | One Show HN launch | Use reviewed copy below and functioning demo. Post once using maintainer identity; disclose project ownership; log URL, replies and actionable issues. No patient data |
| Oct 15–24 | Maintainer + clinical lead | Recruit 3 clinical reviewers | Ask for review of 3 synthetic cases from one familiar disease, with trace and citation checks. Record missing source, mismatch, severity and reproducibility. Any treatment-content edits follow two-reviewer governance |
| Oct 18–27 | Agent | Standards gap analysis | Map PatientProfile fields to mCODE 4.0.0 profiles and document unmapped fields plus synthetic fixtures. No claim of mCODE conformance, OMOP integration or OHDSI affiliation without implemented and validated adapters |
| Oct 20–30 | Maintainer | One appropriate developer-directory submission | Recheck repository activity and contribution rules; supply exact description and evidence of working setup. Avoid directories whose production/adoption criteria are not met |
| Oct 24–Nov 4 | Maintainer + clinical lead | One advocacy / resource-constrained clinic research discussion | Choose a named clinical reviewer and ask about accessibility, language and evidence-review needs. Use synthetic material and clinician supervision; do not advertise as a substitute for licensed guidelines or a validated clinical system |
| Nov 5–9 | Maintainer + agent | Review results, select next investment | Publish dated metrics + issue links. Continue channels yielding qualified reviews; fix recurring onboarding/source problems. Academic manuscript only after methods, evaluation dataset and accountable clinical authors exist |

## Channels verified, with concrete disposition

| Channel | Evidence / fit | First artifact | Disposition |
|---|---|---|---|
| Hacker News | [Show HN guidelines](https://news.ycombinator.com/showhn.html): a usable project people can try | Working browser demo, setup instructions, transparent draft status | First launch candidate after independent demo reproduction; author account required |
| kakoni/awesome-healthcare | [Contribution rules](https://github.com/kakoni/awesome-healthcare/blob/master/CONTRIBUTING.md) require recognized adoption, production use and reasonably GA software | Evidence of adoption and maturity | Defer: early-stage draft positioning does not demonstrate these requirements. Do not submit a misleading PR |
| OHDSI Oncology WG | [Oncology WG](https://ohdsi.github.io/OncologyWG/) works on cancer representation in OMOP for observational research | Explicit OMOP gap report and synthetic mapping example | Technical feedback candidate, not an endorsement channel or existing integration |
| HL7 mCODE | [Published implementation guide](https://hl7.org/fhir/us/mcode/) identifies v4.0.0 / FHIR R4 | Profile mapping, terminology gaps and validator output | Standards work before publicity; “FHIR-shaped JSON” alone proves no conformance |
| Patient advocacy and LMIC clinics | No named recipient or existing partnership verified in this audit | Shortlist with actual clinical reviewer, local access constraints and source-license review | Research pending; do not claim partnerships or replace paid clinical references |

## Show HN copy for maintainer publication

**Title:** Show HN: OpenOnco – rules-first oncology drafts with source citations

**URL:** https://openonco.info/try.html

**First comment:**

I work on OpenOnco, an early-stage open-source oncology decision-support project. Its Python engine reads versioned YAML rules and drafts alternative treatment tracks for a qualified oncologist to inspect. No LLM selects the regimen or dose. Deterministic output can still be wrong if rules, source interpretation or data are wrong; citations and traceability make those errors inspectable, not impossible.

The browser plan builder runs locally with Pyodide. The separate optional Tumor Board interface is server-backed and sends submitted text off-device. Please use synthetic examples when trying public tools. Code is MIT; project content is CC BY 4.0, while cited upstream sources retain their own licenses.

This is an informational tool, not a medical device. Every recommendation must be verified by a qualified oncologist. Clinical content remains provisional pending the project's review requirements; we do not claim clinical validation or patient outcomes.

We would value reproducible setup failures, confusing evidence traces and source mismatches in synthetic cases. Code and issue tracker: https://github.com/romeo111/OpenOnco. Live coverage and review context: https://openonco.info/capabilities.html.

## Distribution log

Maintain one row per real action: date, channel, public URL or private reference, exact copy version, owner, response, resulting issue and next step. No fabricated submissions, contacts, replies or endorsements. Publishing to third-party communities and contacting recipients require a concrete chosen venue/recipient and authorized identity; this plan is not a claim that anything has been sent.

## Explicitly deferred

Journal submission, conference abstracts, Product Hunt launch and broad advocacy promotion follow evaluation and reviewer recruitment. Do not invent authors, affiliations, patient outcomes, ethics approvals or conference deadlines. JSON-LD does not guarantee rich results or ranking: [Google's structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data).

## Execution record

- Implemented in the initial change: deterministic EN/UA disease pages, visible codes and provenance, source links, related wiki links, localized condition names, MedicalCondition metadata and focused regression tests.
- README now points to current metrics rather than embedding stale counts and distinguishes local browser processing from the optional server-backed interface.
- Existing dirty generated files are excluded from this request's commit. Fresh generated disease pages and discovery changes must be built from the isolated delivery checkout before production publication.
- Publication/account work, clinician recruitment and external responses remain pending. No recurring job was created.
