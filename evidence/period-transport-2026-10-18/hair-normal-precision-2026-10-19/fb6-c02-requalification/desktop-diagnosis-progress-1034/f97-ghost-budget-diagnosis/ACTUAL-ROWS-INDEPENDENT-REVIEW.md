# Actual held trace: no demonstrated redundant draw

Actual run-512f-held-v2 row-ghost cold reports327 calls, instrumentationValid=true and traced sum327, against unchanged330. Breakdown:199 opaque main,80 shadow,48 ghost. Ghost layer counts:flora12,terrain10,structures10,trees6,yard-ground5,streets2,signage2,working_bank1. Snapshot with actual ghost rows is independent-row-ghost-cold-analysis.json.

All ghost draws have group=null and no geometry groups. Thus the proposed multimaterial-group eligibility optimization has NO actual candidate in this frame. The only grouped main geometry in tint is sky with a single material/null actualgroup, to which group filtering would not apply.

BackSide/FrontSide call pairs are concretely confirmed for six flora meshes, five merged structure meshes, two tree foliage meshes and signage. These match pinned Three's transparent DoubleSide two-pass behavior, not an unexplained duplicated confidence-plan submission. Other actual ghost draws are single-pass, including streets with forceSinglePass=true.

Changing these pairs to single-pass preserves submitted triangles but can change alpha ordering for overlapping front/back surfaces. It requires geometry-specific proof and actual visual comparison, not an assertion that every second draw is redundant. In particular volumetric merged buildings are not safely treated as flat cards. No forceSinglePass/dither/content suppression patch is justified by this review.

This fresh runtime sample passes330 and does not reproduce the earlier331. It cannot attribute the difference to a particular feature or prove the historical failure was spurious. Further source optimization requires an actual fully discarded object/range, safe batching equivalence, or geometry-specific transparency proof. Keep330 and visible content intact. No browser, app, CI, thresholds or scene geometry changed by this reviewer.
