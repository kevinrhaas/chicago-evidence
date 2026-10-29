# Read-only railway CPU release proposal

Checked source remains9e14c138848ef854a535271fbd3feaae52dd4aa2, unchanged. The supplied native baseline is1,184,409,779B: historical1125MiB is exceeded by4,761,779B. Array-buffer backing is558,704,654B. The railway alone retains65,745,432B CPU geometry, alongside its GPU geometry. The proposed one-code-line change enables its existing upload-release callback on desktop as well as phone; it changes neither mesh/profile/reach/count nor texture/material/lighting quality. Savings are not measured or promised.

## Source safety references

- main.js2322 currently enables railway onGeometry only for coarse devices. railway.js1070–1100 calls this hook after each new near/far rail geometry, so later zones are covered too. Initial railway.update is at main.js2328; desktop continues its ordinary renders, with no forced extra uploads.
- upload-release.js RELEASE_KEEP.railway=[] explicitly supports this layer. markLayer skips instanced geometry and dynamic positions, prepares bounds (including every active BatchedMesh geometry), caches confidenceRange, and only drops static attribute arrays from native onUpload callbacks. BatchedMesh index keeps an empty array of the same type.
- railway.js1211–1231 pickAt marches the ray against retained terrain and station strips/nearestTrack, with no mesh-raycast/vertex-array read. Its grade line/profile/track metadata remain retained.
- railway.js1070–1185 creates new near/far geometries from paths/sections when reached, disposes them when far away, and changes detail by reaches/instance counts. No post-upload vertex/color rewrite was found; shape/wet-color/UV setup occurs during construction.
- main.js1445 and2793 restrict farMerge to furniture layers, excluding railway. createViewOcclusion may target railway ground batches, but its target path (view-occlusion.js404–428) reads cached bounding boxes and instance matrices; backingTriangles is collected from buildings, not railway. Cached bounds are established before release.
- Confidence and season use material uniforms/shader switches. confidence.js561 explicitly falls back to cached confidenceRange after array release; upload-release.js133 records it. No railway per-vertex grade mutation or production confidence.census call was found. main.js2379 patches rail seasonal materials without changing geometry.
- main.js1923–1925 already requests normal context reload when any geometry/image/compressed levels were released. Desktop baseline already released51 compressed sources, so recovery already follows that path. crash-guard.js259–292 performs one ordinary reload on first restore, then retained stepdown behavior on repeated losses. New rail arrays would not have to be rehydrated in-place; boot rebuilds them from source/retained data as before.

## Remaining proof before any acceptance

This is source audit only. Later run the unchanged native memory meter at the same1904spawn/viewports/tiers, with no snapshot/GPU instrumentation overhead beyond its native meter. Actual byte saving must beat the historical1125MiB goal with useful margin. Inspect genuine Full rendering, rail analytic picks (ground, track and edge), confidence/ghost/hide states and seasonal shader changes, near→far→near zones, Full/Balanced/Full switching, and actual context loss→one normal reload plus usable restored frame. Require zero browser/GL errors and preserved geometry/counts/source integrity. No assertion/cap loosening or rendered-detail reduction.

## Existing smoke map on checked9e

The actual native smoke_budget.mjs --for-diff c0936cb192873b8c09a747e4ed3d64b3c6f5115c result maps this diff to ALL parts1–15 at BOTH widths.14paths are outside its map; broad authored-asset and boot-chain rules also select all. Therefore the existing map does not justify excluding UI13. It emitted13mobile+15desktop commands, saved verbatim. Their cost figures are historical/mean prices: mobile13 and many other parts have no individual measurement; desktop13 is estimated8m15s, whereas an earlier actual C3 desktop13 took88m06. Those prices are not current runtime promises. No smoke was launched.
