# PR 1649 final memory repairs and driver preparation, 3 November 2026

This preserves **uncommitted** latest-DEV integration TREE `ef566b993dd2bfe76eea419c750aa01e7acec263`, with app parents `ae762df51dad3bd48e7d5307e0bda3cd0ce05e31` and `92bee8bdb89a900a840bcd94e760bb8f21c757c2`. It also preserves a separate **unadopted** seated-driver motion proposal. No app commit, DEV merge, full-gate pass, photographic acceptance or ticket completion is claimed.

## Public recovery chain

Keep the prior packet `evidence/transport-pr1649-memory-repairs-2026-11-03-2000Z` from chicago-evidence commit `c7dfeb97ea67fa24977703d330ecd62e31750d9d`, and its own required prior packet `evidence/transport-pr1649-recovery-2026-11-03-1935Z` from commit `0b7d232b7c232cee0927ecb6a40dcc30d2cc6fe7`, beside this folder. Their pinned manifests and exact object dependencies are recorded in the recovery maps. Fetch all public app-parent commits named in the chain. `RECOVERY-RECIPE/recover_tree.py` verifies the dependency chain and reconstructs the exact new tree without changing an index or checkout. Its actual isolated roundtrip is included. Only four additional novel blobs are included; no Mayer model, incoming PBR asset, or prior blob pack is duplicated.

## Measured memory and current gate

The actual original native phone gate passed **both 1904 and 1812** on intermediate TREE `5ede9050327ea24598a693d3e9ab4fae6d132722`: 418432890 and 233346945 bytes respectively. Original 180/120/600-second stage caps, source bindings, resource and cleanup receipts are included. That pass is not retargeted to the newer `ef566` source. The newer incoming DEV change adds 23304 decoded accessor bytes; all sixteen compared images are byte-identical. Its own memory gate remained unmeasured at this cutoff.

Latest-source preservation verified 228 own and 197 incoming one-sided paths and all ten saved custom blobs. The latest native owners passed, yielding 987 Liberties. The fresh four-part preflight was still active; its cutoff and any individually closed parts are included without claiming an all-four pass.

## Separate driver proposal

`DRIVER-UNADOPTED/` includes exact producer code and recipes, patches, eight output hashes and actual derivation, native 1032-phase proof, full native 24-file browser fixture result, canonical owner tail, writer and isolation controls. Original failed jaw-scope and sparse-owner attempts are retained. The older ADOPTION-PREP pending-tail label is historical; owners-02 contains the subsequent actual passing tail.

The41MB generated GLBs and installed node dependencies are deliberately omitted. To regenerate, use an isolated clone containing public parent `ae762df51dad3bd48e7d5307e0bda3cd0ce05e31`, copy the two exact producer modules and the seated-driver-look-v2 recipe from `EXACT-PRODUCER-AND-RECIPES/` into their corresponding `chicago/4d/` paths, then run `python3 tools/human_seated_look.py --output FRESH_DIRECTORY` from `chicago/4d`. The recipe pins all eight public parent assets. Verify every generated file against `generated/DERIVATION.json`. The saved actual generation took1.463seconds at its original5second cap; fetching missing public parent blobs is a separate setup step. Review the complete authored/native patch before any adoption, and regenerate derived files on the receiving source.

Files over512KiB may be stored with lossless gzip; COPY-ORIGINS records their original names, byte counts and hashes. No driver asset or runtime code is adopted by this evidence publication.
