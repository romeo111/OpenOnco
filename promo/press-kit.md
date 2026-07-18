# OpenOnco — Press Kit / One-Pager

> *Informational clinical decision support for oncology professionals. Not a medical device. All recommendations must be verified by a qualified oncologist.*

---

## Headline

**OpenOnco: a free, open-source, rules-first decision-support engine for oncology tumor boards — every recommendation cited, no LLM ever picks the regimen or dose.**

## Summary (2 sentences)

OpenOnco is a free, open-source clinical decision support (CDS) resource for oncologists, hematologists, and tumor boards: a clinician feeds in a structured patient profile and a deterministic rule engine — running over a versioned, fully source-cited, human-reviewed knowledge base — drafts two alternative treatment tracks (standard and aggressive) side by side for the clinician to verify and tailor. No large language model ever chooses the regimen or the dose; every claim ships with a source citation, the engine runs locally so patient data never leaves the machine, and it is positioned as an FDA non-device CDS tool — informational support, not a medical device.

---

## The problem

Tumor-board planning is information-dense and time-pressured: clinicians must reconcile guidelines (NCCN, ESMO, EHA, BSH, EASL, national protocols), biomarker actionability, contraindications, and supportive care for each patient, then defend every choice. General-purpose AI tools are tempting shortcuts, but they can hallucinate a drug or a dose, hide their reasoning, and offer a single confident answer that invites automation bias — none of which is acceptable in a safety-critical clinical setting. What is missing is a transparent, auditable, source-grounded starting point that a clinician can trust enough to *check* — one where the software never pretends to make the decision.

---

## How it works (rules-first, cited)

