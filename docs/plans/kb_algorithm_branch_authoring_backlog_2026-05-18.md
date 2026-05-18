# KB-authoring backlog: algorithm-branch coverage gaps (2026-05-18)

## Why this exists

The verified-treatment-examples workstream (PR #594) ran every public
patient example through `generate_plan()` and audited which
`(disease_id, line_of_therapy, recommended_regimen)` signatures are
exercised. It accepted **40 new examples**, covering signatures whose
indications are reachable from the patient profile via the algorithm's
decision tree. It **rejected 89** signatures where the engine could not
be driven to the target.

Every one of those 89 rejections is a `default_indication_mismatch`. The
generator produced a patient that should satisfy the indication's
`applicable_to` block, but the algorithm walked past the target step
because the step's `evaluate:` clauses are written as free-text
`condition:` strings rather than machine-evaluable
`finding:` / `biomarker:` / `red_flag:` references.

This is the same class of issue as the larger silent-False audit
(`docs/reviews/openonco-state-audit-2026-05-17.md` — 376/443 = 85% of
indication clauses are prose, 45/152 = 30% of algorithms fall through
on every patient). This document is a narrower, more actionable view:
which **specific algorithm steps** are blocking which **specific
treatment plans** from being reachable today.

## Acceptance criteria for a chunk built from this backlog

A chunk targeting one algorithm `ALGO-X` is done when:

1. Every indication in `ALGO-X.output_indications` is reachable from
   *some* synthetic patient that the auditor accepts.
2. `scripts/generate_verified_treatment_examples.py` produces an accepted
   example for each of those indications, with the same default-
   indication-match invariant.
3. The free-text `condition:` strings in the rewritten steps either
   become RedFlag references (preferred), `finding:`/`biomarker:`
   references, or remain prose **with an explicit MDT-evaluated note**
   so the engine knows the branch is intentionally MDT-only and won't
   silently fall through.

Authoring effort per step is roughly the same as the existing
`RF-AITL-ROMIDEPSIN-INELIGIBLE` pattern in
`knowledge_base/hosted/content/redflags/rf_aitl_romidepsin_ineligible.yaml`
— a 30-line RF YAML with `any_of: [finding..., finding..., condition...]`
triggers — plus a one-line algorithm-step rewrite.

## Backlog (by algorithm, highest yield first)

Total: **52 algorithms** with at least one unreachable output indication.
Sum of unreachable signatures: **89**.

| algorithm                               | missing | example unreachable indication      |
|---|---:|---|
| ALGO-OVARIAN-2L                         | 6 | IND-OVARIAN-RECURRENT-PARP-REPEAT, IND-OVARIAN-RECURRENT-TOPOTECAN, IND-OVARIAN-RECURRENT-GEMCITABINE |
| ALGO-BREAST-1L                          | 5 | IND-BREAST-HR-POS-EARLY-ADJ-CDK46I, IND-BREAST-BRCA-POS-MET-PARPI, IND-BREAST-TNBC-METASTATIC-1L-PEMBRO-CHEMO |
| ALGO-ESOPH-METASTATIC-1L                | 5 | IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT, IND-ESOPH-OLIGOMET-SYSTEMIC-PLUS-LOCAL, IND-ESOPH-METASTATIC-1L-FLOT |
| ALGO-ALCL-2L                            | 3 | IND-ALCL-MAINTENANCE-BV-POST-ASCT, IND-ALCL-2L-BRENTUXIMAB-MONO, IND-ALCL-2L-CRIZOTINIB-ALKPOS |
| ALGO-NSCLC-METASTATIC-1L                | 3 | IND-NSCLC-1L-*-NON-DEFAULT branches |
| ALGO-NSCLC-METASTATIC-2L                | 3 | IND-NSCLC-2L-*-NON-DEFAULT branches |
| ALGO-RCC-METASTATIC-1L                  | 3 | IND-RCC-METASTATIC-1L-* branches |
| ALGO-SCLC-2L                            | 3 | IND-SCLC-2L-* branches |
| ALGO-UROTHELIAL-METASTATIC-2L           | 3 | IND-UROTHELIAL-2L-* branches |
| ALGO-ANAL-SCC-1L                        | 2 | IND-ANAL-SCC-METASTATIC-* |
| ... 42 more, 1–2 each (see report)      | 53 | |

Authoritative full list with patient/algorithm trace: see
[docs/verified-examples-skips.md](../verified-examples-skips.md) and
[docs/example-plan-coverage-report.json](../example-plan-coverage-report.json)
(`missing_via_algorithm` array — disease_id, line_of_therapy,
regimen_id, indication_ids).

## How to fix one algorithm

Take `ALGO-AITL-2L` as the worked example:

- **Default indication** (`IND-AITL-2L-AZACITIDINE`) — already
  reachable; no action.
- **Step 3 → `IND-AITL-2L-BELINOSTAT`** — already wired with
  `RF-AITL-ROMIDEPSIN-INELIGIBLE`; verified reachable.
- **Step 2 → `IND-AITL-2L-ROMIDEPSIN`** — currently unreachable. Step 2
  has only free-text conditions ("HDAC-inhibitor-naive", "Romidepsin
  accessible", "No baseline cardiac arrhythmia"). To make it
  reachable:
    1. Author a `RF-AITL-HDACI-NAIVE-ROMIDEPSIN-CANDIDATE` (or
       equivalent) with positive triggers — e.g.
       `finding: prior_hdaci_exposure value: false`,
       `finding: romidepsin_accessible value: true`,
       `finding: qtc_ms threshold: 480 comparator: "<"`.
    2. Replace step 2's free-text clauses with
       `red_flag: RF-AITL-HDACI-NAIVE-ROMIDEPSIN-CANDIDATE`.
    3. Re-run `scripts/generate_verified_treatment_examples.py` — the
       previously-rejected `DIS-AITL · L2 · REG-ROMIDEPSIN-PTCL` should
       now accept.
- **Clinical sign-off** — per CHARTER §6.1, RF authoring touching
  clinical content needs two Clinical Co-Lead approvals.

This pattern (1 RF + 1 algorithm-step rewrite + 1 generator re-run) is
repeatable across all 52 algorithms. Expected yield: 89 more verified
examples → 294/294 algorithm-routeable signatures publicly covered.

## Priority shortlist

Five algorithms whose missing indications have the highest clinical
visibility (high-volume diseases, high-impact biomarker-targeted
therapies):

1. **`ALGO-BREAST-1L`** (5 unreachable) — adjuvant CDK4/6i + PARPi + TNBC
   first-line pembrolizumab combo are commonly searched and the
   default `IND-BREAST-HR-POS-MET-1L-CDKI` swallows everything.
2. **`ALGO-NSCLC-METASTATIC-1L`** (3 unreachable) — most-searched
   disease; capmatinib and selpercatinib branches are partially wired
   but specific NDC variants miss.
3. **`ALGO-CRC-METASTATIC-2L`** — KRAS G12C sotorasib and HER2-amp
   tucatinib branches gated by free-text biomarker clauses.
4. **`ALGO-OVARIAN-2L`** (6 unreachable) — biggest single-algorithm gap.
5. **`ALGO-RCC-METASTATIC-1L`** (3 unreachable) — IMDC-risk-stratified
   branches currently fall through to a single default.

Anything else can wait until these five are landed.

## See also

- [docs/example-plan-coverage-report.md](../example-plan-coverage-report.md) —
  human-readable audit summary.
- [docs/verified-examples-skips.md](../verified-examples-skips.md) —
  one line per rejected signature with engine output.
- [docs/reviews/openonco-state-audit-2026-05-17.md](../reviews/openonco-state-audit-2026-05-17.md) —
  broader free-text-condition audit (376/443 = 85% prose) that this
  workstream is a concrete instance of.
- [knowledge_base/hosted/content/redflags/rf_aitl_romidepsin_ineligible.yaml](../../knowledge_base/hosted/content/redflags/rf_aitl_romidepsin_ineligible.yaml) —
  worked example of the RF pattern this backlog asks for.
