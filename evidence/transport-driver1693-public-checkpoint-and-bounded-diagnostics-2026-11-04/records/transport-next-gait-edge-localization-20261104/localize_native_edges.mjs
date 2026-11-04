// Read-only diagnostic. Native GLTFLoader/clone/mixer/getVertexPosition plus
// original Float32 palette arithmetic. No source writes, authoring or gate verdict.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { registerHooks } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
const [cfgPath, outPath] = process.argv.slice(2);
assert(cfgPath && outPath);
const C = JSON.parse(fs.readFileSync(cfgPath));
assert(C.approved === true && C.template_only === false);
assert(C.policy === 'ROOT_AUTHORIZED_ONE_120S_HORSE_EDGE_REGION_DIAGNOSTIC_NO_GENERATION');
assert(C.diagnostic_only && !C.authoring_approved && !C.gait_acceptance && !C.world_acceptance);
assert(C.native_phase_seconds === 120 && Date.now() < Date.parse(C.expires_utc));
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
for (const [f, pin] of Object.entries(C.pins)) assert.equal(sha(fs.readFileSync(f)), pin, f);
assert.equal(sha(fs.readFileSync(C.schedule_path)), C.schedule_sha256);
const schedule = JSON.parse(fs.readFileSync(C.schedule_path));
assert.equal(schedule.frames.length, 1154);
const raw = fs.readFileSync(C.candidate); assert.equal(sha(raw), C.candidate_sha256);
assert.equal(C.candidate_sha256, 'ad9dc060f8630d0de04fef97d716e8c82be3ac8bf070684e78107720c5221ec6');
const doc = JSON.parse(raw.subarray(20, 20 + raw.readUInt32LE(12)));
const rootURL = pathToFileURL(path.resolve(C.engine) + '/').href;
registerHooks({
  resolve(specifier, context, next) {
    if (specifier === 'three') return { url: new URL('three.module.js', rootURL).href, shortCircuit: true };
    if (specifier.startsWith('three/addons/')) return { url: new URL('addons/' + specifier.slice(13), rootURL).href, shortCircuit: true };
    return next(specifier, context);
  },
  load(url, context, next) {
    if (url.startsWith(rootURL) && url.endsWith('.js')) return { format: 'module', source: fs.readFileSync(fileURLToPath(url), 'utf8'), shortCircuit: true };
    return next(url, context);
  },
});
const T = await import('three');
const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
const { clone } = await import('three/addons/utils/SkeletonUtils.js');
assert.equal(T.REVISION, '185');
const loader = new GLTFLoader();
loader.register(() => ({ name: 'CPU_POSE_ONLY_MATERIAL_ADAPTER', loadMaterial: async i => {
  const p = doc.materials[i]; return new T.MeshBasicMaterial({ name: p.name, color: 0xffffff, side: p.doubleSided ? T.DoubleSide : T.FrontSide });
} }));
const parsed = await loader.parseAsync(raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.byteLength), '');
const scene = clone(parsed.scene); scene.updateMatrixWorld(true);
const originalNodes = [], cloneNodes = [];
parsed.scene.traverse(o => originalNodes.push(o)); scene.traverse(o => cloneNodes.push(o));
assert.equal(originalNodes.length, cloneNodes.length);
const meshes = doc.meshes.map((_, mi) => {
  const i = originalNodes.findIndex(o => o.isSkinnedMesh && parsed.parser.associations.get(o)?.meshes === mi);
  assert(i >= 0); return cloneNodes[i];
});
assert.equal(meshes.length, 3);
const limbOffsets = { hind_l: 0, fore_l: .25, hind_r: .5, fore_r: .75 };
const regionOf = name => /^(fore|hind)_[lr]_/.test(name) ? name.slice(0, 6)
  : /tail/i.test(name) ? 'tail' : /neck|head|ear|jaw|eye/i.test(name) ? 'head_neck' : 'trunk';
