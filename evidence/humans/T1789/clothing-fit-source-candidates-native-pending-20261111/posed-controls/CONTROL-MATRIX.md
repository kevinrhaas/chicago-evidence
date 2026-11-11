# Clothing layer controls prepared on 11 November 2026

The eleven small controls passed in 0.618788 seconds under the original
120-second supervisor, resource guard and cleanup rules. They qualify the
math controls only. No new garment was baked, exported, loaded in the native
renderer, visually accepted or declared free of clipping.

`skin_interpolation_controls.py` demonstrates an important failure case: a
2.8 mm bind-pose overlay becomes **23.17 mm inward** relative to its supporting
triangle under an adversarial pair of 15-degree joint rotations. Positions and
skin weights interpolated separately are not a general attachment to the posed
support surface. This synthetic case is not a measurement of a project figure.

`triangle_contact_controls.py` loads only the original scalar `axes` and
`separation` functions from the SHA-pinned historical source. Crossing edges,
coplanar contacts, legitimate separation and malformed inputs are controlled.
The result is a separating-axis gap; it is never called an MTD or penetration
depth. The historical rigid-door interval bound is **not applicable** to
arbitrary skinned cloth deformation and is not imported.

## Actual targets and remaining checks

| Owner observation | Actual source targets | Required checks after canonical bake |
|---|---|---|
| Coachman trousers through coat | `nelson_charles_1904_coachman`, actual breeches versus complete livery coat/skirt | Indexed posed triangle contacts; intended front coverage; near-front skirt self contacts; waist/seam continuity |
| Women's clothing through aprons | `flynn_mary_1835_dress_study`, `williamson_mattie_1904_cook_study`, `reynolds_mary_1904_maid`, `ryan_kate_1904_cook` | Actual dress/bodice versus apron skirt/bib; outline coverage; support correspondence and boundary skin interpolation; no independent-LOD bridges |
| Janky shirt collars | Existing collar-band users identified by the collar writer | Rim topology/levelness in rest pose; actual collar versus neck/shirt/coat during native clips and any actual runtime neck motions; check mixed skin weights |
| Military stripes/trim breaking through | `private_first_infantry_1812` crossbelts and actual officer `on_faces`/epaulette trim where emitted | Actual trim versus uniform; trim-to-trim crossing and physical edge returns; no assumption that matching interpolated weights preserves the uniform surface |
| Linen trousers showing the rear body cleft | `settler_1812`, `loose_trousers` / `garment_lower__trousers_linen_1810` | Body versus trousers contacts/coverage, rear silhouette and section ease throughout the actual walk/idle cycles, and a supported seated variant only if one exists |

The exact woman and military figure seen by the user are not established by
this audit. The named targets come from the committed recipes, not a guessed
identification of the user's view.

## Native adapter requirements

1. Bind every input to its actual emitted GLB SHA256, source recipe/constructor
   revision, loader revision, material/primitive identity and LOD. Compare
   native skinned **world positions**, including the actual bind and world
   transforms, rather than unrelated local POSITION streams.
2. Inventory the native clips. Read-only headers of the preserved 9b6 LOD0
   coachman, maid, private and settler show `idle` and `walk`, not a seated or
   turn animation. Sample their actual key times, interstitial times and the
   runtime's real transitions/blends. A rigid whole-figure yaw alone cannot
   change the internal intersections. Do not invent absent skeletal clips.
3. Evaluate every relevant exported LOD. `human_teamster_blend.object_mesh`
   currently applies independent DECIMATE modifiers to clothing components;
   source support correspondence is not a certificate of the emitted LODs.
4. Use conservative triangle AABB/spatial candidates without losing any pair,
   then the original scalar contact predicate. Report asset, file hash, LOD,
   clip/time and both actual mesh/triangle IDs for every first witness.
5. Distinguish intended topological seams from layer crossings through an
   explicit, narrow source-bound seam contract. Do not exempt a whole material,
   body region, mesh pair or contact class. A coverage hole can expose clothing
   without any triangle intersection, so coverage checks remain separate.
6. Include actual viewport inspection while the figure moves. The small source
   predicates do not evaluate normal shading, collar style, texture quality or
   photographic appearance. Sampled tests do not establish between-sample
   continuous-motion safety; state that limit rather than reusing the rigid
   door certificate.

## Military source audit

The private's `_on_garment` helper clips the coat surface and interpolates new
positions and weights independently. Officer `on_faces` and epaulette pieces
reuse it. The canonical builder then decimates components independently.
These are concrete mechanisms that require posed/native verification; the
current audit has not measured the user's exact stripe intersection.

There is also a nominal layer-spacing warning: the private's crossbelt offsets
are 2.8 and 4.2 mm, a difference of 1.4 mm, while the merged belt boundaries have
1.8 mm inward physical returns. That **0.4 mm nominal deficit is not an actual
triangle intersection measurement** on the curved garment. Check the real
crossing and its posed returns before choosing or claiming a geometry fix.

## Independent source reviews delivered

The coachman candidate initially had two actionable defects: a same-envelope
angular overlap that could self-cross, and a radial-column diagnostic described
too strongly as triangle clearance. The writer replaced it with a single closed
ring and explicitly labeled the radial diagnostic and native limits. The
corrected source has no further blocker found in this bounded review.

The apron helper removes independent-grid bridges and preserves support basis
metadata. No blocker was found in that scoped source claim. Actual front-outline
coverage still needs a real-body check, especially where the whole-face front
plane filter discards a triangle that crosses that plane.

Actual body construction, native exports, pose contact tests and visual approval
remain pending for all next-piece candidates. PR1928's current gate is unchanged.
