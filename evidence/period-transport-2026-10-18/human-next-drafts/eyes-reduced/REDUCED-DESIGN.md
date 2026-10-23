# Reduced original eye design and proposed integration

This supersedes the 9,600-triangle diagnostic with an explicit whole-person eye budget. All work remains under `/workspace/shared/eye-quality-draft`; the application, fixture and running CI/preflight inputs were not changed. No Blender/GPU/browser command was run.

| LOD | Added triangles, both eyes | Added vertices | Material groups | Ceiling |
|---|---:|---:|---:|---:|
| 0 | 1,584 | 956 | 4 | 2,000 |
| 1 | 736 | 482 | 4 | 1,000 |
| 2 | 288 | 212 | 3 | 400 |
| 3 | 128 | 112 | 3 | 200 |

`human_eye_components.py` is a new original CC0, standard-library-only component module proposed for `tools/`. It constructs actual sphere poles/central fans rather than wasting tiny near-zero rings, preserves a distinct sclera aperture, iris annulus and pupil, and drops the limited transparent corneal shell at LOD2/3. Its output arrays match the canonical builder's existing `object_mesh` API. Each component remains bound to the existing `eye_l/r` joints; no extra skeleton or bone naming contract is introduced. All dimensions and brown coloration remain reconstructed authoring parameters, not resident measurements/eye colors.

## Exact checks against the real prepared heads

`reduced-validation.json` and `reduced-topology-validation.json` cover all four LODs on **both actual adult25/adult35 hm08 prepared bodies**, using each body's own eye-helper heads and directions. Exact triangle/vertex counts agree at both ages. Construction validates finite coordinates, 0–1 UVs, index bounds, nonzero triangle areas, outward winding and whole-person triangle ceilings.

On adult25, LOD0 both-eye bounds are:

- X `−0.041549309 .. +0.041549309` m.
- Y `1.628746709 .. 1.652670994` m.
- Z `0.100056774 .. 0.124719710` m.

The helper axis and center coordinates are recorded in each generated `eyes_adult<age>_lod<lod>.json`. The 12 mm globe radius, 5.5 mm iris radius, 2.2 mm pupil radius and 2.1 mm corneal-cap height remain explicit reconstructions. Bone length is not used as an eyeball radius.

Measured adult25 LOD0 sclera face-centroid radial deficit from its analytic 12 mm sphere is at most **0.157 mm**; edge-midpoint deficit at most **0.176 mm**. These measure the actual low-poly faceting, not a claimed whole-surface Hausdorff bound. Lower LOD facets are deliberately larger; exact values for both bodies are in the topology report.

Each eye's existing source mesh has 512 front-orbital vertices in a ±25 mm XY window around the helper center; **zero sampled vertices lie inside the reconstructed 12 mm sphere** on either age body. This is a raw point diagnostic, **not** proof of surface clearance: triangles can cross between vertices, eyelids move, and cornea/tearline/contact need actual render and collision review.

`cpu-head-eye-reduced-lod0.png` was generated and viewed on the actual adult25 source head and reviewed skin atlas. Initial iris/pupil/sclera placement survives the reduction and remains within the visible apertures in this front diagnostic. Its CPU triangle-average texture renderer omits the transparent shell and does not certify PBR, orbit views or eye/face movement.

## Reviewable integration patch, not applied

`proposed-integration.patch` contains exactly three changes:

1. Add `tools/human_eye_components.py` (the original module above).
2. Update `tools/human_teamster_blend.py` to replace its uniformly brown spheres with the budgeted components, create separate valid `eyes__*` material variants and pack an original 512×256 procedural iris atlas. Skin input/UVs, resident references, body/garment selection, facial targets, fixture and canonical export path are retained. No sampled eye image or official accessory mesh is copied.
3. Add explicit reconstructed eye parameters/budgets/status to `data/humans/recipes/worker_1835.json`.

`propose_patch.py` generated this diff against the current application files without writing them. The proposed complete builder and module passed Python syntax compilation. The same script writes `proposed-human_teamster_blend.py` and `proposed-worker_1835.json` for review. After other app edits, regenerate the proposal or resolve its context deliberately; do not apply a stale patch blindly.

The proposed alpha setup is version-adaptive BPy code and **has not run**. The corneal shell is a standard alpha/PBR highlight approximation, not a physically refractive cornea. No unsupported KHR transmission/IOR extension is added. CI must verify actual exported `alphaMode`, material factors, blend sorting, shadows and close/mobile views. If alpha export is unsuitable, keep the cornea disabled until a supported tested representation is chosen; do not silently claim the shell solves eye optics.

## Acceptance still open

Integrate only after the first actual human CI render has been reviewed. Then build the canonical `.blend`, export all four LODs, validate the exact material/morph/skin contracts and Khronos output, decode/compare web derivatives, measure texture/draw/frame costs, and review front/side/three-quarter/head turns and blinks. Sphere/eyelid/tearline intersection, corneal response, facial target quality, individual likeness and photographic acceptance remain open. Hair/eyebrows/eyelashes are still absent and require separate authored fit/groom work; this eye patch does not solve them.
