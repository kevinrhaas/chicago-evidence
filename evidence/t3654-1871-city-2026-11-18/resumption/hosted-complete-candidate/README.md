# Dated recovery snapshots

The progress and PR-body files are byte-preserved snapshots; their evidence link intentionally points to the previous durable checkpoint 9a103dc. `snapshot-provenance.json` records the capture time, original/frozen paths and hashes. The ticket file is the exact committed T-3654 content from chicago-tickets commit `eff0df4761feaf24e607b150f3fafe698d58f8c0`, obtained read-only with `git show`.

These files preserve recovery context and do not replace the immutable hosted-source receipt or the separately captured browser metadata. The research-site candidate remains unapplied future work. No ticket, PR, application or workflow was changed by this archive task.
