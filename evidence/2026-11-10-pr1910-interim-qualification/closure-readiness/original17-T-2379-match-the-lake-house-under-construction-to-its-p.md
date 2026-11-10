---
id: T-2379
title: Match the Lake House under construction to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-11-09
pr: 1907
claimed_by: Chicago five-building completion group 2026-11-10 11/9/2026, 8:03:15 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-11-10T04:16:22Z
claimed_run: null
claimed_at: 2026-11-10T02:03:16.731Z
decision: null
decision_answer: null
group: T-2374,T-2379,T-2380,T-2383
---

Match the Lake House under construction to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_river_mouth_1830.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- lake_house_construction


## Picture-review checkpoint — 2026-10-22

`chicago_fort_dearborn_river_mouth_1830.jpg` actually depicts ca. 1836–1849 per `IMAGE_SOURCES.md`. Its finished hotel cannot establish July 1835 construction progress. Preserve the unfinished phase while resolving this temporal mismatch.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of beaubien-lakehouse-agent 10/23/2026, 9:10:30 AM CT): Owner requested session wrap. Exact closed prototypes, actual renders and unapplied source patches are saved at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . Delegated workers have stopped. Image matching remains unfinished; resume from the case handoff and preserve its evidence limits.

**Released 2026-11-03** (claim of Codex Lake House later-state picture increment 11/3/2026, 1:46:31 PM CT): PR #1670 merged normally into dev at 2026-11-03 20:53:02 UTC as dacc6364b6e6dce484d197627abbea5244218a0c after exact-head full GitHub gate41711919386 passed. Partial progress only: the Lake House Images card gains one credited public-domain1856 Kellogg/Blanchard/NYPL print, explicitly depicting the later completed1836–1849 hotel rather than July1835 construction evidence. Grade remains inferred, shell_1835 and both model bytes unchanged. OriginalT2379 stays OPEN for construction-state picture matching; no matches verdict, full completion or follow-up ticket. Actual authored four-part gate, published desktop/phone and native107 each passed on qualified snapshots; final5603 relevant identity/current validate --all/publish contract passed. Durable final proof: https://github.com/kevinrhaas/chicago-evidence/blob/73579633060c2f49b49764515c2b6b5b82482a6a/evidence/lake-house-2026-11-03/final5603-currentdev-repair-integrated/RECOVERY.md . Public preview remains behind the merge because the existing main deploy failed checkout; delivery is not yet claimed.

## Primary-source research checkpoint — 2026-11-04 (bounded, no new geometry)

Searched 28 full, corpus-hash-verified primary transcriptions: 15 Chicago Democrat issues (20 May–26 August 1835) and 13 Chicago American issues (8 June–29 August 1835), 3,215,983 characters. The 12 broader house/building candidate contexts were manually distinguished from schools, a Rezigue dwelling, bank/warehouse notices and a New Orleans hotel collapse. Only the already-admitted 10 June p.2 col.5 Lake House notice was found under the named/OCR patterns; it supplies no July wall height, roof, floor reached, foundation depth or plan. These are transcription/OCR searches, not proof that no other notice existed; the original June 10 facsimile was not available/read.

A bounded archive check directly verified ONE later printed quote: Fergus, Directory of Chicago 1839 (published 1876), Hotels section, prints “Lake House, cor. Rush and North Water sts”. This verifies that line in the 1876 recollection, NOT a contemporary 1835 address or construction stage. Its North Water address conflicts with the current Andreas/Michigan-Hubbard reasoning and needs source/map/conveyance adjudication before any relocation. The held 1843-canvass/1896-edition entry about the west half of a block fronting Rush, Michigan and Kinzie remains a 2007-transcription-mediated later lead; no facsimile or metric measurement is claimed for it. Existing federal tract entries are not hotel-lot deeds.

No app/source/model/phase/grade changed; no new geometry job is recommended from this evidence. Preserve the July 1835 inferred/reconstructed shell, the credited 1856 print's later completed-state date limit, and the unresolved construction-stage picture acceptance. No backdated completed version, fabricated match, new photo ticket or done override. [Exact findings, complete coverage hashes, direct page image, failed access attempts and recovery](https://github.com/kevinrhaas/chicago-evidence/blob/7dc233d052373ee03feecd7bf8b01f11e1287408/evidence/lake-house-2026-11-04/primary-search28-issues-and-fergus-direct-line/RECOVERY.md).

