# Fixed 520-declaration snapshot on 6409

The immutable proof recorded at 00:11:43 UTC on 19 November 2026 accepts current hosted parts 2/8, 5/8 and 6/8 plus the overlapping fresh local 6/16 receipt. It covers exactly 520 of 1,379 declarations: 517 ordinary checks and three prerequisites, with 859 missing. Counts are unions of declaration ordinals, not sums of passing log totals. The local 6/16 checks already fall within hosted 6/8.

| Hosted partition | Checks | Gate wall seconds |
| --- | ---: | ---: |
| 2/8 | 176 | 342.443 |
| 5/8 | 175 | 289.496 |
| 6/8 | 175 | 393.937 |

All bind source `6409dda1222e1284e111ab0efde1c471f3284d60`, tree `eeaaefef97d3275b048f308c57c3df5514dbb028`, base `c676aa2f4ad6ee8cff0521da6ba8add70d55949c` and actual hosted checkout `9aea1d7aa0706146cf93f11ae4983e5f5cc5496d`. The two new logs, completed metadata, timings and dated three-of-eight guard are under `../../ci/current-6409/completed-parts2-5/`; part 6 remains in the earlier archived directory.

The two original manifests and `archive-dependency-map.json` bind 24 unique incremental dependencies, reusing unchanged exact bytes from earlier archive locations. The reviewed verifier, native harness and fresh local6 bundle remain under the previous `source-6409-part6/` map. Historical verifier fixtures are not current execution coverage. No live canonical summary or mutable helper is copied.

The frozen dispatcher and actual authorization-only refusal are under `../../resumption/dispatch-6409-hosted-2-5-6/`: four simulated positive controls, 53 refusal controls, no real dispatches, and no ledger change on the incomplete 520 proof. Full source, browser readiness and merge authorization remain false. This checkpoint stays fixed even if later CI completes.
