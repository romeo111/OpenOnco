from scripts.restore_clinical_fragments import restore_original_fragments


def test_restores_visible_text_entities_and_accessible_labels_only():
    source = '''<html lang="es"><p id="dose" title="100 mg dos veces al día"> 100 mg dos veces al d&#237;a </p>
<script>const dose="100 mg dos veces al día";</script><input value="100 mg dos veces al día">
<code>100 mg dos veces al día</code><!--100 mg dos veces al día--></html>'''
    result, count = restore_original_fragments(source, {'100 mg dos veces al día': '100 mg once daily'}, 'Original')
    assert count == 2
    assert 'lang="en" data-original-source' in result
    assert 'title="100 mg once daily"' in result
    assert '<script>const dose="100 mg dos veces al día";</script>' in result
    assert '<input value="100 mg dos veces al día">' in result
    assert '<code>100 mg dos veces al día</code>' in result
    assert '<!--100 mg dos veces al día-->' in result
    assert '<p id="dose"' in result
    assert restore_original_fragments(result, {'100 mg dos veces al día': '100 mg once daily'}, 'Original') == (result, 0)


def test_source_markup_is_escaped_and_unmatched_nested_text_is_not_guessed():
    source = '<p>Wrong &amp; text</p><p>Wrong <strong>&amp; text</strong></p>'
    result, count = restore_original_fragments(source, {'Wrong & text': 'Original < 5 mg & unchanged'}, 'Original')
    assert count == 1
    assert 'Original &lt; 5 mg &amp; unchanged' in result
    assert '<p>Wrong <strong>&amp; text</strong></p>' in result


def test_title_and_option_remain_plain_text_and_machine_attributes_stay_intact():
    source = '<title>Wrong</title><select><option value="REG-ID" data-dose="100">Wrong</option></select>'
    result, count = restore_original_fragments(source, {'Wrong': 'Original'}, 'Original')
    assert count == 2
    assert result == '<title>Original</title><select><option value="REG-ID" data-dose="100">Original</option></select>'


def test_attribute_names_and_quoted_input_values_are_not_misread_as_display_labels():
    source = '''<input data-title="Wrong" value='title="Wrong"' aria-label=Wrong>'''
    result, count = restore_original_fragments(source, {'Wrong': 'Original text'}, 'Original')
    assert count == 1
    assert result == '''<input data-title="Wrong" value='title="Wrong"' aria-label="Original text">'''


def test_svg_text_remains_svg_text():
    source = '<svg><text>Wrong</text></svg>'
    assert restore_original_fragments(source, {'Wrong': 'Original'}, 'Original') == ('<svg><text>Original</text></svg>', 1)
