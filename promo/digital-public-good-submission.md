# OpenOnco — Digital Public Goods (DPG) submission draft

Draft answers to the [DPG Standard](https://digitalpublicgoods.net/standard/) 9
indicators, for submission at <https://app.digitalpublicgoods.net/signup>. DPG
recognition is the **single biggest distribution lever for LMIC government/NGO
adoption** of a free health tool and is referenced by downstream health funders
(UNICEF, Digital Square, WHO). No legal entity is required to apply.

> Maintainer: verify each answer and the current questionnaire before submitting;
> the DPG form wording changes. Keep the honest early-stage / STUB framing.

**Project:** OpenOnco · **Website:** https://openonco.info · **Repo:** https://github.com/romeo111/OpenOnco

---

### 1. Relevance to Sustainable Development Goals
Primary: **SDG 3 — Good Health and Well-being** (target 3.4, reduce premature
mortality from non-communicable diseases incl. cancer; 3.8 universal health
coverage; 3.c health workforce). OpenOnco is free oncology clinical decision
*support* that helps clinicians draft and cross-check cited treatment options,
most valuable where specialist tumor boards are scarce (LMICs, rural care).
Supporting: SDG 10 (reduced inequalities — narrows the specialist-access gap),
SDG 9 (open infrastructure).

### 2. Use of an approved open license
- **Code:** MIT (OSI-approved) — root `LICENSE`.
- **Content & specifications:** CC BY 4.0 (an approved open-content license).
- Upstream clinical guidelines are *referenced, not redistributed* (NCCN, ESMO,
  EHA, etc. retain their licenses); biomarker actionability uses **CIViC (CC0)**.

### 3. Clear ownership
Ownership and governance are documented in the public repository
(`specs/CHARTER.md`, `README.md`). The project is maintainer-led
(GitHub: `romeo111`) with AI-assisted contributors; all clinical content passes
human (two-Clinical-Co-Lead) review before promotion out of STUB.

### 4. Platform independence
No mandatory closed-source dependencies. The engine is pure Python (MIT deps:
pydantic, httpx, pyyaml) and also runs **fully in-browser via Pyodide (WASM)**,
on any OS, offline. It deliberately avoids license-gated terminologies
(no SNOMED CT, no MedDRA) in favor of open standards (LOINC, ICD-10/ICD-O-3,
RxNorm, CTCAE v5). No vendor lock-in.

### 5. Documentation
Public and substantial: `README.md`, six specifications under `specs/`
(`CHARTER.md`, `KNOWLEDGE_SCHEMA_SPECIFICATION.md`, `SOURCE_INGESTION_SPEC.md`,
etc.), `CLAUDE.md` contributor guide, `mcp_server/README.md`, an in-browser
demo, and machine-readable `llms.txt` / `llms-full.txt`.

### 6. Mechanism for extracting data
All knowledge-base data is **open YAML in git history** and is also published as
machine-readable JSON (`disease_coverage.json`, `kb_search_index.json`,
exportable engine bundles). No proprietary data store; full export by design
(data is stored as files, validated on load).

### 7. Adherence to privacy & applicable laws
**Privacy by design:** the engine runs locally / in-browser — patient data never
leaves the device; no server-side PHI, no logs, no database. The public site
ships **synthetic examples only** (no real patient data; per `CHARTER §9.3`).
Positioned as **informational, non-device clinical decision support** (not a
medical device); every recommendation must be verified by a qualified
oncologist (`CHARTER §11, §15`).

### 8. Adherence to standards & best practices
Patient intake follows **FHIR R4/R5 + mCODE**; coding via **LOINC, ICD-10 /
ICD-O-3, RxNorm, CTCAE v5**. Open development practices: public repo, tests
(pytest), schema validation (Pydantic), versioned content, citation-guard CI.

### 9. Do no harm by design
- **No LLM picks the regimen or dose** — clinical logic is a deterministic rule
  engine over peer-reviewed content, so it cannot hallucinate a drug or dose
  (`CHARTER §8.3`).
- **Anti-automation-bias:** always presents ≥2 alternative tracks side by side,
  never a single binding directive (`CHARTER §15.2 C6`).
- **Honest maturity:** most content is **STUB ("proposed, not approved")** — only
  15 of 806 entities have two-reviewer sign-off; no formal clinical validation
  yet. This is disclosed everywhere.
- **Data protection:** local-only processing; no PHI collection; synthetic public
  data. **Not for patient self-use**; HCP-facing, adults, non-emergency.
- No targeting of vulnerable groups; no advertising; non-commercial public-good
  posture.

---

*OpenOnco is an informational clinical decision support resource — not a medical
device, not FDA-cleared, not clinically validated. Early-stage (v0.1), actively
seeking clinician feedback. Every recommendation must be verified by a qualified
oncologist.*
