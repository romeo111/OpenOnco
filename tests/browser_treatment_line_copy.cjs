const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('scripts/clinical-localization.js', 'utf8');
const copy = JSON.parse(source.match(/const treatmentLineCopy = (.*);/)[1]);
const translateCode = source.slice(source.indexOf('    const translate = text =>'), source.indexOf('    window.OPENONCO_DISPLAY_LABEL'));
const override = source.match(/    if \(treatmentLineCopy\[locale\]\) catalog\['first line'\] = treatmentLineCopy\[locale\];/)[0];
for (const locale of Object.keys(copy)) {
  const catalog = {'first line': 'literal row error'};
  const context = vm.createContext({locale, catalog, treatmentLineCopy:copy, nativeValues:new Set(), normalize:text=>text.replace(/\s+/g,' ').trim()});
  vm.runInContext(override + '\n' + translateCode + '\nglobalThis.display = translateOption;', context);
  const title = 'Canonical diagnosis — first line · ICD-10 C34';
  assert.equal(context.display(title), 'Canonical diagnosis — ' + copy[locale] + ' · ICD-10 C34');
  assert.equal(context.display('Canonical diagnosis · ICD-10 C34'), 'Canonical diagnosis · ICD-10 C34');
  assert.equal(context.display(context.display(title)), context.display(title));
  assert.equal(context.display('REG-EXAMPLE 20 mg'), 'REG-EXAMPLE 20 mg');
}
console.log('PASS: nine editions override stale row translations and retain diagnosis/ICD metadata');
