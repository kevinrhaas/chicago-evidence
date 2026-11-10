# Charles's existing coat: source prototype, not adoption

This proposal targets only the already drawn 1904 actor
`hi_pa1904_glessner_john_j_c1900_charles_nelson_1904`, using the current
`nelson_charles_1904_coachman` coat. No child GLBs, textile images or new renders
have been generated. No assets are installed. Native loader/render, geometry,
fit, phone memory and photographic acceptance remain pending. Joseph's separate
successful portable-map measurement is not Charles qualification.

The data recipe pins the exact four current near MASTER/WEB GLBs and four far
baselines at `fc5a52b6cab3eed78e2db5864aa811dff5df2795`. These are current GLB
parents, not a retained `.blend`. An actual cached-input preflight verified all
four near SHA256s, sizes and Git blob IDs (22,413,752 bytes; zero network bytes).
`TEXCOORD_0` exists on every coat primitive. Current MASTER coat triangles have
no UV or position degeneracy. Genuine official MikkTSpace corner discontinuities
prevent a single tangent per existing index: LOD0 skirt has seven conflicting
corner occurrences; LOD1 body has 26 and skirt one, including handedness flips.
The existing WEB body has 70/25 UV-degenerate faces and 5/0 position-degenerate
faces at LOD0/1. These are baseline facts, not introduced by this proposal.

`human_charles_coat.mjs` copies the whole old MASTER BIN verbatim and appends
only coat component streams, actual Mikk tangents and three 128-square maps.
Every old row remains in its original position. Only a new `(old index, exact
Float32 Mikk tangent)` group receives a duplicate row. All expanded triangle
PN/UV/JOINTS/WEIGHTS and morph components remain bit-exact; no averaging, UV
repaint, triangle removal or winding change is allowed. The independent Python
verifier checks this directly from raw component bytes, rejects gratuitous
splits, and checks all other JSON, original accessors/views/images, rig, nodes,
animations, identity and frame. Counts, source-index/corner mappings and hashes
will be emitted when generation is approved. They do not exist yet.

The coat keeps the exact material name
`garment_outer__livery_coat_green_1904`. The original effective linear green
palette `[.014,.026,.019]`, roughness `.86` and metalness zero become standard
glTF base-color, ORM and OpenGL tangent-normal maps with
`KHR_texture_transform`. Color pixels use explicit IEC sRGB encoding; ORM and
normal are linear data. The original periodic wool design and 20-micrometre
height coefficient are reconstructed liberties, not historical textile captures.
All original noncoat materials and images are protected. The original coat slot
is shared by body and skirt with different UV densities: one aggregate metric
repeat is calibrated from actual transformed LOD0 triangles and reused exactly
at LOD1. Per-part achieved area-based periods are reported. Existing local UV
stretch remains a qualification question; no uniform physical thread-size claim
is made. Normal-map and roughness interaction must be inspected under native
lighting before adoption.

The optional scoped `fabric.js` mode disables common weave only where that exact
marked coat already has a portable normal map, and disables common dye heather
where its portable color map remains. Common wear, rumple, roughness wear and
sheen remain. `dressCloth` is unchanged: exact-name recoloring clones one shared
material, clears only its base-color map, keeps inherited normal/ORM textures,
and disposing the clone leaves shared textures owned by the asset. Common dye
heather returns on that recolor, while portable thread normals still own weave.
No ordinary material or other person opts in. Real old/new GLTFLoader and actor
lifetime comparisons remain mandatory; the included real-Three controls check
the source decision and existing recolor semantics only.

## Canonical WEB policy

The actual repository pin is **4.5.0** for CLI, core, functions and extensions.
The existing file's discussion of 4.4.2 is historical. The earlier input preflight
used 4.5.0 decoding and MikkTSpace 1.1.1. `human_charles_coat_web.sh` uses the exact
current owning `human_export.sh` texture/codec commands: image caps 2048/1024,
opaque-color JPEG quality 92, then `meshopt --quantization-volume scene --level
medium --quantize-normal 16`. It does not change precision or ceilings. The
current canonical parent is already skin-canonicalized; Blender and a second
skin canonicalization are deliberately absent from this material-only path.

