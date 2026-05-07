"""Audit `Indication.expected_outcomes` traceability.

Phase 1 deliverable for the Pivotal Trial Outcomes Ingestion Plan
(`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`).

For each indication YAML under
`knowledge_base/hosted/content/indications/`, look at every populated
field of the `expected_outcomes` block (schema-declared
`overall_response_rate`, `complete_response`, `progression_free_survival`,
`overall_survival_5y`, `hcv_cure_rate_svr12`, plus any extra free-form
fields the schema's `extra='allow'` admits) and classify each into one
of four buckets:

- ``cited``        — value mentions a `SRC-*` ID listed in
                     ``Indication.sources``, OR a recognized trial
                     abbreviation that resolves (by trial-number) to one
                     of those sources.
- ``probably-cited`` — value mentions a trial-family abbreviation
                     (e.g. ``KEYNOTE``) but the heuristic match to
                     ``Indication.sources`` is a fuzzy substring only,
                     not a confirmed trial-number match.
- ``uncited``      — value present and non-empty but no citation pointer
                     could be reconciled to ``Indication.sources``.
- ``absent``       — field missing or null.

Special handling
----------------
The schema's ``extra='allow'`` lets indications carry sibling fields
inside ``expected_outcomes`` that aren't outcome values at all — most
commonly ``notes``. We do **not** count ``notes`` itself as a separate
outcome row, but its text is appended to the citation-lookup haystack
of every sibling field in the same ``expected_outcomes`` block.
Without this, numeric sibling values (e.g.
``median_overall_survival_months: 46`` next to ``notes: "KEYNOTE-426"``)
are unfairly flagged ``uncited``.

We also skip a small set of free-form sibling keys that are conceptually
metadata, not outcomes (``notes``, ``note``, ``comment``, ``comments``,
``rationale``, ``follow_up``, ``followup``).

Output
------
Writes a markdown report to
``docs/audits/expected_outcomes_traceability_2026-05-01.md``
plus a long per-disease appendix at
``..._2026-05-01_by_disease.md``.

Re-runnable; deterministic ordering and fixed regexes make subsequent
runs produce byte-identical output as long as the underlying YAML is
unchanged.

Usage
-----
::

    py -3.12 scripts/audit_expected_outcomes.py            # full markdown audit
    py -3.12 scripts/audit_expected_outcomes.py --matrix   # tab-separated
                                                           # disease-id ↦ %-cited
                                                           # (loose) for the
                                                           # disease-coverage
                                                           # matrix integration

CLI flags are intentionally minimal — the markdown-audit mode always writes
to the canonical paths above. Override only via direct edit when refreshing
for a new audit date. The ``--matrix`` mode (Phase 2 deliverable for the
Pivotal Trial Outcomes Ingestion Plan) emits a stable ``DIS-*\\t<pct>``
stream consumed by ``scripts/disease_coverage_matrix.py`` so the per-
disease coverage matrix gains an ``Outcomes-Cited %`` column without
duplicating the bucketing logic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import yaml

# ── Configuration ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
INDICATIONS_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "indications"
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
DISEASES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
AUDIT_DIR = REPO_ROOT / "docs" / "audits"
AUDIT_DATE = "2026-05-01"
MAIN_OUT = AUDIT_DIR / f"expected_outcomes_traceability_{AUDIT_DATE}.md"
APPENDIX_OUT = AUDIT_DIR / f"expected_outcomes_traceability_{AUDIT_DATE}_by_disease.md"
BACKLOG_OUT = AUDIT_DIR / f"expected_outcomes_traceability_{AUDIT_DATE}_backlog.json"
LEGACY_UNCITED_SOURCE_ID = "SRC-LEGACY-UNCITED"

# Schema-declared `expected_outcomes` fields (knowledge_base/schemas/indication.py
# `ExpectedOutcomes`). Anything else found inside the block is "extra".
SCHEMA_OUTCOME_FIELDS = (
    "overall_response_rate",
    "complete_response",
    "progression_free_survival",
    "overall_survival_5y",
    "overall_survival_median",
    "disease_free_survival_hr",
    "hcv_cure_rate_svr12",
)

# Free-form sibling keys that live inside `expected_outcomes` blocks
# but are metadata, not outcome values. Excluded from the bucketing
# entirely; their text is appended to siblings' citation haystacks.
NON_OUTCOME_SIBLINGS = frozenset(
    {
        "notes",
        "note",
        "comment",
        "comments",
        "rationale",
        "follow_up",
        "followup",
        "follow-up",
        "caveats",
        "caveat",
    }
)

# Trial-naming patterns. Order matters only for documentation; matching
# is OR-style. Each pattern captures the "brand+number" so we can do a
# precise (number-level) reconciliation against Indication.sources.
#
# Anchored to avoid greedy over-match. Patterns are case-insensitive at
# match time. `_TRIAL_NUMBER_PATTERNS` is the strict set; the broader
# `_TRIAL_FAMILY_PATTERNS` covers brand-only mentions (e.g. "FLAURA",
# "CROWN", "MAIA") which have no number to reconcile.
_TRIAL_NUMBER_PATTERNS = [
    r"KEYNOTE-\d+\w?",
    r"CheckMate-?\d+",
    r"DESTINY-Breast\d+",
    r"DESTINY-Lung\d+",
    r"DESTINY-Gastric\d+",
    r"DESTINY-CRC\d+",
    r"DESTINY-PanTumor\d+",
    r"IMpower\d+",
    r"IMbrave\d+",
    r"KEYLYNK-\d+",
    r"PALOMA-\d+",
    r"MONALEESA-\d+",
    r"MONARCH\s?\d+",
    r"AURA\d+",
    r"SOLO\d+",
    r"SPOTLIGHT-\d+",
    r"LIBRETTO-\d+",
    r"ALTA-\d+",
    r"RATIONALE-\d+",
    r"EMPOWER-Lung-\d+",
    r"FLAURA\d*",
    r"ADAURA\d*",
    r"BREAKWATER\d*",
    r"BEACON\w*\d*",
    r"CROWN\d*",
    r"MOUNTAINEER\d*",
    r"GLOW\d*",
    r"HIMALAYA\d*",
    r"TROPiCS-\d+",
    r"INSPIRE\w*-\d+",
    r"TROPHIMMUN-\d+",
    r"PROfound\d*",
    r"PROpel\d*",
    r"VISION\d*",
    r"VIALE-\w+",
    r"RUBY\d*",
    r"COMMANDS\d*",
    r"PERSEUS\d*",
    r"BRUIN\d*",
    r"TRANSCEND\w*-?\d*",
    r"ZUMA-\d+",
    r"CARTITUDE-\d+",
    r"KarMMa-\d+",
    r"INTRIGUE\d*",
    r"GRIFFIN\d*",
    r"CASSIOPEIA\d*",
    r"ALCYONE\d*",
    r"MAIA\d*",
    r"CASTOR\d*",
    r"POLLUX\d*",
    r"EQUULEUS\d*",
    r"IMROZ\d*",
    r"IKEMA\d*",
    r"ICARIA\d*",
    r"ENZAMET\d*",
    r"ARASENS\d*",
    r"LATITUDE\d*",
    r"OlympiAD\d*",
    r"OLYMPIA\d*",
    r"ARROW\d*",
    r"ARIEL-?\d+",
    r"NAPOLI-?\d+",
    r"GeparOcto\d*",
    r"NeoSphere\d*",
    r"APHINITY\d*",
    r"ATHENA\d*",
    r"ASCENT\d*",
    r"PEARL\d*",
    r"ALEX\d*",
    r"PROFILE-?\d+",
    r"CodeBreaK-?\d+",
    r"KRYSTAL-?\d+",
    r"NSABP-?B?-?\d+",
    r"RATIFY\d*",
    r"QUAZAR\d*",
    r"VIALE-A\d*",
    r"CLEOPATRA\d*",
    r"PERTAIN\d*",
    r"EMERALD-?\d+",
    r"SOPHIA\d*",
    r"INAVO\d+",
    r"capitello-?\d+",
    r"CAPItello-?\d+",
    r"AETHERA\d*",
    r"ECHELON-?\d+",
    r"BRIGHT\w*\d*",
    r"AUGMENT\w*\d*",
    r"GOYA\d*",
    r"GALLIUM\d*",
    r"POLARIX\d*",
    r"ZUMA\d*",
    r"ELARA\d*",
    r"JULIET\d*",
    r"TRANSCEND\d*",
    r"GADOLIN\d*",
    r"AUGMENT-101\d*",
    r"INNOVATE\d*",
    r"NCT\d{8}",
]

# Brand-only patterns (no required number). Hits push a value into
# `probably-cited` if no number-level match was found.
_TRIAL_FAMILY_KEYWORDS = [
    "KEYNOTE",
    "CheckMate",
    "DESTINY",
    "IMpower",
    "IMbrave",
    "PALOMA",
    "MONALEESA",
    "MONARCH",
    "AURA",
    "SOLO",
    "SPOTLIGHT",
    "LIBRETTO",
    "ALTA",
    "RATIONALE",
    "EMPOWER",
    "FLAURA",
    "ADAURA",
    "BREAKWATER",
    "BEACON",
    "CROWN",
    "MOUNTAINEER",
    "GLOW",
    "HIMALAYA",
    "TROPiCS",
    "INSPIRE",
    "PROfound",
    "PROpel",
    "VISION",
    "VIALE",
    "RUBY",
    "COMMANDS",
    "PERSEUS",
    "BRUIN",
    "TRANSCEND",
    "ZUMA",
    "CARTITUDE",
    "KarMMa",
    "INTRIGUE",
    "GRIFFIN",
    "CASSIOPEIA",
    "ALCYONE",
    "MAIA",
    "CASTOR",
    "POLLUX",
    "EQUULEUS",
    "IMROZ",
    "IKEMA",
    "ICARIA",
    "ENZAMET",
    "ARASENS",
    "LATITUDE",
    "OlympiAD",
    "OLYMPIA",
    "ARROW",
    "ARIEL",
    "NAPOLI",
    "GeparOcto",
    "NeoSphere",
    "APHINITY",
    "ATHENA",
    "ASCENT",
    "PEARL",
    "ALEX",
    "PROFILE",
    "CodeBreaK",
    "KRYSTAL",
    "RATIFY",
    "QUAZAR",
    "CLEOPATRA",
    "EMERALD",
    "SOPHIA",
    "INAVO",
    "CAPItello",
    "capitello",
    "AETHERA",
    "ECHELON",
    "AUGMENT",
    "GOYA",
    "GALLIUM",
    "POLARIX",
    "ELARA",
    "JULIET",
    "GADOLIN",
    "INNOVATE",
    "RAINBOW",
    "ATTRACTION",
    "ORIENT",
    "ASCEMBL",
    "ASCEND",
    "ELEVATE",
    "MURANO",
    "CLL14",
    "CLL13",
    "CAPTIVATE",
    "GLOW",
    "ELOQUENT",
    "BOSTON",
    "ICARIA",
    "DREAMM",
    "BLOSSOM",
    "TOURMALINE",
    "POLLUX",
    "ENDURANCE",
    "HORIZON",
    "MAGNITUDE",
    "FIRSTMAPPP",
    "RESILIENT",
    "CASPIAN",
    "MERU",
    "MYSTIC",
    "PACIFIC",
    "POSEIDON",
    "AEGEAN",
    "INDUCT",
    "ELIANA",
]

# Pre-compile combined regexes once.
#
# Word boundaries are CRITICAL here. Without `\b` anchors, brand-only
# patterns like `ZUMA\d*` match the substring "zuma" inside drug names
# (`pembroliZUMAb`, `atezoliZUMAb`, `niVOLUmab` — `MAIA` likewise
# overlaps "MAIntenAnce"). We anchor with `\b` on both ends; the
# numeric tail (`\d+\w?`, `\d*`, etc.) keeps acting as before.
_NUMBER_RE = re.compile(
    r"\b(?:" + "|".join(_TRIAL_NUMBER_PATTERNS) + r")\b",
    re.IGNORECASE,
)
# Word-boundary brand keyword search. Case-sensitive — brand names are
# capitalized in the wild and lowercase noise (e.g. "vision" appearing
# in clinical-narrative free text) causes false hits.
_FAMILY_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(k) for k in _TRIAL_FAMILY_KEYWORDS) + r")\b"
)
_SRC_ID_RE = re.compile(r"SRC-[A-Z0-9][A-Z0-9_\-]*", re.IGNORECASE)


# ── Data classes ────────────────────────────────────────────────────────────


@dataclass
class FieldClassification:
    indication_id: str
    disease_id: str
    field_name: str
    bucket: str  # cited | probably-cited | uncited | absent
    value_excerpt: str = ""
    matched_via: str = ""
    remediation_hint: str = ""

    @property
    def is_present(self) -> bool:
        return self.bucket != "absent"


@dataclass
class IndicationStats:
    indication_id: str
    disease_id: str
    classifications: list[FieldClassification] = field(default_factory=list)

    def bucket_count(self, bucket: str) -> int:
        return sum(1 for c in self.classifications if c.bucket == bucket)


# ── Loading ─────────────────────────────────────────────────────────────────


def _safe_load(path: Path) -> dict | None:
    """Tolerant YAML load. Audit must not block on a malformed file."""
    try:
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def load_source_titles() -> dict[str, str]:
    """Map SRC-* id → lowercase concatenated title+notes for substring
    lookups by indication. Tolerant of partial files."""
    out: dict[str, str] = {}
    for path in sorted(SOURCES_DIR.glob("*.yaml")):
        data = _safe_load(path)
        if not data:
            continue
        sid = data.get("id")
        if not isinstance(sid, str):
            continue
        haystack_parts: list[str] = []
        for key in ("title", "notes", "url", "doi"):
            v = data.get(key)
            if isinstance(v, str):
                haystack_parts.append(v)
        out[sid.upper()] = " ".join(haystack_parts).lower()
    return out


def load_disease_names() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(DISEASES_DIR.glob("*.yaml")):
        data = _safe_load(path)
        if not data:
            continue
        did = data.get("id")
        names = data.get("names") or {}
        preferred = ""
        if isinstance(names, dict):
            preferred = names.get("preferred") or names.get("english") or ""
        if isinstance(did, str):
            out[did] = preferred or did
    return out


# ── Classification logic ─────────────────────────────────────────────────────


def _value_to_text(v: object) -> str:
    """Render a YAML scalar (or list/dict) into a single search string."""
    if v is None:
        return ""
    if isinstance(v, (str, int, float, bool)):
        return str(v)
    if isinstance(v, list):
        return " ".join(_value_to_text(x) for x in v)
    if isinstance(v, dict):
        return " ".join(_value_to_text(x) for x in v.values())
    return str(v)


def _is_blank(v: object) -> bool:
    """True if this YAML value carries no information."""
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict)):
        return len(v) == 0
    return False


def _extract_source_ids(text: str) -> set[str]:
    return {m.group(0).upper() for m in _SRC_ID_RE.finditer(text)}


def _extract_structured_source_ids(value: object) -> set[str]:
    """Return explicit source IDs from native OutcomeValue-shaped dicts.

    The Phase-2 schema lets an outcome be authored as:

        progression_free_survival:
          value: "..."
          source: SRC-...
          source_refs: [SRC-..., SRC-...]

    Older audits only searched rendered text, which missed the intent of
    this native shape. Keep the extractor narrow so arbitrary nested prose
    still goes through the existing regex path.
    """
    if not isinstance(value, dict):
        return set()

    out: set[str] = set()
    for key in ("source", "source_id"):
        raw = value.get(key)
        if isinstance(raw, str) and raw.upper().startswith("SRC-"):
            out.add(raw.upper())

    for key in ("source_refs", "sources"):
        raw_list = value.get(key) or []
        if not isinstance(raw_list, list):
            continue
        for item in raw_list:
            if isinstance(item, str) and item.upper().startswith("SRC-"):
                out.add(item.upper())
            elif isinstance(item, dict):
                sid = item.get("source_id") or item.get("source")
                if isinstance(sid, str) and sid.upper().startswith("SRC-"):
                    out.add(sid.upper())
    return out


def _extract_trial_numbers(text: str) -> set[str]:
    return {m.group(0) for m in _NUMBER_RE.finditer(text)}


def _has_trial_family(text: str) -> bool:
    return _FAMILY_RE.search(text) is not None


def _trial_number_resolves(
    trial_number: str,
    source_ids: Iterable[str],
    source_titles: dict[str, str],
) -> bool:
    """True if the trial-number string matches a substring of any
    Indication source's id or title."""
    needle_low = trial_number.lower()
    needle_compact = re.sub(r"[\s\-]", "", needle_low)
    for sid in source_ids:
        if needle_low in sid.lower() or needle_compact in re.sub(r"[\s\-]", "", sid.lower()):
            return True
        title = source_titles.get(sid.upper(), "")
        if needle_low in title or needle_compact in re.sub(r"[\s\-]", "", title):
            return True
    return False


