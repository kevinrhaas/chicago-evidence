# T-3656 classroom tools — verification checkpoint

Recovery evidence for [chicago PR #2197](https://github.com/kevinrhaas/chicago/pull/2197),
branch `steward/t3656-browser-classroom`. This checkpoint preserves completed work;
**it is not a declaration that the full release gate passed or the PR merged.**

- Original implementation runtime: `6c83e8cf9558c0d6f9ffb422f299764837fc4ed2`.
- Latest code checkpoint: `5034a724d993abe0876a4db7bbfff02d2bb4da0a` (stage 13 expected-budget pin repair).
- Current application runtime remains `ae4e0bdd7368b989dd7569509a6e1d94bf9f6cbc`; the later commits change workflow, tests and documentation files.
- Latest completed focused photo/notebook runtime: `45b35a2c7d910ec1e73f5a60489b1b22c4aff278`.
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
desktop formal smoke failed and reached its cap in
[44372747109](https://github.com/kevinrhaas/chicago/actions/runs/44372747109),
targeting implementation commit 6c83e8cf9. It has 429 passing assertions, one
Full-budget failure, incomplete stage 12, and unrun stages 13–15; there is no
final zero-error or whole-smoke pass. The duplicate full mobile run
[44373274865](https://github.com/kevinrhaas/chicago/actions/runs/44373274865)
was deliberately cancelled; it is not a passing result. The required source CI for the earlier
metadata head cbf3408e is [44375593498](https://github.com/kevinrhaas/chicago/actions/runs/44375593498).
Primary 45b source run 44397687385 failed: partition 1 reached its 600-second
cap and exited 124. Its aggregate failure and the earlier bb593 partition 1
PASS (175 steps, 565.647s) are retained under `gate/`. Neither the timeout nor
the earlier pass establishes latest-head success. Complete required checks are
running for primary 5034a724d: source 44412406486 is pending and moving/upload
44412406478 queued. Old 7019 moving/upload passed and source partitions 2–6
passed, with the rest cancelled; those are historical partial results, not the
latest complete source gate. Consult PR 2197 for current verdicts.

The next browser-only work is checkpointed separately in
[`../t3657-t3658-hunt-accessibility-2026-11-18/`](../t3657-t3658-hunt-accessibility-2026-11-18/).
Its fixtures and photo audit do not extend this PR's full-town release verdict.
The follow-up evidence also preserves newly measured resource regressions and
repairs backed up at `e579424f02287d38639f643b102688ef0846f000`. Those caption/draft
repairs are now integrated into primary 45b; the fresh focused verification
below is separate from the follow-up fixtures.

## Authorized Full-detail budget and incomplete desktop run

`renderer/desktop-6c83-budget-failure-and-cap.log` preserves GitHub run
44372747109 without changing its verdict. It records **429 passing assertions
and one stage 5 failure**: Full detail drew **3,607,087 triangles** at the 1835
West prairie stand, above its 3,605,000 allowance. The 6,813 draw calls remained
within 7,800. The job later hit its 150-minute cap during stage 12; stages 13–15
and the final zero-error verdict did not run. Passing individual assertions do
not make this an aggregate green result.

The owner then authorized “You can raise the budget as appropriate” and “So you
can merge to dev.” Commit `ae4e0bdd7368b989dd7569509a6e1d94bf9f6cbc` changes only
the Full triangle allowance from **3,605,000 to 3,630,000**, using the observed
3,607,087 plus the standing 18,059 margin, rounded up to 5,000. Balanced, Light,
draw-call ceilings, shadow rules, reach, inspection allowances and assets retain
their existing policies. The committed rationale is preserved in
`budget/t-3656-full-detail-budget.md`.

`budget/authorized-full-policy.json` matches the immutable ae4e `main.js` hash
and passes nine deliberately invalid policy mutations. This verifies declaration
and selection policy; it is not a renderer or FPS measurement. A fresh stage 5
retry reached its unchanged **595-second command cap**. Its raw log is retained
as `renderer/desktop-5-budget-incomplete-595s.log`: it did not complete the
stand/tier sweep or produce a final SMOKE PASS. Initial scene assertions and its
isolated zero-page-errors line do not make it green. The budget authorization
does not erase the original failure, supply missing tail
coverage, or authorize production promotion.

## CI completion and dependent follow-up checkpoint

`ci-completion/` records commit 7019f986b's bounded **900-second source CI limit**,
with all eight native partitions, assertions and the aggregate gate still
required. Timeouts remain failures. That CI commit did not change foreground
limits; the later owner-authorized local renderer allowance is documented below. The
check-harness log passes **50 tests, zero failures**, including partition refusal
controls, and the workflow-guard log ends `all good`. These are logic/harness
checks, not successful completion of the live release gates.

The follow-up is now [draft PR 2199](https://github.com/kevinrhaas/chicago/pull/2199),
head `6ee1a689077839dd9923edbc80269dd2cbaccfb6`, targeting dev and depending on
PR 2197. Its bounded preflight passed source **partition 1 of 16 only** (89 checks,
26 self-tests), plus changelog and ticket-ID metadata. The wrapper's standard
“CI has nothing left to ask” banner is broader than that partitioned command;
the remaining 15 partitions and release gates remain required. No browser ran
in that preflight. The precise logs/manifest are in the follow-up evidence folder.

Neither PR is merged at this checkpoint. Required gates remain running. Primary
desktop stages 3, 6, 10 and 11 plus mobile stage 1 completed as recorded below.
The corrected desktop stage 13 hit its 2,100-second cap; the subsequent retry
has no archived verdict. Corrected mobile stage 13 passed as recorded below.
`ci-completion/checkpoint.json` supplies the recovery pointers.

## Initial fresh desktop stages 3 and 6

`renderer/current-desktop-3.log` ends SMOKE PASS with **107 passed, zero failed**
in **6m23s** (94 staged assertions and 13 always-on checks).
`renderer/current-desktop-6.log` ends SMOKE PASS with **20 passed, zero failed**
in **6m03s** (7 staged assertions and 13 always-on checks). These sum to 127
passing assertions, including 26 repeated scaffolding checks; they cover those
two stages only. Both include completed suite, zero-page-error and vendor checks.

`renderer/current-local-stage-manifest.json` preserves the operator's snapshot
at 22:11:14 UTC. It identifies primary code head 7019f986b and the ae4e0bdd7
published build, verifies the harness and both main.js hashes, and separately
records the supplied runtime-tree declaration. Its helper does not independently
recompute that entire runtime tree. The snapshot predates stage 10's launch, so
its `not_run` entry is historical. Stage 10 subsequently completed in the next
batch below; this original snapshot is unchanged. The failed/capped stage 5
remains separate.

The coordinator now uses the owner's budget authorization for new local
renderer stages: **1,200 seconds plus a 5-second kill grace**. Stage 3 completed
under the earlier 595-second cap; stage 6 used 1,200 seconds. Unmodified smoke
logs still print their existing 10-minute guidance footer; the recorded launch
commands identify the actual supervisor cap. Source preflight remains capped at
595 seconds. No timeout or incomplete stage is converted into a pass.

## Additional completed stages and stage 13 pin repair

The next completed local batch is archived under `renderer/`:

| Stage | Passed / failed | Time | Staged / repeated scaffolding |
| --- | --- | --- | --- |
| Desktop 10 | 31 / 0 | 6m54s | 18 / 13 |
| Desktop 11 | 21 / 0 | 6m19s | 8 / 13 |
| Mobile 1 | 95 / 0 | 2m51s | 82 / 13 |

Each log ends SMOKE PASS after suite completion, zero-page-error and vendor
checks. `local-stages-before-stage13-pin.json` records all five completed local
stages (desktop 3/6/10/11 and mobile 1): **274 passing assertions**, including
**65 repeated scaffolding assertions** and 209 staged checks. Their harness is
`285a38d2…` at primary 7019f986b and application runtime ae4e0bdd. They are a
partial cohort, not a complete renderer gate.

Remote desktop stage 13 in run 44403522127 completed **155 passed, two failed**
in **27m58s**, with zero page errors. Both failures expected the old ordinary
Full pin after returning from Ghost to Normal; the actual private/public budget
was the authorized **3,630,000**. The unmodified failed log is
`renderer/desktop13-ae4e-stale-full-pin-failure.log`. A completed failed run is
not relabeled green because its defect was subsequently understood.

Commit **5034a724d** repairs the exact expected Full value in the stage 13 smoke
predicate and its pure policy test, preserving Ghost and lower-tier limits and
adding stale/inflated/public-stat divergence controls. `renderer/stage13-pin-repair/`
contains the coordinator proof, nine passing policy/transition tests, the nine
full-policy negative controls, measured no-write isolation, isolation audit, and
smoke contract checks. The archive independently verified both immutable smoke
hashes and proved the complete smoke file differs only by the one Full value and
its explanatory comment. The only other changed paths are the pure test and
budget documentation; application, assets, data, generators and publisher are
unchanged.

The corrected smoke hash is `eeebfe0a…`. These byte checks preserve the precise
scope of unaffected completed stages; they do not supply a fresh stage 13 result.
The first corrected desktop attempt ran under **2,100 seconds plus a 5-second
kill grace** and subsequently timed out; the later result and passing corrected
mobile run are recorded below. Other renderer stages use 1,200+5 and source
preflight remains 595 seconds. Neither PR is merged and no latest aggregate
release pass is claimed.

## Completed remote desktop batch and corrected stage 13 outcomes

The five remote primary runs on 7019f986b have complete SMOKE PASS summaries:

| Desktop stage | Run | Passed / failed | Time |
| --- | --- | --- | --- |
| 1 | 44405488812 | 95 / 0 | 7m22s |
| 2 | 44405493821 | 115 / 0 | 14m57s |
| 4 | 44405500148 | 42 / 0 | 10m48s |
| 7 | 44405506091 | 39 / 0 | 20m33s |
| 8 | 44405511403 | 22 / 0 | 10m16s |

Their raw logs are `renderer/remote-7019-desktop-*.log`: 313 passing assertions,
including 65 repeated scaffolding checks and 248 staged assertions. These use
the earlier smoke harness; the exact stage-13-only repair proof above preserves
the scope of their unchanged assertions. They do not certify stage 13 or the
whole renderer release gate.

`renderer/corrected-desktop13-2100s-incomplete.log` records **153 printed passes
and one suite-completion failure** when the corrected run reached its 2,100s cap
during the final What's New revisit. Both repaired ordinary-budget assertions
passed. The partial zero-page-errors line does not supply the missing vendor
checks, completed suite, or final SMOKE PASS. This run remains **incomplete**.
The next desktop retry uses 2,700 seconds plus five seconds kill grace and
`SMOKE_TIMING=1`, with unchanged application/harness assertions; no result from
that retry is included here and its active log is not copied.

Corrected **mobile stage 13 completed 157 passed, zero failed in 12m24s** while
this checkpoint was being prepared. `renderer/corrected-mobile13-pass.log`
includes the final returning-visitor check, suite completion, zero page errors,
both vendor checks and SMOKE PASS. Its hash matches the completed record in
`renderer/local-cohorts-after-desktop13-cap.json` (23:21:38 UTC), and that record
confirms the process ended. It uses corrected harness `eeebfe0a…` on primary
5034a724d. This is distinct from the desktop timeout and the older 6c83 mobile run.

Current completed receipts cover desktop **1/2/3/4/6/7/8/10/11** and mobile
**1/13**, totaling **744 passing assertions**: 601 staged assertions and 143
repeated scaffolding checks. The manifest preserves the earlier local cohort,
the corrected cohort, and incomplete attempts separately. Historical full-mobile
6c83 evidence and failed/capped attempts are excluded from this total. Missing
stages remain required; this is not a complete renderer verdict.

Primary mobile stages 2–12 and 14–15 are queued in run **44418522036** on 5034.
Current source **44412406486** and moving/upload **44412406478** remain required.
Old source 7019 and obsolete mobile 13 runs were cancelled, not passed. The
follow-up QA backup `qa/t3657-t3658-parent-pin` is pushed at **b501bfcbc**, with
conditional desktop 5/13 runs **44415899803 / 44415925432** queued. Its provenance
is preserved in the follow-up evidence folder; neither real PR head changed.

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
