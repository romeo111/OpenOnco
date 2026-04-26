// OpenOnco bundle service worker (CSD-6E)
// Cache-first strategy for the lazy-load engine bundles. Cache name is
// stamped with the core bundle's SHA-256 prefix at build time, so any KB
// change automatically rotates the cache key and old bundles are evicted
// on the next install (see the activate handler).
const CACHE_NAME = 'openonco-bundle-519b4505e7b6';
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
    url.pathname.endsWith('/openonco-engine.zip') ||
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
