# Parked desktop13: failed qualification; merge stopped

Exact head: `2aebef95f6a5b6fa1bd8353db936c7674a73c32f`, PR1174 -> dev. Attempt1 run39673247878/job119476336767, step6 **Run the smoke against the published mirror**. Full job log SHA256: `a8d71c87e23bd27dba750195c3a14dd838795ca356b4834a673a3246f8b50493`. The log's actual step environment and runtime filter declarations both bind desktop/13. The suite finished:151 passed,2 failed,140 staged+13 always-on checks,132m47s. It did not time out.

| Failed assertion | Actual | Requirement |
| --- | --- | --- |
| T-2647: X-RAY one tap away stays inside the draw budget |8223 driver draws | <=7800;423 over |
| T-2648: reconstructed row Ghost40% stays inside the draw budget |8469 driver draws | <=7800;669 over |

The latter reports mode=ghost, opacity=.4, summary=Ghost ·40%, changed pixels mean7.56/worst34. The first logged failure is T-2647 at21:53:02.4117318Z; T-2648 follows at21:58:39.8235393Z. There is no causal exception stack or preceding captured page/HTTP/console/request error. Both `the suite body ran to completion` and `zero page errors` pass at the tail. The smoke's error collection includes pageerror, HTTP>=400, non-ERR_ABORTED request failures and console.error other than `Failed to load resource`; this is zero under those existing exclusions, not a claim about excluded events.

## Baseline evidence and limits

`dev-smoke-state.mjs ask --viewport desktop --stage13` was read, never recorded into. Its numeric13 latestPASS is2026-10-09, before the2026-10-11 stage renumbering. The relevant older navigation/settings part12 has an Oct10 PASS101 on a dirty, different tree. No standing reading records either current failed assertion. T-2970 changed draw-count units and established7800 on2026-10-21 at08:04UTC (commit7409cb58b); its six calibration stands were ordinary views. Parent fdb227dbf already contains that change. Old passes therefore do not establish a current passing baseline, and there is no evidence sufficient to label these failures inherited.

The ask command reports the current shared covered-stage tree dirty; its hash is not the failed CI tree. Every diagnosis of parked runtime uses saved exact2aeb Git blobs (`pinned-source/MANIFEST.json`). Working `placements.json` differs because the covered lane owns it; that working version is not used to estimate the failed layer.

## Camera and rendering state in the actual test source

- Part13 enters1835 and initially sets eye height1.68m. It deliberately takes no initial calibrated pose. It later runs camera movement checks.
- The last camera-changing test before T-2647/T-2648 is **Go there rides to the person's building** (`smoke_renderer.mjs`15263-15288): it rides on horse to `hogan_store`, simulates `(distance/6.5)+30` seconds, verifies idle arrival, Hogan's card and framing, then changes travel mode to instantly and closes the popup/person card.
- `travel.js`204-211 and374-391 resolve the destination through `main.js`4039-4102 `framing(id,{mode:'horse',card:true})`;466-495 ease yaw/pitch to that target and finish by restoring the visitor's pace. The preceding test explicitly restores visitor pace=walk. The building/card/viewport geometry, street router, terrain and arrival simulation determine the exact stand and orientation.
- No subsequent source block before these budget reads teleports or starts another ride. Settings theme/skin/text/researcher/sound checks alter UI/state and restore them. Field Check start/skip samples/paints UI (`tour.js`), without moving the walker.
- T-2647 clicks BY GRADE, X-RAY, reads stats after `step()`, then NORMAL. T-2648 starts BY GRADE, changes reconstructed grade to Tint100%, safe/vermilion swatch, Tint0%, then Ghost40%, captures and reads stats after `step()`. Both use the unchanged7800 bar.
- CI does **not** print numeric camera pose, effective auto detail/profile or the saved successful `goThere` details. A source reconstruction is available; its equality to the historic CI floating-point pose cannot be asserted before measurement. A later targeted run must save full pose and state, and label any mismatch explicitly.

## New layer contribution and candidate source paths

Exact2aeb1835 contains three farm-box wagons. `parked-transport.js`31-59 batches each by the GLB material object. The pinned GLB has five used material IDs, all OPAQUE/front-sided, so at most15 ordinary Mesh batches exist for1835. They are not BatchedMesh multi-draw instances. Visibility is restricted to100m Full/65m Balanced/0m Light. Each visible batch can contribute one ordinary colour draw and, in a normal shadowed frame, one directional shadow-map draw. This is a static envelope, not an observed per-frame attribution.

All their confidence values are1 (reconstructed). `confidence.js`548-589 reads that exact range;625-651 omits a wholly ghosted ordinary mesh from the opaque/shadow pass and draws it in the ghost pass. These objects are not automatically doubled in both colour passes. The new layer's picking is `THREE.Raycaster.intersectObjects`, with no GPU render/readback. Three old vehicles become separate fallback yard chunks (`yard.js`3196-3206/3359/3473-3477), and their visibility is owned by the parked layer; this adds a small number of ordinary meshes but also interacts with existing furniture visibility.

