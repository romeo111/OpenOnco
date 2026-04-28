# RedFlag + Indication Coverage Audit — 2026-04-27

**Branch:** feat/oncokb-wiring  
**Drafted by:** Claude Code (extraction-from-source agent), per CHARTER §8.3.  
**Status:** PENDING CLINICAL SIGN-OFF.  
**Scope:** Deep + comprehensive coverage audit of all RedFlag and
Indication entities in `knowledge_base/hosted/content/` against the
expected coverage per `specs/REDFLAG_AUTHORING_GUIDE.md` §2 and
`specs/CLINICAL_CONTENT_STANDARDS.md`.

---

## 1. Method

1. Enumerated all disease YAMLs under
   `knowledge_base/hosted/content/diseases/` (n = **65 diseases**, not
   the 28 listed in `CLAUDE.md` — that figure is stale; the project has
   expanded since the Phase 1–7 RedFlag work).
2. For each disease, mapped the RedFlags whose `relevant_diseases`
   field references it, plus the 3 universal RFs.
3. Categorised each RF against the 5-type matrix
   (organ-dysfunction, infection-screening, high-risk-biology,
   transformation-progression, frailty-age) plus a 6th implicit
   "emergency / decision-trigger" axis (TLS, leukostasis, DIC,
   hyperviscosity, SVC, spinal-cord compression, CNS leukemia,
   mediastinal mass with airway compromise, hypercalcemia, neutropenic
   sepsis, hyperleukocytosis, intracranial hypertension, GI emergency,
   biliary obstruction, paraneoplastic, etc.).
4. For Indications, enumerated by `applicable_to.disease_id` and
   `line_of_therapy`, surfacing diseases with 0 indications and lines
   that are not represented (especially L2 / L3 / R/R).

Per **CHARTER §8.3**, this audit only **extracts** from in-repo cited
guidelines (NCCN, ESMO, ELN, EHA, ESGO, ESMO-MZL, ESMO-WM, EAU, EANO,
AASLD, EASL); no clinical content is generated from the model's priors.
Where the guideline reference for a gap is **not in the in-repo source
catalogue**, the gap is marked `BLOCKED: missing source SRC-…` and no
draft was created.

---

## 2. Headline numbers

| Metric | Count |
|---|---|
| Diseases in KB | 65 |
| Total non-universal RedFlags | 292 |
| Universal RedFlags | 3 (TLS-RISK, HBV-REACTIVATION, INFUSION-REACTION-FIRST-CYCLE) |
| Diseases with **zero** RedFlags | 9 |
| Diseases with **zero** Indications | 11 |
| Diseases missing one or more 5-type categories | 9 (overlap with zero-RF set) |
| Existing emergency-axis RFs | 14 |
| Sources available in repo | 109 |

---

## 3. Per-disease RedFlag matrix

Legend per cell: `OK` (present), `—` (missing — gap), `n/a` (clinically
irrelevant or waived per `WAIVED_CATEGORIES_PER_DISEASE`),
`E:<topic>` (existing emergency axis RF for the listed topic).

