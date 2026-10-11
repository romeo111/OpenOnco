"""Author additional interface drafts locally; stage outputs, never publish directly.

No model or translation request runs on page visits. Source clinical data is
read-only. Draft guards preserve numbers, quantities, identifiers and polarity;
they do not establish clinical or linguistic validation.
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.additional_locale_copy import ADDITIONAL_LANGUAGES, CURATED_SITE_FIELDS, ENGLISH_COPY, NAVIGATION, NAVIGATION_KEYS
from scripts.clinical_curated_copy import UI_MESSAGES
from scripts.clinical_translation_checks import acceptable_draft
from scripts.site_translation_catalog import ProseCollector, normalize
from serverless.clinical_locale_messages import MESSAGES

# Authoring needs public display literals, not the medical engine's runtime.
_disclaimer_tree = ast.parse((ROOT / 'serverless/clinical_question.py').read_text(encoding='utf-8'))
_disclaimers = {
    target.id: ast.literal_eval(node.value)
    for node in _disclaimer_tree.body if isinstance(node, ast.Assign)
    for target in node.targets if isinstance(target, ast.Name)
    and target.id in {'DISCLAIMER_EN', 'DISCLAIMER_TRANSLATIONS'}
}
DISCLAIMER_EN = _disclaimers['DISCLAIMER_EN']
DISCLAIMER_TRANSLATIONS = _disclaimers['DISCLAIMER_TRANSLATIONS']


def interface_sources(site):
    strings = set(ENGLISH_COPY.values()) | set(UI_MESSAGES) | set(MESSAGES)
    for filename in ('index.html', 'about.html', 'capabilities.html', 'specs.html',
                     'news.html', 'participate.html', 'try.html', 'ask.html',
                     'prevent.html', 'diseases.html', 'gallery.html', 'handbook.html', 'kb.html'):
        path = site / filename
        if path.exists():
            collector = ProseCollector()
            collector.feed(path.read_text(encoding='utf-8'))
            strings.update(collector.strings)
    strings.add(normalize(DISCLAIMER_EN))
    return sorted(strings)


def drug_pattern_from_site(site):
    entries = json.loads((site / 'kb_search_index.json').read_text(encoding='utf-8'))['entries']
    names = sorted({row['title'] for row in entries if row.get('kind_key') == 'drugs' and len(row['title']) < 70}, key=len, reverse=True)
    return re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(name) for name in names) + r')(?!\w)', re.I) if names else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('locale', choices=ADDITIONAL_LANGUAGES)
    parser.add_argument('--output-dir', type=Path, default=ROOT / '.tmp/additional-locale-drafts')
    args = parser.parse_args()
    import ctranslate2
    from transformers import MarianTokenizer

    code = args.locale
    model_name = 'gmq' if code in ('da', 'sv', 'nb') else 'fi' if code == 'fi' else 'romance'
    model = ROOT / '.tmp/translation-models' / model_name
    tokenizer = MarianTokenizer.from_pretrained((model / 'tokenizer-path.txt').read_text(encoding='utf-8').strip())
    translator = ctranslate2.Translator(str(model), device='cpu', compute_type='int8', inter_threads=1, intra_threads=1)
    prefix = {'it': '>>it<< ', 'da': '>>dan<< ', 'sv': '>>swe<< ', 'nb': '>>nob<< ', 'fi': ''}[code]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f'clinical.{code}.json'
    catalog = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    sources = interface_sources(ROOT / 'docs')
    pending = [source for source in sources if source not in catalog]
    drug_pattern = drug_pattern_from_site(ROOT / 'docs')
    print(code, len(pending), 'pending interface strings', flush=True)
    for offset in range(0, len(pending), 32):
        batch = pending[offset:offset + 32]
        # Preserve complete conditions; long prose is retained until the full
        # clinical-corpus authoring pass can split at sentence boundaries.
        short = [source for source in batch if len(source) <= 500]
        tokens = [tokenizer.convert_ids_to_tokens(tokenizer.encode(prefix + source)) for source in short]
        results = translator.translate_batch(tokens, beam_size=1, max_batch_size=1024, batch_type='tokens', max_decoding_length=256, no_repeat_ngram_size=3) if tokens else []
        for source, result in zip(short, results):
            translated = tokenizer.decode(tokenizer.convert_tokens_to_ids(result.hypotheses[0]), skip_special_tokens=True).strip()
            catalog[source] = translated if acceptable_draft(source, translated, code, drug_pattern) else source
        for source in batch:
            catalog.setdefault(source, source)
        temporary = target.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        temporary.replace(target)
        print(code, offset + len(batch), '/', len(pending), flush=True)
    catalog[normalize(DISCLAIMER_EN)] = normalize(DISCLAIMER_TRANSLATIONS[code])
    catalog.update({ENGLISH_COPY[key]: value for key, value in CURATED_SITE_FIELDS[code].items()})
    target.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    site_copy = {key: catalog.get(value, value) for key, value in ENGLISH_COPY.items()}
    site_copy.update(dict(zip(NAVIGATION_KEYS, NAVIGATION[code])))
    site_copy.update(CURATED_SITE_FIELDS[code])
    (args.output_dir / f'site.{code}.json').write_text(json.dumps(site_copy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    curated = {source: catalog.get(source, source) for source in UI_MESSAGES}
    (args.output_dir / f'curated.{code}.json').write_text(json.dumps(curated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(code, 'interface draft staged; review pending; originals retained:', sum(catalog[source] == source for source in sources), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
