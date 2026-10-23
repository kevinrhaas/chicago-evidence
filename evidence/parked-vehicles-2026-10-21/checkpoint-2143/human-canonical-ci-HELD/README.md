# One human canonical CI dispatch — staged qualification support

T-1789 support, 2026-10-21. **Prepared only. No final pushed head or dispatch release has been supplied. No GitHub mutation or dispatch was performed.** V2 is provisional; a later bounded collar/waistcoat successor may be included in the final source commit.

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

One call gathers one finite fresh snapshot. An in-progress run yields `PENDING` with actual job/step inventory. A later call uses another fresh output directory; no hidden polling, sleep loop or automatic retry. Terminal failure remains `NOT_QUALIFIED`; preserve it and report the failing actual job/step before any further action. Attempts other than 1 require root reconciliation, not silent replacement.

The helper verifies and preserves:

- Dispatch intent, both true inputs, unique discovered actual run, exact branch/head/event/workflow and attempt 1; exact remote ref; exact workflow hash; recipe/builder/fit/eye/export/normal/sole source blob hashes at that head.
- Actual required `humans` and `teamster-studies` jobs and all named substantive steps. No missing, skipped, failed or cancelled required step qualifies. Fixture byte verification and both viewport fixture/actor checks precede the authoring job.
- Body preparation, physical W01 seated preparation, all three canonical masters/portable exports, same-new-master hierarchy controls, declared animation bounds, hair container/runtime checks, actual container validation, warning-pointer controls, source and published inspections, seated actor/W01 checks, artifact preservation.
- Fresh attempt log ZIP retrieved directly by API, exact `resident-teamster-studies-FINAL_SHA` artifact metadata bound to the actual run/head/ref, fresh artifact ZIP and per-member hashes. ZIP members are read as inert data; nothing downloaded is executed or blindly extracted.
- Exact 3 residents × 4 LODs × 2 viewports for both source and published inspections (24 each), zero recorded page/request/check/GL failures, GLB-byte hashes matching inspection receipts, 12 desktop sole receipts per set with matching provenance, six published hierarchy/raw-frame comparisons, 24 container validations with zero errors and untruncated issue records. Warning inventories remain reviewable; none is silently waived.
- Six named seated runs with `sit_drive`, three refusal controls, closed browser/server, matching actual derivative hashes, and source/published W01 receipt success at both viewports.

The helper is prepared against the current source schemas. A refusal caused by a changed receipt schema is **not a CI failure** and does not permit weakening an input guard; preserve the actual files and review the source/schema distinction. API download/network errors likewise require GET reconciliation, never redispatch.

## Acceptance boundaries

Mechanical qualification does not establish photographic quality, correct collar/waistcoat fit or world acceptance. Read and view the newly acquired same-run images after the actual terminal artifacts exist, keeping the v2 collar gap and absent independent head/jaw clip motion visible unless a later source successor resolves them. No Blender, local browser, new model, workflow edit, old artifact promotion or gate weakening is part of this support handoff. The original source/normal 0.001 and sole 2 mm guards remain authoritative.

Preparation validation: both Python helpers compiled; dispatcher plan-only mode inspected; GET-only helper source has one constant HTTP GET call path and no mutation path. No network calls were needed to prepare this handoff. Full receipt qualification has not run because final SHA/release/run do not yet exist.
