# Six focused canonical checks and separate strict-mode attempt

The canonical receipt records six successful commands on 19 November 2026: asset freshness, derived-output consistency, source-use consistency, unique IDs, changelog entries and ticket-ID collisions. Freshness reports 1,126 fresh assets, zero stale assets, zero errors and 338 existing warnings. These are focused checks, not a complete current source gate or browser verdict.

The earlier attempt added `--strict` to `validate.py --stale` and exited 1 solely because strict mode treats the 338 warnings as errors; it found zero errors. That attempt is retained unchanged under `strict-attempt/`, with `complete:false`, rather than relabelled as a pass. The canonical workflow does not supply `--strict`; the later invocation used the canonical command and exited 0. No application assertion was removed or weakened by this archive task.

Both attempts ran while HEAD was `7c1c1dda52d130b5d4545fd26e384a8711634e08` and the combined staged tree was `852dde5df062ff770cddc19b1c9afef45aab16ad`, against dev `c23d8a9e85bf37de9c2eb2dce9118cb709edf0da`. `commit-binding.json` verifies that only STATUS and portable checkpoint metadata differ between those focused inputs and committed source `933e1f9e00f378436bb2c9396b634696dc6f3138`; runtime and checker bytes were retained.

Original receipts/logs and their maps are preserved. Later publication, current source CI and the new browser batch have separate identities and acceptance requirements. Historical 6409 successes are not imported as new-head passing results.
