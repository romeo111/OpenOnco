# ⚠️ SUPERSEDED — 2026-04-27

This OncoKB-era decision-record is preserved for historical reference.
OncoKB integration was rejected after Terms-of-Service audit found a fundamental
conflict with CHARTER §2 (free public clinical decision-support). See
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` and
`docs/plans/civic_integration_v1.md`.

---

# OncoKB · Render integration (deferred plan, parked 2026-04-25)

**Status:** parked — not implemented in Phase 10 scaffold. Picks up
after legal-review of OncoKB Academic Terms clears (see
`knowledge_base/hosted/content/sources/src_oncokb.yaml`
`legal_review.status`).

## Goal

Plan-render output (`render_plan_html`) gains a new section:

> **OncoKB precision-medicine layer**
>
> Based on the patient's biomarkers, OncoKB cites the following options
> at evidence level ≥3A. **These are not engine recommendations — they
> are external evidence to consult before finalizing the plan.**
>
> | Biomarker | Level | Drug(s) | OncoKB |
> |---|---|---|---|
> | KRAS G12C | 1 | sotorasib, adagrasib | [→ KRAS G12C](https://www.oncokb.org/gene/KRAS/G12C) |
> | TP53 R175H | 3B | (preclinical) | [→ TP53 R175H](https://www.oncokb.org/gene/TP53/R175H) |

## Surface, not branch

The engine **must not** route Plan tracks based on OncoKB output
(CHARTER §8.3). The render layer reads OncoKB-derived options post-hoc
and lists them alongside the engine's two-track plan, with explicit
language that they are *additional evidence to consult*, not
alternatives ranked by us.

## Wiring

### 1. Engine collects biomarkers

In `generate_plan()`, after the indication is selected, walk
`patient.biomarkers` + `patient.findings` for any (gene, variant)
pair recognizable as a clinically interpretable mutation. Examples:

- `BIO-MYD88-L265P` → ("MYD88", "L265P")
- `BIO-BRAF-V600E` → ("BRAF", "V600E")
- `tp53_mutation: true` (boolean — skip; need specific variant)

Initially, conservative extraction: only triplets that have explicit
gene+variant strings in the biomarker entity's `id` or a new
`oncokb_lookup` field.

### 2. Engine calls proxy

Async fetch to `services/oncokb_proxy/lookup` for each (gene, variant,
oncotree_code) triplet, batched. Failure mode: degrade gracefully — if
proxy is unreachable, render the section with a "OncoKB unavailable"
placeholder + the canonical URLs.

### 3. Render reads result

`render_plan_html` adds a `<section class="oncokb-layer">` after the
two-track plan and before the supportive-care section. Filtering rules:

- Levels **1, 2** are usually already covered by the engine's standard
  algorithm — list but mute styling. They confirm, they don't surprise.
- Levels **3A, 3B** are the interesting signal — highlight these as
  "experimental but partially verified" matches that the engine itself
  doesn't recommend.
- Level **4** — show only if zero higher-level options.
- **R1, R2** (resistance) — show as warnings inline with affected drugs.

### 4. Attribution

Per OncoKB Academic Terms + `src_oncokb.yaml` `attribution.text`, every
plan that surfaces OncoKB content must include:

> Therapeutic-level data sourced from OncoKB™ (Memorial Sloan Kettering
> Cancer Center). Citation: Chakravarty et al. JCO Precis Oncol 2017.

Render this in the section header, not as a footnote — visible to
clinicians on first read.

## Out of scope

- **Auto-promoting** OncoKB options into the two-track Plan. Forbidden
  by CHARTER §8.3 — would make the external KB a clinical decision-maker.
- **Caching at render layer.** Caching lives in the proxy. Render is
  stateless.
- **OncoKB-only patients** (no biomarkers). Section is omitted entirely.

## Acceptance criteria

- For one of the 42 examples — `cll-high-risk` (TP53 mutation) — the
  rendered plan shows an OncoKB section with at least one therapeutic
  level entry + valid OncoKB URL.
- For `chl-early` (no biomarkers) — section is absent from render.
- Snapshot test in `tests/test_oncokb_render.py` locks the rendered
  HTML so accidental changes are caught.

## Sequencing

1. Legal review of `src_oncokb.yaml` clears.
2. Deploy proxy to Cloud Run with `ONCOKB_LIVE=1` + secret.
3. Implement biomarker → (gene, variant) extraction in engine.
4. Plumb proxy fetch into `generate_plan` + `render_plan_html`.
5. Snapshot tests for surfaced sections.
6. Update `MEMORY.md` Roadmap with `[x]`.
