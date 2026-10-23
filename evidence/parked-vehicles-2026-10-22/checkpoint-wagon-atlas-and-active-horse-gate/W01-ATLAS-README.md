# W01 timber atlasV2 — exact native-sampling source candidate, HELD

Root-owned T2793; source-only. This is ONE atlas consolidation of frozenV1, not an application activation or a new styling pass. No app/Git/ticket/browser/Blender/fullgate/variant writes occurred. Photographic, historical, near/far visual, device and GPU-budget acceptance remain open. No cost threshold changed.

## Actual result

`wagon-w01.glb`: SHA256d65a4c5c471c7d61ddac3cc1826fda6283018ba87adef80dd8ac46cda908373a,2,724,384 bytes. Actual bounded build0.615s at nice19/math threads1, exit0.23 meshes,23 primitives and6 material definitions (5 referenced) match original parkedW01.12,104 triangles unchanged. V1's8 added native material primitives are gone. All original material assignments and colour factors are restored/preserved; paint/iron/painted hubs remain exact. Old binary prefix and all POSITION/NORMAL/index/scene/node/pivot/skin/animation streams are exact.

The pre-existing triangle soup already provides independent per-triangle UV corners. Subtracting one INTEGER UV translation per whole triangle preserves the repeated material phase without splitting a source triangle or adding a vertex. Whole-side triangles still span up to3.003U periods, so one compact nonrepeated chart cannot preserve their native detail. The actual feasibility audit found side-domain4×2 source tiles and end-domain4×1 source tiles.

The shared colour, normal and ORM atlas images each measure **2576×264** pixels. Side tiles retain native512×128 samples and end tiles retain native128×128 samples. Integer repeats plus4px periodic gutters pack both appearances into the existing shared wood material textures. No source image is downsampled or stretched to hide cost; stored UVs map to equivalent native pixel positions. Metadata explicitly identifies donor-derived timber and original cut-end inputs as reconstructed optical material, never an attested historical specimen.

Actual texture tradeoff, explicitly unaccepted:

| Product | Native primitives | Material definitions | GLB bytes | RGBA8 all-mip dimension estimate |
| --- | ---: | ---: | ---: | ---: |
|Original parkedW01|23|6|1,926,852|6,291,684|
|Frozen surfaceV1|31|9 (8 referenced)|2,478,856|3,408,000|
|AtlasV2|23|6 (5 referenced)|2,724,384|12,976,992|

Simple4/3 mip estimate forV2 is12,978,176 bytes. These dimension-derived RGBA8 figures are NOT measured driver allocation, compressed-image cost or a memory-cap waiver. The device must support a texture edge≥2576. Original parent bytes remain in the immutable binary prefix, including superseded images, so payload growth differs from active GPU-image dimensions. Existing draw ceilings are not relaxed; the memory tradeoff needs actual review.

## Actual sampling and geometry proofs

`ACTUAL-RECEIPT.json` samples **16,176 actual serialized-Float32 UV locations**, four barycentric points per wood/end triangle, against frozenV1 using bilinear repeated source samples and corresponding world-space tangent/bitangent/normal frames. Maximum differences in8bit-channel units: colour.000379; normal.001690; ORM.001232. Maximum world-normal vector delta5.44933e−6. Tangent directions/handedness are retained because each chart remap is a positive diagonal scale plus translation; the actual worldTBN sample comparison includes normal scale.35.

This proof is **base-level sampling only**, not a universal rendered-pixel or all-mip equivalence claim.4px gutters/region alignment serve bounded near filtering; coarse atlas mipmaps can mix regions. Near AND distant real views must be reviewed before any acceptance. Native donor timber detail is only145×40 actual pixels; repeated atlas texels do not manufacture photographic resolution.

`ACTUAL-INDEPENDENT-READBACK.json`: independent actual GLB parse, exact oriented POSITION+NORMAL signature ec856227f831309f05aac28163bb0f2e2a05f42d5cdd4ba661457e80e44e347f before/after; corrupted POSITION negative control rejected. Wood UV minimum double-area4.88244e−7; max actual tangent/normal dot8.94e−8; tangent-length error5.96e−8. Paint and iron material records and bound image bytes are exact. The independent reader's field `cut_end_triangles:0` counts separate cut-end MATERIALS, intentionally absent inV2; the same708V1 end triangles are retained through atlas UVs and included in the native sample proof. It does not mean those faces were lost.

Other existing covered GLBs/recipe were pinned read-only before/after this consolidation. That preserves existing variant identity/paint/canvas assets; it does not establish that the new postprocessor handles covered variants' retired-part ownership. No such generalization or replacement is included. Khronos and actual browser/GPU checks have not run; local validator package was absent and no install was attempted.

## Rights, identity and reconstruction

Side timber is adapted from **Old Cart**, Lyskilde / longtail, CC BY4.0, https://sketchfab.com/3d-models/old-cart-f536745fd82144eeb5cc4900a48e816e and https://creativecommons.org/licenses/by/4.0/ . Actual creator metadata and individual Objaverse annotation match BY/author UID; copies and hashes are included. Attribution and changes are embedded and in `ATTRIBUTION.txt`.

Only the actually viewed CartBase timber crop[372,145,412,290] is transferred;128 actual source UV witnesses exclude padding/hardware. CartDetails hardware atlas is excluded. The derivative rotates/normalizes/reflects detail while preserving original W01 colour factors. Donor AO and metal channels are not transferred. Original new cut-end appearance is CC0-1.0 and unmeasured, with no species/ring-age claim; donor pixels remain CC-BY-4.0. No donor geometry or face/likeness pixels were used.

Old Cart supplies NO verified1835 date, Dearborn identification, maker or Chicago specimen. Its publication date is not object manufacture date. W01's dimensions, silhouette, paint, articulation and historical disclosure remain the original reconstructed design. Nothing here claims source photography, measured optics, aged wear date or photographic completion.

## Inputs and recovery

Original parkedW01 SHA256274e737b51872983df792d0b24de8e75de8631890a8d586a32d9c6f0066484fb. FrozenV1 SHA256da5df4b37ce6830af04f055453f6cb11890be29b3b28e9f4bd31a26bd3ff86ec. FullV1 recovery capsule `/workspace/shared/T2793-W01-OLDCART-SURFACE-V1-ACTUAL-CLOSED-20261022.tar.gz`, SHA256f01f67fc9551732819eb95c4715632175db85a5c75868867357d78a6f2c7b9fc,827,353 bytes, retains all crop/gamut/parse refusals and rights/source pins. Donor13600b73 originalGLB is already durable in root's earlier two-public-GLB audit archive.

`w01-oldcart-atlas-v2-HELD-20261022.py` is the complete bounded authoring script; extract theV1 capsule alongside it to reproduce its exact input maps/helper. Paths target this shared workspace; adapt input locations only after checking exact file hashes in another environment. It refuses an existing output directory. `refine_timber_surface.py` is a frozen helper copy for the independent reader, not a new producer run. `check_actual.py` reads the actual candidate, no app writes. `UNAPPLIED-source.patch` adds the reviewable isolated atlas authoring script and attribution; it does not wire a product into the app. Reconcile authoring input paths/provenance with the current production pipeline if actual images justify intake.

This source result solves the demonstrated extra-primitive cost ofV1 while preserving its native material samples at bounded witness locations. It does not close T2793 or any photographic/world/covered-variant gate.
