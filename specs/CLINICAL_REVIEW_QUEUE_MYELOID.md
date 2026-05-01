# Clinical Review Queue — Myeloid Expansion (heme)

**To:** OpenOnco clinical reviewer (hemato-oncologist specializing in
myeloid malignancies).
**Context:** On 2026-04-25 a vertical covering 7 myeloid diagnoses was added
(AML, APL, CML, MDS-LR, MDS-HR, PV, ET, PMF). All entities are marked
`STUB — requires clinical co-lead signoff before publication`. CHARTER §6.1
requires two clinical reviewer sign-offs before any entity is published to
`knowledge_base/hosted/content/`.

**Files:** All located under `knowledge_base/hosted/content/{diseases,redflags,
indications,regimens,algorithms,drugs,sources}/` with prefixes
`aml_/apl_/cml_/mds_/pv_/et_/pmf_/_pv_et_/`. New sources also added: SRC-ELN-AML-2022,
SRC-ELN-APL-2019, SRC-ELN-CML-2020, SRC-ESMO-AML-2020, SRC-ESMO-CML-2017,
SRC-ESMO-MPN-2015, SRC-ESMO-MDS-2021, SRC-IPSS-M-BERNARD-2022,
SRC-DIPSS-PLUS-GANGAT-2011, SRC-VIALE-A-DINARDO-2020, SRC-RATIFY-STONE-2017,
SRC-APL0406-LOCOCO-2013, SRC-IRIS-OBRIEN-2003, SRC-RESPONSE-VANNUCCHI-2015,
SRC-COMFORT-I-VERSTOVSEK-2012, SRC-COMMANDS-FENAUX-2020.

---

## TL;DR — review priority

1. **Block A — APL emergency / time-critical positioning** (2-4 hours).
   APL is the only "molecularly-defined emergency" archetype in the KB.
   Question: did we correctly set `time_critical: true` on
   IND-APL-1L-* + is the wording in the notes correct regarding CHARTER
   §15.2 C2 (initial ATRA initiation outside the non-device CDS carve-out)?

2. **Block B — AML + MDS-HR ven+aza off-label** (1-2 hours).
   Ven+aza in MDS-HR is an off-label extrapolation from VIALE-A AML;
   documented as IND-MDS-HR-1L-VEN-AZA with NCCN category 2A. Question:
   should this opt-in alternative remain as-is, or be removed pending
   VERONA results?

3. **Block C — TKI selection matrix for CML 1L** (3-5 hours).
   REG-2GEN-TKI-CML bundles dasatinib / nilotinib / bosutinib as a single
   Indication-mapped option with a comorbidity matrix in the notes. Question:
   should these be split into 3 separate regimens with their own indications,
   or is the current compact form acceptable?

4. **Block D — IPSS-R vs IPSS-M default for MDS** (1-2 hours).
   IPSS-M (Bernard 2022) reclassifies ~46% of patients. Should we switch
   the default risk score to IPSS-M now, or wait for broader adoption
   in Ukraine?

5. **Block E — Ukraine access annotations** (2-3 hours).
   Many newer agents (luspatercept, momelotinib, fedratinib, bosutinib,
   ponatinib, asciminib, midostaurin) are NOT registered / NOT reimbursed
   in Ukraine. Verify whether reimbursement data in
   `regulatory_status.ukraine_registration` and `ukraine_availability` is current.

---

## Block A — APL time-critical / emergency positioning

| Entity | File | Question |
|--------|------|---------|
| DIS-APL | diseases/apl.yaml | Is classifying this as `archetype: molecularly_defined_emergency` correct? This is a new archetype in the KB. |
| RF-APL-EMERGENCY-DIC | redflags/rf_apl_emergency_dic.yaml | Trigger: fibrinogen <150, D-dimer elevated, plt <50, active_bleeding, dic_active. Is this complete? |
| RF-APL-TRANSFORMATION-PROGRESSION (differentiation syndrome) | redflags/rf_apl_transformation_progression.yaml | Trigger: fever + new dyspnea + weight gain. Is the weight_gain ≥5 kg cutoff correct? Renamed from RF-APL-DIFFERENTIATION-SYNDROME to satisfy 5-type matrix coverage. |
| RF-APL-HIGH-RISK-BIOLOGY | redflags/rf_apl_high_risk_biology.yaml | Sanz cutoff WBC >10. Does intermediate-risk (plt ≤40 + WBC ≤10) correctly map to the standard track? |
| IND-APL-1L-ATRA-ATO | indications/ind_apl_1l_atra_ato.yaml | `time_critical: true`. ATRA initiation at the bedside is out of scope; do the notes correctly describe this? |
| IND-APL-1L-ATRA-ATO-IDA | indications/ind_apl_1l_atra_ato_ida.yaml | `time_critical: true`. Cumulative anthracycline tracking — how exactly is this reflected in the render? |

