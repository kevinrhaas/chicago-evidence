# Fresh smoke plan and independent review

Source is now committed at `be56fb269eee6aa7963b8a8d76d5a950f56f857c`, tree `a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5`. Tracked source is clean and the preserved content is the same audited tree that passed the complete preflight: **1,065 steps / 384 self-tests**, result 0 in 657.702s, with 721 owned descendants reaped and none remaining.

`/workspace/.cloud-setup/de91-integrated-smoke.py` correctly schedules 24 entirely fresh legs covering every part 1–15 exactly once per viewport. It starts mobile 14 and desktop 14 to exercise the corrected public-image path, then runs the remaining eight mobile groups and fourteen desktop parts. It uses the published mirror and binds the new HEAD/tree; old receipt prefixes and old 20 passing legs are not reused.

The initial published manifest has **5,387 files / 383,212,008 bytes**, including the new build stamp. Do not republish or change source while the matrix runs. Run one browser command at a time, with no simultaneous validator pool. Normal TLS verification remains enabled through the provided runtime CA trusted in Chromium NSS.

Each leg requires actual command and outer return code 0, no timeout, positive staged checks, SMOKE PASS, zero page errors, and complete owned-child cleanup. Fresh prefixes preserve original attempts. Operational limits are 1,800s normally and 3,600s for part 13, based on measured long UI runs; they do not waive application assertions or establish budget compliance. The 600s foreground timing result is recorded separately.

`smoke_budget.mjs` was inspected and run only as a read-only planning command. Its historical 62m22 sum leaves eleven desktop and five mobile parts unmeasured. Do not present that incomplete sum as this tree's full forecast. The current whole-body workflow cap is 150 minutes; the nightly 40 minute cap per leg is a different bound. Preserve actual elapsed times and any budget misses separately from functional coverage.

The separate `/workspace/.cloud-setup/verify-de91-smoke-complete.py` closes the final binding gap: it checks complete status, all 24 command receipts and cleanup, all 15 parts at both viewports, actual HEAD/tree and clean source, the initial manifest's hash, exact current mirror file set, and every file's size/SHA. The hashed build.json also protects the build stamp. Root should run it after the matrix; it was not executed by this audit. Optionally reparse positive staged counts and assert stored outer return code 0 in that final verifier; the driver already enforces those conditions.

Before delivery, refresh actual PR #1279 H/B/Q and required workflow/check evidence. Old test merge Q 01977d66 / H 3290195d evidence does not certify the new source. Merge ordinarily into DEV only on current normal green checks, then verify public DEV source/assets and the yard viewpoint. No admin bypass, uninformed CI retry, or production promotion is authorized. Complete only the three shipping children; retain the broader photographic, native qualification, gait/driver and interaction work.

[Detailed review](/workspace/.cloud-setup/logs/transport-recovery/de91-fresh-smoke-driver-review.json). [Post-preflight preservation](/workspace/.cloud-setup/logs/transport-recovery/incoming-de91-preservation-post-preflight.json). This audit started no browser or gate and changed no application files.
