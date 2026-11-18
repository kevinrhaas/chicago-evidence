# Empty named-structure boot packing

The original 3f81 source CI part 7/8 failed one of 174 checks because 1871/index.json had no boot descriptor. The writer skipped every scene with zero available named-structure sidecars, even when an empty index was valid and the city buildings belonged to its context layer. The historical CI failure remains in `../../ci/supporting-3f81/`.

The repair emits the normal descriptor and empty shared values with no part files. Its checker explicitly refuses missing indexed records and malformed shared tables. `focused-proof/` retains the exact patch/candidate, a reproducer and 767 committed input hashes at 7e99: the original CLI fails on the real empty 1871 index, while the candidate exactly rehydrates all 765 real1835 records. Node 22 self-tests cover empty/nonempty scenes, the 50-row boundary, deterministic repacking, stable sparse positions, nine corruption refusals and stale-part cleanup. Restoring either the old writer or old missing-record checker makes the regression fail.

The later full c0 publication checks1119 records (68 in 1812,765 in 1835,286 in 1904, zero named records in 1871). Its native 1871 empty-boot readiness is verified in `../context-source-use/native-after-c0c235/`. No full current-source or legacy-browser gate is asserted by these focused checks.
