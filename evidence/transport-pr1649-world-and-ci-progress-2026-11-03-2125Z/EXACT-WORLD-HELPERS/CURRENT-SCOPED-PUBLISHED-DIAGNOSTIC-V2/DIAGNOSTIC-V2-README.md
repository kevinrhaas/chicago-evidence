Diagnostic V2 — prepared only, browser UNRUN

The original CURRENT-SCOPED-PUBLISHED directory and failed543 case01 are unchanged. This copy preserves all feature predicates and original600s outer,300s mount,240s boot,90s native entry,30s actions and5s independent route CPU caps. run_current_world_case.py, route observer and summary checker are byteexact copies. No production source, native gate, quality/profile, input or model changes.

During the original mount wait, passive telemetry starts immediately and attempts one browser read every10s. Only one browser read may be in flight. If the browser is blocked, a host-only sample records how long that same read has remained pending; no extra browser queries are queued. The interval is cleared in the wait's finally block, including failure. Late reads are ignored after cleanup. Output: frames/published-YEAR-VIEWPORT-scopeSCOPE-MOUNT-TELEMETRY.json.

Reads: host/browser clocks, rendererframe, detail, document.hidden/visibilityState, welcome and DOM gate hidden, confidence hidden flags, camera/walker coordinates, actual town snapshot/count, humans count and requested asset-entry names, problems/error, renderer counts. The private animationHold flag is not exposed read-only, so the diagnostic explicitly says it cannot read it; it never calls a setter. Human asset entry names include pending GLTF promises and do not claim parse completion.

The Node observer also saves WORLD-CASE-RESULT.json every10s, with actual served-file count and timestamps/bytes of transport, human, decoder and hitch stages. Its interval is cleared in observer finally. HTTP bodies and source hash checks are unchanged. This gives durable server progression even when the browser's main thread is blocked.

Use the same actual543 checked-source ROOT GO as case01, in a NEW output directory, changing only helper path:

  python /workspace/.cloud-setup/transport-current-20261103/world-prep/CURRENT-SCOPED-PUBLISHED-DIAGNOSTIC-V2/run_current_world_case.py --binding ACTUAL_543_ROOT_GO_JSON --year 1904 --viewport mobile --scope C --out NEW_DURABLE_OUTPUT

Root owns detached Python/supervisor session setup; this packet does not alter supervisor/deadline ownership or the original600s cap. No browser was launched here.

Read-only diagnosis of case01

- APIready/world entry and accepted cold personGoTo do not prove the model mounted. The actual original300s predicate timed out; the environment transition killed its Python/supervisor owners, so the surviving Node timeout must not be promoted into a completed guarded product-gate verdict.
- ensureNear is called in main tick only while gate closed, animation not held, document visible and reconstructed confidence visible. Full/Balanced have nonzero reach; Light does not. It only starts ready near the circuit. A later Light tier/disposal generation cancels a load without a product error.
- ready awaits complete route preflight before makeAssembly. Current native preflight yields once initially and between128-sample chunks using setTimeout0, not an explicit rAF. Each chunk competes with actual software-rendered frame work.
- Case01 actually served driven-assembly-loader/draft-hitch modules and the explicit Brougham-near master, anonymous1904lod3 human and drivenad9 horse. In the ordinary path these requests occur AFTER route preflight, inside the parallel asset acquisition/parse stage. No hitch-bindings-v2.json was served; hitch is awaited later, after those jobs settle and driver setup. This narrows the last observable stage to assets/parse/setup rather than proving ensureNear never ran.
- Serving a GLB is not GLTF/meshopt parse completion. Promise.allSettled deliberately waits for every independent asset; until it settles, neither actor nor problems need appear. Human meshes and hitch are attached only after setup. Private in-flight state cannot be read without altering source; V2 makes no such alteration.
- Renderer cadence, visibility/tier transitions, parse/decoder progress and the environment interruption remain competing explanations. No app bug, terrain refusal or harmless300s timing assumption is asserted from the current incomplete evidence.
