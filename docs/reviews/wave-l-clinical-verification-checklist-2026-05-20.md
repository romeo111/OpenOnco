# Wave L Clinical-Co-Lead Verification Checklist — 2026-05-20

**Purpose.** Triage which Wave L+M STUB entities the two Clinical
Co-Leads should verify first before the eventual two-Co-Lead signoff
per CHARTER §6.1. Companion to `wave-l-kb-coverage-2026-05-19.md`
(coverage metrics); this document is action-oriented.

**Scope.** Diff `d60004b723..wave-l-prep-2026-05-19` (21 commits):
43 RedFlags (incl. 9 Wave K cherry-picks), 84 prevention Indications,
4 pediatric anchor diseases, 12 chemoprevention/PrEP/vaccine drugs.
All entities carry `draft: true`, `reviewer_signoffs: 0`, STUB note.

**Stake heuristic.** Aggressive irreversible intervention (PTG, RRM,
RRBSO) or radiation avoidance > intensive imaging surveillance in
children > adult surveillance schedules > counseling-only.

---

## Triage classification

### 🔴 HIGH-STAKES — verify first (10 entries)

Drives prophylactic surgery, chemoprevention initiation, radiation
decisions, or chemo-class restrictions. Wrong guidance has direct,
often irreversible, harm. Verify these BEFORE any other Wave L work.

1. **RF-HDGC-CDH1-CONFIRMED-CARRIER** + IND-HDGC-CDH1-CARRIER-PREVENTION-SURVEILLANCE — recommends prophylactic total gastrectomy ages 20-30 (lifelong B12/Ca/Fe dependence).
2. **RF-CMMRD-CONFIRMED-CARRIER** + IND-CMMRD-CARRIER-PREVENTION-SURVEILLANCE — q6mo brain MRI from age 2, q6mo colonoscopy from age 6, "avoid alkylating + topoisomerase-II chemo / empiric RT" rule.
3. **RF-RHABDOID-PREDISPOSITION-CONFIRMED-CARRIER** + IND-RHABDOID-PREDISPOSITION-CARRIER-SURVEILLANCE — q3mo brain MRI infancy → age 4, q3-6mo whole-body MRI through age 5; extremely narrow ATRT risk window.
4. **RF-BECKWITH-WIEDEMANN-CONFIRMED-CARRIER** + IND-BECKWITH-WIEDEMANN-CARRIER-SURVEILLANCE — q3mo abdominal US birth-to-8 + monthly AFP from birth.
5. **RF-DICER1-CONFIRMED-CARRIER** + IND-DICER1-CARRIER-PREVENTION-SURVEILLANCE — multi-organ pediatric surveillance (PPB, Sertoli-Leydig, multinodular goiter, embryonal RMS).
6. **RF-NF1-CONFIRMED-CARRIER** + IND-NF1-CARRIER-PREVENTION-SURVEILLANCE — BRCA2-equivalent breast surveillance from age 30 + whole-body MRI for MPNST; high-frequency RF (~1:3000) → high blast radius.
7. **RF-PALB2-CONFIRMED-CARRIER** + IND-PALB2-CARRIER-PREVENTION-SURVEILLANCE — BRCA-style annual mammography + MRI from age 30; informs RRM discussion.
8. **RF-ATM-CONFIRMED-CARRIER** + IND-ATM-CARRIER-PREVENTION-SURVEILLANCE — radiation-tolerance landmine (heterozygotes ≠ biallelic A-T) + PDAC FDR-conditional surveillance.
9. **RF-COSTELLO-CONFIRMED-CARRIER** + IND-COSTELLO-CARRIER-INTENSIFIED — pediatric embryonal-sarcoma surveillance + cardiac comorbidity gating.
10. **DRUG-FULVESTRANT-PREVENTION** — gating entity: notes say "Engine MUST NOT surface for prevention." Verify the gating contract (route, evidence base, regulatory text) is unambiguous; misroute would mean off-label IM injection of a treatment-only SERD in a disease-free patient.

### 🟡 MODERATE-STAKES — verify second (sample 5 patterns; full list in YAML diff)

