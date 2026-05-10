# RCC 1L Routing Gap — Diagnostic Report

**Date:** 2026-05-09  
**Author:** Diagnostic agent (claude/romantic-ellis-de1a2b worktree)  
**Status:** Gap resolved in current master; stale artefacts remain. See §3.  
**Clinical authoring needed:** Yes — two-reviewer signoff on RF pending. See §4.

---

## 1. Fixture expectations

`examples/patient_rcc_imdc_int_nivo_ipi.json` — synthetic clear-cell metastatic RCC,
male 62, ECOG 1, IMDC intermediate risk (2 adverse factors: Hgb 11.4 g/dL < LLN;
KPS 80 straddles cut-off). `imdc_risk: "intermediate"`, `imdc_risk_factors_count: 2`,
`active_autoimmune_disease: false`, `prior_systemic_therapy: false`.

Golden: `IND-RCC-METASTATIC-1L-NIVO-IPI` (nivolumab + ipilimumab, CheckMate-214).

Test (Python 3.12): **PASSES** as of commit `a63794679`.

---

## 2. Decision-tree routing (current state)

`ALGO-RCC-METASTATIC-1L` routes this patient via four steps:

| Step | Evaluates | Result for this patient |
|------|-----------|------------------------|
| 1 | Histology gate: `clear_cell_rcc` | **true** → step 2 |
| 2 | `RF-RCC-IMDC-INTERMEDIATE-POOR-RISK` | **fires** (`imdc_risk = "intermediate"`) → step 4 |
| 4 | `active_autoimmune_disease = false` | **true** → `IND-RCC-METASTATIC-1L-NIVO-IPI` ✓ |

Routing is correct. The RF exists at
`knowledge_base/hosted/content/redflags/rf_rcc_imdc_intermediate_poor_risk.yaml`
and is wired to `ALGO-RCC-METASTATIC-1L` via `shifts_algorithm`.

---

## 3. Historical gap and how it was closed

The fixture's `comment` field records the original drift:

> "ALGO-RCC-METASTATIC-1L step 1 uses free-text 'IMDC intermediate or poor risk'
> without a disease-scoped RF, so engine routes to default
> IND-RCC-METASTATIC-1L-PEMBRO-AXI. Drift acknowledged — RF authoring
> (RF-RCC-IMDC-INTERMEDIATE-POOR) tracked separately."

This was the state before PR #171 (`feat(kb): W5b + W5c integration — 14 KB
authoring drift fixes`). That PR authored `RF-RCC-IMDC-INTERMEDIATE-POOR-RISK`
and wired step 2 of the algorithm to use it as a structured `red_flag` clause
instead of the unevaluable free-text condition. The comment in the fixture is now
stale and should be updated to reflect the resolved state.

**Potential remaining CI failure vector:** the test collection fails on Python 3.8
(default on Windows) with `TypeError: 'type' object is not subscriptable` at
`knowledge_base/schemas/base.py:208` (`list[str]` syntax requires Python 3.9+).
CI must run with Python 3.12 as specified in CLAUDE.md. This is not a clinical
routing bug — it is a CI configuration gap.

---

## 4. Clinical authoring work required (CHARTER §6.1)

`rf_rcc_imdc_intermediate_poor_risk.yaml` carries:

```yaml
ukrainian_review_status: pending_clinical_signoff
ukrainian_drafted_by: claude_extraction
```

The RF definition and trigger logic are clinically complete and backed by
SRC-CHECKMATE214-MOTZER-2018 / SRC-KEYNOTE426-RINI-2019 / SRC-NCCN-KIDNEY-2025,
but CHARTER §6.1 requires two Clinical Co-Lead sign-offs before this RF is
considered authoritative for production plans.

Additionally, the RF notes flag a potential conflict-resolution concern: if
`RF-RCC-FRAILTY-AGE` co-fires (de-escalate direction), the current severity matrix
gives `RF-RCC-IMDC-INTERMEDIATE-POOR-RISK` (intensify, priority 80) precedence.
Clinical review should confirm whether frailty should disqualify ICI doublet
independently of the severity matrix.

**No algorithm or RF YAML changes were made in this diagnostic pass.**
