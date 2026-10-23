# Standing horse: fresh serial validation next — 2026-10-23 11:50 UTC

PR1175 is merged and its wagons, covered-wagon variants, Brougham and Bardwell delivery are publicly verified. PR1208 and PR1213 are closed as superseded. Broader photographic, occupied-vehicle, walking, harness and riding tickets remain open.

The complete 40-file standing-horse change remains unchanged on base e4745b3c, staged tree be37faec911f51b5d0bad9c11bed4e352b7a4b12, in /workspace/chicago-waistcoat. Its full source is already GitHub-backed in CURRENT-HORSE-AND-MIRROR-REPAIR-SOURCE.zip (SHA256 5b07a53662b10d709960f598740cfda99e028042cb49dee54109925f2814c201). No horse app commit or PR exists yet: the required full preflight must pass first.

The fifth whole preflight was stopped at 11:45:05 after 703 completed timing rows and 1511.37 seconds. It stalled creating nested Node fixture processes at the environment process ceiling, not a completed product verdict. Only its verified owned process group was stopped; owned cleanup reports no remaining children. Preserve all five nonpasses. Never combine their partial passes into a whole-suite pass.

Both stalled tests (ticket claim lock and PR-stuck) now PASS individually in serial with the standard Node launcher: 3.60 s and 7.51 s. Node --single-threaded is NOT used for the next gate; it was rejected in NODE_OPTIONS and an external probe did not reduce the observed four-thread count. The next fresh whole run uses CHECK_JOBS=1, V8 pool 1, UV pool 1, math threads 1, and per-process Git index/pack threads 1 with preload disabled. Git's default threaded index operations also hit the process ceiling; the per-process resource settings retain normal Git semantics and source bytes.

Use the FINAL waitid helper (SHA256 60ea8bdddc4491cdc788c2574194e2e33410c0c01c3d9a9a0c73a9751b37df2f), not the earlier helper in the 11:11 checkpoint. Its actual main-exit-status/adoption proof passed. It reaps only newly adopted own descendants. The prior PID1 debugger-attachment approval rejection remains binding; no PID1, old orphan, system service or other agent process was touched. Fresh piped shell launches can hang at the ceiling; a single owned PTY command with login:false and the normal approved environment works.

Next gate directory: /workspace/shared/T2800-STANDING-SERIAL-STANDARD-LOW-THREAD-FULL-PREFLIGHT-ACTUAL-20261023. Only a complete actual PASS can release the prepared serial postgreen writer to commit, push and republish. Then create a new DEV draft PR, collect three fresh applicable normal CI runs (human workflow excluded only by a fresh exact changed-path proof), and perform the actual mobile/desktop yard checks. Ordinary green DEV merge remains authorized. Claims for all eight owned people/transport tickets were renewed and pushed at 11:10 and expire at 14:10 UTC. ROOT remains the sole canonical ticket writer. Continue working; no photographic completion is claimed.

---

