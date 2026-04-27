# Clinical questions — 2026-04-27 batch

Compiled for hematologist clinical co-lead review. Each item is a yes/no/
clarify question raised while authoring the recent KB additions
(Plans A/B/C, Round 1A B-cell, Round 1B T/NK, Round 1C myeloid+MM+HL,
Round 2 etiology). Format per item:

- **Q** — what to decide
- **Default** — what KB ships today + brief why
- **Affects** — entity IDs the answer would update
- **From** — batch / commit ref

All affected entities still hold `reviewer_signoffs: 0` and need two of
three Co-Leads under CHARTER §6.1. Grouped by disease; cross-cutting +
schema/engine questions at the bottom.

---

## DLBCL

**Q1. HCV+ very-low burden, CP-A — DAA-first vs chemo-first?**
- Default: chemo-first (R-CHOP / Pola-R-CHP) immediate; DAA concurrent or after induction. Algo notes flag this as unsettled.
- Affects: ALGO-DLBCL-1L, IND-DLBCL-1L-RCHOP, IND-DLBCL-1L-POLA-R-CHP. From: Round 2 (2d6a737).

**Q2. HIV+ DLBCL — make DA-EPOCH-R a first-class indication?**
- Default: rationale-layer note only (DA-EPOCH-R preferred per AMC 034 / Sparano 2010); engine still routes HIV+ to R-CHOP / Pola-R-CHP. Blocked on missing BIO-HIV-STATUS.
- Affects: ALGO-DLBCL-1L; new IND-DLBCL-1L-DAEPOCHR-HIV. From: Round 2.

## Burkitt

**Q3. R-ICE vs R-DHAP as 2L default?**
- Default: R-ICE (CORAL-equivalent, UA institutional familiarity); R-DHAP only if ifosfamide-intolerant.
- Affects: ALGO-BURKITT-2L, IND-BURKITT-2L-RICE-ASCT, IND-BURKITT-2L-RDHAP-ASCT. From: Plan A (82abb38).

**Q4. HIV+ Burkitt — CODOX-M/IVAC threshold?**
- Default: DA-EPOCH-R for HIV+ Burkitt (CALGB 10002 / AMC 048); CODOX-M/IVAC reserved for "HIV+ AND CD4 <100" OR CNS+/leukemic/LDH>3×ULN/bulky abdomen. Confirm.
- Affects: ALGO-BURKITT-1L, IND-BURKITT-1L-DAEPOCHR, IND-BURKITT-1L-CODOXM-IVAC. From: Round 2 (646c8f3).

**Q5. Burkitt 2L palliative routing — dedicated IND or MDT free-text?**
- Default: MDT note "BSC + clinical trial" for transplant-ineligible (frail / organ-dysfunction / infection-screening).
- Affects: ALGO-BURKITT-2L step 1. From: Plan A.

## CLL

**Q6. Hypogammaglobulinemia — IVIG threshold + BTKi/venetoclax interruption?**
- Default: IgG/recurrent-infection thresholds + treatment-interruption rules not formalized; RF-CLL-INFECTION-SCREENING fires on screening side only.
- Affects: RF-CLL-INFECTION-SCREENING, IND-CLL-1L-BTKI, IND-CLL-1L-VENO, IND-CLL-2L-VENR-MURANO. From: Plan A (CLL hypogamma backfill).

## MCL

**Q7. R-maintenance after BTKi-R 1L — none?**
- Default: no R-maintenance added on top of continuous BTKi-R; maintenance applies only after autoSCT (LyMa) or BR / R-CHOP older track. Confirm.
- Affects: IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE, ALGO-MCL-1L. From: Round 1A (0e8a745).

**Q8. MRD-driven early stop of R-maintenance?**
- Default: full LyMa schedule (3 yr post-autoSCT); MRD-guided early stop noted only as `do_not_do` discussion item.
- Affects: IND-MCL-POST-INDUCTION-RITUXIMAB-MAINTENANCE. From: Round 1A.

## FL

**Q9. PRIMA maintenance — full 2 yr in sustained MRD-neg CR?**
- Default: full 2 yr; no early-stop rule.
- Affects: IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE. From: Round 1A (60f9414).

## SMZL / NMZL

