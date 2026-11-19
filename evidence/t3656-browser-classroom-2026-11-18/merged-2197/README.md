# PR2197 merged to dev; T3656 / T3657 / T3658 done

PR2197 merged at **2026-11-19 04:14:38 UTC** as
`256364cc92a42dd6b76f326a01a048fe5f98f027`. The squash commit has sole parent
`8c605db0571e29ee9da6d8aba5181451d9d84db8` and exact tree `6b2c34dfa605a475fc9695abcfb2d0c0b019bb76`,
matching the isolated validated af + DEV8c candidate 539f09. Independent GitHub
reads confirm the closed/merged PR, commit tree/parent, then-current dev ref
and successful source workflow. No production promotion is claimed.

Before the expected-head merge, all fourteen current checks were successful:
eight source partitions (1,397 steps), their aggregate, moving-frames,
upload-release, both fresh renderer ranges and report. The source aggregate
completed at 04:12:48; its original source filename says “queue observation”
but the archived receipt is explicitly terminal SUCCESS. This closes the
earlier queued status without rewriting those historical receipts.

- [Source partition matrix](../ci/af-source-eight-parts-awaiting-aggregate/README.md): all eight retain exact af/DEV69d PR merge attribution; [aggregate log](source-aggregate-pass.log) and independent workflow receipt establish completion.
- [Moving retry](../ci/af-moving-attempt2-pass/README.md): all 12 rows passed unchanged tier ceilings; Balanced flight flora 7.5 ms max / 1.2 ms p95. Original 33.1 > 32 ms failure and exactly-one-retry proof remain. Upload 32 is the original successful execution carried forward, not rerun.
- [Renderer matrix](../renderer/final-af-scoped-coverage/README.md): original desktop DDC/b501 and local 347 phone cohorts retain their scopes and repeated guards; fresh af 13–15 passed 314/0 at both widths. Recovered phone stage 1 still lacks a normal supervisor end receipt.
- [DEV8c publication proof](../dev8c-publication-complete/README.md): exact merged candidate passed targeted publication/parity/site-budget/syntax checks, 0 errors / 340 warnings, unchanged limits. The merged tree matches that candidate exactly.

The supported `ticket.mjs settle` finished with exit 0 in 7.497s and changed
exactly T3656, T3657 and T3658 to **done**, linked to PR2197 with closed_at equal
to the actual merge time. Ticket commit `7ec0f0a0ddb0226859b7bbbe648deca5bc113090`
matches remote main and the three exact ticket Git blob hashes were independently
checked. The settle output and terminal receipts are retained here.

Settlement intentionally mirrored latest `tickets.json` into primary
`site/4d/` **after all tests, merge and explicit freeze release**. Historical
7,667-file hashes remain valid test-time evidence. No current local-mirror
byte equality is claimed after this supported bookkeeping step.

The authoritative live recovery snapshot is `live-recovery-merged.json`.
It preserves obsolete current fields in a historical snapshot and records
the completed merge. **PR2205 / T3663 remains parked, draft and unmerged**;
its pushed fc51 checkpoint and prepared-not-run browser fixture remain saved.
Future work must integrate it onto actual current DEV, preserve upstream
changelog content and complete its own required validation before merging.
