# Prepared near-LOD textile study

Review/apply `cloth-near-study.patch`. Complete source is in the isolated sparse
`material-worktree/`, based on c6dc330d9bfd69fbbfe07d0feb2fb24f3c74fbcd.
ROOT APP was not edited. No commit, Blender execution, workflow dispatch, new GLB,
native rendering or runtime asset adoption occurred.

The builder's new `--woven-cloth-near` flag defaults off and is restricted to the
actual worker_1835 recipe. With the flag, cloned materials on LOD0 and LOD1 get
original packed 128x128 color, ORM and OpenGL tangent-normal PNGs. Existing
materials on LOD2 and LOD3 remain. Body/skin/hair/rig/source UVs remain; existing
Otis files were not touched. Linen and wool have distinct deterministic periodic
height/color/roughness fields. Normal relief uses physical height derivatives,
with disclosed reconstructed 32 mm tile, 2/1 mm thread periods and 25/20 µm height
coefficients. No captured cloth or historically measured weave is claimed.

Color pixels already include the current recipe RGB; cloned BSDF factor is white
to avoid tinting twice. ORM G carries absolute roughness, B is zero metallic,
R is one. Color images are sRGB; ORM and normal data are Non-Color. Standard image,
Mapping, Separate Color and Normal Map nodes are intended for glTF export. Actual
Blender PNG color handling, resulting glTF bindings/factors and texture transforms
still need worker verification. No Blender-only procedural node is required.

Calibration measures actual LOD0 garment surface/UV areas, excluding physical
return strips, and creates one material/repeat used identically by LOD1. The
existing inherited charts are stretched: the measured source-GLB shirt's UV/metre
range is approximately 0.16–16.42. The receipt states that calibration is an
area-weighted average, not uniform metric density. Preserving these UVs cannot
make their local scale exact. `existing-source-uv-measurement.json` records all
three current source assets, their unchanged hashes and read-only arithmetic;
its flat-normal exclusion approximates the BPy return-strip rule, so it is not
verification of the new BPy hook. Approximate Joseph/Martin repeats: shirt 25.158,
waistcoat 55.469, trousers 81.209, jackets 69.674/69.383.

Memory estimates include full mip chains and assume conservative RGBA8 decoding.
Normal images are shared between same-profile garments and between LOD0/1 in the
master. Separate exported GLBs may decode duplicates; the estimate counts both.

| Assembly | New cloth images per near GLB | Total cloth GPU bytes with mips | Net increase over existing 256² shirt map | Both near LODs net |
| --- | ---: | ---: | ---: | ---: |
| Three cloth materials | 8 | 699,040 | 349,516 | 699,032 |
| Four cloth materials | 10 | 873,800 | 524,276 | 1,048,552 |

Joseph plus Martin, retaining both near LODs without cross-GLB sharing, add about
2 MiB of cloth image/mip storage. Default Otis adds zero. Far LODs add zero. These
are texture-storage estimates, not a new phone memory verdict: decoder/bitmap
copies, other assets and shader costs still require the real 400 MiB scene check.
No 1904 recipe opts in. The raw RGBA8 test tiles are 65,536 bytes each; measured
zlib payloads range 385–9,511 bytes for the representative pixels. This is not a
measurement of Blender's eventual encoded PNG or resulting GLB size.

Five pure controls passed under the original 120-second supervisor: periodic
surface/derivative continuity, deterministic finite pixel fields and normalized
normals, retained recipe mean color, known metric calibration/invalid geometry,
and bounded near/far image estimates. Unittest time 0.929 s; supervisor 1.508 s.
Actual `measure_step_isolation --tool` reported no in-tree writes (1.269 s); the
isolation audit passed (0.115 s). Read-only current-GLB arithmetic passed (0.616 s).
All four checks had no timeout override, complete cleanup and no remaining owned
children. Logs and machine-readable closure are beside this file in
`MATERIAL-STUDY-CLOSED.json`. The new pure step is appended at the gate tail in
the isolated patch and its measured isolation row is included.

Before adoption, the Actions worker must render the actual opted-in source and
web GLBs, close garment views and full front/threequarter/profile views. Verify
LOD0/1 image bindings and identical transforms, LOD2/3 baseline, color factors,
normal convention, image count/byte costs, UV appearance, all contracts and the
phone scene memory gate. The ordinary-resident `fabric.js` shader remains
additive: it can layer larger weave/rumples over these microtextures. Their
combined appearance/performance is unmeasured and needs the real scene review.
The inherited tight silhouette and absent drape/wrinkles also remain visible
limits. No photographic, likeness, period-material or fit acceptance is claimed.