**Q10. BR vs ibrutinib as preferred 2L?**
- Default: BR for fit / high-burden, ibrutinib for elderly / frail or post-BR relapse. Ibrutinib not modeled (UA access ≈zero).
- Affects: IND-SMZL-2L-BR, IND-NMZL-2L-BR, ALGO-SMZL-2L, ALGO-NMZL-2L. From: Round 1A (7874e6f, d15163).

**Q11. SMZL/NMZL HCV+ gate — RNA detectable + categorical?**
- Default: gate on BIO-HCV-RNA detectable (actionable per EASL 2023) + BIO-HCV-STATUS categorical. Anti-HCV antibody alone insufficient (persists for life).
- Affects: IND-SMZL-1L-HCV-POSITIVE, IND-NMZL-1L-HCV-POSITIVE, ALGO-SMZL-1L. From: Plan B + Round 2 (3d390eb).

## HCV-MZL

**Q12. Sequential DAA→observe→BR vs concurrent DAA+BR — burden threshold?**
- Default: sequential per ESMO MZL 2024 (~70% avoid chemo); concurrent for high-burden / aggressive / transformation-suspect (IND-HCV-MZL-1L-BR-AGGRESSIVE).
- Affects: IND-HCV-MZL-POST-DAA-SURVEILLANCE, IND-HCV-MZL-1L-BR-AGGRESSIVE, ALGO-HCV-MZL-1L, ALGO-HCV-MZL-2L. From: Round 1A + Round 2.

**Q13. Post-DAA observation window — 6 vs 12 months before escalating?**
- Default: reassess 3, 6, 12 months; no >12 months without imaging response. Within-window escalation MDT-driven.
- Affects: IND-HCV-MZL-POST-DAA-SURVEILLANCE, ALGO-HCV-MZL-2L. From: Round 1A (1b5f2b1).

## HCL

**Q14. Vemurafenib mono vs vemurafenib+rituximab (Tiacci 2021) — combo always?**
- Default: combo preferred per NCCN; surfaced as MDT note ("add rituximab × 8 wk per Tiacci protocol") because dedicated V+R indication not yet modeled.
- Affects: IND-HCL-2L-VEMURAFENIB, ALGO-HCL-2L. From: Round 1A (9625cc6, 68afab9).

**Q15. UA access fallback — cladribine retreatment vs pentostatin vs R+cladribine?**
- Default: vemurafenib+R when funded; cladribine+R when blocked. HCL-variant (BRAF-WT) → R+bendamustine OR R+cladribine, not modeled.
- Affects: IND-HCL-2L-VEMURAFENIB, ALGO-HCL-2L step 3. From: Round 1A.

## NLPBL

**Q16. Mandatory re-biopsy gate — `stop=true` vs precautionary R-CHOP?**
- Default: `stop=true` on missing biopsy; transformation suspected → R-CHOP precautionary; indolent confirmed → R-mono retreatment ± ISRT (free-text, not modeled).
- Affects: ALGO-NLPBL-2L step 1, IND-NLPBL-2L-RCHOP-TRANSFORMATION; new IND-NLPBL-2L-RITUXIMAB-RETREATMENT. From: Round 1A (32d0db9, 08cbfec).

**Q17. R-CHOP vs Pola-R-CHP for transformed NLPBL (THRLBCL)?**
- Default: R-CHOP per NCCN; POLARIX upgrade not modeled at NLPBL line.
- Affects: IND-NLPBL-2L-RCHOP-TRANSFORMATION. From: Round 1A.

## PCNSL

**Q18. R-MPV salvage vs ibrutinib for r/r — split confirm?**
- Default: MTX-responsive late relapse → R-MPV salvage + thiotepa-autoSCT; MTX-refractory / early relapse → ibrutinib mono 560 mg PO daily (iLOC Soussain 2019). Ibrutinib free-text only.
- Affects: ALGO-PCNSL-2L steps 2&3, IND-PCNSL-2L-RMPV-SALVAGE; new IND-PCNSL-2L-IBRUTINIB. From: Round 1A (a5cb830, 4bbcd0a).

**Q19. PCNSL elderly frail — WBRT vs ibrutinib vs len-R vs BSC?**
- Default: placeholder routing + MDT note "WBRT palliative / BSC alternative"; lenalidomide ± rituximab (REAL trial) not modeled.
- Affects: ALGO-PCNSL-2L step 1. From: Round 1A.

