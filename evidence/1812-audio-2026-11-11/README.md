# 1812 seasonal audio — T-3551 / PR 1934

Code: https://github.com/kevinrhaas/chicago/pull/1934
Checkpoint: `3df73785f8ba9093ade9d1fed98503cc45ad76dc`.
Source tree: `f22922b9f32b90f800c018045603cc05b752ad68`.
The current code PR head is `c5de44a61e8cd0c254e4d213f5ecd1046cbe4000`; its only change from this application checkpoint is the stage 13 expected Effects help text. `smoke-scope-reuse.json` proves all other tracked source bytes match.

This folder preserves measured browser and release evidence. Automated decoded-signal checks do not constitute physical listening approval.

## Native town evidence

`native/report.json` and its eight wide screenshots cover actual 1812 town behavior at 390px Light and 1280px Full: four seasonal views, dirt/snow hoof contacts, the existing militia worker’s spring repair and August 14 packing tasks, and mute/visibility/presence cleanup. Runtime media comes from the actual R2 URLs. The native helper temporarily holds drawing during data/audio checks to keep software-rendered browser setup responsive; it restores drawing and checks frame progress for screenshots. Day routines, actors and contacts remain native: no invented contact feeds were used. Wide screenshots alone do not establish close hand/tool visual acceptance.

That initial publication was made before the recovery commit: its build stamp names parent `8a643db9e`, while its separately recorded reviewed source tree is `f7a4e1d433f3c824912c09da23944a295f20f115`. Do not treat the parent build stamp as the tested implementation’s commit identity. The final checkpoint subsequently corrected library CSS overflow and moved an unchanged non-human prop out of the strict human-model directory. `library-fix-runtime-equivalence.json` and `prop-path-equivalence.json` bind the unchanged runtime JavaScript/catalog/geometry to those corrections. The final prop publishes at `data/props/work_1812.glb`; its SHA-256 is `64fdcbdffa35e00b0ed4704794993b21ae24286a3947bcb5961cfc1872180e7f` (19,960 bytes).

## Focused and library evidence

- `focused-prop-path.log`: all 52 integrated focused tests pass after the prop path correction.
- `hoof-browser-report.json`: actual hosted recorded media, output-rate handling, voice/decode limits, lifecycle and snow-filter/gain checks.
- `hosted-library-fixed.log` and `library-layout-fixed.json`: hosted media and bounded controls at both widths. `library-layout.json` retains the original phone overflow observation rather than hiding the failure.

## Release status

Release validation is still in progress. Local parts 1 and 2 pass (328 and 329 checks); their full transcripts are preserved as gzip files. Current-head CI gate, moving frames, portable humans and phone stage 13 pass; desktop stage 13 and local parts 3 and 4 remain pending at this evidence checkpoint. Two phone close work views have been accepted, with desktop views still running; the final close-view corpus will be added together. This is not a completed DEV release.

The failed supplemental capture logs preserve setup mistakes and normal native behavior: software drawing delayed UI actions, nearby people automatically reopened Inspect, and the worker naturally left his primary work spot before a later automation command. Actual impacts stopped correctly. The eventual capture observes pixels and pose synchronously after the same native render, closes UI through normal APIs, and still requires manual visual acceptance; it does not force actor positions or phases.
