# Triage Queue: rec-wording-audit-claim-bearing

**Filter:** severity = `critical`

**Total findings in queue:** 229

Walk through each finding. Read the current value (fetched from entity file), the contributor's suggestion (often a meta-description, not a literal replacement), and decide: edit the field with appropriate rewording, dismiss as false positive, or escalate.

---

## 1/229: f-0005 - CRITICAL

**Entity:** `BMA-ATM-GERMLINE-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_germline_pdac.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
ATM germline pathogenic confers ~5-10× pancreatic-cancer risk; PARPi activity in ATM-mutated PDAC is modest (POLO germline-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or trial-only. ESCAT IIA / OncoKB Level 3A.
```

**Excerpt context:**
```
...risk; PARPi activity in ATM-mutated PDAC is modest (POLO germline-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or trial-only. ESCAT IIA / OncoKB Level 3A.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 2/229: f-0006 - CRITICAL

**Entity:** `BMA-ATM-GERMLINE-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_germline_pdac.yaml`
**Field:** `evidence_summary_ua`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
ATM герміногенний патогенний confers ~5-10× pancreatic-рак risk; PARPi activity in ATM-mutated PDAC is modest (POLO герміногенний-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or дослідження-only. ESCAT IIA / OncoKB рівень 3A.
```

**Excerpt context:**
```
...PARPi activity in ATM-mutated PDAC is modest (POLO герміногенний-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or дослідження-only. ESCAT IIA / OncoKB рівень 3A.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 3/229: f-0007 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline ATM testing recommended.
```

**Excerpt context:**
```
Reflex germline ATM testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 4/229: f-0008 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_pdac.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 5/229: f-0009 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended (~10-15% of tumor ATM in prostate are germline).
```

**Excerpt context:**
```
Reflex germline testing recommended (~10-15% of tumor ATM in prostate are germline).
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 6/229: f-0010 - CRITICAL

**Entity:** `BMA-BARD1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Excerpt context:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 7/229: f-0011 - CRITICAL

**Entity:** `BMA-BARD1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 8/229: f-0012 - CRITICAL

**Entity:** `BMA-BARD1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 9/229: f-0022 - CRITICAL

**Entity:** `BMA-BRAF-V600E-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_gbm.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IIIA. OncoKB Level 2 (tissue-agnostic). Reflex BRAF V600E testing recommended for epithelioid GBM and pediatric/AYA HGG. Distinct from low-grade pediatric glioma where BRAFi has stronger evidence.
```

**Excerpt context:**
```
'ESCAT IIIA. OncoKB Level 2 (tissue-agnostic). Reflex BRAF V600E testing recommended
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 10/229: f-0024 - CRITICAL

**Entity:** `BMA-BRCA1-GERMLINE-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_germline_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
Germline mandates cascade testing (Lynch-like family-line implications, plus elevated breast/ovarian risk in carrier relatives). NCCN strongly recommends germline testing in all metastatic prostate cancer.
```

**Excerpt context:**
```
...mily-line implications, plus elevated breast/ovarian risk in carrier relatives). NCCN strongly recommends germline testing in all metastatic prostate cancer.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 11/229: f-0025 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Off-label PARPi use; reflex germline testing recommended. Distinguish BRCA1 promoter methylation (epigenetic, also actionable) from somatic mutation.
```

**Excerpt context:**
```
Off-label PARPi use; reflex germline testing recommended. Distinguish BRCA1 promoter methylation (epigenetic, also actionable) from somatic mutation.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 12/229: f-0026 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic-only finding does NOT trigger cascade family testing. Tumor NGS reveals; reflex germline testing recommended to clarify. Same drug menu as germline.
```

**Excerpt context:**
```
...ly finding does NOT trigger cascade family testing. Tumor NGS reveals; reflex germline testing recommended to clarify. Same drug menu as germline.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 13/229: f-0027 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_pdac.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended. Somatic-only not labeled for olaparib maintenance in PDAC.
```

**Excerpt context:**
```
Reflex germline testing recommended. Somatic-only not labeled for olaparib maintenance in PDAC.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 14/229: f-0028 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic-only does not mandate cascade testing but reflex germline confirmation strongly recommended (~50% of tumor-detected BRCA in prostate are germline).
```

**Excerpt context:**
```
Somatic-only does not mandate cascade testing but reflex germline confirmation strongly recommended (~50% of tumor-detected BRCA in prostate are germline).

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 15/229: f-0029 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_melanoma.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Germline finding triggers cascade testing — relatives face breast, ovarian, prostate, pancreatic risk regardless of melanoma. Enhanced dermatologic surveillance recommended.
```

**Excerpt context:**
```
...ovarian, prostate, pancreatic risk regardless of melanoma. Enhanced dermatologic surveillance recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 16/229: f-0030 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 17/229: f-0031 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_melanoma.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended; somatic-only is biologically interesting but not clinically actionable in melanoma.
```

**Excerpt context:**
```
Reflex germline testing recommended; somatic-only is biologically interesting but not clinically actionable in melanoma.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 18/229: f-0032 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended; ~30% of tumor-detected BRCA in EOC are germline.
```

**Excerpt context:**
```
Reflex germline testing recommended; ~30% of tumor-detected BRCA in EOC are germline.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 19/229: f-0033 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_pdac.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 20/229: f-0034 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 21/229: f-0035 - CRITICAL

**Entity:** `BMA-BRIP1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_germline_breast.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
BRIP1 germline pathogenic and breast cancer: weak/uncertain risk association (NCCN does not currently recommend enhanced breast surveillance based on BRIP1 alone). No PARPi indication. ESCAT IIIA / OncoKB Level 3B.
```

**Excerpt context:**
```
...ermline pathogenic and breast cancer: weak/uncertain risk association (NCCN does not currently recommend enhanced breast surveillance based on BRIP1 alone). No PARPi indication. ESCAT IIIA / OncoKB L...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 22/229: f-0036 - CRITICAL

**Entity:** `BMA-BRIP1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Matched pattern:** `recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
BRIP1 герміногенний патогенний and рак молочної залози: weak/uncertain risk association (NCCN does not currently recommend enhanced breast спостереження based on BRIP1 alone). ні PARPi показання. ESCAT IIIA / OncoKB рівень 3B.
```

**Excerpt context:**
```
...й патогенний and рак молочної залози: weak/uncertain risk association (NCCN does not currently recommend enhanced breast спостереження based on BRIP1 alone). ні PARPi показання. ESCAT IIIA / OncoKB р...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 23/229: f-0037 - CRITICAL

**Entity:** `BMA-BRIP1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended (ovarian implication for relatives).
```

**Excerpt context:**
```
Reflex germline testing recommended (ovarian implication for relatives).
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 24/229: f-0038 - CRITICAL

**Entity:** `BMA-BRIP1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 25/229: f-0040 - CRITICAL

**Entity:** `BMA-CCND1-T1114-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ccnd1_t1114_mm.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IIA. OncoKB Level 3A. FISH t(11;14) reflex testing should be standard at MM workup. NCCN listed as preferred R/R option in t(11;14)+ patients.
```

**Excerpt context:**
```
ESCAT IIA. OncoKB Level 3A. FISH t(11;14) reflex testing should be standard at MM workup. NCCN listed as preferred R/R option in t(11;14)+ patients.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 26/229: f-0045 - CRITICAL

**Entity:** `BMA-CHEK2-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing per NCCN. CHEK2 c.1100delC (Eastern European founder) is the most common pathogenic variant. Bilateral mastectomy not routinely recommended (risk lower than BRCA).
```

**Excerpt context:**
```
...rn European founder) is the most common pathogenic variant. Bilateral mastectomy not routinely recommended (risk lower than BRCA).

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 27/229: f-0046 - CRITICAL

**Entity:** `BMA-CHEK2-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 28/229: f-0047 - CRITICAL

**Entity:** `BMA-CHEK2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 29/229: f-0058 - CRITICAL

**Entity:** `BMA-FGFR2-FUSION-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_fusion_cholangio.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA. OncoKB Level 1. 1L remains gemcitabine + cisplatin ± durvalumab (TOPAZ-1). FGFR2-fusion testing recommended at diagnosis by NCCN to plan 2L. Detection: RNA-NGS preferred (intronic breakpoints commonly missed by DNA panels). Resistance: gatekeeper V564F, molecular brake L617M, kinase-domain N549K — futibatinib retains activity vs many of these. Source-gap: SRC-NCCN-HEPATOBILIARY / SRC-FIGHT-202 / SRC-FOENIX-CCA2 not yet ingested.
```

**Excerpt context:**
```
...ncoKB Level 1. 1L remains gemcitabine + cisplatin ± durvalumab (TOPAZ-1). FGFR2-fusion testing recommended at diagnosis by NCCN to plan 2L. Detection: RNA-NGS preferred (intronic breakpoints commonly m...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 30/229: f-0063 - CRITICAL

**Entity:** `BMA-HER2-AMP-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_crc.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HER2-amplified metastatic colorectal cancer (~3-5% in RAS/BRAF-WT population): tucatinib + trastuzumab is FDA-approved 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Strickler Lancet Oncol 2023 — ORR 38%, mDOR 12 mo) per SRC-NCCN-COLON-2025. Trastuzumab deruxtecan also has activity (DESTINY-CRC01 Siena Lancet Oncol 2021 — ORR 45% in HER2 IHC 3+ RAS-WT) and tumor-agnostic FDA approval (2024) for HER2-positive solid tumors that have progressed on prior therapy. Older trastuzumab + lapatinib (HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed therapy in 2L because RAS-driven resistance is well-documented per SRC-NCCN-COLON-2025.
```

**Excerpt context:**
```
...rapy. Older trastuzumab + lapatinib (HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed therapy in 2L because RAS-driven resistance is well-documented per S...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 31/229: f-0064 - CRITICAL

**Entity:** `BMA-HER2-AMP-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_crc.yaml`
**Field:** `evidence_summary_ua`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HER2-amplified метастатичний колоректальний рак (~3-5% in RAS/BRAF-WT population): тукатиніб + трастузумаб is схвалений FDA 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Strickler Lancet Oncol 2023 — ORR 38%, mDOR 12 міс.) per SRC-NCCN-COLON-2025. трастузумаб дерукстекан also has activity (DESTINY-CRC01 Siena Lancet Oncol 2021 — ORR 45% in HER2 IHC 3+ RAS-WT) and пухлина-agnostic FDA схвалення (2024) for HER2-positive solid tumors that have progressed on prior терапія. Older трастузумаб + лапатиніб (HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed терапія in 2L because RAS-driven resistance is well-documented per SRC-NCCN-COLON-2025.
```

**Excerpt context:**
```
...апія. Older трастузумаб + лапатиніб (HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed терапія in 2L because RAS-driven resistance is well-documented per S...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 32/229: f-0065 - CRITICAL

**Entity:** `BMA-HER2-AMP-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_crc.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IB / OncoKB Level 2 (initially Level 2A in CRC pre-MOUNTAINEER; Level 1 tumor-agnostic for T-DXd 2024). HER2 testing recommended for metastatic CRC with RAS/BRAF-WT genotype per SRC-NCCN-COLON-2025. RAS mutation = exclusion criterion for anti-HER2 therapy. Source-gap: SRC-MOUNTAINEER-STRICKLER-2023, SRC-DESTINY-CRC01, SRC-HERACLES not yet ingested.
```

**Excerpt context:**
```
...nitially Level 2A in CRC pre-MOUNTAINEER; Level 1 tumor-agnostic for T-DXd 2024). HER2 testing recommended for metastatic CRC with RAS/BRAF-WT genotype per SRC-NCCN-COLON-2025. RAS mutation = exclusion...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 33/229: f-0067 - CRITICAL

**Entity:** `BMA-HER2-AMP-ESOPHAGEAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_esophageal.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA / OncoKB Level 1. HER2 testing for adenocarcinoma histology only (not squamous). Heterogeneity high — ≥4 biopsies recommended. Source-gap: SRC-TOGA-BANG-2010, SRC-KEYNOTE-811, SRC-DESTINY-GASTRIC01 not ingested.
```

**Excerpt context:**
```
...ER2 testing for adenocarcinoma histology only (not squamous). Heterogeneity high — ≥4 biopsies recommended. Source-gap: SRC-TOGA-BANG-2010, SRC-KEYNOTE-811, SRC-DESTINY-GASTRIC01 not ingested.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 34/229: f-0069 - CRITICAL

**Entity:** `BMA-HER2-AMP-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_gastric.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA / OncoKB Level 1. Gastric HER2 scoring (Hofmann 2008) differs from breast: basolateral/lateral membranous staining ≥10% qualifies (cf. circumferential criterion in breast). HER2 testing recommended for all metastatic gastric/GEJ adenocarcinoma at diagnosis. Heterogeneity is significant: ≥4 endoscopic biopsies preferred. Source-gap: SRC-TOGA-BANG-2010, SRC-DESTINY-GASTRIC01, SRC-KEYNOTE-811 not yet ingested.
```

**Excerpt context:**
```
...ral membranous staining ≥10% qualifies (cf. circumferential criterion in breast). HER2 testing recommended for all metastatic gastric/GEJ adenocarcinoma at diagnosis. Heterogeneity is significant: ≥4 e...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 35/229: f-0073 - CRITICAL

**Entity:** `BMA-HRD-STATUS-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_pdac.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA / OncoKB Level 1 (gBRCAm). Somatic BRCA in PDAC has less evidence; PALB2 inclusion in NCCN PARP indication is conditional / Level 2A. Germline testing recommended for ALL pancreatic cancer at diagnosis per NCCN. POLO did not show OS benefit, but PFS improvement with low maintenance toxicity supports use. Source-gap: SRC-POLO-GOLAN-2019 not yet ingested.
```

**Excerpt context:**
```
...evidence; PALB2 inclusion in NCCN PARP indication is conditional / Level 2A. Germline testing recommended for ALL pancreatic cancer at diagnosis per NCCN. POLO did not show OS benefit, but PFS improve...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 36/229: f-0074 - CRITICAL

**Entity:** `BMA-HRD-STATUS-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA / OncoKB Level 1 (BRCA1/2 strongest evidence; other HRR genes Level 1 by FDA label inclusion but heterogeneous evidence — ATM benefit weakest in PROfound subgroup analysis). EAU 2024 more conservative than NCCN on non-BRCA HRR PARP indications — documented position difference. Both germline and somatic testing recommended at metastatic diagnosis. Source-gap: SRC-PROFOUND, SRC-MAGNITUDE, SRC-PROPEL, SRC-TALAPRO2 not yet ingested.
```

**Excerpt context:**
```
...-BRCA HRR PARP indications — documented position difference. Both germline and somatic testing recommended at metastatic diagnosis. Source-gap: SRC-PROFOUND, SRC-MAGNITUDE, SRC-PROPEL, SRC-TALAPRO2 not...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 37/229: f-0075 - CRITICAL

**Entity:** `BMA-IDH1-R132-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132_cholangio.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
IDH1 R132 hotspot mutations occur in ~13-20% of intrahepatic cholangiocarcinoma and are FDA Level-1 actionable. Ivosidenib was FDA-approved 2021 for previously-treated IDH1-mutated locally advanced/metastatic cholangiocarcinoma based on ClarIDHy (Abou-Alfa Lancet Oncol 2020 — mPFS 2.7 vs 1.4 mo, HR 0.37; OS benefit on rank-preserving structural failure time analysis adjusted for crossover) per SRC-NCCN-HEPATOBILIARY. Comprehensive molecular profiling at diagnosis is recommended to identify IDH1-R132 patients who can be sequenced to ivosidenib in 2L after gemcitabine/cisplatin ± durvalumab (TOPAZ-1) 1L.
```

**Excerpt context:**
```
...d for crossover) per SRC-NCCN-HEPATOBILIARY. Comprehensive molecular profiling at diagnosis is recommended to identify IDH1-R132 patients who can be sequenced to ivosidenib in 2L after gemcitabine/cisp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 38/229: f-0076 - CRITICAL

**Entity:** `BMA-IDH1-R132-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132_cholangio.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA / OncoKB Level 1. IDH1 mutations are mutually exclusive with FGFR2 fusions in cholangiocarcinoma; molecular profiling should cover both. Ivosidenib also has on-label use in IDH1-mutated AML (see existing BMAs). Resistance mechanisms: IDH2 isoform switching, receptor tyrosine kinase upregulation. Source-gap: SRC-NCCN-HEPATOBILIARY STUB; SRC-CLARIDHY-ABOU-ALFA-2020 not yet ingested.
```

**Excerpt context:**
```
...mutations are mutually exclusive with FGFR2 fusions in cholangiocarcinoma; molecular profiling should cover both. Ivosidenib also has on-label use in IDH1-mutated AML (see existing BMAs). Resistan...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 39/229: f-0078 - CRITICAL

**Entity:** `BMA-IGHV-UNMUTATED-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ighv_unmutated_cll.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
IGHV mutational status is a fundamental CLL risk stratifier and treatment-selection biomarker per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has shorter response to chemoimmunotherapy (CIT — FCR, BR) and is now a strong indication for continuous BTK inhibitor (ibrutinib, acalabrutinib, zanubrutinib) or fixed-duration venetoclax-obinutuzumab as 1L regardless of TP53 status. CLL14 (Fischer NEJM 2019 — venetoclax + obinutuzumab fixed-duration vs chlorambucil + obinutuzumab) and ECOG E1912 (Shanafelt NEJM 2019 — ibrutinib + rituximab vs FCR) are foundational trials that demonstrated CIT inferiority specifically in IGHV- unmutated subgroups. ESMO 2024 explicitly recommends against FCR/BR 1L in IGHV-unmutated patients.
```

**Excerpt context:**
```
...t demonstrated CIT inferiority specifically in IGHV- unmutated subgroups. ESMO 2024 explicitly recommends against FCR/BR 1L in IGHV-unmutated patients.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 40/229: f-0079 - CRITICAL

**Entity:** `BMA-IGHV-UNMUTATED-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ighv_unmutated_cll.yaml`
**Field:** `evidence_summary_ua`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
IGHV mutational status is a fundamental CLL risk stratifier and лікування-selection біомаркер per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has shorter відповідь to хіміоімунотерапія (CIT — FCR, BR) and is now a strong показання for continuous BTK інгібітор (ібрутиніб, акалабрутиніб, занубрутиніб) or fixed-duration венетоклакс-обінутузумаб as 1L regardless of TP53 status. CLL14 (Fischer NEJM 2019 — венетоклакс + обінутузумаб fixed-duration vs chlorambucil + обінутузумаб) and ECOG E1912 (Shanafelt NEJM 2019 — ібрутиніб + ритуксимаб vs FCR) are foundational trials that продемонстровано CIT inferiority зокрема in IGHV- unmutated subgroups. ESMO 2024 explicitly recommends against FCR/BR 1L in IGHV-unmutated patients.
```

**Excerpt context:**
```
...at продемонстровано CIT inferiority зокрема in IGHV- unmutated subgroups. ESMO 2024 explicitly recommends against FCR/BR 1L in IGHV-unmutated patients.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 41/229: f-0086 - CRITICAL

**Entity:** `BMA-KIT-EXON9-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_exon9_gist.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IB. OncoKB Level 1. Source-gap as DIS-GIST. Adjuvant strategy in high-risk resected exon-9 GIST less established — extended- duration imatinib often considered. Exon 9 GIST predominantly small-bowel primary; extra-gastric origin should prompt KIT exon 9 testing if not already done.
```

**Excerpt context:**
```
...imatinib often considered. Exon 9 GIST predominantly small-bowel primary; extra-gastric origin should prompt KIT exon 9 testing if not already done.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 42/229: f-0087 - CRITICAL

**Entity:** `BMA-KIT-MUTATION-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_mutation_aml.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IIA. OncoKB Level 3A. KIT testing should be performed on every CBF-AML at diagnosis; result modifies prognosis and trial eligibility but does not yet change standard-of-care chemo backbone outside trials. Trial-source gap: SRC-CALGB-10801 not yet ingested.
```

**Excerpt context:**
```
ESCAT IIA. OncoKB Level 3A. KIT testing should be performed on every CBF-AML at diagnosis; result modifies prognosis and trial eligibility bu...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 43/229: f-0088 - CRITICAL

**Entity:** `BMA-KIT-MUTATION-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_mutation_melanoma.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IB. OncoKB Level 2. Trial-source gap: SRC-CARVAJAL-KIT-MELANOMA-2013 / SRC-HODI-2013 not yet ingested. KIT-mutant melanoma is also a scenario where dabrafenib/trametinib does NOT apply (BRAF V600 testing should be parallel).
```

**Excerpt context:**
```
...tant melanoma is also a scenario where dabrafenib/trametinib does NOT apply (BRAF V600 testing should be parallel).

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 44/229: f-0097 - CRITICAL

**Entity:** `BMA-MGMT-METHYLATION-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mgmt_methylation_gbm.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA / OncoKB Level 2 (predictive biomarker; not a target). MGMT testing recommended for ALL newly-diagnosed GBM; methodology = MS-PCR or pyrosequencing; mosaic / weakly-methylated intermediate cases remain therapeutically ambiguous. In MGMT-unmethylated GBM, the benefit of TMZ is small but Stupp remains standard outside of trials per SRC-EANO-GBM-2024 — see notes on contradictions: NCCN does not withhold TMZ from unmethylated patients while EANO 2024 explicitly considers RT-alone an acceptable alternative for unmethylated elderly. This represents a documented evidence-based disagreement between guidelines — flagged for clinical-co-lead review. Source-gap: SRC-STUPP-NEJM-2005, SRC-PERRY-NEJM-2017, SRC-CETEG-NOA09 not ingested.
```

