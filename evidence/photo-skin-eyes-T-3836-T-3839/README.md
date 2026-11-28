# Photo skin and fitted eyes — T-3836, T-3839

These are actual app renders from the generated published mirror, using the app’s materials, world lighting, people and source-derived textures. The review camera is framed on each person and neighbouring figures are temporarily hidden. No image generation or retouching was used for these captures.

Candidate source tree: `5a34d5c01501c8529c95256bba089646020ab369`, based on `bca15881e7343f15182fa002daaa9da8df132faf`. Every final PNG has a sidecar recording its person, source tree, loaded module hashes and image SHA-256. Full repository and published desktop/mobile release qualification is in progress; these images do not establish deployment or physical-GPU performance.

## Martha’s nose

The old importer preserved circular scan-shadow patches at three nasal landmarks, producing extra dark dots under the nose. The corrected importer restores that skin while the fitted 3D nose supplies its own shading. The original photograph and fitted head remain unchanged.

| Earlier native render | Corrected native render |
| --- | --- |
| ![Martha before nasal-shadow removal](before/martha-before-nose.png) | ![Martha after nasal-shadow removal](final-skin-native/martha-front.png) |

## John’s moustache

His existing source portrait shows a white moustache. The earlier candidate painted dark scan shadows around it. The corrected texture uses a reviewed silhouette and the existing grey-hair palette, without a second generated moustache layer.

| Earlier native render | Corrected native render |
| --- | --- |
| ![John before moustache correction](before/john-before-moustache.png) | ![John with corrected white moustache](final-skin-native/john-front.png) |

## Skin and profile views

| Person | Front | Profile |
| --- | --- | --- |
| Martha Williamson | ![Martha front](final-skin-native/martha-front.png) | ![Martha profile](final-skin-native/martha-right-profile.png) |
| John Glessner | ![John front](final-skin-native/john-front.png) | ![John profile](final-skin-native/john-right-profile.png) |
| August Billings | ![August front](final-skin-native/august-front.png) | ![August profile](final-skin-native/august-right-profile.png) |
| Marie Otis | ![Marie front](final-skin-native/marie-front.png) | ![Marie profile](final-skin-native/marie-right-profile.png) |

[Frances Glessner front](final-skin-native/frances-front.png) and [Martha’s opposite profile](final-skin-native/martha-left-profile.png) are also included.

## Eyes and the owner’s visual benchmark

The owner identified Sarah Grey’s current appearance as the best result seen. Her earlier full-head photographic skin is preserved. Newer atlas faces retain their own source photographs and fitted heads; monochrome archival resolution and scan cleanup limit the detail that can be recovered. This is a visual benchmark, not a claim that every archival image can supply the same detail.

| Person / detail | Actual app render |
| --- | --- |
| Sarah Grey / Balanced | ![Sarah Grey](final-native/sarah-balanced-front-in-app-face.png) |
| William Grey / Balanced | ![William Grey front](final-native/william-balanced-front-in-app-face.png) |
| William Grey / oblique | ![William Grey oblique](final-native/william-balanced-oblique-in-app-face.png) |
| Elizabeth Grey / Light | ![Elizabeth Light](final-native/elizabeth-light-front-in-app-face.png) |
| Elizabeth Grey / Full | ![Elizabeth Full](final-native/elizabeth-full-front-in-app-face.png) |
| Dorothy Sterling / Full | ![Dorothy Full](final-native/dorothy-full-front-in-app-face.png) |
| Alice May Stirling / Balanced | ![Alice Balanced](final-native/alice-balanced-front-in-app-face.png) |

[390 × 780 viewport, Alice full body](final-mobile-native/alice-mobile-in-app-body.png). This is Chromium at a phone-sized viewport, not physical iPhone or Safari qualification.

## Preservation and budgets

All 411 original library photographs, head-fit landmarks and shape values, source hair atlases and generic selection tones are preserved. The 52 derived face sheets change; atlas dimensions and GPU bytes do not. The existing ceiling remains 12,873,272 face texture bytes, with at most one shared detail page using 5,592,406 bytes. Eyes add no vertices, triangles, textures, lights or draw passes; private fitted eye position buffers are bounded by the existing detail tier.

Twenty-seven importer regressions pass, including the nasal-shadow regression, unsupported-pixel isolation and exact calibrated-body fallback. [Preservation proof](skin-rebuild-preservation.json), [canonical rebuild](skin-canonical-nose-rebuild.json), [visual manifest](visual-manifest.json) and the complete original native declaration [catalog](step-catalog.json) are included. Full release receipts will be added when qualification completes.

Unseen profile details and colour reconstructed from monochrome remain declared liberties. Hair-card edges, limited archive resolution and thin lower sclera in William’s close-up remain visible limits; this is not a claim of photographic perfection. T-3553’s photo-ingestion page/command and physical-GPU crowd timing are outside this completed correction and remain outstanding.

## Reusable capture template

![Six-view face-matching reference template](face-matching-reference-template.png)

This template is a synthetic illustration generated at the owner’s request on 28 November 2026, not an app render or a photograph of a historical person. The six views define the target input coverage: front, left/right three-quarter, left/right profile and rear; a separate smile/teeth image is optional. Left/right names refer to the visible side of the subject. Original individual images are preferred over a compressed collage.
