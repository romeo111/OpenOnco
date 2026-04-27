"""Static-site builder for the OpenOnco GitHub Pages landing.

Two goals (per user direction):

  1. Explain the project + show numerical metrics already achieved
     (KB scope, per-disease coverage, sources, etc.) — public landing.
  2. Let any visitor manually input a virtual patient profile and get
     a generated Plan back, in-browser, no backend.

The interactive engine demo (`try.html`) runs the real Python engine
in the browser via Pyodide:

    Pyodide loads → micropip installs pydantic + pyyaml → we unpack a
    zip of knowledge_base/ into the Pyodide filesystem → user submits
    patient JSON → generate_plan(...) runs → rendered HTML lands in
    an iframe.

Layout produced:

  docs/
    .nojekyll                      # disable Jekyll
    style.css                      # shared landing/gallery styles
    index.html                     # public landing (hero + stats + comparison)
    gallery.html                   # 7 pre-generated sample cases
    try.html                       # interactive Pyodide demo
    cases/<case-id>.html           # one rendered Plan / Diagnostic Brief
    openonco-engine-core.zip       # core engine + shared KB for Pyodide
    openonco-engine-index.json     # disease_id → per-disease bundle URL map
    disease/openonco-<slug>.zip    # per-disease KB modules (lazy-loaded)
    examples.json                  # dropdown payload for try.html

No real patient data ever flows here — only synthetic seed cases under
examples/, guarded by CHARTER §9.3.

Usage:

    python -m scripts.build_site [--output docs/] [--clean]
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
    orchestrate_mdt,
    render_diagnostic_brief_html,
    render_plan_html,
)
from knowledge_base.clients.ctgov_client import search_trials
from knowledge_base import __version__ as OPENONCO_VERSION
from knowledge_base.stats import collect_stats, format_html_widget
from scripts.site_cases import CASE_CATEGORIES, CASES, CaseEntry
from scripts.site_styles import STYLESHEET as _STYLE_CSS


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"
CTGOV_CACHE = KB_ROOT / "cache" / "ctgov"

GH_REPO = "romeo111/OpenOnco"
GH_NEW_ISSUE = f"https://github.com/{GH_REPO}/issues/new"

# Custom apex domain on GitHub Pages. The build writes a CNAME file every
# run so wiping docs/ via --clean never breaks the binding.
CUSTOM_DOMAIN = "openonco.info"



# ── Engine bundling for Pyodide ───────────────────────────────────────────


# What we ship to the browser. Engine code + schemas + validation + content.
# Excludes: code_systems/civic/ctcae (huge, not referenced at runtime),
# clients/, ingestion/ (need network), __pycache__, *.pyc.
_BUNDLE_INCLUDE_DIRS = [
    "engine",
    "schemas",
    "validation",
    "hosted/content",
]
_BUNDLE_INCLUDE_FILES = ["__init__.py"]


# Entity directories whose YAMLs are *split out* into per-disease modules
# when they tie to a specific disease via disease_id /
# applicable_to_disease / applicable_to.disease_id / relevant_diseases.
# Files from these dirs that don't resolve to any single disease (e.g.
# universal redflags, cross-disease indications) stay in core.
_DISEASE_SCOPED_DIRS = {
    "indications",
    "algorithms",
    "regimens",
    "redflags",
    "biomarker_actionability",
}


def _disease_id_for_yaml(yaml_text: str, arc_path: str) -> str | None:
    """Best-effort: which disease does this YAML belong to?

    Mirrors scripts/profile_engine_bundle.py — same heuristic — so the
    profile and the actual split agree. Returns None when:
      - the YAML doesn't pin to a single disease (universal RFs,
        cross-disease indications), OR
      - the file lives under diseases/ (handled separately — disease
        metadata always stays in core).
    """
    import re as _re
    if "/diseases/" in arc_path:
        # Disease metadata always stays in core, never sharded.
        return None
    m = _re.search(
        r"^\s*disease_id\s*:\s*(DIS-[A-Z0-9_-]+)", yaml_text, _re.MULTILINE,
    )
    if m:
        return m.group(1).upper()
    m = _re.search(
        r"^\s*applicable_to_disease\s*:\s*(DIS-[A-Z0-9_-]+)",
        yaml_text, _re.MULTILINE,
    )
    if m:
        return m.group(1).upper()
    m = _re.search(
        r"applicable_to\s*:\s*\n[\s\S]{0,400}?disease_id\s*:\s*(DIS-[A-Z0-9_-]+)",
        yaml_text,
    )
    if m:
        return m.group(1).upper()
    # redflags: relevant_diseases — only attribute when it pins to a
    # single concrete disease. Universal / multi-disease RFs stay in core.
    m = _re.search(
        r"^relevant_diseases\s*:\s*\n((?:\s*-\s*\S+\s*\n)+)",
        yaml_text, _re.MULTILINE,
    )
    if m:
        diseases = []
        for line in m.group(1).splitlines():
            tok = line.strip().lstrip("-").strip()
            if tok and tok != "*" and tok.upper().startswith("DIS-"):
                diseases.append(tok.upper())
        if len(diseases) == 1:
            return diseases[0]
    return None


def _disease_bundle_basename(disease_id: str) -> str:
    """`DIS-DLBCL-NOS` → `openonco-dis-dlbcl-nos.zip`. Used both for the
    file name on disk and for the URL in the bundle index."""
    slug = disease_id.lower().replace("_", "-")
    return f"openonco-{slug}.zip"


def _icd_to_disease_id_map() -> dict[str, str]:
    """Walk knowledge_base/hosted/content/diseases/*.yaml and produce a
    `{ICD-O-3 morphology code: DIS-...}` map. Shipped in the bundle index
    so the JS lazy-loader can resolve a `disease_id` from the patient's
    `disease.icd_o_3_morphology` without round-tripping into Pyodide."""
    import yaml as _yaml
    src = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
    out: dict[str, str] = {}
    if not src.is_dir():
        return out
    for path in sorted(src.glob("*.yaml")):
        try:
            data = _yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        did = data.get("id")
        code = (data.get("codes") or {}).get("icd_o_3_morphology")
        if did and code:
            out[str(code)] = str(did).upper()
    return out


def _gather_engine_entries() -> list[tuple[Path, str, str | None]]:
    """Walk knowledge_base/ and produce (source_path, archive_name,
    attributed_disease_id) tuples for every file that belongs in any
    bundle. attributed_disease_id is None for files that go in core.
    Code, schemas, validation, and shared content are always None.
    """
    src = REPO_ROOT / "knowledge_base"
    entries: list[tuple[Path, str, str | None]] = []

    for fname in _BUNDLE_INCLUDE_FILES:
        p = src / fname
        if p.is_file():
            entries.append((p, f"knowledge_base/{fname}", None))

    for sub in _BUNDLE_INCLUDE_DIRS:
        sub_root = src / sub
        if not sub_root.is_dir():
            continue
        for path in sub_root.rglob("*"):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            arcname = "knowledge_base/" + str(path.relative_to(src)).replace("\\", "/")

            attributed: str | None = None
            # Only YAML under hosted/content/<disease-scoped-dir>/ is
            # eligible to be sharded out.
            if path.suffix == ".yaml":
                parts = arcname.split("/")
                # parts: knowledge_base, hosted, content, <entity_dir>, ...
                if (
                    len(parts) >= 5
                    and parts[1] == "hosted"
                    and parts[2] == "content"
                    and parts[3] in _DISEASE_SCOPED_DIRS
                ):
                    try:
                        text = path.read_text(encoding="utf-8")
                    except OSError:
                        text = ""
                    attributed = _disease_id_for_yaml(text, arcname)

            entries.append((path, arcname, attributed))
    return entries


def bundle_engine(output_dir: Path) -> dict:
    """Build the Pyodide-loadable engine bundles.

    Produces (in `output_dir/`):

      1. `openonco-engine-core.zip` — code + schemas + validation +
         shared content (drugs, sources, biomarkers, tests,
         supportive_care, monitoring, workups, questionnaires,
         contraindications, mdt_skills, diseases, plus universal
         redflags and any indications/algorithms/regimens/RFs/BMA cells
         that don't pin to a single disease). /try.html fetches this
         first — small enough to make the page interactive quickly.

      2. `disease/openonco-{slug}.zip` per disease — the disease-scoped
         indications, algorithms, regimens, redflags, and BMA cells.
         Fetched on demand once the patient's `disease_id` is known.

      3. `openonco-engine-index.json` — `{core, core_version, diseases,
         disease_versions, icd_to_disease_id}`. /try.html consults this
         to pick the per-disease bundle once `disease_id` is known.

    CSD-9C (2026-04-27): the legacy monolithic `openonco-engine.zip`
    has been retired. Lazy-load (CSD-5B + CSD-6E) is the canonical
    path — the monolithic bundle had crossed the 3 MB ceiling and was
    only kept as a safety fallback. Any stale monolithic on disk is
    cleaned up so deploys don't carry the old file forever.

    Returns a dict whose `core_version` field is a 12-char SHA-256
    prefix of the core zip — used as a `?v=...` cache-buster on the
    Pyodide fetch so users always get fresh bundles on KB updates.
    """
    import hashlib

    core_zip = output_dir / "openonco-engine-core.zip"
    disease_dir = output_dir / "disease"
    index_path = output_dir / "openonco-engine-index.json"
    legacy_monolithic = output_dir / "openonco-engine.zip"

    disease_dir.mkdir(parents=True, exist_ok=True)

    # CSD-9C: clean up any stale monolithic bundle from previous builds.
    if legacy_monolithic.exists():
        legacy_monolithic.unlink()

    entries = _gather_engine_entries()
    # Deterministic order — same input → same zip → same SHA-256.
    entries.sort(key=lambda e: e[1])

    # Bucket by destination.
    core_entries: list[tuple[Path, str]] = []
    by_disease: dict[str, list[tuple[Path, str]]] = {}
    for path, arcname, disease in entries:
        if disease is None:
            core_entries.append((path, arcname))
        else:
            by_disease.setdefault(disease, []).append((path, arcname))

    # 1. Core bundle.
    core_files = 0
    core_uncompressed = 0
    with zipfile.ZipFile(core_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, arcname in core_entries:
            zf.write(path, arcname)
            core_files += 1
            core_uncompressed += path.stat().st_size
    core_bytes = core_zip.read_bytes()
    core_version = hashlib.sha256(core_bytes).hexdigest()[:12]

    # 2. Per-disease bundles. Wipe stale ones first so disease renames
    # don't leave orphans under docs/disease/.
    for stale in disease_dir.glob("openonco-*.zip"):
        stale.unlink()

    disease_meta: dict[str, dict] = {}
    for disease_id, items in sorted(by_disease.items()):
        out_name = _disease_bundle_basename(disease_id)
        out_path = disease_dir / out_name
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for path, arcname in items:
                zf.write(path, arcname)
        b = out_path.read_bytes()
        disease_meta[disease_id] = {
            "url": f"disease/{out_name}",
            "files": len(items),
            "compressed_bytes": out_path.stat().st_size,
            "version": hashlib.sha256(b).hexdigest()[:12],
        }

    # 3. Bundle index — what /try.html consults to know which
    # per-disease module to fetch once disease_id is known.
    index_payload = {
        "core": "openonco-engine-core.zip",
        "core_version": core_version,
        "diseases": {
            did: meta["url"] for did, meta in sorted(disease_meta.items())
        },
        "disease_versions": {
            did: meta["version"] for did, meta in sorted(disease_meta.items())
        },
        # CSD-6E: client-side ICD-O-3 → disease_id resolution. The /try.html
        # JS uses this so it can pick the per-disease bundle from a profile
        # whose only disease hint is `disease.icd_o_3_morphology`.
        "icd_to_disease_id": _icd_to_disease_id_map(),
    }
    index_path.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "core_zip": str(core_zip.relative_to(output_dir)),
        "core_files": core_files,
        "core_uncompressed_bytes": core_uncompressed,
        "core_compressed_bytes": core_zip.stat().st_size,
        "core_version": core_version,
        # `version` retained as alias for `core_version` — older callers
        # (try.html cache-buster wiring) still reference it as a generic
        # "current bundle version" stamp.
        "version": core_version,
        "disease_bundles": disease_meta,
        "index": str(index_path.relative_to(output_dir)),
    }


def write_service_worker(output_dir: Path, *, core_version: str = "") -> dict:
    """Write `docs/sw.js` — a tiny cache-first service worker for the
    bundle artifacts. Stores responses in a versioned `CacheStorage`
    bucket keyed by `core_version`, so a KB push (which rotates the
    SHA-256 prefix) automatically invalidates stale bundles on next
    fetch. CSD-6E polish — speeds up cold loads on repeat visits past
    what localStorage can hold (entire core + all visited diseases)."""
    cache_name = "openonco-bundle-" + (core_version or "v1")
    sw_js = """// OpenOnco bundle service worker (CSD-6E)
// Cache-first strategy for the lazy-load engine bundles. Cache name is
// stamped with the core bundle's SHA-256 prefix at build time, so any KB
// change automatically rotates the cache key and old bundles are evicted
// on the next install (see the activate handler).
const CACHE_NAME = '__CACHE_NAME__';
const PRECACHE = [
  '/openonco-engine-index.json',
  '/openonco-engine-core.zip',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      // Precache best-effort: don't fail the SW install if a single
      // file 404s (e.g. an old deploy that hasn't shipped the index yet).
      Promise.all(PRECACHE.map((u) => cache.add(u).catch(() => null)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k.startsWith('openonco-bundle-') && k !== CACHE_NAME)
            .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // Only intercept our own engine artifacts. Everything else (HTML, CSS,
  // CDN scripts) goes through the normal browser cache.
  const matches =
    url.pathname.endsWith('/openonco-engine-core.zip') ||
    url.pathname.endsWith('/openonco-engine-index.json') ||
    url.pathname.startsWith('/disease/openonco-');
  if (!matches) return;
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      cache.match(event.request, { ignoreSearch: true }).then((hit) =>
        hit || fetch(event.request).then((resp) => {
          // Only cache successful responses; never poison the cache with
          // an opaque 404.
          if (resp && resp.ok) {
            const clone = resp.clone();
            cache.put(event.request, clone);
          }
          return resp;
        })
      )
    )
  );
});
""".replace("__CACHE_NAME__", cache_name)
    out = output_dir / "sw.js"
    out.write_text(sw_js, encoding="utf-8")
    return {"path": "sw.js", "cache_name": cache_name}


def bundle_examples(output_dir: Path) -> dict:
    """Write docs/examples.json — array of {label, json} entries used as
    the 'Load example' dropdown on try.html.

    Also extracts a thin manifest (label + disease_icd only, ~10× smaller)
    used by /try.html for instant dropdown population. Full payload is
    lazy-fetched only when a user actually picks an example.
    """
    payload = []
    manifest = []
    for c in CASES:
        p = EXAMPLES / c.file
        if not p.exists():
            continue
        ex_json = json.loads(p.read_text(encoding="utf-8"))
        payload.append({
            "case_id": c.case_id,
            "label": c.label_ua,
            "file": c.file,
            "json": ex_json,
        })
        manifest.append({
            "case_id": c.case_id,
            "label": c.label_ua,
            "disease_icd": (
                ex_json.get("disease", {}).get("icd_o_3_morphology")
                if isinstance(ex_json, dict) else None
            ),
        })
    out = output_dir / "examples.json"
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "path": "examples.json",
        "count": len(payload),
        "manifest": manifest,
    }


def bundle_questionnaires(output_dir: Path) -> dict:
    """Pre-render all curated Questionnaire YAML files to a single
    JSON file at docs/questionnaires.json + thin manifest for /try.html.

    Manifest carries only the dropdown-needed fields (id + title +
    disease_icd) — ~30× smaller than the full payload — so /try.html
    populates dropdowns instantly. Full payload is lazy-fetched only
    after the user selects a questionnaire.
    """
    qsrc = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "questionnaires"
    payload = []
    manifest = []
    if qsrc.is_dir():
        import yaml as _yaml
        for path in sorted(qsrc.glob("*.yaml")):
            try:
                data = _yaml.safe_load(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    payload.append(data)
                    manifest.append({
                        "id": data.get("id"),
                        "title": data.get("title"),
                        "disease_icd": (
                            (data.get("fixed_fields") or {})
                            .get("disease", {})
                            .get("icd_o_3_morphology")
                        ),
                    })
            except Exception:
                continue
    out = output_dir / "questionnaires.json"
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "path": "questionnaires.json",
        "count": len(payload),
        "manifest": manifest,
    }


# ── Landing page (index.html) ─────────────────────────────────────────────


_NAV_LABELS = {
    "uk": {"home": "Головна", "gallery": "Приклади", "try_cta": "Спробувати →", "diseases": "Хвороби"},
    "en": {"home": "Home", "gallery": "Examples", "try_cta": "Try it →", "diseases": "Diseases"},
}


def _lang_switch_href(page_kind: str, target_lang: str, case_id: str = "") -> str:
    """Build the URL the language-toggle should point to.

    page_kind: 'home' | 'gallery' | 'try' | 'case' | 'capabilities' | 'limitations'
    target_lang: UA-side render asks where the EN mirror lives;
                 EN-side render asks where the UA mirror lives.

    Uses root-relative absolute paths so any nesting depth resolves
    correctly on openonco.info."""
    en_prefix = "/en"
    if target_lang == "uk":
        # UA page → switcher points to EN mirror
        if page_kind == "home":         return f"{en_prefix}/"
        if page_kind == "gallery":      return f"{en_prefix}/gallery.html"
        if page_kind == "try":          return f"{en_prefix}/try.html"
        if page_kind == "case":         return f"{en_prefix}/cases/{case_id}.html"
        if page_kind == "capabilities": return f"{en_prefix}/capabilities.html"
        if page_kind == "limitations":  return f"{en_prefix}/limitations.html"
        if page_kind == "diseases":     return f"{en_prefix}/diseases.html"
    else:
        # EN page → switcher points to UA root
        if page_kind == "home":         return "/"
        if page_kind == "gallery":      return "/gallery.html"
        if page_kind == "try":          return "/try.html"
        if page_kind == "case":         return f"/cases/{case_id}.html"
        if page_kind == "capabilities": return "/capabilities.html"
        if page_kind == "limitations":  return "/limitations.html"
        if page_kind == "diseases":     return "/diseases.html"
    return "/"


def _render_top_bar(active: str = "", target_lang: str = "uk",
                    lang_switch_href: str = "/en/") -> str:
    """Top navigation bar with:
    - brand on the left → links to home
    - reading-only nav (Home, Examples, optional Capabilities/Limitations
      on UA, GitHub) in the middle
    - language switcher (UA / EN toggle) on the right
    - prominent CTA "Try it" button on the far right (action, not reading)

    Per user direction: 'Спробувати' is an action and gets a separate CTA
    button styled distinctly from the nav links."""
    def cls(name: str) -> str:
        return ' class="active"' if active == name else ""

    labels = _NAV_LABELS.get(target_lang, _NAV_LABELS["uk"])
    home_path = "/" if target_lang == "uk" else "/en/"
    gallery_path = "/gallery.html" if target_lang == "uk" else "/en/gallery.html"
    try_path = "/try.html" if target_lang == "uk" else "/en/try.html"

    # Capabilities + Limitations now have EN mirrors; Specs stays UA-only
    # (the spec documents themselves are UA, so no point routing EN nav to them).
    extra_links = ""
    if target_lang == "uk":
        extra_links = (
            f'<a href="/diseases.html"{cls("diseases")}>Хвороби</a>'
            f'<a href="/capabilities.html"{cls("capabilities")}>Можливості</a>'
            f'<a href="/limitations.html"{cls("limitations")}>Обмеження</a>'
            f'<a href="/specs.html"{cls("specs")}>Специфікації</a>'
        )
    else:  # target_lang == "en"
        extra_links = (
            f'<a href="/en/diseases.html"{cls("diseases")}>Diseases</a>'
            f'<a href="/en/capabilities.html"{cls("capabilities")}>Capabilities</a>'
            f'<a href="/en/limitations.html"{cls("limitations")}>Limitations</a>'
        )

    cur_flag_cls = "flag-ua" if target_lang == "uk" else "flag-en"
    other_flag_cls = "flag-en" if target_lang == "uk" else "flag-ua"
    cur_lang = "UA" if target_lang == "uk" else "EN"
    other_lang = "EN" if target_lang == "uk" else "UA"

    return f"""<header class="top-bar">
  <div class="brand-line">
    <a href="{home_path}" class="brand-mini">OpenOnco</a>
    <span class="brand-version" title="Project version">v{OPENONCO_VERSION}</span>
  </div>
  <nav class="top-nav">
    <a href="{home_path}"{cls("home")}>{labels['home']}</a>
    {extra_links}
    <a href="{gallery_path}"{cls("gallery")}>{labels['gallery']}</a>
    <a href="https://github.com/{GH_REPO}" target="_blank" rel="noopener">GitHub</a>
  </nav>
  <div class="top-right">
    <div class="lang-switch" role="group" aria-label="Language">
      <span class="lang-current"><span class="lang-flag {cur_flag_cls}" aria-hidden="true"></span>{cur_lang}</span>
      <a class="lang-other" href="{lang_switch_href}"><span class="lang-flag {other_flag_cls}" aria-hidden="true"></span>{other_lang}</a>
    </div>
    <a href="{try_path}" class="btn-cta-try" {'aria-current="page"' if active == "try" else ""}>{labels['try_cta']}</a>
  </div>
</header>"""


def render_landing(stats, *, target_lang: str = "uk") -> str:
    # Most corpus-mass cards live on /capabilities.html. The landing pulls
    # only the headline counters (diseases, redflags, indications, regimens,
    # algorithms) so the "Ready for patients today" / "Red flags" cards stay
    # in lock-step with the KB instead of drifting into stale text.
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_redflags = by_type.get("redflags", 0)
    n_indications = by_type.get("indications", 0)
    n_regimens = by_type.get("regimens", 0)
    n_algorithms = by_type.get("algorithms", 0)

    if target_lang == "en":
        hero_h1 = "Open-source infrastructure for oncology clinical decision-making"
        hero_sub = (
            "Get clear, evidence-based treatment strategies in minutes. Upload a patient "
            "profile to receive standard and aggressive options, built on global clinical "
            "guidelines and references. Transparent and based on internationally recognized "
            "standards."
        )
        cta_primary = "Try with a virtual patient →"
        cta_secondary = "See examples"
        try_href = "/en/try.html"
        gallery_href = "/en/gallery.html"
        capabilities_href = "/en/capabilities.html"
        how_h2 = "Why it matters and how it works"
        how_lead_1 = (
            "To prescribe a treatment, an oncologist or clinical pharmacologist spends "
            "2–4&nbsp;hours of manual work: opening the NCCN PDF, cross-checking the ESMO "
            "guideline, re-reading the MoH protocol, verifying the national formulary for "
            "drug availability, looking up renal/hepatic dose adjustments, adding "
            "supportive care, remembering vaccinations and opportunistic-infection "
            "prophylaxis. Every time, for every patient, from scratch. Any missed "
            "contraindication can cost a life."
        )
        how_lead_2 = (
            "OpenOnco automates the grunt work: <strong>the logic is the same as a "
            "classic multidisciplinary team (MDT)</strong>, augmented by an analytical "
            "layer. Several specialists around the patient, case discussion, an agreed "
            "plan, return to the case when new data arrives. We simply formalize this as "
            "a structured engine — each &laquo;virtual specialist&raquo; is a versioned "
            "module with its own rules and source list. The clinician receives a ready "
            "draft plan with all citations and only verifies and tunes it for the "
            "specific patient."
        )
        trust_1_strong = "AI is not the doctor."
        trust_1_text = (
            "No LLM decides what to prescribe — clinical logic runs in a declarative "
            "rule engine."
        )
        trust_2_strong = "No external LLM calls"
        trust_2_text = (
            "when a plan is built. Every algorithm is open and auditable line-by-line on "
            "GitHub."
        )
        trust_3_strong = "only to scientific databases"
        trust_3_text_pre = "Lookups go"
        trust_3_text_post = ": PubMed, ClinicalTrials.gov, DailyMed, openFDA, NCCN/ESMO, MoH."
        df_aria = "OpenOnco — data flow from patient profile to two treatment plans"
        df1_title = "Patient profile"
        df1_body = (
            "FHIR R4 / mCODE: diagnosis, stage, histology, biomarkers, labs, prior lines, "
            "comorbidities."
        )
        df1_aria = "Example patient biomarkers"
        df2_title = "Open-standards verification"
        df2_body = (
            "Every diagnosis code, lab value, dose and drug is grounded in a public "
            "international standard. No closed vocabularies."
        )
        df2_aria = "Open standards used for verification"
        df3_title = "Red flags, dose adjustments, links"
        df3_body = (
            "A declarative rule engine surfaces risks, auto-adjusts dosing, and wires "
            "biomarker → drug → monitoring connections."
        )
        df3_li_1 = f"{n_redflags} red flags across {n_diseases} diseases"
        df3_li_2 = "renal / hepatic / age / weight adjustments"
        df3_li_3 = "biomarker ↔ regimen ↔ monitoring"
        df4_title = "Two plans with full citations"
        df4_body = (
            "<strong>Standard</strong> (guideline-grade) + <strong>aggressive</strong> "
            "(trials with higher efficacy). Every claim is a versioned citation. Plans "
            "refresh automatically as new data arrives."
        )
        moh_label = "MoH"
        why_today_h = "Why start using it today"
        why_cards = [
            ("2–4 hours → 5 minutes",
             "Less time on manual NCCN/ESMO/MoH cross-checking, more patients seen. "
             "Fewer missed contraindications, less harm."),
            ("No black box",
             "An LLM is not the decision-maker — a declarative rule engine is, with "
             "public code and a public KB. Plans are built <strong>without external LLM "
             "calls</strong>; only scientific databases (PubMed, ClinicalTrials.gov, "
             "DailyMed, openFDA) are queried. The clinician sees every &laquo;why&raquo; "
             "alongside every &laquo;what&raquo;."),
            ("Biomarkers you won&rsquo;t miss",
             "TP53, CD30, MYD88, eGFR, hepatic function — every flag automatically "
             "rewrites the plan: contraindications, dose adjustments, supportive care, "
             "monitoring."),
            ("New data → instant re-check",
             "Fresh labs or clinician decisions update both plans automatically — no "
             "need to re-sweep all the sources by hand."),
            ("MoH registration & NHSU coverage next to every drug",
             "Each drug in the plan is tagged: whether it is registered in Ukraine "
             "(MoH) and whether it is reimbursed by the state medical-guarantees "
             "programme (NHSU). The clinician immediately sees what is free, what is "
             "by prescription, and what has to be sourced separately. Access is "
             "<strong>metadata shown next to the recommendation</strong>, not a filter "
             "— regimen choice is driven by evidence, not by registration status."),
            ("Patient-friendly simplified report",
             "A separate mode generates a plain-language version of the plan for the "
             "patient: no Latin, no acronyms, with explanations of why each step was "
             "chosen and what to watch for between visits. Same plan, two voices — "
             "clinical for the oncologist, human for the patient."),
            ("Free, open, forever",
             "MIT-style. No paywall, no restrictions for public hospitals. Open-source "
             "means it can&rsquo;t quietly disappear or be locked behind investors "
             "tomorrow."),
            ("Ready for patients today",
             f"{n_diseases} diseases, {n_redflags} red flags, {n_indications} indications, "
             f"{n_regimens} regimens, {n_algorithms} treatment algorithms — clinical sign-off "
             "received. The first real-patient plans were rated strong by practising "
             "oncologists. The KB grows weekly, but it is already the densest open "
             "evidence-to-plan layer for Ukrainian oncology that exists. No reason to wait."),
        ]
        why_today_foot = (
            "Every missed biomarker can cost a life. Every hour of manual cross-checking "
            "is an hour the patient waits for a decision. The tool is ready today — "
            "start with a virtual patient and see your typical case through a layer of "
            "open standards."
        )
        why_cta_secondary = "What&rsquo;s currently in the KB"
    else:
        hero_h1 = "Open-source інфраструктура клінічних рішень в онкології"
        hero_sub = (
            "Отримайте зрозумілі, доказово обґрунтовані стратегії лікування за хвилини. "
            "Завантажте профіль пацієнта — і отримайте стандартний та агресивний варіанти "
            "на основі світових клінічних настанов і референсів. Прозоро та відповідно до "
            "міжнародно визнаних стандартів."
        )
        cta_primary = "Спробувати з віртуальним пацієнтом →"
        cta_secondary = "Дивитись приклади"
        try_href = "try.html"
        gallery_href = "gallery.html"
        capabilities_href = "capabilities.html"
        how_h2 = "Чому це потрібно і як це працює"
        how_lead_1 = (
            "Щоб призначити лікування, лікар або клінічний фармаколог витрачає "
            "2–4&nbsp;години ручної роботи: відкриває NCCN PDF, звіряє ESMO guideline, "
            "перечитує МОЗ протокол, перевіряє НСЗУ-формуляр на доступність препарату, "
            "шукає dose adjustments для нирок чи печінки, додає supportive care, не "
            "забуває про вакцинації та профілактику опортуністичних інфекцій. І так — "
            "для кожного пацієнта, кожного разу заново. Будь-яка пропущена "
            "контраіндикація може коштувати життя."
        )
        how_lead_2 = (
            "OpenOnco автоматизує цю чорнову роботу: <strong>логіка така сама, як у "
            "класичної мультидисциплінарної команди (MDT)</strong>, посиленої шаром "
            "аналітичних алгоритмів. Кілька спеціалістів навколо пацієнта, обговорення "
            "випадку, узгоджений план, повернення до випадку при появі нових даних. Ми "
            "просто оформлюємо це як structured engine — кожен &laquo;віртуальний "
            "лікар&raquo; це модуль із власною версією, правилами та списком джерел. "
            "Лікар отримує готовий проєкт плану з усіма посиланнями і лише верифікує та "
            "коригує його під конкретного пацієнта."
        )
        trust_1_strong = "AI не є лікарем."
        trust_1_text = (
            "LLM не вирішує, що призначати — клінічну логіку виконує декларативний "
            "rule engine."
        )
        trust_2_strong = "Жодних викликів зовнішніх LLM"
        trust_2_text = (
            "у момент побудови плану. Усі алгоритми відкриті, перевіряються "
            "рядок-за-рядком на GitHub."
        )
        trust_3_strong = "лише в наукові бази"
        trust_3_text_pre = "Запити йдуть"
        trust_3_text_post = ": PubMed, ClinicalTrials.gov, DailyMed, openFDA, NCCN/ESMO, МОЗ."
        df_aria = "OpenOnco — потік даних від профілю пацієнта до двох планів лікування"
        df1_title = "Профіль пацієнта"
        df1_body = (
            "FHIR R4 / mCODE: діагноз, стадія, гістологія, біомаркери, лабораторні "
            "показники, попередні лінії терапії, коморбідності."
        )
        df1_aria = "Приклад біомаркерів пацієнта"
        df2_title = "Верифікація відкритими стандартами"
        df2_body = (
            "Кожен код діагнозу, лабораторний показник, доза й препарат — у публічному "
            "міжнародному стандарті. Жодних закритих словників."
        )
        df2_aria = "Відкриті стандарти, якими верифікуються дані"
        df3_title = "Red flags, корекції та зв&rsquo;язки"
        df3_body = (
            "Декларативний rule engine знаходить ризики, автоматично коригує дози й "
            "вибудовує зв&rsquo;язки біомаркер → препарат → моніторинг."
        )
        df3_li_1 = f"{n_redflags} червоних прапорців по {n_diseases} діагнозах"
        df3_li_2 = "корекції на нирки, печінку, вік, вагу"
        df3_li_3 = "зв&rsquo;язок біомаркер ↔ режим ↔ моніторинг"
        df4_title = "Два плани з повними цитатами"
        df4_body = (
            "<strong>Стандартний</strong> (за керівницями) + <strong>агресивний</strong> "
            "(трайали з вищою ефективністю). Кожне твердження — посилання на джерело з "
            "версією. План оновлюється автоматично, щойно з&rsquo;являються нові дані."
        )
        moh_label = "МОЗ"
        why_today_h = "Чому варто почати користуватись уже сьогодні"
        why_cards = [
            ("2–4 години → 5 хвилин",
             "Лікар витрачає менше часу на чорнову звірку NCCN/ESMO/МОЗ і встигає "
             "прийняти більше пацієнтів. Менше пропущених контраіндикацій — менше шкоди."),
            ("Жодного &laquo;чорного ящика&raquo;",
             "Не LLM вирішує лікування, а декларативний rule engine із публічним кодом "
             "і публічною KB. План будується <strong>без викликів зовнішніх LLM</strong> "
             "— лише запити в наукові бази (PubMed, ClinicalTrials.gov, DailyMed, "
             "openFDA). Лікар бачить кожне &laquo;чому&raquo; поряд із кожним "
             "&laquo;що&raquo;."),
            ("Біомаркери, які не пропустиш",
             "TP53, CD30, MYD88, eGFR, печінкова функція — кожен прапорець автоматично "
             "переписує план: контраіндикації, корекція дози, supportive care, моніторинг."),
            ("Перевірка нових даних — миттєво",
             "Свіжі лабораторні чи рішення лікаря оновлюють обидва плани автоматично, "
             "без повторного ручного перебору джерел."),
            ("Реєстрація МОЗ та покриття НСЗУ — поряд із кожним препаратом",
             "Кожен препарат у плані позначений: чи зареєстрований в Україні (МОЗ) і чи "
             "покривається державною програмою медичних гарантій (НСЗУ). Лікар одразу "
             "бачить, що доступно безкоштовно, що — за рецептом, а що доведеться шукати "
             "окремо. Доступність — це <strong>метадані поряд із рекомендацією</strong>, "
             "а не фільтр: вибір режиму керується доказами, а не реєстраційним статусом."),
            ("Спрощений звіт для пацієнта",
             "Окремий режим генерує версію плану зрозумілою мовою для пацієнта: без "
             "латини, без абревіатур, з поясненням, чому призначено саме це і на що "
             "звертати увагу між візитами. Той самий план, дві мови — клінічна для лікаря, "
             "людська для пацієнта."),
            ("Безкоштовно, відкрито, назавжди",
             "MIT-style. Без paywall, без обмежень для державних лікарень. Open-source "
             "гарантує, що завтра воно нікуди не зникне і його не &laquo;закриють&raquo; "
             "інвестори."),
            ("Готово до пацієнтів сьогодні",
             f"{n_diseases} діагнозів, {n_redflags} червоних прапорців, {n_indications} "
             f"індикацій, {n_regimens} режимів, {n_algorithms} алгоритмів лікування — "
             "клінічний sign-off отриманий. Перші реальні плани вже верифіковані "
             "практикуючими онкологами як сильні. KB росте щотижня, але це вже найщільніший "
             "відкритий шар «доказ → план» для української онкології, що існує. Немає сенсу чекати."),
        ]
        why_today_foot = (
            "Кожен пропущений біомаркер може коштувати життя. Кожна година ручного "
            "звіряння — це години, які пацієнт чекає рішення. Інструмент готовий вже "
            "сьогодні — почніть із віртуального пацієнта і подивіться, як виглядає ваш "
            "типовий випадок крізь шар відкритих стандартів."
        )
        why_cta_secondary = "Що зараз у базі знань"

    why_cards_html = "\n".join(
        f'        <div class="why-card">\n'
        f'          <div class="why-card-h">{h}</div>\n'
        f'          <p>{p}</p>\n'
        f'        </div>'
        for h, p in why_cards
    )

    return f"""<!DOCTYPE html>
<html lang="{'en' if target_lang == 'en' else 'uk'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco — Open-source CDS for oncology</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="home", target_lang=target_lang, lang_switch_href=_lang_switch_href("home", target_lang))}

<main>
  <section class="hero">
    <div class="hero-content">
      <h1>{hero_h1}</h1>
      <p class="hero-sub">
        {hero_sub}
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="{try_href}">{cta_primary}</a>
        <a class="btn btn-secondary" href="{gallery_href}">{cta_secondary}</a>
      </div>
    </div>
  </section>

  <section class="how">
    <h2>{how_h2}</h2>
    <p class="how-lead">
      {how_lead_1}
    </p>
    <p class="how-lead">
      {how_lead_2}
    </p>

    <div class="trust-strip" role="note">
      <div class="trust-pill trust-pill--no">
        <span class="trust-pill-mark">×</span>
        <span class="trust-pill-text"><strong>{trust_1_strong}</strong> {trust_1_text}</span>
      </div>
      <div class="trust-pill trust-pill--no">
        <span class="trust-pill-mark">×</span>
        <span class="trust-pill-text"><strong>{trust_2_strong}</strong> {trust_2_text}</span>
      </div>
      <div class="trust-pill trust-pill--yes">
        <span class="trust-pill-mark">✓</span>
        <span class="trust-pill-text">{trust_3_text_pre} <strong>{trust_3_strong}</strong>{trust_3_text_post}</span>
      </div>
    </div>

    <div class="dataflow" aria-label="{df_aria}">
      <div class="dataflow-stage" data-stage="1">
        <div class="dataflow-num">01 · INPUT</div>
        <div class="dataflow-title">{df1_title}</div>
        <div class="dataflow-body">
          {df1_body}
          <div class="biomarker-row" aria-label="{df1_aria}">
            <span class="biomarker">CD30+</span>
            <span class="biomarker">BCL2/MYC</span>
            <span class="biomarker">TP53</span>
            <span class="biomarker">IPI 4</span>
            <span class="biomarker">eGFR 42</span>
          </div>
        </div>
      </div>
      <div class="dataflow-arrow" aria-hidden="true">→</div>
      <div class="dataflow-stage" data-stage="2">
        <div class="dataflow-num">02 · VERIFY</div>
        <div class="dataflow-title">{df2_title}</div>
        <div class="dataflow-body">
          {df2_body}
          <div class="std-row" aria-label="{df2_aria}">
            <span class="std-pill">ICD-O-3</span>
            <span class="std-pill">LOINC</span>
            <span class="std-pill">RxNorm</span>
            <span class="std-pill">ATC</span>
            <span class="std-pill">CTCAE v5</span>
            <span class="std-pill">NCCN</span>
            <span class="std-pill">ESMO</span>
            <span class="std-pill">{moh_label}</span>
          </div>
        </div>
      </div>
      <div class="dataflow-arrow" aria-hidden="true">→</div>
      <div class="dataflow-stage" data-stage="3">
        <div class="dataflow-num">03 · BIOMARKERS</div>
        <div class="dataflow-title">{df3_title}</div>
        <div class="dataflow-body">
          {df3_body}
          <ul class="flow-list">
            <li><span class="rf-tag rf-red">RF</span> {df3_li_1}</li>
            <li><span class="rf-tag rf-amber">DOSE</span> {df3_li_2}</li>
            <li><span class="rf-tag rf-teal">LINK</span> {df3_li_3}</li>
          </ul>
        </div>
      </div>
      <div class="dataflow-arrow" aria-hidden="true">→</div>
      <div class="dataflow-stage" data-stage="4">
        <div class="dataflow-num">04 · OUTPUT</div>
        <div class="dataflow-title">{df4_title}</div>
        <div class="dataflow-body">
          {df4_body}
        </div>
      </div>
    </div>

    <div class="why-today">
      <h3 class="why-today-h">{why_today_h}</h3>
      <div class="why-today-grid">
{why_cards_html}
      </div>
      <p class="why-today-foot">
        {why_today_foot}
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="{try_href}">{cta_primary}</a>
        <a class="btn btn-secondary" href="{capabilities_href}">{why_cta_secondary}</a>
      </div>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    Жодних реальних пацієнтських даних · CHARTER §9.3.
    Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


# ── Gallery page ──────────────────────────────────────────────────────────


def _questionnaire_icd_o_3_codes() -> set:
    """ICD-O-3 morphology codes for which we have a curated questionnaire.
    Used to decide whether a gallery card opens into a real form or just
    a JSON dump on /try.html."""
    qsrc = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "questionnaires"
    codes: set = set()
    if not qsrc.is_dir():
        return codes
    import yaml as _yaml
    for path in qsrc.glob("*.yaml"):
        try:
            data = _yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        code = (
            ((data or {}).get("fixed_fields") or {}).get("disease") or {}
        ).get("icd_o_3_morphology")
        if code:
            codes.add(code)
    return codes


def _case_has_questionnaire(case: CaseEntry, codes: set) -> bool:
    """True if the case's example JSON has a disease ICD-O-3 code that
    matches a curated questionnaire."""
    p = EXAMPLES / case.file
    if not p.exists():
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    code = ((data or {}).get("disease") or {}).get("icd_o_3_morphology")
    return bool(code and code in codes)


def render_gallery(stats_widget_html: str, *, target_lang: str = "uk") -> str:
    is_en = target_lang == "en"
    case_path_prefix = "/en/cases/" if is_en else "/cases/"
    n_cases = len(CASES)

    quest_codes = _questionnaire_icd_o_3_codes()

    cat_counts: dict[str, int] = {}
    for c in CASES:
        cat_counts[c.category] = cat_counts.get(c.category, 0) + 1

    chips: list[str] = []
    all_label = "All" if is_en else "Усі"
    chips.append(
        f'<button type="button" class="case-chip is-active" '
        f'data-filter="all">{all_label} <span class="chip-n">{n_cases}</span></button>'
    )
    for key, ua_label, en_label in CASE_CATEGORIES:
        n = cat_counts.get(key, 0)
        if n == 0:
            continue
        label = en_label if is_en else ua_label
        chips.append(
            f'<button type="button" class="case-chip" '
            f'data-filter="{key}">{label} <span class="chip-n">{n}</span></button>'
        )
    chips_html = "\n    ".join(chips)

    if is_en:
        sort_label = "Sort"
        sort_default = "Default"
        sort_alpha = "Name (A→Z)"
        sort_category = "Category"
    else:
        sort_label = "Сортування"
        sort_default = "За замовчуванням"
        sort_alpha = "За назвою (А→Я)"
        sort_category = "За класифікацією"

    cards: list[str] = []
    for i, c in enumerate(CASES):
        has_quest = _case_has_questionnaire(c, quest_codes)
        json_only_pill = "" if has_quest else (
            f'<span class="case-json-only" title="'
            f'{("Form not yet available — opens as JSON on Try-it" if is_en else "Опитувальник для цієї хвороби ще не готовий — на Try-it відкриється як JSON")}'
            f'">{"JSON-only" if is_en else "JSON-only"}</span>'
        )
        cards.append(
            f"""<a class="case-card" href="{case_path_prefix}{c.case_id}.html"
   data-category="{c.category}" data-default-order="{i}"
   data-name="{c.label_ua}">
  <div class="case-badge-row">
    <div class="case-badge {c.badge_class}">{c.badge}</div>
    {json_only_pill}
  </div>
  <h3>{c.label_ua}</h3>
  <p>{c.summary_ua}</p>
  <div class="case-foot">{c.file}</div>
</a>"""
        )
    cards_html = "\n".join(cards)

    if is_en:
        lead_html = (
            f'{n_cases} synthetic patient profiles run through the engine. '
            f'Each click opens a full Plan or Diagnostic Brief as a clinician '
            f'would see it in tumor-board. If something looks clinically wrong '
            f'or confusing — <a href="{GH_NEW_ISSUE}?title=%5Bfeedback%5D+&labels=tester-feedback" '
            f'target="_blank" rel="noopener">open an issue on GitHub</a> '
            f'with a link to the specific case.'
        )
    else:
        lead_html = (
            f'{n_cases} синтетичних профілів пацієнтів, прогнаних через рушій. '
            f'Кожен клік відкриває повний Plan або Diagnostic Brief, як його '
            f'побачить лікар у tumor-board. Якщо щось виглядає клінічно '
            f'неправильно або дезорієнтує — '
            f'<a href="{GH_NEW_ISSUE}?title=%5Bfeedback%5D+&labels=tester-feedback" '
            f'target="_blank" rel="noopener">відкрий issue на GitHub</a> '
            f'з посиланням на конкретний кейс.'
        )

    category_order_js = "[" + ",".join(
        f'"{key}"' for key, _ua, _en in CASE_CATEGORIES
    ) + "]"

    return f"""<!DOCTYPE html>
<html lang="{'en' if is_en else 'uk'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Sample cases</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="gallery", target_lang=target_lang, lang_switch_href=_lang_switch_href("gallery", target_lang))}

<main class="gallery">
  <h1>{'Sample cases' if is_en else 'Готові приклади'}</h1>
  <p class="lead">{lead_html}</p>

  <div class="case-controls">
    <div class="case-chips" role="group" aria-label="{'Filter by category' if is_en else 'Фільтр за класифікацією'}">
    {chips_html}
    </div>
    <label class="case-sort">
      <span>{sort_label}:</span>
      <select id="caseSort">
        <option value="default">{sort_default}</option>
        <option value="alpha">{sort_alpha}</option>
        <option value="category">{sort_category}</option>
      </select>
    </label>
  </div>

  <section class="case-grid" id="caseGrid">
    {cards_html}
  </section>

  <p class="case-empty" id="caseEmpty" hidden>
    {'No cases in this category.' if is_en else 'У цій категорії немає прикладів.'}
  </p>

  <section class="kb-stats">
    {stats_widget_html}
  </section>

  <footer class="page-foot">
    OpenOnco — open-source · MIT-style usage
    · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    · {'No real patient data' if is_en else 'Жодних реальних пацієнтських даних'} · CHARTER §9.3
  </footer>
</main>

<script>
(function() {{
  var grid = document.getElementById("caseGrid");
  var empty = document.getElementById("caseEmpty");
  var chips = document.querySelectorAll(".case-chip");
  var sort = document.getElementById("caseSort");
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".case-card"));
  var categoryOrder = {category_order_js};
  var activeFilter = "all";

  function applyFilter() {{
    var visible = 0;
    cards.forEach(function(card) {{
      var match = activeFilter === "all" || card.dataset.category === activeFilter;
      card.style.display = match ? "" : "none";
      if (match) visible++;
    }});
    empty.hidden = visible !== 0;
  }}

  function applySort() {{
    var mode = sort.value;
    var sorted = cards.slice();
    if (mode === "alpha") {{
      sorted.sort(function(a, b) {{
        return a.dataset.name.localeCompare(b.dataset.name, "uk");
      }});
    }} else if (mode === "category") {{
      sorted.sort(function(a, b) {{
        var ai = categoryOrder.indexOf(a.dataset.category);
        var bi = categoryOrder.indexOf(b.dataset.category);
        if (ai !== bi) return ai - bi;
        return parseInt(a.dataset.defaultOrder, 10) - parseInt(b.dataset.defaultOrder, 10);
      }});
    }} else {{
      sorted.sort(function(a, b) {{
        return parseInt(a.dataset.defaultOrder, 10) - parseInt(b.dataset.defaultOrder, 10);
      }});
    }}
    sorted.forEach(function(card) {{ grid.appendChild(card); }});
  }}

  chips.forEach(function(chip) {{
    chip.addEventListener("click", function() {{
      chips.forEach(function(c) {{ c.classList.remove("is-active"); }});
      chip.classList.add("is-active");
      activeFilter = chip.dataset.filter;
      applyFilter();
    }});
  }});
  sort.addEventListener("change", applySort);
}})();
</script>
</body>
</html>
"""


# ── Try page (Pyodide interactive) ────────────────────────────────────────


_PYODIDE_VERSION = "0.26.4"


def render_try(
    *,
    target_lang: str = "uk",
    bundle_version: str = "",
    questionnaires_manifest: list = None,
    examples_manifest: list = None,
) -> str:
    # Pyodide assets live at site root — root-relative paths work for both
    # /try.html (UA) and /en/try.html (EN). The Pyodide engine bundle is
    # a single shared copy.
    #
    # Dropdown manifests (~15 KB total) are inlined as JS constants so the
    # form populates instantly. Full questionnaires.json (~640 KB) and
    # examples.json (~230 KB) are lazy-fetched only after the user selects
    # an option — saves ~870 KB on first paint.
    qm = questionnaires_manifest if questionnaires_manifest is not None else []
    em = examples_manifest if examples_manifest is not None else []
    qm_json = json.dumps(qm, ensure_ascii=False).replace("</", "<\\/")
    em_json = json.dumps(em, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!DOCTYPE html>
<html lang="{'en' if target_lang == 'en' else 'uk'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · {'Try it' if target_lang == 'en' else 'Спробувати'}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="try", target_lang=target_lang, lang_switch_href=_lang_switch_href("try", target_lang))}

<main class="try-page">
  <h1>Спробувати з віртуальним пацієнтом</h1>
  <p class="lead">
    Заповни короткий опитувальник по конкретній хворобі — engine у браузері (Pyodide)
    одразу показує які поля тригерять зміну плану. <strong>Жодних реальних пацієнтських
    даних.</strong> Чернетка зберігається у browser localStorage.
  </p>

  <!-- Top status banner — prominent, sticky-ish, animated while loading
       so the user sees that something is happening even when the engine
       is mid-fetch. Mirrors the smaller #status in the sidebar. -->
  <div id="statusTop" class="status-top is-busy" data-kind="info" role="status" aria-live="polite">
    <span class="status-top-spinner" aria-hidden="true"></span>
    <span class="status-top-text">Завантажую опитувальники…</span>
  </div>

  <div class="quest-toolbar">
    <label class="qt-label">
      Хвороба
      <select id="diseaseSelect">
        <option value="">— оберіть —</option>
      </select>
    </label>
    <label class="qt-label">
      Завантажити приклад
      <select id="exampleSelect">
        <option value="">— оберіть —</option>
      </select>
    </label>
    <div class="qt-spacer"></div>
    <div class="qt-modes">
      <button id="modeFormBtn" class="mode-btn active" data-mode="form">Форма</button>
      <button id="modeJsonBtn" class="mode-btn" data-mode="json">Raw JSON (advanced)</button>
    </div>
    <button id="resetBtn" class="btn btn-secondary qt-reset">Очистити</button>
  </div>

  <div class="quest-grid">
    <section class="quest-form-pane" id="formPane">
      <div id="questIntro" class="quest-intro" hidden></div>
      <div id="exampleLockBanner" class="example-lock-banner" hidden>
        <div class="elb-text">
          <strong>📋 Завантажено приклад.</strong>
          Заповнені поля заблоковано, щоб випадково не змінити дані прикладу.
          Натисни кнопку, щоб редагувати все.
        </div>
        <button id="personalizeBtn" type="button" class="btn btn-secondary elb-btn">
          Персоналізувати цей приклад
        </button>
      </div>
      <div id="questGroups"></div>
      <div id="questEmpty" class="quest-empty">
        Оберіть хворобу зі списку вище, щоб почати опитування.
      </div>
    </section>

    <section class="quest-form-pane" id="jsonPane" hidden>
      <label class="qt-label">
        Patient profile (JSON)
        <textarea id="patientJson" rows="28" spellcheck="false"
                  placeholder='{{"patient_id": "...", "disease": {{"icd_o_3_morphology": "9699/3"}}, ...}}'></textarea>
      </label>
      <div class="try-actions">
        <button id="formatBtn" class="btn btn-secondary">Format JSON</button>
      </div>
    </section>

    <aside class="quest-side">
      <div class="quest-impact-card">
        <h3>Імпакт на план</h3>
        <div class="impact-progress">
          <div class="impact-bar">
            <div class="impact-bar-fill" id="progressFill"></div>
          </div>
          <div class="impact-stats">
            <span id="progressText">0 / 0</span>
            <span class="impact-pct" id="progressPct">0%</span>
          </div>
        </div>
        <div class="impact-section" id="impactMissingCritical">
          <h4>⚠️ Критичні поля без відповіді</h4>
          <ul></ul>
        </div>
        <div class="impact-section" id="impactRedflags">
          <h4>🚩 Red flags активовано</h4>
          <ul></ul>
        </div>
        <div class="impact-section" id="impactSelected">
          <h4>📋 Поточний default</h4>
          <p id="impactSelectedText">—</p>
        </div>
        <div class="impact-section" id="impactWarnings" hidden>
          <h4>⚙️ Engine warnings</h4>
          <ul></ul>
        </div>
      </div>

      <div class="try-actions quest-cta">
        <button id="runBtn" class="btn btn-primary" disabled>
          {'Generate full Plan' if target_lang == 'en' else 'Згенерувати повний Plan'}
        </button>
        <button id="viewPlanBtn" class="btn btn-primary" type="button" disabled>
          {'Show plan' if target_lang == 'en' else 'Показати план'}
        </button>
        <button id="pdfBtn" class="btn btn-primary" type="button" disabled
                title="{'Save as PDF via your browser print dialog' if target_lang == 'en' else 'Зберегти як PDF через діалог друку браузера'}">
          {'Download PDF' if target_lang == 'en' else 'Скачати PDF'}
        </button>
      </div>

      <div id="status" class="status">Завантажую опитувальники…</div>
      <div id="error" class="error" hidden></div>
    </aside>
  </div>

  <div id="planModal" class="plan-modal" hidden role="dialog" aria-modal="true"
       aria-label="{'Treatment plan' if target_lang == 'en' else 'План лікування'}">
    <div class="plan-modal-card">
      <div class="plan-modal-toolbar">
        <div class="rt-lang-group" role="group" aria-label="{'Plan language' if target_lang == 'en' else 'Мова плану'}">
          <span class="rt-lang-label">{'Language:' if target_lang == 'en' else 'Мова:'}</span>
          <button id="langUaBtn" class="rt-lang-btn" type="button" data-lang="uk">UA</button>
          <button id="langEnBtn" class="rt-lang-btn" type="button" data-lang="en">EN</button>
        </div>
        <div class="plan-modal-actions">
          <button id="modalPdfBtn" class="rt-btn" type="button"
                  title="{'Save as PDF via your browser print dialog' if target_lang == 'en' else 'Зберегти як PDF через діалог друку браузера'}">
            <span aria-hidden="true">📄</span> {'Download PDF' if target_lang == 'en' else 'Скачати PDF'}
          </button>
          <button id="planModalClose" class="rt-btn rt-btn-ghost" type="button"
                  aria-label="{'Close' if target_lang == 'en' else 'Закрити'}">✕</button>
        </div>
      </div>
      <iframe id="resultFrame"></iframe>
    </div>
  </div>

  <footer class="page-foot">
    Якщо щось не працює — <a href="{GH_NEW_ISSUE}?title=%5Btry-page%5D+&labels=tester-feedback" target="_blank" rel="noopener">відкрий issue</a>.
    Pyodide v{_PYODIDE_VERSION} · engine bundle <code>openonco-engine-core.zip</code> + per-disease modules.
  </footer>
</main>

<div id="initOverlay" class="init-overlay" hidden role="status" aria-live="polite">
  <div class="init-card">
    <h3>Готую двигун OpenOnco</h3>
    <p class="init-lead">Перший запуск триває ~10–20 секунд — двигун завантажується безпосередньо у твій браузер. Дані пацієнта не лишають твого пристрою.</p>
    <ol class="init-stages" id="initStages">
      <li data-stage="pyodide" class="stage pending">Готую обчислювач у браузері (~6 МБ)</li>
      <li data-stage="pydeps" class="stage pending">Налаштовую середовище</li>
      <li data-stage="bundle" class="stage pending">Завантажую базу знань OpenOnco</li>
      <li data-stage="validate" class="stage pending">Звіряю клінічну базу</li>
      <li data-stage="generate" class="stage pending">Будую персональний план</li>
    </ol>
    <p class="init-hint" id="initHint">Якщо зараз вийшло, наступного разу буде ~5 с — двигун залишається в пам'яті.</p>
  </div>
</div>

<div id="generatingOverlay" class="generating-overlay" hidden role="dialog" aria-live="polite" aria-modal="true">
  <div class="generating-card">
    <div class="generating-spinner" aria-hidden="true"></div>
    <h3>Генерую план…</h3>
    <p>Зачекай 5–15 с. Поля заблоковано, щоб результат відповідав поточному вводу.</p>
    <p class="generating-hint" id="generatingHint">Запускаю двигун…</p>
  </div>
</div>

<script type="module">
import {{ loadPyodide }} from "https://cdn.jsdelivr.net/pyodide/v{_PYODIDE_VERSION}/full/pyodide.mjs";

const STORAGE_KEY = 'openonco-try-draft-v1';

// ── DOM refs ──────────────────────────────────────────────────────────────
const status = document.getElementById('status');
const statusTop = document.getElementById('statusTop');
const statusTopText = statusTop ? statusTop.querySelector('.status-top-text') : null;
const errorBox = document.getElementById('error');
const runBtn = document.getElementById('runBtn');
const formatBtn = document.getElementById('formatBtn');
const resetBtn = document.getElementById('resetBtn');
const diseaseSelect = document.getElementById('diseaseSelect');
const exampleSelect = document.getElementById('exampleSelect');
const textarea = document.getElementById('patientJson');
const resultFrame = document.getElementById('resultFrame');
const pdfBtn = document.getElementById('pdfBtn');
const modalPdfBtn = document.getElementById('modalPdfBtn');
const viewPlanBtn = document.getElementById('viewPlanBtn');
const planModal = document.getElementById('planModal');
const planModalClose = document.getElementById('planModalClose');
const langUaBtn = document.getElementById('langUaBtn');
const langEnBtn = document.getElementById('langEnBtn');
const formPane = document.getElementById('formPane');
const jsonPane = document.getElementById('jsonPane');
const questGroups = document.getElementById('questGroups');
const questIntro = document.getElementById('questIntro');
const questEmpty = document.getElementById('questEmpty');
const modeFormBtn = document.getElementById('modeFormBtn');
const modeJsonBtn = document.getElementById('modeJsonBtn');

const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const progressPct = document.getElementById('progressPct');
const impactMissingCritical = document.getElementById('impactMissingCritical');
const impactRedflags = document.getElementById('impactRedflags');
const impactSelected = document.getElementById('impactSelected');
const impactSelectedText = document.getElementById('impactSelectedText');
const impactWarnings = document.getElementById('impactWarnings');
const generatingOverlay = document.getElementById('generatingOverlay');
const generatingHint = document.getElementById('generatingHint');
const mainTryEl = document.querySelector('main.try-page');
const initOverlay = document.getElementById('initOverlay');
const initStagesEl = document.getElementById('initStages');

// ── State ─────────────────────────────────────────────────────────────────
let pyodide = null;
let enginReady = false;
// CSD-6E + CSD-9C: bundle lazy-load state. `bundleIndex` is the parsed
// index (resolved from /openonco-engine-index.json); `coreBundleLoaded`
// is set after the first core extract; `loadedDiseases` remembers which
// per-disease modules we've already merged so re-runs against the same
// disease don't re-fetch. The legacy monolithic fallback was retired in
// CSD-9C — lazy-load is the only path now.
const BUNDLE_INDEX_URL = '/openonco-engine-index.json';
const CORE_BUNDLE_URL = '/openonco-engine-core.zip';
let bundleIndex = null;
let coreBundleLoaded = false;
const loadedDiseases = new Set();
// Build-time manifests — instant dropdown population, no fetch.
const QUESTIONNAIRES_MANIFEST = {qm_json};
const EXAMPLES_MANIFEST = {em_json};
let questionnaires = null;   // lazy-fetched from /questionnaires.json on first need
let examples = null;         // lazy-fetched from /examples.json on first need
let _questionnairesPromise = null;
let _examplesPromise = null;
let activeQuest = null;      // currently selected questionnaire
let generating = false;      // true while runEngine is mid-flight; blocks
                             // input via <main inert> + overlay so the
                             // rendered plan matches a stable snapshot
let previewToken = 0;        // bumped on each runLivePreview start AND on
                             // runEngine start; stale results are discarded
let answers = {{}};          // {{dotted_path: value}}
let mode = 'form';           // 'form' | 'json'
let evalDebounceTimer = null;    // preview debounce
let whatIfDebounceTimer = null;  // what-if debounce — separate + longer so
                                 // dropdowns/typing don't trigger expensive
                                 // shadow evals every 400ms
let lastPreviewResult = null;    // most recent preview result, fed to
                                 // what-if when its (longer) timer fires
const PREVIEW_DEBOUNCE_MS = 400;
const WHATIF_DEBOUNCE_MS = 1500;

// Initial render language follows the page lang (UA on /try.html, EN on
// /en/try.html). User can switch via the buttons in the result toolbar
// without re-running the engine — Pyodide caches _oo_result/_oo_mdt.
let currentResultLang = '{target_lang}';

// planSource tracks where the plan currently shown in the modal came from:
//   null        — no plan yet (form not generated, no example loaded)
//   'example'   — pre-built case HTML loaded from /cases/<case_id>.html;
//                 generate stays disabled because plan IS already generated,
//                 we don't want to lie that clicking does new work
//   'generated' — engine produced this plan from the current profile
// planDirty flips to true the moment the user edits any field (form or JSON)
// after a plan has been shown, which re-enables Generate so the user can
// recompute against the modified profile.
let planSource = null;
let planDirty = false;
let activeExampleCaseId = null;

// ── Helpers ───────────────────────────────────────────────────────────────
function setStatus(msg, kind = 'info', topMode = 'auto') {{
  status.textContent = msg;
  status.dataset.kind = kind;
  // Mirror to the prominent top banner.
  //  topMode='busy'  → spinner, blue
  //  topMode='ok'    → green ✓
  //  topMode='warn'  → amber
  //  topMode='hide'  → hide top banner (sidebar still updates)
  //  topMode='auto'  → kind=info shows busy, ok→green, warn→amber
  if (!statusTop || !statusTopText) return;
  let mode = topMode;
  if (mode === 'auto') {{
    if (kind === 'ok') mode = 'ok';
    else if (kind === 'warn') mode = 'warn';
    else if (!msg) mode = 'hide';
    else mode = 'busy';
  }}
  if (mode === 'hide' || !msg) {{
    statusTop.hidden = true;
    return;
  }}
  statusTop.hidden = false;
  statusTopText.textContent = msg;
  statusTop.dataset.kind = kind;
  statusTop.classList.toggle('is-busy', mode === 'busy');
  statusTop.classList.toggle('is-ok', mode === 'ok');
  statusTop.classList.toggle('is-warn', mode === 'warn');
}}
function setError(msg) {{
  if (msg) {{
    errorBox.hidden = false;
    errorBox.textContent = msg;
  }} else {{
    errorBox.hidden = true;
    errorBox.textContent = '';
  }}
}}

// ── Plan modal + lang switcher ────────────────────────────────────────────
function highlightLangButtons() {{
  langUaBtn.classList.toggle('is-active', currentResultLang === 'uk');
  langEnBtn.classList.toggle('is-active', currentResultLang === 'en');
}}

function openPlanModal() {{
  if (!planModal) return;
  planModal.hidden = false;
  highlightLangButtons();
}}
function closePlanModal() {{
  if (!planModal) return;
  planModal.hidden = true;
}}

function downloadPdf() {{
  // Browser-native print → "Save as PDF" works on every modern browser.
  // The render layer ships A4-print-friendly CSS (@page + @media print)
  // so the iframe content paginates cleanly without any extra deps.
  if (planSource == null) return;
  // Modal must be visible so iframe contentWindow is fully laid out and
  // print() picks up the right document.
  const wasHidden = planModal && planModal.hidden;
  if (wasHidden) openPlanModal();
  try {{
    resultFrame.contentWindow.focus();
    resultFrame.contentWindow.print();
  }} catch (e) {{
    setError('Print failed: ' + (e.message || e));
  }}
}}

async function switchResultLang(newLang) {{
  if (newLang === currentResultLang) return;
  if (planSource === 'example') {{
    // Pre-built case file: just swap the iframe src to the matching
    // language variant. UA at /cases/<id>.html, EN at /en/cases/<id>.html.
    if (!activeExampleCaseId) return;
    resultFrame.src = (newLang === 'en' ? '/en/cases/' : '/cases/') + activeExampleCaseId + '.html';
    currentResultLang = newLang;
    highlightLangButtons();
    return;
  }}
  if (!pyodide) return;
  // Disable buttons during re-render so user can't double-click
  langUaBtn.disabled = true;
  langEnBtn.disabled = true;
  try {{
    pyodide.globals.set('_target_lang', newLang);
    const html = await pyodide.runPythonAsync(`
if _oo_mode == 'diagnostic':
    html = render_diagnostic_brief_html(_oo_result, mdt=_oo_mdt, target_lang=_target_lang)
else:
    html = render_plan_html(_oo_result, mdt=_oo_mdt, target_lang=_target_lang)
html
`);
    resultFrame.removeAttribute('src');
    resultFrame.srcdoc = html;
    currentResultLang = newLang;
    highlightLangButtons();
  }} catch (e) {{
    setError('Re-render failed: ' + (e.message || e));
  }} finally {{
    langUaBtn.disabled = false;
    langEnBtn.disabled = false;
  }}
}}

function loadExamplePlan(caseId) {{
  // Show the pre-built case HTML for the just-loaded example so the user
  // sees a plan immediately — without spinning up Pyodide and without
  // pretending the engine just ran. Generate stays disabled until the
  // user edits something (which sets planDirty).
  if (!caseId) return;
  activeExampleCaseId = caseId;
  resultFrame.removeAttribute('srcdoc');
  resultFrame.src = (currentResultLang === 'en' ? '/en/cases/' : '/cases/') + caseId + '.html';
  planSource = 'example';
  planDirty = false;
  viewPlanBtn.disabled = false;
  pdfBtn.disabled = false;
  modalPdfBtn.disabled = false;
  openPlanModal();
}}

function clearPlanState() {{
  planSource = null;
  planDirty = false;
  activeExampleCaseId = null;
  resultFrame.removeAttribute('src');
  resultFrame.removeAttribute('srcdoc');
  viewPlanBtn.disabled = true;
  pdfBtn.disabled = true;
  modalPdfBtn.disabled = true;
  closePlanModal();
}}

pdfBtn.addEventListener('click', downloadPdf);
modalPdfBtn.addEventListener('click', downloadPdf);
viewPlanBtn.addEventListener('click', openPlanModal);
planModalClose.addEventListener('click', closePlanModal);
planModal.addEventListener('click', (ev) => {{
  if (ev.target === planModal) closePlanModal();
}});
document.addEventListener('keydown', (ev) => {{
  if (ev.key === 'Escape' && !planModal.hidden) closePlanModal();
}});
langUaBtn.addEventListener('click', () => switchResultLang('uk'));
langEnBtn.addEventListener('click', () => switchResultLang('en'));

function escHtml(s) {{
  return String(s).replace(/[&<>"']/g, c => ({{
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }})[c]);
}}

function saveDraft() {{
  try {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{
      questId: activeQuest ? activeQuest.id : null,
      answers,
      mode,
      jsonText: textarea.value,
    }}));
  }} catch (e) {{ /* private mode etc — silent fail */ }}
}}

