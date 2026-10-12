// OpenOnco bundle service worker (CSD-6E + CSD-11A swr)
// Cache strategies:
//   0. Network-first index and validated public form catalogs with offline fallback.
//   1. Cache-first for engine bundle artifacts (large, infrequent).
//   2. Stale-while-revalidate for try.html + style.css — repeat visits
//      paint instantly from cache while a fresh copy fetches in the
//      background, so the dropdowns aren't gated on the HTML download.
// Cache name is stamped with the core bundle's SHA-256 prefix so a KB
// push automatically rotates the cache key.
const CACHE_NAME = 'openonco-bundle-l4-894440195fdf';
const CORE_STREAM_VERSION = 'f52aee8f8012';
const WORKSPACE_DATA_PATHS = ['/questionnaires.json', '/examples.json'];
const PLAN_PAGE_PATHS = ["/try.html", "/ukr/try.html", "/es/try.html", "/pt/try.html", "/de/try.html", "/fr/try.html", "/it/try.html", "/da/try.html", "/sv/try.html", "/nb/try.html", "/fi/try.html"];
// Exact pinned runtime URLs only. No patient data or unrelated CDN traffic.
const PYODIDE_RUNTIME_ASSETS = {"https://cdn.jsdelivr.net/pyodide/v0.26.4/full/PyYAML-6.0.1-cp312-cp312-pyodide_2024_0_wasm32.whl": {"bytes": 480325, "sha256": "7e2c1229550f6e6c64398b551fd70d641709a02df9ae08449c6625451ab68c2a"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/annotated_types-0.6.0-py3-none-any.whl": {"bytes": 27605, "sha256": "50f2adc38958cbac4c343806a8d7554bd987098e332ea5a796c642018455af2a"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pydantic-2.7.0-py3-none-any.whl": {"bytes": 1622248, "sha256": "750ccf9a0b0b9d8ddb555430510d444c1b00f121e51aa94e3b18a82af4d73a99"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pydantic_core-2.18.1-cp312-cp312-pyodide_2024_0_wasm32.whl": {"bytes": 4765973, "sha256": "f85156f928fbed235b783546dbe6fb38ca72cdc72e48aa8f841ea435c0fb2166"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide-lock.json": {"bytes": 106335, "sha256": "cd50b49de944c579045e122fe8628b31f9ce446379f032f36c05e273d38766e0"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.asm.js": {"bytes": 1229099, "sha256": "919560652ed3dad3707cb3a394785da1e046fb13dc0defa162058ff230cb7eed"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.asm.wasm": {"bytes": 10088051, "sha256": "b7e66a19427a55010ac3367c1b6c64b893f9826f783412945fdf0c3337f3bc94"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.mjs": {"bytes": 13779, "sha256": "7f24c6655a79eacf0061d3d4e6a60dc0b1938812d15c52d7ff8b37d9e0689e51"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/python_stdlib.zip": {"bytes": 2341872, "sha256": "72894522b791858b9d613ac786b951d8b5094035dcf376313ea24a466810f336"}, "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/typing_extensions-4.11.0-py3-none-any.whl": {"bytes": 140469, "sha256": "696ecd97bd0abc88fc25d376ac06f4233ab16bba3e992c4b37bbc2715240d4e8"}};
const PYODIDE_RUNTIME_CACHE = 'openonco-runtime-42c5cc37cb67';

async function verifiedRuntimeResponse(response, asset) {
  if (!response || !response.ok || response.type === 'opaque') {
    throw new Error('Runtime download unavailable.');
  }
  const bytes = await response.clone().arrayBuffer();
  if (bytes.byteLength !== asset.bytes) {
    const error = new Error('Runtime size mismatch.'); error.name = 'RuntimeIntegrityError'; throw error;
  }
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  const hash = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
  if (hash !== asset.sha256) {
    const error = new Error('Runtime integrity mismatch.'); error.name = 'RuntimeIntegrityError'; throw error;
  }
  return response;
}

async function pyodideRuntimeResponse(request) {
  const url = typeof request === 'string' ? request : request.url;
  const asset = PYODIDE_RUNTIME_ASSETS[url];
  if (!asset) throw new Error('Unlisted runtime URL.');
  const cache = await caches.open(PYODIDE_RUNTIME_CACHE).catch(() => null);
  if (cache && request.cache !== 'reload') {
    const retained = await cache.match(url).catch(() => null);
    if (retained) {
      try { return await verifiedRuntimeResponse(retained, asset); }
      catch (_) { await cache.delete(url).catch(() => {}); }
    }
  }
  const download = mode => fetch(request, { credentials: 'omit', redirect: 'error', referrerPolicy: 'no-referrer', cache: mode });
  let response;
  try {
    // A first uncontrolled visit may already have these immutable bytes in HTTP cache.
    response = await verifiedRuntimeResponse(await download(request.cache === 'reload' ? 'reload' : 'force-cache'), asset);
  } catch (error) {
    if (error.name !== 'RuntimeIntegrityError' || request.cache === 'reload') throw error;
    // A bad HTTP-cache entry must not permanently trap the next attempt.
    response = await verifiedRuntimeResponse(await download('reload'), asset);
  }
  if (cache) await cache.put(url, response.clone()).catch(() => {});
  return response;
}

let pyodideRuntimePreparation = null;
function preparePyodideRuntime() {
  if (!pyodideRuntimePreparation) {
    pyodideRuntimePreparation = (async () => {
      // Bound memory/network concurrency. A later request retries incomplete files.
      const urls = Object.keys(PYODIDE_RUNTIME_ASSETS);
      let next = 0;
      const results = await Promise.allSettled([0, 1].map(async () => {
        while (next < urls.length) await pyodideRuntimeResponse(urls[next++]);
      }));
      const failure = results.find(result => result.status === 'rejected');
      if (failure) throw failure.reason;
    })().finally(() => { pyodideRuntimePreparation = null; });
  }
  return pyodideRuntimePreparation;
}

self.addEventListener('message', event => {
  if (!event.data || !['CACHE_ENGINE_RUNTIME', 'CHECK_ENGINE_RUNTIME'].includes(event.data.type)) return;
  try {
    const source = new URL(event.source.url);
    if (source.origin !== self.location.origin || !PLAN_PAGE_PATHS.includes(source.pathname)) return;
  } catch (_) { return; }
  // Always use the fixed inventory; ignore supplied URLs, DOM or clinical input.
  event.waitUntil((async () => {
    if (event.data.type === 'CACHE_ENGINE_RUNTIME') {
      await preparePyodideRuntime().catch(error => {
        console.warn('[OpenOnco] runtime retention incomplete:', error);
      });
    }
    const cache = await caches.open(PYODIDE_RUNTIME_CACHE).catch(() => null);
    let completed = 0;
    if (cache) {
      for (const [url, asset] of Object.entries(PYODIDE_RUNTIME_ASSETS)) {
        try {
          const response = await cache.match(url);
          await verifiedRuntimeResponse(response, asset);
          completed++;
        } catch (_) { /* Missing/corrupt/unreadable files must not count as retained. */ }
      }
    }
    if (event.source && typeof event.source.postMessage === 'function') {
      event.source.postMessage({ type: 'ENGINE_RUNTIME_CACHE_STATUS', requestId: Number.isSafeInteger(event.data.requestId) ? event.data.requestId : null, cache: PYODIDE_RUNTIME_CACHE, completed, total: Object.keys(PYODIDE_RUNTIME_ASSETS).length });
    }
  })());
});

const PRECACHE = [
  '/manifest.webmanifest',
  '/logo.svg',
  '/favicon.svg',
  '/openonco-engine-index.json',
  '/openonco-engine-core.tar.gz',
  '/try.html',
  '/ukr/try.html',
  '/style.css',
  ...WORKSPACE_DATA_PATHS,
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
      Promise.all(PRECACHE.map((u) => (
        WORKSPACE_DATA_PATHS.includes(u)
          ? workspaceDataResponse(cache, new Request(self.location.origin + u))
          : cache.add(u)
      ).catch(() => null)))
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
  const url = new URL(event.request.url);
  if (PLAN_PAGE_PATHS.includes(url.pathname) && !url.search) {
    event.respondWith(planNavigationResponse(event.request));
    return;
  }
  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).catch(() =>
      caches.match(event.request, { ignoreSearch: true })
    )
  );
}

async function planNavigationResponse(request) {
  const path = new URL(request.url).pathname;
  const cache = await caches.open(CACHE_NAME).catch(() => null);
  const retained = async () => {
    const hit = cache && await cache.match(path).catch(() => null);
    return hit && hit.ok && (hit.headers.get('Content-Type') || '').includes('text/html') ? hit : null;
  };
  try {
    const response = await fetch(request, { cache: 'no-store' });
    if (response.ok && (response.headers.get('Content-Type') || '').includes('text/html')) {
      if (cache) await cache.put(path, response.clone()).catch(() => {});
      return response;
    }
    return (await retained()) || response;
  } catch (error) {
    const cached = await retained();
    if (cached) return cached;
    throw error;
  }
}

self.addEventListener('message', (event) => {
  const data = event.data;
  if (!data || data.type !== 'CACHE_PLAN_PAGE' || !PLAN_PAGE_PATHS.includes(data.path)) return;
  try {
    const source = new URL(event.source.url);
    if (source.origin !== self.location.origin || source.search) return;
  } catch (_) { return; }
  // Fetch only a known public page; never persist a supplied DOM or profile.
  event.waitUntil(planNavigationResponse(new Request(self.location.origin + data.path)).catch(() => {}));
});

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

function isWorkspaceData(value, path) {
  const id = path === '/questionnaires.json' ? 'id' : 'case_id';
  return Array.isArray(value) && value.every(item => item && typeof item === 'object'
    && typeof item[id] === 'string' && item[id].trim()
    && (path !== '/questionnaires.json' || Array.isArray(item.groups)));
}

async function workspaceDataResponse(cache, request) {
  const key = new URL(request.url).pathname;
  try {
    const response = await fetch(request, { cache: 'no-store' });
    if (!response.ok) throw new Error('Workspace data HTTP ' + response.status);
    if (!isWorkspaceData(await response.clone().json(), key)) throw new Error('Invalid workspace data');
    if (cache) await cache.put(key, response.clone()).catch(() => {});
    return response;
  } catch (error) {
    const cached = cache && await cache.match(key).catch(() => null);
    if (cached && cached.ok) {
      try {
        if (isWorkspaceData(await cached.clone().json(), key)) return cached;
      } catch (_) {}
    }
    throw error;
  }
}

function networkFirstWorkspaceData(event) {
  event.respondWith(caches.open(CACHE_NAME).catch(() => null).then(cache => workspaceDataResponse(cache, event.request)));
}

async function cachedVersionedBundle(cache, request) {
  if (request.cache === 'reload') return undefined;
  const exact = await cache.match(request, { ignoreSearch: false });
  if (exact) return exact;
  const url = new URL(request.url);
  const version = url.searchParams.get('v');
  // The unversioned precached core belongs to this worker's hash bucket.
  if (url.pathname === '/openonco-engine-core.zip' && version && CACHE_NAME.endsWith('-' + version)) {
    return cache.match(url.pathname, { ignoreSearch: false });
  }
  if (url.pathname === '/openonco-engine-core.tar.gz' && version && version === CORE_STREAM_VERSION) {
    return cache.match(url.pathname, { ignoreSearch: false });
  }
}

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  if (event.request.mode !== 'navigate' && Object.prototype.hasOwnProperty.call(PYODIDE_RUNTIME_ASSETS, event.request.url)) {
    event.respondWith(pyodideRuntimeResponse(event.request));
    return;
  }

  // Never touch other cross-origin traffic. Embedded third-party frames (the news
  // comment widget) load with request.mode === 'navigate', so without this
  // guard the navigation branch below would re-issue them as no-store fetches
  // and break them. It also stops the pathname-only matching further down from
  // hijacking a third-party URL that happens to share a path with ours.
  if (url.origin !== self.location.origin) return;

  if (event.request.mode === 'navigate') {
    return networkFirstNavigation(event);
  }

  if (url.pathname === '/openonco-engine-index.json') return networkFirstBundleIndex(event);
  if (WORKSPACE_DATA_PATHS.includes(url.pathname)) return networkFirstWorkspaceData(event);

  // SWR for the small interactive shell (HTML + CSS).
  if (/^\/clinical-localization(?:\.[a-f0-9]{12})?\.js$/.test(url.pathname) ||
      /^\/geo-lang\.[a-f0-9]{12}\.js$/.test(url.pathname) ||
      /^\/(es|pt|de|fr|it|da|sv|nb|fi)\/(clinical-(ui-)?translations(?:\.[a-f0-9]{12})?|kb_search_index)\.json$/.test(url.pathname) ||
      url.pathname.endsWith('/shared-header.fragment') || url.pathname === '/shared-site-header.js' || url.pathname === '/shared-clinical-reader.js' ||
      SWR_PATHS.indexOf(url.pathname) !== -1 ||
      SWR_PREFIXES.some((p) => url.pathname.startsWith(p))) {
    return staleWhileRevalidate(event);
  }

  // Cache-first for the heavy engine bundles.
  const cacheFirstMatch =
    url.pathname.endsWith('/openonco-engine-core.zip') ||
    url.pathname.endsWith('/openonco-engine-core.tar.gz') ||
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
