/* Outside-APP observer. Calls existing native harness APIs; replaces no runtime,
 * clock, loader, asset, clearance, support reader, material or renderer method. */
(() => {
  const need = (v, m) => { if (!v) throw Error(m); };
  const epsilon = 1e-9; // Existing native transport-loop test's numerical epsilon.
  const close = (a, b, m) => need(Math.abs(a - b) <= epsilon, `${m}: ${a} != ${b}`);
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  let api, actor, row, spec, recipe, originalCamera, prior, deadline;
  const report = { ready: false, passed: false, windows: [], controls: [],
    scope: 'Actual mounted native world transport at configured pace; no natural-stride, trusted-UI, phone-performance or photographic acceptance' };
  const remaining = () => { need(performance.now() < deadline, 'Original complete 120s viewport deadline exhausted'); };
  const freeze = () => { api?.setAnimationHold(true); };
  function skeletons() {
    const team = api.townTransport.roots[0].getObjectByName(`team:${row.id}`);
    need(team?.children.length === 2, 'Actual two-horse team missing');
    const locals = root => {
      const records = [], seen = new Set();
      root.traverse(node => {
        if (!node.isSkinnedMesh) return;
        for (const bone of node.skeleton.bones) {
          if (seen.has(bone)) continue; seen.add(bone);
          records.push([bone.name, bone.position.toArray(), bone.quaternion.toArray(), bone.scale.toArray()]);
        }
      });
      return records;
    };
    const protectedDriver = [];
    api.townTransport.roots[0].traverse(node => {
      if (!node.isSkinnedMesh) return;
      for (let p = node; p; p = p.parent) if (p === team) return;
      for (const bone of node.skeleton.bones) if (!['head', 'neck_01'].includes(bone.name)) {
        protectedDriver.push([node.name, bone.name, bone.position.toArray(), bone.quaternion.toArray(), bone.scale.toArray()]);
      }
    });
    return { horses: team.children.map(locals), protectedDriver };
  }
  function snapshot() {
    const state = actor.snapshot(), stats = api.stats(), gl = api.renderer.getContext();
    need(stats.withinBudget, 'Original native render budget exceeded');
    need(!gl.isContextLost() && gl.getError() === 0, 'Native WebGL failure');
    need(state.assembly_state.horse.length === 2, 'Native horse-distance readings absent');
    for (const horse of state.assembly_state.horse) need(Number.isFinite(horse.distance_m) && horse.support, 'Actual support reading absent');
    return { now_ms: performance.now(), state, stats, camera: api.camera.matrixWorld.toArray(),
      drawing_buffer: [gl.drawingBufferWidth, gl.drawingBufferHeight], skeletons: skeletons() };
  }
  function step() {
    remaining(); const before_ms = performance.now(); api.step();
    const after_ms = performance.now(), reading = snapshot();
    reading.step_bracket_ms = [before_ms, after_ms]; return reading;
  }
  async function delayedStep(seconds = .25) {
    remaining(); const due = performance.now() + seconds * 1000;
    while (performance.now() < due) { remaining(); await wait(Math.max(1, due - performance.now())); }
    return step();
  }
  function stationary(before, after, label, visual = true) {
    close(after.state.total_distance_m, before.state.total_distance_m, `${label} distance`);
    need(JSON.stringify(after.state.wheel_rotation_rad) === JSON.stringify(before.state.wheel_rotation_rad), `${label} wheels changed`);
    need(JSON.stringify(after.state.assembly_state.horse) === JSON.stringify(before.state.assembly_state.horse), `${label} horse phase/support changed`);
    if (visual) close(after.state.assembly_state.driver.time_s, before.state.assembly_state.driver.time_s, `${label} visual clock`);
  }
  function checkTravel(before, after) {
    const elapsed = after.state.assembly_state.driver.time_s - before.state.assembly_state.driver.time_s;
    need(elapsed > 0, 'Actual visible native mixer time did not advance');
    const lower = Math.max(0, after.step_bracket_ms[0] - before.step_bracket_ms[1]) / 1000;
    const upper = (after.step_bracket_ms[1] - before.step_bracket_ms[0]) / 1000;
    need(elapsed >= lower - epsilon && elapsed <= upper + epsilon, 'Native admitted time escapes actual wall-clock brackets');
    const travelled = after.state.total_distance_m - before.state.total_distance_m;
    close(travelled, Math.min(row.speed_m_s * elapsed, .25), 'Configured pace/distance ceiling');
    need(after.state.state === 'moving', 'Native route stopped/obstructed during scheduled pace window');
    const routeCurvature = row.route.kind === 'rounded_block' ? 1 / row.route.corner_radius_m : 1 / row.route.radius_m;
    const wheels = after.state.wheel_rotation_rad.map((angle, i) => {
      const delta = ((angle - before.state.wheel_rotation_rad[i]) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
      const upperRatio = (i < 2 ? 1 : Math.hypot(1, row.wheelbase_m * routeCurvature)) + routeCurvature * row.track_m / 2;
      need(delta > 0 && delta <= travelled * upperRatio / row.wheel_radii_m[i] + epsilon, 'Native wheel arc exceeds unchanged route-geometry bound');
      return delta;
    });
    const horses = after.state.assembly_state.horse.map((horse, i) => {
      const distance = horse.distance_m - before.state.assembly_state.horse[i].distance_m;
      need(distance > 0, 'Actual distance-driven horse did not advance');
      const cycles = distance / spec.stride_m;
      if (Math.abs(cycles - Math.round(cycles)) > epsilon) {
        need(JSON.stringify(after.skeletons.horses[i]) !== JSON.stringify(before.skeletons.horses[i]), 'Actual loaded horse bone pose remained unchanged away from whole-cycle alias');
      }
      return { distance_m: distance, phase_cycles: distance / spec.stride_m,
        absolute_phase: (horse.distance_m / spec.stride_m) % 1 };
    });
    need(JSON.stringify(after.skeletons.protectedDriver) === JSON.stringify(before.skeletons.protectedDriver), 'Protected seated driver body/limbs changed');
    need(JSON.stringify(after.camera) === JSON.stringify(originalCamera), 'Scheduled window camera changed');
    return { native_admitted_wall_seconds: elapsed, external_wall_bracket_seconds: [lower, upper],
      distance_m: travelled, configured_speed_m_s: row.speed_m_s, wheel_angle_delta_rad: wheels,
      horses, capped_at_quarter_metre: row.speed_m_s * elapsed > .25 };
  }
  window.nativeElapsedObserver = {
    report,
    async initialize(options) {
      deadline = performance.now() + options.remaining_viewport_ms;
      api = window.__chicago4d; need(api?.ready, 'Native app not ready');
      api.renderer.setAnimationLoop(null); // Existing native API; no function replacement.
      api.setAnimationHold(true); api.setGovernor(false); await api.setDetail(options.tier);
      while (api.welcome?.state !== 'world') {
        remaining(); if (api.welcome?.state === 'welcome') api.welcome.enter('spawn');
        api.step(); await wait(20);
      }
      const response = await fetch(new URL('transport/driven/loops.json', api.dataBase));
      need(response.ok, 'Actual driven-loop source missing'); const config = await response.json();
      const rows = config.rows.filter(r => String(r.scene) === options.scene); need(rows.length === 1, 'Exactly one actual scene journey required');
      row = rows[0]; spec = config.horse_models[row.horse_model];
      need(row.speed_m_s === .084375 && spec.stride_m === .135, 'Configured pace/stride changed from reviewed increment');
      const anchor = api.townTransport?.driverAnchorForPerson(row.person_id); need(anchor, 'Actual native driver anchor unavailable');
      const e = anchor.at[0] + Math.cos(anchor.yaw_rad) * 8;
      const n = anchor.at[1] + Math.sin(anchor.yaw_rad) * 8;
      recipe = { local_e: e, local_n: n,
        yaw_deg: Math.atan2(anchor.at[0] - e, anchor.at[1] - n) * 180 / Math.PI, pitch_deg: 0 };
      api.walker.teleport(recipe); api.step(); api.setAnimationHold(false); api.step();
      await api.townTransport.ready(); remaining();
      actor = api.townTransport.driverForPerson(row.person_id); need(actor, 'Native actual assembly failed admission');
      need(actor.canResume(), 'Native camera/scene obstructs the actual journey');
      actor.stop('interaction'); freeze(); prior = step(); originalCamera = prior.camera;
      report.row = { id: row.id, person_id: row.person_id, scene: row.scene, speed_m_s: row.speed_m_s,
        stride_m: spec.stride_m, route: row.route, tier: options.tier };
      report.camera_recipe = recipe; report.camera_matrix = originalCamera;
      report.initial = prior; report.ready = true; return report;
    },
    prepareWindow() {
      freeze(); actor.stop('interaction'); prior = step(); return prior;
    },
    async runWindow(fps, seconds) {
      need([1, 2, 4].includes(fps) && seconds === 2, 'Finite reviewed schedule only');
      remaining(); api.setAnimationHold(false); need(actor.resume(), 'Public native Continue refused');
      const resumed = step(); stationary(prior, resumed, 'First actual held/Continue resume');
      let before = resumed; const rows = [], period = 1000 / fps;
      for (let i = 0; i < fps * seconds; i++) {
        const due = before.step_bracket_ms[0] + period;
        while (performance.now() < due) { remaining(); await wait(Math.max(1, due - performance.now())); }
        const after = step(); rows.push({ before, after, reading: checkTravel(before, after) }); before = after;
      }
      actor.stop('interaction'); freeze(); const ended = step(); stationary(before, ended, 'Native Stop/hold'); prior = ended;
      const cadenceAvailable = rows.every(r => r.after.step_bracket_ms[1] - r.after.step_bracket_ms[0] <= period);
      const window = { requested_fps: fps, requested_wall_seconds: seconds, rows,
        actual_native_wall_seconds: rows.reduce((sum, r) => sum + r.reading.native_admitted_wall_seconds, 0),
        distance_m: ended.state.total_distance_m - resumed.state.total_distance_m,
        first_actual_resume_zero: true, cadence_available: cadenceAvailable,
        passed: cadenceAvailable };
      report.windows.push(window); need(cadenceAvailable, 'Requested cadence unavailable: native render cost exceeds its frame period; no retry or timeout extension');
      return window;
    },
    async beginControls() {
      api.setAnimationHold(false); need(actor.resume(), 'Public Continue refused');
      const first = step(); stationary(prior, first, 'Control setup resume');
      prior = await delayedStep(); return prior;
    },
    async stopContinue(withStoppedTick) {
      const before = prior; actor.stop('interaction');
      if (withStoppedTick) { const stopped = await delayedStep(); stationary(before, stopped, 'Stopped tick', false); prior = stopped; }
      need(actor.resume(), 'Public Continue refused'); const resumed = step(); stationary(prior, resumed, 'First actual Continue', false);
      const next = await delayedStep(); checkTravel(resumed, next); prior = next;
      report.controls.push({ kind: 'Stop/Continue', withStoppedTick, first: resumed, next, passed: true });
    },
    async hold() {
      const before = prior; api.setAnimationHold(true); const held = await delayedStep(); stationary(before, held, 'Hold');
      api.setAnimationHold(false); const resumed = step(); stationary(held, resumed, 'First actual hold resume');
      const next = await delayedStep(); checkTravel(resumed, next); prior = next;
      report.controls.push({ kind: 'hold', first: resumed, next, passed: true });
    },
    async heldStep(label) { const held = await delayedStep(); stationary(prior, held, label); prior = held; return held; },
    async resumedStep(label) {
      const first = step(); stationary(prior, first, label);
      const next = await delayedStep(); checkTravel(first, next); prior = next;
      report.controls.push({ kind: label, first, next, passed: true }); return first;
    },
    async confidenceWithoutHeldTick() {
      api.hud.setHidden('reconstructed', true, { announce: false });
      api.hud.setHidden('reconstructed', false, { announce: false });
      return this.resumedStep('Confidence hide/show without held tick');
    },
    async range() {
      api.walker.teleport({ ...recipe, local_e: recipe.local_e + 200 });
      const far = await delayedStep(); need(!actor.visible, 'Native range control did not actually leave draw reach');
      api.walker.teleport(recipe);
      // Exercise the actual native same-tier lastUpdate visibility replay. It
      // owns no new assets and must not prime either production elapsed clock.
      await api.townTransport.setTier(report.row.tier);
      need(actor.visible, 'Native synthetic tier refresh did not actually restore draw visibility');
      const synthetic = snapshot(); stationary(far, synthetic, 'Synthetic native range visibility refresh');
      const first = step(); stationary(far, first, 'First actual range return');
      need(actor.visible, 'Native range return did not draw actual model');
      const next = await delayedStep(); checkTravel(first, next); prior = next;
      report.controls.push({ kind: 'range with native synthetic tier refresh', synthetic, first, next, passed: true });
    },
    finish() {
      remaining(); freeze(); report.final = step();
      need(report.windows.length === 3 && report.windows.every(w => w.passed), 'Complete finite cadence matrix absent');
      need(report.controls.length === 8, 'Complete transition matrix absent');
      report.passed = true; return report;
    },
    cleanup() {
      freeze(); api?.renderer.setAnimationLoop(null); const person = row?.person_id;
      api?.townTransport?.dispose();
      const remainingActors = api?.townTransport?.actors.length ?? 0;
      api?.humans?.dispose();
      const driverLeases = api?.humans?.assets?.loaded ?? [];
      return { remaining_transport_actors: remainingActors, driver_leases: driverLeases,
        passed: remainingActors === 0 && driverLeases.length === 0 };
    },
  };
})();
