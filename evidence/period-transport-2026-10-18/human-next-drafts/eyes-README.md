# Original anatomical eye component draft

This is an original CC0 component study outside the application. No fixture, app body, builder or canonical Blender file was changed. No Blender installation/execution, Chromium or GPU rendering was used. It is a geometric/material improvement proposal, **not** photographic/medical/anatomical acceptance.

## Concrete output

`generate.py` produces `eyes.json` (original component meshes/material parameters/UVs/skin weights), `original_iris.png` and `validation.json`. It uses the current prepared adult25 body's actual `eye_l/r` helper heads as centers and normalized helper head→tail directions as optical axes. The left center is `[0.0295836049,1.6407237225,0.1120272253]` m, mirrored on the right; forward axes have ±0.05916 lateral, −0.14378 vertical and +0.98784 forward components. These source directions are retained, not silently replaced with straight-ahead eyeballs.

The helper tail is **not** an eyeball radius. Proposed radius12mm, iris radius5.5mm, pupil radius2.2mm and corneal height2.1mm are reconstructed engineering parameters requiring fit/anatomy review, not measurements of a resident or values established by the helper labels.

- `eyes__sclera`: an off-white sphere with the anterior iris aperture removed. A complete opaque sphere would hide a recessed iris, so the front cap is explicitly absent.
- `eyes__iris`: recessed radial annulus with an original deterministic fiber/limbal-ring image. The 1024×512 atlas gives each eye a separate UV region. Brown coloration is a provisional authoring choice; no resident eye color is attested.
- `eyes__pupil`: separate near-black center geometry, not a brown sphere or baked eye highlight.
- `eyes__cornea`: anterior transparent cap, standard glTF alpha-blend/PBR proposal. It is a **limited highlight shell**, not physical refraction. No unsupported KHR transmission/IOR extension is proposed without changing the contract and testing the renderer.

Every vertex has one normalized influence on the corresponding existing contract eye joint; no ad-hoc extra bone is added. All new UVs stay in0–1. Validation rejects out-of-range triangle indices, nonfinite values and zero-area triangles and orients faces outward. Current two-eye component count is9,600triangles/5,460vertices, deliberately excessive for a first diagnostic; production integration needs per-LOD sampling reductions and complete material/draw/texture budgets.

## Actual review and limits

`render_cpu.py` creates `cpu-head-eye-review.png` from the **actual current male25 prepared head triangles/source UVs**, the reviewed generic skin atlas and the new eye geometry. I viewed it: sclera/iris/pupil appear within the existing eye openings with plausible initial centering, rather than protruding uniformly brown spheres. The renderer is an orthographic diagnostic with triangle-average texture sampling; it omits the transparent corneal shell. It does not prove Blender export, GPU PBR response, three-quarter fit, eye movement, eyelid intersection or photo quality.

`source-receipts.json` retains pinned MakeHuman high-poly eye accessory OBJ/proxy/material files, each explicitly marked CC0, for source assessment only. **None of their geometry, UVs or pixels was copied into this original draft.** Their absolute accessory OBJ coordinates are not directly interchangeable with the base: the raw eye OBJ is vertically offset relative to the current base/helper frame and requires its `.mhclo` fitting semantics. We therefore did not infer centers/radii by naively dropping that OBJ on the body. Full source proxy fitting could be investigated later as a separate cleared alternative.

Remaining gates: full side/three-quarter/orbit fit on both25/35bodies; sclera/tearline/corneal shape review; meaningful blink/jaw interaction with eye placement; transparent-layer sorting and shadow behavior; exact BPy/material/export implementation; contract/Khronos validation; complete four-LOD geometry/texture/draw budgets; master/web parity; mobile/desktop close-up rendering. Hair, eyebrows, eyelashes and scalp coverage remain absent: a separate sourced/reconstructed original hair fit/groom is required. A skin atlas alone does not supply volumetric hair or individually matched appearance.
