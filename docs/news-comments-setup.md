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

The news pages are built as part of `python -m scripts.build_site`, and the
daily refresh workflow picks up new posts with no extra wiring.

## Turning on embedded comments

Comments use [giscus](https://giscus.app/), which stores threads in GitHub
Discussions. The project therefore holds no commenter data of its own, and
there is no advertising or third-party tracking.

Until this is configured, each post shows a link to the repository's
discussion page instead of an embedded widget. The section is fully functional
either way — this is the only step that needs a human with repo admin rights.

1. **Enable Discussions** — repository Settings → General → Features → tick
   *Discussions*.
2. **Create a category** — in the Discussions tab, add a category named
   `Announcements` and set its type to *Announcement*, so only maintainers can
   open threads and readers can only reply. This matters: it stops the comment
   space being used to start unmoderated medical threads.
3. **Install the giscus app** — <https://github.com/apps/giscus>, granted to
   this repository only.
4. **Read off the two ids** — open <https://giscus.app>, enter
   `romeo111/OpenOnco`, pick the `Announcements` category, and copy the
   generated `data-repo-id` and `data-category-id`.
5. **Paste them into `scripts/build_news.py`** in the `GISCUS` dict:

   ```python
   GISCUS = {
       "repo": GH_REPO,
       "repo_id": "R_xxxxxxxxxx",
       "category": "Announcements",
       "category_id": "DIC_xxxxxxxxxx",
       "host": "https://giscus.app",
   }
   ```

   Both ids are public identifiers, not secrets — they are visible in the
   page source of every site that uses giscus.
6. **Rebuild** — `C:/Python312/python.exe -m scripts.build_site`, then commit
   the regenerated `docs/`.

Mapping is `specific`, with the discussion term set to `news/<slug>`. Renaming
a post's slug therefore orphans its existing thread; rename the discussion to
match, or keep the slug stable.

## Moderation

Comments are moderated through GitHub's own tools — maintainers can hide,
delete, or lock any thread from the Discussions UI, and blocking a user is a
repository-level setting.

The house rules rendered above every comment box (see `render_comments` in
`scripts/build_news.py`) exist because this is a cancer-information site:

- **No personal medical data.** Comment threads are public, permanent and
  indexed. Delete-on-sight is the right response to a comment containing a
  diagnosis, test results or anything identifying a patient — and note that
  deletion does not retract what search engines already cached.
- **Comments are not medical advice** and are not reviewed by the clinical
  leads. They carry none of the source-citation guarantees of the knowledge
  base.
- **Clinical errors belong in an issue**, not a comment. Per CHARTER §9.1 the
  `clinical-error` path has a 48-hour triage and 7-day assessment SLA.

## Privacy behaviour

The giscus script is not loaded on page load. Nothing is requested from
giscus.app or github.com until the reader presses *Load comments*, so simply
reading an article makes no third-party request at all.

The service worker skips all cross-origin traffic
(`url.origin !== self.location.origin` in `write_service_worker`). Without that
guard it would intercept the giscus iframe — which loads with
`request.mode === 'navigate'` — and re-issue it as a no-store fetch, breaking
the widget. Do not remove it.