The independent JS semantic reader recomputes actual Mikk corner tangents from
the decoded original MASTER. It reconstructs the existing pinned codec in RAM,
records source triangle/winding correspondence before quantization, and requires
old WEB semantics to equal that actual reference. It then requires the candidate
WEB's expanded PN/UV/JOINTS/WEIGHTS/morph triangle multisets to equal old WEB
exactly, with cyclic corner rotation allowed and reversed winding refused. All
old decoded node/rig/bind/clip values and noncoat material/image bytes must remain
exact. Baseline degeneracies are preserved by their semantic/source-face mapping;
any added, removed or changed degenerate faces fail. This deliberately conservative
exact comparison introduces no numerical tolerance. A real baseline codec
mismatch stops with the concrete delta; it never becomes a new epsilon or an
automatic precision change. WEB raw buffers/indices may be repacked while these
semantics remain protected. Native glTF Validator and actual GLTFLoader, sampled
animation/skin/morph, materials, side-by-side renders and memory gates still follow.

The source03 metadata guards also require actual TRIANGLES mode, complete
noncoat material extensions and TextureInfo sampling definitions, named/ordered
morph targets with semantic membership and effective default weights, and all
coat map slots/marker/sampling retained against both the verified MASTER and the
actual canonical post-JPEG child. JPEG color encoding is kept separate from
geometry acceptance. A read-only `--master-only` entrypoint runs the independent
Mikk, decoded rig/clip/morph/noncoat checks without producing or requiring WEB.

The first actual WEB attempt stopped in this metadata reader after canonical
serialization omitted explicit defaults; it did not pass semantic acceptance.
Source05 resolves only the glTF2 schema's absent defaults: base color `[1,1,1,1]`,
roughness/metallic factor `1`, TextureInfo UV set `0`, normal scale `1` and
occlusion strength `1` where applicable. Explicit null, malformed shapes/types,
nonfinite values and changed effective factors/sampling remain rejected. Texture
and marker presence, transforms, filters, wraps, codec precision and every geometry
check remain mandatory. Actual pinned-writer omission controls use the reviewed
MASTER0 child in memory; no image is decoded or new GLB written by those controls.
Their first run exposed an insertion-order comparison bug: default normalization
produced equal TextureInfo properties in different object key orders. Source06
uses structural exact equality: object insertion order is irrelevant, while array
order, values, types, own property presence and signed zero remain strict. The
original control NONPASS is retained; new controls exercise this distinction.

## Reviewable invocation, not yet run

Use an isolated dependency prefix with the exact published MIT packages
`@gltf-transform/{cli,core,functions,extensions}@4.5.0` and `mikktspace@1.1.1`.
The already cached genuine dependency prefix satisfies these pins; no dependency
was installed for this source proposal. Source tools are GPL-3.0-or-later;
original authored textile pixels and Charles's existing family are CC0-1.0.
The original asset license/provenance remains binding. No new historical source
or `.blend` provenance is invented.

After source review, on a bounded native measurement worker, with `INPUTS`
containing only the four approved current near parents at their recipe paths,
and fresh external `MASTER_CHILDREN` and `WEB_CHILDREN` paths:

```sh
node tools/human_charles_coat.mjs \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$PINNED_NODE_MODULES"
node tools/human_charles_coat_semantics.mjs --master-only \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$PINNED_NODE_MODULES"
bash tools/human_charles_coat_web.sh \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$WEB_CHILDREN" "$PINNED_NODE_MODULES"
```

These commands do not modify a workflow, dispatch a job, install a runtime asset
or opt in an actor. Existing source workflow has no material-child flag; a
reviewed explicit native invocation is needed before execution. Do not pretend
`build_teamsters` rebuilds this current Charles parent. The four far files stay
outside this generator and their whole-file SHAs remain the recorded adoption
baselines. Any later adoption must verify those baselines again on complete
inputs rather than treating their absence as evidence of preservation.

Three 128-square RGBA8 textures with full mips cost 262,140 bytes per near LOD,
524,280 bytes if both are separately resident. Tangents add 16 bytes per resulting
coat vertex before the normal canonical WEB quantization; split counts and all
decoder/transient/texture-sharing costs require actual output measurement. No
current Phone Light or other memory/geometry/frame ceiling is changed. Far LOD
increment is zero by generator scope, pending whole-file adoption validation.

Pure source controls: `node tools/test_human_charles_coat.mjs`. They cover exact
recipe scope, real signed corner-group decisions, dark-color quantizer intervals,
real Three material hooks, exact-name recoloring, shared clones and disposal.
They do not produce or load new GLBs, prove map export, test a renderer, or pass
the full native gate. Generated-writer registration/isolation and full published
loader qualification are pending a reviewed source/output scope.
