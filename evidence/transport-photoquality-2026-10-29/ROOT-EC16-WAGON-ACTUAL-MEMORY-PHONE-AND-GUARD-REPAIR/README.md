# PR 1340: closed ec16 wagon checks and explicit guard repair

Native owners passed. Fresh 1904 memory passed the original limits: desktop 1112.882 MiB / 1125 and phone 396.648 MiB / 400. Timestamped phone farm-master diagnostic passed with three correct selected-LOD HTTP hashes and five actual PNGs personally reviewed by root.

Full application gate 01 is NONPASS: 1104 of 1105 steps passed, one stale protected wagon-placement baseline failed. Incoming DEV had intentionally moved the Green Tree wagon with its shed in T-2376, commit f2635549179a61fd684336248418ba1e48aaeea9. The complete old/new semantic comparison preserves all 81 identities, other 80 records, dimensions and eligibility. The explicit repair changes only the non-runtime protection JSON; checker assertions and runtime assets are unchanged.

Original passing owner/memory/phone receipts remain bound to their original source. A separate exact source bridge records the guard-only transition. Original failed gate and all logs are retained. Gate 02, a new application commit, checked branch push, current CI, published full smoke and DEV merge are pending at this checkpoint. The historical BOTH farm diagnostic remains NONPASS. This evidence commit is a recoverable backup, not application delivery.

Payload manifests record original absolute paths, SHA-256, byte counts and deterministic lossless gzip encoding. Restore gzip payloads by decompressing and verifying the original SHA; unencoded files are exact original bytes.
