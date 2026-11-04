---
id: T-2388
title: Match the second Fort Dearborn (1835) to its pictures, every building in it
state: open
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: null
decision: null
decision_answer: null
---

Match the second Fort Dearborn (1835) to its pictures, every building in it.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

The fort was built without being checked against its pictures as a whole (inventory of 2026-10-11, T-2368). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

A picture of the fort shows many records at once, so `tools/photo_match.mjs` first learns to render a group: the camera names `also_render` (the other structure ids), each placed by its scene position. Every record of the fort is matched through those views, and the gate is carried by the blockhouse's.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Records: `fort_dearborn_artillery_house`, `fort_dearborn_barracks`, `fort_dearborn_big_barn`, `fort_dearborn_blockhouse`, `fort_dearborn_commandants_quarters`, `fort_dearborn_flagstaff`, `fort_dearborn_garrison_garden`, `fort_dearborn_guard_house`, `fort_dearborn_magazine`, `fort_dearborn_officers_quarters`, `fort_dearborn_out_building_a`, `fort_dearborn_out_building_b`, `fort_dearborn_palisade`, `fort_dearborn_parade`, `fort_dearborn_root_house`, `fort_dearborn_root_house_b`, `fort_dearborn_shop`, `fort_dearborn_store_house`, `fort_dearborn_sutlers_store`, `fort_dearborn_us_factors_house`, `fort_dearborn_wash_house`.

Pictures:
  source: `data/sources/kurz_allison_1893.json`
  source: `data/sources/chicagology_prefire276.json`
  source: `data/sources/chicagology_prefire052.json`
  source: `data/sources/wentworth_1881_fort_dearborn.json`
  picture: `chicago/reference/images/chicago/chicago_settlement_1820_2.jpg`
  picture: `chicago/reference/images/chicago/chicago_from_lake_1818_1830_childs.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_2.jpg`
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_river_mouth_1830.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_second_fort_dearborn_1816_getty.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1830_alamy.jpg`
  picture: `chicago/reference/images/chicago/licensed_previews/chicago_fort_dearborn_1892_peck_hindman.jpg`
  picture: `chicago/reference/images/chicago/chicago_harbor_lighthouse_1838.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- fort_dearborn_blockhouse


## Picture-review checkpoint — 2026-10-22

The unique blockhouse at the right of panel 5 has an absent cupola. Add a consumed cupola option, grade occurrence inferred from this source and dimensions reconstructed, then bake. Do not guess which range carries the pictured gallery. Early 1820 views predate replacement barracks; 1838/1850s views cannot silently govern July 1835.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Unapplied next-change handoff — 2026-10-22