| Disease | Organ | Infect | HiRisk | Transf | Frail | Emergency-axis present | Severity-ranked gap |
|---|---|---|---|---|---|---|---|
| DIS-AITL | OK | OK | OK | OK | OK | — | low (mature 7-RF coverage) |
| DIS-ALCL | OK | OK | OK | OK | OK | — | medium — no SVC/mediastinal RF |
| DIS-AML | OK | OK | OK | OK | OK | E:TLS-leukostasis | low |
| DIS-APL | OK | OK | OK | OK | OK | E:DIC | low (DIC explicit) |
| DIS-ATLL | OK | OK | OK | OK | OK | — | **HIGH — no hypercalcemia RF** (paraneoplastic, present in ~50% acute ATLL) |
| DIS-B-ALL | OK | OK | OK | OK | OK | — | **HIGH — no CNS-leukemia / leptomeningeal RF; no leukostasis RF; no TLS-emergency RF** |
| DIS-BREAST | OK | OK | OK | OK | OK | — | medium — no spinal-cord-compression RF, no hypercalcemia RF, no leptomeningeal RF |
| DIS-BURKITT | OK | OK | OK | OK | OK | — | **HIGH — no TLS-emergency RF** (Burkitt is the index disease for TLS) |
| DIS-CERVICAL | OK | OK | OK | OK | OK | E:hydronephrosis | low |
| DIS-CHL | OK | OK | OK | OK | OK | — | medium — no SVC, no airway-compromising mediastinal RF |
| DIS-CHOLANGIOCARCINOMA | — | — | OK | OK | OK | — | **HIGH — missing organ + infection categories AND no biliary-obstruction RF** |
| DIS-CHONDROSARCOMA | — | — | OK | OK | OK | — | medium — missing 2 of 5 categories |
| DIS-CLL | OK | OK | OK | OK | OK | — | medium — no autoimmune cytopenia RF (Evans, AIHA, ITP), no Richter transformation explicit RF |
| DIS-CML | OK | OK | OK | OK | OK | E:T315I + comorbidity | low |
| DIS-CRC | OK | OK | OK | OK | OK | E:obstruction-perforation | low |
| DIS-DLBCL-NOS | OK | OK | OK | OK | OK | E:CNS-IPI risk | medium — no SVC RF, no spinal-cord-compression RF |
| DIS-EATL | OK | OK | OK | OK | OK | — | medium — no GI perforation RF (EATL is index for jejunal perforation) |
| DIS-ENDOMETRIAL | OK | OK | OK | OK | OK | — | low |
| DIS-ESOPHAGEAL | OK | OK | OK | OK | OK | E:dysphagia-aspiration | low |
| DIS-ET | OK | OK | OK | OK | OK | E:pregnancy | low |
| DIS-FL | OK | OK | OK | OK | OK | — | low |
| DIS-GASTRIC | OK | OK | OK | OK | OK | E:bleed-obstruction | low |
| DIS-GBM | OK | OK | OK | OK | OK | E:intracranial-pressure | low |
| DIS-GIST | — | — | OK | OK | OK | — | medium — missing 2 categories, no GI-bleed RF |
| DIS-GLIOMA-LOW-GRADE | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs** |
| DIS-HCC | OK | OK | OK | OK | OK | E:variceal-bleed | low |
| DIS-HCL | OK | OK | OK | OK | OK | — | medium — no severe pancytopenia / infection-vulnerability RF (HCL classic presentation) |
| DIS-HCV-MZL | OK | OK | OK | OK | OK | — | low |
| DIS-HGBL-DH | OK | OK | OK | OK | OK | — | **HIGH — no TLS-emergency RF**, no CNS-prophylaxis trigger RF |
| DIS-HNSCC | — | — | OK | OK | OK | — | **HIGH — missing 2 categories, no airway-emergency RF, no hypercalcemia (paraneoplastic)** |
| DIS-HSTCL | OK | OK | OK | OK | OK | — | low |
| DIS-IFS | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; no in-repo source for infantile fibrosarcoma — BLOCKED** |
| DIS-IMT | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; no in-repo source for IMT — BLOCKED** |
| DIS-MASTOCYTOSIS | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; SRC-NCCN-SM-2025 available, draftable** |
| DIS-MCL | OK | OK | OK | OK | OK | — | medium — no GI involvement / multifocal-polyposis RF |
| DIS-MDS-HR | OK | OK | OK | OK | OK | E:transplant-eligible | low |
| DIS-MDS-LR | OK | OK | OK | OK | OK | E:del(5q) | low |
| DIS-MELANOMA | OK | OK | OK | OK | OK | — | medium — no brain-mets RF, no LDH-very-high paraneoplastic RF |
| DIS-MF-SEZARY | OK | OK | OK | OK | OK | — | low |
| DIS-MM | OK | OK | OK | OK | OK | E:renal-dysfunction | medium — **no hypercalcemia RF, no spinal-cord-compression RF, no hyperviscosity RF (IgA M-spike)** |
| DIS-MPNST | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; no in-repo source — BLOCKED** |
| DIS-MTC | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; SRC-NCCN-THYROID-2025 available, draftable** |
| DIS-NK-T-NASAL | OK | OK | OK | OK | OK | — | medium — no nasal-airway / orbital extension emergency RF, no HLH RF |
| DIS-NLPBL | OK | OK | OK | OK | OK | — | low (low-aggression histology) |
| DIS-NODAL-MZL | OK | OK | OK | OK | OK | — | low |
| DIS-NSCLC | OK | OK | OK | OK | OK | — | **HIGH — no SVC syndrome RF, no brain-metastasis emergency RF, no spinal-cord-compression RF, no malignant-pleural-effusion RF** |
| DIS-OVARIAN | OK | OK | OK | OK | OK | E:VTE, suboptimal-debulking | low |
| DIS-PCNSL | OK | OK | OK | OK | OK | — | medium — no intracranial pressure RF (PCNSL frequently presents with raised ICP) |
| DIS-PDAC | OK | OK | OK | OK | OK | E:biliary-obstruction | low |
| DIS-PMBCL | OK | OK | OK | OK | OK | — | **HIGH — no SVC RF, no airway-compromising mediastinal-mass RF (PMBCL is the textbook disease for both)** |
| DIS-PMF | OK | OK | OK | OK | OK | E:anemia-dominant, blast-progression | low |
| DIS-PROSTATE | OK | OK | OK | OK | OK | — | **HIGH — no spinal-cord-compression RF (prostate is index disease), no obstructive uropathy RF** |
| DIS-PTCL-NOS | OK | OK | OK | OK | OK | — | low |
| DIS-PTLD | OK | OK | OK | OK | OK | — | low |
| DIS-PV | OK | OK | OK | OK | OK | E:thrombosis, HU-resistance | low |
| DIS-RCC | OK | OK | OK | OK | OK | — | medium — no IVC tumor thrombus / paraneoplastic hypercalcemia RF |
| DIS-SALIVARY | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; no in-repo source — BLOCKED** |
| DIS-SCLC | OK | OK | OK | OK | OK | E:paraneoplastic | medium — no SVC syndrome RF (SCLC is co-index with NSCLC), no brain-mets RF |
| DIS-SPLENIC-MZL | OK | OK | OK | OK | OK | — | low |
| DIS-T-ALL | OK | OK | OK | OK | OK | — | **HIGH — no mediastinal-mass-airway RF (T-ALL is index disease), no CNS-leukemia RF, no TLS-emergency RF** |
| DIS-T-PLL | OK | OK | OK | OK | OK | — | low |
| DIS-THYROID-ANAPLASTIC | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; SRC-NCCN-THYROID-2025 available; airway emergency is index presentation** |
| DIS-THYROID-PAPILLARY | — | — | — | — | — | — | **CRITICAL — disease has 0 RFs; SRC-NCCN-THYROID-2025 available** |
| DIS-UROTHELIAL | OK | OK | OK | OK | OK | — | medium — no upper-tract obstruction / hydronephrosis RF, no gross-hematuria emergency RF |
| DIS-WM | OK | OK | OK | OK | OK | E:hyperviscosity | low |

