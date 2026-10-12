/* Exercise the generated worker with a visitor's old cached translations. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const vm = require('node:vm');
const origin = 'https://openonco.info';
const cache = new Map();
const handlers = new Map();
const fetched = [];
const normalize = (url, ignoreSearch) => {
  const key = new URL(url, origin);
  if (ignoreSearch) key.search = '';
  return key.href;
};
cache.set(origin + '/clinical-localization.js', new Response('old four-language runtime'));
for (const locale of ['es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi']) {
  cache.set(`${origin}/${locale}/clinical-translations.json`, new Response('{"Source":"stale translation"}'));
}
const worker = vm.createContext({
  URL, console, Request, Response,
  self: { location: { origin }, addEventListener: (name, callback) => handlers.set(name, callback) },
  caches: { open: async () => ({
    match: async (request, options = {}) => cache.get(normalize(request.url || request, options.ignoreSearch))?.clone(),
    put: async (request, response) => cache.set(normalize(request.url || request, false), response.clone()),
  }) },
  fetch: async request => {
    const path = new URL(request.url).pathname;
    fetched.push(path);
    return new Response(fs.readFileSync('docs' + path));
  },
});
vm.runInContext(fs.readFileSync('docs/sw.js', 'utf8'), worker);
const requestAsset = async path => {
  let response;
  handlers.get('fetch')({ request: new Request(origin + path), respondWith: value => { response = value; } });
  assert(response, `Worker must cache the generated translation asset: ${path}`);
  const result = await response;
  assert(result?.ok, path);
  assert.deepEqual(Buffer.from(await result.arrayBuffer()), fs.readFileSync('docs' + path), path);
  assert(cache.has(origin + path), `Fresh asset must be retained for offline use: ${path}`);
};
(async () => {
  const resources = new Set();
  const deepPage = fs.readFileSync('docs/cases/aitl-cd30-negative.html', 'utf8');
  const geo = deepPage.match(/src="(\/geo-lang\.[a-f0-9]{12}\.js)"/);
  assert(geo, 'Deep source pages must use the shared geographic-language asset');
  resources.add(geo[1]);
  for (const locale of ['es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi']) {
    const page = fs.readFileSync(`docs/${locale}/try.html`, 'utf8');
    const script = page.match(/<script[^>]+src="(\/clinical-localization\.[a-f0-9]{12}\.js)"[^>]+data-catalog="([^"]+)"/);
    assert(script, `Generated ${locale} client must use versioned runtime and catalog`);
    assert.match(script[2], new RegExp(`^/${locale}/clinical-translations\\.[a-f0-9]{12}\\.json$`));
    for (const path of [script[1], script[2]]) {
      const fingerprint = path.match(/\.([a-f0-9]{12})\.(?:js|json)$/)[1];
      assert.equal(crypto.createHash('sha256').update(fs.readFileSync('docs' + path)).digest('hex').slice(0, 12), fingerprint, path);
      resources.add(path);
    }
  }
  for (const resource of resources) await requestAsset(resource);
  assert.equal(fetched.length, resources.size, 'Old canonical entries must not replace current versioned assets');
  worker.fetch = async () => { throw new Error('offline'); };
  for (const resource of resources) await requestAsset(resource);
  console.log(`PASS: all nine translated clients bypass stale cached runtime/catalogs and retain ${resources.size} current assets offline`);
})().catch(error => { console.error(error); process.exitCode = 1; });
