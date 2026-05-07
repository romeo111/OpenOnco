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

## 13. Post-A1/A2 revision (added 2026-05-07, after #408/#409 merged)

Latest committed state through `adc073474` changes the remaining plan in
three material ways:

1. A1 is partially delivered, but the HER2-low/DG04 item was correctly
   stopped because the source is HER2-positive 2L gastric/GEJ, not HER2-low.
2. A2 is partially delivered, but the FGFR2b indication is not executable
   by the Plan engine yet because it has `recommended_regimen: null` and
   no algorithm branch.
3. D1 is now more urgent than originally framed: the KB contains new
   indications that are valid entities but invisible to patient routing
   until algorithms are updated.

### 13.1 Delivered since post-W0

| Item | Status | Notes |
|---|---|---|
| `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO` | delivered + routed | Uses new `REG-IPI-NIVO-ESOPH-SCC`; esoph 1L chemo-sparing branch implemented in this branch. |
| `REG-IPI-NIVO-ESOPH-SCC` | delivered | Correctly avoids reusing melanoma/RCC ipi+nivo dose patterns. |
| `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO` | delivered + routed | Reuses `REG-TRASTUZUMAB-CHEMO-TOGA`; esoph 1L HER2+ adeno branch implemented in this branch. |
| `BIO-FGFR2B-IHC` | delivered | Distinct from FGFR2 amplification; appropriate protein-IHC biomarker. |
| `BMA-FGFR2B-MEMBRANE-GASTRIC` | delivered | ESCAT IIA / moderate confidence; still requires clinical signoff. |
| `IND-GASTRIC-METASTATIC-1L-FGFR2B-BEMARITUZUMAB` | delivered as stub | `recommended_regimen: null`; not ready for engine routing. |
| `BMA-EBV-POSITIVE-GASTRIC` | delivered | Explanatory/subtype-router BMA; primary-source backfill still needed. |

Validator delta reported in the commits and rechecked locally: the new
GI-2 files do not add schema, referential-integrity, or contract-warning
regressions. Global baseline remains non-green (`schema=91`, `ref=179`,
`contract_warnings=217`).

### 13.2 Corrected deferrals

The following original A1/A2 items should not be dispatched as written:

| Original item | Revised decision |
|---|---|
| `ind_esoph_metastatic_1l_her2_low_t_dxd` | Keep deferred. DG04 is HER2-positive 2L gastric/GEJ post-trastuzumab, not HER2-low esophageal 1L. |
| `bma_her2_low_gastric` | Keep deferred until a true HER2-low gastric primary source exists. Do not use DG04 for HER2-low. |
| gastric/esophageal TROP2 BMAs | Keep skipped. No phase-3 actionable data for this wave. |
| separate `bio_ebv.yaml` | Keep skipped. `BIO-EBV-STATUS` already exists. |
| separate `bma_cldn18_2_gej_esoph_adeno` | Keep skipped unless a future branch needs a distinct esophageal/GEJ routing entity. Existing gastric/GEJ CLDN18.2 coverage already mentions GEJ. |

### 13.3 New immediate blockers

#### Blocker 1 - bemarituzumab regimen missing

`IND-GASTRIC-METASTATIC-1L-FGFR2B-BEMARITUZUMAB` intentionally has:

```
recommended_regimen: null
```

This keeps validation stable but prevents meaningful Plan materialization.
Before D1 routes any patient to this indication, create a dedicated regimen:

- `REG-BEMARITUZUMAB-MFOLFOX6`
- file: `knowledge_base/hosted/content/regimens/reg_bemarituzumab_mfolfox6.yaml`
- components: bemarituzumab + mFOLFOX6 backbone
- mandatory supportive/monitoring note: baseline and serial ophthalmology
- status: draft / pending clinical signoff
- source caveat: FIGHT phase 2 + FORTITUDE-101 stub until final phase-3 publication

If the regimen cannot be authored with enough source support, D1 must not
route to the indication; keep it surfaced only through BMA/actionability.

#### Blocker 2 - esophageal 1L algorithm is stale

`ALGO-ESOPH-METASTATIC-1L` currently outputs only:

- `IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC`
- `IND-ESOPH-METASTATIC-1L-PEMBRO-CHEMO`

It must be extended to include:

- `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO`
- `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO`

Minimum branch behavior:

