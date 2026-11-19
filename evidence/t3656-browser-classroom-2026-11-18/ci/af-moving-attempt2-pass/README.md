# Moving-only retry passed with unchanged ceilings

Run 44446919852 attempt 2 / job 135313287687 completed at 04:11:48 UTC with
PASS — every moving frame inside the ceiling. Its normal published build
uses exact PR merge 8d292ea, af into DEV69d. The same desktop 1280×800 / 1835
command ran with --verify --gate. No policy, input or assertion was changed.

The gate measures flora.update maximum and p95 per tier. Full stays 60/15 ms,
Balanced 32/9 ms and Light 21/7 ms (maximum/p95). Balanced flight now reads
**7.5 ms maximum / 1.2 ms p95**, compared with the real failed attempt's
**33.1 ms maximum /1.7 ms p95**. Its 32 ms maximum was not raised. Exactly one
unchanged retry was authorized; this archive adds no retry or workflow action.

| Tier | Move | Scripted p95 / max ms | Flora p95 / max ms | Flora p95 / max ceiling ms |
| --- | --- | ---: | ---: | ---: |
| full | walk | 4.4 / 10.8 | 3.9 / 9.9 | 15 / 60 |
| full | turn | 5.3 / 11.8 | 4.6 / 11.2 | 15 / 60 |
| full | flight | 4.5 / 7.3 | 3.9 / 6.0 | 15 / 60 |
| full | travel | 2.4 / 23.3 | 1.1 / 22.7 | 15 / 60 |
| balanced | walk | 1.4 / 18.1 | 0.5 / 4.2 | 9 / 32 |
| balanced | turn | 4.5 / 13.1 | 4.0 / 12.6 | 9 / 32 |
| balanced | flight | 2.1 / 8.1 | 1.2 / 7.5 | 9 / 32 |
| balanced | travel | 3.5 / 11.0 | 3.0 / 10.6 | 9 / 32 |
| light | walk | 0.9 / 3.6 | 0.3 / 3.2 | 7 / 21 |
| light | turn | 3.1 / 5.6 | 2.7 / 4.9 | 7 / 21 |
| light | flight | 1.3 / 5.4 | 0.5 / 4.8 | 7 / 21 |
| light | travel | 1.5 / 4.0 | 0.6 / 3.2 | 7 / 21 |

All 12 rows are inside their respective unchanged ceilings. The complete log
also contains 12 each zone/ground/yard verification records with 0 mismatches,
plus 2 far spread-versus-one-frame equality records with 0 mismatches. The
verifier found no pageerrors record and the final passing gate verdict.
verification.json retains all values, row timestamps and correctness lines.

The [original failure](../af-source5-moving-retry-20261119/attempt1-moving-failure.log),
[independent retry rationale](../af-source5-moving-retry-20261119/moving-retry-rationale.json)
and [single retry request/response](../af-source5-moving-retry-20261119/retry-response.json)
remain immutable. The complete before/after request receipts and their hashes
are linked in verification.json. The difference does not prove why the first
reading failed; this is a CI SwiftShader scripted desktop measurement, not a
sustained weak-device or phone performance claim.

Upload 32 is the original successful attempt 1 job, carried forward by GitHub
under attempt 2's new job ID; its raw bytes are identical and it was not rerun.
The separate source aggregate is still queued in the coordinator snapshot;
all eight native partitions passed 1,397 steps. Scoped renderer coverage and
DEV8c's targeted publication checks are complete, but no overall release pass
or DEV merge is claimed before the source aggregate and final head review.
