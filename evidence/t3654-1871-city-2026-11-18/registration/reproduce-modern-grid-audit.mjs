#!/usr/bin/env node
// Read-only reproduction of the T-3654 modern-intersection/frame comparison.
// Usage: node t3654-audit-today-registration.mjs /path/to/chicago/4d > audit.json
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const root = path.resolve(process.argv[2] || '.');
const read = rel => JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8'));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const round = n => Number(n.toFixed(9));
const sub = (a, b) => a.map((v, i) => round(v - b[i]));
const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
const must = (condition, message) => { if (!condition) throw Error(message); };
const moduleAt = rel => import(pathToFileURL(path.join(root, rel)).href);
const { CONTROLS, createRegistration } = await moduleAt('renderers/web/js/today-register.js');
const { DATUM, latLngToLocal } = await moduleAt('renderers/web/js/today-geo.js');
const { deriveControls, controlTable } = await moduleAt('tools/today_registration.mjs');
const datum = read('data/datum.json');
const plan = read('data/context/1871/plan.json');
const modern = read('data/modern/streets.json');
const targets = read('data/traces/gcp/mitchell_1870_modern_targets.json');
const rees = read('data/traces/gcp/rees_rucker_1849_gcps.json');
const wright = read('data/traces/gcp/wright_1834_gcps.json');
const origin = [datum.origin_utm_e, datum.origin_utm_n];
const controlById = new Map(plan.map_control.controls.map(c => [c.id, c]));
const todayById = new Map(CONTROLS.map(c => [c[0], c]));
const targetById = new Map(targets.targets.map(t => [t.id, t]));

// Explicit named pairs, not an arbitrary nearest-coordinate match.
const pairs = [
  ['M1', '1835:statexmadison'],
  ['lasalle_lake', '1835:lakexlasalle'],
  ['lasalle_randolph', '1835:randolphxlasalle'],
  ['lasalle_washington', '1835:washingtonxlasalle'],
  ['lasalle_madison', '1835:lasallexmadison'],
  ['clark_madison', '1835:clarkxmadison'],
  ['wells_madison', '1835:wellsxmadison'],
  ['clark_lake', '1835:lakexclark'],
  ['wells_randolph', '1835:randolphxwells'],
];
const comparisons = pairs.map(([id, todayId]) => {
  const c = controlById.get(id), row = todayById.get(todayId);
  must(c && row, `Missing named comparison ${id} / ${todayId}`);
  const current = row.slice(4, 6), drawn = row.slice(2, 4);
  const osm = c.modern_control;
  return {
    control_1871_id: id, feature: c.feature, role_in_1871_fit: c.role,
    modern_target_id: c.modern_target_id ?? null,
    osm_latitude: osm.lat, osm_longitude: osm.lon,
    osm_node_ids: osm.osm_node_ids ?? (id === 'M1' ? wright.gcps.find(g => g.id === 'G1').modern.osm_node_ids : []),
    osm_node_id_provenance: id === 'M1' ? 'Wright G1 records the identical latitude/longitude; the inherited Rees R1 target does not itself list node IDs.' : '1871 retained modern_control',
    osm_way_ids: osm.osm_way_ids ?? null,
    osm_local_enu_m: c.local,
    today_control_id: todayId, today_control_years: row[1].split(' '),
    city_today_local_enu_m: current,
    city_minus_osm_enu_m: sub(current, c.local),
    modern_dataset_difference_m: round(dist(current, c.local)),
    legacy_drawn_scene_local_enu_m: drawn,
    legacy_drawn_scene_minus_osm_enu_m: sub(drawn, c.local),
    legacy_drawn_scene_difference_m: round(dist(drawn, c.local)),
    today_minus_legacy_drawn_scene_enu_m: sub(current, drawn),
    osm_source_id: 'osm_streets_2026', city_source_id: modern.source,
  };
});

