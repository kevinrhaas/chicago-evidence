from pathlib import Path
D=Path(__file__).parent;W=Path('/workspace/chicago-bounds-proposal-20261103');p='chicago/4d/renderers/web/js/batch-bounds.js';old=(D/'BASE'/p).read_text();s=old
helpers=r'''
// -32768 is not needed by the ±32767 grid; reserve it for an exact -0.
const Q_ZERO_NEGATIVE = -32768;
const qValue = q => q === Q_ZERO_NEGATIVE ? -0 : q / 32767;
function qCenter(boxes, b, axis) {
  const a = boxes[b + axis], z = boxes[b + axis + 3];
  return Math.fround(a === Q_ZERO_NEGATIVE || z === Q_ZERO_NEGATIVE
    ? (qValue(a) + qValue(z)) * .5 : (a + z) / 65534);
}

/** Exact Float32-word dictionary only when its extra array is profitable. */
function packRadiusWords(radii) {
  const words = new Uint32Array(radii.buffer, radii.byteOffset, radii.length);
  const byWord = new Map(), unique = [], ids = new Uint32Array(radii.length);
  for (let i = 0; i < words.length; i += 1) {
    const word = words[i];
    let id = byWord.get(word);
    if (id === undefined) { id = unique.length; byWord.set(word, id); unique.push(word); }
    ids[i] = id;
  }
  const Index = unique.length <= 256 ? Uint8Array : unique.length <= 65536 ? Uint16Array : Uint32Array;
  if (unique.length * 4 + radii.length * Index.BYTES_PER_ELEMENT + 128 >= radii.byteLength)
    return { radii, radiusIds: null };
  const dictionary = new Float32Array(unique.length);
  new Uint32Array(dictionary.buffer).set(unique);
  const radiusIds = new Index(radii.length); radiusIds.set(ids);
  return { radii: dictionary, radiusIds };
}

/** Admit only exact reconstructions of the ALREADY rounded Float32 cache.
 * Neither the geometry nor a getter's former value changes. All admission
 * scratch (including the radius Map and original arrays) dies before return. */
function packQuantizedBounds(boxes, spheres, stored, normalized) {
  if (!normalized || !stored.some(Boolean)) return null;
  const n = stored.length, q = new Int16Array(n * 6), radii = new Float32Array(n);
  const exceptions = [], centers = [];
  for (let id = 0; id < n; id += 1) {
    if (stored[id] !== 1) continue;
    const b = id * 6, s = id * 4;
    for (let axis = 0; axis < 6; axis += 1) {
      const value = boxes[b + axis];
      const code = Object.is(value, -0) ? Q_ZERO_NEGATIVE : Math.round(value * 32767);
      if (!Number.isInteger(code) || code < -32767 && code !== Q_ZERO_NEGATIVE || code > 32767)
        return null;
      const restored = axis < 3 ? floorF32(qValue(code)) : ceilF32(qValue(code));
      if (!Object.is(restored, value)) return null;
      q[b + axis] = code;
    }
    if (![spheres[s], spheres[s + 1], spheres[s + 2], spheres[s + 3]].every(Number.isFinite)) return null;
    if (![0, 1, 2].every(axis => Object.is(qCenter(q, b, axis), spheres[s + axis]))) {
      exceptions.push(id); centers.push(spheres[s], spheres[s + 1], spheres[s + 2]);
    }
    radii[id] = spheres[s + 3];
  }
  const Id = n <= 65536 ? Uint16Array : Uint32Array;
  const centerIds = new Id(exceptions), centerValues = new Float32Array(centers);
  const radius = packRadiusWords(radii);
  const bytes = q.byteLength + centerIds.byteLength + centerValues.byteLength
    + radius.radii.byteLength + (radius.radiusIds?.byteLength ?? 0);
  // Tiny batches keep their old arrays rather than buying extra cache/array
  // descriptors. This reserve is not credited as a measured heap saving.
  if (bytes + 512 >= boxes.byteLength + spheres.byteLength) return null;
  return { boxes: q, centerIds, centerValues, ...radius, bytes };
}

function centerExceptionAt(ids, id) {
  let lo = 0, hi = ids.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >>> 1, value = ids[mid];
    if (value === id) return mid;
    if (value < id) lo = mid + 1; else hi = mid - 1;
  }
  return -1;
}
'''
needle='/**\n * Move every computed box and sphere';assert needle in s;s=s.replace(needle,helpers+'\n'+needle)
s=s.replace('  const boxes = new Float32Array(n * 6);','  let boxes = new Float32Array(n * 6);').replace('  const spheres = new Float32Array(n * 4);','  let spheres = new Float32Array(n * 4);')
needle='  const proto = THREE.BatchedMesh.prototype;';assert needle in s;s=s.replace(needle,"  const packed = packQuantizedBounds(boxes, spheres, stored, batch.geometry?.attributes?.position?.normalized === true);\n  if (packed) { boxes = null; spheres = null; } // no old-array retainer in either getter\n"+needle)
a='''      target.min.set(boxes[b], boxes[b + 1], boxes[b + 2]);
      target.max.set(boxes[b + 3], boxes[b + 4], boxes[b + 5]);''';assert a in s;s=s.replace(a,'''      if (packed) {
        target.min.set(floorF32(qValue(packed.boxes[b])), floorF32(qValue(packed.boxes[b + 1])), floorF32(qValue(packed.boxes[b + 2])));
        target.max.set(ceilF32(qValue(packed.boxes[b + 3])), ceilF32(qValue(packed.boxes[b + 4])), ceilF32(qValue(packed.boxes[b + 5])));
      } else {
        target.min.set(boxes[b], boxes[b + 1], boxes[b + 2]);
        target.max.set(boxes[b + 3], boxes[b + 4], boxes[b + 5]);
      }''')
