"""Deterministic static KB browser for OpenOnco.

This is intentionally not an LLM-authored medical wiki. It renders a
human-facing browser over the existing source-grounded YAML knowledge base:
entity facts, source IDs, file provenance, and reverse references.
"""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ENTITY_DIRS = {
    "drugs": {"en": "Drug", "uk": "Препарат"},
    "biomarkers": {"en": "Biomarker", "uk": "Біомаркер"},
    "redflags": {"en": "Red flag", "uk": "Тривожна ознака"},
    "biomarker_actionability": {"en": "Actionability", "uk": "Клінічна застосовність"},
}

T = {
    "en": {
        "html_lang": "en",
        "home_href": "/",
        "kb_href": "/kb.html",
        "diseases_href": "/diseases.html",
        "gallery_href": "/gallery.html",
        "capabilities_href": "/capabilities.html",
        "specs_href": "/specs.html",
        "try_href": "/try.html",
        "home": "Home",
        "kb_search": "Onco Wiki",
        "diseases": "Diseases",
        "gallery": "Examples",
        "capabilities": "Capabilities",
        "specs": "Specs",
        "try_it": "Try it",
        "page_title": "Onco Wiki",
        "lead": (
            "Search diseases, drugs, biomarkers, red flags, and biomarker "
            "actionability. Results are generated directly from the YAML "
            "knowledge base and the disease coverage matrix, with source IDs "
            "and reverse references exposed for audit."
        ),
        "info_title": "Source-grounded browser.",
        "info_body": (
            "This page is generated from checked-in YAML entities, not from "
            "free-text LLM answers. Open an entity to see source IDs, review "
            "status, file provenance, and where it is used."
        ),
        "search_label": "Search Onco Wiki",
        "search_placeholder": "Try NSCLC, rituximab, EGFR L858R, SRC-CIVIC, RF-NSCLC...",
        "search_button": "Search",
        "all": "All",
        "no_matches": "No matching Onco Wiki entries.",
        "used_by": "used by",
        "clinician_faq": "Clinician FAQ",
        "faq_prescribe_q": "Does OpenOnco prescribe treatment?",
        "faq_prescribe_a": (
            "No. The engine emits source-cited drafts for MDT discussion and "
            "always requires clinician verification."
        ),
        "faq_redflag_q": "What does a red flag do?",
        "faq_redflag_a": (
            "A red flag is structured logic that can intensify, de-escalate, "
            "block, or redirect an algorithm branch. Its page shows trigger "
            "logic, disease scope, source IDs, and reverse references."
        ),
        "faq_sources_q": "Why are source IDs shown instead of copied guideline text?",
        "faq_sources_a": (
            "OpenOnco references sources while respecting source licensing. The "
            "source ID points to the KB source record and should be checked "
            "against the original guideline or database."
        ),
        "faq_status_q": "What does reviewed or STUB mean?",
        "faq_status_a": (
            "Clinical content remains provisional until it meets the project "
            "sign-off rules. The status line exposes declared review dates and "
            "review-required flags from YAML."
        ),
        "faq_phi_q": "Can this be used with real patient data?",
        "faq_phi_a": (
            "The public site is designed for synthetic or de-identified examples. "
            "Do not paste PHI into public tooling."
        ),
        "entity_lead": (
            "Deterministic view of the source YAML entity. Clinical authority "
            "remains with the cited source IDs and reviewer sign-off state."
        ),
    },
    "uk": {
        "html_lang": "uk",
        "home_href": "/ukr/",
        "kb_href": "/ukr/kb.html",
        "diseases_href": "/ukr/diseases.html",
        "gallery_href": "/ukr/gallery.html",
        "capabilities_href": "/ukr/capabilities.html",
        "specs_href": "/ukr/specs.html",
        "try_href": "/ukr/try.html",
        "home": "Головна",
        "kb_search": "Onco Wiki",
        "diseases": "Хвороби",
        "gallery": "Приклади",
        "capabilities": "Можливості",
        "specs": "Специфікації",
        "try_it": "Спробувати",
        "page_title": "Onco Wiki",
        "lead": (
            "Шукайте хвороби, препарати, біомаркери, тривожні ознаки та "
            "клінічну застосовність біомаркерів. Результати генеруються "
            "безпосередньо з YAML-бази знань і матриці покриття хвороб, із "
            "відкритими source ID та зворотними посиланнями для аудиту."
        ),
        "info_title": "Браузер, прив’язаний до джерел.",
        "info_body": (
            "Ця сторінка генерується з перевірених YAML-сутностей у репозиторії, "
            "а не з довільних відповідей LLM. Відкрийте сутність, щоб побачити "
            "source ID, статус рев’ю, походження файлу та місця використання."
        ),
        "search_label": "Пошук в Onco Wiki",
        "search_placeholder": "Спробуйте NSCLC, rituximab, EGFR L858R, SRC-CIVIC, RF-NSCLC...",
        "search_button": "Шукати",
        "all": "Усе",
        "no_matches": "Записів Onco Wiki за цим запитом не знайдено.",
        "used_by": "використовується у",
        "clinician_faq": "FAQ для клініцистів",
        "faq_prescribe_q": "Чи призначає OpenOnco лікування?",
        "faq_prescribe_a": (
            "Ні. Рушій формує чернетки для обговорення на MDT із посиланнями "
            "на джерела; кожен результат потребує перевірки лікарем."
        ),
        "faq_redflag_q": "Що робить тривожна ознака?",
        "faq_redflag_a": (
            "Тривожна ознака — це структурована логіка, яка може посилити, "
            "деескалувати, заблокувати або перенаправити гілку алгоритму. "
            "Її сторінка показує логіку спрацьовування, хвороби, source ID "
            "та зворотні посилання."
        ),
        "faq_sources_q": "Чому показані source ID, а не скопійований текст настанов?",
        "faq_sources_a": (
            "OpenOnco посилається на джерела з урахуванням ліцензійних обмежень. "
            "Source ID веде до запису джерела в KB; його треба звіряти з "
            "оригінальною настановою або базою даних."
        ),
        "faq_status_q": "Що означають reviewed або STUB?",
        "faq_status_a": (
            "Клінічний контент лишається попереднім, доки не виконає правила "
            "проєктного sign-off. Рядок статусу показує дати рев’ю та прапорці "
            "потреби в рев’ю, взяті з YAML."
        ),
        "faq_phi_q": "Чи можна вводити реальні дані пацієнта?",
        "faq_phi_a": (
            "Публічний сайт призначений для синтетичних або деідентифікованих "
            "прикладів. Не вставляйте PHI у публічні інструменти."
        ),
        "entity_lead": (
            "Детермінований перегляд YAML-сутності з джерельної бази. "
            "Клінічний авторитет лишається за вказаними source ID та статусом "
            "клінічного sign-off."
        ),
    },
}

