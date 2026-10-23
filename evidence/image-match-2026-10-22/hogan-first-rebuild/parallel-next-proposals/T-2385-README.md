> Subsequent isolated preview: pinned Blender 4.5.3 exported the copied proposal and photo_match rendered it successfully. The actual comparison was inspected and says `differs`. See `preview-root/README.md`, reports, logs, GLB and review images. This did not apply the patch or update a repository manifest; references below to unrun Blender/render validation describe the initial focused-check stage.

# T-2385 — unapplied first Tremont form/fenestration implementation

Status: implementation proposal only. Parent integrates centrally. No tracked file, ticket state, branch, publisher, gate, Blender installation or browser was changed/run by this proposal. T-2385 remains open; the existing camera comparison says `differs`.

## Apply and reproduce

`T-2385.patch` is a standard unified diff for the **chicago repository root**. `git apply --check /tmp/chicago-next-model/T-2385/T-2385.patch` passed against the shared checkout on 2026-10-22; the patch was not applied. It touches:

- `chicago/4d/generators/archetypes/frame_tavern_params.py`
- `chicago/4d/generators/archetypes/frame_tavern.py`
- `chicago/4d/data/structures/tremont_house_1.json`
- `chicago/4d/docs/LIBERTIES.md` (append only)

Copies of the three code/data outputs are under `proposed/`; `liberty-entry.md` is the separate append text. `checkpoint.json` pins the source-file hashes and base HEAD. Recheck before applying: the shared checkout has other work in progress and the liberty EOF hunk can become outdated. Never discard another agent's liberty entries. The patch includes no generated mesh, manifest, sidecar, accepted reference view, changelog, STATUS or ROADMAP update.

Focused checks can be rerun without repository edits:

`PYTHONPATH=/workspace/shared/python python3 /tmp/chicago-next-model/T-2385/test_proposal.py`

The script imports only the copied proposed modules plus existing shared materials/openings/mesh helpers. `bpy` is an import stub and `MeshBuilder.to_object` returns accumulated geometry rather than exporting a Blender object. This is a geometry/parameter regression check, **not a supported content bake or Blender export proof**.

## What visibly changes after a real build

The existing `frame_tavern` archetype gets an opt-in `corner_gable` elevation scheme. The current 15.24 × 9.14 m footprint, position, bearing and documented phase dates stay byte-equivalent as JSON values. The ridge remains along the long u axis, so the short gables stay on x faces and the long elevations on y faces.

The Tremont's form uses three floors instead of two, with three bays across each short gable and five along each long wall; centred ground entrances replace each face's middle window. Shutters are solid closed boxes with real thickness on both wall axes. Lap-course relief now reaches all four walls for this option. Other schemes' geometry is unchanged.

What Gifford actually depicts: three full floors; three-bay short gable; five-bay long elevation; shutters and centred ground entrances. What this proposal reconstructs: 7.8 m wall height (the previous record's existing 2.6 m-per-floor alternative), equal bay stations and floor heights, existing 0.85 × 1.35 m sashes and 1.2 × 2.1 m doors, plain shutter sections/colour and the two concealed faces. Both unseen faces mirror the visible ones, including their entrances: **four model entrances are a reconstruction, not a historical door-count claim**. This avoids silently assigning the undated drawing's pictured pair to named compass faces. Green shutters are a stock-palette choice; the monochrome reproduction supplies no original paint colour.

The source is N. Roswell Gifford's drawing reproduced by Chicagology as “Tremont House No. 1”, https://chicagology.com/prefire/prefire021/, source ID `gifford_tremont_house_no_1`. Owner approved attributed project use on 2026-10-22; no public-domain finding is made. The source remains undated within the first hotel's 1833-1839 life, so using its form for 1835 is explicitly inferred. The structure note preserves the superseded text-only two-storey argument, and explicitly records the unresolved tension with the Saloon's first-three-storey shorthand. No documented construction date, exclusion or geographic control is rewritten.

## Focused results

`focused-checks.log` records:

- Existing resolved parameters **and accumulated geometry/materials identical across 24 phases of frame_tavern records**. One of those is the Sauganash's non-manifest `log_1829` phase; the current actual frame_tavern inventory is 23 assets.
- Proposed actual Tremont phase resolves; schema passes; position/footprint/range unchanged.
- Three-floor corner scheme generates 44 windows, four reconstructed mirrored entries and 88 closed shutter leaves; all vertices and confidence values finite/in range; shutter thickness faces nondegenerate on both wall axes.
- Eleven incompatible/narrow/too-low configurations rejected, including wrong ridge axis/roof, unsupported louvring, chamber-count override, low floor heights and unhandled wings/gallery/frontispiece.
- Turning shutters off emits no shutter faces.

## Exact staleness and supported build scope

`staleness-scope.json` names all **23 committed frame_tavern assets**. `generators/mesh_inputs.py::_code_shas` includes the whole `frame_tavern.py` geometry module in every such recipe. Its changed bytes therefore stale every listed manifest recipe even though the disabled-option geometry is identical for the other buildings. No common generator module is edited, and there are currently no frame_tavern entries in `assets/manifest.versions.json`.

Rebuild the listed structure IDs through the supported pinned content-build path (on a permitted content-build runner, not by installing Blender here), then refresh master/web manifests, derivatives and scene sidecars. The actual Tremont geometry changes and cannot be fixed by restamping its recipe. Do not hide recipe staleness or claim these CPU checks produced fresh GLBs. Selecting all listed structure IDs with `tools/bake.sh --only <comma-separated-ids>` covers this current inventory; re-evaluate if the inventory or shared code has changed.

## Remaining integration and match work

1. Check claims/rival changes, inspect/apply the patch, resolve the liberty append without overwriting other entries. Add a meaningful durable focused test if adopting the implementation and include it in the repository's test workflow.
2. Build/derive via the supported path, inspect both changed and default-option outputs, and check opening normals/materials, shutter overlap, siding/trim interfaces and wall/floor proportions in an actual GLB.
3. Recompute official derived structure grades, scene sidecars and source/picture indexes. The reasonable Gifford picture should be reachable with its credit on the building card; do not hand-edit a grade. The prior inferred grade currently says no picture has been found.
4. Refit the provisional camera against the rebuilt envelope. The baseline camera was fitted to the old 5.2 m-high two-storey envelope and is not a solved calibration. Keep all differences open until actually reviewed.
5. Still visibly unresolved: gable lunette; raised landings/steps/rails; flagstaff/flag; source-specific stack count/stations and roof profile; source/scene dating; materials/tones; street context. Current 38° roof pitch and two stacks are retained deliberately for this first form step.
6. Run required desktop/mobile card/app validation, focused checks, full check/preflight, and add changelog/STATUS/ROADMAP entries with honest scope. PR into dev and merge green. This proposal alone cannot close the original image-match ticket.
