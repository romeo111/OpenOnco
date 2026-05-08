# GI-2 wave: gastric + esophageal KB expansion

**Stamp:** 2026-05-04-1730
**Status:** PROPOSED — not dispatched
**Authors:** orchestrator session `musing-murdock-c08478` (coverage audit + Plan agent synthesis)
**Reviewers needed:** 2/3 Clinical Co-Leads for §17 PROPOSAL gate; chunk PRs follow standard CHARTER §6.1 dev-mode exemption

---

## 1. Problem statement

### 1.1 Trigger

User-driven coverage assessment of the OpenOnco KB against
**UpToDate 6.0 + ESMO 2024** for gastric / esophageal cancer, with
explicit focus on:

- multimodal treatment
- minimally invasive esophagectomy
- OMEC trial results (oligometastatic esophagogastric cancer)
- personalisation of systemic therapy

Plus a concrete clinical-vignette validation: metastatic HER2-negative
gastric cancer, PD-L1 CPS = 25 → expected 1L treatment **FOLFOX +
nivolumab** (per CheckMate-649; ESMO [I, A]; NCCN-2026 lowering CPS
threshold from ≥10 → ≥1 with magnitude-of-benefit notes for ≥5).

### 1.2 Findings (from audit + Plan agent)

#### 1.2.1 Coverage scoring vs ESMO/UpToDate-2024

| Domain | Coverage | Notes |
|---|---|---|
| Personalisation, gastric metastatic | ~65% | HER2/CLDN18.2/PD-L1/MSI/FGFR2/MET/KRAS/PIK3CA/TP53/MMR all present; missing EBV/HER2-low/FGFR2b/TROP2 |
| Personalisation, esoph metastatic | ~30% | Only 2L SCC + 2L adeno-PD-L1; **no 1L indication at all** |
| Multimodal periop, gastric (FLOT) | 0% | No FLOT4 indication, no `flot.yaml` regimen, no D2-lymphadenectomy guidance |
| Multimodal periop, esoph (CROSS) | ~40% | Chemo backbone + adjuvant nivo present; RT/surgery phasing blocked by §17 schema gap |
| Minimally invasive esophagectomy | 0% | No `procedures/` content-type; schema cannot model MIE vs RAMIE vs open |
| OMEC / oligometastatic | 0% | No consensus definition, no oligomet indication, no `IntentOfTreatment` enum |
| Primary-trial source citations | ~5% | Only NCCN/ESMO secondary; ToGA, CROSS, FLOT4, KEYNOTE-590, CheckMate-577/648, DESTINY-Gastric01, SPOTLIGHT/GLOW, RAINBOW, TIME, ROBOT, OMEC, RENAISSANCE all missing |

**Overall:** ~25% of ESMO/UpToDate-level. KB at Tier-1 scaffold quality,
not Tier-2 production for GI domain.

#### 1.2.2 Specific defects found in vignette walk-through (CheckMate-649 / FOLFOX+nivo)

Walking the rule-engine for HER2-neg + CPS=25 metastatic gastric:

1. **Engine produces correct answer** (`IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI` →
   `REG-FOLFOX-NIVO`) — match works, no routing conflict. ✅
2. **CheckMate-649 source file exists** at
   `knowledge_base/hosted/content/sources/src_checkmate_649_janjigian_2022.yaml`
   but is **not cited** by any indication, regimen, or red-flag. ❌
   - `redflags/rf_gastric_pdl1_cps_1_plus.yaml` line 80 contains a **stale TODO**
     referencing the wrong year (`SRC-CHECKMATE-649-JANJIGIAN-2021`, file is `…-2022`).
3. **CPS threshold inconsistency:** algorithm + RF use CPS≥1 (NCCN-2026
   stance), but indication-level `biomarker_requirements_required` still
   demands CPS≥5 (ESMO/EMA stance). For CPS 1-4 patients the engine routes
   to the indication and then rejects → **no recommendation** rather than
   the NCCN-permitted weaker-benefit option.
4. **Nivolumab dosing:** `regimens/folfox_nivolumab.yaml` lists 240 mg q2w /
   480 mg q4w (FDA flat-dose interchange), missing the **CheckMate-649
   primary-protocol canonical dose: 360 mg q3w** with FOLFOX/XELOX backbone.

#### 1.2.3 CheckMate-trial usage across the KB

| Trial | File exists? | Cited where? |
|---|---|---|
| CheckMate-067 (Larkin 2019, melanoma nivo+ipi) | yes | 8+ melanoma files ✅ |
| CheckMate-238 (Weber 2017, adj nivo melanoma) | yes | 2 melanoma indications ✅ |
| CheckMate-816 (Forde 2022, neoadj nivo NSCLC) | yes | `bio_pdl1_28_8_clone` ✅ |
| **CheckMate-649** (Janjigian 2022, gastric 1L) | **yes** | **none — file orphaned** ❌ |
| CheckMate-577 (Kelly 2021, esoph adj nivo) | **no** | text mention only in `ind_esoph_adjuvant_nivolumab_post_cross.yaml` rationale ❌ |
| CheckMate-648 (Doki 2022, esoph SCC 1L) | **no** | not cited; no esoph 1L indication exists ❌ |

