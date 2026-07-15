# OpenOnco — Reddit Promotion Asset

> **Usage note for the poster:** Reddit self-promotion rules are strict and culture varies sharply by subreddit. Post to **one subreddit at a time**, space posts out by several days, and **read each subreddit's rules + recent mod posts before submitting**. Reply to comments in good faith — these are framed as feedback requests, not launches, and should stay that way. Every post below carries the not-a-medical-device disclaimer and the "verify with a qualified oncologist" statement, per project safety rules. Do not edit those out.

---

## 1. r/medicine

**Caution (read first):** r/medicine is heavily moderated and restricts self-promotion. Many "I built a tool" posts are removed on sight. **Message the moderators first** to ask whether a feedback-seeking post about a free, open-source, non-commercial clinician tool is permitted, and disclose that you are the developer. Verification flair may be required to post or comment substantively. Do **not** post a link as the submission — use a self/text post, lead with the critique request, and put links at the bottom. If mods say no, respect it. This is a place to be critiqued by clinicians, not to market.

**Title:**
Built a free, open-source oncology CDS tool where the rule engine — not an LLM — drafts the treatment plan. Looking for clinicians to tear it apart.

**Body:**

Disclosure: I'm the developer. This is a free, non-commercial, open-source project (no product, no signup, nothing to sell). Mods — happy to remove if this isn't allowed; I've tried to follow the self-promo rules and I'm here for critique, not promotion.

I've been building **OpenOnco**, an informational clinical decision support tool for oncologists, hematologists, and tumor boards. I'd genuinely like clinicians here to look at it and tell me where it's wrong.

What it does: you give it a structured patient profile (FHIR/mCODE-shaped JSON — disease, biomarkers, findings, demographics) and a deterministic rule engine returns one Plan with **at least two alternative treatment tracks side by side** (a standard track and a more aggressive track). Each track carries regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and **a source citation on every claim**. If histology isn't confirmed, it refuses to produce a treatment plan and returns a diagnostic workup brief instead.

The design decision I most want feedback on: **no LLM ever picks the regimen or the dose.** All clinical logic is a declarative rule engine over a versioned, human-reviewed knowledge base. Same input + same KB version = same output. It deliberately shows alternatives side by side rather than a single "system says X" directive, as an anti-automation-bias measure. There's no per-patient dose calculation and no raw image/NGS input.

Honest about maturity — this is the important part:
- It's **v0.1 draft.** No formal clinical validation study has been done. No real-world deployment.
- Knowledge base today: 92 diseases, 384 regimens, 664 indications, 298 drugs, 594 red flags, 444 cited sources (state 2026-06-17).
- **But most of that content is STUB:** structured data + algorithm + sources are in place, but only **15 of 806 clinical entities** have passed the required two-Clinical-Co-Lead sign-off. STUB = "proposed plan, not approved plan." I am not claiming this content is reviewed or safe to use as-is.
- Actionability evidence is from CIViC (CC0). Source guidelines (NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU, etc.) are referenced, not redistributed.

It is positioned explicitly as an FDA **non-device** CDS tool: informational support, **not a medical device**, HCP-only, adults only, outpatient/non-time-critical planning. Not for emergencies. Not for direct patient use. **Every output is a draft that must be verified by the treating oncologist.**

What would actually help me: pick a disease you know cold, run a synthetic case in the browser demo (no install, no backend, the patient JSON never leaves your machine), and tell me where the logic, the citations, or the framing is wrong or unsafe.

- Demo (synthetic cases only): https://openonco.info/try.html
- Site: https://openonco.info
- Code: https://github.com/romeo111/OpenOnco

**Disclaimer:** OpenOnco is a research/support tool, not a medical device. It is not FDA-cleared, CE-marked, or clinically validated. All recommendations are drafts and must be verified by a qualified oncologist. It does not diagnose cancer, is HCP-only, and is not for time-critical decisions.

---

## 2. r/oncology

**Caution:** Smaller and less restrictive than r/medicine, but still disclose you're the developer and keep it feedback-first. Lead with the clinical framing (two-track plans, citations) rather than the tech. Expect — and welcome — skepticism about STUB coverage and lack of validation; answer it plainly.

**Title:**
Free open-source tool that drafts two cited treatment tracks (standard + aggressive) for a case — rule engine, not an LLM. Oncologists: where does it break?

**Body:**

Developer disclosure up front. **OpenOnco** is a free, open-source, non-commercial informational CDS resource aimed at oncologists, hematologists, and tumor boards. I'm looking for clinical critique, not signups.

