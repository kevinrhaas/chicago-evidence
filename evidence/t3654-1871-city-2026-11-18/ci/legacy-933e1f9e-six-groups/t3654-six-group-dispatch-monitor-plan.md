# Six-group smoke plan for the integrated checkpoint

Status: prepared only. No new commit is bound and no dispatch is authorized.

Use the unchanged `chicago-4d-smoke.yml` workflow and its 150-minute job limit. Dispatch in this order after root supplies and explicitly authorizes the clean pushed integrated commit:

| Order | Viewport | Stages | Historical harness basis + 15-minute setup allowance |
| --- | --- | --- | --- |
| 1 | desktop | 13 | 112m43s |
| 2 | desktop | 1–8 | 105m09s |
| 3 | mobile | 1–12 | 51m17s |
| 4 | mobile | 13–15 | 54m42s |
| 5 | desktop | 9–12 | 55m50s |
| 6 | desktop | 14–15 | 52m57s |

The exact readings, source identities and 30-cell uniqueness proof are in `/tmp/t3654-proposed-six-smoke-groups.json`. These are planning estimates, not promises about the next runner. Desktop13 remains isolated and first. There are six publishes and six boots instead of twelve; all existing assertions remain.

The new immutable authorization record will identify the actual repository, branch, commit, tree, included dev base, runtime-input hash, and root-approved focused integration/publication receipts by path and SHA-256. Bind these only when root provides the completed checkpoint. Do not inherit any 6409 source or browser credit. Keep the historical ledger and cancellation manifest frozen.

Before dispatch, verify the exact local and remote task heads, clean tracked checkout, included dev base, and the focused receipt hashes. Root's explicit authorization for that exact commit is required. Full hosted source coverage is not a dispatch prerequisite: source and browser jobs may run concurrently after focused checks. Full hosted source success and all30 fresh browser cells remain required before merge.

Use one small dispatch helper with the existing atomic-ID pattern: create a fresh six-row ledger; save `dispatching` and the preceding workflow IDs before each API mutation; record the uniquely identified new run and exact head before proceeding to the next row. If an invocation is interrupted or the new run identity is ambiguous, stop for reconciliation instead of repeating it. No workflow modifications, new threshold, or source-union machinery is needed.

Monitor only the six bound run IDs with one read-only watcher. For every completed run, save final metadata and decoded native logs; verify actual checkout, published mirror, correct stage range and viewport, zero failures/page errors, and `SMOKE PASS` before crediting its cells. Record failures and cancellations as such. Keep ROOT receipt writes on hold until root explicitly releases that boundary, and never import an old run under the new checkout's runtime hash. Source CI may be monitored separately; its full green result remains an independent merge requirement.

No fresh dispatch has occurred. The prior 6409 batch ended with three mobile successes (468 checks, 12 cells) and nine explicitly authorized ordinary cancellations; it is dated evidence only.
