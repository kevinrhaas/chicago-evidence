---
id: T-2385
title: Match the first Tremont House to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-10-29
pr: 1448
claimed_by: Codex Tremont pictured-form and Green Tree continuation 2026-10-29 10/29/2026, 9:35:31 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-29T17:02:09Z
claimed_run: null
claimed_at: 2026-10-29T14:35:32.265Z
decision: null
decision_answer: null
---

Match the first Tremont House to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  source: `data/sources/gifford_tremont_house_no_1.json`
  picture: `chicago/reference/images/chicago/chicago_first_tremont_house_1833.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- tremont_house_1


## Picture-review checkpoint — 2026-10-22

Gifford shows three storeys, a shuttered three-bay gable and five-bay side, raised entrances and flagstaff; model is two storeys. Source remains `check_required` after Chicagology/CARLI/CHM/Internet Archive investigation. A generic pre-1930 assertion does not settle the original sheet's provenance. Simply rotating the existing 50×30 ft rectangle would also make the wrong broad gable.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

## Owner-confirmed reproduction source — 2026-10-22

The owner supplied [https://chicagology.com/prefire/prefire021/](https://chicagology.com/prefire/prefire021/) in reply to the source-credit question.

The live page returned HTTP 200 and reproduces `firsttremont.jpg` with the caption Tremont House No. 1, matching `gifford_tremont_house_no_1`. No original publication date, holding institution or image-use terms are supplied with this drawing. The following Chicago Tribune item dated December 28, 1850 describes the later five-and-a-half-storey hotel; its date does not establish publication of the first-hotel drawing.

The existing source record remains `check_required`; no new rights ruling, derived geometry, camera solution or image-match completion follows from this confirmation. Retain the full ticket acceptance.

## Owner-approved project reference use — 2026-10-22

The owner approved the linked image for project use with source attribution:

> ok i think those images are ok to use as public resources and just make sure you include things like that in sources

T-3053 records the approval in the source catalogue, retaining the hosting credit and original-provenance uncertainty. This supersedes the earlier project-use hold for the approved reference/comparison/source-display scope; it is not a verified public-domain or copyright-holder permission finding. Existing subject/date/measurement limits and this ticket's full image acceptance remain.

## Post-approval rendered baseline — 2026-10-22

The first Tremont committed-mesh comparison rendered successfully and was visually reviewed as `differs`. It shows the two-versus-three-storey mismatch, blank gable, missing shuttered bays, raised entrances and roof details. The provisional six-point fit has 17.23 px point RMS, not a solved historical camera. The current elevation scheme cannot simply be rotated to match the short/long facades; the handoff identifies the required model path.

Attributed source-use update: [PR #1224](https://github.com/kevinrhaas/chicago/pull/1224). Complete camera/render/handoff recovery checkpoint: [post-approval baselines](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/post-approval-school-tremont-baselines). The original image-match acceptance remains open; no geometry or accepted-camera change was made.

**Released 2026-10-23** (claim of Codex frame picture-match integration 10/23/2026, 12:28:11 AM CT): First picture-led frame refinements and source corrections are saved in the GitHub recovery checkpoint aaeac5b0. Full image matches remain open. Shared generator and source prerequisites will be tracked separately; continue the original cases from the recorded previews.
