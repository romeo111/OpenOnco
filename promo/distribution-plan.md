# OpenOnco Launch & Distribution Plan

**Asset type:** Prioritized, sequenced launch/distribution plan
**Project status:** v0.1 draft, early-stage open-source, actively seeking clinician feedback
**Canonical date for all numbers:** state 2026-07-18 (capabilities page)

> **Read before posting anything.** OpenOnco is an informational clinical
> decision-support resource for healthcare professionals and tumor boards — **not
> a medical device, not FDA-cleared/approved, not clinically validated, not for
> patients, not for emergencies.** Every public post, page, and slide must carry
> the not-a-medical-device disclaimer and the "all recommendations must be
> verified by a qualified oncologist" line. No LLM picks the regimen or dose —
> say so, accurately, in every channel. Most clinical content is **STUB** (only
> 15 of 1061 entities are dual-signed-off); pair every coverage/number claim with
> that maturity caveat. Use only the five canonical links below.

---

## Canonical links (use these only — do not invent URLs)

| Purpose | URL |
|---|---|
| Site | https://openonco.info |
| In-browser demo | https://openonco.info/try.html |
| Repo | https://github.com/romeo111/OpenOnco |
| MCP server | https://github.com/romeo111/OpenOnco/tree/main/mcp_server |
| llms.txt | https://openonco.info/llms.txt |

---

## The one message every channel carries

Rules-first, deterministic oncology decision support: a declarative rule engine
over a versioned, fully source-cited, human-reviewed knowledge base (most content
still **STUB** — not yet dual-reviewer signed off) drafts **two alternative
treatment plans (standard + aggressive) side by side** for a clinician to verify.
**No LLM ever picks the regimen or dose — so it can't hallucinate a drug or a
dose.** Runs locally / in-browser; patient data never leaves the machine. Free
and open source (code MIT, content CC BY 4.0). Early stage — we want clinician
feedback.

---

## How actions are tagged

- **[DRAFT-READY]** — copy/config we can write and stage now; no external posting,
  no outreach. Includes our own repo, our own site, our own social drafts held for
  review.
- **[OUTWARD — needs maintainer go-ahead]** — anything that posts publicly to a
  third-party venue (HN, Reddit, X, LinkedIn), opens a PR to an external
  repo/list, or contacts a person/org. Draft now, **hold until a maintainer
  approves the exact text and timing.**

---

## Priority ranking (leverage vs. effort)

Ordered best-leverage-per-unit-effort first. Effort is rough author-time; leverage
is reach × fit-to-audience × durability.

| # | Action | Leverage | Effort | Tag |
|---|---|---|---|---|
| 1 | Repo readiness pass (README counts, disclaimer, screenshots, demo link, contributing) | High | Low | [DRAFT-READY] |
| 2 | `llms.txt` / machine-readable discoverability check | Med-High | Low | [DRAFT-READY] |
| 3 | MCP server listing in MCP registries / awesome-mcp lists | High | Low-Med | [OUTWARD] |
| 4 | Screenshot + short screencast capture (demo + MCP-in-Claude-Desktop) | High (unblocks everything below) | Med | [DRAFT-READY] |
| 5 | "Awesome" / open-source CDS list submissions | Med-High | Low-Med | [OUTWARD] |
| 6 | MCP community post (Discord/forum) | High (warm, on-topic audience) | Low | [OUTWARD] |
| 7 | Show HN post | High (spiky, durable) | Med | [OUTWARD] |
| 8 | Reddit (dev + selected clinical-informatics subs) | Med | Med | [OUTWARD] |
| 9 | LinkedIn (founder + project) | Med | Low | [OUTWARD] |
| 10 | X/Bluesky thread | Med | Low | [OUTWARD] |
| 11 | Direct clinician / tumor-board outreach for feedback | **Highest strategic value**, slow burn | Med-High | [OUTWARD] |

