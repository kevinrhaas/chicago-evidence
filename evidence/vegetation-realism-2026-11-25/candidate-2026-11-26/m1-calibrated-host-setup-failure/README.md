# Eligible calibrated host; publication setup failed before timing

Temporary owner-visible draftPR2382 targets the held feature branch and must never merge. Its app checkout is pinned to1605dcbd4b58bedf98084a16d4b32d95a59bd20e; the entire app treeb148a5508f0fce7169b905963180b4ac641ddc75 is byte-identical. Only the diagnostic workflow is added.

Run45946742086/job140333053812 received an actual four-core AMD EPYC7763 with all three stock desktop ceilings (Full13750, Balanced10500, Light7000ms). The CPU/source eligibility artifact and original ZIP digest are retained. Publication then failed because the older Ubuntu22.04 image's jsonschema module has no Draft202012Validator. **No timing measurement occurred; this is no performance verdict.**

The diagnostic-only follow-up611afa36783bfc87dbdc4311b7bd7c04dfeff453 installs modernjsonschema>=4,<5 before the canonical publisher. The exact app checkout, Node22/Playwright1.56.1, stock measurement, samples, viewport, raster, geometry, population and every CPU-specific ceiling remain. New hardware-probe run45955364389 is separate from the seven required ordinary core CI runs, which remain required. The original calibrated B4 failure and both uncalibrated reports remain in sibling evidence folders; the known timing hold is still open.

Only duplicate automatically-triggered Native workflows on these never-merge diagnostic branches were cancelled. The real core Native45944013491 passed all eight parts and its aggregate. The original duplicate's if-always aggregate remained after ordinary cancellation, so a scoped force-cancellation was needed; its exact outcomes are preserved. No app check was cancelled or waived.
