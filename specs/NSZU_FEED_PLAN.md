# NSZU Feed — Feature Plan (Live-Feed of NSZU Formulary Changes)

**Status:** v0.1 draft, pre-discovery.
**Owner:** TBD.
**Date:** 2026-04-26.

## Goal and non-goals

**Goal:** a clinician receives a signal about reimbursement changes affecting their active plans, without manual monitoring.

**Explicit non-goals:**
- We do not make decisions for the clinician — signaling only.
- **We do not filter the plan by reimbursement** (CHARTER §8.3 + memory rule `efficacy > registration`: NSZU status is a metadata layer, not a gate. The engine always shows the best-evidence option regardless).
- We do not track actual drug availability at a specific hospital (that is a ProZorro-level concern, a separate pipeline, out of scope).

## P0 — Discovery (required BEFORE the first line of code)

The highest-risk phase. Without honest answers, we are building in a vacuum.

| Question | How to answer |
|-|-|
| Where does NSZU publish the current formulary? (PDF / HTML / open-data CSV) | 2 hours of manual exploration of `nszu.gov.ua` + the open-data portal |
| How often is it updated? Regularly or sporadically? | Same + check `Last-Modified` headers over 3 months |
| Granularity: INN only, or with brand names + dosages? | Inspect the specific PDF of the oncology PMG package |
| Does reimbursement differ by region? | 1 query to NSZU press or a clinical chat |
| What hurts more: "in the formulary" vs "actually in stock at the hospital"? | Question #3 in the interview (below) |

**P0 output:** `specs/NSZU_FEED_DISCOVERY.md` — confirmed cadence + format + risks. If no machine-readable format exists (only scanned PDFs without structure) — reassess feasibility.

## Data sources

**Primary:** Medical Guarantees Programme (PMG), NSZU oncology package.
**Secondary:** Ministry of Health order listing "Available Medicines" (oncology section), if relevant.
**Out of scope:** ProZorro tender data (facility-level stock).

Snapshot storage:
```
knowledge_base/hosted/content/reimbursement/snapshots/
  nszu_2026-04-26.yaml
  nszu_2026-05-03.yaml
  ...
```

One file per date, immutable, validated by the schema loader.

## Schema additions

**`ReimbursementStatus`** (per drug):
```yaml
drug_id: drugbank-DB06317
nszu_program: pmg_oncology_2026
status: reimbursed | restricted | not_listed
restrictions:
  - line_of_therapy: ["1L"]
  - indication_codes: ["C90.0"]
effective_from: 2026-04-26
source_url: https://nszu.gov.ua/...
source_snapshot: nszu_2026-04-26.yaml
```

**`ReimbursementChange`** (diff-derived, not hand-authored):
```yaml
change_id: rc-2026-05-03-darat-loss
drug_id: drugbank-DB06317
from_status: reimbursed
to_status: not_listed
detected_at: 2026-05-03
affected_regimen_ids: [REG-DARA-VRD, REG-DARA-RD]
```

## Mapping: NSZU row → KB Drug

**The most brittle part.** NSZU publishes Ukrainian INN + brand names; the engine operates on `Drug.id` (RxNorm/DrugBank-based).

Approach:
1. **Manual seed:** 50 oncology drugs from active KB Regimens → `knowledge_base/hosted/content/reimbursement/mapping_nszu.yaml`. Two-reviewer merge (CHARTER §6.1) because it affects recommendations.
2. **Test gate:** every `Drug.id` used in an active `Regimen` must have either a mapping or an explicit `reimbursement_status: not_tracked`. Otherwise CI fails.
3. **Unmapped queue:** new NSZU rows without a mapping → `unmapped_log.yaml` → manual review by a Clinical Co-Lead (add / reject).

## Pipeline

```
[ weekly cron job ]
       ↓
1. fetch NSZU sources (HTML + PDF + open-data CSV)
       ↓
2. parse → snapshot YAML (validated by loader)
       ↓
3. diff(today, previous_snapshot) → list[ReimbursementChange]
       ↓
4. for each change:
     - find Regimens that use the affected Drug
     - emit ProvenanceEvent (event_type=reimbursement_change) on patient_id
       (via the existing event_store/append_event)
       ↓
5. publish:
     - knowledge_base/hosted/content/reimbursement/changelog.yaml (source of truth)
     - docs/changelog-nszu.html (public, build_site)
```

**Reuse of existing infrastructure:** `ProvenanceEvent` + `event_store` (commit `98ec53f`). A reimbursement change is a new `event_type` literal; the mechanics are otherwise identical.

## Engine integration

When building a plan, the engine reads the current `ReimbursementStatus` for each `Regimen` and **attaches it as a metadata badge** — it does not exclude non-reimbursed options:

- 🟢 **NSZU** — in the formulary, snapshot date
- 🟡 **restricted** — restriction present (line / indication / dose)
- 🔴 **not in formulary** — patient-pay or application required
- ⚪ **not_tracked** — drug not in our mapping (honest indicator)

**Optional "NSZU-only fallback track":** if a clinician explicitly wants it — a separate button "Show alternative regimen using only reimbursed drugs". Not the default. This is a post-hoc lens, not the primary plan.

## UI / alert surfaces

| Surface | What it shows | Auth required? |
|-|-|-|
| `/try.html` plan output | Badge on each Regimen | No |
| `/changelog-nszu.html` (new) | Public feed of all changes over 12 weeks, filterable by drug/disease | No |
| Per-clinician digest | "Today's change affects 13 of your active plans" | Yes — defer until auth (P3 roadmap) |
| Email digest (lightweight) | Mailto: subscribe form, weekly send | No (manual mail-merge in the transitional period) |

## Phasing

| Phase | Scope | Done-criterion | Estimate |
|-|-|-|-|
| **P0** Discovery | Manual NSZU exploration + 1 clinical interview | `NSZU_FEED_DISCOVERY.md` with confirmed cadence/format | 1-2 days |
| **P1** Scraper + snapshot | One oncology package, manual run | YAML snapshot passes validator | 3-5 days |
| **P2** Mapping seed | 50 drugs + test gate | 100% of active Drugs covered by mapping/not_tracked | 2 days |
| **P3** Engine integration (badge) | Read status, render badge | `/try.html` shows status on each Regimen | 2-3 days |
| **P4** Diff + public changelog | Weekly cron + `/changelog-nszu.html` | Live page updates from cron | 3 days |
| **P5** Fallback-track button | "Show NSZU-only alternative" | UX cycle with 1 clinical tester | 2-3 days |
| **P6** Per-clinician alerts | Email digest / inbox | Defer until auth work | — |

**MVP = P0-P4** (~2 weeks). P5/P6 are separate releases; the feature is useful without them.

## Risks

| Risk | Mitigation |
|-|-|
| NSZU format changed unexpectedly, parser broke | Contract-test on each snapshot. On failure — last-good snapshot stays + UI banner "data is stale as of DATE" |
| Drug-name false-positive matching (brand collision) | Manual mapping with two-reviewer sign-off, not auto-mapping |
| Clinician trusts the NSZU signal and misses a more effective regimen | UI copy: "this is formulary information, not a clinical recommendation". Best-evidence option is always the default |
| "Not available in my region" even though it's in the formulary | Honest: we track the formulary only. Link: "where to check availability at a specific facility" |
| Snapshot history bloats the repo | Diff-only after 8 weeks, full snapshot monthly |
| PDF-only source with no structure | Identify in P0. If so — reassess: the project may become volunteer-driven manual-update rather than automated |
| Conflict with memory rule `efficacy > registration` | Architecturally resolved: metadata layer, not a filter. Engine does not change recommendations based on reimbursement |

## Validation interview (conduct before P1)

One call, **5 questions, 20 minutes:**

1. "How many times **per month** do you revise a plan because of a reimbursement change?" — calibrates priority
2. "How do you find out currently — from the patient, a pharmacy chat, the NSZU website, not at all?" — calibrates channel
3. "What hurts more: an alert about the formulary, or real-time stock at a specific hospital?" — calibrates scope (formulary vs ProZorro)
4. "The engine sees that daratumumab is no longer in the formulary — do you want to automatically see a fallback regimen, or just a warning?" — calibrates autonomy
5. "Would you trust a scraper that might occasionally break — vs checking manually once a week yourself?" — calibrates reliability-vs-effort tradeoff

**Hard kill criterion:** if 2+ clinicians say "less than once a quarter do I revise" — the feature is not worth the effort; put it on the shelf until another signal appears.

## Open questions

1. **Clinical contact for P0?** Without one person to interview before writing code, we risk building in a vacuum.
2. **"Metadata, not filter"** — agree explicitly with Clinical Co-Leads, because architecturally this costs less but filtering would theoretically be possible.
3. **Priority vs roadmap:** P1 (push before other work) or P2 (after patient-registry/auth)?

## Dependencies

- `knowledge_base/engine/event_store.py` (commit `98ec53f`) — reuse for reimbursement-change events.
- `knowledge_base/schemas/` — add `ReimbursementStatus`, `ReimbursementChange`.
- `knowledge_base/validation/loader.py` — new content category `reimbursement/`.
- `scripts/build_site.py` — `/changelog-nszu.html` rendering.
- `legacy/source_pdfs/` — raw PDFs may fall back here (already gitignored).

## What this spec does NOT cover

- Auth/registry for per-clinician inbox (P3 in roadmap, separate spec).
- ProZorro stock-level integration (separate feature, separate spec).
- Reimbursement in countries outside Ukraine (not in scope for now).
