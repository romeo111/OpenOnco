# Low Coverage: Biomarkers, Drugs, Regimens

Generated from local hosted YAML inspection on 2026-05-07.

This is a remediation queue, not clinical guidance. Counts were produced from
`knowledge_base/hosted/content` using a lightweight local pass over disease,
biomarker-actionability, indication, and regimen files. Regimen-to-drug counts
depend on `recommended_regimen` links resolving to regimen files with
`components[].drug_id`; a zero drug count can therefore mean either no mapped
therapy or a referential/component integrity gap.

## Baseline

- Diseases checked: 78
- Diseases with 0 biomarker-actionability rows: 17
- Diseases with thin biomarker coverage, 1-2 rows: 34
- Diseases with 0 regimens: 8
- Diseases with exactly 1 regimen: 8
- Diseases with 0 mapped drugs: 11
- Diseases with exactly 1 mapped drug: 7

The existing `docs/kb-coverage-matrix.md` reports 65 diseases, so the matrix is
stale or uses a narrower disease set than the current hosted disease YAML.

## Scoring

`low_score` is a triage score only:

- `+2` for zero biomarker-actionability rows.
- `+1` for 1-2 biomarker-actionability rows.
- `+2` for zero regimens.
- `+1` for exactly 1 regimen.
- `+2` for zero mapped drugs.
- `+1` for exactly 1 mapped drug.

Target floor for general coverage: at least 3 biomarker-actionability rows
where disease biology supports it, at least 2 indication/regimen paths, and at
least 2 mapped drug components. Rare diseases may intentionally stay below this
floor when the safer state is explicit specialist referral, trial referral, or
local-therapy dominance.

## Highest-Priority Rows

| Disease | Biomarkers | Indications | Regimens | Drugs | Low score | First safe action |
|---|---:|---:|---:|---:|---:|---|
| `DIS-EPITHELIOID-SARCOMA` | 1 | 0 | 0 | 0 | 5 | Add sourced draft advanced/unresectable path or explicit deferral state |
| `DIS-GRANULOSA-CELL` | 1 | 0 | 0 | 0 | 5 | Specialist-review queue before systemic authoring |
| `DIS-JMML` | 1 | 0 | 0 | 0 | 5 | Pediatric hematology review before systemic authoring |
| `DIS-LAM` | 1 | 0 | 0 | 0 | 5 | Confirm oncology-scope fit; likely defer from regimen coverage |
| `DIS-MENINGIOMA` | 1 | 0 | 0 | 0 | 5 | Model recurrence around surgery/radiation/trial referral first |
| `DIS-TGCT` | 1 | 0 | 0 | 0 | 5 | Add CSF1R/local-therapy decision path if source-backed |
| `DIS-BCC` | 2 | 0 | 0 | 0 | 5 | Add HHI and post-HHI PD-1 draft paths |
| `DIS-GLIOMA-LOW-GRADE` | 2 | 1 | 0 | 0 | 5 | Repair indication-to-regimen link; separate local/systemic sequence |
| `DIS-CHONDROSARCOMA` | 0 | 1 | 1 | 1 | 4 | Add biology/actionability rows or explicit non-actionable status |
| `DIS-GI-NET` | 0 | 1 | 1 | 1 | 4 | Add SSA/PRRT/targeted/chemo biomarker-context queue |
| `DIS-IMT` | 0 | 1 | 1 | 1 | 4 | Add ALK/NTRK/ROS1 actionability rows |
| `DIS-PNET` | 0 | 1 | 1 | 1 | 4 | Add grade/site/SSA/PRRT/targeted sequencing queue |
| `DIS-MESOTHELIOMA` | 0 | 2 | 2 | 0 | 4 | Investigate regimen component drug IDs |
| `DIS-TESTICULAR-GCT` | 0 | 4 | 3 | 0 | 4 | Investigate regimen component drug IDs |
| `DIS-SOFT-TISSUE-SARCOMA` | 0 | 4 | 4 | 0 | 4 | Investigate regimen component drug IDs |

## Axis-Specific Queues

### Zero Biomarker-Actionability

`DIS-CHONDROSARCOMA`, `DIS-GI-NET`, `DIS-IMT`, `DIS-PNET`,
`DIS-MPNST`, `DIS-MESOTHELIOMA`, `DIS-T-PLL`, `DIS-EATL`,
`DIS-HSTCL`, `DIS-TESTICULAR-GCT`, `DIS-ANAL-SCC`, `DIS-NK-T-NASAL`,
`DIS-PMBCL`, `DIS-SOFT-TISSUE-SARCOMA`, `DIS-APL`, `DIS-PTCL-NOS`,
`DIS-HNSCC`.

### Regimen Count Below Two