a='''      target.center.set(spheres[s], spheres[s + 1], spheres[s + 2]);
      target.radius = spheres[s + 3];''';assert a in s;s=s.replace(a,'''      if (packed) {
        const e = centerExceptionAt(packed.centerIds, geometryId);
        if (e >= 0) target.center.set(packed.centerValues[e * 3], packed.centerValues[e * 3 + 1], packed.centerValues[e * 3 + 2]);
        else target.center.set(qCenter(packed.boxes, geometryId * 6, 0), qCenter(packed.boxes, geometryId * 6, 1), qCenter(packed.boxes, geometryId * 6, 2));
        target.radius = packed.radii[packed.radiusIds ? packed.radiusIds[geometryId] : geometryId];
      } else {
        target.center.set(spheres[s], spheres[s + 1], spheres[s + 2]);
        target.radius = spheres[s + 3];
      }''')
a='  batch.userData.compactBounds = { rows, bytes: boxes.byteLength + spheres.byteLength + stored.byteLength };';assert a in s;s=s.replace(a,'''  batch.userData.compactBounds = { rows, bytes: (packed ? packed.bytes : boxes.byteLength + spheres.byteLength) + stored.byteLength };
  if (packed) Object.assign(batch.userData.compactBounds, { codec: 'q16-bit-exact', centerExceptions: packed.centerIds.length,
    radiusDictionaryEntries: packed.radiusIds ? packed.radii.length : 0, radiusIndexBytes: packed.radiusIds?.BYTES_PER_ELEMENT ?? 0 });''')
s=s.replace(' * two methods, so nothing else has to know.',''' * two methods, so nothing else has to know.
 *
 * A normalized grid batch may then store those SAME Float32 answers as q16
 * endpoints, exact derived centres plus sparse Float32 exceptions, and exact
 * radius words. Admission compares every reconstructed word to the former cache;
 * otherwise the original Float32 arrays remain. No bound is rounded again.''')
(W/p).write_text(s)
