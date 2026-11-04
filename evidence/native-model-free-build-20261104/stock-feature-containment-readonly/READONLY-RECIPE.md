# Existing model-free native build: contained stock feature bake

**Supported with zero workflow changes**, provided root explicitly contains the generated checkpoint in an isolated feature whose parent PR to `dev` remains **draft and unarmed**. Nothing was edited or dispatched by this investigation; no GPU or source/ticket/ref mutation occurred.

At final read, dev is0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4. Active Chicago workflow365585052 is `.github/workflows/chicago-4d-bake.yml`, blob`e0792107caa1abc001694705e628207484a3980b`, fileSHA256`970594c5935a0d27fb58a44797798fe498789d401be678340bef312b38f16bc5`. Bakejob explicitly uses Ubuntu26.04 and `generators/blender.pin`4.5.3: archiveSHA256`975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845`. The pin file blob is`26c2ddf89c36505d949425280ccc5c7bd486bc2e`, fileSHA256`670f43f8f3f22aaafd2743a93b9c6b179a0ccf81991d8f62f2492973dc92fff6`. Fresh extraction verifies the archive; existing cache executable is reused.

## Exact future call, not executed

POST `/repos/kevinrhaas/chicago/actions/workflows/chicago-4d-bake.yml/dispatches` with a root-reviewed isolated FEATURE ref and input `only=first_fort_dearborn_blockhouse_nw,first_fort_dearborn_blockhouse_se`. The workflow filename is already registered on main, so a feature-ref definition can be dispatched without a main merge. The feature must carry the reviewed dev workflow, not main's older floating-image definition. No model/API authoring step is involved.

`bake_ref.resolve(workflow_dispatch, FEATURE)` returns FEATURE. The actual source SHA is captured in `steps.baseref.outputs.sha`; check that against the approved source-half checkpoint. `bake.outputs.base` is that same feature name; `open-pr` passes it as `--base "$BASE"`. The ready content PR is `steward/bake-RUNID` **into FEATURE**, and `gh pr merge "$PR_NUM" --auto --squash` acts on that child PR only. Root may explicitly authorize this reversible unqualified feature checkpoint while leaving the separate parent-to-dev PR draft/unarmed. The merge-ready helper also filters drafts and hold. This containment does not authorize delivery into dev.

The scene bundle step runs only for `baseref.branch == dev && event != push` (workflow631). On FEATURE, no bundle output is set, `publish-bundle` requires bundle==1 and skips (1007–1009), and its dependent fresh-consumer skips. No release/latest-good pointer is written. Pages pushes run only on main/dev; production promotion is a separate owner-dispatch-only workflow not called here.

## Selected assets and order

`only` accepts comma-separated **structure IDs**. build.py resolves every current scene's date, builds each distinct selected phase once, then every version of the selected IDs. Both first-fort IDs currently have one phase `first_fort_1803`, lifetime1803-08-17 through1812-08-16, so the existing all-scene default reaches the1812scene. Neither target has a version directory at the captured dev. A fresh candidate/producer recipe rebind still precedes any future build; the earlier projected two-default plan is not new build proof.

This two-record trial should produce the two selected MASTER paths and corresponding WEB paths. A shared-producer change would require recomputing affected scope; it is not silently covered by selecting two. `bake.sh` emits MASTERs with the pinned binary, passes the same selection to pure-Python emitters, then derives exactly the emitted WROTE paths, including versions. It compiles sidecars globally, publishes, and runs check.sh before committing. The exact published mirror is uploaded and tested at both viewports across18legs before the child PR opens. Root still reviews actual asset/recipe bindings, foreign preservation, current source8 and targeted published/native/UI/pixels before ordinary parent PR delivery.

## Policy and limits

AGENTS877–879 explicitly permits shipping an honest data/archetype half that needs geometry. Therefore an explicitly UNQUALIFIED/needs-bake source-half checkpoint is legitimate under the clarified owner protocol; never describe it as generated or gated. Stock dispatch has no unapplied-patch/artifact input, but no patch system is needed merely to enforce our earlier stricter handoff convention. AGENTS782–783 requires an owner-visible PR for workflow changes; none is needed for this zero-edit route.

Root must own the isolated feature, retain its draft parent, and leave its head still during baking. Concurrency is perref/cancel-in-progress; a second dispatch/push can cancel the first. Base liveness checks do not pin base HEAD or honor a ticket lap. Verify actual baseref SHA and output scope, retain reds, and do not infer a native pass from warranted-only success. Stock pushes content only after bake.sh/check.sh; failures before that can lose generated assets because mirror/branch upload is not unconditional. Its normal18-leg smoke may be expensive.

Avoid editing this workflow just to add a mode: its own push path triggers, and `bake_warranted` treats any change outside its warranted job as a bake before checking mesh freshness. A workflow-only feature push can thus launch a full town bake with blank only. The pure existing-function proof is saved separately; it performed no dispatch, file mutation or bake.