`main.js`1420/2034 lists furniture for Ghost-as-dither, excluding `parked-transport`. That is a policy-alignment candidate to inspect, **not yet a warranted performance fix**: for wholly reconstructed meshes the current ghost plan already removes their opaque/shadow draws, and dither could reintroduce a shadow draw. Do not add the layer blindly or assume15 batches explain423/669 excess.

`far-merge.js` requires the entire cluster beyond340m, while parked authored models disappear by100m. Far-merging these models cannot legitimately address this frame. Existing fallback visibility can conflict with furniture/far-merge ownership because `tick()` updates furniture first and parked fallbacks afterward; any fix needs a measured duplicate/visibility proof, not blanket merging or skipping.

The Light structure shadow-caster optimization (`main.js`2095/2590 and `shadow-casters.js`) and confidence BatchedMesh range/instance culling are legitimate existing performance mechanisms to inspect if per-pass attribution identifies them. Current evidence does not identify a safe source change there. Keep all budgets, modes, assertions and geometry intact.

## Saved parent overlay inputs and prebuilt honesty

`virtual-overlay-inputs/MANIFEST.json` saves29 exact Git blobs, including both refs' changed existing runtime/data files, new2aeb model/module bytes and common camera/travel/confidence support. No checkout, worktree, clone, fetch, publish or index mutation occurred.

For a parent-runtime control, intercept BOTH `/walk/js/...` and `/js/...` module aliases when requested, plus `/data/...` paths. Serve exact fdb227dbf blobs for `main.js`, `yard.js`, `street-grid.js`, `data/scenes/1835.json`, `data/scenes/1904.json`, `data/liberties.json`, and `data/scene.schema.json` if fetched. The parent should request no new parked module, placement or model. The new-runtime arm must route exact2aeb equivalents, `parked-transport.js`, parked placements/manifests and the three new GLBs; this prevents the staged covered placement changes entering either arm. Original common assets can be shared only after their bytes are verified against pinned source inputs, including compressed-published representation where appropriate. Do not claim the current shared mirror is exact2aeb merely from its build stamp.

All declared source input hashes in the current shared1835 prebuilt indices were checked against BOTH pinned refs: base70/frontage71/ground64/streets64/yards81, **zero mismatches** (`all-prebuilt-inputs-vs-pinned-baseline.json`). None of the changed runtime/data files is a declared input of those five builders. The page/prebuilt build stamps currently say2aebef95f. This supports reusing those unchanged derived buffers as a common test substrate after binary-integrity and runtime used/reason checks; it does not turn the overlay into a historical fdb publish.

If a later audit finds a changed input, missing/mismatched buffer, build or replay refusal, stop that comparison. Do not retag an index, rewrite its hashes, lie about the build or accept different builder paths between arms. A separately labelled matched browser-build fallback can be proposed only if needed; it must be identical in both arms and is not a claim about the original CI published prebuild.

## One proposed later finite comparison — not executed

After the covered browser lane is released, run one sequential two-arm read-only overlay comparison, under a single <=10min foreground budget and <=240s boot per arm; no full part13 rerun or CI POST. Use desktop1280x800/DPR1,1835,keep-geometry=1 and the same existing browser launch flags. Pin one recorded effective detail/profile/sharpness/season state across both arms so auto profiling under changing load cannot change the comparison.

In the new arm, reconstruct the exact source's final Sauganash instant-arrival -> Hogan horse-arrival camera prefix with the original travel simulator, walk pace and1.68m eye. Save the resulting full walker/camera pose, projection, state and successful framing. Reuse the identical saved pose/state in the parent arm; assert equality before each read. This yields an exact paired pose; call it the historic failed pose only if the relevant state and8223/8469 readings reproduce. Otherwise report a controlled-pose result and the reproduction gap, rather than silently moving the camera until the bar passes.

At that unchanged pose read NORMAL, X-RAY and reconstructed Ghost40% in each arm using the original state/control sequence. Save driver draws (`renderer.__driverDraws`), renderer calls, triangles, ghostStats, shadow-caster/far-merge state, visible parked batches, loader/captured errors, actual requested/served SHA hashes and prebuilt used/reasons. One bounded candidate-root hide read in each ghost state may isolate direct parked contribution (a counterfactual with fallbacks unchanged, not a parent baseline). No source or test edits are needed.

If parent also exceeds7800, retain the failed qualification and report the same-pose inherited counterexample with exact bindings; if only new exceeds, measure the responsible pass/layer before proposing a source fix. Either result remains a diagnosis, not permission to ignore a red or weaken7800. Stop on route/hash/state/pose drift or deadline. Root must authorize the browser lane and any later source fix or CI action separately.
