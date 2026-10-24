# Current transport recovery handover — 24 October 2026

Captured 2026-10-24T10:46:35.774357+00:00. This is a status checkpoint, not a DEV merge or full delivery receipt.

App: `/workspace/chicago`, branch `steward/t3083-t3086-t3087-transport-recovery-20261024`. HEAD is `3290195d40cbacf5cbfd0c76f14119d6712aa30c`, tree `bac89999d2afd653e632c52d15b2f50336688deb`; source is unchanged.

[Draft PR #1279](https://github.com/kevinrhaas/chicago/pull/1279) targets DEV. The normal ticket CLI put T-3083, T-3086, and T-3087 in **review** for that actual PR; they are not done. See [the pushed review transcript](/workspace/.cloud-setup/logs/transport-recovery/group-review-pr1279.log).

The three source commits remain `4a14cdf92` (lamps), `d718a1711` (eye UVs), and `8c45c899f` (viewpoint/shared provenance), followed by the ordinary DEV merge. [The commit receipt](/workspace/.cloud-setup/logs/transport-recovery/app-commit-receipt.json) preserves their grouping.

The observed server test merge is Q `01977d66`, with base B `c96846f1` and source HEAD H `3290195d`; Q's tree is `7bcae13c`. All 55 child-only files match H byte-for-byte; four shared files contain incoming DEV changes. The actual merge and workflow binding must be rechecked if B, H, or Q changes. See [the exact PR binding](/workspace/.cloud-setup/logs/transport-recovery/queue-review-pr1279-PUBLISHABLE-20261024T1030/queue-review-pr1279-exact-binding-20261024T1027.json).

Current H's complete local preflight passed **1,063 steps, none red**, including 383 negative self-tests. Exact-HEAD changelog and ID checks passed. This is a local result, not a CI substitute. [Gate transcript](/workspace/.cloud-setup/logs/transport-recovery/latest-dev-complete-preflight-check.log).

Runtime execution returned at 10:23 UTC. Mobile stages 1–10 passed in 5 recorded legs; mobile stages 11-12 are active. Desktop and full all-stage coverage are not yet established. The authoritative record is [latest-dev-smoke-resume-binding.json](/workspace/.cloud-setup/logs/transport-recovery/latest-dev-smoke-resume-binding.json); continue with `/workspace/.cloud-setup/resume-transport-smoke.py` and actual persisted receipts, not an old terminal session or blind relaunch.

Mobile stages 3–4 produced Node return code **0**, `SMOKE PASS`, 125 staged checks, and successful owned cleanup, but the outer wrapper returned **120** after stdout closed. A separate closed-stdout reproduction proved the reporting fault; fixed-wrapper success and failing-child checks confirmed correct result preservation. The original receipts remain unchanged. [Reproduction](/workspace/.cloud-setup/logs/transport-recovery/supervisor-closed-stdout-reproduction.summary.json), [fixed success](/workspace/.cloud-setup/logs/transport-recovery/supervisor-closed-stdout-fixed-check.result.json), [failure propagation](/workspace/.cloud-setup/logs/transport-recovery/supervisor-closed-stdout-failed-child-check.result.json).

The earlier old-HEAD smoke interrupted with code 130 is still NOT PASS. Older preflight cleanup records with 701 remaining owned children are not clean receipts; corrected-wrapper tests do not retroactively change them. Keep each run's result and cleanup separate. Never touch PID1 or unowned processes.

Last saved CI snapshot, **10:36 UTC**:

- Gate [40085901834](https://github.com/kevinrhaas/chicago/actions/runs/40085901834): in progress; no final pass recorded.
- Moving frames [40085901811](https://github.com/kevinrhaas/chicago/actions/runs/40085901811): failed at **Install Playwright**, before rendering. The precise installer error is still unread.
- Stuck PR report 40069749728: success.
- Content build 40069749684: `warranted` succeeded; bake, smoke, consumer, publish, and PR jobs were skipped. Do not call those skipped jobs passed.

[Detailed CI snapshot](/workspace/.cloud-setup/logs/transport-recovery/queue-review-pr1279-PUBLISHABLE-20261024T1030/queue-review-ci-final-snapshot-20261024T103600Z-summary.json). Recheck actual current CI before any action; this document does not predict its outcome.

Fetching runner logs is separately blocked by proxy **CONNECT 403** for `productionresultssa14.blob.core.windows.net` and `productionresultssa15.blob.core.windows.net`, before a destination HTTP response. Draft revision 9 contains the pending hostname additions; saving it is not proof of application. Do not invent an installer diagnosis, bypass the proxy, rerun CI, patch source/workflows, or use an admin merge on this evidence. [Sanitized redirect/probe evidence](/workspace/.cloud-setup/logs/transport-recovery/queue-review-pr1279-PUBLISHABLE-20261024T1030/queue-review-moving-log-20261024T103110Z-publishable-probe-binding.json); never export private raw responses or signed log URLs.

Latest pushed evidence checkpoint: **8**, commit `7269858`, under `kevinrhaas/chicago-evidence/evidence/transport-recovery-2026-10-24/CHECKPOINT-8-MOBILE-1-8-AND-CI/`. Newer local browser progress needs the next ordinary checkpoint; root handles pushes.

All 58 original snapshot files were hash-verified and retained as immutable evidence before integration; incoming data and bakes remain preserved. Glessner liberty blocks/records, old liberty raw lines, existing registry rows, previous anchors, and ROADMAP's original non-UTF8 byte remain protected. [Preservation audit](/workspace/.cloud-setup/logs/transport-recovery/latest-dev-merge-preservation-audit.json).

Scope stays bounded: T-3083 changes Brougham lamp form only; T-3086 repairs ocular UVs while preserving geometry, rig, weights, clips, materials, and six images; T-3087 adds the safe yard camera without moving the horse. CPU comparisons and browser numerical checks do not establish photographic completion.

Keep T-3084/T-3085 carriage appearance/interfaces/native qualification and T-3088/T-3089 horse anatomy/materials/portable qualification open. Parents T-2794/T-2800 stay split. Gait, drivers/riders, tack, teams, boarding, and interaction work remain separate; T-2803/T-2804 were released/open. Do not restore the gait study's old eye texture over d454.

Next: complete and inspect the bound browser legs, obtain the blocked CI logs through applied supported settings, diagnose the actual installer error, and collect fresh required green checks on the actual current PR. Merge ordinarily only after those conditions hold; verify public DEV assets and the yard viewpoint before claiming delivery. No DEV merge or production promotion is claimed here.
