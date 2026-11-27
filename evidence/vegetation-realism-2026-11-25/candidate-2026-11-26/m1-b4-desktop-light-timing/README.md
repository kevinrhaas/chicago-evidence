# B4 desktop Light timing failure retained

Current core `b4cd05e12b3c2c113583682b9ba0eda27c37bfb8`, grid run 45927844531, desktop job 140273299979: Full 11,610.6 ms < 13,750; Balanced 9,886.1 < 10,500; **Light 7,213.1 > 7,000**. The EPYC 7763 four-core machine has an existing calibrated ceiling. The failure is a real failed gate and blocks merging.

The original log is preserved as exact decoded UTF-8. Its three geometry/draw counts match the prior C9 run exactly. That older successful job ran on an uncalibrated Intel Xeon 6975P-C: its lack-of-ceiling warning is not proof of passing the EPYC ceiling. Raw CPU times and bare-screen ratios across those machines cannot waive this failure. The current EPYC bare screen read 105.7–106.6 ms; the historical same-model calibration records 99.2–99.7 ms. This motivates a repeat, not a conclusion that the runner caused the failure.

One execution repeat of only this exact job, with unchanged source/settings/limits, is pending the original matrix finishing. GitHub rejected the initial rerun request because the workflow was still running; no repeat has executed. The other fourteen cases continue. The failure and all resulting attempts/runner identities must remain recorded. A new uncalibrated warning alone must not be presented as this calibrated case passing. No geometry, population, radius, raster, samples or ceilings have been changed.

This folder contains a pending failure investigation, not merge qualification. Full local Native/preflight and other CI evidence remain separately versioned. No heap snapshot is included.
