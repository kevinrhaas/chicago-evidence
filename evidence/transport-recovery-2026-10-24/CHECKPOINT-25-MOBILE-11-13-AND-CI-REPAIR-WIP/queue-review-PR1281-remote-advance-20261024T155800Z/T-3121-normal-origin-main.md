---
id: T-3121
title: The full smoke's push path fires on every PR that merges dev after a chicago-4d-smoke.yml edit, cannot finish in 150 min, and so holds those PRs unmergeable (#1277, #1278)
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: null
decision: null
decision_answer: null
---

The full smoke's push path fires on every PR that merges dev after a chicago-4d-smoke.yml edit, cannot finish in 150 min, and so holds those PRs unmergeable (#1277, #1278).

## FILED ABOVE BAND 9, BECAUSE IT BLOCKS

A follow-up goes to the foot of band 9 unless dev's gate is red on it or the build in hand cannot finish without it (owner, 2026-09-27). This one was placed above band 9 on this reason:

> #1278 and #1277 are complete with a green gate but carry an incidental full-smoke run that times out (cancelled) — gh-rest refuses it as red and merge-ready reads the PR as unstable, so neither path can merge them

## What happened (2026-10-24, measured)

- dev commit 10ac7602e (T-3081, T-3082, 12:48Z) changed one line of `.github/workflows/chicago-4d-smoke.yml` (`runs-on: ubuntu-latest` → `ubuntu-24.04`). That workflow's only push path is its own file, so dev's push fired the unfiltered two-viewport full smoke (run 40095445643). It ended **cancelled at 15:18Z, the 150-minute timeout**, with no verdict.
- Every PR that merged dev after that commit carries the same file change in its lap push, so the full smoke fired on the PR branch too: #1277 (run 40096290470, 13:00Z) and #1278 (run 40097468293, 13:17Z). Neither PR edits the workflow in its own diff.
- No push-triggered full smoke has completed since 2026-10-19: every one in the history ended `cancelled` at roughly 150 minutes. Desktop part 13 alone was measured at 85 minutes (#1054).
- `pr-automerge` (gh-rest.sh `gate_state`) counts that check run as part of the gate. While it runs, the PR reads `pending`, and #1278 has spent six 540-second merge laps across three runs on it. Once it times out it reads `red smoke (cancelled)`, which is a refusal. `merge-ready.sh` only merges `clean`, and the PR is `unstable` either way. So a complete PR with a green `gate` cannot merge by either path, and re-running the workflow on the branch only starts another 150-minute run.

## Acceptance

- A lap that merges dev into a PR no longer leaves a check on the head that cannot finish. Options to weigh: restrict the push path to `branches: [dev]`, so the self-test runs once, where the edit lands; or have the merge gate disregard `Chicago 4D — full smoke`, which its own header says is a measurement and not a gate ("a ~25-minute-per-viewport Playwright crawl on every push would be a queue, not a gate").
- #1277 and #1278 merge on their green `gate`, without `GH_REST_MERGE_BLIND`.
