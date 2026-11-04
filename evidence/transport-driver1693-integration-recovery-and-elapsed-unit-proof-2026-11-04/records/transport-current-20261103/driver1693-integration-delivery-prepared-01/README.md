Prepared only; do not execute without ROOT review and explicit GO.

The JSON template has `template_only: true`,
`ROOT_EXPLICIT_INTEGRATION_DELIVERY_GO: false`, and an unset final four-part
receipt hash. ROOT must review the source/execution pins, wait for the actual
`actual-driver1693-dev-b622-fourpart-01/CLOSED.json` all-four PASS, and create a
separate binding containing that file's actual SHA256 plus explicit GO. Keep the
template inert. Preparation does not acquire the canonical lock or execute this
helper, including a dry run.

The helper checks the exact staged TREE, APP, semantic index and MERGE_HEAD;
validates all four native footers, source/resource/cleanup proofs and the pinned
gate runner/binding; takes the canonical lock without waiting; then permits one
ordinary `git commit -F` with parents [edfc3ed, b622c897]. It runs the original
five actual-HEAD QA commands against b622c897, both merge-commit and base-diff
whitespace checks, native publication at 180 seconds, and published verification
at 120 seconds through the existing supervisor. The published build stamp must
name the actual new commit.

Before commit and before push it reads existing PR1693, Git remote feature HEAD,
GitHub feature ref and current DEV ref. The template requires current DEV still
equal reviewed b622c897 by default. ROOT may explicitly set
`require_remote_dev_exact_reviewed_base: false` in the separate GO binding for
this feature checkpoint. That permits an advanced DEV while recording its actual
SHA; the exact qualified integration base and all five QA arguments remain
b622c897. It neither qualifies the later DEV tree nor authorizes a DEV merge.
Fresh HEAD CI and separate PR merge admission still follow. A merged/closed/draft
PR or competing feature head always refuses delivery. No head or base is guessed.

At most one normal feature push updates the existing PR. An uncertain push
transport or wrapper result always receives bounded, read-only Git/API/PR
reconciliation and never repeats the mutation. Commit uncertainty preserves
local HEAD/MERGE_HEAD/parent readback and stops. No PR creation/edit, ticket
write, CI dispatch/rerun, DEV merge, force, amend, reset or own-lap write exists.
Receipts remain outside the repository; owned scratch is removed only after
supervisor descendant cleanup is verified. New HEAD CI and DEV acceptance stay
pending after delivery.

ROOT's reviewed launch, after separate explicit authorization, uses the existing
transport activation environment, Python3.11, a separate GO binding and a fresh
outside-repository output path. This document is not execution authorization.
