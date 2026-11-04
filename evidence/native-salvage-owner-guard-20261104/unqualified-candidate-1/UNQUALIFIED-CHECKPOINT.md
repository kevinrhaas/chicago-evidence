# UNQUALIFIED platform salvage owner guard checkpoint

Base: b37fdeca6b74d8e3c70945a75687140c0718f549 on existing PR 219.
Recovery/review artifact only. No platform feature push, activation, dispatch, merge or qualification.

Fix: owner-targeted Chicago contexts always archive private HEAD/WIP to steward/salvage/unqualified/<run-id>/<full-sha>. They never push the application PR source or create drafts. Dirty WIP uses a separate Git index and commit-tree preserving original history without changing the source branch, index, or working tree. All outcomes preserve WIP, including successful jobs. Default/detached targeted work may archive; default source refs never advance. Generic queue behavior is unchanged.

A success marker with exact ref/SHA is emitted and parsed into salvaged_branches only after normal nonforce push and exact ls-remote readback. Push or verification failures warn and never claim a journal archive.

Local proof: existing salvage checks remain intact; 46 real-Git checks PASS on CPU2 nice19, including private commits, staged/unstaged/deleted/untracked files, source/index invariance, already-pushed work, push rejection, remote verification failure, generic Chicago fast-forward + draft, target without resume, resume partial context, and default-source protection. Shell syntax + diff whitespace checks pass. Parent review and full required platform checks/smoke/hosted CI remain before feature publication/activation.