Rationale for ordering: registries and our own repo/site compound passively and
have no downside, so they go first. The MCP angle is our single most
differentiated, least-crowded distribution surface (an oncology engine an LLM can
*call* instead of guessing) — cheap and high-fit, so it leads the outward push.
HN/social are spikier and riskier on medical framing, so they come after the
assets and disclaimers are locked. Clinician outreach is the **most valuable
outcome** (clinician feedback is the stated #1 contribution we want) but is
slowest and most relationship-dependent, so it runs as a parallel slow track, not
a one-shot launch-day blast.

---

## Phase 0 — Foundation (no external posting)  *[all DRAFT-READY]*
**Timing: Days 1–4. Dependency for every outward action.**

1. **Repo readiness pass.**
   - ~~Reconcile README to canonical counts.~~ **Done 2026-07-18** — README and
     every promo asset were refreshed to the capabilities-page figures:
     **103 diseases, 831 indications (262 first-line, 175 second-line+), 404
     regimens, 321 drugs, 669 red flags, 471 cited sources, 16 virtual MDT
     skills**, and the maturity ratio corrected to **15 of 1061** (it had read
     "15 of 806", which understated the denominator and so overstated how much [figures-frozen]
     of the KB is signed off).
   - Numbers are now single-sourced: run `py -3.12 -m scripts.promo_figures` for
     the canonical block and `--check` to fail on any asset that drifts.
   - Confirm top-of-README carries: one-liner, no-LLM-decides guarantee,
     not-a-medical-device + verify-with-oncologist disclaimer, "v0.1 draft,
     seeking clinician feedback," STUB maturity note (15/1061 dual-signed-off),
     and the demo link.
   - **Fix overclaim in `mcp_server/README.md`.** It currently describes the
     knowledge base as "peer-reviewed clinical content." That overstates maturity
     ("peer-reviewed-validated" is a forbidden claim) and most entities are STUB.
     Reword to "human-reviewed, source-cited clinical content (most entities still
     STUB — not yet dual-reviewer signed off); source guidelines are referenced,
     not redistributed." Keep the existing not-a-medical-device disclaimer there.
   - Confirm license statement: code MIT, specs + generated content CC BY 4.0;
     source guidelines (NCCN, ESMO, EHA, BSH, EASL, Ukraine MoH/NSZU) referenced,
     not redistributed.
   - Confirm `CONTRIBUTING` points AI-tooling contributors at the TaskTorrent
     chunk workflow and states all clinical content is Clinical-Co-Lead reviewed
     before merge.

2. **Discoverability / `llms.txt`.** Verify `https://openonco.info/llms.txt`
   resolves and reflects current scope (synthetic-only examples, HCP framing). It
   already lists canonical URLs and the "synthetic examples only / does not
   replace clinician judgment" framing — good. No new URLs.

3. **Screenshot + screencast capture (HARD DEPENDENCY for #4–#10).** Capture from
   `try.html` using a **synthetic** case only:
   - Two-track plan view (standard vs. aggressive side by side).
   - A visible source citation on a recommendation.
   - The step-by-step decision trace.
   - The "no confirmed histology → Diagnostic Brief" behavior.
   - The MCP server answering inside Claude Desktop/Cursor (engine output relayed
     with citations).
   - Each image/clip must show or be captioned with the disclaimer; never label a
     synthetic case as a real patient.

**Exit criteria for Phase 0:** README counts correct; `mcp_server/README.md`
"peer-reviewed" wording fixed; disclaimers present on repo + site + demo; STUB
caveat visible; screenshots/screencast captured. **Do not start Phase 1 until
these pass.**

---

## Phase 1 — Registries & passive discovery  *[OUTWARD — needs go-ahead]*
**Timing: Days 5–7. Depends on Phase 0.**

1. **MCP registries / `awesome-mcp-servers`.** Submit the MCP server with the
   "route oncology questions through a deterministic, cited engine instead of
   answering from memory" framing and the four tools (`engine_info`,
   `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief`).
   Include disclaimer + "no LLM picks the regimen." **Opens external PRs → needs
   maintainer go-ahead on exact text.**

