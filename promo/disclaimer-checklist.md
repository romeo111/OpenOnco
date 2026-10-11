# Pre-publish safety checklist (gate)

> Solo-project clarification, 2026-10-12: external clinical review is optional, not a development or publication requirement. Multi-review counts below are descriptive audit data, not a release quota. Review-count correction: 0/2,570 records have two eligible current content reviews. Historical counters do not establish current authority, scope, revision or reviewer independence. This is not individual treatment approval and does not deny historical clinician feedback. Other dated figures and feature claims in this draft still require verification against [the current fact sheet](00-FACT-SHEET.md) before publication.


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
      diseases / 664 indications / 444 sources", it must also note that most
      content is STUB ("proposed, not approved"; 0/2,570 dual-signed-off).
- [ ] **Numbers are the canonical ones** (capabilities page, state 2026-06-17):
      92 diseases · 664 indications · 384 regimens · 298 drugs · 594 red flags ·
      444 sources · 16 MDT skills. **Not** the README's stale figures.
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
