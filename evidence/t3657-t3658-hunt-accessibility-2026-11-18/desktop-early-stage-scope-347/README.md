# Desktop stages 1–12: dependency scope on 3472

Evidence candidate: `ddc78606998ea8aee589941c6ab6cae76a80440a` (DDC).
Reviewed combined commit: `3472ec872d00e33761490b0138b23da1c63daee2`.
Combined tree: `33239df61859c000e76ae6a5bd8ec91124ea8352`.
Latest included DEV: `c23d8a9e85bf37de9c2eb2dce9118cb709edf0da`.
Stage 14 patch: `b3272f5a4ac513dc4cd09819d21f4f5acefbff1d`.

## Conclusion

Retain the successful DDC desktop stages 1–4 and 6–12 with their original attribution. Retain the existing stage 5 geometry/detail-policy evidence and its original b501 attribution. No changed early assertion or behavior requires an early-stage rerun from this delta. Fresh stages 13–15 at both widths remain required. This review is not a fresh renderer result.

## Exact object checks

- All stage 1–12 bodies are byte-identical. The only earlier harness diff adds five comment lines to the existing drain-helper documentation. Executable changes occur only in stages 14 and 15; final error/vendor assertions are unchanged.
- Renderer JS, CSS, HTML and vendor content is byte-identical except `changelog.js`, whose assertions are in stage 13. The merged harness retains DDC's Full-policy pins; DEV's older whole harness was not substituted.
- Candidate assets/data subtrees equal DEV c23 exactly. Only three manifest keys change: the old 2027 draft is removed, 2027's mapped 1904 model is added, and the 1815 Sears-Meeker 1904 model changes. Other manifest metadata is unchanged.
- Both 1812 and 1835 scene indices are exact. The 2027 Prairie and 1815 Prairie structures are explicitly `excluded_by_date` in each, and neither is drawn. All 1,528 master/web asset paths referenced by the 1835 structure index exist and retain identical blobs.
- All three complete teacher Jaunt catalogs—1812, 1835 and 1904—are byte-identical. The changed build-log document is not fetched by the early teacher-handout assertions.

## Stage matrix

| Desktop stage | Changed-input reach and retained scope |
|---|---|
| 1 | Default 1835 boot/profile, scene and layered rendering use unchanged runtime/index/assets. New 1904 geometry is absent. |
| 2 | The 1835 trading/frontage/ground inputs are unchanged; no revised 1904 document is read. |
| 3 | Changed global liberties bytes can load, but all 765 drawn 1835 subject arrays and names remain identical. Sauganash/Green Tree card prose, counts, layout and citations retain exact inputs. |
| 4 | Walking, pick, Inspect/card and budget inputs are unchanged. Relevant Hogan/McKee/jail/Sauganash liberties and source joins are identical. |
| 5 | The 1835 stand geometry and policy assertions are unchanged. Preserve the prior b501→DDC reuse limits; this stage sends no keyboard/focus actions, and new DEV adds only 1904 geometry. |
| 6 | Gate/chrome/welcome runtime and 1835 data are unchanged. |
| 7 | Navigation and southern viewpoints remain in 1835. Prairie-named anchors do not load the 1904 scene. Terrain, anchors and assets are unchanged. |
| 8 | Rendered-view assertions use unchanged 1835 runtime and scene inputs. |
| 9 | Facade/material assertions use unchanged 1835 assets and runtime. |
| 10 | Help/chrome and 1835 environmental inputs remain unchanged. |
| 11 | Sward/community assertions use unchanged 1835 records and runtime. |
| 12 | Teacher catalogs and selected printed content are exact. About-destination checks open living/orderbook, inspect topic/card names and visibility, and do not read the changed Sanborn detail or 1904 build-log document. |

## Shared bytes that intentionally differ

The liberties total grows from 1183 to 1184. Only `L-draft-prairie-20-22-east-2352` changes, and `L-k01-2027-villa-3635` is added; neither covers a drawn 1835 structure. The global hidden DOM is not identical. An early shown hub may display 1184 instead of 1183, but early checks do not pin this numeral, and `.ev-count` uses tabular numerals of the same four-digit width. Fresh stages 13/14 cover the changed global reader.

The sources index retains 709 rows. Only Sanborn 1911 sheet 35 changes: claims 917→922 and inferred counts 741→746. Its use remains `other_scene`. The individual source detail changes edges/names. The Sources catalog first opens in stage 13; stages 3/4 use unchanged per-building citation joins. No changed source-index/detail value feeds the early assertions.

## New coverage and limits

Fresh stage 13 covers changed changelog/source/global evidence readers. Fresh stage 14 covers 1904 models, placement/loading/budgets, and both native UI Space and world-focused Space. Fresh stage 15 covers actual year transfer plus the new drain before the `?nav=jump` reload. Each selected invocation retains its own complete boot/error/vendor checks.

Model-source/image checks and final combined source/moving/upload CI remain separate. This is not photographic sign-off or a full build-log jaunt traversal. The stage 5 result remains attributed to its original commit, viewport and log; no new timing or geometry measurement is claimed.

No source/worktree/ref was modified, and no tests/browser/publisher were run for this review. Future changes require another scoped comparison. A later changelog-only fold concerns stage 13.

## Artifacts

- `provenance.json`: exact hashes, changed paths, dependency findings and review limits.
- `indexed1835-assets.json`: every checked master/web asset path and blob.
- `/tmp/t3657-t3658-current-dev-keyboard/stage5-reuse.json`: original stage 5 reuse limits.

Independent `budget_context` review found no blocker in the stage 14 harness patch and independently checked stages 3/4/12 against the changed data. The original inspect/no-fly predicate is preserved; the added UI case uses native Space and verifies no inspection, flight or planar movement. Real headset behavior is outside that review.
