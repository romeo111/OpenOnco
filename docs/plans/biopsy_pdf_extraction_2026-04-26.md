# Biopsy PDF — auto-extract + manual confirm

**Дата:** 2026-04-26.
**Статус:** product + engineering plan, draft для clinical co-leads.
**Зв'язки:** CHARTER §8.3 (LLM extraction allowed з human verification),
CHARTER §9.3 (PHI never leaves the patient device), CHARTER §15.1
(non-device CDS — extraction must show "verify before use"),
DATA_STANDARDS (FHIR R4/R5 + mCODE patient-input).
**Memory:** `feedback_efficacy_over_registration.md` (efficacy > friction —
re-keying biopsies є джерелом помилок та зневіри лікарів).

---

## 0. Project principle (першочергове)

> Лікар вантажить PDF біопсії → форма /try.html авто-заповнюється
> ключовими маркерами (ER/PR/HER2, EGFR, TP53, MGMT, AFP, …) →
> кожен витягнутий маркер — з явним **«✓ підтверджено лікарем»**
> toggle перед тим, як engine його приймає. **PDF та витягнутий
> текст ніколи не покидають браузер.**

Це **інваріант приватності**. План має його захищати, а не тільки
imply-ити. Жодних upload-эндпоінтів, жодних cloud-OCR, жодного
"send to Anthropic for analysis" у v1.

---

## 1. Що працює сьогодні (acceptance baseline)

| Component | Стан | Файл/місце |
|---|---|---|
| /try.html questionnaire form | ✅ | `docs/try.html` — manual entry only |
| Pyodide engine у браузері | ✅ | `docs/openonco-engine.zip` |
| Locked-and-confirm pattern | ✅ partial | example loader + Personalize button |
| PDF parsing | ❌ | nothing wired |
| OCR pipeline | ❌ | (CLAUDE.md мап на tesseract+ukr lang pack для МОЗ ingestion, але це server-side; we need browser-side) |
| Marker regex/NLP | ❌ | nothing |

**Gaps під principle §0:**

1. **PDF text extraction in-browser.** pdf.js — стабільна, ~150KB
   gzipped, MIT-license, працює всередині pyodide-shell-friendly UI.
2. **OCR fallback.** ~30% UA-біопсій — це сканований PDF (скан або
   фото з принтеру). tesseract.js + ukr lang pack — ~3-4MB load,
   повільне (10-30s per page) але точне.
3. **Marker extraction layer.** Regex+prompt-template per-disease.
   Не AI — детермінована, доброякісна для CAP/NCCN-style звітів.
4. **Confirm-toggle UI.** Витягнуті значення показуються з прапором
   ⚠ unconfirmed; engine ignores them поки лікар не натисне ✓.
5. **Audit trail.** Кожна витягнута + підтверджена value — це
   ProvenanceEvent з `extraction_method: regex_v1` + `confirmed_by`.

---

## 2. Архітектура — нові концепти

### 2.1. ExtractedMarker (transient, browser-only)

**НЕ KB entity.** Це in-memory об'єкт, що живе тільки в JS state /
localStorage, ніколи не персистується в knowledge_base/ і не
пересилається на сервер.

```ts
type ExtractionConfidence = "high" | "medium" | "low" | "guess";

interface ExtractedMarker {
  field: string;            // dotted path matching questionnaire (e.g. "biomarkers.ER")
  raw_text: string;         // exact PDF excerpt that produced the match
  parsed_value: any;        // boolean | string | number — same shape engine expects
  confidence: ExtractionConfidence;
  extraction_method: "pdf_text_regex_v1" | "ocr_regex_v1" | "manual";
  pattern_id: string;       // which regex pattern matched (e.g. "BREAST-ER-CAP")
  page: number;
  bbox: [number, number, number, number] | null;  // for highlighting in PDF preview
  confirmed_by_user: boolean;
  confirmed_at: string | null;  // ISO timestamp from browser clock
}
```

**Engine integration:** `assemble_profile()` в `questionnaire_eval.py`
читає тільки `confirmed_by_user === true` поля. Все unconfirmed —
ignored, лічильник `missing_critical` показує їх як "до підтвердження".

### 2.2. MarkerPattern library (per-disease regex)

```yaml
# knowledge_base/extraction/breast_markers.yaml (new dir)
disease_id: DIS-BREAST-INVASIVE
patterns:
  - id: BREAST-ER-CAP
    field: biomarkers.ER
    description: "ER status from CAP-style biomarker block"
    regex_lines:
      - 'ER[\s:]+positive\s+\((\d+)%'
      - 'Estrogen Receptor[:\s]+(positive|negative|POS|NEG)'
    parser: "match group → boolean (positive/POS → true)"
    confidence_default: high
    sources: [SRC-CAP-BREAST-2024]

  - id: BREAST-HER2-IHC
    field: biomarkers.HER2
    regex_lines:
      - 'HER-?2[/-]?neu[\s:]+(\d\+)'
      - 'HER2 IHC[:\s]+score\s+(\d)'
    parser: "score 0/1+ → negative; 2+ → equivocal (needs FISH); 3+ → positive"
    confidence_default: medium  # 2+ requires FISH; we surface as equivocal
```

