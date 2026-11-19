# Exact af + pre-fire DEV validation candidate

Candidate commit: `539f09beb735e7555745566667140de72c44b796`.
Tree: `6b2c34dfa605a475fc9695abcfb2d0c0b019bb76`.
Parents: `af466d1638fda72a468ecd3ac22456844b870c1b` and `8c605db0571e29ee9da6d8aba5181451d9d84db8`.
Merge base: `69d9659ea09bcb8f87f9d9be9c475c657b6f5b8f`.

`git merge-tree --write-tree` succeeded without conflicts. The resulting 4D and .github trees exactly equal af; only the 47 pre-fire paths differ. The candidate is local, detached, unpushed. No real branch or origin/dev moved.

Worktree: `/workspace/chicago-af-prefire-validation`. Created with `--no-checkout`; it is deliberately not populated while the primary phone renderer owns local resources. Its empty working directory is not a failed clean-tree check.

## Scope

Full proof: `/tmp/t3656-dev8c-dependency-proof.json`.

All renderer, moving-frame, GPU upload-release, and offline-year-pack inputs remain identical to af for the upstream 8c delta. Preserve the actual original heads/runs on retained evidence. This is not a fresh source/renderer gate result.

The 4D publisher copies seven changed pre-fire viewer files (+69,236 bytes). Thirteen new media/provenance files (+16,865,001 bytes) remain served from root `/pre-fire/`, as every source/site twin is identical. Root pre-fire grows by 16,934,237 bytes including those viewer changes; a whole-site artifact containing both copies grows by 17,003,473 bytes. A GPU upload-release smoke does not measure that artifact's size.

## Targeted validation after explicit quiet window

Populate only this candidate worktree, install/attach the existing Node 22 runtime, and provide a real tickets clone. Do not touch `/workspace/chicago` or its generated mirror. Use a bounded foreground call and durable elapsed/exit receipt for every step.

From `chicago/4d`:

1. `bash tools/publish.sh`
2. `node tools/check_published.mjs`
3. `python3 tools/validate.py --site` (the CLI has no `--site-only`; this runs normal schema/provenance plus the site size/duplicate checks)
4. `bash ../pre_fire_v1/tools/publish.sh --check`
5. `node --input-type=module --check < ../pre_fire_v1/viewer/notebook.js` and equivalent for `research.js`

Afterward record the complete generated pre-fire file map/hashes, root-served configuration, 4D and whole-site total bytes, and final tracked status. Check generated viewer blobs against the exact 8c source blobs and ensure the new media were pruned from the 4D duplicate and remain present at the root. Preserve the publication log's input summaries. If any command fails, stop and report; do not edit budgets/assertions.

Status: all above execution is pending. No publisher, browser, full gate, workflow dispatch, or push occurred during preparation.
