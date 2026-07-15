# OpenOnco — for oncologists & tumor boards

*A one-page handout for the primary audience. Print/PDF-friendly. Keep the
disclaimer on any version that leaves your hands.*

## A drafted, fully-cited treatment plan — that you verify, not obey

You feed OpenOnco a structured patient profile (disease, biomarkers, findings,
demographics). A **deterministic rule engine** returns **two alternative treatment
tracks side by side** — a standard track and a more aggressive track — each with:

- the regimen, supportive care, contraindications, and monitoring schedule,
- a **step-by-step decision trace** showing *why* each track was selected,
- a **source citation on every recommendation**, and
- red-flag triggers and a "what not to do" view.

If histology isn't confirmed yet, it returns a **diagnostic workup brief** instead
of a treatment plan — never a plan it shouldn't make.

## Why it's safe to reason with

- **No LLM picks the regimen or dose.** All clinical logic is declarative rules
  over a versioned, peer-reviewed knowledge base — so it **cannot hallucinate a
  drug or a dose**. The output is reproducible: same input + same KB version =
  same plan.
- **Everything is cited** (CIViC for biomarker actionability; NCCN/ESMO/EHA/BSH/
  EASL and others referenced). Nothing is unsourced.
- **Always alternatives, never a directive** — two tracks side by side, by design,
  to support your judgment rather than anchor it.
- **Nothing leaves your device.** It runs in your browser (or locally) — no
  server, no PHI upload, no logs. Public examples are synthetic.

## Honest about where it is

This is an **early-stage (v0.1), open-source** project. Most content is **STUB —
"proposed, not approved"**: structured and sourced, but only a small fraction has
passed two-reviewer clinical sign-off. **Treat every output as a draft to verify.**
We are actively seeking oncologist feedback — that's the whole point right now.

## Try it in 2 minutes (no install, no PHI)

1. Open **https://openonco.info/try.html**
2. Pick a sample case or paste a synthetic profile.
3. Read the two tracks, the trace, and the citations.
4. Found something wrong — a missing contraindication, a bad track, a citation that
   doesn't support its claim? **Tell us:** open an issue at
   https://github.com/romeo111/OpenOnco/issues

Want to help sign content out of STUB? We're recruiting **Clinical Co-Leads**.

---
*OpenOnco is an informational clinical decision support tool for healthcare
professionals — not a medical device, not for direct patient use, and not for
emergencies. Every recommendation must be verified by the treating oncologist with
the full clinical picture. Free & open source (code MIT, content CC BY 4.0).*