2. **Open-source / clinical-informatics "awesome" lists.** Identify
   awesome-lists for healthcare-OSS, CDS, or rules engines; prepare one-line
   entries. **External PRs → needs go-ahead.**

These are low-risk, compounding, and seed inbound traffic before any spiky post.

---

## Phase 2 — MCP community (warm, on-topic)  *[OUTWARD — needs go-ahead]*
**Timing: Days 7–9. Depends on Phases 0–1.**

- One post in the MCP community (official Discord/forum, Cursor community).
- Angle: a concrete, safety-first MCP use case — "let your LLM *call* an
  auditable oncology engine instead of guessing; no LLM picks the regimen." Lead
  with the MCP screencast. HCP framing + disclaimer in the post.
- Goal here is qualified developer attention and MCP installs, not volume.

---

## Phase 3 — Show HN  *[OUTWARD — needs go-ahead]*
**Timing: Day 10–12. Depends on Phases 0–2 (especially screenshots + locked disclaimers).**

- **Title (draft):** "Show HN: OpenOnco – open-source, rules-first oncology
  decision support (no LLM picks the treatment)."
- **Body must include, honestly:** what it is (HCP-only CDS, two cited tracks),
  the deterministic/no-LLM-decides differentiator, 3-layer citation guard,
  local/in-browser privacy model, MIT + CC BY 4.0, the demo link, **and** the
  honest maturity statement: v0.1 draft, only 15/1061 dual-signed-off (most
  content STUB), no formal clinical validation study, seeking clinician feedback.
- **Forbidden in the post:** "validated," "FDA-cleared/approved," "diagnoses,"
  "replaces an oncologist," "for patients," "prescribes/calculates doses,"
  "AI picks the treatment."
- Pick a low-traffic morning (US), be present to answer comments, never overclaim
  in replies.

---

## Phase 4 — Broader social  *[OUTWARD — needs go-ahead]*
**Timing: Days 12–16. Depends on Phase 0 assets; sequence after HN so you can reuse the best framing.**

1. **Reddit.** Dev subs (e.g., open-source / self-hosted / MCP-adjacent) and,
   carefully and rules-compliant, clinical-informatics communities. **Read each
   sub's rules first; many ban medical self-promotion.** HCP framing only; never
   post to patient/medical-advice subs.
2. **LinkedIn.** Founder + project post. Best fit for reaching practicing
   oncologists, hematologists, clinical pharmacologists, and MDT leads. Lead with
   the "drafted, fully-cited starting point for tumor boards to verify"
   framing + disclaimer + "seeking clinician feedback."
3. **X / Bluesky.** Short thread reusing the screencast; one differentiator per
   post (no-LLM-decides → two cited tracks → local/privacy → open source →
   feedback ask).

Every post: disclaimer line, HCP-only framing, early-stage honesty, synthetic-data
note on any visual.

---

## Phase 5 — Clinician & contributor outreach (slow track)  *[OUTWARD — needs go-ahead]*
**Timing: starts Day 7, runs continuously for weeks. Parallel to Phases 1–4.**

- **Primary ask:** "Try the in-browser demo on a case you know and tell us
  what's wrong — clinician feedback is the most valuable contribution right now."
  Point to `try.html` and the GitHub issue tracker.
- **Targets:** practicing oncologists/hematologists, tumor-board/MDT leads,
  clinical pharmacologists, oncology-informatics researchers. (Use the
  partner-outreach approach for tailored messages; keep it HCP-to-HCP, never
  patient-facing.)
- **Framing guardrails:** it is a *draft to verify*, not a recommendation; not a
  replacement for an oncologist or a tumor board; STUB content is "proposed, not
  approved."
- **AI-tooling contributors:** invite them to the TaskTorrent chunk workflow
  (draft structured sidecars → PR; no clinical expertise needed to *trigger*
  drafting; all clinical content reviewed by Clinical Co-Leads before merge).

