# Current af desktop stages 13–15 complete

Run 44446945583 / job 135301280663 completed the published desktop 1280×800
range: **314 passed, 0 failed**, including 301 staged assertions and 13
always-on checks counted once for the group. Elapsed harness time was
**69m44s**. The body completed with zero page errors, both vendor checks
and final SMOKE PASS.

The complete log binds direct workflow-dispatch checkout
af466d1638fda72a468ecd3ac22456844b870c1b through the exact Git HEAD output,
publisher `build af466d16`, and the subsequent published mirror invocation
with SMOKE_VIEWPORT=desktop and SMOKE_STAGE=13-15. No separate remote
build-manifest byte hash is claimed.

The [final scoped renderer matrix](../final-af-scoped-coverage/README.md)
retains the original earlier-range and phone evidence. Source aggregate and
moving-frame retry still require terminal success; this is not an overall
release verdict. All prior failed/capped runs remain unchanged in the archive.
