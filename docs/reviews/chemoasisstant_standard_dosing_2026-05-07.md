# chemoASISSTANT v3.2.2 — Standard Dosing Extraction

**Date collected:** 2026-05-07  
**Source app:** chemoASISSTANT v3.2.2 by D.Iskimohy  
**Method:** Manual GUI extraction — "стандартне дозування" field read for each protocol  
**Total protocols found:** 112  
**Purpose:** Dose Review Aid reference data for OpenOnco KB

> Notes:
> - Doses are per-protocol defaults shown in the app without patient data entry.
> - AUC values are for carboplatin (Calvert formula applied at runtime).
> - Loading/maintenance doses shown as loading(maintenance), e.g. 8(6) mg/kg.
> - Three protocols (#59, #72, #75) have no standard preset in the app (monotherapy with weight-based input only).
> - All doses are mg/m² unless otherwise noted.

---

## Protocols #1–36 (Latin-named, A–R)

| # | Protocol name (app label) | Standard dosing |
|---|---|---|
| 1 | ABVD | doxorubicin 25 mg/m² d1, bleomycin 10,000 IU/m² d1, vinblastine 6 mg/m² d1, dacarbazine 375 mg/m² d1 |
| 2 | AC | doxorubicin 60 mg/m² d1, cyclophosphamide 600 mg/m² d1 |
| 3 | AIM | doxorubicin 25 mg/m² d1-3, ifosfamide 2500 mg/m² d1-4, mesna 500 mg/m² TID d1-4 |
| 4 | BEP_5D | cisplatin 20 mg/m² d1-5, etoposide 100 mg/m² d1-5, bleomycin 30,000 IU d1,d8,d15 |
| 5 | CAP | doxorubicin 50 mg/m² d1, cyclophosphamide 500 mg/m² d1, cisplatin 50 mg/m² d1 |
| 6 | CAPOX/XELOX | oxaliplatin 130 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |
| 7 | CAPOX/XELOX+bevacizumab | bevacizumab 7.5 mg/kg d1, oxaliplatin 130 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |
| 8 | CEOP | cyclophosphamide 750 mg/m² d1, etoposide 50 mg/m² d1 + 100 mg/m² d2-3, vincristine 1.4 mg/m² d1, prednisolone 100 mg d1-5 |
| 9 | CHOP | doxorubicin 50 mg/m² d1, cyclophosphamide 750 mg/m² d1, vincristine 1.4 mg/m² d1, prednisolone 100 mg d1-5 |
| 10 | CMF_IV | cyclophosphamide 600 mg/m² d1,8; methotrexate 40 mg/m² d1,8; fluorouracil 600 mg/m² d1,8 |
| 11 | CyBorD | cyclophosphamide 300 mg/m² d1,8,15,22; bortezomib 1.5 mg/m² d1,8,15,22; dexamethasone 40 mg d1,8,15,22 |
| 12 | CYVADIC (18-59y) | cyclophosphamide 500/1200 mg/m² d1; vincristine 1.5 mg/m² (max 2 mg) d1; doxorubicin 50 mg/m² d1; dacarbazine 250 mg/m² d1-5 |
| 13 | DA-EPOCH | etoposide 50 mg/m²/d d1-4, prednisolone 60 mg/m² BID d1-5, vincristine 0.4 mg/m²/d d1-4, cyclophosphamide 750 mg/m² d5, doxorubicin 10 mg/m²/d d1-4 |
| 14 | DA-R-EPOCH | rituximab 375 mg/m² d1 + DA-EPOCH (etoposide 50 mg/m²/d d1-4, prednisolone 60 mg/m² BID d1-5, vincristine 0.4 mg/m²/d d1-4, cyclophosphamide 750 mg/m² d5, doxorubicin 10 mg/m²/d d1-4) |
| 15 | ddAC | doxorubicin 60 mg/m² d1, cyclophosphamide 600 mg/m² d1, filgrastim 5 mcg/kg d3-7 |
| 16 | ddMVAC | methotrexate 30 mg/m² d1, vinblastine 3 mg/m² d1, doxorubicin 30 mg/m² d1, cisplatin 70 mg/m² d1 |
| 17 | DHAP | dexamethasone 40 mg d1-4, cytarabine 2000 mg/m² BID d2, cisplatin 100 mg/m² d1 |
| 18 | escBEACOPP | bleomycin 10,000 IU/m² d8, etoposide 200 mg/m² d1-3, doxorubicin 35 mg/m² d1, cyclophosphamide 1250 mg/m² d1, vincristine 1.4 mg/m² d8, procarbazine 100 mg/m² d1-7, prednisolone 40 mg/m² d1-14 |
| 19 | FLOT | docetaxel 50 mg/m² d1, oxaliplatin 85 mg/m² d1, leucovorin 200 mg/m² d1, fluorouracil 2600 mg/m² d1, filgrastim 5 mcg/kg d4-8 |
| 20 | FOLFIRI | irinotecan 180 mg/m² d1, leucovorin 400 mg/m² d1, fluorouracil bolus 400 mg/m² d1, fluorouracil 46h infusion 2400 mg/m² d1 |
| 21 | FOLFIRI+panitumumab | panitumumab 6 mg/kg d1 + FOLFIRI (irinotecan 180 mg/m² d1, leucovorin 400 mg/m² d1, fluorouracil bolus 400 mg/m² d1, fluorouracil 2400 mg/m² d1) |
| 22 | FOLFIRINOX | oxaliplatin 85 mg/m² d1, irinotecan 180 mg/m² d1, leucovorin 400 mg/m² d1, fluorouracil bolus 400 mg/m² d1, fluorouracil 46h infusion 2400 mg/m² d1 |
| 23 | GemOx | gemcitabine 1000 mg/m² d1, oxaliplatin 100 mg/m² d1 |
| 24 | iGEV | ifosfamide 2000 mg/m² d1-4, mesna 400 mg/m² TID d1-4, gemcitabine 800 mg/m² d1+d4, vinorelbine 20 mg/m² d1, prednisolone 100 mg d1-4 |
| 25 | ICE | ifosfamide 5000 mg/m² d2, etoposide 100 mg/m² d1-3, carboplatin AUC5 d1, mesna 5000 mg/m² d2 + 3000 mg/m² d3 |
| 26 | mFOLFIRINOX | oxaliplatin 85 mg/m² d1, irinotecan 150 mg/m² d1, leucovorin 400 mg/m² d1, fluorouracil 2400 mg/m² 46h infusion d1 (no bolus) |
| 27 | mFOLFOX | oxaliplatin 85 mg/m² d1, leucovorin 400 mg/m² d1, fluorouracil bolus 400 mg/m² d1, fluorouracil 46h infusion 2400 mg/m² d1 |
| 28 | mFOLFOX+bevacizumab | bevacizumab 5 mg/kg d1 + mFOLFOX |
| 29 | mFOLFOX+cetuximab | cetuximab 500 mg/m² d1 + mFOLFOX |
| 30 | mFOLFOX+panitumumab | panitumumab 6 mg/kg d1 + mFOLFOX |
| 31 | mini-CHOP | cyclophosphamide 400 mg/m² d1, doxorubicin 25 mg/m² d1, vincristine 1 mg (flat) d1, prednisolone 40 mg/m² d1-5 |
| 32 | PCV | lomustine 110 mg/m² d1, vincristine 1.4 mg/m² d8+d29, procarbazine 60 mg/m² d8-21 |
| 33 | R-CEOP | rituximab 375 mg/m² d1, cyclophosphamide 750 mg/m² d1, etoposide 50 mg/m² d1 + 100 mg/m² d2-3, vincristine 1.4 mg/m² d1, prednisolone 100 mg d1-5 |
| 34 | R-CHOP | rituximab 375 mg/m² d1, cyclophosphamide 750 mg/m² d1, doxorubicin 50 mg/m² d1, vincristine 1.4 mg/m² d1, prednisolone 100 mg d1-5 |
| 35 | R-CVP | rituximab 375 mg/m² d1, cyclophosphamide 750 mg/m² d1, vincristine 1.4 mg/m² d1, prednisolone 40 mg/m² d1-5 |
| 36 | R-DHAP | rituximab 375 mg/m² d1, dexamethasone 40 mg d1-4, cytarabine 2000 mg/m² BID d2, cisplatin 100 mg/m² d1 |

---

## Protocols #37–46 (Latin-named, R–X continued)

| # | Protocol name (app label) | Standard dosing |
|---|---|---|
| 37 | R-GDP | rituximab 375 mg/m² d1, gemcitabine 1000 mg/m² d1,d8, dexamethasone 40 mg d1-4, cisplatin 75 mg/m² d1 |
| 38 | R-GemOx | rituximab 375 mg/m² d1, gemcitabine 1000 mg/m² d1, oxaliplatin 100 mg/m² d1 |
| 39 | R-ICE | rituximab 375 mg/m² d1, ifosfamide 5000 mg/m² d2, etoposide 100 mg/m² d1-3, carboplatin AUC5 d1, mesna 5000 mg/m² d2 + 3000 mg/m² d3 |
| 40 | R-mini-CHOP | rituximab 375 mg/m² d1, cyclophosphamide 400 mg/m² d1, doxorubicin 25 mg/m² d1, vincristine 1 mg d1, prednisolone 40 mg/m² d1-5 |
| 41 | ТС | docetaxel 75 mg/m² d1, cyclophosphamide 600 mg/m² d1 |
| 42 | ТІР | paclitaxel 250 mg/m² d1 (24h infusion), ifosfamide 1500 mg/m² d2-5, mesna 500 mg/m² TID d2-5, cisplatin 25 mg/m² d2-5 |
| 43 | VAC | vincristine 2 mg/m² d1, doxorubicin 75 mg/m² d1, cyclophosphamide 1200 mg/m² d1, mesna 240 mg/m² TID d1 |
| 44 | VIP | etoposide 75 mg/m² d1-5, ifosfamide 1200 mg/m² d1-5, cisplatin 20 mg/m² d1-5, mesna 400 mg/m² TID d1-5 |
| 45 | XELIRI | irinotecan 250 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |
| 46 | XELIRI+bevacizumab | bevacizumab 7.5 mg/kg d1, irinotecan 250 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |

---

## Protocols #47–84 (Ukrainian-named, В–П)

| # | Protocol name (app label) | Standard dosing |
|---|---|---|
| 47 | вінорельбін | vinorelbine 25 mg/m² d1; or 20-35 mg/m² d1,8; or 25-30 mg/m² d1,8,15 |
| 48 | гемцитабін | gemcitabine 1000 mg/m² d1,8,15 (28-day) or d1,8 (21-day) |
| 49 | гемцитабін/вінорельбін | gemcitabine 1000 mg/m² d1,8, vinorelbine 25 mg/m² d1,8 |
| 50 | гемцитабін/доцетаксел | gemcitabine 900 mg/m² d1,8, docetaxel 75 mg/m² d8 |
| 51 | гемцитабін/капецитабін | gemcitabine 1000 mg/m² d1,8, capecitabine 1000 mg/m² BID d1-14 (21-day cycle) |
| 52 | гемцитабін/карбоплатин | gemcitabine 1000 mg/m² d1,8, carboplatin AUC5 d1 |
| 53 | гемцитабін/паклітаксел | gemcitabine 3000 mg/m² d1, paclitaxel 150 mg/m² d1 |
| 54 | гемцитабін/цисплатин | gemcitabine 1000 mg/m² d1,8, cisplatin 70 mg/m² d1 or 35 mg/m² d1,8 |
| 55 | дакарбазин | dacarbazine 250 mg/m² d1-5 or 1000 mg/m² d1 |
| 56 | доксорубіцин | doxorubicin 60 mg/m² d1 (21-day) or 20 mg/m² d1,8,15 (weekly) |
| 57 | доксорубіцин/іфосфамід | doxorubicin 25 mg/m² IV bolus d1-3, ifosfamide 3000 mg/m² 24h infusion d1-3, mesna 3000 mg/m² 24h infusion d1-3 |
| 58 | доксорубіцин/цисплатин | doxorubicin 45-75 mg/m² d1, cisplatin 40-100 mg/m² d1 (21-day cycle) |
| 59 | доцетаксел | *no standard preset in app — weight-based input required* |
| 60 | доцетаксел/карбоплатин | docetaxel 75 mg/m² d1, carboplatin AUC6 d1 |
| 61 | доцетаксел/преднізолон | docetaxel 75 mg/m² d1, prednisolone 5 mg BID d1-21 |
| 62 | доцетаксел/цисплатин | docetaxel 75 mg/m² d1, cisplatin 75 mg/m² d1 |
| 63 | доцетаксел/цисплатин/фторурацил | docetaxel 75 mg/m² d1, cisplatin 100 mg/m² d1, fluorouracil 1000 mg/m²/day d1-4 |
| 64 | епірубіцин/циклофосфамід | epirubicin 75-100 mg/m² d1, cyclophosphamide 600-930 mg/m² d1 |
| 65 | іринотекан | irinotecan 150-180 mg/m² d1 (14-day); or 250-350 mg/m² d1 (21-day); or 125 mg/m² d1,8 (21-day) |
| 66 | іринотекан/панітумумаб | panitumumab 6 mg/kg d1, irinotecan 180 mg/m² d1 |
| 67 | іринотекан/темозоломід | 2×5/21: temozolomide 100 mg/m² d1-5, irinotecan 10-20 mg/m² d1-5+d8-12; 1×5/21: temozolomide 100 mg/m² d1-5, irinotecan 20-50 mg/m² d1-5 |
| 68 | іфосфамід | ifosfamide 3000 mg/m²/day d1-3, mesna 1000 mg/m² TID d1-3 |
| 69 | іфосфамід/етопозид | ifosfamide 1800 mg/m² d1-5, mesna 360 mg/m² TID d1-5, etoposide 100 mg/m² d1-5 |
| 70 | кабазитаксел/преднізолон | cabazitaxel 25 mg/m² d1, prednisolone 10 mg d1-21 |
| 71 | капецитабін/доцетаксел | capecitabine 950 mg/m² BID d1-14, docetaxel 75 mg/m² d1 |
| 72 | карбоплатин (монорежим) | *no standard preset in app — AUC-based input required* |
| 73 | карбоплатин/етопозид | carboplatin AUC5 d1, etoposide 100 mg/m² d1-3 |
| 74 | карбоплатин/етопозид/атезолізумаб | atezolizumab 1200 mg d1, carboplatin AUC5 d1, etoposide 100 mg/m² d1-3 |
| 75 | паклітаксел (монорежим) | *no standard preset in app — weight-based input required* |
| 76 | паклітаксел/карбоплатин | paclitaxel 175-200 mg/m² d1, carboplatin AUC5-6 d1 |
| 77 | паклітаксел/цисплатин | paclitaxel 135/175-200 mg/m² d1, cisplatin 75/50-75 mg/m² d1 |
| 78 | паклітаксел/цисплатин/бевацизумаб | bevacizumab 15 mg/kg d1, paclitaxel 175 mg/m² d1, cisplatin 50 mg/m² d1 |
| 79 | паклітаксел/цисплатин/фторурацил | paclitaxel 175 mg/m² d1, cisplatin 100 mg/m² d2, fluorouracil 500 mg/m²/day d2-6 |
| 80 | пембролізумаб/паклітаксел/карбоплатин | pembrolizumab 200 mg d1, paclitaxel 200 mg/m² d1, carboplatin AUC6 d1 |
| 81 | пембролізумаб/пеметрексед | pembrolizumab 200 mg d1, pemetrexed 500 mg/m² d1 |
| 82 | пембролізумаб/пеметрексед/карбоплатин | pembrolizumab 200 mg d1, pemetrexed 500 mg/m² d1, carboplatin AUC5 d1 |
| 83 | пеметрексед | pemetrexed 500 mg/m² d1 |
| 84 | пеметрексед/карбоплатин | pemetrexed 500 mg/m² d1, carboplatin AUC6 d1 |

---

## Protocols #85–112 (Ukrainian-named, П–Ц continued)

| # | Protocol name (app label) | Standard dosing |
|---|---|---|
| 85 | пеметрексед/карбоплатин/бевацизумаб | bevacizumab 15 mg/kg d1, pemetrexed 500 mg/m² d1, carboplatin AUC5 d1 |
| 86 | пеметрексед/цисплатин | pemetrexed 500 mg/m² d1, cisplatin 75 mg/m² d1 |
| 87 | пеметрексед/цисплатин/бевацизумаб | pemetrexed 500 mg/m² d1, cisplatin 75 mg/m² d1, bevacizumab 7.5 mg/kg d1 |
| 88 | пертузумаб/трастузумаб/доцетаксель/карбоплатин | pertuzumab 840(420) mg d1, trastuzumab 8(6) mg/kg d1, docetaxel 75 mg/m² d1, carboplatin AUC6 d1 |
| 89 | помалідомід/циклофосфамід/дексаметазон | pomalidomide 4 mg 1×/day d1-21, cyclophosphamide 400 mg d1,d8,d15, dexamethasone 40 mg d1,d8,d15,d22 (28-day cycle) |
| 90 | ритуксимаб | rituximab 375 mg/m² d1 |
| 91 | ритуксимаб/бендамустин | rituximab 375 mg/m² d1, bendamustine 90 mg/m² d1-2 (28-day cycle) |
| 92 | ритуксимаб/леналідомід | Variant 1 (28-day): rituximab 375 mg/m² d1,8,15,22 (cycle 1), d1 (cycles 2-12); lenalidomide 10 mg/day d9-28 (cycle 1), d1-28 (cycles 2+). Variant 2 (28-day): rituximab 375 mg/m² IV d1,8,15,22 + 25 mg intrathecal d1,8,15,22 (cycle 1), d1,15 (cycle 2+); lenalidomide 15 mg/day d1-21 |
| 93 | ритуксимаб/темозоломід | rituximab 750 mg/m² d1,d8,d15,d22, temozolomide 100-200 mg/m² d1-7,d15-21 (28-day cycle) |
| 94 | темозоломід | 5/28: 150-200 mg/m² d1-5; 21/28: 75 mg/m² d1-21; 28/28: 50 mg/m² d1-5 |
| 95 | топотекан | topotecan 1.5 mg/m² d1-5 |
| 96 | топотекан/цисплатин | topotecan 0.75 mg/m² d1-3, cisplatin 50 mg/m² d1 |
| 97 | трастузумаб | trastuzumab 8(6) mg/kg d1 (21-day) or 4(2) mg/kg d1 (weekly) |
| 98 | трастузумаб/вінорельбін | Weekly: vinorelbine 25 mg/m² d1, trastuzumab 4(2) mg/kg d1. Or 21-day: vinorelbine 25 mg/m² d1,d8,d15, trastuzumab 8(6) mg/kg d1. Or 21-day: vinorelbine 20-35 mg/m² d1,d8, trastuzumab 8(6) mg/kg d1 |
| 99 | трастузумаб/доцетаксель | trastuzumab 8(6) mg/kg d1, docetaxel 75 mg/m² d1 |
| 100 | трастузумаб/доцетаксель/карбоплатин | trastuzumab 8(6) mg/kg d1, docetaxel 75 mg/m² d1, carboplatin AUC6 d1 |
| 101 | трастузумаб/оксаліплатин/капецитабін (T-CAPOX/XELOX) | trastuzumab 8(6) mg/kg d1, oxaliplatin 130 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |
| 102 | трастузумаб/паклітаксель | trastuzumab 8(6)/4(2) mg/kg d1, paclitaxel 175(80) mg/m² d1 (21-day/weekly) |
| 103 | трастузумаб/паклітаксель/карбоплатин | trastuzumab 8(6) mg/kg d1, paclitaxel 175 mg/m² d1, carboplatin AUC6 d1 |
| 104 | фторурацил/лейковорин | leucovorin (calcium folinate) 400 mg/m² d1, fluorouracil bolus 400 mg/m² d1, fluorouracil 46h infusion 2400 mg/m² d1 |
| 105 | цисплатин | cisplatin 80 mg/m² d1 |
| 106 | цисплатин/вінорельбін | cisplatin 80 mg/m² d1, vinorelbine 25 mg/m² d1,d8 |
| 107 | цисплатин/етопозид | cisplatin 75 mg/m² d1, etoposide 100 mg/m² d1-3 |
| 108 | цисплатин/іринотекан | 21-day: cisplatin 30 mg/m² d1,8, irinotecan 65 mg/m² d1,8; 28-day: cisplatin 60 mg/m² d1, irinotecan 60 mg/m² d1,8,15 |
| 109 | цисплатин/капецитабін | cisplatin 80 mg/m² d1, capecitabine 1000 mg/m² BID d1-14 |
| 110 | цисплатин/лейковорин/фторурацил | cisplatin 50 mg/m² d1, leucovorin 200 mg/m² d1, fluorouracil 24h infusion 2000 mg/m² d1 |
| 111 | цисплатин/фторурацил | cisplatin 100 mg/m² d1, fluorouracil 1000 mg/m²/day d1-4 |
| 112 | цисплатин/циклофосфамід | cisplatin 75 mg/m² d1, cyclophosphamide 750 mg/m² d1 |

---

## Summary statistics

- **Total protocols:** 112
- **Latin-named (A-X):** 46 (protocols #1-46)
- **Ukrainian-named (В-Ц):** 66 (protocols #47-112)
- **Monotherapy agents with no standard preset:** 3 (доцетаксел, карбоплатин монорежим, паклітаксел монорежим)
- **Combination regimens with standard preset:** 109
- **Targeted/immunotherapy agents present:** bevacizumab, cetuximab, panitumumab, rituximab, pertuzumab, trastuzumab, pembrolizumab, atezolizumab, lenalidomide, pomalidomide, bortezomib

## Coverage notes for OpenOnco KB

The following protocols overlap with or extend OpenOnco KB regimens and should be cross-checked during Dose Review Aid implementation:

- FOLFOX variants (mFOLFOX, mFOLFOX+bev/cet/pani) — align with FOLFOX4/6 in NCCN
- FOLFIRINOX / mFOLFIRINOX — standard vs modified (irinotecan 150 vs 180 mg/m²)
- Gemcitabine combinations (GemOx, gem/carbo, gem/cis, gem/nab-pac) — check AUC
- Pemetrexed regimens — confirm folic acid/B12 premedication note not in dosing
- Trastuzumab pertuzumab combos — loading vs maintenance doses correctly split
- Temozolomide — three schedules (5/28, 21/28, 28/28) with different dose densities
- Rituximab/lenalidomide — two distinct variant regimens (one intrathecal component)
