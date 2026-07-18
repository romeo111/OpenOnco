# OpenOnco — README Blurbs & Promo Copy

Reusable copy for READMEs, landing pages, posts, and decks. All claims are grounded in the OpenOnco fact sheet (state 2026-07-18).

> **Disclaimer (include on every public asset):** OpenOnco is an informational clinical decision support tool for healthcare professionals — **not a medical device**, not FDA-cleared, not for direct patient use, and not for emergency or time-critical decisions. It is an early-stage **v0.1 draft** and is **not clinically validated**. All recommendations are drafts that must be verified by a qualified oncologist.

> **Reuse note for copywriters:** these blurbs are meant to be copied piecemeal. Whenever you excerpt a tagline, description, pitch, or the footer into a standalone public asset, carry the disclaimer above (not-a-medical-device + must-be-verified-by-an-oncologist) with it, and keep the v0.1-draft / STUB maturity framing intact.

---

## Taglines (pick one)

1. **Two cited treatment plans for your tumor board — drafted by rules, not by an LLM.**
2. **Rules-first, fully cited oncology decision support. No LLM ever picks the regimen or dose.**
3. **Open-source CDS for oncologists: deterministic, source-cited, and built to be verified — not trusted blindly.**

*(Each tagline is a draft-to-verify framing for HCPs; pair with the disclaimer when used standalone.)*

---

## Descriptions

### Short (1 sentence)

OpenOnco is a free, open-source clinical decision support resource for oncology tumor boards that drafts two alternative, fully source-cited treatment plans from a deterministic rule engine — no LLM ever picks the regimen or dose, and every plan is an early-stage draft for a clinician to verify.

### Medium (1 paragraph)

OpenOnco is an informational clinical decision support (CDS) tool for oncologists, hematologists, and tumor boards. A clinician feeds it a structured patient profile (FHIR/mCODE-shaped JSON: disease, biomarkers, findings, demographics), and a declarative rule engine returns one Plan with at least two alternative treatment tracks side by side — a standard track and a more aggressive track — each carrying regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. If histology isn't confirmed, it returns a diagnostic workup brief instead of a treatment plan. All clinical logic lives in a deterministic rule engine over a versioned, human-reviewed knowledge base — no LLM chooses the regimen or dose, so it can't hallucinate a drug or a dose. It runs locally (CLI, in-browser Pyodide, Python import, or an MCP server), so patient data never leaves your machine. OpenOnco is an early-stage v0.1 draft actively seeking clinician feedback: the knowledge base spans 103 diseases, but clinical content is still maturing — only 15 of 1061 clinical entities have two-reviewer sign-off and the rest are STUB ("proposed plan, not approved plan"). It is not a medical device, is not clinically validated, and every plan must be verified by a qualified oncologist.

### Long (3 paragraphs)

**What it is.** OpenOnco is a free, open-source clinical decision support resource for oncology — designed for healthcare professionals (oncologists, hematologists, tumor boards) and for builders of safety-critical decision-support systems. A clinician submits a structured patient profile (FHIR/mCODE-shaped JSON), and a declarative rule engine returns one Plan containing at least two alternative treatment tracks side by side: a standard track and a more aggressive track. Each track ships with its regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. When histology is not yet confirmed, the engine declines to produce a treatment plan and instead returns a Diagnostic Brief of workup steps. The knowledge base currently spans 103 diseases across lymphoid and myeloid hematology and solid tumors (with 831 indications, 404 regimens, 321 ATC/RxNorm-coded drugs, 669 red flags, and 471 cited sources) — but coverage is not the same as clinical sign-off: most of this content is still STUB (see "Where it stands").

**How it's different.** Clinical decisions come from declarative rules over a versioned, human-reviewed knowledge base — never from an LLM (CHARTER §8.3). Because no LLM picks the regimen or dose, the engine cannot hallucinate a drug or a dose. The engine is deterministic and reproducible: the same input plus the same KB version always yields the same plan, produced through six fixed stages in roughly 50–200 ms. Every recommendation is source-cited by construction, enforced by a three-layer citation guard (Pydantic referential check, CI paraphrase-grounding verifier, and a render-time guard that warns or drops uncited cells). Actionability evidence is drawn from CIViC (CC0, WashU) read from a local nightly snapshot, with ESCAT tier surfaced as a badge. It is privacy-by-design: the engine runs locally via CLI, in-browser Pyodide (Python WASM, no backend), or Python import — patient JSON never leaves the device, with no server-side PHI, no logs, and no database. It always presents alternatives side by side rather than a single binding directive, an explicit anti-automation-bias design choice (CHARTER §15.2 C6), and it is designed to meet FDA non-device CDS criteria (CHARTER §15) — a design goal, not a certification. Code is MIT; specs and generated content are CC BY 4.0; source guidelines (NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU, and others) are referenced, not redistributed. An MCP server exposes the engine to any Model Context Protocol client (Claude Desktop, Cursor, etc.), so an LLM can relay cited engine output instead of answering from memory.