#### 1.2.4 Schema-level blocker: §17 PROPOSAL not ratified

Both disease YAMLs explicitly flag this gap in their `metadata.awaiting_proposal`:

> KNOWLEDGE_SCHEMA_SPECIFICATION.md §17 — periop FLOT (neoadjuvant→surgery→adjuvant) phasing not modellable today; metastatic biomarker-driven algorithm scaffolded only

§17 introduces `Surgery`, `RadiationCourse`, `Indication.phases[]`,
`IntentOfTreatment` enum (curative / palliative / oligometastatic /
adjuvant / neoadjuvant / periop), and a new `procedures/` content-type
folder. Until ratified, **FLOT periop, CROSS RT phasing, definitive CRT,
MIE/RAMIE selection, and OMEC oligometastatic intent** are all
non-modellable.

---

## 2. Solution overview

GI-2 wave as a **chunk-task batch** following W7-W11 patterns: direct
hosted-KB edits on `chunk/...` branches with `validate_kb` + pytest
quality gate (NOT Q-axis sidecar — this is new authoring).

Total scope: **12 chunks** across 5 phases + 1 non-chunk schema-ratification
workstream.

---

## 3. Workstream sequencing

```
                   ┌──────────────────────────────────────┐
                   │ W0  Source backfill foundation       │
                   │     (15 new + CM-649 propagation)    │
                   └──────────────┬───────────────────────┘
                                  │
              ┌───────────────────┼─────────────────────────┐
              │                   │                         │
              ▼                   ▼                         ▼
        ┌──────────┐        ┌────────────┐         ┌────────────────┐
        │ A1       │        │ A2         │         │ §17 PROPOSAL   │  parallel
        │ Esoph 1L │        │ EBV/HER2L/ │         │ Surgery +      │  (NOT a chunk)
        │ metast.  │        │ FGFR2b/    │         │ RadiationCourse│
        │ (CM-648, │        │ TROP2 BMA  │         │ + Indication.  │
        │ KN-590)  │        │ + indic.   │         │ phases + intent│
        └────┬─────┘        └─────┬──────┘         └────────┬───────┘
             │                    │                         │ ratify
             └────────────┬───────┘                         │ + schema bump
                          ▼                                 │
                  ┌───────────────┐                         │
                  │ B1  CPS recon │                         │
                  │     + nivo    │                         │
                  │     dose patch│                         │
                  └───────┬───────┘                         ▼
                          │                  ┌────────────────────────────────┐
                          │                  │ C1 FLOT periop (gastric)       │
                          │                  │ C2 CROSS phasing (esoph)       │
                          │                  │ C3 Definitive CRT (SCC)        │
                          │                  │ C4 MIE / RAMIE selection       │
                          │                  │ C5 Oligometastatic / OMEC      │
                          │                  └────────────────┬───────────────┘
                          │                                   │
                          └─────────────────┬─────────────────┘
                                            ▼
                                  ┌─────────────────────┐
                                  │ D1  Algorithms      │
                                  │  (CPS update +      │
                                  │   periop + esoph 1L)│
                                  └─────────────────────┘
```

**Critical path:** §17 PROPOSAL → schema bump → C-block (FLOT / CROSS /
MIE / oligo). All of W0/A/B can ship without §17.

**Soft block:** D1 ideally last (consumes C-indications). If §17 slips,
ship a thin-D1 (metastatic algos only, periop deferred).

---

## 4. Phase breakdown

### 4.1 W0 · Sources backfill

Independent of §17. Blocks downstream citations. **3 parallel chunks.**

| # | Chunk | Files | Pattern |
|---|---|---|---|
| W0-1 | gastric trial sources | 8 NEW | W10 source-stub-batch |
| W0-2 | esophageal trial sources | 7 NEW | W10 source-stub-batch |
| W0-3 | CheckMate-649 propagation | 0 new (3-4 edits) | W9-redflag-patch grep-and-add |

**W0-1 manifest (8 IDs):**
- SRC-TOGA-BANG-2010
- SRC-FLOT4-AL-BATRAN-2019
- SRC-KEYNOTE-859-RHA-2023
- SRC-DESTINY-GASTRIC01-SHITARA-2020
- SRC-SPOTLIGHT-SHITARA-2023
- SRC-GLOW-SHAH-2023
- SRC-RAINBOW-WILKE-2014
- SRC-RENAISSANCE-AIO-FLOT5

