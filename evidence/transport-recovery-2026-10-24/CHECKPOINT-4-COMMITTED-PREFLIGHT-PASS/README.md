# Committed transport recovery checkpoint

App branch: `steward/t3083-t3086-t3087-transport-recovery-20261024`. Native Git read verified remote head `8c45c899f696eb87da9f818828bed36668bdfa2b`. Three source commits are recorded in app-commit-receipt.json; their final tree exactly matches the complete preflight source tree.

Complete preflight2 passed: 1,062 steps, zero red, 383 negative self-tests. Canonical derived owner tail passed 59 steps over two laps in424.600s, final lap unchanged (checkpoint2 receipts). Exact committed-head changelog and ticket-ID checks passed. Prior failed preflight1 is retained in checkpoint3; no failure was relabelled.

Cleanup limitation: the old wrapper reported701remaining ownedchildren after each full preflight, separately from the completed code-gate success. The external wrapper now drains all newly owned descendants; a meaningful32-child selfcheck passed with none remaining. Old unowned/PID1 processes must not be touched.

Browser validation across all15stages and bothviewports remains pending. GitHub API and DEVpreview hosts remain blocked by the current runtime networkpolicy; their configuration draft additions have not taken effect. No actual PR, CI success, DEVmerge or public delivery is claimed. No native/world/photographic horse/carriage completion is claimed. Only T3083/T3086/T3087 are this delivery; parent and remaining refinement tickets stay open.
