# Next finite first-fort picture pass — external proposal

This packet prepares the missing **NW-anchored canonical picture coverage** for existing T-3041 / original T-2387. It does not close either ticket, apply any source change, generate geometry, set a match verdict or alter any checkout. The current west-wicket PR is independent and must not wait for this packet.

The patch `UNAPPLIED-NW-CAMERAS.patch` adds exactly two camera JSON files. It changes no existing camera, source record, structure, surveyed position, match record, ticket gate or source-rights finding:

- `data/reference_views/first_fort_dearborn_blockhouse_nw/currey_1912_birdseye.json`: the same fourteen-member Currey compound, moved mathematically from the outer-picket anchor to the NW blockhouse anchor. World eye and all world mesh transforms are preserved. Old eye `(65.92,56.20,49.69)` becomes `(66.87,27.00,49.69)` because the two origins differ by `(-0.95,+29.20)` m. Basis, focal length, principal point and pixels remain unchanged. The original outer-picket camera and current west-wicket review stay in place. The set of credited image members also remains identical; context membership does not create new attestation.
- `data/reference_views/first_fort_dearborn_blockhouse_nw/kurz_allison_1893_panel1.json`: the exact existing T-3040 thirty-member world camera, already anchored on NW, enrolled as explicitly diagnostic. Its known staff/plan disagreement is preserved. No extra `card_members` are invented for the thirty context meshes.

Both use existing verified public-domain picture source IDs. No new source-record enrollment is necessary: NW already cites Currey and Kurz & Allison. The camera's `source_id` provides the explicit view connection. There are deliberately **no proposed match files**. Real `photo_match.mjs` executions must create fresh, unreviewed bindings and actual comparisons before a human adjudicates them.

## What was actually checked

`RIGID-TRANSFER-PROOF.json` proves camera projection invariance for six affine/frame samples on each of the fourteen actual scene-member transforms, including the 22.86 m staff-height sample. Maximum numeric pixel/depth difference is about `7.4e-13`. The same fourteen world members and same image-credit membership are preserved. This is pure mathematical verification, not a browser render.

`PROPOSED-CURRENT-GROUP-IDENTITIES.json` resolves both candidates through the real `renderGroup` / `groupReview` functions against native checkout `86e8653c8fd70bfc7ea4a6da7ee65ee63ce5185c`, records every actual mesh SHA and current scene placement, and verifies both enrolled sources are marked verified/public_domain. `git apply --check` passed against that tree. Re-check on the eventual current dev after the west increment lands; this does not authorize overwriting later work.

`SOURCE-RIGHTS-AND-DATE-INVENTORY.json` preserves six relevant existing source records: Currey, Kurz & Allison, Lossing, Whistler, Chicagology274 and supporting Quaife text. The five-picture/map/container cue was not treated as a quota. These are **existing recorded rights findings**, not a new external provenance investigation. Currey/Kurz/Lossing are recorded public domain. Whistler is a public-domain contemporary map, not an image of all built elevations. Quaife is text-only here. Chicagology274 remains check_required and supplies no new derived picture asset in this proposal.

The four held Getty previews are accounted as one held preview group with no independence assumption, no new public-domain finding and no camera/geometry enrollment. A scene1803 catalogue label does not establish the underlying artwork's publication date. The packet does not silently turn the source-container or agency's captions into rights clearance.

## Thirty components, no sixteen new geometry tasks

`THIRTY-COMPONENT-DISPOSITIONS.json` has one explicit row for every original21 + context9 record, with separate Currey, Kurz-panel1, Lossing and Whistler readings. It distinguishes the fourteen Currey render members, seven other original outer records and all nine context members. A not-shown / not-individually-identifiable finding is an acceptance disposition, not a request to invent a hidden building.

Specific traps are recorded:

- Currey's dashed sally-port marks a route, not the detailed geometry of the four covered-way runs; those runs are not rendered by that view. Whistler's index expressly says the covered way was omitted from the draught.
- Whistler does contain a dotted wharf mark, but the current river seat and minimum deck dimensions remain reconstructed. Do not say that all nine context records are simply absent from every source.
- The record whose durable ID ends `stable_middle` is currently the **house in the factor's department** after the numeral23 re-reading. Preserve its actual current name and identity, rather than treating all three stable IDs as attested stables.
- The unlabelled galleried house outside Kurz's stockade cannot be assigned to an agent/factory/context record merely because that record was rendered nearby. Hidden range faces and the inner picket row are not independently resolved by that panel.
- Keep the source dates separate: first fort1803–1812 / Whistler1808 / Currey1912 retrospective; Kurz panel1 first fort, panel5 rebuilt1835 and panel8 town1830 are not interchangeable. Lossing's retrospective1804–1812 scene does not prove a precise1804 alteration or a contemporary viewpoint.
- T-3335 keeps Whistler's measured plan, range identities and lengths, the main-gate gap and current stacks. The later owner-adopted cupolas, magazine roof, NE pyramid and west-wicket occurrence must not be reopened from stale generic baseline prose. Apply T-3153 to a named visitor-visible discrepancy, not an old unbounded “not matched” placeholder.

## A useful limit from the existing Lossing camera

Lossing has an existing camera solved for the **Kinzie house**. Its exact same-world transfer to NW is retained under `diagnostic-only-not-in-patch/`, deliberately excluded from canonical additions. The CPU projection in `LOSSING-WORLD-CAMERA-LIMIT.json` puts all28 sampled current fort points outside the960px image, at x about2038–4244. The house-fit world camera therefore cannot also be called an accepted fort fit. This is not solved by moving the survey or calling a refit an anchor transfer. A genuine subsequent composite render can document the source/plan conflict and support a bounded owner-plan / tolerance disposition. No new geometry task follows automatically.

## Concrete next-PR sequence

Use this as prepared material for the existing finite sign-off; do not open another empty tooling/checkpoint PR or another photo ticket.

1. After the west increment's normal dev merge, re-read current T-3041 ownership, source/camera/placement guards and current assets. Review and apply only the two absent camera additions if still appropriate. Preserve existing reviewed Currey rows and surveyed geometry.
2. Run the two ordinary `photo_match.mjs` comparisons from current native assets. The patch does not inherit old group hashes or old `matches` flags. Read the source and actual new comparisons, then adjudicate only named remaining visitor-visible differences under T-3153 and T-3335. Existing staff/plan residuals do not authorize metric changes.
3. Make the thirty-component disposition matrix and all parent-listed pictures explicit in the same sign-off. The held Chicagology/Getty group needs an honest source/use disposition; this packet is not a rights waiver. The Lossing limit is a concrete existing-picture finding, not false accepted coverage.
4. Only when canonical NW views have current bindings and legitimately resolved differences should `node tools/image_gate.mjs --structure first_fort_dearborn_blockhouse_nw` and the actual existing ticket gate pass. A passing parser from one token camera must not substitute for the parent's all-pictures acceptance.
5. Combine with the existing/current runtime evidence at desktop and phone, source gates and ordinary protected dev merge. If a bounded unresolved source or pictured feature remains, leave the same original partial with its exact finite remainder; do not split or create follow-ups.

No checkout was edited by this preparation. The candidate cameras are unapplied and unrendered; no historical metric, new license, source attestation, completed match or ticket completion is claimed.
