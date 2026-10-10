"""Integrity of synthetic review evidence; no clinical correctness claims."""
import json
from html.parser import HTMLParser
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan
from scripts.build_clinician_review import KB_ROOT, REPO_ROOT, _canonical, _decision, _sha, _text_sha, build_clinician_review
from scripts.review_dlbcl_scenarios import make_profile, scenarios
from scripts.site_head import inject_geo_lang_redirect, inject_seo_metadata, write_sitemap


@pytest.fixture(scope="module")
def packet(tmp_path_factory):
    output = tmp_path_factory.mktemp("review")
    return output, build_clinician_review(output_dir=output)


def test_packet_contracts_and_scope(packet):
    _, report = packet
    assert 20 <= report["summary"]["cases"] <= 30
    assert report["summary"]["contracts_passed"] == report["summary"]["contracts_total"]
    assert report["clinical_review_status"] == "pending"
    by_id = {case["id"]: case for case in report["cases"]}
    assert len(by_id) == len(scenarios())
    for name in ("unknown-disease", "unsupported-line", "ecog-4"):
        assert not by_id[name]["tracks"]
    assert any(i["code"] == "positive_requirement_conflict" for i in by_id["cd20-negative"]["input_findings"])
    assert any(i["code"] == "conflicting_input" for i in by_id["ipi-conflict"]["input_findings"])
    for case in report["cases"]:
        if case["remove"] and case["category"] == "missing data":
            assert any(i["code"] == "missing_input" for i in case["input_findings"])


def test_profiles_are_synthetic_and_evidence_matches_engine(packet):
    output, report = packet
    for case in report["cases"]:
        profile = json.loads((output / "cases" / f"{case['id']}.profile.json").read_text(encoding="utf-8"))
        assert profile["patient_id"].startswith("SYNTHETIC-REVIEW-")
        assert "clinical_record" not in profile
        assert _sha(_canonical(profile)) == case["profile_sha256"]
        actual = generate_plan(profile, kb_root=KB_ROOT)
        assert _sha(_canonical(_decision(actual))) == case["decision_sha256"]
        persisted = json.loads((output / "cases" / f"{case['id']}.result.json").read_text(encoding="utf-8"))
        assert persisted["synthetic_only"] is True
        assert persisted["result"]["trace"] == actual.to_dict()["trace"]
        assert persisted["result"]["default_indication_id"] == actual.default_indication_id


def test_provenance_hashes_current_files_and_never_grants_signoff(packet):
    output, report = packet
    assert report["entities"]
    assert any(entity["type"] == "sources" for entity in report["entities"])
    for entity in report["entities"]:
        assert _text_sha(KB_ROOT / entity["path"]) == entity["sha256"]
        assert entity["independently_verified_for_packet"] is False
    assert any(gap["code"] == "questionnaire_stub" for gap in report["questionnaire_findings"])
    template = json.loads((output / "review-template.json").read_text(encoding="utf-8"))
    assert template["clinical_signoff_granted"] is False
    assert all(case["assessment"] == "unreviewed" for case in template["cases"])


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.links.append(value)


def test_review_links_and_search_isolation(packet, tmp_path):
    output, _ = packet
    for page in output.rglob("*.html"):
        markup = page.read_text(encoding="utf-8")
        assert 'content="noindex,follow"' in markup
        parser = Links()
        parser.feed(markup)
        for link in parser.links:
            if not link.startswith(("/", "https:", "http:", "#", "data:", "mailto:")):
                assert (page.parent / link.split("#")[0].split("?")[0]).is_file(), (page, link)
    markup = (output / "index.html").read_text(encoding="utf-8")
    path = "review/dlbcl-1l/index.html"
    assert inject_seo_metadata(markup, path=path) == markup
    assert inject_geo_lang_redirect(markup, path=path) == markup
    root = tmp_path / "site"
    (root / "review").mkdir(parents=True)
    (root / "review/index.html").write_text(markup, encoding="utf-8")
    (root / "index.html").write_text("<html></html>", encoding="utf-8")
    assert "/review/" not in write_sitemap(root).read_text(encoding="utf-8")


def test_invalid_kb_cannot_publish_review_artifacts(tmp_path):
    kb = tmp_path / "kb"
    (kb / "biomarkers").mkdir(parents=True)
    (kb / "biomarkers/invalid.yaml").write_text("id: BIO-INVALID\nclinical_context: [not-a-valid-context]\n", encoding="utf-8")
    output = tmp_path / "output"
    with pytest.raises(RuntimeError, match="invalid knowledge base"):
        build_clinician_review(kb_root=kb, output_dir=output)
    assert not output.exists()


def test_mutated_scenario_does_not_retain_seed_narrative():
    case = next(case for case in scenarios() if case["id"] == "ipi-conflict")
    profile = make_profile(case, REPO_ROOT / "examples")
    assert profile["findings"]["ipi_score"] == 1
    assert profile["findings"]["high_ipi"] is True
    assert "clinical_record" not in profile


def test_provenance_is_stable_across_checkout_line_endings(tmp_path):
    lf, crlf = tmp_path / "lf.yaml", tmp_path / "crlf.yaml"
    lf.write_bytes(b"id: CASE-EXAMPLE\nvalue: 1\n")
    crlf.write_bytes(b"id: CASE-EXAMPLE\r\nvalue: 1\r\n")
    assert _text_sha(lf) == _text_sha(crlf)
