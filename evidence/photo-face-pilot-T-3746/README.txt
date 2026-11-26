T-3746 PHOTO FACE PILOT — REVIEW EVIDENCE

The PNGs are unretouched browser screenshots of the actual glTF meshes and
Three renderer. 01 and 02 compare fictional source / old generic / fitted photo.
03 and 04 show the same female sample from three-quarter and profile.
05 shows all sixteen using Light. 06 is the 390 x 780 phone review.
07 shows four existing generic resident models with photoFaces=pilot.
08 shows those same resident models on the default appearance.

The single-photo command, credited sources, generator and rollout code are at:
https://github.com/kevinrhaas/chicago/tree/steward/t3746-photo-face-pilot-16/chicago/4d

photo-face-pilot.zip is an offline review viewer. Extract it and follow README.txt:
python3 -m http.server 3000
then open http://localhost:3000/tools/photo_face_review.html
No internet assets or API credentials are required to view it. It contains both
Light and Full body/texture tiers. The extracted Full face 16 review was checked
for missing dependencies and browser errors.

The existing-resident opt-in shares one 512 x 512 face atlas, 1.33 MiB RGBA8 with
mipmaps for all sixteen. Review Light adds one hair atlas too, 2.67 MiB total;
Full adds 10.67 MiB for both atlases. Existing body assets and whole-scene costs
are additional. No default population assignments are changed.

EYE CORRECTIONS
Preserve iris texture detail through the recorded-colour material layer; avoid
applying a texture gain as a flat eye colour; preserve attested eye colours.
Measure sclera tone, fit pupil positions and iris radii within bounded geometry
adjustments, match lid rest to measured source aperture, soften corneal glare,
and avoid painting pupils or additional eyebrows onto the skin patch.

LIMITS
Synthetic sources depict fictional adults, not archival people. Profile depth,
unseen hair and body/clothes remain reconstructed. This is a visual pilot, not
likeness approval. The review hair proposal is not the town default.
software-measurement.json explicitly reports SwiftShader software rendering.
Its 833.3 ms median / 1616.6 ms p95 frame interval is not a hardware-GPU pass.
It includes 16 LOD2 figures, 152 draws, 176,568 triangles, pixel ratio 1.
Hardware and complete-town low-power-PC performance still need measurement.
The viewer exports the same report on the PC where it runs.

browser-checks.json records desktop 1180 x 1050 and mobile 390 x 780 with no
browser errors. downloaded-measurement.json is the JSON exported by the page.

CURRENT POPULATION COVERAGE
All 1,234 drawn people were checked against their actual scene body assignments.
1,048 generic adults get source-fitted photos across 1,076 assignments. 160 child
and 27 personal-face assignments are protected. Multiple bodies retain one face.
resident-eyes-checks.json verifies the four shown residents keep iris textures,
softened sclera and the same source-guided lid rest as the town actor path.

PUBLISHED FUNCTIONAL CHECKS
Phone stage 1: 96 passed, 0 failed, 6m11s. Desktop stage 1 rerun alone:
96 passed, 0 failed, 11m36s, zero page errors. That desktop run exceeds the
10-minute foreground budget; the first concurrent run timed out settling a
scene capture. These are stage 1 of 15, not the complete renderer gate.
The photo review and population contract checks pass. Real GPU qualification
and default population rollout remain outstanding.
