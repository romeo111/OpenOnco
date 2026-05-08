"""RadiationCourse entity — KNOWLEDGE_SCHEMA_SPECIFICATION §17 (RATIFIED 2026-05-07).

Radiation therapy as a first-class treatment modality — CROSS 41.4 Gy / 23 fx,
SCRT 25 Gy / 5 fx, definitive CRT, SBRT, etc. Referenced from
`IndicationPhase.radiation_id` to model concurrent / sequential CRT and to
make total dose / fractionation / target volume queryable by the engine
and renderable as a phased timeline.

See `docs/plans/schema_17_refactor_2026-05-07.md` for the full rationale.
First RadiationCourse YAMLs land in Phase C of the GI-2 wave (CROSS,
definitive esophageal CRT, rectal SCRT, HCC SBRT).
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import Base, NamePair


class RadiationIntent(str, Enum):
    """Radiation intent vocabulary — distinct from SurgeryIntent because
    radiation oncology classifies intent differently (definitive CRT is a
    radiation-specific category that has no surgical analogue, and surgical
    'salvage' / 'diagnostic' don't translate to radiation). Planning doc §2.3."""

    NEOADJUVANT = "neoadjuvant"
    DEFINITIVE = "definitive"
    ADJUVANT = "adjuvant"
    PALLIATIVE = "palliative"


class RadiationCourse(Base):
    """Radiation therapy course entity — §17.1 ratified 2026-05-07.

    Files live at `knowledge_base/hosted/content/radiation_courses/rc_*.yaml`.
    `concurrent_chemo_regimen` (optional) must resolve to a Regimen entity
    if present (loader enforces ref-integrity per planning doc §2.4 rule 7).
    """

    id: str
    names: NamePair

    total_dose_gy: float
    fractions: int
    fraction_size_gy: Optional[float] = None  # often = total / fractions but explicit per §17.1

    target_volume: Optional[str] = None  # free-string e.g. "primary + involved nodes (CTV)"
    schedule: Optional[str] = None       # free-string e.g. "5 fx/week × 4.6 weeks"

    # Optional Regimen ID — concurrent CRT pattern (CROSS = carbo-paclitaxel
    # weekly with RT). Loader resolves via planning doc §2.4 rule 7.
    concurrent_chemo_regimen: Optional[str] = None

    intent: RadiationIntent

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
