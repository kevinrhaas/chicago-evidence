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
claimed_by: run 11/3/2026, 5:06:32 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41734994705
claimed_at: 2026-11-03T23:06:32.392Z
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
