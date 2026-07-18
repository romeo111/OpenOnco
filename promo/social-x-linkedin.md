# OpenOnco — Social Promotion Asset

> **Posting note (read before publishing):** Every post below must keep its disclaimer line. OpenOnco is informational clinical decision support for healthcare professionals — not a medical device, not for patients, not for emergencies. All engine output is a draft to be verified by a qualified oncologist. Use only the five canonical links. Numbers reflect the capabilities page, state 2026-07-18.

---

## X / Twitter Thread

### Hook (primary)

**1/**
Most "AI for oncology" tools let a language model pick the treatment.

OpenOnco does the opposite: a deterministic rule engine picks from a versioned, source-cited knowledge base. No LLM ever chooses the regimen or dose — so it can't hallucinate a drug.

Built for oncologists & tumor boards. Free + open source. 🧵

**2/**
Here's the flow for a tumor board:

A clinician feeds in a structured patient profile (FHIR/mCODE-shaped JSON). The engine returns ONE plan with at least two alternative tracks side by side — a standard track and a more aggressive track — for the clinician to verify and tailor.

**3/**
Each track ships with: regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim.

Citations aren't optional — a 3-layer guard enforces them. Nothing is unsourced by construction.

**4/**
No confirmed histology? No treatment plan.

Instead the engine returns a Diagnostic Brief with workup steps. It refuses to act outside the FDA non-device CDS envelope it was designed for (CHARTER §15): no raw images/NGS, no per-patient dose math, no time-critical use.

**5/**
Privacy is structural, not a policy line.

The engine is deterministic and runs locally — CLI, in-browser via Pyodide (Python WASM, no backend), or Python import. Patient JSON never leaves your machine. No server-side PHI, no logs, no DB. ~50–200 ms per profile.

**6/**
Honest scope: this is a v0.1 draft.

The engine + a 103-disease, 471-source cited KB are live, but only 15 of 1061 clinical entities have two-reviewer sign-off — the rest are STUB (data + algorithm + sources, not yet dual-signed). It's a proposed plan, not an approved one.

**7/**
You can even route an oncology question through it from your LLM: an MCP server exposes the deterministic engine to Claude Desktop, Cursor, etc. The model relays cited engine output instead of answering from memory.

Code is MIT. Content is CC BY 4.0. Fork it.

**8/**
Try the in-browser demo on a case you know and tell us what's wrong — clinician feedback is the most valuable contribution right now.

🔗 Site: https://openonco.info
▶️ Demo: https://openonco.info/try.html
💻 Repo: https://github.com/romeo111/OpenOnco

For HCPs/tumor boards. Not a medical device; not for patient self-use. Verify all output with a qualified oncologist.

#Oncology #ClinicalDecisionSupport #OpenSource #HealthTech #TumorBoard #Hematology #MedTech #MCP

---

### Alternative hook A (open-source / builder angle)

**1/**
We open-sourced a rules-first clinical decision support engine for oncology (for clinicians & tumor boards).

Deterministic. Fully cited. Runs offline. No LLM picks the regimen or dose — clinical logic is declarative rules over a human-reviewed knowledge base.

Early-stage v0.1; verify output with an oncologist. Code MIT, content CC BY 4.0. 🧵

### Alternative hook B (the "no plan without histology" angle)

**1/**
An oncology decision-support tool (for clinicians, not patients) that *refuses* to give you a treatment plan when histology isn't confirmed — it hands back a diagnostic workup brief instead.

That restraint is the whole point. Meet OpenOnco: rules-first, deterministic, fully source-cited, free + open. Early-stage v0.1 — verify all output with a qualified oncologist. 🧵

---

## LinkedIn Post

**Hook (primary)**

What if your oncology decision-support tool *couldn't* hallucinate a drug — because no language model ever picks the treatment?

That's the design principle behind **OpenOnco**, a free, open-source clinical decision support resource for oncologists, hematologists, and tumor boards.

A clinician feeds in a structured patient profile (FHIR/mCODE-shaped JSON), and a **deterministic rule engine** returns one plan containing at least two alternative treatment tracks side by side — a standard track and a more aggressive track. Each carries its regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. The clinician verifies and tailors; the tool never issues a single binding directive — showing alternatives side by side is a deliberate guard against automation bias.

A few things that make it different:

🔹 **Rules-first, not LLM-first.** All clinical logic lives in a declarative rule engine over a versioned, human-reviewed knowledge base (CHARTER §8.3). Because no LLM chooses the regimen or dose, it cannot invent one.

🔹 **Cited by construction.** Every recommendation ships with a source citation, enforced by a 3-layer citation guard. Actionability evidence comes from CIViC (CC0), with ESCAT tier surfaced as a badge.

🔹 **Private by design.** The engine is deterministic and runs locally — CLI, in-browser via Pyodide, or Python import. Patient data never leaves the device: no backend, no server-side PHI, no logs. (~50–200 ms per profile; same input + same KB version = same output.)

🔹 **Scoped honestly.** Designed to meet FDA non-device CDS criteria (CHARTER §15). No confirmed histology → no treatment plan; the engine returns a diagnostic workup brief instead. It excludes raw image/NGS input, per-patient dose calculation, pediatrics, direct-to-patient use, and time-critical decisions.

🔹 **Composable.** An MCP server exposes the engine to any Model Context Protocol client (Claude Desktop, Cursor, etc.), so a model can relay cited engine output instead of answering from memory.

**Where it stands — honestly:** OpenOnco is a v0.1 draft. The engine and a 103-disease knowledge base (831 indications, 404 regimens, 321 drugs, 669 red flags, 471 cited sources) are live across hematologic and solid-tumor oncology. But only 15 of 1061 clinical entities have completed two-Clinical-Co-Lead sign-off — the rest are STUB: structured data, algorithm, and sources in place, but not yet dual-reviewed. There has been no formal clinical validation study. This is a proposed-plan tool actively seeking clinician feedback, not a validated product.

If you run or sit on tumor boards — or you build safety-critical, rules-first decision-support systems — try the in-browser demo on a case you know and tell us what's wrong. That feedback is the most valuable contribution right now. The code is MIT and the content is CC BY 4.0, so it's also a forkable pattern for any safety-critical domain.

🔗 https://openonco.info
▶️ Demo: https://openonco.info/try.html
💻 Repo: https://github.com/romeo111/OpenOnco

*OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, and not for emergency or time-critical decisions. All recommendations must be verified by a qualified oncologist. Examples use synthetic data only.*

#Oncology #Hematology #ClinicalDecisionSupport #HealthTech #OpenSource #DigitalHealth #TumorBoard #MedicalInformatics #MCP #PrecisionOncology

---

### Alternative LinkedIn hook A (clinician-credibility angle)

Every recommendation in this oncology tool carries a source citation — enforced automatically, so nothing is unsourced by construction. And no language model ever picks the regimen or dose.

Meet **OpenOnco**: a free, open-source, rules-first clinical decision support resource for oncologists and tumor boards. Here's how it works, and where it honestly stands. 👇

### Alternative LinkedIn hook B (health-tech / safety-engineering angle)

In safety-critical AI, the most important design decision is often what you *don't* let the model do.

**OpenOnco** is a free, open-source oncology decision-support engine where the LLM is deliberately kept out of the clinical decision: a deterministic rule engine over a versioned, human-reviewed, fully-cited knowledge base drafts the plans — two alternative tracks side by side — and a clinician verifies. Here's the architecture, and an honest read on its maturity. 👇

---

**Files referenced:** none modified — this is a standalone copy deliverable returned inline per instructions.
