# CSD-2 Drug Categorization (2026-04-27)

Total drugs in KB: **167**
Categorized for 3 parallel Wave 1 authoring agents. Every drug appears
in exactly one pkg (pkg1 ∪ pkg2 ∪ pkg3 = full KB, pairwise disjoint).
Verified by script: `73 + 52 + 42 = 167`, no overlap, no orphans.

Heuristic: drug nature + year of FDA approval + clinical knowledge of
UA reimbursement reality (NSZU онкопакет 2025/2026, Доступні Ліки,
Реімбурсаційні програми). **No WebFetch performed** — Wave 1 agents
will verify against МОЗ Реєстр and the NSZU formulary themselves.

| pkg | count | role |
|---|---:|---|
| pkg1 | 73 | NSZU онкопакет + supportive + hormonals (established) |
| pkg2 | 52 | Реімбурсаційний пакет / partial coverage (newer targeted, ICIs, IMiDs) |
| pkg3 | 42 | Pay-OOP / named-patient / not-yet-registered |

---

## pkg1 — NSZU онкопакет + Supportive (Group 1 + Group 5) → CSD-2-authoring-pkg1

**73 drugs.** Established cytotoxics, first-generation biologics,
hormonals, supportive care. Likely NSZU-reimbursed for at least one
indication. The authoring task is mostly **populating
`reimbursement_indications`** on drugs already flagged
`reimbursed_nszu: true`, plus dating `last_verified` and replacing
`[verify-clinical-co-lead]` placeholders.

- DRUG-5-FLUOROURACIL
- DRUG-ABIRATERONE
- DRUG-ACYCLOVIR
- DRUG-ALLOPURINOL
- DRUG-ANAGRELIDE
- DRUG-ANASTROZOLE
- DRUG-APALUTAMIDE
- DRUG-ASPIRIN
- DRUG-ATO
- DRUG-ATRA
- DRUG-BENDAMUSTINE
- DRUG-BEVACIZUMAB
- DRUG-BLEOMYCIN
- DRUG-CAPECITABINE
- DRUG-CAPECITABINE-BREAST
- DRUG-CARBOPLATIN
- DRUG-CETUXIMAB
- DRUG-CISPLATIN
- DRUG-CLADRIBINE
- DRUG-CYCLOPHOSPHAMIDE
- DRUG-CYTARABINE
- DRUG-DACARBAZINE
- DRUG-DASATINIB
- DRUG-DAUNORUBICIN
- DRUG-DEGARELIX
- DRUG-DENOSUMAB
- DRUG-DEXAMETHASONE
- DRUG-DOCETAXEL
- DRUG-DOXORUBICIN
- DRUG-ENTECAVIR
- DRUG-ENZALUTAMIDE
- DRUG-EPOETIN-ALFA
- DRUG-ETOPOSIDE
- DRUG-EXEMESTANE
- DRUG-FILGRASTIM
- DRUG-FLUDARABINE
- DRUG-FULVESTRANT
- DRUG-GEMCITABINE
- DRUG-GLECAPREVIR-PIBRENTASVIR
- DRUG-GOSERELIN
- DRUG-HYDROXYUREA
- DRUG-IDARUBICIN
- DRUG-IFOSFAMIDE
- DRUG-IMATINIB
- DRUG-INTERFERON-ALPHA
- DRUG-IRINOTECAN
- DRUG-LEUCOVORIN
- DRUG-LEUPROLIDE
- DRUG-LETROZOLE
- DRUG-L-ASPARAGINASE
- DRUG-MERCAPTOPURINE
- DRUG-METHOTREXATE
- DRUG-NAB-PACLITAXEL
- DRUG-NILOTINIB
- DRUG-ONDANSETRON
- DRUG-OXALIPLATIN
- DRUG-PACLITAXEL
- DRUG-PEMETREXED
- DRUG-PERTUZUMAB
- DRUG-PREDNISONE
- DRUG-PROCARBAZINE
- DRUG-RITUXIMAB
- DRUG-SOFOSBUVIR-VELPATASVIR
- DRUG-TAMOXIFEN
- DRUG-TEMOZOLOMIDE
- DRUG-THIOTEPA
- DRUG-TMP-SMX
- DRUG-TRASTUZUMAB
- DRUG-TRIFLURIDINE-TIPIRACIL
- DRUG-VINBLASTINE
- DRUG-VINCRISTINE
- DRUG-ZIDOVUDINE
- DRUG-ZOLEDRONATE

---

## pkg2 — Реімбурсаційний пакет / partial coverage (Group 2) → CSD-2-authoring-pkg2