**Excerpt context:**
```
ESCAT IA / OncoKB Level 2 (predictive biomarker; not a target). MGMT testing recommended for ALL newly-diagnosed GBM; methodology = MS-PCR or pyrosequencing; mosaic / weakly-methylate...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 45/229: f-0099 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_crc.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 46/229: f-0100 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_endometrial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 47/229: f-0101 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_gastric.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 48/229: f-0102 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 49/229: f-0104 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 50/229: f-0105 - CRITICAL

**Entity:** `BMA-MLH1-SOMATIC-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_urothelial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MLH1 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 51/229: f-0107 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_crc.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 52/229: f-0108 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_endometrial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 53/229: f-0109 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_gastric.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 54/229: f-0110 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 55/229: f-0112 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 56/229: f-0113 - CRITICAL

**Entity:** `BMA-MSH2-SOMATIC-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_urothelial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 57/229: f-0115 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_crc.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 58/229: f-0116 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_endometrial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 59/229: f-0117 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_gastric.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 60/229: f-0118 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 61/229: f-0120 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 62/229: f-0121 - CRITICAL

**Entity:** `BMA-MSH6-SOMATIC-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_urothelial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic MSH6 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 63/229: f-0124 - CRITICAL

**Entity:** `BMA-MYC-REARRANGEMENT-HGBL-DH`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_myc_rearrangement_hgbl_dh.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IIA. CNS prophylaxis recommended. MYC-only rearrangement (single-hit) treated as DLBCL-NOS.
```

**Excerpt context:**
```
ESCAT IIA. CNS prophylaxis recommended. MYC-only rearrangement (single-hit) treated as DLBCL-NOS.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 64/229: f-0125 - CRITICAL

**Entity:** `BMA-MYD88-L265P-WM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_myd88_l265p_wm.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA. OncoKB Level 1. CXCR4 WHIM-like mutation testing recommended as it modulates BTKi response. MYD88-WT WM (~10%) responds less well to BTKi.
```

**Excerpt context:**
```
'ESCAT IA. OncoKB Level 1. CXCR4 WHIM-like mutation testing recommended as
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 65/229: f-0132 - CRITICAL

**Entity:** `BMA-NTRK-FUSION-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ntrk_fusion_gist.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. OncoKB Level 1. NTRK-fusion screening in GIST should be reserved for KIT/PDGFRA-WT cases (after SDHB IHC to exclude SDH-deficient GIST). Source-gap: SRC-NCCN-SARCOMA / SRC-NCCN-GIST-2025 not yet ingested.
```

**Excerpt context:**
```
ESCAT IA. OncoKB Level 1. NTRK-fusion screening in GIST should be reserved for KIT/PDGFRA-WT cases (after SDHB IHC to exclude SDH-deficient GIST). Source-gap...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 66/229: f-0135 - CRITICAL

**Entity:** `BMA-PALB2-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_palb2_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing mandatory. PALB2 carriers also face elevated pancreatic and ovarian risk — enhanced surveillance recommended.
```

**Excerpt context:**
```
...ndatory. PALB2 carriers also face elevated pancreatic and ovarian risk — enhanced surveillance recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 67/229: f-0136 - CRITICAL

**Entity:** `BMA-PALB2-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_palb2_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 68/229: f-0137 - CRITICAL

**Entity:** `BMA-PALB2-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_palb2_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 69/229: f-0138 - CRITICAL

**Entity:** `BMA-PALB2-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_palb2_somatic_pdac.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 70/229: f-0139 - CRITICAL

**Entity:** `BMA-PDGFRA-D842V-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pdgfra_d842v_gist.yaml`
**Field:** `notes`
**Matched pattern:** `patients should`
**Pattern class:** patient-directed imperative

**Current value:**
```
ESCAT IA. OncoKB Level 1. Source-gap: SRC-NCCN-SARCOMA / SRC-NCCN-GIST-2025 / SRC-NAVIGATOR / SRC-VOYAGER not yet ingested. CNS toxicity (cognitive effects, intracranial hemorrhage) is on-target / dose- related — dose modifications standard. Companion-diagnostic genotyping via NGS panel mandatory before avapritinib initiation. Adjuvant imatinib has NO benefit in D842V GIST — these patients should be observed post-resection.
```

**Excerpt context:**
```
...andatory before avapritinib initiation. Adjuvant imatinib has NO benefit in D842V GIST — these patients should be observed post-resection.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 71/229: f-0140 - CRITICAL

**Entity:** `BMA-PDGFRA-D842V-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pdgfra_d842v_gist.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. OncoKB Level 1. Source-gap: SRC-NCCN-SARCOMA / SRC-NCCN-GIST-2025 / SRC-NAVIGATOR / SRC-VOYAGER not yet ingested. CNS toxicity (cognitive effects, intracranial hemorrhage) is on-target / dose- related — dose modifications standard. Companion-diagnostic genotyping via NGS panel mandatory before avapritinib initiation. Adjuvant imatinib has NO benefit in D842V GIST — these patients should be observed post-resection.
```

**Excerpt context:**
```
...before avapritinib initiation. Adjuvant imatinib has NO benefit in D842V GIST — these patients should be observed post-resection.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 72/229: f-0143 - CRITICAL

**Entity:** `BMA-PIK3CA-HOTSPOT-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pik3ca_hotspot_endometrial.yaml`
**Field:** `evidence_summary`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
PIK3CA mutations occur in ~30-50% of endometrioid endometrial cancers, often co-occurring with PTEN loss. PI3Ki/AKTi/mTORi monotherapy modest activity (everolimus + letrozole recommended). Tissue-agnostic capivasertib not formally approved in endometrial.
```

**Excerpt context:**
```
...occurring with PTEN loss. PI3Ki/AKTi/mTORi monotherapy modest activity (everolimus + letrozole recommended). Tissue-agnostic capivasertib not formally approved in endometrial.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 73/229: f-0145 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_crc.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 74/229: f-0146 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_endometrial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 75/229: f-0147 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_gastric.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 76/229: f-0148 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 77/229: f-0150 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_prostate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 78/229: f-0151 - CRITICAL

**Entity:** `BMA-PMS2-SOMATIC-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_urothelial.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-specific lines.
```

**Excerpt context:**
```
Somatic PMS2 loss → cascade testing optional (reflex germline confirmation strongly recommended; ~30% of dMMR tumors have germline cause). Pan-tumor MSI-H ICI eligibility supersedes tumor-sp...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 79/229: f-0152 - CRITICAL

**Entity:** `BMA-RAD51B-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51b_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Excerpt context:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 80/229: f-0153 - CRITICAL

**Entity:** `BMA-RAD51B-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51b_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 81/229: f-0154 - CRITICAL

**Entity:** `BMA-RAD51B-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51b_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 82/229: f-0155 - CRITICAL

**Entity:** `BMA-RAD51C-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51c_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Excerpt context:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 83/229: f-0156 - CRITICAL

**Entity:** `BMA-RAD51C-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51c_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 84/229: f-0157 - CRITICAL

**Entity:** `BMA-RAD51C-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51c_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 85/229: f-0158 - CRITICAL

**Entity:** `BMA-RAD51D-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51d_germline_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Excerpt context:**
```
Cascade testing per NCCN. Enhanced screening recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 86/229: f-0159 - CRITICAL

**Entity:** `BMA-RAD51D-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51d_somatic_breast.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 87/229: f-0160 - CRITICAL

**Entity:** `BMA-RAD51D-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_rad51d_somatic_ovarian.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Reflex germline testing recommended.
```

**Excerpt context:**
```
Reflex germline testing recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 88/229: f-0196 - CRITICAL

**Entity:** `IND-AML-1L-QUIZARTINIB-FLT3ITD`
**File:** `knowledge_base/hosted/content/indications/ind_aml_1l_quizartinib_flt3itd.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Quizartinib + standard 7+3 induction + HiDAC consolidation + 3-year maintenance for newly-dx FLT3-ITD+ AML age 18-75. Pivotal QuANTUM-First (Erba et al., Lancet 2023) phase-3 RCT: median OS 31.9 vs 15.1 mo (HR 0.78, p=0.032) vs placebo+chemo. Approved FDA July 2023. Quizartinib is Type-II FLT3 inhibitor — covers FLT3-ITD ONLY, NOT FLT3-TKD (D835/I836); for FLT3-TKD or combined ITD+TKD, midostaurin (RATIFY) remains the option. QTc prolongation requires ACTIVE management: baseline + serial ECG, K+ ≥4.0 / Mg++ ≥2.0 BEFORE initiation, AVOID concomitant QT-prolonging drugs, dose-reduce 50% with strong CYP3A4 inhibitors (azoles). AlloHCT in CR1 still recommended for high FLT3-allelic-burden / NPM1-wild-type per ELN 2022. Ukraine: not registered, major access barrier.
```

**Excerpt context:**
```
...prolonging drugs, dose-reduce 50% with strong CYP3A4 inhibitors (azoles). AlloHCT in CR1 still recommended for high FLT3-allelic-burden / NPM1-wild-type per ELN 2022. Ukraine: not registered, major acc...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 89/229: f-0200 - CRITICAL

**Entity:** `IND-AML-CR1-ORAL-AZA-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_aml_cr1_oral_aza_maintenance.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Standard-track CR1 maintenance for AML patients ≥55 years not proceeding to alloHCT (the dominant scenario for older / unfit patients). QUAZAR AML-001 (Wei 2020): oral azacitidine 300 mg PO daily × 14 d / 28-d cycle vs placebo improved median OS (24.7 vs 14.8 mo; HR 0.69, p<0.001) and RFS (10.2 vs 4.8 mo; HR 0.65) — irrespective of post-induction consolidation status. FDA-approved Sep 2020 as Onureg. CRITICAL: only the oral CC-486 formulation (Onureg) qualifies; SC/IV azacitidine is NOT bioequivalent and must NOT be substituted for QUAZAR maintenance. UA access barrier: Onureg not registered in Ukraine — engine should flag funding pathway as required step before activating this indication.
```

**Excerpt context:**
```
...nly the oral CC-486 formulation (Onureg) qualifies; SC/IV azacitidine is NOT bioequivalent and must NOT be substituted for QUAZAR maintenance. UA access barrier: Onureg not registered in Ukraine...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 90/229: f-0201 - CRITICAL

**Entity:** `IND-AML-CR1-ORAL-AZA-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_aml_cr1_oral_aza_maintenance.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Standard-track CR1 maintenance for AML patients ≥55 years not proceeding to alloHCT (the dominant scenario for older / unfit patients). QUAZAR AML-001 (Wei 2020): oral azacitidine 300 mg PO daily × 14 d / 28-d cycle vs placebo improved median OS (24.7 vs 14.8 mo; HR 0.69, p<0.001) and RFS (10.2 vs 4.8 mo; HR 0.65) — irrespective of post-induction consolidation status. FDA-approved Sep 2020 as Onureg. CRITICAL: only the oral CC-486 formulation (Onureg) qualifies; SC/IV azacitidine is NOT bioequivalent and must NOT be substituted for QUAZAR maintenance. UA access barrier: Onureg not registered in Ukraine — engine should flag funding pathway as required step before activating this indication.
```

**Excerpt context:**
```
...bstituted for QUAZAR maintenance. UA access barrier: Onureg not registered in Ukraine — engine should flag funding pathway as required step before activating this indication.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 91/229: f-0203 - CRITICAL

**Entity:** `IND-AML-CR1-ORAL-AZA-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_aml_cr1_oral_aza_maintenance.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead signoff. Standard-track post-induction maintenance for AML CR1 in transplant-ineligible patients. line_of_therapy: 1 reflects continuation of the 1L pathway (analogous to MM lenalidomide maintenance pattern). Engine should activate after induction → CR/CRi → no-HCT decision branch. Ukraine access barrier dominant (Onureg not registered); engine must flag funding pathway.
```

**Excerpt context:**
```
...ects continuation of the 1L pathway (analogous to MM lenalidomide maintenance pattern). Engine should activate after induction → CR/CRi → no-HCT decision branch. Ukraine access barrier dominant (O...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 92/229: f-0204 - CRITICAL

**Entity:** `IND-AML-CR1-ORAL-AZA-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_aml_cr1_oral_aza_maintenance.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead signoff. Standard-track post-induction maintenance for AML CR1 in transplant-ineligible patients. line_of_therapy: 1 reflects continuation of the 1L pathway (analogous to MM lenalidomide maintenance pattern). Engine should activate after induction → CR/CRi → no-HCT decision branch. Ukraine access barrier dominant (Onureg not registered); engine must flag funding pathway.
```

**Excerpt context:**
```
.../CRi → no-HCT decision branch. Ukraine access barrier dominant (Onureg not registered); engine must flag funding pathway.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 93/229: f-0207 - CRITICAL

**Entity:** `IND-APL-1L-ATRA-ATO`
**File:** `knowledge_base/hosted/content/indications/ind_apl_1l_atra_ato.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
STANDARD track for low/intermediate-risk APL. time_critical: true reflects CHARTER §15.2 C2 — APL initial management is partially outside the non-device CDS carve-out (ATRA initiation must be at bedside within hours, not via this tool). OpenOnco scope: workup + plan AFTER initial stabilization. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...C2 — APL initial management is partially outside the non-device CDS carve-out (ATRA initiation must be at bedside within hours, not via this tool). OpenOnco scope: workup + plan AFTER initial st...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 94/229: f-0216 - CRITICAL

**Entity:** `IND-B-ALL-2L-INOTUZUMAB`
**File:** `knowledge_base/hosted/content/indications/ind_b_all_2l_inotuzumab.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead sign-off. Aggressive-track 2L+ for R/R Ph- B-ALL adult. Bridge-to-HCT intent dominant. Ukraine access barrier. Time-critical: relapse pathway must be confirmed within days.
```

**Excerpt context:**
```
...L adult. Bridge-to-HCT intent dominant. Ukraine access barrier. Time-critical: relapse pathway must be confirmed within days.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 95/229: f-0218 - CRITICAL

**Entity:** `IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_b_all_post_consolidation_pomp_maintenance.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Standard 2-3 yr POMP maintenance is the cornerstone tail of pediatric-inspired BFM-style B-ALL therapy and the dominant driver of cure in AYA + adult Ph-negative B-ALL. CALGB 10403 (Stock 2019, Blood) demonstrated 3-y EFS 59% and OS 73% in AYA 17-39 yr — substantially superior to historical adult-style protocols. Total treatment duration ~2 yr (women) — 3 yr (men) from start of interim maintenance. Components: 6-MP PO daily (titrate to mild myelosuppression) + MTX PO weekly + monthly vincristine + prednisone pulse. PJP prophylaxis mandatory throughout. TPMT/NUDT15 genotyping recommended pre-initiation to identify poor metabolizers requiring dramatic 6-MP reduction. For Ph+ B-ALL, POMP maintenance is given alongside continued TKI (imatinib/dasatinib/ponatinib) per institutional protocol.
```

**Excerpt context:**
```
...y vincristine + prednisone pulse. PJP prophylaxis mandatory throughout. TPMT/NUDT15 genotyping recommended pre-initiation to identify poor metabolizers requiring dramatic 6-MP reduction. For Ph+ B-ALL,...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 96/229: f-0219 - CRITICAL

**Entity:** `IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_b_all_post_consolidation_pomp_maintenance.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead signoff. Standard-track maintenance for B-ALL post-induction-consolidation. line_of_therapy: 1 reflects 1L pathway continuation (analogous to MM lenalidomide and AML QUAZAR patterns). Engine should activate after consolidation + interim maintenance + delayed intensification phases complete with confirmed CR. For Ph+ B-ALL, runs alongside continued TKI per institutional protocol.
```

**Excerpt context:**
```
...eflects 1L pathway continuation (analogous to MM lenalidomide and AML QUAZAR patterns). Engine should activate after consolidation + interim maintenance + delayed intensification phases complete w...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 97/229: f-0229 - CRITICAL

**Entity:** `IND-BREAST-HR-POS-2L-T-DXD-HER2-LOW`
**File:** `knowledge_base/hosted/content/indications/ind_breast_hr_pos_2l_t_dxd_her2_low.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. DESTINY-Breast04 transformed HER2-low (IHC 1+ or IHC 2+/ISH-) from a "negative" category into an actionable one for T-DXd. HR+ subset must have progressed on endocrine ± CDK4/6i and received ≥1 prior chemo line for metastatic disease (OR rapid progression making chemo immediately needed). ILD risk dominant safety concern (~12% any grade, 1.3% G3+ in DB-04) — baseline CT chest + active monitoring; immediate hold + corticosteroids if pneumonitis suspect. UA access barrier: T-DXd registered but reimbursement under negotiation; significant out-of-pocket cost. Sequencing question: T-DXd vs sequential targetable-mutation drugs (capivasertib/alpelisib/elacestrant when applicable) is unsettled — see ALGO-BREAST-HR-POS-2L for default ordering.
```

**Excerpt context:**
```
...IHC 1+ or IHC 2+/ISH-) from a "negative" category into an actionable one for T-DXd. HR+ subset must have progressed on endocrine ± CDK4/6i and received ≥1 prior chemo line for metastatic disease...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 98/229: f-0230 - CRITICAL

**Entity:** `IND-BREAST-HR-POS-3L-POST-CDK46I-POST-AKT`
**File:** `knowledge_base/hosted/content/indications/ind_breast_hr_pos_3l_post_cdk46i_post_akt.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
For HR+/HER2- mBC patients who have exhausted CDK4/6i + AI 1L AND PI3K/AKT pathway targeted endocrine therapy 2L (alpelisib + fulvestrant per SOLAR-1 OR capivasertib + fulvestrant per CAPItello-291), 3L options are limited and salvage in nature. Everolimus + exemestane (BOLERO-2 paradigm) is reasonable if not previously exhausted. Single-agent endocrine therapy (fulvestrant, exemestane, megestrol) is acceptable for indolent disease. Sacituzumab govitecan (TROPiCS-02 Rugo 2023 Lancet; mPFS 5.5 vs 4.0 mo) and trastuzumab deruxtecan (DESTINY-Breast06 for HER2-low; Bardia 2024 NEJM; mPFS 13.2 vs 8.1 mo) are now competitive 3L+ options with stronger evidence than empirical chemo. Preferred order at 3L+: ADC (sacituzumab or T-DXd if HER2-low) > everolimus + exemestane > sequential single-agent chemo (capecitabine, eribulin). ESR1 mutation testing recommended — elacestrant (EMERALD trial) approved for ESR1-mutant tumors. STUB regimen — multiple 3L+ options exist; treatment selection is highly individualized.
```

**Excerpt context:**
```
...s + exemestane > sequential single-agent chemo (capecitabine, eribulin). ESR1 mutation testing recommended — elacestrant (EMERALD trial) approved for ESR1-mutant tumors. STUB regimen — multiple 3L+ opt...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 99/229: f-0235 - CRITICAL

**Entity:** `IND-BREAST-TNBC-2L-BRCA-OLAPARIB`
**File:** `knowledge_base/hosted/content/indications/ind_breast_tnbc_2l_brca_olaparib.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. OlympiAD established olaparib for germline BRCA1/2-mutant HER2- metastatic breast (≤2 prior chemo lines for metastatic; HR+ subset must have ≥1 prior endocrine line). For TNBC subset olaparib is typically ≥2L (after 1L pembro + chemo for PD-L1+ or chemo alone for PD-L1-). Talazoparib (EMBRACA) is the alternative PARPi — comparable efficacy, more anaemia, less GI. Patient preference and AE-profile drive olaparib-vs-talazoparib choice. UA access: olaparib reimbursed for breast indication; talazoparib not yet reimbursed.
```

