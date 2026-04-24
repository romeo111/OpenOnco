"""MonitoringSchedule entity — KNOWLEDGE_SCHEMA_SPECIFICATION §12."""

from typing import Optional

from pydantic import Field

from .base import Base


class MonitoringPhase(Base):
    name: str  # "baseline" | "on_treatment" | "follow_up_short" | "follow_up_long"
    window: Optional[str] = None  # "Week 0" | "Every cycle" | "Every 3 months"
    tests: list[str] = Field(default_factory=list)  # Test IDs
    visits: list[str] = Field(default_factory=list)  # free-form visit descriptors
    checkpoints: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class MonitoringSchedule(Base):
    id: str
    linked_to_regimen: str  # Regimen ID
    phases: list[MonitoringPhase]

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
