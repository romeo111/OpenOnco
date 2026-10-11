"""Inventory authored patient copy before translating it; never modify clinical data.

This inventory covers Python-authored copy, not Ukrainian fields loaded from YAML.
Dynamic disease/drug labels, red-flag definitions and watchpoints need a separate
content audit. Counts are translation work estimates, not language-coverage claims.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


FILES = (
    'knowledge_base/engine/render.py',
    'knowledge_base/engine/_patient_vocabulary.py',
    'knowledge_base/engine/_patient_rationale.py',
    'knowledge_base/engine/_emergency_rf.py',
    'knowledge_base/engine/_ask_doctor.py',
)
CYRILLIC = re.compile(r'[\u0400-\u04ff]')


def inventory(root: Path) -> dict:
    entries = []
    for filename in FILES:
        source = (root / filename).read_text(encoding='utf-8')
        tree = ast.parse(source)
        nodes = list(ast.walk(tree))
        parents = {id(child): parent for parent in nodes for child in ast.iter_child_nodes(parent)}
        docstrings = {
            id(node.body[0].value)
            for node in nodes
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.body and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        }
        lower, upper = 0, len(source.splitlines())
        if filename.endswith('/render.py'):
            lower = next(node.lineno for node in tree.body if getattr(node, 'name', '') == '_patient_doc_shell')
            upper = next(node.end_lineno for node in tree.body if getattr(node, 'name', '') == '_render_patient_mode')
        for node in nodes:
            if not lower <= getattr(node, 'lineno', -1) <= upper or id(node) in docstrings:
                continue
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if isinstance(parents.get(id(node)), ast.JoinedStr):
                    continue
                text, kind = node.value, 'literal'
            elif isinstance(node, ast.JoinedStr):
                text, kind = ast.get_source_segment(source, node), 'template'
            else:
                continue
            if text and CYRILLIC.search(text):
                entries.append({'file': filename, 'line': node.lineno, 'kind': kind, 'source': text})
    entries.sort(key=lambda item: (item['file'], item['line']))
    return {
        'status': 'inventory_only_not_clinical_review',
        'scope': 'Python-authored patient copy; dynamic YAML content is not included',
        'entry_count': len(entries),
        'unique_source_count': len({entry['source'] for entry in entries}),
        'by_file': {filename: sum(entry['file'] == filename for entry in entries) for filename in FILES},
        'entries': entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, help='Optional JSON review inventory; clinical inputs are untouched')
    args = parser.parse_args()
    result = inventory(args.root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'entries'}, indent=2))


if __name__ == '__main__':
    main()