**Excerpt context:**
```
...rmline BRCA1/2-mutant HER2- metastatic breast (≤2 prior chemo lines for metastatic; HR+ subset must have ≥1 prior endocrine line). For TNBC subset olaparib is typically ≥2L (after 1L pembro + ch...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 100/229: f-0236 - CRITICAL

**Entity:** `IND-BREAST-TNBC-2L-BRCA-TALAZOPARIB`
**File:** `knowledge_base/hosted/content/indications/ind_breast_tnbc_2l_brca_talazoparib.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. EMBRACA established talazoparib (1 mg PO daily) for germline BRCA1/2-mutant HER2- metastatic breast (≤3 prior cytotoxic regimens). Comparable efficacy to olaparib (no head-to-head trial), different AE profile: more haematologic (anaemia G3+ ~39%), less GI than olaparib. Patient preference and AE-profile drive the olaparib-vs-talazoparib choice.
KNOWN GAP: dedicated REG-TALAZOPARIB-BREAST regimen entry not yet authored — current placeholder points to REG-OLAPARIB-BREAST. Engine trace must surface that talazoparib dosing differs (1 mg PO daily monotherapy continuous; reduce to 0.75 mg if anaemia, then 0.5 mg). Follow-up authoring task. UA access: talazoparib not reimbursed.
```

**Excerpt context:**
```
...gimen entry not yet authored — current placeholder points to REG-OLAPARIB-BREAST. Engine trace must surface that talazoparib dosing differs (1 mg PO daily monotherapy continuous; reduce to 0.75...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 101/229: f-0237 - CRITICAL

**Entity:** `IND-BREAST-TNBC-2L-SACITUZUMAB`
**File:** `knowledge_base/hosted/content/indications/ind_breast_tnbc_2l_sacituzumab.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ESCAT IA. ASCENT established sacituzumab govitecan (anti-Trop-2 ADC with SN-38 payload) as standard ≥2L for metastatic TNBC pretreated with ≥2 prior chemo lines (≥1 in metastatic). No biomarker gating — Trop-2 expression is universal in TNBC. Severe AE profile: neutropenia G3+ 51% (G-CSF primary prophylaxis recommended), diarrhea G3+ 10%. UGT1A1*28 homozygous patients require dose reduction. Default 2L for non-BRCA TNBC; default 3L for BRCA-mut TNBC after PARPi failure. UA access barrier: not registered; named-patient import / EAP / cross-border only.
```

**Excerpt context:**
```
...ession is universal in TNBC. Severe AE profile: neutropenia G3+ 51% (G-CSF primary prophylaxis recommended), diarrhea G3+ 10%. UGT1A1*28 homozygous patients require dose reduction. Default 2L for non-B...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 102/229: f-0238 - CRITICAL

**Entity:** `IND-BREAST-TNBC-2L-T-DXD-HER2-LOW`
**File:** `knowledge_base/hosted/content/indications/ind_breast_tnbc_2l_t_dxd_her2_low.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESCAT IA. DESTINY-Breast04 included a small TNBC HER2-low cohort (n=63) with consistent benefit signal — T-DXd should be preferred over sacituzumab when HER2-low confirmed (IHC 1+ or IHC 2+/ISH-). When HER2-IHC = 0, sacituzumab govitecan (ASCENT) is the default ≥2L. ILD risk dominant safety concern — baseline CT chest + active monitoring. UA access barrier: T-DXd registered but reimbursement under negotiation. Sequencing question (T-DXd then sacituzumab vs reverse) is unsettled; ALGO-BREAST-TNBC-2L defaults to T-DXd-first for HER2-low.
```

**Excerpt context:**
```
...Y-Breast04 included a small TNBC HER2-low cohort (n=63) with consistent benefit signal — T-DXd should be preferred over sacituzumab when HER2-low confirmed (IHC 1+ or IHC 2+/ISH-). When HER2-IHC =...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 103/229: f-0240 - CRITICAL

**Entity:** `IND-BREAST-TNBC-3L-POST-SACI-POST-T-DXD`
**File:** `knowledge_base/hosted/content/indications/ind_breast_tnbc_3l_post_saci_post_t_dxd.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Triple-negative breast cancer at 3L+ after exhaustion of pembrolizumab + chemo 1L (KEYNOTE-355 for CPS ≥10) and sacituzumab govitecan 2L (ASCENT) ± T-DXd if HER2-low (DESTINY-Breast06) is a salvage setting with limited evidence. Sequential single-agent chemotherapy (capecitabine, eribulin, vinorelbine, gemcitabine) is the mainstay; ORR ~10-20% per agent, mPFS 2-4 mo each, mOS from 3L initiation 6-12 mo. Platinum re-challenge (carboplatin) is reasonable if not previously exhausted, particularly for BRCA-mutated TNBC (TBCRC 030). Olaparib/talazoparib for germline BRCA-mutated TNBC if not previously used (OlympiAD, EMBRACA). Trial enrollment + best supportive care should be prioritized given limited efficacy of empirical chemo. Brain MRI at progression — TNBC has high CNS-relapse rate, may shift to whole-brain RT or capecitabine + tucatinib (off-label) for LMD.
```

**Excerpt context:**
```
...tated TNBC if not previously used (OlympiAD, EMBRACA). Trial enrollment + best supportive care should be prioritized given limited efficacy of empirical chemo. Brain MRI at progression — TNBC has...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 104/229: f-0261 - CRITICAL

**Entity:** `IND-CLL-1L-ZANUBRUTINIB`
**File:** `knowledge_base/hosted/content/indications/ind_cll_1l_zanubrutinib.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Co-Lead sign-off. Standard track for CLL 1L — alternative to existing IND-CLL-1L-BTKI (acalabrutinib). Both second-generation BTKis preferred over ibrutinib. Engine should treat both as interchangeable Cat 1 preferred options based on access. UA reimbursement gap: ibrutinib reimbursed but inferior cardiac profile; zanubrutinib + acalabrutinib not reimbursed.
```

**Excerpt context:**
```
...IND-CLL-1L-BTKI (acalabrutinib). Both second-generation BTKis preferred over ibrutinib. Engine should treat both as interchangeable Cat 1 preferred options based on access. UA reimbursement gap: i...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 105/229: f-0284 - CRITICAL

**Entity:** `IND-DLBCL-1L-POLA-R-CHP`
**File:** `knowledge_base/hosted/content/indications/ind_dlbcl_1l_pola_r_chp.yaml`
**Field:** `rationale`
**Matched pattern:** `MUST`
**Pattern class:** direct obligation

**Current value:**
```
Aggressive-track default for newly-diagnosed DLBCL NOS with IPI ≥2 (RF-DLBCL-HIGH-IPI fired). Replaces vincristine in R-CHOP with polatuzumab vedotin (anti-CD79b ADC with MMAE payload). POLARIX trial (NEJM 2022) showed ~6.5% absolute PFS improvement at 2 years vs R-CHOP. Toxicity profile comparable; peripheral neuropathy slightly higher with polatuzumab but vincristine removed. Major access constraint in Ukraine: polatuzumab not НСЗУ-reimbursed. Funding pathway (clinical trial / charitable / out-of-pocket) MUST be verified before plan finalized.
```

**Excerpt context:**
```
...polatuzumab not НСЗУ-reimbursed. Funding pathway (clinical trial / charitable / out-of-pocket) MUST be verified before plan finalized.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 106/229: f-0297 - CRITICAL

**Entity:** `IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR`
**File:** `knowledge_base/hosted/content/indications/ind_endometrial_2l_dostarlimab_dmmr.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Dostarlimab monotherapy is NCCN cat 1 for 2L+ recurrent/metastatic dMMR endometrial carcinoma after 1L platinum-based chemotherapy failure (in patients who did NOT receive ICI in 1L). GARNET trial established durable responses (ORR 45%, DoR >16 mo). Pembrolizumab monotherapy is the labeled equivalent (KEYNOTE-158 pan-tumor MSI-H). This indication applies primarily to historical-era patients whose 1L predated ICI standard of care (RUBY/NRG-GY018 era ~2023+); newer dMMR patients who already received ICI in 1L should receive pembro+lenva or chemo re-challenge in 2L instead. Dramatically lower toxicity than pembro+lenva — preferred when single-agent ICI is appropriate clinical choice. Lynch syndrome screening mandatory for all dMMR endometrial.
```

**Excerpt context:**
```
...andard of care (RUBY/NRG-GY018 era ~2023+); newer dMMR patients who already received ICI in 1L should receive pembro+lenva or chemo re-challenge in 2L instead. Dramatically lower toxicity than pem...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 107/229: f-0300 - CRITICAL

**Entity:** `IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR`
**File:** `knowledge_base/hosted/content/indications/ind_endometrial_2l_pembro_lenva_pmmr.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Pembrolizumab + lenvatinib is the NCCN cat 1 preferred 2L for advanced/ recurrent pMMR endometrial carcinoma after 1L platinum-based chemo failure. KEYNOTE-775 established OS + PFS + ORR benefit over investigator's-choice chemo (doxo or pacli). Indication applies primarily to pMMR patients (the majority of 2L population since dMMR patients now receive ICI in 1L per RUBY/NRG-GY018). Toxicity is substantial — proactive hypertension management + dose-reduction algorithm + anti-diarrheal supportive care needed. dMMR patients who did not receive ICI in 1L should preferentially receive single-agent ICI (dostarlimab GARNET or pembro KEYNOTE-158) rather than the heavier pembro+lenva combination.
```

**Excerpt context:**
```
...algorithm + anti-diarrheal supportive care needed. dMMR patients who did not receive ICI in 1L should preferentially receive single-agent ICI (dostarlimab GARNET or pembro KEYNOTE-158) rather than...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 108/229: f-0311 - CRITICAL

**Entity:** `IND-ET-2L-ANAGRELIDE`
**File:** `knowledge_base/hosted/content/indications/ind_et_2l_anagrelide.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead signoff. Standard-track 2L cytoreduction for HU-resistant/intolerant ET. NOTE: ET 2L algorithm (algo_et_2l.yaml) is MISSING from KB — flagged in audit report; should be authored from the algorithm-batch process, not unilaterally. Indication can still be activated by 1L algorithm fall-through with HU-resistance RF matching. UA access barrier dominant (not reimbursed for ET).
```

**Excerpt context:**
```
...rant ET. NOTE: ET 2L algorithm (algo_et_2l.yaml) is MISSING from KB — flagged in audit report; should be authored from the algorithm-batch process, not unilaterally. Indication can still be activa...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 109/229: f-0312 - CRITICAL

**Entity:** `IND-FL-1L-BR`
**File:** `knowledge_base/hosted/content/indications/ind_fl_1l_br.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Standard-track 1L for FL grade 1-2 / 3A WITH GELF criteria for high tumor burden. BR (bendamustine + rituximab) is preferred over R-CHOP for FL based on StiL trial — superior PFS with comparable toxicity (less alopecia + neuropathy, more cumulative myelosuppression). Maintenance rituximab × 2 years post-induction recommended (PRIMA trial — additional PFS benefit, no clear OS benefit, balance vs infection risk).
```

**Excerpt context:**
```
...neuropathy, more cumulative myelosuppression). Maintenance rituximab × 2 years post-induction recommended (PRIMA trial — additional PFS benefit, no clear OS benefit, balance vs infection risk).

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 110/229: f-0323 - CRITICAL

**Entity:** `IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_fl_post_induction_rituximab_maintenance.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Post-induction rituximab maintenance × 2 years standard of care for FL high-burden after BR or R-CHOP induction (NCCN Cat 1). PRIMA trial (Salles 2011 Lancet; 9-year update Bachy 2019): R-maintenance extends median PFS from ~4 to ~10 years vs observation; OS benefit not demonstrated in 9-year follow-up. Counsel on cumulative hypogammaglobulinemia + infection risk; PJP prophylaxis recommended; HBV reactivation surveillance mandatory throughout. Skip in elderly/frail/recurrent infection patients (preference-sensitive).
```

**Excerpt context:**
```
...-year follow-up. Counsel on cumulative hypogammaglobulinemia + infection risk; PJP prophylaxis recommended; HBV reactivation surveillance mandatory throughout. Skip in elderly/frail/recurrent infection...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 111/229: f-0327 - CRITICAL

**Entity:** `IND-GASTRIC-METASTATIC-2L-HER2-TDXD`
**File:** `knowledge_base/hosted/content/indications/ind_gastric_metastatic_2l_her2_tdxd.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Trastuzumab deruxtecan (T-DXd) is the NCCN cat 1 preferred 2L for HER2+ metastatic gastric/GEJ adenocarcinoma after 1L trastuzumab-based regimen failure. DESTINY-Gastric01 established ORR + OS + PFS benefit over investigator's-choice chemo. HER2 positivity should be reconfirmed on fresh biopsy where feasible (HER2 loss occurs in ~30% post 1L). Gastric dose is 6.4 mg/kg q3w (higher than breast 5.4 mg/kg). ILD is the dose-limiting boxed-warning toxicity.
```

**Excerpt context:**
```
...Gastric01 established ORR + OS + PFS benefit over investigator's-choice chemo. HER2 positivity should be reconfirmed on fresh biopsy where feasible (HER2 loss occurs in ~30% post 1L). Gastric dose...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 112/229: f-0329 - CRITICAL

**Entity:** `IND-GASTRIC-METASTATIC-2L-RAMUCIRUMAB-PACLITAXEL`
**File:** `knowledge_base/hosted/content/indications/ind_gastric_metastatic_2l_ramucirumab_paclitaxel.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Paclitaxel + ramucirumab is the NCCN cat 1 preferred 2L regimen for HER2-negative metastatic gastric/GEJ adenocarcinoma after 1L platinum + fluoropyrimidine ± ICI failure. RAINBOW trial established OS + PFS + ORR benefit over paclitaxel alone. HER2+ patients route instead to T-DXd (IND-GASTRIC-METASTATIC-2L-HER2-TDXD). MSI-H patients who did not receive ICI in 1L should receive pembrolizumab monotherapy preferentially. Bleeding/perforation risk profile excludes patients with active GI bleed or recent surgery.
```

**Excerpt context:**
```
...d to T-DXd (IND-GASTRIC-METASTATIC-2L-HER2-TDXD). MSI-H patients who did not receive ICI in 1L should receive pembrolizumab monotherapy preferentially. Bleeding/perforation risk profile excludes p...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 113/229: f-0340 - CRITICAL

**Entity:** `IND-HCC-SYSTEMIC-1L-ATEZO-BEV`
**File:** `knowledge_base/hosted/content/indications/ind_hcc_systemic_1l_atezo_bev.yaml`
**Field:** `do_not_do`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
['Do NOT initiate without EGD within 6 months — high-risk varices must be ligated/banded first (perforation/bleed risk)', 'Do NOT use in Child-Pugh B/C — atezo+bev not studied; mortality risk', 'Do NOT skip HBV prophylaxis in HBsAg+ / anti-HBc+ patients (entecavir or TDF) — HBV reactivation reported under anti-VEGF + ICI; continue ≥12 mo post-therapy', 'Do NOT delay HCV-DAA in HCV-RNA+ patients — initiate sofosbuvir/velpatasvir before or concurrently with atezo+bev; SVR12 reduces decompensation risk and may improve OS in HCC-on-HCV-cirrhosis', 'Do NOT combine sofosbuvir with amiodarone — severe bradycardia / cardiac arrest', 'Do NOT continue bevacizumab through Grade 3+ HTN or proteinuria >3.5 g/24h']
```

**Excerpt context:**
```
"Do NOT initiate without EGD within 6 months — high-risk varices must be ligated/banded first (perforation/bleed risk)" "Do NOT use in Child-Pugh B/C — atezo+bev no...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 114/229: f-0356 - CRITICAL

**Entity:** `IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH`
**File:** `knowledge_base/hosted/content/indications/ind_hnscc_rm_1l_pembro_mono_cps_high.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Pembrolizumab monotherapy in PD-L1 CPS ≥20 R/M HNSCC achieves equivalent OS to chemo-IO with substantially less toxicity (no cisplatin/carbo + 5-FU burden) — KEYNOTE-048 — and is preferred for elderly, comorbid, or fitness-limited patients with high-CPS tumors. For low-burden indolent recurrence, the durable-response tail (~22 mo median DOR among responders) is particularly valuable. Patients with rapid progression / visceral crisis or symptomatic disease at 1L assessment should receive chemo-IO instead — pembro monotherapy has insufficient early disease-control kinetics.
```

**Excerpt context:**
```
...ble. Patients with rapid progression / visceral crisis or symptomatic disease at 1L assessment should receive chemo-IO instead — pembro monotherapy has insufficient early disease-control kinetics.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 115/229: f-0360 - CRITICAL

**Entity:** `IND-MCL-2L-ACALABRUTINIB`
**File:** `knowledge_base/hosted/content/indications/ind_mcl_2l_acalabrutinib.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Acalabrutinib monotherapy for r/r MCL after ≥1 prior line per ACE- LY-004 (FDA-approved). Substantially superior cardiac safety vs ibrutinib (afib ~3% vs ~7-15%, hypertension ~5% vs ~17%) while preserving efficacy (ORR 81%, mPFS 22 mo). Preferred BTKi for r/r MCL when accessible, particularly in older patients with cardiac history / hypertension / on anticoagulation. Continuous therapy until progression or intolerance. Funding pathway must be confirmed; ibrutinib (REG-IBRUTINIB-CLL or similar) reimbursed via НСЗУ as fallback.
```

**Excerpt context:**
```
...ion / on anticoagulation. Continuous therapy until progression or intolerance. Funding pathway must be confirmed; ibrutinib (REG-IBRUTINIB-CLL or similar) reimbursed via НСЗУ as fallback.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 116/229: f-0367 - CRITICAL

**Entity:** `IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_mcl_post_induction_rituximab_maintenance.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Post-induction maintenance — applies after autoSCT (fit younger track) OR after BR/R-CHOP (older track). Engine should NOT activate this when 1L was BTKi-R continuous (handled by BTKi continuation). LyMa (Le Gouill 2017 NEJM) is the primary post-autoSCT evidence; EU MCL Elderly (Kluin-Nelemans 2012 NEJM) is the primary post-CIT evidence.
```

**Excerpt context:**
```
...intenance — applies after autoSCT (fit younger track) OR after BR/R-CHOP (older track). Engine should NOT activate this when 1L was BTKi-R continuous (handled by BTKi continuation). LyMa (Le Gouil...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 117/229: f-0370 - CRITICAL

**Entity:** `IND-MDS-HR-1L-VEN-AZA`
**File:** `knowledge_base/hosted/content/indications/ind_mds_hr_1l_ven_aza.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Aggressive track for MDS-HR. NCCN 2A given off-label status pending phase-3. STUB — requires clinical co-lead signoff. Open clinical question for clinical reviewer: should this indication be removed pending phase-3, or kept as scaffolded option?
```

**Excerpt context:**
```
...ase-3. STUB — requires clinical co-lead signoff. Open clinical question for clinical reviewer: should this indication be removed pending phase-3, or kept as scaffolded option?

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 118/229: f-0374 - CRITICAL

**Entity:** `IND-MDS-LR-LENALIDOMIDE-DEL5Q`
**File:** `knowledge_base/hosted/content/indications/ind_mds_lr_lenalidomide_del5q.yaml`
**Field:** `rationale`
**Matched pattern:** `MUST`
**Pattern class:** direct obligation

**Current value:**
```
Lenalidomide is Cat 1 standard for transfusion-dependent del(5q) LR-MDS. Pivotal MDS-003 (Houston phase-2) + MDS-004 (phase-3 RCT, Fenaux et al., Blood 2011) — at 10 mg PO d1-21/28d: ~56% achieve RBC TI vs 5.9% placebo at 26 weeks; ~20-25% achieve cytogenetic CR with loss of del(5q) clone. Median TI duration >2 years. Mechanism: cereblon-mediated selective degradation of casein kinase 1A1 (CK1α), encoded within the 5q33.1 commonly-deleted region — del(5q) cells haploinsufficient → uniquely sensitive. CRITICAL: lenalidomide is teratogenic — REMS / Revlimid Risk Management Programme mandatory; pregnancy testing weekly first month, then monthly. VTE prophylaxis (aspirin 81-325 mg PO daily; LMWH for higher-risk) mandatory. Avoid concurrent ESA (additive VTE risk). MUST screen TP53 — TP53-mutated del(5q) MDS has higher AML transformation risk on lenalidomide (~30-40% at 2 years vs ~10% TP53-wt) and may benefit from earlier alloHCT pathway. Lenalidomide НСЗУ-reimbursed in Ukraine for this indication.
```

**Excerpt context:**
```
...81-325 mg PO daily; LMWH for higher-risk) mandatory. Avoid concurrent ESA (additive VTE risk). MUST screen TP53 — TP53-mutated del(5q) MDS has higher AML transformation risk on lenalidomide (~30...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 119/229: f-0379 - CRITICAL

**Entity:** `IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB`
**File:** `knowledge_base/hosted/content/indications/ind_melanoma_2l_relatlimab_nivolumab.yaml`
**Field:** `rationale`
**Matched pattern:** `patient should`
**Pattern class:** patient-directed imperative

**Current value:**
```
Relatlimab + nivolumab (Opdualag fixed-dose) is the first anti-LAG-3 + anti-PD-1 combination, FDA-approved 2022 in 1L metastatic melanoma per RELATIVITY-047 (mPFS 10.1 vs 4.6 mo vs nivo mono). Key differentiator vs ipi+nivo: Grade 3-4 treatment-related AE 18.9% vs ~50%. Position in our 2L+ algorithm: IO-naive alternative (the patient received 1L BRAFi+MEKi and so has not yet exhausted PD-1/LAG-3 axis), particularly attractive when ipi-grade irAE risk is unacceptable. Trial was 1L; off-label positioning at 2L requires MDT documentation. Note: if RELATIVITY was used at 1L (IO-naive cohort), this Indication does NOT apply at 2L — patient should move to BRAFi+MEKi (if BRAF V600+) or alternative salvage.
```

**Excerpt context:**
```
.... Note: if RELATIVITY was used at 1L (IO-naive cohort), this Indication does NOT apply at 2L — patient should move to BRAFi+MEKi (if BRAF V600+) or alternative salvage.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 120/229: f-0380 - CRITICAL

**Entity:** `IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB`
**File:** `knowledge_base/hosted/content/indications/ind_melanoma_2l_relatlimab_nivolumab.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Relatlimab + nivolumab (Opdualag fixed-dose) is the first anti-LAG-3 + anti-PD-1 combination, FDA-approved 2022 in 1L metastatic melanoma per RELATIVITY-047 (mPFS 10.1 vs 4.6 mo vs nivo mono). Key differentiator vs ipi+nivo: Grade 3-4 treatment-related AE 18.9% vs ~50%. Position in our 2L+ algorithm: IO-naive alternative (the patient received 1L BRAFi+MEKi and so has not yet exhausted PD-1/LAG-3 axis), particularly attractive when ipi-grade irAE risk is unacceptable. Trial was 1L; off-label positioning at 2L requires MDT documentation. Note: if RELATIVITY was used at 1L (IO-naive cohort), this Indication does NOT apply at 2L — patient should move to BRAFi+MEKi (if BRAF V600+) or alternative salvage.
```

**Excerpt context:**
```
...if RELATIVITY was used at 1L (IO-naive cohort), this Indication does NOT apply at 2L — patient should move to BRAFi+MEKi (if BRAF V600+) or alternative salvage.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 121/229: f-0392 - CRITICAL

**Entity:** `IND-MF-EARLY-1L-SKIN-DIRECTED`
**File:** `knowledge_base/hosted/content/indications/ind_mf_early_1l_skin_directed.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Early-stage MF (IA-IIA per ISCL/EORTC TNMB) — skin-directed first-line is curative-intent for IA, durable disease control for IB-IIA. Modalities: topical corticosteroids (potent class for plaques), narrow-band UVB (NBUVB) for thin patches, PUVA for thicker plaques, total skin electron beam therapy (TSEBT) for diffuse extensive disease, topical nitrogen mustard / bexarotene gel. Selection by extent + thickness + dermatology resource. Skin-directed avoids systemic immunosuppression and preserves systemic therapy options for progression. Workup must rule out occult B2 (Sézary count) and LCT before committing — both upstage to advanced + systemic-first.
```

**Excerpt context:**
```
...oids systemic immunosuppression and preserves systemic therapy options for progression. Workup must rule out occult B2 (Sézary count) and LCT before committing — both upstage to advanced + syste...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 122/229: f-0393 - CRITICAL

**Entity:** `IND-MM-1L-DVRD`
**File:** `knowledge_base/hosted/content/indications/ind_mm_1l_dvrd.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
STUB — requires clinical co-lead signoff before publication. Aggressive counterpart to IND-MM-1L-VRD for two-plan output (CHARTER §2). Major access constraint in Ukraine: daratumumab is not currently НСЗУ- reimbursed — funding pathway must be confirmed BEFORE this Plan is finalized. Red-cell phenotyping (type and screen) BEFORE first daratumumab dose is mandatory due to anti-CD38 interference with crossmatching.
```

**Excerpt context:**
```
...access constraint in Ukraine: daratumumab is not currently НСЗУ- reimbursed — funding pathway must be confirmed BEFORE this Plan is finalized. Red-cell phenotyping (type and screen) BEFORE firs...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 123/229: f-0399 - CRITICAL

**Entity:** `IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE`
**File:** `knowledge_base/hosted/content/indications/ind_mm_post_asct_lenalidomide_maintenance.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead sign-off. Standard-track post-ASCT consolidation. line_of_therapy: 1 reflects "1L pathway" continuation rather than "2nd line" — maintenance is part of the 1L plan in MM. Engine should activate this Indication after ASCT decision tree completes. Bortezomib / ixazomib / lenalidomide-bortezomib doublet alternatives are separate future Indications.
```

**Excerpt context:**
```
...athway" continuation rather than "2nd line" — maintenance is part of the 1L plan in MM. Engine should activate this Indication after ASCT decision tree completes. Bortezomib / ixazomib / lenalidom...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 124/229: f-0409 - CRITICAL

**Entity:** `IND-NMZL-1L-BR`
**File:** `knowledge_base/hosted/content/indications/ind_nmzl_1l_br.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Standard 1L for nodal MZL with high tumor burden (GELF-style) or symptomatic disease. BR (bendamustine + rituximab) is preferred over R-CHOP for indolent NMZL — same logic as FL. Maintenance rituximab × 2 years post-induction recommended.
```

**Excerpt context:**
```
...er R-CHOP for indolent NMZL — same logic as FL. Maintenance rituximab × 2 years post-induction recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 125/229: f-0412 - CRITICAL

**Entity:** `IND-NMZL-1L-HCV-POSITIVE`
**File:** `knowledge_base/hosted/content/indications/ind_nmzl_1l_hcv_positive.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — extends NMZL coverage to HCV-positive subset by mirroring SMZL HCV+ / HCV-MZL extranodal logic. Smaller evidence base than HCV-MZL extranodal; clinical co-lead sign-off pending. Open question for hematologist consult: should DAA-first be routed even in GELF-positive HCV+ NMZL, or should BR be added concurrently?
```

**Excerpt context:**
```
...HCV-MZL extranodal; clinical co-lead sign-off pending. Open question for hematologist consult: should DAA-first be routed even in GELF-positive HCV+ NMZL, or should BR be added concurrently?

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 126/229: f-0413 - CRITICAL

**Entity:** `IND-NMZL-1L-HCV-POSITIVE`
**File:** `knowledge_base/hosted/content/indications/ind_nmzl_1l_hcv_positive.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — extends NMZL coverage to HCV-positive subset by mirroring SMZL HCV+ / HCV-MZL extranodal logic. Smaller evidence base than HCV-MZL extranodal; clinical co-lead sign-off pending. Open question for hematologist consult: should DAA-first be routed even in GELF-positive HCV+ NMZL, or should BR be added concurrently?
```

**Excerpt context:**
```
...stion for hematologist consult: should DAA-first be routed even in GELF-positive HCV+ NMZL, or should BR be added concurrently?

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 127/229: f-0418 - CRITICAL

**Entity:** `IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_2l_egfr_post_osi_ami_laz.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Amivantamab (EGFR-MET bispecific antibody) + lazertinib (3rd-gen EGFR-TKI) for EGFR-mutated metastatic NSCLC (ex19del / L858R) progressing on 1L osimertinib. MARIPOSA-2 demonstrated PFS HR ~0.44-0.48 vs platinum doublet alone. The combination targets both the on-pathway (T790M / C797S resistance mutations) and the bypass-pathway (MET amplification — common osimertinib resistance mechanism) by virtue of amivantamab's dual EGFR + MET targeting. Pre-treatment biopsy or ctDNA NGS strongly recommended to characterize resistance and exclude small-cell transformation (5-15%, requires platinum-etoposide instead). Significant toxicity burden: IRR (mitigated by SC formulation), VTE (DOAC prophylaxis mandatory first 4 mo), rash, paronychia. Aggressive-track for fit patients with funding pathway.
```

**Excerpt context:**
```
...virtue of amivantamab's dual EGFR + MET targeting. Pre-treatment biopsy or ctDNA NGS strongly recommended to characterize resistance and exclude small-cell transformation (5-15%, requires platinum-eto...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 128/229: f-0425 - CRITICAL

**Entity:** `IND-NSCLC-2L-KRAS-G12C-SOTORASIB`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_2l_kras_g12c_sotorasib.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead sign-off. Standard-track 2L KRAS G12C+ NSCLC. Adagrasib (separate Indication) preferred for active brain metastases. Replaces existing IND-NSCLC-KRAS-G12C-MET-2L (which is retained but should be deprecated — it points to same regimen).
```

**Excerpt context:**
```
...r active brain metastases. Replaces existing IND-NSCLC-KRAS-G12C-MET-2L (which is retained but should be deprecated — it points to same regimen).

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 129/229: f-0432 - CRITICAL

**Entity:** `IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_2l_pdl1_post_io_docetaxel.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Docetaxel + ramucirumab for 2L driver-negative metastatic NSCLC after 1L platinum + ICI failure (REVEL trial — pre-ICI era but mechanism still applies). Adds modest OS + PFS benefit over single-agent docetaxel. In modern post-ICI+chemo failure setting, this represents the default cytotoxic 2L for driver-negative disease. Single-agent docetaxel (without ramucirumab) is the realistic fallback in Ukraine where ramucirumab not NSZU-reimbursed for NSCLC. Nintedanib + docetaxel (LUME-Lung 1) is alternative for adenocarcinoma histology. CRITICAL: comprehensive NGS panel must rule out all actionable drivers before cytotoxic — driver-positive disease that progressed on 1L (rare given driver-positive ≠ ICI 1L) goes to next-line targeted, not docetaxel.
```

**Excerpt context:**
```
...l (LUME-Lung 1) is alternative for adenocarcinoma histology. CRITICAL: comprehensive NGS panel must rule out all actionable drivers before cytotoxic — driver-positive disease that progressed on...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 130/229: f-0434 - CRITICAL

**Entity:** `IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_2l_ros1_post_criz_entrectinib.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Entrectinib (ROS1 / NTRK / ALK TKI with CNS penetration) for ROS1+ metastatic NSCLC progressing on crizotinib 1L. Crizotinib has poor CNS penetration; CNS progression is a common failure mode and entrectinib's high intracranial activity (~55% intracranial ORR in STARTRK-2 integrated analysis) makes it preferred in CNS-positive disease. For systemic-only progression or G2032R solvent-front resistance, repotrectinib (TRIDENT-1, separate Indication) may be preferred. Lorlatinib also has ROS1 activity but is less specifically studied for ROS1 2L. Pre-treatment NGS recommended to characterize resistance mutations driving precise next-line choice.
```

**Excerpt context:**
```
...latinib also has ROS1 activity but is less specifically studied for ROS1 2L. Pre-treatment NGS recommended to characterize resistance mutations driving precise next-line choice.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 131/229: f-0438 - CRITICAL

**Entity:** `IND-NSCLC-3L-DRIVER-BEYOND-2L`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_3l_driver_beyond_2l.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Patients with driver-positive NSCLC (EGFR, ALK, ROS1, RET, MET, BRAF, NTRK, HER2) who progress through 1L targeted therapy + 2L chemoimmunotherapy or IO have limited 3L+ options. Docetaxel ± ramucirumab (REVEL trial, Garon 2014 Lancet) or docetaxel ± nintedanib (LUME-Lung 1, Reck 2014 Lancet Oncol) are the most-validated 3L+ regimens. mPFS gain ~1.5 mo and mOS gain ~1.5 mo — modest but consistent. Re-biopsy at 3L+ to identify acquired resistance mechanisms (T790M after 1st-gen EGFR TKI, MET amplification, SCLC transformation, lineage plasticity) is strongly recommended; biomarker-driven 3L options (amivantamab for EGFR ex20ins, capmatinib/tepotinib for MET, larotrectinib for NTRK) often outperform empirical chemo. Best supportive care + clinical trial is a valid alternative when ECOG declines.
```

**Excerpt context:**
```
...fter 1st-gen EGFR TKI, MET amplification, SCLC transformation, lineage plasticity) is strongly recommended; biomarker-driven 3L options (amivantamab for EGFR ex20ins, capmatinib/tepotinib for MET, laro...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 132/229: f-0445 - CRITICAL

**Entity:** `IND-NSCLC-ELDERLY-CARBO-PEM-MOD`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_elderly_carbo_pem_mod.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
For elderly (≥75 years) and/or ECOG 2 patients with stage IV non-squamous NSCLC without actionable drivers, full-dose carboplatin AUC 5-6 + pemetrexed 500 mg/m² + pembrolizumab (KEYNOTE-189 dose schedule) has unacceptable toxicity. Modified regimen: carboplatin AUC 4 + pemetrexed 500 mg/m² q21d × 4-6 cycles, then pemetrexed maintenance ± pembrolizumab. JCOG 0803 (Quoix 2011 Lancet) established elderly-specific carbo + pacli/gem combinations; ELDERS (Gridelli 2018) and other elderly-specific trials confirmed dose-modified approach feasible. KEYNOTE-189 / KEYNOTE-407 enrolled patients ≤75 in majority but elderly subgroup analyses (JCO 2020 elderly PCM) suggest pembro addition still beneficial. ECOG 2 patients have more limited evidence; single-agent chemo (weekly paclitaxel, gemcitabine) acceptable. Comprehensive geriatric assessment (CGA) recommended for ≥75 to identify frailty + reversible deficits. STUB regimen — no dedicated REG- entity for elderly carbo-pem-mod yet; flagged for REG follow-up.
```

**Excerpt context:**
```
...nt chemo (weekly paclitaxel, gemcitabine) acceptable. Comprehensive geriatric assessment (CGA) recommended for ≥75 to identify frailty + reversible deficits. STUB regimen — no dedicated REG- entity for...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 133/229: f-0448 - CRITICAL

**Entity:** `IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_pembro_maintenance_post_chemo.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Pembrolizumab maintenance is a continuation of the KEYNOTE-189 (non- squamous, with pemetrexed maintenance partner) and KEYNOTE-407 (squamous, no pemetrexed) 1L regimen — pembrolizumab continues monotherapy q3 weeks until total 35 cycles (~2 years) OR progression OR unacceptable toxicity. 5-year OS ~19-22% in KEYNOTE-189 mature follow-up vs ~11% chemo alone. Critical to recognize maintenance is NOT a separate decision point — patients completing induction without progression should automatically transition to maintenance phase. Discontinuation at 35 cycles is per-protocol; some real-world programs continue beyond if benefit + tolerance.
```

**Excerpt context:**
```
...intenance is NOT a separate decision point — patients completing induction without progression should automatically transition to maintenance phase. Discontinuation at 35 cycles is per-protocol; s...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 134/229: f-0449 - CRITICAL

**Entity:** `IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_pembro_maintenance_post_chemo.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
STUB — pending Clinical Co-Lead sign-off. Standard-track maintenance continuation for stage IV NSCLC after induction chemo+pembro per KEYNOTE-189/-407. Engine should automatically activate at end of induction; not a separate prompt to clinician. Pemetrexed maintenance (in non-squamous, with pembrolizumab) is a separate concurrent regimen consideration — future Indication entity.
```

**Excerpt context:**
```
...ance continuation for stage IV NSCLC after induction chemo+pembro per KEYNOTE-189/-407. Engine should automatically activate at end of induction; not a separate prompt to clinician. Pemetrexed mai...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 135/229: f-0450 - CRITICAL

**Entity:** `IND-NSCLC-TMB-HIGH-MET-1L-PEMBRO-MONO`
**File:** `knowledge_base/hosted/content/indications/ind_nsclc_tmb_high_met_1l_pembro_mono.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Wires BIO-TMB-HIGH for the first time. Per docs/BIOMARKER_CATALOG.md rationale: PER-DISEASE wiring, not pan-tumor abstraction (KEYNOTE-158 excluded NSCLC; engine selection is cleaner per-disease).
Engine usage: this indication should appear as ALTERNATIVE track when PD-L1 TPS is ambiguous (1-49%) or when patient prefers ICI mono over chemo-IO combo. Wired as standalone IND so the algorithm (ALGO-NSCLC-METASTATIC-1L, separate task) can route TMB-high cases here when PD-L1-based default is suboptimal. Driver mutations (EGFR / ALK) explicitly excluded — those have superior targeted therapies (osimertinib / alectinib).
```

**Excerpt context:**
```
...TE-158 excluded NSCLC; engine selection is cleaner per-disease). Engine usage: this indication should appear as ALTERNATIVE track when PD-L1 TPS is ambiguous (1-49%) or when patient prefers ICI mo...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 136/229: f-0464 - CRITICAL

**Entity:** `IND-OVARIAN-MAINT-BEV`
**File:** `knowledge_base/hosted/content/indications/ind_ovarian_maint_bev.yaml`
**Field:** `rationale`
**Matched pattern:** `Must`
**Pattern class:** direct obligation

**Current value:**
```
Bevacizumab 15 mg/kg q3w added to carboplatin + paclitaxel induction (starting cycle 2) and continued as maintenance for 15-22 months total is the GOG-218 / ICON7 paradigm for advanced epithelial ovarian cancer. GOG-218 (Burger 2011 NEJM): mPFS 14.1 vs 10.3 mo (HR 0.72) vs chemo alone; ICON7 (Perren 2011 NEJM): mPFS 19.0 vs 17.3 mo overall, 18.1 vs 14.5 mo in high-risk (suboptimal debulking + stage III/IV). OS benefit confined to high-risk subgroup. PAOLA-1 (Ray-Coquard 2019 NEJM) extended paradigm: bev + olaparib maintenance for HRD-positive non-BRCA patients. Must be discontinued ≥4 weeks before any major surgery; GI perforation, fistula, hemorrhage, hypertension, proteinuria are class effects. Olaparib maintenance (SOLO-1) is preferred for BRCA-mutated patients; bev considered for HRD-positive non-BRCA per PAOLA-1. STUB regimen — no dedicated REG- entity for bev maintenance ovarian yet; flagged for REG follow-up.
```

**Excerpt context:**
```
...d 2019 NEJM) extended paradigm: bev + olaparib maintenance for HRD-positive non-BRCA patients. Must be discontinued ≥4 weeks before any major surgery; GI perforation, fistula, hemorrhage, hypert...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 137/229: f-0476 - CRITICAL

