# Research-site delivery: PR 2206 merged

PR [2206](https://github.com/kevinrhaas/chicago/pull/2206) was squash-merged into dev at `8c605db0571e29ee9da6d8aba5181451d9d84db8`. The independently prepared branch on actual dev changed exactly 47 pre-fire source/site paths, all identical to the reviewed recovery version; its tree equals the merged tree. The 4D application subtree is unchanged from the dev base. No duplicate source images were copied here.

Actual-dev notebook smoke passed 138 checks and dossier smoke passed 57; the handoff records deterministic builds and tracked mirror parity. The original HANDOFF predates PR creation/merge, so its ready-for-review wording is historical. The later review and merge API result establish delivery. Root's live review found no branch rules requiring a gate and no applicable 4D-only source gate; the sole queued check was an administrative stuck-PR report, not a failed or incomplete website validation gate. These records do not claim a production deployment.

Baseline PR 2198 remains draft/unmerged with required 4D source and browser checks incomplete. The research-site merge does not provide that acceptance. Its source/runtime is separately frozen at822; model v2 remains an unplaced candidate with all three image comparisons differs.
