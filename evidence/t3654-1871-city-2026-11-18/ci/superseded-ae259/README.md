# Superseded ae259 legacy-browser batch

All twelve original groups are accounted for in the immutable final ledger and cancellation metadata: **four historical successes and eight cancellations**. These runs tested `ae259f9a5ddd4e79e1c82cd40e5084d6dcf42290`. Necessary source-catalog and benchmark repairs changed smoke inputs, so every group has `coverage_credit: false` for the repaired tree. Cancellation is not an assertion failure.

| Run | Mobile stages | Passed checks | Failures / page errors | Harness duration |
| --- | --- | ---: | --- | --- |
| 44375691729 | 1–4 | 323 | 0 / 0 | 563 s |
| 44375714232 | 5–8 | 76 | 0 / 0 | 1186 s |
| 44375735410 | 9–12 | 69 | 0 / 0 | 714 s |
| 44375760118 | 13 | 157 | 0 / 0 | 702 s |

Each successful group's actual completed log, completion metadata and final supersession metadata are retained. The remaining eight group IDs and final cancelled statuses are retained in `final-ledger.json` and `final-cancel-status.json`. No old run was inserted into the repaired root's dev-smoke-state receipts. A fresh complete source gate must pass before a new frozen-commit legacy batch is dispatched.
