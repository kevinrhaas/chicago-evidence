# T-3040 recoverable checkpoint

## Latest checkpoint: merged into dev

Code commit `7c1d95a801d18ba66f8ced83cb211bb0522f68d7` is pushed on
`steward/t3040-fort-reference-groups`; [PR #1218](https://github.com/kevinrhaas/chicago/pull/1218)
targets `dev`. Local preflight passed all 1,047 checks. Published smoke slices
passed 31 mobile and 107 desktop checks; the full renderer suite was not run.
GitHub CI passed and PR #1218 merged into `dev` at `e81cb09c3b9273c2989a891982101acbb814ca19` on 2026-10-23T00:35:18Z. The integration lock was released. Start from current `origin/dev` for the remaining model work. Read `latest.json` for the
exact state and retained validation logs. Prefer the pushed code to the older WIP
archive below; never apply that archive over newer work.

`unapplied-next-parcels/` preserves three agents' next proposals for T-2375,
T-2377 and T-2388, each with evidence and remaining validation. All passed
`git apply --check` against the checkpoint source. They have not been applied,
baked, visually validated or claimed as picture matches. Review provenance and
current code before use; keep those original tickets open until their full gates
pass. All 17 ticket findings and both actual fort comparisons are in the code
research document linked by `latest.json`.

## Earlier WIP recovery archive

WIP, not a green or completed model-match claim. Six agents reviewed T-2372 through T-2388; findings are in the archived docs/RESEARCH/fort-reference-groups-T-3040/README.md and on the tickets.

The code prerequisite renders complete fort groups and fingerprints every member mesh and placement. Both actual baselines say differs. T-3041 and T-2388 retain the matching work.

To recover: inspect and preserve the existing code worktree first. On the checkpoint base_commit from checkpoint.json, extract work-in-progress.tar.gz outside the checkout, apply changes.patch with git apply, then copy new-files/ into the code checkout, preserving its paths. Never overwrite existing user changes blindly. Install/start instructions are saved in the environment draft; use a physical sparse tickets clone (not a symlink). No credentials are included.

Full preflight was still running when this checkpoint was saved. Read checkpoint.json and run the remaining checks before committing code, opening the PR, or merging dev. The archive is a recovery artifact, not a request to revert newer work.
