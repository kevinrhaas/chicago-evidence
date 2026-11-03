# PR1631 static delivery verified on public dev

The merged Wolf/Sauganash increment is now verified in the public **dev integration preview**. Root verified actual public bytes at **2026-11-03 04:18:25 UTC**: build `1f8a67ca` is a descendant of PR1631 merge `18c037e9f756a5190787ef1bd77bacce78331ad1`, six commits ahead. Exact fetched build metadata, GitHub ancestry comparison, Sauganash sidecar/WEB model and compiled pictures index are preserved under `public-delivery/`.

Live preview links:
- https://chicago.polecat.live/4d/dev/walk/?structure=sauganash_hotel
- https://chicago.polecat.live/4d/dev/walk/?structure=wolf_point_tavern

The shipped Sauganash WEB is exactly 38,168 bytes, SHA256 `5f7d8a54f1c805d53bdb558506dc18ce237c9c0fb180a7cd274dec7d64ad480e`. All six expected Wolf credited picture IDs are present in the public compiled index: Andreas, anonymous pair, Colbert/Chamberlin, Miller/Davis, Widney/Hammon and Blanchard/Shober. This independently packaged evidence rechecks the saved public model hash/length, six IDs and recorded ancestry before publication.

This is **STATIC DELIVERY verification** of the current observed public dev build. Actual UI and native stage-3 qualification remains bound to final source head `0e838b35b5ba32b61ccd01499310520e160ab4a2`, with 107 mobile and 107 desktop checks passed, zero failures/page errors and closed process/source/Git guards. That runtime proof does not automatically qualify later core code in build 1f8a. No new browser/native smoke ran to create this delivery checkpoint. Production at `/4d/` is separate and promotion is not claimed.

The final head-bound runtime proof: https://github.com/kevinrhaas/chicago-evidence/blob/121eaee6e28f74696131cfd71850e26c8cc259b1/evidence/wolf-sauganash-2026-11-03/0e838b35b5ba-final-default-visitor/RECOVERY.md . The exact protected merge/CI handoff: https://github.com/kevinrhaas/chicago-evidence/blob/5978c78ffad4bcce2f8d5cd8c1d950729d1de3d1/evidence/wolf-sauganash-2026-11-03/merged-1631/RECOVERY.md . The earlier handoff correctly said deployment pending at its observation time and remains unchanged.

Root subsequently released T-2383 and T-2386 as **partial/open**, with merge and proof links, through the native ticket CLI in chicago-tickets commit `e085b17f7e5898d3c0a434c0d2b989eaaccda25f`. Its independently fetched public GitHub commit receipt is included. Neither full hotel/compound matching nor Wolf full reference coverage is declared done. Overall original scope remains **9 of 17 completed**, eight unfinished. No door-traversal, full-hotel signoff or Wolf 3D/street-frame claim is added by static delivery.

Green Tree continuation is owned by its agent on a new branch, with exclusive canonical source and ticket-clone ownership coordinated by root. The next prepared packet is https://github.com/kevinrhaas/chicago-evidence/blob/e1c2de29d477bb2441b7b699f82886c82046426a/evidence/green-tree-2026-11-03/combined-0e838b35-consumers/RECOVERY.md . These delivery receipts grant no competing writer/read lease on that checkout.

This checkpoint accessed only closed external delivery files and a public GitHub ticket-commit endpoint. It read or wrote no canonical checkout/Git/app-publication data, mutated no tickets, and left the historical image store and all older evidence untouched. Publication is additive to chicago-evidence by normal fast-forward and exact blob readback. Extract checkpoint.tar.gz and verify archive.json plus CLOSED-MANIFEST.json before continuation.
