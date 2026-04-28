"""Tests for scripts.tasktorrent.next_chunk."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.tasktorrent.next_chunk import (
    ChunkInfo,
    all_inline_codes,
    count_machine_acceptance,
    first_fenced_block,
    first_inline_code,
    first_url,
    main,
    parse_drop_estimate,
    parse_issue,
    parse_manifest,
    parse_sections,
)


# ---------- Real-issue fixture (shape from issue #26 trial-source-ingest-pubmed) ----------

REAL_ISSUE_BODY = """## Chunk Spec

Full spec: https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/trial-source-ingest-pubmed.md

## Chunk ID

`trial-source-ingest-pubmed`

## Topic Labels

`source-ingest`, `metadata-classification`, `pubmed-fetch`

## Drop Estimate

~3 Drops (~300k tokens). 47 candidate trials × ~6k tokens each.

## Required Skill

`citation-verification` (license classification + metadata extraction).

## Branch Naming Convention

`tasktorrent/trial-source-ingest-pubmed`

## Sidecar Output Path

```
contributions/trial-source-ingest-pubmed/
```

## Claim Method

`formal-issue` — comment to claim, maintainer assigns within 24h SLA.

## Task Manifest

48 candidate trial names from the v2 audit.

```
CROSS, PARADIGM, RUBY, NRG-GY018, PAOLA-1, AIDA, CODEBREAK
```

## Allowed Sources

PubMed E-utilities.

## Acceptance Criteria (machine-checkable)

- [ ] Every sidecar has `_contribution.ai_tool` and `_contribution.ai_model` set.
- [ ] PR branch name matches `tasktorrent/trial-source-ingest-pubmed`.
- [ ] `task_manifest.txt` contains the 48 trial names.

## Acceptance Criteria (semantic, maintainer-checked)

