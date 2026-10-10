"""Ukrainian presentation overlay; IDs, grading and review metadata stay intact."""

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

TRANSLATIONS = json.loads(Path(__file__).with_name("locales").joinpath("handbook.uk.json").read_text(encoding="utf-8"))
CONTENT_KEYS = {"title", "learning_objectives", "at_a_glance", "heading", "body", "stem", "text", "explanation", "learning_focus", "legal_notes"}
UI = {
    "OpenOnco Handbook": "Посібник OpenOnco",
    "Source-grounded oncology learning chapters": "Навчальні розділи з онкології з посиланнями на джерела",
    "Educational chapters generated from checked-in OpenOnco YAML entities, source IDs, synthetic cases, and review metadata. This is not official ESMO content and does not grant CME credit.": "Навчальні розділи створені з YAML-записів OpenOnco, ідентифікаторів джерел, синтетичних випадків і метаданих рев’ю. Це не офіційний контент ESMO; бали CME не нараховуються.",
    "DLBCL first-line clinician review packet": "Пакет клінічного рев’ю першої лінії DLBCL",
    ": synthetic scenarios, actual outputs, source provenance and exportable feedback. Clinical review is pending.": ": синтетичні сценарії, фактичні результати, походження джерел і відгук з експортом. Клінічне рев’ю очікується.",
    "Filter and search chapters": "Фільтри й пошук розділів", "Search": "Пошук", "Title, objective, source ID…": "Назва, навчальна ціль, ID джерела…", "Disease": "Хвороба", "All diseases": "Усі хвороби", "Topic tag": "Тема", "All tags": "Усі теми", "Review status": "Статус рев’ю", "All statuses": "Усі статуси", "No chapters match the current filters.": "Розділів за цими фільтрами не знайдено.", "No handbook chapters are authored yet.": "Розділи посібника ще не створені.",
    "draft": "чернетка", "proposed": "запропоновано", "reviewed": "перевірено", "needs_refresh": "потребує оновлення", "retired": "архівовано", "intro": "початковий рівень", "intermediate": "середній рівень", "advanced": "високий рівень", "hcp_learner": "для медичних фахівців", "type_a": "одна правильна відповідь", "type_k": "кілька правильних відповідей", "short_answer": "коротка відповідь", "mcq": "тестове запитання",
    "Linked entities": "Пов’язані записи", "Section sources": "Джерела розділу", "Learning objectives": "Навчальні цілі", "At a glance": "Основні положення", "Worked synthetic cases": "Розібрані синтетичні випадки", "Practice questions": "Практичні запитання", "Reset quiz": "Скинути тест", "Submit answer": "Перевірити відповідь", "Reset": "Скинути", "Reveal model answer": "Показати зразок відповіді", "Your answer (free text — not graded)": "Ваша відповідь (вільний текст — не оцінюється)", "Correct answer:": "Правильна відповідь:", "Sources:": "Джерела:", "Reasoning tags:": "Теми обґрунтування:", "none": "немає",
    "Answers, score, and reasoning tags are kept in your browser session only and clear when you close this tab. Multi-select questions require every correct option (and no extras) for a credit.": "Відповіді, результат і теми обґрунтування зберігаються лише в сесії браузера та очищуються після закриття вкладки. Для зарахування запитання з кількома відповідями потрібно обрати всі правильні варіанти й жодного зайвого.",
    "Deterministic learning chapter over OpenOnco KB entities, synthetic cases, and source records.": "Навчальний розділ, відтворювано побудований із записів бази знань OpenOnco, синтетичних випадків і джерел.",
    "Educational use only.": "Лише для навчання.", "This OpenOnco-authored chapter is not official ESMO material, not a CME-credit activity, and not patient-specific medical advice.": "Цей розділ авторства OpenOnco не є офіційним матеріалом ESMO, не нараховує балів CME та не є індивідуальною медичною порадою.",
    "Current status": "Поточний статус", "Last reviewed": "Останнє рев’ю", "not yet reviewed": "ще не перевірено", "Clinical sign-offs": "Клінічні підтвердження", "No clinical sign-offs recorded yet.": "Клінічних підтверджень ще не зафіксовано.", "Chapter sources": "Джерела розділу", "Entity map": "Карта записів", "No cases linked yet.": "Випадки ще не додані.", "No questions linked yet.": "Запитання ще не додані.",
}
JS_UI = {"✓ Correct": "✓ Правильно", "✗ Not yet — see explanation": "✗ Неправильно — дивіться пояснення", "Model answer revealed": "Зразок відповіді відкрито", "Pick an option first.": "Спершу оберіть варіант.", " of ": " з ", " answered · ": " відповідей · ", " correct": " правильних", " chapter": " розділів"}


def translate_content(value, key=""):
    """Fail on stale/missing prose translations; never translate machine keys."""
    if isinstance(value, dict):
        return {k: translate_content(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [translate_content(v, key) for v in value]
    if isinstance(value, str) and key in CONTENT_KEYS:
        if value not in TRANSLATIONS:
            raise ValueError(f"Missing Ukrainian handbook translation: {value[:100]}")
        return TRANSLATIONS[value]
    return value


class _UITranslator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.raw = None

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        for name, value in attrs:
            if name in {"placeholder", "aria-label"} and value in UI:
                raw = raw.replace(html.escape(value, quote=True), html.escape(UI[value], quote=True))
        self.parts.append(raw)
        if tag in {"script", "style"}:
            self.raw = tag

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")
        if tag == self.raw:
            self.raw = None

    def handle_data(self, data):
        if self.raw:
            if self.raw == "script":
                for source, target in JS_UI.items():
                    data = data.replace("'" + source + "'", "'" + target + "'")
                data = data.replace("(total === 1 ? '' : 's')", "''")
            self.parts.append(data)
            return
        normalized = " ".join(data.split())
        translated = UI.get(normalized)
        if translated is None:
            if re.fullmatch(r"\d+ questions", normalized):
                translated = normalized.split()[0] + " запитань"
            elif re.fullmatch(r"Question \d+", normalized):
                translated = "Запитання " + normalized.split()[1]
            elif re.fullmatch(r"0 of \d+ answered · 0 correct", normalized):
                translated = "0 з " + normalized.split()[2] + " відповідей · 0 правильних"
            elif normalized.startswith("governs status transitions and the "):
                translated = re.sub(r"governs status transitions and the (\d+)-day staleness threshold\.", r"визначає переходи статусів і поріг давності рев’ю в \1 днів.", normalized)
        self.parts.append(html.escape(translated) if translated is not None else data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")


def translate_ui(markup):
    translator = _UITranslator()
    translator.feed(markup)
    return ''.join(translator.parts)
