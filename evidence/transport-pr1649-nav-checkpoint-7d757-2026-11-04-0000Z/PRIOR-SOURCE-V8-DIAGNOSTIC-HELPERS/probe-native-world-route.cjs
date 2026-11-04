// External finite probe, called only in an already boot-ready real app page.
// Does not move the actual actor, replace ground, manufacture route PASS, or open a page.
const assert = require('node:assert/strict');
exports.probeNativeWorldRoute = async function probeNativeWorldRoute(page, { row, moduleBase = '/renderers/web/js/' }) {
  const reading = await page.evaluate(async ({ row, moduleBase }) => {
    const api = window.__chicago4d;
    if (!api?.ready) throw Error('Actual app is not boot-ready');
    const actor = api.townTransport?.actors.find(a => a.id === row.id);
    if (!actor) throw Error('Ordinary near-route mount has not exposed actual actor');
    const routeReading = actor.routeReading;
    if (routeReading?.status !== 'RENDERED_ROUTE_STATIC_CLEARANCE_AND_SUPPORT_SAMPLES_PASS'
      || !routeReading.horse_support_reader_used) throw Error('Actual mounting whole-route terrain/support receipt is absent');
    const { createTransportClearance } = await import(new URL('transport-clearance.js', new URL(moduleBase, location.href)));
    // Independent read-only geometry observation: no GPU/frame yields. A slow
    // synchronous read fails at the strict5s bound and can never return partial PASS.
    const start = performance.now();
    const checkReadBudget = () => {
      if (performance.now() - start > 5000) throw Error('Independent synchronous world-route read exceeded strict5s cap; no partial PASS');
    };
    const clear = createTransportClearance({ footprints: () => api.footprints,
      visitor: () => null, envelope_local_xz_m: row.envelope_local_xz_m });
    const total = routeReading.full_circuit_length_m, count = Math.ceil(total / .25);
    const first = actor.previewAt(0), last = actor.previewAt(total);
    const finite = p => [p.e, p.n, p.yaw, p.height, p.wheelGap, ...p.driverAt].every(Number.isFinite);
    let before = first, maxGap = 0, samples = 0;
    for (let i = 0; i <= count; i++) {
      checkReadBudget();
      const pose = actor.previewAt(total * i / count);
      if (!finite(pose) || !clear(before, pose)) throw Error(`Actual whole-team world clearance/ground NONPASS at sample ${i}`);
      if (pose.wheelGap > .03 + 1e-12) throw Error('Original actual wheel support bound exceeded');
      maxGap = Math.max(maxGap, pose.wheelGap); samples++; before = pose;
    }
    const snap = actor.snapshot(), horses = snap.assembly_state?.horse;
    if (!Array.isArray(horses) || horses.length !== 2) throw Error('Actual occupied actor has no two-horse support snapshot');
    for (const horse of horses) {
      const s = horse.support;
      if (!Number.isFinite(horse.distance_m) || !s || s.sample_count !== 9
        || s.tilt_rad > 2 * Math.PI / 180 + 1e-12 || s.sampled_minimum_clearance_m < -1e-12
        || s.sampled_maximum_clearance_m > .001 + 1e-12) throw Error('Actual live horse rigid-plane bound failed');
    }
    const middle = actor.previewAt(total / 2), block = { id: 'probe-whole-team-obstruction-control', pts: [
      [middle.e - .1, middle.n - .1], [middle.e + .1, middle.n - .1],
      [middle.e + .1, middle.n + .1], [middle.e - .1, middle.n + .1] ] };
    const reject = createTransportClearance({ footprints: () => [block], visitor: () => null,
      envelope_local_xz_m: row.envelope_local_xz_m });
    if (reject(middle, middle)) throw Error('Actual collision predicate failed its physical obstruction control');
    const rootClosure = Math.hypot(first.e - last.e, first.n - last.n, first.height - last.height);
    const driverClosure = Math.hypot(...first.driverAt.map((value, i) => value - last.driverAt[i]));
    if (rootClosure > 1e-9 || driverClosure > 1e-9) throw Error('Actual closed route placement did not close');
    checkReadBudget();
    return { status: 'ACTUAL_WORLD_ROUTE_GROUND_CLEARANCE_AND_LIVE_RIGID_TEAM_SUPPORT_PASS',
      id: actor.id, personId: actor.personId, routeReading, independent_world_preview_samples: samples,
      world_preview_maximum_spacing_m: total / count, maximum_wheel_gap_m: maxGap,
      independent_seconds: (performance.now() - start) / 1000,
      root_closure_m: rootClosure, driver_closure_m: driverClosure,
      actual_live_horse_support: horses, actual_actor_snapshot: snap,
      actual_footprint_count: api.footprints.length, actual_obstruction_negative_control_rejected: true,
      all_loop_motion_replayed: false, actual_posed_hoof_world_surface_acceptance: false,
      image_appearance_or_phone_performance_acceptance: false };
  }, { row, moduleBase });
  assert.equal(reading.status, 'ACTUAL_WORLD_ROUTE_GROUND_CLEARANCE_AND_LIVE_RIGID_TEAM_SUPPORT_PASS');
  assert(reading.independent_seconds <= 5, 'Independent synchronous route read exceeded strict5s cap; no partial PASS');
  return reading;
};
