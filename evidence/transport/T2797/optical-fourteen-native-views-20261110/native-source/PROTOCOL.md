# Fourteen native optical plates — prepared, unrun

One originalSUP120 cell, same4GiB RAM /512MiB workspace /1GiB tmp floors and sole
canonical owner lock. Forecast<=60seconds, <=128MiB own output. Fresh output only;
any real failure/timeout is retained and stops the attempt. No auto-fit or retry.

Inputs: existing installed-source optical near b5b183b4 /mid16daaf1d (not a live
hosted fetch), and temporary full-proof-bound optical near591645f1 /mid4d6df0c3.
All four use exactly the same original material definitions, including declared
thin-sheet glass0transmission/0.14opacity/IOR1.5. Actual native loaded material
values, full geometry inventory, original node transforms and actual door endpoint
are checked; no visual material overrides, hiding, recentering or rescaling.

The fourteen original PNGs are declared in protocol.json:

- Six1280x800 full carriage plates: OLDclosed, NEWclosed, NEWopen−65 for each LOD.
- Four1280x800 lower-bow details: OLDclosed/NEWclosed for each LOD. This declared
  crop checks NDC coverage of both actual right step-support source occurrences;
  the complete carriage stays rendered and surrounding geometry may crop.
- Four390x780 phone plates: NEWclosed/NEWopen for each LOD. Separate true mobile,
  touch-enabled browser context, DPR1, same full-carriage eye/target/horizontal span
  with predeclared aspect-correct vertical bounds. This does not test touch actions.

Exact camera/studio/viewport choices are frozen before launch. Full plates require
all actual loaded vertices inside the frustum. Detail source-coordinate readback
already places all eight old/new actual right supports inside its fixed frustum;
the browser independently repeats this on the actual loaded indexed GLBs. No
native render has occurred during preparation. All fourteen use original native
C02 studio hemisphere/sun/ACES/sRGB/shadow conventions, not production town lighting.

Vendored Three0.185.1 and actual GLTFLoader remain unmodified. Exact local HTTP
routes and every browser response body are SHA checked; unexpected origin, request
failure, page error, console error or WebGL error is fatal. Source/asset hashes are
checked before/after. Pending body tasks drain, each study renderer/model is
disposed, both contexts close, browser and local server close, and original
supervisor owned cleanup must leave zero children.

Success only means14original native PNGs were captured with intact evidence.
ROOT must personally review all images, including actual new seam/cap, original
glass/rail silhouette,188mm lower-bow trial, near/mid and phone appearance. All
qualification flags remain false; no near_mid_visual opt-in, installed delivery,
actual tier selection, town placement, horse/driver, live interaction, boarding,
photographic/world acceptance or release follows from this studio alone.

Proposed output:
`/tmp/T2797-OPTICAL-VISUAL-ATTEMPT1-20261110/results`

After final source review:

```text
source /workspace/.cloud-setup/transport-activate.sh
python /tmp/T2797-DOOR-PRODUCER-PREP-20261110/run_guarded_own_task.py /tmp/T2797-OPTICAL-VISUAL-ATTEMPT1-20261110 120 nice -n 10 node /tmp/T2797-OPTICAL-VISUAL-PREP-v1-20261110/capture-optical.cjs --output /tmp/T2797-OPTICAL-VISUAL-ATTEMPT1-20261110/results --binding-sha PREPARATION_BINDING_SHA
```