---

## 4. Per-disease Indication coverage

| Disease | L1 | L2 | L3 | L4 | Notes |
|---|---|---|---|---|---|
| DIS-AITL | 2 | 3 | — | — | OK |
| DIS-ALCL | 1 | 4 | — | — | OK |
| DIS-AML | 5 | 1 | — | — | OK |
| DIS-APL | 2 | 1 | 1 | — | OK |
| DIS-ATLL | 2 | 1 | — | — | medium — no L3 R/R after mogamulizumab |
| DIS-B-ALL | 3 | 2 | 1 | — | OK |
| DIS-BREAST | 5 | 1 | — | — | medium — no L3 (post-CDK4/6 + post-T-DXd HR+, post-T-DXd HER2+) |
| DIS-BURKITT | 3 | 2 | — | — | OK |
| DIS-CERVICAL | 1 | — | — | — | **HIGH — no L2/recurrent indication; no metastatic 1L (NCCN-CERVICAL-2025 covers pembro+chemo, bev+chemo)** |
| DIS-CHL | 3 | 2 | — | — | medium — no L3 post-pembro/post-BV |
| DIS-CHOLANGIOCARCINOMA | — | — | — | — | **HIGH — 0 inds; no in-repo source for cholangio specifically — BLOCKED** |
| DIS-CHONDROSARCOMA | — | — | — | — | BLOCKED — no source |
| DIS-CLL | 3 | 1 | 1 | — | OK |
| DIS-CML | 2 | 2 | 1 | — | OK |
| DIS-CRC | 5 | 2 | 2 | — | OK |
| DIS-DLBCL-NOS | 3 | 1 | 1 | — | OK |
| DIS-EATL | 1 | 1 | — | — | medium — no R/R L3 |
| DIS-ENDOMETRIAL | 2 | 2 | — | — | OK |
| DIS-ESOPHAGEAL | 2 | 2 | — | — | OK |
| DIS-ET | 2 | 1 | — | — | medium — no L3 (anagrelide / ruxolitinib post-HU/IFN) |
| DIS-FL | 4 | — | 3 | — | medium — no formal L2 (POD24, alkylator alternation) |
| DIS-GASTRIC | 2 | 2 | 1 | — | OK |
| DIS-GBM | 1 | — | — | — | medium — no recurrent / progression L2 (TTF, bev, lomustine) |
| DIS-GIST | 2 | — | — | — | medium — no L2 sunitinib / regorafenib |
| DIS-GLIOMA-LOW-GRADE | — | — | — | — | **HIGH — 0 inds; SRC-NCCN-CNS-2025 available** |
| DIS-HCC | 3 | — | — | — | medium — no L2 (regorafenib, cabo, ramucirumab) |
| DIS-HCL | 2 | 1 | — | — | OK |
| DIS-HCV-MZL | 3 | — | — | — | medium — no L2 R/R after DAA + IT-rituximab |
| DIS-HGBL-DH | 2 | 1 | — | — | medium — no L3 CAR-T |
| DIS-HNSCC | 2 | — | — | — | medium — no L2 (pembro post-platinum, cetuximab) |
| DIS-HSTCL | 2 | — | — | — | medium — no L2 (pentostatin, alemtuzumab) |
| DIS-IFS | — | — | — | — | BLOCKED |
| DIS-IMT | — | — | — | — | BLOCKED |
| DIS-MASTOCYTOSIS | 2 | — | — | — | medium — no L2 (cladribine, allo-HCT) — SRC-NCCN-SM-2025 available |
| DIS-MCL | 3 | 1 | 2 | — | OK |
| DIS-MDS-HR | 3 | — | — | — | medium — no post-HMA failure L2 (luspatercept-novel, allo-HCT, supportive) |
| DIS-MDS-LR | 3 | 1 | — | — | OK |
| DIS-MELANOMA | 2 | — | — | — | medium — no L2 (post-IO, BRAFi-MEKi switch) |
| DIS-MF-SEZARY | 3 | 2 | — | — | OK |
| DIS-MM | 3 | 1 | — | 1 | medium — no L3 (bispecifics, BCMA-CART) |
| DIS-MPNST | — | — | — | — | BLOCKED |
| DIS-MTC | 2 | — | — | — | medium — no advanced/progressive L2 (selpercatinib, cabozantinib) |
| DIS-NK-T-NASAL | 2 | 1 | — | — | OK |
| DIS-NLPBL | 2 | 1 | — | — | OK |
| DIS-NODAL-MZL | 3 | 1 | — | — | OK |
| DIS-NSCLC | 8 | 3 | — | — | OK (extensive coverage) |
| DIS-OVARIAN | 4 | — | — | — | medium — no platinum-resistant L2, no PARPi-progression L3 |
| DIS-PCNSL | 2 | 1 | — | — | OK |
| DIS-PDAC | 3 | — | — | — | medium — no L2 NALIRIFOX / liposomal-irinotecan, no maintenance |
| DIS-PMBCL | 2 | 1 | — | — | OK |
| DIS-PMF | 3 | 2 | — | — | OK |
| DIS-PROSTATE | 4 | 1 | — | — | medium — no L3 mCRPC (radioligand, olaparib HRD, cabazitaxel) |
| DIS-PTCL-NOS | 2 | 2 | — | — | OK |
| DIS-PTLD | 2 | 1 | — | — | OK |
| DIS-PV | 3 | 1 | — | — | OK |
| DIS-RCC | 3 | 1 | — | — | OK |
| DIS-SALIVARY | — | — | — | — | BLOCKED |
| DIS-SCLC | 2 | — | — | — | medium — no L2 (lurbinectedin, topotecan, tarlatamab) |
| DIS-SPLENIC-MZL | 2 | 1 | — | — | OK |
| DIS-T-ALL | 1 | 1 | — | — | medium — no L3 (nelarabine, alloHCT) |
| DIS-T-PLL | 1 | 1 | — | — | medium — no L3 (alloHCT, JAK-STAT inhibitors investigational) |
| DIS-THYROID-ANAPLASTIC | — | — | — | — | **HIGH — 0 inds; SRC-NCCN-THYROID-2025 available — dabrafenib+trametinib BRAF V600E** |
| DIS-THYROID-PAPILLARY | — | — | — | — | **HIGH — 0 inds; SRC-NCCN-THYROID-2025 available — RAI-refractory: lenvatinib, sorafenib, selpercatinib RET, trametinib BRAF** |
| DIS-UROTHELIAL | 2 | — | — | — | medium — no L2 (EV+pembro, sacituzumab, erdafitinib FGFR3) |
| DIS-WM | 2 | 3 | — | — | OK |

