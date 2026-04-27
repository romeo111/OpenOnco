"""Generate TaskTorrent sidecar reports for offline audit chunks.

The script intentionally avoids importing PyYAML because the current
worktree can be used without a fully installed Python dependency set. It
extracts only the top-level YAML fields needed by the two report-only
chunks and writes conservative sidecar reports under contributions/.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "knowledge_base" / "hosted" / "content"
TODAY = date(2026, 4, 27).isoformat()


@dataclass(frozen=True)
class FieldValue:
    value: str
    raw: str


TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$")


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _normalize_block(raw_value: str, block_lines: list[str]) -> str:
    marker = raw_value.strip()
    if not block_lines:
        return ""

    nonblank = [ln for ln in block_lines if ln.strip()]
    min_indent = min((len(ln) - len(ln.lstrip(" ")) for ln in nonblank), default=0)
    stripped = [ln[min_indent:] if len(ln) >= min_indent else ln for ln in block_lines]

    if marker.startswith("|"):
        return "\n".join(stripped).strip()
    if marker.startswith(">"):
        paragraphs: list[str] = []
        current: list[str] = []
        for ln in stripped:
            if ln.strip():
                current.append(ln.strip())
            elif current:
                paragraphs.append(" ".join(current))
                current = []
        if current:
            paragraphs.append(" ".join(current))
        return "\n".join(paragraphs).strip()

    text = "\n".join(stripped).strip()
    if text.startswith("- "):
        items = []
        for ln in stripped:
            s = ln.strip()
            if s.startswith("- "):
                items.append(s[2:].strip())
            elif items and s:
                items[-1] += " " + s
        return "\n".join(items)
    return text


def parse_top_level(text: str) -> dict[str, FieldValue]:
    lines = text.splitlines()
    fields: dict[str, FieldValue] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        match = TOP_KEY_RE.match(line)
        if not match:
            i += 1
            continue

        key, raw_value = match.group(1), (match.group(2) or "")
        block_lines: list[str] = []
        j = i + 1
        while j < len(lines):
            next_line = lines[j]
            if next_line and not next_line.startswith((" ", "\t")) and TOP_KEY_RE.match(next_line):
                break
            block_lines.append(next_line)
            j += 1

        if raw_value.strip() in {"", ">", ">-", ">+", "|", "|-", "|+"}:
            value = _normalize_block(raw_value, block_lines)
        else:
            value = _strip_quotes(raw_value.split(" #", 1)[0])

        raw = "\n".join([line, *block_lines]).strip()
        fields[key] = FieldValue(value=value.strip(), raw=raw)
        i = j
    return fields


def iter_yaml_files(base: Path) -> list[Path]:
    return sorted(p for p in base.rglob("*.yaml") if p.is_file())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def yaml_escape_inline(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_scalar(key: str, value: str | None, indent: int = 0) -> list[str]:
    pad = " " * indent
    if value is None:
        return [f"{pad}{key}: null"]
    value = str(value)
    if value == "":
        return [f"{pad}{key}: \"\""]
    if "\n" in value or len(value) > 110 or ": " in value or value.startswith(("-", "{", "[")):
        out = [f"{pad}{key}: >"]
        for paragraph in value.splitlines() or [""]:
            out.append(f"{pad}  {paragraph}")
        return out
    return [f"{pad}{key}: {yaml_escape_inline(value)}"]


def dump_meta(chunk_id: str, notes: str) -> str:
    lines = [
        f"chunk_id: {chunk_id}",
        "chunk_spec_url: https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/"
        f"{chunk_id}.md",
        "contributor: codex-agent",
        f"submission_date: {TODAY}",
        "ai_tool: codex",
        "ai_model: gpt-5",
        'ai_model_version: ""',
    ]
    lines.extend(yaml_scalar("notes_for_reviewer", notes))
    return "\n".join(lines) + "\n"


def dump_report(chunk_id: str, notes: str, findings: list[dict[str, str | None]]) -> str:
    lines: list[str] = [
        "_contribution:",
        f"  chunk_id: {chunk_id}",
        "  contributor: codex-agent",
        "  ai_tool: codex",
        "  ai_model: gpt-5",
        '  ai_model_version: ""',
    ]
    lines.extend(yaml_scalar("ai_session_notes", notes, 2))
    lines.extend(["", "findings:"])
    if not findings:
        lines.append("  []")
        return "\n".join(lines) + "\n"

    for item in findings:
        lines.append(f"  - finding_id: {item['finding_id']}")
        for key, value in item.items():
            if key == "finding_id" or value is None:
                continue
            lines.extend(yaml_scalar(key, value, 4))
    return "\n".join(lines) + "\n"


REC_SCOPE = {
    "biomarker_actionability": ["evidence_summary", "evidence_summary_ua", "notes", "notes_patient"],
    "indications": ["rationale", "notes", "do_not_do"],
    "drugs": ["mechanism", "notes", "notes_patient"],
    "redflags": ["description", "definition", "recommendation", "notes"],
}

REC_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("patient-directed imperative", re.compile(r"\b(?:patients?\s+should|the\s+patient\s+must|you\s+can)\b", re.I), "critical"),
    ("direct obligation", re.compile(r"\b(?:should|must)\b", re.I), "critical"),
    ("required-language drift", re.compile(r"\b(?:required|requires)\b", re.I), "moderate"),
    ("direct recommendation verb", re.compile(r"\b(?:we\s+recommend|recommend(?:ed|s|ing)?|advise(?:d|s)?|advisable)\b", re.I), "critical"),
    ("preference/ranking", re.compile(r"\b(?:prefer(?:red|s|able)?|first\s+choice|treatment\s+of\s+choice|preferred\s+to)\b", re.I), "moderate"),
    ("superlative claim", re.compile(r"\b(?:best|gold\s+standard)\b", re.I), "moderate"),
    ("standard-language drift", re.compile(r"\b(?:standard\s+of\s+care|standard\s+(?:track|option|therapy|regimen|2L|1L)|2L\s+standard|1L\s+standard)\b", re.I), "minor"),
]


def excerpt_around(text: str, start: int, end: int, radius: int = 95) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = re.sub(r"\s+", " ", text[left:right]).strip()
    if left:
        snippet = "..." + snippet
    if right < len(text):
        snippet += "..."
    return snippet


def suggest_neutral(matched: str) -> str:
    lower = matched.lower()
    if "best" in lower or "first choice" in lower or "treatment of choice" in lower:
        return "Replace ranking language with source-bounded wording such as: 'Guidelines list ... as an option for this context.'"
    if "standard" in lower:
        return "Replace 'standard' phrasing with neutral provenance wording such as: 'Guidelines/source evidence describe ... for this context.'"
    if "required" in lower or "must" in lower or "should" in lower:
        return "Replace obligation wording with declarative criteria such as: 'This field flags the source-attested condition where ... is considered.'"
    if "recommend" in lower or "advise" in lower or "prefer" in lower:
        return "Replace recommendation wording with neutral wording such as: 'The cited source lists ...' or 'Evidence supports ... in the cited setting.'"
    return "Reword to source-attested, non-directive phrasing that preserves the original clinical meaning."


def should_skip_rec_match(pattern_name: str, context: str) -> bool:
    ctx = context.lower()
    if pattern_name != "required-language drift":
        return False
    if re.search(r"\bnot\s+(?:strictly\s+)?required\b", ctx):
        return True
    governance_terms = [
        "clinical co-lead",
        "signoff",
        "sign-off",
        "review",
        "reviewer",
        "validation",
        "source required",
        "requires source",
        "manual curation",
        "requires extraction",
    ]
    return any(term in ctx for term in governance_terms)


def severity_for_rec(pattern_name: str, default: str, context: str) -> str:
    if pattern_name != "required-language drift":
        return default
    ctx = context.lower()
    if re.search(r"\b(?:treatment|therapy|regimen|addition|induction|testing|rebiopsy|biopsy|ngs|pcr|fish)\b", ctx):
        return "moderate"
    return "minor"


def generate_rec_wording() -> tuple[int, int]:
    chunk_id = "rec-wording-audit-claim-bearing"
    outdir = ROOT / "contributions" / chunk_id
    outdir.mkdir(parents=True, exist_ok=True)

    manifest: list[str] = []
    findings: list[dict[str, str | None]] = []
    seen: set[tuple[str, str, str, str]] = set()

    for folder, field_names in REC_SCOPE.items():
        base = CONTENT / folder
        if not base.exists():
            continue
        for path in iter_yaml_files(base):
            fields = parse_top_level(path.read_text(encoding="utf-8"))
            entity_id = fields.get("id", FieldValue(path.stem, "")).value
            for field_name in field_names:
                fv = fields.get(field_name)
                if not fv or not fv.value:
                    continue
                manifest.append(f"{entity_id}::{field_name}::{rel(path)}")
                text = fv.value
                for pattern_name, pattern, severity in REC_PATTERNS:
                    for match in pattern.finditer(text):
                        matched = match.group(0)
                        context = excerpt_around(text, match.start(), match.end(), 90)
                        if should_skip_rec_match(pattern_name, context):
                            continue
                        effective_severity = severity_for_rec(pattern_name, severity, context)
                        key = (entity_id, field_name, matched.lower(), excerpt_around(text, match.start(), match.end(), 40))
                        if key in seen:
                            continue
                        seen.add(key)
                        findings.append(
                            {
                                "finding_id": f"f-{len(findings) + 1:04d}",
                                "entity_id": entity_id,
                                "entity_file": rel(path),
                                "field_path": field_name,
                                "excerpt": excerpt_around(text, match.start(), match.end()),
                                "matched_pattern": matched,
                                "pattern_class": pattern_name,
                                "severity": effective_severity,
                                "suggested_rewording": suggest_neutral(matched),
                                "judgment": "likely_true_positive",
                                "notes": "Regex lower-bound catch with light semantic filtering for CHARTER Section 8.3 recommendation-wording review; maintainer should confirm context before hosted-content edits.",
                            }
                        )

    (outdir / "task_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (outdir / "_contribution_meta.yaml").write_text(
        dump_meta(
            chunk_id,
            "Offline scan of scoped claim-bearing top-level fields. Report is intentionally sidecar-only and does not modify hosted content.",
        ),
        encoding="utf-8",
    )
    (outdir / "audit-report.yaml").write_text(
        dump_report(
            chunk_id,
            "Generated by a conservative regex lower-bound scanner over BMA, Indication, Drug, and RedFlag free-text fields. Suggested rewordings are neutral templates, not clinical upserts.",
            findings,
        ),
        encoding="utf-8",
    )
    return len(manifest), len(findings)


EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")


def english_fragments(text: str) -> list[str]:
    matches = list(EN_WORD_RE.finditer(text))
    fragments: list[str] = []
    current: list[re.Match[str]] = []

    def flush() -> None:
        nonlocal current
        if len(current) >= 3:
            start = current[0].start()
            end = current[-1].end()
            fragment = re.sub(r"\s+", " ", text[start:end]).strip(" ,;:.()[]")
            if fragment and fragment not in fragments:
                fragments.append(fragment)
        current = []

    previous: re.Match[str] | None = None
    for match in matches:
        gap = text[previous.end() : match.start()] if previous else ""
        if previous is not None and CYRILLIC_RE.search(gap):
            flush()
        current.append(match)
        previous = match
    flush()
    return fragments


def severity_for_fragments(fragments: list[str], ua_text: str) -> str:
    english_words = sum(len(EN_WORD_RE.findall(fragment)) for fragment in fragments)
    all_words = max(1, len(re.findall(r"[A-Za-z\u0400-\u04FF][A-Za-z\u0400-\u04FF'-]*", ua_text)))
    if english_words >= 8 or english_words / all_words >= 0.25:
        return "critical"
    if english_words >= 4:
        return "moderate"
    return "minor"


def generate_ua_review() -> tuple[int, int, int]:
    chunk_id = "ua-translation-review-batch"
    outdir = ROOT / "contributions" / chunk_id
    outdir.mkdir(parents=True, exist_ok=True)

    manifest: list[str] = []
    findings: list[dict[str, str | None]] = []
    untranslated_count = 0

    for path in iter_yaml_files(CONTENT):
        text = path.read_text(encoding="utf-8")
        fields = parse_top_level(text)
        if fields.get("ukrainian_review_status", FieldValue("", "")).value != "pending_clinical_signoff":
            continue
        entity_id = fields.get("id", FieldValue(path.stem, "")).value
        ua_keys = sorted(k for k in fields if k.endswith("_ua") and fields[k].value)
        for ua_key in ua_keys:
            ua_text = fields[ua_key].value
            en_key = ua_key[:-3]
            en_text = fields.get(en_key, FieldValue("", "")).value
            manifest.append(f"{entity_id}::{ua_key}::{rel(path)}")

            fragments = english_fragments(ua_text)
            if fragments:
                untranslated_count += 1
                findings.append(
                    {
                        "finding_id": f"f-{len(findings) + 1:04d}",
                        "entity_id": entity_id,
                        "entity_file": rel(path),
                        "field_path": ua_key,
                        "en_excerpt": excerpt_around(en_text, 0, min(len(en_text), 1), 180) if en_text else "",
                        "ua_excerpt": excerpt_around(ua_text, 0, min(len(ua_text), 1), 220),
                        "category": "untranslated_fragment",
                        "severity": severity_for_fragments(fragments, ua_text),
                        "matched_pattern": "; ".join(fragments[:8]),
                        "suggested_correction": "Requires a full Ukrainian rewrite of the field by a bilingual clinical reviewer; do not auto-upsert a partial machine replacement because the current field mixes English fragments with Ukrainian terms.",
                        "notes": "Mechanical lower-bound catch: at least one run of three or more English-alphabet words remains in a UA field.",
                    }
                )
            else:
                findings.append(
                    {
                        "finding_id": f"f-{len(findings) + 1:04d}",
                        "entity_id": entity_id,
                        "entity_file": rel(path),
                        "field_path": ua_key,
                        "en_excerpt": excerpt_around(en_text, 0, min(len(en_text), 1), 180) if en_text else "",
                        "ua_excerpt": excerpt_around(ua_text, 0, min(len(ua_text), 1), 180),
                        "category": "acceptable",
                        "notes": "No >=3-word English fragment detected by the mechanical check. This is not clinical signoff; clinician review is still required for terminology, calque, and clinical drift.",
                    }
                )

    (outdir / "task_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (outdir / "_contribution_meta.yaml").write_text(
        dump_meta(
            chunk_id,
            "Offline bilingual-audit scaffold. The report guarantees coverage for the mechanical untranslated-fragment check and leaves clinical fidelity to Ukrainian-fluent clinician review.",
        ),
        encoding="utf-8",
    )
    (outdir / "audit-report.yaml").write_text(
        dump_report(
            chunk_id,
            "Generated from pending_clinical_signoff UA fields. The report covers every manifest field and flags all detected runs of three or more English-alphabet words.",
            findings,
        ),
        encoding="utf-8",
    )
    return len(manifest), len(findings), untranslated_count


def main() -> None:
    rec_manifest, rec_findings = generate_rec_wording()
    ua_manifest, ua_findings, ua_untranslated = generate_ua_review()
    print(f"rec-wording manifest fields: {rec_manifest}")
    print(f"rec-wording findings: {rec_findings}")
    print(f"ua manifest fields: {ua_manifest}")
    print(f"ua field reviews: {ua_findings}")
    print(f"ua untranslated-fragment findings: {ua_untranslated}")


if __name__ == "__main__":
    main()
