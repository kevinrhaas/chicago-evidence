# Finite bounds diagnostic: PASS; main remains closed

Recovery isolated fixture ran 2026-10-21T22:48:26.318Z to 2026-10-21T22:48:27.458Z; PASS, no page/request errors, inputs unchanged, browser/server closed. No main world boot occurred. Prior successful diagnostic at 22:45:49 was recovered and preserved; its receipt and failed main-v1 receipt hashes remain unchanged.

The production merged meshes use local bounding boxes. Default Three Box3.setFromObject transforms those conservative boxes at yaw -3.075270142014009 rad (~176.2 degrees) and overestimates the actual bounds by up to 0.2556184413 m. precise=true instead enumerates transformed actual vertices and agrees with independent active source-frame enumeration. Manual merged-vertex enumeration independently agrees. Neither inactive retired meshes nor a terrain shift caused the mismatch: both reviewed GLBs contain exactly 26 active mesh nodes and zero inactive mesh references, with 51,876 source and actual merged vertices.

| Case | max precise source-bound distance (m) | tongue angle (rad) |
| --- | ---: | ---: |
| covered_w01_western_blue | 1.65475272549e-07 | 0.18578444010765166 |
| covered_w01_wolfpoint_oak | 1.91104444511e-07 | 0.18756896609746493 |

Full six min/max per-axis deltas for default/precise/manual versus authoritative active source vertices are retained in actual-recovered/receipt.json, at both original stands and actual runtime articulations. Production guard remains strict min/max vector distance < 0.0001 m.

For each model, an actual Float32 extremal canopy source vertex was increased by 0.0009999275207519531 m in an in-memory GLB copy. This changed the source max-Y bound by the same amount and was refused by the exact unchanged production vector-distance predicate. Actual GLB files remain untouched and their hashes match the frozen reviewed inputs. This is an extremal-source-frame bounds corruption detector: interior vertex changes need not alter bounds. Separate exact GLB SHA-256 guards protect asset identity.

Only shared main helper/caller changed: clearance uses setFromObject(group,true); successful runtime controls persist before clearance executes. Existing 22-image/four-page budget, guard thresholds, normal screenshots, lighting, app/model/source/index and publisher remain unchanged. Original helper/caller/manifest/plan preserved under main-v1-source/. The original main-v1 receipt retains its failed bounds verdict and no unsaved runtime-control result is inferred.

Both shared scripts pass node --check. No main retry was launched. Root must explicitly release the next main run after reviewing these hashes.

New shared script hashes:

- browser-control.cjs: `dd2f0d396f426e7d4436d25c0df133eafafa52bcc2f2b16c306f2bef9b818baa`
- capture.cjs: `9adb8e9426a188f328a18b729c0eadc37c9c95566f986b725906b9451dda9e72`
- MANIFEST.json: `383cb0f0a6e23f025691114bbd3169297e9938180db019bf75e7a8f2b07fda05`

Unchanged app HEAD: `2aebef95f6a5b6fa1bd8353db936c7674a73c32f`.
Unchanged index digest: `514767b0696eaf64c29bf45910bce05408a8c35ae950b96cb829cf52327844b8`. No unstaged tracked changes.
