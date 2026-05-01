"""Built-in UA→EN translation overrides for engine-emitted free-text.

Consulted by `render._translate_kb_text` BEFORE the optional live
DeepL/LibreTranslate client. Lets EN renders be fully deterministic in
the browser (Pyodide) where no translation API is reachable, and avoids
hitting paid APIs at build time for code-side strings whose translation
is fixed and reviewed.

Two tables:

- `OVERRIDES_UK_TO_EN`: exact-match UA → EN. Keys must match the
  runtime-concatenated form emitted by the engine, NOT the source-code
  fragments (Python implicit string-concatenation joins them before any
  rendering happens).

- `PREFIX_OVERRIDES_UK_TO_EN`: list of (UA prefix, EN replacement)
  tuples. Used for engine-emitted strings with interpolated IDs at the
  end (e.g. "Чи доступні препарати без реімбурсації НСЗУ для пацієнта
  (DRUG-X, DRUG-Y)? ..."). The matcher replaces the UA prefix with the
  EN one and keeps the trailing variable text intact.

Per CHARTER §8.3 these EN strings are reviewed code-side translations,
not machine output requiring clinical sign-off — they describe
specialty-routing rationale, not clinical recommendations.
"""

from __future__ import annotations


OVERRIDES_UK_TO_EN: dict[str, str] = {
    # ── MDT role reasons (mdt_orchestrator._apply_role_rules) ────────────
    "Лімфомний діагноз — провідна спеціальність для терапевтичного ведення.":
        "Lymphoma diagnosis — leading specialty for treatment management.",
    "Активна вірусна етіологія (HCV/HBV) потребує паралельного ведення антивірусної терапії та оцінки реактивації.":
        "Active viral etiology (HCV/HBV) requires parallel antiviral management and reactivation risk assessment.",
    "Наявні візуалізаційні знахідки — потрібен радіолог для staging/restaging.":
        "Imaging findings present — radiologist needed for staging/restaging.",
    "Підтвердження гістології лімфоми + оцінка ризику трансформації (DLBCL/Richter).":
        "Confirm lymphoma histology + assess transformation risk (DLBCL/Richter).",
    "Хіміоімунотерапевтичний схема — drug-drug interactions, dose adjustments, premedication.":
        "Chemoimmunotherapy regimen — drug-drug interactions, dose adjustments, premedication.",
    "Екстранодальна MALT-лімфома — у частини локалізацій локальна променева терапія є опцією.":
        "Extranodal MALT lymphoma — local radiotherapy is an option in certain sites.",
    "У плані використовуються препарати без реімбурсації НСЗУ — потрібна оцінка доступу для пацієнта.":
        "Plan includes drugs without NSZU reimbursement — patient access pathway must be assessed.",
    "Indication посилається на actionable геномний біомаркер — потрібна інтерпретація мутації / target / actionability.":
        "Indication references an actionable genomic biomarker — mutation / target / actionability interpretation needed.",
    "Знижений performance status / декомпенсована коморбідність — потрібна оцінка цілей лікування.":
        "Reduced performance status / decompensated comorbidity — goals-of-care assessment needed.",

    # ── MDT diagnostic-mode role reasons (_apply_diagnostic_role_rules) ──
    "Підозра на лімфому — провідна спеціальність для diagnostic workup та подальшого ведення.":
        "Suspected lymphoma — leading specialty for diagnostic workup and subsequent management.",
    "Будь-яка підозра вимагає біопсії — патолог планує вибір місця, IHC панель, ancillary tests.":
        "Any suspicion requires biopsy — pathologist plans site selection, IHC panel, ancillary tests.",
    "Stage / restaging imaging + biopsy guidance — радіолог.":
        "Stage / restaging imaging + biopsy guidance — radiologist.",
    "Підозра на солідну пухлину — оцінка resectability, biopsy approach.":
        "Suspected solid tumor — resectability assessment, biopsy approach.",
    "Перед anti-CD20 treatment status HCV/HBV має бути відомий — ще на діагностичній фазі.":
        "HCV/HBV status must be known before anti-CD20 treatment — already at the diagnostic phase.",
    "Знижений performance status / ознаки декомпенсації — рання оцінка цілей лікування.":
        "Reduced performance status / decompensation signs — early goals-of-care assessment.",

    # ── MDT open questions: question + rationale (concat'd at runtime) ──
    "Чи проведена серологія HBV (HBsAg, anti-HBc total)? До початку anti-CD20 терапії статус має бути відомий.":
        "Has HBV serology (HBsAg, anti-HBc total) been done? Status must be known before starting anti-CD20 therapy.",
    "Anti-CD20 без HBV профілактики при HBsAg+/anti-HBc+ несе значний ризик реактивації (CI-HBV-NO-PROPHYLAXIS).":
        "Anti-CD20 without HBV prophylaxis in HBsAg+/anti-HBc+ patients carries significant reactivation risk (CI-HBV-NO-PROPHYLAXIS).",
    "Який стадій фіброзу/цирозу печінки (Child-Pugh, FIB-4)? Це впливає на вибір DAA та dosing бендамустину.":
        "What is the hepatic fibrosis/cirrhosis stage (Child-Pugh, FIB-4)? It affects DAA selection and bendamustine dosing.",
    "Декомпенсований цироз — RF-DECOMP-CIRRHOSIS, вимагає змін у схемі.":
        "Decompensated cirrhosis — RF-DECOMP-CIRRHOSIS, requires regimen modification.",
    "Чи підтверджено CD20+ статус гістологією (IHC)? Без CD20+ rituximab/obinutuzumab не показані.":
        "Is CD20+ status confirmed by histology (IHC)? Without CD20+, rituximab/obinutuzumab are not indicated.",
    "Anti-CD20 терапія — основа для більшості ліній; відсутність експресії CD20 повністю змінює regimen.":
        "Anti-CD20 therapy is the backbone of most lines of treatment; absence of CD20 expression fully changes the regimen.",
    "Чи виконано повне стадіювання (Lugano + PET/CT або CT)?":
        "Has complete staging been done (Lugano + PET/CT or CT)?",
    "Прогноз і вибір треку залежать від stage та tumor burden.":
        "Prognosis and track selection depend on stage and tumor burden.",
    "Який актуальний LDH? Маркер пухлинного навантаження і трансформації.":
        "What is the current LDH? Marker of tumor burden and transformation.",
    "LDH входить у прогностичні індекси індолентних лімфом.":
        "LDH is part of the prognostic indices of indolent lymphomas.",
    "Препарати з reimbursed_nszu=false означають out-of-pocket вартість для пацієнта; це впливає на adherence та реалістичність плану.":
        "Drugs with reimbursed_nszu=false mean out-of-pocket cost for the patient; this affects adherence and feasibility of the plan.",

    # ── MDT diagnostic-mode open questions ──────────────────────────────
    "Який результат CD20 IHC буде після біопсії? Без CD20+ rituximab/obinutuzumab не показані.":
        "What will the CD20 IHC result be after biopsy? Without CD20+, rituximab/obinutuzumab are not indicated.",
    "Базис для будь-якого anti-CD20-containing regimen у майбутньому.":
        "Foundation for any future anti-CD20-containing regimen.",
    "Серологія HBV (HBsAg, anti-HBc) — обов'язкова перед anti-CD20; почати workup зараз.":
        "HBV serology (HBsAg, anti-HBc) — mandatory before anti-CD20; start workup now.",
    "HBV reactivation risk при anti-CD20 без prophylaxis.":
        "HBV reactivation risk on anti-CD20 without prophylaxis.",
    "Чи запланований повний staging (PET/CT + bone marrow за показаннями)?":
        "Is complete staging planned (PET/CT + bone marrow as indicated)?",
    "Stage визначає track і treatment intensity.":
        "Stage determines track and treatment intensity.",
    "Множинні гіпотези — розрізнити їх перед treatment discussion.":
        "Multiple hypotheses — must be differentiated before treatment discussion.",

    # ── Provenance event summaries (mdt_orchestrator._bootstrap_provenance) ─
    # Per-RedFlag-fired summary uses a fixed UA prefix; covered via PREFIX list.
}


