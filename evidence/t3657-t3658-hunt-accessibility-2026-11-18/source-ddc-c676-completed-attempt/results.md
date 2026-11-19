# Frozen ddc local source gate receipt

Head `ddc78606998ea8aee589941c6ab6cae76a80440a`; tree `fa70a0164ccbef670529470937b170677c5a99b0`.
Frozen base `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`. Worktree `/workspace/chicago-followup-validation`.

| Part | Final verdict | Steps | Elapsed |
|---|---|---:|---:|
| 1/8 | PASS | 175 | ~308s |
| 2/8 | PASS | 175 | 412.810s |
| 3/8 | PASS | 175 | 334.880s |
| 4/8 | PASS | 175 | 409.392s |
| 5/8 | PASS | 174 | 250.181s |
| 6/8 | PASS | 174 | 244.851s |
| 7/8 | FAIL (1 step) | 174 | 320.332s |
| 8/8 | UNRUN | — | — |

Part 7 stopped the sequence per the stop-on-real-failure instruction. Its single failed label was T-3575 WebXR wiring; `tools/check_xr_mode.mjs:266` expects the old inline keyboard guard after the T-3658 capture extraction. The current main callback still explicitly blocks XR, arrival and window mode. No fixes, budget/assertion changes, commits or reruns were performed.

Part 1 has a complete final CHECK PASS but its process exit status was lost during context compaction; its duration is approximate. Parts 2–6 exit 0; part 7 exits 1. Each invocation had a 900s timeout plus 5s kill grace, 4 workers, Node22, required readers and required base.

Full logs: `/tmp/t3657-ddc-source-part1of8.log` through `part7of8.log`. Machine receipt includes SHA256 hashes and exact timing: `/tmp/t3657-ddc-source-provenance.json`.

Preflight changelog and ID checks are UNRUN because part 8 was not started. This is not a green full gate. Results apply to ddc/c676 only; newer remote DEV21f609 is outside this proof. Final combined-head CI and renderer gates remain necessary.

Final validation worktree and real tickets clone are clean; ddc, c676 and preserved b501 branch are unchanged. Primary source/mirror and real PR worktrees were not changed by this run.
