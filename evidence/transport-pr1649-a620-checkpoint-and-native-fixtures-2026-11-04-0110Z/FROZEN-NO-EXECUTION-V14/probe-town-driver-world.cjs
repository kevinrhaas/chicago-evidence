// SPDX-License-Identifier: GPL-3.0-or-later
// REAL APP PROBE, PREPARED UNRUN. A caller supplies its ordinary guarded browser/page.
const fs = require('node:fs');
const path = require('node:path');
const SCOPE_PREDICATES = {"A": ["P01_source_profile", "P02_native_boot_entry", "P03_coldFind_ordinary_mount", "P04_one_live_identity_asset", "P05_complete_producer_route", "P06_independent_fullroute", "P07_actual_walk_reach", "P08_trusted_Stop", "P09_stopped_hold_and_PNG"], "B": ["P01_source_profile", "P02_native_boot_entry", "P03_coldFind_ordinary_mount", "P04_one_live_identity_asset", "P05_complete_producer_route", "P08_trusted_Stop", "P10_blocked_trusted_refusal", "P11_clear_Continue_offer", "P12_trusted_Continue_advance_PNG"], "C": ["P01_source_profile", "P02_native_boot_entry", "P03_coldFind_ordinary_mount", "P04_one_live_identity_asset", "P05_complete_producer_route", "P13_posed_proxy_unified_pick", "P14_visible_scene_person_record", "P15_trusted_Find_handler_and_close", "P16_Light_restore_and_PNG"]};