const legacyMatches = Array.from({ length: 14 }, (_, i) => {
  const id = i + 1;
  const c = controlById.get(`M${id}`), g = rees.gcps.find(row => row.id === `R${id}`);
  must(c && g, `Missing legacy pair M${id}/R${id}`);
  const local = [g.modern.local_e, g.modern.local_n];
  const sameCoordinates = c.local[0] === local[0] && c.local[1] === local[1];
  const sameLatLon = c.modern_control.lat === g.modern.lat && c.modern_control.lon === g.modern.lon;
  must(sameCoordinates && sameLatLon, `Inherited target changed at M${id}`);
  return {
    control_1871_id: c.id, legacy_gcp_id: g.id, feature: c.feature,
    legacy_feature: g.map_feature,
    latitude: g.modern.lat, longitude: g.modern.lon,
    target_1871_local_enu_m: c.local, legacy_target_local_enu_m: local,
    difference_m: round(dist(c.local, local)), exact_stored_coordinates_match: sameCoordinates,
    exact_stored_latlon_match: sameLatLon,
    source_path: 'data/traces/gcp/rees_rucker_1849_gcps.json',
  };
});
const g1 = wright.gcps.find(c => c.id === 'G1');
const m1 = controlById.get('M1');
const g1local = [g1.modern.utm_e - origin[0], g1.modern.utm_n - origin[1]];
const wrightCheck = {
  id: 'G1', feature: g1.map_feature, feature_note: g1.feature_note,
  osm_node_ids: g1.modern.osm_node_ids,
  latitude: g1.modern.lat, longitude: g1.modern.lon,
  stored_utm_m: [g1.modern.utm_e, g1.modern.utm_n],
  local_enu_m: g1local.map(round), target_1871_id: 'M1', target_1871_local_enu_m: m1.local,
  difference_m: round(dist(g1local, m1.local)),
  exact_stored_latlon_match: g1.modern.lat === m1.modern_control.lat && g1.modern.lon === m1.modern_control.lon,
  source_path: 'data/traces/gcp/wright_1834_gcps.json',
};
must(dist(g1local, m1.local) < 1e-8 && wrightCheck.exact_stored_latlon_match, 'Wright G1 frame check changed');

const projectionChecks = plan.map_control.controls.map(c => {
  const t = c.modern_control;
  must(Number.isFinite(t.lat) && Number.isFinite(t.lon), `Missing lat/lon: ${c.id}`);
  const projected = latLngToLocal(t.lat, t.lon);
  return {
    id: c.id, feature: c.feature, role: c.role, latitude: t.lat, longitude: t.lon,
    stored_target_local_enu_m: c.local, today_geo_local_enu_m: projected.map(round),
    today_geo_minus_stored_enu_m: sub(projected, c.local), difference_m: round(dist(projected, c.local)),
  };
});
const generatedToday = controlTable(deriveControls().controls);
const todayTableMatches = JSON.stringify(generatedToday) === JSON.stringify(CONTROLS);
must(todayTableMatches, 'Committed Today controls differ from their City-centreline derivation');
const registration = createRegistration('1871');
const identityChecks = plan.map_control.controls.map(c => ({
  id: c.id, input_local_enu_m: c.local,
  to_today_local_enu_m: registration.toToday(...c.local),
  to_scene_local_enu_m: registration.toScene(...c.local),
}));
must(registration.count === 0 && identityChecks.every(c =>
  dist(c.input_local_enu_m, c.to_today_local_enu_m) === 0 &&
  dist(c.input_local_enu_m, c.to_scene_local_enu_m) === 0), '1871 no longer uses identity registration');
must(datum.crs === 'EPSG:26916' && targets.crs === datum.crs, 'Unexpected coordinate reference system');
must(JSON.stringify(origin) === JSON.stringify(plan.origin_utm) &&
  JSON.stringify(origin) === JSON.stringify(targets.origin_utm_m) &&
  DATUM.origin_utm_e === origin[0] && DATUM.origin_utm_n === origin[1] && DATUM.zone === 16,
  'Datum origins disagree');