**Entity:** `IND-PMF-ALLOHCT-HIGH-RISK`
**File:** `knowledge_base/hosted/content/indications/ind_pmf_allohct_high_risk.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
AlloHCT is the ONLY curative option for PMF — mandatory consideration in ALL transplant-eligible patients with DIPSS-Plus intermediate-2 OR high-risk OR MIPSS70+ high-risk OR HMR mutations (TP53, ASXL1, EZH2, IDH1/2, SRSF2). 5-y OS post-HCT 30-65% (DIPSS-stratified) vs <20% high-risk without HCT. Ruxolitinib pre-HCT bridging 3-6 months reduces spleen volume + symptoms → improves transplant outcomes; taper ruxolitinib 5-7 days before conditioning to avoid cytokine rebound. Donor search initiated CONCURRENTLY with JAKi optimization — donor identification can take 3-6 months. Conditioning intensity tailored to age + comorbidity. Splenectomy NOT routinely recommended pre-HCT (high mortality in MF; only for refractory massive splenomegaly per institution). TP53-mutated MF has worse outcomes (~20% 5-y OS post-HCT) but HCT still the only curative pathway. CRITICAL: do NOT defer alloHCT discussion to JAKi failure — long-term JAKi exposure does not delay progression and donor search delays compound.
```

**Excerpt context:**
```
...ke 3-6 months. Conditioning intensity tailored to age + comorbidity. Splenectomy NOT routinely recommended pre-HCT (high mortality in MF; only for refractory massive splenomegaly per institution). TP53...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 138/229: f-0477 - CRITICAL

**Entity:** `IND-PROSTATE-MCRPC-1L-ARPI`
**File:** `knowledge_base/hosted/content/indications/ind_prostate_mcrpc_1l_arpi.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Workhorse mCRPC 1L for non-HRR-mutant disease with prior ADT exposure. Patients ARPI-naive (rare in modern era — most have had ARPI in mHSPC): enzalutamide / abiraterone preferred. Patients with prior ARPI: switch ARPI not generally recommended; consider docetaxel, PARPi (if HRR+), or Lu-PSMA (if PSMA-PET+).
```

**Excerpt context:**
```
...PC): enzalutamide / abiraterone preferred. Patients with prior ARPI: switch ARPI not generally recommended; consider docetaxel, PARPi (if HRR+), or Lu-PSMA (if PSMA-PET+).

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 139/229: f-0481 - CRITICAL

**Entity:** `IND-PTCL-1L-CHOEP-ALLOSCT`
**File:** `knowledge_base/hosted/content/indications/ind_ptcl_1l_choep_allosct.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
CHOEP × 6 induction + alloSCT consolidation in CR1 for fit younger transplant-eligible PTCL NOS where CD30 expression <10% (i.e. CHP-Bv per ECHELON-2 not eligible) OR brentuximab not accessible. CHOEP superior to CHOP in younger T-cell patients per Nordic NLG-T- 01. AlloSCT consolidation in CR1 dramatically improves long-term PFS per EBMT registries (5y PFS ~50% vs ~25-30% CHOEP-alone). AutoSCT alternative considered but generally inferior for PTCL NOS biology. Donor sourcing critical — sibling > matched unrelated > haploidentical. NCCN-recommended for fit patients despite limited RCT data — practice standard given dismal natural history without consolidation.
```

**Excerpt context:**
```
...PTCL NOS biology. Donor sourcing critical — sibling > matched unrelated > haploidentical. NCCN-recommended for fit patients despite limited RCT data — practice standard given dismal natural history wit...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 140/229: f-0490 - CRITICAL

**Entity:** `IND-PV-ANAGRELIDE-CONTINUOUS`
**File:** `knowledge_base/hosted/content/indications/ind_pv_anagrelide_continuous.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Anagrelide is a second-line cytoreductive option for polycythemia vera patients who fail or are intolerant to hydroxyurea, when thrombocytosis is the dominant clinical concern. Mechanism is selective inhibition of megakaryocyte maturation. PT1 trial (Harrison 2005 NEJM, ET cohort): anagrelide + aspirin vs HU + aspirin showed equivalent overall events but higher arterial thrombosis, hemorrhage, and myelofibrotic transformation in anagrelide arm. PV-specific data extrapolated from ET; ELN/NCCN/ESMO position anagrelide as 2L for PV (after HU + ruxolitinib failure). Anagrelide does NOT address erythrocytosis — phlebotomy + low-dose aspirin must continue; ruxolitinib (RESPONSE trial) is competing 2L option with broader symptom + spleen + erythrocytosis benefit. Anagrelide preferred when thrombocytosis is the dominant uncontrolled parameter and ruxolitinib not accessible.
```

**Excerpt context:**
```
...xolitinib failure). Anagrelide does NOT address erythrocytosis — phlebotomy + low-dose aspirin must continue; ruxolitinib (RESPONSE trial) is competing 2L option with broader symptom + spleen +...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 141/229: f-0492 - CRITICAL

