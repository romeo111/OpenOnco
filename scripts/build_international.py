"""Build localized public entry points without rewriting clinical records."""

import html
import json
from pathlib import Path

from scripts.site_locales import COPY, locale_href
from scripts.site_nav import render_top_bar
from scripts.site_head import SITE_FONT_LINK, SITE_FAVICON_LINK

SEARCH_COPY = {
    "es": ["Nombre, sinónimo o ID…", "Todos", "Cargando…", "No se encontraron resultados.", "No se pudo cargar el índice. Vuelve a intentarlo.", "Anterior", "Siguiente", "Resultados", "Página", "Enfermedades", "Medicamentos", "Biomarcadores", "Señales de alarma", "Aplicabilidad clínica", "Los resultados y las fichas se muestran en inglés. Busca también con nombres internacionales, símbolos de genes o identificadores."],
    "pt": ["Nome, sinónimo ou ID…", "Todos", "A carregar…", "Não foram encontrados resultados.", "Não foi possível carregar o índice. Tente novamente.", "Anterior", "Seguinte", "Resultados", "Página", "Doenças", "Medicamentos", "Biomarcadores", "Sinais de alerta", "Aplicabilidade clínica", "Os resultados e as fichas são apresentados em inglês. Pesquise também por nomes internacionais, símbolos de genes ou identificadores."],
    "de": ["Name, Synonym oder ID…", "Alle", "Wird geladen…", "Keine Ergebnisse gefunden.", "Der Index konnte nicht geladen werden. Versuchen Sie es erneut.", "Zurück", "Weiter", "Ergebnisse", "Seite", "Erkrankungen", "Arzneimittel", "Biomarker", "Warnsignale", "Klinische Anwendbarkeit", "Ergebnisse und Datensätze werden auf Englisch angezeigt. Suchen Sie auch nach internationalen Namen, Gensymbolen oder Kennungen."],
    "fr": ["Nom, synonyme ou identifiant…", "Tous", "Chargement…", "Aucun résultat trouvé.", "Impossible de charger l’index. Réessayez.", "Précédent", "Suivant", "Résultats", "Page", "Maladies", "Médicaments", "Biomarqueurs", "Signaux d’alerte", "Applicabilité clinique", "Les résultats et les fiches sont affichés en anglais. Recherchez aussi les noms internationaux, les symboles de gènes ou les identifiants."],
}

CHAPTER_TITLES = {
    "es": ["Cáncer de mama metastásico HER2+: razonamiento de primera línea", "Cáncer de mama metastásico HR+/HER2−: razonamiento de primera línea", "Cáncer colorrectal metastásico: biomarcadores en primera línea", "Linfoma difuso de células B grandes: razonamiento de primera línea", "Melanoma metastásico: BRAF e inmunoterapia en primera línea", "Mieloma múltiple: razonamiento de primera línea", "Cáncer de pulmón no microcítico metastásico: primera línea", "Cáncer de ovario avanzado: mantenimiento de primera línea y HRD/BRCA", "Cáncer de próstata metastásico resistente a la castración: biomarcadores y secuenciación"],
    "pt": ["Cancro da mama metastático HER2+: raciocínio de primeira linha", "Cancro da mama metastático HR+/HER2−: raciocínio de primeira linha", "Cancro colorretal metastático: biomarcadores na primeira linha", "Linfoma difuso de grandes células B: raciocínio de primeira linha", "Melanoma metastático: BRAF e imunoterapia na primeira linha", "Mieloma múltiplo: raciocínio de primeira linha", "Cancro do pulmão de não pequenas células metastático: primeira linha", "Cancro do ovário avançado: manutenção de primeira linha e HRD/BRCA", "Cancro da próstata metastático resistente à castração: biomarcadores e sequenciação"],
    "de": ["HER2-positives metastasiertes Mammakarzinom: Erstlinientherapie", "HR-positives/HER2-negatives metastasiertes Mammakarzinom: Erstlinientherapie", "Metastasiertes kolorektales Karzinom: Biomarker in der Erstlinie", "Diffuses großzelliges B-Zell-Lymphom: Erstlinientherapie", "Metastasiertes Melanom: BRAF und Immuntherapie in der Erstlinie", "Multiples Myelom: Erstlinientherapie", "Metastasiertes nichtkleinzelliges Lungenkarzinom: Erstlinientherapie", "Fortgeschrittenes Ovarialkarzinom: Erstlinien-Erhaltungstherapie und HRD/BRCA", "Metastasiertes kastrationsresistentes Prostatakarzinom: Biomarker und Therapiesequenz"],
    "fr": ["Cancer du sein métastatique HER2+ : raisonnement en première ligne", "Cancer du sein métastatique RH+/HER2− : raisonnement en première ligne", "Cancer colorectal métastatique : biomarqueurs en première ligne", "Lymphome diffus à grandes cellules B : raisonnement en première ligne", "Mélanome métastatique : BRAF et immunothérapie en première ligne", "Myélome multiple : raisonnement en première ligne", "Cancer bronchique non à petites cellules métastatique : première ligne", "Cancer de l’ovaire avancé : entretien de première ligne et HRD/BRCA", "Cancer de la prostate métastatique résistant à la castration : biomarqueurs et séquence thérapeutique"],
}
CHAPTER_IDS = ["HB-BREAST-HER2-POS-MET-1L", "HB-BREAST-HR-POS-HER2-NEG-1L", "HB-CRC-METASTATIC-1L", "HB-DLBCL-1L", "HB-MELANOMA-METASTATIC-1L", "HB-MM-1L", "HB-NSCLC-METASTATIC-1L", "HB-OVARIAN-MAINTENANCE-1L", "HB-PROSTATE-MCRPC-1L"]


