# Fixed 691-declaration verification snapshot

The immutable proof recorded at 00:34:30 UTC on 19 November 2026 covers 691 of 1,379 declarations on source 6409, tree eeaa, base c676: 688 ordinary checks plus three prerequisites, with 688 missing. It accepts completed local 6/16, 8/16 and 16/16 and hosted 2/8, 5/8 and 6/8, counting overlap once. Full source coverage, browser readiness and merge authorization remain false. Local 7 and hosted 1 were running at the capture boundary and receive no credit.

| New local invocation | Checks | Self-tests | Original exit | Wall seconds |
| --- | ---: | ---: | ---: | ---: |
| 16/16 | 88 | 28 | 0 | 270.828 |
| 8/16 | 89 | 25 | 0 | 363.073 |

Both bundles retain raw logs, per-check timings, nanosecond process receipts and wrappers. The controller's reviewed diff changes the authorized invocations; required reader/base flags stay enabled and the original local 6 controller stays unchanged. The frozen after16 and after8 ledgers remain separate capture points.

The equivalence proof shows that local 8/16 and 16/16 cover exactly the 174 declarations selected by hosted 8/8, with no ordinary overlap and only three repeated prerequisites. It does not mark that hosted job successful. The hosted guard still verifies only parts 2, 5 and 6 of 8.

The approved discovery verifier SHA256 is `689cdbe91eb6a2d9499c9f4d27d8e7f12f137c1495fcb1848f04d289d5442c3b`. Its 35 control tests pass. The recorded review covers explicit receipt prefixes, nonrecursive discovery, resolved-parent/path checks, refusal of escaping symlinks, and refusal of an unadmitted current failure. It preserves strict source context and exact invocation exit identity. Historical test fixtures exercise the checker only and supply no current source coverage. The review file is a summary of in-session independent review and root approval, not a CI or browser verdict.

The two original manifests and `archive-dependency-map.json` bind 49 unique dependencies, reusing unchanged earlier evidence. The fixed staging-script copy and exact new bindings are preserved; active helpers, live summaries and running local 7 artifacts are excluded. The separately archived dispatcher refusal on this partial 691 proof leaves its ledger unchanged and launches nothing.

CI metadata snapshots are under `../../ci/current-6409/snapshot-691/`. A separately timestamped moving-frame PASS is under `../../ci/current-6409/moving-completed/`; upload-release was still in progress, so the whole supporting workflow is not claimed green. No research or application changes were made for this checkpoint.
