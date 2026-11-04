---
id: T-2374
title: Match Cobweb Castle to its pictures
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
claimed_by: run 11/3/2026, 6:31:05 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/41746386858
claimed_at: 2026-11-04T00:31:05.635Z
decision: null
decision_answer: null
---

Match Cobweb Castle to its pictures.

Owner, 2026-10-11: "if you have an image you should work towards it until it's a photographic representation of any images even drawings are ok, but it should look exactly perfectly like the image or drawing"; "redo any work already done to meet this high standard"; "you don't wrap the case until it matches the photo".

This building was built without being checked against its pictures (inventory of 2026-10-11, T-2368; compared before: no). Open every picture listed here and read the building off the picture itself. Solve each one's camera into `data/reference_views/<structure_id>/<view>.json`, render with `node tools/photo_match.mjs`, and rebuild until the side-by-side shows nothing the picture shows differently: massing, bays, every opening's shape and height, ornament, cornice, porch and stoop, roof and chimneys, fence, materials and tone (AGENTS.md rule 11; `data/reference_views/README.md`). What the picture does not show stays reconstructed and recorded in `docs/LIBERTIES.md`.

Pictorial sources are tier 5: form only, never a coordinate. Several are drawn from memory or later (Andreas 1884, Kurz & Allison 1893), and some post-date 1835 (each is evidence of its own date, scene 1835-07-01, AGENTS.md rule 3): the build follows what each shows of the building as it stood then, and the match record says which picture governs where they disagree.

Pictures:
  picture: `chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`

**Acceptance:** every reference view of the building(s) below has its camera, its side-by-side from the GLB in the tree, and a match record with verdict `matches` and nothing open. The PR carries the before and after side-by-sides, plus desktop and 390x780 in-app shots with no page errors.

## Image gate
- cobweb_castle


## Picture-review checkpoint — 2026-10-22

The 20-vertex centre/wings/tails footprint is reduced to a bounding box by `log_dwelling_params`. Compound massing is not built; a camera cannot fix it. Implement opt-in compound geometry without changing other cabins.

