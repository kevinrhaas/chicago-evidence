# All eight af source partitions passed; aggregate pending

At 2026-11-19T03:58:03.810Z, run 44446919895 attempt 1 completed all eight
partitions, totaling 1,397 steps. Every complete log identifies PR checkout
8d292ea1f29dfc84e3ccd43a7bed53d0f2d526bb, merging af into DEV69d. The separate aggregate
job 135327670033 was queued. This is not an overall workflow success claim.

| Partition | Passing steps | Completed job / raw log | SHA256 |
| --- | ---: | --- | --- |
| 1 | 175 | [135301363551](../../ci/af-source-parts1-6-20261119/part1-pass.log) | `a5f3acba9eecef028ade24066cb02b2d993c5b817ac10a7f334c03ea541ac214` |
| 2 | 175 | [135301363558](../../ci/af-source-part2-20261119/part2-pass.log) | `8f04b84c978b0ebffba49d9624d3f0e2b59694be3447fb1f4d350d78349b0d72` |
| 3 | 175 | [135301363687](../../ci/af-source-eight-parts-awaiting-aggregate/part3-pass.log) | `4e3ef03084ea049daa7f492dbcc9cc73173315d7e1970cf083535171d7bba109` |
| 4 | 175 | [135301363661](../../ci/af-source-eight-parts-awaiting-aggregate/part4-pass.log) | `e98ddf59f1e76edf160a7ad33971478ab0a9c9f3c90cd8e7928a958083865726` |
| 5 | 174 | [135301363194](../../ci/af-source5-moving-retry-20261119/source-part5-pass.log) | `c827982f2b044a172b3d5e8d06fe1b5db51a9840ac178f7d60e413ea90d2e553` |
| 6 | 174 | [135301363586](../../ci/af-source-parts1-6-20261119/part6-pass.log) | `3d1741ac9c2b22b4b3f3bb59e361dbf4a828650af4a29dee0ab4268855f3b417` |
| 7 | 174 | [135301363633](../../ci/af-source-eight-parts-awaiting-aggregate/part7-pass.log) | `d8a4cfa16f870f7a4bf3ca07ecd53184410fcdabec22f959572437c761f6c472` |
| 8 | 175 | [135301363618](../../ci/af-source-eight-parts-awaiting-aggregate/part8-pass.log) | `13743c36509e6658af49969400de9e7e756d376a5abc36dbd44bda6172b8896f` |

Partitions 1/2/5/6 link to their unchanged earlier archives; only 3/4/7/8
are added here. Each final CHECK PASS and exact checkout was independently
verified. Intentional negative-control failures within individual logs do not
replace their final passing partition verdicts.

The new DEV8c publication dependency has separate executed targeted proof in
[dev8c-publication-complete](../../dev8c-publication-complete/README.md).
These source logs retain their actual af/69d attribution. No source rerun,
browser run, application change, deployment or merge was performed here.
