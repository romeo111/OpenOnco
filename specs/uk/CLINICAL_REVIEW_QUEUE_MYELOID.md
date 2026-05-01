# Черга клінічного review — Myeloid expansion (heme)

**Кому:** клінічному рецензенту OpenOnco (онколог-гематолог зі спеціалізацією
на мієлоїдних новоутвореннях).
**Контекст:** 2026-04-25 додано вертикаль на 7 мієлоїдних діагнозів
(AML, APL, CML, MDS-LR, MDS-HR, PV, ET, PMF). Усі сутності позначені
як `STUB — requires clinical co-lead signoff before publication`. CHARTER §6.1
вимагає двох рецензентів-клініцистів для публікації будь-якої сутності
у `knowledge_base/hosted/content/`.

**Файли:** Усі під `knowledge_base/hosted/content/{diseases,redflags,
indications,regimens,algorithms,drugs,sources}/` з префіксами
`aml_/apl_/cml_/mds_/pv_/et_/pmf_/_pv_et_/`. Sources-теж нові: SRC-ELN-AML-2022,
SRC-ELN-APL-2019, SRC-ELN-CML-2020, SRC-ESMO-AML-2020, SRC-ESMO-CML-2017,
SRC-ESMO-MPN-2015, SRC-ESMO-MDS-2021, SRC-IPSS-M-BERNARD-2022,
SRC-DIPSS-PLUS-GANGAT-2011, SRC-VIALE-A-DINARDO-2020, SRC-RATIFY-STONE-2017,
SRC-APL0406-LOCOCO-2013, SRC-IRIS-OBRIEN-2003, SRC-RESPONSE-VANNUCCHI-2015,
SRC-COMFORT-I-VERSTOVSEK-2012, SRC-COMMANDS-FENAUX-2020.

---

## TL;DR — пріоритет рецензування

1. **Block A — APL emergency / time-critical positioning** (2-4 години).
   APL — це єдиний "molecularly-defined emergency" archetype у KB.
   Питання: чи правильно ми оформили `time_critical: true` на
   IND-APL-1L-* + чи коректне формулювання в notes щодо CHARTER
   §15.2 C2 (initial ATRA initiation поза non-device CDS carve-out).

2. **Block B — AML + MDS-HR ven+aza off-label** (1-2 години).
   Ven+aza у MDS-HR — off-label екстраполяція з VIALE-A AML;
   оформлено як IND-MDS-HR-1L-VEN-AZA з NCCN category 2A. Питання:
   чи ця opt-in alternative має залишитися як-є, чи її прибрати
   до результатів VERONA?

3. **Block C — TKI selection matrix для CML 1L** (3-5 годин).
   У REG-2GEN-TKI-CML об'єднано dasatinib / nilotinib / bosutinib
   як один Indication-mapped option з comorbidity-matrix у notes.
   Питання: чи треба розщепити на 3 окремі регімени з власними
   indications, чи поточна compactна форма прийнятна?

4. **Block D — IPSS-R vs IPSS-M default for MDS** (1-2 години).
   IPSS-M (Bernard 2022) reclassifies ~46% патієнтів. Чи переключити
   default risk-score на IPSS-M тепер, чи зачекати ширшого впровадження
   у Україні?

5. **Block E — Ukraine access annotations** (2-3 години).
   Багато новіших препаратів (luspatercept, momelotinib, fedratinib,
   bosutinib, ponatinib, asciminib, midostaurin) НЕ зареєстровані /
   НЕ reimbursed в Україні. Перевірити, чи актуальні дані про
   reimbursement у regulatory_status.ukraine_registration та
   ukraine_availability.

---

## Block A — APL time-critical / emergency positioning

| Сутність | Файл | Питання |
|---------|------|---------|
| DIS-APL | diseases/apl.yaml | Чи правильно класифікувати як `archetype: molecularly_defined_emergency`? Це новий archetype у KB. |
| RF-APL-EMERGENCY-DIC | redflags/rf_apl_emergency_dic.yaml | Trigger: fibrinogen <150, D-dimer elevated, plt <50, active_bleeding, dic_active. Чи комплектний? |
| RF-APL-TRANSFORMATION-PROGRESSION (differentiation syndrome) | redflags/rf_apl_transformation_progression.yaml | Trigger: fever + new dyspnea + weight gain. Чи cutoff weight_gain ≥5 kg правильний? Renamed from RF-APL-DIFFERENTIATION-SYNDROME to satisfy 5-type matrix coverage. |
| RF-APL-HIGH-RISK-BIOLOGY | redflags/rf_apl_high_risk_biology.yaml | Sanz cutoff WBC >10. Чи intermediate-risk (plt ≤40 + WBC ≤10) у нас правильно мапиться на standard-track? |
| IND-APL-1L-ATRA-ATO | indications/ind_apl_1l_atra_ato.yaml | `time_critical: true`. ATRA initiation на bedside поза scope; чи notes коректно описують це? |
| IND-APL-1L-ATRA-ATO-IDA | indications/ind_apl_1l_atra_ato_ida.yaml | `time_critical: true`. Cumulative anthracycline tracking — як саме у render? |

