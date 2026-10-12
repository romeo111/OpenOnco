import pytest
from scripts.clinical_translation_checks import acceptable_draft
from scripts.clinical_curated_copy import AVAILABILITY_LABELS, STAGING_LABELS, messages_for


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
