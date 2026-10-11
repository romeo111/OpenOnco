"""Scheduled publication must run the same artifact gates before pushing."""
from pathlib import Path

import yaml


def test_daily_refresh_checks_generated_artifacts_before_publishing():
    root = Path(__file__).resolve().parents[1]
    workflow = yaml.safe_load((root / '.github/workflows/daily-site-refresh.yml').read_text(encoding='utf-8'))
    steps = workflow['jobs']['refresh']['steps']
    build = next(i for i, step in enumerate(steps) if 'python -m scripts.build_site' in step.get('run', ''))
    push = next(i for i, step in enumerate(steps) if 'git push origin HEAD:master' in step.get('run', ''))
    for command in ('python -m scripts.audit_core_transport', 'node tests/browser_bundle_versions.cjs',
                    'node tests/browser_engine_loading.cjs', 'node tests/browser_report_export.cjs'):
        matches = [(i, step) for i, step in enumerate(steps) if command in step.get('run', '')]
        assert len(matches) == 1
        position, step = matches[0]
        assert build < position < push
        assert not step.get('continue-on-error')
        assert 'if' not in step
    notes = next(i for i, step in enumerate(steps) if '--check-note-drafts' in step.get('run', ''))
    assert notes < build


def test_daily_refresh_includes_new_files_and_reports_failure_honestly():
    root = Path(__file__).resolve().parents[1]
    workflow = yaml.safe_load((root / '.github/workflows/daily-site-refresh.yml').read_text(encoding='utf-8'))
    steps = workflow['jobs']['refresh']['steps']
    detection = next(step for step in steps if step.get('id') == 'diff')
    assert 'git status --porcelain --untracked-files=all -- docs/' in detection['run']
    summary = next(step for step in steps if step.get('name') == 'Summary')
    assert summary['env']['REFRESH_JOB_STATUS'] == '${{ job.status }}'
    assert summary['run'].index('!= "success"') < summary['run'].index('✓ Site refreshed')
