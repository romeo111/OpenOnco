"""openFDA REST API client.

Per specs/SOURCE_INGESTION_SPEC §16.3 — referenced-mode live API for
FDA drug labels, recalls, and adverse events.
Endpoint: https://api.fda.gov

Rate limit: 240 req/min without key, 120K/day with free API key.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from http.client import HTTPException
from typing import Any, Literal, Optional

from .base import BaseSourceClient, RateLimit

OPENFDA_BASE = "https://api.fda.gov"
USER_AGENT = "OpenOnco/0.1 (https://github.com/romeo111/cancer-autoresearch)"


def _http_get(path: str, params: dict[str, Any]) -> dict:
    api_key = os.environ.get("OPENFDA_API_KEY")
    if api_key:
        params = {**params, "api_key": api_key}
    qs = urllib.parse.urlencode(params)
    url = f"{OPENFDA_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def drug_label_search(query: str, limit: int = 10) -> dict:
    return _http_get("/drug/label.json", {"search": query, "limit": limit})


def drug_recalls(query: str, limit: int = 10) -> dict:
    return _http_get("/drug/enforcement.json", {"search": query, "limit": limit})


@dataclass
class OpenFDAQuery:
    """openFDA endpoint dispatch + free-text search expression."""

    endpoint: Literal["label", "recall"] = "label"
    search: str = ""
    limit: int = 10


def _name(value: str, *, brand: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError("Drug names must be strings")
    if brand:
        # KB display labels may include notes such as '(biosimilar)'.
        value = re.sub(r"\([^()]*\)", "", value)
    return " ".join(value.split())


def _literal(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


@dataclass(frozen=True)
class OpenFDAEventQuery:
    """Named-drug report retrieval, independent of treatment rules.

    Dates, when supplied, are inclusive ISO dates for FDA receipt (not onset).
    Names are quoted literals; callers cannot supply search expressions here.
    """

    active_substance: str = ""
    brand_names: tuple[str, ...] = ()
    limit: int = 10
    skip: int = 0
    received_from: str | None = None
    received_to: str | None = None

    def __post_init__(self) -> None:
        substance = _name(self.active_substance)
        if not isinstance(self.brand_names, (tuple, list)):
            raise ValueError("brand_names must be a tuple or list of names")
        object.__setattr__(self, "brand_names", tuple(self.brand_names))
        brands = [_name(name, brand=True) for name in self.brand_names]
        if any(not name for name in brands):
            raise ValueError("Brand names must not be empty after removing annotations")
        if not substance and not brands:
            raise ValueError("Provide an active substance or at least one brand")
        for field, value, lower, upper in (
            ("limit", self.limit, 1, 1000),
            ("skip", self.skip, 0, 25000),
        ):
            if type(value) is not int or not lower <= value <= upper:
                raise ValueError(f"{field} must be an integer between {lower} and {upper}")
        if (self.received_from is None) != (self.received_to is None):
            raise ValueError("Provide both received_from and received_to")
        if self.received_from is not None:
            for value in (self.received_from, self.received_to):
                if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError("Receipt dates must use YYYY-MM-DD")
                date.fromisoformat(value)
            if self.received_from > self.received_to:
                raise ValueError("received_from must not be after received_to")

    @property
    def search(self) -> str:
        clauses: list[str] = []
        seen: set[tuple[str, str]] = set()

        def add(field: str, name: str) -> None:
            key = (field, name.casefold())
            if key not in seen:
                clauses.append(f"patient.drug.{field}:{_literal(name)}")
                seen.add(key)

        substance = _name(self.active_substance)
        if substance:
            for field in (
                "openfda.generic_name",
                "activesubstance.activesubstancename",
                "medicinalproduct",
            ):
                add(field, substance)
        for brand in self.brand_names:
            name = _name(brand, brand=True)
            for field in ("medicinalproduct", "openfda.brand_name"):
                add(field, name)
        search = "(" + " OR ".join(clauses) + ")"
        if self.received_from is not None:
            start = self.received_from.replace("-", "")
            end = self.received_to.replace("-", "")
            search += f" AND receivedate:[{start} TO {end}]"
        return search

    @property
    def params(self) -> dict[str, Any]:
        return {
            "search": self.search,
            "limit": self.limit,
            "skip": self.skip,
            "sort": "receivedate:desc",
        }

    @property
    def request_url(self) -> str:
        """Reproducible query URL without credentials."""
        return f"{OPENFDA_BASE}/drug/event.json?{urllib.parse.urlencode(self.params)}"


class OpenFDAError(RuntimeError):
    """Event request failure with no credentials or upstream body in the message."""

    def __init__(self, message: str, http_status: int | None = None):
        super().__init__(message)
        self.http_status = http_status


def drug_adverse_events(query: OpenFDAEventQuery) -> dict:
    """Return raw FDA reports/metadata; only an explicit no-match is empty.

    A report can mention several drugs and reactions without linking them.
    These records do not establish causality, incidence or treatment decisions.
    """
    try:
        payload = _http_get("/drug/event.json", query.params)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            try:
                body = json.loads(exc.read(65536).decode("utf-8"))
            except (ValueError, OSError, HTTPException):
                body = None
            if isinstance(body, dict) and body.get("error") == {
                "code": "NOT_FOUND",
                "message": "No matches found!",
            }:
                page = {"skip": query.skip, "limit": query.limit}
                # The same 404 also means an offset past the last matching report.
                if query.skip == 0:
                    page["total"] = 0
                return {"meta": {"results": page}, "results": []}
        raise OpenFDAError(f"openFDA event request failed (HTTP {exc.code})", exc.code) from None
    except (OSError, HTTPException):
        raise OpenFDAError("openFDA event request failed (transport error)") from None
    except (ValueError, UnicodeError):
        raise OpenFDAError("openFDA event response was not valid JSON") from None

    meta = payload.get("meta") if isinstance(payload, dict) else None
    pagination = meta.get("results") if isinstance(meta, dict) else None
    reports = payload.get("results") if isinstance(payload, dict) else None
    if (
        not isinstance(pagination, dict)
        or any(
            type(pagination.get(key)) is not int or pagination[key] < 0
            for key in ("skip", "limit", "total")
        )
        or not isinstance(reports, list)
        or any(not isinstance(report, dict) for report in reports)
        or len(reports) > query.limit
    ):
        raise OpenFDAError("openFDA event response has an invalid result envelope")
    return payload


class OpenFDAClient(BaseSourceClient[OpenFDAQuery | OpenFDAEventQuery, dict]):
    """SourceClient for openFDA."""

    source_id = "SRC-OPENFDA"
    rate_limit = RateLimit(tokens_per_second=4.0, burst=10)  # 240/min without key
    cache_ttl_seconds = 24 * 3600  # 1 day
    api_version = "openFDA"

    def _fetch_raw(self, query: OpenFDAQuery | OpenFDAEventQuery) -> tuple[dict, Optional[str]]:
        if isinstance(query, OpenFDAEventQuery):
            return drug_adverse_events(query), self.api_version
        if query.endpoint == "label":
            return drug_label_search(query.search, limit=query.limit), self.api_version
        if query.endpoint == "recall":
            return drug_recalls(query.search, limit=query.limit), self.api_version
        raise ValueError(f"Unknown openFDA endpoint: {query.endpoint!r}")

    def health(self) -> dict:
        try:
            drug_label_search("aspirin", limit=1)
            return {"ok": True, "latency_ms": None, "last_error": None}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "latency_ms": None, "last_error": str(e)}

    def quota(self) -> dict:
        if os.environ.get("OPENFDA_API_KEY"):
            return {"remaining": "up to 120000/day with key", "reset_at": None}
        return {"remaining": "240/min without key", "reset_at": None}
