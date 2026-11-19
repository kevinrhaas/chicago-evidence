# Fixed 1,121-declaration verification snapshot

The immutable proof recorded at 00:52:07 UTC on 19 November 2026 covers 1,121 of 1,379 declarations on source `6409dda1222e1284e111ab0efde1c471f3284d60`, tree `eeaaefef97d3275b048f308c57c3df5514dbb028`, base `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`. It credits 1,118 ordinary checks and three prerequisites, with 258 missing. Only completed local 3/6/7/8/15/16 and hosted 1/2/5/6 are accepted, with overlap counted once. Local 11 was running at capture and is excluded; later source progress does not alter this snapshot.

| Newly archived invocation | Checks | Self-tests | Process result | Gate wall seconds |
| --- | ---: | ---: | --- | ---: |
| Local 7/16 | 89 | 27 | Original exit 0 | 303.766 |
| Local 15/16 | 88 | 25 | Original exit 0 | 369.900 |
| Local 3/16 | 90 | 25 | Original exit 0 | 253.289 |
| Hosted 1/8 | 175 | See raw log | Successful job / terminal PASS | 294.056 |

The local bundles retain raw logs, timings, original nanosecond process receipts, wrappers and reviewed controller diffs. Required readers and base checks remain enabled. The remaining-parts controller used by local 3 also checks live origin branch/dev before preparing each invocation; its planned later parts do not count as executed evidence. Prior controller bytes remain preserved.

Local 7/16 and 15/16 together cover exactly the 174 declarations selected by hosted 7/8, with no ordinary overlap and only three shared prerequisites. This equivalence does not mark that hosted job successful. The canonical hosted snapshot still has parts 1,2,5,6 passed and parts 3,4,7,8 queued, with no complete gate result.

The two original manifests and `archive-dependency-map.json` bind 62 unique incremental dependencies. The approved discovery verifier, its 35 controls and recorded review are unchanged from the earlier 691 checkpoint and are reused by exact hash. The frozen staging script, new explicit binding, completed raw evidence and actual partial-proof refusal are preserved here. Intermediate 949/1034 reports are not needed for this standalone proof and were omitted.

CI snapshots are under `../../ci/current-6409/snapshot-1121/`. The completed upload-release log now proves all 32 checks passed, completing the moving/upload supporting workflow; its receipt is under `../../ci/current-6409/moving-upload-final/`. Both supporting workflows are successful, while the full source and legacy-browser gates remain incomplete. No browser dispatch, merge, research or app changes are claimed.
