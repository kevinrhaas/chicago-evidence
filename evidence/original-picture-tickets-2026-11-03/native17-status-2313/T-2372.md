---
id: T-2372
title: Match Eliza Chappel's infant school to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-10-31
pr: 1512
claimed_by: Codex continuing same four-picture batch; verified existing ownership 10/30/2026, 8:07:21 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-31T11:19:28Z
claimed_run: null
claimed_at: 2026-10-31T01:07:21.938Z
decision: null
decision_answer: null
group: T-2372,T-2375,T-2378,T-2382
---

Match Eliza Chappel's infant school to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/eliza_chappel_school_shore_view.json`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- chappel_infant_school


## Picture-review checkpoint — 2026-10-22

`eliza_chappel_school_shore_view` remains `check_required` and prohibits derived assets. The school/annex identity is unresolved and the composed drawing has inconsistent perspective. T-0909 already exhausted the uncredited blog/Young lead; do not rerun that search without a new lead.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Owner-confirmed reproduction source — 2026-10-22

The owner supplied [https://drloihjournal.blogspot.com/2018/01/eliza-chappell-the-first-chicago-teacher-paid-by-public-funds-in-1833.html](https://drloihjournal.blogspot.com/2018/01/eliza-chappell-the-first-chicago-teacher-paid-by-public-funds-in-1833.html) in reply to the source-credit question.

The live page returned HTTP 200 and its first school image uses `21617595_10203558686525015_5452300313452439832_n.jpg`, matching the recorded local illustration. Its caption places the school roughly at Lake and Clark. No artist, original publication date, collection credit or image-use terms are supplied with that illustration; the journal explicitly omits inline citations. This confirms the immediate reproduction source, already recorded in `eliza_chappel_school_shore_view`, without resolving the original provenance.

The existing source record remains `check_required`; no new rights ruling, derived geometry, camera solution or image-match completion follows from this confirmation. Retain the full ticket acceptance.

## Owner-approved project reference use — 2026-10-22

The owner approved the linked image for project use with source attribution:

> ok i think those images are ok to use as public resources and just make sure you include things like that in sources

T-3053 records the approval in the source catalogue, retaining the hosting credit and original-provenance uncertainty. This supersedes the earlier project-use hold for the approved reference/comparison/source-display scope; it is not a verified public-domain or copyright-holder permission finding. Existing subject/date/measurement limits and this ticket's full image acceptance remain.

## Post-approval rendered baseline — 2026-10-22

The school committed-mesh comparison rendered successfully and was visually reviewed as `differs`. Door/base framing is approximate; the model has an eave-front roof where the drawing shows a gable over the doorway, plus width, opening-height, door and roof-covering differences. The camera is research-only while pictured-building identity remains unresolved; no grade or acceptance change follows.

Attributed source-use update: [PR #1224](https://github.com/kevinrhaas/chicago/pull/1224). Complete camera/render/handoff recovery checkpoint: [post-approval baselines](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/post-approval-school-tremont-baselines). The original image-match acceptance remains open; no geometry or accepted-camera change was made.

**Released 2026-10-23** (claim of school_lighthouse_castle_bridge 10/23/2026, 8:40:22 AM CT): Run wrapped after verified frozen recovery at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . School recess is prepared UNRUN; Wolf Point latest actual door/log comparison differs. Original full picture-match acceptance remains unfinished and unchanged; no matches or completion claimed. Source-origin identity/date uncertainty and owner-approved attributed school use are preserved.

## Post-PR1456 remaining work estimate — 2026-10-30

The original M estimate included source and identity review, camera solving and visible geometry. Those are completed in the retained native packet: MASTER fb141fef, accepted recipe 2fe83632, camera ca092679 and root-reviewed comparison 905bfca7 with all seven dispositions closed. Both required log producers are now canonical through merged PR1456, and current native recomputation still reproduces that recipe. Remaining work is one bounded twelve-path entrywise adoption, generated owners including alley lanes, and shared current app/source/PR qualification; sized S for this remaining unit. The original image gate, source/date/rights qualifications and done-on-merge acceptance remain unchanged. This is the remaining effort estimate, not a completion claim.
