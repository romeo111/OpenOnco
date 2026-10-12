// Exact pinned runtime URLs only. No patient data or unrelated CDN traffic.
const PYODIDE_RUNTIME_ASSETS = __PYODIDE_RUNTIME_ASSETS__;
const PYODIDE_RUNTIME_CACHE = '__PYODIDE_RUNTIME_CACHE__';

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
  if (!event.data || event.data.type !== 'CACHE_ENGINE_RUNTIME') return;
  try {
    const source = new URL(event.source.url);
    if (source.origin !== self.location.origin || !PLAN_PAGE_PATHS.includes(source.pathname)) return;
  } catch (_) { return; }
  // Always use the fixed inventory; ignore supplied URLs, DOM or clinical input.
  event.waitUntil(preparePyodideRuntime().catch(error => {
    console.warn('[OpenOnco] runtime retention incomplete:', error);
  }));
});
