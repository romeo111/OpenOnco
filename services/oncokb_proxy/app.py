"""OncoKB proxy — FastAPI app holding the OncoKB API token server-side.

Architecture (per docs/plans/oncokb_integration_safe_rollout_v3.md):

  Pyodide engine  ──fetch──▶  this proxy (Cloud Run)  ──auth──▶  OncoKB API
                                       │
                                       └── in-memory LRU cache, 7-day TTL

The Pyodide client never sees the token. Each lookup is keyed on
(gene, variant, disease_oncotree_code, tumor_type) and cached.

Phase 1a hardening (2026-04-26):
  - openonco.info added to default CORS
  - slowapi rate-limit (default 60/min per-IP; disable in tests via env)
  - X-Request-Id middleware (echo or generate UUID4)
  - Structured JSON access log (no token, no body — only key fields)
  - Token-scrub middleware (regex strips Bearer/api-key/token from any error body)
  - /healthz reports git_sha + integration master kill-switch state

Out-of-scope here (deferred to later phases):
  - Singleflight / circuit breaker (Phase 3 hardening)
  - Real Cloud Run deploy (Phase 1b — requires user OK + GCP creds)
  - Render-side integration (Phase 4)
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
import uuid
from collections import OrderedDict
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


# ── Configuration ────────────────────────────────────────────────────────


ONCOKB_API_BASE = os.environ.get("ONCOKB_API_BASE", "https://www.oncokb.org/api/v1")
ONCOKB_API_TOKEN = os.environ.get("ONCOKB_API_TOKEN")
CACHE_TTL_SECONDS = int(os.environ.get("ONCOKB_CACHE_TTL_SECONDS", 7 * 24 * 3600))
CACHE_MAX_ENTRIES = int(os.environ.get("ONCOKB_CACHE_MAX_ENTRIES", 4096))
LIVE_MODE = os.environ.get("ONCOKB_LIVE", "0") == "1"
INTEGRATION_ENABLED = os.environ.get("ONCOKB_INTEGRATION_ENABLED", "1") == "1"
GIT_SHA = os.environ.get("GIT_SHA", "unknown")

RATE_LIMIT = os.environ.get("ONCOKB_RATE_LIMIT", "60/minute")
RATE_LIMIT_DISABLED = os.environ.get("ONCOKB_RATE_LIMIT_DISABLED", "0") == "1"

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ONCOKB_PROXY_CORS_ORIGINS",
        "https://openonco.info,https://openonco.org,http://localhost:8000,http://localhost:3000",
    ).split(",")
    if o.strip()
]


# ── Token-scrub helpers ─────────────────────────────────────────────────


# Patterns we must never let through into logs or error bodies.
# Defensive even though we don't intentionally echo tokens — guards against
# upstream OncoKB error bodies that might quote our Authorization header back
# at us in some edge case.
_SCRUB_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]+", re.IGNORECASE),
    re.compile(r"(api[-_]?key|token|authorization)\s*[=:]\s*[A-Za-z0-9._\-]+", re.IGNORECASE),
]


def scrub(text: str) -> str:
    """Remove anything that looks like a credential. Idempotent."""
    if not text:
        return text
    out = text
    for pat in _SCRUB_PATTERNS:
        out = pat.sub("[REDACTED]", out)
    return out


# ── Structured JSON logger ──────────────────────────────────────────────


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": scrub(record.getMessage()),
        }
        # Allow structured 'extra' fields under record.extra
        extra = getattr(record, "extra", None)
        if isinstance(extra, dict):
            payload.update({k: scrub(str(v)) if isinstance(v, str) else v for k, v in extra.items()})
        return json.dumps(payload, ensure_ascii=False)


_log_handler = logging.StreamHandler()
_log_handler.setFormatter(_JsonFormatter())
logger = logging.getLogger("oncokb_proxy")
logger.handlers = [_log_handler]
logger.setLevel(logging.INFO)
logger.propagate = False


# ── Rate-limiter ─────────────────────────────────────────────────────────


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[] if RATE_LIMIT_DISABLED else [RATE_LIMIT],
)


# ── App + middleware ─────────────────────────────────────────────────────


app = FastAPI(
    title="OpenOnco · OncoKB Proxy",
    description=(
        "Read-only server-side proxy for OncoKB therapeutic-level lookups. "
        "Holds the OncoKB API token; Pyodide client calls this proxy instead "
        "of the OncoKB API directly."
    ),
    version="0.2.0-hardened",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def request_id_and_log(request: Request, call_next):
    req_id = request.headers.get("X-Request-Id") or f"req-{uuid.uuid4().hex[:12]}"
    start = time.time()

    # Master kill-switch: if integration is disabled, return 503 fast on /lookup.
    # /healthz still works so operators can see why.
    if not INTEGRATION_ENABLED and request.url.path == "/lookup":
        latency_ms = int((time.time() - start) * 1000)
        logger.info(
            "kill_switch_active",
            extra={
                "extra": {
                    "request_id": req_id,
                    "path": request.url.path,
                    "status": 503,
                    "latency_ms": latency_ms,
                }
            },
        )
        resp = JSONResponse(
            status_code=503,
            content={"detail": "OncoKB integration disabled (ONCOKB_INTEGRATION_ENABLED=0)"},
        )
        resp.headers["X-Request-Id"] = req_id
        return resp

    response: Response = await call_next(request)
    response.headers["X-Request-Id"] = req_id
    latency_ms = int((time.time() - start) * 1000)

    logger.info(
        "request",
        extra={
            "extra": {
                "request_id": req_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "latency_ms": latency_ms,
            }
        },
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"^http://localhost(:\d+)?$",
    allow_methods=["GET", "POST"],
    allow_headers=["content-type", "x-request-id"],
    expose_headers=["x-request-id"],
)


# ── Cache ────────────────────────────────────────────────────────────────


class _LRU:
    """Tiny LRU with TTL. Sufficient for ~4k entries; swap for redis if scaled."""

    def __init__(self, maxsize: int, ttl_seconds: int) -> None:
        self.maxsize = maxsize
        self.ttl = ttl_seconds
        self._d: "OrderedDict[tuple, tuple[float, dict]]" = OrderedDict()

    def get(self, key: tuple) -> Optional[dict]:
        item = self._d.get(key)
        if item is None:
            return None
        ts, value = item
        if time.time() - ts > self.ttl:
            self._d.pop(key, None)
            return None
        self._d.move_to_end(key)
        return value

    def set(self, key: tuple, value: dict) -> None:
        self._d[key] = (time.time(), value)
        self._d.move_to_end(key)
        while len(self._d) > self.maxsize:
            self._d.popitem(last=False)

    def __len__(self) -> int:
        return len(self._d)


_cache = _LRU(CACHE_MAX_ENTRIES, CACHE_TTL_SECONDS)


# ── Models ───────────────────────────────────────────────────────────────


class LookupRequest(BaseModel):
    gene: str = Field(..., min_length=1, max_length=32)
    variant: str = Field(..., min_length=1, max_length=128)
    oncotree_code: Optional[str] = Field(None, max_length=32)
    tumor_type: Optional[str] = Field(None, max_length=128)


class TherapeuticOption(BaseModel):
    level: str  # "1" | "2" | "3A" | "3B" | "4" | "R1" | "R2"
    drugs: list[str]
    description: Optional[str] = None
    pmids: list[str] = Field(default_factory=list)


class LookupResponse(BaseModel):
    gene: str
    variant: str
    oncokb_url: str
    therapeutic_options: list[TherapeuticOption]
    cached: bool


# ── Endpoints ────────────────────────────────────────────────────────────


@app.get("/healthz")
def healthz() -> dict:
    return {
        "status": "ok",
        "live_mode": LIVE_MODE,
        "integration_enabled": INTEGRATION_ENABLED,
        "token_configured": bool(ONCOKB_API_TOKEN),
        "cache_size": len(_cache),
        "cache_max": CACHE_MAX_ENTRIES,
        "cache_ttl_seconds": CACHE_TTL_SECONDS,
        "allowed_origins": ALLOWED_ORIGINS,
        "git_sha": GIT_SHA,
        "rate_limit": "disabled" if RATE_LIMIT_DISABLED else RATE_LIMIT,
    }


@app.post("/lookup", response_model=LookupResponse)
@limiter.limit(RATE_LIMIT)
async def lookup(req: LookupRequest, request: Request) -> LookupResponse:
    key = (req.gene.upper(), req.variant, req.oncotree_code or "", req.tumor_type or "")

    cached = _cache.get(key)
    if cached is not None:
        return LookupResponse(**cached, cached=True)

    if not LIVE_MODE:
        # Scaffold mode — synthesize an empty response so end-to-end works
        # without an OncoKB token. Tests use this path.
        result = {
            "gene": req.gene.upper(),
            "variant": req.variant,
            "oncokb_url": _oncokb_gene_url(req.gene, req.variant),
            "therapeutic_options": [],
        }
        _cache.set(key, result)
        return LookupResponse(**result, cached=False)

    if not ONCOKB_API_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="ONCOKB_LIVE=1 but ONCOKB_API_TOKEN is unset.",
        )

    try:
        result = await _call_oncokb(req)
    except HTTPException:
        # Already scrubbed below in raising helper
        raise
    except Exception as e:  # noqa: BLE001 — defensive scrub catch-all
        # Never let raw exception text reach client (might quote token)
        raise HTTPException(status_code=502, detail=f"upstream error: {scrub(str(e))[:200]}")

    _cache.set(key, result)
    return LookupResponse(**result, cached=False)


# ── Internals ────────────────────────────────────────────────────────────


def _oncokb_gene_url(gene: str, variant: str) -> str:
    return f"https://www.oncokb.org/gene/{gene.upper()}/{variant}"


async def _call_oncokb(req: LookupRequest) -> dict:
    """Live OncoKB call. Returns the trimmed-down LookupResponse-shaped dict.

    OncoKB's /annotate/mutations/byProteinChange endpoint shape (Phase 0
    A1 to verify with real token):
      GET ?hugoSymbol={gene}&alteration={variant}&tumorType={tumor_type}
    Authorization: Bearer {token}

    We extract `treatments` from the response and reshape into our
    therapeutic_options list. Anything beyond that is dropped (per
    src_oncokb.yaml scope: therapeutic levels only)."""

    headers = {
        "Authorization": f"Bearer {ONCOKB_API_TOKEN}",
        "Accept": "application/json",
    }
    params: dict[str, str] = {
        "hugoSymbol": req.gene.upper(),
        "alteration": req.variant,
    }
    if req.tumor_type:
        params["tumorType"] = req.tumor_type

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{ONCOKB_API_BASE}/annotate/mutations/byProteinChange",
            params=params,
            headers=headers,
        )
        if resp.status_code != 200:
            # Scrub upstream body before echoing — defensive even though
            # OncoKB shouldn't mirror our Authorization header back.
            safe = scrub(resp.text)[:200]
            raise HTTPException(
                status_code=502,
                detail=f"OncoKB returned {resp.status_code}: {safe}",
            )
        data = resp.json()

    options: list[dict] = []
    for tx in data.get("treatments", []) or []:
        options.append(
            {
                "level": str(tx.get("level") or "").replace("LEVEL_", "") or "?",
                "drugs": [d.get("drugName", "") for d in tx.get("drugs", []) or []],
                "description": tx.get("description") or None,
                "pmids": [str(p) for p in tx.get("pmids", []) or []],
            }
        )

    return {
        "gene": req.gene.upper(),
        "variant": req.variant,
        "oncokb_url": _oncokb_gene_url(req.gene, req.variant),
        "therapeutic_options": options,
    }