- ESCC + CPS >=1 + chemo-sparing preference / chemo unsuitability ->
  `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO`
- ESCC + rapid response/high-burden preference -> keep
  `IND-ESOPH-METASTATIC-1L-NIVO-CHEMO-SCC`
- EAC/GEJ Siewert I + HER2-positive -> route to
  `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO`
- EAC/GEJ Siewert I + HER2-negative/unknown -> existing pembro+chemo path

Do not add the HER2-low T-DXd branch until the source issue is resolved.

#### Blocker 3 - gastric 1L algorithm does not know FGFR2b

`ALGO-GASTRIC-METASTATIC-1L` currently routes HER2, CLDN18.2, and PD-L1
but not FGFR2b. Add FGFR2b only after `REG-BEMARITUZUMAB-MFOLFOX6` exists.

Proposed priority order:

1. HER2-positive -> TOGA / HER2 track
2. MSI-H -> pembro branch when dedicated indication exists
3. CLDN18.2-positive HER2-negative -> zolbetuximab branch
4. FGFR2b-positive HER2-negative MSI-stable CLDN18.2-negative -> bemarituzumab branch
5. PD-L1 CPS >=1 HER2-negative -> FOLFOX+nivo branch

For dual CLDN18.2+/FGFR2b+ cases, keep CLDN18.2 ahead of FGFR2b until
FORTITUDE-101 final phase-3 data is available, matching the controversy
block in the new FGFR2b indication.

### 13.4 Revised remaining chunks

| Chunk | Status | Scope now |
|---|---|---|
| A1-redux | mostly done | Only unresolved item is HER2-low/DG04 clarification; no implementation until source intent is corrected. |
| A2-redux | mostly done | Only unresolved items are primary-source backfill for EBV/FIGHT/FORTITUDE and the bemarituzumab regimen. |
| B1 | done earlier | CPS/nivo reconciliation already landed in prior commits; no new B1 chunk needed unless validator/audit finds regression. |
| B2 regimen-fill | NEW | Add `REG-BEMARITUZUMAB-MFOLFOX6` or explicitly freeze the FGFR2b indication as BMA-only. |
| D1-thin | partially done | Esoph 1L branches are implemented for already-authored ipi+nivo and HER2+ adeno indications. Gastric FGFR2b remains deferred until B2 lands. |
| S1 source cleanup | NEXT/parallel | Fix source-id hygiene and TODO stubs: OMEC year, CheckMate/KEYNOTE hyphenation backlog, FORTITUDE/FIGHT source maturity, EBV primary sources. |
| V1 validation debt | NEXT/parallel | Reduce global baseline errors enough that release gates can distinguish new regressions from old debt. |
| C1-C5 | still blocked | No change: multimodal/periop/surgery/RT/OMEC remains blocked by §17 schema ratification. |

### 13.5 Updated execution order

Recommended order from the current HEAD:

1. **B2 regimen-fill decision**: either author `REG-BEMARITUZUMAB-MFOLFOX6`
   or mark FGFR2b indication "not routable until regimen exists".
2. **D1-thin algorithms**:
   - done: `ALGO-ESOPH-METASTATIC-1L` now routes ipi+nivo for ESCC CPS>=1
     chemo-sparing profiles and trastuzumab+chemo for HER2+ EAC/GEJ Siewert I;
   - update `ALGO-GASTRIC-METASTATIC-1L` for FGFR2b only if B2 is complete.
3. **S1 source cleanup**:
   - mature `SRC-FORTITUDE-101` and add/confirm FIGHT source support;
   - add EBV primary sources if BMA remains in the actionability layer;
   - schedule source ID normalisation separately from clinical logic.
4. **V1 validation debt burn-down**:
   - target changed-domain files first (`regimens`, `indications`, `sources`);
   - keep baseline-count reporting in every chunk until full green is realistic.
5. **§17 ratification** before C1-C5:
   - do not dispatch FLOT/CROSS/MIE/OMEC implementation until schema is ratified.

### 13.6 Revised estimates

| Scope | Previous estimate | Revised estimate |
|---|---:|---:|
| Remaining non-§17 work | 3-5 chunks | 3-4 chunks (`B2`, `D1-thin`, `S1`, optional `V1-slice`) |
| Remaining §17-blocked work | 5 chunks | unchanged |
| Calendar risk | §17 + clinical signoff | unchanged, but D1-thin can ship before §17 |
| Highest-risk next chunk | A2 BMA expansion | now `B2` if regimen data is thin; otherwise `D1-thin` |

