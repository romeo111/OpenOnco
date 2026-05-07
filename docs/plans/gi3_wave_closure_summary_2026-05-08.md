# GI-3 wave closure summary

**Stamp:** 2026-05-08
**Master HEAD at closure:** `6915dbae`
**Total PRs in GI-3:** 17 (+ 1 cape-CRT follow-up in flight = 18)

---

## 1. Phase ledger

| Phase | PRs | Description |
|---|---|---|
| **W0 sources** | #454, #455, #456 | 11 NEW primary trials (PDAC × 4, Cholangio × 4, CRC × 3); 4/11 PMIDs corrected at agent-side |
| **Phase A wave 1** | #460, #461, #462 | CRC liver-limited oligomet (mirrors GI-2 C5); cholangio 1L IO (TOPAZ-1 + KEYNOTE-966); PDAC NAPOLI-3 NALIRIFOX 1L |
| **Phase A wave 2** | #467, #468 | Cholangio HER2 zanidatamab (new BMA + drug + indication); IDH1 ivosidenib (BMA reused) |
| **Phase B** | #466 | IDEA stratification 3 vs 6 mo CapOx adjuvant (low/high-risk via ExpectedOutcomes.extra) |
| **Phase C wave 1** | #471, #472 | C1 PDAC adjuvant mFOLFIRINOX (§17 1-phase); C3 RAPIDO rectal TNT short-course (§17 3-phase + new RC + new TME Surgery) |
| **Phase C wave 2** | #476, #477 | C2 PDAC borderline-resectable NORPACT-1 (§17 3-phase + Whipple Surgery promotion); C4 PRODIGE-23 rectal TNT long-course (§17 3-phase + new LCCRT) |
| **Phase C wave 3** | #480 | C5 PDAC LAPC chemoradiation (§17 2-phase + new LAPC RC) |
| **Phase D2** | #482 | 8 algorithms (5 EDIT + 3 NEW); engine smoke 10/10 |

## 2. Net KB additions

| Category | Count |
|---|---|
| Sources NEW | 11 |
| Indications NEW | 11 |
| Indications EDIT | 2 (CRC adjuvant CapOx; cholangio gem+cis controversies) |
| Regimens NEW | 4 (NALIRIFOX, ivosidenib, zanidatamab, mFOLFIRINOX, durva-gem-cis, pembro-gem-cis) — actually 6 |
| BMAs NEW | 1 (HER2-amp cholangio) |
| Biomarkers NEW | 0 (existing BMAs reused — IDH1, BIO-HER2-SOLID) |
| Drugs NEW | 4 (ivosidenib, zanidatamab, liposomal irinotecan, [bemarituzumab from earlier]) |
| RFs NEW | 1 (CRC oligomet liver definition) |
| Algorithms EDIT | 5 |
| Algorithms NEW | 3 (PDAC resectable periop, rectal LARC TNT, PDAC LAPC) |
| Surgery NEW | 2 (Whipple, TME proctectomy) |
| RadiationCourse NEW | 3 (SCRT 25/5, LCCRT 50.4/28, LAPC 50.4/28) |
| Phased Indications | 5 (PDAC adj, PDAC BR, RAPIDO TNT, PRODIGE-23 TNT, PDAC LAPC) |

## 3. §17 schema validated end-to-end

Phase enum stages exercised in production:
- `neoadjuvant` — RAPIDO RT phase, PRODIGE-23 CRT phase, PDAC BR FOLFIRINOX
- `induction` — RAPIDO chemo, PRODIGE-23 FOLFIRINOX, PDAC LAPC FOLFIRINOX
- `surgery` — D2 lymphadenectomy, Whipple, TME proctectomy
- `adjuvant` — PDAC mFOLFIRINOX, PDAC BR adj
- `definitive` — PDAC LAPC CRT
- (`maintenance` not yet exercised — future use case)

Phase type enum exercised:
- `chemotherapy`, `radiation`, `chemoradiation`, `surgery` — all production
- (`targeted_therapy`, `immunotherapy` not yet — future)

XOR rule (exactly one of regimen_id / surgery_id / radiation_id per phase) held across all 14+ §17-consumer indications. RadiationCourse `concurrent_chemo_regimen` correctly used for concurrent CRT (CROSS, PRODIGE-23, LAPC).

## 4. Engine routing 10/10 verified (D2 PR #482 smoke)

