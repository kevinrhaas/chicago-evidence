# PR #1340 actual published mobile sections 4–6

This packet preserves three closed native `--published` mobile groups on HEAD `78b11b7a8e49126a8a5724a4035ea961461a4f49`, TREE `bac0441d0b3cb0db4815b7b6e4a0fd049a365192`, APP `ee7822334b9e11c2321d243b26ecf65ca095656a`. Sections 4, 5 and 6 actually passed 44, 30 and 24 assertions under their original 600-second supervisors. Every source/index/full published mirror before/after guard is retained, with byte-exact aliases where duplicate. All three actual phone PNGs, launch resources, real command/result/cleanup receipts and complete native logs are included.

The external controller stopped with `BrokenPipeError` after section 6 passed. Its stopped state and the minimal durable-output resume source/diff are preserved. Mutable running logs/state and section 7 are excluded. This is partial coverage only, with no whole-gate, photographic-quality, current-CI or DEV-merge claim.

For restoration, decode each `payload_path` as gzip, verify `original_bytes` and `original_sha256`, and restore only the desired `original_path`. Alias rows reference exactly the same encoded bytes while retaining each original path. All originals remain available.