**Q20. Thiotepa autoSCT consolidation — TBC vs BCNU+thiotepa?**
- Default: surfaced as MDT note (IELSG32 / Illerhaus); no dedicated IND-PCNSL-2L-AUTOSCT-CONSOLIDATION.
- Affects: ALGO-PCNSL-2L, IND-PCNSL-2L-RMPV-SALVAGE. From: Round 1A.

## PMBCL

**Q21. Pembrolizumab as standalone 2L indication?**
- Default: R-ICE+autoSCT placeholder both routes; pembro (KEYNOTE-170, ORR 45%) surfaced as MDT note for transplant-ineligible / R-ICE-refractory.
- Affects: ALGO-PMBCL-2L, IND-PMBCL-2L-RICE-AUTOSCT; new IND-PMBCL-2L-PEMBROLIZUMAB. From: Round 1A (90ed13e, 0efdc63).

**Q22. Transplant-ineligible — pembro-first vs CAR-T (axi-cel ZUMA-12)?**
- Default: pembro per KEYNOTE-170; CAR-T not modeled for PMBCL.
- Affects: ALGO-PMBCL-2L. From: Round 1A.

## HGBL-DH

**Q23. Late-relapse (≥12 mo) chemosensitive — CAR-T vs salvage+autoSCT?**
- Default: CAR-T for early-relapse / primary-refractory; salvage R-ICE/R-DHAP → BEAM-autoSCT for late chemosensitive (free-text, no IND).
- Affects: ALGO-HGBL-DH-2L, IND-HGBL-DH-2L-CART-AXICEL; new IND-HGBL-DH-2L-RICE-AUTOSCT. From: Round 1A (161a479, 4d0a113).

**Q24. 12-mo early/late split transferred from DLBCL — appropriate for HGBL-DH?**
- Default: 12-month threshold from ZUMA-7 / TRANSFORM transferred biologically. HGBL-DH typically relapses earlier — should we shorten?
- Affects: ALGO-HGBL-DH-2L step 2/3. From: Round 1A.

## CHL

**Q25. HIV+ — A+AVD or ABVD by default?**
- Default: "ABVD or A+AVD acceptable at full dose with concurrent ART; avoid BEACOPP". Indication selection unchanged (ECHELON-1 underrepresented HIV+).
- Affects: ALGO-CHL-1L, IND-CHL-1L-ABVD, IND-CHL-1L-A-AVD. From: Round 2 (81c1f9c).

**Q26. HBsAg+ on ABVD-without-BV — entecavir mandatory or monitor?**
- Default: entecavir still recommended per NCCN; CI-HBV-NO-PROPHYLAXIS extended to BV+dara contexts; monitor-only acceptable in anti-HBc+ alone.
- Affects: CI-HBV-NO-PROPHYLAXIS, IND-CHL-1L-ABVD, IND-CHL-1L-A-AVD. From: Round 2.

## NK/T-nasal

**Q27. PD-1 selection r/r — pembro vs avelumab vs sintilimab?**
- Default: "Pembrolizumab when accessible (broadest); avelumab or sintilimab if pembro unavailable; all off-label in UA".
- Affects: IND-NK-T-NASAL-2L-AVELUMAB, ALGO-NK-T-NASAL-2L. From: Round 1B (6f11c75).

**Q28. EBV-DNA cutoff for high-risk — ≥10⁴ copies/mL?**
- Default: ≥10⁴ copies/mL OR persistent post-induction (Wang Blood 2012 / Kim JCO 2018) via RF-NK-T-NASAL-INFECTION-SCREENING. Confirm.
- Affects: ALGO-NK-T-NASAL-1L, RF-NK-T-NASAL-INFECTION-SCREENING; future BIO-EBV-DNA. From: Round 2 (6fac0db, f5782b2).

**Q29. SMILE vs P-GEMOX — SMILE default for fit ≤70?**
- Default: SMILE default (strongest RCT); P-GEMOX for older / renal / asparaginase supply concerns.
- Affects: ALGO-NK-T-NASAL-1L, IND-NK-T-NASAL-1L-SMILE, IND-NK-T-NASAL-1L-P-GEMOX. From: Round 1B.

## ATLL

**Q30. Mogamulizumab pre-alloSCT wash-out — 50 vs 90 days?**
- Default: minimum 50 days (FDA black box); extend to 90 if disease control permits.
- Affects: IND-ATLL-2L-MOGAMULIZUMAB, ALGO-ATLL-2L. From: Round 1B (12490e6).

