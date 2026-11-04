// CPU diagnostic only. No asset mutation, new geometry export or coverage PASS.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { registerHooks } from 'node:module';
import { pathToFileURL } from 'node:url';

if (process.argv.includes('--help')) {
  console.log('diagnose_native_coverage.mjs CONFIG_JSON FRESH_OUTPUT_DIRECTORY');
  process.exit(0);
}
const [configFile, output] = process.argv.slice(2);
assert(configFile && output);
const cfg = JSON.parse(await fs.readFile(configFile, 'utf8'));
assert.equal(cfg.template_only, false);
assert.equal(cfg.ROOT_EXPLICIT_GARMENT_DIAGNOSTIC_GO, true);
assert.equal(cfg.protocol, 'NATIVE_SEATED_COVERAGE_DIAGNOSTIC_V1_NOT_ACCEPTANCE');
assert.deepEqual(cfg.phases_seconds, [0, 2, 4, 6]);
assert.equal(cfg.sample_count_per_body_mesh, 192);
assert.equal(cfg.ray_half_length_m, 0.08);
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
for (const [file, digest] of Object.entries(cfg.input_pins)) assert.equal(sha(await fs.readFile(file)), digest, file);
await fs.mkdir(output, { recursive: false });
const report = { status: 'ACTIVE_NATIVE_COVERAGE_DIAGNOSTIC_NOT_PASS',
  scope: 'Finite CPU ray comparisons on native posed geometry; no new asset, garment acceptance, GPU, world or photographic claim.',
  config_sha256: sha(await fs.readFile(configFile)), input_pins: cfg.input_pins,
  sample_plan: { phases_seconds: cfg.phases_seconds, samples_per_body_mesh: 192,
    selection: 'Uniform deterministic triangle indices across the entire LOD3 body, before reference-coverage eligibility; no favourable region filtering.',
    ray_half_length_m: 0.08, ray_range_is_search_extent_not_quality_tolerance: true },
  original_1032_motion_controls_replaced_or_weakened: false, cases: [], errors: [] };
