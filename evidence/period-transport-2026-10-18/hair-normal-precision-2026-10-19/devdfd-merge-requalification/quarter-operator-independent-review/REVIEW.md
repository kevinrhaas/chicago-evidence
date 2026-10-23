# Quarter-vector operator: independent source-only review

2026-10-19. Reviewed /workspace/shared/horse-neck-quarter-operator-source-next, supplied archive SHA57a4434a215a608a0d0bbb1046fa16457540fed6d7a5f75271a68ab9331327a8, together with exact called frozen exporter and metadata source signatures/field accesses. No imports or horse input/evaluation/export/metadata production/Khronos/capture/SAT/browser operations executed. Only source/data-pin manifest text and helper source bytes were read and hashed. All 47 declared source pins match current bytes; both helper directories' .py/.mjs inventories are fully included. No release or acceptance.

## Argument and field contracts

stage_export invokes persisted_trial.run_once(output_dir,baseline,candidate,source,explicit_vector), matching the frozen definition. Its baseline and candidate directories and source edit filename match the frozen verified_inputs conventions. Explicit vector file must equal 24 entries of0.25; frozen explicit_parameters additionally enforces numeric/nonboolean/finite bounded inputs. Python process separation prevents cached ownership/module collisions between exporter and metadata helper namespaces.

stage_metadata invokes produce_metadata with eight arguments in its actual required order: ear parent bytes, actual new bytes, actual sparse proof bytes, ear manifest/proof/source/authority bytes, and original090_inputs dictionary with exactly baseline/producer090/head/ears. Export output names UNACCEPTED-candidate.glb and sparse-export-proof.json agree with persisted_trial. Metadata consumes actual output_sha256/input_pins/authority_sha256/sparse_proof keys present in exporter receipts. Returns are three encoded JSON byte strings, correctly written as manifest.json, authority.json and packet.json. Metadata canonical filenames candidate.glb/sparse-export-proof.json match packet links, and both copies are reread for byte equality.

stage_khronos reads metadata/candidate.glb and invokes validator.validateBytes(Uint8Array,{uri,maxIssues}); report.issues.numErrors/numWarnings are the expected local validator report fields. It saves the report before marking any error or warning nonzero. It never implies REST or collision acceptance.

## Failure and timing semantics

The operator verifies source pins before workers, claims a new outer directory exclusively, records vector/pins/commands/phase logs and status, and starts each worker in a new process group. First nonzero result stops later stages. A phase timeout kills that group and records124. Spawn/kill/wait exceptions record127 and stop. Export retains UNVALIDATED bytes before readback and its own failure receipt; metadata does not run after exporter failure. Each phase gets at most30 seconds and the three-worker loop shares90 seconds from its own start; source-pin hashing and initial receipt setup occur before that90-second clock, so the cap is worker-loop time rather than total invocation wall time. No parameter retry/search or silent source-pin regeneration exists.

No definite unexecuted API mismatch, wrong argument order, missing expected exporter field, or serialization handoff blocker found. This is source feasibility only; actual workers, parameter feasibility, byte artifacts, validation results and timing remain unexecuted. The harness lacks general durable guarantees for filesystem exhaustion or errors during initial source hashing/receipt construction; ordinary failure evidence inside an established writable trial directory is otherwise preserved.

## Mandatory boundary

Success intentionally remains UNACCEPTED with independent REST readback PENDING. That independent check must verify actual output geometry/attributes/storage/authority and protected head/portal rows before any capture. This operator runs neither adapted full-scope collision nor REST verification and cannot substitute metadata assertions or zero Khronos findings for either. No actual execution is authorized by this review. Root remains sole release authority.
