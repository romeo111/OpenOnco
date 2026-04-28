"""One-off bulk-updater for pkg2 NSZU verification (CSD-2-authoring-pkg2).

Updates `regulatory_status.ukraine_registration` per drug with:
  - registered (bool)
  - reimbursed_nszu (bool)
  - reimbursement_indications (list[str], Ukrainian)
  - last_verified ("2026-04-27")
  - notes (UA + indication-restriction summary)

Uses ruamel.yaml to preserve YAML formatting and comments.
Pass a comma-separated list of drug-keys (filename stems) as argv[1] to
process a batch; without args, processes all 52 pkg2 drugs.
"""
from __future__ import annotations

import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent
DRUGS_DIR = ROOT / "knowledge_base" / "hosted" / "content" / "drugs"

LV = "2026-04-27"

# Per-drug verification record. Order = author intent (Ukrainian wording).
# Each entry: registered, reimbursed_nszu, indications, notes
DRUGS: dict[str, dict] = {
    # ── ICIs ──────────────────────────────────────────────────────────────
    "pembrolizumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: меланома нерезектабельна/метастатична 1L (моно)",
            "Програма медичних гарантій 2026: НДРЛ PD-L1 TPS≥50% 1L (моно)",
            "Програма медичних гарантій 2026: НДРЛ 1L у комбінації з пеметрексед+платина (неплоскоклітинний)",
            "Реімбурсаційний пакет «Онкологія» 2026: cHL рецидивний/рефрактерний після BV/ауто-ТКМ",
            "Реімбурсаційний пакет «Онкологія» 2026: MSI-H/dMMR пухлини (пан-онкологічно, після прогресії на стандарт)",
        ],
        notes=(
            "Реєстрація МОЗ підтверджена; включений до НСЗУ онкопакету з суворими "
            "indication-restrictions: меланома 1L, НДРЛ PD-L1≥50% 1L, MSI-H pan-tumor, cHL R/R. "
            "Менш ймовірно покриті НСЗУ: цервікальний 2L, шлунковий 2L, уротеліальний. "
            "Джерело: nszu.gov.ua/likuvannya-zlovkisnykh-novoutvoren (2026-04)."
        ),
    ),
    "nivolumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: меланома нерезектабельна/метастатична 1L (моно або комбо з ipilimumab)",
            "Програма медичних гарантій 2026: НДРЛ 2L після платини (незалежно від PD-L1)",
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки (ccRCC) проміжний/несприятливий ризик 1L (з ipilimumab)",
            "Реімбурсаційний пакет «Онкологія» 2026: cHL R/R після ауто-ТКМ та BV",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває меланому 1L, НДРЛ 2L, RCC 1L (комбо з ipi), cHL R/R. "
            "Адьювантна меланома та СНГ — обмежено. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "atezolizumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ДРЛ-розширене стадія 1L з карбоплатин+етопозид",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ неплоскоклітинний 1L з bevacizumab+карбоплатин+пакліксел (IMpower150)",
            "Реімбурсаційний пакет «Онкологія» 2026: ТНРЗ метастатичний PD-L1+ 1L з nab-paclitaxel (обмежено)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ДРЛ ext-stage 1L, НДРЛ неплоскоклітинний 1L (комбо). "
            "ТНРЗ та HCC — частково. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "durvalumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ стадія III нерезектабельна після ХПТ (PACIFIC, консолідація)",
            "Реімбурсаційний пакет «Онкологія» 2026: ДРЛ-розширене стадія 1L з карбоплатин+етопозид",
        ],
        notes=(
            "Раніше ключ reimbursed_nszu відсутній — встановлено true з обмеженням до PACIFIC-режиму "
            "(NSCLC III nerezектабельна) та ДРЛ ext. STRIDE-режим (з tremelimumab) — без UA НСЗУ. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "ipilimumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: меланома нерезектабельна/метастатична 1L у комбінації з nivolumab",
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки проміжний/несприятливий ризик 1L з nivolumab",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває лише в комбо з nivolumab (мономеланома 2L+ — out-of-pocket). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "avelumab": dict(
        registered=False,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "BORDERLINE / FLAG: реєстрація МОЗ не підтверджена або призупинена станом на 2026-04. "
            "Раніше зареєстровано для меркель-карциноми та уротеліального раку (підтримуюча терапія "
            "1L після платини). НСЗУ не покриває. Імпорт через charity/named-patient. "
            "Потребує перевірки клінічним co-lead — можлива пере-категоризація до pkg3."
        ),
    ),

    # ── PARPi ─────────────────────────────────────────────────────────────
    "olaparib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: рак яєчників BRCA1/2-мутований, підтримуюча терапія 1L після відповіді на платину",
            "Реімбурсаційний пакет «Онкологія» 2026: рак яєчників BRCA1/2 рецидивний платиночутливий — підтримуюча терапія",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HER2- BRCA1/2-герм метастатичний (OlympiAD)",
        ],
        notes=(
            "Раніше reimbursed_nszu=false; виправлено на true для оваріального BRCA1/2 (1L maintenance "
            "та 2L+) і РМЗ BRCA1/2-герм. Простатичний mCRPC HRR (PROfound) — поза НСЗУ, переговори "
            "тривають. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "niraparib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: рак яєчників — підтримуюча терапія 1L (PRIMA, незалежно від BRCA, HRD-стратифіковано)",
            "Реімбурсаційний пакет «Онкологія» 2026: рак яєчників рецидивний платиночутливий — підтримуюча терапія",
        ],
        notes=(
            "Реєстрація МОЗ підтверджена (раніше registered=false — виправлено). НСЗУ покриває "
            "оваріальне 1L maintenance (PRIMA) та 2L+ платиночутливе. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "talazoparib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Зареєстрований у МОЗ для РМЗ HER2- BRCA-мутованого метастатичного (EMBRACA). "
            "НСЗУ не покриває станом на 2026-04 — пацієнти OOP/charity. Простатичний mCRPC HRR "
            "(TALAPRO-2) — також без UA НСЗУ. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── EGFR-TKI / NSCLC targeted ─────────────────────────────────────────
    "osimertinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ EGFR-mut (ex19del/L858R) 1L (FLAURA)",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ EGFR T790M+ 2L після прогресії на 1-/2-gen EGFR-TKI",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ EGFR-mut стадія IB-IIIA адьювантна терапія після резекції (ADAURA)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває 1L EGFR-mut НДРЛ та 2L T790M+. Адьювант (ADAURA) — частково. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "afatinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ EGFR-mut (ex19del/L858R та uncommon mutations) 1L",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває 1L EGFR-mut НДРЛ. Поступається osimertinib, але "
            "ефективний при uncommon EGFR mutations (G719X, L861Q). Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "erlotinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ EGFR-mut 1L (історично; зараз поступається osimertinib)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває для НДРЛ EGFR-mut, але клінічно витіснений osimertinib. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "gefitinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ EGFR-mut 1L (історично)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває для НДРЛ EGFR-mut. Як і erlotinib — клінічно витіснений "
            "osimertinib. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "dacomitinib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для НДРЛ EGFR-mut (раніше registered=false — виправлено). "
            "НСЗУ не покриває — частково через пере-перекриття з gefitinib/erlotinib/osimertinib. "
            "Out-of-pocket. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── ALK/ROS1 inhibitors ───────────────────────────────────────────────
    "alectinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ ALK+ 1L (ALEX)",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ ALK+ адьювант стадія IB-IIIA після резекції (ALINA)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває 1L ALK+ НДРЛ — стандарт допомоги. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "crizotinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: НДРЛ ALK+ або ROS1+ 1L (історично; зараз 2L після alectinib)",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ ROS1+ 1L (PROFILE 1001)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває для ALK+ та ROS1+ НДРЛ. У ALK+ витіснений alectinib, "
            "залишається стандартом для ROS1+. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "brigatinib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для НДРЛ ALK+ (раніше registered=false — виправлено). "
            "НСЗУ не покриває (alectinib — стандарт 1L; brigatinib як 2L+ — out-of-pocket). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "lorlatinib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для НДРЛ ALK+ 2L+ після прогресії на ≥1 ALK-TKI (раніше "
            "registered=false — виправлено). НСЗУ не покриває — out-of-pocket/charity. CROWN 1L дані "
            "поки не транслюються в UA reimbursement. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── BRAF/MEK inhibitors ───────────────────────────────────────────────
    "dabrafenib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: меланома BRAF V600 нерезектабельна/метастатична 1L з trametinib",
            "Реімбурсаційний пакет «Онкологія» 2026: меланома BRAF V600 адьювант стадія III після резекції (COMBI-AD) з trametinib",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ BRAF V600E 1L з trametinib",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває BRAF-меланому 1L (комбо з trametinib) та адьювант. "
            "НДРЛ BRAF V600E — також. Анапластичний рак щитоподібної залози — частково. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "trametinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: меланома BRAF V600 1L з dabrafenib",
            "Реімбурсаційний пакет «Онкологія» 2026: меланома BRAF V600 адьювант з dabrafenib",
            "Реімбурсаційний пакет «Онкологія» 2026: НДРЛ BRAF V600E 1L з dabrafenib",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває лише в комбо з dabrafenib (моно — не рекомендовано). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "encorafenib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Зареєстрований для меланоми BRAF V600 (з binimetinib) та КРР BRAF V600E (з cetuximab, "
            "BEACON). НСЗУ не покриває станом на 2026-04 — out-of-pocket. Меланома — переважно "
            "dabrafenib+trametinib. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── BTKi ──────────────────────────────────────────────────────────────
    "ibrutinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ХЛЛ 1L (моно або з obinutuzumab/rituximab)",
            "Реімбурсаційний пакет «Онкологія» 2026: ХЛЛ 2L+ після ХІТ",
            "Реімбурсаційний пакет «Онкологія» 2026: МКЛ R/R після ≥1 лінії",
            "Реімбурсаційний пакет «Онкологія» 2026: макроглобулінемія Вальденстрема (WM) MYD88+",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ХЛЛ 1L/2L+, МКЛ 2L+, WM. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "acalabrutinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ХЛЛ 1L (ELEVATE-TN, моно або з obinutuzumab)",
            "Реімбурсаційний пакет «Онкологія» 2026: ХЛЛ 2L+ після ХІТ або BTKi/венетоклаксу",
            "Реімбурсаційний пакет «Онкологія» 2026: МКЛ R/R (ACE-LY-004)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ХЛЛ 1L/2L+ та МКЛ 2L+. Кращий профіль кардіотоксичності "
            "ніж ibrutinib. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "zanubrutinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ХЛЛ 1L (SEQUOIA, моно)",
            "Реімбурсаційний пакет «Онкологія» 2026: МКЛ R/R",
            "Реімбурсаційний пакет «Онкологія» 2026: макроглобулінемія Вальденстрема (ASPEN)",
            "Реімбурсаційний пакет «Онкологія» 2026: маргінальна лімфома 2L+ після anti-CD20",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ХЛЛ 1L/2L+, МКЛ 2L+, WM, MZL. "
            "Найновіший з трьох ковалентних BTKi. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── BCL-2 ─────────────────────────────────────────────────────────────
    "venetoclax": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ХЛЛ 1L з obinutuzumab (CLL14, фіксована тривалість)",
            "Реімбурсаційний пакет «Онкологія» 2026: ХЛЛ 2L+ з rituximab (MURANO)",
            "Реімбурсаційний пакет «Онкологія» 2026: ГМЛ 1L у пацієнтів, непридатних до інтенсивної ХТ, з azacitidine (VIALE-A)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ХЛЛ 1L (Ven+O), 2L+ (Ven+R) та ГМЛ unfit (Ven+aza). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── CDK4/6i ───────────────────────────────────────────────────────────
    "palbociclib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: РМЗ HR+/HER2- метастатичний 1L з letrozole/іншим AI (PALOMA-2)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HR+/HER2- метастатичний 2L з fulvestrant (PALOMA-3)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває РМЗ HR+/HER2- метастатичний 1L/2L з ET. "
            "Адьювант (PALLAS — негативний) — без покриття. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "ribociclib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: РМЗ HR+/HER2- метастатичний 1L з letrozole/AI (MONALEESA-2)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HR+/HER2- метастатичний пре/перименопауза 1L з AI+OFS (MONALEESA-7)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HR+/HER2- метастатичний 2L з fulvestrant (MONALEESA-3)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває РМЗ HR+/HER2- метастатичний 1L/2L. Адьювант (NATALEE) — "
            "пілотні програми. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "abemaciclib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: РМЗ HR+/HER2- метастатичний 1L з AI (MONARCH-3)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HR+/HER2- метастатичний 2L з fulvestrant (MONARCH-2)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HR+/HER2- адьювант високого ризику з ET 2 роки (monarchE)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває РМЗ HR+/HER2- метастатичний 1L/2L та адьювант "
            "monarchE-критеріями (≥4 LN+ або 1-3 LN+ з high-risk features). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── HMA ───────────────────────────────────────────────────────────────
    "azacitidine": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: МДС високого ризику (IPSS Int-2/High) — терапія 1L",
            "Реімбурсаційний пакет «Онкологія» 2026: ГМЛ у пацієнтів, непридатних до інтенсивної ХТ, з venetoclax (VIALE-A)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває МДС-HR та ГМЛ unfit (комбо з venetoclax). ХММЛ — також. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "decitabine": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: МДС високого ризику (IPSS Int-2/High) — терапія 1L",
            "Реімбурсаційний пакет «Онкологія» 2026: ГМЛ у пацієнтів старше 65 років, непридатних до інтенсивної ХТ",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває МДС-HR та ГМЛ unfit (моно або комбо з venetoclax). "
            "Симетрично з azacitidine. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── IMiDs ─────────────────────────────────────────────────────────────
    "lenalidomide": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ММ 1L з bortezomib+dexamethasone (VRd) для не-трансплант кандидатів",
            "Програма медичних гарантій 2026: ММ підтримуюча терапія після ауто-ТКМ",
            "Реімбурсаційний пакет «Онкологія» 2026: ММ R/R з dexamethasone (Rd) або з daratumumab",
            "Реімбурсаційний пакет «Онкологія» 2026: МДС низького ризику del(5q) трансфузіє-залежний",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ММ 1L (VRd), maintenance, 2L+ (Rd, DRd) та МДС-LR del(5q). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── Anti-CD38, proteasome inhibitors ─────────────────────────────────
    "daratumumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ММ 1L у не-трансплант кандидатів з VMP/Rd (D-VMP, D-Rd)",
            "Програма медичних гарантій 2026: ММ 1L у трансплант-кандидатів з VTd (D-VTd, CASSIOPEIA)",
            "Реімбурсаційний пакет «Онкологія» 2026: ММ R/R з Rd/Vd/Pd (POLLUX, CASTOR, APOLLO)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ММ 1L (D-VMP/D-Rd/D-VTd) та R/R комбо. SC-формуляція "
            "(daratumumab+hyaluronidase) — пріоритетна. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "carfilzomib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: ММ R/R з dexamethasone (Kd) або з lenalidomide+dex (KRd, ASPIRE)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ММ R/R (KRd, Kd). 1L — без покриття (VRd залишається "
            "стандартом). Кардіотоксичність вимагає моніторингу. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "bortezomib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ММ 1L (VRd, VMP, VTd, VCd)",
            "Програма медичних гарантій 2026: МКЛ 1L з R-CHOP-подібними схемами",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ММ 1L (всі стандартні режими) та МКЛ 1L. "
            "Дженерик доступний з 2017. SC введення — пріоритет (нижчі нейропатії). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── BCR-ABL 2nd-gen ──────────────────────────────────────────────────
    "bosutinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: ХМЛ Ph+ хронічна фаза 2L+ після резистентності/непереносимості imatinib/dasatinib/nilotinib",
            "Реімбурсаційний пакет «Онкологія» 2026: ХМЛ 1L (BFORE) — обмежено",
        ],
        notes=(
            "Реєстрація МОЗ підтверджена (раніше registered=false — виправлено). НСЗУ покриває "
            "ХМЛ 2L+ і частково 1L. Уникати при T315I (потребує ponatinib/asciminib — pkg3). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── ADCs ──────────────────────────────────────────────────────────────
    "brentuximab_vedotin": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: cHL 1L стадія III/IV з AVD (A+AVD, ECHELON-1)",
            "Реімбурсаційний пакет «Онкологія» 2026: cHL R/R після ауто-ТКМ або не-кандидати",
            "Реімбурсаційний пакет «Онкологія» 2026: sALCL CD30+ 1L з CHP (ECHELON-2) або R/R",
            "Реімбурсаційний пакет «Онкологія» 2026: CD30+ MF/Sézary 2L+ після ≥1 системної терапії",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває cHL 1L (A+AVD), R/R та sALCL/CD30+ PTCL 1L (BV-CHP). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "trastuzumab_emtansine": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: РМЗ HER2+ адьювант з резидуальним захворюванням після неоадьювантної терапії (KATHERINE)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HER2+ метастатичний 2L+ після trastuzumab+таксан (EMILIA)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває РМЗ HER2+ адьювант (KATHERINE) та 2L+ метастатичний. "
            "Витісняється trastuzumab deruxtecan у 2L. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "trastuzumab_deruxtecan": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HER2+ метастатичний 2L після trastuzumab+таксан (DESTINY-Breast03)",
            "Реімбурсаційний пакет «Онкологія» 2026: РМЗ HER2-low (IHC 1+ / 2+ ISH-) метастатичний 2L+ (DESTINY-Breast04)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває РМЗ HER2+ 2L (новий стандарт замість T-DM1) і HER2-low "
            "2L+. Шлунковий HER2+ та НДРЛ HER2-mut — поза НСЗУ. ILD вимагає моніторингу. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── Anti-CD20, anti-CD19/22 ──────────────────────────────────────────
    "obinutuzumab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ХЛЛ 1L з chlorambucil або venetoclax (CLL14)",
            "Реімбурсаційний пакет «Онкологія» 2026: ФЛ 1L високого тягаря з ХТ (GALLIUM)",
            "Реімбурсаційний пакет «Онкологія» 2026: ФЛ R/R після rituximab (GADOLIN)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ХЛЛ 1L (CLL14 з venetoclax), ФЛ 1L high-burden та R/R. "
            "Менш універсально доступний ніж rituximab. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "blinatumomab": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: B-ALL Ph- R/R після індукції/реіндукції (TOWER)",
            "Реімбурсаційний пакет «Онкологія» 2026: B-ALL MRD+ після консолідації (BLAST)",
        ],
        notes=(
            "Реєстрація МОЗ підтверджена (раніше registered=false — виправлено). НСЗУ покриває "
            "B-ALL R/R та MRD+. Pediatric — також. CRS/ICANS моніторинг. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── JAK / FLT3 ────────────────────────────────────────────────────────
    "ruxolitinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: первинний мієлофіброз (PMF) проміжний-2/високий ризик (DIPSS)",
            "Програма медичних гарантій 2026: пост-ПВ/пост-ЕТ мієлофіброз",
            "Реімбурсаційний пакет «Онкологія» 2026: справжня поліцитемія (PV) резистентна/непереносна до hydroxyurea",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває MF (PMF, post-PV/ET) та PV 2L після HU. "
            "GVHD — частково. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "fedratinib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для MF проміжний-2/високий ризик (раніше registered=false "
            "— виправлено). НСЗУ не покриває — out-of-pocket. Wernicke encephalopathy — black-box. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "midostaurin": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ГМЛ FLT3-mut (ITD або TKD) 1L з 7+3 індукцією та консолідацією (RATIFY)",
            "Реімбурсаційний пакет «Онкологія» 2026: системний мастоцитоз агресивний/SM-AHN/мастоцитарний лейкоз",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває FLT3-mut ГМЛ 1L з 7+3 індукцією. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── VEGF/multikinase TKI ──────────────────────────────────────────────
    "sorafenib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Програма медичних гарантій 2026: ГЦК Child-Pugh A нерезектабельна",
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки прогресивний 2L+ (історично)",
            "Реімбурсаційний пакет «Онкологія» 2026: радіойод-рефрактерний диференційований рак щитоподібної залози",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває ГЦК, RCC 2L+, радіойод-рефрактерний DTC. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "regorafenib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: КРР метастатичний 3L+ після fluoropyrimidines/oxaliplatin/irinotecan/anti-VEGF/anti-EGFR (CORRECT)",
            "Реімбурсаційний пакет «Онкологія» 2026: ГЦК 2L після sorafenib (RESORCE)",
            "Реімбурсаційний пакет «Онкологія» 2026: GIST 3L+ після imatinib та sunitinib (GRID)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває mCRC 3L+, ГЦК 2L, GIST 3L+. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "lenvatinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: радіойод-рефрактерний DTC (SELECT)",
            "Реімбурсаційний пакет «Онкологія» 2026: ГЦК 1L Child-Pugh A (REFLECT, не-нижче sorafenib)",
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки 2L+ з everolimus або 1L з pembrolizumab (CLEAR)",
            "Реімбурсаційний пакет «Онкологія» 2026: ендометрій R/R з pembrolizumab (KEYNOTE-775)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває DTC, ГЦК, RCC, ендометрій (з pembro). "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "axitinib": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки 2L+ після sunitinib/cytokines (AXIS)",
            "Реімбурсаційний пакет «Онкологія» 2026: НКК нирки 1L з pembrolizumab (KEYNOTE-426) або з avelumab",
        ],
        notes=(
            "Реєстрація МОЗ підтверджена (раніше registered=false — виправлено). НСЗУ покриває "
            "RCC 1L (з pembro) та 2L. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "ramucirumab": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Зареєстрований для шлункового раку 2L (з paclitaxel, RAINBOW), КРР 2L (RAISE), НДРЛ 2L "
            "(REVEL), ГЦК 2L (REACH-2 з AFP≥400). НСЗУ не покриває станом на 2026-04 — out-of-pocket. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── PI3K, NTRK, androgen receptor ─────────────────────────────────────
    "alpelisib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для РМЗ HR+/HER2- PIK3CA-mut з fulvestrant (раніше "
            "registered=false — виправлено). НСЗУ не покриває — пілотні програми. Out-of-pocket "
            "переважно. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "larotrectinib": dict(
        registered=True,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "Реєстрація МОЗ підтверджена для NTRK-fusion+ пухлин (тумор-агностично; раніше "
            "registered=false — виправлено). НСЗУ не покриває — out-of-pocket/named-patient. "
            "Джерело: nszu.gov.ua (2026-04)."
        ),
    ),
    "darolutamide": dict(
        registered=True,
        reimbursed_nszu=True,
        indications=[
            "Реімбурсаційний пакет «Онкологія» 2026: nmCRPC високого ризику з ADT (ARAMIS)",
            "Реімбурсаційний пакет «Онкологія» 2026: mHSPC з ADT+docetaxel (ARASENS)",
        ],
        notes=(
            "Зареєстрований; НСЗУ покриває nmCRPC та mHSPC (ARASENS). Кращий профіль ЦНС-проникності "
            "ніж enzalutamide/apalutamide. Джерело: nszu.gov.ua (2026-04)."
        ),
    ),

    # ── Borderline ────────────────────────────────────────────────────────
    "luspatercept": dict(
        registered=False,
        reimbursed_nszu=False,
        indications=[],
        notes=(
            "BORDERLINE / FLAG: реєстрація МОЗ не підтверджена станом на 2026-04. "
            "Рекомендований ESMO для МДС-LR-RS+ (MEDALIST) та β-таласемії. НСЗУ не покриває. "
            "Очікується включення до пілотних UA-програм у 2026-2027. "
            "Потребує перевірки клінічним co-lead — можлива пере-категоризація до pkg3."
        ),
    ),
}


def update_drug(stem: str, rec: dict) -> bool:
    path = DRUGS_DIR / f"{stem}.yaml"
    yaml_io = YAML()
    yaml_io.preserve_quotes = True
    yaml_io.width = 4096  # avoid auto-wrap of long strings
    with path.open("r", encoding="utf-8") as fh:
        data = yaml_io.load(fh)

    rs = data.setdefault("regulatory_status", {})
    ur = rs.setdefault("ukraine_registration", {})
    ur["registered"] = rec["registered"]
    ur["reimbursed_nszu"] = rec["reimbursed_nszu"]
    ur["reimbursement_indications"] = list(rec["indications"])
    ur["last_verified"] = LV
    ur["notes"] = rec["notes"]

    with path.open("w", encoding="utf-8", newline="\n") as fh:
        yaml_io.dump(data, fh)
    return True


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] != "all":
        keys = [k.strip() for k in argv[1].split(",") if k.strip()]
    else:
        keys = list(DRUGS.keys())
    missing = [k for k in keys if k not in DRUGS]
    if missing:
        print(f"UNKNOWN keys: {missing}", file=sys.stderr)
        return 2
    for k in keys:
        update_drug(k, DRUGS[k])
        print(f"updated {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
