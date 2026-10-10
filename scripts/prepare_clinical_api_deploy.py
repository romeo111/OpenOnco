"""Prepare the existing Vercel API project without publishing website/model files."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination):
    destination = destination.resolve()
    if not destination.is_relative_to(ROOT / '.tmp'):
        raise ValueError('Deployment staging must remain inside this repository .tmp')
    destination.mkdir(parents=True, exist_ok=True)
    for directory in ('api', 'serverless', 'knowledge_base'):
        for source in (ROOT / directory).rglob('*'):
            if source.is_file() and source.suffix in {'.py', '.yaml', '.yml', '.json'} and '__pycache__' not in source.parts and 'cache' not in source.parts:
                target = destination / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    (destination / 'requirements.txt').write_text('pydantic==2.13.3\nPyYAML==6.0.3\n', encoding='utf-8')
    config = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
    config['functions'] = {'api/*.py': {'includeFiles': 'knowledge_base/**'}}
    (destination / 'vercel.json').write_text(json.dumps(config, indent=2)+'\n', encoding='utf-8')
    return destination


if __name__ == '__main__':
    print(prepare(ROOT / '.tmp/clinical-api-deploy'))
