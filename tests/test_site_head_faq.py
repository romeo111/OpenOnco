"""Tests for FAQPage structured data + JSON-LD validity in scripts/site_head.py.

FAQPage markup is a GEO lever (AI search / LLMs lift Q&A and cite declarative
answers). These tests lock: it appears on the homepage only (no duplicate-markup
penalty), every emitted JSON-LD block is valid JSON, and the answers keep the
not-a-medical-device safety framing.
"""

from __future__ import annotations

import json
import re

import pytest

from scripts.site_head import render_seo_metadata

_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def _blocks(path: str, locale: str) -> list[dict]:
    html = render_seo_metadata(path=path, title="OpenOnco", description="x", locale=locale)
    return [json.loads(m) for m in _LD.findall(html)]  # raises if any block is invalid JSON


@pytest.mark.parametrize("path,locale", [("index.html", "en"), ("ukr/index.html", "uk")])
def test_homepage_has_faqpage(path, locale):
    blocks = _blocks(path, locale)
    faqs = [b for b in blocks if b.get("@type") == "FAQPage"]
    assert len(faqs) == 1, "homepage should carry exactly one FAQPage block"
    questions = faqs[0]["mainEntity"]
    assert len(questions) >= 4
    for q in questions:
        assert q["@type"] == "Question" and q["name"]
        assert q["acceptedAnswer"]["@type"] == "Answer" and q["acceptedAnswer"]["text"]


@pytest.mark.parametrize("path", ["about.html", "capabilities.html", "kb/dis-aml.html"])
def test_non_homepage_has_no_faqpage(path):
    assert not [b for b in _blocks(path, "en") if b.get("@type") == "FAQPage"]


def test_faq_answers_keep_safety_framing():
    faq = [b for b in _blocks("index.html", "en") if b.get("@type") == "FAQPage"][0]
    text = " ".join(q["acceptedAnswer"]["text"] for q in faq["mainEntity"]).lower()
    assert "not a medical device" in text
    assert "verified by a qualified oncologist" in text
    assert "no large language model picks" in text  # the core safety differentiator
