# Terrain Ghost performance: finite source finding, no safe quick patch

Exact source2aebef95. No app/index/mirror/CI/browser writes. Root's actualV4b paired observer remains owner; this review takes a NONTERMINAL snapshot only and neither replaces nor qualifies its final receipt. No source, budget, counter or UI policy patch is prepared.

## Concrete actual attribution

The new arm's source-derived Hogan pose reads NORMAL3695, Xray8223, reconstructedGhost40%8466 actual primary GL draws, each equal to the shipped counter, with pickingGL0, extra0, residual0 and GLerror0. Xray exactly reproduces the historical CI8223. Ghost40 is3draws below historical8469, so it is not called an exact reproduction. Parent was not yet complete in this snapshot. The previously held GPU-pick preservation correction is unrelated to these measured samples and remainsHELD; it does not justify changing this counter reading.

Terrain NORMAL186draws/13commands. Xray terrain contributes1opaque plus3908ghost draws in12ghostcommands/12objects. The dominant ghost object is the distant base:3652draw entries,7503instances, transparenttrue, existing coalescerinstalled,0additional eligible neighbouring entries. NORMAL's base has96already-coalesced entries. Ghost40 draws the base in both opaque96 and ghost3652. These are real submissions, not a renderer.info accounting artifact or a missing wrapper. The per-pass actual counter proof matters more than the ordinary-view calibration.

## forceSinglePass is inapplicable

terrain.js2532–2537 creates a default FrontSide MeshStandardMaterial, without a DoubleSide setting anywhere in this module. The same groundMaterial factory supplies detailed ground, apron and base; groundMat is patched at475, baseMat at662–666. Source/prebuilt geometry receives this newly constructed material, not a material from a GLB. terrain.js1438–1469 prebuiltGroundTiles calls batchPieces with that material. The ghost twin inherits side and changes transparency/depthWrite/defines; it does not change FrontSide to DoubleSide.

Thus the measured terrain already submits one ghost command per object. Three's transparent DoubleSide two-pass branch does not apply. Setting forceSinglePass on this heightfield material would not remove a draw. Closed structures' DoubleSide behavior is a different case; no global twin flag is warranted.

## Why the existing coalescer loses the saving

spatial-batch.js partitions complete original triangles by40m centroid cells, preserving exact attributes/winding; each piece receives an identity instance. batchPieces always installs coalesceRuns. Both prebuilt base replay and source-built replacement use it. Base geometry retains its world-space coordinates; its mesh drops3cm, receives but does not cast shadow.

The normal opaque joiner may group touching source index ranges with identical matrix/colour, placing each run where its nearest member appeared. In the ghost twin transparent=true/depthWrite=false, Three sorts instances back to front and joinRuns deliberately selects joinNeighbours, which only combines ranges already adjacent in the real sorted list. The actual base's sorted sequence has no eligible contiguous neighbours. That rule preserves its current transparent triangle order; removing the guard would change it. Adding another identical wrapper would not create eligible ranges.

## Heightfield construction does NOT prove arbitrary transparent reorder safe

terrain.js1751ff and terrain-base.js adaptiveGroundGrid construct one varying-Y surface over X/Z, with upward winding (a,b,c and b,d,c); refined/coarse neighbours share samples. The field and its outward apron are not a closed solid. This proves one ground height in plan, not one front-facing fragment per screen pixel at an oblique camera. A sloping ray may cross multiple rises/banks of a single-valued heightfield. Back-face culling does not by itself exclude multiple front-facing intersections along that ray. Open topology therefore does not establish order-independent alpha compositing.

The base is not coplanar by constructor: each vertex samples the actual heightfield, adaptive refinement is driven by crossing overrun, and its metadata reports112refined cells/115086triangles. It is drawn below detailed ground, but a near-hole fragment discard/cut/opaque depth test does not prove that every potentially overlapping base fragment disappears. Confidence preserves the material's original spatially varying prairie/season/normal/shadow shading; it only adjusts late alpha and grade tint. Different visible fragments can have different RGB. Alpha blending of those colours is order-dependent. Even a single prescribed opacity does not make it commutative.

Accordingly `groundBase.sortObjects=false`, opaque-style run joining under a transparent twin, a generic ground-only forceSinglePass toggle, or wholesale Ghost-to-dither are not justified fixes. No actual buffer triangle projection/pixel nonoverlap audit ran; no assumption is relabelled as that proof. Metadata records are saved honestly as index metadata, not decoded mesh/overlap validation.

## Safe alternative in principle, unsuitable as a quick patch

A separately designed index-repack submission could preserve the exact sorted triangle sequence while concatenating selected original index spans into one contiguous index buffer, then draw identical identity-instance data once. For this base the original per-piece transforms are identity and owner tables absent; confidence is per vertex. That is a plausible order-preserving algorithm rather than a proof of an existing implementation. It would still need strict attribute/transform/material eligibility, original/cull/hidden-index equality, explicit tests for blending order and all modes, live pixel/picking/error comparisons and frame/memory measurement. Released index arrays must be retained or reacquired; the current runtime deliberately discards those CPU copies. Full base115086triangles implies up to1381032bytes for a32bit complete index order before scratch/cache and repeated upload costs. This is not free, and screen-picking/world loops must not silently inherit it. No implementation, new test, buffer sweep or browser run was prepared, per root's finite stop instruction.

## Calibration gap, not a silent assertion waiver

Exact main.js1371–1388 documents T2970's rebase from rendererCalls to true driver draws: six ordinary gate stands, worst desktopFull7358/mobile5898, about5% rounded to7800. That calibration does not price these confidence modes. The failure is a measured additional mode cost from order-preserving transparent draws, not evidence that the new fifteen near wagons themselves caused423/669excess; all three parked wagons are outside reach at this measured pose. Any consciously measured budget/tier policy decision belongs to root's subsequent complete evidence and project rules. This source review does not prepare one, alter Light, substitute rendererCalls, dismiss the failed CI, or authorize merging red.

Finite stopping point: terrain forceSinglePass refuted; unconditional transparent reorder unproven; order-preserving index repack deferred. Save root's final paired receipt separately when it actually terminates.
