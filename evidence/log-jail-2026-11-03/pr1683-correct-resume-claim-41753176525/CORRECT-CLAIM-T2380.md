---
id: T-2380
title: Match the log jail to its pictures
state: claimed
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: null
pr: null
claimed_by: run 11/3/2026, 7:24:15 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41753176525
claimed_at: 2026-11-04T01:24:15.585Z
decision: null
decision_answer: null
---

Match the log jail to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_cook_county_jail_1836.jpg`
  picture: `chicago/reference/images/chicago/chicago_first_courthouse_1835.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- log_jail


## Picture-review checkpoint — 2026-10-22

Pictures show a tall jail behind a palisade plus a low keeper's house; model is a low 6.096×4.572 m outbuilding. Catalogue dates the jail compound to 1836, so resolve identity/date before replacing July 1835 geometry.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of jail-picture-match-agent 10/23/2026, 7:24:30 AM CT): Owner-requested session-wrap handoff; original two-picture scope remains open and DIFFERS. Prior actual compound and corrected UNSELECTED/UNRUN pilot archived at https://github.com/kevinrhaas/chicago-evidence/blob/64fd5de/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . No canonical jail geometry adopted. Camera, chronology, missing details and closed-gate collision limits remain documented; continue original image gate with real rendered comparisons.

## Native-worker recovery handoff — 2026-11-03

This original ticket remains unfinished. Its two canonical comparisons remain `differs`; no full match, new sign-off ticket or completion is claimed. Preserve the chronology/identity limits above: a later catalogue date is not automatically evidence of the exact July1835 condition.

