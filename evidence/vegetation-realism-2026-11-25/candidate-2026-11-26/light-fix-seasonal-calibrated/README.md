# Current seasonal Light fix: actual failed-profile revalidation

The complete staged seasonal source is tree `48f1bb2124e3f95e9262baf10b87ce1c020722e5`, app tree `1a71391e7f5e4a116a99114de82daf72b1da9acd`, on Core `3bdf2349cf29f374833d015e91b84dab6611d636`. This is before seasonal app authorship. See [the complete source and seasonal images](../light-fix-seasonal-working-source/).

All three predeclared allocations finished. Two reached the explicitly required actual EPYC7763 / four-core profile and both passed every unchanged stock desktop ceiling, with zero browser errors. The third was an unsupported Xeon8573C allocation, stopped before source and timing and retained. Every actual reading is retained; no timing failure is discarded.

| Allocation | Full /13750ms | Balanced /10500ms | Light /7000ms |
|---|---:|---:|---:|
|1|11806.3|10025.8|5606.8|
|2|11908.7|10158.4|5646.0|

The previous seasonal candidate measured Light7314.6ms on that same CPU/profile. These readings are approximately23% lower. Both current readings have the exact same per-tier triangles/calls: Full3044315/5962, Balanced2434867/5903, Light1012277/3574. The stock published1835 town-backyard benchmark still uses1280x800 DPR1, two measured frames, zero warmup and CPU throttling4. No density, geometry, raster, sample, helper or ceiling is reduced to get this pass. These are software-renderer benchmark readings, not hardware FPS.

The source-before/source-after receipts verify the entire candidate tree and every owned source hash; raw job metadata/logs, reports, artifact metadata, ZIP digests and unsupported CPU are retained. The strict qualifier independently verifies each allocation, stock helper/ceiling bytes, both complete report footers and real profile limits.

This resolves the earlier performance hold only for this new source. The original failed candidate and its [negative evidence](../reading-fix-seasonal-calibrated-hold/) remain unchanged. Complete fresh Native, actual Core Dev merge, two seasonal ticket commits, committed preflight and all fresh authored-head required CI/published smoke/frame-memory checks remain required. Neither a seasonal app commit nor a Dev merge is claimed by this evidence.
