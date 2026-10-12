// Real shipped preparation code: failure recovery must reuse verified public bytes.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const page = fs.readFileSync('docs/try.html', 'utf8');
const start = page.indexOf('async function cacheAllBundlesForOffline()');
const end = page.indexOf('// Resolve a disease_id', start);
assert(start >= 0 && end > start);
const code = page.slice(start, end).replace(/\r\n/g, '\n');
function fixture() {
  const retained = new Map(), handlers = {}, calls = { fetches: [], opens: 0, progress: [] };
  const state = { indexFails: false, storageFails: false, failedUrl: null, corrupt: false };
  const response = url => ({ ok: true, clone() { return this; }, arrayBuffer: async () => ({ url, corrupt: state.corrupt }) });
  const context = vm.createContext({
    console: { warn() {} }, URL, location: { origin: 'https://openonco.info' },
    navigator: { onLine: true }, offlineModulesStateEl: {}, setText() {},
    window: { caches: {}, addEventListener(name, fn) { handlers[name] = fn; }, setTimeout(fn) { calls.scheduled = fn(); } },
    loadBundleIndex: async () => { if (state.indexFails) throw Error('index unavailable'); },
    offlineBundleUrls: () => ['/core?v=123456789abc', '/module?v=abcdef123456'],
    setOfflineCacheProgress: (...args) => calls.progress.push(args), yieldToBrowser: async () => {},
    verifyBundleVersion: async bytes => { if (bytes.corrupt) throw Error('integrity failure'); },
    caches: { open: async () => {
      calls.opens++;
      if (state.storageFails) throw Error('storage denied');
      return { match: async url => retained.get(url), delete: async url => retained.delete(url),
        put: async (url, value) => retained.set(url, value) };
    } },
    fetch: async url => { calls.fetches.push(url); if (state.failedUrl === url) throw Error('network failure'); return response(url); },
  });
  vm.runInContext('let offlineCacheStarted=false,uiBusy=false,generating=false,enginReady=false,planSource=null; const bundleIndex={core_version:"123456789abc"};' + code, context);
  return { context, retained, state, calls, handlers, run: s => vm.runInContext(s, context) };
}
(async () => {
  let f = fixture();
  f.state.indexFails = true;
  await assert.rejects(f.run('cacheAllBundlesForOffline()'), /index unavailable/);
  assert.equal(f.run('offlineCacheStarted'), false);
  f.state.indexFails = false;
  await Promise.all([f.run('cacheAllBundlesForOffline()'), f.run('cacheAllBundlesForOffline()')]);
  assert.equal(f.calls.opens, 1, 'Concurrent calls must share one preparation pass');
  assert.equal(f.retained.size, 2);
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.calls.fetches.length, 2, 'A completed pass must not redownload');
  f = fixture();
  f.context.navigator.onLine = false;
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.run('offlineCacheStarted'), false);
  assert.equal(f.calls.fetches.length, 0);
  f.handlers.online();
  assert.equal(f.calls.opens, 0, 'Do not start downloads before a generated plan');
  f.context.navigator.onLine = true;
  f.run('enginReady=true;planSource="generated"');
  f.handlers.online();
  // Await the actual scheduled preparation, without timing assumptions.
  await f.calls.scheduled;
  assert.equal(f.retained.size, 2, 'Returning online resumes preparation');
  f = fixture();
  f.state.storageFails = true;
  await assert.rejects(f.run('cacheAllBundlesForOffline()'), /storage denied/);
  assert.equal(f.run('offlineCacheStarted'), false);
  f.state.storageFails = false;
  f.state.failedUrl = '/module?v=abcdef123456';
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.retained.size, 1);
  assert.equal(f.run('offlineCacheStarted'), false);
  f.state.failedUrl = null;
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.retained.size, 2);
  assert.equal(f.calls.fetches.filter(url => url.startsWith('/core')).length, 1, 'Retry reuses verified retained core');
  assert.deepEqual(f.calls.progress.at(-1), [2, 2, 0]);
  f = fixture(); f.state.corrupt = true;
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.retained.size, 0, 'Corrupted bytes must never enter retained storage');
  assert.equal(f.run('offlineCacheStarted'), false);
  f.state.corrupt = false;
  await f.run('cacheAllBundlesForOffline()');
  assert.equal(f.retained.size, 2);
  for (const locale of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
    const html = fs.readFileSync('docs/' + locale + 'try.html', 'utf8');
    const a = html.indexOf('async function cacheAllBundlesForOffline()'), b = html.indexOf('// Resolve a disease_id', a);
    const actual = html.slice(a, b).replace(/\r\n/g, '\n');
    // Labels are translated, so compare the recovery/control flow around those labels.
    assert(actual.includes('if (!complete) offlineCacheStarted = false;'));
    assert(actual.includes("window.addEventListener('online'"));
    assert(actual.includes('enginReady && planSource === \'generated\''));
    assert(actual.includes('complete = failed === 0;'));
  }
  console.log('Offline preparation recovers after index/network/storage/integrity failures; retries reuse verified bytes; all eleven clients guarded');
})().catch(error => { console.error(error); process.exitCode = 1; });