A proposed first refinement and its evidence/remaining validation are saved in [T-2388.patch and T-2388.md](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/t3040-compound-review-checkpoint/unapplied-next-parcels). `git apply --check` passed against code commit `d3685569c5284946ab400deb0d2ccd0aa17a06be`. This is not an applied change, bake, solved camera or completed match. Claim the ticket before implementation, inspect current source and the handoff, and retain its full image acceptance. Whole-compound review support is [code PR #1218](https://github.com/kevinrhaas/chicago/pull/1218), awaiting GitHub CI at this checkpoint.

**Released 2026-10-23** (claim of run 10/23/2026, 8:49:10 AM CT): Owner requested session wrap. Exact closed prototypes, actual renders and unapplied source patches are saved at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Delegated workers have stopped. Image matching remains unfinished; resume from the case handoff and preserve its evidence limits.


## Exact native-worker blockhouse cupola handoff — 2026-11-03

The bounded visible increment under existing T-2388 is ONLY the second fort blockhouse roof assembly: build its pictured little square cupola and replace the current invented separate centre stack that would intersect it. Full all-buildings/all-pictures matching remains unfinished. No new photo ticket, split, done--pr or forced completion is authorized for this partial work.

Read the [closed current-source and actual-picture implementation packet](https://github.com/kevinrhaas/chicago-evidence/blob/3c8069d96f65410adb186478ae435bf9691229da/evidence/second-fort-2026-11-03/native-blockhouse-cupola-readiness-current42b/RECOVERY.md), ROOT-REVIEW.md, AUDIT.json and actual public-domain Kurz & Allison panel5 before editing. Root directly reviewed the actual plate, existing source/record and producer. Fresh current-source/ownership readbacks are saved with this handoff; recheck actual current dev when the native worker starts.

Keep fort_dearborn_blockhouse a fort_structure(kind=blockhouse), log_1816 phase. Add an optional/default-off explicitly consumed blockhouse cupola control locally in fort_structure.py and fort_structure_params.py. Existing lantern only builds on _tower(): toggling it on this blockhouse adds nothing. Do not route this building through the lighthouse, change shared common geometry or turn on cupolas globally. Implement finite bounded parameters and supported combinations without weakening generic schemas/assertions.

Root qualified this intentional roof-assembly choice: replace the unsupported reconstructed centre chimney count with0 and build the pictured cupola at the centre. The old single chimney is placed exactly there. This limited depiction choice is NOT a claim of no heating, no flue, or no later secondary projection, and does not silently move a stack elsewhere. Cupola occurrence is inferred from identified pictures; exact dimensions, cap pitch, openings, joinery and materials are reconstructed and recorded as a liberty. Preserve the entire existing below-roof body, walls, doors, jetty0.45m, loopholes, surveyed seat/rotation8degrees, 14.52by9.80m inferred footprint with its existing ambiguity,5.2m reconstructed walls, two stories, main pyramid/pitch30degrees and existing palettes. The cupola must sit/overlap properly against all four sloping roof planes, without floating corners, sky gaps or a hidden stack.

The Kurz & Allison1893 sheet is a verified public-domain retrospective picture at tier5, not a coordinate, metric, paint or independent proof of every feature on1July1835. Existing Wau-Bun/1831 reproductions corroborate the cap. The filename chicago_fort_dearborn_river_mouth_1830.jpg is misleading: its verified1856Kellogg/Blanchard print depicts about1836–1849 and has a small ambiguous secondary projection beside a louvred cap. Keep that later detail unresolved; do not backdate its louvres/projection or completed Lake House. No asset may derive from held check_required sources.

Changing this producer reaches the current25fort_structure MASTERs plus any applicable variants found by the actual staleness owner, including the already accepted1832lighthouse. Before the FIRST geometry-source commit, genuinely generate/qualify every affected current MASTER on pinnedUbuntu26.04/SHA-verifiedBlender4.5.3 in bounded native batches, with actual complete normalized inputs and output hashes. Do not predict/stamp freshness, omit foreign family members, alter recipe schemes or accept old WEB derivatives by filename. Actually regenerated byte-identical MASTERs may retain genuinely bound existing WEB bytes; changed outputs require actual encoding.

The independent Jail run41734994705 targets T-2380/frame_dwelling271 and the first-fort NE roof run41739288717 targets T-3041/outbuilding243. Their producers are distinct. Leave their runs/topics/claims/source alone. Preserve every foreign registry row and new keeper/NE model, use native entry-wise registry integration, and genuinely rebake any true both-sides model conflict. Keep accepted Green Tree and lighthouse outputs intact.

Preserve the historical docs/RESEARCH/fort-reference-groups-T-3040/second-fort-panel-5.* bodies as historical diagnostics. Capture ACTUAL same-camera before/after current21member compound comparisons through photo_match.mjs, with actual model hashes/placements and fresh group binding. Do not turn the old100m-eye/undersized compound into a claimed historical or metric fit, move surveyed geometry to match it or relabel old renders as new. A separate local blockhouse camera refinement may state actual controls/uncertainty; camera uncertainty alone adds no extra stop beyond T3153. Re-render every actual canonical group whose member bytes change. Mark only this pictured roof-assembly change fixed after actual visual confirmation; every other real compound/date gap remainsOPEN/DIFFERS.

Make the picture reachable with credit on the actual blockhouse Images card through supported native source/camera compilation. Baseline Images0/gradeinferred; a reasonable whole picture shows this named building, so derive the attested grade with an explicit pictured-source reason. Do not type sidecar confidence, guess library_image/held/thumbnail flags or attest hidden context. If a fresh canonical comparison is enrolled, resolve the actual photo/hash correctly and keep diagnostic_only:true for poorly constrained framing, without a false from-this-spot invitation.

Root reviewed platform draftPR219 exact feature aa9d7d2322d3abbc78d72526146c018a241c643e on steward/chicago-native-exact-ticket-20261103; both sourceCI checks and official15case desktop/phone smoke passed. The dedicated exact native-authoring job is literalUbuntu26.04/150minutes with existing pinnedBlender cache. Platform main stays unchanged. Only one exact target_ticket=T-2388 dispatch, lane fort-cupola-native-20261103, appchicago/slice1/slices1/defaultmodel-effort is authorized after this handoff sync/release and fresh ownership recheck. No unrelated fallback or duplicate Jail/NE job. No dispatch is claimed by this metadata handoff.

After all genuine affected geometry, all four source-check parts must PASS BEFORE first source commit, every native foreground command bounded600seconds with truthful reaping/verdicts. Ask actual committed-head PR changelog and ID questions; push a native feature branch and draft dev PR promptly. Publish the exact committed head and verify the byte contract, then actual default1835 desktop1280x800 AND phone390x780 roof/body in Normal/ByGrade, Imagescredit/Record/date/reconstructed metrics, grounded native arrival/entry/roof joins and appropriate existing smoke with zero page/console/network/server errors. Price current light-tier headroom before the deal and retain its floor/assertions. Keep conservative smoke-budget request distinct from actual subset; do not claim unrun whole15. Root must inspect actual pixels before required hosted-green ordinary exact-head dev merge.

Append LIBERTIES/STATUS/ROADMAP without replacing concurrent suffixes; one small visitor-facing changelog entry. Checkpoint qualified geometry/source4/PR/merge/delivery in chicago-evidence. Ship a checked partial cupola increment and release T-2388 OPEN with the remaining discrepancy/recovery pointer. No direct dev/main push, admin/force merge, local-host Blender, fabricated source/license/metric, new photo followup or done--anyway.

**Released 2026-11-03** (claim of Codex second-fort cupola native handoff 2026-11-03 11/3/2026, 5:34:11 PM CT): Reviewed bounded pictured-cupola native handoff saved; OPEN for authorized exact T2388 worker. No geometry, worker dispatch or full-original completion claimed by metadata handoff.

**Released 2026-11-03** (claim of run 11/3/2026, 5:40:26 PM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/41740271907): Shipped the bounded pictured-cupola increment on PR #1687 (branch steward/t2388-blockhouse-cupola-native-20261103, commit cdac604e): the small square cupola panel 5 of kurz_allison_1893 draws at the centre of fort_dearborn_blockhouse's four-sided cap is built, seated into all four roof planes, and the invented unattested centre chimney that stood in its place is recorded at a count of 0 as an explicit depiction choice (not a claim of no heating, no flue or no later projection). Occurrence inferred; every dimension reconstructed and admitted in docs/LIBERTIES.md L-second-fort-blockhouse-cupola-2388. All 25 fort_structure MASTERs genuinely rebuilt on pinned Ubuntu 26.04 / Blender 4.5.3; one master's bytes moved. Picture enrolled on the card by an explicit pictured ruling, grade derives attested. check.sh parts 1-4 PASS; desktop 1280x800 and phone 390x780 smoke PASS with zero page errors. THE ORIGINAL ACCEPTANCE IS NOT MET AND THIS TICKET STAYS OPEN: the compound view's verdict is differs (docs/RESEARCH/second-fort-cupola-T-2388/second-fort-panel-5-compound.match.json), the camera is an unfitted 100 m diagnostic, and the galleried range's identity, the facade openings, the other roof forms and chimney counts, the compound's composition and every other dated picture listed here remain unread. Recovery: https://github.com/kevinrhaas/chicago-evidence/blob/fff86d87b8bb17be2b6aaf782fa0416b8d56d739/evidence/second-fort-2026-11-03/native-blockhouse-cupola-shipped-t2388/RECOVERY.md


## Exact existing-PR recovery — 2026-11-04 second-fort handoff

Resume existing **PR #1687**, branch `steward/t2388-blockhouse-cupola-native-20261103`, head `cdac604e34b1b3ba3ed981ebfcfd0d0efc1e8f2f`. Do not pick another unit, create a replacement PR, or redo the cupola from scratch. Old draft #1682 was closed and replaced by #1687 on the same branch; #1687 is the existing non-draft PR to finish. Native source run https://github.com/kevinrhaas/polecat-platform/actions/runs/41740271907 is completed SUCCESS, actual outcome RESUME after two 540-second pending-gate waits (189 turns, 109.7 minutes), not a max-turn failure. The native worker released this original OPEN; do not force any live owner. Take the normal PR lap after its current holder releases it.

The cupola and its explicit reconstructed dimensions, removal of the invented center stack as a depiction choice, picture grade ruling, and source limits are already authored and genuinely baked. All 25 fort_structure MASTERs were actually rebuilt on pinned Ubuntu26.04/Blender4.5.3 before the native source commit f447b68a1fbe332d1b5d4375d49ef021a81a53d0; only the blockhouse MASTER/WEB bytes moved. Reuse that real proof only while exact producer, parameters, full recipe/input document and output bindings still agree. No host Blender, invented input hash, or redundant whole-family rebake to restart the task. Actual native event ZIP artifact13287228564 is SHA256 c7b2b1a72a77949a7202198d18c5a880745d7b29159d310def6b6727642df369.

Current dev advanced through the occupied-transport PR1649 (9881d782 and later folds/followups), so cdac is now conflicted. Merge CURRENT dev normally into this same branch, preserving every foreign authored row and raw append-only doc prefix; regenerate derived products from the combined tree. The observed overlap was LIBERTIES/STATUS/ROADMAP plus derived liberties/source-use; no fort producer/common/input overlap was found in the 256-path transport merge. Verify the actual current tree rather than assuming it stayed there. Refuse any incompatible actual geometry/input change instead of stamping a predicted hash.

Independent cdac integration proof against its 96d0612d incoming parent found all25 own MASTER rows/1WEB and all87 incoming MASTER rows/3WEB preserved exactly. Own producer/params/record, compiled blockhouse sidecar, both source credits, grade rulings and actual MASTER/WEB were exact to f447. That renderer-tree proof ends at96d: subsequent current transport changes main/navigator/runtime. Qualify the CURRENT published app at desktop1280x800 and phone390x780, including useful cupola/body Normal and ByGrade plus reachable card picture/source credits and Record account as warranted by the actual change. Prior actual native official smoke passed desktop stage3 107/0 and mobile3-4 139/0; do not claim the full15-stage smoke ran. Root directly reviewed visible cupola/body at both viewports. Only two roof planes are visible in those screenshots; source/geometry join reasoning is separate from unseen pixels. The phone lower Images credits/Record paragraph were cropped, not demonstrated product failures. The custom screenshot script logged pending texture/transcoder requestfailed URLs after browser.close without errorText/timestamps, so cancellation cause remains unverified; do not claim blanket zero custom network errors from its zero exit.

Complete source checks1/4 through4/4 and PR preflight before any app-source commit. The current CI runs the full suite in eight parallel parts; the final actual named whole `gate` aggregator must be SUCCESS, with every native part successful. Report/warranted green alone is insufficient. Address bounded real reds within the same run, ordinary protected merge to dev only, then verify the actual public dev delivery. No admin merge, direct dev/main push, force Git push, assertion weakening, or production dispatch.

Publish **UNQUALIFIED working-source plus raw log/hash checkpoints** in chicago-evidence every15–20minutes BEFORE full gates, using ordinary fast-forward evidence commits, so private progress survives a stopped run. Unqualified checkpoints are evidence, not assertions that app commits passed. Reuse exact successful source/runtime proof where valid; do not rerun merely because a summary was lost.

This is a bounded partial increment: original T-2388 stays OPEN/PARTIAL, compound verdict DIFFERS, diagnostic_only camera still unfitted at100m, remaining ranges/galleries/openings/other roofs/chimneys/composition/dated pictures still open. Preserve the entire prior original body. No done--pr, split, new photo follow-up, or whole-picture match claim. Release the original/your lap normally after merging or handing on.

Durable raw native and current conflict pickup: https://github.com/kevinrhaas/chicago-evidence/blob/edf16c06dfad3b6fff5bb271753765a3dc7975fc/evidence/second-fort-2026-11-04/native41740271907-completed-current9881-handoff/RECOVERY.md
Independent registry/runtime/doc bindings: https://github.com/kevinrhaas/chicago-evidence/blob/62033921402ac27ee5cc98b7105be4f670a78b51/evidence/original-picture-tickets-2026-11-04/integrated1687-1684-independent-audits-0123/RECOVERY.md
