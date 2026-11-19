# Recovered frozen 347 mobile stage 1

**Stage 1 passed 95/0 checks**: 82 staged checks plus 13 always-on checks,
with suite completion, zero page errors, both vendor guards and final SMOKE
PASS. The harness reports 3m23s. Runtime/publication is frozen
`3472ec872d00e33761490b0138b23da1c63daee2`, build 2026-11-19T02:43:30Z.
This is one stage, not the complete mobile or release gate.

The normal Python supervisor was SIGKILLed before it could write its end
receipt. Original `manifest.json` and `events.ndjson` remain untouched and
still show stage 1 running/start only. The separately labeled recovery receipt
records the exact timeout PID 234227 as a zombie with kernel exit 0, matches
the durable spawn PID and start time within 0.028966 seconds, and records a
full unchanged mirror content rehash. The coordinator explicitly accepted
this recovered result. It does not invent normal supervisor completion or an
exact process end timestamp, and stage 1 was not rerun.

The receipt SHA-256 is
`221b718ca6898cee7b502c3831d3dbd908c97c61e6a529bc265b03548c8fe467`.
The archive independently checks raw kernel fields, durable identity, original
manifest/events/log/inventory hashes, all 95 printed passes, final guards and
immutable source hashes. The saved inventory contains 7,667 files / 515,543,560 bytes;
its canonical digest matches both original and recovered records. The archive
did not rehash the live mirror or run any browser/source tests.

`runner-preparation/` saves v1 and v2, their diff, preparation-only parser and
lifecycle checks, the tiny own-session launch test, and the new 2–12 config and
launch receipt. V2 only adds validated contiguous-stage selection and its
scope metadata/loop. The launcher uses `start_new_session=True`; its recorded
PID, process group and session are 235873. This separate 2–12 cohort is only
**prepared/started** in this checkpoint. No active log, event stream, manifest
or inventory from that cohort was copied, and no older result is imported.
The owner's README retains its historical preparation preamble; its later
recovery section and this index describe the actual launch.

The current release head af466d differs from frozen 347 only in the upstream
changelog fold. Fresh 13–15 at both widths and current source/moving/upload
remain required. All earlier cohorts keep their original attribution.