The idea: feed it a structured patient profile (disease, biomarkers, findings, demographics) and get back **two alternative treatment tracks side by side** — a standard track and a more aggressive one — each with regimen, supportive care, contraindications, monitoring, a decision trace, and **a citation on every claim.** No confirmed histology → it returns a diagnostic workup brief instead of a treatment plan.

Why it might be worth your five minutes:
- **The engine is deterministic and rules-first. No LLM selects the regimen or dose** — so it can't hallucinate a drug or a dose. The clinical logic is a versioned, human-reviewed knowledge base, not a model's guess.
- It always presents **alternatives, never one binding directive** — a deliberate hedge against automation bias.
- Every recommendation is **sourced**, enforced by a citation guard, so you can chase the evidence behind each cell.

Coverage spans lymphoid + myeloid heme and solid tumors — examples in the gallery include DLBCL, FL, CLL/SLL, MCL, MZL, MM, gastric, esophageal, PDAC, cholangiocarcinoma, CRC, NSCLC, SCLC, mesothelioma. 92 diseases total (77 with a full modeled chain), 444 cited sources, actionability from CIViC (CC0); ESCAT tier shown as a badge.

The honest caveats, because they matter clinically:
- **v0.1 draft. No formal clinical validation study. No real-world deployment.**
- **Most content is STUB** — data + algorithm + sources exist, but only **15 of 806 entities** have two-reviewer clinical sign-off. Treat everything as a proposed draft, not an approved plan.
- HCP-only, adults only, outpatient/non-time-critical. Not for emergencies. Not for patient self-use.

What I'd love: run a synthetic case you know well in the demo and tell me where the regimen logic, the citations, or the red flags are wrong, dated, or missing.

- Demo (synthetic only, runs in-browser, data stays local): https://openonco.info/try.html
- Site: https://openonco.info
- Code: https://github.com/romeo111/OpenOnco

**Disclaimer:** Research/support tool, not a medical device; not FDA-cleared, CE-marked, or clinically validated. Outputs are drafts to be verified by a qualified oncologist. Does not diagnose cancer. HCP-only. Not for time-critical use.

---

## 3. r/LocalLLaMA

**Caution:** This crowd is technical and allergic to hype/marketing and to medical overclaiming. Lead with the engineering angle (deterministic engine, MCP, "stop your LLM hallucinating regimens"), be blunt about maturity, and don't oversell. Avoid words like "revolutionary." Expect hard questions about determinism, the KB, and the licensing — answer them. Keep the medical disclaimer but make it short and matter-of-fact.

**Title:**
A deterministic oncology engine + MCP server so your LLM relays cited, rule-based output instead of hallucinating a chemo regimen

**Body:**

If you've ever watched an LLM confidently invent a cancer drug or a dose, this is an attempt at the opposite pattern: keep the LLM out of the decision entirely and make it a relay over a deterministic engine.

**OpenOnco** is a free, open-source (code MIT, content CC BY 4.0) clinical decision support project for oncology. The relevant bit for this sub:

- **The clinical logic is a deterministic rule engine over a versioned, human-reviewed knowledge base. No LLM picks the regimen or dose.** Because the model isn't choosing, it can't hallucinate a drug or a dose. Same input + same KB version = same output.
- The engine runs **6 deterministic stages** (resolve algorithm → flatten findings → evaluate red flags → walk decision tree → materialize tracks → resolve regimens), ~**50–200 ms** per profile, fully reproducible.
- It runs **locally / offline**: CLI, **in-browser via Pyodide (Python WASM, no backend)**, or Python import. Patient JSON never leaves the machine — no server-side data, no logs, no DB.
- **MCP server** exposes the engine to any Model Context Protocol client (Claude Desktop, Cursor, etc.) with tools `engine_info`, `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief`. The LLM **relays the cited engine output and never selects the regimen itself.** That's the whole point: the model routes the question through deterministic, sourced logic instead of answering from memory.
- Every recommendation carries a source citation, enforced by a 3-layer citation guard (Pydantic referential check → CI paraphrase-grounding verifier → render-time guard that drops/flags uncited cells).

Input is structured FHIR/mCODE-shaped JSON; output is one Plan with two alternative tracks (standard + aggressive) side by side, each with a step-by-step decision trace. No confirmed histology → it returns a diagnostic brief instead of a plan.