def classify_value(
    value_text: str,
    sibling_haystack: str,
    indication_source_ids: set[str],
    source_titles: dict[str, str],
    structured_source_ids: set[str] | None = None,
) -> tuple[str, str]:
    """Return (bucket, matched_via)."""
    full_text = f"{value_text} {sibling_haystack}".strip()
    explicit = {sid.upper() for sid in (structured_source_ids or set())}
    known_source_ids = set(source_titles)

    if (
        LEGACY_UNCITED_SOURCE_ID in explicit
        or LEGACY_UNCITED_SOURCE_ID in _extract_source_ids(full_text)
    ):
        return "uncited", "legacy placeholder source"

    explicit_overlap = explicit & indication_source_ids
    if explicit_overlap:
        return "cited", f"OutcomeValue.source: {sorted(explicit_overlap)[0]}"

    explicit_known = explicit & known_source_ids
    if explicit_known:
        return (
            "probably-cited",
            f"OutcomeValue.source not in indication.sources: {sorted(explicit_known)[0]}",
        )

    if explicit:
        return "probably-cited", f"OutcomeValue.source unresolved: {sorted(explicit)[0]}"

    # 1. Direct SRC-* mention that's in this indication's sources?
    src_hits = _extract_source_ids(full_text)
    if LEGACY_UNCITED_SOURCE_ID in src_hits:
        return "uncited", "legacy placeholder source"
    overlap = src_hits & indication_source_ids
    if overlap:
        return "cited", f"SRC-id hit: {sorted(overlap)[0]}"

    # 2. Trial number that resolves to one of the indication's sources?
    nums = _extract_trial_numbers(full_text)
    for n in sorted(nums):
        if _trial_number_resolves(n, indication_source_ids, source_titles):
            return "cited", f"trial-number resolved: {n}"

    # 3. Trial number present but didn't resolve → probably-cited.
    if nums:
        return "probably-cited", f"trial-number unresolved: {sorted(nums)[0]}"

    # 4. Brand-only family keyword present → probably-cited.
    if _has_trial_family(full_text):
        m = _FAMILY_RE.search(full_text)
        return "probably-cited", f"trial-family: {m.group(0) if m else ''}"

    # 5. Stray SRC-* hit that didn't intersect this indication's sources?
    if src_hits:
        return "probably-cited", f"SRC-id (not in indication.sources): {sorted(src_hits)[0]}"

    return "uncited", ""


