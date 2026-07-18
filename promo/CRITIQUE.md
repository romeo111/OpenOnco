# Completeness critique of the promotion kit

The promotion kit asset files (press-kit.md, etc.) do not exist on disk in this worktree or elsewhere in the repo — `find` returned no matches. They are described only in the brief. My job as completeness critic is to assess the kit at the spec/coverage level using the fact sheet and the kit manifest provided in the brief, which I have in full. I don't need the file bodies to assess channel/audience coverage, cross-asset consistency risks, and next actions — that analysis works off the asset list, the fact sheet's audiences/claims/safety rules, and what a complete launch kit should contain.

I have everything needed. Here is the assessment.

---

# OpenOnco Promotion Kit — Completeness Critique

## Scope note
The 8 asset files named in the brief are not present on disk in this worktree (confirmed via repo-wide `find`); I assessed against the fact sheet, the asset manifest, and standard launch-kit completeness rather than the rendered copy. Gaps below are at the channel/audience/consistency level, which the manifest fully supports.

## Channel & audience coverage

**Covered well:** press, Show HN, Reddit, X/LinkedIn, MCP registries, community outreach, README, and an overarching distribution plan. Good HCP + builder + AI-tooling spread.

**High-leverage gaps:**
1. **Clinician / academic channels — the primary audience is underserved.** The kit leans developer/social. Missing: a one-page **clinician-facing PDF flyer / tumor-board handout**, and an outreach track to **oncology societies, residency programs, and hem/onc Twitter(X) KOLs**. The #1 user (oncologists running tumor boards) has no asset in their native format. This is the biggest gap.
2. **No demo media.** No **short screencast/GIF/Loom** of the in-browser `try.html` demo. Every channel (HN, Reddit, X, README) converts far better with a 30–60s demo. Single highest-ROI missing artifact.
3. **No email / direct-outreach templates** for the `partner-outreach` motion — cold emails to clinical advisors (recruiting Co-Leads is the actual bottleneck, given 15/1061 sign-off) and to potential institutional pilots.
4. **No `llms.txt` / AI-discoverability asset treatment** despite it being a canonical link — worth a dedicated "be cited by LLMs" angle given the MCP differentiator.
5. **No FAQ / objection-handling doc** ("is this a medical device?", "how is this not just an LLM?", "STUB — so is it safe?"). This will be asked on HN/Reddit and should have canonical answers to keep messaging consistent.
6. **Contributor onboarding (TaskTorrent chunk workflow)** is named as an audience but has no standalone "how to contribute" recruitment asset beyond community-outreach.

## Cross-asset consistency risks
- **KB number drift is the top risk.** The fact sheet itself flags README using stale counts (420 indications / 377 sources / 140 algorithms) vs canonical (664 / 444 / capabilities-page, state 2026-06-17). `readme-badges-and-blurbs.md` is the one asset with `all_clear=false` — almost certainly the stale-numbers issue. **Numbers must be single-sourced** (ideally generated from the capabilities page) or they will diverge again at the next refresh. [figures-frozen]
- **"471 sources" vs "103 diseases" pairing** must be uniform across assets; approved_claims fixes the canonical pairing — verify every asset uses it verbatim.
- **STUB caveat placement** — safety_rules require pairing every coverage/number claim with the STUB caveat. Headline-grabbing numbers on social/HN are exactly where this caveat gets dropped. Needs an explicit per-asset check.

## Medical-safety framing
Cannot verify presence in each rendered asset (files absent), but the structural risk: safety_rules require the **not-a-medical-device disclaimer + "verify with a qualified oncologist"** on *every* public asset including slides, social posts, and badges. Short-form assets (X posts, badges, registry blurbs) are where disclaimers are most often omitted for length. **Recommend a disclaimer-presence checklist gate** before any asset ships.

## Early-stage honesty
The fact sheet enforces this well (v0.1, "seeking feedback", no validation, STUB). Risk concentrates in **press-kit headlines and social hooks**, where "103 diseases, deterministic, cited" reads as a finished product. Every asset needs the explicit "early-stage, actively seeking clinician feedback" frame, not just the long-form ones.

---

## TOP 5 next actions (priority order)

1. **[OUTWARD] Record a 30–60s demo screencast/GIF of `try.html`** on a known case (e.g. DLBCL), showing the two-track output + citations + decision trace + disclaimer. Needs the maintainer to record/approve real UI. Unlocks higher conversion on every existing asset. *Highest ROI, only maintainer can produce.*
2. **[DRAFT-READY] Fix README number drift + establish a single source of truth for KB counts.** Resolve the one `all_clear=false` asset; make counts reference capabilities-page figures (state 2026-07-18) and add a note/script so future daily refreshes don't re-introduce drift. *Blocks credible launch; fully draftable now.*
3. **[DRAFT-READY] Create a clinician one-pager + FAQ/objection-handling doc.** PDF tumor-board handout (clinician-native format) plus canonical Q&A ("medical device?", "just an LLM?", "STUB safety?") to keep messaging consistent across HN/Reddit/press. Closes the primary-audience and consistency gaps together. *Draftable from fact sheet.*
4. **[DRAFT-READY] Add a disclaimer + STUB-caveat + early-stage compliance checklist and run every asset through it.** A short gate doc: each asset must carry not-a-medical-device + verify-with-oncologist + early-stage frame + STUB caveat on any number. Catches the safety/honesty omissions that short-form assets invite. *Pure drafting.*
5. **[OUTWARD] Draft + send clinical-advisor / Co-Lead recruitment outreach.** Email templates targeting oncology societies, residency programs, and hem/onc KOLs — the 15/1061 sign-off bottleneck is the real maturity constraint, so recruiting reviewers is more leveraged than top-of-funnel reach. Templates are draftable; sending and target selection need the maintainer. *Use the `partner-outreach` skill to draft.*

---
**Note:** If you want me to actually critique the rendered copy (disclaimer presence per asset, exact number drift, claim-by-claim compliance), point me at the directory where the 8 `.md` files live — they are not in `C:\Users\805\cancer-autoresearch` or its worktrees.
