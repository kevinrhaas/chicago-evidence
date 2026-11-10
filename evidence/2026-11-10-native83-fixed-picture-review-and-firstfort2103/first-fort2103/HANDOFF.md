# T-3041: finite northwest first-fort picture coverage

Prepared in isolated `/tmp/nov9-group-cobweb`, branch `steward/t3041-nw-camera-coverage-20261110`, exact dev base `c5382c727ae06e0ba1cd6816cc072cbfba4d963d`. Root owns claim `ac51fdb0` and integration/PR duties. No active-full source, ticket, GitHub or geometry writes. One local-only source checkpoint commit `210324205d68d3a1c1b8e2c909ca2c4bcd69af07` (no push); full gate and fresh pairs remain pending. Cobweb's previous source work is preserved in local stash and `/tmp/nov9-cobweb-group/`; its fresh-before/ready-after fixtures are untouched.

## Final derived correction and truthful visible announcement

Final local branch head is `4d8292da47df257cbdbec8476cb54de9a2385706`, parent source checkpoint `210324205d68d3a1c1b8e2c909ca2c4bcd69af07`. No push. The authoritative compiler ran `--all` successfully across1812,1835,1904; `--all --check` then passed with “OK: every committed sidecar is what the dataset compiles to”. Exact full diff from source checkpoint is one NW1812 sidecar grade block plus the corrected pending changelog entry. Every non-grade part of that sidecar and all other sidecars are identical. Root should cherry-pick/fetch this final local head or use `DERIVED-BADGE-AND-ENTRY.patch`; `FINAL-COMPLETE-SOURCE.patch` includes both commits relative to devc538.

The badge changes **inferred → attested**. The compiler-owned reason becomes **“Pictured: 2 of the pictures on the Images tab show it.”** Its picture list becomes `[early-currey-1912-first-fort-birdseye, kurz_allison_1893]`. AGENTS.md rule12 explicitly defines attested as having a reasonable whole front/oblique/side/rear picture. These retained retrospective drawings show the blockhouse sufficiently for that existing rule. This classifies pictured appearance; it does not attest every dimension, exact parametric geometry, historical optical camera, source date precision, or acceptance against every picture. All per-attribute confidence and native geometry remain unchanged. No hand upgrade/downgrade or manual why-string edit was made.

The read chain is `compile_scene.structure_grader → grade_structures.grader → compile_pictures.read_tree/derive → grade_structures.depicting`. The last function adds each own canonical camera’s `library_image` or `source_id`, including diagnostic cameras, even without a match record. `compile_pictures.read_tree` explicitly skips `.match.json`; later match verdict changes do not affect this annotation. The existing camera/grade behavior is preserved, not weakened. `NW-SIDECAR-COMPILER-RECEIPT.json` records exact before/after and full owner receipts.

The pictured badge is a visitor-visible change; the earlier internal-only announcement was corrected in the same derived commit. The Images list itself remains unchanged. No new Images feature or site comparison link is claimed. Full PR gate and actual new canonical pairs remain separate pending work.

## Original source camera scope

- `T3041-TWO-NW-CAMERAS.patch` adds exactly two canonical JSON records under `data/reference_views/first_fort_dearborn_blockhouse_nw/`. SHA256 `0b11084ff1bca54d69bc2bda55db7b5aa8079d1327dc61dd902ebe109f60b875`, identical to prepared Nov9 patch. No existing camera changes.
- Currey uses the exact outer-picket world camera with a rigid anchor transfer: eye [65.92,56.20,49.69] -> [66.87000000000012,27.00000000000003,49.69]. All intrinsics, basis, image/source, fourteen scene members, world placements and credited-member set preserved. Original outer camera remains.
- Kurz & Allison panel1 uses the exact existing T-3040 thirty-member NW world camera; no pose refit, new credit membership or historical optical-viewpoint claim. Both cameras remain explicitly diagnostic, suppressing From-this-spot.
- There are deliberately **no match JSONs**. Actual renders must generate fresh unreviewed bindings, hashes and comparison pictures. No manual GLB/group SHA attestation or inherited `matches` verdict.
- `PENDING-CHANGELOG.patch` contains the historical source-checkpoint entry. The final `change` entry now announces the pictured badge and preserves diagnostic/unfinished-match limits; use the final two-file derived patch or complete final patch, not that obsolete historical announcement.
- `COMPLETE-SOURCE.patch` combines the two additions and optional pending chore entry. All three files are now in one local-only source checkpoint commit, explicitly requested by root; no GitHub push. The source-only draft does not claim the full gate or fresh renders have passed.

## Verification actually completed

`CURRENT-DEV-RIGID-PROOF.json` regenerates the affine check from current dev's actual old camera and sidecar placements: six frame/affine samples on each of fourteen members, including 22.86m staff sample; maximum projection/depth difference 7.389644451905042e-13. This proves unchanged world framing, not a historical fit or image match. Reproduce with `/tmp/nov10-firstfort-nw-coverage-verify.py`.

The existing owners passed: `python3 tools/compile_pictures.py --self-test`, `node tools/test_photo_match_group.mjs`, `node tools/changelog-entries.mjs --check`. `git apply --check` passed before applying source additions; `git apply --check --cached` passed after writing the untracked files. No full gate/native/browser claim.

Actually viewed both full current source pictures: the Currey889×588 bird's-eye and Kurz1538×859 panel1. Currey's drawn northern/western gate, two blockhouses, courtyard ranges/galleries and dashed route are visible; the dashed route does not depict hidden covered-way geometry. Kurz's across-river composition hides many thirty-member context structures; its towers/staff perspective remains inconsistent with the retained contemporary plan. These readings do not assign the unlabelled galleried outbuilding to an individual context record.