**52 drugs.** Newer targeted therapies, ICIs, PARPi, BTKi, CDK4/6, HMA,
IMiDs, mature ADCs. NSZU coverage typically exists but is strictly
indication-restricted; many need careful indication wording (PD-L1
cutoff, line of therapy, biomarker requirement).

- DRUG-ABEMACICLIB
- DRUG-ACALABRUTINIB
- DRUG-AFATINIB
- DRUG-ALECTINIB
- DRUG-ALPELISIB
- DRUG-ATEZOLIZUMAB
- DRUG-AVELUMAB
- DRUG-AXITINIB
- DRUG-AZACITIDINE
- DRUG-BLINATUMOMAB
- DRUG-BORTEZOMIB
- DRUG-BOSUTINIB
- DRUG-BRENTUXIMAB-VEDOTIN
- DRUG-BRIGATINIB
- DRUG-CARFILZOMIB
- DRUG-CRIZOTINIB
- DRUG-DABRAFENIB
- DRUG-DACOMITINIB
- DRUG-DARATUMUMAB
- DRUG-DAROLUTAMIDE
- DRUG-DECITABINE
- DRUG-DURVALUMAB
- DRUG-ENCORAFENIB
- DRUG-ERLOTINIB
- DRUG-FEDRATINIB
- DRUG-GEFITINIB
- DRUG-IBRUTINIB
- DRUG-IPILIMUMAB
- DRUG-LAROTRECTINIB
- DRUG-LENALIDOMIDE
- DRUG-LENVATINIB
- DRUG-LORLATINIB
- DRUG-LUSPATERCEPT
- DRUG-MIDOSTAURIN
- DRUG-NIRAPARIB
- DRUG-NIVOLUMAB
- DRUG-OBINUTUZUMAB
- DRUG-OLAPARIB
- DRUG-OSIMERTINIB
- DRUG-PALBOCICLIB
- DRUG-PEMBROLIZUMAB
- DRUG-RAMUCIRUMAB
- DRUG-REGORAFENIB
- DRUG-RIBOCICLIB
- DRUG-RUXOLITINIB
- DRUG-SORAFENIB
- DRUG-TALAZOPARIB
- DRUG-TRAMETINIB
- DRUG-TRASTUZUMAB-DERUXTECAN
- DRUG-TRASTUZUMAB-EMTANSINE
- DRUG-VENETOCLAX
- DRUG-ZANUBRUTINIB

---

## pkg3 — Pay-OOP / named-patient / not-yet-registered (Group 3 + Group 4) → CSD-2-authoring-pkg3

**42 drugs.** Recent FDA approvals, cell therapies, bispecifics, novel
ADCs, niche oncogene-specific inhibitors, radioligands. Most are not
yet registered in UA or registered-but-not-reimbursed. Wave 1 agent
must establish whether the drug appears in МОЗ Реєстр at all and
document the charity-import / clinical-trial / named-patient pathway
in `notes:`.

- DRUG-ADAGRASIB
- DRUG-ALEMTUZUMAB
- DRUG-ASCIMINIB
- DRUG-AXICABTAGENE-CILOLEUCEL
- DRUG-BELINOSTAT
- DRUG-BELZUTIFAN
- DRUG-BEXAROTENE
- DRUG-BREXUCABTAGENE-AUTOLEUCEL
- DRUG-CAPMATINIB
- DRUG-CPX-351
- DRUG-DOSTARLIMAB
- DRUG-ELACESTRANT
- DRUG-ENFORTUMAB-VEDOTIN
- DRUG-ENTRECTINIB
- DRUG-GEMTUZUMAB-OZOGAMICIN
- DRUG-GILTERITINIB
- DRUG-IMETELSTAT
- DRUG-INOTUZUMAB-OZOGAMICIN
- DRUG-ISATUXIMAB
- DRUG-LUTETIUM-177-PSMA
- DRUG-MOGAMULIZUMAB
- DRUG-MOMELOTINIB
- DRUG-MOSUNETUZUMAB
- DRUG-NELARABINE
- DRUG-PIRTOBRUTINIB
- DRUG-POLATUZUMAB-VEDOTIN
- DRUG-PONATINIB
- DRUG-PRALATREXATE
- DRUG-QUIZARTINIB
- DRUG-RADIUM-223
- DRUG-RELUGOLIX
- DRUG-ROMIDEPSIN
- DRUG-ROPEGINTERFERON-ALFA-2B
- DRUG-SACITUZUMAB-GOVITECAN
- DRUG-SELPERCATINIB
- DRUG-SOTORASIB
- DRUG-TAZEMETOSTAT
- DRUG-TECLISTAMAB
- DRUG-TEPOTINIB
- DRUG-TISAGENLECLEUCEL
- DRUG-TREMELIMUMAB
- DRUG-TUCATINIB

