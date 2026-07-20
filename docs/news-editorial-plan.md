# News: length, cadence, and what to publish next

Companion to `docs/news-comments-setup.md`, which covers the mechanics.

## Two kinds of post

Set `kind:` in the YAML. It defaults to `project`.

**`project`** — what changed in OpenOnco and why. Everything published so far.
Claims are about our own commits, so the commit is the evidence and citations
are optional.

**`explainer`** — background on cancer biology, or on how the clinical
literature and guidelines actually work. These assert things about the world,
not about our repository, so two things are enforced by the build:

- **`sources:` is mandatory** and the build fails without it. Each entry needs
  a `citation` and an `id` (PMID, DOI or URL); bare PMIDs and DOIs are turned
  into links automatically. This is CLINICAL_CONTENT_STANDARDS applied to
  editorial content — a claim about cancer biology on a public medical site
  needs the same grounding as a claim in the knowledge base.
- **A standing note** appears above the body saying this is background reading
  rather than clinical guidance, and that cited studies may have been
  superseded. Someone arriving from search at a page about tumour biology
  should not have to infer that.

Explainers are also badged on the index so they are not mistaken for release
notes.

**Where the line is.** An explainer describes published research. It does not
tell a reader what to do about their own case, does not compare named drugs as
better or worse, and does not turn a mechanism into an implication for
treatment. If a draft starts doing that, it is no longer editorial content and
belongs in the knowledge base, behind CHARTER §6.1 two-reviewer signoff.

Prefer topics where the honest finding is a limitation — how evidence grades
are misread, why a cell-line result may not transfer, where precision oncology
underdelivered. Those are useful to a clinician and carry little risk of being
read as advice.

## How long a post should be

Three tiers. Word counts are **per language** — every post ships EN and UA.

| Tier | Length | Use it for | How often |
|---|---|---|---|
| **Note** | 60–150 words, 2–4 blocks | A single fix, a data refresh, a small release. One `p`, maybe one `ul`. | As needed |
| **Standard** | 250–500 words, 6–10 blocks | A workstream landing, a fix with a lesson, a KB wave digest. **This is the default.** | Most posts |
| **Milestone** | 700–1,200 words | A pivot, a governance decision, a published audit. Rare — 3–4 a year. | Rarely |

The eight posts now live run 220–330 words. That is correctly calibrated; the
risk over time is drift upward, not that they are too short.

**Why not longer.** Nielsen Norman Group's log and eye-tracking work finds
readers consume roughly 20–28% of the words on a page, and that each additional
100 words buys about 4.4 seconds of extra attention — meaning the marginal 300
words of a 900-word post are mostly unread. The SEO advice that a post should
run 1,500–2,500 words measures ranking correlation on commercial keywords and
does not apply here: this page is not an acquisition channel, and its readers
arrive already on the site or from a colleague's link.

**What readers actually punish is vagueness, not brevity.** The largest study of
release notes in practice (Bi, Xia, Lo, Grundy & Zimmermann, IEEE TSE — 32,425
release notes across 1,000 projects, plus 314 survey respondents) found
"appropriate length" to be the single highest-agreement point between the people
who write release notes and the people who read them. The dominant user
complaint is not that notes are short — it is "bug fixes and performance
improvements," which says nothing. **Short and specific is the target; short and
vague is the failure mode.**

A useful corollary from the same work: major releases are mostly system-level
content (what the project now does), minor ones mostly class-level (what
specific thing changed). Do not write milestone-style prose for a routine data
refresh.

## How often

**Target monthly. Treat a quarter as the floor. Do not promise weekly.**

Verified cadences from comparable projects: Home Assistant publishes monthly on
the first Wednesday and has held it for twelve consecutive months; Open Targets
is quarterly, tied to data releases; Bioconductor twice a year; Zotero four to
seven posts a year, event-driven only. Most instructive is cBioPortal — a
well-funded, actively developed cancer-genomics resource that went silent for
five months in 2025 and four months over 2025–26, and suffered no visible
reputational cost. Nobody thinks cBioPortal is dead.

So cadence discipline matters less than it feels like it should. What it
protects is narrower and specific to this project: **recency is a documented
credibility heuristic in health information.** Consumer-health guidance
routinely tells readers to check when a page was last updated. On a site that
renders treatment recommendations, a dormant news page does not read as "the
team is busy" — it reads as "the guidelines behind this may be stale."

There is no study establishing a minimum viable cadence. Anyone claiming one is
selling content marketing.

Two cheap hedges, both worth taking:

