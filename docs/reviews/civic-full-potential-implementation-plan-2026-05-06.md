# CIViC full-potential implementation plan - 2026-05-06

**Purpose:** maximize use of CIViC's open molecular evidence while keeping
OpenOnco clinically conservative and license-compliant.

**Core decision:** CIViC is the hosted/open molecular evidence base. NCCN,
ESMO, regulatory labels, and primary trials are non-hosted guardrails for
standard-of-care classification.

---

## 1. Operating model

OpenOnco should render biomarker findings in separate lanes:

| Lane | Meaning | Required evidence |
|---|---|---|
| Standard care | Treatment is appropriate to show in the main plan | Guideline, label, or high-quality trial source plus supporting KB entity |
| Molecular evidence option | CIViC supports actionability, but standard-care status is not established in repo sources | CIViC accepted evidence with source PMIDs/EIDs |
| Resistance or avoidance signal | CIViC indicates resistance or lack of support for a therapy | CIViC resistance or `Does Not Support` evidence |
| Trial/research option | Signal is plausible but not enough for treatment recommendation | CIViC C/D/E or preclinical/inferential evidence plus trial search |
| Insufficient evidence | Marker is detected but no defensible actionability claim exists | Explicit no-match / low-confidence record |

This prevents a CIViC-supported research signal from being promoted into a
standard treatment recommendation without clinical-source confirmation.

---

## 2. Data expansion phases

### Phase 1 - CIViC snapshot inventory

Build a repeatable inventory over `knowledge_base/hosted/civic/<date>/`.

Deliverables:
- accepted evidence item count
- unique molecular profiles
- unique gene/variant pairs
- evidence type distribution
- evidence level distribution
- therapy-bearing evidence count
- resistance evidence count
- disease and therapy coverage matrix

Acceptance criteria:
- inventory script is deterministic
- output is committed as a dated review artifact
- counts match the loaded snapshot

### Phase 2 - Normalized CIViC matcher

Improve matching beyond naive `gene == symbol`.

Required matching behavior:
- fusion-aware matching for `BCR::ABL1`, `EML4::ALK`, `ETV6::NTRK3`, etc.
- case-insensitive exon descriptors
- variant substring matching for fusion-background resistance mutations
- alias normalization for common symbols and therapy names
- disease mapping through DOID plus existing disease aliases

Acceptance criteria:
- unit tests cover fusions, exon deletions/insertions, resistance mutations,
  and empty/null fields
- matcher returns structured confidence reasons, not just true/false

### Phase 3 - Evidence lane classifier

Create a small rule layer that classifies CIViC evidence into OpenOnco lanes.

Rules:
- CIViC A/B predictive evidence with therapy can enter "molecular evidence
  option"
- CIViC resistance or `Does Not Support` evidence enters "resistance or
  avoidance signal"
- CIViC C/D/E evidence enters "trial/research option" unless overridden by
  a stronger source
- diagnostic/prognostic/oncogenic evidence must not create a therapy
  recommendation by itself
- standard-care lane requires non-CIViC confirmation from label, guideline,
  or primary trial source

Acceptance criteria:
- every BMA receives one lane
- lane decision includes source IDs and rationale
- renderer never treats CIViC-only evidence as standard care

### Phase 4 - BMA reconstruction at scale

Use CIViC to backfill biomarker_actionability records where evidence exists.

Workflow:
- scan all biomarker records for actionable lookup fields
- match against CIViC evidence
- attach granular `SRC-CIVIC-EID-*` references
- preserve `actionability_review_required: true`
- generate a conflict report for existing claims contradicted by CIViC

Acceptance criteria:
- no unreviewed clinical content goes live
- idempotent re-run changes nothing when the snapshot is unchanged
- report lists skipped markers by reason

### Phase 5 - Non-CIViC biomarker coverage

Do not force CIViC to cover guideline-style biomarkers.

Separate work queues:
- IHC markers: PD-L1, HER2, CD30, CD20, ER/PR
- composite markers: HRD, MSI/MMR, TMB-high
- methylation/risk markers: MGMT, IGHV, cytogenetic scores
- infectious/status markers: HPV, EBV, HBV, HCV, HIV

Evidence approach:
- use labels, primary trials, NCI/public sources, and referenced guideline
  citations
- do not host NCCN/ESMO tables or algorithms
- model disagreements explicitly instead of resolving them by LLM judgment

Acceptance criteria:
- every non-CIViC marker has a source strategy
- unsupported cells are marked blocked-on-source
- guideline disagreements are visible in review artifacts

### Phase 6 - Renderer and patient-facing behavior

Update the report renderer so users see evidence strength without seeing
unsupported recommendations.

Required UI/report behavior:
- standard-care treatments remain separate from molecular evidence options
- resistance signals are shown near affected drugs
- CIViC-only signals include "molecular evidence, not standard-care
  confirmation"
- every claim links to source IDs, PMIDs, and CIViC EIDs where available
- no legacy OncoKB citation is surfaced

Acceptance criteria:
- snapshot date appears in output
- CIViC evidence lane is distinguishable from guideline/label evidence
- patient-facing language does not imply CIViC is medical advice

### Phase 7 - Monthly refresh and drift review

Automate update detection but keep clinical promotion human-reviewed.

Refresh workflow:
- fetch new CIViC snapshot
- run inventory
- run matcher
- diff evidence added/removed/changed
- identify lane changes and new resistance signals
- open review artifact for clinical co-leads

Acceptance criteria:
- automated refresh never silently changes standard-care recommendations
- new CIViC signals default to review-required
- removal/downgrade of evidence creates a high-priority review item

---

## 3. Governance rules

- CIViC can be hosted and redistributed because the repo source entity records
  CC0 status.
- NCCN/ESMO should remain referenced, not hosted, unless explicit written
  permission exists.
- LLMs may extract and draft, but must not decide clinical recommendation
  rank, regimen choice, dosing, or biomarker interpretation for treatment
  selection.
- Two clinical co-lead approvals are required before clinical content affects
  live recommendations.
- Conflicts between CIViC and guideline/label sources must be displayed as
  conflicts, not averaged away.

---

## 4. Priority build order

1. Inventory script and dated CIViC coverage report.
2. Fusion-aware and disease-aware matcher tests.
3. Evidence lane classifier.
4. BMA reconstruction re-run with lane metadata.
5. Renderer changes for standard-care vs molecular-evidence separation.
6. Non-CIViC biomarker backlog for IHC/composite markers.
7. Monthly refresh CI with clinical-review queue.

---

## 5. Success metrics

- More CIViC evidence is visible without increasing clinical overclaim risk.
- Every CIViC-backed BMA has granular EID citations.
- CIViC resistance signals are surfaced before treatment ranking.
- Standard-care recommendations remain traceable to guideline, label, or
  primary trial sources.
- NCCN/ESMO content is referenced but not copied into hosted OpenOnco data.
- Monthly refreshes produce reviewable diffs instead of silent behavior changes.
