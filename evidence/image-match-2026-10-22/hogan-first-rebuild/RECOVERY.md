Latest bounded CI recovery: [50b6 addendum](../hogan-50b6-ci-recovery-addendum-20261023T095659Z/README.md) preserves the original checkout timeout and successful authorized failed-job rerun. No geometry bake or dedicated-smoke success is inferred. Initial50b6 archive remains unchanged.

Newer independent Hogan integration evidence: code head `50b6b0fe0ce661d513988ef913f296391d1c2bea` has official strict local preflight PASS1049 plus changelog/IDs; all ten exact-head workflows were still in progress at the frozen snapshot. No merge, match closure or sourceS gate result is implied. [Immutable bundle](../hogan-pr1229-50b6-checkpoint-20261023T094744Z/README.md).

# Hogan recovery — 05f6, local and targeted QA pass; CI pending

Current pushed head: **`05f6b886e5a31f17ec21e743f945cc4a89abc745`**, branch
`steward/t2377-hogan-picture-match`, [PR #1229](https://github.com/kevinrhaas/chicago/pull/1229)
into dev. Latest dev 5135 is merged. The deterministic 1904 oracle fix adds exactly
27 verified T-3009 Indiana IDs to the expected-ID literal. Assertions, isolation,
workflows and timeouts are unchanged.

Latest frozen evidence: [new-head-05f6-both-QA--20261023T061922Z/STATE.json](new-head-05f6-both-QA--20261023T061922Z/STATE.json).
[Verified checkpoint archive](new-head-05f6-both-QA--20261023T061922Z.tar.gz) — 2,539,818 bytes,
SHA256 `86a59eef6c03b4baba32cccfa771ef0ba7769572401afb5526ba65da7e6c853d`. It contains logs, both completed targeted QA result sets,
screenshots, the actual mirror build.json and the new ten-run smoke plan.

## Completed and the build-tag distinction

Strict local preflight **PASS**: check.sh and committed-diff changelog/ID checks.
Validator: **0 errors, 280 warnings**. The ordered producer settled after **2 laps**,
with its final lap changing nothing. These producer results belong to Hogan;
they do not retroactively settle the archived frame WIP's three-lap warning.

Both targeted Hogan app/card checks **PASS**: mobile 390×780 and desktop 1280×800.
They verify rebuilt attributes and grade, expected declared review records,
credited Cameron/Chicago Historical Society picture/source text, viewport and no
unexpected page/loader errors. Parent inspected the screenshots; the process is
closed. The declared town research-review records are not a scene-release pass.

**The tested mirror build.json says `6156a0367`, built 05:57:20 UTC.** It was published
before the 05f6 dev merge commit. Parent confirms the tested code/content is identical
to the clean 05f6 tree. This is targeted **content-equivalence QA**, not a claim that
the mirror carried a 05f6 build tag. The evidence writer copied the actual build.json
and checked the local code head, without claiming an independent full mirror
rebuild. The new exact-head workflow smokes regenerate their own build tag.

## Remaining gates and changed integration plan

The current CI gate and full smoke conclusions are **pending verification** here.
The [new ten-run plan](new-head-05f6-both-QA--20261023T061922Z/smoke-runs-05f6.json) pins all runs to 05f6 and covers
all 15 parts at both viewports, partitioned 1–4/5–8/9–12/13/14–15. One successful
partition cannot substitute for complete current-head coverage.

Parent next plans a broader prerequisite branch from 05f6 for **T-3055 (M) + T-3056 (S)**,
including the reviewed Hogan progress. Related jail/Beaubien source credits may
expand that pipeline. A concrete broader PR may supersede #1229 after appropriate
preflight. **Do not use an automatic merge helper while that plan is pending.**
No merge or production promotion is authorized by this evidence save.

**Do not run `merge-if-ready.py` or `dispatch-smokes.py`.** Those old 6156 entrypoints
now refuse execution. Their exact source bytes remain in
`merge-if-ready.OBSOLETE-6156.py.txt` and `dispatch-smokes.OBSOLETE-6156.py.txt` for
historical inspection only. No new merge helper is supplied. The old 6156 runs are
superseded; their [capture-time snapshot](new-head-05f6-both-QA--20261023T061922Z/superseded-6156-runs.json) preserves
recorded states, including some in_progress rows, rather than asserting verified
final cancellation conclusions. Old successes do not cover the new head.

## Acceptance and recovery boundaries

Original **T-2377 remains open, not done**. Its provisional research comparison is
**differs**, with no accepted reference view. Pictured attested structure-grade is
not complete geometry matching. Source/date/survival and visible differences remain.

The original four M frame claims were released; genuine prerequisites T-3055 (M) plus
T-3056 (S) are now claimed as one M plus S. Original frame image gates stay open. This
evidence writer changed no claim or ticket. The existing frame stash and every
prior published archive remain intact.

Evolving T-2377 continuation and T-2385 third/roof-flag-anchor packages remain absent
until their agents finalize them. Earlier 6156 RECOVERY/checkpoint snapshots remain
explicitly superseded history. Prefer the new pushed code head and this frozen
state over old WIP patches; reconcile any newer branch work before recovery.
