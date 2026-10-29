# Unadopted eye-normal source study, 29 October 2026

This directory contains a reproducible **UNADOPTED / UNQUALIFIED** source prototype. It has never been installed in the application or published mirror. There is no browser, photographic, physical129 or posed129 acceptance for these new bytes. The existing e49 certificate belongs only to the exact e49 parent and is not rebound here.

The parent is `e49b6f1c9f7b70f1fcdf19fa7f6dddf54048b32256b4d8030d6238d6dfe79d49`, 4,159,196 bytes. Public recovery source: chicago-evidence CP15 commit `2c76735371058f52d1e7c275f23dd25c1ffedfda`. The candidate is `bd443df87b92d19266284cb9b52d30e791215cddf099876c774e9cfb5f5a79b6`, also 4,159,196 bytes, below the unchanged 4 MiB source cap.

## Actual bounded change

The two eye surfaces each have 482 unique source positions. A deterministic, centered least-squares sphere fit gives approximately 34.830 mm radius, with at most 3.207 micrometres between the minimum and maximum sampled radii. The recipe records each actual fitted center separately; it does not reflect one eye onto the other.

The generator replaces only accessor 208's 3,968 Float32 eye normals with outward `normalize(position - fitted_center)` directions. It honors accessor offsets and stride, refuses storage aliases, and updates the existing NORMAL accessor's min/max to the actual serialized values. All other JSON fields and all BIN bytes outside that normal storage remain exact. Positions, indices, UVs, joints, weights, binds, rig, animations, image payloads, materials, and hair/BODY normals are unchanged.

`SOURCE-PROOF.json` records exact half-open BIN byte ranges and unit/outward checks. `COMPONENT-PROOF.json` records every accessor's payload hashes, the six retained image hashes, protected JSON section hashes, and actual source invariants. The generator's second in-memory derivation reproduced the candidate byte for byte. All 53 existing application source pins still matched their current binding, TREE `4564435e579f6e3781b56b544da4b336d2295ca1`.

Actual numerical result: the original eye's 1,920 flat-shaded triangles become zero flat-shaded triangles; maximum coincident-position normal disagreement changes from 15.861162 degrees to approximately 0.000001708 degrees. The maximum original-to-new vertex-normal change is 7.932603 degrees. These measurements describe source normals; they do not establish a visible improvement in a rendered view.

Seven in-memory corruption controls were actually rejected: BODY position, hair normal, eye UV, embedded image payload, eye roughness, stale NORMAL extrema, and an inward unit eye normal. Corrupt candidates were not written to disk. The controls exercise protected data and directional invariants rather than duplicating the construction formula.

## Reproduce

The generator uses the Python standard library. Supply the exact e49 parent and fresh output paths outside every app checkout:

```sh
python3 generate_eye_normals.py --parent /path/to/exact-e49.glb --recipe recipe.json --out /outside/app/fresh-eye-study.glb --proof /outside/app/fresh-source-proof.json
```

The generator rejects an incorrect parent and refuses existing output files. The candidate inherits the parent's historical GLB metadata except for truthful NORMAL extrema; inherited historical text is not a new qualification record. The sidecar, certificate, source recipes, current app, index and mirror were not edited.

## Limits and next observation

This study can address eye-surface shading facets. It cannot thin the BODY socket or painted pale/dark eye ring, retopologize the cheek/brow, or improve mane/forelock silhouettes, hair transparency, material response or texture detail. No roughness or texture change is hidden in the prototype.

A later, separately labelled source-view study must compare exact old/new assets under identical native camera, lighting and material conditions and personally inspect the resulting views. That comparison is not the current published gate. Adoption and any qualification for the new bytes remain separate future work.
