"""Public participation hub and reproducible launch/evaluation materials."""
from pathlib import Path
from scripts.build_kb_wiki import _page_shell

REPO = "https://github.com/romeo111/OpenOnco"

LAUNCH = """Show HN: OpenOnco – rules-first oncology drafts with source citations
https://openonco.info/try.html

OpenOnco applies checked-in YAML rules to structured oncology profiles and
produces source-cited drafts for clinician review. Try a synthetic example
without signup, inspect its sources in Onco Wiki, or run the Python engine.
Deterministic output can still be wrong: clinical content is provisional,
and a qualified oncologist must verify every recommendation.

The Plan Builder runs the Python engine through Pyodide in the browser.
The separate Tumor Board service can send submitted information to its
server; review that page's data notice before entering information.
Code is MIT; project content is CC BY 4.0; upstream sources retain their
own licenses. This is an informational resource, not a medical device.

Feedback requested: reproducible setup failures, missing provenance and
rule/source mismatches on synthetic profiles. Do not post patient data.
Code: https://github.com/romeo111/OpenOnco
Review packet: https://openonco.info/review/dlbcl-1l/
Participation: https://openonco.info/participate.html

Publication status: prepared copy, not submitted. The posting maintainer
must add their true relationship to the project in the first comment.
"""

EVALUATION = """# OpenOnco evaluation and application-paper working outline

Status: protocol and methods outline, not a completed study or submission.
No clinical effectiveness, time savings or safety benefit has been measured.

## Proposed research question
Can reviewers reproduce deterministic source-cited drafts and locate
rule/source discrepancies using the public synthetic review packet?

## Methods available now
Versioned YAML KB, Python rules engine, browser Pyodide execution, source
identifiers, bilingual audit pages and a DLBCL first-line synthetic packet.
Freeze the Git commit and KB revision before evaluation. Record environment,
scenario IDs, expected engineering contracts and complete traces. Technical
contract passes are distinct from clinical correctness and sign-off.

## Evaluation to perform
1. Recruit qualified oncology reviewers; record credentials and conflicts.
2. Independently review synthetic cases in a familiar disease area.
3. Record missing input, unsafe output, source mismatch and severity.
4. Report inter-reviewer disagreement and adjudication; retain negative results.
5. Measure completion time only with a defined comparator and consent.
6. Report denominators, uncertainty, exclusions and KB review limitations.

## Manuscript outline
Background; governance and intended use; architecture; source licensing;
reproducible evaluation methods; results once collected; limitations;
data/code availability; contributions; conflicts; ethics statement as applicable.

## Publication gates
Accountable real authors and clinical co-authors; actual evaluation dataset;
institutional determination of applicable ethics requirements; journal scope
and current submission instructions; no fabricated affiliations or results.
Conference abstracts follow the same evidence gates. No journal/conference
submission has occurred. Patient data cannot be published without the
repository's consent, de-identification and ethics requirements.
"""

INTEROP = """# OpenOnco interoperability gap analysis — 2026-10-10

Scope: conceptual mapping of the checked-in synthetic JSON input shape.
This is not a FHIR adapter, mCODE conformance report or OMOP implementation.
Reference: mCODE 4.0.0 STU4, FHIR R4 (current published guide checked today):
https://hl7.org/fhir/us/mcode/

| OpenOnco input | Candidate FHIR/mCODE representation | Missing work |
| --- | --- | --- |
| patient_id | Patient.identifier | Namespace and identity policy; do not export synthetic labels as real identities |
| disease.id / disease_id | PrimaryCancerCondition | Internal DIS identifiers need reviewed code mappings; entity codes alone do not meet profile requirements |
| demographics.age / sex | Patient and relevant observations | Age is not birthDate; administrative gender and clinical sex require explicit semantics |
| demographics.ecog | ECOGPerformanceStatus observation | Coding, effective time, subject references and profile validation |
| biomarkers | GenomicVariant / GenomicReport where applicable | Variant system, assay, specimen, status, dates and missing-value semantics |
| findings | Observation / DiagnosticReport where applicable | Unit normalization, LOINC mapping, dates and provenance; raw flags cannot be promoted to diagnoses |
| line_of_therapy | Context for treatment records | Does not reconstruct CancerRelatedMedicationAdministration or treatment episodes |
| generated regimen IDs | Draft planning context | A draft is not an administered medication event |

Mapping acceptance work: select supported profiles; pin package versions;
create fully synthetic fixtures; validate with the FHIR validator and mCODE
dependencies; test missing/unknown values and round trips; document every
unsupported element; obtain clinical and terminology review. No conformance
claim until this evidence exists. Licensed terminology gates still apply.

OHDSI Oncology WG focuses on observational oncology data in OMOP:
https://ohdsi.github.io/OncologyWG/
https://ohdsi.github.io/OncologyWG/gettingInvolved.html
Ask about the narrow mapping problem, not endorsement. OpenOnco currently
has no OMOP ETL, vocabulary mapping or observational outcomes dataset.
"""