def esc(text):
    return html.escape(str(text), quote=True)


def _shell(locale, page, title, lead, content):
    t = COPY[locale]
    active = page.removesuffix(".html") if page != "index.html" else "home"
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — OpenOnco</title><meta name="description" content="{esc(lead)}">
{SITE_FONT_LINK}{SITE_FAVICON_LINK}
<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/international.css?v=20261010"></head>
<body class="home-page">{render_top_bar(active, locale, page_path=page)}
<main class="international-main"><section class="international-hero"><p class="home-kicker">{esc(t['kicker'])}</p><h1>{esc(title)}</h1><p class="international-lead">{esc(lead)}</p></section>
{content}
<section class="international-note"><h2>{esc(t['clinical_title'])}</h2><p>{esc(t['clinical'])}</p></section>
<footer class="page-foot">{esc(t['footer'])} · <a href="https://github.com/romeo111/OpenOnco">GitHub</a></footer></main></body></html>'''


def _button(href, text, secondary=False):
    return f'<a class="btn {"btn-secondary" if secondary else "btn-primary"}" href="{esc(href)}">{esc(text)}</a>'


def _note(t):
    return f'<section class="international-note"><h2>{esc(t["status_title"])}</h2><p>{esc(t["status"])}</p></section>'


def render_wiki(locale):
    t, s = COPY[locale], SEARCH_COPY[locale]
    kinds = ["", "diseases", "drugs", "biomarkers", "redflags", "biomarker_actionability"]
    options = ''.join(f'<option value="{k}">{esc(s[1] if not k else s[9+i-1])}</option>' for i, k in enumerate(kinds))
    content = f'''<section class="international-search" role="search" aria-label="{esc(t['search'])}">