function loadDraft() {{
  try {{
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  }} catch {{ return null; }}
}}

// ── Form rendering ────────────────────────────────────────────────────────
const IMPACT_LABEL = {{
  critical: 'CRITICAL',
  required: 'Required',
  recommended: 'Recommended',
  optional: 'Optional',
}};

// Decoupled from engine readiness — button is clickable as soon as
// there is something to send. The engine itself loads lazily on click
// (and also kicks off in the background after first interaction so the
// live impact panel can populate without waiting for a click).
//
// Disabled when a plan is already shown for the current input — either
// because the user just generated it, or because they loaded an example
// (which auto-displays the pre-built case HTML). Re-enables the moment
// the user edits any field (planDirty), so they can recompute.
function updateRunBtnEnabled() {{
  let hasInput = false;
  if (mode === 'form') hasInput = !!activeQuest;
  else hasInput = textarea.value.trim().length > 0;
  const planFresh = planSource !== null && !planDirty;
  runBtn.disabled = !hasInput || planFresh;
}}

// Mark the currently-shown plan as out-of-sync with the current input.
// Called from every input handler so the next click on Generate runs
// against the modified profile, not the cached/example plan.
function markPlanDirty() {{
  if (planSource !== null) {{
    planDirty = true;
    updateRunBtnEnabled();
  }}
}}