FIELD_LABELS = {
    "en": {
        "id": "ID",
        "type": "Type",
        "status": "Status",
        "file": "File",
        "diseases": "Diseases",
        "sources": "Sources",
        "aliases": "Aliases",
        "none_declared": "None declared",
        "status_not_declared": "status not declared",
        "reviewed": "reviewed",
        "actionability_review_required": "actionability review required",
        "drug_facts": "Drug Facts",
        "class": "Class",
        "mechanism": "Mechanism",
        "typical_dosing": "Typical dosing",
        "ukraine_registered": "Ukraine registered",
        "nszu_reimbursed": "NSZU reimbursed",
        "ukraine_last_verified": "Ukraine last verified",
        "warnings": "Warnings",
        "biomarker_facts": "Biomarker Facts",
        "biomarker_type": "Biomarker type",
        "mutation_details": "Mutation details",
        "measurement": "Measurement",
        "actionability_lookup": "Actionability lookup",
        "related_biomarkers": "Related biomarkers",
        "redflag_origin": "Red Flag Origin",
        "definition": "Definition",
        "clinical_direction": "Clinical direction",
        "category": "Category",
        "shifts_algorithm": "Shifts algorithm",
        "trigger_logic": "Trigger Logic",
        "actionability_facts": "Actionability Facts",
        "biomarker": "Biomarker",
        "variant": "Variant",
        "disease": "Disease",
        "escat_tier": "ESCAT tier",
        "recommended_combinations": "Recommended combinations",
        "contraindicated_monotherapy": "Contraindicated monotherapy",
        "evidence_summary": "Evidence summary",
        "notes": "Notes",
        "used_by_heading": "Used By",
        "no_reverse_refs": "No reverse references found in the YAML corpus.",
        "more": "more",
    },
    "uk": {
        "id": "ID",
        "type": "Тип",
        "status": "Статус",
        "file": "Файл",
        "diseases": "Хвороби",
        "sources": "Джерела",
        "aliases": "Синоніми",
        "none_declared": "Не вказано",
        "status_not_declared": "статус не вказано",
        "reviewed": "переглянуто",
        "actionability_review_required": "потрібне рев’ю клінічної застосовності",
        "drug_facts": "Дані про препарат",
        "class": "Клас",
        "mechanism": "Механізм дії",
        "typical_dosing": "Типове дозування",
        "ukraine_registered": "Зареєстровано в Україні",
        "nszu_reimbursed": "Відшкодовується НСЗУ",
        "ukraine_last_verified": "Остання перевірка для України",
        "warnings": "Застереження",
        "biomarker_facts": "Дані про біомаркер",
        "biomarker_type": "Тип біомаркера",
        "mutation_details": "Деталі мутації",
        "measurement": "Вимірювання",
        "actionability_lookup": "Пошук клінічної застосовності",
        "related_biomarkers": "Пов’язані біомаркери",
        "redflag_origin": "Походження тривожної ознаки",
        "definition": "Визначення",
        "clinical_direction": "Клінічний напрям",
        "category": "Категорія",
        "shifts_algorithm": "Змінює алгоритм",
        "trigger_logic": "Логіка спрацьовування",
        "actionability_facts": "Дані про клінічну застосовність",
        "biomarker": "Біомаркер",
        "variant": "Варіант",
        "disease": "Хвороба",
        "escat_tier": "Рівень ESCAT",
        "recommended_combinations": "Рекомендовані комбінації",
        "contraindicated_monotherapy": "Протипоказана монотерапія",
        "evidence_summary": "Підсумок доказів",
        "notes": "Нотатки",
        "used_by_heading": "Де використовується",
        "no_reverse_refs": "У YAML-корпусі не знайдено зворотних посилань.",
        "more": "ще",
    },
}