**Where it stands.** OpenOnco is an early-stage **v0.1 draft**. The engine and the cited knowledge base are live, but clinical maturity is deliberately measured by dual sign-off: only **15 of 1061** clinical entities have received two-Clinical-Co-Lead approval — the rest are **STUB** (structured data, algorithm, and sources are in place, but not yet dual-reviewer signed off). STUB means "proposed plan, not approved plan." No formal clinical validation study has been done, and there is no real-world deployment validation. OpenOnco is **not** a medical device, is **not** clinically validated, and does **not** replace an oncologist or a tumor board — it produces drafts to be verified by the treating physician. The most valuable contribution right now is clinician feedback: try the in-browser demo (synthetic examples only) on a case you know, and tell us what's wrong.

---

## Suggested README badges

```markdown
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://github.com/romeo111/OpenOnco)
[![Content License: CC BY 4.0](https://img.shields.io/badge/content%20license-CC%20BY%204.0-lightgrey.svg)](https://github.com/romeo111/OpenOnco)
[![Site: openonco.info](https://img.shields.io/badge/site-openonco.info-brightgreen.svg)](https://openonco.info)
[![Try the demo](https://img.shields.io/badge/demo-try%20in%20browser-orange.svg)](https://openonco.info/try.html)
[![MCP server](https://img.shields.io/badge/MCP-server-purple.svg)](https://github.com/romeo111/OpenOnco/tree/main/mcp_server)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-success.svg)](https://github.com/romeo111/OpenOnco)
[![Status: v0.1 draft](https://img.shields.io/badge/status-v0.1%20draft-yellow.svg)](https://openonco.info)
```

Rendered:

[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://github.com/romeo111/OpenOnco)
[![Content License: CC BY 4.0](https://img.shields.io/badge/content%20license-CC%20BY%204.0-lightgrey.svg)](https://github.com/romeo111/OpenOnco)
[![Site: openonco.info](https://img.shields.io/badge/site-openonco.info-brightgreen.svg)](https://openonco.info)
[![Try the demo](https://img.shields.io/badge/demo-try%20in%20browser-orange.svg)](https://openonco.info/try.html)
[![MCP server](https://img.shields.io/badge/MCP-server-purple.svg)](https://github.com/romeo111/OpenOnco/tree/main/mcp_server)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-success.svg)](https://github.com/romeo111/OpenOnco)
[![Status: v0.1 draft](https://img.shields.io/badge/status-v0.1%20draft-yellow.svg)](https://openonco.info)

---

## Elevator pitches by audience

*(Each pitch is HCP/builder-facing; carry the not-a-medical-device + verify-with-an-oncologist disclaimer whenever a pitch is used on its own.)*

**For the oncologist / tumor board:**
Feed OpenOnco a structured patient profile and get two alternative, fully source-cited treatment tracks (standard + aggressive) side by side, each with a step-by-step decision trace to verify and tailor — drafted by a deterministic rule engine, never by an LLM, so it can't hallucinate a drug or dose. It's an early-stage v0.1 draft: the KB spans 103 diseases but most clinical content is STUB (only 15 of 1061 entities are dual-reviewer signed off), so treat every plan as a starting point you verify, not a replacement for your judgment. Try it on a case you know and tell us what's wrong.

**For the AI developer:**
OpenOnco is a forkable, open-source pattern for safety-critical CDS: a deterministic, reproducible rule engine (six stages, ~50–200 ms, same input + same KB version = same output) over a versioned knowledge base with citations enforced by a three-layer guard — and an MCP server that lets any LLM route an oncology question through the engine instead of answering from memory. Code is MIT; the LLM relays cited engine output and never picks the regimen itself.

**For the open-source contributor:**
OpenOnco runs on a distributed, AI-assisted "chunk" workflow (TaskTorrent): you can draft structured sidecars and open PRs without clinical expertise, and Clinical Co-Leads review all clinical content before merge. Today only 15 of 1061 entities are dual-signed-off and the project is openly seeking clinician feedback — there's a lot of high-leverage, well-scoped work to pick up. Code is MIT, content is CC BY 4.0.

**For the potential funder:**
OpenOnco is a free public-good oncology CDS resource built rules-first for safety: deterministic logic over a 103-disease, 471-source cited knowledge base, no LLM choosing regimens, privacy-by-design (runs locally, no PHI leaves the device), and designed to meet FDA non-device CDS criteria. It's an early-stage v0.1 draft and is not clinically validated — most clinical content is still STUB (only 15 of 1061 entities have two-reviewer sign-off) and no formal validation study has been done. Funding would accelerate dual-reviewer clinical sign-off and the path toward validation.

---

*OpenOnco is an early-stage, open-source project actively seeking clinician feedback. It is an informational tool for healthcare professionals — not a medical device, not clinically validated; all recommendations must be verified by a qualified oncologist. Site: https://openonco.info · Repo: https://github.com/romeo111/OpenOnco · Demo: https://openonco.info/try.html*
