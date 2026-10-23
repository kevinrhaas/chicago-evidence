---
id: T-2979
title: Park refined wagons and a period carriage in the walking scenes
state: done
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2791
opened: 2026-10-21
closed: 2026-10-21
pr: 1174
claimed_by: run 10/21/2026, 2:35:03 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-22T04:16:26Z
claimed_run: null
claimed_at: 2026-10-21T19:35:04.161Z
decision: null
decision_answer: null
---

Park refined wagons and a period carriage in the walking scenes.

**Acceptance:** Install reproducible original W01/C02 finish variants and render a bounded set of parked examples in the real1835/1904 walking scenes. Replace selected existing1835 farm-box stands at their current coordinates; preserve carts/covered wagons and a Light/far/load-failure fallback. Empty1904 carriage is clear of the sidewalk/crossing, without asserted maker or ownership. Grounding, inspection card/grade, detail transitions, actual desktop/mobile source+published images, console and existing budgets pass. Full preflight passes; commit/push and ordinary greenDEV merge. This ticket is the visible placement increment, not closure of photographic model quality, people/horses, driving or boarding.

Owner steering2026-10-21: prioritize attractive parked vehicles first, then ready static people/horses, and use researched era manufacturers/models where the evidence establishes them. Parent model acceptance T-2793/T-2794 remains open.

**Progress2026-10-21:** Final actual wheel-vs-rendered-road check passed (maximum0.690mm difference; all carriage wheels on the rendered asphalt). Final full preflight is running; no application PASS, commit, PR or merge claimed yet. Current staged source, source-reviewed human repair and named Studebaker WIP are preserved in `evidence/parked-vehicles-2026-10-21/checkpoint-2017/`; the new named model remains unrendered/unaccepted.

**Validation update2026-10-21:** Full1038-step run terminated with one failed step: the dataset validator rejected the unregistered new scene layer (two scene errors). The scene schema now registers `parked_transport`; targeted full dataset validation passes0errors. Independent publication review found and fixed the missing parked placement-data copy, with a matching byte-copy contract row. Final published runtime and first actual street images are next; a fresh full gate is still required before commit.

**Actual street inspection2026-10-21:** All four first-phase PNGs are saved and root-inspected: published1835desktop Western Hotel/Wolf Point, and1904mobile Balanced wide/curbside carriage. Placements and grounding are acceptable as a bounded prototype increment. Western scene2449driver draws/1,249,166tri; mobile carriage close3975/1,875,879, both within unchanged budgets. GL/page/console errors0. The overall helper receipt remains FAIL because an existing people.json request failure omitted its error reason; preserve that unresolved event, not a retroactive PASS. Phase2 adds one justified reason-preserving publishedmobile recheck to the four remaining planned boots, plus real vehicle popup DOM checks. Final corrected full preflight is now running (session34702); no application commit/PR/merge yet. Actual images, failed receipts and the prepared successor caller are backed up as capsule3e456644 in checkpoint-2017.

**Committed/pushed2026-10-21:** `2aebef95f6a5b6fa1bd8353db936c7674a73c32f` on `steward/parked-period-vehicles-20261021`. Corrected full preflight PASS1038steps/380deliberate refusal self-tests; exact-commit changelog/ID checks PASS. Final commit-stamped publication and remaining world/request/card checks are delegated to env_validation; CI qualifier wagon_visual will dispatch the18-cell grid once root supplies the draftPR. No DEV merge yet.

**DEV review opened:** Draft https://github.com/kevinrhaas/chicago/pull/1174 at exact pushed2aebef95. Local acceptance recheck and18selected CI smoke cells are running in parallel. Ticket remains claimed pending that review work; no merge/done claim.

**Final local acceptance, 2026-10-21 21:18 UTC:** Corrected full preflight PASS1038/380 self-tests; exact-commit checks PASS. Final source/published runtime PASS168 assertions and actual card/ground/budget checks pass. Main-scene packet has11 normal browser images plus2 explicitly canvas-only1904 desktop images; source Wolf Point image was interrupted and is not claimed. Original failures retained. checkpoint-2118 preserves final packet5662755c. DraftPR1174 exact2aebef95 has14/18 selected smoke cells and all3 normal workflows green,4 still running. No merge claimed; no duplicate dispatch.

**Terminal CI — 2026-10-21 23:02 UTC:** PR1174 exact2aeb has17/18 selected smoke cells and all3 normal workflowsPASS. Desktop13 actually completed151PASS/2FAIL/0pageerrors: Xray8223 and Ghost40%8469 exceed unchanged7800. Merge stopped; no rerun or weakened budget. Cause open; exact-parent/new finite diagnostic caller being prepared outsideapp, held until covered browser closes. Full failed log/receipt/diagnosis archived in checkpoint-ci-failure-and-v5-held (405a5613). Ticket remainsreview, notdone.

**Counter diagnosis finding — 2026-10-21 23:31 UTC:** Focused actual gpuPick/Three with deterministicGL-boundary confirms private picks restore renderer.info.render but leak separate multiDrawExtra (5-entrypick adds4, repeat/nested accumulate). Minimal source461687ff +12-check portable regression10dd6159 pass outsideapp; original modules fail same regression on actual leakedvalue. This is not yet mainGPU/CIcausality proof. Exactparent/new passivecaller manifest101edd3b/support23e07ca8 is HELD until coveredmainCLOSED. No sourceapplied/rerun/merge/budgetchange. Evidence in checkpoint-counter-regression-and-held-diagnosis.

**Actual performance attribution — 2026-10-22 00:36 UTC:** V4b stopped honestly at its600s bound; candidate NORMAL3695/Xray8223/Ghost408466, parent NORMAL3694 only. Xray matches CI exactly, Ghost differs−3; historic camera/detail unlogged. Actual GL primary equals shipped counter in every sample, private picks0; confirmed private-pick contract bug does not explain these frames. Xrayterrain3908draws, base3652transparent vs96opaque entries. ExactsourceFrontSide already; no safeblindforceSinglePass/transparentreorder. Rawcapsule2c3e09d2 andfinite review83612033 in checkpoint-terrain-attribution-and-shoe-correction. BothliveguardsPASS/CLOSED/ownerdeparted; parent-only continuation preparation remainsheld. No budget/source/assertion change or DEVmerge.
