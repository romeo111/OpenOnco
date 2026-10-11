// OpenOnco bundle service worker (CSD-6E + CSD-11A swr)
// Cache strategies:
//   0. Network-first index with offline fallback, so releases refresh metadata.
//   1. Cache-first for engine bundle artifacts (large, infrequent).
//   2. Stale-while-revalidate for try.html + style.css — repeat visits
//      paint instantly from cache while a fresh copy fetches in the
//      background, so the dropdowns aren't gated on the HTML download.
// Cache name is stamped with the core bundle's SHA-256 prefix so a KB
// push automatically rotates the cache key.
const CACHE_NAME = 'openonco-bundle-l4-6f513b923145';
const PRECACHE = [
  '/manifest.webmanifest',
  '/logo.svg',
  '/favicon.svg',
  '/openonco-engine-index.json',
  '/openonco-engine-core.zip',
  '/try.html',
  '/ukr/try.html',
  '/style.css',
];
// Routes that use stale-while-revalidate (instant from cache, refresh
// in background). HTML pages must be on this list — never cache-first,
// or the user gets stuck on an old build.
const SWR_PATHS = ['/try.html', '/ukr/try.html', '/about.html', '/ukr/about.html',
  '/style.css', '/news.html', '/ukr/news.html'];
// Per-article news pages are matched by prefix rather than listed, since slugs
// are added by content authors without touching this file.
const SWR_PREFIXES = ['/news/', '/ukr/news/', '/clinical-styles/'];

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

function staleWhileRevalidate(event) {
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      cache.match(event.request, { ignoreSearch: new URL(event.request.url).pathname !== '/clinical-localization.js' }).then((hit) => {
        const network = fetch(event.request).then((resp) => {
          if (resp && resp.ok) cache.put(event.request, resp.clone());
          return resp;
        }).catch(() => hit);
        return hit || network;
      })
    )
  );
}

function networkFirstNavigation(event) {
  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).catch(() =>
      caches.match(event.request, { ignoreSearch: true })
    )
  );
}

function networkFirstBundleIndex(event) {
  event.respondWith(caches.open(CACHE_NAME).then(async cache => {
    try {
      const response = await fetch(event.request, { cache: 'no-store' });
      if (!response.ok) throw new Error('Bundle index HTTP ' + response.status);
      await cache.put('/openonco-engine-index.json', response.clone()).catch(() => {});
      return response;
    } catch (error) {
      const cached = await cache.match('/openonco-engine-index.json');
      if (cached) return cached;
      throw error;
    }
  }));
}

async function cachedVersionedBundle(cache, request) {
  const exact = await cache.match(request, { ignoreSearch: false });
  if (exact) return exact;
  const url = new URL(request.url);
  const version = url.searchParams.get('v');
  // The unversioned precached core belongs to this worker's hash bucket.
  if (url.pathname === '/openonco-engine-core.zip' && version && CACHE_NAME.endsWith('-' + version)) {
    return cache.match(url.pathname, { ignoreSearch: false });
  }
}

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  // Never touch cross-origin traffic. Embedded third-party frames (the news
  // comment widget) load with request.mode === 'navigate', so without this
  // guard the navigation branch below would re-issue them as no-store fetches
  // and break them. It also stops the pathname-only matching further down from
  // hijacking a third-party URL that happens to share a path with ours.
  if (url.origin !== self.location.origin) return;

  if (event.request.mode === 'navigate') {
    return networkFirstNavigation(event);
  }

  if (url.pathname === '/openonco-engine-index.json') return networkFirstBundleIndex(event);

  // SWR for the small interactive shell (HTML + CSS).
  if (url.pathname === '/clinical-localization.js' ||
      /^\/(es|pt|de|fr)\/(clinical-(ui-)?translations|kb_search_index)\.json$/.test(url.pathname) ||
      SWR_PATHS.indexOf(url.pathname) !== -1 ||
      SWR_PREFIXES.some((p) => url.pathname.startsWith(p))) {
    return staleWhileRevalidate(event);
  }

  // Cache-first for the heavy engine bundles.
  const cacheFirstMatch =
    url.pathname.endsWith('/openonco-engine-core.zip') ||
    url.pathname.startsWith('/disease/openonco-');
  if (!cacheFirstMatch) return;
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      cachedVersionedBundle(cache, event.request).then((hit) =>
        hit || fetch(event.request).then((resp) => {
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