def _remediation_hint(bucket: str, matched_via: str) -> str:
    if bucket in {"cited", "absent"}:
        return ""
    if "legacy placeholder" in matched_via:
        return (
            "Replace SRC-LEGACY-UNCITED with the real pivotal-trial or "
            "guideline Source ID after clinician/source review."
        )
    if "not in indication.sources" in matched_via:
        return (
            "Confirm the source supports this exact outcome, then add it to "
            "Indication.sources or correct the outcome-level source."
        )
    if "unresolved" in matched_via:
        return "Create/fix the Source entity before accepting this outcome anchor."
    if bucket == "probably-cited":
        return (
            "Resolve the trial hint to a concrete SRC-* ID and author the "
            "outcome as an OutcomeValue dict."
        )
    return (
        "Trace this value to a specific publication/guideline Source and "
        "replace the scalar with an OutcomeValue dict."
    )


def classify_indication(
    data: dict,
    source_titles: dict[str, str],
) -> IndicationStats:
    ind_id = str(data.get("id") or "")
    applicable = data.get("applicable_to") or {}
    disease_id = ""
    if isinstance(applicable, dict):
        disease_id = str(applicable.get("disease_id") or "")

    sources = data.get("sources") or []
    source_ids: set[str] = set()
    if isinstance(sources, list):
        for s in sources:
            if isinstance(s, dict):
                sid = s.get("source_id")
                if isinstance(sid, str):
                    source_ids.add(sid.upper())
            elif isinstance(s, str):
                source_ids.add(s.upper())

    stats = IndicationStats(indication_id=ind_id, disease_id=disease_id)

    eo = data.get("expected_outcomes")
    if not isinstance(eo, dict):
        eo = {}

    # Build sibling haystack from non-outcome sibling keys (notes etc.).
    sibling_haystack_parts: list[str] = []
    for k, v in eo.items():
        if k.lower() in NON_OUTCOME_SIBLINGS:
            sibling_haystack_parts.append(_value_to_text(v))
    sibling_haystack = " ".join(sibling_haystack_parts)

    # Outcome fields = schema-declared union ∪ extra non-metadata siblings.
    outcome_keys: list[str] = []
    for k in SCHEMA_OUTCOME_FIELDS:
        outcome_keys.append(k)
    for k in eo.keys():
        if k in SCHEMA_OUTCOME_FIELDS:
            continue
        if k.lower() in NON_OUTCOME_SIBLINGS:
            continue
        outcome_keys.append(k)
    # de-dupe preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for k in outcome_keys:
        if k not in seen:
            seen.add(k)
            deduped.append(k)
    outcome_keys = deduped

    for fname in sorted(outcome_keys):
        v = eo.get(fname)
        if _is_blank(v):
            stats.classifications.append(
                FieldClassification(
                    indication_id=ind_id,
                    disease_id=disease_id,
                    field_name=fname,
                    bucket="absent",
                )
            )
            continue
        text = _value_to_text(v)
        structured_source_ids = _extract_structured_source_ids(v)
        bucket, matched_via = classify_value(
            value_text=text,
            sibling_haystack=sibling_haystack,
            indication_source_ids=source_ids,
            source_titles=source_titles,
            structured_source_ids=structured_source_ids,
        )
        excerpt = text if len(text) <= 120 else text[:117] + "..."
        stats.classifications.append(
            FieldClassification(
                indication_id=ind_id,
                disease_id=disease_id,
                field_name=fname,
                bucket=bucket,
                value_excerpt=excerpt,
                matched_via=matched_via,
                remediation_hint=_remediation_hint(bucket, matched_via),
            )
        )

    return stats


