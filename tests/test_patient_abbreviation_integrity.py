from knowledge_base.engine._patient_vocabulary import expand_first_use
from knowledge_base.engine._patient_vocabulary import (
    ABBREVIATION_FIRST_USE_EN, ABBREVIATION_FIRST_USE_UA,
    ABBREVIATION_TRANSLATION_STATUS,
)
import pytest


def test_abbreviation_expansion_preserves_html_metadata_and_original_sources():
    protected = '''<head><title>FDA</title><style>.FDA {color:red}</style></head>
<!-- FDA source -->
<script>const label = "FDA";</script>
<details data-original-source><summary>FDA publication</summary><a href="https://example.org/FDA">FDA original title</a></details>
<code>FDA</code>'''
    link = '<a href="https://example.org/FDA" data-id="FDA" title="FDA">FDA</a>'
    output = expand_first_use(protected + '\n' + link + '<p>FDA again; dose 0.5 mg/kg &amp; threshold &lt;38.5°C.</p>')
    assert output.startswith(protected)
    assert '<a href="https://example.org/FDA" data-id="FDA" title="FDA">FDA (' in output
    assert '<p>FDA again; dose 0.5 mg/kg &amp; threshold &lt;38.5°C.</p>' in output
    assert output.count('FDA (') == 1
    assert expand_first_use(output) == output


def test_english_first_use_glossary_is_complete_and_keeps_source_markup():
    assert ABBREVIATION_FIRST_USE_EN.keys() == ABBREVIATION_FIRST_USE_UA.keys()
    assert ABBREVIATION_TRANSLATION_STATUS['en'] == 'draft_pending_review'
    original = '<details data-original-source>FDA publication</details>'
    sample = original + '<p>FDA and ECOG; dose 0.5 mg/kg. FDA again.</p>'
    result = expand_first_use(sample, target_lang='en')
    assert result.startswith(original)
    assert 'FDA (the US Food and Drug Administration)' in result
    assert 'daily activities' in result
    assert 'dose 0.5 mg/kg. FDA again.' in result
    assert expand_first_use(result, target_lang='en') == result


def test_unavailable_glossary_language_is_not_silently_ukrainian():
    with pytest.raises(ValueError, match='only in Ukrainian'):
        expand_first_use('<p>FDA</p>', target_lang='fr')


@pytest.mark.parametrize('language,glossary', [('uk', ABBREVIATION_FIRST_USE_UA), ('en', ABBREVIATION_FIRST_USE_EN)])
def test_infection_glosses_preserve_identifiers_sources_and_negative_results(language, glossary):
    source = '<details data-original-source><a href="https://example.org/EBV">EBV original publication</a></details>'
    content = '<p data-source-id="RF-HIV">HIV negative; EBV not detected; CMV &lt;0.5.</p><p>HIV, EBV and CMV again.</p>'
    output = expand_first_use(source + content, target_lang=language)
    assert output.startswith(source)
    assert 'data-source-id="RF-HIV"' in output
    assert glossary['HIV'] + ' negative' in output
    assert glossary['EBV'] + ' not detected' in output
    assert glossary['CMV'] + ' &lt;0.5' in output
    assert '<p>HIV, EBV and CMV again.</p>' in output
    assert expand_first_use(output, target_lang=language) == output
