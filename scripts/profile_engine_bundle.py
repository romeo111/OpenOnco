"""Analyze the composition of the OpenOnco engine bundle.

Goal: understand what bloats `docs/openonco-engine.zip` so the CSD-5B
core+per-disease split can be sized properly.

Run:
    python -m scripts.profile_engine_bundle

Outputs a Markdown report at
`docs/plans/archive/csd_5_bundle_profile_<YYYY-MM-DD>.md` and prints a summary
to stdout. Builds the bundle on the fly if it doesn't already exist.
"""

from __future__ import annotations

import datetime as _dt
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE = REPO_ROOT / "docs" / "openonco-engine.zip"
PLANS_DIR = REPO_ROOT / "docs" / "plans"


_DISEASE_ID_RE = re.compile(r"DIS-[A-Z0-9_-]+", re.IGNORECASE)


def _ensure_bundle() -> Path:
    if BUNDLE.exists():
        return BUNDLE
    print(f"[profile] {BUNDLE} not found — running scripts/build_site.py first…")
    subprocess.check_call(
        [sys.executable, "-m", "scripts.build_site"],
        cwd=REPO_ROOT,
    )
    if not BUNDLE.exists():
        raise SystemExit(f"build_site did not produce {BUNDLE}")
    return BUNDLE


def _entity_dir(arc_path: str) -> str | None:
    """Return the entity directory name (e.g. 'indications') for files
    living under `knowledge_base/hosted/content/<dir>/...yaml`. Returns
    None for code / non-content files."""
    parts = arc_path.split("/")
    if len(parts) < 5:
        return None
    if parts[0] != "knowledge_base" or parts[1] != "hosted" or parts[2] != "content":
        return None
    return parts[3]