**W0-2 manifest (7 IDs):**
- SRC-CROSS-VAN-HAGEN-2012
- SRC-CHECKMATE-577-KELLY-2021
- SRC-CHECKMATE-648-DOKI-2022
- SRC-KEYNOTE-590-SUN-2021
- SRC-TIME-BIERE-2012
- SRC-ROBOT-VAN-DER-SLUIS-2019
- SRC-OMEC-1-KROESE-2018

**W0-3 manifest (existing-file-edits only):**
- `indications/ind_gastric_metastatic_1l_pdl1_chemo_ici.yaml`
- `regimens/folfox_nivolumab.yaml`
- `redflags/rf_gastric_pdl1_cps_1_plus.yaml`
- (any other gastric-1L-PD-L1 references found via grep)

### 4.2 A · 1L metastatic gaps

Depends on W0 merged. **2 chunks.**

#### A1 — Esoph 1L metastatic + HER2-positive esoph adeno

NEW indications:
- `ind_esoph_metastatic_1l_adeno_chemo_pembro` (KEYNOTE-590)
- `ind_esoph_metastatic_1l_scc_ipi_nivo` (CheckMate-648, ipi+nivo arm)
- `ind_esoph_metastatic_1l_scc_chemo_nivo` (CheckMate-648, chemo+nivo arm)
- `ind_esoph_metastatic_1l_her2_trastuzumab_chemo` (ToGA extrap)
- `ind_esoph_metastatic_1l_her2_low_t_dxd` (DESTINY-Gastric04 extrap, `confidence: moderate`)

NEW regimens:
- `reg_folfox_pembro_esoph`
- `reg_ipi_nivo_esoph_scc`
- `reg_folfox_nivo_esoph_scc`

Allowlist: `indications/ind_esoph_metastatic_1l_*.yaml` + 3 regimens.

#### A2 — Extended personalisation BMA + indications

NEW BMAs (must use Phase 1.5 `evidence_sources` block, not legacy
`oncokb_*`):
- `bma_ebv_positive_gastric` (subtype router)
- `bma_her2_low_gastric` (T-DXd line-extension; DESTINY-Gastric04)
- `bma_fgfr2b_membrane_gastric` (bemarituzumab; FORTITUDE-101 — interim, `confidence: moderate`, `actionability_review_required: true`)
- `bma_trop2_gastric`, `bma_trop2_esoph_adeno` (Dato-DXd)
- `bma_cldn18_2_gej_esoph_adeno` (SPOTLIGHT/GLOW GEJ subset)

Companion biomarkers (only if missing): `bio_ebv.yaml`, `bio_fgfr2b_ihc.yaml`,
`bio_trop2_ihc.yaml`.

Companion indications: `ind_*_t_dxd_her2_low.yaml`, `ind_*_bemarituzumab.yaml`.

### 4.3 B · Reconciliation patches

Independent. **1 chunk, 1 agent, ≤3 files.**

#### B1 — CPS threshold + nivo dosing

- Reconcile `rf_gastric_pdl1_cps_1_plus` (≥1) vs
  `ind_gastric_metastatic_1l_pdl1_chemo_ici` (≥5) → align to **NCCN-2026 ≥1**,
  add `magnitude_of_benefit` notes for CPS 1-4 vs ≥5 stratum.
- Add canonical CheckMate-649 q3w (nivo 360 mg + FOLFOX) to
  `regimens/folfox_nivolumab.yaml` alongside existing q2w/q4w.
- Add `known_controversies` block re: ESMO ≥5 vs NCCN-2026 ≥1.

Allowlist: 3 files exactly.

### 4.4 §17 PROPOSAL ratification (NOT a chunk)

Sequential, human-in-the-loop, blocks C-block.