- **Structured input.** A clinician supplies a patient profile shaped as FHIR/mCODE-style JSON (disease, biomarkers, findings, demographics). Synthetic examples only on the public site.
- **Deterministic rule engine.** All clinical logic lives in a declarative rule engine over a curated, human-reviewed knowledge base (CHARTER §8.3). It runs **6 stages** — resolve algorithm → flatten findings → evaluate red flags → walk decision tree → materialize tracks → resolve regimens — in roughly **50–200 ms per profile**. Same input + same KB version = same output (reproducible).
- **No LLM in the decision.** No language model selects the regimen or dose, so the engine cannot hallucinate a drug or a dose. LLMs only relay already-cited engine output.
- **Two tracks, side by side.** Every Plan returns at least two alternative treatment tracks — a standard track and a more aggressive track — each with regimen, supportive care, contraindications, monitoring, and a step-by-step decision trace. Never a single binding directive (an explicit anti-automation-bias design, CHARTER §15.2 C6).
- **Histology gate.** If histology is not yet confirmed, the engine refuses to draft a treatment plan and returns a **Diagnostic Brief** (workup steps) instead.
- **Citations by construction.** Every recommendation carries a source citation, enforced by a **3-layer citation guard**: a Pydantic loader referential check, a CI verifier for paraphrase grounding, and a render-time guard that warns on or drops uncited cells.
- **Actionability evidence.** Biomarker actionability comes from **CIViC (CC0, WashU)** as the primary source, read from a local nightly snapshot, with the ESCAT tier surfaced as a badge. (OncoKB was rejected because its ToS conflicts with the project's non-commercial scope.)
- **Runs anywhere, privately.** CLI, in-browser Pyodide (Python WASM, no backend), Python import, or an **MCP server** for any Model Context Protocol client (Claude Desktop, Cursor, etc.). Patient JSON never leaves the user's machine — no server-side PHI, no logs, no database.

---

## Key facts & numbers *(state 2026-07-18)*

| Metric | Value |
|---|---|
| Diseases covered | **103** (86 with a full modeled chain, rest partial) |
| Indications | **831** (262 first-line, 175 second-line+) |
| Treatment regimens | **404** |
| Drugs (ATC/RxNorm coded) | **321** |
| Red flags | **669** |
| Cited sources | **471** |
| Virtual MDT clinician skills | **16** |
| Engine runtime | ~50–200 ms per profile, deterministic |

**Coverage** spans lymphoid + myeloid hematology and solid tumors — e.g. DLBCL, FL, CLL/SLL, MCL, MZL, MM, gastric, esophageal, PDAC, cholangiocarcinoma, CRC, NSCLC, SCLC, mesothelioma.

**Maturity — read this honestly:** the clinical content is mostly **STUB** — meaning the structured data, algorithm, and sources are in place, but the entity has *not* yet passed two-Clinical-Co-Lead sign-off (CHARTER §6.1). Only **15 of 1061** clinical entities are dual-signed-off; the rest are "proposed plan, not approved plan." There has been **no formal clinical validation study and no real-world deployment validation** (CHARTER §13). This is a **v0.1 draft** actively seeking clinician feedback — not a validated or production-ready product.

**Licensing:** code is **MIT**; specifications and generated content are **CC BY 4.0**. Original source guidelines (NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU, etc.) are *referenced, not redistributed*.

---

## Who it is for

- **Practicing oncologists and hematologists** preparing for or running tumor boards (primary user; HCP-only).
- **Multidisciplinary tumor boards / MDT teams** wanting a drafted, fully-cited starting point to verify and tailor.
- **Clinical pharmacologists** reviewing regimens, contraindications, and access/reimbursement context.
- **Developers / builders of safety-critical, rules-first decision-support systems** who want a forkable open-source pattern (engine + MCP interface).
- **AI-tooling contributors** who want to help verify or draft clinical content via the TaskTorrent "chunk" workflow (no clinical expertise required to trigger drafting; all clinical content is reviewed by Clinical Co-Leads before merge).
- **Researchers and clinicians** who want a transparent, source-grounded, auditable oncology logic reference.

**Scope guardrails:** adults only, HCP-only, outpatient / non-time-critical planning. It explicitly **excludes** pediatrics, direct-to-patient use, and emergency / time-critical oncology. It does not diagnose, screen for, or detect cancer; it does not prescribe drugs or calculate patient-specific doses.

---

## What makes it different

1. **Rules-first, deterministic — not an LLM.** Clinical decisions come from declarative rules over a versioned, human-reviewed KB (CHARTER §8.3); because no LLM picks the regimen or dose, the engine *cannot hallucinate a drug or a dose*.
2. **Cited by construction.** Every single recommendation ships with a source citation, enforced by a 3-layer citation guard — nothing is unsourced.
3. **Always two tracks, never one directive.** Standard + aggressive side by side, an explicit counter to automation bias.
4. **Transparent and auditable.** Step-by-step decision trace, FDA Criterion-4 metadata block, reproducible output.
5. **Private by design.** Runs locally / in-browser; patient data never leaves the device; no backend, no logging.
6. **Open and forkable.** MIT code + CC BY 4.0 content, reusable for any safety-critical decision-support domain.
7. **Built to stay inside the FDA non-device CDS envelope.** No histology → no treatment plan; no raw image/signal/NGS input; no time-critical indications; no per-patient dose math.
8. **MCP-native safety.** An MCP server lets any LLM route an oncology question through the deterministic engine instead of answering from memory — safer by construction.

---

## Links

- **Site:** https://openonco.info
- **Try the in-browser demo:** https://openonco.info/try.html
- **Code (GitHub):** https://github.com/romeo111/OpenOnco
- **MCP server:** https://github.com/romeo111/OpenOnco/tree/main/mcp_server
- **llms.txt:** https://openonco.info/llms.txt

---

## Boilerplate (reusable)

> OpenOnco is a free, open-source clinical decision support resource for oncology professionals. A clinician feeds it a structured patient profile and a deterministic, rules-first engine — running over a versioned, fully source-cited, human-reviewed knowledge base — drafts two alternative treatment tracks (standard and aggressive) side by side, each with a regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. No large language model ever chooses the regimen or the dose, so the engine cannot hallucinate a drug or a dose; it runs locally and in the browser, so patient data never leaves the user's machine. OpenOnco is positioned as an FDA non-device clinical decision support tool — informational support for healthcare professionals, not a medical device, and every recommendation must be verified by a qualified oncologist. It is an early-stage (v0.1) project actively seeking clinician feedback. Code is MIT-licensed; content is CC BY 4.0. Learn more at https://openonco.info.

---

## What we need

OpenOnco is early-stage and open — the most valuable contribution right now is honest clinical feedback.

- **Clinician feedback (most valuable).** Try the in-browser demo on a case you know and tell us what's wrong: https://openonco.info/try.html
- **Clinical Co-Leads / reviewers.** Help move entities from STUB to dual-signed-off (CHARTER §6.1) — only 15 of 1061 are signed off today. Oncologists, hematologists, and clinical pharmacologists especially welcome.
- **Contributors (no clinical expertise required to start).** Draft structured sidecars and open PRs via the TaskTorrent "chunk" workflow; all clinical content is reviewed by Clinical Co-Leads before merge.
- **Builders of safety-critical CDS.** Fork the engine + MCP pattern, kick the tires, and tell us where the rules-first design breaks.

---

## Screenshots / assets to capture

- **In-browser demo** (`try.html`) — landing state plus a worked synthetic case being entered.
- **Sample two-track Plan** — standard vs. aggressive tracks side by side, showing regimen, contraindications, monitoring, and a visible source citation on a claim.
- **Decision-trace view** — the step-by-step trace + FDA Criterion-4 metadata block (the auditability story).
- **Virtual MDT view** — the 16 MDT clinician skills / multidisciplinary perspective.
- **Diagnostic Brief** — the "no confirmed histology → workup steps instead of a plan" safety behavior.
- **Citation guard in action** — a recommendation cell with its source citation (and, if showable, an uncited cell being dropped/flagged).
- **MCP integration** — the engine called from an MCP client (e.g. Claude Desktop / Cursor) relaying cited engine output.
- **Capabilities page** — the coverage numbers (state 2026-07-18) with the STUB-vs-signed-off maturity caveat visible.

---

### Disclaimer footer

*OpenOnco is an informational clinical decision support resource for healthcare professionals — it is **not a medical device**, is not FDA-approved, FDA-cleared, or CE-marked, and is **not clinically validated**. It does not diagnose, screen for, or detect cancer; it does not prescribe drugs or calculate patient-specific doses; and it does not replace or substitute for an oncologist or a tumor board. It is intended for adult, outpatient, non-time-critical planning by qualified healthcare professionals only — not for direct patient use and not for emergency or time-critical decisions. All outputs are drafts that **must be verified by a qualified oncologist** (CHARTER §11, §15). This is an early-stage v0.1 open-source project; most clinical content is STUB (only 15 of 1061 entities dual-reviewer signed off) and no formal clinical validation study has been performed. All examples use synthetic data; nothing shown represents a real patient or guarantees any clinical outcome.*