`DIS-EPITHELIOID-SARCOMA`, `DIS-GRANULOSA-CELL`, `DIS-JMML`,
`DIS-LAM`, `DIS-MENINGIOMA`, `DIS-TGCT`, `DIS-BCC`,
`DIS-GLIOMA-LOW-GRADE`, `DIS-CHONDROSARCOMA`, `DIS-GI-NET`,
`DIS-IMT`, `DIS-PNET`, `DIS-MPNST`, `DIS-IFS`, `DIS-SALIVARY`,
`DIS-THYROID-PAPILLARY`.

### Mapped Drug Count Below Two

`DIS-MESOTHELIOMA`, `DIS-TESTICULAR-GCT`, `DIS-SOFT-TISSUE-SARCOMA`,
`DIS-EPITHELIOID-SARCOMA`, `DIS-GRANULOSA-CELL`, `DIS-JMML`,
`DIS-LAM`, `DIS-MENINGIOMA`, `DIS-TGCT`, `DIS-BCC`,
`DIS-GLIOMA-LOW-GRADE`, `DIS-CHONDROSARCOMA`, `DIS-GI-NET`,
`DIS-IMT`, `DIS-PNET`, `DIS-IFS`, `DIS-THYROID-PAPILLARY`, `DIS-GBM`.

## Execution Plan

1. Preserve this queue and treat it as the disease-level coverage backlog.
2. Start with `DIS-BCC`, because the hosted disease and biomarker-actionability
   files already contain source IDs and an explicit HHI/post-HHI PD-1 pathway.
3. Keep new clinical rows draft/pending review unless two reviewer signoffs are
   added later through the signoff workflow.
4. Add only source-linked entities:
   - missing source stubs for regulatory labels or trials when needed;
   - missing drug entities for regimen components;
   - regimen records with `components[].drug_id`;
   - indication records that reference those regimens;
   - draft drug-indication rows for label/access audit.
5. Run available local validation. Python is unavailable in this sandbox, so
   schema validation may need to be run later with `py -V:3.12` or equivalent.
6. Continue disease-by-disease in this order:
   - `DIS-BCC`
   - `DIS-TGCT`
   - `DIS-EPITHELIOID-SARCOMA`
   - `DIS-GLIOMA-LOW-GRADE`
   - regimen-component integrity repair for `DIS-MESOTHELIOMA`,
     `DIS-TESTICULAR-GCT`, and `DIS-SOFT-TISSUE-SARCOMA`
   - biomarker-actionability pass for `DIS-IMT`, `DIS-PNET`, `DIS-GI-NET`,
     and `DIS-CHONDROSARCOMA`

## Quality Gate

- No new recommendation without at least one source ID.
- No regimen without valid `DRUG-*` component IDs.
- No drug-indication row marked reviewed unless jurisdiction-specific label or
  payer evidence is attached.
- No disease is considered closed merely because a row exists; the minimum
  close condition is disease-specific source backing plus clinical signoff.

## Execution Log

### 2026-05-07: BCC Starter Slice

Started `DIS-BCC` because hosted disease/BMA files already contained a clear
HHI and post-HHI PD-1 pathway plus source IDs. Added draft source, drug,
regimen, indication, and drug-indication rows for:

- `REG-VISMODEGIB-BCC` / `IND-BCC-ADVANCED-1L-VISMODEGIB`
- `REG-SONIDEGIB-BCC` / `IND-BCC-ADVANCED-1L-SONIDEGIB`
- `REG-CEMIPLIMAB-BCC` / `IND-BCC-ADVANCED-2L-CEMIPLIMAB`

Post-slice local coverage for `DIS-BCC`: 2 biomarker-actionability rows,
3 indications, 3 referenced regimens, and 3 mapped drugs. Rows remain draft and
pending clinical signoff.

### 2026-05-07: Epithelioid Sarcoma Blocked

Scanned `DIS-EPITHELIOID-SARCOMA` as the next apparently easy target because
`DRUG-TAZEMETOSTAT`, `SRC-EZH202-GOUNDER-2020`, and
`BMA-SMARCB1-EPITHELIOID-SARCOMA` already exist. Authoring a new recommended
tazemetostat indication was paused after finding a 2026-03-09 Ipsen voluntary
withdrawal notice for Tazverik across follicular lymphoma and epithelioid
sarcoma. Added `SRC-IPSEN-TAZVERIK-WITHDRAWAL-2026` and marked
`DRUG-TAZEMETOSTAT` with `market_status: voluntary_withdrawal_announced`.

Next safe action: clinical/regulatory review before any epithelioid sarcoma
treatment-row authoring. This disease remains a coverage gap, but it is no
longer a silent gap.
