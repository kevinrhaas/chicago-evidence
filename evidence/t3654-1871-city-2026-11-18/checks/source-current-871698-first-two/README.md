# Current local source parts 1 and 2

These immutable bundles test clean source commit `871698ae94659100fcb8894f4967d4b15c62150f`, using the same 1,379-declaration source harness. They retain the exact wrapper, transcript, per-check timings, process result, receipt and original bundle manifest for each invocation.

| Partition | Checks | Self-tests | Exit | Wall seconds |
| --- | ---: | ---: | ---: | ---: |
| 1/32 | 46 | 15 | 0 | 180.559 |
| 17/32 | 46 | 13 | 0 | 211.089 |
| 2/16 | 90 | 22 | 0 | 450.358 |

Each duration comes from nanosecond timestamps written immediately before and after the foreground timeout subprocess. The logs end with matching terminal PASS results; source HEAD, tree cleanliness and harness hashes remained unchanged. The wrappers retain their original absolute paths and source `/tmp/t3654-runtime.sh`; they are executed-procedure evidence, not standalone portable launch scripts.

`first-part-union.json` binds the two 32-way receipts and proves their union equals the original 1/16 selection: 89 unique declarations. Only the three required prerequisites (ordinals 319, 320 and 321) repeat; no ordinary declaration overlaps. No assertions or workflow schedule changed for this split.

The dated [coverage receipt](../../resumption/local-source-coverage-20261118T225759-871698.json) and its [frozen selection](../../resumption/source-current-completed-601-871698.json) accept eight completed current-head receipts: these three runs, recovered 6/16, and 13–16/16. They credit 601 ordinary declarations, with 775 missing and no duplicate ordinary coverage. The three every-part prerequisites are counted separately. Recovered 6/16 retains its kernel-derived exit and approximate timing qualification in its original evidence.

This is partial local source coverage. The active 3/16 run and mutable summaries are excluded. Hosted source status is independent: the last frozen guard verifies parts 4 and 7 of 8, preserves the original part 6 timeout and leaves five pending. No new completed hosted result was available for this update; no retry or fresh legacy dispatch is claimed.
