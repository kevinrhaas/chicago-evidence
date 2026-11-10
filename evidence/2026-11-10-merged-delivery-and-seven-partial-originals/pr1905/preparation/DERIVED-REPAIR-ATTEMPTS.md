# Bounded setup errors and final receipt

- Initial authoritative sparse `compile_scene.py --all` exited1 before output writes because `data/exclusions.json` was absent. Exact traceback is retained in `COMPILE-SPARSE-FIRST-ATTEMPT.log`.
- Metadata was materialized from the sparse branch's exact current dev base/committed source cameras, excluding native/image assets. The next `--all` compiled1812, producing the NW grade-only delta, then exited2 because the committed terrain heightfield binary was excluded. Full partial transcript retained as `COMPILE-ALL-PARTIAL-HEIGHTFIELD-MISSING.log`.
- Materializing the existing committed terrain binaries allowed full authoritative `--all` and `--all --check` to pass across1812,1835,1904. No active full-repo inputs were written or overridden, and no compiler code/output was manually stamped.
- The expanded sparse patterns omitted `changelog.d`, so the first attempted announcement edit failed without writing. An attempted `git sparse-checkout add --no-cone` was rejected because this Git subcommand accepts the existing mode instead of that flag; plain `git sparse-checkout add /chicago/4d/changelog.d/` materialized the already committed file successfully.
- One changelog check was invoked from repository root rather than the app cwd and failed MODULE_NOT_FOUND. It was immediately rerun from `/tmp/nov9-group-cobweb/chicago/4d` and passed. This note is a retrospective error index, not a raw full transcript of those shell calls.
- Transient unpushed local derived commit `a0b58cce92def40b90c982e219af66e8a99998f0` was amended on root's explicit instruction to include the truthful pictured-badge announcement. Final derived commit is `4d8292da47df257cbdbec8476cb54de9a2385706`. No GitHub push by this child.

Authoritative final logs are `COMPILE-ALL-AUTHORITATIVE.log` and `COMPILE-ALL-CHECK.log`. Exact limited before/after, command exit codes and rule interpretation are in `NW-SIDECAR-COMPILER-RECEIPT.json`.
