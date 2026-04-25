"""Translation clients — DeepL Free primary + LibreTranslate self-hosted fallback.

CHARTER §8.3 allows LLM use only for: boilerplate code, doc drafts, extraction
from clinical documents (with human verification), and **translation with
clinical review**. Every translation produced here is automatically marked
`machine_translated: true` so a downstream renderer / reviewer can flag it
for clinical sign-off before publication.

Architecture:

    TranslateClient (Protocol)
        .translate(text, target_lang, source_lang=None) -> str

    DeepLClient                — primary; DeepL Free API (500K chars/month).
    LibreTranslateClient       — fallback; self-hosted at LIBRETRANSLATE_URL.
    FallbackTranslateClient    — wraps two: tries primary, on TranslateError
                                  falls back to secondary.
    CachedTranslateClient      — wraps any client; deterministic on-disk
                                  JSON cache keyed by (source, target, text).

    build_translate_client(...) — factory reading env vars:
        DEEPL_API_KEY, LIBRETRANSLATE_URL, LIBRETRANSLATE_API_KEY

Cache layout:

    knowledge_base/cache/translations/<sha256[:16]>.json

    {
      "source_text": "...",
      "translation":  "...",
      "source_lang":  "en",
      "target_lang":  "uk",
      "engine":       "deepl|libretranslate|fallback|cached",
      "translated_at": "2026-04-25T15:30:00+00:00",
      "machine_translated": true
    }

CLI:

    python -m knowledge_base.clients.translate_client \\
        --to uk --text "Hello world"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable

import httpx


logger = logging.getLogger(__name__)


_DEFAULT_CACHE_DIR = (
    Path(__file__).resolve().parent.parent / "cache" / "translations"
)


class TranslateError(RuntimeError):
    """Raised when a translation call fails (network, quota, auth, etc.)."""


# ── Protocol ─────────────────────────────────────────────────────────────


@runtime_checkable
class TranslateClient(Protocol):
    """Common interface. Implementations: DeepL, LibreTranslate, Fallback,
    Cached, plus user-supplied stubs in tests."""

    name: str

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str: ...


# ── DeepL ────────────────────────────────────────────────────────────────


class DeepLClient:
    """DeepL Free / Pro API client.

    Free tier: 500K chars/month, requires (free) API key signup at
    https://www.deepl.com/pro-api?cta=header-pro-api/. Free-tier endpoint
    is `api-free.deepl.com`; pro is `api.deepl.com`. The auth key suffix
    `:fx` indicates a Free key (toggle `free=True`).

    DeepL language codes are 2-letter uppercase: EN, UK, RU, DE, FR, etc.
    Some target codes have variants (EN-US/EN-GB, PT-BR/PT-PT) — pass full.
    """

    name = "deepl"
    BASE_URL_FREE = "https://api-free.deepl.com/v2/translate"
    BASE_URL_PRO = "https://api.deepl.com/v2/translate"

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        free: Optional[bool] = None,
        timeout: float = 10.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("DEEPL_API_KEY")
        if not self.api_key:
            raise TranslateError(
                "DeepL: DEEPL_API_KEY env var or api_key arg required"
            )
        # If `free` not specified, infer from key suffix (`:fx` = free)
        if free is None:
            free = self.api_key.endswith(":fx")
        self.url = self.BASE_URL_FREE if free else self.BASE_URL_PRO
        self.timeout = timeout

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str:
        if not text:
            return text
        headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
        data: dict = {"text": [text], "target_lang": target_lang.upper()}
        if source_lang:
            data["source_lang"] = source_lang.upper()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(self.url, headers=headers, json=data)
                resp.raise_for_status()
                payload = resp.json()
                return payload["translations"][0]["text"]
        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            if code == 456:
                raise TranslateError("DeepL quota exceeded (HTTP 456)") from e
            if code == 403:
                raise TranslateError("DeepL auth failed (HTTP 403) — check DEEPL_API_KEY") from e
            raise TranslateError(f"DeepL HTTP {code}") from e
        except (httpx.RequestError, KeyError, IndexError, ValueError) as e:
            raise TranslateError(f"DeepL: {e}") from e


# ── LibreTranslate (self-hosted) ─────────────────────────────────────────


class LibreTranslateClient:
    """LibreTranslate client — for self-hosted instance (default
    http://localhost:5000) or a public LT mirror.

    LT uses 2-letter lowercase codes: en, uk, ru, de, fr, etc. Source
    can be `auto` to auto-detect. Optional `api_key` for instances that
    require it; self-hosted defaults to no key.
    """

    name = "libretranslate"

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
    ) -> None:
        url = url or os.environ.get("LIBRETRANSLATE_URL", "http://localhost:5000")
        self.base_url = url.rstrip("/")
        self.api_key = api_key or os.environ.get("LIBRETRANSLATE_API_KEY")
        self.timeout = timeout

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str:
        if not text:
            return text
        body: dict = {
            "q": text,
            "target": target_lang.lower(),
            "source": (source_lang or "auto").lower(),
            "format": "text",
        }
        if self.api_key:
            body["api_key"] = self.api_key
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(f"{self.base_url}/translate", json=body)
                resp.raise_for_status()
                return resp.json()["translatedText"]
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, ValueError) as e:
            raise TranslateError(f"LibreTranslate: {e}") from e


# ── Fallback chain ───────────────────────────────────────────────────────


class FallbackTranslateClient:
    """Try `primary`; on TranslateError, fall back to `secondary`. Logs
    the failure with reason — important for telemetry (DeepL quota
    exhaustion is a recurring event)."""

    name = "fallback"

    def __init__(self, primary: TranslateClient, secondary: TranslateClient) -> None:
        self.primary = primary
        self.secondary = secondary

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str:
        try:
            return self.primary.translate(text, target_lang, source_lang)
        except TranslateError as exc:
            logger.warning(
                "Translate primary=%s failed (%s); falling back to %s",
                getattr(self.primary, "name", "?"),
                exc,
                getattr(self.secondary, "name", "?"),
            )
            return self.secondary.translate(text, target_lang, source_lang)


# ── On-disk cache wrapper ────────────────────────────────────────────────


class CachedTranslateClient:
    """Wrap any TranslateClient with deterministic on-disk JSON cache.

    Cache hits return immediately without network. Cache directory is
    gitignored (CHARTER §9.3 — never commit derived clinical content).
    Each entry carries `machine_translated: true` + engine name so a
    downstream renderer can visually flag MT content for clinician
    review per CHARTER §8.3.
    """

    name = "cached"

    def __init__(
        self,
        inner: TranslateClient,
        cache_dir: Path = _DEFAULT_CACHE_DIR,
    ) -> None:
        self.inner = inner
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, text: str, target_lang: str, source_lang: Optional[str]) -> Path:
        canonical = f"{(source_lang or 'auto').lower()}|{target_lang.lower()}|{text}"
        h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / f"{h}.json"

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str:
        if not text:
            return text
        path = self._key(text, target_lang, source_lang)
        if path.exists():
            try:
                cached = json.loads(path.read_text(encoding="utf-8"))
                return cached["translation"]
            except (OSError, ValueError, KeyError):
                # Cache corrupt — re-fetch
                pass

        translated = self.inner.translate(text, target_lang, source_lang)
        record = {
            "source_text": text,
            "translation": translated,
            "source_lang": (source_lang or "auto").lower(),
            "target_lang": target_lang.lower(),
            "engine": getattr(self.inner, "name", "unknown"),
            "translated_at": datetime.now(timezone.utc).isoformat(),
            "machine_translated": True,
        }
        path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return translated


# ── Factory ──────────────────────────────────────────────────────────────


def build_translate_client(
    *,
    use_cache: bool = True,
    cache_dir: Path = _DEFAULT_CACHE_DIR,
    deepl_key: Optional[str] = None,
    libre_url: Optional[str] = None,
    libre_key: Optional[str] = None,
) -> TranslateClient:
    """Construct the production stack: cached(fallback(deepl, libretranslate)).

    Falls back gracefully:

    - If DEEPL_API_KEY is missing → returns just LibreTranslate (cached)
      (so a self-hosted-only deployment still works).
    - If neither key/URL is provided → raises TranslateError; caller can
      handle (e.g., skip MT path entirely).

    Always wraps with cache by default — translations are deterministic
    so re-fetch is wasteful and counts against DeepL quota.
    """
    primary: Optional[TranslateClient] = None
    if deepl_key or os.environ.get("DEEPL_API_KEY"):
        try:
            primary = DeepLClient(api_key=deepl_key)
        except TranslateError:
            primary = None

    secondary: TranslateClient = LibreTranslateClient(url=libre_url, api_key=libre_key)

    if primary is None:
        chain: TranslateClient = secondary
    else:
        chain = FallbackTranslateClient(primary=primary, secondary=secondary)

    if use_cache:
        return CachedTranslateClient(chain, cache_dir=cache_dir)
    return chain


# ── CLI ──────────────────────────────────────────────────────────────────


def _cli(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="One-shot translation via DeepL Free + LibreTranslate fallback."
    )
    parser.add_argument("--text", required=True, help="Source text to translate.")
    parser.add_argument("--to", dest="target_lang", required=True,
                        help="Target language (e.g., uk, en, de).")
    parser.add_argument("--from", dest="source_lang", default=None,
                        help="Source language (default: auto-detect).")
    parser.add_argument("--no-cache", action="store_true",
                        help="Disable on-disk cache.")
    parser.add_argument("--engine", choices=["auto", "deepl", "libretranslate"],
                        default="auto",
                        help="Force a specific engine instead of fallback chain.")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        if args.engine == "deepl":
            client: TranslateClient = DeepLClient()
        elif args.engine == "libretranslate":
            client = LibreTranslateClient()
        else:
            client = build_translate_client(use_cache=not args.no_cache)

        if args.engine != "auto" and not args.no_cache:
            client = CachedTranslateClient(client)

        result = client.translate(
            args.text,
            target_lang=args.target_lang,
            source_lang=args.source_lang,
        )
        print(result)
        return 0
    except TranslateError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli())


__all__ = [
    "TranslateClient",
    "TranslateError",
    "DeepLClient",
    "LibreTranslateClient",
    "FallbackTranslateClient",
    "CachedTranslateClient",
    "build_translate_client",
]
