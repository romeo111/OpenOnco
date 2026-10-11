// Version integrity and worker update/offline behavior, using actual shipped code.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { webcrypto, createHash } = require('node:crypto');
const page = fs.readFileSync('docs/try.html', 'utf8');
const worker = fs.readFileSync('docs/sw.js', 'utf8');
function fn(source, name) {
  const match = source.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`, 'm'));
  assert(match, name); return match[0];
}
const bytes = Uint8Array.from([1, 2, 3]);
const version = createHash('sha256').update(bytes).digest('hex').slice(0, 12);
const state = { unpacked: 0, fetches: 0, refreshes: 0 };
const index = { core: 'openonco-engine-core.zip', core_version: version };
const context = vm.createContext({
  Uint8Array, ArrayBuffer, crypto: webcrypto, Date, console: { warn() {}, error() {} }, index, bytes,
  BUNDLE_INDEX_URL: '/openonco-engine-index.json',
    fetch: async (_url, options) => { state.fetches++; if (options) assert(['no-store', 'reload'].includes(options.cache));
    return { ok: true, json: async () => index, arrayBuffer: async () => bytes.buffer }; },
  refreshBuildPanel: async () => { state.refreshes++; }, yieldToBrowser: async () => {},
  setStatus() {}, setLoadingProgress() {}, pyodide: { unpackArchive() { state.unpacked++; } },
});
vm.runInContext('let bundleIndex=null,bundleIndexPromise=null,coreBundleLoaded=false;' +
  ['loadBundleIndex', 'verifyBundleVersion', 'recoverBundleVersion', 'loadCoreBundle'].map(name => fn(page, name)).join('\n'), context);
const run = source => vm.runInContext(source, context);
function swFixture({ online = true, ok = true, hit = true } = {}) {
  const calls = { fetches: 0, puts: 0, matches: [] };
  const cached = { cached: true }, fresh = { ok, clone() { return this; } };
  const cache = {
    match: async (request, options) => { calls.matches.push([typeof request === 'string' ? request : request.url, options]); return hit ? cached : undefined; },
    put: async () => { calls.puts++; },
  };
  const c = vm.createContext({ URL, CACHE_NAME: 'openonco-bundle-l4-' + version,
    caches: { open: async () => cache },
    fetch: async (_request, options) => { calls.fetches++; assert.equal(options.cache, 'no-store'); if (!online) throw Error('offline'); return fresh; },
  });
  vm.runInContext(fn(worker, 'networkFirstBundleIndex') + fn(worker, 'cachedVersionedBundle'), c);
  let response;
  c.event = { request: { url: 'https://openonco.info/openonco-engine-index.json?t=1' }, respondWith: value => { response = value; } };
  return { c, calls, cache, cached, fresh, index: () => { vm.runInContext('networkFirstBundleIndex(event)', c); return response; } };
}
(async () => {
  await Promise.all([run('loadBundleIndex()'), run('loadBundleIndex()')]);
  assert.equal(state.fetches, 1, 'Concurrent index loading shares one request');
  await run('loadCoreBundle()'); assert.equal(state.unpacked, 1);
  run('coreBundleLoaded=false');
  const normalFetch = context.fetch;
  let recoveryRequests = 0;
  context.fetch = async (_url, options) => {
    recoveryRequests++;
    if (recoveryRequests === 1) return { ok: true, arrayBuffer: async () => Uint8Array.from([9]).buffer };
    assert.equal(options.cache, 'reload');
    return { ok: true, arrayBuffer: async () => bytes.buffer };
  };
  await run('loadCoreBundle()');
  assert.equal(recoveryRequests, 2);
  assert.equal(state.unpacked, 2, 'Only the verified recovery response is unpacked');
  context.fetch = normalFetch;
  run('coreBundleLoaded=false; bundleIndex={...index,core_version:"000000000000"}');
  const beforeMismatchFetches = state.fetches;
  await assert.rejects(run('loadCoreBundle()'), /changed during a site update/);
  assert.equal(state.fetches - beforeMismatchFetches, 2, 'A persistent mismatch gets only one recovery request');
  assert.equal(state.unpacked, 2, 'Mixed-version bytes cannot enter the runtime');
  assert.equal(run('coreBundleLoaded'), false);
  run('bundleIndex={...index,core_version:"invalid"}');
  await assert.rejects(run('loadCoreBundle()'), /version missing or invalid/);
  run('bundleIndex=null;bundleIndexPromise=null;');
  context.fetch = async () => ({ ok: false, status: 503 });
  await assert.rejects(run('loadBundleIndex()'), /unavailable/);
  assert.equal(run('bundleIndexPromise'), null);
  context.fetch = async () => ({ ok: true, json: async () => index });
  await run('loadBundleIndex()'); assert.equal(run('bundleIndex.core_version'), version);
  run('bundleIndex=null;bundleIndexPromise=null;');
  context.fetch = async () => ({ ok: true, json: async () => ({}) });
  await assert.rejects(run('loadBundleIndex()'), /Invalid bundle index metadata/);
  let f = swFixture();
  f.c.request = { url: 'https://openonco.info/openonco-engine-core.zip?v=' + version, cache: 'reload' };
  assert.equal(await vm.runInContext('cachedVersionedBundle(cache, request)', vm.createContext({ ...f.c, cache: f.cache })), undefined);
  assert.equal(f.calls.matches.length, 0, 'A recovery reload must bypass every worker cache hit');
  assert.equal(await f.index(), f.fresh); assert.equal(f.calls.puts, 1); assert.equal(f.calls.matches.length, 0);
  f = swFixture({ online: false }); assert.equal(await f.index(), f.cached);
  f = swFixture({ ok: false }); assert.equal(await f.index(), f.cached); assert.equal(f.calls.puts, 0);
  f = swFixture(); f.cache.put = async () => { throw Error('cache quota'); };
  assert.equal(await f.index(), f.fresh, 'Cache write failure must not replace a fresh online index with an old one');
  f = swFixture({ online: false, hit: false }); await assert.rejects(f.index(), /offline/);
  f = swFixture({ hit: false });
  f.cache.match = async (request, options) => { assert.equal(options.ignoreSearch, false); f.calls.matches.push(request); return typeof request === 'string' ? f.cached : undefined; };
  f.c.request = { url: `https://openonco.info/openonco-engine-core.zip?v=${version}` };
  assert.equal(await vm.runInContext('cachedVersionedBundle(cache,request)', Object.assign(f.c, { cache: f.cache })), f.cached);
  f.c.request.url = 'https://openonco.info/openonco-engine-core.zip?v=000000000000';
  assert.equal(await vm.runInContext('cachedVersionedBundle(cache,request)', f.c), undefined);
  const manifest = JSON.parse(fs.readFileSync('docs/openonco-engine-index.json', 'utf8'));
  const artifacts = [[manifest.core, manifest.core_version], ...Object.entries(manifest.diseases).map(([id, path]) => [path, manifest.disease_versions[id]])];
  for (const [path, expected] of artifacts) {
    assert.equal(createHash('sha256').update(fs.readFileSync('docs/' + path)).digest('hex').slice(0, 12), expected, path);
  }
  async function warmup({ invalidNetwork = false, invalidCached = false } = {}) {
    const calls = { puts: 0, deleted: 0, progress: [] };
    const response = data => ({ ok: true, clone: () => ({ arrayBuffer: async () => data.buffer }) });
    const c = vm.createContext({ Uint8Array, URL, crypto: webcrypto,
      location: { origin: 'https://openonco.info' }, window: { caches: {} }, navigator: { onLine: true },
      console: { warn() {} },
      caches: { open: async () => ({
        match: async (_url, options) => { assert.equal(options.ignoreSearch, false); return invalidCached ? response(Uint8Array.from([9])) : undefined; },
        delete: async () => { calls.deleted++; }, put: async () => { calls.puts++; },
      }) },
      fetch: async () => response(invalidNetwork ? Uint8Array.from([9]) : bytes),
      loadBundleIndex: async () => {}, yieldToBrowser: async () => {}, setText() {},
      setOfflineCacheProgress: (...values) => calls.progress.push(values), index,
    });
    vm.runInContext("let offlineCacheStarted=false,uiBusy=false,generating=false;const bundleIndex=index;" +
      ['verifyBundleVersion', 'offlineBundleUrls', 'cacheAllBundlesForOffline'].map(name => fn(page, name)).join('\n'), c);
    await vm.runInContext('cacheAllBundlesForOffline()', c);
    return calls;
  }
  let warm = await warmup(); assert.equal(warm.puts, 1); assert.deepEqual(warm.progress.at(-1), [1, 1, 0]);
  warm = await warmup({ invalidNetwork: true }); assert.equal(warm.puts, 0); assert.deepEqual(warm.progress.at(-1), [1, 1, 1]);
  warm = await warmup({ invalidCached: true }); assert.equal(warm.deleted, 1); assert.equal(warm.puts, 1);
  for (const locale of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/']) {
    const html = fs.readFileSync(`docs/${locale}try.html`, 'utf8');
    assert.equal((html.match(/await verifyBundleVersion\(/g) || []).length, 5);
    assert.equal(fn(html, 'recoverBundleVersion'), fn(page, 'recoverBundleVersion'));
    const withoutStatusCopy = code => code.replace(/setStatus\('[^']*'\);/, 'setStatus(LOCALIZED_COPY);');
    assert.equal(withoutStatusCopy(fn(html, 'loadCoreBundle')), withoutStatusCopy(fn(page, 'loadCoreBundle')));
    assert(html.includes('<dd id="coreVersion">—</dd>'));
    assert(html.includes('if (bundleIndexPromise) return bundleIndexPromise;'));
  }
  console.log('Bundle hashes, shared index loading, fresh online index and explicit offline fallback passed');
})().catch(error => { console.error(error); process.exitCode = 1; });