let engineKickoffStarted = false;
function kickoffEngineLoad() {{
  if (engineKickoffStarted) return;
  engineKickoffStarted = true;
  // Don't await — let it run in background so live preview can populate
  // as soon as it's ready. Errors surface via setError on real click.
  ensureEngine().catch(e => console.warn('engine bg load failed:', e));
}}

function hideExampleLockBanner() {{
  const banner = document.getElementById('exampleLockBanner');
  if (banner) banner.hidden = true;
}}
function showExampleLockBanner() {{
  const banner = document.getElementById('exampleLockBanner');
  if (banner) banner.hidden = false;
}}

function lockFilledFields() {{
  // Mark every form field that already has an answer as disabled and
  // tag its wrapper for visual distinction. Fields without a value stay
  // editable so the user can complete anything missing.
  const wrappers = formPane.querySelectorAll('.quest-q');
  wrappers.forEach(wrap => {{
    const field = wrap.dataset.field;
    if (!field) return;
    const inp = wrap.querySelector('input,select,textarea');
    if (!inp) return;
    if (answers[field] !== undefined && answers[field] !== null && answers[field] !== '') {{
      inp.disabled = true;
      wrap.classList.add('locked');
    }} else {{
      inp.disabled = false;
      wrap.classList.remove('locked');
    }}
  }});
}}

function unlockAllFields() {{
  formPane.querySelectorAll('.quest-q').forEach(wrap => {{
    wrap.classList.remove('locked');
    const inp = wrap.querySelector('input,select,textarea');
    if (inp) inp.disabled = false;
  }});
  hideExampleLockBanner();
}}

function renderForm(quest) {{
  activeQuest = quest;
  answers = {{}};
  questGroups.innerHTML = '';
  hideExampleLockBanner();
  if (!quest) {{
    questEmpty.style.display = '';
    questIntro.hidden = true;
    updateRunBtnEnabled();
    return;
  }}
  questEmpty.style.display = 'none';
  if (quest.intro) {{
    questIntro.hidden = false;
    questIntro.textContent = quest.intro;
  }} else {{
    questIntro.hidden = true;
  }}
  for (const group of quest.groups || []) {{
    const groupEl = document.createElement('div');
    groupEl.className = 'quest-group';
    groupEl.innerHTML = `
      <h3>${{escHtml(group.title || '')}}</h3>
      ${{group.description ? `<p class="quest-group-desc">${{escHtml(group.description)}}</p>` : ''}}
    `;
    for (const q of group.questions || []) {{
      groupEl.appendChild(renderQuestion(q));
    }}
    questGroups.appendChild(groupEl);
  }}
  updateRunBtnEnabled();
}}

function renderQuestion(q) {{
  const wrap = document.createElement('div');
  wrap.className = 'quest-q';
  wrap.dataset.field = q.field;
  const impact = q.impact || 'optional';
  wrap.dataset.impact = impact;
  const fieldId = 'fld-' + q.field.replace(/[^A-Za-z0-9]/g, '_');

  const triggers = (q.triggers || []).map(t => `<span class="trigger-pill">${{escHtml(t)}}</span>`).join('');

  let inputHtml = '';
  const placeholder = q.range_min !== undefined && q.range_max !== undefined
    ? `${{q.range_min}}–${{q.range_max}}` : '';
  switch (q.type) {{
    case 'integer':
    case 'float':
      inputHtml = `<input type="number" id="${{fieldId}}" data-field="${{q.field}}"
        ${{q.range_min !== undefined ? `min="${{q.range_min}}"` : ''}}
        ${{q.range_max !== undefined ? `max="${{q.range_max}}"` : ''}}
        ${{q.type === 'float' ? 'step="0.1"' : 'step="1"'}}
        ${{placeholder ? `placeholder="${{placeholder}}"` : ''}}>`;
      break;
    case 'boolean':
      inputHtml = `<select id="${{fieldId}}" data-field="${{q.field}}" data-type="boolean">
        <option value="">—</option>
        <option value="true">Так</option>
        <option value="false">Ні</option>
      </select>`;
      break;
    case 'enum':
      const opts = (q.options || []).map(o =>
        `<option value="${{escHtml(JSON.stringify(o.value))}}">${{escHtml(o.label)}}</option>`
      ).join('');
      inputHtml = `<select id="${{fieldId}}" data-field="${{q.field}}" data-type="enum">
        <option value="">— оберіть —</option>${{opts}}
      </select>`;
      break;
    case 'text':
    default:
      inputHtml = `<input type="text" id="${{fieldId}}" data-field="${{q.field}}">`;
  }}

  wrap.innerHTML = `
    <div class="quest-q-head">
      <label for="${{fieldId}}" class="quest-q-label">${{escHtml(q.label)}}</label>
      <span class="impact-pill impact-${{impact}}">${{IMPACT_LABEL[impact] || impact}}</span>
    </div>
    ${{inputHtml}}
    ${{q.units ? `<span class="quest-units">${{escHtml(q.units)}}</span>` : ''}}
    ${{q.helper ? `<p class="quest-helper">${{escHtml(q.helper)}}</p>` : ''}}
    ${{triggers ? `<div class="quest-triggers">${{triggers}}</div>` : ''}}
  `;

  // Apply default value
  const inp = wrap.querySelector('input,select');
  if (q.default_value !== undefined && q.default_value !== null) {{
    if (q.type === 'boolean') inp.value = String(q.default_value);
    else if (q.type === 'enum') inp.value = JSON.stringify(q.default_value);
    else inp.value = q.default_value;
    answers[q.field] = q.default_value;
  }}
  inp.addEventListener('input', onAnswerChange);
  inp.addEventListener('change', onAnswerChange);
  return wrap;
}}

function readValue(input, type) {{
  const v = input.value;
  if (v === '') return undefined;
  switch (type) {{
    case 'boolean': return v === 'true';
    case 'enum':
      try {{ return JSON.parse(v); }} catch {{ return v; }}
    case 'integer': return parseInt(v, 10);
    case 'float': return parseFloat(v);
    default: return v;
  }}
}}

function onAnswerChange(ev) {{
  const inp = ev.target;
  const field = inp.dataset.field;
  if (!field) return;
  const type = inp.dataset.type
    || (inp.type === 'number' ? (inp.step === '0.1' ? 'float' : 'integer') : 'text');
  const val = readValue(inp, type);
  if (val === undefined) delete answers[field];
  else answers[field] = val;
  markPlanDirty();
  saveDraft();
  updateRunBtnEnabled();
  updateImpactPanelLocal();
}}

function scheduleEval() {{
  if (evalDebounceTimer) clearTimeout(evalDebounceTimer);
  if (whatIfDebounceTimer) clearTimeout(whatIfDebounceTimer);
  evalDebounceTimer = setTimeout(runLivePreview, PREVIEW_DEBOUNCE_MS);
  whatIfDebounceTimer = setTimeout(triggerWhatIfFromState, WHATIF_DEBOUNCE_MS);
}}

function triggerWhatIfFromState() {{
  whatIfDebounceTimer = null;
  if (!enginReady || !activeQuest || generating || !lastPreviewResult) return;
  runWhatIf(lastPreviewResult).catch(e => console.warn('what-if eval error:', e));
}}

// Cancel any pending preview/what-if when user starts interacting with the
// toolbar (disease/example dropdown, mode buttons, reset). Bumps tokens so
// any in-flight Pyodide call's result is discarded the moment it lands.
// We can't interrupt a synchronous wasm call mid-flight, but this prevents
// new evals from starting while the user is choosing from a dropdown —
// which is when native <select> popup needs the main thread free.
function pauseEvalForToolbar() {{
  if (evalDebounceTimer) {{ clearTimeout(evalDebounceTimer); evalDebounceTimer = null; }}
  if (whatIfDebounceTimer) {{ clearTimeout(whatIfDebounceTimer); whatIfDebounceTimer = null; }}
  ++previewToken;
  ++whatIfToken;
}}

// ── Mode switch ───────────────────────────────────────────────────────────
function setMode(newMode) {{
  mode = newMode;
  modeFormBtn.classList.toggle('active', mode === 'form');
  modeJsonBtn.classList.toggle('active', mode === 'json');
  formPane.hidden = mode !== 'form';
  jsonPane.hidden = mode !== 'json';
  if (mode === 'json' && activeQuest) {{
    // Sync form → JSON
    textarea.value = JSON.stringify(buildProfile(), null, 2);
  }}
  saveDraft();
  updateRunBtnEnabled();
}}

// ── Profile assembly + live preview ───────────────────────────────────────
function buildProfile() {{
  if (mode === 'json') {{
    try {{ return JSON.parse(textarea.value); }} catch {{ return null; }}
  }}
  if (!activeQuest) return null;
  // Deep-merge fixed_fields + expand dotted-path answers
  const profile = JSON.parse(JSON.stringify(activeQuest.fixed_fields || {{}}));
  for (const [path, val] of Object.entries(answers)) {{
    if (val === undefined || val === null) continue;
    const parts = path.split('.');
    let cur = profile;
    for (let i = 0; i < parts.length - 1; i++) {{
      const seg = parts[i];
      if (typeof cur[seg] !== 'object' || cur[seg] === null) cur[seg] = {{}};
      cur = cur[seg];
    }}
    cur[parts[parts.length - 1]] = val;
  }}
  return profile;
}}

async function runLivePreview() {{
  const _ooT0 = performance.now();
  const myToken = ++previewToken;
  const profile = buildProfile();
  if (!profile || !activeQuest) {{
    updateImpactPanel(null);
    return;
  }}
  // Local-only progress before Pyodide ready
  const total = (activeQuest.groups || []).reduce(
    (acc, g) => acc + (g.questions || []).length, 0);
  const filled = Object.keys(answers).length;
  setProgress(filled, total);

  // Call evaluator if engine ready
  if (!enginReady) return;
  try {{
    pyodide.globals.set('_profile_json', JSON.stringify(profile));
    pyodide.globals.set('_quest_id', activeQuest.id);
    const resultJson = await pyodide.runPythonAsync(`
import json
from pathlib import Path
from knowledge_base.engine import evaluate_partial
from knowledge_base.validation.loader import load_content
profile = json.loads(_profile_json)
KB = Path('knowledge_base/hosted/content')
ld = load_content(KB)
quest = next((info['data'] for eid, info in ld.entities_by_id.items()
              if info['type'] == 'questionnaires' and info['data'].get('id') == _quest_id), None)
if quest is None:
    _preview_result = json.dumps({{'error': f'Questionnaire {{_quest_id}} not found'}})
else:
    _preview_eval = evaluate_partial(profile, quest, kb_root=KB)
    _payload = _preview_eval.to_dict()
    # P4: enrich fired_redflags with definition + sources so the live
    # impact panel can show meaningful context, not just IDs.
    _rf_lookup = {{
        info['data'].get('id'): info['data']
        for info in ld.entities_by_id.values()
        if info['type'] == 'redflags' and info['data'].get('id')
    }}
    _payload['fired_redflags_detail'] = [
        {{
            'id': rid,
            'definition_ua': (_rf_lookup.get(rid) or {{}}).get('definition_ua'),
            'definition': (_rf_lookup.get(rid) or {{}}).get('definition'),
            'clinical_direction': (_rf_lookup.get(rid) or {{}}).get('clinical_direction'),
            'severity': (_rf_lookup.get(rid) or {{}}).get('severity', 'major'),
            'sources': (_rf_lookup.get(rid) or {{}}).get('sources') or [],
        }}
        for rid in (_payload.get('fired_redflags') or [])
    ]
    _preview_result = json.dumps(_payload)
_preview_result
`);
    if (myToken !== previewToken) {{
      console.log(`[OO] preview ${{(performance.now() - _ooT0).toFixed(0)}}ms (stale, discarded)`);
      return;
    }}
    const result = JSON.parse(resultJson);
    if (result.error) {{
      setError(result.error);
      return;
    }}
    updateImpactPanel(result);
    lastPreviewResult = result;
    console.log(`[OO] preview ${{(performance.now() - _ooT0).toFixed(0)}}ms`);
    // What-if shadow evaluation runs from its own timer (WHATIF_DEBOUNCE_MS,
    // longer than preview) so rapid typing / dropdown interaction doesn't
    // trigger 10-30 sequential Pyodide evals that block the main thread and
    // make <select> popups laggy.
  }} catch (e) {{
    /* Don't spam errors during typing — just log */
    console.warn('preview eval error:', e);
  }}
}}

// ── What-if shadow evaluation ─────────────────────────────────────────────
let whatIfToken = 0;

async function runWhatIf(currentResult) {{
  if (!enginReady || !activeQuest || !currentResult) return;
  const _ooT0 = performance.now();
  const myToken = ++whatIfToken;

  const specs = [];
  for (const group of activeQuest.groups || []) {{
    for (const q of group.questions || []) {{
      if (q.impact !== 'critical' && q.impact !== 'required') continue;
      if (q.type !== 'boolean' && q.type !== 'enum') continue;
      const currentVal = answers[q.field];
      if (q.type === 'boolean') {{
        if (currentVal === true) specs.push({{field: q.field, alt_value: false, label: 'Ні'}});
        else if (currentVal === false) specs.push({{field: q.field, alt_value: true, label: 'Так'}});
        else {{
          specs.push({{field: q.field, alt_value: true, label: 'Так'}});
          specs.push({{field: q.field, alt_value: false, label: 'Ні'}});
        }}
      }} else if (q.type === 'enum') {{
        for (const opt of q.options || []) {{
          if (JSON.stringify(opt.value) === JSON.stringify(currentVal)) continue;
          specs.push({{field: q.field, alt_value: opt.value, label: opt.label}});
        }}
      }}
    }}
  }}

  if (specs.length === 0) {{ clearWhatIfMarks(); return; }}

  const profile = buildProfile();
  if (!profile) return;

  pyodide.globals.set('_wf_profile', JSON.stringify(profile));
  pyodide.globals.set('_wf_quest_id', activeQuest.id);
  pyodide.globals.set('_wf_specs', JSON.stringify(specs));
  pyodide.globals.set('_wf_main_ind', currentResult.would_select_indication || '');
  pyodide.globals.set('_wf_main_rfs', JSON.stringify(currentResult.fired_redflags || []));

  let raw;
  try {{
    raw = await pyodide.runPythonAsync(`
import json, copy
from pathlib import Path
from knowledge_base.engine import evaluate_partial
from knowledge_base.validation.loader import load_content
profile = json.loads(_wf_profile)
specs = json.loads(_wf_specs)
main_ind = _wf_main_ind
main_rfs = set(json.loads(_wf_main_rfs))
KB = Path('knowledge_base/hosted/content')
ld = load_content(KB)
quest = next((info['data'] for eid, info in ld.entities_by_id.items()
              if info['type'] == 'questionnaires' and info['data'].get('id') == _wf_quest_id), None)

def _set_path(d, dotted, val):
    parts = dotted.split('.')
    cur = d
    for p in parts[:-1]:
        if not isinstance(cur.get(p), dict):
            cur[p] = {{}}
        cur = cur[p]
    cur[parts[-1]] = val

results = []
if quest is not None:
    for spec in specs:
        sp = copy.deepcopy(profile)
        _set_path(sp, spec['field'], spec['alt_value'])
        try:
            sr = evaluate_partial(sp, quest, kb_root=KB, loaded_kb=ld).to_dict()
        except Exception:
            continue
        diff = {{}}
        si = sr.get('would_select_indication') or ''
        if si != main_ind:
            diff['indication_now'] = si
        srfs = set(sr.get('fired_redflags') or [])
        added = sorted(srfs - main_rfs)
        removed = sorted(main_rfs - srfs)
        if added: diff['rf_added'] = added
        if removed: diff['rf_removed'] = removed
        if diff:
            results.append({{
                'field': spec['field'],
                'alt_value': spec['alt_value'],
                'label': spec.get('label', ''),
                'diff': diff,
            }})
_wf_result_json = json.dumps(results)
_wf_result_json
`);
  }} catch (e) {{
    console.warn('what-if eval error:', e);
    return;
  }}

  if (myToken !== whatIfToken) {{
    console.log(`[OO] whatif ${{(performance.now() - _ooT0).toFixed(0)}}ms (stale, discarded)`);
    return;
  }}
  let results;
  try {{ results = JSON.parse(raw); }} catch {{ return; }}
  renderWhatIfMarks(results);
  console.log(`[OO] whatif ${{(performance.now() - _ooT0).toFixed(0)}}ms (${{specs.length}} specs, ${{results.length}} differing)`);
}}

function clearWhatIfMarks() {{
  formPane.querySelectorAll('.quest-whatif').forEach(n => n.remove());
}}

function renderWhatIfMarks(results) {{
  clearWhatIfMarks();
  const byField = {{}};
  for (const r of results) {{
    (byField[r.field] = byField[r.field] || []).push(r);
  }}
  for (const field of Object.keys(byField)) {{
    const wrap = formPane.querySelector(`.quest-q[data-field="${{CSS.escape(field)}}"]`);
    if (!wrap) continue;
    const box = document.createElement('div');
    box.className = 'quest-whatif';
    let html = '<div class="whatif-head">Якщо це поле буде іншим:</div><ul>';
    for (const it of byField[field]) {{
      const parts = [];
      if (it.diff.indication_now) {{
        parts.push(`Indication → <code>${{escHtml(it.diff.indication_now)}}</code>`);
      }}
      if (it.diff.rf_added && it.diff.rf_added.length) {{
        parts.push('<span class="wf-add">+RF</span> ' + it.diff.rf_added.map(r => `<code>${{escHtml(r)}}</code>`).join(' '));
      }}
      if (it.diff.rf_removed && it.diff.rf_removed.length) {{
        parts.push('<span class="wf-rm">−RF</span> ' + it.diff.rf_removed.map(r => `<code>${{escHtml(r)}}</code>`).join(' '));
      }}
      const altLabel = it.label || JSON.stringify(it.alt_value);
      html += `<li><span class="whatif-alt">${{escHtml(altLabel)}}:</span> ${{parts.join(' · ')}}</li>`;
    }}
    html += '</ul>';
    box.innerHTML = html;
    wrap.appendChild(box);
  }}
}}

// Local-only impact panel update — runs WITHOUT Pyodide so form interaction
// stays snappy. Computes progress + missing critical fields directly from
// the questionnaire schema. Engine-dependent sections (red flags, indication)
// show "click Generate" placeholders. Replaces the auto-fired runLivePreview
// path which was costing 4–5 s per keystroke once KB grew past ~30 diseases.
function updateImpactPanelLocal() {{
  if (!activeQuest) {{
    setProgress(0, 0);
    impactMissingCritical.querySelector('ul').innerHTML = '';
    impactRedflags.querySelector('ul').innerHTML =
      '<li class="muted">Натисни «Згенерувати», щоб побачити red flags</li>';
    impactSelectedText.innerHTML =
      '<span class="muted">— оберіть хворобу і заповніть форму —</span>';
    impactWarnings.hidden = true;
    return;
  }}
  let total = 0, filled = 0;
  const missing = [];
  for (const group of activeQuest.groups || []) {{
    for (const q of group.questions || []) {{
      total++;
      const val = answers[q.field];
      const isFilled = val !== undefined && val !== null && val !== '';
      if (isFilled) filled++;
      else if (q.impact === 'critical') {{
        missing.push({{ label: q.label, group: group.title || '' }});
      }}
    }}
  }}
  setProgress(filled, total);
  const ul = impactMissingCritical.querySelector('ul');
  ul.innerHTML = missing.length
    ? missing.map(m =>
        `<li><strong>${{escHtml(m.label)}}</strong> <span class="muted">(${{escHtml(m.group)}})</span></li>`
      ).join('')
    : '<li class="muted">Усі critical поля заповнені ✓</li>';
  impactRedflags.querySelector('ul').innerHTML =
    '<li class="muted">Натисни «Згенерувати», щоб побачити red flags</li>';
  impactSelectedText.innerHTML =
    '<span class="muted">Натисни «Згенерувати», щоб побачити рекомендований Indication</span>';
  impactWarnings.hidden = true;
}}

function setProgress(filled, total) {{
  progressText.textContent = `${{filled}} / ${{total}}`;
  const pct = total ? Math.round(filled * 100 / total) : 0;
  progressPct.textContent = `${{pct}}%`;
  progressFill.style.width = `${{pct}}%`;
}}

function updateImpactPanel(result) {{
  if (!result) {{
    impactMissingCritical.querySelector('ul').innerHTML = '';
    impactRedflags.querySelector('ul').innerHTML = '';
    impactSelectedText.textContent = '—';
    impactWarnings.hidden = true;
    return;
  }}
  setProgress(result.filled_count, result.total_questions);

  const miss = result.missing_critical || [];
  impactMissingCritical.querySelector('ul').innerHTML = miss.length
    ? miss.map(m => `<li><strong>${{escHtml(m.label)}}</strong> <span class="muted">(${{escHtml(m.group)}})</span></li>`).join('')
    : '<li class="muted">Усі critical поля заповнені ✓</li>';

  const rfs = result.fired_redflags || [];
  const rfDetail = result.fired_redflags_detail || [];
  // Build detail-keyed map so we can join id -> {{definition, sources}}
  const detailById = {{}};
  for (const d of rfDetail) detailById[d.id] = d;

  const dirEmoji = {{
    'hold': '🛑', 'intensify': '⚡', 'de-escalate': '🔻', 'investigate': '🔍'
  }};

  impactRedflags.querySelector('ul').innerHTML = rfs.length
    ? rfs.map(r => {{
        const d = detailById[r] || {{}};
        const defn = d.definition_ua || d.definition || '';
        const dir = d.clinical_direction || '';
        const emoji = dirEmoji[dir] || '';
        const sources = (d.sources || []).map(
          s => `<span class="rf-src-chip">${{escHtml(s)}}</span>`
        ).join('');
        return `<li class="rf-fired-item">
          <div class="rf-fired-head"><code>${{escHtml(r)}}</code> ${{emoji}}
            <span class="rf-dir rf-dir-${{escHtml(dir)}}">${{escHtml(dir)}}</span></div>
          ${{defn ? `<div class="rf-fired-defn">${{escHtml(defn)}}</div>` : ''}}
          ${{sources ? `<div class="rf-fired-srcs">${{sources}}</div>` : ''}}
        </li>`;
      }}).join('')
    : '<li class="muted">Жодного RedFlag поки не активовано</li>';

  impactSelectedText.innerHTML = result.would_select_indication
    ? `<code>${{escHtml(result.would_select_indication)}}</code>`
    : '— (бракує даних для вибору)';

  if ((result.warnings || []).length) {{
    impactWarnings.hidden = false;
    impactWarnings.querySelector('ul').innerHTML =
      result.warnings.map(w => `<li>${{escHtml(w)}}</li>`).join('');
  }} else {{
    impactWarnings.hidden = true;
  }}
  // ready_to_generate is advisory — don't block the button on it; the
  // user can still try to generate even with missing critical fields
  // and the engine will surface the gaps.
}}

// ── Bundle lazy-load (CSD-6E + CSD-9C) ────────────────────────────────────
// Two-tier bundle: fetch openonco-engine-core.zip first (~1.4 MB), then
// fetch the matching per-disease module (~15-40 KB) once we know the
// patient's disease_id. CSD-9C (2026-04-27) drops the legacy monolithic
// fallback — the lazy-load path is the canonical path now. The index
// fetch retries once on transient failure before giving up; if that
// fails too we surface a clear error rather than silently downloading
// 3+ MB of fallback that no longer ships.

async function loadBundleIndex() {{
  if (bundleIndex !== null) return bundleIndex;
  // One retry to absorb a transient CDN hiccup before failing the load.
  let lastErr = null;
  for (let attempt = 0; attempt < 2; attempt++) {{
    try {{
      const r = await fetch(BUNDLE_INDEX_URL + '?t=' + Date.now());
      if (!r.ok) throw new Error('Index fetch HTTP ' + r.status);
      bundleIndex = await r.json();
      return bundleIndex;
    }} catch (e) {{
      lastErr = e;
      if (attempt === 0) {{
        console.warn('[OpenOnco] bundle index fetch failed — retrying once:', e);
        await yieldToBrowser(250);
      }}
    }}
  }}
  console.error('[OpenOnco] bundle index unavailable after retry:', lastErr);
  throw new Error('Bundle index unavailable: ' + (lastErr && lastErr.message || lastErr));
}}

// Resolve a disease_id from whatever the patient profile / form gives us.
// Order: explicit disease.id (or top-level disease_id) → active
// questionnaire's disease_id → ICD-O-3 morphology → null.
function resolveDiseaseId(profile) {{
  if (!profile) return null;
  const d = profile.disease || {{}};
  if (typeof d.id === 'string' && d.id.startsWith('DIS-')) return d.id.toUpperCase();
  if (typeof profile.disease_id === 'string' && profile.disease_id.startsWith('DIS-')) {{
    return profile.disease_id.toUpperCase();
  }}
  if (activeQuest && typeof activeQuest.disease_id === 'string'
      && activeQuest.disease_id.startsWith('DIS-')) {{
    return activeQuest.disease_id.toUpperCase();
  }}
  const code = d.icd_o_3_morphology;
  if (code && bundleIndex && bundleIndex.icd_to_disease_id) {{
    const did = bundleIndex.icd_to_disease_id[String(code)];
    if (did) return did;
  }}
  return null;
}}

async function loadCoreBundle() {{
  if (coreBundleLoaded) return;
  // CSD-9C: index is required — monolithic fallback retired.
  await loadBundleIndex();
  if (!bundleIndex || !bundleIndex.core) {{
    throw new Error('Bundle index missing core entry — cannot load engine');
  }}
  setStatus('Завантажую ядро двигуна (~1.4 МБ)…');
  const ver = bundleIndex.core_version || '';
  const url = '/' + bundleIndex.core + (ver ? '?v=' + ver : '');
  const r = await fetch(url);
  if (!r.ok) throw new Error('Core bundle fetch HTTP ' + r.status);
  const buf = await r.arrayBuffer();
  await yieldToBrowser();
  pyodide.unpackArchive(buf, 'zip');
  coreBundleLoaded = true;
}}

// Per-disease module: tiny zip with the disease's indications, regimens,
// algorithms, redflags, and biomarker_actionability cells. Cached in
// localStorage keyed by disease_id + version so subsequent visits skip
// the fetch entirely. Quota is ~5-10 MB; we only cache one disease at a
// time per slot and drop silently on quota errors.
async function loadDiseaseModule(diseaseId) {{
  if (!diseaseId) return;
  if (loadedDiseases.has(diseaseId)) return;
  if (!bundleIndex || !bundleIndex.diseases) return;
  const relUrl = bundleIndex.diseases[diseaseId];
  if (!relUrl) {{
    // Disease has no per-disease bundle — its content is fully in core.
    loadedDiseases.add(diseaseId);
    return;
  }}
  const ver = (bundleIndex.disease_versions || {{}})[diseaseId] || '';
  const cacheKey = 'openonco-disease-' + diseaseId + '-' + ver;

  // localStorage cache hit: decode base64 → ArrayBuffer → unpack.
  try {{
    const cached = localStorage.getItem(cacheKey);
    if (cached) {{
      const bin = atob(cached);
      const u8 = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
      pyodide.unpackArchive(u8.buffer, 'zip');
      loadedDiseases.add(diseaseId);
      console.log('[OO] disease module ' + diseaseId + ' loaded from localStorage cache');
      return;
    }}
  }} catch (e) {{
    console.warn('[OpenOnco] disease cache read failed for ' + diseaseId + ':', e);
    try {{ localStorage.removeItem(cacheKey); }} catch (_) {{}}
  }}

  setStatus('Завантажую модуль ' + diseaseId + '…');
  const url = '/' + relUrl + (ver ? '?v=' + ver : '');
  const r = await fetch(url);
  if (!r.ok) throw new Error('Disease module fetch HTTP ' + r.status + ' for ' + diseaseId);
  const buf = await r.arrayBuffer();
  await yieldToBrowser();
  pyodide.unpackArchive(buf, 'zip');
  loadedDiseases.add(diseaseId);

  // Re-validate after merge so the next generate_plan() sees the new YAMLs.
  // apply_disease_module() drops the loader cache; cheap enough to run on
  // every disease swap.
  try {{
    await pyodide.runPythonAsync(
      "from knowledge_base.engine import apply_disease_module\n" +
      "from pathlib import Path\n" +
      "apply_disease_module(Path('knowledge_base/hosted/content'))\n"
    );
  }} catch (e) {{
    console.warn('[OpenOnco] apply_disease_module failed (continuing):', e);
  }}

  // Cache for next visit. Skip silently on quota or encoding errors.
  try {{
    let bin = '';
    const u8 = new Uint8Array(buf);
    const chunk = 0x8000;
    for (let i = 0; i < u8.length; i += chunk) {{
      bin += String.fromCharCode.apply(null, u8.subarray(i, i + chunk));
    }}
    localStorage.setItem(cacheKey, btoa(bin));
  }} catch (e) {{
    // Quota exceeded or encoding hiccup — just don't cache.
  }}
}}

