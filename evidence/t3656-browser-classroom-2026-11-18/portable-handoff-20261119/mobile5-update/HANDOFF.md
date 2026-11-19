# 4D Chicago continuation — 19 November 2026

The user authorized parallel non-server work, periodic GitHub commits/PRs, and merging to DEV when green. They now request wrap-up because the conversation budget is nearly exhausted. No DEV merge has happened as of the latest 03:04 UTC check. Production promotion is not authorized.

## PRs and saved work

- PR2197: https://github.com/kevinrhaas/chicago/pull/2197 — classroom photos/share, notebook, reflections, lesson guides, daily photo hunt and bounded accessibility/keyboard work; tickets T3656/T3657/T3658 all review. Current pushed head `af466d1638fda72a468ecd3ac22456844b870c1b`, tree `b39124d16c7869bf816354ab78a177eea320fb39`, based on DEV `69d9659ea09bcb8f87f9d9be9c475c657b6f5b8f`. Draft until full release gates finish. PR2199 is closed unmerged, superseded by2197.
- PR2205: https://github.com/kevinrhaas/chicago/pull/2205 — T3663 optional cited Gossip investigation, saved to existing notebook. Head `fc51c9efcd56f863a3493d67101ae2e1ec60e75e`, branch `steward/t3663-gossip-evidence`, worktree `/workspace/chicago-investigation`. Draft, depends on2197; current DEV diff contains its parent work. Rebase only T3663 commits onto actual DEV after2197 lands. Pure/storage/export/regression checks, gate registration, official no-write measurement and source review pass. Browser/full source/release gates are pending. Ticket is review, pushed at32855a34f.
- No server/service activation or production promotion. Item1 Jump remains deprioritized; no extra world/preload. Full twenty-item disposition is `chicago/4d/docs/CLASSROOM-FEATURES.md`.

## Critical live freeze

`/workspace/chicago` deliberately remains at LOCAL `3472ec872d00e33761490b0138b23da1c63daee2`, tree `33239df61859c000e76ae6a5bd8ec91124ea8352`. Its source and `/workspace/chicago/site/4d` publication are FROZEN for the live mobile cohort. Do not checkout, pull, publish, run a local full gate, or launch another Chromium while it is active.

The remote PR head af was created using merge-tree/commit-tree and pushed by SHA without changing the local branch. af differs from347 ONLY in the upstream T3562 pending-entry deletion and folded changelog. Stage13 reads the changelog; mobile1–12 inputs are unchanged. Remote refs may move; local HEAD/source/publication must not.

Publication version3472ec872, built_utc2026-11-19T02:43:30Z. Harness SHA256578bc819aac9b3dbe4e508a715504a5896a81bf6d81e0a9e823fa6535377c004. Source/published main SHA256bbcb5d888bf3516e8cb7dba7e8ceb162c70e88c21ff71ec86b033c560fb85df7.

## Current2197 release checks

- Source workflow44446919895: eight queued parts at03:04; require ALL eight and aggregate green on af.
- Moving/upload44446919852: both running at03:04; require both green.
- Desktop published13–15:44446945583 running; mobile13–15:44446951072 queued. Require terminal PASS, selected body completion, zero page errors and both vendor guards. No partial/failed/capped group credit.
- Desktop1–4 and6–12 already terminalPASS on ddc786069 (320/0 and111/0). Stage5 retains its scoped b501 result. Independent exact-input proof at `/tmp/t3658-desktop-early-stage-scope/` supports reuse through347; af is fold-only. All1528 indexed1835 assets, all765 relevant liberty subsets, three teacher catalogs and early stage bodies match.
- Mobile1: recoveredPASS95/0. The original Python supervisor was SIGKILLed before its normal end receipt; preserve that limitation. Kernel zombie timeoutPID234227 had exit0, matching durable start/PID within0.029s, full mirror rehash and all final guards. Exact accepted recovery receipt `/tmp/t3658-347-mobile-1-12/mobile-1-recovered-kernel-exit.json`, SHA221b718ca6898cee7b502c3831d3dbd908c97c61e6a529bc265b03548c8fe467. Do not describe this as an ordinary supervisor exit receipt.
- Distinct normal mobile2–12 cohort `/tmp/t3658-347-mobile-2-12/`: stages2/3/4 PASS115/107/45, exit0 with all guards and frozen inputs; stage5 active at03:04. SupervisorPID=PGID=session235873, stage5timeout238431. It runs one stage/world at a time,1200+5sec cap, durable receipts. Do not launch a duplicate. Monitor: `python3 /tmp/t3658-347-mobile-status.py`. Detailed interruption instructions: `/tmp/t3658-347-mobile-handoff.md`.

The old ddc desktop13–15 failed308/2 (retained UI focus, texture errors), and old ddc mobile was cancelled after recording the same Space failure; neither establishes passing coverage. Fixed native/world Space block passed11 checks at each width; first desktop diagnostic failed context loss and is preserved. Current af includes the proved stage14 world-focus precondition and upstream stage15 picture-drain repair without weakening assertions. Queued347 replacement runs were cancelled before any step and replaced by af runs.

## Finish order

1. Keep the healthy mobile supervisor alive. Read complete receipts; never infer exit0 from PASS text alone. Preserve failures and do not auto-retry caps.
2. Wait for current af CI and both published13–15 runs. Agent release_checks owns monitoring and has been delegated the authorized2197 merge endgame.
3. Fresh-read actual DEV and PRhead. If both still69d9659/af and all gates are green, update final PR validation, mark ready, expected-head squash-merge2197 toDEV, verify merge and ticket settle. If DEV changed, review/integrate its actual delta and validate it. Never merge blind or with admin bypass.
4. After2197 lands, rebase only T3663 commits from347 onto actual DEV, update2205. Browser fixture `/tmp/t3663-investigation-browser.mjs` is PREPARED, NOT RUN. Proposed scope `/tmp/t3663-scope-against-af.md`: fresh15 both widths, real published completed-Gossip flows including daybook return/Go-to, native keyboard/200% text/export checks, and explicit unchanged-input proof for any reused stages. It is a proposal, not passing coverage. Full source and CI are still required.

## Durable evidence

Repository https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence . Current completed archive18f498395a89f4417fd3059f6160b851019a0729 includes `t3663-gossip-investigation-2026-11-19/`; prior7dc8fdc includes recovered mobile1. Evidence_checkpoint is archiving completed normal mobile2–4 and this handoff next. Do not archive an active log as completed.

Primary evidence: `t3656-browser-classroom-2026-11-18/`; follow-up evidence: `t3657-t3658-hunt-accessibility-2026-11-18/`. These preserve exact provenance, passed/failed/cancelled attempts, source repair/negative controls, scope proofs and screenshots.

Live detailed local recovery: `/tmp/t3656-live-recovery.json` (current_summary and named current fields take precedence over retained historical sections). CI monitor: `/tmp/t3656-ci-monitor-state.json`, owned by release_checks. All code is pushed; no credential values belong in artifacts.

Latest mobile update: stage5 also completed normalPASS30/0 in354.664s, all guards/pins/quiet; stage6 now running, timeoutPID239665 under the same healthy supervisor235873. The stage5 raw log/receipt are ready for archival. Earlier03:04 status above is preserved as a dated snapshot.
