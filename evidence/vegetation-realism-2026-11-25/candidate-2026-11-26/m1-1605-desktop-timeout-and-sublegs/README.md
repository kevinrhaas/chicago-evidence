# Exact1605 desktop body: cancelled without a final verdict; full coverage re-run

The core's broad desktop run45944011105/job140324466997 concluded cancelled at the stock150-minute job limit. Its last assertion at06:48:16UTC was the documented-wall-height check at the end of part4; no result from part5's complete detail sweep appeared before cancellation at08:17. This identifies a long silent sweep, not its cause. No failed assertion was reported, but the viewport never reached its final zero-page-error check or complete success footer. NONE of its partial positive assertions qualifies any gate coverage.

All14previously unqualified desktop parts were re-dispatched, with identical app1605, workflow, source, assertions, dimensions, scene density, draw/triangle/frame/memory limits and150-minute job cap:

- Parts1–4: run45964918139.
- Part5alone: run45964921408.
- Parts6–10: run45964924873.
- Parts11–12and14–15: run45964928360.

These are existing stock SMOKE_STAGE inputs, no workflow or app edit. Each replacement must complete its own final page-error check and full success footer. All4are queued when this folder is recorded; no result is claimed for them. The independent stock stages support fresh contexts. The source fixture and production renderer remain unchanged.

Six other exact-head workflows remain successful: full Native (all8parts and aggregate), portable humans, moving/upload-release, the15-case standard frame/memory grid, phoneALL15 and desktop13. The actual phone raw log has746passes/0failures and zero page errors; desktop13has158passes/0failures and zero page errors. Both are positive controls for the strict log verifier. The same verifier rejects the actual cancelled body for its missing final page-error check. These controls and raw logs are retained here.

Ten actual final workloads must pass: the six unaffected workflows plus all4replacement desktop bodies. The original cancelled body is explicitly excluded and preserved, not relabelled as a pass. The active calibrated timing concern, exact source/upstream composition, reviews, raw clean merge state and live owned lap are separate requirements. This folder claims no merge or performance pass. No heap snapshot is included.
