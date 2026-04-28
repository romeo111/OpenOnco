"""Extract list of trial names needing source ingest, from
citation-semantic-verify-v2's source_stub_needed rows.

Each row in that report whose suggested_action is `source_stub_needed`
references a specific RCT (KEYNOTE-X, CHECKMATE-X, MAGNITUDE, THOR, etc.)
that has no corresponding SRC-* in `knowledge_base/hosted/content/sources/`.
This script extracts those trial names, groups by trial, lists referencing
entities + finding_ids, and produces a maintainer-actionable triage report.

Sorted by trial-occurrence count (most-used trial first → highest priority
to ingest).

Usage:
    python -m scripts.tasktorrent.extract_trials_needing_source

Output:
    contributions/citation-semantic-verify-v2/trials-needing-source-ingest.md
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CHUNK_DIR = REPO_ROOT / "contributions" / "citation-semantic-verify-v2"
REPORT = CHUNK_DIR / "citation-report-v2.yaml"

_TRIAL_PATTERNS = [
    re.compile(r"""trial ['"]([^'"]{2,80})['"]"""),
    re.compile(r"""trial/source ['"]([^'"]{2,80})['"]"""),
]


def _load_yaml(p: Path) -> Any:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _extract_trials(text: str) -> list[str]:
    out: list[str] = []
    for pat in _TRIAL_PATTERNS:
        for m in pat.finditer(text or ""):
            t = m.group(1).strip()
            if t and t.lower() not in {"trial", "source"}:
                out.append(t)
    seen = set()
    result = []
    for t in out:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


def _normalize_trial(name: str) -> str:
    s = name.upper()
    s = s.replace("KEYNOTE ", "KEYNOTE-")
    s = s.replace("CHECKMATE ", "CHECKMATE-")
    s = s.replace("IMPOWER ", "IMPOWER-")
    s = s.replace("LIBRETTO ", "LIBRETTO-")
    s = s.replace("KRYSTAL ", "KRYSTAL-")
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"--+", "-", s)
    return s


def main() -> int:
    if not REPORT.exists():
        print(f"report missing: {REPORT}", file=sys.stderr)
        return 1
    report = _load_yaml(REPORT)
    rows = report.get("rows", []) if isinstance(report, dict) else []
    stub_rows = [r for r in rows if isinstance(r, dict) and r.get("suggested_action") == "source_stub_needed"]
    print(f"source_stub_needed rows: {len(stub_rows)}")

    trials: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    no_trial_extracted: list[str] = []

    for r in stub_rows:
        rat = r.get("verified_rationale") or ""
        finding_id = r.get("finding_id", "?")
        entity_id = r.get("entity_id", "")
        entity_file = r.get("entity_file", "")
        names = _extract_trials(rat)
        if not names:
            no_trial_extracted.append(finding_id)
            continue
        trial_norm = _normalize_trial(names[0])
        trials[trial_norm].append((finding_id, entity_id, entity_file))

    print(f"unique trials extracted: {len(trials)}")
    print(f"rows without extractable trial: {len(no_trial_extracted)}")

    sorted_trials = sorted(trials.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    out_path = CHUNK_DIR / "trials-needing-source-ingest.md"
    lines: list[str] = []
    lines.append("# Trials Needing Source Ingest\n")
    lines.append(
        f"Extracted from {len(stub_rows)} source_stub_needed rows in "
        f"citation-report-v2.yaml. {len(trials)} unique trials identified, "
        f"sorted by usage count (most-cited first → highest priority).\n"
    )
    lines.append(
        "Each trial below needs a `SRC-<TRIAL>-<AUTHOR>-<YEAR>` entity in "
        "`knowledge_base/hosted/content/sources/`. Use PubMed/CIViC/etc. to "
        "find the pivotal publication; create the Source stub via "
        "`source_stub.yaml` template; ingest per `specs/SOURCE_INGESTION_SPEC.md`.\n"
    )
    lines.append(
        "> **⚠️ False-positive warning:** trial names below are extracted from "
        "Codex's `verified_rationale` field. In rows where the v1 audit did "
        "not identify a specific trial, Codex sometimes labels generic words "
        "(e.g. 'CROSS', 'PARADIGM') as trial names — these may NOT correspond "
        "to actual RCTs. Quick sanity-check: if a trial spans many unrelated "
        "disease domains (e.g. FLT3 AML + esophageal + melanoma), it's likely "
        "a false positive. Verify each trial-name vs the cited entity's "
        "domain before ingesting.\n"
    )
    lines.append("---\n")

    for trial, refs in sorted_trials:
        lines.append(f"## {trial}\n")
        lines.append(f"**Cited by:** {len(refs)} finding(s)")
        lines.append(f"**Distinct entities:** {len(set(r[1] for r in refs))}")
        lines.append("")
        lines.append("**Maintainer todo:**")
        lines.append(
            "- [ ] PubMed lookup → identify pivotal publication "
            "(lead author, year, journal, DOI, PMID)"
        )
        lines.append("- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`")
        lines.append("- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`")
        lines.append(
            "- [ ] Update referencing entities: replace placeholder citation "
            "with new SRC-* ID"
        )
        lines.append("")
        lines.append("**Referenced findings (first 10):**")
        for fid, eid, ef in refs[:10]:
            lines.append(f"- `{fid}` → `{eid}` ({ef})")
        if len(refs) > 10:
            lines.append(f"- ... +{len(refs) - 10} more")
        lines.append("")
        lines.append("---\n")

    if no_trial_extracted:
        lines.append("## Rows where trial name could not be extracted\n")
        lines.append(f"{len(no_trial_extracted)} `source_stub_needed` rows had rationale text that didn't match known trial-name regex patterns. These need manual look-up.\n")
        for fid in no_trial_extracted[:30]:
            lines.append(f"- `{fid}`")
        if len(no_trial_extracted) > 30:
            lines.append(f"- ... +{len(no_trial_extracted) - 30} more")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