**Q31. HTLV-1 quantitative proviral load as biomarker?**
- Default: serology + PCR mandatory at diagnosis; quantitative proviral load not wired (BIO-HTLV-1 missing).
- Affects: ALGO-ATLL-1L; new BIO-HTLV-1. From: Round 2 (f734721).

**Q32. Mogamulizumab vs lenalidomide for r/r ATLL — moga first?**
- Default: "moga first-line salvage; lenalidomide when moga inaccessible or in indolent disease".
- Affects: IND-ATLL-2L-MOGAMULIZUMAB. From: Round 1B.

## AITL

**Q33. Azacitidine vs HDACi (belinostat / romidepsin) as AITL 2L+ first?**
- Default: 5-aza first in UA (access + AITL-specific RUYUAN-2 / Lemonnier data + TET2/IDH2/DNMT3A rationale); ≥6 cycles before declaring failure.
- Affects: IND-AITL-2L-AZACITIDINE, IND-AITL-2L-BELINOSTAT, IND-AITL-2L-ROMIDEPSIN. From: Round 1B (d90b536).

**Q34. AITL allo-SCT 3L framing — realistic default or MDT referral only?**
- Default: "AlloSCT in fit responders" in `followed_by` blocks across PTCL; not modeled as standalone IND.
- Affects: IND-AITL-2L-* set, ALGO-PTCL-2L. From: Round 1B.

## ALCL

**Q35. BV maintenance × 16 cycles post-ASCT — extrapolation from cHL (AETHERA) acceptable?**
- Default: maintenance for ALCL ALK- with high-risk features post-ASCT; surveillance acceptable for ALK+ standard-risk in CR1 post-ASCT.
- Affects: IND-ALCL-MAINTENANCE-BV-POST-ASCT, ALGO-ALCL-2L. From: Round 1B (7bb101d).

**Q36. ALCL DUSP22-rearranged — modify maintenance/SCT recommendation?**
- Default: DUSP22 (favorable ALK- subset) not modeled as biomarker gate.
- Affects: RF-ALCL-HIGH-RISK-BIOLOGY, IND-ALCL-MAINTENANCE-BV-POST-ASCT. From: Plan A.

## T-PLL

**Q37. Venetoclax mono vs ven+alemtuzumab for r/r T-PLL?**
- Default: combo preferred when both accessible (Hampel 2020); ven mono acceptable when alemtuzumab inaccessible.
- Affects: IND-T-PLL-2L-VENETOCLAX-ALEMTUZUMAB, ALGO-T-PLL-2L. From: Round 1B (689a724).

## HSTCL

**Q38. CHOEP-unfit fallback framing — palliative-only?**
- Default: "CHOEP for elderly/unfit; ICE/IVAC if patient could convert to transplant-eligible". Cure ≈zero without alloSCT; do_not_do says "do not promise curative intent".
- Affects: IND-HSTCL-1L-CHOEP-UNFIT, IND-HSTCL-1L-ICE-ALLOSCT, ALGO-HSTCL-1L. From: Round 1B (9cc4ebd).

## EATL

**Q39. ICE vs DHAP vs GemOx for salvage?**
- Default: ICE for fit ≤65; GemOx/GDP for older or renal-impaired.
- Affects: IND-EATL-2L-ICE. From: Round 1B (b3df826).

## T-ALL / T-LBL

**Q40. Nelarabine vs FLAG-IDA / clofarabine as 2L salvage?**
- Default: nelarabine first when accessible; FLAG-IDA / clofarabine when unavailable or neurologic comorbidity (nelarabine neurotoxicity may be irreversible).
- Affects: IND-T-ALL-2L-NELARABINE, ALGO-T-ALL-2L. From: Round 1B (c975a54).

## PTLD

**Q41. PTLD-1 maintenance — 4 q3w consolidation vs extended q2-mo × 2 yr?**
- Default: PTLD-1 standard 4 q3w; extend q2-mo × up to 2 yr only in high-risk responders with persistent EBV viral load.
- Affects: IND-PTLD-MAINTENANCE-RITUXIMAB, ALGO-PTLD-2L. From: Round 1B (2c0ece3).

**Q42. EBV-negative B-PTLD — escalation threshold to R-CHOP?**
- Default: reduce-IS + rituximab attempt; MDT re-evaluation at 4 weeks if no response. Confirm cutoff.
- Affects: ALGO-PTLD-1L step 3, IND-PTLD-1L-REDUCE-IS, IND-PTLD-1L-RCHOP. From: Round 2 (8d934bf, 4dd91be).

