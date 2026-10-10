"""Prepare private EN-source Wiki translation drafts for clinical review.

Never writes to docs/ or the clinical knowledge base. Drafts under build/ are
gitignored and must not be published until qualified language/clinical review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Protocol

import yaml

from knowledge_base.clients.translate_client import build_full_stack

ROOT = Path(__file__).resolve().parent.parent
DRAFT_DIR = ROOT / "build" / "translation-drafts"
KINDS = ("diseases", "indications", "regimens")
LOCALES = ("es", "pt", "de", "fr")
PROTECTED = re.compile(r"\b(?:EGFR|HER2|BRAF|ALK|ROS1|KRAS|BCL2|MYC|CD\d+|DLBCL|NSCLC|SCLC|HCV)\b")


class Translator(Protocol):
    def translate(self, text: str, target_lang: str, source_lang: str | None = None) -> str: ...


def _source_paths(kb_root: Path, kind: str) -> dict[str, Path]:
    paths = {}
    for path in sorted((kb_root / kind).rglob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            paths[data["id"]] = path
    return paths


def prepare_drafts(
    index_path: Path,
    kb_root: Path,
    output_path: Path,
    *,
    locale: str,
    kind: str,
    client: Translator,
    limit: int,
) -> int:
    if locale not in LOCALES or kind not in KINDS or limit < 1:
        raise ValueError("Specify a supported locale, kind, and positive limit")
    entries = json.loads(index_path.read_text(encoding="utf-8"))["entries"]
    source_paths = _source_paths(kb_root, kind)
    existing = {}
    if output_path.exists():
        for line in output_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["id"]] = row
    written = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8", newline="\n") as out:
        for entry in entries:
            if entry.get("kind_key") != kind:
                continue
            entity_id = entry["id"]
            path = source_paths.get(entity_id)
            if path is None:
                raise ValueError(f"Missing YAML source for {entity_id}")
            title = entry["title"].strip()
            if not title:
                raise ValueError(f"Missing English title for {entity_id}")
            source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            previous = existing.get(entity_id)
            if previous and previous["source_sha256"] == source_hash and previous["en"] == title:
                continue
            translated = client.translate(title, locale, source_lang="en").strip()
            if not translated or translated == title:
                raise ValueError(f"Empty or unchanged translation for {entity_id}")
            tokens = set(PROTECTED.findall(title))
            missing_tokens = sorted(token for token in tokens if token not in translated)
            record = {
                "id": entity_id,
                "kind": kind,
                "en": title,
                locale: translated,
                "source_lang": "en",
                "target_lang": locale,
                "source_yaml": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix(),
                "source_sha256": source_hash,
                "machine_translated": True,
                "clinical_review": "required",
                "publication": "blocked",
                "review_flags": [f"protected term missing: {token}" for token in missing_tokens],
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
            if written >= limit:
                break
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True, choices=LOCALES)
    parser.add_argument("--kind", required=True, choices=KINDS)
    parser.add_argument("--limit", required=True, type=int)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if not (os.environ.get("DEEPL_API_KEY") or os.environ.get("LIBRETRANSLATE_URL")):
        parser.error("Configure DEEPL_API_KEY or LIBRETRANSLATE_URL locally; no service is configured")
    client = build_full_stack(cache_dir=DRAFT_DIR / "cache")
    output = DRAFT_DIR / f"wiki-{args.kind}-{args.locale}.jsonl"
    count = prepare_drafts(
        ROOT / "docs" / "kb_search_index.json",
        ROOT / "knowledge_base" / "hosted" / "content",
        output,
        locale=args.locale,
        kind=args.kind,
        client=client,
        limit=args.limit,
    )
    print(f"Wrote {count} unreviewed EN→{args.locale} drafts to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
