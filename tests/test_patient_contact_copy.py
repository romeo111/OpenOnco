"""Native display headings retain distinct contact timing and canonical aliases."""
import json
import re
from pathlib import Path

import pytest

from scripts.patient_contact_copy import HEADINGS, SOURCES, messages_for
from scripts.clinical_curated_copy import messages_for as curated_messages
from scripts.clinical_translation_checks import acceptable_draft


@pytest.mark.parametrize('locale', HEADINGS)
def test_contact_timing_and_action_remain_distinct_in_all_catalogs(locale):
    messages = messages_for(locale)
    assert len(set(HEADINGS[locale])) == 5
    assert len(messages) == 10
    curated = curated_messages(locale)
    for aliases, native in zip(SOURCES, HEADINGS[locale], strict=True):
        for source in aliases:
            assert messages[source] == curated[source] == native
        assert acceptable_draft(aliases[0], native, locale)


def test_dynamic_overrides_match_static_curated_copy_before_native_identity_set():
    source = (Path(__file__).resolve().parents[1] / 'scripts/clinical-localization.js').read_text(encoding='utf-8')
    embedded = json.loads(re.search(r'const patientContactCopy = (.*);', source)[1])
    assert embedded == {locale: messages_for(locale) for locale in HEADINGS}
    assert source.index('Object.assign(catalog, patientContactCopy') < source.index('const nativeValues =')
