256 fictional photo faces for generic adults — T-3761, extends T-3746

all-256-rendered.jpg shows every actual Light rendered head. Individual page-01.png
through page-16.png retain larger views. source-before-after-full.png shows selected
face 189 in the extracted runnable viewer, with actual source/before/fitted geometry.
three-quarter.png, profile.png, phone-light-face-256.png and the four existing-resident
images show other actual renderer views. Images are screenshots, not retouched renders.

Download photo-face-library-256.zip (under 50 MB), unzip, and follow its README.txt:
  python3 -m http.server 3000
  http://localhost:3000/tools/photo_face_review.html
The archive includes the required local JS module closure, calibrated bodies, morph kit,
all source previews and all sixteen face/hair texture pages. No network model is needed.
The source originals, offline fitter and pinned landmark/fit recipes are in chicago PR2355:
https://github.com/kevinrhaas/chicago/pull/2355

The catalog preserves the first sixteen and adds 240 generated fictional adults, 128 men
and 128 women in total, with apparent ages 18–87. These are not historical likenesses.
Source credit: synthetic_photo_face_pilot_2026 and synthetic_photo_faces_256_2026.
The same single-photo command accepts a registered historical photo for the next phase.
The single-photo test here deliberately uses a fictional source and full camera search.

Town preview: photoFaces=pilot. A shared 1024-square crowd atlas and ONE resident-or-
loading nearby 1024-square face page cap added RGBA8/mipmapped face textures at 10.67 MiB.
Other faces retain their own crowd versions. Existing body, clothing and whole-scene
costs are additional; visible-person and body LOD limits remain the existing engine’s.
The review loads sixteen heads on each page and releases its renderer/caches on page
navigation. Light uses a 1.33 MiB face page; Full 5.33 MiB. The optional scalp trial adds
a same-sized hair page. Existing styles in source-based colours are the default.
Photographed-scalp trial hairlines/coverage still need work; it is labelled separately.

population-and-cache-checks.txt: 1,234 drawn people; 1,048 generic adults on 1,076 bodies
use 201 different faces; 160 child and 27 personal-face assignments protected. Nearby
page priority, one resident-or-loading slot, late delivery, 32-page traversal, failures,
retry and disposal pass. resident-page-checks.json verifies actual shader UVs and texture
sizes while moving four real residents between pages, with intact iris detail/lid tone.
The first concurrent screenshot attempt timed out; the later resident run passed.

browser-checks.json covers all 256 fitted heads on sixteen pages, only current-page
atlas/thumbnail requests, real Previous navigation, no browser errors, Full geometry
and phone layout. package-checks.json verifies the extracted archive, selected face 189
(exactly two before/after figures with distinct body geometry), phone face 256, optional
scalp trial, single-photo review and no missing files. writer-reproduction.json records
two actual offline writes reproducing 325 outputs and repairing a damaged final page.
Read-only fitting parents remain unchanged; the proof does not call the uncommitted
feature tree Git-clean. The writer’s full-manifest ordering remains explicitly pending.

Performance limit: available browser is SwiftShader software. This evidence does not
qualify a real low-power GPU or whole-town crowd performance. A 256-face library is not
256 people drawn at once. Historical likeness and hair review, target-hardware timing
and default rollout are pending. Current code/preflight/CI status is on PR2355; published
renderer stages 2–15 remain outstanding from the original pilot handoff.

Local preflight passed with CHECK_PART=2/8: 182 steps, 39 self-tests, plus PR changelog/id checks. Other parts and complete CI are not implied by that result.

Measurement export is also verified: it correctly says 16 drawn heads from a 256-entry catalog. The measured renderer is SwiftShader software; a local gate was concurrent. measurement-context.json marks this as UI/export validation only, not a hardware performance result.