// ── Pyodide loader ────────────────────────────────────────────────────────
// Lazy: runs only when user clicks Generate. Drives the init overlay's
// 4 setup stages (pyodide / pydeps / bundle / validate) with explicit
// yields between each so the browser can repaint and process input
// (F12, scroll, keyboard) instead of locking up for 10–20 s straight.
async function ensureEngine() {{
  if (enginReady) return pyodide;
  let stage = null;
  try {{
    stage = 'pyodide';
    initStageStart(stage);
    setStatus('Завантажую Pyodide…');
    await yieldToBrowser(50);
    pyodide = await loadPyodide({{indexURL: "https://cdn.jsdelivr.net/pyodide/v{_PYODIDE_VERSION}/full/"}});
    initStageDone(stage);

    stage = 'pydeps';
    initStageStart(stage);
    setStatus('Встановлюю pydantic + pyyaml…');
    await yieldToBrowser(50);
    await pyodide.loadPackage(['micropip']);
    await yieldToBrowser();
    await pyodide.runPythonAsync(`
import micropip
await micropip.install(['pydantic', 'pyyaml'])
`);
    initStageDone(stage);

    stage = 'bundle';
    initStageStart(stage);
    setStatus('Завантажую двигун OpenOnco…');
    await yieldToBrowser(50);
    // CSD-6E + CSD-9C: lazy-load core bundle (~1.4 MB). Monolithic
    // fallback retired (CSD-9C 2026-04-27) — the index + core + per-
    // disease modules are the only path. Per-disease modules are
    // fetched later in runEngine() once disease_id is known.
    await loadCoreBundle();
    initStageDone(stage);

    stage = 'validate';
    initStageStart(stage);
    setStatus('Перевіряю базу…');
    await yieldToBrowser(50);
    const validationSummary = await pyodide.runPythonAsync(`
from pathlib import Path
from knowledge_base.validation.loader import load_content
_r = load_content(Path('knowledge_base/hosted/content'))
if _r.ok:
    _summary = "ok"
else:
    _parts = []
    if _r.schema_errors:
        _parts.append(f"schema({{len(_r.schema_errors)}}): " + "; ".join(f"{{p.name}}: {{m}}" for p, m in _r.schema_errors[:3]))
    if _r.ref_errors:
        _parts.append(f"ref({{len(_r.ref_errors)}}): " + "; ".join(f"{{p.name}}: {{m}}" for p, m in _r.ref_errors[:3]))
    if _r.contract_errors:
        _parts.append(f"contract({{len(_r.contract_errors)}}): " + "; ".join(f"{{p.name}}: {{m}}" for p, m in _r.contract_errors[:3]))
    _summary = " | ".join(_parts)
_summary
`);
    initStageDone(stage);
    enginReady = true;
    if (validationSummary === 'ok') {{
      setStatus('Двигун готовий ✓', 'ok');
    }} else {{
      console.warn('[OpenOnco] KB validation did not pass — engine loaded anyway for testing.\\n' + validationSummary);
      setStatus('Двигун готовий ⚠ KB неверифіковано (деталі в консолі)', 'warn');
    }}
    return pyodide;
  }} catch (e) {{
    if (stage) initStageError(stage, e && e.message);
    throw e;
  }}
}}

// ── Generate full plan ────────────────────────────────────────────────────
async function runEngine() {{
  if (generating) return;  // double-click / re-entry guard
  const _ooT0 = performance.now();
  setError(null);
  const profile = buildProfile();
  if (!profile) {{
    setError('Не вдалося зібрати профіль (форма / JSON порожні).');
    return;
  }}

  // Lock the form so input during generation can't desync the rendered
  // plan from a moving profile. <main inert> hard-blocks pointer + keyboard
  // focus; init overlay (sibling of <main>) explains what's happening.
  generating = true;
  if (mainTryEl) mainTryEl.inert = true;
  if (evalDebounceTimer) {{ clearTimeout(evalDebounceTimer); evalDebounceTimer = null; }}
  if (whatIfDebounceTimer) {{ clearTimeout(whatIfDebounceTimer); whatIfDebounceTimer = null; }}
  ++previewToken;
  ++whatIfToken;
  initStagesReset();
  // If engine is already loaded from a prior click, fast-forward setup
  // stages so the doctor sees only "Будую план" active. First run lights
  // up all 5 stages.
  if (enginReady) {{
    initStageDone('pyodide');
    initStageDone('pydeps');
    initStageDone('bundle');
    initStageDone('validate');
  }}
  initShow();

  try {{
    try {{
      await ensureEngine();
    }} catch (e) {{
      setError('Двигун не завантажився: ' + (e.message || e));
      setStatus('');
      return;
    }}
    // CSD-6E: lazy-fetch the per-disease module before generate. No-op
    // when the disease has no per-disease bundle (its content is in
    // core). Failures are surfaced but non-fatal — generate_plan()
    // will fall back to whatever's already loaded.
    try {{
      const did = resolveDiseaseId(profile);
      if (did) await loadDiseaseModule(did);
    }} catch (e) {{
      console.warn('[OpenOnco] disease module load failed (continuing):', e);
    }}
    initStageStart('generate');
    setStatus('Будую персональний план…');
    await yieldToBrowser(30);
    const _ooTPython = performance.now();
    try {{
      pyodide.globals.set('_patient_json', JSON.stringify(profile));
      pyodide.globals.set('_target_lang', currentResultLang);
      const html = await pyodide.runPythonAsync(`
import json
from pathlib import Path
from knowledge_base.engine import (
    generate_plan, generate_diagnostic_brief, is_diagnostic_profile,
    orchestrate_mdt, render_plan_html, render_diagnostic_brief_html,
)
patient = json.loads(_patient_json)
KB = Path('knowledge_base/hosted/content')
if is_diagnostic_profile(patient):
    _oo_result = generate_diagnostic_brief(patient, kb_root=KB)
    _oo_mdt = orchestrate_mdt(patient, _oo_result, kb_root=KB)
    _oo_mode = 'diagnostic'
    html = render_diagnostic_brief_html(_oo_result, mdt=_oo_mdt, target_lang=_target_lang)
else:
    # Pyodide can't reach api.clinicaltrials.gov directly — pass the
    # baked cache_root only (no search_fn). Cache hits surface trials;
    # misses fall through to the "search not configured" empty bundle.
    _oo_result = generate_plan(
        patient, kb_root=KB, experimental_cache_root=KB / 'cache' / 'ctgov',
    )
    _oo_mdt = orchestrate_mdt(patient, _oo_result, kb_root=KB)
    _oo_mode = 'treatment'
    html = render_plan_html(_oo_result, mdt=_oo_mdt, target_lang=_target_lang)
html
`);
      initStageDone('generate');
      resultFrame.removeAttribute('src');
      resultFrame.srcdoc = html;
      planSource = 'generated';
      planDirty = false;
      activeExampleCaseId = null;
      viewPlanBtn.disabled = false;
      pdfBtn.disabled = false;
      modalPdfBtn.disabled = false;
      openPlanModal();
      setStatus('Plan готовий ✓', 'ok');
      const _ooTNow = performance.now();
      console.log(`[OO] generate ${{(_ooTNow - _ooT0).toFixed(0)}}ms total (engine-load ${{(_ooTPython - _ooT0).toFixed(0)}}ms + python ${{(_ooTNow - _ooTPython).toFixed(0)}}ms)`);
    }} catch (e) {{
      initStageError('generate', e && e.message);
      setError('Двигун повернув помилку:\\n' + (e.message || e));
      setStatus('');
    }}
  }} finally {{
    generating = false;
    if (mainTryEl) mainTryEl.inert = false;
    // Brief delay so the doctor sees green checkmarks before the overlay
    // fades — purely cosmetic confirmation that all stages succeeded.
    setTimeout(initHide, 600);
    updateRunBtnEnabled();
  }}
}}

function setGeneratingUI(on, hint) {{
  generatingOverlay.hidden = !on;
  // <main inert> hard-blocks pointer + keyboard focus on every interactive
  // element inside (form fields, toolbar, runBtn). The overlay is a sibling
  // of <main>, so it stays interactive — but we don't currently put any
  // controls in it (no cancel — Pyodide runPythonAsync is not interruptable).
  if (mainTryEl) mainTryEl.inert = on;
  if (on && hint) setGeneratingHint(hint);
}}

function setGeneratingHint(text) {{
  if (generatingHint) generatingHint.textContent = text;
}}

// ── Init overlay (one-time engine load with named stages) ─────────────────
// Shown on first Generate click; doctor sees what's happening instead of a
// mystery lag. Yields to the browser between stages so F12, scrolling, and
// keyboard input remain responsive even though wasm chunks block the main
// thread internally.
function initShow() {{ if (initOverlay) initOverlay.hidden = false; }}
function initHide() {{ if (initOverlay) initOverlay.hidden = true; }}

function initStageStart(id) {{
  if (!initStagesEl) return;
  const li = initStagesEl.querySelector(`[data-stage="${{id}}"]`);
  if (!li) return;
  li.classList.remove('pending', 'done', 'error');
  li.classList.add('active');
}}
function initStageDone(id) {{
  if (!initStagesEl) return;
  const li = initStagesEl.querySelector(`[data-stage="${{id}}"]`);
  if (!li) return;
  li.classList.remove('pending', 'active', 'error');
  li.classList.add('done');
}}
function initStageError(id, msg) {{
  if (!initStagesEl) return;
  const li = initStagesEl.querySelector(`[data-stage="${{id}}"]`);
  if (!li) return;
  li.classList.remove('pending', 'active', 'done');
  li.classList.add('error');
  if (msg) li.title = String(msg);
}}
function initStagesReset() {{
  if (!initStagesEl) return;
  initStagesEl.querySelectorAll('.stage').forEach(li => {{
    li.classList.remove('active', 'done', 'error');
    li.classList.add('pending');
  }});
}}

// Yield to the browser so it can repaint + process input between heavy
// synchronous wasm chunks (Pyodide loadPackage / unpackArchive / Python
// eval). 16ms ≈ one frame; 50ms gives visibly snappier dropdowns.
function yieldToBrowser(ms) {{
  return new Promise(resolve => setTimeout(resolve, ms == null ? 16 : ms));
}}

// ── Boot ──────────────────────────────────────────────────────────────────
//
// Lazy-loaders for full questionnaire/example data. Dropdowns populate
// instantly from the build-time manifests above; the full ~870 KB payload
// is fetched only after the user picks something.
async function ensureQuestionnaires() {{
  if (questionnaires) return questionnaires;
  if (!_questionnairesPromise) {{
    _questionnairesPromise = fetch('/questionnaires.json')
      .then(r => r.json())
      .then(data => {{ questionnaires = data; return data; }});
  }}
  return _questionnairesPromise;
}}
async function ensureExamples() {{
  if (examples) return examples;
  if (!_examplesPromise) {{
    _examplesPromise = fetch('/examples.json')
      .then(r => r.json())
      .then(data => {{ examples = data; return data; }});
  }}
  return _examplesPromise;
}}

async function loadAssets() {{
  // Populate dropdowns from manifests — instant, no network fetch.
  diseaseSelect.innerHTML = '<option value="">— оберіть —</option>';
  QUESTIONNAIRES_MANIFEST.forEach((q, i) => {{
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = q.title;
    diseaseSelect.appendChild(opt);
  }});

  // Examples selector — initial population shows all; narrows once a
  // disease is picked.
  repopulateExamples(null);

  // Restore draft
  const draft = loadDraft();
  if (draft && draft.questId) {{
    const idx = QUESTIONNAIRES_MANIFEST.findIndex(q => q.id === draft.questId);
    if (idx >= 0) {{
      diseaseSelect.value = idx;
      // Draft restore needs full data — lazy-fetch now
      const fullList = await ensureQuestionnaires();
      renderForm(fullList[idx]);
      repopulateExamples(idx);
      // Apply saved answers
      if (draft.answers) {{
        for (const [field, val] of Object.entries(draft.answers)) {{
          const inp = formPane.querySelector(`[data-field="${{CSS.escape(field)}}"]`);
          if (!inp) continue;
          if (typeof val === 'boolean') inp.value = String(val);
          else if (inp.dataset.type === 'enum') inp.value = JSON.stringify(val);
          else inp.value = val;
          answers[field] = val;
        }}
      }}
      if (draft.jsonText) textarea.value = draft.jsonText;
      if (draft.mode === 'json') setMode('json');
      setStatus('Чернетку відновлено ✓ Натисни «Згенерувати» коли готовий.', 'ok');
      updateRunBtnEnabled();
      updateImpactPanelLocal();
    }}
  }} else {{
    // Initial load done — hide the top busy banner; sidebar still shows hint.
    setStatus('Оберіть хворобу зі списку, щоб почати.', 'info', 'hide');
    updateRunBtnEnabled();
    updateImpactPanelLocal();
  }}

  // Engine is fully lazy now — Pyodide loads only when the user clicks
  // «Згенерувати». Form interaction stays Pyodide-free and snappy.
}}

// ── Examples filtering by selected disease ────────────────────────────────
// We narrow the example dropdown to those whose disease.icd_o_3_morphology
// matches the active questionnaire — otherwise the picker overwhelms with
// 35 cases for which we don't have a form.
function repopulateExamples(activeQuestIdx) {{
  // Filter from manifest only — no need to await full examples payload
  // just to populate a dropdown (manifest carries label + disease_icd).
  const wantCode = activeQuestIdx == null
    ? null
    : (QUESTIONNAIRES_MANIFEST[activeQuestIdx] || {{}}).disease_icd;
  exampleSelect.innerHTML = '';
  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = wantCode == null
    ? '— оберіть приклад —'
    : '— оберіть приклад для цієї хвороби —';
  exampleSelect.appendChild(placeholder);
  let n = 0;
  EXAMPLES_MANIFEST.forEach((ex, i) => {{
    if (wantCode != null) {{
      if (ex.disease_icd !== wantCode) return;
    }}
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = ex.label;
    exampleSelect.appendChild(opt);
    n++;
  }});
  if (wantCode != null && n === 0) {{
    const noneOpt = document.createElement('option');
    noneOpt.value = '';
    noneOpt.disabled = true;
    noneOpt.textContent = '(прикладів для цієї хвороби поки немає)';
    exampleSelect.appendChild(noneOpt);
  }}
}}

// ── Event wiring ──────────────────────────────────────────────────────────
diseaseSelect.addEventListener('change', async () => {{
  const i = diseaseSelect.value;
  // Switching disease invalidates whatever plan was on screen — there is
  // no longer any example or generated plan that matches the new form.
  clearPlanState();
  if (i === '') {{
    renderForm(null);
    repopulateExamples(null);
    updateRunBtnEnabled();
    return;
  }}
  const idx = parseInt(i, 10);
  const fullList = await ensureQuestionnaires();
  renderForm(fullList[idx]);
  repopulateExamples(idx);
  exampleSelect.value = '';
  saveDraft();
  updateRunBtnEnabled();
  updateImpactPanelLocal();
}});

function findQuestionnaireForProfile(profile) {{
  // Match by ICD-O-3 morphology — manifest carries disease_icd, no need
  // to wait for full questionnaires payload.
  const code = profile && profile.disease && profile.disease.icd_o_3_morphology;
  if (!code) return -1;
  return QUESTIONNAIRES_MANIFEST.findIndex(q => q.disease_icd === code);
}}

function getByPath(obj, dotted) {{
  let cur = obj;
  for (const seg of dotted.split('.')) {{
    if (cur === null || typeof cur !== 'object') return undefined;
    cur = cur[seg];
  }}
  return cur;
}}

function populateFormFromProfile(quest, profile) {{
  // Walk every form question and try to read its dotted-path value
  // out of the example profile. Unset inputs stay empty (will count as
  // not-filled so user can finish anything missing).
  for (const group of quest.groups || []) {{
    for (const q of group.questions || []) {{
      const path = q.field;
      if (!path) continue;
      const val = getByPath(profile, path);
      if (val === undefined || val === null) continue;
      const inp = formPane.querySelector(`[data-field="${{CSS.escape(path)}}"]`);
      if (!inp) continue;
      if (q.type === 'boolean') inp.value = String(val);
      else if (q.type === 'enum') inp.value = JSON.stringify(val);
      else inp.value = val;
      answers[path] = val;
    }}
  }}
}}

exampleSelect.addEventListener('change', async () => {{
  const i = exampleSelect.value;
  if (i === '') return;
  const fullExamples = await ensureExamples();
  const ex = fullExamples[parseInt(i, 10)];
  setError(null);
  // Prefer form mode: find a questionnaire that matches this example's
  // disease and populate it. Fall back to JSON view only when no
  // matching questionnaire exists (most diseases don't have one yet).
  const qIdx = findQuestionnaireForProfile(ex.json);
  if (qIdx >= 0) {{
    diseaseSelect.value = qIdx;
    const fullList = await ensureQuestionnaires();
    renderForm(fullList[qIdx]);
    repopulateExamples(qIdx);
    exampleSelect.value = i;
    populateFormFromProfile(fullList[qIdx], ex.json);
    setMode('form');
    // Lock filled fields and reveal the personalize banner so the user
    // can opt-in to editing the example's data.
    lockFilledFields();
    showExampleLockBanner();
    // Keep the JSON mirror in sync so toggling to JSON shows the loaded data
    textarea.value = JSON.stringify(buildProfile(), null, 2);
    // Show the pre-built case plan in the modal — the example IS already
    // a generated plan, so we display it directly instead of pretending
    // Generate would do new work.
    loadExamplePlan(ex.case_id);
    setStatus('{'Example loaded ✓ Plan shown — edit any field to generate your own.' if target_lang == 'en' else 'Приклад завантажено ✓ План показано — зміни поле, щоб згенерувати власний.'}', 'ok');
  }} else {{
    setMode('json');
    textarea.value = JSON.stringify(ex.json, null, 2);
    // No questionnaire match: still show the prebuilt plan if a case file
    // exists for this example.
    if (ex.case_id) loadExamplePlan(ex.case_id);
    setStatus('Приклад завантажено як JSON (ще немає опитувальника для цієї хвороби)', 'ok');
  }}
  saveDraft();
  updateRunBtnEnabled();
  updateImpactPanelLocal();
}});

const personalizeBtn = document.getElementById('personalizeBtn');
personalizeBtn && personalizeBtn.addEventListener('click', () => {{
  unlockAllFields();
  setStatus('Поля розблоковано — редагуй що завгодно. Натисни «Згенерувати» коли готовий.', 'ok');
}});

modeFormBtn.addEventListener('click', () => setMode('form'));
modeJsonBtn.addEventListener('click', () => setMode('json'));
formatBtn && formatBtn.addEventListener('click', () => {{
  setError(null);
  try {{ textarea.value = JSON.stringify(JSON.parse(textarea.value), null, 2); }}
  catch (e) {{ setError('Невалідний JSON: ' + e.message); }}
}});
textarea.addEventListener('input', () => {{
  markPlanDirty();
  saveDraft();
  updateRunBtnEnabled();
  // No live preview from JSON — engine runs only on Generate click.
}});

resetBtn.addEventListener('click', () => {{
  if (!confirm('Очистити форму і прибрати чернетку?')) return;
  answers = {{}};
  textarea.value = '';
  diseaseSelect.value = '';
  renderForm(null);
  clearPlanState();
  localStorage.removeItem(STORAGE_KEY);
  updateImpactPanelLocal();
  updateRunBtnEnabled();
  setStatus('Очищено.');
}});

runBtn.addEventListener('click', runEngine);

// Pause pending evals the moment the user reaches for a toolbar control —
// fires before the native <select> popup opens, so the main thread is free
// to render it. Covers both dropdowns + mode/reset buttons.
[diseaseSelect, exampleSelect, modeFormBtn, modeJsonBtn, resetBtn].forEach(el => {{
  if (!el) return;
  el.addEventListener('mousedown', pauseEvalForToolbar);
  el.addEventListener('focus', pauseEvalForToolbar);
}});

// ── Case-token URL handler (CSD-3-qr-token) ───────────────────────────────
// QR codes printed on CSD Lab NGS reports encode the patient profile in the
// URL hash: openonco.info/try.html#p=<base64-gzip-json>. We decode entirely
// in the browser — CHARTER §9.3, no PHI ever touches a server.
async function loadFromUrlHash() {{
  const hash = window.location.hash.slice(1);  // strip #
  if (!hash) return;
  const params = new URLSearchParams(hash);
  const token = params.get('p');
  if (!token) return;

  try {{
    // urlsafe-base64 → bytes (re-add padding) → gunzip → JSON
    const padded = token + '='.repeat((-token.length) & 3);
    const binStr = atob(padded.replace(/-/g, '+').replace(/_/g, '/'));
    const bytes = Uint8Array.from(binStr, c => c.charCodeAt(0));
    const ds = new DecompressionStream('gzip');
    const stream = new Response(bytes).body.pipeThrough(ds);
    const json = await new Response(stream).text();
    const patient = JSON.parse(json);

    // Try to match a disease questionnaire so the form mode picks up the
    // profile cleanly — same flow as the example loader.
    const qIdx = findQuestionnaireForProfile(patient);
    if (qIdx >= 0) {{
      diseaseSelect.value = qIdx;
      const fullList = await ensureQuestionnaires();
      renderForm(fullList[qIdx]);
      repopulateExamples(qIdx);
      populateFormFromProfile(fullList[qIdx], patient);
      setMode('form');
      lockFilledFields();
      showExampleLockBanner();
      textarea.value = JSON.stringify(buildProfile(), null, 2);
    }} else {{
      setMode('json');
      textarea.value = JSON.stringify(patient, null, 2);
    }}
    saveDraft();
    updateRunBtnEnabled();
    updateImpactPanelLocal();

    const banner = document.createElement('div');
    banner.className = 'case-token-banner';
    banner.textContent = '✓ Профіль завантажено з QR-коду. Натисніть «Згенерувати», щоб побудувати план, або відредагуйте поля.';
    mainTryEl.parentNode.insertBefore(banner, mainTryEl);
    setStatus('Профіль із QR завантажено ✓', 'ok');
  }} catch (err) {{
    console.error('Failed to decode case token:', err);
    const banner = document.createElement('div');
    banner.className = 'case-token-banner-error';
    banner.textContent = '⚠ Не вдалося завантажити профіль із QR-коду. Введіть JSON вручну або оберіть приклад.';
    mainTryEl.parentNode.insertBefore(banner, mainTryEl);
    setError('QR token decode failed: ' + (err.message || err));
  }}
}}

// Run after loadAssets so questionnaires + examples are populated and
// findQuestionnaireForProfile/populateFormFromProfile can do their job.
loadAssets()
  .then(() => loadFromUrlHash())
  .catch(e => setError('Initialization failed: ' + e));
window.addEventListener('hashchange', loadFromUrlHash);

// CSD-6E: kick off the bundle index fetch as soon as the page loads —
// it's tiny (~5 KB) and lets resolveDiseaseId() pre-resolve from
// ICD-O-3 codes before the user clicks Generate. Best-effort, never
// blocks UI.
loadBundleIndex().catch(() => {{}});

