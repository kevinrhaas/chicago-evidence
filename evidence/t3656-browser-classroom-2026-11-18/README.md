# T-3656 classroom tools — verification checkpoint

Recovery evidence for [chicago PR #2197](https://github.com/kevinrhaas/chicago/pull/2197),
branch `steward/t3656-browser-classroom`. This checkpoint preserves completed work;
**it is not a declaration that the full release gate passed or the PR merged.**

- Implementation: `6c83e8cf9558c0d6f9ffb422f299764837fc4ed2`.
- Latest code-repository checkpoint: `7969031f049fb2d54df2ce8a6bccd014c5ea1a1e`.
  It and the previous checkpoint `cbf3408e032eb6341df9d52bfbb289810035f412` change
  only STATUS and the smoke ledger; application/runtime source is identical to
  the implementation commit.
- Base dev: `169af6421e2b9af10b98970cced2988fe2383b25`.
- Ticket: `T-3656`, in `kevinrhaas/chicago-tickets`, state `review` with PR 2197.
- Current progress and remaining actions are tracked on that PR and ticket.

## Completed formal checks in this checkpoint

`gate/part1of8.log` through `part4of8.log` end with CHECK PASS:
175, 174, 174, and 174 steps respectively. The source gate is green only when **all
eight partitions** pass. `preflight-part1of8.log` also records the PR changelog
and ticket-ID checks; it ran with `CHECK_PART=1/8`, so its PREFLIGHT PASS is not
a claim that partitions 2–8 ran inside that command.

Source partition 3's initial dead-ticket-pin failure came from a local checkout
layout: the app's `tickets/` was a symlink, which the Python recursive walk did
not traverse. The real tickets clone was moved to the normal app location and
the outside alias points back to it. The targeted roof-pin check and then the
entire partition passed without changing application code or gate assertions.

`renderer/mobile-1.log` through `mobile-12.log` are completed, unmodified official
`tools/smoke_renderer.mjs --published` runs at 390×780, one stage per command.
All twelve end with SMOKE PASS (585 total assertions including repeated scaffolding;
429 staged assertions and 156 always-on assertions). They cover the frozen
published mirror identified by `renderer/runtime-manifest.json` at the final
implementation runtime. The mirror was produced by `tools/publish.sh` and then
copied for testing so concurrent source gates could not replace its files.
The earlier publication footer named the parent commit; the manifest hashes
identify the runtime bytes actually tested.

`renderer/mobile-6-contention-failure.log` preserves the original stage 6
failure. A second full-world boot timed out at the unchanged 240-second limit
while source workers and a first software-rendered world occupied the machine.
The quiet retry in `mobile-6.log` passed all 24 assertions, including the second
context's checks, in 5m32. No assertion or timeout was weakened. The failed run
is historical evidence, not an additional green result.

At this checkpoint, source partitions 5–8, mobile stages 13–15, and the complete
desktop formal smoke were still pending or running. GitHub full-smoke runs
[44372747109 (desktop)](https://github.com/kevinrhaas/chicago/actions/runs/44372747109)
and [44373274865 (mobile)](https://github.com/kevinrhaas/chicago/actions/runs/44373274865)
target implementation commit 6c83e8cf9. The required source CI for the earlier
metadata head cbf3408e is [44375593498](https://github.com/kevinrhaas/chicago/actions/runs/44375593498).
Read the PR's exact-head checks for the latest checkpoint. Their final results
must be read separately; this archive does not assume them.

## Focused checks and their limits

The reports, selected screenshots, and reproduction harnesses are under
`focused/` and `harnesses/`. They are complementary evidence, not replacements
for the complete official published renderer gate.

- **Photo/source and photo/published:** both reports pass at 390×780 and
  1280×800. They check a nonblank captured town image, bounded PNG dimensions,
  moment URL/arrival state, retained but inactive saved jaunt, no page errors,
  local missing resources, or overflow, and `preserveDrawingBuffer: false`.
  Only published screenshots/exports are copied to avoid duplicate images.
  The harness pauses continuous rendering between interactions, queues the
  production shutter, and executes one actual normal render tick. This checks
  capture correctness; it does **not** establish sustained performance on a
  low-end Chromebook or other weak device.
- **Important photo-run scope correction:** `photoOnly` is true in the saved
  harness. Its report label “shared moment restores and notebook survives page
  navigation” is too broad: notebook persistence was skipped, and the recorded
  notebook is null. These photo reports establish only the moment/jaunt part of
  that label. They do not establish full-town notebook persistence.
- **Photo runtime provenance:** the saved published `tested-files.sha256`
  names `main.js` hash `bcff5a8b…`; final implementation `main.js` is
  `541993c2…`. The photo runs preceded the final review changes. The old bytes
  were reconstructed by reversing those changes, then their SHA-256 was checked
  against the saved photo-run hash before producing
  `photo-tested-to-final-main.diff`. The diff is limited to `jauntDocument`
  reader-text projection and explicit person-selection retention/callbacks and
  precedence. Shutter/render/capture code is unchanged. This is pre-final-review
  focused evidence, not an exact-final-runtime full-town test.
- **Notebook fixture:** `notebook-fixture-smoke/report.json` records six passing
  flows at each size: Guide save form, editing and persistence after reload,
  person-card grade/citation saving, safe standalone HTML download, iframe
  print/cleanup, and visible denied-storage failure. It measures no horizontal
  overflow and dark input contrast 10.62:1. This is the actual persistence
  evidence here, in a browser fixture, not a whole-town run.
- **Lesson fixture:** `lesson-fixture-smoke/report.json` records all ten
  available year/group combinations at both sizes, grade selection, stale
  response rejection, links and print PDF, readable controls, no overflow,
  and zero page errors. One of the equivalent PDF exports is retained.
- **Person selection:** `person-moment-fixture/report.json` checks actual
  People/Inspect views plus extracted production `rememberMomentPerson` and
  `readMoment` bodies for 1812 and 1904. Explicit selection survives Home and
  replaces a previous hidden card in captions and copied URLs. It was run after
  the final person-selection changes; it is still a fixture, not a rendered town.
- **Reflection integration:** `understanding-final-ui.log` records the actual
  completion integration at both sizes: typing, source review, draft retention,
  retry, skip, focus, and no overflow/errors. This is a fixture verdict.

The notebook, lesson, and reflection fixture reports do not embed a precise
tested-tree hash. Their original file timestamps are retained in
`artifact-manifest.json`; do not turn those timestamps into an exact-commit
claim. The formal renderer manifest supplies exact provenance for its own runs.

### Earlier individual flows, preserved with their failures

`focused/historical-mixed-results/classroom-source-final.json` records the
source-town phone notebook save/edit/export/print flow and subsequent shared-link
notebook persistence passing, together with the real-jaunt reflection flow. The
same run failed other checks: it waited for a deliberately hidden lesson print
node to become visible, its photo check failed, and it saw a narration-index 404.
Its desktop boot was interrupted. This is not an aggregate green run.

`focused/historical-mixed-results/classroom-published-final.json` records the
published desktop notebook, lesson/PDF, real-jaunt completion, and final
zero-page-error/local-404/overflow checks passing. Its photo capture timed out and
the subsequent shared-link check had no URL, so those failed. Neither historical
report embeds an exact tested-tree hash. These reports support the individual
flow claims in earlier STATUS prose, not complete release coverage or a
final-runtime photo-to-notebook flow.

### Prepared final photo-to-notebook integration

`harnesses/final-photo-notebook-smoke.mjs` is a new narrow harness prepared and
syntax checked at this checkpoint, **not yet run in a browser**. It first verifies
the frozen runtime file hashes. For each viewport it opens one real 1835 world,
selects John S. C. Hogan through the People search/results UI, saves that record's
canonical citations, captures a photo with the production shutter and one normal
render tick, clicks **Save to notebook**, edits the photo's note, and navigates
the same page to the copied moment URL. It then checks byte-for-byte notebook
persistence, the retained photo/note/citations and selected person, bounded PNG
and local JPEG sizes, zero page errors/local missing resources, and no overflow.
Photo source rows must match the actual captured metadata; an honest empty list
is possible when no place is selected. The person entry must have its real
canonical source IDs. There are no skipped flows hidden behind a passing label.

Run each viewport separately under the existing per-command cap after the
official renderer's quiet CPU window finishes. Example for the phone:

```sh
QA_WIDTHS=390 QA_OUT=/tmp/t3656-final-photo-notebook-390 \
  /tmp/chicago-check-runtime/node_modules/node/bin/node \
  /tmp/t3656-final-photo-notebook-smoke.mjs \
  > /tmp/t3656-final-photo-notebook-390.log 2>&1
```

Use width `1280` and its own output directory/log for desktop. The unfiltered
default runs both sequentially, but could exceed one command's budget. These
commands are reproduction instructions, not records of a completed test.

## Reproduction and integrity

The local gate environment used Node 22.23.5 at
`/tmp/chicago-check-runtime/node_modules/node/bin/node`, Chromium at
`/usr/bin/chromium`, Python validator dependencies, and `bc` under
`/tmp/chicago-check-runtime/bc/usr/bin`. Source partitions used `CHECK_JOBS=3`.
The machine has a four-core CPU quota and software GPU rendering; multiple
simultaneous worlds materially affect boot time. Harnesses retain their original
local paths and require path/dependency setup on a new machine.

`artifact-manifest.json` records SHA-256, size, original path, original modified
time, and scope for every copied artifact. Original logs/reports are preserved;
this README corrects the misleading photo label without rewriting the evidence.
No runtime source, production site, accounts, or server configuration is changed
by this evidence checkpoint.
