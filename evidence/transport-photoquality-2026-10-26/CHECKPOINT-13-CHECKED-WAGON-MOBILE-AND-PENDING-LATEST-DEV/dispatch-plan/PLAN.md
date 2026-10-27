Prepared commands only; no workflow has been dispatched by this checkpoint.

The source contract requires foreground native source checks before a checked commit and the complete published renderer gate at both 390x780 and 1280x800 before merge. The main/runtime/texture and wagon asset changes select all fifteen smoke parts. The retained actual native coverage report records that selection. A historical green run for a966 is not qualification of the pending 6c composition or its future checked HEAD.

Use the fresh checked/pushed feature HEAD after the current intake, supported owner, publisher, complete preflight, new-HEAD changelog/ID/history questions and remote equality close. Root must authorize the concrete SHA before the prepared shell file is executed. Keep this branch frozen through dispatch and verification. The script rejects old a966 and the accepted-base commit itself, checks both remote branch and PR head equality, and checks exact native workflow bytes on the new commit. A branch race after a check remains possible: reject any resulting run whose head_sha differs from the authorized SHA; do not count it.

The immutable 4220 workflow reads are current-policy evidence. The saved 4220-to-6c GitHub comparison changes none of these workflows, the instruction files, smoke_budget or dev-smoke-state. The no-lazy local 6c read attempted during preparation had not yet hydrated the commit, so no local fallback/fetch or assumption of a future composed workflow is hidden here. Runtime guards read the actual future checked SHA through GitHub and fail if workflow bytes differ.

Native dispatch inputs are exactly viewport and stage. Reuse the bake's current nine disjoint ranges: 1-2, 3-4, 5, 6-7, 8, 9-12, 13, 14, 15. They tile 1..15 exactly once per viewport; 18 manual invocations cover 30 viewport/part cells exactly once. Each manual workflow job has its own existing 150-minute ceiling, publishes its own mirror, and calls node tools/smoke_renderer.mjs --published. The nightly bake's separate 40-minute per-leg cap does not apply to these manual invocations. No workflow edit, ceiling change or single combined 150-minute two-viewport job is proposed.

Native budget output is retained in ACTUAL-NATIVE-READONLY-BUDGET-LEGS.log. It was obtained by the unmodified native metadata CLI on immutable source copies, without any smoke/browser/test invocation. Many ranges are unmeasured; zero seconds for those is not a measurement. Existing grouped readings can overprice a range that shares a reading with its neighbor. No duration guarantee follows. The smoke workflow also records the historical desktop part13 ~85-minute observation; its 150-minute timeout is why it is split into a dedicated hosted job.

Before dispatch, retain the UTC start and current run-ID sets externally:

```bash
gh run list --repo kevinrhaas/chicago --workflow chicago-4d-frame-time.yml --event workflow_dispatch --branch steward/t2793-wagon-photoquality-20261026 --commit "$T3173_CHECKED_HEAD" --limit 100 --json databaseId,headSha,event,createdAt,status,conclusion,url
gh run list --repo kevinrhaas/chicago --workflow chicago-4d-smoke.yml --event workflow_dispatch --branch steward/t2793-wagon-photoquality-20261026 --commit "$T3173_CHECKED_HEAD" --limit 100 --json databaseId,headSha,event,createdAt,status,conclusion,url
```

Record each returned fresh run ID in the dispatch ledger. gh workflow run submission output alone does not prove a run ID, inputs, completion or success. If interrupted or rate-limited, stop and reconcile the existing ledger and fresh run IDs before any additional submission; never blindly repeat the loop. No gh run rerun command is proposed.

For every candidate ID, retain native run metadata, all jobs, and the actual final log:

```bash
gh api "repos/kevinrhaas/chicago/actions/runs/$run_id"
gh api --paginate "repos/kevinrhaas/chicago/actions/runs/$run_id/jobs?per_page=100"
gh run view "$run_id" --repo kevinrhaas/chicago --log > "$external_log_path"
```

Verify the exact fresh SHA, event workflow_dispatch, correct workflow path, run_attempt1, completed/success and no cancelled/skipped required job. For smoke, map the job's actual SMOKE_VIEWPORT/SMOKE_STAGE environment plus log banners NOT THE FULL GATE - viewports filtered to "..." and stages filtered to "..." of15 to exactly one row in EXPECTED-SMOKE-COVERAGE.json. Verify the executed published-mirror command, the stage's actual final zero-failure verdict and no page errors. Every smoke invocation correctly says it is not the full gate; only the verified union of all18 disjoint rows qualifies the complete published two-viewport smoke. Do not infer inputs from dispatch order or a workflow's generic job name. If any run is missing, ambiguous, timed out, cancelled or red, coverage is incomplete and needs root's next decision.

The frame-time dispatch has no inputs and requires all9 native matrix jobs: two still-frame viewports; memory1812/1835/1904 at both widths; and memory1835 self-test. Require every expected job completed/success, the same fresh SHA and final native artifact readings tied to that run. The memory self-test's deliberate negative is valid only through its successful final self-test verdict. Retain exact artifact identity/digest and inspect emitted JSON if used to report numeric claims; workflow success alone is not an invented numeric reading. a966's run40421012712 is historical evidence only.

Desktop detail/return/context lifecycle remains a separate unrun proof, and successful hosted submissions do not close it. Root retains PR ready/merge/ticket/DEV authority.