**Entity:** `IND-PV-PREGNANCY-PEG-IFN`
**File:** `knowledge_base/hosted/content/indications/ind_pv_pregnancy_peg_ifn.yaml`
**Field:** `rationale`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Polycythemia vera in pregnancy is high-risk: maternal thrombosis ~20%, fetal loss ~25%, pre-eclampsia ~10%, IUGR ~10%. Hydroxyurea is teratogenic (FDA category D) and must be discontinued ≥3 months pre-conception (peg-IFN bridge) OR immediately on confirmed pregnancy. Pegylated interferon alpha-2a (Pegasys) 45-90 μg SC weekly is the cytoreductive of choice — does not cross placenta, no documented teratogenicity in registry data (PROUD-PV, MPN registries). Ropeginterferon alfa-2b (Besremi, REG-ROPEGINTERFERON-PV) is the modern alternative with weekly-to-biweekly dosing. Targets: HCT <45%, platelets <600 ×10⁹/L. Concurrent low-dose aspirin (75-100 mg PO daily) throughout pregnancy + 6 weeks postpartum. Low-dose phlebotomy (200-300 mL units) only if HCT >45%. LMWH prophylaxis postpartum 4-6 weeks (high VTE risk window). Multidisciplinary care: hematology + maternal-fetal medicine. ELN-MPN guidelines (Tefferi 2018, Barbui 2018) and pregnancy registry data underpin recommendations.
```

**Excerpt context:**
```
...etal loss ~25%, pre-eclampsia ~10%, IUGR ~10%. Hydroxyurea is teratogenic (FDA category D) and must be discontinued ≥3 months pre-conception (peg-IFN bridge) OR immediately on confirmed pregnanc...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 142/229: f-0503 - CRITICAL

**Entity:** `IND-TCELL-1L-CHP-BV`
**File:** `knowledge_base/hosted/content/indications/ind_tcell_1l_chp_bv.yaml`
**Field:** `rationale`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Standard 1L for systemic ALCL (universal CD30+) + CD30+ PTCL NOS + CD30+ AITL per ECHELON-2 (Horwitz 2019). Brentuximab REPLACES vincristine — avoids additive MMAE neuropathy. AutoSCT consolidation recommended for ALCL ALK- + high-IPI PTCL NOS in fit younger.
```

**Excerpt context:**
```
...19). Brentuximab REPLACES vincristine — avoids additive MMAE neuropathy. AutoSCT consolidation recommended for ALCL ALK- + high-IPI PTCL NOS in fit younger.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 143/229: f-0513 - CRITICAL

**Entity:** `IND-WM-2L-ZANUBRUTINIB`
**File:** `knowledge_base/hosted/content/indications/ind_wm_2l_zanubrutinib.yaml`
**Field:** `rationale`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Zanubrutinib monotherapy for r/r MYD88-mutated WM after ≥1 prior line per ASPEN trial. Substantially superior cardiac safety vs ibrutinib (afib 2.6% vs 15.3%; cardiac death 0% vs 1.6%; major bleeding 4% vs 9%; hypertension 13% vs 25%) while preserving efficacy (numerically superior VGPR rate in MYD88-mut cohort: 28% vs 19%). Preferred BTKi for r/r WM where accessible — particularly for older patients with cardiac history, hypertension, or anticoagulation. Continuous therapy until progression or intolerance. CXCR4 status should be checked — WHIM-mutated subset has reduced depth of response with both BTKis; consider BDR or CaRD alternative for these patients.
```

**Excerpt context:**
```
...tension, or anticoagulation. Continuous therapy until progression or intolerance. CXCR4 status should be checked — WHIM-mutated subset has reduced depth of response with both BTKis; consider BDR o...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 144/229: f-0522 - CRITICAL

**Entity:** `DRUG-ANAGRELIDE`
**File:** `knowledge_base/hosted/content/drugs/anagrelide.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ET 2L per PT-1 trial (Harrison et al., NEJM 2005): non-inferior to HU on thrombosis but more arterial thrombosis + bleeding + myelofibrosis progression in some endpoints. Reserved for HU-intolerance/resistance or for younger ET patients wanting to avoid HU's theoretical leukemogenic concern. Cardiac evaluation (ECG ± echo) recommended before starting if comorbidity present.
```

**Excerpt context:**
```
...tients wanting to avoid HU's theoretical leukemogenic concern. Cardiac evaluation (ECG ± echo) recommended before starting if comorbidity present.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 145/229: f-0523 - CRITICAL

**Entity:** `DRUG-ANASTROZOLE`
**File:** `knowledge_base/hosted/content/drugs/anastrozole.yaml`
**Field:** `mechanism`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Reversible non-steroidal AI — competitively inhibits aromatase, blocking peripheral conversion of androgens to estrogens. Postmenopausal estrogen suppression to <2 pmol/L. In premenopausal women, must be combined with ovarian suppression (LHRH agonist).
```

**Excerpt context:**
```
...rogens to estrogens. Postmenopausal estrogen suppression to <2 pmol/L. In premenopausal women, must be combined with ovarian suppression (LHRH agonist).

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 146/229: f-0524 - CRITICAL

**Entity:** `DRUG-APREPITANT`
**File:** `knowledge_base/hosted/content/drugs/aprepitant.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Foundation NK1 antagonist for CINV prevention in HEC regimens. Three- drug regimen (NK1 + 5-HT3 + dex) shifts complete-response rate from ~50% (5-HT3 + dex alone) to ~80% across days 1-5 in cisplatin-based HEC trials (Hesketh, Warr). Adding olanzapine 10 mg PO d1-4 to make it a four-drug regimen further improves complete response by ~10% absolute (Navari, NEJM 2016). Critical interaction: aprepitant doubles dexamethasone exposure → must halve dex dose when co- prescribed (16 mg → 8 mg on day 1 if using oral dex; IV dex needs similar adjustment). Fosaprepitant 150 mg IV is the IV pro-drug alternative (single dose). For high-risk DLBCL R-CHOP / BEACOPP / ICE / DHAP, aprepitant is standard premed.
```

**Excerpt context:**
```
...bsolute (Navari, NEJM 2016). Critical interaction: aprepitant doubles dexamethasone exposure → must halve dex dose when co- prescribed (16 mg → 8 mg on day 1 if using oral dex; IV dex needs simi...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 147/229: f-0525 - CRITICAL

**Entity:** `DRUG-AVAPRITINIB`
**File:** `knowledge_base/hosted/content/drugs/avapritinib.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Two distinct dose levels by indication. NAVIGATOR established 300 mg as PDGFRA D842V GIST dose (transformative ORR ~88% vs <5% historical imatinib in this genotype). EXPLORER showed cognitive AEs and cerebral microbleeds at 300 mg in advanced SM, leading to PATHFINDER's 200 mg dose registration. Baseline + on-treatment brain MRI recommended in advanced SM. Not effective in KIT D816V- negative advanced SM (rare FIP1L1-PDGFRA myeloid neoplasm with eosinophilia is treated with imatinib instead).
```

**Excerpt context:**
```
...vanced SM, leading to PATHFINDER's 200 mg dose registration. Baseline + on-treatment brain MRI recommended in advanced SM. Not effective in KIT D816V- negative advanced SM (rare FIP1L1-PDGFRA myeloid n...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 148/229: f-0526 - CRITICAL

**Entity:** `DRUG-AXICABTAGENE-CILOLEUCEL`
**File:** `knowledge_base/hosted/content/drugs/axicabtagene_ciloleucel.yaml`
**Field:** `notes`
**Matched pattern:** `MUST`
**Pattern class:** direct obligation

**Current value:**
```
ZUMA-1 pivotal trial (r/r DLBCL after ≥2 lines): ~83% ORR, ~58% CR; durable remissions in ~40% at 5 years. ZUMA-7 moved axi-cel to 2L for primary-refractory / early-relapse DLBCL (superior EFS vs salvage + autoSCT). Tocilizumab MUST be on-site BEFORE infusion (anti-IL6R for CRS rescue). Centre must be REMS / FACT-accredited for CAR-T administration. Bridge therapy may be needed during 3-4 week manufacturing window. Major access barrier in Ukraine: not registered; international referral pathway required if patient + funding feasible.
```

**Excerpt context:**
```
...for primary-refractory / early-relapse DLBCL (superior EFS vs salvage + autoSCT). Tocilizumab MUST be on-site BEFORE infusion (anti-IL6R for CRS rescue). Centre must be REMS / FACT-accredited f...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 149/229: f-0527 - CRITICAL

**Entity:** `DRUG-AXICABTAGENE-CILOLEUCEL`
**File:** `knowledge_base/hosted/content/drugs/axicabtagene_ciloleucel.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
ZUMA-1 pivotal trial (r/r DLBCL after ≥2 lines): ~83% ORR, ~58% CR; durable remissions in ~40% at 5 years. ZUMA-7 moved axi-cel to 2L for primary-refractory / early-relapse DLBCL (superior EFS vs salvage + autoSCT). Tocilizumab MUST be on-site BEFORE infusion (anti-IL6R for CRS rescue). Centre must be REMS / FACT-accredited for CAR-T administration. Bridge therapy may be needed during 3-4 week manufacturing window. Major access barrier in Ukraine: not registered; international referral pathway required if patient + funding feasible.
```

**Excerpt context:**
```
...age + autoSCT). Tocilizumab MUST be on-site BEFORE infusion (anti-IL6R for CRS rescue). Centre must be REMS / FACT-accredited for CAR-T administration. Bridge therapy may be needed during 3-4 we...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 150/229: f-0529 - CRITICAL

**Entity:** `DRUG-AXITINIB`
**File:** `knowledge_base/hosted/content/drugs/axitinib.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Patient-specific titration to maximum tolerated dose (5 → 7 → 10 mg BID) is a defining feature — patients tolerating starting dose with normotension should escalate, as exposure correlates with efficacy. KEYNOTE-426 + JAVELIN-Renal-101 redefined 1L mRCC by combining axitinib with anti-PD-(L)1 — dual mechanism of action outperforms sunitinib monotherapy. Baseline workup: BP, urinalysis (UPCR), LFTs, CBC, TSH, ECG, pregnancy test. Monitor BP weekly first 6 weeks then monthly, urinalysis monthly, LFTs monthly, TSH q3 months. Hold for SBP >160/100 — escalate antihypertensives (ACE-i / ARB first then CCB amlodipine). Hold ≥2 weeks before elective surgery; resume only after full wound healing. Counsel patients on dental procedures (bleeding risk). UA: registered; НСЗУ-reimbursed in RCC.
```

**Excerpt context:**
```
...5 → 7 → 10 mg BID) is a defining feature — patients tolerating starting dose with normotension should escalate, as exposure correlates with efficacy. KEYNOTE-426 + JAVELIN-Renal-101 redefined 1L m...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 151/229: f-0535 - CRITICAL

**Entity:** `DRUG-BREXUCABTAGENE-AUTOLEUCEL`
**File:** `knowledge_base/hosted/content/drugs/brexucabtagene_autoleucel.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
ZUMA-2 (Wang 2020): r/r MCL after prior cBTKi (median 3 prior lines) — ORR 91%, CR 68%, 3-yr OS ~60%. First and only CAR-T approved for MCL. Higher Grade ≥3 ICANS in MCL setting (~31%) vs DLBCL (~28%) — MCL patients tend to be older + heavily pretreated. CD19-depletion manufacturing step distinguishes brexu-cel from axi-cel — needed due to leukemic-phase MCL contamination of apheresis. Centre must be FACT/JACIE/REMS-accredited. Tocilizumab on-site mandatory. Major UA access barrier: not registered.
```

**Excerpt context:**
```
...s brexu-cel from axi-cel — needed due to leukemic-phase MCL contamination of apheresis. Centre must be FACT/JACIE/REMS-accredited. Tocilizumab on-site mandatory. Major UA access barrier: not reg...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 152/229: f-0537 - CRITICAL

**Entity:** `DRUG-CAPECITABINE`
**File:** `knowledge_base/hosted/content/drugs/capecitabine.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
HFS prophylaxis: emollient creams (urea 10-20%), avoid friction and pressure on hands/feet, pre-emptive dose-hold at Grade 2 with resumption at lower dose. Renal dose adjustment is mandatory and often missed: CrCl 30-50 → 75% dose; CrCl <30 contraindicated. Hofheinz 2012 (rectal CRT): capecitabine non-inferior to infusional 5-FU with patient-friendlier oral schedule (no central line / pump). DPD deficiency screening (DPYD genotyping or uracilemia level) increasingly recommended pre-treatment in EU per EMA 2020 — pre-emptive dose adjustment for partial deficiency, contraindicated in complete deficiency. Warfarin INR monitoring weekly initially (CYP2C9 inhibition). Common combinations: CAPOX (capecitabine + oxaliplatin), CAPIRI / CAPEFOX, capecitabine + trastuzumab in HER2+ mBC, X-RT for rectal/gastric. UA: generic available, широко reimbursed under НСЗУ.
```

**Excerpt context:**
```
...tral line / pump). DPD deficiency screening (DPYD genotyping or uracilemia level) increasingly recommended pre-treatment in EU per EMA 2020 — pre-emptive dose adjustment for partial deficiency, contrai...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 153/229: f-0539 - CRITICAL

**Entity:** `DRUG-CAPECITABINE-BREAST`
**File:** `knowledge_base/hosted/content/drugs/capecitabine_breast.yaml`
**Field:** `notes`
**Matched pattern:** `Recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
Use DRUG-CAPECITABINE (created by GI agent for colorectal); this entry exists only to make the breast-builder script self-contained. Recommend deletion + reuse of cross-disease entry once both branches merge.
```

**Excerpt context:**
```
...gent for colorectal); this entry exists only to make the breast-builder script self-contained. Recommend deletion + reuse of cross-disease entry once both branches merge.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 154/229: f-0549 - CRITICAL

**Entity:** `DRUG-CIPROFLOXACIN`
**File:** `knowledge_base/hosted/content/drugs/ciprofloxacin.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Workhorse fluoroquinolone for Gram-negative + Pseudomonas. In oncology, the principal use is IV-to-PO step-down therapy after documented Gram-negative bacteremia / UTI / intra-abdominal infection responding to initial broad-spectrum, allowing earlier discharge. ALSO used for outpatient management of low-risk febrile neutropenia (MASCC score ≥21, no comorbidities, expected ANC recovery <7 days) with the IDSA-recommended ciprofloxacin + amoxicillin-clavulanate oral regimen. NOT used for FN prophylaxis — that role belongs to levofloxacin, which has better Gram-positive coverage (esp. viridans streptococci, a major mucositis-related bacteremia source). Class-wide FDA / EMA 2018 warning restricts fluoroquinolones to serious infections without alternatives — applies to ciprofloxacin. Polyvalent cation chelation is the most common cause of treatment failure with oral therapy — patient counselling critical. CYP1A2 inhibition causes major DDIs (tizanidine contraindicated; theophylline doubles). Ukraine: cheap, ubiquitous, NSZU-covered.
```

**Excerpt context:**
```
...e neutropenia (MASCC score ≥21, no comorbidities, expected ANC recovery <7 days) with the IDSA-recommended ciprofloxacin + amoxicillin-clavulanate oral regimen. NOT used for FN prophylaxis — that role...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 155/229: f-0563 - CRITICAL

**Entity:** `DRUG-ELACESTRANT`
**File:** `knowledge_base/hosted/content/drugs/elacestrant.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Indication: ESR1-mutant HR+/HER2- metastatic after at least one prior endocrine therapy. ESR1 mutation testing on ctDNA recommended pre-start.
```

**Excerpt context:**
```
...R+/HER2- metastatic after at least one prior endocrine therapy. ESR1 mutation testing on ctDNA recommended pre-start.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 156/229: f-0565 - CRITICAL

**Entity:** `DRUG-EPINEPHRINE`
**File:** `knowledge_base/hosted/content/drugs/epinephrine.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ABSOLUTE FIRST-LINE for anaphylaxis — no equivalent alternative. H1/H2 antihistamines (diphenhydramine, famotidine), corticosteroids (hydrocortisone, methylprednisolone), and bronchodilators are all ADJUNCTS, NOT replacements. Delay or omission of epinephrine in anaphylaxis is the leading modifiable cause of fatal outcome — give EARLY (within 5 min of recognition), give IM thigh (NOT SC, NOT deltoid), and REPEAT every 5-15 min if symptoms persist. Common pitfall in chemotherapy infusion reactions: treating with diphenhydramine + steroid alone while withholding epinephrine for "mild" symptoms — escalate immediately if hypotension, bronchospasm, or upper airway involvement. Patients on β-blockers who develop refractory anaphylaxis: add glucagon 1-5 mg IV bolus then 5-15 µg/min infusion (bypasses β-receptor block via intracellular cAMP elevation). Auto-injectors not widely available in Ukraine — emergency department / oncology day-unit protocols should pre-position 1 mg/mL ampules + syringes and drill the IM-thigh administration. Ukraine: registered, NSZU- covered, ubiquitous.
```

**Excerpt context:**
```
...injectors not widely available in Ukraine — emergency department / oncology day-unit protocols should pre-position 1 mg/mL ampules + syringes and drill the IM-thigh administration. Ukraine: regist...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 157/229: f-0570 - CRITICAL

**Entity:** `DRUG-5-FLUOROURACIL`
**File:** `knowledge_base/hosted/content/drugs/fluorouracil.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
DPYD genotyping (variants *2A, *13, c.2846A>T, HapB3) recommended before first dose per CPIC guidelines and EMA 2020 recommendation (NCCN colon v2.2025, pretreatment section). Bolus-only schedules largely superseded by infusional + LV in modern adjuvant. Coronary spasm: hold drug, urgent ECG; switch to raltitrexed if confirmed. Uridine triacetate (Vistogard) is the antidote for severe overdose or early-onset toxicity (≤96 h post-exposure).
```

**Excerpt context:**
```
DPYD genotyping (variants *2A, *13, c.2846A>T, HapB3) recommended before first dose per CPIC guidelines and EMA 2020 recommendation (NCCN colon v2.2025, pretrea...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 158/229: f-0583 - CRITICAL

**Entity:** `DRUG-IRINOTECAN`
**File:** `knowledge_base/hosted/content/drugs/irinotecan.yaml`
**Field:** `mechanism`
**Matched pattern:** `recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
Prodrug hydrolyzed by carboxylesterases to active metabolite SN-38 (~100-1000× more potent than parent). SN-38 stabilizes the topoisomerase-I/DNA cleavable complex, producing single-strand DNA breaks that become lethal double-strand breaks during S-phase replication. SN-38 is glucuronidated by UGT1A1 to inactive SN-38G; patients homozygous for UGT1A1*28 (Gilbert-syndrome variant) or *6 have impaired clearance and severe neutropenia + diarrhea risk — CPIC and FDA label both recommend testing before high-dose use.
```

**Excerpt context:**
```
...or *6 have impaired clearance and severe neutropenia + diarrhea risk — CPIC and FDA label both recommend testing before high-dose use.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 159/229: f-0584 - CRITICAL

**Entity:** `DRUG-IRINOTECAN`
**File:** `knowledge_base/hosted/content/drugs/irinotecan.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
UGT1A1 testing strongly recommended for FOLFIRINOX (intensive dose). Loperamide schedule: 4 mg at first loose stool then 2 mg q2h (q4h overnight) until 12 h diarrhea-free; consider octreotide (100-150 mcg SC TID, escalate to 500 mcg) for refractory diarrhea. Hospitalize for Grade 3-4 diarrhea + IV fluids + broad-spectrum antibiotics if febrile. Atropine 0.25-1 mg SC/IV for acute cholinergic syndrome (premedicate in patients with prior episodes).
```

**Excerpt context:**
```
UGT1A1 testing strongly recommended for FOLFIRINOX (intensive dose). Loperamide schedule: 4 mg at first loose stool then 2 mg q2h...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 160/229: f-0585 - CRITICAL

**Entity:** `DRUG-LEUCOVORIN`
**File:** `knowledge_base/hosted/content/drugs/leucovorin.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Most 5-FU regimens require leucovorin for activity modulation; doses are protocol-specific: Mayo Clinic (20 mg/m² IV bolus pre-5FU), Roswell Park (500 mg/m² IV 2-h infusion), de Gramont / FOLFOX / FOLFIRI (200-400 mg/m² IV 2-h infusion Day 1 ± Day 2). Levoleucovorin (l-isomer) is the active enantiomer; half the dose of racemic leucovorin (10 mg/m² Mayo equivalent). In high-dose methotrexate rescue: 15 mg PO/IV q6h starting 24 h post-MTX, continued until MTX level <0.05-0.1 µM (escalate dose if MTX clearance delayed). Critical safety point: leucovorin rescue dose must be matched to MTX level — under-rescue causes fatal MTX toxicity. UA: зареєстрований; НСЗУ-reimbursed for 5-FU modulation in CRC and as MTX rescue. Generic widely available.
```

**Excerpt context:**
```
...0.1 µM (escalate dose if MTX clearance delayed). Critical safety point: leucovorin rescue dose must be matched to MTX level — under-rescue causes fatal MTX toxicity. UA: зареєстрований; НСЗУ-rei...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 161/229: f-0594 - CRITICAL

