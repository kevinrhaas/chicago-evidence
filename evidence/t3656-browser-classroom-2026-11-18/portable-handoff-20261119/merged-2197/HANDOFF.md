# Durable handoff — PR2197 merged

**T3656, T3657 and T3658 are delivered to dev.** PR2197 merged at
2026-11-19 04:14:38 UTC as `256364cc92a42dd6b76f326a01a048fe5f98f027` and the supported ticket
workflow marked all three done in pushed ticket commit `7ec0f0a0ddb0226859b7bbbe648deca5bc113090`.
The exact merge tree equals validated candidate 539f09 and preserves DEV8c.

[Final merge and gate receipts](../../merged-2197/README.md) include source 1,397 plus
successful aggregate, passing unchanged moving retry, upload 32 carry-forward,
the scoped renderer matrix and exact DEV publication proof. Original failures,
recovered phone stage 1 and b501 geometry-only reuse limits remain preserved.
All validation was complete before the guarded expected-head merge.

After tests/merge/freeze release, ticket settlement intentionally mirrored
`tickets.json` into primary `site/4d`. Historical fullhash receipts prove the
tested fixture; they do not claim current mirror equality after settlement.

**PR2205 / T3663 is parked, draft and unmerged** at pushed fc51c9ef. Its next
step is integration onto actual current DEV with upstream changelog preserved,
then its required native/published browser and source/renderer validation.
Its prepared browser harness remains unrun in this checkpoint. PR2199 is the
older superseded follow-up, not the next delivery. No production promotion
was requested or performed by this archive task.

The [updated portable recovery JSON](../../merged-2197/live-recovery-merged.json)
keeps earlier history and identifies the completed delivery. Evidence_checkpoint
retains archive ownership until explicit handoff. Older “pending” snapshots
remain historical; this merged record is the current continuation point.
