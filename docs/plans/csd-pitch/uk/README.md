# OpenOnco × CSD Lab — Pitch Pack

Зібрано 2026-04-27. KB snapshot: 2 413 entities. Site: https://openonco.info ·
GitHub: https://github.com/romeo111/OpenOnco

## Що в цій папці

| # | Файл | Що показує |
|---|---|---|
| 01 | `01_clinician_demo.html` | End-to-end clinician demo: BRAF V600E + mCRC NGS-звіт → ESCAT/OncoKB tier badges + NSZU availability + sign-off status. ~63 KB, A4-printable. |
| 02 | `02_patient_demo.html` | Patient-mode рендер з QR-code. UA plain-language, emergency-RF banner, "що запитати лікаря" секція. ~50 KB. |
| 03 | `03_drug_registration_completion.md` | 167/167 онко-препаратів verified UA registration + NSZU reimbursement (100% acceptance). |
| 04 | `04_solid_tumor_audit.md` | Solid-tumor expansion план: gap audit + categorization. |
| 05 | `05_bundle_architecture.md` | Lazy-load bundle architecture: core 1.99 MB + per-disease modules. |
| 06 | `06_signoff_status.md` | Clinical sign-off coverage dashboard (CHARTER §6.1). |
| 07 | `07_clinical_signoff_workflow.md` | Гайд для Clinical Co-Lead: CLI + dashboard + audit log. |
| 08 | `08_engine_lazy_load.md` | Bundle архітектура (technical detail). |
| 09 | `09_clinical_questions.md` | 64 yes/no/clarify питання для гематолога — груповані по 32 діагнозах. |
| — | `EMAIL.md` | Чернетка email до CSD Lab (UA, дві версії — повна + коротка). |

## KB snapshot (2026-04-27)

| Категорія | К-сть |
|---|---:|
| Total entities | **2 413** |
| Diseases | 65 |
| Indications | 302 |
| Algorithms | 110 |
| Regimens | 244 |
| Drugs | 216 (167 з verified UA registration) |
| RedFlags | 462 |
| BiomarkerActionability cells (ESCAT/OncoKB) | 399 |
| Biomarkers | 111 |
| Sources | 268 |
| Reviewer profiles (placeholders) | 3 |
| Tests | 1 450+ |

## Що ми пропонуємо CSD Lab

1. **Безкоштовний clinical-interpretation overlay для ваших MyAction панелей.**
   Ви робите wet lab + variant calling. Ми додаємо ESCAT/OncoKB tier mapping +
   drug recommendations + UA NSZU availability + UA/EN patient-mode рендер.
   Open-source, MIT-style attribution. CHARTER §2 — non-commercial завжди.

2. **Coverage audit ваших 4 панелей** (MyAction BRCA1/2 / 18&18 / Solid 67 / 32 HRR).
   Покажемо gene-by-gene: що actionable, який ESCAT tier у якому tumor type,
   gaps (наприклад, MSI-H/MMR не в Solid 67 — це потенційна panel extension).

3. **Sample interpretation report** для 3 anonymized тест-кейсів.
   1 heme через M398 CLL, 1 solid через M396, 1 breast через M420.
   Side-by-side порівняння поточного MyAction звіту vs OpenOnco-augmented version.

4. **Pyodide widget** для embedding у ваш report PDF як QR-код.
   Пацієнт сканує → відкривається openonco.info/try.html з пред-заповненим
   профілем (browser-only state, нічого на сервер).

## В обмін

Один з ваших молекулярних онкологів стає **Clinical Co-Lead** для solid-tumor
контенту (CHARTER §6.1 вимагає 2 рев'юверів). Це закриває нашу єдину
existential blocker — поки що `reviewer_signoffs: []` на 100% ентіті.
Інфраструктура (CLI + dashboard + audit log) готова — потрібен лише real
clinician для ratification. Кредит співавторства на open-source standard
для UA геноміки.

## Технічна реалізація

- **Engine**: rule-based декларативна система (не LLM, не black-box AI). CHARTER §8.3 —
  LLM не клінічний decision-maker. Лікар може аудитувати чому саме така
  рекомендація дана — кожен step traceable до KB entity з ≥2 sources.
- **Render**: Pyodide-runtime у браузері. PHI ніколи не залишає клієнтський
  браузер (CHARTER §9.3). Lazy-load: ~1.4 MB core + ~30 KB per-disease modules.
- **Sign-off**: CLI + audit log + render badges. Real Co-Lead додає profile YAML
  + bulk-approves через `scripts/clinical_signoff.py`.
- **License**: open-source MIT-style. Атрибуція CSD Lab у кожному
  interpretation звіті, якщо partnership активна.

---

Контакт: GitHub Issues — https://github.com/romeo111/OpenOnco/issues
