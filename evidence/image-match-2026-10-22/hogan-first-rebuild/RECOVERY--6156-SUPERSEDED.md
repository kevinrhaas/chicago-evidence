# Recover Hogan's first picture-based rebuild

Read checkpoint.json for current state. This is an actual first geometry increment, with remaining image differences; do not close T-2377 on this archive. Prefer a later pushed code branch/PR or merged dev result if recorded. Initial recovery: preserve newer work, decompress changes.patch.gz outside the checkout, inspect it, and apply only on its stated base after git apply --check. The patch includes new source/docs/changelog plus rebuilt GLB/web derivative and manifests; no missing untracked source is required. Before/after and reviewed differences are copied alongside it. The source/rights/survival/camera limits remain in the handoff. No accepted camera, full smoke or merge is claimed by the initial WIP.


## Pushed PR and exact remaining work

Prefer code branch `steward/t2377-hogan-picture-match`, commit `6156a0367a2379f0d986b88c7c8236c4ebec0e55`, PR1229 into dev. Local strict-reader preflight passed1049steps; committed-diff changelog/ID checks passed; mobile and desktop published app/card checks passed. Six runs in smoke-runs.json cover all15parts at both viewports. Do not mistake one successful smoke check for allsix.

`merge-if-ready.py` is a guarded one-shot check/merge helper authorized by the owner’s instruction to merge completed PRs to dev. Copy it plus smoke-runs.json into `/tmp/t2377-model/` in an authenticated checkout before executing; it refuses a changed head, missing coverage or failed/pending runs, requires the current CI gate and clean mergeability, and pins the squash merge to the expected SHA. Inspect the actual GitHub state and lap ownership before using it. If any source changes, rerun appropriate gates/smoke for the new head.

After successful merge, save receipts, release `lap/pr-1229`, and release the T2377 claim with an explicit reason that only the first geometry increment landed and full matching remains open. Do not call ticket done while the comparison is differs. No production promotion is authorized here.
