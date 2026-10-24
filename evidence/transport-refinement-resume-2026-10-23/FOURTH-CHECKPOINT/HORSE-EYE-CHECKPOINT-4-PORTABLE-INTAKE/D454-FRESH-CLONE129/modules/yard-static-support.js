// SPDX-License-Identifier: GPL-3.0-or-later
// A bounded copy of actual rendered yard triangles, made BEFORE upload release.
import * as THREE from 'three';

const MAX_REGIONS = 1, MAX_TRIANGLES = 32, MAX_BYTES = 4096;

/** Retains only triangles overlapping a declared small ENU support rectangle.
 * Does not retain original town arrays, change RELEASE_KEEP or depend on
 * ?keep-geometry. Fresh yard batches have contiguous, undeleted instance IDs.
 */
export function retainYardStaticSupport(group, regions = [], problems = []) {
  const retained = new Map(), census = { regions: 0, triangles: 0, bytes: 0, disposed: false };
  const out = { census,
    heightAt(e, n, recordId, regionId) {
      const entry = retained.get(regionId);
      if (!entry || census.disposed || entry.recordId !== recordId) return null;
      const [[e0, n0], [e1, n1]] = entry.bounds;
      if (e < e0 || e > e1 || n < n0 || n > n1) return null;
      const z = -n, a = entry.triangles; let highest = -Infinity;
      for (let i = 0; i < a.length; i += 9) {
        const x0 = a[i], z0 = a[i + 2], dx1 = a[i + 3] - x0, dz1 = a[i + 5] - z0;
        const dx2 = a[i + 6] - x0, dz2 = a[i + 8] - z0;
        const determinant = dx1 * dz2 - dx2 * dz1;
        if (Math.abs(determinant) < 1e-12) continue;
        const u = ((e - x0) * dz2 - (z - z0) * dx2) / determinant;
        const v = (dx1 * (z - z0) - dz1 * (e - x0)) / determinant;
        if (u < -1e-9 || v < -1e-9 || u + v > 1 + 1e-9) continue;
        const y = a[i + 1] + u * (a[i + 4] - a[i + 1]) + v * (a[i + 7] - a[i + 1]);
        highest = Math.max(highest, y);
      }
      return Number.isFinite(highest) ? highest : null;
    },
    dispose() { retained.clear(); census.disposed = true; census.regions = census.triangles = census.bytes = 0; },
  };
  if (regions.length > MAX_REGIONS) { problems.push('yards: static support region budget exceeded'); return out; }
  const point = new THREE.Vector3(), matrix = new THREE.Matrix4();
  group.updateMatrixWorld(true);
  for (const region of regions) {
    try {
      const b = region.bounds_enu_m;
      if (!region.id || !region.record_id || !Array.isArray(b) || b.flat().length !== 4
        || !b.flat().every(Number.isFinite) || b[1][0] <= b[0][0] || b[1][1] <= b[0][1]
        || (b[1][0] - b[0][0]) * (b[1][1] - b[0][1]) > 4 || retained.has(region.id)) {
        throw Error('Invalid/oversized static support rectangle');
      }
      const values = [];
      for (const mesh of group.children) {
        if (mesh.name !== 'yard-worn_earth') continue;
        if (!mesh.isBatchedMesh) throw Error('Expected actual yard BatchedMesh');
        const position = mesh.geometry.getAttribute('position'), index = mesh.geometry.getIndex();
        if (!position?.array || (index && !index.array?.length)) throw Error('Yard arrays released before support snapshot');
        for (let instance = 0; instance < mesh.instanceCount; instance++) {
          if (!mesh.getVisibleAt(instance)) continue;
          const range = mesh.getGeometryRangeAt(mesh.getGeometryIdAt(instance));
          mesh.getMatrixAt(instance, matrix).premultiply(mesh.matrixWorld);
          for (let i = range.start; i < range.start + range.count; i += 3) {
            const triangle = [];
            for (let j = 0; j < 3; j++) {
              point.fromBufferAttribute(position, index ? index.getX(i + j) : i + j).applyMatrix4(matrix);
              if (![point.x, point.y, point.z].every(Number.isFinite)) throw Error('Nonfinite support triangle');
              triangle.push(point.x, point.y, point.z);
            }
            const es = [triangle[0], triangle[3], triangle[6]], ns = [-triangle[2], -triangle[5], -triangle[8]];
            if (Math.max(...es) < b[0][0] || Math.min(...es) > b[1][0]
              || Math.max(...ns) < b[0][1] || Math.min(...ns) > b[1][1]) continue;
            values.push(...triangle);
            if (values.length / 9 > MAX_TRIANGLES || (values.length * 8 + census.bytes) > MAX_BYTES) {
              throw Error('Static support triangle/byte cap exceeded; horse support unavailable');
            }
          }
        }
      }
      if (!values.length) throw Error('No actual yard triangles overlap support rectangle');
      const triangles = new Float64Array(values);
      retained.set(region.id, { recordId: region.record_id, bounds: b, triangles });
      census.regions++; census.triangles += triangles.length / 9; census.bytes += triangles.byteLength;
    } catch (error) { problems.push(`yards static support: ${error.message}`); }
  }
  return out;
}

/** A separate bounded provider for a named1904 drawn TOP carriageway. The old
 * yard implementation above is unchanged. Copies no source mesh/array into its
 * return value; no analytic-height fallback, overlay, curb or town retention.
 */
