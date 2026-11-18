# Resuming T-3654 validation

Snapshot captured **2026-11-18 19:44:14 UTC**. Source checkout: `8d59e79cd657f58f483533246973e0e1c00ebf51`; existing legacy CI jobs test `ae259f9a5ddd4e79e1c82cd40e5084d6dcf42290`. Read `SNAPSHOT-STATUS.json` and the dated `*-partial.json` ledgers first. They preserve work in progress, not a complete-gate result. The CI snapshot records one completed group, three running and eight queued. That historical source snapshot records part 6/16 running. Later completed receipts now prove part 6 PASS and part 7 FAIL with four failed checks; consult `../checks/source-part6of16-receipt.json` and `../checks/source-part7of16-receipt.json` before using the older snapshot. The fallback paused after the part 7 failure.

The helpers retain their original absolute `/workspace` and `/tmp` paths. Restore or deliberately adjust those paths in the resumed environment. Select **Node 22**, restore the project's documented reader dependencies, and keep `C4D_GATE_REQUIRE_READERS=1` for source checks. These are setup requirements; no credential store, authentication configuration, or environment dump is included.

| File | Role |
| --- | --- |
| `dispatch-smoke.py` | Original dispatcher with exact local/remote SHA checks and existing-run reconciliation. Every planned group already has a run ID; inspect those runs before considering any new dispatch. |
| `ci-smoke-plan.md` | Historical procedure and group layout. Its dispatch command block is a record, not a queue to replay. |
| `gh-log-adapter/gh` | Narrow adapter for the exact `gh run view RUN_ID --log` call. All metadata requests pass unchanged to the real `/usr/bin/gh`. |
| `source-fallback-ledger.py` | Original partition bookkeeping and terminal-log recovery helper, retained as executed for earlier calls. |
| `source-fallback-ledger-process-receipts.py` | Subsequent executed version: validates the foreground process sidecar, uses its actual exit code/timestamps, and writes an immutable per-attempt receipt. It does not execute the source gate. |
| Dated `legacy-coverage-ledger-*-partial.json` | Existing run IDs, actual tested SHA, latest statuses, input binding and calibration exclusions. |
| Dated `source-fallback-summary-*-partial.json` | Partition declarations, completed receipts, remaining ordinals, and the active part 6 start record. Earlier-source receipts remain explicitly distinguished from current-HEAD coverage. |

Use existing run IDs to fetch current GitHub metadata, including `headSha`, status, conclusion and actual job IDs. Preserve that metadata beside the log. Obtain actual completed job logs through the GitHub connector when the CLI's archive handling cannot read them. Before adding a `T3654_CI_LOG_MAP` entry, bind the actual job to the intended run and SHA, save its bytes verbatim, and calculate their SHA256. The adapter checks byte integrity; the metadata establishes provenance. Record through `tools/dev-smoke-state.mjs ci RUN_ID` only when smoke inputs match, retaining the actual tested SHA separately from the recording checkout. Missing, cancelled, timed-out or incomplete logs supply no passing counts.

The archived first completed CI proof is `../ci/44375691729-mobile-1-4.log` plus its real metadata: 323 checks, zero failures/page errors, four of the required 30 stage/viewport cells. It does not prove the remaining groups.

Source part 5 has a complete matching terminal PASS for 89 steps, including 20 self-tests, on unchanged clean 8d59. A transient reconnect lost the process result: its receipt deliberately keeps `exit_code: null`, status `pass_from_terminal_log`, and approximate 544.875-second duration derived from start time and final log modification time. Preserve those qualifiers. Before resuming an active ledger entry, inspect whether its process still exists and reconcile any complete terminal result. For future foreground invocations, immediately persist the actual timeout-process return code and start/end timestamps to an atomic sidecar, alongside the log, so a reconnect cannot erase that receipt. Never infer an exit code from a recovered terminal line.

The part 7 `.process.json` and receipt demonstrate durable result capture: exit 1 and nanosecond start/end timestamps survive independently of the tool session. Use the sidecar’s actual return code with the helper’s `finish` mode; the older `recover-log` path represents cases where no process result survived. Keep failed invocations as failures while repairs and reruns proceed.
