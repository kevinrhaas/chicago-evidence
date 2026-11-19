# Dated partial source coverage on 6409

This snapshot binds source `6409dda1222e1284e111ab0efde1c471f3284d60`, tree `eeaaefef97d3275b048f308c57c3df5514dbb028`, and dev base `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`. The new binding starts empty: no historical execution coverage, timeout exclusion or recovered-exit exception is inherited.

The frozen empty report covers zero declarations. The subsequent frozen report covers 175 of 1,379 declarations: 172 ordinary checks plus three required prerequisites, with 1,204 declarations missing. It accepts only the fresh local 6/16 and hosted 6/8 receipts; their overlap is credited once. Full source coverage, browser readiness and merge authorization remain false.

| Completed invocation | Checks | Self-tests | Process result | Wall seconds |
| --- | ---: | ---: | ---: | ---: |
| Local 6/16 | 89 | 18 | Exit 0 | 466.796 |
| Hosted 6/8 | 175 | See raw log | Successful job / terminal PASS | 393.937 |

The local bundle retains its original nanosecond process receipt, wrapper, new controller, raw log and timings; readers and base requirements were enabled. Its frozen ledger has no imported old receipts. Local 14/16 was not started because the completed hosted 6/8 already covers that selection.

The completed hosted job ran actual checkout `9aea1d7aa0706146cf93f11ae4983e5f5cc5496d`, whose parents are c676aa and 6409 and whose tree equals the source tree. Exact checkout API metadata, tree comparison, timing and completed log are under `../../ci/current-6409/completed-part6/`. Only one of eight hosted parts is verified in the dated guard.

`source-original-manifest.json` and `dispatch-original-manifest.json` retain the two immutable closures. `archive-dependency-map.json` maps all 31 unique dependencies to their archived bytes. The reviewed verifier has the same SHA256 as the earlier reviewed version; its 30 historical fixture controls remain historical evidence. Current empty and partial audit results are included here. The separately frozen dispatcher has four simulated positive and 53 refusal controls, plus an actual authorization-only refusal on this incomplete proof with no dispatch or ledger mutation. See `../../resumption/dispatch-6409-part6/`.

These helpers retain their execution paths and are not instructions to replay queued jobs. No verifier, dispatcher or browser was run while creating this archive. The original full historical 871698 union remains separate and supplies no current-head coverage.