async function probeTownDriverWorld(page, { sceneId, touch = false, moduleBase,
  outdir, label, timeoutMs = 30000, bootReadyMs = 240000, mountReadyMs = 300000, checkLight = true, routeProbe = null, scope = null } = {}) {
  if (!outdir || !label || !moduleBase || !['1835', '1904'].includes(String(sceneId))) throw Error('world probe: concrete case/output bindings required');
  sceneId = String(sceneId);
  if (!['1835', '1904'].includes(sceneId) || !['A', 'B', 'C'].includes(scope)) throw Error('Explicit1835/1904 A/B/C scope required');
  if (scope === 'C' && !checkLight) throw Error('ScopeC requires original Light restore assertions');
  fs.mkdirSync(outdir, { recursive: true });
  const readings = [], images = [], errors = [];
  const phases = [], phaseStarted = Date.now();
  const markPhase = (name, detail = {}) => {
    phases.push({ name, hostUtc: new Date().toISOString(), hostElapsedMs: Date.now() - phaseStarted, ...detail });
    fs.writeFileSync(path.join(outdir, label + '-PHASES.json'), JSON.stringify(phases, null, 2) + '\n');
  };
  const onError = e => errors.push(String(e)); page.on('pageerror', onError);
  const flushReadings = () => fs.writeFileSync(path.join(outdir, label + '-LIVE-READINGS.json'), JSON.stringify(readings, null, 2) + '\n');
  const read = async name => {
    const value = await page.evaluate(() => {
      const a = window.__chicago4d, loop = a.townTransport?.actors[0];
      const personId = loop?.personId, human = personId && a.humans.get(personId);
      const liveRoots = [];
      if (personId) a.scene3d.traverse(n => { if (n.userData?.personId === personId) liveRoots.push(n.uuid); });
      const btn = document.getElementById('btn-interact');
      return { scene: String(a.scene?.id ?? a.year), detail: a.detail, error: a.error,
        problems: [...a.problems], frame: a.renderer.info.render.frame,
        graphics: { actualPixelRatio: a.renderer.getPixelRatio(), devicePixelRatio: devicePixelRatio, nativeQualityPreference: a.hud.settings.quality, governor: a.governor },
        walker: { e: a.walker.state.e, n: a.walker.state.n, flying: a.walker.state.flying },
        humanCount: a.humans.count, allHumanRoots: a.humans.actors.map(h => ({ personId: h.personId, rootUUID: h.root.uuid })),
        loop: loop?.snapshot() ?? null, actorCount: a.townTransport?.actors.length ?? 0,
        canResume: loop?.canResume() ?? null,
        human: human ? { id: human.id, personId: human.personId, rootUUID: human.root.uuid,
          assetId: human.instance.appearance.asset_id, position: human.position,
          externallyOwned: a.humans.external(personId) === human } : null,
        identities: personId ? a.humans.actors.filter(h => h.personId === personId).length : 0,
        livePersonRoots: liveRoots, button: btn ? { hidden: btn.hidden,
          thing: btn.dataset.thing, label: btn.querySelector('.ik-what')?.textContent } : null,
        peopleCard: a.people?.state?.open ?? null, travel: a.travelState,
        renderer: { memory: { ...a.renderer.info.memory }, render: { ...a.renderer.info.render } },
      };
    });
    readings.push({ name, utc: new Date().toISOString(), value });
    fs.writeFileSync(path.join(outdir, label + '-LIVE-READINGS.json'), JSON.stringify(readings, null, 2) + '\n'); return value;
  };
  const check = (ok, why) => { if (!ok) throw Error(`world interaction: ${why}`); };
  const frames = async (count = 2) => {
    const from = await page.evaluate(() => window.__chicago4d.renderer.info.render.frame);
    await page.waitForFunction(({ from, count }) => window.__chicago4d.renderer.info.render.frame >= from + count,
      { from, count }, { timeout: timeoutMs, polling: 100 });
  };
  const screenshot = async suffix => {
    const file = path.join(outdir, `${label}-${suffix}.png`);
    const capture = await page.context().newCDPSession(page);
    try {
      const result = await bounded(capture.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false }));
      fs.writeFileSync(file, Buffer.from(result.data, 'base64')); images.push(file);
    } finally { await capture.detach(); }
  };
  const bounded = async promise => {
    let timer;
    try { return await Promise.race([promise, new Promise((_, reject) => {
      timer = setTimeout(() => reject(Error('native input/capture acknowledgement exceeded original30s budget')), timeoutMs);
    })]); } finally { clearTimeout(timer); }
  };
  const press = async () => {
    let priorClicks = 0;
    if (touch) {
      const point = await page.evaluate(() => {
        const button = document.getElementById('btn-interact'), box = button.getBoundingClientRect();
        const x = box.x + box.width / 2, y = box.y + box.height / 2;
        if (button.hidden || !box.width || !box.height || button.disabled
          || button.getAttribute('aria-disabled') === 'true' || !button.contains(document.elementFromPoint(x, y))) {
          throw Error('actual Interact button is hidden, disabled or covered');
        }
        if (!window.__transportProbeTrustedClicks) {
          window.__transportProbeTrustedClicks = [];
          button.addEventListener('click', event => window.__transportProbeTrustedClicks.push({
            trusted: event.isTrusted, pointerType: event.pointerType, label: button.getAttribute('aria-label')
          }), { capture: true });
        }
        return { x, y, prior: window.__transportProbeTrustedClicks.length };
      });
      priorClicks = point.prior;
      touchSession ??= await page.context().newCDPSession(page);
      await bounded(Promise.all([
        touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: point.x, y: point.y }] }),
        touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }),
      ]));
    } else await page.keyboard.press('r');
    await frames(2);
    if (touch) {
      const clicks = await page.evaluate(from => window.__transportProbeTrustedClicks.slice(from), priorClicks);
      check(clicks.length === 1 && clicks[0].trusted && clicks[0].pointerType === 'touch',
        'native trusted touch did not reach the actual Interact button exactly once');
      readings.push({ name: 'actual-trusted-DOM-touch-click', value: clicks[0] });
      flushReadings();
    }
  };
  let touchSession = null;
  try {
    markPhase('before-native-app-ready');
    await page.waitForFunction(() => window.__chicago4d?.ready || !!window.__chicago4d?.error, null, { timeout: bootReadyMs, polling: 1000 });
    markPhase('after-native-app-ready');
    const bootFailure = await page.evaluate(() => window.__chicago4d?.error ?? null);
    check(!bootFailure, `app boot failed: ${bootFailure}`);
    const initial = await read('actual-ready-app'); check(initial.scene === sceneId && !initial.error, 'wrong scene or app error');
    check(initial.actorCount === 0, 'probe requires a fresh boot-ready welcome before occupied actors load');
    check(initial.graphics.nativeQualityPreference === 1 && initial.graphics.actualPixelRatio > 0 && initial.graphics.actualPixelRatio <= 1, 'native Low(1) sharpness preference was not applied');
    check(initial.detail === (touch ? 'balanced' : 'full'), 'native stored visitor detail tier was not applied at boot');
    markPhase('before-native-welcome-entry');
    await page.evaluate(async () => {
    if (!document.getElementById('gate').hasAttribute('hidden')) {
      const welcome = window.__chicago4d.welcome;
      if (welcome) {
        const deadline = Date.now() + 90_000;
        while (welcome.state !== 'world' && Date.now() < deadline) {
          if (welcome.state === 'welcome') welcome.enter('spawn');
          if (welcome.state !== 'world') await new Promise((r) => setTimeout(r, 100));
        }
      } else document.getElementById('home-roam')?.click();
      await new Promise((r) => setTimeout(r, 150));
      document.exitPointerLock?.();
    }
    const help = document.getElementById('control-help');
    if (help && !help.hasAttribute('hidden')) {
      document.getElementById('control-help-gotit')?.click();
    }
  });
    markPhase('after-native-welcome-entry');
    const enteredWorld = await page.evaluate(() => window.__chicago4d.welcome?.state === 'world');
    check(enteredWorld, 'native90s welcome entry did not reach world');
    markPhase('before-original-setDetail', { requestedTier: touch ? 'balanced' : 'full' });
    await page.evaluate(async tier => {
      const a = window.__chicago4d; await a.setDetail(tier);
      a.setFly(false); a.setPace('walk'); a.setAnimationHold(false); a.hud.setPanel(false); a.popup.close();
    }, touch ? 'balanced' : 'full');
    markPhase('after-original-setDetail');
    // A real source/published row and the actual route module choose the setup.
    // Only this starting camera placement is a harness teleport; the approach
    // below uses ordinary keyboard/touch movement and ordinary lazy loading.
    markPhase('before-cold-person-Find-setup');
    const setup = await page.evaluate(async ({ sceneId, moduleBase }) => {
      const a = window.__chicago4d;
      const response = await fetch(new URL('transport/driven/loops.json', a.dataBase));
      if (!response.ok) throw Error(`actual route table HTTP${response.status}`);
      const config = await response.json(), row = config.rows.find(r => r.scene === sceneId);
      if (!row) throw Error('actual scene has no driven row');
      const { roundedBlockRoute, circleRoute } = await import(new URL('transport-loop.js', new URL(moduleBase, location.href)).href);
      const route = row.route.kind === 'rounded_block' ? roundedBlockRoute(row.route) : circleRoute(row.route);
      const pose = route.at(row.initial_distance_m ?? 0);
      const lead = row.root_ahead_of_rear_axle_m + row.driver_local_m[2];
      const driver = { e: pose.e + Math.sin(pose.yaw) * lead, n: pose.n - Math.cos(pose.yaw) * lead };
      const old = a.humans.get(row.person_id);
      const coldBefore = { actors: a.townTransport.actors.length,
        external: !!a.humans.external(row.person_id), detail: a.detail };
      if (coldBefore.actors !== 0 || coldBefore.external) throw Error('cold Find requires the ordinary unloaded driver');
      a.setTravelMode('instantly');
      const accepted = a.goToTarget({ kind: 'person', id: row.person_id, label: 'Driver' });
      if (!accepted) throw Error('ordinary cold person Go to was refused');
      const expected = [1, -1].map(side => ({ e: driver.e + Math.cos(pose.yaw) * side * 4,
        n: driver.n + Math.sin(pose.yaw) * side * 4 }));
      const actual = { e: a.walker.state.e, n: a.walker.state.n };
      if (!expected.some(p => Math.hypot(p.e - actual.e, p.n - actual.n) < 1e-6))
        throw Error('cold person Go to did not use the actual configured driver seat stand');
      return { row, originalRootUUID: old?.root.uuid ?? null, originalCount: a.humans.count,
        coldFind: { before: coldBefore, accepted: !!accepted, actual, expected, noForcedReadyOrAssetWarmup: true } };
    }, { sceneId, moduleBase });
    markPhase('after-cold-person-Find-setup');
    setup.originalRootUUID = initial.allHumanRoots.find(h => h.personId === setup.row.person_id)?.rootUUID ?? null;
    setup.originalCount = initial.humanCount;
    fs.writeFileSync(path.join(outdir, label + '-ACTUAL-COLD-FIND.json'), JSON.stringify(setup.coldFind, null, 2) + '\n');
    // Diagnostic only: passive reads while the ORIGINAL mount predicate waits.
    // At most one read is in flight; a blocked browser cannot queue more samples.
    markPhase('before-original-mount-wait');
    const mountSamples = [], mountStarted = Date.now();
    let mountSampling = true, mountReadPending = false, mountReadStarted = null;
    const persistMountSample = value => {
      mountSamples.push({ hostUtc: new Date().toISOString(), hostElapsedMs: Date.now() - mountStarted, ...value });
      fs.writeFileSync(path.join(outdir, label + '-MOUNT-TELEMETRY.json'), JSON.stringify(mountSamples, null, 2) + '\n');
    };
    const sampleMount = () => {
      if (!mountSampling) return;
      if (mountReadPending) { persistMountSample({ browserReadStillPending: true, pendingMs: Date.now() - mountReadStarted }); return; }
      mountReadPending = true; mountReadStarted = Date.now();
      page.evaluate(() => {
        const a = window.__chicago4d, gate = document.getElementById('gate');
        return { browserUtc: new Date().toISOString(), browserNowMs: performance.now(),
          frame: a?.renderer?.info?.render?.frame ?? null, detail: a?.detail ?? null,
          documentHidden: document.hidden, visibilityState: document.visibilityState,
          gateHidden: gate ? gate.hidden : null, welcome: a?.welcome?.state ?? null,
          ready: a?.ready ?? null, error: a?.error ?? null, problems: [...(a?.problems ?? [])],
          confidenceHidden: a?.confidence?.hidden ? { ...a.confidence.hidden } : null,
          camera: a?.camera ? { x: a.camera.position.x, y: a.camera.position.y, z: a.camera.position.z } : null,
          walker: a?.walker ? { e: a.walker.state.e, n: a.walker.state.n } : null,
          town: a?.townTransport?.snapshot?.() ?? null, actorCount: a?.townTransport?.actors?.length ?? null,
          humanCount: a?.humans?.count ?? null,
          // Asset keys include pending entries, not proof GLTF parse completed.
          humanAssetRequestedEntries: a?.humans?.assets?.loaded ?? null,
          rendererMemory: a?.renderer?.info?.memory ? { ...a.renderer.info.memory } : null,
          rendererRender: a?.renderer?.info?.render ? { ...a.renderer.info.render } : null,
          animationHold: 'not exposed by read-only public API; no setter called' };
      }).then(value => { if (mountSampling) persistMountSample({ browser: value }); })
        .catch(error => { if (mountSampling) persistMountSample({ browserReadError: String(error) }); })
        .finally(() => { mountReadPending = false; });
    };
    sampleMount();
    const mountSampleTimer = setInterval(sampleMount, 10000);
    try {
      await page.waitForFunction(personId => {
        const a = window.__chicago4d, actor = a.townTransport?.driverForPerson(personId);
        return actor?.visible && a.humans.external(personId)?.body;
      }, setup.row.person_id, { timeout: mountReadyMs, polling: 100 });
    } finally {
      mountSampling = false; clearInterval(mountSampleTimer);
      persistMountSample({ mountWaitEnded: true, readStillPending: mountReadPending });
      markPhase('original-mount-wait-ended');
    }
    markPhase('after-original-mount-predicate-passed');
    const mounted = await read('ordinary-near-loader-mounted-actual-driver');
    check(mounted.identities === 1 && mounted.livePersonRoots.length === 1 && mounted.human.externallyOwned,
      'seated driver identity is missing or duplicated');
    check(mounted.human.assetId === setup.row.driver_asset, 'actual driver asset does not match its route row');
    const producer = await page.evaluate(id => window.__chicago4d.townTransport.actors.find(a => a.id === id)?.routeReading, setup.row.id);
    check(producer?.status === 'RENDERED_ROUTE_STATIC_CLEARANCE_AND_SUPPORT_SAMPLES_PASS'
      && producer.horse_support_reader_used === true && Number.isFinite(producer.full_circuit_length_m)
      && producer.full_circuit_length_m > 0 && producer.samples === Math.ceil(producer.full_circuit_length_m / .25) + 1
      && producer.maximum_spacing_m <= .25 && producer.maximum_wheel_gap_m <= .03,
      'Ordinary mounted actor lacks its complete actual producer route receipt');
    readings.push({ name: 'actual-complete-producer-route-receipt-every-scope', value: producer });
    flushReadings();
    if (scope === 'A') {
      check(typeof routeProbe === 'function', 'ScopeA requires full independent whole-route observer');
      readings.push({ name: 'actual-whole-circuit-ground-and-clearance', value: await routeProbe(page, { row: setup.row, moduleBase }) });
      flushReadings();
    }

    if (scope === 'A') {
    const beforeWalk = await page.evaluate(() => {
      const a = window.__chicago4d, actor = a.townTransport.actors[0], at = actor.at;
      const yaw = actor.snapshot().yaw_rad;
      a.walker.teleport({ local_e: at[0] + Math.cos(yaw) * 7.5, local_n: at[1] + Math.sin(yaw) * 7.5,
        yaw_deg: (Math.atan2(-Math.cos(yaw), -Math.sin(yaw)) * 180 / Math.PI + 360) % 360 });
      a.interactKey.refresh();
      return { e: a.walker.state.e, n: a.walker.state.n, actorAt: at, hidden: document.getElementById('btn-interact').hidden };
    });
    check(beforeWalk.hidden, 'Interact offered beyond the actual reach');
    if (touch) {
      touchSession = await page.context().newCDPSession(page);
      const v = page.viewportSize(), point = { x: Math.round(v.width * .25), y: Math.round(v.height * .65) };
      await touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [point] });
      await touchSession.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: point.x, y: point.y - 24 }] });
    } else await page.keyboard.down('w');
    try {
      await page.waitForFunction(() => {
        const a = window.__chicago4d; return !document.getElementById('btn-interact').hidden
          && a.interactKey.current?.kind === 'vehicle';
      }, null, { timeout: timeoutMs, polling: 100 });
    } finally {
      if (touchSession) await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      else await page.keyboard.up('w');
    }
    const approached = await read('actual-keyboard-or-touch-walk-into-reach');
    check(Math.hypot(approached.walker.e - beforeWalk.e, approached.walker.n - beforeWalk.n) > 1,
      'no actual walk occurred before Interact appeared');
    check(approached.button.label === 'Stop driver', 'wrong offered action');
    await press();
    const stopped = await read('actual-interact-stopped-driver');
    check(stopped.loop.state === 'stopped', 'R/touch did not stop the actual controller');
    await frames(3);
    const held = await read('actual-stopped-controller-held-across-rendered-frames');
    check(held.loop.total_distance_m === stopped.loop.total_distance_m
      && JSON.stringify(held.loop.wheel_rotation_rad) === JSON.stringify(stopped.loop.wheel_rotation_rad), 'stopped vehicle advanced');
    await screenshot('STOPPED');

    }
    if (scope === 'B') {
    await page.evaluate(() => {
      const a = window.__chicago4d, actor = a.townTransport.actors[0], at = actor.at, yaw = actor.snapshot().yaw_rad;
      a.walker.teleport({ local_e: at[0] + Math.cos(yaw) * 4.5, local_n: at[1] + Math.sin(yaw) * 4.5,
        yaw_deg: (Math.atan2(-Math.cos(yaw), -Math.sin(yaw)) * 180 / Math.PI + 360) % 360 });
      a.interactKey.refresh();
    });
    const setupStop = await read('scopeB-harness-side-stand-no-walk-claim');
    check(setupStop.button.label === 'Stop driver', 'ScopeB shared actual Stop offer missing');
    await press();
    const stopped = await read('actual-interact-stopped-driver');
    check(stopped.loop.state === 'stopped', 'R/touch did not stop the actual controller');
    // Deliberate obstruction fixture; this is not reported as a natural walk.
    await page.evaluate(() => {
      const a = window.__chicago4d, at = a.townTransport.actors[0].at;
      a.walker.teleport({ local_e: at[0], local_n: at[1] }); a.interactKey.refresh();
    });
    const blocked = await read('deliberate-visitor-obstruction');
    check(blocked.canResume === false && /Step back/.test(blocked.button.label), 'visitor obstruction did not refuse resume');
    await press();
    const refused = await read('blocked-continue-refused');
    check(refused.loop.state === 'stopped' && refused.loop.total_distance_m === stopped.loop.total_distance_m,
      'obstructed Interact moved the vehicle');
    await page.evaluate(() => {
      const a = window.__chicago4d, actor = a.townTransport.actors[0], at = actor.at, yaw = actor.snapshot().yaw_rad;
      a.walker.teleport({ local_e: at[0] + Math.cos(yaw) * 4.5, local_n: at[1] + Math.sin(yaw) * 4.5,
        yaw_deg: (Math.atan2(-Math.cos(yaw), -Math.sin(yaw)) * 180 / Math.PI + 360) % 360 });
      a.interactKey.refresh();
    });
    const clear = await read('clear-side-stand');
    check(clear.canResume === true && clear.button.label === 'Continue journey', 'clear stand did not offer Continue');
    await press();
    await page.waitForFunction(distance => window.__chicago4d.townTransport.actors[0].snapshot().total_distance_m > distance + .005,
      stopped.loop.total_distance_m, { timeout: timeoutMs, polling: 100 });
    const continued = await read('actual-continue-advanced-distance');
    check(continued.loop.state === 'moving', 'Continue did not enter moving state');
    await screenshot('CONTINUED');

    }
    if (scope === 'C') {
    markPhase('before-real-driver-inspection');
    await page.evaluate(() => {
      const a = window.__chicago4d, actor = a.townTransport.actors[0], at = actor.at, yaw = actor.snapshot().yaw_rad;
      a.walker.teleport({ local_e: at[0] + Math.cos(yaw) * 4.5, local_n: at[1] + Math.sin(yaw) * 4.5,
        yaw_deg: (Math.atan2(-Math.cos(yaw), -Math.sin(yaw)) * 180 / Math.PI + 360) % 360 });
      a.interactKey.refresh();
    });
    readings.push({ name: 'scopeC-harness-side-stand-no-walk-claim', value: { local_side_distance_m: 4.5, actual_walk_claimed: false } });
    flushReadings();
    // Real posed proxy -> existing unified pick path -> existing resident card.
    const picked = await page.evaluate(() => {
      const a = window.__chicago4d, actor = a.humans.external(a.townTransport.actors[0].personId);
      actor.proxy.updateWorldMatrix(true, false);
      const point = actor.proxy.getWorldPosition(actor.root.position.clone());
      const target = point.clone().project(a.camera);
      const hit = a.townTransport.pickDriverAt(target, a.camera);
      window.__transportCardEvents = [];
      a.humans.on('select', d => window.__transportCardEvents.push({type:'select', personId:d.personId, opens:d.opens}));
      a.humans.on('open', d => window.__transportCardEvents.push({type:'open', personId:d.personId, opens:d.opens}));
      const actual = a.pick({ x: target.x, y: target.y });
      return { hitPerson: hit?.personId, pickedPerson: actual?.personId, ndc: { x: target.x, y: target.y } };
    });
    check(picked.hitPerson === setup.row.person_id && picked.pickedPerson === setup.row.person_id,
      'real seated proxy did not resolve through the existing resident pick path');
    if (sceneId === '1835') {
    await page.waitForFunction(personId => window.__chicago4d.people?.state?.open === personId,
      setup.row.person_id, { timeout: timeoutMs });
    const card = await read('actual-seated-driver-existing-resident-card');
    check(card.peopleCard === setup.row.person_id && card.identities === 1, 'wrong or duplicate resident card');
    await page.evaluate(() => { const a = window.__chicago4d; a.people.close(); a.hud.setPanel(false); });
    const goTo = await page.evaluate(personId => {
      const a = window.__chicago4d, actor = a.humans.external(personId);
      const at = actor.position;
      a.setTravelMode('instantly');
      const accepted = a.goToTarget({ kind: 'person', id: personId, label: 'Driver' });
      return { accepted, driver: at, walker: { e: a.walker.state.e, n: a.walker.state.n },
        loop: a.townTransport.driverForPerson(personId).snapshot(), travel: a.travelState };
    }, setup.row.person_id);
    check(goTo.accepted && goTo.loop.state === 'stopped', 'People/Find GoTo did not address and stop the current driver');
    check(Math.hypot(goTo.walker.e - goTo.driver.e, goTo.walker.n - goTo.driver.n) <= 6,
      'instant GoTo used the historical standing location instead of the current driver');
    readings.push({ name: 'actual-People-Find-GoTo-current-moving-driver', value: goTo });
    flushReadings();

    } else {
      // 1904 has no legacy residents layer. Observe the real public Navigator
      // Inspect card and hydrated household record; never invent people.state.
      markPhase('nativeInspector-visible-wait-start', { timeoutMs, pollingMs: 100, expectedPersonId: setup.row.person_id });
      let p14Observed = false;
      try {
      await page.waitForFunction(personId => {
        const a = window.__chicago4d;
        const pane = document.querySelector(`#nav-app-inspect .insp-pane[data-person="${CSS.escape(personId)}"]`);
        const card = pane?.querySelector(`.insp-person-card[data-person-id="${CSS.escape(personId)}"]`);
        const box = card?.getBoundingClientRect();
        const flags = {
          inspectApp: a.navigator?.app === 'inspect', navigatorOpen: a.navigator.level > 0,
          linkedPerson: a.navigator.link?.person === personId, paneNotHidden: !pane?.hidden,
          positiveWidth: box?.width > 0, positiveHeight: box?.height > 0,
          bottomAboveViewportTop: box?.bottom > 0, topBelowViewportBottom: box?.top < innerHeight,
          exactName: card?.querySelector('.insp-person-name')?.textContent?.trim() === 'Hans Johnson',
          census: !!card?.querySelector('.insp-person-census'),
          noWaiting: !card?.querySelector('.insp-person-wait'),
          noHouseholdFailure: !/household record could not be read/i.test(card?.textContent),
        };
        (window.__transportP14Trace ??= []).push({ utc: new Date().toISOString(), performanceMs: performance.now(),
          frame: a.renderer?.info.render.frame, expectedPersonId: personId,
          innerWidth, innerHeight, visualViewport: window.visualViewport ? {
            width: visualViewport.width, height: visualViewport.height, offsetTop: visualViewport.offsetTop, scale: visualViewport.scale } : null,
          navigatorApp: a.navigator?.app, navigatorLevel: a.navigator?.level, link: a.navigator?.link,
          paneDataset: pane ? { ...pane.dataset } : null, paneHidden: pane?.hidden,
          cardDataset: card ? { ...card.dataset } : null, box: box?.toJSON(),
          name: card?.querySelector('.insp-person-name')?.textContent,
          flags, allFlags: Object.values(flags).every(Boolean) });
        return a.navigator?.app === 'inspect' && a.navigator.level > 0
          && a.navigator.link?.person === personId && !pane?.hidden
          && box?.width > 0 && box.height > 0 && box.bottom > 0 && box.top < innerHeight
          && card.querySelector('.insp-person-name')?.textContent?.trim() === 'Hans Johnson'
          && !!card.querySelector('.insp-person-census')
          && !card.querySelector('.insp-person-wait')
          && !/household record could not be read/i.test(card.textContent);
      }, setup.row.person_id, { timeout: timeoutMs, polling: 100 });
      p14Observed = true;
      } finally { markPhase('nativeInspector-visible-wait-end', { observed: p14Observed }); }
      const nativeCard = await page.evaluate(personId => {
        const a = window.__chicago4d;
        const pane = document.querySelector(`#nav-app-inspect .insp-pane[data-person="${CSS.escape(personId)}"]`);
        const card = pane.querySelector(`.insp-person-card[data-person-id="${CSS.escape(personId)}"]`);
        return { p14Trace: window.__transportP14Trace ?? [], viewport: { innerWidth, innerHeight },
          personId: pane.dataset.person, cardPersonId: card.dataset.personId,
          name: card.querySelector('.insp-person-name')?.textContent?.trim(),
          census: card.querySelector('.insp-person-census')?.textContent?.trim(),
          navigator: a.navigator.snapshot(), link: { ...a.navigator.link },
          identities: a.humans.actors.filter(h => h.personId === personId).length,
          legacyPeopleHasState: !!a.people?.state };
      }, setup.row.person_id);
      check(nativeCard.personId === setup.row.person_id && nativeCard.cardPersonId === setup.row.person_id
        && nativeCard.link.id === 'otis_house_2033_prairie' && nativeCard.identities === 1,
        'Native Inspect showed the wrong household/person or a duplicate driver');
      readings.push({ name: 'actual-seated-driver-native-Inspector-Hans-record', value: nativeCard });
      flushReadings();
      // Exercise the product's own Find button through trusted native input.
      // Its ordinary handler must stop/approach the actual moving driver.
      markPhase('before-native-Find');
      const beforeNativeFind = await page.evaluate(personId => {
        const a = window.__chicago4d; a.setTravelMode('instantly');
        const before = { walker: { e: a.walker.state.e, n: a.walker.state.n },
          loop: a.townTransport.driverForPerson(personId).snapshot() };
        window.__transportProbeNativeFindBefore = before;
        return before;
      }, setup.row.person_id);
      const point = await page.evaluate(personId => {
        const selector = `#nav-app-inspect .insp-pane[data-person="${CSS.escape(personId)}"] .insp-person-find[data-person-find="${CSS.escape(personId)}"]`;
        const button = document.querySelector(selector);
        if (!button) throw Error('Actual native person Find action missing');
        button.scrollIntoView({ block: 'center', inline: 'nearest' });
        const box = button.getBoundingClientRect(), x = box.x + box.width / 2, y = box.y + box.height / 2;
        if (button.disabled || button.hidden || !box.width || !box.height || x < 0 || y < 0 || x >= innerWidth || y >= innerHeight
          || button.getAttribute('aria-disabled') === 'true' || !button.contains(document.elementFromPoint(x, y))) {
          throw Error('Actual native Find button is hidden, disabled or covered');
        }
        window.__transportProbeNativeFindClicks ??= [];
        const prior = window.__transportProbeNativeFindClicks.length;
        window.__transportProbeNativeFindOutcomes ??= [];
        const outcome = phase => {
          const base = { phase, browserUtc: new Date().toISOString(), performanceMs: performance.now(), personId };
          try {
            const a = window.__chicago4d, loop = a.townTransport?.driverForPerson(personId)?.snapshot();
            window.__transportProbeNativeFindOutcomes.push({ ...base, frame: a.renderer?.info.render.frame,
              walker: { e: a.walker.state.e, n: a.walker.state.n },
              travel: JSON.parse(JSON.stringify(a.travelState ?? null)),
              loop: loop ? { state: loop.state, reason: loop.reason, total_distance_m: loop.total_distance_m,
                at_enu_m: loop.at_enu_m } : null });
          } catch (error) {
            window.__transportProbeNativeFindOutcomes.push({ ...base, diagnosticError: String(error) });
          }
        };
        button.addEventListener('click', event => {
          window.__transportProbeNativeFindClicks.push({
            trusted: event.isTrusted, pointerType: event.pointerType, personId: button.dataset.personFind,
            text: button.textContent.trim(), browserUtc: new Date().toISOString(),
            performanceMs: performance.now(), eventTimeStamp: event.timeStamp,
            frame: window.__chicago4d.renderer?.info.render.frame,
          });
          outcome('click-capture-before-bubble');
          // Passive snapshots: the ordinary handler alone changes walker/vehicle state.
          // Several microtasks distinguish its queued async continuation from delivery.
          queueMicrotask(() => {
            outcome('click-microtask-1');
            queueMicrotask(() => {
              outcome('click-microtask-2');
              queueMicrotask(() => outcome('click-microtask-3'));
            });
          });
        }, { capture: true, once: true });
        return { x, y, prior };
      }, setup.row.person_id);
      if (touch) {
        touchSession ??= await page.context().newCDPSession(page);
        const inputStarted = Date.now();
        let inputWithinDeadline = true;
        try {
          // One original30s deadline covers both dependent native requests and ACKs.
          // Queue work after bounded installs its timer; neither request gets a new cap.
          await bounded(Promise.resolve().then(async () => {
            markPhase('native-Find-touchStart-send', { inputElapsedMs: Date.now() - inputStarted, timeoutMs });
            await touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: point.x, y: point.y }] });
            markPhase('native-Find-touchStart-ack', { inputElapsedMs: Date.now() - inputStarted });
            if (!inputWithinDeadline) {
              markPhase('native-Find-touchEnd-not-sent-after-deadline', { inputElapsedMs: Date.now() - inputStarted });
              return;
            }
            markPhase('native-Find-touchEnd-send', { inputElapsedMs: Date.now() - inputStarted });
            await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
            markPhase('native-Find-touchEnd-ack', { inputElapsedMs: Date.now() - inputStarted });
          }));
          markPhase('native-Find-both-touch-acks-complete', { inputElapsedMs: Date.now() - inputStarted });
        } catch (error) {
          markPhase('native-Find-touch-input-failed', { inputElapsedMs: Date.now() - inputStarted, failure: String(error) });
          throw error;
        } finally { inputWithinDeadline = false; }
      } else await bounded(page.mouse.click(point.x, point.y));
      await frames(2);
      const nativeClicks = await page.evaluate(from => window.__transportProbeNativeFindClicks.slice(from), point.prior);
      check(nativeClicks.length === 1 && nativeClicks[0].trusted
        && nativeClicks[0].pointerType === (touch ? 'touch' : 'mouse') && nativeClicks[0].personId === setup.row.person_id,
        'Native person Find action did not receive exactly one trusted input');
      const goTo = await page.evaluate(personId => {
        const a = window.__chicago4d, actor = a.humans.external(personId);
        return { driver: actor.position, walker: { e: a.walker.state.e, n: a.walker.state.n },
          loop: a.townTransport.driverForPerson(personId).snapshot(), travel: a.travelState };
      }, setup.row.person_id);
      // accepted records trusted delivery to the native button, not a forged
      // return value from its asynchronous application handler.
      goTo.beforeNativeFind = beforeNativeFind;
      goTo.walkerChangedM = Math.hypot(goTo.walker.e - beforeNativeFind.walker.e,
        goTo.walker.n - beforeNativeFind.walker.n);
      goTo.nativeFindClick = nativeClicks[0];
      goTo.accepted = nativeClicks[0].trusted && goTo.walkerChangedM > .05
        && goTo.loop.state === 'stopped' && goTo.loop.reason === 'approach';
      check(goTo.walkerChangedM > .05, 'Native person Find click did not actually move the visitor');
      check(goTo.accepted && goTo.loop.state === 'stopped' && goTo.loop.reason === 'approach',
        'People/Find GoTo did not address and stop the current driver with the native approach reason');
      check(Math.hypot(goTo.walker.e - goTo.driver.e, goTo.walker.n - goTo.driver.n) <= 6,
        'instant GoTo used the historical standing location instead of the current driver');
      readings.push({ name: 'actual-People-Find-GoTo-current-moving-driver', value: goTo });
      flushReadings();
      await page.evaluate(() => { const a = window.__chicago4d; a.navigator.closeApp(); a.hud.setPanel(false); });
      await page.waitForFunction(() => window.__chicago4d.navigator.level === 0,
        null, { timeout: timeoutMs, polling: 100 });
    }

    if (checkLight) {
      markPhase('before-original-Light-retirement');
      await page.evaluate(async () => { await window.__chicago4d.setDetail('light'); });
      markPhase('after-original-Light-setDetail');
      await page.waitForFunction(() => window.__chicago4d.townTransport.actors.length === 0,
        null, { timeout: timeoutMs, polling: 100 });
      const retired = await page.evaluate(personId => {
        const a = window.__chicago4d, actor = a.humans.get(personId);
        const roots = []; a.scene3d.traverse(n => { if (n.userData?.personId === personId) roots.push(n.uuid); });
        return { detail: a.detail, actorCount: a.townTransport.actors.length, external: !!a.humans.external(personId),
          rootUUID: actor?.root.uuid ?? null, humanCount: a.humans.count, sceneRoots: roots,
          vehicleOffers: a.interactions.list.filter(t => t.kind === 'vehicle' && t.at !== null).length };
      }, setup.row.person_id);
      check(retired.detail === 'light' && !retired.external && retired.vehicleOffers === 0,
        'Light kept a driven model or live interaction offer');
      check(retired.rootUUID === setup.originalRootUUID && retired.humanCount === setup.originalCount,
        'Light failed to restore the original standing ownership/count');
      readings.push({ name: 'actual-Light-retirement-and-standing-owner-restore', value: retired });
      flushReadings();
      markPhase('after-original-Light-retirement-checks-before-PNG');
      await screenshot('LIGHT-RESTORED');
      markPhase('after-original-Light-retirement');
    }
    }
    markPhase('all-scope-actions-ended');
    check(errors.length === 0, `page errors: ${errors.join('; ')}`);
    const result = { status: 'ACTUAL_APP_WORLD_DRIVER_SCOPE_PASS', sceneId, touch, label, scope, predicate_ids: SCOPE_PREDICATES[scope],
      moduleBase, readings, images, pageErrors: errors,
      approachWasActualKeyboardOrCDPTouch: scope === 'A', obstructionWasDeliberateHarnessPlacement: scope === 'B',
      all_original_predicates_in_one_case: false,
      defaultPhoneLightMotionNotClaimed: true, photorealismOrWholeLoopReplayNotClaimed: true };
    fs.writeFileSync(path.join(outdir, `${label}.json`), JSON.stringify(result, null, 2) + '\n');
    return result;
  } catch (error) {
    markPhase('scope-failed', { failure: String(error) });
    fs.writeFileSync(path.join(outdir, `${label}-NONPASS.json`), JSON.stringify({ status: 'ACTUAL_WORLD_SCOPE_PROBE_NONPASS',
      sceneId, touch, label, scope, failure: String(error), readings, images, pageErrors: errors }, null, 2) + '\n');
    throw error;
  } finally {
    await page.keyboard.up('w').catch(() => {});
    if (touchSession) {
      await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }).catch(() => {});
      await touchSession.detach().catch(() => {});
    }
    page.off('pageerror', onError);
  }
}
module.exports = { probeTownDriverWorld };
