# Premerge evidence checkpoint — 2026-11-19T04:06:42.978269+00:00

Current af desktop 13–15 completed **314/0**, 301 staged plus 13 always-on
checks, in 69m44s. Exact checkout, normal published build, desktop environment,
full body, zero page errors, both vendor checks and final SMOKE PASS were
independently verified from the complete run 44446945583 log.

The [final renderer matrix](../../renderer/final-af-scoped-coverage/README.md) links both widths and keeps
all groups separate: DDC desktop 1–4 = 320, DDC 6–12 = 111, b501 stage 5 = 30 under
its narrow geometry proof, current af 13–15 = 314; phone recovered 347 stage 1 = 95,
normal 347 stages 2–12 = 490, and current af 13–15 = 314. Exact hashes and reuse
limits are in matrix.json. This completes scoped renderer coverage, not a
single full-range run or an overall release verdict.

All eight source partitions passed 1,397 steps; aggregate job 135327670033
remains queued in the coordinator snapshot. Moving retry is active with no
terminal result here; the original 33.1 ms > 32 ms failure and one-retry limit remain.
Upload 32 is the earlier success carried forward. DEV8c is the latest observed
base; its exact merged 539f09 publication dependency checks are complete.

Release_checks retains ownership of final gate review, fresh PR/DEV head
guards and eventual authorized merge. PR2197 remains draft pending those
requirements; no merge or deployment is claimed. PR2205 remains dependent.
Evidence_checkpoint retains archive ownership. Earlier snapshots and failed
runs stay intact; only the pending desktop-range status is superseded here.
