# Genuine 933 source failure and dated partial successes

Source run 44444393454, part 1/8, failed exactly one of 175 steps: the derived liberty count. Raw job 135292880886 logs and metadata preserve the failure; the actual checkout `9e56164a47ae1688039555508e687e0fb9158fc8` has the exact 933 tree `a23d5cdae537c07952174887776dbd6a67cbbe50`. This was a real input defect, not an old-checkout mismatch.

The bounded closure also records part 8/8's genuine 174-check PASS and PR-only changelog success, plus the upload-release job's 32-check PASS on the same dated tree. They do not turn the failed source gate green or establish complete supporting-workflow success. No successor-head credit is granted.

The combined 21-file manifest/map is under `../933-terminal-822-initial/`. Its explicit note maps the failed summary's active metadata pointer to the frozen same-hash snapshot; no later live metadata was substituted. The owner repair and fresh successor publication are separate records.

The later terminal boundary preserves all eight old native parts: part 1 genuinely failed, part 8 passed, and six were cancelled. Cancelled source-part-4, human and moving-frame logs are retained without pass credit; the earlier upload-release success does not make its cancelled workflow fully successful.

Root then verified all eight native parts were terminal and only aggregate job 135302483215 remained queued. A narrowly targeted force-cancel of old source run 44444393454 returned HTTP 202; the final metadata records the aggregate and workflow cancelled. This administrative retirement is separate from the six ordinary browser cancellations and does not erase the native part-1 failure. See `terminal-boundary/` and `aggregate-cancellation/`.
