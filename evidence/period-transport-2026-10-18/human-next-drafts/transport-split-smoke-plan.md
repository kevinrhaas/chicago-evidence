# Transport smoke: 18 existing-workflow dispatches, one frozen head

Status: proposal only. No dispatch, branch update, workflow edit, geometry bake, or cap change has been performed. Start only after instrument corrections are committed, the full preflight passes, and root authorizes dispatch. The original head 1b3c73d is NOT green: mobile full smoke failed stage 5; desktop full smoke hit the 90-minute job limit and contained four observed failures. Preserve those records.

## Verified existing contracts

- `.github/workflows/chicago-4d-smoke.yml` accepts `viewport` and `stage` through workflow_dispatch. Its one job has a 90-minute timeout, installs Node 22 + Playwright 1.56.1, runs `bash tools/publish.sh`, then `node tools/smoke_renderer.mjs --published`. It has no concurrency cancellation group.
- `.github/workflows/chicago-4d-bake.yml` smoke matrix uses mobile/desktop and nine ranges: `1-2`, `3-4`, `5`, `6-7`, `8`, `9-12`, `13`, `14`, `15`. That union covers parts 1..15 exactly once per viewport. The bake's legs use a 40-minute cap and a shared downloaded published artifact; this proposal uses the existing manual workflow's unchanged 90-minute cap and independently publishes the same committed inputs in each job.
- `node tools/smoke_budget.mjs --self-test` was run read-only and passed: 15 parts, 232 patterns, eight anchored modules, nine gate legs tiling 1..15 exactly once. Its `gateShape()` reads the actual workflow matrix; its self-test rejects gaps and overlaps.
- `tools/smoke_renderer.mjs` increments `stageWorkChecks` only inside each `stageOn(n)` section, prints pass/fail totals, then prints `N staged-section check(s) (stage RANGE of 15), A always-on check(s)`. Every invocation runs boot, suite-completion, page-error and vendor guards. The observed original mobile full run had 668 section checks + 13 always-on checks = 681 total, but that is evidence of that OLD head, not a count to assume for a corrected head.
- `tools/dev-smoke-state.mjs` parses the selected viewport/range, published/source target, assertion lines, body-end zero-page-error marker, and wall time. It records `killed` if a body does not complete. It does NOT validate the 18-run union or retain staged/always-on audit counts; use an outside-checkout aggregate receipt as described below. Its `record`/`ci` commands hash the CURRENT checkout, not the run's archived tree: never fold old logs into an unrelated branch and claim exact-tree evidence.

## Freeze and dispatch exactly 18 legs

Use one branch/ref whose head root promises not to move until collection completes. The workflow_dispatch API documents branch/tag refs, so do not assume raw commit SHA is accepted. Verify every resulting run's `head_sha` against the chosen SHA; ref immutability alone is not accepted as proof.

Set task-specific values (never infer the target from the current local branch):

```bash
REPO=kevinrhaas/chicago
REF=steward/FROZEN_TRANSPORT_BRANCH
SHA=FULL_40_HEX_COMMIT_AFTER_FIXES_AND_PREFLIGHT
```

Read-only preparation:

```bash
gh api "repos/$REPO/git/ref/heads/$REF" --jq .object.sha
# Require output == SHA. Save UTC dispatch start and existing run IDs outside checkout.
gh api "repos/$REPO/actions/workflows/chicago-4d-smoke.yml/runs?event=workflow_dispatch&per_page=100" \
  --jq '.workflow_runs[] | {id,head_sha,created_at,run_attempt,status,conclusion}'
```

After authorization, these are the exact 18 dispatches; each loop iteration is one separate existing-workflow run:

```bash
for viewport in mobile desktop; do
  for stage in 1-2 3-4 5 6-7 8 9-12 13 14 15; do
    gh workflow run chicago-4d-smoke.yml --repo "$REPO" --ref "$REF" \
      -f viewport="$viewport" -f stage="$stage"
  done
done
```

Expected dispatch grid:

| viewport | exact stage inputs |
| --- | --- |
| mobile | 1-2; 3-4; 5; 6-7; 8; 9-12; 13; 14; 15 |
| desktop | 1-2; 3-4; 5; 6-7; 8; 9-12; 13; 14; 15 |

No bake workflow is dispatched. The manual workflow only publishes committed assets through its existing publisher; it does not invoke Blender or regenerate masters. Runner availability may queue some legs. Queueing is not failure, and no additional dispatch is needed merely because a leg waits.

## Identify and monitor runs without guessing the pairing

Do not assume dispatch command order equals GitHub run-ID order, or that gh prints an ID. Save the before/after workflow run-ID difference, constrained to event workflow_dispatch, creation at/after dispatch start, and exact `head_sha == SHA`. Then read the selected `SMOKE_VIEWPORT` and `SMOKE_STAGE` from each job log's environment and its `NOT THE FULL GATE` lines to establish its actual grid cell. The workflow run summary does not itself expose inputs reliably.

Read summaries about once a minute, all commands with explicit repository and run ID:

