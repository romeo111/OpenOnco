# Development and deployment

## Runtime

Use Python 3.12 (CI runtime), install `requirements.lock`, then `python -m pip install --no-build-isolation --no-deps -e .`. See [README](../README.md) for virtual-environment setup. The optional MCP extra is installed with `python -m pip install -e ".[mcp]"`.

## Verify a change

```bash
python scripts/audit_validator.py --human
python -m pytest tests/test_kb_wiki.py tests/test_site_head_faq.py tests/test_site_discovery.py -q
python -m ruff check --select E9,F63,F7,F82 scripts/ knowledge_base/ serverless/ api/ tests/
```

Run additional tests appropriate to the changed component. The [Validate Knowledge Base workflow](../.github/workflows/validate-kb.yml) also checks examples, executable conditions, DLBCL review contracts and engine regressions. The nightly suite covers a broader selection. A green test run is engineering evidence, not clinical approval.

## Preview and build

```bash
python -m scripts.build_site --output build/site-preview
python -m http.server 8000 --directory build/site-preview
```

This builds into a separate directory. To prepare the published output, use `python -m scripts.build_site --output docs`. Avoid `--clean` against `docs/`: that directory also contains manually authored Markdown and audit artifacts. For metadata-only changes, call `scripts.site_head.finalize_site_discovery(Path("docs"))`; it updates head/discovery assets without rebuilding clinical page bodies. Run discovery tests and inspect the resulting diff.

The shared navigation is in `scripts/site_nav.py`, styles in `scripts/site_header.css`, Wiki in `scripts/build_kb_wiki.py`, Handbook in `scripts/build_handbook.py`, and discovery metadata in `scripts/site_head.py`. Daily rebuilds use the same sources.

### Partial clinical releases

After generating a selected group of clinical pages, finalize that exact group before committing. Create a JSON manifest of relative HTML paths, including every changed original and its translated editions, for example `["cases/example.html", "ukr/cases/example.html", "fi/cases/example.html"]`.

```bash
python -m scripts.finalize_partial_site --output docs --manifest .tmp/release-pages.json
python -m scripts.finalize_partial_site --output docs --manifest .tmp/release-pages.json --write
node tests/browser_translation_cache.cjs
node tests/browser_bundle_versions.cjs
```

The first command is a dry run. Output is normalized to LF line endings, so an initial run can report formatting changes in a Windows checkout. The second applies the verified batch: shared navigation, discovery metadata, the existing versioned geographic-language asset, and reader fingerprints bound to final originals. It validates the whole batch before replacing files, preserves clinical bodies, rejects preserved pages and paths outside the output, and restores already-replaced pages if a write fails. Keep the normal shared header and language assets in the output; this command does not regenerate them. It also does not rebuild engine archives, search indexes, sitemaps or API packages: verify those separately when their source data changes.

The default path inventory comes from committed `docs/` filenames plus the manifest. For a separate preview with additional destinations, pass `--inventory .tmp/preview-paths.json`, a JSON list of available relative HTML paths. Reader originals outside the manifest must be inventoried; they remain unchanged. A synchronized fingerprint proves source identity, not translation accuracy or clinical approval.

## Publish

After deployment, check the eight main public pages in all eleven languages and the additional internal destinations linked from their headers:

```bash
python -m scripts.check_live_navigation --report .tmp/live-navigation.json
```

Use `--base-url http://localhost:8000/` for a locally served preview. The check uses bounded, read-only GET requests, verifies shared headers, language order and flags, document language, canonical links and main landmarks, and fails on broken navigation destinations. Redirects cannot leave the selected website origin. It does not submit cases, call the clinical API, execute JavaScript or prove visual layout, accessibility with assistive technology, or clinical correctness. Create the report directory before running.

GitHub Pages serves branch **`master`**, directory **`/docs`**, at **https://openonco.info/**. Push reviewed generated output and its source changes to the deployment branch through the repository's authorized delivery flow. The standard **pages build and deployment** run must succeed; inspect the live pages afterward. The [Daily Site Refresh](../.github/workflows/daily-site-refresh.yml) rebuilds from current KB content and commits changed output.

The optional question API is a separate deployment; updating GitHub Pages does not configure its secrets or deploy that backend. Keep all credentials outside Git and use synthetic fixtures in demos, screenshots and review packets.

The existing Vercel project is `openonco-vercel-api`, serving `https://openonco-vercel-api.vercel.app/api/clinical-question`. After verification, `python -m scripts.prepare_clinical_api_deploy` creates an isolated package under `.tmp/clinical-api-deploy` containing the API, serverless adapter and public knowledge base; it excludes website pages and translation models. Link that directory to the existing project and deploy with the authenticated Vercel CLI. Do not create a replacement project or copy secrets into source files. Verify an empty synthetic request after deployment; it must return a localized clarification without calling the model provider.
