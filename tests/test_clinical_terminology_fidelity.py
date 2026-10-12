import pytest
from scripts.clinical_translation_checks import acceptable_draft
from scripts.clinical_curated_copy import AVAILABILITY_LABELS, STAGING_LABELS, messages_for


@pytest.mark.parametrize('locale,period,counts', [
    ('es', 'al día', ['una vez', 'dos veces', 'tres veces']),
    ('pt', 'ao dia', ['uma vez', 'duas vezes', 'três vezes']),
    ('de', 'täglich', ['einmal', 'zweimal', 'dreimal']),
    ('fr', 'par jour', ['une fois', 'deux fois', 'trois fois']),
    ('it', 'al giorno', ['una volta', 'due volte', 'tre volte']),
    ('da', 'dagligt', ['en gang', 'to gange', 'tre gange']),
    ('sv', 'dagligen', ['en gång', 'två gånger', 'tre gånger']),
    ('nb', 'daglig', ['en gang', 'to ganger', 'tre ganger']),
    ('fi', 'päivässä', ['kerran', 'kahdesti', 'kolmesti']),
])
def test_explicit_frequency_is_preserved_for_every_edition(locale, period, counts):
    weekly = {'es': 'semanalmente', 'pt': 'semanalmente', 'de': 'wöchentlich',
              'fr': 'hebdomadaire', 'it': 'settimanale', 'da': 'ugentligt',
              'sv': 'varje vecka', 'nb': 'ukentlig', 'fi': 'viikoittain'}[locale]
    for index, source_count in enumerate(['once', 'twice', 'three times']):
        source = f'100 mg {source_count} daily'
        assert acceptable_draft(source, f'100 mg {counts[index]} {period}', locale)
        assert not acceptable_draft(source, f'100 mg {period}', locale)
        assert not acceptable_draft(source, f'100 mg {counts[(index + 1) % 3]} {period}', locale)
        assert acceptable_draft(source, source, locale)
        assert acceptable_draft(f'100 mg {source_count} weekly', f'100 mg {counts[index]} {weekly}', locale)
        assert not acceptable_draft(f'100 mg {source_count} weekly', f'100 mg {counts[(index + 1) % 3]} {weekly}', locale)
    assert not acceptable_draft('100 mg daily', f'100 mg {counts[1]} {period}', locale)
    assert not acceptable_draft('100 mg once daily; 100 mg once daily',
                                f'100 mg {counts[0]} {period}; 100 mg {counts[1]} {period}', locale)
    assert not acceptable_draft('100 mg once daily; 200 mg twice daily',
                                f'100 mg {counts[1]} {period}; 200 mg {counts[0]} {period}', locale)


def test_mixed_periods_retain_original_until_clause_alignment_is_verified():
    from scripts.clinical_translation_checks import schedule_fidelity
    source = '100 mg once daily; 100 mg twice weekly'
    assert not schedule_fidelity(source, '100 mg deux fois par jour; 100 mg une fois hebdomadaire', 'fr')
    assert schedule_fidelity(source, source, 'fr')


@pytest.mark.parametrize('locale,daily,weekly', [
    ('es', '100 mg al día', '100 mg semanalmente'),
    ('pt', '100 mg ao dia', '100 mg semanalmente'),
    ('de', '100 mg täglich', '100 mg wöchentlich'),
    ('fr', '100 mg par jour', '100 mg hebdomadaire'),
    ('it', '100 mg al giorno', '100 mg settimanale'),
    ('da', '100 mg dagligt', '100 mg ugentligt'),
    ('sv', '100 mg dagligen', '100 mg varje vecka'),
    ('nb', '100 mg daglig', '100 mg ukentlig'),
    ('fi', '100 mg päivittäin', '100 mg viikoittain'),
])
def test_schedule_cannot_disappear_or_reverse_in_any_clinical_edition(locale, daily, weekly):
    assert acceptable_draft('100 mg daily', daily, locale)
    assert acceptable_draft('100 mg weekly', weekly, locale)
    assert not acceptable_draft('100 mg daily', '100 mg', locale)
    assert not acceptable_draft('100 mg weekly', '100 mg', locale)
    assert not acceptable_draft('100 mg daily', weekly, locale)
    assert not acceptable_draft('100 mg weekly', daily, locale)
    assert not acceptable_draft('100 mg weekly', daily + '; ' + weekly, locale)
    assert acceptable_draft('100 mg weekly', '100 mg weekly', locale)


@pytest.mark.parametrize('source,wrong', [
    ('Tucatinib + Trastuzumab (MOUNTAINEER, HER2+ RAS-WT mCRC)', 'Tucatinib + Trastuzumab (MONTAINER, HER2+ RAS-WT mCRC)'),
    ('Trifluridine-Tipiracil + Bevacizumab (SUNLIGHT)', 'Trifluridine-Tipiracil + Bevacizumab (LUMIÈRE DE SOL)'),
])
def test_trial_names_are_identifiers_not_translatable_prose(source, wrong):
    assert not acceptable_draft(source, wrong, 'fr')
    assert acceptable_draft(source, source, 'fr')


@pytest.mark.parametrize('locale', AVAILABILITY_LABELS)
def test_availability_label_retains_ukraine_for_every_edition(locale):
    assert messages_for(locale)['✗ Not registered in UA'] == AVAILABILITY_LABELS[locale]
    assert 'VAE' not in messages_for(locale)['✗ Not registered in UA']
    assert acceptable_draft('✗ Not registered in UA', AVAILABILITY_LABELS[locale], locale)
    assert not acceptable_draft('✗ Not registered in UA', 'Registered in UAE', locale)


@pytest.mark.parametrize('locale,wrong', [('it','Stagione'),('da','Etage'),('sv','Iscensättning'),('nb','Igangsetting'),('fi','Paikannus')])
def test_staging_labels_cannot_revert_to_floor_season_or_theatre(locale, wrong):
    for source, expected in STAGING_LABELS[locale].items():
        assert messages_for(locale)[source] == expected
        assert acceptable_draft(source, expected, locale)
        assert not acceptable_draft(source, wrong, locale)
