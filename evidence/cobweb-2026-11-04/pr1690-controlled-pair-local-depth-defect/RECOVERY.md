# Cobweb PR1690: controlled pixels reveal a local aperture-depth defect

Two real renders of the committed before and after MASTERs were made with the existing project `photo_match.mjs`. The root-approved private camera, original source image, tool files and all scene settings stayed fixed; only the GLB changed. This is an **unsolved diagnostic camera**, not a calibrated historic view or an accepted image match.

Before: `af1f33c0f5d75fc8c40e6cbb589adfd7d29d551572c2775e236bb260f6ee561f`. After: `4f42207be5fcb2391fda58672ce8442b02aba9510f3096db8c2934b695fe7bea`, the actual PR1690 MASTER. Camera SHA256 `07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977`; source SHA256 `624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f`.

The aperture count visibly improves: an upper dark rectangle appears, and two lower rectangles replace the former central door. **Both lower rectangles, however, have visible horizontal log courses across them.** They read as striped surfaces rather than unobstructed neutral recesses. The upper mark is clear. The unchanged massing and unresolved wider source differences remain evident.

The source diagnosis is narrow and concrete. `openings.surround` places the inner reveal at `w.skin + back`; the new direct `openings.face` call places the dark surface at `back` alone. Here the wall skin is 0.022m. The lower dark face is therefore at9.004m, behind the log skin at9.022m, while its own reveal ends at9.026m. Passing `w.skin + APERTURE_BACK_M` to that local face call is the consistent repair candidate. No code was changed and no fix is claimed; genuine native rebuilding and a new comparison must verify it.

The full source image was not edited. The three analysis crops use the **same pre-existing crop rectangle** `[1380,330,1500,420]` and nearest-neighbor8× enlargement, with no new fit, enhancement or annotation. Full composite and bare render outputs are also retained. Original camera prose still carries its historical “unrun candidate” label because its bytes were preserved; these two renders have now actually run, while the camera remains unsolved.

Successful pass times were65.4s and5.1s. The protected controller ended exit0 with all children reaped and no leftovers. An earlier browser launch failed because the long external TMPDIR exceeded the Unix socket-path limit; that failure is retained, and a short task-specific external TMPDIR repaired setup without editing project tools. All match/output writes stayed in the private external fixture. No app source, canonical camera, grade, match verdict or ticket/PR ownership was changed. Both private match records remain unreviewed.

The live native worker still owns the candidate; this receipt is for the parent reviewer to coordinate a bounded repair, not permission to steal its branch or claim. Native82 execution, final source gates, current-dev integration, actual application checks and named full gate still need their own final receipts.

Initial independent scope/GLB audit: https://github.com/kevinrhaas/chicago-evidence/blob/aa684df2e799570571eb367b9dfaf515e64b684b/evidence/cobweb-2026-11-04/pr1690-live-f6-independent-scope-and-glb/RECOVERY.md
