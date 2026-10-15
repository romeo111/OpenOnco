/* Run the complete display runtime against stale labels, preserving input data. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('scripts/clinical-localization.js', 'utf8');
const copy = JSON.parse(source.match(/const patientContactCopy = (.*);/)[1]);

(async () => {
  for (const [locale, messages] of Object.entries(copy)) {
    const parent = {closest: () => null};
    const nodes = Object.keys(messages).map(nodeValue => ({nodeValue, parentElement: parent}));
    const profileInput = {value: '{"temperature":38,"contact":"source-defined","dose":"100 mg"}'};
    const before = profileInput.value;
    const staleCatalog = Object.fromEntries(Object.keys(messages).map(key => [key, 'Discuss at next visit']));
    let requests = 0;
    const document = {
      currentScript: {dataset: {locale}},
      documentElement: {lang: 'en', dataset: {}},
      getElementById: id => id === 'patientJson' ? profileInput : null,
      createTreeWalker: (root, show, filter) => {
        let index = 0;
        return {nextNode: () => {
          while (index < nodes.length) {
            const node = nodes[index++];
            if (filter.acceptNode(node) === 1) return node;
          }
          return null;
        }};
      },
    };
    document.body = {nodeType: 1, ownerDocument: document, matches: () => false,
      querySelectorAll: () => [], closest: () => null, hasAttribute: () => false};
    const window = {};
    const context = vm.createContext({document, window, console, Set, WeakSet, URL,
      location: {origin: 'https://openonco.info'},
      Node: {ELEMENT_NODE: 1, TEXT_NODE: 3},
      NodeFilter: {SHOW_TEXT: 4, FILTER_ACCEPT: 1, FILTER_REJECT: 2},
      MutationObserver: class {observe() {} disconnect() {}},
      fetch: async () => { requests++; return {ok: true, json: async () => staleCatalog}; },
    });
    vm.runInContext(source, context);
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(requests, 1);
    assert.notEqual(document.documentElement.dataset.translationRuntime, 'unavailable');
    assert.equal(window.OPENONCO_REPORT_LOCALE, locale);
    for (let index = 0; index < nodes.length; index++) {
      const key = Object.keys(messages)[index];
      assert.equal(nodes[index].nodeValue, messages[key], `${locale}: ${key}`);
      assert.equal(window.OPENONCO_DISPLAY_LABEL(messages[key]), messages[key]);
    }
    assert.notEqual(messages['Tell your doctor or nurse'], messages['Contact your doctor or nurse immediately']);
    assert.equal(window.OPENONCO_DISPLAY_LABEL('REG-EXAMPLE 100 mg'), 'REG-EXAMPLE 100 mg');
    assert.equal(profileInput.value, before);
  }
  console.log('PASS: complete runtime overrides stale contact headings in nine languages; input data unchanged');
})().catch(error => { console.error(error); process.exitCode = 1; });
