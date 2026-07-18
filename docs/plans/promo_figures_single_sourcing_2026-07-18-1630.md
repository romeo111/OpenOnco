# Promo/README KB figures were stale — and understated review maturity

**Created:** 2026-07-18-1630
**Status:** DONE in this branch
**Gate:** none — documentation and tooling only
**Origin:** gallery audit on `claude/gallery-examples-outdated-eb7f06`

---

## 1. The defect

Every outward-facing asset quoted knowledge-base figures from a 2026-06-17
snapshot. The KB had grown substantially since.

| Figure | Was | Now |
|---|---|---|
| Diseases | 92 | **103** |
| Indications | 664 | **831** (262 first-line, 175 second-line+) |
| Treatment regimens | 384 | **404** |
| Drugs (ATC/RxNorm) | 298 | **321** |
| Red flags | 594 | **669** |
| Cited sources | 444 | **471** |
| Diseases with full modeled chain | 77 of 92 | **86 of 103** |
| Two-reviewer sign-off | 15 of **806** | 15 of **1061** |

### The last row is the one that matters

The others understate scale, which is merely unflattering. The sign-off ratio
understates the **denominator** — so it overstates how much of the knowledge
base has passed two-reviewer clinical sign-off: 1.9% claimed versus 1.4% actual.

That figure appears in roughly ten places in outreach copy, always inside the
project's honest-maturity disclosure — the sentence whose entire purpose is to
avoid overclaiming. `promo/disclaimer-checklist.md` treats it as a pre-publish
safety gate. Of all the stale numbers, this is the one that was actively
misleading in the project's favour.

### Where it came from

`promo/README.md` designated the capabilities page as canonical and instructed
copywriters to hand-copy from it. Hand-copying is why 18 files drifted together.

`promo/CRITIQUE.md` had already diagnosed this exactly: *"KB number drift is the
top risk … Numbers must be single-sourced (ideally generated from the
capabilities page) or they will diverge again at the next refresh."* The
diagnosis was right and had not been acted on.

---

## 2. What was done

**`scripts/promo_figures.py`** (new) reads the figures straight off the live KB:

```
py -3.12 -m scripts.promo_figures            # canonical block
py -3.12 -m scripts.promo_figures --check    # non-zero exit if promo/ is stale
```

It delegates to `knowledge_base.stats.collect_stats` for the sign-off ratio and
the full-chain count, so it cannot diverge from what the site itself renders.
(Counting `coverage_status` from raw YAML yields 0 — it is a derived attribute,
which is the kind of subtlety that makes hand-copying fail.)

**109 figure updates across 18 files** — all of `promo/*.md` plus `README.md`.
`promo/README.md` now instructs running the script rather than hand-copying.

### The check had to be rebuilt once

The first version matched fixed phrases ("92 diseases"). It passed while
`promo/press-kit.md` still carried a stale table, because markdown tables put
the label *before* the number:

```
| Diseases covered | **92** (77 with a full modeled chain, rest partial) |
| Cited sources | **444** |
```

Worse, the first pass had already updated that table's *date stamp* to
2026-07-18 while leaving the 2026-06-17 numbers — stale figures presented as
current, the worst possible outcome. The check now matches a bare number
anywhere on a line that also mentions the thing being counted, which catches the
table form. Re-running it immediately found two more (`444-source`, a hyphenated
compound the phrase list also missed).

Self-tested: planting `**444**` back into the press-kit table makes `--check`
exit 1 and name the line.

### Audit-trail lines are frozen, not rewritten

Three lines record what a *past* review verified. Rewriting their numbers would
falsify the record, so they keep the old figures and carry a `[figures-frozen]`
marker that `--check` skips:

- `promo/CRITIQUE.md` — the drift diagnosis quoted above
- `promo/clinician-community-outreach-playbook.md` ×2 — reviewer notes stating
  which figures a past pass verified

The same marker is used on the two new lines that deliberately quote the old
numbers to explain why the guard exists.

---

## 3. Deliberately not changed

**KB content.** Nothing under `knowledge_base/hosted/content/` was touched; the
figures were always correct there. This was purely a reporting-layer drift.

**The "16 virtual MDT clinician skills" figure.** `collect_stats` reports
`skills_count: 0` alongside `skills_planned_roles: 16`, and the capabilities
page renders 16. The promo copy says "16 virtual MDT clinician skills", which
matches the page but may overstate what is implemented. Left as-is —
reconciling it is a product-claim question for the maintainer, not a number
refresh.

---

## 4. Follow-up

Wire `py -3.12 -m scripts.promo_figures --check` into CI or the pre-commit hook
so the drift cannot silently return. Not done here because it would change
repo-wide CI behaviour, which is the maintainer's call.
