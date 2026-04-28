"""CLI flag wiring tests — engine/cli.py.

Renamed from test_oncokb_cli.py during the CIViC pivot. The previous
flags (--oncokb-proxy / --oncokb-timeout) were removed in Phase 1
because the OncoKB proxy is gone (license conflict with CHARTER §2 —
see docs/reviews/oncokb-public-civic-coverage-2026-04-27.md).

Phase 2 will add `--civic-snapshot PATH` once SnapshotActionabilityClient
ships. Until then this module skips, preserving the contract
documentation (default-OFF, no accidental network calls)."""

from __future__ import annotations

import pytest

pytest.skip(
    "phase-2: CLI flag set redefined for CIViC (--civic-snapshot pending). "
    "Default-OFF behaviour is still pinned by test_actionability_invariants.",
    allow_module_level=True,
)
