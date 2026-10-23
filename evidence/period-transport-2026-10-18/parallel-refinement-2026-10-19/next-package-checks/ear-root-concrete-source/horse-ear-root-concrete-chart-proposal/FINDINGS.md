# Concrete source chart — requires reviewed18→22 cut-knot amendment

No model or GLB was generated, no source geometry was edited, and no browser ran. All coordinates below are read-only construction recipes pinned to horse090be8fdc2516ee5b5c8f886026f441850cc208f17b6ede71fed9007ab80f12f and its existing source arrays. Existing failed archives/statuses are unchanged.

The first vertical-Y projection was not feasible: actual retained ear-loop corners can lie laterally outside the bounded upper skull chart. failed_vertical_projection.py preserves that failed construction. No ear shrink or arbitrary coordinate adjustment repairs it here.

Concrete successful source-map construction

The actual centroid of original24vertex skull ring1 supplies an internal projection focus (approximately[0,.015,.02], exact value stored per side). Each actual retained18-edge ear cross section lies in a constant-Y plane. Rays from this focus through the actual leaf boundary intersect the original upper skull triangles. Perspective barycentrics are corrected into original source barycentrics, so each returned point lies on its claimed original triangle. No scalp vertex is moved. CONCRETE-CHART.json contains the18 actual projected corner positions per side, their source face IDs/three barycentric coefficients, original ear-loop corner ownership, ordered correspondence and the complete conforming cut sequence.

The natural18-corner cut crosses four existing skull edges per side. A surface-conforming cut therefore needs22 boundary knots, not18. Treating the18 points as straight3D edges would leave four segments crossing old facets without a shared knot; that would not be an exact source-surface cut. This is the smallest requested contract amendment: allow a22edge skull boundary connected to the EXISTING18edge leaf boundary with an unequal-ring annular triangulation. Do not move/split the visible upper leaf ring to force equal counts. No protected48vertex attribute change or wider skull region is requested.

Exact affected cohorts

Right(-X): source skull faces16,17,19; actual coat primitive0 triangles2044,2045,2047. Left(+X): source skull faces4,6,7; actual triangles2032,2034,2035. None is fully consumed by the cut. Each original triangle requires a constrained planar complement split; original protected vertices/edge positions, weights and normals remain exact. Original full triangle indices are replaced by that complement, not simply deleted. ACTUAL-FACE-COHORTS.json gives original source/emitted vertex IDs.

The existing ear retirement tables remain those in the prior proposal:56 outer/rim and32 concave root faces per side, with upper leaf position/index/weight protection and declared cut-ring normal halo. All other skull faces, orbital/nasal/lip geometry, ears above the root band, body/lower limb/soles, rig/rest/IBMs/sockets/clips and gear are protected. Old48portal/band attribute vectors remain exact even though some incident planar faces are split.

Measured static source-chart checks

Both actual projected18edge outlines are simple: zero strict edge crossings and minimum nonadjacent projected edge separation4.619337mm. Each footprint triangulates into16 triangles. Clipping against ALL eligible original upper chart faces covers its area exactly to<2e-19m² and gives zero overlapping projected face interiors within the footprint. Thus the skull projection is globally injective over this specific cut region, not merely positive-area per triangle. Source coverage is not claimed outside the footprint.

Exact piecewise3D cut segments stay at least76.994835mm(right) and66.712130mm(left) from the rear24edge portal segments. Minimum cut-segment distance to any of the48 protected vertices is10.338621mm(right) and21.863880mm(left). These are actual segment-to-segment/point minima, not just corner samples. They do not by themselves establish a shaded normal halo or posed clearance.

Minimum source leaf-plane to skull intersection Y gap at the18 corners is9.194103mm(right)/15.569570mm(left). Four extra source-edge knots retain their explicit correspondence s=i+t on the original leaf boundary. Their source barycentric ownership is stored. No arbitrary polygon scaling is used.

Injective bridge parameterization condition (not an implemented mesh)

For original leaf-edge parameter s, let L(s) be its piecewise-linear position, C the source-derived focus and K(s)=C+rho(s)(L(s)-C) the exact ray/skull intersection. All participating rays have positive Y direction from C, rho(s) is continuous and strictly0<rho<1, and central projection onto the leaf plane is globally one-to-one around the simple boundary. The ruled annulus B(s,u)=C+[(1-u)rho(s)+u](L(s)-C) is then injective at rest: projection fixes s, and the strictly increasing radial factor fixes u. This does NOT prove a discrete triangulation or skinned animation.

At each leaf edge, source-edge knots divide its lower boundary into a short polygonal chain; its upper boundary remains one original ear edge. Triangulate that patch within the plane through C and the leaf edge, preserving cyclic order and the exact lower22/upper18 boundary vertices. Require every projected patch once-covered, nonzero oriented areas and strict all-head intersections zero; reject a twisted correspondence, repeated knot, radial reversal or triangle outside the ruled annular patch. There is no need for extra upper-ear vertices or hidden caps.

Animated mixed-weight proof remains REQUIRED

The actual original skull boundary has blended root/head weights (.5/.8 at the known contact triangle); the upper ear ring is nearer head-only. New skull-edge knots must interpolate the original source weights, the leaf boundary must preserve actual weights, and the annulus must use a bounded normalized two-bone field matching both. Static radial injectivity is not preserved automatically under that LBS field. An eventual candidate needs all63 actual head+ears PLUS adjacent neck/body strict crossing tests, exact shared seam positions/weights/normals, declared active triangle ownership, deterministic builds, and the unchanged078 first gear-fit test before any bridle repair. Current self/gear failures stay red until actual new proofs exist. Normals at the48protected vertices cannot silently change; if the constrained shading field yields a crease, report it for review.

Source analysis controls

check_chart.py includes six independent clipping/segment-distance controls. test_source_map.py has six actual-recipe controls, normal and optimized Python: actual map, false18knot claim, invalid barycentric, wrong source face, off-surface coordinate and wrong frozen input. These validate a recipe, not a generated horse. Root approval of this22/18 topology amendment is required before any geometry generation.
