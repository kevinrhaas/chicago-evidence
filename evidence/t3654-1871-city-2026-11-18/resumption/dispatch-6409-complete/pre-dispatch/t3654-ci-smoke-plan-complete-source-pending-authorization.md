# Existing CI smoke plan

Current frozen commit: `6409dda1222e1284e111ab0efde1c471f3284d60`, incorporating dev `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`. Its runtime-input hash is `sha256:be6a6a9e5ee3c3e2`, confirmed by the clean publication receipt `/tmp/t3654-6409-publication-receipt.json`. Fresh dispatches require complete source assertion coverage on this exact tree. This may be the full hosted gate in run `44421763389`, or the separately verified union of successful current-tree local and hosted native partitions. The full hosted eight-part gate and aggregate must still pass before merge; the canonical hosted summary is never promoted by a local/hosted union. All previous head results are historical and carry zero current source/browser coverage. In particular, the complete 871698 assertion union is dated evidence, while its hosted gate had seven passes and an actual part 6 timeout; its obsolete aggregate was administratively cancelled.

Twelve workflow dispatches cover every stage exactly once for each viewport. Mobile starts with 1–4; the dirty local 95-check pass is calibration only, not the final commit-bound coverage proof. No workflow edits. Each job has the existing 150-minute limit. Desktop 13 remains isolated: the standing record includes 97m43s on an older tree; a later held-draws branch completed its smoke job in 17m07s, but that historical source is not used as acceptance for this change.

Run only after one of those complete exact-tree source proofs passes, the exact task commit is pushed, and root has reviewed the prepared proof/helper for the first batch. The reviewed verifier `/tmp/t3654-pre-browser-source-coverage-strict-reviewed.py --bindings EXACT_CURRENT_BINDING --require-complete` rechecks original logs, process exits and timing, semantic reader/base prerequisites, declaration ordinals and Git tree identity each time; a stale ready boolean cannot authorize dispatch. Its pinned SHA is `accc8728fb6e35995f52b910c5bad86a1a1b8617dbe74cf7e5409800591a1b07`. The final complete current binding `/tmp/t3654-pre-browser-bindings-6409-h1-2-4-5-6-l3of16-6of16-7of16-8of16-11of16-15of16-16of16-strict.json` contains only fresh hosted 1/8+2/8+4/8+5/8+6/8 and local 3/16+6/16+7/16+8/16+11/16+15/16+16/16: all1379/1379 declarations; the immutable initial binding began with zero inherited coverage. Its reviewed artifact inputs are SHA-pinned; the dispatcher pins binding SHA `bf8ef18eb2cec4eb68fa97240d8aa9c277b042334a2cce2f4c681fc4198ed33a`. The reviewed verifier now confirms complete current source assertion coverage with zero missing and no exceptions. Root first-batch authorization and ledger holds remain pending; the canonical hosted gate remains incomplete until its remaining three parts and aggregate pass. Preserve a run ID after each dispatch before sending the next, and verify headSha equals the frozen commit.

Before dispatch, intentionally reconcile the 12 unassigned ledger rows from `not_dispatched` to `pending_dispatch` once. Use the guarded helper instead of issuing independent commands:

```sh
source /tmp/t3654-runtime.sh
python3 /tmp/t3654-dispatch-smoke.py 6409dda1222e1284e111ab0efde1c471f3284d60
```

The helper has no checkpoint bypass. It requires either eight verified hosted source jobs plus a successful aggregate, or a freshly verified complete 1–1379 ordinal union on the identical committed tree. Both routes require exact repository/PR/run/head/base identity, unchanged declarations, no dispatch hold, a clean tracked checkout, matching local/remote heads, unchanged live dev, and fresh live source-job metadata. The union route preserves `hosted_gate_required_before_merge:true`; no timeout exception from the superseded 871698 run applies to 6409. Any current source failure or cancellation requires review. It records each new run ID before dispatching the next group. Reconcile any ambiguous or interrupted dispatch against its saved prior IDs; never retry blindly.

| Viewport | Stage groups |
| --- | --- |
| Mobile | 1–4; 5–8; 9–12; 13; 14–15 |
| Desktop | 1–2; 3–4; 5–6; 7–8; 9–12; 13; 14–15 |

For each completed run, from /workspace/chicago/chicago/4d:

```sh
gh run view RUN_ID --repo kevinrhaas/chicago --json headSha,headBranch,status,conclusion,createdAt,updatedAt,jobs,url > /tmp/t3654-ci-RUN_ID-meta.json
T3654_CI_LOG_MAP=/tmp/t3654-verified-ci-logs.json PATH="/tmp/t3654-gh-log-adapter:$PATH" node tools/dev-smoke-state.mjs ci RUN_ID
```

Before recording, obtain the actual job ID from run metadata and call the GitHub connector `mcp__codex_apps__github_fetch_workflow_job_logs({job_id: JOB_ID, repo_full_name: "kevinrhaas/chicago"})`. Save `structuredContent.content` verbatim as the run log. The verified-log map is keyed by run ID, each row `{ "path": "/tmp/t3654-ci-RUN_ID.log", "sha256": "<actual log digest>" }`.

The temporary adapter intercepts only the exact `gh run view RUN_ID --log` call and returns those hash-verified connector bytes. Every metadata call passes unchanged to `/usr/bin/gh`. Its capability check reproduced an old real log byte-for-byte and forwarded actual head metadata; no historical reading was inserted into ROOT. This avoids gh 2.46’s empty display for the archive’s flat `0_smoke.txt` layout and direct artifact-host refusal.

`ci` uses GitHub metadata and labels the reading as CI with unavailable CI CPU/load values, but its tree hash is the current checkout. Record only with matching smoke inputs and the actual corrected tested commit; read the current ledger for that exact SHA. The ledger records both the actual run SHA and recording checkout/input hash separately. Root receipt writes wait for a safe boundary with source checks. Do not report a timeout/cancelled job as a pass. Do not infer a detailed page-error or check count from missing logs.

Actual local calibration: mobile 1–2 with source work overlapped hit 590s before full coverage, benchmark warm 69ms; quiet mobile 1 passed 95 checks / 0 page errors in 400s harness (402s wall), boot 79.7s, warm-cache assertion <50ms. Corrected wrapper SHA: fc6196e6865b6e5f86ac262d50abbffc433d3ac0c3beaeaaf6703044542df4fa

Detailed ledger: /tmp/t3654-legacy-coverage-ledger.json. The focused 1812 readiness/walk/canvas probe already passed both widths on the ae259 published snapshot and is archived as dated evidence; it is not full legacy coverage.
