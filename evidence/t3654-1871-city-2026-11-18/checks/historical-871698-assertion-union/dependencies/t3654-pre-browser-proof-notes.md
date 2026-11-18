# Temporary native-source coverage auditor

This is an independent browser-sequencing proof, not a GitHub check or merge authorization. It never changes the canonical hosted gate. Complete hosted source parts and aggregate, browser checks, and other repository merge requirements remain mandatory before merging.

## Frozen historical result

The actual audited source head is `871698ae94659100fcb8894f4967d4b15c62150f`, tree `8a4cf0055119d8dcf4b5bc813590abaf5231944d`, integrated dev base `169404c9f99d2defeca2b05f2364c868a4f4e745`. The hosted checkout `bd8bbfdff8f2575f1d7437be255f6617509ce6fc` has the exact same tree and parents `[base, head]`.

All 1,379 native declarations are covered by successful actual executions: 1,376 ordinary assertions and prerequisites 319, 320, 321. Seven hosted parts passed; hosted part 6/8 timed out and contributes zero coverage. Successful current local 6/16 and 14/16 executions cover its missing ordinary assertions. Other accepted local executions are retained as overlapping evidence and counted once.

The complete frozen proof is `/tmp/t3654-source-assertion-union-871698-bound-complete-dated.json` (SHA256 `d5c80a8fa71745811071fb1e9c7d103555cbf4ba01092c7cd338ae6f8ba4c636`). It records `source_check_coverage_complete: true`, `ready_for_browser_queue: false`, and blocker `live_dev_base_changed`, because live dev was `c26d33718ecb68cbed172d8b549cce720af71b56`. The actual `--require-complete` command exited 1. No browser run was dispatched. This remains dated evidence after the combined-head integration.

The earlier pre-binding proof and matching archived verifier are preserved as `/tmp/t3654-source-assertion-union-871698-complete-dated.json` and `/tmp/t3654-pre-browser-source-coverage-871698-original.py`.

## Reviewed inputs and invocation

```sh
python3 /tmp/t3654-pre-browser-source-coverage.py \
  --bindings /tmp/t3654-pre-browser-bindings-871698.json \
  --require-complete
```

Exit 0 with `--require-complete` requires complete coverage, successful actual PR-only checks, clean exact local source/base/tree, and exact live branch/dev identities. Exit 1 means valid incomplete or live-identity-blocked evidence; exit 2 means rejected source/evidence. A refusal clears the active output's ready flag once bindings have been loaded. Consumers must always honor the process exit and freshly written report, never a previously cached boolean.

Bindings pin one exact head/tree/base/run, all three native harness files, declaration count and prerequisites, accepted local receipt hashes, accepted hosted metadata hashes, and the independently recorded hosted log index hash. Local log/process receipts and qualified kernel bundles are checked recursively. Hosted log SHA, checkout, reader/base requirements, native verdict/headings, successful gate step, and exact base/head changelog command are verified. Unknown completed failures/cancellations in the bound hosted index are refused. Original timeout exclusions are explicit, hash-bound, and give no assertion credit.

The only special local exit is the documented 6/16 attempt 2 process whose original timing sidecar was lost during reconnect. Its explicit approved bundle ties the actual GNU timeout PID, Linux zombie wait status 0, original stdout inode, unchanged gate command, original wrapper, restored transcript and receipt together. Its wall duration is approximate. No other alternate exit is implicitly allowed.

Repeated evidence is counted as a set of declaration ordinals. No summed part counts, old-head evidence, terminal-log-only verdict, running job, timeout, or original failed run is credited. The tool rechecks source and bound artifacts at the end of the audit.

## New source binding

A new source head needs a new explicit binding file, with that source's exact tree, integrated base, actual hosted merge checkout, run identity, harness hashes and prerequisite layout. Start `accepted_local_receipts`, `accepted_hosted_metadata`, `qualified_local_exits`, and `excluded_hosted_timeouts` empty, and bind a new empty evidence index with matching identity. Add only newly verified exact-head evidence. The verifier deliberately grants no implicit cross-head credit, even when source declaration hashes match. An independently reviewed tree-equivalence mechanism would need its own explicit evidence; none is automatically inherited here.

The dispatcher must pin both helper and binding SHA256, run the verifier immediately before queueing, check the fresh complete exhaustive ordinal array and source identity, and independently fetch live workflow run/job metadata to reject any new unknown failure/cancellation or changed run. The helper's frozen hosted evidence index is not a substitute for that live API check. Owner review and explicit queue authorization remain outside this tool.

## Validation

`/tmp/t3654-test-pre-browser-source-coverage.py` has 26 passing focused positive/refusal tests; transcript `/tmp/t3654-pre-browser-refusal-tests.log`. Tests use synthetic mutations or read-only copies and do not create check verdicts. They cover actual local/hosted/kernel positives, wrong and dirty source, hashes, exit status, kernel raw status/PID/inode, declaration headings/terminal verdict/self-test counts, PR-only and dependency requirements, missing coverage, overlap accounting, old-head exclusion, empty new-head bindings, live identity changes, unknown hosted failures/cancellations, and stale ready output refusal.

No application, workflow, canonical hosted guard, or merge requirement was modified.