<label for="international-query">{esc(t['search'])}</label><p id="international-hint">{esc(s[14])}</p>
<form id="international-search"><input type="search" id="international-query" name="q" placeholder="{esc(s[0])}" aria-describedby="international-hint" autocomplete="off"><button class="btn btn-primary" type="submit">{esc(t['search'])}</button>
<label for="international-kind" class="sr-only">{esc(s[1])}</label><select id="international-kind" name="kind">{options}</select></form></section>
<p id="international-count" aria-live="polite"></p><div id="international-results" class="international-grid" aria-live="polite"></div>
<nav class="international-pagination" aria-label="{esc(s[8])}"><button id="international-prev" class="btn btn-secondary">{esc(s[5])}</button><span id="international-page"></span><button id="international-next" class="btn btn-secondary">{esc(s[6])}</button></nav>
<script>
(() => {{
const COPY = {json.dumps(s, ensure_ascii=False)};
const query = document.getElementById('international-query'), kind = document.getElementById('international-kind');
const results = document.getElementById('international-results'), count = document.getElementById('international-count');
const prev = document.getElementById('international-prev'), next = document.getElementById('international-next'), pageLabel = document.getElementById('international-page');
let entries = [], loaded = false, failed = false, page = 0;
const params = new URLSearchParams(location.search); query.value = params.get('q') || ''; kind.value = params.get('kind') || '';
function render() {{
  results.replaceChildren();
  if (!loaded) {{ count.textContent = failed ? COPY[4] : COPY[2]; prev.disabled = next.disabled = true; pageLabel.textContent = ''; return; }}
  const words = query.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);
  const selected = entries.filter(e => (!kind.value || e.kind_key === kind.value) && words.every(w => (e.search_text || e.title || '').toLowerCase().includes(w)));
  const pages = Math.max(1, Math.ceil(selected.length / 50)); page = Math.max(0, Math.min(page, pages - 1));
  count.textContent = COPY[7] + ': ' + selected.length; pageLabel.textContent = COPY[8] + ' ' + (page + 1) + ' / ' + pages;
  prev.disabled = page === 0; next.disabled = page === pages - 1;
  if (!selected.length) {{ const p = document.createElement('p'); p.textContent = COPY[3]; results.append(p); }}
  selected.slice(page * 50, (page + 1) * 50).forEach(e => {{
    const card = document.createElement('article'); card.className = 'international-card'; card.lang = 'en';
    const h = document.createElement('h2'), a = document.createElement('a'); a.textContent = e.title; a.href = e.url; a.hreflang = 'en'; h.append(a); card.append(h);
    const meta = document.createElement('p'); meta.textContent = e.subtitle || e.id; card.append(meta);
    const tag = document.createElement('small'); tag.textContent = 'EN · ' + e.id; card.append(tag); results.append(card);
  }});
}}
function change() {{ page = 0; const p = new URLSearchParams(); if(query.value.trim()) p.set('q', query.value.trim()); if(kind.value) p.set('kind', kind.value); history.replaceState(null, '', location.pathname + (p.size ? '?' + p : '') + location.hash); render(); }}
document.getElementById('international-search').addEventListener('submit', e => {{ e.preventDefault(); change(); }});
query.addEventListener('input', change); kind.addEventListener('change', change);
prev.addEventListener('click', () => {{ page--; render(); }}); next.addEventListener('click', () => {{ page++; render(); }});
render(); fetch('/kb_search_index.json').then(r => {{ if(!r.ok) throw new Error(r.status); return r.json(); }}).then(data => {{ entries = data.entries; loaded = true; render(); }}).catch(() => {{ failed = true; render(); }});
}})();
</script>'''
    return _shell(locale, "kb.html", t["search"], s[14], content)


def build_international(output_dir: Path) -> dict:
    stats = json.loads((output_dir / "kb_search_index.json").read_text(encoding="utf-8"))["counts"]
    chapters = json.loads((output_dir / "handbook_index.json").read_text(encoding="utf-8"))["chapters"]
    pages = []
    for locale, t in COPY.items():
        directory = output_dir / locale
        directory.mkdir(parents=True, exist_ok=True)
        title_map = dict(zip(CHAPTER_IDS, CHAPTER_TITLES[locale], strict=True))
        chapter_cards = ''.join(f'<article class="international-card"><h2>{esc(title_map.get(c["id"], c["title"]))}</h2><p>{esc(t["questions"])}: {c["question_count"]} · <code>{esc(t.get(c["review_status"], c["review_status"]))}</code></p>{_button(c["url"], t["chapter_en"])} {_button("/ukr" + c["url"], t["chapter_uk"], True)}</article>' for c in chapters)
        cards = ''.join(f'<article class="international-card"><h2><a href="{locale_href(p, locale)}">{esc(t[k])}</a></h2><p>{esc(t[b])}</p></article>' for p, k, b in [("kb.html", "kb", "lead"), ("handbook.html", "handbook", "handbook_body"), ("try.html", "try_cta", "try_body"), ("ask.html", "ask", "ask_body")])
        count_values = [stats.get("Disease", 0), stats.get("Drugs", 0), stats.get("Biomarkers", 0)]
        counts = ''.join(f'<div><strong>{n}</strong><span>{esc(label)}</span></div>' for n, label in zip(count_values, SEARCH_COPY[locale][9:12]))
        # Counts reflect the actual published search inventory, not a claim
        # that all those records have completed clinical review.
        home_content = f'<div class="cta-row">{_button(locale_href("kb.html", locale), t["search"])} {_button(locale_href("handbook.html", locale), t["learn"], True)}</div><section class="international-stats" aria-label="{esc(t["scale"])}">{counts}</section><section class="international-grid">{cards}</section>' + _note(t)
        generated = {
            "index.html": _shell(locale, "index.html", t["title"], t["lead"], home_content),
            "about.html": _shell(locale, "about.html", t["about_title"], t["about_body"], _note(t) + f'<section class="international-card"><h2>{esc(t["privacy_title"])}</h2><p>{esc(t["privacy"])}</p></section><div class="cta-row">{_button("https://github.com/romeo111/OpenOnco", t["contribute"])} {_button("https://github.com/romeo111/OpenOnco/blob/master/docs/DEVELOPMENT.md", t["documentation"], True)}</div>'),
            "kb.html": render_wiki(locale),
            "handbook.html": _shell(locale, "handbook.html", t["handbook_title"], t["handbook_body"], '<section class="international-grid">' + chapter_cards + '</section>'),
        }
        for page, key, body in [("try.html", "try_cta", "try_body"), ("ask.html", "ask", "ask_body"), ("prevent.html", "prevent", "prevent_body"), ("gallery.html", "gallery", "gallery_body"), ("diseases.html", "diseases", "diseases_body"), ("specs.html", "specs", "specs_body"), ("news.html", "news", "news_body")]:
            generated[page] = _shell(locale, page, t[key], t[body], f'<section class="international-note"><p>{esc(t["english_note"])}</p>{_button("/" + page, t["english"])}</section>')
        for page, markup in generated.items():
            (directory / page).write_text(markup, encoding="utf-8")
            pages.append(f"{locale}/{page}")
    (output_dir / "international.css").write_text(Path(__file__).with_name("site_international.css").read_text(encoding="utf-8"), encoding="utf-8")
    return {"locales": list(COPY), "pages": pages}
