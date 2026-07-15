# OpenOnco — promotion fact sheet (source of truth)

> Auto-extracted + safety-reviewed. All promo copy must conform to this.

## One-liner

OpenOnco is a free, open-source clinical decision support resource for oncology tumor boards: a rules-first, deterministic engine over a versioned, fully source-cited knowledge base that drafts two alternative treatment plans for a clinician to verify — no LLM ever picks the regimen or dose.

## What it is

OpenOnco is an informational clinical decision support (CDS) tool for healthcare professionals (oncologists, hematologists, and tumor boards) and for builders of safety-critical decision-support systems. A clinician feeds it a structured patient profile (FHIR/mCODE-shaped JSON: disease, biomarkers, findings, demographics) and a declarative rule engine returns one Plan containing at least two alternative treatment tracks (a standard track and a more aggressive track) side by side, each with regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. If histology is not yet confirmed, the engine returns a Diagnostic Brief (workup steps) instead of a treatment Plan. All clinical logic lives in the rule engine over a curated, human-reviewed knowledge base; the engine is deterministic and runs offline (CLI, in-browser Pyodide, Python import, or via an MCP server). It is positioned as an FDA non-device CDS tool (CHARTER §15) — informational support, not a medical device, not for direct patient use, and not for time-critical/emergency decisions.

## Key facts

- Knowledge base scale (capabilities page, state 2026-06-17): 92 diseases, 664 indications (230 first-line, 172 second-line+), 384 treatment regimens, 298 drugs (ATC/RxNorm coded), 594 red flags, 444 cited sources, 16 virtual MDT clinician skills.
- Dual clinical sign-off is the key maturity metric: only 15 of 806 clinical entities have received two-Clinical-Co-Lead sign-off; the rest are STUB (structured data + algorithm + sources in place, but not yet dual-signed-off).
- STUB means 'proposed plan, not approved plan' — structured data, algorithm, and sources exist, but it has not passed two-reviewer clinical sign-off (CHARTER §6.1).
- Coverage spans lymphoid + myeloid hematology and solid tumors; 77 of 92 diseases have a full modeled chain, the rest partial. Examples in gallery: DLBCL, FL, CLL/SLL, MCL, MZL, MM, gastric, esophageal, PDAC, cholangiocarcinoma, CRC, NSCLC, SCLC, mesothelioma.
- Engine runs 6 deterministic stages (resolve algorithm, flatten findings, evaluate red flags, walk decision tree, materialize tracks, resolve regimens); ~50-200 ms per profile; same input + same KB version = same output (reproducible).
- Privacy by design: runs locally via CLI, in-browser Pyodide (Python WASM, no backend), or Python import — patient JSON never leaves the user's machine; no server-side PHI, no logs, no DB. Public site uses synthetic examples only.
- Actionability evidence comes from CIViC (CC0, WashU) as the primary source, read from a local nightly snapshot; ESCAT tier surfaced as a badge. OncoKB was rejected because its ToS conflicts with the project's non-commercial scope.
- Every recommendation carries a source citation enforced by a 3-layer citation guard (Pydantic loader referential check, CI verifier for paraphrase grounding, render-time guard that warns or drops uncited cells).
- Licensing: code is MIT; specifications and generated content are CC BY 4.0. Original source guidelines (NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU, etc.) are referenced, not redistributed.
- An MCP server exposes the engine to any Model Context Protocol client (Claude Desktop, Cursor, etc.) with tools engine_info, list_diseases, generate_treatment_plan, generate_diagnostic_brief; the LLM relays cited engine output and never picks the regimen itself.
- Project status is v0.1 draft, explicitly seeking clinician feedback; no formal clinical validation study has been done and there is no real-world deployment validation (CHARTER §13).
- Scope is adults only, HCP-only, outpatient/non-time-critical planning; explicitly excludes pediatrics, direct-to-patient use, and emergency/time-critical oncology.
- Built for distributed AI-assisted contribution via a TaskTorrent 'chunk' workflow; contributors draft structured sidecars and open PRs, but all clinical content is reviewed by Clinical Co-Leads before merge.
- Note for copywriters: README cites older KB numbers (420 indications, 377 sources, 140 algorithms); prefer the capabilities-page figures (state 2026-06-17) as the current canonical counts.

## Audiences

- Practicing oncologists and hematologists preparing for or running tumor boards (primary user; HCP-only)
- Multidisciplinary tumor boards / MDT teams seeking a drafted, fully-cited starting point to verify and tailor
- Clinical pharmacologists reviewing regimens, contraindications, and access/reimbursement context
- Developers and builders of safety-critical, rules-first decision-support systems who want a forkable open-source pattern (engine + MCP interface)
- AI-tooling contributors who want to help verify/draft clinical content via the TaskTorrent chunk workflow (no clinical expertise required to trigger drafting)
- Researchers and clinicians who want a transparent, source-grounded, auditable oncology logic reference

## Differentiators

