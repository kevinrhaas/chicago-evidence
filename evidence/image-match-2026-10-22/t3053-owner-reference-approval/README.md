# T-3053 recoverable source-approval update

The owner approved attributed project reference use of the school and first Tremont illustrations. Both catalogue records preserve the existing credits, links and historical limits and record the approval separately from any public-domain determination. Original matching tickets remain open.

Read checkpoint.json for the actual state. For the initial WIP archive only, decompress changes.patch.gz outside the checkout and inspect/apply it on the stated base with git apply after preserving existing work. Prefer a later pushed code branch or merged dev result if present. The patch is not a completed-match claim or a request to replace newer work.

The source update is pushed at `680e10c02b5f93f69852996e98c3fbc88fd04058` and PR #1224 targets dev. Full local reader-required preflight passed 1,047 steps, including 381 self-tests. Both published citation smoke slices passed 107/0. Prefer the pushed branch to the historical initial patch. CI/merge state is recorded in checkpoint.json.

PR #1224 MERGED to dev at 2026-10-23T02:45:21Z, commit `7a9123e9d6986fc3ea7b8912bd78f6278b0350f7`. Required GitHub gate and report passed on reviewed head `680e10c02b5f93f69852996e98c3fbc88fd04058`. Both approved source files are byte-identical on the merged tree; the integration lock is released. The original image-match tickets remain open. See github-merge-receipt.json and github-checks.json.
