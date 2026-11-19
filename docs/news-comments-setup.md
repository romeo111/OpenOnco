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

This part happens in the Vercel and Neon dashboards, under your own accounts —
it cannot be automated from this repository. It is a one-time, ~20–40 minute
job. Verified current against Waline's Vercel deploy guide on 2026-07-20.

1. Open the Waline Vercel deploy link:
   `https://vercel.com/new/clone?repository-url=https://github.com/walinejs/waline/tree/main/example`
   — sign in to Vercel, name the project, and create it. (Vercel Hobby is free
   and within limits for this traffic.)
2. In the project, go to **Storage → Create Database → Neon**, pick an **EU
   region**, and create it. Vercel wires the Postgres connection variables in
   for you.
3. Open Neon's SQL editor and run the `waline.pgsql` schema (linked from the
   Waline deploy guide) to create the tables.
4. Add the environment variables below (Settings → Environment Variables), then
   **Deployments → Redeploy** — Waline only picks up new variables on a
   redeploy.
5. Once the deployment is `Ready`, open `<your-server>/ui/register` and register
   **immediately** — the first account to register becomes the admin. Do this
   before sharing the URL anywhere.
6. Send the deployed server URL back, and the one-line `COMMENTS["server_url"]`
   change plus rebuild can be committed for you. (Or edit it yourself in
   `scripts/build_news.py` and run `python -m scripts.build_site`.)

**Environment variables — paste these:**

```
JWT_TOKEN        = <any long random string; this signs admin login tokens>
SITE_NAME        = OpenOnco
SITE_URL         = https://openonco.info
SERVER_URL       = <your Vercel deployment URL, once you know it>
SECURE_DOMAINS   = openonco.info
AKISMET_KEY      = false
```

`SECURE_DOMAINS` restricts posting to your own site — without it, any website
can point its comment box at your server and use it as a spam relay. Set it.

**Two choices baked into the block above, and why:**

- **`AKISMET_KEY = false`.** Waline defaults to Akismet spam filtering using a
  shared key hardcoded into every install, which means **every comment's text
  is sent to a third party unless you opt out**. On a page where a comment may
  mention someone's illness, that default is wrong. Turning it off leans on the
  approval queue, `IPQPS` rate limiting (default 60s) and `SECURE_DOMAINS`
  instead. If spam becomes a real problem later, get your own Akismet key
  rather than reinstating the shared one.
- **Neon in an EU region, not LeanCloud.** Waline's docs lead with LeanCloud,
  which is China-hosted. For a Ukrainian and EU audience the datastore region
  is a data-protection question, not a preference — keep it in the EU.

**Optional — hold comments for approval.** If unmoderated comments on a
cancer-information page feel too exposed, add `COMMENT_AUDIT = true`. New
comments then stay hidden until you approve them in the admin UI. This trades
"open" for "safe"; the default (immediate) is what "open comments" means, but
the choice is yours.

**Alternative storage — `GITHUB_REPO`.** Waline can keep comments as files in a
git repository instead of a database. It does not scale to high volume, but it
removes the database entirely, puts comments under version control, and fits
this project's existing "YAML plus git history" model. Worth considering while
volume is low.

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
