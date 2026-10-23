# Outside-app split smoke coverage validator

Files:

- `validate_transport_split_smoke.py`: Python stdlib CLI; only invokes read-only GitHub API and `gh run view --log`. It never dispatches, edits a repository, publishes a mirror, merges, or mutates the smoke ledger.
- `transport-split-smoke-manifest.template.json`: exactly eighteen expected cells. Replace SHA and null IDs only AFTER dispatch authorization and actual run IDs exist. Each selected attempt is explicit.
- `test_transport_split_smoke_validator.py`: twelve local tests, including acceptance of a complete synthetic matrix and rejection of wrong SHA, cancellation, missing cells/guards/tail, false green footer, and audit count mismatches. Also verifies the real 1b3c73d frozen source topology using read-only git show.

Run after all eighteen selected runs finish:

```bash
python3 /workspace/shared/validate_transport_split_smoke.py \
  /workspace/shared/transport-split-smoke-manifest.json \
  --out /workspace/shared/transport-split-smoke-evidence-FROZEN_SHA \
  --workers 3
```

The output directory must be fresh/empty. The tool fetches source blobs at the manifest's exact commit through GitHub, validates the source's 15 stage-work blocks, unchanged counter contract, reviewed always-on guard literals, manual workflow inputs and bake matrix. It then verifies each selected run's actual SHA, explicit attempt, event and workflow path. Successful metadata alone is insufficient: all logs must prove one requested viewport/range, published mode, terminal SMOKE PASS, completed body, zero page errors, all thirteen reviewed guards exactly once, zero untagged failures, audit arithmetic and complete section counts.

It writes ordinary downloaded logs, manifest.json, and aggregate.json outside the checkout. Each log is hashed; aggregate includes source Git blob IDs/SHA256 values, complete assertion lines, per-viewport section inventory/totals, repeated always-on counts and the logical unique guard total. No existing evidence is overwritten.

The two distinct results are:

1. `workflow_successes_at_sha`: completed successful selected workflows at the required head/event/path/attempt.
2. `coverage_proof_passed`: additionally requires all source topology/log/guard/count checks and eighteen unique grid cells whose ranges tile parts1..15 exactly once PER viewport.

Thus eighteen green workflows can still produce `coverage_proof_passed: false`. Exit0 requires the coverage proof; exit1 means coverage was not proven (receipt saved); exit2 means manifest/output/initial validation could not proceed. Unknown or changed source/guard contracts fail closed for review.

No new unfiltered pass is claimed. If a completed unfiltered count at the SAME SHA exists, optionally provide `expected_section_totals: {"mobile": N, "desktop": M}` in the manifest; each value must come from that head's actual complete log, not an old/cancelled reading. Without it, the receipt explicitly says same-head unfiltered numeric comparison unavailable; proof is the repository's existing structural split-gate contract plus executed section/guard evidence. No old 668-section mobile count is assumed.

This validator does not validate the PR gate/preflight, review/merge policy, or subjective visual quality. Root must separately verify required checks at the same final head and decide whether to mark ready/merge. Every individual workflow remains a PARTIAL leg; only the accepted union establishes split full coverage.

Test:

```bash
python3 /workspace/shared/test_transport_split_smoke_validator.py -v
```

No real runs have been dispatched or certified by preparing these tools.