---

## Block B — Off-label / emerging therapy selection

| Сутність | Файл | Питання |
|---------|------|---------|
| IND-MDS-HR-1L-VEN-AZA | indications/ind_mds_hr_1l_ven_aza.yaml | Off-label MDS-HR. Залишити як alternative track чи прибрати до VERONA? |
| RF-AML-FLT3-ACTIONABLE | redflags/rf_aml_flt3_actionable.yaml | Midostaurin not Ukraine-reimbursed. Чи є практична альтернатива (gilteritinib теж не reimbursed)? |
| REG-VEN-AZA-AML | regimens/ven_aza_aml.yaml | Venetoclax не reimbursed в Україні. Чи зробити annotation у render про access? |

---

## Block C — CML TKI selection bundle

| Сутність | Файл | Питання |
|---------|------|---------|
| REG-2GEN-TKI-CML | regimens/dasatinib_or_nilotinib_cml.yaml | Bundled dasatinib/nilotinib/bosutinib з comorbidity matrix у notes. Розщепити чи компактно? |
| RF-CML-ORGAN-DYSFUNCTION | redflags/rf_cml_organ_dysfunction.yaml | Direction "investigate" — surfaces TKI-comorbidity matching annotation. Чи це правильна semantics? |
| RF-CML-T315I-MUTATION | redflags/rf_cml_t315i_mutation.yaml | Ponatinib + asciminib NOT in Ukraine. AlloHCT — реалістична альтернатива для T315I в нашому context? |

---

## Block D — Risk-score scoring system selection

| Сутність | Файл | Питання |
|---------|------|---------|
| RF-MDS-HIGH-RISK-IPSS | redflags/rf_mds_high_risk_ipss.yaml | Тригер обоих IPSS-R AND IPSS-M. Чи зробити IPSS-M primary тепер? |
| DIS-MDS-LR / DIS-MDS-HR | diseases/mds_lr.yaml, mds_hr.yaml | Risk cutoff IPSS-R ≤3.5 vs >4.5 — int (3.5-4.5) переважно куди треба класифікувати? |
| RF-PMF-HIGH-RISK-DIPSS | redflags/rf_pmf_high_risk_dipss.yaml | DIPSS-Plus vs MIPSS70. Чи чекати MIPSS70-plus v2.0 широкого впровадження? |
| RF-CML-HIGH-RISK-ELTS | redflags/rf_cml_high_risk_elts.yaml | ELTS перевага над Sokal — підтверджено. Чи дроп Sokal зі scoring? |

---

## Block E — Ukraine access / reimbursement audit

Перевірити НСЗУ-list (станом на 2026-Q2) на:
- DRUG-VENETOCLAX (не reimbursed; підтвердити)
- DRUG-MIDOSTAURIN (не reimbursed)
- DRUG-LUSPATERCEPT (не registered)
- DRUG-MOMELOTINIB (не registered)
- DRUG-FEDRATINIB (не registered)
- DRUG-BOSUTINIB (не registered)
- DRUG-PONATINIB (не registered)
- DRUG-RUXOLITINIB (registered, не reimbursed)
- DRUG-ANAGRELIDE (registered, не reimbursed)
- DRUG-DECITABINE (reimbursed)
- DRUG-AZACITIDINE (reimbursed)
- DRUG-IMATINIB (reimbursed; generics)
- DRUG-DASATINIB / NILOTINIB (reimbursed)
- DRUG-EPOETIN-ALFA (reimbursed)
- DRUG-HYDROXYUREA (reimbursed)
- DRUG-ATRA / DRUG-ATO / DRUG-DAUNORUBICIN / DRUG-IDARUBICIN / DRUG-CYTARABINE (reimbursed)

---

## Acceptance criteria для перекладу із STUB у published

Для кожної з 7 хвороб + супутніх RF / Indication / Regimen / Algorithm:
- [ ] Технічно: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` повертає 0 помилок (вже виконано)
- [ ] Технічно: `pytest -q` повертає 0 регресій (вже виконано)
- [ ] Клінічно: clinical co-lead проходить per-RF, per-Indication, per-Regimen перевірку
- [ ] Клінічно: ≥2 reviewer sign-offs на Indications (CHARTER §6.1)
- [ ] Контент: видалити `STUB — requires clinical co-lead signoff before publication` з `notes`
- [ ] Контент: оновити `last_reviewed` на дату клінічного review + `reviewers` зі справжніми ID

---

## Estimate сумарно

~30-50 годин клінічного review (5 блоків × 4-10 годин кожен).
Найвищий ROI — Block A (APL emergency framing) і Block E (Ukraine access).