# ── Roll-ups ────────────────────────────────────────────────────────────────


@dataclass
class DiseaseRollup:
    disease_id: str
    cited: int = 0
    probably_cited: int = 0
    uncited: int = 0
    absent: int = 0
    indications: int = 0

    @property
    def populated(self) -> int:
        return self.cited + self.probably_cited + self.uncited

    @property
    def total_field_slots(self) -> int:
        return self.populated + self.absent

    @property
    def outcomes_cited_pct(self) -> float:
        if self.populated == 0:
            return 0.0
        return 100.0 * (self.cited + self.probably_cited) / self.populated

    @property
    def cited_pct_strict(self) -> float:
        if self.populated == 0:
            return 0.0
        return 100.0 * self.cited / self.populated


def rollup_by_disease(
    all_stats: list[IndicationStats],
) -> dict[str, DiseaseRollup]:
    out: dict[str, DiseaseRollup] = defaultdict(lambda: DiseaseRollup(disease_id=""))
    for s in all_stats:
        d = s.disease_id or "(unknown)"
        r = out[d]
        r.disease_id = d
        r.indications += 1
        for c in s.classifications:
            if c.bucket == "cited":
                r.cited += 1
            elif c.bucket == "probably-cited":
                r.probably_cited += 1
            elif c.bucket == "uncited":
                r.uncited += 1
            else:
                r.absent += 1
    return dict(out)