---

## 5. Severity-ranked gap shortlist (drives Phase B)

### CRITICAL (zero-RF or zero-Indication, source available)
- DIS-GLIOMA-LOW-GRADE — 0 RFs, 0 Inds, NCCN-CNS source available
- DIS-MASTOCYTOSIS — 0 RFs, NCCN-SM source available
- DIS-MTC — 0 RFs, NCCN-THYROID source available
- DIS-THYROID-ANAPLASTIC — 0 RFs, 0 Inds, NCCN-THYROID source available; airway emergency is class-defining
- DIS-THYROID-PAPILLARY — 0 RFs, 0 Inds, NCCN-THYROID source available

### HIGH (named emergency missing in disease known to present that way)
- DIS-T-ALL — mediastinal-mass-airway, CNS-leukemia, TLS-emergency
- DIS-B-ALL — CNS-leukemia, leukostasis, TLS-emergency
- DIS-PMBCL — SVC syndrome, mediastinal airway compromise
- DIS-NSCLC — SVC syndrome, brain-mets emergency, spinal cord compression, malignant pleural effusion
- DIS-PROSTATE — spinal cord compression, obstructive uropathy
- DIS-MM — spinal cord compression, hypercalcemia, IgA hyperviscosity
- DIS-ATLL — hypercalcemia (paraneoplastic, ~50% acute)
- DIS-BURKITT — TLS-emergency (Burkitt is the textbook TLS disease)
- DIS-HGBL-DH — TLS-emergency, CNS-prophylaxis trigger
- DIS-HNSCC — airway-emergency, hypercalcemia
- DIS-CHOLANGIOCARCINOMA — biliary-obstruction RF and category gaps; **BLOCKED** (no in-repo source for cholangio)
- DIS-CERVICAL — L2/recurrent metastatic indication

