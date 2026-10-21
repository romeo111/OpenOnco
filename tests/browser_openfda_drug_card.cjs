// Exercise the exact published JavaScript with synthetic FDA responses only.
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const site = process.argv[2] || 'docs';
const decode = text => text.replaceAll('&quot;', '"').replaceAll('&#x27;', "'").replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');
class Element {
  constructor(tag = 'div') { this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.listeners = {}; this._text = ''; }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  set innerHTML(_) { throw Error('HTML injection is forbidden'); }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this._text = ''; this.children = nodes; }
  setAttribute(key, value) { this.attrs[key] = value; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
}
const response = (body, status = 200) => ({ok: status === 200, status, json: async () => body});
const sample = () => ({meta: {last_updated: '2026-07-30', results: {skip: 0, limit: 5, total: 42}}, results: [{
  safetyreportid: '12345678', receivedate: '20260630', patient: {
    drug: [{medicinalproduct: 'TAGRISSO'}, {medicinalproduct: 'OTHER MEDICINE'}],
    reaction: [{reactionmeddrapt: '<img src=x onerror=alert(1)>'}, {reactionmeddrapt: 'Synthetic reaction'}],
  },
}]});
function fixture(locale, fetcher, customURL) {
  const page = fs.readFileSync(`${site}/${locale}kb/drugs/drug-osimertinib.html`, 'utf8');
  const tag = page.match(/<section[^>]*data-openfda-card[^>]*>/)[0];
  const root = new Element('section');
  root.dataset = {copy: decode(tag.match(/data-copy="([^"]*)"/)[1]), queryUrl: customURL || decode(tag.match(/data-query-url="([^"]*)"/)[1])};
  const copy = JSON.parse(root.dataset.copy), nodes = {};
  for (const name of ['load','status','updated','total','results']) nodes[name] = new Element(name === 'load' ? 'button' : 'div');
  root.querySelector = selector => nodes[selector.match(/data-openfda-(\w+)/)[1]];
  nodes.load.disabled = true;
  const scriptURL = page.match(/<script src="(\/openfda-drug-card\.[a-f0-9]+\.js)"/)[1];
  const script = fs.readFileSync(site + scriptURL, 'utf8');
  assert.equal(script, fs.readFileSync('scripts/openfda-drug-card.js', 'utf8').replaceAll('\r\n', '\n'));
  const calls = [], timers = new Map(); let timerId = 0;
  const context = vm.createContext({URL, URLSearchParams, Date, AbortController,
    document: {querySelectorAll: () => [root], createElement: tag => new Element(tag)},
    fetch: async (url, options) => { calls.push({url, options}); return fetcher(url, options); },
    setTimeout: callback => { timers.set(++timerId, callback); return timerId; },
    clearTimeout: id => timers.delete(id),
  });
  vm.runInContext(script, context);
  assert.equal(calls.length, 0, 'No FDA request during page load');
  return {root, nodes, copy, calls, timers, click: () => nodes.load.listeners.click?.()};
}
(async () => {
  for (const locale of ['', 'ukr/']) {
    let resolve;
    const f = fixture(locale, () => new Promise(r => { resolve = r; }));
    assert.equal(f.nodes.load.disabled, false);
    const pending = f.click();
    await f.click();
    assert.equal(f.calls.length, 1, 'Repeated click cannot duplicate an in-flight request');
    assert.equal(f.nodes.load.disabled, true);
    assert.equal(f.root.attrs['aria-busy'], 'true');
    resolve(response(sample())); await pending;
    assert.equal(f.nodes.updated.textContent, '2026-07-30');
    assert.equal(f.nodes.updated.children[0].dateTime, '2026-07-30');
    assert.equal(f.nodes.total.textContent, '42');
    assert.match(f.nodes.results.textContent, /2026-06-30/);
    assert.match(f.nodes.results.textContent, /TAGRISSO; OTHER MEDICINE/);
    assert.match(f.nodes.results.textContent, /<img src=x onerror=alert\(1\)>/);
    const all = node => [node, ...node.children.flatMap(all)];
    assert(!all(f.nodes.results).some(node => ['img','script'].includes(node.tagName)), 'Untrusted FDA text stays text');
    const link = all(f.nodes.results).find(node => node.tagName === 'a');
    assert.equal(new URL(link.href).searchParams.get('search'), 'safetyreportid:"12345678"');
    assert.equal(f.nodes.results.hidden, false);
    assert.equal(f.nodes.load.textContent, f.copy.refresh);
    assert.equal(f.nodes.load.disabled, false);
    assert.equal(f.timers.size, 0);
    assert.equal(f.calls[0].options.credentials, 'omit');
    assert.equal(f.calls[0].options.referrerPolicy, 'no-referrer');
    assert.equal(f.calls[0].options.cache, 'no-store');
    assert.equal(f.calls[0].options.redirect, 'error');
    const noMatch = fixture(locale, () => response({error: {code:'NOT_FOUND',message:'No matches found!'}},404));
    await noMatch.click();
    assert.equal(noMatch.nodes.total.textContent, '0');
    assert.equal(noMatch.nodes.updated.textContent, noMatch.copy.unknown);
    assert.equal(noMatch.nodes.status.textContent, noMatch.copy.empty);
    for (const fetcher of [
      () => response({error:{code:'NOT_FOUND',message:'Unknown endpoint'}},404),
      () => response(sample(),429), () => response(sample(),503),
      () => { throw Error('offline'); },
      () => ({ok:true,status:200,json:async () => {throw Error('bad JSON');}}),
      ...[null,[],{}, {results:[]}, {meta:{results:{total:0}},results:[{}]}, {meta:{results:{total:1}},results:[]}].map(body => () => response(body)),
    ]) {
      const error = fixture(locale, fetcher); await error.click();
      assert.equal(error.nodes.status.textContent, error.copy.error);
      assert.equal(error.nodes.total.textContent, '—');
      assert.equal(error.nodes.results.hidden, true);
      assert.equal(error.nodes.load.disabled, false);
      assert.equal(error.nodes.load.textContent, error.copy.retry);
      assert.equal(error.root.attrs['aria-busy'], 'false');
    }
    let attempts = 0;
    const retry = fixture(locale, () => {if (++attempts === 1) throw Error('offline'); return response(sample());});
    await retry.click(); await retry.click(); assert.equal(retry.nodes.total.textContent, '42');
    for (const date of [undefined, '2026-02-30', '2026-0730', '<svg onload=x>']) {
      const data = sample(); data.meta.last_updated = date;
      const missing = fixture(locale, () => response(data)); await missing.click();
      assert.equal(missing.nodes.updated.textContent, missing.copy.unknown);
    }
    const timeout = fixture(locale, (_url, options) => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(Error('timeout')));
    }));
    const loading = timeout.click(); [...timeout.timers.values()][0](); await loading;
    assert.equal(timeout.nodes.status.textContent, timeout.copy.error);
    assert.equal(timeout.nodes.load.disabled, false);
  }
  for (const url of ['https://example.org/?limit=5', 'https://api.fda.gov/drug/event.json?search=X&limit=1000', 'javascript:alert(1)']) {
    const f = fixture('', () => {throw Error('Must not fetch');}, url);
    await f.click(); assert.equal(f.calls.length, 0); assert.equal(f.nodes.load.disabled, true);
  }
  console.log('Published openFDA card passed EN/UK loading, provenance, XSS, empty/error, retry, timeout and request-boundary checks.');
})().catch(error => {console.error(error); process.exitCode = 1;});
