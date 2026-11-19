# Final renderer coverage for af, with original attribution

All desktop and phone stage ranges have passing evidence applicable under
the linked dependency reviews. Fresh exact-af stages 13–15 passed at both
widths. Earlier desktop results remain historical DDC/b501 measurements;
phone stages 1–12 remain frozen 347 runs. No single full-range run is claimed.

## Desktop 1280×800

| Stages | Original head | Passed / failed | Staged | Always-on in this run | Run / complete raw log |
| --- | --- | ---: | ---: | ---: | --- |
| 1-4 | `ddc786069` | 320 / 0 | 307 | 13 | [44426888539](../../../t3657-t3658-hunt-accessibility-2026-11-18/current-dev-keyboard/renderer/desktop1-4-pass.log) |
| 5 | `b501bfcbc` | 30 / 0 | 17 | 13 | [44415899803](../../../t3657-t3658-hunt-accessibility-2026-11-18/parent-pin-validation/desktop5-pass.log) |
| 6-12 | `ddc786069` | 111 / 0 | 98 | 13 | [44426953188](../../../t3657-t3658-hunt-accessibility-2026-11-18/current-dev-keyboard/renderer/desktop6-12-pass.log) |
| 13-15 | `af466d163` | 314 / 0 | 301 | 13 | [44446945583](../../../t3656-browser-classroom-2026-11-18/renderer/af-desktop13-15-complete/desktop13-15-pass.log) |

DDC early ranges retain their exercised dependencies under the
[347 scope review](../../../t3657-t3658-hunt-accessibility-2026-11-18/desktop-early-stage-scope-347/README.md).
Stage 5 retains the narrower [b501 geometry/detail-policy evidence](../../../t3657-t3658-hunt-accessibility-2026-11-18/current-dev-keyboard/stage5-reuse.json):
unchanged 1835 stand functions, API-driven assertions and 1,528 indexed asset
variants. It is not a fresh af measurement or proof of changed keyboard
ownership. Its 13 common guards remain attributed to b501, while the fresh
af range has its own complete boot/error/vendor guards.

## Phone 390×780

| Stages | Original head | Passed / failed | Staged | Always-on | Completion |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | `3472ec872` | 95 / 0 | 82 | 13 | Accepted recovered kernel exit 0; normal supervisor end receipt remains unavailable |
| 2–12 | `3472ec872` | 490 / 0 | 347 | 143 | Eleven normal child exit 0 receipts and complete guards / unchanged pins |
| 13–15 | `af466d163` | 314 / 0 | 301 | 13 | Complete current remote range with all terminal guards |

The [local map](../347-mobile1-12-complete/verification.json) binds every
1–12 raw log and receipt. [Fresh af phone verification](../af-mobile13-15-complete/verification.json)
binds run 44446951072. Recovery limitations and repeated guard counts are
preserved; the table is not a unique-assertion count or a single run.

## Applicability and remaining release gates

[The af fold proof](../../combined-347-c23-20261119/folded-af/verification.json)
limits af versus 347 to deleting the upstream T3562 pending entry and folding
its changelog. The affected 13–15 range ran freshly on af. Latest observed
DEV8c retains identical 4D and workflow trees; its copied pre-fire/root-media
publication delta has [executed targeted candidate 539f09 proof](../../dev8c-publication-complete/README.md),
with unchanged budgets, 0 errors and 340 warnings. This is not an executed
full source or renderer rerun on 539f09.

All eight af source partitions passed 1,397 steps, but the separate aggregate
job remains queued at the coordinator snapshot. The original moving-frame
failure (33.1 ms against 32 ms) remains real; its one unchanged retry is active
without terminal credit here. Upload 32 is the original success carried forward.
No overall release pass, deployment or DEV merge is claimed. Release_checks
owns final gate and expected-head / current-DEV review before merging PR2197.

matrix.json provides complete raw-log and scope-proof paths and SHA256 values.
No application mutation, publisher, browser or new test was run for this archive.