**Released 2026-11-03** (claim of Codex Lake House bounded primary-source research 11/3/2026, 6:29:29 PM CT): PR #1694 merged the directly checked later Lake House address and credited source as a documentary increment. The July 1835 construction-state image match remains OPEN/PARTIAL: later hotel imagery and the 1839 listing recalled in 1876 do not establish that construction stage or position. Native both-viewport and exact source/merge evidence: https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/lake-house-2026-11-04/PR1694-native-both-integrated73d4 . No completion or new follow-up ticket is claimed.

**Released 2026-11-04** (claim of Codex Lake House editorial proposal correction 11/4/2026, 3:21:43 AM CT): Merged notes-only partial PR1703 (790535c3314f631152604b904ac6b5daf7f5f3f0); actual current7fe eight-part gate41810382776 plus aggregate PASS. Record/c001 now distinguish editorial desired relative hotel size from measured scale, hotel ranking, July construction stage or vacant-site proof. Exact quotation/normalized/locator/reading, prior1694 Fergus address, geometry/recipes/native outputs preserved; no native or browser execution claimed. Source evidence checkpoint https://github.com/kevinrhaas/chicago-evidence/blob/998a2f995a49e0b1e014083509c296224754078c/evidence/lake-house-2026-11-04/pr1703-current-e897-sauganash-preserved/RECOVERY.md . Original image match remains OPEN/PARTIAL; later completed-hotel picture does not establish July1835 progress.

## Final qualified resolution and merged receipt — 2026-11-10