SEARCH_KINDS = set(ENTITY_DIRS)
DISEASE_KIND_LABELS = {"en": "Disease", "uk": "Хвороба"}
ID_RE = re.compile(r"\b(?:DRUG|BIO|BMA|RF|DIS|REG|IND|ALGO|SRC|CI|SUP|TEST|MON)-[A-Z0-9][A-Z0-9_-]*\b")


@dataclass(frozen=True)
class KbEntity:
    kind: str
    kind_label: str
    id: str
    title: str
    data: dict[str, Any]
    path: Path
    rel_path: str

    @property
    def url(self) -> str:
        return f"kb/{self.kind}/{slugify(self.id)}.html"


def _kind_label(kind: str, locale: str = "en") -> str:
    labels = ENTITY_DIRS.get(kind)
    if isinstance(labels, dict):
        return labels.get(locale, labels["en"])
    return kind.replace("_", " ").title()


def _entity_url(entity: KbEntity, locale: str = "en") -> str:
    if locale == "uk":
        return f"ukr/{entity.url}"
    return entity.url


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "entity"


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _text(value: Any, *, limit: int | None = None) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(str(value).split())
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "..."
    return text


def _load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if not data.get("id"):
        return None
    return data


def _name_from_data(data: dict[str, Any]) -> str:
    names = data.get("names")
    if isinstance(names, dict):
        for key in ("preferred", "english", "ukrainian"):
            if names.get(key):
                return str(names[key])
    for key in ("title", "definition", "evidence_summary", "name"):
        if data.get(key):
            return _text(data[key], limit=90)
    return str(data.get("id", ""))


def _aliases(data: dict[str, Any]) -> list[str]:
    names = data.get("names")
    aliases: list[str] = []
    if isinstance(names, dict):
        for key in ("english", "ukrainian"):
            if names.get(key):
                aliases.append(str(names[key]))
        for key in ("synonyms", "brand_names"):
            for item in _as_list(names.get(key)):
                aliases.append(str(item))
    return sorted({a for a in aliases if a and a != _name_from_data(data)})


def load_entities(kb_root: Path) -> dict[str, KbEntity]:
    entities: dict[str, KbEntity] = {}
    for kind_dir in sorted(p for p in kb_root.iterdir() if p.is_dir()):
        kind = kind_dir.name
        kind_label = _kind_label(kind, "en")
        for path in sorted(kind_dir.rglob("*.yaml")):
            data = _load_yaml(path)
            if not data:
                continue
            entity_id = str(data["id"])
            entities[entity_id] = KbEntity(
                kind=kind,
                kind_label=kind_label,
                id=entity_id,
                title=_name_from_data(data),
                data=data,
                path=path,
                rel_path=path.relative_to(kb_root.parent.parent.parent).as_posix(),
            )
    return entities


def _collect_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            found.update(_collect_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_collect_ids(item))
    elif isinstance(value, str):
        found.update(ID_RE.findall(value))
    return found


def build_reverse_refs(entities: dict[str, KbEntity]) -> dict[str, list[KbEntity]]:
    reverse: dict[str, list[KbEntity]] = {}
    for entity in entities.values():
        for ref_id in _collect_ids(entity.data) - {entity.id}:
            reverse.setdefault(ref_id, []).append(entity)
    for refs in reverse.values():
        refs.sort(key=lambda e: (e.kind, e.id))
    return reverse


def _source_ids(data: dict[str, Any]) -> list[str]:
    ids = set()
    for key in ("sources", "primary_sources"):
        for item in _as_list(data.get(key)):
            if isinstance(item, str) and item.startswith("SRC-"):
                ids.add(item)
    for item in _as_list(data.get("evidence_sources")):
        if isinstance(item, dict) and str(item.get("source", "")).startswith("SRC-"):
            ids.add(str(item["source"]))
    return sorted(ids)


def _disease_ids(data: dict[str, Any]) -> list[str]:
    ids = set()
    for key in ("disease_id", "applicable_to_disease"):
        value = data.get(key)
        if isinstance(value, str) and value.startswith("DIS-"):
            ids.add(value)
    for item in _as_list(data.get("relevant_diseases")):
        if isinstance(item, str) and item.startswith("DIS-"):
            ids.add(item)
    applicable = data.get("applicable_to")
    if isinstance(applicable, dict):
        value = applicable.get("disease_id")
        if isinstance(value, str) and value.startswith("DIS-"):
            ids.add(value)
    return sorted(ids)


def _status(entity: KbEntity, locale: str = "en") -> str:
    data = entity.data
    labels = FIELD_LABELS[locale]
    flags = []
    if data.get("last_reviewed") or data.get("last_verified"):
        flags.append(f"{labels['reviewed']} {data.get('last_reviewed') or data.get('last_verified')}")
    if data.get("ukrainian_review_status"):
        flags.append(str(data["ukrainian_review_status"]))
    if data.get("actionability_review_required"):
        flags.append(labels["actionability_review_required"])
    return " | ".join(flags) or labels["status_not_declared"]


def _source_title(source_id: str, entities: dict[str, KbEntity]) -> str:
    source = entities.get(source_id)
    if not source:
        return source_id
    return source.title


