# af mobile stages 13–15 complete

Run 44446951072 / job 135301296300 completed the published mobile 390×780
range with **314 passed, 0 failed** in **24m41s**: 301 staged assertions plus
13 always-on checks counted once for the group. The body completed; zero page
errors, both vendor checks and final SMOKE PASS are present.

The complete job log binds the direct workflow-dispatch checkout to
af466d1638fda72a468ecd3ac22456844b870c1b through `git log -1 --format=%H`,
the normal publisher's `build af466d16` line and the subsequent published
mirror invocation with SMOKE_VIEWPORT=mobile and SMOKE_STAGE=13-15. It is
not the source workflow's PR merge checkout. No separate remote source-byte
or downloaded build-manifest hash is claimed.

Phone coverage now spans all stages through these separate cohorts:

| Stages | Original head | Passed / failed | Staged | Always-on | Completion |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | 3472ec872 | 95 / 0 | 82 | 13 | Accepted recovered kernel exit 0; original supervisor was killed and normal end receipt remains unavailable |
| 2–12 | 3472ec872 | 490 / 0 | 347 | 143 | Eleven normal child exit 0 receipts, complete guards and unchanged publication pins |
| 13–15 | af466d163 | 314 / 0 | 301 | 13 | This complete remote published range |

[The local 1–12 artifact map](../347-mobile1-12-complete/verification.json)
retains every log and receipt. [The af fold proof](../../combined-347-c23-20261119/folded-af/verification.json)
limits its difference from 347 to the T3562 changelog fold; the affected
13–15 range above ran freshly on af. The subsequent DEV8c publication change
has [separate targeted execution and dependency proof](../../dev8c-publication-complete/README.md).

This is coverage assembled from the original attributed cohorts, not a single
full-range run. The source aggregate, desktop 13–15 and moving-frame retry
remain required. Live remote-media/CORS checks and weak-device performance
are outside this harness evidence. All older failures remain archived.
