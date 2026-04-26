"""OncoKB integration — shared dataclasses (Phase 2 of safe-rollout v3).

All types here are pure data containers (no I/O, no logic). They form
the contract between:

  Biomarker.oncokb_lookup → normalize_variant → OncoKBQuery
                                              → OncoKBClient (lookup)
                                              → OncoKBResult | OncoKBError
                                              → OncoKBLayer (engine output)
                                              → render layer (HCP-only)

Per safe-rollout v3 §0.1 invariant: nothing in this module reads from or
writes to the engine's track-builder. The architectural firewall against
§8.3 violation is enforced by an import-graph test (added in Phase 3b).

See specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md PROPOSAL §18 for the formal
schema spec entry.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal, Optional


# ── Variant + query primitives ───────────────────────────────────────────


@dataclass(frozen=True)
class NormalizedVariant:
    """Output of normalize_variant. Frozen for safe use as dict key.

    `oncokb_query_string` is what we pass to OncoKB's `alteration` URL
    parameter — verified format pending Phase 0 A6 (likely short HGVS-p
    like "V600E" or structured like "Exon 19 deletion").
    """

    gene: str  # HGNC symbol, uppercase
    oncokb_query_string: str
    raw: str  # original input — for traceability in errors/logs
    skip_reason: None = None  # always None on the success path


@dataclass(frozen=True)
class OncoKBQuery:
    """Single (gene, variant, oncotree) query. Composed in engine/oncokb_extract.py."""

    gene: str
    variant: str
    oncotree_code: Optional[str]
    source_biomarker_id: str  # for traceability + provenance event metadata


# ── Lookup results ───────────────────────────────────────────────────────


# OncoKB therapeutic levels we surface (per locked decision Q1: skip 1/2,
# show 3A/3B/4 + R1/R2). The proxy still receives 1/2 from OncoKB; the
# render layer filters them out via SURFACED_LEVELS below.
TherapeuticLevel = Literal["1", "2", "3A", "3B", "4", "R1", "R2"]

SURFACED_LEVELS: frozenset[str] = frozenset({"3A", "3B", "4", "R1", "R2"})
RESISTANCE_LEVELS: frozenset[str] = frozenset({"R1", "R2"})


@dataclass(frozen=True)
class OncoKBTherapeuticOption:
    level: str  # one of TherapeuticLevel values, but not enforced (proxy may emit "?")
    drugs: tuple[str, ...]
    description: Optional[str]
    pmids: tuple[str, ...]
    fda_approved: bool = False
    fda_approval_year: Optional[int] = None  # populated when available (Q8)


@dataclass(frozen=True)
class OncoKBResult:
    """Successful lookup. May still have empty therapeutic_options
    (negative result — biomarker is recognised but no actionable evidence)."""

    query: OncoKBQuery
    oncokb_url: str
    therapeutic_options: tuple[OncoKBTherapeuticOption, ...]
    cached: bool
    oncokb_data_version: Optional[str] = None  # populated when proxy receives it from upstream

    @property
    def is_negative(self) -> bool:
        return len(self.therapeutic_options) == 0

    @property
    def highest_level(self) -> Optional[str]:
        if not self.therapeutic_options:
            return None
        # Level rank: lower number = stronger; resistance R1/R2 sorted last
        return sorted(
            (opt.level for opt in self.therapeutic_options),
            key=_level_sort_key,
        )[0]


@dataclass(frozen=True)
class OncoKBError:
    """Failure mode. Engine wraps these in the layer instead of raising —
    fail-open contract per safe-rollout v3 §0 founding principle 3."""

    query: OncoKBQuery
    error_kind: Literal["timeout", "http_error", "parse_error", "circuit_open", "disabled"]
    detail: str  # human-readable; never contains secrets (proxy already scrubs)


# ── Resistance-conflict + layer ──────────────────────────────────────────


@dataclass(frozen=True)
class ResistanceConflict:
    """Detected when an engine-recommended drug appears in OncoKB R1/R2
    evidence for one of the patient's biomarkers. Per safe-rollout v3 §6
    this triggers (a) inline banner in track-card, (b) provenance event,
    (c) MDT role escalation (molecular_geneticist)."""

    track_id: str
    drug: str
    gene: str
    variant: str
    level: str  # "R1" | "R2"
    description: Optional[str]


@dataclass
class OncoKBLayer:
    """Engine output — surfaces alongside (NEVER inside) the two-track Plan.

    `render_plan_html(mode="hcp")` reads this. `render_plan_html(mode="patient")`
    MUST ignore it entirely (patient-mode HTML must contain zero OncoKB content
    per Q4-related invariant + AC-3)."""

    results: list[OncoKBResult] = field(default_factory=list)
    errors: list[OncoKBError] = field(default_factory=list)
    resistance_conflicts: list[ResistanceConflict] = field(default_factory=list)
    pan_tumor_fallback_used: bool = False  # warning badge per Q4

    @property
    def is_empty(self) -> bool:
        """Empty layer = render skips section entirely. Q3 + scrub-noise rule."""
        if self.resistance_conflicts:
            return False
        for r in self.results:
            if any(opt.level in SURFACED_LEVELS for opt in r.therapeutic_options):
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "results": [_result_to_dict(r) for r in self.results],
            "errors": [asdict(e) for e in self.errors],
            "resistance_conflicts": [asdict(c) for c in self.resistance_conflicts],
            "pan_tumor_fallback_used": self.pan_tumor_fallback_used,
        }


# ── Internals ────────────────────────────────────────────────────────────


_LEVEL_RANK: dict[str, int] = {
    "1": 0,
    "2": 1,
    "3A": 2,
    "3B": 3,
    "4": 4,
    "R1": 5,
    "R2": 6,
}


def _level_sort_key(level: str) -> int:
    return _LEVEL_RANK.get(level, 99)


def _result_to_dict(r: OncoKBResult) -> dict:
    return {
        "query": asdict(r.query),
        "oncokb_url": r.oncokb_url,
        "therapeutic_options": [asdict(o) for o in r.therapeutic_options],
        "cached": r.cached,
        "oncokb_data_version": r.oncokb_data_version,
    }


__all__ = [
    "NormalizedVariant",
    "OncoKBQuery",
    "OncoKBTherapeuticOption",
    "OncoKBResult",
    "OncoKBError",
    "ResistanceConflict",
    "OncoKBLayer",
    "TherapeuticLevel",
    "SURFACED_LEVELS",
    "RESISTANCE_LEVELS",
]
