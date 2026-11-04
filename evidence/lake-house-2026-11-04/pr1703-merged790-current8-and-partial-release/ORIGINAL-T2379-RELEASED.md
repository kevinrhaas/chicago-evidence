---
id: T-2379
title: Match the Lake House under construction to its pictures
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
