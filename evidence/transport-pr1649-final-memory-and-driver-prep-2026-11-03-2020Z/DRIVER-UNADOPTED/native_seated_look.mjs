// Actual vendored GLTFLoader, Meshopt, AnimationMixer and Float32 skin palettes.
// CPU only: real PNG/JPEG decoding via @napi-rs/canvas; no WebGL or scene claim.
import assert from 'node:assert/strict';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { registerHooks } from 'node:module';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [app, candidate, output] = process.argv.slice(2).map(p => path.resolve(p));
assert(app && candidate && output);
const engine = path.join(app, 'renderers/web/vendor/three-0.185.1');
registerHooks({ resolve(specifier, context, next) {
  if (specifier === 'three') return { url: pathToFileURL(path.join(engine, 'three.module.js')).href, shortCircuit: true };
  if (specifier.startsWith('three/addons/')) return { url: pathToFileURL(path.join(engine, specifier.slice(6))).href, shortCircuit: true };
  return next(specifier, context);
} });
const THREE = await import(pathToFileURL(path.join(engine, 'three.module.js')).href);
const { GLTFLoader } = await import(pathToFileURL(path.join(engine, 'addons/loaders/GLTFLoader.js')).href);
const { MeshoptDecoder } = await import(pathToFileURL(path.join(engine, 'addons/libs/meshopt_decoder.module.js')).href);
const { loadImage } = await import('./node-deps/node_modules/@napi-rs/canvas/index.js');
globalThis.self = globalThis;
globalThis.ProgressEvent = class ProgressEvent extends Event { constructor(type, init = {}) { super(type); Object.assign(this, init); } };
let decodedImages = 0;
globalThis.createImageBitmap = async blob => { const image = await loadImage(Buffer.from(await blob.arrayBuffer())); assert(image.width > 0 && image.height > 0); decodedImages++; return image; };
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const read = p => readFile(path.join(app, p));
const recipe = JSON.parse(await read('data/humans/animations/seated-driver-look-v2.json'));
const derivation = JSON.parse(await readFile(path.join(candidate, 'DERIVATION.json')));
const loops = JSON.parse(await read('data/transport/driven/loops.json'));
assert.equal(derivation.recipe_sha256, sha(await read('data/humans/animations/seated-driver-look-v2.json')));
assert.equal(derivation.generator_sha256, sha(await read('tools/human_seated_look.py')));
assert.equal(recipe.parents.length, 8);
const implementations = ['tools/human_seated_look.py', 'tools/human_natural_idle.py',
  'data/humans/animations/seated-driver-look-v2.json', 'data/transport/driven/loops.json',
  'tools/test_human_natural_idle.py', 'tools/test_driven_assembly.mjs',
  'renderers/web/js/main.js', 'renderers/web/js/town-transport.js', 'renderers/web/js/driven-assembly-loader.js',
  'renderers/web/vendor/three-0.185.1/three.module.js', 'renderers/web/vendor/three-0.185.1/three.core.js',
  'renderers/web/vendor/three-0.185.1/addons/loaders/GLTFLoader.js',
  'renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js'];
const pins = Object.fromEntries(await Promise.all(implementations.map(async p => [p, sha(await read(p))])));
pins.native_runner = sha(await readFile(new URL(import.meta.url)));
const candidatePins = Object.fromEntries(await Promise.all(recipe.parents.map(async row => [row.file, sha(await readFile(path.join(candidate, row.file)))])));
for (const row of derivation.files) assert.equal(candidatePins[row.file], row.sha256);
await mkdir(output, { recursive: false });
const report = { passed: false, scope: 'CPU-only actual loader/mixer/Float32 palettes and configured palm surfaces; no browser/WebGL/world/garment/photographic claim',
  recipe_sha256: pins['data/humans/animations/seated-driver-look-v2.json'], implementation_pins_before: pins,
  candidate_sha256_before: candidatePins, phases_per_file: 129, files: [], errors: [] };
