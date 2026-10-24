Exact-head normal CI expectations for PR #1279

Source H: be56fb269eee6aa7963b8a8d76d5a950f56f857c
Source tree: a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5
Observed base B: de91c45b314a705a6cc2fb9430becb666dfbded6
Observed GitHub synthetic merge Q: 0acb98a9adbafa43fa9346b4d00a08f81101a30c
Q parents are exactly [B,H], and Q tree equals H tree. Recheck these bindings if either PR head or base advances.

Normal PR-event checks on new H: gate run40103721055/job120900960327; moving-frames run40103721119/job120900960672. The current PR diff includes Chicago 4D files and renderer JS, satisfying both path filters. No humans path-filter match exists in the current diff against B, so absence of a new humans run is expected.

Normal branch-push checks on new H: full smoke run40103716423/job120900945869, content build run40103716420, stuck-PR report run40103716422. Full smoke is triggered because the normal branch update brings the already accepted DEV smoke workflow change relative to historical source329. It is not a manual dispatch. The content build warranted check succeeded and downstream expensive bake/publish/smoke/fresh-consumer jobs were skipped. That skipped content-build smoke job is not the independently active full-smoke job120900945869.

Both moving-frames and full-smoke Playwright install steps succeeded (22s and24s respectively), resolving the historical329 Ubuntu26 install failure on the new inherited Ubuntu24 runner definition. These installation outcomes do not by themselves prove browser coverage.

On completion verify actual checkout/commit and published build from each original job log. PR-event jobs may check out Q while branch-push smoke checks out H; matching Q/H trees provide the precise content binding. Full-smoke workflow supplies empty viewport/stage filters and should execute all15stages for mobile and desktop; require the final runner summary, positive executed counts, no failed assertions and actual completion. Record skipped/failed/cancelled/timed-out outcomes distinctly. All prior329 CI results remain historical.

Read-only audit: no reruns, dispatches, remote writes or new runner patch. Safe metadata snapshots are in ci-newhead-be56-20261024T144352Z and ci-be56-watch-20261024T144615Z.
