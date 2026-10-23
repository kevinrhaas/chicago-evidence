# T-2372 next step — provisional school image comparison

Status: research/evidence only; no tracked files, ticket state, branch, structure
data, accepted reference view, grade, publisher output or geometry were changed.
Original T-2372 remains open. The inspected comparison verdict is differs.

## Files

- shore-provisional.json: directly runnable temporary camera, with an absolute
  photo path valid in this workspace.
- shore-provisional.match.json: actual rendered mesh/camera/photo hashes, reviewed
  verdict differs and explicit open differences.
- comparisons/shore-provisional-side-by-side.jpg: actual source|committed-GLB result.
- comparisons/shore-provisional-render.png: original render copied byte-for-byte
  from photo_match's temporary output.
- preview-projection.json: diagnostic projections of existing model points.
  These are not measured historic dimensions, camera controls or fit residuals.
- source-context.json: citation, reproduction credit and dated owner approval.
- shore-provisional.repo.json: alternative camera with relative photo path for
  a research-directory integration; changing the path changes its camera hash.
- T-2372-camera.patch: UNAPPLIED unified diff adding a research camera and README
  under docs/RESEARCH/chappel-school-T-2372, not data/reference_views.

The patch must remain unapplied during this baseline evidence-only handoff.
It is available for recovery and an explicitly selected later research integration.
Do not copy the standalone match's camera hash onto the repo-path camera: rerender
the latter if it is ever integrated. No accepted camera is enrolled in this step.

## Reproduce current baseline

Working directory: /workspace/chicago/chicago/4d

PW_EXECUTABLE=/usr/bin/chromium node tools/photo_match.mjs /tmp/t3053-next-parcels/T-2372/shore-provisional.json --out /tmp/t3053-next-parcels/T-2372/comparisons

A rerun with identical camera/mesh/photo keeps the reviewed differs verdict.
The tool starts its own ephemeral local server and closes the browser/server at
completion; no publish command is involved. It needs the existing Playwright
module and installed /usr/bin/chromium. No installation was performed.

Initial launch without PW_EXECUTABLE failed before browser start because the
default Playwright download was absent. Reusing /usr/bin/chromium corrected that
runtime selection. One actual focused browser render then completed with exit0.
No full gates, schema/browser suites or publishing were run by this agent.

## Preview rationale and limits

The deposited image is640x368px. Existing T-0649 readings put the gable apex at
(561,158), doorcase head near y216.75 and distant horizon near y215+/-3. The
front-wall foot near y280-286 is an approximate visual reading, obscured by
people and grass. These are image-space anchors, not a surveyed construction.

The camera uses principal point(566,215), focal2050px,
eye[-10,80,2.625]m and yaw169.613672degrees. All pose/scale numbers are reconstructed
preview choices: they frame the building at the picture's right crop and roughly
align the current mesh's wall-base/eave/roof heights so differences are visible.
The existing model's7.315x5.486m footprint is itself reconstructed. No independent
metric length, station, residual or historical field of view is asserted.
Overcast light is a provisional review choice; source tone is not historical color.

## What the actual comparison shows

- The source doorway is in a gable front; the model's entrance is under a long
  eave, with its ridge running across the view.
- With approximate vertical alignment, the model facade is materially too wide.
- Door/window heads sit lower than the drawn ones.
- The mesh has a closed board door; a woman stands in the drawn dark doorway.
- Roof shingles/shakes resolve in the drawing but not on the smooth render.
- Wall/chink/roof tone differs; lighting and material causes remain to separate.
- The crop does not establish rear, right return, chimney absence or true color.

First visible modeling direction: provide an opt-in gable-front/ridge-axis path
or an appropriately justified footprint/frontage change, then refine opening
positions and roof covering. Do not rotate geometry or change dimensions simply
to drive a guessed camera green. Preserve evidence tiers, source citation and
the still-unresolved pictured-building identity.

## Attribution

Artist unidentified; reproduced by the Digital Research Library of Illinois
History Journal in its2018 Eliza Chappell article. Keep this credit and the
source link with any displayed reference or comparison:
https://drloihjournal.blogspot.com/2018/01/eliza-chappell-the-first-chicago-teacher-paid-by-public-funds-in-1833.html

Owner approval is project-specific attributed reference/comparison/display use
(T-3053,2026-10-22). It is not a public-domain or copyright-holder grant.
The full dated source context is retained in source-context.json.

## Grade/identity safeguard

An enrolled image-gate camera can cause automatic attested grading. Because the
school/annex identity remains unresolved, this provisional camera is staged only
in research/evidence. Do not silently enroll it under data/reference_views.
No new rights decision is needed for this approved project use; identity and
camera/geometry work remain practical research/modeling tasks, not an
owner-approval blocker.
