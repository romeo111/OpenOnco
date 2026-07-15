"""UA-translation quality validator.

Catches the failure modes that Phase 1 parallel agents are most likely
to produce:

  1. **EN bleed** — runs of >=4 consecutive ASCII alphabetic words inside
     a ``*_ua`` field that aren't in the ``stay_latin`` whitelist or the
     ``preserve_verbatim`` patterns. (Per-agent draft prose drifting back
     to English.)
  2. **Glossary divergence** — a ``phrases`` glossary entry's EN form
     appearing in ``*_ua`` without the corresponding UA form anywhere
     near it. (Agent invented a synonym instead of using the locked term.)
  3. **Numeric drift** — every numeric+unit token (dose, %, year, NCT,
     EID, OpenOnco ID, HGVS) in the EN field MUST appear in the UA
     field. (Mistyped dose is the highest-blast-radius failure.)
  4. **Markdown link parity** — ``[text](url)`` count must match.
  5. **Marker integrity** — if a ``*_ua`` field is non-empty, the entity
     MUST carry ``ukrainian_review_status`` and ``ukrainian_drafted_by``.
     If ``draft_revision`` is set, it MUST be a positive integer.

Usage:
    python -m knowledge_base.validation.ua_quality knowledge_base/hosted/content
    python -m knowledge_base.validation.ua_quality path/to/single.yaml

Exit code: 0 if no errors. 1 on any error. Warnings do not fail.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
GLOSSARY_PATH = REPO / "knowledge_base" / "translation" / "ua_terminology.yaml"

# Mirror of audit_ua_coverage.ENTITY_PLAN — kept local to avoid import.
ENTITY_PLAN: dict[str, list[tuple[str, str]]] = {
    "biomarkers": [("notes", "notes_ua"), ("description", "description_ua")],
    "biomarker_actionability": [
        ("evidence_summary", "evidence_summary_ua"),
        ("notes", "notes_ua"),
    ],
    "diseases": [("notes", "notes_ua")],
    "regimens": [("notes", "notes_ua")],
    "redflags": [("notes", "notes_ua"), ("description", "description_ua")],
    "indications": [("rationale", "rationale_ua")],
    "drugs": [("notes", "notes_ua")],
    "algorithms": [("notes", "notes_ua")],
    "procedures": [("notes", "notes_ua")],
    "radiation_courses": [("notes", "notes_ua")],
}


@dataclass
class GlossaryView:
    stay_latin: set[str] = field(default_factory=set)
    phrases: dict[str, str] = field(default_factory=dict)
    drugs: dict[str, str] = field(default_factory=dict)
    preserve_patterns: list[re.Pattern] = field(default_factory=list)


def load_glossary(path: Path = GLOSSARY_PATH) -> GlossaryView:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    g = GlossaryView()
    sl = raw.get("stay_latin", {}) or {}
    for bucket in sl.values():
        for tok in bucket or []:
            g.stay_latin.add(str(tok))
    for k, v in (raw.get("phrases") or {}).items():
        g.phrases[str(k).lower()] = str(v)
    for k, v in (raw.get("drugs") or {}).items():
        g.drugs[str(k).lower()] = str(v)
    for entry in raw.get("preserve_verbatim", []) or []:
        for _name, pat in entry.items():
            g.preserve_patterns.append(re.compile(pat, re.IGNORECASE))
    return g


@dataclass
class Issue:
    file: str
    field: str
    severity: str  # "error" | "warning"
    code: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.file}:{self.field}  {self.code}: {self.message}"


# ── Detectors ───────────────────────────────────────────────────────────

# Run of 4+ ASCII alphabetic words separated only by spaces / hyphens /
# apostrophes / slashes. Excludes anything with Cyrillic. Trial / drug /
# gene names have to be filtered against the glossary AFTER capture.
_EN_RUN = re.compile(
    r"\b(?:[A-Za-z][A-Za-z'\-\/]*(?:\s+|$)){4,}"
)
_HAS_CYRILLIC = re.compile(r"[Ѐ-ӿ]")
_NUMERIC_TOKENS = re.compile(
    r"""
    \b\d+(?:\.\d+)?\s*(?:mg|g|mcg|µg|kg|ml|mL|U|IU|MU)(?:/(?:m²|m\^2|kg|day|d|h|hr|wk))?\b
  | \b\d+(?:\.\d+)?\s*%
  | \bNCT\d{6,8}\b
  | \bEID\d{1,6}\b
  | \b(?:DIS|BIO|BMA|DRUG|IND|RF|REG|SRC|ALGO|PROC|RAD)-[A-Z0-9-]+\b
  | \b[pcgn]\.[A-Z][A-Za-z0-9*>=._-]+\b
  | \b(?:t|inv|del|dup|add|der)\(\d+(?:;\d+)?(?:[pq]\d+(?:\.\d+)?)?\)
    """,
    re.VERBOSE,
)
_MD_LINK = re.compile(r"\[[^\]]+\]\([^)]+\)")


def detect_en_bleed(ua_text: str, gloss: GlossaryView) -> list[str]:
    """Return list of suspicious EN runs in UA text."""
    if not ua_text:
        return []
    # Strip preserved tokens first so they don't trigger the run detector.
    stripped = ua_text
    for pat in gloss.preserve_patterns:
        stripped = pat.sub(" ", stripped)
    # Strip stay_latin tokens.
    if gloss.stay_latin:
        sl_pattern = re.compile(
            r"\b(?:" + "|".join(re.escape(t) for t in gloss.stay_latin) + r")\b"
        )
        stripped = sl_pattern.sub(" ", stripped)

    findings = []
    for m in _EN_RUN.finditer(stripped):
        run = m.group(0).strip()
        if len(run.split()) < 4:
            continue
        # Word count after removing acronyms/numbers
        words = [w for w in re.split(r"[\s\-\/]+", run) if w and w.isalpha()]
        if len(words) < 4:
            continue
        # If most words are ALL-CAPS acronyms, skip (likely trial / regimen).
        caps = sum(1 for w in words if w.isupper() and len(w) >= 2)
        if caps >= len(words) * 0.6:
            continue
        findings.append(run)
    return findings


def detect_glossary_divergence(
    en_text: str, ua_text: str, gloss: GlossaryView
) -> list[tuple[str, str]]:
    """Return (en_phrase, expected_ua) where EN phrase appears in EN source
    but UA translation doesn't include the expected UA form."""
    findings = []
    en_lower = (en_text or "").lower()
    ua_lower = (ua_text or "").lower()
    for en_p, ua_p in gloss.phrases.items():
        if en_p in en_lower and ua_p.lower() not in ua_lower:
            # Tolerate close morphology: check first 5 chars of UA stem
            stem = ua_p.lower()[: max(5, len(ua_p) // 2)]
            if stem in ua_lower:
                continue
            findings.append((en_p, ua_p))
    for en_d, ua_d in gloss.drugs.items():
        if en_d in en_lower and ua_d.lower() not in ua_lower and en_d not in ua_lower:
            findings.append((en_d, ua_d))
    return findings


def detect_numeric_drift(en_text: str, ua_text: str) -> list[str]:
    en_tokens = {m.group(0) for m in _NUMERIC_TOKENS.finditer(en_text or "")}
    ua_tokens = {m.group(0) for m in _NUMERIC_TOKENS.finditer(ua_text or "")}
    return sorted(en_tokens - ua_tokens)


def detect_link_parity(en_text: str, ua_text: str) -> tuple[int, int]:
    return (
        len(_MD_LINK.findall(en_text or "")),
        len(_MD_LINK.findall(ua_text or "")),
    )


# ── Driver ──────────────────────────────────────────────────────────────


def check_file(path: Path, plan: list[tuple[str, str]], gloss: GlossaryView) -> list[Issue]:
    abs_path = path.resolve()
    try:
        rel = str(abs_path.relative_to(REPO)).replace("\\", "/")
    except ValueError:
        rel = str(path).replace("\\", "/")
    issues: list[Issue] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [Issue(rel, "_FILE_", "error", "PARSE", str(exc)[:160])]
    if not isinstance(data, dict):
        return []

    has_any_ua = False
    for en_field, ua_field in plan:
        en_val = data.get(en_field)
        ua_val = data.get(ua_field)
        if not (ua_val and str(ua_val).strip()):
            continue
        has_any_ua = True
        en_text = str(en_val or "")
        ua_text = str(ua_val)

        for run in detect_en_bleed(ua_text, gloss):
            issues.append(
                Issue(
                    rel, ua_field, "error", "EN_BLEED",
                    f'untranslated EN run: "{run[:80]}"',
                )
            )
        for en_p, ua_p in detect_glossary_divergence(en_text, ua_text, gloss):
            issues.append(
                Issue(
                    rel, ua_field, "warning", "GLOSSARY_MISS",
                    f'EN "{en_p}" present in source; expected UA "{ua_p}" not found',
                )
            )
        missing_nums = detect_numeric_drift(en_text, ua_text)
        if missing_nums:
            issues.append(
                Issue(
                    rel, ua_field, "error", "NUMERIC_DRIFT",
                    f"missing in UA: {', '.join(missing_nums[:6])}"
                    + (f" (+{len(missing_nums)-6} more)" if len(missing_nums) > 6 else ""),
                )
            )
        en_links, ua_links = detect_link_parity(en_text, ua_text)
        if en_links != ua_links:
            issues.append(
                Issue(
                    rel, ua_field, "error", "LINK_PARITY",
                    f"EN has {en_links} markdown links, UA has {ua_links}",
                )
            )

    if has_any_ua:
        if not data.get("ukrainian_review_status"):
            issues.append(
                Issue(rel, "_ENTITY_", "error", "MISSING_MARKER",
                      "ukrainian_review_status absent though *_ua field present")
            )
        if not data.get("ukrainian_drafted_by"):
            issues.append(
                Issue(rel, "_ENTITY_", "error", "MISSING_MARKER",
                      "ukrainian_drafted_by absent though *_ua field present")
            )
        rev = data.get("draft_revision")
        if rev is not None and not (isinstance(rev, int) and rev >= 1):
            issues.append(
                Issue(rel, "_ENTITY_", "error", "BAD_REVISION",
                      f"draft_revision must be positive int, got {rev!r}")
            )
    return issues


def collect_paths(targets: list[Path]) -> list[tuple[Path, list[tuple[str, str]]]]:
    """Resolve CLI args into (file, plan) pairs."""
    out: list[tuple[Path, list[tuple[str, str]]]] = []
    for t in targets:
        if t.is_file():
            entity_type = t.parent.name
            plan = ENTITY_PLAN.get(entity_type)
            if plan:
                out.append((t, plan))
            continue
        for entity_dir, plan in ENTITY_PLAN.items():
            d = t / entity_dir if t.name != entity_dir else t
            if not d.exists():
                continue
            for f in sorted(d.glob("*.yaml")):
                out.append((f, plan))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="+", type=Path)
    ap.add_argument("--quiet", action="store_true", help="Only print errors, suppress warnings.")
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    gloss = load_glossary()
    pairs = collect_paths(args.targets)
    all_issues: list[Issue] = []
    for path, plan in pairs:
        all_issues.extend(check_file(path, plan, gloss))

    errors = [i for i in all_issues if i.severity == "error"]
    warnings = [i for i in all_issues if i.severity == "warning"]

    if not args.summary_only:
        for i in all_issues:
            if args.quiet and i.severity != "error":
                continue
            print(i)

    print(f"\nUA quality: {len(pairs)} files checked, {len(errors)} errors, {len(warnings)} warnings.")
    if errors:
        by_code: dict[str, int] = {}
        for i in errors:
            by_code[i.code] = by_code.get(i.code, 0) + 1
        for code, n in sorted(by_code.items(), key=lambda kv: -kv[1]):
            print(f"  {code:<18} {n}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