## MF / Sézary

**Q43. Bexarotene supply — when does MTX replace as 2L?**
- Default: bexarotene first-line systemic 2L when accessible; MTX 5-25 mg/wk PO when bexarotene inaccessible (UA international supply only).
- Affects: IND-MF-ADVANCED-2L-BEXAROTENE, IND-MF-MAINTENANCE-RETINOID, ALGO-MF-SEZARY-2L. From: Round 1B (725d862).

**Q44. MF→ATLL reclassification on unexpected HTLV-1 detection — auto or MDT?**
- Default: not wired; surfaced as open re-classification rule.
- Affects: DIS-MF-SEZARY, DIS-ATLL, ALGO-ATLL-1L. From: Plan A.

## WM

**Q45. Bing-Neel — dedicated CNS-penetrating BTKi indication needed?**
- Default: standard WM 2L BTKi indications; no Bing-Neel-specific route (zanubrutinib / ibrutinib + HD-MTX add-on).
- Affects: IND-WM-1L-BTKI, IND-WM-2L-ZANUBRUTINIB. From: Plan A.

## ET

**Q46. Peg-IFN as dedicated 2L (pregnancy / younger JAK2+)?**
- Default: anagrelide default 2L; peg-IFN MDT free-text only via RF-PV-ET-PREGNANCY-OR-PLANNING.
- Affects: ALGO-ET-2L, IND-ET-2L-ANAGRELIDE; new IND-ET-2L-PEG-IFN. From: Round 1C (5ac2dda, 742cf4e).

## APL

**Q47. ATRA+ATO+IDA vs classic AIDA for high-risk?**
- Default: ATRA+ATO+IDA when ATO available (UA: yes, reimbursed); AIDA only on ATO contraindication.
- Affects: IND-APL-1L-ATRA-ATO-IDA, IND-APL-1L-ATRA-ATO. From: Round 1C.

**Q48. APL maintenance debate — needed after modern ATO regimens?**
- Default: not formalized; flagged in commit messages. Modern APL0406-era low/intermediate-risk may not need ATRA+6-MP+MTX maintenance.
- Affects: IND-APL-1L-ATRA-ATO, IND-APL-1L-ATRA-ATO-IDA; future IND-APL-MAINTENANCE. From: Round 1C.

## AML

**Q49. Oral aza (Onureg) — bridge-to-transplant off-label use?**
- Default: maintenance only for non-HCT pathway; HCT-eligible patients proceed direct to transplant once donor secured (per QUAZAR enrollment).
- Affects: IND-AML-CR1-ORAL-AZA-MAINTENANCE. From: Round 1C (8462f42).

## B-ALL

**Q50. POMP duration — sex-specific (2 yr women, 3 yr men) per CALGB 10403?**
- Default: sex-specific per CALGB 10403; shorter if toxicity-limiting.
- Affects: IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE. From: Round 1C (ad9bb5d).

**Q51. Ph+ B-ALL on POMP — which TKI on top?**
- Default: "continued TKI per institutional protocol"; no preferred TKI in maintenance.
- Affects: IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE, IND-B-ALL-1L-PH-POS. From: Round 1C.

## MM

**Q52. PI-doublet (bortezomib+len) maintenance for high-risk cytogenetics?**
- Default: lenalidomide alone for standard-risk; bortezomib+len doublet considered for high-risk + clinical trial / access feasibility.
- Affects: IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE; future IND-MM-POST-ASCT-VR-MAINTENANCE. From: Round 1C.

## MDS-HR

**Q53. Decitabine vs azacitidine parity — interchangeable?**
- Default: aza modeled (IND-MDS-HR-1L-AZA, IND-MDS-HR-1L-VEN-AZA); decitabine not modeled separately (AZA-001 OS data favors aza).
- Affects: IND-MDS-HR-1L-AZA, ALGO-MDS-HR-1L; future IND-MDS-HR-1L-DECITABINE. From: Round 1C.

## HCC

**Q54. HBV+ HCC — tenofovir vs entecavir during atezo+bev?**
- Default: "entecavir or tenofovir prophylaxis" (interchangeable in algo notes); not formalized.
- Affects: ALGO-HCC-SYSTEMIC-1L, IND-HCC-SYSTEMIC-1L-ATEZO-BEV. From: Round 2 (adc4bd7, 9f1ae45).

