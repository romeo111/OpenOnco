/* Exercise the exact guard used before dynamic report translation. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('scripts/clinical-localization.js', 'utf8');
const guard = source.split('// BEGIN dosing schedule guard:')[1].split('// END dosing schedule guard.')[0];
const context = vm.createContext({});
vm.runInContext('// ' + guard + '\nglobalThis.check = preserveSchedule;', context);
const editions = [
  ['es', 'al día', 'semanalmente'], ['pt', 'ao dia', 'semanalmente'],
  ['de', 'täglich', 'wöchentlich'], ['fr', 'par jour', 'hebdomadaire'],
  ['it', 'al giorno', 'settimanale'], ['da', 'dagligt', 'ugentligt'],
  ['sv', 'dagligen', 'varje vecka'], ['nb', 'daglig', 'ukentlig'],
  ['fi', 'päivittäin', 'viikoittain'],
];
for (const [locale, daily, weekly] of editions) {
  for (const [cadence, native] of [['daily', daily], ['weekly', weekly]]) {
    assert(context.check(`100 mg ${cadence}`, `100 mg ${native}`, locale), locale);
    assert(!context.check(`100 mg ${cadence}`, '100 mg', locale), locale);
    assert(context.check(`100 mg ${cadence}`, `100 mg ${cadence}`, locale), locale);
  }
  assert(!context.check('100 mg weekly', `100 mg ${daily}`, locale), locale);
  assert(!context.check('100 mg daily', `100 mg ${weekly}`, locale), locale);
  assert(!context.check('100 mg weekly', `100 mg ${daily}; ${weekly}`, locale), locale);
}
assert(context.check('100 mg', '100 mg', 'unknown'));
assert(!context.check('100 mg daily', '100 mg', 'unknown'));
assert(source.includes('if (!preserveSchedule(source, translated, locale)) catalog[source] = source;'));
console.log('PASS: all nine dynamic editions retain unproven daily/weekly schedules as original text');
