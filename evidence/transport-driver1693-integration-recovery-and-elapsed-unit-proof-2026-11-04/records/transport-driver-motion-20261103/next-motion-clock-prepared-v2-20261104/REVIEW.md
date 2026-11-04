# V2 preparation — independent visual admission

V1 is unchanged. V2 is prepared outside APP, unexecuted and unapplied.

The sole runtime difference from V1 is the town visual-call guard:
`if (!elapsedFrame || motionFrame) actor.updateVisual?.(...)`.
Production main always opts into elapsedFrame:true. Its synthetic lastUpdate
refreshes therefore neither call nor prime the driver visual clock. Real frames
still call that independent clock once, including while the journey is stopped.

The existing bounded-dt legacy contract remains unchanged, including all original
test assertions and the original legacy Light-restoration expectation. This is
an explicit production elapsed-frame guarantee, not a universal change to every
legacy dt caller.

The acceptance patch adds an actual createDrivenAssembly/town regression,
alongside V1's controller and native main-clock tests. It checks synthetic new
admission, stopped visual calls, Continue, synthetic range return and Light
restoration. First actual restored frame consumes zero; the next consumes .125s.
It uses real adapters with test Three nodes, not a copied adapter implementation.

V1-V2-REVIEW.diff and SOURCE-PINS.json make the exact refinement reviewable.
No browser, Node test, native gate, app modification, or asset write was run.
