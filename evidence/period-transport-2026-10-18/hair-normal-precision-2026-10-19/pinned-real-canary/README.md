# Authored-only Meshopt normal correction

Actual pinned CLI/core/functions/extensions4.5.0 tested; no Blender/browser/app edits. See receipt.json and reproducible canary.mjs (explicit local dependency adapter points at isolated npm cache). Tiny original skinned triangle includes the normalized direction underlying CI's [-92,-10,-86]/127 hair failure, unit weights, UVs, a named joint/IBM and a translation clip.

Real CLI outputs decoded through actual Meshopt decoder/NodeIO and then actual vendored Three BufferAttribute getX/Y/Z:
- default high: Int8 normal, length error0.005252806465905091, FAIL unchanged0.005 bar.
- high --quantize-normal16: identical failure; exact4.5.0 meshopt.ts:79 forcibly caps high precision at8 for octahedral filtering.
- --level medium --quantize-normal16: Int16 normalized, length error0.000002434157153174965, PASS.

`authored-normal16.patch` changes ONLY MODE=master's Meshopt invocation. Portable fixture invocation remains byte-identical. Source GLBs untouched. Container/runtime guard thresholds untouched. Medium retains EXT_meshopt_compression; it changes method from FILTER to QUANTIZE. Actual resident output sizes and full contract/render qualification therefore still require root's full gate/CI; no size budget acceptance is inferred from this tiny canary.

Canary asserts exact cross-output invariance for position storage, joint indices, inverse-bind matrices, node transforms, UV storage, weights and joint lists. Clip names/times unchanged. Initial exact high-vs-medium animation byte/value assertion failed: high's exponential filter rounds sourceFloat32 0.10000000149011612 to0.0999755859375; medium retains original sourceFloat32 exactly. Final canary explicitly asserts medium output clip equals original source clip exactly, and retains all three decoded clip receipts rather than concealing this difference. There is no claim all high/medium motion floats are identical. Resident hierarchy/raw-frame comparisons remain necessary, as already required by existing pipeline.

Initial local non-escalated npm/network and child spawn attempts hit EPERM; authorized isolated escalated tool execution succeeded. No automatic review rejection occurred.