**Authoring rule:** every pattern has ≥1 `sources:` reference (Tier-1
guideline / CAP synoptic / accredited-lab template) — same evidentiary
floor as KB content (CHARTER §6.1).

### 2.3. ExtractionRun (audit object, transient)

```ts
interface ExtractionRun {
  id: string;                // sha1(pdf_bytes + timestamp), browser-side only
  source_pdf_name: string;   // filename, not path
  page_count: number;
  text_layer_present: boolean;  // false → OCR was needed
  extracted_markers: ExtractedMarker[];
  unmatched_text_excerpts: string[];  // top-N candidates that no pattern caught
  duration_ms: number;
  warnings: string[];        // e.g. "scan quality low — verify carefully"
}
```

**Persists** тільки в browser localStorage під ключем
`openonco.extraction.<run_id>` з 7-day TTL. Жодного server-side
запису.

---

## 3. UI flow

```
┌──────────────────────────────────────────────────┐
│ /try.html                                         │
│ [Хвороба ▼] [Завантажити приклад ▼] [📄 Загрузити biopsy PDF] │
└──────────────────────────────────────────────────┘
                        │
                        ▼ (drag-drop or file picker)
┌──────────────────────────────────────────────────┐
│ Extracting...                                     │
│  ✓ pdf.js text layer extracted (3 pages)         │
│  ✓ regex matched 8 markers, 2 with low confidence│
│  ⚠ HER2 IHC score 2+ — FISH recommended           │
└──────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────┐
│ Form (questionnaire)                              │
│                                                   │
│  ER status:  [POSITIVE 95%] ⚠ Підтвердити   [✓]  │
│              ↳ "ER: 95% nuclear staining" (page 2)│
│                                                   │
│  PR status:  [POSITIVE 80%] ⚠ Підтвердити   [✓]  │
│  HER2:       [EQUIVOCAL 2+] ⚠ Чекає FISH    [✓]  │
│  Ki-67:      [22%]          ⚠ Підтвердити   [✓]  │
│  …                                                │
│                                                   │
│  📋 4 поля з 12 потребують підтвердження          │
│  [Підтвердити всі] [Очистити]                    │
└──────────────────────────────────────────────────┘
                        │
                        ▼
              [Згенерувати план] (disabled поки
                 не всі critical-impact fields = ✓)
```

**Visual rules:**
- Незатверджене поле має жовту-помаранчеву рамку + ⚠ icon.
- Hover на extracted value показує raw PDF excerpt (`<details>` accordion).
- Низька confidence (`low | guess`) → жирний warning "перевірити вручну".
- Engine `runBtn` disabled поки `unconfirmed_critical_count > 0`.

---

## 4. Per-disease pattern coverage (priority)

Зробити в перші 5 хвороб тих, де PDF-біопсія найбагатша на маркери:

| Disease | Markers | Pattern count | Priority |
|---|---|---|---|
| Breast invasive (DIS-BREAST-INVASIVE) | ER, PR, HER2 IHC + FISH, Ki-67, grade, LVI, margins | ~12 | 1 (tracer) |
| NSCLC (DIS-NSCLC) | EGFR (exon 19/L858R/T790M), ALK, ROS1, KRAS G12C, BRAF V600E, PD-L1 (TPS), MET, RET | ~16 | 2 |
| CRC (DIS-CRC) | KRAS, NRAS, BRAF V600E, MSI-H/MMR, HER2 amplification, NTRK | ~10 | 3 |
| Prostate (DIS-PROSTATE) | Gleason score, ISUP grade, PSA, BRCA1/2 (tumor), MSI-H | ~8 | 4 |
| CLL/Lymphoma | TP53 mut+del17p, IGHV mutational status, NOTCH1, ATM, complex karyotype | ~10 | 5 |

**Не для v1:** rare biomarkers (FGFR3 in urothelial, IDH1/2 у glioma і т.д.) —
залишаються manual entry, додаються incrementally.

---

## 5. Phasing

### Phase A — Tracer-bullet (BREAST + text-layer PDFs only)

1. Add pdf.js (~150KB gzip) to `/try.html` head; lazy-load on first
   "Загрузити PDF" click.
2. New module `docs/extraction/breast_v1.js`: 12 patterns from §4 row 1.
   Each pattern: regex + parser callback + confidence + pattern_id.
