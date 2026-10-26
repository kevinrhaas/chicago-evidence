#!/usr/bin/env node
// Exercise the actual observer's manifest validator without evaluating its browser entrypoint.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const dir = path.dirname(fileURLToPath(import.meta.url));
const source = await fs.readFile(path.join(dir, 'observe-lifecycle.mjs'), 'utf8');
const start = source.indexOf('function validateRuntimeManifest(bytes) {');
const end = source.indexOf('\nconst manifestBytes =', start);
assert(start >= 0 && end > start, 'Actual observer validator definition must be present');
const validate = new vm.Script(`${source.slice(start, end)}\nvalidateRuntimeManifest`).runInNewContext();
const paths = ['renderers/web/js/ktx2.js', 'renderers/web/js/texture-residency.js', 'renderers/web/js/main.js'];
const valid = paths.map((p, i) => ({ path: p, proposed_sha256: String(i + 1).repeat(64) }));
const invoke = (rows) => validate(Buffer.from(JSON.stringify(rows)));
let checks = 0;
function pass(label, fn) { fn(); checks++; console.log(`PASS ${label}`); }
pass('actual complete three-path manifest accepted', () => assert.equal(invoke(valid).length, 3));
pass('path order does not alter completeness', () => assert.equal(invoke([...valid].reverse()).length, 3));
pass('uppercase hexadecimal SHA-256 accepted', () => assert.equal(invoke(valid.map((r) => ({ ...r, proposed_sha256: 'A'.repeat(64) })))[0].proposed_sha256, 'a'.repeat(64)));
pass('empty manifest rejected', () => assert.throws(() => invoke([]), /exactly the three/));
pass('partial manifest rejected', () => assert.throws(() => invoke(valid.slice(0, 2)), /exactly the three/));
pass('duplicate runtime path rejected', () => assert.throws(() => invoke([valid[0], valid[0], valid[2]]), /Duplicate/));
pass('unknown runtime path rejected', () => assert.throws(() => invoke([valid[0], valid[1], { ...valid[2], path: 'renderers/web/js/unknown.js' }]), /Unknown/));
pass('non-runtime path rejected', () => assert.throws(() => invoke([valid[0], valid[1], { ...valid[2], path: 'tools/check.sh' }]), /Unknown/));
pass('extra rows rejected', () => assert.throws(() => invoke([...valid, valid[0]]), /exactly the three/));
pass('short hash rejected', () => assert.throws(() => invoke([valid[0], valid[1], { ...valid[2], proposed_sha256: 'a'.repeat(63) }]), /Invalid/));
pass('nonhex hash rejected', () => assert.throws(() => invoke([valid[0], valid[1], { ...valid[2], proposed_sha256: 'x'.repeat(64) }]), /Invalid/));
pass('numeric hash rejected', () => assert.throws(() => invoke([valid[0], valid[1], { ...valid[2], proposed_sha256: 123 }]), /Invalid/));
pass('missing hash rejected', () => assert.throws(() => invoke([valid[0], valid[1], { path: valid[2].path }]), /Invalid/));
pass('null row rejected', () => assert.throws(() => invoke([valid[0], valid[1], null]), /Unknown/));
pass('nonarray manifest rejected', () => assert.throws(() => invoke({ rows: valid }), /exactly the three/));
pass('malformed JSON rejected', () => assert.throws(() => validate(Buffer.from('{'))));
const result = { status: 'PASS', controls: checks, scope: 'Actual observer validator only; no browser entrypoint evaluated or browser launched' };
await fs.writeFile(path.join(dir, 'MANIFEST-VALIDATION-RESULT.json'), `${JSON.stringify(result, null, 2)}\n`);
console.log(`${checks} actual manifest-validation controls PASS`);