# ── Markdown rendering ──────────────────────────────────────────────────────


def _pct(num: int, denom: int) -> str:
    if denom == 0:
        return "n/a"
    return f"{100.0 * num / denom:.1f}%"


def render_main(
    all_stats: list[IndicationStats],
    rollups: dict[str, DiseaseRollup],
    disease_names: dict[str, str],
    appendix_path: Path,
) -> str:
    total_indications = len(all_stats)
    cited = sum(s.bucket_count("cited") for s in all_stats)
    probably = sum(s.bucket_count("probably-cited") for s in all_stats)
    uncited = sum(s.bucket_count("uncited") for s in all_stats)
    absent = sum(s.bucket_count("absent") for s in all_stats)
    populated = cited + probably + uncited
    total_slots = populated + absent

    lines: list[str] = []
    lines.append(
        f"# `expected_outcomes` traceability audit ({AUDIT_DATE})"
    )
    lines.append("")
    lines.append(
        "Phase 1 deliverable for "
        "[`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`]"
        "(../plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md). "
        "Read-only baseline of how well each indication's "
        "`expected_outcomes` block traces back to its `Indication.sources`. "
        "Re-run via `py -3.12 scripts/audit_expected_outcomes.py`."
    )
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "For every YAML at `knowledge_base/hosted/content/indications/*.yaml`, "
        "every populated field of `expected_outcomes` (schema fields plus "
        "any extra `extra='allow'` siblings) is bucketed:"
    )
    lines.append("")
    lines.append(
        "- **`cited`** — value contains a `SRC-*` id from "
        "`Indication.sources`, or a recognized trial abbreviation "
        "(e.g. `KEYNOTE-006`, `CheckMate-577`) whose number resolves "
        "by substring to one of the indication's source ids or titles."
    )
    lines.append(
        "- **`probably-cited`** — value contains a trial-family keyword "
        "or trial number that did not resolve to `Indication.sources`. "
        "A SRC id from outside the indication's source list also lands here."
    )
    lines.append(
        "- **`uncited`** — value present and non-empty but no citation "
        "pointer. This is the Phase-3 remediation backlog."
    )
    lines.append(
        "- **`absent`** — field is null or missing."
    )
    lines.append("")
    lines.append(
        "Sibling keys inside `expected_outcomes` that are conceptually "
        "metadata (`notes`, `note`, `comment`, `comments`, `rationale`, "
        "`follow_up`, `caveats`) are **not** counted as outcome fields, "
        "but their text **is** appended to the citation-lookup haystack "
        "of every sibling outcome value in the same block. This handles "
        "the common pattern `{median_overall_survival_months: 46, "
        "notes: \"KEYNOTE-426\"}` where the trial name lives in `notes` "
        "and the numeric value cannot self-cite."
    )
    lines.append("")
    lines.append(
        "Trial-name regexes are an explicit allowlist hard-coded in "
        "`scripts/audit_expected_outcomes.py`. They cover the common "
        "modern oncology trials (KEYNOTE, CheckMate, DESTINY-Breast, "
        "IMpower / IMbrave, etc.) but are deliberately incomplete — "
        "uncovered trials will land as `uncited` rather than "
        "`probably-cited`. False negatives here under-state the citation "
        "rate; tighten the allowlist as new trial families enter the KB."
    )
    lines.append("")

    lines.append("## Headline numbers")
    lines.append("")
    lines.append(f"- **Indications audited:** {total_indications}")
    lines.append(f"- **Outcome-field slots (populated + absent):** {total_slots}")
    lines.append(f"- **Populated outcome-field slots:** {populated}")
    lines.append("")
    lines.append("| Bucket | Count | % of populated | % of all slots |")
    lines.append("|---|---:|---:|---:|")
    for label, n in (
        ("cited", cited),
        ("probably-cited", probably),
        ("uncited", uncited),
    ):
        lines.append(
            f"| `{label}` | {n} | {_pct(n, populated)} | {_pct(n, total_slots)} |"
        )
    lines.append(
        f"| `absent` | {absent} | n/a | {_pct(absent, total_slots)} |"
    )
    lines.append("")
    cited_or_probably = cited + probably
    lines.append(
        f"**Combined `cited + probably-cited`:** {cited_or_probably} / "
        f"{populated} = {_pct(cited_or_probably, populated)} of populated "
        "outcome values carry a citation pointer (loose definition). "
        f"Strict-cited only: {cited} / {populated} = "
        f"{_pct(cited, populated)}."
    )
    lines.append("")
    lines.append(
        "Plan v1.0 target is ≥90% citation-traceable on the strict "
        "definition. Today's `cited`-only rate is the gap to close."
    )
    lines.append("")

    # Diseases ranked
    rollup_list = sorted(rollups.values(), key=lambda r: r.disease_id)

    lines.append("## Top 10 worst-offender diseases (by absolute `uncited` count)")
    lines.append("")
    lines.append(
        "Sorted by raw `uncited` count: the diseases with the largest "
        "Phase-3 remediation backlog measured in cells, not percentage."
    )
    lines.append("")
    lines.append(
        "| # | Disease | Indications | populated | uncited | probably-cited | cited | outcomes-cited % (loose) |"
    )
    lines.append(
        "|---:|---|---:|---:|---:|---:|---:|---:|"
    )
    worst = sorted(
        rollup_list,
        key=lambda r: (-r.uncited, -r.indications, r.disease_id),
    )[:10]
    for i, r in enumerate(worst, 1):
        name = disease_names.get(r.disease_id, r.disease_id)
        lines.append(
            f"| {i} | `{r.disease_id}` — {name} | {r.indications} | "
            f"{r.populated} | {r.uncited} | {r.probably_cited} | "
            f"{r.cited} | {r.outcomes_cited_pct:.1f}% |"
        )
    lines.append("")

    lines.append("## Top 10 best-cited diseases (by outcomes-cited %)")
    lines.append("")
    lines.append(
        "Sorted by `(cited + probably-cited) / populated`. Tie-broken by "
        "absolute `cited` count, then disease id. Diseases with zero "
        "populated outcome fields are excluded."
    )
    lines.append("")
    lines.append(
        "| # | Disease | Indications | populated | cited | probably-cited | uncited | outcomes-cited % (loose) |"
    )
    lines.append(
        "|---:|---|---:|---:|---:|---:|---:|---:|"
    )
    eligible_for_best = [r for r in rollup_list if r.populated > 0]
    best = sorted(
        eligible_for_best,
        key=lambda r: (-r.outcomes_cited_pct, -r.cited, r.disease_id),
    )[:10]
    for i, r in enumerate(best, 1):
        name = disease_names.get(r.disease_id, r.disease_id)
        lines.append(
            f"| {i} | `{r.disease_id}` — {name} | {r.indications} | "
            f"{r.populated} | {r.cited} | {r.probably_cited} | "
            f"{r.uncited} | {r.outcomes_cited_pct:.1f}% |"
        )
    lines.append("")

    # Per-disease rollup (full)
    lines.append("## Per-disease rollup (all diseases, alphabetical)")
    lines.append("")
    lines.append(
        "| Disease | Indications | populated | absent | cited | probably-cited | uncited | outcomes-cited % (loose) |"
    )
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|"
    )
    for r in rollup_list:
        name = disease_names.get(r.disease_id, r.disease_id)
        lines.append(
            f"| `{r.disease_id}` — {name} | {r.indications} | "
            f"{r.populated} | {r.absent} | {r.cited} | "
            f"{r.probably_cited} | {r.uncited} | "
            f"{r.outcomes_cited_pct:.1f}% |"
        )
    lines.append("")

    # Worst 3 diseases — full per-indication detail in the main doc.
    lines.append("## Worst 3 diseases — full per-indication detail")
    lines.append("")
    lines.append(
        "Per the plan brief, the worst three diseases (by `uncited` "
        "count) are inlined here. The remaining diseases' per-indication "
        f"detail lives in the appendix [`{appendix_path.name}`]({appendix_path.name})."
    )
    lines.append("")
    by_disease = defaultdict(list)
    for s in all_stats:
        by_disease[s.disease_id].append(s)
    for r in worst[:3]:
        name = disease_names.get(r.disease_id, r.disease_id)
        lines.append(f"### `{r.disease_id}` — {name}")
        lines.append("")
        lines.append(
            f"Indications: {r.indications}; populated: {r.populated}; "
            f"cited: {r.cited}; probably-cited: {r.probably_cited}; "
            f"uncited: {r.uncited}; absent: {r.absent}."
        )
        lines.append("")
        lines.extend(_render_disease_detail(by_disease.get(r.disease_id, [])))
        lines.append("")

    # Plan implications
    lines.append("## Plan implications — Phase 3 prioritization")
    lines.append("")
    lines.append(
        "The plan (`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md` "
        "Phase 3) sequences Phase-3 chunks as:"
    )
    lines.append("")
    lines.append(
        "1. **8 shelf-task items first** — KEYNOTE-006/-054, EXTREME, "
        "CPX-351, GO, loncastuximab, zanu 1L CLL, CheckMate-577."
    )
    lines.append(
        "2. **High-volume diseases** with uncited outcomes — NSCLC, "
        "breast, CRC, prostate, AML, DLBCL."
    )
    lines.append(
        "3. **Other diseases** alphabetical until ≥90% threshold met."
    )
    lines.append("")
    lines.append(
        "### Audit findings vs plan order"
    )
    lines.append("")
    lines.append(
        "Below: how this audit's measured `uncited` counts re-shuffle "
        "that order. Diseases with **higher** uncited counts than the "
        "plan implies should move up; diseases already in good shape "
        "(high cited %, low uncited count) should drop down."
    )
    lines.append("")
    lines.append(
        "| Plan-listed high-volume disease | DIS id (best guess) | populated | uncited | cited | outcomes-cited % | suggested action |"
    )
    lines.append(
        "|---|---|---:|---:|---:|---:|---|"
    )
    # Plan names "DLBCL"; KB ID is DIS-DLBCL-NOS. Map carefully.
    plan_targets = [
        ("NSCLC", "DIS-NSCLC"),
        ("Breast", "DIS-BREAST"),
        ("CRC", "DIS-CRC"),
        ("Prostate", "DIS-PROSTATE"),
        ("AML", "DIS-AML"),
        ("DLBCL", "DIS-DLBCL-NOS"),
    ]
    for label, did in plan_targets:
        r = rollups.get(did)
        if r is None:
            lines.append(
                f"| {label} | `{did}` | — | — | — | — | not found in KB rollup; verify disease id |"
            )
            continue
        if r.uncited >= 5:
            action = "prioritize as planned"
        elif r.outcomes_cited_pct >= 75:
            action = "**better than plan assumes — defer**"
        else:
            action = "keep in queue, mid-priority"
        lines.append(
            f"| {label} | `{did}` | {r.populated} | {r.uncited} | "
            f"{r.cited} | {r.outcomes_cited_pct:.1f}% | {action} |"
        )
    lines.append("")
    lines.append(
        "### Diseases worse than plan assumes (top-10 worst, not in plan list)"
    )
    lines.append("")
    plan_ids = {did for _, did in plan_targets}
    surprises = [r for r in worst if r.disease_id not in plan_ids][:10]
    if not surprises:
        lines.append(
            "_None — every top-10 worst-offender is already on the "
            "plan's high-volume list._"
        )
    else:
        lines.append(
            "These diseases have larger `uncited` backlogs than the "
            "plan's named high-volume list and should be promoted into "
            "Phase-3 chunk planning earlier than alphabetical order."
        )
        lines.append("")
        lines.append(
            "| Disease | populated | uncited | cited | outcomes-cited % |"
        )
        lines.append("|---|---:|---:|---:|---:|")
        for r in surprises:
            name = disease_names.get(r.disease_id, r.disease_id)
            lines.append(
                f"| `{r.disease_id}` — {name} | {r.populated} | "
                f"{r.uncited} | {r.cited} | {r.outcomes_cited_pct:.1f}% |"
            )
    lines.append("")
    lines.append(
        "### Diseases better than plan assumes (skip / defer)"
    )
    lines.append("")
    bench = [
        r for r in rollup_list
        if r.populated >= 4 and r.outcomes_cited_pct >= 80
    ]
    bench.sort(key=lambda r: (-r.outcomes_cited_pct, -r.populated, r.disease_id))
    if not bench:
        lines.append(
            "_No diseases meet the (≥4 populated outcomes AND ≥80% "
            "loose-cited) skip threshold._"
        )
    else:
        lines.append(
            "Diseases with ≥4 populated outcome values and ≥80% "
            "loose-cited rate. Phase 3 can deprioritize these — the "
            "marginal cost of remediating the residual uncited cells is "
            "high relative to other backlog."
        )
        lines.append("")
        lines.append(
            "| Disease | populated | cited | probably-cited | uncited | outcomes-cited % |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|")
        for r in bench[:15]:
            name = disease_names.get(r.disease_id, r.disease_id)
            lines.append(
                f"| `{r.disease_id}` — {name} | {r.populated} | "
                f"{r.cited} | {r.probably_cited} | {r.uncited} | "
                f"{r.outcomes_cited_pct:.1f}% |"
            )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"_Generated by `scripts/audit_expected_outcomes.py` on {AUDIT_DATE}. "
        f"Indications audited: {total_indications}. Underlying KB tree: "
        "`knowledge_base/hosted/content/`._"
    )
    lines.append("")
    return "\n".join(lines)