```bash
gh api "repos/$REPO/actions/runs/RUN_ID" \
  --jq '{id,event,path,head_sha,status,conclusion,html_url,run_attempt,created_at}'
gh api "repos/$REPO/actions/runs/RUN_ID/jobs" \
  --jq '.jobs[] | {id,name,status,conclusion,steps}'
```

After a run finishes, obtain its normal GitHub log outside the checkout:

```bash
gh run view RUN_ID --repo "$REPO" --log > /workspace/shared/transport-smoke-RUN_ID.log
```

Preserve normal TLS/proxy configuration. If log retrieval is blocked, do not bypass it or loop unchanged downloads: summary success alone cannot establish detailed coverage receipt fields. Ask for the supported missing access and leave aggregate validation incomplete.

## Required per-leg receipt

Store one JSON record per selected run under `/workspace/shared`, with:

- repository, workflow path, frozen SHA, actual run head SHA, run ID, run attempt, URL, event, UTC start/end, API conclusion;
- actual viewport, actual stage input, expanded integer parts, target `published`, runner/tool version evidence from log;
- final passed/failed totals, section count, always-on count, wall seconds, `SMOKE PASS` presence;
- counts and exact names of every untagged pass/fail assertion; body-completed and zero-page-errors guards; vendor decoder support and no-error guards;
- log file path and SHA256, plus smoke source/ledger versions from the frozen commit. Preserve any earlier failed/cancelled attempts as separate records; a replacement does not erase them.

A valid individual leg requires ALL of:

1. API conclusion success, event workflow_dispatch, expected workflow path, and actual `head_sha == SHA`.
2. Exactly one expected viewport and the requested range; the log says PUBLISHED mirror and contains `--published` execution.
3. A terminal `SMOKE PASS`, `failed == 0`, nonzero executed section checks, and a final summary. No cancellation, timeout, traceback, missing page-error guard, or incomplete body.
4. `passed + failed == sectionCount + alwaysOnCount`, and counts equal the parsed assertion lines (include both vendor assertions in the global total).
5. All always-on guards actually passed. At the previously measured head there are 13 per single-viewport invocation; establish the exact guard manifest from the FROZEN smoke source before dispatch and require the same count/manifest in every leg. Do not silently change the expected count to match a log.
6. No hidden untagged failure line, including a failure before an eventual successful-looking footer. Intentional negative self-tests from check.sh are not part of these browser logs.

## Aggregate coverage validation

Select exactly one accepted successful attempt per expected grid cell, preserving superseded attempts separately. Reject unexpected viewport/range cells, duplicate selected cells, missing cells, different heads, source-tree runs, empty/partial logs, or any failed/killed selected leg.

For EACH viewport:

- Require exactly nine selected legs and expand the ranges. The sorted multiset must equal `[1,2,...,15]` (15 entries, no duplicates). This is the same tiling contract already enforced by smoke_budget's self-test for the bake matrix.
- Sum `sectionCount` across the nine legs. Validate that sum against the concatenated selected SECTION assertion inventory and retain it as `executedSections`. Always-on guard repetitions must not be counted as additional section coverage.
- Require all nine identical always-on guard manifests. Report repeated guard executions separately (`9 * A`), and count the logical always-on set once when presenting equivalent per-viewport gate checks (`sum(sectionCount) + A`). Raw aggregate assertion executions are `sum(sectionCount) + 9*A`.
- If a completed unfiltered reading exists at the SAME frozen head, require its section count to equal the nine-leg sum and its always-on count to equal A. Do not substitute the old mobile 668/13 reading from head1b3c73d or a cancelled desktop run. If no same-head unfiltered reading exists, state that numeric comparison is unavailable; structural tiling + executed-section inventory + every-leg guards establish the staged full-coverage gate per the repository's bake contract. Do not pretend that a new unfiltered run passed.

Across both viewports, require 18/18 accepted legs, all parts 1..15 exactly once PER viewport, and no unresolved head mismatch. Produce a single aggregate JSON receipt and a concise table of viewport, range, run URL, actual SHA, section checks, always-on checks, verdict, duration. Name the result **"complete split published smoke coverage, both viewports, at SHA"**. Every individual run remains a PARTIAL leg and must retain its own `NOT THE FULL GATE` label.

Full check/preflight and relevant PR checks must also be green at the same final head before root marks ready/merges. This plan neither grants merge approval nor treats partial leg success as full coverage.

## Current known failures and stop conditions

- Original mobile run39164260098: 680 passed/1 failed, stage5 far-merge strict triangle parity; body completed. Preserve failure evidence.
- Original desktop39164186323: 90-minute job timeout; 353 observed passes and failures in stages1,2,5,6. No complete all-stage verdict.
- Instrument fixes must preserve existing bars and be validated before dispatch. Any newly failing leg requires diagnosis, a documented correction, fresh frozen SHA/preflight if source changed, and a new consistent coverage set. Do not combine different source heads to make a green matrix.
- Existing 90-minute cap is unchanged. If a selected split leg still times out, report that measured leg and diagnose it; do not raise the cap or call its partial execution a pass.