The original work is delivered by [PR #1907](https://github.com/kevinrhaas/chicago/pull/1907), ordinarily merged to dev at **2026-11-10T04:16:22Z** as `c6e4462975b953866bf5e75774cfbe55ae0a8a2e`, from exact qualified head `84628e5945100671ec899b351379d778d9f15ebe`. Earlier partial/open notes above describe preceding increments and are superseded by this final scoped resolution.

Qualification: pinned native run [42745792113](https://github.com/kevinrhaas/chicago/actions/runs/42745792113) genuinely exported375bindings from `64a752353bc66fa6bfa58c853b90c32625f7b739`; the217-file [native/control/picture checkpoint](https://github.com/kevinrhaas/chicago-evidence/tree/9807336dcbabe0b4feccfaf7c223bb1d990eea5e/evidence/2026-11-10-native-four-building-acceptance-and-final-three/) preserves exact outputs and unchanged-control audits. All eight source-gate parts plus required aggregate passed at846 in [run42751573783](https://github.com/kevinrhaas/chicago/actions/runs/42751573783),1293actual steps. The94-file [final public qualification](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/) retains all nine raw CI logs and terminal verification, actual published URL/model/date/phase/publisher bindings, preserved harness failures and corrections, and43directly reviewed actual or explicitly controlled screenshots across focused desktop1280×800 and phone390×780 flows, with zero page errors in final runs. UI ran at `c5551fdd66fc79d673155a20138f7d331df51b8b`; [unchanged-consumer proof](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/qualification/UNCHANGED-CONSUMER-PROOF.json) and the two-file patch establish that final846 changes only the measured storage allowance/documentation, with renderer, models, assets, data and sidecars exact. This is focused runtime plus full source qualification, not an assertion that the broader inherited smoke/performance suite passed or that production was promoted.

Green Tree **T-2376 remains OPEN/PARTIAL**: the categorical third upper-front window is still absent from the PR1907 model and open in its three comparison records. Its public release/handoff is preserved; it continues with the two forts in the next existing-ticket group. This resolution neither closes Green Tree nor creates a photo follow-up.

## T-2379 completion and dated image disposition — 2026-11-10

FINAL QUALIFIED LAKE RESOLUTION — actual native/published/visual review and
final source qualification are complete. Root retains sole ticket/PR authority;
no historical image match is asserted and no merge is claimed by this text.

The July 1835 Lake House is now built as a bounded reconstructed worksite rather
than a uniform magazine skin: thick stepped brick walls, seven open work bays,
three timber-supported bridged openings and two internal timber stages. The
existing 24×15m footprint, four-metre maximum and independently declared material
piles remain. The June 10, 1835 Chicago Democrat notice supports the active project;
its exact July lift, openings, thickness and stages remain reconstructed. No
completed-hotel roof, cupola, glazing, sign or accommodation is backdated.

The original picture has a finite wrong-date disposition. The1856
Kellogg/Blanchard Old Fort Dearborn lithograph, stored under a misleading 1830
filename, depicts the completed Lake House in ca. 1836–1849. Its planning copy is
byte-identical. All four Lake House illustrations on the known Chicagology
source page were also opened: the about 1860 photograph and 1869 map concern later
completed states; the 1857 ad and 1856 ad/1854 menu composite depict no architecture.
Milwaukee's Lake House image is a different hotel. None supplies a July 1835
construction view. The later west-of-Rush map conflict remains declared, with no
claim that it is a July survey. Source coverage and image hashes are in
`docs/RESEARCH/lake-house-completion-20261110/`.

This is the existing image-gate exception for a picture wrong for the target
state, consistent with the original ticket's own each-picture-at-its-date rule
and its 2026-10-22 checkpoint. It is not a geometric `matches` verdict and creates
no fictitious source camera or empty accepted comparison. The picture remains
credited later context. Missing exact July progress does not block the visible,
openly declared reconstruction under AGENTS.md's reconstruction rule.

Actual final receipts:

- Integrated source and native input pin: native source 64a752353bc66fa6bfa58c853b90c32625f7b739, run 42745792113; published build c5551fdd66; exact official publisher-transform receipt 9d385c84bd5a8310387fa6de2a468cc539e5956b3e268f0c6a7525fa712db128 at /tmp/nov10-completion-ui/LAKE-OFFICIAL-PUBLISHER-BINDING.json.
- Final master and published derivative SHA-256: master d89e437a37c91d3627c2deb867ef20eeeb0dceeb6506163a8ac6f17e7f641f2a; actual published 347864382d6b6fb257214bdeef7b718d587978d322185216b918f88a2701133c. Source-web b639cc368cca555c92ffa6afaee8f59adf1eede151867cc7be4698ed10483695 is separately bound through the official transformation and is not assumed byte-identical.
- Published page-loaded asset/date/phase/raw confidence, real opening/thickness/
  lift probes and old-magazine comparison: /tmp/nov10-lake-native-review/final-desktop/desktop.json and final-phone-repaired/phone.json: actual published byte hash, July phase/date, raw 1560vertices/all1.0, existing display 0.5, rendered 24×3.999145×14.998993m, wall 0.45997497m, seven open bays, three upper spans and no central cap. The old master blocks all seven aperture probe lines.
- Actual1280×800 and 390×780 screenshots inspected; grounding, open walls/stages
  and card liberties readable; zero page errors: /tmp/nov10-lake-native-review/FINAL-ACTUAL-VISUAL-REVIEW.json: all 13actual/controlled captures directly opened; actual application street, aerial, card and liberty views pass both viewport reviews. Rear actual phone aerial plus controlled comparison expose both internal stages. Zero page errors in both final runs. Controlled comparison is explicitly not a historical-image match.
- Exact integrated full gate and required release checks: GitHub source run 42751573783 at exact head 84628e5945100671ec899b351379d778d9f15ebe: all eight gate parts and required aggregate gate completed success; actual terminal CHECK PASS readings and all nine raw logs are preserved in source-ci/. The actual focused published desktop/phone qualification ran at c5551fdd66fc79d673155a20138f7d331df51b8b; UNCHANGED-CONSUMER-PROOF.json and c555-to-846-ONLY-TWO-FILES.patch prove that final846 changes only the measured storage allowance and documentation, with no app, geometry, data, sidecar, asset or publisher change. This is focused UI qualification plus full source gate, not a claim of full smoke, separate performance certification or production promotion..

After recording this ruling in the ticket body, root may use the existing
`done T-2379 --pr N --anyway --why` lifecycle with this narrow period-scope reason.
In repo mode the ticket becomes review, and settle marks it done only on merge.
No follow-up ticket or speculative July image is required.


Public durable counterparts for the local paths in that pre-merge qualified ruling: [complete Lake visual review](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/lake-review/FINAL-ACTUAL-VISUAL-REVIEW.json), [publisher byte transform](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/five-building-ui/LAKE-OFFICIAL-PUBLISHER-BINDING.json), [dated exception reason](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/lake-review/WHY.txt), and [full qualified resolution](https://github.com/kevinrhaas/chicago-evidence/tree/00dbfbc77e10f857f19a42a1e38b95a83a329c77/evidence/2026-11-10-pr1907-final-qualification/qualification/T2379-FINAL-QUALIFIED-RESOLUTION.md). PR1907 has now actually merged as recorded above. The existing wrong-state exception is used only for Lake; no July geometric image match, empty accepted view or invented camera is asserted.