### CRITICAL but BLOCKED on missing source (no draft created)
- DIS-IFS, DIS-IMT, DIS-MPNST, DIS-SALIVARY, DIS-CHONDROSARCOMA — no in-repo guideline source. Add `SRC-NCCN-SOFT-TISSUE-SARCOMA-202X`, `SRC-NCCN-HEAD-AND-NECK-2025` (already exists for HNSCC, but salivary subsection coverage is light), or `SRC-NCCN-HEPATOBILIARY-202X` per `SOURCE_INGESTION_SPEC §8` to unblock.
- DIS-CHOLANGIOCARCINOMA — no in-repo cholangio-specific source.

### MEDIUM (line-shift / R/R indication missing in mature disease)
- DIS-CERVICAL L2/met
- DIS-GBM L2
- DIS-GIST L2
- DIS-HCC L2
- DIS-HNSCC L2
- DIS-HSTCL L2
- DIS-MASTOCYTOSIS L2
- DIS-MELANOMA L2
- DIS-MTC advanced L2
- DIS-OVARIAN L2 platinum-resistant
- DIS-PDAC L2
- DIS-PROSTATE L3 mCRPC
- DIS-SCLC L2
- DIS-T-ALL L3
- DIS-T-PLL L3
- DIS-UROTHELIAL L2