def _render_disease_detail(stats_for_disease: list[IndicationStats]) -> list[str]:
    out: list[str] = []
    out.append(
        "| Indication | Field | Bucket | Matched via | Remediation | Value excerpt |"
    )
    out.append("|---|---|---|---|---|---|")
    rows: list[tuple[str, str, str, str, str, str]] = []
    for s in sorted(stats_for_disease, key=lambda x: x.indication_id):
        for c in s.classifications:
            if c.bucket == "absent":
                # don't print absent rows in the per-indication detail —
                # they balloon the table; the rollup already counts them.
                continue
            rows.append(
                (
                    s.indication_id,
                    c.field_name,
                    c.bucket,
                    c.matched_via or "—",
                    (c.remediation_hint or "review only").replace("\n", " ").replace("|", "\\|"),
                    (c.value_excerpt or "").replace("\n", " ").replace("|", "\\|"),
                )
            )
    if not rows:
        out.append("| _(no populated outcome fields)_ | | | | | |")
        return out
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return out


def render_appendix(
    all_stats: list[IndicationStats],
    rollups: dict[str, DiseaseRollup],
    disease_names: dict[str, str],
    skip_diseases: set[str],
) -> str:
    by_disease = defaultdict(list)
    for s in all_stats:
        by_disease[s.disease_id].append(s)

    lines: list[str] = []
    lines.append(
        f"# `expected_outcomes` traceability — per-disease appendix ({AUDIT_DATE})"
    )
    lines.append("")
    lines.append(
        "Per-indication detail tables for every disease **except** the "
        "worst-3 (which are inlined in the main report "
        f"`expected_outcomes_traceability_{AUDIT_DATE}.md`)."
    )
    lines.append("")
    lines.append(
        "Rows are limited to populated outcome fields. `absent` rows are "
        "summarized in the rollup line at the head of each section, not "
        "listed individually."
    )
    lines.append("")
    rollup_list = sorted(rollups.values(), key=lambda r: r.disease_id)
    for r in rollup_list:
        if r.disease_id in skip_diseases:
            continue
        name = disease_names.get(r.disease_id, r.disease_id)
        lines.append(f"## `{r.disease_id}` — {name}")
        lines.append("")
        lines.append(
            f"Indications: {r.indications}; populated: {r.populated}; "
            f"cited: {r.cited}; probably-cited: {r.probably_cited}; "
            f"uncited: {r.uncited}; absent: {r.absent}; "
            f"outcomes-cited % (loose): {r.outcomes_cited_pct:.1f}%."
        )
        lines.append("")
        lines.extend(_render_disease_detail(by_disease.get(r.disease_id, [])))
        lines.append("")
    return "\n".join(lines)