| # | Patient profile | Algorithm | → Indication |
|---|---|---|---|
| 1 | Cholangio 1L IO-eligible | ALGO-CHOLANGIO-1L | TOPAZ-1 durva+chemo |
| 2 | Cholangio IDH1+ 2L | ALGO-CHOLANGIO-2L | ivosidenib |
| 3 | PDAC 1L ECOG 1 | ALGO-PDAC-METASTATIC-1L | NALIRIFOX or FOLFIRINOX |
| 4 | CRC liver-only oligomet | ALGO-CRC-METASTATIC-1L step 0 | IND-CRC-OLIGOMET-LIVER-LIMITED |
| 5 | CRC stage III low-risk | ALGO-CRC-ADJUVANT | CapOx 3-mo per IDEA |
| 6 | PDAC resectable | ALGO-PDAC-RESECTABLE-PERIOP | mFOLFIRINOX adj |
| 7 | PDAC borderline | same | IND-PDAC-BORDERLINE-NEOADJ-FOLFIRINOX |
| 8 | LARC | ALGO-RECTAL-LOCALLY-ADVANCED-TNT | RAPIDO or PRODIGE-23 |
| 9 | PDAC unresectable T4 | ALGO-PDAC-LAPC | IND-PDAC-LAPC-CHEMORADIATION |
| 10 | **Regression**: existing PDAC FOLFIRINOX | preserved | unchanged |

## 5. Spec defects caught (cumulative)

GI-3 wave continued the pattern of agents catching planning-stage defects:

| # | Defect | Caught by | Resolution |
|---|---|---|---|
| W0-PDAC | 3/4 PMIDs wrong (PRODIGE-24, NAPOLI-3, ESPAC-5F) | W0-PDAC agent | All corrected via NCBI esearch |
| W0-CHOLANGIO | ClarIDHy PMID wrong (32758454 → 32416072) | W0-CHOLANGIO agent | Corrected |
| W0-CHOLANGIO | NORPACT-1 PMID not in spec | W0-PDAC agent | Located via search → 38237621 |
| C2 NORPACT-1 framing | NORPACT-1 enrolled resectable (not BR) | C2 agent | Cited as feasibility evidence; BR rec rests on NCCN/ESMO extrapolation; evidence_level moderate |
| C2 Whipple `applicable_diseases` | Cholangio is subtype-agnostic; only dCCA Whipple-resectable | C2 agent | DIS-CHOLANGIOCARCINOMA NOT added; subtype-split flagged in notes |
| C4 / C5 concurrent capecitabine | REG-CAPECITABINE-CRT-CONCURRENT doesn't exist | Both agents | concurrent_chemo_regimen: null + audit; follow-up chunk #483 closes this |
| D2 algo collision | ALGO-CRC-ADJUVANT vs ALGO-CRC-METASTATIC-1L state-agnostic | D2 agent | Pre-existing per stash check; flagged for engine refactor |

**Total cumulative session defects:** ~12 (spec defects + KB integrity issues caught + auto-resolved by agents).

## 6. Items deferred / not landed

| Item | Reason |
|---|---|
| A5 CRC peritoneal CRS+HIPEC (PRODIGE-7) | Trial was negative for HIPEC benefit; nuanced authoring needed; deferred |
| Watch-and-wait protocol post-cCR rectal | No current schema support; defer to potential §18 |
| LAP07 / CONKO-007 source stubs | Cited via NCCN/ESMO consensus chain in C5; primary stubs deferred |
| KRAS G12C extrapolation PDAC | DRUG-SOTORASIB exists in CRC; PDAC indication deferred |
| HER2-positive PDAC trastuzumab+pertuzumab MyPathway | Out of v0.1 scope |
| EBV+ subset analysis cholangio (KEYNOTE-966) | Not separately citable at landmark grade |
| Source-ID renormalisation #400 | Low-priority cleanup; large blast radius |
| ALGO-CRC state-agnostic collision fix | Engine refactor scope, not chunk-task |
| Phase 1.5 BMA two-Clinical-Co-Lead signoffs | Process gate, dev-mode-exempt v0.1 |

## 7. Estimate vs actual

| Metric | Original GI-3 plan | Actual |
|---|---|---|
| Chunks | 14-18 | 17 |
| Agent-hours | 35-60 | ~25-30 |
| PRs | 14-18 | 17 (+ #483 in flight) |
| Calendar-days | 5-12 | 1 (2026-05-08) |

**Significantly under estimate** thanks to parallel dispatch (3-4 chunks per wave).

## 8. Reference docs

- `docs/plans/gi3_wave_pancreaticobiliary_crc_2026-05-08.md` — GI-3 plan (template)
- `docs/plans/refactor_lessons_2026-05-07.md` — refactor lessons (10+ patterns + §11 GI-3 closure findings)
- `docs/plans/gi2_long_tail_followups_2026-05-07.md` — GI-2 long-tail backlog
- `docs/plans/gi2_wave_gastric_esophageal_2026-05-04-1730.md` — GI-2 plan
- `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §17 — Surgery + RadiationCourse + IndicationPhase (ratified)