def _entity_link(
    entity_id: str,
    entities: dict[str, KbEntity],
    *,
    root_prefix: str = "/",
    locale: str = "en",
) -> str:
    entity = entities.get(entity_id)
    if entity and entity.kind in SEARCH_KINDS:
        return f'<a href="{root_prefix}{html.escape(_entity_url(entity, locale))}"><code>{html.escape(entity_id)}</code></a>'
    return f"<code>{html.escape(entity_id)}</code>"


def _chips(
    ids: list[str],
    entities: dict[str, KbEntity],
    *,
    root_prefix: str = "/",
    locale: str = "en",
) -> str:
    if not ids:
        return f'<span class="kb-muted">{html.escape(FIELD_LABELS[locale]["none_declared"])}</span>'
    return " ".join(
        f'<span class="kb-chip">{_entity_link(i, entities, root_prefix=root_prefix, locale=locale)}</span>'
        for i in ids
    )


def _rows(rows: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"<tr><th>{html.escape(label)}</th><td>{value}</td></tr>"
        for label, value in rows
        if value
    )


def _json_block(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return f"<pre>{html.escape(text)}</pre>"


def _clean_html(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def _shared_top_bar(*, active: str = "kb", locale: str = "en", lang_switch_href: str | None = None) -> str:
    from scripts.build_site import _render_top_bar

    target_lang = "uk" if locale == "uk" else "en"
    if lang_switch_href is None:
        lang_switch_href = "/kb.html" if target_lang == "uk" else "/ukr/kb.html"
    return _render_top_bar(
        active=active,
        target_lang=target_lang,
        lang_switch_href=lang_switch_href,
    )


def _page_shell(
    title: str,
    body: str,
    *,
    active: str = "kb",
    locale: str = "en",
    lang_switch_href: str | None = None,
) -> str:
    from scripts.site_head import SITE_FAVICON_LINK, SITE_FONT_LINK

    t = T[locale]
    return f"""<!doctype html>
<html lang="{html.escape(t["html_lang"])}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - OpenOnco</title>
  {SITE_FONT_LINK}
  {SITE_FAVICON_LINK}
  <link rel="stylesheet" href="/style.css">
  <style>{KB_CSS}</style>
</head>
<body>
  {_shared_top_bar(active=active, locale=locale, lang_switch_href=lang_switch_href)}
  {body}
</body>
</html>
"""


def _frontmatter(entity: KbEntity, entities: dict[str, KbEntity], *, locale: str = "en") -> str:
    data = entity.data
    sources = _source_ids(data)
    diseases = _disease_ids(data)
    labels = FIELD_LABELS[locale]
    rows = [
        (labels["id"], f"<code>{html.escape(entity.id)}</code>"),
        (labels["type"], html.escape(_kind_label(entity.kind, locale))),
        (labels["status"], html.escape(_status(entity, locale))),
        (labels["file"], f"<code>{html.escape(entity.rel_path)}</code>"),
        (labels["diseases"], _chips(diseases, entities, locale=locale)),
        (
            labels["sources"],
            " ".join(
                f'<span class="kb-chip" title="{html.escape(_source_title(s, entities))}"><code>{html.escape(s)}</code></span>'
                for s in sources
            )
            if sources
            else f'<span class="kb-muted">{html.escape(labels["none_declared"])}</span>',
        ),
    ]
    aliases = _aliases(data)
    if aliases:
        rows.insert(2, (labels["aliases"], html.escape(", ".join(aliases[:12]))))
    return f'<table class="kb-facts">{_rows(rows)}</table>'


def _drug_sections(entity: KbEntity, *, locale: str = "en") -> str:
    d = entity.data
    reg = ((d.get("regulatory_status") or {}).get("ukraine_registration") or {})
    labels = FIELD_LABELS[locale]
    rows = [
        (labels["class"], html.escape(_text(d.get("drug_class")))),
        (labels["mechanism"], html.escape(_text(d.get("mechanism"), limit=900))),
        (labels["typical_dosing"], html.escape(_text(d.get("typical_dosing"), limit=700))),
        (labels["ukraine_registered"], html.escape(str(reg.get("registered"))) if reg else ""),
        (labels["nszu_reimbursed"], html.escape(str(reg.get("reimbursed_nszu"))) if reg else ""),
        (labels["ukraine_last_verified"], html.escape(str(reg.get("last_verified"))) if reg.get("last_verified") else ""),
    ]
    warnings = "".join(f"<li>{html.escape(_text(w))}</li>" for w in _as_list(d.get("black_box_warnings"))[:8])
    return f"<h2>{html.escape(labels['drug_facts'])}</h2><table class=\"kb-facts\">{_rows(rows)}</table>" + (
        f"<h2>{html.escape(labels['warnings'])}</h2><ul>{warnings}</ul>" if warnings else ""
    )


def _biomarker_sections(entity: KbEntity, entities: dict[str, KbEntity], *, locale: str = "en") -> str:
    d = entity.data
    labels = FIELD_LABELS[locale]
    rows = [
        (labels["biomarker_type"], html.escape(_text(d.get("biomarker_type")))),
        (labels["mutation_details"], html.escape(_text(d.get("mutation_details"), limit=500))),
        (labels["measurement"], html.escape(_text(d.get("measurement"), limit=500))),
        (labels["actionability_lookup"], html.escape(_text(d.get("actionability_lookup"), limit=500))),
        (labels["related_biomarkers"], _chips([str(x) for x in _as_list(d.get("related_biomarkers"))], entities, locale=locale)),
    ]
    return f'<h2>{html.escape(labels["biomarker_facts"])}</h2><table class="kb-facts">{_rows(rows)}</table>'


def _redflag_sections(entity: KbEntity, *, locale: str = "en") -> str:
    d = entity.data
    labels = FIELD_LABELS[locale]
    rows = [
        (labels["definition"], html.escape(_text(d.get("definition"), limit=900))),
        (labels["clinical_direction"], html.escape(_text(d.get("clinical_direction")))),
        (labels["category"], html.escape(_text(d.get("category")))),
        (labels["shifts_algorithm"], html.escape(", ".join(str(x) for x in _as_list(d.get("shifts_algorithm"))))),
    ]
    trigger = _json_block(d.get("trigger"))
    return f'<h2>{html.escape(labels["redflag_origin"])}</h2><table class="kb-facts">{_rows(rows)}</table>' + (
        f"<h2>{html.escape(labels['trigger_logic'])}</h2>{trigger}" if trigger else ""
    )


def _actionability_sections(entity: KbEntity, entities: dict[str, KbEntity], *, locale: str = "en") -> str:
    d = entity.data
    labels = FIELD_LABELS[locale]
    rows = [
        (labels["biomarker"], _entity_link(str(d.get("biomarker_id")), entities, locale=locale) if d.get("biomarker_id") else ""),
        (labels["variant"], html.escape(_text(d.get("variant_qualifier")))),
        (labels["disease"], _entity_link(str(d.get("disease_id")), entities, locale=locale) if d.get("disease_id") else ""),
        (labels["escat_tier"], html.escape(_text(d.get("escat_tier")))),
        (labels["recommended_combinations"], html.escape(", ".join(str(x) for x in _as_list(d.get("recommended_combinations"))))),
        (labels["contraindicated_monotherapy"], html.escape(", ".join(str(x) for x in _as_list(d.get("contraindicated_monotherapy"))))),
        (labels["evidence_summary"], html.escape(_text(d.get("evidence_summary"), limit=1100))),
    ]
    return f'<h2>{html.escape(labels["actionability_facts"])}</h2><table class="kb-facts">{_rows(rows)}</table>'


def _reverse_ref_section(entity: KbEntity, reverse_refs: dict[str, list[KbEntity]], *, locale: str = "en") -> str:
    labels = FIELD_LABELS[locale]
    refs = [r for r in reverse_refs.get(entity.id, []) if r.id != entity.id]
    if not refs:
        return f"<h2>{html.escape(labels['used_by_heading'])}</h2><p class=\"kb-muted\">{html.escape(labels['no_reverse_refs'])}</p>"
    by_kind: dict[str, list[KbEntity]] = {}
    for ref in refs:
        by_kind.setdefault(_kind_label(ref.kind, locale), []).append(ref)
    parts = [f"<h2>{html.escape(labels['used_by_heading'])}</h2>"]
    for kind, items in sorted(by_kind.items()):
        rows = "".join(
            f'<li><code>{html.escape(item.id)}</code> - {html.escape(item.title)} '
            f'<span class="kb-muted">({html.escape(item.rel_path)})</span></li>'
            for item in items[:40]
        )
        more = f'<li class="kb-muted">... {len(items) - 40} {html.escape(labels["more"])}</li>' if len(items) > 40 else ""
        parts.append(f"<h3>{html.escape(kind)}</h3><ul>{rows}{more}</ul>")
    return "\n".join(parts)


def render_entity_page(
    entity: KbEntity,
    entities: dict[str, KbEntity],
    reverse_refs: dict[str, list[KbEntity]],
    *,
    locale: str = "en",
) -> str:
    if entity.kind == "drugs":
        specifics = _drug_sections(entity, locale=locale)
    elif entity.kind == "biomarkers":
        specifics = _biomarker_sections(entity, entities, locale=locale)
    elif entity.kind == "redflags":
        specifics = _redflag_sections(entity, locale=locale)
    elif entity.kind == "biomarker_actionability":
        specifics = _actionability_sections(entity, entities, locale=locale)
    else:
        specifics = ""

    labels = FIELD_LABELS[locale]
    t = T[locale]
    notes = entity.data.get("notes") or entity.data.get("evidence_summary")
    notes_html = (
        f"<h2>{html.escape(labels['notes'])}</h2><p>{html.escape(_text(notes, limit=1200))}</p>"
        if notes
        else ""
    )
    body = f"""<main class="kb-page kb-entity">
  <p class="kb-breadcrumb"><a href="{t["kb_href"]}">{html.escape(t["kb_search"])}</a> / {html.escape(_kind_label(entity.kind, locale))}</p>
  <h1>{html.escape(entity.title)}</h1>
  <p class="kb-lead">{html.escape(t["entity_lead"])}</p>
  {_frontmatter(entity, entities, locale=locale)}
  {specifics}
  {notes_html}
  {_reverse_ref_section(entity, reverse_refs, locale=locale)}
</main>"""
    switch_locale = "en" if locale == "uk" else "uk"
    return _page_shell(
        f"{entity.title}",
        body,
        locale=locale,
        lang_switch_href="/" + _entity_url(entity, switch_locale),
    )


def _search_entry(entity: KbEntity, reverse_refs: dict[str, list[KbEntity]], *, locale: str = "en") -> dict[str, Any]:
    d = entity.data
    sources = _source_ids(d)
    diseases = _disease_ids(d)
    refs = reverse_refs.get(entity.id, [])
    subtitle_parts = []
    if diseases:
        subtitle_parts.append(("хвороба: " if locale == "uk" else "disease: ") + ", ".join(diseases[:4]))
    if sources:
        subtitle_parts.append(("джерела: " if locale == "uk" else "sources: ") + ", ".join(sources[:4]))
    subtitle_parts.append(_status(entity, locale))
    search_text = " ".join(
        [
            entity.id,
            entity.title,
            entity.kind_label,
            _kind_label(entity.kind, locale),
            " ".join(_aliases(d)),
            " ".join(sources),
            " ".join(diseases),
            _text(d.get("definition")),
            _text(d.get("mechanism")),
            _text(d.get("evidence_summary")),
            _text(d.get("notes")),
        ]
    )
    return {
        "id": entity.id,
        "kind": _kind_label(entity.kind, locale),
        "kind_key": entity.kind,
        "title": entity.title,
        "url": "/" + _entity_url(entity, locale),
        "subtitle": " | ".join(subtitle_parts),
        "sources": sources,
        "diseases": diseases,
        "used_by_count": len(refs),
        "search_text": search_text.lower(),
    }


def _disease_search_entries(kb_root: Path, *, locale: str = "en") -> list[dict[str, Any]]:
    from scripts.disease_coverage_matrix import per_disease_metrics

    rows = per_disease_metrics(kb_root)
    kind = DISEASE_KIND_LABELS[locale]
    url_prefix = "/ukr/diseases.html" if locale == "uk" else "/diseases.html"
    entries: list[dict[str, Any]] = []
    for row in rows:
        disease_id = str(row["id"])
        name = _text(row.get("name")) or disease_id
        family = _text(row.get("family"))
        icd10 = _text(row.get("icd10"))
        subtitle_parts = [
            f"ICD-10: {icd10}" if icd10 else "",
            f"family: {family}" if family and locale == "en" else "",
            f"родина: {family}" if family and locale == "uk" else "",
            f"fill {row['fill_pct']}%",
            f"verified {row['verified_pct']}%",
            f"{row['n_inds']} indications",
            f"{row['n_regs']} regimens",
            f"{row['n_rfs']} red flags",
        ]
        search_text = " ".join(
            [
                disease_id,
                name,
                kind,
                family,
                icd10,
                f"fill {row['fill_pct']}",
                f"verified {row['verified_pct']}",
                f"bio {row['n_bios']}",
                f"drug {row['n_drugs']}",
                f"indication {row['n_inds']}",
                f"regimen {row['n_regs']}",
                f"redflag {row['n_rfs']}",
                "1l algorithm" if row["algo_1l"] else "",
                "2l algorithm" if row["algo_2l"] else "",
                "questionnaire" if row["has_quest"] else "",
                "workup" if row["has_workup"] else "",
            ]
        )
        entries.append(
            {
                "id": disease_id,
                "kind": kind,
                "kind_key": "diseases",
                "title": name,
                "url": f"{url_prefix}#{disease_id}",
                "subtitle": " | ".join(part for part in subtitle_parts if part),
                "sources": [],
                "diseases": [disease_id],
                "used_by_count": row["n_inds"] + row["n_regs"] + row["n_rfs"],
                "search_text": search_text.lower(),
            }
        )
    entries.sort(key=lambda e: (e["title"].lower(), e["id"]))
    return entries


def render_kb_home(entries: list[dict[str, Any]], counts: dict[str, int], *, locale: str = "en") -> str:
    t = T[locale]
    faq = f"""
  <section class="kb-faq">
    <h2>{html.escape(t["clinician_faq"])}</h2>
    <details><summary>{html.escape(t["faq_prescribe_q"])}</summary><p>{html.escape(t["faq_prescribe_a"])}</p></details>
    <details><summary>{html.escape(t["faq_redflag_q"])}</summary><p>{html.escape(t["faq_redflag_a"])}</p></details>
    <details><summary>{html.escape(t["faq_sources_q"])}</summary><p>{html.escape(t["faq_sources_a"])}</p></details>
    <details><summary>{html.escape(t["faq_status_q"])}</summary><p>{html.escape(t["faq_status_a"])}</p></details>
    <details><summary>{html.escape(t["faq_phi_q"])}</summary><p>{html.escape(t["faq_phi_a"])}</p></details>
  </section>
"""
    count_cards = "".join(
        f'<div class="kb-count"><span>{count}</span>{html.escape(label)}</div>'
        for label, count in counts.items()
    )
    filter_buttons = "\n      ".join(
        [
            f'<button type="button" data-kind="">{html.escape(t["all"])}</button>',
            *(
                f'<button type="button" data-kind="{html.escape(label)}">{html.escape(label)}</button>'
                for label in counts
            ),
        ]
    )
    body = f"""<main class="kb-page">
  <section class="kb-hero">
    <h1>{html.escape(t["page_title"])}</h1>
    <p class="kb-lead">{html.escape(t["lead"])}</p>
    <div class="kb-info-box" role="note">
      <strong>{html.escape(t["info_title"])}</strong>
      {html.escape(t["info_body"])}
    </div>
    <div class="kb-counts">{count_cards}</div>
    <label class="kb-search-label" for="kbSearch">{html.escape(t["search_label"])}</label>
    <div class="kb-search-row">
      <input id="kbSearch" class="kb-search" type="search" autocomplete="off" placeholder="{html.escape(t["search_placeholder"])}">
      <button id="kbSearchBtn" class="kb-search-btn" type="button">{html.escape(t["search_button"])}</button>
    </div>
    <div class="kb-filter-row">
      {filter_buttons}
    </div>
  </section>
  <section>
    <div id="kbResults" class="kb-results"></div>
  </section>
  {faq}
</main>
<script>
const KB_ENTRIES = {json.dumps(entries, ensure_ascii=False)};
const KB_COPY = {json.dumps({"no_matches": t["no_matches"], "used_by": t["used_by"]}, ensure_ascii=False)};
const searchInput = document.getElementById('kbSearch');
const searchButton = document.getElementById('kbSearchBtn');
const results = document.getElementById('kbResults');
const filterButtons = Array.from(document.querySelectorAll('[data-kind]'));
let activeKind = '';

function escapeHtml(value) {{
  return String(value || '').replace(/[&<>"']/g, ch => ({{
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }}[ch]));
}}

function scoreEntry(entry, terms) {{
  let score = 0;
  for (const term of terms) {{
    if (!entry.search_text.includes(term)) return -1;
    if (entry.id.toLowerCase().includes(term)) score += 8;
    if (entry.title.toLowerCase().includes(term)) score += 6;
    if (entry.kind.toLowerCase().includes(term)) score += 2;
    score += 1;
  }}
  return score;
}}

function renderResults() {{
  const q = (searchInput.value || '').trim().toLowerCase();
  const terms = q.split(/\\s+/).filter(Boolean);
  const ranked = KB_ENTRIES
    .filter(e => !activeKind || e.kind === activeKind)
    .map(e => [scoreEntry(e, terms), e])
    .filter(pair => terms.length === 0 ? true : pair[0] >= 0)
    .sort((a, b) => b[0] - a[0] || a[1].title.localeCompare(b[1].title))
    .slice(0, 80)
    .map(pair => pair[1]);
  if (!ranked.length) {{
    results.innerHTML = `<p class="kb-muted">${{escapeHtml(KB_COPY.no_matches)}}</p>`;
    return;
  }}
  results.innerHTML = ranked.map(e => `
    <a class="kb-result" href="${{e.url}}">
      <span class="kb-kind">${{escapeHtml(e.kind)}}</span>
      <strong>${{escapeHtml(e.title)}}</strong>
      <code>${{escapeHtml(e.id)}}</code>
      <small>${{escapeHtml(e.subtitle)}} | ${{escapeHtml(KB_COPY.used_by)}} ${{e.used_by_count}}</small>
    </a>
  `).join('');
}}

filterButtons.forEach(btn => btn.addEventListener('click', () => {{
  activeKind = btn.dataset.kind || '';
  filterButtons.forEach(b => b.classList.toggle('active', b === btn));
  renderResults();
}}));
searchInput.addEventListener('input', renderResults);
searchInput.addEventListener('keydown', event => {{
  if (event.key === 'Enter') {{
    event.preventDefault();
    renderResults();
    results.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
  }}
}});
searchButton.addEventListener('click', () => {{
  renderResults();
  results.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
}});
filterButtons[0].classList.add('active');
renderResults();
</script>
"""
    return _page_shell(t["page_title"], body, locale=locale)


def build_kb_wiki(kb_root: Path, output_dir: Path) -> dict[str, Any]:
    entities = load_entities(kb_root)
    reverse_refs = build_reverse_refs(entities)
    searchable = [e for e in entities.values() if e.kind in SEARCH_KINDS]
    searchable.sort(key=lambda e: (e.kind, e.title.lower(), e.id))

    output_dir.mkdir(parents=True, exist_ok=True)
    for kind in SEARCH_KINDS:
        (output_dir / "kb" / kind).mkdir(parents=True, exist_ok=True)
        (output_dir / "ukr" / "kb" / kind).mkdir(parents=True, exist_ok=True)

    payloads: dict[str, dict[str, Any]] = {}
    for locale in ("en", "uk"):
        entity_entries = [_search_entry(e, reverse_refs, locale=locale) for e in searchable]
        disease_entries = _disease_search_entries(kb_root, locale=locale)
        entries = [*disease_entries, *entity_entries]
        count_labels = (
            {
                "drugs": "Drugs",
                "biomarkers": "Biomarkers",
                "redflags": "Red flags",
                "biomarker_actionability": "Actionability",
            }
            if locale == "en"
            else {
                "drugs": "Препарати",
                "biomarkers": "Біомаркери",
                "redflags": "Тривожні ознаки",
                "biomarker_actionability": "Клінічна застосовність",
            }
        )
        counts = {
            DISEASE_KIND_LABELS[locale]: len(disease_entries),
            count_labels["drugs"]: sum(1 for e in searchable if e.kind == "drugs"),
            count_labels["biomarkers"]: sum(1 for e in searchable if e.kind == "biomarkers"),
            count_labels["redflags"]: sum(1 for e in searchable if e.kind == "redflags"),
            count_labels["biomarker_actionability"]: sum(1 for e in searchable if e.kind == "biomarker_actionability"),
        }
        payloads[locale] = {"entries": entries, "counts": counts}

    (output_dir / "kb.html").write_text(
        _clean_html(render_kb_home(payloads["en"]["entries"], payloads["en"]["counts"], locale="en")),
        encoding="utf-8",
    )
    (output_dir / "kb_search_index.json").write_text(
        json.dumps(payloads["en"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "ukr" / "kb.html").write_text(
        _clean_html(render_kb_home(payloads["uk"]["entries"], payloads["uk"]["counts"], locale="uk")),
        encoding="utf-8",
    )
    (output_dir / "ukr" / "kb_search_index.json").write_text(
        json.dumps(payloads["uk"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for entity in searchable:
        out_path = output_dir / entity.url
        out_path.write_text(_clean_html(render_entity_page(entity, entities, reverse_refs, locale="en")), encoding="utf-8")
        uk_out_path = output_dir / "ukr" / entity.url
        uk_out_path.write_text(_clean_html(render_entity_page(entity, entities, reverse_refs, locale="uk")), encoding="utf-8")

    return {
        "entities": len(payloads["en"]["entries"]),
        "counts": payloads["en"]["counts"],
        "index": "kb_search_index.json",
        "home": "kb.html",
        "uk_index": "ukr/kb_search_index.json",
        "uk_home": "ukr/kb.html",
    }


KB_CSS = """
.kb-page { padding-top: 34px; }
.kb-page h1 { font-family: var(--font-display); font-size: 38px; color: var(--green-900); margin-bottom: 10px; }
.kb-page h2 { font-family: var(--font-display); color: var(--green-900); font-size: 24px; margin: 30px 0 12px; }
.kb-page h3 { color: var(--green-900); font-size: 17px; margin: 18px 0 8px; }
.kb-lead { color: var(--gray-700); font-size: 16px; max-width: 880px; margin-bottom: 22px; }
.kb-breadcrumb { font-size: 13px; margin-bottom: 12px; color: var(--gray-500); }
.kb-info-box { background: white; border: 1px solid var(--green-100); border-left: 5px solid var(--green-700); border-radius: 7px; padding: 13px 15px; color: var(--gray-700); margin: 18px 0 20px; max-width: 920px; }
.kb-info-box strong { color: var(--green-900); }
.kb-counts { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin: 20px 0 24px; }
.kb-count { border: 1px solid var(--gray-200); background: white; border-radius: 7px; padding: 12px; color: var(--gray-700); }
.kb-count span { display: block; color: var(--green-700); font-size: 28px; font-weight: 700; line-height: 1; }
.kb-search-label { display: block; font-weight: 700; margin-bottom: 7px; }
.kb-search-row { display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: stretch; }
.kb-search { width: 100%; border: 1px solid var(--gray-200); border-radius: 7px; padding: 13px 14px; font-size: 16px; background: white; }
.kb-search-btn { min-width: 118px; border: 1px solid var(--green-700); background: var(--green-700); color: white; border-radius: 7px; padding: 0 18px; font-weight: 700; cursor: pointer; }
.kb-search-btn:hover { background: var(--green-600); border-color: var(--green-600); }
.kb-filter-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 22px; }
.kb-filter-row button { border: 1px solid var(--gray-200); background: white; color: var(--gray-700); border-radius: 5px; padding: 7px 11px; cursor: pointer; }
.kb-filter-row button.active { background: var(--green-700); color: white; border-color: var(--green-700); }
.kb-results { display: grid; gap: 8px; }
.kb-result { display: grid; grid-template-columns: 105px 1fr auto; gap: 10px; align-items: baseline; background: white; border: 1px solid var(--gray-200); border-radius: 7px; padding: 12px; text-decoration: none; color: var(--gray-900); }
.kb-result:hover { border-color: var(--green-600); }
.kb-result small { grid-column: 2 / -1; color: var(--gray-500); }
.kb-kind { font-family: var(--font-mono); font-size: 11px; color: var(--green-700); text-transform: uppercase; }
.kb-facts { width: 100%; border-collapse: collapse; background: white; border: 1px solid var(--gray-200); border-radius: 7px; overflow: hidden; }
.kb-facts th, .kb-facts td { border-bottom: 1px solid var(--gray-200); padding: 10px 12px; vertical-align: top; text-align: left; }
.kb-facts th { width: 190px; color: var(--gray-700); background: var(--gray-50); }
.kb-chip { display: inline-block; margin: 2px 4px 2px 0; padding: 3px 7px; border-radius: 4px; background: var(--green-50); border: 1px solid var(--green-100); }
.kb-muted { color: var(--gray-500); }
.kb-entity ul { padding-left: 22px; }
.kb-entity pre { background: var(--gray-900); color: white; border-radius: 7px; padding: 14px; overflow: auto; font-size: 12px; }
.kb-faq { margin-top: 36px; }
.kb-faq details { background: white; border: 1px solid var(--gray-200); border-radius: 7px; padding: 11px 13px; margin-bottom: 8px; }
.kb-faq summary { cursor: pointer; font-weight: 700; color: var(--green-900); }
@media (max-width: 700px) {
  .kb-search-row { grid-template-columns: 1fr; }
  .kb-search-btn { min-height: 44px; }
  .kb-result { grid-template-columns: 1fr; }
  .kb-result small { grid-column: auto; }
  .kb-facts th { width: auto; display: block; border-bottom: 0; }
  .kb-facts td { display: block; }
}
"""
