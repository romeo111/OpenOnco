import os
from pathlib import Path
os.environ['HF_HOME'] = str(Path('.tmp/huggingface').resolve())
os.environ['HF_HUB_DISABLE_XET'] = '1'
from huggingface_hub import snapshot_download
from ctranslate2.converters import TransformersConverter

models = {
    'romance': ('Helsinki-NLP/opus-mt-en-ROMANCE', 'f8f3a28e8b6272d0ccc0290b832f699e154ae431'),
    'de': ('Helsinki-NLP/opus-mt-en-de', '6183067f769a302e3861815543b9f312c71b0ca4'),
}
for name, (repo, revision) in models.items():
    target = Path('.tmp/translation-models') / name
    if (target / 'model.bin').exists():
        continue
    source = snapshot_download(repo, revision=revision, allow_patterns=['config.json','generation_config.json','pytorch_model.bin','source.spm','target.spm','tokenizer_config.json','vocab.json'])
    print('Downloaded', name, flush=True)
    TransformersConverter(source).convert(str(target), quantization='int8', force=True)
    (target / 'tokenizer-path.txt').write_text(source, encoding='utf-8')
    print('Converted', name, flush=True)
