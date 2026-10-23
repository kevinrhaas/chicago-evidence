// SPDX-License-Identifier: GPL-3.0-or-later
// Scene selection only: a flag is a reviewed declaration, never an automatic proof.
const check = (ok, message) => { if (!ok) throw Error('Horse placement: ' + message); };
export function selectStandingHorseRows(manifest, { sceneId, targetDate, supportRegions = [],
  hostMissing = () => false, hostPresent = () => false } = {}) {
  const era = String(sceneId);
  if (!['1835', '1904'].includes(era)) return [];
  const rows = (manifest.scenes?.[era] ?? []).filter(row => row.enabled !== false
    && !hostMissing(row.belongs_to));
  check(rows.length <= 1, 'one active horse per scene');
  if (era === '1835') return rows; // Preserve the existing first-yard contract.
  check(targetDate === '1904-07-01', '1904 scene date mismatch');
  for (const row of rows) {
    check(row.scene_id === era && row.target_date === targetDate, 'row scene/date mismatch');
    check(!row.belongs_to || hostPresent(row.belongs_to), 'host is not present in this scene');
    check(row.surface_kind === 'carriageway_triangle', '1904 requires drawn carriageway support');
    check(row.world_qualified === true, '1904 stand remains unqualified');
    const regions = supportRegions.filter(r => r.id === row.ground_support_region_id);
    check(supportRegions.length === 1 && regions.length === 1, 'one declared support region required');
    const region = regions[0];
    check(region.record_id === row.ground_record_id && region.scene_id === era
      && region.target_date === targetDate && region.surface_kind === row.surface_kind,
    'support region identity mismatch');
  }
  return rows;
}
