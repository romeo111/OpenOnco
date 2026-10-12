/* Actual generated worker must retain visited public Plan Builder pages. */
const fs=require('node:fs'), vm=require('node:vm'), assert=require('node:assert/strict');
const origin='https://openonco.info';
const prefixes=['','ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/'];
const stored=new Map(), handlers=new Map();
let mode='online', failOpen=false, failPut=false, puts=0, installed=false;
const path=request=>new URL(request.url||request,origin).pathname;
const cache={match:async request=>stored.get(path(request))?.clone(),put:async(request,response)=>{
  if(failPut) throw new Error('Quota'); puts++; stored.set(path(request),response.clone());
},add:async request=>{
  const filename='docs'+path(request);
  stored.set(path(request),new Response(fs.readFileSync(filename),{headers:{'Content-Type':filename.endsWith('.html')?'text/html':'application/octet-stream'}}));
}};
const worker=vm.createContext({URL,Request,Response,console,
  self:{location:{origin},addEventListener:(name,fn)=>handlers.set(name,fn),skipWaiting:async()=>{installed=true;}},
  caches:{open:async()=>{if(failOpen) throw Error('Storage unavailable');return cache;},match:cache.match},
  fetch:async(request,options)=>{
    assert.equal(options.cache,'no-store');
    if(mode==='offline') throw Error('Offline');
    if(mode==='http-error') return new Response('Unavailable',{status:503});
    if(mode==='json') return new Response('{"error":"Unexpected content"}',{headers:{'Content-Type':'application/json'}});
    const filename='docs'+path(request);
    return new Response(fs.existsSync(filename)?fs.readFileSync(filename):'Other page',{headers:{'Content-Type':filename.endsWith('.json')?'application/json':'text/html'}});
  },
});
vm.runInContext(fs.readFileSync('docs/sw.js','utf8'),worker);
function navigate(url,method='GET'){
  let result;
  handlers.get('fetch')({request:{url:new URL(url,origin).href,method,mode:'navigate'},respondWith:value=>{result=value;}});
  return result;
}
function retain(url,source=origin+url+'#p=TEST-DO-NOT-STORE'){
  let pending;
  handlers.get('message')({data:{type:'CACHE_PLAN_PAGE',path:url,html:'PRIVATE INPUT MUST NOT BE CACHED'},source:{url:source},waitUntil:value=>{pending=value;}});
  return pending;
}
(async()=>{
  let install;
  handlers.get('install')({waitUntil:value=>{install=value;}});
  await install;
  assert(installed);
  for(const prefix of prefixes){
    const url='/'+prefix+'try.html', expected=fs.readFileSync('docs'+url,'utf8');
    stored.delete(url);
    await retain(url);
    assert.equal(await stored.get(url).clone().text(),expected,'First visit activation must fetch the public shell, not persist the live form');
    stored.set(url,new Response('Old page',{headers:{'Content-Type':'text/html'}}));
    mode='online';
    assert.equal(await(await navigate(url)).text(),expected,'Online must show latest language shell');
    assert.equal(await stored.get(url).clone().text(),expected,'Visited shell must be retained');
    for(mode of ['offline','http-error','json']) assert.equal(await(await navigate(url)).text(),expected,'A failed/invalid fetch must preserve usable HTML');
    stored.delete(url); mode='offline';
    await assert.rejects(navigate(url),/Offline/);
    stored.set(url,new Response('{}',{headers:{'Content-Type':'application/json'}}));
    await assert.rejects(navigate(url),/Offline/);
    mode='online';failOpen=true;
    assert.equal(await(await navigate(url)).text(),expected,'Storage denial must not break online navigation');
    failOpen=false;failPut=true;
    assert.equal(await(await navigate(url)).text(),expected,'Quota failure must not break online navigation');
    failPut=false;
  }
  mode='online';const before=puts;
  for(const url of ['/try.html?case=TEST-DO-NOT-CACHE','/patient-profile.html','/api/profile','/cases/example.patient.html']) await navigate(url);
  assert.equal(puts,before,'Only the exact public allowlist may add navigation cache entries');
  assert.equal(navigate('https://other.example/try.html'),undefined);
  assert.equal(navigate('/try.html','POST'),undefined);
  assert.equal(retain('/patient-profile.html'),undefined);
  assert.equal(retain('/try.html?case=TEST-DO-NOT-STORE'),undefined);
  assert.equal(retain('/try.html',origin+'/try.html?case=TEST-DO-NOT-STORE'),undefined);
  assert.equal(retain('/try.html','https://other.example/try.html'),undefined);
  const page=fs.readFileSync('docs/try.html','utf8');
  const retainCode=page.match(/^function retainCurrentPlanPage\([^\n]*\{[\s\S]*?^\}/m)[0];
  const messages=[];
  let active={postMessage:data=>messages.push(data)};
  const client=vm.createContext({navigator:{serviceWorker:{get ready(){return Promise.resolve({active});}}},
    location:new Proxy({pathname:'/fr/try.html'},{get(target,name){assert.equal(name,'pathname','Client must not read or transmit query/hash/profile values');return target[name];}})});
  vm.runInContext('let retainedPlanWorker=null;'+retainCode,client);
  vm.runInContext('retainCurrentPlanPage();retainCurrentPlanPage();',client);
  await Promise.resolve();await Promise.resolve();
  assert.equal(messages.length,1,'Ready and controller-change notifications must not duplicate requests');
  assert.equal(messages[0].path,'/fr/try.html');
  active={postMessage:data=>messages.push(data)};
  vm.runInContext('retainCurrentPlanPage();',client);await Promise.resolve();await Promise.resolve();
  assert.equal(messages.length,2,'New active worker must retain the page on upgrade');
  for(const prefix of prefixes){
    const localized=fs.readFileSync('docs/'+prefix+'try.html','utf8');
    assert.equal(localized.match(/^function retainCurrentPlanPage\([^\n]*\{[\s\S]*?^\}/m)[0].replace(/\r\n/g,'\n'),retainCode.replace(/\r\n/g,'\n'));
  }
  console.log('All eleven visited Plan Builder shells: fresh online, retained offline, invalid-response recovery, quota/storage tolerance; query/private/API/POST/cross-origin writes excluded');
})().catch(error=>{console.error(error);process.exitCode=1;});