Surveillance schedules or cascade testing where wrong frequency / starting
age produces suboptimal but recoverable detection. Verify representative
exemplars per pattern, then accept-by-pattern for the siblings.

- **Cascade testing pattern**: IND-CASCADE-{LYNCH,BRCA,FAP,LFS,VHL}-FDR-POSITIVE-{TESTING,SURVEILLANCE} — verify Lynch as exemplar; site-specific vs panel routing + 50% prior probability framing.
- **Iatrogenic late-effects pattern**: IND-IATROGENIC-METHOTREXATE-LONGTERM-LYMPHOMA-PREVENTION-SURVEILLANCE + IND-IATROGENIC-IODINE131-SECONDARY-PREVENTION-SURVEILLANCE — verify MTX-LPD withdrawal-trial guidance + I-131 CBC ×10yr window.
- **Chronic-condition pattern**: IND-CHRONIC-T2DM-CANCER-RISK-PREVENTION-* + IND-CHRONIC-NAFLD-MASLD-HCC-PREVENTION-* — RR magnitudes (T2DM-pancreatic ~1.8-2.0; new-onset T2DM ≥50 ~2.5) + metformin observational signal claim.
- **Reproductive pattern**: IND-REPRODUCTIVE-ENDOMETRIOSIS-OVARIAN-PREVENTION-SURVEILLANCE — opportunistic salpingectomy + UKCTOCS/PLCO "no population screening" framing.
- **Moderate-penetrance HR-pathway pattern**: IND-{BARD1,BRIP1,RAD51C-D}-CARRIER-PREVENTION-SURVEILLANCE — verify BRIP1 ovarian-only-not-breast risk assignment is preserved (commonly mis-tier'd by clinicians).
- **Pediatric anchor diseases** (DIS-ATRT, DIS-HEPATOBLASTOMA, DIS-MEDULLOBLASTOMA, DIS-RHABDOMYOSARCOMA) — encyclopedia content, no direct intervention; verify epidemiology + WHO-classification fields against NCCN-CNS-2025 / COG.

### 🟢 LOW-STAKES — verify last (sample 2 patterns)

Counseling-only entities — lifestyle education / dietary advice / broad
symptom literacy. Wrong guidance is recoverable in subsequent visits;
verify representatives only.

- **Lifestyle pattern**: IND-LIFESTYLE-{SMOKELESS-TOBACCO,SUGARY-BEVERAGES,SALTY-PICKLED-DIET,HOT-MATE,RED-MEAT}-PREVENTION-* — IARC-evidence-level + actionable change framing.
- **Occupational pattern**: IND-OCC-{GLYPHOSATE,SHIFTWORK,PCB,FRYING-EMISSIONS}-PREVENTION-* — IARC Group 2A status accurately represented (no overclaim of Group 1).

---

## Per-entity checklist — top 15

Row format: ID | Clinical claim | Sources cited | Verification action | Triage | Effort

| ID | Clinical claim (1 line) | Sources | Verification action | Tier | Effort |
|---|---|---|---|---|---|
| RF-HDGC-CDH1-CONFIRMED-CARRIER | CDH1 carriers → PTG 20-30; lifetime DGC risk ~37-42% F / ~33-37% M (downward-revised per IGCLC 2020 + Hansford 2015) | NCCN-GFBO-2025, NCCN-BREAST-2025, ESMO-GASTRIC-2024 | Confirm IGCLC 2020 PTG age range + Hansford 2015 risk numbers; check ESMO-GASTRIC-2024 actually addresses HDGC (some editions omit) | 🔴 | high |
| IND-HDGC-CDH1-CARRIER-PREVENTION-SURVEILLANCE | EGD q6-12mo Cambridge protocol for PTG-decliners; F: annual mammo + MRI from age 30 | NCCN-GFBO-2025, NCCN-BREAST-2025, ESMO-GASTRIC-2024 | Confirm Cambridge protocol still endorsed in IGCLC 2020 (some recent literature questions yield); verify "estrogen-only HRT" do-not-do has source support | 🔴 | high |
| RF-CMMRD-CONFIRMED-CARRIER | Biallelic MMR → ~100% cancer by adolescence; immunotherapy effective in established CMMRD cancers | NCCN-GFCRC-2025, ASCO-ACMG-LYNCH-2014 | Confirm C4CMMRD 2014 + Tabori 2017 update support q6mo brain MRI from age 2; check ASCO-ACMG-LYNCH-2014 actually covers biallelic / CMMRD (it's typically Lynch monoallelic) — possible source mismatch | 🔴 | high |
| IND-CMMRD-CARRIER-PREVENTION-SURVEILLANCE | q6mo brain MRI from age 2; q6mo colonoscopy from age 6; avoid alkylating + topo-II chemo; anti-PD-1 for established cancers | NCCN-GFCRC-2025, ASCO-ACMG-LYNCH-2014 | Same source-coverage concern as RF row. Confirm "avoid empiric RT" framing (rather than "contraindicated" — radiation IS used in established cancers when needed) | 🔴 | high |
| RF-RHABDOID-PREDISPOSITION-CONFIRMED-CARRIER | SMARCB1/SMARCA4 → near-100% early-childhood penetrance; q3mo brain MRI infancy → age 4 | NCCN-CNS-2025, NCCN-GFBO-2025 | Verify NCCN-CNS-2025 covers RTPS surveillance (likely sparse — primary source is Foulkes 2017 IRSC consensus); flag source gap if confirmed | 🔴 | high |
| IND-RHABDOID-PREDISPOSITION-CARRIER-SURVEILLANCE | Brain MRI q3mo infancy → age 4 → q6mo to age 5; WB-MRI q3-6mo to age 5; SMARCA4 → SCCOHT surveillance from menarche | NCCN-CNS-2025, NCCN-GFBO-2025 | Same source-gap concern. Verify SCCOHT surveillance modality (TVUS vs pelvic exam) per Foulkes / Witkowski IRSC | 🔴 | medium |
| RF-BECKWITH-WIEDEMANN-CONFIRMED-CARRIER + IND-...-SURVEILLANCE | q3mo abdominal US birth-to-8 + monthly AFP birth-to-3-4 then q3mo to age 4; subtype-aware (IC1 highest Wilms risk) | NCCN-GFBO-2025 (context), AASLD-HCC-2023 (context) | Confirm Brioude 2018 AJMG consensus + Kalish 2017 AACR — neither cited as primary source. Add as primary sources or rely on context citations | 🔴 | medium |
| RF-DICER1-CONFIRMED-CARRIER + IND-...-SURVEILLANCE | DICER1 → PPB childhood + Sertoli-Leydig adolescent + multinodular goiter ~75% | (verify) | Confirm Schultz 2018 / Stewart 2019 DICER1 surveillance consensus is cited (or stub a SRC- for it); verify chest CT cadence stated in YAML | 🔴 | medium |
| RF-NF1-CONFIRMED-CARRIER + IND-...-SURVEILLANCE | NF1 F lifetime breast ~18% by 50 / ~50% by 70 (BRCA2-comparable); MPNST ~10-15% lifetime | NCCN-GFBO-2025, NCCN-BREAST-2025 | Verify NCCN-GFBO-2025 covers NF1 breast surveillance (added in recent editions); confirm "MPNST symptom-driven" stance vs. some centers screening WB-MRI | 🔴 | high |
| RF-ATM-CONFIRMED-CARRIER + IND-...-SURVEILLANCE | ATM het: breast mammo from 40 ± MRI (moderate-tier); pancreatic surveillance ONLY if PDAC FDR/SDR; therapeutic radiation SAFE in heterozygotes | NCCN-GFBO-2025, NCCN-BREAST-2025 | Critical do-not-do "do not extrapolate biallelic A-T radiation sensitivity to heterozygotes" — verify CAPS Consortium 2022 cited correctly; confirm ATM c.7271T>G earlier-mammography note | 🔴 | medium |
| RF-PALB2-CONFIRMED-CARRIER + IND-...-SURVEILLANCE | PALB2 → BRCA-style annual MRI + mammo from age 30; pancreatic surveillance if PDAC FDR | NCCN-GFBO-2025, NCCN-BREAST-2025 | Confirm PALB2 promoted to BRCA-tier in NCCN-GFBO-2025 (was moderate-tier in 2022); verify CAPS Consortium cited | 🔴 | medium |
| RF-COSTELLO-CONFIRMED-CARRIER + IND-COSTELLO-CARRIER-INTENSIFIED | HRAS → 6-15% lifetime cancer; embryonal RMS childhood + bladder TCC in adolescents/adults; HCM cardiac comorbidity gates therapy | NCCN-GFBO-2025, ESMO-SARCOMA-2024, NCCN-BLADDER-2025 | Confirm Gripp 2019 / 2022 Costello surveillance consensus; verify NCCN-BLADDER-2025 cited makes sense (TCC risk window is age >20) | 🔴 | medium |
| DRUG-FULVESTRANT-PREVENTION | Pure ER antagonist; "Engine MUST NOT surface for prevention"; SERD class completeness only | USPSTF-BREAST-2024, NCCN-BREAST-2025 | Read the engine routing layer + render layer to confirm `intent: prevention` filter excludes this drug — gating must be enforced in code, not just documented in notes | 🔴 | low |
| IND-CASCADE-LYNCH-FDR-POSITIVE-TESTING | Site-specific cascade testing first-line; 50% prior probability in FDR; counseling-first | NCCN-GFCRC-2025, ASCO-ACMG-LYNCH-2014, ESMO-CRC-2024 | Verify cost figures (~3000-6000 UAH site-specific vs 5000-15000 UAH panel) reflect current Ukrainian lab pricing 2026-Q2 | 🟡 | low |
| IND-IATROGENIC-METHOTREXATE-LONGTERM-LYMPHOMA-PREVENTION-SURVEILLANCE | Annual MTX necessity review + CBC q6-12mo; MTX-withdrawal trial achieves 30-60% MTX-LPD regression | (verify) | Confirm Hoshida + Tokuhira retrospective series cited; verify DLBCL-NOS disease anchor is appropriate (vs HEM-DLBCL) | 🟡 | low |
| IND-REPRODUCTIVE-ENDOMETRIOSIS-OVARIAN-PREVENTION-SURVEILLANCE | "NO population screening for ovarian cancer" framing + opportunistic salpingectomy at hysterectomy | (verify) | Confirm Hanley JAMA Network 2022 cited; confirm UKCTOCS long-term + PLCO referenced; verify SGO+ACOG 2024 endorsement | 🟡 | low |

Effort key: **low** ≤30 min (single guideline lookup); **medium** ≤2 h
(multi-source reconciliation); **high** ≥2 h (clinical-judgment +
controversy review).

---

## Cross-cutting verification themes

### 1. Source citation integrity (Wave L diff only)

Confirm each cited source actually supports the claim. Concrete check:

```powershell
# List every Wave L source citation
git diff d60004b723..HEAD -- "knowledge_base/hosted/content/" | Select-String -Pattern "^\+\s+source_id: SRC-" | Group-Object Line | Sort-Object Count -Descending
```

**Specific concerns flagged in row-level checklist:**
- CMMRD entities cite ASCO-ACMG-LYNCH-2014 — Lynch monoallelic ≠ CMMRD biallelic. Likely needs Tabori 2017 / Wimmer 2014 (C4CMMRD) as primary source.
- Rhabdoid entities cite NCCN-CNS-2025 — surveillance content is typically thin in NCCN; primary source is Foulkes 2017 IRSC consensus. Either confirm NCCN coverage or add Foulkes as a Source stub.
- Beckwith-Wiedemann entities cite only NCCN-GFBO-2025 + AASLD-HCC-2023 as `position: context` — neither is a primary BWS source. Brioude 2018 AJMG + Kalish 2017 AACR are the canonical references; add as Source stubs if missing.
- DICER1 entities need Schultz 2018 / Stewart 2019 DICER1-syndrome surveillance consensus.

### 2. STUB consistency on Wave L additions

Every Wave L entity must have `draft: true` + `reviewer_signoffs: 0` +
STUB note. Check:

```powershell
# Wave L RFs with draft: true (expect 34 new RFs; 43 total includes 9 Wave K cherry-picks already draft)
git diff d60004b723..HEAD --name-only -- "knowledge_base/hosted/content/redflags/" | ForEach-Object { Select-String -Path $_ -Pattern "^draft: true" -SimpleMatch } | Measure-Object | Select-Object Count

# Wave L Indications with reviewer_signoffs: 0
git diff d60004b723..HEAD --name-only -- "knowledge_base/hosted/content/indications/" | ForEach-Object { Select-String -Path $_ -Pattern "^reviewer_signoffs: 0" -SimpleMatch } | Measure-Object | Select-Object Count
```

Already enforced by `tests/test_prevention_kb_audit.py`
(`test_prevention_redflag_stub_consistency`, `test_prevention_indication_stub_consistency`). Re-run before signoff commits:

```powershell
C:/Python312/python.exe -m pytest tests/test_prevention_kb_audit.py -q
```

Current state: **44 sub-tests pass.**

### 3. Banned-source policy compliance

Wave L diff must not introduce SRC-ONCOKB / SRC-SNOMED / SRC-MEDDRA
citations.

```powershell
git diff d60004b723..HEAD -- "knowledge_base/hosted/content/" | Select-String -Pattern "^\+.*SRC-(ONCOKB|SNOMED|MEDDRA)"
```

Current state: **0 hits** on the Wave L diff. (Note: 200+ legacy
SRC-ONCOKB occurrences exist in pre-baseline files — these are
migration metadata per CIViC pivot, render layer suppresses them;
they are NOT Wave L regressions.)

### 4. Reference integrity (every `triggered_by_redflags`, `sources`, `applicable_to.disease_id` resolves)

Already enforced by `tests/test_prevention_kb_audit.py`
(`test_prevention_indication_triggered_redflag_refs_resolve`,
`test_prevention_indication_source_refs_resolve`,
`test_prevention_indication_disease_anchor_resolves`). Test count
above (44) covers this.

**Known acceptable mismatches** (flagged in YAML notes, NOT bugs):
- Rhabdoid + ATRT use `DIS-GLIOMA-LOW-GRADE` as nearest CNS anchor (no DIS-ATRT existed when RF authored; DIS-ATRT now exists but cross-link not yet updated → v0.4 cleanup).
- BWS uses `DIS-WILMS` as anchor; hepatoblastoma cancer-spectrum noted in rationale prose only (no DIS- anchor in KB yet).

### 5. Engine gating contract (DRUG-FULVESTRANT-PREVENTION specifically)

`DRUG-FULVESTRANT-PREVENTION.notes` says: "Engine MUST NOT surface
fulvestrant as a chemoprevention option." This is a contract on the
render layer, not just documentation. Verify by inspection of the
prevention routing code in `knowledge_base/engine/`:

```powershell
Select-String -Path "knowledge_base/engine/*.py" -Pattern "FULVESTRANT" -SimpleMatch
```

If no enforcing code exists, raise as a v0.4 follow-up: add a
class-completeness-only filter to suppress fulvestrant from any
`intent: prevention` Indication recommendation surface.

---

## Recommended signoff process (executable by either Co-Lead alone)

Two-Co-Lead signoff per CHARTER §6.1. Read this section as a script.

### Step 1 — Initial pass (Co-Lead A — verify 🔴 tier first)

Triage the 10 🔴 rows above. For each:

1. Open the relevant YAML file (`knowledge_base/hosted/content/redflags/rf_*.yaml` and the paired `knowledge_base/hosted/content/indications/ind_*.yaml`).
2. Cross-check the clinical claim against the cited source(s) in the row. If you have direct access to NCCN / IGCLC / C4CMMRD / Brioude / Schultz / Foulkes / CAPS guidelines, compare line-by-line; if not, use the verification-action note as a search prompt against PubMed / NCCN-PDF / society websites.
3. **If you agree with the claim** → in the YAML, append your name to `reviewers:` (currently `[]`); increment `reviewer_signoffs:` from 0 → 1.
4. **If you disagree** → leave the `draft: true` + `reviewer_signoffs: 0` as-is. Add your concern to `known_controversies:` as a new entry, or open a PR comment if the disagreement is binary (e.g., "wrong source" rather than "alternative valid position").
5. **Do NOT** flip `draft: true → false` yet. Second signoff is required.

### Step 2 — Second pass (Co-Lead B)

For each row Co-Lead A signed off:

1. Read Co-Lead A's signoff in `reviewers:`.
2. Independently confirm the claim against the same sources (or others).
3. **If you concur** → append your name; increment `reviewer_signoffs:` from 1 → 2; flip `draft: true → false`; set `last_reviewed:` to today's date.
4. **If you disagree** → leave `reviewer_signoffs: 1` + `draft: true`; add a `known_controversies:` entry or PR comment; Co-Lead A should respond.

### Step 3 — Gate the post-signoff commit

After each batch of signoffs (recommend batch size: one triage tier per session — 🔴 first, then 🟡, then 🟢), run the gate before commit:

```powershell
# Audit suite must stay green
C:/Python312/python.exe -m pytest tests/test_prevention_kb_audit.py -q

# Engine + render suites
C:/Python312/python.exe -m pytest tests/test_prevention_engine.py tests/test_prevention_render.py -q

# Validator
C:/Python312/python.exe -m knowledge_base.validation.validate_all
```

All three must pass. If any fail, fix before committing.

### Step 4 — Commit signoffs

Single commit per signoff batch. Use explicit pathspec (CLAUDE.md
bans `-A`):

```powershell
git add knowledge_base/hosted/content/redflags/rf_hdgc_cdh1_confirmed_carrier.yaml `
        knowledge_base/hosted/content/indications/ind_hdgc_cdh1_carrier_prevention_surveillance.yaml `
        # ...more files as appropriate
git commit -m "review(wave-l): 🔴-tier signoffs (HDGC, CMMRD, ...)"
```

### Step 5 — When all three tiers fully signed off

After all 43 RFs + 84 Indications + 4 diseases + 12 drugs have
`reviewer_signoffs: 2` and `draft: false`:

1. Update `wave-l-kb-coverage-2026-05-19.md` "Audit-trail compliance" section: replace `pending_clinical_signoff` with `signed_off_two_co_leads`.
2. Open PR from `wave-l-prep-2026-05-19` → `master` for two-Co-Lead-approved merge.
3. The orchestrating session reviews + merges; agents do not push directly to master.

### Triage-effort estimate

- 🔴 tier (10 entries, ~5 high + 5 medium): ~20-25 hours combined for both Co-Leads.
- 🟡 tier (5 pattern-exemplars + ~50 sibling accepts-by-pattern): ~8-12 hours.
- 🟢 tier (2 pattern-exemplars + ~20 sibling accepts): ~2-4 hours.

Total: **~30-40 Co-Lead-hours** to clear Wave L+M from STUB to
signed-off.

---

## Stop conditions for the Co-Leads

Abort + report (do not proceed to flip `draft: false`) if:
- Cited source does not exist or does not address the claim.
- Source supports a materially different recommendation than YAML encodes (e.g., different starting age, different cadence, different drug class).
- Wave L entity is `draft: false` already → indicates parallel-session error; investigate before adding signoff.
- Pre-flight tests fail → fix root cause (do not commit signoffs over a failing audit suite).
- Banned-source (SRC-ONCOKB / SNOMED / MEDDRA) citation found in Wave L entity → coordinate with maintainer to substitute before signoff.

---

## Companion documents

- `docs/reviews/wave-l-kb-coverage-2026-05-19.md` — coverage metrics + commit-by-commit log.
- `specs/CHARTER.md` §6.1 — two-reviewer signoff policy + dev-mode exemption.
- `specs/CLINICAL_CONTENT_STANDARDS.md` — citation + claim standards.
- `tests/test_prevention_kb_audit.py` — automated audit gates (44 sub-tests).
