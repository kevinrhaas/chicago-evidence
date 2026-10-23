# Body-normal authoring alternatives: bounded investigation after failed2679

No method is recommended for production before the next CI's observed max/mean/top-corner and source-ID seam-spread data. This investigation does not change the1e-3 guard, execute Blender/browser, derive a new model, dispatch CI or download artifacts. The actual failure's cause remains unknown.

The existing source-ID-shared area-weighted targets are internally coherent, but Blender4.5.3 encodes custom normals in each smooth fan's own short2 frame. Identical world-space targets at two UV-split points can therefore decode differently. See sibling human-normal-readback-2679/CODEC-ANALYSIS.md for the proven beta-snap counterexample and limits of a global bound.

##1. Diagnose actual corners first

The root-integrated diagnostic now prints finite readback max/mean, count over unchanged1e-3, five worst loop/vertex/source IDs with intended/actual vectors, plus actual normal pair spreads across distinct UV-split vertices sharing a source ID. These observations distinguish small codec quantization, appreciable seam discontinuity, zero/invalid output, wrong coordinate convention and cache trouble. A source argument alone does not establish which occurred in this body.

Acceptance should keep separate questions separate: normal values finite/unit; intended-direction error; actual agreement across source UV duplicates; unchanged geometry/UV/weights/morphs; emitted source/web buffers and decoded deformed shading; visible neck/head/garment/hair appearance. A camera or mechanical gait pass cannot establish normal quality. No threshold is suggested here.

##2. Ordinary setter input pre-distortion cannot universally repair the beta hole

Merely nudging the intended input and calling normals_split_custom_set again is not a universally reversible solution. For an equatorial target in the middle of the encoder's beta-zero dead region, output beta is either0 or lies near/outside its ~0.01414rad boundary, up to quantization. At fixed valid fan frame, the nearest representable direction through that encoder can remain ~0.007rad away. Altering alpha cannot supply the missing orthogonal component at the equator. Thus an input-only search cannot guarantee1e-3 for all targets; it must be allowed to fail without moving the guard. Global rigid rotation of both geometry and targets preserves the relative fan angles and therefore does not remove the dead region.

A measured per-corner iterative setter experiment might improve some real normals, but needs reversibility, explicit target-error/seam checks and a stopping/failure criterion. It must not silently modify target directions until a test passes.

##3. Direct packed-code authoring: a supported data path, not a ready implementation

Pinned4.5.3 RNA confirms a possible route that bypasses the **encoder** beta snap while preserving its decoder:

- rna_attribute.cc38/69 lists INT16_2D.
- rna_attribute.cc1306–1343 defines Short2Attribute and its writable two-integer value property.
- mesh_normals.cc1594–1595 stores custom_normal as corner-domain short2.
- rna_attribute.cc413–421 tags dependency updates only for data with users; it does not itself explicitly invalidate the normal caches. A deliberate mesh.update is needed when probing raw codes on a fresh mesh.

These APIs were read from the official Blender/blender v4.5.3 sources via configured gh. Local read-only GPL evidence: sibling human-ci-watch-2679d6c98/Blender453-rna_attribute.audit.cc. No BPy assignment has been executed.

Direct code values can represent small nonzero beta even where the ordinary input encoder would choose0. However a code pair has meaning only in its actual **fan frame**. Copying the same short pair across UV-split points is wrong when their frames differ. Incorrect per-corner codes within one fan can also be averaged by the decoder (mesh_normals.cc1190–1204). The frame axes/reference angles are not exposed by the inspected public RNA API.

A future isolated CI probe could recover/validate each fan's response with controlled packed-code samples, then compute/search an integer code pair for the intended unit direction. It must identify complete fans, maintain coherent codes within them, detect invalid/ambiguous spaces, explicitly invalidate caches between probes, and restore the original packed attribute plus any sharp-edge changes on failure. It must not change positions, UVs, skin, materials or morphs. Final actual decoded target error and seam spread must both satisfy unchanged quality criteria. Snapshot/reload/export proofs are essential; this is substantially more complex than changing a number and is not proposed for blind integration.

##4. Exact source-ID point joining with CORNER UV: a basis-sharing alternative

