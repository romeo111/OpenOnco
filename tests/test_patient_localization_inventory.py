from scripts.audit_patient_localization import dynamic_inventory


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