def _disease_id_from_yaml(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> str | None:
    """Best-effort guess at which disease this YAML belongs to.

    Strategy:
      1. Open the YAML, look for `disease_id: DIS-...` or
         `applicable_to_disease: DIS-...` at the top level.
      2. Fall back to the `id:` line for diseases/ entities.
      3. Last resort: scan first ~3 KB for any DIS-XXX token.

    Returns None when no disease can be resolved (shared content).
    """
    if not info.filename.endswith(".yaml"):
        return None
    try:
        head = zf.read(info).decode("utf-8", errors="replace")
    except Exception:
        return None
    # Look for explicit disease_id / applicable_to_disease lines first
    m = re.search(r"^\s*disease_id\s*:\s*(DIS-[A-Z0-9_-]+)", head, re.MULTILINE)
    if m:
        return m.group(1).upper()
    m = re.search(r"^\s*applicable_to_disease\s*:\s*(DIS-[A-Z0-9_-]+)", head, re.MULTILINE)
    if m:
        return m.group(1).upper()
    # diseases/ files: id: DIS-...
    if "/diseases/" in info.filename:
        m = re.search(r"^\s*id\s*:\s*(DIS-[A-Z0-9_-]+)", head, re.MULTILINE)
        if m:
            return m.group(1).upper()
    # applicable_to: { disease_id: DIS-... } (nested style)
    m = re.search(r"applicable_to\s*:\s*\n[\s\S]{0,200}?disease_id\s*:\s*(DIS-[A-Z0-9_-]+)", head)
    if m:
        return m.group(1).upper()
    # relevant_diseases for redflags — pick first listed disease (skip "*").
    # Handles inline [DIS-X] and block-list format.
    m = re.search(r"relevant_diseases\s*:\s*\[([^\]]+)\]", head)
    if m:
        for tok in m.group(1).split(","):
            tok = tok.strip()
            if tok.upper().startswith("DIS-"):
                return tok.upper()
    m = re.search(r"relevant_diseases\s*:\s*\n((?:\s*-\s*\S+\s*\n)+)", head)
    if m:
        block = m.group(1)
        for line in block.splitlines():
            tok = line.strip().lstrip("-").strip()
            if tok and tok != "*" and tok.upper().startswith("DIS-"):
                return tok.upper()
    return None


def main() -> int:
    bundle = _ensure_bundle()
    bundle_size = bundle.stat().st_size

    sizes_by_top: dict[str, int] = defaultdict(int)
    sizes_by_entity_dir: dict[str, int] = defaultdict(int)
    counts_by_entity_dir: dict[str, int] = defaultdict(int)
    sizes_by_disease: dict[str, int] = defaultdict(int)
    files_by_disease: dict[str, int] = defaultdict(int)
    code_size = 0
    code_files = 0
    shared_content_size = 0  # YAMLs we couldn't tag with a disease

    largest: list[tuple[int, str]] = []

    with zipfile.ZipFile(bundle) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            csize = info.compress_size
            largest.append((csize, info.filename))

            top = info.filename.split("/")[1] if "/" in info.filename else "(root)"
            sizes_by_top[top] += csize

            if info.filename.endswith((".py",)):
                code_size += csize
                code_files += 1
                continue

            edir = _entity_dir(info.filename)
            if edir is not None:
                sizes_by_entity_dir[edir] += csize
                counts_by_entity_dir[edir] += 1
                disease = _disease_id_from_yaml(zf, info)
                if disease:
                    sizes_by_disease[disease] += csize
                    files_by_disease[disease] += 1
                else:
                    shared_content_size += csize

    largest.sort(reverse=True)
    top_files = largest[:15]
    top_diseases = sorted(sizes_by_disease.items(), key=lambda kv: kv[1], reverse=True)[:20]

    today = _dt.date.today().isoformat()
    report_path = PLANS_DIR / f"csd_5_bundle_profile_{today}.md"
    PLANS_DIR.mkdir(parents=True, exist_ok=True)

    def kb(n: int) -> str:
        return f"{n / 1024:.1f} KB"

    lines: list[str] = []
    lines.append(f"# CSD-5B engine-bundle composition profile — {today}\n")
    lines.append(f"Bundle: `{bundle.relative_to(REPO_ROOT).as_posix()}`  ")
    lines.append(f"Compressed size: **{kb(bundle_size)}** ({bundle_size:,} bytes)\n")

    lines.append("## Breakdown by top-level subtree (compressed)\n")
    lines.append("| Subtree | Size | % |")
    lines.append("|---|--:|--:|")
    total = sum(sizes_by_top.values()) or 1
    for top, sz in sorted(sizes_by_top.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"| `{top}` | {kb(sz)} | {sz / total * 100:.1f}% |")
    lines.append("")

    lines.append("## Code vs content\n")
    lines.append(f"- Python code: **{kb(code_size)}** across {code_files} files")
    lines.append(f"- KB content (YAML): **{kb(sum(sizes_by_entity_dir.values()))}** across "
                 f"{sum(counts_by_entity_dir.values())} files")
    lines.append("")

    lines.append("## KB content by entity type (compressed)\n")
    lines.append("| Entity dir | Files | Compressed | % of content |")
    lines.append("|---|--:|--:|--:|")
    content_total = sum(sizes_by_entity_dir.values()) or 1
    for edir, sz in sorted(sizes_by_entity_dir.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(
            f"| `{edir}` | {counts_by_entity_dir[edir]} | {kb(sz)} | "
            f"{sz / content_total * 100:.1f}% |"
        )
    lines.append("")

    lines.append("## Top diseases by attributed bundle weight\n")
    lines.append("Best-effort tagging: a YAML is attributed to a disease when it cites "
                 "`disease_id`, `applicable_to_disease`, `applicable_to.disease_id`, or "
                 "(for redflags) the first concrete entry in `relevant_diseases`.\n")
    lines.append("| Disease | Files | Compressed |")
    lines.append("|---|--:|--:|")
    for disease, sz in top_diseases:
        lines.append(f"| `{disease}` | {files_by_disease[disease]} | {kb(sz)} |")
    lines.append("")
    lines.append(f"**Total disease-attributed YAML weight:** "
                 f"{kb(sum(sizes_by_disease.values()))} across "
                 f"{sum(files_by_disease.values())} files\n")
    lines.append(f"**Shared / un-attributable YAML weight (drugs, sources, biomarkers, …):** "
                 f"{kb(shared_content_size)}\n")

    lines.append("## Top-15 largest individual files in the bundle\n")
    lines.append("| Compressed | Path |")
    lines.append("|--:|---|")
    for csize, name in top_files:
        lines.append(f"| {kb(csize)} | `{name}` |")
    lines.append("")

    lines.append("## Implications for the core/per-disease split\n")
    biggest_disease = top_diseases[0] if top_diseases else None
    if biggest_disease:
        lines.append(
            f"- Biggest single disease attributed: `{biggest_disease[0]}` at "
            f"{kb(biggest_disease[1])} compressed. Per-disease bundles should "
            f"comfortably fit under 300 KB compressed.\n"
        )
    core_estimate = (
        code_size + shared_content_size
        + sizes_by_entity_dir.get("sources", 0)
        + sizes_by_entity_dir.get("drugs", 0)
        + sizes_by_entity_dir.get("biomarkers", 0)
        + sizes_by_entity_dir.get("tests", 0)
        + sizes_by_entity_dir.get("supportive_care", 0)
        + sizes_by_entity_dir.get("monitoring", 0)
        + sizes_by_entity_dir.get("workups", 0)
        + sizes_by_entity_dir.get("questionnaires", 0)
        + sizes_by_entity_dir.get("contraindications", 0)
        + sizes_by_entity_dir.get("mdt_skills", 0)
        + sizes_by_entity_dir.get("diseases", 0)
    )
    lines.append(
        f"- Estimated core bundle (code + shared content + disease "
        f"metadata): **~{kb(core_estimate)}** compressed.\n"
    )
    lines.append(
        f"- Estimated per-disease tail (indications + algorithms + regimens "
        f"+ disease-specific RFs + BMA cells): "
        f"**~{kb(sum(sizes_by_disease.values()))}** total, distributed.\n"
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[profile] wrote {report_path.relative_to(REPO_ROOT).as_posix()}")
    print(f"[profile] bundle = {kb(bundle_size)}, "
          f"code = {kb(code_size)}, content = {kb(content_total)}")
    print(f"[profile] core estimate = {kb(core_estimate)}, "
          f"per-disease tail total = {kb(sum(sizes_by_disease.values()))}")
    if top_diseases:
        d, sz = top_diseases[0]
        print(f"[profile] biggest disease = {d} at {kb(sz)} compressed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