const V = new T.Vector3(), Q = new T.Vector3();
const vector = (attr, i) => [attr.getX(i), attr.getY(i), attr.getZ(i)];
const weightInfo = (m, i) => {
  const j = m.geometry.attributes.skinIndex, w = m.geometry.attributes.skinWeight;
  return Array.from({ length: 4 }, (_, k) => {
    const index = j.getComponent(i, k), weight = w.getComponent(i, k);
    return { joint: index, bone: m.skeleton.bones[index].name, weight, region: regionOf(m.skeleton.bones[index].name) };
  });
};
const meshData = meshes.map((m, mi) => {
  const a = m.geometry.attributes.position, I = m.geometry.index.array;
  const rest = Array.from({ length: a.count }, (_, i) => vector(a, i));
  const weights = rest.map((_, i) => weightInfo(m, i));
  const edges = [];
  for (let i = 0; i < I.length; i += 3) {
    const ids = [I[i], I[i + 1], I[i + 2]];
    for (let k = 0; k < 3; k++) {
      const u = ids[k], v = ids[(k + 1) % 3];
      const length = Math.hypot(...rest[u].map((x, j) => rest[v][j] - x));
      if (length <= 1e-8) continue; // Exact original degenerate-edge exclusion.
      const signature = [...new Set([...weights[u], ...weights[v]].filter(x => x.weight > 0).map(x => x.region))].sort().join('+');
      edges.push({ u, v, triangle: i / 3, edgeInTriangle: k, length, signature });
    }
  }
  return { mi, m, rest, weights, edges, native: new Float64Array(a.count * 3), shader: new Float64Array(a.count * 3),
    materials: [...new Set(doc.meshes[mi].primitives.map(p => doc.materials[p.material]?.name))] };
});
const report = { status: 'DIAGNOSTIC_RUNNING_NO_GAIT_ACCEPTANCE', candidate_sha256: C.candidate_sha256,
  originalLimits: C.originalLimits, diagnostic_observes: 'edge ratios and causal endpoint skin support only; not a rerun or replacement of all seven physical predicates',
  expected_frames: 1154, completed_frames: 0, completed_modes: { walk: 0, quiet: 0 },
  methods: ['nativeGetVertexPosition', 'nativeBoneMatrixShaderArithmetic'],
  known_extrema_first: schedule.known_global_edge_extrema_first, known_extrema_readbacks: [], regions: {},
  exact_native_loader_clone_mixer_skin_positions: true, material_adapter: 'CPU_ONLY_NO_IMAGE_DECODE',
  generation: false, current_model_modified: false, original_thresholds_changed: false,
  world_or_visual_or_photo_or_new_stride_accepted: false };
const byMode = {};
const saved = () => fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + '\n');
assert(!fs.existsSync(outPath)); saved();
function describe(D, e, frame, ratio, positions) {
  return { mode: frame.mode, frame: frame.index, timeSeconds: frame.timeSeconds, frameKind: frame.kind,
    serialized_clip_duration_s: byMode[frame.mode].clip.duration,
    authored_limb_phases: Object.fromEntries(Object.entries(limbOffsets).map(([limb, offset]) => [limb,
      frame.mode === 'walk' ? ((frame.timeSeconds / 1.6 - offset) % 1 + 1) % 1 : null])),
    meshIndex: D.mi, meshName: D.m.name, materials: D.materials, triangleIndex: e.triangle, edgeInTriangle: e.edgeInTriangle,
    vertexIndices: [e.u, e.v], support_signature: e.signature, ratio, rest_edge_length_m: e.length,
    posed_edge_length_m: ratio * e.length,
    endpoints: [e.u, e.v].map(i => ({ vertex: i, rest_xyz_m: D.rest[i], actual_posed_xyz_m: Array.from(positions.subarray(i * 3, i * 3 + 3)), skin: D.weights[i] })) };
}
function updateBounds(bucket, ratio, make) {
  if (!bucket.min || ratio < bucket.min.ratio) bucket.min = make();
  if (!bucket.max || ratio > bucket.max.ratio) bucket.max = make();
}
for (const mode of ['walk', 'quiet']) {
  const clip = parsed.animations.find(a => a.name === C[mode + '_clip']); assert(clip);
  byMode[mode] = { clip, mixer: new T.AnimationMixer(scene), action: null };
  const x = byMode[mode]; x.action = x.mixer.clipAction(clip);
  x.action.setLoop(T.LoopOnce, 1); x.action.clampWhenFinished = true;
}
const knownKeys = new Set(schedule.known_global_edge_extrema_first.map(f => f.mode + ':' + f.index));
const frames = [...schedule.known_global_edge_extrema_first,
  ...schedule.frames.filter(f => !knownKeys.has(f.mode + ':' + f.index))];
