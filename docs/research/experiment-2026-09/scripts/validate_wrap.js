// Runs avoid-ai-writing's preservation validator (MIT, detector/validate.js) and prints JSON.
const path = process.argv[2];
const v = require(path);
const fs = require('node:fs');
const r = v.validate(fs.readFileSync(process.argv[3], 'utf8'), fs.readFileSync(process.argv[4], 'utf8'), { residualPolicy: 'warn' });
console.log(JSON.stringify({ ok: r.preservation ? r.preservation.ok : r.ok, errors: r.errors.map(e => e.code), warnings: r.warnings.map(w => w.code) }));