## Visitor-visible limit and actual owners

`IMAGES-CARD-BEFORE-AFTER.json` executes the **actual** `tools/compile_pictures.py` derive function with current-dev NW structure text, source records, existing outer camera, candidate cameras, and the actual held Prairie image library index. Before/after output is **exactly equal**: two existing entries, the held credited Currey picture and Kurz/Library of Congress link. NW already cites both sources and the outer camera already credits NW. Neither diagnostic camera gets a historical spot.

The source cameras add canonical **review coverage**, and their authoritative sidecar derivation changes the visible **pictured badge**. The existing Images list and its access remain unchanged. Comparison exposure would require `tools/compile_pictures.py` and its consumer `renderers/web/js/pictures.js`; root explicitly excludes that broader change today. `tools/publish.sh` publishes the generated picture index but currently does not copy `docs/RESEARCH/photo-match/` comparisons to the visitor mirror. Retain actual source/evidence comparison files and link them from the PR; do not claim a new site/card feature or publicly reachable site comparison URL without testing it.

## Source credits and scope retained

`SOURCE-CREDITS.json` copies the existing recorded findings; no external rights research or upgrade.

- Currey: “Bird’s-Eye View of Old Fort Dearborn,” p27 of J. Seymour Currey, *The Story of Old Fort Dearborn* (A.C.McClurg,1912), illustrator uncredited; held Commons/Gutenberg copy. Retrospective first fort1803–1812. Recorded verified/public_domain. Caption provenance follows the1899 Tribune drawing of Van den Berghen's1898 model; this run does not independently re-verify that underlying chain.
- Kurz & Allison: *Chicago In Early Days,1779–1857* (Chicago,1893), Library of Congress Prints and Photographs Division, [catalogue](https://www.loc.gov/pictures/item/2003656685/), **panel1**, “Old Fort Dearborn. Erected1803.” Existing held `p4_0.png`; recorded verified/public_domain. Do not substitute panel5 (rebuilt1835) or panel8 (town1830).
- Existing Whistler1808 measured plan, T-3335 owner choices, staff height, positions, range identities, gate, cupolas, magazine/NE caps and west wicket are preserved. No new source, surveyed dimensions, date precision, geometry or depicted context identity. The compiler-owned pictured grade annotation is explained above; no attribute grade or accepted-match claim changes.

Original T-2387 and T-3041 remain **partial** until actual current-native reviews and the existing all-pictures acceptance are legitimately resolved. Existing finite matrix, Getty/Chicagology source-use limitations and Lossing-world-camera exclusion remain at `/tmp/nov9-firstfort-coverage-next/`; this patch does not turn them into new geometry tasks or close those pictures.

## Fresh actual comparisons after grouped native

Root first completes the current grouped-native adoption and normal branch/dev integration, then applies this separate patch to its T-3041 branch. Recheck absent paths; never overwrite a sibling's NW camera. Use unchanged source JSON bytes before rendering. Parent owns serial GPU slots.

From actual full app cwd, two normal commands (run serially):

```bash
source /tmp/chicago-resume-env-20261109.sh
cd /tmp/chicago-west-wicket-20261109/chicago/4d
timeout 570s node tools/photo_match.mjs data/reference_views/first_fort_dearborn_blockhouse_nw/currey_1912_birdseye.json --out docs/RESEARCH/photo-match/first_fort_dearborn_blockhouse_nw > /tmp/nov10-firstfort-nw-currey-render.log 2>&1
```

```bash
source /tmp/chicago-resume-env-20261109.sh
cd /tmp/chicago-west-wicket-20261109/chicago/4d
timeout 570s node tools/photo_match.mjs data/reference_views/first_fort_dearborn_blockhouse_nw/kurz_allison_1893_panel1.json --out docs/RESEARCH/photo-match/first_fort_dearborn_blockhouse_nw > /tmp/nov10-firstfort-nw-kurz-render.log 2>&1
```

Each prints its bare random `/tmp/photo-match-*/<view>-render.png`; copy those untouched to a fresh external evidence folder immediately. Retain actual resulting match files and complete JPEG pairs. Record actual current source HEAD, native assets/run identity, source/camera/group/each-member mesh+placement hashes from the generated records. Review actual whole pictures and comparisons; use T-3153 only for named visitor-scale discrepancies and actual T-3335 owner choices. No prewritten blanket `matches` finding. Re-read existing original acceptance/matrix and all named source limits; these two comparisons alone do not cover every original picture/component.

Run ordinary image schema checks and compile-picture/grade owners on the full tree, inspect any derived grade/picture delta instead of manually upgrading it, and complete normal required gate/runtime/preflight for the eventual actual PR. Root owns shared STATUS/ROADMAP/changelog integration, source/evidence preservation, PR creation and protected dev merge. Do not close the original all-picture ticket from a successful parser or this mathematical proof.

## Draft PR description

The first fort's northwest blockhouse lacks canonical review records for two pictures already held and credited by the project. This adds diagnostic NW cameras for Currey's fourteen-member bird's-eye group and the existing thirty-member Kurz & Allison panel1 group, preserving their exact world poses, intrinsics, surveyed scene placements and source credits. Currey is only re-anchored mathematically; Kurz's camera is copied without refitting.

This is a bounded picture-coverage increment with a visible pictured badge change: town geometry, per-attribute confidence and the visitor's Images list are unchanged. Fresh actual current-native comparison files and their generated unreviewed/reviewed records must accompany the final PR; all-picture sign-off remains partial wherever the existing finite acceptance is unresolved. Affine preservation, card-output equivalence and existing picture/group owners pass; append actual native/render/required-gate receipts only after they exist.