**Entity:** `DRUG-MERCAPTOPURINE`
**File:** `knowledge_base/hosted/content/drugs/mercaptopurine.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Cornerstone of B-ALL maintenance (POMP regimen, 2-3 years post-induction- consolidation). TPMT and NUDT15 genotyping should be performed pre-initiation when available — poor metabolizers require dramatic dose reduction or alternative therapy. Take on empty stomach (food + dairy reduce absorption ~25%). Avoid allopurinol coadministration without dose reduction. Bedtime dosing improves tolerance.
```

**Excerpt context:**
```
...aintenance (POMP regimen, 2-3 years post-induction- consolidation). TPMT and NUDT15 genotyping should be performed pre-initiation when available — poor metabolizers require dramatic dose reduction...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 162/229: f-0597 - CRITICAL

**Entity:** `DRUG-METHOTREXATE`
**File:** `knowledge_base/hosted/content/drugs/methotrexate.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
HD-MTX (≥1 g/m²) protocol essentials: alkalinize urine to pH ≥7 (sodium bicarbonate IV); hydrate 3 L/m²/day starting 12 h pre-dose; monitor MTX levels at 24, 48, 72 h post-dose with target <0.1 µM at 72 h; continue leucovorin rescue (15 mg/m² IV q6h, escalate per nomogram if level elevated) until MTX <0.05 µM. Glucarpidase (Voraxaze) is the rescue agent for delayed clearance / AKI: rapidly hydrolyzes MTX to inactive metabolites. Pleural effusion / ascites must be fully drained before HD-MTX (third-spacing causes prolonged toxic exposure). Avoid TMP-SMX, NSAIDs, PPIs around HD-MTX dosing. Intrathecal MTX must use preservative-free formulation; leucovorin should NOT be given systemic- ically to rescue intrathecal MTX (it does not enter CSF in adequate concentration but can rescue systemic effects). For breast cancer, CMF largely supplanted by anthracycline + taxane regimens; retained for cardiac contraindication scenarios.
```

**Excerpt context:**
```
...ed clearance / AKI: rapidly hydrolyzes MTX to inactive metabolites. Pleural effusion / ascites must be fully drained before HD-MTX (third-spacing causes prolonged toxic exposure). Avoid TMP-SMX,...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 163/229: f-0598 - CRITICAL

**Entity:** `DRUG-METHOTREXATE`
**File:** `knowledge_base/hosted/content/drugs/methotrexate.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
HD-MTX (≥1 g/m²) protocol essentials: alkalinize urine to pH ≥7 (sodium bicarbonate IV); hydrate 3 L/m²/day starting 12 h pre-dose; monitor MTX levels at 24, 48, 72 h post-dose with target <0.1 µM at 72 h; continue leucovorin rescue (15 mg/m² IV q6h, escalate per nomogram if level elevated) until MTX <0.05 µM. Glucarpidase (Voraxaze) is the rescue agent for delayed clearance / AKI: rapidly hydrolyzes MTX to inactive metabolites. Pleural effusion / ascites must be fully drained before HD-MTX (third-spacing causes prolonged toxic exposure). Avoid TMP-SMX, NSAIDs, PPIs around HD-MTX dosing. Intrathecal MTX must use preservative-free formulation; leucovorin should NOT be given systemic- ically to rescue intrathecal MTX (it does not enter CSF in adequate concentration but can rescue systemic effects). For breast cancer, CMF largely supplanted by anthracycline + taxane regimens; retained for cardiac contraindication scenarios.
```

