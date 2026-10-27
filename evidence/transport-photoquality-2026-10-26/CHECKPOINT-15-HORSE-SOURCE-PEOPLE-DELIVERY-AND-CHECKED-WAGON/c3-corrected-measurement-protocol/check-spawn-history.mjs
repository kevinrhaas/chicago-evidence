// Source-only native history control; fake GPU setters, no renderer/browser.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
const COMMIT = 'c3d98a9d70308cac17b00e3adf3777a61ecc7cb0';
const repo = '/tmp/chicago-photo-worker-t2793-20261026';
const sourcePins = [];
function read(relative) {
  const path = 'chicago/4d/' + relative;
  const bytes = execFileSync('git', ['show', COMMIT + ':' + path], {
    cwd: repo, env: { ...process.env, GIT_NO_LAZY_FETCH: '1', GIT_OPTIONAL_LOCKS: '0' }, maxBuffer: 4 * 1024 * 1024,
  });
  sourcePins.push({ path, sha256: crypto.createHash('sha256').update(bytes).digest('hex'), bytes: bytes.length });
  return bytes.toString('utf8');
}
const tree = read('renderers/web/js/tree-instances.js');
const street = read('renderers/web/js/street-trees.js');
const main = read('renderers/web/js/main.js');
const scene = JSON.parse(read('data/scenes/1904.json'));
const rows = JSON.parse(read('data/street_trees/1904.json')).trees;
const spawn = { x: scene.spawn.local_e, z: -scene.spawn.local_n };
assert.deepEqual(scene.spawn, { local_e: 1410.12, local_n: -3218.01, yaw_deg: 264.94 });
const logic = tree.slice(tree.indexOf('    const dist = this.dist;'), tree.indexOf('    const dispose = () =>', tree.indexOf('    const dist = this.dist;')));
assert(logic.startsWith('    const dist = this.dist;') && logic.includes('const update ='));
const nearest = tree.slice(tree.indexOf('const ORDER ='), tree.indexOf('\nfunction hashString', tree.indexOf('function nearestLevel(')))
  .replace(/^const (WHOLE|_fade) =.*$/gm, '')
  + ['STEP_M', 'HYSTERESIS_M', 'JUMP_M'].map(n => tree.match(new RegExp('const ' + n + ' = [^;]+;'))[0]).join('\n');
const ringsCode = street.match(/const STREET_LEVELS = \{[\s\S]*?\n\};/)[0];
const rings = vm.runInNewContext(ringsCode + '\nSTREET_LEVELS');
const fadeS = Number(street.match(/const FADE_S = ([\d.]+);/)[1]);
const make = vm.runInNewContext(`(function(){const stats={};const fading=true;
 const sets={shade:['near','mid'],far:['mid','far','distant']};
 const show=(p,s,v)=>p.visible=v;const shape=(p,s,v,l)=>p.geometry=l;const fadeTo=(p,s,a)=>p.fade=a;
 ${nearest}\n${logic}\nreturn {update,stats,stems:this.stems};})`);