REVIEW_TEMPLATE = """# Synthetic clinical review report
Git commit / KB version:
Scenario ID (synthetic only):
Reviewer specialty and conflicts (optional public attribution):
Engine input completeness:
Output section / entity / source ID:
Expected behavior and supporting original source:
Observed behavior:
Severity and rationale:
Reproduction steps:
Independent second review / adjudication:

Do not include names, dates of birth, real clinical records or identifiers.
Use the DLBCL packet's local export for structured feedback. Clinical KB
recommendation changes still require two-reviewer approval.
"""


def build_participation(output_dir: Path) -> dict:
    resources = output_dir / "resources"
    resources.mkdir(parents=True, exist_ok=True)
    for name, content in {
        "launch.txt": LAUNCH,
        "evaluation-outline.md": EVALUATION,
        "interop-gap-analysis.md": INTEROP,
        "synthetic-review-template.md": REVIEW_TEMPLATE,
    }.items():
        (resources / name).write_text(content, encoding="utf-8")
    for locale in ("en", "uk"):
        uk = locale == "uk"
        title = "Долучитися до OpenOnco" if uk else "Participate in OpenOnco"
        body = f'''<main class="kb-page">
<h1>{title}</h1>
<p class="kb-lead">{'Допоможіть перевірити код, джерела й зручність розмови з онкологом.' if uk else 'Help verify the code, evidence traces and usefulness for oncology discussion.'}</p>
<p class="kb-info-box">{'Клінічний вміст є попереднім. Потрібна перевірка кваліфікованим онкологом. Технічні тести не є клінічною валідацією. Використовуйте лише синтетичні дані для публічних звітів.' if uk else 'Clinical content is provisional and requires verification by a qualified oncologist. Engineering tests are not clinical validation. Use synthetic data only in public reports.'}</p>
<h2>{'Для розробників' if uk else 'For developers'}</h2>
<ol><li><a href="{'/ukr/try.html' if uk else '/try.html'}">{'Відкрити демо без реєстрації' if uk else 'Try the demo without signup'}</a> — {'оберіть синтетичний приклад і перевірте посилання на джерела.' if uk else 'choose a synthetic example and inspect its source links.'}</li>
<li>{'Для локальної роботи: Python 3.12, окреме середовище, залежності з requirements.lock.' if uk else 'For local development: Python 3.12, an isolated environment and requirements.lock.'}</li></ol>
<pre><code>git clone https://github.com/romeo111/OpenOnco.git
cd OpenOnco
python -m venv .venv
# Activate .venv for your operating system, then:
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python scripts/audit_validator.py --human
python -m http.server 8000 --directory docs</code></pre>
<p><a href="{REPO}/blob/master/docs/DEVELOPMENT.md">Development guide</a> · <a href="{REPO}/blob/master/mcp_server/README.md">MCP setup</a> · <a href="{REPO}/issues/new">{'Повідомити про відтворювану помилку' if uk else 'Report a reproducible issue'}</a></p>
<h2>{'Для клінічних рецензентів' if uk else 'For clinical reviewers'}</h2>
<p>{'Почніть із пакета DLBCL першої лінії: синтетичні сценарії, трасування правил і локальний експорт відгуку. Виберіть сценарій у своїй спеціальності, порівняйте результат з оригінальними джерелами й зафіксуйте розбіжності.' if uk else 'Start with the DLBCL first-line packet: synthetic scenarios, rule traces and local feedback export. Choose a scenario within your expertise, compare the output with original sources and record discrepancies.'}</p>
<p><a class="btn btn-primary" href="/review/dlbcl-1l/">{'Відкрити пакет рецензування' if uk else 'Open the review packet'}</a> · <a href="/resources/synthetic-review-template.md" download>{'Шаблон звіту' if uk else 'Review report template'}</a></p>
<h2>{'Розмова з лікарем і PDF' if uk else 'Doctor discussion and PDF'}</h2>
<p>{'У Plan Builder відкрийте синтетичний приклад або створений план, натисніть «Для лікаря · PDF» та виберіть «Зберегти як PDF» у браузері. Друкується сам план із посиланнями на джерела. Лікар має перевірити його застосовність; не змінюйте лікування самостійно.' if uk else 'In Plan Builder, open a synthetic example or generated plan, select “Share with your doctor · PDF”, then “Save as PDF” in the browser. The plan itself is printed with its source citations. Your clinician must verify applicability; do not change treatment yourself.'}</p>
<h2>{'Стандарти та інтеграції' if uk else 'Standards and integrations'}</h2>
<p>{'Опубліковано початковий аналіз відповідності полів mCODE/FHIR R4 і відсутніх елементів. Готового FHIR/OMOP-адаптера та підтвердженої відповідності mCODE поки немає.' if uk else 'An initial mCODE/FHIR R4 field mapping and gap analysis is available. A FHIR/OMOP adapter and demonstrated mCODE conformance are pending.'}</p>
<p><a href="/resources/interop-gap-analysis.md">{'Аналіз прогалин' if uk else 'Interop gap analysis'}</a> · <a href="https://hl7.org/fhir/us/mcode/">mCODE 4.0.0</a> · <a href="https://ohdsi.github.io/OncologyWG/gettingInvolved.html">OHDSI Oncology WG</a></p>
<h2>{'Пацієнтські організації та клініки з обмеженими ресурсами' if uk else 'Advocacy groups and resource-constrained clinics'}</h2>
<p>{'Пропонуємо перевірку зрозумілості освітніх матеріалів і підготовки запитань до онколога на синтетичних прикладах. Пілот потребує відповідального клінічного рецензента, перевірки місцевого контексту й конфіденційності. Доступність коду не означає доступність препаратів чи ліцензованих рекомендацій.' if uk else 'A useful initial collaboration is reviewing educational wording and question preparation using synthetic examples. Any pilot needs an accountable clinical reviewer, local context and privacy review. Free code does not imply access to drugs or licensed guidelines.'}</p>
<p><a href="{REPO}/issues/new">{'Запропонувати конкретний освітній або технічний пілот без даних пацієнтів' if uk else 'Propose a specific educational or technical pilot without patient data'}</a></p>
<h2>{'Публікації та відкритий запуск' if uk else 'Publication and public launch'}</h2>
<p><a href="/resources/evaluation-outline.md">{'План дослідження та структура статті' if uk else 'Evaluation protocol and paper outline'}</a> · <a href="/resources/launch.txt" download>{'Текст Show HN' if uk else 'Show HN launch copy'}</a></p>
<p>{'Матеріали готові для підготовки запуску. Зовнішні пости й заявки не подані; результати дослідження та клінічні автори ще потрібні для академічної публікації.' if uk else 'These materials support launch preparation. External posts and submissions have not been sent; study results and accountable clinical authors are still required for academic publication.'}</p>
<p>{'Код: MIT. Вміст проєкту: CC BY 4.0. Оригінальні джерела мають власні ліцензії.' if uk else 'Code: MIT. Project content: CC BY 4.0. Original sources retain their own licenses.'}</p>
</main>'''
        path = output_dir / ("ukr/participate.html" if uk else "participate.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_page_shell(title, body, active="", locale=locale, lang_switch_href="/participate.html" if uk else "/ukr/participate.html"), encoding="utf-8")
    return {"pages": 2, "resources": 4}
