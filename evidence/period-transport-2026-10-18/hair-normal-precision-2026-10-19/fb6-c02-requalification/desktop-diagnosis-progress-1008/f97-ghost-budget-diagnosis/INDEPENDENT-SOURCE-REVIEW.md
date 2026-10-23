# Independent source review: ghost draw budget

Actual failure is 331 calls against unchanged 330. No source correction is justified from that aggregate alone. At this review snapshot, this directory has no successful object/pass trace: run-512f4a7e3-bind-failure.json says EPERM listening on127.0.0.1, stopped before browser, no draw measurements. No new browser, app edit, CI, or test execution was performed by this reviewer.

Confirmed current confidence.js behavior:

- `render` excludes all-ghost ordinary objects/batch instances from opaque work where it can safely do so; mixed-grade geometry can legitimately participate in both passes. Furniture already uses the documented opaque-pass dither route.
- `renderGhost` sets the ghost camera layer, clears scene background, disables shadow updates and info auto-reset, then restores material, visibility, mask, background and renderer flags in finally. Summing opaque plus ghost calls is intentional; the 330 bar remains real.
- Unknown `_confidence` ranges conservatively participate in both passes. A trace must establish an actual eligible empty draw before replacing that conservative behavior; object-count estimates are not draw proof.

One concrete source mechanism worth checking, not an optimization recommendation: ghostTwin makes the inherited material transparent. Pinned Three185 renderObject (three.module.js around18127) performs TWO renderBufferDirect calls for transparent DoubleSide material with forceSinglePass=false, temporarily setting BackSide then FrontSide. Thus repeated same-object/group rows could be actual two-sided blending, not a duplicate confidence-plan defect. Need the actual material.side, forceSinglePass, transparent/depthWrite values and object geometry/pass in the trace. An unconditional single-pass or side suppression can change visible volumetric overlap, so is not an accepted fix.

A defensible next source correction needs trace evidence of one of: a submitted group/range containing no ghost-grade fragments; a batched instance not actually eligible; duplicated identical draw submission beyond required face/pass semantics; or compatible material/geometry batches that can merge without changing visibility or shadow policy. Then verify exact existing strict330 and visible output against the relevant state. If every submitted call is necessary, no optimization is established yet. Do not weaken330, skip the failure, reclassify content as dither without a feature decision, or declare the diagnostic an exact reproduction of70minutes of CI residency.

Instrumentation note sent to environment-validation: currently prepared trace records object/materialtype/group/pass but not material side/forceSinglePass. Enrich only if needed under root control; this reviewer did not edit the harness or run it.