for (const frame of frames) {
  const x = byMode[frame.mode];
  for (const y of Object.values(byMode)) y.mixer.stopAllAction();
  x.action.reset().play(); x.mixer.setTime(frame.timeSeconds);
  scene.updateMatrixWorld(true); for (const m of meshes) m.skeleton.update();
  const actorDistance = frame.mode === 'walk' ? .135 * frame.timeSeconds / x.clip.duration : 0;
  const frameGlobal = {};
  for (const D of meshData) {
    const m = D.m, P = m.geometry.attributes.position, J = m.geometry.attributes.skinIndex, W = m.geometry.attributes.skinWeight, B = m.skeleton.boneMatrices;
    for (let i = 0; i < P.count; i++) {
      m.getVertexPosition(i, V).applyMatrix4(m.matrixWorld); V.z += actorDistance;
      D.native[i * 3] = V.x; D.native[i * 3 + 1] = V.y; D.native[i * 3 + 2] = V.z;
      V.fromBufferAttribute(P, i).applyMatrix4(m.bindMatrix); Q.set(0, 0, 0);
      for (let k = 0; k < 4; k++) {
        const j = J.getComponent(i, k) * 16, w = W.getComponent(i, k);
        Q.x += w * (B[j] * V.x + B[j + 4] * V.y + B[j + 8] * V.z + B[j + 12]);
        Q.y += w * (B[j + 1] * V.x + B[j + 5] * V.y + B[j + 9] * V.z + B[j + 13]);
        Q.z += w * (B[j + 2] * V.x + B[j + 6] * V.y + B[j + 10] * V.z + B[j + 14]);
      }
      Q.applyMatrix4(m.bindMatrixInverse).applyMatrix4(m.matrixWorld); Q.z += actorDistance;
      D.shader[i * 3] = Q.x; D.shader[i * 3 + 1] = Q.y; D.shader[i * 3 + 2] = Q.z;
    }
    for (const [method, positions] of [['nativeGetVertexPosition', D.native], ['nativeBoneMatrixShaderArithmetic', D.shader]]) {
      const key = frame.mode + ':' + method;
      const all = report.regions[key] ??= { global: {}, byMesh: {}, bySupport: {} };
      const mb = all.byMesh[D.mi] ??= {};
      const fg = frameGlobal[method] ??= {};
      for (const e of D.edges) {
        const u = e.u * 3, v = e.v * 3;
        const ratio = Math.hypot(positions[u] - positions[v], positions[u + 1] - positions[v + 1], positions[u + 2] - positions[v + 2]) / e.length;
        assert(Number.isFinite(ratio));
        const description = () => describe(D, e, frame, ratio, positions);
        updateBounds(all.global, ratio, description); updateBounds(mb, ratio, description);
        const region = all.bySupport[D.mi + ':' + e.signature] ??= {};
        updateBounds(region, ratio, description); updateBounds(fg, ratio, description);
      }
    }
  }
  report.completed_frames++; report.completed_modes[frame.mode]++;
  if (knownKeys.has(frame.mode + ':' + frame.index)) report.known_extrema_readbacks.push({ ...frame, methods: frameGlobal });
  if (report.completed_frames === 4) {
    report.known_extrema_first_complete = true;
    fs.writeFileSync(outPath + '.KNOWN-EXTREMA-FIRST.json', JSON.stringify({ status: 'FOUR_KNOWN_PHASES_LOCALIZED_NOT_FULL_REGIONAL_BOUNDS', completed_frames: 4,
      records: report.known_extrema_readbacks, originalLimits: C.originalLimits, no_gait_or_world_qualification: true }, null, 2) + '\n', { flag: 'wx' });
    saved();
  }
  if (report.completed_frames % 32 === 0) { saved(); console.log(JSON.stringify({ completed: report.completed_frames, expected: 1154 })); }
}
assert.equal(report.completed_frames, 1154);
for (const mode of ['walk', 'quiet']) for (const method of report.methods) {
  const b = report.regions[mode + ':' + method].global;
  for (const [metric, value] of [['edgeMin', b.min.ratio], ['edgeMax', b.max.ratio]]) {
    const reference = schedule.reference_extrema[mode + '.' + method + '.' + metric];
    assert(Math.abs(value - reference.value) < 1e-9, 'Actual same-input native edge result disagrees with sealed baseline ' + mode + '/' + method + '/' + metric);
  }
}
for (const [f, pin] of Object.entries(C.pins)) assert.equal(sha(fs.readFileSync(f)), pin, 'Input changed: ' + f);
report.status = 'DIAGNOSTIC_COMPLETE_SAME_INPUT_NATIVE_EDGE_LOCALIZATION_NOT_GAIT_ACCEPTANCE';
report.full_sealed_timeline_reproduced = true;
report.sealed_global_edge_ratios_reproduced_within_1e_minus_9 = true;
saved();
console.log(JSON.stringify({ status: report.status, completed_frames: report.completed_frames }));