PREFIX_OVERRIDES_UK_TO_EN: list[tuple[str, str]] = [
    # Q6 in _apply_open_question_rules — drug list + final UA tail
    (
        "Чи доступні препарати без реімбурсації НСЗУ для пацієнта",
        "Are drugs without NSZU reimbursement accessible to the patient",
    ),
    (
        "Чи потрібна social work consult / альтернативний схема?",
        "Is a social work consult / alternative regimen needed?",
    ),
    # DQ4 in _apply_diagnostic_open_questions — hypothesis list + UA tail
    (
        "Який план диференціальної діагностики між гіпотезами:",
        "What is the differential diagnosis plan between hypotheses:",
    ),
    (
        "Які молекулярні / IHC тести розрізняють?",
        "Which molecular / IHC tests differentiate them?",
    ),
    # Provenance auto-generated event summaries (per-RedFlag fired, plan-version, etc.)
    (
        "Engine згенерував план",
        "Engine generated plan",
    ),
    (
        "Запрошено роль",
        "Requested role",
    ),
    (
        "Підняте питання для",
        "Question raised for",
    ),
]


def lookup(text: str) -> str | None:
    """Try exact match first, then prefix-substitution. Return EN string
    if a translation rule applies, else None.

    The prefix rule is greedy: if a UA fragment starts with a known
    prefix, replace it; the trailing text (drug IDs, hypothesis names,
    numeric IDs) is left untouched. Multiple prefixes can match in one
    string; all are applied in order."""
    if not text:
        return None
    stripped = text.strip()
    hit = OVERRIDES_UK_TO_EN.get(stripped)
    if hit is not None:
        return hit
    # Prefix-replace pass — accumulate substitutions
    out = text
    changed = False
    for uk_prefix, en_prefix in PREFIX_OVERRIDES_UK_TO_EN:
        if uk_prefix in out:
            out = out.replace(uk_prefix, en_prefix)
            changed = True
    return out if changed else None
