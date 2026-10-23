# T-2385 — first Tremont rendered comparison baseline

Status: rendered exploratory baseline, `differs`. No repository or ticket file was edited. The owner-approved Gifford drawing is credited to N. Roswell Gifford, reproduced by Chicagology as “Tremont House No. 1” at https://chicagology.com/prefire/prefire021/. This is project reference-use approval, not a verified public-domain ruling. T-2385 remains open.

## What is ready

- `gifford-provisional.json`: runnable /tmp camera, with absolute local photo path.
- `gifford-provisional.repository-camera.json`: identical framing with a portable path, intended only if adopted under `data/reference_views/tremont_house_1/gifford-provisional.json`.
- `gifford-provisional-side-by-side.jpg` and `gifford-provisional-render.png`: actual committed-GLB render, inspected visually. Renderer exited 0 using installed Chromium; no publisher or heavy gates ran.
- `gifford-provisional.match.json`: actual mesh/camera/photo hashes, reviewer verdict `differs`, explicit open differences. Its camera hash is for the runnable /tmp camera. Do not transplant the match record beside the repository-path camera: changing the path changes its hash; rerender there.
- `fit_camera.py` and `camera-fit.json`: reproducible six-point bounded pinhole fit, manual picks, predictions and residuals. Requires NumPy/SciPy already available via `PYTHONPATH=/workspace/shared/python`.
- `checkpoint.json`: source, mesh and input hashes plus execution receipt.

The image is 1637 × 796. Framing uses eye [-11.9284, -11.0330, 2.4222], yaw 45.3203°, focal length 575.427 px, principal point [1018.9117, 433.8643]. It fits three approximate wall-bottom corners and their eaves against the current reconstructed 15.24 × 9.14 m, 5.2 m-high wall envelope. Point RMS is 17.230 px; maximum point residual is 25.363 px. This is **not a solved historical camera**. Dimensions are current reconstruction choices, the mesh has the wrong storey count, and the retrospective drawing has inconsistent convergence. No real-world camera location, dimensions or geographic placement follows from this fit. The global image frame is retained so future comparisons use the same pixels.

## What the actual render shows

The current mesh has two floors, a blank short gable, unshuttered long-elevation windows, two simple stacks and no flagstaff or entrance landings. The source has three floors, three bays across its short gable, five bays along the eaves elevation, shutters, a gable lunette, centred entrances/raised steps, more complex roof stacks and a flagstaff. Current roof ridge is around y=239 against source y=277 in this framing. This is a visible silhouette difference, not a calibrated roof-pitch measurement. The match record lists these differences individually.

## Next implementation step

1. Resolve the pictured massing as an explicitly retrospective form inference, retain the documented corner/date and current reconstructed envelope until a better warranted size is chosen, and supersede the structure's stale claim that only an uncredited modern sentence supports three storeys. The actual Gifford picture is independent visual evidence of the depicted form; it still does not date every feature to 1835-07-01.
2. Add a dedicated opt-in elevation treatment or generalize the existing one. Simply setting `elevation_scheme=gable_front` does not work here: validation requires depth > width, its fenestration assumes short gables at y faces, and it rejects shutters. The current rectangle is 15.24 in u × 9.14 in v with short gables at x faces. Rotating the building alone makes the short/long facades wrong. Keep source-induced form changes distinct from any geographic reorientation.
3. Add the short-gable three-bay openings/lunette, shuttered three-floor long elevation, appropriate entry/step/roof features and explicit reconstruction liberties. Examine stack count/stations at full resolution before encoding them; source monochrome tones do not attest original paint colours.
4. Use the supported pinned bake workflow; refresh manifests/derivatives/sidecars. Linking this reasonable picture or adopting a camera can change the derived structure grade and picture card: rerun the official grade/compiler pipeline rather than hand-editing a grade.
5. Refit camera with the corrected envelope, render all relevant images again, inspect each actual side-by-side, and only accept when differences are resolved. Check the credited image on the desktop and mobile card, then required gates/PR/merge. No part of this handoff closes T-2385.
