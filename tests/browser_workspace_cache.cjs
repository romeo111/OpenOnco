/* Execute the shipped worker: public form data must stay fresh and survive offline. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const origin = 'https://openonco.info';
const paths = ['/questionnaires.json', '/examples.json'];
const stored = new Map(), handlers = new Map(), requests = [];
let networkMode = 'online', failPut = false, failOpen = false, failMatch = false, installed = false;
const key = request => new URL(request.url || request, origin).pathname;
const cache = {
  match: async request => { if (failMatch) throw new Error('Storage unavailable'); return stored.get(key(request))?.clone(); },
  put: async (request, response) => { if (failPut) throw new Error('Storage full'); stored.set(key(request), response.clone()); },
  add: async () => {},
};
const worker = vm.createContext({
  URL, Request, Response, console,
  self: {location:{origin},addEventListener:(name,fn)=>handlers.set(name,fn),skipWaiting:async()=>{installed=true;}},
  caches:{open:async()=>{ if (failOpen) throw new Error('Storage unavailable'); return cache; }},
  fetch:async (request, options) => {
    requests.push({url:request.url, options});
    if (networkMode === 'offline') throw new Error('Offline');
    if (networkMode === 'http-error') return new Response('Unavailable',{status:503});
    if (networkMode === 'html') return new Response('<html>Gateway error</html>');
    if (networkMode === 'object') return new Response('{"error":"Unavailable"}');
    if (networkMode === 'array-error') return new Response('[{"error":"Unavailable"}]');
    return new Response(fs.readFileSync('docs'+key(request)),{headers:{'Content-Type':'application/json'}});
  },
});
vm.runInContext(fs.readFileSync('docs/sw.js','utf8'),worker);
function request(path, options = {}) {
  let pending;
  handlers.get('fetch')({request:new Request(new URL(path,origin),options),respondWith:value=>{pending=value;}});
  return pending;
}
(async()=>{
  let install;
  handlers.get('install')({waitUntil:value=>{install=value;}});
  await install;
  assert(installed);
  for (const path of paths) {
    assert.deepEqual(await stored.get(path).clone().json(),JSON.parse(fs.readFileSync('docs'+path)), 'First install must retain valid public data');
    stored.set(path,new Response('[{"id":"old"}]'));
    const fresh=await request(path);
    assert.deepEqual(await fresh.json(),JSON.parse(fs.readFileSync('docs'+path)), 'Online response must bypass stale data');
    assert.equal(requests.at(-1).options.cache,'no-store');
    for (networkMode of ['offline','http-error','html','object','array-error']) {
      assert.deepEqual(await (await request(path)).json(),JSON.parse(fs.readFileSync('docs'+path)), 'Only a valid cached catalog may recover a failed fetch');
    }
    stored.delete(path);
    await assert.rejects(request(path));
    stored.set(path,new Response('invalid cached JSON'));
    await assert.rejects(request(path));
    networkMode='online'; failPut=true;
    assert.deepEqual(await (await request(path)).json(),JSON.parse(fs.readFileSync('docs'+path)), 'Cache quota must not break a working online form');
    failPut=false;
    failOpen=true;
    assert.deepEqual(await (await request(path)).json(),JSON.parse(fs.readFileSync('docs'+path)), 'Unavailable CacheStorage must not block the network');
    failOpen=false; failMatch=true; networkMode='offline';
    await assert.rejects(request(path),/Offline/);
    failMatch=false; networkMode='online';
  }
  assert.equal(request('https://third-party.example/questionnaires.json'),undefined);
  assert.equal(request('/questionnaires.json',{method:'POST',body:'TEST-DO-NOT-CACHE'}),undefined);
  assert.equal(request('/api/clinical-question'),undefined);
  assert.equal(request('/patient-profile.json'),undefined);
  networkMode='offline'; installed=false;
  handlers.get('install')({waitUntil:value=>{install=value;}});
  await install;
  assert(installed,'Unavailable public data must not prevent worker installation');
  console.log('Public catalogs: fresh online, validated offline fallback, cold-install precache, corruption/quota handling; private/API/POST/cross-origin requests untouched');
})().catch(error=>{console.error(error);process.exitCode=1;});
