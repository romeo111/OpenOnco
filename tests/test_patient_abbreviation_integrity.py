from knowledge_base.engine._patient_vocabulary import expand_first_use


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
