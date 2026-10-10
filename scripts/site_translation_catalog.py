"""Exact public prose catalogs; source data and executable code stay unchanged."""
import html
import ast
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

LANGUAGES = ('es', 'pt', 'de', 'fr')
PAGES = ('try.html', 'ask.html', 'prevent.html', 'diseases.html', 'gallery.html', 'handbook.html', 'kb.html')
CATALOG_DIR = Path(__file__).with_name('locales')

def normalize(text):
    return ' '.join(text.split())

def prose(text):
    text = normalize(text)
    return bool(re.search(r'[A-Za-z]{3}', text)) and not (
        re.search(r'[\u0400-\u04ff]', text) or re.fullmatch(r'[A-Z0-9_.:/+−–-]+', text)
        or text.startswith(('https://', 'http://', 'SRC-', 'DIS-', 'BIO-', 'DRUG-', 'REG-', 'ALGO-', 'RF-', 'IND-', 'HQ-', 'HB-'))
    )

class ProseCollector(HTMLParser):
    def __init__(self, dynamic_only=False):
        super().__init__(convert_charrefs=True)
        self.dynamic_only = dynamic_only
        self.stack = []
        self.strings = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'area', 'wbr'}:
            self.stack.append(tag)
        if self.dynamic_only:
            return
        if not any(t in {'script', 'style', 'code', 'pre'} for t in self.stack):
            for key in ('title', 'aria-label', 'placeholder', 'alt', 'data-step-label'):
                if prose(attrs.get(key, '')):
                    self.strings.add(normalize(attrs[key]))
            if tag == 'meta' and attrs.get('name') == 'description' and prose(attrs.get('content', '')):
                self.strings.add(normalize(attrs['content']))
            if prose(attrs.get('data-search', '')):
                self.strings.add(normalize(attrs['data-search']))
    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]
    def handle_data(self, data):
        if self.stack and self.stack[-1] == 'script':
            # Collect display literals without rewriting or executing the script.
            for match in re.finditer(r'''(["'])([^\n\\]*?)\1''', data):
                value = match.group(2)
                if prose(value) and len(value) < 240 and not re.search(r'[{}<>;=]', value):
                    self.strings.add(normalize(value))
        if not self.dynamic_only and not any(t in {'script', 'style', 'code', 'pre', 'textarea'} for t in self.stack) and prose(data):
            self.strings.add(normalize(data))

def source_pages(root):
    return [root / p for p in PAGES if (root / p).exists()] + [
        p for section in ('kb', 'cases', 'handbook', 'plans', 'disease') for p in sorted((root / section).rglob('*.html'))
    ]

def collect_strings(root, dynamic_only=False):
    strings = set()
    for path in source_pages(root):
        collector = ProseCollector(dynamic_only and path.relative_to(root).parts[0] not in {'cases', 'plans'})
        collector.feed(path.read_text(encoding='utf-8'))
        strings.update(collector.strings)
    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key not in {'url', 'search_text', '_stub_reason', 'id', 'source_ids', 'icd10', 'icd_o_3_morphology'}:
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str) and prose(value):
            strings.add(normalize(value))
    for name in ('kb_search_index.json', 'questionnaires.json', 'handbook_index.json'):
        if (root / name).exists():
            visit(json.loads((root / name).read_text(encoding='utf-8')))
    for engine in (Path('knowledge_base/engine/render.py'), Path('serverless/clinical_question.py')):
        if engine.exists():
            tree = ast.parse(engine.read_text(encoding='utf-8'))
            # These dictionaries contain native curated copy, not English
            # source prose. Their values are preserved by load_catalog.
            tree.body = [node for node in tree.body if not (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in {'DISCLAIMER_TRANSLATIONS', 'ANSWER_LANGUAGES'} for target in node.targets))]
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value
                    if prose(value) and len(value) < 500 and not re.search(r'[{}<>;=]', value):
                        strings.add(normalize(value))
    return sorted(strings)

def numeric_tokens(text):
    """Check digits and explicit inequality signs before accepting a draft."""
    normalized = text.replace(',', '.').translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789'))
    return sorted(re.findall(r'\d+(?:[.,]\d+)?|[<>≤≥]', normalized))

def quantity_tokens(text):
    """Compare quantities with physical units, not just the set of digits."""
    normalized = text.replace(',', '.').replace('μ', 'µ').translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789'))
    quantities = re.findall(r'\d+(?:\.\d+)?\s*(?:µg|mg|mcg|g|mL|ml|mm|cm|Gy|mCi|GBq|IU)(?:/[A-Za-z0-9]+)?\b', normalized)
    return sorted(re.sub(r'\s+', '', value).lower() for value in quantities)


def polarity_tokens(text, locale='en'):
    """Conservative lexical check, not a claim of semantic equivalence."""
    plain = ''.join(c for c in unicodedata.normalize('NFKD', text.casefold()) if not unicodedata.combining(c))
    patterns = {
        'en': r'\b(?:no|not|never|without|avoid\w*|contraindicat\w*)\b',
        'es': r'\b(?:no|nunca|sin|evit\w*|contraindicad\w*)\b',
        'pt': r'\b(?:nao|nunca|sem|evit\w*|contraindicad\w*)\b',
        'de': r'\b(?:nicht|nie|kein\w*|ohne|vermeid\w*|kontraindiz\w*)\b',
        'fr': r'\b(?:pas|jamais|sans|evit\w*|contre-indiqu\w*)\b',
    }
    return (len(re.findall(patterns[locale], plain)), len(re.findall(r'\b(?:positiv\w*|positif\w*|positivity)\b', plain)), len(re.findall(r'\b(?:negativ\w*|negatif\w*|negativity)\b', plain)))


def load_catalog(locale, catalog_dir=None):
    from serverless.clinical_locale_messages import messages_for
    from scripts.clinical_curated_copy import messages_for as clinical_titles
    from serverless.clinical_question import DISCLAIMER_EN, DISCLAIMER_TRANSLATIONS
    path = (catalog_dir or CATALOG_DIR) / f'clinical.{locale}.json'
    catalog = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    if catalog:
        curated = messages_for(locale)
        curated.update(clinical_titles(locale))
        catalog.update(curated)
        catalog.update({value: value for value in curated.values()})
        catalog.update({normalize(value): normalize(value) for value in DISCLAIMER_TRANSLATIONS.values()})
        catalog[normalize(DISCLAIMER_EN)] = normalize(DISCLAIMER_TRANSLATIONS[locale])
    return catalog
