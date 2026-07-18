# Show HN: OpenOnco

## Title

```
Show HN: OpenOnco – Rules-first, source-cited oncology decision support (no LLM picks)
```

## Body

```
OpenOnco is a free, open-source clinical decision support resource for oncology
tumor boards. A clinician feeds it a structured patient profile (FHIR/mCODE-shaped
JSON: disease, biomarkers, findings, demographics), and a declarative rule engine
returns one Plan with at least two alternative treatment tracks side by side — a
standard track and a more aggressive track — each with regimen, supportive care,
contraindications, monitoring, a step-by-step decision trace, and a source citation
on every claim.

The thing I most want feedback on is the architecture, because it's a deliberate
bet on what *not* to let an LLM do.

No LLM ever picks the regimen or the dose. All clinical logic lives in a
deterministic rule engine reading a versioned, human-reviewed knowledge base
(CHARTER §8.3). Because no model is choosing the treatment, the engine cannot
hallucinate a drug or a dose — the worst failure mode is a wrong or incomplete
rule, which is auditable and fixable, not a confident fabrication. Same input +
same KB version = same output.

How the engine works — six deterministic stages per profile (~50-200 ms):
resolve algorithm → flatten findings → evaluate red flags → walk decision tree →
materialize tracks → resolve regimens. If histology isn't confirmed, it refuses to
emit a treatment Plan and returns a Diagnostic Brief (workup steps) instead.

Design choices that fall out of "rules-first":
- Every recommendation carries a source citation, enforced by a 3-layer citation
  guard (Pydantic referential check on load, a CI verifier for paraphrase
  grounding, and a render-time guard that warns or drops uncited cells). Nothing
  is unsourced by construction.
- It always shows at least two tracks side by side, never a single "system
  prescribes X" directive — an explicit anti-automation-bias choice (CHARTER §15.2 C6).
- Runs locally: CLI, in-browser via Pyodide (Python WASM, no backend), Python
  import, or an MCP server. Patient JSON never leaves your machine — no server-side
  PHI, no logs, no DB. The public site uses synthetic examples only.
- Actionability evidence comes from CIViC (CC0, WashU), read from a local nightly
  snapshot; ESCAT tier shows as a badge. (OncoKB was rejected — its ToS conflicts
  with the project's non-commercial scope.)

There's also an MCP server (tools: engine_info, list_diseases,
generate_treatment_plan, generate_diagnostic_brief) so any MCP client — Claude
Desktop, Cursor — can route an oncology question through the deterministic engine
and relay cited output, instead of answering from memory. The model never picks the
regimen; it's a transport for the engine's result.

Current scope (capabilities page, state 2026-07-18): 103 diseases across lymphoid
and myeloid hematology plus solid tumors, 831 indications, 404 regimens, 321 drugs
(ATC/RxNorm coded), 669 red flags, 471 cited sources, 16 virtual MDT clinician
skills. 86 of 103 diseases have a full modeled chain.

Honest about maturity: this is a v0.1 draft. The big caveat is clinical sign-off —
only 15 of 1061 clinical entities have passed two-Clinical-Co-Lead review. The rest
are STUB: structured data, algorithm, and sources are in place, but they are
"proposed plan, not approved plan." There has been no formal clinical validation
study and no real-world deployment validation.

Licensing: code is MIT, specs and generated content CC BY 4.0. Original guidelines
(NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU, etc.) are referenced, not
redistributed.

Scope limits: it's positioned as an FDA non-device CDS tool (CHARTER §15) —
informational support for healthcare professionals, not a medical device, not for
direct patient use, adults only, outpatient/non-time-critical planning. Not for
emergencies. It does not diagnose, screen for, or detect cancer, and it does not
calculate patient-specific doses. Every plan is a draft to be verified by the
treating oncologist.

Not a medical device. All recommendations must be verified by a qualified
oncologist.

Site: https://openonco.info
Repo: https://github.com/romeo111/OpenOnco
Try it (synthetic cases): https://openonco.info/try.html
MCP server: https://github.com/romeo111/OpenOnco/tree/main/mcp_server

I'd love critique from oncologists and from anyone who's built rules-first
decision-support systems.
```

## First comment (author)

```
Author here. Some backstory on why this is shaped the way it is.

It started from a real situation — helping put together treatment-planning material
for a patient — and the obvious temptation was to just ask an LLM "what's the
regimen?" That's exactly the thing I decided the system must never do. In a domain
where a hallucinated drug or a plausible-but-wrong dose can hurt someone, "the model
sounded confident" is not an acceptable failure mode. So the hard rule became: an
LLM can write prose, draft code, and help extract structured data from documents
(with human review), but it never chooses a regimen, a dose, or how to interpret a
biomarker for treatment selection. Those decisions come only from declarative rules
over a versioned, human-reviewed knowledge base.

That single constraint drives almost every other design choice: deterministic
six-stage engine, reproducible output, a citation required on every claim (enforced
by the loader, CI, and the renderer), two tracks always shown side by side so it
reads as "here are alternatives to weigh," not "here is the answer," and a hard
refusal to emit a plan when histology isn't confirmed.

I want to be very plain about what this is NOT, because HN will (rightly) push on it:
it is not validated, not a medical device, not FDA-cleared, and not a replacement
for an oncologist or a tumor board. It does not diagnose or screen. Most of the
knowledge base is still STUB — only 15 of 1061 clinical entities have two-reviewer
sign-off, so please read everything else as "proposed, not approved." There has been
no formal clinical validation study.

What I'm actually asking for: if you're an oncologist or hematologist, please open
the in-browser demo (https://openonco.info/try.html — synthetic cases only, no PHI,
nothing leaves your browser), run a case you know cold, and tell me where it's wrong
— a missing contraindication, a bad track split, a citation that doesn't support the
claim, a red flag it should have raised. Tearing the clinical logic apart is the
single most valuable contribution right now.

And if you build rules-first / safety-critical decision systems: I'd genuinely like
critique of the engine and the citation-guard approach. The whole thing is meant to
be forkable for other domains (code MIT, content CC BY 4.0).

Not a medical device. All recommendations must be verified by a qualified oncologist.
```
