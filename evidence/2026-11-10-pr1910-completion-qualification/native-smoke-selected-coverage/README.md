# Final published stockade consumer and hosted smoke recovery

Both final published official stage1 runs completed at source `af4cc3ff486a90571edb7f3bb48ee1609343ad5f`, build `af4cc3ff48`: desktop95 passed/0 failed in455.17s; mobile95/0 in134.11s. Each retained all82 staged and13 always-on assertions, completed the suite, and reported zero page errors. Both timeout flags are false. Entire before/after bindings are equal, including source HEAD, published build, renderer files and stockade/garden MASTER/WEB/published files. GPU release was checked after both browsers exited.

Actual commands in separate serial calls, sourced environment, app working directory:

```sh
PW_EXECUTABLE=/usr/bin/chromium NODE_PATH=/tmp/chicago-browser-tools/node_modules SMOKE_VIEWPORT=desktop SMOKE_STAGE=1 SMOKE_TIMING=1 node tools/smoke_renderer.mjs --published
PW_EXECUTABLE=/usr/bin/chromium NODE_PATH=/tmp/chicago-browser-tools/node_modules SMOKE_VIEWPORT=mobile SMOKE_STAGE=1 SMOKE_TIMING=1 node tools/smoke_renderer.mjs --published
```

Receipts and raw stdout/stderr are under `desktop/` and `mobile/`. `GPU-RELEASE.json` records no remaining owned smoke/wrapper or Chromium GPU processes. `ACTUAL-NATIVE-LOCAL-STAGE1-TIMING.json` compares79 exact matching assertions: median native/local elapsed ratio1.102. The prepared local13 wrapper was NOT EXECUTED: this actual speed evidence cannot support completing the long leg inside590s. See `LOCAL13-NOT-EXECUTED.json`.

Full18-leg coverage remains PENDING until hosted desktop13 completes. `EXACT-18-LEG-COVERAGE.json` retains each original source/job/conclusion and replacement. Sixteen original native smoke legs passed on b9c7679; original mobile5 timed out during stalled Ubuntu dependencies before the mirror/app ran, then official mobile5 recovery42764396718 passed30/0 on final merged363236c. Original desktop13 timed out after an actual Full X-RAY triangle RED:3,737,315 above3,675,000. That RED remains preserved verbatim. Root consciously priced the narrow Full active Ghost cap at3,750,000 in af4cc3f with unchanged other budgets and strict actual/public/stat comparisons. Official150m desktop13 recovery42765919955 is pinned to that source and is still executing; no passing verdict is asserted before terminal raw-log verification.

The initial native run itself is not asserted globally PASS: its original baked gate REDs and cancellations remain historical evidence. Source fixes, official rederivations and protected source CI qualify those separately. No model geometry was changed by these reader/consumer reviews or smoke recoveries. The initial preparation statement remains verbatim in `README-PREPARATION.md`.