The coherent **prepared, unapplied 16-path keeper/compound increment** and genuine native evidence are saved in [the closed source packet](https://github.com/kevinrhaas/chicago-evidence/blob/d73cd2f3d8f7b207069ac479846a21ddc4d24f3d/evidence/log-jail-2026-11-03/prepared-keeper-compound-485c/RECOVERY.md). It adds the keeper, reconstructed1.30m core setback, continuous palisade and low house-side gate as one partial improvement. Re-read its actual images and discrepancies before adoption; its keeper-only cut would leave the proposed compound incomplete.

[Current-preimage and native-budget assessment](https://github.com/kevinrhaas/chicago-evidence/blob/fa5f251e140e005efe2386e00ec3619b0ce394f8/evidence/log-jail-2026-11-03/prepared-keeper-compound-485c/EXECUTION-BUDGET-2037.md) assessed dev92bee: eleven preimages exact, four new files absent, and one LIBERTIES mismatch. **Recheck all16 against actual current dev.** Preserve the entire latest LIBERTIES body (including T3356 and subsequent Green Tree additions) and port only the owned2,511-byte jail append. Never overwrite it with the older whole file or bypass a failed preimage guard.

The retained keeper's full normalized native input is `cbc1246652fa64234391b08cde5701e910d545540112a22962bbf2c2da6067ea`. Its genuine MASTER is72,588bytes/SHA256`03aafaa4ae61edc263dbdff7f8d82d63f0fd284d084d03260f65ebe7922e34d0`; WEB is20,896bytes/SHA256`b1997083a1fc4fe75bf0150daacd36a6097e9326ec697de2acb85add6eecc620`. Reuse requires complete current input-document equality, not an assumed hash. The optional frame-producer change also reaches **271 existing default frame assets**: qualify them by actual pinned native MASTER generation; preserve byte-identical genuinely bound WEBs or encode real changed outputs. Do not predict or manually stamp recipe freshness. Preserve every foreign registry row and later merged work.

[Draft platformPR219](https://github.com/kevinrhaas/polecat-platform/pull/219), reviewed feature commit `aa9d7d2322d3abbc78d72526146c018a241c643e` on `steward/chicago-native-exact-ticket-20261103`, prepares an exact-ticket **Ubuntu26.04 / pinned SHA-verified Blender4.5.3** native-authoring worker with150minutes. Its [checked source/smoke recovery](https://github.com/kevinrhaas/chicago-evidence/blob/e6881845a18edfcb7805a781a99d658104b74139/evidence/native-geometry-worker-2026-11-03/draft-pr219-checked-aa9/RECOVERY.md) records validation. No worker has been dispatched by this handoff, and no platform-main merge or local-host Blender execution is authorized here. The coordinator must use the reviewed feature definition only after its own review; the worker claims this exact ticket normally and stops for another live owner/PR, with no unrelated queue fallback.

Use bounded native producer/derivative batches under600seconds, then all four source-gate parts **before the first source commit**. The stock selected272-id content bake is not a safe50-minute assumption: actual checkout15m58 + successful whole gate21m21 + historical native-family estimate17minutes already totals54m19 before setup/publication/push (earlier gate29m05 makes62m03). `bake.sh` contains the whole embedded gate; a timeout is not a pass and it has no skip-check shortcut.

Ship only a checked, evidence-bounded partial PR into dev: actual current-model comparisons, published desktop and390x780 phone checks, appropriate native smoke, current hosted gate and an ordinary protected merge. Retain the T3153 stopping bar, explicit liberties and source/date/rights conflicts. Keep originalT2380 OPEN/released with remaining differences unless its complete image gate is genuinely met; no `done --anyway`, new photo follow-up or direct dev/main push.

**Released 2026-11-03** (claim of Codex original jail native-worker recovery handoff 2026-11-03 11/3/2026, 4:52:33 PM CT): Checked recovery links and native-family requirements published; released OPEN for reviewed exact-ticket native worker. No worker dispatched, geometry applied or full image match claimed.

## Exact existing-PR recovery — 2026-11-04

**Partial work is saved in existing [Chicago PR1683](https://github.com/kevinrhaas/chicago/pull/1683), head `bc0b8c56494c89e85cc4df745ef862fbb1577f50`, branch `steward/t2380-keeper-compound-native`. Resume that PR; do not create a competing PR or new image ticket.** The original two-picture image gate remains OPEN/DIFFERS. Keep every prior paragraph and the source/date/rights/identity limits above.

Native worker [41734994705](https://github.com/kevinrhaas/polecat-platform/actions/runs/41734994705), job126261776333, completed FAILURE at 2026-11-04T00:51:27Z: `error_max_turns`, 201 turns after114.6minutes against a200-turn limit. This was neither a native/setup failure nor a150minute timeout. There is **no salvage ref**: the existing PR commits are the saved source work. The authenticated [raw-run recovery](https://github.com/kevinrhaas/chicago-evidence/blob/10583a4d9a5198d1213048d4536df3239eb3872d/evidence/log-jail-2026-11-03/pr1683-native-run-max-turns-pickup/RECOVERY.md) preserves artifact13285207925, ZIP SHA256 `8898d89654ba8ef1c73e687ce4b35ba42be9b58bc808f41852b5f3f98db82b3d`.

Actual native proof: event368 derives the272-frame roster from the manifest; event374 runs pinned Blender4.5.3/build67807e1800cc `build.py` for all272 (exit0,21.475seconds); event396 verifies271 existing GLBs byte-identical with only their manifest input SHA updated, relative to the worker's OLD parent38119e64. Event1030 actually builds and encodes the final keeper: MASTER70,712bytes/SHA256 `431dc44f37bdcb2c7f705a5b17b65fe6a1cf748d077c337b699094c9b41752a8`; WEB20,632bytes/SHA256 `15eb2fbad5e1b8f464c30f7135297047896b4eff95f9168de6084e75e86f710e`. Event1034 refreshes both comparisons as DIFFERS. Reuse any output only after exact current code/input/byte binding; these old-parent facts do not prove current dev.

**Work still owed before a qualified source commit/merge:** integrate actual latest dev (observed `96d0612d940e3652af24875674a2e17feeb38184` at01:08UTC; re-read before use), preserving all Bridge/GreenTree/Sauganash and other foreign rows. PeerPR1679 changed `pruyne_kimball_drugstore__frame_1830s.glb`: the changed frame producer needs an actual genuine current-Pruyne rebake on the combined state, never a freshness-only stamp. Retain the entire current LIBERTIES body and all unrelated changes. The saved native stream has intermediate/focused source checks and repairs but **no all-four foreground source-gate PASS on finalbc0**. Its part1 PASS522.749seconds came after publishing/checking moved into background; part3 backlinks were repaired atbc0 and part4 held-head count at93d, without a final all-four clean recheck. Run all four under proper foreground600second bounds/reaping. There is **no smoke_renderer, Playwright or app screenshot call** in the200-tool stream: actual desktop and390x780 UI/no-page-error checks, appropriate native smoke and named full gate on the exact final head remain owed. A report/warranted result alone is not that named gate.

Root directly inspected the actual saved canonical JPEGs: Gale is sideways90degrees with diagnostic framing; Andreas is a broad courthouse view with the jail small at right. Keeper, continuous palisade and low house-side gate are visible; the core remains hidden and roof/proportion differences remain OPEN. Do not claim a full match or that physical app QA occurred.

Fresh ownership audit at01:08UTC: old worker completed failure, PR1683 head unchanged, `lap/pr-1683` free, and originalT2380 still owned only by that old failed run. Release that dead claim natively; originalT2380 stays OPEN/PARTIAL until its complete gate is genuinely met. Use the documented PR `resume:` comment/label, with a reason, preserving existing history.

**Dispatch remains gated on root review of the optional existing-PR resume feature.** Reviewed old platform commit `aa9d7d2322d3abbc78d72526146c018a241c643e` refuses any open PR owning the target and is NOT a working resume path. The new optional `resume_pr` feature requires all11 platform CI checks, official15 Chromium smoke cases/both viewports, hosted checks and root code review before use. Only after the root explicitly authorizes its exact feature SHA, target `app=chicago`, `target_ticket=T-2380`, `resume_pr=1683`, `slice=1`, `slices=1`, ORIGINAL `lane=jail-native-20261103`, existing `max_turns=400`; leave model/effort defaults and150minute native budget. Stop for any other live ticket claim/PR lap; no force, extra ticket/PR, local-host Blender, direct dev/main push or administrative merge.

During resume, publish **UNQUALIFIED working-source plus raw log/hash checkpoints to chicago-evidence every15–20minutes**, using ordinary fast-forward evidence updates before full gates; do not make an unqualified app source commit. Preserve SDK first-history truth, original WIP commits, actual build ledger/source-four/UI logs for direct review. Finish with an evidence-bounded partial PR, ordinary protected green dev merge, and original-ticket OPEN/release unless every image gate is actually met.

**Released 2026-11-03** (claim of run 11/3/2026, 5:06:32 PM CT, by https://github.com/kevinrhaas/polecat-platform/actions/runs/41734994705): Native run41734994705 completed FAILURE/error_max_turns; preserve existing PR1683 headbc0b8c5 and exact dated recovery. Original image gate remains OPEN/DIFFERS; root-reviewed existing-PR native resume, combined current-Pruyne bake, final source-four/UI/full gate and protected merge remain owed.