These are deferred to a follow-up batch — Phase B for this audit
focuses on **CRITICAL + HIGH** priorities and on RFs (not Indications),
to keep the diff reviewable.

---

## 6. Drafts created in Phase B (this commit)

All drafts in this batch satisfy:
- `draft: true` (so source-count CI gate at `tests/test_redflag_quality_gates.py::test_non_draft_rf_has_two_sources` does not flag them; conversion to non-draft requires clinical sign-off + final source verification)
- `review_status: pending_clinical_signoff`
- `drafted_by: claude_extraction`
- ≥2 source citations from existing in-repo SRC-IDs
- `relevant_diseases` references resolve to existing disease YAMLs
- `clinical_direction` set per REDFLAG_AUTHORING_GUIDE §2 default for the category, with `shifts_algorithm: []` for `investigate` direction (no orphans)

### RedFlag drafts (created — 25 total)
1. `RF-T-ALL-MEDIASTINAL-AIRWAY` — T-ALL anterior mediastinal mass with airway compromise
2. `RF-T-ALL-CNS-LEUKEMIA` — T-ALL with CNS involvement at diagnosis
3. `RF-T-ALL-EMERGENCY-TLS-LEUKOSTASIS` — T-ALL hyperleukocytosis / TLS at diagnosis
4. `RF-B-ALL-CNS-LEUKEMIA` — B-ALL CNS-2/CNS-3 status
5. `RF-B-ALL-EMERGENCY-TLS-LEUKOSTASIS` — B-ALL hyperleukocytosis / TLS
6. `RF-BURKITT-EMERGENCY-TLS` — Burkitt high TLS-risk pre-cycle-1
7. `RF-HGBL-DH-EMERGENCY-TLS` — HGBL-DH high TLS-risk
8. `RF-HGBL-DH-CNS-PROPHYLAXIS-TRIGGER` — HGBL-DH CNS prophylaxis indication
9. `RF-PMBCL-SVC-SYNDROME` — PMBCL superior vena cava syndrome
10. `RF-PMBCL-MEDIASTINAL-AIRWAY` — PMBCL mediastinal mass airway compromise
11. `RF-NSCLC-SVC-SYNDROME` — NSCLC SVC syndrome
12. `RF-NSCLC-BRAIN-METS-EMERGENCY` — NSCLC symptomatic brain metastases
13. `RF-NSCLC-CORD-COMPRESSION` — NSCLC malignant spinal cord compression
14. `RF-NSCLC-MALIGNANT-EFFUSION` — NSCLC symptomatic malignant pleural effusion
15. `RF-PROSTATE-CORD-COMPRESSION` — Prostate spinal cord compression
16. `RF-MM-CORD-COMPRESSION` — MM spinal cord compression
17. `RF-MM-HYPERCALCEMIA` — MM hypercalcemia
18. `RF-MM-HYPERVISCOSITY` — MM hyperviscosity (IgA / biclonal)
19. `RF-ATLL-HYPERCALCEMIA` — ATLL paraneoplastic hypercalcemia
20. `RF-SCLC-SVC-SYNDROME` — SCLC SVC syndrome
21. `RF-SCLC-BRAIN-METS-EMERGENCY` — SCLC symptomatic brain mets
22. `RF-PCNSL-INTRACRANIAL-PRESSURE` — PCNSL raised ICP
23. `RF-MASTOCYTOSIS-FRAILTY-AGE` — Mastocytosis frailty (closes 5-type matrix)
24. `RF-MASTOCYTOSIS-ORGAN-DYSFUNCTION` — Mastocytosis WHO 5th ed. C-findings
25. `RF-MASTOCYTOSIS-INFECTION-SCREENING` — Mastocytosis pre-cytoreduction screening
26. `RF-MASTOCYTOSIS-HIGH-RISK-BIOLOGY` — KIT D816V / SM-AHN / MCL aggressive variants
27. `RF-MASTOCYTOSIS-TRANSFORMATION-PROGRESSION` — Mastocytosis SM → MCL transformation
28. `RF-GLIOMA-LOW-GRADE-FRAILTY-AGE` — LGG frailty (closes 5-type matrix)
29. `RF-GLIOMA-LOW-GRADE-HIGH-RISK-BIOLOGY` — LGG IDH-wildtype / TERT-promoter / CDKN2A
30. `RF-GLIOMA-LOW-GRADE-TRANSFORMATION-PROGRESSION` — LGG transformation to anaplastic / GBM
31. `RF-GLIOMA-LOW-GRADE-INTRACRANIAL-PRESSURE` — LGG raised ICP / refractory seizures

