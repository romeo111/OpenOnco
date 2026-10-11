"""Progress reports completed rendering work without corrupting JSON stdout."""
import json

import pytest

from scripts import build_site as site


@pytest.mark.parametrize('progress', [False, True])
def test_case_progress_reports_completed_tasks_on_stderr(tmp_path, monkeypatch, capsys, progress):
    monkeypatch.setenv('OPENONCO_BUILD_WORKERS', '1')
    monkeypatch.setattr(site, '_public_case_entries', lambda: ['example'])
    monkeypatch.setattr(site, '_public_example_entries', lambda: ['example'])
    monkeypatch.setattr(site, '_build_one_case_worker', lambda task: {'lang': task[2], 'path': 'synthetic.html'})
    result = site._build_all_cases_parallel(tmp_path, progress=progress)
    assert [len(group) for group in result] == [1, 1, 1]
    captured = capsys.readouterr()
    assert captured.out == ''
    if progress:
        assert 'Rendered case tasks: 3/3' in captured.err
    else:
        assert captured.err == ''


def test_failed_case_is_not_reported_as_completed(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('OPENONCO_BUILD_WORKERS', '1')
    monkeypatch.setattr(site, '_public_case_entries', lambda: ['example'])
    monkeypatch.setattr(site, '_public_example_entries', lambda: [])
    def fail(task):
        if task[2] == 'en':
            raise RuntimeError('render failed')
        return {'lang': task[2], 'path': 'synthetic.html'}
    monkeypatch.setattr(site, '_build_one_case_worker', fail)
    with pytest.raises(RuntimeError, match='render failed'):
        site._build_all_cases_parallel(tmp_path, progress=True)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert '1/2' in captured.err
    assert '2/2' not in captured.err


def test_cli_progress_preserves_machine_readable_json(tmp_path, monkeypatch, capsys):
    def build(output_dir, *, progress=False):
        assert output_dir == tmp_path
        assert progress is True
        print('[build] completed', file=site.sys.stderr)
        return {'status': 'ok', 'cases_built': 3}

    monkeypatch.setattr(site, 'build_site', build)
    assert site.main(['--output', str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {'status': 'ok', 'cases_built': 3}
    assert captured.err == '[build] completed\n'
