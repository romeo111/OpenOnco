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


def dynamic_inventory(root: Path) -> dict:
    """Candidate patient-facing KB text; not proof that every field is displayed."""
    import yaml

    entries = []
    content = root / 'knowledge_base/hosted/content'
    fields = {'definition_ua', 'trigger_ua', 'action_ua', 'notes_patient'}

    def visit(value, path, filename, entity_id):
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = [*path, str(key)]
                selected = key in fields or (
                    key == 'ukrainian' and path and path[-1] == 'names'
                )
                if selected and isinstance(child, str) and child.strip():
                    entries.append({
                        'file': filename, 'entity_id': entity_id,
                        'field_path': child_path, 'source': child,
                    })
                else:
                    visit(child, child_path, filename, entity_id)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, [*path, str(index)], filename, entity_id)

    loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
    for category in ('diseases', 'drugs', 'redflags', 'regimens'):
        for file in sorted((content / category).glob('*.yaml')):
            record = yaml.load(file.read_text(encoding='utf-8'), Loader=loader)
            entity_id = record.get('id') if isinstance(record, dict) else None
            visit(record, [], file.relative_to(root).as_posix(), entity_id)
    return {
        'status': 'inventory_only_not_clinical_review',
        'scope': 'Candidate YAML names, authored patient notes, red-flag definitions and watchpoints; not displayed coverage',
        'entry_count': len(entries),
        'unique_source_count': len({entry['source'] for entry in entries}),
        'entries': entries,
    }


def drug_class_inventory(root: Path) -> dict:
    """Record lookup readiness, not rendered coverage or clinical signoff."""
    import yaml
    from knowledge_base.engine._patient_vocabulary import explain_drug_class
    from knowledge_base.engine._patient_note_translations import translate_patient_note

    entries = []
    loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
    for file in sorted((root / 'knowledge_base/hosted/content/drugs').glob('*.yaml')):
        record = yaml.load(file.read_text(encoding='utf-8'), Loader=loader)
        if not isinstance(record, dict):
            continue
        label = record.get('drug_class') or ''
        entries.append({
            'file': str(file.relative_to(root)).replace('\\', '/'),
            'entity_id': record.get('id'), 'drug_class': label,
            'uk_class_explanation': bool(explain_drug_class(label)),
            'en_class_explanation_draft': bool(explain_drug_class(label, target_lang='en')),
            'has_authored_patient_note': bool((record.get('notes_patient') or '').strip()),
            'en_current_source_note_draft': bool(translate_patient_note(record.get('id'), record.get('notes_patient') or '')),
        })
    return {
        'status': 'lookup_inventory_not_clinical_review',
        'scope': 'Drug-class lookup readiness only; authored-note translation and displayed report coverage are not proven',
        'record_count': len(entries),
        'uk_class_explanation_count': sum(item['uk_class_explanation'] for item in entries),
        'en_class_explanation_draft_count': sum(item['en_class_explanation_draft'] for item in entries),
        'authored_patient_note_count': sum(item['has_authored_patient_note'] for item in entries),
        'en_current_source_note_draft_count': sum(item['en_current_source_note_draft'] for item in entries),
        'entries': entries,
    }


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
    parser.add_argument('--include-dynamic', action='store_true', help='Include a separate candidate YAML text inventory')
    parser.add_argument('--include-drug-classes', action='store_true', help='Include drug-class lookup readiness and authored-note presence')
    args = parser.parse_args()
    result = inventory(args.root)
    if args.include_dynamic:
        result['dynamic_content'] = dynamic_inventory(args.root)
    if args.include_drug_classes:
        result['drug_classes'] = drug_class_inventory(args.root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {key: value for key, value in result.items() if key != 'entries'}
    for section in ('dynamic_content', 'drug_classes'):
        if section in summary:
            summary[section] = {key: value for key, value in summary[section].items() if key != 'entries'}
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