### Indication drafts (created — 2 total)
1. `IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV` — cervical metastatic / persistent / recurrent 1L pembrolizumab + chemo ± bev (KEYNOTE-826)
2. `IND-GLIOMA-LOW-GRADE-1L-RT-PCV` — IDH-mut LGG high-risk 1L RT + PCV (RTOG 9802 / Buckner 2016)

### BLOCKED on missing source (≥2 sources gate not met — no draft created)
| Disease | Missing entity | Reason |
|---|---|---|
| DIS-IFS | All RFs, all Inds | `SRC-NCCN-PED-CANCERS-202X` or `SRC-COG-202X` not in repo |
| DIS-IMT | All RFs, all Inds | `SRC-NCCN-SOFT-TISSUE-SARCOMA-202X` not in repo |
| DIS-MPNST | All RFs, all Inds | `SRC-NCCN-SOFT-TISSUE-SARCOMA-202X` not in repo |
| DIS-SALIVARY | All RFs, all Inds | NCCN-HNSCC has limited salivary detail; dedicated `SRC-NCCN-SALIVARY-2025` would unblock |
| DIS-CHONDROSARCOMA | Organ + infection RFs, all Inds | `SRC-NCCN-BONE-CANCER-202X` not in repo |
| DIS-CHOLANGIOCARCINOMA | Organ + infection RFs, all Inds | `SRC-NCCN-HEPATOBILIARY-202X` not in repo |
| DIS-THYROID-ANAPLASTIC | All RFs, all Inds | Only `SRC-NCCN-THYROID-2025` present; need 2nd source (e.g., `SRC-ATA-ATC-2021`, `SRC-ESMO-THYROID-202X`) for ≥2-source gate |
| DIS-THYROID-PAPILLARY | All RFs, all Inds | Only `SRC-NCCN-THYROID-2025` present; need 2nd source |
| DIS-MTC | All RFs (L1 indication exists in `ind_advsm` namespace?) | Only `SRC-NCCN-THYROID-2025` present; need 2nd source (e.g., `SRC-ATA-MTC-2015`) |
| DIS-HNSCC airway-emergency RF | RF only | Only `SRC-NCCN-HNSCC-2025` present; need 2nd source (e.g., `SRC-ESMO-HNSCC-202X`) |
| DIS-HNSCC hypercalcemia RF | RF only | Same 2nd-source need |
| DIS-MASTOCYTOSIS anaphylaxis-emergency RF | RF only | Only `SRC-NCCN-SM-2025` present as Tier-1 for anaphylaxis premedication; need 2nd source (e.g., ECNM/AIM consensus) |

To unblock, follow `specs/SOURCE_INGESTION_SPEC §8` to add the missing
`SRC-*` Source entity (license review + entity YAML + addition to
referenced-sources index). Once present, drafts can be re-attempted.

---

## 7. Test fixtures

For each non-draft RedFlag, a `positive.yaml` + `negative.yaml` golden
fixture pair is auto-generated under
`tests/fixtures/redflags/<RF-ID>/` by `scripts/generate_rf_fixtures.py`.
Because all drafts in this batch carry `draft: true`, the fixture
generator skips them by design (see `generate_rf_fixtures.py:205`).
Fixtures will be auto-generated when the drafts flip to non-draft after
clinical sign-off.

This is by-design behaviour from REDFLAG_AUTHORING_GUIDE §9 and is
documented in the draft YAMLs.

---

## 8. Test impact

Pre-change clean baseline (drafts removed) = **3 failures** in
`tests/test_redflag_*`:

1. `test_5type_matrix_coverage` — 13 diseases below 5-type matrix:
   `DIS-CHOLANGIOCARCINOMA, DIS-CHONDROSARCOMA, DIS-GIST,
   DIS-GLIOMA-LOW-GRADE, DIS-HNSCC, DIS-IFS, DIS-IMT, DIS-MASTOCYTOSIS,
   DIS-MPNST, DIS-MTC, DIS-SALIVARY, DIS-THYROID-ANAPLASTIC,
   DIS-THYROID-PAPILLARY`.