const save = () => writeFile(path.join(output, 'RESULT.json'), JSON.stringify(report, null, 2) + '\n');
await save();
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
await MeshoptDecoder.ready;
const decode = async bytes => loader.parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '');
function play(gltf, clip) {
  const mixer = new THREE.AnimationMixer(gltf.scene), action = mixer.clipAction(clip);
  action.play(); mixer.update(0);
  const meshes = []; gltf.scene.traverse(node => { if (node.isSkinnedMesh) meshes.push(node); });
  assert(meshes.length > 0);
  const update = t => { mixer.setTime(t); gltf.scene.updateMatrixWorld(true); for (const mesh of meshes) mesh.skeleton.update(); };
  return { mixer, meshes, update };
}
function compare(old, now, record, bindings, fault = false) {
  const nowByName = new Map(now.meshes.map(mesh => [mesh.name, mesh]));
  const oldByName = new Map(old.meshes.map(mesh => [mesh.name, mesh]));
  const v = new THREE.Vector3(), w = new THREE.Vector3();
  for (let phase = 0; phase < 129; phase++) {
    const time = 8 * phase / 128;
    old.update(time); now.update(time);
    for (const oldMesh of old.meshes) {
      const mesh = nowByName.get(oldMesh.name); assert(mesh);
      assert.equal(mesh.skeleton.bones.length, oldMesh.skeleton.bones.length);
      const left = new Uint32Array(oldMesh.skeleton.boneMatrices.buffer), right = new Uint32Array(mesh.skeleton.boneMatrices.buffer);
      for (let i = 0; i < oldMesh.skeleton.bones.length; i++) {
        const a = oldMesh.skeleton.bones[i], b = mesh.skeleton.bones[i];
        assert.equal(a.name, b.name);
        if (!['neck_01', 'head'].includes(a.name)) {
          for (const property of ['position', 'quaternion', 'scale']) {
            const source = a[property].toArray(), target = b[property].toArray();
            source.forEach((v, k) => assert(Object.is(v, target[k]), `protected local transform changed ${a.name}.${property} phase${phase}`));
          }
        }
        let ancestor = a, headBranch = false;
        while (ancestor) { if (['neck_01', 'head'].includes(ancestor.name)) { headBranch = true; break; } ancestor = ancestor.parent; }
        if (headBranch) {
          record.max_head_neck_world_delta = Math.max(record.max_head_neck_world_delta, ...a.matrixWorld.elements.map((n, k) => Math.abs(n - b.matrixWorld.elements[k])));
          continue;
        }
        for (let k = 0; k < 16; k++) {
          assert(Object.is(a.matrixWorld.elements[k], b.matrixWorld.elements[k]), `protected transform changed ${a.name} phase${phase}${fault ? ' FAULT' : ''}`);
          assert.equal(left[i * 16 + k], right[i * 16 + k], `protected Float32 skin palette changed ${a.name} phase${phase}`);
        }
      }
    }
    for (const [side, binding] of Object.entries(bindings ?? {})) {
      const a = oldByName.get(binding.actual_body_mesh), b = nowByName.get(binding.actual_body_mesh); assert(a && b);
      const oldPoint = new THREE.Vector3(), newPoint = new THREE.Vector3();
      binding.actual_triangle_indices.forEach((index, i) => {
        a.getVertexPosition(index, v); v.applyMatrix4(a.matrixWorld); oldPoint.addScaledVector(v, binding.barycentric[i]);
        b.getVertexPosition(index, w); w.applyMatrix4(b.matrixWorld); newPoint.addScaledVector(w, binding.barycentric[i]);
      });
      const movement = oldPoint.distanceTo(newPoint);
      record.max_palm_delta_m = Math.max(record.max_palm_delta_m, movement);
      assert(movement <= 1e-9, `${side} palm changed at phase${phase}`);
      const existing = oldPoint.distanceTo(new THREE.Vector3().fromArray(binding.actual_point_vehicle_local_m));
      record.max_existing_palm_binding_error_m = Math.max(record.max_existing_palm_binding_error_m, existing);
      assert(existing <= 1e-9, `actual existing ${side} palm binding differs from loaded model`);
    }
    record.phases++;
  }
}
try {
  for (const row of recipe.parents) {
    const beforeImages = decodedImages;
    const parent = await read(row.file), child = await readFile(path.join(candidate, row.file));
    assert.equal(sha(parent), row.sha256);
    assert.equal(sha(child), candidatePins[row.file]);
    const a = await decode(parent), b = await decode(child);
    const oldClip = a.animations.find(clip => clip.name === 'sit_drive');
    const clip = b.animations.find(clip => clip.name === recipe.clip); assert(oldClip && clip);
    assert.equal(clip.duration, 8);
    const old = play(a, oldClip), now = play(b, clip);
    const bindings = row.web && row.asset_id === 'anonymous_working_driver_1904'
      ? loops.rows.find(r => r.driver_asset === row.asset_id).driver_palm_bindings_by_lod[String(row.lod)] : null;
    for (const binding of Object.values(bindings ?? {})) assert.equal(binding.asset_sha256, row.sha256);
    const record = { file: row.file, parent_sha256: row.sha256, child_sha256: candidatePins[row.file],
      phases: 0, max_head_neck_world_delta: 0, max_palm_delta_m: 0, max_existing_palm_binding_error_m: 0,
      protected_world_scope: 'all skeleton bones outside the authored neck/head descendant branch; all other local transforms including jaw/eyes remain bitexact',
      decoded_images: decodedImages - beforeImages, protected_float32_skin_palettes_bitexact: false, pelvis_3mm_fault_refused: false };
    compare(old, now, record, bindings);
    assert(record.max_head_neck_world_delta > .001, 'actual native head/neck motion absent');
    record.protected_float32_skin_palettes_bitexact = true;
    now.mixer.stopAllAction(); now.mixer.uncacheRoot(b.scene);
    const faulty = clip.clone(), pelvis = faulty.tracks.find(track => /^pelvis\.position$/.test(track.name)); assert(pelvis, 'actual pelvis track missing');
    for (let i = 0; i < pelvis.values.length; i += 3) pelvis.values[i] += .003;
    const wrong = play(b, faulty);
    try { compare(old, wrong, { phases: 0, max_head_neck_world_delta: 0, max_palm_delta_m: 0, max_existing_palm_binding_error_m: 0 }, bindings, true); }
    catch (error) { record.pelvis_3mm_fault_refused = /protected local transform changed|protected transform changed|protected Float32 skin palette/.test(String(error)); record.fault_reason = String(error); }
    assert(record.pelvis_3mm_fault_refused, '3mm pelvis control incorrectly passed');
    old.mixer.stopAllAction(); old.mixer.uncacheRoot(a.scene); wrong.mixer.stopAllAction(); wrong.mixer.uncacheRoot(b.scene);
    for (const model of [a, b]) model.scene.traverse(node => { if (node.isSkinnedMesh) node.skeleton.dispose(); if (node.isMesh) { node.geometry.dispose(); for (const material of Array.isArray(node.material) ? node.material : [node.material]) material.dispose(); } });
    report.files.push(record); await save();
    console.log(JSON.stringify(record));
  }
  report.implementation_pins_after = Object.fromEntries(await Promise.all(implementations.map(async p => [p, sha(await read(p))])));
  for (const p of implementations) assert.equal(report.implementation_pins_after[p], pins[p]);
  report.candidate_sha256_after = Object.fromEntries(await Promise.all(recipe.parents.map(async row => [row.file, sha(await readFile(path.join(candidate, row.file)))])));
  assert.deepEqual(report.candidate_sha256_after, candidatePins);
  report.passed = report.files.length === 8 && report.files.every(row => row.phases === 129 && row.protected_float32_skin_palettes_bitexact && row.pelvis_3mm_fault_refused);
  assert(report.passed);
} catch (error) { report.errors.push(error.stack ?? String(error)); process.exitCode = 1; }
await save();
console.log(JSON.stringify({ passed: report.passed, files: report.files.length, phases: report.files.reduce((n, row) => n + row.phases, 0), errors: report.errors }));
