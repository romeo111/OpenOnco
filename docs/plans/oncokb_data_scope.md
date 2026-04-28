# ⚠️ SUPERSEDED — 2026-04-27

This OncoKB-era decision-record is preserved for historical reference.
OncoKB integration was rejected after Terms-of-Service audit found a fundamental
conflict with CHARTER §2 (free public clinical decision-support). See
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` and
`docs/plans/civic_integration_v1.md`.

---

# OncoKB · Data scope (deferred decision, parked 2026-04-25)

**Status:** parked default — confirmed during Phase 10 scaffold sprint.

## Decision

OpenOnco consumes **only therapeutic levels** from OncoKB:

- **1** — FDA-recognized biomarker for therapy in this tumor type
- **2** — Standard care biomarker per professional guidelines
- **3A** — Compelling clinical evidence (different tumor type)
- **3B** — Compelling biological evidence
- **4** — Standard-care resistance biomarker (R1) / investigational
- **R1, R2** — Resistance levels

For each (gene, variant, disease_oncotree_code) triplet, the proxy returns:
- the therapeutic level
- drug name(s)
- short description
- cited PMIDs

Plus a deep-link to the OncoKB page (`https://www.oncokb.org/gene/{gene}/{variant}`)
for the clinician to read the full interpretation.

## What we do NOT consume

- **Gene-level annotations** (oncogenic effect, hotspot status). These
  are not actionable enough at the level our engine operates — it would
  surface noise without changing the plan.
- **Variants of unknown significance (VUS)**. By definition not
  actionable; surfacing them invites automation bias.
- **Structural variant annotations**. Out-of-scope for our current
  rule-engine; needs a dedicated entity type if revisited.
- **Diagnostic / prognostic levels (Dx, Px)**. Different signal — should
  be a separate ingestion pass if/when added.

## Why narrow

CHARTER §8.3: LLMs / external KBs cannot be the clinical decision-maker.
Therapeutic-level data is the cleanest match for the
"surface-as-precision-medicine-layer" pattern: the engine does not pick
based on it, the plan render simply lists what OncoKB cites for the
patient's biomarkers and the clinician decides whether to consult.

## Revisit triggers

Reopen this scope decision if:
- A clinical co-lead asks for VUS triage (e.g. paneled NGS results with
  many novel variants).
- The structural-variant entity type is added to KNOWLEDGE_SCHEMA_SPECIFICATION.
- OncoKB API changes the therapeutic-level taxonomy (currently stable).