### 13.7 Acceptance criteria for the next chunk

For `B2`:

- Adds no schema/ref/contract regressions against current baseline.
- Does not invent a full registration claim for bemarituzumab.
- Keeps access pathway explicit: trial / named-patient / charitable only.
- Includes ophthalmology monitoring in regimen notes or linked monitoring.

For `D1-thin`:

- Adds new output indications to algorithm `output_indications`.
- Adds deterministic branches for ESCC ipi+nivo and HER2+ EAC.
- Does not route to FGFR2b bemarituzumab unless `recommended_regimen` is non-null.
- Adds/updates focused tests covering at least:
  - ESCC CPS>=1 chemo-sparing profile -> ipi+nivo;
  - HER2+ EAC -> trastuzumab+chemo;
  - HER2-negative EAC -> existing pembro+chemo;
  - FGFR2b+ gastric behavior gated by the B2 decision.

### 13.8 Implementation reality check: no runtime database population

After reading the implementation, this plan must not assume there is a
mutable runtime "database" that can be filled from the PWA, engine, or
agent workflow.

Actual storage model:

- Canonical KB is Git-tracked YAML under `knowledge_base/hosted/content/`.
- The browser receives generated immutable bundles from `scripts/build_site.py`
  (`openonco-engine-core.zip` + per-disease zips).
- `patient_plans/` persistence is gitignored local JSON/JSONL for generated
  Plan artifacts and provenance events only; it is not KB storage.
- `scripts/tasktorrent/upsert_contributions.py` is maintainer-only mechanical
  sidecar upsert after review. It defaults to dry-run and does not enforce
  clinical signoff itself.
- `legacy/storage/research_db.py` is an old SQLite autoresearch store, not
  the active OpenOnco KB.

Therefore "fill the database" is not an available operation in the current
architecture. Any new Regimen/Indication/BMA is a source-controlled clinical
content change, not a runtime DB write.

#### No-KB-fill mode

If the current operating constraint is "do not add more canonical KB content",
then the remaining plan changes as follows:

| Item | Previous plan | No-KB-fill decision |
|---|---|---|
| `REG-BEMARITUZUMAB-MFOLFOX6` | Add as B2 regimen-fill | Do not add. Keep FGFR2b surfaced as BMA/actionability only. |
| `IND-GASTRIC-METASTATIC-1L-FGFR2B-BEMARITUZUMAB` | Route after regimen exists | Do not route. It has `recommended_regimen: null`; routing would create a Plan track without regimen materialization. |
| Gastric FGFR2b algorithm branch | Add after B2 | Defer. Algorithm must not select an unroutable indication. |
| Esophageal ipi+nivo / HER2+ branches | Add in D1-thin | Allowed only as integration of already-merged KB entities, not new content authoring. |
| Source cleanup / TODO stubs | S1 source cleanup | Defer unless it is fixing existing broken references required for validation gates. |
| Validation debt | V1 | Still valid, because this is implementation health, not KB expansion. |

Under no-KB-fill mode, the next implementation-safe step is:

1. Update `ALGO-ESOPH-METASTATIC-1L` to expose already-existing delivered
   indications (`SCC-IPI-NIVO`, `HER2-TRASTUZUMAB-CHEMO`) if this is
   considered routing integration rather than new clinical content. **Done in
   this branch.**
2. Add tests proving the new branches are deterministic and do not regress
   existing ESCC/EAC defaults.
3. Leave gastric FGFR2b as render-time actionability context only until a
   reviewed regimen entity exists.
4. Add a guard/test that no Algorithm can route to an Indication with
   `recommended_regimen: null` unless its `plan_track` is explicitly
   `trial`, `surveillance`, or another non-regimen track.

This replaces "populate the database" with "make existing authored entities
reachable safely, and prevent unroutable authored entities from entering
Plan selection."

### 13.9 Coverage/normalization document check

Reviewing the nearby coverage and normalization documents does not change the
no-runtime-DB conclusion, but it tightens how the next GI-2 work should be
framed.

`contributions/drug-class-normalization/normalization_report.yaml` is a
negative-finding audit: all 216 hosted Drug `drug_class` values were checked
and no actionable normalization clusters were found. Do not schedule GI-2 work
around drug-class cleanup unless a new audit finds concrete violations.

