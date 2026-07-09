"""MonitoringSchedule entity — KNOWLEDGE_SCHEMA_SPECIFICATION §12."""

from typing import Optional

from pydantic import Field

from .base import Base


class MonitoringPhase(Base):
    name: str  # "baseline" | "on_treatment" | "follow_up_short" | "follow_up_long"
    window: Optional[str] = None  # "Week 0" | "Every cycle" | "Every 3 months"
    window_ua: Optional[str] = None  # translated companion; None if not yet drafted
    tests: list[str] = Field(default_factory=list)  # Test IDs
    visits: list[str] = Field(default_factory=list)  # free-form visit descriptors
    visits_ua: list[str] = Field(default_factory=list)  # parallel to `visits`, index-aligned
    checkpoints: list[str] = Field(default_factory=list)
    checkpoints_ua: list[str] = Field(default_factory=list)  # parallel to `checkpoints`, index-aligned
    notes: Optional[str] = None
    notes_ua: Optional[str] = None


class MonitoringSchedule(Base):
    id: str
    linked_to_regimen: Optional[str] = None  # Regimen ID; null for surveillance schedules
    phases: list[MonitoringPhase]

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
    notes_ua: Optional[str] = None
