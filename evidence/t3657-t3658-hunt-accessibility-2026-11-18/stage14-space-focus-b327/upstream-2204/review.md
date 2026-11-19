# Upstream T-3662 / PR 2204 texture-navigation review

Reviewed 2026-11-19, read-only repository inspection and GitHub receipts. No browser, WebGL, publisher, source tests, repository edits, or ref changes were performed for this review.

## Exact inputs

- Failed combined desktop 13–15 run: `44426968208`, DDC `ddc78606998ea8aee589941c6ab6cae76a80440a`, 308 passes / 2 failures. One failure concerns Space focus (separate repair); the other is the zero-page-errors verdict for three GLTFLoader blob texture failures.
- Preserved raw failure log: `/tmp/t3656-ci-ddc78606998ea8aee589941c6ab6cae76a80440a-44426968208-smoke-desktop-stage-13-15.log`.
- Upstream [PR 2204](https://github.com/kevinrhaas/chicago/pull/2204), branch commit `b1c8f6354229363965b439e5dcf78ad3c2276397`, merged as `e72a2e986c42b7ca39c63598846dc98c4af88c1e` (parent `d47d9550bf914d33860a56b99fd11ad2f6f6018b`, tree `7f8d988b1d43011c2d28fed2eb97061e0aa01c49`).
- Subsequent DEV `c23d8a9e85bf37de9c2eb2dce9118cb709edf0da` (tree `f557ac648c66bc3bebbc5c5d9c823f59acfb0dfd`) retains the identical smoke harness.

## Code result

The entire e72 change is 15 added lines in `chicago/4d/tools/smoke_renderer.mjs`: comments plus one logged call at upstream lines 22253–22254 to the existing `settlePictureWork(p14, p14PictureFiles)`, immediately before the intermediate `p14.goto(...&nav=jump)`.

This is precisely the missing wait independently identified in the DDC failure: the 1904 page is entered and its Confidence settings checked, then replaced by the 1835 deep link without draining its picture work. The existing final settlement ran on the replacement 1835 document, so it could not protect the outgoing 1904 document.

The patch does not modify application loading/disposal, probes, picture counters, error listeners, or assertions. The 3-second quiet interval and nominal 60-second settlement polling budget remain unchanged. The zero-page-error verdict still includes errors logged while settling. The existing navigation and suite-completion assertions are unchanged. Independent child review reached the same conclusion.

The helper's cap logs busy work and then navigation proceeds; it does not turn a timeout into a green assertion. An individual page evaluation can exceed the nominal polling budget, so the invocation still requires an external runtime cap.

## Evidence result and limits

GitHub receipts at review time show source-gate run `44422662536` SUCCESS on b1c8f635 (all eight native parts plus aggregate gate). The PR's check rollup contains that source gate, not a completed renderer gate.

The branch's full-smoke workflow-dispatch runs `44443187381` (job `135288850755`) and `44443184558` (job `135288842940`) are QUEUED with no steps or conclusion. The PR body says the intended demonstration is desktop 15 and mobile 15, but the observed receipts do not yet supply that demonstration. Its merge at 2026-11-19T02:17:47Z must not be represented as proof of a successful renderer run.

The DDC errors are tagged to `/1904/` after the Confidence carry-over check, and matching probe warnings report `fetch blob:... TypeError Failed to fetch`. Those buffered tags identify the lifecycle window but do not timestamp each actual rejection. Read-only loader inspection found no premature application object-URL revocation: the GLTFLoader revokes after successful texture load, and disposal closes completed decoded images. This narrows the diagnosis without proving causality.

Recommendation: integrate the upstream fix rather than create a duplicate stage-15 patch. Prioritize actual-world Space validation as coordinated by root. Require fresh complete official desktop and mobile stages 13–15 on the final folded candidate, including the new pre-reload settlement line and unchanged zero-error/vendor/final PASS verdicts. If blob failures recur, resume the timestamped diagnostic rather than ignoring them or modifying application disposal on speculation.

A prepared, syntax-checked standalone diagnostic is retained at `/tmp/t3658-texture-navigation-probe.mjs`; it has not been launched and is not validation evidence. It needs final review of early optional globals before any future run. No claim of deterministic reproduction, specific failing asset ownership, or verified elimination of the race is made here.