# ── Public helpers (Phase 2 — matrix integration) ───────────────────────────


def _classify_all() -> tuple[list[IndicationStats], dict[str, DiseaseRollup]]:
    """Run the audit's classification pass and return (per-indication stats,
    per-disease rollups). Shared between the markdown-audit mode and the
    matrix-emit mode so bucketing logic stays single-sourced."""
    source_titles = load_source_titles()
    all_stats: list[IndicationStats] = []
    for path in sorted(INDICATIONS_DIR.glob("*.yaml")):
        data = _safe_load(path)
        if data is None:
            continue
        all_stats.append(classify_indication(data, source_titles))
    all_stats.sort(key=lambda s: s.indication_id)
    return all_stats, rollup_by_disease(all_stats)


def disease_outcomes_cited_pct() -> dict[str, float]:
    """Return ``{disease_id: outcomes_cited_pct (loose)}`` for every disease
    that owns ≥1 indication.

    Phase 2 deliverable — consumed by
    ``scripts/disease_coverage_matrix.py`` to populate the new
    ``Outcomes-Cited %`` column without re-implementing the bucketing.

    "Loose" = ``(cited + probably-cited) / populated``, matching the
    headline metric in the markdown audit. Diseases with zero populated
    outcome fields return 0.0 (vs. ``n/a`` in the markdown — the matrix
    column needs a numeric value for sorting).
    """
    _, rollups = _classify_all()
    return {did: r.outcomes_cited_pct for did, r in rollups.items()}