**Q55. HCV+ HCC — DAA timing vs atezo+bev start (defer 2-4 wk?)?**
- Default: "DAA before/concurrent with atezo+bev when feasible (CP-A); defer atezo+bev 2-4 wk if rapid HCV clearance feasible AND tumor not aggressive". Sofosbuvir+amiodarone forbidden.
- Affects: ALGO-HCC-SYSTEMIC-1L, IND-HCC-SYSTEMIC-1L-ATEZO-BEV. From: Round 2.

## Cervical

**Q56. Transformation-progression RF — waiver from 5-type matrix?**
- Default: RF-CERVICAL-TRANSFORMATION-PROGRESSION ships; solid-tumor "transformation" semantics differ from lymphoma.
- Affects: RF-CERVICAL-TRANSFORMATION-PROGRESSION; tests/test_redflag_quality_gates.py baseline. From: Plan A (f8c543e).

---

## Cross-cutting

**Q57. HBV occult-positive (anti-HBc+ alone) — universal entecavir or monitor-only?**
- Default: entecavir mandatory in HBsAg+; in anti-HBc+ alone, "still recommended" but optional in some indications. CI-HBV-NO-PROPHYLAXIS extended in CHL — generalize across all anti-CD20 / BV / dara contexts?
- Affects: CI-HBV-NO-PROPHYLAXIS, all CD20+ indications + CHL (BV) + MM (dara). From: Round 2 (81c1f9c).

**Q58. Two-reviewer signoff backlog — batch process?**
- Default: every entity in this batch ships `reviewer_signoffs: 0` + STUB note. ~60 entities awaiting Co-Lead signoff per CHARTER §6.1.
- Affects: every IND/ALGO touched in this batch. From: Plan A + every Round.

**Q59. Histologic transformation — auto-route to ALGO-DLBCL vs surface only?**
- Default: placeholder routing within source algo + MDT note; cross-disease auto-routing not implemented (SMZL, NMZL, HCV-MZL, FL, NLPBL).
- Affects: ALGO-SMZL-2L, ALGO-NMZL-2L, ALGO-HCV-MZL-2L, ALGO-FL-1L, ALGO-NLPBL-2L; engine routing layer. From: Round 1A.

**Q60. Aspirin VTE prophylaxis on lenalidomide maintenance — confirm standard?**
- Default: aspirin standard; no LMWH escalation unless prior VTE.
- Affects: IND-MM-POST-ASCT-LENALIDOMIDE-MAINTENANCE + IMiD-bearing indications. From: Round 1C.

---

## Schema / engine

**Q61. Promote etiology biomarkers to first-class — BIO-HIV-STATUS, BIO-HBV-STATUS, BIO-EBV-DNA, BIO-HTLV-1?**
- Default: flagged in 5+ algo `notes` blocks (DLBCL, Burkitt, CHL, NK/T-nasal, ATLL); HCV side already wired (BIO-HCV-RNA + BIO-HCV-STATUS).
- Affects: new BIO-* entities + biomarker_requirements wiring across ~15 indications. From: Plan B + Round 2.

**Q62. NLPBL `do_not_do` with `stop=true` — engine support?**
- Default: ALGO-NLPBL-2L step 1 uses `stop=true`; if engine doesn't support, trace must escalate as hard blocking precondition.
- Affects: ALGO-NLPBL-2L step 1; engine decision_tree handling. From: Round 1A (32d0db9).

**Q63. Cross-algo `route_to:` primitive — MDS-HR→AML, NLPBL→DLBCL, indolent→aggressive?**
- Default: all such routings are MDT free-text notes today.
- Affects: ALGO-MDS-HR-2L, ALGO-NLPBL-2L, ALGO-SMZL-2L, ALGO-NMZL-2L, ALGO-HCV-MZL-2L, ALGO-FL-1L; engine schema. From: Plan A + Round 1A.

**Q64. Maintenance entities use `line_of_therapy: 1` — confirm convention?**
- Default: lenalidomide post-ASCT, oral aza, POMP, FL/MCL R-maintenance all use `line_of_therapy: 1` ("1L pathway continuation"); PTLD maintenance uses `line_of_therapy: 2`.
- Affects: all maintenance indications; engine activation logic. From: Round 1A + 1C.

---

*~60 questions. Reply by Q-number; I will then update referenced
entities and stamp `reviewer_signoffs` per CHARTER §6.1.*