const save = async () => fs.writeFile(path.join(output, 'RESULT.json'), JSON.stringify(report, null, 2) + '\n');
await save();
const engine = path.join(cfg.app, 'renderers/web/vendor/three-0.185.1');
registerHooks({ resolve(specifier, context, next) {
  if (specifier === 'three') return { url: pathToFileURL(path.join(engine, 'three.module.js')).href, shortCircuit: true };
  if (specifier.startsWith('three/addons/')) return { url: pathToFileURL(path.join(engine, specifier.slice(6))).href, shortCircuit: true };
  return next(specifier, context);
} });
const THREE = await import(pathToFileURL(path.join(engine, 'three.module.js')).href);
const { GLTFLoader } = await import(pathToFileURL(path.join(engine, 'addons/loaders/GLTFLoader.js')).href);
const { MeshoptDecoder } = await import(pathToFileURL(path.join(engine, 'addons/libs/meshopt_decoder.module.js')).href);
const { loadImage } = await import(pathToFileURL(cfg.native_canvas_module).href);
globalThis.self = globalThis;
globalThis.ProgressEvent = class ProgressEvent extends Event {
  constructor(type, init = {}) { super(type); Object.assign(this, init); }
};
let decodedImages = 0;
globalThis.createImageBitmap = async blob => {
  const image = await loadImage(Buffer.from(await blob.arrayBuffer()));
  assert(image.width > 0 && image.height > 0); decodedImages++; return image;
};
await MeshoptDecoder.ready;
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const decode = async file => {
  const bytes = await fs.readFile(file);
  return loader.parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '');
};
const materialNames = mesh => (Array.isArray(mesh.material) ? mesh.material : [mesh.material]).map(m => m.name);
const rawBytes = array => Buffer.from(array.buffer, array.byteOffset, array.byteLength);
function play(gltf) {
  const clip = gltf.animations.find(a => a.name === 'sit_drive_look_v2');
  assert(clip && clip.duration === 8, 'Use the actual current public driver look clip.');
  const mixer = new THREE.AnimationMixer(gltf.scene);
  mixer.clipAction(clip).play(); mixer.update(0);
  const meshes = [];
  gltf.scene.traverse(node => { if (node.isSkinnedMesh) meshes.push(node); });
  assert(meshes.length > 0);
  const originalPositions = new Map(meshes.map(m => [m.name, sha(rawBytes(m.geometry.attributes.position.array))]));
  return { gltf, mixer, meshes, originalPositions,
    update(t) { mixer.setTime(t); gltf.scene.updateMatrixWorld(true); for (const mesh of meshes) mesh.skeleton.update(); },
    verifyUnchanged() { for (const mesh of meshes) assert.equal(sha(rawBytes(mesh.geometry.attributes.position.array)), originalPositions.get(mesh.name)); } };
}
// Native getVertexPosition evaluates the real loader's morph and skin code. A
// temporary identity-transform CPU mesh retains every original triangle and
// Float64 world position, so rays do not repeatedly evaluate the same skeleton.
// This is not a replacement asset or an approximation to a different rig.
function bakeForRays(mesh) {
  const values = new Float64Array(mesh.geometry.attributes.position.count * 3), v = new THREE.Vector3();
  for (let i = 0; i < mesh.geometry.attributes.position.count; i++) {
    mesh.getVertexPosition(i, v).applyMatrix4(mesh.matrixWorld);
    assert(v.toArray().every(Number.isFinite)); values.set(v.toArray(), i * 3);
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(values, 3));
  assert(mesh.geometry.index, 'Current driver exports must be indexed.');
  geometry.setIndex(mesh.geometry.index.clone());
  geometry.computeBoundingBox(); geometry.computeBoundingSphere();
  const flat = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }));
  flat.name = mesh.name; flat.userData.originalMaterials = materialNames(mesh); flat.updateMatrixWorld(true);
  return flat;
}
const ray = new THREE.Raycaster();
function hits(meshes, point, normal, half = cfg.ray_half_length_m) {
  ray.set(point.clone().addScaledVector(normal, -half), normal);
  ray.near = 0; ray.far = 2 * half;
  return ray.intersectObjects(meshes, false).map(hit => ({
    mesh: hit.object.name, material: hit.object.userData.originalMaterials,
    face_index: hit.faceIndex, signed_distance_m: hit.distance - half,
    face_normal_dot_axis: hit.face.normal.dot(normal), point_m: hit.point.toArray() }));
}
function signedSummary(rows) {
  return { hit_count: rows.length,
    nearest_to_sample_m: rows.length ? rows.reduce((a, b) => Math.abs(a.signed_distance_m) < Math.abs(b.signed_distance_m) ? a : b).signed_distance_m : null,
    maximum_outward_m: rows.length ? Math.max(...rows.map(r => r.signed_distance_m)) : null,
    outward_hits: rows.filter(r => r.signed_distance_m > 0).length };
}
function boneLabels(mesh, indices) {
  const skin = mesh.geometry.attributes.skinIndex, weights = mesh.geometry.attributes.skinWeight, mass = new Map();
  for (const i of indices) for (let k = 0; k < 4; k++) {
    const joint = skin.getComponent(i, k), weight = weights.getComponent(i, k);
    const name = mesh.skeleton.bones[joint].name;
    mass.set(name, (mass.get(name) ?? 0) + weight / 3);
  }
  return [...mass].sort((a, b) => b[1] - a[1]).slice(0, 6);
}
function costs(model, file) {
  const textures = new Set(), rows = [];
  for (const mesh of model.meshes) {
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    for (const mat of materials) for (const value of Object.values(mat)) if (value?.isTexture) textures.add(value);
    rows.push({ mesh: mesh.name, materials: materials.map(m => ({ name: m.name, transparent: m.transparent, alphaTest: m.alphaTest, side: m.side })),
      vertices: mesh.geometry.attributes.position.count, triangles: mesh.geometry.index.count / 3 });
  }
  return { file, triangles: rows.reduce((n, r) => n + r.triangles, 0),
    vertices: rows.reduce((n, r) => n + r.vertices, 0), draws: rows.length, meshes: rows,
    textures: [...textures].map(t => ({ name: t.name, width: t.image?.width, height: t.image?.height })),
    meaning: 'Actual selected asset costs; no invented per-human ceiling or world-budget waiver.' };
}
try {
  // Three native Raycaster calibrations catch sign, missed-hit and false-cover
  // mistakes before interpreting source geometry. They never modify an asset.
  const origin = new THREE.Vector3(), normal = new THREE.Vector3(0, 0, 1);
  function plane(z) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }));
    m.position.z = z; m.userData.originalMaterials = ['synthetic_calibration_only']; m.updateMatrixWorld(true); return m;
  }
  const outside = hits([plane(.01)], origin, normal), inside = hits([plane(-.01)], origin, normal);
  assert(Math.abs(signedSummary(outside).nearest_to_sample_m - .01) < 1e-12);
  assert(Math.abs(signedSummary(inside).nearest_to_sample_m + .01) < 1e-12);
  assert.equal(hits([plane(.2)], origin, normal).length, 0);
  report.ray_calibrations = { actual_native_outside_plane: true, actual_native_inside_plane: true, outside_search_extent_is_not_falsely_covered: true };
  for (const item of cfg.cases) {
    const decodedBefore = decodedImages;
    const fine = play(await decode(item.lod0)), coarse = play(await decode(item.lod3));
    const caseRow = { asset: item.asset, lod0: costs(fine, item.lod0), lod3: costs(coarse, item.lod3), phases: [] };
    report.cases.push(caseRow); await save();
    for (const t of cfg.phases_seconds) {
      fine.update(t); coarse.update(t);
      const fineFlat = fine.meshes.map(bakeForRays), coarseFlat = coarse.meshes.map(bakeForRays);
      const fineBodies = fineFlat.filter(m => m.userData.originalMaterials.includes('skin'));
      const garments = xs => xs.filter(m => m.userData.originalMaterials.some(s => /^garment_(upper|outer|lower)__/.test(s)));
      const fineGarments = garments(fineFlat), coarseGarments = garments(coarseFlat);
      assert(fineBodies.length > 0 && fineGarments.length > 0 && coarseGarments.length > 0);
      const phase = { time_s: t, body_samples: [], native_float32_palette_SHA256: {} };
      caseRow.phases.push(phase);
      for (const [kind, model] of [['lod0', fine], ['lod3', coarse]]) for (const mesh of model.meshes) {
        assert(mesh.skeleton.boneMatrices instanceof Float32Array);
        assert([...mesh.skeleton.boneMatrices].every(Number.isFinite));
        phase.native_float32_palette_SHA256[kind + ':' + mesh.name] = sha(rawBytes(mesh.skeleton.boneMatrices));
      }
      for (let mi = 0; mi < coarse.meshes.length; mi++) {
        const source = coarse.meshes[mi], flat = coarseFlat[mi];
        if (!materialNames(source).includes('skin')) continue;
        const count = flat.geometry.index.count / 3, N = Math.min(192, count), position = flat.geometry.attributes.position;
        for (let sample = 0; sample < N; sample++) {
          const fi = Math.floor((sample + .5) * count / N);
          const ids = [0, 1, 2].map(k => flat.geometry.index.getX(fi * 3 + k));
          const points = ids.map(i => new THREE.Vector3().fromBufferAttribute(position, i));
          const n = points[1].clone().sub(points[0]).cross(points[2].clone().sub(points[0]));
          assert(n.lengthSq() > 0, 'Degenerate actual posed sample triangle; preserve diagnostic negative.'); n.normalize();
          const p = points[0].clone().add(points[1]).add(points[2]).multiplyScalar(1 / 3);
          const fBody = hits(fineBodies, p, n), fCloth = hits(fineGarments, p, n), cCloth = hits(coarseGarments, p, n);
          const bodySummary = signedSummary(fBody), fineSummary = signedSummary(fCloth), coarseSummary = signedSummary(cCloth);
          const refBody = bodySummary.nearest_to_sample_m;
          const fineOutwardOfOwnReference = refBody !== null && fCloth.some(h => h.signed_distance_m > refBody);
          phase.body_samples.push({ coarse_mesh: source.name, coarse_face_index: fi, coarse_vertex_indices: ids,
            dominant_bone_mass: boneLabels(source, ids), point_vehicle_local_m: p.toArray(), native_posed_face_normal: n.toArray(),
            fine_body: bodySummary, fine_garments: fineSummary, coarse_garments: coarseSummary,
            fine_reference_has_cloth_outside_reference_body: fineOutwardOfOwnReference,
            potential_coarse_exposure_for_followup_only: fineOutwardOfOwnReference && !cCloth.some(h => h.signed_distance_m > 0),
            fine_body_hits: fBody, fine_garment_hits: fCloth, coarse_garment_hits: cCloth });
        }
      }
      phase.sample_count = phase.body_samples.length;
      phase.reference_eligible_count = phase.body_samples.filter(r => r.fine_reference_has_cloth_outside_reference_body).length;
      phase.potential_exposure_count = phase.body_samples.filter(r => r.potential_coarse_exposure_for_followup_only).length;
      // Distances and potential labels remain diagnostics, never a new quality bar.
      for (const flat of [...fineFlat, ...coarseFlat]) { flat.geometry.dispose(); flat.material.dispose(); }
      fine.verifyUnchanged(); coarse.verifyUnchanged(); await save();
    }
    caseRow.images_decoded = decodedImages - decodedBefore;
    fine.mixer.stopAllAction(); coarse.mixer.stopAllAction(); await save();
  }
  for (const [file, digest] of Object.entries(cfg.input_pins)) assert.equal(sha(await fs.readFile(file)), digest, file);
  report.status = 'NATIVE_FINITE_COVERAGE_DIAGNOSTIC_COMPLETE_NOT_GARMENT_ACCEPTANCE';
  report.no_assets_changed = true; report.decoded_images = decodedImages; await save();
  console.log(JSON.stringify({ status: report.status, output }));
} catch (error) {
  report.status = 'NATIVE_COVERAGE_DIAGNOSTIC_NONPASS'; report.errors.push(String(error.stack ?? error));
  await save(); throw error;
}