export function retainCarriagewayStaticSupport(meshes, regions = [], {
  sceneId, targetDate, problems = [],
} = {}) {
  const retained = new Map();
  const census = { regions: 0, triangles: 0, bytes: 0, disposed: false };
  const out = { census,
    snapshot(recordId, regionId) {
      const r = retained.get(regionId);
      return !census.disposed && r?.recordId === recordId ? { scene_id: String(sceneId),
        target_date: targetDate, surface_kind: 'carriageway_triangle', record_id: recordId,
        region_id: regionId, triangles: r.triangles.length / 9, bytes: r.triangles.byteLength } : null;
    },
    heightAt(e, n, recordId, regionId) {
      const r = retained.get(regionId);
      if (census.disposed || !r || r.recordId !== recordId || !Number.isFinite(e) || !Number.isFinite(n)) return null;
      const b = r.bounds;
      if (e < b[0][0] || e > b[1][0] || n < b[0][1] || n > b[1][1]) return null;
      const a = r.triangles, z = -n; let highest = -Infinity;
      for (let i = 0; i < a.length; i += 9) {
        const x = a[i], zz = a[i + 2], dx1 = a[i + 3] - x, dz1 = a[i + 5] - zz;
        const dx2 = a[i + 6] - x, dz2 = a[i + 8] - zz;
        const determinant = dx1 * dz2 - dx2 * dz1;
        if (Math.abs(determinant) < 1e-12) continue;
        const u = ((e - x) * dz2 - (z - zz) * dx2) / determinant;
        const v = (dx1 * (z - zz) - dz1 * (e - x)) / determinant;
        if (u < -1e-9 || v < -1e-9 || u + v > 1 + 1e-9) continue;
        highest = Math.max(highest, a[i + 1] + u * (a[i + 4] - a[i + 1]) + v * (a[i + 7] - a[i + 1]));
      }
      return Number.isFinite(highest) ? highest : null;
    },
    dispose() { retained.clear(); census.disposed = true; census.regions = census.triangles = census.bytes = 0; },
  };
  if (!regions.length) return out;
  try {
    if (String(sceneId) !== '1904' || targetDate !== '1904-07-01' || regions.length !== 1)
      throw Error('Carriageway support scene/date/region budget refused');
    const region = regions[0], b = region.bounds_enu_m;
    if (!region.id || !region.record_id || region.scene_id !== String(sceneId)
      || region.target_date !== targetDate || region.surface_kind !== 'carriageway_triangle'
      || !Array.isArray(b) || b.length !== 2 || b.some(p => !Array.isArray(p) || p.length !== 2)
      || !b.flat().every(Number.isFinite) || b[1][0] <= b[0][0] || b[1][1] <= b[0][1]
      || (b[1][0] - b[0][0]) * (b[1][1] - b[0][1]) > 4)
      throw Error('Invalid carriageway support region');
    const values = [], point = new THREE.Vector3();
    for (const mesh of meshes) {
      if (!mesh.isMesh || !mesh.visible || mesh.userData.cls !== 'carriageway'
        || mesh.geometry.hasAttribute('seam')) continue;
      if (mesh.isBatchedMesh || Array.isArray(mesh.material) || mesh.material.transparent)
        throw Error('Expected opaque unbatched carriageway top');
      const spans = (mesh.userData.spans ?? []).filter(s => s.id === region.record_id);
      if (!spans.length) continue;
      const geometry = mesh.geometry, position = geometry.getAttribute('position'), index = geometry.getIndex();
      if (!position?.array?.length || (index && !index.array?.length))
        throw Error('Carriageway arrays released before support snapshot');
      const count = index?.count ?? position.count;
      const start = geometry.drawRange.start, end = Math.min(count, start + geometry.drawRange.count);
      mesh.updateWorldMatrix(true, false);
      for (const span of spans) {
        if (!Number.isInteger(span.from) || !Number.isInteger(span.to) || span.from < 0
          || span.to < span.from || span.from * 3 < start || span.to * 3 > end)
          throw Error('Invalid named carriageway triangle span');
        for (let i = span.from * 3; i < span.to * 3; i += 3) {
          const tri = [];
          for (let j = 0; j < 3; j++) {
            point.fromBufferAttribute(position, index ? index.getX(i + j) : i + j).applyMatrix4(mesh.matrixWorld);
            if (![point.x, point.y, point.z].every(Number.isFinite)) throw Error('Nonfinite carriageway triangle');
            tri.push(point.x, point.y, point.z);
          }
          const es = [tri[0], tri[3], tri[6]], ns = [-tri[2], -tri[5], -tri[8]];
          if (Math.max(...es) < b[0][0] || Math.min(...es) > b[1][0]
            || Math.max(...ns) < b[0][1] || Math.min(...ns) > b[1][1]) continue;
          const up = (tri[5] - tri[2]) * (tri[6] - tri[0]) - (tri[3] - tri[0]) * (tri[8] - tri[2]);
          if (up <= 1e-12) throw Error('Non-upward carriageway triangle');
          values.push(...tri);
          if (values.length / 9 > MAX_TRIANGLES || values.length * 8 > MAX_BYTES)
            throw Error('Carriageway support triangle/byte cap exceeded');
        }
      }
    }
    if (!values.length) throw Error('No named actual carriageway top triangles');
    const triangles = new Float64Array(values);
    retained.set(region.id, { recordId: region.record_id, bounds: b.map(p => p.slice()), triangles });
    census.regions = 1; census.triangles = triangles.length / 9; census.bytes = triangles.byteLength;
  } catch (error) { problems.push(`carriageway static support: ${error.message}`); }
  return out;
}
