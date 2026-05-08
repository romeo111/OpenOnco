# Session tally + forward plan

**Stamp:** 2026-05-09
**Master HEAD at pause:** `b10dc242` (post PUL-A2 MARIPOSA merge)
**Sessions span:** 2026-05-04 → 2026-05-09
**Status:** PAUSED — 2 chunks still in flight (PUL-A4 DeLLphi tarlatamab, will report on completion)

---

## 1. Session entity tally

### 1.1 Content entities ADDED

| Category | NEW | Notes |
|---|---|---|
| **Sources** | **36** | GI-2: 20, GI-3: 11, PUL: 5 (+ 1 PALETTE rewrite from skeleton) |
| **Indications** | **23** | GI-2: 9, GI-3: 11, PUL: 3 (A1+A2+A3); A4 DeLLphi pending |
| **Regimens** | **11** | GI-2: 2, GI-3: 6, PUL: 2 (FLAURA-2, ADRIATIC), cape-CRT shared: 1; A2 ami+laz pending +1 |
| **BMAs** | **4** | HER2-low gastric, FGFR2b gastric, EBV gastric, HER2-amp cholangio |
| **Biomarkers** | **1** | BIO-FGFR2B-IHC |
| **Drugs** | **5** | bemarituzumab, pazopanib (GI-2), liposomal-irinotecan, ivosidenib, zanidatamab (GI-3); tarlatamab pending +1 |
| **Surgery (procedures/)** | **6** | D2 lymphadenectomy, esophagectomy × 3 (open/MIE/RAMIE), Whipple, TME proctectomy |
| **RadiationCourse** | **5** | CROSS neoadj, definitive esoph SCC, SCRT 25/5 rectal, LCCRT 50.4/28 rectal, LAPC PDAC |
| **RFs** | **2** | OMEC oligomet definition, CRC oligomet liver definition |
| **Algorithms** | **5** | gastric resectable periop, esoph definitive 1L (GI-2 D2); PDAC resectable periop, rectal LARC TNT, PDAC LAPC (GI-3 D2) |
| **TOTAL content NEW** | **~98** | (24 entity types × diseases × intent space) |

### 1.2 Content entities EDITED (preserving counts)

- ~25 indication EDITs (citation upgrades, controversy blocks, magnitude_of_benefit additions, recommended_regimen backfills, phases populated, IDEA stratification)
- ~5 regimen EDITs (canonical 360 q3w nivo, capecitabine-CRT FK backfill, etc.)
- ~9 algorithm EDITs (4 GI-2 D1, 5 GI-2 D2 + GI-3 D2)
- 1 RF EDIT (jurisdictional split)
- 5 disease re-stamps (GI: gastric, esophageal, pdac, hcc, crc → proposal_status full)

### 1.3 Infrastructure (§17 schema refactor)

- 3 NEW Pydantic models (Surgery, RadiationCourse, IndicationPhase)
- 4 NEW enums (SurgeryIntent, RadiationIntent, IndicationPhaseStage, IndicationPhaseType)
- Loader extensions: ENTITY_BY_DIR + REF_FIELDS + per-entity FK rules
- 28 NEW tests + 3 fixtures
- Spec §17 PROPOSAL → ratified

### 1.4 PRs merged

- GI-2 wave: 14 PRs
- §17 schema: 4 PRs (planning + lessons + impl + §8)
- GI-3 wave: 17 PRs
- Cape-CRT follow-up: 1 PR
- PUL wave (so far): 4 PRs (W0 + A1 + A2 + A3)
- Docs/lessons updates: ~7 PRs
- **Total: ~47 PRs merged** (PUL-A4 in flight will be ~48; this tally PR ~49)

### 1.5 Entity count growth

| Marker | Count |
|---|---|
| Master baseline at session start (~2790-2799) | ~2790 |
| Master HEAD post PUL-A2 (`b10dc242`) | ~2993 |
| **Net entity growth** | **~+200** (additions + algorithm count + procedures + radiation_courses + new schema-validated entities) |

---

## 2. Forward plan (resumable from this point)

### 2.1 Pulmonary wave continuation (immediate)

