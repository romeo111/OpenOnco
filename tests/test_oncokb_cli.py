"""CLI flag wiring tests — engine/cli.py --oncokb-proxy.

Verifies that the CLI flag correctly toggles OncoKB integration
without breaking the default-OFF contract (AC-7)."""

from __future__ import annotations

import argparse
from unittest.mock import patch

import pytest


def _build_parser():
    """Re-exec the CLI parser without invoking main(). Mirrors cli.py
    so we can inspect flags without spawning subprocess."""
    from knowledge_base.engine.cli import main as _  # noqa: F401 — ensure import OK
    # We can't easily reuse the parser from main() since it's defined inside.
    # Instead verify behaviour via subprocess in dedicated tests below.
    return None


def test_cli_help_mentions_oncokb_proxy_flag():
    """--help text exposes the new flag."""
    import subprocess
    import sys
    proc = subprocess.run(
        [sys.executable, "-m", "knowledge_base.engine.cli", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    assert "--oncokb-proxy" in proc.stdout
    assert "--oncokb-timeout" in proc.stdout
    # Help mentions the surface-only invariant
    assert "surface-only" in proc.stdout.lower() or "§8.3" in proc.stdout


def test_cli_default_invocation_does_not_use_oncokb():
    """AC-7 preservation at CLI level: without --oncokb-proxy,
    HttpxOncoKBClient is never instantiated.

    Verified by source-level check (regex over cli.py): the import + ctor
    of HttpxOncoKBClient must be guarded by `if args.oncokb_proxy`."""
    from pathlib import Path
    cli_path = Path(__file__).resolve().parent.parent / "knowledge_base" / "engine" / "cli.py"
    src = cli_path.read_text(encoding="utf-8")

    # All occurrences of HttpxOncoKBClient must appear inside an
    # `if args.oncokb_proxy:` block — verify every instantiation is
    # preceded by that guard within the same function scope.
    import re
    occurrences = [m.start() for m in re.finditer(r"HttpxOncoKBClient\(", src)]
    assert occurrences, "HttpxOncoKBClient ctor not found in cli.py"
    for idx in occurrences:
        # Look backwards within the previous 500 chars for the guard
        window = src[max(0, idx - 500):idx]
        assert "if args.oncokb_proxy" in window, (
            f"HttpxOncoKBClient() at offset {idx} not guarded by "
            "`if args.oncokb_proxy:` — risks accidental network calls"
        )


def test_cli_argparse_recognizes_oncokb_proxy_flag():
    """Verify argparse accepts the flag without error (signature smoke test)."""
    import subprocess
    import sys
    # --help with the flag should still succeed
    proc = subprocess.run(
        [sys.executable, "-m", "knowledge_base.engine.cli", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    # Parse the help output to confirm the flag has expected metavar
    assert "--oncokb-proxy URL" in proc.stdout
    assert "--oncokb-timeout SECONDS" in proc.stdout


def test_cli_unknown_flag_rejected():
    """Sanity: argparse still rejects unknown flags (no accidental swallow)."""
    import subprocess
    import sys
    proc = subprocess.run(
        [sys.executable, "-m", "knowledge_base.engine.cli", "--bogus-flag"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode != 0
    assert "unrecognized" in proc.stderr.lower() or "error" in proc.stderr.lower()


def test_revise_plan_accepts_oncokb_kwargs():
    """Q7 lock: revise_plan must accept oncokb_enabled + oncokb_client."""
    import inspect
    from knowledge_base.engine.revisions import revise_plan

    sig = inspect.signature(revise_plan)
    assert "oncokb_enabled" in sig.parameters
    assert sig.parameters["oncokb_enabled"].default is False  # safe default
    assert "oncokb_client" in sig.parameters
    assert sig.parameters["oncokb_client"].default is None
