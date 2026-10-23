# T-2375: Dearborn board-parapet implementation proposal

Status: UNAPPLIED proposal. No tracked repository file, ticket, branch, grade,
publisher output or geometry asset was changed. No match verdict is claimed.
Parent coordinates claims, integration, actual baking, cameras, app checks and PR.

## Concrete change

`T-2375-board-parapet.patch` adds opt-in `railing_kind: board`, leaving `pole` as
the default and leaving disabled rails unchanged. It adds the field to CONSUMED,
resolves and validates it, implements the horizontal-board parapets, enables them
only on Dearborn, and appends a reconstruction liberty. It contains four files:

- generators/archetypes/bridge_timber_params.py
- generators/archetypes/bridge_timber.py
- data/structures/dearborn_street_drawbridge.json
- docs/LIBERTIES.md

Relative paths in the actual unified diff start with `chicago/4d/` from the code
repository root. The `before/` and `after/` directories preserve exact snapshots
used for the proposal and focused validation; they are not checkouts/worktrees.
`LIBERTY-entry.md` also provides the entry separately for safe append at a newer
working tree's current end. Do not overwrite or move newer liberty entries.

## Evidence read directly

Both actual images were opened and inspected:

- chicago/reference/images/chicago/chicago_dearborn_drawbridge_1834.png,
  the Andreas 1884 plate, printed p. 631 (1920 x 1346).
- chicago/reference/images/chicago/chicago_dearborn_street_bridge_1834.jpg,
  the second engraving (1501 x 969), visually corroborating boarded sides.

The geometry-source citation is `andreas_1884_dearborn_drawbridge_plate`, public
 domain by its documented 1884 publication, with the original page link retained:
https://archive.org/details/historyofchicago01andr/page/n1295/mode/1up .
The second website record remains check_required and is not used to license this
new geometry. Both pictures are retrospective: boarded side treatment is inferred
form, never a coordinate, width, dimension or surveyed historical clearance.

## What is reconstructed

Five courses, 162 mm board heights, 40 mm thickness, 10 mm course gaps, 40 mm lower
clearance, 200 x 60 mm cap and joint details are reconstruction choices. Overall
parapet height stays at the former 0.95 m, with approximately 2.2 m post bays.
Boards and caps break at post bays, both draw ends and the two-leaf centre joint;
no new board/cap becomes a continuous timber across a moving leaf.

A refinement to the previous proposal prevents cap/post overlap: in board mode
only, post heads end at the cap underside (0.89 m above deck), avoiding exposed,
coplanar cap/post top faces. Default pole mode retains the former 0.95 m posts
and every prior emitted mesh-list value. The pictures do not specify these details.

## Validation actually completed

Run from anywhere in this workspace:

    python3 /tmp/chicago-next-model/T-2375/validate_proposal.py

The script runs the real generator and common mesh helpers in pure Python;
Blender object/material emission alone is stubbed, following the established
repository test_facade_board_faces.py pattern. It does not prove Blender export,
textures/normals, GLB contract, baked asset freshness or appearance in the app.

`validation.log` and `validation.json` record success:

- All six current bridge phases resolve. Default pole and disabled-rail geometry
  is exactly identical to the current generator's vertex/face/confidence/material
  mesh lists, including Dearborn with its old pole rail.
- Proposed Dearborn selects board, the parameter is consumed and inferred, and
  the actual full generated mesh differs. Non-railing geometry is unchanged.
- Board/cap boxes do not cross draw ends or the leaf meeting line. Geometry is
  finite, positive, nondegenerate, symmetric, within intended overall height and
  free of cap/post overlap. Output has 27,100 vertices and 6,711 polygon faces;
  this is an in-memory mesh, not an exported/baked GLB or triangle-count claim.
- Invalid kind values and board-without-railing fail direct and phase validation.
- `mutation-cap-overlap.log` records the expected assertion failure when the old
  cap/post overlap is deliberately restored. The unmodified proposal passes again.
- Proposed structure satisfies data/structures.schema.json with date checking.
- Both proposed Python modules compile.
- `git apply --check` succeeded against the parent's checkout at handoff creation.

## Exact freshness scope

`freshness-scope.json` records current input hashes and manifest rows for:

1. dearborn_street_drawbridge__draw_1834.glb
2. lasalle_slough_crossing__crossing_1835.glb
3. north_branch_bridge__log_1832.glb
4. north_water_slough_crossing__crossing_1835.glb
5. slough_log_bridge__log_1833.glb
6. south_branch_raft_bridge__log_1833.glb

The archetype code hash changes for all six. Also, `railing_kind` is a dataclass
field and enters every resolved parameter document, including default pole on the
other five. A Dearborn-only bake leaves five stale recipe/manifest entries even
though their default geometry is unchanged. Rebuild/refresh them via the supported
build path; do not exempt stale records or hand-assert a new bake.

## Integration and remaining acceptance

The old proposal's generator/parameter hashes still matched this snapshot. The
Dearborn structure gained `built` and documented_range.from_is in intervening date
work; these are preserved. LIBERTIES has newer entries, so this proposal was
rebuilt against its current end. Exact four-file before/after hashes and snapshot
head are in checkpoint.json. If the parent appends Hogan or other liberties first,
append LIBERTY-entry.md at the new end rather than inserting ahead of new entries.

Before applying, check live rival work/claims and inspect the diff. Parent must
record the change in STATUS, ROADMAP and a visitor changelog entry. Bake affected
assets with the supported pinned workflow, refresh derivatives/manifests/sidecars
and asset license provenance, then inspect source credit on the bridge card at
mobile and desktop. Solve both actual image cameras, render before/after and
review differences; do not use the previous exploratory 21.64 px fit as an accepted
camera. Both drawings show a raised/bent central deck profile that remains flat
here. Approaches, central profile, proportions, supports, lighting/materials and
remaining image comparison are unresolved. Run required focused checks, check.sh,
preflight and relevant published smoke before committing/merging. T-2375 remains
open until its full image gate and app acceptance pass.
