"""Technical pilot regressions: unknown coverage and no patient-row retention."""

import io
import json
import urllib.error

from scripts import pilot_dataplex_openfda as pilot

DRUG = {"generic_name": "Pembrolizumab", "brand_names": ["Keytruda"]}


def test_dataplex_headers_do_not_imply_zero_drug_coverage():
    result = pilot.summarize_dataplex_sample({
        "product": "fda_aems", "table": "DRUG_REPORTS", "row_count": 1,
        "rows": [{"DRUG_COUNT": 2, "PATIENT_SUMMARY_NARRATIVE": "PRIVATE SENTINEL",
                  "SAFETY_REPORT_ID": "REPORT SENTINEL", "RECEIVE_DATE": "2026-06-01"}],
    })
    assert result["drug_coverage"] == "not_assessable"
    assert result["observed_rows"] == 1
    assert "PRIVATE SENTINEL" not in json.dumps(result)
    assert "REPORT SENTINEL" not in json.dumps(result)


def test_matched_drug_roles_do_not_come_from_other_drugs():
    payload = {"meta": {"results": {"total": 42}}, "results": [{
        "safetyreportid": "REPORT SENTINEL", "receivedate": "20260601",
        "patient": {"drug": [
            {"medicinalproduct": "KEYTRUDA 100 MG", "drugcharacterization": "2"},
            {"medicinalproduct": "OTHER DRUG", "drugcharacterization": "1",
             "openfda": {"generic_name": ["OTHER"], "rxcui": ["123"]}},
        ], "reaction": [{"reactionmeddrapt": "REACTION SENTINEL"}]},
    }]}
    result = pilot.summarize_fda(payload, DRUG)
    assert result["matched_drug_roles_in_sample"] == {"2": 1}
    assert result["field_coverage_in_sample"]["matched_drugs_with_rxcui"] == 0
    assert result["field_coverage_in_sample"]["reports_with_multiple_drugs"] == 1
    assert "REACTION SENTINEL" not in json.dumps(result)
    assert "REPORT SENTINEL" not in json.dumps(result)


def test_transport_failure_is_unknown_not_zero():
    assert pilot.summarize_fda(None, DRUG)["total_reports_in_window"] is None
    empty = {"meta": {"results": {"total": 0}}, "results": []}
    assert pilot.summarize_fda(empty, DRUG)["total_reports_in_window"] == 0


def test_only_explicit_fda_no_matches_is_zero(monkeypatch):
    def no_matches(*args, **kwargs):
        body = json.dumps({"error": {"code": "NOT_FOUND", "message": "No matches found!"}}).encode()
        raise urllib.error.HTTPError(pilot.FDA, 404, "Not Found", {}, io.BytesIO(body))
    monkeypatch.setattr(pilot.urllib.request, "urlopen", no_matches)
    result, observation = pilot.request_json(pilot.FDA)
    assert observation["status"] == "no_matches"
    assert result["meta"]["results"]["total"] == 0

    def bad_endpoint(*args, **kwargs):
        raise urllib.error.HTTPError(pilot.FDA, 404, "Not Found", {}, io.BytesIO(b"not found"))
    monkeypatch.setattr(pilot.urllib.request, "urlopen", bad_endpoint)
    result, observation = pilot.request_json(pilot.FDA)
    assert result is None
    assert observation["status"] == "http_error"


def test_queries_share_date_window_and_expanded_includes_raw_aliases():
    generic = pilot.search_expression(DRUG, False)
    expanded = pilot.search_expression(DRUG, True)
    assert "receivedate:[20200101 TO 20260630]" in generic
    assert "receivedate:[20200101 TO 20260630]" in expanded
    assert 'patient.drug.medicinalproduct:"Keytruda"' in expanded
    assert "activesubstancename" in expanded
    assert "drugcharacterization" not in expanded


def test_matcher_handles_formulations_without_substring_collisions():
    assert pilot.name_matches("PEMBROLIZUMAB 100 MG", ["pembrolizumab"])
    assert not pilot.name_matches("notpembrolizumab", ["pembrolizumab"])


def test_mcp_tool_error_does_not_become_empty_valid_sample():
    assert pilot.decode_tool({"result": {"isError": True, "content": []}}) is None
    assert pilot.decode_tool({"error": {"code": -32602}}) is None
    assert pilot.decode_tool({"result": {"content": [{"type": "text", "text": "Unavailable"}]}}) is None
    for value in (None, {}, {"rows": []}, {"product": "fda_aems", "table": "DRUG_REPORTS", "rows": [1]}):
        result = pilot.summarize_dataplex_sample(value)
        assert result["available"] is False
        assert result["observed_rows"] is None


def test_rpc_initialization_and_discovery_errors_are_not_success():
    for method in ("initialize", "tools/list"):
        request = {"method": method, "id": 1}
        assert not pilot.valid_rpc_result({"id": 1, "error": {"code": -32600}}, request)
        assert not pilot.valid_rpc_result({"id": 1, "result": {}}, request)
    assert pilot.valid_rpc_result({"id": 1, "result": {"tools": []}}, {"id": 1, "method": "tools/list"})


def test_brand_annotations_are_not_sent_as_part_of_drug_name():
    drug = {"generic_name": "Rituximab", "brand_names": ["Truxima (biosimilar)"]}
    query = pilot.search_expression(drug, True)
    assert 'medicinalproduct:"Truxima"' in query
    assert "biosimilar" not in query
    assert drug["brand_names"] == ["Truxima (biosimilar)"]


def test_selected_drugs_are_grounded_in_kb():
    drugs = pilot.load_drugs()
    assert len(drugs) == 8
    assert all(drug["id"].startswith("DRUG-") for drug in drugs)
    assert all(len(drug["kb_sha256"]) == 64 for drug in drugs)
