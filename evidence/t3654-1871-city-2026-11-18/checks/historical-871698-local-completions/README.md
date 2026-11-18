# Dated local completions on 871698

All three invocations retained clean head `871698ae94659100fcb8894f4967d4b15c62150f` and base `169404c9f99d2defeca2b05f2364c868a4f4e745`. Each bundle includes the exact wrapper, terminal log, per-check timings, original exit-0 process receipt and final receipt.

| Partition | Checks | Self-tests | Wall seconds |
| --- | ---: | ---: | ---: |
| 3/16 attempt 1 | 90 | 25 | 255.854 |
| 4/16 attempt 2 | 89 | 25 | 455.878 |
| 8/16 attempt 2 | 89 | 25 | 345.524 |

The dated local-only snapshots progress from 774 ordinary declarations covered / 602 missing to 860 covered / 516 missing, with no ordinary duplicates. Both remain partial local coverage. Their frozen mixed-history ledgers retain earlier failures and separate declaration layouts. The later reviewed local-plus-hosted union is a different proof, archived next door under `historical-871698-assertion-union/`.

These results predate upstream integration and receive no automatic credit for 6409. Absolute paths in original wrappers and receipts identify the execution environment and require deliberate restoration for reproduction.
