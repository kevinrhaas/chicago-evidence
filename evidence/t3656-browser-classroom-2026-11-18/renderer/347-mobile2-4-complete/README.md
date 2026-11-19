# Frozen 347 mobile stages 2–4 complete

**Stages 2–4 passed 267/0 checks**: 228 staged checks and 39 repeated
always-on checks. Each has a normal durable exit0/end receipt, complete suite,
zero page errors, both vendor guards, terminal SMOKE PASS, unchanged post-run
input checks and no renderer remaining after its stage.

| Stage | Pass/fail | Staged + always-on | Actual process seconds |
|---|---|---|---|
| 2 | 115/0 | 102 + 13 | 244.706 |
| 3 | 107/0 | 94 + 13 | 212.986 |
| 4 | 45/0 | 32 + 13 | 236.997 |

These results use frozen `3472ec872d00e33761490b0138b23da1c63daee2`,
build2026-11-19T02:43:30Z, under the separate2–12 supervisor235873. The current
release head af has only the separately recorded changelog fold; results here
retain347 attribution. They are not a complete mobile or release gate.

The [separate recovered stage1](../347-mobile1-recovered/README.md) remains
95/0 with accepted saved kernel exit0 and unchanged full mirror rehash, while
its original supervisor SIGKILL and unavailable normal end receipt remain
explicit. Its artifacts, runner/config/launch and inventory are reused through
verified exact-byte references in `verification.json`, without duplicate copies
or silently importing stage1 into this normal2–12 cohort.

`manifest-running-snapshot.json` and `events-running-snapshot.ndjson` are dated
partial snapshots: only2–4 are credited and stage5 was running. The active
stage5 log was neither read nor copied. Stages5–12 and the whole-cohort final
content rehash remain pending. The handoff's PID/status observations are dated,
not evergreen. Preserve the running supervisor and frozen publication; inspect
current state before any recovery action.

The new supervisor verifies an initial full-content inventory and unchanged
file-set/stat metadata before/after each stage. That inventory exactly matches
the earlier archived file. This checkpoint does not claim another full-content
rehash after stage4. Remote13–15 at both widths and source/moving/upload remain
separate required evidence. No browser, source test, publisher, application,
ticket or application-ref change was performed while archiving.
