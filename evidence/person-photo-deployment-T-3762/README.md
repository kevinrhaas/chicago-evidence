# Named photo deployment and the Stirling reference models — T-3762

The existing fitted heads used generic skin. This applies retained photographic detail to each exact person/scene and adds two separate owner-chosen likenesses for Dorothy Sterling (younger daughter, 19 in 1904) and Alice May Stirling (older daughter, 20). Their stored project references are edited period portraits and neutral texture companions. Modern original uploads are not published.

Coverage: twenty own-person archive portraits, five previously labelled staff references, two existing Grey full skins and two new Stirling references. The atlas contains 27 entries: 26 currently cast people (27 body assignments, because Charles also drives) and the retained uncast Kate Ryan reference. William and Sarah retain their full skins. No new actor or historical presence is inferred from a photo. Twenty-five existing heads and all generic adult/child pixels remain unchanged.

Current source: `c72869d67626f0264da7277a179b6659e456d92c`. Renderer, data and asset trees remain byte-identical to the reviewed client revision `c9b3417f8c0f1a4ebee7cae969028b1769a2aa6d` in kevinrhaas/chicago. Source PR: https://github.com/kevinrhaas/chicago/pull/2371. All four local gate sections pass (361/361/362/361 steps) on the first integrated tree, recorded by tree hash in `historical-local-complete-gate.json`. The latest dev integration was rebuilt through all 209 steps, seven second-pass steps and a settled 60-step tail. Every generic and named photo-generator input remains byte-identical. Final targeted checks pass after integration. The published local mirror reports c9b3417f8c and passes served-code, three-library, 19-detail-page, two-period-portrait and 7,610-assignment checks (`historical-final-published-verification.json`). Hosted eight-part gate, human-rendering checks and all 30 published viewport/stage smoke legs are running or queued. Final CI and dev delivery receipts will be added before completion. Production is untouched.

## Pictures

[All rendered comparisons](rendered/) use the actual compressed web human assets, real population records, period dress/hair and production photo renderer. The page waits for its one sharp-detail page; `browser-checks.json` records the admitted page, calls, triangles, textures, identity and errors. All 27 fronts, six three-quarter views, both Stirling profiles and both phone views were checked (37 comparisons, zero page errors). Alice’s explicit reference spectacles also remain in the close Light model: 1,460 additional triangles and no texture, bounded by the existing 1,600-triangle spectacle contract.

- [Dorothy: reference, previous appearance and applied face](rendered/pa1904_stirling_william_r_c1900_dorothy_sterling-0-1400.png)
- [Alice May: reference, previous appearance and applied face](rendered/pa1904_stirling_william_r_c1900_alice_m_sterling-0-1400.png)
- [Alice’s Light phone view](rendered/pa1904_stirling_william_r_c1900_alice_m_sterling-0-390.png)
- [John J. Glessner](rendered/glessner_john_j-0-1400.png)
- [Frances Macbeth Glessner](rendered/glessner_frances_m-0-1400.png)
- [Marshall Field](rendered/pa1904_field_marshall-0-1400.png)
- [Harriet Sanger Pullman](rendered/pa1904_pullman_mrs_george_m-0-1400.png)

These are Chromium SwiftShader captures. The front-source fit and photographic texture do not establish hidden profile depth, exact colour from monochrome sources, hair shape or a perfect likeness. The Stirling images are explicitly edited reference models. Profiles and period styling remain reconstructed.

## Reproduction and budgets

`generic-and-child-writer-reproduction.json` retains the 349 final generic outputs and their frozen generator inputs from two actual writes. All 272 generic face/eye/head records and 345 raster/scalp files match the deployed forehead correction. The enclosing three-catalog writes took 205.27/192.63 seconds; per-catalog durations are not claimed. Historical processing-source records were subsequently consolidated; their final version is measured separately.

`person-photo-writer-reproduction.json` measures the final named writer twice (43.44/33.61 seconds), retaining all 43 output hashes: 42 payloads are actually rewritten and stable coverage.json is retained. A deliberately damaged second detail page is refused and restored byte-exact. Every input/source/fit/recipe hash remains unchanged. The importer needs no model or network for these pinned rebuilds.

Exact added face textures, including mipmaps: 12,873,272 bytes (12.28 MiB); conservative metadata also stays below 13 MiB. Three crowd sheets share one resident-or-loading nearby page. Body/cloth textures, existing Grey skins, geometry, image decode and driver overhead are outside this added bound. This is not a complete-town hardware FPS qualification.

The source index remains below its unchanged 328,000-byte capacity at 323,418 bytes. Compressed first-open index + Sources JS/CSS is 81,975 bytes, inside the unchanged 120,000-byte cap. One project-processing clearance record replaces duplicated derivative citations; every original archive citation, link, rights statement, person/source/crop identity and hash remains intact.

Published local verification checks the served modules, all three default catalogs, all 19 detail pages, both period card portraits and all 7,610 actual body assignments across four years. Exact-ID, scene, sex, own-skin and visitor-choice guards, unchanged existing heads, age/height and child proportions are also checked.

Evidence is stored here under the owner’s instruction in chicago/4d/AGENTS.md lines 417–423: “Bulky evidence goes to kevinrhaas/chicago-evidence, never to the tickets repo.”

## Stored portrait cards

Both daughters’ actual People cards deliver their 480×640 period portraits at 390px and 1280px widths, with zero page errors (`card-checks.json`). The four `rendered/card-*` captures show the edited period clothing and backgrounds. Desktop captures await decoded pixels before photographing. This checks UI delivery, not hardware frame rate.

## Broader portrait-archive audit

`historical-portrait-archive-audit.json` accounts for all 63 JPEGs in the committed human portrait directory: 27 registered source portraits, their 27 generated model previews, seven painted Met stand-ins for the 1812 garrison, and two Kirkland line engravings. The two new Stirling period references are accounted for separately. The paintings retain their stand-in labels; the engravings need a separate age-aware reconstruction before photographic texture use. The unverified/uncleared Ira Couch candidate is excluded. This distinguishes stored reference artwork from usable identified photographs and introduces no extra actor.

## Release-note smoke readiness

The initial c9b desktop stage 13 reported 155 passed, three failed, zero page errors: the first release-note read saw no entries while the later returning-visitor reload rendered the feed. `release-note-smoke-repair/` contains that transcript and the correction: the existing draw-hold helper covers only the DOM/storage feed checks, is reacquired after reload, and restores rendering in `finally`. Every assertion, readiness timeout and hit test is retained. The 15-part map and 35 smoke-input partition self-tests pass. Client renderer/data/assets tree hashes are identical before/after; only the test harness changes. The corrected local desktop stage 13 passes all 158 assertions with zero page errors (48m28s under SwiftShader). Hosted desktop and mobile stage 13 also each pass 158 assertions with zero page errors, on c728. Their decoded transcripts are in `hosted-current/`.

Qualification snapshot, 2026-11-27 00:55 UTC: six of eight hosted gate parts pass, as do portable humans and the 32-check phone upload-release guard. The remaining gate parts and 28 published viewport/stage legs are queued or running. The first moving-frame attempt reached Full and Balanced measurements without an assertion failure but hit the job's 40-minute limit; its transcript is retained and that job alone is being retried. Final CI and dev-delivery receipts remain pending.