No matching verdict or completion is claimed. See the [shared compound-render checkpoint](https://github.com/kevinrhaas/chicago/blob/steward/t3040-fort-reference-groups/chicago/4d/docs/RESEARCH/fort-reference-groups-T-3040/README.md) for source/date findings and the next implementation step.

**Released 2026-11-03** (claim of Codex Cobweb recovered original-panorama increment 11/3/2026, 8:05:03 AM CT): Merged PR1665 to dev as ae54d698c93f0543a233e7127e9ff036efe10506: one credited original-panorama Images link, actual desktop/phone card and native107x2 passed. Partial only; source geometry/camera/grade unchanged, private camera remains unsolved and full compound picture match unfinished. Source proof b1a59536572f005a24344fbfc602a6bc114e6ad6; fresh QA https://github.com/kevinrhaas/chicago-evidence/blob/b6168fa2fb109f505388df61f698949605c8b95c/evidence/cobweb-wolf-2026-11-03/fresh-07b8-card-and-native-stage3/RECOVERY.md. Keep original open with PR null; no completed-match claim.


## Exact native-worker central-front aperture handoff — 2026-11-04

This is one bounded visible partial increment of existing T-2374, NOT a full Cobweb Castle image match. PR1665's credited picture link and research work are already merged; the current producer ALREADY consumes all FIVE compound_parts. Do not replay that work or the obsolete October22 bbox-only diagnosis.

Read the [closed current-source/native-controls/actual-picture readiness](https://github.com/kevinrhaas/chicago-evidence/blob/86aea589f0c096f73bcf47f9dd8c9840710108b7/evidence/cobweb-2026-11-04/native-front-aperture-readiness-current42b/RECOVERY.md) and [actual same-pixel source/native crop + projected-landmark review](https://github.com/kevinrhaas/chicago-evidence/blob/39acf006e8bd11368e5c3df4e34c550c1fac3cd9/evidence/cobweb-2026-11-04/retained-native-face-correspondence-review/RECOVERY.md). Root read the full plan and directly viewed the full panorama, genuine af1f native comparison, equal8x crop and overlay: triangle1/2/3 is the existing central+Y closedgable facing the camera. WorkingLOCALface correspondence is qualified ASRECONSTRUCTED, not a solved global camera. Fresh source/ownership contract must preserve latest dev. Current75cd3593 includes merged SauganashPR1680 metadata/gallery at6953, plus independently merged1679walks/1675drawbridge/fold. Exactnativehandoff audit confirms ONLYPruyneKimball and DearbornBridge MASTER/WEB registry entries differ from42b; all82log-family rows and CobwebMASTER/WEB/source/producers are identical. Preserve those new foreign rows and current placement/entrance data; do not replay old registries.

The source AgencyHousegable shows TWO lower dark upright marks plus ONE small upper mark, while current native centralfront is one centred door and no upper light. Count is inferred from the identified verifiedpublic-domain Wentworth1881/WauBun1857 reproduction of1831 scenery; exact localposition/size/shape/function/casing remain RECONSTRUCTED. No source-measured metric fit, glass, interior, atticroom, whitepaint or literal historic door/window function is established. The earlier wrong-side reading was corrected; retain the correction/history.

The ONLY proposed geometric scope is one optional explicit aperture set selected for Cobweb's existing central+Y wall/gable, implemented locally in log_dwelling.py and log_dwelling_params.py plus target data. All existing data-only two-window/upper-light/extra-room trials were actually rejected by strict current params, so a producer control is required. Do not weaken generic forbidden-compound validation, split a room to multiply openings or substitute Wolf's elbow. Preserve all5compoundrectangles/roofs/footprint/wings/stack/materials/placement/defaults and accepted Wolf elbow. The new option must be absent/default-off for every old unrelated record.

Use neutral exterior dark recess/aperture geometry with coherent surround/relief, not a renderer/image overlay or fake glass claim. Strictly validate finite bounded coordinates, supported room/face/kind, non-overlap, wall/rake containment and unsupported combinations. Upper geometry belongs on the actual+Y gable plane using existingoutboard convention, not buried/floating. New explicitset overrides only centralroom's singular oldfrontopening, so the old centre door does not remain phantom/duplicated among the new marks. At most ONE of the two lower marks may have an explicitly RECONSTRUCTED entry role to keep access usable; source does not establish which. Native frontage/entrance geometry and reader must share actual returned rectangles and no phantomoldcentraldoor; record/body/native groundedentry tests must agree.

Keep helpers local; do NOT edit sharedcommon/openings.py,logwork.py,mesh.py,emit.py,materials.py, genericschema or recipescheme. Actual current expected family is82log_dwelling MASTERs plus actualvariants; preserve accepted Eliza/Wolf/Miller/Carpenter defaults and every foreign row/newkeeper. Native staleness is authoritative: if it crosses into another family or a same-model peer rebuild, STOP and coordinate, do not stamp a larger roster fresh. Otheractivejobs are Jail41734994705/frame_dwelling271, NEfirstfort41739288717/outbuilding243, secondfort41740271907/fort_structure25 and GreenTree41742893188/frame_tavern data-onlyone. Leave those runs/claims/topics/source untouched.

Before the FIRST geometry-source commit, genuinely build/qualify every actual affected log-family MASTER/variant on pinnedUbuntu26.04/SHA-verifiedBlender4.5.3 in supported bounded600s batches. Record actual complete normalizedinputs and realoutputs; never predict/stamp hashes. Only actually regenerated byte-identical MASTERs may retain genuinely bound oldWEB; changed outputs need actual nativeencoding. CurrentCobweb MASTERaf1f33c0...139824B and WEB49cfcb86...31804B are genuine baseline, not newresult. Preserve foreign entries through native registrymerger/currentdevintegration; true both-sides model changes require genuine rebake.

Capture ACTUAL controlled private BEFORE/AFTER using the retained source/camera and genuine old/current assets. Its frontRMS1.848px and heldoutrear20.751px do NOT solve it; keep UNSOLVED/unreviewed/private, never enroll canonically or take a grade/spot shortcut. Camera/source/photo/MASTER bindings stay exact; do not rename old observations current. The new native comparison/rootpixels must show a useful two-lower/upper-count improvement without body/wing regression. If credible face correspondence or useful countgain fails, preserve recovery and LEAVE APPUNCHANGED rather than asserting a confident numericshape. Other broadcompoundwidth/wings/subroof/camera/datecontinuity remain OPEN.

Partialclapboarding is separately textattested afterward, exactextent/height/July1835continuation unknown; currentbarehewnlogfinish is NOT fixed by apertures. Whiteengravingpaper is not whitepaint evidence. Source is retrospective1831context, not unchangedJuly1835 proof. Preserve sourcewarnings/history/already merged Imagescredit and current grade; no camera/attestation/MATCHES/originalcompletion shortcut. No newphoto followups, new split, done--anyway or done--pr for partialwork.

Root reviewed owner-visible platformdraftPR219 exactaa9d7d2322d3abbc78d72526146c018a241c643e feature steward/chicago-native-exact-ticket-20261103 withall11CIgroups/official15case bothviewportsmoke/bothhostedchecks passed. Dedicatedexactjob literalUbuntu26.04/150min uses verifiedBlendercache; platformmain stays unchanged. After this preservednativehandoff sync/release and freshownership check, one exacttargetT-2374/appchicago/slice1/slices1/lanecobweb-apertures-native-20261104/defaultmodel-effort dispatch is authorized; metadatahandoff alone claims no dispatch orgeometryresult. No unrelatedqueuefallback/duplicateother4jobs/hostBlender.

All four complete source-check parts must PASS BEFOREfirstsourcecommit, actual foregroundcommands bounded600s/properreaping/verdicts. Preserve assertions/light-tierfloor, pricecurrentheadroombeforedeal, ask actualcommittedheadPRchangelog/IDquestions and push draftdevPR promptly for a usefulcheckedincrement. Exactheadpublish+bytecontract, actualdefault1835 desktop1280x800 AND phone390x780 body/apertures/credit/record/groundednativeentry andappropriateexistingnativesmoke/zero page-console-network-servererrors are release requirements. Split customQA into boundedlegs as needed; coarseALL15budget versusactual scopedtests stays explicit. Rootmustdirectly reviewactualpixels; requiredhostedgreen/ordinaryexactheadprotecteddevmerge only.

Append liberty/reconstruction/sourcewarnings/STATUS/ROADMAP without replacing concurrent suffixes; one small visitor-facing changelogentry. Save qualifiedgeometry/source4/PR/merge/delivery checkpoints to chicago-evidence. After usefulmergedpartial, releaseoriginalOPEN/PARTIAL/DIFFERS withremainingdiscrepancy/recoverypointer. No directdev/mainpush, admin/forcemerge, fabricatedsource/rights/dimensions or forcedcompletion.

**Released 2026-11-03** (claim of Codex Cobweb aperture native handoff 2026-11-04 11/3/2026, 6:21:49 PM CT): Reviewed bounded reconstructed-face aperture native handoff saved; OPEN for authorized exact T2374 worker. No geometry, dispatch or full-original completion claimed by metadata handoff.