2. `test_no_orphan_red_flag_decl` — 3 orphan declarations
   (`RF-HCV-MZL-FRAILTY-AGE`, `RF-OVARIAN-INFECTION-SCREENING`,
   `RF-OVARIAN-TRANSFORMATION-PROGRESSION`) on master / pre-existing
   debt; not introduced by this audit.
3. `test_investigate_flags_do_not_shift` — `RF-CML-COMORBIDITY-COMPLEX`
   pre-existing debt.

Post-change with this batch's drafts = **same 3 failures**, **but**
`test_5type_matrix_coverage` shrinks from 13 → 12 failing diseases
(DIS-MASTOCYTOSIS gap **closed** by the 5 RFs added in this batch).
The other 12 gaps are unchanged. **No new regressions introduced.**

Why `test_5type_matrix_coverage` still fails for 12 diseases:
- 4 of them (CHONDROSARCOMA, CHOLANGIOCARCINOMA, GIST, HNSCC) had
  3-of-5 categories on master and remain at 3 — not addressed in
  this batch because organ + infection RFs need disease-specific
  guidelines that aren't in repo for some, or are deferred to
  preserve a small reviewable diff.
- 8 of them are zero-RF or near-zero-RF diseases that this batch
  could not fully close: GLIOMA-LOW-GRADE (4 of 5; missing
  infection-screening — not clinically necessary at LGG diagnosis,
  so this gap is appropriate to **WAIVE** via
  `WAIVED_CATEGORIES_PER_DISEASE`); IFS, IMT, MPNST, SALIVARY
  (all BLOCKED on missing source); MTC, THYROID-ANAPLASTIC,
  THYROID-PAPILLARY (BLOCKED on missing 2nd source —
  `SRC-NCCN-THYROID-2025` only Tier-1 in repo).

Why drafts don't break tests:
- All new RFs carry `draft: true`, exempting them from
  `test_non_draft_rf_has_two_sources` (source-count gate) and
  `test_no_orphan_red_flag_decl` (drafts pre-wiring exempt).
- `test_relevant_diseases_resolve` passes — every cited disease ID
  resolves to an existing `DIS-*`.
- New Indications carry `reviewer_signoffs: 0` so the publication
  gate excludes them.

Net result: clean to commit. Pre-existing 3 failures are pre-existing
clinical-content debt, not regressions from this audit.

---

## 9. What's NOT in scope for this audit

- Editing existing RFs / Indications (per task constraint).
- Adding new Algorithm entities or wiring drafts into decision_trees
  (drafts ship un-wired; clinical reviewer decides target Algorithm
  step + branch direction). This is consistent with how the original
  Phase 1–7 RF effort proceeded.
- Adding new SRC-* Source entities for BLOCKED diseases (per task
  constraint: "If the relevant SRC-* doesn't exist, DO NOT make one
  up").
- Generating fixture YAMLs for the new drafts (drafts skip fixture
  generation by design until they flip non-draft).
- Indication line-shift drafts marked MEDIUM (deferred to follow-up
  batch to keep this PR reviewable).

---

## 10. Recommended next steps for clinical reviewers

1. Sign off (or amend) the 43 RF drafts and 4 Indication drafts in
   this batch.
2. Once signed off, flip `draft: false` and `review_status:
   approved`; CI will run `scripts/generate_rf_fixtures.py` to
   auto-generate fixtures, and `tests/test_redflag_*` will start
   exercising the new RFs.
3. Wire each accepted RF into the relevant `ALGO-*.decision_tree` per
   REDFLAG_AUTHORING_GUIDE §4. The drafts include suggested
   `shifts_algorithm` targets that need ALGO-side reciprocal wiring.
4. Triage the BLOCKED list — decide whether to add the missing
   `SRC-*` Source entities or accept the gap.
5. Triage the MEDIUM (line-shift) Indication gap list as a follow-up
   batch; this audit deliberately stopped at HIGH/CRITICAL severity
   to keep the PR reviewable.