- **Say what the schedule is.** A stated cadence converts a gap from "abandoned"
  into "on schedule." Astropy publishes a release calendar for exactly this.
- **Keep the Note tier available.** A 90-word post that says the knowledge base
  grew and one routing bug closed costs twenty minutes and keeps the page alive.
  Assembling release notes is a documented burnout vector for volunteer
  maintainers; the tiering exists so the monthly target is survivable.

## What to publish next

Today is 2026-07-19. Eight posts are live, spanning 2026-04-26 to 2026-07-19,
all but the newest marked as written retrospectively.

### Ready now — merged, verifiable, unwritten

1. **The 161-algorithm clinical audit** (merged 2026-07-15, PR #633; report at
   `docs/reviews/algorithm-clinical-audit-2026-07-11.md`). 23 review agents,
   125 findings, 47 critical/high sent to independent verification: **47
   confirmed, 0 refuted**, 44 of them PubMed-grounded. The strongest available
   story, and it is about the project finding its own faults. Milestone tier.
2. **Nothing clinical was auto-fixed** — the companion story to (1). Of four
   auto-applied edits, the project's own verification pass rejected three. The
   remaining ~38 confirmed findings are deferred because they need clinical
   authoring, not a script. Standard tier. Could merge into (1).
3. **Nine new disease pathways** (merged 2026-07-15, PR #633) — full first-line
   coverage for laryngeal SCC, nasopharyngeal, parathyroid, penile SCC,
   pituitary adenoma, adrenocortical, Kaposi, phaeochromocytoma, and
   vulvar/vaginal SCC; 105 new files, plus two real routing bugs found in the
   process. Standard tier.
4. **Prose conditions wired to structured clauses** (merged 2026-07-15, PR
   #632) — the direct sequel to the 2026-05-17 audit post: 107 algorithms, 90
   clause conversions, dead steps down from 160 to 128. A propose-then-verify
   pipeline caught five real regressions. Standard tier, and it closes a loop
   readers have already seen opened.
5. **Ukrainian terminology: режим/регімен → «схема лікування»** (merged, PRs
   #634/#635) — 313 renames across 315 files, with roughly 78 occurrences
   correctly left alone and three judgment calls escalated to clinical
   reviewers. Genuinely interesting to the Ukrainian audience. Standard tier.

### Triggered — write when the condition is met

| Trigger | Post |
|---|---|
| Comments backend deployed | Note: comments are open, here is how moderation works |
| PR #640 merges | The figure correction: `15 of 806` was wrong, it is `15 of 1061` — the project overstated its own dual-signoff coverage and fixed it |
| PR #641 merges | NSCLC T790M routing fix — but note it is labelled DO NOT MERGE pending two Co-Lead sign-offs |
| A Clinical Co-Lead is appointed | Milestone. Also auto-expires the CHARTER dev-mode exemptions |
| KB coverage Phase 2 lands | Zero-biomarker gap closed across 22 diseases |
| MCP registry / PyPI publish | Note |
| CHARTER §2 / §15-C1 text reconciled with the patient-facing site | Governance post — currently an open contradiction |

### A suggested month

| Week | Post | Tier |
|---|---|---|
| 2026-07-21 | The 161-algorithm clinical audit (items 1 + 2) | Milestone |
| 2026-07-28 | Prose conditions wired — sequel to the May audit | Standard |
| 2026-08-04 | Nine new disease pathways | Standard |
| 2026-08-11 | Ukrainian terminology rename | Standard |
| 2026-08-18 | Whatever landed in August, or a Note | Note |

That front-loads the backlog, then settles to monthly. If only one of these
ships, make it the clinical audit.

## House style

- **State what changed, why it matters, and what is still open.** The third part
  is the one that gets dropped and the one that builds trust.
- **Numbers, verbatim.** Quote the real figure from the audit or commit. Never
  round in a way that flatters.
- **Name what was deliberately not fixed.** Several of the best posts here are
  about a refusal — 35% of profiles would have breached the two-track invariant,
  so the strict fix was rejected.
- **A news post is not a clinical claim.** Say "added regimen X for indication Y
  based on trial Z," never "X is recommended for Y." News lives outside
  `knowledge_base/hosted/content/` precisely so it never enters the CHARTER §6.1
  clinical path — do not let the prose smuggle it back in.
- **Write both languages at once.** The build fails if either is missing, which
  is deliberate: a Ukrainian version added "later" is a Ukrainian version that
  rots.
- **Backfilled posts set `published:`.** The dateline stays the date of the
  event; the page then says the post was written retrospectively, and structured
  data reports the real publication date.
