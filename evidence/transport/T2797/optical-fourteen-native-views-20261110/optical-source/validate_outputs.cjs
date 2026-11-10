// SPDX-License-Identifier: GPL-3.0-or-later
// Official Khronos conformance only. This does not establish rendered appearance.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const validatorPath = '/home/agent/.npm/_npx/c14427ece02cd616/node_modules/gltf-validator';
const validator = require(validatorPath);
assert.equal(require(path.join(validatorPath, 'package.json')).version, '2.0.0-dev.3.10');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const [listFile, output] = process.argv.slice(2);
assert(listFile && output && !fs.existsSync(output));
const files = JSON.parse(fs.readFileSync(listFile));
assert.equal(files.length, 4);
(async () => {
  const reports = [];
  for (const row of files) {
    const bytes = fs.readFileSync(row.path);
    assert.equal(sha(bytes), row.sha256);
    const result = await validator.validateBytes(new Uint8Array(bytes), {
      uri: path.basename(row.path), maxIssues: 10000,
      externalResourceFunction: async () => { throw Error('Self-contained GLB only'); },
    });
    reports.push({file: row.path, sha256: row.sha256, bytes: bytes.length, report: result});
    // Persist genuine nonconformance as well as the complete successful reports.
    fs.writeFileSync(output, JSON.stringify({official_validator: '2.0.0-dev.3.10',
      ignoredIssues: [], severityOverrides: {}, photographic_accepted: false,
      native_GLTFLoader_run: false, reports}, null, 2) + '\n');
    assert.equal(result.issues.numErrors, 0, row.path + ' validator errors');
    assert.equal(result.issues.numWarnings, 0, row.path + ' validator warnings');
    assert.equal(result.issues.truncated, false, row.path + ' truncated validator issues');
    assert.equal(sha(fs.readFileSync(row.path)), row.sha256);
  }
  assert.equal(reports.length, 4);
  console.log(JSON.stringify({official_validator: '2.0.0-dev.3.10', files: 4,
    zero_errors_warnings: true, truncated: false, photographic_accepted: false}));
})().catch(error => {console.error(error.stack ?? error); process.exitCode = 1;});