| Step | Owner | Output |
|---|---|---|
| 1. Spec author writes §17 final | spec-author (human) | `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 promoted PROPOSAL → RATIFIED |
| 2. Two-reviewer signoff | 2/3 Clinical Co-Leads (CHARTER §6.1) | sign-off recorded |
| 3. Schema bump | dev (Claude OK autonomously) | `knowledge_base/schemas/{indication.py, disease.py}` + new `procedure.py`, `radiation_course.py`; `IntentOfTreatment` enum |
| 4. Validator update | dev | accepts new fields; existing data still validates (no breakage) |
| 5. Migration | dev | `scripts/_migrate_§17_phases.py` adds `phases:` to existing CROSS / adjuvant nivo indications. Idempotent. |
| 6. Test fixtures | dev | `tests/fixtures/{phased_indication, surgery_procedure, radiation_course}.yaml`; `tests/test_phases.py` |

**Schema fields (sketch — proposal-author authoritative):**
- `Indication.phases: list[Phase]` where
  `Phase = {phase_name: str, order: int, regimen_ref: str?, procedure_ref: str?, radiation_ref: str?, duration_weeks: int?}`
- `Indication.intent: IntentOfTreatment` (curative | palliative | oligometastatic | adjuvant | neoadjuvant | periop)
- new `Surgery` model: `{procedure_id, technique: enum[open|MIE|RAMIE|...], approach, lymphadenectomy_extent, contraindications, citations}`
- new `RadiationCourse` model: `{rt_id, modality: enum[3DCRT|IMRT|VMAT|SBRT|protons], dose_gy, fractions, target_volume, concurrent_chemo_ref, citations}`
- new `procedures/` content-type folder, validated like other entities

**Estimate:** 1.5-3 working days end-to-end (proposal text 0.5d → 2-reviewer
signoff calendar gate 1-3d wait → schema+validator+migration+tests 1-2d).

### 4.5 C · Multimodal / surgery / RT (BLOCKED until §17 ratifies)

**5 chunks, all §17-blocked.** Pattern: W11 multi-entity.

| # | Chunk | New entities |
|---|---|---|
| C1 | FLOT periop (gastric) | `ind_gastric_periop_flot4`, `ind_gastric_adjuvant_capox`, `ind_gej_neoadj_crt`, `reg_flot`, `reg_capox_adjuvant`, `proc_d2_lymphadenectomy`, update `dis_gastric` |
| C2 | CROSS RT phasing (esoph) | populate `RadiationCourse` + `Indication.phases[]` for existing CROSS neoadjuvant; new `proc_cross_rt.yaml` |
| C3 | Definitive CRT (esoph SCC unresectable) | `ind_esoph_definitive_crt_scc`, `reg_definitive_crt_esoph`, `proc_definitive_rt_esoph` |
| C4 | MIE / RAMIE selection | `proc_esophagectomy_open`, `proc_esophagectomy_mie`, `proc_esophagectomy_ramie` + `dis_esophageal` procedure-options block; cite TIME / ROBOT |
| C5 | Oligometastatic / OMEC | `ind_gastric_oligometastatic_*`, `ind_esoph_oligometastatic_*`, `rf_oligometastatic_definition`; cite OMEC-1 + RENAISSANCE-AIO-FLOT5 |

**Disease-file write contention:** `dis_gastric` (C1, C5), `dis_esophageal`
(C2, C3, C4). Sequence within C-block: C1 + C2 first (different diseases);
C3-C5 after. Or: integration agent owns all disease-file edits last.

### 4.6 D · Algorithms

Final pass. **1 chunk** (or thin version if §17 slips).

#### D1 — Algorithms

- Extend `algo_gastric_metastatic_1l` (CPS branch update — consume B1 reconciliation)
- New `algo_gastric_periop` (consumes C1)
- New `algo_esoph_metastatic_1l` (consumes A1)

If §17 slips → thin-D1 = first item only (CPS update), defer the other two.

---

## 5. Sources-backfill strategy: rationale

Hybrid 3 sub-chunks (W0-1 / W0-2 / W0-3). **Why not** alternatives:

| Option | Rejected because |
|---|---|
| One mega-chunk (15+ sources, single agent) | >2h wall time; allowlist sprawl; one failure blast-radius too wide |
| One source per indication-chunk | Same trial cited from multiple indications (CROSS by C2+C3, ToGA by A1+A2+C2) → race conditions on source files; each chunk re-discovers PubMed format → infra duplication |
| **Hybrid (chosen)** | Parallel agents, separate folders by trial-disease, no overlap; CheckMate-649 special-case (zero-new-file) isolated to its own chunk with distinct rejection criteria |

---

## 6. Risk register

| # | Risk | Mitigation |
|---|---|---|
| R1 | §17 ratification slips → C-block (5 chunks) blocked indefinitely; D1 partially blocked | Dispatch C-block with explicit "DO NOT START" gate. Start §17 ratification on Day 1 in parallel with W0/A/B. Have thin-D1 fallback ready (metastatic algos only). |
| R2 | OMEC consensus / oligometastatic sparse evidence | C5 author cites OMEC-1 + ESMO consensus 2024 with `confidence: moderate`; mark indication `proposal_status: partial` if needed. |
| R3 | bemarituzumab FORTITUDE-101 readout (Fall 2024) — final OS data may shift; current data interim | A2 author uses `data_cutoff:` + `confidence: moderate` + `actionability_review_required: true`; flag for re-review when final OS published. |
| R4 | Two-reviewer clinical signoff (CHARTER §6.1) for periop / curative-intent C-block | Mark C/D PRs `needs-clinical-review`; **do not auto-push** even with green gates — clinical signoff is a gate. |
| R5 | CIViC pivot active; A2 BMA must use Phase 1.5 `evidence_sources` block | Bake into A2 chunk acceptance criteria; reject any `oncokb_lookup` / `oncokb_level` field. Reference commits: `5384348` (Phase 1) + `c72e45b` (Phase 1.5). |
| R6 | Concurrent worktree edits to `dis_gastric.yaml` / `dis_esophageal.yaml` across C1-C5 | Sequence within C-block: C1 + C2 first (different diseases); C3-C5 after, sequentially. Or: integration agent owns disease-file edits last. |

---

## 7. Estimate

| Metric | Without §17 (W0+A+B+thin-D) | With §17 (full wave) |
|---|---|---|
| Chunks | 6-8 | 11-14 |
| Agent-hours | 14-30 | 30-65 |
| PRs | 6-8 | 11-14 |
| §17 ratification calendar-days | 0 | 1.5-5 (proposal + 2-reviewer wait + schema bump) |
| **Total calendar-days** | **3-8** | **6-16** |

Bottlenecks: (1) §17 2-reviewer wait (calendar, not work) — start Day 1;
(2) clinical signoff for C-block PRs — overlap with D1 dispatch;
(3) disease-file write contention within C-block.

---

## 8. Chunk inventory summary

| Chunk | Phase | §17? | Parallel-with | Files |
|---|---|---|---|---|
| W0-1 sources gastric | W0 | no | W0-2, W0-3, B1, §17 | 8 new |
| W0-2 sources esoph | W0 | no | W0-1, W0-3, B1, §17 | 7 new |
| W0-3 CM-649 propagate | W0 | no | W0-1, W0-2, B1, §17 | 0 new (3-4 edits) |
| A1 esoph 1L met | A | no | A2, B1 | 5+3=8 new |
| A2 BMA expansion | A | no | A1, B1 | ~10 new |
| B1 CPS+nivo patch | B | no | A, W0 | 3 edits |
| C1 FLOT periop | C | YES | C2 | 7 new+edit |
| C2 CROSS phasing | C | YES | C1 | 1 edit + 1 new |
| C3 definitive CRT | C | YES | (after C2) | 3 new |
| C4 MIE/RAMIE | C | YES | (after C2/C3) | 2-3 new |
| C5 oligometastatic | C | YES | (after C1) | 3 new |
| D1 algorithms | D | partial | (after A, C) | 3 edits |

---

## 9. Pre-dispatch decisions needed (orchestrator → user)

1. **Start §17 ratification now** (parallel with W0/A/B, calendar wait
   not work) **or** defer until W0/A/B merged?
2. **First batch scope:**
   - Conservative: W0 only (3 chunks, foundation, lowest risk)
   - Default: W0 + B1 (4 chunks; B1 has zero overlap with W0)
   - Aggressive: W0 + A + B1 (5-6 chunks; risks W0-3 / B1 race on
     `folfox_nivolumab.yaml` — must serialise these two)
3. **Auto-push policy for C/D chunks:** confirm CHARTER §6.1 dev-mode
   exemption holds for periop / curative-intent, OR explicitly require
   clinical signoff before merge for C-block (recommendation: require).

---

## 10. Open questions / follow-ups

- Does §17 PROPOSAL author already exist, or does this plan need to
  trigger that recruitment first?
- NCCN-2026 source — currently we cite `SRC-NCCN-GASTRIC-2025`. If the
  CPS≥1 stance is from NCCN-2024+, do we need a fresh `SRC-NCCN-GASTRIC-2026`
  source file, or hold on `2025`?
- Does the existing `regimens/folfox_nivolumab.yaml` need a separate
  `reg_xelox_nivolumab.yaml` (CheckMate-649 also tested XELOX backbone)?
- Standalone KEYNOTE-859 (pembro+chemo gastric 1L) indication —
  in-scope or defer to GI-3?

---

## 11. Audit / provenance

- Coverage audit: this session, 2026-05-04, against repo HEAD on
  `chore/q-axis-batch5c-upsert-2026-05-02`.
- Vignette walk-through: `IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI`
  routing trace, files
  `algo_gastric_metastatic_1l.yaml`, `ind_gastric_metastatic_1l_pdl1_chemo_ici.yaml`,
  `regimens/folfox_nivolumab.yaml`, `rf_gastric_pdl1_cps_1_plus.yaml`,
  `bma_her2_amp_gastric.yaml`.
- CheckMate-trial usage scan: full-tree grep for `SRC-CHECKMATE`,
  `CheckMate`, `checkmate` across `knowledge_base/hosted/content/`.
- Source-of-record: this document.

---

## 12. Post-W0 corrections (added 2026-05-04, after W0-1/W0-2/W0-3 merged)

Three findings surfaced during W0 dispatch that invalidate parts of this
plan as originally written. Captured here as a post-mortem so subsequent
phases (A, B, C, D) act on the corrected understanding.

### 12.1 Coverage audit was partially wrong: esoph 1L exists

This document §1.2.1 said "esoph metastatic ~30% — Only 2L SCC + 2L
adeno-PD-L1; **no 1L indication at all**."

That is **incorrect**. `git ls knowledge_base/hosted/content/indications/`
on `origin/master` shows:

- `ind_esoph_metastatic_1l_pembro_chemo.yaml` — KEYNOTE-590 covered
- `ind_esoph_metastatic_1l_nivo_chemo_scc.yaml` — CheckMate-648 (chemo + nivo arm) covered
- `algorithms/algo_esoph_metastatic_1l.yaml` — algorithm tree exists

**Phase A1 redux scope** — what actually remains to add:

- `ind_esoph_metastatic_1l_scc_ipi_nivo` — CheckMate-648 ipi + nivo arm only (chemo + nivo arm already covered)
- `ind_esoph_metastatic_1l_her2_trastuzumab_chemo` — ToGA extrapolation
- `ind_esoph_metastatic_1l_her2_low_t_dxd` — DESTINY-Gastric04 extrapolation
- Companion regimens for the 3 above

Drops 2 indications and 1 regimen from original A1 scope. **A1 is roughly
half the size originally planned.**

### 12.2 Manifest collision: hyphenation inconsistency

W0-2 agent stopped on collision: 2 of 7 manifest IDs (`SRC-CHECKMATE-648-DOKI-2022`,
`SRC-KEYNOTE-590-SUN-2021`) already exist as `SRC-CHECKMATE648-DOKI-2022` /
`SRC-KEYNOTE590-SUN-2021` (no hyphen between trial name and number).

KB-wide naming inconsistency observed: some sources use `keynote006`,
some `keynote_826`, some hyphenated. Resolution: **drop the 2
collisions from W0-2 manifest** (they're already cited 3× each); defer
KB-wide normalisation to a future renormalisation chunk.

**Add to renormalisation backlog:**
- `SRC-CHECKMATE648-DOKI-2022` → `SRC-CHECKMATE-648-DOKI-2022`
- `SRC-KEYNOTE590-SUN-2021` → `SRC-KEYNOTE-590-SUN-2021`
- Audit any other source IDs without hyphens for consistency

### 12.3 Manifest defect: OMEC-1 year wrong

W0-2 agent flagged: manifest ID `SRC-OMEC-1-KROESE-2018` references a
non-existent paper. The actual OMEC-1 Delphi consensus is Kroese 2023
(PMID 36947929). 2018 paper does not exist.

Agent preserved manifest ID verbatim per brief, with year-mismatch
flagged in source YAML `notes` field.

**Add to renormalisation backlog:**
- `SRC-OMEC-1-KROESE-2018` → `SRC-OMEC-1-KROESE-2023` (rename file + ID)
- Verify any future references use corrected ID

### 12.4 Schema field naming defect in this plan's chunk-issue templates

Original W0 chunk-issue bodies (this doc §4.1) listed required fields:

```
kind: trial
clinical_trial_registration: NCT-...
```

**These fields do NOT exist** in `knowledge_base/schemas/source.py`. The
actual schema convention (matching `src_keynote189_gandhi_2018.yaml`,
`src_adaura_wu_2020.yaml`, etc.):

```
source_type: rct_publication   # for trials
source_type: guideline         # for consensus papers / guidelines
notes: |
  ...narrative description with NCT-XXXXXXXX embedded inline...
