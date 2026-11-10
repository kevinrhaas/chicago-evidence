---
id: T-2378
title: Match J. B. Beaubien's homestead to its pictures
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

Match J. B. Beaubien's homestead to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- jb_beaubien_homestead


## Picture-review checkpoint — 2026-10-22

Isolate the keyed Beaubien building from the separate Dean house in the panorama. T-0894 withdrew identity with the U.S. Factor's House; do not borrow that house's two-storey description.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of beaubien-lakehouse-agent 10/23/2026, 9:10:20 AM CT): Owner requested session wrap. Exact closed prototypes, actual renders and unapplied source patches are saved at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Delegated workers have stopped. Image matching remains unfinished; resume from the case handoff and preserve its evidence limits.

## Post-PR1456 remaining work estimate — 2026-10-30

The original M estimate included source and identity review, camera comparison and visible model refinement. Those are completed in the checkpoint737 native packet: MASTER 222fce, WEB 64fb, camera 6a44 and source-scoped reviewed matches e032. PR1456 has landed both required producers, and current native recomputation still gives the accepted fdac754a recipe. Remaining work is one bounded fourteen-path entrywise adoption, generated owners and shared current app/source/PR qualification; sized S for this remaining unit. The original image gate, source/date/rights qualifications and done-on-merge acceptance remain unchanged. This is the remaining effort estimate, not a completion claim.
