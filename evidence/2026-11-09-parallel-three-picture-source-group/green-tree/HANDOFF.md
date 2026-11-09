# T-2376 Green Tree — bounded shoulder-roof source trial

Status: source-only trial ready for the combined T-2374/T-2376/T-2380 integration. No commit, push, browser, Blender, full gate, derived-data generation or image-match verdict was made here. Own checkout `/tmp/nov9-group-green_tree`, branch `steward/t2376-group-parcel-20261109`, base `c6dc330d9bfd69fbbfe07d0feb2fb24f3c74fbcd`.

## Concrete change

Only `chicago/4d/data/structures/green_tree_tavern.json` changes: `form.enclosed_left_annex.value.shoulder.roof_high_m` 4.0→4.6 m, plus an appended construction-note paragraph. The old note is retained as a prefix. No shared producer or parameter contract changes.

The current held Andreas comparison and the source image were actually viewed. Its shoulder roof rises strongly toward the main wall behind the pointed light; the present model’s roof meets that wall too low and reads shallow. Raising the existing attachment control steepens the slope from12.53° to21.25°. This is a reconstructed relative-form trial, not a measurement or a new dated July1835 assertion. The poorly constrained fixed camera remains unchanged. The outer3.2m eave,4.85m pointed cap, light/sash, shoulder wall, all spans/depths/turns/occupied rings/entrance and the main block’s footprint/height/site remain exact. No attempt is made to repair the broader group’s proportions by moving buildings or to resolve Trowbridge’s competing open bay.

## Actual checks

- Existing `python3 tools/test_frame_tavern_picture_features.py`: all25 tests PASS under the parent’s environment, no Blender.
- `/tmp/nov9-green-tree-group/probe.py`: actual current class and accumulator build before/trial PASS. Only eight vertex z coordinates change, confined to the shoulder roof/upper infill. All xy coordinates, faces, material assignment/specifications, confidence, named attributes,6666vertices/1668polygons/3330triangles and full model bounds are identical. Occupied component frames and entrance are exact.
- All24 other current frame-family input documents recompute to the existing native-binding hashes exactly. The data edit introduces no new note path; existing `phases[].form.enclosed_left_annex.note` is already declared in name_pool_keys.
- `git diff --check` PASS. No shared file was edited.

## Native scope and stopping point

One structure only: `green_tree_tavern`, phase `frame_1833`, one default output and zero versions. No shared-family bake is earned by this record-only change. Before inputs SHA256 `7949ea008870a2bf203d9c599b23c58ede5195c8a853caf55e7d9e63fa2b9144`; trial `c8f9a7cd184702d6600ca6bef7a181e565b34a604c2d1f2be21fca17d1d8a911`. Old current master remains `f213818f5a686d31bfbb07217233a7021c514be64b841035d3c29996a380807b` (270816B), not a new output claim.

After combined integration, run the real native owner and refresh `data/reference_views/green_tree_tavern/andreas_1838.json` without altering its camera/photo. Accept or reject the trial by actually viewing that new comparison. Keep original T-2376 partial unless every remaining visitor-visible discrepancy and its broader picture coverage is adjudicated. Fresh current WEB/registry/sidecar, published body/yard/terrain, desktop and phone remain unqualified here. No new photo follow-up is needed.

## Integration files

`SOURCE.patch` contains the complete single tracked-file diff (no untracked source file). Check `PATCH-MANIFEST.json` before application. `LIBERTY-DRAFT.md`, `STATUS-DRAFT.md`, `ROADMAP-DRAFT.md`, `CHANGELOG-DRAFT.json` and `NAME-POOL-NOTE.md` are snippets for the sole integrator; they were not applied to shared files. `ACTUAL-SCOPE-PASS.json`, both input documents and owner/probe logs retain actual verification. The external probe is evidence, not a new gate step and therefore needs no new isolation registry row.
