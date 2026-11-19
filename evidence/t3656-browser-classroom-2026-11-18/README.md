# T-3656 classroom tools — verification checkpoint

Recovery evidence for [chicago PR #2197](https://github.com/kevinrhaas/chicago/pull/2197),
branch `steward/t3656-browser-classroom`. This checkpoint preserves completed work;
**it is not a declaration that the full release gate passed or the PR merged.**

- Original implementation runtime: `6c83e8cf9558c0d6f9ffb422f299764837fc4ed2`.
- Latest remote combined checkpoint: `edc7099032cd6d55d7a7e7f0d66d313b15960f10` (all three tickets in PR2197, folded DEVd47 integrated; final gates pending).
- The completed local desktop 13 retry passed on frozen code `5034a724d993abe0876a4db7bbfff02d2bb4da0a` / published build `ae4e0bdd7`. It does not test b1's changed upstream inputs.
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

## Combined single-PR delivery on folded DEV d47

All three tickets now deliver together through **PR2197**, branch
`steward/t3656-browser-classroom`, at **edc7099032cd6d55d7a7e7f0d66d313b15960f10**,
tree **b9c9b74ecb9f98869ff6a46a4d56a1993db25dd8**, parents **ddc786069** and
folded DEV **d47d9550**. The independent Git checks in
`combined-edc-d47-20261119/verification.json` bind the preparation record to
this pushed commit: incoming DEV paths and shipped changelog are preserved,
the renderer differs from ddc only in the folded changelog, the smoke harness
is identical, and the focused XR checker is included exactly. One pending
`T-3656.json` entry describes the combined delivery; `T-3657.json` is removed.

Ticket checkpoint **5206e4c9e38126fadb4db9fc872712c829615af7** keeps all three
in review, points each to2197, and records their shared group. The former
parent-first/rebase plan is superseded. PR2199 is superseded; its closure is
owned by the coordinator and is not claimed by this archive. No PR has merged.

The bundle preserves official measurement of the incoming unique-ID validator
and the combined isolation audit (1068 measured tools,1337 keyed steps).
The follow-up evidence folder contains the test-only fd27937a XR repair:
20 focused checks, keyboard regression and measured zero writes. Its empty
quiet audit log has an explicit exit0 receipt; silence alone is not counted.
The active part7 repair rerun was excluded.

The completed frozen ddc source sequence is preserved as **parts1–6 PASS,
part7 FAIL1/174, part8/preflight UNRUN**. The original failure was a stale XR
capture-shape assertion; the focused repair is not a full combined gate.
Its original part1 shell-exit receipt remains lost. Ddc desktop6–12 completed
**111/0 in82m18s**,98 staged checks plus13 always-on checks once. Ddc desktop
13–15 completed **308/2 in50m39s**: Space did not inspect, and transfer texture
blob errors failed the zero-page-error assertion. That failed run remains red;
neither consolidation nor focused source tests silently resolve it.

The b1/c676 source baseline now has **all8 native partitions and the aggregate
job successful**,1394 steps. Its overall workflow conclusion is **CANCELLED**
after the edc update, so it is not labeled overall workflow success. The final
API receipt and aggregate log are under `ci/source-44422645793/`. All b1/ddc
baseline results retain their original inputs. Current combined source run
**44442868750**, preflight/moving/upload and fresh official13–15 at both widths
remain required. This checkpoint is not merge approval. Earlier sections are
historical candidate and delivery plans.

## Earlier DEV advance to 21f checkpoint

DEV advanced from c676 to **21f609244a4a54135e0d3657bf0d1fff44ee30c7** with
T-3635's 2027 Prairie integration. **Primary b1 is not merge-ready against this
new DEV.** Its complete scoped renderer coverage, moving/upload results and
source receipts remain attributable to frozen b1/c676. The follow-up ddc source
gate remains frozen on c676 in its isolated worktree and was not disturbed.

`dev-21f-20261119/` preserves the dated API receipt, input provenance and read-only
coverage review. All 25 incoming paths were independently checked as the old
blob/absence in both b1 and ddc; this verifies their current inputs, not a
merged candidate. The incoming renderer subtree is unchanged, but the 1904
villa model and yard/door/inside inputs, global liberty collection, source
counts/detail edges, jaunt opening and unique-ID validator change. Those
inputs cannot inherit a whole-scene pass by source-code similarity alone.

After incorporating the **actual latest folded DEV**, complete the current
source/metadata gates and rerun unchanged official **13–15 on both desktop and
mobile** for every final runtime being released. The review supports scoped
retention of 1–12, with explicit hidden-prose, count, source-detail and route
limits; it does not certify a future merge or weaken any assertion. The pending
release fragment at 21f is not yet the final folded changelog.

The saved source attempt2 baseline now has parts **1, 2, 3, 4, 5, 6, 7, 8**
completed (1394 steps); pending parts are **none**.
Aggregate success observed in this snapshot: **no**. The separate aggregate
job135281050097 was queued at02:00UTC; all eight partition successes do not
invent an aggregate verdict.
Logs preserve actual checkout cda72 into c676 and never overwrite attempt1.
`premerge-b1-c676/` contains only two metadata portions: changelog-entry passed,
and the ticket-ID check explicitly returned not-applicable because tickets are
a separate repository. Both exited 0; this is not complete preflight or 21f
validation. Earlier sections and the coverage matrix remain historical
b1/c676 records, not current-DEV merge approval.

## Earlier completed b1 phone cohort and source rerun attempts

The [consolidated primary coverage matrix](primary-coverage-matrix.md) links every retained and fresh renderer log to its full SHA-256 record, with the scoped DEV-input review and remaining source requirements.
The [independent reuse review](coverage-review/independent-review-20261119.md) is preserved separately as a read-only consumer/input audit, with its explicit coverage limits and no new test execution.

All **b1 mobile stages 2–15 passed 826/0 checks**, comprising 644 staged checks
and 182 repeated scaffolding checks. Summed reported runtime was **69m25s** in
the software-rendered test environment; this is not a device benchmark.
`renderer/b1-mobile-complete/` preserves the immutable final manifest, operator
digest and completed 13–15 logs. Its verification references the unchanged
2–12 logs in their earlier folder rather than duplicating them. All fourteen
log hashes, final summaries and suite/page/vendor guards were checked. The
manifest SHA-256 is
`e111d4b45f6ac9798345299f26ed926f39d8577b046caaf0ab674b1484dd4610`;
the digest SHA-256 is
`105c3879f6db1d2372204330879a896c2ad563d6cec66be8fc80d1a7974b9a85`.
Stage2's original shell-exit receipt remains lost; complete final PASS and all
guards establish its recorded completion without inventing an exit code.
Stages3–15 have operator-recorded exit0. Mobile1 retains its separately reviewed
earlier evidence; it is not counted or relabeled as a fresh b1 execution here.
The historical frozen 5034/ae4 manifest remains unchanged.

Source run **44422645793** was refreshed **once** on unchanged b1 / PR merge
**cda72c805** / dev **c676** inputs. `ci/source-44422645793/` preserves the pre,
cancel and rerun receipts plus separate attempt records. Attempt1 retained
**part2 PASS174** while the other seven jobs were cancelled wholly queued. The
existing part2 log is referenced with its verified hash and explicit attempt1
source alias; it is never overwritten or counted as an attempt2 pass. Attempt2
now has **part4 PASS174**, completed at01:24:54UTC. Its other seven parts,
including part2, and aggregate remain required. There is no complete source
gate success in this checkpoint. Prior moving/upload success remains separately
scoped to the same actual PR merge.

The follow-up ddc desktop **1–4 group passed320/0 in38m29s**, including307 staged
checks across the group and13 always-on checks counted once. Its exact environment,
published checkout and final suite/page/vendor guards are archived in the
follow-up folder. Other remote groups remain in progress at this dated snapshot;
the isolated local combined source gate is separate and no partial output was
copied. Current **b1 desktop13–15 also completed310/0 in54m06s** at01:27:36UTC,
with297 staged checks across the range and13 always-on checks once. Its raw
published log and exact environment/final-guard verification are in
`renderer/b1-desktop-13-15/`; earlier desktop1–12 retain their separate reviewed
behavioral applicability and original attribution. Required source checks
remain pending; no whole release gate or PR merge is declared. Earlier sections retain their
original checkpoint context.

## Earlier b1 mobile 2–12 and merge CI checkpoint

At this dated **2026-11-19 00:54 UTC** checkpoint, local b1 mobile stages **2–12
passed 490/0 checks**: 347 staged checks and 143 repeated scaffolding checks.
`renderer/b1-mobile-2-12/` preserves the eleven complete raw logs, original
00:50:59 manifest and per-stage verification. Every log has final SMOKE PASS,
completed suite, zero page-error and both vendor guards; hashes match the
manifest. Stage 2's shell exit receipt was lost across the workspace restart,
so no exit code is invented. Stages 3–12 have operator-reported exit 0. The
manifest predates stage 13's launch; **stage 13 was active at the later checkpoint
and its raw log was neither read nor copied**. Stages 13–15 remain uncredited.
These runs use published b1, build 2026-11-19T00:01:25Z, and retain their own
source/runtime/harness provenance independently from earlier passing cohorts.

CI run **44422645797** completed both moving frames and upload-release
successfully; upload-release passed **32 checks**. Source run **44422645793**
partition **2/8 passed 174 steps**; the other seven partitions and aggregate
remain pending. All three completed logs explicitly checked out PR merge
**cda72c80519f5478380dd44b67615e2f97142dd5**, merging workflow head b1 into dev
c676. `ci/checkpoint-20261119-0054/` preserves their logs and dated monitor,
recovery, runner-label and DEV receipts. DEV remained c676 at **00:54:20 UTC**;
runner labels were observed earlier at **00:08:28 UTC**. These snapshots are not
evergreen queue or branch claims. Current b1 desktop 13–15 was still running.

The ddc follow-up's renderer groups have now been dispatched: desktop 1–4 and
6–12 were running; desktop 13–15 and mobile 1–15 were queued. No completed ddc
group is claimed here. The follow-up folder records original dispatch times and
the later status snapshot separately. Ticket recovery checkpoint
**49b415cf73d188c807c13a77da77b9930330488e** is pushed. Full required gates remain
incomplete and neither PR is declared merged. Earlier sections below retain
their historical checkpoint context.

## Earlier completed retry, keyboard backup and publication

The corrected frozen **5034/ae4 desktop 13 retry passed 157/0 in 35m34s** under
the authorized 2,700-second command allowance, with completed suite, zero page
errors and vendor checks. `renderer/corrected-desktop13-2700s-pass.log` preserves
the full timed log. Its printed standard ten-minute steward guidance is the
harness footer; the actual command allowance is recorded in the frozen manifest.
The earlier 2,100-second incomplete attempt remains separate and is not green.
`renderer/local-stages-5034-complete.json` has SHA-256
`d65790467cb783f5f23761da4d768ba94164be31f03e5fec1e76abbec1dd2eb8`.
It records seven completed local stages, 588 assertions including 91 repeated
scaffolding checks, with explicit pre-pin and corrected-harness cohorts. It
declares **full_renderer_gate: false**; this is not latest b1 aggregate coverage.

The official b1 publication is now complete, build **2026-11-19T00:01:25Z**.
`publication-b1/` records the publisher log, build stamp, saved monitor/recovery
snapshots and verification. The published main.js independently matches b1's
immutable Git source; the unchanged harness SHA is also verified. The reported
smoke-tree prefix `6a914d94e3eb1159` is attributed to the coordinator, not
independently recomputed here. Local b1 mobile validation is in progress; **no
active mobile log was copied**. Remote mobile run **44422910837** was cancelled
while wholly queued and supplies no executed coverage. Source **44422645793**,
moving/upload **44422645797**, and desktop 13–15 **44422884843** remain required;
their current completion is not established by this archive.

The follow-up folder now separately preserves the historical **b501 QA desktop
13 PASS157/0 in 27m47s**, a **20-check keyboard DOM/browser fixture** at 3131/597,
and the pushed normalized QA **ddc78606998ea8aee589941c6ab6cae76a80440a**. These
have separate runtime scopes. ddc's parent is b1 and all 46 current-dev changed
blobs are preserved; no full combined renderer success is claimed. Neither PR
has merged. The following sections retain earlier checkpoint context.

## Earlier dev integration and completed receipts

Remote primary **b1f507400cb743a3985cb1d50de1ebd085bd4f63** has parents 5034a724d
and current dev **c676aa2f4ad6ee8cff0521da6ba8add70d55949c**, with tree
**858aa04a6f34329f71efbbe0c472ad5902fea23b**. This integrates dev into the feature
branch; PR 2197 has **not** merged into dev. All 46 changed upstream blobs were
independently checked as exact in this actual tree and the predicted normalized
follow-up tree. See the follow-up folder's `integration-c676/` provenance.

The latest application still requires source **44422645793**, moving/upload
**44422645797**, affected desktop stages 13–15 **44422884843**, and fresh mobile stages
2–15. The original remote mobile dispatch **44422910837** was subsequently
cancelled wholly queued; local b1 mobile work replaces that queue plan. Historical stage results keep their original runtime and
checkout identities; applicability to changed inputs is documented separately.
The final dependency review supports retaining prior desktop 1–12 and mobile 1
behavior, with explicit stage-3 hidden-prose and stage-12 handout-projection limits.
It does not validate the changed paragraph, source-detail edges, full revised
route, or new changelog/model behavior. The final mapping is in
`../t3657-t3658-hunt-accessibility-2026-11-18/integration-c676/t3657-t3658-rebase-c676-plan.md`.
There is no latest-head full-source/renderer or merge verdict here. The completed
2,700-second desktop 13 retry above remains scoped to frozen 5034/ae4. Ticket checkpoint 85ea6b1 predates this dev integration.

The newly completed historical receipts are:

| Scope | Run | Result | Time |
| --- | --- | --- | --- |
| Primary 7019 desktop 9 | 44405517767 | 27 passed / 0 failed | 13m24s |
| Primary 7019 desktop 12 | 44405524076 | 29 passed / 0 failed | 12m17s |
| Primary 7019 desktop 14 | 44405530319 | 145 passed / 0 failed | 15m53s |
| QA b501 desktop 5 | 44415899803 | 30 passed / 0 failed | 13m32s |

All four have complete suite, zero-page-error, vendor and SMOKE PASS summaries.
The primary logs are under `renderer/`; the QA log is in the follow-up folder's
`parent-pin-validation/`. QA stage 5 exercised all three detail tiers and their
worst stands: Full 3,544,203/3,630,000 triangles, Balanced 2,694,447/2,750,000,
Light 1,279,387/1,305,000. This remains a b501 result; its applicability to the
unchanged 1835 geometry is separate from latest-dev changelog/source behavior.

Both jobs in run **44412406478** now completed successfully: moving frames and
upload-release (32 checks). The workflow head was 5034, but both logs explicitly
checked out **400ac5f8e803958e4ec577ea3317d9003b6f7efa**, the PR merge with old
dev 169404. `ci/5034-pr-merge-400ac/` preserves the completed logs and final live
GitHub job receipt. These are exact old-merge results, not latest b1 coverage.

`ci/latest-dev-checkpoint/` preserves the saved monitor, root recovery, concurrency
snapshot and cancellation receipts. The concurrency snapshot is explicitly
**23:37:16 UTC**, not a live view. Old 5034 mobile range 44418522036 and old
400ac candidates 44422222083 / 44422343106 were cancelled while wholly queued;
they supply no executed coverage. The latest root recovery supersedes those
queue plans without rewriting their historical receipts.

The older sections below retain their original cohorts and checkpoint context.

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

Before the latest dev integration, completed receipts covered desktop **1/2/3/4/6/7/8/10/11** and mobile
**1/13**, totaling **744 passing assertions**: 601 staged assertions and 143
repeated scaffolding checks. The manifest preserves the earlier local cohort,
the corrected cohort, and incomplete attempts separately. Historical full-mobile
6c83 evidence and failed/capped attempts are excluded from this total. Missing
stages remain required; this is not a complete renderer verdict.

At that earlier checkpoint, primary mobile stages 2–12 and 14–15 were queued
in run **44418522036** on 5034; the wholly queued run was subsequently cancelled.
Those historical source/moving runs are distinct from the current b1 checks
listed above.
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