---

## Suggested launch sequence (one line)

**Phase 0 foundation (repo + disclaimers + screenshots)** → **registries + awesome-lists** → **MCP community** → **Show HN** → **Reddit / LinkedIn / X** → **clinician outreach (parallel, ongoing)**.

---

## Dependencies (explicit)

- **Screenshots/screencast (Phase 0 #3) gate every social/community post (Phases 2–4).** Do not post visuals you haven't captured from synthetic cases.
- **README count reconciliation + `mcp_server/README.md` wording fix (Phase 0 #1) gate all numeric and maturity claims everywhere.** Quote 2026-07-18 capabilities figures, not README's older numbers; do not let any linked asset say "peer-reviewed."
- **Disclaimers + STUB caveat locked (Phase 0) gate all outward posting.** No public post before the medical-safety framing is verified on repo, site, and demo.
- **HN (Phase 3) before broad social (Phase 4)** so the best-tested framing/Q&A can be reused; but HN is *not* a prerequisite for registries or MCP-community.
- **Registries/awesome-lists and MCP community first** so inbound has somewhere credible to land before any spike.
- **All [OUTWARD] items require maintainer sign-off on exact wording + timing** before they go live.

---

## Success metrics

Track against the project's actual goal — clinician feedback first, reach second.

**Primary (what we actually want):**
- **Clinician feedback issues / emails:** count of substantive feedback items
  from self-identified HCPs (target: first 5 within 2 weeks of clinician
  outreach; 15 within 6 weeks). This is the headline success signal.
- **Qualified clinician demo sessions:** outreach replies that confirm they ran a
  case on `try.html`.

**Secondary (reach / adoption):**
- **GitHub stars & forks:** baseline at Phase 0; watch the Show HN / MCP-community
  spike. Forks matter more than stars given the "forkable pattern" positioning.
- **MCP installs / config adoption:** registry listing clicks, repo traffic to
  `mcp_server/`, mentions in MCP community.
- **Site traffic:** unique visitors and `try.html` sessions; track per-channel
  referrers (registry vs. HN vs. Reddit vs. LinkedIn) to see which channel sends
  *qualified* HCP traffic, not just volume.
- **Contributor signal:** TaskTorrent chunk PRs opened by new contributors.

**Guardrail metric (must stay clean):**
- **Zero medical-overclaim incidents** — no post, reply, or list entry that says
  validated / FDA-cleared / diagnoses / replaces an oncologist / for patients /
  prescribes doses / AI-picks-treatment / peer-reviewed-validated. Audit each
  outward post against the forbidden-claims list before publishing. A single
  overclaim is a bigger failure than a slow week of stars.

---

## Pre-publish checklist (run on every outward asset)

- [ ] Not-a-medical-device disclaimer present.
- [ ] "Verified by a qualified oncologist" line present.
- [ ] HCP / tumor-board framing — not patients, not caregivers.
- [ ] "v0.1 draft, seeking clinician feedback" stated or clearly implied.
- [ ] Any coverage/number paired with the STUB caveat (15/1061 dual-signed-off).
- [ ] Numbers match the 2026-07-18 capabilities figures.
- [ ] "No LLM picks the regimen/dose; deterministic + cited" stated accurately.
- [ ] Any visual uses synthetic data and is not labeled as a real patient.
- [ ] Only the five canonical links used.
- [ ] No forbidden claim (validated / FDA / diagnoses / replaces oncologist /
      patient-use / prescribes-doses / AI-picks-treatment / peer-reviewed-validated /
      OncoKB-SNOMED-MedDRA as sources).
- [ ] Maintainer signed off on exact wording + timing (for [OUTWARD] items).

---

*OpenOnco is an informational clinical decision-support resource for healthcare
professionals — **not a medical device**, not FDA-cleared/approved, and not
clinically validated. All recommendations must be verified by a qualified
oncologist. v0.1 early-stage open-source draft; examples are synthetic.*
