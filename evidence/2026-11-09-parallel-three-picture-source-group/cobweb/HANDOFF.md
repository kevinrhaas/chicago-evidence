# T-2374 Cobweb Castle — source increment ready for the grouped PR

Status: SOURCE/PRE-EXPORT QUALIFIED ONLY. No commit, push, native build, browser, full gate or image-match claim. Original remains partial and its private panorama camera remains unsolved/unenrolled.

Own checkout `/tmp/nov9-group-cobweb`, base `c6dc330d9bfd69fbbfe07d0feb2fb24f3c74fbcd`, branch `steward/t2374-group-parcel-20261109`. Complete patch `SOURCE-WITH-UNTRACKED.patch`: SHA256 `47abf6e0cc22377471470b29be674a8669426d9d3c32dd056276f8cedb15b928`, 25770bytes; three tracked files plus the new test. Postimage hashes and exact paths are in PATCH-MANIFEST.json. Checkout is frozen after this handoff.

## Actual change

The archetype is **log_dwelling**, not fort_structure. A new default-None, keyword-only `compound_clapboard_height_m` allows a declared lower-wall band on the independent connected-room path only. Cobweb selects1.30m, half its existing inferred2.6m wall. It follows only the exterior union boundary, clips every existing +Y front aperture/window, leaves upper logs and notched corners exposed, and uses the existing unpainted frame material (linearRGBA0.52,0.44,0.34,1; roughness0.86). It adds no material, image, texture, historic paint or new date.

The source is McKee’s account printed by Andreas: “the agency-house being afterward clapboarded part way up.” The height, corner clearances, exact extent and July1835 application are reconstructed. That wording does not establish the finish’s completion date; position, phase dates, footprint, all five rooms, roof forms/pitches, chimneys and current apertures stay unchanged.

## Actual checks

- `python3 tools/test_log_compound_clapboards.py`:4testsPASS. Validates invalid/boolean/nonfinite/extreme heights and unsupported plain/elbow use; actual exterior runs equal the footprint’s perimeter; physical emitted faces leave holes clear; face winding/caps/height correct; all existing body/roof/stack/dark-face geometry remains an exact prefix and total bounds stay exact.
- `python3 tools/test_log_compound_apertures.py`:complete existing ownerPASS.
- `/tmp/nov9-cobweb-group/check_controls.py`:loads actual baseline params/producer from Git, resolves all82 current registry defaults and builds old/new full pre-export accumulators with stable actual asset identities. All81 non-target geometry/material/confidence snapshots EXACT; every old constructor positional/keyword field/default and record parameter preserved. Target grows3342→5346verts and838→1339polygonfaces by adding the partial boards; this is NOT a native draw/payload measurement. New controls produce no registered variants.
- Actual name harvester flags exactly the one new construction-note path. Its proposed precise ignored declaration clears that path with no change to the record’s existing read-word/key sets; see NAME-POOL-TARGETED-PASS.json and BASELINE-NAME-POOL-READ-COMPARISON.json.
- `git diff --check`PASS.

The full name-pool CLI is NOT green in this sparse parcel: unrelated `data/traces/vectors/thompson_lots.json` is absent. Preserve that red and run the full owner in the integrated checkout after adding the supplied declaration. Early probe/test setup errors are honestly indexed in INITIAL-PROBE-ERRORS.md; that index is not a raw execution transcript.

## Root integration required

1. Integrate only the four patch paths (no shared docs/registries were edited). Append LIBERTY-SNIPPET.md, STATUS-SNIPPET.md and ROADMAP-SNIPPET.md using native compilers afterward; copy CHANGELOG-ENTRY.json to a suitable unique T-2374 entry file.
2. Add the exact `ignored.structures["phases[].form.compound_clapboard_height_m.note"]` supplied in NAME-POOL-DECLARATION.json, preserving all current declarations; run full name-pool check/self-test.
3. Enroll the new owner in check.sh and **genuinely measure it** with `node tools/measure_step_isolation.mjs --tool tools/test_log_compound_clapboards.py`, then audit isolation. No hand-authored row.
4. Rebind the current combined group and source before native. This producer change affects82 log_dwelling defaults/0variants: one intended Cobweb target and81 old controls here. Before other group changes, preserve962 foreign defaults and all6 foreign variants. If the Jail parcel changes another log target, adjust the intentional/control partition; don’t relabel it an unchanged control. `82-FAMILY-CONTROLS.json` retains actual before asset hashes/bytes/registry rows, no asset copies.
5. Genuinely regenerate the affected family on pinned Blender4.5.3; actual MASTER export/UV differences and derived WEB bindings must be audited, not predicted or hand-stamped. Then actual fixed-private-camera and app desktop/phone review, full integrated source/required checks and ordinary dev merge under your qualification.

## Fixed private picture proof

Actually viewed the full current1920×1042 panorama, sourcecrop955124dee76ee2d5585e0461688d9c141cad79a25d192248d8fca7c4377d4750 and current repaired modelcrop76920874cce6fc8ee17ba92313ca3aaa6f761df8c045288be6520bcb1c10b9e1. The currentMASTER is1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82; WEB99997b5f3935ceceddb072286387859a5d9a8dd3dfa112b64978d1213e20890e. Previous aperture/depth work is already merged and preserved.

`private-camera-used.json` is the unchanged07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977 camera from the immutable final PR1690 evidence folder. Its photo is relative `../chicago/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`. To preserve camera bytes, stage it under an external `.../review/` folder beside a read-only `.../chicago` alias to your full repo; its literal photo path then resolves without rewriting the camera. Use actual old/new GLBs and this same unsolved pose. Do NOT enroll this camera, invent a fit, promote grade, or call matches.

Whole compound width, wings/sub-roofs/junctions and finish interpretation remain open. This is one visible text-backed partial-siding increment, not a complete photograph match.
