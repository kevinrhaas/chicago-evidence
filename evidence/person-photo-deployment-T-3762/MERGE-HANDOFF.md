# PR #2371 merge handoff — 28 November 2026

The owner explicitly transferred PR #2371 merge work to another session. This session will not push its source branch, mark it ready or merge it. Dev only; no production authorization.

At handoff, the other session's remote source was `403af078acbbf1d2251fdc049dda8c930717f2b7`, tree `5494319a999a4b8ebb7130057b627a30f2dcc681`, with parents `22966758e90c9316b66596c08c98881e368cdac6` and `b74eeba3570fce60c58e8d862168af399be77fd2`.

## Outstanding test cleanup

[Review this four-line patch](merge-handoff-2026-11-28/retire-asserted-page-before-reload.diff). It is absent from 403af. It stops only the outgoing page's native animation loop AFTER that page's assertions and BEFORE the existing 60-second picture settle and navigation. The replacement page boots its normal renderer. No assertion, timeout or error listener changes.

A fresh original desktop stage3 on source 2296675 failed: 106 passed, 1 failed: navigation canceled 5 pending GLTF blob reads after the existing 60-second settle expired while rendering kept running. [Original complete log](merge-handoff-2026-11-28/failed-original-desktop3.log). The cleanup's direct local reproduction passed 107 checks, 0 failed, zero page errors in 530 seconds, within the original 600-second cap; its final picture settle completed in 9.6 seconds. [Complete local log](merge-handoff-2026-11-28/local-desktop3-after-retirement.log). This is a diagnostic against that prior app runtime, not blanket qualification of the current integration.

## Preserve the exact test provenance

Our uncommitted canonical integration has tree `118bbfb26f26ed746a242c00a4285b80a8538334`, represented ONLY by isolated test fixture `68fd236318161d27691af26e8593409aea442cca` on `validation/t3762-final-118bbfb26f26`. Never merge that synthetic test ref.

It differs from403af in exactly four paths: `data/liberties.json`, `docs/LIBERTIES.md`, `docs/STATUS.md`, and the four-line `tools/smoke_renderer.mjs` cleanup. Renderer modules, human assets and photo libraries are identical. Compare all differing files before reusing results; the entire source trees are not identical.

The current original native catalog has 1,458 checks, retaining every one of the previous 1,454. The local current-integration gate is PARTIAL; no complete current project-gate receipt has been recorded here. Its coordinator stops scheduling after the handoff and lets active original parts finish within their existing caps. Raw receipts remain in the local work folders.

The original native fixture run is [46139213849](https://github.com/kevinrhaas/chicago/actions/runs/46139213849). [All 30 published viewport/stage requests](merge-handoff-2026-11-28/fixture-browser-runs.json) are retained, pending at handoff. These run on the fixture above, not on403af; the merge owner may review or retire them. No new fixture workflows will be launched here.

The actual source head still needs its native gate and aggregate, portable-human reproduction/model opening, moving-frame and phone upload/release checks, plus complete published desktop/mobile qualification. Verify the actual postmerge dev build and served modules/data before calling it delivered.

## Preserved work and remaining limits

The canonical merge completed 209 ordered writers, a 7-step dependency pass, and one 60-step final tail that moved nothing. All 99 photo inputs, 536 outputs, 8 photo/hair modules and 7,610 assignments remain protected. All 78,927 workbook cell values/comments/hyperlinks matched; exact incoming workbook files were retained and the resident-audit generator check passed. Fresh creator browser walk-through: 64 checks passed. These local details are in `/workspace/work/photo-qual-b/chicago/4d/work/deployment-trees-c18420/` if the workspace is shared.

[The app gallery](GALLERY.md) still shows the prior normal source 2296675. It must not be relabelled as a fresh capture of a changed runtime. Original William/Sarah head mappings are retained. William's narrow frontal eye strips remain a separate T3553 follow-up; no speculative geometry experiment was shipped. Physical-GPU crowd FPS remains unmeasured.

An earlier automatic approval review rejected marking ready while integration/auxiliary/release checks were pending: “Marking the PR ready could trigger review or merge automation while documented integration, auxiliary checks, and dev qualification remain pending; repository instructions require keeping it draft until those checks pass. Do not bypass this rejection through a workaround or indirect execution.” Complete the prerequisites and retry the original ready action; no CLI readiness workaround is authorized by this handoff.

The previous merge lease has been released; see [release receipt](merge-handoff-2026-11-28/lease-release.json). The next local focus is William Grey's frontal eyes on an isolated checkout.