def build_remediation_backlog(all_stats: list[IndicationStats]) -> list[dict]:
    """Machine-readable backlog for Phase-3 outcome-citation work.

    The markdown audit is readable, but hard to assign in chunks. This JSON
    output lets contributors filter by disease, bucket, or indication and
    work only the highest-value uncited cells.
    """
    rows: list[dict] = []
    priority_by_bucket = {"uncited": 0, "probably-cited": 1}
    for stats in all_stats:
        for c in stats.classifications:
            if c.bucket not in priority_by_bucket:
                continue
            rows.append(
                {
                    "disease_id": c.disease_id,
                    "indication_id": c.indication_id,
                    "field_name": c.field_name,
                    "bucket": c.bucket,
                    "matched_via": c.matched_via,
                    "remediation_hint": c.remediation_hint,
                    "value_excerpt": c.value_excerpt,
                }
            )
    return sorted(
        rows,
        key=lambda r: (
            priority_by_bucket.get(r["bucket"], 9),
            r["disease_id"],
            r["indication_id"],
            r["field_name"],
        ),
    )


# ── Main ────────────────────────────────────────────────────────────────────


def _run_matrix_mode() -> int:
    """Emit ``<DIS-*>\\t<pct>`` lines to stdout. Stable order: by disease id."""
    pct_map = disease_outcomes_cited_pct()
    for did in sorted(pct_map):
        print(f"{did}\t{pct_map[did]:.2f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit `Indication.expected_outcomes` traceability. "
            "Default mode writes the markdown audit; --matrix emits "
            "tab-separated disease-id ↦ outcomes-cited % for the "
            "coverage-matrix integration."
        )
    )
    parser.add_argument(
        "--matrix",
        action="store_true",
        help=(
            "Emit `<DIS-*>\\t<pct>` lines (loose outcomes-cited %) to "
            "stdout instead of writing the markdown audit. "
            "Consumed by scripts/disease_coverage_matrix.py."
        ),
    )
    args = parser.parse_args(argv)

    if not INDICATIONS_DIR.is_dir():
        print(f"FATAL: indications dir not found: {INDICATIONS_DIR}")
        return 2

    if args.matrix:
        return _run_matrix_mode()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    disease_names = load_disease_names()

    all_stats, rollups = _classify_all()

    # Identify worst-3 disease ids — they go inline; the rest into the appendix.
    worst3_ids = {
        r.disease_id
        for r in sorted(
            rollups.values(),
            key=lambda r: (-r.uncited, -r.indications, r.disease_id),
        )[:3]
    }

    main_md = render_main(all_stats, rollups, disease_names, APPENDIX_OUT)
    appendix_md = render_appendix(all_stats, rollups, disease_names, worst3_ids)
    backlog = build_remediation_backlog(all_stats)

    MAIN_OUT.write_text(main_md, encoding="utf-8")
    APPENDIX_OUT.write_text(appendix_md, encoding="utf-8")
    BACKLOG_OUT.write_text(
        json.dumps(
            {
                "audit_date": AUDIT_DATE,
                "generated_by": "scripts/audit_expected_outcomes.py",
                "target": ">=90% strict-cited populated outcome values",
                "rows": backlog,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    skipped = [
        path
        for path in sorted(INDICATIONS_DIR.glob("*.yaml"))
        if _safe_load(path) is None
    ]

    print(f"Wrote {MAIN_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {APPENDIX_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {BACKLOG_OUT.relative_to(REPO_ROOT)}")
    print(f"Indications audited: {len(all_stats)}")
    print(f"Backlog rows: {len(backlog)}")
    if skipped:
        print(f"Skipped (unparseable YAML): {len(skipped)}")
        for p in skipped:
            print(f"  - {p.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