// CSD-6E polish: register the cache-first service worker so repeat
// visits skip the network for the engine bundle entirely. Best-effort
// — falls through silently when the SW API is unavailable (private
// mode, ITP, file://, etc.).
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('/sw.js').catch((e) => {{
      console.warn('[OpenOnco] service worker registration failed:', e);
    }});
  }});
}}
</script>
</body>
</html>
"""


# ── Per-case page (back-link banner, no auth gate) ────────────────────────


def _wrap_case_html(rendered_html: str, case: CaseEntry,
                    *, target_lang: str = "uk") -> str:
    """Insert a thin sticky bar with back-link + per-case feedback + lang
    switcher into the rendered Plan/Brief HTML. No auth gate — landing
    is fully public."""
    bar_style = (
        '<style>'
        '.case-bar{position:sticky;top:0;z-index:99;background:#0a2e1a;'
        'color:#dcfce7;padding:10px 24px;display:flex;justify-content:space-between;'
        'align-items:center;font-family:Source Sans 3,sans-serif;font-size:13px;}'
        '.case-bar a{color:#86efac;text-decoration:none;margin-left:14px;}'
        '.case-bar a:hover{text-decoration:underline;}'
        '.case-bar .lang-mini{font-family:JetBrains Mono,monospace;font-size:10px;'
        'background:rgba(255,255,255,.1);padding:3px 7px;border-radius:3px;'
        'margin-left:14px;letter-spacing:.5px;display:inline-flex;align-items:center;gap:5px;}'
        '.case-bar .lang-mini-current{font-family:JetBrains Mono,monospace;'
        'font-size:11px;background:rgba(255,255,255,.18);padding:3px 8px;'
        'border-radius:3px;letter-spacing:.5px;font-weight:600;'
        'display:inline-flex;align-items:center;gap:5px;}'
        '.case-bar .mini-flag{display:inline-block;width:14px;height:10px;'
        'border-radius:1.5px;vertical-align:middle;'
        'box-shadow:0 0 0 1px rgba(0,0,0,.25) inset;}'
        '.case-bar .mini-flag-ua{background:linear-gradient(to bottom,#0057b7 50%,#ffd500 50%);}'
        '.case-bar .mini-flag-en{background:#012169 '
        "url(\"data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 30' preserveAspectRatio='none'%3E%3Cpath d='M0,0 L60,30 M60,0 L0,30' stroke='%23fff' stroke-width='6'/%3E%3Cpath d='M0,0 L60,30 M60,0 L0,30' stroke='%23C8102E' stroke-width='2'/%3E%3Cpath d='M30,0 V30 M0,15 H60' stroke='%23fff' stroke-width='10'/%3E%3Cpath d='M30,0 V30 M0,15 H60' stroke='%23C8102E' stroke-width='6'/%3E%3C/svg%3E\") center/cover no-repeat;}"
        '@media print{.case-bar{display:none;}}'
        '</style>\n'
    )

    back_label = "← Back to gallery" if target_lang == "en" else "← Назад до галереї"
    feedback_label = "Feedback on this case" if target_lang == "en" else "Feedback на цей кейс"
    gallery_href = "/en/gallery.html" if target_lang == "en" else "/gallery.html"
    cur_flag_cls = "mini-flag-ua" if target_lang == "uk" else "mini-flag-en"
    other_flag_cls = "mini-flag-en" if target_lang == "uk" else "mini-flag-ua"
    cur_lang_label = "UA" if target_lang == "uk" else "EN"
    other_lang_label = "EN" if target_lang == "uk" else "UA"
    other_lang_href = _lang_switch_href("case", target_lang, case.case_id)

    bar_html = (
        '<div class="case-bar no-print">'
        f'<div><span class="lang-mini-current" title="Active language">'
        f'<span class="mini-flag {cur_flag_cls}" aria-hidden="true"></span>{cur_lang_label}</span>'
        f' · OpenOnco · <strong>{case.label_ua}</strong></div>'
        '<div>'
        f'<a href="{gallery_href}">{back_label}</a>'
        f'<a href="{GH_NEW_ISSUE}?title=%5Bfeedback%5D+'
        f'{case.case_id}&labels=tester-feedback" target="_blank" rel="noopener">'
        f'{feedback_label}</a>'
        f'<a class="lang-mini" href="{other_lang_href}" title="Switch to {other_lang_label}">'
        f'<span class="mini-flag {other_flag_cls}" aria-hidden="true"></span>{other_lang_label}</a>'
        '</div>'
        '</div>\n'
    )

    out = rendered_html.replace("</head>", bar_style + "</head>", 1)
    out = out.replace('<div class="page">', bar_html + '<div class="page">', 1)
    return out


# ── Static stylesheet ─────────────────────────────────────────────────────




# ── Capabilities page ─────────────────────────────────────────────────────


# Capabilities / Limitations pages need a heme-vs-solid split and a 1L /
# 2L+ split. We compute these on demand here (rather than extending
# `Stats`) by re-reading the relevant YAML directories. Cheap — small KB.
def _coverage_breakdown() -> dict:
    import yaml as _yaml
    from pathlib import Path as _Path

    base = _Path(__file__).resolve().parent.parent / "knowledge_base" / "hosted" / "content"

    def _load_dir(name):
        d = base / name
        if not d.exists():
            return []
        out = []
        for p in sorted(d.glob("*.yaml")):
            try:
                with p.open(encoding="utf-8") as fh:
                    obj = _yaml.safe_load(fh)
                if isinstance(obj, dict):
                    out.append(obj)
            except Exception:
                pass
        return out

    diseases = _load_dir("diseases")
    algorithms = _load_dir("algorithms")
    indications = _load_dir("indications")

    heme_ids: set[str] = set()
    solid_ids: set[str] = set()
    short_by_id: dict[str, str] = {}
    for d in diseases:
        d_id = d.get("id") or ""
        lin = (d.get("lineage") or "").lower()
        short_by_id[d_id] = d_id.replace("DIS-", "")
        if (
            "b_cell" in lin or "t_cell" in lin or "plasma" in lin
            or "myeloid" in lin or "lymph" in lin or "mpn" in lin
            or "leuk" in lin or "mds" in lin
            or lin in {"hodgkin", "myeloma"}
        ):
            heme_ids.add(d_id)
        elif lin:
            solid_ids.add(d_id)

    algos_1l = algos_2l = 0
    diseases_with_2l: set[str] = set()
    for a in algorithms:
        try:
            lot = int(a.get("applicable_to_line_of_therapy"))
        except (TypeError, ValueError):
            continue
        if lot == 1:
            algos_1l += 1
        elif lot >= 2:
            algos_2l += 1
            d_id = a.get("applicable_to_disease")
            if d_id:
                diseases_with_2l.add(d_id)

    inds_1l = inds_2l = 0
    for ind in indications:
        try:
            lot = int((ind.get("applicable_to") or {}).get("line_of_therapy"))
        except (TypeError, ValueError):
            continue
        if lot == 1:
            inds_1l += 1
        elif lot >= 2:
            inds_2l += 1

    diseases_2l_heme_list = ", ".join(
        sorted(short_by_id.get(d, d) for d in diseases_with_2l & heme_ids)
    )
    diseases_2l_solid_list = ", ".join(
        sorted(short_by_id.get(d, d) for d in diseases_with_2l & solid_ids)
    ) or "—"
    solid_disease_list = ", ".join(
        sorted(short_by_id.get(d, d) for d in solid_ids)
    )

    return {
        "heme_diseases": len(heme_ids),
        "solid_diseases": len(solid_ids),
        "algorithms_1l": algos_1l,
        "algorithms_2l_plus": algos_2l,
        "diseases_with_2l_plus": len(diseases_with_2l),
        "diseases_with_2l_plus_heme": len(diseases_with_2l & heme_ids),
        "diseases_with_2l_plus_solid": len(diseases_with_2l & solid_ids),
        "diseases_2l_heme_list": diseases_2l_heme_list,
        "diseases_2l_solid_list": diseases_2l_solid_list,
        "solid_disease_list": solid_disease_list,
        "indications_1l": inds_1l,
        "indications_2l_plus": inds_2l,
    }


def render_capabilities(stats, *, target_lang: str = "uk") -> str:
    if target_lang == "en":
        return _render_capabilities_en(stats)
    return _render_capabilities_uk(stats)


def _render_capabilities_uk(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_regimens = by_type.get("regimens", 0)
    n_tests = by_type.get("tests", 0)
    n_redflags = by_type.get("redflags", 0)
    n_workups = by_type.get("workups", 0)
    n_sources = by_type.get("sources", 0)
    n_drugs = by_type.get("drugs", 0)
    n_skills = stats.skills_planned_roles
    cov = _coverage_breakdown()
    n_heme = cov["heme_diseases"]
    n_solid = cov["solid_diseases"]
    n_algos_1l = cov["algorithms_1l"]
    n_algos_2l = cov["algorithms_2l_plus"]
    n_inds_1l = cov["indications_1l"]
    n_inds_2l = cov["indications_2l_plus"]
    n_dis_2l = cov["diseases_with_2l_plus"]
    n_dis_2l_heme = cov["diseases_with_2l_plus_heme"]
    n_dis_2l_solid = cov["diseases_with_2l_plus_solid"]

    # Live KB metric (moved here from landing). Per-disease coverage is
    # computed once and re-used in the cards block below.
    diseases_full = sum(
        1 for d in stats.diseases
        if d.coverage_status in {"stub_full_chain", "reviewed"}
    )
    diseases_partial = sum(1 for d in stats.diseases if d.coverage_status == "partial")

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Можливості</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="capabilities", target_lang="uk", lang_switch_href=_lang_switch_href("capabilities", "uk"))}

<main>
  <section class="info-page">
    <h1>Можливості</h1>
    <p class="lead">
      OpenOnco приймає JSON-профіль пацієнта і повертає структурований план
      лікування або діагностичний brief, з повним trace кожного рішення і
      цитуваннями всіх джерел. Жодного «чорного ящика»: усе рішення складається
      з декларативних правил, які можна прочитати у KB і відстежити в trace.
      Нижче — детально, як ми працюємо з даними, джерелами і запитами.
    </p>

    <div class="promo-info" role="img" aria-label="OpenOnco — інфографіка можливостей">
      <div class="promo-eyebrow">OpenOnco · v0.1 · engine у двох словах</div>
      <h2 class="promo-headline">
        Один JSON-профіль → <em>два альтернативні плани лікування</em>
        з цитатою під кожною рекомендацією.
      </h2>
      <p class="promo-sub">
        Декларативний rule engine на <strong>{n_diseases} хворобах</strong>,
        реферує <strong>{stats.corpus_references_total:,}+ публікацій</strong> під
        <strong>{n_sources} джерелами верхнього рівня</strong>. Без LLM у клінічному рішенні,
        без серверу, без логів. Patient JSON ніколи не покидає машину.
      </p>

      <div class="promo-stats">
        <div class="promo-stat">
          <div class="promo-stat-num">{n_diseases}</div>
          <div class="promo-stat-lbl">Хвороб у KB</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{stats.corpus_references_total:,}<span class="promo-stat-plus">+</span></div>
          <div class="promo-stat-lbl">Клінічних публікацій</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{n_sources}</div>
          <div class="promo-stat-lbl">Цитованих джерел</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{n_redflags}</div>
          <div class="promo-stat-lbl">Red flags</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">~200<span class="promo-stat-plus">мс</span></div>
          <div class="promo-stat-lbl">На один профіль</div>
        </div>
      </div>

      <div class="promo-flow">
        <div class="promo-flow-card">
          <div class="promo-flow-tag">Вхід</div>
          <div class="promo-flow-title">JSON-профіль пацієнта</div>
          <div class="promo-flow-desc">
            FHIR / mCODE-сумісний. <code>disease</code>, <code>biomarkers</code>,
            <code>findings</code>, <code>line_of_therapy</code>.
          </div>
        </div>
        <div class="promo-flow-arrow" aria-hidden="true">→</div>
        <div class="promo-flow-card">
          <div class="promo-flow-tag">Engine · 6 стадій</div>
          <div class="promo-flow-title">Алгоритм + RedFlags</div>
          <div class="promo-flow-desc">
            Resolve → flatten → eval RedFlags → walk algorithm → materialize tracks → resolve regimens.
            Все з KB readonly.
          </div>
        </div>
        <div class="promo-flow-arrow" aria-hidden="true">→</div>
        <div class="promo-flow-card is-output">
          <div class="promo-flow-tag">Вихід</div>
          <div class="promo-flow-title">Plan з ≥2 tracks + trace</div>
          <div class="promo-flow-desc">
            Кожна рекомендація з paraphrased citation, page/section, FDA Crit. 4 fields.
          </div>
          <div class="promo-flow-tracks">
            <div class="promo-flow-track">
              <span class="promo-flow-track-label">Default</span>
              стандартний
            </div>
            <div class="promo-flow-track is-alt">
              <span class="promo-flow-track-label">Alternative</span>
              агресивний
            </div>
          </div>
        </div>
      </div>

      <div class="promo-pillars">
        <div class="promo-pillar">
          <div class="promo-pillar-num">01</div>
          <div>
            <div class="promo-pillar-title">Не «чорний ящик»</div>
            <div class="promo-pillar-desc">
              Кожен крок алгоритму у trace. LLM не приймає клінічних рішень
              (CHARTER §8.3).
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">02</div>
          <div>
            <div class="promo-pillar-title">Кожна claim з citation</div>
            <div class="promo-pillar-desc">
              source_id + position + paraphrased quote + page. FDA Criterion 4 —
              лікар перевіряє підставу.
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">03</div>
          <div>
            <div class="promo-pillar-title">Privacy by design</div>
            <div class="promo-pillar-desc">
              CLI / Pyodide / Python import. Серверу немає. Patient JSON
              лишається на машині.
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">04</div>
          <div>
            <div class="promo-pillar-title">Plan живе</div>
            <div class="promo-pillar-desc">
              <code>revise_plan(...)</code> оновлює рекомендацію щойно з'являються
              нові біомаркери чи findings.
            </div>
          </div>
        </div>
      </div>
    </div>

    <section class="numbers numbers-on-info">
      <h2>Що вже зроблено</h2>
      <div class="num-grid num-grid--rich">

        <div class="num-card">
          <div class="num-big">{n_diseases}</div>
          <div class="num-lbl">Хвороби в KB</div>
          <div class="num-detail">{n_heme} гематологічних · {n_solid} солідних · {diseases_full} з повним ланцюгом · {n_dis_2l} мають 2L+ алгоритм</div>
          <p class="num-text">
            Кожна хвороба має свій <strong>archetype</strong> (etiologically_driven як
            HCV-MZL, risk_stratified як MM, biomarker_driven як NSCLC/EGFR або
            HGBL/MYC-BCL2, stage_driven як cervical), що визначає логіку алгоритму
            вибору лікування. Зараз 1L покрито для всіх {n_diseases} хвороб
            ({n_algos_1l} алгоритмів), 2L+ — для {n_dis_2l_heme} гематологічних
            та {n_dis_2l_solid} солідних ({n_algos_2l} алгоритмів).
          </p>
        </div>

        <div class="num-card num-card--accent">
          <div class="num-big">{n_skills}</div>
          <div class="num-lbl">Лікарі-скіли (віртуальні спеціалісти)</div>
          <div class="num-detail">кожен скіл має свою версію, sources, last_reviewed</div>
          <p class="num-text">
            Гематолог, патолог, інфекціоніст-гепатолог, радіолог, молекулярний генетик,
            клінічний фармацевт, радіотерапевт, паліативна допомога та інші — кожен
            активується на конкретні тригери у профілі пацієнта і додає свої open-questions
            + supportive care recommendations до плану.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_workups}</div>
          <div class="num-lbl">Workups (триаж)</div>
          <div class="num-detail">pre-biopsy діагностичний шлях</div>
          <p class="num-text">
            Коли в пацієнта ще немає підтвердженої гістології (CHARTER §15.2 C7 забороняє
            treatment Plan без неї), engine вмикає <strong>diagnostic mode</strong>: видає
            Workup Brief зі списком тестів, biopsy approach, IHC panel, та переліком ролей
            що мають бути в triage MDT. Як тільки histology підтверджено — diagnostic plan
            promote-иться в treatment plan через <code>revise_plan(...)</code>.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_redflags}</div>
          <div class="num-lbl">Red flags</div>
          <div class="num-detail">тригери ескалації або розслідування</div>
          <p class="num-text">
            Червоні прапорці — структуровані клінічні умови, що автоматично змінюють план:
            <em>RF-BULKY-DISEASE</em> (нодальна маса &gt;7 см) перемикає HCV-MZL з antiviral-first
            на BR + DAA, <em>RF-MM-HIGH-RISK-CYTOGENETICS</em> (t(4;14), del(17p), gain 1q)
            ескалує MM з триплету VRd до квадруплету D-VRd. Кожен RedFlag прив'язаний до
            domain-role, який «виловлює» його у MDT brief.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_regimens}</div>
          <div class="num-lbl">Режими лікування</div>
          <div class="num-detail">{n_indications} показань ({n_inds_1l} першої лінії · {n_inds_2l} 2L+)</div>
          <p class="num-text">
            Кожна схема — список drugs з дозами, шкалою циклів, dose adjustments
            (для renal impairment, FIB-4, frailty), premedications, mandatory supportive
            care та monitoring schedule. Кожна <em>Indication</em> (сполучення
            disease + line_of_therapy + biomarker / stage / demographic-фільтрів) гейтить
            конкретний Regimen — наприклад, MGMT-METHYLATION для GBM Stupp, CD79B/COO/IPI
            для DLBCL R-CHOP vs Pola-R-CHP, t(11;14)/MIPI для MCL, MYC+BCL2 rearrangements
            для HGBL-DH, AFP для HCC, FLIPI для FL.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_drugs}</div>
          <div class="num-lbl">Препарати</div>
          <p class="num-text">
            ATC/RxNorm-кодовані. Кожен з регуляторним статусом FDA/EMA/MOЗ + НСЗУ
            reimbursement (наприклад, daratumumab наразі НЕ реімбурсується НСЗУ —
            це блокер для D-VRd, явно фіксований у плані).
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_tests}</div>
          <div class="num-lbl">Тести / процедури</div>
          <p class="num-text">
            LOINC-кодовані лабораторні + imaging + histology + IHC + genomic тести.
            Кожен має <code>priority_class</code> (critical / standard / desired /
            calculation_based) — рендеряться у Plan як «pre-treatment investigations»
            таблиця.
          </p>
        </div>

        <div class="num-card num-card--accent">
          <div class="num-big">{n_sources}</div>
          <div class="num-lbl">Джерела (top-level guidelines + RCTs)</div>
          <div class="num-detail">NCCN · ESMO · EHA · BSH · EASL · МОЗ · WHO · CTCAE · FDA</div>
          <p class="num-text">
            Під цими {n_sources} джерелами — <strong>{stats.corpus_references_total:,}+ primary
            clinical publications</strong> (RCTs, мета-аналізи, когортні дослідження)
            і <strong>{stats.corpus_pages_total:,} сторінок керівництв</strong>. Сама лише
            NCCN B-Cell Lymphomas guideline — ~500 сторінок з ~700 references.
            Кожна Indication / Regimen / RedFlag цитує конкретні джерела з
            <em>position</em> (supports / contradicts / context), paraphrased
            quote, page/section. FDA Criterion 4 — лікар незалежно перевіряє
            підставу кожної рекомендації.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{stats.specs_count}</div>
          <div class="num-lbl">Специфікації</div>
          <p class="num-text">
            CHARTER (governance + FDA позиціювання), CLINICAL_CONTENT_STANDARDS,
            KNOWLEDGE_SCHEMA, DATA_STANDARDS, SOURCE_INGESTION, REFERENCE_CASE,
            MDT_ORCHESTRATOR, DIAGNOSTIC_MDT, WORKUP_METHODOLOGY, SKILL_ARCHITECTURE.
          </p>
        </div>

      </div>
      <div class="num-foot">
        Зріз станом на <code>{stats.generated_at_utc}</code>.
        Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
        — увесь клінічний контент позначено як <strong>STUB</strong> до dual-sign-off
        Clinical Co-Lead. Це інструмент підтримки рішень, не медичний пристрій.
      </div>
    </section>

    <div class="info-section">
      <h2>1. Як обробляється запит</h2>
      <p class="info-text">
        Лікар дає engine'у JSON-профіль пацієнта (FHIR/mCODE-сумісний у
        майбутньому, спрощений dict у MVP). Engine виконує 6 послідовних
        стадій і повертає Plan з ≥2 альтернативними tracks (CHARTER §2 —
        обидва треки в одному документі, alternative не сховано).
      </p>
      <div class="flow-strip">
        <div class="flow-step">
          <div class="flow-num">Stage 1</div>
          <div class="flow-title">Disease + Algorithm resolve</div>
          <div class="flow-desc">
            <code>disease.icd_o_3_morphology</code> або <code>disease.id</code>
            → знайти Disease entity. Disease + <code>line_of_therapy</code>
            → знайти відповідний Algorithm.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 2</div>
          <div class="flow-title">Findings flattening</div>
          <div class="flow-desc">
            Об'єднує <code>demographics</code> + <code>biomarkers</code>
            + <code>findings</code> в один flat dict для evaluation.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 3</div>
          <div class="flow-title">RedFlag evaluation</div>
          <div class="flow-desc">
            Кожен з {n_redflags} RedFlag-ів перевіряється проти findings.
            Boolean rule engine: <code>any_of</code>/<code>all_of</code>/<code>none_of</code>
            clauses з threshold-ами.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 4</div>
          <div class="flow-title">Algorithm walk</div>
          <div class="flow-desc">
            Decision tree крок за кроком. Кожен step → outcome → branch
            (<code>result</code> або <code>next_step</code>). Trace зберігає
            всі fired_red_flags на кожному кроці.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 5</div>
          <div class="flow-title">Tracks materialization</div>
          <div class="flow-desc">
            ВСІ Indication з <code>algorithm.output_indications</code> стають
            окремими tracks (standard / aggressive / surveillance). Selected
            = default, перший. Решта — alternative.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 6</div>
          <div class="flow-title">Per-track resolution</div>
          <div class="flow-desc">
            Indication → Regimen → MonitoringSchedule + SupportiveCare +
            Contraindications. Все resolve'иться з KB readonly.
          </div>
        </div>
      </div>
      <p class="info-text">
        Час обробки одного пацієнта — 50-200&nbsp;ms (KB load домінує). У
        Pyodide перший запуск 8-15&nbsp;сек (завантаження runtime), наступні
        — як локальний CLI. <strong>Серверу немає</strong> — engine крутиться
        локально (CLI) або у браузері користувача (Pyodide). Patient JSON
        ніколи не залишає машину.
      </p>
    </div>

    <div class="info-section">
      <h2>2. Як ми працюємо з даними пацієнта</h2>
      <p class="info-text">
        Engine читає лише структуровані поля з patient profile. Кожне поле
        має чітку семантику: або тригерить RedFlag, або filter'ує доступні
        Indications, або configurує Regimen materialization. Невпізнані поля
        ігноруються — ніяких «прихованих ефектів».
      </p>
      <table class="kv-table">
        <thead><tr><th>Категорія</th><th>Що читаємо</th><th>Як використовуємо</th></tr></thead>
        <tbody>
          <tr>
            <td>Disease (вхідна точка)</td>
            <td><code>disease.id</code> · <code>icd_o_3_morphology</code> · <code>line_of_therapy</code></td>
            <td>визначає який Algorithm запускати</td>
          </tr>
          <tr>
            <td>Diagnostic mode trigger</td>
            <td><code>disease.suspicion.lineage_hint</code> · <code>tissue_locations</code> · <code>presentation</code></td>
            <td>вмикає DiagnosticPlan замість Plan (workup brief)</td>
          </tr>
          <tr>
            <td>Demographics</td>
            <td><code>age</code> · <code>sex</code> · <code>ecog</code> · <code>fit_for_transplant</code> · <code>decompensated_cirrhosis</code> · <code>pregnancy_status</code></td>
            <td>filter в <code>Indication.applicable_to.demographic_constraints</code></td>
          </tr>
          <tr>
            <td>Biomarkers</td>
            <td>будь-які <code>BIO-X</code> з KB як ключі: <code>BIO-CLL-HIGH-RISK-GENETICS</code>, <code>BIO-MM-CYTOGENETICS-HR</code>, <code>BIO-HCV-RNA</code>, ...</td>
            <td>тригерять RedFlags, filter'ять Indications</td>
          </tr>
          <tr>
            <td>Findings</td>
            <td>{n_redflags}+ структурованих полів — <code>dominant_nodal_mass_cm</code>, <code>ldh_ratio_to_uln</code>, <code>creatinine_clearance_ml_min</code>, <code>blastoid_morphology</code>, <code>tp53_mutation</code>, <code>del_17p</code>, ...</td>
            <td>thresholds у RedFlag triggers</td>
          </tr>
          <tr>
            <td>Prior tests completed</td>
            <td><code>prior_tests_completed: [TEST-IDs]</code></td>
            <td>виключає вже зроблені тести з generated workup_steps</td>
          </tr>
          <tr>
            <td>Clinical record (free-form)</td>
            <td>будь-який <code>clinical_record</code> envelope</td>
            <td>не читається engine'ом — використовується тільки render layer для context</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="info-section">
      <h2>3. Як ми працюємо з джерелами — і чому це наша ключова перевага</h2>
      <div class="hero-corpus" style="max-width:none; margin-bottom:18px;">
        <div class="hcorpus-num">{stats.corpus_references_total:,}+</div>
        <div class="hcorpus-text">
          <strong>{stats.corpus_references_total:,}+ primary clinical publications</strong>
          (RCTs, мета-аналізи, когортні дослідження) реферуються під
          <strong>{n_sources} обраними top-level guidelines</strong>.
          Сумарно — <strong>{stats.corpus_pages_total:,} сторінок керівництв</strong>.
          Жоден лікар фізично не може опрацювати такий обсяг для кожного пацієнта;
          engine реферує його за вас і повертає Plan з phrased citations + page links.
        </div>
      </div>
      <p class="info-text">
        Кожне джерело — це окрема <code>Source</code> entity з власним ID
        (наприклад <code>SRC-NCCN-BCELL-2025</code>), title, version, license,
        access mode (referenced vs hosted per SOURCE_INGESTION_SPEC §1.4).
        Зараз у KB <strong>{n_sources}</strong> джерел:
      </p>
      <table class="kv-table">
        <thead><tr><th>Source ID</th><th>Тип</th><th>Сторінок</th><th>Primary refs</th><th>Роль у корпусі</th></tr></thead>
        <tbody>
          <tr><td><code>SRC-NCCN-BCELL-2025</code></td><td>NCCN B-Cell Lymphomas v.2.2025</td><td class="num">500</td><td class="num">700</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MM-2025</code></td><td>NCCN Multiple Myeloma 2025</td><td class="num">400</td><td class="num">600</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-AML-2025</code></td><td>NCCN AML 2025</td><td class="num">350</td><td class="num">500</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MPN-2025</code></td><td>NCCN MPN 2025</td><td class="num">300</td><td class="num">400</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-EASL-HCV-2023</code></td><td>EASL HCV Guidelines 2023</td><td class="num">80</td><td class="num">250</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-WHO-LNSC-2023</code></td><td>WHO Lymph Node, Spleen, Thymus Cytopathology</td><td class="num">150</td><td class="num">200</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-CTCAE-V5</code></td><td>NCI CTCAE v5.0 (toxicity terminology)</td><td class="num">150</td><td class="num">30</td><td>terminology</td></tr>
          <tr><td><code>SRC-ESMO-MZL-2024</code></td><td>ESMO Marginal Zone Lymphomas 2024</td><td class="num">30</td><td class="num">150</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-BSH-MZL-2024</code></td><td>BSH MZL Guideline 2024</td><td class="num">50</td><td class="num">120</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-EHA-WORKUP-2024</code></td><td>EHA Practical Workup Guidelines 2024</td><td class="num">40</td><td class="num">100</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-MOZ-UA-LYMPH-2024</code></td><td>МОЗ Україна — Лімфоми (placeholder)</td><td class="num">60</td><td class="num">50</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-ARCAINI-2014</code></td><td>IELSG-19 RCT — MALT lymphoma</td><td class="num">10</td><td class="num">50</td><td>rct_publication</td></tr>
          <tr><td><code>SRC-FDA-CDS-2026</code></td><td>FDA CDS Software Guidance 2026</td><td class="num">30</td><td class="num">20</td><td>regulatory</td></tr>
          <tr><td colspan="2"><strong>Сумарно</strong></td><td class="num"><strong>{stats.corpus_pages_total:,}</strong></td><td class="num"><strong>{stats.corpus_references_total:,}+</strong></td><td>—</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        <strong>Кожна клінічна claim у KB має citation</strong>. Indication,
        Regimen, RedFlag, Algorithm — всі мають поле <code>sources: list</code>
        де для кожного джерела вказано:
      </p>
      <div class="q-list">
        <h4>Структура citation</h4>
        <ul>
          <li><code>source_id</code> — посилання на Source entity</li>
          <li><code>position</code> — <em>supports</em> / <em>contradicts</em> / <em>context</em></li>
          <li><code>relevant_quote_paraphrase</code> — паніфразоване твердження з guideline (не дослівне copy-paste для license safety)</li>
          <li><code>page_or_section</code> — точна локалізація в документі</li>
        </ul>
      </div>
      <p class="info-text">
        Render layer показує <strong>повний список cited sources</strong>
        під кожною Indication у Plan. Це і є FDA Criterion 4 (CHARTER §15.2):
        лікар може незалежно перевірити підставу кожної рекомендації, не
        довіряючись engine на віру.
      </p>
      <div class="callout callout-good">
        <strong>Source hosting за замовчуванням — referenced.</strong>
        Ми не дублюємо бази (NCCN, ESMO, etc.) — посилаємось. Hosting
        потребує explicit H1-H5 justification (CHARTER §15.2 referenced
        vs hosted vs mixed). Виключення: PDF документи (FDA CDS, CTCAE)
        збережено локально для archive stability.
      </div>
    </div>

    <div class="info-section">
      <h2>4. Як ми обробляємо запити</h2>
      <p class="info-text">
        Три способи запустити engine, жоден не серверний:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">CLI</div>
          <div class="num-lbl">Локально на машині лікаря</div>
          <p class="num-text">
            <code>python -m knowledge_base.engine.cli --patient profile.json --render plan.html</code>.
            Працює offline, не потребує мережі. Profile залишається на диску.
          </p>
        </div>
        <div class="num-card num-card--accent">
          <div class="num-big">Pyodide</div>
          <div class="num-lbl">У браузері (try.html)</div>
          <p class="num-text">
            Pyodide v0.26.4 завантажує Python WebAssembly runtime, micropip
            ставить pydantic+pyyaml, розпаковує engine bundle (~302KB) у
            in-memory FS. Engine крутиться у браузері. Patient JSON не
            покидає машину.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">Library</div>
          <div class="num-lbl">Python import</div>
          <p class="num-text">
            <code>from knowledge_base.engine import generate_plan, revise_plan</code>
            — інтеграція з EHR, CSV pipelines, batch testing. Stateless, deterministic.
          </p>
        </div>
      </div>
      <div class="callout callout-good">
        <strong>Privacy by design.</strong> Patient JSON ніколи не залишає
        машину користувача. Немає логів, немає БД, немає accidental
        leakage. Reproducibility: <code>Plan.knowledge_base_state.algorithm_version</code>
        фіксує версію KB → same input + same KB = same output.
      </div>
    </div>

    <div class="info-section">
      <h2>5. Що повертаємо назад</h2>
      <p class="info-text">
        Engine повертає <strong>Plan</strong> (treatment mode) або
        <strong>DiagnosticPlan</strong> (workup brief). Кожен Plan містить:
      </p>
      <table class="kv-table">
        <thead><tr><th>Поле</th><th>Що містить</th></tr></thead>
        <tbody>
          <tr><td><code>tracks[]</code></td><td>≥2 alternative tracks (default first), кожен з indication + regimen + monitoring + supportive_care + contraindications</td></tr>
          <tr><td><code>fda_compliance</code></td><td>FDA Criterion 4 fields: intended_use, hcp_user_specification, patient_population_match, algorithm_summary, data_sources_summary, data_limitations, automation_bias_warning</td></tr>
          <tr><td><code>trace</code></td><td>покрокова історія walk_algorithm: step / outcome / branch / fired_red_flags для кожного кроку</td></tr>
          <tr><td><code>knowledge_base_state</code></td><td>snapshot версії KB на момент генерації (audit per CHARTER §10.2)</td></tr>
          <tr><td><code>kb_resolved</code></td><td>всі referenced entities (Disease, Tests, RedFlags, Algorithm) для render layer</td></tr>
          <tr><td><code>warnings</code></td><td>schema/ref errors, time_critical disqualifications, missing data hints</td></tr>
          <tr><td><code>supersedes</code> / <code>superseded_by</code></td><td>версійний chain між plans для тієї ж пацієнта</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        Опціонально вмикається <strong>MDT brief</strong> — orchestrate_mdt() читає Plan +
        патієнтський профіль і додає required/recommended/optional ролі (з {n_skills}
        віртуальних спеціалістів), open questions, provenance graph. Renders як inline
        section у Plan HTML.
      </p>
    </div>

    <div class="info-section">
      <h2>6. Як план оновлюється при появі нових даних</h2>
      <p class="info-text">
        <code>revise_plan(updated_patient, previous_plan, revision_trigger)</code>
        приймає оновлений профіль і генерує нову версію плану з
        <code>supersedes</code>/<code>superseded_by</code> chain. Три легальні
        переходи + одна заборона:
      </p>
      <table class="kv-table">
        <thead><tr><th>Із</th><th>Зі змінами</th><th>Перехід</th><th>Результат</th></tr></thead>
        <tbody>
          <tr><td>DiagnosticPlan vN</td><td>тільки suspicion (без histology)</td><td>diagnostic → diagnostic</td><td>DiagnosticPlan v(N+1)</td></tr>
          <tr><td>DiagnosticPlan vN</td><td>підтверджена histology</td><td>diagnostic → treatment <strong>(promotion)</strong></td><td>Plan v1 (перший treatment)</td></tr>
          <tr><td>Plan vN</td><td>будь-яке оновлення з histology</td><td>treatment → treatment</td><td>Plan v(N+1)</td></tr>
          <tr><td>Plan vN</td><td>видалено histology</td><td colspan="2"><span style="color:var(--red);font-weight:600;">ILLEGAL — ValueError, CHARTER §15.2 C7</span></td></tr>
        </tbody>
      </table>
      <p class="info-text">
        Попередній plan <strong>не мутується</strong> — повертається deep copy
        з <code>superseded_by</code> заповненим. Caller (CLI / EHR) сам вирішує
        що робити з обома версіями. Per CHARTER §10.2 — стара версія
        зберігається indefinitely.
      </p>
      <div class="callout callout-good">
        <strong>Що тригерить новий plan:</strong> зміна будь-якого з ~30 структурованих
        полів — нові biomarkers (del(17p) виявлено), нова стадія (ECOG 1→3),
        нові findings (bulky disease на restaging), нові infectious flags (HBV
        reactivation), pregnancy detected. Зміна <code>clinical_record</code>
        free-text НЕ тригерить regeneration (engine не читає free text).
      </div>
    </div>

    <div class="info-section">
      <h2>7. Що ще робимо</h2>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">{n_workups}</div>
          <div class="num-lbl">Diagnostic workups</div>
          <p class="num-text">
            Pre-biopsy режим: коли histology ще немає, engine видає
            <strong>Workup Brief</strong> зі списком тестів, biopsy approach,
            IHC panel і ролей triage MDT. Per CHARTER §15.2 C7 — без
            histology treatment Plan не генерується.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">MDT</div>
          <div class="num-lbl">Multidisciplinary brief</div>
          <p class="num-text">
            Orchestrator читає Plan + profile і призначає required/recommended/
            optional ролі ({n_skills} catalog), формулює open questions
            (Q1-Q6 + DQ1-DQ4), будує decision provenance graph.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">stats</div>
          <div class="num-lbl">KB dashboard</div>
          <p class="num-text">
            <code>python -m knowledge_base.stats</code> — actual entity counts
            + per-disease coverage matrix + reviewer signoff ratio. Доступне
            як CLI / JSON / embeddable HTML widget для landing page.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">render</div>
          <div class="num-lbl">A4 print-friendly HTML</div>
          <p class="num-text">
            Single-file HTML з embedded CSS, без external assets крім Google Fonts.
            Adapt'ується під A4 print через <code>@page</code> + <code>@media print</code>.
            Tracks side-by-side, alternative не сховано (anti automation-bias per CHARTER §15.2 C6).
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">trials</div>
          <div class="num-lbl">Experimental options (Phase C — done)</div>
          <p class="num-text">
            <code>enumerate_experimental_options(...)</code> запитує
            ClinicalTrials.gov v2 за disease + biomarker + line_of_therapy і
            повертає <code>ExperimentalOption</code> з UA-availability metadata
            (sites_ua, countries) — render-time, engine не використовує trial
            як сигнал вибору. Status filter: RECRUITING /
            ACTIVE_NOT_RECRUITING / ENROLLING_BY_INVITATION; інтегровано у
            <code>generate_plan</code>, render показує третій трек у Plan;
            7-day on-disk TTL cache для офлайн-запусків.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">access</div>
          <div class="num-lbl">Access Matrix (Phase D)</div>
          <p class="num-text">
            Кожен Plan містить <code>AccessMatrix</code> — per-track agg-table
            UA-реєстрації, НСЗУ-покриття, cost orientation (₴ ranges) і
            primary <code>AccessPathway</code>. Render-time only (CHARTER §8.3,
            invariant test guarantee). Stale-cost warning при
            <code>cost_last_updated</code> &gt; 180 днів. Trial-рядки додаються
            автоматично коли experimental track активний.
          </p>
        </div>
      </div>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    Жодних реальних пацієнтських даних · CHARTER §9.3.
    Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


def _render_capabilities_en(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_regimens = by_type.get("regimens", 0)
    n_tests = by_type.get("tests", 0)
    n_redflags = by_type.get("redflags", 0)
    n_workups = by_type.get("workups", 0)
    n_sources = by_type.get("sources", 0)
    n_drugs = by_type.get("drugs", 0)
    n_skills = stats.skills_planned_roles
    cov = _coverage_breakdown()
    n_heme = cov["heme_diseases"]
    n_solid = cov["solid_diseases"]
    n_algos_1l = cov["algorithms_1l"]
    n_algos_2l = cov["algorithms_2l_plus"]
    n_inds_1l = cov["indications_1l"]
    n_inds_2l = cov["indications_2l_plus"]
    n_dis_2l = cov["diseases_with_2l_plus"]
    n_dis_2l_heme = cov["diseases_with_2l_plus_heme"]
    n_dis_2l_solid = cov["diseases_with_2l_plus_solid"]
    diseases_full = sum(
        1 for d in stats.diseases
        if d.coverage_status in {"stub_full_chain", "reviewed"}
    )
    diseases_partial = sum(1 for d in stats.diseases if d.coverage_status == "partial")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Capabilities</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="capabilities", target_lang="en", lang_switch_href=_lang_switch_href("capabilities", "en"))}

<main>
  <section class="info-page">
    <h1>Capabilities</h1>
    <p class="lead">
      OpenOnco takes a JSON patient profile and returns a structured treatment
      plan or a diagnostic brief, with a full trace of every decision and
      citations for every claim. There is no black box: every recommendation
      comes from declarative rules you can read in the knowledge base and
      follow through the trace. The rest of this page details how we work
      with data, sources, and requests.
    </p>

    <div class="promo-info" role="img" aria-label="OpenOnco — capabilities infographic">
      <div class="promo-eyebrow">OpenOnco · v0.1 · the engine, distilled</div>
      <h2 class="promo-headline">
        One JSON profile → <em>two alternative treatment plans</em>,
        a citation under every recommendation.
      </h2>
      <p class="promo-sub">
        A declarative rule engine across <strong>{n_diseases} diseases</strong>,
        backed by <strong>{stats.corpus_references_total:,}+ clinical publications</strong>
        under <strong>{n_sources} top-level guidelines</strong>. No LLM in the clinical
        decision, no server, no logs. Patient JSON never leaves the machine.
      </p>

      <div class="promo-stats">
        <div class="promo-stat">
          <div class="promo-stat-num">{n_diseases}</div>
          <div class="promo-stat-lbl">Diseases in KB</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{stats.corpus_references_total:,}<span class="promo-stat-plus">+</span></div>
          <div class="promo-stat-lbl">Clinical publications</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{n_sources}</div>
          <div class="promo-stat-lbl">Cited sources</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">{n_redflags}</div>
          <div class="promo-stat-lbl">Red flags</div>
        </div>
        <div class="promo-stat">
          <div class="promo-stat-num">~200<span class="promo-stat-plus">ms</span></div>
          <div class="promo-stat-lbl">Per profile</div>
        </div>
      </div>

      <div class="promo-flow">
        <div class="promo-flow-card">
          <div class="promo-flow-tag">Input</div>
          <div class="promo-flow-title">Patient JSON profile</div>
          <div class="promo-flow-desc">
            FHIR / mCODE-friendly. <code>disease</code>, <code>biomarkers</code>,
            <code>findings</code>, <code>line_of_therapy</code>.
          </div>
        </div>
        <div class="promo-flow-arrow" aria-hidden="true">→</div>
        <div class="promo-flow-card">
          <div class="promo-flow-tag">Engine · 6 stages</div>
          <div class="promo-flow-title">Algorithm + RedFlags</div>
          <div class="promo-flow-desc">
            Resolve → flatten → eval RedFlags → walk algorithm → materialize tracks → resolve regimens.
            All from a readonly KB.
          </div>
        </div>
        <div class="promo-flow-arrow" aria-hidden="true">→</div>
        <div class="promo-flow-card is-output">
          <div class="promo-flow-tag">Output</div>
          <div class="promo-flow-title">Plan with ≥2 tracks + trace</div>
          <div class="promo-flow-desc">
            Each recommendation carries paraphrased citation, page/section, FDA Crit. 4 fields.
          </div>
          <div class="promo-flow-tracks">
            <div class="promo-flow-track">
              <span class="promo-flow-track-label">Default</span>
              standard
            </div>
            <div class="promo-flow-track is-alt">
              <span class="promo-flow-track-label">Alternative</span>
              aggressive
            </div>
          </div>
        </div>
      </div>

      <div class="promo-pillars">
        <div class="promo-pillar">
          <div class="promo-pillar-num">01</div>
          <div>
            <div class="promo-pillar-title">No black box</div>
            <div class="promo-pillar-desc">
              Every algorithm step in the trace. LLMs do not make clinical
              decisions (CHARTER §8.3).
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">02</div>
          <div>
            <div class="promo-pillar-title">Every claim cited</div>
            <div class="promo-pillar-desc">
              source_id + position + paraphrased quote + page. FDA Criterion 4 —
              the clinician verifies the basis.
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">03</div>
          <div>
            <div class="promo-pillar-title">Privacy by design</div>
            <div class="promo-pillar-desc">
              CLI / Pyodide / Python import. No server. Patient JSON stays
              on the user's machine.
            </div>
          </div>
        </div>
        <div class="promo-pillar">
          <div class="promo-pillar-num">04</div>
          <div>
            <div class="promo-pillar-title">The plan is alive</div>
            <div class="promo-pillar-desc">
              <code>revise_plan(...)</code> updates recommendations as new
              biomarkers and findings come in.
            </div>
          </div>
        </div>
      </div>
    </div>

    <section class="numbers numbers-on-info">
      <h2>What's already in</h2>
      <div class="num-grid num-grid--rich">

        <div class="num-card">
          <div class="num-big">{n_diseases}</div>
          <div class="num-lbl">Diseases in the KB</div>
          <div class="num-detail">{n_heme} hematologic · {n_solid} solid · {diseases_full} with the full chain · {n_dis_2l} carry a 2L+ algorithm</div>
          <p class="num-text">
            Each disease carries an <strong>archetype</strong>
            (etiologically_driven like HCV-MZL, risk_stratified like MM,
            biomarker_driven like NSCLC/EGFR or HGBL/MYC-BCL2, stage_driven
            like cervical) which determines the algorithm logic for treatment
            selection. 1L is covered for all {n_diseases} diseases
            ({n_algos_1l} algorithms); 2L+ is covered for {n_dis_2l_heme}
            hematologic and {n_dis_2l_solid} solid diseases ({n_algos_2l} algorithms).
          </p>
        </div>

        <div class="num-card num-card--accent">
          <div class="num-big">{n_skills}</div>
          <div class="num-lbl">Clinician skills (virtual specialists)</div>
          <div class="num-detail">each skill carries its own version, sources, last_reviewed</div>
          <p class="num-text">
            Hematologist, pathologist, infectious-disease/hepatologist,
            radiologist, molecular geneticist, clinical pharmacist, radiation
            oncologist, palliative care and others — each is activated by
            specific triggers in the patient profile and contributes its own
            open questions and supportive-care recommendations to the plan.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_workups}</div>
          <div class="num-lbl">Workups (triage)</div>
          <div class="num-detail">pre-biopsy diagnostic path</div>
          <p class="num-text">
            When histology is not yet confirmed (CHARTER §15.2 C7 forbids a
            treatment Plan without it), the engine switches into
            <strong>diagnostic mode</strong>: it emits a Workup Brief with
            the test list, biopsy approach, IHC panel, and the roles required
            in the triage MDT. Once histology is confirmed, the diagnostic
            plan is promoted to a treatment plan via
            <code>revise_plan(...)</code>.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_redflags}</div>
          <div class="num-lbl">Red flags</div>
          <div class="num-detail">escalation or investigation triggers</div>
          <p class="num-text">
            Red flags are structured clinical conditions that automatically
            change the plan: <em>RF-BULKY-DISEASE</em> (nodal mass &gt;7 cm)
            switches HCV-MZL from antiviral-first to BR + DAA;
            <em>RF-MM-HIGH-RISK-CYTOGENETICS</em> (t(4;14), del(17p), gain 1q)
            escalates MM from triplet VRd to quadruplet D-VRd. Every RedFlag
            is bound to a domain role that "catches" it in the MDT brief.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_regimens}</div>
          <div class="num-lbl">Treatment regimens</div>
          <div class="num-detail">{n_indications} indications ({n_inds_1l} first-line · {n_inds_2l} 2L+)</div>
          <p class="num-text">
            Each regimen is a list of drugs with doses, cycle schedule, dose
            adjustments (renal impairment, FIB-4, frailty), premedications,
            mandatory supportive care, and a monitoring schedule. Every
            <em>Indication</em> (the combination of disease + line_of_therapy +
            biomarker / stage / demographic filters) gates a specific Regimen —
            e.g. MGMT-METHYLATION for GBM Stupp; CD79B / COO-Hans / IPI for DLBCL
            R-CHOP vs Pola-R-CHP; t(11;14) / MIPI for MCL; MYC + BCL2 rearrangements
            for HGBL-DH; AFP for HCC; FLIPI for FL.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_drugs}</div>
          <div class="num-lbl">Drugs</div>
          <p class="num-text">
            ATC/RxNorm-coded. Each carries its FDA/EMA/local-MoH regulatory
            status plus reimbursement flags (e.g. daratumumab is currently
            NOT reimbursed by Ukraine's NHSU — a hard blocker for D-VRd,
            surfaced explicitly in the plan).
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{n_tests}</div>
          <div class="num-lbl">Tests / procedures</div>
          <p class="num-text">
            LOINC-coded labs + imaging + histology + IHC + genomic tests.
            Each carries a <code>priority_class</code> (critical / standard /
            desired / calculation_based) — rendered in every Plan as the
            "pre-treatment investigations" table.
          </p>
        </div>

        <div class="num-card num-card--accent">
          <div class="num-big">{n_sources}</div>
          <div class="num-lbl">Sources (top-level guidelines + RCTs)</div>
          <div class="num-detail">NCCN · ESMO · EHA · BSH · EASL · MoH UA · WHO · CTCAE · FDA</div>
          <p class="num-text">
            Behind these {n_sources} curated sources sit
            <strong>{stats.corpus_references_total:,}+ primary clinical
            publications</strong> (RCTs, meta-analyses, cohort studies) and
            <strong>{stats.corpus_pages_total:,} pages of guideline text</strong>.
            The NCCN B-Cell Lymphomas guideline alone is ~500 pages with
            ~700 references. Every Indication / Regimen / RedFlag cites
            specific sources with a <em>position</em> (supports / contradicts
            / context), a paraphrased quote, and page/section locator. FDA
            Criterion 4 — the clinician independently verifies the basis
            for every recommendation.
          </p>
        </div>

        <div class="num-card">
          <div class="num-big">{stats.specs_count}</div>
          <div class="num-lbl">Specifications</div>
          <p class="num-text">
            CHARTER (governance + FDA positioning), CLINICAL_CONTENT_STANDARDS,
            KNOWLEDGE_SCHEMA, DATA_STANDARDS, SOURCE_INGESTION, REFERENCE_CASE,
            MDT_ORCHESTRATOR, DIAGNOSTIC_MDT, WORKUP_METHODOLOGY,
            SKILL_ARCHITECTURE.
          </p>
        </div>

      </div>
      <div class="num-foot">
        Snapshot as of <code>{stats.generated_at_utc}</code>.
        Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
        — all clinical content is marked <strong>STUB</strong> until two of
        three Clinical Co-Leads sign it off. This is a decision-support tool,
        not a medical device.
      </div>
    </section>

    <div class="info-section">
      <h2>1. How a request is processed</h2>
      <p class="info-text">
        The clinician feeds the engine a JSON patient profile (FHIR/mCODE-aligned
        in the future, a simplified dict in the MVP). The engine runs six
        sequential stages and returns a Plan with ≥2 alternative tracks
        (CHARTER §2 — both tracks live in the same document; alternatives
        are never hidden).
      </p>
      <div class="flow-strip">
        <div class="flow-step">
          <div class="flow-num">Stage 1</div>
          <div class="flow-title">Disease + Algorithm resolve</div>
          <div class="flow-desc">
            <code>disease.icd_o_3_morphology</code> or <code>disease.id</code>
            → look up the Disease entity. Disease + <code>line_of_therapy</code>
            → look up the matching Algorithm.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 2</div>
          <div class="flow-title">Findings flattening</div>
          <div class="flow-desc">
            Merges <code>demographics</code> + <code>biomarkers</code> +
            <code>findings</code> into one flat dict for evaluation.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 3</div>
          <div class="flow-title">RedFlag evaluation</div>
          <div class="flow-desc">
            Each of the {n_redflags} RedFlags is checked against the findings.
            Boolean rule engine: <code>any_of</code> / <code>all_of</code> /
            <code>none_of</code> clauses with thresholds.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 4</div>
          <div class="flow-title">Algorithm walk</div>
          <div class="flow-desc">
            Decision tree, step by step. Each step → outcome → branch
            (<code>result</code> or <code>next_step</code>). The trace records
            every fired_red_flags entry at each step.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 5</div>
          <div class="flow-title">Tracks materialization</div>
          <div class="flow-desc">
            ALL Indications in <code>algorithm.output_indications</code> become
            their own tracks (standard / aggressive / surveillance). The first
            is the default; the rest are alternatives.
          </div>
        </div>
        <div class="flow-step">
          <div class="flow-num">Stage 6</div>
          <div class="flow-title">Per-track resolution</div>
          <div class="flow-desc">
            Indication → Regimen → MonitoringSchedule + SupportiveCare +
            Contraindications. Everything resolves from the read-only KB.
          </div>
        </div>
      </div>
      <p class="info-text">
        Per-patient processing time is 50–200&nbsp;ms (KB load dominates).
        In Pyodide the first run takes 8–15&nbsp;sec (runtime download); subsequent
        runs match a local CLI. <strong>There is no server</strong> — the engine
        runs locally (CLI) or in the user's browser (Pyodide). The patient JSON
        never leaves the machine.
      </p>
    </div>

    <div class="info-section">
      <h2>2. How we work with patient data</h2>
      <p class="info-text">
        The engine reads only structured fields from the patient profile.
        Each field has a clear semantic role: it either triggers a RedFlag,
        filters available Indications, or configures Regimen materialization.
        Unknown fields are ignored — no hidden side effects.
      </p>
      <table class="kv-table">
        <thead><tr><th>Category</th><th>What we read</th><th>How we use it</th></tr></thead>
        <tbody>
          <tr>
            <td>Disease (entry point)</td>
            <td><code>disease.id</code> · <code>icd_o_3_morphology</code> · <code>line_of_therapy</code></td>
            <td>determines which Algorithm to run</td>
          </tr>
          <tr>
            <td>Diagnostic-mode trigger</td>
            <td><code>disease.suspicion.lineage_hint</code> · <code>tissue_locations</code> · <code>presentation</code></td>
            <td>switches output to DiagnosticPlan instead of Plan (workup brief)</td>
          </tr>
          <tr>
            <td>Demographics</td>
            <td><code>age</code> · <code>sex</code> · <code>ecog</code> · <code>fit_for_transplant</code> · <code>decompensated_cirrhosis</code> · <code>pregnancy_status</code></td>
            <td>filter on <code>Indication.applicable_to.demographic_constraints</code></td>
          </tr>
          <tr>
            <td>Biomarkers</td>
            <td>any <code>BIO-X</code> from the KB as keys: <code>BIO-CLL-HIGH-RISK-GENETICS</code>, <code>BIO-MM-CYTOGENETICS-HR</code>, <code>BIO-HCV-RNA</code>, …</td>
            <td>fire RedFlags, filter Indications</td>
          </tr>
          <tr>
            <td>Findings</td>
            <td>{n_redflags}+ structured fields — <code>dominant_nodal_mass_cm</code>, <code>ldh_ratio_to_uln</code>, <code>creatinine_clearance_ml_min</code>, <code>blastoid_morphology</code>, <code>tp53_mutation</code>, <code>del_17p</code>, …</td>
            <td>thresholds inside RedFlag triggers</td>
          </tr>
          <tr>
            <td>Prior tests completed</td>
            <td><code>prior_tests_completed: [TEST-IDs]</code></td>
            <td>excludes already-done tests from generated workup_steps</td>
          </tr>
          <tr>
            <td>Clinical record (free-form)</td>
            <td>any <code>clinical_record</code> envelope</td>
            <td>not read by the engine — surfaced only by the render layer for context</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="info-section">
      <h2>3. How we work with sources — and why this is our key advantage</h2>
      <div class="hero-corpus" style="max-width:none; margin-bottom:18px;">
        <div class="hcorpus-num">{stats.corpus_references_total:,}+</div>
        <div class="hcorpus-text">
          <strong>{stats.corpus_references_total:,}+ primary clinical
          publications</strong> (RCTs, meta-analyses, cohort studies) sit
          beneath <strong>{n_sources} curated top-level guidelines</strong>.
          That is <strong>{stats.corpus_pages_total:,} pages of guideline
          text</strong> in total. No clinician can physically work through
          that volume for every patient; the engine indexes it for you and
          returns a Plan with phrased citations and page-level locators.
        </div>
      </div>
      <p class="info-text">
        Each source is its own <code>Source</code> entity with a stable ID
        (e.g. <code>SRC-NCCN-BCELL-2025</code>), title, version, license, and
        access mode (referenced vs hosted per SOURCE_INGESTION_SPEC §1.4).
        The KB currently holds <strong>{n_sources}</strong> sources:
      </p>
      <table class="kv-table">
        <thead><tr><th>Source ID</th><th>Type</th><th>Pages</th><th>Primary refs</th><th>Role in the corpus</th></tr></thead>
        <tbody>
          <tr><td><code>SRC-NCCN-BCELL-2025</code></td><td>NCCN B-Cell Lymphomas v.2.2025</td><td class="num">500</td><td class="num">700</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MM-2025</code></td><td>NCCN Multiple Myeloma 2025</td><td class="num">400</td><td class="num">600</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-AML-2025</code></td><td>NCCN AML 2025</td><td class="num">350</td><td class="num">500</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-NCCN-MPN-2025</code></td><td>NCCN MPN 2025</td><td class="num">300</td><td class="num">400</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-EASL-HCV-2023</code></td><td>EASL HCV Guidelines 2023</td><td class="num">80</td><td class="num">250</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-WHO-LNSC-2023</code></td><td>WHO Lymph Node, Spleen, Thymus Cytopathology</td><td class="num">150</td><td class="num">200</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-CTCAE-V5</code></td><td>NCI CTCAE v5.0 (toxicity terminology)</td><td class="num">150</td><td class="num">30</td><td>terminology</td></tr>
          <tr><td><code>SRC-ESMO-MZL-2024</code></td><td>ESMO Marginal Zone Lymphomas 2024</td><td class="num">30</td><td class="num">150</td><td>primary_guideline</td></tr>
          <tr><td><code>SRC-BSH-MZL-2024</code></td><td>BSH MZL Guideline 2024</td><td class="num">50</td><td class="num">120</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-EHA-WORKUP-2024</code></td><td>EHA Practical Workup Guidelines 2024</td><td class="num">40</td><td class="num">100</td><td>diagnostic_methodology</td></tr>
          <tr><td><code>SRC-MOZ-UA-LYMPH-2024</code></td><td>Ukraine MoH — Lymphomas (placeholder)</td><td class="num">60</td><td class="num">50</td><td>regional_guideline</td></tr>
          <tr><td><code>SRC-ARCAINI-2014</code></td><td>IELSG-19 RCT — MALT lymphoma</td><td class="num">10</td><td class="num">50</td><td>rct_publication</td></tr>
          <tr><td><code>SRC-FDA-CDS-2026</code></td><td>FDA CDS Software Guidance 2026</td><td class="num">30</td><td class="num">20</td><td>regulatory</td></tr>
          <tr><td colspan="2"><strong>Total</strong></td><td class="num"><strong>{stats.corpus_pages_total:,}</strong></td><td class="num"><strong>{stats.corpus_references_total:,}+</strong></td><td>—</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        <strong>Every clinical claim in the KB has a citation</strong>.
        Indication, Regimen, RedFlag, Algorithm — all carry a
        <code>sources: list</code> field where each source is annotated with:
      </p>
      <div class="q-list">
        <h4>Citation structure</h4>
        <ul>
          <li><code>source_id</code> — points to the Source entity</li>
          <li><code>position</code> — <em>supports</em> / <em>contradicts</em> / <em>context</em></li>
          <li><code>relevant_quote_paraphrase</code> — paraphrased statement from the guideline (not verbatim copy-paste, for license safety)</li>
          <li><code>page_or_section</code> — exact locator inside the document</li>
        </ul>
      </div>
      <p class="info-text">
        The render layer surfaces the <strong>full list of cited sources</strong>
        below every Indication in the Plan. This is FDA Criterion 4
        (CHARTER §15.2): the clinician can independently verify the basis
        for every recommendation, instead of taking the engine on faith.
      </p>
      <div class="callout callout-good">
        <strong>Source hosting defaults to referenced.</strong> We do not
        mirror external databases (NCCN, ESMO, etc.) — we link to them.
        Hosting requires an explicit H1–H5 justification (CHARTER §15.2,
        referenced vs hosted vs mixed). Exception: regulatory PDFs (FDA CDS,
        CTCAE) are kept locally for archive stability.
      </div>
    </div>

    <div class="info-section">
      <h2>4. How we run requests</h2>
      <p class="info-text">
        Three ways to run the engine — none of them server-bound:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">CLI</div>
          <div class="num-lbl">Locally on the clinician's machine</div>
          <p class="num-text">
            <code>python -m knowledge_base.engine.cli --patient profile.json --render plan.html</code>.
            Works offline, no network needed. The profile stays on disk.
          </p>
        </div>
        <div class="num-card num-card--accent">
          <div class="num-big">Pyodide</div>
          <div class="num-lbl">In the browser (try.html)</div>
          <p class="num-text">
            Pyodide v0.26.4 loads the Python WebAssembly runtime, micropip
            installs pydantic + pyyaml, and the engine bundle (~302 KB) is
            unpacked into the in-memory FS. The engine runs in the browser.
            Patient JSON never leaves the machine.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">Library</div>
          <div class="num-lbl">Python import</div>
          <p class="num-text">
            <code>from knowledge_base.engine import generate_plan, revise_plan</code>
            — integration with EHRs, CSV pipelines, batch testing. Stateless
            and deterministic.
          </p>
        </div>
      </div>
      <div class="callout callout-good">
        <strong>Privacy by design.</strong> Patient JSON never leaves the
        user's machine. There are no logs, no database, no accidental
        leakage. Reproducibility:
        <code>Plan.knowledge_base_state.algorithm_version</code> pins the
        KB version — same input + same KB = same output.
      </div>
    </div>

    <div class="info-section">
      <h2>5. What we return</h2>
      <p class="info-text">
        The engine returns a <strong>Plan</strong> (treatment mode) or a
        <strong>DiagnosticPlan</strong> (workup brief). Each Plan contains:
      </p>
      <table class="kv-table">
        <thead><tr><th>Field</th><th>Contents</th></tr></thead>
        <tbody>
          <tr><td><code>tracks[]</code></td><td>≥2 alternative tracks (default first), each with indication + regimen + monitoring + supportive_care + contraindications</td></tr>
          <tr><td><code>fda_compliance</code></td><td>FDA Criterion 4 fields: intended_use, hcp_user_specification, patient_population_match, algorithm_summary, data_sources_summary, data_limitations, automation_bias_warning</td></tr>
          <tr><td><code>trace</code></td><td>step-by-step history of walk_algorithm: step / outcome / branch / fired_red_flags for every step</td></tr>
          <tr><td><code>knowledge_base_state</code></td><td>snapshot of the KB version at generation time (audit per CHARTER §10.2)</td></tr>
          <tr><td><code>kb_resolved</code></td><td>all referenced entities (Disease, Tests, RedFlags, Algorithm) for the render layer</td></tr>
          <tr><td><code>warnings</code></td><td>schema/ref errors, time-critical disqualifications, missing-data hints</td></tr>
          <tr><td><code>supersedes</code> / <code>superseded_by</code></td><td>version chain across plans for the same patient</td></tr>
        </tbody>
      </table>
      <p class="info-text">
        Optionally, a <strong>MDT brief</strong> is added by
        orchestrate_mdt(): it reads the Plan + patient profile and appends
        required / recommended / optional roles (drawn from {n_skills} virtual
        specialists), open questions, and a provenance graph. It renders as
        an inline section inside the Plan HTML.
      </p>
    </div>

    <div class="info-section">
      <h2>6. How a plan updates when new data arrives</h2>
      <p class="info-text">
        <code>revise_plan(updated_patient, previous_plan, revision_trigger)</code>
        takes the updated profile and produces a new plan version with a
        <code>supersedes</code> / <code>superseded_by</code> chain. Three
        legal transitions plus one prohibition:
      </p>
      <table class="kv-table">
        <thead><tr><th>From</th><th>With changes</th><th>Transition</th><th>Result</th></tr></thead>
        <tbody>
          <tr><td>DiagnosticPlan vN</td><td>only suspicion (no histology)</td><td>diagnostic → diagnostic</td><td>DiagnosticPlan v(N+1)</td></tr>
          <tr><td>DiagnosticPlan vN</td><td>confirmed histology</td><td>diagnostic → treatment <strong>(promotion)</strong></td><td>Plan v1 (first treatment)</td></tr>
          <tr><td>Plan vN</td><td>any update with histology present</td><td>treatment → treatment</td><td>Plan v(N+1)</td></tr>
          <tr><td>Plan vN</td><td>histology removed</td><td colspan="2"><span style="color:var(--red);font-weight:600;">ILLEGAL — ValueError, CHARTER §15.2 C7</span></td></tr>
        </tbody>
      </table>
      <p class="info-text">
        The previous plan <strong>is not mutated</strong> — a deep copy is
        returned with <code>superseded_by</code> filled in. The caller (CLI
        or EHR) decides what to do with both versions. Per CHARTER §10.2,
        the older version is kept indefinitely.
      </p>
      <div class="callout callout-good">
        <strong>What triggers a new plan:</strong> any change to one of the
        ~30 structured fields — new biomarkers (del(17p) detected), new stage
        (ECOG 1 → 3), new findings (bulky disease on restaging), new infectious
        flags (HBV reactivation), pregnancy detected. Changes to the
        <code>clinical_record</code> free-text do <strong>not</strong> trigger
        regeneration (the engine does not read free text).
      </div>
    </div>

    <div class="info-section">
      <h2>7. What else we do</h2>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">{n_workups}</div>
          <div class="num-lbl">Diagnostic workups</div>
          <p class="num-text">
            Pre-biopsy mode: when histology is missing, the engine emits a
            <strong>Workup Brief</strong> with the test list, biopsy approach,
            IHC panel, and triage MDT roles. Per CHARTER §15.2 C7, no
            treatment Plan is generated without histology.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">MDT</div>
          <div class="num-lbl">Multidisciplinary brief</div>
          <p class="num-text">
            The orchestrator reads the Plan + profile and assigns required /
            recommended / optional roles ({n_skills} catalog), formulates open
            questions (Q1–Q6 + DQ1–DQ4), and builds the decision-provenance
            graph.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">stats</div>
          <div class="num-lbl">KB dashboard</div>
          <p class="num-text">
            <code>python -m knowledge_base.stats</code> — actual entity counts
            + per-disease coverage matrix + reviewer sign-off ratio. Available
            as CLI / JSON / embeddable HTML widget for the landing page.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">render</div>
          <div class="num-lbl">A4 print-friendly HTML</div>
          <p class="num-text">
            Single-file HTML with embedded CSS, no external assets beyond
            Google Fonts. Adapts to A4 print via <code>@page</code> and
            <code>@media print</code>. Tracks are shown side by side; the
            alternative is never hidden (anti automation-bias per
            CHARTER §15.2 C6).
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">trials</div>
          <div class="num-lbl">Experimental options (Phase C — done)</div>
          <p class="num-text">
            <code>enumerate_experimental_options(...)</code> queries
            ClinicalTrials.gov v2 by disease + biomarker + line_of_therapy
            and returns <code>ExperimentalOption</code> entries with
            UA-availability metadata (sites_ua, countries) — render-time
            only; the engine never uses a trial as a selection signal.
            Status filter: RECRUITING / ACTIVE_NOT_RECRUITING /
            ENROLLING_BY_INVITATION; integrated into <code>generate_plan</code>,
            rendered as a third Plan track; 7-day on-disk TTL cache for
            offline runs.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">access</div>
          <div class="num-lbl">Access Matrix (Phase D)</div>
          <p class="num-text">
            Every Plan carries an <code>AccessMatrix</code> — per-track
            aggregation of UA registration, НСЗУ coverage, ₴ cost
            orientation, and primary <code>AccessPathway</code>. Render-time
            only (CHARTER §8.3, guaranteed by the invariant test). Stale-cost
            warning fires when <code>cost_last_updated</code> &gt; 180 days.
            Trial rows are appended automatically when the experimental
            track is active.
          </p>
        </div>
      </div>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    No real patient data · CHARTER §9.3.
    Informational tool for clinicians, not a medical device (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


# ── Diseases coverage page ────────────────────────────────────────────────


def _build_disease_coverage_rows() -> list[dict]:
    """Bridge to scripts/disease_coverage_matrix.py — re-uses its
    per_disease_metrics walker so the page + the JSON snapshot + the
    plan markdown all share one source of truth."""
    from scripts.disease_coverage_matrix import per_disease_metrics
    return per_disease_metrics(REPO_ROOT / "knowledge_base" / "hosted" / "content")


_DISEASES_PAGE_LABELS = {
    "uk": {
        "title": "Хвороби · OpenOnco",
        "h1": "Хвороби в базі знань",
        "lead": (
            "Покриття OpenOnco по 65 онкологічних діагнозах: біомаркери, "
            "препарати, indications/regimens/RedFlags, наявність алгоритму та "
            "опитувальника, % наповненості і % верифікації Clinical Co-Lead."
        ),
        "sum_diseases": "Усього діагнозів",
        "sum_avg_fill": "Сер. наповненість",
        "sum_avg_ver": "Сер. верифікація",
        "sum_with_signed": "З ≥1 верифікованим indication",
        "sum_quest_real": "Hand-authored questionnaires",
        "sum_quest_stub": "STUB questionnaires",
        "sum_algo_1l": "З 1L алгоритмом",
        "sum_algo_2l": "З 2L+ алгоритмом",
        "fam_lymphoid": "Лімфоїдна гематологія",
        "fam_myeloid": "Мієлоїдна гематологія",
        "fam_solid": "Солідні пухлини",
        "th_disease": "Хвороба", "th_icd": "ICD-10",
        "th_bio": "Bio", "th_drug": "Drug",
        "th_ind": "Ind", "th_reg": "Reg", "th_rf": "RF",
        "th_1l": "1L", "th_2l": "2L", "th_quest": "Quest",
        "th_fill": "Fill %", "th_ver": "Ver %",
        "yes": "✓", "no": "—",
        "metrics_title": "Метрики",
        "metrics": [
            "<b>#Bio</b> — distinct biomarkers, на які посилаються Indications + Regimens цієї хвороби",
            "<b>#Drug</b> — distinct drugs у regimens цієї хвороби",
            "<b>#Ind / #Reg / #RF</b> — Indications / Regimens / RedFlags для цієї хвороби",
            "<b>1L / 2L</b> — наявність Algorithm для першої / другої+ лінії",
            "<b>Quest</b> — ✓ hand-authored / STUB auto-generated / — відсутній",
            "<b>Fill %</b> — composite з 8 ентити-типів: ≥1 indication, ≥1 regimen, ≥1 biomarker, ≥1 drug, ≥1 redflag, 1L algo, questionnaire, workup",
            "<b>Ver %</b> — % indications цієї хвороби з reviewer_signoffs ≥ 2 (CHARTER §6.1)",
        ],
        "verified_note": (
            "<b>Ver % переважно 0%</b> — діє dev-mode signoff exemption "
            "(<code>project_charter_dev_mode_exemptions</code>) до призначення "
            "Clinical Co-Leads. Це навмисно, не bug."
        ),
        "footer_data": "Дані оновлюються при кожному build_site.py запуску. JSON snapshot:",
    },
    "en": {
        "title": "Diseases · OpenOnco",
        "h1": "Diseases in the Knowledge Base",
        "lead": (
            "OpenOnco coverage across 65 oncology diagnoses: biomarkers, "
            "drugs, indications/regimens/RedFlags, algorithm and questionnaire "
            "presence, % fill and % Clinical Co-Lead verification."
        ),
        "sum_diseases": "Total diseases",
        "sum_avg_fill": "Avg fill",
        "sum_avg_ver": "Avg verified",
        "sum_with_signed": "With ≥1 verified indication",
        "sum_quest_real": "Hand-authored questionnaires",
        "sum_quest_stub": "STUB questionnaires",
        "sum_algo_1l": "With 1L algorithm",
        "sum_algo_2l": "With 2L+ algorithm",
        "fam_lymphoid": "Lymphoid hematologic",
        "fam_myeloid": "Myeloid hematologic",
        "fam_solid": "Solid tumors",
        "th_disease": "Disease", "th_icd": "ICD-10",
        "th_bio": "Bio", "th_drug": "Drug",
        "th_ind": "Ind", "th_reg": "Reg", "th_rf": "RF",
        "th_1l": "1L", "th_2l": "2L", "th_quest": "Quest",
        "th_fill": "Fill %", "th_ver": "Ver %",
        "yes": "✓", "no": "—",
        "metrics_title": "Metric definitions",
        "metrics": [
            "<b>#Bio</b> — distinct biomarkers referenced by this disease's Indications + Regimens",
            "<b>#Drug</b> — distinct drugs in this disease's regimens",
            "<b>#Ind / #Reg / #RF</b> — Indications / Regimens / RedFlags for this disease",
            "<b>1L / 2L</b> — Algorithm presence for first-line / second-line+",
            "<b>Quest</b> — ✓ hand-authored / STUB auto-generated / — absent",
            "<b>Fill %</b> — composite over 8 entity types: ≥1 indication, ≥1 regimen, ≥1 biomarker, ≥1 drug, ≥1 redflag, 1L algo, questionnaire, workup",
            "<b>Ver %</b> — % of this disease's indications with reviewer_signoffs ≥ 2 (CHARTER §6.1)",
        ],
        "verified_note": (
            "<b>Ver % is mostly 0%</b> — dev-mode signoff exemption "
            "(<code>project_charter_dev_mode_exemptions</code>) is in effect "
            "until Clinical Co-Leads are appointed. This is intentional, not a bug."
        ),
        "footer_data": "Data refreshes on every build_site.py run. JSON snapshot:",
    },
}


def _disease_row_html(r: dict, lbl: dict) -> str:
    yes, no = lbl["yes"], lbl["no"]
    algo_1l = yes if r["algo_1l"] else no
    algo_2l = yes if r["algo_2l"] else no
    if r["has_quest"]:
        quest = "STUB" if r["is_stub_quest"] else yes
    else:
        quest = no
    fill_class = "fill-high" if r["fill_pct"] >= 75 else ("fill-mid" if r["fill_pct"] >= 50 else "fill-low")
    ver_class = "ver-high" if r["verified_pct"] >= 60 else ("ver-mid" if r["verified_pct"] >= 1 else "ver-low")
    short_id = r["id"].replace("DIS-", "")
    name = (r["name"] or "")[:48]
    return (
        '<tr>'
        f'<td><strong>{html.escape(short_id)}</strong> <span class="dis-name">{html.escape(name)}</span></td>'
        f'<td class="mono">{html.escape(r["icd10"] or "")}</td>'
        f'<td class="num">{r["n_bios"]}</td>'
        f'<td class="num">{r["n_drugs"]}</td>'
        f'<td class="num">{r["n_inds"]}</td>'
        f'<td class="num">{r["n_regs"]}</td>'
        f'<td class="num">{r["n_rfs"]}</td>'
        f'<td class="ck">{algo_1l}</td>'
        f'<td class="ck">{algo_2l}</td>'
        f'<td class="ck quest-cell quest-{("stub" if r["is_stub_quest"] else "real" if r["has_quest"] else "none")}">{quest}</td>'
        f'<td class="num pct {fill_class}"><strong>{r["fill_pct"]}%</strong></td>'
        f'<td class="num pct {ver_class}">{r["verified_pct"]}%</td>'
        '</tr>'
    )


def render_diseases(stats, *, target_lang: str = "uk") -> str:
    """Per-disease coverage page. Pulls live metrics from
    disease_coverage_matrix.per_disease_metrics so this page is the
    canonical UI surface for the same data exported as
    /disease_coverage.json."""
    import html as _html
    rows = _build_disease_coverage_rows()
    lbl = _DISEASES_PAGE_LABELS.get(target_lang, _DISEASES_PAGE_LABELS["uk"])

    n = len(rows)
    avg_fill = round(sum(r["fill_pct"] for r in rows) / max(1, n), 1)
    avg_ver = round(sum(r["verified_pct"] for r in rows) / max(1, n), 1)
    n_signed = sum(1 for r in rows if r["verified_pct"] > 0)
    n_quest_real = sum(1 for r in rows if r["has_quest"] and not r["is_stub_quest"])
    n_quest_stub = sum(1 for r in rows if r["has_quest"] and r["is_stub_quest"])
    n_algo_1l = sum(1 for r in rows if r["algo_1l"])
    n_algo_2l = sum(1 for r in rows if r["algo_2l"])

    # Group by family
    by_family: dict[str, list[dict]] = {
        "Лімфоїдна гематологія": [],
        "Мієлоїдна гематологія": [],
        "Солідні пухлини": [],
    }
    for r in rows:
        by_family.setdefault(r["family"], []).append(r)

    fam_label_map = {
        "Лімфоїдна гематологія": lbl["fam_lymphoid"],
        "Мієлоїдна гематологія": lbl["fam_myeloid"],
        "Солідні пухлини": lbl["fam_solid"],
    }

    family_blocks: list[str] = []
    for fam_key in ("Лімфоїдна гематологія", "Мієлоїдна гематологія", "Солідні пухлини"):
        flist = by_family.get(fam_key) or []
        if not flist:
            continue
        flist_sorted = sorted(flist, key=lambda x: (-x["fill_pct"], x["name"]))
        rows_html = "\n".join(_disease_row_html(r, lbl) for r in flist_sorted)
        f_fill = round(sum(r["fill_pct"] for r in flist) / max(1, len(flist)), 1)
        f_ver = round(sum(r["verified_pct"] for r in flist) / max(1, len(flist)), 1)
        family_blocks.append(f"""
