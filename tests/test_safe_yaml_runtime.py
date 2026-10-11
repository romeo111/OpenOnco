"""Compiled YAML parsing preserves safe construction and engine inputs."""

from datetime import date

import pytest
import yaml

from knowledge_base.validation.loader import _SAFE_YAML_LOADER


def test_compiled_parser_preserves_clinical_values():
    text = """
id: IND-TEST
review_date: 2026-10-11
dose: 1.5
threshold: 30
enabled: false
name: 'лікування · traitement'
defaults: &defaults
  drug_id: DRUG-ONE
  unit: mg/m²
schedule:
  - <<: *defaults
    days: [1, 8, 15]
    note: 'QTc >480 → caution'
"""
    actual = yaml.load(text, Loader=_SAFE_YAML_LOADER)
    assert actual == yaml.load(text, Loader=yaml.SafeLoader)
    assert actual['review_date'] == date(2026, 10, 11)
    assert actual['enabled'] is False
    assert actual['schedule'][0]['days'] == [1, 8, 15]


@pytest.mark.parametrize('loader', [_SAFE_YAML_LOADER, yaml.SafeLoader])
def test_yaml_parser_rejects_python_object_construction(loader):
    with pytest.raises(yaml.constructor.ConstructorError):
        yaml.load('!!python/object/apply:builtins.str [unsafe]', Loader=loader)
