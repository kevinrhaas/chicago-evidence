# Adult checkpoint validation (c7de594a7)

Code revision `c7de594a7ef7ec484d8759ff024bdcbec9fab249`, including dev `900d9166`.

All four local check sections passed. The first section initially rejected unsupported source metadata enums; the original failure is retained as `integrated-check-1.log`. After the two text-only source records were corrected, dataset validation and the complete first section passed (`integrated-check-1-retry.log`). Parts 2–4 also passed.

The new portrait cases passed against the published final build at native pixel ratio 1:

| Case | Viewport | Scene age | Paired conversation | Triangles / limit | Draw calls / limit |
|---|---|---:|---|---:|---:|
| Grace Murray Meeker | 390 × 780 phone | 35 | Arthur Meeker | 630,378 / 1,270,000 | 1,621 / 7,800 |
| Albertine Huck Field | 1280 × 800 desktop | 32 | Marshall Field Jr. | 1,751,181 / 4,700,000 | 1,270 / 7,800 |

Both checks assert the intended body and age, visible figure, compact accessible Interact controls, household call, actual paired meeting at 1.4 m, return indoors with mesh/control retirement, another activity requested at night, nearest entrance, home return, and loaded portrait/model images. Both completed with zero page errors and no reported app problems. The logs retain the exact build metadata. The phone screenshot captures a scrolled drawer; the complete source/model pair is in `../portrait-comparisons-4.jpg`.

`final-smoke-runs.json` lists all 15 published renderer stages in both viewports dispatched against this same commit. Dispatch status is not a passing result; completed results are recorded on PR #1932 before merge. These finite functional checks do not assert photographic acceptance.

The final c7 desktop 14–15 run 43017045621 completed with 164 passes and one failure in the Inspect-to-Go-to keyboard handoff; there were zero page errors. `desktop-14-15-first-failure.log` retains that failed run. An unchanged rerun, 43023016089, was dispatched to establish reproducibility; its result was still pending when this note was written. Required CI and all phone stages were green. This failed run must not be described as passing or omitted from the final account.

The unchanged rerun 43023016089 passed all 165 checks, including the previously failing keyboard handoff, with zero failures. Its transcript is `desktop-14-15-unchanged-retry.log`. Both attempts are retained. This folder now records an earlier adult checkpoint: PR #1932 subsequently expanded to include the owner-approved younger residents and dev 62da0f4. Fresh combined validation is required before merge.
