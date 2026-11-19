# Independent review of retained primary renderer coverage

Reviewed 2026-11-19 by the accessibility lane, with an independent stage-5 review from its review agent. This records the completed CPU-light, read-only audit; no additional test, browser, publisher, application edit, or Git-ref mutation was performed.

## Conclusion

No genuine coverage hole was found in the scoped reuse of desktop stages 1–12 and mobile stage 1. The retained executions remain historical evidence, with their original source identities. Fresh b1 desktop 13–15 and mobile 2–15 supply the changed destination/release-note integration coverage. This is not an all-fresh thirty-stage run or a substitute for the required source gates.

## Compared objects and records

- Earlier retained source: `7019f986b3773a27a3acc1b47135fa14f9086aa3`.
- Corrected primary: `5034a724d993abe0876a4db7bbfff02d2bb4da0a`.
- Integrated primary: `b1f507400cb743a3985cb1d50de1ebd085bd4f63`, tree `858aa04a6f34329f71efbbe0c472ad5902fea23b`.
- Integrated DEV: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`.
- Reviewed matrix: `/workspace/chicago-evidence/evidence/t3656-browser-classroom-2026-11-18/primary-coverage-matrix.md` and `.json`.
- Reviewed applicability evidence: `/tmp/t3657-t3658-rebase-c676-plan.md` and `/tmp/t3657-t3658-rebase-c676-provenance.json`.

Git-object comparisons established that 7019→5034 changes the stage-13 exact ordinary-Full assertion pin/comment, its budget note and budget test. It does not change the retained stages' assertions or application runtime. For 5034→b1, the only changed runtime JS/CSS/HTML file is `renderers/web/js/changelog.js`; the smoke harness and tools/workflow definitions are unchanged. The changed data, assets and generators were considered separately rather than treated as unchanged application inputs.

## Consumer checks

### Desktop stage 3

`tools/smoke_renderer.mjs:9072` onwards reads Sauganash's existing sidecar citations. At line 9262 it explicitly loads/render the global liberties array, so changed global bytes really are parsed. Its subsequent liberty assertions inspect Sauganash and Green Tree subsets and the popup's collapsed/open behavior, not the monument entry.

A structural JSON comparison found exactly one changed liberty value: `liberties[1088].fields[2].text` in `L-fort-dearborn-monument-3567`, whose subject is `fort_dearborn_massacre_monument_1893`. All other fields, counts, names and entries are identical. `main.js:4114` and `liberties.js:230` explain the hidden global render; that changed hidden paragraph does not alter the inspected subsets or asserted layout. The old result does not validate its new wording.

All 24 changed source-detail JSON files differ only in 66 `edges[].claim` strings, all belonging to `prairie-built-so-far`; other fields and edge counts are identical. The changed source IDs are not named by smoke stages 1–12. The actual Sources implementation reads the unchanged index/uses for its list (`sources.js:96` onwards); detail edges load only when a source detail is opened (`sources.js:159`). The reviewed retained stage paths do not open these revised details.

### Desktop stage 5

The independent stage-5 subreview found no changed exercised 1835 geometry or ladder input. The changed monument, Keith, and Sears/Meeker models and manifest entries are absent from 1835/1812 structure lists and explicitly excluded by date; only 1904 draws them. Git objects confirm unchanged 1835 scene/index/doors/catalog, application loader, published-assets module, main module and smoke harness.

The sweep at `smoke_renderer.mjs:11381–11817` uses the unchanged 1835 `STANDS`. `main.js:7685` moves to same-scene anchors; its frame path defaults `card:false` at line 5693, so the sweep opens no revised liberty/source/jaunt content. The changed 1904 doors are loaded only for year 1904 (`main.js:2448`). Stage 5 does not read asset manifests directly; the scene loader selects the unchanged scene/index entries (`scene-loader.js:373–398`). Retention therefore applies to the existing desktop 1835 detail ladder and policy, not the new 1904 models.

### Desktop stage 12

Guide loads the three catalogs through `guide-view.js:125` and `main.js:7006`. A structural comparison of all 96 rows in the 1904 catalog verified identical complete handout-consumed fields: `id`, `title`, `availability`, `audience`, `version_of`, `featured`, `stop_count`, and `premise`.

`teacher-handout.js:29–53` selects, sorts and projects these fields; the selected suggestions, their order and printed content therefore remain identical. The changed row contains route timing, content-version and destination-order changes that this handout does not consume. The lesson panel stays unopened in this stage and does not fetch the revised 50-stop document. The later About-this-destination checks open living/orderbook, not revised source details (`smoke_renderer.mjs:15082` and `15108`).

## Retained raw-log verification

The three focal matrix records match their archived raw-log SHA-256 values. Each contains the complete selected-body check, zero-page-errors check, both vendor checks, final counts and `SMOKE PASS`. Remote CI teardown appears after the final smoke verdict and is not part of the smoke result.

| Desktop stage | Original source | Passed / failed | Staged + always-on | Time | Raw-log SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 3 | 7019f986b | 107 / 0 | 94 + 13 | 6m23s | `99b557d69fff232e624fd7cccfc1978e21b6645e7abc215513daa9ef01085a2a` |
| 5 | 5034a724d | 30 / 0 | 17 + 13 | 7m54s | `7f8c865e42ac29fcfb72d1ea335afbc24675e388f7aab778f9e8cc635f8510ce` |
| 12 | 7019f986b | 29 / 0 | 16 + 13 | 12m17s | `551de03ad8cdaa4db0933214117dc7601793c3906cf6afb584bcc03c4c7f87a4` |

## Explicit limits

- This audit checks applicability of existing results; it is not a new execution and does not relabel older logs as b1 runs.
- Retained coverage does not validate revised monument wording, revised source-backlink claim text, or traversal of the complete revised 50-stop route. Fresh stages 14/15 exercise the new 1904 integration but do not prove every route stop or photographic face match.
- Source/data/generator gates remain independently required on the actual merged candidate; this review does not certify their completion or authorize a merge by itself.
- New shared-boot/publication/release-note checks are supplied by the fresh b1 runs, not inferred from historical logs.
- The reviewed matrix preserves mobile 2's lost direct shell-exit receipt after reconnection; its complete final summary and body/page/vendor checks survive. No exit-code receipt is invented.
- Timing values are software-rendered validation timings, not device-performance benchmarks. No claim here applies to a future changed DEV, squash/fold tree, application input, or harness without renewed applicability review.
