from scripts.audit_patient_localization import dynamic_inventory, drug_class_inventory


def test_dynamic_inventory_preserves_source_and_nested_field_locations(tmp_path):
    content = tmp_path / 'knowledge_base/hosted/content'
    file = content / 'regimens/example.yaml'
    file.parent.mkdir(parents=True)
    source = '''id: REG-EXAMPLE
names:
  ukrainian: Приклад
  english: Example
patient_watchpoints:
  - trigger_ua: Температура >38.5°C
    action_ua: Не чекати
    urgency: er_now
dose: 0.5 mg/kg
internal_note: Не перекладати в цьому переліку
'''
    file.write_text(source, encoding='utf-8')
    result = dynamic_inventory(tmp_path)
    assert result['entry_count'] == 3
    entries = result['entries']
    assert all(entry['entity_id'] == 'REG-EXAMPLE' for entry in entries)
    assert entries[1]['field_path'] == ['patient_watchpoints', '0', 'trigger_ua']
    assert entries[1]['source'] == 'Температура >38.5°C'
    assert entries[2]['source'] == 'Не чекати'
    assert file.read_text(encoding='utf-8') == source
    assert 'not displayed coverage' in result['scope']


def test_drug_inventory_keeps_authored_notes_separate_from_class_readiness(tmp_path):
    folder = tmp_path / 'knowledge_base/hosted/content/drugs'
    folder.mkdir(parents=True)
    source = '''id: DRUG-EXAMPLE
drug_class: Anthracycline (topoisomerase II inhibitor + DNA intercalator)
notes_patient: Не змінюйте дозу 0.5 mg.
'''
    file = folder / 'example.yaml'
    file.write_text(source, encoding='utf-8')
    (folder / 'unknown.yaml').write_text('id: DRUG-UNKNOWN\ndrug_class: Investigational combination\n', encoding='utf-8')
    classes = drug_class_inventory(tmp_path)
    assert classes['record_count'] == 2
    assert classes['en_class_explanation_draft_count'] == 1
    assert classes['authored_patient_note_count'] == 1
    assert classes['en_current_source_note_draft_count'] == 0
    assert classes['entries'][1]['en_class_explanation_draft'] is False
    notes = dynamic_inventory(tmp_path)
    assert notes['entries'][0]['field_path'] == ['notes_patient']
    assert notes['entries'][0]['source'] == 'Не змінюйте дозу 0.5 mg.'
    assert file.read_text(encoding='utf-8') == source
