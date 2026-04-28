# Triage Queue: ua-translation-review-batch

**Filter:** severity = `critical`

**Total findings in queue:** 200

Walk through each finding. Read the current value (fetched from entity file), the contributor's suggestion (often a meta-description, not a literal replacement), and decide: edit the field with appropriate rewording, dismiss as false positive, or escalate.

---

## 1/200: f-0001 - CRITICAL

**Entity:** `BMA-ALK-EML4-V1-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_alk_eml4_v1_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `E13;A20) is a stable; isoform with longer PFS on 2nd-gen ALK-TKIs vs; v1 patients show; durable responses to; in subset analyses of ALEX and J-ALEX
`

**Current value:**
```
EML4-ALK варіант 1 (E13;A20) is a stable злиття isoform with longer PFS on 2nd-gen ALK-TKIs vs варіант 3. стандарт 1L is алектиніб or лорлатиніб; v1 patients show особливо durable responses to алектиніб (~3-year медіана ВБП in subset analyses of ALEX and J-ALEX).
```

**EN excerpt:**
```
EML4-ALK variant 1 (E13;A20) is a stable fusion isoform with longer PFS on 2nd-gen ALK-TKIs vs variant 3. Standard 1L is alectinib or lorlatinib; v1 patients show particularly durab...

```

**UA excerpt:**
```
EML4-ALK варіант 1 (E13;A20) is a stable злиття isoform with longer PFS on 2nd-gen ALK-TKIs vs варіант 3. стандарт 1L is алектиніб or лорлатиніб; v1 patients show особливо durable responses to алектиніб (~3-year медіана В...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 2/200: f-0002 - CRITICAL

**Entity:** `BMA-ALK-EML4-V3-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_alk_eml4_v3_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `is associated with shorter PFS on 2nd-gen ALK-TKIs; and a higher rate of; G1202R resistance. CROWN (Solomon 2024) showed; L delivers uniformly long PFS regardless of; L choice for v
`

**Current value:**
```
EML4-ALK варіант 3 is associated with shorter PFS on 2nd-gen ALK-TKIs (кризотиніб/алектиніб) and a higher rate of набутий G1202R resistance. CROWN (Solomon 2024) showed лорлатиніб 1L delivers uniformly long PFS regardless of варіант — making лорлатиніб the переважний 1L choice for v3.
```

**EN excerpt:**
```
EML4-ALK variant 3 is associated with shorter PFS on 2nd-gen ALK-TKIs (crizotinib/alectinib) and a higher rate of acquired G1202R resistance. CROWN (Solomon 2024) showed lorlatinib...

```

**UA excerpt:**
```
EML4-ALK варіант 3 is associated with shorter PFS on 2nd-gen ALK-TKIs (кризотиніб/алектиніб) and a higher rate of набутий G1202R resistance. CROWN (Solomon 2024) showed лорлатиніб 1L delivers uniformly long PFS regardless...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 3/200: f-0003 - CRITICAL

**Entity:** `BMA-ALK-FUSION-ALCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_alk_fusion_alcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `NPM1-ALK t(2;5)) is; cured by CHOP-based; ECHELON-2: BV-CHP). For; COG NCT00939770). ALK-TKIs are an; option but not 1L
`

**Current value:**
```
ALK-positive ALCL (типово NPM1-ALK t(2;5)) is загалом cured by CHOP-based схеми with брентуксимаб ведотин (ECHELON-2: BV-CHP). For рецидивний/рефрактерний ALK+ ALCL, кризотиніб монотерапія achieves high відповідь rates (Gambacorti-Passerini 2014; педіатричний COG NCT00939770). ALK-TKIs are an усталений сальвадж option but not 1L.
```

**EN excerpt:**
```
ALK-positive ALCL (typically NPM1-ALK t(2;5)) is generally cured by CHOP-based regimens with brentuximab vedotin (ECHELON-2: BV-CHP). For relapsed/refractory ALK+ ALCL, crizotinib m...