function build(detail = 'full') {
  const level = rings[detail];
  const pair = visible => ({ visible, fade: 1, geometry: 'distant' });
  const stems = rows.map(t => ({ id: t.id, x: t.e, z: -t.n, h: 20, lodK: 1,
    shade: false, level: 'distant', fade: null, culled: false,
    v: { tris: { near: 1, mid: 1, far: 1, distant: 1 } },
    inst: { shade: pair(false), far: pair(true) }, ghost: { shade: pair(false), far: pair(false) },
  }));
  return make.call({ dist: level, shadowM: level.mid, cullPerM: Infinity, distantM: level.distant, fadeS, stems });
}
const snapshot = f => JSON.stringify({ stats: f.stats, stems: f.stems.map(s => ({
  id: s.id, level: s.level, shade: s.shade, culled: s.culled, fade: s.fade,
  inst: s.inst, ghost: s.ghost,
})) });
const stateDiffs = (a, b) => a.stems.filter((s, i) => {
  const t = b.stems[i]; return s.level !== t.level || s.shade !== t.shade || !!s.fade !== !!t.fade;
}).map(s => s.id);
const historical = build(), oldFresh = build();
historical.update(spawn, 0); historical.update({ x: 1405, z: 3230 }, 0);
oldFresh.update({ x: 1405, z: 3230 }, 0);
const historicalDifferences = stateDiffs(historical, oldFresh);
assert.equal(historicalDifferences.length, 9);
assert.equal(historical.stats.fading, 8);
const initial = build(), fresh = build();
initial.update(spawn, 0); initial.update(spawn, 0); fresh.update(spawn, 0);
assert.equal(snapshot(initial), snapshot(fresh));
const initialState = snapshot(initial);
for (let i = 0; i < 15; i++) initial.update(spawn, 0);
assert.equal(snapshot(initial), initialState);
// Native tree update depends on XZ; actual900m eviction and return retain XZ.
initial.update({ ...spawn, y: 900 }, 0); initial.update({ ...spawn, y: 5.7 }, 0);
assert.equal(snapshot(initial), initialState);
const balanced = build('balanced'); balanced.update(spawn, 0);
const rebuiltFull = build(); rebuiltFull.update(spawn, 0);
for (let i = 0; i < 15; i++) rebuiltFull.update(spawn, 0);
assert.equal(snapshot(initial), snapshot(rebuiltFull));
assert.equal(stateDiffs(initial, rebuiltFull).length, 0);
// Actual street-tree wind accumulator/update closure, isolated from GPU setters.
const windStart = street.indexOf('  let wind = 0;');
const windEnd = street.indexOf('  /** Finish every dissolve', windStart);
assert(windStart > street.indexOf('  await build(') && windEnd > windStart);
const makeWind = vm.runInNewContext(`(function(){let forest=null;const stats={};const out={};const uWind={value:0};
 ${street.slice(windStart, windEnd)}
 return {out,uWind,setForest(value){forest=value}};})`);
const wind = makeWind(); const sharedUniform = wind.uWind;
wind.setForest({ update() {}, stats: { triangles: 1 } });
wind.out.update(.1375, { position: spawn }); const windBefore = wind.uWind.value;
wind.setForest({ update() {}, stats: { triangles: 2 } });
for (let i = 0; i < 15; i++) wind.out.update(0, { position: spawn });
wind.setForest({ update() {}, stats: { triangles: 3 } });
for (let i = 0; i < 15; i++) wind.out.update(0, { position: spawn });
assert.equal(wind.uWind, sharedUniform); assert.equal(wind.uWind.value, windBefore);
assert(street.indexOf('  const uWind = { value: 0 };') < street.indexOf('  const build = async'));
assert.equal((street.match(/const uWind =/g) || []).length, 1);
assert(main.includes('const frameDt = animationHold || gateOpen ? 0 : elapsed;'));
assert(main.includes('const dt = Math.min(frameDt, 0.05);'));
assert(main.includes('streetTrees.update(dt, camera);'));
const result = {
  status: 'PASS_SOURCE_STATE_ONLY', immutable_commit: COMMIT, source_pins: sourcePins,
  native_spawn: scene.spawn, native_street_tree_records: rows.length,
  historical_negative_control: { differences: historicalDifferences.length, fading: historical.stats.fading },
  spawn_to_spawn_vs_fresh_spawn: { exact_state_equal: true, differences: 0, stats: initial.stats },
  original15held_dt0_steps_preserve_equal_state: true,
  native900m_sameXZ_eviction_and_return_preserve_equal_tree_state: true,
  balanced_then_fresh_full_at_spawn_matches_initial_full: true,
  wind: { actual_native_update_closure: true, retained_uniform_identity: true, before: windBefore, after: wind.uWind.value,
    source_fact: 'wind and uWind/mats live outside the per-detail forest build; held native dt0 does not advance them' },
  limitations: 'Source-extracted native update/nearest logic and actual407street-tree positions; fake batch setters/template triangle counts; context-city trees/GPU/shadows/pixels/async rebuild completion not qualified. Wind test changes only the closure forest pointer, not a real GPU build.',
  actual_corrected_GPU_run: 'UNRUN', historical_pixel_NONPASS: 'UNCHANGED', production_edits: false, browser_launched: false,
};
fs.writeFileSync(new URL('SOURCE-HISTORY-CONTROL-RESULT.json', import.meta.url), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result));
