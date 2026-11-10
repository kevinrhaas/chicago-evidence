---
id: T-2386
title: Match the Wolf Point Tavern to its pictures
state: done
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-10-11
closed: 2026-11-03
pr: 1666
claimed_by: Codex Wolf Point private poster fit resumed after outage 11/3/2026, 10:26:48 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-11-03T21:50:54Z
claimed_run: null
claimed_at: 2026-11-03T16:26:48.929Z
decision: null
decision_answer: null
---

Match the Wolf Point Tavern to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: partial). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1830.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1830_and_1833_engravings.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1832.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_tavern_miller_house_1832.jpg`
  picture: `chicago/reference/images/chicago/chicago_town_view_1833_colbert.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833_hammon.jpg`
  picture: `chicago/reference/images/chicago/chicago_wolf_point_1833_nypl.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- wolf_point_tavern


## Picture-review checkpoint — 2026-10-22

The inspected NYPL Blanchard/Shober lithograph bears a legible 1867 publication line. Pictures show parallel gable-front volumes with two entrances and roof-piercing stacks; current model puts core/addition inline. Register that specific source and implement opt-in ridge/entrance composition before solving.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-10-23** (claim of school_lighthouse_castle_bridge 10/23/2026, 7:14:35 AM CT): Run wrapped after verified frozen recovery at https://github.com/kevinrhaas/chicago-evidence/blob/3575ef6/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md . School recess is prepared UNRUN; Wolf Point latest actual door/log comparison differs. Original full picture-match acceptance remains unfinished and unchanged; no matches or completion claimed. Source-origin identity/date uncertainty and owner-approved attributed school use are preserved.

## Incremental picture-review progress — 2026-11-03