3. New `runExtraction(pdfBytes, diseaseId)` function:
   - pdf.js parses text layer
   - Iterate patterns, collect matches, dedupe overlapping (prefer higher-confidence)
   - Return ExtractionRun
4. UI: file-picker button, "extracting…" indicator, populate form from
   `ExtractedMarker[]`, render confirm toggles.
5. `assemble_profile()` mod (Pyodide-side): only confirmed markers feed
   into engine.
6. Tests:
   - `tests/test_extraction_breast.js` — 5 fixture PDFs (synthetic NCCN-style
     reports) → 5 expected ExtractionRun outputs (jest or pure-Node test).
   - `tests/test_engine_ignores_unconfirmed.py` — mock browser flow:
     unconfirmed marker NOT in `findings` dict that engine sees.

**Estimate: ~5 днів.** **Critical path** — без цього feature нічого не показує.

### Phase B — OCR fallback + 4 більше хвороб

1. tesseract.js + ukr+eng lang packs (lazy-load, ~4MB total).
2. `runExtraction` detects empty text layer → falls back to OCR per page.
3. Progress indicator (OCR is slow: 10-30s per page) з cancel button.
4. Pattern files for NSCLC + CRC + Prostate + CLL/Lymphoma (§4 rows 2-5).
5. Synthetic fixture PDFs per disease (3-5 each, ~20 total).

**Estimate: ~7 днів.**

### Phase C — Quality + audit + edge cases

1. **Confidence scoring refinement:** patterns get a `score(match,
   context)` callback that bumps confidence based on surrounding text
   (e.g. "ER 95%" with `±50 chars` context "nuclear staining" → high;
   no context → medium).
2. **Unmatched-text surfacing:** top-5 lines that no pattern caught,
   shown collapsed at bottom of form for manual review. Helps catch
   markers we don't yet have patterns for.
3. **ProvenanceEvent on confirm:** kожна "✓ підтверджено" пише event у
   patient_plans/<id>/events.jsonl з `extraction_method`, `pattern_id`,
   `confirmed_at`. Engine MDT graph picks it up via existing merge.
4. **PDF preview pane:** thumbnail виходить, hover на marker
   highlights bbox у preview. (Optional polish.)
5. **Confirmation gate:** `runBtn` lockout enforced + visible counter.

**Estimate: ~5 днів.**

---

## 6. Privacy invariant — enforcement

1. **Network-tab test:** `tests/test_no_pdf_egress.html` opens /try.html
   in headless browser, uploads a fixture PDF, asserts zero network
   requests beyond static assets (pdf.js, tesseract, engine.zip).
2. **CSP hardening:** `Content-Security-Policy: connect-src 'self'`
   на /try.html — browser blocks any accidental fetch to external
   hosts. (Build-time check у `scripts/build_site.py`.)
3. **No localStorage persistence of raw text** — only structured
   `ExtractedMarker[]` з parsed values. Raw PDF text discarded after
   pattern run. (Mitigates сценарій "браузер кешує + бекап у iCloud".)
4. **README block on /try.html:** "PDF не покидає твоє пристрою.
   Перевір це у DevTools → Network."

---

## 7. Governance (CHARTER compliance)

1. **Pattern files = clinical content** → 2-reviewer rule (CHARTER §6.1).
   Author + clinical reviewer signoff before merge.
2. **Confidence default per pattern** — set by author, reviewable.
3. **CHARTER §15.1 Criterion 4 disclosure** на /try.html: "PDF-екстракція —
   допоміжний інструмент. Лікар відповідає за фінальне прийняття значень."
4. **Per-extraction audit:** ProvenanceEvent (Phase C §3) забезпечує
   that every engine input traceable to PDF source + manual confirm.
5. **No clinical decisioning у extraction layer** (CHARTER §8.3) —
   regex/parser тільки витягають значення, не інтерпретують їх. HER2
   2+ marked "equivocal" — engine downstream вирішує що з тим робити.

---

## 8. Acceptance criteria (overall)

Phase plan complete коли:

1. **Breast tracer працює** — 1 fixture PDF → 12 markers extracted,
   confirm-toggle UI, engine receives only confirmed values, plan
   generates.
2. **Privacy invariant test green** — `test_no_pdf_egress.html` пройшов
   на CI.
3. **Top-5 диseases pattern coverage ≥80%** — 80% маркерів типового
   біопсії-звіту витягуються correctly (per fixture suite).
4. **OCR fallback працює** на сканованих PDFs з друкованим текстом
   (handwritten — explicitly out of scope, raise warning).
5. **CSP hardening landed** — connect-src 'self' блокує external fetches.
6. **Per-disease patterns sourced** — each pattern cites a guideline
   або CAP synoptic source.
7. **Confirmation gate enforced** — engine не приймає unconfirmed
   markers, runBtn disabled поки є unconfirmed critical fields.

