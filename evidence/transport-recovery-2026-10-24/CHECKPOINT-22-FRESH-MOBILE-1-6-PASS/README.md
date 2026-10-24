# Fresh mobile parts 1–6 pass

On unchanged head be56fb269eee6aa7963b8a8d76d5a950f56f857c/tree a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5, the published mobile checks passed:

- Parts1–2:181staged checks,300.137s.
- Parts3–4:125staged checks,305.198s.
- Parts5–6:28staged checks,487.415s.

All three actual command/outer return codes are0, with zero page errors and complete owned-child cleanup/none remaining. The earlier fresh mobile14pass is retained on the independently rehashed identical published tree. Current verified mobile coverage is1–6and14, not the full matrix. Desktop14's1800s timeout/browser-closed completion failure remains in checkpoint21 and is not counted as passed; a new3600s attempt is queued after remaining parts.

Normal gate/moving/report/warrantedCI metadata areSUCCESS for the same candidate; independent unfiltered full-smokeCI is still running at the saved snapshot. No DEV merge, delivery or production promotion. PR1279 remains draft.

Parallelqueuework is isolated in an ordinary separate clone forPR1281/T3113, with a normal lap acquired15:19:39UTC and three-hour expiry. PR1281was converted to draft because its existing photo residual and missing child image-gate section are not acceptance. Local authored geometry/provenance correction and two generated merge conflicts remain WIP, not committed/pushed or photo-qualified. That candidate has no effect on the frozen transport source/mirror.
