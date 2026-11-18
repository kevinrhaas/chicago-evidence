# T-3656 classroom tools — verification checkpoint

Recovery evidence for [chicago PR #2197](https://github.com/kevinrhaas/chicago/pull/2197),
branch `steward/t3656-browser-classroom`. This checkpoint preserves completed work;
**it is not a declaration that the full release gate passed or the PR merged.**

- Original implementation runtime: `6c83e8cf9558c0d6f9ffb422f299764837fc4ed2`.
- Latest tested code/runtime checkpoint: `45b35a2c7d910ec1e73f5a60489b1b22c4aff278`.
  This revision adds bounded caption fitting, notebook draft pruning, a
  person-row alias repair, and on-mount classroom styles. Fresh actual-town
  photo/notebook/link flows passed at both sizes on these exact bytes. Earlier
  formal mobile results remain scoped to the original runtime; they are not
  silently extended to the repairs. `recovery-checkpoint.json` records this
  distinction and the remaining release checks.
- Base dev: `169af6421e2b9af10b98970cced2988fe2383b25`.
- Ticket: `T-3656`, in `kevinrhaas/chicago-tickets`, state `review` with PR 2197.
- Current progress and remaining actions are tracked on that PR and ticket.

## Completed formal checks in this checkpoint

`gate/part1of8.log` through `part7of8.log` end with CHECK PASS:
175, 174, 174, 174, 175, 174, and 174 steps respectively. The source gate is green only when **all
eight partitions** pass. `preflight-part1of8.log` also records the PR changelog
and ticket-ID checks; it ran with `CHECK_PART=1/8`, so its PREFLIGHT PASS is not
a claim that partitions 2–8 ran inside that command.

Source partition 3's initial dead-ticket-pin failure came from a local checkout
layout: the app's `tickets/` was a symlink, which the Python recursive walk did
not traverse. The real tickets clone was moved to the normal app location and
the outside alias points back to it. The targeted roof-pin check and then the
entire partition passed without changing application code or gate assertions.

`gate/ci-part6-step-isolation-failure.log` preserves a historical CI failure:
the four newly added logic tests had no measured rows in `step_isolation.json`.
Commit `03ecd9678e15988abe44c50e27c2bd9fec569530` adds those measured rows;
the later local partition 6 passed. This does not declare the latest exact-head
CI green.

`gate/part7-tour-source-span-failure.log` preserves partition 7's tour-order
failure. The old assertion searched a source-text span rather than mounting the
Guide. Commit `bb59311bf` replaces that assertion with a check that the original
tour element leads the actual mounted Guide's controls and hosted sections.
Focused tour/Guide checks passed, and `gate/tour-order-negative-checks.json`
records both deliberately moved and omitted tour mutations being rejected.
Application code and the intended ordering are unchanged. The complete
partition 7 rerun now passes all 174 steps in `gate/part7of8.log`; the historical
failure is retained separately and is never relabeled green.

`gate/part8-dataset-failure.log` and `gate/ci-bb59311bf-part8-dataset-failure.log`
preserve local and CI partition 8 failures. The dataset validator reports two
errors: a local person-row alias is interpreted as reading nonexistent
`placement.id`, and four byte-identical year pages have crossed its 64 KB
duplication threshold. Commit `45b35a2c7` repairs the alias and moves photo/notebook
CSS loading to their mounted views. The completed official rerun is preserved
in `gate/part8-resource-runtime-pass.log`: **174 steps, CHECK PASS, 314.004s**.
The published era pages are 65,534 bytes each. The earlier failures are retained.
All eight source partitions now have completed passing receipts across the
implementation and repair checkpoints. This does not mean all partitions were
rerun on 45b or that its exact-head GitHub checks are already green.

`renderer/mobile-1.log` through `mobile-12.log`, plus `mobile-14.log` and `mobile-15.log`, are completed, unmodified official
`tools/smoke_renderer.mjs --published` runs at 390×780, one stage per command.
All fourteen end with SMOKE PASS (764 total assertions including repeated scaffolding;
582 staged assertions and 182 always-on assertions). Stage 14 passed 145 assertions
in 5m11; stage 15 passed 34 assertions in 9m28. `renderer/progress-checkpoint.json`
preserves the stage-by-stage counts, times, hashes, and incomplete stage 13 status.
These completed runs cover the frozen
published mirror identified by `renderer/runtime-manifest.json` at the
original implementation runtime 6c83e8cf9. The mirror was produced by `tools/publish.sh` and then
copied for testing so concurrent source gates could not replace its files.
The earlier publication footer named the parent commit; the manifest hashes
identify the runtime bytes actually tested.

`renderer/mobile-13-ci.log` now supplies the missing stage: GitHub run
`44385930725`, job `135090381320`, completed successfully with **157 passed,
zero failed, SMOKE PASS in 8m28**. Together, these local runs and the CI stage
cover all fifteen mobile stages: 921 assertions including repeated scaffolding
(726 staged assertions and 195 always-on assertions). This is complete mobile
renderer coverage for 6c83e8cf9, not a declaration that the later 45b runtime or
complete desktop release gate passed.

`renderer/mobile-6-contention-failure.log` preserves the original stage 6
failure. A second full-world boot timed out at the unchanged 240-second limit
while source workers and a first software-rendered world occupied the machine.
The quiet retry in `mobile-6.log` passed all 24 assertions, including the second
context's checks, in 5m32. No assertion or timeout was weakened. The failed run
is historical evidence, not an additional green result.

`renderer/mobile-13-incomplete-cap.log` is **not green**. The local stage hit the
595-second command cap (supervisor exit 124) and reported 149 passes plus one
suite-completion failure. No application assertion failed before the cap, but
the What's New reload tail was not verified. The passing assertions in this
incomplete run are not included in the completed-stage total above. No timeout
or assertion was changed to complete it. The unchanged official stage 13 subsequently
passed separately in GitHub run
[44385930725](https://github.com/kevinrhaas/chicago/actions/runs/44385930725),
job `135090381320`, on metadata head `7969031f0` with unchanged runtime.
The local-only `progress-checkpoint.json` intentionally retains its original
incomplete-at-cap record; the later CI success is a separate artifact.

All source partitions now have passing receipts, with partition 8 rerun on 45b.
Formal mobile coverage is complete for the original 6c83 runtime. The complete
desktop formal smoke was last observed active in
[44372747109](https://github.com/kevinrhaas/chicago/actions/runs/44372747109),
targeting implementation commit 6c83e8cf9. The duplicate full mobile run
[44373274865](https://github.com/kevinrhaas/chicago/actions/runs/44373274865)
was deliberately cancelled; it is not a passing result. The required source CI for the earlier
metadata head cbf3408e is [44375593498](https://github.com/kevinrhaas/chicago/actions/runs/44375593498).
Read the PR's exact-head checks for the latest checkpoint. Their final results
must be read separately; this archive does not assume them.

The next browser-only work is checkpointed separately in
[`../t3657-t3658-hunt-accessibility-2026-11-18/`](../t3657-t3658-hunt-accessibility-2026-11-18/).
Its fixtures and photo audit do not extend this PR's full-town release verdict.
The follow-up evidence also preserves newly measured resource regressions and
repairs backed up at `e579424f02287d38639f643b102688ef0846f000`. Those caption/draft
repairs are now integrated into primary 45b; the fresh focused verification
below is separate from the follow-up fixtures.

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

### Completed photo-to-notebook integration on the original 6c83 runtime

`harnesses/final-photo-notebook-smoke.mjs` **passed all five integrated checks
at 390×780 and 1280×800**, each in a separate command with exit 0. No harness,
application, assertion, or timeout changes were needed during either run. Both
reports verify the frozen original 6c83 runtime hashes before launching the browser and
record the exact file hashes they tested. The reports, logs, full PNG exports,
and selected notebook screenshots are in `focused/final-photo-notebook-390/`
and `focused/final-photo-notebook-1280/`.

Each run opened a real 1835 world, selected John S. C. Hogan through the People
search/results UI, saved that record's four canonical citations, captured a
photo with the production shutter and one normal render tick, clicked **Save to
notebook**, edited the photo's note, then navigated the same page to the copied
moment URL. Both retained the photo's ten Sauganash place citations. The checks
confirmed byte-for-byte notebook persistence, unchanged photo/note/citations,
selected-person restoration, the saved jaunt retained but inactive, bounded PNG
and local JPEG sizes, zero page errors/local missing resources, and no overflow.
The image check excludes the stamped footer when testing for nonblank rendered
scene pixels. There are no skipped flows hidden behind a passing label.

| Viewport | PNG dimensions | Notebook JPEG dimensions | Serialized notebook | Serialized photo |
| --- | --- | --- | --- | --- |
| 390×780 | 390×886 | 282×640 | 33,690 characters | 27,211 characters |
| 1280×800 | 1174×840 | 640×458 | 53,734 characters | 47,255 characters |

Each viewport used exactly two sequential boots, one page and world at a time,
with back-forward caching disabled. The phone boots took 42.0 and 42.3 seconds;
desktop took 51.4 and 65.3 seconds while source checks ran separately. Continuous
rendering was paused between interactions and one normal tick produced each
photo. These are functional integration results, not sustained performance or
low-end hardware certification.

For reproduction, run each viewport separately under the existing 595-second
command cap after any official renderer quiet CPU window finishes. The phone
command executed was:

```sh
timeout --signal=TERM --kill-after=5s 595s env \
  QA_WIDTHS=390 QA_OUT=/tmp/t3656-final-photo-notebook-390 \
  /tmp/chicago-check-runtime/node_modules/node/bin/node \
  /tmp/t3656-final-photo-notebook-smoke.mjs \
  > /tmp/t3656-final-photo-notebook-390.log 2>&1
```

The desktop command used width `1280` and its own matching output directory/log.
The unfiltered default runs both sequentially, but separate commands preserve
the per-command budget. This completed original-runtime integration supersedes the
older mixed-run evidence for this specific photo-to-notebook-to-share flow; it
does not replace pending complete source/renderer release gates.

## Completed verification of repaired runtime 45b

After the source partition 8 publisher completed and the coordinator granted a
quiet browser window, its official mirror was copied to a new immutable test
root, `/workspace/chicago-classroom-final-published`. The original frozen root,
manifest and all reports remain unchanged as pre-repair 6c83 evidence.

`harnesses/resource-manifest.py` verified the publication stamp against
`45b35a2c7d910ec1e73f5a60489b1b22c4aff278` and matched **428 authored JS/CSS files**
to that immutable Git commit. `renderer/resource-runtime-manifest.json` records
**432 published hashes** including separately hashed generated entry pages and
the changelog re-export. Both new browser reports verified these hashes before
launching, then recorded them with the exact runtime commit.

`harnesses/resource-photo-notebook-smoke.mjs` passed **all five integrated checks
at 390×780 and 1280×800**, run sequentially, one page/world at a time, each under
the unchanged 595-second command cap. It retained every preceding assertion:
actual People selection and four canonical Hogan citations; an actual production
shutter capture with one normal render tick; actual Save to notebook and note
editing; copied-link navigation with person/view, photo, note and all ten
captured Sauganash citations preserved byte-for-byte; bounded images/storage;
zero page errors/missing local resources and no horizontal overflow. Each
viewport used exactly two boots. No application or harness repair was needed
during these runs.

The additional stylesheet assertions passed at both sizes. Photo and notebook
CSS remained unrequested and absent from the DOM before their views opened;
mounting each view loaded its actual stylesheet with 13 CSS rules and exactly
one link per document. Opening Guide retained one photo stylesheet link.
After shared navigation, the notebook stylesheet loaded once in the new
document. The reports retain the precise requests and sheet URLs.

| Viewport | Boots (seconds) | PNG dimensions | Local JPEG | Notebook / photo characters |
| --- | --- | --- | --- | --- |
| 390×780 | 33.23 / 36.88 | 390×886 | 282×640 | 33,702 / 27,223 |
| 1280×800 | 37.884 / 37.440 | 1174×840 | 640×458 | 53,722 / 47,243 |

Reports, unmodified logs, full PNG exports, and before/after notebook screenshots
are under `focused/resource-photo-notebook-390/` and
`focused/resource-photo-notebook-1280/`. The phone supervisor returned exit 0.
The desktop's original tool return was truncated during context rollover; its
completed all-green report, final PASS log and terminated browser/harness were
verified. A recovered desktop supervisor exit code is not claimed.
`prepared-resource-rerun.json` now records completion and reproduction paths.

The actual phone command was:

```sh
timeout --signal=TERM --kill-after=5s 595s env \
  QA_MANIFEST=/tmp/t3656-resource-renderer-manifest.json \
  QA_ROOT=/workspace/chicago-classroom-final-published \
  QA_WIDTHS=390 QA_OUT=/tmp/t3656-resource-photo-notebook-390 \
  /tmp/chicago-check-runtime/node_modules/node/bin/node \
  /tmp/t3656-resource-photo-notebook-smoke.mjs \
  > /tmp/t3656-resource-photo-notebook-390.log 2>&1
```

The desktop command substituted width `1280` and its matching output paths.
These are actual-town functional checks. Continuous software-GPU drawing is
paused between interactions; the shutter uses one real normal frame. This is
not sustained weak-device performance evidence and does not replace the full
official renderer or latest-head CI gates. Narration uses the same controlled
index helper as the official smoke; audio correctness is outside this flow.

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