---

## Block B — Off-label / emerging therapy selection

| Entity | File | Question |
|--------|------|---------|
| IND-MDS-HR-1L-VEN-AZA | indications/ind_mds_hr_1l_ven_aza.yaml | Off-label MDS-HR. Keep as an alternative track or remove until VERONA results? |
| RF-AML-FLT3-ACTIONABLE | redflags/rf_aml_flt3_actionable.yaml | Midostaurin not Ukraine-reimbursed. Is there a practical alternative (gilteritinib is also not reimbursed)? |
| REG-VEN-AZA-AML | regimens/ven_aza_aml.yaml | Venetoclax not reimbursed in Ukraine. Should an access annotation be added to the render? |

---

## Block C — CML TKI selection bundle

| Entity | File | Question |
|--------|------|---------|
| REG-2GEN-TKI-CML | regimens/dasatinib_or_nilotinib_cml.yaml | Bundled dasatinib/nilotinib/bosutinib with comorbidity matrix in notes. Split or keep compact? |
| RF-CML-ORGAN-DYSFUNCTION | redflags/rf_cml_organ_dysfunction.yaml | Direction "investigate" — surfaces TKI-comorbidity matching annotation. Is this the correct semantics? |
| RF-CML-T315I-MUTATION | redflags/rf_cml_t315i_mutation.yaml | Ponatinib + asciminib NOT available in Ukraine. Is alloHCT a realistic alternative for T315I in our context? |

---

## Block D — Risk-score scoring system selection

| Entity | File | Question |
|--------|------|---------|
| RF-MDS-HIGH-RISK-IPSS | redflags/rf_mds_high_risk_ipss.yaml | Triggers on both IPSS-R AND IPSS-M. Should IPSS-M be made the primary now? |
| DIS-MDS-LR / DIS-MDS-HR | diseases/mds_lr.yaml, mds_hr.yaml | Risk cutoff IPSS-R ≤3.5 vs >4.5 — where should the intermediate range (3.5-4.5) be classified? |
| RF-PMF-HIGH-RISK-DIPSS | redflags/rf_pmf_high_risk_dipss.yaml | DIPSS-Plus vs MIPSS70. Should we wait for broader adoption of MIPSS70-plus v2.0? |
| RF-CML-HIGH-RISK-ELTS | redflags/rf_cml_high_risk_elts.yaml | ELTS superiority over Sokal — confirmed. Should Sokal be dropped from scoring? |

---

## Block E — Ukraine access / reimbursement audit

Verify the NSZU list (as of 2026-Q2) for:
- DRUG-VENETOCLAX (not reimbursed; confirm)
- DRUG-MIDOSTAURIN (not reimbursed)
- DRUG-LUSPATERCEPT (not registered)
- DRUG-MOMELOTINIB (not registered)
- DRUG-FEDRATINIB (not registered)
- DRUG-BOSUTINIB (not registered)
- DRUG-PONATINIB (not registered)
- DRUG-RUXOLITINIB (registered, not reimbursed)
- DRUG-ANAGRELIDE (registered, not reimbursed)
- DRUG-DECITABINE (reimbursed)
- DRUG-AZACITIDINE (reimbursed)
- DRUG-IMATINIB (reimbursed; generics)
- DRUG-DASATINIB / NILOTINIB (reimbursed)
- DRUG-EPOETIN-ALFA (reimbursed)
- DRUG-HYDROXYUREA (reimbursed)
- DRUG-ATRA / DRUG-ATO / DRUG-DAUNORUBICIN / DRUG-IDARUBICIN / DRUG-CYTARABINE (reimbursed)

---

## Acceptance criteria for promoting from STUB to published

For each of the 7 diseases + associated RF / Indication / Regimen / Algorithm:
- [ ] Technical: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns 0 errors (already done)
- [ ] Technical: `pytest -q` returns 0 regressions (already done)
- [ ] Clinical: clinical co-lead performs per-RF, per-Indication, per-Regimen review
- [ ] Clinical: ≥2 reviewer sign-offs on Indications (CHARTER §6.1)
- [ ] Content: remove `STUB — requires clinical co-lead signoff before publication` from `notes`
- [ ] Content: update `last_reviewed` to the date of clinical review + `reviewers` with real IDs

---

## Total estimate

~30-50 hours of clinical review (5 blocks × 4-10 hours each).
Highest ROI — Block A (APL emergency framing) and Block E (Ukraine access).
