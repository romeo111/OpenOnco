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

## Publish

GitHub Pages serves branch **`master`**, directory **`/docs`**, at **https://openonco.info/**. Push reviewed generated output and its source changes to the deployment branch through the repository's authorized delivery flow. The standard **pages build and deployment** run must succeed; inspect the live pages afterward. The [Daily Site Refresh](../.github/workflows/daily-site-refresh.yml) rebuilds from current KB content and commits changed output.

The optional question API is a separate deployment; updating GitHub Pages does not configure its secrets or deploy that backend. Keep all credentials outside Git and use synthetic fixtures in demos, screenshots and review packets.