`docs/kb-coverage-strategy.md` and `docs/kb-coverage-matrix.md` do affect this
plan. They require future chunks to name the exact coverage cell they move and
to separate field presence from verified clinical quality. For the current GI-2
slice:

- A `recommended_regimen: null` indication can improve content presence, but
  it must not be counted as route-ready Plan behavior.
- Algorithm work should be declared as routing integration for already-authored
  entities, not as broad coverage-fill.
- Any PWA display should expose verification/signoff/freshness state next to
  GI-2 recommendations, especially while global validation debt remains.
- Speculative cleanup chunks should start with an audit threshold, matching the
  drug-class normalization lesson.

Implementation follow-up completed in this branch:

- Added a loader contract that blocks any Algorithm from routing to an active
  treatment Indication with `recommended_regimen: null`.
- Kept explicit non-regimen tracks allowed (`surveillance`, `local_therapy`,
  `transplant`, `trial`, `palliative`, and adjacent procedural/supportive
  tracks).
- Reclassified existing routed no-regimen active tracks:
  `IND-MF-EARLY-1L-SKIN-DIRECTED` -> `local_therapy` and
  `IND-GCT-SALVAGE-2L-HDCT-ASCT` -> `transplant`.
- Implemented esophageal D1-thin routing for already-authored A1 indications:
  `IND-ESOPH-METASTATIC-1L-SCC-IPI-NIVO` and
  `IND-ESOPH-METASTATIC-1L-HER2-TRASTUZUMAB-CHEMO`.

### 13.10 V1 validation-debt slice completed

The first V1 slice is implementation health, not new clinical KB content.
It addresses the old generated regimen shape that blocked full KB loading.

Implemented:

- `Regimen` schema now accepts legacy `agents:` payloads and normalizes them
  to canonical `components:` in memory.
- Legacy `DRG-*` component IDs are mapped to current `DRUG-*` IDs, including
  special cases where the canonical ID is not a direct prefix replacement:
  `DRG-FLUOROURACIL` -> `DRUG-5-FLUOROURACIL` and
  `DRG-RADIUM223` -> `DRUG-RADIUM-223`.
- Legacy `total_planned_cycles` is copied to `total_cycles`.
- Regimens missing `name` receive a deterministic fallback from their `REG-*`
  ID so they can materialize in Plans.
- Loader stores the normalized in-memory payload, so downstream engine and
  render code see canonical `components`.
- Legacy free-text `mandatory_supportive_care` entries now produce contract
  warnings instead of ref errors; real `SUP-*` IDs remain strict references.

Validation impact:

| Metric | Before | After |
|---|---:|---:|
| Global schema errors | 91 | 65 |
| Global ref errors | 179 | 154 |
| Contract errors | 0 | 0 |
| Regimen schema errors | 26 | 0 |
| Regimen ref errors | 22 | 6 |

Remaining regimen-specific blockers are now concrete missing Drug entities:
`DRUG-CABAZITAXEL`, `DRUG-MESNA`, `DRUG-NAL-IRI`,
`DRUG-MITOMYCIN-C`, and `DRUG-PAZOPANIB`.

### 13.11 V1 missing-drug slice completed

The second V1 slice adds thin Drug entities for the five concrete component
refs surfaced by the legacy-regimen compatibility layer:

- `DRUG-CABAZITAXEL`
- `DRUG-MESNA`
- `DRUG-NAL-IRI`
- `DRUG-MITOMYCIN-C`
- `DRUG-PAZOPANIB`

These are intentionally minimal source-aware records. They unblock regimen
materialization and referential integrity, but they are not complete drug
monographs. Detailed Ukraine availability and full label metadata remain
future curation work.

Validation impact:

| Metric | After compatibility slice | After missing-drug slice |
|---|---:|---:|
| Global schema errors | 65 | 65 |
| Global ref errors | 154 | 148 |
| Contract errors | 0 | 0 |
| Regimen ref errors | 6 | 0 |

Next V1 slice:

1. Attack indication ref errors, because 90 of the remaining 148 ref errors
   are in `indications/`.
2. Then resolve algorithm refs, which account for 50 remaining errors.
3. Keep PWA work behind this gate; installability should not make a partially
   valid KB feel production-ready.