**Excerpt context:**
```
...s prolonged toxic exposure). Avoid TMP-SMX, NSAIDs, PPIs around HD-MTX dosing. Intrathecal MTX must use preservative-free formulation; leucovorin should NOT be given systemic- ically to rescue i...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 164/229: f-0599 - CRITICAL

**Entity:** `DRUG-METHOTREXATE`
**File:** `knowledge_base/hosted/content/drugs/methotrexate.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HD-MTX (≥1 g/m²) protocol essentials: alkalinize urine to pH ≥7 (sodium bicarbonate IV); hydrate 3 L/m²/day starting 12 h pre-dose; monitor MTX levels at 24, 48, 72 h post-dose with target <0.1 µM at 72 h; continue leucovorin rescue (15 mg/m² IV q6h, escalate per nomogram if level elevated) until MTX <0.05 µM. Glucarpidase (Voraxaze) is the rescue agent for delayed clearance / AKI: rapidly hydrolyzes MTX to inactive metabolites. Pleural effusion / ascites must be fully drained before HD-MTX (third-spacing causes prolonged toxic exposure). Avoid TMP-SMX, NSAIDs, PPIs around HD-MTX dosing. Intrathecal MTX must use preservative-free formulation; leucovorin should NOT be given systemic- ically to rescue intrathecal MTX (it does not enter CSF in adequate concentration but can rescue systemic effects). For breast cancer, CMF largely supplanted by anthracycline + taxane regimens; retained for cardiac contraindication scenarios.
```

**Excerpt context:**
```
...PPIs around HD-MTX dosing. Intrathecal MTX must use preservative-free formulation; leucovorin should NOT be given systemic- ically to rescue intrathecal MTX (it does not enter CSF in adequate con...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 165/229: f-0601 - CRITICAL

**Entity:** `DRUG-METHYLPREDNISOLONE`
**File:** `knowledge_base/hosted/content/drugs/methylprednisolone.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Workhorse corticosteroid for: (1) acute infusion reactions and anaphylaxis adjunct (40-125 mg IV after epinephrine); (2) immune- related adverse events from checkpoint inhibitors — the defining role; (3) CRS escalation when tocilizumab inadequate. Compared to hydrocortisone: more potent per mg (4-5×), longer duration, less mineralocorticoid effect (preferred when fluid retention undesirable). Compared to dexamethasone: slightly less potent (×6), shorter duration, but lower CNS penetration (slightly less psychiatric AE per equivalent dose); dex preferred for cerebral edema and antiemesis, methylprednisolone preferred for irAE management per NCCN / ESMO immunotherapy toxicity guidelines. CRITICAL: high-dose pulse (≥250 mg IV) must be infused over ≥30 min — rapid bolus risks fatal cardiac arrhythmia. Aprepitant DDI: aprepitant increases methylprednisolone exposure ~2.5× — reduce methylprednisolone ~50% when both prescribed (e.g., in HEC chemotherapy with antiemetic regimen). Single bolus of 40-125 mg has minimal long-term consequences; courses ≥2 weeks require taper to prevent adrenal crisis. Long-acting Depo-Medrol IM is for joint injections only — never for systemic IV use. Ukraine: NSZU-covered; widely available.
```

**Excerpt context:**
```
...ment per NCCN / ESMO immunotherapy toxicity guidelines. CRITICAL: high-dose pulse (≥250 mg IV) must be infused over ≥30 min — rapid bolus risks fatal cardiac arrhythmia. Aprepitant DDI: aprepita...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 166/229: f-0618 - CRITICAL

**Entity:** `DRUG-POLATUZUMAB-VEDOTIN`
**File:** `knowledge_base/hosted/content/drugs/polatuzumab_vedotin.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Replaces vincristine in Pola-R-CHP regimen for newly-diagnosed DLBCL with IPI ≥2 (POLARIX trial — improved PFS vs R-CHOP). Substantial cost + access constraint in Ukraine: NOT НСЗУ-reimbursed as of 2026-04-25 — funding pathway must be confirmed BEFORE plan finalization (clinical trial / charitable scheme / out-of-pocket). Premedication: antihistamine + paracetamol for first dose (infusion-related reactions). Hold for Grade ≥2 peripheral neuropathy.
```

**Excerpt context:**
```
...al cost + access constraint in Ukraine: NOT НСЗУ-reimbursed as of 2026-04-25 — funding pathway must be confirmed BEFORE plan finalization (clinical trial / charitable scheme / out-of-pocket). Pr...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 167/229: f-0620 - CRITICAL

**Entity:** `DRUG-PROCARBAZINE`
**File:** `knowledge_base/hosted/content/drugs/procarbazine.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Patient counseling on MAOI diet (avoid aged cheese, cured/smoked meats, fermented soy, broad beans, tap beer, draft wine, marmite) is mandatory and must be documented at every cycle. Avoid all SSRIs (fluoxetine, sertraline) and decongestants for 2 weeks after last dose. R-MPV (PCNSL) and BEACOPP-escalated (Hodgkin advanced-stage IPI≥3) are the principal modern uses; both are restricted to specialist centers in UA. AML risk is the dominant late toxicity in Hodgkin survivors and a key reason ABVD remains preferred over BEACOPP in early-stage / lower-IPI disease.
```

**Excerpt context:**
```
...ured/smoked meats, fermented soy, broad beans, tap beer, draft wine, marmite) is mandatory and must be documented at every cycle. Avoid all SSRIs (fluoxetine, sertraline) and decongestants for 2...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 168/229: f-0631 - CRITICAL

**Entity:** `DRUG-THIOTEPA`
**File:** `knowledge_base/hosted/content/drugs/thiotepa.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
In MATRix the thiotepa component is what enhances CNS penetration and drives the regimen's superior CR rate vs MTR (Ferreri IELSG32 trial, Lancet Haematol 2016). For CNS-relapse-risk lymphomas autoSCT, TBC (thiotepa + busulfan + cyclophosphamide) and TT-BCNU are preferred over BEAM (Soussain 2008; Cordoba/MSKCC retrospective). Drug is excreted in sweat — patient must shower BID and change linens during HD therapy to avoid contact dermatitis (caregivers also). Defibrotide prophylaxis considered for high-VOD-risk patients (prior abdominal RT, baseline hepatic dysfunction). Intrathecal use largely supplanted by IT-MTX + IT-cytarabine but retained in select pediatric protocols.
```

**Excerpt context:**
```
...ed over BEAM (Soussain 2008; Cordoba/MSKCC retrospective). Drug is excreted in sweat — patient must shower BID and change linens during HD therapy to avoid contact dermatitis (caregivers also)....

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 169/229: f-0636 - CRITICAL

**Entity:** `DRUG-TOPOTECAN`
**File:** `knowledge_base/hosted/content/drugs/topotecan.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Renal dose adjustment is mandatory and frequently overlooked — CrCl 20-39 requires 50% dose reduction; CrCl <20 not recommended. Weekly schedule (4 mg/m² Days 1, 8, 15) is better tolerated than the 5-day continuous schedule in older / pretreated patients — cross-trial efficacy comparable in ovarian salvage. Oral formulation has more diarrhea, less neutropenia; convenient for outpatient use but logistics of oral cytotoxic handling apply (PPE for caregivers, avoid pregnancy / breastfeeding contact). Vesicant on extravasation — administer through central or large peripheral vein; have extravasation kit available. G-CSF support after first febrile neutropenia event. Baseline + serial CBC weekly. Premedicate with 5-HT3 antagonist + dexamethasone for nausea. UA: generic, available, НСЗУ-reimbursed for indicated uses.
```

**Excerpt context:**
```
...is mandatory and frequently overlooked — CrCl 20-39 requires 50% dose reduction; CrCl <20 not recommended. Weekly schedule (4 mg/m² Days 1, 8, 15) is better tolerated than the 5-day continuous schedul...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 170/229: f-0648 - CRITICAL

**Entity:** `RF-AML-CORE-BINDING-FACTOR-FAVORABLE`
**File:** `knowledge_base/hosted/content/redflags/rf_aml_core_binding_factor_favorable.yaml`
**Field:** `definition`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
AML with core-binding-factor (CBF) cytogenetics: t(8;21)(q22;q22.1) with RUNX1::RUNX1T1 fusion OR inv(16)(p13.1q22) / t(16;16)(p13.1;q22) with CBFB::MYH11 fusion. ~10-15% of de novo adult AML, ~25% of pediatric AML. ELN 2022 favorable risk; standard 7+3 induction + 3-4 cycles HiDAC consolidation is curative-intent in CR1 (5-year OS 60-75%); upfront alloHCT is NOT recommended in CR1 default. Adding gemtuzumab ozogamicin to induction (ALFA-0701, AML-19) further improves OS specifically in CBF AML (HR 0.69). c-KIT mutations (D816, exon-8) co-occur in ~25% of CBF AML and may downgrade favorability — warrant MRD-directed approach.
```

**Excerpt context:**
```
...ycles HiDAC consolidation is curative-intent in CR1 (5-year OS 60-75%); upfront alloHCT is NOT recommended in CR1 default. Adding gemtuzumab ozogamicin to induction (ALFA-0701, AML-19) further improves...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 171/229: f-0653 - CRITICAL

**Entity:** `RF-APL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_apl_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
APL patient with positive HBV / HCV / HIV serology, latent TB, or active uncontrolled infection — needs antiviral prophylaxis before initiating consolidation; ATRA initiation should NOT wait for these results
```

**Excerpt context:**
```
...olled infection — needs antiviral prophylaxis before initiating consolidation; ATRA initiation should NOT wait for these results

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 172/229: f-0654 - CRITICAL

**Entity:** `RF-APL-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_apl_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Direction "investigate" — surfaces a monitoring annotation rather than shifting indication. Triggers immediate dexamethasone 10 mg IV BID, consideration of temporary ATRA/ATO hold (per severity), aggressive diuresis, ICU monitoring. Prophylactic steroids (prednisone 0.5 mg/kg or dexamethasone 2.5 mg/m² BID) are recommended for high-risk (WBC >10) and any patient with rising WBC during induction. DS occurs in ~5-25% and is a leading cause of induction mortality if not promptly recognized. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...CU monitoring. Prophylactic steroids (prednisone 0.5 mg/kg or dexamethasone 2.5 mg/m² BID) are recommended for high-risk (WBC >10) and any patient with rising WBC during induction. DS occurs in ~5-25%...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 173/229: f-0663 - CRITICAL

**Entity:** `RF-BREAST-AKT1-E17K-ACTIONABLE`
**File:** `knowledge_base/hosted/content/redflags/rf_breast_akt1_e17k_actionable.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
AKT1 E17K is the dominant (>90%) AKT1 hotspot. Tested via tissue NGS or ctDNA. Capivasertib hyperglycemia rate lower than alpelisib. Toxicity: diarrhea (70%), rash (35%), hyperglycemia (~16%). Concurrent PIK3CA / AKT1 / PTEN testing recommended at first progression on AI ± CDK4/6i — any single alteration triggers pathway-targeted therapy.
```

**Excerpt context:**
```
...ity: diarrhea (70%), rash (35%), hyperglycemia (~16%). Concurrent PIK3CA / AKT1 / PTEN testing recommended at first progression on AI ± CDK4/6i — any single alteration triggers pathway-targeted therapy...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 174/229: f-0665 - CRITICAL

**Entity:** `RF-BREAST-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_breast_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Geriatric assessment (G8 / CGA) recommended pre-treatment for ≥70. HR+ disease in frail elderly may be managed with endocrine therapy alone (favorable risk-benefit). HER2+: trastuzumab + paclitaxel weekly or T-DM1 monotherapy alternatives. TNBC: weekly paclitaxel or capecitabine.
```

**Excerpt context:**
```
Geriatric assessment (G8 / CGA) recommended pre-treatment for ≥70. HR+ disease in frail elderly may be managed with endocrine therapy alon...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 175/229: f-0667 - CRITICAL

**Entity:** `RF-BREAST-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_breast_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Cross-disease HBV reactivation handled by RF-UNIVERSAL-HBV-REACTIVATION- RISK. DPYD deficiency screening unique to fluoropyrimidine-containing regimens; severe / fatal toxicity in homozygous deficient patients — EU/EMA-recommended pre-test.
```

**Excerpt context:**
```
...imidine-containing regimens; severe / fatal toxicity in homozygous deficient patients — EU/EMA-recommended pre-test.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 176/229: f-0670 - CRITICAL

**Entity:** `RF-BURKITT-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_burkitt_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
Burkitt is curable but cure rates collapse from 80-90% (young fit) to 20-40% (>65 frail) on full-intensity regimens — toxicity-driven treatment-related mortality is the dominant driver. NCCN B-Cell recommends DA-EPOCH-R (preferred over CODOX-M/IVAC) for fit elderly and modified DA-EPOCH-R or R-CHOP-like for frail. TLS prophylaxis mandatory regardless of dose intensity (rasburicase preferred over allopurinol given high TLS risk in Burkitt).
```

**Excerpt context:**
```
...ity regimens — toxicity-driven treatment-related mortality is the dominant driver. NCCN B-Cell recommends DA-EPOCH-R (preferred over CODOX-M/IVAC) for fit elderly and modified DA-EPOCH-R or R-CHOP-lik...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 177/229: f-0673 - CRITICAL

**Entity:** `RF-BURKITT-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_burkitt_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Active or latent infection requiring resolution / prophylaxis before initiating DA-EPOCH-R or CODOX-M/IVAC in Burkitt: HBsAg-positive (mandatory anti-CD20 → high HBV reactivation risk), anti-HBc-positive (occult HBV), HCV-RNA-positive, HIV-positive (high prevalence in Burkitt — endemic and sporadic), or active TB. EBV testing recommended (endemic Burkitt EBV-driven; informs prognostication).
```

**Excerpt context:**
```
...e, HIV-positive (high prevalence in Burkitt — endemic and sporadic), or active TB. EBV testing recommended (endemic Burkitt EBV-driven; informs prognostication).

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 178/229: f-0677 - CRITICAL

**Entity:** `RF-CERVICAL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_cervical_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Active or unmanaged infection requiring resolution before initiating cisplatin-based chemoradiation in cervical cancer: HIV-positive (HPV-driven disease — almost universal HIV testing recommended; CD4 informs cisplatin dosing and pelvic-RT field tolerance), HBV-positive (reactivation risk on prolonged chemoradiation), active pelvic abscess / pyometra (must drain before RT), or active TB.
```

**Excerpt context:**
```
...BV-positive (reactivation risk on prolonged chemoradiation), active pelvic abscess / pyometra (must drain before RT), or active TB.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 179/229: f-0678 - CRITICAL

**Entity:** `RF-CERVICAL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_cervical_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Active or unmanaged infection requiring resolution before initiating cisplatin-based chemoradiation in cervical cancer: HIV-positive (HPV-driven disease — almost universal HIV testing recommended; CD4 informs cisplatin dosing and pelvic-RT field tolerance), HBV-positive (reactivation risk on prolonged chemoradiation), active pelvic abscess / pyometra (must drain before RT), or active TB.
```

**Excerpt context:**
```
...oradiation in cervical cancer: HIV-positive (HPV-driven disease — almost universal HIV testing recommended; CD4 informs cisplatin dosing and pelvic-RT field tolerance), HBV-positive (reactivation risk...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 180/229: f-0679 - CRITICAL

**Entity:** `RF-CERVICAL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_cervical_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
HIV testing recommended for all cervical cancer patients per NCCN (HPV / HIV co-infection extremely common). HIV+ patients tolerate cisplatin-CRT with ART optimization; CD4 <200 is relative contraindication — coordinate with HIV clinic. HBV+: entecavir/tenofovir prophylaxis during prolonged chemo phases. Pelvic abscess / pyometra: percutaneous drainage / antibiotics first; RT into infected field worsens necrosis. This RF surfaces workup-prerequisites; engine does not switch indication.
```

**Excerpt context:**
```
HIV testing recommended for all cervical cancer patients per NCCN (HPV / HIV co-infection extremely common). HIV+ pati...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 181/229: f-0682 - CRITICAL

**Entity:** `RF-CHL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_chl_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
HBsAg+ → entecavir or tenofovir prophylaxis throughout chemo + 6-12 mo post (particularly important if escalated BEACOPP — prolonged steroid + alkylator load). HIV+ cHL: continue ART, full-dose ABVD (or A+AVD if fit) — outcomes approach HIV-negative cHL; avoid BEACOPP in HIV (excess toxicity). Active TB: full anti-TB course before chemo when feasible. PJP prophylaxis (TMP-SMX) not routine on ABVD but recommended on BEACOPP-escalated. EBV detectable ~30-40% cHL — informative not actionable for treatment selection.
```

**Excerpt context:**
```
...l anti-TB course before chemo when feasible. PJP prophylaxis (TMP-SMX) not routine on ABVD but recommended on BEACOPP-escalated. EBV detectable ~30-40% cHL — informative not actionable for treatment se...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 182/229: f-0685 - CRITICAL

**Entity:** `RF-CHOLANGIOCARCINOMA-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_cholangiocarcinoma_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
TOPAZ-1 (gem-cis-durvalumab) and KEYNOTE-966 (gem-cis-pembrolizumab) enrolled mostly ECOG 0–1 fit patients; older / frail patients have higher rates of gem-cis-related thrombocytopenia, neutropenia, and decompensated cholestasis. Geriatric assessment (G8) recommended ≥70. In frail patients with adequate biliary drainage, gem-cis doublet (ABC-02 doublet) remains acceptable; gem monotherapy or capecitabine for very frail. Source gap: NCCN Hepatobiliary / ESMO Biliary Tract Cancer guideline not yet ingested as a separate Source entity — using SRC-NCCN-HCC-2025 (adjacent hepatobiliary reference per disease YAML precedent) and SRC-ONCOKB until biliary-specific Source is added.
```

**Excerpt context:**
```
...elated thrombocytopenia, neutropenia, and decompensated cholestasis. Geriatric assessment (G8) recommended ≥70. In frail patients with adequate biliary drainage, gem-cis doublet (ABC-02 doublet) remain...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 183/229: f-0691 - CRITICAL

**Entity:** `RF-CLL-HIGH-RISK`
**File:** `knowledge_base/hosted/content/redflags/rf_cll_high_risk.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Triggers preference for fixed-duration venetoclax+obinutuzumab (CLL14) over BTKi continuous in some patient profiles, AND absolutely contraindicates chemoimmunotherapy (FCR/BR). High-risk CLL must NEVER receive chemoimmuno 1L — survival impact substantial.
```

**Excerpt context:**
```
...me patient profiles, AND absolutely contraindicates chemoimmunotherapy (FCR/BR). High-risk CLL must NEVER receive chemoimmuno 1L — survival impact substantial.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 184/229: f-0692 - CRITICAL

**Entity:** `RF-CLL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_cll_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
Obinutuzumab (CLL14) is potent B-cell depleter — HBV reactivation risk among the highest of all CD20 antibodies. Mandatory entecavir / tenofovir prophylaxis from –7d through +12mo (some recommend +18-24mo given extended B-cell aplasia). HCV+: defer DAA cure pre-treatment if feasible; concurrent ledipasvir/sofosbuvir + venetoclax has CYP3A4 drug interactions — coordinate. Hypogamma + recurrent serious infection: IVIG 0.4 g/kg q3-4 weeks (per ESMO CLL §infection management). PJP prophylaxis routine on bendamustine, fludarabine, idelalisib; not routine on BTKi/V+O alone.
```

**Excerpt context:**
```
...all CD20 antibodies. Mandatory entecavir / tenofovir prophylaxis from –7d through +12mo (some recommend +18-24mo given extended B-cell aplasia). HCV+: defer DAA cure pre-treatment if feasible; concu...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 185/229: f-0702 - CRITICAL

**Entity:** `RF-CML-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_cml_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Direction "investigate" — surfaces a workup-prerequisite annotation. CML TKI-related HBV reactivation is rare but reported (especially with immunosuppression-dose TKI shifts and post-TFR discontinuation). HBV testing recommended before initiating any TKI per ELN 2020 + NCCN. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...(especially with immunosuppression-dose TKI shifts and post-TFR discontinuation). HBV testing recommended before initiating any TKI per ELN 2020 + NCCN. STUB — requires clinical co-lead signoff.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 186/229: f-0708 - CRITICAL

**Entity:** `RF-DLBCL-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_dlbcl_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
HBsAg+ → mandatory entecavir or tenofovir prophylaxis from –7d through +12mo post-last-anti-CD20 (NCCN B-Cell §HBV-1; ESMO DLBCL §pre-treatment). HIV+ DLBCL is treatable with R-CHOP or DA-EPOCH-R but requires concomitant ART — use the existing IND-DLBCL-1L-RCHOP, but the clinical team must confirm ART regimen and CD4 baseline first. Active TB: full anti-TB course before chemoimmunotherapy when feasible. This RF surfaces the hold; the algorithm engages ALGO-DLBCL-1L step 1 to defer indication selection until prophylaxis/ART/anti-TB pathway is documented.
```

**Excerpt context:**
```
...CH-R but requires concomitant ART — use the existing IND-DLBCL-1L-RCHOP, but the clinical team must confirm ART regimen and CD4 baseline first. Active TB: full anti-TB course before chemoimmunot...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 187/229: f-0711 - CRITICAL

**Entity:** `RF-DLBCL-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_dlbcl_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Closes the 5-type matrix gap for DLBCL-NOS (REDFLAG_AUTHORING_GUIDE §2 — every disease should have a transformation-progression entry).
The clinical concept differs from indolent-lymphoma transformation (FL → DLBCL or CLL → DLBCL Richter): DLBCL is already aggressive at baseline, so "transformation" here means either (a) response failure to first-line standard regimens, or (b) histologic re-classification to an even more aggressive entity (HGBL with MYC + BCL2/BCL6 rearrangements, or Burkitt-like) on re-biopsy at relapse.
Operationally drives: - CAR-T eligibility assessment (axi-cel / liso-cel / tisagenlecleucel
  per FDA/EMA labels for r/r DLBCL ≥2L; ZUMA-7 / TRANSFORM /
  BELINDA support 2L use in early-relapse / refractory disease)
- Salvage chemo (R-DHAP / R-ICE) + autoSCT for chemo-sensitive
  relapse > 12 months
- Bispecific antibodies (epcoritamab, glofitamab) in CAR-T-ineligible
  or post-CAR-T relapse
- Pola-BR for transplant-ineligible or post-CAR-T
STUB — content reflects standard 2026 practice; clinical reviewer must confirm the trigger thresholds (especially the "primary refractory" definition, which varies between SCHOLAR-1 and FDA-label conventions) before this RedFlag is wired into ALGO-DLBCL-2L decision_tree.
reviewer_signoffs: 0
```

**Excerpt context:**
```
Closes the 5-type matrix gap for DLBCL-NOS (REDFLAG_AUTHORING_GUIDE §2 — every disease should have a transformation-progression entry). The clinical concept differs from indolent-lymphoma...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 188/229: f-0712 - CRITICAL

**Entity:** `RF-DLBCL-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_dlbcl_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Closes the 5-type matrix gap for DLBCL-NOS (REDFLAG_AUTHORING_GUIDE §2 — every disease should have a transformation-progression entry).
The clinical concept differs from indolent-lymphoma transformation (FL → DLBCL or CLL → DLBCL Richter): DLBCL is already aggressive at baseline, so "transformation" here means either (a) response failure to first-line standard regimens, or (b) histologic re-classification to an even more aggressive entity (HGBL with MYC + BCL2/BCL6 rearrangements, or Burkitt-like) on re-biopsy at relapse.
Operationally drives: - CAR-T eligibility assessment (axi-cel / liso-cel / tisagenlecleucel
  per FDA/EMA labels for r/r DLBCL ≥2L; ZUMA-7 / TRANSFORM /
  BELINDA support 2L use in early-relapse / refractory disease)
- Salvage chemo (R-DHAP / R-ICE) + autoSCT for chemo-sensitive
  relapse > 12 months
- Bispecific antibodies (epcoritamab, glofitamab) in CAR-T-ineligible
  or post-CAR-T relapse
- Pola-BR for transplant-ineligible or post-CAR-T
STUB — content reflects standard 2026 practice; clinical reviewer must confirm the trigger thresholds (especially the "primary refractory" definition, which varies between SCHOLAR-1 and FDA-label conventions) before this RedFlag is wired into ALGO-DLBCL-2L decision_tree.
reviewer_signoffs: 0
```

**Excerpt context:**
```
...ant-ineligible or post-CAR-T STUB — content reflects standard 2026 practice; clinical reviewer must confirm the trigger thresholds (especially the "primary refractory" definition, which varies b...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 189/229: f-0713 - CRITICAL

**Entity:** `RF-EATL-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_eatl_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Refractory EATL has dismal prognosis; clinical trial referral is the recommended next step.
```

**Excerpt context:**
```
Refractory EATL has dismal prognosis; clinical trial referral is the recommended next step.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 190/229: f-0723 - CRITICAL

**Entity:** `RF-GELF-LOW-BURDEN`
**File:** `knowledge_base/hosted/content/redflags/rf_gelf_low_burden.yaml`
**Field:** `notes`
**Matched pattern:** `recommend`
**Pattern class:** direct recommendation verb

**Current value:**
```
Low-burden FL (no GELF criterion) is the canonical watch-and-wait population. RESORT (E4402, Kahl 2014) showed rituximab-monotherapy did not improve OS over observation; Ardeshna 2014 showed similar. ESMO FL 2024 / NCCN B-cell 2025 recommend observation as first approach for stage III-IV asymptomatic low-burden FL; rituximab monotherapy is acceptable when patient prefers active intervention and meets shared-decision threshold. de-escalate direction routes away from chemoimmunotherapy.
```

**Excerpt context:**
```
...not improve OS over observation; Ardeshna 2014 showed similar. ESMO FL 2024 / NCCN B-cell 2025 recommend observation as first approach for stage III-IV asymptomatic low-burden FL; rituximab monothera...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 191/229: f-0725 - CRITICAL

**Entity:** `RF-GIST-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_gist_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Imatinib is generally well-tolerated in elderly but cumulative fluid retention, periorbital edema, and hepatotoxicity are more frequent. Sunitinib (2L) carries significant cardiotoxicity, hypertension, hand-foot syndrome — geriatric patients at higher risk; regorafenib (3L) similar concerns. Adjuvant imatinib durations (3 vs 6 yr) should be individualized in elderly: SSG-XXII / PERSIST-5 data on extended duration enrolled fewer patients ≥70. Source-gap caveat: NCCN GIST / ESMO Sarcoma not yet ingested — using NCCN-MELANOMA-2025 (adjacent KIT-pathway reference per disease YAML precedent) and SRC-ONCOKB.
```

**Excerpt context:**
```
...nts at higher risk; regorafenib (3L) similar concerns. Adjuvant imatinib durations (3 vs 6 yr) should be individualized in elderly: SSG-XXII / PERSIST-5 data on extended duration enrolled fewer pa...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 192/229: f-0732 - CRITICAL

**Entity:** `RF-HBV-COINFECTION`
**File:** `knowledge_base/hosted/content/redflags/rf_hbv_coinfection.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HBV co-infection in HCV-MZL patients triggers MDT-brief annotation recommending HBV-prophylaxis (entecavir or TDF) before any anti-CD20 exposure. Reactivation rates without prophylaxis: ~50% in HBsAg+, 5-10% in anti-HBc+ (occult HBV). Algorithm choice between ANTIVIRAL and BR-AGGRESSIVE arms is not affected — both arms can proceed with HBV prophylaxis in parallel.
The cross-disease/universal HBV reactivation handling (HBsAg+, anti-HBc+, HBV-DNA detectable) is consolidated into RF-UNIVERSAL-HBV-REACTIVATION-RISK. This disease-specific entry kept for backwards compatibility with existing HCV-MZL plans; new diseases should rely on the universal flag instead.
```

**Excerpt context:**
```
...ease-specific entry kept for backwards compatibility with existing HCV-MZL plans; new diseases should rely on the universal flag instead.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 193/229: f-0733 - CRITICAL

**Entity:** `RF-HBV-COINFECTION`
**File:** `knowledge_base/hosted/content/redflags/rf_hbv_coinfection.yaml`
**Field:** `notes`
**Matched pattern:** `recommending`
**Pattern class:** direct recommendation verb

**Current value:**
```
HBV co-infection in HCV-MZL patients triggers MDT-brief annotation recommending HBV-prophylaxis (entecavir or TDF) before any anti-CD20 exposure. Reactivation rates without prophylaxis: ~50% in HBsAg+, 5-10% in anti-HBc+ (occult HBV). Algorithm choice between ANTIVIRAL and BR-AGGRESSIVE arms is not affected — both arms can proceed with HBV prophylaxis in parallel.
The cross-disease/universal HBV reactivation handling (HBsAg+, anti-HBc+, HBV-DNA detectable) is consolidated into RF-UNIVERSAL-HBV-REACTIVATION-RISK. This disease-specific entry kept for backwards compatibility with existing HCV-MZL plans; new diseases should rely on the universal flag instead.
```

**Excerpt context:**
```
HBV co-infection in HCV-MZL patients triggers MDT-brief annotation recommending HBV-prophylaxis (entecavir or TDF) before any anti-CD20 exposure. Reactivation rates without p...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 194/229: f-0738 - CRITICAL

**Entity:** `RF-HCV-MZL-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_hcv_mzl_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `patients should`
**Pattern class:** patient-directed imperative

**Current value:**
```
HCV-MZL is typically indolent and DAA-responsive — antiviral therapy alone (DAA: glecaprevir/pibrentasvir or sofosbuvir/velpatasvir) produces ~75% lymphoma response when achieved viral cure (Arcaini 2014). Frail patients should preferentially receive DAA-only with watch-and-wait for the lymphoma; reserve immunochemotherapy (R-bendamustine, R-CVP) for symptomatic / progressive disease after SVR. Bendamustine in elderly: high infection risk, monitor lymphocyte recovery + add PJP prophylaxis. Cirrhotic + frail: prefer rituximab- monotherapy. Geriatric assessment recommended.
```

**Excerpt context:**
```
...ir/velpatasvir) produces ~75% lymphoma response when achieved viral cure (Arcaini 2014). Frail patients should preferentially receive DAA-only with watch-and-wait for the lymphoma; reserve immunochemothera...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 195/229: f-0739 - CRITICAL

**Entity:** `RF-HCV-MZL-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_hcv_mzl_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HCV-MZL is typically indolent and DAA-responsive — antiviral therapy alone (DAA: glecaprevir/pibrentasvir or sofosbuvir/velpatasvir) produces ~75% lymphoma response when achieved viral cure (Arcaini 2014). Frail patients should preferentially receive DAA-only with watch-and-wait for the lymphoma; reserve immunochemotherapy (R-bendamustine, R-CVP) for symptomatic / progressive disease after SVR. Bendamustine in elderly: high infection risk, monitor lymphocyte recovery + add PJP prophylaxis. Cirrhotic + frail: prefer rituximab- monotherapy. Geriatric assessment recommended.
```

**Excerpt context:**
```
...asvir) produces ~75% lymphoma response when achieved viral cure (Arcaini 2014). Frail patients should preferentially receive DAA-only with watch-and-wait for the lymphoma; reserve immunochemothera...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 196/229: f-0740 - CRITICAL

**Entity:** `RF-HCV-MZL-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_hcv_mzl_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
HCV-MZL is typically indolent and DAA-responsive — antiviral therapy alone (DAA: glecaprevir/pibrentasvir or sofosbuvir/velpatasvir) produces ~75% lymphoma response when achieved viral cure (Arcaini 2014). Frail patients should preferentially receive DAA-only with watch-and-wait for the lymphoma; reserve immunochemotherapy (R-bendamustine, R-CVP) for symptomatic / progressive disease after SVR. Bendamustine in elderly: high infection risk, monitor lymphocyte recovery + add PJP prophylaxis. Cirrhotic + frail: prefer rituximab- monotherapy. Geriatric assessment recommended.
```

**Excerpt context:**
```
...+ add PJP prophylaxis. Cirrhotic + frail: prefer rituximab- monotherapy. Geriatric assessment recommended.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 197/229: f-0742 - CRITICAL

**Entity:** `RF-HGBL-DH-CNS-PROPHYLAXIS-TRIGGER`
**File:** `knowledge_base/hosted/content/redflags/rf_hgbl_dh_cns_prophylaxis_trigger.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Per NCCN B-cell v.X.2025 HGBL section: CNS prophylaxis recommended for all HGBL-DH/TH regardless of CNS-IPI score (biology-driven); typical approach HD-MTX 3-3.5 g/m² IV intercalated with DA-EPOCH-R cycles. Direction INVESTIGATE because RF doesn't shift main regimen — adds CNS-directed therapy as plan particularity. shifts_algorithm:[] per REDFLAG_AUTHORING_GUIDE §4 rule 2. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
Per NCCN B-cell v.X.2025 HGBL section: CNS prophylaxis recommended for all HGBL-DH/TH regardless of CNS-IPI score (biology-driven); typical approach HD-MTX 3-3.5...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 198/229: f-0747 - CRITICAL

**Entity:** `RF-HGBL-DH-ORGAN-DYSFUNCTION`
**File:** `knowledge_base/hosted/content/redflags/rf_hgbl_dh_organ_dysfunction.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
DA-EPOCH-R cumulative doxorubicin exceeds R-CHOP; cardio-monitoring should be aggressive in baseline-borderline LVEF. Indication-level dose adjustment, not 1L Algorithm shift.
```

**Excerpt context:**
```
DA-EPOCH-R cumulative doxorubicin exceeds R-CHOP; cardio-monitoring should be aggressive in baseline-borderline LVEF. Indication-level dose adjustment, not 1L Algorithm...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 199/229: f-0749 - CRITICAL

**Entity:** `RF-HNSCC-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_hnscc_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
HNSCC patients are disproportionately tobacco / alcohol users with cardiopulmonary comorbidity and pre-treatment malnutrition. High-dose 3-weekly cisplatin (100 mg/m²) yields high renal / ototoxicity rates in elderly — Bonner cetuximab + RT (mAB-targeted) remains an option for cisplatin-ineligible. RTOG 1016 / De-ESCALaTE showed cetuximab + RT inferior to cisplatin + RT for HPV+ disease, so de-escalation should be cisplatin-ineligibility-driven, not HPV-driven. Pre-treatment swallowing evaluation, gastrostomy consideration, and dental clearance are mandatory in frail patients. Source-gap caveat: NCCN H&N / ESMO H&N not yet ingested as separate Source entities — using SRC-NCCN-NSCLC-2025 (adjacent thoracic / squamous reference per disease YAML precedent) and SRC-ONCOKB.
```

**Excerpt context:**
```
...e-ESCALaTE showed cetuximab + RT inferior to cisplatin + RT for HPV+ disease, so de-escalation should be cisplatin-ineligibility-driven, not HPV-driven. Pre-treatment swallowing evaluation, gastro...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 200/229: f-0761 - CRITICAL

**Entity:** `RF-MDS-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_mds_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Direction "hold" surfaces a workup prerequisite. HBV testing mandatory pre-HMA. HMA-induced cytopenias prolong infection windows; pre-existing infections must be controlled before initiation. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...g mandatory pre-HMA. HMA-induced cytopenias prolong infection windows; pre-existing infections must be controlled before initiation. STUB — requires clinical co-lead signoff.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 201/229: f-0762 - CRITICAL

**Entity:** `RF-MDS-TP53-MUTATION`
**File:** `knowledge_base/hosted/content/redflags/rf_mds_tp53_mutation.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
TP53-mutated MDS is its own WHO 5th-edition entity with median OS ~6-9 months on standard HMA. AlloHCT carries higher relapse risk vs TP53-wt. Active research questions: ven+aza vs aza alone, magrolimab + aza (failed phase-3 ENHANCE), eprenetapopt + aza (mixed results). NOT clear best regimen — flagged as intensify but the algorithm should also surface palliative-intent option. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...etapopt + aza (mixed results). NOT clear best regimen — flagged as intensify but the algorithm should also surface palliative-intent option. STUB — requires clinical co-lead signoff.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 202/229: f-0766 - CRITICAL

**Entity:** `RF-MF-SEZARY-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_mf_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Active or latent infection requiring resolution / prophylaxis before initiating systemic MF/Sézary therapy: HBsAg-positive (HBV reactivation risk on prolonged systemic therapy with steroid co-medication), anti-HBc-positive (occult HBV), HCV-RNA-positive, HIV-positive (HTLV-1 in differential — must distinguish from ATLL — see DIS-ATLL workup pathway), HTLV-1-positive (reclassify as ATLL), or active skin superinfection (MF skin disease frequently superinfected with S. aureus — antibiotics before topical/systemic intensification).
```

**Excerpt context:**
```
...ion), anti-HBc-positive (occult HBV), HCV-RNA-positive, HIV-positive (HTLV-1 in differential — must distinguish from ATLL — see DIS-ATLL workup pathway), HTLV-1-positive (reclassify as ATLL), or...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 203/229: f-0769 - CRITICAL

**Entity:** `RF-MM-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_mm_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
Plasma cell leukemia (PCL) — both primary and secondary forms have inferior PFS/OS on standard VRd; D-VRd or KCd is preferred. EMD at diagnosis (soft-tissue plasmacytoma not extending from bone): ≈30% worse PFS regardless of cytogenetics. ESMO MM 2023 §IV.2 explicitly recommends quadruplet (D-VRd / IsaVRd) for these high-risk presentations even in cytogenetically standard-risk patients. This RF intensifies toward D-VRd track, supplementing RF-MM-HIGH-RISK-CYTOGENETICS step 1.
```

**Excerpt context:**
```
...extending from bone): ≈30% worse PFS regardless of cytogenetics. ESMO MM 2023 §IV.2 explicitly recommends quadruplet (D-VRd / IsaVRd) for these high-risk presentations even in cytogenetically standard...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 204/229: f-0777 - CRITICAL

**Entity:** `RF-NSCLC-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_nsclc_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Geriatric assessment (G8 / CGA) recommended pre-treatment for ≥70. PD-L1≥50% driver-negative elderly: pembrolizumab mono is the best-tolerated option preserving OS benefit.
```

**Excerpt context:**
```
Geriatric assessment (G8 / CGA) recommended pre-treatment for ≥70. PD-L1≥50% driver-negative elderly: pembrolizumab mono is the best-toler...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 205/229: f-0779 - CRITICAL

**Entity:** `RF-NSCLC-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_nsclc_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Active TB OR latent TB conversion risk — ICI may trigger TB reactivation; pre-treatment IGRA / TST + chest imaging recommended.
```

**Excerpt context:**
```
...TB conversion risk — ICI may trigger TB reactivation; pre-treatment IGRA / TST + chest imaging recommended.
```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 206/229: f-0787 - CRITICAL