[PR #1631](https://github.com/kevinrhaas/chicago/pull/1631) adds seven reviewed native Wolf Point comparisons, with actual camera/photo/model bindings and source-specific T-3153 dispositions. The accepted target is the low Wolf cabins and sign; the opposite-bank Miller House is not mistaken for the tavern. No Wolf geometry change is claimed. The Images card gains one held picture and five credited links, with publication dates distinguished from depicted dates.

The original eight files contain nine compositions. Seven usable compositions have reviewed comparison records. Herriott's tiny unkeyed view has no securely identified measurable Wolf target. The poster remains inspection-only: [Newberry's primary record](https://collections.newberry.org/asset-management/2KXJ8ZS8068IZ) dates it 1935 and says Copyright Not Evaluated; the older 1892 attribution is unverified. Settle that provenance/rights or establish a justified scope disposition before full original-ticket signoff. Do not invent a camera or matching verdict for either excluded composition.

This is partial progress; T-2386 is not done.

Pushed application revision: `e51af51e7723b1f39586e204f29b64f15263b920`. Fresh published desktop and 390×780 phone checks pass with default geometry release enabled, no page/console/network/server errors, all six captures directly reviewed and source/publication/metadata guards unchanged. [Durable actual runtime proof and recovery](https://github.com/kevinrhaas/chicago-evidence/blob/fd7b25a3f6d3470da24d5071dbfbe4ab6818864d/evidence/wolf-sauganash-2026-11-03/e51af51e7723-default-visitor/RECOVERY.md). Native stage 3 was not rerun on e51; the earlier qualified feature head has both native stage-3 passes. Newer Fort/Pullman changes on dev are being integrated before merge. No final integration, merge or full-ticket completion is claimed by this checkpoint.

The normal street arrival currently frames Miller House in the foreground. The diagnostic Wolf comparisons and credited Images card do not establish accepted Wolf street-arrival framing.

## Merged incremental progress — 2026-11-03

[PR #1631](https://github.com/kevinrhaas/chicago/pull/1631) merged into dev at 2026-11-03 04:03:42 UTC as `18c037e9f756a5190787ef1bd77bacce78331ad1`. The checked source head is `0e838b35b5ba32b61ccd01499310520e160ab4a2`; GitHub gate passed before merge. [Final screenshots, source transcripts and native regression proof](https://github.com/kevinrhaas/chicago-evidence/blob/121eaee6e28f74696131cfd71850e26c8cc259b1/evidence/wolf-sauganash-2026-11-03/0e838b35b5ba-final-default-visitor/RECOVERY.md). Actual published desktop and phone checks pass with default geometry release, all six captures directly reviewed and no page/console/network/server errors. Native stage 3 passes 107 checks at each viewport with zero failures/page errors; all source/publication/Git guards stay unchanged.

Seven usable native picture comparisons and five new credited source links are landed beside the held NYPL illustration. Wolf geometry is unchanged. The 1935 poster remains inspection-only; the tiny unkeyed Herriott target still lacks a secure measurable identification. Original scope/rights dispositions and full signoff remain unfinished. Normal street arrival foregrounds Miller House, so accepted Wolf street framing is not claimed.

This original ticket remains open for its remaining work. No follow-up ticket or whole-ticket completion is filed. The published dev deployment was still pending at the first post-merge read; the merge itself is verified.

**Released 2026-11-02** (claim of T2386 Wolf Point native picture signoff 10/26/2026, 2:23:10 AM CT): Merged scoped facade and credited-picture progress in PR #1631 (18c037e9); original picture coverage and signoff remain. Final 107+107 viewport proof is linked in each ticket.

**Released 2026-11-03** (claim of wolf-poster-credit-20261103 11/3/2026, 4:47:36 AM CT): PR #1652 merged normally into dev as 738f0f81566693980a09f20175a90c5602ec042f. Partial T-2386 progress: the distinct Blanchard/Davis ca.1893 poster now has a credited current-Newberry Images link, with archived primary publication evidence and the current1935/CopyrightNotEvaluated conflict retained. Existing seven diagnostic comparisons and Wolf geometry/cameras are unchanged. Fresh combined desktop/phone cards and GreenTree exterior pass at ebf7befa1afba05947578a5ee08e0cbc8655d98a, all six images directly reviewed; official native stage3 passes107/0 at both viewports and all source/publication/Git guards close unchanged. Proof: https://github.com/kevinrhaas/chicago-evidence/blob/4d1d14b0929b147d586603a59ca04af340851e96/evidence/green-tree-2026-11-03/combined-ebf7-actual-qa/RECOVERY.md . Full original picture matching is unfinished: the separate initial poster camera remains unfitted/unenrolled, the tiny unkeyed Herriott composition still needs its honest scope disposition, and accepted Wolf street framing is not claimed. Release is PARTIAL/OPEN/prnull, not done.

## Final eight-comparison signoff merged — 2026-11-03 21:50 UTC

[PR #1666](https://github.com/kevinrhaas/chicago/pull/1666) merged normally into dev at 2026-11-03T21:50:54Z as `8025bc1ef69db40a1ebf6c5ced6b81de58c9d759`, from checked head `8e5aedc13ec207020c1c08d1ea78ec0eab450654`. The final current-head [GitHub gate 41717780685](https://github.com/kevinrhaas/chicago/actions/runs/41717780685) passed all 1137 source steps with none red, followed by the PR checks. No admin/forced source merge or weakened assertion was used.

The original eight-file inventory is now resolved as eight identified compositions with accepted, native source/camera/model-bound comparisons and one tiny, unkeyed Herriott composition explicitly recorded as contextual/unidentified. The distinct Blanchard/Davis ca. 1893 poster supplies the eighth comparison. Its archived primary publication evidence and the conflicting current Newberry 1935/CopyrightNotEvaluated metadata are retained in the source record and research dossier. The earlier 1867 witness governs the disputed gable opening where the later poster differs, under the recorded T-3153 source-disagreement disposition. The comparison supplies no historical/geographic camera or measured dimensions. Wolf geometry and the prior seven camera/match/image tuples are unchanged.

Actual published desktop and phone body/card/reader checks and official native stage3 passes 107/0 at both viewports are [saved with direct reviews](https://github.com/kevinrhaas/chicago-evidence/blob/7efac0293d29089e13a2c02970ec4d5fa13e3b95/evidence/wolf-sauganash-2026-11-03/final-e32-accepted-both-native107/RECOVERY.md). Final integration preserved the exact Wolf sidecar, all eight reference sets, MASTER/WEB, all seven Images source rows and accepted native reader text. The clear body inspection was a bounded elevated view. [Current integration and per-target identity proof](https://github.com/kevinrhaas/chicago-evidence/blob/9c7942d953a1c06a6acb51488fd96ce22c3bd240/evidence/wolf-sauganash-2026-11-03/final8e5-lake-dev-integration/RECOVERY.md).

The final dev base also contains independently gated PR #1674's night-window stability fix: only its stable instance-translation window hash and shader cache key change. Daylight glow remains exactly 0; positions/normals, Wolf data/models, card and reader are unchanged. This bounded daytime qualification does not claim the entire merged renderer is byte-identical or that a fresh night review ran here.

This closes the original picture inventory under its documented T-3153 scope; no photo follow-up ticket was filed. Public-preview delivery is independently checked after merge. Its existing main deployment checkout failures have left the live build behind dev, so this record claims the verified dev merge and qualified runtime evidence, with no unverified new live-delivery claim.