```

**UA excerpt:**
```
ALK-positive ALCL (типово NPM1-ALK t(2;5)) is загалом cured by CHOP-based схеми with брентуксимаб ведотин (ECHELON-2: BV-CHP). For рецидивний/рефрактерний ALK+ ALCL, кризотиніб монотерапія achieves high відповідь rates (G...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 4/200: f-0005 - CRITICAL

**Entity:** `BMA-ALK-G1202R-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_alk_g1202r_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `ALK G1202R is a solvent-front; st/2nd-gen ALK-TKIs; remains active and is the; G1202R is the`

**Current value:**
```
ALK G1202R is a solvent-front мутація conferring резистентність до 1st/2nd-gen ALK-TKIs (кризотиніб, алектиніб, брігатиніб, цертиніб). лорлатиніб remains active and is the стандарт сальвадж TKI (Shaw 2019). набутий G1202R is the найбільш поширений резистентна мутація after алектиніб failure (~20-40%).
```

**EN excerpt:**
```
ALK G1202R is a solvent-front mutation conferring resistance to 1st/2nd-gen ALK-TKIs (crizotinib, alectinib, brigatinib, ceritinib). Lorlatinib remains active and is the standard sa...

```

**UA excerpt:**
```
ALK G1202R is a solvent-front мутація conferring резистентність до 1st/2nd-gen ALK-TKIs (кризотиніб, алектиніб, брігатиніб, цертиніб). лорлатиніб remains active and is the стандарт сальвадж TKI (Shaw 2019). набутий G1202R...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 5/200: f-0006 - CRITICAL

**Entity:** `BMA-ALK-L1196M-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_alk_l1196m_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `ALK L1196M is the gatekeeper; to 2nd-gen ALK-TKIs; less prevalent now that`

**Current value:**
```
ALK L1196M is the gatekeeper мутація conferring резистентність до кризотиніб but retaining чутливість to 2nd-gen ALK-TKIs (алектиніб, брігатиніб, цертиніб) and to лорлатиніб. Historically the найбільш поширений кризотиніб-резистентна мутація; less prevalent now that кризотиніб is ні longer 1L.
```

**EN excerpt:**
```
ALK L1196M is the gatekeeper mutation conferring resistance to crizotinib but retaining sensitivity to 2nd-gen ALK-TKIs (alectinib, brigatinib, ceritinib) and to lorlatinib. Histori...

```

**UA excerpt:**
```
ALK L1196M is the gatekeeper мутація conferring резистентність до кризотиніб but retaining чутливість to 2nd-gen ALK-TKIs (алектиніб, брігатиніб, цертиніб) and to лорлатиніб. Historically the найбільш поширений кризотиніб...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 6/200: f-0007 - CRITICAL

**Entity:** `BMA-ATM-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `confers ~2× lifetime breast-; TBCRC-048 ATM cohort showed minimal activity; by ER/HER2 status. ESCAT IIA (predisposition) / OncoKB; in homozygous/biallelic ATM (radiosensitivity
`

**Current value:**
```
ATM герміногенний патогенний confers ~2× lifetime breast-рак risk; ні PARPi показання (TBCRC-048 ATM cohort showed minimal activity). стандарт breast- рак терапія by ER/HER2 status. ESCAT IIA (predisposition) / OncoKB рівень 3A. Avoid променева терапія in homozygous/biallelic ATM (radiosensitivity).
```

**EN excerpt:**
```
ATM germline pathogenic confers ~2× lifetime breast-cancer risk; no PARPi indication (TBCRC-048 ATM cohort showed minimal activity). Standard breast- cancer therapy by ER/HER2 statu...

```

**UA excerpt:**
```
ATM герміногенний патогенний confers ~2× lifetime breast-рак risk; ні PARPi показання (TBCRC-048 ATM cohort showed minimal activity). стандарт breast- рак терапія by ER/HER2 status. ESCAT IIA (predisposition) / OncoKB рів...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 7/200: f-0008 - CRITICAL

**Entity:** `BMA-ATM-GERMLINE-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_germline_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `risk; PARPi activity in ATM-mutated PDAC is modest (POLO; only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or; only. ESCAT IIA / OncoKB
`

**Current value:**
```
ATM герміногенний патогенний confers ~5-10× pancreatic-рак risk; PARPi activity in ATM-mutated PDAC is modest (POLO герміногенний-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or дослідження-only. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
ATM germline pathogenic confers ~5-10× pancreatic-cancer risk; PARPi activity in ATM-mutated PDAC is modest (POLO germline-only, BRCA-restricted). NCCN recommends platinum-based che...

```

**UA excerpt:**
```
ATM герміногенний патогенний confers ~5-10× pancreatic-рак risk; PARPi activity in ATM-mutated PDAC is modest (POLO герміногенний-only, BRCA-restricted). NCCN recommends platinum-based chemo first; PARPi off-label or досл...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 8/200: f-0009 - CRITICAL

**Entity:** `BMA-ATM-GERMLINE-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_germline_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `per PROfound (Cohort A included ATM; smaller than BRCA but FDA/EMA-labeled; also include ATM in HRR- mutated populations. ESCAT IB / OncoKB
`

**Current value:**
```
ATM герміногенний патогенний in mCRPC: олапариб схвалений per PROfound (Cohort A included ATM); виграш smaller than BRCA but FDA/EMA-labeled. талазопариб+ензалутамід and олапариб+абіратерон also include ATM in HRR- mutated populations. ESCAT IB / OncoKB рівень 1.
```

**EN excerpt:**
```
ATM germline pathogenic in mCRPC: olaparib approved per PROfound (Cohort A included ATM); benefit smaller than BRCA but FDA/EMA-labeled. Talazoparib+enzalutamide and olaparib+abirat...

```

**UA excerpt:**
```
ATM герміногенний патогенний in mCRPC: олапариб схвалений per PROfound (Cohort A included ATM); виграш smaller than BRCA but FDA/EMA-labeled. талазопариб+ензалутамід and олапариб+абіратерон also include ATM in HRR- mutate...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 9/200: f-0010 - CRITICAL

**Entity:** `BMA-ATM-LOSS-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_loss_cll.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `ATM loss in CLL (del(11q) or; FCR), but BTK; abrogate this risk. Avoid FCR in ATM-deficient CLL. ESCAT IIA`

**Current value:**
```
ATM loss in CLL (del(11q) or соматичний мутація): historically poor-прогностичний with хіміоімунотерапія (FCR), but BTK інгібітори (ібрутиніб, акалабрутиніб, занубрутиніб) and венетоклакс+обінутузумаб abrogate this risk. Avoid FCR in ATM-deficient CLL. ESCAT IIA (лікування-modifying) / OncoKB рівень 3A.
```

**EN excerpt:**
```
ATM loss in CLL (del(11q) or somatic mutation): historically poor-prognostic with chemoimmunotherapy (FCR), but BTK inhibitors (ibrutinib, acalabrutinib, zanubrutinib) and venetocla...

```

**UA excerpt:**
```
ATM loss in CLL (del(11q) or соматичний мутація): historically poor-прогностичний with хіміоімунотерапія (FCR), but BTK інгібітори (ібрутиніб, акалабрутиніб, занубрутиніб) and венетоклакс+обінутузумаб abrogate this risk....

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 10/200: f-0011 - CRITICAL

**Entity:** `BMA-ATM-LOSS-MCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_loss_mcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `ATM is the; in MCL (~40-50%). Not directly; BTKi, R-CHOP/R-DHAP; ASCT, BR) apply. ATM loss may sensitize to ATR; in trials. ESCAT IIA (biological) / OncoKB
`

**Current value:**
```
ATM is the найбільш поширений соматичний мутація in MCL (~40-50%). Not directly терапія-selecting; стандарт MCL схеми (BTKi, R-CHOP/R-DHAP індукція + ASCT, BR) apply. ATM loss may sensitize to ATR інгібітори in trials. ESCAT IIA (biological) / OncoKB рівень 3A.
```

**EN excerpt:**
```
ATM is the most common somatic mutation in MCL (~40-50%). Not directly therapy-selecting; standard MCL regimens (BTKi, R-CHOP/R-DHAP induction + ASCT, BR) apply. ATM loss may sensit...

```

**UA excerpt:**
```
ATM is the найбільш поширений соматичний мутація in MCL (~40-50%). Not directly терапія-selecting; стандарт MCL схеми (BTKi, R-CHOP/R-DHAP індукція + ASCT, BR) apply. ATM loss may sensitize to ATR інгібітори in trials. ES...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 11/200: f-0012 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in breast: minimal PARPi activity in ATM-only basket arms; by HR/HER2 status. ESCAT IIIA / OncoKB
`

**Current value:**
```
соматичний ATM втрата функції in breast: minimal PARPi activity in ATM-only basket arms; лікування by HR/HER2 status. ESCAT IIIA / OncoKB рівень 4.
```

**EN excerpt:**
```
Somatic ATM loss-of-function in breast: minimal PARPi activity in ATM-only basket arms; treatment by HR/HER2 status. ESCAT IIIA / OncoKB Level 4.

```

**UA excerpt:**
```
соматичний ATM втрата функції in breast: minimal PARPi activity in ATM-only basket arms; лікування by HR/HER2 status. ESCAT IIIA / OncoKB рівень 4.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 12/200: f-0013 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `may be enhanced. PARPi off-label only. ESCAT IIA / OncoKB`

**Current value:**
```
соматичний ATM втрата функції in PDAC: обмежені докази; platinum чутливість may be enhanced. PARPi off-label only. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
Somatic ATM loss-of-function in PDAC: limited evidence; platinum sensitivity may be enhanced. PARPi off-label only. ESCAT IIA / OncoKB Level 3A.

```

**UA excerpt:**
```
соматичний ATM втрата функції in PDAC: обмежені докази; platinum чутливість may be enhanced. PARPi off-label only. ESCAT IIA / OncoKB рівень 3A.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 13/200: f-0014 - CRITICAL

**Entity:** `BMA-ATM-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_atm_somatic_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mCRPC: PROfound enrolled both; ATM in Cohort A; covers both. ESCAT IB / OncoKB
`

**Current value:**
```
соматичний ATM втрата функції in mCRPC: PROfound enrolled both герміногенний and соматичний ATM in Cohort A; олапариб показання covers both. ESCAT IB / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic ATM loss-of-function in mCRPC: PROfound enrolled both germline and somatic ATM in Cohort A; olaparib indication covers both. ESCAT IB / OncoKB Level 1.

```

**UA excerpt:**
```
соматичний ATM втрата функції in mCRPC: PROfound enrolled both герміногенний and соматичний ATM in Cohort A; олапариб показання covers both. ESCAT IB / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 14/200: f-0015 - CRITICAL

**Entity:** `BMA-BARD1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `confers moderate breast-; risk (~2-3×). BARD1 forms heterodimer with BRCA1 → biological HR deficiency. Limited clinical PARPi; off-label consideration. ESCAT IIA / OncoKB
`

**Current value:**
```
BARD1 герміногенний патогенний confers moderate breast-рак risk (~2-3×). BARD1 forms heterodimer with BRCA1 → biological HR deficiency. Limited clinical PARPi дані; off-label consideration. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
BARD1 germline pathogenic confers moderate breast-cancer risk (~2-3×). BARD1 forms heterodimer with BRCA1 → biological HR deficiency. Limited clinical PARPi data; off-label consider...

```

**UA excerpt:**
```
BARD1 герміногенний патогенний confers moderate breast-рак risk (~2-3×). BARD1 forms heterodimer with BRCA1 → biological HR deficiency. Limited clinical PARPi дані; off-label consideration. ESCAT IIA / OncoKB рівень 3A.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 15/200: f-0016 - CRITICAL

**Entity:** `BMA-BARD1-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `included in HRR panels; PARPi; extrapolated from HRD-positive; subgroups (PAOLA-1, NOVA non-gBRCA). ESCAT IIB / OncoKB
`

**Current value:**
```
BARD1 герміногенний патогенний in EOC: рідкісний; included in HRR panels; PARPi виграш extrapolated from HRD-positive дослідження subgroups (PAOLA-1, NOVA non-gBRCA). ESCAT IIB / OncoKB рівень 3B.
```

**EN excerpt:**
```
BARD1 germline pathogenic in EOC: rare; included in HRR panels; PARPi benefit extrapolated from HRD-positive trial subgroups (PAOLA-1, NOVA non-gBRCA). ESCAT IIB / OncoKB Level 3B.

```

**UA excerpt:**
```
BARD1 герміногенний патогенний in EOC: рідкісний; included in HRR panels; PARPi виграш extrapolated from HRD-positive дослідження subgroups (PAOLA-1, NOVA non-gBRCA). ESCAT IIB / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 16/200: f-0017 - CRITICAL

**Entity:** `BMA-BARD1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BARD1 in breast; biological HRR rationale only. ESCAT IIIA / OncoKB`

**Current value:**
```
соматичний BARD1 in breast: рідкісний; biological HRR rationale only. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
Somatic BARD1 in breast: rare; biological HRR rationale only. ESCAT IIIA / OncoKB Level 3B.

```

**UA excerpt:**
```
соматичний BARD1 in breast: рідкісний; biological HRR rationale only. ESCAT IIIA / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 17/200: f-0018 - CRITICAL

**Entity:** `BMA-BARD1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bard1_somatic_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BARD1 in EOC: HRR panel inclusion variable; PARPi off-label consideration in HRD-positive context. ESCAT IIB / OncoKB
`

**Current value:**
```
соматичний BARD1 in EOC: HRR panel inclusion variable; PARPi off-label consideration in HRD-positive context. ESCAT IIB / OncoKB рівень 3B.
```

**EN excerpt:**
```
Somatic BARD1 in EOC: HRR panel inclusion variable; PARPi off-label consideration in HRD-positive context. ESCAT IIB / OncoKB Level 3B.

```

**UA excerpt:**
```
соматичний BARD1 in EOC: HRR panel inclusion variable; PARPi off-label consideration in HRD-positive context. ESCAT IIB / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 18/200: f-0019 - CRITICAL

**Entity:** `BMA-BCL2-EXPRESSION-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_expression_cll.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CLL universally expresses BCL; needed; driven by miR-; based fixed-duration (CLL14: VenO 1L; MURANO: VenR; defining as a target. Not; selected per se — BCL2 is a CLL-class marker
`

**Current value:**
```
CLL universally expresses BCL2 (ні перебудова needed; driven by miR-15/16 делеція at 13q14). венетоклакс-based fixed-duration (CLL14: VenO 1L; MURANO: VenR р/р) is FDA/схвалений EMA and хвороба-defining as a target. Not біомаркер-selected per se — BCL2 is a CLL-class marker.
```

**EN excerpt:**
```
CLL universally expresses BCL2 (no rearrangement needed; driven by miR-15/16 deletion at 13q14). Venetoclax-based fixed-duration (CLL14: VenO 1L; MURANO: VenR R/R) is FDA/EMA-approv...

```

**UA excerpt:**
```
CLL universally expresses BCL2 (ні перебудова needed; driven by miR-15/16 делеція at 13q14). венетоклакс-based fixed-duration (CLL14: VenO 1L; MURANO: VenR р/р) is FDA/схвалений EMA and хвороба-defining as a target. Not б...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 19/200: f-0020 - CRITICAL

**Entity:** `BMA-BCL2-EXPRESSION-DLBCL-NOS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_expression_dlbcl_nos.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `High BCL2 IHC; in GCB and ABC subsets. 'Dual-expressor' (BCL2+MYC IHC ≥40-50% / ≥70%) is; but distinct from HGBL-DH; CAVALLI Ph2). Not
`

**Current value:**
```
High BCL2 IHC експресія in DLBCL — поширений in GCB and ABC subsets. 'Dual-expressor' (BCL2+MYC IHC ≥40-50% / ≥70%) is несприятливий but distinct from HGBL-DH (перебудова-defined). венетоклакс + R-CHOP експериментальний (CAVALLI Ph2). Not біомаркер-selected for венетоклакс in DLBCL.
```

**EN excerpt:**
```
High BCL2 IHC expression in DLBCL — common in GCB and ABC subsets. 'Dual-expressor' (BCL2+MYC IHC ≥40-50% / ≥70%) is adverse but distinct from HGBL-DH (rearrangement-defined). Venet...

```

**UA excerpt:**
```
High BCL2 IHC експресія in DLBCL — поширений in GCB and ABC subsets. 'Dual-expressor' (BCL2+MYC IHC ≥40-50% / ≥70%) is несприятливий but distinct from HGBL-DH (перебудова-defined). венетоклакс + R-CHOP експериментальний (...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 20/200: f-0021 - CRITICAL

**Entity:** `BMA-BCL2-EXPRESSION-FL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_expression_fl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `universal in FL (driven by t; selecting in 1L`

**Current value:**
```
High BCL2 експресія universal in FL (driven by t(14;18)). діагностичний but not терапія-selecting in 1L.
```

**EN excerpt:**
```
High BCL2 expression universal in FL (driven by t(14;18)). Diagnostic but not therapy-selecting in 1L.
```

**UA excerpt:**
```
High BCL2 експресія universal in FL (driven by t(14;18)). діагностичний but not терапія-selecting in 1L.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 21/200: f-0022 - CRITICAL

**Entity:** `BMA-BCL2-EXPRESSION-MCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_expression_mcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `High BCL2 in MCL universal (cyclin D1-driven; Tam NEJM 2018) active in`

**Current value:**
```
High BCL2 in MCL universal (cyclin D1-driven виживаність pathway). венетоклакс + ібрутиніб (AIM дослідження; Tam NEJM 2018) active in р/р MCL — off-label.
```

**EN excerpt:**
```
High BCL2 in MCL universal (cyclin D1-driven survival pathway). Venetoclax + ibrutinib (AIM trial; Tam NEJM 2018) active in R/R MCL — off-label.

```

**UA excerpt:**
```
High BCL2 in MCL universal (cyclin D1-driven виживаність pathway). венетоклакс + ібрутиніб (AIM дослідження; Tam NEJM 2018) active in р/р MCL — off-label.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 22/200: f-0023 - CRITICAL

**Entity:** `BMA-BCL2-REARRANGEMENT-DLBCL-NOS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_rearrangement_dlbcl_nos.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `from FL. Not; Treat per DLBCL-NOS algorithm`

**Current value:**
```
Isolated BCL2 перебудова in DLBCL (ні MYC partner) — поширений in GCB-DLBCL трансформований from FL. Not еквівалентний to DH лімфома. Treat per DLBCL-NOS algorithm; венетоклакс експериментальний.
```

**EN excerpt:**
```
Isolated BCL2 rearrangement in DLBCL (no MYC partner) — common in GCB-DLBCL transformed from FL. Not equivalent to DH lymphoma. Treat per DLBCL-NOS algorithm; venetoclax investigati...

```

**UA excerpt:**
```
Isolated BCL2 перебудова in DLBCL (ні MYC partner) — поширений in GCB-DLBCL трансформований from FL. Not еквівалентний to DH лімфома. Treat per DLBCL-NOS algorithm; венетоклакс експериментальний.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 23/200: f-0024 - CRITICAL

**Entity:** `BMA-BCL2-REARRANGEMENT-FL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_rearrangement_fl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `t(14;18) IGH/BCL2 is the defining genetic lesion of; Drives constitutive BCL; modest activity in FL (Davids JCO 2017 ORR ~38%); combos with R-CHOP (CONTRALTO) and; L (BR, R-CHOP; chemo) effective regardless of BCL2-R presence
`

**Current value:**
```
t(14;18) IGH/BCL2 is the defining genetic lesion of фолікулярна лімфома (~85%). Drives constitutive BCL2 гіперекспресія. венетоклакс монотерапія modest activity in FL (Davids JCO 2017 ORR ~38%); combos with R-CHOP (CONTRALTO) and обінутузумаб in дослідження. стандарт 1L (BR, R-CHOP, обінутузумаб + chemo) effective regardless of BCL2-R presence.
```

**EN excerpt:**
```
t(14;18) IGH/BCL2 is the defining genetic lesion of follicular lymphoma (~85%). Drives constitutive BCL2 overexpression. Venetoclax monotherapy modest activity in FL (Davids JCO 201...

```

**UA excerpt:**
```
t(14;18) IGH/BCL2 is the defining genetic lesion of фолікулярна лімфома (~85%). Drives constitutive BCL2 гіперекспресія. венетоклакс монотерапія modest activity in FL (Davids JCO 2017 ORR ~38%); combos with R-CHOP (CONTRA...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 24/200: f-0025 - CRITICAL

**Entity:** `BMA-BCL2-REARRANGEMENT-HGBL-DH`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_rearrangement_hgbl_dh.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCL2-R as the partner of MYC-R defines HGBL-DH. Same management as MYC-R cell: DA-EPOCH-R 1L
`

**Current value:**
```
BCL2-R as the partner of MYC-R defines HGBL-DH. Same management as MYC-R cell: DA-EPOCH-R 1L переважний per найбільш series.
```

**EN excerpt:**
```
BCL2-R as the partner of MYC-R defines HGBL-DH. Same management as MYC-R cell: DA-EPOCH-R 1L preferred per most series.

```

**UA excerpt:**
```
BCL2-R as the partner of MYC-R defines HGBL-DH. Same management as MYC-R cell: DA-EPOCH-R 1L переважний per найбільш series.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 25/200: f-0026 - CRITICAL

**Entity:** `BMA-BCL2-REARRANGEMENT-MCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcl2_rearrangement_mcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in MCL is very; MCL algorithm continues`

**Current value:**
```
BCL2 перебудова in MCL is very рідкісний and зазвичай denotes composite лімфома or трансформація. стандарт MCL algorithm continues.
```

**EN excerpt:**
```
BCL2 rearrangement in MCL is very rare and usually denotes composite lymphoma or transformation. Standard MCL algorithm continues.

```

**UA excerpt:**
```
BCL2 перебудова in MCL is very рідкісний and зазвичай denotes composite лімфома or трансформація. стандарт MCL algorithm continues.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 26/200: f-0027 - CRITICAL

**Entity:** `BMA-BCR-ABL1-E255K-CML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_e255k_cml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCR-ABL1 E255K/V is a P-loop; is fully active. P-loop; historically associated with`

**Current value:**
```
BCR-ABL1 E255K/V is a P-loop мутація conferring strong резистентність до іматиніб and зменшений чутливість to нілотиніб. дазатиніб retains activity; понатиніб is fully active. P-loop мутації historically associated with гірше outcomes — consider понатиніб early.
```

**EN excerpt:**
```
BCR-ABL1 E255K/V is a P-loop mutation conferring strong resistance to imatinib and reduced sensitivity to nilotinib. Dasatinib retains activity; ponatinib is fully active. P-loop mu...

```

**UA excerpt:**
```
BCR-ABL1 E255K/V is a P-loop мутація conferring strong резистентність до іматиніб and зменшений чутливість to нілотиніб. дазатиніб retains activity; понатиніб is fully active. P-loop мутації historically associated with г...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 27/200: f-0028 - CRITICAL

**Entity:** `BMA-BCR-ABL1-F317L-BALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_f317l_ball.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `F317L in Ph+ B-ALL — same kinase-domain consequence as in CML; resistance with retained`

**Current value:**
```
F317L in Ph+ B-ALL — same kinase-domain consequence as in CML: дазатиніб resistance with retained чутливість to нілотиніб and понатиніб. In ALL, понатиніб + chemo or блінатумомаб is переважний switch given хвороба tempo.
```

**EN excerpt:**
```
F317L in Ph+ B-ALL — same kinase-domain consequence as in CML: dasatinib resistance with retained sensitivity to nilotinib and ponatinib. In ALL, ponatinib + chemo or blinatumomab i...

```

**UA excerpt:**
```
F317L in Ph+ B-ALL — same kinase-domain consequence as in CML: дазатиніб resistance with retained чутливість to нілотиніб and понатиніб. In ALL, понатиніб + chemo or блінатумомаб is переважний switch given хвороба tempo.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 28/200: f-0029 - CRITICAL

**Entity:** `BMA-BCR-ABL1-F317L-CML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_f317l_cml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCR-ABL1 F317L confers; Soverini 2011, in vitro; panels). Switch to`

**Current value:**
```
BCR-ABL1 F317L confers резистентність до дазатиніб but retains чутливість to нілотиніб, бозутиніб, and понатиніб (Soverini 2011, in vitro чутливість panels). Switch to нілотиніб or бозутиніб is стандарт per ELN 2020/2025 мутація-guided algorithm.
```

**EN excerpt:**
```
BCR-ABL1 F317L confers resistance to dasatinib but retains sensitivity to nilotinib, bosutinib, and ponatinib (Soverini 2011, in vitro sensitivity panels). Switch to nilotinib or bo...

```

**UA excerpt:**
```
BCR-ABL1 F317L confers резистентність до дазатиніб but retains чутливість to нілотиніб, бозутиніб, and понатиніб (Soverini 2011, in vitro чутливість panels). Switch to нілотиніб or бозутиніб is стандарт per ELN 2020/2025...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 29/200: f-0030 - CRITICAL

**Entity:** `BMA-BCR-ABL1-P190-BALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_p190_ball.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `p190) requires TKI-incorporating; Modern trials (D-ALBA, Foà 2020; GIMEMA LAL2116) show; achieves molecular CR in >60% with; hyper-CVAD (Jabbour 2024) and; combos extend this further. TKI selection now favors
`

**Current value:**
```
Ph+ B-ALL (типово p190) requires TKI-incorporating схеми. Modern trials (D-ALBA, Foà 2020; GIMEMA LAL2116) show дазатиніб + блінатумомаб achieves molecular CR in >60% with зменшений хіміотерапія. понатиніб + hyper-CVAD (Jabbour 2024) and понатиніб + блінатумомаб combos extend this further. TKI selection now favors понатиніб for найвища molecular-відповідь rates.
```

**EN excerpt:**
```
Ph+ B-ALL (typically p190) requires TKI-incorporating regimens. Modern trials (D-ALBA, Foà 2020; GIMEMA LAL2116) show dasatinib + blinatumomab achieves molecular CR in >60% with red...

```

**UA excerpt:**
```
Ph+ B-ALL (типово p190) requires TKI-incorporating схеми. Modern trials (D-ALBA, Foà 2020; GIMEMA LAL2116) show дазатиніб + блінатумомаб achieves molecular CR in >60% with зменшений хіміотерапія. понатиніб + hyper-CVAD (J...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 30/200: f-0031 - CRITICAL

**Entity:** `BMA-BCR-ABL1-P210-BALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_p210_ball.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `p210 BCR-ABL1 in B-ALL (~30% of; Ph+ ALL, much rarer in; needs careful distinction from CML in lymphoid blast crisis; principles mirror p190 Ph+ ALL: TKI; limited by rarity but appear
`

**Current value:**
```
p210 BCR-ABL1 in B-ALL (~30% of дорослий Ph+ ALL, much rarer in педіатричний) — needs careful distinction from CML in lymphoid blast crisis. лікування principles mirror p190 Ph+ ALL: TKI + хіміотерапія or TKI + блінатумомаб. Outcomes дані limited by rarity but appear співставний з p190.
```

**EN excerpt:**
```
p210 BCR-ABL1 in B-ALL (~30% of adult Ph+ ALL, much rarer in pediatric) — needs careful distinction from CML in lymphoid blast crisis. Treatment principles mirror p190 Ph+ ALL: TKI...

```

**UA excerpt:**
```
p210 BCR-ABL1 in B-ALL (~30% of дорослий Ph+ ALL, much rarer in педіатричний) — needs careful distinction from CML in lymphoid blast crisis. лікування principles mirror p190 Ph+ ALL: TKI + хіміотерапія or TKI + блінатумом...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 31/200: f-0032 - CRITICAL

**Entity:** `BMA-BCR-ABL1-P210-CML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_p210_cml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCR-ABL1 p210 (e13a2/e14a2) defines chronic-phase CML and is the paradigm targeted-; L (IRIS, O'Brien; BCR-ABL1 TKI as; achieve faster, deeper molecular responses with; ASCEMBL, Réa 2021) is the first STAMP-class allosteric TKI for resistant
`

**Current value:**
```
BCR-ABL1 p210 (e13a2/e14a2) defines chronic-phase CML and is the paradigm targeted-терапія success story. іматиніб 1L (IRIS, O'Brien 2003) усталений BCR-ABL1 TKI as стандарт; 2nd-gen TKIs (дазатиніб/нілотиніб/бозутиніб) achieve faster, deeper molecular responses with подібний OS. асциминіб (ASCEMBL, Réa 2021) is the first STAMP-class allosteric TKI for resistant хвороба.
```

**EN excerpt:**
```
BCR-ABL1 p210 (e13a2/e14a2) defines chronic-phase CML and is the paradigm targeted-therapy success story. Imatinib 1L (IRIS, O'Brien 2003) established BCR-ABL1 TKI as standard; 2nd-...

```

**UA excerpt:**
```
BCR-ABL1 p210 (e13a2/e14a2) defines chronic-phase CML and is the paradigm targeted-терапія success story. іматиніб 1L (IRIS, O'Brien 2003) усталений BCR-ABL1 TKI as стандарт; 2nd-gen TKIs (дазатиніб/нілотиніб/бозутиніб) a...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 32/200: f-0033 - CRITICAL

**Entity:** `BMA-BCR-ABL1-T315I-BALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_t315i_ball.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `T315I in Ph+ B-ALL — same biological consequence as in CML: pan-; st/2nd-gen TKIs; T315I is more; in B-ALL than CML; due to faster; tempo and higher; pressure under early TKI exposure
`

**Current value:**
```
T315I in Ph+ B-ALL — same biological consequence as in CML: pan-резистентність до 1st/2nd-gen TKIs. понатиніб + хіміотерапія is стандарт (Jabbour 2018, hyper-CVAD + понатиніб). T315I is more поширений in B-ALL than CML при зверненні due to faster хвороба tempo and higher мутація pressure under early TKI exposure.
```

**EN excerpt:**
```
T315I in Ph+ B-ALL — same biological consequence as in CML: pan-resistance to 1st/2nd-gen TKIs. Ponatinib + chemotherapy is standard (Jabbour 2018, hyper-CVAD + ponatinib). T315I is...

```

**UA excerpt:**
```
T315I in Ph+ B-ALL — same biological consequence as in CML: pan-резистентність до 1st/2nd-gen TKIs. понатиніб + хіміотерапія is стандарт (Jabbour 2018, hyper-CVAD + понатиніб). T315I is more поширений in B-ALL than CML пр...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 33/200: f-0034 - CRITICAL

**Entity:** `BMA-BCR-ABL1-T315I-CML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_t315i_cml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCR-ABL1 T315I is the gatekeeper; PACE, Cortes 2013) is; T315I+ CML; mg BID) also has T315I activity per ASCEMBL extension and dedicated cohorts. Allo-HCT remains a; option in eligible patients
`

**Current value:**
```
BCR-ABL1 T315I is the gatekeeper мутація conferring pan-резистентність до іматиніб, дазатиніб, нілотиніб, and бозутиніб. понатиніб (PACE, Cortes 2013) is схвалений для T315I+ CML. асциминіб (allosteric STAMP інгібітор) at higher доза (200 mg BID) also has T315I activity per ASCEMBL extension and dedicated cohorts. Allo-HCT remains a сальвадж option in eligible patients.
```

**EN excerpt:**
```
BCR-ABL1 T315I is the gatekeeper mutation conferring pan-resistance to imatinib, dasatinib, nilotinib, and bosutinib. Ponatinib (PACE, Cortes 2013) is approved for T315I+ CML. Ascim...

```

**UA excerpt:**
```
BCR-ABL1 T315I is the gatekeeper мутація conferring pan-резистентність до іматиніб, дазатиніб, нілотиніб, and бозутиніб. понатиніб (PACE, Cortes 2013) is схвалений для T315I+ CML. асциминіб (allosteric STAMP інгібітор) at...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 34/200: f-0035 - CRITICAL

**Entity:** `BMA-BCR-ABL1-V299L-CML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_bcr_abl1_v299l_cml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BCR-ABL1 V299L confers; reserved for multi-TKI-resistant`

**Current value:**
```
BCR-ABL1 V299L confers резистентність до дазатиніб and бозутиніб but retains чутливість to нілотиніб and понатиніб. Switch to нілотиніб is стандарт сальвадж; понатиніб reserved for multi-TKI-resistant.
```

**EN excerpt:**
```
BCR-ABL1 V299L confers resistance to dasatinib and bosutinib but retains sensitivity to nilotinib and ponatinib. Switch to nilotinib is standard salvage; ponatinib reserved for mult...

```

**UA excerpt:**
```
BCR-ABL1 V299L confers резистентність до дазатиніб and бозутиніб but retains чутливість to нілотиніб and понатиніб. Switch to нілотиніб is стандарт сальвадж; понатиніб reserved for multi-TKI-resistant.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 35/200: f-0036 - CRITICAL

**Entity:** `BMA-BRAF-CLASS3-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_class3_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `Class 2 BRAF (e.g., K601E, L597, fusions) — RAS-independent`

**Current value:**
```
Class 2 BRAF (e.g., K601E, L597, fusions) — RAS-independent, signal as dimers. Class 3 BRAF (e.g., G466, N581, D594) — kinase-impaired, RAS-dependent. Neither responds well to V600E-targeted вемурафеніб. траметиніб монотерапія or MEKi + pan-RAF інгібітори under investigation. NCI-MATCH subprotocol H (траметиніб for non-V600 BRAF) showed limited responses.
```

**EN excerpt:**
```
'Class 2 BRAF (e.g., K601E, L597, fusions) — RAS-independent, signal
```

**UA excerpt:**
```
'Class 2 BRAF (e.g., K601E, L597, fusions) — RAS-independent,
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 36/200: f-0037 - CRITICAL

**Entity:** `BMA-BRAF-V600E-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in AML is; more in histiocytic disorders`

**Current value:**
```
BRAF V600E in AML is рідкісний (<1%, more in histiocytic disorders / mixed-фенотип acute лейкоз with histiocytic component). Tissue-agnostic дабрафеніб + траметиніб not схвалений in heme. off-label use case-report level; consider in BRAF V600E AML with myeloid/dendritic mixed lineage.
```

**EN excerpt:**
```
'BRAF V600E in AML is rare (<1%, more in histiocytic disorders /
```

**UA excerpt:**
```
'BRAF V600E in AML is рідкісний (<1%, more in histiocytic disorders
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 37/200: f-0038 - CRITICAL

**Entity:** `BMA-BRAF-V600E-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_cholangio.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in cholangiocarcinoma (mainly intrahepatic`

**Current value:**
```
BRAF V600E in cholangiocarcinoma (mainly intrahepatic, ~5%) is a пухлина-agnostic FDA Level-1 actionable target. дабрафеніб + траметиніб is рекомендований for previously-treated BRAF V600E cholangiocarcinoma per SRC-NCCN-HEPATOBILIARY based on the ROAR basket дослідження (Subbiah Lancet Oncol 2020 — biliary tract cohort ORR 51%, mPFS 9 міс., міс. 14 міс.). 1L remains гемцитабін + цисплатин ± дурвалумаб (TOPAZ-1) for найбільш patients; testing for BRAF V600E is рекомендований при діагнозі to plan 2L+ in patients without other actionable альтерації (FGFR2 злиття, IDH1 мутація) per SRC-NCCN-HEPATOBILIARY.
```

**EN excerpt:**
```
'BRAF V600E in cholangiocarcinoma (mainly intrahepatic, ~5%) is
```

**UA excerpt:**
```
'BRAF V600E in cholangiocarcinoma (mainly intrahepatic, ~5%)
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 38/200: f-0039 - CRITICAL

**Entity:** `BMA-BRAF-V600E-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_cll.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in CLL is very; does not change`

**Current value:**
```
BRAF V600E in CLL is very рідкісний (~1-3%); does not change стандарт management (BTKi or венетоклакс-based fixed-duration). Tissue- agnostic BRAFi off-label only.
```

**EN excerpt:**
```
'BRAF V600E in CLL is very rare (~1-3%); does not change standard
```

**UA excerpt:**
```
'BRAF V600E in CLL is very рідкісний (~1-3%); does not change
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 39/200: f-0040 - CRITICAL

**Entity:** `BMA-BRAF-V600E-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in`

**Current value:**
```
BRAF V600E in метастатичний CRC: енкорафеніб + цетуксимаб (with or without біниметиніб) покращує OS vs цетуксимаб+іринотекан in 2L+ (BEACON-CRC, Kopetz et al. 2019). BRAFi монотерапія is ineffective in CRC due to EGFR-mediated feedback reactivation — distinct from меланома where BRAFi alone works.
```

**EN excerpt:**
```
'BRAF V600E in metastatic CRC: encorafenib + cetuximab (with or

```

**UA excerpt:**
```
'BRAF V600E in метастатичний CRC: енкорафеніб + цетуксимаб (with

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 40/200: f-0041 - CRITICAL

**Entity:** `BMA-BRAF-V600E-DLBCL-NOS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_dlbcl_nos.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in DLBCL is exceptional. Tissue-agnostic`

**Current value:**
```
BRAF V600E in DLBCL is exceptional. Tissue-agnostic дабрафеніб + траметиніб could be considered after стандарт lines exhausted.
```

**EN excerpt:**
```
'BRAF V600E in DLBCL is exceptional. Tissue-agnostic dabrafenib
```

**UA excerpt:**
```
'BRAF V600E in DLBCL is exceptional. Tissue-agnostic дабрафеніб
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 41/200: f-0042 - CRITICAL

**Entity:** `BMA-BRAF-V600E-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in`

**Current value:**
```
BRAF V600E in дорослий-type гліобластома is рідкісний (~1-3%) but more поширений in epithelioid GBM and педіатричний високого ступеня glioma. дабрафеніб + траметиніб is tissue-agnostic схвалений FDA (2022) for BRAF V600E solid tumors after прогресування on prior терапія — covers BRAF V600E GBM (Wen et al. ROAR-glioma 2022, ORR 33% in HGG). Vorasidenib does NOT apply here (IDH-mutant only).
```

**EN excerpt:**
```
'BRAF V600E in adult-type glioblastoma is rare (~1-3%) but more
```

**UA excerpt:**
```
'BRAF V600E in дорослий-type гліобластома is рідкісний (~1-3%)
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 42/200: f-0043 - CRITICAL

**Entity:** `BMA-BRAF-V600E-HCC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_hcc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in HCC is exceptional (<1%). Tissue-agnostic`

**Current value:**
```
BRAF V600E in HCC is exceptional (<1%). Tissue-agnostic дабрафеніб + траметиніб could be considered after стандарт lines.
```

**EN excerpt:**
```
'BRAF V600E in HCC is exceptional (<1%). Tissue-agnostic dabrafenib
```

**UA excerpt:**
```
'BRAF V600E in HCC is exceptional (<1%). Tissue-agnostic дабрафеніб
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 43/200: f-0044 - CRITICAL

**Entity:** `BMA-BRAF-V600E-HCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_hcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E is the defining molecular lesion of classic`

**Current value:**
```
BRAF V600E is the defining molecular lesion of classic волосатоклітинний лейкоз (~100% of cHCL; absent in HCL-варіант). вемурафеніб монотерапія yields CR ~35% / ORR ~96% in рецидивний/рефрактерний cHCL (Tiacci et al. NEJM 2015). вемурафеніб + ритуксимаб gives durable CR in ~87% (Tiacci et al. NEJM 2021). дабрафеніб + траметиніб also active. Used as сальвадж after purine-analog failure or in кладрибін-ineligible patients.
```

**EN excerpt:**
```
'BRAF V600E is the defining molecular lesion of classic hairy cell
```

**UA excerpt:**
```
'BRAF V600E is the defining molecular lesion of classic волосатоклітинний
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 44/200: f-0045 - CRITICAL

**Entity:** `BMA-BRAF-V600E-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E (and V600K) in cutaneous; is the prototypical`

**Current value:**
```
BRAF V600E (and V600K) in cutaneous меланома is the prototypical driver: комбінація BRAF + MEK inhibition (дабрафеніб + траметиніб; енкорафеніб + біниметиніб; вемурафеніб + кобіметиніб) yields high ORR (~65-70%) and покращує OS vs single-agent BRAFi (COMBI-d/v, coBRIM, COLUMBUS). ад'ювантний дабрафеніб + траметиніб покращує RFS in resected stage III (COMBI-AD). триплет with anti-PD-1 (атезолізумаб + вемурафеніб + кобіметиніб; IMspire150) extends PFS over дублет.
```

**EN excerpt:**
```
'BRAF V600E (and V600K) in cutaneous melanoma is the prototypical
```

**UA excerpt:**
```
'BRAF V600E (and V600K) in cutaneous меланома is the prototypical
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 45/200: f-0046 - CRITICAL

**Entity:** `BMA-BRAF-V600E-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_mm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E is found in ~4% of`

**Current value:**
```
BRAF V600E is found in ~4% of множинна мієлома при діагнозі (more in extramedullary / plasma cell лейкоз). Case series and small prospective cohorts (Andrulis et al. 2013, Sharman et al. 2015) document responses to вемурафеніб монотерапія and BRAFi+MEKi combinations off-label, особливо in plasmablastic / агресивний р/р хвороба. Not стандарт-of-care; tissue-agnostic дабрафеніб + траметиніб (BRAF V600E solid пухлина схвалення 2022) does not formally extend to heme but is invoked as off-label rationale.
```

**EN excerpt:**
```
'BRAF V600E is found in ~4% of multiple myeloma at diagnosis (more
```

**UA excerpt:**
```
'BRAF V600E is found in ~4% of множинна мієлома при діагнозі
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 46/200: f-0047 - CRITICAL

**Entity:** `BMA-BRAF-V600E-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in; NSCLC (≈1-2% of adenocarcinomas`

**Current value:**
```
BRAF V600E in поширений NSCLC (≈1-2% of adenocarcinomas): дабрафеніб + траметиніб gives ORR ~64% in 1L (Planchard et al. Lancet Oncol 2017) and is FDA/схвалений EMA across lines. енкорафеніб + біниметиніб (PHAROS, Riely et al. JCO 2023) ORR 75% in без попереднього лікування, 46% pretreated — also схвалений FDA 2023.
```

**EN excerpt:**
```
'BRAF V600E in advanced NSCLC (≈1-2% of adenocarcinomas): dabrafenib

```

**UA excerpt:**
```
'BRAF V600E in поширений NSCLC (≈1-2% of adenocarcinomas): дабрафеніб

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 47/200: f-0048 - CRITICAL

**Entity:** `BMA-BRAF-V600E-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E is a`

**Current value:**
```
BRAF V600E is a рецидивний driver in низького ступеня serous ovarian карцинома (LGSOC) — ~30% of LGSOC. Tissue-agnostic FDA схвалення of дабрафеніб + траметиніб for BRAF V600E solid tumors (Subbiah et al. ROAR; Salama et al. NCI-MATCH 2020) covers ovarian. ORR ~33% in basket trials. MEK інгібітори (траметиніб, біниметиніб) also active in LGSOC regardless of BRAF status (MILO, GOG 281).
```

**EN excerpt:**
```
'BRAF V600E is a recurrent driver in low-grade serous ovarian carcinoma
```

**UA excerpt:**
```
'BRAF V600E is a рецидивний driver in низького ступеня serous
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 48/200: f-0049 - CRITICAL

**Entity:** `BMA-BRAF-V600E-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in PDAC; in KRAS-WT subset). Tissue-`

**Current value:**
```
BRAF V600E in PDAC (~1-3%, часто in KRAS-WT subset). Tissue- agnostic дабрафеніб + траметиніб (FDA 2022) схвалений для нерезектабельний/метастатичний V600E solid tumors after prior терапія. Consider after FOLFIRINOX failure in BRAF V600E PDAC.
```

**EN excerpt:**
```
'BRAF V600E in PDAC (~1-3%, often in KRAS-WT subset). Tissue- agnostic
```

**UA excerpt:**
```
'BRAF V600E in PDAC (~1-3%, часто in KRAS-WT subset). Tissue-
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 49/200: f-0050 - CRITICAL

**Entity:** `BMA-BRAF-V600E-THYROID-ANAPLASTIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600e_thyroid_anaplastic.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600E in anaplastic thyroid`

**Current value:**
```
BRAF V600E in anaplastic thyroid карцинома (ATC, ~25-50% of cases): дабрафеніб + траметиніб has пухлина-agnostic FDA схвалення for BRAF V600E нерезектабельний/метастатичний хвороба and is переважний 1L for V600E-mutant ATC per SRC-NCCN-THYROID-2025. The pivotal ROAR basket дослідження (Subbiah JCO 2018 — ATC cohort ORR 69%, міс. ~14 міс., dramatic відповідь in a historically rapid-fatal хвороба — historical mOS ~5 міс.) drove the 2018 FDA accelerated схвалення (full conversion 2022 with pan-рак broadening). Consider неоад'ювантний дабрафеніб+траметиніб to enable surgery in initially нерезектабельний V600E ATC per SRC-NCCN-THYROID-2025.
```

**EN excerpt:**
```
'BRAF V600E in anaplastic thyroid carcinoma (ATC, ~25-50% of cases):
```

**UA excerpt:**
```
'BRAF V600E in anaplastic thyroid карцинома (ATC, ~25-50% of
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 50/200: f-0051 - CRITICAL

**Entity:** `BMA-BRAF-V600K-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_braf_v600k_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRAF V600K (~10-20% of BRAF-mutant melanomas) shares all BRAF/MEKi`

**Current value:**
```
BRAF V600K (~10-20% of BRAF-mutant melanomas) shares all BRAF/MEKi approvals with V600E. Slightly lower ORR in pooled analyses (COMBI-d/v subgroup) but PFS/OS виграш preserved. Companion-діагностичний kits (cobas, THxID) detect both V600E and V600K.
```

**EN excerpt:**
```
'BRAF V600K (~10-20% of BRAF-mutant melanomas) shares all BRAF/MEKi
```

**UA excerpt:**
```
'BRAF V600K (~10-20% of BRAF-mutant melanomas) shares all BRAF/MEKi
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 51/200: f-0052 - CRITICAL

**Entity:** `BMA-BRCA1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in HER2-negative; breast (HR+ or TNBC; OlympiAD, Robson 2017) and; EMBRACA, Litton 2018) improve PFS vs physician-choice; HER2-negative: 1y; iDFS and OS (OlympiA, Tutt 2021). ESCAT IA / OncoKB
`

**Current value:**
```
BRCA1 герміногенний патогенний in HER2-negative метастатичний breast (HR+ or TNBC): олапариб (OlympiAD, Robson 2017) and талазопариб (EMBRACA, Litton 2018) improve PFS vs physician-choice хіміотерапія. In ранньої стадії високого ризику HER2-negative: 1y ад'ювантний олапариб покращує iDFS and OS (OlympiA, Tutt 2021). ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA1 germline pathogenic in HER2-negative metastatic breast (HR+ or TNBC): olaparib (OlympiAD, Robson 2017) and talazoparib (EMBRACA, Litton 2018) improve PFS vs physician-choice c...

```

**UA excerpt:**
```
BRCA1 герміногенний патогенний in HER2-negative метастатичний breast (HR+ or TNBC): олапариб (OlympiAD, Robson 2017) and талазопариб (EMBRACA, Litton 2018) improve PFS vs physician-choice хіміотерапія. In ранньої стадії в...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 52/200: f-0053 - CRITICAL

**Entity:** `BMA-BRCA1-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `incl. fallopian-tube and primary peritoneal; in 1L (SOLO1, Moore 2018) yields; NOVA, Mirza 2016) and; ARIEL3) extend PFS in platinum-sensitive; ESCAT IA / OncoKB
`

**Current value:**
```
BRCA1 герміногенний патогенний варіанти in поширений epithelial ovarian карцинома (incl. fallopian-tube and primary peritoneal): олапариб підтримка after platinum-відповідь in 1L (SOLO1, Moore 2018) yields ~70% зниження in прогресування risk; нірапариб (NOVA, Mirza 2016) and рукапариб (ARIEL3) extend PFS in platinum-sensitive рецидив. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA1 germline pathogenic variants in advanced epithelial ovarian carcinoma (incl. fallopian-tube and primary peritoneal): olaparib maintenance after platinum-response in 1L (SOLO1,...

```

**UA excerpt:**
```
BRCA1 герміногенний патогенний варіанти in поширений epithelial ovarian карцинома (incl. fallopian-tube and primary peritoneal): олапариб підтримка after platinum-відповідь in 1L (SOLO1, Moore 2018) yields ~70% зниження i...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 53/200: f-0054 - CRITICAL

**Entity:** `BMA-BRCA1-GERMLINE-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_germline_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `PDAC after ≥16 weeks of platinum without; PFS (POLO, Golan; but durable PFS responders observed. ESCAT IA / OncoKB
`

**Current value:**
```
BRCA1 герміногенний патогенний in метастатичний PDAC after ≥16 weeks of platinum without прогресування: олапариб підтримка покращує PFS (POLO, Golan 2019). ні OS виграш продемонстровано but durable PFS responders observed. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA1 germline pathogenic in metastatic PDAC after ≥16 weeks of platinum without progression: olaparib maintenance improves PFS (POLO, Golan 2019). No OS benefit demonstrated but du...

```

**UA excerpt:**
```
BRCA1 герміногенний патогенний in метастатичний PDAC after ≥16 weeks of platinum without прогресування: олапариб підтримка покращує PFS (POLO, Golan 2019). ні OS виграш продемонстровано but durable PFS responders observed...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 54/200: f-0055 - CRITICAL

**Entity:** `BMA-BRCA1-GERMLINE-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_germline_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `rPFS and OS post-NHA (PROfound Cohort A, de Bono; MAGNITUDE BRCA subset) also; MAGNITUDE) extend rPFS in HRR-positive mCRPC. ESCAT IA / OncoKB
`

**Current value:**
```
BRCA1 герміногенний патогенний in mCRPC: олапариб покращує rPFS and OS post-NHA (PROfound Cohort A, de Bono 2020); рукапариб (TRITON2/3) and нірапариб (MAGNITUDE BRCA subset) also схвалений. 1L олапариб + абіратерон (PROpel) and нірапариб + абіратерон (MAGNITUDE) extend rPFS in HRR-positive mCRPC. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA1 germline pathogenic in mCRPC: olaparib improves rPFS and OS post-NHA (PROfound Cohort A, de Bono 2020); rucaparib (TRITON2/3) and niraparib (MAGNITUDE BRCA subset) also approv...

```

**UA excerpt:**
```
BRCA1 герміногенний патогенний in mCRPC: олапариб покращує rPFS and OS post-NHA (PROfound Cohort A, de Bono 2020); рукапариб (TRITON2/3) and нірапариб (MAGNITUDE BRCA subset) also схвалений. 1L олапариб + абіратерон (PROp...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 55/200: f-0056 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in HER2-negative; breast: TBCRC-048 (Tung 2020) showed; activity in sBRCA tumors (ORR ~31%). PARPi labels in breast are formally; tumors treated off-label or via NCCN extrapolation. ESCAT IB / OncoKB
`

**Current value:**
```
соматичний BRCA1 втрата функції in HER2-negative метастатичний breast: TBCRC-048 (Tung 2020) showed талазопариб activity in sBRCA tumors (ORR ~31%). PARPi labels in breast are formally герміногенний-only (gBRCAm); соматичний tumors treated off-label or via NCCN extrapolation. ESCAT IB / OncoKB рівень 2.
```

**EN excerpt:**
```
Somatic BRCA1 loss-of-function in HER2-negative metastatic breast: TBCRC-048 (Tung 2020) showed talazoparib activity in sBRCA tumors (ORR ~31%). PARPi labels in breast are formally...

```

**UA excerpt:**
```
соматичний BRCA1 втрата функції in HER2-negative метастатичний breast: TBCRC-048 (Tung 2020) showed талазопариб activity in sBRCA tumors (ORR ~31%). PARPi labels in breast are formally герміногенний-only (gBRCAm); соматич...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 56/200: f-0057 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EOC confer PARPi; SOLO1 included sBRCA in EU label) and; L+ are FDA; EMA regardless of; status. ESCAT IA / OncoKB
`

**Current value:**
```
соматичний BRCA1 втрата функції варіанти in поширений EOC confer PARPi чутливість еквівалентний to герміногенний; олапариб 1L підтримка (SOLO1 included sBRCA in EU label) and рукапариб 3L+ are FDA/схвалений EMA regardless of герміногенний status. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic BRCA1 loss-of-function variants in advanced EOC confer PARPi sensitivity equivalent to germline; olaparib 1L maintenance (SOLO1 included sBRCA in EU label) and rucaparib 3L+...

```

**UA excerpt:**
```
соматичний BRCA1 втрата функції варіанти in поширений EOC confer PARPi чутливість еквівалентний to герміногенний; олапариб 1L підтримка (SOLO1 included sBRCA in EU label) and рукапариб 3L+ are FDA/схвалений EMA regardless...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 57/200: f-0058 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `limited but smaller series suggest; NCCN allows PARPi consideration off-label in sBRCA PDAC. ESCAT IIA / OncoKB
`

**Current value:**
```
соматичний BRCA1 втрата функції in метастатичний PDAC: POLO дослідження restricted to герміногенний; соматичний дані limited but smaller series suggest подібний PARPi чутливість. NCCN allows PARPi consideration off-label in sBRCA PDAC. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
Somatic BRCA1 loss-of-function in metastatic PDAC: POLO trial restricted to germline; somatic data limited but smaller series suggest similar PARPi sensitivity. NCCN allows PARPi co...

```

**UA excerpt:**
```
соматичний BRCA1 втрата функції in метастатичний PDAC: POLO дослідження restricted to герміногенний; соматичний дані limited but smaller series suggest подібний PARPi чутливість. NCCN allows PARPi consideration off-label...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 58/200: f-0059 - CRITICAL

**Entity:** `BMA-BRCA1-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca1_somatic_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mCRPC: PROfound enrolled both; PARPi labels in prostate cover both gBRCA and sBRCA. ESCAT IA / OncoKB
`

**Current value:**
```
соматичний BRCA1 втрата функції in mCRPC: PROfound enrolled both герміногенний and соматичний; олапариб виграш еквівалентний. PARPi labels in prostate cover both gBRCA and sBRCA. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic BRCA1 loss-of-function in mCRPC: PROfound enrolled both germline and somatic; olaparib benefit equivalent. PARPi labels in prostate cover both gBRCA and sBRCA. ESCAT IA / On...

```

**UA excerpt:**
```
соматичний BRCA1 втрата функції in mCRPC: PROfound enrolled both герміногенний and соматичний; олапариб виграш еквівалентний. PARPi labels in prostate cover both gBRCA and sBRCA. ESCAT IA / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 59/200: f-0060 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in HER2-negative; EMBRACA) improve PFS; in; HER2-negative, 1y; iDFS and OS (OlympiA). ESCAT IA / OncoKB`

**Current value:**
```
BRCA2 герміногенний патогенний in HER2-negative метастатичний breast: олапариб (OlympiAD) and талазопариб (EMBRACA) improve PFS; in ранньої стадії високого ризику HER2-negative, 1y ад'ювантний олапариб покращує iDFS and OS (OlympiA). ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA2 germline pathogenic in HER2-negative metastatic breast: olaparib (OlympiAD) and talazoparib (EMBRACA) improve PFS; in early-stage high-risk HER2-negative, 1y adjuvant olaparib...

```

**UA excerpt:**
```
BRCA2 герміногенний патогенний in HER2-negative метастатичний breast: олапариб (OlympiAD) and талазопариб (EMBRACA) improve PFS; in ранньої стадії високого ризику HER2-negative, 1y ад'ювантний олапариб покращує iDFS and O...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 60/200: f-0061 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `confers ~2-3× elevated cutaneous; risk and uveal-; BRAF/MEKi or ICI) per usual algorithm. PARPi only in clinical-; context. ESCAT IIIA / OncoKB
`

**Current value:**
```
BRCA2 герміногенний патогенний confers ~2-3× elevated cutaneous меланома risk and uveal-меланома association; ні меланома-specific PARPi показання exists. стандарт меланома терапія (BRAF/MEKi or ICI) per usual algorithm. PARPi only in clinical-дослідження context. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
BRCA2 germline pathogenic confers ~2-3× elevated cutaneous melanoma risk and uveal-melanoma association; no melanoma-specific PARPi indication exists. Standard melanoma therapy (BRA...

```

**UA excerpt:**
```
BRCA2 герміногенний патогенний confers ~2-3× elevated cutaneous меланома risk and uveal-меланома association; ні меланома-specific PARPi показання exists. стандарт меланома терапія (BRAF/MEKi or ICI) per usual algorithm....

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 61/200: f-0062 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `not reached vs 13.8 mo placebo at 5y; ESCAT IA / OncoKB`

**Current value:**
```
BRCA2 герміногенний патогенний in поширений EOC: олапариб 1L підтримка (SOLO1) → медіана ВБП not reached vs 13.8 mo placebo at 5y. нірапариб (NOVA), рукапариб (ARIEL3) схвалений in platinum-sensitive рецидив. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA2 germline pathogenic in advanced EOC: olaparib 1L maintenance (SOLO1) → median PFS not reached vs 13.8 mo placebo at 5y. Niraparib (NOVA), rucaparib (ARIEL3) approved in platin...

```

**UA excerpt:**
```
BRCA2 герміногенний патогенний in поширений EOC: олапариб 1L підтримка (SOLO1) → медіана ВБП not reached vs 13.8 mo placebo at 5y. нірапариб (NOVA), рукапариб (ARIEL3) схвалений in platinum-sensitive рецидив. ESCAT IA / O...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 62/200: f-0063 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `after ≥16 weeks platinum without; mo. ESCAT IA / OncoKB`

**Current value:**
```
BRCA2 герміногенний патогенний in метастатичний PDAC: олапариб підтримка after ≥16 weeks platinum without прогресування (POLO) → mPFS 7.4 проти 3.8 mo. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA2 germline pathogenic in metastatic PDAC: olaparib maintenance after ≥16 weeks platinum without progression (POLO) → mPFS 7.4 vs 3.8 mo. ESCAT IA / OncoKB Level 1.

```

**UA excerpt:**
```
BRCA2 герміногенний патогенний in метастатичний PDAC: олапариб підтримка after ≥16 weeks platinum without прогресування (POLO) → mPFS 7.4 проти 3.8 mo. ESCAT IA / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 63/200: f-0064 - CRITICAL

**Entity:** `BMA-BRCA2-GERMLINE-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_germline_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mCRPC: largest PARPi; in HRR pathway (PROfound Cohort A; ESCAT IA / OncoKB
`

**Current value:**
```
BRCA2 герміногенний патогенний in mCRPC: largest PARPi виграш in HRR pathway (PROfound Cohort A); олапариб post-NHA, 1L олапариб+абіратерон (PROpel), нірапариб+абіратерон (MAGNITUDE), талазопариб+ензалутамід (TALAPRO-2) all схвалений. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
BRCA2 germline pathogenic in mCRPC: largest PARPi benefit in HRR pathway (PROfound Cohort A); olaparib post-NHA, 1L olaparib+abiraterone (PROpel), niraparib+abiraterone (MAGNITUDE),...

```

**UA excerpt:**
```
BRCA2 герміногенний патогенний in mCRPC: largest PARPi виграш in HRR pathway (PROfound Cohort A); олапариб post-NHA, 1L олапариб+абіратерон (PROpel), нірапариб+абіратерон (MAGNITUDE), талазопариб+ензалутамід (TALAPRO-2) a...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 64/200: f-0065 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in HER2-neg; activity (ORR ~31%); PARPi labels in breast remain; only. ESCAT IB / OncoKB`

**Current value:**
```
соматичний BRCA2 втрата функції in HER2-neg метастатичний breast: TBCRC-048 продемонстровано талазопариб activity (ORR ~31%); PARPi labels in breast remain герміногенний-only. ESCAT IB / OncoKB рівень 2.
```

**EN excerpt:**
```
Somatic BRCA2 loss-of-function in HER2-neg metastatic breast: TBCRC-048 demonstrated talazoparib activity (ORR ~31%); PARPi labels in breast remain germline-only. ESCAT IB / OncoKB...

```

**UA excerpt:**
```
соматичний BRCA2 втрата функції in HER2-neg метастатичний breast: TBCRC-048 продемонстровано талазопариб activity (ORR ~31%); PARPi labels in breast remain герміногенний-only. ESCAT IB / OncoKB рівень 2.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 65/200: f-0066 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `biological rationale only. Treat per; algorithm. ESCAT IV / OncoKB`

**Current value:**
```
соматичний BRCA2 втрата функції in меланома: ні PARPi показання; biological rationale only. Treat per стандарт меланома algorithm. ESCAT IV / OncoKB рівень 4.
```

**EN excerpt:**
```
Somatic BRCA2 loss-of-function in melanoma: no PARPi indication; biological rationale only. Treat per standard melanoma algorithm. ESCAT IV / OncoKB Level 4.

```

**UA excerpt:**
```
соматичний BRCA2 втрата функції in меланома: ні PARPi показання; biological rationale only. Treat per стандарт меланома algorithm. ESCAT IV / OncoKB рівень 4.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 66/200: f-0067 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `status; SOLO1 EU label and; FDA label include sBRCA. ESCAT IA / OncoKB`

**Current value:**
```
соматичний BRCA2 втрата функції in поширений EOC: PARPi (олапариб, нірапариб, рукапариб) схвалений regardless of герміногенний status; SOLO1 EU label and рукапариб FDA label include sBRCA. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic BRCA2 loss-of-function in advanced EOC: PARPi (olaparib, niraparib, rucaparib) approved regardless of germline status; SOLO1 EU label and rucaparib FDA label include sBRCA....

```

**UA excerpt:**
```
соматичний BRCA2 втрата функції in поширений EOC: PARPi (олапариб, нірапариб, рукапариб) схвалений regardless of герміногенний status; SOLO1 EU label and рукапариб FDA label include sBRCA. ESCAT IA / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 67/200: f-0068 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `less robust. NCCN allows off-label PARPi consideration. ESCAT IIA / OncoKB`

**Current value:**
```
соматичний BRCA2 втрата функції in метастатичний PDAC: POLO герміногенний-only; соматичний series suggest подібний PARPi чутливість but докази less robust. NCCN allows off-label PARPi consideration. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
Somatic BRCA2 loss-of-function in metastatic PDAC: POLO germline-only; somatic series suggest similar PARPi sensitivity but evidence less robust. NCCN allows off-label PARPi conside...

```

**UA excerpt:**
```
соматичний BRCA2 втрата функції in метастатичний PDAC: POLO герміногенний-only; соматичний series suggest подібний PARPi чутливість but докази less robust. NCCN allows off-label PARPi consideration. ESCAT IIA / OncoKB рів...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 68/200: f-0069 - CRITICAL

**Entity:** `BMA-BRCA2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brca2_somatic_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mCRPC: PROfound included sBRCA; ESCAT IA / OncoKB
`

**Current value:**
```
соматичний BRCA2 втрата функції in mCRPC: PROfound included sBRCA; олапариб виграш еквівалентний to герміногенний. Labels cover герміногенний OR соматичний. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic BRCA2 loss-of-function in mCRPC: PROfound included sBRCA; olaparib benefit equivalent to germline. Labels cover germline OR somatic. ESCAT IA / OncoKB Level 1.

```

**UA excerpt:**
```
соматичний BRCA2 втрата функції in mCRPC: PROfound included sBRCA; олапариб виграш еквівалентний to герміногенний. Labels cover герміногенний OR соматичний. ESCAT IA / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 69/200: f-0070 - CRITICAL

**Entity:** `BMA-BRIP1-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `weak/uncertain risk association (NCCN does not currently recommend enhanced breast; based on BRIP1 alone; ESCAT IIIA / OncoKB
`

**Current value:**
```
BRIP1 герміногенний патогенний and рак молочної залози: weak/uncertain risk association (NCCN does not currently recommend enhanced breast спостереження based on BRIP1 alone). ні PARPi показання. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
BRIP1 germline pathogenic and breast cancer: weak/uncertain risk association (NCCN does not currently recommend enhanced breast surveillance based on BRIP1 alone). No PARPi indicati...

```

**UA excerpt:**
```
BRIP1 герміногенний патогенний and рак молочної залози: weak/uncertain risk association (NCCN does not currently recommend enhanced breast спостереження based on BRIP1 alone). ні PARPi показання. ESCAT IIIA / OncoKB рівен...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 70/200: f-0071 - CRITICAL

**Entity:** `BMA-BRIP1-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `moderate-risk gene (~RR 3-5); included in HRR panels and HRD-positive PARPi; BRIP1 in PARPi-eligible HRR list. ESCAT IIA / OncoKB
`

**Current value:**
```
BRIP1 (FANCJ) герміногенний патогенний in EOC: усталений moderate-risk gene (~RR 3-5); included in HRR panels and HRD-positive PARPi дослідження subgroups. NCCN включає BRIP1 in PARPi-eligible HRR list. ESCAT IIA / OncoKB рівень 3A.
```

**EN excerpt:**
```
BRIP1 (FANCJ) germline pathogenic in EOC: established moderate-risk gene (~RR 3-5); included in HRR panels and HRD-positive PARPi trial subgroups. NCCN includes BRIP1 in PARPi-eligi...

```

**UA excerpt:**
```
BRIP1 (FANCJ) герміногенний патогенний in EOC: усталений moderate-risk gene (~RR 3-5); included in HRR panels and HRD-positive PARPi дослідження subgroups. NCCN включає BRIP1 in PARPi-eligible HRR list. ESCAT IIA / OncoKB...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 71/200: f-0072 - CRITICAL

**Entity:** `BMA-BRIP1-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRIP1 in breast; ESCAT IV / OncoKB`

**Current value:**
```
соматичний BRIP1 in breast: рідкісний; ні actionable показання. ESCAT IV / OncoKB рівень 4.
```

**EN excerpt:**
```
Somatic BRIP1 in breast: rare; no actionable indication. ESCAT IV / OncoKB Level 4.

```

**UA excerpt:**
```
соматичний BRIP1 in breast: рідкісний; ні actionable показання. ESCAT IV / OncoKB рівень 4.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 72/200: f-0073 - CRITICAL

**Entity:** `BMA-BRIP1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_brip1_somatic_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BRIP1 in EOC: HRR panel inclusion; PARPi consideration in HRD-positive context. ESCAT IIB / OncoKB
`

**Current value:**
```
соматичний BRIP1 in EOC: HRR panel inclusion; PARPi consideration in HRD-positive context. ESCAT IIB / OncoKB рівень 3B.
```

**EN excerpt:**
```
Somatic BRIP1 in EOC: HRR panel inclusion; PARPi consideration in HRD-positive context. ESCAT IIB / OncoKB Level 3B.

```

**UA excerpt:**
```
соматичний BRIP1 in EOC: HRR panel inclusion; PARPi consideration in HRD-positive context. ESCAT IIB / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 73/200: f-0074 - CRITICAL

**Entity:** `BMA-CALR-ET`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_calr_et.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CALR exon 9 indels are the second; driver in ET (~25-30%) and a WHO 2022 / ICC 2022 major; criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR- mutated ET has lower thrombosis risk than JAK2-mutated ET, which feeds into IPSET-thrombosis stratification: very-; CALR patients may be managed with observation alone; otherwise risk- stratified management identical to JAK2-positive ET; IFN per SRC-PT1-HARRISON-
`

**Current value:**
```
CALR exon 9 indels are the second найбільш поширений driver in ET (~25-30%) and a WHO 2022 / ICC 2022 major діагностичний criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR- mutated ET has lower thrombosis risk than JAK2-mutated ET, which feeds into IPSET-thrombosis stratification: very-низького ризику CALR patients may be managed with observation alone; otherwise risk- stratified management identical to JAK2-positive ET (низького ризику → aspirin; високого ризику → гідроксикарбамід/IFN per SRC-PT1-HARRISON-2005).
```

**EN excerpt:**
```
CALR exon 9 indels are the second most common driver in ET (~25-30%) and a WHO 2022 / ICC 2022 major diagnostic criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESM...

```

**UA excerpt:**
```
CALR exon 9 indels are the second найбільш поширений driver in ET (~25-30%) and a WHO 2022 / ICC 2022 major діагностичний criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR- mutated ET...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 74/200: f-0075 - CRITICAL

**Entity:** `BMA-CALR-PMF`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_calr_pmf.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CALR exon 9 indels are the second; driver in PMF (~25%) and a WHO 2022 / ICC 2022 major; criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR type-; in PMF is associated with; OS and lower leukemic; risk than JAK2 V617F or triple-negative PMF, integrated into MIPSS70+v2 risk model; by symptom / risk score; for symptomatic intermediate-
`

**Current value:**
```
CALR exon 9 indels are the second найбільш поширений driver in PMF (~25%) and a WHO 2022 / ICC 2022 major діагностичний criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR type-1 мутація in PMF is associated with краще OS and lower leukemic трансформація risk than JAK2 V617F or triple-negative PMF, integrated into MIPSS70+v2 risk model. лікування is генотип- agnostic JAK-інгібітор терапія by symptom / risk score: руксолитиніб for symptomatic intermediate-2/високого ризику (COMFORT-I extends to all driver genotypes); федратиніб for руксолитиніб failure (JAKARTA2); момелотиніб for anemic patients (MOMENTUM); алогенний HCT for придатний до трансплантації higher-risk patients per SRC-NCCN-MPN-2025.
```

**EN excerpt:**
```
CALR exon 9 indels are the second most common driver in PMF (~25%) and a WHO 2022 / ICC 2022 major diagnostic criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-...

```

**UA excerpt:**
```
CALR exon 9 indels are the second найбільш поширений driver in PMF (~25%) and a WHO 2022 / ICC 2022 major діагностичний criterion in JAK2/MPL- negative cases (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). CALR type-1 мутація...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 75/200: f-0076 - CRITICAL

**Entity:** `BMA-CCND1-IHC-MCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ccnd1_ihc_mcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `Cyclin D1 IHC is a defining; marker of MCL (positive in >95%; SOX11 used in cyclin D1-negative; but does not 'select'; independently of t
`

**Current value:**
```
Cyclin D1 IHC is a defining діагностичний marker of MCL (positive in >95%; SOX11 used in cyclin D1-negative варіант). Drives DIS-MCL діагноз but does not 'select' терапія independently of t(11;14).
```

**EN excerpt:**
```
Cyclin D1 IHC is a defining diagnostic marker of MCL (positive in >95%; SOX11 used in cyclin D1-negative variant). Drives DIS-MCL diagnosis but does not 'select' therapy independent...

```

**UA excerpt:**
```
Cyclin D1 IHC is a defining діагностичний marker of MCL (positive in >95%; SOX11 used in cyclin D1-negative варіант). Drives DIS-MCL діагноз but does not 'select' терапія independently of t(11;14).

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 76/200: f-0077 - CRITICAL

**Entity:** `BMA-CCND1-IHC-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ccnd1_ihc_mm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CCND1 (cyclin D; in MM strongly correlates with t(11;14) and BCL2 dependence — predicts; Used as surrogate when FISH unavailable
`

**Current value:**
```
CCND1 (cyclin D1) гіперекспресія in MM strongly correlates with t(11;14) and BCL2 dependence — predicts венетоклакс відповідь. Used as surrogate when FISH unavailable.
```

**EN excerpt:**
```
CCND1 (cyclin D1) overexpression in MM strongly correlates with t(11;14) and BCL2 dependence — predicts venetoclax response. Used as surrogate when FISH unavailable.

```

**UA excerpt:**
```
CCND1 (cyclin D1) гіперекспресія in MM strongly correlates with t(11;14) and BCL2 dependence — predicts венетоклакс відповідь. Used as surrogate when FISH unavailable.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 77/200: f-0078 - CRITICAL

**Entity:** `BMA-CCND1-T1114-MCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ccnd1_t1114_mcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `t(11;14) IGH/CCND1 is the defining genetic lesion of MCL — drives cyclin D; TRIANGLE, Dreyling Lancet 2024; ECHO — Wang NEJM 2024) is the new 1L; regardless of fitness for TP53-mut; high-; historically (LyMa, MCL Younger; CCND1 → BCL2-mediated anti-apoptosis rationale) active
`

**Current value:**
```
t(11;14) IGH/CCND1 is the defining genetic lesion of MCL — drives cyclin D1 гіперекспресія. BTKi (акалабрутиніб + ритуксимаб — TRIANGLE, Dreyling Lancet 2024; ECHO — Wang NEJM 2024) is the new 1L стандарт regardless of fitness for TP53-mut; high-доза AraC + аутоТГСК historically (LyMa, MCL Younger). венетоклакс (CCND1 → BCL2-mediated anti-apoptosis rationale) active р/р.
```

**EN excerpt:**
```
t(11;14) IGH/CCND1 is the defining genetic lesion of MCL — drives cyclin D1 overexpression. BTKi (acalabrutinib + rituximab — TRIANGLE, Dreyling Lancet 2024; ECHO — Wang NEJM 2024)...

```

**UA excerpt:**
```
t(11;14) IGH/CCND1 is the defining genetic lesion of MCL — drives cyclin D1 гіперекспресія. BTKi (акалабрутиніб + ритуксимаб — TRIANGLE, Dreyling Lancet 2024; ECHO — Wang NEJM 2024) is the new 1L стандарт regardless of fi...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 78/200: f-0079 - CRITICAL

**Entity:** `BMA-CCND1-T1114-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ccnd1_t1114_mm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `distinct biology with high BCL2/MCL1 ratio; M14-032; Kumar Blood 2017 ORR ~40%) and; dexamethasone (BELLINI subgroup; Kumar Lancet Oncol 2020) active. BELLINI raised mortality signal in non-t(11;14) arm; is now t(11;14)-selected in MM. CANOVA Ph; dex in t; MM) read out
`

**Current value:**
```
t(11;14) мієлома (~15-20%) — distinct biology with high BCL2/MCL1 ratio. венетоклакс монотерапія (M14-032; Kumar Blood 2017 ORR ~40%) and венетоклакс + dexamethasone (BELLINI subgroup; Kumar Lancet Oncol 2020) active. BELLINI raised mortality signal in non-t(11;14) arm — венетоклакс is now t(11;14)-selected in MM. CANOVA Ph3 (венетоклакс + dex vs помалідомід + dex in t(11;14) р/р MM) read out 2024.
```

**EN excerpt:**
```
t(11;14) myeloma (~15-20%) — distinct biology with high BCL2/MCL1 ratio. Venetoclax monotherapy (M14-032; Kumar Blood 2017 ORR ~40%) and venetoclax + dexamethasone (BELLINI subgroup...

```

**UA excerpt:**
```
t(11;14) мієлома (~15-20%) — distinct biology with high BCL2/MCL1 ratio. венетоклакс монотерапія (M14-032; Kumar Blood 2017 ORR ~40%) and венетоклакс + dexamethasone (BELLINI subgroup; Kumar Lancet Oncol 2020) active. BEL...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 79/200: f-0080 - CRITICAL

**Entity:** `BMA-CD30-ALCL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_cd30_alcl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `BV) targets CD30 with an auristatin payload. 1L sALCL: BV + CHP; over CHOP per ECHELON-2 (Horwitz Lancet 2019 — mPFS; HR 0.71; OS HR 0.66) per SRC-NCCN-BCELL-2025, SRC-ESMO-PTCL-; was the basis of FDA accelerated; Pro JCO 2012 — ORR 86%, CR 57%) and is; ALCL: AHOD1331 supports BV + AVEPC
`

**Current value:**
```
CD30 експресія is a визначальна ознака anaplastic large-cell лімфома (sALCL); брентуксимаб ведотин (BV) targets CD30 with an auristatin payload. 1L sALCL: BV + CHP (циклофосфамід / доксорубіцин / prednisone, replacing вінкристин) is переважний over CHOP per ECHELON-2 (Horwitz Lancet 2019 — mPFS 48 проти 21 міс., HR 0.71; OS HR 0.66) per SRC-NCCN-BCELL-2025, SRC-ESMO-PTCL-2024. р/р sALCL: BV монотерапія was the basis of FDA accelerated схвалення (Pro JCO 2012 — ORR 86%, CR 57%) and is переважний сальвадж. педіатричний ALCL: AHOD1331 supports BV + AVEPC.
```

**EN excerpt:**
```
CD30 expression is a defining feature of anaplastic large-cell lymphoma (sALCL); brentuximab vedotin (BV) targets CD30 with an auristatin payload. 1L sALCL: BV + CHP (cyclophosphami...

```

**UA excerpt:**
```
CD30 експресія is a визначальна ознака anaplastic large-cell лімфома (sALCL); брентуксимаб ведотин (BV) targets CD30 with an auristatin payload. 1L sALCL: BV + CHP (циклофосфамід / доксорубіцин / prednisone, replacing він...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 80/200: f-0081 - CRITICAL

**Entity:** `BMA-CD30-CHL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_cd30_chl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CD30 is universally expressed on Reed-Sternberg cells in classical; and is the target of; BV), an anti-CD; auristatin payload). 1L; stage cHL: A+AVD (BV; over ABVD per ECHELON-1 (Ansell NEJM 2022 — 6y OS; HR 0.59) per SRC-NCCN-BCELL-2025, SRC-ESMO-HODGKIN-; AHOD1331 supported BV + AVE-PC for
`

**Current value:**
```
CD30 is universally expressed on Reed-Sternberg cells in classical лімфома Ходжкіна and is the target of брентуксимаб ведотин (BV), an anti-CD30 кон'югат антитіло-препарат (auristatin payload). 1L поширений- stage cHL: A+AVD (BV + доксорубіцин/вінбластин/dacarbazine) is переважний over ABVD per ECHELON-1 (Ansell NEJM 2022 — 6y OS 93.9% проти 89.4%, HR 0.59) per SRC-NCCN-BCELL-2025, SRC-ESMO-HODGKIN-2024. педіатричний AHOD1331 supported BV + AVE-PC for високого ризику педіатричний. р/р cHL: BV монотерапія and BV + ніволумаб are стандарт pre-/post- HCT options. BV консолідація post-autoHCT for високого ризику р/р cHL (AETHERA Younes Lancet 2015 — покращує PFS) per SRC-NCCN-BCELL-2025.
```

**EN excerpt:**
```
CD30 is universally expressed on Reed-Sternberg cells in classical Hodgkin lymphoma and is the target of brentuximab vedotin (BV), an anti-CD30 antibody-drug conjugate (auristatin p...

```

**UA excerpt:**
```
CD30 is universally expressed on Reed-Sternberg cells in classical лімфома Ходжкіна and is the target of брентуксимаб ведотин (BV), an anti-CD30 кон'югат антитіло-препарат (auristatin payload). 1L поширений- stage cHL: A+...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 81/200: f-0082 - CRITICAL

**Entity:** `BMA-CHEK1-SOMATIC-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek1_somatic_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `included in some HRR panel definitions but; weaker than core HRR genes. NCCN HRR panel inclusion is variable. ESCAT IIIA / OncoKB
`

**Current value:**
```
соматичний CHEK1 втрата функції in EOC: рідкісний (<1%); included in some HRR panel definitions but докази for PARPi виграш weaker than core HRR genes. NCCN HRR panel inclusion is variable. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
Somatic CHEK1 loss-of-function in EOC: rare (<1%); included in some HRR panel definitions but evidence for PARPi benefit weaker than core HRR genes. NCCN HRR panel inclusion is vari...

```

**UA excerpt:**
```
соматичний CHEK1 втрата функції in EOC: рідкісний (<1%); included in some HRR panel definitions but докази for PARPi виграш weaker than core HRR genes. NCCN HRR panel inclusion is variable. ESCAT IIIA / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 82/200: f-0083 - CRITICAL

**Entity:** `BMA-CHEK1-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek1_somatic_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `PROfound included CHEK1 in Cohort B but small sample; CHEK1 in HRR list. ESCAT IIIA / OncoKB`

**Current value:**
```
соматичний CHEK1 втрата функції in mCRPC: рідкісний; PROfound included CHEK1 in Cohort B but small sample. олапариб FDA label включає CHEK1 in HRR list. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
Somatic CHEK1 loss-of-function in mCRPC: rare; PROfound included CHEK1 in Cohort B but small sample. Olaparib FDA label includes CHEK1 in HRR list. ESCAT IIIA / OncoKB Level 3B.

```

**UA excerpt:**
```
соматичний CHEK1 втрата функції in mCRPC: рідкісний; PROfound included CHEK1 in Cohort B but small sample. олапариб FDA label включає CHEK1 in HRR list. ESCAT IIIA / OncoKB рівень 3B.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 83/200: f-0084 - CRITICAL

**Entity:** `BMA-CHEK2-GERMLINE-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_germline_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `e.g. 1100delC) confers ~2× breast-; TBCRC-048 CHEK2 cohort minimal; HR/HER2-directed; ESCAT IIA (predisposition) / OncoKB
`

**Current value:**
```
CHEK2 герміногенний патогенний (e.g. 1100delC) confers ~2× breast-рак risk; ні PARPi activity продемонстровано (TBCRC-048 CHEK2 cohort minimal відповідь). стандарт HR/HER2-directed терапія. ESCAT IIA (predisposition) / OncoKB рівень 3A.
```

**EN excerpt:**
```
CHEK2 germline pathogenic (e.g. 1100delC) confers ~2× breast-cancer risk; no PARPi activity demonstrated (TBCRC-048 CHEK2 cohort minimal response). Standard HR/HER2-directed therapy...

```

**UA excerpt:**
```
CHEK2 герміногенний патогенний (e.g. 1100delC) confers ~2× breast-рак risk; ні PARPi activity продемонстровано (TBCRC-048 CHEK2 cohort minimal відповідь). стандарт HR/HER2-directed терапія. ESCAT IIA (predisposition) / On...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 84/200: f-0085 - CRITICAL

**Entity:** `BMA-CHEK2-GERMLINE-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_germline_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mCRPC: included in PROfound Cohort B; FDA HRR label (post-NHA; CHEK2 (FDA), though EMA label restricts to BRCA1/2. ESCAT IB (FDA jurisdiction) / OncoKB
`

**Current value:**
```
CHEK2 герміногенний патогенний in mCRPC: included in PROfound Cohort B; олапариб FDA HRR label (post-NHA) включає CHEK2 (FDA), though EMA label restricts to BRCA1/2. ESCAT IB (FDA jurisdiction) / OncoKB рівень 1.
```

**EN excerpt:**
```
CHEK2 germline pathogenic in mCRPC: included in PROfound Cohort B; olaparib FDA HRR label (post-NHA) includes CHEK2 (FDA), though EMA label restricts to BRCA1/2. ESCAT IB (FDA juris...

```

**UA excerpt:**
```
CHEK2 герміногенний патогенний in mCRPC: included in PROfound Cohort B; олапариб FDA HRR label (post-NHA) включає CHEK2 (FDA), though EMA label restricts to BRCA1/2. ESCAT IB (FDA jurisdiction) / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 85/200: f-0086 - CRITICAL

**Entity:** `BMA-CHEK2-SOMATIC-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_somatic_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CHEK2 in breast: minimal PARPi activity; ESCAT IIIA / OncoKB
`

**Current value:**
```
соматичний CHEK2 in breast: minimal PARPi activity; стандарт підтип-directed терапія. ESCAT IIIA / OncoKB рівень 4.
```

**EN excerpt:**
```
Somatic CHEK2 in breast: minimal PARPi activity; standard subtype-directed therapy. ESCAT IIIA / OncoKB Level 4.

```

**UA excerpt:**
```
соматичний CHEK2 in breast: minimal PARPi activity; стандарт підтип-directed терапія. ESCAT IIIA / OncoKB рівень 4.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 86/200: f-0087 - CRITICAL

**Entity:** `BMA-CHEK2-SOMATIC-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_chek2_somatic_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `CHEK2 in mCRPC: PROfound enrolled both g/s; FDA; CHEK2. ESCAT IB / OncoKB
`

**Current value:**
```
соматичний CHEK2 in mCRPC: PROfound enrolled both g/s; FDA олапариб HRR label включає CHEK2. ESCAT IB / OncoKB рівень 1.
```

**EN excerpt:**
```
Somatic CHEK2 in mCRPC: PROfound enrolled both g/s; FDA olaparib HRR label includes CHEK2. ESCAT IB / OncoKB Level 1.

```

**UA excerpt:**
```
соматичний CHEK2 in mCRPC: PROfound enrolled both g/s; FDA олапариб HRR label включає CHEK2. ESCAT IB / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 87/200: f-0088 - CRITICAL

**Entity:** `BMA-CXCR4-WHIM-WM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_cxcr4_whim_wm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `co-occur in ~30-40% of MYD88-L265P Waldenström macroglobulinemia and confer relative; BTKi) — lower ORR and major-; slower kinetics of IgM; Treon NEJM 2015 — initial cohort; Castillo Blood 2020 — confirmation) per SRC-NCCN-BCELL-2025, SRC-ESMO-WM-2024. CXCR4 status drives 1L; selection in WM: in CXCR4-mutated patients; BR) or proteasome-; in CXCR4-WT patients, BTKi; has FDA orphan designation for WHIM but is
`

**Current value:**
```
CXCR4 WHIM-like мутації co-occur in ~30-40% of MYD88-L265P Waldenström macroglobulinemia and confer relative резистентність до ібрутиніб (BTKi) — lower ORR and major-частота відповіді, slower kinetics of IgM зниження (Treon NEJM 2015 — initial cohort; Castillo Blood 2020 — confirmation) per SRC-NCCN-BCELL-2025, SRC-ESMO-WM-2024. CXCR4 status drives 1L терапія selection in WM: in CXCR4-mutated patients, настанови list бендамустин + ритуксимаб (BR) or proteasome-інгібітор- based схеми (BDR — бортезоміб/dex/ритуксимаб) as переважний over BTKi монотерапія; in CXCR4-WT patients, BTKi монотерапія (ібрутиніб or занубрутиніб) is переважний. Mavorixafor (CXCR4 антагоніст) has FDA orphan designation for WHIM but is експериментальний in WM.
```

**EN excerpt:**
```
CXCR4 WHIM-like mutations co-occur in ~30-40% of MYD88-L265P Waldenström macroglobulinemia and confer relative resistance to ibrutinib (BTKi) — lower ORR and major-response rate, sl...

```

**UA excerpt:**
```
CXCR4 WHIM-like мутації co-occur in ~30-40% of MYD88-L265P Waldenström macroglobulinemia and confer relative резистентність до ібрутиніб (BTKi) — lower ORR and major-частота відповіді, slower kinetics of IgM зниження (Tre...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 88/200: f-0089 - CRITICAL

**Entity:** `BMA-EGFR-C797S-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_c797s_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR C797S is the principal; Cis-configuration with T790M renders all currently; rd-gen EGFR-TKIs ineffective; trans-configuration may respond to; th-gen EGFR-TKIs (BLU-945, BBT-176) and; chemo (MARIPOSA-2) are active options
`

**Current value:**
```
EGFR C797S is the principal набутий резистентна мутація to осимертиніб. Cis-configuration with T790M renders all currently схвалений 3rd-gen EGFR-TKIs ineffective; trans-configuration may respond to комбінація 1st-gen + осимертиніб. експериментальний 4th-gen EGFR-TKIs (BLU-945, BBT-176) and амівантамаб+chemo (MARIPOSA-2) are active options.
```

**EN excerpt:**
```
EGFR C797S is the principal acquired resistance mutation to osimertinib. Cis-configuration with T790M renders all currently approved 3rd-gen EGFR-TKIs ineffective; trans-configurati...

```

**UA excerpt:**
```
EGFR C797S is the principal набутий резистентна мутація to осимертиніб. Cis-configuration with T790M renders all currently схвалений 3rd-gen EGFR-TKIs ineffective; trans-configuration may respond to комбінація 1st-gen + о...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 89/200: f-0090 - CRITICAL

**Entity:** `BMA-EGFR-EX19DEL-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_ex19del_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR-TKIs (FLAURA, Soria et al. 2018; Ramalingam; DFS (ADAURA, Wu et al. 2020). Exon 19 del is one of two classical sensitizing; with L858R) and predicts the
`

**Current value:**
```
EGFR exon 19 делеція in поширений NSCLC: осимертиніб 1L покращує OS vs першого покоління EGFR-TKIs (FLAURA, Soria et al. 2018; Ramalingam 2020). ад'ювантний осимертиніб після резекції покращує DFS (ADAURA, Wu et al. 2020). Exon 19 del is one of two classical sensitizing мутації (with L858R) and predicts the найвища TKI відповідь rates.
```

**EN excerpt:**
```
EGFR exon 19 deletion in advanced NSCLC: osimertinib 1L improves OS vs first-generation EGFR-TKIs (FLAURA, Soria et al. 2018; Ramalingam 2020). Adjuvant osimertinib post-resection i...

```

**UA excerpt:**
```
EGFR exon 19 делеція in поширений NSCLC: осимертиніб 1L покращує OS vs першого покоління EGFR-TKIs (FLAURA, Soria et al. 2018; Ramalingam 2020). ад'ювантний осимертиніб після резекції покращує DFS (ADAURA, Wu et al. 2020)...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 90/200: f-0091 - CRITICAL

**Entity:** `BMA-EGFR-EX20INS-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_ex20ins_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR exon 20 insertions; A763_Y764insFQEA) are insensitive to classical EGFR-TKIs; chemo is 1L; PAPILLON, Zhou et al; was withdrawn globally 2023-2024 for failed confirmatory; option in 2L
`

**Current value:**
```
EGFR exon 20 insertions (виключаючи A763_Y764insFQEA) are insensitive to classical EGFR-TKIs. амівантамаб (EGFR-MET біспецифічний) + chemo is 1L стандарт (PAPILLON, Zhou et al. 2023). мобоцертиніб was withdrawn globally 2023-2024 for failed confirmatory дослідження. Sunvozertinib (China-схвалений) is an новий option in 2L.
```

**EN excerpt:**
```
EGFR exon 20 insertions (excluding A763_Y764insFQEA) are insensitive to classical EGFR-TKIs. Amivantamab (EGFR-MET bispecific) + chemo is 1L standard (PAPILLON, Zhou et al. 2023). M...

```

**UA excerpt:**
```
EGFR exon 20 insertions (виключаючи A763_Y764insFQEA) are insensitive to classical EGFR-TKIs. амівантамаб (EGFR-MET біспецифічний) + chemo is 1L стандарт (PAPILLON, Zhou et al. 2023). мобоцертиніб was withdrawn globally 2...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 91/200: f-0092 - CRITICAL

**Entity:** `BMA-EGFR-G719X-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_g719x_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR exon 18 G719X (G719A/C/S) is an "uncommon" sensitizing; of EGFR-mut NSCLC; LUX-Lung pooled analysis, Yang 2015) shows; activity in G719X; also active (UNICORN, Ahn; co-occurs with S768I or L861Q
`

**Current value:**
```
EGFR exon 18 G719X (G719A/C/S) is an "uncommon" sensitizing мутація (~3% of EGFR-mut NSCLC). афатиніб (LUX-Lung pooled analysis, Yang 2015) shows найвища activity in G719X; осимертиніб also active (UNICORN, Ahn 2022). часто co-occurs with S768I or L861Q.
```

**EN excerpt:**
```
EGFR exon 18 G719X (G719A/C/S) is an "uncommon" sensitizing mutation (~3% of EGFR-mut NSCLC). Afatinib (LUX-Lung pooled analysis, Yang 2015) shows highest activity in G719X; osimert...

```

**UA excerpt:**
```
EGFR exon 18 G719X (G719A/C/S) is an "uncommon" sensitizing мутація (~3% of EGFR-mut NSCLC). афатиніб (LUX-Lung pooled analysis, Yang 2015) shows найвища activity in G719X; осимертиніб also active (UNICORN, Ahn 2022). час...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 92/200: f-0093 - CRITICAL

**Entity:** `BMA-EGFR-L858R-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_l858r_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR L858R in; FLAURA); L858R historically shows somewhat lower TKI; than exon 19 del, prompting interest in; strategies (FLAURA2 chemo combo; MARIPOSA; indicated post resection (ADAURA
`

**Current value:**
```
EGFR L858R in поширений NSCLC: осимертиніб 1L is стандарт (FLAURA); L858R historically shows somewhat lower TKI відповідь than exon 19 del, prompting interest in комбінація strategies (FLAURA2 chemo combo; MARIPOSA амівантамаб+лазертиніб). ад'ювантний осимертиніб indicated post resection (ADAURA).
```

**EN excerpt:**
```
EGFR L858R in advanced NSCLC: osimertinib 1L is standard (FLAURA); L858R historically shows somewhat lower TKI response than exon 19 del, prompting interest in combination strategie...

```

**UA excerpt:**
```
EGFR L858R in поширений NSCLC: осимертиніб 1L is стандарт (FLAURA); L858R historically shows somewhat lower TKI відповідь than exon 19 del, prompting interest in комбінація strategies (FLAURA2 chemo combo; MARIPOSA аміван...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 93/200: f-0094 - CRITICAL

**Entity:** `BMA-EGFR-MUTATION-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_mutation_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `has shown OS; trials negative. Depatuxizumab-mafodotin (ADC) failed`

**Current value:**
```
EGFR ампліфікація (~40%) and EGFRvIII варіант (~25%) are поширений in гліобластома but ні таргетна терапія has shown OS виграш. ерлотиніб, гефітиніб, лапатиніб trials negative. Depatuxizumab-mafodotin (ADC) failed фаза 3 INTELLANCE-1. Currently ні actionable EGFR-таргетна терапія in GBM.
```

**EN excerpt:**
```
EGFR amplification (~40%) and EGFRvIII variant (~25%) are common in glioblastoma but no targeted therapy has shown OS benefit. Erlotinib, gefitinib, lapatinib trials negative. Depat...

```

**UA excerpt:**
```
EGFR ампліфікація (~40%) and EGFRvIII варіант (~25%) are поширений in гліобластома but ні таргетна терапія has shown OS виграш. ерлотиніб, гефітиніб, лапатиніб trials negative. Depatuxizumab-mafodotin (ADC) failed фаза 3...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 94/200: f-0095 - CRITICAL

**Entity:** `BMA-EGFR-T790M-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_egfr_t790m_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EGFR T790M is the dominant; resistance mechanism after 1st/2nd-gen EGFR-TKI; rd-gen) is active against T790M and is; L (AURA3, Mok et al. 2017). In the modern era T790M is; encountered de novo since; has moved to 1L; remains relevant after legacy 1L-TKI use
`

**Current value:**
```
EGFR T790M is the dominant набутий-resistance mechanism after 1st/2nd-gen EGFR-TKI (гефітиніб/ерлотиніб/афатиніб). осимертиніб (3rd-gen) is active against T790M and is стандарт 2L (AURA3, Mok et al. 2017). In the modern era T790M is рідко encountered de novo since осимертиніб has moved to 1L; remains relevant after legacy 1L-TKI use.
```

**EN excerpt:**
```
EGFR T790M is the dominant acquired-resistance mechanism after 1st/2nd-gen EGFR-TKI (gefitinib/erlotinib/afatinib). Osimertinib (3rd-gen) is active against T790M and is standard 2L...

```

**UA excerpt:**
```
EGFR T790M is the dominant набутий-resistance mechanism after 1st/2nd-gen EGFR-TKI (гефітиніб/ерлотиніб/афатиніб). осимертиніб (3rd-gen) is active against T790M and is стандарт 2L (AURA3, Mok et al. 2017). In the modern e...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 95/200: f-0096 - CRITICAL

**Entity:** `BMA-EPCAM-GERMLINE-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_epcam_germline_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `end) silences downstream MSH2 by promoter hypermethylation → Lynch syndrome with isolated MSH2/MSH6 protein loss on IHC. Treat as MSH; L mCRC dMMR (KEYNOTE-177); pan-; MSI-H ICI eligibility supersedes; specific lines. ESCAT IA / OncoKB
`

**Current value:**
```
EPCAM герміногенний делеція (3' end) silences downstream MSH2 by promoter hypermethylation → Lynch syndrome with isolated MSH2/MSH6 protein loss on IHC. Treat as MSH2-еквівалентний Lynch: пембролізумаб 1L mCRC dMMR (KEYNOTE-177); pan- пухлина MSI-H ICI eligibility supersedes пухлина-specific lines. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
EPCAM germline deletion (3' end) silences downstream MSH2 by promoter hypermethylation → Lynch syndrome with isolated MSH2/MSH6 protein loss on IHC. Treat as MSH2-equivalent Lynch:...

```

**UA excerpt:**
```
EPCAM герміногенний делеція (3' end) silences downstream MSH2 by promoter hypermethylation → Lynch syndrome with isolated MSH2/MSH6 protein loss on IHC. Treat as MSH2-еквівалентний Lynch: пембролізумаб 1L mCRC dMMR (KEYNO...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 96/200: f-0097 - CRITICAL

**Entity:** `BMA-EPCAM-GERMLINE-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_epcam_germline_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `silences MSH2 → Lynch syndrome with dMMR; Treat as MSH; dostarlimab + chemo 1L (RUBY); pan-; MSI-H ICI applies. ESCAT IA / OncoKB
`

**Current value:**
```
EPCAM герміногенний делеція silences MSH2 → Lynch syndrome with dMMR рак ендометрію фенотип. Treat as MSH2-еквівалентний: dostarlimab + chemo 1L (RUBY); pan-пухлина MSI-H ICI applies. ESCAT IA / OncoKB рівень 1.
```

**EN excerpt:**
```
EPCAM germline deletion silences MSH2 → Lynch syndrome with dMMR endometrial cancer phenotype. Treat as MSH2-equivalent: dostarlimab + chemo 1L (RUBY); pan-tumor MSI-H ICI applies....

```

**UA excerpt:**
```
EPCAM герміногенний делеція silences MSH2 → Lynch syndrome with dMMR рак ендометрію фенотип. Treat as MSH2-еквівалентний: dostarlimab + chemo 1L (RUBY); pan-пухлина MSI-H ICI applies. ESCAT IA / OncoKB рівень 1.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 97/200: f-0098 - CRITICAL

**Entity:** `BMA-EZH2-Y641-FL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ezh2_y641_fl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `EZH2 Y641 hotspot activating; occur in ~20-25% of; in DLBCL/HGBL). Tazemetostat is a; FL: in EZH2- mutated FL after ≥2 prior lines, ORR 69%, mPFS; E7438-202 Morschhauser Lancet Oncol 2020); in EZH2-WT FL, ORR 35%, mPFS; mutated population had stronger responses, leading to a companion-; per SRC-NCCN-BCELL-2025, SRC-ESMO-FL-
`

**Current value:**
```
EZH2 Y641 hotspot activating мутації occur in ~20-25% of фолікулярна лімфома (and рідко in DLBCL/HGBL). Tazemetostat is a селективний EZH2 інгібітор FDA-схвалений для рецидивний/рефрактерний FL: in EZH2- mutated FL after ≥2 prior lines, ORR 69%, mPFS 13.8 міс. (E7438-202 Morschhauser Lancet Oncol 2020); in EZH2-WT FL, ORR 35%, mPFS 11.1 міс. — mutated population had stronger responses, leading to a companion-діагностичний-paired показання per SRC-NCCN-BCELL-2025, SRC-ESMO-FL-2024.
```

**EN excerpt:**
```
EZH2 Y641 hotspot activating mutations occur in ~20-25% of follicular lymphoma (and rarely in DLBCL/HGBL). Tazemetostat is a selective EZH2 inhibitor FDA-approved for relapsed/refra...

```

**UA excerpt:**
```
EZH2 Y641 hotspot activating мутації occur in ~20-25% of фолікулярна лімфома (and рідко in DLBCL/HGBL). Tazemetostat is a селективний EZH2 інгібітор FDA-схвалений для рецидивний/рефрактерний FL: in EZH2- mutated FL after...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 98/200: f-0099 - CRITICAL

**Entity:** `BMA-FANCA-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fanca_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `heterozygous) in EOC: Fanconi-; pathway gene; biallelic loss = Fanconi; recessive). Heterozygous carriers have uncertain; risk. FANCA included in some HRR panels (FANCL on PROfound HRR list). PARPi off-label consideration in HRD-positive. ESCAT IIIA / OncoKB
`

**Current value:**
```
FANCA герміногенний (heterozygous) in EOC: Fanconi-анемія-pathway gene; biallelic loss = Fanconi анемія (recessive). Heterozygous carriers have uncertain рак risk. FANCA included in some HRR panels (FANCL on PROfound HRR list). PARPi off-label consideration in HRD-positive. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
FANCA germline (heterozygous) in EOC: Fanconi-anemia-pathway gene; biallelic loss = Fanconi anemia (recessive). Heterozygous carriers have uncertain cancer risk. FANCA included in s...

```

**UA excerpt:**
```
FANCA герміногенний (heterozygous) in EOC: Fanconi-анемія-pathway gene; biallelic loss = Fanconi анемія (recessive). Heterozygous carriers have uncertain рак risk. FANCA included in some HRR panels (FANCL on PROfound HRR...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 99/200: f-0100 - CRITICAL

**Entity:** `BMA-FANCL-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fancl_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `heterozygous) in EOC: Fanconi-; pathway gene; biallelic loss = Fanconi; recessive). Heterozygous carriers have uncertain; risk. FANCL included in some HRR panels (FANCL on PROfound HRR list). PARPi off-label consideration in HRD-positive. ESCAT IIIA / OncoKB
`

**Current value:**
```
FANCL герміногенний (heterozygous) in EOC: Fanconi-анемія-pathway gene; biallelic loss = Fanconi анемія (recessive). Heterozygous carriers have uncertain рак risk. FANCL included in some HRR panels (FANCL on PROfound HRR list). PARPi off-label consideration in HRD-positive. ESCAT IIIA / OncoKB рівень 3B.
```

**EN excerpt:**
```
FANCL germline (heterozygous) in EOC: Fanconi-anemia-pathway gene; biallelic loss = Fanconi anemia (recessive). Heterozygous carriers have uncertain cancer risk. FANCL included in s...

```

**UA excerpt:**
```
FANCL герміногенний (heterozygous) in EOC: Fanconi-анемія-pathway gene; biallelic loss = Fanconi анемія (recessive). Heterozygous carriers have uncertain рак risk. FANCL included in some HRR panels (FANCL on PROfound HRR...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 100/200: f-0101 - CRITICAL

**Entity:** `BMA-FGFR1-AMP-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr1_amp_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `PFS on aromatase; actionability is unproven — multiple FGFR-TKI trials (lucitanib FINESSE, dovitinib) negative or marginal
`

**Current value:**
```
FGFR1 ампліфікація in HR+ рак молочної залози (~10-15%): прогностичний for endocrine-терапія resistance and зменшений PFS on aromatase інгібітор. терапевтичний actionability is unproven — multiple FGFR-TKI trials (lucitanib FINESSE, dovitinib) negative or marginal. ні FGFR-targeted drug схвалений для рак молочної залози.
```

**EN excerpt:**
```
FGFR1 amplification in HR+ breast cancer (~10-15%): prognostic for endocrine-therapy resistance and reduced PFS on aromatase inhibitor. Therapeutic actionability is unproven — multi...

```

**UA excerpt:**
```
FGFR1 ампліфікація in HR+ рак молочної залози (~10-15%): прогностичний for endocrine-терапія resistance and зменшений PFS on aromatase інгібітор. терапевтичний actionability is unproven — multiple FGFR-TKI trials (lucitan...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 101/200: f-0102 - CRITICAL

**Entity:** `BMA-FGFR1-AMP-NSCLC-SQUAMOUS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr1_amp_nsclc_squamous.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in squamous NSCLC (~15-20%). Multiple FGFR-TKI trials (lucitanib, AZD4547, BGJ398, erdafitinib) showed modest activity (ORR 5-15%) — FGFR1-amp does not predict robust; Erdafitinib is NOT; FGFR1-amp NSCLC (label is FGFR2/3 in urothelial; applies; FGFR1-amp is
`

**Current value:**
```
FGFR1 ампліфікація in squamous NSCLC (~15-20%). Multiple FGFR-TKI trials (lucitanib, AZD4547, BGJ398, erdafitinib) showed modest activity (ORR 5-15%) — FGFR1-amp does not predict robust відповідь. Erdafitinib is NOT схвалений для FGFR1-amp NSCLC (label is FGFR2/3 in urothelial). стандарт squamous NSCLC терапія applies; FGFR1-amp is дослідження-only actionability.
```

**EN excerpt:**
```
FGFR1 amplification in squamous NSCLC (~15-20%). Multiple FGFR-TKI trials (lucitanib, AZD4547, BGJ398, erdafitinib) showed modest activity (ORR 5-15%) — FGFR1-amp does not predict r...

```

**UA excerpt:**
```
FGFR1 ампліфікація in squamous NSCLC (~15-20%). Multiple FGFR-TKI trials (lucitanib, AZD4547, BGJ398, erdafitinib) showed modest activity (ORR 5-15%) — FGFR1-amp does not predict robust відповідь. Erdafitinib is NOT схвал...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 102/200: f-0103 - CRITICAL

**Entity:** `BMA-FGFR2-AMP-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_amp_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in gastric/GEJ adenocarcinoma (~5-7% high-level): bemarituzumab (anti-FGFR2b mAb) + mFOLFOX; PFS/OS in FGFR2b-overexpressing 1L gastric (FIGHT; Wainberg Lancet Oncol 2022 — PFS; FGFR-TKIs (futibatinib, pemigatinib) have basket activity in FGFR2-amp gastric
`

**Current value:**
```
FGFR2 ампліфікація in gastric/GEJ adenocarcinoma (~5-7% high-level): bemarituzumab (anti-FGFR2b mAb) + mFOLFOX6 покращений PFS/OS in FGFR2b-overexpressing 1L gastric (FIGHT фаза 2, Wainberg Lancet Oncol 2022 — PFS 9.5 проти 7.4 міс.; фаза 3 FORTITUDE-101 ongoing). селективний FGFR-TKIs (futibatinib, pemigatinib) have basket activity in FGFR2-amp gastric.
```

**EN excerpt:**
```
FGFR2 amplification in gastric/GEJ adenocarcinoma (~5-7% high-level): bemarituzumab (anti-FGFR2b mAb) + mFOLFOX6 improved PFS/OS in FGFR2b-overexpressing 1L gastric (FIGHT phase 2,...

```

**UA excerpt:**
```
FGFR2 ампліфікація in gastric/GEJ adenocarcinoma (~5-7% high-level): bemarituzumab (anti-FGFR2b mAb) + mFOLFOX6 покращений PFS/OS in FGFR2b-overexpressing 1L gastric (FIGHT фаза 2, Wainberg Lancet Oncol 2022 — PFS 9.5 про...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 103/200: f-0104 - CRITICAL

**Entity:** `BMA-FGFR2-BICC1-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_bicc1_cholangio.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `partner in intrahepatic cholangiocarcinoma; is identical to gene-level FGFR; pemigatinib (FIGHT-202) and futibatinib (FOENIX-CCA; partner identity does not currently modify TKI selection
`

**Current value:**
```
BICC1-FGFR2 злиття is the найбільш поширений FGFR2 злиття partner in intrahepatic cholangiocarcinoma. лікування is identical to gene-level FGFR2-злиття: pemigatinib (FIGHT-202) and futibatinib (FOENIX-CCA2). злиття-partner identity does not currently modify TKI selection.
```

**EN excerpt:**
```
BICC1-FGFR2 fusion is the most common FGFR2 fusion partner in intrahepatic cholangiocarcinoma. Treatment is identical to gene-level FGFR2-fusion: pemigatinib (FIGHT-202) and futibat...

```

**UA excerpt:**
```
BICC1-FGFR2 злиття is the найбільш поширений FGFR2 злиття partner in intrahepatic cholangiocarcinoma. лікування is identical to gene-level FGFR2-злиття: pemigatinib (FIGHT-202) and futibatinib (FOENIX-CCA2). злиття-partne...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 104/200: f-0105 - CRITICAL

**Entity:** `BMA-FGFR2-FUSION-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_fusion_cholangio.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in intrahepatic cholangiocarcinoma (~10-15%): pemigatinib (FIGHT-202, Abou-Alfa Lancet Oncol 2020 — ORR 36%, mDOR; and futibatinib (FOENIX-CCA2, Goyal NEJM 2023 — ORR 42%, mPFS; cholangio. Futibatinib is; and has activity against pemigatinib-resistance gatekeeper
`

**Current value:**
```
FGFR2 злиття in intrahepatic cholangiocarcinoma (~10-15%): pemigatinib (FIGHT-202, Abou-Alfa Lancet Oncol 2020 — ORR 36%, mDOR 9.1 міс.) and futibatinib (FOENIX-CCA2, Goyal NEJM 2023 — ORR 42%, mPFS 9.0 міс.) are FDA-схвалений для previously-treated FGFR2-злиття cholangio. Futibatinib is необоротний and has activity against pemigatinib-resistance gatekeeper мутації.
```

**EN excerpt:**
```
FGFR2 fusion in intrahepatic cholangiocarcinoma (~10-15%): pemigatinib (FIGHT-202, Abou-Alfa Lancet Oncol 2020 — ORR 36%, mDOR 9.1 mo) and futibatinib (FOENIX-CCA2, Goyal NEJM 2023...

```

**UA excerpt:**
```
FGFR2 злиття in intrahepatic cholangiocarcinoma (~10-15%): pemigatinib (FIGHT-202, Abou-Alfa Lancet Oncol 2020 — ORR 36%, mDOR 9.1 міс.) and futibatinib (FOENIX-CCA2, Goyal NEJM 2023 — ORR 42%, mPFS 9.0 міс.) are FDA-схва...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 105/200: f-0106 - CRITICAL

**Entity:** `BMA-FGFR2-MUTATION-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_mutation_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `Pemigatinib and erdafitinib have basket activity (FIGHT-207, Mirati / NCI-MATCH EAY131-W) — ORR ~25-30% in FGFR2-mutant endometrial; for endometrial alone; agnostic FGFR-TKI label not yet granted
`

**Current value:**
```
FGFR2 мутація in endometrial карцинома (~10-12% endometrioid гістологія). Pemigatinib and erdafitinib have basket activity (FIGHT-207, Mirati / NCI-MATCH EAY131-W) — ORR ~25-30% in FGFR2-mutant endometrial. ні regulatory схвалення for endometrial alone; пухлина-agnostic FGFR-TKI label not yet granted.
```

**EN excerpt:**
```
FGFR2 mutation in endometrial carcinoma (~10-12% endometrioid histology). Pemigatinib and erdafitinib have basket activity (FIGHT-207, Mirati / NCI-MATCH EAY131-W) — ORR ~25-30% in...

```

**UA excerpt:**
```
FGFR2 мутація in endometrial карцинома (~10-12% endometrioid гістологія). Pemigatinib and erdafitinib have basket activity (FIGHT-207, Mirati / NCI-MATCH EAY131-W) — ORR ~25-30% in FGFR2-mutant endometrial. ні regulatory...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 106/200: f-0107 - CRITICAL

**Entity:** `BMA-FGFR2-MUTATION-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_mutation_urothelial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `erdafitinib (BLC2001, Loriot NEJM 2019 — ORR 40%; THOR; Loriot NEJM 2023 — OS HR 0.64 vs chemo) is FDA-; urothelial 2L+. FGFR; than FGFR3 in urothelial
`

**Current value:**
```
FGFR2 злиття / активуюча мутація in метастатичний уротеліальна карцинома: erdafitinib (BLC2001, Loriot NEJM 2019 — ORR 40%; THOR фаза 3, Loriot NEJM 2023 — OS HR 0.64 vs chemo) is FDA-схвалений для FGFR2/3-altered місцево-поширений or метастатичний urothelial 2L+. FGFR2 альтерації less поширений than FGFR3 in urothelial (~3% проти ~15%).
```

**EN excerpt:**
```
FGFR2 fusion / activating mutation in metastatic urothelial carcinoma: erdafitinib (BLC2001, Loriot NEJM 2019 — ORR 40%; THOR phase 3, Loriot NEJM 2023 — OS HR 0.64 vs chemo) is FDA...

```

**UA excerpt:**
```
FGFR2 злиття / активуюча мутація in метастатичний уротеліальна карцинома: erdafitinib (BLC2001, Loriot NEJM 2019 — ORR 40%; THOR фаза 3, Loriot NEJM 2023 — OS HR 0.64 vs chemo) is FDA-схвалений для FGFR2/3-altered місцево...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 107/200: f-0108 - CRITICAL

**Entity:** `BMA-FGFR3-MUTATION-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr3_mutation_mm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `places MMSET/FGFR3 under IgH control; ~30% of t(4;14) cases co-express FGFR3, with; Y373C, K650E). Despite preclinical; dovitinib, AZD4547) in MM showed limited
`

**Current value:**
```
In множинна мієлома, t(4;14) транслокація places MMSET/FGFR3 under IgH control; ~30% of t(4;14) cases co-express FGFR3, with рідкісний набутий activating point мутації (Y373C, K650E). Despite preclinical чутливість, клінічні дослідження of FGFR інгібітори (dovitinib, AZD4547) in MM showed limited ефективність; ні FGFR-таргетна терапія is схвалений in MM. лікування is стандарт t(4;14) високого ризику мієлома protocol (proteasome-інгібітор-based).
```

**EN excerpt:**
```
In multiple myeloma, t(4;14) translocation places MMSET/FGFR3 under IgH control; ~30% of t(4;14) cases co-express FGFR3, with rare acquired activating point mutations (Y373C, K650E)...

```

**UA excerpt:**
```
In множинна мієлома, t(4;14) транслокація places MMSET/FGFR3 under IgH control; ~30% of t(4;14) cases co-express FGFR3, with рідкісний набутий activating point мутації (Y373C, K650E). Despite preclinical чутливість, кліні...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 108/200: f-0109 - CRITICAL

**Entity:** `BMA-FGFR3-R248C-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr3_r248c_urothelial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FGFR3 R248C is an extracellular-domain; included in the erdafitinib companion-; to S249C: erdafitinib in 2L
`

**Current value:**
```
FGFR3 R248C is an extracellular-domain активуюча мутація included in the erdafitinib companion-діагностичний FGFR альтерація panel. лікування-еквівалентний to S249C: erdafitinib in 2L+ метастатичний уротеліальна карцинома per THOR.
```

**EN excerpt:**
```
FGFR3 R248C is an extracellular-domain activating mutation included in the erdafitinib companion-diagnostic FGFR alteration panel. Treatment-equivalent to S249C: erdafitinib in 2L+...

```

**UA excerpt:**
```
FGFR3 R248C is an extracellular-domain активуюча мутація included in the erdafitinib companion-діагностичний FGFR альтерація panel. лікування-еквівалентний to S249C: erdafitinib in 2L+ метастатичний уротеліальна карцинома...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 109/200: f-0110 - CRITICAL

**Entity:** `BMA-FGFR3-S249C-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr3_s249c_urothelial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FGFR3 S249C is the; THOR cohort 1, Loriot 2023 — OS`

**Current value:**
```
FGFR3 S249C is the найбільш поширений activating FGFR3 мутація in уротеліальна карцинома. Erdafitinib is схвалений для FGFR3-altered метастатичний уротеліальна карцинома after platinum хіміотерапія (THOR cohort 1, Loriot 2023 — OS виграш vs хіміотерапія in 2L+).
```

**EN excerpt:**
```
FGFR3 S249C is the most common activating FGFR3 mutation in urothelial carcinoma. Erdafitinib is approved for FGFR3-altered metastatic urothelial carcinoma after platinum chemothera...

```

**UA excerpt:**
```
FGFR3 S249C is the найбільш поширений activating FGFR3 мутація in уротеліальна карцинома. Erdafitinib is схвалений для FGFR3-altered метастатичний уротеліальна карцинома after platinum хіміотерапія (THOR cohort 1, Loriot...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 110/200: f-0111 - CRITICAL

**Entity:** `BMA-FGFR3-TACC3-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr3_tacc3_urothelial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `is an activating; Included in the erdafitinib companion-; list. Erdafitinib responses in; positive patients are; positive (THOR, BLC
`

**Current value:**
```
FGFR3-TACC3 злиття is an activating перебудова in уротеліальна карцинома (~2-3%). Included in the erdafitinib companion-діагностичний FGFR альтерація list. Erdafitinib responses in злиття-positive patients are співставний з those in мутація-positive (THOR, BLC2001).
```

**EN excerpt:**
```
FGFR3-TACC3 fusion is an activating rearrangement in urothelial carcinoma (~2-3%). Included in the erdafitinib companion-diagnostic FGFR alteration list. Erdafitinib responses in fu...

```

**UA excerpt:**
```
FGFR3-TACC3 злиття is an activating перебудова in уротеліальна карцинома (~2-3%). Included in the erdafitinib companion-діагностичний FGFR альтерація list. Erdafitinib responses in злиття-positive patients are співставний...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 111/200: f-0112 - CRITICAL

**Entity:** `BMA-FGFR3-Y373C-UROTHELIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_fgfr3_y373c_urothelial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FGFR3 Y373C is a transmembrane-domain; included in erdafitinib companion-; identical to other actionable FGFR; erdafitinib 2L+ post-platinum
`

**Current value:**
```
FGFR3 Y373C is a transmembrane-domain активуюча мутація in уротеліальна карцинома; included in erdafitinib companion-діагностичний panel. лікування identical to other actionable FGFR3 мутації: erdafitinib 2L+ post-platinum.
```

**EN excerpt:**
```
FGFR3 Y373C is a transmembrane-domain activating mutation in urothelial carcinoma; included in erdafitinib companion-diagnostic panel. Treatment identical to other actionable FGFR3...

```

**UA excerpt:**
```
FGFR3 Y373C is a transmembrane-domain активуюча мутація in уротеліальна карцинома; included in erdafitinib companion-діагностичний panel. лікування identical to other actionable FGFR3 мутації: erdafitinib 2L+ post-platinu...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 112/200: f-0113 - CRITICAL

**Entity:** `BMA-FLT3-D835-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_d835_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-D835 (TKD) in newly-diagnosed AML`

**Current value:**
```
FLT3-D835 (TKD) in newly-diagnosed AML: мідостаурин + 7+3 was studied in FLT3-mutant (ITD or TKD) AML in RATIFY (Stone 2017) — виграш driven перш за все by ITD subset, with smaller magnitude in TKD. квізартиніб (type II FLT3i) is INACTIVE against TKD D835 (target alternate conformation). гілтеритиніб (type I) and мідостаурин retain activity. ELN 2022 прогностичний impact of D835 alone is intermediate.
```

**EN excerpt:**
```
'FLT3-D835 (TKD) in newly-diagnosed AML: midostaurin + 7+3 was studied

```

**UA excerpt:**
```
'FLT3-D835 (TKD) in newly-diagnosed AML: мідостаурин + 7+3 was

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 113/200: f-0114 - CRITICAL

**Entity:** `BMA-FLT3-D835-AML-RR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_d835_aml_rr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-D835 in`

**Current value:**
```
FLT3-D835 in р/р AML: гілтеритиніб перевершує сальвадж chemo (ADMIRAL, Perl 2019 — pre-specified subset analysis showed activity across both ITD and D835/TKD; D835 subset відповідь rates подібний to ITD overall). гілтеритиніб is переважний type-I FLT3i for D835-mutant р/р хвороба. квізартиніб remains протипоказаний (ні D835 activity).
```

**EN excerpt:**
```
'FLT3-D835 in R/R AML: gilteritinib superior to salvage chemo (ADMIRAL,

```

**UA excerpt:**
```
'FLT3-D835 in р/р AML: гілтеритиніб перевершує сальвадж chemo

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 114/200: f-0115 - CRITICAL

**Entity:** `BMA-FLT3-F691L-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_f691l_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-F691L is a gatekeeper; arising under FLT3-TKI`

**Current value:**
```
FLT3-F691L is a gatekeeper мутація arising under FLT3-TKI селективний pressure (гілтеритиніб, квізартиніб). Confers cross-резистентність до найбільш current FLT3i. Crenolanib (експериментальний type-I) and next-gen FLT3i retain partial activity. ні схвалений targeted option — включення в клінічне дослідження or сальвадж chemo + allo-SCT.
```

**EN excerpt:**
```
'FLT3-F691L is a gatekeeper mutation arising under FLT3-TKI selective
```

**UA excerpt:**
```
'FLT3-F691L is a gatekeeper мутація arising under FLT3-TKI селективний
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 115/200: f-0116 - CRITICAL

**Entity:** `BMA-FLT3-ITD-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_itd_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-ITD in newly-diagnosed AML; OS vs chemo alone in fit adults (RATIFY, Stone NEJM; in QuANTUM-First (Erba Lancet; OS HR 0.78). FLT3-ITD remains a poor-risk marker (ELN 2022) when allelic ratio high; allo-SCT in CR1 indicated
`

**Current value:**
```
FLT3-ITD in newly-diagnosed AML: мідостаурин + 7+3 індукція + high-доза цитарабін консолідація + підтримка покращений OS vs chemo alone in fit adults (RATIFY, Stone NEJM 2017 — 4-рік OS HR 0.78). квізартиніб + 7+3 + підтримка also перевершує in QuANTUM-First (Erba Lancet 2023 — 4-рік OS HR 0.78). FLT3-ITD remains a poor-risk marker (ELN 2022) when allelic ratio high; allo-SCT in CR1 indicated.
```

**EN excerpt:**
```
FLT3-ITD in newly-diagnosed AML: midostaurin + 7+3 induction + high-dose cytarabine consolidation + maintenance improved OS vs chemo alone in fit adults (RATIFY, Stone NEJM 2017 — 4...

```

**UA excerpt:**
```
FLT3-ITD in newly-diagnosed AML: мідостаурин + 7+3 індукція + high-доза цитарабін консолідація + підтримка покращений OS vs chemo alone in fit adults (RATIFY, Stone NEJM 2017 — 4-рік OS HR 0.78). квізартиніб + 7+3 + підтр...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 116/200: f-0117 - CRITICAL

**Entity:** `BMA-FLT3-ITD-AML-RR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_itd_aml_rr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-ITD in; chemo (ADMIRAL, Perl NEJM 2019 — OS; L for FLT3-mutant; AML and is a bridge to allo-SCT; QuANTUM-R) but FDA label is 1L only
`

**Current value:**
```
FLT3-ITD in рецидивний/рефрактерний AML: гілтеритиніб монотерапія перевершує сальвадж chemo (ADMIRAL, Perl NEJM 2019 — OS 9.3 проти 5.6 міс., HR 0.64). гілтеритиніб is переважний 2L for FLT3-mutant р/р AML and is a bridge to allo-SCT. квізартиніб also active р/р (QuANTUM-R) but FDA label is 1L only (р/р label withdrawn).
```

**EN excerpt:**
```
FLT3-ITD in relapsed/refractory AML: gilteritinib monotherapy superior to salvage chemo (ADMIRAL, Perl NEJM 2019 — OS 9.3 vs 5.6 mo, HR 0.64). Gilteritinib is preferred 2L for FLT3-...

```

**UA excerpt:**
```
FLT3-ITD in рецидивний/рефрактерний AML: гілтеритиніб монотерапія перевершує сальвадж chemo (ADMIRAL, Perl NEJM 2019 — OS 9.3 проти 5.6 міс., HR 0.64). гілтеритиніб is переважний 2L for FLT3-mutant р/р AML and is a bridge...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 117/200: f-0118 - CRITICAL

**Entity:** `BMA-FLT3-ITD-B-ALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_flt3_itd_b_all.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `FLT3-ITD in B-ALL is; enriched in MLL/KMT2A-; have basket activity in FLT3-mutant ALL but; agnostic FLT3i actionability is informed by AML; specific B-ALL trials pending
`

**Current value:**
```
FLT3-ITD in B-ALL is рідкісний (~1-3% дорослий; enriched in MLL/KMT2A- перебудований infant ALL). гілтеритиніб and мідостаурин have basket activity in FLT3-mutant ALL but ні phase-3 докази. пухлина-agnostic FLT3i actionability is informed by AML дані; specific B-ALL trials pending.
```

**EN excerpt:**
```
FLT3-ITD in B-ALL is rare (~1-3% adult; enriched in MLL/KMT2A- rearranged infant ALL). Gilteritinib and midostaurin have basket activity in FLT3-mutant ALL but no phase-3 evidence....

```

**UA excerpt:**
```
FLT3-ITD in B-ALL is рідкісний (~1-3% дорослий; enriched in MLL/KMT2A- перебудований infant ALL). гілтеритиніб and мідостаурин have basket activity in FLT3-mutant ALL but ні phase-3 докази. пухлина-agnostic FLT3i actionab...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 118/200: f-0119 - CRITICAL

**Entity:** `BMA-HER2-AMP-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in RAS/BRAF-WT population; FDA 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Strickler Lancet Oncol 2023 — ORR 38%, mDOR; also has activity (DESTINY-CRC01 Siena Lancet Oncol 2021 — ORR 45% in HER2 IHC 3+ RAS-WT) and; for HER2-positive solid tumors that have progressed on prior; HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed; in 2L because RAS-driven resistance is well-documented per SRC-NCCN-COLON-
`

**Current value:**
```
HER2-amplified метастатичний колоректальний рак (~3-5% in RAS/BRAF-WT population): тукатиніб + трастузумаб is схвалений FDA 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Strickler Lancet Oncol 2023 — ORR 38%, mDOR 12 міс.) per SRC-NCCN-COLON-2025. трастузумаб дерукстекан also has activity (DESTINY-CRC01 Siena Lancet Oncol 2021 — ORR 45% in HER2 IHC 3+ RAS-WT) and пухлина-agnostic FDA схвалення (2024) for HER2-positive solid tumors that have progressed on prior терапія. Older трастузумаб + лапатиніб (HERACLES) is referenced as alternative. RAS-mutant tumors should not receive HER2-directed терапія in 2L because RAS-driven resistance is well-documented per SRC-NCCN-COLON-2025.
```

**EN excerpt:**
```
HER2-amplified metastatic colorectal cancer (~3-5% in RAS/BRAF-WT population): tucatinib + trastuzumab is FDA-approved 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Stric...

```

**UA excerpt:**
```
HER2-amplified метастатичний колоректальний рак (~3-5% in RAS/BRAF-WT population): тукатиніб + трастузумаб is схвалений FDA 2L+ for HER2- positive RAS-WT mCRC based on MOUNTAINEER (Strickler Lancet Oncol 2023 — ORR 38%, m...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 119/200: f-0120 - CRITICAL

**Entity:** `BMA-HER2-AMP-ESOPHAGEAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_esophageal.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `HER2-positive esophageal/GEJ adenocarcinoma scored by gastric criteria; L (cross-referenced from ToGA / KEYNOTE-811) per SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-; fluoropyrimidine/platinum is FDA-; HER2+ PD-L1 CPS; GEJ adenocarcinoma (KEYNOTE-; FDA 2L+ for HER2-positive; gastric/GEJ adenocarcinoma (DESTINY-Gastric; Siewert types). Squamous-cell esophageal
`

**Current value:**
```
HER2-positive esophageal/GEJ adenocarcinoma scored by gastric criteria: трастузумаб + хіміотерапія is переважний 1L (cross-referenced from ToGA / KEYNOTE-811) per SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024. пембролізумаб + трастузумаб + fluoropyrimidine/platinum is FDA-схвалений для HER2+ PD-L1 CPS≥1 метастатичний GEJ adenocarcinoma (KEYNOTE-811). трастузумаб дерукстекан is схвалений FDA 2L+ for HER2-positive поширений gastric/GEJ adenocarcinoma (DESTINY-Gastric01 включає Siewert types). Squamous-cell esophageal карцинома is HER2-negative as a rule and is not in scope for HER2-directed терапія.
```

**EN excerpt:**
```
HER2-positive esophageal/GEJ adenocarcinoma scored by gastric criteria: trastuzumab + chemotherapy is preferred 1L (cross-referenced from ToGA / KEYNOTE-811) per SRC-NCCN-ESOPHAGEAL...

```

**UA excerpt:**
```
HER2-positive esophageal/GEJ adenocarcinoma scored by gastric criteria: трастузумаб + хіміотерапія is переважний 1L (cross-referenced from ToGA / KEYNOTE-811) per SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024. пембро...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 120/200: f-0121 - CRITICAL

**Entity:** `BMA-HER2-AMP-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_her2_amp_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `HER2-positive gastric/GEJ adenocarcinoma; L (ToGA Bang Lancet; FDA 1L for HER2-positive PD-L1 CPS; per SRC-NCCN-GASTRIC-2025, SRC-ESMO-GASTRIC-2024 (KEYNOTE-; FDA 2L+ for HER2-positive (IHC; gastric/GEJ adenocarcinoma based on DESTINY-Gastric01 (Shitara NEJM 2020 — ORR
`

**Current value:**
```
HER2-positive gastric/GEJ adenocarcinoma (~15-20%): трастузумаб + хіміотерапія is стандарт 1L (ToGA Bang Lancet 2010 — міс. 13.8 проти 11.1 міс., HR 0.74). пембролізумаб + трастузумаб + chemo is схвалений FDA 1L for HER2-positive PD-L1 CPS ≥1 метастатичний gastric/GEJ хвороба per SRC-NCCN-GASTRIC-2025, SRC-ESMO-GASTRIC-2024 (KEYNOTE-811). трастузумаб дерукстекан (T-DXd) is схвалений FDA 2L+ for HER2-positive (IHC 3+ або 2+) поширений gastric/GEJ adenocarcinoma based on DESTINY-Gastric01 (Shitara NEJM 2020 — ORR 51% проти 14% with хіміотерапія).
```

**EN excerpt:**
```
HER2-positive gastric/GEJ adenocarcinoma (~15-20%): trastuzumab + chemotherapy is standard 1L (ToGA Bang Lancet 2010 — mOS 13.8 vs 11.1 mo, HR 0.74). Pembrolizumab + trastuzumab + c...

```

**UA excerpt:**
```
HER2-positive gastric/GEJ adenocarcinoma (~15-20%): трастузумаб + хіміотерапія is стандарт 1L (ToGA Bang Lancet 2010 — міс. 13.8 проти 11.1 міс., HR 0.74). пембролізумаб + трастузумаб + chemo is схвалений FDA 1L for HER2-...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 121/200: f-0122 - CRITICAL

**Entity:** `BMA-HRD-STATUS-BREAST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_breast.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `HER2-negative, ~5-10% of; FDA 2L+ for gBRCAm HER2-negative; based on OlympiAD (Robson NEJM 2017 — mPFS; criteria (EMBRACA Litton NEJM 2018 — mPFS; HR 0.54) per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-; for 1y is FDA-; gBRCAm HER2-negative; based on OlympiA (Tutt NEJM 2021 — IDFS HR 0.58, OS HR 0.68) per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-EARLY-
`

**Current value:**
```
герміногенний BRCA1/2 мутація (gBRCAm) рак молочної залози (HER2-negative, ~5-10% of метастатичний): олапариб монотерапія is схвалений FDA 2L+ for gBRCAm HER2-negative метастатичний рак молочної залози based on OlympiAD (Robson NEJM 2017 — mPFS 7.0 проти 4.2 міс., HR 0.58); талазопариб монотерапія is схвалений FDA on подібний criteria (EMBRACA Litton NEJM 2018 — mPFS 8.6 проти 5.6 міс., HR 0.54) per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-метастатичний-2024. In the ад'ювантний setting, олапариб for 1y is FDA-схвалений для gBRCAm HER2-negative високого ризику early рак молочної залози based on OlympiA (Tutt NEJM 2021 — IDFS HR 0.58, OS HR 0.68) per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-EARLY-2024.
```

**EN excerpt:**
```
Germline BRCA1/2 mutation (gBRCAm) breast cancer (HER2-negative, ~5-10% of metastatic): olaparib monotherapy is FDA-approved 2L+ for gBRCAm HER2-negative metastatic breast cancer ba...

```

**UA excerpt:**
```
герміногенний BRCA1/2 мутація (gBRCAm) рак молочної залози (HER2-negative, ~5-10% of метастатичний): олапариб монотерапія is схвалений FDA 2L+ for gBRCAm HER2-negative метастатичний рак молочної залози based on OlympiAD (...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 122/200: f-0123 - CRITICAL

**Entity:** `BMA-HRD-STATUS-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `encompassing BRCA1/2-mutated and BRCA-WT/HRD; for BRCA1/2-mutated newly-diagnosed; ovarian after CR/PR to platinum (SOLO-1 Moore NEJM 2018 — mPFS not reached vs; HR 0.30) per SRC-NCCN-OVARIAN-2025, SRC-ESMO-OVARIAN-; for HRD-positive (BRCA-mut OR HRD-genomic) post-1L platinum; PAOLA-1 Ray-Coquard NEJM 2019 — HRD subgroup mPFS; all-comers (PRIMA Gonzalez-Martin NEJM 2019), with the strongest; in HRD-positive subgroup
`

**Current value:**
```
HRD-positive високого ступеня serous ovarian карцинома (~50% — encompassing BRCA1/2-mutated and BRCA-WT/HRD+): інгібітор PARP підтримка after platinum відповідь is схвалений FDA 1L. олапариб монотерапія підтримка for BRCA1/2-mutated newly-diagnosed поширений ovarian after CR/PR to platinum (SOLO-1 Moore NEJM 2018 — mPFS not reached vs 13.8 міс., HR 0.30) per SRC-NCCN-OVARIAN-2025, SRC-ESMO-OVARIAN-2024. олапариб + бевацизумаб підтримка for HRD-positive (BRCA-mut OR HRD-genomic) post-1L platinum + бевацизумаб (PAOLA-1 Ray-Coquard NEJM 2019 — HRD subgroup mPFS 37 проти 17 міс., HR 0.33). нірапариб монотерапія підтримка is схвалений для all-comers (PRIMA Gonzalez-Martin NEJM 2019), with the strongest виграш in HRD-positive subgroup.
```

**EN excerpt:**
```
HRD-positive high-grade serous ovarian carcinoma (~50% — encompassing BRCA1/2-mutated and BRCA-WT/HRD+): PARP inhibitor maintenance after platinum response is FDA-approved 1L. Olapa...

```

**UA excerpt:**
```
HRD-positive високого ступеня serous ovarian карцинома (~50% — encompassing BRCA1/2-mutated and BRCA-WT/HRD+): інгібітор PARP підтримка after platinum відповідь is схвалений FDA 1L. олапариб монотерапія підтримка for BRCA...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 123/200: f-0124 - CRITICAL

**Entity:** `BMA-HRD-STATUS-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `after ≥4 months of platinum-based 1L (FOLFIRINOX or; FDA based on POLO (Golan NEJM 2019 — mPFS; HR 0.53; OS not significant) per SRC-NCCN-PANCREATIC-2025, SRC-ESMO-PANCREATIC-2024. Platinum-containing 1L is; for gBRCAm PDAC over; because of platinum; rates substantially higher in gBRCAm patients per multiple retrospective series cited in SRC-NCCN-PANCREATIC-
`

**Current value:**
```
герміногенний BRCA1/2 мутація in метастатичний PDAC (~5-7%): олапариб монотерапія підтримка after ≥4 months of platinum-based 1L (FOLFIRINOX or гемцитабін/цисплатин) without прогресування is схвалений FDA based on POLO (Golan NEJM 2019 — mPFS 7.4 проти 3.8 міс., HR 0.53; OS not significant) per SRC-NCCN-PANCREATIC-2025, SRC-ESMO-PANCREATIC-2024. Platinum-containing 1L is переважний for gBRCAm PDAC over гемцитабін + наб-паклітаксел because of platinum чутливість (FOLFIRINOX відповідь rates substantially higher in gBRCAm patients per multiple retrospective series cited in SRC-NCCN-PANCREATIC-2025).
```

**EN excerpt:**
```
Germline BRCA1/2 mutation in metastatic PDAC (~5-7%): olaparib monotherapy maintenance after ≥4 months of platinum-based 1L (FOLFIRINOX or gemcitabine/cisplatin) without progression...

```

**UA excerpt:**
```
герміногенний BRCA1/2 мутація in метастатичний PDAC (~5-7%): олапариб монотерапія підтримка after ≥4 months of platinum-based 1L (FOLFIRINOX or гемцитабін/цисплатин) without прогресування is схвалений FDA based on POLO (G...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 124/200: f-0125 - CRITICAL

**Entity:** `BMA-HRD-STATUS-PROSTATE`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_hrd_status_prostate.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `Homologous-recombination-repair (HRR) gene; BRCA1/2 (and several other HRR genes per FDA label) mCRPC after; failure based on PROfound (de Bono NEJM 2020 — cohort A BRCA1/2/ATM mPFS; acetate (MAGNITUDE Chi JCO 2023) and; PROpel Clarke NEJM Evid 2022) are; FDA 1L combinations for HRR- altered mCRPC; TALAPRO-2 Agarwal Lancet 2023) is FDA-; HRR-mutated mCRPC 1L
`

**Current value:**
```
Homologous-recombination-repair (HRR) gene альтерації in метастатичний castration-resistant рак передміхурової залози (mCRPC, ~25% соматичний + герміногенний): олапариб монотерапія is FDA-схвалений для BRCA1/2 (and several other HRR genes per FDA label) mCRPC after ензалутамід or абіратерон failure based on PROfound (de Bono NEJM 2020 — cohort A BRCA1/2/ATM mPFS 7.4 проти 3.6 міс., HR 0.34). нірапариб + абіратерон acetate (MAGNITUDE Chi JCO 2023) and олапариб + абіратерон (PROpel Clarke NEJM Evid 2022) are схвалений FDA 1L combinations for HRR- altered mCRPC. талазопариб + ензалутамід (TALAPRO-2 Agarwal Lancet 2023) is FDA-схвалений для HRR-mutated mCRPC 1L. рукапариб has accelerated схвалення for BRCA1/2 mCRPC post-androgen-receptor- таргетна терапія (TRITON3) per SRC-NCCN-PROSTATE-2025, SRC-ESMO-PROSTATE-2024, SRC-EAU-PROSTATE-2024.
```

**EN excerpt:**
```
Homologous-recombination-repair (HRR) gene alterations in metastatic castration-resistant prostate cancer (mCRPC, ~25% somatic + germline): olaparib monotherapy is FDA-approved for...

```

**UA excerpt:**
```
Homologous-recombination-repair (HRR) gene альтерації in метастатичний castration-resistant рак передміхурової залози (mCRPC, ~25% соматичний + герміногенний): олапариб монотерапія is FDA-схвалений для BRCA1/2 (and severa...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 125/200: f-0126 - CRITICAL

**Entity:** `BMA-IDH1-R132-CHOLANGIO`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132_cholangio.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132 hotspot; occur in ~13-20% of intrahepatic cholangiocarcinoma and are FDA Level-1 actionable; FDA 2021 for previously-treated IDH1-mutated; cholangiocarcinoma based on ClarIDHy (Abou-Alfa Lancet Oncol 2020 — mPFS; on rank-preserving structural failure time analysis adjusted for crossover) per SRC-NCCN-HEPATOBILIARY. Comprehensive molecular profiling; to identify IDH1-R132 patients who can be sequenced to; in 2L after
`

**Current value:**
```
IDH1 R132 hotspot мутації occur in ~13-20% of intrahepatic cholangiocarcinoma and are FDA Level-1 actionable. івосиденіб was схвалений FDA 2021 for previously-treated IDH1-mutated місцево-поширений/метастатичний cholangiocarcinoma based on ClarIDHy (Abou-Alfa Lancet Oncol 2020 — mPFS 2.7 проти 1.4 міс., HR 0.37; OS виграш on rank-preserving structural failure time analysis adjusted for crossover) per SRC-NCCN-HEPATOBILIARY. Comprehensive molecular profiling при діагнозі is рекомендований to identify IDH1-R132 patients who can be sequenced to івосиденіб in 2L after гемцитабін/цисплатин ± дурвалумаб (TOPAZ-1) 1L.
```

**EN excerpt:**
```
IDH1 R132 hotspot mutations occur in ~13-20% of intrahepatic cholangiocarcinoma and are FDA Level-1 actionable. Ivosidenib was FDA-approved 2021 for previously-treated IDH1-mutated...

```

**UA excerpt:**
```
IDH1 R132 hotspot мутації occur in ~13-20% of intrahepatic cholangiocarcinoma and are FDA Level-1 actionable. івосиденіб was схвалений FDA 2021 for previously-treated IDH1-mutated місцево-поширений/метастатичний cholangio...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 126/200: f-0127 - CRITICAL

**Entity:** `BMA-IDH1-R132C-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132c_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132C — same; implications as R132H; targets all R`

**Current value:**
```
IDH1 R132C — same терапевтичний implications as R132H; івосиденіб targets all R132 варіанти.
```

**EN excerpt:**
```
IDH1 R132C — same therapeutic implications as R132H; ivosidenib targets all R132 variants.
```

**UA excerpt:**
```
IDH1 R132C — same терапевтичний implications as R132H; івосиденіб targets all R132 варіанти.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 127/200: f-0128 - CRITICAL

**Entity:** `BMA-IDH1-R132C-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132c_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132C in glioma — non-canonical; same; implications as R132H (vorasidenib`

**Current value:**
```
IDH1 R132C in glioma — non-canonical; same терапевтичний implications as R132H (vorasidenib).
```

**EN excerpt:**
```
IDH1 R132C in glioma — non-canonical; same therapeutic implications as R132H (vorasidenib).
```

**UA excerpt:**
```
IDH1 R132C in glioma — non-canonical; same терапевтичний implications as R132H (vorasidenib).
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 128/200: f-0129 - CRITICAL

**Entity:** `BMA-IDH1-R132G-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132g_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132G — covered by IDH1-mut label (any R`

**Current value:**
```
IDH1 R132G — covered by IDH1-mut label (any R132).
```

**EN excerpt:**
```
IDH1 R132G — covered by IDH1-mut label (any R132).
```

**UA excerpt:**
```
IDH1 R132G — covered by IDH1-mut label (any R132).
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 129/200: f-0130 - CRITICAL

**Entity:** `BMA-IDH1-R132G-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132g_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132G — covered by IDH-mut glioma vorasidenib label`

**Current value:**
```
IDH1 R132G — covered by IDH-mut glioma vorasidenib label.
```

**EN excerpt:**
```
IDH1 R132G — covered by IDH-mut glioma vorasidenib label.
```

**UA excerpt:**
```
IDH1 R132G — covered by IDH-mut glioma vorasidenib label.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 130/200: f-0131 - CRITICAL

**Entity:** `BMA-IDH1-R132H-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `AGILE, Montesinos et al. NEJM 2022 — combo with; L unfit, AGILE) doubles OS vs`

**Current value:**
```
IDH1 R132 мутації (~6-10% of AML). івосиденіб монотерапія (AGILE, Montesinos et al. NEJM 2022 — combo with азацитидин; AG120-C-001 — монотерапія in р/р) схвалений FDA. івосиденіб + азацитидин (1L unfit, AGILE) doubles OS vs азацитидин alone.
```

**EN excerpt:**
```
IDH1 R132 mutations (~6-10% of AML). Ivosidenib monotherapy (AGILE, Montesinos et al. NEJM 2022 — combo with azacitidine; AG120-C-001 — monotherapy in R/R) FDA-approved. Ivosidenib...

```

**UA excerpt:**
```
IDH1 R132 мутації (~6-10% of AML). івосиденіб монотерапія (AGILE, Montesinos et al. NEJM 2022 — combo with азацитидин; AG120-C-001 — монотерапія in р/р) схвалений FDA. івосиденіб + азацитидин (1L unfit, AGILE) doubles OS...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 131/200: f-0132 - CRITICAL

**Entity:** `BMA-IDH1-R132H-B-ALL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_b_all.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in B-ALL is; in lymphoid; per usual B-ALL`

**Current value:**
```
IDH1 мутація in B-ALL is рідкісний. Tissue-agnostic івосиденіб not схвалений in lymphoid; per usual B-ALL педіатричний/дорослий protocol.
```

**EN excerpt:**
```
IDH1 mutation in B-ALL is rare. Tissue-agnostic ivosidenib not approved in lymphoid; per usual B-ALL pediatric/adult protocol.

```

**UA excerpt:**
```
IDH1 мутація in B-ALL is рідкісний. Tissue-agnostic івосиденіб not схвалений in lymphoid; per usual B-ALL педіатричний/дорослий protocol.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 132/200: f-0133 - CRITICAL

**Entity:** `BMA-IDH1-R132H-DLBCL-NOS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_dlbcl_nos.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132H in DLBCL is exceptional; per usual DLBCL algorithm`

**Current value:**
```
IDH1 R132H in DLBCL is exceptional (<1%). ні таргетна терапія in this показання; per usual DLBCL algorithm.
```

**EN excerpt:**
```
IDH1 R132H in DLBCL is exceptional (<1%). No targeted therapy in this indication; per usual DLBCL algorithm.
```

**UA excerpt:**
```
IDH1 R132H in DLBCL is exceptional (<1%). ні таргетна терапія in this показання; per usual DLBCL algorithm.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 133/200: f-0134 - CRITICAL

**Entity:** `BMA-IDH1-R132H-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132H — defines IDH-mutant astrocytoma (WHO 2021 grade 2-4) and oligodendroglioma (with 1p/19q codeletion). Vorasidenib; PFS in residual; grade 2 IDH-mut glioma post- resection (INDIGO, Mellinghoff et al. NEJM; FDA 2024. For grade 4 (IDH-mut GBM; still RT + TMZ
`

**Current value:**
```
IDH1 R132H — defines IDH-mutant astrocytoma (WHO 2021 grade 2-4) and oligodendroglioma (with 1p/19q codeletion). Vorasidenib покращений PFS in residual/рецидивний grade 2 IDH-mut glioma post- resection (INDIGO, Mellinghoff et al. NEJM 2023) — схвалений FDA 2024. For grade 4 (IDH-mut GBM еквівалентний) — стандарт лікування still RT + TMZ; івосиденіб explored.
```

**EN excerpt:**
```
IDH1 R132H — defines IDH-mutant astrocytoma (WHO 2021 grade 2-4) and oligodendroglioma (with 1p/19q codeletion). Vorasidenib improved PFS in residual/recurrent grade 2 IDH-mut gliom...

```

**UA excerpt:**
```
IDH1 R132H — defines IDH-mutant astrocytoma (WHO 2021 grade 2-4) and oligodendroglioma (with 1p/19q codeletion). Vorasidenib покращений PFS in residual/рецидивний grade 2 IDH-mut glioma post- resection (INDIGO, Mellinghof...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 134/200: f-0135 - CRITICAL

**Entity:** `BMA-IDH1-R132H-MDS-HR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_mds_hr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132 in MDS; active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR`

**Current value:**
```
IDH1 R132 in MDS — івосиденіб монотерапія active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). івосиденіб + азацитидин combos in дослідження. off-label NCCN-supported.
```

**EN excerpt:**
```
IDH1 R132 in MDS — ivosidenib monotherapy active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). Ivosidenib + azacitidine combos in trial. Off-label NCCN-supported.

```

**UA excerpt:**
```
IDH1 R132 in MDS — івосиденіб монотерапія active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). івосиденіб + азацитидин combos in дослідження. off-label NCCN-supported.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 135/200: f-0136 - CRITICAL

**Entity:** `BMA-IDH1-R132H-MDS-LR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132h_mds_lr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132 in MDS; active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR`

**Current value:**
```
IDH1 R132 in MDS — івосиденіб монотерапія active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). івосиденіб + азацитидин combos in дослідження. off-label NCCN-supported.
```

**EN excerpt:**
```
IDH1 R132 in MDS — ivosidenib monotherapy active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). Ivosidenib + azacitidine combos in trial. Off-label NCCN-supported.

```

**UA excerpt:**
```
IDH1 R132 in MDS — івосиденіб монотерапія active (DiNardo et al. JCO 2021 — ORR 75% MDS, CR 38%). івосиденіб + азацитидин combos in дослідження. off-label NCCN-supported.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 136/200: f-0137 - CRITICAL

**Entity:** `BMA-IDH1-R132L-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132l_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132L — covered by IDH1-mut label`

**Current value:**
```
IDH1 R132L — covered by IDH1-mut label.
```

**EN excerpt:**
```
IDH1 R132L — covered by IDH1-mut label.
```

**UA excerpt:**
```
IDH1 R132L — covered by IDH1-mut label.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 137/200: f-0138 - CRITICAL

**Entity:** `BMA-IDH1-R132L-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132l_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132L — covered by vorasidenib`

**Current value:**
```
IDH1 R132L — covered by vorasidenib.
```

**EN excerpt:**
```
IDH1 R132L — covered by vorasidenib.
```

**UA excerpt:**
```
IDH1 R132L — covered by vorasidenib.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 138/200: f-0139 - CRITICAL

**Entity:** `BMA-IDH1-R132S-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132s_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132S — covered by IDH1-mut label`

**Current value:**
```
IDH1 R132S — covered by IDH1-mut label.
```

**EN excerpt:**
```
IDH1 R132S — covered by IDH1-mut label.
```

**UA excerpt:**
```
IDH1 R132S — covered by IDH1-mut label.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 139/200: f-0140 - CRITICAL

**Entity:** `BMA-IDH1-R132S-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh1_r132s_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH1 R132S — covered by vorasidenib`

**Current value:**
```
IDH1 R132S — covered by vorasidenib.
```

**EN excerpt:**
```
IDH1 R132S — covered by vorasidenib.
```

**UA excerpt:**
```
IDH1 R132S — covered by vorasidenib.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 140/200: f-0141 - CRITICAL

**Entity:** `BMA-IDH2-R140Q-AITL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r140q_aitl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R140Q in AITL — much less; than R172 in T-cell; rationale extrapolated; case-report level`

**Current value:**
```
IDH2 R140Q in AITL — much less поширений than R172 in T-cell лімфома (myeloid pattern). енасиденіб rationale extrapolated; case-report level.
```

**EN excerpt:**
```
IDH2 R140Q in AITL — much less common than R172 in T-cell lymphoma (myeloid pattern). Enasidenib rationale extrapolated; case-report level.

```

**UA excerpt:**
```
IDH2 R140Q in AITL — much less поширений than R172 in T-cell лімфома (myeloid pattern). енасиденіб rationale extrapolated; case-report level.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 141/200: f-0142 - CRITICAL

**Entity:** `BMA-IDH2-R140Q-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r140q_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R140Q (~5-9% of AML; IDHIFA, AG221-C-001 Stein et al. Blood; IDH2-mut AML. IDHENTIFY (Ph3) confirmed OS; late-line. Combos with; Ph2) promising 1L unfit
`

**Current value:**
```
IDH2 R140Q (~5-9% of AML). енасиденіб (IDHIFA, AG221-C-001 Stein et al. Blood 2017) схвалений FDA 2017 for р/р IDH2-mut AML. IDHENTIFY (Ph3) confirmed OS виграш late-line. Combos with азацитидин (Ph2) promising 1L unfit.
```

**EN excerpt:**
```
IDH2 R140Q (~5-9% of AML). Enasidenib (IDHIFA, AG221-C-001 Stein et al. Blood 2017) FDA-approved 2017 for R/R IDH2-mut AML. IDHENTIFY (Ph3) confirmed OS benefit late-line. Combos wi...

```

**UA excerpt:**
```
IDH2 R140Q (~5-9% of AML). енасиденіб (IDHIFA, AG221-C-001 Stein et al. Blood 2017) схвалений FDA 2017 for р/р IDH2-mut AML. IDHENTIFY (Ph3) confirmed OS виграш late-line. Combos with азацитидин (Ph2) promising 1L unfit.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 142/200: f-0143 - CRITICAL

**Entity:** `BMA-IDH2-R140Q-DLBCL-NOS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r140q_dlbcl_nos.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R140Q in DLBCL is exceptional; per usual DLBCL algorithm`

**Current value:**
```
IDH2 R140Q in DLBCL is exceptional (<1%). ні таргетна терапія in this показання; per usual DLBCL algorithm.
```

**EN excerpt:**
```
IDH2 R140Q in DLBCL is exceptional (<1%). No targeted therapy in this indication; per usual DLBCL algorithm.
```

**UA excerpt:**
```
IDH2 R140Q in DLBCL is exceptional (<1%). ні таргетна терапія in this показання; per usual DLBCL algorithm.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 143/200: f-0144 - CRITICAL

**Entity:** `BMA-IDH2-R140Q-MDS-HR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r140q_mds_hr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R140Q in MDS; active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS; progresses to AML; IDH2i can delay; Not yet on full FDA MDS label (off-label use NCCN-supported
`

**Current value:**
```
IDH2 R140Q in MDS — енасиденіб монотерапія active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS часто progresses to AML; IDH2i can delay трансформація. Not yet on full FDA MDS label (off-label use NCCN-supported).
```

**EN excerpt:**
```
IDH2 R140Q in MDS — enasidenib monotherapy active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS often progresses to AML; IDH2i can delay transformation. Not yet on fu...

```

**UA excerpt:**
```
IDH2 R140Q in MDS — енасиденіб монотерапія active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS часто progresses to AML; IDH2i can delay трансформація. Not yet on full FDA MDS label (off-label use NCCN-supp...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 144/200: f-0145 - CRITICAL

**Entity:** `BMA-IDH2-R140Q-MDS-LR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r140q_mds_lr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R140Q in MDS; active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS; progresses to AML; IDH2i can delay; Not yet on full FDA MDS label (off-label use NCCN-supported
`

**Current value:**
```
IDH2 R140Q in MDS — енасиденіб монотерапія active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS часто progresses to AML; IDH2i can delay трансформація. Not yet on full FDA MDS label (off-label use NCCN-supported).
```

**EN excerpt:**
```
IDH2 R140Q in MDS — enasidenib monotherapy active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS often progresses to AML; IDH2i can delay transformation. Not yet on fu...

```

**UA excerpt:**
```
IDH2 R140Q in MDS — енасиденіб монотерапія active in MDS (NCT01915498, DiNardo et al. Blood 2018). IDH-mut MDS часто progresses to AML; IDH2i can delay трансформація. Not yet on full FDA MDS label (off-label use NCCN-supp...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 145/200: f-0147 - CRITICAL

**Entity:** `BMA-IDH2-R172K-AITL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r172k_aitl.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `occur in ~30% of AITL (TFH-derived PTCL; active in IDH2-mut AITL (small case series; Lemonnier et al. Blood 2016 / 2021). NCCN supports off-label use in; IDH2-mut AITL
`

**Current value:**
```
IDH2 R172 мутації occur in ~30% of AITL (TFH-derived PTCL). енасиденіб монотерапія active in IDH2-mut AITL (small case series; Lemonnier et al. Blood 2016 / 2021). NCCN supports off-label use in р/р IDH2-mut AITL.
```

**EN excerpt:**
```
IDH2 R172 mutations occur in ~30% of AITL (TFH-derived PTCL). Enasidenib monotherapy active in IDH2-mut AITL (small case series; Lemonnier et al. Blood 2016 / 2021). NCCN supports o...

```

**UA excerpt:**
```
IDH2 R172 мутації occur in ~30% of AITL (TFH-derived PTCL). енасиденіб монотерапія active in IDH2-mut AITL (small case series; Lemonnier et al. Blood 2016 / 2021). NCCN supports off-label use in р/р IDH2-mut AITL.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 146/200: f-0148 - CRITICAL

**Entity:** `BMA-IDH2-R172K-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r172k_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R172K — slightly; metabolic profile but same`

**Current value:**
```
IDH2 R172K — slightly відмінний metabolic profile but same енасиденіб показання.
```

**EN excerpt:**
```
IDH2 R172K — slightly different metabolic profile but same enasidenib indication.
```

**UA excerpt:**
```
IDH2 R172K — slightly відмінний metabolic profile but same енасиденіб показання.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 147/200: f-0149 - CRITICAL

**Entity:** `BMA-IDH2-R172K-MDS-HR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r172k_mds_hr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R172K in MDS — same; rationale as R140Q`

**Current value:**
```
IDH2 R172K in MDS — same енасиденіб rationale as R140Q.
```

**EN excerpt:**
```
IDH2 R172K in MDS — same enasidenib rationale as R140Q.
```

**UA excerpt:**
```
IDH2 R172K in MDS — same енасиденіб rationale as R140Q.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 148/200: f-0150 - CRITICAL

**Entity:** `BMA-IDH2-R172K-MDS-LR`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_idh2_r172k_mds_lr.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IDH2 R172K in MDS — same; rationale as R140Q`

**Current value:**
```
IDH2 R172K in MDS — same енасиденіб rationale as R140Q.
```

**EN excerpt:**
```
IDH2 R172K in MDS — same enasidenib rationale as R140Q.
```

**UA excerpt:**
```
IDH2 R172K in MDS — same енасиденіб rationale as R140Q.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 149/200: f-0151 - CRITICAL

**Entity:** `BMA-IGHV-UNMUTATED-CLL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_ighv_unmutated_cll.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `IGHV mutational status is a fundamental CLL risk stratifier and; per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has shorter; CIT — FCR, BR) and is now a strong; for continuous BTK; as 1L regardless of TP53 status. CLL14 (Fischer NEJM; fixed-duration vs chlorambucil; and ECOG E1912 (Shanafelt NEJM; vs FCR) are foundational trials that
`

**Current value:**
```
IGHV mutational status is a fundamental CLL risk stratifier and лікування-selection біомаркер per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has shorter відповідь to хіміоімунотерапія (CIT — FCR, BR) and is now a strong показання for continuous BTK інгібітор (ібрутиніб, акалабрутиніб, занубрутиніб) or fixed-duration венетоклакс-обінутузумаб as 1L regardless of TP53 status. CLL14 (Fischer NEJM 2019 — венетоклакс + обінутузумаб fixed-duration vs chlorambucil + обінутузумаб) and ECOG E1912 (Shanafelt NEJM 2019 — ібрутиніб + ритуксимаб vs FCR) are foundational trials that продемонстровано CIT inferiority зокрема in IGHV- unmutated subgroups. ESMO 2024 explicitly recommends against FCR/BR 1L in IGHV-unmutated patients.
```

**EN excerpt:**
```
IGHV mutational status is a fundamental CLL risk stratifier and treatment-selection biomarker per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has...

```

**UA excerpt:**
```
IGHV mutational status is a fundamental CLL risk stratifier and лікування-selection біомаркер per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022. IGHV-unmutated CLL has shorter відповідь to хіміоімунотерапія...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 150/200: f-0152 - CRITICAL

**Entity:** `BMA-JAK2-V617F-ET`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_jak2_v617f_et.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `JAK2 V617F is one of three defining drivers in essential thrombocythemia`

**Current value:**
```
JAK2 V617F is one of three defining drivers in essential thrombocythemia (~50-60%; CALR ~25-30%, MPL ~3-5%, triple-negative ~10-15%) and a WHO 2022 / ICC 2022 major діагностичний criterion (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). лікування is risk-stratified by IPSET-thrombosis (age, prior thrombosis, JAK2 V617F positivity, cardiovascular risk factors); високого ризику → cytoreduction with гідроксикарбамід (PT1 дослідження Harrison 2005 — перевершує thrombosis-free виживаність vs анагрелід in HU-naive ET); низького ризику → low-доза aspirin alone (or observation in CALR-mutated very-низького ризику per SRC-ESMO-MPN-2015).
```

**EN excerpt:**
```
'JAK2 V617F is one of three defining drivers in essential thrombocythemia
```

**UA excerpt:**
```
'JAK2 V617F is one of three defining drivers in essential thrombocythemia
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 151/200: f-0153 - CRITICAL

**Entity:** `BMA-JAK2-V617F-PMF`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_jak2_v617f_pmf.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `JAK2 V617F is one of three defining drivers in primary myelofibrosis`

**Current value:**
```
JAK2 V617F is one of three defining drivers in primary myelofibrosis (~50-60%; CALR ~25%, MPL ~5-10%, triple-negative ~10%) and a WHO 2022 / ICC 2022 major діагностичний criterion (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). лікування by symptom burden / risk score (DIPSS- Plus, MIPSS70, MIPSS70+v2): symptomatic intermediate/високого ризику → руксолитиніб (COMFORT-I Verstovsek 2012 — 41.9% spleen відповідь vs 0.7% placebo, OS виграш on extended спостереження); федратиніб for руксолитиніб-failure (JAKARTA2 Harrison 2017 — 31% spleen відповідь in RUX-failure); момелотиніб for anemic patients (MOMENTUM Verstovsek 2023 — перевершує анемія + symptom виграш vs danazol). алогенний HCT is the only curative терапія and is рекомендований for transplant- eligible higher-risk patients per SRC-NCCN-MPN-2025.
```

**EN excerpt:**
```
'JAK2 V617F is one of three defining drivers in primary myelofibrosis
```

**UA excerpt:**
```
'JAK2 V617F is one of three defining drivers in primary myelofibrosis
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 152/200: f-0154 - CRITICAL

**Entity:** `BMA-JAK2-V617F-PV`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_jak2_v617f_pv.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `JAK2 V617F is the defining driver of polycythemia vera`

**Current value:**
```
JAK2 V617F is the defining driver of polycythemia vera (~95%) and a WHO 2022 / ICC 2022 major діагностичний criterion (per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015). лікування is risk-stratified, not варіант-генотип directed: низького ризику PV → phlebotomy + low-доза aspirin; високого ризику PV (age ≥60 or prior thrombosis) → cytoreduction with гідроксикарбамід or інтерферон-alpha (ropeginterferon-alfa-2b, PROUD-PV / CONTINUATION-PV Gisslinger 2020 — перевершує molecular відповідь and виживаність без подій at 5y vs гідроксикарбамід); руксолитиніб (відповідь Vannucchi 2015 — 21% CHR + spleen відповідь vs 1% найкращий available терапія) for гідроксикарбамід- intolerant or -resistant хвороба.
```

**EN excerpt:**
```
'JAK2 V617F is the defining driver of polycythemia vera (~95%) and
```

**UA excerpt:**
```
'JAK2 V617F is the defining driver of polycythemia vera (~95%)
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 153/200: f-0155 - CRITICAL

**Entity:** `BMA-KIT-D816V-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_d816v_gist.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KIT D816V in GIST is; more typical of systemic mastocytosis) but emerges as a secondary; resistance. Ripretinib (INVICTUS, Blay Lancet Oncol 2020 — switch- control; with broad activation-loop coverage) and avapritinib (NAVIGATOR; FDA in PDGFRA D842V and ASM) retain activity vs D816V
`

**Current value:**
```
KIT D816V in GIST is рідкісний as primary мутація (more typical of systemic mastocytosis) but emerges as a secondary резистентна мутація under іматиніб pressure. Confers іматиніб + сунитиніб resistance. Ripretinib (INVICTUS, Blay Lancet Oncol 2020 — switch- control інгібітор with broad activation-loop coverage) and avapritinib (NAVIGATOR; схвалений FDA in PDGFRA D842V and ASM) retain activity vs D816V.
```

**EN excerpt:**
```
KIT D816V in GIST is rare as primary mutation (more typical of systemic mastocytosis) but emerges as a secondary resistance mutation under imatinib pressure. Confers imatinib + suni...

```

**UA excerpt:**
```
KIT D816V in GIST is рідкісний as primary мутація (more typical of systemic mastocytosis) but emerges as a secondary резистентна мутація under іматиніб pressure. Confers іматиніб + сунитиніб resistance. Ripretinib (INVICT...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 154/200: f-0156 - CRITICAL

**Entity:** `BMA-KIT-D816V-MASTOCYTOSIS`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_d816v_mastocytosis.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KIT D816V in; systemic mastocytosis (AdvSM; SM, SM-AHN, mast cell; Gotlib NEJM 2016 — ORR 60%) and avapritinib (PATHFINDER / EXPLORER, Gotlib JCO 2023 — ORR 75%, deeper molecular; Avapritinib selectively targets the D816V conformation with high potency; is INACTIVE against D816V — distinct from
`

**Current value:**
```
KIT D816V in поширений systemic mastocytosis (AdvSM — агресивний SM, SM-AHN, mast cell лейкоз): мідостаурин (EXPLORER / D2201 фаза 2, Gotlib NEJM 2016 — ORR 60%) and avapritinib (PATHFINDER / EXPLORER, Gotlib JCO 2023 — ORR 75%, deeper molecular відповідь) are FDA- схвалений. Avapritinib selectively targets the D816V conformation with high potency. іматиніб is INACTIVE against D816V — distinct from іматиніб-sensitive juxtamembrane мутації.
```

**EN excerpt:**
```
KIT D816V in advanced systemic mastocytosis (AdvSM — aggressive SM, SM-AHN, mast cell leukemia): midostaurin (EXPLORER / D2201 phase 2, Gotlib NEJM 2016 — ORR 60%) and avapritinib (...

```

**UA excerpt:**
```
KIT D816V in поширений systemic mastocytosis (AdvSM — агресивний SM, SM-AHN, mast cell лейкоз): мідостаурин (EXPLORER / D2201 фаза 2, Gotlib NEJM 2016 — ORR 60%) and avapritinib (PATHFINDER / EXPLORER, Gotlib JCO 2023 — O...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 155/200: f-0157 - CRITICAL

**Entity:** `BMA-KIT-EXON11-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_exon11_gist.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `mg/day is; L (B2222, Demetri NEJM 2002 — ORR 67%; EORTC-62005 / S0033 confirmed long-term; Exon 11 mutants have the longest PFS and OS on; of any GIST
`

**Current value:**
```
KIT exon 11 мутація in GIST: іматиніб 400 mg/day is стандарт 1L (B2222, Demetri NEJM 2002 — ORR 67%; EORTC-62005 / S0033 confirmed long-term виграш). Exon 11 mutants have the longest PFS and OS on іматиніб of any GIST генотип. ад'ювантний іматиніб 3 рік post- resection покращує RFS in високого ризику хвороба (SSG-XVIII / ACOSOG-Z9001).
```

**EN excerpt:**
```
KIT exon 11 mutation in GIST: imatinib 400 mg/day is standard 1L (B2222, Demetri NEJM 2002 — ORR 67%; EORTC-62005 / S0033 confirmed long-term benefit). Exon 11 mutants have the long...

```

**UA excerpt:**
```
KIT exon 11 мутація in GIST: іматиніб 400 mg/day is стандарт 1L (B2222, Demetri NEJM 2002 — ORR 67%; EORTC-62005 / S0033 confirmed long-term виграш). Exon 11 mutants have the longest PFS and OS on іматиніб of any GIST ген...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 156/200: f-0158 - CRITICAL

**Entity:** `BMA-KIT-EXON13-17-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_exon13_17_gist.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `failure cluster in exon 13/14 (ATP-binding pocket — V654A, T670I) or exon 17/18 (activation loop — D816, D820, N822, Y; Demetri Lancet 2006) covers exon 13/14 secondaries; GRID) provides 3L coverage; ripretinib (INVICTUS) is a switch-control; active across both classes
`

**Current value:**
```
Secondary KIT мутації after іматиніб failure cluster in exon 13/14 (ATP-binding pocket — V654A, T670I) or exon 17/18 (activation loop — D816, D820, N822, Y823). сунитиніб (Demetri Lancet 2006) covers exon 13/14 secondaries; регорафеніб (GRID) provides 3L coverage; ripretinib (INVICTUS) is a switch-control інгібітор active across both classes — переважний 4L+.
```

**EN excerpt:**
```
Secondary KIT mutations after imatinib failure cluster in exon 13/14 (ATP-binding pocket — V654A, T670I) or exon 17/18 (activation loop — D816, D820, N822, Y823). Sunitinib (Demetri...

```

**UA excerpt:**
```
Secondary KIT мутації after іматиніб failure cluster in exon 13/14 (ATP-binding pocket — V654A, T670I) or exon 17/18 (activation loop — D816, D820, N822, Y823). сунитиніб (Demetri Lancet 2006) covers exon 13/14 secondarie...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 157/200: f-0159 - CRITICAL

**Entity:** `BMA-KIT-EXON9-GIST`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_exon9_gist.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KIT exon 9 GIST has shorter PFS on; mg vs exon; mg/day (split 400 mg BID; PFS and OS vs 400 mg in this; EORTC-62005 / MetaGIST meta-analysis, Gastrointest Stromal; L for exon
`

**Current value:**
```
KIT exon 9 GIST has shorter PFS on іматиніб 400 mg vs exon 11. іматиніб 800 mg/day (split 400 mg BID) покращує PFS and OS vs 400 mg in this генотип (EORTC-62005 / MetaGIST meta-analysis, Gastrointest Stromal пухлина Meta-Analysis 2010). High доза is стандарт 1L for exon 9.
```

**EN excerpt:**
```
KIT exon 9 GIST has shorter PFS on imatinib 400 mg vs exon 11. Imatinib 800 mg/day (split 400 mg BID) improves PFS and OS vs 400 mg in this genotype (EORTC-62005 / MetaGIST meta-ana...

```

**UA excerpt:**
```
KIT exon 9 GIST has shorter PFS on іматиніб 400 mg vs exon 11. іматиніб 800 mg/day (split 400 mg BID) покращує PFS and OS vs 400 mg in this генотип (EORTC-62005 / MetaGIST meta-analysis, Gastrointest Stromal пухлина Meta-...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 158/200: f-0160 - CRITICAL

**Entity:** `BMA-KIT-MUTATION-AML`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_mutation_aml.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in core-binding-factor (CBF) AML (t(8;21) / inv(16)) is enriched (~25-30%) and confers; OS vs CBF-AML wild-type; CALGB-10801, Marcucci Blood 2020 — CBF-AML setting) is being studied; not; Avapritinib has activity in D816V-mutant AML basket cohorts but; ELN 2022 considers KIT; in CBF-AML as intermediate; risk modifier within the
`

**Current value:**
```
KIT мутація in core-binding-factor (CBF) AML (t(8;21) / inv(16)) is enriched (~25-30%) and confers гірше OS vs CBF-AML wild-type. дазатиніб + 7+3 + HiDAC консолідація (CALGB-10801, Marcucci Blood 2020 — CBF-AML setting) is being studied; not стандарт. Avapritinib has activity in D816V-mutant AML basket cohorts but ні AML схвалення. ELN 2022 considers KIT мутація in CBF-AML as intermediate/несприятливий-risk modifier within the сприятливий CBF subset.
```

**EN excerpt:**
```
KIT mutation in core-binding-factor (CBF) AML (t(8;21) / inv(16)) is enriched (~25-30%) and confers worse OS vs CBF-AML wild-type. Dasatinib + 7+3 + HiDAC consolidation (CALGB-10801...

```

**UA excerpt:**
```
KIT мутація in core-binding-factor (CBF) AML (t(8;21) / inv(16)) is enriched (~25-30%) and confers гірше OS vs CBF-AML wild-type. дазатиніб + 7+3 + HiDAC консолідація (CALGB-10801, Marcucci Blood 2020 — CBF-AML setting) i...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 159/200: f-0161 - CRITICAL

**Entity:** `BMA-KIT-MUTATION-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kit_mutation_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in mucosal / acral / chronic-sun-damaged; in cutaneous CSD-low; has activity (Carvajal JCO 2013; Hodi JCO 2013 — ORR 16-23% in selected KIT-mutant; Exon 11 L576P and exon 13 K642E are the; is reserved for IO-; or IO-ineligible KIT-mutant
`

**Current value:**
```
KIT мутація in mucosal / acral / chronic-sun-damaged меланома (~15-20% of these підтипи; рідкісний in cutaneous CSD-low): іматиніб has activity (Carvajal JCO 2013; Hodi JCO 2013 — ORR 16-23% in selected KIT-mutant меланома). Exon 11 L576P and exon 13 K642E are the найбільш іматиніб-responsive варіанти. Modern перша лінія is імунотерапія (anti-PD-1 ± anti-CTLA-4); іматиніб is reserved for IO-рефрактерний or IO-ineligible KIT-mutant хвороба.
```

**EN excerpt:**
```
KIT mutation in mucosal / acral / chronic-sun-damaged melanoma (~15-20% of these subtypes; rare in cutaneous CSD-low): imatinib has activity (Carvajal JCO 2013; Hodi JCO 2013 — ORR...

```

**UA excerpt:**
```
KIT мутація in mucosal / acral / chronic-sun-damaged меланома (~15-20% of these підтипи; рідкісний in cutaneous CSD-low): іматиніб has activity (Carvajal JCO 2013; Hodi JCO 2013 — ORR 16-23% in selected KIT-mutant меланом...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 160/200: f-0162 - CRITICAL

**Entity:** `BMA-KRAS-A146T-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_a146t_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS A146T`

**Current value:**
```
KRAS A146T — рідкісний, anti-EGFR протипоказання marker. ні таргетна терапія.
```

**EN excerpt:**
```
KRAS A146T — rare, anti-EGFR contraindication marker. No targeted therapy.
```

**UA excerpt:**
```
KRAS A146T — рідкісний, anti-EGFR протипоказання marker. ні таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 161/200: f-0163 - CRITICAL

**Entity:** `BMA-KRAS-A146T-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_a146t_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS A146T in NSCLC`

**Current value:**
```
KRAS A146T in NSCLC — рідкісний; ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS A146T in NSCLC — rare; no approved targeted therapy.
```

**UA excerpt:**
```
KRAS A146T in NSCLC — рідкісний; ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 162/200: f-0164 - CRITICAL

**Entity:** `BMA-KRAS-A146T-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_a146t_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS A146T in PDAC`

**Current value:**
```
KRAS A146T in PDAC — рідкісний; ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS A146T in PDAC — rare; no approved targeted therapy.
```

**UA excerpt:**
```
KRAS A146T in PDAC — рідкісний; ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 163/200: f-0165 - CRITICAL

**Entity:** `BMA-KRAS-EXON3-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_exon3_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS exon 3 codon 59/61 in mCRC — extended-RAS WT criterion fails; anti-EGFR`

**Current value:**
```
KRAS exon 3 codon 59/61 in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.
```

**EN excerpt:**
```
KRAS exon 3 codon 59/61 in mCRC — extended-RAS WT criterion fails; anti-EGFR (cetuximab/panitumumab) contraindicated. Standard chemo ± bevacizumab.

```

**UA excerpt:**
```
KRAS exon 3 codon 59/61 in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 164/200: f-0166 - CRITICAL

**Entity:** `BMA-KRAS-EXON4-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_exon4_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS exon 4 codon 117/146 in mCRC — extended-RAS WT criterion fails; anti-EGFR`

**Current value:**
```
KRAS exon 4 codon 117/146 in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.
```

**EN excerpt:**
```
KRAS exon 4 codon 117/146 in mCRC — extended-RAS WT criterion fails; anti-EGFR (cetuximab/panitumumab) contraindicated. Standard chemo ± bevacizumab.

```

**UA excerpt:**
```
KRAS exon 4 codon 117/146 in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 165/200: f-0167 - CRITICAL

**Entity:** `BMA-KRAS-G12C-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in mCRC (~3-4%): single-agent KRASG12C
`

**Current value:**
```
KRAS G12C in mCRC (~3-4%): single-agent KRASG12C інгібітори insufficient (intrinsic EGFR feedback). комбінація адаграсиб + цетуксимаб (KRYSTAL-1, Yaeger et al. NEJM 2023) ORR 46%, PFS 6.9 mo. соторасиб + панітумумаб (CodeBreaK 300, Fakih et al. NEJM 2023) ORR 26% vs investigator's choice. Both схвалений FDA 2024.
```

**EN excerpt:**
```
'KRAS G12C in mCRC (~3-4%): single-agent KRASG12C inhibitors insufficient

```

**UA excerpt:**
```
'KRAS G12C in mCRC (~3-4%): single-agent KRASG12C інгібітори

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 166/200: f-0168 - CRITICAL

**Entity:** `BMA-KRAS-G12C-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `occur in ~15-25% of endometrioid endometrial cancers`

**Current value:**
```
KRAS мутації occur in ~15-25% of endometrioid endometrial cancers; G12C is a minority subset. Tissue-agnostic rationale with соторасиб/адаграсиб supported by NCCN as off-label option in pretreated G12C+ хвороба.
```

**EN excerpt:**
```
'KRAS mutations occur in ~15-25% of endometrioid endometrial cancers;
```

**UA excerpt:**
```
'KRAS мутації occur in ~15-25% of endometrioid endometrial cancers;
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 167/200: f-0169 - CRITICAL

**Entity:** `BMA-KRAS-G12C-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in gastric/GEJ adenocarcinoma is`

**Current value:**
```
KRAS G12C in gastric/GEJ adenocarcinoma is рідкісний. соторасиб basket дані limited; дослідження-only.
```

**EN excerpt:**
```
'KRAS G12C in gastric/GEJ adenocarcinoma is rare. Sotorasib basket
```

**UA excerpt:**
```
'KRAS G12C in gastric/GEJ adenocarcinoma is рідкісний. соторасиб
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 168/200: f-0170 - CRITICAL

**Entity:** `BMA-KRAS-G12C-HCC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_hcc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in HCC is`

**Current value:**
```
KRAS G12C in HCC is рідкісний. соторасиб not схвалений in HCC; дослідження-only.
```

**EN excerpt:**
```
'KRAS G12C in HCC is rare. Sotorasib not approved in HCC; trial-only.
```

**UA excerpt:**
```
'KRAS G12C in HCC is рідкісний. соторасиб not схвалений in HCC;
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 169/200: f-0171 - CRITICAL

**Entity:** `BMA-KRAS-G12C-MM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_mm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in; tissue-agnostic G12Ci`

**Current value:**
```
KRAS G12C in мієлома — рідкісний; tissue-agnostic G12Ci (соторасиб/адаграсиб) not схвалений in heme. дослідження-only consideration.
```

**EN excerpt:**
```
'KRAS G12C in myeloma — rare; tissue-agnostic G12Ci (sotorasib/adagrasib)
```

**UA excerpt:**
```
'KRAS G12C in мієлома — рідкісний; tissue-agnostic G12Ci (соторасиб/адаграсиб)
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 170/200: f-0172 - CRITICAL

**Entity:** `BMA-KRAS-G12C-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in; NSCLC (~13% of adenocarcinoma`

**Current value:**
```
KRAS G12C in поширений NSCLC (~13% of adenocarcinoma): соторасиб (CodeBreaK 100/200) and адаграсиб (KRYSTAL-1) are FDA/EMA-схвалений для previously-treated метастатичний хвороба. ORR ~40%, PFS ~6 mo. перша лінія KRYSTAL-7 (адаграсиб + пембролізумаб) and CodeBreaK 202 ongoing.
```

**EN excerpt:**
```
'KRAS G12C in advanced NSCLC (~13% of adenocarcinoma): sotorasib

```

**UA excerpt:**
```
'KRAS G12C in поширений NSCLC (~13% of adenocarcinoma): соторасиб

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 171/200: f-0173 - CRITICAL

**Entity:** `BMA-KRAS-G12C-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C in ovarian (mostly`

**Current value:**
```
KRAS G12C in ovarian (mostly низького ступеня serous) is рідкісний. Tissue- agnostic basket дані (CodeBreaK 100 multi-пухлина cohort) show modest activity. NCCN supports off-label use after стандарт терапія in G12C+ поширений ovarian.
```

**EN excerpt:**
```
'KRAS G12C in ovarian (mostly low-grade serous) is rare. Tissue-
```

**UA excerpt:**
```
'KRAS G12C in ovarian (mostly низького ступеня serous) is рідкісний.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 172/200: f-0174 - CRITICAL

**Entity:** `BMA-KRAS-G12C-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12c_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12C is; G12D and`

**Current value:**
```
KRAS G12C is рідкісний in PDAC (~1-2%, проти ~30% G12D and ~25% G12V). соторасиб (CodeBreaK 100 PDAC cohort, Strickler et al. NEJM 2023) ORR 21%, PFS 4 mo in pretreated G12C PDAC. адаграсиб (KRYSTAL-1 GI cohort) ORR 33%. NCCN recommends in 2L+.
```

**EN excerpt:**
```
'KRAS G12C is rare in PDAC (~1-2%, vs ~30% G12D and ~25% G12V).
```

**UA excerpt:**
```
'KRAS G12C is рідкісний in PDAC (~1-2%, проти ~30% G12D and ~25%
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 173/200: f-0175 - CRITICAL

**Entity:** `BMA-KRAS-G12D-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D in mCRC predicts anti-EGFR resistance; only (MRTX1133, RMC-`

**Current value:**
```
KRAS G12D in mCRC predicts anti-EGFR resistance. ні схвалений таргетна терапія 2026; дослідження-only (MRTX1133, RMC-9805 + цетуксимаб combos).
```

**EN excerpt:**
```
KRAS G12D in mCRC predicts anti-EGFR resistance. No approved targeted therapy 2026; trial-only (MRTX1133, RMC-9805 + cetuximab combos).

```

**UA excerpt:**
```
KRAS G12D in mCRC predicts anti-EGFR resistance. ні схвалений таргетна терапія 2026; дослідження-only (MRTX1133, RMC-9805 + цетуксимаб combos).

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 174/200: f-0176 - CRITICAL

**Entity:** `BMA-KRAS-G12D-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D in endometrial`

**Current value:**
```
KRAS G12D in endometrial — поширений in endometrioid; ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS G12D in endometrial — common in endometrioid; no approved targeted therapy.
```

**UA excerpt:**
```
KRAS G12D in endometrial — поширений in endometrioid; ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 175/200: f-0177 - CRITICAL

**Entity:** `BMA-KRAS-G12D-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D in gastric`

**Current value:**
```
KRAS G12D in gastric — ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS G12D in gastric — no approved targeted therapy.
```

**UA excerpt:**
```
KRAS G12D in gastric — ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 176/200: f-0178 - CRITICAL

**Entity:** `BMA-KRAS-G12D-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D in NSCLC (~5%) — pan-KRAS / G12D-; in early trials. ICI-based; per usual NSCLC algorithm`

**Current value:**
```
KRAS G12D in NSCLC (~5%) — pan-KRAS / G12D-селективний інгібітори in early trials. ICI-based схеми переважний per usual NSCLC algorithm.
```

**EN excerpt:**
```
KRAS G12D in NSCLC (~5%) — pan-KRAS / G12D-selective inhibitors in early trials. ICI-based regimens preferred per usual NSCLC algorithm.

```

**UA excerpt:**
```
KRAS G12D in NSCLC (~5%) — pan-KRAS / G12D-селективний інгібітори in early trials. ICI-based схеми переважний per usual NSCLC algorithm.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 177/200: f-0179 - CRITICAL

**Entity:** `BMA-KRAS-G12D-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D in mucinous`

**Current value:**
```
KRAS G12D in mucinous/низького ступеня serous ovarian — ні схвалений drug; дослідження-only (MRTX1133).
```

**EN excerpt:**
```
KRAS G12D in mucinous/low-grade serous ovarian — no approved drug; trial-only (MRTX1133).
```

**UA excerpt:**
```
KRAS G12D in mucinous/низького ступеня serous ovarian — ні схвалений drug; дослідження-only (MRTX1133).
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 178/200: f-0180 - CRITICAL

**Entity:** `BMA-KRAS-G12D-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12d_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12D is the; PDAC driver (~35-40%). MRTX1133 (Mirati/Bristol) and RMC-9805 are in clinical development; ASTX295 / BI-2865 also active; yet (2026); NCCN flags
`

**Current value:**
```
KRAS G12D is the найбільш поширений PDAC driver (~35-40%). MRTX1133 (Mirati/Bristol) and RMC-9805 are in clinical development; ASTX295 / BI-2865 also active. ні FDA схвалення yet (2026); NCCN flags клінічне дослідження.
```

**EN excerpt:**
```
KRAS G12D is the most common PDAC driver (~35-40%). MRTX1133 (Mirati/Bristol) and RMC-9805 are in clinical development; ASTX295 / BI-2865 also active. No FDA approval yet (2026); NC...

```

**UA excerpt:**
```
KRAS G12D is the найбільш поширений PDAC driver (~35-40%). MRTX1133 (Mirati/Bristol) and RMC-9805 are in clinical development; ASTX295 / BI-2865 also active. ні FDA схвалення yet (2026); NCCN flags клінічне дослідження.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 179/200: f-0181 - CRITICAL

**Entity:** `BMA-KRAS-G12V-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12v_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12V in mCRC — anti-EGFR`

**Current value:**
```
KRAS G12V in mCRC — anti-EGFR протипоказання marker, ні таргетна терапія. стандарт chemo ± anti-VEGF.
```

**EN excerpt:**
```
KRAS G12V in mCRC — anti-EGFR contraindication marker, no targeted therapy. Standard chemo ± anti-VEGF.
```

**UA excerpt:**
```
KRAS G12V in mCRC — anti-EGFR протипоказання marker, ні таргетна терапія. стандарт chemo ± anti-VEGF.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 180/200: f-0182 - CRITICAL

**Entity:** `BMA-KRAS-G12V-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12v_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12V in endometrial — POLE/MMR/p53 subtyping drives 1L`

**Current value:**
```
KRAS G12V in endometrial — POLE/MMR/p53 subtyping drives 1L.
```

**EN excerpt:**
```
KRAS G12V in endometrial — POLE/MMR/p53 subtyping drives 1L.
```

**UA excerpt:**
```
KRAS G12V in endometrial — POLE/MMR/p53 subtyping drives 1L.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 181/200: f-0183 - CRITICAL

**Entity:** `BMA-KRAS-G12V-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12v_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12V in; serous / mucinous ovarian`

**Current value:**
```
KRAS G12V in низького ступеня serous / mucinous ovarian — ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS G12V in low-grade serous / mucinous ovarian — no approved targeted therapy.
```

**UA excerpt:**
```
KRAS G12V in низького ступеня serous / mucinous ovarian — ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 182/200: f-0184 - CRITICAL

**Entity:** `BMA-KRAS-G12V-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12v_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12V in PDAC — second-; and TCR therapies in`

**Current value:**
```
KRAS G12V in PDAC — second-найбільш поширений driver. ні схвалений drug 2026; pan-KRAS інгібітори and TCR therapies in дослідження.
```

**EN excerpt:**
```
KRAS G12V in PDAC — second-most common driver. No approved drug 2026; pan-KRAS inhibitors and TCR therapies in trial.

```

**UA excerpt:**
```
KRAS G12V in PDAC — second-найбільш поширений driver. ні схвалений drug 2026; pan-KRAS інгібітори and TCR therapies in дослідження.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 183/200: f-0185 - CRITICAL

**Entity:** `BMA-KRAS-G12X-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g12x_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G12 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR`

**Current value:**
```
KRAS G12 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.
```

**EN excerpt:**
```
KRAS G12 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (cetuximab/panitumumab) contraindicated. Standard chemo ± bevacizumab.

```

**UA excerpt:**
```
KRAS G12 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 184/200: f-0186 - CRITICAL

**Entity:** `BMA-KRAS-G13D-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g13d_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G13D in mCRC — historical signal of partial; De Roock 2010) was not confirmed prospectively. Treat as RAS-mut, anti-EGFR
`

**Current value:**
```
KRAS G13D in mCRC — historical signal of partial цетуксимаб відповідь (De Roock 2010) was not confirmed prospectively. Treat as RAS-mut, anti-EGFR протипоказаний.
```

**EN excerpt:**
```
KRAS G13D in mCRC — historical signal of partial cetuximab response (De Roock 2010) was not confirmed prospectively. Treat as RAS-mut, anti-EGFR contraindicated.

```

**UA excerpt:**
```
KRAS G13D in mCRC — historical signal of partial цетуксимаб відповідь (De Roock 2010) was not confirmed prospectively. Treat as RAS-mut, anti-EGFR протипоказаний.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 185/200: f-0187 - CRITICAL

**Entity:** `BMA-KRAS-G13D-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g13d_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G13D in NSCLC; per usual algorithm`

**Current value:**
```
KRAS G13D in NSCLC — ні схвалений KRASi; ICI-based терапія per usual algorithm.
```

**EN excerpt:**
```
KRAS G13D in NSCLC — no approved KRASi; ICI-based therapy per usual algorithm.
```

**UA excerpt:**
```
KRAS G13D in NSCLC — ні схвалений KRASi; ICI-based терапія per usual algorithm.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 186/200: f-0188 - CRITICAL

**Entity:** `BMA-KRAS-G13X-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_g13x_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS G13 (any non-G13C) in mCRC — extended-RAS WT criterion fails; anti-EGFR`

**Current value:**
```
KRAS G13 (any non-G13C) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.
```

**EN excerpt:**
```
KRAS G13 (any non-G13C) in mCRC — extended-RAS WT criterion fails; anti-EGFR (cetuximab/panitumumab) contraindicated. Standard chemo ± bevacizumab.

```

**UA excerpt:**
```
KRAS G13 (any non-G13C) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 187/200: f-0189 - CRITICAL

**Entity:** `BMA-KRAS-Q61-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_q61_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS Q61 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR`

**Current value:**
```
KRAS Q61 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.
```

**EN excerpt:**
```
KRAS Q61 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (cetuximab/panitumumab) contraindicated. Standard chemo ± bevacizumab.

```

**UA excerpt:**
```
KRAS Q61 (any) in mCRC — extended-RAS WT criterion fails; anti-EGFR (цетуксимаб/панітумумаб) протипоказаний. стандарт chemo ± бевацизумаб.

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 188/200: f-0190 - CRITICAL

**Entity:** `BMA-KRAS-Q61-MELANOMA`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_q61_melanoma.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `NRAS Q61 is more; KRAS Q61 cells extrapolated`

**Current value:**
```
KRAS Q61 (рідкісний in меланома; NRAS Q61 is more поширений) — MEKi монотерапія modest activity (біниметиніб in NRAS-mut меланома NEMO дослідження; KRAS Q61 cells extrapolated).
```

**EN excerpt:**
```
KRAS Q61 (rare in melanoma; NRAS Q61 is more common) — MEKi monotherapy modest activity (binimetinib in NRAS-mut melanoma NEMO trial; KRAS Q61 cells extrapolated).

```

**UA excerpt:**
```
KRAS Q61 (рідкісний in меланома; NRAS Q61 is more поширений) — MEKi монотерапія modest activity (біниметиніб in NRAS-mut меланома NEMO дослідження; KRAS Q61 cells extrapolated).

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 189/200: f-0191 - CRITICAL

**Entity:** `BMA-KRAS-Q61-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_q61_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS Q61 in NSCLC`

**Current value:**
```
KRAS Q61 in NSCLC — ні схвалений таргетна терапія.
```

**EN excerpt:**
```
KRAS Q61 in NSCLC — no approved targeted therapy.
```

**UA excerpt:**
```
KRAS Q61 in NSCLC — ні схвалений таргетна терапія.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 190/200: f-0192 - CRITICAL

**Entity:** `BMA-KRAS-Q61-PDAC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_kras_q61_pdac.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `KRAS Q61 in PDAC`

**Current value:**
```
KRAS Q61 in PDAC (рідкісний vs G12) — ні схвалений drug; chemo + клінічне дослідження.
```

**EN excerpt:**
```
KRAS Q61 in PDAC (rare vs G12) — no approved drug; chemo + clinical trial.
```

**UA excerpt:**
```
KRAS Q61 in PDAC (рідкісний vs G12) — ні схвалений drug; chemo + клінічне дослідження.
```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 191/200: f-0193 - CRITICAL

**Entity:** `BMA-MET-AMP-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in gastric / GEJ adenocarcinoma (~5%): preclinical rationale strong but; trials of rilotumumab (anti-HGF; RILOMET-1) and onartuzumab (anti-MET; METGastric) were negative; MET-TKI activity in MET-amp gastric is reported in case series and basket cohorts
`

**Current value:**
```
MET ампліфікація in gastric / GEJ adenocarcinoma (~5%): preclinical rationale strong but фаза 3 trials of rilotumumab (anti-HGF; RILOMET-1) and onartuzumab (anti-MET; METGastric) were negative. селективний MET-TKI activity in MET-amp gastric is reported in case series and basket cohorts; ні regulatory схвалення.
```

**EN excerpt:**
```
MET amplification in gastric / GEJ adenocarcinoma (~5%): preclinical rationale strong but phase 3 trials of rilotumumab (anti-HGF; RILOMET-1) and onartuzumab (anti-MET; METGastric)...

```

**UA excerpt:**
```
MET ампліфікація in gastric / GEJ adenocarcinoma (~5%): preclinical rationale strong but фаза 3 trials of rilotumumab (anti-HGF; RILOMET-1) and onartuzumab (anti-MET; METGastric) were negative. селективний MET-TKI activit...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 192/200: f-0194 - CRITICAL

**Entity:** `BMA-MET-AMP-HCC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_hcc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in HCC has biological rationale (HGF/MET autocrine loop in subset of HCC). Tivantinib (MET-high IHC) failed; in HCC; activity in baskets has been modest
`

**Current value:**
```
MET ампліфікація / гіперекспресія in HCC has biological rationale (HGF/MET autocrine loop in subset of HCC). Tivantinib (MET-high IHC) failed фаза 3 (METIV-HCC, Rimassa 2018). ні схвалений MET-таргетна терапія in HCC; activity in baskets has been modest.
```

**EN excerpt:**
```
MET amplification / overexpression in HCC has biological rationale (HGF/MET autocrine loop in subset of HCC). Tivantinib (MET-high IHC) failed phase 3 (METIV-HCC, Rimassa 2018). No...

```

**UA excerpt:**
```
MET ампліфікація / гіперекспресія in HCC has biological rationale (HGF/MET autocrine loop in subset of HCC). Tivantinib (MET-high IHC) failed фаза 3 (METIV-HCC, Rimassa 2018). ні схвалений MET-таргетна терапія in HCC; act...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 193/200: f-0195 - CRITICAL

**Entity:** `BMA-MET-AMP-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `activity in high-amp cohort of GEOMETRY mono-1 (ORR ~29-40% at GCN; FDA drug for MET-amp alone — actionability is expansion-cohort / off-label; Also a key resistance mechanism to EGFR-TKIs (post-
`

**Current value:**
```
High-level MET ампліфікація in NSCLC: капматиніб activity in high-amp cohort of GEOMETRY mono-1 (ORR ~29-40% at GCN ≥10). ні схвалений FDA drug for MET-amp alone — actionability is expansion-cohort / off-label / дослідження. Also a key resistance mechanism to EGFR-TKIs (post-осимертиніб MET-amp → дослідження enrollment for амівантамаб + лазертиніб MARIPOSA-2 / SAVANNAH).
```

**EN excerpt:**
```
High-level MET amplification in NSCLC: capmatinib activity in high-amp cohort of GEOMETRY mono-1 (ORR ~29-40% at GCN ≥10). No FDA-approved drug for MET-amp alone — actionability is...

```

**UA excerpt:**
```
High-level MET ампліфікація in NSCLC: капматиніб activity in high-amp cohort of GEOMETRY mono-1 (ORR ~29-40% at GCN ≥10). ні схвалений FDA drug for MET-amp alone — actionability is expansion-cohort / off-label / досліджен...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 194/200: f-0196 - CRITICAL

**Entity:** `BMA-MET-AMP-RCC-PAPILLARY`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_met_amp_rcc_papillary.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `MET-driven papillary type-1 RCC; in MET-driven pRCC (PAPMET / SWOG-1500, Pal 2021 — PFS; mo in MET-driven cohort; MET-TKI) showed activity in MET-driven papillary RCC (SAVOIR; closed early for futility vs; but signal in MET-driven subset
`

**Current value:**
```
MET-driven papillary type-1 RCC: кабозантиніб перевершує сунитиніб in MET-driven pRCC (PAPMET / SWOG-1500, Pal 2021 — PFS 9.0 проти 5.6 mo in MET-driven cohort). саволітиніб (селективний MET-TKI) showed activity in MET-driven papillary RCC (SAVOIR фаза 3 closed early for futility vs сунитиніб but signal in MET-driven subset).
```

**EN excerpt:**
```
MET-driven papillary type-1 RCC: cabozantinib superior to sunitinib in MET-driven pRCC (PAPMET / SWOG-1500, Pal 2021 — PFS 9.0 vs 5.6 mo in MET-driven cohort). Savolitinib (selectiv...

```

**UA excerpt:**
```
MET-driven papillary type-1 RCC: кабозантиніб перевершує сунитиніб in MET-driven pRCC (PAPMET / SWOG-1500, Pal 2021 — PFS 9.0 проти 5.6 mo in MET-driven cohort). саволітиніб (селективний MET-TKI) showed activity in MET-dr...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 195/200: f-0197 - CRITICAL

**Entity:** `BMA-MET-EX14-NSCLC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_met_ex14_nsclc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `MET exon 14 skipping in; NSCLC (~3-4% of adenocarcinoma; GEOMETRY mono-1, Wolf 2020 — ORR 68% 1L / 41% prior-tx) and; VISION, Paik 2020 — ORR 46% liquid + tissue) are; MET-TKIs with FDA; has activity but is
`

**Current value:**
```
MET exon 14 skipping in поширений NSCLC (~3-4% of adenocarcinoma): капматиніб (GEOMETRY mono-1, Wolf 2020 — ORR 68% 1L / 41% prior-tx) and тепотиніб (VISION, Paik 2020 — ORR 46% liquid + tissue) are селективний MET-TKIs with FDA схвалення. кризотиніб has activity but is поступається; селективний інгібітори переважний.
```

**EN excerpt:**
```
MET exon 14 skipping in advanced NSCLC (~3-4% of adenocarcinoma): capmatinib (GEOMETRY mono-1, Wolf 2020 — ORR 68% 1L / 41% prior-tx) and tepotinib (VISION, Paik 2020 — ORR 46% liqu...

```

**UA excerpt:**
```
MET exon 14 skipping in поширений NSCLC (~3-4% of adenocarcinoma): капматиніб (GEOMETRY mono-1, Wolf 2020 — ORR 68% 1L / 41% prior-tx) and тепотиніб (VISION, Paik 2020 — ORR 46% liquid + tissue) are селективний MET-TKIs w...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 196/200: f-0198 - CRITICAL

**Entity:** `BMA-MGMT-METHYLATION-GBM`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mgmt_methylation_gbm.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `is the strongest validated predictor of temozolomide; Stupp NEJM 2005 / 2009 long-term — methylated patients derive ~2x OS; from RT+TMZ vs RT alone; L for newly-diagnosed GBM remains Stupp protocol (concurrent RT + temozolomide; TMZ) per SRC-NCCN-CNS-2025, SRC-EANO-GBM-2024 — but; status drives intensification decisions: in; MGMT-methylated patients, hypofractionated RT + TMZ (Perry NEJM 2017) is; MGMT-unmethylated patients can receive RT alone with much smaller TMZ
`

**Current value:**
```
MGMT promoter метилювання in IDH-WT гліобластома is the strongest validated predictor of temozolomide виграш (Stupp NEJM 2005 / 2009 long-term — methylated patients derive ~2x OS виграш from RT+TMZ vs RT alone). стандарт 1L for newly-diagnosed GBM remains Stupp protocol (concurrent RT + temozolomide → 6 цикли ад'ювантний TMZ) per SRC-NCCN-CNS-2025, SRC-EANO-GBM-2024 — but метилювання status drives intensification decisions: in літнього віку MGMT-methylated patients, hypofractionated RT + TMZ (Perry NEJM 2017) is переважний, while літнього віку MGMT-unmethylated patients can receive RT alone with much smaller TMZ виграш. CeTeG/NOA-09 (Herrlinger Lancet 2019) showed lomustine + TMZ + RT may extend OS in newly-diagnosed MGMT- methylated GBM but is not стандарт worldwide.
```

**EN excerpt:**
```
MGMT promoter methylation in IDH-WT glioblastoma is the strongest validated predictor of temozolomide benefit (Stupp NEJM 2005 / 2009 long-term — methylated patients derive ~2x OS b...

```

**UA excerpt:**
```
MGMT promoter метилювання in IDH-WT гліобластома is the strongest validated predictor of temozolomide виграш (Stupp NEJM 2005 / 2009 long-term — methylated patients derive ~2x OS виграш from RT+TMZ vs RT alone). стандарт...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 197/200: f-0199 - CRITICAL

**Entity:** `BMA-MLH1-GERMLINE-CRC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_germline_crc.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in crc produces dMMR/MSI-H; MSI-H ICI eligibility; per KEYNOTE-158, dostarlimab per GARNET) supersedes; specific lines via tissue-agnostic FDA; mo vs chemo; ICI in stage III dMMR CRC under investigation; deferral of; FU appropriate in stage II dMMR (chemoinsensitive; dostarlimab in dMMR rectal
`

**Current value:**
```
MLH1 герміногенний втрата функції in crc produces dMMR/MSI-H фенотип. Pan-пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FDA схвалення. 1L mCRC: пембролізумаб монотерапія (KEYNOTE-177) — mPFS 16.5 проти 8.2 mo vs chemo. ад'ювантний ICI in stage III dMMR CRC under investigation; deferral of ад'ювантний 5-FU appropriate in stage II dMMR (chemoinsensitive). неоад'ювантний dostarlimab in dMMR rectal рак → 100% cCR (Cercek 2022).
```

**EN excerpt:**
```
MLH1 germline loss-of-function in crc produces dMMR/MSI-H phenotype. Pan-tumor MSI-H ICI eligibility (pembrolizumab per KEYNOTE-158, dostarlimab per GARNET) supersedes tumor-specifi...

```

**UA excerpt:**
```
MLH1 герміногенний втрата функції in crc produces dMMR/MSI-H фенотип. Pan-пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FDA схв...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 198/200: f-0200 - CRITICAL

**Entity:** `BMA-MLH1-GERMLINE-ENDOMETRIAL`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_germline_endometrial.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in endometrial produces dMMR/MSI-H; MSI-H ICI eligibility; per KEYNOTE-158, dostarlimab per GARNET) supersedes; specific lines via tissue-agnostic FDA; dMMR endometrial: dostarlimab + carbo; L (RUBY) and; NRG-GY018) doubled PFS. Dostarlimab
`

**Current value:**
```
MLH1 герміногенний втрата функції in endometrial produces dMMR/MSI-H фенотип. Pan-пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FDA схвалення. поширений/рецидивний dMMR endometrial: dostarlimab + carbo/паклітаксел 1L (RUBY) and пембролізумаб + carbo/паклітаксел (NRG-GY018) doubled PFS. Dostarlimab/пембролізумаб монотерапія in 2L+. ад'ювантний ICI in ранньої стадії dMMR under дослідження.
```

**EN excerpt:**
```
MLH1 germline loss-of-function in endometrial produces dMMR/MSI-H phenotype. Pan-tumor MSI-H ICI eligibility (pembrolizumab per KEYNOTE-158, dostarlimab per GARNET) supersedes tumor...

```

**UA excerpt:**
```
MLH1 герміногенний втрата функції in endometrial produces dMMR/MSI-H фенотип. Pan-пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 199/200: f-0201 - CRITICAL

**Entity:** `BMA-MLH1-GERMLINE-GASTRIC`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_germline_gastric.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in gastric produces dMMR/MSI-H; MSI-H ICI eligibility; per KEYNOTE-158, dostarlimab per GARNET) supersedes; specific lines via tissue-agnostic FDA; L MSI-H gastric; chemo (CheckMate-649) and; chemo (KEYNOTE-859) show enhanced; in MSI-H subgroup
`

**Current value:**
```
MLH1 герміногенний втрата функції in gastric produces dMMR/MSI-H фенотип. Pan- пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FDA схвалення. 1L MSI-H gastric: ніволумаб + chemo (CheckMate-649) and пембролізумаб + chemo (KEYNOTE-859) show enhanced виграш in MSI-H subgroup. трастузумаб+pembro+chemo in HER2+ MSI-H (KEYNOTE-811).
```

**EN excerpt:**
```
MLH1 germline loss-of-function in gastric produces dMMR/MSI-H phenotype. Pan- tumor MSI-H ICI eligibility (pembrolizumab per KEYNOTE-158, dostarlimab per GARNET) supersedes tumor-sp...

```

**UA excerpt:**
```
MLH1 герміногенний втрата функції in gastric produces dMMR/MSI-H фенотип. Pan- пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FD...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---

## 200/200: f-0202 - CRITICAL

**Entity:** `BMA-MLH1-GERMLINE-OVARIAN`
**File:** `knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_germline_ovarian.yaml`
**Field:** `evidence_summary_ua`
**Category:** untranslated_fragment
**Matched pattern:** `in ovarian produces dMMR/MSI-H; MSI-H ICI eligibility; per KEYNOTE-158, dostarlimab per GARNET) supersedes; specific lines via tissue-agnostic FDA; tissue-agnostic applies in pretreated setting
`

**Current value:**
```
MLH1 герміногенний втрата функції in ovarian produces dMMR/MSI-H фенотип. Pan- пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FDA схвалення. MSI-H is рідкісний (~3%) in EOC; пембролізумаб tissue-agnostic applies in pretreated setting.
```

**EN excerpt:**
```
MLH1 germline loss-of-function in ovarian produces dMMR/MSI-H phenotype. Pan- tumor MSI-H ICI eligibility (pembrolizumab per KEYNOTE-158, dostarlimab per GARNET) supersedes tumor-sp...

```

**UA excerpt:**
```
MLH1 герміногенний втрата функції in ovarian produces dMMR/MSI-H фенотип. Pan- пухлина MSI-H ICI eligibility (пембролізумаб per KEYNOTE-158, dostarlimab per GARNET) supersedes пухлина-specific lines via tissue-agnostic FD...

```

**Contributor suggestion:**
```
Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.

```

**Notes:** Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.


**Maintainer action:**
- [ ] applied (edited the field with appropriate rewording)
- [ ] dismissed (false positive / not actually a violation)
- [ ] needs-discussion (escalate)

---