---

## Borderline cases / categorization rationale

Notes only on non-obvious calls. Bare cytotoxics, hormonals and basic
supportive care are silently in pkg1.

### Why pkg1 carries 73 instead of the suggested 40–45

The starter heuristic separated "Group 1 (cytotoxics + biologics)" from
"Group 5 (supportive)" but they share an authoring profile: drugs that
are already `reimbursed_nszu: true` and just need their
`reimbursement_indications` array filled. Splitting them into 5a/5b
would force one agent to author indications and another to author
supportive-care notes, which is artificial. pkg1 stays at 73; the agent
is told that **~40 of those drugs are already
`reimbursed_nszu: true` and just need indication strings**, with the
remainder being mechanical date stamps.

### Drug-by-drug rationale (only ones non-obvious)

- **DRUG-BORTEZOMIB → pkg1**. Generic since 2017; on NSZU онкопакет for
  MM since 2022. Established enough to belong with first-line cytotoxics.
- **DRUG-IMATINIB / NILOTINIB / DASATINIB → pkg1**. CML 1st-gen TKIs,
  on NSZU since 2017–2019; treat as established.
- **DRUG-BOSUTINIB → pkg2**, **DRUG-PONATINIB / DRUG-ASCIMINIB → pkg3**.
  Newer-generation BCR-ABL: bosutinib has 2nd-line use with plausible
  partial reimbursement; ponatinib + asciminib are T315I-niche, expensive,
  named-patient typical.
- **DRUG-BRENTUXIMAB-VEDOTIN → pkg2**. ADC in cHL/PTCL; first-gen ADC
  with mature data; recently joined NSZU онкопакет for cHL.
- **DRUG-POLATUZUMAB-VEDOTIN → pkg3**. Newer (2019/2020), DLBCL only,
  no UA reimbursement yet.
- **DRUG-AZACITIDINE → pkg2 / DRUG-DECITABINE → pkg2**. HMAs — both have
  partial NSZU coverage for MDS / AML in elderly. Symmetric placement.
- **DRUG-LENALIDOMIDE → pkg2**. IMiD with NSZU coverage for MM since
  ~2021; stays in pkg2 because indication wording is restrictive.
- **DRUG-DARATUMUMAB → pkg2**. Anti-CD38 mAb; NSZU coverage for some
  MM lines exists but is indication-restricted.
- **DRUG-ISATUXIMAB → pkg3**. Same target as daratumumab but newer (2020)
  and not yet on NSZU formulary as of 2026-04 to our knowledge.
- **DRUG-RADIUM-223 → pkg3**. Registered in UA but not reimbursed;
  patients self-pay or import.
- **DRUG-LUTETIUM-177-PSMA → pkg3**. Recently FDA-approved (2022);
  no UA registration to our knowledge.
- **DRUG-IBRUTINIB → pkg2** (not pkg1). Partial NSZU coverage for CLL
  in 2nd-line; first-generation BTKi but indication-restricted.
- **DRUG-OBINUTUZUMAB → pkg2**. Anti-CD20 mAb, second-generation;
  NSZU may cover for CLL / FL high-burden but indication-restricted —
  not as universal as rituximab.
- **DRUG-PERTUZUMAB → pkg1**. Bundled with trastuzumab in HER2+ breast
  NSZU package; treat as established.
- **DRUG-PEMBROLIZUMAB / NIVOLUMAB / ATEZOLIZUMAB → pkg2**. ICIs;
  NSZU coverage exists but is PD-L1- and indication-restricted —
  exact wording matters. Wave 1 must verify.
- **DRUG-DURVALUMAB → pkg2**. `reimbursed_nszu` key currently absent
  in YAML — pkg2 agent must resolve.
- **DRUG-TREMELIMUMAB → pkg3**. STRIDE regimen partner; new (2022);
  no UA reimbursement; key absent in YAML.
- **DRUG-INTERFERON-ALPHA → pkg1**. Oldest cytokine immunotherapy;
  NSZU package for MPN. `reimbursed_nszu` key currently absent —
  pkg1 agent must explicitly set the value.
- **DRUG-ROPEGINTERFERON-ALFA-2B → pkg3**. Newer formulation (2022 EMA);
  not yet registered in UA.
- **DRUG-INOTUZUMAB-OZOGAMICIN / DRUG-GEMTUZUMAB-OZOGAMICIN / DRUG-CPX-351
  → pkg3**. ALL/AML-targeted, niche, expensive.
