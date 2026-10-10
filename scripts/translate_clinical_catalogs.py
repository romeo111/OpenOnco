"""Generate offline display drafts into a separate staging directory.
Run from repository root after scripts/prepare_translation_models.py.
Original catalogs are read-only. Publication requires separate verification.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.clinical_translation_checks import acceptable_draft
from scripts.clinical_curated_copy import diagnostic_display

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('locale', choices=('es', 'pt', 'de', 'fr'))
parser.add_argument('corpus', type=Path)
parser.add_argument('--output-dir', type=Path, default=Path('.tmp/clinical-next'))
args = parser.parse_args()

# Authoring-only dependencies; no browser/server build imports these modules.
import ctranslate2
from transformers import MarianTokenizer

sources = json.loads(args.corpus.read_text(encoding='utf-8'))
locale = args.locale
model = Path('.tmp/translation-models') / ('de' if locale == 'de' else 'romance')
tokenizer = MarianTokenizer.from_pretrained((model / 'tokenizer-path.txt').read_text(encoding='utf-8'))
translator = ctranslate2.Translator(str(model), device='cpu', compute_type='int8', inter_threads=1, intra_threads=1)
index = json.loads(Path('docs/kb_search_index.json').read_text(encoding='utf-8'))
drug_names = sorted({e['title'] for e in index['entries'] if e.get('kind_key') == 'drugs' and len(e['title']) < 70}, key=len, reverse=True)
drug_pattern = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(n) for n in drug_names) + r')(?!\w)', re.I)
baseline_path = Path('scripts/locales') / f'clinical.{locale}.json'
baseline = json.loads(baseline_path.read_text(encoding='utf-8')) if baseline_path.exists() else {}
args.output_dir.mkdir(parents=True, exist_ok=True)
target = args.output_dir / f'clinical.{locale}.json'
catalog = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {
    source: value for source, value in baseline.items()
    if len(source) <= 180 and acceptable_draft(source, value, locale, drug_pattern)
}
for source in sources:
    diagnostic = diagnostic_display(source, locale)
    if diagnostic is not None:
        catalog[source] = diagnostic
pending = [s for s in sources if s not in catalog]
prefix = '' if locale == 'de' else f'>>{locale}<< '
print(locale, 'pending', len(pending), 'staging', target, flush=True)

def translate_batch(strings):
    counts = []
    flattened = []
    for value in strings:
        chunks = []
        while len(value) > 500:
            end = value.rfind('. ', 0, 500)
            end = end + 2 if end > 150 else value.rfind(' ', 0, 500)
            end = end if end > 0 else 500
            chunks.append(value[:end])
            value = value[end:].lstrip()
        chunks.append(value)
        counts.append(len(chunks))
        flattened.extend(chunks)
    tokens = [tokenizer.convert_ids_to_tokens(tokenizer.encode(prefix + s)) for s in flattened]
    results = translator.translate_batch(tokens, beam_size=1, max_batch_size=2048, batch_type='tokens', max_decoding_length=256, no_repeat_ngram_size=3)
    values = [
        tokenizer.decode(tokenizer.convert_tokens_to_ids(r.hypotheses[0]), skip_special_tokens=True).strip() for r in results
    ]
    combined, cursor = [], 0
    for count in counts:
        combined.append(' '.join(values[cursor:cursor+count]))
        cursor += count
    return combined

start = time.monotonic()

def save_catalog():
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    temporary.replace(target)


for offset in range(0, len(pending), 64):
    batch = pending[offset:offset+64]
    values = translate_batch(batch)
    for source, value in zip(batch, values):
        # Do not assemble translations around isolated dose fragments:
        # losing a surrounding condition is worse than retaining the source.
        catalog[source] = value if acceptable_draft(source, value, locale, drug_pattern) else source
    if offset % 256 == 0 or offset+64 >= len(pending):
        save_catalog()
        print(locale, offset+len(batch), '/', len(pending), 'seconds', round(time.monotonic()-start), flush=True)

# Preserve keys from previous work even when the source page has since changed.
for source, value in baseline.items():
    if source not in catalog:
        catalog[source] = value if acceptable_draft(source, value, locale, drug_pattern) else source
assert set(baseline) <= set(catalog)
assert all(s in catalog for s in sources)
save_catalog()
summary = {
    'locale': locale, 'strings': len(catalog), 'source_strings': len(sources),
    'changed_strings': sum(catalog[s] != s for s in sources),
    'review': 'pending_clinical_review',
}
(target.with_suffix('.summary.json')).write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
print(summary, flush=True)
