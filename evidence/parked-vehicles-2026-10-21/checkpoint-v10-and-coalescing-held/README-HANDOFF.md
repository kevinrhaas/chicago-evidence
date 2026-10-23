# Studebaker Brougham V10 — frozen roof-only source proposal, UNRENDERED

This is one bounded roof/front-header/molding proposal against exact V9 `03c333af…`. It is outside the app. No browser/server, tracked app/index, Git/CI/ref change, new acquisition, installation or Blender action occurred. No actual V10 render, source match, photographic, collision, occupant, LOD or scene acceptance is claimed. V9 is preserved in `baseline/` and its source is in `preimage/`.

The correct acquired reference is the actually viewed 1556×1145 `reference/studebaker-brougham-cdn.jpg`, SHA256 `b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe`,1893 Studebaker catalog leaf0095. I also viewed the V9 actual reference render and contact sheet. The similarly named `studebaker-brougham-page.jpg` SHA2daf1ecd is a blank aged-paper neighboring page; prior research already warned of this mismatch. It supplies no vehicle evidence. Keep that excluded. The included source record is PROPOSED and must not be treated as installed app data. Maker/catalog type is documented; a specific1904 household, owner, specimen presence, absolute dimensions, opposite side and interior remain reconstructed. Coachmen obscure the far/front roof and their clothing does not attest empty upholstery. The unresolved upper-quarter material ruling is unchanged; opaque dark is still a bounded appearance choice.

## Bounded change

The V9 preview shows a conspicuous forward roof curl. Keep roof width, transverse crown, rear profile half, front/rear endpoints and maximum longitudinal height exact; shift the longitudinal crest rearward0.16m (Z+.12→−.04m), easing the neighboring approach heights. This reduces the short leading rise rather than changing the cabin or camera. Reduce reconstructed sheet thickness35→25mm, drip radius15→10mm and end lip12→9mm. Attached upper/end headers follow the changed roof profile; all their lower interface points remain unchanged. These numbers are engineering choices guided by the broad plate contour, not historical measurements.

Under the unchanged nonunique camera, the near crest control projects from x1014.44/y486.03 to x1046.92/y485.78 source pixels; adjacent controls move smoothly. That direction is consistent with the visibly rearward broad source arch. This is a projection of geometry controls before occlusion, NOT a rendered silhouette match. Uncertainty in the perspective hypothesis and source ink remains. No camera fitting or source-pixel retouching occurred.

The actual producer diff replaces roof-local constants with three explicit parameters and changes only the longitudinal roof controls.337 nonroof component POSITION/NORMAL arrays are byte-equivalent Float32 values against V9, including door/U/glass/opaque quarter, perch/dash/cushions, lamps, wheels/hubs, axles, pole, steps and sockets. Node graph/translations/materials/scenes/parts metadata, triangle counts and camera bytes are exact. All existing producer refusal guards remain verbatim. Only seven named roof/header part families are allowed to differ;120 component records (including individual fascia quads) are covered by that allowance.

## Actual finite checks

Candidate/repeat `645e3a9c3dcb448469a4d9d1bd3bcbb8ffde81fddf5aa401a39e08e44e731c0e`,2292536bytes,30782triangles/24batches/41nodes, deterministic byte exact. Khronos0errors/0warnings/4inherited empty-anchor infos, untruncated. All triangle areas are positive (minimum1.30477e−5m²); maximum unit-normal error4.78181e−8; all body stored-corner normals face the geometric surface (minimum dot+.423184). All four changed roof trim tubes have positive signed volume. The complete top/underside/fascia roof shell has exactly two incident triangles at every position-welded edge and positive oriented volume. These local checks do not establish whole-vehicle clearance or visual quality.

`SOURCE-GEOMETRY-AUDIT.json` contains exact bindings, full protected inventory and source-space control projections. Original V9 door/body cap clearance remains invariant because all relevant positions/normals are exact; no broad collision rerun is relabeled as new proof. V9 shadow diagnostics and remaining perch/dash/finish/photographic gaps remain open. The included V9 before PNG uses preview normalBias.008m and is clearly labelled; it is not production lighting evidence or a V10 result.

## Reproduction and next step

Use a fresh output path:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python proposed/generate_brougham.py --output /tmp/brougham-v10-fresh
OPENBLAS_NUM_THREADS=1 python audit_geometry.py
node validate.cjs
```

NumPy and the already available Khronos validator path are required; no install is needed on this environment. The audit is self-contained relative to this directory; the validator references the existing `/workspace/shared/transport-tools/node_modules/gltf-validator`.

After root explicitly releases the browser lane, one bounded actual same-camera V9/V10 reference study could test whether the roof change helps. Keep the same actual light/shadow settings for both arms, retain V9 before, and report all remaining differences. Do not install this proposal, claim matching pixels, replace generic C02, add occupants or close T2794 based on this source arithmetic. Root owns integration and all required app gates.