- **DRUG-IMETELSTAT → pkg3**. 2024 FDA approval (LR-MDS); no UA reg.
- **DRUG-LUSPATERCEPT → pkg2**. ESMO endorsed for LR-MDS; recently
  added to UA reimbursement programs (some pilot indications).
- **DRUG-MIDOSTAURIN → pkg2**, **DRUG-GILTERITINIB → pkg3**,
  **DRUG-QUIZARTINIB → pkg3**. Midostaurin older (2017); gilteritinib
  2018 + no UA NSZU; quizartinib 2023 (very new).
- **DRUG-VENETOCLAX → pkg2**. BCL-2 inhibitor; CLL + AML; partial NSZU
  coverage exists.
- **DRUG-MOSUNETUZUMAB / DRUG-TECLISTAMAB → pkg3**. Bispecifics, recent.
- **DRUG-PIRTOBRUTINIB → pkg3**. 2023 FDA accelerated approval; no UA reg.
- **DRUG-ELACESTRANT → pkg3**. 2023 FDA, ESR1-niche.
- **DRUG-ALPELISIB → pkg2**. 2019 FDA; some pilot UA programs.
- **DRUG-TUCATINIB → pkg3**. HER2+ brain-mets niche; 2020 FDA; no UA NSZU.
- **DRUG-LAROTRECTINIB → pkg2** vs **DRUG-ENTRECTINIB / SELPERCATINIB → pkg3**.
  Larotrectinib has been around longer (2018) with tumor-agnostic
  NCCN/ESMO support; the others newer / niche.
- **DRUG-MOGAMULIZUMAB → pkg3**. CTCL niche, expensive.
- **DRUG-PRALATREXATE / BELINOSTAT / ROMIDEPSIN → pkg3**. PTCL-niche,
  no UA NSZU.
- **DRUG-NELARABINE → pkg3**. T-ALL niche, no UA NSZU.
- **DRUG-RELUGOLIX → pkg3**. Oral GnRH antagonist, 2020 FDA, no UA reg.
- **DRUG-DAROLUTAMIDE → pkg2** / **DRUG-APALUTAMIDE → pkg1**. Apalutamide
  has been on UA market longer with some NSZU coverage; darolutamide
  newer + more partial.
- **DRUG-ALEMTUZUMAB → pkg3**. Anti-CD52 mAb; in OncoPlan use is mostly
  niche/named-patient (T-PLL) — flagged with placeholder string already.
- **DRUG-AVELUMAB → pkg2** but flag for human review (see below).

### Items flagged for human (clinical co-lead) decision

- `DRUG-LUSPATERCEPT` — pkg2 vs pkg3 depends on whether the current MoH
  2026 reimbursement program includes LR-MDS. Wave 1 agent should
  verify and re-classify if needed.
- `DRUG-AVELUMAB` — 2024 verification suggests UA registration may have
  lapsed or never been granted; currently in pkg2 but may belong in pkg3.
- `DRUG-DURVALUMAB` and `DRUG-TREMELIMUMAB` — STRIDE regimen for HCC.
  Durvalumab kept in pkg2 (older single-agent ICI indications);
  tremelimumab in pkg3.
- `DRUG-AZACITIDINE` (pkg2) and `DRUG-DECITABINE` (pkg2) — symmetric.
  If NSZU now covers azacitidine but not decitabine for AML/MDS, the
  fix is in YAML, not the partition.
- `DRUG-CABOZANTINIB` — *not present in KB* (verified via the audit
  script). If a cabozantinib YAML is added later it would belong in pkg2.

---

## Wave 1 authoring agent prompts (one-line summaries)

- **CSD-2-authoring-pkg1** — for each of 73 drugs in pkg1, set
  `last_verified: 2026-04-27`, populate `reimbursement_indications`
  where `reimbursed_nszu: true`, replace any `[verify-clinical-co-lead]`
  placeholder, optionally fill `registration_number` from МОЗ Реєстр.
- **CSD-2-authoring-pkg2** — for each of 52 drugs in pkg2, verify
  registration + reimbursement status against МОЗ Реєстр + NSZU
  formulary, populate indication list with exact line-of-therapy /
  biomarker wording, set `last_verified`.
- **CSD-2-authoring-pkg3** — for each of 42 drugs in pkg3, verify
  whether registered in UA at all; if not, set `registered: false`,
  `reimbursed_nszu: false`, populate `notes:` with named-patient /
  charity-import / clinical-trial pathway. Set `last_verified`.
