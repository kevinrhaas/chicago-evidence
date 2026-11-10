# PR1921 moving-frames attempt1: preserved actual failure

Exact PR head `facd644869541d81fe5058b0e9f23719a936e907`; CI tested synthetic merge `317e958df2e7826cddb6081f6cba0e25b1f4c4a5` into DEV `8aa1afcac4788764aff9d12a53d3f89bc38d0167` and published build `317e958d`.

Step6, “Walk, turn, fly and ride; hold the flora frame to its ceilings”, failed on desktop1280×800, unthrottled, default1835, Balanced flight: flora.update maximum48.4ms against unchanged32ms. Flora p95 was2.3ms, scripted-frame maximum49.2ms; only one reading failed. All source/worker zone, ground, yard and far-result equivalence controls agreed.

The same row reports a48.1ms maximum far pass. That is accumulated per-pass CPU, potentially spread over frames; it does not identify the offending frame or prove a hot call. No CPU profile was requested; the default50ms detailed-frame threshold also exceeds49.2ms. A specific repair is not established.

1835 has no street_grid layer. Its null dataBase returns before createMaskedPedestrianHeight; the main call is also restricted toYEAR1904. Therefore the new sampler has no1835 construction, queries or index. Module definitions load; the figure-ground helper still dispatches its old formula with null admission. This footprint does not prove zero indirect causality.

The exact Git objects for flora.js, jobs/, data/flora/, measure_walk_frames.mjs and the moving-frames workflow are identical between head and DEV base; full identifiers are in SAFE-DIAGNOSIS.json. No assertion, cap, workflow or source edit is proposed. ROOT requested one ordinary unchanged-source failed-job rerun; attempt1 remains a failure, without a flake claim or permission for a second retry.

Original private log:76,881bytes, SHA256 `1eb72d19115987ae90225746cc051b4673de33dc499f7271b3f4cac9e1e197d8`, bounded below8MiB. Raw log stays local/private. Check: https://github.com/kevinrhaas/chicago/actions/runs/42825131045/job/129860350214
