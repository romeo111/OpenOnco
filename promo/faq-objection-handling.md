# OpenOnco — FAQ / objection handling

Canonical answers so messaging stays consistent across HN, Reddit, press, and
outreach. Keep answers honest; never soften the maturity caveats.

### Is this a medical device?
No. OpenOnco is an **informational clinical decision support** resource for
healthcare professionals, designed to meet **FDA non-device CDS** criteria
(CHARTER §15) — it supports a clinician's reasoning and every recommendation must
be independently verified by a qualified oncologist. It is not a medical device,
not for direct patient use, and not for time-critical/emergency decisions.

### How is this different from just asking ChatGPT "what's the regimen?"
A general LLM answers from memory and can confidently fabricate a drug or a dose.
OpenOnco **never lets an LLM pick the regimen or the dose** (CHARTER §8.3). All
clinical logic is a **deterministic rule engine** over a versioned, human-reviewed
knowledge base, and **every recommendation carries a source citation**. The worst
failure mode is a wrong or incomplete *rule* — auditable and fixable — not a
plausible fabrication. (Via the MCP server, an LLM can even *route through* the
engine instead of guessing.)

### Most of the knowledge base is "STUB" — is it safe to use?
Be clear-eyed: only **15 of 806** clinical entities have two-Clinical-Co-Lead
sign-off. The rest are **STUB** — structured data, algorithm, and sources are in
place, but they are **"proposed, not approved."** Treat every output as a *draft to
verify*, never as an approved plan. This is exactly why the project is asking for
clinician feedback. Do not use STUB content as a clinical recommendation without
independent verification.

### Is it FDA-approved or clinically validated?
No. There has been **no formal clinical validation study** and no real-world
deployment validation (CHARTER §13). "Designed to meet FDA non-device CDS criteria"
is a **design goal**, not a clearance or certification.

### Does patient data leave my machine?
No. The engine is deterministic and runs **locally** — CLI, in-browser via Pyodide
(Python WASM, no backend), Python import, or the MCP server. Patient JSON never
leaves the device; no server-side PHI, no logs, no database. The public site uses
**synthetic examples only**.

### Can patients use it to decide their own treatment?
No. It is **HCP-only**, adults only, for outpatient/non-time-critical planning. It
does not diagnose, screen for, or detect cancer. Patients should always work with
their treating oncologist.

### Does it replace the tumor board or the oncologist?
No. It produces a **drafted, fully-cited starting point** — always at least two
alternative tracks side by side — for the clinician and tumor board to verify and
tailor. It is the "second pair of eyes that read every guideline at once," not the
decision-maker.

### What does it actually output?
For a confirmed diagnosis: one Plan with ≥2 treatment tracks (standard + aggressive),
each with regimen, supportive care, contraindications, monitoring, a step-by-step
decision trace, and citations. If histology isn't confirmed, it refuses to emit a
treatment plan and returns a **Diagnostic Brief** (workup steps) instead.

### Is it really free / open source? Can I fork it?
Yes. **Code MIT, content & specs CC BY 4.0.** Upstream guidelines (NCCN, ESMO, EHA,
BSH, EASL, Ukraine MoH/NSZU, etc.) are referenced, not redistributed. It's
explicitly designed to be forked and reused for other safety-critical
decision-support domains.

### How can I help?
- **Oncologists/hematologists:** run a case you know cold in the
  [demo](https://openonco.info/try.html) and open an issue with what's wrong — a
  missing contraindication, a bad track split, a citation that doesn't support its
  claim. This is the most valuable contribution.
- **Become a Clinical Co-Lead** to dual-sign content out of STUB (the real
  bottleneck).
- **Developers:** the engine + MCP server are open; PRs welcome.

### Why these diseases / why the Ukrainian roots?
The project began from a real treatment-planning need and has Ukrainian clinical
roots (specs and content carry UA originals); coverage spans lymphoid + myeloid
hematology and major solid tumors and is growing.

---
*OpenOnco is an informational decision-support tool, not a medical device. All
recommendations must be verified by a qualified oncologist.*
