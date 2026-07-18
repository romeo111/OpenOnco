# Blog post draft — "Why we built an oncology decision-support tool that *forbids* the LLM from choosing treatment"

*A publishable technical/founder post for dev.to, Hashnode, Medium, or a LinkedIn
article. ~900 words. Post it yourself, disclosed as the maintainer. Keep the
not-a-medical-device + early-stage framing intact. Swap in a real demo
GIF/screenshot where marked.*

---

## TL;DR

[OpenOnco](https://openonco.info) is a free, open-source clinical decision
**support** tool for oncology tumor boards. You give it a structured patient
profile; a **deterministic rule engine** over a versioned, fully source-cited
knowledge base drafts two alternative treatment plans — standard and aggressive,
side by side — for a clinician to verify. The deliberate, load-bearing design
choice: **no large language model ever picks the regimen or the dose.** Code is
MIT, content is CC BY 4.0, and there's an MCP server so your AI assistant can
*call* the engine instead of guessing.

> Informational support, **not a medical device**, not FDA-cleared, not clinically
> validated. Early-stage (v0.1), most content is draft pending clinician
> sign-off. Every recommendation must be verified by a qualified oncologist.

## The problem

Picking a regimen for one real cancer patient is hours of careful desk work:
open the NCCN PDF, cross-check ESMO, re-read the local protocol, verify the
biomarker is actually actionable, check renal/hepatic dose adjustments, layer
supportive care, confirm contraindications, remember prophylaxis. Every patient.
One missed contraindication can be fatal. And this burden falls hardest exactly
where specialist tumor boards are scarce — rural care and lower-resource health
systems.

The obvious 2026 temptation is to ask a general-purpose LLM "what's the regimen?"
That is the one thing I decided the system must **never** do.

## Why not just let the model decide?

In most domains, a confidently-wrong answer is an annoyance. In oncology, a
hallucinated drug or a plausible-but-wrong dose can kill someone. "The model
sounded sure" is not an acceptable failure mode. So the hard rule became:

- An LLM may write prose, draft code, and help extract structured data from
  documents (with human review).
- An LLM may **not** choose a regimen, a dose, or how to interpret a biomarker
  for treatment selection.

Those decisions come only from declarative rules authored and reviewed by
clinicians, over a versioned knowledge base.

## How the engine works

A patient profile (FHIR/mCODE-shaped JSON: disease, biomarkers, findings,
demographics) goes through six deterministic stages — resolve algorithm →
flatten findings → evaluate red flags → walk the decision tree → materialize
tracks → resolve regimens — in ~50–200 ms. The output is a plan with **at least
two alternative tracks side by side**, each carrying its regimen, supportive
care, contraindications, monitoring schedule, a step-by-step decision trace, and
**a source citation on every recommendation**. If histology isn't confirmed, it
refuses to emit a treatment plan and returns a diagnostic workup brief instead.

Three properties fall out of "rules-first":

1. **It can't hallucinate a drug or a dose.** The worst failure is a wrong or
   incomplete *rule* — auditable and fixable in the open — not a confident
   fabrication.
2. **It's reproducible.** Same input + same knowledge-base version → same plan.
3. **Everything is cited**, enforced by a three-layer citation guard (at load,
   in CI, and at render time). Nothing is unsourced by construction.

Biomarker actionability comes from the openly-licensed CIViC knowledgebase;
intake follows FHIR + mCODE; and it deliberately avoids license-gated
terminologies in favor of open standards (LOINC, ICD-O-3, RxNorm, CTCAE).

*[Insert a 10–20s GIF of try.html generating a DLBCL plan with citations here.]*

## Where the LLM *does* belong: as a caller, not a decider

There's an [MCP server](https://github.com/romeo111/OpenOnco/tree/main/mcp_server)
so any Model Context Protocol client (Claude Desktop, Cursor, …) can call the
engine — `engine_info`, `list_diseases`, `generate_treatment_plan`,
`generate_diagnostic_brief` — and relay its cited output. The assistant becomes a
transport for a deterministic engine's answer, not the source of the answer. It
also runs offline / in-browser via Pyodide, so patient data never leaves the
device.

## Privacy and positioning

The engine runs locally — CLI, in-browser, Python import, or MCP — so there's no
server-side PHI, no logs, no database. The public site uses synthetic examples
only. It's positioned as informational, non-device clinical decision support for
healthcare professionals.

## Honest about where it is

This is early-stage. ~103 diseases and 471 cited sources are in, but **most
content is STUB — "proposed, not approved":** only a small fraction has passed
two-reviewer clinical sign-off, and there's been no formal clinical validation
study. I'm publishing it precisely to get clinicians to tear the logic apart.

## How you can help

- **Oncologists / hematologists:** run a case you know cold in the
  [demo](https://openonco.info/try.html) (synthetic only, nothing leaves your
  browser) and [open an issue](https://github.com/romeo111/OpenOnco/issues) with
  what's wrong — a missing contraindication, a bad track split, a citation that
  doesn't support its claim. That's the most valuable contribution right now.
- **Become a Clinical Co-Lead** to dual-sign content out of STUB.
- **Developers / builders:** the engine + MCP server are open and meant to be
  forked for other safety-critical decision domains. PRs welcome.

Repo: <https://github.com/romeo111/OpenOnco> · Site: <https://openonco.info>

*OpenOnco is an informational clinical decision support tool, not a medical
device. Every recommendation must be verified by a qualified oncologist.*