---

## 9. Ризики і чесні compromise-и

### Ризик: OCR на UA-біопсіях точність

Tesseract на українській з друкованим текстом — ~95-98% chars correct.
Але scan-only PDFs з кепською якістю (тіні, кривий аркуш) — 70-80%.
Маркер як "ТР53 мут." → "TP53 mvT." → regex miss.

**Compromise:** show OCR confidence per-page; на низькій confidence
явно warning "сканована якість низька, перевір кожне поле". Не auto-fill
critical fields на page-confidence < 80%.

### Ризик: regex false positives

"ER negative for amplification" у HER2 секції → regex matches
"ER negative" якщо неуважний. Усі патерни з `±N char` контекстом
(або секційний parser, який спочатку розбиває звіт на блоки).

**Compromise:** patterns мають `requires_context: ["IHC", "Estrogen
Receptor", "ER:"]` requirement — match valid тільки якщо один з cues
поряд.

### Ризик: лікар клікає "✓ всі" не дивлячись

UX-проблема, не технічна. Confirmation gate виглядає як formality.

**Compromise:** "Підтвердити всі" disabled поки користувач не
просковзав через раз кожне поле (sticky scroll observer); critical
fields (HER2 equivocal, MSI status) завжди потребують **окремого**
кліку, не входять у bulk confirm.

### Ризик: PDF-format zoo

Лабораторії в Україні + ЄС + США використовують 50+ темплейтів.
12 регексів на хворобу не покриють все.

**Compromise:** v1 fokuset на "structured CAP synoptic" + найпоширені
templates (Synevo, Diлa, Mayo Clinic). Custom templates → manual entry,
але "unmatched-text surfacing" (Phase C §6.2) допомагає curator-y
розширювати library коли з'являється новий лаб.

### Ризик: "auto-extraction confidence" — ілюзія компетентності

Лікар бачить "extracted with high confidence" і втрачає пильність.
Це класичний automation bias (CHARTER §15.1).

**Compromise:** UI **ніколи не показує** "extraction is correct" —
тільки "extracted, requires confirmation". Confidence score
visualized як warning-color (orange/red) для low/medium, не reassuring
green. Confirm-toggle є unfilled by default навіть для high-confidence
matches.

---

## 10. Open clinical questions (для co-leads)

1. **Confidence threshold для auto-pre-fill** — high тільки, чи medium теж?
   (Аргумент: medium з warning > порожнє поле; контр: пацієнт довіряє
   pre-filled значенням більше ніж warning.)
2. **HER2 equivocal handling** — 2+ score автоматично triggers
   "FISH required" red flag, чи лікар бачить обидва recommendation
   tracks (FISH-positive vs FISH-negative)?
3. **Multi-page concordance** — якщо ER з'являється у 3 секціях
   (synopsis + IHC details + comment), які не співпадають → 1
   highest-confidence чи показуємо всі 3 для ручного вибору?
4. **PDF preview** — чи треба highlighter (показувати raw text у
   контексті), чи enough hover-on-field "ось рядок з PDF"?
5. **Consented data** — якщо ми **отримаємо** consent + ethics — чи
   корисно мати opt-in cloud-LLM режим для "messy" PDFs у майбутньому?
   (Тільки якщо v1 in-browser виявиться недостатнім.)

---

## 11. Recommended first PR

(Per плана §5 Phase A — критично-шляховий blocker.)

Tracer-bullet для **BREAST**, text-layer PDFs only:

1. `docs/extraction/breast_v1.js` — 12 patterns від §4 row 1, з
   sources references.
2. `docs/extraction/runner.js` — pdf.js wrapper, `runExtraction()`
   public function.
3. /try.html: "Загрузити PDF" button, extraction-progress indicator,
   confirm-toggle UI на existing form.
4. Pyodide-side `assemble_profile()` mod — ignore unconfirmed markers.
5. Privacy test: `tests/test_no_pdf_egress.html` (Playwright).
6. Pattern test: 3 synthetic CAP-style fixture PDFs → expected
   ExtractedMarker[] outputs.
7. Doc /try.html footer: privacy + verify-before-use disclosure.

Це ~3-5 днів роботи. Після merge — phases B/C паралельно та безпечно.

---

## 12. Out of scope (explicitly)

- Cloud-LLM extraction (Anthropic/OpenAI) — v1 stays in-browser.
- Handwritten note OCR — quality unreliable, separate research project.
- DICOM/imaging report extraction — biopsy text only for v1.
- HL7/FHIR import — separate flow, не via PDF.
- Non-Latin-script biomarker names (Cyrillic-only labs) — supported via
  ukr lang pack у OCR layer, але pattern library у v1 — англійською.
  Cyrillic-only patterns — Phase C+ if demand.
