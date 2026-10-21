"""Free, metadata-only comparison of Dataplex and openFDA drug-event access.

Run from the repository root with Python 3.12. No keys, signup, warehouse,
patient inputs, clinical scoring, or changes to the knowledge base are used.
Response bodies exist only in memory; output contains technical summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DRUGS = (
    "pembrolizumab", "nivolumab", "rituximab", "trastuzumab",
    "osimertinib", "imatinib", "cisplatin", "paclitaxel",
)
DATAPLEX = "https://api.dataplex-consulting.com"
MCP = "https://mcp.dataplex-consulting.com/mcp"
FDA = "https://api.fda.gov/drug/event.json"
WINDOW = ("20200101", "20260630")
MAX_BYTES = 25 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def schema_paths(value: Any, prefix: str = "") -> set[str]:
    """Return field names, never field values or array positions."""
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            paths.add(path)
            paths.update(schema_paths(child, path))
    elif isinstance(value, list):
        for child in value:
            paths.update(schema_paths(child, prefix + "[]"))
    return paths


def request_json(url: str, payload: dict | None = None) -> tuple[Any, dict]:
    """Record failures separately from no matches; never persist raw bodies."""
    allowed = {"api.fda.gov", "api.dataplex-consulting.com", "mcp.dataplex-consulting.com"}
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in allowed:
        raise ValueError("Only the three public pilot hosts are allowed")
    started = time.perf_counter()
    observation: dict[str, Any] = {"url": url, "retrieved_at_utc": utc_now()}
    headers = {
        "User-Agent": "OpenOnco-source-pilot/1.0 (https://github.com/romeo111/OpenOnco)",
        "Accept": "application/json, text/event-stream",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers.update({"Content-Type": "application/json", "MCP-Protocol-Version": "2025-03-26"})
        # Audit only tool/method names and our non-patient arguments.
        observation["rpc"] = payload
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            body = response.read(MAX_BYTES + 1)
            observation.update({"http_status": response.status, "response_bytes": len(body)})
            if len(body) > MAX_BYTES:
                raise ValueError("Response exceeds pilot memory limit")
            observation["sha256"] = hashlib.sha256(body).hexdigest()
            content_type = response.headers.get("Content-Type", "")
            if "text/event-stream" in content_type:
                messages = [json.loads(line[5:].strip()) for line in body.decode().splitlines()
                            if line.startswith("data:") and line[5:].strip()]
                result = next(item for item in messages if item.get("id") == payload["id"])
            else:
                result = json.loads(body)
            if payload is not None and not valid_rpc_result(result, payload):
                observation["status"] = "invalid_rpc_result"
                if isinstance(result, dict) and isinstance(result.get("error"), dict):
                    observation["rpc_error_code"] = result["error"].get("code")
                return None, observation
            observation["status"] = "ok"
            return result, observation
    except urllib.error.HTTPError as exc:
        observation.update({"status": "http_error", "http_status": exc.code})
        # FDA documents this specific JSON error for valid zero-result queries.
        if parsed.hostname == "api.fda.gov" and exc.code == 404:
            try:
                error = json.loads(exc.read(8192)).get("error", {})
                if error.get("code") == "NOT_FOUND" and error.get("message") == "No matches found!":
                    observation["status"] = "no_matches"
                    return {"meta": {"results": {"total": 0}}, "results": []}, observation
            except (ValueError, AttributeError):
                pass
        return None, observation
    except (OSError, ValueError, StopIteration) as exc:
        observation.update({"status": "transport_or_parse_error", "error_type": type(exc).__name__})
        return None, observation
    finally:
        observation["elapsed_ms"] = round((time.perf_counter() - started) * 1000)


def valid_rpc_result(result: Any, request: dict) -> bool:
    if not isinstance(result, dict) or "error" in result or result.get("id") != request["id"]:
        return False
    value = result.get("result")
    if not isinstance(value, dict):
        return False
    if request["method"] == "initialize":
        return isinstance(value.get("serverInfo"), dict) and isinstance(value.get("protocolVersion"), str)
    if request["method"] == "tools/list":
        return isinstance(value.get("tools"), list) and all(
            isinstance(tool, dict) and isinstance(tool.get("name"), str) for tool in value["tools"]
        )
    return not value.get("isError")


def decode_tool(result: dict | None) -> Any:
    if result is None or "error" in result:
        return None
    value = result.get("result", {})
    if value.get("isError"):
        return None
    if "structuredContent" in value:
        return value["structuredContent"]
    texts = [item["text"] for item in value.get("content", []) if item.get("type") == "text"]
    try:
        return json.loads("\n".join(texts))
    except ValueError:
        return None


def brand_aliases(drug: dict) -> list[str]:
    # KB brand labels include explanatory '(biosimilar)' / '(with ...)' text.
    # Keep original labels in provenance; strip annotations only for retrieval.
    return list(dict.fromkeys(re.sub(r"\s*\([^)]*\)", "", name).strip()
                              for name in drug["brand_names"]))


def load_drugs() -> list[dict]:
    drugs = []
    for slug in DRUGS:
        path = ROOT / "knowledge_base/hosted/content/drugs" / f"{slug}.yaml"
        body = path.read_bytes()
        record = yaml.safe_load(body)
        names = record["names"]
        drugs.append({
            "id": record["id"], "slug": slug,
            "generic_name": names.get("english", names["preferred"]),
            "brand_names": names.get("brand_names", []),
            "rxnorm_id": record.get("rxnorm_id"),
            "kb_path": path.relative_to(ROOT).as_posix(),
            "kb_sha256": hashlib.sha256(body).hexdigest(),
        })
    return drugs


def quoted(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def search_expression(drug: dict, expanded: bool) -> str:
    name = drug["generic_name"]
    clauses = [f"patient.drug.openfda.generic_name:{quoted(name)}"]
    if expanded:
        clauses.append(f"patient.drug.activesubstance.activesubstancename:{quoted(name)}")
        for alias in [name, *brand_aliases(drug)]:
            clauses.append(f"patient.drug.medicinalproduct:{quoted(alias)}")
        for alias in brand_aliases(drug):
            clauses.append(f"patient.drug.openfda.brand_name:{quoted(alias)}")
    return "(" + " OR ".join(clauses) + f") AND receivedate:[{WINDOW[0]} TO {WINDOW[1]}]"


def name_matches(value: str, aliases: list[str]) -> bool:
    # Boundary-aware phrase matching includes salts, formulation text and
    # biosimilar suffixes. This is retrieval matching, not ingredient identity.
    normalize = lambda text: " ".join(re.findall(r"[a-z0-9]+", str(text).lower()))
    text = " " + normalize(value) + " "
    return any(" " + normalize(alias) + " " in text for alias in aliases if normalize(alias))


def summarize_fda(payload: dict | None, drug: dict) -> dict:
    if payload is None:
        return {"total_reports_in_window": None, "sample_reports": None}
    records = payload.get("results", [])
    aliases = [drug["generic_name"], *brand_aliases(drug)]
    roles: Counter = Counter()
    coverage: Counter = Counter()
    matched_drugs = 0
    received_dates = []
    for report in records:
        patient = report.get("patient", {})
        drugs = patient.get("drug", [])
        reactions = patient.get("reaction", [])
        coverage["reports_with_reaction_field"] += bool(reactions)
        coverage["reports_with_multiple_drugs"] += len(drugs) > 1
        received = report.get("receivedate")
        if received:
            received_dates.append(str(received))
        found = False
        for item in drugs:
            harmonized = item.get("openfda", {})
            generic_names = harmonized.get("generic_name", [])
            brand_names = harmonized.get("brand_name", [])
            substance = item.get("activesubstance", {}).get("activesubstancename", "")
            names = [item.get("medicinalproduct", ""), substance, *generic_names, *brand_names]
            if not any(name_matches(name, aliases) for name in names):
                continue
            found = True
            matched_drugs += 1
            roles[str(item.get("drugcharacterization", "missing"))] += 1
            coverage["matched_drugs_with_harmonized_generic_name"] += bool(generic_names)
            coverage["matched_drugs_with_rxcui"] += bool(harmonized.get("rxcui"))
            coverage["matched_drugs_with_substance_name"] += bool(substance)
        coverage["reports_with_local_name_match"] += found
    return {
        "total_reports_in_window": payload.get("meta", {}).get("results", {}).get("total"),
        "dataset_last_updated": payload.get("meta", {}).get("last_updated"),
        "sample_reports": len(records), "matched_drug_entries_in_sample": matched_drugs,
        "matched_drug_roles_in_sample": dict(roles), "field_coverage_in_sample": dict(coverage),
        "sample_receivedate_min": min(received_dates, default=None),
        "sample_receivedate_max": max(received_dates, default=None),
        "schema_paths": sorted(schema_paths(records)),
    }


def summarize_dataplex_sample(payload: dict | None) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("rows"), list) or not all(
        isinstance(row, dict) for row in payload["rows"]
    ) or not isinstance(payload.get("product"), str) or not isinstance(payload.get("table"), str):
        return {"available": False, "drug_coverage": "not_assessable", "observed_rows": None}
    rows = payload["rows"]
    fields = sorted({key for row in rows for key in row})
    name_fields = [key for key in fields if key.upper() in {
        "SUBSTANCE_NAME", "MEDICINAL_PRODUCT", "MEDICINALPRODUCT", "GENERIC_NAME", "BRAND_NAME",
    }]
    dates = [str(row["RECEIVE_DATE"]) for row in rows if row.get("RECEIVE_DATE")]
    return {
        "available": True, "product": payload.get("product"), "table": payload.get("table"),
        "generated_at": payload.get("generated_at"), "declared_row_count": payload.get("row_count"),
        "observed_rows": len(rows), "fields": fields, "drug_name_fields": name_fields,
        "rows_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest(),
        "drug_coverage": "requires_sample_matching" if name_fields else "not_assessable",
        "sample_receive_date_min": min(dates, default=None),
        "sample_receive_date_max": max(dates, default=None),
        "field_nonnull_counts": {key: sum(row.get(key) is not None for row in rows) for key in fields},
        "field_types": {key: sorted({type(row[key]).__name__ for row in rows if key in row})
                        for key in fields},
    }


def collect(sample_size: int) -> dict:
    drugs = load_drugs()
    report: dict[str, Any] = {
        "schema_version": 1, "started_at_utc": utc_now(),
        "kb_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope": "Technical access and metadata pilot; no clinical conclusions",
        "window_receivedate_inclusive": list(WINDOW), "sample_size_per_drug": sample_size,
        "sampling": "openFDA: most recent receivedate in fixed window; Dataplex: supplier-selected headers",
        "no_raw_reports_saved": True, "no_credentials_or_subscriptions_used": True,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "matching_scope": "Broad retrieval includes formulations, biosimilars and combinations; not ingredient-adjudicated",
        "requests": [], "drugs": drugs,
    }
    observations = report["requests"]

    def get(label: str, url: str, rpc: dict | None = None) -> Any:
        value, observation = request_json(url, rpc)
        observation["label"] = label
        observations.append(observation)
        print(f"{label}: {observation['status']}", flush=True)
        time.sleep(0.3)  # comfortably below unauthenticated FDA rate limits
        return value

    catalog = get("dataplex_catalog", DATAPLEX + "/v1/catalog.json")
    products = (catalog or {}).get("products", [])
    product = next((item for item in products if item.get("slug") == "fda_aems"), {})
    report["dataplex"] = {
        "catalog_generated_at": (catalog or {}).get("generated_at"),
        "product": {key: product.get(key) for key in (
            "slug", "display_name", "tables", "refresh_frequency", "monthly_price_usd", "docs_url",
        )},
    }
    sample = get("dataplex_static_sample", DATAPLEX + "/v1/products/fda_aems/sample.json")
    report["dataplex"]["static_sample"] = summarize_dataplex_sample(sample)
    observations[-1]["tool_result_usable"] = report["dataplex"]["static_sample"]["available"]
    initialize = get("dataplex_mcp_initialize", MCP, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "OpenOnco-free-source-pilot", "version": "1.0"},
        },
    })
    report["dataplex"]["mcp_server"] = (initialize or {}).get("result", {}).get("serverInfo")
    tools_response = get("dataplex_mcp_tools", MCP, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tool_list = (tools_response or {}).get("result", {}).get("tools", [])
    report["dataplex"]["mcp_tools"] = [{"name": item["name"], "inputSchema": item.get("inputSchema")} for item in tool_list]
    for request_id, (name, args) in enumerate([
        ("get_data_dictionary", {"slug": "fda_aems"}),
        ("get_sample_data", {"slug": "fda_aems", "max_rows": 100}),
    ], start=3):
        result = get("dataplex_mcp_" + name, MCP, {
            "jsonrpc": "2.0", "id": request_id, "method": "tools/call",
            "params": {"name": name, "arguments": args},
        })
        decoded = decode_tool(result)
        observations[-1]["tool_result_usable"] = decoded is not None
        if name == "get_sample_data":
            report["dataplex"]["mcp_sample"] = summarize_dataplex_sample(decoded)
            observations[-1]["tool_result_usable"] = report["dataplex"]["mcp_sample"]["available"]
        else:
            report["dataplex"]["dictionary_response_schema"] = sorted(schema_paths(decoded))
            report["dataplex"]["dictionary_top_level_fields"] = sorted(decoded) if isinstance(decoded, dict) else None

    for drug in drugs:
        for mode in ("generic", "expanded"):
            query = search_expression(drug, expanded=mode == "expanded")
            params = {"search": query, "limit": 1 if mode == "generic" else sample_size,
                      "sort": "receivedate:desc"}
            url = FDA + "?" + urllib.parse.urlencode(params)
            result = get(f"openfda_{drug['slug']}_{mode}", url)
            drug["openfda_" + mode] = summarize_fda(result, drug)
        drug["dataplex_drug_coverage"] = "not_assessable_from_unfiltered_header_sample"
    report["finished_at_utc"] = utc_now()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sample-size", type=int, choices=range(1, 26), default=10)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; choose a new path to preserve the observation")
    report = collect(args.sample_size)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = [item for item in report["requests"] if item["status"] not in {"ok", "no_matches"}
                or item.get("tool_result_usable") is False]
    print(f"Saved {args.output}; {len(failures)} failed requests", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