Maturity, straight: it's **v0.1**. KB is 92 diseases / 384 regimens / 444 cited sources, but **most entities are STUB** — only 15 of 806 have full two-reviewer clinical sign-off — and there's been **no formal clinical validation.** It's a working pattern and a forkable architecture, not a finished product. Honestly the "engine, not the LLM, owns the decision + MCP-as-relay" pattern is reusable for any safety-critical rules-first domain, which is partly why it's open source.

- MCP server: https://github.com/romeo111/OpenOnco/tree/main/mcp_server
- Repo: https://github.com/romeo111/OpenOnco
- In-browser demo: https://openonco.info/try.html
- `llms.txt`: https://openonco.info/llms.txt

Medical note (this part isn't optional): informational HCP-only CDS tool, **not a medical device**, not validated, outputs are drafts to be verified by a qualified oncologist. Not for patient self-use or time-critical decisions.

---

## 4. r/mcp (primary) / r/ClaudeAI (alternate)

**Caution:** Post the MCP-server angle to **r/mcp** if it fits; r/ClaudeAI is the fallback if you want a Claude-Desktop framing. Both like concrete "here's a real MCP server doing a real job" posts over abstract pitches. Show the tool list and the "model relays, never decides" guarantee. Keep medical claims tight and honest; this audience will notice overclaiming. Don't cross-post the same body to both on the same day.

**Title:**
A real-world MCP server: route oncology questions through a deterministic, fully-cited engine so the model relays answers instead of guessing

**Body:**

Sharing an MCP server that's built around a specific safety idea: **the LLM should never make the call — it should relay output from a deterministic engine, with a citation on every claim.**

**OpenOnco** is a free, open-source oncology clinical decision support project. It ships an **MCP server** that exposes a deterministic rule engine to any MCP client (Claude Desktop, Cursor, etc.). Tools:

- `engine_info`
- `list_diseases`
- `generate_treatment_plan`
- `generate_diagnostic_brief`

How it behaves through MCP: the model passes a structured patient profile to the engine and **relays the engine's cited output verbatim — it does not pick the regimen or the dose.** The clinical logic is a versioned, human-reviewed knowledge base evaluated by deterministic rules, so the same input + same KB version always yields the same plan, and the model can't hallucinate a drug or dose because it isn't the one choosing. `generate_treatment_plan` returns two alternative tracks (standard + aggressive) side by side, each with regimen, contraindications, monitoring, a step-by-step decision trace, and source citations. If histology isn't confirmed, `generate_diagnostic_brief` returns a workup brief instead of a treatment plan.

Why it's a decent MCP case study:
- It's a clean example of **MCP-as-guardrail**: the server constrains the model to relaying sourced, deterministic output rather than free-generating in a high-stakes domain.
- Runs locally — engine is offline-capable, patient data never leaves the machine, no backend.
- Open source: code MIT, content CC BY 4.0. Forkable as a pattern for other rules-first, safety-critical domains.

Honest status: **v0.1 draft.** The KB covers 92 diseases with 444 cited sources, but **most clinical entities are STUB** (only 15 of 806 have two-reviewer sign-off) and there's been **no formal clinical validation.** Use the synthetic demo cases to kick the tires; don't point it at a real patient and trust the output.

- MCP server: https://github.com/romeo111/OpenOnco/tree/main/mcp_server
- Repo: https://github.com/romeo111/OpenOnco
- Try it in-browser (synthetic cases): https://openonco.info/try.html

Disclaimer: informational, HCP-only clinical decision support — **not a medical device**, not FDA-cleared/CE-marked, not clinically validated. All output is a draft to be verified by a qualified oncologist. Not for patient self-use or time-critical decisions.

---

### Cross-posting summary (for the poster)

| Subreddit | Angle | Top risk | Mitigation |
|---|---|---|---|
| r/medicine | Clinician critique of a free CDS tool | Removal for self-promo | Message mods first; self-post; critique-led; verified flair |
| r/oncology | Two cited tracks, rules-first | STUB/validation skepticism | Lead clinical, answer caveats plainly |
| r/LocalLLaMA | Deterministic engine + MCP vs. hallucinated regimens | Hype/medical overclaim allergy | Engineering-led, blunt maturity, short disclaimer |
| r/mcp ↔ r/ClaudeAI | Real-world MCP-as-guardrail server | Abstract-pitch fatigue | Concrete tool list + "relays, never decides" |

All four bodies use only fact-sheet figures (state 2026-06-17), the five canonical links, the rules-first/no-LLM-decides differentiator, the STUB maturity caveat, and the required not-a-medical-device + verify-with-oncologist disclaimers.
