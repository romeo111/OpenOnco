# News section — authoring and comment setup

## Writing a post

One YAML file per post in `content/news/`, named `YYYY-MM-DD-slug.yaml`.
Posts are bilingual: both `en` and `uk` are required, and the build fails if
either is missing. Newest post sorts first automatically.

```yaml
slug: my-post                 # lowercase kebab-case, unique, becomes the URL
date: 2026-07-19              # unquoted ISO date
author: OpenOnco
tags: [knowledge-base]

title:
  en: Title in English
  uk: Заголовок українською
summary:
  en: One or two sentences. Also used as the meta description and OG description.
  uk: Одне-два речення. Також використовується як meta description.

body:
  en:
    - type: p
      text: A paragraph.
    - type: h2
      text: A heading
    - type: ul
      items: [First item, Second item]
    - type: callout
      tone: warn                # info (default) | good | warn
      text: Something to flag.
  uk:
    - type: p
      text: Абзац.
```

Block types: `p`, `h2`, `h3`, `ul`, `ol`, `quote`, `callout`, `code`.

Inside `p`, `ul`/`ol` items, `quote` and `callout` text you may use
`[label](url)`, `**bold**` and `` `code` ``. Everything is HTML-escaped first,
so raw HTML in YAML renders as visible text rather than markup, and link
targets are restricted to `http(s)`, site-relative, `#` and `mailto:` — a
`javascript:` or `data:` URL is silently dropped.

Validate without building the site:

```bash
C:/Python312/python.exe -m scripts.build_news --check
```

News pages are built by `python -m scripts.build_site`, and the daily refresh
workflow picks up new posts with no extra wiring.

## Comments

Readers comment with **no account, no login, and no mandatory name or email**.
A blank name posts as "Anonymous" / "Анонім".

**One thread per article, shared between languages.** The thread key is
`/news/<slug>` with no `/ukr` prefix, so the English and Ukrainian versions of
a post show the same discussion. The key is derived from the slug rather than
the URL — renaming a slug orphans its thread, so keep slugs stable.

### Choosing a backend

The section ships with the backend unconfigured: each post simply says comments
are not switched on yet. Nothing else breaks. Configure it in the `COMMENTS`
dict at the top of `scripts/build_news.py` and rebuild.

The default provider is **[Waline](https://waline.js.org/)** — open source,
no ads, no tracking, anonymous posting as a first-class mode, and the only
live option that runs on a free serverless tier rather than a VPS you must fund
and patch. Verified actively maintained as of 2026-07-19.

`remark42` and `disqus` are also wired up. This indirection is deliberate:
**Cusdis, a leading privacy-first comment system, was archived on 2026-07-17.**
Comment backends churn, and no single vendor should be load-bearing here.
Avoid Disqus unless there is no alternative — its free tier is ad-supported and
it does cross-context behavioural advertising, which is a poor fit for pages
where readers are researching a cancer diagnosis.

### Deploying Waline

1. Deploy the Waline server — the documented path is the Vercel template, then
   add a database from the Vercel dashboard under Storage → Create Database.
   Vercel Hobby plus Neon Free is comfortably within limits for this traffic.
2. Run the `waline.pgsql` schema to create the tables, then redeploy so the
   database environment variables take effect.
3. Set `JWT_TOKEN` (any random string), `SITE_NAME`, `SITE_URL`, `SERVER_URL`.
4. Register the admin account at `<your-server>/ui/register`. **Do this
   immediately after deploying** — the first account to register becomes admin.
5. Put the deployed URL into `COMMENTS["server_url"]` in
   `scripts/build_news.py`, then rebuild and commit the regenerated `docs/`.

Two settings deserve a deliberate decision rather than the default:

- **`AKISMET_KEY`.** Waline enables Akismet spam filtering by default using a
  shared key hardcoded into every install, which means **every comment's text
  is sent to a third party unless you opt out**. On a site where a comment may
  mention someone's illness, that should be a conscious choice: either set your
  own Akismet key, or set `AKISMET_KEY=false` and rely on the approval queue
  and rate limiting.
- **Storage region.** Waline's docs lead with LeanCloud, which is
  China-hosted. For a Ukrainian and EU audience choose Postgres in an EU
  region instead. This is a data-protection question, not a preference.

There is also a `GITHUB_REPO` storage backend that keeps comments as files in a
git repository instead of a database. It does not scale to high volume, but it
removes the database entirely, puts comments under version control, and fits
this project's existing "YAML plus git history" storage model. Worth
considering while comment volume is low.

### Moderation

Comments are visible immediately by default, which is what "open comments"
means and is the intended behaviour here. If that becomes untenable, set
`COMMENT_AUDIT=true` to hold new comments for approval; `forbiddenWords`,
`IPQPS` rate limiting, and Turnstile/reCAPTCHA keys are also available.

The moderation load, not the hosting, is the recurring cost of this feature.
Two things are worth acting on quickly when they appear:

- **A comment containing someone's medical details.** Threads are public and
  indexed; delete on sight, and note that deletion does not retract what search
  engines already cached. The note above each comment box asks readers not to
  post these, but some will anyway.
- **Treatment advice from one reader to another.** Not something to host
  silently on a site positioned as clinician-facing decision support.

Clinical errors in the knowledge base belong in a `clinical-error` issue, which
has a triage SLA under CHARTER §9.1, not in a comment thread. The note above
each comment box links there.

### Ukrainian interface

Waline ships no Ukrainian UI — its locales are Chinese, English, Japanese,
Korean, Portuguese, Russian, French, Vietnamese and Spanish. Falling back to
Russian on this site is not acceptable, so `_WALINE_LOCALE_UK` in
`scripts/build_news.py` supplies Ukrainian strings through the `locale`
override, with English as the base for anything not listed. If the widget shows
an English string you want translated, add its key there — the full key list is
in the Waline locale cookbook.

### Client assets

The Waline client is loaded from unpkg by default (`COMMENTS["client_base"]`).
To avoid the third-party CDN entirely, vendor `waline.js` and `waline.css` into
`docs/` and point `client_base` at the local copy.

## Service worker

The service worker skips all cross-origin traffic
(`url.origin !== self.location.origin` in `write_service_worker`). Without that
guard it would intercept the comment widget's iframe — which loads with
`request.mode === 'navigate'` — and re-issue it as a no-store fetch, breaking
the widget. Do not remove it.
