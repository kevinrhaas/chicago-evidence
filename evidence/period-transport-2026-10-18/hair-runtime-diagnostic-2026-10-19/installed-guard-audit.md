# Installed diagnostic guard audit

Read-only review of the installed two-tool working diff against its current committed parent. No app writes, tests, browser, Blender, CI calls, or heavy computation.

No blocking change found. Every preexisting runtime predicate, tolerance, `errors.push` statement, and runner `failures.push` path remains textually unchanged. Runtime acceptance remains `errors.length===0`; the runner still enforces every returned check and returns failure exit status. New sampling reads existing attributes only after the original matching/nonempty-attribute check; it does not mutate transforms, attributes, weights, materials, textures, renderer state, or arrays used by acceptance.

New invalid-vertex samples stop at eight per mesh, with fixed-size position/UV/normal/joint/weight vectors. Bone names stop at64. Log errors stop at8 with explicit truncation state, and meshes stop at8. Attribute receipts contain only counts/types/normalization, and image receipts only expected/actual dimensions. No image objects, binary bytes, pixel arrays, screenshots, or complete geometry are included. Material receipts enumerate matching hair materials (the standalone container contract already requires the exact single hair material); this collection has no separate hard count cap, so it should not be described as an arbitrary-malicious-input bounded logger. This is not a blocker for the inspected contracted asset pipeline.

Missing map/offset/repeat/matrix properties are protected with optional chaining; absent image sizes remain null diagnostics and continue to fail the unchanged dimension predicate. The new mapping assumes actual Three Skeleton bones are objects and actual material arrays contain materials, as the preexisting inspection already does. No new missing-optional-property crash found in that supported API. A deliberately malformed nonfunction toArray property is outside the actual Three/mock API, not newly claimed supported input.

Nonfinite numerical diagnostic fields serialize as JSON null, as usual; their original guard errors remain preserved. The stored matrix is read without updateMatrix/transformUv, so no implicit transform or wrapping occurs. Raw UVs remain the checked coordinates. Actual CI hair failure cause is still UNKNOWN; these changes make the next failure observable and do not purport to repair it.

Audited parent: `45eab8cd02a0c6c80633cda7e9cfff589f5b2085`.
Installed SHA256:
- human_hair_runtime.mjs: `6fddbb02f19aaae0e0b26214b75bceadfac322db6fb1eb3970e9ef22aa40f020`
- human_teamster.mjs: `5eb6f2c7d6379145444062fc74a90aaf02d7ac08d234edcdc93772361cf5c81a`
