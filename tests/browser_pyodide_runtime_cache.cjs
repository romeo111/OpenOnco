// Execute the complete deployed worker; validate strict retention and recovery.
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const { webcrypto, createHash } = require('node:crypto');
const manifest = JSON.parse(fs.readFileSync('scripts/pyodide-runtime-manifest.json'));
const original = fs.readFileSync('docs/sw.js', 'utf8');
const assets = Object.fromEntries(Object.keys(manifest.assets).map((name, i) => {
  const bytes = process.argv[2] ? fs.readFileSync(require('node:path').join(process.argv[2], name)) : Buffer.from('VIRTUAL-RUNTIME-FIXTURE-' + i);
  return [manifest.base_url + name, { bytes, metadata: { bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex') } }];
}));
const inventory = Object.fromEntries(Object.entries(assets).map(([url, a]) => [url, a.metadata]));
const actualInventory = JSON.parse(original.match(/^const PYODIDE_RUNTIME_ASSETS = (.*);$/m)[1]);
assert.deepEqual(actualInventory, Object.fromEntries(Object.entries(manifest.assets).map(([n, a]) => [manifest.base_url + n, a])));
const code = original.replace(/^const PYODIDE_RUNTIME_ASSETS = .*;$/m, 'const PYODIDE_RUNTIME_ASSETS = ' + JSON.stringify(inventory) + ';');
function fixture() {
  const stored = new Map(), handlers = {}, state = { offline: false, corrupt: false, openFails: false, putFails: false, failedUrl: null, httpCache: false, badHttpCache: false };
  const replies = [];
  const calls = { fetches: [], puts: [], active: 0, peak: 0 };
  const context = vm.createContext({ URL, Request, Response, Uint8Array, crypto: webcrypto, console: { warn() {} },
    self: { location: { origin: 'https://openonco.info' }, addEventListener(name, fn) { (handlers[name] ||= []).push(fn); } },
    caches: { open: async () => {
      if (state.openFails) throw Error('storage unavailable');
      return { match: async url => stored.get(url)?.clone(), delete: async url => stored.delete(url),
        put: async (url, response) => { if (state.putFails) throw Error('quota'); calls.puts.push(url); stored.set(url, response.clone()); } };
    } },
    fetch: async (request, options) => {
      const url = typeof request === 'string' ? request : request.url;
      calls.fetches.push(url);
      assert.equal(options.credentials, 'omit'); assert.equal(options.redirect, 'error'); assert.equal(options.referrerPolicy, 'no-referrer');
      assert(assets[url], 'Only fixed runtime assets may reach the network');
      if ((state.offline && !(state.httpCache && options.cache === 'force-cache')) || state.failedUrl === url) throw Error('offline');
      calls.active++; calls.peak = Math.max(calls.peak, calls.active);
      await Promise.resolve(); calls.active--;
      return new Response((state.corrupt || (state.badHttpCache && options.cache === 'force-cache')) ? Buffer.alloc(assets[url].bytes.length, 0) : assets[url].bytes);
    },
  });
  vm.runInContext(code, context);
  const run = s => vm.runInContext(s, context);
  function request(url, options = {}) {
    let result;
    for (const fn of handlers.fetch) fn({ request: { url, method: 'GET', cache: 'default', mode: 'cors', ...options }, respondWith(p) { result = p; } });
    return result;
  }
  function message(source, data = { type: 'CACHE_ENGINE_RUNTIME' }) {
    let result;
    for (const fn of handlers.message) fn({ source: { url: source, postMessage: data => replies.push(data) }, data, waitUntil(p) { result = p; } });
    return result;
  }
  return { state, stored, calls, replies, request, message, run };
}
(async () => {
  const urls = Object.keys(assets);
  let f = fixture();
  for (const url of urls) {
    assert.deepEqual(Buffer.from(await (await f.request(url)).arrayBuffer()), assets[url].bytes);
  }
  assert.equal(f.stored.size, 10);
  f.state.offline = true;
  for (const url of urls) assert.deepEqual(Buffer.from(await (await f.request(url)).arrayBuffer()), assets[url].bytes);
  assert.equal(f.calls.fetches.length, 10, 'Retained runtime works without further network access');
  f.stored.set(urls[0], new Response('corrupt'));
  await assert.rejects(f.request(urls[0]), /offline/);
  assert(!f.stored.has(urls[0]), 'Corrupt retained bytes must be evicted');
  f.state.offline = false; f.state.corrupt = true;
  await assert.rejects(f.request(urls[0]), /integrity mismatch/);
  assert(!f.stored.has(urls[0]), 'Corrupt network bytes must never be retained');
  f.state.corrupt = false;
  await f.request(urls[0]);
  await f.request(urls[0], { cache: 'reload' });
  assert.equal(f.calls.fetches.at(-1), urls[0], 'Explicit reload bypasses retained bytes');
  for (const url of [urls[0] + '?profile=PRIVATE', manifest.base_url + 'unlisted.whl',
    'https://third-party.example/pyodide.mjs', 'https://cdn.jsdelivr.net/pyodide/v0.26.5/full/pyodide.mjs']) {
    assert.equal(f.request(url), undefined, 'Other versions/query-bearing/unrelated requests are not intercepted');
  }
  assert.equal(f.request(urls[0], { method: 'POST' }), undefined);
  assert.equal(f.request(urls[0], { mode: 'navigate' }), undefined);
  f = fixture(); f.state.badHttpCache = true;
  await f.request(urls[0]);
  assert.equal(f.calls.fetches.length, 2, 'One forced reload repairs a corrupt HTTP-cache entry');
  assert.equal(f.stored.size, 1);
  f = fixture(); f.state.offline = true; f.state.httpCache = true;
  await f.message('https://openonco.info/try.html');
  assert.equal(f.stored.size, 10, 'First uncontrolled visit can retain already downloaded HTTP-cache bytes offline');
  f = fixture(); f.state.openFails = true;
  await f.request(urls[0]); assert.equal(f.stored.size, 0);
  f.state.openFails = false; f.state.putFails = true;
  await f.request(urls[0]); assert.equal(f.stored.size, 0, 'Storage denial must not break valid online loading');
  f = fixture();
  assert.equal(f.message('https://third-party.example/try.html'), undefined);
  assert.equal(f.message('https://openonco.info/news.html'), undefined);
  await Promise.all([f.message('https://openonco.info/fi/try.html?profile=PRIVATE'), f.message('https://openonco.info/try.html')]);
  assert.equal(f.calls.fetches.length, 10, 'First uncontrolled visit preparation is deduplicated');
  assert(f.calls.peak <= 2, 'Bound concurrent network/buffer use');
  assert(f.calls.puts.every(url => assets[url]), 'Never retain source URL, profile, DOM or supplied URL');
  f.state.offline = true;
  await f.message('https://openonco.info/try.html', { type: 'CACHE_ENGINE_RUNTIME', html: 'PRIVATE', urls: ['https://private.example'] });
  assert.equal(f.calls.fetches.length, 10);
  f = fixture(); f.state.failedUrl = urls[0];
  await f.message('https://openonco.info/try.html');
  assert.equal(f.stored.size, 9);
  f.state.failedUrl = null;
  await f.message('https://openonco.info/try.html');
  assert.equal(f.stored.size, 10);
  assert.equal(f.calls.fetches.length, 11, 'Retry fetches only incomplete runtime files');
  for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
    const html = fs.readFileSync('docs/' + prefix + 'try.html', 'utf8');
    const labels = JSON.parse(html.match(/^const runtimeCacheCopy = (.*);$/m)[1]);
    assert(html.includes('<dt>' + labels.label + '</dt>'));
    assert(html.includes('aria-live="polite">' + labels.unchecked + '</dd>'));
    if (prefix) assert.notEqual(labels.ready, 'Files saved', 'Native runtime status must be available in every localized edition');
    const receiver = html.match(/^function receiveRuntimeCacheStatus\([^\n]*\{[\s\S]*?^\}/m)[0].replace(/\r\n/g, '\n');
    const originalReceiver = fs.readFileSync('docs/try.html', 'utf8').match(/^function receiveRuntimeCacheStatus\([^\n]*\{[\s\S]*?^\}/m)[0].replace(/\r\n/g, '\n');
    assert.equal(receiver, originalReceiver, 'All eleven editions must use the same trusted-worker and count validation');
    assert(html.includes('async function retainEngineRuntime()'));
    assert(html.includes("postMessage({ type: 'CACHE_ENGINE_RUNTIME', requestId: ++runtimeCacheRequestId })"));
    assert(html.includes('retainEngineRuntime().catch(() => {});'));
  }
  const page = fs.readFileSync('docs/try.html', 'utf8');
  const clientCode = page.slice(page.indexOf('async function checkRuntimeCacheStatus()'), page.indexOf('function scheduleOfflineCacheWarmup()'));
  const posts = [], clientEvents = {};
  let active = { scriptURL: 'https://openonco.info/sw.js', postMessage: data => posts.push(data) };
  const serviceWorker = { get controller() { return active; }, get ready() { return Promise.resolve({ active }); },
    addEventListener: (name, fn) => { clientEvents[name] = fn; } };
  const stateEl = {};
  const cacheVersion = JSON.parse(page.match(/^const runtimeCacheVersion = (.*);$/m)[1]);
  const copy = JSON.parse(page.match(/^const runtimeCacheCopy = (.*);$/m)[1]);
  const client = vm.createContext({ URL, location: { origin: 'https://openonco.info' }, runtimeCacheStateEl: stateEl, runtimeCacheCopy: copy, runtimeCacheFileCount: 10, runtimeCacheVersion: cacheVersion, runtimeCacheRequestId: 0, setText: (el, value) => { el.textContent = value; }, navigator: { serviceWorker }, console: { warn() {} } });
  vm.runInContext('let enginReady=false,planSource=null;' + clientCode, client);
  clientEvents.controllerchange();
  for (let i = 0; i < 5; i++) await Promise.resolve();
  assert(posts.every(data => data.type === 'CHECK_ENGINE_RUNTIME'), 'Only inspect retained bytes before generation');
  posts.length = 0;
  vm.runInContext('enginReady=true;planSource="generated";', client);
  await vm.runInContext('retainEngineRuntime()', client);
  active = { scriptURL: 'https://openonco.info/sw.js', postMessage: data => posts.push(data) };
  clientEvents.controllerchange();
  for (let i = 0; i < 5; i++) await Promise.resolve();
  assert.equal(posts.length, 2, 'Worker upgrades retry retention after generation');
  assert(posts.every(data => Object.keys(data).length === 2 && Number.isSafeInteger(data.requestId) && data.type === 'CACHE_ENGINE_RUNTIME'));
  const trusted = active;
  clientEvents.message({ source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', cache: cacheVersion, requestId: client.runtimeCacheRequestId, completed: 9, total: 10 } });
  assert.equal(stateEl.textContent, copy.partial + ' (9 / 10)');
  clientEvents.message({ source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', cache: cacheVersion, requestId: client.runtimeCacheRequestId, completed: 10, total: 10 } });
  assert.equal(stateEl.textContent, copy.ready + ' (10 / 10)');
  for (const event of [
    { source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', requestId: client.runtimeCacheRequestId - 1, completed: 0, total: 10 } },
    { source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', cache: 'old-inventory', completed: 0, total: 10 } },
    { source: { scriptURL: 'https://openonco.info/sw.js' }, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', completed: 0, total: 10 } },
    { source: { scriptURL: 'https://third-party.example/sw.js' }, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', completed: 0, total: 10 } },
    { source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', completed: 11, total: 10 } },
    { source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', completed: '10', total: 10 } },
    { source: trusted, data: { type: 'ENGINE_RUNTIME_CACHE_STATUS', completed: 10, total: 11 } },
  ]) { if (!event.data.cache) event.data.cache = cacheVersion; if (event.data.requestId === undefined) event.data.requestId = client.runtimeCacheRequestId; clientEvents.message(event); assert.equal(stateEl.textContent, copy.ready + ' (10 / 10)'); }
  f = fixture();
  await f.message('https://openonco.info/try.html', { type: 'CHECK_ENGINE_RUNTIME' });
  assert.equal(f.calls.fetches.length, 0, 'Status checks must not download runtime');
  assert.equal(f.replies.at(-1).completed, 0);
  await f.message('https://openonco.info/try.html');
  assert.equal(f.replies.at(-1).completed, 10);
  f.stored.set(urls[0], new Response('corrupt'));
  await f.message('https://openonco.info/try.html', { type: 'CHECK_ENGINE_RUNTIME' });
  assert.equal(f.replies.at(-1).completed, 9, 'Corrupt retained bytes cannot produce a ready indication');
  assert.equal(f.calls.fetches.length, 10);
  f.state.openFails = true;
  await f.message('https://openonco.info/try.html', { type: 'CHECK_ENGINE_RUNTIME' });
  assert.equal(f.replies.at(-1).completed, 0, 'Storage denial cannot produce a ready indication');
  console.log('Pinned runtime: all 10 assets offline, integrity failure rejection/recovery, storage tolerance, strict URL/method/privacy scope, bounded cold-visit preparation and retry; eleven clients guarded');
})().catch(error => { console.error(error); process.exitCode = 1; });
