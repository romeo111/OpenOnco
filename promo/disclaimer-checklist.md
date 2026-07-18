# Pre-publish safety checklist (gate)

Run **every** public-facing OpenOnco asset through this before it ships — including
short-form ones (tweets, badges, registry blurbs) where caveats are most often
dropped for length.

## Must be TRUE for every asset

- [ ] **Not-a-medical-device disclaimer present** ("informational decision support,
      not a medical device").
- [ ] **"Verify with a qualified oncologist"** (or equivalent) present.
- [ ] **Early-stage frame present** ("v0.1 / early-stage / seeking clinician
      feedback") — not implied as finished.
- [ ] **STUB caveat sits next to any coverage number.** If the asset cites "92
      diseases / 831 indications / 471 sources", it must also note that most
      content is STUB ("proposed, not approved"; 15/1061 dual-signed-off).
- [ ] **Numbers are the canonical ones** (capabilities page, state 2026-07-18):
      103 diseases · 831 indications · 404 regimens · 321 drugs · 669 red flags ·
      471 sources · 16 MDT skills. **Not** the README's stale figures.
- [ ] **Links are the canonical five**: site `openonco.info`, repo
      `github.com/romeo111/OpenOnco`, demo `openonco.info/try.html`, MCP
      `…/tree/main/mcp_server`, `openonco.info/llms.txt`.

## Must be ABSENT (forbidden claims)

- [ ] No "diagnoses / screens for / detects cancer".
- [ ] No "FDA-approved / FDA-cleared / clinically validated".
- [ ] No "replaces your oncologist / the tumor board".
- [ ] No patient-facing "use this to choose your treatment".
- [ ] No "calculates your dose" / per-patient dosing.
- [ ] No "for emergencies / time-critical decisions".
- [ ] No "the AI/LLM chooses the treatment" (it never does).

## Channel-specific

- [ ] **Short-form (X/badges/registry blurb):** if the disclaimer truly won't fit,
      link to a page that carries it; never publish a standalone clinical claim
      without it.
- [ ] **Medical subreddits (r/medicine etc.):** check self-promotion rules; frame
      as a tool seeking clinician critique, not an ad.
- [ ] **Demo media:** show the on-screen disclaimer; use synthetic cases only.

> If any box can't be checked, fix the asset before publishing.
