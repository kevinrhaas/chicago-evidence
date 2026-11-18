# Existing CI smoke plan

Current frozen commit: `871698ae94659100fcb8894f4967d4b15c62150f` (combined upstream roof/changelog integration, context source-use, empty-boot, trace summation and seven measured isolation-row repairs). Its runtime-input hash is `sha256:7e62e06ff2c268dd`, confirmed in `/tmp/t3654-871698-runtime-hash.log`. Fresh dispatches wait until all eight source parts and the aggregate pass on this exact commit in run `44407494538`. Prior ae259 runs are retired: four historical passes and eight cancellations; none count for this tree.

Twelve workflow dispatches cover every stage exactly once for each viewport. Mobile starts with 1–4; the dirty local 95-check pass is calibration only, not the final commit-bound coverage proof. No workflow edits. Each job has the existing 150-minute limit. Desktop 13 remains isolated: the standing record includes 97m43s on an older tree; a later held-draws branch completed its smoke job in 17m07s, but that historical source is not used as acceptance for this change.

Run only after source gates pass and the exact task commit is pushed. Capture a run ID after each dispatch before sending the next, and verify headSha equals the frozen commit.

Before dispatch, intentionally reconcile the 12 unassigned ledger rows from `not_dispatched` to `pending_dispatch` once. Use the guarded helper instead of issuing independent commands:

```sh
source /tmp/t3654-runtime.sh
python3 /tmp/t3654-dispatch-smoke.py 871698ae94659100fcb8894f4967d4b15c62150f
```

The helper has no checkpoint bypass. It requires literal true completeness for the requested commit, the expected repository/PR/run identity, eight distinct verified source jobs, a successful aggregate, no dispatch hold, matching live GitHub metadata, and matching local and remote heads, a clean tracked checkout, and the unchanged verified dev base. It records each new run ID before dispatching the next group. Reconcile any ambiguous or interrupted dispatch against its saved prior IDs; never retry blindly.

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