The body preparation represents UV seams as duplicate POINT vertices. Blender can instead share an anatomical point across its faces while retaining different UV values per CORNER. Joining **only identical explicit source IDs**, with exact equal positions/weights, could give those UV faces one shared smooth fan/basis. glTF can then split the UV vertices again at export while copying an identical already-decoded normal to each duplicate. This attacks the seam's different-basis problem rather than enlarging a per-normal error cap.

Actual frozen2679 adult25 **and** adult35 prerequisites were inspected with the original JSON bytes:

-14517 split vertices,13380 explicit source IDs,1122 IDs represented by multiple vertices;
- all same-ID positions and skin-weight mappings exactly equal;
-26756 triangles,80268 oriented corners; joining by source ID collapses no triangle;
- expanding the candidate joined representation reproduces every original oriented corner's position, UV and skin weights **exactly**;
- input data remain unchanged; hashes and per-body results in source-join-feasibility.json.

The outside audit_source_join.py only constructs/checks an in-memory feasibility representation. It creates no Blender object or asset. It deliberately does not epsilon-weld different IDs. Current blink/jaw authoring depends on vertex coordinates (frozen builder338–358), so identical joined points would receive the same formula, but actual shape-key export and skinning still need proof.

Limitations: Blender connectivity and vertex indexing change. One source point can contain multiple disconnected or intentionally sharp fans; joining alone does not prove one normal. Normal definition also matters: Blender automatic smoothing may use angle weighting rather than the current intended area weighting. Keeping custom normals still exposes codec error, although shared fan duplicates may agree. Removing custom normals is a deliberate authoring-method change requiring a new source-grounded reference and visual review, not a way to evade readback. LOD decimation may behave differently with shared seam topology. All facial targets, materials, per-corner UVs, source/web geometry, skin and actual gait contacts must be rechecked. Hair cards and garment shells must not be joined by this body-only mapping.

A bounded later experiment should begin LOD0 body only and retain an exact reversible old-to-new/source-ID map. Compare oriented corner position/UV/weights/morph deltas rather than assuming old/new vertex ordering. Existing parented/root control compares the same newly authored mesh and remains useful but does not by itself prove old-vs-new topology/attribute equivalence.

##5. Independent exported seam audit is useful regardless of authoring method

At the decoded source and web GLB boundary, verify finite/unit NORMALs and agreement of corners corresponding to the **same explicit source vertex**, separately from raw target agreement. Prefer a retained verified source-to-export mapping; do not guess correspondence by nearest positions, since different anatomical surfaces or intentional hard edges can coincide. Stable correspondence can use audited source IDs plus original corner UV/material/weights/morph signatures, with duplicate ambiguity rejected. Adding a custom source-ID attribute would require explicit exporter/contract/license/publish review; it is not silently authorized by this report.

Observe deformed normal behavior at idle/walk/morph samples as well as rest; weights duplicated across a seam should produce consistent transformed normal directions, but morph-normal generation/export can introduce differences. Normalizing a malformed zero normal must fail rather than hide it.

##6. Post-export float NORMAL replacement is a separate pipeline design

Writing intended float32 normals into the emitted GLB would bypass Blender's codec, but it creates an authored transformation beyond canonical Blender export. It needs exact per-corner mapping after UV/morph/export splitting and decimation; correct morph NORMAL deltas; unit/finite frame checks; source/web derivation parity; hashes/receipts and an explicit canonical-source contract. It must never mutate positions, UVs, weights or animation to repair lighting. Without those proofs it is less defensible than leaving the current guard red. It is not proposed as a quick fix.

## Practical next decision

Read the next actual bounded diagnostics before selecting any alternative. If the target error is large/invalid, repair the cause. If it is the documented encoder dead region while seam spread stays low, a codec-supported acceptance discussion needs a real derived bound plus observed values and visual/export checks; the current source analysis explicitly does not certify a full floating-point cap. If different seam frames dominate visible discontinuity, source-ID/CORNER-UV topology or correctly framed packed-code authoring are investigable routes. None establishes photographic skin, hair, period clothes or an individual's likeness without the separate image/appearance review.