- Rules-first, deterministic engine — clinical decisions come from declarative rules over a versioned, human-reviewed knowledge base, NOT from an LLM (CHARTER §8.3). Because no LLM picks the regimen or dose, the engine cannot hallucinate a drug or a dose.
- Every single recommendation ships with a source citation, enforced by a 3-layer citation guard; nothing is unsourced by construction.
- Always presents at least two alternative tracks side by side (standard + aggressive) — never a single 'system-prescribes-X' directive — an explicit anti-automation-bias design (CHARTER §15.2 C6).
- Fully transparent and auditable: step-by-step decision trace, FDA Criterion-4 metadata block, and reproducible output (same input + same KB version = same plan).
- Privacy by design: deterministic engine runs locally / in-browser; patient data never leaves the device, no backend, no logging.
- Fully open source and free: code MIT, content CC BY 4.0 — designed to be forked and reused for any safety-critical decision-support domain.
- Designed to meet FDA non-device CDS criteria (CHARTER §15) and refuses to act outside that envelope (no histology -> no treatment plan; no raw image/signal/NGS input; no time-critical indications; no per-patient dose calculation).
- An MCP server lets any LLM route an oncology question through the deterministic engine instead of answering from memory — safer by construction.

## Links

- **site**: https://openonco.info
- **repo**: https://github.com/romeo111/OpenOnco
- **demo**: https://openonco.info/try.html
- **mcp_server**: https://github.com/romeo111/OpenOnco/tree/main/mcp_server
- **llms_txt**: https://openonco.info/llms.txt

## Approved claims

- Free and fully open source — code MIT, content CC BY 4.0.
- An informational clinical decision support resource for oncologists and tumor boards.
- Generates two alternative treatment plans (standard + aggressive) side by side for a clinician to verify and tailor.
- Every recommendation comes with a source citation.
- No LLM picks the regimen or dose — clinical logic is a deterministic rule engine over a versioned, human-reviewed knowledge base (so it can't hallucinate a drug or dose).
- Runs locally and in the browser; patient data never leaves your machine.
- Designed as an FDA non-device clinical decision support tool (informational support, not a medical device).
- Always shows alternatives side by side — never a single binding directive — by design, to counter automation bias.
- Transparent and auditable: a step-by-step decision trace accompanies every plan.
- An early-stage, open-source project actively seeking clinician feedback.
- Can be called from your LLM (Claude, Cursor, etc.) via an MCP server so the model relays cited engine output instead of guessing.
- Covers 92 diseases across hematologic and solid-tumor oncology with 444 cited sources (state 2026-06-17).
- Refuses to generate a treatment plan without confirmed histology; returns a diagnostic workup brief instead.
- Try the in-browser demo on a case you know and tell us what's wrong — clinician feedback is the most valuable contribution right now.

## Forbidden claims (NEVER say)

- Do NOT say it diagnoses cancer or detects/screens for cancer.
- Do NOT say it is a medical device, FDA-approved, FDA-cleared, or CE-marked.
- Do NOT say it is clinically validated, clinically proven, peer-reviewed-validated, or production-ready (no formal clinical validation study has been done).
- Do NOT say it replaces, substitutes for, or is as good as an oncologist or a tumor board.
- Do NOT say it prescribes drugs, calculates patient-specific doses, or makes the treatment decision.
- Do NOT say patients can or should use it to self-treat, self-diagnose, or make their own treatment decisions — it is HCP-only.
- Do NOT say it is for emergencies, urgent, or time-critical oncology decisions.
- Do NOT say an LLM/AI chooses or recommends the regimen, or that it uses AI to pick treatments.
- Do NOT imply the clinical content is fully reviewed or signed off — most entities are STUB (only 15 of 806 dual-signed-off).
- Do NOT claim EHR integration that executes actions, real-time formulary feeds, surgery/radiation-as-standalone modeling, or pediatric coverage (these are out of scope or not modeled).
- Do NOT cite OncoKB, SNOMED CT, or MedDRA as data sources (OncoKB rejected on ToS/license grounds; SNOMED/MedDRA out of MVP on license grounds).
- Do NOT present synthetic/demo cases or the reference case as real patient outcomes, or imply outcome/efficacy guarantees.

## Safety rules

- Every public asset (page, post, slide, README, demo) must carry the not-a-medical-device disclaimer and the 'all recommendations must be verified by a qualified oncologist' statement (CHARTER §11 + §15).
- Always frame the audience as healthcare professionals / tumor boards (and builders) — never patients or caregivers self-treating.
- Always state or clearly imply the project is early-stage (v0.1 draft) and seeking clinician feedback; never imply it is validated or production-ready.
- When citing the engine's output, make clear it is a draft to be verified by the treating physician, not a final decision.
- Pair any coverage/number claim with the maturity caveat that most clinical content is STUB (not yet dual-reviewer signed off).
- Use only the five canonical links provided; do not invent URLs or cite real-patient data.
- Never present synthetic examples as real patients; the public site and all examples use synthetic/de-identified data only.
- Reinforce the core safety guarantee accurately: no LLM picks the regimen/dose — recommendations are deterministic, rule-based, and cited.

## Maturity note

Early-stage v0.1 open-source draft: the engine and a 92-disease cited knowledge base are live, but only 15 of 806 clinical entities have two-reviewer sign-off and there has been no formal clinical validation study — frame it as a project actively seeking clinician feedback, not a validated product.
