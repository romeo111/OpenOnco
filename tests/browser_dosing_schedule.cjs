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
const frequencies = [
  ['es', 'al día', ['una vez', 'dos veces', 'tres veces']],
  ['pt', 'ao dia', ['uma vez', 'duas vezes', 'três vezes']],
  ['de', 'täglich', ['einmal', 'zweimal', 'dreimal']],
  ['fr', 'par jour', ['une fois', 'deux fois', 'trois fois']],
  ['it', 'al giorno', ['una volta', 'due volte', 'tre volte']],
  ['da', 'dagligt', ['en gang', 'to gange', 'tre gange']],
  ['sv', 'dagligen', ['en gång', 'två gånger', 'tre gånger']],
  ['nb', 'daglig', ['en gang', 'to ganger', 'tre ganger']],
  ['fi', 'päivässä', ['kerran', 'kahdesti', 'kolmesti']],
];
for (const [locale, period, counts] of frequencies) {
  ['once', 'twice', 'three times'].forEach((word, index) => {
    const original = `100 mg ${word} daily`;
    assert(context.check(original, `100 mg ${counts[index]} ${period}`, locale), locale);
    assert(!context.check(original, `100 mg ${period}`, locale), locale);
    assert(!context.check(original, `100 mg ${counts[(index + 1) % 3]} ${period}`, locale), locale);
    const weekly = editions.find(edition => edition[0] === locale)[2];
    assert(context.check(`100 mg ${word} weekly`, `100 mg ${counts[index]} ${weekly}`, locale), locale);
    assert(!context.check(`100 mg ${word} weekly`, `100 mg ${counts[(index + 1) % 3]} ${weekly}`, locale), locale);
  });
  assert(!context.check('100 mg daily', `100 mg ${counts[1]} ${period}`, locale), locale);
  assert(!context.check('100 mg once daily; 200 mg twice daily',
    `100 mg ${counts[1]} ${period}; 200 mg ${counts[0]} ${period}`, locale), locale);
}
assert(!context.check('100 mg once daily; 100 mg twice weekly', '100 mg deux fois par jour; 100 mg une fois hebdomadaire', 'fr'));
assert(source.includes('if (!preserveSchedule(source, translated, locale)) catalog[source] = source;'));
console.log('PASS: all nine dynamic editions retain unproven daily/weekly schedules as original text');
