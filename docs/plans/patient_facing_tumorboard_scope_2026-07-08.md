# Scope decision — patient-facing AI Tumor Board (understand-your-plan layer)

**Date:** 2026-07-08
**Type:** §15.3 patient-facing pivot decision (dev-mode §6.1 Initiator-only exemption)
**Initiator:** Project owner
**Status:** Ratified for the v0.1 public site; residual regulatory obligations open (see below)

## Decision

The public site's homepage **Patient / caregiver door** now routes patients into
the free-text **AI Tumor Board** (`ask.html`), pre-seeded to help a patient
**understand a treatment plan their own oncologist already gave them** and
**prepare questions for their next visit**. This is the "explicit patient-facing
pivot" that the 2026-05-18 §3 amendment parked as Path B for "v1.0+ explicit
pivot"; the owner has elected to make a **scoped** version of it now.

## Why this touches the CHARTER

- **§2** states the tool "is not intended for patients / caregivers directly — HCP
  only," and **§15.2 C1** = "HCP-only, never patient-facing; direct-to-patient
  deployment = device (loss of non-device status)." **§15.3** lists "pivot to a
  patient-facing version" as a change requiring a §6 governance review *before*
  implementation.
- `PATIENT_MODE_SPEC` scopes patient mode as a **render-only translation of an
  HCP-authored plan bundle** — it does **not** cover a direct-to-patient free-text
  intake that transmits text to a server. Routing patients into `ask.html` is
  therefore outside the prior reconciliation and is a genuine C1/§15.3 matter,
  independent of data retention (the classification line is about *audience*, not
  storage).

## Scope of what was ratified (and what was NOT)

**In scope now (v0.1):** an *education / question-preparation* patient layer —
"understand your plan, prepare questions for your oncologist." Never a verdict on
a patient's plan, never a treatment recommendation to the patient.

**Still parked (v1.0+, unchanged):** a full direct-to-patient clinical service /
autonomous patient triage. Per §1 (not-in-MVP), that path still requires Clinical
Co-Lead expansion (§4.3), legal-structure formalization (§13), and a separate
regulatory pathway — none of which this decision waives.

## Safeguards implemented alongside the decision

1. Patient-door copy is framed strictly as *understand + prepare questions for
   your oncologist*; the plan-builder ("build your own plan") route was **removed**
   from the patient door (patient self-generation of a plan is more device-like).
2. A not-a-medical-device disclaimer renders under the patient door buttons.
3. `ask.html` gains an additive patient layer: a plain-language "this does not
   replace your doctor; never start/stop/change treatment" banner, a
   de-identification + transmission notice ("text is sent to a server; remove
   name/DOB/IDs; paste only the parts you have questions about"), and two
   patient-voice example prompts. The load-bearing string *"Do not paste real
   identifiable patient data. This is a tumor-board draft, not autonomous medical
   advice."* is preserved verbatim.
4. The `?case=` prefill is a **synthetic, de-identified template** assigned via
   `.value` only; no flow ever places a patient's real pasted plan into a URL.

## Invariant impact

- **§15.2 C4/C6/C7** (≥2 tracks, no automation-bias, histology gate) — unchanged.
- **§15.2 C1** — a **scoped patient-facing education layer** is now ratified;
  the full "direct-to-patient clinical service = device" prohibition remains for
  the parked Path B. §2 / §15.2 C1 prose carries a pointer to this record.

## Honest trade-off note (per the §2.2 pattern)

This decision widens the gap between the CHARTER's "HCP-only" prose and the live
patient-facing site. The owner has accepted this for v0.1 to enable early patient
acquisition, on the basis of the education/question-prep framing and the
safeguards above, and with the data-not-retained posture. It does **not** remove
the regulatory obligations for a full direct-to-patient service, which remain
parked. A full §6 Clinical Co-Lead review is recommended before v1.0.

## Open follow-ups

- Duplicate the not-a-device patient disclaimer onto every patient-reachable
  destination (`gallery.html`, `try.html`) and reconcile "for clinicians" footers.
- Verify the engine maps lay terms in the prefill ("stomach cancer" → gastric).
- Consider a patient-context variant of `ask.html` hiding the "API endpoint"
  field and the clinician "OpenOnco AI draft" kicker.
