# Independent remaining lip crossing diagnosis

Archive verified SHA256369d8a6ab71b07001411ecd546c93bdb9a1f604ef5631e57eede59c15d65e510. Read actual archived source/head_surface.py, source-self.json, trial1/head-source-surface.json and CHECKPOINT.json. No generator, GLB mutation, browser or app edit executed. Extracted source/receipts only.

Actual failed source has8 strict crossings; every pair is annulus skin:lip_l face1578 or1579 versus lining lip_l face1606,1608,1609,1610,1611. Witness signed distances include millimetres on both sides, not tolerance-scale contact: first witness+1.6098/-3.8170mm, interior barycentrics(.1623,.4605,.3772). Protected9688faces/48vectors and topology7negativecontrols were reported passing in archived checkpoint; they do not certify embedded surface geometry.

## Concrete mechanism

Ordered UV mapping repaired earlier global correspondence but lining remains independently reprojected to the curved muzzle width function. Source inside loop contracts y,z halfway toward lip center then sets x=side*(sx(y,z)-depth*.8). Center similarly calls sx(cy,cz)-depth. Because sx changes rapidly over this muzzle patch, “subtract depth” is NOT an inward displacement from aperture. Actual aperture878=(.060210537,-.22306066,.50456066); corresponding inner894=(.065559633,-.22253033,.48728033). Left-side inner goes5.349096mm OUTWARD inx, not inward, while moving17.28033mm posterior. Aperture879→inner895 likewise increases outwardx by5.4027mm. This lining bow intersects prior annulus triangles1578/1579. Source positions match witness world coordinates after common1.88y/.8z translation; no inferred camera geometry.

## ONE bounded repair recommendation

Change lip-only lining construction to a depth-monotone extrusion from the actual aperture boundary: retain ordered UV capsule and existing annulus; derive each inner side-normal coordinate from its corresponding APERTURE coordinate minus explicit additional inward inset, instead of reevaluating sx at contracted yz. Derive closure center from a bounded inward envelope of that aperture/inner loop, not another independent sx(center) reproject. For side+1 inward is decreasingx; side-1 increasingx. Keep current local y,z contraction initially so the experiment isolates this independent reprojection defect. No global muzzle widening, tolerance relaxation, extra shell, hidden face deletion or protected portal change.

This eliminates the demonstrated outward-recess mechanism; it is NOT a mathematical guarantee of all nonadjacent surface separation. Inward x per correspondence alone does not prove projected triangulation disjointness or clearance from other surfaces. Actual candidate must rerun strict selfcrossing against all head faces, topology/negativecontrols and exact protected face/portal attribute invariants; reject any remaining crossing. If it fails, preserve witnesses rather than silently increase depth or waive contact. Recheck left/right even though only left currently fails; asymmetry follows existing surface geometry. Only after source selfgate passes should root authorize gear sweep/render.

No implementation or claimed repaired asset is supplied by this independent read-only review.