#### Wave 1 closure (in flight)
- ⏳ **PUL-A4 DeLLphi tarlatamab** (#491) — NEW drug + regimen + indication; SCLC RR DLL3 BiTE

#### Wave 2 (pulmonary Phase A continued)
- **PUL-A5** NSCLC perioperative pembro (KEYNOTE-671) — §17 multi-phase (neoadj+adj × IO+chemo)
- **PUL-A6** NSCLC adjuvant ATEZO (IMpower010) — single-phase adjuvant atezo for stage II-III post-resection
- **PUL-A7** Mesothelioma 2L nivo-mono (CONFIRM trial) — verify exists; cite if missing
- **PUL-A8** NSCLC stage IV nivo+ipi+chemo (CheckMate-9LA) — 1L IO+chemo combo

#### Wave 3 (pulmonary Phase D + extended)
- **PUL-D1** Algorithm extensions for FLAURA-2 / MARIPOSA / ADRIATIC / DeLLphi (algo_nsclc_metastatic_1l, algo_sclc_2l updates)
- **PUL-D2** Algorithm `algo_nsclc_resectable_periop` (NEW) for KN-671 routing
- Optional W0-extra sources: KEYNOTE-789, ATTLAS, ATALANTE, KEYNOTE-585 (gastric — already done), CheckMate-9LA, IMpower010 if missing

### 2.2 Cross-cutting follow-ups (low priority backlog)

From `docs/plans/gi2_long_tail_followups_2026-05-07.md` + GI-3 closure:
- DESTINY-Gastric02 watch (HER2-low Western gastric)
- Source-ID renormalisation #400 (hyphenation cleanup)
- ALGO-CRC-ADJUVANT vs ALGO-CRC-METASTATIC-1L state-agnostic collision (engine refactor)
- A5 CRC peritoneal CRS+HIPEC PRODIGE-7 (controversial; defer)
- HER2+ esoph adeno coverage gap (ToGA extrap is C2 GI-2 partial)
- Phase 1.5 BMA two-Clinical-Co-Lead signoff queue (process gate)

### 2.3 Future domain waves

After pulmonary closure, candidate next domains:
- **Hematologic** — DLBCL (R-CHOP, polatuzumab POLARIX, axi-cel/liso-cel CAR-T 2L), MM (DVRd/Dara-VRd, teclistamab BiTE), MZL/FL refinements, CLL (acalabrutinib AMPLIFY, venetoclax CLL14)
- **Breast** — Adjuvant CDK4/6i (monarchE abemaciclib, NATALEE ribociclib), DB-04/05 HER2-low, KEYNOTE-522 TNBC, sacituzumab post-T-DXd
- **GU** — Prostate (PARPi PROpel/MAGNITUDE, AR pathway 1L mCRPC), RCC pembro+axi alternatives, urothelial enfortumab+pembro 1L (EV-302), PEACE-1
- **Gynecological** — Cervical pembro+chemo/bev (KN-826), endometrial dostarlimab+chemo (RUBY) and pembro+chemo (NRG-GY018), ovarian PARP maintenance refinements

### 2.4 Schema / engine refactor candidates

- **§18 PROPOSAL** — Patient-trajectory entity (longitudinal): tracks treatment+response history; needed for "patient X failed line N → eligible for line N+1 indications"
- Engine fix for state-agnostic algo collision (CRC adjuvant vs metastatic_1l)
- Render layer §17.4 step 5 (phased timeline UI) — currently just structural data; render not yet phase-aware

---

## 3. Resumption checklist for next session

When resuming:
1. Verify master HEAD (should be ≥ `b10dc242`); pull if behind
2. Check PUL-A4 DeLLphi status (issue #491 — should be merged or have agent report)
3. Read `docs/plans/refactor_lessons_2026-05-07.md` §11 + §12 if new findings landed
4. Read this doc + `docs/plans/gi3_wave_closure_summary_2026-05-08.md` for context
5. Consider current backlog priorities — pulmonary Wave 2 is next-most-natural extension
6. Or pivot to new domain (heme, breast, GU, gyn) — see §2.3

---

## 4. Reference docs

- `docs/plans/gi2_wave_gastric_esophageal_2026-05-04-1730.md` — GI-2 plan
- `docs/plans/gi3_wave_pancreaticobiliary_crc_2026-05-08.md` — GI-3 plan
- `docs/plans/gi2_long_tail_followups_2026-05-07.md` — long-tail backlog
- `docs/plans/gi3_wave_closure_summary_2026-05-08.md` — GI-3 17-PR ledger
- `docs/plans/refactor_lessons_2026-05-07.md` — 11 sections / 36+ patterns
- `docs/plans/schema_17_refactor_2026-05-07.md` — §17 design + execution
- `docs/plans/q_axis_dispatch_template_2026-05-01.md` — chunk-task dispatch template
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` — canonical schema (§17 ratified)
- `CLAUDE.md` — repo conventions
