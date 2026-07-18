# OpenOnco promotion kit

Ready-to-use, **safety-reviewed** assets for promoting OpenOnco. Every asset was
drafted against [`00-FACT-SHEET.md`](00-FACT-SHEET.md) (the source of truth) and
passed an adversarial accuracy/safety review.

## ⚠️ Non-negotiable rules for any public post

OpenOnco is a **medical** tool. Before publishing anything from this kit:

1. **Keep the disclaimer.** Every public-facing asset must say it is an
   **informational decision-support tool, not a medical device**, and that every
   recommendation must be **verified by a qualified oncologist**.
2. **Stay honest about maturity.** It is an **early-stage (v0.1) project** —
   only **15 of 1061** clinical entities have two-reviewer sign-off; the rest are
   STUB (structured + sourced, *not* clinically approved). Never imply it is
   clinically validated, FDA-cleared, or production-ready.
3. **Never claim** it diagnoses cancer, treats patients, replaces an oncologist,
   is for patient self-use, or that an LLM picks the regimen. See the
   `forbidden_claims` in the fact sheet.
4. **Numbers:** never hand-copy them. Run `py -3.12 -m scripts.promo_figures`
   for the canonical block (103 diseases · 831 indications · 404 regimens ·
   471 sources, as of 2026-07-18) and `py -3.12 -m scripts.promo_figures --check`
   before publishing — it fails on any asset still quoting a superseded figure.
   Hand-copying is what let assets ship "92 diseases / 444 sources" for a month, [figures-frozen]
   and a "15 of 806" sign-off ratio whose denominator had grown to 1061. [figures-frozen]

## Contents

| File | Channel / use | Outward action? |
|---|---|---|
| [00-FACT-SHEET.md](00-FACT-SHEET.md) | Source of truth for all copy | internal |
| [press-kit.md](press-kit.md) | One-pager / boilerplate / "what we need" | internal ref |
| [clinician-one-pager.md](clinician-one-pager.md) | Tumor-board handout for the primary audience (print/PDF) | internal ref |
| [faq-objection-handling.md](faq-objection-handling.md) | Canonical answers ("medical device?", "just an LLM?", "STUB safety?") | internal ref |
| [disclaimer-checklist.md](disclaimer-checklist.md) | Pre-publish safety gate — run every asset through it | gate |
| [readme-badges-and-blurbs.md](readme-badges-and-blurbs.md) | Taglines, badges, short/medium/long descriptions, per-audience pitches | internal ref |
| [mcp-registries.md](mcp-registries.md) | Listing entries + steps for MCP directories | **PRs/forms — maintainer** |
| [hacker-news-show-hn.md](hacker-news-show-hn.md) | Show HN post + first comment | **post — maintainer** |
| [reddit-posts.md](reddit-posts.md) | r/medicine, r/oncology, r/LocalLLaMA, r/mcp | **post — maintainer** |
| [social-x-linkedin.md](social-x-linkedin.md) | X thread + LinkedIn post | **post — maintainer** |
| [community-outreach.md](community-outreach.md) | Cold-outreach drafts to orgs/communities | **send — maintainer** |
| [distribution-plan.md](distribution-plan.md) | Prioritized launch sequence + metrics | plan |
| [CRITIQUE.md](CRITIQUE.md) | Completeness critique + top next actions | plan |

## Repo-metadata quick wins (found while preparing this kit)

These are cheap, high-leverage credibility/discoverability fixes:

- **No `LICENSE` file exists.** GitHub shows *no license* even though the project
  is MIT (code) + CC BY 4.0 (content) — this undercuts the "full open source"
  pitch and discourages reuse. Add a root `LICENSE` (MIT, for the code; the
  README already documents the CC BY 4.0 content split). *Licensing is sensitive
  (CLAUDE.md) — confirm the copyright holder line before adding; "OpenOnco
  contributors" is a safe default.*
- **Thin repo topics.** Current: `clinical-decision-support, lymphoma,
  medical-informatics, oncology, open-source`. Add high-traffic discovery tags:
  `mcp`, `model-context-protocol`, `llm`, `ai`, `healthcare`, `cancer`,
  `python`, `precision-medicine`, `civic`. This is the single fastest way to be
  found by the AI/MCP audience.
- **Open Graph image.** `SITE_IMAGE` is currently `None` in `scripts/site_head.py`,
  so social shares have no preview card. A simple branded OG image lifts
  click-through on every X/LinkedIn/Slack share.

## How outward actions are gated

Producing this kit is internal and reversible. **Actual promotion is
outward-facing and is the maintainer's call** — posting to HN/Reddit/X/LinkedIn,
opening PRs to external "awesome" lists, sending outreach, and changing public
repo settings. The [distribution plan](distribution-plan.md) marks each action
`[DRAFT-READY]` vs `[OUTWARD — needs maintainer go-ahead]`.