<section class="dis-family">
  <h2>{fam_label_map[fam_key]} <span class="fam-count">({len(flist)})</span></h2>
  <table class="dis-table">
    <thead><tr>
      <th class="th-disease">{lbl["th_disease"]}</th>
      <th>{lbl["th_icd"]}</th>
      <th class="th-num">{lbl["th_bio"]}</th>
      <th class="th-num">{lbl["th_drug"]}</th>
      <th class="th-num">{lbl["th_ind"]}</th>
      <th class="th-num">{lbl["th_reg"]}</th>
      <th class="th-num">{lbl["th_rf"]}</th>
      <th class="th-ck">{lbl["th_1l"]}</th>
      <th class="th-ck">{lbl["th_2l"]}</th>
      <th class="th-ck">{lbl["th_quest"]}</th>
      <th class="th-num">{lbl["th_fill"]}</th>
      <th class="th-num">{lbl["th_ver"]}</th>
    </tr></thead>
    <tbody>
{rows_html}
    </tbody>
    <tfoot><tr>
      <td colspan="10"><em>avg</em></td>
      <td class="num pct"><em>{f_fill}%</em></td>
      <td class="num pct"><em>{f_ver}%</em></td>
    </tr></tfoot>
  </table>
</section>
""")

    metrics_li = "\n".join(f"<li>{m}</li>" for m in lbl["metrics"])

    top_bar = _render_top_bar(
        active="diseases", target_lang=target_lang,
        lang_switch_href=_lang_switch_href("diseases", target_lang),
    )

    return f"""<!DOCTYPE html>
