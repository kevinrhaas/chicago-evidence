# Existing CI smoke plan

Twelve workflow dispatches cover every stage exactly once for each viewport. Mobile starts with1–4; the dirty local95-check pass is calibration only, not the final commit-bound coverage proof. No workflow edits. Each job has the existing150-minute limit. Desktop13 remains isolated: the standing record includes97m43s on an older tree; a later held-draws branch completed its smoke job in17m07s, but that historical source is not used as acceptance for this change.

Run only after source gates pass and the exact task commit is pushed. Capture a run ID after each dispatch before sending the next, and verify headSha equals the frozen commit.

```sh
source /tmp/t3654-runtime.sh
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=mobile -f stage=1-4
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=mobile -f stage=5-8
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=mobile -f stage=9-12
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=mobile -f stage=13
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=mobile -f stage=14-15
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=1-2
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=3-4
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=5-6
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=7-8
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=9-12
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=13
gh workflow run chicago-4d-smoke.yml --repo kevinrhaas/chicago --ref steward/t3654-1871-city-baseline -f viewport=desktop -f stage=14-15
```

For each completed run, from /workspace/chicago/chicago/4d:

```sh
gh run view RUN_ID --repo kevinrhaas/chicago --json headSha,headBranch,status,conclusion,createdAt,updatedAt,jobs,url > /tmp/t3654-ci-RUN_ID-meta.json
T3654_CI_LOG_MAP=/tmp/t3654-verified-ci-logs.json PATH="/tmp/t3654-gh-log-adapter:$PATH" node tools/dev-smoke-state.mjs ci RUN_ID
```

Before recording, obtain the actual job ID from run metadata and call the GitHub connector `mcp__codex_apps__github_fetch_workflow_job_logs({job_id: JOB_ID, repo_full_name: "kevinrhaas/chicago"})`. Save `structuredContent.content` verbatim as the run log. The verified-log map is keyed by run ID, each row `{ "path": "/tmp/t3654-ci-RUN_ID.log", "sha256": "<actual log digest>" }`.

The temporary adapter intercepts only the exact `gh run view RUN_ID --log` call and returns those hash-verified connector bytes. Every metadata call passes unchanged to `/usr/bin/gh`. Its capability check reproduced an old real log byte-for-byte and forwarded actual head metadata; no historical reading was inserted into ROOT. This avoids gh2.46’s empty display for the archive’s flat `0_smoke.txt` layout and direct artifact-host refusal.

`ci` uses GitHub metadata and labels the reading as CI with unavailable CI CPU/load values, but its tree hash is the current checkout. Record only with matching smoke inputs: current documentation-only checkpoint8d59 leaves those inputs unchanged from the actual tested commit ae259. The ledger records both the actual run SHA and recording checkout/input hash separately. Do not report a timeout/cancelled job as a pass. Do not infer a detailed page-error or check count from missing logs.

Actual local calibration: mobile1–2 with source work overlapped hit590s before full coverage, benchmark warm69ms; quiet mobile1 passed95checks/0errors in400s harness (402s wall), boot79.7s, warm-cache assertion<50ms. Corrected wrapper SHA: fc6196e6865b6e5f86ac262d50abbffc433d3ac0c3beaeaaf6703044542df4fa

Detailed ledger: /tmp/t3654-legacy-coverage-ledger.json. After source-only block, local1812 readiness/walk/canvas probe may run while the remote CI jobs execute.
