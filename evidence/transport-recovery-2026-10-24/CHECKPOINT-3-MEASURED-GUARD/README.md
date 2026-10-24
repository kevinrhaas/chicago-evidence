# Complete preflight failure retained; missing measurement corrected

The first full preflight completed657.063s and failed exactlyone of1062steps: the new eyeUVboundary gate had no measured row in the isolation registry. The prior frozen packet omitted it. Changelog/ID checks passed on their then-current committed base; exact final-HEAD checks remain required after sourcecommits.

Run the repository-supported per-tool instrumenter, not a hand-authored exemption: `node tools/measure_step_isolation.mjs --tool tools/test_standing_horse_eye_uv_boundary.py`. It executed the declared unit and measured zero writes in the live tree. The isolation audit then passed all1035keyed step declarations. The resulting four-line registry addition belongs in T-3086's sourcecommit.

A second complete normal preflight is now running with fiveworker slots. No required gate/assertion is disabled and no failed/interrupted run is relabeledgreen. Appcommits,PR,CI,DEVmerge and published delivery are stillpending. This checkpoint supplements the complete binary sourcepatch inCHECKPOINT-2 with the actual measured registry and retained failure/fix evidence.
