# PR2198 browser validation handoff

PR: https://github.com/kevinrhaas/chicago/pull/2198

Frozen head: `822f0a9ae94b52c893a00aaf7baf698a3cd1a6b9`; tree `8c2f7998938e95f1da1562258991ea6c16fbb330`; included dev `69d9659ea09bcb8f87f9d9be9c475c657b6f5b8f`; runtime input hash `sha256:f681e5412b836a8d`.

At 2026-11-19T03:15:31.779Z, desktop13 is running the published smoke and desktop1–8 is in checkout; four other workflows are queued. Verified browser coverage is0/30. Full source and all30 browser cells remain required before merge. Root confirms PR2206's new dev commit8c605db0571e29ee9da6d8aba5181451d9d84db8 changes only pre-fire source/site paths, with no4D runtime input change, so keep these existing822jobs; do not retire or redispatch them. The user has authorized merging to dev when the complete required checks are green; no additional user confirmation is needed.

| Viewport | Stages | Run | Native job |
| --- | --- | --- | --- |
| desktop | 13 | https://github.com/kevinrhaas/chicago/actions/runs/44447647854 | 135303589201 |
| desktop | 1–8 | https://github.com/kevinrhaas/chicago/actions/runs/44447665922 | 135303646577 |
| mobile | 1–12 | https://github.com/kevinrhaas/chicago/actions/runs/44447683223 | 135303702865 |
| mobile | 13–15 | https://github.com/kevinrhaas/chicago/actions/runs/44447702227 | 135303766503 |
| desktop | 9–12 | https://github.com/kevinrhaas/chicago/actions/runs/44447717746 | 135303819580 |
| desktop | 14–15 | https://github.com/kevinrhaas/chicago/actions/runs/44447735937 | 135303877687 |

All six were dispatched exactly once, with each ID durably recorded before the next API action. Do not dispatch duplicates or blindly retry. Existing workflow assertions and150-minute job caps are unchanged. Historical6409/933 results give zero coverage to this head.

The local watcher has been stopped at root's explicit session-wrap-up instruction. PID244990 was verified as only `/tmp/t3654-watch-ci.py`, then terminated withSIGTERM (exit143); no GitHub workflow was cancelled. There is no background-monitoring guarantee after this handoff. To resume, first check `pgrep -af '^python3 /tmp/t3654-watch-ci.py$'`; start one copy only if absent, using the existing six IDs in `/tmp/t3654-legacy-coverage-ledger.json`. Poll those workflows—do not rerun or redispatch them. `/tmp/t3654-watch-ci.py` is read-only and may be restarted into a new dated log. Its final prior log is `/tmp/t3654-watch-ci-822f0a9a-final.log`; final native status and ledger snapshots are `/tmp/t3654-822f0a9a-browser-session-final-status.json` and `/tmp/t3654-822f0a9a-browser-session-final-ledger.json`. The original immutable dispatch closure is `/tmp/t3654-822f0a9a-six-group-dispatch-evidence-manifest.json`.

For each completed run, fetch final metadata using `gh run view RUN --repo kevinrhaas/chicago --json headSha,headBranch,status,conclusion,createdAt,updatedAt,jobs,url` into `/tmp/t3654-ci-RUN-meta.json`. Obtain decoded native logs with GitHub connector `github_fetch_workflow_job_logs`: the actual log is `structuredContent.content`, not the display message. Save those exact UTF-8 bytes to `/tmp/t3654-ci-RUN.log`. Verify actual checkout822f0a9a, published target, expected viewport/stages, zero failures/page errors, and terminal `SMOKE PASS`. Then `/tmp/t3654-register-ci-log.py RUN` updates only the ledger and verified-log map. Never credit queued/running/cancelled/failed or missing logs.

ROOT receipt writes are still held for the owning agent's release. When released, use the existing `node tools/dev-smoke-state.mjs ci RUN` under `/tmp/t3654-runtime.sh`, with `T3654_CI_LOG_MAP=/tmp/t3654-verified-ci-logs.json` and `/tmp/t3654-gh-log-adapter` first inPATH. The adapter supplies only hash-verified decoded logs and forwards metadata to realgh. The importer hashes the current checkout: do not import an old run under a different runtime hash or mislabel CI as local.

Before merge, require all30 fresh stage/viewport cells plus the complete current hosted source gate (eight parts and aggregate), required supporting checks, and the same verified PR head. Source run44447282208, humans44447282230 and moving/upload44447282219 belong to the source monitor. Recheck live PR/head/base and any unresolved findings; preserve all real failures. Root owns ready/merge and the lap lease, last renewed02:22UTC to about05:22UTC. No production deployment is authorized by this handoff.
