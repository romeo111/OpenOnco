// Exercise the deployed client's failure paths without a network or patient data.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('docs/try.html', 'utf8');
function section(start, end) {
  const index = html.indexOf(start);
  assert(index >= 0);
  const stop = html.indexOf(end, index);
  assert(stop > index);
  return html.slice(index, stop);
}
const moduleCode = section('async function validateDiseaseModule()', '// ── Pyodide loader');
const initializationCode = section('let engineLoadPromise = null;', '// ── Generate full plan');
const generationCode = section('async function runEngine()', 'function setGeneratingUI');
function fixture({ cached = null, valid = true, httpOk = true, coreValid = true } = {}) {
  const calls = { initializations: 0, validations: 0, fetches: 0, removed: 0, unpacked: 0, errors: [], generated: 0 };
  const context = vm.createContext({
    console: { warn() {}, log() {} }, Uint8Array, ArrayBuffer,
    atob: value => Buffer.from(value, 'base64').toString('binary'),
    btoa: value => Buffer.from(value, 'binary').toString('base64'),
    localStorage: { getItem: () => cached, removeItem() { calls.removed++; cached = null; }, setItem() {} },
    fetch: async () => { calls.fetches++; return { ok: httpOk, status: 503, arrayBuffer: async () => new ArrayBuffer(1) }; },
    fake: { unpackArchive() { calls.unpacked++; }, runPythonAsync: async code => {
      if (code.includes('_module_validation')) { calls.validations++; return valid; }
      return coreValid ? 'ok' : 'schema(1): invalid fixture';
    }, globals: { set() { calls.generated++; } }, loadPackage: async () => {} },
    refreshBuildPanel: async () => {}, setStatus() {}, setLoadingProgress() {}, yieldToBrowser: async () => {},
    initStageStart() {}, initStageDone() {}, initStageError() {},
    ensurePyodideLoader: async () => async () => { calls.initializations++; return context.fake; },
    loadCoreBundle: async () => {}, setError(error) { if (error) calls.errors.push(error); },
    performance: { now: () => 0 }, buildProfile: () => ({ disease: { id: 'DIS-ONE' } }),
    resolveDiseaseId: () => 'DIS-ONE', setGeneratingUI() {}, updateRunBtnEnabled() {},
    initShow() {}, initHide() {}, setTimeout() {}, scheduleOfflineCacheWarmup() {},
    updateWorkflowControls() {}, initStagesReset() {},
  });
  vm.runInContext(`let pyodide=fake, enginReady=false, coreBundleLoaded=true;
    const loadedDiseases=new Set(); const bundleIndex={diseases:{'DIS-ONE':'disease/one.zip'},disease_versions:{}};
    let uiBusy=false,generating=false,planSource=null;
    let evalDebounceTimer=null,whatIfDebounceTimer=null,previewToken=0,whatIfToken=0;
    const runBtn={disabled:false}; const mainTryEl={inert:false};`, context);
  vm.runInContext(moduleCode + initializationCode + generationCode, context);
  return { context, calls, run: code => vm.runInContext(code, context) };
}
(async () => {
  let f = fixture({ cached: 'AA==' });
  await f.run("loadDiseaseModule('DIS-ONE')");
  assert.equal(f.calls.validations, 1); assert.equal(f.calls.fetches, 0);
  assert.equal(f.run("loadedDiseases.has('DIS-ONE')"), true);
  f = fixture({ cached: 'AA==', valid: false });
  await assert.rejects(f.run("loadDiseaseModule('DIS-ONE')"), /validation failed/);
  assert.equal(f.calls.removed, 1); assert.equal(f.calls.validations, 2);
  assert.equal(f.run("loadedDiseases.has('DIS-ONE')"), false);
  f = fixture({ httpOk: false });
  f.context.ensureEngine = async () => {};
  await f.run('runEngine()');
  assert.equal(f.calls.generated, 0);
  assert(f.calls.errors.some(error => error.includes('module failed to load')));
  assert.equal(f.run('generating'), false);
  f = fixture({ coreValid: false });
  await assert.rejects(f.run('ensureEngine()'), /validation failed/);
  assert.equal(f.run('enginReady'), false); assert.equal(f.run('coreBundleLoaded'), false);
  assert.equal(f.run('engineLoadPromise'), null);
  f.context.fake.runPythonAsync = async () => 'ok';
  await f.run('ensureEngine()');
  assert.equal(f.run('enginReady'), true);
  assert.equal(f.calls.initializations, 2);
  f = fixture();
  await Promise.all([f.run('ensureEngine()'), f.run('ensureEngine()')]);
  assert.equal(f.calls.initializations, 1);
  for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/']) {
    const page = fs.readFileSync('docs/' + prefix + 'try.html', 'utf8');
    assert.equal((page.match(/await validateDiseaseModule\(\);/g) || []).length, 2);
    assert(page.includes("if (validationSummary !== 'ok')"));
    assert(!page.includes('failed (continuing)'));
  }
  console.log('PASS: cache validation, invalid-cache fallback, invalid-network rejection, generation blocked on download failure, invalid core rejection and retry; six language clients guarded');
})().catch(error => { console.error(error); process.exitCode = 1; });
