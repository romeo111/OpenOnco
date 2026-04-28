"""Encode/decode patient profile tokens for URL-hash transport (browser-only state).

Used by the QR-code / case-token flow (CSD-3): a patient profile dict is
gzipped + base64-url-safe-encoded into a compact token, embedded in the URL
hash, and decoded entirely in the browser by /try.html. No PHI ever leaves
the device — CHARTER §9.3.

The encoding is round-trip safe: ``decode(encode(d)) == d`` for any
JSON-serialisable dict. ``sort_keys=True`` makes the output deterministic so
two equal profiles produce the same token (useful for testing + for
cache-stable QR PNGs).
"""

from __future__ import annotations

import base64
import gzip
import json
from typing import Optional


def encode(patient_dict: dict) -> str:
    """Patient dict → URL-safe base64-gzip-json token. Round-trip safe."""
    json_bytes = json.dumps(
        patient_dict, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    gzipped = gzip.compress(json_bytes, compresslevel=9)
    return base64.urlsafe_b64encode(gzipped).decode("ascii").rstrip("=")


def decode(token: str) -> Optional[dict]:
    """Token → patient dict. Returns None on any decode failure.

    The browser-side decoder in /try.html mirrors this logic using the
    DecompressionStream + atob web APIs.
    """
    if not token:
        return None
    try:
        # Re-add base64 padding stripped by encode().
        padded = token + "=" * (-len(token) % 4)
        gzipped = base64.urlsafe_b64decode(padded.encode("ascii"))
        json_bytes = gzip.decompress(gzipped)
        return json.loads(json_bytes.decode("utf-8"))
    except Exception:
        return None
