# Email до CSD Lab

**Кому:** info@csdlab.ua (підтвердити правильну адресу — є також контакти в
розділі "Партнерство" на сайті https://www.csdlab.ua, або через LinkedIn для
прямого контакту з molecular oncology lead).

**Тема:**

```
Безкоштовний clinical-interpretation шар для MyAction панелей — пропозиція партнерства
```

## Повна версія (UA)

```
Доброго дня,

Я підтримую open-source проект OpenOnco (openonco.info) — безкоштовний
рішень-сапорт інструмент для онкології з фокусом на UA контекст. KB на
зараз: 2 413 ентіті, 65 діагнозів, 302 показання, 462 red-flag правил,
167 препаратів з verified НСЗУ статусом.

Розглянули ваші 4 NGS панелі MyAction (BRCA1/2, 18&18, Solid 67, 32 HRR)
+ MyAction PanCancer + MyAction Tumor Profile Complete + ваш MDT
консиліум. Бачимо одну спільну невирішену задачу: щоб лікар-онколог міг
взяти ваш звіт і одразу зрозуміти "що робити з цим варіантом", потрібен
шар клінічної інтерпретації — ESCAT/OncoKB tier mapping, NSZU-доступність,
trial matching, UA-переклад для пацієнта.

OpenOnco це робить — і ми хотіли б запропонувати безкоштовний
co-branded interpretation шар для ваших MyAction панелей (Foundation
Medicine + Oncotype DX залишаємо в стороні — їхні власні reports
це покривають).

Що пропонуємо як 2-тижневий pilot:

1. Coverage audit ваших 4 панелей: gene-by-gene actionability map,
   ESCAT tiers per tumor type, gaps (наприклад, MSI-H/MMR не в Solid 67 —
   потенційна panel extension).

2. Sample interpretation reports для 3 anonymized тест-кейсів — heme
   (M398 CLL), solid (M396), breast (M420). Сторона до сторони:
   ваш поточний MyAction звіт vs OpenOnco-augmented version.

3. Pyodide widget mock — QR-код у вашому report PDF, пацієнт сканує →
   відкривається openonco.info/try.html з пред-заповненим профілем
   (browser-only state, ніяких PHI на сервер; CHARTER §9.3 + GDPR
   compliance by design).

В обмін: один з ваших молекулярних онкологів стає Clinical Co-Lead
для solid-tumor контенту. Інфраструктура для sign-off (CLI + audit
log + render badges) готова — потрібно тільки real clinician щоб
почати ratification. Кредит співавторства на open-source standard
для UA геноміки.

OpenOnco — non-commercial open-source (MIT-style). CHARTER §2 завжди
forbids paid tier — це не Trojan horse. Цінність для CSD: ваш звіт
стає actionable для лікаря-receivера + brand-touchpoint з пацієнтом
(QR/UA-переклад) + ви рівноправний co-author стандарту.

Pitch pack (9 deliverables) у docs/plans/csd-pitch/ нашого репозиторію:
https://github.com/romeo111/OpenOnco/tree/master/docs/plans/csd-pitch

Можемо зустрітися онлайн на ~30 хв щоб показати:
- Live demo (BRAF V600E mCRC profile через /try.html)
- Coverage audit для MyAction Solid 67 (підготуємо як PDF до зустрічі)
- Q&A про governance та integration shape

Який слот вам зручний на наступному тижні? Можу підлаштуватись.

З повагою,
[Ім'я]
Maintainer, OpenOnco
[Email]
GitHub: romeo111/OpenOnco
```

## Коротша версія (якщо потрібно швидше)

```
Доброго дня,

Підтримую open-source проект OpenOnco (openonco.info) — безкоштовний
oncology decision-support з UA контекстом (НСЗУ-доступність, UA
переклад для пацієнта, ESCAT/OncoKB tier mapping).

Хочу запропонувати безкоштовний co-branded interpretation шар для
ваших MyAction панелей. Не Foundation/Oncotype — їхні власні reports
це покривають. Лише ваші own-IP MyAction PanCancer/Tumor Profile/HRR/etc.

Що зробимо за 2 тижні pilot:
1. Coverage audit ваших 4 MyAction панелей (PDF)
2. 3 sample interpretation reports для anonymized тест-кейсів
3. Pyodide widget mock (QR код для пацієнта)

В обмін — один з ваших молекулярних онкологів стає Clinical Co-Lead
у нашій governance (CHARTER §6.1). Open-source MIT-style, no paid tier.

Pitch-pack: https://github.com/romeo111/OpenOnco/tree/master/docs/plans/csd-pitch

30-хв дзвінок наступного тижня — який слот зручний?

З повагою,
[Ім'я]
```

---

## Що додати перед відправленням

1. **Підпис:** ім'я + email + LinkedIn (якщо є) + телефон
2. **Тема email** — testувати кілька варіантів через A/B якщо буде список
3. **Адреса** — підтвердити info@csdlab.ua або знайти прямий контакт
   (наприклад керівника лабораторії or molecular oncology lead через LinkedIn)
4. **Attachment**: 1 PDF з summary `01_clinician_demo.html` як показовий артефакт
   (опціонально; лінк на GitHub достатньо для ознайомлення)

## Очікувана response

- **Найбільш ймовірно:** generic "дякуємо, передамо технічному директору"
  → fallback: follow-up через 1 тиждень якщо тиша
- **Можливо:** прямий запит на demo → готовий за 1 годину з підготовленим
  coverage audit
- **Малоймовірно:** одразу "так, давайте pilot" — bonus

## Plan B якщо тиша

1. Через тиждень — follow-up email коротший
2. Через 2 тижні — звернутися напряму через molecular oncology lead на LinkedIn
3. Через 3 тижні — через спільні контакти або UA онко-спільноту
   (Українська асоціація медичних онкологів)