- [ ] False-positive filter ≥ 90% accurate.
"""


def make_issue(**overrides) -> dict:
    base = {
        "number": 26,
        "title": "[Chunk] trial-source-ingest-pubmed",
        "body": REAL_ISSUE_BODY,
        "assignees": [],
        "labels": [{"name": "chunk-task"}, {"name": "status-active"}],
        "createdAt": "2026-04-28T18:00:00Z",
        "url": "https://github.com/romeo111/OpenOnco/issues/26",
    }
    base.update(overrides)
    return base


# ---------- Section + helper unit tests ----------

def test_parse_sections_simple() -> None:
    md = "Pre.\n\n## A\n\nA-body\n\n## B\n\nB-body line\n"
    secs = parse_sections(md)
    assert secs == {"A": "A-body", "B": "B-body line"}


def test_first_inline_code_strips_backticks() -> None:
    assert first_inline_code("`formal-issue`") == "formal-issue"
    assert first_inline_code("Some prose then `value` then more.") == "value"


def test_first_inline_code_returns_none_when_absent() -> None:
    assert first_inline_code("plain prose, no code") is None


def test_first_url_strips_trailing_punct() -> None:
    assert first_url("see https://example.com/x.md.") == "https://example.com/x.md"
    assert first_url("link: (https://example.com/y)") == "https://example.com/y"


def test_first_fenced_block_yaml_or_plain() -> None:
    text = "prose\n```\nline1\nline2\n```\nmore"
    assert first_fenced_block(text) == "line1\nline2"
    text2 = "prose\n```yaml\nfoo: 1\n```\nmore"
    assert first_fenced_block(text2) == "foo: 1"


def test_all_inline_codes_collects_all() -> None:
    assert all_inline_codes("`a`, `b`, `c`") == ["a", "b", "c"]


def test_parse_drop_estimate_tokens_priority() -> None:
    text, tok = parse_drop_estimate("~3 Drops (~300k tokens). lots of detail.")
    assert "300k" in text or "Drops" in text
    assert tok == 300_000


def test_parse_drop_estimate_drops_fallback() -> None:
    _, tok = parse_drop_estimate("~5 Drops, no token figure")
    assert tok == 500_000


def test_parse_drop_estimate_neither() -> None:
    raw, tok = parse_drop_estimate("vaguely large work")
    assert raw == "vaguely large work"
    assert tok is None


def test_parse_manifest_fenced_block() -> None:
    text = "prose\n```\nA, B, C\n```"
    assert parse_manifest(text) == ["A", "B", "C"]


def test_parse_manifest_bullet_list_fallback() -> None:
    text = "Items:\n- BMA-X\n- BMA-Y\n"
    assert parse_manifest(text) == ["BMA-X", "BMA-Y"]


def test_count_machine_acceptance() -> None:
    text = "- [ ] one\n- [ ] two\n- [x] done\n- [ ] three"
    # Counts unchecked boxes ([ ]); does not count [x]
    assert count_machine_acceptance(text) == 3


# ---------- parse_issue end-to-end ----------

def test_parse_issue_real_shape() -> None:
    info = parse_issue(make_issue())
    assert info.issue_number == 26
    assert info.chunk_id == "trial-source-ingest-pubmed"
    assert info.spec_url == "https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/trial-source-ingest-pubmed.md"
    assert info.branch == "tasktorrent/trial-source-ingest-pubmed"
    assert info.sidecar_dir == "contributions/trial-source-ingest-pubmed/"
    assert info.claim_method == "formal-issue"
    assert info.drop_estimate_tokens == 300_000
    assert info.required_skill == "citation-verification"
    assert "source-ingest" in info.topic_labels
    assert info.acceptance_criteria_machine_count == 3
    assert info.manifest_preview[:3] == ["CROSS", "PARADIGM", "RUBY"]
    assert info.parse_warnings == []
    assert info.agent_prompt_url_guess == (
        "https://github.com/romeo111/OpenOnco/blob/master/"
        "docs/contributing/AGENT_PROMPT_trial-source-ingest-pubmed.md"
    )


def test_parse_issue_invalid_claim_method_warns() -> None:
    body = REAL_ISSUE_BODY.replace("`formal-issue`", "`open-bidding`")
    info = parse_issue(make_issue(body=body))
    assert info.claim_method is None
    assert any("open-bidding" in w for w in info.parse_warnings)


def test_parse_issue_missing_section_warns() -> None:
    # Drop the entire Chunk ID section
    body = REAL_ISSUE_BODY.replace(
        "## Chunk ID\n\n`trial-source-ingest-pubmed`\n\n", ""
    )
    info = parse_issue(make_issue(body=body))
    assert any("Chunk ID" in w for w in info.parse_warnings)


def test_parse_issue_branch_naming_alt_heading() -> None:
    body = REAL_ISSUE_BODY.replace("## Branch Naming Convention", "## Branch Naming")
    info = parse_issue(make_issue(body=body))
    assert info.branch == "tasktorrent/trial-source-ingest-pubmed"


# ---------- CLI offline-mode integration ----------

def write_issues(tmp_path: Path, issues: list[dict]) -> Path:
    p = tmp_path / "issues.json"
    p.write_text(json.dumps(issues), encoding="utf-8")
    return p


def test_cli_offline_picks_oldest(tmp_path: Path, capsys) -> None:
    older = make_issue(number=26, createdAt="2026-04-28T18:00:00Z")
    newer = make_issue(
        number=27,
        createdAt="2026-04-28T19:00:00Z",
        body=REAL_ISSUE_BODY.replace("trial-source-ingest-pubmed", "other-chunk"),
    )
    p = write_issues(tmp_path, [newer, older])  # intentionally out of order
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["issue_number"] == 26
    assert out["chunk_id"] == "trial-source-ingest-pubmed"
    assert out["status"] == "ok"


def test_cli_offline_skips_assigned(tmp_path: Path, capsys) -> None:
    assigned = make_issue(number=26, assignees=[{"login": "someone"}])
    available = make_issue(
        number=27,
        body=REAL_ISSUE_BODY.replace("trial-source-ingest-pubmed", "open-chunk"),
        createdAt="2026-04-28T20:00:00Z",
    )
    p = write_issues(tmp_path, [assigned, available])
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["issue_number"] == 27


def test_cli_offline_no_chunks(tmp_path: Path, capsys) -> None:
    p = write_issues(tmp_path, [])
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 2
    out = json.loads(capsys.readouterr().out)
    assert out == {"status": "no_chunks_available"}


def test_cli_offline_all_assigned(tmp_path: Path, capsys) -> None:
    assigned = make_issue(assignees=[{"login": "x"}])
    p = write_issues(tmp_path, [assigned])
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 2


def test_cli_offline_bad_file(tmp_path: Path, capsys) -> None:
    p = tmp_path / "missing.json"
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 1


def test_cli_offline_bad_shape(tmp_path: Path) -> None:
    p = tmp_path / "wrong.json"
    p.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    rc = main(["--offline", str(p), "--json-only"])
    assert rc == 1