<html lang="{target_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_html.escape(lbl['title'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
<style>
.dis-summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0 24px; }}
.dis-summary .card {{ background: var(--gray-50); border-left: 3px solid var(--green-600); padding: 10px 14px; border-radius: 4px; }}
.dis-summary .card .v {{ font-family: var(--font-display); font-size: 22px; color: var(--green-800); }}
.dis-summary .card .k {{ font-size: 12px; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.5px; }}
.dis-family {{ margin: 28px 0; }}
.dis-family h2 {{ margin-bottom: 8px; }}
.dis-family .fam-count {{ font-size: 14px; color: var(--gray-500); font-weight: normal; }}
.dis-table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
.dis-table th {{ background: var(--green-700); color: white; padding: 6px 8px; text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.4px; }}
.dis-table td {{ padding: 6px 8px; border-bottom: 1px solid var(--gray-100); vertical-align: top; }}
.dis-table tr:nth-child(even) td {{ background: var(--gray-50); }}
.dis-table tfoot td {{ background: var(--gray-100); font-style: italic; color: var(--gray-700); }}
.dis-table .num {{ text-align: right; font-family: var(--font-mono); }}
.dis-table .ck {{ text-align: center; }}
.dis-table .mono {{ font-family: var(--font-mono); font-size: 11px; color: var(--gray-500); }}
.dis-table .dis-name {{ color: var(--gray-700); font-weight: normal; }}
.dis-table .pct {{ font-weight: 600; }}
.dis-table .pct.fill-high {{ color: #166534; }}
.dis-table .pct.fill-mid {{ color: #b45309; }}
.dis-table .pct.fill-low {{ color: #991b1b; }}
.dis-table .pct.ver-high {{ color: #166534; background: #ecfdf5; }}
.dis-table .pct.ver-mid {{ color: #b45309; }}
.dis-table .pct.ver-low {{ color: var(--gray-500); }}
.quest-cell.quest-stub {{ color: #b45309; font-size: 10px; font-family: var(--font-mono); }}
.quest-cell.quest-real {{ color: #166534; font-weight: 600; }}
.quest-cell.quest-none {{ color: var(--gray-500); }}
.dis-metrics {{ background: var(--gray-50); padding: 16px 20px; border-radius: 6px; margin-top: 28px; font-size: 13px; }}
.dis-metrics ul {{ padding-left: 20px; line-height: 1.7; }}
.dis-metrics .verified-note {{ background: #fef3c7; border-left: 3px solid #d97706; padding: 10px 14px; margin-top: 12px; border-radius: 4px; color: #92400e; }}
.dis-footer-data {{ font-size: 12px; color: var(--gray-500); margin-top: 20px; }}
.dis-footer-data a {{ font-family: var(--font-mono); }}
@media (max-width: 800px) {{ .dis-summary {{ grid-template-columns: repeat(2, 1fr); }} .dis-table {{ font-size: 11px; }} }}
</style>
</head>
<body>
{top_bar}
<main>
  <section class="info-page">
    <h1>{_html.escape(lbl['h1'])}</h1>
    <p class="lead">{_html.escape(lbl['lead'])}</p>

    <div class="dis-summary">
      <div class="card"><div class="k">{lbl['sum_diseases']}</div><div class="v">{n}</div></div>
      <div class="card"><div class="k">{lbl['sum_avg_fill']}</div><div class="v">{avg_fill}%</div></div>
      <div class="card"><div class="k">{lbl['sum_avg_ver']}</div><div class="v">{avg_ver}%</div></div>
      <div class="card"><div class="k">{lbl['sum_with_signed']}</div><div class="v">{n_signed}/{n}</div></div>
      <div class="card"><div class="k">{lbl['sum_quest_real']}</div><div class="v">{n_quest_real}</div></div>
      <div class="card"><div class="k">{lbl['sum_quest_stub']}</div><div class="v">{n_quest_stub}</div></div>
      <div class="card"><div class="k">{lbl['sum_algo_1l']}</div><div class="v">{n_algo_1l}/{n}</div></div>
      <div class="card"><div class="k">{lbl['sum_algo_2l']}</div><div class="v">{n_algo_2l}/{n}</div></div>
    </div>

    {''.join(family_blocks)}

    <div class="dis-metrics">
      <h3>{lbl['metrics_title']}</h3>
      <ul>
        {metrics_li}
      </ul>
      <div class="verified-note">{lbl['verified_note']}</div>
    </div>

    <p class="dis-footer-data">{lbl['footer_data']} <a href="/disease_coverage.json">/disease_coverage.json</a></p>
  </section>
</main>
</body>
</html>
"""


def bundle_disease_coverage(output_dir: Path) -> dict:
    """Write JSON snapshot of per-disease coverage for CI / external tooling.
    Same source data as the /diseases.html page."""
    rows = _build_disease_coverage_rows()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_diseases": len(rows),
        "rows": rows,
    }
    out = output_dir / "disease_coverage.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"path": "disease_coverage.json", "count": len(rows)}


# ── Limitations page ──────────────────────────────────────────────────────


def render_limitations(stats, *, target_lang: str = "uk") -> str:
    if target_lang == "en":
        return _render_limitations_en(stats)
    return _render_limitations_uk(stats)


def _render_limitations_uk(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_redflags = by_type.get("redflags", 0)
    diseases_full = sum(1 for d in stats.diseases if d.coverage_status in {"stub_full_chain", "reviewed"})
    cov = _coverage_breakdown()
    n_heme = cov["heme_diseases"]
    n_solid = cov["solid_diseases"]
    n_inds_1l = cov["indications_1l"]
    n_inds_2l = cov["indications_2l_plus"]
    n_dis_2l = cov["diseases_with_2l_plus"]
    n_dis_2l_heme = cov["diseases_with_2l_plus_heme"]
    n_dis_2l_solid = cov["diseases_with_2l_plus_solid"]
    heme_2l_list = cov["diseases_2l_heme_list"]
    solid_2l_list = cov["diseases_2l_solid_list"]
    solid_disease_list = cov["solid_disease_list"]

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Обмеження</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="limitations", target_lang="uk", lang_switch_href=_lang_switch_href("limitations", "uk"))}

<main>
  <section class="info-page">
    <h1>Обмеження</h1>
    <p class="lead">
      OpenOnco свідомо не намагається замінити лікаря або повноцінну
      MDT-команду. Цей розділ — повний і чесний список того, що engine
      <strong>не робить</strong>, де він <strong>відмовляється</strong>
      генерувати план без додаткових даних, і де клінічне рішення
      залишається за лікарем. Знати обмеження так само важливо, як
      знати можливості.
    </p>

    <div class="callout callout-hard">
      <strong>STUB-статус усього клінічного контенту.</strong>
      Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
      (CHARTER §6.1 вимагає двох Clinical Co-Lead approvals для будь-якої
      Indication, перш ніж її можна вважати «published»). Зараз весь контент
      — STUB. Це інструмент демонстрації архітектури, не клінічна довідка
      для реальних пацієнтів. Стан станом на <code>{stats.generated_at_utc}</code>.
    </div>

    <div class="info-section">
      <h2>1. Виявлення відсутніх даних — Open Questions механізм</h2>
      <p class="info-text">
        Engine <strong>не приймає рішення без потрібних даних</strong>. Замість
        того, щоб мовчки brati default, він явно фіксує які поля бракує і
        якого тесту/висновку потребує. Цей механізм називається
        <strong>Open Questions</strong> і він — цілеспрямована частина
        MDT-orchestrator (Q1-Q6 + DQ1-DQ4 rules per MDT_ORCHESTRATOR_SPEC §3).
      </p>
      <div class="q-list">
        <h4>Treatment-mode Open Questions (Q1-Q6) — приклади з реального коду</h4>
        <ul>
          <li><strong>Q1 — Histology not confirmed:</strong> якщо <code>disease.id</code> резолвиться але немає <code>biopsy_date</code> чи <code>histology_report</code> — engine emits warning «Treatment Plan generated against ICD-O-3 code only; recommend confirming primary histology before initiating therapy».</li>
          <li><strong>Q2 — Stage missing:</strong> якщо Algorithm.decision_tree посилається на staging але profile немає <code>stage</code> — fall-through на default з flag «Lugano/Ann Arbor stage required for confident risk-stratification».</li>
          <li><strong>Q3 — RedFlag clause references findings absent:</strong> якщо <code>RF-MM-HIGH-RISK-CYTOGENETICS</code> перевіряє <code>tp53_mutation</code> + <code>del_17p</code> + <code>t_4_14</code> + <code>gain_1q</code>, а в profile є тільки <code>del_17p</code> — engine не дає false negative; emits «Cytogenetic panel incomplete; high-risk status assessed with partial data».</li>
          <li><strong>Q4 — Biomarker required by Indication missing:</strong> якщо <code>IND-CLL-1L-VENO</code> вимагає <code>BIO-CLL-HIGH-RISK-GENETICS</code> для default-track selection — engine emits «IGHV mutation status + FISH del(17p) required to confirm 1L recommendation».</li>
          <li><strong>Q5 — Performance status missing:</strong> якщо <code>ecog</code> відсутній — fall на conservative default (тільки standard track), emits «ECOG performance status required for transplant-eligibility assessment».</li>
          <li><strong>Q6 — Drug availability flag:</strong> якщо selected Regimen містить препарат позначений як <code>nszu_reimbursement: false</code> (наприклад daratumumab у MM) — emits «D-VRd: daratumumab not currently NSZU-reimbursed in Ukraine; verify funding pathway before initiation».</li>
        </ul>
      </div>
      <div class="q-list">
        <h4>Diagnostic-mode Open Questions (DQ1-DQ4) — для pre-biopsy режиму</h4>
        <ul>
          <li><strong>DQ1 — Tissue location missing:</strong> якщо <code>suspicion.tissue_locations</code> empty — workup match не може ranжувати, emits «Тип ткани локалізації потрібно вказати для матчингу workup».</li>
          <li><strong>DQ2 — Lineage hint absent:</strong> без <code>lineage_hint</code> engine використовує тільки tissue + presentation для matching, lower confidence.</li>
          <li><strong>DQ3 — Presentation free-text empty:</strong> presentation_keywords scoring × 0; only lineage + tissue brati участь.</li>
          <li><strong>DQ4 — Working hypotheses not provided:</strong> engine не має preferred direction, переважає найбільш generic workup (наприклад <code>WORKUP-LYMPHADENOPATHY-NONSPECIFIC</code> замість <code>WORKUP-SUSPECTED-LYMPHOMA</code>).</li>
        </ul>
      </div>
      <div class="callout">
        <strong>Чому не «беремо default тихо»:</strong> CHARTER §15.2 C6 (anti
        automation-bias) — engine не може робити вигляд що знає коли не знає.
        Кожна missing-data ситуація має бути візуально помітна лікарю.
        Open Questions рендеряться у Plan як окрема section, не сховано.
      </div>
    </div>

    <div class="info-section">
      <h2>2. П'ять gap-ів персоналізації</h2>
      <p class="info-text">
        «Персоналізація» в OpenOnco — це rule-based <strong>вибір з фіксованих
        варіантів</strong>, а не AI-генерація. Цe навмисна архітектурна позиція
        (CHARTER §8.3 — заборонені prompt patterns). Конкретні gap-и:
      </p>
      <div class="gap-grid">
        <div class="gap-card">
          <div class="gap-tag">Gap 1</div>
          <h3>Без per-patient dose calculation</h3>
          <p>
            Regimen зберігає <strong>стандартну дозу</strong> (<code>bortezomib 1.3 mg/m²</code>),
            не множиться на BSA пацієнта і не зменшується під CrCl 30 мл/хв
            автоматично. Лікар сам перераховує. Це принципово, щоб уникнути
            класифікації як FDA medical device.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 2</div>
          <h3>Без response-adapted cycle adjustment</h3>
          <p>
            Regimen фіксує <code>total_cycles: 6 + 2 maintenance</code>.
            Engine не адаптується автоматично на основі response (PR vs CR
            після PET2). Re-staging plan генерується через окремий
            <code>revise_plan</code> з новим profile — лікар явно тригерить.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 3</div>
          <h3>Genomic matching обмежений curated biomarkers</h3>
          <p>
            Якщо у пацієнта виявили PD-L1 78%, engine не запропонує pembrolizumab —
            бо немає Indication з відповідним biomarker_requirement у KB.
            Це обмеження coverage (треба додати entity), не engine-логіки.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 4</div>
          <h3>SupportiveCare однакова для всіх на одному режимі</h3>
          <p>
            PJP prophylaxis attached до D-VRd для всіх — навіть для пацієнта
            з алергією на bactrim. Engine не знає альтернатив (dapsone замість
            bactrim). Лікар сам substitute'ить.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 5</div>
          <h3>Без cumulative-toxicity tracking між lines</h3>
          <p>
            2L+ алгоритми вже існують для {n_dis_2l} гематологічних хвороб
            ({n_inds_2l} показань 2L+), але profile не carrier'ить
            <code>prior_treatment_history</code> як structured field. 2L plan
            для пацієнта що отримав bortezomib у 1L з grade 2 нейропатією —
            engine не знає про попередній exposure якщо нічого нового не
            вказано; лікар сам інтерпретує prior_lines з вільного тексту.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>3. Жорсткі CHARTER-обмеження (will not change)</h2>
      <p class="info-text">
        Це не technical debt — це принципові архітектурні рішення
        що визначають позицію проекту як non-device CDS і
        gатекіпять FDA / клінічну безпеку.
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §8.3</div>
          <h3>LLM не приймає клінічні рішення</h3>
          <p>
            LLM-и допомагають лише з: boilerplate code, doc drafts,
            extraction з clinical documents (з human verification),
            translation з clinical review. <strong>Не</strong>: вибір
            режиму, генерація доз, інтерпретація biomarker для
            therapy selection.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C7</div>
          <h3>Без histology — без treatment Plan</h3>
          <p>
            Treatment Plan генерується тільки якщо <code>disease.id</code>
            або <code>icd_o_3_morphology</code> підтверджені. Інакше
            engine відмовляється і вмикає DiagnosticPlan mode (workup brief).
            <code>revise_plan</code> з treatment назад в diagnostic —
            <strong>заборонено</strong>, raises ValueError.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C5</div>
          <h3>Без time-critical recommendations</h3>
          <p>
            Engine не призначений для emergency oncology (oncologic
            emergencies, time-sensitive infusion reactions). Це б тригернуло
            device classification. Якщо Indication позначена
            <code>time_critical: true</code> — engine додає disqualification
            warning у FDA compliance.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §6.1</div>
          <h3>Two-reviewer merge для clinical content</h3>
          <p>
            Будь-яка зміна під <code>knowledge_base/hosted/content/</code>
            що affects clinical recommendations потребує два з трьох Clinical
            Co-Lead approvals. Без цього Indication залишається STUB.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C6</div>
          <h3>Anti automation-bias mandatory</h3>
          <p>
            Engine ніколи не показує тільки одну рекомендацію — завжди ≥2
            tracks side-by-side. Alternative не buried, не «click to expand»,
            не fine-print. Лікар бачить що це вибір, не директива.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §9.3</div>
          <h3>Patient data ніколи не у repo / public artifact</h3>
          <p>
            <code>patient_plans/</code> gitignored. Будь-які patient HTML —
            gitignored pattern. Site (<code>docs/</code>) показує тільки
            synthetic examples. Збір telemetry заборонений без explicit consent.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>4. Coverage limits (поточний стан KB)</h2>
      <p class="info-text">
        OpenOnco — work in progress. Зараз модельовано <strong>{n_diseases}
        захворювань</strong> ({n_heme} гематологічних + {n_solid} солідних) —
        це далеко не повний WHO-HAEM5 / WHO Classification of Tumours. Конкретно:
      </p>
      <table class="kv-table">
        <thead><tr><th>Категорія</th><th>Стан</th><th>Що це означає</th></tr></thead>
        <tbody>
          <tr><td>Хвороби з повним ланцюгом</td><td>{diseases_full} / {n_diseases}</td><td>Решта — частково модельовані; engine може видати warning «no Algorithm found for disease=X»</td></tr>
          <tr><td>Indications 1L</td><td>{n_inds_1l}</td><td>Перша лінія покрита для всіх {n_diseases} хвороб</td></tr>
          <tr><td>Indications 2L+</td><td>{n_inds_2l}</td><td>Друга-четверта лінія: {n_dis_2l_heme} гематологічних хвороб ({heme_2l_list}) + {n_dis_2l_solid} солідних ({solid_2l_list}). Решта solid-tumor 2L+ — частково (CRC, breast, urothelial), не systematically.</td></tr>
          <tr><td>RedFlags</td><td>{n_redflags}</td><td>Cover критичні clinical scenarios для існуючих хвороб; для нових disease треба додавати</td></tr>
          <tr><td>Solid tumors</td><td>{n_solid}</td><td>{solid_disease_list} — переважно 1L. 2L+ і ад'ювантні контексти — частково.</td></tr>
          <tr><td>Pediatric oncology</td><td>0</td><td>Out of scope for MVP — окремий track спеціалізації</td></tr>
          <tr><td>Радіотерапія планів</td><td>частково</td><td>RT входить у мультимодальні Indications (cervical CRT, GBM Stupp, PMBCL R-CHOP+RT, esophageal CROSS), але як окрема сутність з технічними параметрами (доза/фракції/target volumes) ще не моделюється</td></tr>
          <tr><td>Хірургія планів</td><td>не модельовано</td><td>Surgical oncology indications відсутні</td></tr>
          <tr><td>Маркетингових даних доступу до режимів (НСЗУ formulary live)</td><td>статичний flag</td><td>Поки що hard-coded на режимах; не auto-refresh з НСЗУ — це окремий backlog item</td></tr>
          <tr><td>Experimental options (clinical trials)</td><td>integrated</td><td>Phase C done: <code>enumerate_experimental_options</code> + ExperimentalOption schema, інтеграція у <code>generate_plan</code>, render третього треку, 7-day on-disk TTL cache. Що ще: курований мапінг trials ↔ patient-eligibility (а не лише disease+biomarker)</td></tr>
          <tr><td>Access Matrix (UA-availability per Plan)</td><td>integrated</td><td>Phase D: <code>AccessMatrix</code> + <code>AccessMatrixRow</code> агрегують registered/НСЗУ/cost/pathway по треках, рендеряться у Plan. Що ще: curated <code>AccessPathway</code> seed (~30 препаратів) — потребує two-reviewer signoff per CHARTER §6.1</td></tr>
        </tbody>
      </table>
      <div class="callout">
        <strong>Що НЕ означає STUB:</strong> structured data + algorithm logic
        + sources вже є. Що STUB означає: <strong>не пройшло dual sign-off
        Clinical Co-Lead</strong>. Тобто фактично ми маємо «proposed plan»
        який треба перевірити, не «approved plan».
      </div>
    </div>

    <div class="info-section">
      <h2>5. Що engine ніколи не робить</h2>
      <p class="info-text">
        Прозорий список заборонених patterns — щоб усі знали межі:
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не сховує alternative track</h3>
          <p>Обидві рекомендації завжди показані. UI не has «expand to see alternative» pattern.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не генерує нову Indication LLM-ом</h3>
          <p>Усе вибирається з уже-curated KB. Якщо немає підходящої Indication — engine emits warning, не «creative invention».</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не модифікує дози «під пацієнта»</h3>
          <p>Дози зі стандартного NCCN/ESMO. Adjustments тільки через explicit dose_modification_rules у Regimen YAML, ніяких ad hoc calculations.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не оцінює «що краще» між tracks</h3>
          <p>Algorithm обирає default, але не вирішує що default «кращий». Лікар має повну autonomy обрати alternative — це задокументовано у automation_bias_warning.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не інтерпретує imaging</h3>
          <p>«Bulky disease» приходить як structured field <code>dominant_nodal_mass_cm</code>, не з аналізу зображень. Image analysis = device classification.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Не робить cohort matching</h3>
          <p>«У базі з N пацієнтів M% обрали X» — це окремий future feature, потребує persisted patient registry + privacy review. Поки що недоступне.</p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>6. Як з цим жити</h2>
      <p class="info-text">
        Цей engine задумано як <strong>підготовку до tumor-board</strong>,
        не заміну. Лікар вводить profile, отримує structured draft з усіма
        sources і open questions, а далі:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">1</div>
          <div class="num-lbl">Перевіряє sources</div>
          <p class="num-text">
            Кожна claim у плані має citation. Лікар може прочитати оригінальний
            NCCN/ESMO/МОЗ розділ і підтвердити що engine не misquote'ить.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">2</div>
          <div class="num-lbl">Заповнює Open Questions</div>
          <p class="num-text">
            Якщо engine emit'ить «cytogenetic panel incomplete» — лікар замовляє
            тест, додає у profile, запускає <code>revise_plan</code>. Plan
            оновлюється, OpenQuestion закривається.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">3</div>
          <div class="num-lbl">Адаптує під пацієнта</div>
          <p class="num-text">
            Дози пере-перевіряє, supportive care substitute'ить за алергіями,
            Ukraine-availability перевіряє вручну. Engine — draft, лікар — final.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">4</div>
          <div class="num-lbl">Tumor board discusses</div>
          <p class="num-text">
            MDT brief показує які ролі activated і які питання відкриті. Це
            structured agenda для board meeting. Decisions з board fixед'аться
            як provenance events.
          </p>
        </div>
      </div>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    Жодних реальних пацієнтських даних · CHARTER §9.3.
    Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


def _render_limitations_en(stats) -> str:
    by_type = {e.type: e.count for e in stats.entities}
    n_diseases = by_type.get("diseases", 0)
    n_indications = by_type.get("indications", 0)
    n_redflags = by_type.get("redflags", 0)
    diseases_full = sum(1 for d in stats.diseases if d.coverage_status in {"stub_full_chain", "reviewed"})
    cov = _coverage_breakdown()
    n_heme = cov["heme_diseases"]
    n_solid = cov["solid_diseases"]
    n_inds_1l = cov["indications_1l"]
    n_inds_2l = cov["indications_2l_plus"]
    n_dis_2l = cov["diseases_with_2l_plus"]
    n_dis_2l_heme = cov["diseases_with_2l_plus_heme"]
    n_dis_2l_solid = cov["diseases_with_2l_plus_solid"]
    heme_2l_list = cov["diseases_2l_heme_list"]
    solid_2l_list = cov["diseases_2l_solid_list"]
    solid_disease_list = cov["solid_disease_list"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Limitations</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="limitations", target_lang="en", lang_switch_href=_lang_switch_href("limitations", "en"))}

<main>
  <section class="info-page">
    <h1>Limitations</h1>
    <p class="lead">
      OpenOnco deliberately does not try to replace a clinician or a full
      MDT. This page is the complete, honest list of what the engine
      <strong>does not do</strong>, where it <strong>refuses</strong> to
      generate a plan without additional data, and where the clinical
      decision stays with the clinician. Knowing the limitations is as
      important as knowing the capabilities.
    </p>

    <div class="callout callout-hard">
      <strong>All clinical content is STUB-status.</strong>
      Reviewer sign-offs ≥ 2: <strong>{stats.reviewer_signoffs_reviewed}/{stats.reviewer_signoffs_total}</strong>
      (CHARTER §6.1 requires two Clinical Co-Lead approvals before any
      Indication can be considered "published"). Right now everything is
      STUB. This is an architecture demo, not a clinical reference for real
      patients. Snapshot as of <code>{stats.generated_at_utc}</code>.
    </div>

    <div class="info-section">
      <h2>1. Detecting missing data — the Open Questions mechanism</h2>
      <p class="info-text">
        The engine <strong>does not make a decision when required data is
        missing</strong>. Instead of silently picking a default, it
        explicitly records which fields are missing and which test or
        finding is needed. This mechanism is called <strong>Open
        Questions</strong> and it is a deliberate part of the MDT
        orchestrator (Q1–Q6 + DQ1–DQ4 rules per
        MDT_ORCHESTRATOR_SPEC §3).
      </p>
      <div class="q-list">
        <h4>Treatment-mode Open Questions (Q1–Q6) — examples from real code</h4>
        <ul>
          <li><strong>Q1 — Histology not confirmed:</strong> if <code>disease.id</code> resolves but there is no <code>biopsy_date</code> or <code>histology_report</code>, the engine emits "Treatment Plan generated against ICD-O-3 code only; recommend confirming primary histology before initiating therapy".</li>
          <li><strong>Q2 — Stage missing:</strong> if Algorithm.decision_tree references staging but the profile has no <code>stage</code>, the walker falls through to default with a flag "Lugano/Ann Arbor stage required for confident risk-stratification".</li>
          <li><strong>Q3 — RedFlag clause references findings absent:</strong> if <code>RF-MM-HIGH-RISK-CYTOGENETICS</code> checks <code>tp53_mutation</code> + <code>del_17p</code> + <code>t_4_14</code> + <code>gain_1q</code> and only <code>del_17p</code> is in the profile, the engine does not produce a false negative; it emits "Cytogenetic panel incomplete; high-risk status assessed with partial data".</li>
          <li><strong>Q4 — Biomarker required by Indication missing:</strong> if <code>IND-CLL-1L-VENO</code> requires <code>BIO-CLL-HIGH-RISK-GENETICS</code> for default-track selection, the engine emits "IGHV mutation status + FISH del(17p) required to confirm 1L recommendation".</li>
          <li><strong>Q5 — Performance status missing:</strong> if <code>ecog</code> is absent, the engine falls back to a conservative default (standard track only) and emits "ECOG performance status required for transplant-eligibility assessment".</li>
          <li><strong>Q6 — Drug availability flag:</strong> if the selected Regimen contains a drug flagged <code>nszu_reimbursement: false</code> (e.g. daratumumab in MM), the engine emits "D-VRd: daratumumab not currently NHSU-reimbursed in Ukraine; verify funding pathway before initiation".</li>
        </ul>
      </div>
      <div class="q-list">
        <h4>Diagnostic-mode Open Questions (DQ1–DQ4) — for pre-biopsy mode</h4>
        <ul>
          <li><strong>DQ1 — Tissue location missing:</strong> if <code>suspicion.tissue_locations</code> is empty, workup matching cannot rank candidates; emits "Tissue location is required to match a workup".</li>
          <li><strong>DQ2 — Lineage hint absent:</strong> without <code>lineage_hint</code> the engine matches on tissue + presentation only, with lower confidence.</li>
          <li><strong>DQ3 — Presentation free-text empty:</strong> presentation_keywords scoring × 0; only lineage + tissue contribute.</li>
          <li><strong>DQ4 — Working hypotheses not provided:</strong> the engine has no preferred direction and prefers the most generic workup (e.g. <code>WORKUP-LYMPHADENOPATHY-NONSPECIFIC</code> over <code>WORKUP-SUSPECTED-LYMPHOMA</code>).</li>
        </ul>
      </div>
      <div class="callout">
        <strong>Why we don't pick defaults silently:</strong> CHARTER §15.2 C6
        (anti automation-bias) — the engine cannot pretend to know what it
        does not know. Every missing-data situation must be visually obvious
        to the clinician. Open Questions are rendered in the Plan as their
        own section, never hidden.
      </div>
    </div>

    <div class="info-section">
      <h2>2. Five personalization gaps</h2>
      <p class="info-text">
        "Personalization" in OpenOnco is rule-based <strong>selection from
        fixed options</strong>, not AI generation. This is an intentional
        architectural stance (CHARTER §8.3 — forbidden prompt patterns).
        The concrete gaps:
      </p>
      <div class="gap-grid">
        <div class="gap-card">
          <div class="gap-tag">Gap 1</div>
          <h3>No per-patient dose calculation</h3>
          <p>
            A Regimen stores the <strong>standard dose</strong>
            (<code>bortezomib 1.3 mg/m²</code>); it is not multiplied by
            patient BSA and not auto-reduced for CrCl &lt; 30 mL/min. The
            clinician recalculates. This is deliberate — it keeps OpenOnco
            out of FDA medical-device classification.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 2</div>
          <h3>No response-adapted cycle adjustment</h3>
          <p>
            A Regimen pins <code>total_cycles: 6 + 2 maintenance</code>.
            The engine does not auto-adapt based on response (PR vs CR
            after PET2). A re-staging plan is generated through a separate
            <code>revise_plan</code> with a new profile — the clinician
            triggers it explicitly.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 3</div>
          <h3>Genomic matching is bounded by curated biomarkers</h3>
          <p>
            If a patient turns up with PD-L1 78%, the engine will not
            propose pembrolizumab — because no Indication with the
            corresponding biomarker_requirement exists in the KB. This is a
            coverage limit (add an entity), not an engine-logic limit.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 4</div>
          <h3>SupportiveCare is uniform per regimen</h3>
          <p>
            PJP prophylaxis is attached to D-VRd for everyone — even for a
            patient allergic to bactrim. The engine does not know about
            alternatives (dapsone instead of bactrim). The clinician
            substitutes.
          </p>
        </div>
        <div class="gap-card">
          <div class="gap-tag">Gap 5</div>
          <h3>No cumulative-toxicity tracking across lines</h3>
          <p>
            2L+ algorithms are now in for {n_dis_2l} hematologic diseases
            ({n_inds_2l} 2L+ indications), but the profile does not yet
            carry <code>prior_treatment_history</code> as a structured
            field. A 2L plan for a patient who received bortezomib in 1L
            with grade 2 neuropathy — the engine does not know about the
            prior exposure unless something new is added; the clinician
            interprets prior_lines from free text.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>3. Hard CHARTER constraints (will not change)</h2>
      <p class="info-text">
        These are not technical debt — they are deliberate architectural
        decisions that establish the project's position as non-device CDS
        and gate FDA / clinical safety.
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §8.3</div>
          <h3>LLMs do not make clinical decisions</h3>
          <p>
            LLMs only assist with: boilerplate code, doc drafts, extraction
            from clinical documents (with human verification), translation
            with clinical review. <strong>Not</strong>: regimen selection,
            dose generation, biomarker interpretation for therapy choice.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C7</div>
          <h3>No histology → no treatment Plan</h3>
          <p>
            A treatment Plan is generated only when <code>disease.id</code>
            or <code>icd_o_3_morphology</code> is confirmed. Otherwise the
            engine refuses and switches to DiagnosticPlan mode (workup
            brief). <code>revise_plan</code> from treatment back to
            diagnostic is <strong>forbidden</strong> and raises ValueError.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C5</div>
          <h3>No time-critical recommendations</h3>
          <p>
            The engine is not designed for emergency oncology (oncologic
            emergencies, time-sensitive infusion reactions). That would
            trigger device classification. If an Indication is flagged
            <code>time_critical: true</code>, the engine adds a
            disqualification warning to FDA compliance.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §6.1</div>
          <h3>Two-reviewer merge for clinical content</h3>
          <p>
            Any change under <code>knowledge_base/hosted/content/</code>
            that affects clinical recommendations needs two of three
            Clinical Co-Lead approvals. Without that, the Indication stays
            STUB.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §15.2 C6</div>
          <h3>Anti automation-bias is mandatory</h3>
          <p>
            The engine never shows a single recommendation — always ≥2
            tracks side by side. The alternative is never buried, never
            "click to expand", never fine-print. The clinician sees this is
            a choice, not a directive.
          </p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">CHARTER §9.3</div>
          <h3>Patient data never in repo / public artifacts</h3>
          <p>
            <code>patient_plans/</code> is gitignored. Any patient HTML
            files are gitignored by pattern. The site (<code>docs/</code>)
            ships only synthetic examples. Telemetry collection is
            forbidden without explicit consent.
          </p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>4. Coverage limits (current KB state)</h2>
      <p class="info-text">
        OpenOnco is a work in progress. <strong>{n_diseases} diseases</strong>
        are currently modeled ({n_heme} hematologic + {n_solid} solid tumors)
        — far short of the full WHO-HAEM5 / WHO Classification of Tumours.
        Specifically:
      </p>
      <table class="kv-table">
        <thead><tr><th>Category</th><th>State</th><th>What it means</th></tr></thead>
        <tbody>
          <tr><td>Diseases with the full chain</td><td>{diseases_full} / {n_diseases}</td><td>The rest are partially modeled; the engine may emit "no Algorithm found for disease=X"</td></tr>
          <tr><td>Indications 1L</td><td>{n_inds_1l}</td><td>First line covered for all {n_diseases} diseases</td></tr>
          <tr><td>Indications 2L+</td><td>{n_inds_2l}</td><td>Second-to-fourth line: {n_dis_2l_heme} hematologic diseases ({heme_2l_list}) + {n_dis_2l_solid} solid ({solid_2l_list}). The rest of solid-tumor 2L+ is partial (CRC, breast, urothelial), not systematic.</td></tr>
          <tr><td>RedFlags</td><td>{n_redflags}</td><td>Cover critical clinical scenarios for existing diseases; new diseases need their own RFs added</td></tr>
          <tr><td>Solid tumors</td><td>{n_solid}</td><td>{solid_disease_list} — mostly 1L. 2L+ and adjuvant contexts are partial.</td></tr>
          <tr><td>Pediatric oncology</td><td>0</td><td>Out of scope for MVP — separate specialization track</td></tr>
          <tr><td>Radiation therapy plans</td><td>partial</td><td>RT is wired into multimodality Indications (cervical CRT, GBM Stupp, PMBCL R-CHOP+RT, esophageal CROSS), but not yet modeled as a separate entity with technical parameters (dose / fractions / target volumes)</td></tr>
          <tr><td>Surgery plans</td><td>not modeled</td><td>Surgical-oncology indications are absent</td></tr>
          <tr><td>Live regimen-availability data (NHSU formulary live feed)</td><td>static flag</td><td>Currently hard-coded on regimens; not auto-refreshed from NHSU — separate backlog item</td></tr>
          <tr><td>Experimental options (clinical trials)</td><td>integrated</td><td>Phase C done: <code>enumerate_experimental_options</code> + ExperimentalOption schema, integrated into <code>generate_plan</code>, third Plan track is rendered, 7-day on-disk TTL cache. Still missing: curated trial ↔ patient-eligibility mapping (not just disease+biomarker)</td></tr>
          <tr><td>Access Matrix (UA-availability per Plan)</td><td>integrated</td><td>Phase D: <code>AccessMatrix</code> + <code>AccessMatrixRow</code> aggregate registered/НСЗУ/cost/pathway across tracks; rendered in Plan. Still missing: a curated <code>AccessPathway</code> seed (~30 drugs) — gated on two-reviewer signoff per CHARTER §6.1</td></tr>
        </tbody>
      </table>
      <div class="callout">
        <strong>What STUB does NOT mean:</strong> the structured data,
        algorithm logic, and sources are already in. What STUB
        <strong>does</strong> mean: <strong>two-of-three Clinical Co-Lead
        sign-off has not happened yet</strong>. So in effect we have a
        "proposed plan" that needs review, not an "approved plan".
      </div>
    </div>

    <div class="info-section">
      <h2>5. What the engine never does</h2>
      <p class="info-text">
        A transparent list of forbidden patterns — so the boundaries are
        clear:
      </p>
      <div class="gap-grid">
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Hide the alternative track</h3>
          <p>Both recommendations are always shown. The UI never has an "expand to see alternative" pattern.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Generate a new Indication via LLM</h3>
          <p>Everything is selected from already-curated KB. If no matching Indication exists, the engine emits a warning — never "creative invention".</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Adjust doses "for the patient"</h3>
          <p>Doses come from standard NCCN/ESMO. Adjustments live only inside explicit dose_modification_rules in the Regimen YAML — no ad-hoc calculations.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Score "which is better" between tracks</h3>
          <p>The Algorithm picks a default but does not declare the default "better". The clinician retains full autonomy to choose the alternative — documented in automation_bias_warning.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Interpret imaging</h3>
          <p>"Bulky disease" arrives as a structured field <code>dominant_nodal_mass_cm</code>, not from image analysis. Image analysis = device classification.</p>
        </div>
        <div class="gap-card gap-hard">
          <div class="gap-tag">Never</div>
          <h3>Cohort matching</h3>
          <p>"In the cohort of N patients, M% picked X" is a future feature requiring a persisted patient registry + privacy review. Not available yet.</p>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>6. How to live with this</h2>
      <p class="info-text">
        This engine is intended as <strong>tumor-board preparation</strong>,
        not a replacement. The clinician inputs a profile, receives a
        structured draft with all sources and open questions, and then:
      </p>
      <div class="num-grid num-grid--rich">
        <div class="num-card">
          <div class="num-big">1</div>
          <div class="num-lbl">Verifies the sources</div>
          <p class="num-text">
            Every claim in the plan carries a citation. The clinician can
            read the original NCCN / ESMO / local-MoH section and confirm
            the engine did not misquote it.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">2</div>
          <div class="num-lbl">Closes Open Questions</div>
          <p class="num-text">
            If the engine flags "cytogenetic panel incomplete", the
            clinician orders the test, adds it to the profile, and runs
            <code>revise_plan</code>. The plan refreshes, the OpenQuestion
            closes.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">3</div>
          <div class="num-lbl">Adapts for the patient</div>
          <p class="num-text">
            Re-checks doses, substitutes supportive care for known
            allergies, manually verifies local-availability constraints.
            The engine produces a draft; the clinician produces the final.
          </p>
        </div>
        <div class="num-card">
          <div class="num-big">4</div>
          <div class="num-lbl">Tumor board discusses</div>
          <p class="num-text">
            The MDT brief shows which roles are activated and which
            questions are open. That is the structured agenda for the board
            meeting. Decisions taken at the board are captured as
            provenance events.
          </p>
        </div>
      </div>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    No real patient data · CHARTER §9.3.
    Informational tool for clinicians, not a medical device (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


# ── Specs page ────────────────────────────────────────────────────────────


_SPECS_CATALOG: list[dict] = [
    {
        "id": "CHARTER",
        "file": "CHARTER.md",
        "title": "Charter та Governance",
        "tag": "governance",
        "summary": (
            "Управління проектом, scope (що проект робить і чого не робить), "
            "FDA non-device CDS positioning (§15 з constraints C1-C7), two-reviewer rule "
            "для clinical content (§6.1), patient-data privacy (§9.3), forbidden prompt "
            "patterns для LLM (§8.3 — LLM не приймає клінічні рішення)."
        ),
    },
    {
        "id": "CLINICAL_CONTENT_STANDARDS",
        "file": "CLINICAL_CONTENT_STANDARDS.md",
        "title": "Clinical Content Standards",
        "tag": "clinical",
        "summary": (
            "Стандарти клінічного контенту: citation format (source_id + position + "
            "paraphrase + page), evidence-level taxonomy (Tier 1-6), reviewer signoff "
            "workflow, STUB → reviewed transition criteria. Кожна claim у Indication / "
            "Regimen / RedFlag має посилання на Source entity."
        ),
    },
    {
        "id": "DATA_STANDARDS",
        "file": "DATA_STANDARDS.md",
        "title": "Data Standards — Patient Model",
        "tag": "data",
        "summary": (
            "Patient profile data model. FHIR R4/R5 + mCODE alignment у плані. "
            "Кодові системи: LOINC + ICD-10/O-3 + RxNorm + CTCAE v5.0. Без SNOMED CT, "
            "без MedDRA у MVP (license gates). Поля профілю та semantic interoperability."
        ),
    },
    {
        "id": "KNOWLEDGE_SCHEMA_SPECIFICATION",
        "file": "KNOWLEDGE_SCHEMA_SPECIFICATION.md",
        "title": "Knowledge Schema Specification",
        "tag": "schema",
        "summary": (
            "Pydantic schemas всіх KB entities — Disease / Indication / Regimen / "
            "Algorithm / Biomarker / Drug / Test / Workup / RedFlag / Contraindication / "
            "MonitoringSchedule / SupportiveCare / Source. Defines fields, validators, "
            "referential integrity rules, migration roadmap до PostgreSQL."
        ),
    },
    {
        "id": "SOURCE_INGESTION_SPEC",
        "file": "SOURCE_INGESTION_SPEC.md",
        "title": "Source Ingestion & Licensing",
        "tag": "sources",
        "summary": (
            "Як інгестимо джерела: hosting matrix (referenced vs hosted vs mixed) з H1-H5 "
            "justification, license classification gates, add-a-source checklist (§8), "
            "hosted-source checklist (§20), SourceClient protocol для live APIs."
        ),
    },
    {
        "id": "REFERENCE_CASE_SPECIFICATION",
        "file": "REFERENCE_CASE_SPECIFICATION.md",
        "title": "Reference Case — \"Patient Zero\"",
        "tag": "testing",
        "summary": (
            "Synthetic HCV-MZL reference case як P0 acceptance test. Defines всі required "
            "fields у patient profile (§2 templates), critical structural assertions для "
            "Plan render output (§1.3), milestones M1-M6 для розширення coverage."
        ),
    },
    {
        "id": "MDT_ORCHESTRATOR_SPEC",
        "file": "MDT_ORCHESTRATOR_SPEC.md",
        "title": "MDT Orchestrator + Decision Provenance",
        "tag": "engine",
        "summary": (
            "Orchestrate_mdt rules (R1-R9 для treatment, D1-D6 для diagnostic), "
            "role activation logic (required / recommended / optional), Open Questions "
            "механізм (Q1-Q6 + DQ1-DQ4 — engine не приймає рішення без потрібних даних), "
            "decision provenance graph для audit-grade explanation."
        ),
    },
    {
        "id": "DIAGNOSTIC_MDT_SPEC",
        "file": "DIAGNOSTIC_MDT_SPEC.md",
        "title": "Diagnostic-Phase MDT (Pre-biopsy)",
        "tag": "engine",
        "summary": (
            "Pre-biopsy режим: коли histology ще немає, engine emit DiagnosticPlan з "
            "workup brief замість treatment Plan. CHARTER §15.2 C7 hard rule. "
            "DiagnosticWorkup + DiagnosticPlan schemas, generate_diagnostic_brief(), "
            "polymorphic orchestrate_mdt з DQ1-DQ4 rules."
        ),
    },
    {
        "id": "WORKUP_METHODOLOGY_SPEC",
        "file": "WORKUP_METHODOLOGY_SPEC.md",
        "title": "Workup Research Methodology",
        "tag": "clinical",
        "summary": (
            "Як ми будуємо basic workup для будь-якої онкологічної області. Source "
            "hierarchy (Tier 1: NCCN/ESMO/EHA/BSH/WHO/ASH), Test/Workup completeness "
            "checklists, 7-step process для нової domain extension, anti-patterns."
        ),
    },
    {
        "id": "SKILL_ARCHITECTURE_SPEC",
        "file": "SKILL_ARCHITECTURE_SPEC.md",
        "title": "Skill-Oriented Architecture (MDT Roles as Skills)",
        "tag": "engine",
        "summary": (
            "Formalізує MDT ролі (гематолог / патолог / радіолог / etc.) як "
            "clinically-verified skills — кожен skill має version, sources, "
            "last_reviewed, clinical_lead. Sizing horizon (~12-15 MVP → 50-60 "
            "comprehensive), 8-domain layout, 5-phase refactor plan."
        ),
    },
]

_SPEC_TAG_LABELS = {
    "governance": "Governance",
    "clinical": "Clinical",
    "data": "Data",
    "schema": "Schema",
    "sources": "Sources",
    "testing": "Testing",
    "engine": "Engine",
}

_SPEC_TAG_COLORS = {
    "governance": "var(--red)",
    "clinical": "var(--green-700)",
    "data": "var(--teal)",
    "schema": "var(--green-600)",
    "sources": "var(--green-700)",
    "testing": "var(--amber)",
    "engine": "var(--green-700)",
}


def render_specs(stats) -> str:
    spec_cards = []
    for sp in _SPECS_CATALOG:
        gh_url = (
            f"https://github.com/{GH_REPO}/blob/master/specs/{sp['file']}"
        )
        raw_url = (
            f"https://raw.githubusercontent.com/{GH_REPO}/master/specs/{sp['file']}"
        )
        color = _SPEC_TAG_COLORS.get(sp["tag"], "var(--gray-500)")
        tag_label = _SPEC_TAG_LABELS.get(sp["tag"], sp["tag"])
        spec_cards.append(f"""
        <div class="spec-card">
          <div class="spec-card-head">
            <span class="spec-tag" style="background:{color}">{tag_label}</span>
            <code class="spec-id">{sp['file']}</code>
          </div>
          <h3>{sp['title']}</h3>
          <p>{sp['summary']}</p>
          <div class="spec-card-foot">
            <a href="{gh_url}" target="_blank" rel="noopener">Read on GitHub →</a>
            <a href="{raw_url}" target="_blank" rel="noopener" class="spec-raw">Raw markdown</a>
          </div>
        </div>
        """)

    cards_html = "".join(spec_cards)
    n_specs = len(_SPECS_CATALOG)

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · Специфікації</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="style.css" rel="stylesheet">
</head>
<body>
{_render_top_bar(active="specs")}

<main>
  <section class="info-page">
    <h1>Специфікації</h1>
    <p class="lead">
      OpenOnco — це specifications-first проект. Кожна архітектурна, клінічна, або
      governance деталь зафіксована у markdown-документі під <code>specs/</code>,
      який підлягає версіонуванню та public review. {n_specs} активних специфікацій
      описують все: від FDA non-device CDS positioning до структури кожної YAML
      entity у KB. Усі тексти живуть у <a href="https://github.com/{GH_REPO}/tree/master/specs"
      target="_blank" rel="noopener">github.com/{GH_REPO}/specs</a>.
    </p>

    <div class="callout">
      <strong>Source-of-truth ієрархія</strong> (з CLAUDE.md): коли специфікації
      конфліктують, обов'язковий порядок: <strong>1.</strong> CHARTER.md →
      <strong>2.</strong> інші <code>specs/*.md</code> → <strong>3.</strong> CLAUDE.md →
      <strong>4.</strong> README.md. Контент під <code>legacy/</code> не authoritative.
    </div>

    <div class="info-section">
      <h2>Активні специфікації ({n_specs})</h2>
      <div class="spec-grid">
        {cards_html}
      </div>
    </div>

    <div class="info-section">
      <h2>Регуляторне джерело (PDF)</h2>
      <div class="spec-card">
        <div class="spec-card-head">
          <span class="spec-tag" style="background:var(--gray-700)">Regulatory PDF</span>
          <code class="spec-id">Guidance-Clinical-Decision-Software_5.pdf</code>
        </div>
        <h3>FDA Clinical Decision Support Software Guidance</h3>
        <p>
          Офіційне керівництво FDA про non-device CDS classification under
          §520(o)(1)(E). Лежить у <code>specs/</code> як hosted PDF. CHARTER §15
          цитує конкретні criteria 1-4 з цього документа для обґрунтування OpenOnco
          positioning як non-device.
        </p>
        <div class="spec-card-foot">
          <a href="https://github.com/{GH_REPO}/blob/master/specs/Guidance-Clinical-Decision-Software_5.pdf"
             target="_blank" rel="noopener">View PDF on GitHub →</a>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h2>Як ми оновлюємо специфікації</h2>
      <p class="info-text">
        Кожна зміна під <code>specs/</code> або <code>knowledge_base/hosted/content/</code>
        що affects clinical recommendations потребує <strong>two-reviewer merge</strong>
        (CHARTER §6.1) — два з трьох Clinical Co-Lead approvals. Це жорстке правило
        gатекіпить якість клінічного контенту. Технічні специфікації (схеми, engine,
        ingestion) можуть merge'итися single-reviewer для прискорення розробки, але
        clinical content — завжди dual sign-off.
      </p>
      <p class="info-text">
        Усі специфікації Ukrainian-first (мова інтерфейсу + клінічних reviewers UA),
        але technical terms та license names залишаються English inline. Версіонування
        — через git: кожна специфікація має <code>v0.1 (draft)</code> у header, bump
        на minor/major залежно від breaking changes.
      </p>
    </div>

    <div class="info-section">
      <h2>Compliance + Privacy (короткий зріз)</h2>
      <table class="kv-table">
        <thead><tr><th>Гарантія</th><th>Specification</th><th>Що це означає</th></tr></thead>
        <tbody>
          <tr>
            <td><strong>FDA non-device CDS</strong></td>
            <td><code>CHARTER.md §15</code></td>
            <td>OpenOnco проектується під §520(o)(1)(E) carve-out — не медичний пристрій. Constraints C1-C7 hard-enforced.</td>
          </tr>
          <tr>
            <td><strong>No patient data</strong></td>
            <td><code>CHARTER.md §9.3</code></td>
            <td><code>patient_plans/</code> + будь-які patient HTML gitignored. Усі examples — synthetic.</td>
          </tr>
          <tr>
            <td><strong>Two-reviewer merge</strong></td>
            <td><code>CHARTER.md §6.1</code></td>
            <td>Clinical content потребує 2 з 3 Clinical Co-Lead approvals; інакше Indication залишається STUB.</td>
          </tr>
          <tr>
            <td><strong>No LLM clinical judgment</strong></td>
            <td><code>CHARTER.md §8.3</code></td>
            <td>LLM не вибирає режими, не генерує дози, не інтерпретує biomarkers для therapy selection.</td>
          </tr>
          <tr>
            <td><strong>No treatment without histology</strong></td>
            <td><code>CHARTER.md §15.2 C7</code></td>
            <td>Engine відмовляється generate'ити treatment Plan без <code>disease.id</code> або <code>icd_o_3_morphology</code>; тільки DiagnosticPlan.</td>
          </tr>
          <tr>
            <td><strong>Anti automation-bias</strong></td>
            <td><code>CHARTER.md §15.2 C6</code></td>
            <td>Завжди показуються ≥2 alternative tracks side-by-side; alternative не сховано.</td>
          </tr>
          <tr>
            <td><strong>Source hosting default = referenced</strong></td>
            <td><code>SOURCE_INGESTION_SPEC.md §1.4</code></td>
            <td>Не дублюємо external бази; hosting потребує explicit H1-H5 justification.</td>
          </tr>
          <tr>
            <td><strong>Free public resource → non-commercial</strong></td>
            <td><code>CHARTER.md §2</code></td>
            <td>Багато ліцензій (ESMO CC-BY-NC-ND, OncoKB academic, ATC) залежать від цього. Paid tier тригернув би license audit.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11).
  </footer>
</main>
</body>
</html>
"""


# ── Build orchestration ───────────────────────────────────────────────────


def _build_one_case_worker(args: tuple) -> dict:
    """Top-level wrapper for ProcessPoolExecutor (must be picklable).
    Returns the dict shape that build_site() collects into case_paths_uk/en."""
    case, output_dir, target_lang = args
    p = build_one_case(case, output_dir, target_lang=target_lang)
    return {
        "case_id": case.case_id,
        "lang": target_lang,
        "path": str(p.relative_to(output_dir)),
    }


def _build_all_cases_parallel(output_dir: Path) -> tuple[list[dict], list[dict]]:
    """Render every CASE × {uk, en} in a process pool.

    Each worker re-imports knowledge_base and reloads the YAML KB once on
    startup, then handles a chunk of cases — so a 4-worker pool amortises
    the import cost across ~50 cases per worker. On Windows (spawn) this
    cuts the 99×2-case build from ~12 min serial to ~2 min on 4 cores.
    """
    import os
    from concurrent.futures import ProcessPoolExecutor

    tasks = [(c, output_dir, "uk") for c in CASES] + \
            [(c, output_dir, "en") for c in CASES]
    n_workers = min(os.cpu_count() or 4, 8)

    if n_workers <= 1 or len(tasks) <= 2:
        results = [_build_one_case_worker(t) for t in tasks]
    else:
        with ProcessPoolExecutor(max_workers=n_workers) as ex:
            results = list(ex.map(_build_one_case_worker, tasks, chunksize=4))

    uk = [r for r in results if r["lang"] == "uk"]
    en = [r for r in results if r["lang"] == "en"]
    return uk, en


def build_one_case(case: CaseEntry, output_dir: Path,
                   *, target_lang: str = "uk") -> Path:
    """Render one case to HTML in `target_lang`. Output path:
    - target_lang='uk' → output_dir/cases/<id>.html
    - target_lang='en' → output_dir/en/cases/<id>.html
    """
    patient_path = EXAMPLES / case.file
    patient = json.loads(patient_path.read_text(encoding="utf-8"))

    if is_diagnostic_profile(patient):
        result = generate_diagnostic_brief(patient, kb_root=KB_ROOT)
        mdt = orchestrate_mdt(patient, result, kb_root=KB_ROOT)
        html = render_diagnostic_brief_html(result, mdt=mdt, target_lang=target_lang)
    else:
        result = generate_plan(
            patient,
            kb_root=KB_ROOT,
            experimental_search_fn=search_trials,
            experimental_cache_root=CTGOV_CACHE,
        )
        mdt = orchestrate_mdt(patient, result, kb_root=KB_ROOT)
        html = render_plan_html(result, mdt=mdt, target_lang=target_lang)

    wrapped = _wrap_case_html(html, case, target_lang=target_lang)
    sub = "en/cases" if target_lang == "en" else "cases"
    out_path = output_dir / sub / f"{case.case_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(wrapped, encoding="utf-8")
    return out_path


def _copy_landing_assets(output_dir: Path) -> list[str]:
    """Copy infographic images used by the landing into docs/. Source-of-truth
    lives in infograph/ (gitignored except these). Listed by name so we don't
    accidentally copy patient HTMLs (CHARTER §9.3)."""
    src_root = REPO_ROOT / "infograph"
    assets = ["MDT.png", "MDT-light.png"]
    copied: list[str] = []
    for name in assets:
        src = src_root / name
        if src.exists():
            shutil.copyfile(src, output_dir / name)
            copied.append(name)
    # favicon.svg lives directly under docs/ (committed) — preserve on --clean
    favicon_src = REPO_ROOT / "docs" / "favicon.svg"
    if favicon_src.exists() and favicon_src.resolve() != (output_dir / "favicon.svg").resolve():
        shutil.copyfile(favicon_src, output_dir / "favicon.svg")
        copied.append("favicon.svg")
    return copied


def build_site(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cases").mkdir(parents=True, exist_ok=True)
    (output_dir / "en").mkdir(parents=True, exist_ok=True)
    (output_dir / "en" / "cases").mkdir(parents=True, exist_ok=True)
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    (output_dir / "style.css").write_text(_STYLE_CSS, encoding="utf-8")
    landing_assets = _copy_landing_assets(output_dir)

    stats = collect_stats()
    stats_widget = format_html_widget(stats, embed_style=True)

    # Build engine bundle FIRST so we can stamp its content-hash into
    # try.html as a cache-buster (?v=<hash>). Without this, GitHub Pages
    # serves the zip with Cache-Control: max-age=600 and users get stale
    # bundles for ~10 minutes after a KB push.
    engine_bundle = bundle_engine(output_dir)
    bundle_version = engine_bundle.get("version", "")
    sw_payload = write_service_worker(
        output_dir, core_version=engine_bundle.get("core_version", ""),
    )

    # Bundle dropdowns BEFORE render_try so /try.html can inline the
    # ~15 KB manifests as JS constants — saves the ~870 KB initial fetch
    # of questionnaires.json + examples.json on first paint.
    examples_payload = bundle_examples(output_dir)
    questionnaires_payload = bundle_questionnaires(output_dir)
    questionnaires_manifest = questionnaires_payload.get("manifest", [])
    examples_manifest = examples_payload.get("manifest", [])

    # ── UA build (default at site root) ──
    (output_dir / "index.html").write_text(render_landing(stats), encoding="utf-8")
    (output_dir / "capabilities.html").write_text(render_capabilities(stats), encoding="utf-8")
    (output_dir / "limitations.html").write_text(render_limitations(stats), encoding="utf-8")
    (output_dir / "specs.html").write_text(render_specs(stats), encoding="utf-8")
    (output_dir / "gallery.html").write_text(render_gallery(stats_widget), encoding="utf-8")
    (output_dir / "diseases.html").write_text(render_diseases(stats), encoding="utf-8")
    (output_dir / "try.html").write_text(
        render_try(
            bundle_version=bundle_version,
            questionnaires_manifest=questionnaires_manifest,
            examples_manifest=examples_manifest,
        ), encoding="utf-8")

    # ── EN build (mirror at /en/) ──
    # Body copy of landing/gallery/try is currently UA — nav + lang attribute
    # + try-CTA labels translated; full EN body copy is a separate workstream.
    # Per-case Plan/Brief HTMLs ARE rendered in EN via target_lang="en" —
    # that's where 80% of the user-facing content lives.
    (output_dir / "en" / "index.html").write_text(
        render_landing(stats, target_lang="en"), encoding="utf-8")
    (output_dir / "en" / "capabilities.html").write_text(
        render_capabilities(stats, target_lang="en"), encoding="utf-8")
    (output_dir / "en" / "limitations.html").write_text(
        render_limitations(stats, target_lang="en"), encoding="utf-8")
    (output_dir / "en" / "gallery.html").write_text(
        render_gallery(stats_widget, target_lang="en"), encoding="utf-8")
    (output_dir / "en" / "diseases.html").write_text(
        render_diseases(stats, target_lang="en"), encoding="utf-8")
    (output_dir / "en" / "try.html").write_text(
        render_try(
            target_lang="en",
            bundle_version=bundle_version,
            questionnaires_manifest=questionnaires_manifest,
            examples_manifest=examples_manifest,
        ), encoding="utf-8")

    case_paths_uk, case_paths_en = _build_all_cases_parallel(output_dir)
    disease_coverage_payload = bundle_disease_coverage(output_dir)

    return {
        "output_dir": str(output_dir),
        "cases_built": len(case_paths_uk) + len(case_paths_en),
        "cases_uk": case_paths_uk,
        "cases_en": case_paths_en,
        "engine_bundle": engine_bundle,
        "service_worker": sw_payload,
        "examples_payload": examples_payload,
        "questionnaires_payload": questionnaires_payload,
        "disease_coverage_payload": disease_coverage_payload,
        "landing_assets": landing_assets,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build OpenOnco static site for GitHub Pages.")
    parser.add_argument("--output", default="docs", help="Output directory (default: docs/)")
    parser.add_argument("--clean", action="store_true", help="Wipe output directory before building.")
    args = parser.parse_args(argv)

    output_dir = (REPO_ROOT / args.output) if not Path(args.output).is_absolute() else Path(args.output)
    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    report = build_site(output_dir)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
