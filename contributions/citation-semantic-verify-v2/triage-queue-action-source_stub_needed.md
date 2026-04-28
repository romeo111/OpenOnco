# Triage Queue: citation-semantic-verify-v2

**Filter:** status=`None`, action=`source_stub_needed`

**Total rows:** 324

---

## 1/324: CV914-0007 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-P210-BALL`
**File:** `bma_bcr_abl1_p210_ball.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:71`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_bcr_abl1_p210_ball.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 2/324: CV914-0008 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-P210-BALL`
**File:** `bma_bcr_abl1_p210_ball.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:72`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_p210_ball.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 3/324: CV914-0013 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-OVARIAN`
**File:** `bma_brca1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:79`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_brca1_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 4/324: CV914-0015 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-OVARIAN`
**File:** `bma_brca1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:81`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 5/324: CV914-0017 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-PROSTATE`
**File:** `bma_brca1_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:85`

**Audit finding text:**
```
trial ''PROpel'' mentioned but no matching source citation (looked for substrings: [''PROPEL'', ''OLAPARIB-PROST''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_brca1_germline_prostate.yaml and the hosted source registry for trial 'PROpel', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 6/324: CV914-0018 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-PROSTATE`
**File:** `bma_brca1_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:86`

**Audit finding text:**
```
trial ''MAGNITUDE'' mentioned but no matching source citation (looked for substrings: [''MAGNITUDE'', ''NIRAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MAGNITUDE'. Prior candidate SRC-CHECKMATE-649-JANJIGIAN-2022 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CHECKMATE-649-JANJIGIAN-2022 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 7/324: CV914-0019 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-PROSTATE`
**File:** `bma_brca1_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:87`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (5) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 8/324: CV914-0022 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-BREAST`
**File:** `bma_brca2_germline_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:92`

**Audit finding text:**
```
trial ''OLYMPIA'' mentioned but no matching source citation (looked for substrings: [''OLYMPIA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'OLYMPIA'. Prior candidate SRC-OLYMPIAD-ROBSON-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-OLYMPIAD-ROBSON-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 9/324: CV914-0025 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-BREAST`
**File:** `bma_brca2_germline_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:95`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_germline_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 10/324: CV914-0027 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-PROSTATE`
**File:** `bma_brca2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:99`

**Audit finding text:**
```
trial ''PROpel'' mentioned but no matching source citation (looked for substrings: [''PROPEL'', ''OLAPARIB-PROST''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_brca2_germline_prostate.yaml and the hosted source registry for trial 'PROpel', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 11/324: CV914-0028 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-PROSTATE`
**File:** `bma_brca2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:100`

**Audit finding text:**
```
trial ''MAGNITUDE'' mentioned but no matching source citation (looked for substrings: [''MAGNITUDE'', ''NIRAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MAGNITUDE'. Prior candidate SRC-CHECKMATE-649-JANJIGIAN-2022 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CHECKMATE-649-JANJIGIAN-2022 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 12/324: CV914-0029 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-PROSTATE`
**File:** `bma_brca2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:101`

**Audit finding text:**
```
trial ''TALAPRO-2'' mentioned but no matching source citation (looked for substrings: [''TALAPRO'', ''TALAZOPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_brca2_germline_prostate.yaml and the hosted source registry for trial 'TALAPRO-2', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 13/324: CV914-0030 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-PROSTATE`
**File:** `bma_brca2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:102`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 14/324: CV914-0032 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-C797S-NSCLC`
**File:** `bma_egfr_c797s_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:106`

**Audit finding text:**
```
trial ''MARIPOSA'' mentioned but no matching source citation (looked for substrings: [''MARIPOSA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MARIPOSA'. Prior candidate SRC-MARIPOSA2-PASSARO-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-MARIPOSA2-PASSARO-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 15/324: CV914-0033 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-C797S-NSCLC`
**File:** `bma_egfr_c797s_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:107`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_c797s_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 16/324: CV914-0039 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-EX19DEL-NSCLC`
**File:** `bma_egfr_ex19del_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:115`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_ex19del_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 17/324: CV914-0044 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-L858R-NSCLC`
**File:** `bma_egfr_l858r_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:122`

**Audit finding text:**
```
trial ''MARIPOSA'' mentioned but no matching source citation (looked for substrings: [''MARIPOSA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MARIPOSA'. Prior candidate SRC-MARIPOSA2-PASSARO-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-MARIPOSA2-PASSARO-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 18/324: CV914-0045 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-L858R-NSCLC`
**File:** `bma_egfr_l858r_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:123`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_l858r_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 19/324: CV914-0047 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-ENDOMETRIAL`
**File:** `bma_mlh1_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:127`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_mlh1_germline_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 20/324: CV914-0048 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-ENDOMETRIAL`
**File:** `bma_mlh1_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:128`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_mlh1_germline_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 21/324: CV914-0049 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-ENDOMETRIAL`
**File:** `bma_mlh1_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:129`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 22/324: CV914-0052 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-ENDOMETRIAL`
**File:** `bma_mlh1_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:134`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_mlh1_somatic_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 23/324: CV914-0053 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-ENDOMETRIAL`
**File:** `bma_mlh1_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:135`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_mlh1_somatic_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 24/324: CV914-0054 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-ENDOMETRIAL`
**File:** `bma_mlh1_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:136`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 25/324: CV914-0057 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:141`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh2_germline_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 26/324: CV914-0058 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:142`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh2_germline_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 27/324: CV914-0059 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:143`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 28/324: CV914-0062 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:148`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh2_somatic_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 29/324: CV914-0063 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:149`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh2_somatic_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 30/324: CV914-0064 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:150`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 31/324: CV914-0067 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh6_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:155`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh6_germline_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 32/324: CV914-0068 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh6_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:156`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh6_germline_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 33/324: CV914-0069 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-ENDOMETRIAL`
**File:** `bma_msh6_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:157`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 34/324: CV914-0072 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh6_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:162`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh6_somatic_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 35/324: CV914-0073 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh6_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:163`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_msh6_somatic_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 36/324: CV914-0074 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-ENDOMETRIAL`
**File:** `bma_msh6_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:164`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 37/324: CV914-0082 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-ENDOMETRIAL`
**File:** `bma_pms2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:176`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_pms2_germline_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 38/324: CV914-0083 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-ENDOMETRIAL`
**File:** `bma_pms2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:177`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_pms2_germline_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 39/324: CV914-0084 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-ENDOMETRIAL`
**File:** `bma_pms2_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:178`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 40/324: CV914-0087 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-ENDOMETRIAL`
**File:** `bma_pms2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:183`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_pms2_somatic_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 41/324: CV914-0088 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-ENDOMETRIAL`
**File:** `bma_pms2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:184`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_pms2_somatic_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 42/324: CV914-0089 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-ENDOMETRIAL`
**File:** `bma_pms2_somatic_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:185`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 43/324: CV914-0092 - unclear -> source_stub_needed

**Entity:** `BMA-RAD51B-GERMLINE-OVARIAN`
**File:** `bma_rad51b_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:190`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_rad51b_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 44/324: CV914-0097 - unclear -> source_stub_needed

**Entity:** `BMA-RAD51C-GERMLINE-OVARIAN`
**File:** `bma_rad51c_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:197`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_rad51c_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 45/324: CV914-0099 - unclear -> source_stub_needed

**Entity:** `BMA-RAD51C-GERMLINE-OVARIAN`
**File:** `bma_rad51c_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:199`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_rad51c_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 46/324: CV914-0102 - unclear -> source_stub_needed

**Entity:** `BMA-RAD51D-GERMLINE-OVARIAN`
**File:** `bma_rad51d_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:204`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_rad51d_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 47/324: CV914-0104 - unclear -> source_stub_needed

**Entity:** `BMA-RAD51D-GERMLINE-OVARIAN`
**File:** `bma_rad51d_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:206`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_rad51d_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 48/324: CV914-0107 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-MAINT-BEV`
**File:** `ind_ovarian_maint_bev.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:211`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_maint_bev.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 49/324: CV914-0109 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-MAINT-BEV`
**File:** `ind_ovarian_maint_bev.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:213`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_maint_bev.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 50/324: CV914-0110 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-MAINT-BEV`
**File:** `ind_ovarian_maint_bev.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:214`

**Audit finding text:**
```
trial ''GOG-218'' mentioned but no matching source citation (looked for substrings: [''GOG-218''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_maint_bev.yaml and the hosted source registry for trial 'GOG-218', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 51/324: CV914-0111 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-MAINT-BEV`
**File:** `ind_ovarian_maint_bev.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:215`

**Audit finding text:**
```
trial ''ICON7'' mentioned but no matching source citation (looked for substrings: [''ICON7''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_maint_bev.yaml and the hosted source registry for trial 'ICON7', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 52/324: CV914-0113 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-FUSION-ALCL`
**File:** `bma_alk_fusion_alcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:219`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_fusion_alcl.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 53/324: CV914-0117 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-FUSION-NSCLC`
**File:** `bma_alk_fusion_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:225`

**Audit finding text:**
```
trial ''ALINA'' mentioned but no matching source citation (looked for substrings: [''ALINA'', ''ALECTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_alk_fusion_nsclc.yaml and the hosted source registry for trial 'ALINA', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 54/324: CV914-0119 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-FUSION-NSCLC`
**File:** `bma_alk_fusion_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:227`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_fusion_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 55/324: CV914-0122 - unclear -> source_stub_needed

**Entity:** `BMA-BCL2-EXPRESSION-CLL`
**File:** `bma_bcl2_expression_cll.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:232`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcl2_expression_cll.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 56/324: CV914-0124 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-BREAST`
**File:** `bma_brca1_germline_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:236`

**Audit finding text:**
```
trial ''OLYMPIA'' mentioned but no matching source citation (looked for substrings: [''OLYMPIA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'OLYMPIA'. Prior candidate SRC-OLYMPIAD-ROBSON-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-OLYMPIAD-ROBSON-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 57/324: CV914-0127 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-BREAST`
**File:** `bma_brca1_germline_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:239`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_germline_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 58/324: CV914-0130 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-OVARIAN`
**File:** `bma_brca2_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:244`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 59/324: CV914-0132 - unclear -> source_stub_needed

**Entity:** `BMA-CCND1-T1114-MCL`
**File:** `bma_ccnd1_t1114_mcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:248`

**Audit finding text:**
```
trial ''TRIANGLE'' mentioned but no matching source citation (looked for substrings: [''TRIANGLE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'TRIANGLE'. Prior candidate SRC-ESMO-MCL-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 60/324: CV914-0133 - unclear -> source_stub_needed

**Entity:** `BMA-CCND1-T1114-MCL`
**File:** `bma_ccnd1_t1114_mcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:249`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (5) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ccnd1_t1114_mcl.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 61/324: CV914-0136 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR2-MUTATION-ENDOMETRIAL`
**File:** `bma_fgfr2_mutation_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:254`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_fgfr2_mutation_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 62/324: CV914-0137 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR2-MUTATION-ENDOMETRIAL`
**File:** `bma_fgfr2_mutation_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:255`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_fgfr2_mutation_endometrial.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 63/324: CV914-0140 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-ITD-AML`
**File:** `bma_flt3_itd_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:260`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_flt3_itd_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 64/324: CV914-0144 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-PDAC`
**File:** `bma_kras_g12c_pdac.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:266`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 65/324: CV914-0146 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-PDAC`
**File:** `bma_kras_g12c_pdac.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:268`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kras_g12c_pdac.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 66/324: CV914-0148 - unclear -> source_stub_needed

**Entity:** `BMA-PALB2-GERMLINE-OVARIAN`
**File:** `bma_palb2_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:272`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_palb2_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 67/324: CV914-0150 - unclear -> source_stub_needed

**Entity:** `BMA-PALB2-GERMLINE-OVARIAN`
**File:** `bma_palb2_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:274`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_palb2_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 68/324: CV914-0155 - unclear -> source_stub_needed

**Entity:** `BMA-RET-FUSION-NSCLC`
**File:** `bma_ret_fusion_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:281`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_fusion_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 69/324: CV914-0159 - unclear -> source_stub_needed

**Entity:** `BMA-RET-KIF5B-NSCLC`
**File:** `bma_ret_kif5b_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:287`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_kif5b_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 70/324: CV914-0160 - unclear -> source_stub_needed

**Entity:** `BMA-TP53-MUT-MCL`
**File:** `bma_tp53_mut_mcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:290`

**Audit finding text:**
```
trial ''TRIANGLE'' mentioned but no matching source citation (looked for substrings: [''TRIANGLE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'TRIANGLE'. Prior candidate SRC-ESMO-MCL-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 71/324: CV914-0167 - unclear -> source_stub_needed

**Entity:** `IND-BREAST-HR-POS-MAINT-CDK46I`
**File:** `ind_breast_hr_pos_maint_cdk46i.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:299`

**Audit finding text:**
```
trial ''TROPiCS-02'' mentioned but no matching source citation (looked for substrings: [''TROPICS'', ''SACITUZUMAB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'TROPiCS-02'. Prior candidate SRC-NCCN-BREAST-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-NCCN-BREAST-2025 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 72/324: CV914-0168 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET`
**File:** `ind_prostate_mhspc_1l_arpi_doublet.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:302`

**Audit finding text:**
```
trial ''LATITUDE'' mentioned but no matching source citation (looked for substrings: [''LATITUDE'', ''ABIRATERONE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'LATITUDE'. Prior candidate SRC-ESMO-PROSTATE-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-ESMO-PROSTATE-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 73/324: CV914-0169 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET`
**File:** `ind_prostate_mhspc_1l_arpi_doublet.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:303`

**Audit finding text:**
```
trial ''ENZAMET'' mentioned but no matching source citation (looked for substrings: [''ENZAMET'', ''ENZALUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_prostate_mhspc_1l_arpi_doublet.yaml and the hosted source registry for trial 'ENZAMET', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 74/324: CV914-0170 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET`
**File:** `ind_prostate_mhspc_1l_arpi_doublet.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:304`

**Audit finding text:**
```
trial ''TITAN'' mentioned but no matching source citation (looked for substrings: [''TITAN'', ''APALUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_prostate_mhspc_1l_arpi_doublet.yaml and the hosted source registry for trial 'TITAN', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 75/324: CV914-0171 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET`
**File:** `ind_prostate_mhspc_1l_arpi_doublet.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:305`

**Audit finding text:**
```
trial ''ARASENS'' mentioned but no matching source citation (looked for substrings: [''ARASENS'', ''DAROLUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_prostate_mhspc_1l_arpi_doublet.yaml and the hosted source registry for trial 'ARASENS', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 76/324: CV914-0172 - unclear -> source_stub_needed

**Entity:** `BMA-BARD1-GERMLINE-OVARIAN`
**File:** `bma_bard1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:308`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_bard1_germline_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 77/324: CV914-0173 - unclear -> source_stub_needed

**Entity:** `BMA-BARD1-GERMLINE-OVARIAN`
**File:** `bma_bard1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:309`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bard1_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 78/324: CV914-0175 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-E255K-CML`
**File:** `bma_bcr_abl1_e255k_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:313`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_e255k_cml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 79/324: CV914-0178 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-F317L-BALL`
**File:** `bma_bcr_abl1_f317l_ball.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:318`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_f317l_ball.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 80/324: CV914-0181 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-T315I-BALL`
**File:** `bma_bcr_abl1_t315i_ball.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:323`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_t315i_ball.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 81/324: CV914-0185 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-T315I-CML`
**File:** `bma_bcr_abl1_t315i_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:329`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_t315i_cml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 82/324: CV914-0189 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-CRC`
**File:** `bma_braf_v600e_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:335`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 83/324: CV914-0190 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-HCL`
**File:** `bma_braf_v600e_hcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:338`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_hcl.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 84/324: CV914-0195 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-MELANOMA`
**File:** `bma_braf_v600e_melanoma.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:345`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_melanoma.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 85/324: CV914-0197 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600K-MELANOMA`
**File:** `bma_braf_v600k_melanoma.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:349`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600k_melanoma.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 86/324: CV914-0200 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-SOMATIC-OVARIAN`
**File:** `bma_brca1_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:354`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 87/324: CV914-0202 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-SOMATIC-PROSTATE`
**File:** `bma_brca1_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:358`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 88/324: CV914-0206 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-SOMATIC-OVARIAN`
**File:** `bma_brca2_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:364`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 89/324: CV914-0208 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-SOMATIC-PROSTATE`
**File:** `bma_brca2_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:368`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 90/324: CV914-0211 - unclear -> source_stub_needed

**Entity:** `BMA-BRIP1-GERMLINE-OVARIAN`
**File:** `bma_brip1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:373`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brip1_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 91/324: CV914-0214 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-EX20INS-NSCLC`
**File:** `bma_egfr_ex20ins_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:378`

**Audit finding text:**
```
trial ''PAPILLON'' mentioned but no matching source citation (looked for substrings: [''PAPILLON'', ''AMIVANTAMAB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'PAPILLON'. Prior candidate SRC-CHRYSALIS-PARK-2021 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CHRYSALIS-PARK-2021 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 92/324: CV914-0215 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-EX20INS-NSCLC`
**File:** `bma_egfr_ex20ins_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:379`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_ex20ins_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 93/324: CV914-0218 - unclear -> source_stub_needed

**Entity:** `BMA-EPCAM-GERMLINE-CRC`
**File:** `bma_epcam_germline_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:384`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_epcam_germline_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 94/324: CV914-0220 - unclear -> source_stub_needed

**Entity:** `BMA-EPCAM-GERMLINE-ENDOMETRIAL`
**File:** `bma_epcam_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:388`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_epcam_germline_endometrial.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 95/324: CV914-0221 - unclear -> source_stub_needed

**Entity:** `BMA-EPCAM-GERMLINE-ENDOMETRIAL`
**File:** `bma_epcam_germline_endometrial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:389`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_epcam_germline_endometrial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 96/324: CV914-0223 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR2-MUTATION-UROTHELIAL`
**File:** `bma_fgfr2_mutation_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:393`

**Audit finding text:**
```
trial ''BLC2001'' mentioned but no matching source citation (looked for substrings: [''BLC2001'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_fgfr2_mutation_urothelial.yaml and the hosted source registry for trial 'BLC2001', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 97/324: CV914-0224 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR2-MUTATION-UROTHELIAL`
**File:** `bma_fgfr2_mutation_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:394`

**Audit finding text:**
```
trial ''THOR'' mentioned but no matching source citation (looked for substrings: [''THOR'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'THOR'. Prior candidate SRC-POSEIDON-JOHNSON-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-POSEIDON-JOHNSON-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 98/324: CV914-0225 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR2-MUTATION-UROTHELIAL`
**File:** `bma_fgfr2_mutation_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:395`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_fgfr2_mutation_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 99/324: CV914-0226 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-TACC3-UROTHELIAL`
**File:** `bma_fgfr3_tacc3_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:398`

**Audit finding text:**
```
trial ''BLC2001'' mentioned but no matching source citation (looked for substrings: [''BLC2001'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_fgfr3_tacc3_urothelial.yaml and the hosted source registry for trial 'BLC2001', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 100/324: CV914-0227 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-TACC3-UROTHELIAL`
**File:** `bma_fgfr3_tacc3_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:399`

**Audit finding text:**
```
trial ''THOR'' mentioned but no matching source citation (looked for substrings: [''THOR'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'THOR'. Prior candidate SRC-POSEIDON-JOHNSON-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-POSEIDON-JOHNSON-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 101/324: CV914-0228 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-TACC3-UROTHELIAL`
**File:** `bma_fgfr3_tacc3_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:400`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_fgfr3_tacc3_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 102/324: CV914-0229 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-D835-AML`
**File:** `bma_flt3_d835_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:403`

**Audit finding text:**
```
trial ''MAGNITUDE'' mentioned but no matching source citation (looked for substrings: [''MAGNITUDE'', ''NIRAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MAGNITUDE'. Prior candidate SRC-CHECKMATE-649-JANJIGIAN-2022 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CHECKMATE-649-JANJIGIAN-2022 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 103/324: CV914-0230 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-D835-AML`
**File:** `bma_flt3_d835_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:404`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_flt3_d835_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 104/324: CV914-0232 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-F691L-AML`
**File:** `bma_flt3_f691l_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:408`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 105/324: CV914-0235 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132C-AML`
**File:** `bma_idh1_r132c_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:413`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132c_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 106/324: CV914-0238 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-CRC`
**File:** `bma_kras_g12c_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:418`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 107/324: CV914-0240 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-CRC`
**File:** `bma_kras_g12c_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:420`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kras_g12c_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 108/324: CV914-0241 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-NSCLC`
**File:** `bma_kras_g12c_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:423`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 109/324: CV914-0243 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-NSCLC`
**File:** `bma_kras_g12c_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:425`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kras_g12c_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 110/324: CV914-0245 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-GASTRIC`
**File:** `bma_mlh1_germline_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:429`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 111/324: CV914-0248 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-GASTRIC`
**File:** `bma_mlh1_somatic_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:434`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 112/324: CV914-0251 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-GASTRIC`
**File:** `bma_msh2_germline_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:439`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 113/324: CV914-0254 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-GASTRIC`
**File:** `bma_msh2_somatic_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:444`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 114/324: CV914-0257 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-GASTRIC`
**File:** `bma_msh6_germline_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:449`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 115/324: CV914-0260 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-GASTRIC`
**File:** `bma_msh6_somatic_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:454`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 116/324: CV914-0262 - unclear -> source_stub_needed

**Entity:** `BMA-MYD88-L265P-HCV-MZL`
**File:** `bma_myd88_l265p_hcv_mzl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:458`

**Audit finding text:**
```
trial ''MAGNOLIA'' mentioned but no matching source citation (looked for substrings: [''MAGNOLIA''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_myd88_l265p_hcv_mzl.yaml and the hosted source registry for trial 'MAGNOLIA', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 117/324: CV914-0265 - unclear -> source_stub_needed

**Entity:** `BMA-MYD88-L265P-NODAL-MZL`
**File:** `bma_myd88_l265p_nodal_mzl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:463`

**Audit finding text:**
```
trial ''MAGNOLIA'' mentioned but no matching source citation (looked for substrings: [''MAGNOLIA''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_myd88_l265p_nodal_mzl.yaml and the hosted source registry for trial 'MAGNOLIA', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 118/324: CV914-0268 - unclear -> source_stub_needed

**Entity:** `BMA-MYD88-L265P-SPLENIC-MZL`
**File:** `bma_myd88_l265p_splenic_mzl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:468`

**Audit finding text:**
```
trial ''MAGNOLIA'' mentioned but no matching source citation (looked for substrings: [''MAGNOLIA''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_myd88_l265p_splenic_mzl.yaml and the hosted source registry for trial 'MAGNOLIA', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 119/324: CV914-0272 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-GASTRIC`
**File:** `bma_pms2_germline_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:474`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 120/324: CV914-0275 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-GASTRIC`
**File:** `bma_pms2_somatic_gastric.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:479`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_gastric.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 121/324: CV914-0279 - unclear -> source_stub_needed

**Entity:** `BMA-RET-CCDC6-NSCLC`
**File:** `bma_ret_ccdc6_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:485`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_ccdc6_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 122/324: CV914-0282 - unclear -> source_stub_needed

**Entity:** `BMA-RET-FUSION-THYROID-PAPILLARY`
**File:** `bma_ret_fusion_thyroid_papillary.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:490`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_fusion_thyroid_papillary.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 123/324: CV914-0284 - unclear -> source_stub_needed

**Entity:** `BMA-ROS1-G2032R-NSCLC`
**File:** `bma_ros1_g2032r_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:494`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ros1_g2032r_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 124/324: CV914-0286 - unclear -> source_stub_needed

**Entity:** `BMA-TP53-MUT-BREAST`
**File:** `bma_tp53_mut_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:498`

**Audit finding text:**
```
trial ''KEYNOTE-522'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-522'', ''KEYNOTE522''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'KEYNOTE-522'. Prior candidate SRC-NCCN-BREAST-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 125/324: CV914-0289 - unclear -> source_stub_needed

**Entity:** `IND-CML-1L-2GEN-TKI`
**File:** `ind_cml_1l_2gen_tki.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:503`

**Audit finding text:**
```
trial ''ENESTnd'' mentioned but no matching source citation (looked for substrings: [''ENESTND'', ''NILOTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_cml_1l_2gen_tki.yaml and the hosted source registry for trial 'ENESTnd', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 126/324: CV914-0290 - unclear -> source_stub_needed

**Entity:** `IND-CML-1L-2GEN-TKI`
**File:** `ind_cml_1l_2gen_tki.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:504`

**Audit finding text:**
```
trial ''DASISION'' mentioned but no matching source citation (looked for substrings: [''DASISION'', ''DASATINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_cml_1l_2gen_tki.yaml and the hosted source registry for trial 'DASISION', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 127/324: CV914-0291 - unclear -> source_stub_needed

**Entity:** `IND-CML-1L-2GEN-TKI`
**File:** `ind_cml_1l_2gen_tki.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:505`

**Audit finding text:**
```
trial ''BFORE'' mentioned but no matching source citation (looked for substrings: [''BFORE'', ''BOSUTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_cml_1l_2gen_tki.yaml and the hosted source registry for trial 'BFORE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 128/324: CV914-0292 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO`
**File:** `ind_endometrial_advanced_1l_pembro_chemo.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:508`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_advanced_1l_pembro_chemo.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 129/324: CV914-0293 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO`
**File:** `ind_endometrial_advanced_1l_pembro_chemo.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:509`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_advanced_1l_pembro_chemo.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 130/324: CV914-0294 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO`
**File:** `ind_endometrial_advanced_1l_pembro_chemo.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:510`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_advanced_1l_pembro_chemo.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 131/324: CV914-0297 - unclear -> source_stub_needed

**Entity:** `IND-MTC-ADVANCED-1L-SELPERCATINIB`
**File:** `ind_mtc_advanced_1l_selpercatinib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:515`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 132/324: CV914-0300 - unclear -> source_stub_needed

**Entity:** `IND-NSCLC-ALK-MAINT-ALECTINIB`
**File:** `ind_nsclc_alk_maint_alectinib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:520`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_nsclc_alk_maint_alectinib.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 133/324: CV914-0301 - unclear -> source_stub_needed

**Entity:** `REG-2GEN-TKI-CML`
**File:** `dasatinib_or_nilotinib_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:523`

**Audit finding text:**
```
trial ''ENESTnd'' mentioned but no matching source citation (looked for substrings: [''ENESTND'', ''NILOTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity dasatinib_or_nilotinib_cml.yaml and the hosted source registry for trial 'ENESTnd', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 134/324: CV914-0302 - unclear -> source_stub_needed

**Entity:** `REG-2GEN-TKI-CML`
**File:** `dasatinib_or_nilotinib_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:524`

**Audit finding text:**
```
trial ''DASISION'' mentioned but no matching source citation (looked for substrings: [''DASISION'', ''DASATINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity dasatinib_or_nilotinib_cml.yaml and the hosted source registry for trial 'DASISION', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 135/324: CV914-0303 - unclear -> source_stub_needed

**Entity:** `REG-2GEN-TKI-CML`
**File:** `dasatinib_or_nilotinib_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:525`

**Audit finding text:**
```
trial ''BFORE'' mentioned but no matching source citation (looked for substrings: [''BFORE'', ''BOSUTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity dasatinib_or_nilotinib_cml.yaml and the hosted source registry for trial 'BFORE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 136/324: CV914-0305 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-EML4-V1-NSCLC`
**File:** `bma_alk_eml4_v1_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:529`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_eml4_v1_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 137/324: CV914-0307 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-EML4-V3-NSCLC`
**File:** `bma_alk_eml4_v3_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:533`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_eml4_v3_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 138/324: CV914-0308 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-G1202R-NSCLC`
**File:** `bma_alk_g1202r_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:536`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_g1202r_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 139/324: CV914-0310 - unclear -> source_stub_needed

**Entity:** `BMA-ALK-L1196M-NSCLC`
**File:** `bma_alk_l1196m_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:540`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_alk_l1196m_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 140/324: CV914-0312 - unclear -> source_stub_needed

**Entity:** `BMA-ATM-SOMATIC-PROSTATE`
**File:** `bma_atm_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:544`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_atm_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 141/324: CV914-0314 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-F317L-CML`
**File:** `bma_bcr_abl1_f317l_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:548`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_f317l_cml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 142/324: CV914-0316 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-P190-BALL`
**File:** `bma_bcr_abl1_p190_ball.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:552`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_p190_ball.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 143/324: CV914-0318 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-P210-CML`
**File:** `bma_bcr_abl1_p210_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:556`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_bcr_abl1_p210_cml.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 144/324: CV914-0319 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-P210-CML`
**File:** `bma_bcr_abl1_p210_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:557`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_p210_cml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 145/324: CV914-0320 - unclear -> source_stub_needed

**Entity:** `BMA-BCR-ABL1-V299L-CML`
**File:** `bma_bcr_abl1_v299l_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:560`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_bcr_abl1_v299l_cml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 146/324: CV914-0322 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-GBM`
**File:** `bma_braf_v600e_gbm.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:564`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_gbm.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 147/324: CV914-0324 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-OVARIAN`
**File:** `bma_braf_v600e_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:568`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 148/324: CV914-0326 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-PDAC`
**File:** `bma_braf_v600e_pdac.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:572`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_pdac.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 149/324: CV914-0328 - unclear -> source_stub_needed

**Entity:** `BMA-CHEK1-SOMATIC-PROSTATE`
**File:** `bma_chek1_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:576`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_chek1_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 150/324: CV914-0330 - unclear -> source_stub_needed

**Entity:** `BMA-CHEK2-GERMLINE-PROSTATE`
**File:** `bma_chek2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:580`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_chek2_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 151/324: CV914-0332 - unclear -> source_stub_needed

**Entity:** `BMA-CHEK2-SOMATIC-PROSTATE`
**File:** `bma_chek2_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:584`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_chek2_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 152/324: CV914-0335 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-T790M-NSCLC`
**File:** `bma_egfr_t790m_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:589`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_t790m_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 153/324: CV914-0336 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-R248C-UROTHELIAL`
**File:** `bma_fgfr3_r248c_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:592`

**Audit finding text:**
```
trial ''THOR'' mentioned but no matching source citation (looked for substrings: [''THOR'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'THOR'. Prior candidate SRC-POSEIDON-JOHNSON-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-POSEIDON-JOHNSON-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 154/324: CV914-0337 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-R248C-UROTHELIAL`
**File:** `bma_fgfr3_r248c_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:593`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_fgfr3_r248c_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 155/324: CV914-0338 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-S249C-UROTHELIAL`
**File:** `bma_fgfr3_s249c_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:596`

**Audit finding text:**
```
trial ''THOR'' mentioned but no matching source citation (looked for substrings: [''THOR'', ''ERDAFITINIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'THOR'. Prior candidate SRC-POSEIDON-JOHNSON-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-POSEIDON-JOHNSON-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 156/324: CV914-0339 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-S249C-UROTHELIAL`
**File:** `bma_fgfr3_s249c_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:597`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_fgfr3_s249c_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 157/324: CV914-0340 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132C-GBM`
**File:** `bma_idh1_r132c_gbm.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:600`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132c_gbm.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 158/324: CV914-0342 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132G-AML`
**File:** `bma_idh1_r132g_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:604`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132g_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 159/324: CV914-0344 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132H-AML`
**File:** `bma_idh1_r132h_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:608`

**Audit finding text:**
```
trial ''AGILE'' mentioned but no matching source citation (looked for substrings: [''AGILE'', ''IVOSIDENIB''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_idh1_r132h_aml.yaml and the hosted source registry for trial 'AGILE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 160/324: CV914-0345 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132H-AML`
**File:** `bma_idh1_r132h_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:609`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132h_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 161/324: CV914-0346 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132H-GBM`
**File:** `bma_idh1_r132h_gbm.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:612`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132h_gbm.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 162/324: CV914-0348 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132L-AML`
**File:** `bma_idh1_r132l_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:616`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132l_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 163/324: CV914-0350 - unclear -> source_stub_needed

**Entity:** `BMA-IDH1-R132S-AML`
**File:** `bma_idh1_r132s_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:620`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh1_r132s_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 164/324: CV914-0354 - unclear -> source_stub_needed

**Entity:** `BMA-KIT-D816V-GIST`
**File:** `bma_kit_d816v_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:628`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kit_d816v_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 165/324: CV914-0356 - unclear -> source_stub_needed

**Entity:** `BMA-KIT-EXON11-GIST`
**File:** `bma_kit_exon11_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:632`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kit_exon11_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 166/324: CV914-0358 - unclear -> source_stub_needed

**Entity:** `BMA-KIT-EXON13-17-GIST`
**File:** `bma_kit_exon13_17_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:636`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kit_exon13_17_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 167/324: CV914-0360 - unclear -> source_stub_needed

**Entity:** `BMA-KIT-EXON9-GIST`
**File:** `bma_kit_exon9_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:640`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kit_exon9_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 168/324: CV914-0362 - unclear -> source_stub_needed

**Entity:** `BMA-KRAS-G12C-OVARIAN`
**File:** `bma_kras_g12c_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:644`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 169/324: CV914-0364 - unclear -> source_stub_needed

**Entity:** `BMA-MET-AMP-NSCLC`
**File:** `bma_met_amp_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:648`

**Audit finding text:**
```
trial ''MARIPOSA'' mentioned but no matching source citation (looked for substrings: [''MARIPOSA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MARIPOSA'. Prior candidate SRC-MARIPOSA2-PASSARO-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-MARIPOSA2-PASSARO-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 170/324: CV914-0366 - unclear -> source_stub_needed

**Entity:** `BMA-MET-AMP-RCC-PAPILLARY`
**File:** `bma_met_amp_rcc_papillary.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:652`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_met_amp_rcc_papillary.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 171/324: CV914-0369 - unclear -> source_stub_needed

**Entity:** `BMA-MET-EX14-NSCLC`
**File:** `bma_met_ex14_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:657`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_met_ex14_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 172/324: CV914-0371 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-CRC`
**File:** `bma_mlh1_germline_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:661`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 173/324: CV914-0372 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-OVARIAN`
**File:** `bma_mlh1_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:664`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 174/324: CV914-0374 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-PROSTATE`
**File:** `bma_mlh1_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:668`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 175/324: CV914-0377 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-CRC`
**File:** `bma_mlh1_somatic_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:673`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 176/324: CV914-0378 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-OVARIAN`
**File:** `bma_mlh1_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:676`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 177/324: CV914-0380 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-PROSTATE`
**File:** `bma_mlh1_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:680`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 178/324: CV914-0383 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-CRC`
**File:** `bma_msh2_germline_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:685`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 179/324: CV914-0384 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-OVARIAN`
**File:** `bma_msh2_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:688`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 180/324: CV914-0386 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-PROSTATE`
**File:** `bma_msh2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:692`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 181/324: CV914-0389 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-CRC`
**File:** `bma_msh2_somatic_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:697`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 182/324: CV914-0390 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-OVARIAN`
**File:** `bma_msh2_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:700`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 183/324: CV914-0392 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-PROSTATE`
**File:** `bma_msh2_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:704`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 184/324: CV914-0395 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-CRC`
**File:** `bma_msh6_germline_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:709`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 185/324: CV914-0396 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-OVARIAN`
**File:** `bma_msh6_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:712`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 186/324: CV914-0398 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-PROSTATE`
**File:** `bma_msh6_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:716`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 187/324: CV914-0401 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-CRC`
**File:** `bma_msh6_somatic_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:721`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 188/324: CV914-0402 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-OVARIAN`
**File:** `bma_msh6_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:724`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 189/324: CV914-0404 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-PROSTATE`
**File:** `bma_msh6_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:728`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 190/324: CV914-0407 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-CRC`
**File:** `bma_pms2_germline_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:733`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 191/324: CV914-0408 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-OVARIAN`
**File:** `bma_pms2_germline_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:736`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 192/324: CV914-0410 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-PROSTATE`
**File:** `bma_pms2_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:740`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 193/324: CV914-0413 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-CRC`
**File:** `bma_pms2_somatic_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:745`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 194/324: CV914-0414 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-OVARIAN`
**File:** `bma_pms2_somatic_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:748`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_ovarian.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 195/324: CV914-0416 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-PROSTATE`
**File:** `bma_pms2_somatic_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:752`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 196/324: CV914-0419 - unclear -> source_stub_needed

**Entity:** `BMA-RET-C634R-MTC`
**File:** `bma_ret_c634r_mtc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:757`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_c634r_mtc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 197/324: CV914-0421 - unclear -> source_stub_needed

**Entity:** `BMA-RET-M918T-MTC`
**File:** `bma_ret_m918t_mtc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:761`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ret_m918t_mtc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 198/324: CV914-0423 - unclear -> source_stub_needed

**Entity:** `BMA-ROS1-FUSION-NSCLC`
**File:** `bma_ros1_fusion_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:765`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ros1_fusion_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 199/324: CV914-0424 - unclear -> source_stub_needed

**Entity:** `IND-ALCL-MAINTENANCE-BV-POST-ASCT`
**File:** `ind_alcl_maintenance_bv_post_asct.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:768`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_alcl_maintenance_bv_post_asct.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 200/324: CV914-0427 - unclear -> source_stub_needed

**Entity:** `IND-APL-1L-ATRA-ATO-IDA`
**File:** `ind_apl_1l_atra_ato_ida.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:773`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://ashpublications.org/blood/article/133/15/1630/272971 failed with 'HTTP Error 403: Forbidden'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-ESMO-AML-2020, SRC-APL0406-LOCOCO-2013


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 201/324: CV914-0434 - unclear -> source_stub_needed

**Entity:** `IND-BREAST-TNBC-EARLY-NEOADJUVANT`
**File:** `ind_breast_tnbc_early_neoadjuvant.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:788`

**Audit finding text:**
```
trial ''OLYMPIA'' mentioned but no matching source citation (looked for substrings: [''OLYMPIA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'OLYMPIA'. Prior candidate SRC-OLYMPIAD-ROBSON-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-OLYMPIAD-ROBSON-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 202/324: CV914-0435 - unclear -> source_stub_needed

**Entity:** `IND-BREAST-TNBC-EARLY-NEOADJUVANT`
**File:** `ind_breast_tnbc_early_neoadjuvant.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:789`

**Audit finding text:**
```
trial ''KEYNOTE-522'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-522'', ''KEYNOTE522''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'KEYNOTE-522'. Prior candidate SRC-NCCN-BREAST-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-NCCN-BREAST-2025 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 203/324: CV914-0440 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR`
**File:** `ind_endometrial_2l_dostarlimab_dmmr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:800`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_2l_dostarlimab_dmmr.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 204/324: CV914-0441 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR`
**File:** `ind_endometrial_2l_dostarlimab_dmmr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:801`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_2l_dostarlimab_dmmr.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 205/324: CV914-0442 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR`
**File:** `ind_endometrial_2l_pembro_lenva_pmmr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:804`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_2l_pembro_lenva_pmmr.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 206/324: CV914-0443 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR`
**File:** `ind_endometrial_2l_pembro_lenva_pmmr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:805`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_2l_pembro_lenva_pmmr.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 207/324: CV914-0444 - unclear -> source_stub_needed

**Entity:** `IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS`
**File:** `ind_esoph_adjuvant_nivolumab_post_cross.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:808`

**Audit finding text:**
```
trial ''CheckMate-577'' mentioned but no matching source citation (looked for substrings: [''CHECKMATE-577'', ''CHECKMATE577''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_esoph_adjuvant_nivolumab_post_cross.yaml and the hosted source registry for trial 'CheckMate-577', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 208/324: CV914-0445 - unclear -> source_stub_needed

**Entity:** `IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS`
**File:** `ind_esoph_adjuvant_nivolumab_post_cross.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:809`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 209/324: CV914-0446 - unclear -> source_stub_needed

**Entity:** `IND-FL-1L-BR`
**File:** `ind_fl_1l_br.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:812`

**Audit finding text:**
```
trial ''STIL'' mentioned but no matching source citation (looked for substrings: [''STIL''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_fl_1l_br.yaml and the hosted source registry for trial 'STIL', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 210/324: CV914-0450 - unclear -> source_stub_needed

**Entity:** `IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME`
**File:** `ind_melanoma_braf_metastatic_1l_dabra_trame.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:820`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 211/324: CV914-0457 - unclear -> source_stub_needed

**Entity:** `IND-NSCLC-EGFR-MAINT-OSIMERTINIB`
**File:** `ind_nsclc_egfr_maint_osimertinib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:833`

**Audit finding text:**
```
trial ''MARIPOSA'' mentioned but no matching source citation (looked for substrings: [''MARIPOSA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MARIPOSA'. Prior candidate SRC-MARIPOSA2-PASSARO-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-MARIPOSA2-PASSARO-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 212/324: CV914-0463 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG`
**File:** `ind_ovarian_advanced_1l_carbo_pacli_hrd_neg.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:845`

**Audit finding text:**
```
trial ''GOG-218'' mentioned but no matching source citation (looked for substrings: [''GOG-218''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_advanced_1l_carbo_pacli_hrd_neg.yaml and the hosted source registry for trial 'GOG-218', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 213/324: CV914-0465 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP`
**File:** `ind_ovarian_advanced_1l_carbo_pacli_hrd_olap.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:849`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_advanced_1l_carbo_pacli_hrd_olap.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 214/324: CV914-0467 - unclear -> source_stub_needed

**Entity:** `IND-OVARIAN-MAINTENANCE-OLAPARIB`
**File:** `ind_ovarian_maintenance_olaparib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:853`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ovarian_maintenance_olaparib.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 215/324: CV914-0468 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MCRPC-1L-PARPI`
**File:** `ind_prostate_mcrpc_1l_parpi.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:856`

**Audit finding text:**
```
trial ''MAGNITUDE'' mentioned but no matching source citation (looked for substrings: [''MAGNITUDE'', ''NIRAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'MAGNITUDE'. Prior candidate SRC-CHECKMATE-649-JANJIGIAN-2022 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CHECKMATE-649-JANJIGIAN-2022 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 216/324: CV914-0469 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MCRPC-1L-PARPI`
**File:** `ind_prostate_mcrpc_1l_parpi.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:857`

**Audit finding text:**
```
trial ''TALAPRO-2'' mentioned but no matching source citation (looked for substrings: [''TALAPRO'', ''TALAZOPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_prostate_mcrpc_1l_parpi.yaml and the hosted source registry for trial 'TALAPRO-2', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 217/324: CV914-0471 - unclear -> source_stub_needed

**Entity:** `IND-SCLC-EXTENSIVE-1L`
**File:** `ind_sclc_extensive_1l.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:861`

**Audit finding text:**
```
trial ''IMpower133'' mentioned but no matching source citation (looked for substrings: [''IMPOWER133'', ''ATEZOLIZUMAB-SCLC''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'IMpower133'. Prior candidate SRC-ESMO-SCLC-2021 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-ESMO-SCLC-2021 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 218/324: CV914-0472 - unclear -> source_stub_needed

**Entity:** `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO`
**File:** `ind_urothelial_metastatic_1l_ev_pembro.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:864`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_urothelial_metastatic_1l_ev_pembro.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 219/324: CV914-0473 - unclear -> source_stub_needed

**Entity:** `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO`
**File:** `ind_urothelial_metastatic_1l_ev_pembro.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:865`

**Audit finding text:**
```
trial ''EV-302'' mentioned but no matching source citation (looked for substrings: [''EV-302'', ''EV302'', ''ENFORTUMAB'', ''PADCEV''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_urothelial_metastatic_1l_ev_pembro.yaml and the hosted source registry for trial 'EV-302', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 220/324: CV914-0474 - unclear -> source_stub_needed

**Entity:** `REG-ADT-ABIRATERONE`
**File:** `reg_adt_abiraterone.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:868`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 221/324: CV914-0475 - unclear -> source_stub_needed

**Entity:** `REG-ADT-ABIRATERONE`
**File:** `reg_adt_abiraterone.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:869`

**Audit finding text:**
```
trial ''LATITUDE'' mentioned but no matching source citation (looked for substrings: [''LATITUDE'', ''ABIRATERONE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'LATITUDE'. Prior candidate SRC-ESMO-PROSTATE-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 222/324: CV914-0477 - unclear -> source_stub_needed

**Entity:** `REG-ALECTINIB-NSCLC`
**File:** `reg_alectinib_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:873`

**Audit finding text:**
```
trial ''ALINA'' mentioned but no matching source citation (looked for substrings: [''ALINA'', ''ALECTINIB''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_alectinib_nsclc.yaml and the hosted source registry for trial 'ALINA', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 223/324: CV914-0484 - unclear -> source_stub_needed

**Entity:** `REG-DOSTARLIMAB-MONO-ENDOM`
**File:** `reg_dostarlimab_mono_endom.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:888`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_dostarlimab_mono_endom.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 224/324: CV914-0485 - unclear -> source_stub_needed

**Entity:** `REG-DOSTARLIMAB-MONO-ENDOM`
**File:** `reg_dostarlimab_mono_endom.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:889`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_dostarlimab_mono_endom.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 225/324: CV914-0486 - unclear -> source_stub_needed

**Entity:** `REG-EV-PEMBRO-UROTHELIAL`
**File:** `reg_ev_pembro_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:892`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_ev_pembro_urothelial.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 226/324: CV914-0487 - unclear -> source_stub_needed

**Entity:** `REG-EV-PEMBRO-UROTHELIAL`
**File:** `reg_ev_pembro_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:893`

**Audit finding text:**
```
trial ''EV-302'' mentioned but no matching source citation (looked for substrings: [''EV-302'', ''EV302'', ''ENFORTUMAB'', ''PADCEV''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_ev_pembro_urothelial.yaml and the hosted source registry for trial 'EV-302', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 227/324: CV914-0488 - unclear -> source_stub_needed

**Entity:** `REG-FOLFOX-CETUX`
**File:** `folfox_cetuximab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:896`

**Audit finding text:**
```
trial ''FIRE-3'' mentioned but no matching source citation (looked for substrings: [''FIRE-3''])

```

**Verification rationale:**
```
Investigated current hosted entity folfox_cetuximab.yaml and the hosted source registry for trial 'FIRE-3', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 228/324: CV914-0489 - unclear -> source_stub_needed

**Entity:** `REG-FOLFOX-CETUX`
**File:** `folfox_cetuximab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:897`

**Audit finding text:**
```
trial ''CRYSTAL'' mentioned but no matching source citation (looked for substrings: [''CRYSTAL''])

```

**Verification rationale:**
```
Investigated current hosted entity folfox_cetuximab.yaml and the hosted source registry for trial 'CRYSTAL', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 229/324: CV914-0490 - unclear -> source_stub_needed

**Entity:** `REG-NIVO-ADJUVANT-ESOPH`
**File:** `nivolumab_adjuvant_esophageal.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:900`

**Audit finding text:**
```
trial ''CheckMate-577'' mentioned but no matching source citation (looked for substrings: [''CHECKMATE-577'', ''CHECKMATE577''])

```

**Verification rationale:**
```
Investigated current hosted entity nivolumab_adjuvant_esophageal.yaml and the hosted source registry for trial 'CheckMate-577', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 230/324: CV914-0491 - unclear -> source_stub_needed

**Entity:** `REG-NIVO-ADJUVANT-ESOPH`
**File:** `nivolumab_adjuvant_esophageal.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:901`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-ESMO-ESOPHAGEAL-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-ESMO-ESOPHAGEAL-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 231/324: CV914-0492 - unclear -> source_stub_needed

**Entity:** `REG-OLAPARIB-BREAST`
**File:** `reg_olaparib_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:904`

**Audit finding text:**
```
trial ''OLYMPIA'' mentioned but no matching source citation (looked for substrings: [''OLYMPIA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'OLYMPIA'. Prior candidate SRC-OLYMPIAD-ROBSON-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-OLYMPIAD-ROBSON-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 232/324: CV914-0495 - unclear -> source_stub_needed

**Entity:** `REG-OLAPARIB-MAINT-OVARIAN`
**File:** `olaparib_maintenance_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:909`

**Audit finding text:**
```
trial ''PAOLA-1'' mentioned but no matching source citation (looked for substrings: [''PAOLA'', ''OLAPARIB''])

```

**Verification rationale:**
```
Investigated current hosted entity olaparib_maintenance_ovarian.yaml and the hosted source registry for trial 'PAOLA-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 233/324: CV914-0498 - unclear -> source_stub_needed

**Entity:** `REG-PEMBRO-CHEMO-NSCLC-NONSQ`
**File:** `reg_pembro_chemo_nsclc_nonsq.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:916`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 234/324: CV914-0502 - unclear -> source_stub_needed

**Entity:** `REG-RICE-BURKITT`
**File:** `reg_rice_burkitt.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:924`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 235/324: CV914-0505 - unclear -> source_stub_needed

**Entity:** `REG-SACITUZUMAB`
**File:** `reg_sacituzumab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:929`

**Audit finding text:**
```
trial ''TROPiCS-02'' mentioned but no matching source citation (looked for substrings: [''TROPICS'', ''SACITUZUMAB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'TROPiCS-02'. Prior candidate SRC-NCCN-BREAST-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Other source candidates: SRC-ASCENT-BARDIA-2021


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 236/324: CV914-0511 - unclear -> source_stub_needed

**Entity:** `REG-TECLISTAMAB`
**File:** `reg_teclistamab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:941`

**Audit finding text:**
```
trial ''MonumenTAL-1'' mentioned but no matching source citation (looked for substrings: [''MONUMENTAL'', ''TALQUETAMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_teclistamab.yaml and the hosted source registry for trial 'MonumenTAL-1', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 237/324: CV914-0514 - unclear -> source_stub_needed

**Entity:** `BMA-ATM-GERMLINE-PROSTATE`
**File:** `bma_atm_germline_prostate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:948`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_atm_germline_prostate.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 238/324: CV914-0515 - unclear -> source_stub_needed

**Entity:** `BMA-ATM-LOSS-CLL`
**File:** `bma_atm_loss_cll.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:951`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_atm_loss_cll.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 239/324: CV914-0516 - unclear -> source_stub_needed

**Entity:** `BMA-BRAF-V600E-NSCLC`
**File:** `bma_braf_v600e_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:954`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_braf_v600e_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 240/324: CV914-0517 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA1-GERMLINE-PDAC`
**File:** `bma_brca1_germline_pdac.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:957`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca1_germline_pdac.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 241/324: CV914-0518 - unclear -> source_stub_needed

**Entity:** `BMA-BRCA2-GERMLINE-PDAC`
**File:** `bma_brca2_germline_pdac.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:960`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_brca2_germline_pdac.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 242/324: CV914-0519 - unclear -> source_stub_needed

**Entity:** `BMA-EGFR-G719X-NSCLC`
**File:** `bma_egfr_g719x_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:963`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_egfr_g719x_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 243/324: CV914-0522 - unclear -> source_stub_needed

**Entity:** `BMA-FGFR3-Y373C-UROTHELIAL`
**File:** `bma_fgfr3_y373c_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:972`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_fgfr3_y373c_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 244/324: CV914-0523 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-D835-AML-RR`
**File:** `bma_flt3_d835_aml_rr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:975`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_flt3_d835_aml_rr.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 245/324: CV914-0524 - unclear -> source_stub_needed

**Entity:** `BMA-FLT3-ITD-AML-RR`
**File:** `bma_flt3_itd_aml_rr.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:978`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_flt3_itd_aml_rr.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 246/324: CV914-0525 - unclear -> source_stub_needed

**Entity:** `BMA-IDH2-R140Q-AML`
**File:** `bma_idh2_r140q_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:981`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh2_r140q_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 247/324: CV914-0526 - unclear -> source_stub_needed

**Entity:** `BMA-IDH2-R172K-AML`
**File:** `bma_idh2_r172k_aml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:984`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_idh2_r172k_aml.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 248/324: CV914-0527 - unclear -> source_stub_needed

**Entity:** `BMA-KIT-D816V-MASTOCYTOSIS`
**File:** `bma_kit_d816v_mastocytosis.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:987`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_kit_d816v_mastocytosis.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 249/324: CV914-0528 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-GERMLINE-UROTHELIAL`
**File:** `bma_mlh1_germline_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:990`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_germline_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 250/324: CV914-0529 - unclear -> source_stub_needed

**Entity:** `BMA-MLH1-SOMATIC-UROTHELIAL`
**File:** `bma_mlh1_somatic_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:993`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_mlh1_somatic_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 251/324: CV914-0530 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-GERMLINE-UROTHELIAL`
**File:** `bma_msh2_germline_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:996`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_germline_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 252/324: CV914-0531 - unclear -> source_stub_needed

**Entity:** `BMA-MSH2-SOMATIC-UROTHELIAL`
**File:** `bma_msh2_somatic_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:999`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh2_somatic_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 253/324: CV914-0532 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-GERMLINE-UROTHELIAL`
**File:** `bma_msh6_germline_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1002`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_germline_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 254/324: CV914-0533 - unclear -> source_stub_needed

**Entity:** `BMA-MSH6-SOMATIC-UROTHELIAL`
**File:** `bma_msh6_somatic_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1005`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_msh6_somatic_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 255/324: CV914-0534 - unclear -> source_stub_needed

**Entity:** `BMA-MYD88-L265P-WM`
**File:** `bma_myd88_l265p_wm.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1008`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_myd88_l265p_wm.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 256/324: CV914-0535 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-ETV6-SALIVARY`
**File:** `bma_ntrk_etv6_salivary.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1011`

**Audit finding text:**
```
trial ''STARTRK'' mentioned but no matching source citation (looked for substrings: [''STARTRK''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'STARTRK'. Prior candidate SRC-STARTRK2-DRILON-2020 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-STARTRK2-DRILON-2020 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 257/324: CV914-0536 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-FUSION-CRC`
**File:** `bma_ntrk_fusion_crc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1014`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ntrk_fusion_crc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 258/324: CV914-0537 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-FUSION-IFS`
**File:** `bma_ntrk_fusion_ifs.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1017`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity bma_ntrk_fusion_ifs.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 259/324: CV914-0538 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-FUSION-NSCLC`
**File:** `bma_ntrk_fusion_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1020`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ntrk_fusion_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 260/324: CV914-0539 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-FUSION-SALIVARY`
**File:** `bma_ntrk_fusion_salivary.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1023`

**Audit finding text:**
```
trial ''STARTRK'' mentioned but no matching source citation (looked for substrings: [''STARTRK''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'STARTRK'. Prior candidate SRC-STARTRK2-DRILON-2020 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-STARTRK2-DRILON-2020 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 261/324: CV914-0540 - unclear -> source_stub_needed

**Entity:** `BMA-NTRK-FUSION-THYROID-PAPILLARY`
**File:** `bma_ntrk_fusion_thyroid_papillary.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1026`

**Audit finding text:**
```
trial ''STARTRK'' mentioned but no matching source citation (looked for substrings: [''STARTRK''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'STARTRK'. Prior candidate SRC-STARTRK2-DRILON-2020 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-STARTRK2-DRILON-2020 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 262/324: CV914-0541 - unclear -> source_stub_needed

**Entity:** `BMA-PDGFRA-EXON12-GIST`
**File:** `bma_pdgfra_exon12_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1029`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pdgfra_exon12_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 263/324: CV914-0542 - unclear -> source_stub_needed

**Entity:** `BMA-PDGFRA-EXON14-GIST`
**File:** `bma_pdgfra_exon14_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1032`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pdgfra_exon14_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 264/324: CV914-0543 - unclear -> source_stub_needed

**Entity:** `BMA-PDGFRA-EXON18-NON-D842-GIST`
**File:** `bma_pdgfra_exon18_non_d842_gist.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1035`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pdgfra_exon18_non_d842_gist.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 265/324: CV914-0544 - unclear -> source_stub_needed

**Entity:** `BMA-PIK3CA-E542K-BREAST`
**File:** `bma_pik3ca_e542k_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1038`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pik3ca_e542k_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 266/324: CV914-0545 - unclear -> source_stub_needed

**Entity:** `BMA-PIK3CA-E545K-BREAST`
**File:** `bma_pik3ca_e545k_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1041`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pik3ca_e545k_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 267/324: CV914-0546 - unclear -> source_stub_needed

**Entity:** `BMA-PIK3CA-H1047L-BREAST`
**File:** `bma_pik3ca_h1047l_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1044`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pik3ca_h1047l_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 268/324: CV914-0547 - unclear -> source_stub_needed

**Entity:** `BMA-PIK3CA-H1047R-BREAST`
**File:** `bma_pik3ca_h1047r_breast.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1047`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pik3ca_h1047r_breast.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 269/324: CV914-0548 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-GERMLINE-UROTHELIAL`
**File:** `bma_pms2_germline_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1050`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_germline_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 270/324: CV914-0549 - unclear -> source_stub_needed

**Entity:** `BMA-PMS2-SOMATIC-UROTHELIAL`
**File:** `bma_pms2_somatic_urothelial.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1053`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_pms2_somatic_urothelial.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 271/324: CV914-0550 - unclear -> source_stub_needed

**Entity:** `BMA-ROS1-CD74-NSCLC`
**File:** `bma_ros1_cd74_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1056`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ros1_cd74_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 272/324: CV914-0551 - unclear -> source_stub_needed

**Entity:** `BMA-ROS1-EZR-NSCLC`
**File:** `bma_ros1_ezr_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1059`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ros1_ezr_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 273/324: CV914-0552 - unclear -> source_stub_needed

**Entity:** `BMA-ROS1-SLC34A2-NSCLC`
**File:** `bma_ros1_slc34a2_nsclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1062`

**Audit finding text:**
```
regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

```

**Verification rationale:**
```
Current entity bma_ros1_slc34a2_nsclc.yaml still has regulatory_approval content but no primary/source/evidence source ID containing FDA, EMA, DailyMed, openFDA, or label. Because v1 has source_id=null, no regulatory source could be fetched.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 274/324: CV914-0554 - unclear -> source_stub_needed

**Entity:** `IND-APL-1L-ATRA-ATO`
**File:** `ind_apl_1l_atra_ato.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1068`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://ashpublications.org/blood/article/133/15/1630/272971 failed with 'HTTP Error 403: Forbidden'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-APL0406-LOCOCO-2013, SRC-ESMO-AML-2020


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 275/324: CV914-0555 - unclear -> source_stub_needed

**Entity:** `IND-APL-SALVAGE-ATRA-ATO`
**File:** `ind_apl_salvage_atra_ato.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1071`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-ELN-APL-2019 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 276/324: CV914-0556 - unclear -> source_stub_needed

**Entity:** `IND-ATLL-2L-MOGAMULIZUMAB`
**File:** `ind_atll_2l_mogamulizumab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1074`

**Audit finding text:**
```
trial ''BRIGHT'' mentioned but no matching source citation (looked for substrings: [''BRIGHT''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_atll_2l_mogamulizumab.yaml and the hosted source registry for trial 'BRIGHT', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 277/324: CV914-0561 - unclear -> source_stub_needed

**Entity:** `IND-BURKITT-2L-RDHAP-ASCT`
**File:** `ind_burkitt_2l_rdhap_asct.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1089`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 278/324: CV914-0562 - unclear -> source_stub_needed

**Entity:** `IND-BURKITT-2L-RICE-ASCT`
**File:** `ind_burkitt_2l_rice_asct.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1092`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_burkitt_2l_rice_asct.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 279/324: CV914-0568 - unclear -> source_stub_needed

**Entity:** `IND-CML-3L-ASCIMINIB`
**File:** `ind_cml_3l_asciminib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1110`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 280/324: CV914-0570 - unclear -> source_stub_needed

**Entity:** `IND-CRC-METASTATIC-1L-RAS-WT-LEFT`
**File:** `ind_crc_metastatic_1l_ras_wt_left.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1116`

**Audit finding text:**
```
trial ''FIRE-3'' mentioned but no matching source citation (looked for substrings: [''FIRE-3''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_crc_metastatic_1l_ras_wt_left.yaml and the hosted source registry for trial 'FIRE-3', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 281/324: CV914-0574 - unclear -> source_stub_needed

**Entity:** `IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV`
**File:** `ind_crc_metastatic_maint_folfiri_bev.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1128`

**Audit finding text:**
```
trial ''PRODIGE'' mentioned but no matching source citation (looked for substrings: [''PRODIGE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_crc_metastatic_maint_folfiri_bev.yaml and the hosted source registry for trial 'PRODIGE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 282/324: CV914-0575 - unclear -> source_stub_needed

**Entity:** `IND-EATL-2L-ICE`
**File:** `ind_eatl_2l_ice.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1131`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_eatl_2l_ice.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 283/324: CV914-0576 - unclear -> source_stub_needed

**Entity:** `IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO`
**File:** `ind_endometrial_advanced_1l_dostarlimab_chemo.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1134`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_endometrial_advanced_1l_dostarlimab_chemo.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 284/324: CV914-0577 - unclear -> source_stub_needed

**Entity:** `IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS`
**File:** `ind_esoph_metastatic_2l_nivo_squamous.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1137`

**Audit finding text:**
```
trial ''KEYNOTE-590'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-590'', ''KEYNOTE590''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_esoph_metastatic_2l_nivo_squamous.yaml and the hosted source registry for trial 'KEYNOTE-590', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 285/324: CV914-0578 - unclear -> source_stub_needed

**Entity:** `IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT`
**File:** `ind_esoph_resectable_cross_neoadjuvant.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1140`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 286/324: CV914-0580 - unclear -> source_stub_needed

**Entity:** `IND-FL-3L-MOSUNETUZUMAB`
**File:** `ind_fl_3l_mosunetuzumab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1146`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_fl_3l_mosunetuzumab.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 287/324: CV914-0583 - unclear -> source_stub_needed

**Entity:** `IND-GBM-NEWLY-DIAGNOSED-STUPP`
**File:** `ind_gbm_newly_diagnosed_stupp.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1155`

**Audit finding text:**
```
trial ''Stupp'' mentioned but no matching source citation (looked for substrings: [''STUPP'', ''TEMOZOLOMIDE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'Stupp'. Prior candidate SRC-EANO-GBM-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-EANO-GBM-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 288/324: CV914-0584 - unclear -> source_stub_needed

**Entity:** `IND-GIST-1L-IMATINIB`
**File:** `ind_gist_1l_imatinib.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1158`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 289/324: CV914-0590 - unclear -> source_stub_needed

**Entity:** `IND-MTC-ADVANCED-1L-CABOZANTINIB-RET-WT`
**File:** `ind_mtc_advanced_1l_cabozantinib_ret_wt.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1176`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 290/324: CV914-0591 - unclear -> source_stub_needed

**Entity:** `IND-NLPBL-2L-RCHOP-TRANSFORMATION`
**File:** `ind_nlpbl_2l_rchop_transformation.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1179`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_nlpbl_2l_rchop_transformation.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 291/324: CV914-0592 - unclear -> source_stub_needed

**Entity:** `IND-NMZL-1L-WATCH`
**File:** `ind_nmzl_1l_watch.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1182`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_nmzl_1l_watch.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 292/324: CV914-0593 - unclear -> source_stub_needed

**Entity:** `IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB`
**File:** `ind_nsclc_2l_docetaxel_ramucirumab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1185`

**Audit finding text:**
```
trial ''IMpower150'' mentioned but no matching source citation (looked for substrings: [''IMPOWER150''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_nsclc_2l_docetaxel_ramucirumab.yaml and the hosted source registry for trial 'IMpower150', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 293/324: CV914-0595 - unclear -> source_stub_needed

**Entity:** `IND-NSCLC-KRAS-G12C-MET-2L`
**File:** `ind_nsclc_kras_g12c_met_2l.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1191`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 294/324: CV914-0597 - unclear -> source_stub_needed

**Entity:** `IND-NSCLC-STAGE-III-PACIFIC`
**File:** `ind_nsclc_stage_iii_pacific.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1197`

**Audit finding text:**
```
trial ''PACIFIC'' mentioned but no matching source citation (looked for substrings: [''PACIFIC'', ''DURVALUMAB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'PACIFIC'. Prior candidate SRC-NCCN-NSCLC-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-NCCN-NSCLC-2025 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 295/324: CV914-0598 - unclear -> source_stub_needed

**Entity:** `IND-PDAC-METASTATIC-1L-FOLFIRINOX`
**File:** `ind_pdac_metastatic_1l_folfirinox.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1200`

**Audit finding text:**
```
trial ''PRODIGE'' mentioned but no matching source citation (looked for substrings: [''PRODIGE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_pdac_metastatic_1l_folfirinox.yaml and the hosted source registry for trial 'PRODIGE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 296/324: CV914-0600 - unclear -> source_stub_needed

**Entity:** `IND-PROSTATE-MHSPC-1L-TRIPLET`
**File:** `ind_prostate_mhspc_1l_triplet.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1206`

**Audit finding text:**
```
trial ''ARASENS'' mentioned but no matching source citation (looked for substrings: [''ARASENS'', ''DAROLUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_prostate_mhspc_1l_triplet.yaml and the hosted source registry for trial 'ARASENS', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 297/324: CV914-0602 - unclear -> source_stub_needed

**Entity:** `IND-PTCL-2L-PRALATREXATE`
**File:** `ind_ptcl_2l_pralatrexate.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1212`

**Audit finding text:**
```
trial ''PROpel'' mentioned but no matching source citation (looked for substrings: [''PROPEL'', ''OLAPARIB-PROST''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_ptcl_2l_pralatrexate.yaml and the hosted source registry for trial 'PROpel', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 298/324: CV914-0603 - unclear -> source_stub_needed

**Entity:** `IND-RCC-METASTATIC-1L-NIVO-IPI`
**File:** `ind_rcc_metastatic_1l_nivo_ipi.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1215`

**Audit finding text:**
```
trial ''CheckMate-214'' mentioned but no matching source citation (looked for substrings: [''CHECKMATE-214'', ''CHECKMATE214''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_rcc_metastatic_1l_nivo_ipi.yaml and the hosted source registry for trial 'CheckMate-214', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 299/324: CV914-0604 - unclear -> source_stub_needed

**Entity:** `IND-RCC-METASTATIC-1L-PEMBRO-AXI`
**File:** `ind_rcc_metastatic_1l_pembro_axi.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1218`

**Audit finding text:**
```
trial ''KEYNOTE-426'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-426'', ''KEYNOTE426''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_rcc_metastatic_1l_pembro_axi.yaml and the hosted source registry for trial 'KEYNOTE-426', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 300/324: CV914-0606 - unclear -> source_stub_needed

**Entity:** `IND-WM-2L-VRD`
**File:** `ind_wm_2l_vrd.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1224`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity ind_wm_2l_vrd.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 301/324: CV914-0609 - unclear -> source_stub_needed

**Entity:** `REG-ACALABRUTINIB-RITUXIMAB`
**File:** `acalabrutinib_rituximab.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1233`

**Audit finding text:**
```
trial ''SHINE'' mentioned but no matching source citation (looked for substrings: [''SHINE'', ''IBRUTINIB-MCL''])

```

**Verification rationale:**
```
Investigated current hosted entity acalabrutinib_rituximab.yaml and the hosted source registry for trial 'SHINE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 302/324: CV914-0610 - unclear -> source_stub_needed

**Entity:** `REG-ADT-APALUTAMIDE`
**File:** `reg_adt_apalutamide.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1236`

**Audit finding text:**
```
trial ''TITAN'' mentioned but no matching source citation (looked for substrings: [''TITAN'', ''APALUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_adt_apalutamide.yaml and the hosted source registry for trial 'TITAN', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 303/324: CV914-0611 - unclear -> source_stub_needed

**Entity:** `REG-ADT-DAROLUTAMIDE-DOCETAXEL`
**File:** `reg_adt_darolutamide_docetaxel.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1239`

**Audit finding text:**
```
trial ''ARASENS'' mentioned but no matching source citation (looked for substrings: [''ARASENS'', ''DAROLUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_adt_darolutamide_docetaxel.yaml and the hosted source registry for trial 'ARASENS', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 304/324: CV914-0612 - unclear -> source_stub_needed

**Entity:** `REG-ADT-ENZALUTAMIDE`
**File:** `reg_adt_enzalutamide.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1242`

**Audit finding text:**
```
trial ''ENZAMET'' mentioned but no matching source citation (looked for substrings: [''ENZAMET'', ''ENZALUTAMIDE''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_adt_enzalutamide.yaml and the hosted source registry for trial 'ENZAMET', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 305/324: CV914-0615 - unclear -> source_stub_needed

**Entity:** `REG-ASCIMINIB-CML`
**File:** `reg_asciminib_cml.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1251`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 306/324: CV914-0616 - unclear -> source_stub_needed

**Entity:** `REG-ATRA-ATO-APL`
**File:** `atra_ato_apl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1254`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://ashpublications.org/blood/article/133/15/1630/272971 failed with 'HTTP Error 403: Forbidden'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-APL0406-LOCOCO-2013, SRC-ESMO-AML-2020


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 307/324: CV914-0617 - unclear -> source_stub_needed

**Entity:** `REG-ATRA-ATO-APL-SALVAGE`
**File:** `reg_atra_ato_apl_salvage.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1257`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://ashpublications.org/blood/article/133/15/1630/272971 failed with 'HTTP Error 403: Forbidden'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-ESMO-AML-2020, SRC-APL0406-LOCOCO-2013


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 308/324: CV914-0618 - unclear -> source_stub_needed

**Entity:** `REG-ATRA-ATO-IDA-APL`
**File:** `atra_ato_ida_apl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1260`

**Audit finding text:**
```
trial ''AIDA'' mentioned but no matching source citation (looked for substrings: [''AIDA''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'AIDA'. Prior candidate SRC-ELN-APL-2019 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://ashpublications.org/blood/article/133/15/1630/272971 failed with 'HTTP Error 403: Forbidden'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-APL0406-LOCOCO-2013, SRC-ESMO-AML-2020


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 309/324: CV914-0621 - unclear -> source_stub_needed

**Entity:** `REG-CARBO-PACLI-OVARIAN`
**File:** `carboplatin_paclitaxel_ovarian.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1269`

**Audit finding text:**
```
trial ''GOG-218'' mentioned but no matching source citation (looked for substrings: [''GOG-218''])

```

**Verification rationale:**
```
Investigated current hosted entity carboplatin_paclitaxel_ovarian.yaml and the hosted source registry for trial 'GOG-218', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 310/324: CV914-0622 - unclear -> source_stub_needed

**Entity:** `REG-CARBOPLATIN-PACLITAXEL-WEEKLY`
**File:** `carboplatin_paclitaxel_weekly.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1272`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-ESMO-ESOPHAGEAL-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-ESMO-ESOPHAGEAL-2024 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 311/324: CV914-0625 - unclear -> source_stub_needed

**Entity:** `REG-DOSTARLIMAB-CARBO-PACLI-ENDOM`
**File:** `reg_dostarlimab_carbo_pacli_endom.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1281`

**Audit finding text:**
```
trial ''RUBY'' mentioned but no matching source citation (looked for substrings: [''RUBY'', ''DOSTARLIMAB''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_dostarlimab_carbo_pacli_endom.yaml and the hosted source registry for trial 'RUBY', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 312/324: CV914-0626 - unclear -> source_stub_needed

**Entity:** `REG-DURVA-CONSOLIDATION-PACIFIC`
**File:** `reg_durva_consolidation_pacific.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1284`

**Audit finding text:**
```
trial ''PACIFIC'' mentioned but no matching source citation (looked for substrings: [''PACIFIC'', ''DURVALUMAB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'PACIFIC'. Prior candidate SRC-NCCN-NSCLC-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Other source candidates: SRC-ESMO-NSCLC-EARLY-2024


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 313/324: CV914-0628 - unclear -> source_stub_needed

**Entity:** `REG-EP-ATEZO-SCLC`
**File:** `reg_ep_atezo_sclc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1290`

**Audit finding text:**
```
trial ''IMpower133'' mentioned but no matching source citation (looked for substrings: [''IMPOWER133'', ''ATEZOLIZUMAB-SCLC''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'IMpower133'. Prior candidate SRC-ESMO-SCLC-2021 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Other source candidates: SRC-NCCN-SCLC-2025


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 314/324: CV914-0631 - unclear -> source_stub_needed

**Entity:** `REG-FOLFIRINOX`
**File:** `folfirinox.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1299`

**Audit finding text:**
```
trial ''PRODIGE'' mentioned but no matching source citation (looked for substrings: [''PRODIGE''])

```

**Verification rationale:**
```
Investigated current hosted entity folfirinox.yaml and the hosted source registry for trial 'PRODIGE', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 315/324: CV914-0636 - unclear -> source_stub_needed

**Entity:** `REG-NIVO-IPI-RCC`
**File:** `reg_nivo_ipi_rcc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1314`

**Audit finding text:**
```
trial ''CheckMate-214'' mentioned but no matching source citation (looked for substrings: [''CHECKMATE-214'', ''CHECKMATE214''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_nivo_ipi_rcc.yaml and the hosted source registry for trial 'CheckMate-214', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 316/324: CV914-0637 - unclear -> source_stub_needed

**Entity:** `REG-PEMBRO-AXI-RCC`
**File:** `reg_pembro_axi_rcc.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1317`

**Audit finding text:**
```
trial ''KEYNOTE-426'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-426'', ''KEYNOTE426''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_pembro_axi_rcc.yaml and the hosted source registry for trial 'KEYNOTE-426', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 317/324: CV914-0638 - unclear -> source_stub_needed

**Entity:** `REG-PEMBRO-CARBO-PACLI-ENDOM`
**File:** `reg_pembro_carbo_pacli_endom.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1320`

**Audit finding text:**
```
trial ''NRG-GY018'' mentioned but no matching source citation (looked for substrings: [''GY018'', ''PEMBRO-ENDOM''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_pembro_carbo_pacli_endom.yaml and the hosted source registry for trial 'NRG-GY018', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 318/324: CV914-0639 - unclear -> source_stub_needed

**Entity:** `REG-PEMBRO-CHEMO-TNBC-NEOADJUVANT`
**File:** `reg_pembro_chemo_tnbc_neoadjuvant.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1323`

**Audit finding text:**
```
trial ''KEYNOTE-522'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-522'', ''KEYNOTE522''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'KEYNOTE-522'. Prior candidate SRC-NCCN-BREAST-2025 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 319/324: CV914-0640 - unclear -> source_stub_needed

**Entity:** `REG-PEMBRO-MONO-ESOPH-2L`
**File:** `reg_pembro_mono_esoph_2l.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1326`

**Audit finding text:**
```
trial ''KEYNOTE-590'' mentioned but no matching source citation (looked for substrings: [''KEYNOTE-590'', ''KEYNOTE590''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_pembro_mono_esoph_2l.yaml and the hosted source registry for trial 'KEYNOTE-590', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 320/324: CV914-0643 - unclear -> source_stub_needed

**Entity:** `REG-PRALATREXATE-PTCL`
**File:** `reg_pralatrexate_ptcl.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1335`

**Audit finding text:**
```
trial ''PROpel'' mentioned but no matching source citation (looked for substrings: [''PROPEL'', ''OLAPARIB-PROST''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_pralatrexate_ptcl.yaml and the hosted source registry for trial 'PROpel', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 321/324: CV914-0644 - unclear -> source_stub_needed

**Entity:** `REG-RDHAP-BURKITT`
**File:** `reg_rdhap_burkitt.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1338`

**Audit finding text:**
```
trial ''CROSS'' mentioned but no matching source citation (looked for substrings: [''CROSS''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CROSS'. Prior candidate SRC-IMC-HTLV-2017 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-IMC-HTLV-2017 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 322/324: CV914-0646 - unclear -> source_stub_needed

**Entity:** `REG-SOTORASIB-KRAS`
**File:** `reg_sotorasib_kras.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1344`

**Audit finding text:**
```
trial ''CodeBreaK'' mentioned but no matching source citation (looked for substrings: [''CODEBREAK'', ''SOTORASIB''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'CodeBreaK'. Prior candidate SRC-CODEBREAK-300-FAKIH-2023 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** Strict replace_source repair: previous candidate SRC-CODEBREAK-300-FAKIH-2023 rejected; no specific-trial to guideline/different-trial replacement retained.


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 323/324: CV914-0647 - unclear -> source_stub_needed

**Entity:** `REG-STUPP-TMZ`
**File:** `stupp_temozolomide.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1347`

**Audit finding text:**
```
trial ''Stupp'' mentioned but no matching source citation (looked for substrings: [''STUPP'', ''TEMOZOLOMIDE''])

```

**Verification rationale:**
```
Rechecked after maintainer review. Audit names specific trial 'Stupp'. Prior candidate SRC-EANO-GBM-2024 was rejected because the target source id/title does not contain the exact trial name or is a general guideline/different trial. No strict trial-specific hosted Source was found in knowledge_base/hosted/content/sources by source id/title, so this row remains unresolved and needs a trial-specific source stub or maintainer mapping.

```

**Notes:** URL reachability check on https://www.eano.eu/guidelines/ failed with 'HTTP Error 404: Not Found'; row downgraded from supported to access_blocked pending maintainer/source replacement review.       Other source candidates: SRC-NCCN-CNS-2025


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---

## 324/324: CV914-0652 - unclear -> source_stub_needed

**Entity:** `REG-VRD-WM`
**File:** `reg_vrd_wm.yaml`
**Claim locator:** `docs/reviews/citation-verification-2026-04-27.md:1362`

**Audit finding text:**
```
trial ''PARADIGM'' mentioned but no matching source citation (looked for substrings: [''PARADIGM''])

```

**Verification rationale:**
```
Investigated current hosted entity reg_vrd_wm.yaml and the hosted source registry for trial 'PARADIGM', but no existing SRC-* record matched the trial name in source id/title. The v1 row has source_id=null, so there is no cited source to fetch; a real source stub or maintainer mapping is still needed.

```

**Notes:** ""


**Maintainer action:**
- [ ] keep (genuinely unresolvable; no edit)
- [ ] file source_stub_needed (attempt to find authoritative source)
- [ ] revise_claim (narrow the claim wording)
- [ ] escalate

---
