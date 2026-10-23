# Apply only the horse delta after the final person target lands

This read-only audit is pinned to person target tree `5a6ad43ef2dda3fe002d2f5de3476fbba7927af6`, the pending ordinary merge of primary 2f and DEV 59da. It does not approve that target, interrupt its active preflight 15623, or apply any changes. If the eventual landed/squashed DEV tree differs, compare the later delta against these dependency pins before inheriting this scope.

## Concrete result

Horse commit `0b051fd753ff2b2a353e2224bff71959578360b9` has exactly one parent, `2f1bad56ffa14abf2644f8d12f118096944eeec5`; the horse delta is exactly one commit  / 50 changed paths. The proposed person target changes 49 paths against 2f. Only three paths overlap. Actual three-way `git merge-file -p --diff3` using temporary outside-app files returned exit 0 and zero conflict regions for each:

| Overlapping path under chicago/4d | Text result | Required resolution |
| --- | --- | --- |
| docs/LIBERTIES.md | Clean merge | Preserve all incoming declarations and the horse declaration `L-standing-horse-development-2800`. Do not replace the register with either whole side. |
| data/liberties.json | Clean merge | Rebuild from the combined authored register; a clean textual merge does not prove derived counts/content correct. |
| docs/measurements/source_use_coverage.md | Clean merge | Regenerate using the combined target's source/scene data. |

The other 47 horse paths have byte-exact target preimages or are new paths absent from both 2f and the target. There are no add/add, delete/modify, binary or predicted textual conflicts. None of the three overlapping paths has a custom merge attribute. `HORSE-50-PATH-THREE-WAY.json` gives exact base/target/horse blob IDs; `EXACT-CONFLICT-HUNKS.json` is correctly an empty list. This is a finite merge-impact prediction, not an executed cherry-pick.

## Runtime and grounding dependencies

`UNCHANGED-HORSE-DEPENDENCIES.json` verifies 31 exact Git object identities between 2f and the person target. They include the complete 1835 sidecar tree, complete enclosure tree and Western Hotel yard record, committed e1834 heightfield directory, existing parked-transport tree, scene/schema, host/source record, main/yards/terrain/upload-release/spatial-batch/enclosure loaders, skin disposal, confidence, popup, walker/travel settings, angles, complete Three 0.185.1 vendor tree, prebuild code/index and unchanged producer/gate/catalog sources. This compares source objects without decoding, baking or rendering geometry.

The original licensed GLB, horse consumer, support helper, placements and sidecar are six NEW exact payloads from 0b; `HORSE-PAYLOAD-PINS.json` records full hashes. The GLB remains 3,211,248 bytes / SHA256 `41acd9bee7bf05fbcdd813fad965027b01b8801d6a21ca1c22eb2178c8842988` at authored/runtime paths. No incoming target path modifies those payloads. `GLOBAL-ASSET-MANIFEST-DELTAS.json` independently shows the incoming global manifest differences are only the Glessner 1887 and Kimball 1904 entries; no 1835 model entry changed. The global changelog and 1904 research/geometry did change, so this report does not claim the whole app/site is byte-identical.

## Correct dependency and producer sequence

Root should retain the original 0b branch/commit and its source-labelled evidence. After PR #1175 lands, use the actual landed DEV/person target as the base of a new horse PR and apply **only `0b051fd753ff2b2a353e2224bff71959578360b9`**. A squash may remove 2f from ancestry; that does not require merging the old horse branch's entire person history. Do not force-push away the original 0b source snapshot.

The future application is the ordinary one-commit cherry-pick; no cherry-pick/rebase/ref/index operation has been run by this audit. After combining the authored register, run the supported producer tail from the liberty compiler, before gate/publication:

```sh
node tools/rederive.mjs --tail tools/compile_liberties.py
```

The target manifest is unchanged: this starts at 142, compiles the final register, then scene 146, source-use 149 and all downstream exports in supported order. Let its normal convergence finish; do not hand-merge generated backlink/count fields or restore 0b's entire derived output over incoming 1904 data. A schema/source rebase amendment or geometry bake is not predicted. If the incoming Glessner package leaves stale ignored local outputs, verify the current committed package and restore only the confirmed stale generated copies via its existing materializer; never repack stale outputs or alter shared/master geometry.

Run required full preflight on the final combined source (Python 3.11 path, mandatory readers, four jobs and root-controlled lane). The new CPU-support regression and actual measured catalog row are already in 0b and still have unchanged preimages; no new timing record or test framework is needed. Required repository CI still applies; this audit waives no gate.

## Existing visual proof and narrow new-head review

Root reports actual 0b published desktop 60446 and mobile 25665 CLOSED/PASS and personally reviewed all four PNGs; the receipts/evidence were pushed to tickets commit fff88667. The copied `ORIGINAL-0b-VISUAL-REVIEW.md` states that exact source and its remaining limits. Actual mobile used ordinary coarse upload release, retained 12 support triangles / 864 bytes, and passed light no-fetch, normal balanced load, contact, budget, selection credit, confidence hide/pick and disposal checks. Maximum lower-hoof samples remain roughly 30.63 mm despite accepted per-foot minimum gaps; this is not continuous flat-sole certification or a photographic master.

Keep all original proof labels at 0b. Do not relabel those PNGs or source pass flags as the new cherry-picked commit. Before publication, verify the new horse payload blobs still match `HORSE-PAYLOAD-PINS.json` and the listed incoming runtime/1835 dependencies remain unchanged. Rebuild and publish the actual new HEAD so build-stamp/prebuilt-index/recordhash ownership belongs to it, then run the existing bounded production yard desktop/mobile integration phases with their exact source guards and original .97 all-indexed-vertex framing/contact/budget/cleanup assertions. No camera adjustment or automatic retry is implied. This is the narrow meaningful integration check; unchanged canonical human assets, horse mesh/skin/textures and anatomy do not need a fresh source sculpt or historical research round.

No fresh eighteen-cell redispatch, canonical human rebuild, Blender bake or unrelated 1904 visual campaign is justified solely by this unchanged horse delta; root must still satisfy all normal required PR CI and any real later dependency changes. Existing source-side status prose says yard/mobile pending because 0b preceded those actual runs. A later documentation update should cite the successful 0b snapshot and separately state the new target's actual verification, retaining photographic-master/motion/tack/hitch/riding/boarding limits.

## Files and limitations

`AUDIT.json` binds exact source/target IDs. `INCOMING-PATHS.json` and the 50-path table enumerate scope. All operation output is outside app/tickets; no app/index/ref/object mutation, network, test gate, browser, geometry, merge or PR action was performed. The future target may evolve while its own preflight/merge completes; recheck changed inputs if it does.