```

Both W0-1 and W0-2 agents adapted to actual schema (W0-3 didn't need to
because no new files). **Update all chunk-issue templates in this plan
(§4.1, §4.2, §4.3) and the q_axis_dispatch_template_2026-05-01.md
sister document before dispatching A/B/C/D.**

### 12.5 Pre-commit hooks not configured in repo

Plan §6 R6 mitigation referenced `pre-commit run --all-files` as a
quality gate. Both W0 agents reported `.pre-commit-config.yaml` does
not exist in repo. Quality gate effectively reduces to:

```
C:/Python312/python.exe -m knowledge_base.validation.cli   # ok=True, 0 schema, 0 contract regressions
C:/Python312/python.exe -m pytest tests/test_<scope>.py     # green
```

Update chunk-issue templates accordingly.

### 12.6 Pre-existing baseline failures

Both `test_seed_loads_without_errors` and a regimen-schema-error pattern
in `regimens/reg_bep_gct.yaml` etc. fail on baseline `origin/master`.
Agents must verify pytest-fail count is **identical pre/post**, not
**zero**.

KB validator schema errors: 91 baseline (concentrated in regimens/
files from prior chunks). New work must not *increase* this count.

### 12.7 Net effect on remaining phases

| Phase | Original scope | Revised scope (post-W0) |
|---|---|---|
| A1 esoph 1L met | 5 NEW indications + 3 regimens | **3 NEW** indications (CM-648 ipi+nivo, HER2-positive 1L × 2) + 1-2 regimens — half the work |
| A2 BMA expansion | unchanged | unchanged (no overlap with W0 findings) |
| B1 CPS+nivo patch | 3-file edit | unchanged (race with W0-3 already serialised — W0-3 merged, B1 dispatchable now) |
| §17 PROPOSAL | unchanged | unchanged (still blocking C-block) |
| C1-C5 multimodal | unchanged scope | unchanged scope; templates need schema-field corrections |
| D1 algorithms | extend `algo_gastric_metastatic_1l` + new `algo_gastric_periop` + new `algo_esoph_metastatic_1l` | extend × 2 only — `algo_esoph_metastatic_1l` ALREADY EXISTS (just needs CM-648 ipi+nivo branch added) |

**Estimate impact:** -2 chunks-worth of work (A1 reduced by half; D1 reduced).
Total wave probably 10-12 chunks instead of 12.

---

## 13. Phase A final outcome (added 2026-05-07)

Phase A (W0 sources + A1 indications + A2 BMA + B1 reconciliation + W0-4/W0-5
extensions + bemfill housekeeping) **landed in master across 11 squash-merged PRs**.
Phase C (multimodal — FLOT periop / CROSS phasing / MIE / oligomet) remains
**§17-blocked** per #394. Phase D (algorithms) flagged for follow-up (engine-side
extensions only — no clinical content).

### 13.1 PR ledger

| PR | Commit | Chunk |
|---|---|---|
| #396 | `ad90099b` | W0-1 gastric trial sources × 8 |
| #397 | `b6f49b26` | W0-3 CheckMate-649 propagation |
| #398 | `3cac0fe8` | W0-2 esoph trial sources × 5 |
| #401 | `09359087` | B1 CPS reconciliation + canonical nivo q3w |
| #402 | `1017fe5c` | Plan doc + post-W0 corrections |
| #404 | `92744023` | W0-4 DESTINY-Gastric04 source |
| #408 | `bce7a093` | A1-redux esoph 1L (2 indications + 1 regimen) |
| #409 | `adc07347` | A2 BMA expansion (3 BMAs + 1 bio + 1 indication) |
| #414 | `397dbc0b` | W0-5 EBV gastric primary sources + BMA upgrade |
| #416 | `0593eb5d` | bemfill (regimen + FORTITUDE-101 stub upgrade) |
| #417 | `eaa2b906` | A1-extension HER2-positive 2L T-DXd repurpose |

### 13.2 Net KB additions

| Category | Count | IDs |
|---|---|---|
| Sources NEW | 17 | ToGA-Bang-2010, FLOT4-Al-Batran-2019, KEYNOTE-859-Rha-2023, DESTINY-Gastric01-Shitara-2020, DESTINY-Gastric04-Shitara-2025, SPOTLIGHT-Shitara-2023, GLOW-Shah-2023, RAINBOW-Wilke-2014, RENAISSANCE-AIO-FLOT5, CROSS-van-Hagen-2012, CheckMate-577-Kelly-2021, TIME-Biere-2012, ROBOT-van-der-Sluis-2019, OMEC-1-Kroese-2018-→-actually-2023, TCGA-Gastric-Bass-2014, Kim-Pembro-EBV-NatMed-2018, FORTITUDE-101-stub-upgrade |
| Sources cited (propagation) | 4 | CheckMate-649 across indication / regimen / RF + EBV BMA real-source upgrade |
| Indications NEW | 4 | esoph SCC ipi+nivo, esoph HER2+ trastuzumab+chemo, gastric 1L FGFR2b bemarituzumab, esoph 2L HER2+ T-DXd |
| Indications EDIT | 2 | gastric 2L HER2+ T-DXd (DG-04 outcomes added), gastric 1L PD-L1 (CPS≥1 + magnitude_of_benefit + jurisdictional split) |
| Regimens NEW | 2 | reg_ipi_nivo_esoph_scc, reg_bemarituzumab_mfolfox6 |
| Regimens EDIT | 1 | folfox_nivolumab (canonical 360 q3w added) |
| BMAs NEW | 3 | FGFR2b-membrane gastric (ESCAT IIA), EBV-positive gastric (ESCAT IIIA), HER2-low gastric tier-1 EXPLICITLY DROPPED |
| Biomarkers NEW | 1 | BIO-FGFR2B-IHC |
| RFs EDIT | 1 | rf_gastric_pdl1_cps_1_plus (jurisdictional split) |

### 13.3 Spec defects caught by agents (5 total)

Plan was authored as orchestrator's best understanding. Across the 11 chunks, agents
honest-reported **5 distinct spec defects**, refused to invent / fabricate, and
either deferred-with-rationale or auto-corrected within scope:

| # | Defect | Origin | Caught by | Resolution |
|---|---|---|---|---|
| 1 | DG-04 covers HER2-low | §4.2 line 201 | A1 + A2 (independent runs) | Repurposed to HER2-positive 2L (A1-ext); HER2-low dropped from wave (no 2026 phase-3 evidence) |
| 2 | OMEC-1 manifest year 2018 | W0-2 manifest | W0-2 agent | ID preserved verbatim with year-mismatch flag in `notes:`; rename queued in #400 backlog |
| 3 | Schema fields `kind:` / `clinical_trial_registration:` invented | §4.1 chunk template | W0-2 + B1 | Real schema uses `source_type:` + NCT in `notes:` prose; templates updated post-mortem |
| 4 | Kim NatMed PMID `29983499` | W0-5 manifest | W0-5 agent | Corrected to canonical `30013197` (real Kim ST et al., DOI 10.1038/s41591-018-0101-z) |
| 5 | Kim paper described as KEYNOTE-012 sub-analysis | W0-5 description | W0-5 agent | Real paper is independent Samsung Medical Center phase-2 (n=61); description rewritten |

Pattern that worked:
- Mandatory schema-discovery step (read `schemas/*.py` + 2-3 existing entity templates first)
- Canonical-citation verification via WebFetch / NCBI E-utilities (PubMed MCP was permission-denied)
- Hard rule "DO NOT invent fields" with free-text fallback in `notes:`
- Honest-reporting expectation in commit messages + PR bodies (e.g., bemfill explicitly flagged +1 ref error as expected DRUG-BEMARITUZUMAB unresolved)
- `actionability_review_required: true` on all tier-1 BMAs (Phase 1.5 schema clinical-signoff gate)

### 13.4 Items deferred / not landed

| Item | Reason |
|---|---|
| HER2-low gastric / esoph T-DXd | No phase-3 evidence in 2026 (DESTINY-Gastric02 not yet published; DESTINY-Breast04 is breast-only). Hold for DG-02 readout. |
| KEYNOTE-061 EBV+ subset | Not separately citable at landmark grade per W0-5; flagged in `bma_ebv_positive_gastric.notes:` as future ingest |
| `DRUG-BEMARITUZUMAB` drug stub | Same pre-existing pattern as `DRUG-PAZOPANIB`; deferred to drug-stub housekeeping chunk (+1 ref error in bemfill PR — expected) |
| Source-ID hyphenation normalisation | #400 backlog (CHECKMATE648 vs CHECKMATE-648; KEYNOTE590 vs KEYNOTE-590; OMEC-1 year-mismatch rename) |
| Phase C (multimodal — FLOT periop / CROSS phasing / definitive CRT / MIE/RAMIE / oligomet) | §17 PROPOSAL not ratified (#394). Requires human spec-author + 2/3 Clinical Co-Leads signoff per CHARTER §6.1. |
| Phase D (algorithms) | Engine-side extensions to `algo_esoph_metastatic_1l` (CM-648 ipi+nivo branch + HER2-positive adeno branch + HER2-positive 2L branch). Not blocking for clinical content. |
| Two Clinical Co-Lead signoff on tier-1 BMAs | All 3 new BMAs have `actionability_review_required: true` per Phase 1.5 — awaiting CHARTER §6.1 review. |

### 13.5 Estimate vs actual

| Metric | Original (full wave with §17) | Phase-A actual |
|---|---|---|
| Chunks | 11-14 | 11 |
| Agent-hours | 30-65 | ~14 (lots of synchronous gates + WebFetch lookups) |
| PRs | 11-14 | 11 |
| Calendar-days | 6-16 | 3 (2026-05-04 through 2026-05-07) |

Phase-A (no §17 dependency) ran cleanly under estimate. Phase C blocked indefinitely
on §17 ratification (human-in-the-loop calendar gate, not a work gate).

---

## 14. Post-merge implementation follow-up (added 2026-05-07)

After the GI-2 routing and structural-validation work, the remaining
architecture constraint is explicit: there is no mutable runtime database to
"fill" from the PWA or engine. Canonical clinical content remains Git-tracked
YAML under `knowledge_base/hosted/content/`; the browser consumes immutable
bundles generated by `scripts/build_site.py`.

Implementation follow-up completed in PR #449:

- Added a loader contract that blocks any Algorithm from routing to an active
  treatment Indication with `recommended_regimen: null`, unless the Indication
  is explicitly a non-regimen track such as surveillance, local therapy,
  transplant, trial, palliative, procedural, or supportive care.
- Preserved no-KB-fill mode for gastric FGFR2b: the authored FGFR2b
  indication remains unrouted until a reviewed non-null regimen exists.
- Kept esophageal D1-thin routing limited to already-authored A1 entities:
  `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO` and
  `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO`.
- Completed the structural V1 cleanup to 0 schema errors, 0 ref errors, and
  0 contract errors; remaining 524 warnings are quality/curation debt, not
  broken graph integrity.
- Added a scoped KB validation workflow gate for validator/contracts/routing/
  legacy-normalization/PWA smoke tests, with manual dispatch for release
  verification.
- Added the minimal PWA shell for `/try.html`: manifest, service-worker
  precache, and a visible build/cache/offline/version panel.

Next work should prioritize the 524 warnings by patient-facing blast radius:
free-text required/desired tests, hard contraindications, supportive care, and
draft/source-signoff warnings. PWA installability polish should remain a shell
layer on top of hash-stamped bundles and must keep exposing build/signoff state
rather than making partially curated content look final.