const sources = ['osm_streets_2026', 'chicago_street_center_lines', 'wright_1834', 'rees_rucker_1849', 'mitchell_1870_chicago_map'].map(id => {
  const rel = `data/sources/${id}.json`, source = read(rel);
  return { id, path: rel, sha256: sha(fs.readFileSync(path.join(root, rel))),
    citation: source.citation, url: source.url,
    role_in_this_audit: id === 'osm_streets_2026' ? 'Modern intersection targets; not historical proof.'
      : id === 'chicago_street_center_lines' ? 'Second modern dataset used by the existing Today navigation registration; not historical proof.'
      : 'Identifies the historical-map/GCP lineage; this audit does not re-fit or re-read the map.' };
});
const paths = [
  'data/datum.json', 'data/context/1871/plan.json', 'data/modern/streets.json',
  'data/streets/1835.json', 'data/street_grid/1904.json', 'data/modern/landmark_sites.json',
  'data/structures/first_fort_dearborn_pickets_outer.json', 'data/structures/fort_dearborn_palisade.json',
  'data/traces/street_control.json', 'data/traces/gcp/wright_1834_gcps.json',
  'data/traces/gcp/rees_rucker_1849_gcps.json', 'data/traces/gcp/mitchell_1870_modern_targets.json',
  targets.portable_primitive_extract,
  'renderers/web/js/today-register.js', 'renderers/web/js/today-geo.js',
  'renderers/web/js/today-view.js', 'renderers/web/js/modern-streets.js', 'renderers/web/js/main.js',
  'tools/today_registration.mjs', 'tools/build_modern_streets.py', 'tools/fit_1871_city_map.py',
  'docs/CORRIDOR-LINES.md', ...sources.map(s => s.path),
];
const hashes = Object.fromEntries(paths.map(rel => [rel, sha(fs.readFileSync(path.join(root, rel)))]));
const mse = comparisons.reduce((sum, c) => sum + dist(c.city_today_local_enu_m, c.osm_local_enu_m) ** 2, 0) / comparisons.length;
const script = fs.readFileSync(fileURLToPath(import.meta.url), 'utf8');
const audit = {
  id: 't-3654-today-registration-audit', schema: 1,
  recorded_utc: new Date().toISOString(),
  source_base: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  scope: 'Read-only comparison of existing 1871 modern targets with the project Today/Google Street View registration and committed survey-control lineage. No Google API, network request, coordinate mutation, fitting or historical geometry change.',
  conclusion: 'No missing global or legacy coordinate correction. 1871 and Today use the same EPSG:26916 local-metre frame. The old per-year Today shifts correct particular older reconstructions and must not be transplanted into the 1871 map fit.',
  source_sha256: hashes, sources,
  frame: {
    crs: datum.crs, units: 'metres', axis: 'local east, local north; renderer x=e, z=-n',
    origin_utm_m: origin, plan_coordinate_system: plan.coordinate_system,
    today_origin_utm_m: [DATUM.origin_utm_e, DATUM.origin_utm_n], today_utm_zone: DATUM.zone,
    formula: 'local_e = EPSG:26916.easting - 447072.7; local_n = EPSG:26916.northing - 4637395.8',
    inverse_formula: 'latitude/longitude = today-geo.js.localToLatLng(local_e, local_n); latLngToLocal is its numerical inverse',
    epsg_3435_used_by_these_paths: false,
    all_origin_and_crs_checks_pass: true,
  },
  formulas: {
    comparison_delta: 'delta = City current intersection [E,N] - 1871 OSM target [E,N]',
    comparison_distance: 'sqrt(delta_E^2 + delta_N^2)',
    comparison_rmse: 'sqrt(sum(distance_i^2) / 9), calculated before reporting-rounding',
    legacy_match: 'Compare M1..M14 local and lat/lon against R1..R14 modern targets; no historic Rees/Rucker pixel or affine transform reused.',
    wright_g1: '[447910.33,4636870.53] - [447072.7,4637395.8] = [837.63,-525.27]',
    today_shift: 'For each year select only CONTROLS rows naming it. Shift is inverse-distance blend of (today - scene); 1871 has zero rows and returns [0,0].',
  },
  modern_dataset_comparison: {
    count: comparisons.length, named_pair_selection: pairs,
    rmse_m: round(Math.sqrt(mse)), max_m: Math.max(...comparisons.map(c => c.modern_dataset_difference_m)),
    pairs: comparisons,
    city_data_source_edited: modern.source_edited,
    city_data_source_url: modern.source_url, city_data_source_sha256: modern.source_sha256,
    city_extract_bbox_local_enu_m: modern.box_local_m,
    city_extract_bbox_order: ['min_e', 'min_n', 'max_e', 'max_n'],
    city_extract_counts: modern.counts,
  },
  inherited_target_matches: { count: legacyMatches.length, all_exact: true, pairs: legacyMatches },
  wright_g1_check: wrightCheck,
  today_projection_check: {
    method: 'Call the shipped today-geo.js.latLngToLocal on each retained 1871 modern_control latitude/longitude, then compare to its stored local target. This is projection/rounding agreement, not historical-position validation.',
    count: projectionChecks.length,
    max_difference_m: Math.max(...projectionChecks.map(c => c.difference_m)),
    points: projectionChecks,
  },
  today_registration_1871: {
    control_count: registration.count, identity: true,
    existing_table_count: CONTROLS.length, existing_table_matches_rederived_city_controls: todayTableMatches,
    derived_from: 'tools/today_registration.mjs::deriveControls; controlTable',
    existing_years: [...new Set(CONTROLS.flatMap(c => c[1].split(' ')))].sort(),
    identity_checks: identityChecks,
    runtime_integration: 'main.js passes createRegistration(scene id) to both loadModernStreets(toScene) and createTodayView(register).',
  },
  native_survey_constraint: {
    source: 'docs/CORRIDOR-LINES.md; data/traces/street_control.json',
    ruling: 'The drawn line controls blocks/lots/roofs. The survey-controlled line answers roadway corridor questions. Neither is a citywide correction and neither rewrites the other.',
    kinzie_recentering_m: 2.91, south_water_recentering_m: 8.58,
    action: 'Preserve native historical street geometry; do not copy legacy Today shifts, corridor offsets, or an extra warp into the 1871 fitter.',
  },
  limitations: [
    'Agreement of two modern datasets is not independent survey truth; their source lineages may overlap. Neither establishes unchanged historical street centres.',
    'The City extract is bounded to [-800,-4000,2300,1250] local metres and the nine named comparisons are concentrated downtown. This does not validate the full 1871 municipal extent.',
    'The City file was last edited 2014-10-15; modern OSM controls have separately recorded retrieval dates. Street widening, reconstruction and changed node definitions can affect comparisons.',
    'The committed Today controls are rounded to 0.1 m, the 1871 targets generally to 0.01 m. Numerical precision is not surveying accuracy.',
    'today-geo.js uses the GRS80 ellipsoid for NAD83/WGS84 at this scale. The sub-centimetre code agreement is not a claim of sub-centimetre geodetic or historical accuracy.',
    'The 1871 map still has its declared affine-fit and reserved-check residuals. This comparison neither lowers those errors nor validates individual buildings, riverbanks, shoreline or generic lots.',
    '1871 currently has no scene-specific Today correction. Any future display alignment needs explicit 1871 correspondences and its own evidence; copying older-year corrections would import their reconstruction offsets.',
    'No actual Google Maps or Street View imagery was queried or used as historical evidence. Google is the destination of the existing navigation feature.',
  ],
  reproduction: {
    command: 'node /tmp/t3654-audit-today-registration.mjs /workspace/chicago/chicago/4d > /tmp/t3654-today-registration-audit.json',
    portable_command: 'node <saved-script.mjs> <checkout>/chicago/4d > <audit.json>',
    prerequisites: 'Node.js with ESM support; the source paths listed in source_sha256. No packages, network, browser, Python, Google API or generators required.',
    comparison_note: 'recorded_utc and source_base may change on reproduction; source hashes and calculated values identify the measured bytes and result.',
    script_sha256: sha(script), embedded_script: script,
  },
};
process.stdout.write(JSON.stringify(audit, null, 2) + '\n');
