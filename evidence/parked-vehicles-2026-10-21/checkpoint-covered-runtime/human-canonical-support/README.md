# One human canonical CI dispatch — staged qualification support

T-1789 support, 2026-10-21. **HELD. No final pushed head or dispatch release has been supplied. No GitHub mutation or dispatch was performed.** Expected final runtime source is now **V4**, including the V3 shared collar/waistcoat successor and V4 measured shoulder ease field. Root reports both observed shoulder holes gone in the one actual V4 preview. All **40 inherited idle0 negative source-face projections remain OPEN**; source-array/runtime previews do not qualify canonical exports, complete cloth fit or photographic quality.

`V4-SOURCE-BINDING.json` records exact expected recipe/builder/fit/eye hashes, unchanged source dependencies, the observed nine-file staged set and the pinned source/peer/actual-preview evidence. These are expected source bytes, **not a final commit or dispatch authorization**. After root supplies its final committed/pushed SHA, check that its four runtime inputs equal these V4 pins. The support refresh changes README/source-binding/audit records only; dispatcher and qualifier program bytes remain unchanged.

Repository `kevinrhaas/chicago`; branch `steward/1835-workwear-repair-20261021`; workflow `.github/workflows/chicago-4d-humans.yml`. Current reviewed workflow bytes: SHA-256 `62048edeed40b6d5fe8c42feec1a031b7b2581a39ec7215ce0a20b170769c847`, saved as `workflow-reviewed-source.yml`. Final remote bytes must match this hash; otherwise inspect the actual changed workflow before adapting anything. No workflow edits are proposed.

## Dispatch handoff

Root owns the single dispatch unless it explicitly delegates ownership. `dispatch_once.py` reuses the existing `/workspace/shared/dispatch_human_seated_qualification.py` pattern, changing only the branch. Its `PINNED_WORKFLOW_SHA256` intentionally remains **None**, so `--dispatch` refuses before any network request. Plan-only mode needs no release or network:

```bash
python /workspace/shared/human-canonical-qualification-20261021/dispatch_once.py --sha FINAL_FULL_40_HEX_SHA --out /workspace/shared/human-canonical-dispatch-FINAL_SHA.json
```

After root provides the final committed/pushed exact SHA **and explicitly releases this one dispatch**, freeze the reviewed workflow hash in the dispatcher, rehash it, and use its `--dispatch` option once. The helper rechecks remote head, retrieves workflow bytes at the exact SHA, writes an exclusive intent receipt before POST, sends **both** `build_teamsters=true` and `build_seated_driver_study=true`, and discovers exactly one new matching workflow_dispatch run. An ambiguous POST, run ambiguity or head movement means **reconcile by GET; never repeat POST blindly**. Do not use the older probe helper: it sends only `build_teamsters` and cannot establish seated coverage.

The workflow has `cancel-in-progress: true` per ref. Once dispatched, do not move/push this branch until root reconciles the terminal evidence; a second run on that ref can cancel the intended run. Ordinary PR CI may verify fixtures while teamster studies are skipped. Such a green badge is not this manual canonical qualification.

## Read-only qualification

`qualify_get_only.py` has a constant GET HTTP method and no dispatch, rerun, merge or upload path. Use the single actual run ID in the dispatch receipt, the final exact SHA, and a **fresh** receipt directory:

```bash
python /workspace/shared/human-canonical-qualification-20261021/qualify_get_only.py --sha FINAL_FULL_40_HEX_SHA --run-id ACTUAL_RUN_ID --dispatch-receipt /workspace/shared/human-canonical-dispatch-FINAL_SHA.json --out /workspace/shared/human-canonical-qualification-ACTUAL_RUN_ID-snapshot1
```

One call gathers one finite fresh snapshot. Prefer the qualifier after the selected run is terminal. If both required jobs already exist, an in-progress run yields `PENDING` with actual inventory. If GitHub has not yet materialized the dependent teamster job, this version refuses a missing job before the pending-status return; that is a local snapshot limitation, not proof of CI failure. Use a fresh later snapshot and GET reconciliation, never another dispatch. There is no hidden polling, sleep loop or automatic retry. Attempts other than 1 require root reconciliation, not silent replacement.

On a failed terminal run this version saves actual run/jobs and returns `NOT_QUALIFIED` before downloading log/artifact ZIPs. Preserve those files, then collect failure logs/artifact metadata with GET (or the existing read-only `watch_human_ci.py`); do not claim failure diagnostics were downloaded by this qualifier. A fresh direct failure-log command is `gh api --method GET repos/kevinrhaas/chicago/actions/runs/ACTUAL_RUN_ID/attempts/1/logs`, redirecting binary output into a fresh shared file. No helper logic or CI input guard was changed during the V4 binding refresh.

The helper verifies and preserves:

- Dispatch intent, both true inputs, unique discovered actual run, exact branch/head/event/workflow and attempt 1; exact remote ref; exact workflow hash; recipe/builder/fit/eye/export/normal/sole source blob hashes at that head.
- Actual required `humans` and `teamster-studies` jobs and all named substantive steps. No missing, skipped, failed or cancelled required step qualifies. Fixture byte verification and both viewport fixture/actor checks precede the authoring job.
- Body preparation, physical W01 seated preparation, all three canonical masters/portable exports, same-new-master hierarchy controls, declared animation bounds, hair container/runtime checks, actual container validation, warning-pointer controls, source and published inspections, seated actor/W01 checks, artifact preservation.
- Fresh attempt log ZIP retrieved directly by API, exact `resident-teamster-studies-FINAL_SHA` artifact metadata bound to the actual run/head/ref, fresh artifact ZIP and per-member hashes. ZIP members are read as inert data; nothing downloaded is executed or blindly extracted.
- Exact 3 residents × 4 LODs × 2 viewports for both source and published inspections (24 each), zero recorded page/request/check/GL failures, GLB-byte hashes matching inspection receipts, 12 desktop sole receipts per set with matching provenance, six published hierarchy/raw-frame comparisons, 24 container validations with zero errors and untruncated issue records. Warning inventories remain reviewable; none is silently waived.
- Six named seated runs with `sit_drive`, three refusal controls, closed browser/server, matching actual derivative hashes, and source/published W01 receipt success at both viewports.

The helper is prepared against the current source schemas. A refusal caused by a changed receipt schema is **not a CI failure** and does not permit weakening an input guard; preserve the actual files and review the source/schema distinction. API download/network errors likewise require GET reconciliation, never redispatch.

## Acceptance boundaries

Mechanical qualification does not establish photographic quality, complete collar/waistcoat fit or world acceptance. Read and view the newly acquired same-run images after the actual terminal artifacts exist. V3 replaces the V2 separate ellipse with a genuinely shared source seam; V4 resolves the two observed shoulder-ray holes in the actual preview. Post-decimation/canonical behavior, independent head/jaw movement and the 40 inherited negative face projections remain unresolved unless actual new evidence addresses them. No Blender, local browser, new model, workflow edit, old artifact promotion or gate weakening is part of this support handoff. The original source/normal 0.001 and sole 2 mm guards remain authoritative.

Preparation validation: both Python helpers compiled; dispatcher plan-only mode inspected; GET-only helper source has one constant HTTP GET call path and no mutation path. The V4 refresh rechecked identical workflow bytes/hash, both inputs, the disabled dispatcher pin, one-POST intent/discovery safeguards, and current success-receipt source schemas. Known pending/failed-run evidence limitations are stated above. No network calls were needed. Full receipt qualification has not run because final SHA/release/run do not yet exist.