**Entity:** `RF-OVARIAN-BRCA-MUT-ACTIONABLE`
**File:** `knowledge_base/hosted/content/redflags/rf_ovarian_brca_mut_actionable.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Tumor-tissue testing identifies somatic BRCA missed by germline-only testing — both germline (blood) AND tumor BRCA testing recommended at diagnosis for all newly diagnosed advanced ovarian. Germline finding triggers cascade testing of relatives + risk-reducing surgery counseling. Olaparib + bevacizumab (PAOLA-1) extended benefit in HRD-positive (incl. BRCA-mut) cohort. RF coexists with RF-OVARIAN-HRD-ACTIONABILITY — BRCA-mut is the BRCA-specific subset; HRD covers both BRCA + GIS-positive non-BRCA cases.
```

**Excerpt context:**
```
...es somatic BRCA missed by germline-only testing — both germline (blood) AND tumor BRCA testing recommended at diagnosis for all newly diagnosed advanced ovarian. Germline finding triggers cascade testi...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 207/229: f-0792 - CRITICAL

**Entity:** `RF-OVARIAN-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_ovarian_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Platinum-resistant ovarian (PROC) is a defining transition point — prognosis worsens markedly (median OS ~12 mo). Sequential single- agent non-platinum chemo: PLD or weekly paclitaxel are preferred backbones; AURELIA (bevacizumab + chemo) improved PFS (HR 0.48) and is the standard if not bev-exposed and no contraindication. Mirvetuximab-soravtansine (MIRASOL) for FRα-high (≥75% by IHC PS2+) PROC: ORR 42% vs chemo 16%, OS benefit confirmed. PARPi at platinum- resistance generally not recommended (low ORR). Direction "intensify" — operationally re-routes plan generation to PROC algorithm rather than 1L choice. CA-125 + imaging confirmation per GCIG criteria.
```

**Excerpt context:**
```
...PROC: ORR 42% vs chemo 16%, OS benefit confirmed. PARPi at platinum- resistance generally not recommended (low ORR). Direction "intensify" — operationally re-routes plan generation to PROC algorithm r...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 208/229: f-0794 - CRITICAL

**Entity:** `RF-PCNSL-INTRACRANIAL-PRESSURE`
**File:** `knowledge_base/hosted/content/redflags/rf_pcnsl_intracranial_pressure.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
PCNSL frequently presents with raised ICP; 60-70% have focal deficit at diagnosis. Per NCCN-CNS PCNSL section: dexamethasone 16 mg/day initial dose markedly reduces tumor (steroid-responsive); however steroids must be HELD before stereotactic biopsy if biopsy is diagnostic-pending — steroids alone can produce tissue regression precluding histology. Direction HOLD on definitive HD-MTX-based induction until ICP managed AND biopsy obtained. Priority 10. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...methasone 16 mg/day initial dose markedly reduces tumor (steroid-responsive); however steroids must be HELD before stereotactic biopsy if biopsy is diagnostic-pending — steroids alone can produc...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 209/229: f-0798 - CRITICAL

**Entity:** `RF-PDAC-HIGH-RISK-BIOLOGY`
**File:** `knowledge_base/hosted/content/redflags/rf_pdac_high_risk_biology.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Germline NGS (24-gene HBOC + Lynch panel) + tumor NGS recommended for ALL PDAC at diagnosis (NCCN MS-12). POLO trial: olaparib maintenance after ≥16 weeks platinum without progression in BRCA1/2-germline mPDAC — mPFS 7.4 vs 3.8 mo placebo.
```

**Excerpt context:**
```
Germline NGS (24-gene HBOC + Lynch panel) + tumor NGS recommended for ALL PDAC at diagnosis (NCCN MS-12). POLO trial: olaparib maintenance after ≥16 weeks plati...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 210/229: f-0799 - CRITICAL

**Entity:** `RF-PDAC-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_pdac_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
CA19-9 must be interpreted with caution in Lewis-blood-group-negative patients (~5-7% non-secretors). Always re-image (CT) — CA19-9 fluctuations alone don't define progression.
```

**Excerpt context:**
```
CA19-9 must be interpreted with caution in Lewis-blood-group-negative patients (~5-7% non-secretors). Alwa...
```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 211/229: f-0804 - CRITICAL

**Entity:** `RF-PMF-BLAST-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_pmf_blast_progression.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Post-MPN AML has dismal prognosis (~5-month median OS); ven+aza achieves modest response. Most patients with ≥10% PB blasts and fit-enough biology should be on accelerated alloHCT trajectory. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...S); ven+aza achieves modest response. Most patients with ≥10% PB blasts and fit-enough biology should be on accelerated alloHCT trajectory. STUB — requires clinical co-lead signoff.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 212/229: f-0805 - CRITICAL

**Entity:** `RF-PMF-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_pmf_infection_screening.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Direction "hold" — surfaces a JAKi-prerequisite annotation. JAK inhibitors carry a real (if uncommon) risk of HBV reactivation, TB reactivation, and opportunistic infections (PJP, cryptococcal). Screening + prophylaxis must be in place before initiation. STUB — requires clinical co-lead signoff.
```

**Excerpt context:**
```
...on, TB reactivation, and opportunistic infections (PJP, cryptococcal). Screening + prophylaxis must be in place before initiation. STUB — requires clinical co-lead signoff.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 213/229: f-0808 - CRITICAL

**Entity:** `RF-PROSTATE-HIGH-RISK-BIOLOGY`
**File:** `knowledge_base/hosted/content/redflags/rf_prostate_high_risk_biology.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
PROfound (olaparib) + TALAPRO-2 (talazoparib + enzalutamide) + MAGNITUDE (niraparib + abiraterone) define PARPi indications. BRCA1/2 largest benefit; broader HRR cohort smaller but positive. Germline + somatic testing recommended for ALL metastatic patients per NCCN 2025.
```

**Excerpt context:**
```
.... BRCA1/2 largest benefit; broader HRR cohort smaller but positive. Germline + somatic testing recommended for ALL metastatic patients per NCCN 2025.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 214/229: f-0810 - CRITICAL

**Entity:** `RF-PROSTATE-PSA-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_prostate_psa_progression.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
PSA-only progression on ARPI / chemotherapy is common (~30-40% of patients show PSA flare or transient rise). PCWG3 explicitly cautions against line switch on PSA alone — radiographic progression (RECIST 1.1 for soft tissue, PCWG3 bone-scan rules) or new symptomatic events must accompany the PSA finding. This RF surfaces the signal for MDT; it does not auto-switch tracks. Action lives in monitoring schedule (re-image at PSA-progression event), not in `shifts_algorithm`.
```

**Excerpt context:**
```
...phic progression (RECIST 1.1 for soft tissue, PCWG3 bone-scan rules) or new symptomatic events must accompany the PSA finding. This RF surfaces the signal for MDT; it does not auto-switch tracks...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 215/229: f-0813 - CRITICAL

**Entity:** `RF-PTCL-NOS-FRAILTY-AGE`
**File:** `knowledge_base/hosted/content/redflags/rf_ptcl_frailty_age.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Etoposide adds toxicity (cytopenia, mucositis, secondary leukemia long-term) without clear OS benefit in elderly per German High-Grade NHL Study Group reanalysis — CHOP without etoposide reasonable for ≥60y or frail. CD30+ frail elderly: CHP-Bv preferred over CHOEP if fit-enough; brentuximab monotherapy palliative-curative for very frail. AutoSCT consolidation generally off-table for frail elderly. AlloHCT contraindicated. CGA-guided dose attenuation essential — PTCL outcomes poor and treatment-related mortality must be balanced against modest cure rates.
```

**Excerpt context:**
```
...ed. CGA-guided dose attenuation essential — PTCL outcomes poor and treatment-related mortality must be balanced against modest cure rates.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 216/229: f-0815 - CRITICAL

**Entity:** `RF-PTCL-NOS-INFECTION-SCREENING`
**File:** `knowledge_base/hosted/content/redflags/rf_ptcl_infection_screening.yaml`
**Field:** `definition`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Active or latent infection requiring resolution / prophylaxis before initiating CHOEP / CHP-Bv in PTCL NOS: HBsAg-positive (HBV reactivation on prolonged steroid + chemo), anti-HBc-positive (occult HBV), HCV-RNA-positive, HIV-positive (HTLV-1 differential — must exclude ATLL), HTLV-1-positive (reclassify as ATLL), EBV-driven (informs prognostication; some PTCL subsets EBV+), or active TB.
```

**Excerpt context:**
```
...chemo), anti-HBc-positive (occult HBV), HCV-RNA-positive, HIV-positive (HTLV-1 differential — must exclude ATLL), HTLV-1-positive (reclassify as ATLL), EBV-driven (informs prognostication; some...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 217/229: f-0819 - CRITICAL

**Entity:** `RF-PTLD-ORGAN-DYSFUNCTION`
**File:** `knowledge_base/hosted/content/redflags/rf_ptld_organ_dysfunction.yaml`
**Field:** `definition`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Allograft dysfunction (worsening creatinine if kidney, transaminases if liver, troponin if heart) at PTLD diagnosis — IS-reduction must be balanced against allograft loss; transplant team co-management mandatory.
```

**Excerpt context:**
```
...atinine if kidney, transaminases if liver, troponin if heart) at PTLD diagnosis — IS-reduction must be balanced against allograft loss; transplant team co-management mandatory.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 218/229: f-0824 - CRITICAL

**Entity:** `RF-R-ISS-3-HIGH-RISK`
**File:** `knowledge_base/hosted/content/redflags/rf_r_iss_3_high_risk.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
R-ISS (Palumbo et al., JCO 2015) refined ISS by adding LDH and FISH cytogenetics: R-ISS-3 = ISS-3 + LDH-high + high-risk FISH. R-ISS-3 median OS ~43 mo pre-daratumumab; modern PERSEUS / IsKia / GRIFFIN show D-VRd benefits across risk groups but absolute outcomes in R-ISS-3 remain inferior — argues for tandem ASCT consideration (StaMINA / EMN02) and aggressive maintenance (lenalidomide +/- daratumumab + ixazomib in selected protocols). Severity `critical` for conflict resolution: this should win over standard de-escalation flags. Co-fires with biomarker-actionability flags for individual cytogenetic hits.
```

**Excerpt context:**
```
...ratumumab + ixazomib in selected protocols). Severity `critical` for conflict resolution: this should win over standard de-escalation flags. Co-fires with biomarker-actionability flags for individ...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 219/229: f-0835 - CRITICAL

**Entity:** `RF-SMZL-TRANSFORMATION-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/rf_smzl_transformation_progression.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Transformation to DLBCL changes the disease classification entirely — the engine should hand off to DLBCL Algorithm with the DLBCL biopsy result.
```

**Excerpt context:**
```
Transformation to DLBCL changes the disease classification entirely — the engine should hand off to DLBCL Algorithm with the DLBCL biopsy result.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 220/229: f-0849 - CRITICAL

**Entity:** `RF-CAR-T-ELIGIBLE`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_car_t_eligible.yaml`
**Field:** `notes`
**Matched pattern:** `must`
**Pattern class:** direct obligation

**Current value:**
```
Composite gate harmonized across landmark CAR-T trials (ZUMA-1, TRANSCEND, JULIET, ZUMA-7, TRANSFORM, ZUMA-2, KarMMa, CARTITUDE-1). Real-world expansion of criteria (CIBMTR analysis): ECOG 2 acceptable with consultant judgment; LVEF 40-50% acceptable with cardiology input; bilirubin elevation from disease (Gilbert, hemolysis, cholestasis) vs primary hepatic dysfunction must be distinguished. Active CNS disease requires control (resection / IT / RT) before lymphodepletion; some centers offer CAR-T for primary CNS lymphoma with restricted criteria. Bridging plan is critical — manufacture takes 2-5 weeks; if bridging chemo gives PR/CR, lymphodepletion still scheduled. Ineligibility for one product (e.g., cilta-cel parkinsonism risk) does not preclude another (ide-cel) — re-evaluate per product.
```

**Excerpt context:**
```
...irubin elevation from disease (Gilbert, hemolysis, cholestasis) vs primary hepatic dysfunction must be distinguished. Active CNS disease requires control (resection / IT / RT) before lymphodeple...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 221/229: f-0853 - CRITICAL

**Entity:** `RF-FITNESS-ECOG-INTERMEDIATE`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_fitness_ecog_intermediate.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
ECOG 2 is the borderline zone where most intensified regimens lose benefit and gain toxicity. R-CHOP standard, R-mini-CHOP for elderly ECOG 2, ABVD over BEACOPP for Hodgkin, dose-attenuated DA-EPOCH-R selectable per case. CAR-T trials (ZUMA-1, JULIET) excluded ECOG ≥2; real-world evidence supports ECOG 2 with adequate organ function, but admission protocols vary. Geriatric assessment recommended at ECOG 2 for patients >70 to disambiguate frailty vs disease burden.
```

**Excerpt context:**
```
...pports ECOG 2 with adequate organ function, but admission protocols vary. Geriatric assessment recommended at ECOG 2 for patients >70 to disambiguate frailty vs disease burden.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 222/229: f-0855 - CRITICAL

**Entity:** `RF-FRAILTY-AGE-G8-LOW`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_frailty_age_g8_low.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
G8 is the SIOG-recommended screening tool for older oncology patients. Score ≤14 mandates full CGA (Charlson, IADL, MNA, MMSE, GDS) before regimen selection. SIOG / NCCN Older Adult Oncology guidelines: at G8 ≤14, default to dose-attenuated chemotherapy (R-mini-CHOP for DLBCL >80, attenuated VRD for myeloma in unfit, ABVD over BEACOPP for Hodgkin >60, FCR contraindicated in CLL >65). Distinct from RF-FITNESS- ECOG-POOR — a patient can be ECOG 1 yet G8-vulnerable due to cognitive/social/nutritional fragility.
```

**Excerpt context:**
```
G8 is the SIOG-recommended screening tool for older oncology patients. Score ≤14 mandates full CGA (Charlson, IADL, MNA,...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 223/229: f-0857 - CRITICAL

**Entity:** `RF-UNIVERSAL-INFUSION-REACTION-FIRST-CYCLE`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_infusion_reaction_first_cycle.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Anti-CD20 cycle-1 infusion-reaction rate: 30-77% any-grade for rituximab (Lim et al. 2012); 65% for obinutuzumab cycle-1 vs <10% by cycle-3. Premedication: paracetamol 1g + diphenhydramine 25-50 mg PO 30-60 min pre-infusion; methylprednisolone 80-100 mg IV when CD20 burden is high. Initial infusion rate 50 mg/h, escalate by 50 mg/h every 30 min if no reaction, max 400 mg/h (rituximab). Mogamulizumab and brentuximab have their own premedication regimens — engine should select per drug.
```

**Excerpt context:**
```
...mg/h (rituximab). Mogamulizumab and brentuximab have their own premedication regimens — engine should select per drug.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 224/229: f-0860 - CRITICAL

**Entity:** `RF-ORGAN-RENAL-IMPAIRED`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_organ_renal_impaired.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Single trigger covers both moderate (30-50) and severe (<30) — engine consumers should branch on the actual finding value to apply the correct attenuation. Per NCCN Drug Renal Dosing Tables / ASCO expert-panel 2014 (Lichtman et al.): cisplatin contraindicated CrCl <30 (substitute carboplatin Calvert AUC 4-5); HD-MTX contraindicated <50 mL/min (substitute IT MTX for CNS prophylaxis); cyclophosphamide reduce 25% at CrCl 30-50, 50% at <30; lenalidomide 10 mg (vs 25 mg) at CrCl 30-60, 15 mg q48h <30, dialysis-specific dosing. Anti-CD20 monoclonals (rituximab, obinutuzumab) and BTKi do not require renal adjustment. Multiple myeloma RF-MM-RENAL-DYSFUNCTION already exists for myeloma-specific cast-nephropathy logic.
```

**Excerpt context:**
```
Single trigger covers both moderate (30-50) and severe (<30) — engine consumers should branch on the actual finding value to apply the correct attenuation. Per NCCN Drug Renal Dosin...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 225/229: f-0861 - CRITICAL

**Entity:** `RF-PREGNANCY-ACTIVE`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_pregnancy_active.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
ESMO clinical practice guideline on cancer in pregnancy (Peccatori 2013, updated). First-trimester teratogenicity: no chemotherapy except emergency hematologic salvage; counsel on therapeutic abortion vs delayed therapy. Second/third trimester safety profile (Loibl, Amant): doxorubicin + cyclophosphamide AC for breast — safe; weekly paclitaxel — safe; trastuzumab — contraindicated (oligohydramnios); ICI — limited data, defer to postpartum; rituximab — neonatal B-cell depletion but reversible, often acceptable; ABVD for Hodgkin — safe in T2/T3; BEACOPP — avoid; R-CHOP for DLBCL — feasible T2/T3 with MFM. Delivery 2-3 weeks after last cycle to allow nadir recovery. Direction `hold` for any first-trimester systemic; modulated to `de-escalate` later — engine should consume gestational age.
```

**Excerpt context:**
```
.... Direction `hold` for any first-trimester systemic; modulated to `de-escalate` later — engine should consume gestational age.

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 226/229: f-0863 - CRITICAL

**Entity:** `RF-PRIOR-BTKI-PROGRESSION`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_prior_btki_progression.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
CLL: BRUIN study (Mato 2023) — pirtobrutinib ORR 82% in BTKi-pretreated; venetoclax + obinutuzumab also active (CLL14 was 1L but venetoclax monotherapy MURANO post-BTKi shows efficacy); CAR-T (liso-cel) per TRANSCEND-CLL-004. MCL: BRUIN MCL-321 — pirtobrutinib ORR 58% post- cBTKi; brexu-cel (ZUMA-2) ORR 91% in r/r MCL. WM: pirtobrutinib in TBLINNA, venetoclax + rituximab (BGB-3111-302). BTK C481S testing recommended at progression to confirm acquired resistance vs intolerance/non-adherence (different management).
```

**Excerpt context:**
```
.../r MCL. WM: pirtobrutinib in TBLINNA, venetoclax + rituximab (BGB-3111-302). BTK C481S testing recommended at progression to confirm acquired resistance vs intolerance/non-adherence (different manageme...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 227/229: f-0868 - CRITICAL

**Entity:** `RF-RICHTER-TRANSFORMATION`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_richter_transformation.yaml`
**Field:** `notes`
**Matched pattern:** `recommended`
**Pattern class:** direct recommendation verb

**Current value:**
```
Incidence 5-10% over CLL course; risk factors include unmutated IGHV, TP53 disruption, NOTCH1, MYC alterations, prior fludarabine. Clonally- related Richter (>80%) has worse OS (median 8-12 months) than clonally-unrelated (de novo DLBCL in CLL patient, 2-year OS 60%). Treatment paradigm: R-CHOP induction (CR 20-30%), consolidate with alloSCT or CAR-T (TRANSCEND-CLL-004 includes Richter cohort, ORR ~60%); BTKi-Richter — pirtobrutinib + venetoclax + R-CHOP under investigation (Mato), pembrolizumab + ibrutinib (Ding 2017) shows responses; Hodgkin-variant Richter — ABVD/AVD ± brentuximab. PET-CT guided biopsy of FDG-avid lesion (SUVmax >5) recommended in CLL patients with rapid clinical change.
```

**Excerpt context:**
```
...-variant Richter — ABVD/AVD ± brentuximab. PET-CT guided biopsy of FDG-avid lesion (SUVmax >5) recommended in CLL patients with rapid clinical change.

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 228/229: f-0869 - CRITICAL

**Entity:** `RF-UNIVERSAL-TLS-RISK`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_tls_risk.yaml`
**Field:** `notes`
**Matched pattern:** `should`
**Pattern class:** direct obligation

**Current value:**
```
Howard et al. 2011 NEJM TLS-risk stratification. NCCN Burkitt v2.2025 §BURK-A mandates rasburicase for high-risk; allopurinol for intermediate. ESMO guidance on intensive lymphoma regimens (DA-EPOCH-R, R-CHOP cycle 1) recommends 24-48h pre-cycle hydration + allopurinol when LDH ≥2× ULN. Engine should surface this RF in the plan's supportive-care section alongside the chosen regimen, not as an indication-switch.
```

**Excerpt context:**
```
..., R-CHOP cycle 1) recommends 24-48h pre-cycle hydration + allopurinol when LDH ≥2× ULN. Engine should surface this RF in the plan's supportive-care section alongside the chosen regimen, not as an...

```

**Contributor suggestion:**
```
Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 229/229: f-0870 - CRITICAL

**Entity:** `RF-UNIVERSAL-TLS-RISK`
**File:** `knowledge_base/hosted/content/redflags/universal/rf_universal_tls_risk.yaml`
**Field:** `notes`
**Matched pattern:** `recommends`
**Pattern class:** direct recommendation verb

**Current value:**
```
Howard et al. 2011 NEJM TLS-risk stratification. NCCN Burkitt v2.2025 §BURK-A mandates rasburicase for high-risk; allopurinol for intermediate. ESMO guidance on intensive lymphoma regimens (DA-EPOCH-R, R-CHOP cycle 1) recommends 24-48h pre-cycle hydration + allopurinol when LDH ≥2× ULN. Engine should surface this RF in the plan's supportive-care section alongside the chosen regimen, not as an indication-switch.
```

**Excerpt context:**
```
...ol for intermediate. ESMO guidance on intensive lymphoma regimens (DA-EPOCH-R, R-CHOP cycle 1) recommends 24-48h pre-cycle hydration + allopurinol when LDH ≥2× ULN. Engine should surface this RF in th...

```

**Contributor suggestion:**
```
Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'

```

**Notes:** Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.


**Contributor judgment:** likely_true_positive

**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---
